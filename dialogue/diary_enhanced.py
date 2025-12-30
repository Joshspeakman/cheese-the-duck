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
    ],
    DiaryPromptType.GRATITUDE: [
        "What are three things you're grateful for?",
        "Who made you smile today?",
        "What small joy did you experience?",
        "What comfort do you appreciate most?",
        "What about your home makes you happy?",
    ],
    DiaryPromptType.DREAM: [
        "If you could go anywhere, where would it be?",
        "What's your biggest dream?",
        "If you could fly, where would you go first?",
        "What would your perfect day look like?",
        "If you could meet anyone, who would it be?",
    ],
    DiaryPromptType.GOAL: [
        "What do you want to achieve this week?",
        "What new thing do you want to try?",
        "How do you want to grow?",
        "What skill do you want to improve?",
        "What habit do you want to build?",
    ],
    DiaryPromptType.MEMORY: [
        "What's your earliest happy memory?",
        "What's the best day you remember?",
        "What's a funny moment you'll never forget?",
        "What's the kindest thing anyone did for you?",
        "What adventure do you remember most?",
    ],
    DiaryPromptType.LETTER: [
        "Write a letter to your future self.",
        "Write a thank you note to your human.",
        "Write a letter to your past self.",
        "Write a note to a friend.",
        "Write about why you matter.",
    ],
    DiaryPromptType.WISHLIST: [
        "What three wishes would you make?",
        "What would you put on your bucket list?",
        "What experiences do you want to have?",
        "What would make next month amazing?",
        "What do you hope for?",
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
