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
    "DJ Duck. Back again. Like a recurring dream you can't explain.",
    "Welcome. I have songs. You have ears. Let's see where this goes.",
    "It's me. The duck. With the music. You're still here. Noted.",
    "DJ Duck broadcasting. From a pond. The acoustics are terrible.",
    "Hello. It's Saturday. I'm a duck with a playlist. Life is strange.",
    "DJ Duck, live and... present. That's the best I can offer.",
    "You found the show. Congratulations. Or my condolences. Either way.",
    "Saturday night radio. Hosted by waterfowl. Standards have never been lower.",
    "This is DJ Duck. I picked these songs. Some of them on purpose.",
    "Welcome to the only show hosted by a duck. The competition was zero.",
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
    "Song transition. Smooth as a duck on water. Which is very smooth.",
    "That one's done. This one isn't. Enjoy the difference.",
    "Here's another one I picked. My taste is... present.",
    "Moving on. Like life. But with more bass.",
    "Next track. I put thought into this. Some thought. A thought.",
    "And now this. Because silence would be too honest.",
    "More music. The alternative was me talking. You're welcome.",
    "Transitioning. Between songs. It's what I do. Besides floating.",
    "That ended. This begins. The cycle continues.",
    "Another selection from DJ Duck. Curated with mild indifference.",
    "Here's the next one. I'd describe it but that seems like effort.",
    "Song change. Same vibes. Different vibrations. That's basically the same thing.",
    "Next up. I could tell you about it. But I won't. Mystery is my brand.",
    "That was track... something. I lost count. Here's another.",
]

MOOD_OBSERVATIONS = {
    "happy": [
        "You seem happy. Suspicious.",
        "I sense contentment. Weird flex but okay.",
        "Good mood detected. This song won't ruin that. Probably.",
        "You're in a good mood. I had nothing to do with that. But I'll take credit.",
        "Happy listener. That's new. I'll try not to ruin it.",
        "Positive vibes detected. Foreign territory for me. But here we are.",
    ],
    "sad": [
        "Feeling down? This next song won't help. But here it is anyway.",
        "Sad duck hours. I get it. Here's noise to fill the void.",
        "Melancholy detected. Music can't fix that but it's something.",
        "You seem... heavy. Music won't solve it. But it sits with you. Like a duck.",
        "Sad vibes. I get those too. Between songs 3 and 4 usually.",
        "I'm sensing feelings. The sad kind. This next song is just a song. But it's here.",
    ],
    "tired": [
        "Tired? Same. Here's a song while we both suffer.",
        "Sleepy vibes. I'd play a lullaby but I don't have one. Here's this instead.",
        "You look exhausted. Join the club. Here's background noise.",
        "Tired listener alert. I'll keep the commentary short. You're welcome.",
        "You and sleep are clearly not on speaking terms tonight.",
        "Fatigue detected. I'd offer a pillow but I'm a duck. I offer music instead.",
    ],
    "energetic": [
        "High energy detected. Let's match that. Or not. Here's a song.",
        "Feeling peppy? I wouldn't know what that's like. Anyway, music.",
        "You have energy. I have songs. Seems like a fair trade.",
        "Energetic listener. I'll try to keep up. I won't. But I'll try.",
        "So much energy. I'm exhausted just observing. Here's an upbeat one. Maybe.",
        "You're buzzing. I'm floating. Same energy. Different execution.",
    ],
    "bored": [
        "Bored? I'm a duck playing music. What more do you want.",
        "I sense restlessness. Maybe this next song will fix that. Doubt it though.",
        "You seem bored. That's fair. I'm a duck on the radio. Expectations should be low.",
    ],
    "content": [
        "You seem peaceful. I won't disrupt that. Much.",
        "Content listener detected. Perfect conditions for mediocre radio.",
        "You look... okay. That's the sweet spot. Here's a song that won't change that.",
    ],
}

CLOSING_LINES = [
    "And that's the show. We survived. Barely.",
    "DJ Duck signing off. See you next Saturday. If you dare.",
    "Show's over. Go touch grass or whatever.",
    "That's it. That's the show. Don't applaud, I can't hear you anyway.",
    "DJ Duck out. My contractual obligations are fulfilled.",
    "End of broadcast. Time resumes its normal flow.",
    "That's all the music I have. That's a lie. But the show's over.",
    "Signing off. The pond awaits. It always does.",
    "Show's done. I'm going back to floating. My real calling.",
    "DJ Duck, out. Same time next week. Or don't. I'll be here either way.",
    "End of show. Thanks for listening. Or having this on in the background. Same thing.",
    "We're done. I'd say it was fun but I have standards for the word 'fun'.",
    "That's a wrap. Go do something else. Anything. I believe in you. Mildly.",
]

HOUR_COMMENTS = {
    20: [  # 8 PM
        "8 PM. The show begins. Hold onto your feathers.",
        "It's 8. I'm here. The music exists. Let's do this.",
        "Eight o'clock. Prime duck radio hours. If that's a thing. It's a thing now.",
        "8 PM. The night is young. I am not. Let's begin.",
    ],
    21: [  # 9 PM
        "9 PM. An hour in. Still going.",
        "We've reached 9. Time is relentless.",
        "One hour down. Three to go. Not that I'm counting. I'm definitely counting.",
        "9 PM. Still awake. Both of us. Impressive.",
    ],
    22: [  # 10 PM
        "10 PM. Past bedtime for sensible ducks.",
        "It's 10. Two hours down. Two to go.",
        "22 hundred hours. Military time. Because this show is serious business.",
        "10 PM. We're in the deep end now. Of the show. And the pond.",
    ],
    23: [  # 11 PM
        "11 PM. Final stretch. Almost free.",
        "One hour left. We can do this. Probably.",
        "11 PM. The home stretch. I can see the finish line. It looks like sleep.",
        "Almost midnight. The songs get weirder at this hour. I get weirder at this hour.",
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

    def _ensure_llm(self) -> bool:
        """Auto-connect to LLM if not set. Returns True if LLM is available."""
        if not self._llm_chat:
            try:
                from dialogue.llm_chat import get_llm_chat
                self._llm_chat = get_llm_chat()
            except Exception:
                return False
        return self._llm_chat is not None and self._llm_chat.is_available()

    def get_intro(self) -> str:
        """Get a show intro line."""
        self._show_started = True
        self._commentary_count = 0
        
        if self._ensure_llm():
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
        
        if self._ensure_llm():
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
        
        if self._ensure_llm():
            return self._generate_llm_line("closing")
        
        return random.choice(CLOSING_LINES)
    
    def _generate_llm_line(
        self, 
        line_type: str, 
        duck_mood: Optional[str] = None
    ) -> str:
        """Generate commentary using LLM."""
        if not self._llm_chat or not self._llm_chat.is_available():
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
            if not self._llm_chat._llama:
                return self._get_fallback(line_type)
            # Use raw completion with low token count for quick DJ lines
            from dialogue.llm_chat import _call_with_timeout
            response = _call_with_timeout(
                lambda: self._llm_chat._llama(
                    prompt,
                    max_tokens=50,
                    temperature=0.9,
                    top_p=0.9,
                    stop=["\n\n", ".", "!"],
                ),
                timeout=10.0
            )
            if response and "choices" in response and response["choices"]:
                content = response["choices"][0].get("text", "").strip()
                if content and len(content) < 150:
                    return content.strip('"')
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
