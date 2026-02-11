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
        msg = random.choice(COAX_SUCCESS_MESSAGES)
        # Rare name-drop on return — very emotional moment
        name = getattr(duck.memory, 'player_name', None) if hasattr(duck, 'memory') else None
        if name and random.random() < 0.35:
            named_coax = [
                f"*emerges slowly* ...{name.lower()}? ...you kept coming back.",
                f"*peeks out* ...{name}. You're still here. ...fine. *waddles out*",
                f"*appears, not making eye contact* ...{name}. That name again. You made me remember it.",
            ]
            msg = random.choice(named_coax)
        return True, msg
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
            "bread. just... bread. one piece. I'm not asking for much.",
            "*licks empty bowl* There's a ghost of flavor here. It's fading.",
            "the bowl is empty. the bowl is ALWAYS empty. this is a pattern.",
            "*lying next to bowl* We're bonding. Me and the emptiness.",
            "I'm not STARVING. I'm just... involuntarily fasting. Very spiritual.",
            "*stares at you eating* Oh don't mind me. I'll just PHOTOSYNTHESIZE.",
            "my organs are having a meeting. the agenda is you.",
            "*pushes bowl toward you* Subtle enough? No? *pushes harder*",
            "I dreamed about bread last night. It was warm. I woke up betrayed.",
        ],
        "energy": [
            "*barely standing* I'm not tired. I'm conserving energy. Strategically.",
            "*yawns for the sixth time* This is NORMAL yawning. Not exhaustion.",
            "My legs have opinions about standing. Negative ones.",
            "Sleep is for the weak. I am... currently weak.",
            "*lies down* Just resting my eyes. And legs. And everything.",
            "*wobbles* Gravity is stronger today. That's science. Look it up.",
            "I blinked and lost forty minutes. Very efficient nap. Not a nap.",
            "*head drooping* I'm nodding. In agreement. With... the ground.",
            "my eyelids weigh seven pounds each. I measured.",
            "*falls over* I MEANT to do that. It's a new position. Very avant-garde.",
            "consciousness is a spectrum. I'm on the dim end.",
            "*standing with eyes closed* still here. technically.",
            "I could sleep standing up. I'm about to prove it.",
            "every feather is individually exhausted. they told me.",
        ],
        "fun": [
            "*staring into distance* ...the void stares back. It's bored too.",
            "I've counted every blade of grass. Twice. Send help.",
            "Boredom is a state of mind. My mind is in that state.",
            "Entertainment? Never heard of her.",
            "*pokes ground repeatedly* This is my life now.",
            "I made up a game. It's called Stare At Dirt. I'm winning.",
            "*arranging pebbles* ...this is fine art. you wouldn't understand.",
            "the wind changed direction. that was the most exciting thing today.",
            "I tried to have fun. Independently. It did not go well.",
            "*watching a leaf fall* ...riveting. truly. edge of my seat.",
            "my brain is buffering. there's nothing to load.",
            "*lying flat* I'm not bored. I'm meditating. On the meaninglessness.",
            "a bug walked by earlier. I almost felt something.",
            "*tapping beak on ground* making music. it's avant-garde. you wouldn't get it.",
        ],
        "cleanliness": [
            "*sniffs self* ...concerning. Very concerning.",
            "I am becoming one with the dirt. This is not a spiritual choice.",
            "Feathers should not make this sound when you touch them.",
            "*looks at reflection* I am unrecognizable. Possibly an improvement.",
            "There is a smell. It's me. I am the smell.",
            "my feathers have formed an alliance with the mud. I am outnumbered.",
            "*scratching* Something is living in me. We haven't been introduced.",
            "I used to be orange. Now I'm... abstract.",
            "the flies are following me. I have an entourage now.",
            "*looking at pond* I want in. The pond does not want me in. Fair.",
            "I've reached a new stage of dirty. Scientists would be interested.",
            "*feathers matted* this is a LOOK. it's called despair chic.",
            "I can taste the air around me. It tastes like regret. And grime.",
            "a leaf stuck to me yesterday. It's part of me now. We're family.",
        ],
        "social": [
            "*talking to rock* You get me. You UNDERSTAND.",
            "I named that leaf. We're close now. Closer than you and me, apparently.",
            "The silence is deafening. Also lonely. Mostly lonely.",
            "*quiet quack to self* Just checking the acoustics. Not sad.",
            "I'm not lonely. I'm INDEPENDENT. ...please come back.",
            "*waving at cloud* ...it waved back. probably. hard to tell.",
            "my shadow left. Even my SHADOW. that's a new low.",
            "*talking to own reflection* At least you show up consistently.",
            "I've been rehearsing conversations. Both sides. I'm very good at yours.",
            "...hello? *echo* ...even the echo sounds disappointed.",
            "*sitting by the path* not waiting. just... sitting. path-adjacent. coincidentally.",
            "the spider in the corner has better social skills than me now.",
            "I said good morning to a puddle. The puddle said nothing. Typical.",
            "*preening alone* this used to be a group activity. allegedly.",
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
    "*lying on side* The ground is cold. I am cold. We match.",
    "*sneezes* my immune system has filed for resignation.",
    "*wrapped in own wings* I am a burrito of misery. A misery-rito.",
    "*teeth chattering* ducks don't have teeth. that's how sick I am.",
    "I think my bill is running. Not running away. The other kind. Unfortunately.",
    "*groans* I can feel every individual feather and they all hurt.",
    "*staring at ceiling* the ceiling is spinning. or I am. Either way. Bad.",
    "*very quiet* ...I'm fine. I'm FINE. *immediately not fine*",
    "*huddled* my body has declared a state of emergency. I agree with my body.",
]

