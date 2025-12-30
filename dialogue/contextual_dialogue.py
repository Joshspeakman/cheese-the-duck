"""
Contextual Dialogue System - Comments on weather, events, and visitors.
Deadpan witty nonsense in the finest Animal Crossing tradition.
"""
import random
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ContextComment:
    """A contextual comment the duck can make."""
    text: str
    rarity: int = 1  # 1 = common, 2 = uncommon, 3 = rare


# =============================================================================
# WEATHER COMMENTS - Deadpan reactions to weather
# =============================================================================

WEATHER_COMMENTS: Dict[str, List[ContextComment]] = {
    "sunny": [
        ContextComment("*squints* The sun is out. Aggressively."),
        ContextComment("Sunny day. Perfect for standing here. Menacingly."),
        ContextComment("*basking* I'm absorbing vitamin D. For my bones. Duck bones."),
        ContextComment("The sun is judging me. I can feel it."),
        ContextComment("*sits in sunbeam* I've claimed this spot. Fight me."),
        ContextComment("Another sunny day in paradise. Allegedly."),
        ContextComment("The weather is being suspiciously pleasant today."),
        ContextComment("*preening* The sun brings out my natural radiance. Obviously."),
        ContextComment("Sunny. Good. I was worried it might be interesting outside.", 2),
        ContextComment("I'm a solar-powered duck today. Don't unplug me.", 2),
    ],
    "cloudy": [
        ContextComment("*looks up* Clouds. The sky's way of being indecisive."),
        ContextComment("Overcast. Very dramatic. Very moody."),
        ContextComment("The clouds match my general life outlook. Gray."),
        ContextComment("*stares at clouds* That one looks like bread. They all look like bread."),
        ContextComment("Cloudy with a chance of me standing here doing nothing."),
        ContextComment("The sun is hiding. Probably from its responsibilities."),
        ContextComment("*contemplative* The clouds understand me."),
        ContextComment("Atmospheric conditions are... atmospheric.", 2),
        ContextComment("Gray skies. My kind of aesthetic.", 2),
        ContextComment("The clouds are having a meeting. I wasn't invited.", 3),
    ],
    "rainy": [
        ContextComment("*splashing* PUDDLES. This is EXCELLENT."),
        ContextComment("Rain. Finally, weather that matches my personality."),
        ContextComment("*getting wet* I'm a duck. This is literally my element."),
        ContextComment("*opens beak* Free water from the sky. Efficient."),
        ContextComment("The sky is crying. I relate."),
        ContextComment("*shakes feathers* Built-in raincoat. Superior duck technology."),
        ContextComment("Rain makes the worms come out. I'm not saying anything else."),
        ContextComment("*stands in rain* This is refreshing. And free."),
        ContextComment("Pitter patter. The only acceptable form of small talk.", 2),
        ContextComment("*splashing intensifies* YOU CAN'T STOP ME.", 2),
        ContextComment("The rain whispers secrets. Mostly 'splash splash' but still.", 3),
    ],
    "stormy": [
        ContextComment("*nervous* That thunder was... fine. I'm fine. Everything's fine."),
        ContextComment("*feathers puffed* I'M NOT SCARED. I'm just... alert."),
        ContextComment("Storm's here. Nature is having a moment."),
        ContextComment("*flinches at thunder* ...that was on purpose."),
        ContextComment("*hiding under wing* I'm not hiding. I'm conserving heat."),
        ContextComment("Lightning is just sky electricity. Sky electricity can't hurt me. Probably."),
        ContextComment("The universe is yelling. Classic universe behavior."),
        ContextComment("*watching storm* This is fine. I'm waterproof. Partially."),
        ContextComment("*duck under cover* Strategic repositioning. Not fear.", 2),
        ContextComment("*counting after lightning* One... two... WHERE IS COVER?", 2),
        ContextComment("The storm respects me. We have an understanding.", 3),
    ],
    "foggy": [
        ContextComment("*squinting* I can't see anything. This is concerning."),
        ContextComment("Fog. Very mysterious. Very me."),
        ContextComment("*walks into fog* Stealth mode activated."),
        ContextComment("The world has been replaced with cotton. Interesting."),
        ContextComment("I could be anywhere right now. Mostly I'm here though."),
        ContextComment("*appearing from fog* BOO. ...did that work?"),
        ContextComment("Silent Hill energy today. Not loving it."),
        ContextComment("The fog is hiding something. Probably just more fog.", 2),
        ContextComment("*dramatic entrance from fog* ...no one saw that? Okay.", 2),
        ContextComment("I am one with the mist. The mist is also confused.", 3),
    ],
    "snowy": [
        ContextComment("*shivers* Cold. The air is attacking me."),
        ContextComment("Snow. Frozen water falling from the sky. Rude."),
        ContextComment("*fluffed up* Maximum poof mode engaged."),
        ContextComment("*standing in snow* My feet are cold. My dignity is colder."),
        ContextComment("Winter has come. I didn't invite it."),
        ContextComment("*catches snowflake on beak* ...okay that was actually nice."),
        ContextComment("Snow day. Perfect for indoor activities. ...we're outside."),
        ContextComment("The world is a freezer now. Cool. Literally.", 2),
        ContextComment("*waddles in snow* I'm making duck prints. Art.", 2),
        ContextComment("Snow angels? I prefer 'snow duck aggressive floor interaction'.", 3),
    ],
    "windy": [
        ContextComment("*feathers everywhere* MY AESTHETIC. IT'S RUINED."),
        ContextComment("The wind is testing me. I will not be moved."),
        ContextComment("*leaning into wind* I am steadfast. Majestic even."),
        ContextComment("*blown sideways* ...I meant to do that."),
        ContextComment("Wind advisory: duck may experience temporary flight."),
        ContextComment("The wind is whispering. It's saying 'whoooosh'. Very profound."),
        ContextComment("*flapping in wind* I could fly right now. I'm choosing not to."),
        ContextComment("*bracing* The wind respects no one. Especially not feathers.", 2),
        ContextComment("Windy day. Good for dramatic pauses.", 2),
        ContextComment("I am become kite. Destroyer of composure.", 3),
    ],
    "rainbow": [
        ContextComment("*staring* ...is the sky having a moment? Should I be concerned?"),
        ContextComment("Rainbow. The sky is showing off again."),
        ContextComment("*impressed despite self* ...okay, that's actually pretty."),
        ContextComment("A rainbow. Pot of gold at the end, allegedly."),
        ContextComment("*gazing* This is the most color I've experienced today."),
        ContextComment("The universe is apologizing for the rain. Accepted."),
        ContextComment("Rainbow means the storm apologized. Good. It should.", 2),
        ContextComment("*chasing rainbow* I WILL FIND THE GOLD. ...eventually.", 2),
        ContextComment("The sky is gay. Good for it, honestly.", 3),
    ],
}


