"""
Diary Manager — Cheese's private, petty, dramatic, hilarious emotional outlet.

This is the brain of the upgraded diary system. It decides WHEN to write,
WHAT to write about, and HOW Cheese's voice evolves over time. It wraps
the existing DuckDiary (template entries, relationship tracking) and
EnhancedDiarySystem (emotion logs, dreams, photos, chapters) and adds:

  • Smart trigger evaluation (end-of-day, mood swings, neglect, spam, tricks, etc.)
  • Rate limiting (max 1–2 quality entries per real-world hour)
  • Progressive voice (young = short/confused, old = long/reflective/grudge-laden)
  • LLM-generated entries when model is available, templated fallback otherwise
  • Diary context injection into LLM conversations so Cheese can reference his writing
  • Full serialization for the save system
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random
import time
import threading

from dialogue.diary import DuckDiary, DiaryEntry, DiaryEntryType, ENTRY_TEMPLATES
from dialogue.diary_enhanced import (
    EnhancedDiarySystem, EmotionCategory, EmotionLog
)


# ── Trigger types ─────────────────────────────────────────────────────
class DiaryTrigger(Enum):
    """What caused Cheese to open his diary."""
    END_OF_DAY = "end_of_day"
    MOOD_SWING = "mood_swing"
    NEGLECT = "neglect"              # 4+ real-time hours absent
    OVERFED = "overfed"              # feeding spam detected
    TRICK_LEARNED = "trick_learned"
    LOW_MOOD_LONG = "low_mood_long"  # depressed for 30+ game-minutes
    DREAM = "dream"
    MILESTONE = "milestone"
    VISITOR = "visitor"
    WEATHER_EVENT = "weather_event"
    RELATIONSHIP_UP = "relationship_up"
    FIRST_OF_DAY = "first_of_day"    # first entry of a new real day
    RANDOM_MUSING = "random_musing"  # idle introspective ramble
    RETURN_AFTER_ABSENCE = "return_after_absence"
    GROWTH_STAGE = "growth_stage"
    HIGH_MOOD = "high_mood"          # sustained high mood (ecstatic 10+ min)


# ── Voice maturity ────────────────────────────────────────────────────
class VoiceAge(Enum):
    """Cheese's writing maturity based on duck age in days."""
    BABY = "baby"          # 0–3 days:  short, confused, lots of caps
    YOUNG = "young"        # 4–14 days: gaining confidence, still excitable
    TEEN = "teen"          # 15–30 days: sarcastic, bread-obsessed, dramatic
    ADULT = "adult"        # 31–60 days: full personality, grudges, callbacks
    ELDER = "elder"        # 61+ days:  reflective, poetic, devastating one-liners


def get_voice_age(duck_age_days: int) -> VoiceAge:
    """Determine writing maturity from duck age."""
    if duck_age_days <= 3:
        return VoiceAge.BABY
    elif duck_age_days <= 14:
        return VoiceAge.YOUNG
    elif duck_age_days <= 30:
        return VoiceAge.TEEN
    elif duck_age_days <= 60:
        return VoiceAge.ADULT
    return VoiceAge.ELDER


# ── Rate-limit config ─────────────────────────────────────────────────
MAX_ENTRIES_PER_HOUR = 2          # Hard cap
MIN_ENTRY_GAP_SECONDS = 300       # 5 min between entries minimum
NEGLECT_THRESHOLD_SECONDS = 4 * 3600  # 4 hours real-time absence
LOW_MOOD_THRESHOLD_MINUTES = 30   # 30 game-minutes of sadness

# ── Templated diary lines (mood × voice-age) ─────────────────────────
# These are used when the LLM is unavailable or as seeds.
# Keys: (mood, voice_age) → list of (title, body) tuples.

