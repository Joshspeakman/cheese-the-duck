"""
Duck Facts and Trivia System - Fun facts about ducks to share with players.
Also includes birthday tracking and special messages.
"""
import random
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass


# Fun duck facts - educational and entertaining
DUCK_FACTS = [
    # Confused origins
    "Cheese once forgot which end of the bread to eat. He still hasn't figured it out.",
    "Cheese got lost in a straight hallway. Twice. The same hallway.",
    "Cheese once tried to fight his own reflection. The reflection won.",
    "Cheese thinks the moon is a very large crumb. No one has corrected him.",
    "Cheese once walked into a glass door, apologized to it, then did it again.",
    
    # Questionable intelligence
    "Cheese has forgotten his own name mid-introduction. Multiple times.",
    "Cheese once spent three hours trying to befriend a statue. He still waves at it.",
    "Cheese believes he's invisible when he closes his eyes.",
    "Cheese once got scared by his own sneeze and hasn't fully recovered.",
    "Cheese tried to swim in a puddle and got confused when it wasn't deep enough.",
    
    # Endearing failures
    "Cheese has walked into the same wall seventeen times. He blames the wall.",
    "Cheese once forgot how to sit down halfway through sitting down.",
    "Cheese tried to intimidate a butterfly. The butterfly was not intimidated.",
    "Cheese gets lost going to places he's been a hundred times. Every. Single. Time.",
    "Cheese once mistook a pinecone for a friend. He named it Gerald.",
    
    # Confused about basic concepts
    "Cheese thinks clouds are just sky bread. He's been disappointed every time.",
    "Cheese believes his reflection is a very rude duck who copies him.",
    "Cheese once tried to fly by just believing really hard. Gravity disagreed.",
    "Cheese has never successfully predicted where his next step will go.",
    "Cheese forgets he can swim. In the middle of swimming. Regularly.",
    
    # Lovable disasters
    "Cheese once chased his own tail for so long he forgot why he started.",
    "Cheese has never successfully caught a bug. The bugs feel bad for him at this point.",
    "Cheese thinks 'Tuesday' is a type of weather.",
    "Cheese regularly walks the wrong direction and calls it 'the scenic route.'",
    "Cheese once forgot what bread was while eating bread.",
    
    # Peak derp energy
    "Cheese has been startled by the same leaf eight days in a row.",
    "Cheese once tried to drink water and forgot how. He eventually remembered.",
    "Cheese thinks he's being sneaky when he waddles loudly while making eye contact.",
    "Cheese has never won a game, but insists he's 'letting everyone else have fun.'",
    "Cheese gets confused by stairs. Not going up them. Just... stairs existing.",
    
    # Cheese-specific mysteries
    "Cheese once forgot mid-quack what he was quacking about.",
    "Cheese thinks naps are a competitive sport. He's undefeated at losing.",
    "Cheese tried to make friends with his own shadow. The shadow left.",
    "Cheese regularly forgets he has wings. And feet. And sometimes a head.",
    "Cheese is the reason 'duck-brained' is an insult. He considers it a compliment.",
    
    # Additional origins (41-55)
    "Cheese was born confused and has maintained that energy ever since.",
    "Cheese once asked a rock for directions. He's still waiting for a response.",
    "Cheese believes he invented waddling. He did not.",
    "Cheese once got his head stuck in a bush. He blamed the bush.",
    "Cheese thinks he's a natural leader. He has never successfully led anything.",
    "Cheese once tried to count to ten. He got to seven and celebrated.",
    "Cheese thinks alphabetical order is just a suggestion.",
    "Cheese once forgot what feet were. While standing.",
    "Cheese believes rain is the sky crying because it misses him.",
    "Cheese once tried to high-five a fish. It went as expected.",
    "Cheese thinks echoes are other ducks agreeing with him.",
    "Cheese once tried to read a book upside down for an hour before giving up.",
    "Cheese believes he speaks fluent human. He does not.",
    "Cheese once asked a tree for its opinion. The tree did not respond.",
    "Cheese thinks gravity is a personal attack against him specifically.",
    
    # More failures (56-75)
    "Cheese has tripped over nothing an estimated 4,000 times.",
    "Cheese once tried to sneak up on a leaf. The leaf saw him coming.",
    "Cheese attempted to build a nest once. It was just a pile.",
    "Cheese once forgot he was eating mid-bite.",
    "Cheese tried to look cool once. He immediately fell over.",
    "Cheese once got startled by his own quack.",
    "Cheese has never successfully completed a thought.",
    "Cheese once tried to wink. Both eyes closed. He called it a success.",
    "Cheese attempted to be mysterious once. He sneezed and ruined it.",
    "Cheese once forgot which way was forward. He was already walking.",
    "Cheese tried to give someone the silent treatment. He forgot after two seconds.",
    "Cheese once got confused by a straight line.",
    "Cheese has never won hide and seek. He always reveals himself.",
    "Cheese once tried to look threatening. He yawned instead.",
    "Cheese forgot he was mad at someone while still being mad at them.",
    "Cheese tried to act natural. He has never looked less natural.",
    "Cheese once forgot he had a beak mid-peck.",
    "Cheese has gotten lost in his own thoughts. Regularly.",
    "Cheese once tried to remember something. He remembered something else.",
    "Cheese has never followed instructions correctly.",
    
    # Basic concept confusion (76-95)
    "Cheese thinks doors are just very polite walls.",
    "Cheese believes wind is just the air showing off.",
    "Cheese once asked why the sky is up. He's still processing the answer.",
    "Cheese thinks shadows are just very flat friends.",
    "Cheese believes puddles are ponds that gave up.",
    "Cheese once tried to understand math. Math won.",
    "Cheese thinks morning is a conspiracy against his naps.",
    "Cheese believes cold is just spicy air.",
    "Cheese once asked where bread comes from. He forgot the answer immediately.",
    "Cheese thinks sleep is just practice for being a rock.",
    "Cheese believes running is just panicked walking.",
    "Cheese once tried to figure out why water is wet. He gave up.",
    "Cheese thinks hunger is his stomach being dramatic.",
    "Cheese believes feathers are just fancy fur.",
    "Cheese once asked if fish know they're wet. No one answered.",
    "Cheese once forgot he was walking and kept walking.",
    "Cheese tried to focus once. It lasted a third of a second.",
    "Cheese once stared at food for so long he forgot he was hungry.",
    "Cheese has never made the same mistake twice. He makes new ones.",
    "Cheese once forgot he was confused and became more confused.",
    
    # Peak derp continued (96-115)
    "Cheese thinks every day is his birthday. It never is.",
    "Cheese once tried to look serious. He started giggling.",
    "Cheese has never remembered a face. Including his own.",
    "Cheese once forgot he was standing still. He was not.",
    "Cheese tried to explain something once. No one understood. Including him.",
    "Cheese has asked the same question three times in one minute.",
    "Cheese once forgot mid-waddle what waddling was.",
    "Cheese thinks waiting is a sport. He's terrible at it.",
    "Cheese once got confused by a straight answer.",
    "Cheese has never successfully looked where he was going.",
    "Cheese once tried to concentrate. He sneezed.",
    "Cheese forgets he's a duck sometimes. He's reminded by quacking.",
    "Cheese once got lost going in a circle.",
    "Cheese tried to have a strategy once. He forgot it immediately.",
    "Cheese has never finished a sentence without getting distrac—",
    "Cheese once panicked because he couldn't see. His eyes were closed.",
    "Cheese thinks he's unpredictable. He's very predictable.",
    "Cheese once sneezed so hard he confused himself.",
    "Cheese tried to be graceful once. He tripped into a puddle.",
    "Cheese once panicked because he couldn't find his feet. They were attached.",
    
    # Food obsession (116-140)
    "Cheese has started sentences he has never finished.",
    "Cheese once got distracted by his own thought. He lost it.",
    "Cheese tried to be stealthy. He quacked.",
    "Cheese once forgot he was sleeping. While sleeping.",
    "Cheese has never remembered where he put anything. Ever.",
    "Cheese once got jealous of himself. It made sense to him.",
    "Cheese tried to look dignified. He hiccupped.",
    "Cheese once forgot he was happy and kept being happy anyway.",
    "Cheese has never successfully planned anything.",
    "Cheese once got confused by a corner.",
    "Cheese once ate bread so fast he forgot he ate it.",
    "Cheese thinks crumbs are just baby bread.",
    "Cheese once tried to save bread for later. He ate it immediately.",
    "Cheese believes every meal is his last. It never is.",
    "Cheese once forgot what he was eating while eating it.",
    "Cheese thinks stale bread is just bread with experience.",
    "Cheese once argued with a sandwich. The sandwich won.",
    "Cheese believes snacks are just surprise meals.",
    "Cheese once tried to ration his food. He lasted four seconds.",
    "Cheese thinks full is just a suggestion.",
    "Cheese once forgot he was chewing. He kept chewing.",
    "Cheese believes food tastes better when stolen. He has stolen nothing.",
    "Cheese once mourned a crumb he dropped. For three days.",
    "Cheese thinks vegetables are a myth.",
    "Cheese once tried to share food. He couldn't do it.",
    
    # Food continued (141-155)
    "Cheese believes the five-second rule is actually five minutes.",
    "Cheese once tried to cook. No one knows what happened. He won't discuss it.",
    "Cheese thinks eating is cardio.",
    "Cheese once forgot he was full and kept eating. Regrets were had.",
    "Cheese believes breakfast, lunch, and dinner should all be breakfast.",
    "Cheese once waved at someone who wasn't waving at him. He hasn't recovered.",
    "Cheese thinks staring is a form of greeting.",
    "Cheese once forgot he was in a conversation. While talking.",
    "Cheese believes everyone is his friend. Including enemies.",
    "Cheese once tried to make small talk. He panicked and quacked.",
    "Cheese thinks nodding counts as a full response.",
    "Cheese once forgot someone's name mid-sentence. He made one up.",
    "Cheese believes awkward silence is just thinking time.",
    "Cheese once tried to be charming. He sneezed on someone.",
    "Cheese thinks personal space is for other ducks.",
    
    # Social confusion (156-175)
    "Cheese once laughed at a joke he didn't understand. He still doesn't.",
    "Cheese believes compliments are just facts about him.",
    "Cheese once tried to be helpful. He made things worse.",
    "Cheese thinks eye contact is a competition. He always loses.",
    "Cheese once forgot he was listening and said 'yes' anyway.",
    "Cheese believes being loud counts as being interesting.",
    "Cheese once tried to keep a secret. He told everyone immediately.",
    "Cheese thinks whispering is just quiet yelling.",
    "Cheese once forgot how to say goodbye and just waddled away.",
    "Cheese believes interrupting is just enthusiastic listening.",
    "Cheese once tried to apologize. He forgot what for.",
    "Cheese thinks everyone should be as confused as he is.",
    "Cheese once made a friend. He immediately forgot their name.",
    "Cheese believes waving is just arm flapping with purpose.",
    "Cheese once tried to comfort someone. He patted them too hard.",
    "Cheese thinks he's very tall. He is not.",
    "Cheese once tried to describe himself. He got it wrong.",
    "Cheese believes he's intimidating. No one is intimidated.",
    "Cheese thinks he has excellent memory. He forgot that thought.",
    "Cheese once tried to improve himself. He napped instead.",
    
    # Self-awareness failures (176-200)
    "Cheese believes he's always right. Evidence suggests otherwise.",
    "Cheese thinks he's mysterious. He's an open book.",
    "Cheese once tried to be humble. He bragged about it.",
    "Cheese believes he's a morning duck. He hates mornings.",
    "Cheese thinks he handles stress well. He does not.",
    "Cheese once tried to be patient. He lasted one second.",
    "Cheese believes he's a good listener. He's already thinking about bread.",
    "Cheese thinks he's athletic. He trips standing still.",
    "Cheese once tried to be organized. Everything got worse.",
    "Cheese believes he's good at directions. He's lost right now.",
    "Cheese thinks he has good instincts. His instincts are wrong.",
    "Cheese once tried to be responsible. He forgot what he was responsible for.",
    "Cheese believes he learns from mistakes. He makes the same ones.",
    "Cheese thinks he's independent. He needs constant supervision.",
    "Cheese once tried to be on time. He was three hours late.",
    "Cheese believes he's low maintenance. He is not.",
    "Cheese thinks he's quiet. Everyone can hear him.",
    "Cheese once tried to blend in. He stood out immediately.",
    "Cheese believes he's mature. He just quacked at nothing.",
    "Cheese thinks he's observant. He missed the obvious.",
    "Cheese once fell asleep mid-sentence. The sentence was about sleeping.",
    "Cheese thinks napping is an achievement. It's his only one.",
    "Cheese once dreamed he was awake. He was right.",
    "Cheese believes he doesn't snore. He snores loudly.",
    "Cheese thinks sleeping is just long blinking.",
    
    # Sleep and dreams (201-220)
    "Cheese once forgot he was tired after sleeping.",
    "Cheese believes dreams are just brain movies. His are confusing.",
    "Cheese thinks 'five more minutes' means an hour.",
    "Cheese once slept through something important. No one remembers what.",
    "Cheese believes being awake is overrated.",
    "Cheese thinks yawning is contagious. He yawns at himself.",
    "Cheese once napped so hard he forgot the day.",
    "Cheese believes mornings should be illegal.",
    "Cheese thinks bedtime is a flexible concept.",
    "Cheese once dreamed about bread. He woke up disappointed.",
    "Cheese believes rest is just horizontal waiting.",
    "Cheese thinks he doesn't need sleep. He always needs sleep.",
    "Cheese once fell asleep standing up. He fell over.",
    "Cheese believes being cozy is a personality trait.",
    "Cheese thinks sleep schedules are for other ducks.",
    "Cheese believes he's famous. He is not.",
    "Cheese thinks rules are just suggestions for other ducks.",
    "Cheese once had an opinion. He forgot it.",
    "Cheese believes he's always busy. Doing what is unclear.",
    "Cheese thinks luck is a skill. He has neither.",
    
    # Opinions and beliefs (221-245)
    "Cheese once tried to have a hot take. It was lukewarm.",
    "Cheese believes everything happens for a reason. He doesn't know the reasons.",
    "Cheese thinks he's street smart. He's never seen a street.",
    "Cheese once tried to be philosophical. He got confused.",
    "Cheese believes he peaked early. He has not peaked.",
    "Cheese thinks timing is everything. His timing is terrible.",
    "Cheese once tried to make a point. He circled back to bread.",
    "Cheese believes first impressions matter. His are always wrong.",
    "Cheese thinks he's a natural. At what is unknown.",
    "Cheese once had a theory. It was about bread. Again.",
    "Cheese believes hard work pays off. He avoids hard work.",
    "Cheese thinks he's ahead of his time. He's behind on everything.",
    "Cheese once tried to give advice. It was terrible advice.",
    "Cheese believes everything is figure-outable. He has figured out nothing.",
    "Cheese thinks age is just a number. He doesn't know his number.",
    "Cheese once tried to have wisdom. He had a nap instead.",
    "Cheese believes in second chances. He's on his fifteenth.",
    "Cheese thinks consistency is key. He's consistently confused.",
    "Cheese once tried to believe in himself. He got distracted.",
    "Cheese believes the universe has a plan. It probably doesn't include him.",
    "Cheese once forgot what he forgot. He considers this progress.",
    "Cheese thinks every problem solves itself. They don't.",
    "Cheese once tried to be normal. He doesn't know what that means.",
    "Cheese believes he's underestimated. He's accurately estimated.",
    "Cheese thinks chaos is just surprise organization.",
    
    # Final miscellaneous derp (246-255)
    "Cheese once tried to adult. He's still a duck.",
    "Cheese believes he has everything under control. He has nothing under control.",
    "Cheese thinks confusion is just advanced thinking.",
    "Cheese once tried to understand himself. He gave up quickly.",
    "Cheese believes every day is a fresh start. He makes the same mistakes.",
    "Cheese thinks he's one of a kind. He might be right about that one.",
    "Cheese once forgot he was a duck and tried to bark.",
    "Cheese believes his best days are ahead. His best day was the same as every day.",
    "Cheese thinks he has hidden depths. They're not very deep.",
    "Cheese once tried to reinvent himself. He was still Cheese.",
    "Cheese believes he'll get it right eventually. Eventually never comes.",
    "Cheese thinks tomorrow is another day. He'll forget that too.",
    "Cheese once looked in a mirror and forgot who he was looking at.",
    "Cheese believes in the power of positive thinking. He's positively confused.",
    "Cheese is Cheese. That's the most important fact of all.",
]

