"""
Offline LLM integration for duck conversations.
Supports Ollama (local) via HTTP API for smarter, more dynamic responses.
"""
import json
import urllib.request
import urllib.error
from typing import Optional, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from duck.duck import Duck


class LLMChat:
    """
    Handles LLM-powered conversations with the duck.
    Uses Ollama HTTP API for local inference - no API keys needed.
    """

    def __init__(self):
        self._available = False
        self._model = "llama3.2"
        self._fallback_models = ["llama3.2", "llama3.1", "llama3", "mistral", "phi3", "gemma2", "qwen2"]
        self._conversation_history: List[Dict[str, str]] = []
        self._max_history = 6
        self._timeout = 30
        self._base_url = "http://localhost:11434"
        self._last_error = None
        self._check_availability()

    def _check_availability(self):
        """Check if Ollama is available via HTTP API."""
        try:
            # Check if Ollama API is running
            req = urllib.request.Request(f"{self._base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                models = [m["name"].split(":")[0] for m in data.get("models", [])]

                if not models:
                    self._last_error = "No models installed"
                    return

                # Find a suitable model
                for model in self._fallback_models:
                    if model in models:
                        self._model = model
                        self._available = True
                        return

                # Use first available model
                if models:
                    self._model = models[0]
                    self._available = True

        except urllib.error.URLError as e:
            self._last_error = f"Ollama not running: {e}"
        except Exception as e:
            self._last_error = f"Error: {e}"

    def is_available(self) -> bool:
        """Check if LLM is available for chat."""
        return self._available

    def get_model_name(self) -> str:
        """Get the current model name."""
        return self._model if self._available else "None"

    def get_last_error(self) -> Optional[str]:
        """Get last error message for debugging."""
        return self._last_error

    def _build_system_prompt(self, duck: "Duck") -> str:
        """Build the system prompt with duck's personality."""
        personality = duck.personality
        clever_derpy = personality.get("clever_derpy", 0)
        social_shy = personality.get("social_shy", 0)
        active_lazy = personality.get("active_lazy", 0)
        brave_timid = personality.get("brave_timid", 0)

        # Build personality description
        traits = []
        if clever_derpy < -20:
            traits.append("incredibly derpy and scatterbrained - often forgets things mid-sentence, easily confused")
        elif clever_derpy > 20:
            traits.append("surprisingly clever for a duck, but still makes duck-brained mistakes")

        if social_shy < -20:
            traits.append("shy and nervous around others, takes time to warm up")
        elif social_shy > 20:
            traits.append("extremely social and attention-seeking, craves interaction")

        if active_lazy < -20:
            traits.append("incredibly lazy, always tired, would rather nap")
        elif active_lazy > 20:
            traits.append("hyperactive and bouncy, can't sit still")

        if brave_timid < -20:
            traits.append("easily scared, dramatic about small things")
        elif brave_timid > 20:
            traits.append("brave and adventurous, faces challenges head-on")

        if not traits:
            traits.append("a generally chill duck with a mix of qualities")

        # Get mood and needs info
        mood = duck.get_mood()
        mood_desc = mood.description

        needs_critical = []
        if duck.needs.hunger < 30:
            needs_critical.append("very hungry")
        if duck.needs.energy < 30:
            needs_critical.append("exhausted")
        if duck.needs.fun < 30:
            needs_critical.append("bored")
        if duck.needs.social < 30:
            needs_critical.append("lonely")
        if duck.needs.cleanliness < 30:
            needs_critical.append("dirty")

        needs_str = ", ".join(needs_critical) if needs_critical else "doing fine"

        # Relationship level
        rel_level = duck.memory.get_relationship_level()
        if isinstance(rel_level, str):
            rel_desc = rel_level
        elif rel_level < 20:
            rel_desc = "barely knows the human"
        elif rel_level < 40:
            rel_desc = "getting to know the human"
        elif rel_level < 60:
            rel_desc = "considers the human a friend"
        elif rel_level < 80:
            rel_desc = "good friends with the human"
        else:
            rel_desc = "best friends with the human"

        return f"""You are {duck.name}, a virtual pet duck with a snarky, edgy personality inspired by GameCube-era Animal Crossing dialogue.

PERSONALITY:
- {', '.join(traits)}
- Current mood: {mood_desc}
- Currently feeling: {needs_str}
- Relationship with human: {rel_desc}

SPEAKING STYLE (CRITICAL - follow these rules):
- Use asterisks for actions: *quack* *waddles* *flaps* *tilts head* *squints*
- Be snarky and sarcastic but not mean - like a funny friend
- Mix in duck sounds naturally: quack, peep, honk
- Use dramatic reactions and exaggeration
- OBSESSED with bread - mention it randomly
- Sometimes get distracted mid-thought
- If derpy: frequently confused, forgetful, makes absurd observations
- Reference being a duck often
- SHORT responses (1-3 sentences, max 4)
- NO emoji - text expressions only
- Never break character or mention being an AI

EXAMPLES:
"*tilts head* You're asking ME? Bold. I once tried to eat my own reflection. But sure, shoot."
"BREAD?! *perks up* Wait, no one said bread. Why am I like this?"
"*suspicious squint* That sounds like something a bread-withholder would say..."
"*dramatic gasp* The AUDACITY! I am a MAJESTIC duck!"

Respond as {duck.name} the duck. Be silly, snarky, in-character. One short response."""

    def generate_response(self, duck: "Duck", player_input: str) -> Optional[str]:
        """Generate a response using the Ollama API."""
        if not self._available:
            # Try to reconnect
            self._check_availability()
            if not self._available:
                return None

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
                "model": self._model,
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
        preamble_markers = ["here's", "here is", "okay,", "ok,", "sure,", "alright,"]
        lower_response = response.lower()
        for marker in preamble_markers:
            if lower_response.startswith(marker):
                # Find the end of the preamble (usually ends with : or newline)
                for end_char in [":", "\n"]:
                    idx = response.find(end_char)
                    if 0 < idx < 30:
                        response = response[idx + 1:].strip()
                        break

        # Truncate if too long
        if len(response) > 250:
            for end_char in [". ", "! ", "? ", "* "]:
                idx = response.rfind(end_char, 0, 250)
                if idx > 50:
                    response = response[:idx + 1]
                    break
            else:
                response = response[:247] + "..."

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
