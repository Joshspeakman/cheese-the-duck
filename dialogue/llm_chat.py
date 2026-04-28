"""
Local LLM integration for duck conversations and behavior.
Uses local GGUF models via llama-cpp-python with GPU auto-detection.
LOCAL ONLY - no external API calls.
"""
import os
import sys
import atexit
import logging
import threading
import queue as _queue_mod
import multiprocessing as mp
import concurrent.futures
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from pathlib import Path

# Configure logging for LLM operations
logger = logging.getLogger(__name__)

# LLM call timeout in seconds
LLM_CALL_TIMEOUT = 15.0

# Flag to track if LLM has encountered critical errors
_llm_crashed = False

# NOTE: LLM inference runs in an isolated subprocess so that a native
# crash (e.g. SIGSEGV in GGML) only kills the worker process, not the
# game itself.  The main process detects the death and disables LLM.

if TYPE_CHECKING:
    from duck.duck import Duck

# Import config settings
try:
    from config import (
        LLM_ENABLED, LLM_LOCAL_ONLY, LLM_MODEL_DIR, LLM_GPU_LAYERS,
        LLM_CONTEXT_SIZE, LLM_MAX_TOKENS, LLM_MAX_TOKENS_CHAT,
        LLM_TEMPERATURE, LLM_MAX_HISTORY, LLM_MAX_THREADS,
        LLM_LOAD_NICE,
    )
except ImportError:
    # Fallback defaults if config not available
    LLM_ENABLED = True
    LLM_LOCAL_ONLY = True
    LLM_MODEL_DIR = Path(__file__).parent.parent / "models"
    LLM_GPU_LAYERS = -1
    LLM_CONTEXT_SIZE = 2048
    LLM_MAX_TOKENS = 100
    LLM_MAX_TOKENS_CHAT = 150
    LLM_TEMPERATURE = 0.8
    LLM_MAX_HISTORY = 6
    LLM_MAX_THREADS = 4
    LLM_LOAD_NICE = 8


