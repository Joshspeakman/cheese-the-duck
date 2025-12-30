"""
Offline LLM integration for duck conversations.
Supports local GGUF models via llama-cpp-python, with Ollama as fallback.
"""
import json
import os
import urllib.request
import urllib.error
from typing import Optional, List, Dict, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from duck.duck import Duck


# Model configuration
MODEL_DIR = Path(__file__).parent.parent / "models"


class LLMChat:
    """
    Handles LLM-powered conversations with the duck.
    Uses llama-cpp-python for local inference with bundled model.
    Falls back to Ollama HTTP API if available.
    """

    def __init__(self):
        self._available = False
        self._model_name = None
        self._llama = None
        self._use_ollama = False
        self._conversation_history: List[Dict[str, str]] = []
        self._max_history = 6
        self._timeout = 30
        self._base_url = "http://localhost:11434"
        self._last_error = None
        self._check_availability()

    def _check_availability(self):
        """Check for available LLM backends."""
        # Try local GGUF model first
        if self._try_local_model():
            return
        
        # Fall back to Ollama
        if self._try_ollama():
            return
        
        self._last_error = "No LLM available. Run 'python download_model.py' to get started."

    def _try_local_model(self) -> bool:
        """Try to load a local GGUF model."""
        try:
            from llama_cpp import Llama
        except ImportError:
            self._last_error = "llama-cpp-python not installed"
            return False

        # Look for model files
        if not MODEL_DIR.exists():
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            return False

        # Find any .gguf file
        gguf_files = list(MODEL_DIR.glob("*.gguf"))
        if not gguf_files:
            self._last_error = f"No model found in {MODEL_DIR}"
            return False

        model_path = gguf_files[0]

        try:
            # Suppress llama.cpp warnings during model loading
            import sys
            import os
            stderr_fd = sys.stderr.fileno()
            old_stderr = os.dup(stderr_fd)
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, stderr_fd)

            try:
                # Load the model with conservative settings for compatibility
                self._llama = Llama(
                    model_path=str(model_path),
                    n_ctx=2048,
                    n_threads=4,
                    n_gpu_layers=0,  # CPU only for maximum compatibility
                    verbose=False,
                )
            finally:
                # Restore stderr
                os.dup2(old_stderr, stderr_fd)
                os.close(old_stderr)
                os.close(devnull)

            self._model_name = model_path.name
            self._available = True
            self._use_ollama = False
            return True
        except Exception as e:
            self._last_error = f"Failed to load model: {e}"
            return False

    def _try_ollama(self) -> bool:
        """Try to connect to Ollama."""
        fallback_models = ["llama3.2", "llama3.1", "llama3", "mistral", "phi3", "gemma2", "qwen2"]
        
        try:
            req = urllib.request.Request(f"{self._base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                models = [m["name"].split(":")[0] for m in data.get("models", [])]

                if not models:
                    return False

                for model in fallback_models:
                    if model in models:
                        self._model_name = model
                        self._available = True
                        self._use_ollama = True
                        return True

                if models:
                    self._model_name = models[0]
                    self._available = True
                    self._use_ollama = True
                    return True

        except Exception:
            pass
        
        return False

    def is_available(self) -> bool:
        """Check if LLM is available for chat."""
        return self._available

    def get_model_name(self) -> str:
        """Get the current model name."""
        if self._available:
            prefix = "[Ollama] " if self._use_ollama else "[Local] "
            return prefix + (self._model_name or "Unknown")
        return "None"

    def get_last_error(self) -> Optional[str]:
        """Get last error message for debugging."""
        return self._last_error

    def _build_system_prompt(self, duck: "Duck") -> str:
        """Build the system prompt with duck's personality."""
        personality = duck.personality
        clever_derpy = personality.get("clever_derpy", 0)

        # Simple trait
        if clever_derpy < -20:
            trait = "easily distracted and spacey"
        elif clever_derpy > 20:
            trait = "observant and dry-witted"
        else:
            trait = "matter-of-fact"

        # Get mood
        mood = duck.get_mood()

        # System prompt for Ollama and fallback
        return f"""You are {duck.name}, a pet duck. You are currently {mood.state.value}.

Your personality:
- Deadpan and a bit confused, but friendly
- Not mean or sarcastic, just... a duck
- Give SHORT responses (1-2 sentences max)
- Use *actions* like *blinks* *tilts head* *stares*
- You love bread
- Easily distracted, sometimes forget what you were saying

Example responses:
"*blinks* Oh. Hello. Do you have bread?"
"*tilts head* I think so? Wait, what was the question."
"That's nice. I like that. I think. *stares into distance*"
"Bread would be good right now. Just saying."""

    def generate_response(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate a response using available LLM backend.
        
        Args:
            duck: The Duck instance
            player_input: What the player said
            memory_context: Optional context from duck's memory (favorites, relationships, etc.)
        """
        if not self._available:
            self._check_availability()
            if not self._available:
                return None

        if self._use_ollama:
            return self._generate_ollama(duck, player_input, memory_context)
        else:
            return self._generate_local(duck, player_input, memory_context)

    def _generate_local(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using local GGUF model."""
        if not self._llama:
            self._last_error = "Model not loaded"
            return None

        mood = duck.get_mood().state.value
        name = duck.name

        # Check if this is a capable model (Llama, Phi, Qwen) or a tiny model
        model_name_lower = self._model_name.lower() if self._model_name else ""
        is_capable_model = any(m in model_name_lower for m in ["llama", "phi", "qwen", "mistral"])

        if is_capable_model:
            # Use chat completion for capable models
            return self._generate_local_chat(duck, player_input, memory_context)
        else:
            # Use completion-style for tiny models
            return self._generate_local_completion(duck, player_input, memory_context)

    def _generate_local_chat(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using chat completion (for capable models like Llama 3.2)."""
        mood = duck.get_mood().state.value
        name = duck.name

        system_prompt = f"""You are {name}, a pet duck. You are currently {mood}.

Your personality:
- Deadpan and a bit confused, but friendly
- Not mean or sarcastic, just... a duck
- Give SHORT responses (1-2 sentences max)
- Use *actions* like *blinks* *tilts head* *stares*
- You love bread
- Easily distracted, sometimes forget what you were saying

Example responses:
"*blinks* Oh. Hello. Do you have bread?"
"*tilts head* I think so? Wait, what was the question."
"That's nice. I like that. I think. *stares into distance*"
"Bread would be good right now. Just saying."""

        if memory_context:
            system_prompt += f"\n\nContext about you: {memory_context}"

        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        for msg in self._conversation_history[-self._max_history:]:
            messages.append(msg)
        messages.append({"role": "user", "content": player_input})

        try:
            response = self._llama.create_chat_completion(
                messages=messages,
                max_tokens=60,
                temperature=0.8,
                top_p=0.9,
                stop=["\n\n", "Human:", "User:"],
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

        except Exception as e:
            self._last_error = f"Local model error: {e}"

        return None

    def _generate_local_completion(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
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
            response = self._llama(
                prompt,
                max_tokens=50,
                temperature=0.7,
                top_p=0.9,
                stop=["Human:", "\n\n", f"\n{name}:"],
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

        except Exception as e:
            self._last_error = f"Local model error: {e}"

        return None

    def _generate_ollama(self, duck: "Duck", player_input: str, memory_context: str = "") -> Optional[str]:
        """Generate response using Ollama API."""
        system_prompt = self._build_system_prompt(duck)
        
        # Add memory context to system prompt if available
        if memory_context:
            system_prompt += f"\n\nMemory context (use naturally if relevant): {memory_context}"

        # Build messages for chat API
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        for msg in self._conversation_history[-self._max_history:]:
            messages.append(msg)

        # Add current user message
        messages.append({"role": "user", "content": player_input})

        try:
            # Use Ollama chat API
            payload = {
                "model": self._model_name,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "num_predict": 150,  # Keep responses short
                }
            }

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                f"{self._base_url}/api/chat",
                data=data,
                headers={"Content-Type": "application/json"}
            )

            with urllib.request.urlopen(req, timeout=self._timeout) as response:
                result = json.loads(response.read().decode())

                if "message" in result and "content" in result["message"]:
                    response_text = result["message"]["content"]
                    response_text = self._clean_response(response_text, duck.name)

                    # Update history
                    self._conversation_history.append({"role": "user", "content": player_input})
                    self._conversation_history.append({"role": "assistant", "content": response_text})

                    # Trim history
                    if len(self._conversation_history) > self._max_history * 2:
                        self._conversation_history = self._conversation_history[-self._max_history * 2:]

                    return response_text

        except urllib.error.URLError as e:
            self._last_error = f"Connection error: {e}"
            self._available = False
        except json.JSONDecodeError as e:
            self._last_error = f"JSON error: {e}"
        except Exception as e:
            self._last_error = f"Error: {e}"

        return None

    def _clean_response(self, response: str, duck_name: str = "Cheese") -> Optional[str]:
        """Clean up LLM response."""
        if not response:
            return None

        response = response.strip()

        if not response:
            return None

        # Remove quotes if the whole thing is quoted
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]

        # Remove the duck's name from the start (common LLM behavior)
        # Handle patterns like "Cheese:", "Cheese the duck:", "Cheese here!", etc.
        import re
        name_patterns = [
            rf"^{re.escape(duck_name)}[\s:!\-]+",  # "Cheese:" or "Cheese " or "Cheese!"
            rf"^{re.escape(duck_name)}\s+the\s+duck[\s:!\-]+",  # "Cheese the duck:"
            rf"^{re.escape(duck_name)}\s+here[\s:!\-]+",  # "Cheese here!"
            rf"^\*?[Aa]s\s+{re.escape(duck_name)}\*?[\s:]+",  # "*As Cheese*" or "As Cheese:"
        ]
        for pattern in name_patterns:
            response = re.sub(pattern, "", response, flags=re.IGNORECASE).strip()

        # Remove common prefixes (generic)
        prefixes = ["Duck:", "duck:", "Assistant:", "Response:",
                    "*as the duck*", "*As the duck*", "The duck:"]
        for prefix in prefixes:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()

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
        max_len = 180  # Slightly longer allowed
        if len(response) > max_len:
            best_cut = -1
            # Priority: end after punctuation or after asterisk action
            for end_pattern in ["! ", "? ", ". ", "* "]:
                idx = response.rfind(end_pattern, 30, max_len)
                if idx > best_cut:
                    best_cut = idx + len(end_pattern) - 1
            
            # Also check for closing asterisk
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
llm_chat = None  # Will be set on first import if needed


def init_llm():
    """Initialize LLM chat."""
    global llm_chat
    llm_chat = get_llm_chat()
    return llm_chat
