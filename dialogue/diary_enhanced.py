"""
Enhanced Diary System - Extends the base diary with more features.
Adds emotional tracking, photo attachments, prompts, and deeper narrative.
"""
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class EmotionCategory(Enum):
    """Categories of emotions for tracking."""
    JOY = "joy"
    SADNESS = "sadness"
    EXCITEMENT = "excitement"
    CALM = "calm"
    ANXIETY = "anxiety"
    LOVE = "love"
    CURIOSITY = "curiosity"
    CONTENTMENT = "contentment"


class DiaryPromptType(Enum):
    """Types of diary writing prompts."""
    REFLECTION = "reflection"
    GRATITUDE = "gratitude"
    DREAM = "dream"
    GOAL = "goal"
    MEMORY = "memory"
    LETTER = "letter"
    WISHLIST = "wishlist"


class PhotoType(Enum):
    """Types of diary photos (ASCII representations)."""
    SELFIE = "selfie"
    SCENERY = "scenery"
    FRIEND = "friend"
    FOOD = "food"
    ADVENTURE = "adventure"
    COZY = "cozy"
    SILLY = "silly"


@dataclass
class EmotionLog:
    """A logged emotion moment."""
    emotion: EmotionCategory
    intensity: int  # 1-10
    timestamp: str
    trigger: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class DiaryPhoto:
    """An ASCII photo in the diary."""
    photo_id: str
    photo_type: PhotoType
    ascii_art: List[str]
    caption: str
    date_taken: str
    location: Optional[str] = None
    mood: Optional[str] = None


@dataclass
class DiaryPrompt:
    """A writing prompt for the diary."""
    prompt_id: str
    prompt_type: DiaryPromptType
    question: str
    response: Optional[str] = None
    date_answered: Optional[str] = None


@dataclass
class LifeChapter:
    """A chapter in the duck's life story."""
    chapter_id: str
    title: str
    start_date: str
    summary: str
    key_events: List[str]
    dominant_mood: str
    end_date: Optional[str] = None


@dataclass
class DreamLog:
    """A recorded dream."""
    dream_id: str
    date: str
    title: str
    description: str
    symbols: List[str]
    interpretation: Optional[str] = None
    recurring: bool = False


# ASCII photo templates
PHOTO_TEMPLATES = {
    PhotoType.SELFIE: [
        [
            "  +---------+  ",
            "  |  [#]     |  ",
            "  |   d    |  ",
            "  |  *pose* |  ",
            "  +---------+  ",
        ],
        [
            "  +=========+  ",
            "  | SELFIE! |  ",
            "  |   *d*  |  ",
            "  |  smile! |  ",
            "  +=========+  ",
        ],
    ],
    PhotoType.SCENERY: [
        [
            "  +---------+  ",
            "  | (*)  *  |  ",
            "  |  /\\A  |  ",
            "  |d ~~~   |  ",
            "  +---------+  ",
        ],
        [
            "  +=========+  ",
            "  |  -*-     |  ",
            "  |  ~~~  |  ",
            "  |    d   |  ",
            "  +=========+  ",
        ],
    ],
    PhotoType.FRIEND: [
        [
            "  +---------+  ",
            "  | FRIENDS |  ",
            "  | d  d  |  ",
            "  |  <3 BFF <3 |  ",
            "  +---------+  ",
        ],
    ],
    PhotoType.FOOD: [
        [
            "  +---------+  ",
            "  |  YUM!   |  ",
            "  |  BW   |  ",
            "  | d *nom* |  ",
            "  +---------+  ",
        ],
    ],
    PhotoType.ADVENTURE: [
        [
            "  +---------+  ",
            "  |ADVENTURE|  ",
            "  | [?]  (+)  |  ",
            "  |  d->->   |  ",
            "  +---------+  ",
        ],
    ],
    PhotoType.COZY: [
        [
            "  +---------+  ",
            "  |  COZY   |  ",
            "  | c S   |  ",
            "  |   dz  |  ",
            "  +---------+  ",
        ],
    ],
    PhotoType.SILLY: [
        [
            "  +---------+  ",
            "  | DERP!   |  ",
            "  |   @_@   |  ",
            "  |   d    |  ",
            "  +---------+  ",
        ],
    ],
}

