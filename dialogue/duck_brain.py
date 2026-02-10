"""
Duck Brain - The unified intelligence system for Cheese the Duck.

This is the central orchestrator that combines:
- DuckMemory (event/interaction memory)
- ConversationMemory (full conversation history)
- PlayerModel (what we know about the player)
- QuestionManager (asking and tracking questions)
- SeamanDialogue (deadpan response generation)
- Personality evolution over time

The Duck Brain determines what the duck says, when to ask questions,
what observations to make, and how to reference past conversations.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, TYPE_CHECKING
from datetime import datetime, timedelta
from enum import Enum
import random
import time

from dialogue.player_model import PlayerModel
from dialogue.conversation_memory import ConversationMemory
from dialogue.questions import QuestionManager, DUCK_QUESTIONS, DuckQuestion
from dialogue.seaman_style import SeamanDialogue, DialogueLine, DialogueTone
from dialogue.ritual_tracker import RitualTracker

if TYPE_CHECKING:
    from dialogue.memory import DuckMemory


class ResponsePriority(Enum):
    """Priority levels for different types of responses."""
    CRITICAL = 5      # Must say this (direct question, important event)
    HIGH = 4          # Should say this (callbacks, observations)
    NORMAL = 3        # Good to say (contextual comments)
    LOW = 2           # Can say this (idle thoughts)
    AMBIENT = 1       # Background flavor


@dataclass
class DuckThought:
    """A thought or observation the duck wants to express."""
    text: str
    priority: ResponsePriority
    category: str  # greeting, observation, callback, question, idle, etc.
    source: str  # What triggered this thought
    tone: DialogueTone = DialogueTone.DEADPAN
    expires_at: Optional[float] = None  # Unix timestamp when thought is no longer relevant
    requires_response: bool = False  # Does this need player input?
    metadata: Dict = field(default_factory=dict)


class DuckMood(Enum):
    """Internal emotional state that affects dialogue."""
    NEUTRAL = "neutral"
    PLEASED = "pleased"
    ANNOYED = "annoyed"
    CURIOUS = "curious"
    MELANCHOLIC = "melancholic"
    AFFECTIONATE = "affectionate"
    PHILOSOPHICAL = "philosophical"
    PLAYFUL = "playful"


class DuckBrain:
    """
    The unified intelligence system for the duck.
    
    Coordinates all memory systems and dialogue generation to create
    a coherent, persistent personality that remembers everything
    and makes uncomfortably accurate observations.
    """
    
    def __init__(self, duck_name: str = "Cheese", duck_memory: "DuckMemory" = None):
        # Duck identity
        self.duck_name = duck_name
        
        # Core systems
        self.duck_memory = duck_memory  # Existing memory system
        self.player_model = PlayerModel()
        self.conversation_memory = ConversationMemory()
        self.question_manager = QuestionManager()
        self.dialogue_generator = SeamanDialogue(duck_name=duck_name)
        self.ritual_tracker = RitualTracker()
        
        # Internal state
        self._internal_mood = DuckMood.NEUTRAL
        self._mood_intensity = 0.5  # 0-1, how strongly feeling the mood
        self._last_mood_update = time.time()
        
        # Thought queue (prioritized things to say)
        self._thought_queue: List[DuckThought] = []
        
        # Recent interaction tracking
        self._last_player_message: Optional[str] = None
        self._last_duck_response: Optional[str] = None
        self._last_interaction_time = time.time()
        self._interactions_this_session = 0
        
        # Session tracking
        self._session_start_time: Optional[float] = None
        self._session_messages: int = 0
        self._asked_question_this_session = False
        
        # Observation cooldowns (prevent spam)
        self._last_observation_time = 0.0
        self._last_callback_time = 0.0
        self._last_question_time = 0.0
        
        # Personality evolution
        self._affection_growth_rate = 0.1  # How fast affection builds
        self._trust_growth_rate = 0.05
        
        # Genuine moment tracking (to keep them rare)
        self._genuine_moments_today = 0
        self._last_genuine_moment_date: Optional[str] = None
        self._max_genuine_per_day = 3
        
        # External state flags (set by game loop)
        self.__cold_shoulder_active = False  # Suppresses genuine moments during cold shoulder
        self.__duck_trust = 20.0  # Synced from duck.trust for genuine moment gating
    
    @property
    def _cold_shoulder_active(self) -> bool:
        return self.__cold_shoulder_active
    
    @_cold_shoulder_active.setter
    def _cold_shoulder_active(self, value: bool):
        self.__cold_shoulder_active = value
        # Propagate to dialogue generator so it can suppress genuine moments too
        if hasattr(self, 'dialogue_generator'):
            self.dialogue_generator._cold_shoulder_active = value

    @property
    def _duck_trust(self) -> float:
        return self.__duck_trust
    
    @_duck_trust.setter
    def _duck_trust(self, value: float):
        self.__duck_trust = value
        if hasattr(self, 'dialogue_generator'):
            self.dialogue_generator._duck_trust = value
    
    # ========== SESSION MANAGEMENT ==========
    
    def start_session(self, time_since_last: float = 0):
        """Called when player starts playing."""
        self._session_start_time = time.time()
        self._session_messages = 0
        self._asked_question_this_session = False
        self._interactions_this_session = 0
        
        # Update player model
        self.player_model.start_session()
        
        # Reset question manager session
        self.question_manager.reset_session()
        
        # Check for pending observations
        self._generate_session_start_thoughts(time_since_last)
        
        # Start conversation in conversation memory
        mood_str = self._internal_mood.value if self._internal_mood else "neutral"
        self.conversation_memory.start_conversation(duck_mood=mood_str)
    
    def end_session(self):
        """Called when player stops playing."""
        if self._session_start_time:
            duration = (time.time() - self._session_start_time) / 60  # Minutes
            self.player_model.end_session()
        
        # End conversation in conversation memory
        mood_str = self._internal_mood.value if self._internal_mood else "neutral"
        self.conversation_memory.end_conversation(duck_mood=mood_str)
        
        self._session_start_time = None
    
    # ========== MAIN DIALOGUE INTERFACE ==========
    
    def process_player_message(self, message: str, response: str = None, context: Dict = None) -> str:
        """
        Process a player message and the duck's response.
        
        This records the exchange in memory for future callbacks.
        
        Args:
            message: What the player said
            response: What the duck responded with (if already generated by LLM)
            context: Optional context dict with keys like 'duck_mood', 'weather', etc.
            
        Returns:
            The response (either the passed one or a generated one)
        """
        if isinstance(response, dict):
            # Support old calling convention where response was context
            context = response
            response = None
        context = context or {}
        now = time.time()
        
        self._last_player_message = message
        self._last_interaction_time = now
        self._session_messages += 1
        
        # Record in conversation memory
        topics = self.conversation_memory._detect_topics(message)
        sentiment = self._estimate_sentiment(message)
        self.conversation_memory.add_message(
            role="player",
            content=message,
            sentiment=sentiment,
            topics=topics
        )
        
        # Record in player model
        self.player_model.record_statement(
            text=message,
            context=context.get("context", "chat"),
            topic_tags=topics,
            sentiment=sentiment
        )
        
        # Update relationship based on interaction
        self._update_relationship_from_message(message, sentiment)
        
        # Use provided response or generate one
        if response is None:
            response = self._generate_response(message, context)
        
        # Record duck response
        self._last_duck_response = response
        duck_sentiment = 0.1  # Slightly positive (duck is engaging)
        self.conversation_memory.add_message(
            role="duck",
            content=response,
            sentiment=duck_sentiment
        )
        
        return response
    
    def process_action(self, action: str, context = None) -> str:
        """
        Process a player action (feed, play, clean, pet, etc.)
        and generate a response.
        
        Args:
            action: The action type (feed, play, clean, pet, sleep, etc.)
            context: Either a dict with context keys or a string description
        """
        # Handle context as either dict or string
        if isinstance(context, str):
            context = {"description": context}
        context = context or {}
        now = time.time()
        
        self._last_interaction_time = now
        self._interactions_this_session += 1
        
        # Record in player model
        duck_mood = context.get("duck_mood", "content")
        self.player_model.record_action(action, duck_mood)
        
        # Record in ritual tracker — may return a deadpan observation
        ritual_obs = self.ritual_tracker.record_interaction(action)
        if ritual_obs:
            self._thought_queue.append(DuckThought(
                text=ritual_obs,
                priority=ResponsePriority.NORMAL,
                category="ritual",
                source="ritual_tracker",
                tone=DialogueTone.DEADPAN,
                expires_at=now + 120,  # 2 minute window to surface
            ))
        
        # Get action count for milestones
        action_count = self.player_model.behavior_pattern.favorite_actions.get(action, 0)
        
        # Generate response
        response_line = self.dialogue_generator.generate_after_action(
            action=action,
            duck_mood=duck_mood,
            player_model=self.player_model,
            action_count=action_count
        )
        
        # Maybe add a follow-up thought
        if random.random() < 0.2:  # 20% chance
            self._maybe_add_observation()
        
        return response_line.text
    
    def get_greeting(self, time_since_last: float = 0) -> str:
        """Get a greeting when player arrives."""
        greeting = self.dialogue_generator.generate_greeting(
            player_model=self.player_model,
            duck_memory=self.duck_memory,
            time_since_last=time_since_last
        )
        return greeting.text
    
    def get_farewell(self) -> str:
        """Get a farewell when player leaves."""
        session_duration = 0.0
        if self._session_start_time:
            session_duration = (time.time() - self._session_start_time) / 60
        
        farewell = self.dialogue_generator.generate_farewell(
            player_model=self.player_model,
            session_duration=session_duration
        )
        return farewell.text
    
    def get_idle_thought(self, duck_mood: str = None, 
                          weather: str = None,
                          time_of_day: str = None) -> Optional[str]:
        """Get an idle thought/comment if appropriate."""
        # Check if we have queued thoughts (includes ritual match observations)
        thought = self._get_next_thought()
        if thought:
            return thought.text
        
        # Check for missed rituals (broken routines the duck should mention)
        missed = self.ritual_tracker.check_missed_rituals()
        if missed:
            # Queue all but return the first one now
            for obs in missed[1:]:
                self._thought_queue.append(DuckThought(
                    text=obs,
                    priority=ResponsePriority.NORMAL,
                    category="ritual",
                    source="ritual_tracker_missed",
                    tone=DialogueTone.DEADPAN,
                    expires_at=time.time() + 300,
                ))
            return missed[0]
        
        # Generate new idle thought
        idle = self.dialogue_generator.generate_idle(
            duck_mood=duck_mood or "content",
            weather=weather,
            time_of_day=time_of_day,
            player_model=self.player_model
        )
        return idle.text
    
    def get_observation(self, context: Dict = None) -> Optional[str]:
        """Get an observation about player behavior if available.
        
        Args:
            context: Optional dict with keys like 'weather', 'time_of_day', 'location', 'mood'
        """
        now = time.time()
        context = context or {}
        
        # Cooldown check (minimum 2 minutes between observations)
        if now - self._last_observation_time < 120:
            return None
        
        observation = self.dialogue_generator.generate_observation(
            player_model=self.player_model,
            duck_memory=self.duck_memory,
            context=context
        )
        
        if observation:
            self._last_observation_time = now
            return observation.text
        
        return None

    def get_weather_forecast(self, atmosphere) -> Optional[str]:
        """Get a weather forecast comment if weather is about to change.
        
        Args:
            atmosphere: AtmosphereManager instance
            
        Returns:
            A deadpan forecast comment, or None
        """
        remaining = atmosphere.get_weather_remaining_hours()
        # Only forecast when current weather has < 1 hour left
        if remaining > 1.0:
            return None
        
        # Low probability (10% per call to prevent spam)
        if random.random() > 0.10:
            return None
        
        try:
            from world.atmosphere import WEATHER_DATA
            next_type, confidence = atmosphere.forecast_next_weather()
            weather_name = WEATHER_DATA.get(next_type, {}).get("name", next_type.value)
        except Exception:
            return None
        
        # Higher confidence = more certain predictions
        if confidence > 0.3:
            forecasts = [
                f"My feathers say {weather_name.lower()} is coming. They're rarely wrong. Unfortunately.",
                f"*sniffs air* ...{weather_name}. Soon. Don't ask how I know.",
                f"Weather's shifting. I give it an hour before {weather_name.lower()}. Calling it.",
                f"The wind changed. That means {weather_name.lower()}. Duck meteorology. Look it up.",
            ]
        else:
            forecasts = [
                f"Something's changing in the air. Could be {weather_name.lower()}. Could be nothing.",
                f"*tilts head* ...My weather sense is tingling. Maybe {weather_name.lower()}? Maybe gas.",
                f"I'd say {weather_name.lower()} is on the way, but honestly, I'm guessing. Educated guessing.",
            ]
        
        return random.choice(forecasts)
    
    def get_callback(self) -> Optional[str]:
        """Get a callback to a past conversation if appropriate."""
        now = time.time()
        
        # Cooldown check (minimum 5 minutes between callbacks)
        if now - self._last_callback_time < 300:
            return None
        
        # Try question callback first
        callback_data = self.question_manager.get_callback(self.player_model)
        if callback_data:
            self._last_callback_time = now
            return callback_data[0]
        
        # Try conversation callback
        callback = self.dialogue_generator.generate_callback(
            player_model=self.player_model,
            conversation_memory=self.conversation_memory
        )
        
        if callback:
            self._last_callback_time = now
            return callback.text
        
        return None
    
    def get_question(self, relationship_level: str = "acquaintance",
                      time_of_day: str = "day",
                      hours_since_last: float = 0) -> Optional[Tuple[str, str]]:
        """
        Get a question to ask the player if appropriate.
        
        Returns (question_id, question_text) if available.
        """
        now = time.time()
        
        # Cooldown check
        if now - self._last_question_time < 180:  # 3 minutes
            return None
        
        # Session limit
        if self._asked_question_this_session:
            return None
        
        question = self.question_manager.get_next_question(
            relationship_level=relationship_level,
            time_of_day=time_of_day,
            hours_since_last_visit=hours_since_last,
            player_model=self.player_model
        )
        
        if question:
            self._last_question_time = now
            self._asked_question_this_session = True
            self.question_manager.record_question_asked(question.id)
            return question.id, question.text
        
        return None
    
    def record_question_answer(self, question_id: str, answer: str) -> Optional[str]:
        """
        Record player's answer to a question.
        
        Returns follow-up response if available.
        """
        follow_up = self.question_manager.record_answer(question_id, answer)
        
        # Extract any facts
        if question_id in DUCK_QUESTIONS:
            question = DUCK_QUESTIONS[question_id]
            if question.extracts_fact:
                self.player_model.record_fact(
                    fact_type=question.extracts_fact,
                    value=answer,
                    source="question_answer"
                )
        
        return follow_up
    
    # ========== LLM INTEGRATION ==========
    
    def build_llm_prompt(self) -> str:
        """Build the system prompt for LLM dialogue generation."""
        return self.dialogue_generator.build_llm_personality_prompt(
            player_model=self.player_model,
            duck_memory=self.duck_memory,
            conversation_memory=self.conversation_memory
        )
    
    def get_llm_context(self, max_messages: int = 10) -> List[Dict]:
        """Get recent conversation context for LLM."""
        return self.conversation_memory.get_recent_context(max_messages)
    
    # ========== INTERNAL METHODS ==========
    
    def _generate_response(self, message: str, context: Dict) -> str:
        """Generate a response to a player message."""
        message_lower = message.lower()
        
        # Check if this is answering a pending question
        unanswered = self.question_manager.get_unanswered_questions()
        if unanswered:
            # Assume this is answering the most recent question
            last_q = unanswered[-1]
            follow_up = self.record_question_answer(last_q, message)
            if follow_up:
                return follow_up
        
        # Check for specific question patterns
        is_question = self.conversation_memory._is_question(message)
        if is_question:
            response = self.dialogue_generator.generate_question_response(
                player_question=message,
                player_model=self.player_model,
                duck_memory=self.duck_memory
            )
            return response.text
        
        # Default to template/random response
        # (In real implementation, this would call LLM)
        return self._generate_contextual_response(message, context)
    
    def _generate_contextual_response(self, message: str, context: Dict) -> str:
        """Generate a contextual response without LLM."""
        message_lower = message.lower()
        
        # Simple pattern matching for common phrases
        if any(g in message_lower for g in ["hello", "hi ", "hey", "good morning", "good evening"]):
            responses = [
                "Hello. You're here. I noticed.",
                "Ah. Greetings. I was just contemplating existence.",
                "*looks up* Oh. It's you. Hello.",
            ]
            return random.choice(responses)
        
        if any(f in message_lower for f in ["bye", "goodbye", "see you", "gotta go"]):
            return self.get_farewell()
        
        if any(l in message_lower for l in ["love you", "i love", "you're the best"]):
            if random.random() < 0.15:  # Rare genuine
                return "I... appreciate you too. Don't make me say it again."
            return "That's... a strong statement. I'm just a duck. But thank you."
        
        if any(s in message_lower for s in ["sorry", "apologize", "my bad"]):
            return "Apology... acknowledged. I'll add it to my records. Under 'times you said sorry'."
        
        if any(t in message_lower for t in ["thank", "thanks"]):
            return "You're... welcome? I'm not sure what I did, but I'll accept gratitude."
        
        # Random thoughtful response
        responses = [
            "I heard you. I'm processing it. Results pending.",
            "*tilts head* Interesting. Tell me more. Or don't. Either way.",
            "Hmm. That's... something. I'll think about it. For a while.",
            "I see. Words. You've spoken them. I'm acknowledging them.",
            "*blinks* Noted. Filed under 'things you said'. It's a large file.",
        ]
        return random.choice(responses)
    
    def _generate_session_start_thoughts(self, time_since_last: float):
        """Generate thoughts for the start of a session."""
        hours = time_since_last
        
        # Long absence observation
        if hours > 72:
            days = int(hours / 24)
            self._thought_queue.append(DuckThought(
                text=f"You were gone {days} days. I wasn't worried. Ducks don't worry. Much.",
                priority=ResponsePriority.HIGH,
                category="observation",
                source="absence",
                tone=DialogueTone.DEADPAN
            ))
        
        # Check for pending observations from player model
        obs = self.player_model.get_pending_observation()
        if obs:
            self._thought_queue.append(DuckThought(
                text=obs,
                priority=ResponsePriority.NORMAL,
                category="observation",
                source="player_model"
            ))
    
    def _maybe_add_observation(self):
        """Maybe add an observation to the thought queue."""
        if random.random() > 0.3:  # 70% chance to skip
            return
        
        observation = self.dialogue_generator.generate_observation(
            player_model=self.player_model,
            duck_memory=self.duck_memory
        )
        
        if observation:
            self._thought_queue.append(DuckThought(
                text=observation.text,
                priority=ResponsePriority.LOW,
                category="observation",
                source="random",
                tone=observation.tone
            ))
    
    def _get_next_thought(self) -> Optional[DuckThought]:
        """Get the next thought from the queue if available."""
        if not self._thought_queue:
            return None
        
        now = time.time()
        
        # Remove expired thoughts
        self._thought_queue = [
            t for t in self._thought_queue
            if not t.expires_at or t.expires_at > now
        ]
        
        if not self._thought_queue:
            return None
        
        # Sort by priority and return highest
        self._thought_queue.sort(key=lambda t: t.priority.value, reverse=True)
        return self._thought_queue.pop(0)
    
    def _update_relationship_from_message(self, message: str, sentiment: float):
        """Update relationship metrics based on a message."""
        # Positive messages increase trust and affection
        if sentiment > 0.3:
            self.player_model.trust_level = min(100, 
                self.player_model.trust_level + self._trust_growth_rate * 5)
            self.player_model.affection_level = min(100,
                self.player_model.affection_level + self._affection_growth_rate * 3)
        
        # Negative messages decrease trust, increase annoyance
        elif sentiment < -0.3:
            self.player_model.trust_level = max(-100,
                self.player_model.trust_level - self._trust_growth_rate * 3)
            self.player_model.annoyance_level = min(100,
                self.player_model.annoyance_level + 5)
        
        # Regular interaction slowly builds trust
        else:
            self.player_model.trust_level = min(100,
                self.player_model.trust_level + self._trust_growth_rate)
        
        # Annoyance decays over time
        self.player_model.annoyance_level = max(0,
            self.player_model.annoyance_level - 0.5)
    
    def _estimate_sentiment(self, text: str) -> float:
        """Estimate sentiment of text (-1 to 1)."""
        text_lower = text.lower()
        
        positive_words = [
            "love", "great", "amazing", "awesome", "wonderful", "beautiful",
            "happy", "joy", "best", "thank", "appreciate", "good", "nice",
            "cute", "sweet", "kind", "friend", "like"
        ]
        
        negative_words = [
            "hate", "terrible", "awful", "horrible", "ugly", "stupid",
            "sad", "angry", "worst", "bad", "annoying", "boring", "dumb",
            "suck", "idiot", "shut up"
        ]
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count + neg_count == 0:
            return 0.0
        
        return (pos_count - neg_count) / (pos_count + neg_count)
    
    def _can_do_genuine_moment(self) -> bool:
        """Check if we can have a genuine moment (keep them rare).
        
        Blocked entirely during cold shoulder — the duck is too upset
        to let its guard down. Also requires trust ≥ 70 (devoted level).
        """
        if self._cold_shoulder_active:
            return False
        if self._duck_trust < 70:
            return False
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        if self._last_genuine_moment_date != today:
            self._genuine_moments_today = 0
            self._last_genuine_moment_date = today
        
        return self._genuine_moments_today < self._max_genuine_per_day
    
    def _record_genuine_moment(self):
        """Record that a genuine moment occurred."""
        today = datetime.now().strftime("%Y-%m-%d")
        if self._last_genuine_moment_date != today:
            self._genuine_moments_today = 0
            self._last_genuine_moment_date = today
        self._genuine_moments_today += 1
    
    # ========== PERSISTENCE ==========
    
    def to_dict(self) -> Dict:
        """Serialize the duck brain for persistence."""
        return {
            "player_model": self.player_model.to_dict(),
            "conversation_memory": self.conversation_memory.to_dict(),
            "question_manager": self.question_manager.to_dict(),
            "ritual_tracker": self.ritual_tracker.to_dict(),
            "internal_mood": self._internal_mood.value,
            "mood_intensity": self._mood_intensity,
            "genuine_moments_today": self._genuine_moments_today,
            "last_genuine_moment_date": self._last_genuine_moment_date,
            "last_observation_time": self._last_observation_time,
            "last_callback_time": self._last_callback_time,
            "last_question_time": self._last_question_time,
            "duck_name": self.duck_name,
        }
    
    @classmethod
    def from_dict(cls, data: Dict, duck_memory: "DuckMemory" = None) -> "DuckBrain":
        """Deserialize from dictionary."""
        duck_name = data.get("duck_name", "Cheese")
        brain = cls(duck_name=duck_name, duck_memory=duck_memory)
        
        if "player_model" in data:
            brain.player_model = PlayerModel.from_dict(data["player_model"])
        
        if "conversation_memory" in data:
            brain.conversation_memory = ConversationMemory.from_dict(data["conversation_memory"])
        
        if "question_manager" in data:
            brain.question_manager = QuestionManager.from_dict(data["question_manager"])
        
        if "ritual_tracker" in data:
            brain.ritual_tracker = RitualTracker.from_dict(data["ritual_tracker"])
        
        if "internal_mood" in data:
            try:
                brain._internal_mood = DuckMood(data["internal_mood"])
            except ValueError:
                brain._internal_mood = DuckMood.NEUTRAL
        
        brain._mood_intensity = data.get("mood_intensity", 0.5)
        brain._genuine_moments_today = data.get("genuine_moments_today", 0)
        brain._last_genuine_moment_date = data.get("last_genuine_moment_date")
        brain._last_observation_time = data.get("last_observation_time", 0)
        brain._last_callback_time = data.get("last_callback_time", 0)
        brain._last_question_time = data.get("last_question_time", 0)
        
        return brain
    
    # ========== STATISTICS & DEBUG ==========
    
    def get_statistics(self) -> Dict:
        """Get brain statistics for debugging/display."""
        return {
            "player_name": self.player_model.name,
            "total_visits": self.player_model.visit_pattern.total_visits,
            "current_streak": self.player_model.visit_pattern.current_streak,
            "best_streak": self.player_model.visit_pattern.best_streak,
            "total_conversations": self.conversation_memory.total_conversations,
            "total_messages": self.conversation_memory.total_messages,
            "questions_asked": self.question_manager.total_questions_asked,
            "questions_answered": self.question_manager.total_answers_received,
            "facts_known": len(self.player_model.facts),
            "statements_remembered": len(self.player_model.statements),
            "trust_level": self.player_model.trust_level,
            "affection_level": self.player_model.affection_level,
            "relationship_level": self._get_relationship_label(),
        }
    
    def _get_relationship_label(self) -> str:
        """Get a human-readable relationship label."""
        trust = self.player_model.trust_level
        affection = self.player_model.affection_level
        
        combined = (trust + affection) / 2
        
        if combined < -50:
            return "Hostile"
        elif combined < -20:
            return "Distrustful"
        elif combined < 10:
            return "Stranger"
        elif combined < 30:
            return "Acquaintance"
        elif combined < 50:
            return "Familiar"
        elif combined < 70:
            return "Friend"
        elif combined < 90:
            return "Close Friend"
        else:
            return "Bonded"
