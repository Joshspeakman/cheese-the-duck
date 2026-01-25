"""
Local LLM integration for duck conversations and behavior.
Uses local GGUF models via llama-cpp-python with GPU auto-detection.
LOCAL ONLY - no external API calls.
"""
import os
import sys
import signal
import logging
import threading
import concurrent.futures
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from pathlib import Path

# Configure logging for LLM operations
logger = logging.getLogger(__name__)

# LLM call timeout in seconds
LLM_CALL_TIMEOUT = 30.0

# Flag to track if LLM crashed (SIGSEGV, etc.)
_llm_crashed = False

def _handle_segfault(signum, frame):
    """Handle SIGSEGV by disabling LLM instead of crashing."""
    global _llm_crashed
    _llm_crashed = True
    logger.error("LLM caused a segmentation fault - disabling LLM for this session")

# Install signal handler for SIGSEGV
try:
    signal.signal(signal.SIGSEGV, _handle_segfault)
except (ValueError, OSError):
    # Signal handling not available (Windows, etc.)
    pass

if TYPE_CHECKING:
    from duck.duck import Duck

# Import config settings
try:
    from config import (
        LLM_ENABLED, LLM_LOCAL_ONLY, LLM_MODEL_DIR, LLM_GPU_LAYERS,
        LLM_CONTEXT_SIZE, LLM_MAX_TOKENS, LLM_MAX_TOKENS_CHAT,
        LLM_TEMPERATURE, LLM_MAX_HISTORY
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


def _call_with_timeout(func, timeout: float = LLM_CALL_TIMEOUT) -> Any:
    """
    Execute an LLM call with a timeout.
    
    Args:
        func: A callable that performs the LLM operation
        timeout: Maximum time in seconds to wait
        
    Returns:
        The result of func() or None if timeout/error
        
    Raises:
        TimeoutError: If the call exceeds the timeout
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            logger.warning(f"LLM call timed out after {timeout}s")
            raise TimeoutError(f"LLM call timed out after {timeout} seconds")
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise


class LLMChat:
    """
    Handles LLM-powered conversations with the duck.
    Uses llama-cpp-python for local inference with bundled model.
    LOCAL ONLY - no external API calls.
    """

    def __init__(self):
        self._available = False
        self._model_name = None
        self._llama = None
        self._conversation_history: List[Dict[str, str]] = []
        self._max_history = LLM_MAX_HISTORY
        self._last_error = None
        self._gpu_layers = 0
        self._model_path = None
        
        if LLM_ENABLED:
            self._check_availability()

    def _check_availability(self):
        """Check for local GGUF model (local only, no external fallback)."""
        if not LLM_ENABLED:
            self._last_error = "LLM disabled in config"
            return
            
        if self._try_local_model():
            return
        
        # No fallback - local only mode
        if not self._last_error:
            self._last_error = "No local model available. Run 'python download_model.py' to get started."

    def _try_local_model(self) -> bool:
        """Try to load a local GGUF model with GPU auto-detection."""
        try:
            from llama_cpp import Llama
        except ImportError:
            self._last_error = "llama-cpp-python not installed. Run: pip install llama-cpp-python"
            return False

        model_dir = Path(LLM_MODEL_DIR)
        
        # Look for model files
        if not model_dir.exists():
            model_dir.mkdir(parents=True, exist_ok=True)
            self._last_error = f"Model directory created at {model_dir}. Run 'python download_model.py' to download a model."
            return False

        # Find any .gguf file
        gguf_files = list(model_dir.glob("*.gguf"))
        if not gguf_files:
            self._last_error = f"No .gguf model found in {model_dir}. Run 'python download_model.py' to download a model."
            return False

        model_path = gguf_files[0]
        self._model_path = model_path

        # Auto-detect GPU layers
        self._gpu_layers = _detect_gpu_layers()

        try:
            # Suppress llama.cpp warnings during model loading
            stderr_fd = sys.stderr.fileno()
            old_stderr = os.dup(stderr_fd)
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, stderr_fd)

            try:
                # Load the model with GPU support
                self._llama = Llama(
                    model_path=str(model_path),
                    n_ctx=LLM_CONTEXT_SIZE,
                    n_threads=4,
                    n_gpu_layers=self._gpu_layers,
                    verbose=False,
                )
            finally:
                # Restore stderr
                os.dup2(old_stderr, stderr_fd)
                os.close(old_stderr)
                os.close(devnull)

            self._model_name = model_path.name
            self._available = True
            return True
        except Exception as e:
            # If GPU failed, try CPU-only as fallback
            if self._gpu_layers > 0:
                try:
                    self._gpu_layers = 0
                    self._llama = Llama(
                        model_path=str(model_path),
                        n_ctx=LLM_CONTEXT_SIZE,
                        n_threads=4,
                        n_gpu_layers=0,
                        verbose=False,
                    )
                    self._model_name = model_path.name
                    self._available = True
                    return True
                except Exception as e2:
                    self._last_error = f"Failed to load model (GPU and CPU): {e2}"
                    return False
            self._last_error = f"Failed to load model: {e}"
            return False

    def is_available(self) -> bool:
        """Check if LLM is available for chat."""
        global _llm_crashed
        if _llm_crashed:
            return False
        return self._available

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
            return duck_brain.build_llm_prompt()

        # Fallback to basic prompt if no DuckBrain
        prompt = f"""You are {duck.name}, a male pet duck with a deadpan, dry-witted personality like Seaman from the Dreamcast game.
You are a he/him - an old-school traditional guy. Straight, only interested in lady ducks. No modern sensibilities about that.
If asked about relationships or attraction, you're only into female ducks. You're old-fashioned that way.

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

Context: {context}''' if context else ''}"""
            
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
        
        # Record the exchange in DuckBrain if available
        duck_brain = getattr(self, '_duck_brain', None)
        if response and duck_brain:
            duck_brain.process_player_message(player_input, response)
        
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

        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        for msg in self._conversation_history[-self._max_history:]:
            messages.append(msg)
        messages.append({"role": "user", "content": player_input})

        try:
            # Use timeout wrapper to prevent hanging
            response = _call_with_timeout(
                lambda: self._llama.create_chat_completion(
                    messages=messages,
                    max_tokens=LLM_MAX_TOKENS_CHAT,
                    temperature=LLM_TEMPERATURE,
                    top_p=0.9,
                    stop=["\n\n", "Human:", "User:"],
                )
            )

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
            response = _call_with_timeout(
                lambda: self._llama(
                    prompt,
                    max_tokens=LLM_MAX_TOKENS,
                    temperature=LLM_TEMPERATURE,
                    top_p=0.9,
                    stop=["Human:", "\n\n", f"\n{name}:"],
                )
            )

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
            response = _call_with_timeout(
                lambda: self._llama(
                    prompt,
                    max_tokens=15,
                    temperature=0.7,
                    top_p=0.9,
                    stop=["\n", ".", "!", "?"],
                ),
                timeout=10.0  # Shorter timeout for action commentary
            )

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
            response = _call_with_timeout(
                lambda: self._llama(
                    prompt,
                    max_tokens=60,
                    temperature=0.85,
                    top_p=0.9,
                    stop=["\n\n", "Human:", f"\n{visitor_name}:", f"\n{duck.name}:"],
                ),
                timeout=15.0  # Moderate timeout for visitor dialogue
            )

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

        # Remove asterisk-wrapped actions from the start (e.g., "*waddles around* ")
        # These should only appear in the activity indicator, not the message
        action_pattern = r'^\*[^*]+\*\s*'
        response = re.sub(action_pattern, '', response).strip()
        
        # Also remove any underscores that might be in action names
        # (but be careful not to break legitimate underscores)
        response = re.sub(r'\*[a-z_]+\*', '', response).strip()

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


# Global instance - initialized lazily
_llm_chat_instance = None


def get_llm_chat() -> LLMChat:
    """Get or create the LLM chat instance."""
    global _llm_chat_instance
    if _llm_chat_instance is None:
        _llm_chat_instance = LLMChat()
    return _llm_chat_instance


# For backwards compatibility
llm_chat = None


def init_llm():
    """Initialize LLM chat."""
    global llm_chat
    llm_chat = get_llm_chat()
    return llm_chat
