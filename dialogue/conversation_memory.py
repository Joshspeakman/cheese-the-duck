"""
Conversation Memory - Persistent storage of all conversations with the duck.

Tracks complete conversation history, extracts key information,
generates summaries for context compression, and enables semantic
retrieval of past conversations.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict
import json
import hashlib


class MessageRole(Enum):
    """Who sent the message."""
    PLAYER = "player"
    DUCK = "duck"
    SYSTEM = "system"


class ConversationTopic(Enum):
    """Broad topic categories for conversations."""
    GREETING = "greeting"
    FAREWELL = "farewell"
    PERSONAL = "personal"           # About player's life
    DUCK_LIFE = "duck_life"         # About duck's experiences
    PHILOSOPHY = "philosophy"       # Deep thoughts
    JOKES = "jokes"                 # Humor attempts
    FOOD = "food"                   # Food related
    WEATHER = "weather"             # Weather talk
    GAMES = "games"                 # Games and play
    MEMORIES = "memories"           # Reminiscing
    FEELINGS = "feelings"           # Emotional topics
    QUESTIONS = "questions"         # Q&A
    COMPLAINTS = "complaints"       # Complaints/concerns
    PRAISE = "praise"               # Compliments
    INSULTS = "insults"             # Negative talk
    EXISTENTIAL = "existential"     # Meaning of life stuff
    RANDOM = "random"               # Misc topics
    SECRETS = "secrets"             # Confidential stuff
    DREAMS = "dreams"               # Hopes/dreams
    PAST = "past"                   # History
    FUTURE = "future"               # Plans


@dataclass
class ConversationMessage:
    """A single message in a conversation."""
    role: str  # player, duck, system
    content: str
    timestamp: str
    sentiment: float = 0.0  # -1.0 to 1.0
    topics: List[str] = field(default_factory=list)
    extracted_facts: List[str] = field(default_factory=list)
    was_question: bool = False
    was_answer: bool = False
    referenced_memory: Optional[str] = None  # ID of memory referenced


@dataclass
class Conversation:
    """A complete conversation session."""
    id: str
    started_at: str
    ended_at: Optional[str] = None
    messages: List[ConversationMessage] = field(default_factory=list)
    summary: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    mood_start: Optional[str] = None
    mood_end: Optional[str] = None
    player_sentiment_avg: float = 0.0
    duck_sentiment_avg: float = 0.0
    key_facts_extracted: List[str] = field(default_factory=list)
    notable_quotes: List[str] = field(default_factory=list)
    was_meaningful: bool = False  # Did something important happen?
    relationship_delta: float = 0.0  # How much relationship changed


@dataclass
class ConversationSummary:
    """A compressed summary of one or more conversations."""
    id: str
    conversation_ids: List[str]
    period_start: str
    period_end: str
    summary_text: str
    key_topics: List[str]
    key_facts: List[str]
    relationship_trend: str  # improving, stable, declining
    notable_moments: List[str]
    message_count: int


class ConversationMemory:
    """
    Complete persistent memory of all conversations with the player.
    
    Features:
    - Bounded conversation history (prevents memory leaks)
    - Topic categorization
    - Fact extraction
    - Summary generation for old conversations
    - Semantic search through past conversations
    - Quote recall
    - Callback references ("Remember when you said...")
    """
    
    # Memory limits to prevent unbounded growth
    MAX_CONVERSATIONS = 100  # Keep last 100 full conversations
    MAX_SUMMARIES = 50  # Keep last 50 period summaries
    MAX_NOTABLE_QUOTES = 100  # Keep last 100 notable quotes
    MAX_INDEX_ENTRIES_PER_KEY = 50  # Max entries per topic/fact/date
    MAX_UNANSWERED_QUESTIONS = 20  # Keep last 20 unanswered questions
    MAX_CALLBACKS = 50  # Keep last 50 callback items
    
    def __init__(self):
        # Complete conversation history (bounded)
        self.conversations: List[Conversation] = []
        self.current_conversation: Optional[Conversation] = None
        
        # Summaries of old conversations (for context compression)
        self.summaries: List[ConversationSummary] = []
        
        # Indices for quick lookup (bounded per key)
        self.topic_index: Dict[str, List[str]] = defaultdict(list)  # topic -> conversation IDs
        self.fact_index: Dict[str, List[str]] = defaultdict(list)  # fact -> conversation IDs
        self.date_index: Dict[str, List[str]] = defaultdict(list)  # YYYY-MM-DD -> conversation IDs
        
        # Notable quotes from player (for callbacks)
        self.notable_quotes: List[Tuple[str, str, str]] = []  # (quote, conversation_id, timestamp)
        
        # Running statistics
        self.total_messages: int = 0
        self.total_player_messages: int = 0
        self.total_duck_messages: int = 0
        self.total_conversations: int = 0
        self.avg_conversation_length: float = 0.0
        self.longest_conversation: int = 0
        
        # Topic statistics
        self.topic_counts: Dict[str, int] = defaultdict(int)
        self.topic_sentiment: Dict[str, float] = defaultdict(float)
        
        # Time-based patterns
        self.conversations_by_hour: Dict[int, int] = defaultdict(int)
        self.conversations_by_day: Dict[int, int] = defaultdict(int)
        
        # Unanswered questions (things player asked that weren't answered)
        self.unanswered_questions: List[Tuple[str, str]] = []  # (question, timestamp)
        
        # Things to bring up later
        self.callbacks_queue: List[Dict] = []  # {type, content, context, priority}
    
    def start_conversation(self, duck_mood: Optional[str] = None) -> str:
        """Start a new conversation session."""
        conv_id = self._generate_id()
        now = datetime.now()
        
        self.current_conversation = Conversation(
            id=conv_id,
            started_at=now.isoformat(),
            mood_start=duck_mood
        )
        
        self.total_conversations += 1
        self.conversations_by_hour[now.hour] += 1
        self.conversations_by_day[now.weekday()] += 1
        
        return conv_id
    
    def add_message(self, role: str, content: str,
                    sentiment: float = 0.0,
                    topics: List[str] = None,
                    is_question: bool = False,
                    is_answer: bool = False,
                    referenced_memory: str = None) -> ConversationMessage:
        """Add a message to the current conversation."""
        if not self.current_conversation:
            self.start_conversation()
        
        # Detect if it's a question
        if not is_question and role == "player":
            is_question = self._is_question(content)
        
        # Auto-detect topics if not provided
        if not topics:
            topics = self._detect_topics(content)
        
        msg = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            sentiment=sentiment,
            topics=topics,
            was_question=is_question,
            was_answer=is_answer,
            referenced_memory=referenced_memory
        )
        
        self.current_conversation.messages.append(msg)
        
        # Update statistics
        self.total_messages += 1
        if role == "player":
            self.total_player_messages += 1
        elif role == "duck":
            self.total_duck_messages += 1
        
        # Track unanswered questions
        if is_question and role == "player":
            self.unanswered_questions.append((content, msg.timestamp))
        elif is_answer and role == "duck" and self.unanswered_questions:
            self.unanswered_questions.pop()  # Question was answered
        
        # Update topic indices
        for topic in topics:
            self.topic_counts[topic] += 1
            if self.current_conversation.id not in self.topic_index[topic]:
                self.topic_index[topic].append(self.current_conversation.id)
        
        # Check for notable quotes
        if role == "player" and self._is_notable_quote(content):
            self.notable_quotes.append((
                content,
                self.current_conversation.id,
                msg.timestamp
            ))
        
        # Extract facts from player messages
        if role == "player":
            facts = self._extract_facts(content)
            msg.extracted_facts = facts
            for fact in facts:
                self.fact_index[fact].append(self.current_conversation.id)
        
        return msg
    
    def end_conversation(self, duck_mood: Optional[str] = None):
        """End the current conversation and generate summary."""
        if not self.current_conversation:
            return
        
        conv = self.current_conversation
        conv.ended_at = datetime.now().isoformat()
        conv.mood_end = duck_mood
        
        # Calculate sentiments
        player_msgs = [m for m in conv.messages if m.role == "player"]
        duck_msgs = [m for m in conv.messages if m.role == "duck"]
        
        if player_msgs:
            conv.player_sentiment_avg = sum(m.sentiment for m in player_msgs) / len(player_msgs)
        if duck_msgs:
            conv.duck_sentiment_avg = sum(m.sentiment for m in duck_msgs) / len(duck_msgs)
        
        # Aggregate topics
        all_topics = []
        for msg in conv.messages:
            all_topics.extend(msg.topics)
        conv.topics = list(set(all_topics))
        
        # Aggregate extracted facts
        all_facts = []
        for msg in conv.messages:
            all_facts.extend(msg.extracted_facts)
        conv.key_facts_extracted = list(set(all_facts))
        
        # Determine if conversation was meaningful
        conv.was_meaningful = (
            len(conv.messages) >= 5 or
            any(t in conv.topics for t in ["personal", "feelings", "secrets", "dreams"]) or
            len(conv.key_facts_extracted) > 0
        )
        
        # Update statistics
        msg_count = len(conv.messages)
        if self.total_conversations > 0:
            self.avg_conversation_length = (
                (self.avg_conversation_length * (self.total_conversations - 1) + msg_count)
                / self.total_conversations
            )
        else:
            self.avg_conversation_length = float(msg_count)
        if msg_count > self.longest_conversation:
            self.longest_conversation = msg_count
        
        # Add to date index
        date_str = conv.started_at[:10]
        self.date_index[date_str].append(conv.id)
        
        # Generate summary for long conversations
        if len(conv.messages) >= 10:
            conv.summary = self._generate_summary(conv)
        
        # Store conversation
        self.conversations.append(conv)
        self.current_conversation = None
        
        # Periodically consolidate old conversations into summaries
        self._maybe_consolidate_old_conversations()
    
    def get_recent_context(self, max_messages: int = 20) -> List[Dict]:
        """Get recent conversation history for LLM context."""
        messages = []
        
        # Get current conversation messages
        if self.current_conversation:
            for msg in self.current_conversation.messages[-max_messages:]:
                messages.append({
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                })
        
        # If not enough, get from previous conversation
        if len(messages) < max_messages and self.conversations:
            remaining = max_messages - len(messages)
            last_conv = self.conversations[-1]
            for msg in last_conv.messages[-remaining:]:
                messages.insert(0, {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                })
        
        return messages
    
    def get_conversations_by_topic(self, topic: str, max_results: int = 10) -> List[Conversation]:
        """Get conversations that discussed a specific topic."""
        conv_ids = self.topic_index.get(topic, [])[-max_results:]
        return [c for c in self.conversations if c.id in conv_ids]
    
    def get_conversations_by_date(self, date: str) -> List[Conversation]:
        """Get conversations from a specific date (YYYY-MM-DD)."""
        conv_ids = self.date_index.get(date, [])
        return [c for c in self.conversations if c.id in conv_ids]
    
    def search_conversations(self, query: str, max_results: int = 10) -> List[Tuple[Conversation, List[ConversationMessage]]]:
        """Search through conversation history for matching content."""
        query_lower = query.lower()
        results = []
        
        for conv in reversed(self.conversations):
            matching_msgs = []
            for msg in conv.messages:
                if query_lower in msg.content.lower():
                    matching_msgs.append(msg)
            
            if matching_msgs:
                results.append((conv, matching_msgs))
                if len(results) >= max_results:
                    break
        
        return results
    
    def get_random_callback(self) -> Optional[Dict]:
        """Get a random past conversation element to bring up."""
        import random
        
        callbacks = []
        
        # Notable quotes the duck hasn't mentioned recently
        for quote, conv_id, timestamp in self.notable_quotes[-50:]:
            callbacks.append({
                "type": "quote",
                "content": quote,
                "intro": random.choice([
                    "You once said:",
                    "I remember you telling me:",
                    "You mentioned once that",
                    "I recall you saying:",
                    "Didn't you say something like:",
                ])
            })
        
        # Topics we discussed before
        if self.topic_counts:
            top_topics = sorted(self.topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for topic, count in top_topics:
                if count >= 3:
                    callbacks.append({
                        "type": "topic",
                        "content": topic,
                        "intro": random.choice([
                            f"We've talked about {topic} quite a bit.",
                            f"You seem to bring up {topic} often.",
                            f"Ah yes, {topic}. A recurring theme with you.",
                        ])
                    })
        
        # Unanswered questions
        for question, timestamp in self.unanswered_questions[-5:]:
            callbacks.append({
                "type": "unanswered",
                "content": question,
                "intro": "You once asked me something I never answered:"
            })
        
        if callbacks:
            return random.choice(callbacks)
        return None
    
    def get_conversation_stats(self) -> Dict:
        """Get statistics about conversation history."""
        return {
            "total_conversations": self.total_conversations,
            "total_messages": self.total_messages,
            "player_messages": self.total_player_messages,
            "duck_messages": self.total_duck_messages,
            "avg_conversation_length": self.avg_conversation_length,
            "longest_conversation": self.longest_conversation,
            "top_topics": sorted(self.topic_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "notable_quotes_count": len(self.notable_quotes),
            "unanswered_questions": len(self.unanswered_questions)
        }
    
    def get_topic_summary(self) -> Dict[str, Dict]:
        """Get summary of topics discussed."""
        return {
            topic: {
                "count": count,
                "sentiment": self.topic_sentiment.get(topic, 0.0),
                "conversations": len(self.topic_index.get(topic, []))
            }
            for topic, count in sorted(self.topic_counts.items(), key=lambda x: x[1], reverse=True)
        }
    
    def _generate_id(self) -> str:
        """Generate a unique conversation ID."""
        timestamp = datetime.now().isoformat()
        hash_input = f"{timestamp}-{self.total_conversations}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12]
    
    def _is_question(self, text: str) -> bool:
        """Detect if text is a question."""
        text = text.strip()
        if text.endswith("?"):
            return True
        question_starters = [
            "what", "who", "where", "when", "why", "how",
            "do you", "are you", "is it", "can you", "will you",
            "have you", "did you", "would you", "could you"
        ]
        text_lower = text.lower()
        return any(text_lower.startswith(q) for q in question_starters)
    
    def _detect_topics(self, text: str) -> List[str]:
        """Auto-detect conversation topics from text."""
        text_lower = text.lower()
        topics = []
        
        topic_keywords = {
            "greeting": ["hello", "hi ", "hey", "good morning", "good evening", "how are you"],
            "farewell": ["bye", "goodbye", "see you", "later", "goodnight", "gotta go"],
            "food": ["food", "eat", "hungry", "bread", "feed", "meal", "snack", "delicious"],
            "weather": ["weather", "rain", "sun", "snow", "cold", "hot", "storm", "cloudy"],
            "feelings": ["feel", "sad", "happy", "angry", "love", "hate", "scared", "worried"],
            "personal": ["my life", "my job", "my family", "my friend", "i work", "i live"],
            "games": ["play", "game", "fun", "boring", "exciting"],
            "philosophy": ["meaning", "life", "death", "purpose", "why do", "existence"],
            "dreams": ["dream", "hope", "wish", "want to", "someday", "future"],
            "past": ["remember", "used to", "when i was", "back then", "years ago"],
            "secrets": ["secret", "don't tell", "between us", "private", "confidential"],
            "praise": ["good duck", "love you", "best", "amazing", "awesome", "great"],
            "complaints": ["annoying", "stop", "don't like", "hate when", "frustrated"],
            "existential": ["exist", "real", "consciousness", "what am i", "who am i"],
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)
        
        if not topics:
            topics.append("random")
        
        return topics
    
    def _is_notable_quote(self, text: str) -> bool:
        """Determine if a player statement is worth remembering."""
        # Length check - not too short, not too long
        if len(text) < 10 or len(text) > 200:
            return False
        
        # Check for personal statements
        personal_markers = [
            "i think", "i believe", "i feel", "i love", "i hate",
            "my favorite", "i always", "i never", "i wish", "i hope",
            "i'm afraid", "i'm happy", "i'm sad", "i want"
        ]
        text_lower = text.lower()
        if any(marker in text_lower for marker in personal_markers):
            return True
        
        # Check for strong statements
        if any(word in text_lower for word in ["always", "never", "best", "worst", "love", "hate"]):
            return True
        
        return False
    
    def _extract_facts(self, text: str) -> List[str]:
        """Extract factual claims from player text."""
        facts = []
        text_lower = text.lower()
        
        # Name mentions
        if "my name is" in text_lower or "i'm called" in text_lower:
            facts.append("player_name_mentioned")
        
        # Pet mentions
        if any(pet in text_lower for pet in ["my cat", "my dog", "my pet", "i have a cat", "i have a dog"]):
            facts.append("has_pet")
        
        # Job/work mentions
        if any(work in text_lower for work in ["my job", "i work", "my career", "at work"]):
            facts.append("discussed_work")
        
        # Family mentions
        if any(fam in text_lower for fam in ["my mom", "my dad", "my sister", "my brother", "my family"]):
            facts.append("discussed_family")
        
        # Hobby mentions
        if any(hobby in text_lower for hobby in ["i like to", "i enjoy", "my hobby", "in my free time"]):
            facts.append("discussed_hobbies")
        
        # Emotional statements
        if any(emo in text_lower for emo in ["i'm sad", "i'm happy", "i'm stressed", "i'm tired"]):
            facts.append("emotional_statement")
        
        return facts
    
    def _generate_summary(self, conv: Conversation) -> str:
        """Generate a text summary of a conversation."""
        msg_count = len(conv.messages)
        topics = ", ".join(conv.topics[:3]) if conv.topics else "various things"
        
        summary_parts = [f"A conversation with {msg_count} messages about {topics}."]
        
        if conv.key_facts_extracted:
            summary_parts.append(f"Player shared: {', '.join(conv.key_facts_extracted[:3])}.")
        
        if conv.player_sentiment_avg > 0.3:
            summary_parts.append("Player seemed positive.")
        elif conv.player_sentiment_avg < -0.3:
            summary_parts.append("Player seemed negative.")
        
        return " ".join(summary_parts)
    
    def _maybe_consolidate_old_conversations(self):
        """Consolidate old conversations into summaries and enforce memory limits."""
        # Enforce all memory limits
        self._enforce_memory_limits()
        
        # Keep full details for last MAX_CONVERSATIONS
        if len(self.conversations) <= self.MAX_CONVERSATIONS:
            return
        
        # Find conversations to consolidate (beyond MAX_CONVERSATIONS limit)
        to_consolidate = self.conversations[:-self.MAX_CONVERSATIONS]
        
        if len(to_consolidate) >= 5:
            period_start = to_consolidate[0].started_at
            period_end = to_consolidate[-1].started_at
            
            all_topics = []
            all_facts = []
            all_moments = []
            total_messages = 0
            
            for conv in to_consolidate:
                all_topics.extend(conv.topics)
                all_facts.extend(conv.key_facts_extracted)
                total_messages += len(conv.messages)
                if conv.was_meaningful:
                    all_moments.append(conv.summary or f"Conversation on {conv.started_at[:10]}")
            
            summary = ConversationSummary(
                id=self._generate_id(),
                conversation_ids=[c.id for c in to_consolidate],
                period_start=period_start,
                period_end=period_end,
                summary_text=f"Period with {len(to_consolidate)} conversations, {total_messages} messages.",
                key_topics=list(set(all_topics))[:10],
                key_facts=list(set(all_facts))[:10],
                relationship_trend="stable",
                notable_moments=all_moments[:5],
                message_count=total_messages
            )
            
            self.summaries.append(summary)
            
            # Enforce summary limit
            if len(self.summaries) > self.MAX_SUMMARIES:
                self.summaries = self.summaries[-self.MAX_SUMMARIES:]
        
        # ACTUALLY REMOVE the old conversations to free memory
        self.conversations = self.conversations[-self.MAX_CONVERSATIONS:]
    
    def _enforce_memory_limits(self):
        """Enforce memory limits on all unbounded data structures."""
        # Limit notable quotes
        if len(self.notable_quotes) > self.MAX_NOTABLE_QUOTES:
            self.notable_quotes = self.notable_quotes[-self.MAX_NOTABLE_QUOTES:]
        
        # Limit unanswered questions
        if len(self.unanswered_questions) > self.MAX_UNANSWERED_QUESTIONS:
            self.unanswered_questions = self.unanswered_questions[-self.MAX_UNANSWERED_QUESTIONS:]
        
        # Limit callbacks queue
        if len(self.callbacks_queue) > self.MAX_CALLBACKS:
            self.callbacks_queue = self.callbacks_queue[-self.MAX_CALLBACKS:]
        
        # Limit index entries per key
        for topic in list(self.topic_index.keys()):
            if len(self.topic_index[topic]) > self.MAX_INDEX_ENTRIES_PER_KEY:
                self.topic_index[topic] = self.topic_index[topic][-self.MAX_INDEX_ENTRIES_PER_KEY:]
        
        for fact in list(self.fact_index.keys()):
            if len(self.fact_index[fact]) > self.MAX_INDEX_ENTRIES_PER_KEY:
                self.fact_index[fact] = self.fact_index[fact][-self.MAX_INDEX_ENTRIES_PER_KEY:]
        
        # Limit date index - only keep last 30 days
        now = datetime.now()
        cutoff = (now - timedelta(days=30)).strftime("%Y-%m-%d")
        old_dates = [d for d in self.date_index.keys() if d < cutoff]
        for date in old_dates:
            del self.date_index[date]
        
        # Limit remaining date entries
        for date in list(self.date_index.keys()):
            if len(self.date_index[date]) > self.MAX_INDEX_ENTRIES_PER_KEY:
                self.date_index[date] = self.date_index[date][-self.MAX_INDEX_ENTRIES_PER_KEY:]
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for persistence."""
        return {
            "conversations": [
                {
                    "id": c.id,
                    "started_at": c.started_at,
                    "ended_at": c.ended_at,
                    "messages": [
                        {
                            "role": m.role,
                            "content": m.content,
                            "timestamp": m.timestamp,
                            "sentiment": m.sentiment,
                            "topics": m.topics,
                            "extracted_facts": m.extracted_facts,
                            "was_question": m.was_question,
                            "was_answer": m.was_answer,
                            "referenced_memory": m.referenced_memory
                        }
                        for m in c.messages
                    ],
                    "summary": c.summary,
                    "topics": c.topics,
                    "mood_start": c.mood_start,
                    "mood_end": c.mood_end,
                    "player_sentiment_avg": c.player_sentiment_avg,
                    "duck_sentiment_avg": c.duck_sentiment_avg,
                    "key_facts_extracted": c.key_facts_extracted,
                    "notable_quotes": c.notable_quotes,
                    "was_meaningful": c.was_meaningful,
                    "relationship_delta": c.relationship_delta
                }
                for c in self.conversations
            ],
            "summaries": [
                {
                    "id": s.id,
                    "conversation_ids": s.conversation_ids,
                    "period_start": s.period_start,
                    "period_end": s.period_end,
                    "summary_text": s.summary_text,
                    "key_topics": s.key_topics,
                    "key_facts": s.key_facts,
                    "relationship_trend": s.relationship_trend,
                    "notable_moments": s.notable_moments,
                    "message_count": s.message_count
                }
                for s in self.summaries
            ],
            "topic_index": dict(self.topic_index),
            "fact_index": dict(self.fact_index),
            "date_index": dict(self.date_index),
            "notable_quotes": self.notable_quotes,
            "total_messages": self.total_messages,
            "total_player_messages": self.total_player_messages,
            "total_duck_messages": self.total_duck_messages,
            "total_conversations": self.total_conversations,
            "avg_conversation_length": self.avg_conversation_length,
            "longest_conversation": self.longest_conversation,
            "topic_counts": dict(self.topic_counts),
            "topic_sentiment": dict(self.topic_sentiment),
            "conversations_by_hour": dict(self.conversations_by_hour),
            "conversations_by_day": dict(self.conversations_by_day),
            "unanswered_questions": self.unanswered_questions,
            "callbacks_queue": self.callbacks_queue
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "ConversationMemory":
        """Deserialize from dictionary."""
        mem = cls()
        
        # Restore conversations
        for c_data in data.get("conversations", []):
            conv = Conversation(
                id=c_data["id"],
                started_at=c_data["started_at"],
                ended_at=c_data.get("ended_at"),
                summary=c_data.get("summary"),
                topics=c_data.get("topics", []),
                mood_start=c_data.get("mood_start"),
                mood_end=c_data.get("mood_end"),
                player_sentiment_avg=c_data.get("player_sentiment_avg", 0.0),
                duck_sentiment_avg=c_data.get("duck_sentiment_avg", 0.0),
                key_facts_extracted=c_data.get("key_facts_extracted", []),
                notable_quotes=c_data.get("notable_quotes", []),
                was_meaningful=c_data.get("was_meaningful", False),
                relationship_delta=c_data.get("relationship_delta", 0.0)
            )
            
            for m_data in c_data.get("messages", []):
                msg = ConversationMessage(
                    role=m_data["role"],
                    content=m_data["content"],
                    timestamp=m_data["timestamp"],
                    sentiment=m_data.get("sentiment", 0.0),
                    topics=m_data.get("topics", []),
                    extracted_facts=m_data.get("extracted_facts", []),
                    was_question=m_data.get("was_question", False),
                    was_answer=m_data.get("was_answer", False),
                    referenced_memory=m_data.get("referenced_memory")
                )
                conv.messages.append(msg)
            
            mem.conversations.append(conv)
        
        # Restore summaries
        for s_data in data.get("summaries", []):
            summary = ConversationSummary(
                id=s_data["id"],
                conversation_ids=s_data["conversation_ids"],
                period_start=s_data["period_start"],
                period_end=s_data["period_end"],
                summary_text=s_data["summary_text"],
                key_topics=s_data["key_topics"],
                key_facts=s_data["key_facts"],
                relationship_trend=s_data["relationship_trend"],
                notable_moments=s_data["notable_moments"],
                message_count=s_data["message_count"]
            )
            mem.summaries.append(summary)
        
        # Restore indices
        mem.topic_index = defaultdict(list, data.get("topic_index", {}))
        mem.fact_index = defaultdict(list, data.get("fact_index", {}))
        mem.date_index = defaultdict(list, data.get("date_index", {}))
        
        # Restore stats
        mem.notable_quotes = data.get("notable_quotes", [])
        mem.total_messages = data.get("total_messages", 0)
        mem.total_player_messages = data.get("total_player_messages", 0)
        mem.total_duck_messages = data.get("total_duck_messages", 0)
        mem.total_conversations = data.get("total_conversations", 0)
        mem.avg_conversation_length = data.get("avg_conversation_length", 0.0)
        mem.longest_conversation = data.get("longest_conversation", 0)
        mem.topic_counts = defaultdict(int, data.get("topic_counts", {}))
        mem.topic_sentiment = defaultdict(float, data.get("topic_sentiment", {}))
        mem.conversations_by_hour = defaultdict(int, {int(k): v for k, v in data.get("conversations_by_hour", {}).items()})
        mem.conversations_by_day = defaultdict(int, {int(k): v for k, v in data.get("conversations_by_day", {}).items()})
        mem.unanswered_questions = data.get("unanswered_questions", [])
        mem.callbacks_queue = data.get("callbacks_queue", [])
        
        return mem


# ============================================================
# Callback Intro Templates - Cheese's deadpan voice
# ============================================================

CALLBACK_INTRO_TEMPLATES = {
    "quote_recall": [
        "you said \"{quote}\" once. I wrote it down. in my brain.",
        "*stares* ...you told me \"{quote}.\" I remember everything.",
        "fun fact. you once said \"{quote}.\" not sure you meant it.",
        "I keep a mental file. under Q for quotes. you said \"{quote}.\"",
        "your exact words were \"{quote}.\" ducks have EXCELLENT memory.",
        "*flips through invisible notes* ah yes. \"{quote}.\" that was you.",
        "you probably forgot you said \"{quote}.\" I did not.",
        "I was thinking about when you said \"{quote}.\" just now. no reason.",
        "somewhere in our history you stated \"{quote}.\" for the record.",
        "*taps beak* \"{quote}.\" your words. not mine.",
    ],
    "topic_recall": [
        "we've talked about {topic} a suspicious number of times.",
        "*tilts head* {topic} again. you have patterns. I NOTICE patterns.",
        "ah. {topic}. your favorite recurring theme.",
        "you bring up {topic} a lot. like a LOT a lot.",
        "*adjusts feathers* so. {topic}. we meet again.",
        "I was going to bring up {topic} but you always beat me to it.",
        "the {topic} saga continues. I should start keeping a tally.",
        "*stares into the distance* {topic}. our old friend.",
        "you and {topic}. name a more iconic duo. I'll wait.",
        "every time you mention {topic} I add a mental tally mark. we're in double digits.",
    ],
    "unanswered_question": [
        "you asked me \"{question}\" and I never answered. it's been bothering me.",
        "*suddenly* wait. you once asked \"{question}\" and I just... didn't respond.",
        "so about \"{question}\" — I've been thinking. PROCESSING. same thing.",
        "remember when you asked \"{question}\"? I do. I had no answer then.",
        "*clears throat* you asked \"{question}\" a while back. I owe you an answer.",
        "I ghosted your question about \"{question}.\" not on purpose. probably.",
        "that time you asked \"{question}\" and I went silent. that was THINKING.",
        "you asked \"{question}\" once. I'm circling back. ducks are thorough.",
    ],
    "pattern_observation": [
        "I've noticed you {pattern}. don't worry about it. or DO worry.",
        "*squints* you {pattern}. consistently. I have DATA.",
        "pattern detected. you {pattern}. this is just an observation.",
        "so you {pattern}. every time. I find that... interesting.",
        "I'm not judging but you {pattern}. ok maybe I'm judging a LITTLE.",
        "fun behavioral note. you {pattern}. filed under: habits.",
        "*pulls out invisible clipboard* subject {pattern}. noted.",
        "you probably don't realize you {pattern}. but I see everything.",
        "statistically speaking you {pattern}. the numbers don't lie.",
        "you {pattern}. this is not a complaint. it's a REPORT.",
    ],
    "milestone_recall": [
        "remember when {milestone}. I remember. I was there.",
        "*stares wistfully* {milestone}. good times. or at least times.",
        "we've come a long way since {milestone}. mostly you. I was already great.",
        "*nods* {milestone}. a moment in our shared history.",
        "thinking about when {milestone}. nostalgia is a weird feeling for a duck.",
        "it was a big deal when {milestone}. I played it cool but I was impressed.",
        "*adjusts feathers* {milestone}. seems like yesterday. or whenever it was.",
        "I have a mental scrapbook and {milestone} is in it. the page is slightly crumpled.",
    ],
    "mood_observation": [
        "you seem {mood} lately. I notice these things. occupational hazard.",
        "*tilts head* you've been {mood}. I'm not a therapist but I have observations.",
        "detecting {mood} energy. my readings are NEVER wrong.",
        "you're giving {mood} vibes. ducks are very perceptive. it's a whole thing.",
        "*looks at you sideways* {mood}. am I right. I'm right.",
        "I've been picking up on some {mood} patterns from you. just saying.",
        "your whole energy has been {mood} recently. I have a chart. in my head.",
        "*concerned duck noises* you seem {mood}. not that I'm WORRIED or anything.",
    ],
}