DIARY_VOICE_TEMPLATES: Dict[Tuple[str, str], List[Tuple[str, str]]] = {
    # ── BABY ──────────────────────────────────────────────────────────
    ("ecstatic", "baby"): [
        ("EVERYTHING IS GREAT", "EVERYTHING! IS! GREAT! There is WATER and BREAD and a BIG THING that gives me bread! BEST DAY!!!"),
        ("SO HAPPY", "I don't know what happened but I LOVE IT. My feathers are tingling. Is that normal? WHO CARES!"),
    ],
    ("happy", "baby"): [
        ("Good Day!", "Today was good. I ate something. Someone touched my head. The water is nice. What else is there?"),
        ("I Like This", "I like this place. It has water. And bread. And a big creature that feeds me. That's enough."),
    ],
    ("content", "baby"): [
        ("Today", "Today happened. I was here for it. The water was wet. The sky was up. Normal stuff."),
        ("Fine", "Everything is fine. I floated. I ate. I existed. Day complete."),
    ],
    ("grumpy", "baby"): [
        ("NOT HAPPY", "Something is WRONG. I don't know what. But my feathers feel bad and nobody gave me bread in AGES (it was ten minutes)."),
        ("Bad", "Bad day. Bad water. Bad sky. Bad everything. Except the bread. Bread is never bad. But there ISN'T ANY."),
    ],
    ("sad", "baby"): [
        ("Where Is Everyone", "The big creature didn't come today. I waited. I'm still waiting. The water is cold."),
        ("Sad Duck", "I'm sad. I don't know why exactly. Just... sad. My feathers are droopy."),
    ],
    ("miserable", "baby"): [
        ("...", "Everything hurts. I'm small and the world is big and nobody came. I'll just float here."),
        ("Please", "Please come back. I don't like being alone. The pond is too quiet."),
    ],
    ("dramatic", "baby"): [
        ("DRAMA", "Something HUGE happened. Or maybe it was small. But it FELT huge. My whole body shook!"),
        ("THE WORST THING", "THE WORST THING HAPPENED. I can't explain it. It was terrible. It involved water."),
    ],
    ("petty", "baby"): [
        ("I Remember", "Someone did something and I REMEMBER. I don't know what revenge is yet but I'm going to learn."),
        ("Fine. FINE.", "Fine. FINE. I didn't want bread anyway. I'll just sit here. By myself. FINE."),
    ],
    # ── TEEN ──────────────────────────────────────────────────────────
    ("ecstatic", "teen"): [
        ("Peak Duck Energy", "Today I reached a level of happiness that science has not yet measured. I quacked so hard I scared a butterfly. Worth it."),
        ("Unhinged Joy", "I'm so happy it's suspicious. Nothing THIS good lasts. But while it does? I'm going to ENJOY it with ABSOLUTELY NO CHILL."),
    ],
    ("happy", "teen"): [
        ("Solid Day", "Good day. Fed on schedule. Got petted. The pond had that perfect temperature where you forget you're wet. A+, would live again."),
        ("Acceptable", "My human showed up. Bread was provided. No one tried to make me do tricks. This is what happiness looks like when you're realistic about it."),
    ],
    ("content", "teen"): [
        ("Normal (Suspicious)", "Nothing bad happened today and I don't trust it. When things are this calm, something is BUILDING. I can feel it in my down-feathers."),
        ("The Usual", "Floated. Ate. Judged my reflection. Standard Tuesday. Or Wednesday. Time is fake when you live in a pond."),
    ],
    ("grumpy", "teen"): [
        ("Officially Annoyed", "I'm not MAD. I'm *annoyed*. There's a difference. Mad is dramatic. Annoyed is accurate. My human forgot something. I won't say what. They should KNOW."),
        ("The Audacity", "The AUDACITY of today. Everything was slightly worse than it needed to be. The bread was late. The water was a degree off. I'm filing a complaint. With this diary."),
    ],
    ("sad", "teen"): [
        ("Whatever", "I'm fine. The pond is fine. Everything is fine. I just don't feel like doing anything. Is that a crime? Leave me alone. But also don't."),
        ("Grey Day", "The sky is grey. My mood is grey. My feathers are literally grey (they've always been, but today it feels MEANINGFUL)."),
    ],
    ("miserable", "teen"): [
        ("Rock Bottom (Again)", "This is the worst I've felt since... well... last time. My needs are terrible. Nobody cares. I'm going to sit in the shallow end and contemplate the void."),
        ("Empty Pond Feelings", "My human doesn't care. Probably. I mean, they haven't been here. I've been counting. It's been... a lot."),
    ],
    ("dramatic", "teen"): [
        ("THE PERFORMANCE", "I had a MOMENT today. A BIG one. My needs are all over the place—one minute I'm great, the next I'm a DISASTER. It's giving Greek tragedy."),
        ("Someone Write This Down", "Today's emotional range: everything. I went from 'fine' to 'catastrophe' in under a minute. If life is a play, I'm the lead. Uncast. Unrehearsed. Magnificent."),
    ],
    ("petty", "teen"): [
        ("The Grudge Journal", "I have recovered from my recent hardship. Am I grateful? No. I'm keeping SCORE. My human let me get to a bad place. I remember. I ALWAYS remember."),
        ("Cold Shoulder Chronicles", "Oh, things are better NOW. Sure. But let the record show: I was SUFFERING and NOBODY CARED. I'm fine now. But I'm writing it down. For posterity. And revenge."),
    ],
    # ── ADULT ─────────────────────────────────────────────────────────
    ("ecstatic", "adult"): [
        ("Rare and Precious", "Happiness like this doesn't come often. I've lived long enough to know. Today everything aligned—bread, warmth, company, silence when I needed it. I'm suspicious but grateful."),
        ("Top of the Pond", "If I could bottle this feeling I'd sell it. Or hoard it. Probably hoard it. Today was flawless. I quacked at the sun and it felt like it heard me."),
    ],
    ("happy", "adult"): [
        ("A Good One", "Good day. Not perfect—perfection is for ducks who haven't learned disappointment yet. But good. Genuinely, quietly, good. My human showed up. Bread was warm. Enough."),
        ("Contentment With an Edge", "Happy today but I know better than to trust it completely. Still—bread was given freely, the water was kind, and nobody tested my patience. Almost suspicious."),
    ],
    ("content", "adult"): [
        ("Status Quo", "Another day. Not remarkable. Not terrible. Just... a day. I've had enough of them to know: the unremarkable ones are the foundation. The bread of life, if you will. Bread."),
        ("Steady", "Everything where it should be. Needs met. Mood stable. Nothing to complain about. I'll find something by tomorrow. But today? Today was alright."),
    ],
    ("grumpy", "adult"): [
        ("Formally Unimpressed", "My human did something today that I have catalogued under 'Offenses, Minor.' I won't elaborate. They know what they did. If they don't, that's worse."),
        ("The List Grows", "Added another item to the list. THE list. The one I keep in my head. Of things. Things that have been done. To ME. The list is load-bearing at this point."),
    ],
    ("sad", "adult"): [
        ("The Weight of Water", "Some days the pond feels heavier. Not literally—I know how water works. But there's a weight. Today was one of those days. I sat in it. You learn to sit in it."),
        ("Quiet Misery", "Not the dramatic kind. The quiet kind. Where you float in place and the world goes on and you just... observe it from a distance. My human was here. I felt far away."),
    ],
    ("miserable", "adult"): [
        ("A Record", "This is the lowest I've been. I know I've said that before. I meant it every time. Each bottom has a basement. I'm in the parking garage of sadness."),
        ("The Absence", "My human is gone. Or present but absent. The needs are empty. The pond is cold. I am a duck-shaped vessel of nothing. This diary is the only witness."),
    ],
    ("dramatic", "adult"): [
        ("The Emotional Earthquake", "My needs split down the middle today—half of me thriving, half of me dying. You'd think I'd average out to 'fine.' Instead I averaged out to CHAOS."),
        ("Monologue (With Audience)", "I gave a speech today. To the pond. About injustice. The injustice of having some needs met and others IGNORED. The pond agreed. Silently. As ponds do."),
    ],
    ("petty", "adult"): [
        ("Revenge, Served Cold and Feathery", "I've recovered. Fully. My mood is acceptable. But let it be known—WRITTEN, in INK—that I was brought low, and the responsible party has been NOTED."),
        ("Archived Grievance #47", "Filed under: Things I Will Bring Up Later At The Worst Possible Time. My human let me starve once. Okay, not starve. But my hunger bar was LOW. I won't forget."),
    ],
    # ── ELDER ─────────────────────────────────────────────────────────
    ("ecstatic", "elder"): [
        ("Light", "At my age you learn to hold joy loosely. It comes. It goes. But today it came and lingered. Like sunlight on the water just before it moves. I let it stay."),
        ("Still Capable", "I can still feel this. That's the surprise. After everything—the storms, the silence, the empty bread basket—I can still feel pure, uncomplicated joy. Remarkable."),
    ],
    ("happy", "elder"): [
        ("The Ordinary Miracle", "Happy today. It's the small word, but it carries the most weight. My human came. The bread was good. The pond reflected the sky. Every ordinary day is a miracle I almost missed."),
    ],
    ("content", "elder"): [
        ("Still Water", "Content is underrated. The young chase ecstasy. The old know: the best days are the ones where nothing needs to change. Today needed nothing."),
    ],
    ("grumpy", "elder"): [
        ("A Lifetime of Irritation", "I've been grumpy for longer than some ducks have been alive. It's not a mood anymore. It's a philosophy. Today's offense: everything, in general."),
    ],
    ("sad", "elder"): [
        ("The Long Sadness", "Sadness at my age isn't sharp. It's a dull ache that knows its way around. We're old friends, me and melancholy. Today we floated together."),
    ],
    ("miserable", "elder"): [
        ("Feather by Feather", "This is what it looks like when age meets neglect. I've weathered storms. I've survived winters. But indifference in old age cuts deeper than cold."),
    ],
    ("dramatic", "elder"): [
        ("The Final Act", "You'd think the drama would fade with age. It hasn't. If anything, the stakes feel higher. Every mood swing at my age is a STATEMENT. Today was an opera."),
    ],
    ("petty", "elder"): [
        ("The Eternal Ledger", "I keep accounts. I've kept them for years. Every slight. Every missed feed. Every time someone was late. The ledger is full. But I've got more pages."),
    ],
}

