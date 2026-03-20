"""
Enhanced Diary System - Extends the base diary with more features.
Adds emotional tracking, dream journaling, life chapters, and deeper narrative.
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


@dataclass
class EmotionLog:
    """A logged emotion moment."""
    emotion: EmotionCategory
    intensity: int  # 1-10
    timestamp: str
    trigger: Optional[str] = None
    notes: Optional[str] = None


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
        self.life_chapters: List[LifeChapter] = []
        self.dream_logs: List[DreamLog] = []
        
        # Tracking
        self.current_chapter: Optional[str] = None
        self.daily_mood_summary: Dict[str, List[str]] = {}  # date -> moods
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
        
        return {
            "emotion_analysis": analysis,
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
        system.dreams_recorded = data.get("dreams_recorded", 0)
        return system


# Global instance
enhanced_diary = EnhancedDiarySystem()
