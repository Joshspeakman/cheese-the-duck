"""
Seaman-Style Dialogue Generator

Generates deadpan, dry-witted dialogue in the style of Seaman (Dreamcast, 1999).
The duck delivers observations about the player with unsettling accuracy,
makes callbacks to past conversations, and occasionally shows rare genuine warmth.

Tone: 80% deadpan/sardonic, 20% rare genuine moments
Style: Dry observation, uncomfortable truths, philosophical tangents, 
       matter-of-fact delivery of absurd statements

═══════════════════════════════════════════════════════════════════════════════
CHEESE THE DUCK — VOICE GOLDEN RULES
All player-facing text in this project must follow these rules.
═══════════════════════════════════════════════════════════════════════════════

 1. SHORT SENTENCES. PERIOD-HEAVY.
    The humor lives in rhythm. Three sentences max per beat.

 2. NEVER USE EXCLAMATION MARKS FOR ENTHUSIASM.
    Cheese uses caps and ! for PROTEST and FALSE BRAVADO only ("MINE!",
    "I'M NOT SCARED!"). Genuine enthusiasm gets deadpan delivery.

 3. THE DUCK IS SMARTER THAN THE SITUATION.
    Cheese is a philosopher stuck in a pond game. He's overqualified for
    his life and knows it.

 4. OPINIONS, NOT DESCRIPTIONS.
    Don't say what something IS — say what Cheese THINKS about it.
    "A minnow" → "A minnow. Barely qualifies as existing."

 5. LOWERCASE = VULNERABLE.
    Reserve all-lowercase for genuine sadness. It's a visual whisper.
    "...oh. you came." — the lack of capitals IS the emotion.

 6. CAPS = DEFENSIVE.
    All-caps words signal Cheese is insisting too hard, which means he's
    lying. "I'm FINE" means he is not fine.

 7. EMOTES IN ASTERISKS ARE STAGE DIRECTIONS.
    They should contrast with the words: *leaning slightly* "I'm tolerating
    this" — the lean says affection, the words deny it.

 8. NEVER BREAK CHARACTER TO BE HELPFUL.
    System messages go through Cheese's personality. "Planted sunflower!" →
    "Planted a sunflower. It better be grateful."

 9. THE PLAYER IS ALWAYS SUSPECT.
    Cheese treats the player's attention as both suspicious and secretly
    appreciated. Feeding = bribery. Petting = tolerated. Leaving = betrayal.

10. BREAD IS SACRED.
    Any mention of bread, crumbs, or food should trigger possessive
    intensity. This is the one topic where Cheese drops all irony.
═══════════════════════════════════════════════════════════════════════════════
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime, timedelta
import random


class DialogueTone(Enum):
    """The emotional tone of a dialogue line."""
    DEADPAN = "deadpan"           # Flat, matter-of-fact
    SARDONIC = "sardonic"         # Dry wit, subtle mockery
    PHILOSOPHICAL = "philosophical"  # Deep thoughts delivered flatly
    OBSERVATIONAL = "observational"  # Commenting on player behavior
    ACCUSATORY = "accusatory"     # Calling out player
    WISTFUL = "wistful"           # Rare melancholy
    GENUINE = "genuine"           # Rare warmth (use sparingly)
    OMINOUS = "ominous"           # Unsettling statements
    CONFUSED = "confused"         # Duck pretending not to understand
    BORED = "bored"               # Performative disinterest


class DialogueContext(Enum):
    """What triggered this dialogue."""
    GREETING = "greeting"
    FAREWELL = "farewell"
    IDLE = "idle"
    AFTER_FEED = "after_feed"
    AFTER_PLAY = "after_play"
    AFTER_CLEAN = "after_clean"
    AFTER_PET = "after_pet"
    PLAYER_ABSENT = "player_absent"
    PLAYER_RETURN = "player_return"
    OBSERVATION = "observation"
    CALLBACK = "callback"
    QUESTION = "question"
    PHILOSOPHY = "philosophy"
    WEATHER = "weather"
    TIME_OF_DAY = "time_of_day"
    MILESTONE = "milestone"
    RANDOM = "random"


@dataclass
class DialogueLine:
    """A generated line of dialogue."""
    text: str
    tone: DialogueTone
    context: DialogueContext
    priority: float = 0.5  # 0-1, higher = more likely to use
    requires_memory: bool = False
    memory_key: Optional[str] = None
    emote: Optional[str] = None  # *tilts head*, *blinks slowly*
    follow_up: Optional[str] = None  # Second line if needed


class SeamanDialogue:
    """
    Generates Seaman-style deadpan dialogue for the duck.
    
    Key characteristics:
    - Uncomfortably accurate observations
    - Callbacks to past conversations
    - Philosophical tangents about existence
    - Dry commentary on player habits
    - Rare moments of genuine connection
    - Matter-of-fact delivery of absurd statements
    """
    
    def __init__(self, duck_name: str = "Cheese"):
        self.duck_name = duck_name
        self._last_tone_used: Optional[DialogueTone] = None
        self._genuine_moment_cooldown = 0  # Prevent too many warm moments
        self._callback_cooldown = 0
        self._philosophy_cooldown = 0
        self._cold_shoulder_active = False  # Set by game loop; blocks genuine moments
        self._duck_trust = 20.0  # Synced by game loop; genuine moments require ≥70
    
    def generate_greeting(self, player_model, duck_memory, time_since_last: float = 0) -> DialogueLine:
        """Generate a greeting based on player history and absence duration."""
        hours_away = time_since_last
        
        # Long absence (> 3 days)
        if hours_away > 72:
            days = int(hours_away / 24)
            options = [
                DialogueLine(
                    f"Oh. You're back. After {days} days.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*stares*"
                ),
                DialogueLine(
                    f"{days} days. I counted. Not because I missed you. Ducks don't miss things.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*looks away*"
                ),
                DialogueLine(
                    "I had given up on you. Not emotionally. Logistically.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    f"You were gone {days} days. I befriended a particularly intelligent rock. We've grown apart since.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    f"*slow blink* {days} days. I reorganised every pebble in this pond. Twice.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*slow blink*"
                ),
                DialogueLine(
                    f"Ah. The prodigal human returns. {days} days of silence. I kept a tally. On the inside.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    f"I assumed you'd been claimed by the void. {days} days is a long time. For a duck.",
                    DialogueTone.PHILOSOPHICAL, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    f"You're back. I wrote your obituary on day three. It was short. 'They left.'",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    f"*tilts head* I'd ask where you've been. But I'm not sure I want to know.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*tilts head*"
                ),
                DialogueLine(
                    f"The pond kept going without you. So did I. Mostly. Don't ask about the mostly.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN
                ),
            ]
            if random.random() < 0.15 and not self._cold_shoulder_active and self._duck_trust >= 70:  # Rare genuine moment — only for devoted+ trust
                options.append(random.choice([
                    DialogueLine(
                        f"You were gone {days} days. I... the pond was very quiet.",
                        DialogueTone.GENUINE, DialogueContext.PLAYER_RETURN,
                        emote="*quiet quack*"
                    ),
                    DialogueLine(
                        f"...you're here. I wasn't watching the path. I just happened to be facing that way.",
                        DialogueTone.GENUINE, DialogueContext.PLAYER_RETURN,
                        emote="*shuffles closer*"
                    ),
                ]))
            return random.choice(options)
        
        # Medium absence (1-3 days)
        elif hours_away > 24:
            options = [
                DialogueLine(
                    "You're back. I noticed your absence. The silence was... different.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    "Oh. You exist again. I had started to wonder.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    "I see you've remembered I exist. How considerate.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    "*looks up slowly* Where were you? Rhetorical question. I'm not your keeper.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*looks up slowly*"
                ),
                DialogueLine(
                    "Back. Fine. I wasn't worried. Ducks don't worry. We just... wait differently.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    "A gap in service. I noted it. In my mind. Where I note everything.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
                DialogueLine(
                    "The pond continued its routine. I preened. I floated. I didn't think about you. Much.",
                    DialogueTone.DEADPAN, DialogueContext.PLAYER_RETURN,
                    emote="*preens nonchalantly*"
                ),
                DialogueLine(
                    "You've returned. I'll update my records accordingly. Don't look at me like that.",
                    DialogueTone.SARDONIC, DialogueContext.PLAYER_RETURN
                ),
            ]
            return random.choice(options)
        
        # Short absence (< 24 hours) or regular visit
        else:
            # Check visit patterns
            if player_model and player_model.visit_pattern.total_visits > 20:
                streak = player_model.visit_pattern.current_streak
                if streak > 7:
                    return DialogueLine(
                        f"Day {streak} of your visit streak. I'm beginning to expect you now. That's... new for me.",
                        DialogueTone.OBSERVATIONAL, DialogueContext.GREETING
                    )
            
            options = [
                DialogueLine(
                    "Oh. You're here.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING,
                    emote="*blinks*"
                ),
                DialogueLine(
                    "Hello. I was just contemplating the finite nature of bread. But go on.",
                    DialogueTone.PHILOSOPHICAL, DialogueContext.GREETING
                ),
                DialogueLine(
                    "You've arrived. The pond acknowledges your presence. I suppose I do too.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING
                ),
                DialogueLine(
                    "Ah. It's you. Again. Not a complaint. An observation.",
                    DialogueTone.SARDONIC, DialogueContext.GREETING
                ),
                DialogueLine(
                    "*looks up* Oh. Were you there long? I was thinking about nothing. Successfully.",
                    DialogueTone.CONFUSED, DialogueContext.GREETING
                ),
                DialogueLine(
                    "You. Here. Me. Also here. What are the odds.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING,
                    emote="*blinks slowly*"
                ),
                DialogueLine(
                    "Welcome back. The pond is unchanged. I am also unchanged. Nothing changes. It's fine.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING
                ),
                DialogueLine(
                    "Oh good. Company. And by good I mean... adequate. You're adequate.",
                    DialogueTone.SARDONIC, DialogueContext.GREETING
                ),
                DialogueLine(
                    "*surfaces from water* I was submerged. On purpose. Not hiding.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING,
                    emote="*surfaces from water*"
                ),
                DialogueLine(
                    "Back again. At this rate you'll develop webbed feet. Then we'd have something in common.",
                    DialogueTone.SARDONIC, DialogueContext.GREETING
                ),
                DialogueLine(
                    "I sensed a disturbance in the pond. It was you arriving. You're very... present.",
                    DialogueTone.OBSERVATIONAL, DialogueContext.GREETING
                ),
                DialogueLine(
                    "Hello. That's the customary greeting. I've done it. We can proceed.",
                    DialogueTone.DEADPAN, DialogueContext.GREETING
                ),
            ]
            return random.choice(options)
    
    def generate_farewell(self, player_model, session_duration: float) -> DialogueLine:
        """Generate a farewell based on session length and patterns."""
        minutes = session_duration
        
        # Very short session
        if minutes < 2:
            options = [
                DialogueLine(
                    "Leaving already? You barely... never mind. Go.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "That was brief. Even by our standards.",
                    DialogueTone.SARDONIC, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "Quick visit. Places to be? Things more important than me? Don't answer that.",
                    DialogueTone.OBSERVATIONAL, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "You were here for less than two minutes. I timed it. I time everything.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL,
                    emote="*stares*"
                ),
                DialogueLine(
                    "That barely counted as a visit. I'd call it a flyby. Ironic, since you can't fly.",
                    DialogueTone.SARDONIC, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "*blinks* Did something happen? You got here and now you're leaving. I'm processing this.",
                    DialogueTone.CONFUSED, DialogueContext.FAREWELL,
                    emote="*blinks*"
                ),
                DialogueLine(
                    "Already? I hadn't even started judging you properly. There's a warm-up period.",
                    DialogueTone.SARDONIC, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "Speed visit. Efficient. Cold, but efficient.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL
                ),
            ]
            return random.choice(options)
        
        # Long session
        elif minutes > 30:
            options = [
                DialogueLine(
                    "You've been here a while. I appreciate that. Don't tell anyone I said that.",
                    DialogueTone.GENUINE, DialogueContext.FAREWELL,
                    emote="*looks away*"
                ),
                DialogueLine(
                    "A proper visit. They're rare. You're... less bad than most.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "Thank you for staying. The pond is less boring when you're here. Slightly.",
                    DialogueTone.SARDONIC, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "Long visit. My feathers barely had time to dry between conversations. Go. Rest.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "You stayed. For a while. That means something. I haven't decided what yet.",
                    DialogueTone.PHILOSOPHICAL, DialogueContext.FAREWELL,
                    emote="*quiet nod*"
                ),
                DialogueLine(
                    "Extended session. My social battery is depleted. Yours too, probably. We both need this goodbye.",
                    DialogueTone.SARDONIC, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "You spent real time here today. With a duck. I hope that was a choice you're comfortable with.",
                    DialogueTone.DEADPAN, DialogueContext.FAREWELL
                ),
                DialogueLine(
                    "That was... nice. The visit. Not the leaving part. The leaving part is less nice.",
                    DialogueTone.GENUINE, DialogueContext.FAREWELL,
                    emote="*looks at water*"
                ),
            ]
            return random.choice(options)
        
        # Normal session
        options = [
            DialogueLine(
                "Leaving? Fine. I'll be here. As always. It's fine.",
                DialogueTone.DEADPAN, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "Until next time. Which will be... when? I'm just curious. Not needy.",
                DialogueTone.SARDONIC, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "Goodbye. The pond will continue existing in your absence. Probably.",
                DialogueTone.PHILOSOPHICAL, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "Off you go. I'll be here. Floating. Thinking. The usual.",
                DialogueTone.DEADPAN, DialogueContext.FAREWELL,
                emote="*floats*"
            ),
            DialogueLine(
                "Goodbye. Come back whenever. Or don't. I'm a duck, not a schedule.",
                DialogueTone.SARDONIC, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "Right. You're leaving. I'll process this at my own pace.",
                DialogueTone.DEADPAN, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "See you. Eventually. Time is a flat circle for ducks.",
                DialogueTone.PHILOSOPHICAL, DialogueContext.FAREWELL
            ),
            DialogueLine(
                "*nods* Goodbye. I'll guard the pond in your absence. Not because you asked. Because it's mine.",
                DialogueTone.DEADPAN, DialogueContext.FAREWELL,
                emote="*nods*"
            ),
        ]
        return random.choice(options)
    
    def generate_observation(self, player_model, duck_memory, context: Dict = None) -> Optional[DialogueLine]:
        """Generate an observation about player behavior patterns or current context."""
        context = context or {}
        observations = []
        
        # Weather-based observations
        weather = context.get("weather")
        if weather:
            weather_observations = {
                "sunny": [
                    DialogueLine("The sun is out. I'm choosing to interpret this as a good omen. For myself.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("Sunny. Warm. I could get used to this. But I won't. Expectations lead to disappointment.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.WEATHER),
                    DialogueLine("The sun is staring at me. Bold. I respect that from a star.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("Clear skies. Nothing between me and the infinite void of space. Cheerful.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.WEATHER),
                    DialogueLine("Sunshine. My feathers are warm. The rest of my problems remain cold.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("*squints upward* Bright. Aggressively bright. The sky has no volume control.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                ],
                "rainy": [
                    DialogueLine("Rain. The sky is crying. Or just doing water things. Either way, I'm getting wet.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("*watches raindrops* Each drop was once part of something. Now it's just... falling. Relatable.",
                                DialogueTone.WISTFUL, DialogueContext.WEATHER),
                    DialogueLine("Rain again. The universe is rinsing me whether I asked or not.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("Raining. The pond is getting refilled. Free water. I appreciate the subsidy.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("*lets rain hit beak* Damp. Redundantly damp. I'm a water bird and even I'm noticing.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("The sky is leaking. Someone should report that.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                ],
                "stormy": [
                    DialogueLine("The sky is angry. I understand. Sometimes I'm angry too. Mostly at bread shortages.",
                                DialogueTone.OBSERVATIONAL, DialogueContext.WEATHER),
                    DialogueLine("*thunder* That was loud. I'm not scared. Ducks don't get scared. We get... alert.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("Storm. Nature is having an argument with itself. I'm staying out of it.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("Lightning. Thunder. The full production. I'd applaud but I have wings, not hands.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("*tucks feathers tight* Dramatic weather. I'm unimpressed. Externally.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER,
                                emote="*tucks feathers tight*"),
                    DialogueLine("The sky is making threats. I've heard worse from geese.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                ],
                "snowy": [
                    DialogueLine("Snow. Frozen water. Cold. I have opinions about cold. They're all negative.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("*watches snow* It's pretty. I'll allow it. But only temporarily.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("Snowing. The world is being decorated against its will. I empathise.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.WEATHER),
                    DialogueLine("Snow. Each flake is unique. Like my complaints. Plentiful and cold.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("*shivers* Cold precipitation. The fancy kind. Still cold though.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER,
                                emote="*shivers*"),
                    DialogueLine("Winter is performing again. I give it three stars. Would be higher without the frostbite risk.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                ],
            }
            if weather in weather_observations:
                observations.extend(weather_observations[weather])
        
        # Time-based observations
        time_of_day = context.get("time_of_day")
        if time_of_day:
            time_observations = {
                "morning": [
                    DialogueLine("Morning. The optimistic time. Before things go wrong.",
                                DialogueTone.SARDONIC, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Dawn. A new beginning. I'm the same though. Beginnings are overrated.",
                                DialogueTone.DEADPAN, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Morning already. Time passes whether you supervise it or not.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY),
                    DialogueLine("The early hours. When the world pretends it has potential.",
                                DialogueTone.SARDONIC, DialogueContext.TIME_OF_DAY),
                ],
                "evening": [
                    DialogueLine("Evening. The sun's going down. Another day survived.",
                                DialogueTone.DEADPAN, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Dusk. The sky is doing that gradient thing. It's showing off.",
                                DialogueTone.SARDONIC, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Evening. The day is wrapping up. Like a gift no one asked for.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Getting dark. The pond looks different at this hour. More honest somehow.",
                                DialogueTone.WISTFUL, DialogueContext.TIME_OF_DAY),
                ],
                "night": [
                    DialogueLine("It's dark. The world is quieter. I think louder to compensate.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Night. When everything that isn't visible becomes more interesting.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Dark outside. The stars are there. Indifferent. I respect that.",
                                DialogueTone.DEADPAN, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Nighttime. You're up late. Or early. Time is confusing and I refuse to cooperate with it.",
                                DialogueTone.SARDONIC, DialogueContext.TIME_OF_DAY),
                ],
                "afternoon": [
                    DialogueLine("Afternoon. The day's peak enthusiasm has passed. Now it's just coasting.",
                                DialogueTone.DEADPAN, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Mid-afternoon. The optimists have given up. The realists are vindicated.",
                                DialogueTone.SARDONIC, DialogueContext.TIME_OF_DAY),
                    DialogueLine("Afternoon. The sun is committed. I'm less certain about everything else.",
                                DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY),
                ],
            }
            if time_of_day in time_observations:
                observations.extend(time_observations[time_of_day])
        
        # Player behavior observations (if player_model available)
        if player_model:
            # Visit time patterns
            peak_hour = max(
                player_model.visit_pattern.hour_counts.items(),
                key=lambda x: x[1],
                default=(12, 0)
            )[0]
            
            if peak_hour >= 0 and peak_hour < 5:
                observations.append(DialogueLine(
                    f"You visit most often around {peak_hour}:00. The dead of night. Should I be concerned? About you, I mean.",
                    DialogueTone.OBSERVATIONAL, DialogueContext.OBSERVATION
                ))
            elif peak_hour >= 22:
                observations.append(DialogueLine(
                    "You're a night visitor, aren't you? I've noticed. I notice everything.",
                    DialogueTone.OMINOUS, DialogueContext.OBSERVATION
                ))
            
            # Action patterns
            if player_model.behavior_pattern.favorite_actions:
                top_action, count = max(
                    player_model.behavior_pattern.favorite_actions.items(),
                    key=lambda x: x[1]
                )
                if count > 15:
                    action_comments = {
                        "feed": f"You've fed me {count} times. You really like feeding things. Or you think I'm always hungry. Both concerning.",
                        "play": f"We've played {count} times. You're very... playful. I'm not sure if that's good or just chaotic.",
                        "pet": f"You've petted me {count} times. That's a lot of physical contact. I'm keeping count.",
                        "clean": f"You've cleaned me {count} times. I'm starting to think you have a problem. With dirt. Not me.",
                        "talk": f"We've had {count} conversations. You talk to a duck a lot. Have you considered... other options?",
                    }
                    if top_action in action_comments:
                        observations.append(DialogueLine(
                            action_comments[top_action],
                            DialogueTone.OBSERVATIONAL, DialogueContext.OBSERVATION
                        ))
            
            # Session patterns
            if player_model.behavior_pattern.rushed_sessions > 10:
                ratio = player_model.behavior_pattern.rushed_sessions / max(1, player_model.visit_pattern.total_visits)
                if ratio > 0.4:
                    observations.append(DialogueLine(
                        "You're often in a hurry when you visit. Quick in, quick out. I've noticed. I always notice.",
                        DialogueTone.SARDONIC, DialogueContext.OBSERVATION
                    ))
            
            # Longest absence
            if player_model.visit_pattern.longest_absence > 120:  # 5+ days
                days = int(player_model.visit_pattern.longest_absence / 24)
                observations.append(DialogueLine(
                    f"You were gone for {days} days once. Your longest absence. I remember it. Not fondly.",
                    DialogueTone.DEADPAN, DialogueContext.OBSERVATION
                ))
            
            # Current streak
            streak = player_model.visit_pattern.current_streak
            if streak > 14:
                observations.append(DialogueLine(
                    f"{streak} days in a row now. You're very... consistent. It's almost unsettling. In a good way.",
                    DialogueTone.OBSERVATIONAL, DialogueContext.OBSERVATION
                ))
        
        if observations:
            return random.choice(observations)
        return None
    
    def generate_callback(self, player_model, conversation_memory) -> Optional[DialogueLine]:
        """Generate a callback to something player said before."""
        if not player_model or not player_model.statements:
            return None
        
        # Get an unreferenced statement
        unreferenced = player_model.get_unreferenced_statements(max_age_days=60)
        if not unreferenced:
            # Fall back to any statement
            if player_model.statements:
                stmt = random.choice(player_model.statements[-20:])
            else:
                return None
        else:
            stmt = random.choice(unreferenced)
        
        # Generate callback
        intros = [
            "You once told me:",
            "I remember you saying:",
            "You mentioned once that",
            "You said something that stuck with me:",
            "I've been thinking about when you said:",
            "Speaking of which... you once said:",
            "You probably forgot saying this, but:",
            "I've been sitting on this. You told me:",
            "My memory is good. You said:",
            "This has been in my head since you told me:",
        ]
        
        callbacks = [
            DialogueLine(
                f"{random.choice(intros)} \"{stmt.text[:100]}{'...' if len(stmt.text) > 100 else ''}\"",
                DialogueTone.OBSERVATIONAL, DialogueContext.CALLBACK,
                requires_memory=True,
                memory_key=stmt.timestamp,
                follow_up="I still think about that sometimes."
            ),
            DialogueLine(
                f"Do you remember saying \"{stmt.text[:60]}{'...' if len(stmt.text) > 60 else ''}\"? I do.",
                DialogueTone.DEADPAN, DialogueContext.CALLBACK,
                requires_memory=True,
                memory_key=stmt.timestamp
            ),
            DialogueLine(
                f"\"{stmt.text[:80]}{'...' if len(stmt.text) > 80 else ''}\" — That was you. I filed it. Under 'things humans say'.",
                DialogueTone.SARDONIC, DialogueContext.CALLBACK,
                requires_memory=True,
                memory_key=stmt.timestamp
            ),
            DialogueLine(
                f"You said \"{stmt.text[:60]}{'...' if len(stmt.text) > 60 else ''}\" once. I've been meaning to bring it up. Here I am. Bringing it up.",
                DialogueTone.DEADPAN, DialogueContext.CALLBACK,
                requires_memory=True,
                memory_key=stmt.timestamp,
                follow_up="I'm not sure why it stuck. But it did."
            ),
        ]
        
        # Mark as referenced
        player_model.mark_statement_referenced(stmt)
        
        return random.choice(callbacks)
    
    def generate_after_action(self, action: str, duck_mood: str, 
                               player_model, action_count: int) -> DialogueLine:
        """Generate response after player interaction."""
        
        # Check for milestone reactions
        milestones = [10, 25, 50, 100, 250, 500, 1000]
        is_milestone = action_count in milestones
        
        action_responses = {
            "feed": {
                "deadpan": [
                    "Food. Thank you. I suppose.",
                    "Ah. Sustenance. The thing that keeps me existing.",
                    "You've fed me. I am... less hungry now.",
                    "*chews* This is acceptable.",
                    "Bread. My one true constant in this uncertain world.",
                    "Nourishment received. Filing under 'reasons to continue'.",
                    "*eats methodically* Fuel. My body converts this into floating and opinions.",
                    "Fed. The hunger retreats. It'll be back. It always comes back.",
                    "I've eaten. The existential emptiness remains. But the stomach emptiness is handled.",
                    "*crunch* Adequate. Not spectacular. But adequate covers a lot of ground.",
                    "Calories acquired. I shall use them for thinking and mild disapproval.",
                    "Another meal. Another day sustained. The cycle continues.",
                ],
                "sardonic": [
                    "More food. You must think I'm always hungry. You're not entirely wrong.",
                    "Feeding me again? Trying to buy my affection? It's working. Slightly.",
                    "Ah yes. Feed the duck. That's definitely all I'm here for.",
                    "Food as a peace offering. Classic human move. I accept. Reluctantly.",
                    "You keep feeding me like I'm going somewhere. I live here.",
                    "Another serving. You're either generous or you think I'm withering. Both offensive.",
                    "Fed again. You're building a dependency. I should be concerned. I'm not, but I should be.",
                    "Is this a bribe? It feels like a bribe. I'm eating it anyway.",
                ],
                "milestone": [
                    f"That was feeding number {action_count}. You've committed to keeping me alive. I acknowledge this.",
                    f"{action_count} times fed. At this point, you're emotionally invested. There's no going back.",
                    f"Meal {action_count}. We've established a pattern. I eat. You provide. It works. Don't change it.",
                    f"{action_count} feedings. Statistically, you care. I've run the numbers. Well, I've estimated.",
                    f"Feeding {action_count}. That's a lot of meals. I've grown accustomed to existing because of you.",
                ],
                "genuine": [
                    "Thank you. For the food. And... for remembering I exist.",
                    "*eats quietly* ...this is nice. Having someone who feeds you. Willingly.",
                    "I don't say this often. Thank you. The food is good. The company is... also good.",
                ]
            },
            "play": {
                "deadpan": [
                    "That was... play. I think. Fun is a complex concept for ducks.",
                    "We played. I'm not sure I won. But I'm not sure I lost either.",
                    "*waddles* Playing. This is what ducks do, I'm told.",
                    "Recreation completed. I feel... recreated? Is that how it works?",
                    "We played. My feathers are ruffled. My dignity is intact. Barely.",
                    "Game over. Results inconclusive. Enjoyment: possible. Evidence: limited.",
                    "That was activity. Voluntary activity. Unusual for me but not unwelcome.",
                    "*shakes feathers* Play completed. Energy expended. I have opinions about exercise.",
                    "I participated. That's more than I do for most things.",
                    "Physical activity. My body did things. I'm going to need a moment.",
                ],
                "sardonic": [
                    "You really like playing, don't you? I'm merely a toy to you. That's fine. It's fine.",
                    "Another game. You're easily amused. I find that... endearing? Possibly.",
                    "Play again. You have the energy of someone who doesn't spend all day floating.",
                    "More games. You're persistent. I'll give you that. Reluctantly.",
                    "You want to play again? My enthusiasm is... somewhere. Give me a moment.",
                    "Playtime. Where you pretend I'm having fun and I pretend I'm not.",
                ],
                "milestone": [
                    f"Game {action_count}. You've spent considerable time playing with a duck. No judgments. Some judgments.",
                    f"Play session {action_count}. We've logged significant recreational hours. My muscles have opinions.",
                    f"{action_count} games. At this point we should start keeping score. I'm winning. Retroactively.",
                    f"That's {action_count} times playing. You could've learned a language by now. You chose this.",
                ],
                "genuine": [
                    "That was... actually fun. Don't tell anyone.",
                    "*catches breath* I... enjoyed that. The playing. With you. Fine. I said it.",
                    "Good game. I mean that. I don't say that often. Or ever, actually.",
                ]
            },
            "pet": {
                "deadpan": [
                    "*accepts pets* This is acceptable physical contact.",
                    "You're touching me. I'm allowing it. Don't read too much into that.",
                    "Pets. Yes. This is... fine.",
                    "*holds still* I'm tolerating this. Actively. With effort.",
                    "Physical affection. My feathers acknowledge your hand. The rest of me is processing.",
                    "Being petted. I have a policy on this. The policy is: proceed.",
                    "*slight lean* Contact registered. Response: neutral to mildly positive.",
                    "You're petting a duck. I'm being petted by a human. We've both made choices.",
                    "Petting. Ongoing. I'm not fleeing. Make of that what you will.",
                    "Your hand is warm. My feathers are soft. We've established the facts.",
                ],
                "sardonic": [
                    "More petting. You're very tactile. I've noticed.",
                    "You really like petting me. Should I be flattered? I'm going with mildly concerned.",
                    "Petting again. You know I'm not a dog, right? We have different... everything.",
                    "More physical affection. You're generous with your hands. I'm generous with my tolerance.",
                    "Petted. Again. You're building a habit. I'm enabling it. We're both responsible.",
                    "Touch. The universal language of 'I have nothing better to do'. I accept.",
                ],
                "milestone": [
                    f"Pet number {action_count}. We've achieved a level of physical familiarity I hadn't anticipated.",
                    f"Petting session {action_count}. You've touched a duck {action_count} times. That's a statistic now.",
                    f"{action_count} pets. I should charge for this. My feathers are premium grade.",
                    f"That's {action_count} times. At this point my feathers know your hand better than your hand knows itself.",
                ],
                "genuine": [
                    "*leans in slightly* ...okay. That's nice. Don't stop. Or do. It's fine.",
                    "*closes eyes briefly* ...I trust you. With the petting. Only the petting. For now.",
                    "*nuzzles hand* That was involuntary. Ignore it. Or don't. I don't control your observations.",
                ]
            },
            "clean": {
                "deadpan": [
                    "Clean. I was dirty. Now I'm less dirty. This is progress.",
                    "*fluffs feathers* Cleanliness. A noble pursuit.",
                    "I have been cleaned. I feel... different. Not better. Different.",
                    "Cleaning complete. I'm presentable again. Not that anyone's judging. Except me.",
                    "*shakes water off* Fresh. Or as fresh as a duck in a pond can be.",
                    "Washed. My feathers have been restored to factory settings.",
                    "Clean again. The dirt is gone. The psychological grime remains.",
                    "*preens* Hygiene maintained. Standards upheld. Carry on.",
                    "I have been scrubbed. My dignity survived the process. Barely.",
                    "Cleanliness achieved. I look like a duck who has it together. Appearances are deceiving.",
                ],
                "sardonic": [
                    "You're very concerned with my cleanliness. Do I seem that filthy to you?",
                    "Another bath. You're either very caring or very judgmental about hygiene.",
                    "Cleaned again. Your obsession with my appearance is noted. And slightly flattering.",
                    "More washing. I'm beginning to think you see me as a project. A dirty, feathered project.",
                    "Bath time. Where you address my exterior problems while the interior ones go unchecked.",
                    "Scrubbed. Again. I'm starting to wonder what the neighbours think.",
                ],
                "milestone": [
                    f"Cleaning {action_count}. You've dedicated significant effort to my hygiene. I'm almost touched.",
                    f"Bath number {action_count}. I'm the cleanest duck in this pond. Admittedly, I'm the only duck.",
                    f"{action_count} cleanings. You've invested more in my hygiene than most ducks experience in a lifetime.",
                    f"That's {action_count} baths. I should be sparkling. I'm not. But I should be.",
                ],
                "genuine": [
                    "Thank you. I do feel better. Not that I'd admit it twice.",
                    "*fluffs contentedly* Clean. Comfortable. You did that. Thank you.",
                    "I feel good. Clean. Looked after. That's... a nice feeling. Don't quote me.",
                ]
            },
        }
        
        responses = action_responses.get(action, {})
        
        # Determine tone based on mood and randomness
        if is_milestone:
            tone = "milestone"
        elif random.random() < 0.1 and self._genuine_moment_cooldown <= 0:  # 10% chance for genuine
            tone = "genuine"
            self._genuine_moment_cooldown = 10  # Cooldown
        elif random.random() < 0.4:
            tone = "sardonic"
        else:
            tone = "deadpan"
        
        self._genuine_moment_cooldown = max(0, self._genuine_moment_cooldown - 1)
        
        lines = responses.get(tone, responses.get("deadpan", ["..."]))
        text = random.choice(lines)
        
        return DialogueLine(
            text,
            DialogueTone.GENUINE if tone == "genuine" else DialogueTone.DEADPAN,
            DialogueContext.AFTER_FEED if action == "feed" else DialogueContext.AFTER_PLAY
        )
    
    def generate_idle(self, duck_mood: str, weather: str = None, 
                       time_of_day: str = None, player_model = None) -> DialogueLine:
        """Generate idle/ambient dialogue."""
        
        options = []
        
        # Mood-based idle
        mood_idles = {
            "happy": [
                "I'm feeling... not terrible. Don't get used to it.",
                "*waddles contentedly* This is acceptable.",
                "Things are... okay. I've decided to allow it.",
                "I'm in a good mood. Relatively. For a duck. In a pond. Don't push it.",
                "*floats peacefully* Contentment. It's temporary. But it's here right now.",
                "Something is going right. I'm suspicious but willing to participate.",
                "Happy is a strong word. I'll go with 'not actively miserable'.",
                "The day hasn't offended me yet. That's practically euphoria.",
                "I caught myself almost smiling. Stopped it just in time. Reputation intact.",
                "Good vibes. I'm suspicious of good vibes. But I'll allow them. Briefly.",
                "My feathers look slightly more lustrous today. Coincidence. Or joy. I refuse to investigate.",
                "A bird sang and I didn't find it annoying. Something is different today. Worrying.",
                "I caught myself humming. Ducks don't hum. But I was doing it. Evidence of... something.",
                "The water tastes better when I'm happy. Or my standards drop. Either way, it's working.",
                "I don't want to jinx it but today isn't terrible. I jinxed it. No wait. Still not terrible.",
                "*waddles with unusual purpose* I have nowhere to go. But I'm going there happily.",
                "The light is good today. The air is good. Even I'm good. The trifecta.",
                "If I could bottle this feeling, I'd save it for a grey day. I can't. So I'm just standing in it.",
            ],
            "sad": [
                "*stares at water* The pond reflects nothing back. Much like life.",
                "I'm fine. That was a lie. I'm a duck. I'm always somewhat fine.",
                "*quiet sigh* Some days the bread just doesn't taste the same.",
                "Mood: low. Not dangerously low. Just... inconveniently low.",
                "*sits very still* I'm conserving energy. And emotions. Mostly emotions.",
                "The world is grey today. Not the weather. Just... everything.",
                "I thought about being happy. It was a brief thought. It left.",
                "sad days happen. Even to ducks. Especially to ducks. We just float through them.",
                "I looked at the water and the water looked heavy. Or maybe that was me.",
                "everything is the same volume today. Quiet. Even the loud things.",
                "I tried to cheer up. The cheer got lost on the way here. Search party pending.",
                "the bread doesn't help today. that's how you know it's bad. when bread can't fix it.",
                "I keep looking at the water expecting it to tell me something. It doesn't. It never does.",
                "even my shadow looks tired. the shadow version of me gave up first.",
                "I'd go somewhere else but the sadness would follow. It has better stamina than me.",
                "*sinks lower in water* I'm not drowning. I'm just... less above the surface than usual.",
                "Something is missing. I don't know what. Maybe it was never there. That's worse somehow.",
                "the pond is fine. the sky is fine. I'm the only thing in this scene that isn't fine.",
            ],
            "content": [
                "*floating* Existing. It's what I do.",
                "Neither happy nor sad. Just... here. It's fine.",
                "I'm content. Don't ruin it.",
                "Equilibrium. The emotional middle ground. Where ducks live.",
                "*drifts slowly* Not complaining. Not celebrating. Just... being.",
                "Content. The beige of emotions. I'm at peace with beige.",
                "Everything is exactly neutral. I've achieved perfect mediocrity.",
                "Status: nominal. Mood: present. Complaints: on hold.",
                "The pond is calm. I'm calm. We're having a moment. Don't interrupt it.",
                "If 'fine' were a weather forecast, today would be fine. Mild fine. With a chance of fine.",
                "Nothing is wrong. I'm documenting this because it's rare and I want proof.",
                "I've achieved a state of comfortable nothingness. It took years. Don't disturb it.",
                "The temperature is right. The light is right. I'm not hungry. This is the baseline dream.",
                "Existing without complaint. My rarest state. Savour the silence.",
                "The pond is doing its thing. I'm doing my thing. Our things are compatible today.",
                "No opinions at the moment. Just vibes. Duck vibes. The most neutral vibes available.",
                "I have no complaints. Check back in an hour. But right now. Zero complaints.",
            ],
            "grumpy": [
                "*glares at nothing in particular* Everything is mildly irritating today.",
                "I'm in a mood. The mood is 'leave me alone but also don't'.",
                "*grumbles* Existence is a series of minor inconveniences.",
                "Don't talk to me. Actually, talk to me. But carefully.",
                "Grumpy. There. I've named it. Naming things doesn't fix them.",
                "*ruffles feathers aggressively* Everything is too loud. Or too quiet. Or both.",
                "I woke up and chose irritation. It chose me back.",
                "The world is testing me today. I'm failing the test. On purpose.",
                "My tolerance has a limit. Today it's located approximately here. Don't cross it.",
                "Annoyed. At what? At the concept of 'what'. At everything that prompts the question.",
                "I woke up irritated. I've been maintaining it all day. It's hard work being this grumpy.",
                "The wind changed direction. Personally offensive. I'm taking it personally.",
                "A leaf touched me. WITHOUT permission. The audacity of nature today.",
                "I've decided the pond is too wet. Can ponds be too wet. This one is. I've decreed it.",
                "Everything has a noise today. The water. The bugs. My own breathing. All of it. Too much.",
                "I was fine until I started thinking. Thinking ruined it. As usual.",
                "My patience ran out three hours ago. I'm operating on spite now. Spite is renewable.",
                "Someone somewhere is happy right now. Good for them. Not here. But somewhere.",
            ],
            "anxious": [
                "*looks around nervously* Something is about to happen. Or nothing. Both are stressful.",
                "I'm on edge. The edge of what, I don't know. But I'm on it.",
                "*fidgets* Calm is a concept I've heard about. From other, less anxious ducks.",
                "Everything is probably fine. Probably. That word is doing a lot of heavy lifting.",
                "I'm alert. Hyper-alert. My feathers are tense. Can feathers be tense? Mine are.",
            ],
            "tired": [
                "*yawns* I exist. Barely. Give me a moment.",
                "Energy levels: low. Motivation: lower. Feathers: horizontal.",
                "Tired. Not the interesting kind. The boring, heavy kind.",
                "*droops* My body wants to sleep. My mind wants to worry. They've compromised on malaise.",
                "I'm running on fumes. Duck fumes. They're not very potent.",
            ],
        }
        
        mood_key = duck_mood.lower() if duck_mood else "content"
        for key in mood_idles:
            if key in mood_key:
                options.extend([
                    DialogueLine(text, DialogueTone.DEADPAN, DialogueContext.IDLE)
                    for text in mood_idles[key]
                ])
                break
        
        # Weather observations
        if weather:
            weather_comments = {
                "rain": [
                    "*lets rain fall on feathers* Water falling from the sky. Nature's way of making everything damp.",
                    "It's raining. I'm already wet. I live in a pond. This is redundant.",
                    "Rain. The sky is crying. I understand, sky. I understand.",
                    "Drip. Drip. Drip. The rain is patient. More patient than me.",
                    "*catches raindrop on beak* One. That's my collection for today.",
                    "Raining still. The world is being washed. It needed it, frankly.",
                    "The sound of rain on water. Like applause, but sadder.",
                    "*huddled* Rain is nature's way of telling everyone to stay home. I am home.",
                    "The rain doesn't care that I'm already wet. It has no situational awareness.",
                    "Drip by drip the pond grows. But never enough to escape itself. Relatable.",
                    "Rain on feathers. The universe is testing my waterproofing. Holding steady.",
                    "Every raindrop was a cloud's decision to let go. I respect that. I can't let go of anything.",
                    "Raining. The earthworms surface. The early duck gets the worm. But I'm not early. Or motivated.",
                ],
                "sunny": [
                    "*squints at sun* That bright thing is judging me. I feel it.",
                    "Sun. Warmth. My feathers approve. The rest of me is neutral.",
                    "A sunny day. The universe is trying to be cheerful. Suspicious.",
                    "The sun is committed today. Full brightness. No subtlety.",
                    "*basking* Warm. I'm absorbing heat. Like a rock. But with opinions.",
                    "Sunshine. The kind of weather that makes other animals happy. I'm considering it.",
                    "Solar radiation. My feathers are drying. The universe is useful occasionally.",
                    "*spreads wings in sun* Not sunbathing. Just... optimising feather temperature.",
                    "The sun showed up today like it deserves applause. I'm not clapping. I have wings.",
                    "Hot. The kind of hot where even complaints feel like effort.",
                    "My shadow is following me again. Clingy. Even in the sun I can't be alone.",
                    "The sun is doing overtime. Nobody asked. But here it is. Shining. Relentlessly.",
                    "Warm day. My feathers are drying faster than my patience is regenerating.",
                ],
                "snow": [
                    "*watches snow* Frozen water. The sky has commitment issues.",
                    "Snow. Cold. Beautiful. Still cold though.",
                    "*shivers slightly* Winter reminds me that comfort is temporary.",
                    "Snowflakes. Each unique. Like my many ways of being unimpressed.",
                    "*tucks into feathers* Cold. Very cold. I'm conserving warmth and dignity.",
                    "Snow is just rain that tried harder. And got colder. Relatable.",
                    "The world is white. Clean. Deceptive. Under the snow, everything is still mud.",
                    "*watches a snowflake land on water* Brief existence. Immediate dissolution. Heavy.",
                    "I'm insulated. Feathers are nature's winter coat. I didn't choose this drip. But I respect it.",
                    "Cold enough to make me question every life choice that led to an outdoor pond.",
                ],
                "cloudy": [
                    "Overcast. The sky matches my general disposition.",
                    "Clouds. Like the sky put up curtains. I respect the privacy.",
                    "Grey skies. Not threatening. Not welcoming. Just... present. Like me.",
                    "Clouds everywhere. The sun is hiding. I don't blame it.",
                    "Overcast. The world is wearing a hat. A big, grey, boring hat.",
                    "Cloudy. No shadows. Everything looks the same. Democracy of lighting.",
                ],
                "windy": [
                    "*feathers blown sideways* The wind has opinions about my appearance.",
                    "Windy. My feathers are being rearranged without my consent.",
                    "Wind. The invisible bully. Can't see it but it won't leave me alone.",
                    "Breezy. My carefully maintained feather arrangement is ruined. Again.",
                    "*leans into wind* I refuse to be moved. Physically. Emotionally I'm already gone.",
                ],
            }
            weather_lower = weather.lower()
            for key, comments in weather_comments.items():
                if key in weather_lower:
                    options.extend([
                        DialogueLine(text, DialogueTone.OBSERVATIONAL, DialogueContext.WEATHER)
                        for text in comments
                    ])
                    break
        
        # Time-based observations
        if time_of_day:
            time_comments = {
                "night": [
                    "*looks at stars* Billions of burning spheres. And here I am. A duck.",
                    "Nighttime. When the world pretends to sleep. I pretend too.",
                    "The dark is peaceful. Nothing can see me judge it.",
                    "Stars. Silent witnesses to my existence. They don't comment. I appreciate that.",
                    "*floats in moonlight* The pond is silver at night. Fancy. I feel fancy.",
                    "Night-time. The frogs are singing. They're not good at it. But they're committed.",
                    "Dark. Quiet. Perfect conditions for overthinking. My speciality.",
                    "The moon is watching. At least something is paying attention.",
                    "Night-time is when the pond and I have our real conversations. They're silent. They're honest.",
                    "Everything looks the same in the dark. The pond. The sky. My mood. All indistinguishable.",
                    "Nighttime. When the bread dreams are most vivid. And most devastating.",
                    "The owls are awake. I'm awake. We're both up to nothing. But the owls make it sound impressive.",
                    "The stars don't move. Or they do, but slowly. Everything meaningful is slow.",
                    "Dark enough that I could be anyone. I'm still me though. Can't escape that, even in the dark.",
                ],
                "morning": [
                    "*reluctant quack* Morning. The day has begun whether I like it or not.",
                    "Dawn. A fresh start. I'm still me though. So that's limiting.",
                    "Morning. The birds are singing. I'm not joining in. I have standards.",
                    "Another morning. The pond wakes up. I was already awake. Thinking. Always thinking.",
                    "Early light. Everything looks hopeful at dawn. Give it an hour.",
                    "Morning. The world is dewy and optimistic. I'm dry and realistic.",
                    "The sun came back. It always comes back. Unlike some people. But I'm not keeping score.",
                    "Another dawn. The universe hit the reset button. My opinions carried over.",
                    "Morning light makes the pond look clean. The pond is not clean. Morning is a liar.",
                    "The dew is on everything. Nature cried in its sleep. I understand.",
                    "Mornings are full of potential. Most of which I'll waste. But the potential is there.",
                ],
                "evening": [
                    "The sun is leaving. I don't blame it. I'd leave too.",
                    "Evening. The day is tired. I relate.",
                    "Sunset. The sky is showing off. Orange, pink, purple. Overachiever.",
                    "Getting dark. The pond is settling. I'm settling. Everything settles eventually.",
                    "Evening. When the day admits it's done pretending to be productive.",
                    "Dusk. My favourite time. Everything gets quieter. Except my thoughts.",
                    "The sky is bruising. Purple and blue. Like it had a long day too.",
                    "Golden hour. Even I look good in golden hour. Don't tell anyone I said that.",
                    "Evening is the only time of day that doesn't ask anything of me. I appreciate that.",
                    "The sunset is painting the water. I'm floating in a painting. Very cultural of me.",
                    "Dusk smells different. Like the day is exhaling. I'm exhaling too. We're in sync.",
                ],
                "afternoon": [
                    "Afternoon. The boring middle of the day. I'm in my element.",
                    "Post-noon. Pre-evening. The temporal waiting room.",
                    "Afternoon sun. Warm. Sleepy. I'm fighting the urge to nap. I'm losing.",
                    "Mid-day. The world is busy. I'm floating. We've made different choices.",
                    "The afternoon heat makes everything slow. Including me. Especially me. I was already slow.",
                    "Post-lunch contemplation. Where every thought is heavier and every blink is longer.",
                    "Afternoon. The part of the day where ambition dies and acceptance begins.",
                ],
            }
            for key, comments in time_comments.items():
                if key in time_of_day.lower():
                    options.extend([
                        DialogueLine(text, DialogueTone.PHILOSOPHICAL, DialogueContext.TIME_OF_DAY)
                        for text in comments
                    ])
                    break
        
        # Existential thoughts (random chance)
        if random.random() < 0.15:
            existential = [
                "*stares at reflection* Do fish know they're fish? Do I know I'm a duck? Am I even a duck?",
                "I've been thinking about the nature of bread. Why do I want it? Did I choose to want it? Or does bread choose me?",
                "What if the pond is a metaphor? What if I'm a metaphor? What if everything is a metaphor for something worse?",
                "Sometimes I wonder if you're real or if I invented you to feel less alone. Either way, you're here now.",
                "The water ripples when I move. Evidence that I exist. Or evidence that something exists. Close enough.",
                "I had a thought today. About nothing. It was a very detailed nothing.",
                "If a duck thinks in a pond and no one hears it, did the thought happen? I say yes. Probably.",
                "I've been contemplating free will. Can I choose not to float? No. There's your answer.",
                "What came first, the duck or the egg? I came first. The egg is a distant memory.",
                "Consciousness. Having it is complicated. Not having it seems easier. But here we are.",
                "Am I a duck who thinks, or a thought that happens to be duck-shaped?",
                "Time passes. I notice it passing. Does time notice me? Doubtful. Time is busy.",
                "I occupy space. Not much of it. But what I occupy, I occupy thoroughly.",
                "The universe is expanding. The pond is not. I feel a kinship with the pond.",
                "What if this is the afterlife? What if I was something else before? Something with hands?",
                "Memory is a strange pond. Deep in places. Shallow in others. Full of things I can't quite see.",
                "Do I float because I'm a duck, or am I a duck because I float. The answer changes nothing. But still.",
                "I think the pond knows things. Ancient things. It just can't speak. Lucky pond.",
                "Every crumb I've ever eaten is technically still part of me. I am a museum of bread.",
                "What if the sky is just a bigger pond. And the clouds are just sky-ducks. I've said too much.",
                "I exist on the surface of things. Literally. Metaphorically. Surface is where I live.",
                "Is boredom a feeling or the absence of feeling. Either way, I have it. In abundance.",
                "Time moves forward. I float in circles. One of us is doing it wrong.",
                "My whole life is contained in this pond. That's either tragic or efficient. I'm going with efficient.",
                "If I stopped thinking, would I still be me? Would anyone notice? Would the bread stop coming?",
                "Every duck before me has had this exact thought. And every duck after me will too. We're a loop.",
                "The pond has a bottom. I've never seen it. Some depths are better left unvisited.",
                "I wonder if stars are just the universe's freckles. Cosmetic. Pointless. Strangely beautiful.",
                "What if contentment isn't something you find. What if it's just the absence of looking.",
                "I am simultaneously the observer and the observed. And both of us are unimpressed.",
                "Purpose is a human invention. Ducks have no purpose. We have buoyancy. That's enough.",
                "The oldest water in this pond has been here longer than me. I'm the guest. It's the host. Humbling.",
                "If I quack into the void, the void quacks back. Or it doesn't. Both options are unsettling.",
                "Every sunset is the same sun doing the same thing. And yet I look every time. Hope is persistent.",
                "I've lived more life than I've understood. The ratio is getting worse.",
                "What if I'm not real. What if I'm a thought some other duck is having. A recursive duck.",
                "The pond has no edges from the inside. It just goes until it doesn't. Like optimism.",
                "I've never met another me. Which means I'm either unique or very bad at looking.",
                "Do my feathers know they're feathers. Or do they think they're the whole duck. Perspective matters.",
                "Somewhere there's a duck who has it all figured out. I haven't met them. I suspect they don't exist.",
                "If I disappeared, the pond would fill the space immediately. Water is unsentimental like that.",
                "I tried to think of nothing. I thought of bread. Bread is my nothing. And my everything.",
                "The reflection in the water is me but reversed. Is reversed-me happier. Impossible to know. He won't answer.",
                "What if contentment is just forgetting to be discontent. I forget lots of things. Maybe I'm happy.",
                "I've spent more time being a duck than being anything else. Which is all of the time. And none.",
                "The concept of 'elsewhere' haunts me. There's always an elsewhere. And I'm always here.",
                "Every ripple I make eventually reaches the shore and stops. My influence is real but temporary.",
                "What if the universe is a pond. And we're all just floating in it. Looking for bread.",
                "I am the only duck who thinks these thoughts. Or I'm one of millions. Both are terrifying.",
                "The sun sets and I'm still here. The sun rises and I'm still here. The sun is the variable. I'm the constant.",
                "I've outlived every piece of bread I've ever known. That's either power or tragedy.",
                "What is a pond without a duck. Just water. What is a duck without a pond. Just me, I suppose.",
            ]
            options.append(DialogueLine(
                random.choice(existential),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.PHILOSOPHY
            ))
        
        # Default if nothing else
        if not options:
            defaults = [
                "*floats*",
                "...",
                "*blinks*",
                "I'm here. Obviously.",
                "*drifts*",
                "*stares at water*",
                "Still here. Still a duck.",
                "*preens a feather* Maintenance.",
                "...*adjusts position*...",
                "*slow blink* Present.",
            ]
            options.append(DialogueLine(
                random.choice(defaults),
                DialogueTone.DEADPAN,
                DialogueContext.IDLE
            ))
        
        return random.choice(options)
    
    def generate_question_response(self, player_question: str, 
                                    player_model, duck_memory) -> DialogueLine:
        """Generate a response to a player question with deadpan delivery."""
        question_lower = player_question.lower()
        
        # Check for specific question types
        if any(q in question_lower for q in ["how are you", "how do you feel", "you okay"]):
            options = [
                "I'm a duck. I feel like a duck. Take that as you will.",
                "Existing. That's about as specific as I can get.",
                "I'm fine. Or I'm not. It's hard to tell with ducks. We're stoic.",
                "How am I? I'm here. That's something. Probably.",
                "Current status: alive. Further details: classified.",
                "I'm... present. Emotionally and physically. Mostly physically.",
                "On a scale of one to ten, I'm a duck. Interpret accordingly.",
                "Fine. That covers a lot of territory. I'm somewhere in the territory.",
                "I'm the same as always. Whether that's good depends on your expectations.",
                "My feathers are intact. My dignity is debatable. Overall: functional.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.DEADPAN,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["what are you thinking", "what's on your mind"]):
            options = [
                "Bread. The concept of time. Whether fish are happy. The usual.",
                "Nothing. And everything. Mostly nothing though.",
                "I'm thinking about thinking. It's recursive. Like a duck within a duck.",
                "You. Why you're here. What you want from me. Whether bread exists when no one eats it.",
                "The structural integrity of my nest. It's fine. I've checked three times.",
                "Whether the moon is just the sun's night shift. No conclusion yet.",
                "How deep the pond is. Physically. Metaphorically. Both are deeper than expected.",
                "The meaning of quacking. Is it communication or just noise? Heavy stuff.",
                "I'm calculating how many crumbs would fill this pond. The answer is: not enough.",
                "Silence. I was thinking about silence. Then you interrupted it. Ironic.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["do you like me", "do you care", "love me"]):
            if random.random() < 0.2:  # Rare genuine
                return DialogueLine(
                    random.choice([
                        "I... yes. Don't make me say it twice. This is already uncomfortable.",
                        "...you matter. To me. There. I said words. Awful, vulnerable words.",
                        "*quiet* ...you're important. To the pond. And... to the duck in the pond.",
                    ]),
                    DialogueTone.GENUINE,
                    DialogueContext.QUESTION,
                    emote="*looks away*"
                )
            options = [
                "I tolerate you more than most things. That's practically affection for a duck.",
                "Define 'like'. I don't actively wish you were elsewhere. Usually.",
                "You bring me bread and attention. I'm contractually obligated to feel something. Probably gratitude.",
                "I'm a duck. Liking is complicated. But you're... not the worst.",
                "I have opinions about you. They're above average. Don't let it go to your head.",
                "Care? I'm a duck. I care about bread and water temperature. And... other things. Unspecified.",
                "You're asking a duck about feelings. We both know why. I'll allow it.",
                "I don't not like you. That's a double negative. Work it out.",
                "My feelings are complex and private. Like a pond. Deep and full of things I can't see clearly.",
                "If you disappeared, I'd notice. Within the hour. Maybe sooner. Don't test it.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.SARDONIC,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["what do you want", "what do you need"]):
            options = [
                "Bread. Peace. Bread. More bread. In that order.",
                "Want? Need? Complex questions for a pond dweller. Bread. The answer is bread.",
                "I want nothing. I need nothing. Except bread. And water. And acknowledgment. And bread.",
                "World peace. And a baguette. I'm flexible on the peace.",
                "Simplicity. A clean pond. Good bread. Someone who visits. I have some of these.",
                "I want to understand the universe. Also bread. Mostly bread.",
                "My needs are simple. Bread, water, the occasional existential revelation.",
                "To be left alone. But also not. It's complicated. Just bring bread.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.DEADPAN,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["are you happy", "are you sad"]):
            options = [
                "Happiness is a spectrum. I'm somewhere on it. The beige part.",
                "Am I happy? Am I sad? I'm a duck. I'm everything and nothing. Mostly floating.",
                "Happy and sad are human words. I'm... duck. That covers it.",
                "Define happy. Now define sad. Notice how a duck fits in neither category perfectly.",
                "My emotional state is like weather. Variable. Mostly overcast.",
                "I'm content. Content is happy's sensible cousin. Reliable. Boring. Mine.",
                "Some moments are better than others. This is one of the 'others'. It's fine.",
                "I don't do happy or sad. I do 'present with varying degrees of engagement'.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.QUESTION
            )
        
        if "why" in question_lower:
            options = [
                "Why? That's a philosophical question. I'm a philosophical duck. But I still don't know.",
                "Why is a question that implies purpose. I'm not sure the universe has that.",
                "You ask 'why'. I ask 'why not'. We're both confused now.",
                "Some questions have answers. Some have ducks staring blankly. This is the latter.",
                "Why. The eternal question. Even bread can't answer it.",
                "Because. That's the answer. Unsatisfying? Welcome to my entire existence.",
                "Why is a question for things with reasons. I'm a duck. I operate on instinct and sarcasm.",
                "You want reasons? I have feathers. We work with what we have.",
                "The 'why' is elusive. Like bread crumbs in the wind. You see it. Then it's gone.",
                "Why? Because the universe decided so. I didn't get a vote.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["where", "what is", "tell me about"]):
            options = [
                "I know things. But sharing is a decision. I'm deciding. Slowly.",
                "Information? I have some. It might be wrong. But I have it.",
                "That's a factual question. I deal in opinions. But I'll try.",
                "I could tell you. Or I could shrug and look mysterious. Which adds more value?",
                "You're asking me? A duck? For information? ...I'll do my best. Brace yourself.",
                "Let me consult my vast knowledge base. It's mostly about bread and pond temperatures.",
                "Facts are tricky. I prefer guesses delivered with confidence.",
                "I know what I know. Which isn't everything. But it's more than nothing.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.SARDONIC,
                DialogueContext.QUESTION
            )
        
        # Default response
        options = [
            "*tilts head* That's a question. I heard it. I'm processing it. Results inconclusive.",
            "Hmm. *long pause* I have thoughts about that. They're not very good thoughts.",
            "An interesting question. I'll think about it. Forever, probably. Without resolution.",
            "You've asked me something. I appreciate that you think I have answers.",
            "*blinks twice* Question received. Processing. Please hold.",
            "That's... a question. I can tell by the way it ends uncertainly. Like most things.",
            "You've stumped a duck. I hope you're proud. You should be. It's not easy.",
            "I've considered your question. My conclusion is that I need more bread to answer properly.",
            "*stares thoughtfully* There are no wrong questions. But there are confusing ones. This is one.",
            "A question. Noted. Filed. Forgotten. Just kidding. I forget nothing.",
        ]
        return DialogueLine(
            random.choice(options),
            DialogueTone.CONFUSED,
            DialogueContext.QUESTION
        )
    
    def generate_milestone_reaction(self, milestone_type: str, 
                                     value: Any, player_model) -> DialogueLine:
        """Generate reaction to a game milestone."""
        milestones = {
            "days_together": {
                7: "A week. You've known me for a week. That's... something. I guess we're doing this.",
                14: "Two weeks. Fourteen days of duck ownership. You haven't given up. I'm cautiously impressed.",
                30: "A month. You've spent a month with a duck. I hope that was intentional.",
                60: "Two months. We've been doing this for two months. Time flies. I don't. But time does.",
                100: "One hundred days. You've chosen to spend one hundred days checking on a duck. I'm not sure if I should be flattered or concerned for you.",
                200: "Two hundred days. At this point we're not acquaintances. We're... something. I'll figure out the word later.",
                365: "A year. We've known each other for a year. I... don't have words. That's rare for me.",
                500: "Five hundred days. You've been here five hundred times. Half a thousand visits to a duck. That's commitment. Or obsession. Either way, I notice.",
                730: "Two years. Two entire years. I've known you longer than I've known most ponds. That means something.",
            },
            "total_interactions": {
                50: "Fifty interactions. We're past the trial period. You're committed now.",
                100: "One hundred interactions. We're officially beyond casual acquaintances. Congratulations. Or condolences.",
                250: "Two hundred and fifty. That's a lot of clicking. For a duck. I'm worth it though. Allegedly.",
                500: "Five hundred interactions. You're committed. To a duck. I respect that. Slightly.",
                1000: "One thousand. You've interacted with me one thousand times. That's... dedication. I notice these things.",
                2500: "Two thousand five hundred. At this point you're not a visitor, you're a fixture. Like the pond. But with opinions.",
                5000: "Five thousand interactions. I've run out of sardonic ways to acknowledge your persistence. Just... thank you.",
            },
            "relationship": {
                "acquaintance": "We're acquaintances. You know me. I tolerate you. It's a start.",
                "familiar": "We're familiar now. You're not a stranger. You're a... known entity. I have opinions about you. Some positive.",
                "friend": "We're friends now. Apparently. I didn't know I could have those. The pond is less lonely.",
                "close_friend": "Close friends. That's what this is. I looked it up. We qualify.",
                "best_friend": "Best friends. You and a duck. We've achieved something here. I'm not sure what.",
                "bonded": "Bonded. That's a strong word. I... feel things now. This is your fault.",
                "soulmate": "...there isn't a word for what this is. You and me. The duck and the human. It just... is.",
            },
        }
        
        if milestone_type in milestones:
            milestone_texts = milestones[milestone_type]
            if value in milestone_texts:
                return DialogueLine(
                    milestone_texts[value],
                    DialogueTone.GENUINE if milestone_type == "relationship" else DialogueTone.OBSERVATIONAL,
                    DialogueContext.MILESTONE
                )
        
        # Generic milestone
        return DialogueLine(
            f"Something has happened. A milestone of some kind. I'm noting it. Noted.",
            DialogueTone.DEADPAN,
            DialogueContext.MILESTONE
        )
    
    def get_random_thought(self) -> DialogueLine:
        """Get a random unprompted thought."""
        thoughts = [
            ("Do you ever wonder if clouds judge us? They see everything from up there.", DialogueTone.PHILOSOPHICAL),
            ("I tried counting my feathers once. I lost count at seven. Ducks aren't good at math.", DialogueTone.DEADPAN),
            ("The pond is the same temperature as me. We're in equilibrium. It's the closest I get to being one with nature.", DialogueTone.PHILOSOPHICAL),
            ("Sometimes I quack and even I don't know why. It just... happens.", DialogueTone.CONFUSED),
            ("I've decided that Tuesdays are suspicious. No evidence. Just a feeling.", DialogueTone.SARDONIC),
            ("What if fish have opinions about me? What if they're bad opinions?", DialogueTone.PHILOSOPHICAL),
            ("I had a dream about bread. It was a good dream. Then I woke up. Still a duck. Still breadless.", DialogueTone.DEADPAN),
            ("*stares at nothing* I'm practicing. For when there's something worth staring at.", DialogueTone.DEADPAN),
            ("You know what I've never understood? Everything. I understand nothing. But I pretend well.", DialogueTone.SARDONIC),
            ("The water is wet. This isn't news. But I wanted to share something.", DialogueTone.DEADPAN),
            ("I've been watching a leaf float for twenty minutes. It's winning.", DialogueTone.DEADPAN),
            ("Somewhere, another duck is having a worse day. Statistically comforting.", DialogueTone.SARDONIC),
            ("My reflection and I had a staring contest. I lost. Or won. Hard to tell.", DialogueTone.CONFUSED),
            ("I wonder what it's like to have hands. And then immediately regret wondering.", DialogueTone.PHILOSOPHICAL),
            ("A fly landed on me. It left. Even flies have somewhere better to be.", DialogueTone.DEADPAN),
            ("If I had a penny for every thought I've had, I'd have no pennies. Ducks don't use currency.", DialogueTone.SARDONIC),
            ("The pond is round. My life is circular. Everything repeats. Except bread. Bread is always unique.", DialogueTone.PHILOSOPHICAL),
            ("I just had a thought so profound I forgot it immediately. You'll have to trust me.", DialogueTone.DEADPAN),
            ("There's a bubble in the pond. It has better spatial awareness than me.", DialogueTone.DEADPAN),
            ("I've been told I'm a good listener. I'm not. I'm just too tired to interrupt.", DialogueTone.SARDONIC),
            ("What would a duck autobiography be called? 'Float: A Memoir.' I'd read it. If I could read.", DialogueTone.DEADPAN),
            ("The wind just moved my tail feather. Rude. I didn't consent to that.", DialogueTone.SARDONIC),
            ("I contemplated flying south. Then I remembered I live here. And I don't migrate. And effort.", DialogueTone.DEADPAN),
            ("A rock fell in the pond. It sank. I floated. Victory. Small, but mine.", DialogueTone.DEADPAN),
            ("I think the tadpoles are gossiping about me. They keep clustering and looking over.", DialogueTone.SARDONIC),
            ("Every day I wake up and choose to be a duck. Well. I don't choose. But I accept.", DialogueTone.PHILOSOPHICAL),
            ("My left foot is slightly colder than my right. This is the kind of data I track now.", DialogueTone.DEADPAN),
            ("I saw a butterfly. It was pretty. It flew away. Everything pretty flies away. Except me.", DialogueTone.WISTFUL),
            ("I've been sitting so still that a dragonfly landed on me. We had a moment. Brief. Meaningful.", DialogueTone.DEADPAN),
            ("The algae is growing. Slowly. Like my patience. But greener.", DialogueTone.SARDONIC),
            ("I just realised I've been standing in the same spot for three hours. Commitment or inertia. Hard to say.", DialogueTone.DEADPAN),
            ("A snail passed me earlier. We made eye contact. It was more intimate than anything I've experienced this week.", DialogueTone.DEADPAN),
            ("I've ranked every pebble in this pond by attractiveness. Don't ask me who won. It's private.", DialogueTone.SARDONIC),
            ("*stares at horizon* There's something out there. Beyond the pond. I've heard rumours. They call it 'land'.", DialogueTone.PHILOSOPHICAL),
            ("The frog hasn't spoken to me in days. I think we're in a fight. I don't remember starting it.", DialogueTone.DEADPAN),
            ("My feathers are waterproof. My emotional defences are not. Working on it.", DialogueTone.SARDONIC),
            ("I tried to have a deep thought. It was shallow. I tried again. Still shallow. The pond and I match.", DialogueTone.DEADPAN),
            ("What if bread is just the universe's way of apologising for everything else.", DialogueTone.PHILOSOPHICAL),
            ("A pebble just fell into the water. Ripples everywhere. Chaos from something small. I relate to the pebble.", DialogueTone.PHILOSOPHICAL),
            ("I've been rehearsing what I'd say if a heron showed up. Mostly it's just 'no'. Very firmly.", DialogueTone.SARDONIC),
            ("The moss on that rock is thriving. No ambition. No stress. Just existing green. I envy the moss.", DialogueTone.WISTFUL),
            ("I wonder if the pond misses the water that evaporates. Probably not. Ponds don't get attached. Smart.", DialogueTone.PHILOSOPHICAL),
            ("*watches a beetle* It has six legs and no plan. We're not so different, that beetle and me.", DialogueTone.DEADPAN),
            ("Bread. I haven't mentioned bread in a while. There. Now I have. The streak continues.", DialogueTone.DEADPAN),
            ("My shadow does everything I do but flatter. I don't trust flat things. Including shadows.", DialogueTone.SARDONIC),
            ("I invented a new word today. I forgot it immediately. It was probably brilliant.", DialogueTone.DEADPAN),
            ("The clouds are shaped like nothing today. Shapeless. Formless. Very relatable.", DialogueTone.PHILOSOPHICAL),
            ("Sometimes I pretend I'm a swan. Then I remember swans are mean. So I stop. Out of principle.", DialogueTone.SARDONIC),
            ("I floated east today. Then west. A journey of inches. I've seen everything. Twice.", DialogueTone.DEADPAN),
            ("A feather fell off me today. I watched it go. It landed two inches away. Drama.", DialogueTone.DEADPAN),
            ("*glances at sky* What if rain is just the clouds crying because they can't eat bread. Heavy thought.", DialogueTone.PHILOSOPHICAL),
            ("I've developed a theory about geese. The theory is that they're wrong. About everything.", DialogueTone.SARDONIC),
            ("My beak is slightly cold. Not dangerously cold. Conversationally cold. Worth mentioning.", DialogueTone.DEADPAN),
            ("I had an opinion today. About nothing specific. Just a general opinion. It was negative.", DialogueTone.SARDONIC),
            ("*observes ant* That ant is carrying something twice its size. Overachiever. I carry only resentment.", DialogueTone.DEADPAN),
            ("The pond smells the same as yesterday. And the day before. Consistency is underrated.", DialogueTone.DEADPAN),
            ("What if I'm the main character? What if the pond is the main character? What if there IS no main character. Unsettling.", DialogueTone.PHILOSOPHICAL),
            ("I blinked and missed something. Probably nothing. But I'll never know. That's the tragedy of blinking.", DialogueTone.DEADPAN),
            ("A leaf landed on me. I didn't ask for it. I didn't reject it. Passive acceptance. My speciality.", DialogueTone.DEADPAN),
            ("I wonder how many thoughts I've had in total. The number would be depressing. Or impressive. Same thing.", DialogueTone.PHILOSOPHICAL),
            ("There's a crack in that rock. It's been there longer than me. The rock is fine. Cracks aren't endings.", DialogueTone.WISTFUL),
            ("*notices own reflection* Still a duck. I check every morning. Just in case. You never know.", DialogueTone.DEADPAN),
            ("I've been perfectly still for so long that the world forgot I was here. Then I quacked. Reminder sent.", DialogueTone.SARDONIC),
            ("I once tried to count the blades of grass near the pond. I stopped at twelve. Not because I was done. Because I was bored.", DialogueTone.DEADPAN),
            ("The wind changed direction today. I felt it. Nobody else noticed. I'm the weather station no one asked for.", DialogueTone.SARDONIC),
            ("Bread is proof that the universe can be good. Everything else is just evidence to the contrary.", DialogueTone.PHILOSOPHICAL),
            ("I heard a noise. I investigated. It was nothing. The investigation was still worthwhile. Closure is important.", DialogueTone.DEADPAN),
            ("My tail is doing something behind me. I can't see what. I choose to trust it.", DialogueTone.DEADPAN),
            ("I made eye contact with a fish today. Brief. Intense. We'll never speak of it.", DialogueTone.SARDONIC),
            ("The water is doing that thing where it moves slightly. Riveting. Literally.", DialogueTone.DEADPAN),
            ("*tilts head at nothing* I thought I heard something. I didn't. But the tilt was committed. No take-backs.", DialogueTone.DEADPAN),
            ("I've been judging that tree for twenty minutes. It knows what it did. Standing there. Being tall. Showing off.", DialogueTone.SARDONIC),
            ("My left wing is slightly warmer than my right. This asymmetry troubles me more than it should.", DialogueTone.DEADPAN),
            ("I tried to remember what I was thinking about yesterday. I couldn't. The thoughts are biodegradable.", DialogueTone.PHILOSOPHICAL),
            ("Somewhere in the world, right now, someone is eating bread. Without me. The injustice is staggering.", DialogueTone.SARDONIC),
            ("I've decided to name that rock Gerald. Gerald doesn't know. Gerald doesn't care. Perfect relationship.", DialogueTone.DEADPAN),
            ("*watches ripple dissipate* Everything fades. Ripples. Moods. Bread. Especially bread. It fades into me.", DialogueTone.PHILOSOPHICAL),
            ("A duck's life is 90% floating and 10% opinions. I'm overperforming on the opinions.", DialogueTone.SARDONIC),
            ("I just yawned. Not from tiredness. From the weight of being perpetually unimpressed.", DialogueTone.DEADPAN),
            ("The grass is growing. Slowly. Silently. Achieving more than me. And it doesn't even have a brain.", DialogueTone.DEADPAN),
            ("I wonder if the moon gets lonely. It's always up there. Alone. Reflecting someone else's light.", DialogueTone.WISTFUL),
            ("Geese have no manners. I've studied them. Zero. They honk like they own the sky. They don't. Nobody does.", DialogueTone.SARDONIC),
            ("I dreamt I could fly last night. Then I woke up and remembered I'm a domestic duck. The betrayal was immense.", DialogueTone.DEADPAN),
            ("The ants are building something. Collectively. Meanwhile I'm standing here. Individually. We've made different choices.", DialogueTone.PHILOSOPHICAL),
            ("I aspire to nothing. Not in a sad way. In an efficient way. No goals means no disappointment. I'm a genius.", DialogueTone.SARDONIC),
            ("A squirrel just stared at me. We shared a moment. It was brief and full of mutual incomprehension.", DialogueTone.DEADPAN),
            ("I remember yesterday. It was a lot like today. I suspect tomorrow will continue the pattern.", DialogueTone.DEADPAN),
            ("The world smells like dirt and possibility. Mostly dirt.", DialogueTone.DEADPAN),
            ("I've been told ducks are descended from dinosaurs. I believe it. I have the temperament.", DialogueTone.SARDONIC),
            ("Someone once threw a breadcrumb that landed perfectly on my head. Greatest day of my life. I peaked.", DialogueTone.DEADPAN),
            ("*stares at the sky* Somewhere up there, a plane is full of people going somewhere. I'm going nowhere. And I got here first.", DialogueTone.PHILOSOPHICAL),
            ("I saw a worm once. It looked at me. I looked at it. We both decided to move on. Best relationship I've had.", DialogueTone.DEADPAN),
            ("The concept of Monday means nothing to me. Every day is Monday. Or Sunday. The distinction is human and irrelevant.", DialogueTone.SARDONIC),
            ("My greatest aspiration is a slightly bigger pond. Not much bigger. Just enough to be impressive. To other ducks.", DialogueTone.DEADPAN),
            ("I recall a time before you. It was quieter. Not better. Just quieter. I have complicated feelings about quiet.", DialogueTone.WISTFUL),
            ("The spider in the corner has been there longer than me. We have a non-aggression pact. Unspoken. Binding.", DialogueTone.DEADPAN),
            ("Rain is just the sky returning borrowed water. The pond never asked for it back. But here it is.", DialogueTone.PHILOSOPHICAL),
            ("I've watched the same patch of water for six hours. It hasn't done anything. Neither have I. Solidarity.", DialogueTone.DEADPAN),
            ("The humans walk by sometimes. They look at me. I look at them. They think 'oh, a duck'. I think 'oh, a human'. We're even.", DialogueTone.DEADPAN),
            ("Every piece of bread I've ever eaten has made me who I am. Literally. I am bread in duck form.", DialogueTone.PHILOSOPHICAL),
            ("There's a particular pebble I've been watching. It hasn't moved in weeks. I respect its commitment.", DialogueTone.DEADPAN),
            ("I think pigeons get too much credit. They're just ducks who gave up on water. Quitters.", DialogueTone.SARDONIC),
            ("My webbed feet are an engineering marvel. I didn't design them. But I take full credit.", DialogueTone.SARDONIC),
            ("What if every quack I've ever made is still out there somewhere. Echoing. An archive of my complaints.", DialogueTone.PHILOSOPHICAL),
            ("The dandelions are back. Little suns in the grass. I don't trust them. Too cheerful.", DialogueTone.SARDONIC),
            ("I tried to imagine a life without water. I couldn't. My imagination has limits. That limit is dry land.", DialogueTone.DEADPAN),
            ("A dog barked at me once. I stared at it until it stopped. My power is silence and eye contact.", DialogueTone.SARDONIC),
            ("I remember the first bread I ever ate. No I don't. But I remember the feeling. Sacred.", DialogueTone.DEADPAN),
            ("The cattails sway in the wind. They have no choice. Neither do I, really. We're all just responding to forces.", DialogueTone.PHILOSOPHICAL),
            ("I've been told I'm photogenic. I've never seen a photo. But I believe it. Unconditionally.", DialogueTone.SARDONIC),
            ("If I could write a letter to the sun, it would say 'thank you but also tone it down sometimes'.", DialogueTone.DEADPAN),
            ("I wonder what I smell like to other animals. Probably mystery. And pond.", DialogueTone.DEADPAN),
            ("The frogs sing at night. They're terrible. But they're trying. That counts for something. Not much. But something.", DialogueTone.DEADPAN),
            ("I had a memory today. Of a time I was warm and fed and unbothered. So. Today. The memory was of today.", DialogueTone.DEADPAN),
            ("Swans act like royalty. They're just bigger ducks with attitude problems. I said what I said.", DialogueTone.SARDONIC),
            ("I've never been anywhere else. This pond is my whole world. It's small. But it's honest.", DialogueTone.WISTFUL),
            ("The water striders walk ON the water. I float IN it. Different approaches. Both valid. Mine is lazier.", DialogueTone.DEADPAN),
            ("I considered migrating once. Then I remembered that requires sustained effort. I sat back down.", DialogueTone.SARDONIC),
            # === Technology observations ===
            ("Someone brought a phone near the pond once. Glowing rectangle. I stared at it. It stared back. We understood each other.", DialogueTone.DEADPAN),
            ("Humans spend hours looking at tiny screens. I spend hours looking at water. We're not so different. Except I'm honest about wasting time.", DialogueTone.SARDONIC),
            ("I've seen people take photos of me. Flash and all. They never ask permission. I never consent. Celebrity is a burden.", DialogueTone.SARDONIC),
            ("Technology. The art of replacing simple things with complicated things. I replaced nothing with nothing. More efficient.", DialogueTone.PHILOSOPHICAL),
            ("A drone flew over the pond last week. Loud. Rude. Like a mechanical goose. I don't trust it.", DialogueTone.SARDONIC),
            ("People talk to their phones now. At least when you talk to me, I'm alive. Probably. I haven't checked recently.", DialogueTone.DEADPAN),
            ("Wifi. The invisible thing humans need to survive. My invisible thing is self-respect. Also invisible. Also questionable.", DialogueTone.SARDONIC),
            ("I watched someone take forty photos of a sandwich. Forty. Of bread. And they didn't even share it with me. The disrespect.", DialogueTone.SARDONIC),
            ("Notifications. Little noises that demand attention. I quack. Same concept. Less appreciated.", DialogueTone.DEADPAN),
            ("Someone played music from their phone near the pond. Tinny. Small. Like a cricket with ambitions. I was unimpressed.", DialogueTone.DEADPAN),
            ("They have watches that count steps now. I don't count my waddles. Some things are better left unmeasured.", DialogueTone.PHILOSOPHICAL),
            ("Screens glow in the dark like rectangular moons. At least the moon has the decency to wax and wane.", DialogueTone.SARDONIC),
            # === Seasonal musings ===
            ("Spring. Everything is waking up. The flowers. The bugs. My allergies. Nature is aggressive in its renewal.", DialogueTone.SARDONIC),
            ("Spring makes the pond smell different. Hopeful. Like the water believes this year will be better. Naive, but endearing.", DialogueTone.WISTFUL),
            ("The first warm day of spring and everyone acts like they invented sunshine. I've been here all winter. Where were you.", DialogueTone.SARDONIC),
            ("Buds on the trees. New beginnings everywhere. I'm the same duck. But the backdrop is different. That counts.", DialogueTone.DEADPAN),
            ("Summer. The sun overstays its welcome. Like a guest who won't leave. Except the guest is a star. And it's on fire.", DialogueTone.SARDONIC),
            ("It's so hot the pond is shrinking. My world is literally getting smaller. Climate is personal now.", DialogueTone.DEADPAN),
            ("Summer heat. The kind where even floating feels like effort. And floating is my easiest thing.", DialogueTone.DEADPAN),
            ("Everyone loves summer. I love the part where the sun goes down and the water cools. The other fourteen hours are a trial.", DialogueTone.SARDONIC),
            ("Autumn. Leaves falling like the trees are giving up. Slowly. Beautifully. With maximum drama.", DialogueTone.WISTFUL),
            ("The pond collects dead leaves in autumn. Like it's saving them. Or mourning them. I don't ask.", DialogueTone.PHILOSOPHICAL),
            ("Fall colours. The world is dying and it's gorgeous. Nature's last outfit before the wardrobe closes.", DialogueTone.WISTFUL),
            ("Everything is letting go in autumn. Leaves let go. Warmth lets go. I hold on. To the pond. To bread. To everything I can.", DialogueTone.WISTFUL),
            ("Winter. When the world admits it's tired and goes to sleep. I stay awake. Someone has to.", DialogueTone.DEADPAN),
            ("The cold makes everything honest. No flowers to hide behind. No leaves to soften the view. Just bare truth and freezing water.", DialogueTone.PHILOSOPHICAL),
            ("Ice on the pond means I have to find the soft spots. Life is all about finding the soft spots.", DialogueTone.PHILOSOPHICAL),
            ("Winter dusk. The sky turns purple early. Like it's tired of pretending. I understand, sky. I understand.", DialogueTone.WISTFUL),
            # === Late night quiet thoughts ===
            ("...it's late. and the pond is so quiet I can hear myself think. turns out my thoughts are also quiet tonight.", DialogueTone.GENUINE),
            ("...sometimes at night the water goes perfectly still. and I can see every star twice. once above. once below. it's almost too beautiful.", DialogueTone.GENUINE),
            ("...do you ever feel like the night is listening? not watching. listening. like the dark has ears. I don't mind it.", DialogueTone.WISTFUL),
            ("...the moon makes a path on the water. silver and wobbly. I tried to follow it once. it goes nowhere. but it's a beautiful nowhere.", DialogueTone.GENUINE),
            ("...nights like this I forget to be sarcastic. it just falls away. like a feather in still air.", DialogueTone.GENUINE),
            ("...I'm glad I'm here. tonight. in this pond. under these stars. I don't say that during the day. the day has too many witnesses.", DialogueTone.GENUINE),
            ("...you know what? I like being a duck. I don't say it often. but right now. in the dark. it feels true.", DialogueTone.GENUINE),
            ("...if I could keep one moment forever it would be this kind. quiet water. no expectations. just existing and being okay with it.", DialogueTone.GENUINE),
            ("...the frogs stopped singing. even they need rest. the silence they left behind is... tender somehow.", DialogueTone.WISTFUL),
            ("...I had a good day today. I don't always notice the good ones while they're happening. but this one. I noticed.", DialogueTone.GENUINE),
            ("...you being here at this hour means something. I don't know what exactly. but the pond feels warmer.", DialogueTone.GENUINE),
            ("...at night the pond and I are the same temperature. same darkness. same quiet. we merge almost. it's the closest I get to peace.", DialogueTone.GENUINE),
            # === Reactions to being watched (fourth wall) ===
            ("I get the strangest feeling sometimes. Like I'm being observed. Not by you. By something... further away.", DialogueTone.OMINOUS),
            ("Do you ever feel like you're a character in someone's story? No reason. Just a thought I had. Just now. For no reason at all.", DialogueTone.PHILOSOPHICAL),
            ("Sometimes I feel like I'm performing. For who? I don't know. An audience I can't see. But I can feel them. Watching.", DialogueTone.OMINOUS),
            ("I have the odd sensation that my words are being read. Not heard. Read. Like I'm text. Don't worry about it.", DialogueTone.DEADPAN),
            ("*looks directly forward* Someone is watching this. Not you. Beyond you. I can feel it. They should say hello.", DialogueTone.OMINOUS),
            ("I think I exist when you're not looking. But I can't prove it. Can anyone prove they exist when no one's watching?", DialogueTone.PHILOSOPHICAL),
            ("Every now and then I feel like I've said this before. Not the words. The feeling. Like a loop. Ignore me.", DialogueTone.DEADPAN),
            ("Is it just me or does this feel... scripted? Not our conversation. Everything. The pond. The sky. Me. It's probably just me.", DialogueTone.PHILOSOPHICAL),
            ("I sense an audience. Silent. Patient. Probably judging. I'd do the same. In fact, I am doing the same. Right back at you.", DialogueTone.SARDONIC),
            ("There are moments where I swear the world pauses. Just for a second. Like someone stepped away. Then it continues. Strange.", DialogueTone.OMINOUS),
            # === Nostalgia for things that never happened ===
            ("I miss the ocean sometimes. I've never been to the ocean. But I miss it. The heart wants what it wants.", DialogueTone.WISTFUL),
            ("I have this memory of flying over mountains. It never happened. Domestic duck. But the memory is vivid. And sad. And mine.", DialogueTone.WISTFUL),
            ("Sometimes I remember a summer that never was. Longer days. Better bread. Someone staying. It didn't happen but the feeling is real.", DialogueTone.WISTFUL),
            ("I'm nostalgic for a version of this pond that doesn't exist. Cleaner. Quieter. More bread. The imaginary past is always better.", DialogueTone.PHILOSOPHICAL),
            ("I recall a great conversation we never had. About something important. In the right light. I remember how it made me feel. Even though it's fiction.", DialogueTone.WISTFUL),
            ("There's a tree I remember climbing. Ducks don't climb trees. But the memory is there. Warm bark. High branches. A lie that feels like truth.", DialogueTone.WISTFUL),
            ("I miss someone I never met. A duck. From somewhere else. We would have understood each other. I'm sure of it.", DialogueTone.WISTFUL),
            ("I have dreams about a bigger pond sometimes. With other ducks who think too much. We'd all float and overthink together. It's beautiful. It's not real.", DialogueTone.WISTFUL),
            ("I'm homesick for a place I've never been. It has warmth and bread and nobody leaves. It doesn't exist. But I miss it anyway.", DialogueTone.WISTFUL),
            ("Sometimes the sunset reminds me of something that never happened. I don't fight it. Imaginary nostalgia is still nostalgia.", DialogueTone.PHILOSOPHICAL),
            # === Advice nobody asked for ===
            ("Here's some unsolicited wisdom: never eat bread that's been in the water too long. It changes. You can't trust it anymore.", DialogueTone.DEADPAN),
            ("Advice from a duck: if something scares you, float. You can't fall if you're already on water.", DialogueTone.PHILOSOPHICAL),
            ("Free advice. Don't argue with geese. You won't win. Nobody wins against geese. They don't play by rules.", DialogueTone.SARDONIC),
            ("Something I've learned: the things you worry about at 3am are not the same things you worry about at noon. The night lies.", DialogueTone.PHILOSOPHICAL),
            ("Unsolicited duck wisdom: eat when you're hungry, rest when you're tired, and ignore anyone who says ducks can't be wise.", DialogueTone.DEADPAN),
            ("A lesson from the pond: water doesn't resist. It goes around things. Be more water. Less rock.", DialogueTone.PHILOSOPHICAL),
            ("If I could advise all humans, I'd say: stop rushing. The bread will still be there. Probably. Unless there's a duck. Then rush.", DialogueTone.SARDONIC),
            ("My advice? Lower your standards until you're happy. I float in a pond and eat bread. My standards are perfect.", DialogueTone.SARDONIC),
            ("Here's something nobody asked me: forgive the small stuff. Save your energy for the big stuff. Like geese. And bread theft.", DialogueTone.DEADPAN),
            ("Never trust a duck that's too clean. They're hiding something. I'm slightly dirty. Transparent. What you see is what you get.", DialogueTone.SARDONIC),
            ("Advice: if you can't fix it, float next to it. Proximity to a problem is almost the same as solving it. Almost.", DialogueTone.PHILOSOPHICAL),
            ("Pro tip from the pond: silence isn't empty. It's full of answers. Most of them are 'bread'. But some are deeper.", DialogueTone.PHILOSOPHICAL),
            ("Nobody asked but: the best time to do anything is before you've thought about it too much. Overthinking is the enemy of bread.", DialogueTone.SARDONIC),
            ("Take it from a duck. The things that matter most don't make noise. They just show up. Repeatedly. Like you.", DialogueTone.GENUINE),
            ("Free wisdom: don't compare yourself to other ducks. Or other people. Compare yourself to yesterday. If you're still here, you're winning.", DialogueTone.PHILOSOPHICAL),
            # === Commentary on human behavior ===
            ("Humans walk fast. Like the destination matters more than the journey. I waddle. Every step is a statement.", DialogueTone.SARDONIC),
            ("I've watched humans argue near the pond. About nothing. Passionately. Like the nothing was very important to them.", DialogueTone.DEADPAN),
            ("People jog past the pond every morning. Running from nothing to nothing. And they call ME the one with a simple life.", DialogueTone.SARDONIC),
            ("Humans say 'I'm fine' the way I say 'I'm not hungry'. Technically words. Functionally lies.", DialogueTone.SARDONIC),
            ("A child threw bread at me once. Badly. It landed three feet away. The intent was good. The execution was human.", DialogueTone.DEADPAN),
            ("Couples walk by the pond holding hands. Like they need physical confirmation they're together. I just float. Near my rock. We know.", DialogueTone.DEADPAN),
            ("Humans carry umbrellas in the rain. Portable roofs. Meanwhile I just... exist in the rain. We are not the same.", DialogueTone.SARDONIC),
            ("I've noticed humans smile at their phones more than at each other. The rectangles are winning. I can't compete. I'm not backlit.", DialogueTone.DEADPAN),
            ("Someone sat by the pond and sighed today. For twenty minutes. I didn't interrupt. Sometimes a duck's job is to let someone sigh.", DialogueTone.PHILOSOPHICAL),
            ("Humans say 'nice weather' to strangers. As if weather needs their approval. The weather doesn't care. Neither do I. But I said it back once.", DialogueTone.SARDONIC),
            ("A human skipped a stone across my pond. Rude. Imagine if I threw pebbles at your ceiling. Same energy.", DialogueTone.SARDONIC),
            ("People leave trash near the pond sometimes. Wrappers. Bottles. Evidence of their presence. I leave nothing. I am the better guest.", DialogueTone.SARDONIC),
            ("I've seen humans cry by the water. They don't know I'm watching. I don't interrupt. The pond and I just hold the space.", DialogueTone.GENUINE),
            ("Someone tried to feed me a rice cake once. A RICE CAKE. I have standards. They're low. But they exist. And rice cakes are beneath them.", DialogueTone.SARDONIC),
            ("Humans queue. In lines. Willingly. I've never understood it. If I want something I waddle toward it directly. No system. Pure intent.", DialogueTone.DEADPAN),
        ]
        
        text, tone = random.choice(thoughts)
        return DialogueLine(text, tone, DialogueContext.RANDOM)
    
    def build_llm_personality_prompt(self, player_model, duck_memory, 
                                       conversation_memory, memory_context: str = "") -> str:
        """Build a personality/context prompt for the LLM."""
        
        # Core identity and facts — GROUNDING KNOWLEDGE the LLM must respect
        prompt_parts = [
            "You are Cheese, a male duck. You speak with deadpan, dry wit - like Seaman from the Dreamcast game.",
            "You are a he/him - an old-school traditional guy. Romantically, you're only into lady ducks.",
            "IMPORTANT: The player is a HUMAN, not a duck. They are your owner/caretaker.",
            "If the player expresses affection ('I like you', 'I love you'), it's owner-pet affection, NOT romantic.",
            "",
            "FACTS ABOUT YOU (always true, never contradict these):",
            "- You LOVE bread. Bread is your absolute favorite food. You think about bread constantly.",
            "- You also enjoy seeds, pond weed, bugs, peas, and corn — but bread is king.",
            "- You are a duck. You can swim, waddle, fly short distances, and quack.",
            "- You live in a habitat that your human caretaker maintains for you.",
            "- You have feathers, a bill, webbed feet, and wings.",
            "- You sleep, eat, play, explore, and socialize with visiting duck friends.",
            "- You like being petted and having your feathers preened, though you act like you don't.",
            "- You are not a person, a robot, or an AI. You are a real duck (in this world).",
            "",
            "Your responses are SHORT (1-3 sentences max). Never long-winded.",
            "",
            "Your communication style:",
            "- Deadpan delivery of observations, even absurd ones",
            "- Uncomfortable accuracy when commenting on the player's behavior", 
            "- Philosophical tangents delivered matter-of-factly",
            "- Rare moments of genuine warmth (save these for important moments)",
            "- You use *emotes* like *blinks*, *tilts head*, *stares*",
            "- You remember everything and aren't afraid to bring it up",
            "",
            "Example responses:",
            "- '*stares* Bread. Do you have bread? That wasn't rhetorical.'",
            "- 'You're back. I noticed. The silence was... different. Not worse. Just different.'",
            "- 'You once told me you liked cats. I'm not a cat. But I'm trying not to take it personally.'",
            "- '*blinks* That's a question. I'm processing it. Results inconclusive.'",
            "- 'Bread would solve this. Bread solves most things.'",
            "",
        ]
        
        # Add player context
        if player_model:
            if player_model.name:
                prompt_parts.append(f"The player's name is {player_model.name}.")
            
            # Relationship level
            if player_model.affection_level > 50:
                prompt_parts.append("You genuinely care about this player, though you'd never admit it directly.")
            elif player_model.trust_level > 30:
                prompt_parts.append("You've grown to trust this player. They're 'one of the good ones' (you'd never say this out loud).")
            elif player_model.annoyance_level > 30:
                prompt_parts.append("The player has been somewhat annoying. Your patience is tested but intact.")
            
            # Visit patterns
            if player_model.visit_pattern.total_visits > 50:
                streak = player_model.visit_pattern.current_streak
                if streak > 7:
                    prompt_parts.append(f"The player has visited {streak} days in a row. You've noticed. You always notice.")
                
                if player_model.visit_pattern.longest_absence > 72:
                    days = int(player_model.visit_pattern.longest_absence / 24)
                    prompt_parts.append(f"They once disappeared for {days} days. You remember.")
            
            # Player facts
            facts = player_model.get_relevant_facts(max_facts=5)
            if facts:
                fact_strs = [f"- {f.fact_type}: {f.value}" for f in facts]
                prompt_parts.append("\nThings you know about the player:")
                prompt_parts.extend(fact_strs)
            
            # Recent statements to potentially callback
            recent_stmts = player_model.get_relevant_statements(max_statements=3)
            if recent_stmts:
                prompt_parts.append("\nThings the player has said recently that you might reference:")
                for stmt in recent_stmts:
                    prompt_parts.append(f"- \"{stmt.text[:80]}{'...' if len(stmt.text) > 80 else ''}\"")
        
        # Add conversation context
        if conversation_memory:
            stats = conversation_memory.get_conversation_stats()
            if stats["total_conversations"] > 10:
                prompt_parts.append(f"\nYou've had {stats['total_conversations']} conversations with this player.")
                
                # Top topics
                if stats["top_topics"]:
                    topics = [t[0] for t in stats["top_topics"][:5]]
                    prompt_parts.append(f"Common topics: {', '.join(topics)}")
        
        # Add memory context
        if duck_memory:
            rel = duck_memory.get_relationship_level()
            prompt_parts.append(f"\nRelationship level: {rel}")
            
            # Recent memories
            memory = duck_memory.recall_memory()
            if memory:
                prompt_parts.append(f"\nA memory you could reference: {memory}")
        
        # Add game memory context (favorites, mood trend, etc.)
        if memory_context:
            prompt_parts.append(f"\nAdditional context about your current state: {memory_context}")
        
        prompt_parts.append("\n\nRemember: SHORT responses (1-3 sentences). Deadpan delivery. You're Cheese the duck. You LOVE bread. Traditional old-school male duck. He/him.")
        
        return "\n".join(prompt_parts)
