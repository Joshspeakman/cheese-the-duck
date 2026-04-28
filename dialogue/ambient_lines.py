"""
Ambient Line Generator — Background LLM dialogue pre-generation.

After player interactions, quietly asks the LLM to generate a small batch
of future dialogue lines in Cheese's deadpan voice. These are stored in
SQLite and consumed later by existing dialogue systems (greetings, idle
thoughts, after-action responses, callbacks).

Fully non-blocking: uses a single worker thread with fire-and-forget
semantics. If the worker is busy or the LLM is unavailable, requests
are silently dropped. The game never waits on this system.
"""
import sqlite3
import logging
import threading
import time
import random
import re
import concurrent.futures
from pathlib import Path
from typing import Optional, List, Tuple, Dict

from config import SAVE_DIR

logger = logging.getLogger(__name__)

# Storage in the same DB as LearningEngine
DB_PATH = SAVE_DIR / "cheese_brain.db"

# Valid context types for generated lines
VALID_CONTEXTS = frozenset({
    "greeting", "feed", "play", "pet", "clean",
    "idle", "callback", "chat_response",
})

# chat_response lines older than this are stale — the conversation moved on
CHAT_RESPONSE_STALENESS_SECONDS = 600  # 10 minutes

# Regex to parse tagged lines from LLM output
# Matches patterns like "greeting: *blinks* Oh. Josh." or "- idle: ..."
_LINE_RE = re.compile(
    r"^[-*\d.)\s]*(?P<ctx>" + "|".join(VALID_CONTEXTS) + r")\s*:\s*(?P<text>.+)",
    re.IGNORECASE,
)


