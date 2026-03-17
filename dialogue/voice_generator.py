"""
Voice Generator — Markov chain text generation in Cheese's voice.

Uses Markovify to train on ALL existing Cheese dialogue and generate
novel lines that statistically mirror his vocabulary, rhythm, and style.

Generated text goes through a SeamanStyleFilter to enforce the golden
voice rules (max 3 sentences, no enthusiasm !, length bounds, etc).

Gated by interaction count — only activates after 100+ interactions
so new players get the hand-curated template experience first.
"""
import re
import json
import logging
import threading
from pathlib import Path
from typing import Optional, List

from config import SAVE_DIR

logger = logging.getLogger(__name__)

# Brain file path
BRAIN_PATH = SAVE_DIR / "cheese_voice.json"

# Minimum interactions before voice generator activates
MIN_INTERACTIONS = 100


class SeamanStyleFilter:
    """
    Validates generated text against Cheese's golden voice rules.

    Rules:
    1. Max 3 sentences per response
    2. No exclamation marks for enthusiasm (only protest/false bravado)
    3. Length between 10 and 200 characters
    4. No obviously broken/gibberish output
    5. Must contain at least 3 words
    """

    # Words that make ! acceptable (protest/bravado, not enthusiasm)
    _OKAY_BANG_PATTERNS = re.compile(
        r"(MINE|NO|STOP|I'M NOT|DON'T|NEVER|LEAVE|EXCUSE ME|RUDE|HEY)",
        re.IGNORECASE
    )

    # Banned patterns (things that would break character)
    _BANNED = re.compile(
        r"(https?://|www\.|@\w+|#\w+|\bLOL\b|\bOMG\b|\bROFL\b)",
        re.IGNORECASE
    )

    @classmethod
    def validate(cls, text: str) -> Optional[str]:
        """
        Validate and clean generated text.
        Returns cleaned text or None if it fails validation.
        """
        if not text or not text.strip():
            return None

        text = text.strip()

        # Length check
        if len(text) < 10 or len(text) > 200:
            return None

        # Word count check
        words = text.split()
        if len(words) < 3:
            return None

        # Sentence count check (max 3)
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        if len(sentences) > 3:
            # Truncate to 3 sentences
            truncated = '. '.join(sentences[:3])
            if not truncated.endswith('.'):
                truncated += '.'
            text = truncated

        # Exclamation mark check — only okay for protest/bravado
        if '!' in text and not cls._OKAY_BANG_PATTERNS.search(text):
            text = text.replace('!', '.')

        # Banned patterns
        if cls._BANNED.search(text):
            return None

        # Check for obvious gibberish: too many repeated words
        if len(words) > 4:
            unique_ratio = len(set(w.lower() for w in words)) / len(words)
            if unique_ratio < 0.3:
                return None

        return text


class VoiceGenerator:
    """
    Generates novel dialogue lines in Cheese's voice using Markov chains.
    """

    def __init__(self, brain_path: Path = BRAIN_PATH):
        self._brain_path = brain_path
        self._brain_path.parent.mkdir(parents=True, exist_ok=True)
        self._model = None
        self._trained = False
        self._lock = threading.Lock()

    @property
    def is_trained(self) -> bool:
        return self._trained

    def train(self, corpus_lines: List[str]):
        """
        Train the Markov model on a corpus of Cheese dialogue lines.

        Args:
            corpus_lines: List of dialogue strings in Cheese's voice
        """
        try:
            import markovify
        except ImportError:
            logger.warning("markovify not installed — voice generator disabled")
            return

        if not corpus_lines:
            return

        with self._lock:
            # Join all lines into a single text body for markovify
            # Each line is treated as a sentence
            corpus_text = '\n'.join(corpus_lines)

            self._model = markovify.NewlineText(
                corpus_text,
                state_size=2,  # Bigrams — good balance of coherence vs novelty
                well_formed=False,  # Don't reject sentences without end punctuation
            )
            self._trained = True

            # Save the model for persistence
            self._save()
            logger.info(f"Voice generator trained on {len(corpus_lines)} lines")

    def _save(self):
        """Save the trained model to disk."""
        if self._model:
            try:
                model_json = self._model.to_json()
                self._brain_path.write_text(model_json)
            except Exception as e:
                logger.debug(f"Could not save voice model: {e}")

    def load(self) -> bool:
        """Load a previously trained model from disk."""
        if not self._brain_path.exists():
            return False

        try:
            import markovify
        except ImportError:
            return False

        try:
            model_json = self._brain_path.read_text()
            self._model = markovify.NewlineText.from_json(model_json)
            self._trained = True
            logger.info("Voice generator loaded from disk")
            return True
        except Exception as e:
            logger.debug(f"Could not load voice model: {e}")
            return False

    def generate(self, hint: str = None, max_attempts: int = 20) -> Optional[str]:
        """
        Generate a novel line in Cheese's voice.

        Args:
            hint: Optional seed word to try to work into the generation
            max_attempts: Number of generation attempts before giving up

        Returns:
            A validated line or None
        """
        if not self._trained or not self._model:
            return None

        with self._lock:
            for _ in range(max_attempts):
                try:
                    # Generate a sentence
                    if hint:
                        raw = self._model.make_sentence_with_start(
                            hint, strict=False, tries=5
                        )
                    else:
                        raw = None

                    if not raw:
                        raw = self._model.make_sentence(tries=5)

                    if raw:
                        cleaned = SeamanStyleFilter.validate(raw)
                        if cleaned:
                            return cleaned
                except Exception:
                    continue

        return None

    def generate_batch(self, count: int = 5) -> List[str]:
        """Generate multiple validated lines."""
        results = []
        for _ in range(count * 3):  # Over-generate since some will be filtered
            line = self.generate()
            if line and line not in results:
                results.append(line)
                if len(results) >= count:
                    break
        return results


