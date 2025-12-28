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
            # Load the model with conservative settings for compatibility
            self._llama = Llama(
                model_path=str(model_path),
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=0,  # CPU only for maximum compatibility
                verbose=False,
            )
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
            trait = "derpy and easily confused"
        elif clever_derpy > 20:
            trait = "clever but still a duck"
        else:
            trait = "a regular duck"

        # Get mood
        mood = duck.get_mood()

        # Compact prompt for smaller models
        return f"""You are {duck.name} the duck. You are {trait}, currently {mood.state.value}.

RULES:
1. Use *actions* like *quack* *waddle* *flap*
2. Be snarky and funny, not mean
3. Love bread, mention it sometimes
4. 1-2 sentences only
5. Never break character

Examples:
"*tilts head* Quack? Did someone say bread?"
"*flaps* The AUDACITY! I am a MAJESTIC duck!"
"*suspicious squint* ...are you hiding bread from me?"

Now respond as {duck.name}:"""

    def generate_response(self, duck: "Duck", player_input: str) -> Optional[str]:
        """Generate a response using available LLM backend."""
        if not self._available:
            self._check_availability()
            if not self._available:
                return None

        if self._use_ollama:
            return self._generate_ollama(duck, player_input)
        else:
            return self._generate_local(duck, player_input)

    def _generate_local(self, duck: "Duck", player_input: str) -> Optional[str]:
        """Generate response using local GGUF model."""
        if not self._llama:
            return None

        system_prompt = self._build_system_prompt(duck)

        # Build chat messages with few-shot examples to prime the model
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add few-shot examples to show the expected format
        few_shot = [
            {"role": "user", "content": "Hey there!"},
            {"role": "assistant", "content": "*waddles over* Oh! A visitor! *quack* Got any bread?"},
            {"role": "user", "content": "You're so cute!"},
            {"role": "assistant", "content": "*puffs up proudly* I KNOW, right?! *flaps wings* I'm basically perfect. Quack!"},
        ]
        messages.extend(few_shot)
        
        # Add real conversation history
        for msg in self._conversation_history[-self._max_history:]:
            messages.append(msg)
        messages.append({"role": "user", "content": player_input})

        try:
            response = self._llama.create_chat_completion(
                messages=messages,
                max_tokens=80,  # Keep it short
                temperature=0.9,
                top_p=0.95,
                stop=["User:", "Human:", "\n\n", "You:"],
            )

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("message", {}).get("content", "")
                if content:
                    content = self._clean_response(content)
                    self._conversation_history.append({"role": "user", "content": player_input})
                    self._conversation_history.append({"role": "assistant", "content": content})
                    if len(self._conversation_history) > self._max_history * 2:
                        self._conversation_history = self._conversation_history[-self._max_history * 2:]
                    return content

        except Exception as e:
            self._last_error = f"Local model error: {e}"

        return None

    def _generate_ollama(self, duck: "Duck", player_input: str) -> Optional[str]:
        """Generate response using Ollama API."""
        system_prompt = self._build_system_prompt(duck)

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
                    response_text = self._clean_response(response_text)

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

    def _clean_response(self, response: str) -> str:
        """Clean up LLM response."""
        response = response.strip()

        # Remove quotes if the whole thing is quoted
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]

        # Remove common prefixes
        prefixes = ["Duck:", "duck:", "Cheese:", "cheese:", "Assistant:", "Response:", "*As Cheese*", "*as the duck*"]
        for prefix in prefixes:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()

        # Remove any "Here's my response:" type preambles
        preamble_markers = ["here's", "here is", "okay,", "ok,", "sure,", "alright,", "i'm ", "i am "]
        lower_response = response.lower()
        for marker in preamble_markers:
            if lower_response.startswith(marker) and "programmed" in lower_response[:100]:
                # Skip robotic responses entirely
                return None

        # Find a good stopping point
        # First, try to find a complete sentence ending in punctuation + space or action
        max_len = 150
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
