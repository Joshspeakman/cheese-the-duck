"""
Memory Recall — Relevance-based memory retrieval for Cheese the Duck.

Replaces random callback selection with contextual, scored retrieval.
When the player mentions a topic, Cheese can recall related past
conversations, quotes, facts, and behavioral patterns — making his
callbacks feel natural rather than random.

No new dependencies — pure Python on existing data structures.
"""
import random
import time
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
from collections import defaultdict

logger = logging.getLogger(__name__)

# Cooldown between contextual callbacks (seconds)
CALLBACK_COOLDOWN = 300  # 5 minutes

# How many recent callback IDs to track for staleness
MAX_RECENT_CALLBACKS = 20


class MemoryRecall:
    """
    Contextual memory retrieval that scores memories by relevance
    to the current conversation, rather than picking randomly.
    """

    def __init__(self, conversation_memory, player_model, duck_memory=None):
        self._conv_mem = conversation_memory
        self._player = player_model
        self._duck_mem = duck_memory

        # Track recently used callbacks to avoid repetition
        self._recent_callback_ids: List[str] = []
        self._last_callback_time = 0.0

    def find_relevant_memory(self, current_input: str,
                              current_topics: List[str] = None) -> Optional[Dict]:
        """
        Find the most relevant memory to the current conversation.

        Scores candidates by:
        1. Topic overlap with current input
        2. Keyword overlap (word intersection)
        3. Temporal relevance (prefer old-enough but not ancient)
        4. Emotional intensity (stronger emotions = more memorable)
        5. Staleness penalty (don't repeat recently used memories)

        Returns a callback dict with type, content, intro, and score.
        """
        now = time.time()
        if now - self._last_callback_time < CALLBACK_COOLDOWN:
            return None

        if not current_topics:
            current_topics = self._detect_topics(current_input)

        input_words = set(current_input.lower().split())
        candidates = []

        # Source 1: Notable quotes matching current topics
        candidates.extend(
            self._score_quotes(input_words, current_topics)
        )

        # Source 2: Player facts relevant to current input
        candidates.extend(
            self._score_facts(input_words, current_topics)
        )

        # Source 3: Topic frequency observations
        candidates.extend(
            self._score_topic_patterns(current_topics)
        )

        # Source 4: Unanswered questions relevant to current context
        candidates.extend(
            self._score_unanswered_questions(input_words)
        )

        # Source 5: Player statements with topic overlap
        candidates.extend(
            self._score_player_statements(input_words, current_topics)
        )

        # Source 6: Promise tracking
        candidates.extend(
            self._score_promises()
        )

        if not candidates:
            return None

        # Sort by score descending, pick best non-stale one
        candidates.sort(key=lambda c: c["score"], reverse=True)

        for candidate in candidates[:5]:  # Check top 5
            callback_id = f"{candidate['type']}:{candidate.get('content', '')[:50]}"
            if callback_id not in self._recent_callback_ids:
                # Mark as used
                self._recent_callback_ids.append(callback_id)
                if len(self._recent_callback_ids) > MAX_RECENT_CALLBACKS:
                    self._recent_callback_ids.pop(0)
                self._last_callback_time = now
                return candidate

        return None

    def get_contextual_callback(self, trigger_type: str,
                                 context: Dict = None) -> Optional[Dict]:
        """
        Get a callback for a specific trigger type.

        Trigger types:
        - topic_echo: Player mentioned a topic they discussed before
        - time_anniversary: It's been N weeks/months since a meaningful event
        - behavior_pattern: Player's behavior deviates from their pattern
        - broken_promise: Player promised something and didn't follow through
        - fact_callback: Current context relates to a stored player fact
        """
        context = context or {}

        if trigger_type == "topic_echo":
            return self._topic_echo_callback(context)
        elif trigger_type == "time_anniversary":
            return self._time_anniversary_callback()
        elif trigger_type == "behavior_pattern":
            return self._behavior_pattern_callback(context)
        elif trigger_type == "broken_promise":
            return self._broken_promise_callback()
        elif trigger_type == "fact_callback":
            return self._fact_callback(context)

        return None

    # ── Scoring methods ──────────────────────────────────────────────────

    def _score_quotes(self, input_words: set,
                       current_topics: List[str]) -> List[Dict]:
        """Score notable quotes by relevance to current input."""
        results = []

        for quote, conv_id, timestamp in self._conv_mem.notable_quotes[-50:]:
            quote_words = set(quote.lower().split())
            quote_topics = self._detect_topics(quote)

            # Word overlap score
            overlap = len(input_words & quote_words)
            word_score = min(1.0, overlap / max(len(input_words), 1) * 2)

            # Topic overlap score
            topic_overlap = len(set(current_topics) & set(quote_topics))
            topic_score = min(1.0, topic_overlap / max(len(current_topics), 1))

            # Age score: prefer quotes that are old enough to be a callback
            # but not so old they're irrelevant
            age_score = self._age_score(timestamp)

            total = word_score * 0.4 + topic_score * 0.4 + age_score * 0.2

            if total > 0.2:
                intro = self._format_quote_intro(quote)
                results.append({
                    "type": "quote",
                    "content": quote,
                    "intro": intro,
                    "score": total,
                    "source": "quote_recall",
                })

        return results

    def _score_facts(self, input_words: set,
                      current_topics: List[str]) -> List[Dict]:
        """Score player facts by relevance."""
        results = []
        if not self._player:
            return results

        fact_topic_map = {
            "has_pet": {"personal", "feelings"},
            "discussed_work": {"personal"},
            "discussed_family": {"personal", "feelings"},
            "discussed_hobbies": {"personal", "games"},
            "emotional_statement": {"feelings"},
        }

        for fact_type, fact in self._player.facts.items():
            related_topics = fact_topic_map.get(fact_type, set())
            topic_overlap = len(set(current_topics) & related_topics)
            score = topic_overlap * 0.3

            # Keyword bonus
            fact_words = set(str(fact.value).lower().split())
            word_overlap = len(input_words & fact_words)
            score += min(0.4, word_overlap * 0.15)

            # Confidence bonus
            score += fact.confidence * 0.1

            if score > 0.2:
                intro = self._format_fact_intro(fact_type, fact.value)
                if intro:
                    results.append({
                        "type": "fact",
                        "content": f"{fact_type}: {fact.value}",
                        "intro": intro,
                        "score": score,
                        "source": "fact_callback",
                    })

        return results

    def _score_topic_patterns(self, current_topics: List[str]) -> List[Dict]:
        """Score topic frequency patterns."""
        results = []

        for topic in current_topics:
            count = self._conv_mem.topic_counts.get(topic, 0)
            if count >= 3:
                # More mentions = higher score, but capped
                score = min(0.8, 0.3 + count * 0.05)
                intros = [
                    f"we've talked about {topic} a suspicious number of times.",
                    f"*tilts head* {topic} again. you have patterns. I NOTICE patterns.",
                    f"ah. {topic}. your favorite recurring theme.",
                    f"you and {topic}. at this point it's a whole saga.",
                    f"every time you mention {topic} I add a mental tally mark. we're in double digits.",
                    f"*adjusts feathers* so. {topic}. we meet again.",
                ]
                results.append({
                    "type": "topic_pattern",
                    "content": topic,
                    "intro": random.choice(intros),
                    "score": score,
                    "source": "topic_recall",
                })

        return results

    def _score_unanswered_questions(self, input_words: set) -> List[Dict]:
        """Score unanswered questions by relevance."""
        results = []

        for question, timestamp in self._conv_mem.unanswered_questions[-10:]:
            question_words = set(question.lower().split())
            overlap = len(input_words & question_words)
            score = min(0.8, overlap / max(len(question_words), 1))

            # Age bonus for old unanswered questions (more guilt)
            age_score = self._age_score(timestamp, ideal_age_days=7)
            score = score * 0.6 + age_score * 0.4

            if score > 0.15:
                intros = [
                    f"you asked me \"{question}\" and I never answered. it's been bothering me.",
                    f"*suddenly* wait. you once asked \"{question}\" and I just... didn't respond.",
                    f"I ghosted your question about \"{question}.\" not on purpose. probably.",
                    f"you asked \"{question}\" once. I'm circling back. ducks are thorough.",
                ]
                results.append({
                    "type": "unanswered",
                    "content": question,
                    "intro": random.choice(intros),
                    "score": score,
                    "source": "unanswered_question",
                })

        return results

    def _score_player_statements(self, input_words: set,
                                   current_topics: List[str]) -> List[Dict]:
        """Score player statements by topic and keyword relevance."""
        results = []
        if not self._player:
            return results

        for stmt in self._player.statements[-50:]:
            stmt_words = set(stmt.text.lower().split())
            stmt_topics = stmt.topic_tags or []

            # Word overlap
            word_overlap = len(input_words & stmt_words)
            word_score = min(1.0, word_overlap / max(len(input_words), 1) * 2)

            # Topic overlap
            topic_overlap = len(set(current_topics) & set(stmt_topics))
            topic_score = min(1.0, topic_overlap / max(len(current_topics), 1))

            # Staleness: prefer unreferenced statements
            stale_bonus = 0.1 if stmt.times_referenced == 0 else 0.0

            # Emotional intensity bonus
            emotion_score = abs(stmt.sentiment) * 0.15

            total = (word_score * 0.35 + topic_score * 0.35
                     + stale_bonus + emotion_score)

            if total > 0.3:
                truncated = stmt.text[:80]
                if len(stmt.text) > 80:
                    truncated += "..."
                intro = self._format_statement_intro(truncated)
                results.append({
                    "type": "statement",
                    "content": stmt.text,
                    "intro": intro,
                    "score": total,
                    "source": "quote_recall",
                    "statement": stmt,
                })

        return results

    def _score_promises(self) -> List[Dict]:
        """Score unfulfilled promises."""
        results = []
        if not self._player:
            return results

        for promise in self._player.promises_made[-10:]:
            if promise.get("fulfilled"):
                continue

            age_days = 0
            if promise.get("made_at"):
                try:
                    made = datetime.fromisoformat(promise["made_at"])
                    age_days = (datetime.now() - made).days
                except (ValueError, TypeError):
                    pass

            # Older broken promises score higher (more guilt)
            score = min(0.9, 0.3 + age_days * 0.05)

            text = promise.get("text", "something")
            intros = [
                f"you said you'd {text}. I remember. ducks remember EVERYTHING.",
                f"*stares* so about when you promised to {text}...",
                f"I'm not bringing up that you said you'd {text}. except I just did.",
                f"just checking. you mentioned you'd {text}. no pressure. except all the pressure.",
            ]
            results.append({
                "type": "promise",
                "content": text,
                "intro": random.choice(intros),
                "score": score,
                "source": "pattern_observation",
            })

        return results

    # ── Trigger-based callbacks ──────────────────────────────────────────

    def _topic_echo_callback(self, context: Dict) -> Optional[Dict]:
        """Generate callback when player revisits a previously discussed topic."""
        topic = context.get("topic", "")
        if not topic:
            return None

        # Find a past quote on this topic
        for quote, conv_id, ts in reversed(self._conv_mem.notable_quotes[-50:]):
            quote_topics = self._detect_topics(quote)
            if topic in quote_topics:
                truncated = quote[:80] + ("..." if len(quote) > 80 else "")
                intros = [
                    f"you told me once that \"{truncated}.\" I've been thinking about it. not jealously.",
                    f"this reminds me. you said \"{truncated}\" before. my brain flagged it.",
                    f"*blinks* didn't you say something like \"{truncated}\"? I have a mental file.",
                ]
                return {
                    "type": "topic_echo",
                    "content": quote,
                    "intro": random.choice(intros),
                    "score": 0.7,
                    "source": "quote_recall",
                }

        return None

    def _time_anniversary_callback(self) -> Optional[Dict]:
        """Generate callback for time-based milestones."""
        if not self._conv_mem.conversations:
            return None

        now = datetime.now()

        # Check for weekly/monthly anniversaries of meaningful conversations
        for conv in reversed(self._conv_mem.conversations[-30:]):
            if not conv.was_meaningful:
                continue

            try:
                conv_date = datetime.fromisoformat(conv.started_at)
            except (ValueError, TypeError):
                continue

            days_ago = (now - conv_date).days
            topics = ", ".join(conv.topics[:2]) if conv.topics else "things"

            # One-week anniversary
            if 6 <= days_ago <= 8:
                return {
                    "type": "anniversary",
                    "content": f"week since {topics}",
                    "intro": f"it was about a week ago we talked about {topics}. time moves. I don't.",
                    "score": 0.5,
                    "source": "milestone_recall",
                }

            # One-month anniversary
            if 28 <= days_ago <= 32:
                return {
                    "type": "anniversary",
                    "content": f"month since {topics}",
                    "intro": f"it was about a month ago we talked about {topics}. I've been counting. silently.",
                    "score": 0.6,
                    "source": "milestone_recall",
                }

        return None

    def _behavior_pattern_callback(self, context: Dict) -> Optional[Dict]:
        """Generate callback when player deviates from their pattern."""
        deviation = context.get("deviation", "")
        if not deviation:
            return None

        intros = [
            f"you usually {deviation}. I'm not worried. I'm NOTING.",
            f"*squints* something's different. you normally {deviation}.",
            f"interesting. you {deviation} but not today. I have questions. I'll keep them to myself.",
            f"my internal clock says you should be doing something else right now. {deviation}. but who am I to judge.",
        ]
        return {
            "type": "behavior",
            "content": deviation,
            "intro": random.choice(intros),
            "score": 0.6,
            "source": "pattern_observation",
        }

    def _broken_promise_callback(self) -> Optional[Dict]:
        """Surface an unfulfilled promise."""
        if not self._player:
            return None

        for promise in self._player.promises_made[-10:]:
            if not promise.get("fulfilled"):
                text = promise.get("text", "something")
                intros = [
                    f"so. about that time you said you'd {text}. I'm not mad. I'm DOCUMENTING.",
                    f"I keep a ledger. you promised to {text}. the ledger remembers.",
                    f"you said you'd {text}. I didn't forget. I CHOSE to bring it up now.",
                ]
                return {
                    "type": "promise",
                    "content": text,
                    "intro": random.choice(intros),
                    "score": 0.7,
                    "source": "pattern_observation",
                }

        return None

    def _fact_callback(self, context: Dict) -> Optional[Dict]:
        """Generate callback based on a stored player fact."""
        if not self._player:
            return None

        fact_type = context.get("fact_type", "")
        if fact_type and fact_type in self._player.facts:
            fact = self._player.facts[fact_type]
            intro = self._format_fact_intro(fact_type, fact.value)
            if intro:
                return {
                    "type": "fact",
                    "content": f"{fact_type}: {fact.value}",
                    "intro": intro,
                    "score": 0.6,
                    "source": "fact_callback",
                }

        # Try to find any relevant fact
        for fact_type, fact in self._player.facts.items():
            intro = self._format_fact_intro(fact_type, fact.value)
            if intro:
                return {
                    "type": "fact",
                    "content": f"{fact_type}: {fact.value}",
                    "intro": intro,
                    "score": 0.4,
                    "source": "fact_callback",
                }

        return None

    # ── Helpers ──────────────────────────────────────────────────────────

    def _detect_topics(self, text: str) -> List[str]:
        """Lightweight topic detection (mirrors ConversationMemory._detect_topics)."""
        text_lower = text.lower()
        topics = []

        topic_keywords = {
            "food": ["food", "eat", "hungry", "bread", "feed", "meal", "snack"],
            "weather": ["weather", "rain", "sun", "snow", "cold", "hot", "storm"],
            "feelings": ["feel", "sad", "happy", "angry", "love", "hate", "scared"],
            "personal": ["my life", "my job", "my family", "my friend", "i work"],
            "games": ["play", "game", "fun", "boring"],
            "philosophy": ["meaning", "life", "death", "purpose", "existence"],
            "dreams": ["dream", "hope", "wish", "someday"],
            "past": ["remember", "used to", "when i was", "back then"],
        }

        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)

        return topics or ["random"]

    def _age_score(self, timestamp: str, ideal_age_days: int = 14) -> float:
        """
        Score a memory by age. Peaks at ideal_age_days,
        falls off for very recent or very old memories.
        """
        try:
            mem_date = datetime.fromisoformat(timestamp)
            age_days = (datetime.now() - mem_date).days
        except (ValueError, TypeError):
            return 0.3  # Unknown age gets neutral score

        if age_days < 1:
            return 0.1  # Too recent to be a "callback"
        elif age_days <= ideal_age_days:
            return 0.5 + (age_days / ideal_age_days) * 0.5
        elif age_days <= ideal_age_days * 4:
            return 1.0 - ((age_days - ideal_age_days) / (ideal_age_days * 3)) * 0.5
        else:
            return 0.3  # Very old but still viable

    def _format_quote_intro(self, quote: str) -> str:
        """Format a quote recall intro in Cheese's voice."""
        truncated = quote[:80] + ("..." if len(quote) > 80 else "")
        intros = [
            f"you said \"{truncated}\" once. I wrote it down. in my brain.",
            f"*stares* ...you told me \"{truncated}.\" I remember everything.",
            f"I keep a mental file. under Q for quotes. you said \"{truncated}.\"",
            f"you probably forgot you said \"{truncated}.\" I did not.",
            f"I was thinking about when you said \"{truncated}.\" just now. no reason.",
            f"*taps beak* \"{truncated}.\" your words. not mine.",
            f"my brain filed this under 'important': \"{truncated}.\" take that as you will.",
            f"somewhere in our history you stated \"{truncated}.\" for the record.",
        ]
        return random.choice(intros)

    def _format_statement_intro(self, text: str) -> str:
        """Format a player statement recall intro."""
        intros = [
            f"you once told me: \"{text}\"",
            f"I remember you saying: \"{text}\"",
            f"you said something that stuck with me: \"{text}\"",
            f"I've been thinking about when you said: \"{text}\"",
            f"my memory is good. you said: \"{text}\"",
            f"this has been in my head since you told me: \"{text}\"",
        ]
        return random.choice(intros)

    def _format_fact_intro(self, fact_type: str, value: Any) -> Optional[str]:
        """Format a fact callback in Cheese's voice."""
        templates = {
            "has_pet": [
                f"you have a {value}. how are they. I'm asking for ME, not for them.",
                f"your {value}. I think about them sometimes. is that weird. it's weird.",
                f"*tilts head* how's the {value} situation. I'm collecting data.",
            ],
            "player_name": [
                f"I know your name is {value}. I remember names. it's a curse.",
            ],
            "discussed_work": [
                "you mentioned work before. how's that going. I'm asking out of obligation. and curiosity.",
                "work. you talked about it once. I listened. ducks are excellent listeners. mostly because we can't interrupt.",
            ],
            "discussed_family": [
                "you mentioned your family once. they doing okay? I'm asking because I'm nosy. and slightly invested.",
                "family. you brought them up. I stored it. ducks have good memory. and opinions about everything.",
            ],
            "discussed_hobbies": [
                "your hobbies. I remember you talking about them. I was judging. I mean listening.",
                "so those hobbies you mentioned. still doing them? I'm tracking your character arc.",
            ],
            "age": [
                f"you said you're {value}. I filed that. age is just a number. but I filed it anyway.",
                f"{value}. that's how old you are. I remembered. you're welcome.",
            ],
            "occupation": [
                f"you work as {value}. how's that going. I'm curious. for research purposes.",
                f"so you're a {value}. I think about that sometimes. when I'm floating.",
            ],
            "location": [
                f"you live in {value}. I've never been. obviously. I'm a duck. in a pond.",
                f"{value}. that's where you are when you're not here. I have opinions about that. I'll keep them to myself.",
            ],
        }

        options = templates.get(fact_type)
        if options:
            return random.choice(options)
        return None