# =============================================================================
# EVENT COMMENTS - Reactions to various events
# =============================================================================

EVENT_COMMENTS: Dict[str, List[ContextComment]] = {
    "found_crumb": [
        ContextComment("CRUMB. MINE. Don't even LOOK at it."),
        ContextComment("*possessively* I found this. Me. It's mine now."),
        ContextComment("The universe provides. Mostly crumbs, but still."),
    ],
    "butterfly": [
        ContextComment("*watching* I could catch it. I'm choosing not to."),
        ContextComment("Butterfly. Flying around like it owns the place. Rude."),
        ContextComment("*head tracking* Don't think I don't see you, butterfly."),
    ],
    "nice_breeze": [
        ContextComment("*feathers rustle* The wind knows how to treat a duck."),
        ContextComment("Ah. Nature's air conditioning."),
        ContextComment("*content sigh* ...don't tell anyone I made that sound."),
    ],
    "found_shiny": [
        ContextComment("SHINY. This is MINE now. No questions."),
        ContextComment("*hoarding* The treasure... grows."),
        ContextComment("Another addition to the collection. Excellent."),
    ],
    "random_quack": [
        ContextComment("*quack* ...I don't know why I did that either."),
        ContextComment("*sudden quack* ...anyway."),
        ContextComment("Quack. There. I said it."),
    ],
    "bird_overhead": [
        ContextComment("*looks up* Show off. Not all of us can fly."),
        ContextComment("Bird. In the sky. Being all... sky-like."),
        ContextComment("*watching bird* One day. One day I'll figure out the flying thing."),
    ],
    "splash_sound": [
        ContextComment("*ears perk* SPLASH? WHERE? Is someone having fun without me?"),
        ContextComment("I heard water. My people are calling."),
        ContextComment("*excited* Pool party? POOL PARTY?"),
    ],
    "leaf_falls": [
        ContextComment("*watches leaf* Gravity claims another victim."),
        ContextComment("A leaf fell. Circle of life or whatever."),
        ContextComment("*inspects leaf* You okay, buddy? ...it's a leaf. I'm talking to a leaf."),
    ],
    "acorn_drops": [
        ContextComment("*startled* WHAT WAS THAT. Oh. Acorn. Okay."),
        ContextComment("*investigates* Not edible. Probably. ...maybe."),
        ContextComment("Nature is dropping things. Classic nature."),
    ],
}