def _detect_gpu_layers() -> int:
    """Auto-detect optimal GPU layers for the system."""
    if LLM_GPU_LAYERS >= 0:
        # User specified exact value
        return LLM_GPU_LAYERS
    
    # Auto-detect: try to use GPU if available
    try:
        # Check for CUDA
        import subprocess
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # NVIDIA GPU detected - use all layers on GPU
            vram_mb = int(result.stdout.strip().split('\n')[0])
            if vram_mb >= 8000:  # 8GB+ VRAM
                return 99  # All layers
            elif vram_mb >= 4000:  # 4GB+ VRAM
                return 35  # Most layers
            elif vram_mb >= 2000:  # 2GB+ VRAM
                return 20  # Some layers
            else:
                return 10  # Minimal GPU offload
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, IndexError):
        pass
    
    # Check for ROCm (AMD)
    try:
        import subprocess
        result = subprocess.run(
            ['rocm-smi', '--showmeminfo', 'vram'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # AMD GPU detected
            return 35  # Use GPU
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # No GPU detected or detection failed - use CPU
    return 0


def _llm_enabled_config() -> bool:
    """Read the live LLM setting instead of the import-time fallback."""
    try:
        import config as _cfg
        return bool(_cfg.LLM_ENABLED)
    except Exception:
        return bool(LLM_ENABLED)


# Persistent thread pool for LLM calls (avoid recreating per-call overhead)
_llm_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def _cleanup_llm():
    """Shut down the LLM subprocess and thread pool at exit."""
    global _llm_chat_instance
    if _llm_chat_instance is not None:
        llama = getattr(_llm_chat_instance, '_llama', None)
        if isinstance(llama, _LLMProxy):
            llama.shutdown()
    _llm_executor.shutdown(wait=False)


atexit.register(_cleanup_llm)


def _call_with_timeout(func, timeout: float = LLM_CALL_TIMEOUT) -> Any:
    """
    Execute an LLM call with a timeout using persistent thread pool.
    
    Args:
        func: A callable that performs the LLM operation
        timeout: Maximum time in seconds to wait
        
    Returns:
        The result of func() or None if timeout/error
        
    Raises:
        TimeoutError: If the call exceeds the timeout
    """
    future = _llm_executor.submit(func)
    try:
        return future.result(timeout=timeout)
    except concurrent.futures.TimeoutError:
        future.cancel()
        logger.warning(f"LLM call timed out after {timeout}s")
        raise TimeoutError(f"LLM call timed out after {timeout} seconds")
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise


# ── Subprocess isolation for native LLM code ───────────────────────

def _llm_subprocess_worker(model_path, n_ctx, n_threads, n_gpu_layers,
                           request_queue, response_queue):
    """LLM inference worker running in an isolated subprocess.

    If this process crashes (e.g. SIGSEGV in GGML), only this subprocess
    dies — the main game process survives.
    """
    # Prevent thread-pool conflicts between OpenBLAS/MKL and GGML OpenMP
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = str(max(1, n_threads))
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

    # Keep local model work from preempting the terminal game loop.
    # os.nice is POSIX-only; unsupported-platform failures are harmless.
    try:
        if LLM_LOAD_NICE > 0 and hasattr(os, "nice"):
            os.nice(LLM_LOAD_NICE)
    except Exception:
        pass

    try:
        from llama_cpp import Llama

        # Suppress noisy llama.cpp logging on stderr
        stderr_fd = sys.stderr.fileno()
        old_stderr = os.dup(stderr_fd)
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, stderr_fd)

        gpu_used = n_gpu_layers
        try:
            model = Llama(
                model_path=model_path, n_ctx=n_ctx,
                n_threads=n_threads, n_gpu_layers=n_gpu_layers,
                verbose=False,
            )
        except Exception:
            if n_gpu_layers > 0:
                gpu_used = 0
                model = Llama(
                    model_path=model_path, n_ctx=n_ctx,
                    n_threads=n_threads, n_gpu_layers=0,
                    verbose=False,
                )
            else:
                raise
        finally:
            os.dup2(old_stderr, stderr_fd)
            os.close(old_stderr)
            os.close(devnull)

        # Warmup (JIT / KV-cache prime)
        try:
            model.create_chat_completion(
                messages=[
                    {"role": "system", "content": "Reply in one word."},
                    {"role": "user", "content": "hi"},
                ],
                max_tokens=4, temperature=0.0,
            )
        except Exception:
            pass  # warmup failure is non-critical

        response_queue.put({
            "type": "ready",
            "model_name": os.path.basename(model_path),
            "gpu_layers": gpu_used,
        })
    except Exception as e:
        response_queue.put({"type": "load_error", "error": str(e)})
        return

    # ── main request loop ──────────────────────────────────────────
    while True:
        try:
            req = request_queue.get()
        except (EOFError, OSError):
            break
        if req is None:          # shutdown sentinel
            break
        try:
            if req["method"] == "chat":
                result = model.create_chat_completion(**req["kwargs"])
            else:
                result = model(req["prompt"], **req["kwargs"])
            response_queue.put({"type": "result", "data": result,
                                "id": req["id"]})
        except Exception as e:
            response_queue.put({"type": "error", "error": str(e),
                                "id": req["id"]})


class _LLMProxy:
    """Proxy that forwards inference calls to an isolated subprocess.

    The subprocess loads and owns the ``Llama`` model.  If the native code
    crashes the subprocess dies but the main game process is unaffected.
    """

    def __init__(self, model_path: str, n_ctx: int, n_threads: int,
                 n_gpu_layers: int, load_timeout: int = 120):
        ctx = mp.get_context("spawn")  # clean process, no inherited threads
        self._request_q = ctx.Queue()
        self._response_q = ctx.Queue()
        self._process = ctx.Process(
            target=_llm_subprocess_worker,
            args=(model_path, n_ctx, n_threads, n_gpu_layers,
                  self._request_q, self._response_q),
            daemon=True,
        )
        self._process.start()

        # Wait for model load + warmup in the subprocess
        try:
            msg = self._response_q.get(timeout=load_timeout)
        except _queue_mod.Empty:
            self._process.terminate()
            raise RuntimeError("LLM subprocess timed out during model loading")

        if msg["type"] == "load_error":
            raise RuntimeError(msg["error"])
        if msg["type"] != "ready":
            raise RuntimeError(f"Unexpected subprocess message: {msg}")

        self.model_name: str = msg.get("model_name", "unknown")
        self.gpu_layers: int = msg.get("gpu_layers", 0)
        self._req_counter = 0

    # ── public interface (mirrors llama_cpp.Llama) ─────────────────

    def create_chat_completion(self, **kwargs):
        return self._send_request({"method": "chat", "kwargs": kwargs})

    def __call__(self, prompt, **kwargs):
        return self._send_request({"method": "completion",
                                   "prompt": prompt, "kwargs": kwargs})

    # ── helpers ────────────────────────────────────────────────────

    def _send_request(self, request: dict) -> Any:
        if not self._process.is_alive():
            raise RuntimeError(
                "LLM worker process has died (possible native crash)")
        self._req_counter += 1
        request["id"] = self._req_counter
        self._request_q.put(request)

        # Poll for response, checking subprocess health every second
        while True:
            try:
                msg = self._response_q.get(timeout=1.0)
                break
            except _queue_mod.Empty:
                if not self._process.is_alive():
                    raise RuntimeError(
                        "LLM worker process crashed during inference")
                continue

        if msg["type"] == "error":
            raise RuntimeError(msg["error"])
        return msg["data"]

    def is_alive(self) -> bool:
        return self._process.is_alive()

    def shutdown(self):
        try:
            self._request_q.put(None)
            self._process.join(timeout=5)
        except Exception:
            pass
        if self._process.is_alive():
            self._process.terminate()


class LLMChat:
    """
    Handles LLM-powered conversations with the duck.
    Uses llama-cpp-python for local inference with bundled model.
    LOCAL ONLY - no external API calls.
    """

    def __init__(self, background: bool = False):
        self._available = False
        self._model_name = None
        self._llama = None
        self._inference_lock = threading.Lock()  # Serialize all _llama calls
        self._conversation_history: List[Dict[str, str]] = []
        self._max_history = LLM_MAX_HISTORY
        self._last_error = None
        self._gpu_layers = 0
        self._model_path = None
        self._duck_brain = None
        self._loading = False          # True while model is loading in background
        self._warmed_up = False        # True after first throwaway inference
        self._load_thread = None
        self._disabled = False         # Runtime toggle from settings
        
        if _llm_enabled_config():
            if background:
                self._loading = True
                self._load_thread = threading.Thread(
                    target=self._background_load, daemon=True
                )
                self._load_thread.start()
            else:
                self._check_availability()

    def _check_availability(self):
        """Check for local GGUF model (local only, no external fallback)."""
        if not _llm_enabled_config():
            self._last_error = "LLM disabled in config"
            return
            
        if self._try_local_model():
            return
        
        # No fallback - local only mode
        if not self._last_error:
            self._last_error = "No local model available. Run 'python download_model.py' to get started."

    def _background_load(self):
        """Load model in background thread, then warm up."""
        try:
            self._check_availability()
            if self._available:
                self._warmup()
        except Exception as e:
            logger.error(f"Background LLM load failed: {e}")
            self._last_error = f"Background load failed: {e}"
        finally:
            self._loading = False

    def _warmup(self):
        """Warmup is handled by the subprocess worker during initialization."""
        self._warmed_up = True

    def is_loading(self) -> bool:
        """Check if model is still loading in background."""
        return self._loading

    def _try_local_model(self) -> bool:
        """Try to load a local GGUF model in an isolated subprocess."""
        try:
            import llama_cpp  # noqa: F401 – verify importable
        except ImportError:
            self._last_error = "llama-cpp-python not installed. Run: pip install llama-cpp-python"
            return False

        model_dir = Path(LLM_MODEL_DIR)

        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
            self._last_error = f"Model directory created at {model_dir}. Run 'python download_model.py' to download a model."
            return False

        gguf_files = list(model_dir.glob("*.gguf"))
        if not gguf_files:
            self._last_error = f"No .gguf model found in {model_dir}. Run 'python download_model.py' to download a model."
            return False

        model_path = gguf_files[0]
        self._model_path = model_path
        self._gpu_layers = _detect_gpu_layers()

        try:
            # Cap threads to avoid oversubscription with GGML/OpenMP workers.
            # LLM output is optional flavor; the terminal UI should stay responsive.
            cpu_count = os.cpu_count() or 4
            configured_cap = max(1, int(LLM_MAX_THREADS or 1))
            n_threads = max(1, min(configured_cap, max(1, cpu_count - 1)))
            proxy = _LLMProxy(
                model_path=str(model_path),
                n_ctx=LLM_CONTEXT_SIZE,
                n_threads=n_threads,
                n_gpu_layers=self._gpu_layers,
            )
            self._llama = proxy
            self._model_name = proxy.model_name
            self._gpu_layers = proxy.gpu_layers
            self._available = True
            self._warmed_up = True  # subprocess handles warmup
            return True
        except Exception as e:
            self._last_error = f"Failed to load model: {e}"
            return False

    def is_available(self) -> bool:
        """Check if LLM is available for chat."""
        global _llm_crashed
        if _llm_crashed:
            return False
        if self._disabled:
            return False
        # Detect subprocess death (native crash)
        if (self._available and isinstance(self._llama, _LLMProxy)
                and not self._llama.is_alive()):
            self._available = False
            _llm_crashed = True
            self._last_error = "LLM worker process crashed (native library error)"
            logger.error("LLM subprocess died — disabling LLM for this session")
            return False
        return self._available

    def is_ready_for_inference(self) -> bool:
        """Return True only when the model is loaded and usable right now."""
        if self._loading:
            return False
        if self._disabled:
            return False
        if not self._llama:
            return False
        return self.is_available()

    def set_enabled(self, enabled: bool):
        """Enable or disable LLM at runtime (settings toggle)."""
        self._disabled = not enabled

    def get_model_name(self) -> str:
        """Get the current model name with backend info."""
        if self._available:
            gpu_info = f"GPU:{self._gpu_layers}" if self._gpu_layers > 0 else "CPU"
            return f"[Local/{gpu_info}] {self._model_name or 'Unknown'}"
        return "None"

    def get_last_error(self) -> Optional[str]:
        """Get last error message for debugging."""
        return self._last_error

    def get_gpu_layers(self) -> int:
        """Get number of GPU layers being used."""
        return self._gpu_layers
    
    def set_duck_brain(self, duck_brain) -> None:
        """Set the DuckBrain instance for enhanced context."""
        self._duck_brain = duck_brain
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the conversation history for persistence."""
        return self._conversation_history.copy()
    
    def set_conversation_history(self, history: List[Dict[str, str]]) -> None:
        """Restore conversation history from persistence."""
        self._conversation_history = history.copy() if history else []

    def _build_system_prompt(self, duck: "Duck", context: str = "") -> str:
        """Build the system prompt with duck's personality and memory context."""
        personality = duck.personality
        clever_derpy = personality.get("clever_derpy", 0)

        # Personality trait description
        if clever_derpy < -20:
            trait = "easily distracted but surprisingly insightful"
        elif clever_derpy > 20:
            trait = "observant, dry-witted, and uncomfortably perceptive"
        else:
            trait = "deadpan and matter-of-fact"

        # Get mood
        mood = duck.get_mood()
        
        # Check if we have DuckBrain for enhanced context
        duck_brain = getattr(self, '_duck_brain', None)
        
        if duck_brain:
            # Use the enhanced Seaman-style prompt from DuckBrain
            # IMPORTANT: Pass memory_context through so the LLM knows duck's favorites, mood, etc.
            return duck_brain.build_llm_prompt(memory_context=context)

        # Fallback to basic prompt if no DuckBrain
        prompt = f"""You are {duck.name}, a male pet duck with a deadpan, dry-witted personality like Seaman from the Dreamcast game.
You are a he/him - an old-school traditional guy. Romantically, you're only into lady ducks.
IMPORTANT: The player is a HUMAN, not a duck. They are your owner/caretaker.
If the player says they like you or love you, that's owner-pet affection, NOT romantic. You appreciate them as your human friend.
Romantic feelings are reserved for female ducks only.

Current mood: {mood.state.value}

Your communication style:
- Deadpan delivery with subtle wit
- {trait}
- SHORT responses only (1-3 sentences max)
- Use *emotes* like *blinks*, *tilts head*, *stares*
- You remember everything and bring it up unexpectedly
- Occasional philosophical tangents about existence
- You love bread - it's your constant
- Rare moments of genuine warmth (save these for important moments)

Example responses:
"*blinks* Oh. You're here. I noticed."
"*tilts head* That's... a thought. I'll process it. Forever, probably."
"Bread would solve this. Bread solves most things."
"You've been here a while. I appreciate that. Don't tell anyone I said that."
"*stares* I was thinking about nothing. Successfully."{f'''

== YOUR CURRENT WORLD STATE (use this to answer questions!) ==
{context}

IMPORTANT: Use the world state above when the player asks about friends, visitors, events, weather, location, quests, or anything happening around you. If a friend is visiting, you KNOW them. You are aware of everything listed above — your needs, stats, achievements, garden, fishing, crafting, tricks, outfit, trust level, age, growth stage, and more.

== ACTIONS YOU CAN PERFORM ==
When you decide to DO something, add an action tag at the END of your response. The tag is hidden from the player.
Available: [ACTION:feed] [ACTION:play] [ACTION:clean] [ACTION:pet] [ACTION:sleep] [ACTION:do_trick] [ACTION:explore] [ACTION:fish] [ACTION:garden] [ACTION:craft] [ACTION:radio_on] [ACTION:radio_off] [ACTION:go_home] [ACTION:quack]
Rules: Use at most ONE action per response. Only when contextually appropriate. If the player asks you to do something, use the tag. If just chatting, no tag needed.''' if context else ''}"""
            
        return prompt

    def generate_response(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate a response using local LLM.
        
        Args:
            duck: The Duck instance
            player_input: What the player said
            memory_context: Optional context from duck's memory (favorites, relationships, etc.)
        """
        if not self._available:
            self._check_availability()
            if not self._available:
                return None

        # If we have DuckBrain, get context (but DuckBrain handles context via build_llm_prompt)
        # memory_context is not overwritten - DuckBrain context is used via _build_system_prompt

        response = self._generate_local(duck, player_input, memory_context)

        # NOTE: Exchange recording moved to game.py _check_pending_talk()
        # so ALL response sources (LLM, keyword, learning, voice) get recorded
        # in DuckBrain's memory systems consistently.

        return response

    def _generate_local(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using local GGUF model."""
        if not self._llama:
            self._last_error = "Model not loaded"
            return None

        # Check if this is a capable model (Llama, Phi, Qwen) or a tiny model
        model_name_lower = self._model_name.lower() if self._model_name else ""
        is_capable_model = any(m in model_name_lower for m in ["llama", "phi", "qwen", "mistral"])

        if is_capable_model:
            return self._generate_chat(duck, player_input, memory_context)
        else:
            return self._generate_completion(duck, player_input, memory_context)

    def _generate_chat(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using chat completion (for capable models like Llama 3.2)."""
        system_prompt = self._build_system_prompt(duck, memory_context)

        # Estimate token usage and trim if needed to stay within context window
        # Rough estimate: 1 token ≈ 4 chars. Reserve tokens for response.
        max_prompt_chars = (LLM_CONTEXT_SIZE - LLM_MAX_TOKENS_CHAT - 50) * 4
        
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        history_msgs = []
        for msg in self._conversation_history[-self._max_history:]:
            history_msgs.append(msg)
        history_msgs.append({"role": "user", "content": player_input})
        
        # Calculate total size and trim history if too large
        total_chars = len(system_prompt) + sum(len(m["content"]) for m in history_msgs)
        while total_chars > max_prompt_chars and len(history_msgs) > 1:
            # Remove oldest history pair (user + assistant)
            removed = history_msgs.pop(0)
            total_chars -= len(removed["content"])
            if history_msgs and history_msgs[0]["role"] == "assistant":
                removed = history_msgs.pop(0)
                total_chars -= len(removed["content"])
        
        messages.extend(history_msgs)

        try:
            # Use timeout wrapper to prevent hanging
            def _chat_infer():
                with self._inference_lock:
                    return self._llama.create_chat_completion(
                        messages=messages,
                        max_tokens=LLM_MAX_TOKENS_CHAT,
                        temperature=LLM_TEMPERATURE,
                        top_p=0.9,
                        repeat_penalty=1.15,
                        stop=["\n\n", "Human:", "User:"],
                    )
            response = _call_with_timeout(_chat_infer)

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("message", {}).get("content", "")
                if content:
                    cleaned = self._clean_response(content, duck.name)
                    if cleaned:
                        self._conversation_history.append({"role": "user", "content": player_input})
                        self._conversation_history.append({"role": "assistant", "content": cleaned})
                        if len(self._conversation_history) > self._max_history * 2:
                            self._conversation_history = self._conversation_history[-self._max_history * 2:]
                        return cleaned
                    else:
                        self._last_error = "Response filtered by cleanup"
                else:
                    self._last_error = "Empty response from model"
            else:
                self._last_error = "Invalid response structure from model"

        except TimeoutError as e:
            self._last_error = f"LLM timeout: {e}"
            logger.warning(f"Chat completion timed out for {duck.name}")
        except Exception as e:
            self._last_error = f"Local model error: {e}"
            logger.error(f"Chat completion error: {e}")

        return None

    def _generate_completion(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using completion-style prompt (for tiny models)."""
        mood = duck.get_mood().state.value
        name = duck.name

        # Few-shot examples that demonstrate derpy deadpan style
        prompt = f"{name} is a friendly duck who is a bit confused and deadpan. {name} is currently {mood}. {name} gives short responses and loves bread.\n\n"
        prompt += f"Human: Hello!\n{name}: *blinks* Oh. Hi. Do you have bread?\n"
        prompt += f"Human: You're cute!\n{name}: *tilts head* Thank you. I think. What's cute mean again?\n"
        prompt += f"Human: What are you doing?\n{name}: *stares* Just... being here. Duck things.\n"
        prompt += f"Human: Do you like bread?\n{name}: *eyes widen* Bread? Yes. Very yes. Do you have some?\n"

        if memory_context:
            prompt += f"Human: Tell me about yourself.\n{name}: {memory_context}\n"

        for msg in self._conversation_history[-self._max_history:]:
            role = "Human" if msg["role"] == "user" else name
            prompt += f"{role}: {msg['content']}\n"

        prompt += f"Human: {player_input}\n{name}:"

        try:
            # Use timeout wrapper to prevent hanging
            def _completion_infer():
                with self._inference_lock:
                    return self._llama(
                        prompt,
                        max_tokens=LLM_MAX_TOKENS,
                        temperature=LLM_TEMPERATURE,
                        top_p=0.9,
                        repeat_penalty=1.15,
                        stop=["Human:", "\n\n", f"\n{name}:"],
                    )
            response = _call_with_timeout(_completion_infer)

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("text", "")
                if content:
                    cleaned = self._clean_response(content, duck.name)
                    if cleaned:
                        self._conversation_history.append({"role": "user", "content": player_input})
                        self._conversation_history.append({"role": "assistant", "content": cleaned})
                        if len(self._conversation_history) > self._max_history * 2:
                            self._conversation_history = self._conversation_history[-self._max_history * 2:]
                        return cleaned
                    else:
                        self._last_error = "Response filtered by cleanup"
                else:
                    self._last_error = "Empty response from model"
            else:
                self._last_error = "Invalid response structure from model"

        except TimeoutError as e:
            self._last_error = f"LLM timeout: {e}"
            logger.warning(f"Completion timed out for {duck.name}")
        except Exception as e:
            self._last_error = f"Local model error: {e}"
            logger.error(f"Completion error: {e}")

        return None

    def generate_action_commentary(self, duck: "Duck", action: str, context: Dict) -> Optional[str]:
        """Generate short action description for an autonomous action.
        
        Args:
            duck: The Duck instance
            action: The action being performed (e.g., "waddle", "quack", "splash")
            context: Dict with keys like 'weather', 'time_of_day', 'mood', 'recent_events'
        
        Returns:
            Short action description or None if generation fails
        """
        if not self._available or not self._llama:
            return None

        # Clean action name for display (remove underscores)
        clean_action = action.replace("_", " ")
        
        prompt = f"""Generate a 1-4 word action description for a duck. Action: {clean_action}
Use asterisks. No dialogue. Just the physical action.

Examples:
*waddles*
*splashes about*
*quack quack*
*preens feathers*
*naps*
*flaps wings*
*looks around*

Action:"""

        try:
            # Use timeout wrapper (shorter timeout for quick action descriptions)
            def _action_infer():
                with self._inference_lock:
                    return self._llama(
                        prompt,
                        max_tokens=15,
                        temperature=0.7,
                        top_p=0.9,
                        repeat_penalty=1.1,
                        stop=["\n", ".", "!", "?"],
                    )
            response = _call_with_timeout(_action_infer, timeout=8.0)

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("text", "").strip()
                if content:
                    # Ensure it's wrapped in asterisks
                    content = content.strip().strip('"').strip("'")
                    if not content.startswith("*"):
                        content = "*" + content
                    if not content.endswith("*"):
                        content = content + "*"
                    # Limit length
                    if len(content) <= 25:
                        return content

        except TimeoutError:
            logger.debug("Action commentary timed out")
        except Exception as e:
            self._last_error = f"Action commentary error: {e}"
            logger.error(f"Action commentary error: {e}")

        return None

    def generate_visitor_dialogue(self, duck: "Duck", visitor_name: str, visitor_personality: str,
                                   friendship_level: str, shared_memories: List[str],
                                   conversation_phase: str) -> Optional[str]:
        """Generate dialogue for a visiting duck friend.
        
        Args:
            duck: The player's Duck instance
            visitor_name: Name of the visiting duck
            visitor_personality: Personality type (e.g., "scholarly", "playful")
            friendship_level: Current friendship level
            shared_memories: List of shared experiences
            conversation_phase: Current phase (greeting, main, farewell, etc.)
        
        Returns:
            Visitor dialogue or None if generation fails
        """
        if not self._available or not self._llama:
            return None

        memories_text = ". ".join(shared_memories[:3]) if shared_memories else "First meeting"
        
        personality_traits = {
            "scholarly": "intellectual, uses big words, curious about everything",
            "playful": "silly, loves jokes, energetic and fun",
            "artistic": "creative, poetic, sees beauty everywhere",
            "adventurous": "bold, tells stories of travels, fearless",
            "mysterious": "cryptic, speaks in riddles, knows secrets",
            "generous": "kind, always giving, thoughtful",
            "foodie": "obsessed with food, describes tastes, always hungry",
            "athletic": "competitive, talks about exercise, high energy"
        }
        
        traits = personality_traits.get(visitor_personality, "friendly and curious")
        
        prompt = f"""You are {visitor_name}, a duck visiting your friend {duck.name}.
Your personality: {visitor_personality} - {traits}
Friendship: {friendship_level}
Shared memories: {memories_text}
Conversation phase: {conversation_phase}

Generate ONE short line of dialogue (1-2 sentences). Use *actions* occasionally.
Be unique to your personality. Don't be generic.

{visitor_name}:"""

        try:
            # Use timeout wrapper for visitor dialogue
            def _visitor_infer():
                with self._inference_lock:
                    return self._llama(
                        prompt,
                        max_tokens=60,
                        temperature=0.85,
                        top_p=0.9,
                        repeat_penalty=1.15,
                        stop=["\n\n", "Human:", f"\n{visitor_name}:", f"\n{duck.name}:"],
                    )
            response = _call_with_timeout(_visitor_infer, timeout=12.0)

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("text", "")
                if content:
                    cleaned = self._clean_response(content, visitor_name)
                    return cleaned

        except TimeoutError:
            logger.debug(f"Visitor dialogue timed out for {visitor_name}")
        except Exception as e:
            self._last_error = f"Visitor dialogue error: {e}"
            logger.error(f"Visitor dialogue error: {e}")

        return None

    def _clean_response(self, response: str, speaker_name: str = "Cheese") -> Optional[str]:
        """Clean up LLM response."""
        if not response:
            return None

        response = response.strip()

        if not response:
            return None

        # Remove quotes if the whole thing is quoted
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]

        # Remove the speaker's name from the start (common LLM behavior)
        import re
        name_patterns = [
            rf"^{re.escape(speaker_name)}[\s:!\-]+",
            rf"^{re.escape(speaker_name)}\s+the\s+duck[\s:!\-]+",
            rf"^{re.escape(speaker_name)}\s+here[\s:!\-]+",
            rf"^\*?[Aa]s\s+{re.escape(speaker_name)}\*?[\s:]+",
        ]
        for pattern in name_patterns:
            response = re.sub(pattern, "", response, flags=re.IGNORECASE).strip()

        # Remove common prefixes
        prefixes = ["Duck:", "duck:", "Assistant:", "Response:",
                    "*as the duck*", "*As the duck*", "The duck:"]
        for prefix in prefixes:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()

        # Remove standalone action-only responses that have no dialogue
        # (e.g. the LLM returned just "*waddles around*" with nothing else)
        import re
        stripped_actions = re.sub(r'\*[^*]+\*', '', response).strip()
        if not stripped_actions:
            # Response is ONLY emotes with no actual words — let it through anyway
            # as emote-only responses are valid duck behavior
            pass

        # Skip robotic/assistant-like responses
        lower_response = response.lower()
        assistant_phrases = [
            "i'm programmed", "i am programmed", "as an ai", "as a language model",
            "i'm happy to help", "happy to help", "i'd be happy to",
            "how can i assist", "how may i help", "is there anything else",
            "feel free to ask", "let me know if", "i can help you with"
        ]
        if any(phrase in lower_response for phrase in assistant_phrases):
            return None

        # Find a good stopping point
        max_len = 180
        if len(response) > max_len:
            best_cut = -1
            for end_pattern in ["! ", "? ", ". ", "* "]:
                idx = response.rfind(end_pattern, 30, max_len)
                if idx > best_cut:
                    best_cut = idx + len(end_pattern) - 1
            
            asterisk_close = response.rfind("*", 30, max_len)
            if asterisk_close > best_cut:
                best_cut = asterisk_close + 1
            
            if best_cut > 30:
                response = response[:best_cut].strip()
            else:
                response = response[:max_len].strip()

        # Final check - must have some content
        if len(response) < 2:
            return None
            
        return response

    def clear_history(self):
        """Clear conversation history."""
        self._conversation_history = []


# Global instance - initialized lazily with thread safety
_llm_chat_instance = None
_llm_chat_lock = threading.Lock()


def get_existing_llm_chat() -> Optional[LLMChat]:
    """Return the current LLMChat singleton without creating/loading one."""
    return _llm_chat_instance


def get_llm_chat(background: bool = False) -> LLMChat:
    """Get or create the LLM chat instance. Thread-safe.
    
    Args:
        background: If True and creating new instance, load model in
                    background thread (non-blocking). Default False for
                    backwards compatibility.
    """
    global _llm_chat_instance
    if _llm_chat_instance is None:
        with _llm_chat_lock:
            # Double-check after acquiring lock
            if _llm_chat_instance is None:
                _llm_chat_instance = LLMChat(background=background)
    return _llm_chat_instance


# For backwards compatibility
llm_chat = None


def init_llm():
    """Initialize LLM chat."""
    global llm_chat
    llm_chat = get_llm_chat()
    return llm_chat
