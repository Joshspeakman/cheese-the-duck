"""
Duck Friends System - Visiting ducks, friendship levels, and social interactions.
Includes visitor events, gift exchanges, and duck personalities.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import time


class FriendshipLevel(Enum):
    """Friendship tier with visiting ducks."""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    BEST_FRIEND = "best_friend"


class DuckPersonalityType(Enum):
    """Personality archetypes for visitor ducks."""
    ADVENTUROUS = "adventurous"
    SCHOLARLY = "scholarly"
    ARTISTIC = "artistic"
    PLAYFUL = "playful"
    MYSTERIOUS = "mysterious"
    GENEROUS = "generous"
    FOODIE = "foodie"
    ATHLETIC = "athletic"


# Visitor duck appearances
DUCK_APPEARANCES = {
    "adventurous": {"color": "tan", "accessory": "explorer_hat", "scarf": "green"},
    "scholarly": {"color": "gray", "accessory": "glasses", "scarf": "blue"},
    "artistic": {"color": "white", "accessory": "beret", "scarf": "rainbow"},
    "playful": {"color": "yellow", "accessory": "propeller_hat", "scarf": "red"},
    "mysterious": {"color": "black", "accessory": "mask", "scarf": "purple"},
    "generous": {"color": "golden", "accessory": "bow_tie", "scarf": "pink"},
    "foodie": {"color": "orange", "accessory": "chef_hat", "scarf": "white"},
    "athletic": {"color": "brown", "accessory": "headband", "scarf": "orange"},
}

# Visitor NPC ASCII art by personality (facing left, toward Cheese)
VISITOR_ASCII_ART = {
    "adventurous": {
        "idle": [
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--^    ",
            "    /|     ",
            "   (_|     ",
        ],
        "waddle": [
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-~-'   ",
            "   / |     ",
            "  (_)|     ",
        ],
        "happy": [
            "   \\!/     ",
            "    __     ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--^    ",
            "   (\\|/)   ",
        ],
        "gift": [
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--^ [#]",
            "    /|     ",
            "   (_|     ",
        ],
    },
    "scholarly": {
        "idle": [
            "    __     ",
            "  _/  \\_   ",
            " /@o  o@\\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
            "   (_|     ",
        ],
        "waddle": [
            "    __     ",
            "  _/  \\_   ",
            " /@o  o@\\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-~-'   ",
            "   / |     ",
            "  (_)|     ",
        ],
        "happy": [
            "    !      ",
            "    __     ",
            "  _/  \\_   ",
            " /@^  ^@\\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "reading": [
            "    __     ",
            "  _/  \\_   ",
            " /@-  -@\\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--' ___",
            "    /| |=| ",
            "   (_| |=| ",
        ],
    },
    "artistic": {
        "idle": [
            "   ~@      ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
        ],
        "waddle": [
            "   ~@      ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-~-'   ",
            "   / |     ",
        ],
        "happy": [
            "   ~@ *    ",
            "    __  *  ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "painting": [
            "   ~@      ",
            "    __     ",
            "  _/  \\_   ",
            " / -  o \\ ~",
            " \\_    _/ ~",
            " <|  \\_/ ~ ",
            "   '--' /| ",
            "    /| [=] ",
        ],
    },
    "playful": {
        "idle": [
            "    @/     ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
        ],
        "waddle": [
            "    @\\     ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-~-'   ",
            "  (_) |    ",
        ],
        "happy": [
            "  * @/ *   ",
            "    __ !   ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "bounce": [
            "    @|     ",
            "    __     ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-^-'   ",
            "    \\ /    ",
        ],
    },
    "mysterious": {
        "idle": [
            "    __     ",
            "  _/##\\_   ",
            " / ?  ? \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
            "   (_|     ",
        ],
        "waddle": [
            "    __     ",
            "  _/##\\_   ",
            " / ?  ? \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '~~~'   ",
            "   / |     ",
            "  (_)|     ",
        ],
        "happy": [
            "    ...    ",
            "    __     ",
            "  _/##\\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
        ],
        "vanish": [
            "    __     ",
            "  ./##\\.   ",
            "  / ?  ?   ",
            "  \\_    /  ",
            " . |  \\_.  ",
            "   .--'.   ",
            "   ./|.    ",
            "   ._.     ",
        ],
    },
    "generous": {
        "idle": [
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <| [+]_/  ",
            "   '--'    ",
            "    /|     ",
            "   (_|     ",
        ],
        "waddle": [
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <| [+]_/  ",
            "   '-~-'   ",
            "   / |     ",
            "  (_)|     ",
        ],
        "happy": [
            "   <3 <3   ",
            "    __     ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <| [+]_/  ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "giving": [
            "    __     ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/ [*]",
            " <| [+]_/ ->",
            "   '--'    ",
            "    /|     ",
            "   (_|     ",
        ],
    },
    "foodie": {
        "idle": [
            "   _|=|_   ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
        ],
        "waddle": [
            "   _|=|_   ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-~-'   ",
            "   / |     ",
        ],
        "happy": [
            "   _|=|_ ! ",
            "    __  om ",
            "  _/  \\_ nom",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "eating": [
            "   _|=|_   ",
            "    __ nom ",
            "  _/  \\_ @ ",
            " / -  - \\  ",
            " \\_   >_/  ",
            " <|  \\_/ .,",
            "   '--' .  ",
            "    /|     ",
        ],
    },
    "athletic": {
        "idle": [
            "    ==     ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "    /|     ",
        ],
        "waddle": [
            "    ==     ",
            "    __     ",
            "  _/  \\_   ",
            " / o  o \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '-v-'   ",
            "   / |\\    ",
        ],
        "happy": [
            "   \\==/    ",
            "    __  !  ",
            "  _/  \\_   ",
            " / ^  ^ \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "   '--'    ",
            "   (\\|/)   ",
        ],
        "exercise": [
            "    ==     ",
            "    __ !!  ",
            "  _/  \\_   ",
            " / >  < \\  ",
            " \\_    _/  ",
            " <|  \\_/   ",
            "  /'-^-'\\  ",
            " / /| |\\ \\ ",
        ],
    },
}

# Visitor animation states by mood/activity
VISITOR_ANIMATION_STATES = {
    "arriving": ["waddle", "waddle", "idle"],
    "chatting": ["idle", "happy", "idle", "happy"],
    "playing": ["happy", "bounce" if "playful" else "happy", "waddle", "happy"],
    "giving_gift": ["idle", "gift" if "adventurous" else "giving", "happy"],
    "receiving_gift": ["happy", "happy", "idle"],
    "eating": ["eating", "eating", "happy"],
    "leaving": ["waddle", "waddle", "waddle"],
    "idle": ["idle", "idle", "happy", "idle"],
}

# Visitor animation timing
VISITOR_ANIMATION_SPEED = 0.8  # Seconds per frame


class VisitorAnimator:
    """Handles visitor NPC animations during visits."""
    
    def __init__(self):
        self._current_state: str = "idle"
        self._frame_index: int = 0
        self._last_frame_time: float = 0.0
        self._personality: str = "adventurous"
        self._position_x: int = 0  # Offset from base position
        self._wobble: int = 0
    
    def set_visitor(self, personality: str):
        """Set the current visitor's personality for art selection."""
        self._personality = personality.lower() if personality else "adventurous"
        self._frame_index = 0
        self._current_state = "arriving"
    
    def set_state(self, state: str):
        """Set the animation state (arriving, chatting, playing, etc.)."""
        if state in VISITOR_ANIMATION_STATES:
            self._current_state = state
            self._frame_index = 0
    
    def update(self, current_time: float) -> bool:
        """Update animation frame. Returns True if frame changed."""
        if current_time - self._last_frame_time >= VISITOR_ANIMATION_SPEED:
            self._last_frame_time = current_time
            frames = VISITOR_ANIMATION_STATES.get(self._current_state, ["idle"])
            self._frame_index = (self._frame_index + 1) % len(frames)
            
            # Add wobble for movement
            if self._current_state in ["arriving", "leaving", "playing"]:
                self._wobble = 1 if self._wobble == 0 else 0
            else:
                self._wobble = 0
            
            return True
        return False
    
    def get_current_art(self) -> List[str]:
        """Get the current animation frame's ASCII art."""
        frames = VISITOR_ANIMATION_STATES.get(self._current_state, ["idle"])
        frame_name = frames[self._frame_index % len(frames)]
        
        # Get personality-specific art
        personality_art = VISITOR_ASCII_ART.get(self._personality, VISITOR_ASCII_ART["adventurous"])
        art = personality_art.get(frame_name, personality_art.get("idle", ["[DUCK]"]))
        
        # Apply wobble offset
        if self._wobble:
            art = [" " + line[:-1] if len(line) > 1 else line for line in art]
        
        return art
    
    def get_activity_message(self) -> str:
        """Get a message describing what the visitor is doing."""
        messages = {
            "arriving": "*waddles over excitedly*",
            "chatting": "*quacks in conversation*",
            "playing": "*having fun!*",
            "giving_gift": "*offers a gift*",
            "receiving_gift": "*accepts gift happily*",
            "eating": "*om nom nom*",
            "leaving": "*waves goodbye*",
            "idle": "*standing around*",
        }
        return messages.get(self._current_state, "")