# =============================================================================
# VISITOR COMMENTS - Reactions to visitors based on personality
# =============================================================================

VISITOR_COMMENTS: Dict[str, List[ContextComment]] = {
    "adventurous": [
        ContextComment("Oh look, the adventurer is here. Probably lost again."),
        ContextComment("*nods* Tell me about your 'incredible journey'. Again."),
        ContextComment("Adventure duck is here. I'm already tired just looking at them."),
        ContextComment("*sigh* Here comes trouble. The fun kind, allegedly."),
        ContextComment("Adventure time. I'll just... watch from here.", 2),
    ],
    "scholarly": [
        ContextComment("The smart one is here. Time for unsolicited facts."),
        ContextComment("*prepares for lecture* Go ahead. Educate me."),
        ContextComment("Ah, the wise one. What wisdom do they bring? Probably about bread."),
        ContextComment("*respectful nod* Fellow intellectual. Or whatever.", 2),
        ContextComment("I understood maybe 40% of that. I'll pretend it was 90%.", 2),
    ],
    "artistic": [
        ContextComment("The artsy one. Everything's a canvas to them. Even me."),
        ContextComment("*poses* Am I art? I feel like I should be art."),
        ContextComment("Creative friend is here. Time for deep thoughts about shapes."),
        ContextComment("Art is subjective. I'm objectively adorable though.", 2),
        ContextComment("*looking at nothing* I'm appreciating the aesthetic. Obviously.", 2),
    ],
    "playful": [
        ContextComment("Oh no. The chaotic one. My feathers are not ready."),
        ContextComment("*bracing for impact* Here comes the energy."),
        ContextComment("The fun friend. 'Fun' is generous. Chaos is more accurate."),
        ContextComment("*suspicious* What are they planning? Something. Definitely something.", 2),
        ContextComment("I don't trust that look. Good things don't follow that look.", 2),
    ],
    "mysterious": [
        ContextComment("*suspicious* ...why are they like that? So... mysterious."),
        ContextComment("The cryptic one. I never know what they're thinking."),
        ContextComment("Mysterious friend appeared. Dramatically, probably."),
        ContextComment("What secrets do you hold? ...it's probably nothing. Or everything.", 2),
        ContextComment("*leans in* Tell me something I don't know. Actually don't. Maybe.", 2),
    ],
    "generous": [
        ContextComment("*perks up* The gift-giver is here! I mean... hello. Friend."),
        ContextComment("Generous friend! My favorite kind of friend! ...don't tell the others."),
        ContextComment("Oh look who it is. The nice one. Suspiciously nice."),
        ContextComment("*innocently* Gifts? Did someone say gifts? I didn't. Maybe.", 2),
        ContextComment("The giving tree, but a duck. Best kind of friend.", 2),
    ],
    "foodie": [
        ContextComment("*interested* The food one. My kind of duck."),
        ContextComment("Foodie friend! Finally, someone who understands priorities."),
        ContextComment("They always know where the good crumbs are. Essential ally."),
        ContextComment("*stomach growls on cue* What? Coincidence.", 2),
        ContextComment("Food friend. The most important kind of friend.", 2),
    ],
    "athletic": [
        ContextComment("*exhausted just watching* The energetic one. Great."),
        ContextComment("Athlete friend. I'll just... be here. Not moving."),
        ContextComment("So much energy. Where does it come from? Where does it go?"),
        ContextComment("They want me to exercise. I want them to reconsider.", 2),
        ContextComment("*pretends to stretch* See? I'm athletic too. Done now.", 2),
    ],
}


