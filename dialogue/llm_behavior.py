"""
LLM Behavior Controller - Background threaded LLM for dynamic dialogue.
Provides non-blocking LLM generation with caching and fallback to templates.
LOCAL ONLY - uses bundled GGUF model, no external API calls.
"""
import threading
import queue
import time
import hashlib
import logging
from typing import Optional, Dict, List, Callable, Any, TYPE_CHECKING

# Configure logging for LLM behavior operations
logger = logging.getLogger(__name__)
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import OrderedDict

if TYPE_CHECKING:
    from duck.duck import Duck

# Import config module for dynamic access to settings
import config as llm_config

# Get config values with fallbacks
def _get_config(name: str, default):
    """Get config value with fallback."""
    return getattr(llm_config, name, default)


class RequestType(Enum):
    """Types of LLM requests."""
    ACTION_COMMENTARY = auto()
    VISITOR_DIALOGUE = auto()
    SPECIAL_EVENT = auto()
    PLAYER_CHAT = auto()


class RequestPriority(Enum):
    """Priority levels for LLM requests."""
    LOW = 0       # Background pre-generation
    NORMAL = 1    # Regular requests
    HIGH = 2      # User-initiated or time-sensitive


@dataclass
class LLMRequest:
    """A request for LLM generation."""
    request_type: RequestType
    priority: RequestPriority
    context: Dict[str, Any]
    callback: Optional[Callable[[Optional[str]], None]] = None
    created_at: float = field(default_factory=time.time)
    
    def __lt__(self, other: "LLMRequest") -> bool:
        """Compare by priority (higher priority first)."""
        return self.priority.value > other.priority.value


@dataclass
class CacheEntry:
    """A cached LLM response."""
    response: str
    created_at: float
    context_hash: str


class ResponseCache:
    """LRU cache with TTL for LLM responses."""
    
    def __init__(self, max_size: int = None, ttl: float = None):
        if max_size is None:
            max_size = _get_config('LLM_CACHE_SIZE', 100)
        if ttl is None:
            ttl = _get_config('LLM_CACHE_TTL', 60)
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.Lock()
    
    def _make_key(self, context: Dict[str, Any]) -> str:
        """Create a cache key from context dict."""
        # Sort keys for consistent hashing
        sorted_items = sorted(context.items())
        key_string = str(sorted_items)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, context: Dict[str, Any]) -> Optional[str]:
        """Get cached response if available and not expired."""
        key = self._make_key(context)
        
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check TTL
            if time.time() - entry.created_at > self._ttl:
                del self._cache[key]
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            return entry.response
    
    def put(self, context: Dict[str, Any], response: str):
        """Store a response in cache."""
        key = self._make_key(context)
        
        with self._lock:
            # Remove oldest if at capacity
            while len(self._cache) >= self._max_size:
                self._cache.popitem(last=False)
            
            self._cache[key] = CacheEntry(
                response=response,
                created_at=time.time(),
                context_hash=key
            )
    
    def clear(self):
        """Clear all cached responses."""
        with self._lock:
            self._cache.clear()
    
    def cleanup_expired(self):
        """Remove expired entries."""
        now = time.time()
        with self._lock:
            expired = [k for k, v in self._cache.items() 
                      if now - v.created_at > self._ttl]
            for key in expired:
                del self._cache[key]