# Global visitor animator instance
visitor_animator = VisitorAnimator()

# Duck names by personality
DUCK_NAMES = {
    "adventurous": ["Marco", "Amelia", "Columbus", "Vasco", "Marina"],
    "scholarly": ["Einstein", "Newton", "Ada", "Darwin", "Curie"],
    "artistic": ["Picasso", "Frida", "Leonardo", "Monet", "Georgia"],
    "playful": ["Bubbles", "Giggles", "Zippy", "Bouncy", "Sunny"],
    "mysterious": ["Shadow", "Phantom", "Enigma", "Whisper", "Raven"],
    "generous": ["Charity", "Grace", "Blessing", "Angel", "Heart"],
    "foodie": ["Cookie", "Biscuit", "Truffle", "Pepper", "Ginger"],
    "athletic": ["Dash", "Sprint", "Champion", "Victor", "Rocket"],
}


@dataclass
class DuckFriend:
    """A friend duck that can visit."""
    id: str
    name: str
    personality: DuckPersonalityType
    friendship_level: FriendshipLevel
    friendship_points: int = 0
    times_visited: int = 0
    gifts_given: int = 0
    gifts_received: int = 0
    favorite_food: str = "bread"
    favorite_activity: str = "chat"
    first_met: str = ""
    last_visit: str = ""
    special_memories: List[str] = field(default_factory=list)
    unlocked_dialogue: List[str] = field(default_factory=list)