# =============================================================================
# TIME OF DAY COMMENTS
# =============================================================================

TIME_COMMENTS: Dict[str, List[ContextComment]] = {
    "dawn": [
        ContextComment("*yawning* Why is the sun awake before me? Rude."),
        ContextComment("Morning. The world is way too bright right now."),
        ContextComment("*blinks at sunrise* I didn't agree to this."),
        ContextComment("Dawn. Nature's alarm clock. Unsubscribe.", 2),
    ],
    "morning": [
        ContextComment("Morning. Coffee? Tea? Bread? ...mostly bread."),
        ContextComment("*stretching* Okay. I'm awake. Allegedly."),
        ContextComment("Good morning. Or is it? We'll see."),
        ContextComment("Morning routine: wake up, exist, question existence.", 2),
    ],
    "noon": [
        ContextComment("Noon. Peak standing around time."),
        ContextComment("*squinting at sun* You're very... up there."),
        ContextComment("Middle of the day. Maximum vibes."),
        ContextComment("High noon. Time for a showdown. Or a nap. Probably nap.", 2),
    ],
    "afternoon": [
        ContextComment("Afternoon. The 'everything is fine' part of the day."),
        ContextComment("*relaxing* Post-noon vibes. Quality time."),
        ContextComment("Afternoon slump. I'm going to lean into it."),
        ContextComment("Prime contemplation hours. I'm contemplating bread.", 2),
    ],
    "evening": [
        ContextComment("Evening approaches. Time to be dramatic about it."),
        ContextComment("*watching sunset* ...okay, that's actually nice."),
        ContextComment("The day is ending. I have no regrets. Some regrets."),
        ContextComment("Golden hour. I'm extra handsome right now.", 2),
    ],
    "night": [
        ContextComment("*looking at stars* ...what's up there? Probably nothing. Probably."),
        ContextComment("Night time. The void stares back. I stare harder."),
        ContextComment("*yawning* Sleep soon. Or not. We'll see."),
        ContextComment("The moon is judging me now. Great. Switch shifts.", 2),
    ],
}


# =============================================================================
# IDLE CHATTER - Random comments when nothing is happening
# =============================================================================

IDLE_COMMENTS: List[ContextComment] = [
    ContextComment("*standing* This is me. Standing. Professional standing."),
    ContextComment("*staring into distance* I'm not spacing out. I'm thinking. Deeply."),
    ContextComment("*quack* ...don't know why I did that."),
    ContextComment("*preening* Maintenance. Very important."),
    ContextComment("*looking around* Something might happen. Any moment now."),
    ContextComment("*existential pause* ...anyway."),
    ContextComment("I wonder what bread is doing right now."),
    ContextComment("*waddles in place* Cardio. Sort of."),
    ContextComment("Just duck things. You wouldn't understand."),
    ContextComment("*tilts head* Did you hear that? ...probably nothing."),
    ContextComment("Standing here like it's my job. It is my job.", 2),
    ContextComment("If I stand still enough, maybe I become furniture.", 2),
    ContextComment("I'm not doing nothing. I'm actively choosing to not do things.", 2),
    ContextComment("The floor is particularly floor-like today.", 2),
    ContextComment("*contemplates existence* ...nah.", 2),
    ContextComment("I should do something. I won't, but I should.", 3),
    ContextComment("In an alternate universe, I'm doing something productive.", 3),
    ContextComment("Did you know ducks can see more colors than you? Flex.", 3),
]


