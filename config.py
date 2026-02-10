"""
Game configuration and constants for Cheese the Duck.
"""
from pathlib import Path

# Paths
GAME_DIR = Path(__file__).parent
DATA_DIR = GAME_DIR / "data"
SAVE_DIR = Path.home() / ".cheese_the_duck"
SAVE_FILE = SAVE_DIR / "save.json"

# Default duck name
DEFAULT_DUCK_NAME = "Cheese"

# Game timing
FPS = 60
TICK_RATE = 1.0  # Seconds between game ticks
TIME_MULTIPLIER = 1.0  # Speed up time for testing (1.0 = real time)

# Need decay rates (per real minute)
# Designed for ~8 hour decay from full to empty
# 100% / rate = minutes to empty
NEED_DECAY_RATES = {
    "hunger": 0.21,     # ~8 hours to empty from full (100/0.21 = 476 min)
    "energy": 0.12,     # ~14 hours to empty from full  
    "fun": 0.21,        # ~8 hours to empty from full
    "cleanliness": 0.08, # ~21 hours to empty (stays clean longest)
    "social": 0.21,     # ~8 hours to empty from full
}

# Need thresholds
NEED_MAX = 100
NEED_MIN = 0
NEED_CRITICAL = 20  # Below this, urgent warnings
NEED_LOW = 40       # Below this, duck gets grumpy

# Interaction effects (balanced - should require multiple interactions to fully satisfy a need)
INTERACTION_EFFECTS = {
    "feed": {"hunger": 18, "fun": 2},
    "play": {"fun": 15, "energy": -5, "social": 5},
    "clean": {"cleanliness": 20, "fun": -2},
    "pet": {"social": 12, "fun": 5},
    "sleep": {"energy": 25, "hunger": -3},
}

# Mood thresholds (based on weighted need average)
MOOD_THRESHOLDS = {
    "ecstatic": 90,
    "happy": 70,
    "content": 50,
    "grumpy": 30,
    "sad": 10,
    "miserable": 0,
}

# Mood weights for need calculation
MOOD_WEIGHTS = {
    "hunger": 0.25,
    "energy": 0.25,
    "fun": 0.20,
    "cleanliness": 0.15,
    "social": 0.15,
}

# Growth stages (in real hours to reach next stage)
# Based on aging.py day ranges: hatchling(0-3d), duckling(3-14d), juvenile(14-30d),
# young_adult(30-90d), adult(90-365d), mature(365-730d), elder(730-1095d), legendary(1095+)
GROWTH_STAGES = {
    "egg": {"duration_hours": 0.5, "next": "hatchling"},
    "hatchling": {"duration_hours": 72, "next": "duckling"},      # 3 days
    "duckling": {"duration_hours": 264, "next": "juvenile"},      # 11 days (3-14)
    "juvenile": {"duration_hours": 384, "next": "young_adult"},   # 16 days (14-30)
    "young_adult": {"duration_hours": 1440, "next": "adult"},     # 60 days (30-90)
    "adult": {"duration_hours": 6600, "next": "mature"},          # 275 days (90-365)
    "mature": {"duration_hours": 8760, "next": "elder"},          # 365 days (365-730)
    "elder": {"duration_hours": 8760, "next": "legendary"},       # 365 days (730-1095)
    "legendary": {"duration_hours": None, "next": None},          # Final stage
    # Legacy mappings for old saves
    "teen": {"duration_hours": 384, "next": "young_adult"},       # Maps to juvenile->young_adult
}

# Personality trait ranges
PERSONALITY_MIN = -100
PERSONALITY_MAX = 100

# Default personality (slightly derpy duck)
DEFAULT_PERSONALITY = {
    "clever_derpy": -30,   # Leaning derpy
    "brave_timid": 0,      # Neutral
    "active_lazy": 20,     # Slightly active
    "social_shy": 30,      # Fairly social
    "neat_messy": -20,     # Bit messy
}

# AI behavior settings
AI_IDLE_INTERVAL = 15.0    # Seconds between autonomous actions (feels more natural)
AI_RANDOMNESS = 0.3        # Base randomness in action selection
DERPY_RANDOMNESS_BONUS = 0.4  # Extra randomness for derpy ducks

# Offline progression
MAX_OFFLINE_HOURS = 8760   # Cap offline time processing (1 year — effectively uncapped)
MAX_OFFLINE_NEED_HOURS = 24  # Needs never decay worse than 1 bad day
OFFLINE_DECAY_MULTIPLIER = 0.5  # Needs decay slower offline