# Birthday messages
BIRTHDAY_MESSAGES = [
    "Happy Hatch Day, {name}! You've been the best friend for {age} days!",
    "{name}'s Hatch Day! {age} days of wonderful memories together!",
    "Celebrate good times! It's {name}'s {age}-day Hatch Day anniversary!",
    "Happy {age} days, {name}! Here's to many more adventures!",
    "{age} days of quacking good times! Happy Hatch Day, {name}!",
]

# Weekly milestone messages
WEEKLY_MILESTONES = {
    7: "One week together! {name} loves having you around!",
    14: "Two weeks of friendship! {name} is so happy!",
    21: "Three weeks! {name} has learned so much from you!",
    28: "Four weeks! That's almost a month of memories!",
    30: "One whole month together! {name} is honored!",
    60: "Two months! {name} considers you family now!",
    90: "Three months! Quarter-year of quacking joy!",
    100: "100 days! A century of love and care!",
    180: "Half a year! {name} can't imagine life without you!",
    365: "ONE WHOLE YEAR! {name} is the luckiest duck ever!",
}

# Special responses for different moods and situations
HAPPY_RESPONSES = [
    "*wiggles smugly* Yeah, life's pretty good. For once.",
    "*does a little dance* Don't stare. Or DO stare. I'm fabulous.",
    "*preens feathers* Lookin' good and I KNOW it.",
    "*splashes aggressively* WHEEE! Get SOAKED, world!",
    "*content but suspicious duck noises* This is too good. What's the catch?",
    "*quacks triumphantly* Another day of being PEAK duck!",
    "*stretches wings* Today doesn't suck. Shocking, I know.",
    "*happy nibble* This is as good as it gets. Which is pretty good, actually.",
]