@dataclass
class VisitEvent:
    """An active visit from a friend duck."""
    friend_id: str
    started_at: str
    duration_minutes: int
    activities_done: List[str] = field(default_factory=list)
    mood: str = "happy"
    gift_brought: Optional[str] = None
    waiting_for_gift: bool = False


# Friendship point thresholds
FRIENDSHIP_THRESHOLDS = {
    FriendshipLevel.STRANGER: 0,
    FriendshipLevel.ACQUAINTANCE: 50,
    FriendshipLevel.FRIEND: 150,
    FriendshipLevel.CLOSE_FRIEND: 350,
    FriendshipLevel.BEST_FRIEND: 600,
}

# Gift preferences by personality
GIFT_PREFERENCES = {
    "adventurous": ["map", "compass", "binoculars", "hiking_boots"],
    "scholarly": ["book", "quill", "scroll", "telescope"],
    "artistic": ["paintbrush", "canvas", "palette", "sketchbook"],
    "playful": ["ball", "toy", "balloon", "party_hat"],
    "mysterious": ["crystal", "candle", "tarot_deck", "incense"],
    "generous": ["flowers", "chocolate", "ribbon", "heart_charm"],
    "foodie": ["bread", "cake", "cheese", "apple"],
    "athletic": ["dumbbell", "whistle", "medal", "energy_drink"],
}

