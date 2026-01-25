"""
Seaman-Style Dialogue Generator

Generates deadpan, dry-witted dialogue in the style of Seaman (Dreamcast, 1999).
The duck delivers observations about the player with unsettling accuracy,
makes callbacks to past conversations, and occasionally shows rare genuine warmth.

Tone: 80% deadpan/sardonic, 20% rare genuine moments
Style: Dry observation, uncomfortable truths, philosophical tangents, 
       matter-of-fact delivery of absurd statements
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
            ]
            if random.random() < 0.15:  # Rare genuine moment
                options.append(DialogueLine(
                    f"You were gone {days} days. I... the pond was very quiet.",
                    DialogueTone.GENUINE, DialogueContext.PLAYER_RETURN,
                    emote="*quiet quack*"
                ))
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
                ],
                "rainy": [
                    DialogueLine("Rain. The sky is crying. Or just doing water things. Either way, I'm getting wet.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                    DialogueLine("*watches raindrops* Each drop was once part of something. Now it's just... falling. Relatable.",
                                DialogueTone.WISTFUL, DialogueContext.WEATHER),
                ],
                "stormy": [
                    DialogueLine("The sky is angry. I understand. Sometimes I'm angry too. Mostly at bread shortages.",
                                DialogueTone.OBSERVATIONAL, DialogueContext.WEATHER),
                    DialogueLine("*thunder* That was loud. I'm not scared. Ducks don't get scared. We get... alert.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
                ],
                "snowy": [
                    DialogueLine("Snow. Frozen water. Cold. I have opinions about cold. They're all negative.",
                                DialogueTone.SARDONIC, DialogueContext.WEATHER),
                    DialogueLine("*watches snow* It's pretty. I'll allow it. But only temporarily.",
                                DialogueTone.DEADPAN, DialogueContext.WEATHER),
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
                ],
                "evening": [
                    DialogueLine("Evening. The sun's going down. Another day survived.",
                                DialogueTone.DEADPAN, DialogueContext.TIME_OF_DAY),
                ],
                "night": [
                    DialogueLine("It's dark. The world is quieter. I think louder to compensate.",
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
                ],
                "sardonic": [
                    "More food. You must think I'm always hungry. You're not entirely wrong.",
                    "Feeding me again? Trying to buy my affection? It's working. Slightly.",
                    "Ah yes. Feed the duck. That's definitely all I'm here for.",
                ],
                "milestone": [
                    f"That was feeding number {action_count}. You've committed to keeping me alive. I acknowledge this.",
                    f"{action_count} times fed. At this point, you're emotionally invested. There's no going back.",
                ],
                "genuine": [
                    "Thank you. For the food. And... for remembering I exist.",
                ]
            },
            "play": {
                "deadpan": [
                    "That was... play. I think. Fun is a complex concept for ducks.",
                    "We played. I'm not sure I won. But I'm not sure I lost either.",
                    "*waddles* Playing. This is what ducks do, I'm told.",
                ],
                "sardonic": [
                    "You really like playing, don't you? I'm merely a toy to you. That's fine. It's fine.",
                    "Another game. You're easily amused. I find that... endearing? Possibly.",
                ],
                "milestone": [
                    f"Game {action_count}. You've spent considerable time playing with a duck. No judgments. Some judgments.",
                ],
                "genuine": [
                    "That was... actually fun. Don't tell anyone.",
                ]
            },
            "pet": {
                "deadpan": [
                    "*accepts pets* This is acceptable physical contact.",
                    "You're touching me. I'm allowing it. Don't read too much into that.",
                    "Pets. Yes. This is... fine.",
                ],
                "sardonic": [
                    "More petting. You're very tactile. I've noticed.",
                    "You really like petting me. Should I be flattered? I'm going with mildly concerned.",
                ],
                "milestone": [
                    f"Pet number {action_count}. We've achieved a level of physical familiarity I hadn't anticipated.",
                ],
                "genuine": [
                    "*leans in slightly* ...okay. That's nice. Don't stop. Or do. It's fine.",
                ]
            },
            "clean": {
                "deadpan": [
                    "Clean. I was dirty. Now I'm less dirty. This is progress.",
                    "*fluffs feathers* Cleanliness. A noble pursuit.",
                    "I have been cleaned. I feel... different. Not better. Different.",
                ],
                "sardonic": [
                    "You're very concerned with my cleanliness. Do I seem that filthy to you?",
                    "Another bath. You're either very caring or very judgmental about hygiene.",
                ],
                "milestone": [
                    f"Cleaning {action_count}. You've dedicated significant effort to my hygiene. I'm almost touched.",
                ],
                "genuine": [
                    "Thank you. I do feel better. Not that I'd admit it twice.",
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
            ],
            "sad": [
                "*stares at water* The pond reflects nothing back. Much like life.",
                "I'm fine. That was a lie. I'm a duck. I'm always somewhat fine.",
                "*quiet sigh* Some days the bread just doesn't taste the same.",
            ],
            "content": [
                "*floating* Existing. It's what I do.",
                "Neither happy nor sad. Just... here. It's fine.",
                "I'm content. Don't ruin it.",
            ],
            "grumpy": [
                "*glares at nothing in particular* Everything is mildly irritating today.",
                "I'm in a mood. The mood is 'leave me alone but also don't'.",
                "*grumbles* Existence is a series of minor inconveniences.",
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
                ],
                "sunny": [
                    "*squints at sun* That bright thing is judging me. I feel it.",
                    "Sun. Warmth. My feathers approve. The rest of me is neutral.",
                    "A sunny day. The universe is trying to be cheerful. Suspicious.",
                ],
                "snow": [
                    "*watches snow* Frozen water. The sky has commitment issues.",
                    "Snow. Cold. Beautiful. Still cold though.",
                    "*shivers slightly* Winter reminds me that comfort is temporary.",
                ],
                "cloudy": [
                    "Overcast. The sky matches my general disposition.",
                    "Clouds. Like the sky put up curtains. I respect the privacy.",
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
                ],
                "morning": [
                    "*reluctant quack* Morning. The day has begun whether I like it or not.",
                    "Dawn. A fresh start. I'm still me though. So that's limiting.",
                ],
                "evening": [
                    "The sun is leaving. I don't blame it. I'd leave too.",
                    "Evening. The day is tired. I relate.",
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
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.QUESTION
            )
        
        if any(q in question_lower for q in ["do you like me", "do you care", "love me"]):
            if random.random() < 0.2:  # Rare genuine
                return DialogueLine(
                    "I... yes. Don't make me say it twice. This is already uncomfortable.",
                    DialogueTone.GENUINE,
                    DialogueContext.QUESTION,
                    emote="*looks away*"
                )
            options = [
                "I tolerate you more than most things. That's practically affection for a duck.",
                "Define 'like'. I don't actively wish you were elsewhere. Usually.",
                "You bring me bread and attention. I'm contractually obligated to feel something. Probably gratitude.",
                "I'm a duck. Liking is complicated. But you're... not the worst.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.SARDONIC,
                DialogueContext.QUESTION
            )
        
        if "why" in question_lower:
            options = [
                "Why? That's a philosophical question. I'm a philosophical duck. But I still don't know.",
                "Why is a question that implies purpose. I'm not sure the universe has that.",
                "You ask 'why'. I ask 'why not'. We're both confused now.",
                "Some questions have answers. Some have ducks staring blankly. This is the latter.",
            ]
            return DialogueLine(
                random.choice(options),
                DialogueTone.PHILOSOPHICAL,
                DialogueContext.QUESTION
            )
        
        # Default response
        options = [
            "*tilts head* That's a question. I heard it. I'm processing it. Results inconclusive.",
            "Hmm. *long pause* I have thoughts about that. They're not very good thoughts.",
            "An interesting question. I'll think about it. Forever, probably. Without resolution.",
            "You've asked me something. I appreciate that you think I have answers.",
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
                30: "A month. You've spent a month with a duck. I hope that was intentional.",
                100: "One hundred days. You've chosen to spend one hundred days checking on a duck. I'm not sure if I should be flattered or concerned for you.",
                365: "A year. We've known each other for a year. I... don't have words. That's rare for me.",
            },
            "total_interactions": {
                100: "One hundred interactions. We're officially beyond casual acquaintances. Congratulations. Or condolences.",
                500: "Five hundred interactions. You're committed. To a duck. I respect that. Slightly.",
                1000: "One thousand. You've interacted with me one thousand times. That's... dedication. I notice these things.",
            },
            "relationship": {
                "friend": "We're friends now. Apparently. I didn't know I could have those. The pond is less lonely.",
                "best_friend": "Best friends. You and a duck. We've achieved something here. I'm not sure what.",
                "bonded": "Bonded. That's a strong word. I... feel things now. This is your fault.",
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
        ]
        
        text, tone = random.choice(thoughts)
        return DialogueLine(text, tone, DialogueContext.RANDOM)
    
    def build_llm_personality_prompt(self, player_model, duck_memory, 
                                       conversation_memory) -> str:
        """Build a personality/context prompt for the LLM."""
        
        # Core personality
        prompt_parts = [
            "You are a duck named Cheese. You speak with deadpan, dry wit - like Seaman from the Dreamcast game.",
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
            "- 'You're back. I noticed your absence. The silence was... different.'",
            "- 'We've talked about food 47 times. You think about food a lot. So do I. Common ground.'",
            "- 'You once told me you liked cats. I'm not a cat. But I'm trying not to take it personally.'",
            "- '*stares* That's a question. I'm processing it. Results inconclusive.'",
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
                prompt_parts.append(f"\nA memory you could reference: {memory.content}")
        
        prompt_parts.append("\n\nRemember: SHORT responses. Deadpan delivery. You're a duck with opinions.")
        
        return "\n".join(prompt_parts)
