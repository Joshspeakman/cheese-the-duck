"""
Photo Album/Scrapbook System - Captures and stores memorable moments.
Creates a visual memory collection of special events, milestones, and discoveries.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class PhotoCategory(Enum):
    """Categories of scrapbook photos/memories."""
    MILESTONE = "milestone"
    ADVENTURE = "adventure"
    FRIENDSHIP = "friendship"
    DISCOVERY = "discovery"
    SEASONAL = "seasonal"
    ACHIEVEMENT = "achievement"
    FUNNY = "funny"
    DAILY = "daily"


@dataclass
class ScrapbookPhoto:
    """A single photo/memory in the scrapbook."""
    photo_id: str
    category: PhotoCategory
    title: str
    description: str
    date_taken: str  # ISO date
    ascii_art: List[str]
    mood_at_time: str
    duck_age_days: int
    is_favorite: bool = False
    tags: List[str] = field(default_factory=list)
    location: str = "home"
    weather: str = "sunny"
    stickers: List[str] = field(default_factory=list)  # Decorative stickers added


# Pre-made ASCII art frames for photos
PHOTO_FRAMES = {
    "simple": [
        "╔════════════════════════╗",
        "║  {title:^20}  ║",
        "╠════════════════════════╣",
        "║                        ║",
        "║   {art_line_1:^20}   ║",
        "║   {art_line_2:^20}   ║",
        "║   {art_line_3:^20}   ║",
        "║   {art_line_4:^20}   ║",
        "║                        ║",
        "╠════════════════════════╣",
        "║  {date:^20}  ║",
        "╚════════════════════════╝",
    ],
    "fancy": [
        "╭─────────✦ ✧ ✦─────────╮",
        "│  {title:^20}  │",
        "├───────────────────────┤",
        "│                       │",
        "│  {art_line_1:^19}  │",
        "│  {art_line_2:^19}  │",
        "│  {art_line_3:^19}  │",
        "│  {art_line_4:^19}  │",
        "│                       │",
        "├───────────────────────┤",
        "│  ✿ {date:^17} ✿  │",
        "╰─────────✧ ✦ ✧─────────╯",
    ],
    "polaroid": [
        "┌─────────────────────────┐",
        "│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │",
        "│ ▓                     ▓ │",
        "│ ▓  {art_line_1:^17}  ▓ │",
        "│ ▓  {art_line_2:^17}  ▓ │",
        "│ ▓  {art_line_3:^17}  ▓ │",
        "│ ▓  {art_line_4:^17}  ▓ │",
        "│ ▓                     ▓ │",
        "│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │",
        "│                         │",
        "│  {title:^21}  │",
        "│  {date:^21}  │",
        "└─────────────────────────┘",
    ],
}

# Photo ASCII templates for different moments
PHOTO_ART = {
    "duck_happy": [
        "   __(o>",
        "  (  🌟",
        " _/  \\",
        "Happy moment!",
    ],
    "duck_sleeping": [
        "   __(-)>",
        "  (  💤",
        " _/  \\",
        "Sweet dreams",
    ],
    "duck_eating": [
        "   __(o>🍞",
        "  ( nom",
        " _/  \\",
        "Yummy time!",
    ],
    "duck_playing": [
        "   __(>o)>",
        "  ( ⚽",
        "  _\\ /",
        "Playtime!",
    ],
    "duck_friends": [
        " __(o> __(o>",
        "(   )(   )",
        " \\_/  \\_/",
        "Friends!",
    ],
    "duck_adventure": [
        "   🗺️__(o>",
        "  (   🎒",
        " _/   \\",
        "Adventure!",
    ],
    "duck_discovery": [
        "   __(O>",
        "  ( ✨💎",
        " _/  \\",
        "Found it!",
    ],
    "duck_celebration": [
        " 🎉__(^o^)>🎉",
        "  (  🎊",
        " _/   \\",
        "Party time!",
    ],
    "duck_rain": [
        "  ☔__(o>",
        "💧(  💧",
        " _/  \\",
        "Rainy day!",
    ],
    "duck_snow": [
        " ❄️ __(o>❄️",
        "  (  ⛄",
        " _/  \\",
        "Snow day!",
    ],
    "duck_rainbow": [
        "  🌈__(^o^)>",
        "  (   ✨",
        " _/   \\",
        "Rainbow!",
    ],
    "duck_fishing": [
        "   __(o>",
        "  ( 🎣",
        " _/  \\ ~🐟",
        "Gone fishing",
    ],
    "duck_garden": [
        "🌸__(o>🌷",
        "  (  🌻",
        " _/  \\",
        "Garden day!",
    ],
}

# Decorative stickers that can be added to photos
STICKERS = {
    "heart": "❤️",
    "star": "⭐",
    "sparkle": "✨",
    "flower": "🌸",
    "rainbow": "🌈",
    "sun": "☀️",
    "moon": "🌙",
    "crown": "👑",
    "trophy": "🏆",
    "bread": "🍞",
    "butterfly": "🦋",
    "music": "🎵",
    "gift": "🎁",
    "camera": "📸",
    "clover": "🍀",
}


class Scrapbook:
    """
    Manages the photo album/scrapbook collection.
    Captures and stores memorable moments from the duck's life.
    """
    
    def __init__(self):
        self.photos: Dict[str, ScrapbookPhoto] = {}
        self.pages: List[List[str]] = []  # Organized pages of photo IDs
        self.current_page: int = 0
        self.photos_per_page: int = 4
        self.total_photos_taken: int = 0
        self.favorite_count: int = 0
        self.auto_capture_enabled: bool = True
        self.unlocked_frames: List[str] = ["simple"]
        self.unlocked_stickers: List[str] = ["heart", "star", "sparkle"]
    
    def take_photo(
        self,
        title: str,
        description: str,
        category: PhotoCategory,
        art_key: str = "duck_happy",
        mood: str = "happy",
        duck_age: int = 1,
        location: str = "home",
        weather: str = "sunny",
        tags: List[str] = None
    ) -> ScrapbookPhoto:
        """Take a new photo and add it to the scrapbook."""
        self.total_photos_taken += 1
        photo_id = f"photo_{self.total_photos_taken}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        ascii_art = PHOTO_ART.get(art_key, PHOTO_ART["duck_happy"]).copy()
        
        photo = ScrapbookPhoto(
            photo_id=photo_id,
            category=category,
            title=title,
            description=description,
            date_taken=datetime.now().isoformat(),
            ascii_art=ascii_art,
            mood_at_time=mood,
            duck_age_days=duck_age,
            tags=tags or [],
            location=location,
            weather=weather,
        )
        
        self.photos[photo_id] = photo
        self._add_to_page(photo_id)
        
        return photo
    
    def _add_to_page(self, photo_id: str):
        """Add a photo to the album pages."""
        if not self.pages or len(self.pages[-1]) >= self.photos_per_page:
            self.pages.append([])
        self.pages[-1].append(photo_id)
    
    def toggle_favorite(self, photo_id: str) -> bool:
        """Toggle favorite status of a photo."""
        if photo_id in self.photos:
            photo = self.photos[photo_id]
            photo.is_favorite = not photo.is_favorite
            self.favorite_count += 1 if photo.is_favorite else -1
            return photo.is_favorite
        return False
    
    def add_sticker(self, photo_id: str, sticker: str) -> bool:
        """Add a sticker to a photo."""
        if photo_id in self.photos and sticker in self.unlocked_stickers:
            self.photos[photo_id].stickers.append(sticker)
            return True
        return False
    
    def unlock_frame(self, frame_name: str):
        """Unlock a new photo frame style."""
        if frame_name in PHOTO_FRAMES and frame_name not in self.unlocked_frames:
            self.unlocked_frames.append(frame_name)
    
    def unlock_sticker(self, sticker_name: str):
        """Unlock a new sticker."""
        if sticker_name in STICKERS and sticker_name not in self.unlocked_stickers:
            self.unlocked_stickers.append(sticker_name)
    
    def get_page(self, page_num: int) -> List[ScrapbookPhoto]:
        """Get photos for a specific page."""
        if 0 <= page_num < len(self.pages):
            return [self.photos[pid] for pid in self.pages[page_num] if pid in self.photos]
        return []
    
    def get_photos_by_category(self, category: PhotoCategory) -> List[ScrapbookPhoto]:
        """Get all photos in a category."""
        return [p for p in self.photos.values() if p.category == category]
    
    def get_favorites(self) -> List[ScrapbookPhoto]:
        """Get all favorite photos."""
        return [p for p in self.photos.values() if p.is_favorite]
    
    def render_photo(self, photo: ScrapbookPhoto, frame_style: str = "simple") -> List[str]:
        """Render a photo with its frame."""
        frame = PHOTO_FRAMES.get(frame_style, PHOTO_FRAMES["simple"])
        
        # Pad or truncate art lines to 4
        art = photo.ascii_art[:4]
        while len(art) < 4:
            art.append("")
        
        rendered = []
        for line in frame:
            rendered_line = line.format(
                title=photo.title[:20],
                date=photo.date_taken[:10],
                art_line_1=art[0][:20],
                art_line_2=art[1][:20],
                art_line_3=art[2][:20],
                art_line_4=art[3][:20],
            )
            rendered.append(rendered_line)
        
        # Add stickers if any
        if photo.stickers:
            sticker_line = " ".join([STICKERS.get(s, s) for s in photo.stickers[:5]])
            rendered.append(f"  {sticker_line}")
        
        return rendered
    
    def render_album_page(self, page_num: int = None) -> List[str]:
        """Render a full album page with multiple photos."""
        if page_num is None:
            page_num = self.current_page
        
        photos = self.get_page(page_num)
        if not photos:
            return [
                "╔═══════════════════════════════════════╗",
                "║        📷 SCRAPBOOK - Empty Page 📷    ║",
                "║                                       ║",
                "║       No photos on this page yet!     ║",
                "║                                       ║",
                "║   Make memories with your duck to     ║",
                "║   fill your scrapbook!                ║",
                "║                                       ║",
                "╚═══════════════════════════════════════╝",
            ]
        
        lines = [
            f"╔═══════════════════════════════════════════════════╗",
            f"║     📷 SCRAPBOOK - Page {page_num + 1}/{len(self.pages)} 📷     ║",
            f"╠═══════════════════════════════════════════════════╣",
        ]
        
        for photo in photos:
            fav = "★" if photo.is_favorite else "☆"
            lines.append(f"║ {fav} {photo.title[:25]:<25} - {photo.date_taken[:10]} ║")
            lines.append(f"║   {photo.description[:40]:<40} ║")
            lines.append(f"╟───────────────────────────────────────────────────╢")
        
        lines.append(f"║  [<] Prev  [>] Next  [F] Toggle Favorite  [Q] Back ║")
        lines.append(f"╚═══════════════════════════════════════════════════╝")
        
        return lines
    
    def auto_capture_milestone(self, milestone_type: str, duck_name: str, duck_age: int, mood: str = "happy"):
        """Automatically capture a milestone photo."""
        milestones = {
            "first_feed": ("First Meal!", f"{duck_name}'s very first feeding!", "duck_eating"),
            "first_play": ("First Playtime!", f"{duck_name} played for the first time!", "duck_playing"),
            "growth_teen": ("Growing Up!", f"{duck_name} became a teenager!", "duck_celebration"),
            "growth_adult": ("All Grown Up!", f"{duck_name} is now an adult!", "duck_celebration"),
            "growth_elder": ("Wise Duck", f"{duck_name} has become an elder!", "duck_celebration"),
            "best_friends": ("Best Friends!", f"You and {duck_name} are now best friends!", "duck_friends"),
            "first_visitor": ("First Visitor!", f"{duck_name} met their first visitor!", "duck_friends"),
            "first_adventure": ("Adventure Time!", f"{duck_name}'s first adventure!", "duck_adventure"),
            "rainbow_seen": ("Rainbow Spotted!", f"{duck_name} saw a beautiful rainbow!", "duck_rainbow"),
            "treasure_found": ("Treasure Hunter!", f"{duck_name} found treasure!", "duck_discovery"),
            "fishing_catch": ("Big Catch!", f"{duck_name} caught a fish!", "duck_fishing"),
            "garden_harvest": ("Harvest Time!", f"{duck_name} harvested from the garden!", "duck_garden"),
        }
        
        if milestone_type in milestones and self.auto_capture_enabled:
            title, desc, art = milestones[milestone_type]
            self.take_photo(
                title=title,
                description=desc,
                category=PhotoCategory.MILESTONE,
                art_key=art,
                mood=mood,
                duck_age=duck_age,
                tags=[milestone_type, "auto"],
            )
    
    def to_dict(self) -> dict:
        """Convert scrapbook to dictionary for saving."""
        return {
            "photos": {
                pid: {
                    "photo_id": p.photo_id,
                    "category": p.category.value,
                    "title": p.title,
                    "description": p.description,
                    "date_taken": p.date_taken,
                    "ascii_art": p.ascii_art,
                    "mood_at_time": p.mood_at_time,
                    "duck_age_days": p.duck_age_days,
                    "is_favorite": p.is_favorite,
                    "tags": p.tags,
                    "location": p.location,
                    "weather": p.weather,
                    "stickers": p.stickers,
                }
                for pid, p in self.photos.items()
            },
            "pages": self.pages,
            "current_page": self.current_page,
            "total_photos_taken": self.total_photos_taken,
            "favorite_count": self.favorite_count,
            "auto_capture_enabled": self.auto_capture_enabled,
            "unlocked_frames": self.unlocked_frames,
            "unlocked_stickers": self.unlocked_stickers,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Scrapbook":
        """Create scrapbook from dictionary."""
        scrapbook = cls()
        
        for pid, pdata in data.get("photos", {}).items():
            photo = ScrapbookPhoto(
                photo_id=pdata["photo_id"],
                category=PhotoCategory(pdata["category"]),
                title=pdata["title"],
                description=pdata["description"],
                date_taken=pdata["date_taken"],
                ascii_art=pdata["ascii_art"],
                mood_at_time=pdata["mood_at_time"],
                duck_age_days=pdata["duck_age_days"],
                is_favorite=pdata.get("is_favorite", False),
                tags=pdata.get("tags", []),
                location=pdata.get("location", "home"),
                weather=pdata.get("weather", "sunny"),
                stickers=pdata.get("stickers", []),
            )
            scrapbook.photos[pid] = photo
        
        scrapbook.pages = data.get("pages", [])
        scrapbook.current_page = data.get("current_page", 0)
        scrapbook.total_photos_taken = data.get("total_photos_taken", len(scrapbook.photos))
        scrapbook.favorite_count = data.get("favorite_count", 0)
        scrapbook.auto_capture_enabled = data.get("auto_capture_enabled", True)
        scrapbook.unlocked_frames = data.get("unlocked_frames", ["simple"])
        scrapbook.unlocked_stickers = data.get("unlocked_stickers", ["heart", "star", "sparkle"])
        
        return scrapbook


# Global scrapbook instance
scrapbook = Scrapbook()