# Writing prompts
DIARY_PROMPTS = {
    DiaryPromptType.REFLECTION: [
        "What made today special?",
        "What did you learn today?",
        "How have you grown this week?",
        "What challenges did you face today?",
        "What are you proud of right now?",
        "What surprised you about yourself today?",
        "What would you do differently if you could redo today?",
        "What moment from today will you remember?",
        "What was the hardest part of your day?",
        "How are you different from who you were a month ago?",
        "What did you notice that you usually overlook?",
        "What thought kept coming back to you today?",
        "What did you do today that your past self would be proud of?",
        "What's one thing you understood today that you didn't yesterday?",
        "What part of today felt most like 'you'?",
        "What did you avoid today, and why?",
        "What would today look like if you described it to a stranger?",
        "What's one thing that went differently than you expected?",
        "If today were a chapter in a book, what would the title be?",
        "What conversation—real or imagined—occupied your mind today?",
        "What's something you said today that you actually meant?",
        "What would today look like from someone else's perspective?",
        "What pattern in your life are you just now noticing?",
        "What did you do on autopilot today that deserves more attention?",
        "What feeling did you push away today instead of sitting with?",
        "What's one thing you did today just because you wanted to?",
        "What would you tell yourself at the start of today, knowing how it ended?",
    ],
    DiaryPromptType.GRATITUDE: [
        "What are three things you're grateful for?",
        "Who made you smile today?",
        "What small joy did you experience?",
        "What comfort do you appreciate most?",
        "What about your home makes you happy?",
        "What food are you thankful for today? (Bread is always acceptable.)",
        "What sound made you feel peaceful?",
        "Who do you wish you could thank right now?",
        "What part of your routine do you secretly love?",
        "What's something you take for granted that's actually amazing?",
        "What made you feel safe today?",
        "What's one thing about your pond that you'd miss if it were gone?",
        "What's the most reliable thing in your life right now?",
        "Who showed up for you recently without being asked?",
        "What ability do you have that you're thankful for?",
        "What moment today would you save in a jar if you could?",
        "What's something boring that you're secretly grateful for?",
        "What comfort did you not appreciate until now?",
        "What's one thing about today's weather that was actually kind of nice?",
        "Who in your life asks nothing of you but still shows up?",
        "What's a food you had today that you're glad exists?",
        "What's something your body did today without you even thinking about it?",
        "What problem do you NOT have right now that you're thankful for?",
        "What's a sound you heard today that made the world feel okay?",
        "What's something free that brought you joy today?",
        "What part of your routine secretly makes you feel safe?",
        "What's a texture that makes you feel calm?",
        "What's something you saw today that you're glad you noticed?",
        "What's one thing that worked today without you having to try?",
        "Who makes your world smaller in a good way?",
        "What did the weather do for you today, even if it wasn't trying?",
        "What's a skill you have that you forget to appreciate?",
        "What's something ugly or imperfect that you love anyway?",
        # ── Round 3: More gratitude prompts ────────────────────────────
        "What's a sound you heard today that you're glad exists?",
        "What part of your body worked well today without you asking it to?",
        "What's a boring thing in your life that's actually a luxury?",
        "Who's someone you've never thanked but should?",
        "What mistake are you grateful for because of where it led?",
        "What's something you use every day that someone else made with care?",
        "What's a view you see so often you've stopped appreciating it?",
        "What did the world give you today that it didn't have to?",
    ],
    DiaryPromptType.DREAM: [
        "If you could go anywhere, where would it be?",
        "What's your biggest dream?",
        "If you could fly, where would you go first?",
        "What would your perfect day look like?",
        "If you could meet anyone, who would it be?",
        "If you woke up in a different body, what would you do first?",
        "What does your ideal pond look like?",
        "If you could talk to any animal, which one?",
        "What would you build if you had unlimited resources?",
        "If time stopped for everyone but you, what would you do?",
        "What world from a story would you want to visit?",
        "If you could have any superpower, what would you choose and why?",
        "What would your life look like if you had zero fear?",
        "If you could live in any time period, which one?",
        "What would you do with an entire day where nothing could go wrong?",
        "If you could send a message to every duck in the world, what would it say?",
        "If the pond had no edges, where would you float to first?",
        "What impossible thing do you secretly believe might happen someday?",
        "If you could wake up tomorrow with one new ability, what would it be?",
        "What does your perfect morning look like, down to every detail?",
        "If the pond had no limits, what would you build beside it?",
        "What would you do if you were invisible for one day?",
        "If you could live inside any dream you've had, which one?",
        "What's a place that doesn't exist that you wish did?",
        "If you could give one gift to every duck in the world, what would it be?",
        "What would your life look like if every day were exactly like your best day?",
        "If you could have a conversation with any version of yourself, which age?",
        "What would you create if you had no fear of failure?",
        "If you could redesign the pond from scratch, what would it include?",
        "What adventure would you go on if someone else handled the scary parts?",
        "If you could bottle a moment and open it whenever you wanted, which moment?",
        "What would your dream day smell like?",
        "If the stars rearranged into a message just for you, what would it say?",
    ],
    DiaryPromptType.GOAL: [
        "What do you want to achieve this week?",
        "What new thing do you want to try?",
        "How do you want to grow?",
        "What skill do you want to improve?",
        "What habit do you want to build?",
        "What fear do you want to face?",
        "What relationship do you want to strengthen?",
        "What bad habit do you want to leave behind?",
        "What would make you prouder of yourself?",
        "What's one small step you can take tomorrow?",
        "What would you attempt if you knew no one was watching?",
        "What do you want to be known for?",
        "What's one thing you keep putting off that would make life better?",
        "What boundary do you want to set this week?",
        "What's something you want to try even though it might not work?",
        "What would make you proud of this week when it's over?",
        "What conversation are you avoiding that might make things better?",
        "What's one thing you could stop doing that would improve your life?",
        "What would you practice every day if you knew it would pay off?",
        "What's the smallest possible step toward something you want?",
        "What would you do more of if nobody judged you?",
        "What's a compliment you want to be true that isn't yet?",
        "What are you tolerating that you could actually change?",
        "What would make you feel braver tomorrow?",
        "What would you do differently if you cared less about what others think?",
        "What relationship in your life needs the most attention right now?",
        "What's one thing you could forgive yourself for this week?",
        "What area of your life are you coasting in that deserves real effort?",
        "What would your life look like with one more hour in the day?",
        "What skill would future-you be glad you started learning today?",
        "What's one promise you want to make to yourself and actually keep?",
        # ── Round 3: More goal prompts ─────────────────────────────────
        "What would you build if you had unlimited time?",
        "What's a habit you admire in someone else that you want to adopt?",
        "What scares you just enough to be exciting?",
        "What would you do more of if you trusted yourself more?",
        "What part of your routine deserves an upgrade?",
        "What would your life look like in a year if everything went well?",
        "What kindness do you want to practice more?",
        "What do you keep almost doing that you should just do?",
    ],
    DiaryPromptType.MEMORY: [
        "What's your earliest happy memory?",
        "What's the best day you remember?",
        "What's a funny moment you'll never forget?",
        "What's the kindest thing anyone did for you?",
        "What adventure do you remember most?",
        "What smell brings back a strong memory?",
        "What's a memory that still makes you laugh?",
        "What's a moment you wish you could relive?",
        "What's the bravest thing you ever did?",
        "What memory do you think about before falling asleep?",
        "What's a small moment that turned out to matter a lot?",
        "What's the most peaceful moment you can remember?",
        "What's a memory that always makes you feel warm inside?",
        "When was the last time you were truly surprised?",
        "What's a moment where everything felt exactly right?",
        "What sound from the past do you still hear sometimes?",
        "What's a memory you'd want to show someone who doesn't know you?",
        "What's the most ordinary moment that turned out to matter?",
        "What's a meal you remember not because of the food but because of the company?",
        "What's the youngest memory you can access?",
        "What's a place you used to go that you can't go back to?",
        "What's something someone said to you years ago that you still carry?",
        "When was the last time you laughed so hard it hurt?",
        "What's a scent that unlocks a specific moment in your past?",
        "What's a goodbye you still think about?",
        "What's a taste that takes you back to a specific time and place?",
        "What's a moment of courage you had that nobody else knows about?",
        "When was the last time you felt completely safe?",
        "What's a conversation you replay in your mind sometimes?",
        "What memory makes you proud of who you used to be?",
        "What's the most beautiful thing you've ever seen, and where were you?",
        "What's a promise someone kept that meant more than they knew?",
    ],
    DiaryPromptType.LETTER: [
        "Write a letter to your future self.",
        "Write a thank you note to your human.",
        "Write a letter to your past self.",
        "Write a note to a friend.",
        "Write about why you matter.",
        "Write a letter to someone you miss.",
        "Write a letter to the pond.",
        "Write a note you'd want to find in a bottle.",
        "Write to the person you want to become.",
        "Write a letter forgiving yourself for something.",
        "Write a letter to the version of you that was having the worst day.",
        "Write a thank-you note to someone who'll never read it.",
        "Write a note to the next duck who'll live at this pond.",
        "Write a letter to the sky. Tell it what you think of its work.",
        "Write a letter to bread. Be honest about your feelings.",
        "Write to someone you argued with. Say what you wish you'd said.",
        "Write a letter to the rain. Thank it or complain. Your choice.",
        "Write a letter to your favorite food. Be honest about the relationship.",
        "Write a note to yourself for the next bad day.",
        "Write a letter to someone you've never met but think about sometimes.",
        "Write to the moon. Ask it something you've always wondered.",
        "Write a letter to the version of you that exists in other people's memories.",
        "Write a letter to silence. Tell it what you hear when it's around.",
        "Write a thank-you note to your pond. List what it's given you.",
        "Write a letter to the first friend you ever made.",
        "Write a message to the duck you'll be in a year.",
        "Write a letter to your fear. Tell it you see it.",
        "Write to the wind. Ask it where it's been.",
        "Write a letter to yesterday. Tell it what it missed.",
        "Write a note to your future self about what matters right now.",
    ],
    DiaryPromptType.WISHLIST: [
        "What three wishes would you make?",
        "What would you put on your bucket list?",
        "What experiences do you want to have?",
        "What would make next month amazing?",
        "What do you hope for?",
        "What would you wish for someone you love?",
        "If you could change one thing about the world, what?",
        "What invention do you wish existed?",
        "What's on your dream menu? (Bread doesn't count. Just kidding. Bread always counts.)",
        "What would you do if you knew you couldn't fail?",
        "What would you add to the pond if you could add anything?",
        "If you could relive one perfect day, which would it be?",
        "What do you wish someone would say to you right now?",
        "What's one thing you wish you could tell every duckling?",
        "If you had a magic quack that granted one wish, what would you quack for?",
        "What would make tomorrow the best day of your life?",
        "What's something you'd love to try but haven't had the courage?",
        "What would you add to the world if you could add anything at all?",
        "What's a sound you wish you could hear right now?",
        "If you could bottle one feeling and keep it forever, which feeling?",
        "What's one thing you'd want every duck to experience at least once?",
        "What would the perfect gift for you look like?",
        "If tomorrow could be any kind of day, what kind would you pick?",
        "What's something that doesn't exist yet but absolutely should?",
        "What would you ask for if you knew the answer would be yes?",
        "What experience do you keep postponing that you should just do?",
        "What would your perfect shelter look like?",
        "If you could master one thing overnight, what would it be?",
        "What's a place you've imagined but never been to?",
        "What conversation do you wish you could have?",
        "What would you grow in a magic garden?",
    ],
}