class AmbientLineGenerator:
    """
    Generates future dialogue lines in the background via LLM.

    Usage:
        gen = AmbientLineGenerator(llm_chat)
        gen.request_lines("chat", player_input="my name is Josh",
                          duck_response="Noted.", context={...})

    Lines are stored in SQLite and consumed via consume_line(context).
    """

    def __init__(self, llm_chat=None, cooldown: float = 120.0,
                 max_stored: int = 100):
        self._llm_chat = llm_chat
        self._cooldown = cooldown
        self._max_stored = max_stored
        # Respect the cooldown after startup so the first chat does not
        # immediately launch another LLM job for future-line enrichment.
        self._last_generation_time = time.time() if cooldown > 0 else 0.0
        self._worker = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self._busy = False  # Simple flag — no lock needed for a bool check
        self._lock = threading.Lock()
        self._conn: Optional[sqlite3.Connection] = None
        self._consecutive_failures = 0
        self._max_consecutive_failures = 3  # Back off after 3 failures
        self._init_db()

    # ── Database ──────────────────────────────────────────────────────

    def _init_db(self):
        """Create the ambient_lines table if it doesn't exist."""
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS ambient_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at REAL NOT NULL,
                used INTEGER DEFAULT 0,
                source_trigger TEXT,
                topics TEXT DEFAULT ''
            )
        """)
        # Add topics column if upgrading from older schema
        try:
            self._conn.execute(
                "ALTER TABLE ambient_lines ADD COLUMN topics TEXT DEFAULT ''"
            )
        except sqlite3.OperationalError:
            pass  # Column already exists
        self._conn.commit()
        self._conn.commit()

    def _store_lines(self, lines: List[Tuple[str, str]], source_trigger: str,
                     topics: str = ""):
        """Store parsed lines in the database."""
        if not self._conn:
            return
        now = time.time()
        with self._lock:
            for ctx, text in lines:
                self._conn.execute(
                    "INSERT INTO ambient_lines (context, text, created_at, source_trigger, topics) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (ctx, text, now, source_trigger, topics),
                )
            self._conn.commit()
            self._prune()

    def _prune(self):
        """Keep only the newest max_stored unused lines."""
        # Delete used lines older than 1 hour
        cutoff = time.time() - 3600
        self._conn.execute(
            "DELETE FROM ambient_lines WHERE used = 1 AND created_at < ?",
            (cutoff,),
        )
        # If we still have too many unused lines, delete oldest
        count = self._conn.execute(
            "SELECT COUNT(*) FROM ambient_lines WHERE used = 0"
        ).fetchone()[0]
        if count > self._max_stored:
            excess = count - self._max_stored
            self._conn.execute(
                "DELETE FROM ambient_lines WHERE id IN ("
                "  SELECT id FROM ambient_lines WHERE used = 0 "
                "  ORDER BY created_at ASC LIMIT ?"
                ")",
                (excess,),
            )
        self._conn.commit()

    # ── Line consumption (called from DuckBrain) ─────────────────────

    def consume_line(self, context: str, mood: str = "") -> Optional[str]:
        """
        Get and mark-as-used one ambient line for the given context.
        
        If mood is provided, prefers lines matching that tonal range.
        Returns None if no unused lines are available for that context.
        """
        if not self._conn:
            return None
        with self._lock:
            # If mood provided, try to pick a tonally-appropriate line
            if mood and mood in ("sad", "miserable", "grumpy"):
                # Prefer melancholic lines (containing *sigh*, ellipsis, etc.)
                row = self._conn.execute(
                    "SELECT id, text FROM ambient_lines "
                    "WHERE context = ? AND used = 0 "
                    "AND (text LIKE '%...%' OR text LIKE '%*sigh%' OR text LIKE '%*stares%') "
                    "ORDER BY created_at ASC LIMIT 1",
                    (context,),
                ).fetchone()
                if row:
                    self._conn.execute(
                        "UPDATE ambient_lines SET used = 1 WHERE id = ?",
                        (row[0],),
                    )
                    self._conn.commit()
                    return row[1]
            
            row = self._conn.execute(
                "SELECT id, text FROM ambient_lines "
                "WHERE context = ? AND used = 0 "
                "ORDER BY created_at ASC LIMIT 1",
                (context,),
            ).fetchone()
            if not row:
                return None
            self._conn.execute(
                "UPDATE ambient_lines SET used = 1 WHERE id = ?",
                (row[0],),
            )
            self._conn.commit()
            return row[1]

    def consume_chat_response(self, player_input: str = "") -> Optional[str]:
        """
        Try to consume a chat_response ambient line, preferring topic matches.

        Lines older than CHAT_RESPONSE_STALENESS_SECONDS are auto-expired
        to prevent context-drifted responses.
        """
        if not self._conn:
            return None
        staleness_cutoff = time.time() - CHAT_RESPONSE_STALENESS_SECONDS
        with self._lock:
            # Auto-expire stale chat_response lines
            self._conn.execute(
                "UPDATE ambient_lines SET used = 1 "
                "WHERE context = 'chat_response' AND used = 0 AND created_at < ?",
                (staleness_cutoff,),
            )
            self._conn.commit()
            
            if player_input:
                # Extract content words for matching
                words = set(player_input.lower().split())
                # Try topic-matched line first
                rows = self._conn.execute(
                    "SELECT id, text, topics FROM ambient_lines "
                    "WHERE context = 'chat_response' AND used = 0 "
                    "ORDER BY created_at DESC LIMIT 20",
                ).fetchall()
                best_row = None
                best_score = 0
                for row_id, text, topics in rows:
                    if topics:
                        topic_words = set(topics.lower().split(","))
                        overlap = len(words & topic_words)
                        if overlap > best_score:
                            best_score = overlap
                            best_row = (row_id, text)
                if best_row:
                    self._conn.execute(
                        "UPDATE ambient_lines SET used = 1 WHERE id = ?",
                        (best_row[0],),
                    )
                    self._conn.commit()
                    return best_row[1]

            # Fall back to any unused chat_response line
            row = self._conn.execute(
                "SELECT id, text FROM ambient_lines "
                "WHERE context = 'chat_response' AND used = 0 "
                "ORDER BY created_at ASC LIMIT 1",
            ).fetchone()
            if not row:
                return None
            self._conn.execute(
                "UPDATE ambient_lines SET used = 1 WHERE id = ?",
                (row[0],),
            )
            self._conn.commit()
            return row[1]

    def count_unused(self, context: str = None) -> int:
        """Count unused lines, optionally filtered by context."""
        if not self._conn:
            return 0
        with self._lock:
            if context:
                row = self._conn.execute(
                    "SELECT COUNT(*) FROM ambient_lines WHERE context = ? AND used = 0",
                    (context,),
                ).fetchone()
            else:
                row = self._conn.execute(
                    "SELECT COUNT(*) FROM ambient_lines WHERE used = 0"
                ).fetchone()
            return row[0] if row else 0

    # ── Generation request (fire-and-forget) ─────────────────────────

    def request_lines(self, trigger: str, player_input: str = "",
                      duck_response: str = "", context: Dict = None):
        """
        Request background generation of ambient lines.

        Non-blocking. Silently drops the request if:
        - LLM is not available
        - Worker is already busy
        - Cooldown has not elapsed
        - Too many consecutive failures
        """
        # Gate checks (fast, no locks)
        if not self._llm_chat or not self._llm_chat.is_available():
            return
        if self._busy:
            return
        # Back off after consecutive failures
        if self._consecutive_failures >= self._max_consecutive_failures:
            return
        now = time.time()
        if now - self._last_generation_time < self._cooldown:
            return

        self._last_generation_time = now
        self._busy = True

        # Build context for the prompt
        ctx = context or {}
        player_name = ctx.get("player_name", "")
        duck_mood = ctx.get("duck_mood", "content")
        location = ctx.get("location", "")
        weather = ctx.get("weather", "")
        personality = ctx.get("personality", {})  # Duck personality traits

        # Determine which context types to request
        context_types = self._pick_contexts(trigger)

        self._worker.submit(
            self._generate_worker,
            trigger, player_input, duck_response,
            player_name, duck_mood, location, weather,
            context_types, personality,
        )

    def _pick_contexts(self, trigger: str) -> List[str]:
        """Pick which context types to request based on trigger."""
        if trigger == "chat":
            return ["greeting", "idle", "callback", "chat_response"]
        elif trigger == "chat_enrich":
            return ["chat_response"]
        elif trigger in ("feed", "play", "pet", "clean"):
            return [trigger, "idle"]
        elif trigger == "login":
            return ["greeting", "idle"]
        elif trigger == "vocab":
            return ["idle", "callback"]
        elif trigger == "warmup":
            return ["greeting", "idle", "chat_response"]
        else:
            return ["idle"]

    # ── Background worker ─────────────────────────────────────────────

    def _generate_worker(self, trigger: str, player_input: str,
                         duck_response: str, player_name: str,
                         duck_mood: str, location: str, weather: str,
                         context_types: List[str], personality: Dict = None):
        """Run in background thread. Calls LLM and stores results."""
        try:
            prompt = self._build_prompt(
                trigger, player_input, duck_response,
                player_name, duck_mood, location, weather,
                context_types, personality or {},
            )

            response = self._call_llm(prompt)
            if not response:
                return

            lines = self._parse_response(response)
            if not lines:
                return

            # Content filter
            lines = self._filter_lines(lines)
            if lines:
                source = f"{trigger}:{player_input[:50]}" if player_input else trigger
                # Extract topic keywords from player input for chat_response matching
                topics = ""
                if player_input and any(ctx == "chat_response" for ctx, _ in lines):
                    topic_words = [w for w in player_input.lower().split() if len(w) > 3]
                    topics = ",".join(topic_words[:10])
                self._store_lines(lines, source, topics=topics)
                self._consecutive_failures = 0
                logger.debug(
                    "Ambient: stored %d lines from trigger '%s'",
                    len(lines), trigger,
                )
        except Exception as e:
            self._consecutive_failures += 1
            logger.debug("Ambient generation failed (%d): %s", self._consecutive_failures, e)
        finally:
            self._busy = False

    def _build_prompt(self, trigger: str, player_input: str,
                      duck_response: str, player_name: str,
                      duck_mood: str, location: str, weather: str,
                      context_types: List[str], personality: Dict = None) -> str:
        """Build a minimal system+user prompt for line generation."""
        name_clause = f"The player's name is {player_name}. " if player_name else ""
        location_clause = f"Location: {location}. " if location else ""
        weather_clause = f"Weather: {weather}. " if weather else ""
        
        # Build personality hint from traits
        personality_clause = ""
        if personality:
            traits = []
            for trait, val in personality.items():
                if val > 20:
                    traits.append(trait.split("_")[0])
                elif val < -20:
                    traits.append(trait.split("_")[-1])
            if traits:
                personality_clause = f"Personality leanings: {', '.join(traits)}. "

        context_desc = {
            "greeting": "when the player arrives to visit",
            "feed": "right after the player feeds Cheese",
            "play": "right after playing with the player",
            "pet": "right after being petted",
            "clean": "right after being cleaned",
            "idle": "random thoughts while hanging around",
            "callback": "referencing something from a past conversation",
            "chat_response": "a reply to what the player just said in conversation",
        }

        ctx_lines = "\n".join(
            f"- {c}: {context_desc.get(c, c)}"
            for c in context_types
        )

        trigger_desc = ""
        if player_input:
            trigger_desc = f'The player just said: "{player_input}"\n'
            if duck_response:
                trigger_desc += f'Cheese replied: "{duck_response}"\n'
        elif trigger in ("feed", "play", "pet", "clean"):
            trigger_desc = f"The player just {trigger}{'ed' if trigger != 'clean' else 'ed'} Cheese.\n"

        system = (
            "You are writing dialogue lines for Cheese, a male pet duck. "
            "Cheese has a deadpan, dry-witted personality. "
            "Rules: short sentences (1-2 max). Period-heavy. "
            "Use *emotes* like *blinks*, *tilts head*, *stares*. "
            "No exclamation marks for enthusiasm. Sardonic but not mean. "
            "Rare moments of quiet warmth buried under deadpan delivery."
        )

        user = (
            f"{name_clause}{location_clause}{weather_clause}{personality_clause}\n"
            f"Cheese's mood: {duck_mood}.\n"
            f"{trigger_desc}\n"
            f"Write 3-5 short dialogue lines Cheese might say LATER. "
            f"Each line must be tagged with a context type.\n"
            f"Contexts:\n{ctx_lines}\n\n"
            f"Format each line as:\ncontext: dialogue text\n\n"
            f"Example:\n"
            f"greeting: *blinks* Oh. You're back. I noticed.\n"
            f"idle: I was thinking about nothing. Successfully.\n"
            f"feed: Food received. Filing under 'reasons to continue'.\n"
        )

        return f"[SYSTEM]{system}\n\n[USER]{user}"

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Call the LLM with a lightweight prompt. Returns raw text or None."""
        llm = self._llm_chat
        if not llm or not llm._llama:
            return None

        # Acquire inference lock to prevent concurrent llama.cpp access
        lock = getattr(llm, '_inference_lock', None)
        if lock and not lock.acquire(timeout=30):
            logger.debug("Ambient: could not acquire inference lock")
            return None

        try:
            # Use chat completion for capable models, completion for others
            model_name = (llm._model_name or "").lower()
            is_capable = any(m in model_name for m in ["llama", "phi", "qwen", "mistral"])

            if is_capable:
                # Split our combined prompt into system/user messages
                parts = prompt.split("\n\n[USER]", 1)
                system_text = parts[0].replace("[SYSTEM]", "").strip()
                user_text = parts[1].strip() if len(parts) > 1 else prompt

                messages = [
                    {"role": "system", "content": system_text},
                    {"role": "user", "content": user_text},
                ]
                result = llm._llama.create_chat_completion(
                    messages=messages,
                    max_tokens=120,
                    temperature=0.6,
                    top_p=0.9,
                    repeat_penalty=1.15,
                    stop=["\n\n\n"],
                )
                if result and "choices" in result and result["choices"]:
                    return result["choices"][0].get("message", {}).get("content", "")
            else:
                result = llm._llama(
                    prompt,
                    max_tokens=120,
                    temperature=0.6,
                    top_p=0.9,
                    repeat_penalty=1.15,
                    stop=["\n\n\n"],
                )
                if result and "choices" in result and result["choices"]:
                    return result["choices"][0].get("text", "")

        except Exception as e:
            logger.debug("Ambient LLM call failed: %s", e)
        finally:
            if lock:
                lock.release()

        return None

    def _parse_response(self, raw: str) -> List[Tuple[str, str]]:
        """Parse tagged lines from LLM output."""
        lines = []
        for line in raw.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            m = _LINE_RE.match(line)
            if m:
                ctx = m.group("ctx").lower()
                text = m.group("text").strip()
                # Basic quality checks
                if len(text) < 5 or len(text) > 200:
                    continue
                if ctx in VALID_CONTEXTS:
                    lines.append((ctx, text))
        return lines

    def _filter_lines(self, lines: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Run content filter on parsed lines."""
        try:
            from dialogue.content_filter import get_content_filter
            cf = get_content_filter()
            return [(ctx, text) for ctx, text in lines if cf.is_safe_to_learn(text)]
        except Exception:
            return lines  # If filter unavailable, pass through

    # ── Lifecycle ─────────────────────────────────────────────────────

    def shutdown(self):
        """Clean shutdown of worker thread."""
        self._worker.shutdown(wait=False)
        if self._conn:
            try:
                self._conn.close()
            except Exception:
                pass

    @staticmethod
    def clear_all_lines():
        """Delete all ambient lines from the database (for new game reset)."""
        try:
            conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
            conn.execute("DELETE FROM ambient_lines")
            conn.commit()
            conn.close()
        except Exception:
            pass
