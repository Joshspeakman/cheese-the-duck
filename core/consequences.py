"""
Consequence Engine — makes neglect matter and care rewarding.

See dialogue/seaman_style.py for the voice golden rules.
All player-facing text must sound like Cheese.

Three escalation stages:
  Stage 1: Any need at 0 for 1+ hour → mood tanks, duck complains
  Stage 2: 2+ needs at 0 for 4+ hours → sick, can't play/learn, needs medicine
  Stage 3: Sick + untreated 24+ hours → hiding, needs 3 coaxing visits

Need cascading: low hunger drains energy 1.5×, low social drains fun 1.5×.

Trust: grows +0.3/day of good care, +0.05/interaction. Decays during absence.
"""
import time
import random
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

from config import NEED_CRITICAL


# ── Consequence timing thresholds (minutes) ─────────────────────────────
# These are BASE values — multiplied by growth stage modifiers
STAGE1_MINUTES = 60        # 1 hour at 0 → complain + mood tank
STAGE2_MINUTES = 240       # 4 hours at 0 (2+ needs) → sickness
STAGE3_MINUTES = 1440      # 24 hours sick + untreated → hiding
COAX_VISITS_NEEDED = 3     # Separate sessions to bring duck back from hiding

# Trust constants
TRUST_MIN = 0.0
TRUST_MAX = 100.0
TRUST_PER_INTERACTION = 0.05     # Tiny bit per feed/play/pet/clean
TRUST_GOOD_DAY_BONUS = 0.3      # All needs > 40 at session end
TRUST_SICK_CURE_BONUS = 1.0     # Curing sickness with medicine
TRUST_COAX_RETURN_BONUS = 2.0   # Successfully coaxing duck out of hiding

# Need cascade multipliers
CASCADE_HUNGER_TO_ENERGY = 1.5   # Low hunger → energy decays this much faster
CASCADE_SOCIAL_TO_FUN = 1.5      # Low social → fun decays this much faster
CASCADE_THRESHOLD = 20           # Below this value, cascade kicks in

# Sickness effects
SICKNESS_DECAY_MULTIPLIER = 1.5  # All needs decay faster when sick
SICKNESS_NATURAL_CURE_MINUTES = 120  # 2 hours of good care cures sickness
SICKNESS_CURE_THRESHOLD = 40     # All needs must be above this to natural-cure


@dataclass
class ConsequenceState:
    """Snapshot of the consequence system for UI display."""
    stage: int                  # 0=fine, 1=complaining, 2=sick, 3=hiding
    is_sick: bool
    is_hiding: bool
    is_cold_shoulder: bool
    trust: float
    trust_level: str            # "hostile" through "bonded"
    neglect_warnings: List[str] # Duck-voiced complaint messages
    sickness_message: Optional[str]


def get_trust_level(trust: float) -> str:
    """Convert trust value to a named level.
    
    These labels are displayed in the UI and referenced by
    content-gating systems (tricks, genuine moments, etc.).
    """
    if trust >= 90:
        return "bonded"
    elif trust >= 70:
        return "devoted"
    elif trust >= 50:
        return "close"
    elif trust >= 35:
        return "friendly"
    elif trust >= 20:
        return "familiar"
    elif trust >= 10:
        return "wary"
    else:
        return "distant"


def get_trust_level_display(trust: float) -> str:
    """Get a display-friendly trust level string."""
    level = get_trust_level(trust)
    displays = {
        "bonded": "Bonded",
        "devoted": "Devoted",
        "close": "Close Friend",
        "friendly": "Friendly",
        "familiar": "Familiar",
        "wary": "Wary",
        "distant": "Distant",
    }
    return displays.get(level, level.title())


def clamp_trust(value: float) -> float:
    """Clamp trust to valid range."""
    return max(TRUST_MIN, min(TRUST_MAX, value))


# ── Need cascade modifiers ──────────────────────────────────────────────