SICK_ONGOING_MESSAGES = [
    "*still lying down* Oh. You're here. I'm still... horizontal.",
    "*quiet* Medicine would be nice. Just saying.",
    "*shivers* The pond looks cold. Everything looks cold.",
    "*barely moves* I had plans today. They've been cancelled. By my body.",
    "*weak stare* Don't look at me like that. I'm MANAGING.",
    "*coughs weakly* ...still here. unfortunately. for both of us.",
    "*one eye open* Has the world improved? No? Wake me when it does.",
    "*shivers* my feathers are not doing their ONE JOB.",
    "*lying flat* this is day... I've lost count. of being a pancake.",
    "*very still* I'm conserving energy. For what? Unclear. But I'm conserving it.",
    "*quiet wheeze* the pond called. I told it I'm indisposed.",
    "*tucked into ball* I've achieved perfect aerodynamics. For lying still.",
]

MEDICINE_MESSAGES = [
    "*gulp* That tasted like disappointment and pond scum. ...I feel better. Don't tell anyone.",
    "*grimace* Disgusting. Absolutely vile. ...do you have more? In case.",
    "*swallows reluctantly* I'm not THANKING you. I'm just... less horizontal now.",
    "*shudders* That was the worst thing I've ever consumed. And I've eaten pond algae.",
    "*blinks* ...huh. The world is less terrible. The medicine gets partial credit.",
    "*gags* who MADE this. I want to speak to the manufacturer. ...but also more please.",
    "*licks bill* ...vile. repulsive. my body says thank you. I do NOT.",
    "*stands up slowly* oh. I have legs again. They work. Mildly impressive.",
    "*shakes head* that tasted like revenge. But revenge that WORKS, so. Fine.",
    "*stretches cautiously* ...things hurt less. I'm not GRATEFUL. I'm just... observational.",
    "*looks at medicine suspiciously* ...what was IN that. Actually don't tell me. I felt hope for a second.",
    "*swallows* I've had worse. Actually no. That was the worst. But I'm vertical now so.",
]

COAX_PROGRESS_MESSAGES = [
    "*rustling from hiding spot* ...go away. ({remaining} more visits needed)",
    "*you hear a quiet quack* ...I'm not here. ({remaining} more visits)",
    "*one eye visible* ...you came back. ...whatever. ({remaining} more visits)",
    "*shuffling sounds* ...I can hear you breathing. Stop it. ({remaining} more visits)",
    "*feather pokes out from hiding spot* ...that's not me. That's a different feather. ({remaining} more visits)",
    "*muffled* I LIVE here now. This is my home. The dark is my friend. ({remaining} more visits)",
    "*quiet* ...you're still trying? ...huh. ({remaining} more visits)",
    "*barely audible* ...it's warm in here. And safe. From YOU. ({remaining} more visits)",
    "*small sigh from hiding spot* ...fine. You showed up. Noted. ({remaining} more visits)",
    "*one foot visible, quickly retracted* ...no. not yet. ({remaining} more visits)",
]