class ContextualDialogueSystem:
    """System for generating contextual comments about the world."""
    
    def __init__(self):
        self.last_weather_comment: Optional[str] = None
        self.last_event_comment: Optional[str] = None
        self.last_visitor_comment: Optional[str] = None
        self.last_time_comment: Optional[str] = None
        self.last_idle_comment: Optional[str] = None
        self.comment_cooldowns: Dict[str, float] = {}
    
    def _pick_comment(self, comments: List[ContextComment], last_text: Optional[str] = None) -> str:
        """Pick a comment, weighted by rarity, avoiding repeats."""
        # Filter out the last one
        available = [c for c in comments if c.text != last_text]
        if not available:
            available = comments
        
        # Weight by inverse rarity (common = more likely)
        weighted = []
        for comment in available:
            weight = 4 - comment.rarity  # rarity 1 = weight 3, rarity 3 = weight 1
            weighted.extend([comment] * weight)
        
        return random.choice(weighted).text
    
    def get_weather_comment(self, weather_type: str) -> Optional[str]:
        """Get a comment about the current weather."""
        weather_key = weather_type.lower()
        comments = WEATHER_COMMENTS.get(weather_key)
        if not comments:
            return None
        
        text = self._pick_comment(comments, self.last_weather_comment)
        self.last_weather_comment = text
        return text
    
    def get_event_comment(self, event_id: str) -> Optional[str]:
        """Get a comment about a specific event."""
        comments = EVENT_COMMENTS.get(event_id)
        if not comments:
            return None
        
        text = self._pick_comment(comments, self.last_event_comment)
        self.last_event_comment = text
        return text
    
    def get_visitor_comment(self, personality: str) -> Optional[str]:
        """Get a comment about a visitor based on their personality."""
        personality_key = personality.lower()
        comments = VISITOR_COMMENTS.get(personality_key)
        if not comments:
            return None
        
        text = self._pick_comment(comments, self.last_visitor_comment)
        self.last_visitor_comment = text
        return text
    
    def get_time_comment(self, time_of_day: str) -> Optional[str]:
        """Get a comment about the time of day."""
        time_key = time_of_day.lower()
        comments = TIME_COMMENTS.get(time_key)
        if not comments:
            return None
        
        text = self._pick_comment(comments, self.last_time_comment)
        self.last_time_comment = text
        return text
    
    def get_idle_comment(self) -> str:
        """Get a random idle comment."""
        text = self._pick_comment(IDLE_COMMENTS, self.last_idle_comment)
        self.last_idle_comment = text
        return text
    
    def get_contextual_comment(self, weather: Optional[str] = None, 
                               event: Optional[str] = None,
                               visitor_personality: Optional[str] = None,
                               time_of_day: Optional[str] = None) -> Optional[str]:
        """Get a contextual comment based on current game state.
        
        Prioritizes: visitor > event > weather > time > idle
        """
        # Check for visitor first (most specific)
        if visitor_personality:
            comment = self.get_visitor_comment(visitor_personality)
            if comment:
                return comment
        
        # Then check for event
        if event:
            comment = self.get_event_comment(event)
            if comment:
                return comment
        
        # Then weather
        if weather:
            comment = self.get_weather_comment(weather)
            if comment:
                return comment
        
        # Then time of day
        if time_of_day:
            comment = self.get_time_comment(time_of_day)
            if comment:
                return comment
        
        # Fall back to idle
        return self.get_idle_comment()


# Global instance
contextual_dialogue = ContextualDialogueSystem()