# Dream symbols and interpretations
DREAM_SYMBOLS = {
    "bread": "Nourishment and comfort await",
    "water": "Emotional depth and cleansing",
    "flying": "Freedom and new perspectives",
    "pond": "Reflection and inner peace",
    "human": "Connection and trust",
    "storm": "Challenges to overcome",
    "sunshine": "Joy and optimism",
    "feathers": "Identity and self-expression",
    "nest": "Home and security",
    "stars": "Guidance and hope",
    "rainbow": "Promise and wonder",
    "darkness": "The unknown, potential growth",
    "garden": "Growth and nurturing",
    "treasure": "Hidden potential and discovery",
    "friend": "Companionship and belonging",
    "moon": "Intuition and hidden knowledge",
    "fish": "Abundance and the unconscious",
    "egg": "New beginnings and potential",
    "forest": "Exploration of the self",
    "mirror": "Self-reflection and truth",
    "door": "Opportunity and transition",
    "clock": "Awareness of time passing",
    "snow": "Purity and fresh starts",
    "fire": "Passion and transformation",
    "bridge": "Connection between states of being",
    "mountain": "Challenges to overcome and ambitions to pursue",
    "river": "Flow of time and journey of life",
    "cave": "Unexplored parts of the self",
    "stone": "Stability, patience, and endurance",
    "sand": "Impermanence and the passage of time",
    "rain": "Cleansing, renewal, and emotional release",
    "wind": "Change approaching and unseen forces",
    "leaf": "Letting go and natural cycles",
    "tree": "Growth, roots, and stability",
    "island": "Solitude and self-sufficiency",
    "key": "Solutions waiting to be discovered",
    "book": "Knowledge and stories yet to unfold",
    "candle": "Hope in small but persistent form",
    "path": "Choices ahead and directions to take",
    "bell": "Awakening and moments of clarity",
    "shadow": "Parts of the self yet to be understood",
    "music": "Harmony and emotional expression",
    "feather": "Lightness, freedom, and identity",
    "wave": "Emotional ups and downs, rhythm of life",
    "fog": "Uncertainty but also possibility hidden from view",
    "ladder": "Ambition and the willingness to climb toward something",
    "anchor": "What keeps you grounded and steady",
    "map": "Direction and the desire to understand where you're going",
    "sunrise": "New beginnings and hope returning",
    "sunset": "Completion and the beauty of endings",
    "root": "Where you come from and what feeds you",
    "shell": "Protection and the beauty of vulnerability",
    "tide": "Forces larger than yourself that you can ride but not control",
    "seed": "Potential waiting for the right conditions",
    "web": "Connections between things that seem separate",
    "nest": "Safety built by your own effort",
    "horizon": "The edge of what you know and the beginning of what you don't",
    "echo": "The past repeating in the present",
    "lantern": "Guidance you carry with you",
    "frost": "Temporary hardship that reveals beauty",
    "harvest": "The result of patience and steady work",
    "storm": "Overwhelming emotions that pass and leave clarity",
    "pebble": "Small things that create large ripples",
}