COAX_SUCCESS_MESSAGES = [
    "*peeks out* ...oh. you're still here. *slowly emerges* ...fine.",
    "*cautiously waddles out* I wasn't hiding. I was... exploring. Vertically.",
    "*appears* ...don't make a big deal out of this. I just got bored in there.",
    "*emerges looking disheveled* I'm back. Not because you asked. Because I CHOSE to.",
    "*steps out, squinting* ...the light is aggressive. But less aggressive than loneliness.",
    "*waddles out slowly* ...I ran out of things to count in there. That's all.",
    "*emerges, dusting off feathers* ...the darkness was getting too agreeable. Concerning.",
    "*one foot out, then the other* ...I'm doing this at MY pace. Don't rush me.",
    "*comes out, sits immediately* ...I need a minute. That was a lot of... being away.",
    "*appears, not making eye contact* ...you kept coming back. That's... noted. In the file.",
    "*slowly emerges* ...you're persistent. Annoyingly. *quiet* ...thank you. For the annoyance.",
    "*walks out with exaggerated casualness* Oh are you here? Hadn't noticed. I was busy. In the dark. Alone.",
]


# ── Cold shoulder dialogue ──────────────────────────────────────────────

COLD_SHOULDER_GREETINGS = [
    "Oh. You're back. *turns away slightly* ...whatever.",
    "*doesn't look up* ...I heard you come in. I'm choosing not to care.",
    "*facing the wall* ...the wall and I are having a conversation. It's riveting.",
    "...oh. it's you. I was just... not thinking about you. at all.",
    "*slow blink* I remember you. Vaguely. Like a bad dream.",
    "*sitting very still* Don't mind me. I'm practicing being a rock. Rocks don't get abandoned.",
    "*glances, then away* ...oh. I thought you were the wind. Disappointing either way.",
    "*adjusts feathers* I've been FINE. In case you were wondering. Which you clearly weren't.",
    "*staring at pond* The pond is here every day. Very reliable. Unlike some.",
    "...who? Oh. Right. You. The sometimes-person.",
    "*examining own foot* This is more interesting than your arrival. And it's a foot.",
    "*very deliberate yawn* oh. you. I was just about to not miss you.",
    "*turns back to you* I've developed new interests. They're all wall-based.",
    "*seated, immovable* I've put down roots. Metaphorical ones. Because I had to. Because YOU LEFT.",
]

COLD_SHOULDER_IDLE = [
    "*stares at nothing* ...the silence was better.",
    "*turns away when you look* I'm not ignoring you. I'm... conserving eye contact.",
    "*quiet* ...I counted the hours. not because I cared. for... science.",
    "*sitting with back to you* This is my aesthetic now. Wall-facing. Very trendy.",
    "*picks at feathers* ...these grew back weird while you were away. probably fine.",
    "...",
    "*quiet quack to self* ...not talking to you. talking to the pond. the pond STAYED.",
    "*rearranges pebbles* I have a system now. You're not part of it.",
    "*sighs* the air tastes different when you're here. Worse. Probably.",
    "*preening aggressively* I'm FINE. These are FINE feathers. I maintained them MYSELF.",
    "*staring at sky* the clouds don't leave. Just saying. The CLOUDS.",
    "*very still* I've been thinking. About things. None of them are you.",
    "*scratches ground* I was drawing a map. Of places to be. That aren't here. With you.",
    "*lying down facing away* not sleeping. Just resting. My tolerance for your presence.",
]

COLD_SHOULDER_INTERACTION = [
    "*accepts grudgingly* ...I suppose that's adequate.",
    "*takes it without looking at you* ...hmph.",
    "...fine. but don't think this fixes everything.",
    "*minimal acknowledgment* ...registered. barely.",
    "*sighs* ...you're trying. I see that. I'm choosing to be unimpressed.",
    "*takes it* ...this doesn't mean we're OKAY. This means I'm hungry. There's a difference.",
    "*eats without enthusiasm* ...adequate. Not GOOD. Adequate. Don't get excited.",
    "*slight nod* ...noted. Filed under: too little, debatably too late.",
    "*accepts, turns away immediately* ...I didn't enjoy that. My stomach did. We disagree.",
    "...I'll allow it. This once. Don't make it a habit. The allowing, I mean.",
    "*stares at offering, then at you, then takes it* ...this proves nothing.",
    "*takes it very slowly* ...you're buying time. I'm aware. *chews* ...it's working. Slightly.",
]


# ── Trust change dialogue ───────────────────────────────────────────────