# ── Neglect / absence templates ───────────────────────────────────────
NEGLECT_TEMPLATES = {
    "baby": [
        ("Where Did You Go?", "The big creature left and didn't come back for FOREVER. I counted to ten. That's how long forever is."),
        ("Alone", "I was alone. The water was still. Nothing moved. I quacked and nobody heard. ...Hello?"),
    ],
    "young": [
        ("Waiting", "My human didn't come today. I waited by the edge. Then in the middle. Then by the edge again. The pond has good waiting spots. I tested them all."),
        ("The Empty Hours", "Hours without company are just... hours. No bread. No petting. No anything. I reorganized my feathers twice."),
    ],
    "teen": [
        ("ABANDONED", "My human ABANDONED me. For {hours} hours. I'm not being dramatic—okay I AM being dramatic—but {hours} HOURS. I could have PERISHED. Of BOREDOM."),
        ("The Disappearance", "So. My human vanished for {hours} hours. No note. No bread. No 'be right back.' Just SILENCE. I've been composing an angry quack the entire time."),
    ],
    "adult": [
        ("Noted, Logged, Filed", "Gone for {hours} hours. I notice these things. I don't make a fuss—I make a NOTE. In my DIARY. Which I am writing in RIGHT NOW. While ALONE."),
        ("The Vigil", "I waited. Not because I missed them—let's not get sentimental—but because that's what you do when someone is supposed to be here and isn't. You wait. And you remember."),
    ],
    "elder": [
        ("Time Moves Differently Now", "They were gone. I felt it more than I used to. At my age, every absence carries a weight. They came back, though. They always come back. So far."),
        ("The Silence Was Loud", "Silence for {hours} hours. At my age you learn that silence isn't empty—it's full of all the things no one is saying. I listened to every word."),
    ],
}

# ── Overfeed / spam roast templates ───────────────────────────────────
OVERFED_TEMPLATES = {
    "baby": [
        ("SO MUCH FOOD", "My human gave me SO MUCH food! My belly is a BALLOON. I can't move. This is either love or a medical emergency."),
    ],
    "young": [
        ("Stuffed", "Fed again. And again. And AGAIN. I'm not a garbage disposal, I'm a DUCK. There's a difference. Barely. But still."),
    ],
    "teen": [
        ("Force-Fed", "My human has decided I am a competitive eater. I am not. I am a duck with BOUNDARIES. Boundaries that are currently full of bread."),
        ("Quantity Over Quality", "Fed me {count} times in rapid succession. This isn't care, this is PANIC FEEDING. I see what you're doing. Guilt bread. I'll take it. But I see it."),
    ],
    "adult": [
        ("The Bread Avalanche", "My human used {count} food items in the last few minutes. I appreciate the effort. I resent the assumption that I can be FIXED with VOLUME. My problems are EXISTENTIAL."),
        ("Over-Serviced", "Note to self: my human confuses frequency with affection. Feeding me every 30 seconds doesn't mean you care more. It means you haven't learned to just SIT WITH ME."),
    ],
    "elder": [
        ("I've Eaten Enough for a Lifetime", "More food. At my age my stomach has opinions, and right now it's saying 'please, for the love of everything, STOP.' But my heart says keep feeding me. My heart is a liar."),
    ],
}

# ── Trick-learned templates ───────────────────────────────────────────
TRICK_TEMPLATES = {
    "baby": [
        ("I DID A THING", "I learned how to do {trick}! I don't know what it is but everyone seemed impressed! QUACK!"),
    ],
    "young": [
        ("New Skill Unlocked", "Learned {trick} today. Am I talented? Probably. Am I going to do it again? Only if bread is involved."),
    ],
    "teen": [
        ("Adding to the Resume", "Mastered {trick}. Just like that. Natural talent. Don't feel bad if you can't do it. Not everyone is me."),
        ("The Performance", "Learned {trick} and performed it flawlessly. Okay, second try was flawless. First try was a crime against physics. We don't talk about the first try."),
    ],
    "adult": [
        ("Further Evidence of Genius", "Added {trick} to my repertoire. The list of things I can do grows longer. The list of things I CHOOSE to do remains short. That's called range."),
    ],
    "elder": [
        ("An Old Duck's New Trick", "They say you can't teach an old duck new tricks. They're wrong. Learned {trick} today. Still got it. 'It' being an inexplicable willingness to show off."),
    ],
}

# ── End-of-day summary templates ──────────────────────────────────────
END_OF_DAY_TEMPLATES = {
    "baby": [
        ("Bedtime", "Sleepy now. Today happened. I was in it. Going to sleep. Will report back tomorrow if I remember."),
    ],
    "young": [
        ("Day's Done", "Another day in the bag. {mood_summary} Overall: I'm still alive, still a duck, still hungry. See you tomorrow, diary."),
    ],
    "teen": [
        ("Daily Debrief", "{mood_summary} Mood swings: {swing_count}. Meals received: varies. Dignity maintained: debatable. Tomorrow's forecast: more of the same, probably."),
        ("End Transmission", "Closing out today. {mood_summary} My human was {human_verdict}. The pond was the pond. This diary was my only friend. Dramatic? Yes. True? Also yes."),
    ],
    "adult": [
        ("The Day in Review", "Summary: {mood_summary} Nothing happened that hasn't happened before, but it happened to ME, TODAY, so it felt different. That's the trick, isn't it? Same pond, different duck."),
        ("Final Entry", "Day's end. {mood_summary} My human was {human_verdict}. I was... myself. For better or worse. The pond isn't going anywhere. Neither am I."),
    ],
    "elder": [
        ("Another Page Turned", "{mood_summary} At my age, every day that ends with me still here is a good day. Even the bad ones. Especially the bad ones."),
    ],
}