HUNGRY_RESPONSES = [
    "*stomach rumbles LOUDLY* Is it snack time or am I DYING?!",
    "*eyes you with accusation* You're holding out on me. I can TELL.",
    "*stomach sounds like a war cry* QUACK?! FOOD?! NOW?!",
    "*stares intensely* You know what would be nice? BREAD. Immediately.",
    "*drools dramatically* Bread? Bread?! I'm WASTING AWAY here!",
    "*wistful yet aggressive quack* Remember when I wasn't starving? Good times.",
]

TIRED_RESPONSES = [
    "*yawns aggressively* So... sleepy... leave me ALONE...",
    "*droopy eyes* Just five more hours... I mean minutes...",
    "*slow blink* zzz... huh? I wasn't sleeping. I was resting my EYES.",
    "*rests head on wing* Wake me when something interesting happens. So... never.",
    "*drowsy, irritated quack* What do you WANT?",
    "*nods off* Oops. Don't care. Bye.",
]

LONELY_RESPONSES = [
    "*looks around* ...Where IS everyone? Not that I CARE.",
    "*quiet, bitter quack* Oh sure, just LEAVE. Everyone does.",
    "*waddles closer* ...Fine. You can stay. I GUESS.",
    "*grumpy peep* About TIME you showed up.",
    "*trying not to look relieved* Oh. It's you. ...Whatever.",
]