def get_cascade_modifiers(needs) -> Dict[str, float]:
    """Calculate need cascade multipliers based on current need states.
    
    Low hunger drains energy faster. Low social drains fun faster.
    Returns a dict of multipliers to apply to need decay rates.
    
    Args:
        needs: The duck's Needs object
        
    Returns:
        Dict mapping need name to decay rate multiplier (1.0 = normal)
    """
    modifiers = {
        "hunger": 1.0,
        "energy": 1.0,
        "fun": 1.0,
        "cleanliness": 1.0,
        "social": 1.0,
    }
    
    # Low hunger cascades into energy drain
    if needs.hunger < CASCADE_THRESHOLD:
        modifiers["energy"] = CASCADE_HUNGER_TO_ENERGY
    
    # Low social cascades into fun drain
    if needs.social < CASCADE_THRESHOLD:
        modifiers["fun"] = CASCADE_SOCIAL_TO_FUN
    
    return modifiers


# ── Consequence checking ────────────────────────────────────────────────

def check_consequences(duck, delta_minutes: float, stage_modifiers: Optional[Dict[str, float]] = None) -> ConsequenceState:
    """Check and update consequence state based on current needs.
    
    Called every game tick after needs.update(). Tracks how long needs
    have been at zero and escalates consequences accordingly.
    
    Args:
        duck: The Duck object (modified in place)
        delta_minutes: Minutes since last check
        stage_modifiers: Growth stage consequence modifiers from aging.py
            sickness_time_mult: Multiplier for sickness trigger time
            coldness_time_mult: Multiplier for cold shoulder duration
            trust_decay_mult: Multiplier for trust decay rate
    
    Returns:
        ConsequenceState with current status and any messages
    """
    mods = stage_modifiers or {"sickness_time_mult": 1.0, "coldness_time_mult": 1.0, "trust_decay_mult": 1.0}
    warnings = []
    sickness_msg = None
    
    # ── Track time at zero for each need ─────────────────────────────
    needs = duck.needs
    zero_needs = []
    for need_name in ["hunger", "energy", "fun", "cleanliness", "social"]:
        value = getattr(needs, need_name)
        if value <= 0.5:  # Effectively zero
            current = duck.neglect_minutes_at_zero.get(need_name, 0)
            duck.neglect_minutes_at_zero[need_name] = current + delta_minutes
            zero_needs.append(need_name)
        else:
            # Reset timer when need is no longer at zero
            duck.neglect_minutes_at_zero.pop(need_name, None)
    
    # ── If hiding, only check for coax visits ────────────────────────
    if duck.hiding:
        return ConsequenceState(
            stage=3,
            is_sick=duck.is_sick,
            is_hiding=True,
            is_cold_shoulder=_is_cold_shoulder(duck),
            trust=duck.trust,
            trust_level=get_trust_level(duck.trust),
            neglect_warnings=["..."],
            sickness_message="*gone*",
        )
    
    # ── Stage 2 → 3 escalation: sick too long → hiding ───────────────
    if duck.is_sick and duck.sick_since:
        sick_minutes = (time.time() - duck.sick_since) / 60
        hiding_threshold = STAGE3_MINUTES * mods["sickness_time_mult"]
        
        if sick_minutes >= hiding_threshold:
            duck.hiding = True
            duck.hiding_coax_visits = 0
            return ConsequenceState(
                stage=3,
                is_sick=True,
                is_hiding=True,
                is_cold_shoulder=_is_cold_shoulder(duck),
                trust=duck.trust,
                trust_level=get_trust_level(duck.trust),
                neglect_warnings=["*gone*"],
                sickness_message=None,
            )
    
    # ── Check for natural sickness cure ──────────────────────────────
    if duck.is_sick:
        all_above_threshold = all(
            getattr(needs, n) >= SICKNESS_CURE_THRESHOLD
            for n in ["hunger", "energy", "fun", "cleanliness", "social"]
        )
        if all_above_threshold and duck.sick_since:
            healthy_time = (time.time() - duck.sick_since) / 60
            if healthy_time >= SICKNESS_NATURAL_CURE_MINUTES:
                _cure_sickness(duck)
                sickness_msg = "*stretches* ...okay. I feel less terrible. Don't get smug about it."
    
    # ── Stage 1 → 2 escalation: prolonged zero needs → sickness ──────
    if not duck.is_sick and len(zero_needs) >= 2:
        # Need at least 2 needs at zero, and the longest-zero must exceed threshold
        max_zero_minutes = max(
            duck.neglect_minutes_at_zero.get(n, 0) for n in zero_needs
        )
        sickness_threshold = STAGE2_MINUTES * mods["sickness_time_mult"]
        
        if max_zero_minutes >= sickness_threshold:
            duck.is_sick = True
            duck.sick_since = time.time()
            sickness_msg = random.choice(SICKNESS_MESSAGES)
    
    # ── Stage 1: any need at zero for 1+ hour → complain ─────────────
    if zero_needs and not duck.is_sick:
        for need_name in zero_needs:
            minutes_at_zero = duck.neglect_minutes_at_zero.get(need_name, 0)
            complain_threshold = STAGE1_MINUTES * mods["sickness_time_mult"]
            if minutes_at_zero >= complain_threshold:
                warnings.append(_get_neglect_complaint(need_name))
    
    # ── Sickness complaints ──────────────────────────────────────────
    if duck.is_sick and not sickness_msg:
        sickness_msg = random.choice(SICK_ONGOING_MESSAGES)
    
    # ── Determine current stage ──────────────────────────────────────
    if duck.is_sick:
        stage = 2
    elif warnings:
        stage = 1
    else:
        stage = 0
    
    return ConsequenceState(
        stage=stage,
        is_sick=duck.is_sick,
        is_hiding=False,
        is_cold_shoulder=_is_cold_shoulder(duck),
        trust=duck.trust,
        trust_level=get_trust_level(duck.trust),
        neglect_warnings=warnings,
        sickness_message=sickness_msg,
    )