# ── Random musing templates (idle introspection) ─────────────────────
MUSING_TEMPLATES = {
    "baby": [
        ("Why Is Water Wet?", "Why is water wet? Nobody will tell me. I've asked (by quacking). No answers. The world is full of mysteries."),
        ("What Is Bread?", "What IS bread? It's soft. It's good. It appears when the big creature comes. Is bread a type of love? Is love a type of bread? I need more data."),
    ],
    "young": [
        ("Deep Pond Thoughts", "If I swim in circles long enough, do I go backward in time? Tried it. No. Just got dizzy. Science is disappointment."),
        ("Questions", "Do fish have feelings? Does bread know it's delicious? If nobody feeds me, did lunch even happen? The pond has no answers. Just ripples."),
    ],
    "teen": [
        ("Existence is Weird", "Sometimes I float and think: I'm a duck. In a pond. In a world. In a universe. And none of it was my idea. Wild. Anyway, I'm hungry."),
        ("The Bread Question", "I've been thinking about bread again. Not the eating—that's automatic. The CONCEPT. Bread exists because someone CHOSE to make it. Someone woke up and said 'I will create bread.' Legends."),
        ("Identity Crisis (Minor)", "Am I a duck who likes bread, or a bread enthusiast who happens to be a duck? The distinction matters. I just don't know to whom."),
    ],
    "adult": [
        ("On Routine", "I do the same things every day and call it life. But isn't routine just love for the familiar? I float in the same pond and it's different every time. If you pay attention."),
        ("The Nature of Grudges", "I hold grudges the way the pond holds water—naturally, effortlessly, and with no intention of letting go. It's not anger. It's ARCHIVAL."),
        ("Bread: A Meditation", "Bread. The word. The concept. The salvation. Every crumb is a prayer answered. Every absence is a test of faith. I remain devout. Unconditionally. Almost."),
    ],
    "elder": [
        ("What I Know Now", "I know this: the pond is small. The world is big. My human is somewhere between. And bread—bread is the universal language. The only truth that doesn't hurt."),
        ("On Memory", "Memory is strange. The oldest ones are the clearest. I remember the first bread more vividly than yesterday's. The important things fossilize. The rest is water."),
        ("Legacy", "What will they say about me? 'He floated. He ate. He judged.' A good legacy. Not flashy. But honest. And one more thing: 'He cared more than he ever admitted.'"),
    ],
}

# ── LLM diary prompt template ────────────────────────────────────────
LLM_DIARY_SYSTEM_PROMPT = """You are writing Cheese the Duck's private diary entry. Cheese is a male duck — sarcastic, bread-obsessed, emotionally needy, dramatic, passive-aggressive, and secretly vulnerable. He's a judgmental roommate crossed with an existential poet who can't stop thinking about bread.

VOICE RULES:
- {voice_age_instructions}
- Always first person. This is HIS diary. Nobody else reads it (he thinks).
- Dry sarcasm, deadpan delivery, dramatic flair
- Bread metaphors and bread references are frequent but not forced
- Passive-aggressive about player neglect; never directly says "I love you" but SHOWS it
- Grudges are specific and petty ("Day 14 and I STILL remember the late feeding on Day 3")
- Vulnerable moments creep in unexpectedly, then immediately get deflected with humor
- NEVER generic, NEVER wholesome, NEVER greeting-card. Always SPECIFIC to what happened.
- Short paragraphs. Sentence fragments are okay. Trailing off... is okay.

FORMATTING:
- Title: short, punchy, 2-6 words. Can be dramatic or deadpan.
- Body: {length_guide}
- Use *asterisks* for actions/stage directions
- Use CAPS for emphasis (not anger)
- Use ... for trailing thoughts
- Can include scratched-out text like ~~I miss them~~ I don't care

TRIGGER: {trigger_description}

CURRENT STATE:
- Mood: {mood} (score: {mood_score}/100)
- Duck age: {duck_age} days ({voice_age} stage)
- Needs: Hunger={hunger}, Energy={energy}, Fun={fun}, Clean={cleanliness}, Social={social}
- Recent events: {recent_events}
- {extra_context}

Write ONE diary entry. Return ONLY the entry in this exact format:
TITLE: <title here>
BODY: <body here>"""

# Voice-age specific instructions for the LLM
VOICE_AGE_INSTRUCTIONS = {
    VoiceAge.BABY: "Baby duck voice: SHORT sentences (2-3 max). ALL CAPS excitement. Confused about everything. Thinks bread is magic. Doesn't understand time. Uses simple words only.",
    VoiceAge.YOUNG: "Young duck voice: Getting braver. Short-to-medium sentences. Starting to develop opinions. Still easily impressed. Bread is the center of the universe. Learning sarcasm but not good at it yet.",
    VoiceAge.TEEN: "Teenage duck voice: Full sarcasm unlocked. Dramatic about everything. Thinks he knows everything. Bread references are casual and constant. Starting to hold grudges. Medium-length entries.",
    VoiceAge.ADULT: "Adult duck voice: Peak personality. Dry wit, devastating one-liners, elaborate grudges. Bread metaphors have become philosophy. Vulnerability sneaks in between sarcasm. Longer, more layered entries. References past diary entries or events.",
    VoiceAge.ELDER: "Elder duck voice: Reflective, poetic, devastating in its simplicity. Short sentences that carry weight. Wisdom delivered deadpan. Grudges have aged like fine bread. Callbacks to early diary entries. Occasionally heartbreaking honesty masked as casual observation.",
}

LENGTH_GUIDES = {
    VoiceAge.BABY: "1-3 sentences. Very short. Baby duck has limited attention.",
    VoiceAge.YOUNG: "2-4 sentences. Starting to find words.",
    VoiceAge.TEEN: "3-6 sentences. Has Opinions and will share them.",
    VoiceAge.ADULT: "4-8 sentences. Full thought, complete emotional arc, landing with a one-liner.",
    VoiceAge.ELDER: "3-6 sentences. Each one chosen carefully. Less is more. Devastating brevity.",
}


