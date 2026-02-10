"""
Visitor Dialogue System - Comprehensive dialogue trees for duck friends.
Each personality has dialogue for each friendship level that progresses naturally.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


# =============================================================================
# VISITOR WEATHER COMMENTS - Weather-specific comments by personality
# =============================================================================

VISITOR_WEATHER_COMMENTS: Dict[str, Dict[str, List[str]]] = {
    "adventurous": {
        "sunny": [
            "Perfect weather for an adventure! The sun is calling!",
            "*checks compass* Excellent conditions for exploration!",
            "Sunny skies mean new trails to discover!",
            "I mapped three new routes just this morning! The visibility is INCREDIBLE!",
            "*shielding eyes* I can see all the way to the horizon! Let's find out what's there!",
            "The sun is nature's green light! Full speed ahead!",
            "Every great expedition starts with a day like THIS!",
            "*packing supplies* Daylight's burning! Adventure waits for no duck!",
        ],
        "rainy": [
            "Rain never stopped a TRUE adventurer! Let's go!",
            "I once crossed a monsoon. This is nothing!",
            "*excited* PUDDLES! Nature's obstacle course!",
            "Wet terrain means new challenges! My favorite kind!",
            "*adjusts rain gear* The jungle explorers didn't have HALF this equipment!",
            "Rain reveals hidden streams and waterfalls! Quick, let's find them!",
            "The best discoveries happen when most ducks stay home!",
            "*consulting waterproof map* There's a cave system nearby. Perfect shelter AND exploration!",
        ],
        "stormy": [
            "*eyes wide* Now THIS is weather! EXCITING!",
            "Storms make everything more dramatic!",
            "*watches lightning* The universe is putting on a SHOW!",
            "I've navigated worse! This barely rates a three on my danger scale!",
            "*bracing against wind* This is what separates adventurers from tourists!",
            "Thunder is just the world telling us to pay ATTENTION!",
            "The most legendary tales always start with 'it was a dark and stormy day'!",
        ],
        "snowy": [
            "Snow means winter expeditions! I'm SO ready!",
            "I've trekked through worse blizzards. This is cozy!",
            "*catching snowflakes* Perfect for tracking!",
            "Fresh snow means uncharted territory! Nobody's been here yet!",
            "*checking gear* Snow boots, check! Compass, check! Sense of wonder, DOUBLE check!",
            "You can read the whole forest in fresh snow. Every creature leaves a story!",
            "Arctic expeditions are the ULTIMATE test! I'm ready!",
        ],
        "windy": [
            "The wind guides my adventures! Which way, wind?",
            "*feathers blown back* FREEDOM feels like this!",
            "Wind at our backs! Let's GO!",
            "Ancient navigators followed the wind to new continents! We should too!",
            "*spreading wings* If I just angle these right... I could SOAR!",
            "The wind carries scents from faraway lands! Can you smell the adventure?!",
            "Headwinds build CHARACTER! Tailwinds build SPEED! Both are great!",
        ],
        "foggy": [
            "Mysterious! Could be ANYTHING out there!",
            "Fog makes everything feel like a quest!",
            "*squinting* Adventure awaits beyond the mist!",
            "You never know what's ten feet ahead in fog. That's the THRILL!",
            "*navigating by sound* True explorers don't need to SEE to find their way!",
            "Some of my best discoveries happened when I couldn't see a thing!",
            "The fog is just the world wrapping itself in mystery! Let's unwrap it!",
        ],
    },
    "scholarly": {
        "sunny": [
            "Optimal photosynthetic conditions. Fascinating.",
            "The sun provides excellent reading light!",
            "*adjusts glasses* Clear skies. Perfect for observations.",
            "The solar irradiance today must be approximately 1000 watts per square meter. Splendid!",
            "UV index is moderate. I recommend SPF 30 and a good book.",
            "*consulting almanac* The sun reaches its zenith at precisely 12:47 today.",
            "Fun fact: sunlight takes 8 minutes and 20 seconds to reach us. We're literally seeing the past!",
        ],
        "rainy": [
            "Rain increases ambient humidity by... *calculates*",
            "Did you know rain forms around dust particles?",
            "*taking notes* Precipitation patterns are remarkable!",
            "The average raindrop falls at 14 miles per hour. I measured.",
            "*opens weather journal* This brings our monthly rainfall total to... significant.",
            "Petrichor! That's the scientific name for the smell of rain on dry earth. Glorious.",
            "Rainfall frequency correlates inversely with barometric pressure. As expected.",
            "*collecting sample* The pH of this rainwater would make an excellent study!",
        ],
        "stormy": [
            "The electrical potential in those clouds is IMMENSE!",
            "Storm systems are nature's most complex phenomena!",
            "*fascinated* Each lightning bolt is 30,000 kelvin!",
            "The cumulonimbus formations are textbook perfect! I should photograph these!",
            "*counting seconds after flash* The storm front is 2.3 kilometers away. Approaching.",
            "Thunder is merely rapid air expansion. Still, the acoustics are remarkable!",
            "Did you know a single thunderstorm can release more energy than a nuclear weapon?",
        ],
        "snowy": [
            "Each snowflake IS unique. I've verified this.",
            "Snow crystals form in fascinating hexagonal patterns!",
            "*examining snowflake* Six-fold symmetry! Beautiful!",
            "Fresh snow has an albedo of 0.9. It reflects 90% of sunlight! Remarkable!",
            "*recording temperature* At this rate of accumulation, we'll have 12 centimeters by evening.",
            "The dendritic crystal structure depends on precise temperature and humidity conditions.",
            "Snow is an excellent thermal insulator. Igloos work because of this principle!",
        ],
        "windy": [
            "Wind is simply differential air pressure. Elegantly simple.",
            "The Coriolis effect influences this breeze!",
            "*hair blown* Aerodynamics in action!",
            "I estimate wind speed at approximately 25 kilometers per hour. Beaufort scale 4.",
            "*taking anemometer readings* Gusting to 35! Fascinating variance in the data!",
            "Wind patterns at this latitude follow predictable seasonal models. Mostly.",
            "The Bernoulli principle is beautifully demonstrated by these gusts!",
        ],
        "foggy": [
            "Fog is merely ground-level stratus clouds. Technically.",
            "Visibility reduced to approximately... *squints* ...limited.",
            "Water vapor condensation. Quite poetic, actually.",
            "Advection fog forms when warm air passes over a cool surface. Elementary meteorology!",
            "*checking hygrometer* Relative humidity: 100%. As one would expect.",
            "The dew point and air temperature have converged. Textbook fog conditions!",
            "Fog droplets are typically 1 to 10 micrometers in diameter. Invisible individually, yet...",
        ],
    },
    "artistic": {
        "sunny": [
            "*gestures dramatically* The LIGHT! The SHADOWS! Art!",
            "Golden rays inspire golden creativity!",
            "The sun paints everything in warm tones!",
            "The chiaroscuro today is absolutely DIVINE! Renaissance masters wept for this light!",
            "*holding up frame fingers* Every direction I look is a MASTERPIECE!",
            "I could paint for HOURS in this luminance! The warmth! The radiance!",
            "Sunlight through leaves creates the most EXQUISITE dappled patterns!",
        ],
        "rainy": [
            "Rain creates the most MELANCHOLIC aesthetic!",
            "*spreading wings* The drama! The romance!",
            "Everything glistens! Nature's rhinestones!",
            "The way droplets catch the light... every surface becomes a CANVAS!",
            "*sketching furiously* The reflections in the puddles! Upside-down worlds! INSPIRED!",
            "Rain is liquid poetry falling from the sky! I'm WEEPING with beauty!",
            "The grey palette! So subtle! So NUANCED! Most underappreciate grey!",
        ],
        "stormy": [
            "DRAMATIC! INTENSE! INSPIRED!",
            "*poses in wind* The perfect backdrop for art!",
            "Such POWERFUL energy! I must create!",
            "The contrast of dark clouds and lightning! It's CHIAROSCURO from the HEAVENS!",
            "*arms spread wide* The raw EMOTION! The FURY! I feel it in my SOUL!",
            "Turner painted storms. Constable painted storms. I UNDERSTAND them now!",
            "Every thunderclap is a PERCUSSION performance! The sky is a STAGE!",
        ],
        "snowy": [
            "A blank canvas! The world is ART waiting to happen!",
            "*twirling* Pure white beauty! Pristine!",
            "Snow muffles sound... so peaceful... so inspiring...",
            "The minimalism! White on white with subtle shadows! It's BREATHTAKING!",
            "*catching snowflakes on tongue* Even the TASTE is aesthetic!",
            "Every footprint in fresh snow is an act of CREATION! We are all artists today!",
            "The way snow softens every harsh edge... the world becomes a watercolor!",
        ],
        "windy": [
            "*feathers flowing* I am become SCULPTURE!",
            "The wind creates such dynamic MOVEMENT!",
            "DRAMATIC! The wind is an artist too!",
            "*scarf billowing* THIS is what fashion DREAMS of! Natural dynamism!",
            "The way the wind sculpts the clouds! Impermanent art! EPHEMERAL beauty!",
            "Everything DANCES in the wind! Leaves, grass, feathers! A CHOREOGRAPHY!",
            "Wind is the invisible brushstroke! You can't see it but you feel the EFFECT!",
        ],
        "foggy": [
            "The atmosphere is MOODY! I love it!",
            "*mysterious pose* Ethereal. Haunting. Perfect.",
            "Fog turns everything into impressionism!",
            "Monet would have SOLD HIS SOUL for this fog! The diffusion! The softness!",
            "*disappearing into mist* I am becoming ONE with the aesthetic!",
            "The world behind a veil of gauze... everything is suggestion and MYSTERY!",
            "Fog reduces the world to shapes and silhouettes. Pure ABSTRACTION!",
        ],
    },
    "playful": {
        "sunny": [
            "YAY! Sunny! Let's play EVERYTHING!",
            "*bouncing* The sun wants us to have FUN!",
            "Perfect day for shenanigans!",
            "Tag! You're it! No wait, the SUN is it! Everyone's it!",
            "*doing cartwheels* Sunny days are CARTWHEEL days! Wheee!",
            "I brought a frisbee AND a ball AND a kite! What first?! WHAT FIRST?!",
            "The ground is lava! Quick, get on the grass! Wait, that's also lava! EVERYTHING IS LAVA!",
        ],
        "rainy": [
            "PUDDLES! PUDDLES EVERYWHERE! *splashing*",
            "Rain is just nature's sprinkler system!",
            "*spinning* SPLASHY SPLASH SPLASH!",
            "Bet I can make a BIGGER splash than you! Ready? CANNONBALL!",
            "*catching raindrops in beak* Blep! Blep! Blep! It's a game!",
            "Mud pies! MUD PIES! Who wants mud pies?! Everyone gets mud pies!",
            "Rain means indoor blanket fort time! I brought the pillows!",
        ],
        "stormy": [
            "*hides* The sky is being LOUD. Make it stop?",
            "Thunder is just sky farts. Right? RIGHT?",
            "*nervous but excited* SCARY but also COOL!",
            "Let's count between the flash and the boom! One duck, two duck, three duck—BOOM!",
            "*hiding under wing* I'm not scared! I'm just... practicing being small!",
            "The thunder is the sky playing DRUMS! Not very well though!",
            "Quick! Build a blanket fort! Fort protects from EVERYTHING!",
        ],
        "snowy": [
            "SNOWBALL FIGHT! I mean... SNOWBALL CUDDLE!",
            "*diving into snow* I'm a snow duck now!",
            "Let's make snow angels! Or snow DUCKS!",
            "*rolling giant snowball* This is gonna be the BIGGEST snowduck EVER!",
            "Brain freeze from eating snow! Worth it! *eats more snow*",
            "Belly slide down the hill! WHEEEEE! Again! AGAIN!",
            "*flopping in snow* I'm making a snow duck angel! It has WINGS!",
        ],
        "windy": [
            "*spreads wings* I can ALMOST fly! Almost!",
            "WHEEEEE! The wind is playing with me!",
            "*spinning* I'm a feathery windmill!",
            "Let's play who can lean the farthest into the wind without falling! I'll go first!",
            "*chasing hat* Come back! That's MY hat! This is the best game EVER!",
            "If I run fast enough WITH the wind, I'm basically SUPERSONIC!",
            "The wind stole my feather! Come back, feather! *chasing* This is actually really fun!",
        ],
        "foggy": [
            "Spooky! Let's play hide and seek!",
            "*disappears into fog* Can you find me??",
            "The fog is trying to play! It's hiding everything!",
            "BOO! Did I scare you?! I scared MYSELF! This fog is GREAT!",
            "*whispering* We're basically invisible! Let's sneak up on EVERYONE!",
            "Marco! ...Marco? ...Is anyone there? MARCO! This game is INTENSE!",
            "I just walked in a circle THREE times and it was fun EVERY time!",
        ],
    },
    "mysterious": {
        "sunny": [
            "The sun reveals what darkness conceals...",
            "*squints* Too bright. I prefer shadows.",
            "Even light casts darkness somewhere...",
            "Bright days make the deepest shadows. Ironic, isn't it?",
            "*retreating to shade* The sun exposes too much. Some things should stay hidden.",
            "Sunshine is a distraction. The real truths hide in the glare.",
            "They celebrate the light... but forget what crawls beneath it.",
        ],
        "rainy": [
            "The sky weeps. I understand.",
            "Rain washes away secrets... or hides them.",
            "*gazes at puddles* Reflections of other worlds...",
            "Every raindrop is a tiny mirror. Be careful what you let them see.",
            "*standing motionless in rain* This is the weather my soul makes.",
            "The rain knows things. Listen closely and it will tell you.",
            "Footprints vanish in the rain. Convenient for some of us.",
        ],
        "stormy": [
            "The storm and I have an... understanding.",
            "*unfazed by thunder* We've met before.",
            "Such weather reveals true nature...",
            "Lightning illuminates for only a moment. What you see in that flash... is the truth.",
            "*standing in the storm calmly* Chaos is just another form of order, you know.",
            "The thunder speaks in a language older than words. I am fluent.",
            "Some fear the storm. I find it... familiar.",
        ],
        "snowy": [
            "Snow covers all tracks... how convenient.",
            "*watching snowfall* Each flake carries a secret.",
            "The silence of snow... it speaks volumes.",
            "Beneath the white, everything is buried. Forgotten. Almost.",
            "*catching a snowflake* This one traveled a very long way to find you. Why?",
            "The world looks innocent under snow. Looks can be deceiving.",
            "Cold preserves things. Memories. Evidence. Secrets.",
        ],
        "windy": [
            "The wind whispers things... dark things...",
            "*listening* Do you hear it too?",
            "Ancient messages on the breeze...",
            "The wind carries voices from places that no longer exist.",
            "*cloak billowing* Every gust is a ghost passing through.",
            "They say the wind has no master. They are wrong.",
            "Something is shifting. Not just the air. Something deeper.",
        ],
        "foggy": [
            "*emerges from fog* My element.",
            "Fog hides many mysteries. Including me.",
            "The veil between worlds is thin today...",
            "*appearing and disappearing* Now you see me. Now you don't. Now you question everything.",
            "In the fog, distance has no meaning. Neither does time.",
            "Perfect weather for those who prefer not to be... observed.",
            "The fog doesn't hide things. It reveals what was always invisible.",
        ],
    },
    "generous": {
        "sunny": [
            "Sunny days deserve extra gifts!",
            "*handing out treats* The sun smiles, so should we!",
            "Perfect weather for sharing joy!",
            "I packed enough picnic for EVERYONE! Help yourselves!",
            "*distributing sunscreen* Can't have anyone getting burned on my watch!",
            "Sunny days are meant to be shared! Here, have some lemonade!",
            "The sun gives us light freely. I want to be that generous!",
        ],
        "rainy": [
            "I brought extra! In case you got wet!",
            "*offers umbrella* Rain can't dampen generosity!",
            "Here! Something to warm you up!",
            "*distributing towels* I packed twelve. You never know how many you'll need!",
            "Hot cocoa for everyone! I made THREE thermoses!",
            "Take my raincoat! I have a spare! And a spare spare!",
            "Rainy days are when kindness matters MOST! Here, take these cookies!",
        ],
        "stormy": [
            "Stay safe! Here's something to help!",
            "*worried* Do you need anything? I have extras!",
            "Storms mean we stick together!",
            "I brought emergency supplies for everyone! Blankets, snacks, flashlights!",
            "*ushering everyone to shelter* Come in, come in! There's room for all!",
            "Nobody should face a storm alone! I'm here for you!",
            "*handing out candles* Just in case the power goes. I brought forty.",
        ],
        "snowy": [
            "*bundled up* I brought you something warm!",
            "Snow days mean hot cocoa gifts!",
            "Here! To keep you cozy!",
            "*distributing hand-knitted scarves* I made one for everyone! Matching!",
            "I baked warm cookies to share! Snow day treats for ALL!",
            "Take these mittens! I noticed yours were thin! I carry spares!",
            "*handing out hot water bottles* Winter is better when we keep each other warm!",
        ],
        "windy": [
            "*holding onto things* Don't let the gifts blow away!",
            "Windy days need extra cheer!",
            "I brought something stable. Unlike the weather!",
            "*chasing a hat* That was YOUR present! I'll get it back!",
            "I tied ribbons on everything so the gifts wouldn't fly away! Prepared!",
            "Here, hold onto me! We can be each other's anchor!",
            "The wind tried to take your gift but I held on TIGHT! Here!",
        ],
        "foggy": [
            "Hard to see, but I found you anyway! With gifts!",
            "*emerges from fog* Surprise! It's gift time!",
            "Fog can't hide my generosity!",
            "I followed the sound of your voice! Had to deliver these treats somehow!",
            "*setting up glow sticks* So we can find each other AND the snack table!",
            "Even in fog, the warmth of giving lights the way!",
            "I left a trail of little gifts so everyone can find their way here!",
        ],
    },
    "foodie": {
        "sunny": [
            "Perfect weather for a picnic! Did you bring snacks?",
            "The sun makes everything taste better!",
            "*sniffing* I smell... POSSIBILITIES.",
            "Sunny days mean grilling season! Fire up the barbecue!",
            "*setting up picnic blanket* I brought seven courses. For a SNACK.",
            "The warmth really brings out the flavor in fresh berries! I brought twelve kinds!",
            "Ice cream weather! I mean, it's ALWAYS ice cream weather, but especially now!",
        ],
        "rainy": [
            "Rain means comfort food time!",
            "Wet weather, warm snacks. Perfect combo!",
            "*excited* Raindrops make everything taste fresh!",
            "I've got stew going at home! The rain inspired me at 5 AM!",
            "*pulling out thermos* Mushroom soup! Rain makes the best mushrooms!",
            "The patter of rain on the window while bread bakes... perfection.",
            "Rainy days demand dumplings. This is not negotiable.",
        ],
        "stormy": [
            "Storm baking! The BEST kind of baking!",
            "*cozy* Perfect weather for hot soup!",
            "Thunder? That's the universe's tummy rumbling!",
            "Lightning crackle reminds me of caramelizing sugar! Now I'm HUNGRY!",
            "*stress baking* I've already made three pies! The storm makes me PRODUCTIVE!",
            "Nothing beats eating chili during a thunderstorm. It's SCIENCE.",
            "The power might go out but I already cooked EVERYTHING. Prepared!",
        ],
        "snowy": [
            "Cold weather means hot food! PERFECT!",
            "*making snow cones* Nature provides!",
            "Winter is soup season. All soup. Always.",
            "*stirring enormous pot* Fondue weather! Everything gets dipped in CHEESE!",
            "Fresh snow makes the best shaved ice! Just add syrup! I brought fourteen flavors!",
            "My hot cocoa recipe has seven secret ingredients. The eighth is LOVE.",
            "Snow day baking marathon! Cookies, bread, cakes, MORE cookies!",
        ],
        "windy": [
            "Wind-blown snacks are still snacks!",
            "*chasing leaves* Wait, those aren't food!",
            "The wind brings new smells! New FLAVORS!",
            "*nose twitching* The wind is carrying the smell of someone's bakery three blocks away!",
            "Hard to eat a sandwich in this wind but I WILL NOT BE DEFEATED!",
            "The wind is basically a convection oven! Nature wants us to COOK!",
            "*clutching picnic basket* The wind wants my food but it CAN'T HAVE IT!",
        ],
        "foggy": [
            "Can't see but I can SMELL everything!",
            "Misty mornings, perfect breakfast vibes!",
            "*sniffing* My nose sees through fog!",
            "Fog mornings call for warm pastries and strong coffee. I brought BOTH.",
            "*navigating by smell* The bakery is THAT way. My nose is never wrong!",
            "This fog smells like dew and possibility and... is someone grilling?!",
            "My nose works BETTER in humid air! I can smell dinner from a mile away!",
        ],
    },
    "athletic": {
        "sunny": [
            "PERFECT training weather! Let's GO!",
            "*stretching* The sun energizes my workout!",
            "Peak conditions for peak performance!",
            "Clear skies, warm muscles, ZERO excuses! Drop and give me twenty!",
            "*doing lunges* Vitamin D AND gains! Today is a GIFT!",
            "My personal best was set on a day JUST like this! Let's break it!",
            "The sun is my spotter today! Light reps, heavy motivation!",
        ],
        "rainy": [
            "Rain is just nature's sweat! Keep pushing!",
            "*running in rain* REFRESHING!",
            "Wet feathers mean harder workout! GAINS!",
            "Rain is just the sky doing its OWN workout! Solidarity!",
            "*doing burpees in mud* Functional training! This is what the pros do!",
            "Every elite athlete trains in the rain! It builds MENTAL TOUGHNESS!",
            "Slip resistance training! Working muscles you didn't know you HAD!",
        ],
        "stormy": [
            "*pumped* EXTREME weather! EXTREME training!",
            "Storm drills! Nature's intensity training!",
            "Lightning reflexes! Get it? LIGHTNING?",
            "Thunder is my HYPE MUSIC! Each boom is a new SET!",
            "*doing pushups* The storm can't train harder than ME!",
            "This is basically a CrossFit workout designed by NATURE!",
            "Storm sprints! Dodge the rain! Weave through the wind! AGILITY!",
        ],
        "snowy": [
            "Cold weather burns MORE calories!",
            "*running in snow* RESISTANCE training!",
            "Snow sports time! Race you to that drift!",
            "Shivering burns 400 calories per hour! Just STANDING here is a workout!",
            "*doing snow lunges* Every step is LEG DAY! Nature's leg press!",
            "Snowshoeing works your glutes, quads, AND core! Triple threat weather!",
            "Ice bath weather! Recovery AND training at the SAME TIME!",
        ],
        "windy": [
            "*running into wind* CARDIO INTENSIFIES!",
            "Wind resistance! Free gym membership!",
            "The wind is my sparring partner today!",
            "Running into the wind adds 30% more resistance! FREE GAINS!",
            "*leaning forward at 45 degrees* Core workout just from STANDING!",
            "Sprint WITH the wind for speed work, AGAINST it for strength! Perfect intervals!",
            "The wind is basically an invisible resistance band! FULL BODY workout!",
        ],
        "foggy": [
            "Training in limited visibility! SKILL BUILDER!",
            "*jogging* Can't see? Run ANYWAY!",
            "Fog is just the world making training harder!",
            "Reduced visibility means heightened REFLEXES! Elite training conditions!",
            "*doing jumping jacks* My body doesn't need to SEE to get SWOLE!",
            "Fog running builds mental discipline! You can't see the finish line but you BELIEVE!",
            "Proprioception training! When you can't see, your body learns to FEEL the workout!",
        ],
    },
}


# Import base types from dialogue_base to avoid circular imports
from dialogue.dialogue_base import ConversationPhase, DialogueLine, DIALOGUE_TREES


@dataclass 
class ConversationState:
    """Tracks the state of the current conversation."""
    phase: ConversationPhase = ConversationPhase.GREETING
    lines_said: List[str] = field(default_factory=list)
    topics_discussed: List[str] = field(default_factory=list)
    dialogue_index: int = 0
    visit_count: int = 1
    

# Friendship level order for comparisons
FRIENDSHIP_ORDER = ["stranger", "acquaintance", "friend", "close_friend", "best_friend"]


def friendship_meets_minimum(current: str, minimum: str) -> bool:
    """Check if current friendship level meets the minimum requirement."""
    current_idx = FRIENDSHIP_ORDER.index(current) if current in FRIENDSHIP_ORDER else 0
    min_idx = FRIENDSHIP_ORDER.index(minimum) if minimum in FRIENDSHIP_ORDER else 0
    return current_idx >= min_idx


class VisitorDialogueManager:
    """Manages dialogue for a visitor during their visit."""
    
    def __init__(self):
        self.state = ConversationState()
        self.personality: str = "adventurous"
        self.friendship_level: str = "stranger"
        self.friend_name: str = "Friend"
        self.unlocked_topics: set = set()
        self.visit_number: int = 1
        # NEW: Memory for tracking conversation history
        self.conversation_topics: List[str] = []  # What we've discussed before
        self.shared_experiences: List[str] = []  # What we've done together
        self.last_conversation_summary: str = ""  # What we talked about last time
        
    def start_visit(self, personality: str, friendship_level: str, 
                    friend_name: str, visit_number: int, unlocked_topics: set = None,
                    conversation_topics: List[str] = None, shared_experiences: List[str] = None,
                    last_conversation_summary: str = ""):
        """Initialize for a new visit."""
        self.state = ConversationState()
        self.state.phase = ConversationPhase.GREETING
        self.personality = personality.lower()
        self.friendship_level = friendship_level.lower().replace(" ", "_")
        self.friend_name = friend_name
        self.visit_number = visit_number
        self.unlocked_topics = unlocked_topics or set()
        self.state.visit_count = visit_number
        # Store memory
        self.conversation_topics = conversation_topics or []
        self.shared_experiences = shared_experiences or []
        self.last_conversation_summary = last_conversation_summary
        
    def get_next_dialogue(self, duck_name: str = "friend") -> Optional[str]:
        """Get the next line of dialogue based on current state."""
        dialogue_tree = DIALOGUE_TREES.get(self.personality, {})

        # Special handling for greetings when we've met before
        # Only try returning greeting if we haven't said ANY lines yet (first call)
        if self.state.phase == ConversationPhase.GREETING and self.visit_number > 1 and len(self.state.lines_said) == 0:
            returning_greeting = self._get_returning_greeting(duck_name)
            if returning_greeting:
                self.state.lines_said.append(returning_greeting)
                # Advance past greeting phase after returning greeting
                self.state.phase = ConversationPhase.OPENING
                return returning_greeting

        phase_dialogue = dialogue_tree.get(self.state.phase.value, [])
        
        # Filter to lines we can say
        available = []
        for line in phase_dialogue:
            # Check friendship requirement
            if not friendship_meets_minimum(self.friendship_level, line.friendship_min):
                continue
            # Check if already said this visit
            if line.once_per_visit and line.text in self.state.lines_said:
                continue
            # Check topic requirements
            if line.requires_topic and line.requires_topic not in self.unlocked_topics:
                continue
            available.append(line)
        
        if not available:
            # Move to next phase
            return self._advance_phase(duck_name)
        
        # Pick a line that hasn't been said yet in this visit
        unsaid = [l for l in available if l.text not in self.state.lines_said]
        if unsaid:
            line = random.choice(unsaid)
        else:
            # All lines in this phase have been said at least once - advance to next phase
            return self._advance_phase(duck_name)
        
        # Record that we said it
        self.state.lines_said.append(line.text)

        # Handle topic unlocking
        if line.unlocks_topic:
            self.unlocked_topics.add(line.unlocks_topic)

        # After a greeting, automatically advance to opening phase
        # This ensures exactly ONE greeting per visit, then natural conversation flow
        if self.state.phase == ConversationPhase.GREETING:
            self.state.phase = ConversationPhase.OPENING

        # Format and return
        text = line.text.format(duck=duck_name, name=self.friend_name)
        return f"{self.friend_name}: {text}"
    
    def _advance_phase(self, duck_name: str) -> Optional[str]:
        """Move to the next conversation phase."""
        phase_order = [
            ConversationPhase.GREETING,
            ConversationPhase.OPENING,
            ConversationPhase.MAIN,
            ConversationPhase.STORY,
            ConversationPhase.PERSONAL,
            ConversationPhase.ACTIVITY,
            ConversationPhase.CLOSING,
            ConversationPhase.FAREWELL,
        ]

        current_idx = phase_order.index(self.state.phase)

        # Find next valid phase (skip phases that require higher friendship)
        next_idx = current_idx + 1
        while next_idx < len(phase_order):
            next_phase = phase_order[next_idx]

            # Check if this phase should be skipped based on friendship level
            if next_phase == ConversationPhase.STORY:
                if not friendship_meets_minimum(self.friendship_level, "acquaintance"):
                    next_idx += 1
                    continue
            elif next_phase == ConversationPhase.PERSONAL:
                if not friendship_meets_minimum(self.friendship_level, "friend"):
                    next_idx += 1
                    continue

            # Valid phase found
            break

        if next_idx >= len(phase_order):
            return None  # Conversation over

        self.state.phase = phase_order[next_idx]
        self.state.dialogue_index = 0

        # Get first line of new phase
        return self.get_next_dialogue(duck_name)
    
    def is_conversation_over(self) -> bool:
        """Check if the conversation has ended."""
        return self.state.phase == ConversationPhase.FAREWELL and len(self.state.lines_said) > 5
    
    def _get_returning_greeting(self, duck_name: str) -> Optional[str]:
        """Get a special greeting for returning visitors that references past visits."""
        import random
        
        # Only use this sometimes to add variety
        if random.random() > 0.7:
            return None
        
        greetings = []
        
        # Reference shared experiences
        if self.shared_experiences:
            recent_exp = self.shared_experiences[-1] if self.shared_experiences else None
            exp_greetings = {
                "adventurous": [
                    f"*arrives* {duck_name}! Remember when we {recent_exp}? Still thinking about that.",
                    f"Back again! That {recent_exp} thing we did... I've told everyone.",
                    f"*waves* {duck_name}! So about that {recent_exp}... any more adventures planned?",
                ],
                "scholarly": [
                    f"*adjusts glasses* Ah, {duck_name}! I've been analyzing our {recent_exp} experience.",
                    f"{duck_name}! I documented everything from when we {recent_exp}. Fascinating data.",
                    f"*opens notebook* Our {recent_exp}... I have follow-up questions.",
                ],
                "artistic": [
                    f"*twirls* {duck_name}! That {recent_exp}... it INSPIRED me!",
                    f"There you are! I painted a mural about when we {recent_exp}.",
                    f"*gestures dramatically* {duck_name}! Our {recent_exp} was pure art!",
                ],
                "playful": [
                    f"*bounces* {duck_name}! {duck_name}! That {recent_exp} was SO FUN!",
                    f"HI AGAIN! Remember {recent_exp}? Let's do that AGAIN!",
                    f"*giggles* Our {recent_exp}... best day EVER! Well, second best. Today could be better!",
                ],
                "mysterious": [
                    f"*appears* {duck_name}... The stars aligned again. Like when we {recent_exp}...",
                    f"Our {recent_exp}... the spirits still speak of it.",
                    f"*cryptic nod* Fate brought me back. Perhaps to recreate our {recent_exp}...",
                ],
                "generous": [
                    f"*hugs* {duck_name}! I've thought about our {recent_exp} every day!",
                    f"There's my favorite friend! That {recent_exp}... I brought something to celebrate!",
                    f"*beams* Remember our {recent_exp}? Made me so happy!",
                ],
                "foodie": [
                    f"*sniffs* {duck_name}! That {recent_exp}... but more importantly, what's for lunch?",
                    f"Back for more! That {recent_exp} worked up quite an appetite.",
                    f"*belly rumbles* {duck_name}! After that {recent_exp}, I dreamed about food here.",
                ],
                "athletic": [
                    f"*jogs over* {duck_name}! Ready to top our {recent_exp}?",
                    f"Champion! That {recent_exp}... let's go bigger!",
                    f"*stretches* Our {recent_exp}... good training. Let's level up!",
                ],
            }
            if self.personality in exp_greetings and recent_exp:
                greetings.extend(exp_greetings[self.personality])
        
        # Reference visit count
        if self.visit_number > 3:
            count_greetings = {
                "adventurous": [
                    f"*arrives* Visit number {self.visit_number}. I've been counting. Don't judge me, {duck_name}.",
                    f"{duck_name}! I keep coming back. This place is on all my maps now.",
                ],
                "scholarly": [
                    f"*adjusts glasses* Visit {self.visit_number}, {duck_name}. I'm collecting data.",
                    f"{duck_name}! My studies bring me back. You're a fascinating subject.",
                ],
                "artistic": [
                    f"*dramatically* {duck_name}! My muse calls me back again!",
                    f"Visit {self.visit_number}! Each one more inspiring than the last!",
                ],
                "playful": [
                    f"*spins* {duck_name}! I missed you SO MUCH! Again!",
                    f"HIII! I can't stay away! This is too fun!",
                ],
                "mysterious": [
                    f"*appears* We meet again, {duck_name}. As foretold.",
                    f"The threads of fate keep weaving us together...",
                ],
                "generous": [
                    f"*waves excitedly* My dear {duck_name}! I couldn't stay away!",
                    f"Back again with gifts! You deserve ALL the visits!",
                ],
                "foodie": [
                    f"*sniffs air* {duck_name}! The crumbs here... I dream about them.",
                    f"I keep coming back. Your pond has the BEST food!",
                ],
                "athletic": [
                    f"*runs in* Training partner! Ready for round {self.visit_number}?",
                    f"{duck_name}! Our workouts are the highlight of my week!",
                ],
            }
            if self.personality in count_greetings:
                greetings.extend(count_greetings[self.personality])
        
        # Pick one if we have any
        if greetings:
            text = random.choice(greetings)
            return f"{self.friend_name}: {text}"
        
        return None
    
    def get_weather_comment(self, weather_type: str) -> Optional[str]:
        """Get a weather-specific comment based on personality and current weather."""
        if not weather_type:
            return None
        
        # Normalize weather type to match our comment keys
        weather_key = weather_type.lower()
        
        # Map specific weather types to broader categories for comments
        weather_mapping = {
            # Rain variants
            "drizzle": "rainy",
            "heavy_rain": "rainy", 
            "spring_showers": "rainy",
            "thunderstorm": "stormy",
            "summer_storm": "stormy",
            "storm": "stormy",
            # Snow variants
            "light_snow": "snowy",
            "heavy_snow": "snowy",
            "blizzard": "snowy",
            "snow_flurries": "snowy",
            "frost": "snowy",
            "sleet": "snowy",
            "hail": "stormy",
            "ice_storm": "stormy",
            # Other variants
            "partly_cloudy": "sunny",
            "cloudy": "foggy",
            "overcast": "foggy",
            "misty": "foggy",
            "breezy": "windy",
            "leaf_storm": "windy",
            "warm_breeze": "sunny",
            "crisp": "sunny",
            "golden_hour": "sunny",
            "perfect_day": "sunny",
            "balmy_evening": "sunny",
            "scorching": "sunny",
            "heat_wave": "sunny",
            "humid": "sunny",
            "muggy": "sunny",
            "dewy_morning": "foggy",
            "pollen_drift": "windy",
            "aurora": "snowy",
            "meteor_shower": "sunny",
            "double_rainbow": "rainy",
            "rainbow": "rainy",
        }
        
        # Get the mapped key or use the original
        mapped_key = weather_mapping.get(weather_key, weather_key)
        
        # Get personality comments
        personality_comments = VISITOR_WEATHER_COMMENTS.get(self.personality, {})
        weather_comments = personality_comments.get(mapped_key, [])
        
        if weather_comments:
            comment = random.choice(weather_comments)
            return f"{self.friend_name}: {comment}"
        
        return None
    
    def get_farewell(self, duck_name: str) -> str:
        """Get a farewell message."""
        self.state.phase = ConversationPhase.FAREWELL
        return self.get_next_dialogue(duck_name) or f"{self.friend_name}: Bye, {duck_name}!"


# ============================================================================
# DIALOGUE TREES BY PERSONALITY
# Each personality has dialogue organized by phase and friendship level
# DIALOGUE_TREES is imported from dialogue_base to avoid circular imports
# ============================================================================

# Import personality-specific dialogue - each file populates DIALOGUE_TREES when imported
from dialogue.dialogue_adventurous import ADVENTUROUS_DIALOGUE
from dialogue.dialogue_scholarly import SCHOLARLY_DIALOGUE
from dialogue.dialogue_artistic import ARTISTIC_DIALOGUE
from dialogue.dialogue_playful import PLAYFUL_DIALOGUE
from dialogue.dialogue_mysterious import MYSTERIOUS_DIALOGUE
from dialogue.dialogue_generous import GENEROUS_DIALOGUE
from dialogue.dialogue_foodie import FOODIE_DIALOGUE
from dialogue.dialogue_athletic import ATHLETIC_DIALOGUE


# Verify all personalities are loaded
def get_available_personalities() -> list:
    """Return list of personalities with dialogue trees."""
    return list(DIALOGUE_TREES.keys())


def count_dialogue_lines(personality: str) -> int:
    """Count total dialogue lines for a personality."""
    if personality not in DIALOGUE_TREES:
        return 0
    tree = DIALOGUE_TREES[personality]
    return sum(len(lines) for lines in tree.values())