class EnhancedDiarySystem:
    """Enhanced diary system with emotional tracking and more features."""
    
    def __init__(self):
        self.emotion_logs: List[EmotionLog] = []
        self.photos: List[DiaryPhoto] = []
        self.prompts: List[DiaryPrompt] = []
        self.life_chapters: List[LifeChapter] = []
        self.dream_logs: List[DreamLog] = []
        
        # Tracking
        self.current_chapter: Optional[str] = None
        self.daily_mood_summary: Dict[str, List[str]] = {}  # date -> moods
        self.prompts_completed: int = 0
        self.photos_taken: int = 0
        self.dreams_recorded: int = 0
        
    def log_emotion(self, emotion: EmotionCategory, intensity: int,
                   trigger: Optional[str] = None, notes: Optional[str] = None) -> EmotionLog:
        """Log an emotional moment."""
        log = EmotionLog(
            emotion=emotion,
            intensity=max(1, min(10, intensity)),
            timestamp=datetime.now().isoformat(),
            trigger=trigger,
            notes=notes,
        )
        
        self.emotion_logs.append(log)
        
        # Update daily summary
        today = date.today().isoformat()
        if today not in self.daily_mood_summary:
            self.daily_mood_summary[today] = []
        self.daily_mood_summary[today].append(emotion.value)
        
        # Keep logs manageable
        if len(self.emotion_logs) > 200:
            self.emotion_logs = self.emotion_logs[-200:]
            
        return log
        
    def get_emotion_analysis(self, days: int = 7) -> Dict:
        """Analyze emotions over a period."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [log for log in self.emotion_logs 
                  if datetime.fromisoformat(log.timestamp) > cutoff]
        
        if not recent:
            return {"dominant": None, "variety": 0, "average_intensity": 0}
            
        # Count emotions
        emotion_counts = {}
        total_intensity = 0
        
        for log in recent:
            emotion_counts[log.emotion] = emotion_counts.get(log.emotion, 0) + 1
            total_intensity += log.intensity
            
        dominant = max(emotion_counts.keys(), key=lambda e: emotion_counts[e])
        
        return {
            "dominant": dominant.value,
            "variety": len(emotion_counts),
            "average_intensity": total_intensity / len(recent),
            "total_logs": len(recent),
            "breakdown": {e.value: c for e, c in emotion_counts.items()},
        }
        
    def take_photo(self, photo_type: PhotoType, caption: str,
                  location: Optional[str] = None, mood: Optional[str] = None) -> DiaryPhoto:
        """Take a diary photo."""
        templates = PHOTO_TEMPLATES.get(photo_type, PHOTO_TEMPLATES[PhotoType.SELFIE])
        ascii_art = random.choice(templates)
        
        photo = DiaryPhoto(
            photo_id=f"photo_{self.photos_taken + 1}",
            photo_type=photo_type,
            ascii_art=ascii_art,
            caption=caption,
            date_taken=datetime.now().isoformat(),
            location=location,
            mood=mood,
        )
        
        self.photos.append(photo)
        self.photos_taken += 1
        
        # Keep photos manageable
        if len(self.photos) > 50:
            self.photos = self.photos[-50:]
            
        return photo
        
    def get_random_prompt(self, prompt_type: Optional[DiaryPromptType] = None) -> DiaryPrompt:
        """Get a random writing prompt."""
        if prompt_type:
            prompts = DIARY_PROMPTS.get(prompt_type, [])
        else:
            prompt_type = random.choice(list(DiaryPromptType))
            prompts = DIARY_PROMPTS.get(prompt_type, [])
            
        question = random.choice(prompts) if prompts else "Write about your day."
        
        prompt = DiaryPrompt(
            prompt_id=f"prompt_{len(self.prompts) + 1}",
            prompt_type=prompt_type,
            question=question,
        )
        
        self.prompts.append(prompt)
        return prompt
        
    def answer_prompt(self, prompt_id: str, response: str):
        """Answer a writing prompt."""
        for prompt in self.prompts:
            if prompt.prompt_id == prompt_id:
                prompt.response = response
                prompt.date_answered = datetime.now().isoformat()
                self.prompts_completed += 1
                break
                
    def start_life_chapter(self, title: str, summary: str) -> LifeChapter:
        """Start a new life chapter."""
        # End current chapter if exists
        if self.current_chapter:
            self.end_life_chapter()
            
        chapter = LifeChapter(
            chapter_id=f"chapter_{len(self.life_chapters) + 1}",
            title=title,
            start_date=datetime.now().isoformat(),
            summary=summary,
            key_events=[],
            dominant_mood="hopeful",
        )
        
        self.life_chapters.append(chapter)
        self.current_chapter = chapter.chapter_id
        return chapter
        
    def add_chapter_event(self, event: str):
        """Add an event to the current chapter."""
        if not self.current_chapter:
            return
            
        for chapter in self.life_chapters:
            if chapter.chapter_id == self.current_chapter:
                chapter.key_events.append(event)
                break
                
    def end_life_chapter(self, summary_update: Optional[str] = None):
        """End the current chapter."""
        if not self.current_chapter:
            return
            
        for chapter in self.life_chapters:
            if chapter.chapter_id == self.current_chapter:
                chapter.end_date = datetime.now().isoformat()
                if summary_update:
                    chapter.summary = summary_update
                    
                # Determine dominant mood from recent emotions
                recent_analysis = self.get_emotion_analysis(7)
                if recent_analysis["dominant"]:
                    chapter.dominant_mood = recent_analysis["dominant"]
                break
                
        self.current_chapter = None
        
    def record_dream(self, title: str, description: str,
                    recurring: bool = False) -> DreamLog:
        """Record a dream."""
        # Find symbols in description
        symbols_found = []
        desc_lower = description.lower()
        for symbol in DREAM_SYMBOLS:
            if symbol in desc_lower:
                symbols_found.append(symbol)
                
        # Generate interpretation
        interpretation = None
        if symbols_found:
            interpretations = [DREAM_SYMBOLS[s] for s in symbols_found[:3]]
            interpretation = ". ".join(interpretations) + "."
            
        dream = DreamLog(
            dream_id=f"dream_{self.dreams_recorded + 1}",
            date=datetime.now().isoformat(),
            title=title,
            description=description,
            symbols=symbols_found,
            interpretation=interpretation,
            recurring=recurring,
        )
        
        self.dream_logs.append(dream)
        self.dreams_recorded += 1
        
        # Keep dreams manageable
        if len(self.dream_logs) > 30:
            self.dream_logs = self.dream_logs[-30:]
            
        return dream
        
    def get_mood_calendar(self, month: int, year: int) -> Dict[int, str]:
        """Get mood summary for each day of a month."""
        calendar = {}
        
        for day in range(1, 32):
            try:
                day_date = date(year, month, day).isoformat()
                if day_date in self.daily_mood_summary:
                    moods = self.daily_mood_summary[day_date]
                    # Get most common mood
                    mood_counts = {}
                    for mood in moods:
                        mood_counts[mood] = mood_counts.get(mood, 0) + 1
                    dominant = max(mood_counts.keys(), key=lambda m: mood_counts[m])
                    calendar[day] = dominant
            except ValueError:
                break  # Invalid day for month
                
        return calendar
        
    def generate_weekly_summary(self) -> Dict:
        """Generate a weekly emotional summary."""
        analysis = self.get_emotion_analysis(7)
        
        # Get photos from this week
        week_ago = datetime.now() - timedelta(days=7)
        week_photos = [p for p in self.photos 
                       if datetime.fromisoformat(p.date_taken) > week_ago]
        
        # Get answered prompts
        week_prompts = [p for p in self.prompts if p.date_answered and
                        datetime.fromisoformat(p.date_answered) > week_ago]
        
        return {
            "emotion_analysis": analysis,
            "photos_taken": len(week_photos),
            "prompts_completed": len(week_prompts),
            "highlight_emotion": analysis.get("dominant", "calm"),
            "emotional_variety": analysis.get("variety", 0),
        }
        
    def render_emotion_wheel(self, width: int = 40) -> List[str]:
        """Render an emotion wheel display."""
        lines = []
        
        analysis = self.get_emotion_analysis(7)
        
        lines.append("+" + "=" * (width - 2) + "+")
        lines.append("|" + " * Emotion Wheel * ".center(width - 2) + "|")
        lines.append("+" + "=" * (width - 2) + "+")
        
        emotion_emojis = {
            "joy": ":)",
            "sadness": ":(",
            "excitement": ":D",
            "calm": ":)",
            "anxiety": ":o",
            "love": ":)",
            "curiosity": "o",
            "contentment": ":)️",
        }
        
        breakdown = analysis.get("breakdown", {})
        total = sum(breakdown.values()) if breakdown else 1
        
        for emotion in EmotionCategory:
            count = breakdown.get(emotion.value, 0)
            percentage = (count / total * 100) if total > 0 else 0
            bar_width = int(percentage / 5)  # Max 20 chars
            bar = "█" * bar_width + "." * (20 - bar_width)
            emoji = emotion_emojis.get(emotion.value, "?")
            
            line = f" {emoji} {emotion.value[:8]:8} [{bar}] {percentage:.0f}%"
            lines.append("|" + line[:width-3].ljust(width - 2) + "|")
            
        lines.append("+" + "-" * (width - 2) + "+")
        
        dominant = analysis.get("dominant", "unknown")
        lines.append("|" + f" Dominant mood: {dominant} ".center(width - 2) + "|")
        
        lines.append("+" + "=" * (width - 2) + "+")
        
        return lines
        
    def render_photo_album_page(self, page: int = 0, photos_per_page: int = 2) -> List[str]:
        """Render a page of the photo album."""
        lines = []
        
        start_idx = page * photos_per_page
        page_photos = self.photos[start_idx:start_idx + photos_per_page]
        
        lines.append("+========================================+")
        lines.append("|        [#] Photo Album Page {:02d} [#]        |".format(page + 1))
        lines.append("+========================================+")
        
        if not page_photos:
            lines.append("|         No photos yet!                 |")
            lines.append("|      Take some photos to fill         |")
            lines.append("|          this album! [#]               |")
        else:
            for photo in page_photos:
                lines.append("|                                        |")
                for art_line in photo.ascii_art:
                    lines.append("|" + art_line.center(40) + "|")
                lines.append("|" + f'"{photo.caption}"'.center(40) + "|")
                lines.append("|" + f"- {photo.date_taken[:10]} -".center(40) + "|")
                lines.append("|                                        |")
                
        lines.append("+========================================+")
        
        return lines
        
    def render_dream_journal(self, width: int = 50) -> List[str]:
        """Render the dream journal."""
        lines = []
        
        lines.append("+" + "=" * (width - 2) + "+")
        lines.append("|" + " ) Dream Journal ) ".center(width - 2) + "|")
        lines.append("+" + "=" * (width - 2) + "+")
        
        if not self.dream_logs:
            lines.append("|" + " No dreams recorded yet... ".center(width - 2) + "|")
            lines.append("|" + " Sweet dreams await! z ".center(width - 2) + "|")
        else:
            for dream in self.dream_logs[-3:]:  # Show last 3
                lines.append("|" + f" * {dream.title} * "[:width-3].center(width - 2) + "|")
                lines.append("|" + f"   {dream.date[:10]}"[:width-3].ljust(width - 2) + "|")
                
                desc_preview = dream.description[:width-6] + "..." if len(dream.description) > width-6 else dream.description
                lines.append("|" + f"   {desc_preview}"[:width-3].ljust(width - 2) + "|")
                
                if dream.interpretation:
                    lines.append("|" + f"   -> {dream.interpretation}"[:width-3].ljust(width - 2) + "|")
                    
                lines.append("|" + "-" * (width - 2) + "|")
                
        lines.append("+" + "=" * (width - 2) + "+")
        
        return lines
        
    def render_life_story(self, width: int = 60) -> List[str]:
        """Render the life story timeline."""
        lines = []
        
        lines.append("+" + "=" * (width - 2) + "+")
        lines.append("|" + " [=] Life Story [=] ".center(width - 2) + "|")
        lines.append("+" + "=" * (width - 2) + "+")
        
        if not self.life_chapters:
            lines.append("|" + " Your story is just beginning... ".center(width - 2) + "|")
        else:
            for i, chapter in enumerate(self.life_chapters):
                status = "* Current" if chapter.chapter_id == self.current_chapter else "x Complete"
                lines.append("|" + f" Chapter {i+1}: {chapter.title} "[:width-3].ljust(width - 2) + "|")
                lines.append("|" + f"   {status}"[:width-3].ljust(width - 2) + "|")
                lines.append("|" + f"   {chapter.summary}"[:width-3].ljust(width - 2) + "|")
                
                if chapter.key_events:
                    events_preview = ", ".join(chapter.key_events[:2])
                    lines.append("|" + f"   Events: {events_preview}"[:width-3].ljust(width - 2) + "|")
                    
                lines.append("|" + "|".center(width - 2) + "|")
                
        lines.append("+" + "=" * (width - 2) + "+")
        
        return lines
        
    def to_dict(self) -> Dict:
        """Serialize to dictionary."""
        return {
            "emotion_logs": [
                {
                    "emotion": log.emotion.value,
                    "intensity": log.intensity,
                    "timestamp": log.timestamp,
                    "trigger": log.trigger,
                    "notes": log.notes,
                }
                for log in self.emotion_logs[-100:]  # Keep last 100
            ],
            "photos": [
                {
                    "photo_id": p.photo_id,
                    "photo_type": p.photo_type.value,
                    "ascii_art": p.ascii_art,
                    "caption": p.caption,
                    "date_taken": p.date_taken,
                    "location": p.location,
                    "mood": p.mood,
                }
                for p in self.photos
            ],
            "prompts": [
                {
                    "prompt_id": p.prompt_id,
                    "prompt_type": p.prompt_type.value,
                    "question": p.question,
                    "response": p.response,
                    "date_answered": p.date_answered,
                }
                for p in self.prompts if p.response  # Only save answered
            ],
            "life_chapters": [
                {
                    "chapter_id": c.chapter_id,
                    "title": c.title,
                    "start_date": c.start_date,
                    "end_date": c.end_date,
                    "summary": c.summary,
                    "key_events": c.key_events,
                    "dominant_mood": c.dominant_mood,
                }
                for c in self.life_chapters
            ],
            "dream_logs": [
                {
                    "dream_id": d.dream_id,
                    "date": d.date,
                    "title": d.title,
                    "description": d.description,
                    "symbols": d.symbols,
                    "interpretation": d.interpretation,
                    "recurring": d.recurring,
                }
                for d in self.dream_logs
            ],
            "current_chapter": self.current_chapter,
            "daily_mood_summary": dict(list(self.daily_mood_summary.items())[-30:]),
            "prompts_completed": self.prompts_completed,
            "photos_taken": self.photos_taken,
            "dreams_recorded": self.dreams_recorded,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EnhancedDiarySystem":
        """Deserialize from dictionary."""
        system = cls()
        system.emotion_logs = []
        for log_data in data.get("emotion_logs", []):
            try:
                system.emotion_logs.append(EmotionLog(
                    emotion=EmotionCategory(log_data["emotion"]),
                    intensity=log_data["intensity"],
                    timestamp=log_data["timestamp"],
                    trigger=log_data.get("trigger"),
                    notes=log_data.get("notes"),
                ))
            except (ValueError, KeyError):
                pass
                
        system.photos = []
        for p_data in data.get("photos", []):
            try:
                system.photos.append(DiaryPhoto(
                    photo_id=p_data["photo_id"],
                    photo_type=PhotoType(p_data["photo_type"]),
                    ascii_art=p_data["ascii_art"],
                    caption=p_data["caption"],
                    date_taken=p_data["date_taken"],
                    location=p_data.get("location"),
                    mood=p_data.get("mood"),
                ))
            except (ValueError, KeyError):
                pass
                
        system.prompts = []
        for p_data in data.get("prompts", []):
            try:
                system.prompts.append(DiaryPrompt(
                    prompt_id=p_data["prompt_id"],
                    prompt_type=DiaryPromptType(p_data["prompt_type"]),
                    question=p_data["question"],
                    response=p_data.get("response"),
                    date_answered=p_data.get("date_answered"),
                ))
            except (ValueError, KeyError):
                pass
                
        system.life_chapters = []
        for c_data in data.get("life_chapters", []):
            try:
                system.life_chapters.append(LifeChapter(
                    chapter_id=c_data["chapter_id"],
                    title=c_data["title"],
                    start_date=c_data["start_date"],
                    summary=c_data["summary"],
                    key_events=c_data.get("key_events", []),
                    dominant_mood=c_data.get("dominant_mood", "hopeful"),
                    end_date=c_data.get("end_date"),
                ))
            except (ValueError, KeyError):
                pass
                
        system.dream_logs = []
        for d_data in data.get("dream_logs", []):
            try:
                system.dream_logs.append(DreamLog(
                    dream_id=d_data["dream_id"],
                    date=d_data["date"],
                    title=d_data["title"],
                    description=d_data["description"],
                    symbols=d_data.get("symbols", []),
                    interpretation=d_data.get("interpretation"),
                    recurring=d_data.get("recurring", False),
                ))
            except (ValueError, KeyError):
                pass
                
        system.current_chapter = data.get("current_chapter")
        system.daily_mood_summary = data.get("daily_mood_summary", {})
        system.prompts_completed = data.get("prompts_completed", 0)
        system.photos_taken = data.get("photos_taken", 0)
        system.dreams_recorded = data.get("dreams_recorded", 0)
        return system


# Global instance
enhanced_diary = EnhancedDiarySystem()
