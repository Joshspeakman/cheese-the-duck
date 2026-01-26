"""
DJ Duck commentary system.

Generates deadpan radio host lines for DJ Duck's Saturday night show.
Uses LLM when available, falls back to pre-written quips.
"""

import random
import threading
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from dialogue.llm_chat import LLMChat


# Pre-written DJ Duck commentary for when LLM is unavailable
INTRO_LINES = [
    "You're listening to DJ Duck. I don't know why either.",
    "DJ Duck here. Let's get this over with.",
    "Welcome to the show. I'm contractually obligated to be here.",
    "It's Saturday night. You're listening to a duck. Think about that.",
    "DJ Duck, live. Unfortunately for both of us.",
    "This is DJ Duck. I have access to music. Here's some.",
    "Saturday night with DJ Duck. My enthusiasm is overwhelming.",
    "You tuned in. That was your choice. I'm just here.",
]

BETWEEN_SONG_LINES = [
    "That was a song. Here's another one.",
    "Music. More of it. You're welcome.",
    "Another track. Try to contain your excitement.",
    "That song ended. This one's starting. Cause and effect.",
    "Here's something else. I picked it. Probably.",
    "Next song. Same general concept as the last one.",
    "More audio. For your ears. You have those, right?",
    "That was... something. This will also be something.",
    "Continuing the show. Because that's how shows work.",
    "Another song. Time continues to pass. Remarkable.",
]

MOOD_OBSERVATIONS = {
    "happy": [
        "You seem happy. Suspicious.",
        "I sense contentment. Weird flex but okay.",
        "Good mood detected. This song won't ruin that. Probably.",
    ],
    "sad": [
        "Feeling down? This next song won't help. But here it is anyway.",
        "Sad duck hours. I get it. Here's noise to fill the void.",
        "Melancholy detected. Music can't fix that but it's something.",
    ],
    "tired": [
        "Tired? Same. Here's a song while we both suffer.",
        "Sleepy vibes. I'd play a lullaby but I don't have one. Here's this instead.",
        "You look exhausted. Join the club. Here's background noise.",
    ],
    "energetic": [
        "High energy detected. Let's match that. Or not. Here's a song.",
        "Feeling peppy? I wouldn't know what that's like. Anyway, music.",
        "You have energy. I have songs. Seems like a fair trade.",
    ],
}

CLOSING_LINES = [
    "And that's the show. We survived. Barely.",
    "DJ Duck signing off. See you next Saturday. If you dare.",
    "Show's over. Go touch grass or whatever.",
    "That's it. That's the show. Don't applaud, I can't hear you anyway.",
    "DJ Duck out. My contractual obligations are fulfilled.",
    "End of broadcast. Time resumes its normal flow.",
]

HOUR_COMMENTS = {
    20: [  # 8 PM
        "8 PM. The show begins. Hold onto your feathers.",
        "It's 8. I'm here. The music exists. Let's do this.",
    ],
    21: [  # 9 PM
        "9 PM. An hour in. Still going.",
        "We've reached 9. Time is relentless.",
    ],
    22: [  # 10 PM
        "10 PM. Past bedtime for sensible ducks.",
        "It's 10. Two hours down. Two to go.",
    ],
    23: [  # 11 PM
        "11 PM. Final stretch. Almost free.",
        "One hour left. We can do this. Probably.",
    ],
}


class DJDuckCommentary:
    """Generates DJ Duck's deadpan radio commentary."""
    
    def __init__(self, llm_chat: Optional['LLMChat'] = None):
        """
        Initialize DJ Duck commentary system.
        
        Args:
            llm_chat: Optional LLMChat instance for dynamic commentary.
        """
        self._llm_chat = llm_chat
        self._last_commentary_type: Optional[str] = None
        self._commentary_count = 0
        self._show_started = False
    
    def set_llm(self, llm_chat: 'LLMChat'):
        """Set the LLM chat instance for dynamic commentary."""
        self._llm_chat = llm_chat
    
    def get_intro(self) -> str:
        """Get a show intro line."""
        self._show_started = True
        self._commentary_count = 0
        
        if self._llm_chat and self._llm_chat.is_available():
            return self._generate_llm_line("intro")
        
        return random.choice(INTRO_LINES)
    
    def get_between_songs(self, duck_mood: Optional[str] = None) -> str:
        """
        Get commentary between songs.
        
        Args:
            duck_mood: Current mood of the duck for contextual comments.
        """
        self._commentary_count += 1
        
        # Occasionally add mood observation
        if duck_mood and random.random() < 0.3:
            mood_lines = MOOD_OBSERVATIONS.get(duck_mood, [])
            if mood_lines:
                return random.choice(mood_lines)
        
        if self._llm_chat and self._llm_chat.is_available():
            return self._generate_llm_line("between", duck_mood)
        
        return random.choice(BETWEEN_SONG_LINES)
    
    def get_hour_comment(self, hour: int) -> Optional[str]:
        """Get commentary for a specific hour, if any."""
        lines = HOUR_COMMENTS.get(hour)
        if lines:
            return random.choice(lines)
        return None
    
    def get_closing(self) -> str:
        """Get a show closing line."""
        self._show_started = False
        
        if self._llm_chat and self._llm_chat.is_available():
            return self._generate_llm_line("closing")
        
        return random.choice(CLOSING_LINES)
    
    def _generate_llm_line(
        self, 
        line_type: str, 
        duck_mood: Optional[str] = None
    ) -> str:
        """Generate commentary using LLM."""
        if not self._llm_chat:
            return self._get_fallback(line_type)
        
        prompts = {
            "intro": (
                "You are DJ Duck, a deadpan, unenthusiastic radio host duck. "
                "Write a single short sentence to start your Saturday night show. "
                "Be dry, slightly sarcastic, and unimpressed with everything. "
                "Keep it under 15 words."
            ),
            "between": (
                "You are DJ Duck, a deadpan radio host duck. "
                f"{'The listener seems ' + duck_mood + '. ' if duck_mood else ''}"
                "Write a single short transition line between songs. "
                "Be dry and unenthusiastic. State the obvious. "
                "Keep it under 15 words."
            ),
            "closing": (
                "You are DJ Duck, a deadpan radio host. "
                "Write a single short sentence to end your show. "
                "Sound relieved it's over. Keep it under 15 words."
            ),
        }
        
        prompt = prompts.get(line_type, prompts["between"])
        
        try:
            # Use a quick generation with low token count
            response = self._llm_chat.generate_quick(
                prompt, 
                max_tokens=50,
                temperature=0.9
            )
            if response and len(response) < 150:
                return response.strip().strip('"')
        except Exception:
            pass
        
        return self._get_fallback(line_type)
    
    def _get_fallback(self, line_type: str) -> str:
        """Get a fallback pre-written line."""
        if line_type == "intro":
            return random.choice(INTRO_LINES)
        elif line_type == "closing":
            return random.choice(CLOSING_LINES)
        else:
            return random.choice(BETWEEN_SONG_LINES)


# Singleton instance with thread-safe initialization
_dj_duck: Optional[DJDuckCommentary] = None
_dj_duck_lock = threading.Lock()


def get_dj_duck() -> DJDuckCommentary:
    """Get the global DJ Duck commentary instance. Thread-safe."""
    global _dj_duck
    if _dj_duck is None:
        with _dj_duck_lock:
            if _dj_duck is None:
                _dj_duck = DJDuckCommentary()
    return _dj_duck