# UI Colors (for blessed terminal)
COLORS = {
    "duck_body": "yellow",
    "duck_beak": "bright_yellow",
    "happy": "green",
    "sad": "blue",
    "hungry": "red",
    "tired": "magenta",
    "dirty": "white",
    "border": "cyan",
    "text": "white",
    "highlight": "bright_white",
}

# Duck names for random selection (Cheese is default, not in this list)
DUCK_NAMES = [
    "Quackers", "Waddles", "Ducky", "Puddles", "Feathers",
    "Bubbles", "Nugget", "Pickle", "Biscuit", "Cheddar",
    "Sprocket", "Waffles", "Noodle", "Potato", "Beans",
]

# ===== LLM SETTINGS =====
# Core LLM Configuration
LLM_ENABLED = True              # Master switch for all LLM features
LLM_LOCAL_ONLY = True           # ONLY use local GGUF model (no Ollama/external)

# Model directory - use user-writable location for system installs
def _get_model_dir():
    """Get model directory, using user home for system installs."""
    game_path = str(GAME_DIR)
    if game_path.startswith('/opt/') or game_path.startswith('/usr/') or game_path.startswith('/snap/'):
        # System install - use user's home directory
        user_model_dir = Path.home() / ".local" / "share" / "cheese-the-duck" / "models"
        user_model_dir.mkdir(parents=True, exist_ok=True)
        return user_model_dir
    else:
        # Local install - use game directory
        return GAME_DIR / "models"

LLM_MODEL_DIR = _get_model_dir()

# GPU Acceleration (auto-detect if -1, or specify layer count)
LLM_GPU_LAYERS = 0              # 0 = CPU only (set to -1 after reinstalling llama-cpp-python with CUDA)

# Model Parameters
LLM_CONTEXT_SIZE = 2048         # Context window size
LLM_MAX_TOKENS = 100            # Max tokens for behavior commentary
LLM_MAX_TOKENS_CHAT = 150       # Max tokens for player chat
LLM_TEMPERATURE = 0.8           # Response creativity (0.0-1.0)

# LLM Behavior Integration  
LLM_BEHAVIOR_ENABLED = True     # Use LLM for duck action commentary
LLM_VISITOR_ENABLED = True      # Use LLM for visitor dialogue
LLM_ACTION_CHANCE = 0.7         # 70% of actions use LLM (rest use templates)
LLM_VISITOR_CHANCE = 0.8        # 80% of visitor lines use LLM
LLM_SPECIAL_EVENT_CHANCE = 1.0  # Always use LLM for special moments

# Caching & Performance
LLM_CACHE_SIZE = 100            # Max cached responses
LLM_CACHE_TTL = 60              # Seconds before cache entry expires
LLM_MAX_QUEUE_DEPTH = 3         # Max pending LLM requests before fallback
LLM_WORKER_TIMEOUT = 10.0       # Max seconds to wait for LLM response

# Conversation Memory
LLM_MAX_HISTORY = 6             # Messages to keep in conversation history


# ===== GAMEPLAY CONSTANTS =====
# Timing (seconds)
EXPLORATION_COOLDOWN = 30           # Cooldown between explorations
DEFAULT_EVENT_COOLDOWN = 300        # Default event cooldown (5 minutes)
DAILY_COOLDOWN = 86400              # 24 hours in seconds
HOURLY_COOLDOWN = 3600              # 1 hour in seconds
MUSIC_COOLDOWN_MIN = 120            # Min seconds between music loops
MUSIC_COOLDOWN_MAX = 300            # Max seconds between music loops

# XP Rewards
BASE_EXPLORATION_XP = 5             # XP per exploration
XP_PER_BUILD_STAGE = 20             # XP per building stage completed
RARE_DISCOVERY_XP_BONUS = 20        # Bonus XP for rare discoveries
NEW_AREA_XP_BONUS = 50              # Bonus XP for discovering new areas

# Skill Thresholds (XP required for each level 1-10)
BUILDING_SKILL_THRESHOLDS = [0, 40, 120, 280, 500, 800, 1200, 1700, 2400, 3200]
GATHERING_SKILL_THRESHOLDS = [0, 50, 150, 300, 500, 800, 1200, 1800, 2500, 3500]
CRAFTING_SKILL_THRESHOLDS = [0, 50, 150, 350, 600, 1000, 1500, 2200, 3000, 4000]

# Rates and Chances
AREA_DISCOVERY_CHANCE = 0.1         # 10% chance to discover new area
CRAFTING_CANCEL_REFUND_RATE = 0.5   # 50% material refund on cancel
UPGRADE_MATERIAL_RECOVERY = 0.5     # 50% materials recovered when upgrading
RAINY_DAY_CHANCE = 0.05             # 5% chance for special rainy day event
