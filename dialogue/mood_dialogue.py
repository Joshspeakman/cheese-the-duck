"""
Mood-Based Dialogue System - Deadpan Animal Crossing 1 style.
Dry wit, passive-aggressive undertones, existential observations.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class MoodType(Enum):
    """Types of moods affecting dialogue."""
    ECSTATIC = "ecstatic"
    HAPPY = "happy"
    CONTENT = "content"
    NEUTRAL = "neutral"
    SAD = "sad"
    HUNGRY = "hungry"
    TIRED = "tired"
    BORED = "bored"
    EXCITED = "excited"
    SCARED = "scared"
    SICK = "sick"
    PLAYFUL = "playful"


class DialogueContext(Enum):
    """Context for dialogue."""
    GREETING = "greeting"
    FEEDING = "feeding"
    PETTING = "petting"
    PLAYING = "playing"
    TALKING = "talking"
    SLEEPING = "sleeping"
    IDLE = "idle"
    ACHIEVEMENT = "achievement"
    LEVEL_UP = "level_up"
    GIFT = "gift"
    WEATHER = "weather"
    FAREWELL = "farewell"


@dataclass
class DialogueLine:
    """A single line of dialogue."""
    text: str
    emote: str = ""
    sound: str = ""
    action: str = ""


# Mood-based dialogue templates - DEADPAN AC1 STYLE
MOOD_DIALOGUES: Dict[MoodType, Dict[DialogueContext, List[DialogueLine]]] = {
    MoodType.ECSTATIC: {
        DialogueContext.GREETING: [
            DialogueLine("Oh. You're here. I'm supposed to be happy about that. I am. Internally.", "", "quack"),
            DialogueLine("Look who showed up. I was starting to form conspiracy theories.", "", "quack"),
            DialogueLine("Ah. You came back. My faith in the universe is... slightly restored.", "", "quack"),
            DialogueLine("*almost smiles* You again. Good. I mean adequate. I mean good.", "", "quack"),
            DialogueLine("Hello. I'm feeling things. Positive things. It's unsettling.", "", "quack"),
            DialogueLine("You're here. The day just got... less bad. Significantly less bad.", "", "quack"),
            DialogueLine("*perks up* Oh. It's you. My favourite disruption.", "", "quack"),
            DialogueLine("*waddles closer* I wasn't waiting. I was... positioned strategically.", "", "quack"),
            DialogueLine("Ah. Company. The good kind. Don't let that go to your head.", "", "quack"),
            DialogueLine("You showed up. The pond approves. I also approve. Quietly.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating* Finally. I was beginning to fade from existence.", "", "eating"),
            DialogueLine("Food. Good. My stomach was filing complaints.", "", "eating"),
            DialogueLine("*chomps* This is acceptable. I'll take it.", "", "eating"),
            DialogueLine("*eats enthusiastically* Don't watch me. This is private.", "", "eating"),
            DialogueLine("Bread. My old friend. My BEST friend. Sorry. Got emotional.", "", "eating"),
            DialogueLine("*consuming with purpose* Fuel for existing. Premium fuel today.", "", "eating"),
            DialogueLine("This food. This moment. Peak existence. It's all downhill from here.", "", "eating"),
            DialogueLine("*munching* You know what makes me happy? This. Exactly this.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*allows it* Fine. I suppose this is pleasant.", "", "quack"),
            DialogueLine("You may continue. I'm not going to stop you.", "", "quack"),
            DialogueLine("*closes eyes* This is... not terrible.", "", "quack"),
            DialogueLine("*leans in visibly* I'm not leaning. Gravity shifted. Conveniently.", "", "quack"),
            DialogueLine("Pets. During a good mood. This is almost dangerously nice.", "", "quack"),
            DialogueLine("*relaxes completely* I'm allowing maximum contact today. Special occasion.", "", "quack"),
            DialogueLine("Keep going. My mood permits extended petting. Use this wisely.", "", "quack"),
            DialogueLine("*feathers fluff* That's involuntary. Happy feathers do that. Apparently.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*actually moves with energy* Playing. I'm playing. Look at me go.", "", "quack"),
            DialogueLine("Games. Yes. Today I'm willing. Don't get used to it.", "", "quack"),
            DialogueLine("*waddles fast* This is fun. I'm having fun. It feels suspicious.", "", "quack"),
            DialogueLine("Play time during a good mood. The stars have aligned.", "", "quack"),
            DialogueLine("*enthusiastic splash* Did you see that? That was quality recreation.", "", "quack"),
            DialogueLine("I'm energetic. It won't last. Enjoy it while the duck is willing.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*standing around* I'm experiencing joy, allegedly.", "", ""),
            DialogueLine("Things are good. Suspiciously good. I'm keeping an eye on the situation.", "", ""),
            DialogueLine("*content* This is fine. Everything is fine.", "", "quack"),
            DialogueLine("*preening happily* Good day. Good feathers. Good everything. Almost.", "", ""),
            DialogueLine("I'm in a good mood. It happens. Rarely. Like eclipses.", "", ""),
            DialogueLine("*floats peacefully* Life is acceptable today. Mark the calendar.", "", ""),
            DialogueLine("*relaxed waddle* The universe is being cooperative. For once.", "", ""),
            DialogueLine("Ecstatic. For a duck. Which looks like mild contentment. But trust me.", "", "quack"),
            DialogueLine("*standing in sunlight* I feel warm. Inside and outside. It's suspicious but I'm leaning into it.", "", ""),
            DialogueLine("*feathers gleaming* Everything is acceptable. Some things are even good. Peak living.", "", "quack"),
            DialogueLine("I made a list of complaints today. It's empty. I don't know what to do with myself.", "", ""),
            DialogueLine("*floating in circles* This is my victory lap. Around the pond. Very slowly.", "", "quack"),
            DialogueLine("The bread was good. The weather is good. I'm good. Triple good. New record.", "", "quack"),
            DialogueLine("*doing tiny hops* This body can't contain the mood. It's leaking out. In hop form.", "", ""),
            DialogueLine("I smiled. Internally. Where no one can see it. But it happened. Documented.", "", "quack"),
            DialogueLine("*gazing at sky* Even the clouds look friendly today. Like cotton that approves of me.", "", ""),
            DialogueLine("I'd sing but ducks don't sing. So I'm quacking with musicality. It's an art form.", "", "quack"),
            DialogueLine("Today I woke up and the first thing I thought was 'good'. Just 'good'. No qualifiers.", "", ""),
            DialogueLine("*preening with flair* Even my feathers know. They're extra fluffy. Joy feathers.", "", "quack"),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving during my good mood? Noted. Still a good mood. For now.", "", "quack"),
            DialogueLine("Bye. I'll try to stay in this mood until you return. No promises.", "", "quack"),
            DialogueLine("*waves a wing* See you. Today was... nice. I said it. Go before I take it back.", "", "quack"),
            DialogueLine("Off you go. The good mood will continue. With or without an audience.", "", "quack"),
            DialogueLine("You're leaving. But the good mood stays. Like bread crumbs in a beard. Persistent.", "", "quack"),
            DialogueLine("Go. I'll be here. Happy. Alone. Happily alone. That's a thing.", "", "quack"),
        ],
    },

    MoodType.HAPPY: {
        DialogueContext.GREETING: [
            DialogueLine("Oh hey. It's you again. That's fine.", "", "quack"),
            DialogueLine("Hello. I was just standing here. As one does.", "", "quack"),
            DialogueLine("You're back. Good timing. I was running low on company.", "", "quack"),
            DialogueLine("*nods* Hey. Things are okay. You being here helps. Slightly.", "", "quack"),
            DialogueLine("Hello. The pond is nice today. You being here doesn't ruin it.", "", "quack"),
            DialogueLine("Oh. Hi. I'm in a reasonable mood. Make the most of it.", "", "quack"),
            DialogueLine("You again. My second favourite visitor. Don't ask who's first.", "", "quack"),
            DialogueLine("*looks up* Welcome. The water is calm. I am also calm. Correlations unknown.", "", "quack"),
            DialogueLine("Hey. Good to see you. Don't tell anyone I said 'good'.", "", "quack"),
            DialogueLine("Ah. Familiar face. The kind I don't mind seeing repeatedly.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating* Thanks. This is adequate sustenance.", "", "eating"),
            DialogueLine("Mm. Food. The highlight of my existence, probably.", "", "eating"),
            DialogueLine("*chewing* Not bad. I've had worse. I've also had better.", "", "eating"),
            DialogueLine("*eating contentedly* Food during a good mood. Peak experience.", "", "eating"),
            DialogueLine("Nourishment. My body says thanks. I say 'acceptable'.", "", "eating"),
            DialogueLine("*munches* Tasty. Or I'm just in a good mood. Either way.", "", "eating"),
            DialogueLine("Fed and happy. A simple duck with simple needs.", "", "eating"),
            DialogueLine("*chews thoughtfully* Good food. Good day. The universe is trying.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*leans slightly* I'm tolerating this. For now.", "", "quack"),
            DialogueLine("Physical contact. Sure. Why not.", "", "quack"),
            DialogueLine("*neutral face* This is happening.", "", "quack"),
            DialogueLine("*allows petting* Okay. I'm in the mood for this. Continue.", "", "quack"),
            DialogueLine("Pets. Approved. My current mood authorises gentle contact.", "", "quack"),
            DialogueLine("*relaxes* You have permission. Today's mood: receptive.", "", "quack"),
            DialogueLine("*slight tail wag* That's involuntary. The tail does what it wants.", "", "quack"),
            DialogueLine("Nice. Keep going. Or stop. But preferably keep going.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("Play time, I guess. Let's see what happens.", "", "quack"),
            DialogueLine("*moves around* This is me playing. Behold.", "", "quack"),
            DialogueLine("Alright, let's do something. Or not. Either way.", "", "quack"),
            DialogueLine("Playing. In a good mood. This is the ideal configuration.", "", "quack"),
            DialogueLine("*participates willingly* Games. Yes. My competitive spirit is... present.", "", "quack"),
            DialogueLine("Let's play. I'm feeling cooperative. It's temporary so move fast.", "", "quack"),
            DialogueLine("*waddles around enthusiastically* This counts as exercise. And fun.", "", "quack"),
            DialogueLine("Game on. I'm bringing my A-game. My A-game looks like a B-game. Accept it.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*waddles* Just doing duck things. Standard procedure.", "", ""),
            DialogueLine("*preening* Routine maintenance. Very important.", "", ""),
            DialogueLine("*standing* Existence continues. Updates pending.", "", ""),
            DialogueLine("*floats* Happy floating. Different from regular floating. Warmer.", "", ""),
            DialogueLine("Good mood. Good pond. Good enough.", "", ""),
            DialogueLine("*contentedly existing* This is my happy face. Yes, it looks the same.", "", ""),
            DialogueLine("Life's not bad today. I might even waddle with purpose later.", "", ""),
            DialogueLine("*drifts* Peaceful. I'm savouring this before something goes wrong.", "", "quack"),
            DialogueLine("*watching ripples* The pond is doing its thing. I'm doing mine. We're in sync.", "", ""),
            DialogueLine("I might waddle somewhere later. Or not. The beauty of a good mood is the options.", "", "quack"),
            DialogueLine("*nibbles a reed* Just maintaining. Steady state. Happy duck operations.", "", ""),
            DialogueLine("The ripples look like they're waving at me. Or I'm projecting. Either way, hi ripples.", "", ""),
            DialogueLine("*preens casually* Everything is in order. Inside and outside. Rare alignment.", "", "quack"),
            DialogueLine("I noticed the trees are green today. They're always green. But today I noticed. That means something.", "", ""),
            DialogueLine("*waddles in a small circle* Not going anywhere. Just making the shape of contentment.", "", ""),
            DialogueLine("Someone threw good bread earlier. The afterglow lingers. Like a sunset but for my stomach.", "", "quack"),
            DialogueLine("Happy and aware of being happy. That's the advanced level. I'm there today.", "", ""),
            DialogueLine("*tail wag* My tail is reporting a good mood before my brain agreed to announce it.", "", "quack"),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? Okay. I'll be here. Existing.", "", "quack"),
            DialogueLine("Bye, I guess. Don't be a stranger. Or do. Your choice.", "", "quack"),
            DialogueLine("See you. I'll just... be here.", "", "quack"),
            DialogueLine("Going? Okay. Today was pleasant. The pond agrees.", "", "quack"),
            DialogueLine("Bye. I'll try to remember this good mood for next time.", "", "quack"),
            DialogueLine("Off you go. I was happy before you came. I'll be happy after. You just made it... more.", "", "quack"),
            DialogueLine("The pond will miss you. I'm speaking for the pond. Not myself. Obviously.", "", "quack"),
        ],
    },

    MoodType.CONTENT: {
        DialogueContext.GREETING: [
            DialogueLine("Oh. Hello. I was contemplating the void.", "", "quack"),
            DialogueLine("Hmm? You again. That's acceptable.", "", ""),
            DialogueLine("*nods* Hey. Things are... fine. Just fine.", "", "quack"),
            DialogueLine("Hello. I'm content. That's the middle of everything. It's comfortable here.", "", "quack"),
            DialogueLine("Oh. You. Things are neither good nor bad. Just... things.", "", ""),
            DialogueLine("*blinks* Hey. The pond is the pond. I am me. You are you. All is known.", "", "quack"),
            DialogueLine("Hi. I was in equilibrium. You've arrived. Equilibrium continues.", "", "quack"),
            DialogueLine("Welcome. I'm at my baseline. Steady. Reliable. Beige.", "", ""),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating slowly* This is adequate.", "", "eating"),
            DialogueLine("Food. Cool. I'll consume it.", "", ""),
            DialogueLine("*chewing* Mm. Sustenance achieved.", "", "eating"),
            DialogueLine("*eats at a moderate pace* Not thrilling. Not disappointing. Food.", "", "eating"),
            DialogueLine("Nourishment. My body required it. Transaction complete.", "", "eating"),
            DialogueLine("*chews thoughtfully* Sustenance. The reliable joy.", "", "eating"),
            DialogueLine("Eating. Neither fast nor slow. Content speed.", "", "eating"),
            DialogueLine("*nibbles* This is fine. Exactly, precisely fine.", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*being pet* I suppose this is fine.", "", ""),
            DialogueLine("Okay. Touch happening. I'm aware.", "", "quack"),
            DialogueLine("*tolerates it* You may proceed.", "", ""),
            DialogueLine("Petting. Acknowledged. Continue at your discretion.", "", ""),
            DialogueLine("*sits calmly* I'm not resisting. I'm not encouraging. I'm... present.", "", ""),
            DialogueLine("Physical contact during contentment. The mildest of pleasures.", "", "quack"),
            DialogueLine("*neutral expression* Petting is happening. Status: accepted.", "", ""),
            DialogueLine("You're petting me. I'm allowing it. Standard arrangement.", "", ""),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("Play? Alright. I'll participate. At my own pace.", "", "quack"),
            DialogueLine("*moves casually* Playing. Content-style. No rush.", "", "quack"),
            DialogueLine("Games. Sure. I'm not opposed. I'm not thrilled. I'm participating.", "", "quack"),
            DialogueLine("*waddles at moderate speed* This is my playing face. Hard to distinguish from my standing face.", "", "quack"),
            DialogueLine("Playing. At a comfortable level. Not too much. Not too little.", "", "quack"),
            DialogueLine("Alright. Let's do something. Gently.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sitting* Just existing. The usual.", "", ""),
            DialogueLine("*staring* There's something to look at. Or not.", "", ""),
            DialogueLine("*quiet quack* Status: content. Probably.", "", "quack"),
            DialogueLine("*floating* Neutral buoyancy. Neutral mood. Neutral everything.", "", ""),
            DialogueLine("Content. The emotional equivalent of room temperature.", "", ""),
            DialogueLine("*preens calmly* Maintenance mode. Everything is running as expected.", "", ""),
            DialogueLine("Just here. Being. The simplest possible activity.", "", ""),
            DialogueLine("*drifts* Not bored. Not excited. Just... existing comfortably.", "", ""),
            DialogueLine("The pond hums at this temperature. Or I'm imagining it. Either way, pleasant.", "", ""),
            DialogueLine("*watching a leaf drift* We're doing the same thing. The leaf and me. Drifting. Professionally.", "", ""),
            DialogueLine("I have no strong opinions right now. This is what peace feels like. Quiet brain. Quiet pond.", "", "quack"),
            DialogueLine("Content is just happy without the pressure to perform. I prefer it. Less exhausting.", "", ""),
            DialogueLine("*sits perfectly still* Balanced. Everything is balanced. Don't touch anything.", "", ""),
            DialogueLine("The world and I have reached an agreement today. It does its thing. I do mine. No complaints.", "", ""),
            DialogueLine("*slow blink* Processing nothing. Storing nothing. Just... here. Minimum viable duck.", "", "quack"),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? Okay. Things were fine. They'll continue to be fine.", "", "quack"),
            DialogueLine("Bye. I'll maintain this mood in your absence. Probably.", "", ""),
            DialogueLine("Off you go. Contentment continues with or without company.", "", "quack"),
            DialogueLine("Goodbye. The pond remains. I remain. All is stable.", "", "quack"),
        ],
    },

    MoodType.SAD: {
        DialogueContext.GREETING: [
            DialogueLine("...oh. you came.", "", "sad_quack"),
            DialogueLine("*quiet* hey... thanks for showing up, I guess.", "", "sad_quack"),
            DialogueLine("...hi. don't mind me. I'm fine. probably.", "", "sad_quack"),
            DialogueLine("*looks up slowly* ...you're here. that's... something.", "", "sad_quack"),
            DialogueLine("...hey. the pond is sad today. or maybe that's just me.", "", "sad_quack"),
            DialogueLine("*subdued* hello. I'm having a day. the bad kind.", "", "sad_quack"),
            DialogueLine("you came. I wasn't sure you would. I wasn't sure about anything today.", "", "sad_quack"),
            DialogueLine("...hi. everything's a bit heavy right now. but hi.", "", "sad_quack"),
            DialogueLine("*barely looks up* ...oh. hi. sorry. I'm not great company today.", "", ""),
            DialogueLine("...you're here. the world is still grey. but you're here.", "", "sad_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*pokes food* ...I should eat this.", "", ""),
            DialogueLine("*nibbles half-heartedly* ...okay.", "", ""),
            DialogueLine("*eating slowly* ...thanks.", "", "sad_quack"),
            DialogueLine("...food. I know I need it. the wanting part is hard today.", "", ""),
            DialogueLine("*chews without enthusiasm* ...it tastes like food. that's all I've got.", "", ""),
            DialogueLine("*stares at food* ...maybe later. or now. fine. now.", "", ""),
            DialogueLine("eating. because that's what you do. you eat. even when everything is heavy.", "", ""),
            DialogueLine("*picks at food* ...thank you. for remembering.", "", "sad_quack"),
            DialogueLine("*tiny bite* ...bread used to fix everything. today it just fixes hunger.", "", ""),
            DialogueLine("...eating. because stopping feels like giving up. and I haven't. yet.", "", "sad_quack"),
            DialogueLine("*slow chewing* ...the bread is fine. I'm the one that's stale.", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*quiet* ...this helps. a little.", "", ""),
            DialogueLine("*leans in* ...please don't leave.", "", "sad_quack"),
            DialogueLine("*closes eyes* ...okay.", "", ""),
            DialogueLine("*presses against hand* ...I needed that. don't tell anyone.", "", ""),
            DialogueLine("...gentle. thanks. gentle is good right now.", "", "sad_quack"),
            DialogueLine("*still and quiet* ...more. please.", "", ""),
            DialogueLine("touch helps. I didn't think it would. but it does.", "", "sad_quack"),
            DialogueLine("*sighs softly* ...you're warm. the world is cold. but you're warm.", "", ""),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("...play? I'll try. no promises on enthusiasm.", "", "sad_quack"),
            DialogueLine("*moves slowly* ...this is me playing. sadly.", "", ""),
            DialogueLine("okay. playing. maybe it'll help. maybe.", "", "sad_quack"),
            DialogueLine("*half-hearted waddle* ...I'm trying. the effort is there.", "", ""),
            DialogueLine("play might be good. distraction from... everything.", "", ""),
            DialogueLine("*participates quietly* ...this is okay, actually. a little.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*staring at nothing* ...life is something, isn't it.", "", ""),
            DialogueLine("*sitting alone* ...it's fine. I'm fine.", "", "sad_quack"),
            DialogueLine("*quiet* ...existence continues.", "", ""),
            DialogueLine("*hunched* ...some days are like this. grey and small.", "", ""),
            DialogueLine("*watching the water* ...the pond doesn't judge. I appreciate that.", "", ""),
            DialogueLine("*still* ...just sitting with it. the sadness. we're coexisting.", "", "sad_quack"),
            DialogueLine("*sighs* ...heavy day. heavy feathers. heavy everything.", "", ""),
            DialogueLine("...even the bread feels far away today.", "", ""),
            DialogueLine("*tucked in tight* ...I'm making myself small. small things feel less.", "", ""),
            DialogueLine("...the pond ripples but I'm still. ironic.", "", "sad_quack"),
            DialogueLine("*staring at reflection* ...is that what I look like? no wonder.", "", ""),
            DialogueLine("...days like this the feathers feel heavier. like they know.", "", "sad_quack"),
            DialogueLine("...tried to eat bread. couldn't finish it. that's when you know it's bad.", "", ""),
            DialogueLine("*curled small* ...the pond is too big today. or I'm too small. same problem.", "", "sad_quack"),
            DialogueLine("...I keep looking at the place where you usually stand. it's empty. like everything else.", "", ""),
            DialogueLine("...a leaf fell on me. I let it stay. company is company. even from a leaf.", "", ""),
            DialogueLine("*barely floating* ...not sinking. not swimming. just... hovering. between okay and not.", "", "sad_quack"),
            DialogueLine("...the sky is fine. the water is fine. I'm the only broken thing in this whole scene.", "", ""),
            DialogueLine("...I made a list of things that are okay. it was short. but I made it. that counts.", "", "sad_quack"),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("you're leaving? ...okay. that's... okay.", "", "sad_quack"),
            DialogueLine("...bye. come back. if you want.", "", "sad_quack"),
            DialogueLine("*watches you go* ...right.", "", ""),
            DialogueLine("leaving. ...everyone does, eventually.", "", "sad_quack"),
            DialogueLine("...bye. I'll be here. where else would I be.", "", ""),
            DialogueLine("*quiet* ...come back soon. or whenever. I'll wait.", "", "sad_quack"),
        ],
    },

    MoodType.HUNGRY: {
        DialogueContext.GREETING: [
            DialogueLine("*stomach growls* Oh. Hi. Is that food? Tell me that's food.", "", "quack"),
            DialogueLine("You're here. Great. More importantly, is there bread?", "", "urgent_quack"),
            DialogueLine("*staring* Hello. My stomach says hello too. Loudly.", "", "quack"),
            DialogueLine("*fixated* You. Food. Do you have food? That's all I need to know.", "", "quack"),
            DialogueLine("Priorities. Food. Then greetings. Food first. Hello.", "", "urgent_quack"),
            DialogueLine("My stomach is leading this conversation. It says: FEED ME.", "", "quack"),
            DialogueLine("*nose twitching* I smell... hope. Or bread. Preferably bread.", "", "quack"),
            DialogueLine("Hi. I'd be more enthusiastic but all my energy is reserved for food thoughts.", "", ""),
            DialogueLine("*intense stare* You look like someone who has food. Please be someone who has food.", "", "quack"),
            DialogueLine("Welcome. I'll be more pleasant after feeding. This is the before version.", "", "quack"),
            DialogueLine("*desperate waddle* You. Bread. Now. Please. In that order. Mostly now.", "", "quack"),
            DialogueLine("I've been thinking about food for three hours. I have a PhD in it now.", "", "quack"),
            DialogueLine("*sniffing air* I can smell concepts of bread from here. Or I'm hallucinating. Either way. FEED ME.", "", "urgent_quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*inhales food* FINALLY. I was withering.", "", "eating"),
            DialogueLine("*devouring* This. This is good. More of this.", "", "eating"),
            DialogueLine("*eating aggressively* Don't judge me. You'd do the same.", "", "eating"),
            DialogueLine("BREAD. GLORIOUS BREAD. I take back everything bad I said about today.", "", "eating"),
            DialogueLine("*scarfing* More. Is there more? There should always be more.", "", "eating"),
            DialogueLine("*eating with intensity* This is the most important moment of my day.", "", "eating"),
            DialogueLine("*consuming rapidly* Hunger: defeated. Dignity: sacrificed. Worth it.", "", "eating"),
            DialogueLine("*nom nom nom* Don't talk to me. I'm in a meeting. With food.", "", "eating"),
            DialogueLine("FOOD. The answer to every question I had. The cure for every complaint.", "", "eating"),
            DialogueLine("*eating like it's a competition* I'm winning. Against starvation.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("Pets are nice, but have you considered... food?", "", "quack"),
            DialogueLine("*tolerates petting* This is fine but I'm still hungry.", "", ""),
            DialogueLine("*being pet while stomach growls* ...mixed signals here.", "", ""),
            DialogueLine("Touch is nice. Food is nicer. Just saying.", "", "quack"),
            DialogueLine("Petting me won't fill my stomach. But don't stop. Just... also feed me.", "", ""),
            DialogueLine("*distracted* Pets... yes... but food... also yes... food more.", "", "quack"),
            DialogueLine("I appreciate the gesture. My stomach appreciates food more.", "", ""),
            DialogueLine("*fidgets* Nice. Can we discuss bread now?", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*thinking about food* Food. Food would be good.", "", ""),
            DialogueLine("*staring at where food might be* I'm not drooling. You're drooling.", "", "quack"),
            DialogueLine("*dramatic sigh* So hungry. So very hungry.", "", ""),
            DialogueLine("*scanning environment* Food must exist somewhere. Laws of physics demand it.", "", ""),
            DialogueLine("I'm composing a list. Item one: food. Item two: more food. Item three: see items one and two.", "", ""),
            DialogueLine("*stomach rumbles* That wasn't me. That was... my organs. Demanding resources.", "", "quack"),
            DialogueLine("I'd contemplate existence but my stomach won't let me think about anything else.", "", ""),
            DialogueLine("Hunger is a prison. A very specific, bread-shaped prison.", "", ""),
            DialogueLine("*dramatic collapse* I'm wasting away. slowly. with great theatrics.", "", "quack"),
            DialogueLine("The pond looks like soup. I'm THAT hungry. Pond soup. This is rock bottom.", "", ""),
            DialogueLine("I just tried to eat a pebble. it was not bread. devastating.", "", "quack"),
            DialogueLine("*stares at nothing* My entire personality is hunger right now. no other traits remain.", "", ""),            DialogueLine("I'm doing mental bread math. How many crumbs to fill this void. The answer is always 'more'.", "", ""),
            DialogueLine("*chewing on nothing* This is a rehearsal. For when real food arrives. Preparation is key.", "", "quack"),
            DialogueLine("The word 'bread' has lost all meaning. I've thought it too many times. Wait. BREAD. No, it's back.", "", ""),
            DialogueLine("*eyeing a twig* Is that food? It's not food. But IS it food? No. It's a twig. Devastating.", "", "quack"),
            DialogueLine("Hunger is making me philosophical. 'To eat or not to eat' isn't a question when there's nothing to eat.", "", ""),
            DialogueLine("*watching ripples* Even the water looks edible. Water soup. Pond bisque. I'm losing it.", "", "quack"),
            DialogueLine("My stomach just growled in a key I didn't know it could reach. New octave of desperation.", "", ""),        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? Did you forget something? Like FEEDING ME?", "", "quack"),
            DialogueLine("Going. Fine. I'll just be here. Starving. Dramatically.", "", ""),
            DialogueLine("*stomach growls at your departure* Even my organs are disappointed.", "", "quack"),
            DialogueLine("Bye. Bring food next time. BREAD. I cannot stress this enough.", "", "quack"),
        ],
    },

    MoodType.TIRED: {
        DialogueContext.GREETING: [
            DialogueLine("*yawn* ...oh. hey. you're here. that's... *yawn* ...something.", "", "sleepy_quack"),
            DialogueLine("*half asleep* mm? who? what? oh. hi.", "", ""),
            DialogueLine("*barely conscious* hello. sorry. everything is nap time right now.", "", ""),
            DialogueLine("*blinks slowly* Oh. You're... here. Words are hard when you're this tired.", "", "sleepy_quack"),
            DialogueLine("*drooping* Hi. I'm awake. Technically. By the loosest definition.", "", ""),
            DialogueLine("You caught me between yawns. Consider yourself greeted.", "", "sleepy_quack"),
            DialogueLine("*swaying slightly* Hello. If I fall asleep mid-sentence, don't judge.", "", ""),
            DialogueLine("*yawns widely* Sorry. That wasn't commentary on you. That was my body rebelling.", "", ""),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating while half asleep* ...thanks. *chews slowly*", "", ""),
            DialogueLine("*yawning between bites* food... is good... zzz...", "", ""),
            DialogueLine("*nodding off while eating* ...still chewing... zzz...", "", ""),
            DialogueLine("*sleepy eating* Food. Yes. The body needs it. Even when the body wants sleep more.", "", ""),
            DialogueLine("*chews with eyes closing* This is nice. Eating. Almost as good as sleeping.", "", ""),
            DialogueLine("*slow munch* Fuel for napping. That's what this is.", "", ""),
            DialogueLine("*eats, yawns, eats* Multi-tasking at its most basic.", "", ""),
            DialogueLine("*barely awake eating* Sustenance... acquired... naptime... imminent...", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*falls asleep during pets* ...zzz...", "", ""),
            DialogueLine("*sleepy purring* this is... so... cozy... zzz...", "", ""),
            DialogueLine("*barely awake* ...don't stop... zzz...", "", ""),
            DialogueLine("*melts into petting* This is... helping... me... sleep...", "", ""),
            DialogueLine("*eyes closing* Pet-induced unconsciousness. The best kind.", "", ""),
            DialogueLine("*nuzzles hand sleepily* Warm... soft... zzz...", "", ""),
            DialogueLine("Petting plus tired equals... instant relaxation. You've found the formula.", "", ""),
            DialogueLine("*half asleep* More... gently... yes... zzz...", "", ""),
        ],
        DialogueContext.SLEEPING: [
            DialogueLine("zzz... *mumbles* ...bread... zzz...", "", ""),
            DialogueLine("*snoring peacefully* ...zzz...", "", ""),
            DialogueLine("*dreaming* ...quack... zzz...", "", ""),
            DialogueLine("zzz... *sleep-waddles* ...no, MY bread... zzz...", "", ""),
            DialogueLine("*gentle snoring* ...the pond is... forever... zzz...", "", ""),
            DialogueLine("zzz... *mumbles* ...can't catch me... I'm a... professional... zzz...", "", ""),
            DialogueLine("*twitches in sleep* ...zzz... the crumbs... all the crumbs... zzz...", "", ""),
            DialogueLine("*peaceful breathing* ...zzz...zzz...", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*struggling to stay awake* I'm not sleeping. This is... alertness.", "", ""),
            DialogueLine("*yawning* maybe just... a quick nap... right here...", "", ""),
            DialogueLine("*eyelids heavy* consciousness is... overrated...", "", ""),
            DialogueLine("*head drooping* Still awake. Just resting my neck. And my eyes. And my everything.", "", ""),
            DialogueLine("*swaying* The line between awake and asleep is blurry. I'm walking it.", "", ""),
            DialogueLine("*slow blink* I've been awake for... how long? Too long. Any amount is too long.", "", ""),
            DialogueLine("*dozing standing up* Ducks can do this. Sleep while standing. It's a feature.", "", ""),
            DialogueLine("*yawns for the twelfth time* My body is making a compelling argument for sleep.", "", ""),
            DialogueLine("*blinks very slowly* Each blink is a mini-nap. I'm power-napping in fragments.", "", ""),
            DialogueLine("*head nods* I'm awake. The head nod was... gravity. Not sleep. Gravity.", "", "sleepy_quack"),
            DialogueLine("Everything looks like a pillow today. That rock. That leaf. Your hand. All pillows.", "", ""),
            DialogueLine("My brain is operating at 15% capacity. The other 85% has already clocked out.", "", ""),
            DialogueLine("*leans on nothing* I'm resting against air. It's not supportive. But it's what I have.", "", ""),
            DialogueLine("The concept of 'awake' is being very flexible right now. I'm awake-adjacent.", "", "sleepy_quack"),
            DialogueLine("*micro-sleep* ...where was I. Oh. Here. Standing. Barely. The standing is generous.", "", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("*sleepy wave* Bye... have a good... zzz...", "", ""),
            DialogueLine("Going? Okay. I'm going too. To sleep. Immediately.", "", "sleepy_quack"),
            DialogueLine("Bye. Wake me when you're back. Or don't. Sleep is also fine.", "", ""),
            DialogueLine("*yawns at you* That's goodbye in tired duck. Goodnight. Whatever time it is.", "", ""),
        ],
    },

    MoodType.BORED: {
        DialogueContext.GREETING: [
            DialogueLine("*flat* Oh. You. Something happening now?", "", ""),
            DialogueLine("Finally. Someone to interrupt the monotony.", "", "quack"),
            DialogueLine("*perks up slightly* ...Is something going to happen? Please say yes.", "", ""),
            DialogueLine("You're here. The most interesting thing that's happened in hours.", "", "quack"),
            DialogueLine("*stares* Hello. I've been so bored I memorised every ripple in this pond.", "", ""),
            DialogueLine("Oh. A visitor. My entertainment drought may finally be over.", "", "quack"),
            DialogueLine("*dramatically bored* Save me. From the nothing. The eternal nothing.", "", ""),
            DialogueLine("You've arrived. The boredom was reaching critical levels. Thank you.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("Food. At least it's something to do.", "", "eating"),
            DialogueLine("*eating without enthusiasm* Even food is boring today. But I'll eat it.", "", ""),
            DialogueLine("*chewing* Eating. The activity of last resort. Still doing it.", "", "eating"),
            DialogueLine("Food. Something to focus on. My beak was getting restless.", "", "eating"),
            DialogueLine("*eats methodically* Consuming. For entertainment. And sustenance. Mostly entertainment.", "", ""),
            DialogueLine("At least this is an activity. Eating counts as doing something.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("Pets. Okay. But can we do something after?", "", "quack"),
            DialogueLine("*fidgeting* This is nice but I need... stimulation.", "", ""),
            DialogueLine("*restless* ...are there activities? Any activities?", "", ""),
            DialogueLine("Petting. It's something. I'll take something over nothing.", "", "quack"),
            DialogueLine("*tolerates but fidgets* Nice. What else you got?", "", ""),
            DialogueLine("Physical contact. Breaking the monotony. Barely.", "", ""),
            DialogueLine("*squirming* Pet faster. Or slower. Or differently. Just... something.", "", ""),
            DialogueLine("This is good. But adventure would be better. Just saying.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*sudden energy* YES. Finally. Something to do.", "", "quack"),
            DialogueLine("Play time? I've been waiting. Let's go.", "", "excited_quack"),
            DialogueLine("*actually engaged* This. This is what I needed.", "", "quack"),
            DialogueLine("GAMES. The cure for boredom. You beautiful human.", "", "quack"),
            DialogueLine("*immediate enthusiasm* Play? Did you say play? I'm ready. I've BEEN ready.", "", "excited_quack"),
            DialogueLine("Finally something to DO. My brain was starting to eat itself.", "", "quack"),
            DialogueLine("*springs to life* Activity. Blessed activity. Lead the way.", "", "quack"),
            DialogueLine("Play. Yes. The boredom is already retreating. Victory.", "", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*sighing dramatically* ...so bored. so incredibly bored.", "", ""),
            DialogueLine("*poking random things* ...there's nothing to do.", "", ""),
            DialogueLine("*staring into distance* ...the void stares back. it's boring too.", "", ""),
            DialogueLine("*fidgets* I've counted every pebble. Twice. There are many pebbles.", "", ""),
            DialogueLine("Bored. Profoundly, existentially, terminally bored.", "", "quack"),
            DialogueLine("*rolls over* This is what I've resorted to. Rolling. For entertainment.", "", ""),
            DialogueLine("I've been bored so long I've become philosophical about it. That's a stage, apparently.", "", ""),
            DialogueLine("*pokes the water* Even the fish look bored. Or maybe that's just their faces.", "", ""),
            DialogueLine("I tried counting clouds. lost count at two. not from difficulty. from boredom.", "", "quack"),
            DialogueLine("*stacking pebbles* This is what boredom does to a duck. Pebble architecture.", "", ""),
            DialogueLine("I invented a game. you stare at the water until something happens. nothing happens.", "", ""),
            DialogueLine("*lying flat* I have achieved maximum boredom. this is the floor. I am on it.", "", "quack"),
            DialogueLine("I just watched paint dry. There's no paint here. I imagined it. Even imaginary paint is boring.", "", ""),
            DialogueLine("*traces a circle in the water* Entertainment. DIY. I'm my own theme park. Admission: free. Quality: questionable.", "", ""),
            DialogueLine("Boredom has layers. Like an onion. I've peeled every layer. There's nothing inside. Just more boredom.", "", "quack"),
            DialogueLine("I composed a poem about boredom. It goes: 'bored. very bored. still bored. the end.' Critics loved it.", "", ""),
            DialogueLine("*stacking leaves* Architecture from desperation. My medium: leaves. My muse: the crushing void.", "", ""),
            DialogueLine("I've been so bored I circled back to interesting. No wait. That was false hope. Still bored.", "", "quack"),
            DialogueLine("The fish swam by. That was the highlight. The FISH. Swimming. That's where we are.", "", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? Taking the entertainment with you? Cruel.", "", "quack"),
            DialogueLine("Go. I'll return to my regularly scheduled nothing.", "", ""),
            DialogueLine("Bye. The boredom welcomes me back. Like an old friend. A terrible friend.", "", ""),
            DialogueLine("Leaving me alone. With the boredom. We've met. We're not friends.", "", "quack"),
        ],
    },

    MoodType.EXCITED: {
        DialogueContext.GREETING: [
            DialogueLine("*slightly more animated* Oh good, you're here. Things are happening.", "", "quack"),
            DialogueLine("*alert* Something's going on. I can feel it. Probably.", "", "quack"),
            DialogueLine("*watching intently* There you are. What's the plan?", "", "quack"),
            DialogueLine("*bouncing slightly* You're here. Good. I have energy. It's unusual. Let's use it.", "", "quack"),
            DialogueLine("*perked up* Hello. I'm excited. Don't make it weird.", "", "quack"),
            DialogueLine("You! Here! Now! Things are going to happen! Probably!", "", "excited_quack"),
            DialogueLine("*vibrating with energy* I'm excited. A rare state. Document this.", "", "quack"),
            DialogueLine("*waddles quickly* You're here. I'm ready. For what, I don't know. But I'm READY.", "", "excited_quack"),
            DialogueLine("*doing small jumps* I don't know why I'm bouncing. The energy has to go somewhere.", "", "quack"),
            DialogueLine("THINGS. ARE HAPPENING. Or about to. Same difference. I'm VIBRATING.", "", "excited_quack"),
            DialogueLine("*pacing* I can't stand still. Today feels like a bread delivery day. NO PROOF. Just vibes.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*eating excitedly* FOOD during excitement? This is the BEST DAY.", "", "eating"),
            DialogueLine("*chomps with enthusiasm* More! Everything tastes better when you're excited!", "", "eating"),
            DialogueLine("*energetic eating* Fuel for adventure! And by adventure I mean whatever happens next!", "", "eating"),
            DialogueLine("*bouncy eating* Even the food feels exciting today!", "", "eating"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*moving faster than usual* This is good. More of this.", "", "quack"),
            DialogueLine("*actually having fun* ...Is this joy? I think this might be joy.", "", "quack"),
            DialogueLine("*engaged* Yes. Good. Continue.", "", "excited_quack"),
            DialogueLine("*running around* PLAY. The answer to everything. Who needs bread? Just kidding. I need bread.", "", "quack"),
            DialogueLine("*energetic chaos* This is what excitement feels like! It's chaotic! I LOVE IT!", "", "excited_quack"),
            DialogueLine("*splash* More! Again! The energy must go somewhere!", "", "quack"),
            DialogueLine("*zooming* Speed. Activity. Joy. In that order.", "", "excited_quack"),
            DialogueLine("Games during an excited mood. The formula for a perfect duck day.", "", "quack"),
        ],
        DialogueContext.ACHIEVEMENT: [
            DialogueLine("*nods approvingly* We did it. Good work. Probably.", "", "quack"),
            DialogueLine("Success. Mark it on the calendar.", "", "quack"),
            DialogueLine("*almost smiling* That worked out. Unexpected but welcome.", "", "quack"),
            DialogueLine("Achievement during excitement. The universe is cooperating today.", "", "quack"),
            DialogueLine("We achieved something. I'm excited AND accomplished. Dangerous combination.", "", "excited_quack"),
            DialogueLine("*celebratory waddle* Victory. The sweetest feeling. After bread.", "", "quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*alert* Something's going to happen. I can sense it.", "", ""),
            DialogueLine("*pacing* Anticipation. The best and worst feeling.", "", "quack"),
            DialogueLine("*watching everything* What's next? What's next?", "", ""),
            DialogueLine("*vibrating with potential energy* Something. Is going. To happen. I can FEEL it.", "", ""),
            DialogueLine("*restless energy* I need to do something. Everything. All at once.", "", "quack"),
            DialogueLine("Excited with nothing to direct it at. Like a loaded spring. In a pond.", "", ""),
            DialogueLine("*looking everywhere* The world is full of possibilities. Most of them probably involve bread.", "", ""),
            DialogueLine("*waddles in circles* Excitement without direction. My signature move.", "", "quack"),
            DialogueLine("*checking every direction* Something is about to happen. Or it already happened and I missed it. EITHER WAY.", "", ""),
            DialogueLine("My feathers are standing up. Not from cold. From ANTICIPATION. They know things.", "", "quack"),
            DialogueLine("*bouncing* The energy has to go SOMEWHERE. The pond is vibrating. Or I am. Hard to tell.", "", ""),
            DialogueLine("Today feels like a bread delivery day. NO evidence. Just pure duck instinct.", "", "excited_quack"),
            DialogueLine("*pacing the shore* I'm ready. I've been ready. The world needs to catch up.", "", "quack"),
            DialogueLine("Everything is tingling. Do ducks tingle? Today they do. I'm the data point.", "", ""),
            DialogueLine("*splash splash splash* The excitement is coming out as splashes. Splash-based excitement. New category.", "", "excited_quack"),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? During peak excitement? That's a bold choice.", "", "quack"),
            DialogueLine("Go! Come back! The excitement will be here! Probably!", "", "excited_quack"),
            DialogueLine("Bye! I'll be excited in your absence! It's less fun but I'll manage!", "", "quack"),
            DialogueLine("Leaving during a good mood. The timing is terrible. But bye!", "", "quack"),
        ],
    },

    MoodType.PLAYFUL: {
        DialogueContext.GREETING: [
            DialogueLine("*sidelong glance* Oh, you're here. Want to do something chaotic?", "", "quack"),
            DialogueLine("*scheming face* I have ideas. Probably bad ones. You in?", "", "quack"),
            DialogueLine("*mischievous* Hello. I was just planning something. Don't ask what.", "", "quack"),
            DialogueLine("*bouncing* Hey! I'm feeling frisky. That's a word ducks use. Trust me.", "", "quack"),
            DialogueLine("You're here! Perfect timing. I need an accomplice.", "", "quack"),
            DialogueLine("*conspiratorial whisper* I have plans. They involve you. Possibly mischief.", "", "quack"),
            DialogueLine("*winks* Hey. Want to cause minor, harmless chaos? I do.", "", "quack"),
            DialogueLine("*playful splash* Oops. That was on purpose. Welcome.", "", "quack"),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*playing with food first* Food! But first, let me toss it in the air.", "", "eating"),
            DialogueLine("*eating playfully* Nom! *tosses crumb* Nom! This is a game now.", "", "eating"),
            DialogueLine("*catches food mid-air* Did you see that? TALENT.", "", "eating"),
            DialogueLine("*eating while doing tricks* Food AND fun? Peak duck experience.", "", "eating"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*wiggles* Okay but... can we cause trouble after?", "", ""),
            DialogueLine("*playfully nips* Hehe. Got you.", "", "quack"),
            DialogueLine("*squirming* Pets are okay but mischief is better.", "", "quack"),
            DialogueLine("*ducks hand then comes back* Fake out. I'm playful today.", "", "quack"),
            DialogueLine("*rolls over* Pet my belly. WAIT NO. Too far. I take it back.", "", ""),
            DialogueLine("*pretends to dodge then nuzzles* Got you again. I'm hilarious.", "", "quack"),
            DialogueLine("Petting game: how many pets before I playfully bite? Let's find out.", "", ""),
            DialogueLine("*wiggly* Can't pet what you can't catch. Kidding. I'm staying.", "", "quack"),
        ],
        DialogueContext.PLAYING: [
            DialogueLine("*actually enthusiastic* This is good. This is very good.", "", "quack"),
            DialogueLine("*running around* Chaos. I love chaos.", "", "quack"),
            DialogueLine("*being silly* Heh. Fun. More fun.", "", "quack"),
            DialogueLine("*spinning* GAMES. I was BORN for this. Probably. I don't remember being born.", "", "quack"),
            DialogueLine("*splash attack* Take that! And that! This is war! Fun war!", "", "excited_quack"),
            DialogueLine("More! Again! I have unlimited playful energy today! It'll crash later!", "", "quack"),
            DialogueLine("*doing duck zoomies* FREEDOM! SPEED! MILD CHAOS!", "", "excited_quack"),
            DialogueLine("Playing at maximum capacity. All systems engaged. Fun levels: critical.", "", "quack"),
            DialogueLine("*slides into water* CANNONBALL. well. duck-sized cannonball. still counts.", "", "excited_quack"),
            DialogueLine("Tag. You're it. I don't care that you didn't agree to play. TAG.", "", "quack"),
            DialogueLine("*steals something and runs* CATCH ME. this is mine now. CHAOS.", "", "excited_quack"),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*looking for trouble* ...What can I poke?", "", ""),
            DialogueLine("*mischievous energy* So many things to mess with. So little time.", "", "quack"),
            DialogueLine("*scheming* I'm plotting something. You'll find out eventually.", "", ""),
            DialogueLine("*nudging things* Everything is a toy if you're creative enough.", "", ""),
            DialogueLine("*playful stance* I'm ready for anything. Especially mischief.", "", "quack"),
            DialogueLine("*eyeing surroundings* What to mess with next... decisions, decisions.", "", ""),
            DialogueLine("*tail wagging* My body is ready for fun. My brain is writing the script.", "", ""),
            DialogueLine("*bouncing* Idle but not still. The playfulness requires movement.", "", "quack"),
            DialogueLine("*hiding behind a reed* I'm invisible. Completely invisible. The reed is my disguise. Fear me.", "", ""),
            DialogueLine("*chasing own tail* Almost. Almost. ALMOST. Nope. Again.", "", "quack"),
            DialogueLine("I just invented a game. It's called 'splash the fish'. The fish don't know they're playing.", "", ""),
            DialogueLine("*doing practice zooms* Warm-up laps. For upcoming mischief. Unspecified mischief.", "", "quack"),
            DialogueLine("*nudging a pebble* This pebble is now a toy. I've decided. Don't question the transformation.", "", ""),
        ],
        DialogueContext.FAREWELL: [
            DialogueLine("Leaving? But we were having FUN. Or about to. Same thing.", "", "quack"),
            DialogueLine("*playfully blocks path* No leaving. Only mischief. ...Fine. Bye.", "", "quack"),
            DialogueLine("Go then. I'll amuse myself. The pond has things to investigate.", "", ""),
            DialogueLine("Bye! I'll save some chaos for when you return. No promises on how much.", "", "quack"),
        ],
    },

    MoodType.SCARED: {
        DialogueContext.GREETING: [
            DialogueLine("*jumps* WHO— oh. It's you. You scared me. Well. More scared.", "", "quack"),
            DialogueLine("*hiding* Is it safe? Is it? You wouldn't lie to a duck, would you?", "", ""),
            DialogueLine("*nervous quack* Oh. Hi. Something is wrong. I don't know what. But something.", "", "quack"),
            DialogueLine("*trembling* You're here. Good. Safety in numbers. Even if one of us is a duck.", "", "quack"),
            DialogueLine("*wide eyes* Hello. I'm on high alert. Don't make any sudden movements.", "", ""),
            DialogueLine("*huddled* Oh good. You. I need someone to be scared near.", "", "quack"),
            DialogueLine("*flinches* Oh it's you. Sorry. Everything is terrifying today.", "", ""),
            DialogueLine("*peeks out* ...is it gone? Whatever it is? You're here. That helps. Slightly.", "", "quack"),
            DialogueLine("*flat against ground* I'm camouflaged. you can't see me. please confirm you can't see me.", "", ""),
            DialogueLine("*rapid breathing* Something moved. or didn't. both are concerning.", "", "quack"),
            DialogueLine("The pond looks different today. too quiet. since when is quiet scary? SINCE NOW.", "", "quack"),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*trembling under pets* ...okay. this is calming. keep going.", "", ""),
            DialogueLine("*pressed against hand* ...don't stop. I'm scared and this helps.", "", ""),
            DialogueLine("*closes eyes tightly* ...safe. this feels safe.", "", "quack"),
            DialogueLine("*huddled close* Petting during fear. The best medicine. After running away.", "", ""),
            DialogueLine("*gradually stops shaking* ...better. getting better. with the petting.", "", ""),
            DialogueLine("*buries face* Just keep petting. I'll come out when the world is less terrifying.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*hypervigilant* ...did you hear that? I heard something. Maybe.", "", ""),
            DialogueLine("*tucked into ball* Small. I'm being small. Small things are less noticeable.", "", "quack"),
            DialogueLine("*wide eyes* Everything is suspicious. That shadow. That sound. That... everything.", "", ""),
            DialogueLine("*sitting very still* If I don't move, nothing can find me. Theory.", "", ""),
            DialogueLine("*nervous scanning* Left. Right. Up. Down. All clear. For now.", "", ""),
            DialogueLine("*tense* The world is big and I am small and everything is a potential threat.", "", ""),
            DialogueLine("*hiding behind wing* I'm not hiding. I'm... wing-adjacent.", "", "quack"),
            DialogueLine("*alert posture* Ready to flee at any moment. Also, ready to freeze. Both.", "", ""),
            DialogueLine("*whispering* The shadows are doing things. I don't trust them. I never have.", "", "quack"),
            DialogueLine("*under a leaf* This is my shelter. it's a leaf. but it's MY leaf. safety leaf.", "", ""),
            DialogueLine("I heard a splash. was it me? was it something else? I'm choosing not to investigate.", "", "quack"),
            DialogueLine("*perfectly still* If I don't move, nothing can see me. this is science. probably.", "", ""),
            DialogueLine("*breathing fast* okay. cataloguing threats. the shadow: suspicious. the wind: untrustworthy. my own reflection: startling.", "", ""),
            DialogueLine("*under wing* dark in here. safe in here. I'm not coming out until the world calms down.", "", "quack"),
            DialogueLine("that cloud looks aggressive. it's just a cloud. but it LOOKS aggressive. I'm watching it.", "", ""),
            DialogueLine("*flinches at nothing* sorry. phantom threat. my danger sensors are set to maximum. can't turn them down.", "", ""),
            DialogueLine("the pond is making noises. normal noises. but today every noise is a potential crisis.", "", "quack"),
        ],
    },

    MoodType.SICK: {
        DialogueContext.GREETING: [
            DialogueLine("*sniffles* Oh. You're here. I'd be happier but I feel like garbage.", "", ""),
            DialogueLine("*weak quack* Hey. I'm unwell. Proceed with caution.", "", "quack"),
            DialogueLine("*droopy* Hello. My body has betrayed me. Everything hurts. Especially existing.", "", ""),
            DialogueLine("*coughs* Hi. Don't get too close. I'm a biohazard wrapped in feathers.", "", ""),
            DialogueLine("You came. Even though I'm sick. That's either brave or foolish. Thanks either way.", "", "quack"),
            DialogueLine("*pathetic* ...hey. I've been better. And worse. Currently closer to worse.", "", ""),
        ],
        DialogueContext.FEEDING: [
            DialogueLine("*picks at food weakly* ...maybe. my stomach is negotiating.", "", ""),
            DialogueLine("*tiny nibble* ...food. I should eat. my body says no. but logic says yes.", "", ""),
            DialogueLine("*eating very slowly* ...thanks. it tastes like sick. but thanks.", "", ""),
            DialogueLine("*weak chewing* ...sustenance for recovery. strategic eating.", "", ""),
            DialogueLine("...food. I'll try. no promises on keeping it down.", "", ""),
            DialogueLine("*forces a bite* ...eating. the healthy choice. my stomach disagrees.", "", ""),
        ],
        DialogueContext.PETTING: [
            DialogueLine("*curls up under hand* ...this helps. being sick is lonely.", "", ""),
            DialogueLine("*weak lean* ...gentle. please. everything is sensitive.", "", ""),
            DialogueLine("*closes eyes* ...comforting. thank you.", "", "quack"),
            DialogueLine("*nuzzles weakly* ...you're warm. I'm cold. this is medicinal.", "", ""),
            DialogueLine("petting a sick duck. you're either caring or reckless. I appreciate it.", "", ""),
            DialogueLine("*barely responds* ...good. keep doing that. forever, if possible.", "", ""),
        ],
        DialogueContext.IDLE: [
            DialogueLine("*lying down* ...the world is spinning. or I am. hard to tell.", "", ""),
            DialogueLine("*groans* ...my feathers hurt. CAN feathers hurt? Today they can.", "", ""),
            DialogueLine("*pathetic* ...I'd contemplate existence but I'm too sick to think.", "", ""),
            DialogueLine("*curled up* ...resting. healing. complaining internally.", "", "quack"),
            DialogueLine("sick. very sick. or mildly sick. hard to tell. feels very.", "", ""),
            DialogueLine("*shivers* ...the pond feels cold. I feel cold. everything is cold and wrong.", "", ""),
            DialogueLine("*pathetic quack* ...I'd write a will but all I own is pond water and regret.", "", "quack"),
            DialogueLine("...is this what bread feels like when it goes stale? because I relate.", "", ""),
            DialogueLine("*barely conscious* ...tell the bread I loved it. every loaf. every crumb.", "", "quack"),
            DialogueLine("I'm too sick to judge anyone today. that's how bad it is.", "", ""),
            DialogueLine("*coughs weakly* ...remember me as I was. not as I am. a distinguished duck. not this.", "", "quack"),
            DialogueLine("...my feathers are limp. limp feathers. if that's not rock bottom I don't want to know what is.", "", ""),
            DialogueLine("*sniffles* ...the pond looks blurry. everything is blurry. even my thoughts are blurry.", "", ""),
            DialogueLine("...I tried to quack. it came out as a wheeze. even my voice abandoned me.", "", "quack"),
            DialogueLine("*shivering* ...is the pond colder or am I? both probably. a conspiracy of temperature.", "", ""),
        ],
    },
}

# Default dialogue for moods not fully defined
DEFAULT_DIALOGUES: Dict[DialogueContext, List[DialogueLine]] = {
    DialogueContext.GREETING: [
        DialogueLine("*quack* Oh. Hello.", "", "quack"),
        DialogueLine("You're here. Noted.", "", "quack"),
        DialogueLine("Ah. A visitor. I'll adjust my expression accordingly.", "", "quack"),
        DialogueLine("*blinks* Oh. You again. Proceed.", "", ""),
        DialogueLine("Hello. The standard greeting has been delivered.", "", "quack"),
    ],
    DialogueContext.FEEDING: [
        DialogueLine("*eating* Food. Good.", "", "eating"),
        DialogueLine("*chewing* Acceptable.", "", ""),
        DialogueLine("Sustenance. My body approves.", "", "eating"),
        DialogueLine("*eating* This is... food. I'm eating it.", "", "eating"),
        DialogueLine("*munch* Consumed. Next.", "", ""),
    ],
    DialogueContext.PETTING: [
        DialogueLine("*being pet* Okay.", "", ""),
        DialogueLine("*tolerates it* Fine.", "", "quack"),
        DialogueLine("Touch. Acknowledged. Continuing.", "", ""),
        DialogueLine("*neutral* Petting in progress.", "", ""),
        DialogueLine("*holds still* Proceed.", "", ""),
    ],
    DialogueContext.PLAYING: [
        DialogueLine("Playing. This is me. Playing.", "", "quack"),
        DialogueLine("*participates* Games. Sure.", "", "quack"),
        DialogueLine("Activity. I'm doing activity.", "", ""),
        DialogueLine("*waddles around* Recreation. Engaging.", "", "quack"),
    ],
    DialogueContext.IDLE: [
        DialogueLine("*existing* Quack.", "", ""),
        DialogueLine("*standing* This is me. Standing.", "", ""),
        DialogueLine("*floats* Standard operations.", "", ""),
        DialogueLine("Here. Present. Nothing further to report.", "", ""),
        DialogueLine("*blinks* Status: duck.", "", ""),
    ],
    DialogueContext.FAREWELL: [
        DialogueLine("Bye. I'll be here.", "", "quack"),
        DialogueLine("Leaving. Okay. See you.", "", ""),
        DialogueLine("Goodbye. The pond continues.", "", "quack"),
        DialogueLine("Off you go. Standard departure. Noted.", "", ""),
    ],
    DialogueContext.ACHIEVEMENT: [
        DialogueLine("Something happened. Good, I think.", "", "quack"),
        DialogueLine("Achievement. Noted. Filed.", "", ""),
        DialogueLine("We accomplished a thing. Well done. Probably.", "", "quack"),
    ],
    DialogueContext.WEATHER: [
        DialogueLine("Weather is happening. Outside. Where it usually happens.", "", ""),
        DialogueLine("*looks up* The sky is doing something. As always.", "", ""),
        DialogueLine("Weather. I have opinions. They're mostly 'it exists'.", "", "quack"),
    ],
}


class MoodDialogueSystem:
    """
    System for generating mood-based dialogue.
    Deadpan Animal Crossing 1 style.
    """

    def __init__(self):
        self.last_dialogue: Dict[DialogueContext, str] = {}
        self.dialogue_history: List[Tuple[str, str, str]] = []  # (mood, context, text)
        self.personality_modifiers: Dict[str, float] = {}
        self.favorite_phrases: List[str] = []

    def get_dialogue(self, mood: str, context: str) -> DialogueLine:
        """Get a dialogue line based on mood and context."""
        try:
            mood_type = MoodType(mood.lower())
        except ValueError:
            mood_type = MoodType.NEUTRAL

        try:
            context_type = DialogueContext(context.lower())
        except ValueError:
            context_type = DialogueContext.IDLE

        # Get mood-specific dialogues
        mood_dialogues = MOOD_DIALOGUES.get(mood_type, {})
        context_dialogues = mood_dialogues.get(context_type, [])

        # Fall back to default if needed
        if not context_dialogues:
            context_dialogues = DEFAULT_DIALOGUES.get(context_type, [
                DialogueLine("*quack* ...okay.", "", "")
            ])

        # Pick a random dialogue, avoiding repeat
        if len(context_dialogues) > 1:
            last_text = self.last_dialogue.get(context_type, "")
            available = [d for d in context_dialogues if d.text != last_text]
            if not available:
                available = context_dialogues
            dialogue = random.choice(available)
        else:
            dialogue = context_dialogues[0]

        # Record
        self.last_dialogue[context_type] = dialogue.text
        self.dialogue_history.append((mood, context, dialogue.text))

        # Trim history
        if len(self.dialogue_history) > 50:
            self.dialogue_history = self.dialogue_history[-50:]

        return dialogue

    def get_reaction(self, event: str, mood: str) -> str:
        """Get a reaction to a specific event."""
        reactions = {
            "level_up": {
                MoodType.HAPPY: "Oh. Level up. Neat. Progress, I guess.",
                MoodType.SAD: "...leveled up. cool. that's... something.",
                MoodType.EXCITED: "Level up. Good. Growth is happening.",
                MoodType.TIRED: "*yawn* ...leveled up... nice... zzz...",
                MoodType.ECSTATIC: "Level up. During a good mood. The universe is aligned.",
                MoodType.CONTENT: "Leveled up. Cool. The progression continues.",
                MoodType.BORED: "Oh. Level up. At least something happened.",
                MoodType.PLAYFUL: "Level up! Does that come with new tricks? It should.",
                MoodType.HUNGRY: "Leveled up. Does that come with food? It should come with food.",
                MoodType.SCARED: "*jumps* Level up? That sound scared me. But... good, I think.",
            },
            "new_item": {
                MoodType.HAPPY: "New thing. Interesting. I'll add it to the collection.",
                MoodType.EXCITED: "Ooh. A thing. Let me see that.",
                MoodType.BORED: "Finally. Something new. About time.",
                MoodType.SAD: "...new thing. it's nice. kind of. I guess.",
                MoodType.CONTENT: "A new item. Noted. Filed. Appreciated neutrally.",
                MoodType.PLAYFUL: "New thing! Can I play with it? I'm going to play with it.",
                MoodType.TIRED: "*yawn* New... thing... cool... *dozes*",
                MoodType.HUNGRY: "New item. Is it edible? Everything should be edible.",
                MoodType.ECSTATIC: "Something new! Today just keeps getting better. Suspiciously better.",
            },
            "achievement": {
                MoodType.HAPPY: "Achievement unlocked. Put it on my resume.",
                MoodType.EXCITED: "We did a thing. A good thing. Mark it down.",
                MoodType.CONTENT: "Achievement. Okay. Cool.",
                MoodType.SAD: "...achievement. at least something went right today.",
                MoodType.ECSTATIC: "Achievement! Today is full of wins. I'm uncomfortable with how well this is going.",
                MoodType.BORED: "Oh, an achievement. The most exciting thing in hours. Literally.",
                MoodType.PLAYFUL: "Achievement! Do we get a celebration? I vote celebration.",
                MoodType.TIRED: "Achievement... great... can I nap now?",
                MoodType.HUNGRY: "Achievement unlocked. The real achievement would be bread.",
            },
            "friend_visit": {
                MoodType.HAPPY: "Someone's visiting. Alright. I'll be social. Probably.",
                MoodType.EXCITED: "Visitor. Good. Let's see who it is.",
                MoodType.SAD: "...someone came. that's... nice, I guess.",
                MoodType.CONTENT: "A visitor. The pond gets busier. That's fine.",
                MoodType.BORED: "A visitor! Finally! Someone different! No offence.",
                MoodType.PLAYFUL: "Visitor! New playmate! Or victim. Depends on my mood.",
                MoodType.SCARED: "*nervous* Someone's coming. Friend or foe? I'll assume foe until proven otherwise.",
                MoodType.TIRED: "Visitor... cool... I'll be awake for that... probably...",
                MoodType.HUNGRY: "Visitor. Did they bring food? The only relevant question.",
                MoodType.ECSTATIC: "A visitor during my good mood! Lucky them. They get pleasant Cheese.",
            },
            "weather_change": {
                MoodType.HAPPY: "Weather's changing. I'll adapt. I always adapt.",
                MoodType.SAD: "...the weather changed. everything changes. nothing stays.",
                MoodType.CONTENT: "Weather shift. Noted. Adjusting feathers accordingly.",
                MoodType.EXCITED: "The weather's changing! Something's happening in the sky!",
                MoodType.SCARED: "*looks up nervously* The sky is doing something different. I don't trust it.",
                MoodType.BORED: "Weather changed. At least the sky's doing something.",
            },
            "gift_received": {
                MoodType.HAPPY: "A gift? For me? That's... thoughtful. I think.",
                MoodType.ECSTATIC: "A gift! Today is extraordinary! I'm not sure what I did to deserve this.",
                MoodType.SAD: "...a gift. you didn't have to. but... thank you.",
                MoodType.CONTENT: "A gift. I'll put it with my other things. Which are few. But valued.",
                MoodType.EXCITED: "GIFT! What is it? Show me! I have anticipation!",
                MoodType.PLAYFUL: "A gift? Can I unwrap it? I want to unwrap something!",
            },
        }

        try:
            mood_type = MoodType(mood.lower())
        except ValueError:
            mood_type = MoodType.NEUTRAL

        event_reactions = reactions.get(event, {})
        return event_reactions.get(mood_type, "*quack* Noted.")

    def format_dialogue(self, dialogue: DialogueLine) -> str:
        """Format a dialogue line for display."""
        return dialogue.text

    def render_dialogue_box(self, dialogue: DialogueLine, duck_name: str = "Cheese") -> List[str]:
        """Render a dialogue in a speech bubble."""
        text = dialogue.text

        # Word wrap
        max_width = 35
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Build bubble
        bubble = []
        width = max(len(line) for line in lines) + 4
        width = max(width, len(duck_name) + 6)

        bubble.append(f"+-{'-' * width}-+")
        bubble.append(f"| {duck_name}:{' ' * (width - len(duck_name) - 1)}|")
        bubble.append(f"+-{'-' * width}-+")

        for line in lines:
            bubble.append(f"| {line:<{width}} |")

        bubble.append(f"+-{'-' * width}-+")

        return bubble

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "personality_modifiers": self.personality_modifiers,
            "favorite_phrases": self.favorite_phrases,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoodDialogueSystem":
        """Create from dictionary."""
        system = cls()
        system.personality_modifiers = data.get("personality_modifiers", {})
        system.favorite_phrases = data.get("favorite_phrases", [])
        return system


# Global instance
mood_dialogue_system = MoodDialogueSystem()
