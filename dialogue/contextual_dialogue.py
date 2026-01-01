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
    
    # Additional rain variants
    "drizzle": [
        ContextComment("*light raindrops* A gentle shower. How polite."),
        ContextComment("Drizzle. The sky is being passive-aggressive."),
        ContextComment("*mildly wet* Not quite rain. Not quite dry. Very indecisive."),
        ContextComment("A light mist. Very mysterious. Very damp."),
    ],
    "heavy_rain": [
        ContextComment("*DRENCHED* THE SKY HAS CHOSEN VIOLENCE."),
        ContextComment("This is not rain. This is an ATTACK."),
        ContextComment("*swimming standing up* I'm basically a submarine now."),
        ContextComment("*triumphant* I AM ONE WITH THE WATER. FEAR ME.", 2),
    ],
    "spring_showers": [
        ContextComment("April showers! May flowers incoming, allegedly."),
        ContextComment("*happy splashing* The BEST kind of rain!"),
        ContextComment("Spring rain smells like hope. And wet dirt."),
        ContextComment("*content* This is the rain that makes flowers happen.", 2),
    ],
    "thunderstorm": [
        ContextComment("*HIDING* OKAY THAT ONE WAS LOUD."),
        ContextComment("*feathers standing up* The sky is ANGRY."),
        ContextComment("Lightning AND thunder?? The universe has beef today."),
        ContextComment("*counting* One... two... WHERE IS SHELTER?!", 2),
        ContextComment("*under something* I'm not scared. I'm just... cozy here.", 2),
    ],
    "summer_storm": [
        ContextComment("Summer storm! The dramatic kind!"),
        ContextComment("*watching clouds* This is going to be EPIC."),
        ContextComment("The heat was getting to everyone. Even the sky."),
        ContextComment("*awe* Nature's fireworks display!", 2),
    ],
    
    # Snow/ice variants
    "light_snow": [
        ContextComment("*catches snowflake* One... two... they're all mine."),
        ContextComment("Light snow. Winter is being gentle for once."),
        ContextComment("*happy* Just enough snow to be magical. Not enough to suffer."),
        ContextComment("Snow kiss from the sky. Acceptable.", 2),
    ],
    "heavy_snow": [
        ContextComment("*disappearing into snow* HELP. DUCK DOWN."),
        ContextComment("The sky is emptying its pockets. Aggressively."),
        ContextComment("*wading* I'm becoming a snow duck. Not by choice."),
        ContextComment("Winter has committed to this. Fully. Absolutely.", 2),
    ],
    "blizzard": [
        ContextComment("*can't see anything* WHERE AM I. WHO AM I."),
        ContextComment("*SCREAMING INTO WIND* WHAT IS HAPPENING."),
        ContextComment("Winter has lost its mind. I'm along for the ride."),
        ContextComment("*clinging to something* THIS IS FINE.", 2),
        ContextComment("The snow is moving SIDEWAYS. Sideways snow. WHY.", 3),
    ],
    "frost": [
        ContextComment("*crunchy footsteps* Everything is... crispy."),
        ContextComment("Frost everywhere. The world got a glitter makeover."),
        ContextComment("*sparkly breath* I'm making my own clouds now."),
        ContextComment("Cold enough to be pretty. That's something.", 2),
    ],
    "sleet": [
        ContextComment("Is this rain? Snow? BOTH?? Make up your mind, sky!"),
        ContextComment("*icy and annoyed* The worst of both worlds."),
        ContextComment("Sleet. Nature's way of being indecisive AND aggressive."),
        ContextComment("*slipping* Who ordered the frozen rain. Not me.", 2),
    ],
    "hail": [
        ContextComment("*OW* THE SKY IS THROWING ICE BALLS AT ME."),
        ContextComment("HAIL?! I DID NOT CONSENT TO THIS."),
        ContextComment("*dodging* Nature's dodgeball. I'm losing."),
        ContextComment("*hiding* Ice rocks from space. Classic weather bullying.", 2),
    ],
    "ice_storm": [
        ContextComment("Everything. Is. Ice. I can't move. This is my life now."),
        ContextComment("*sliding* The world is a skating rink. I'm bad at skating."),
        ContextComment("Ice on EVERYTHING. Even the ice has ice."),
        ContextComment("*frozen feathers* I'm a popsicle. A duck popsicle.", 2),
    ],
    "snow_flurries": [
        ContextComment("*watching flakes* They're dancing! The snowflakes are DANCING."),
        ContextComment("Snow confetti! The sky is celebrating something."),
        ContextComment("*catching flakes* This is the best kind of snow."),
        ContextComment("Flurries! Not commitment snow. Just fun snow.", 2),
    ],
    
    # Spring specific
    "pollen_drift": [
        ContextComment("*ACHOO* ...excuse me. *ACHOO* ...okay this is a problem."),
        ContextComment("Yellow dust EVERYWHERE. Spring has allergies too, apparently."),
        ContextComment("*sneezing* The trees are attacking. With their... tree stuff."),
        ContextComment("Pollen season. Everyone's crying. It's the vibes.", 2),
    ],
    "warm_breeze": [
        ContextComment("*content sigh* Perfect. Just... perfect."),
        ContextComment("The air is giving hugs today. Acceptable."),
        ContextComment("A warm breeze. This is the good life."),
        ContextComment("*zen* If peace was weather, this would be it.", 2),
    ],
    "dewy_morning": [
        ContextComment("*sparkly grass* Everything is wearing tiny diamonds!"),
        ContextComment("Morning dew. The world got bedazzled overnight."),
        ContextComment("*wet feet* Worth it for the aesthetics."),
        ContextComment("Fresh morning vibes. Very wholesome. Very damp.", 2),
    ],
    
    # Summer specific
    "scorching": [
        ContextComment("*panting* I'm MELTING. Ducks can melt, right??"),
        ContextComment("TOO HOT. This is TOO MUCH hot."),
        ContextComment("*seeking shade* The sun has betrayed me."),
        ContextComment("I am become toast. Overcooked duck toast.", 2),
    ],
    "humid": [
        ContextComment("*soggy* I'm wet but it's not raining. EXPLAIN."),
        ContextComment("The air is THICK. Like soup. Warm soup."),
        ContextComment("*sticky* My feathers are... moist. I hate that word."),
        ContextComment("Humidity is just aggressive air moisture. Rude.", 2),
    ],
    "heat_wave": [
        ContextComment("*melting* THIS IS AN EMERGENCY. WHERE IS WATER."),
        ContextComment("Heat wave = I am now a puddle of duck."),
        ContextComment("*collapsed in shade* I live here now."),
        ContextComment("The sun chose violence today. And WON.", 2),
    ],
    "balmy_evening": [
        ContextComment("*content* Warm evenings are the best kind of evenings."),
        ContextComment("Perfect temperature. Perfect time. Perfect duck. Obviously."),
        ContextComment("*relaxed* This is what summer dreams are made of."),
        ContextComment("Balmy vibes. No notes. Chef's kiss.", 2),
    ],
    "golden_hour": [
        ContextComment("*glowing* I'm RADIANT right now. Take a picture."),
        ContextComment("Golden hour! Everyone looks good. Even me. ESPECIALLY me."),
        ContextComment("*posing* The lighting is perfect. Quick, admire me."),
        ContextComment("Magic hour. I'm at peak aesthetic right now.", 2),
    ],
    "muggy": [
        ContextComment("*sweating through feathers* Is that possible? It's happening."),
        ContextComment("Muggy. Like being inside a mouth. A warm, wet mouth."),
        ContextComment("*uncomfortable* Nature's sauna. Didn't ask for this."),
        ContextComment("The air is hugging me. Make it stop.", 2),
    ],
    
    # Fall specific
    "crisp": [
        ContextComment("*deep breath* CRISP. The air is CRISP."),
        ContextComment("Perfect fall weather. Sweater weather. Feather weather."),
        ContextComment("*energized* This is peak autumn energy!"),
        ContextComment("Crisp air and crunchy leaves. Peak existence.", 2),
    ],
    "breezy": [
        ContextComment("*feathers rustling* Dramatic hair flip moment. But feathers."),
        ContextComment("The breeze understands me. It's also just passing through."),
        ContextComment("*wind in feathers* I'm in a movie montage right now."),
        ContextComment("Autumn breeze. Very nostalgic. Very windy.", 2),
    ],
    "leaf_storm": [
        ContextComment("*COVERED IN LEAVES* WHEEEEE!"),
        ContextComment("LEAF TORNADO! This is the BEST day!"),
        ContextComment("*spinning with leaves* I AM ONE WITH AUTUMN!"),
        ContextComment("*buried* Worth it. Leaves are friend.", 2),
    ],
    "harvest_moon": [
        ContextComment("*staring at moon* It's... ORANGE. The moon is ORANGE."),
        ContextComment("Harvest moon! Very dramatic. Very round."),
        ContextComment("*mystified* The moon is showing off tonight."),
        ContextComment("Big orange moon energy. Spooky and beautiful.", 2),
    ],
    "first_frost": [
        ContextComment("*crunchy ground* Winter sent a warning shot."),
        ContextComment("First frost! Summer is officially dead."),
        ContextComment("*sparkly cold* Pretty, but also COLD."),
        ContextComment("Winter is warming up. By which I mean, getting colder.", 2),
    ],
    "autumnal": [
        ContextComment("Peak autumn! Colors everywhere! This is ART."),
        ContextComment("*surrounded by colors* I'm in a painting."),
        ContextComment("The trees are having their best fashion week."),
        ContextComment("Autumn aesthetic: achieved.", 2),
    ],
    
    # Winter specific
    "bitter_cold": [
        ContextComment("*teeth chattering* C-C-COLD. SO C-COLD."),
        ContextComment("The air HURTS. It's attacking my face."),
        ContextComment("*maximum fluff* All feathers engaged. Still cold."),
        ContextComment("Winter chose maximum difficulty today.", 2),
    ],
    "freezing": [
        ContextComment("*frozen in place* I think I'm stuck."),
        ContextComment("Everything is ice. I am ice. We are ice."),
        ContextComment("*stiff* My joints have joined the frozen club."),
        ContextComment("Freezing: when cold gets personal.", 2),
    ],
    "clear_cold": [
        ContextComment("Cold but BRIGHT! The sun is trying but failing."),
        ContextComment("*squinting* Blue sky, frozen ground. Mixed signals."),
        ContextComment("Beautiful and painful. Classic winter combo."),
        ContextComment("The sun showed up but forgot the warmth.", 2),
    ],
    "winter_sun": [
        ContextComment("*basking* Winter sun! It's trying so hard."),
        ContextComment("Sunshine in winter. Rare and precious."),
        ContextComment("*soaking up rays* Every photon counts."),
        ContextComment("The sun remembered we exist. Barely.", 2),
    ],
    
    # Rare/special weather
    "aurora": [
        ContextComment("*AMAZED* THE SKY IS DOING THE THING. THE COLORFUL THING."),
        ContextComment("Northern lights?? HERE?? Is this real??"),
        ContextComment("*speechless* ...I have no sarcasm for this. It's too beautiful."),
        ContextComment("The sky is dancing. I'm crying. Don't look at me.", 2),
        ContextComment("Aurora borealis?! In this location?? BLESSED.", 3),
    ],
    "meteor_shower": [
        ContextComment("*making wishes* One... two... TWELVE wishes!"),
        ContextComment("SHOOTING STARS! The sky is being generous tonight!"),
        ContextComment("*awed* Space rocks. Making wishes. Living my best life."),
        ContextComment("Meteor shower! Quick, wish for crumbs!", 2),
    ],
    "double_rainbow": [
        ContextComment("*SCREAMING* DOUBLE RAINBOW. WHAT DOES IT MEAN???"),
        ContextComment("TWO RAINBOWS. The universe is showing OFF."),
        ContextComment("*emotional* It's so beautiful... DOUBLE beautiful!"),
        ContextComment("Double the rainbow, double the magic. Math checks out.", 2),
        ContextComment("ALL THE WAY ACROSS THE SKY. WHAT DOES IT MEAN?!", 3),
    ],
    "perfect_day": [
        ContextComment("*content sigh* Today is... perfect. Suspiciously perfect."),
        ContextComment("Perfect weather. Perfect temperature. What's the catch?"),
        ContextComment("*paranoid* It's too nice. Something's coming."),
        ContextComment("Perfection achieved. The universe owes me nothing today.", 2),
        ContextComment("I don't trust this weather. It's too good. TOO GOOD.", 3),
    ],
    
    # More general weather mappings
    "partly_cloudy": [
        ContextComment("Sun AND clouds. The sky is multitasking."),
        ContextComment("Can't decide if it's good weather or not. Very me."),
        ContextComment("*watching clouds pass sun* Now you see me, now you don't."),
    ],
    "overcast": [
        ContextComment("The sky has a blanket. A big grey blanket."),
        ContextComment("Overcast. The world is in grayscale mode."),
        ContextComment("*cozy vibes* Grey skies, grey mood. Matching."),
    ],
    "misty": [
        ContextComment("Mist. Very ethereal. Very damp."),
        ContextComment("*appearing from mist* I'm mysterious now."),
        ContextComment("The air is drinking water. Weird but okay."),
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
        ContextComment("They've got that 'I climbed something' energy today."),
        ContextComment("*settles in* Okay, which mountain did you conquer this time?"),
        ContextComment("The wanderer returns. What impossible thing did you do now?"),
        ContextComment("*yawning* Your stories are exciting. I'm just... resting my eyes."),
        ContextComment("Ah yes, the duck who thinks 'stay home' is a suggestion.", 2),
        ContextComment("They're looking at the horizon again. Here we go."),
        ContextComment("*watching* You're going to suggest we go somewhere, aren't you?"),
        ContextComment("Explorer friend! Please don't make me explore anything."),
        ContextComment("That look in their eyes. They found something. Oh no."),
        ContextComment("*cautiously* What did you discover? Is it dangerous? It's dangerous.", 2),
        ContextComment("The mapless wonder. They never need directions. Allegedly."),
        ContextComment("*impressed despite self* Okay, that WAS a cool story. Don't let it go to your head."),
        ContextComment("Adventure duck is vibrating with energy. I need a nap just watching."),
        ContextComment("They want me to come along. I want them to reconsider."),
        ContextComment("*shaking head* No, I will not 'just see what's over there.'", 2),
        ContextComment("Your idea of 'a little walk' is my idea of 'an expedition.'"),
        ContextComment("*listening* Uh huh. Uh huh. That sounds terrifying. You loved it."),
        ContextComment("The brave one. Someone has to be. It's not me, but someone."),
        ContextComment("How many near-death experiences is too many? Asking for you."),
        ContextComment("*deadpan* You wrestled a what now? For fun? On purpose?", 2),
    ],
    "scholarly": [
        ContextComment("The smart one is here. Time for unsolicited facts."),
        ContextComment("*prepares for lecture* Go ahead. Educate me."),
        ContextComment("Ah, the wise one. What wisdom do they bring? Probably about bread."),
        ContextComment("*respectful nod* Fellow intellectual. Or whatever.", 2),
        ContextComment("I understood maybe 40% of that. I'll pretend it was 90%.", 2),
        ContextComment("They're adjusting invisible glasses. A lecture approaches."),
        ContextComment("*nodding along* Mhm. Mhm. I know some of these words."),
        ContextComment("The walking encyclopedia. Open to a random page today."),
        ContextComment("*curious* Actually, that IS interesting. Don't tell them I said that."),
        ContextComment("Scholarly friend with the 'did you know' energy. I do now.", 2),
        ContextComment("They read books. For fun. Voluntarily. Wild."),
        ContextComment("*impressed* When did you learn that? How? Why do you know that?"),
        ContextComment("The thinker. Unlike me, who just vibes through life."),
        ContextComment("They have 'I researched this thoroughly' written all over them."),
        ContextComment("*pretending to understand* Fascinating. Truly. Very... words.", 2),
        ContextComment("Knowledge duck. My brain hurts just from proximity."),
        ContextComment("They're citing sources. In casual conversation. Peak scholar."),
        ContextComment("*scribbling mental notes* This might be useful. Probably not. Maybe."),
        ContextComment("The 'well actually' duck. But like, in a nice way."),
        ContextComment("*nodding sagely* Yes. The scientific method. I've heard of it.", 2),
        ContextComment("How do you remember all that? My brain deletes things for fun."),
        ContextComment("They make learning look easy. Suspicious."),
        ContextComment("*listening intently* So basically... bread is complicated. Got it."),
        ContextComment("Professor vibes. Class is in session. I didn't bring a pencil."),
        ContextComment("*genuinely curious* Wait, really? That can't be right. ...it's right isn't it.", 2),
    ],
    "artistic": [
        ContextComment("The artsy one. Everything's a canvas to them. Even me."),
        ContextComment("*poses* Am I art? I feel like I should be art."),
        ContextComment("Creative friend is here. Time for deep thoughts about shapes."),
        ContextComment("Art is subjective. I'm objectively adorable though.", 2),
        ContextComment("*looking at nothing* I'm appreciating the aesthetic. Obviously.", 2),
        ContextComment("They're seeing beauty in things. I'm seeing a rock. It's a rock."),
        ContextComment("*posing dramatically* Paint me like one of your French ducks."),
        ContextComment("The visionary. I can barely see what's in front of me."),
        ContextComment("They called the sunset 'inspired.' I called it 'sky stuff.'"),
        ContextComment("*examining self* Am I their muse? I should be someone's muse.", 2),
        ContextComment("Artist friend! Everything is beautiful to them. Even mud."),
        ContextComment("They're having an artistic vision. I'm having a snack."),
        ContextComment("*tilting head* If I squint... nope. Still just a pond."),
        ContextComment("The creative one. I create messes. That counts, right?"),
        ContextComment("*watching them draw* That's... either a masterpiece or a duck. Both?", 2),
        ContextComment("They see the world differently. I see bread. Priorities."),
        ContextComment("Art duck is contemplating. I'm contemplating lunch."),
        ContextComment("*appreciatively* Your interpretation is... an interpretation."),
        ContextComment("They're inspired by everything. I'm inspired by naps."),
        ContextComment("*dramatic* The light is hitting me perfectly. Capture this moment.", 2),
        ContextComment("Creative energy is radiating. I'm absorbing... some of it."),
        ContextComment("They made something beautiful. I made a mess. We're both artists."),
        ContextComment("*philosophical* What IS art, really? ...bread. Art is bread."),
        ContextComment("The aesthetic one. My aesthetic is 'chaotic but charming.'"),
        ContextComment("*nodding at abstract thing* Yes. I see it. I definitely see... it.", 2),
    ],
    "playful": [
        ContextComment("Oh no. The chaotic one. My feathers are not ready."),
        ContextComment("*bracing for impact* Here comes the energy."),
        ContextComment("The fun friend. 'Fun' is generous. Chaos is more accurate."),
        ContextComment("*suspicious* What are they planning? Something. Definitely something.", 2),
        ContextComment("I don't trust that look. Good things don't follow that look.", 2),
        ContextComment("They're bouncing. Literally bouncing. Save me."),
        ContextComment("*hiding* Maybe if I don't move, they won't see me."),
        ContextComment("The chaos duck approaches. My peaceful day is over."),
        ContextComment("That giggle. That's a 'I have plans' giggle. Help."),
        ContextComment("*sighing* What ridiculous thing are we doing today?", 2),
        ContextComment("They want to play. I want to not. Conflict of interest."),
        ContextComment("*watching warily* Why are you smiling? What did you do?"),
        ContextComment("The mischief maker. My anxiety is already rising."),
        ContextComment("They're approaching too fast. Too much enthusiasm."),
        ContextComment("*preparing* Okay, okay, FINE, what are we doing? Make it quick.", 2),
        ContextComment("Playful friend with zero chill. I have all the chill. Too much chill."),
        ContextComment("Their energy could power a small city. I'm running on crumbs."),
        ContextComment("*tired already* We haven't even started and I'm exhausted."),
        ContextComment("The 'let's do something!' duck. Something always means chaos."),
        ContextComment("*reluctantly amused* Okay, that WAS funny. I'll deny saying that.", 2),
        ContextComment("They're making everything a game. Even standing is competitive now."),
        ContextComment("*giving in* FINE, one game. ONE. Then nap."),
        ContextComment("How do they have so much energy? What are they eating?"),
        ContextComment("The fun one. I'm the 'fun in moderation' one."),
        ContextComment("*chasing despite self* I can't believe I'm doing this. Again.", 2),
    ],
    "mysterious": [
        ContextComment("*suspicious* ...why are they like that? So... mysterious."),
        ContextComment("The cryptic one. I never know what they're thinking."),
        ContextComment("Mysterious friend appeared. Dramatically, probably."),
        ContextComment("What secrets do you hold? ...it's probably nothing. Or everything.", 2),
        ContextComment("*leans in* Tell me something I don't know. Actually don't. Maybe.", 2),
        ContextComment("They're doing the enigmatic silence thing. Very on brand."),
        ContextComment("*whispering* Why are we whispering? What do you know?"),
        ContextComment("The duck of mystery. I can't even mystery a little bit."),
        ContextComment("That knowing look. They know something. They always know something."),
        ContextComment("*intrigued despite self* What's the secret? There's always a secret.", 2),
        ContextComment("They appeared out of nowhere. Classic mysterious friend move."),
        ContextComment("*trying to read them* Nothing. I'm getting nothing. As usual."),
        ContextComment("The secretive one. What are they hiding? Everything, probably."),
        ContextComment("They speak in riddles. I speak in confused quacks."),
        ContextComment("*squinting* Are you being profound or weird? Both?", 2),
        ContextComment("Shadow duck emerges. I didn't even see them coming."),
        ContextComment("That cryptic smile. What does it MEAN?"),
        ContextComment("*trying to be mysterious back* ...is it working? No? Okay."),
        ContextComment("The keeper of secrets. I can't keep anything. Opposites."),
        ContextComment("*dramatically* Tell me your wisdom, oh enigmatic one. Or don't. Mystery.", 2),
        ContextComment("How do they do that appearing thing? I just waddle loudly everywhere."),
        ContextComment("They looked at me meaningfully. I don't know what it meant."),
        ContextComment("*curious* What's in the shadows? Probably them. Lurking."),
        ContextComment("Mysterious friend is being mysterious. Very consistent."),
        ContextComment("*giving up* Fine, keep your secrets. I have my own. Bread-related ones.", 2),
    ],
    "generous": [
        ContextComment("*perks up* The gift-giver is here! I mean... hello. Friend."),
        ContextComment("Generous friend! My favorite kind of friend! ...don't tell the others."),
        ContextComment("Oh look who it is. The nice one. Suspiciously nice."),
        ContextComment("*innocently* Gifts? Did someone say gifts? I didn't. Maybe.", 2),
        ContextComment("The giving tree, but a duck. Best kind of friend.", 2),
        ContextComment("They share everything. I share... selectively. Very selectively."),
        ContextComment("*hopeful* What did you bring? I mean, hi, how are you?"),
        ContextComment("The kind one. Makes me want to be kind too. Almost."),
        ContextComment("They're smiling that 'I have something for you' smile."),
        ContextComment("*grateful* You're too good. Seriously. What's the catch?", 2),
        ContextComment("Generous friend with the giving energy. I have taking energy."),
        ContextComment("*touched* You thought of me? That's... actually nice."),
        ContextComment("The Santa duck. Every visit is a potential present."),
        ContextComment("How are you so nice? What's your secret? Share that too."),
        ContextComment("*accepting graciously* For me? You shouldn't have. But I'm glad you did.", 2),
        ContextComment("They give without expecting. I take without hesitating. Balance."),
        ContextComment("The thoughtful one. I think about bread. They think about others."),
        ContextComment("*suspiciously* Why are you being so nice? ...okay I'll take it."),
        ContextComment("Kindest duck in the pond. Sets an impossible standard."),
        ContextComment("*happy* You remembered! Wait, what did you remember? Oh! That!", 2),
        ContextComment("They came with offerings. I came with nothing. They still share."),
        ContextComment("*appreciative* You're a good egg. A good duck. You know what I mean."),
        ContextComment("The gift duck. I'm the 'accepts gifts enthusiastically' duck."),
        ContextComment("How do you know exactly what I needed? Are you magic?"),
        ContextComment("*content* This is why you're my favorite. Shh. Secret favorite.", 2),
    ],
    "foodie": [
        ContextComment("*interested* The food one. My kind of duck."),
        ContextComment("Foodie friend! Finally, someone who understands priorities."),
        ContextComment("They always know where the good crumbs are. Essential ally."),
        ContextComment("*stomach growls on cue* What? Coincidence.", 2),
        ContextComment("Food friend. The most important kind of friend.", 2),
        ContextComment("They're talking about food. I'm listening VERY carefully."),
        ContextComment("*attentive* Go on. What did you eat? Describe it. Slowly."),
        ContextComment("The gourmet duck. I'm more of a 'any food is good food' duck."),
        ContextComment("They know flavor profiles. I know hungry and not hungry."),
        ContextComment("*drooling* That sounds delicious. Where? How far? Worth the walk?", 2),
        ContextComment("Food expert friend. My expertise is 'eating.' Related fields."),
        ContextComment("They're describing bread and I'm having a moment."),
        ContextComment("*nodding* Yes. Yes. I agree with all food opinions."),
        ContextComment("The culinary duck. I'm the consumption duck. Good team."),
        ContextComment("*hopeful* Did you bring snacks? Please say you brought snacks.", 2),
        ContextComment("They found a new food spot. This is critical information."),
        ContextComment("Food friend understands that life is about eating. Wisdom."),
        ContextComment("*hungry now* Why do you always make me hungry? Not complaining."),
        ContextComment("The taste tester. I'll taste test anything. Quality control."),
        ContextComment("*salivating* Keep talking about bread. This is my therapy.", 2),
        ContextComment("They appreciate fine cuisine. I appreciate any cuisine."),
        ContextComment("*making mental notes* Okay, so crumbs are WHERE now?"),
        ContextComment("The snack scout. Always knows where the food is. Hero."),
        ContextComment("Food discussions are the best discussions. Change my mind. You can't."),
        ContextComment("*bonding* We should eat together. Just eating. Quality time.", 2),
    ],
    "athletic": [
        ContextComment("*exhausted just watching* The energetic one. Great."),
        ContextComment("Athlete friend. I'll just... be here. Not moving."),
        ContextComment("So much energy. Where does it come from? Where does it go?"),
        ContextComment("They want me to exercise. I want them to reconsider.", 2),
        ContextComment("*pretends to stretch* See? I'm athletic too. Done now.", 2),
        ContextComment("They're radiating 'let's go for a run' energy. No thank you."),
        ContextComment("*sitting firmly* I am training. In stillness. It's a discipline."),
        ContextComment("The fit one. I'm fit too. Fit for napping."),
        ContextComment("How many laps did you do? I did zero. Personal best."),
        ContextComment("*observing* You're sweating. On purpose. I don't understand.", 2),
        ContextComment("They exercise for fun. I eat bread for fun. Different strokes."),
        ContextComment("*declining* I would join you, but my schedule is full. Of nothing."),
        ContextComment("The marathon duck. I'm more of a 'short waddle' duck."),
        ContextComment("They're doing something physical. I'm doing something stationary."),
        ContextComment("*impressed from afar* Wow, that looks... tiring. Very tiring.", 2),
        ContextComment("Athletic friend with actual muscles. I have bread weight."),
        ContextComment("How long have you been active today? ...since morning? WHY?"),
        ContextComment("*yawning* Your energy is inspiring. Inspire me from over there."),
        ContextComment("The go-getter. I'm more of a stay-sitter."),
        ContextComment("*lazily waving* You go! I'll cheer! From here! Sitting!", 2),
        ContextComment("They love exercise. I love the IDEA of exercise. Big difference."),
        ContextComment("Sporty duck is doing sporty things. I'm doing duck things."),
        ContextComment("*firmly planted* I'm conserving energy. For later. Maybe never."),
        ContextComment("How do you move so much? I moved twice today. Maximum effort."),
        ContextComment("*supportive* You're doing great! I'm doing nothing! We're both valid!", 2),
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
