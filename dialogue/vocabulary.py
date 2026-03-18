"""
Vocabulary Learning — Lets Cheese learn new words from the player.

When the player teaches Cheese what a word means, it gets stored
and occasionally surfaces in his responses.  All learned words pass
through the ContentFilter before storage.
"""
import logging
import random
import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

from dialogue.content_filter import get_content_filter

logger = logging.getLogger(__name__)

# Maximum number of words Cheese can remember
MAX_VOCABULARY = 150

# Teaching patterns — (compiled regex, group index for word, group index for definition)
_TEACHING_PATTERNS = [
    # "the word X means Y" — must come before generic "X means Y"
    (re.compile(r'the\s+word\s+["\']?(\w+)["\']?\s+means?\s+(.+)', re.IGNORECASE), 1, 2),
    # "do you know what X means" — detection only, no definition yet
    (re.compile(r'do\s+you\s+know\s+what\s+["\']?(\w+)["\']?\s+means?', re.IGNORECASE), 1, None),
    # "X means Y"
    (re.compile(r'\b(\w[\w\s]{0,25}?)\s+means?\s+(.+)', re.IGNORECASE), 1, 2),
    # "X is when Y"
    (re.compile(r'\b(\w[\w\s]{0,25}?)\s+is\s+when\s+(.+)', re.IGNORECASE), 1, 2),
    # "X is a/an Y" (only short X to avoid matching normal sentences)
    (re.compile(r'\b(\w{2,15})\s+is\s+an?\s+(.{5,})', re.IGNORECASE), 1, 2),
]

# Acknowledgment responses when Cheese learns a new word
_LEARN_RESPONSES = [
    "Noted. {word}. I'll file that somewhere important.",
    "So {word} means {definition}. Humans are complicated.",
    "{word}. Got it. My vocabulary just expanded. You should be proud. Or concerned.",
    "I have added {word} to my personal dictionary. Which is just my brain. Same thing.",
    "{word}. Interesting. I'll pretend I didn't already know that.",
    "Filing {word} under 'things I now know because of you.'",
    "*writes {word} on invisible notepad* Continue.",
    "{word}. {definition}. I'll remember that. I remember everything. It's a curse.",
]

# Responses when Cheese already knows the word
_ALREADY_KNOW_RESPONSES = [
    "I already know what {word} means. You told me. I remember things.",
    "{word}. Yes. We've covered this. My memory is impeccable.",
    "You taught me {word} already. {definition}. See? Perfect recall.",
]

# Responses when Cheese uses a learned word
_USAGE_INTROS = [
    "Speaking of {word} — ",
    "As I've learned, {word}: {definition}. Relevant? Maybe not. But I said it.",
    "*adjusts feathers* {word}. That's a thing you taught me. I use it now.",
    "To use a word I learned from you: {word}.",
]