def apply_trust_gain(duck, reason: str = "interaction") -> float:
    """Apply trust gain from a positive interaction.
    
    Args:
        duck: The Duck object
        reason: Why trust increased (interaction, good_day, cure, coax)
    
    Returns:
        Amount of trust gained
    """
    gains = {
        "interaction": TRUST_PER_INTERACTION,
        "good_day": TRUST_GOOD_DAY_BONUS,
        "cure": TRUST_SICK_CURE_BONUS,
        "coax": TRUST_COAX_RETURN_BONUS,
    }
    gain = gains.get(reason, TRUST_PER_INTERACTION)
    old = duck.trust
    duck.trust = clamp_trust(duck.trust + gain)
    return duck.trust - old


def attempt_coax(duck) -> Tuple[bool, str]:
    """Attempt to coax a hiding duck out.
    
    Must be called across separate sessions (game restarts).
    Returns (success, message).
    """
    if not duck.hiding:
        return False, ""
    
    duck.hiding_coax_visits += 1
    remaining = COAX_VISITS_NEEDED - duck.hiding_coax_visits
    
    if remaining <= 0:
        # Duck comes back
        duck.hiding = False
        duck.hiding_coax_visits = 0
        _cure_sickness(duck)
        apply_trust_gain(duck, "coax")
        return True, random.choice(COAX_SUCCESS_MESSAGES)
    else:
        return False, random.choice(COAX_PROGRESS_MESSAGES).format(remaining=remaining)


def apply_medicine(duck) -> Tuple[bool, str]:
    """Apply medicine to cure sickness.
    
    Returns (success, message).
    """
    if not duck.is_sick:
        return False, "I'm not sick. I'm FINE. Stop hovering."
    
    if duck.hiding:
        return False, "..."  # Can't medicine a duck that won't come out
    
    _cure_sickness(duck)
    apply_trust_gain(duck, "cure")
    return True, random.choice(MEDICINE_MESSAGES)