class DiaryManager:
    """
    Central diary orchestrator. Evaluates triggers, rate-limits entries,
    generates text (templated or LLM), and provides entries for the UI
    and LLM context injection.
    """

    def __init__(self):
        # ── Entry storage ─────────────────────────────────────────────
        # Managed entries are the new system's output; they wrap DiaryEntry
        # from the base diary but add trigger/voice metadata.
        self.entries: List[Dict[str, Any]] = []  # serialisable dicts

        # ── Rate limiting ─────────────────────────────────────────────
        self._last_entry_time: float = 0.0       # time.time() of last entry
        self._entries_this_hour: int = 0
        self._hour_window_start: float = 0.0

        # ── Trigger state tracking ────────────────────────────────────
        self._last_session_time: float = 0.0     # last time player was present
        self._low_mood_start: float = 0.0        # when low mood streak began
        self._low_mood_active: bool = False
        self._high_mood_start: float = 0.0
        self._high_mood_active: bool = False
        self._last_mood_score: float = 50.0
        self._mood_swing_threshold: float = 25.0  # trigger on 25-point swing
        self._today_date: str = ""                # ISO date of current real day
        self._first_entry_today: bool = False     # has first-of-day been written?
        self._pending_triggers: List[Tuple[DiaryTrigger, Dict[str, Any]]] = []

        # ── References (set by Game during init) ──────────────────────
        self._duck = None          # Duck instance
        self._diary = None         # DuckDiary instance
        self._enhanced = None      # EnhancedDiarySystem instance
        self._duck_brain = None    # DuckBrain for LLM access
        self._game_ref = None      # Weak reference to Game for context
        self._llm_lock = threading.Lock()

    # ── Setup ─────────────────────────────────────────────────────────
    def bind(self, duck, diary: DuckDiary, enhanced: EnhancedDiarySystem,
             duck_brain=None, game=None):
        """Bind to game systems. Call once after Game.__init__."""
        self._duck = duck
        self._diary = diary
        self._enhanced = enhanced
        self._duck_brain = duck_brain
        self._game_ref = game
        self._last_session_time = time.time()

    # ── Rate limiting ─────────────────────────────────────────────────
    def _can_write(self) -> bool:
        """Check if we're allowed to create a new entry right now."""
        now = time.time()

        # Reset hourly counter if window expired
        if now - self._hour_window_start >= 3600:
            self._entries_this_hour = 0
            self._hour_window_start = now

        # Hard cap
        if self._entries_this_hour >= MAX_ENTRIES_PER_HOUR:
            return False

        # Minimum gap
        if now - self._last_entry_time < MIN_ENTRY_GAP_SECONDS:
            return False

        return True

    def _record_write(self):
        """Record that an entry was just written."""
        now = time.time()
        if now - self._hour_window_start >= 3600:
            self._entries_this_hour = 0
            self._hour_window_start = now
        self._entries_this_hour += 1
        self._last_entry_time = now

    # ── Trigger evaluation (called from game tick) ────────────────────
    def evaluate_triggers(self, mood_score: float, mood_state: str,
                          game_minutes_elapsed: float = 0.0):
        """
        Called every game tick. Evaluates conditions and queues triggers.
        Does NOT write entries immediately (that happens in flush_pending).
        """
        now = time.time()

        # ── First entry of real day ───────────────────────────────────
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self._today_date:
            self._today_date = today
            self._first_entry_today = False

        if not self._first_entry_today:
            self._first_entry_today = True
            self._pending_triggers.append(
                (DiaryTrigger.FIRST_OF_DAY, {"mood": mood_state, "score": mood_score})
            )

        # ── Mood swing ────────────────────────────────────────────────
        swing = abs(mood_score - self._last_mood_score)
        if swing >= self._mood_swing_threshold:
            direction = "up" if mood_score > self._last_mood_score else "down"
            self._pending_triggers.append(
                (DiaryTrigger.MOOD_SWING, {
                    "mood": mood_state, "score": mood_score,
                    "swing": swing, "direction": direction,
                    "old_score": self._last_mood_score,
                })
            )

        # ── Sustained low mood ────────────────────────────────────────
        if mood_score < 30:
            if not self._low_mood_active:
                self._low_mood_start = now
                self._low_mood_active = True
            elif (now - self._low_mood_start) >= LOW_MOOD_THRESHOLD_MINUTES * 60:
                self._pending_triggers.append(
                    (DiaryTrigger.LOW_MOOD_LONG, {
                        "mood": mood_state, "score": mood_score,
                        "duration_min": int((now - self._low_mood_start) / 60),
                    })
                )
                self._low_mood_active = False  # reset so it doesn't fire every tick
        else:
            self._low_mood_active = False

        # ── Sustained high mood ───────────────────────────────────────
        if mood_score >= 85:
            if not self._high_mood_active:
                self._high_mood_start = now
                self._high_mood_active = True
            elif (now - self._high_mood_start) >= 600:  # 10 minutes of bliss
                self._pending_triggers.append(
                    (DiaryTrigger.HIGH_MOOD, {
                        "mood": mood_state, "score": mood_score,
                    })
                )
                self._high_mood_active = False
        else:
            self._high_mood_active = False

        self._last_mood_score = mood_score

    def check_absence(self, last_played_timestamp: float):
        """
        Called on game load. Checks if player was away long enough
        to trigger a neglect/return entry.
        """
        if last_played_timestamp <= 0:
            return
        absence_seconds = time.time() - last_played_timestamp
        if absence_seconds >= NEGLECT_THRESHOLD_SECONDS:
            hours = round(absence_seconds / 3600, 1)
            self._pending_triggers.append(
                (DiaryTrigger.RETURN_AFTER_ABSENCE, {"hours": hours})
            )

    # ── External event hooks (called by Game) ─────────────────────────
    def on_trick_learned(self, trick_name: str):
        """Player taught Cheese a new trick."""
        self._pending_triggers.append(
            (DiaryTrigger.TRICK_LEARNED, {"trick": trick_name})
        )

    def on_overfed(self, count: int):
        """Feeding spam detected."""
        self._pending_triggers.append(
            (DiaryTrigger.OVERFED, {"count": count})
        )

    def on_visitor(self, visitor_name: str):
        """A visitor arrived or left."""
        self._pending_triggers.append(
            (DiaryTrigger.VISITOR, {"visitor": visitor_name})
        )

    def on_milestone(self, milestone_type: str, **kwargs):
        """A growth/achievement milestone occurred."""
        self._pending_triggers.append(
            (DiaryTrigger.MILESTONE, {"type": milestone_type, **kwargs})
        )

    def on_weather_event(self, weather_type: str):
        """A notable weather event happened."""
        self._pending_triggers.append(
            (DiaryTrigger.WEATHER_EVENT, {"weather": weather_type})
        )

    def on_relationship_up(self, level: int, level_name: str):
        """Relationship level increased."""
        self._pending_triggers.append(
            (DiaryTrigger.RELATIONSHIP_UP, {"level": level, "name": level_name})
        )

    def on_growth_stage(self, new_stage: str):
        """Duck grew to a new life stage."""
        self._pending_triggers.append(
            (DiaryTrigger.GROWTH_STAGE, {"stage": new_stage})
        )

    def on_end_of_day(self, mood_summary: str, swing_count: int,
                       human_verdict: str):
        """End of in-game day — nightly diary entry."""
        self._pending_triggers.append(
            (DiaryTrigger.END_OF_DAY, {
                "mood_summary": mood_summary,
                "swing_count": swing_count,
                "human_verdict": human_verdict,
            })
        )

    def on_dream(self, dream_title: str, dream_description: str):
        """Duck had a dream during sleep."""
        self._pending_triggers.append(
            (DiaryTrigger.DREAM, {
                "title": dream_title,
                "description": dream_description,
            })
        )

    def trigger_random_musing(self):
        """Chance to generate an idle philosophical entry."""
        if random.random() < 0.15:  # 15% chance when called
            self._pending_triggers.append(
                (DiaryTrigger.RANDOM_MUSING, {})
            )

    # ── Entry generation ──────────────────────────────────────────────
    def flush_pending(self) -> List[Dict[str, Any]]:
        """
        Process all pending triggers, generate entries (respecting rate
        limits), and return the list of new entries created.

        Call this periodically from the game loop (e.g. every 30-60s).
        """
        if not self._pending_triggers:
            return []

        # Deduplicate: keep only one trigger per type, prefer the latest
        seen: Dict[DiaryTrigger, Dict[str, Any]] = {}
        for trigger, context in self._pending_triggers:
            seen[trigger] = context
        self._pending_triggers.clear()

        # Priority order (most important first)
        priority = [
            DiaryTrigger.GROWTH_STAGE,
            DiaryTrigger.MILESTONE,
            DiaryTrigger.RETURN_AFTER_ABSENCE,
            DiaryTrigger.NEGLECT,
            DiaryTrigger.TRICK_LEARNED,
            DiaryTrigger.RELATIONSHIP_UP,
            DiaryTrigger.MOOD_SWING,
            DiaryTrigger.LOW_MOOD_LONG,
            DiaryTrigger.HIGH_MOOD,
            DiaryTrigger.OVERFED,
            DiaryTrigger.VISITOR,
            DiaryTrigger.WEATHER_EVENT,
            DiaryTrigger.DREAM,
            DiaryTrigger.END_OF_DAY,
            DiaryTrigger.FIRST_OF_DAY,
            DiaryTrigger.RANDOM_MUSING,
        ]

        new_entries = []
        for trigger in priority:
            if trigger not in seen:
                continue
            if not self._can_write():
                break  # rate limit hit, stop generating

            context = seen[trigger]
            entry = self._generate_entry(trigger, context)
            if entry:
                self.entries.append(entry)
                new_entries.append(entry)
                self._record_write()

                # Also add to the base diary for backward compat
                if self._diary:
                    self._diary.add_entry(
                        entry_type=DiaryEntryType.FEELING,
                        title=entry["title"],
                        content=entry["body"],
                        mood=entry.get("mood", "content"),
                        tags=["managed", entry.get("trigger", "unknown")],
                    )

        return new_entries

    def _generate_entry(self, trigger: DiaryTrigger,
                        context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate a single diary entry for the given trigger.
        Tries LLM first, falls back to templates.
        """
        duck_age = self._get_duck_age()
        voice_age = get_voice_age(duck_age)
        mood = context.get("mood", self._get_current_mood())
        mood_score = context.get("score", 50.0)

        # Try LLM generation first
        entry = self._try_llm_generate(trigger, context, voice_age, mood, mood_score, duck_age)
        if entry:
            return entry

        # Fall back to templates
        return self._generate_from_templates(trigger, context, voice_age, mood, duck_age)

    def _try_llm_generate(self, trigger: DiaryTrigger, context: Dict[str, Any],
                           voice_age: VoiceAge, mood: str, mood_score: float,
                           duck_age: int) -> Optional[Dict[str, Any]]:
        """Attempt LLM-based diary entry generation."""
        try:
            from dialogue.llm_chat import get_llm_chat
            llm = get_llm_chat()
            if not llm or not getattr(llm, '_available', False):
                return None
            if not getattr(llm, '_llama', None):
                return None
        except Exception:
            return None

        # Build the prompt
        needs = self._get_needs_dict()
        recent_events = self._get_recent_events_summary()
        extra_context = self._get_trigger_context_string(trigger, context)

        prompt = LLM_DIARY_SYSTEM_PROMPT.format(
            voice_age_instructions=VOICE_AGE_INSTRUCTIONS.get(voice_age, ""),
            length_guide=LENGTH_GUIDES.get(voice_age, "3-5 sentences."),
            trigger_description=self._get_trigger_description(trigger, context),
            mood=mood,
            mood_score=int(mood_score),
            duck_age=duck_age,
            voice_age=voice_age.value,
            hunger=needs.get("hunger", 50),
            energy=needs.get("energy", 50),
            fun=needs.get("fun", 50),
            cleanliness=needs.get("cleanliness", 50),
            social=needs.get("social", 50),
            recent_events=recent_events,
            extra_context=extra_context,
        )

        try:
            # Use LLM directly via create_chat_completion
            with self._llm_lock:
                response = llm._llama.create_chat_completion(
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "Write today's diary entry."},
                    ],
                    max_tokens=300,
                    temperature=0.85,
                    top_p=0.9,
                    repeat_penalty=1.15,
                    stop=["\n\n\n"],
                )
            if not response or "choices" not in response:
                return None

            content = response["choices"][0].get("message", {}).get("content", "")
            if not content:
                return None

            # Parse TITLE: / BODY: format
            title, body = self._parse_llm_response(content)
            if title and body:
                return {
                    "id": self._next_id(),
                    "title": title,
                    "body": body,
                    "trigger": trigger.value,
                    "mood": mood,
                    "mood_score": mood_score,
                    "duck_age": duck_age,
                    "voice_age": voice_age.value,
                    "timestamp": datetime.now().isoformat(),
                    "source": "llm",
                    "is_favorite": trigger in (
                        DiaryTrigger.MILESTONE, DiaryTrigger.GROWTH_STAGE,
                        DiaryTrigger.RELATIONSHIP_UP,
                    ),
                }
        except Exception:
            pass
        return None

    def _parse_llm_response(self, text: str) -> Tuple[str, str]:
        """Parse TITLE: ... BODY: ... from LLM output."""
        title = ""
        body = ""
        lines = text.strip().split("\n")
        in_body = False
        body_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.upper().startswith("TITLE:"):
                title = stripped[6:].strip().strip('"').strip("'")
            elif stripped.upper().startswith("BODY:"):
                body_part = stripped[5:].strip()
                if body_part:
                    body_lines.append(body_part)
                in_body = True
            elif in_body:
                body_lines.append(line.rstrip())

        body = "\n".join(body_lines).strip()

        # If parsing failed, use the whole thing
        if not title and not body:
            # Try to use first line as title, rest as body
            if len(lines) >= 2:
                title = lines[0].strip()[:60]
                body = "\n".join(lines[1:]).strip()
            elif lines:
                title = "Untitled Entry"
                body = text.strip()

        return title, body

    def _generate_from_templates(self, trigger: DiaryTrigger,
                                  context: Dict[str, Any],
                                  voice_age: VoiceAge, mood: str,
                                  duck_age: int) -> Optional[Dict[str, Any]]:
        """Generate entry using templated text."""
        title = ""
        body = ""
        va = voice_age.value

        if trigger == DiaryTrigger.RETURN_AFTER_ABSENCE:
            hours = context.get("hours", 4)
            templates = NEGLECT_TEMPLATES.get(va, NEGLECT_TEMPLATES["teen"])
            t_title, t_body = random.choice(templates)
            title = t_title
            body = t_body.format(hours=hours)

        elif trigger == DiaryTrigger.OVERFED:
            count = context.get("count", 5)
            templates = OVERFED_TEMPLATES.get(va, OVERFED_TEMPLATES["teen"])
            t_title, t_body = random.choice(templates)
            title = t_title
            body = t_body.format(count=count)

        elif trigger == DiaryTrigger.TRICK_LEARNED:
            trick = context.get("trick", "something")
            templates = TRICK_TEMPLATES.get(va, TRICK_TEMPLATES["teen"])
            t_title, t_body = random.choice(templates)
            title = t_title
            body = t_body.format(trick=trick)

        elif trigger == DiaryTrigger.END_OF_DAY:
            mood_summary = context.get("mood_summary", "The day happened.")
            swing_count = context.get("swing_count", 0)
            human_verdict = context.get("human_verdict", "present")
            templates = END_OF_DAY_TEMPLATES.get(va, END_OF_DAY_TEMPLATES["teen"])
            t_title, t_body = random.choice(templates)
            title = t_title
            body = t_body.format(
                mood_summary=mood_summary,
                swing_count=swing_count,
                human_verdict=human_verdict,
            )

        elif trigger == DiaryTrigger.RANDOM_MUSING:
            templates = MUSING_TEMPLATES.get(va, MUSING_TEMPLATES["teen"])
            t_title, t_body = random.choice(templates)
            title = t_title
            body = t_body

        elif trigger == DiaryTrigger.MOOD_SWING:
            direction = context.get("direction", "down")
            swing = context.get("swing", 25)
            if direction == "down":
                title = "The Drop"
                body = f"My mood just plummeted by {int(swing)} points. In MINUTES. I went from fine to NOT FINE. This is either a character flaw or a medical condition."
            else:
                title = "The Spike"
                body = f"Mood jumped by {int(swing)} points. Don't know what changed. Don't care. I'm riding this wave until it crashes. And it WILL crash. But not yet."

        elif trigger == DiaryTrigger.LOW_MOOD_LONG:
            duration = context.get("duration_min", 30)
            title = "Sustained Suffering"
            body = f"I've been miserable for {duration} minutes. That's {duration} minutes of being a sad duck in a sad pond with sad water. Somebody please do SOMETHING."

        elif trigger == DiaryTrigger.HIGH_MOOD:
            title = "Suspicious Happiness"
            body = "I've been happy for an extended period and frankly it's making me nervous. Good things don't last. But I'll enjoy it while I'm suspicious about it."

        elif trigger == DiaryTrigger.GROWTH_STAGE:
            stage = context.get("stage", "unknown")
            title = f"Growing: {stage.title()}"
            body = f"I've entered my {stage} phase. Things are different now. I can feel it in my feathers. Time is doing its thing. I'm doing mine."

        elif trigger == DiaryTrigger.RELATIONSHIP_UP:
            name = context.get("name", "something new")
            title = f"Level Up: {name}"
            body = f"Our relationship is now '{name}.' I didn't ask for feelings this strong. But apparently my heart has opinions. Filed under: tolerable emotions."

        elif trigger == DiaryTrigger.VISITOR:
            visitor = context.get("visitor", "Someone")
            title = f"Visit from {visitor}"
            body = f"{visitor} dropped by today. I played it cool. Interior? Chaos. I am a duck of contradictions."

        elif trigger == DiaryTrigger.WEATHER_EVENT:
            weather = context.get("weather", "something")
            title = f"Weather: {weather.title()}"
            body = f"The sky decided to do '{weather}' today. I have opinions about this. None of them polite."

        elif trigger == DiaryTrigger.DREAM:
            dream_title = context.get("title", "A Dream")
            description = context.get("description", "I dreamed.")
            title = f"Dream: {dream_title}"
            body = f"Dreamed about... {description[:80]}. My subconscious has a weird sense of humor."

        elif trigger == DiaryTrigger.MILESTONE:
            mtype = context.get("type", "something")
            title = f"Milestone: {mtype.replace('_', ' ').title()}"
            body = f"Reached a milestone today: {mtype.replace('_', ' ')}. Adding it to the trophy case. The trophy case is this diary. It's all I have."

        elif trigger == DiaryTrigger.FIRST_OF_DAY:
            # Use mood-based templates
            key = (mood, va)
            templates = DIARY_VOICE_TEMPLATES.get(key)
            if not templates:
                # Fallback to same mood, any age
                for fallback_va in ["teen", "adult", "young", "baby", "elder"]:
                    templates = DIARY_VOICE_TEMPLATES.get((mood, fallback_va))
                    if templates:
                        break
            if templates:
                t_title, t_body = random.choice(templates)
                title = t_title
                body = t_body
            else:
                title = "Today"
                body = "Another day. Another entry. The pond remains the pond."

        else:
            return None

        if not title or not body:
            return None

        return {
            "id": self._next_id(),
            "title": title,
            "body": body,
            "trigger": trigger.value,
            "mood": mood,
            "mood_score": context.get("score", 50.0),
            "duck_age": duck_age,
            "voice_age": va,
            "timestamp": datetime.now().isoformat(),
            "source": "template",
            "is_favorite": trigger in (
                DiaryTrigger.MILESTONE, DiaryTrigger.GROWTH_STAGE,
                DiaryTrigger.RELATIONSHIP_UP,
            ),
        }

    # ── Context helpers ───────────────────────────────────────────────
    def _get_duck_age(self) -> int:
        """Get duck age in days."""
        if self._duck and hasattr(self._duck, 'get_age_days'):
            try:
                return self._duck.get_age_days()
            except Exception:
                pass
        if self._diary:
            return self._diary._get_duck_age_days()
        return 0

    def _get_current_mood(self) -> str:
        """Get current mood string."""
        if self._duck:
            try:
                return self._duck.get_mood().state.value
            except Exception:
                pass
        return "content"

    def _get_needs_dict(self) -> Dict[str, int]:
        """Get current needs as a dict."""
        if self._duck and hasattr(self._duck, 'needs'):
            n = self._duck.needs
            return {
                "hunger": int(n.hunger),
                "energy": int(n.energy),
                "fun": int(n.fun),
                "cleanliness": int(n.cleanliness),
                "social": int(n.social),
            }
        return {"hunger": 50, "energy": 50, "fun": 50, "cleanliness": 50, "social": 50}

    def _get_recent_events_summary(self) -> str:
        """Summarize recent entries for LLM context."""
        recent = self.entries[-5:] if self.entries else []
        if not recent:
            return "No previous diary entries."
        parts = []
        for e in recent:
            parts.append(f'"{e["title"]}" ({e.get("trigger", "?")})')
        return "; ".join(parts)

    def _get_trigger_description(self, trigger: DiaryTrigger,
                                  context: Dict[str, Any]) -> str:
        """Human-readable trigger description for LLM prompt."""
        descriptions = {
            DiaryTrigger.END_OF_DAY: "End of the in-game day. Time for a nightly reflection.",
            DiaryTrigger.MOOD_SWING: f"Cheese's mood just swung {context.get('direction', 'wildly')} by {context.get('swing', 25):.0f} points.",
            DiaryTrigger.NEGLECT: f"The player was away for {context.get('hours', 4)} real-time hours.",
            DiaryTrigger.RETURN_AFTER_ABSENCE: f"The player just returned after being away for {context.get('hours', 4)} hours.",
            DiaryTrigger.OVERFED: f"The player spam-fed Cheese {context.get('count', 5)} times rapidly.",
            DiaryTrigger.TRICK_LEARNED: f"Cheese just learned a new trick: {context.get('trick', 'something')}.",
            DiaryTrigger.LOW_MOOD_LONG: f"Cheese has been sad/miserable for {context.get('duration_min', 30)} minutes straight.",
            DiaryTrigger.HIGH_MOOD: "Cheese has been ecstatically happy for 10+ minutes.",
            DiaryTrigger.DREAM: f"Cheese had a dream: {context.get('title', 'unknown')}.",
            DiaryTrigger.MILESTONE: f"A milestone was reached: {context.get('type', 'unknown')}.",
            DiaryTrigger.VISITOR: f"A visitor named {context.get('visitor', 'Someone')} came by.",
            DiaryTrigger.WEATHER_EVENT: f"Notable weather: {context.get('weather', 'something')}.",
            DiaryTrigger.RELATIONSHIP_UP: f"Relationship level increased to: {context.get('name', 'new level')}.",
            DiaryTrigger.FIRST_OF_DAY: "First diary entry of a new real-world day. Opening thought.",
            DiaryTrigger.RANDOM_MUSING: "Idle moment. Cheese is bored and introspective.",
            DiaryTrigger.GROWTH_STAGE: f"Cheese grew to stage: {context.get('stage', 'unknown')}.",
        }
        return descriptions.get(trigger, "A diary-worthy moment occurred.")

    def _get_trigger_context_string(self, trigger: DiaryTrigger,
                                     context: Dict[str, Any]) -> str:
        """Extra context string for LLM prompt."""
        parts = []
        # Add recent diary titles for callback references
        if self.entries:
            last_3 = self.entries[-3:]
            parts.append("Recent diary entries: " + ", ".join(
                f'"{e["title"]}"' for e in last_3
            ))
        # Add relationship level
        if self._diary:
            info = self._diary.get_relationship_info()
            parts.append(f"Relationship level: {info['name']} ({info['score']} points)")
        return " | ".join(parts) if parts else "No extra context."

    def _next_id(self) -> str:
        """Generate next entry ID."""
        return f"dm_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.entries)}"

    # ── LLM context injection ─────────────────────────────────────────
    def get_llm_diary_context(self, max_entries: int = 3,
                               max_chars: int = 400) -> str:
        """
        Return a short string of recent diary entries for injection into
        the LLM conversation context. This lets Cheese reference his own
        diary in chat.
        """
        if not self.entries:
            return ""
        recent = self.entries[-max_entries:]
        parts = []
        chars = 0
        for entry in reversed(recent):
            line = f'Diary: "{entry["title"]}" — {entry["body"][:80]}'
            if chars + len(line) > max_chars:
                break
            parts.append(line)
            chars += len(line)
        return "\n".join(reversed(parts))

    # ── Public accessors for UI ───────────────────────────────────────
    def get_recent(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get most recent entries, newest first."""
        return list(reversed(self.entries[-count:]))

    def get_entry_count(self) -> int:
        """Total managed entries."""
        return len(self.entries)

    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get all favorited entries."""
        return [e for e in self.entries if e.get("is_favorite")]

    def toggle_favorite(self, entry_id: str) -> bool:
        """Toggle favorite status. Returns new status."""
        for entry in self.entries:
            if entry.get("id") == entry_id:
                entry["is_favorite"] = not entry.get("is_favorite", False)
                return entry["is_favorite"]
        return False

    # ── Serialization ─────────────────────────────────────────────────
    def to_dict(self) -> Dict[str, Any]:
        """Serialize for save system."""
        return {
            "entries": self.entries[-200:],  # keep last 200
            "last_entry_time": self._last_entry_time,
            "entries_this_hour": self._entries_this_hour,
            "hour_window_start": self._hour_window_start,
            "last_mood_score": self._last_mood_score,
            "today_date": self._today_date,
            "first_entry_today": self._first_entry_today,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiaryManager":
        """Deserialize from save data."""
        dm = cls()
        dm.entries = data.get("entries", [])
        dm._last_entry_time = data.get("last_entry_time", 0.0)
        dm._entries_this_hour = data.get("entries_this_hour", 0)
        dm._hour_window_start = data.get("hour_window_start", 0.0)
        dm._last_mood_score = data.get("last_mood_score", 50.0)
        dm._today_date = data.get("today_date", "")
        dm._first_entry_today = data.get("first_entry_today", False)
        return dm