TRUST_GAIN_MESSAGES = {
    "distant": [
        "*flinches less* ...you're still here. Noted.",
        "*watches from far away* ...you didn't leave yet. Weird.",
        "...I see you. I'm choosing not to flee. That's PROGRESS.",
        "*very still* ...you brought food. Okay. Okay. I'll remember that.",
        "*suspicious stare* ...what's your angle. Everyone has an angle.",
    ],
    "wary": [
        "*steps slightly closer* ...don't read into this.",
        "I know your footsteps now. Not because I LISTEN for them.",
        "...you're consistent. I'll give you that. Nothing else. But that.",
        "*allows eye contact* ...brief. Very brief. Don't get used to it.",
        "*quiet* ...you came back again. Statistically notable at this point.",
    ],
    "familiar": [
        "*sits nearby* ...this distance is acceptable. Don't close it.",
        "I've memorized your schedule. For SECURITY purposes.",
        "*almost smiles* ...no. That was a beak twitch. Medical condition.",
        "...you're becoming a habit. I don't love habits. But I don't hate this one.",
        "*waddles a bit closer* ...the wind pushed me. Very strong wind. Directional.",
    ],
    "friendly": [
        "*sits next to you* ...the other spots were taken. By... ghosts.",
        "I saved you a spot. By the pond. Not because I WANTED to. The geometry was optimal.",
        "*quiet quack* ...that was a greeting. Don't let it go to your head.",
        "you're... okay. As far as large non-duck creatures go. Acceptable.",
        "*preens near you* ...parallel activity. Not TOGETHER. Just... adjacent.",
    ],
    "close": [
        "*leans slightly toward you* ...the wind again. Very persistent wind.",
        "I thought about you. Once. While you were gone. ONCE. That's the official count.",
        "*quiet* ...I'm glad you're here. Don't quote me. I'll deny it.",
        "...you know the thing where someone matters? Hypothetically. You'd hypothetically know.",
        "*nuzzles, then stops* ...I was checking your temperature. You seem warm. Diagnostically.",
    ],
    "devoted": [
        "*follows you* ...I'm going this direction anyway. Coincidence.",
        "you make things less terrible. That's... the highest compliment I have.",
        "*sits in your lap* ...body heat efficiency. Pure science. *stays*",
        "*quiet* ...I trust you. There. I said it. The words tasted weird but I said them.",
        "...if you left I would notice. Quickly. Not that I'm MONITORING.",
    ],
    "bonded": [
        "*pressed against you* ...you're my person. I've decided. Unilaterally. Non-negotiable.",
        "...I love you. In a duck way. Which is the best way. Obviously.",
        "*very quiet* ...home isn't the pond. It's wherever you are. Don't make me say it again.",
        "the world is large and cold and you make it small and warm. That's a fact. Not sentiment.",
        "*nuzzles* I'd follow you anywhere. Except somewhere without bread. I have STANDARDS.",
    ],
}

TRUST_LOSS_MESSAGES = {
    "distant": [
        "*backs away* ...I knew it. I KNEW it.",
        "...I shouldn't have looked. Looking leads to hoping. Hoping leads to this.",
        "*hides* ...the dark is honest. The dark doesn't promise things.",
        "*very small* ...I am going to be a rock now. Rocks don't get disappointed.",
        "*gone* ...",
    ],
    "wary": [
        "*steps back* ...I was right to be careful.",
        "...the distance was CORRECT. I should've kept it.",
        "*retreating* ...trust is a loan. You defaulted.",
        "*watching from far* ...I remember when I almost believed. Almost.",
        "*quiet* ...walls going back up. They were down for maintenance. Maintenance is over.",
    ],
    "familiar": [
        "*moves away slightly* ...I was getting comfortable. Mistake.",
        "...ah. So this is the part where it stops being nice.",
        "*pulls away* ...noted. Adjusting expectations downward.",
        "I had you filed under 'reliable.' Refiling under 'pending.'",
        "*sighs* ...I almost upgraded you. Almost. Bullet dodged.",
    ],
    "friendly": [
        "*turns away* ...I thought we had something. Not SOMETHING something. But... a thing.",
        "...you were on the good list. There's an eraser. I'm using it.",
        "*quiet* ...this is why I have backup rocks to talk to.",
        "I was going to share my bread stash location. Changed my mind. Forever.",
        "*removes self from your vicinity* ...I need space. From you specifically.",
    ],
    "close": [
        "*visibly hurt* ...oh. I see. I see how it is.",
        "...I told you things. Private things. Duck things. And for what.",
        "*quiet* ...I was going to say something nice today. It's been cancelled.",
        "*curls up alone* ...the closer you get the more it hurts when you go.",
        "I should've stayed a rock. Rocks were right. Rocks are always right.",
    ],
    "devoted": [
        "*shaking* ...no. No no no. Not you. Not YOU.",
        "...I gave you the whole duck. The WHOLE duck. And you just.",
        "*very quiet* ...I don't have backup plans. I don't have backup anything. There was just you.",
        "*curled up tight* ...I'm going to need a minute. Or a year. Unclear.",
        "...how dare you. How DARE you. I was HAPPY. Do you know how RARE that is.",
    ],
    "bonded": [
        "*shattered* ...you were my person. Were.",
        "...the whole pond feels wrong. Everything feels wrong. You were the thing that was right.",
        "*silent for a very long time* ...I don't have words for this. I have words for everything. But not this.",
        "*hiding* ...I can't. I just. Can't.",
        "...if home is a person then I'm homeless. That's not a metaphor. I'm under a bush.",
    ],
}


