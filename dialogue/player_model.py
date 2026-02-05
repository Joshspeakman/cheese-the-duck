"""
Player Model - What the duck learns about and remembers about the player.

Tracks player preferences, habits, statements, personality traits inferred from behavior,
and builds a comprehensive psychological profile that the duck uses to generate
contextually aware, sometimes unsettlingly perceptive observations.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import json
import random


class PlayerTraitAxis(Enum):
    """Inferred player personality axes based on behavior patterns."""
    ATTENTIVE_NEGLECTFUL = "attentive_neglectful"      # How often they check on duck
    PATIENT_IMPATIENT = "patient_impatient"            # How long they wait for responses
    GENEROUS_STINGY = "generous_stingy"                # Gift/feeding frequency
    TALKATIVE_QUIET = "talkative_quiet"                # Chat frequency
    CONSISTENT_CHAOTIC = "consistent_chaotic"          # Visit time patterns
    PLAYFUL_SERIOUS = "playful_serious"                # Play vs other interactions
    CURIOUS_ROUTINE = "curious_routine"                # Exploration/variety in actions
    NIGHT_OWL_EARLY_BIRD = "night_owl_early_bird"      # When they typically visit


@dataclass
class PlayerStatement:
    """Something the player said that the duck should remember."""
    text: str
    timestamp: str
    context: str  # What prompted this (question asked, topic discussed)
    topic_tags: List[str] = field(default_factory=list)
    sentiment: float = 0.0  # -1.0 to 1.0
    importance: float = 0.5  # 0.0 to 1.0
    times_referenced: int = 0
    last_referenced: Optional[str] = None


@dataclass
class PlayerFact:
    """A concrete fact learned about the player."""
    fact_type: str  # name, favorite_x, dislikes_x, has_pet, job, etc.
    value: Any
    confidence: float  # 0.0 to 1.0 - how sure we are
    source: str  # How we learned this (player_stated, inferred, asked)
    learned_at: str
    times_confirmed: int = 0
    contradicted: bool = False


@dataclass
class VisitPattern:
    """Tracks when the player typically visits."""
    hour_counts: Dict[int, int] = field(default_factory=lambda: defaultdict(int))
    day_counts: Dict[int, int] = field(default_factory=lambda: defaultdict(int))  # 0=Mon
    session_durations: List[float] = field(default_factory=list)  # Minutes
    gaps_between_visits: List[float] = field(default_factory=list)  # Hours
    last_visit: Optional[str] = None
    total_visits: int = 0
    longest_absence: float = 0.0  # Hours
    current_streak: int = 0  # Consecutive days
    best_streak: int = 0


@dataclass
class BehaviorPattern:
    """Patterns in how the player interacts."""
    action_sequences: List[List[str]] = field(default_factory=list)  # Common action orders
    favorite_actions: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    action_by_mood: Dict[str, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    action_by_time: Dict[int, Dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    avg_actions_per_session: float = 0.0
    rushed_sessions: int = 0  # Quick in-and-out
    leisurely_sessions: int = 0  # Long, varied


class PlayerModel:
    """
    Comprehensive model of the player built from observations and conversations.
    
    The duck uses this to:
    - Remember what the player told them
    - Notice behavioral patterns
    - Make eerily accurate observations
    - Ask follow-up questions about past topics
    - Reference shared history in deadpan ways
    """
    
    # Memory limits to prevent unbounded growth
    MAX_STATEMENTS = 200  # Keep last 200 player statements
    MAX_QUESTIONS_ASKED = 100  # Keep last 100 questions
    MAX_QUESTIONS_PENDING = 20  # Max pending questions
    MAX_SESSION_DURATIONS = 100  # Keep last 100 session durations
    MAX_VISIT_GAPS = 100  # Keep last 100 visit gaps
    MAX_ACTION_SEQUENCES = 100  # Keep last 100 action sequences
    MAX_PROMISES = 50  # Keep last 50 promises
    MAX_OBSERVATIONS = 20  # Max pending observations
    MAX_STATEMENT_INDEX_PER_TOPIC = 50  # Max statements per topic index
    
    def __init__(self):
        # Core identity
        self.name: Optional[str] = None
        self.nickname: Optional[str] = None  # What duck calls them
        self.first_met: Optional[str] = None
        
        # Facts learned about player
        self.facts: Dict[str, PlayerFact] = {}
        
        # Things player has said
        self.statements: List[PlayerStatement] = []
        self.statement_topics: Dict[str, List[int]] = defaultdict(list)  # topic -> statement indices
        
        # Questions asked and answered
        self.questions_asked: List[Dict] = []  # {question, asked_at, answered, answer}
        self.questions_pending: List[str] = []  # Questions to ask next opportunity
        self.question_cooldown: Dict[str, str] = {}  # topic -> last asked timestamp
        
        # Behavioral patterns
        self.visit_pattern = VisitPattern()
        self.behavior_pattern = BehaviorPattern()
        
        # Inferred personality traits (-100 to +100)
        self.inferred_traits: Dict[str, float] = {
            axis.value: 0.0 for axis in PlayerTraitAxis
        }
        self.trait_confidence: Dict[str, float] = {
            axis.value: 0.0 for axis in PlayerTraitAxis
        }
        
        # Relationship dynamics
        self.trust_level: float = 0.0  # -100 to 100
        self.annoyance_level: float = 0.0  # How annoyed duck is with player
        self.affection_level: float = 0.0  # Genuine warmth (rare)
        self.respect_level: float = 0.0  # Does duck respect player
        
        # Topics of conversation
        self.topics_discussed: Dict[str, int] = defaultdict(int)  # topic -> count
        self.topic_sentiment: Dict[str, float] = defaultdict(float)  # topic -> avg sentiment
        self.favorite_topics: List[str] = []
        self.avoided_topics: List[str] = []
        
        # Promises and commitments
        self.promises_made: List[Dict] = []  # Things player said they'd do
        self.promises_kept: int = 0
        self.promises_broken: int = 0
        
        # Session tracking
        self._current_session_start: Optional[str] = None
        self._current_session_actions: List[str] = []
        self._last_action_time: Optional[str] = None
        
        # Observations queue (things to comment on)
        self._pending_observations: List[Tuple[str, float]] = []  # (observation, priority)

    def start_session(self):
        """Called when player starts playing."""
        now = datetime.now()
        now_str = now.isoformat()
        
        self._current_session_start = now_str
        self._current_session_actions = []
        
        # Update visit patterns
        self.visit_pattern.hour_counts[now.hour] += 1
        self.visit_pattern.day_counts[now.weekday()] += 1
        self.visit_pattern.total_visits += 1
        
        # Calculate gap since last visit
        if self.visit_pattern.last_visit:
            try:
                last = datetime.fromisoformat(self.visit_pattern.last_visit)
                gap_hours = (now - last).total_seconds() / 3600
                self.visit_pattern.gaps_between_visits.append(gap_hours)
                
                # Track longest absence
                if gap_hours > self.visit_pattern.longest_absence:
                    self.visit_pattern.longest_absence = gap_hours
                
                # Track streak
                if gap_hours < 36:  # Visited within ~1.5 days
                    self.visit_pattern.current_streak += 1
                    if self.visit_pattern.current_streak > self.visit_pattern.best_streak:
                        self.visit_pattern.best_streak = self.visit_pattern.current_streak
                else:
                    self.visit_pattern.current_streak = 1
                    
            except (ValueError, TypeError):
                pass
        
        self.visit_pattern.last_visit = now_str
        
        # Queue observations about visit patterns
        self._generate_visit_observations(now)
    
    def end_session(self):
        """Called when player stops playing."""
        if not self._current_session_start:
            return
        
        try:
            start = datetime.fromisoformat(self._current_session_start)
            duration = (datetime.now() - start).total_seconds() / 60  # Minutes
            self.visit_pattern.session_durations.append(duration)
            
            # Categorize session
            action_count = len(self._current_session_actions)
            if duration < 2 and action_count < 3:
                self.behavior_pattern.rushed_sessions += 1
                self._adjust_trait(PlayerTraitAxis.PATIENT_IMPATIENT, -5)
            elif duration > 15 and action_count > 10:
                self.behavior_pattern.leisurely_sessions += 1
                self._adjust_trait(PlayerTraitAxis.PATIENT_IMPATIENT, 5)
            
            # Update avg actions per session
            total_sessions = len(self.visit_pattern.session_durations)
            if total_sessions > 0:
                total_actions = sum(len(seq) for seq in self.behavior_pattern.action_sequences[-50:])
                self.behavior_pattern.avg_actions_per_session = total_actions / min(50, total_sessions)
            
            # Store action sequence
            if self._current_session_actions:
                self.behavior_pattern.action_sequences.append(self._current_session_actions.copy())
                # Keep last 100 sequences
                if len(self.behavior_pattern.action_sequences) > 100:
                    self.behavior_pattern.action_sequences = self.behavior_pattern.action_sequences[-100:]
                    
        except (ValueError, TypeError):
            pass
        
        self._current_session_start = None
        self._current_session_actions = []
        
        # Enforce memory limits periodically
        self._enforce_memory_limits()
    
    def record_action(self, action: str, duck_mood: Optional[str] = None):
        """Record a player action for pattern analysis."""
        now = datetime.now()
        
        self._current_session_actions.append(action)
        self._last_action_time = now.isoformat()
        
        # Update action counts
        self.behavior_pattern.favorite_actions[action] += 1
        self.behavior_pattern.action_by_time[now.hour][action] += 1
        
        if duck_mood:
            self.behavior_pattern.action_by_mood[duck_mood][action] += 1
        
        # Infer traits from actions
        self._infer_traits_from_action(action)
    
    def record_statement(self, text: str, context: str = "", 
                         topic_tags: List[str] = None,
                         sentiment: float = 0.0,
                         importance: float = 0.5):
        """Record something the player said."""
        statement = PlayerStatement(
            text=text,
            timestamp=datetime.now().isoformat(),
            context=context,
            topic_tags=topic_tags or [],
            sentiment=sentiment,
            importance=importance
        )
        
        idx = len(self.statements)
        self.statements.append(statement)
        
        # Index by topic
        for tag in statement.topic_tags:
            self.statement_topics[tag].append(idx)
            self.topics_discussed[tag] += 1
            
            # Update topic sentiment (rolling average)
            prev = self.topic_sentiment[tag]
            count = self.topics_discussed[tag]
            self.topic_sentiment[tag] = (prev * (count - 1) + sentiment) / count
        
        # Update personality inference from talkative trait
        self._adjust_trait(PlayerTraitAxis.TALKATIVE_QUIET, 3)
        
        # Try to extract facts from statement
        self._extract_facts_from_statement(statement)
    
    def record_fact(self, fact_type: str, value: Any, 
                    confidence: float = 0.8,
                    source: str = "player_stated"):
        """Record a learned fact about the player."""
        existing = self.facts.get(fact_type)
        
        if existing:
            if existing.value == value:
                existing.times_confirmed += 1
                existing.confidence = min(1.0, existing.confidence + 0.1)
            else:
                # Contradicting information
                if confidence > existing.confidence:
                    existing.value = value
                    existing.confidence = confidence
                    existing.contradicted = True
                    existing.source = source
        else:
            self.facts[fact_type] = PlayerFact(
                fact_type=fact_type,
                value=value,
                confidence=confidence,
                source=source,
                learned_at=datetime.now().isoformat()
            )
        
        # Special handling for name
        if fact_type == "name" and not self.name:
            self.name = value
    
    def record_question_asked(self, question: str, topic: str = "general"):
        """Record that the duck asked the player a question."""
        self.questions_asked.append({
            "question": question,
            "topic": topic,
            "asked_at": datetime.now().isoformat(),
            "answered": False,
            "answer": None
        })
        self.question_cooldown[topic] = datetime.now().isoformat()
    
    def record_question_answered(self, answer: str):
        """Record the player's answer to the most recent question."""
        if self.questions_asked:
            last_q = self.questions_asked[-1]
            if not last_q["answered"]:
                last_q["answered"] = True
                last_q["answer"] = answer
                last_q["answered_at"] = datetime.now().isoformat()
    
    def add_pending_question(self, question: str, priority: float = 0.5):
        """Queue a question to ask the player later."""
        if question not in self.questions_pending:
            self.questions_pending.append(question)
    
    def get_next_question(self, topic_cooldown_hours: float = 24.0) -> Optional[str]:
        """Get the next question to ask, respecting cooldowns."""
        if not self.questions_pending:
            return None
        
        now = datetime.now()
        
        for q in self.questions_pending[:]:
            # Simple cooldown check (could be more sophisticated)
            can_ask = True
            for topic, last_asked in self.question_cooldown.items():
                if topic.lower() in q.lower():
                    try:
                        last = datetime.fromisoformat(last_asked)
                        if (now - last).total_seconds() < topic_cooldown_hours * 3600:
                            can_ask = False
                            break
                    except (ValueError, TypeError):
                        pass
            
            if can_ask:
                self.questions_pending.remove(q)
                return q
        
        return None
    
    def get_relevant_facts(self, context: str = "", max_facts: int = 10) -> List[PlayerFact]:
        """Get facts relevant to the current context."""
        facts = list(self.facts.values())
        
        if context:
            context_lower = context.lower()
            # Score by relevance
            scored = []
            for fact in facts:
                score = fact.confidence
                if fact.fact_type.lower() in context_lower:
                    score += 0.5
                if str(fact.value).lower() in context_lower:
                    score += 0.3
                scored.append((score, fact))
            scored.sort(key=lambda x: x[0], reverse=True)
            return [f for _, f in scored[:max_facts]]
        
        # Return highest confidence facts
        facts.sort(key=lambda f: (f.confidence, f.times_confirmed), reverse=True)
        return facts[:max_facts]
    
    def get_relevant_statements(self, topic: str = "", max_statements: int = 5) -> List[PlayerStatement]:
        """Get player statements relevant to a topic."""
        if topic and topic in self.statement_topics:
            indices = self.statement_topics[topic][-max_statements:]
            return [self.statements[i] for i in indices if i < len(self.statements)]
        
        # Return most important/recent statements
        sorted_statements = sorted(
            self.statements,
            key=lambda s: (s.importance, s.timestamp),
            reverse=True
        )
        return sorted_statements[:max_statements]
    
    def get_unreferenced_statements(self, max_age_days: int = 30) -> List[PlayerStatement]:
        """Get statements the duck hasn't brought up recently."""
        now = datetime.now()
        cutoff = now - timedelta(days=max_age_days)
        
        unreferenced = []
        for stmt in self.statements:
            try:
                stmt_time = datetime.fromisoformat(stmt.timestamp)
                if stmt_time < cutoff:
                    continue
            except (ValueError, TypeError):
                continue
            
            if stmt.times_referenced == 0 or (
                stmt.last_referenced and 
                (now - datetime.fromisoformat(stmt.last_referenced)).days > 7
            ):
                unreferenced.append(stmt)
        
        return unreferenced
    
    def mark_statement_referenced(self, statement: PlayerStatement):
        """Mark that we referenced a statement in dialogue."""
        statement.times_referenced += 1
        statement.last_referenced = datetime.now().isoformat()
    
    def get_behavioral_observations(self) -> List[str]:
        """Generate observations about player behavior patterns."""
        observations = []
        
        # Visit time patterns
        if self.visit_pattern.hour_counts:
            peak_hour = max(self.visit_pattern.hour_counts.items(), key=lambda x: x[1])[0]
            if peak_hour >= 0 and peak_hour < 6:
                observations.append(f"You seem to prefer visiting in the dead of night. Specifically around {peak_hour}:00. Is everything... okay?")
            elif peak_hour >= 22:
                observations.append(f"A creature of the night, I see. You do realize I have a bedtime? Not that you asked.")
            elif peak_hour >= 5 and peak_hour < 8:
                observations.append("An early riser. How aggressively optimistic of you.")
        
        # Session duration patterns
        if self.behavior_pattern.rushed_sessions > 5:
            ratio = self.behavior_pattern.rushed_sessions / max(1, self.visit_pattern.total_visits)
            if ratio > 0.5:
                observations.append("I've noticed you tend to pop in, poke around, and leave. Places to be? Things more important than me? No, don't answer that.")
        
        # Favorite actions
        if self.behavior_pattern.favorite_actions:
            top_action = max(self.behavior_pattern.favorite_actions.items(), key=lambda x: x[1])
            if top_action[1] > 20:
                action_names = {
                    "feed": "feeding me",
                    "play": "playing",
                    "clean": "cleaning",
                    "pet": "petting",
                    "talk": "talking to me"
                }
                name = action_names.get(top_action[0], top_action[0])
                observations.append(f"You really do love {name}, don't you? {top_action[1]} times now. I'm keeping count. Clearly.")
        
        # Streak observations
        if self.visit_pattern.current_streak >= 7:
            observations.append(f"You've visited {self.visit_pattern.current_streak} days in a row. That's either dedication or... something else. I choose not to speculate.")
        
        # Longest absence
        if self.visit_pattern.longest_absence > 72:
            days = int(self.visit_pattern.longest_absence / 24)
            observations.append(f"You were gone for {days} days once. Not that I was counting. I wasn't waiting by the pond or anything.")
        
        return observations
    
    def get_trait_description(self, trait: PlayerTraitAxis) -> Optional[str]:
        """Get a deadpan description of an inferred trait."""
        value = self.inferred_traits.get(trait.value, 0)
        confidence = self.trait_confidence.get(trait.value, 0)
        
        if confidence < 0.3:
            return None
        
        descriptions = {
            PlayerTraitAxis.ATTENTIVE_NEGLECTFUL: {
                50: "You're quite attentive. Almost suspiciously so.",
                -50: "You have a talent for... not being here."
            },
            PlayerTraitAxis.PATIENT_IMPATIENT: {
                50: "Patient. I appreciate that. Most creatures just mash buttons.",
                -50: "Always in such a rush. The pond will still be here, you know."
            },
            PlayerTraitAxis.GENEROUS_STINGY: {
                50: "You're generous. With bread, at least. I'll take it.",
                -50: "You're not exactly known for your generosity, are you?"
            },
            PlayerTraitAxis.TALKATIVE_QUIET: {
                50: "You do like to chat. I'm mostly listening. Mostly.",
                -50: "The strong, silent type. How very... silent of you."
            },
            PlayerTraitAxis.PLAYFUL_SERIOUS: {
                50: "Always wanting to play. You're like a large, slightly concerning puppy.",
                -50: "All business with you, isn't it? Not much for fun."
            },
            PlayerTraitAxis.NIGHT_OWL_EARLY_BIRD: {
                50: "An early bird. You probably eat worms. I'm not judging. Much.",
                -50: "A night owl. We have that in common. Sort of. I'm a duck."
            }
        }
        
        if trait in descriptions:
            if value > 40:
                return descriptions[trait].get(50)
            elif value < -40:
                return descriptions[trait].get(-50)
        
        return None
    
    def get_pending_observation(self) -> Optional[str]:
        """Get the next observation to share with the player."""
        if not self._pending_observations:
            return None
        
        # Sort by priority and return highest
        self._pending_observations.sort(key=lambda x: x[1], reverse=True)
        obs, _ = self._pending_observations.pop(0)
        return obs
    
    def _generate_visit_observations(self, now: datetime):
        """Generate observations about this visit."""
        # Long absence
        if self.visit_pattern.gaps_between_visits:
            last_gap = self.visit_pattern.gaps_between_visits[-1]
            if last_gap > 48:
                days = int(last_gap / 24)
                obs = [
                    f"Oh. You're back. After {days} days. I wasn't worried. Ducks don't worry.",
                    f"{days} days. I had started to think you'd found a better duck. Have you?",
                    f"It's been {days} days. The pond was very quiet. I talked to a frog. It wasn't the same.",
                ]
                self._pending_observations.append((random.choice(obs), 0.9))
            elif last_gap > 24:
                self._pending_observations.append((
                    "You were gone a while. Not that I track these things. But I do.",
                    0.5
                ))
        
        # Unusual time
        peak_hour = max(self.visit_pattern.hour_counts.items(), key=lambda x: x[1], default=(12, 0))[0]
        if abs(now.hour - peak_hour) > 6:
            obs = [
                f"You're here at {now.hour}:00? That's not your usual time. Everything alright?",
                "This is... an unusual hour for you. I notice these things.",
            ]
            self._pending_observations.append((random.choice(obs), 0.4))
    
    def _adjust_trait(self, trait: PlayerTraitAxis, delta: float):
        """Adjust an inferred trait value."""
        current = self.inferred_traits.get(trait.value, 0)
        self.inferred_traits[trait.value] = max(-100, min(100, current + delta))
        
        # Increase confidence
        confidence = self.trait_confidence.get(trait.value, 0)
        self.trait_confidence[trait.value] = min(1.0, confidence + 0.02)
    
    def _infer_traits_from_action(self, action: str):
        """Update trait inferences based on an action."""
        trait_effects = {
            "feed": [(PlayerTraitAxis.GENEROUS_STINGY, 2), (PlayerTraitAxis.ATTENTIVE_NEGLECTFUL, 1)],
            "play": [(PlayerTraitAxis.PLAYFUL_SERIOUS, 3), (PlayerTraitAxis.ATTENTIVE_NEGLECTFUL, 1)],
            "clean": [(PlayerTraitAxis.ATTENTIVE_NEGLECTFUL, 2)],
            "pet": [(PlayerTraitAxis.ATTENTIVE_NEGLECTFUL, 2), (PlayerTraitAxis.PLAYFUL_SERIOUS, 1)],
            "talk": [(PlayerTraitAxis.TALKATIVE_QUIET, 3)],
            "sleep": [(PlayerTraitAxis.ATTENTIVE_NEGLECTFUL, 1)],
        }
        
        effects = trait_effects.get(action, [])
        for trait, delta in effects:
            self._adjust_trait(trait, delta)
    
    def _extract_facts_from_statement(self, statement: PlayerStatement):
        """Try to extract factual information from a statement."""
        text_lower = statement.text.lower()
        
        # Name extraction (simple patterns)
        name_patterns = [
            "my name is ", "i'm ", "i am ", "call me ", "name's "
        ]
        for pattern in name_patterns:
            if pattern in text_lower:
                idx = text_lower.index(pattern) + len(pattern)
                potential_name = statement.text[idx:].split()[0].strip(".,!?")
                if potential_name and len(potential_name) > 1:
                    self.record_fact("name", potential_name, confidence=0.9, source="player_stated")
                    break
        
        # Pet mentions
        pet_patterns = [
            ("i have a cat", "has_cat"),
            ("i have a dog", "has_dog"),
            ("my cat", "has_cat"),
            ("my dog", "has_dog"),
        ]
        for pattern, fact_type in pet_patterns:
            if pattern in text_lower:
                self.record_fact(fact_type, True, confidence=0.85, source="player_stated")
        
        # Preference extraction
        like_patterns = ["i like ", "i love ", "i enjoy ", "i prefer "]
        dislike_patterns = ["i hate ", "i don't like ", "i dislike "]
        
        for pattern in like_patterns:
            if pattern in text_lower:
                idx = text_lower.index(pattern) + len(pattern)
                thing = statement.text[idx:].split(".")[0].split(",")[0].strip()
                if thing:
                    self.record_fact(f"likes_{thing.replace(' ', '_')}", thing, 
                                    confidence=0.8, source="player_stated")
        
        for pattern in dislike_patterns:
            if pattern in text_lower:
                idx = text_lower.index(pattern) + len(pattern)
                thing = statement.text[idx:].split(".")[0].split(",")[0].strip()
                if thing:
                    self.record_fact(f"dislikes_{thing.replace(' ', '_')}", thing,
                                    confidence=0.8, source="player_stated")
    
    def _enforce_memory_limits(self):
        """Enforce memory limits on all unbounded data structures."""
        # Limit statements
        if len(self.statements) > self.MAX_STATEMENTS:
            # Keep important statements (high importance or frequently referenced)
            important = [s for s in self.statements if s.importance > 0.7 or s.times_referenced > 2]
            recent = self.statements[-self.MAX_STATEMENTS // 2:]
            # Combine, deduplicate, and limit
            combined = list({id(s): s for s in (important + recent)}.values())
            self.statements = combined[-self.MAX_STATEMENTS:]
            # Rebuild topic index
            self._rebuild_statement_index()
        
        # Limit questions asked
        if len(self.questions_asked) > self.MAX_QUESTIONS_ASKED:
            self.questions_asked = self.questions_asked[-self.MAX_QUESTIONS_ASKED:]
        
        # Limit pending questions
        if len(self.questions_pending) > self.MAX_QUESTIONS_PENDING:
            self.questions_pending = self.questions_pending[-self.MAX_QUESTIONS_PENDING:]
        
        # Limit visit pattern data
        if len(self.visit_pattern.session_durations) > self.MAX_SESSION_DURATIONS:
            self.visit_pattern.session_durations = self.visit_pattern.session_durations[-self.MAX_SESSION_DURATIONS:]
        
        if len(self.visit_pattern.gaps_between_visits) > self.MAX_VISIT_GAPS:
            self.visit_pattern.gaps_between_visits = self.visit_pattern.gaps_between_visits[-self.MAX_VISIT_GAPS:]
        
        # Limit action sequences (already done in end_session, but enforce here too)
        if len(self.behavior_pattern.action_sequences) > self.MAX_ACTION_SEQUENCES:
            self.behavior_pattern.action_sequences = self.behavior_pattern.action_sequences[-self.MAX_ACTION_SEQUENCES:]
        
        # Limit promises
        if len(self.promises_made) > self.MAX_PROMISES:
            self.promises_made = self.promises_made[-self.MAX_PROMISES:]
        
        # Limit pending observations
        if len(self._pending_observations) > self.MAX_OBSERVATIONS:
            # Keep highest priority observations
            self._pending_observations.sort(key=lambda x: x[1], reverse=True)
            self._pending_observations = self._pending_observations[:self.MAX_OBSERVATIONS]
    
    def _rebuild_statement_index(self):
        """Rebuild the statement topic index after trimming statements."""
        self.statement_topics = defaultdict(list)
        for idx, stmt in enumerate(self.statements):
            for tag in stmt.topic_tags:
                self.statement_topics[tag].append(idx)
                # Enforce per-topic limit
                if len(self.statement_topics[tag]) > self.MAX_STATEMENT_INDEX_PER_TOPIC:
                    self.statement_topics[tag] = self.statement_topics[tag][-self.MAX_STATEMENT_INDEX_PER_TOPIC:]
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for persistence."""
        return {
            "name": self.name,
            "nickname": self.nickname,
            "first_met": self.first_met,
            "facts": {k: {
                "fact_type": v.fact_type,
                "value": v.value,
                "confidence": v.confidence,
                "source": v.source,
                "learned_at": v.learned_at,
                "times_confirmed": v.times_confirmed,
                "contradicted": v.contradicted
            } for k, v in self.facts.items()},
            "statements": [{
                "text": s.text,
                "timestamp": s.timestamp,
                "context": s.context,
                "topic_tags": s.topic_tags,
                "sentiment": s.sentiment,
                "importance": s.importance,
                "times_referenced": s.times_referenced,
                "last_referenced": s.last_referenced
            } for s in self.statements],
            "questions_asked": self.questions_asked,
            "questions_pending": self.questions_pending,
            "question_cooldown": dict(self.question_cooldown),
            "visit_pattern": {
                "hour_counts": dict(self.visit_pattern.hour_counts),
                "day_counts": dict(self.visit_pattern.day_counts),
                "session_durations": self.visit_pattern.session_durations[-100:],
                "gaps_between_visits": self.visit_pattern.gaps_between_visits[-100:],
                "last_visit": self.visit_pattern.last_visit,
                "total_visits": self.visit_pattern.total_visits,
                "longest_absence": self.visit_pattern.longest_absence,
                "current_streak": self.visit_pattern.current_streak,
                "best_streak": self.visit_pattern.best_streak
            },
            "behavior_pattern": {
                "action_sequences": self.behavior_pattern.action_sequences[-50:],
                "favorite_actions": dict(self.behavior_pattern.favorite_actions),
                "action_by_mood": {k: dict(v) for k, v in self.behavior_pattern.action_by_mood.items()},
                "action_by_time": {str(k): dict(v) for k, v in self.behavior_pattern.action_by_time.items()},
                "avg_actions_per_session": self.behavior_pattern.avg_actions_per_session,
                "rushed_sessions": self.behavior_pattern.rushed_sessions,
                "leisurely_sessions": self.behavior_pattern.leisurely_sessions
            },
            "inferred_traits": self.inferred_traits,
            "trait_confidence": self.trait_confidence,
            "trust_level": self.trust_level,
            "annoyance_level": self.annoyance_level,
            "affection_level": self.affection_level,
            "respect_level": self.respect_level,
            "topics_discussed": dict(self.topics_discussed),
            "topic_sentiment": dict(self.topic_sentiment),
            "favorite_topics": self.favorite_topics,
            "avoided_topics": self.avoided_topics,
            "promises_made": self.promises_made,
            "promises_kept": self.promises_kept,
            "promises_broken": self.promises_broken
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PlayerModel":
        """Deserialize from dictionary."""
        model = cls()
        
        model.name = data.get("name")
        model.nickname = data.get("nickname")
        model.first_met = data.get("first_met")
        
        # Restore facts
        for k, v in data.get("facts", {}).items():
            model.facts[k] = PlayerFact(
                fact_type=v["fact_type"],
                value=v["value"],
                confidence=v["confidence"],
                source=v["source"],
                learned_at=v["learned_at"],
                times_confirmed=v.get("times_confirmed", 0),
                contradicted=v.get("contradicted", False)
            )
        
        # Restore statements
        for s in data.get("statements", []):
            stmt = PlayerStatement(
                text=s["text"],
                timestamp=s["timestamp"],
                context=s.get("context", ""),
                topic_tags=s.get("topic_tags", []),
                sentiment=s.get("sentiment", 0.0),
                importance=s.get("importance", 0.5),
                times_referenced=s.get("times_referenced", 0),
                last_referenced=s.get("last_referenced")
            )
            model.statements.append(stmt)
            for tag in stmt.topic_tags:
                model.statement_topics[tag].append(len(model.statements) - 1)
        
        model.questions_asked = data.get("questions_asked", [])
        model.questions_pending = data.get("questions_pending", [])
        model.question_cooldown = defaultdict(str, data.get("question_cooldown", {}))
        
        # Restore visit pattern
        vp = data.get("visit_pattern", {})
        model.visit_pattern.hour_counts = defaultdict(int, {int(k): v for k, v in vp.get("hour_counts", {}).items()})
        model.visit_pattern.day_counts = defaultdict(int, {int(k): v for k, v in vp.get("day_counts", {}).items()})
        model.visit_pattern.session_durations = vp.get("session_durations", [])
        model.visit_pattern.gaps_between_visits = vp.get("gaps_between_visits", [])
        model.visit_pattern.last_visit = vp.get("last_visit")
        model.visit_pattern.total_visits = vp.get("total_visits", 0)
        model.visit_pattern.longest_absence = vp.get("longest_absence", 0)
        model.visit_pattern.current_streak = vp.get("current_streak", 0)
        model.visit_pattern.best_streak = vp.get("best_streak", 0)
        
        # Restore behavior pattern
        bp = data.get("behavior_pattern", {})
        model.behavior_pattern.action_sequences = bp.get("action_sequences", [])
        model.behavior_pattern.favorite_actions = defaultdict(int, bp.get("favorite_actions", {}))
        # Restore action_by_mood (nested defaultdict)
        for mood, actions in bp.get("action_by_mood", {}).items():
            for action, count in actions.items():
                model.behavior_pattern.action_by_mood[mood][action] = count
        # Restore action_by_time (nested defaultdict with int keys)
        for hour_str, actions in bp.get("action_by_time", {}).items():
            hour = int(hour_str)
            for action, count in actions.items():
                model.behavior_pattern.action_by_time[hour][action] = count
        model.behavior_pattern.avg_actions_per_session = bp.get("avg_actions_per_session", 0)
        model.behavior_pattern.rushed_sessions = bp.get("rushed_sessions", 0)
        model.behavior_pattern.leisurely_sessions = bp.get("leisurely_sessions", 0)
        
        model.inferred_traits = data.get("inferred_traits", {axis.value: 0.0 for axis in PlayerTraitAxis})
        model.trait_confidence = data.get("trait_confidence", {axis.value: 0.0 for axis in PlayerTraitAxis})
        
        model.trust_level = data.get("trust_level", 0.0)
        model.annoyance_level = data.get("annoyance_level", 0.0)
        model.affection_level = data.get("affection_level", 0.0)
        model.respect_level = data.get("respect_level", 0.0)
        
        model.topics_discussed = defaultdict(int, data.get("topics_discussed", {}))
        model.topic_sentiment = defaultdict(float, data.get("topic_sentiment", {}))
        model.favorite_topics = data.get("favorite_topics", [])
        model.avoided_topics = data.get("avoided_topics", [])
        
        model.promises_made = data.get("promises_made", [])
        model.promises_kept = data.get("promises_kept", 0)
        model.promises_broken = data.get("promises_broken", 0)
        
        return model