class ContextBuilder:
    """Builds compact context dicts for LLM prompts."""
    
    @staticmethod
    def build_action_context(duck: "Duck", action: str, 
                             weather: str = "clear",
                             time_of_day: str = "day",
                             recent_events: List[str] = None) -> Dict[str, Any]:
        """Build context for action commentary."""
        return {
            "type": "action",
            "duck_name": duck.name,
            "action": action,
            "mood": duck.get_mood().state.value if duck.get_mood() else "content",
            "weather": weather,
            "time_of_day": time_of_day,
            "personality_hash": hash(frozenset(duck.personality.items())) % 1000,
        }
    
    @staticmethod
    def build_visitor_context(duck: "Duck", visitor_name: str,
                              visitor_personality: str,
                              friendship_level: str,
                              shared_memories: List[str],
                              conversation_phase: str) -> Dict[str, Any]:
        """Build context for visitor dialogue."""
        return {
            "type": "visitor",
            "duck_name": duck.name,
            "visitor_name": visitor_name,
            "visitor_personality": visitor_personality,
            "friendship_level": friendship_level,
            "memories_count": len(shared_memories) if shared_memories else 0,
            "conversation_phase": conversation_phase,
        }
    
    @staticmethod
    def build_event_context(duck: "Duck", event_type: str,
                            event_details: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for special events."""
        return {
            "type": "event",
            "duck_name": duck.name,
            "event_type": event_type,
            "mood": duck.get_mood().state.value if duck.get_mood() else "content",
            **event_details
        }


class LLMWorker(threading.Thread):
    """Background thread for non-blocking LLM generation."""
    
    def __init__(self, controller: "LLMBehaviorController"):
        super().__init__(daemon=True, name="LLMWorker")
        self._controller = controller
        self._request_queue: queue.PriorityQueue = queue.PriorityQueue()
        self._running = False
        self._llm = None
        self._duck = None  # Reference to current duck
    
    def set_duck(self, duck: "Duck"):
        """Set the duck reference for generation."""
        self._duck = duck
    
    def start_worker(self):
        """Start the worker thread."""
        if not self._running:
            self._running = True
            self.start()
    
    def stop_worker(self):
        """Stop the worker thread."""
        self._running = False
        # Add a poison pill to wake up the queue
        try:
            self._request_queue.put_nowait((999, None))
        except queue.Full:
            pass
    
    def queue_request(self, request: LLMRequest) -> bool:
        """Add a request to the queue. Returns False if queue is full."""
        max_queue = _get_config('LLM_MAX_QUEUE_DEPTH', 3)
        if self._request_queue.qsize() >= max_queue:
            return False
        
        # Priority queue uses tuples: (priority_value, request)
        # Lower number = higher priority, so we negate
        priority = -request.priority.value
        self._request_queue.put((priority, request))
        return True
    
    def queue_size(self) -> int:
        """Get current queue size."""
        return self._request_queue.qsize()
    
    def run(self):
        """Main worker loop."""
        # Lazy import to avoid circular imports
        from dialogue.llm_chat import get_llm_chat
        self._llm = get_llm_chat()
        
        while self._running:
            try:
                # Wait for request with timeout
                priority, request = self._request_queue.get(timeout=1.0)
                
                if request is None:
                    # Poison pill - exit
                    break
                
                # Process the request
                response = self._process_request(request)
                
                # Store in cache
                if response:
                    self._controller._cache.put(request.context, response)
                
                # Call callback if provided
                if request.callback:
                    try:
                        request.callback(response)
                    except Exception as callback_error:
                        logger.warning(f"Callback error: {callback_error}")
                
                self._request_queue.task_done()
                
            except queue.Empty:
                # Timeout - cleanup expired cache entries
                self._controller._cache.cleanup_expired()
            except Exception as e:
                # Log error but keep running
                logger.error(f"LLM worker error: {e}")
    
    def _process_request(self, request: LLMRequest) -> Optional[str]:
        """Process a single LLM request."""
        if not self._llm or not self._llm.is_available():
            return None
        
        if not self._duck:
            return None
        
        context = request.context
        
        try:
            if request.request_type == RequestType.ACTION_COMMENTARY:
                return self._llm.generate_action_commentary(
                    self._duck,
                    context.get("action", "idle"),
                    {
                        "mood": context.get("mood", "content"),
                        "weather": context.get("weather", "clear"),
                        "time_of_day": context.get("time_of_day", "day"),
                    }
                )
            
            elif request.request_type == RequestType.VISITOR_DIALOGUE:
                return self._llm.generate_visitor_dialogue(
                    self._duck,
                    context.get("visitor_name", "Friend"),
                    context.get("visitor_personality", "playful"),
                    context.get("friendship_level", "acquaintance"),
                    context.get("shared_memories", []),
                    context.get("conversation_phase", "main"),
                )
            
            elif request.request_type == RequestType.SPECIAL_EVENT:
                # For now, use action commentary with event details
                return self._llm.generate_action_commentary(
                    self._duck,
                    context.get("event_type", "event"),
                    context
                )
            
        except Exception as e:
            logger.error(f"Error processing LLM request {request.request_type}: {e}")
            return None
        
        return None


class LLMBehaviorController:
    """
    Coordinates all LLM usage across duck behavior and visitors.
    Manages caching, queueing, and fallback to templates.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._cache = ResponseCache()
        self._worker = LLMWorker(self)
        self._duck = None
        self._pending_responses: Dict[str, Optional[str]] = {}
        self._fallback_templates: Dict[str, List[str]] = {}
        
        # Start worker thread
        if _get_config('LLM_ENABLED', True) and _get_config('LLM_BEHAVIOR_ENABLED', True):
            self._worker.start_worker()
    
    def set_duck(self, duck: "Duck"):
        """Set the current duck for generation."""
        self._duck = duck
        self._worker.set_duck(duck)
    
    def is_available(self) -> bool:
        """Check if LLM behavior is available."""
        from dialogue.llm_chat import get_llm_chat
        return _get_config('LLM_ENABLED', True) and _get_config('LLM_BEHAVIOR_ENABLED', True) and get_llm_chat().is_available()
    
    def register_fallback_templates(self, action: str, templates: List[str]):
        """Register fallback templates for an action type."""
        self._fallback_templates[action] = templates
    
    def request_action_commentary(self, duck: "Duck", action: str,
                                   weather: str = "clear",
                                   time_of_day: str = "day",
                                   fallback: str = None,
                                   callback: Callable[[str], None] = None) -> str:
        """
        Request action commentary with seamless fallback.
        
        Returns immediately with cached/fallback response.
        If LLM generates later, callback is called.
        """
        import random
        
        # Check if LLM should be used (probability gating)
        llm_enabled = _get_config('LLM_ENABLED', True)
        behavior_enabled = _get_config('LLM_BEHAVIOR_ENABLED', True)
        action_chance = _get_config('LLM_ACTION_CHANCE', 0.7)
        use_llm = llm_enabled and behavior_enabled and random.random() < action_chance
        
        if not use_llm:
            return fallback or self._get_fallback(action)
        
        # Build context
        context = ContextBuilder.build_action_context(
            duck, action, weather, time_of_day
        )
        
        # Check cache first
        cached = self._cache.get(context)
        if cached:
            return cached
        
        # Queue LLM request
        request = LLMRequest(
            request_type=RequestType.ACTION_COMMENTARY,
            priority=RequestPriority.NORMAL,
            context=context,
            callback=callback
        )
        
        if self._worker.queue_request(request):
            # Request queued - return fallback for now
            return fallback or self._get_fallback(action)
        else:
            # Queue full - use fallback
            return fallback or self._get_fallback(action)
    
    def request_visitor_dialogue(self, duck: "Duck", visitor_name: str,
                                  visitor_personality: str,
                                  friendship_level: str,
                                  shared_memories: List[str],
                                  conversation_phase: str,
                                  fallback: str = None,
                                  callback: Callable[[str], None] = None) -> str:
        """
        Request visitor dialogue with seamless fallback.
        """
        import random
        
        # Check if LLM should be used
        llm_enabled = _get_config('LLM_ENABLED', True)
        visitor_enabled = _get_config('LLM_VISITOR_ENABLED', True)
        visitor_chance = _get_config('LLM_VISITOR_CHANCE', 0.8)
        use_llm = llm_enabled and visitor_enabled and random.random() < visitor_chance
        
        if not use_llm:
            return fallback or f"*{visitor_name} looks around thoughtfully*"
        
        # Build context
        context = ContextBuilder.build_visitor_context(
            duck, visitor_name, visitor_personality,
            friendship_level, shared_memories, conversation_phase
        )
        
        # Check cache
        cached = self._cache.get(context)
        if cached:
            return cached
        
        # Queue request
        request = LLMRequest(
            request_type=RequestType.VISITOR_DIALOGUE,
            priority=RequestPriority.NORMAL,
            context=context,
            callback=callback
        )
        
        if self._worker.queue_request(request):
            return fallback or f"*{visitor_name} smiles*"
        else:
            return fallback or f"*{visitor_name} looks around*"
    
    def request_special_event(self, duck: "Duck", event_type: str,
                               event_details: Dict[str, Any],
                               fallback: str = None,
                               callback: Callable[[str], None] = None) -> str:
        """
        Request special event dialogue (always uses LLM if available).
        """
        import random
        
        llm_enabled = _get_config('LLM_ENABLED', True)
        event_chance = _get_config('LLM_SPECIAL_EVENT_CHANCE', 1.0)
        use_llm = llm_enabled and random.random() < event_chance
        
        if not use_llm:
            return fallback or f"*Something special happens!*"
        
        context = ContextBuilder.build_event_context(duck, event_type, event_details)
        
        cached = self._cache.get(context)
        if cached:
            return cached
        
        request = LLMRequest(
            request_type=RequestType.SPECIAL_EVENT,
            priority=RequestPriority.HIGH,  # Higher priority for special events
            context=context,
            callback=callback
        )
        
        if self._worker.queue_request(request):
            return fallback or "*..."
        else:
            return fallback or "*Something happens*"
    
    def _get_fallback(self, action: str) -> str:
        """Get a fallback template for an action."""
        import random
        
        templates = self._fallback_templates.get(action, [])
        if templates:
            return random.choice(templates)
        
        # Default fallbacks
        default_fallbacks = {
            "waddle": [
                "*waddles around*",
                "*waddles with purpose... no wait, lost it*",
                "*waddle waddle waddle* ...this is my whole thing apparently",
                "*waddles in a circle* ...déjà vu",
                "*waddles aggressively* this is as fast as i go",
                "*waddles to the left* *waddles to the right* *existential waddle*",
                "*waddles nowhere in particular* the journey is the destination or whatever",
                "*one waddle* ...that's enough cardio for today",
                "*waddles with dramatic flair* i'm basically a runway model",
                "*waddles into a wall* meant to do that",
            ],
            "quack": [
                "*quack*",
                "*quack* ...profound, i know",
                "*halfhearted quack*",
                "*quack quack* that's duck for 'leave me alone'",
                "*single dignified quack*",
                "*quacks into the void* the void does not quack back",
                "*tiny quack* ...sorry, was that too loud",
                "*quack* i said what i said",
                "*aggressive quack* ...don't test me",
                "*quacks softly* this is my inside quack",
            ],
            "splash": [
                "*splash splash*",
                "*splashes water halfheartedly* ...riveting",
                "*tiny splash* ...masterpiece",
                "*splash* *gets self wet* *surprised pikachu face*",
                "*splashes dramatically* i am one with the water",
                "*splish* ...too tired for full splash",
                "*splash splash splash* ...okay that was actually fun",
                "*cannonball* ...or the duck equivalent",
                "*gentle ripple* that was a splash. trust me.",
            ],
            "preen": [
                "*preens feathers*",
                "*preens feathers* gotta look good for no one in particular",
                "*adjusts single feather* perfection takes time",
                "*preening* this feather has been bugging me ALL day",
                "*aggressive preening* self-care is not optional",
                "*preens* *finds snack crumb in feathers* nice",
                "*preens half-heartedly* good enough for government work",
                "*preens feathers meticulously* i am a work of art",
                "*preens* i woke up like this. but also this helps.",
            ],
            "nap": [
                "*zzzz*",
                "*naps with one eye open* trust no one",
                "*falls asleep mid-thought* ...zzzz",
                "*power nap* five minutes is all i need... *three hours later*",
                "*napping aggressively* do NOT wake me",
                "*sleepy quack* ...zzz...",
                "*curls up* the world can wait",
                "*snoring softly* ...this is my most productive state",
                "*naps standing up* a skill, honestly",
                "*dreams of bread* ...zzz... *quacks in sleep*",
            ],
            "explore": [
                "*looks around curiously*",
                "*looks around* ...same pond as yesterday. groundbreaking.",
                "*investigates suspicious leaf* ...it's a leaf",
                "*explores corner* found dust. adding to collection.",
                "*peers behind thing* nothing. as expected. as always.",
                "*ventures two feet to the left* uncharted territory",
                "*sniffs around* something is different... no wait, it's the same",
                "*wanders* i'm not lost. i'm discovering.",
                "*exploring* found a rock. it's mine now.",
                "*looks under thing* there's nothing here but i needed to check",
            ],
            "eat": [
                "*nom nom*",
                "*eats* this is fine. everything is fine.",
                "*monch* ...acceptable",
                "*nibbles* i've had better. i've had worse. this is.",
                "*eats crumb* the feast of a lifetime",
                "*nom* calories are just energy points. i need those.",
                "*chewing thoughtfully* ...needs salt",
                "*eats like nobody's watching* ...because nobody is",
                "*tiny bite* savoring the mediocrity",
                "*nom nom nom* don't judge me",
            ],
            "play": [
                "*having fun*",
                "*having what could loosely be described as fun*",
                "*plays* ...is this fun? i think this is fun",
                "*bats at thing* entertainment achieved",
                "*plays by self* introverts unite. separately.",
                "*chases own tail* a classic for a reason",
                "*plays half-heartedly* i'm participating. you're welcome.",
                "*bounces thing* again. again. the dopamine demands it.",
                "*making own fun* nobody else is gonna do it",
            ],
            "swim": [
                "*glides across water* born for this",
                "*paddles in circle* the world's smallest whirlpool",
                "*floats* achieving peak duck performance",
                "*swims laps* ...one. that's enough laps.",
                "*dips below surface* *pops back up* still here unfortunately",
                "*backstroke* this is the life. this is literally the whole life.",
                "*swimming* feet going crazy under the water but i look SERENE up top",
                "*drifts aimlessly* current situation: going with the current",
                "*splashes into water* nailed the landing",
            ],
            "think": [
                "*stares into middle distance* ...processing",
                "*thinking* ...this could take a while",
                "*contemplates existence* ...yep, still existing",
                "*has a thought* ...and it's gone",
                "*deep in thought* the deepest. uncharted thought depths.",
                "*ponders* why ARE we here... in this pond specifically",
                "*thinking hard* you can almost see the gears turning. almost.",
                "*philosophical stare* what IS a duck, really",
                "*zones out* ...i was thinking about bread again",
            ],
            "sulk": [
                "*sits in corner* this is fine",
                "*sulking* ...not that anyone would notice",
                "*mopes* the world is a pond and the pond is empty",
                "*dramatic sigh* nobody understands the struggle",
                "*sulks quietly* making it everyone else's problem by proximity",
                "*stares at ground* the ground gets it",
                "*turns back to everyone* i need a moment. or several.",
                "*sad quack* ...that was involuntary",
                "*sulking intensifies* this isn't even my final form of sadness",
            ],
            "beg": [
                "*big eyes* ...please?",
                "*stares at food* ...i'm not begging. this is... assertive requesting.",
                "*pathetic quack* ...bread? ...anyone? ...bread?",
                "*sits pretty* i learned this for exactly this purpose",
                "*tilts head adorably* this face has a 73% success rate",
                "*begging* not proud of this. but not above it either.",
                "*puppy eyes but duck* ...it's less effective with a beak",
                "*nudges hand* ...just checking if food falls out",
                "*quacks softly* i haven't eaten in hours. HOURS.",
            ],
            "hide": [
                "*hides behind smallest possible object*",
                "*disappears* ...or tries to. ducks are not stealthy.",
                "*hides* you can't see me if i can't see you. that's the rule.",
                "*tucked behind rock* i live here now",
                "*camouflage attempt* *fails* ...i'm yellow",
                "*hides under wing* invisible. definitely invisible.",
                "*crouching behind blade of grass* am i hidden? ...no? okay.",
                "*retreats into feathers* the world can find someone else",
                "*hiding* this is tactical. not cowardly. TACTICAL.",
            ],
            "stretch": [
                "*stretches wings* ...magnificent wingspan if i say so myself",
                "*big stretch* every feather participating",
                "*stretches one leg* ...now the other... forgot how legs work for a second",
                "*yawns and stretches* the full reset",
                "*stretches neck* crack. that's concerning. moving on.",
                "*morning stretch* ...at 3 PM. don't judge.",
                "*stretches dramatically* i contain multitudes. and stiff joints.",
                "*full body stretch* EXPANDED",
                "*stretches* the only exercise i believe in",
            ],
            "dance": [
                "*shuffles feet* ...this is dancing. accept it.",
                "*wiggles* the rhythm is in me. it's just shy.",
                "*head bobs* this is my whole routine",
                "*spins once* ...okay dizzy. worth it.",
                "*does the duck walk* a classic. timeless. iconic.",
                "*dances like nobody's watching* because they're not. hopefully.",
                "*grooves* *trips* *plays it off* that was CHOREOGRAPHY",
                "*tail waggle* that's the encore. show's over.",
                "*rhythmic waddling* is this a dance? i've decided it is.",
            ],
            "stare": [
                "*stares* ...what. WHAT.",
                "*unblinking gaze* i can do this all day",
                "*stares at nothing* it's staring back and it's WINNING",
                "*stares judgmentally* ...i'm not judging. this is just my face.",
                "*thousand yard stare* i've seen things. mostly bread.",
                "*stares at wall* the wall understands me",
                "*makes eye contact* *refuses to break it* this is a power move",
                "*staring contest with inanimate object* ...i lost",
                "*blank stare* the screensaver has kicked in",
            ],
        }
        
        options = default_fallbacks.get(action, [f"*{action}s*"])
        return random.choice(options) if isinstance(options, list) else options
    
    def get_status(self) -> Dict[str, Any]:
        """Get current controller status."""
        from dialogue.llm_chat import get_llm_chat
        llm = get_llm_chat()
        
        return {
            "enabled": _get_config('LLM_ENABLED', True) and _get_config('LLM_BEHAVIOR_ENABLED', True),
            "llm_available": llm.is_available() if llm else False,
            "model_name": llm.get_model_name() if llm else "None",
            "gpu_layers": llm.get_gpu_layers() if llm else 0,
            "queue_size": self._worker.queue_size(),
            "cache_size": len(self._cache._cache),
        }
    
    def shutdown(self):
        """Shutdown the controller and worker thread."""
        self._worker.stop_worker()
        # Wait for worker thread to finish (with timeout to avoid hanging)
        if self._worker.is_alive():
            self._worker.join(timeout=5.0)
        self._cache.clear()


# Global instance getter
_controller_instance = None


def get_behavior_controller() -> LLMBehaviorController:
    """Get or create the behavior controller singleton."""
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = LLMBehaviorController()
    return _controller_instance