# Gifts that visitors can bring
VISITOR_GIFTS = {
    "adventurous": ["exotic_feather", "rare_shell", "ancient_coin", "treasure_map"],
    "scholarly": ["rare_book", "fossil", "star_chart", "potion_recipe"],
    "artistic": ["painting", "sculpture", "poem", "melody"],
    "playful": ["toy", "joke_item", "party_favor", "fun_hat"],
    "mysterious": ["mystery_box", "crystal_ball", "shadow_stone", "prophecy"],
    "generous": ["gold_coins", "rare_seed", "blessing_charm", "wish_token"],
    "foodie": ["gourmet_bread", "secret_recipe", "rare_fruit", "magic_ingredient"],
    "athletic": ["trophy", "energy_boost", "speed_shoes", "champion_medal"],
}


class FriendsSystem:
    """
    Manages duck friends, visits, and social interactions.
    """
    
    def __init__(self):
        self.friends: Dict[str, DuckFriend] = {}
        self.current_visit: Optional[VisitEvent] = None
        self.total_visits: int = 0
        self.total_gifts_exchanged: int = 0
        self.last_visitor_time: str = ""
        self.friend_count_by_level: Dict[str, int] = {}
        self.best_friend_id: Optional[str] = None
        self.pending_invitations: List[str] = []
    
    def generate_new_friend(self) -> DuckFriend:
        """Generate a new random friend duck."""
        personality = random.choice(list(DuckPersonalityType))
        names = DUCK_NAMES[personality.value]
        name = random.choice(names)
        
        # Ensure unique name
        existing_names = {f.name for f in self.friends.values()}
        while name in existing_names and len(existing_names) < len(names):
            name = random.choice(names)
        
        friend_id = f"friend_{len(self.friends)}_{random.randint(1000, 9999)}"
        
        # Random favorite food and activity
        foods = ["bread", "seeds", "berries", "worms", "algae", "fish"]
        activities = ["chat", "play", "swim", "explore", "nap", "eat"]
        
        friend = DuckFriend(
            id=friend_id,
            name=name,
            personality=personality,
            friendship_level=FriendshipLevel.STRANGER,
            favorite_food=random.choice(foods),
            favorite_activity=random.choice(activities),
            first_met=datetime.now().isoformat(),
        )
        
        self.friends[friend_id] = friend
        return friend
    
    def get_friend_by_id(self, friend_id: str) -> Optional[DuckFriend]:
        """Get a friend by their ID."""
        return self.friends.get(friend_id)
    
    def start_visit(self, friend_id: Optional[str] = None) -> Tuple[bool, str, Optional[VisitEvent]]:
        """Start a visit from a friend duck."""
        if self.current_visit:
            return False, "A friend is already visiting!", None
        
        # Get or generate friend
        if friend_id and friend_id in self.friends:
            friend = self.friends[friend_id]
        elif self.friends:
            # Random friend visits
            friend = random.choice(list(self.friends.values()))
        else:
            # Generate new friend
            friend = self.generate_new_friend()
        
        # Determine visit duration based on friendship level
        duration_map = {
            FriendshipLevel.STRANGER: 10,
            FriendshipLevel.ACQUAINTANCE: 15,
            FriendshipLevel.FRIEND: 25,
            FriendshipLevel.CLOSE_FRIEND: 35,
            FriendshipLevel.BEST_FRIEND: 45,
        }
        
        duration = duration_map.get(friend.friendship_level, 15)
        
        # Determine if they brought a gift
        gift_chance = 0.2 + (friend.friendship_points / 1000)
        brought_gift = random.random() < gift_chance
        gift = None
        if brought_gift:
            gifts = VISITOR_GIFTS.get(friend.personality.value, ["surprise_gift"])
            gift = random.choice(gifts)
        
        self.current_visit = VisitEvent(
            friend_id=friend.id,
            started_at=datetime.now().isoformat(),
            duration_minutes=duration,
            gift_brought=gift,
        )
        
        friend.times_visited += 1
        friend.last_visit = datetime.now().isoformat()
        self.total_visits += 1
        self.last_visitor_time = datetime.now().isoformat()
        
        gift_msg = f" They brought you a {gift}!" if gift else ""
        return True, f"🦆 {friend.name} is visiting!{gift_msg}", self.current_visit
    
    def interact_with_visitor(self, activity: str) -> Tuple[bool, str, int]:
        """Do an activity with the visiting friend."""
        if not self.current_visit:
            return False, "No one is visiting right now!", 0
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return False, "Friend not found!", 0
        
        # Calculate friendship points earned
        base_points = 10
        
        # Bonus for favorite activity
        if activity == friend.favorite_activity:
            base_points += 15
            message = f"{friend.name} loves this! +{base_points} friendship points!"
        else:
            message = f"You and {friend.name} enjoyed {activity}. +{base_points} friendship points!"
        
        # Record activity
        self.current_visit.activities_done.append(activity)
        
        # Add friendship points
        friend.friendship_points += base_points
        
        # Check for level up
        old_level = friend.friendship_level
        new_level = self._calculate_level(friend.friendship_points)
        
        if new_level != old_level:
            friend.friendship_level = new_level
            message += f"\n🎉 Friendship level up! {friend.name} is now your {new_level.value.replace('_', ' ')}!"
            
            # Add special memory
            friend.special_memories.append(
                f"Became {new_level.value.replace('_', ' ')} on {datetime.now().strftime('%Y-%m-%d')}"
            )
        
        return True, message, base_points
    
    def give_gift_to_visitor(self, item: str) -> Tuple[bool, str, int]:
        """Give a gift to the visiting friend."""
        if not self.current_visit:
            return False, "No one is visiting right now!", 0
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return False, "Friend not found!", 0
        
        # Check if it's their preferred gift type
        preferred = GIFT_PREFERENCES.get(friend.personality.value, [])
        
        if item in preferred:
            points = 30
            reaction = f"😍 {friend.name} LOVES this gift!"
        elif item == friend.favorite_food:
            points = 25
            reaction = f"🥰 {friend.name}'s favorite food! They're so happy!"
        else:
            points = 15
            reaction = f"😊 {friend.name} appreciates the gift!"
        
        friend.friendship_points += points
        friend.gifts_received += 1
        self.total_gifts_exchanged += 1
        
        return True, f"{reaction} +{points} friendship points!", points
    
    def receive_gift(self) -> Tuple[bool, str, Optional[str]]:
        """Receive the gift brought by a visitor."""
        if not self.current_visit or not self.current_visit.gift_brought:
            return False, "No gift to receive!", None
        
        gift = self.current_visit.gift_brought
        self.current_visit.gift_brought = None
        
        friend = self.friends.get(self.current_visit.friend_id)
        if friend:
            friend.gifts_given += 1
        
        self.total_gifts_exchanged += 1
        
        return True, f"🎁 You received: {gift}!", gift
    
    def end_visit(self) -> Tuple[bool, str, Dict]:
        """End the current visit."""
        if not self.current_visit:
            return False, "No active visit to end!", {}
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            self.current_visit = None
            return False, "Friend not found!", {}
        
        activities = len(self.current_visit.activities_done)
        summary = {
            "friend_name": friend.name,
            "activities_done": activities,
            "friendship_points": friend.friendship_points,
            "friendship_level": friend.friendship_level.value,
        }
        
        farewell_messages = [
            f"👋 {friend.name} waves goodbye! Come back soon!",
            f"🦆 {friend.name} quacks a cheerful farewell!",
            f"💫 {friend.name} waddles away happily!",
        ]
        
        self.current_visit = None
        
        return True, random.choice(farewell_messages), summary
    
    def _calculate_level(self, points: int) -> FriendshipLevel:
        """Calculate friendship level based on points."""
        if points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.BEST_FRIEND]:
            return FriendshipLevel.BEST_FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.CLOSE_FRIEND]:
            return FriendshipLevel.CLOSE_FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.FRIEND]:
            return FriendshipLevel.FRIEND
        elif points >= FRIENDSHIP_THRESHOLDS[FriendshipLevel.ACQUAINTANCE]:
            return FriendshipLevel.ACQUAINTANCE
        else:
            return FriendshipLevel.STRANGER
    
    def check_for_random_visitor(self, hour: int) -> Tuple[bool, Optional[str]]:
        """Check if a random visitor should appear."""
        if self.current_visit:
            return False, None
        
        # More likely during day hours
        if 8 <= hour <= 18:
            chance = 0.05  # 5% chance per check during day
        else:
            chance = 0.02  # 2% chance at night
        
        # More friends = more chances
        chance += len(self.friends) * 0.01
        
        if random.random() < chance:
            _, message, _ = self.start_visit()
            return True, message
        
        return False, None
    
    def get_friend_list(self) -> List[Dict]:
        """Get list of all friends with their info."""
        return [
            {
                "id": f.id,
                "name": f.name,
                "personality": f.personality.value,
                "level": f.friendship_level.value,
                "points": f.friendship_points,
                "visits": f.times_visited,
            }
            for f in sorted(
                self.friends.values(),
                key=lambda x: x.friendship_points,
                reverse=True
            )
        ]
    
    def render_friend_card(self, friend_id: str) -> List[str]:
        """Render a friend's info card."""
        friend = self.friends.get(friend_id)
        if not friend:
            return ["Friend not found!"]
        
        appearance = DUCK_APPEARANCES.get(friend.personality.value, {})
        
        level_stars = {
            FriendshipLevel.STRANGER: "☆☆☆☆☆",
            FriendshipLevel.ACQUAINTANCE: "★☆☆☆☆",
            FriendshipLevel.FRIEND: "★★☆☆☆",
            FriendshipLevel.CLOSE_FRIEND: "★★★★☆",
            FriendshipLevel.BEST_FRIEND: "★★★★★",
        }
        
        next_level_points = 0
        levels = list(FRIENDSHIP_THRESHOLDS.items())
        for i, (level, threshold) in enumerate(levels):
            if level == friend.friendship_level and i < len(levels) - 1:
                next_level_points = levels[i + 1][1]
                break
        
        progress = ""
        if next_level_points > 0:
            progress_pct = friend.friendship_points / next_level_points
            filled = int(progress_pct * 10)
            progress = f"[{'█' * filled}{'░' * (10 - filled)}] {friend.friendship_points}/{next_level_points}"
        
        lines = [
            "╔════════════════════════════════════╗",
            f"║  🦆 {friend.name:^28} ║",
            f"║  {appearance.get('color', 'yellow'):^32} ║",
            "╠════════════════════════════════════╣",
            f"║  Personality: {friend.personality.value:^17} ║",
            f"║  {level_stars.get(friend.friendship_level, '☆☆☆☆☆'):^32} ║",
            f"║  {friend.friendship_level.value.replace('_', ' ').title():^32} ║",
            "╠════════════════════════════════════╣",
            f"║  Visits: {friend.times_visited:^23} ║",
            f"║  Gifts Given: {friend.gifts_given:^18} ║",
            f"║  Gifts Received: {friend.gifts_received:^15} ║",
            "╠════════════════════════════════════╣",
            f"║  Likes: {friend.favorite_food}, {friend.favorite_activity:^15} ║",
        ]
        
        if progress:
            lines.append(f"║  {progress:^32} ║")
        
        lines.append("╚════════════════════════════════════╝")
        
        return lines
    
    def render_visit_screen(self) -> List[str]:
        """Render the current visit screen."""
        if not self.current_visit:
            return ["No visitor right now!"]
        
        friend = self.friends.get(self.current_visit.friend_id)
        if not friend:
            return ["Visitor not found!"]
        
        lines = [
            "╔═══════════════════════════════════════════════╗",
            f"║  🦆 VISITOR: {friend.name:^28}  ║",
            f"║  {friend.personality.value.title():^41}  ║",
            "╠═══════════════════════════════════════════════╣",
            f"║  Friendship: {friend.friendship_level.value.replace('_', ' ').title():^28}  ║",
            "║                                               ║",
            "║       .--.                                    ║",
            "║      (_ ^ _)                                  ║",
            "║      /`    '\\                                 ║",
            "║     (__)(____)                                ║",
            "║                                               ║",
            "╠═══════════════════════════════════════════════╣",
            "║  Activities:                                  ║",
        ]
        
        activities = self.current_visit.activities_done or ["None yet"]
        for activity in activities[-4:]:  # Show last 4 activities
            lines.append(f"║    • {activity:^37}  ║")
        
        if self.current_visit.gift_brought:
            lines.append("╠═══════════════════════════════════════════════╣")
            lines.append(f"║  🎁 Gift: {self.current_visit.gift_brought:^31}  ║")
        
        lines.extend([
            "╠═══════════════════════════════════════════════╣",
            "║  [C]hat  [P]lay  [G]ive Gift  [B]ye          ║",
            "╚═══════════════════════════════════════════════╝",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "friends": {
                fid: {
                    "id": f.id,
                    "name": f.name,
                    "personality": f.personality.value,
                    "friendship_level": f.friendship_level.value,
                    "friendship_points": f.friendship_points,
                    "times_visited": f.times_visited,
                    "gifts_given": f.gifts_given,
                    "gifts_received": f.gifts_received,
                    "favorite_food": f.favorite_food,
                    "favorite_activity": f.favorite_activity,
                    "first_met": f.first_met,
                    "last_visit": f.last_visit,
                    "special_memories": f.special_memories,
                    "unlocked_dialogue": f.unlocked_dialogue,
                }
                for fid, f in self.friends.items()
            },
            "current_visit": {
                "friend_id": self.current_visit.friend_id,
                "started_at": self.current_visit.started_at,
                "duration_minutes": self.current_visit.duration_minutes,
                "activities_done": self.current_visit.activities_done,
                "mood": self.current_visit.mood,
                "gift_brought": self.current_visit.gift_brought,
                "waiting_for_gift": self.current_visit.waiting_for_gift,
            } if self.current_visit else None,
            "total_visits": self.total_visits,
            "total_gifts_exchanged": self.total_gifts_exchanged,
            "last_visitor_time": self.last_visitor_time,
            "best_friend_id": self.best_friend_id,
            "pending_invitations": self.pending_invitations,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "FriendsSystem":
        """Create from dictionary."""
        system = cls()
        
        for fid, fdata in data.get("friends", {}).items():
            system.friends[fid] = DuckFriend(
                id=fdata["id"],
                name=fdata["name"],
                personality=DuckPersonalityType(fdata["personality"]),
                friendship_level=FriendshipLevel(fdata["friendship_level"]),
                friendship_points=fdata.get("friendship_points", 0),
                times_visited=fdata.get("times_visited", 0),
                gifts_given=fdata.get("gifts_given", 0),
                gifts_received=fdata.get("gifts_received", 0),
                favorite_food=fdata.get("favorite_food", "bread"),
                favorite_activity=fdata.get("favorite_activity", "chat"),
                first_met=fdata.get("first_met", ""),
                last_visit=fdata.get("last_visit", ""),
                special_memories=fdata.get("special_memories", []),
                unlocked_dialogue=fdata.get("unlocked_dialogue", []),
            )
        
        visit_data = data.get("current_visit")
        if visit_data:
            system.current_visit = VisitEvent(
                friend_id=visit_data["friend_id"],
                started_at=visit_data["started_at"],
                duration_minutes=visit_data["duration_minutes"],
                activities_done=visit_data.get("activities_done", []),
                mood=visit_data.get("mood", "happy"),
                gift_brought=visit_data.get("gift_brought"),
                waiting_for_gift=visit_data.get("waiting_for_gift", False),
            )
        
        system.total_visits = data.get("total_visits", 0)
        system.total_gifts_exchanged = data.get("total_gifts_exchanged", 0)
        system.last_visitor_time = data.get("last_visitor_time", "")
        system.best_friend_id = data.get("best_friend_id")
        system.pending_invitations = data.get("pending_invitations", [])
        
        return system


# Global friends system instance
friends_system = FriendsSystem()