def _cure_sickness(duck):
    """Internal: clear sickness state."""
    duck.is_sick = False
    duck.sick_since = None
    # Reset all neglect timers
    duck.neglect_minutes_at_zero.clear()


def _is_cold_shoulder(duck) -> bool:
    """Check if the duck is currently giving cold shoulder."""
    if duck.cooldown_until is None:
        return False
    return time.time() < duck.cooldown_until


def thaw_cold_shoulder(duck, minutes: float = 30):
    """Reduce cold shoulder timer from a caring visit.
    
    Each good interaction session shaves time off the cooldown.
    """
    if duck.cooldown_until is None:
        return
    
    # Each caring visit removes ~30 minutes of cooldown
    reduction_seconds = minutes * 60
    duck.cooldown_until -= reduction_seconds
    
    if duck.cooldown_until <= time.time():
        duck.cooldown_until = None


# ── Neglect complaint messages (in Cheese's voice) ──────────────────────

def _get_neglect_complaint(need_name: str) -> str:
    """Get a voiced complaint for a specific neglected need."""
    complaints = {
        "hunger": [
            "*stares at empty bowl* This is fine. I'm FINE. Everything is FINE.",
            "*stomach growls* That's not me. That's... the wind. Hungry wind.",
            "Remember food? I remember food. Good times.",
            "*staring at nothing* I used to eat. Those were the days.",
            "My stomach is filing a formal complaint. I support it.",
        ],
        "energy": [
            "*barely standing* I'm not tired. I'm conserving energy. Strategically.",
            "*yawns for the sixth time* This is NORMAL yawning. Not exhaustion.",
            "My legs have opinions about standing. Negative ones.",
            "Sleep is for the weak. I am... currently weak.",
            "*lies down* Just resting my eyes. And legs. And everything.",
        ],
        "fun": [
            "*staring into distance* ...the void stares back. It's bored too.",
            "I've counted every blade of grass. Twice. Send help.",
            "Boredom is a state of mind. My mind is in that state.",
            "Entertainment? Never heard of her.",
            "*pokes ground repeatedly* This is my life now.",
        ],
        "cleanliness": [
            "*sniffs self* ...concerning. Very concerning.",
            "I am becoming one with the dirt. This is not a spiritual choice.",
            "Feathers should not make this sound when you touch them.",
            "*looks at reflection* I am unrecognizable. Possibly an improvement.",
            "There is a smell. It's me. I am the smell.",
        ],
        "social": [
            "*talking to rock* You get me. You UNDERSTAND.",
            "I named that leaf. We're close now. Closer than you and me, apparently.",
            "The silence is deafening. Also lonely. Mostly lonely.",
            "*quiet quack to self* Just checking the acoustics. Not sad.",
            "I'm not lonely. I'm INDEPENDENT. ...please come back.",
        ],
    }
    options = complaints.get(need_name, ["...something is wrong."])
    return random.choice(options)


# ── Sickness messages ───────────────────────────────────────────────────

SICKNESS_MESSAGES = [
    "*lying very still* I'm not sick. I'm... horizontal. By choice.",
    "*shivering* Everything hurts and the pond is too bright.",
    "*weak quack* I've been better. I've also been worse. But not recently.",
    "*curled up* This is a STRATEGIC position. For... warmth. And dignity.",
    "*coughs* My feathers are staging a rebellion. I don't blame them.",
]

SICK_ONGOING_MESSAGES = [
    "*still lying down* Oh. You're here. I'm still... horizontal.",
    "*quiet* Medicine would be nice. Just saying.",
    "*shivers* The pond looks cold. Everything looks cold.",
    "*barely moves* I had plans today. They've been cancelled. By my body.",
    "*weak stare* Don't look at me like that. I'm MANAGING.",
]