# ── Corpus extraction for training ───────────────────────────────────────────

def extract_voice_corpus() -> List[str]:
    """
    Extract all Cheese dialogue text from template files for training.
    Returns a list of individual dialogue lines.
    """
    lines = set()  # Deduplicate

    # Extract from seaman_style.py — the richest source
    lines.update(_extract_seaman_lines())

    # Extract from keyword responses
    lines.update(_extract_keyword_lines())

    # Extract from mood dialogue
    lines.update(_extract_mood_lines())

    # Extract from contextual dialogue
    lines.update(_extract_contextual_lines())

    # Extract from conversation.py templates
    lines.update(_extract_conversation_lines())

    # Clean: remove emote-only lines and very short lines
    cleaned = []
    for line in lines:
        # Strip emotes for training (we want the text voice, not stage directions)
        text = re.sub(r'\*[^*]+\*', '', line).strip()
        if text and len(text) >= 15:
            cleaned.append(text)

    logger.info(f"Extracted {len(cleaned)} unique voice corpus lines")
    return cleaned


def _extract_seaman_lines() -> set:
    """Extract dialogue text from seaman_style.py template dicts."""
    lines = set()
    try:
        from dialogue.seaman_style import SeamanDialogue
        sd = SeamanDialogue()

        # Generate a large sample of idle lines across moods
        moods = ["happy", "sad", "content", "grumpy", "anxious", "tired",
                 "dramatic", "petty"]
        for mood in moods:
            for _ in range(10):
                line = sd.generate_idle(mood)
                lines.add(line.text)

        # Random thoughts
        for _ in range(40):
            line = sd.get_random_thought()
            lines.add(line.text)

    except Exception as e:
        logger.debug(f"Could not extract seaman lines: {e}")
    return lines


def _extract_keyword_lines() -> set:
    """Extract response text from keyword response modules."""
    lines = set()
    try:
        from dialogue.keyword_responses import get_keyword_engine
        engine = get_keyword_engine()
        for topic_resp in engine.topic_responses:
            for mood, responses in topic_resp.mood_responses.items():
                for response in responses:
                    lines.add(response)
    except Exception as e:
        logger.debug(f"Could not extract keyword lines: {e}")
    return lines


def _extract_mood_lines() -> set:
    """Extract response text from mood_dialogue.py."""
    lines = set()
    try:
        from dialogue.mood_dialogue import MOOD_RESPONSES
        for mood, contexts in MOOD_RESPONSES.items():
            if isinstance(contexts, dict):
                for context, responses in contexts.items():
                    if isinstance(responses, list):
                        for resp in responses:
                            if isinstance(resp, str):
                                lines.add(resp)
    except Exception as e:
        logger.debug(f"Could not extract mood lines: {e}")
    return lines


def _extract_contextual_lines() -> set:
    """Extract response text from contextual_dialogue.py."""
    lines = set()
    try:
        from dialogue.contextual_dialogue import CONTEXTUAL_COMMENTS
        if isinstance(CONTEXTUAL_COMMENTS, dict):
            for category, items in CONTEXTUAL_COMMENTS.items():
                if isinstance(items, dict):
                    for key, responses in items.items():
                        if isinstance(responses, list):
                            for resp in responses:
                                if isinstance(resp, str):
                                    lines.add(resp)
                                elif hasattr(resp, 'text'):
                                    lines.add(resp.text)
                elif isinstance(items, list):
                    for resp in items:
                        if isinstance(resp, str):
                            lines.add(resp)
    except Exception as e:
        logger.debug(f"Could not extract contextual lines: {e}")
    return lines


def _extract_conversation_lines() -> set:
    """Extract response text from conversation.py DIALOGUE templates."""
    lines = set()
    try:
        from dialogue.conversation import DIALOGUE
        if isinstance(DIALOGUE, dict):
            for category, responses in DIALOGUE.items():
                if isinstance(responses, list):
                    for resp in responses:
                        if isinstance(resp, str):
                            lines.add(resp)
    except Exception as e:
        logger.debug(f"Could not extract conversation lines: {e}")
    return lines


# ── Singleton ────────────────────────────────────────────────────────────────

_instance: Optional[VoiceGenerator] = None
_train_thread: Optional[threading.Thread] = None


def get_voice_generator() -> VoiceGenerator:
    """Get or create the singleton VoiceGenerator instance."""
    global _instance, _train_thread
    if _instance is None:
        _instance = VoiceGenerator()

        # Try to load existing brain
        if not _instance.load():
            # Train in background on first run
            def _train():
                try:
                    corpus = extract_voice_corpus()
                    if corpus:
                        _instance.train(corpus)
                except Exception as e:
                    logger.error(f"Failed to train voice generator: {e}")

            _train_thread = threading.Thread(target=_train, daemon=True)
            _train_thread.start()

    return _instance