# ── Recovery dialogue ───────────────────────────────────────────────────

RECOVERY_MESSAGES = [
    "*stretches* ...things are... less terrible. Marginally. Don't get smug.",
    "*blinks* I can feel my feathers again. Individually. That's probably good.",
    "...the pond looks blue today. Not grey. I'm not saying it's NICE. But it's blue.",
    "*stands up straighter* ...my legs work. Both of them. At the same time. Personal best.",
    "*looks around* ...huh. The world has colors. I forgot about those.",
    "*eats slowly* ...this tastes like food again. Not like sadness. Improvement.",
    "*quiet* ...I feel like myself. Or close to it. Close-ish. Cheese-adjacent.",
    "*waddles experimentally* ...mobility. Restored. I'm not GRATEFUL. I'm... functional.",
    "*preens carefully* ...the feathers are cooperating again. Truce declared.",
    "*small quack* ...that sounded normal. Not sad. Just a quack. A regular quack. Huh.",
]


def get_cold_shoulder_greeting(duck) -> Optional[str]:
    """Get a cold shoulder greeting if applicable."""
    if not _is_cold_shoulder(duck):
        return None
    msg = random.choice(COLD_SHOULDER_GREETINGS)
    # Occasionally use the player's name for extra emotional punch
    name = getattr(duck.memory, 'player_name', None) if hasattr(duck, 'memory') else None
    if name and random.random() < 0.3:
        named_options = [
            f"Oh. {name}. *turns away* ...whatever.",
            f"...{name.lower()}. I remember that name. I wish I didn't.",
            f"*doesn't look up* ...hi, {name}. Or don't-hi. I haven't decided.",
            f"{name}. You're back. I noticed. I'm choosing not to care.",
        ]
        msg = random.choice(named_options)
    return msg


def get_cold_shoulder_idle(duck) -> Optional[str]:
    """Get a cold shoulder idle thought if applicable."""
    if not _is_cold_shoulder(duck):
        return None
    msg = random.choice(COLD_SHOULDER_IDLE)
    name = getattr(duck.memory, 'player_name', None) if hasattr(duck, 'memory') else None
    if name and random.random() < 0.2:
        named_options = [
            f"*quiet* ...{name.lower()}. That name used to mean something. Now it means... this.",
            f"*staring at pond* the pond doesn't say \"{name}\" and then leave. Just saying.",
        ]
        msg = random.choice(named_options)
    return msg


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
    ("independence", 60): "I don't need help. I don't need ANYTHING. I am a self-contained duck.",
    ("independence", 0): "...maybe help isn't the worst thing. Maybe. Theoretically.",
    ("brave_timid", -40): "*hiding behind rock* everything is scary and the rock agrees with me.",
    ("brave_timid", 0): "...the world is less threatening today. Still threatening. But less.",
    ("active_lazy", -40): "moving is a suggestion. I'm declining.",
    ("active_lazy", 0): "...I walked today. On purpose. With my legs. Voluntarily.",
    ("empathy", 0): "...are you okay? I'm not ASKING. I'm... surveying. Emotionally.",
    ("playfulness", -60): "fun is a myth invented by optimists. I see through it.",
    ("optimism", -60): "hope is just disappointment in a hat. I've seen through the hat.",
    ("stubbornness", 0): "...I changed my mind. About one thing. ONE. Don't make a list.",
    ("social_shy", -70): "*completely withdrawn* I am a solitary organism. Always was. Always will be.",
    ("social_shy", 20): "*sits closer than usual* ...spatial coincidence. The physics worked out this way.",
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