MEDICINE_MESSAGES = [
    "*gulp* That tasted like disappointment and pond scum. ...I feel better. Don't tell anyone.",
    "*grimace* Disgusting. Absolutely vile. ...do you have more? In case.",
    "*swallows reluctantly* I'm not THANKING you. I'm just... less horizontal now.",
    "*shudders* That was the worst thing I've ever consumed. And I've eaten pond algae.",
    "*blinks* ...huh. The world is less terrible. The medicine gets partial credit.",
]

COAX_PROGRESS_MESSAGES = [
    "*rustling from hiding spot* ...go away. ({remaining} more visits needed)",
    "*you hear a quiet quack* ...I'm not here. ({remaining} more visits)",
    "*one eye visible* ...you came back. ...whatever. ({remaining} more visits)",
]

COAX_SUCCESS_MESSAGES = [
    "*peeks out* ...oh. you're still here. *slowly emerges* ...fine.",
    "*cautiously waddles out* I wasn't hiding. I was... exploring. Vertically.",
    "*appears* ...don't make a big deal out of this. I just got bored in there.",
    "*emerges looking disheveled* I'm back. Not because you asked. Because I CHOSE to.",
]


# ── Cold shoulder dialogue ──────────────────────────────────────────────

COLD_SHOULDER_GREETINGS = [
    "Oh. You're back. *turns away slightly* ...whatever.",
    "*doesn't look up* ...I heard you come in. I'm choosing not to care.",
    "*facing the wall* ...the wall and I are having a conversation. It's riveting.",
    "...oh. it's you. I was just... not thinking about you. at all.",
    "*slow blink* I remember you. Vaguely. Like a bad dream.",
    "*sitting very still* Don't mind me. I'm practicing being a rock. Rocks don't get abandoned.",
]

COLD_SHOULDER_IDLE = [
    "*stares at nothing* ...the silence was better.",
    "*turns away when you look* I'm not ignoring you. I'm... conserving eye contact.",
    "*quiet* ...I counted the hours. not because I cared. for... science.",
    "*sitting with back to you* This is my aesthetic now. Wall-facing. Very trendy.",
    "*picks at feathers* ...these grew back weird while you were away. probably fine.",
    "...",
    "*quiet quack to self* ...not talking to you. talking to the pond. the pond STAYED.",
]

COLD_SHOULDER_INTERACTION = [
    "*accepts grudgingly* ...I suppose that's adequate.",
    "*takes it without looking at you* ...hmph.",
    "...fine. but don't think this fixes everything.",
    "*minimal acknowledgment* ...registered. barely.",
    "*sighs* ...you're trying. I see that. I'm choosing to be unimpressed.",
]


def get_cold_shoulder_greeting(duck) -> Optional[str]:
    """Get a cold shoulder greeting if applicable."""
    if not _is_cold_shoulder(duck):
        return None
    return random.choice(COLD_SHOULDER_GREETINGS)


def get_cold_shoulder_idle(duck) -> Optional[str]:
    """Get a cold shoulder idle thought if applicable."""
    if not _is_cold_shoulder(duck):
        return None
    return random.choice(COLD_SHOULDER_IDLE)


def get_cold_shoulder_interaction(duck) -> Optional[str]:
    """Get a cold shoulder response to an interaction."""
    if not _is_cold_shoulder(duck):
        return None
    return random.choice(COLD_SHOULDER_INTERACTION)


def is_cold_shoulder_active(duck) -> bool:
    """Public check for cold shoulder state."""
    return _is_cold_shoulder(duck)


# ── Personality drift from neglect / recovery from care ─────────────────
# Traits shift when the duck is neglected (toward withdrawn) or cared for
# (toward social). Always recoverable — drift never exceeds ±40 from baseline.