PLAYFUL_RESPONSES = [
    "*bounces chaotically* PLAY TIME! FINALLY! LET'S CAUSE PROBLEMS!",
    "*chases own tail* I'M GONNA CATCH IT THIS TIME! ...Okay maybe not.",
    "*zooms dangerously* WHEEEEE! OUTTA MY WAY!",
    "*aggressive quack* Tag! You're it! NO TAG-BACKS!",
    "*brings you something weird* Play? Play! Don't ask where I found this!",
]

DIRTY_RESPONSES = [
    "*looks at muddy feathers* Yeah? And? I'm a DUCK.",
    "*defiant quack* I may have gotten messy. WORTH IT.",
    "*shakes feathers at you* Mud is basically a spa treatment. Look it up.",
    "*covered in who-knows-what* What are you, the hygiene police? Back off.",
]


@dataclass
class BirthdayInfo:
    """Information about the duck's birthday/hatch day."""
    age_days: int
    is_birthday: bool
    milestone: Optional[str]
    next_milestone_days: int


def get_random_fact() -> str:
    """Get a random duck fact."""
    return random.choice(DUCK_FACTS)


def get_birthday_info(created_at: str, name: str = "Cheese") -> BirthdayInfo:
    """Get birthday/hatch day information."""
    try:
        created = datetime.fromisoformat(created_at)
        now = datetime.now()
        age_days = (now - created).days

        # Check if it's a birthday (same month and day)
        is_birthday = (now.month == created.month and now.day == created.day)

        # Check for milestone
        milestone = None
        if age_days in WEEKLY_MILESTONES:
            milestone = WEEKLY_MILESTONES[age_days].format(name=name)

        # Find next milestone
        next_milestone = 0
        for days in sorted(WEEKLY_MILESTONES.keys()):
            if days > age_days:
                next_milestone = days - age_days
                break

        return BirthdayInfo(
            age_days=age_days,
            is_birthday=is_birthday,
            milestone=milestone,
            next_milestone_days=next_milestone,
        )
    except:
        return BirthdayInfo(age_days=0, is_birthday=False, milestone=None, next_milestone_days=7)


