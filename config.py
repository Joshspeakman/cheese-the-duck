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
FPS = 30
TICK_RATE = 1.0  # Seconds between game ticks
TIME_MULTIPLIER = 1.0  # Speed up time for testing (1.0 = real time)

# Need decay rates (per real minute)
# Designed so needs last ~8-12 hours from full
# 100% / rate = minutes to empty
NEED_DECAY_RATES = {
    "hunger": 0.15,     # ~11 hours to empty from full
    "energy": 0.12,     # ~14 hours to empty from full  
    "fun": 0.18,        # ~9 hours to empty (boredom is faster)
    "cleanliness": 0.08, # ~21 hours to empty (stays clean longest)
    "social": 0.10,     # ~17 hours to empty
}

# Need thresholds
NEED_MAX = 100
NEED_MIN = 0
NEED_CRITICAL = 20  # Below this, urgent warnings
NEED_LOW = 40       # Below this, duck gets grumpy

# Interaction effects
INTERACTION_EFFECTS = {
    "feed": {"hunger": 35, "fun": 5},
    "play": {"fun": 30, "energy": -10, "social": 10},
    "clean": {"cleanliness": 40, "fun": -5},
    "pet": {"social": 25, "fun": 10},
    "sleep": {"energy": 50, "hunger": -5},
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
GROWTH_STAGES = {
    "egg": {"duration_hours": 0.5, "next": "duckling"},
    "duckling": {"duration_hours": 24, "next": "teen"},
    "teen": {"duration_hours": 72, "next": "adult"},
    "adult": {"duration_hours": 168, "next": "elder"},
    "elder": {"duration_hours": None, "next": None},
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
MAX_OFFLINE_HOURS = 24     # Cap offline time processing
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
LLM_MODEL_DIR = GAME_DIR / "models"  # Directory containing .gguf files

# GPU Acceleration (auto-detect if -1, or specify layer count)
LLM_GPU_LAYERS = -1             # -1 = auto-detect, 0 = CPU only, >0 = specific layers

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