@dataclass
class LearnedWord:
    """A word Cheese learned from the player."""
    word: str
    definition: str
    context: str           # sentence it was taught in
    learned_at: float      # timestamp
    times_used: int = 0    # how often Cheese has used it
    confidence: float = 0.7

    def to_dict(self) -> Dict[str, Any]:
        return {
            "word": self.word,
            "definition": self.definition,
            "context": self.context,
            "learned_at": self.learned_at,
            "times_used": self.times_used,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnedWord":
        return cls(
            word=data["word"],
            definition=data["definition"],
            context=data.get("context", ""),
            learned_at=data.get("learned_at", 0.0),
            times_used=data.get("times_used", 0),
            confidence=data.get("confidence", 0.7),
        )


class VocabularyMemory:
    """
    Stores words the player has taught Cheese and provides
    methods for detecting teaching attempts and formatting responses.
    """

    def __init__(self) -> None:
        self._words: Dict[str, LearnedWord] = {}
        self._filter = get_content_filter()

    # -- teaching detection -----------------------------------------------

    def detect_teaching(self, text: str) -> Optional[Dict[str, str]]:
        """
        Check if the player is trying to teach Cheese a word.

        Returns a dict with 'word' and optionally 'definition' keys,
        or None if no teaching pattern was detected.
        """
        for pattern, word_group, def_group in _TEACHING_PATTERNS:
            m = pattern.search(text)
            if m:
                word = m.group(word_group).strip().lower()
                # Skip very short or very long "words"
                if len(word) < 2 or len(word) > 30:
                    continue
                # Skip common false positives
                if word in _FALSE_POSITIVE_WORDS:
                    continue

                definition = m.group(def_group).strip().rstrip(".!?") if def_group else None
                if definition and len(definition) < 3:
                    continue

                return {"word": word, "definition": definition}
        return None

    def try_learn(self, text: str) -> Optional[str]:
        """
        Attempt to learn a word from the player's message.

        Returns an acknowledgment response if a word was learned,
        or None if no teaching was detected or the word was filtered.
        """
        detected = self.detect_teaching(text)
        if not detected:
            return None

        word = detected["word"]
        definition = detected.get("definition")

        if not definition:
            # Player asked "do you know what X means?" — we don't have a def yet
            if word in self._words:
                lw = self._words[word]
                return f"{word}. Yes. It means {lw.definition}. You taught me that."
            return None  # Don't respond here; let normal dialogue handle the question

        # Content filter gate
        if not self._filter.is_safe_to_learn(word):
            logger.debug("Blocked learning word: %s (failed filter)", word)
            return None
        if not self._filter.is_safe_to_learn(definition):
            logger.debug("Blocked learning definition for %s (failed filter)", word)
            return None

        # Already know this word?
        if word in self._words:
            existing = self._words[word]
            if existing.definition.lower() == definition.lower():
                existing.times_confirmed = getattr(existing, 'times_confirmed', 0) + 1
                existing.confidence = min(1.0, existing.confidence + 0.1)
                return random.choice(_ALREADY_KNOW_RESPONSES).format(
                    word=word, definition=existing.definition
                )
            else:
                # Update definition
                existing.definition = definition
                existing.context = text
                existing.confidence = 0.8
                return f"Wait. I thought {word} meant {existing.definition}. But now it means {definition}? Updating my files."

        # Enforce capacity
        if len(self._words) >= MAX_VOCABULARY:
            self._evict_one()

        # Store it
        self._words[word] = LearnedWord(
            word=word,
            definition=definition,
            context=text,
            learned_at=time.time(),
        )

        return random.choice(_LEARN_RESPONSES).format(
            word=word, definition=definition
        )

    # -- usage in responses -----------------------------------------------

    def check_usage(self, player_text: str) -> Optional[str]:
        """
        If the player's message contains a learned word, optionally
        return a line where Cheese references his knowledge.

        Low probability (~8%) to keep it natural.
        """
        if not self._words:
            return None

        text_lower = player_text.lower()
        text_words = set(re.findall(r'\b\w+\b', text_lower))
        matches = [w for w in self._words if w in text_words]

        if not matches:
            return None

        if random.random() > 0.08:
            return None

        word = random.choice(matches)
        lw = self._words[word]
        lw.times_used += 1
        return random.choice(_USAGE_INTROS).format(
            word=lw.word, definition=lw.definition
        )

    def get_random_word_thought(self) -> Optional[str]:
        """
        Occasionally return an idle thought about a learned word.
        For use in idle dialogue.
        """
        if not self._words:
            return None

        candidates = [w for w in self._words.values() if w.confidence >= 0.5]
        if not candidates:
            return None

        lw = random.choice(candidates)
        lw.times_used += 1
        thoughts = [
            f"I was thinking about the word '{lw.word}.' {lw.definition}. You taught me that. I use it internally now.",
            f"'{lw.word}.' That's a word I know because of you. My vocabulary grows. Concerning.",
            f"Did you know I know what '{lw.word}' means? {lw.definition}. I'm basically a scholar.",
            f"*stares at pond* '{lw.word}.' I keep going over that one. {lw.definition}. Important stuff.",
        ]
        return random.choice(thoughts)

    # -- lookup -----------------------------------------------------------

    def knows_word(self, word: str) -> bool:
        return word.lower() in self._words

    def get_definition(self, word: str) -> Optional[str]:
        lw = self._words.get(word.lower())
        return lw.definition if lw else None

    @property
    def word_count(self) -> int:
        return len(self._words)

    @property
    def all_words(self) -> List[str]:
        return list(self._words.keys())

    # -- persistence ------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "words": {k: v.to_dict() for k, v in self._words.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VocabularyMemory":
        mem = cls()
        for key, word_data in data.get("words", {}).items():
            mem._words[key] = LearnedWord.from_dict(word_data)
        return mem

    # -- internal ---------------------------------------------------------

    def _evict_one(self) -> None:
        """Remove the least useful word to make room."""
        if not self._words:
            return
        # Evict lowest confidence + oldest
        evict_key = min(
            self._words,
            key=lambda k: (self._words[k].confidence, -self._words[k].learned_at)
        )
        del self._words[evict_key]


# Common words that would false-positive on teaching patterns
_FALSE_POSITIVE_WORDS = {
    "it", "he", "she", "they", "we", "you", "i", "this", "that",
    "there", "here", "what", "who", "how", "the", "a", "an",
    "cheese", "duck", "game", "thing", "stuff", "something",
    "nothing", "everything", "everyone", "someone", "today",
    "tomorrow", "yesterday", "now", "then", "life", "time",
    "is", "are", "was", "were", "been", "being",
}