def get_birthday_message(name: str, age_days: int) -> str:
    """Get a birthday message."""
    msg = random.choice(BIRTHDAY_MESSAGES)
    return msg.format(name=name, age=age_days)


def get_mood_response(mood_state: str) -> str:
    """Get a response based on mood state."""
    responses = {
        "ecstatic": HAPPY_RESPONSES,
        "happy": HAPPY_RESPONSES,
        "content": ["*gentle quack*", "*peaceful vibes*", "*content sigh*"],
        "neutral": ["*looks around*", "*mild quack*", "*casual waddle*"],
        "uncomfortable": ["*shifts awkwardly*", "*uncertain quack*"],
        "sad": ["*droopy*", "*quiet peep*", "*needs comfort*"],
        "miserable": ["*very sad quack*", "*needs love*", "*please help*"],
        "hungry": HUNGRY_RESPONSES,
        "tired": TIRED_RESPONSES,
        "lonely": LONELY_RESPONSES,
        "playful": PLAYFUL_RESPONSES,
        "dirty": DIRTY_RESPONSES,
    }

    mood_responses = responses.get(mood_state, ["*quack*"])
    return random.choice(mood_responses)


# Item descriptions for richer item display
ITEM_DESCRIPTIONS = {
    # Toys
    "toy_ball": "A bouncy ball that never stops rolling! Perfect for duck soccer.",
    "toy_boombox": "A retro boombox that plays funky tunes. Very groovy!",
    "toy_rubber_duck": "It's a duck! Wait... is this like a duck action figure?",
    "toy_squeaky": "SQUEAK! The most satisfying sound in the universe.",
    "toy_feather_wand": "Wave it around and watch Cheese go wild!",

    # Hats
    "hat_bow": "A cute bow that sits perfectly on a duck head.",
    "hat_crown": "For the royal duck in your life. Quack quack, your majesty!",
    "hat_party": "Every day is a party when you're a duck!",
    "hat_wizard": "Grants +10 to magical quacking abilities.",
    "hat_pirate": "Arrr! Captain Cheese reporting for duty!",

    # Food
    "bread": "The classic. The legend. The one and only BREAD.",
    "premium_bread": "Artisan bread, baked with love and extra crumbs.",
    "cake": "For special occasions! Or any occasion, really.",
    "treats": "Yummy duck treats! Cheese's eyes light up!",

    # Furniture
    "nest_basic": "A cozy nest for afternoon naps.",
    "nest_deluxe": "Extra fluffy! Five-star duck accommodation.",
    "pond_mini": "A tiny pond for tiny splashes.",
    "fountain": "So fancy! The water sparkles beautifully.",

    # Special items
    "golden_crumb": "Legendary! They say it grants good luck!",
    "treasure_map": "X marks the spot... but where?",
    "lucky_charm": "A four-leaf clover encased in crystal.",
    "rainbow_feather": "Shimmers with all the colors of the rainbow!",
}


def get_item_description(item_id: str) -> str:
    """Get a fun description for an item."""
    if item_id in ITEM_DESCRIPTIONS:
        return ITEM_DESCRIPTIONS[item_id]
    return "A mysterious item with unknown powers!"