# Neglect drift: per hour of neglect, multiplied by consequence stage
_NEGLECT_DRIFT = {
    # Base personality traits (name: delta per hour, negative = toward low end)
    "base": {
        "social_shy": -0.5,     # → Shy
        "brave_timid": -0.3,    # → Timid
        "active_lazy": -0.3,    # → Lazy
    },
    # Extended personality traits
    "extended": {
        "independence": 0.5,    # → More independent (self-reliant)
        "playfulness": -0.5,    # → Less playful
        "optimism": -0.4,       # → Less optimistic
        "empathy": -0.3,        # → Less empathetic (walls go up)
        "stubbornness": 0.3,    # → More stubborn (resistant)
    },
}

# Care recovery: per hour of good care (all needs > 40, trust > 20)
# Slower than neglect drift (~60% rate) — damage is easier than healing
_CARE_DRIFT = {
    "base": {
        "social_shy": 0.3,      # → Social again
        "brave_timid": 0.2,     # → Brave again
        "active_lazy": 0.2,     # → Active again
    },
    "extended": {
        "independence": -0.3,   # → Allows reliance
        "playfulness": 0.3,     # → Fun returns
        "optimism": 0.2,        # → Hope rebuilding
        "empathy": 0.2,         # → Walls come down
        "stubbornness": -0.2,   # → Softening
    },
}

# Stage multipliers for neglect drift intensity
_STAGE_DRIFT_MULT = {0: 0.0, 1: 0.5, 2: 1.0, 3: 1.5}

# Max drift from baseline (personality core identity preserved)
_MAX_DRIFT_FROM_BASELINE = 40

# Threshold-crossing dialogue (fires once per crossing)
_DRIFT_THRESHOLD_LINES = {
    ("social_shy", -50): "I don't need anyone. I've decided. Unilaterally.",
    ("playfulness", -40): "Play? What's the point. Games end. Everything ends.",
    ("optimism", -40): "I used to think things would get better. Adorable, past-me.",
    ("empathy", -30): "Your feelings are your problem. I have enough of my own.",
    ("stubbornness", 50): "I've made up my mind about everything. Forever. Don't test me.",
    ("social_shy", 0): "...I missed... the noise. Not you. The noise.",
    ("playfulness", 0): "...maybe one game wouldn't hurt. A short one.",
    ("optimism", 0): "...things might be okay. Not great. Okay. I'll allow okay.",
}


