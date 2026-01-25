"""
Duck Questions - System for the duck to ask player questions.

The duck asks questions to learn about the player, then remembers
and references the answers later. Questions are contextual, 
relationship-appropriate, and delivered with characteristic deadpan.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import random


class QuestionCategory(Enum):
    """Categories of questions the duck can ask."""
    INTRODUCTION = "introduction"       # Name, basic info
    PREFERENCES = "preferences"         # Likes, dislikes
    PERSONAL = "personal"               # Life, job, family
    PHILOSOPHICAL = "philosophical"     # Deep thoughts
    FEELINGS = "feelings"               # Emotions, moods
    OPINIONS = "opinions"               # Views on things
    HYPOTHETICAL = "hypothetical"       # What-if scenarios
    MEMORIES = "memories"               # Player's past
    HABITS = "habits"                   # Daily life patterns
    RELATIONSHIP = "relationship"       # About player-duck bond
    SILLY = "silly"                     # Absurd questions
    CALLBACK = "callback"               # Follow-up to past answers


class QuestionTiming(Enum):
    """When a question is appropriate to ask."""
    FIRST_MEETING = "first_meeting"
    EARLY_RELATIONSHIP = "early_relationship"
    ESTABLISHED = "established"
    CLOSE_FRIENDS = "close_friends"
    ANY_TIME = "any_time"
    AFTER_ABSENCE = "after_absence"
    LATE_NIGHT = "late_night"
    MILESTONE = "milestone"


@dataclass
class DuckQuestion:
    """A question the duck can ask the player."""
    id: str
    text: str
    category: QuestionCategory
    timing: QuestionTiming
    follow_ups: List[str] = field(default_factory=list)
    extracts_fact: Optional[str] = None  # What fact to extract from answer
    asked: bool = False
    answer: Optional[str] = None
    asked_at: Optional[str] = None
    callback_text: Optional[str] = None  # What to say when referencing answer


# Master question library
DUCK_QUESTIONS: Dict[str, DuckQuestion] = {
    # ========== INTRODUCTION ==========
    "name": DuckQuestion(
        id="name",
        text="So. What do they call you? Besides 'the one who feeds the duck'.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.FIRST_MEETING,
        extracts_fact="name",
        follow_ups=[
            "Interesting name. I'll try to remember it. I probably will.",
            "Hmm. That's a name. You're stuck with it, I suppose.",
        ],
        callback_text="I remember your name. {value}. I didn't forget."
    ),
    
    "why_here": DuckQuestion(
        id="why_here",
        text="I've been wondering. Why did you come here? To a duck. In a pond.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        follow_ups=[
            "That's... surprisingly honest. I appreciate that. Probably.",
            "Interesting. I'm still figuring out why I'm here too.",
        ]
    ),
    
    # ========== PREFERENCES ==========
    "favorite_food": DuckQuestion(
        id="favorite_food",
        text="What's your favorite food? I'm asking for research purposes. Not to judge. Much.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        extracts_fact="favorite_food",
        follow_ups=[
            "Not bread? That's... unexpected. But I'll allow it.",
            "I've noted that. It might come up again. You've been warned.",
        ],
        callback_text="You told me once that you liked {value}. I still think about that sometimes."
    ),
    
    "favorite_color": DuckQuestion(
        id="favorite_color",
        text="Do you have a favorite color? I'm partial to yellow, obviously. It's my color.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        extracts_fact="favorite_color",
        follow_ups=[
            "A fine choice. Not as good as yellow, but respectable.",
            "I'll remember that. For reasons that will become apparent later. Or not.",
        ],
        callback_text="Your favorite color was {value}, wasn't it? I remember."
    ),
    
    "pets": DuckQuestion(
        id="pets",
        text="Do you have other... companions? Other animals you visit? Should I be jealous?",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        extracts_fact="has_other_pets",
        follow_ups=[
            "I see. I'm trying not to feel replaced. It's going moderately well.",
            "No others? I'm your only animal friend? That's... a lot of pressure, actually.",
        ],
        callback_text="You mentioned having other pets. I hope I'm still your favorite duck. I'm your only duck. That should count."
    ),
    
    # ========== PERSONAL ==========
    "what_do": DuckQuestion(
        id="what_do",
        text="What do you do? When you're not here, I mean. You have a life out there, presumably.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="occupation",
        follow_ups=[
            "That sounds... complicated. I just float. It's simpler.",
            "Interesting. My job is being a duck. Less paperwork.",
        ],
        callback_text="You work as {value}, right? I remember. I wonder what that's like."
    ),
    
    "live_alone": DuckQuestion(
        id="live_alone",
        text="Do you live alone? Or are there others? I'm curious about your... ecosystem.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I see. I live alone too. Well, not alone. There are fish. We don't talk much.",
            "That sounds... either nice or chaotic. I'm not sure which.",
        ]
    ),
    
    "hobbies": DuckQuestion(
        id="hobbies",
        text="What do you do for fun? Besides visiting ducks. Which I assume is your primary hobby now.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="hobby",
        follow_ups=[
            "That's more interesting than floating. Maybe. Floating is pretty good.",
            "I'll keep that in mind. In case I ever need to make small talk. Which I won't. But still.",
        ],
        callback_text="You enjoy {value}, don't you? You mentioned it once. I was listening."
    ),
    
    # ========== PHILOSOPHICAL ==========
    "meaning": DuckQuestion(
        id="meaning",
        text="What do you think is the meaning of all this? Life, I mean. Not the pond specifically.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Hmm. That's a better answer than I had. I was going to say 'bread'.",
            "Deep. I'm just a duck, but that resonated. In a duck way.",
        ]
    ),
    
    "happy": DuckQuestion(
        id="happy",
        text="Are you happy? Generally speaking? It's okay if you don't know. I'm not sure either.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I understand. Happiness is complicated. I settle for 'not actively distressed'.",
            "That's honest. I appreciate honest. It's rare.",
        ]
    ),
    
    "regrets": DuckQuestion(
        id="regrets",
        text="Do you have regrets? Things you wish you'd done differently? I have a few. Mostly about bread choices.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Regrets are heavy. For a duck, the heaviest thing I carry is water in my feathers. But I understand.",
            "That's very... human. I regret nothing. Ducks don't have the capacity. Lucky us.",
        ]
    ),
    
    # ========== FEELINGS ==========
    "feeling_now": DuckQuestion(
        id="feeling_now",
        text="How are you feeling? Actually feeling? Not the polite answer. The real one.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Thank you for being honest. I'm... here if you need to talk. To a duck. About things.",
            "That's valid. Feelings are complicated. I mostly feel 'duck'. It's simpler.",
        ]
    ),
    
    "stressed": DuckQuestion(
        id="stressed",
        text="You seem... different today. Stressed, maybe? I can tell. I'm perceptive for a waterfowl.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "The pond doesn't have stress. You could float here a while. It helps. Probably.",
            "I understand. Life is... a lot. Even from a duck's perspective.",
        ]
    ),
    
    # ========== OPINIONS ==========
    "ducks": DuckQuestion(
        id="ducks",
        text="What did you think about ducks? Before you met me, I mean. Be honest.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        follow_ups=[
            "And now? Have I changed your opinion? For better or worse? I need to know.",
            "Interesting. I had no opinions about you before we met either. We're even.",
        ]
    ),
    
    "best_quality": DuckQuestion(
        id="best_quality",
        text="What's your best quality? The thing you like most about yourself? Don't be modest. I'm genuinely curious.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I see that in you. I've observed it. I observe everything.",
            "That's a good quality. Better than my best quality, which is 'floating'. And bread-eating.",
        ]
    ),
    
    # ========== HYPOTHETICAL ==========
    "power": DuckQuestion(
        id="power",
        text="If you could have any power, what would it be? I'd choose infinite bread. But that's me.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Interesting choice. More interesting than bread. But bread is reliable.",
            "I'll remember that. In case a wizard asks. You never know.",
        ]
    ),
    
    "duck_life": DuckQuestion(
        id="duck_life",
        text="If you were a duck for a day, what would you do? Hypothetically. This isn't a trap.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's... actually a good answer. You'd make a decent duck. High praise.",
            "Interesting. I do that every day. It's less exciting than it sounds.",
        ]
    ),
    
    # ========== MEMORIES ==========
    "childhood": DuckQuestion(
        id="childhood",
        text="What's your earliest memory? I was a duckling. It was very yellow. That's all I remember.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... a nice memory. Or a complicated one. Either way, thank you for sharing.",
            "Memories are strange. They stay with us. Like pond water in feathers.",
        ]
    ),
    
    "best_day": DuckQuestion(
        id="best_day",
        text="What's the best day you ever had? I'm curious what makes a good day for you.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds... actually nice. My best day involved finding extra bread. Priorities.",
            "I hope you have more days like that. Even if I'm not there. Which I won't be. I'm a duck.",
        ]
    ),
    
    # ========== HABITS ==========
    "morning_routine": DuckQuestion(
        id="morning_routine",
        text="What's the first thing you do when you wake up? I flap. Then I contemplate existence. Then bread.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's more structured than my routine. I respect it.",
            "Interesting. I'll think about that next time I'm floating at dawn.",
        ]
    ),
    
    "sleep": DuckQuestion(
        id="sleep",
        text="Do you sleep well? I'm asking because I noticed you visit at strange hours. Sometimes.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Sleep is important. Even for ducks. I tuck my head under my wing. It's cozy.",
            "I understand. The pond is quiet at night. You're welcome here. Any hour.",
        ]
    ),
    
    # ========== RELATIONSHIP ==========
    "why_come_back": DuckQuestion(
        id="why_come_back",
        text="Why do you keep coming back? Genuine question. I'm a duck. There must be better options.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's... nicer than I expected. I'm not sure how to react. *shuffles feathers*",
            "I see. Well. You're welcome here. Always. That's not something I say lightly.",
        ]
    ),
    
    "me_honest": DuckQuestion(
        id="me_honest",
        text="What do you honestly think of me? Good, bad, I can take it. I'm a duck. We're resilient.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I... thank you. That means something. Don't tell anyone I said that.",
            "I appreciate your honesty. I feel similarly. About you. There. I said it.",
        ]
    ),
    
    # ========== SILLY ==========
    "superpower_vegetable": DuckQuestion(
        id="superpower_vegetable",
        text="If vegetables had superpowers, which vegetable would be the most dangerous? This is important.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I agree. That vegetable is not to be trusted.",
            "Interesting choice. I was thinking carrots. They see in the dark. Suspicious.",
        ]
    ),
    
    "moon_cheese": DuckQuestion(
        id="moon_cheese",
        text="Do you think the moon is made of cheese? I'm named Cheese. This could be personal.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "A reasonable answer. The moon remains mysterious.",
            "I like that answer. We should discuss more celestial dairy products sometime.",
        ]
    ),
    
    # ========== AFTER ABSENCE ==========
    "where_were_you": DuckQuestion(
        id="where_were_you",
        text="Where were you? You were gone a while. I'm not upset. Just... curious. Very curious.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.AFTER_ABSENCE,
        follow_ups=[
            "I see. Life happened. It does that. The pond was quiet.",
            "That's fair. You have a life out there. I just float here. Waiting.",
        ]
    ),
    
    # ========== LATE NIGHT ==========
    "cant_sleep": DuckQuestion(
        id="cant_sleep",
        text="It's late. You're here instead of sleeping. Can't sleep? Or don't want to?",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "The night is strange. Things feel different. I understand coming here.",
            "I'm here too. Obviously. If you need company at this hour, I'm... available. For talking.",
        ]
    ),
}


class QuestionManager:
    """
    Manages the duck's questions to the player.
    
    Tracks what's been asked, respects cooldowns, and generates
    contextually appropriate questions based on relationship level,
    time of day, and conversation history.
    """
    
    def __init__(self):
        # Track asked questions
        self.asked_questions: Dict[str, Dict] = {}  # question_id -> {asked_at, answer, etc.}
        
        # Cooldowns
        self.category_cooldowns: Dict[str, str] = {}  # category -> last_asked timestamp
        self.general_cooldown_until: Optional[str] = None
        
        # Queue of questions to ask
        self.question_queue: List[str] = []
        
        # Questions per session limit
        self.questions_this_session: int = 0
        self.max_questions_per_session: int = 3
        
        # Statistics
        self.total_questions_asked: int = 0
        self.total_answers_received: int = 0
    
    def get_next_question(self, 
                          relationship_level: str,
                          time_of_day: str,
                          hours_since_last_visit: float = 0,
                          player_model = None,
                          force: bool = False) -> Optional[DuckQuestion]:
        """
        Get the next appropriate question to ask.
        
        Args:
            relationship_level: stranger/acquaintance/friend/best_friend/bonded
            time_of_day: morning/afternoon/evening/night
            hours_since_last_visit: Hours since player was last here
            player_model: PlayerModel for context
            force: Skip cooldowns and limits
        
        Returns:
            DuckQuestion if appropriate, None otherwise
        """
        if not force:
            # Check session limit
            if self.questions_this_session >= self.max_questions_per_session:
                return None
            
            # Check general cooldown
            if self.general_cooldown_until:
                try:
                    cooldown_end = datetime.fromisoformat(self.general_cooldown_until)
                    if datetime.now() < cooldown_end:
                        return None
                except (ValueError, TypeError):
                    pass
        
        # Determine appropriate timing
        timing_filter = [QuestionTiming.ANY_TIME]
        
        if relationship_level == "stranger":
            timing_filter.append(QuestionTiming.FIRST_MEETING)
        elif relationship_level in ["stranger", "acquaintance"]:
            timing_filter.append(QuestionTiming.EARLY_RELATIONSHIP)
        elif relationship_level in ["friend", "best_friend"]:
            timing_filter.append(QuestionTiming.ESTABLISHED)
        if relationship_level in ["best_friend", "bonded"]:
            timing_filter.append(QuestionTiming.CLOSE_FRIENDS)
        
        if hours_since_last_visit > 48:
            timing_filter.append(QuestionTiming.AFTER_ABSENCE)
        
        if time_of_day == "night":
            timing_filter.append(QuestionTiming.LATE_NIGHT)
        
        # Find eligible questions
        eligible = []
        for qid, question in DUCK_QUESTIONS.items():
            # Skip if already asked
            if qid in self.asked_questions:
                continue
            
            # Check timing
            if question.timing not in timing_filter:
                continue
            
            # Check category cooldown
            cat_str = question.category.value
            if cat_str in self.category_cooldowns:
                try:
                    last_asked = datetime.fromisoformat(self.category_cooldowns[cat_str])
                    if (datetime.now() - last_asked).total_seconds() < 3600:  # 1 hour cooldown
                        continue
                except (ValueError, TypeError):
                    pass
            
            eligible.append(question)
        
        if not eligible:
            return None
        
        # Prioritize certain categories based on context
        weighted = []
        for q in eligible:
            weight = 1.0
            
            # Boost introduction questions early
            if q.category == QuestionCategory.INTRODUCTION and self.total_questions_asked < 5:
                weight = 3.0
            
            # Boost feeling questions if player visits late at night
            if q.category == QuestionCategory.FEELINGS and time_of_day == "night":
                weight = 2.0
            
            # Boost after-absence questions
            if q.timing == QuestionTiming.AFTER_ABSENCE and hours_since_last_visit > 48:
                weight = 3.0
            
            # Slight randomness
            weight *= random.uniform(0.8, 1.2)
            
            weighted.append((weight, q))
        
        weighted.sort(key=lambda x: x[0], reverse=True)
        return weighted[0][1]
    
    def record_question_asked(self, question_id: str):
        """Record that a question was asked."""
        if question_id not in DUCK_QUESTIONS:
            return
        
        question = DUCK_QUESTIONS[question_id]
        now = datetime.now()
        
        self.asked_questions[question_id] = {
            "asked_at": now.isoformat(),
            "category": question.category.value,
            "answer": None,
            "answered_at": None
        }
        
        # Update cooldowns
        self.category_cooldowns[question.category.value] = now.isoformat()
        self.general_cooldown_until = (now + timedelta(minutes=5)).isoformat()
        
        # Update counters
        self.questions_this_session += 1
        self.total_questions_asked += 1
    
    def record_answer(self, question_id: str, answer: str) -> Optional[str]:
        """
        Record the player's answer to a question.
        
        Returns the follow-up response if available.
        """
        if question_id not in self.asked_questions:
            return None
        
        if question_id not in DUCK_QUESTIONS:
            return None
        
        question = DUCK_QUESTIONS[question_id]
        now = datetime.now()
        
        self.asked_questions[question_id]["answer"] = answer
        self.asked_questions[question_id]["answered_at"] = now.isoformat()
        
        self.total_answers_received += 1
        
        # Return a follow-up if available
        if question.follow_ups:
            return random.choice(question.follow_ups)
        return None
    
    def get_callback(self, player_model = None) -> Optional[Tuple[str, str]]:
        """
        Get a callback to a previous answer.
        
        Returns (callback_text, original_answer) if available.
        """
        # Find answered questions with callback text
        callbacks = []
        for qid, data in self.asked_questions.items():
            if not data.get("answer"):
                continue
            
            if qid not in DUCK_QUESTIONS:
                continue
            
            question = DUCK_QUESTIONS[qid]
            if not question.callback_text:
                continue
            
            callbacks.append((question, data))
        
        if not callbacks:
            return None
        
        # Pick a random one
        question, data = random.choice(callbacks)
        
        # Format the callback
        callback = question.callback_text
        if "{value}" in callback:
            callback = callback.replace("{value}", data["answer"])
        
        return callback, data["answer"]
    
    def reset_session(self):
        """Reset session-specific counters."""
        self.questions_this_session = 0
    
    def get_unanswered_questions(self) -> List[str]:
        """Get list of questions asked but not answered."""
        unanswered = []
        for qid, data in self.asked_questions.items():
            if data.get("answer") is None:
                unanswered.append(qid)
        return unanswered
    
    def get_extracted_facts(self) -> Dict[str, str]:
        """Get facts extracted from answered questions."""
        facts = {}
        for qid, data in self.asked_questions.items():
            if not data.get("answer"):
                continue
            
            if qid in DUCK_QUESTIONS:
                question = DUCK_QUESTIONS[qid]
                if question.extracts_fact:
                    facts[question.extracts_fact] = data["answer"]
        
        return facts
    
    def to_dict(self) -> Dict:
        """Serialize for persistence."""
        return {
            "asked_questions": self.asked_questions,
            "category_cooldowns": self.category_cooldowns,
            "general_cooldown_until": self.general_cooldown_until,
            "question_queue": self.question_queue,
            "total_questions_asked": self.total_questions_asked,
            "total_answers_received": self.total_answers_received
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "QuestionManager":
        """Deserialize from persistence."""
        manager = cls()
        manager.asked_questions = data.get("asked_questions", {})
        manager.category_cooldowns = data.get("category_cooldowns", {})
        manager.general_cooldown_until = data.get("general_cooldown_until")
        manager.question_queue = data.get("question_queue", [])
        manager.total_questions_asked = data.get("total_questions_asked", 0)
        manager.total_answers_received = data.get("total_answers_received", 0)
        return manager


def generate_callback_dialogue(question_id: str, answer: str) -> str:
    """Generate dialogue that callbacks to a previous answer."""
    if question_id not in DUCK_QUESTIONS:
        return f"You told me something once. I remember. '{answer[:50]}...'"
    
    question = DUCK_QUESTIONS[question_id]
    
    if question.callback_text:
        return question.callback_text.replace("{value}", answer)
    
    # Generic callbacks based on category
    category_callbacks = {
        QuestionCategory.PREFERENCES: [
            f"You mentioned you liked {answer}. I remember these things.",
            f"Ah, {answer}. You told me about that. I was listening.",
        ],
        QuestionCategory.PERSONAL: [
            f"You told me about {answer}. I think about that sometimes.",
            f"I remember when you mentioned {answer}. Details stick with me.",
        ],
        QuestionCategory.FEELINGS: [
            f"You shared how you felt once. About {answer}. I haven't forgotten.",
            f"I recall you opening up about {answer}. That meant something.",
        ],
    }
    
    callbacks = category_callbacks.get(question.category, [
        f"You told me: '{answer[:40]}...' I remember.",
    ])
    
    return random.choice(callbacks)
