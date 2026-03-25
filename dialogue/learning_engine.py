"""
Learning Engine — Lightweight conversational learning for Cheese the Duck.

Uses difflib fuzzy matching + SQLite to learn input-response pairs from
every conversation. Over time, Cheese gets better at responding to things
the player says often, without needing any external APIs or heavy NLP libs.

The engine is seeded with all existing template responses on first run,
then continuously learns from successful LLM and keyword responses.
"""
import sqlite3
import difflib
import re
import logging
import threading
from pathlib import Path
from typing import Optional, Tuple, List

from config import SAVE_DIR
from dialogue.content_filter import get_content_filter

logger = logging.getLogger(__name__)

# Database path (separate from JSON saves to avoid bloating save files)
DB_PATH = SAVE_DIR / "cheese_brain.db"

# Text normalization pattern
_NORMALIZE_RE = re.compile(r'[^\w\s]')


def _normalize(text: str) -> str:
    """Normalize text for fuzzy matching: lowercase, strip punctuation."""
    return _NORMALIZE_RE.sub('', text.lower()).strip()


def _tokenize(text: str) -> set:
    """Get unique word tokens from text."""
    return set(_normalize(text).split())


class LearningEngine:
    """
    Learns input-response pairs and fuzzy-matches new inputs to return
    the best learned response. Uses difflib.SequenceMatcher for matching
    and SQLite for persistent storage.
    """

    def __init__(self, db_path: Path = DB_PATH):
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
        self._lock = threading.Lock()
        self._seeded = False
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database."""
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                input_normalized TEXT NOT NULL,
                response TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source TEXT DEFAULT 'template',
                tone TEXT DEFAULT '',
                context TEXT DEFAULT ''
            )
        """)
        # Migrate older schemas
        for col, default in [("tone", "''"), ("context", "''")]:
            try:
                self._conn.execute(f"ALTER TABLE pairs ADD COLUMN {col} TEXT DEFAULT {default}")
            except sqlite3.OperationalError:
                pass  # Column already exists
        self._conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_input_normalized
            ON pairs(input_normalized)
        """)
        self._conn.commit()

        # Check if we have any data
        cursor = self._conn.execute("SELECT COUNT(*) FROM pairs")
        count = cursor.fetchone()[0]
        self._seeded = count > 0

    @property
    def is_seeded(self) -> bool:
        return self._seeded

    @staticmethod
    def clear_all_pairs():
        """Delete all learned pairs from the database (for new game reset)."""
        try:
            conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
            conn.execute("DELETE FROM pairs")
            conn.commit()
            conn.close()
        except Exception:
            pass

    def seed_corpus(self, pairs: List[Tuple[str, str]], source: str = "template"):
        """
        Seed the database with input-response pairs.

        Args:
            pairs: List of (input_pattern, response) tuples.
                   input_pattern can be a topic keyword or a sample question.
            source: Where these pairs came from (template, llm, conversation)
        """
        with self._lock:
            self._conn.executemany(
                """INSERT INTO pairs (input_text, input_normalized, response, source)
                   VALUES (?, ?, ?, ?)""",
                [(inp, _normalize(inp), resp, source) for inp, resp in pairs]
            )
            self._conn.commit()
            self._seeded = True
            logger.info(f"Learning engine seeded with {len(pairs)} pairs from '{source}'")

    def learn(self, player_input: str, duck_response: str,
              source: str = "conversation", tone: str = "",
              context: str = ""):
        """
        Learn a new input-response pair from a successful exchange.

        If this exact pair already exists, increment its frequency.
        Pairs containing blocked content are silently skipped.
        Only learns from voice-safe sources (keyword, seaman).
        """
        normalized = _normalize(player_input)
        if not normalized or not duck_response.strip():
            return

        # Content filter gate — don't learn inappropriate content
        content_filter = get_content_filter()
        if not content_filter.is_safe_to_learn(player_input):
            return
        if not content_filter.is_safe_to_learn(duck_response):
            return

        with self._lock:
            # Check for existing exact match
            cursor = self._conn.execute(
                """SELECT id, frequency FROM pairs
                   WHERE input_normalized = ? AND response = ?""",
                (normalized, duck_response)
            )
            row = cursor.fetchone()

            if row:
                # Boost frequency
                self._conn.execute(
                    """UPDATE pairs SET frequency = frequency + 1,
                       last_used = CURRENT_TIMESTAMP WHERE id = ?""",
                    (row[0],)
                )
            else:
                # New pair
                self._conn.execute(
                    """INSERT INTO pairs
                       (input_text, input_normalized, response, source, tone, context)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (player_input, normalized, duck_response, source, tone, context)
                )
            self._conn.commit()

    def get_response(self, player_input: str,
                     confidence_threshold: float = 0.65) -> Optional[Tuple[str, float]]:
        """
        Find the best learned response for the given input.

        Uses a combination of:
        1. Word overlap (Jaccard similarity) for fast candidate filtering
        2. SequenceMatcher ratio for precise ranking
        3. Frequency weighting (more-used pairs score slightly higher)

        Heavily penalises mismatched lengths to avoid short seed keywords
        (e.g. "hello") matching long player sentences.

        Args:
            player_input: What the player said
            confidence_threshold: Minimum confidence to return a result

        Returns:
            (response_text, confidence) or None if below threshold
        """
        if not self._seeded:
            return None

        normalized = _normalize(player_input)
        if not normalized:
            return None

        input_tokens = _tokenize(player_input)
        if not input_tokens:
            return None

        input_len = len(normalized)

        # Fetch candidates — use word overlap for fast pre-filtering
        # We pull a broader set and score them precisely
        with self._lock:
            cursor = self._conn.execute(
                """SELECT input_normalized, response, frequency
                   FROM pairs ORDER BY frequency DESC LIMIT 5000"""
            )
            candidates = cursor.fetchall()

        if not candidates:
            return None

        best_score = 0.0
        best_response = None

        for stored_input, response, frequency in candidates:
            stored_tokens = set(stored_input.split())
            if not stored_tokens:
                continue

            # Stage 1: fast word overlap check (Jaccard)
            intersection = input_tokens & stored_tokens
            if not intersection:
                continue  # No shared words at all — skip

            union = input_tokens | stored_tokens
            jaccard = len(intersection) / len(union) if union else 0

            # Require meaningful overlap — at least 20% shared words
            if jaccard < 0.2:
                continue

            # Stage 2: precise SequenceMatcher score
            ratio = difflib.SequenceMatcher(
                None, normalized, stored_input
            ).ratio()

            # Stage 3: length similarity penalty
            # Prevents "hello" (5 chars) from matching "what do you
            # think about the meaning of life" (38 chars)
            stored_len = len(stored_input)
            len_ratio = min(input_len, stored_len) / max(input_len, stored_len)
            length_penalty = len_ratio  # 0-1, closer lengths = higher

            # Stage 4: blend scores with frequency bonus
            freq_bonus = min(0.08, (frequency - 1) * 0.015)
            score = (ratio * 0.5 + jaccard * 0.3 + length_penalty * 0.2) + freq_bonus

            if score > best_score:
                best_score = score
                best_response = response

        if best_response and best_score >= confidence_threshold:
            return (best_response, best_score)

        return None

    def prune(self, max_age_days: int = 90, min_frequency: int = 1):
        """
        Remove old, low-frequency learned pairs to prevent unbounded growth.
        Never removes template-seeded pairs or rare-tagged pairs.
        """
        with self._lock:
            self._conn.execute(
                """DELETE FROM pairs
                   WHERE source NOT IN ('template', 'rare')
                   AND frequency <= ?
                   AND last_used < datetime('now', ?)""",
                (min_frequency, f'-{max_age_days} days')
            )
            self._conn.commit()

    def get_stats(self) -> dict:
        """Get statistics about the learning engine."""
        with self._lock:
            total = self._conn.execute("SELECT COUNT(*) FROM pairs").fetchone()[0]
            templates = self._conn.execute(
                "SELECT COUNT(*) FROM pairs WHERE source = 'template'"
            ).fetchone()[0]
            learned = self._conn.execute(
                "SELECT COUNT(*) FROM pairs WHERE source != 'template'"
            ).fetchone()[0]
            top_freq = self._conn.execute(
                "SELECT input_text, frequency FROM pairs ORDER BY frequency DESC LIMIT 5"
            ).fetchall()
            # Source distribution
            sources = self._conn.execute(
                "SELECT source, COUNT(*) FROM pairs GROUP BY source"
            ).fetchall()
            # Avg confidence proxy (avg frequency)
            avg_freq = self._conn.execute(
                "SELECT AVG(frequency) FROM pairs WHERE source != 'template'"
            ).fetchone()[0] or 0.0
            # Staleness: pairs not used in 30+ days
            stale = self._conn.execute(
                "SELECT COUNT(*) FROM pairs WHERE source != 'template' "
                "AND last_used < datetime('now', '-30 days')"
            ).fetchone()[0]
            # Tone distribution
            tones = self._conn.execute(
                "SELECT tone, COUNT(*) FROM pairs WHERE tone != '' GROUP BY tone"
            ).fetchall()
            # Context distribution
            contexts = self._conn.execute(
                "SELECT context, COUNT(*) FROM pairs WHERE context != '' GROUP BY context"
            ).fetchall()

        return {
            "total_pairs": total,
            "template_pairs": templates,
            "learned_pairs": learned,
            "top_inputs": [(t, f) for t, f in top_freq],
            "source_distribution": dict(sources),
            "tone_distribution": dict(tones),
            "context_distribution": dict(contexts),
            "avg_frequency": round(avg_freq, 2),
            "stale_pairs": stale,
        }

    def close(self):
        """Close the database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


# ── Corpus extraction ────────────────────────────────────────────────────────
# Extracts input-response pairs from existing template files to seed the engine.

def extract_corpus() -> List[Tuple[str, str]]:
    """
    Extract all template dialogue as input-response pairs for seeding.

    Maps topic keywords / context descriptions to their response text.
    This gives the learning engine a starting vocabulary of Cheese's voice.
    """
    pairs = []

    # 1. Keyword responses — these have clear input→response mapping
    pairs.extend(_extract_keyword_pairs())

    # 2. Seaman-style mood idles — map mood keywords to idle lines
    pairs.extend(_extract_mood_idle_pairs())

    # 3. Random thoughts — map general prompts to thought text
    pairs.extend(_extract_thought_pairs())

    # 4. Question responses — map question patterns to response text
    pairs.extend(_extract_question_response_pairs())

    logger.info(f"Extracted {len(pairs)} corpus pairs for learning engine")
    return pairs


def _extract_keyword_pairs() -> List[Tuple[str, str]]:
    """Extract pairs from the keyword response engine."""
    pairs = []
    try:
        from dialogue.keyword_responses import get_keyword_engine
        engine = get_keyword_engine()
        # The engine has topic_responses which map keywords to responses
        for topic_resp in engine.topic_responses:
            keywords = topic_resp.keywords
            for keyword in keywords:
                for mood, responses in topic_resp.mood_responses.items():
                    for response in responses:
                        pairs.append((keyword, response))
    except Exception as e:
        logger.debug(f"Could not extract keyword pairs: {e}")
    return pairs


def _extract_mood_idle_pairs() -> List[Tuple[str, str]]:
    """Extract mood→idle line pairs from seaman_style.py templates."""
    pairs = []
    # Map mood names to typical player inputs that would trigger them
    mood_inputs = {
        "happy": ["how are you", "are you happy", "you seem happy", "good day"],
        "sad": ["are you sad", "you seem sad", "what's wrong", "are you okay"],
        "content": ["how's it going", "what's up", "hey", "hello"],
        "grumpy": ["you seem grumpy", "are you angry", "what's bothering you"],
        "anxious": ["are you worried", "you seem nervous", "what's wrong"],
        "tired": ["are you tired", "sleepy", "you look tired", "need rest"],
        "dramatic": ["drama", "being dramatic", "you're dramatic"],
        "petty": ["you're petty", "still mad", "holding a grudge"],
    }

    try:
        from dialogue.seaman_style import SeamanDialogue
        sd = SeamanDialogue()
        # Generate some idle lines for each mood to extract the templates
        for mood, inputs in mood_inputs.items():
            for _ in range(3):
                line = sd.generate_idle(mood)
                for inp in inputs:
                    pairs.append((inp, line.text))
    except Exception as e:
        logger.debug(f"Could not extract mood idle pairs: {e}")
    return pairs


def _extract_thought_pairs() -> List[Tuple[str, str]]:
    """Extract random thought pairs."""
    pairs = []
    thought_inputs = [
        "what are you thinking about",
        "penny for your thoughts",
        "tell me something",
        "talk to me",
        "say something",
        "what's on your mind",
        "share a thought",
    ]
    try:
        from dialogue.seaman_style import SeamanDialogue
        sd = SeamanDialogue()
        for _ in range(20):
            line = sd.get_random_thought()
            for inp in thought_inputs:
                pairs.append((inp, line.text))
    except Exception as e:
        logger.debug(f"Could not extract thought pairs: {e}")
    return pairs


def _extract_question_response_pairs() -> List[Tuple[str, str]]:
    """Extract question-response pairs from the conversation system."""
    pairs = []
    try:
        from dialogue.seaman_style import SeamanDialogue
        sd = SeamanDialogue()

        # Common questions players ask
        question_types = [
            ("how are you", "how_are_you"),
            ("what are you thinking", "thinking"),
            ("what's your name", "name"),
            ("do you like me", "like_me"),
            ("what do you want", "want"),
            ("are you hungry", "hungry"),
            ("tell me a joke", "joke"),
            ("what's your favorite food", "favorite_food"),
            ("do you dream", "dream"),
            ("are you lonely", "lonely"),
        ]

        for question, _ in question_types:
            line = sd.generate_question_response(question, None, None)
            pairs.append((question, line.text))
    except Exception as e:
        logger.debug(f"Could not extract question response pairs: {e}")
    return pairs


# ── Singleton ────────────────────────────────────────────────────────────────

_instance: Optional[LearningEngine] = None
_seed_thread: Optional[threading.Thread] = None


def get_learning_engine() -> LearningEngine:
    """Get or create the singleton LearningEngine instance."""
    global _instance, _seed_thread
    if _instance is None:
        _instance = LearningEngine()

        # Seed in background on first run (like LLM loading pattern)
        if not _instance.is_seeded:
            def _seed():
                try:
                    corpus = extract_corpus()
                    if corpus:
                        _instance.seed_corpus(corpus, source="template")
                except Exception as e:
                    logger.error(f"Failed to seed learning engine: {e}")

            _seed_thread = threading.Thread(target=_seed, daemon=True)
            _seed_thread.start()

    return _instance