def apply_personality_drift(duck, ext_personality, delta_minutes: float,
                           consequence_stage: int) -> Optional[str]:
    """
    Apply personality drift based on neglect or care.
    
    Args:
        duck: The Duck instance (for base personality + needs + trust)
        ext_personality: ExtendedPersonalitySystem instance
        delta_minutes: Time elapsed since last tick
        consequence_stage: Current consequence stage (0-3)
        
    Returns:
        A deadpan observation if a trait crosses a notable threshold, else None
    """
    # Don't drift while hiding — the duck is already gone
    if duck.hiding:
        return None
    
    delta_hours = delta_minutes / 60.0
    if delta_hours <= 0:
        return None
    
    # Determine if we're drifting from neglect or recovering from care
    is_neglected = consequence_stage >= 1
    all_needs_ok = all(
        getattr(duck.needs, need, 50) > 40
        for need in ("hunger", "energy", "fun", "cleanliness", "social")
    )
    is_cared_for = not is_neglected and all_needs_ok and duck.trust > 20
    
    if not is_neglected and not is_cared_for:
        return None  # In between — no drift
    
    # Get or initialize baseline
    if not hasattr(duck, '_personality_baseline') or not duck._personality_baseline:
        duck._personality_baseline = dict(duck.personality)
    if not hasattr(duck, '_ext_personality_baseline') or not duck._ext_personality_baseline:
        duck._ext_personality_baseline = dict(ext_personality.extended_traits)
    
    observation = None
    
    if is_neglected:
        stage_mult = _STAGE_DRIFT_MULT.get(consequence_stage, 1.0)
        
        # Drift base personality traits
        for trait, rate_per_hour in _NEGLECT_DRIFT["base"].items():
            delta = rate_per_hour * delta_hours * stage_mult
            observation = _apply_base_drift(duck, trait, delta) or observation
        
        # Drift extended traits
        for trait, rate_per_hour in _NEGLECT_DRIFT["extended"].items():
            delta = rate_per_hour * delta_hours * stage_mult
            old_val = ext_personality.get_trait_value(trait)
            _apply_ext_drift(ext_personality, duck, trait, delta)
            new_val = ext_personality.get_trait_value(trait)
            obs = _check_threshold_crossing(trait, old_val, new_val)
            observation = obs or observation
    
    elif is_cared_for:
        # Recovery drift (toward baseline, slower)
        for trait, rate_per_hour in _CARE_DRIFT["base"].items():
            baseline = duck._personality_baseline.get(trait, 0)
            current = duck.personality.get(trait, 0)
            # Only drift toward baseline, don't overshoot
            if rate_per_hour > 0 and current >= baseline:
                continue
            if rate_per_hour < 0 and current <= baseline:
                continue
            delta = rate_per_hour * delta_hours
            observation = _apply_base_drift(duck, trait, delta) or observation
        
        for trait, rate_per_hour in _CARE_DRIFT["extended"].items():
            baseline = duck._ext_personality_baseline.get(trait, 0)
            current = ext_personality.get_trait_value(trait)
            if rate_per_hour > 0 and current >= baseline:
                continue
            if rate_per_hour < 0 and current <= baseline:
                continue
            old_val = current
            delta = rate_per_hour * delta_hours
            _apply_ext_drift(ext_personality, duck, trait, delta)
            new_val = ext_personality.get_trait_value(trait)
            obs = _check_threshold_crossing(trait, old_val, new_val)
            observation = obs or observation
    
    return observation


def _apply_base_drift(duck, trait: str, delta: float) -> Optional[str]:
    """Apply drift to a base personality trait, respecting baseline limits."""
    current = duck.personality.get(trait, 0)
    baseline = duck._personality_baseline.get(trait, 0)
    
    new_val = current + delta
    # Clamp to ±MAX_DRIFT from baseline and global -100/+100
    min_val = max(-100, baseline - _MAX_DRIFT_FROM_BASELINE)
    max_val = min(100, baseline + _MAX_DRIFT_FROM_BASELINE)
    new_val = max(min_val, min(max_val, new_val))
    
    old_int = int(current)
    new_int = int(new_val)
    
    if old_int != new_int:
        duck.personality[trait] = new_int
        obs = _check_threshold_crossing(trait, old_int, new_int)
        return obs
    
    # Store fractional drift for sub-integer precision
    duck.personality[trait] = new_val
    return None


def _apply_ext_drift(ext_personality, duck, trait: str, delta: float):
    """Apply drift to an extended personality trait, respecting baseline limits."""
    current = ext_personality.get_trait_value(trait)
    baseline = getattr(duck, '_ext_personality_baseline', {}).get(trait, 0)
    
    new_val = current + delta
    min_val = max(-100, baseline - _MAX_DRIFT_FROM_BASELINE)
    max_val = min(100, baseline + _MAX_DRIFT_FROM_BASELINE)
    new_val = max(min_val, min(max_val, new_val))
    
    reason = "neglect_drift" if delta < 0 or (trait in ("independence", "stubbornness") and delta > 0) else "care_recovery"
    ext_personality.adjust_trait(trait, int(new_val) - current, reason)


def _check_threshold_crossing(trait: str, old_val, new_val) -> Optional[str]:
    """Check if a trait crossed a notable threshold and return dialogue."""
    for (t, threshold), line in _DRIFT_THRESHOLD_LINES.items():
        if t != trait:
            continue
        # Crossing from one side to the other
        if old_val < threshold <= new_val or old_val > threshold >= new_val:
            return line
    return None

