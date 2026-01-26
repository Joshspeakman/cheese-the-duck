"""
Duck Diary/Journal system - Creates narrative storytelling and memorable moments.
Tracks the duck's life story, creating emotional investment (Sims family history style).
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import threading


class DiaryEntryType(Enum):
    """Types of diary entries."""
    MILESTONE = "milestone"       # Growth, achievements
    RELATIONSHIP = "relationship"  # Bond changes
    ADVENTURE = "adventure"       # Special events
    MEMORY = "memory"             # Sweet moments
    DISCOVERY = "discovery"       # Found items, visitors
    FEELING = "feeling"           # Mood reflections
    VISITOR = "visitor"           # Visitor interactions
    WEATHER = "weather"           # Special weather events


@dataclass
class DiaryEntry:
    """A single diary entry."""
    entry_id: str
    entry_type: DiaryEntryType
    date: str  # ISO date
    title: str
    content: str
    mood_at_time: str
    duck_age_days: int
    is_favorite: bool = False
    tags: List[str] = field(default_factory=list)


# Template entries for auto-generation
ENTRY_TEMPLATES = {
    DiaryEntryType.MILESTONE: {
        "hatched": {
            "title": "The Day I Hatched!",
            "template": "Today is the most important day ever - I was born! *cracks shell* Hello world! I wonder what adventures await... My human seems nice. I hope they have bread!",
        },
        "first_steps": {
            "title": "My First Waddle!",
            "template": "I took my very first steps today! It was wobbly and I fell twice, but I DID IT! Look at me go! *waddle waddle* Soon I'll be the fastest duck ever!",
        },
        "became_teen": {
            "title": "Growing Up!",
            "template": "I'm not a tiny duckling anymore! Look at these feathers coming in! I feel so grown up. Still love bread though. Some things never change.",
        },
        "became_adult": {
            "title": "All Grown Up!",
            "template": "I did it! I'm officially a full adult duck now! It's been quite a journey. Through all the ups and downs, my human was always there. We make a pretty good team.",
        },
        "became_elder": {
            "title": "Wisdom of Years",
            "template": "I've lived a good, long life. My feathers may be getting grey, but my heart is full of wonderful memories. Every bread crumb was worth it!",
        },
        "level_up": {
            "title": "Level Up! (Level {level})",
            "template": "My human and I reached level {level} together! We've come so far. Remember when I was just a tiny duckling? Now look at us! Champions!",
        },
    },
    DiaryEntryType.RELATIONSHIP: {
        "first_pet": {
            "title": "First Pets!",
            "template": "My human petted me for the first time today! Their hands are so gentle. I think... I think we're going to be friends!",
        },
        "best_friends": {
            "title": "Best Friends Forever!",
            "template": "I officially declare: my human is my BEST FRIEND! We've been through so much together. I would share my last bread crumb with them. (But please don't test that)",
        },
        "bonded": {
            "title": "Soul Bond",
            "template": "I can't imagine life without my human anymore. We understand each other without words. When they're happy, I'm happy. This is what true friendship feels like!",
        },
        "streak_milestone": {
            "title": "Day {days} Together!",
            "template": "We've been together for {days} days now! That's like... a lot of days! Every single one has been special. Here's to {days} more!",
        },
    },
    DiaryEntryType.ADVENTURE: {
        "rainbow": {
            "title": "I Saw a Rainbow!",
            "template": "A RAINBOW appeared today! I made a wish for infinite bread. And also for my human to be happy forever. Priorities, you know?",
        },
        "storm_brave": {
            "title": "Braved the Storm!",
            "template": "*BOOM* There was a big scary storm today! I was a tiny bit scared (only a tiny bit!), but my human was there. We got through it together!",
        },
        "snow_day": {
            "title": "First Snow!",
            "template": "Cold white flakes are falling from the sky! I tried to eat one. Not bread. Still pretty though! My feathers are all floofy from the cold!",
        },
    },
    DiaryEntryType.MEMORY: {
        "happy_moment": {
            "title": "A Perfect Moment",
            "template": "Nothing special happened today, but somehow... it was perfect. Just me, my human, and peaceful quacking. These are the moments I'll remember forever.",
        },
        "silly_fall": {
            "title": "I Fell Down!",
            "template": "I tripped over my own feet today. *bonk* My human laughed but then gave me extra pets. 10/10 would embarrass myself again.",
        },
        "nap_time": {
            "title": "The Best Nap Ever",
            "template": "I had the COZIEST nap today! I dreamed of swimming in a pond made of bread. Don't judge me.",
        },
    },
    DiaryEntryType.DISCOVERY: {
        "found_treasure": {
            "title": "Treasure Found!",
            "template": "I found a {item} today! It's SO shiny! I'll add it to my collection. My human seemed happy too. Finder's keepers!",
        },
        "rare_find": {
            "title": "Amazing Discovery!",
            "template": "THIS IS HUGE! I discovered a {item}! It's super rare and special! I feel like an explorer! Marco Polo Duck!",
        },
    },
    DiaryEntryType.VISITOR: {
        "visitor_came": {
            "title": "A Visitor!",
            "template": "{visitor_name} visited today! It was so exciting to meet someone new! They seemed really nice. I hope they come back!",
        },
        "visitor_gift": {
            "title": "A Generous Guest",
            "template": "{visitor_name} visited and gave me a gift! A {gift}! Making friends is the BEST!",
        },
    },
    DiaryEntryType.FEELING: {
        "grateful": {
            "title": "Feeling Grateful",
            "template": "Today I'm just really grateful. For my cozy home, for bread, for my human, for everything. Life is good.",
        },
        "excited": {
            "title": "So Excited!",
            "template": "I don't know why but I'm SO HYPED today! Everything is AMAZING! *flap flap* Let's DO THINGS!",
        },
        "contemplative": {
            "title": "Deep Thoughts",
            "template": "I spent today thinking about life, the universe, and bread. Mostly bread. But also important stuff! I'm a very philosophical duck.",
        },
    },
}

# Relationship level descriptions and thresholds
RELATIONSHIP_LEVELS = {
    0: {"name": "Strangers", "threshold": 0, "description": "Just met, still getting to know each other"},
    1: {"name": "Acquaintance", "threshold": 10, "description": "Starting to recognize each other"},
    2: {"name": "Friendly", "threshold": 25, "description": "Getting comfortable together"},
    3: {"name": "Friends", "threshold": 50, "description": "A solid friendship forming"},
    4: {"name": "Good Friends", "threshold": 75, "description": "Really enjoy spending time together"},
    5: {"name": "Best Friends", "threshold": 100, "description": "Inseparable companions"},
    6: {"name": "Soul Bonded", "threshold": 150, "description": "A connection that transcends words"},
}


class DuckDiary:
    """
    Manages the duck's diary/journal.
    Creates a narrative history of the duck's life.
    """

    def __init__(self):
        self.entries: List[DiaryEntry] = []
        self.relationship_score: int = 0
        self.current_relationship_level: int = 0
        self.milestones_recorded: List[str] = []
        self.first_entry_date: Optional[str] = None
        self.total_interactions: int = 0

    def _generate_entry_id(self) -> str:
        """Generate unique entry ID."""
        return f"entry_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.entries)}"

    def _get_duck_age_days(self) -> int:
        """Calculate duck age in days."""
        if not self.first_entry_date:
            return 0
        try:
            first = datetime.fromisoformat(self.first_entry_date)
            return (datetime.now() - first).days
        except (ValueError, TypeError):
            return 0

    def add_entry(
        self,
        entry_type: DiaryEntryType,
        title: str,
        content: str,
        mood: str = "happy",
        tags: List[str] = None,
    ) -> DiaryEntry:
        """Add a new diary entry."""
        if not self.first_entry_date:
            self.first_entry_date = datetime.now().isoformat()

        entry = DiaryEntry(
            entry_id=self._generate_entry_id(),
            entry_type=entry_type,
            date=datetime.now().isoformat(),
            title=title,
            content=content,
            mood_at_time=mood,
            duck_age_days=self._get_duck_age_days(),
            tags=tags or [],
        )

        self.entries.append(entry)

        # Keep diary manageable (max 100 entries)
        if len(self.entries) > 100:
            # Keep favorites and remove oldest non-favorites
            non_favorites = [e for e in self.entries if not e.is_favorite]
            if len(non_favorites) > 50:
                self.entries = [e for e in self.entries if e.is_favorite] + non_favorites[-50:]

        return entry

    def record_milestone(self, milestone_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record a milestone event in the diary."""
        if milestone_type in self.milestones_recorded:
            return None  # Don't double-record milestones

        templates = ENTRY_TEMPLATES.get(DiaryEntryType.MILESTONE, {})
        if milestone_type not in templates:
            return None

        template = templates[milestone_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        entry = self.add_entry(
            DiaryEntryType.MILESTONE,
            title,
            content,
            mood="excited",
            tags=["milestone", milestone_type],
        )
        entry.is_favorite = True  # Milestones are auto-favorited

        self.milestones_recorded.append(milestone_type)
        return entry

    def record_relationship_change(self, event_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record a relationship event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.RELATIONSHIP, {})
        if event_type not in templates:
            return None

        template = templates[event_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        entry = self.add_entry(
            DiaryEntryType.RELATIONSHIP,
            title,
            content,
            mood="loved",
            tags=["relationship", event_type],
        )

        if event_type in ["best_friends", "bonded"]:
            entry.is_favorite = True

        return entry

    def record_adventure(self, adventure_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record an adventure/special event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.ADVENTURE, {})
        if adventure_type not in templates:
            return None

        template = templates[adventure_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        return self.add_entry(
            DiaryEntryType.ADVENTURE,
            title,
            content,
            mood="excited",
            tags=["adventure", adventure_type],
        )

    def record_discovery(self, item_name: str, is_rare: bool = False) -> DiaryEntry:
        """Record finding an item."""
        template_key = "rare_find" if is_rare else "found_treasure"
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.DISCOVERY, {})
        template = templates.get(template_key, templates.get("found_treasure"))

        title = template["title"].format(item=item_name)
        content = template["template"].format(item=item_name)

        entry = self.add_entry(
            DiaryEntryType.DISCOVERY,
            title,
            content,
            mood="excited",
            tags=["discovery", "rare" if is_rare else "common"],
        )

        if is_rare:
            entry.is_favorite = True

        return entry

    def record_visitor(self, visitor_name: str, gift: Optional[str] = None) -> DiaryEntry:
        """Record a visitor event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.VISITOR, {})

        if gift:
            template = templates["visitor_gift"]
            content = template["template"].format(visitor_name=visitor_name, gift=gift)
            title = template["title"]
        else:
            template = templates["visitor_came"]
            content = template["template"].format(visitor_name=visitor_name)
            title = template["title"]

        return self.add_entry(
            DiaryEntryType.VISITOR,
            title,
            content,
            mood="friendly",
            tags=["visitor", visitor_name.lower().replace(" ", "_")],
        )

    def record_feeling(self, feeling_type: str = None) -> Optional[DiaryEntry]:
        """Record a random feeling/reflection entry."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.FEELING, {})

        if feeling_type and feeling_type in templates:
            template = templates[feeling_type]
        else:
            feeling_type = random.choice(list(templates.keys()))
            template = templates[feeling_type]

        return self.add_entry(
            DiaryEntryType.FEELING,
            template["title"],
            template["template"],
            mood=feeling_type,
            tags=["feeling", feeling_type],
        )

    def record_random_memory(self) -> Optional[DiaryEntry]:
        """Record a random sweet memory (call occasionally)."""
        if random.random() > 0.3:  # 30% chance to record
            return None

        templates = ENTRY_TEMPLATES.get(DiaryEntryType.MEMORY, {})
        memory_type = random.choice(list(templates.keys()))
        template = templates[memory_type]

        return self.add_entry(
            DiaryEntryType.MEMORY,
            template["title"],
            template["template"],
            mood="content",
            tags=["memory", memory_type],
        )

    def increase_relationship(self, amount: int = 1) -> Optional[Tuple[int, str]]:
        """
        Increase relationship score.
        Returns (new_level, level_name) if level changed, None otherwise.
        """
        self.relationship_score += amount
        self.total_interactions += 1

        # Check for level up
        for level, data in sorted(RELATIONSHIP_LEVELS.items(), reverse=True):
            if self.relationship_score >= data["threshold"]:
                if level > self.current_relationship_level:
                    self.current_relationship_level = level

                    # Record relationship milestone
                    if level == 5:
                        self.record_relationship_change("best_friends")
                    elif level == 6:
                        self.record_relationship_change("bonded")

                    return (level, data["name"])
                break

        return None

    def get_relationship_info(self) -> Dict:
        """Get current relationship status."""
        level_data = RELATIONSHIP_LEVELS.get(self.current_relationship_level, RELATIONSHIP_LEVELS[0])
        next_level = self.current_relationship_level + 1

        progress = 0
        if next_level in RELATIONSHIP_LEVELS:
            current_threshold = level_data["threshold"]
            next_threshold = RELATIONSHIP_LEVELS[next_level]["threshold"]
            if next_threshold > current_threshold:
                progress = ((self.relationship_score - current_threshold) /
                           (next_threshold - current_threshold)) * 100

        return {
            "level": self.current_relationship_level,
            "name": level_data["name"],
            "description": level_data["description"],
            "score": self.relationship_score,
            "progress_to_next": min(100, progress),
            "total_interactions": self.total_interactions,
        }

    def get_recent_entries(self, count: int = 10) -> List[DiaryEntry]:
        """Get most recent diary entries."""
        return sorted(self.entries, key=lambda e: e.date, reverse=True)[:count]

    def get_favorite_entries(self) -> List[DiaryEntry]:
        """Get all favorite entries."""
        return [e for e in self.entries if e.is_favorite]

    def get_entries_by_type(self, entry_type: DiaryEntryType) -> List[DiaryEntry]:
        """Get entries of a specific type."""
        return [e for e in self.entries if e.entry_type == entry_type]

    def toggle_favorite(self, entry_id: str) -> bool:
        """Toggle favorite status of an entry."""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                entry.is_favorite = not entry.is_favorite
                return entry.is_favorite
        return False

    def get_stats(self) -> Dict:
        """Get diary statistics."""
        return {
            "total_entries": len(self.entries),
            "favorites": len([e for e in self.entries if e.is_favorite]),
            "milestones": len([e for e in self.entries if e.entry_type == DiaryEntryType.MILESTONE]),
            "adventures": len([e for e in self.entries if e.entry_type == DiaryEntryType.ADVENTURE]),
            "days_documented": self._get_duck_age_days(),
            "relationship_level": self.current_relationship_level,
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "entries": [
                {
                    "entry_id": e.entry_id,
                    "entry_type": e.entry_type.value,
                    "date": e.date,
                    "title": e.title,
                    "content": e.content,
                    "mood_at_time": e.mood_at_time,
                    "duck_age_days": e.duck_age_days,
                    "is_favorite": e.is_favorite,
                    "tags": e.tags,
                }
                for e in self.entries
            ],
            "relationship_score": self.relationship_score,
            "current_relationship_level": self.current_relationship_level,
            "milestones_recorded": self.milestones_recorded,
            "first_entry_date": self.first_entry_date,
            "total_interactions": self.total_interactions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DuckDiary":
        """Create from dictionary."""
        diary = cls()
        diary.relationship_score = data.get("relationship_score", 0)
        diary.current_relationship_level = data.get("current_relationship_level", 0)
        diary.milestones_recorded = data.get("milestones_recorded", [])
        diary.first_entry_date = data.get("first_entry_date")
        diary.total_interactions = data.get("total_interactions", 0)

        for e_data in data.get("entries", []):
            try:
                entry = DiaryEntry(
                    entry_id=e_data["entry_id"],
                    entry_type=DiaryEntryType(e_data["entry_type"]),
                    date=e_data["date"],
                    title=e_data["title"],
                    content=e_data["content"],
                    mood_at_time=e_data.get("mood_at_time", "happy"),
                    duck_age_days=e_data.get("duck_age_days", 0),
                    is_favorite=e_data.get("is_favorite", False),
                    tags=e_data.get("tags", []),
                )
                diary.entries.append(entry)
            except (KeyError, TypeError, ValueError):
                continue

        return diary


# Lazy singleton pattern with thread-safe initialization
_duck_diary: Optional[DuckDiary] = None
_duck_diary_lock = threading.Lock()


def get_duck_diary() -> DuckDiary:
    """Get the global duck diary instance (lazy initialization). Thread-safe."""
    global _duck_diary
    if _duck_diary is None:
        with _duck_diary_lock:
            if _duck_diary is None:
                _duck_diary = DuckDiary()
    return _duck_diary


# Direct instance for backwards compatibility
duck_diary = DuckDiary()
