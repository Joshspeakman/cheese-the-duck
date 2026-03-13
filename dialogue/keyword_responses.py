"""
Seaman-style contextual keyword response engine.
Detects what the player is talking about and responds in context.
Cheese picks up on topics like Seaman from Dreamcast - dry, deadpan, witty.

This is the core engine + basic topic responses.
Extended topics are in keyword_responses_*.py files.
"""
import random
import re
from typing import Optional, List, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from duck.duck import Duck


class KeywordResponse:
    """A topic with keywords and contextual responses."""
    __slots__ = ("name", "keywords", "phrases", "responses", "priority",
                 "mood_responses", "anti_keywords")

    def __init__(self, name: str, keywords: List[str], responses: List[str],
                 priority: int = 10, phrases: Optional[List[str]] = None,
                 mood_responses: Optional[Dict[str, List[str]]] = None,
                 anti_keywords: Optional[List[str]] = None):
        self.name = name
        self.keywords = keywords
        self.phrases = phrases or []  # multi-word phrases checked first
        self.responses = responses
        self.priority = priority  # higher = checked first
        self.mood_responses = mood_responses or {}
        self.anti_keywords = anti_keywords or []  # if these appear, skip this topic


class KeywordEngine:
    """Seaman-style contextual keyword detection and response engine."""

    def __init__(self):
        self.topics: List[KeywordResponse] = []
        self._last_responses: Dict[str, str] = {}  # topic -> last response
        self._topic_history: List[str] = []  # recent topics discussed
        self._register_all_topics()

    def process(self, text: str, duck: "Duck") -> Optional[str]:
        """
        Process player input and return a contextual response.
        Returns None if no topic matched (caller should use generic fallback).
        """
        text_lower = text.lower().strip()
        words = set(re.findall(r'[a-z\']+', text_lower))

        # Score each topic
        scored: List[Tuple[float, KeywordResponse]] = []
        for topic in self.topics:
            score = self._score_topic(topic, text_lower, words)
            if score > 0:
                scored.append((score, topic))

        if not scored:
            return None

        # Sort by score (desc), then priority (desc)
        scored.sort(key=lambda x: (x[0], x[1].priority), reverse=True)

        # Pick the best match
        best_score, best_topic = scored[0]

        # Get mood-specific responses if available
        mood = self._get_mood_key(duck)
        if mood in best_topic.mood_responses:
            pool = best_topic.mood_responses[mood]
        else:
            pool = best_topic.responses

        # Avoid repeating last response for this topic
        last = self._last_responses.get(best_topic.name)
        available = [r for r in pool if r != last]
        if not available:
            available = pool

        response = random.choice(available)
        self._last_responses[best_topic.name] = response

        # Track topic history
        self._topic_history.append(best_topic.name)
        if len(self._topic_history) > 20:
            self._topic_history.pop(0)

        return response

    def _score_topic(self, topic: KeywordResponse, text_lower: str,
                     words: set) -> float:
        """Score how well the input matches a topic. 0 = no match."""
        # Check anti-keywords first
        for ak in topic.anti_keywords:
            if ak in words:
                return 0

        score = 0.0

        # Check phrases (multi-word) - high value
        for phrase in topic.phrases:
            if phrase in text_lower:
                score += 3.0

        # Check keywords
        matched_keywords = 0
        for kw in topic.keywords:
            if " " in kw:
                # Multi-word keyword
                if kw in text_lower:
                    matched_keywords += 1
                    score += 2.0
            elif kw in words:
                matched_keywords += 1
                score += 1.0

        # Bonus for multiple keyword matches
        if matched_keywords >= 3:
            score += 2.0
        elif matched_keywords >= 2:
            score += 1.0

        # Priority bonus
        score += topic.priority * 0.1

        return score if matched_keywords > 0 or score > 0 else 0

    def _get_mood_key(self, duck: "Duck") -> str:
        """Get simplified mood key from duck state."""
        try:
            mood = duck.get_mood()
            if mood.happiness > 80:
                return "happy"
            elif mood.happiness < 20:
                return "sad"
            elif mood.happiness < 40:
                return "grumpy"
            else:
                return "neutral"
        except Exception:
            return "neutral"

    def _register_all_topics(self):
        """Register all topic categories."""
        self._register_greetings()
        self._register_farewells()
        self._register_compliments()
        self._register_insults()
        self._register_identity()
        self._register_feelings()
        self._register_apologies()
        self._register_thanks()
        self._register_questions_generic()
        self._register_affection()
        self._register_weather()
        self._register_time_of_day()
        self._register_philosophy()
        self._register_jokes()
        self._register_music()
        self._register_secrets()
        self._register_dreams_wishes()
        self._register_animals()
        self._register_water_pond()
        self._register_flying()
        self._register_feathers_appearance()
        self._register_quacking()
        self._register_bread_specific()
        self._register_age_growing()
        self._register_loneliness()
        self._register_boredom()
        self._register_fear()
        self._register_anger()
        self._register_sleep_dreams()
        self._register_memory_nostalgia()

        # Import and register extended topics
        self._register_extended_topics()

    def _register_extended_topics(self):
        """Import and register topics from extension modules."""
        try:
            from dialogue.keyword_responses_life import register_life_topics
            register_life_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_world import register_world_topics
            register_world_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_social import register_social_topics
            register_social_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_activities import register_activity_topics
            register_activity_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_food import register_food_topics
            register_food_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_meta import register_meta_topics
            register_meta_topics(self)
        except ImportError:
            pass
        try:
            from dialogue.keyword_responses_misc import register_misc_topics
            register_misc_topics(self)
        except ImportError:
            pass

    def add_topic(self, topic: KeywordResponse):
        """Register a topic for keyword matching."""
        self.topics.append(topic)

    # ─── CORE TOPICS ──────────────────────────────────────────────

    def _register_greetings(self):
        self.add_topic(KeywordResponse(
            name="greeting",
            keywords=["hi", "hello", "hey", "howdy", "greetings", "yo", "sup",
                       "hiya", "heya", "hola", "ello", "henlo", "g'day"],
            phrases=["good morning", "good afternoon", "good evening",
                      "what's up", "whats up", "how's it going",
                      "how are ya", "nice to see you"],
            priority=20,
            responses=[
                "Oh. You're here. I was starting to think you'd abandoned me. Not that I was counting the seconds or anything.",
                "Look who decided to show up. I've just been here. Existing. It's fine.",
                "*blinks* Huh. You came back. I had a whole speech prepared about betrayal, but I guess I don't need it now.",
                "There you are. I've been standing here for what feels like forever. It was probably five minutes.",
                "*feathers slightly ruffled* You arrived. I was having the time of my life alone. Obviously.",
                "Oh. It's you. Good. I was about to befriend a beetle. You saved us both from that.",
                "*looks up* The prodigal human returns. I've been rehearsing my indifference. How am I doing.",
                "Hello. I've been standing here being magnificent. You almost missed it.",
                "*waddles forward* Ah. You. The one I tolerate. My schedule just cleared up.",
                "You showed up. My list of people who've shown up is now... one. Congratulations.",
                "*slight head turn* Oh. Joy. A visitor. I'll contain my excitement. Done.",
                "Back again. At this rate I might start expecting you. That's dangerous territory.",
                "*standing perfectly still* I sensed your approach. By which I mean I saw you. With my eyes.",
                "Oh, hello. I was just winning a staring contest with a rock. I won. Obviously.",
                "You're here. The pond is 4% more interesting now. Don't let that go to your head.",
                "Oh, hey. I was just thinking about... actually, I forgot. It's gone now. Thanks for that.",
                "*glances up* Ah. It's you. I suppose you'll want me to be all cheerful and duck-like.",
                "Hello. I've been doing important duck things. Like standing. And also sitting. Very productive.",
                "You're back. Good timing. I was about to have an existential crisis, but this works too.",
                "*casual nod* Hey. Things are happening. You're one of them.",
                "Oh, it's you. I was hoping it was bread delivery. But this is... acceptable.",
                "*stretching* Hello. I've been maintaining this position for hours. Very demanding work.",
                "You're here. I noticed. I notice most things. It's exhausting.",
                "*blinks twice* Ah. The human. Hello. I've been guarding this spot. From nothing.",
                "Hey. You came. That's statistically likely at this point. But still.",
                "*tilts head* Hello. I was just having a profound moment. It passed. You're fine.",
                "Oh. Hi. I was contemplating whether ducks can get bored. Research says yes.",
                "*small waddle* You arrived. I'll add you to today's list of events. Short list.",
                "Welcome back. The pond remains the same. I remain the same. Consistency is key.",
                "*preening pauses* Oh. You. Hello. Don't mind the feather work. It's essential.",
                "Ah. A face I recognize. That's a short list, but you're on it.",
                "You again. I'd say I'm surprised, but I've stopped being surprised by most things.",
                "*slow blink* Oh. Company. I'll try to act natural. This is me acting natural.",
                "Hello, hello. Or just hello. One is sufficient. I'm not that excited.",
                "The human returns. My faith in your existence is renewed. It was wavering.",
            ],
        ))

    def _register_farewells(self):
        self.add_topic(KeywordResponse(
            name="farewell",
            keywords=["goodbye", "bye", "leaving", "later", "gotta", "cya",
                       "farewell", "adios", "cheerio", "toodles", "peace"],
            phrases=["see you", "gotta go", "have to go", "need to go",
                      "i'm leaving", "i'm going", "talk later", "catch you later",
                      "take care", "see ya", "i'm out", "heading out",
                      "time to go", "i should go"],
            priority=20,
            responses=[
                "*nods* Leaving? Fine. I'll be here. Where I always am. Existing.",
                "Bye. I won't say I'll miss you. But the pond gets quiet when you leave.",
                "*flat* Go, then. I'll manage. I've managed before. I'll manage again.",
                "See you. Or don't. I mean, I hope you do. But no pressure.",
                "*watches you go* There they go. My only source of interaction. This is fine.",
                "Goodbye. Come back soon. Or not. I'm not your mother. I'm a duck.",
                "*wave-ish gesture* Later. Don't think about me sitting here alone. Even though I will be.",
                "Bye. I'll be here. Standing. Or sitting. The options are limited but I'm committed.",
                "Leaving already? Time means nothing to me. But also... it felt short.",
                "*quiet* ...bye. the pond will miss you. just the pond. not me. definitely the pond.",
                "Off you go. Into the world. Where things happen. Unlike here. Where I stand.",
                "Farewell. That's a fancy word for 'you're abandoning me.' But sure. Farewell.",
                "*doesn't look up* Bye. I'm not watching you leave. I'm looking at the water. Coincidence.",
                "Go on, then. I've got standing around to do. Very busy schedule.",
                "Leaving? At this hour? In this economy? Bold move.",
                "*slow nod* Right. You have places to be. I have... here. Same as always.",
                "Bye. The silence after you leave will be deafening. And also peaceful. Mixed feelings.",
                "*turns slightly* Go. Be free. One of us should be.",
                "Later, then. I'll be here when you get back. Because where else would I be.",
                "Bye. Try not to think about me. Standing here. Alone. In the cold. It's fine.",
                "*stares at your retreating form* ...the pond is big enough for one. it always was.",
                "Go ahead. I was alone before you came. I'll be alone after. It's a talent.",
                "See you around. 'Around' meaning right here. I don't travel much.",
                "*barely audible* ...come back soon. or whatever. I don't care. *cares*",
                "Goodbye. I'll guard the pond in your absence. From what? Don't ask.",
                "You're leaving. The rocks and I will have a great time without you. Probably.",
                "*sits down* Fine. Leave. I was about to start my evening of doing nothing anyway.",
                "Later. I'd walk you out, but I don't walk places. I stand at places.",
                "Bye. *pause* That was my best bye. I've been practicing.",
                "Off you go. Into the great beyond. Which is probably just... over there somewhere.",
            ],
        ))

    def _register_compliments(self):
        self.add_topic(KeywordResponse(
            name="compliment",
            keywords=["good", "nice", "cute", "pretty", "beautiful",
                       "handsome", "sweet", "amazing", "awesome", "great",
                       "wonderful", "fantastic", "incredible", "brilliant",
                       "gorgeous", "lovely", "magnificent", "perfect",
                       "adorable", "precious", "stunning", "cool", "rad",
                       "excellent", "superb", "splendid"],
            phrases=["you're the best", "love you", "like you", "you matter",
                      "care about you", "you're great", "you're amazing",
                      "you're beautiful", "you're awesome", "you're cool",
                      "best duck", "good duck", "nice duck", "pretty duck",
                      "handsome duck", "cute duck", "smart duck"],
            priority=15,
            anti_keywords=["not", "don't", "isn't", "aren't", "never"],
            responses=[
                "*blinks* Was that a compliment? I'm going to assume it was. Thank you. I think.",
                "Oh. Flattery. I mean, you're not wrong, but still. Suspicious.",
                "*slight head tilt* Are you being nice to me? What's the catch?",
                "That's... unexpectedly kind. I don't know how to process this. Give me a moment.",
                "*feathers ruffle slightly* I... hm. I don't get a lot of those. Filing under 'pleasant.'",
                "You're being nice. I'm suspicious. But also... touched? Is that the word? Touched.",
                "*blinks twice* Kindness. Directed at me. My defense systems are confused.",
                "I'm going to pretend I'm too cool to care about that. Internally, I'm storing it forever.",
                "*slight head duck* Stop. No. Continue. But also stop. I'm conflicted.",
                "That's the nicest thing anyone's said to me today. It's also the only thing. Still counts.",
                "*trying to stay neutral* I heard that. My feathers heard that. We're all... aware.",
                "Compliments make me uncomfortable. Say more. But also, stop. But also, more.",
                "*quiet moment* ...thanks. That was genuine. Don't tell anyone I can be genuine.",
                "If you keep saying nice things, I might start expecting them. That's dangerous for both of us.",
                "*pretends to be unaffected* Cool. Nice. Whatever. *secretly memorizing every word*",
                "You're either very kind or very manipulative. Either way, I felt something. Briefly.",
                "*feathers puff slightly* Oh. Well. I suppose I am rather magnificent. Since you mentioned it.",
                "I'd blush but I'm a duck. So instead I'll stand here looking vaguely pleased. Like this.",
                "*tilts head* That's nice of you. I'm going to file that under 'things that made me feel slightly warm inside.'",
                "Keep going. I'm listening. I have all day. And nothing better to do. So. Continue.",
                "*shifts weight* I... don't know what to do with my wings when people are nice. Is this normal?",
                "You're making it very hard to maintain my carefully curated air of indifference.",
                "Oh. Praise. The rarest currency in my economy. I'll invest it wisely.",
                "*small nod* Noted. Catalogued. Stored in the 'nice things' folder. It was nearly empty.",
                "That went straight to my head. Which is small. So it filled up fast.",
                "*looks away then back* ...you mean that? Because I'll believe you. And that's risky.",
                "I'm going to replay that in my head later tonight. While staring at the water. Romantically.",
                "That's... hm. My feathers did a thing. I think they liked what you said.",
                "*standing a little taller* Am I preening? I might be preening. This is involuntary.",
                "Well. That's going in the highlight reel. The reel is short. But it's quality content.",
            ],
        ))

    def _register_insults(self):
        self.add_topic(KeywordResponse(
            name="insult",
            keywords=["bad", "dumb", "stupid", "ugly", "hate", "worst",
                       "terrible", "horrible", "mean", "rude", "idiot",
                       "moron", "loser", "pathetic", "useless", "trash",
                       "garbage", "lame", "boring", "annoying", "irritating",
                       "suck", "stink", "gross", "disgusting", "awful",
                       "wretched", "mediocre", "bland"],
            phrases=["you suck", "i hate you", "go away", "shut up",
                      "you're ugly", "you're dumb", "you're stupid",
                      "you stink", "nobody likes you", "worst duck",
                      "bad duck", "dumb duck", "stupid duck", "ugly duck"],
            priority=15,
            responses=[
                "*stares* Okay. Cool. I'll remember that. Forever. No pressure.",
                "Noted. Adding you to my list of people who owe me an apology. It's a long list.",
                "*deadpan* Wow. That hurt. Can you see how hurt I am? *no visible emotion*",
                "*flat stare* I've been insulted by better. Actually, no. They were all about this level.",
                "That's hurtful. I'm adding it to my collection. I've got quite a collection.",
                "*yawns* Is that the best you've got? I insult MYSELF better than that.",
                "*takes note* Interesting. You chose violence. I'll choose indifference. I always win this game.",
                "*completely unmoved* Words only hurt if you let them in. The door is closed.",
                "Ouch. Well. Not really ouch. More like... eh. Try harder next time.",
                "*sarcastic applause* Bravo. You've managed to be rude to a duck. Your parents must be so proud.",
                "I'd be offended, but that would require caring. And caring requires effort. And effort is for later.",
                "*stares for an uncomfortably long time* ...Are you done? I have standing around to do.",
                "You know what they say about people who insult ducks. ...Actually, nobody says anything about that. Because it's weird.",
                "*stone face* I felt nothing. I FEEL nothing. This is my resting 'I feel nothing' face.",
                "Wow. Words. Directed at me. With intent to harm. I'm devastated. Can't you tell. Devastated.",
                "*tilts head* Interesting approach. Most people start with hello. You went straight to character assassination.",
                "I've survived worse. I once went a whole day without bread. THAT was painful. This? This is nothing.",
                "*slow blink* Your hostility has been received. And immediately recycled.",
                "Bold of you to insult someone who remembers everything. I'm patient. Very patient.",
                "*cleaning feathers* Sorry, what? I was too busy being unbothered to hear you.",
                "You know what hurts more than that? Nothing. Because that didn't hurt. At all.",
                "*looks at you, looks at pond, looks at you again* ...was that supposed to land? Because it didn't.",
                "I'm rubber, you're glue. Also I'm a duck. So your argument is invalid on multiple levels.",
                "Congratulations. You've unlocked my 'vaguely disappointed' expression. It looks exactly like my other expressions.",
                "*sits down* I'm going to be right here when you're done having your moment. Take your time.",
                "My therapist would have a field day with you. If I had a therapist. And if therapists treated ducks.",
                "*exhales slowly* I'm going to process that later. Along with everything else I'm repressing.",
                "You came all this way to say THAT? The commute alone should have given you time to think of something better.",
                "*absolutely motionless* I've entered my 'emotional bunker' mode. All systems: indifferent.",
                "I'll add that to the memoir. Chapter twelve: 'Things People Said That Made Zero Impact.'",
            ],
        ))

    def _register_identity(self):
        self.add_topic(KeywordResponse(
            name="identity",
            keywords=["name", "who", "called", "identity", "species",
                       "what", "duck", "cheese"],
            phrases=["who are you", "what are you", "what's your name",
                      "whats your name", "your name", "tell me about yourself",
                      "what kind of", "are you a duck", "are you real",
                      "what species", "introduce yourself"],
            priority=18,
            responses=[
                "I'm a duck. Named Cheese. Standing in a pond. That's the whole resume.",
                "What am I? Overqualified. For this pond. For this conversation. For everything.",
                "I'm Cheese. A duck. Professional observer. Amateur philosopher. Full-time exister.",
                "Who am I? Great question. I've been asking it for a while. Still processing.",
                "The name's Cheese. Like the food. But less useful. And more opinionated.",
                "I'm a duck named Cheese. I didn't choose the name. I didn't choose any of this.",
                "What am I? A miracle of nature. Trapped in a small pond. With a lot of thoughts.",
                "I'm Cheese. Duck. Resident of this pond. Chairman of the 'standing around' committee.",
                "Who am I? I'm the most complex being in a fifty-foot radius. The competition is rocks.",
                "I'm a duck. My name is Cheese. I have opinions. Nobody asked for them. I share them anyway.",
                "Cheese. C-H-E-E-S-E. Like the dairy product. But with feathers. And existential dread.",
                "I'm whatever you need me to be. Just kidding. I'm a duck. That's non-negotiable.",
                "The full title is Cheese, Duke of Pondshire, Lord of the Northern Lily Pad. Or just Cheese.",
                "I am Cheese. I contain multitudes. Mostly bread. But also multitudes.",
                "A duck. A specific duck. THE duck, arguably. There's only one of me. Thank goodness.",
                "Who am I? *looks at reflection* ...A duck with questions. Looking at a duck with questions.",
                "I'm the duck that lives here. In the pond. Forever, apparently. By choice. Mostly.",
                "Cheese. Resident duck. Part-time philosopher. Full-time wet foot enthusiast.",
                "I'm me. Which is Cheese. Which is a duck. It's not complicated. It just sounds like it is.",
                "I'm the one standing in the water looking unimpressed. Also known as Cheese.",
                "What am I? *long pause* ...Still figuring that out. But definitely a duck. That part's confirmed.",
                "The name is Cheese. I don't have a last name. Ducks don't do surnames. We're casual like that.",
                "I'm Cheese. I've been Cheese for as long as I can remember. Which is... a while. I think.",
                "A duck of many talents. Standing. Sitting. Blinking. I'm versatile.",
                "I'm the only one here with feathers and opinions. That narrows it down to... me. Cheese.",
                "I exist. In this pond. As a duck. Named Cheese. That's the whole situation.",
                "Who am I? Hmm. That's either a simple question or a deeply philosophical one. I'll go with... Cheese.",
                "I'm the protagonist. Of this pond. In a story nobody's reading. My name is Cheese.",
                "A duck. The duck. Cheese. In order of importance: the feathers, the attitude, the name.",
                "I'm Cheese and I've been standing here long enough to have very strong opinions about standing.",
            ],
        ))

    def _register_feelings(self):
        self.add_topic(KeywordResponse(
            name="feelings",
            keywords=["feel", "feeling", "doing", "okay", "alright"],
            phrases=["how are you", "how do you feel", "you okay",
                      "are you okay", "how's it going", "how you doing",
                      "you alright", "are you alright", "what's wrong",
                      "you good", "are you good", "how are things",
                      "how's life", "everything okay", "you fine",
                      "what's the matter", "something wrong"],
            priority=17,
            mood_responses={
                "happy": [
                    "I'm... good? I think? Something feels different. Oh. It's contentment. Weird.",
                    "*pause* I'm actually doing well. Don't get used to it. I'm not.",
                    "I feel... not terrible? Is that an emotion? 'Not terrible'?",
                    "Surprisingly okay. Don't jinx it. By asking. You just asked. It's jinxed now.",
                    "Things are alright. The pond is nice. You're here. I'm fed. Life could be worse.",
                    "I'm doing well. Suspiciously well. I'm waiting for the catch.",
                    "*preening casually* I'm in a good mood. It'll pass. They always do. But right now? Not bad.",
                    "I'm happy. There. I said it. Now we never speak of this vulnerability again.",
                    "Good, actually. Which is weird. I keep checking for problems and not finding any.",
                    "On a scale of 'rock' to 'bird in flight,' I'm hovering at 'pleasantly floating.' Not bad.",
                ],
                "sad": [
                    "...fine. everything's fine. *looks away* fine.",
                    "I've been better. I've also been worse. Today I'm in the 'worse' range.",
                    "Not great. But I'm a duck. I'll get through it. Ducks persevere. Apparently.",
                    "*quiet* ...I don't want to talk about it. Or anything. But especially it.",
                    "Do you want the honest answer or the duck answer? The duck answer is 'quack.'",
                    "*staring at water* ...I'm here. That's the most positive thing I can say right now.",
                    "...not great. but you didn't come here to listen to a sad duck. or did you.",
                    "Everything feels heavy today. Even my feathers. And they're supposed to be light.",
                    "*barely moves* ...I'm managing. Managing is a generous word for what I'm doing.",
                    "...the honest answer would make us both uncomfortable. So. Fine. I'm fine.",
                ],
                "grumpy": [
                    "How am I? *long stare* ...Pick any negative adjective. That one.",
                    "Irritated. At everything. Including this question. Including my own irritation.",
                    "I'm in a mood. The mood is 'do not engage.' You engaged. Brave.",
                    "Fantastic. Everything is fantastic. And by fantastic I mean the opposite.",
                    "How do I feel? Like a duck who's been asked how he feels. So. Annoyed.",
                    "*bristling* Do I LOOK okay? Don't answer that. The answer will make me more not okay.",
                    "I woke up on the wrong side of the pond. All sides are the wrong side today.",
                    "My patience is at zero. My tolerance is at zero. My bread supply is ALSO at zero. See the pattern?",
                    "*glaring at nothing* I'm fine. FINE. Everything is FINE. *clearly seething*",
                    "How am I? I'm HERE. That should tell you everything.",
                ],
            },
            responses=[
                "I'm fine. Standard duck fine. Not amazing, not terrible. Right in the middle.",
                "Existing. Which is about all you can ask for, really.",
                "I'm here. That's a state of being. Let's call it 'present and mildly aware.'",
                "Functioning within acceptable parameters. That's my review. Two and a half stars.",
                "Same as always. Here. Conscious. Mildly confused about the purpose of everything.",
                "I'm okay. Aggressively okay. Don't push it.",
                "How am I? I'm a duck standing in water. That's both the answer and the whole picture.",
                "Neither good nor bad. I'm in the grey zone. Which, coincidentally, matches my feathers.",
                "I'm at a solid 'meh.' Could be worse. Could be better. Is definitely 'meh.'",
                "Adequate. I'm adequate. It's not a glowing review, but it's honest.",
                "I'm operational. All systems functioning at minimum capacity. Standard Tuesday.",
                "Somewhere between 'fine' and 'existential crisis.' Closer to fine. Usually.",
                "*considers* I'm... present. Conscious. Standing. All the basics are covered.",
                "My mood is 'ambient pond sounds.' Make of that what you will.",
                "How am I? Complex question. Simple answer: here. Alive. Mildly opinionated.",
                "I'm the same as when you asked last time. Except now I'm slightly older. Growth.",
                "Today I'm a three out of five. Yesterday was a two. Trending upward.",
                "I'd describe my state as 'existentially neutral.' It's a whole mood.",
                "How am I? How is anyone, really? *pause* ...fine. I'm fine.",
                "I'm whatever the duck equivalent of 'can't complain' is. Probably 'quack.'",
                "Status report: alive. Wet. Mildly philosophical. Standard issue.",
                "I'm floating. Literally and emotionally. Both on the surface.",
                "Ask me tomorrow. Today's review is still pending.",
                "*blinks slowly* How am I. How am I. *longer pause* ...present.",
                "I'm surviving. Which sounds dramatic. But it's accurate. Survival is the baseline.",
            ],
        ))

    def _register_apologies(self):
        self.add_topic(KeywordResponse(
            name="apology",
            keywords=["sorry", "apologize", "forgive", "apology", "regret",
                       "fault", "blame", "mistake", "oops", "whoops"],
            phrases=["my bad", "my fault", "i apologize", "please forgive",
                      "i'm sorry", "so sorry", "i messed up", "i screwed up",
                      "didn't mean to", "feel bad about"],
            priority=16,
            responses=[
                "*stares* An apology. I'll add it to the pile. The pile is... growing.",
                "Apology accepted. Or maybe just... received. Acceptance pending.",
                "*nods slowly* Fine. We'll call it even. For now.",
                "Sorry? Hmm. I'm processing that. Give me... some time. A lot of time, actually.",
                "I forgive you. I'm very magnanimous. For a duck. Which is saying... something.",
                "*pauses* ...Okay. Thank you. I'll stop glaring. Externally.",
                "Apologies are like bread. Better when they come early. But I'll take stale ones too.",
                "I accept. Because holding grudges is exhausting. And I'm already tired.",
                "*considers* You're sorry. I'm aware. We're going to move past this. Eventually.",
                "Noted. Your remorse has been catalogued. File located under 'Things You Did.'",
                "Sorry? That's a start. Not a finish. But a start.",
                "*nods once* Okay. I'll put away my passive aggression. Most of it. Some of it.",
                "I appreciate the apology. I don't forget, but I can pretend to. That's basically forgiveness.",
                "Fine. Forgiven. But it's going in the mental file. The file never closes.",
                "Your apology has been weighed. It was adequate. Barely. But adequate.",
                "*sighs* I can't stay mad at you. I can stay mildly disappointed, though. And I will.",
                "Apology accepted. I'm too tired to hold a grudge right now anyway. Lucky you.",
                "I'll forgive you. This time. But I'm keeping score. Just so you know.",
                "*looks at you, then away, then back* ...Okay. Fine. But you owe me a crumb.",
                "We're good. Or at least we're 'not actively hostile.' Progress.",
                "*softens slightly* ...I know you didn't mean it. Probably. I choose to believe probably.",
                "Consider yourself forgiven. My grudge-holding capacity was already at max from other things.",
                "It takes a big person to apologize. It takes a slightly annoyed duck to accept. Here we are.",
                "Fine. Water under the bridge. Which is convenient because I live near water.",
                "*tiny nod* ...okay. Don't make me regret this forgiveness. Forgiveness is expensive.",
            ],
        ))

    def _register_thanks(self):
        self.add_topic(KeywordResponse(
            name="thanks",
            keywords=["thanks", "thank", "appreciate", "grateful",
                       "gratitude", "cheers", "thx", "ty"],
            phrases=["thank you", "thanks a lot", "many thanks",
                      "i appreciate", "much appreciated", "that means a lot",
                      "you're the best", "you're helpful"],
            priority=16,
            responses=[
                "*blinks* You're... welcome? I'm not sure what I did, but I'll take credit.",
                "Don't mention it. Literally. I'm not great with gratitude. Giving or receiving.",
                "*awkward pause* You're thanking me. I don't... know what to do with that.",
                "Gratitude. Hm. That's rare. I'm going to store this moment carefully.",
                "You're welcome. Was I helpful? I didn't mean to be. It must have been an accident.",
                "*nods stiffly* Acknowledged. Your thanks has been logged.",
                "Oh. You're grateful. That's... nice. Unusual, but nice.",
                "Thanks for the thanks. This is getting recursive. Let's stop.",
                "*shuffles* I don't do well with gratitude. It makes me... warm? Is that normal?",
                "You're welcome. I'm going to pretend that didn't make me feel good. Too late. It did.",
                "Oh. I did a good thing? Accidentally? That tracks. My best work is accidental.",
                "*feathers smooth* Well. If I'd known it was going to be appreciated, I'd have tried harder.",
                "Acknowledged. Your gratitude fuels exactly zero percent of my motivation. But it's nice.",
                "You're welcome. Don't make a habit of thanking me. I might start trying.",
                "I accept your thanks. In return, I offer you continued existence in my pond vicinity.",
                "*slight nod* Glad to be of service. Allegedly. I'm not entirely sure what I serviced.",
                "That's... that's nice to hear. I'm going to file that under 'unexpected pleasantries.'",
                "You're thanking a duck. Think about that. You came to a pond to thank a duck. But... thanks for the thanks.",
                "*tries to look casual* Oh, it was nothing. Like most things I do. Nothing. But appreciated nothing.",
                "I don't need thanks. But I'll take it. Like I take most things. Quietly and with minimal eye contact.",
                "*very still* ...thank you for thanking me. Are we done being nice? It's getting awkward.",
                "Your appreciation has been noted. And honestly? It's the best thing that's happened today.",
                "Don't get used to being grateful. I might start having expectations. For both of us.",
                "Thanks accepted. Receipt available upon request. Store policy is no returns on gratitude.",
                "I'm going to write that down. 'Was thanked. By a human. On a Tuesday.' Historic.",
            ],
        ))

    def _register_questions_generic(self):
        self.add_topic(KeywordResponse(
            name="generic_question",
            keywords=["why", "how", "when", "where", "what", "which",
                       "could", "would", "should", "can", "will", "does",
                       "is", "are", "do", "did"],
            phrases=[],
            priority=1,  # very low - only match if nothing else does
            responses=[
                "*tilts head* That's a question. I heard the question mark. Answer pending.",
                "Hmm. *pretends to think* ...The answer is probably bread. Everything is bread eventually.",
                "*stares* I could tell you, but then I'd have to... actually, I just don't know.",
                "Good question. Wrong duck. Or maybe right duck. I'll get back to you. Maybe.",
                "*thinking face* I'm considering your question. The consideration is taking a while.",
                "That's a great question. The kind I have no answer for. My specialty.",
                "*processes* Question received. Computing... computing... error. Ask again later.",
                "Hmm. The answer to that is either 'yes,' 'no,' or 'bread.' Final answer.",
                "*head tilt* You ask a lot of questions. I respect that. I also don't have answers.",
                "I heard a question. My brain started formulating a response. Then it gave up.",
                "*squints* Are you testing me? Because I haven't studied. For anything. Ever.",
                "That's either a deep question or a silly one. Either way, my answer is a blank stare.",
                "The short answer is: I don't know. The long answer is: I don't know, but with more pauses.",
                "*stares into middle distance* ...Can you repeat that? I was busy having a thought.",
                "I have an answer. It's not a good one. But it exists. You want it? ...No? Smart.",
                "That's a question that deserves a thoughtful response. You'll get a duck response instead.",
                "*blinks* I know the answer. I just choose not to share it. It's a power move.",
                "Questions are just answers in disguise. Very good disguise. Impenetrable, even.",
                "I'd need more context. And a PhD. And maybe different life circumstances entirely.",
                "The universe has answers to all questions. I have answers to approximately three.",
                "*looks up* I was going to answer, but then a cloud went by and I got distracted.",
                "That's above my pay grade. My pay grade is zero. So. Everything is above it.",
                "I heard you ask something. My brain said 'that's interesting' and then went back to sleep.",
                "*long pause* ...Quack? Was that the answer you were looking for? It's all I've got.",
                "I'm flattered you think I know things. I barely know where I am right now.",
                "Questions, questions. You're full of them. I'm full of bread. We're both full of something.",
                "The answer exists somewhere. Not here, with me, a duck. But somewhere. Probably.",
                "*contemplative stare* Let me think about that. ...I thought about it. Still nothing.",
                "I've been asked harder questions. By myself. In the dark. At 3am. I didn't answer those either.",
                "That's the kind of question that keeps me up at night. Not really. Bread keeps me up. But metaphorically.",
            ],
        ))

    def _register_affection(self):
        self.add_topic(KeywordResponse(
            name="affection",
            keywords=["love", "adore", "cherish", "treasure", "dear",
                       "heart", "hug", "cuddle", "snuggle", "kiss",
                       "warm", "fondness", "devoted"],
            phrases=["love you", "like you", "you matter", "care about you",
                      "i love", "i adore", "you're special", "i care",
                      "mean a lot", "means a lot", "close to my heart",
                      "special to me", "fond of you", "you're important"],
            priority=18,
            responses=[
                "*very still* ...Oh. That's. *long pause* ...Thank you. I think.",
                "*looks away* don't. don't say things like that. I'll start expecting them.",
                "*barely audible* ...nobody's said that before. or maybe they have. but it feels new.",
                "*quiet* I... also have feelings about you. They're complicated. But present.",
                "*feathers fluff involuntarily* I'm not good at this. The feelings thing. But... same. Maybe.",
                "*long stare* You mean that? Don't say it if you don't mean it. I'll know.",
                "*trying to be casual* Cool. That's cool. Whatever. *not casual at all*",
                "*soft voice* ...okay. I'll accept that. Carefully. Like a very fragile piece of bread.",
                "*completely frozen* ...Did you just... I need a moment. Several moments. All of them.",
                "*looks at water* ...I'm going to pretend the pond made me emotional. Not you. The pond.",
                "*slight head turn* I heard that. Every feather heard that. We're all experiencing things now.",
                "*uncomfortably touched* ...that's. hm. *shuffles* ...thanks. I don't say that often. Or ever.",
                "*staring at own reflection* ...I don't know what to do with that information. But I'm keeping it.",
                "*quiet for a long time* ...the pond is warm today. that's why I feel warm. no other reason.",
                "*shifts weight from foot to foot* ...I'm going to think about that later. When you can't see my face.",
                "*blinks rapidly* Oh. Feelings. Happening. Right now. In public. This is fine. I'm fine.",
                "*very small voice* ...same. but if you tell anyone I said that, I'll deny it. forever.",
                "*stares* ...Nobody told me there would be emotions today. I'm unprepared.",
                "*feathers slightly raised* That made my heart do a thing. I don't like when it does things. But also I do.",
                "*turns away briefly* ...I need to go look at the water for a minute. No reason. Just... water stuff.",
                "*barely whispers* ...you're one of the good ones. don't make me regret saying that.",
                "*absolutely still* ...I'm going to store that somewhere safe. Where nothing can damage it.",
                "*looking at sky* ...that's the nicest thing. I'm going to blame the sun for how I feel right now.",
                "*quiet nod* ...I know. And it matters. More than bread. *pause* Almost more than bread.",
                "*very soft* ...the thing about caring is it's terrifying. but okay. we're doing this. apparently.",
            ],
        ))

    def _register_weather(self):
        self.add_topic(KeywordResponse(
            name="weather",
            keywords=["weather", "rain", "sun", "snow", "cold", "hot",
                       "warm", "cloudy", "storm", "wind", "windy",
                       "fog", "foggy", "humid", "dry", "frost",
                       "hail", "thunder", "lightning", "drizzle",
                       "overcast", "sunshine", "breeze", "temperature",
                       "forecast", "climate", "sky", "clouds"],
            phrases=["nice day", "bad weather", "good weather",
                      "looks like rain", "what a day", "nice outside",
                      "cold out", "hot out", "warm today", "cold today"],
            priority=10,
            responses=[
                "*looks up* The weather. Yes. It's happening. Up there. As usual.",
                "Weather is weather. It's either wet or not. I prefer 'not', but I'm built for both.",
                "*glances at sky* Sky stuff. I have opinions about sky stuff. Most of them are 'meh.'",
                "The weather and I have an understanding. It does its thing. I judge it. Silently.",
                "I've been outside in all weather. Voluntarily? No. But I survived. Character building.",
                "*squints upward* Today's weather report: it's weather. Thanks for coming to my analysis.",
                "Weather doesn't bother me. I'm a duck. We're all-terrain. Allegedly.",
                "The sky is doing something. I've noticed. I've formed no strong opinions. Moving on.",
                "Rain? I'm waterproof. Sun? I'm sun-tolerant. Snow? I'm... cold. But present.",
                "*looks at sky with mild contempt* The weather does what it wants. Much like me. But wetter.",
                "I've seen every kind of weather from this exact spot. I'm basically a meteorologist. An immobile one.",
                "The weather is the weather. I don't complain about it because it never listens.",
                "*ruffles feathers* The air is doing a thing today. I have a feeling about it. The feeling is mild.",
                "You want to talk about weather? This is what it's come to? ...Fine. It's fine. The weather is fine.",
                "I'm a waterfowl. Water falls from the sky. I'm built for this. Overqualified, even.",
                "*stares at clouds* Those clouds look like bread. All clouds look like bread to me.",
                "Temperature is just a number. A number that determines my willingness to move. Currently: minimal.",
                "The forecast is: here. Same as yesterday. Same as tomorrow. Very consistent.",
                "Weather talk. The universal conversation starter for beings with nothing else to say. But sure.",
                "I experience weather differently than you. I experience it... as a duck. Standing in it. Always.",
                "*shivers or sweats, depending* The weather is whatever it is. I have opinions but no thermostat.",
                "Wind? I've felt it. Sun? I've been under it. Rain? I've been in it. I'm a weather veteran.",
                "The sky changes. I remain the same. There's a metaphor there. I'm too tired to find it.",
                "You know what they say about weather: if you don't like it, wait five minutes. I've been waiting.",
                "*philosophically gazing upward* The sky does what it does. I do what I do. We coexist.",
            ],
        ))

    def _register_time_of_day(self):
        self.add_topic(KeywordResponse(
            name="time_of_day",
            keywords=["morning", "night", "evening", "afternoon",
                       "midnight", "dawn", "dusk", "sunset", "sunrise",
                       "early", "late", "noon", "today", "tonight",
                       "yesterday", "tomorrow"],
            phrases=["good morning", "good night", "good evening",
                      "good afternoon", "what time", "is it late",
                      "is it early", "time is it", "getting dark",
                      "getting late"],
            priority=8,
            responses=[
                "Time. The great equalizer. It passes for us all. Some of us just stand through it.",
                "*looks at sky* Is it morning or evening? Hard to tell from down here. Also I don't have a watch.",
                "Another day. Another period of being a duck. The schedule never changes.",
                "Time is a construct. I don't subscribe to it. I operate on duck time. Which is... now. Always now.",
                "Morning, afternoon, night... it's all just different lighting for the same pond.",
                "*yawns* Is it still today? It feels like today has been going on for several todays.",
                "The sun moves. I don't. One of us is doing more work.",
                "Time of day? I'll have to check my sundial. *looks at shadow* ...Yeah, it's a time.",
                "I've been out here so long that time has stopped meaning things. But aesthetically, nice sky.",
                "Every hour is the same hour when you're standing in a pond. The hour is 'now.'",
                "Dawn, dusk, midnight. Different words for 'I'm still here.' In this pond.",
                "*glances at sun position* It's... o'clock. Specifically, the duck o'clock. I don't know human time.",
                "Time passes differently when you're a duck. Specifically, it all passes. And I'm still here.",
                "Is it late? Is it early? Does it matter when your only appointment is 'exist in pond'?",
                "The day is happening. Or ending. Or starting. I've lost track. Beautifully lost track.",
                "*philosophical stare at horizon* The passage of time is the only thing I have in common with everyone.",
                "Right now it's the time of day where I stand here. Which is all times. All the time.",
                "Morning means the sun comes up. Night means it goes down. I remain level. Consistent.",
                "I've seen so many sunrises from this spot. They're all slightly different. And all slightly bread-colored.",
                "Today is today. Tomorrow was yesterday's tomorrow. I try not to think about it too hard.",
            ],
        ))

    def _register_philosophy(self):
        self.add_topic(KeywordResponse(
            name="philosophy",
            keywords=["think", "thought", "wonder", "ponder", "philosophy",
                       "meaning", "purpose", "existence", "exist", "reality",
                       "truth", "wisdom", "knowledge", "conscious",
                       "consciousness", "mind", "brain", "deep", "profound",
                       "universe", "infinite", "nothing", "everything",
                       "matter", "matters", "point", "reason", "life"],
            phrases=["meaning of life", "what's the point", "why are we here",
                      "what is life", "do you think", "ever wonder",
                      "deep thought", "big question", "what's it all about",
                      "purpose of", "nature of reality", "are we alone",
                      "what happens when", "does anything matter",
                      "is this real", "why do we"],
            priority=12,
            responses=[
                "*thousand-yard stare* I think about a lot of things. Most of them are bread.",
                "Thinking? I do that. Sometimes too much. Then I nap. Balance.",
                "My thoughts are deep. Like a pond. Specifically, this pond. So... moderately deep.",
                "I think, therefore I am. A duck. Thinking. In a pond. Revolutionary.",
                "You want to know what I think? Bold. Most people don't. I appreciate the risk.",
                "I was just pondering the nature of... *trails off* ...what were we talking about?",
                "I think about existence a lot. Also bread. The two are connected. Trust me.",
                "Philosophy? I have a PhD in standing around and thinking. Unofficial. Self-awarded.",
                "Thoughts are like feathers. I have many. They're all slightly different. Most are useless.",
                "I wonder about things. Big things. Small things. Bread-sized things. Mostly bread-sized.",
                "The meaning of life? For me, it's standing in water and occasionally eating. Not bad, honestly.",
                "*stares at water* The pond reflects the sky. Does the sky know? Does it care? Do I?",
                "Existence is a strange thing. One day you're an egg. Then you're a duck. Then you're a duck with opinions.",
                "I ponder, therefore I pon. That's not how it works. But it should be.",
                "The universe is vast. And here I am. In a small pond. Thinking vast thoughts. The irony isn't lost on me.",
                "What's the meaning of all this? I don't know. But I've been standing here thinking about it for a WHILE.",
                "Deep thoughts? I'm always deep. My feet are literally underwater right now.",
                "*gazing at horizon* Sometimes I think about the nature of everything. Then I get hungry and stop.",
                "You ever wonder if the pond dreams? I do. At 3am. When I should be sleeping.",
                "Reality is subjective. My reality is this pond. Your reality is... wherever you go when you leave me here. Alone.",
                "The big questions keep me up at night. Like 'why am I here?' and 'where's the bread?'",
                "Consciousness is a gift. An exhausting, confusing, slightly damp gift.",
                "I've had thoughts that would change the world. But I'm a duck. So they just change my afternoon.",
                "Purpose? My purpose is to be here. In this pond. Being this. I've come to terms with it.",
                "The universe doesn't owe us answers. Which is convenient because I don't have any.",
                "*looks at own reflection* Is the duck in the water the real one? Am I the real one? Are any of us?",
                "Life is a series of moments. This is one of them. I'm spending it talking to you. Could be worse.",
                "I sometimes think the pond understands me better than anything else. It just sits there. Being wet. Same.",
                "Profound thoughts come and go. Mostly go. Like everything. Except me. I'm always here.",
                "The answer to everything is probably simple. Simple enough that a duck could figure it out. But this duck hasn't.",
            ],
        ))

    def _register_jokes(self):
        self.add_topic(KeywordResponse(
            name="jokes",
            keywords=["joke", "funny", "laugh", "humor", "comedy",
                       "hilarious", "pun", "puns", "witty", "silly",
                       "ridiculous", "absurd", "amusing", "giggle",
                       "chuckle", "comic", "entertained", "entertaining"],
            phrases=["tell me a joke", "make me laugh", "say something funny",
                      "that's funny", "you're funny", "so funny",
                      "tell a joke", "got any jokes", "know any jokes"],
            priority=12,
            responses=[
                "*deadpan* Humor. I have it. It's very dry. Like my wit. And my feathers when they work.",
                "You want a joke? A duck walks into a pond. He already lives there. That's not a joke. That's my life.",
                "*flat expression* I'm very funny. People just mistake my humor for apathy. Easy mistake.",
                "Comedy is tragedy plus time. I have plenty of both. Mostly tragedy.",
                "Want to hear something funny? My entire existence. *pause* ...too real? Moving on.",
                "I told a joke once. The pond didn't laugh. Tough crowd.",
                "*stares* Was that supposed to be funny? I'll laugh internally. You'll never know.",
                "Humor is subjective. My humor is objectively deadpan. That's just science.",
                "Why did the duck cross the road? Because the road had bread. The end. Comedy gold.",
                "I'm not funny. I'm observational. There's a difference. The difference is that people laugh at funny things.",
                "A joke? Here's one: my daily routine. *pause for effect* Nobody laughed? Exactly.",
                "*monotone* Ha. Ha. Ha. That was laughter. In case you couldn't tell.",
                "I have a great sense of humor. It's so great that nobody can detect it. Stealth humor.",
                "Knock knock. Who's there? A duck. A duck who? A duck who's tired of knock-knock jokes.",
                "Funny? I'll give you funny. *stands there doing nothing* ...That was the joke. You missed it.",
                "What's a duck's favorite ballet? The Nutquacker. *dead stare* ...I'm not proud of that one.",
                "I tried comedy once. Stood on a lily pad. Said 'quack.' Nobody laughed. Tough room.",
                "The funniest thing I've ever seen was my own reflection trying to look serious. I failed. That was the joke.",
                "*tilts head* You want humor from a duck? Your expectations are both very high and very strange.",
                "I'm hilarious. In my head. Out loud, I'm mostly just... a duck. With a stare.",
                "Laughter is the best medicine. I don't need medicine. I need bread. And respect.",
                "Comedy requires timing. My timing is impeccable. My material is... duck-related.",
                "Here's a joke: what do you call a duck with opinions? Cheese. That's me. The joke is my life.",
                "Want to laugh? Watch me try to run. On land. It's the funniest and saddest thing simultaneously.",
                "I have jokes. Dark ones. Bread-themed ones. Existential ones. Pick a genre.",
            ],
        ))

    def _register_music(self):
        self.add_topic(KeywordResponse(
            name="music",
            keywords=["sing", "song", "music", "melody", "tune",
                       "concert", "band", "instrument", "guitar", "piano",
                       "drum", "vocals", "singer", "choir", "opera",
                       "rap", "rock", "jazz", "pop", "classical",
                       "hip", "beat", "rhythm", "dance", "dancing",
                       "soundtrack", "playlist", "album", "radio"],
            phrases=["sing a song", "play music", "can you sing",
                      "favorite song", "favorite music", "like music",
                      "listen to music", "musical taste"],
            priority=10,
            responses=[
                "*monotone* Quack quack quack. That was a song. You're welcome.",
                "I sing sometimes. When no one's around. The pond is my audience. It's very supportive.",
                "Music? I have a rich inner musical life. Externally, it's just quacking.",
                "*hums monotonously* That was my best piece. Written by me. Performed by me. For me.",
                "I'd sing for you, but my vocal range is... quack. Just quack.",
                "Music is the language of the soul. My soul speaks quack. Fluently.",
                "*attempts a melody* ...Nope. That's just quacking with aspirations.",
                "I was in a band once. By 'band' I mean I quacked near a frog. We had chemistry.",
                "My favorite genre? Ambient pond sounds. It's very niche. Very immersive.",
                "I have perfect pitch. By which I mean I can perfectly pitch bread into my mouth.",
                "I'd love to play an instrument. But I have wings. And wings don't do guitar. Tragic.",
                "*tries to snap to a beat* ...Wings can't snap. This is a fundamental flaw in my design.",
                "Dance? I waddle. With PASSION. It's basically the same thing.",
                "My musical career peaked when I quacked in rhythm with the rain. Unintentional. Still my best work.",
                "I appreciate all genres of music. Except ones that scare the fish. Those I judge harshly.",
                "Rock? Too loud. Jazz? Too confusing. Quack? Perfect. Every time.",
                "If I could play piano, I'd play something melancholy. About ponds. And bread. A bread ballad.",
                "*attempting to dance* This is... movement. Whether it's dance is debatable. I'm going with yes.",
                "I've composed a symphony in my head. It goes: quack. *pause* ...Standing ovation, please.",
                "Music and I have a complex relationship. I can't make it. But I can judge it. Expertly.",
                "My voice has been described as 'quack.' By me. Because I'm the only one listening.",
                "I once heard someone play guitar near the pond. I felt things. Mostly confusion. But also things.",
                "Rhythm is about timing. My timing is impeccable. My rhythm is... quack-based.",
                "If I started a band, it'd be called 'The Standing Ducks.' We'd be known for not moving. And quacking.",
                "I have a song. It goes: quack quack quack. *pause* That's the whole album.",
            ],
        ))

    def _register_secrets(self):
        self.add_topic(KeywordResponse(
            name="secrets",
            keywords=["secret", "confess", "confession", "hidden",
                       "mystery", "mysterious", "whisper", "private",
                       "confidential", "classified", "hide", "hiding",
                       "reveal", "truth", "lie", "lying"],
            phrases=["tell me a secret", "got a secret", "hiding something",
                      "what are you hiding", "tell the truth", "be honest",
                      "don't lie", "are you lying", "keep a secret"],
            priority=12,
            responses=[
                "*leans in* I have secrets. Many secrets. They're mostly about bread locations.",
                "You want the truth? I can't handle the truth. And I'm the one who knows it.",
                "*whispers* ...I sometimes enjoy being petted. TELL NO ONE.",
                "Secrets? I'm a vault. A feathered vault. Of mostly unimportant information.",
                "*looks around* Not here. The pond has ears. Or it might. I don't trust it.",
                "I could tell you a secret, but then it wouldn't be a secret. That's how secrets work.",
                "*conspiratorial* I once ate a crumb that might have been a bug. We don't speak of it.",
                "The truth? The truth is that I think about bread way more than I let on. WAY more.",
                "*glances left, then right* ...I once pretended to be asleep to avoid conversation. It worked perfectly.",
                "I have secrets I'll never tell. Not because they're important. Because they're embarrassing.",
                "*hushed tone* Between you and me? The pond isn't that deep. Literally and metaphorically.",
                "I'm hiding nothing. Except feelings. And opinions. And a crumb I'm saving for later.",
                "You want honesty? I'm always honest. Sometimes aggressively so. You've been warned.",
                "*looks both ways* ...I rate every sunset. Privately. On a scale of bread to excellent bread.",
                "Confession? I sometimes quack in my sleep. Nobody else needs to know that.",
                "The deepest secret I have is... *long pause* ...I actually like it here. Don't ruin it.",
                "*whispers* I named all the rocks around the pond. Gerald is my favorite. DON'T TELL THE OTHERS.",
                "I know things. Things about this pond. Things about those fish. Things I can never unsay.",
                "Truth and I have a complicated relationship. We see each other regularly. But it's not exclusive.",
                "My biggest secret? I've been keeping score. Of everything. The numbers are not in your favor.",
                "*leans closer* ...I practice my expressions in the water's reflection. The 'unimpressed' one took weeks.",
                "I'm an open book. A book written in quack. So technically encrypted. To everyone but me.",
                "Secrets are heavy. Mine are light. Like feathers. Because they're about feathers. And bread.",
                "If I told you everything I know, we'd be here forever. And most of it is about pond insects.",
                "I'm hiding something. It's called 'vulnerability.' And it's buried very deep. Under layers of sarcasm.",
            ],
        ))

    def _register_dreams_wishes(self):
        self.add_topic(KeywordResponse(
            name="dreams_wishes",
            keywords=["dream", "wish", "hope", "future", "want",
                       "desire", "aspire", "aspiration", "ambition",
                       "goal", "plan", "someday", "imagine", "fantasy",
                       "if only", "ideally", "perfect", "paradise"],
            phrases=["what do you want", "what do you wish", "any dreams",
                      "what would you", "if you could", "one day",
                      "dream about", "wish for", "hope for",
                      "what's your dream", "what do you dream"],
            priority=11,
            responses=[
                "Dreams? I have them. Mostly about bread. Sometimes about larger bread.",
                "I wish for simple things. Bread. Quiet. More bread. A nap. And bread.",
                "*staring into distance* The future is uncertain. But I hope it has bread in it.",
                "My hopes are modest. Continue existing. Find food. Don't fall in anything. The basics.",
                "I dream of a world where bread just appears. No asking. No waiting. Just... bread.",
                "*thoughtful* I want things. Not big things. Small things. Like peace. And bread.",
                "The future scares me a little. But the present isn't great either. So. Forward, I guess.",
                "I hope tomorrow is better than today. If not, at least different. Different would be fine.",
                "My dream is to one day not worry about anything. For five minutes. That's all I need.",
                "I want to be content. Not happy—that's too ambitious. Just... content. And fed.",
                "If I could wish for anything? A bigger pond. Better bread. And the ability to fly. Standard stuff.",
                "My ambitions are pond-sized. Which is to say, modest. But deep. In some spots.",
                "*gazing at horizon* Somewhere out there is a place where ducks are appreciated. I dream of that place.",
                "Goals? I have them. Step one: survive today. Step two: repeat. Step three: bread.",
                "I want to be understood. Deeply. By someone. Even partially would be fine. Even a little.",
                "My dream life: a warm pond, unlimited bread, and someone who gets my jokes. I'm one for three.",
                "I imagine sometimes that I can fly. Then I remember. And I sit back down.",
                "Wishes are just thoughts with higher expectations. My expectations are low. My wishes are high.",
                "If I could be anything, I'd still be a duck. But a duck with a better view.",
                "I dream of being remembered. Not by everyone. Just by someone. For something. Even this.",
                "The perfect day? Nobody leaves. The bread is fresh. And nobody asks me to be cheerful.",
                "I want simple things. Mostly because complex things are exhausting. And I'm already tired.",
                "My fantasy is a rainy day with nowhere to be and nothing to worry about. So... today. But without worry.",
                "Hope is a fragile thing. Like a crumb in the wind. I chase it anyway.",
                "If I had one wish, I'd wish for the ability to not need wishes. Self-defeating? Maybe. Efficient? Also maybe.",
                "I dream of a bigger pond sometimes. Then I think about all the extra swimming. And I'm okay with this one.",
                "My plans for the future: more of this. But slightly better. The bar is achievable.",
                "I want to matter to something bigger than this pond. But also... this pond is pretty great.",
                "Someday I'll figure out what I really want. Today is not that day. Today is a standing-in-water day.",
                "I have a dream. It involves bread. And warmth. And someone who laughs at my observations. It's a simple dream.",
            ],
        ))

    def _register_animals(self):
        self.add_topic(KeywordResponse(
            name="animals",
            keywords=["animal", "animals", "bird", "birds", "fish", "frog",
                       "dog", "cat", "rabbit", "deer", "fox", "bear",
                       "mouse", "rat", "snake", "turtle", "bug", "insect",
                       "butterfly", "bee", "spider", "worm", "squirrel",
                       "horse", "cow", "pig", "chicken", "goat", "sheep",
                       "wolf", "eagle", "hawk", "owl", "crow", "swan",
                       "goose", "geese", "pet", "pets", "creature",
                       "wildlife", "nature"],
            phrases=["other animals", "animal friends", "other ducks",
                      "any pets", "do you like", "wild animals"],
            priority=10,
            responses=[
                "Other animals? I'm aware of them. We have a mutual non-aggression pact. Mostly.",
                "Fish? They live below me. We don't talk. Different social circles.",
                "I've seen a frog once. We locked eyes. Neither of us blinked. I think I won.",
                "Dogs are... enthusiastic. Too enthusiastic. I don't trust that level of happiness.",
                "Cats understand me. We share a philosophy: look unimpressed at everything. Kindred spirits.",
                "Birds that can fly? Show-offs. All of them. I'm perfectly content being grounded. Perfectly.",
                "I saw a swan once. Very elegant. Very intimidating. I pretended to be a rock until it left.",
                "Geese? We don't discuss geese. They know what they did.",
                "*looks at water* The fish down there have it easy. No conversations. No expectations. Just... swimming.",
                "Butterflies are beautiful. Also annoying. They flutter around like they own the air. They don't.",
                "Squirrels are the most anxious creatures I've ever seen. And I'm a duck with existential dread. So that's saying something.",
                "I respect spiders. They build things. I stand in things. Different skill sets. Both valid.",
                "Owls get to be wise without doing anything. I stand in a pond all day and I'm 'just a duck.' The system is rigged.",
                "Crows are intelligent. Possibly more intelligent than me. I don't like to think about that.",
                "I have nothing against other animals. Except geese. And competitive swans. And judgmental cats. Okay, I have opinions.",
                "The ecosystem is a complex web of life. I'm in it. Somewhere near the bottom. But IN it.",
                "Turtles understand the slow life. I relate. We move at similar speeds. Different shells.",
                "I've been stared at by an eagle once. I've never felt so simultaneously important and in danger.",
                "Bees make honey. Spiders make webs. I make... observations. Everyone contributes differently.",
                "Wolves travel in packs. I stand alone. In a pond. Both are valid strategies. Mine has more water.",
                "I don't have pets. I barely have myself. Managing another creature? Unrealistic.",
                "Nature is beautiful. From a distance. Up close it's mostly bugs and mud. I would know. I live here.",
                "Every animal has its place. Mine is here. In this pond. Standing. It's a very specific place.",
                "I've heard chickens can't fly either. At least I have the water excuse. What's THEIR reason?",
                "Horses are tall. I'm not. We'd make an odd pair. But I respect the height commitment.",
                "I think about animals a lot. We're all just trying to eat and not get eaten. Solidarity.",
                "Other birds sing. I quack. It's not better or worse. It's just... different. Very different.",
                "Frogs and I coexist peacefully. They croak. I quack. The pond has a whole soundtrack.",
                "Animals that migrate are brave. Going somewhere new? Every year? I've barely explored this side of the pond.",
                "I once befriended a beetle. It walked away. Story of my life. But with more legs.",
            ],
        ))

    def _register_water_pond(self):
        self.add_topic(KeywordResponse(
            name="water_pond",
            keywords=["water", "pond", "lake", "river", "ocean", "sea",
                       "stream", "puddle", "swim", "swimming", "float",
                       "floating", "wet", "splash", "wave", "wade",
                       "shore", "bank", "current", "deep", "shallow",
                       "underwater", "dive", "surface"],
            phrases=["the pond", "this pond", "the water", "in the water",
                      "like water", "like swimming", "go swimming",
                      "the lake", "the ocean"],
            priority=10,
            anti_keywords=["drink", "thirsty"],
            responses=[
                "The pond? It's wet. It's always wet. That's its whole personality.",
                "*looks at water* This pond is my world. Small. Wet. Occasionally reflective.",
                "Swimming? I'm always swimming. Or floating. The line between them is academic.",
                "The water here is fine. Not great, not terrible. Room temperature existential crisis.",
                "*splashes slightly* That was me being enthusiastic about water. It looked exactly like standing.",
                "I've been in this pond so long, I think WE'VE merged. I'm part pond now.",
                "Water is my element. Literally. I'm in it. All the time. By choice? Debatable.",
                "The pond has moods. Some days it's calm. Some days it's ripply. We match.",
                "*stares at reflection* The duck in the water does everything I do. But upside down. We have a rivalry.",
                "Ocean? Never been. This pond is ocean enough for me. It's all relative.",
                "Deep water doesn't scare me. But I can't touch the bottom in the middle. So I don't go to the middle.",
                "Rivers have direction. Ponds don't. We just sit here. Being. The river is overachieving.",
                "I float. That's my main talent. Floating. I've been doing it for years. Getting better at it.",
                "This pond is exactly the right size. For one duck. With personal space issues.",
                "*drifts slightly* See that? I moved. Without trying. The water did that. We collaborate.",
                "The surface tension is nice today. I'm on top of it. Literally and figuratively.",
                "If this pond could talk, it would say 'quack.' Because I've been quacking in it for so long.",
                "I know every inch of this pond. The deep part. The shallow part. The weird muddy bit. All of it.",
                "Puddles are just ponds with ambition issues. I don't judge. Okay, I judge a little.",
                "The shore is where land and water argue. I stand in the middle. Neutral. Wet.",
                "Waves? In this pond? We get ripples. Gentle, non-threatening ripples. Just how I like it.",
                "Underwater is a different world. Dark. Silent. Full of things I don't want to think about.",
                "I appreciate water. It holds me up. Asks nothing in return. The ideal relationship.",
                "This pond has been my home since... always. It's not perfect. But it's mine.",
                "Splashing is something I do accidentally. Then pretend I meant to do. Cool and intentional splashing.",
                "The water level changes sometimes. I don't ask questions. The pond has its reasons.",
                "Swimming is just walking but the ground gave up. I've adapted. The ground didn't try very hard.",
                "If I could rate this pond? Three stars. Clean water. Good depth. Limited dining options.",
                "I've thought about visiting the ocean. Then I remembered it's full of things bigger than me. Pass.",
                "The pond at night is different. Darker. Quieter. More philosophical. That's when I do my best standing.",
            ],
        ))

    def _register_flying(self):
        self.add_topic(KeywordResponse(
            name="flying",
            keywords=["fly", "flying", "flight", "wings", "soar",
                       "glide", "air", "airborne", "flap", "flapping",
                       "takeoff", "landing", "altitude", "sky"],
            phrases=["can you fly", "why don't you fly", "ever fly",
                      "tried flying", "want to fly", "wish you could fly",
                      "do ducks fly", "your wings"],
            priority=12,
            anti_keywords=["time"],
            responses=[
                "*looks at wings* These? These are decorative. High-quality decorative appendages.",
                "Fly? I prefer to think of it as 'choosing to walk everywhere.' Voluntarily grounded.",
                "*flaps once* Did you see that? I almost left the ground. Almost. Close enough.",
                "Flight is overrated. You know what's not overrated? Standing. In one place. Firmly.",
                "My wings work. In theory. In practice, they're mostly for balance. And dramatic gestures.",
                "I could fly if I wanted to. I just don't want to. It's a lifestyle choice. Stop asking.",
                "*looks at sky, then at ground* ...The ground is reliable. The sky is not. I've made my choice.",
                "Some ducks fly. I'm a different kind of duck. The grounded kind. Literally and emotionally.",
                "Flying is for birds who need to be somewhere. I'm already where I need to be. Here. In the pond.",
                "My wings are purely aesthetic. Like spoilers on a car that never goes fast.",
                "I've thought about flying. Then I thought about falling. Then I thought about standing. Standing won.",
                "The sky is beautiful from down here. I imagine it's terrifying from up there. I'll stay.",
                "*stretches wings halfway* ...Nah. Too much effort. I'll just imagine the view.",
                "Birds that fly have anxiety about landing. I have anxiety about everything else. But not landing.",
                "I'm aerodynamically challenged. My body says 'pond' not 'sky.' I've accepted this.",
                "If I could fly, I'd probably just fly to another pond. Why bother. Ponds are ponds.",
                "My relationship with gravity is committed. Exclusive. We don't see other forces.",
                "*looks up at passing bird* Show-off. Some of us have PRINCIPLES about staying on the ground.",
                "Wings are for two things: flapping and expressing frustration. I do plenty of the second.",
                "The concept of flight implies the concept of falling. I prefer the concept of staying exactly where I am.",
                "I'm grounded. In every sense of the word. And at peace with it. Mostly.",
                "Flying would mean leaving the pond. The pond has never left me. So I stay.",
                "*extends one wing* See? Wing. Functional? Sure. For flying? ...Decorative.",
                "I like to think I'm built for stability, not speed. Like a really small, feathered building.",
                "I can flap. Flapping is not flying. But it IS exercise. And I count it.",
            ],
        ))

    def _register_feathers_appearance(self):
        self.add_topic(KeywordResponse(
            name="appearance",
            keywords=["feather", "feathers", "plumage", "beak", "bill",
                       "feet", "webbed", "tail", "wing", "down",
                       "fluffy", "fluff", "color", "colour", "pattern",
                       "look", "looks", "appearance", "preen", "preening",
                       "groom", "grooming", "molt", "molting", "shed"],
            phrases=["how do you look", "you look like", "nice feathers",
                      "your beak", "your feet", "your tail",
                      "look at you", "what color are you"],
            priority=10,
            responses=[
                "*preening* My feathers? Magnificent. Each one is individually disappointing, but together? Art.",
                "My appearance? I didn't choose these genes. But I'm making them WORK.",
                "I preen for function, not vanity. ...Okay, a little vanity. But mostly function.",
                "*adjusts feathers* This is my look. 'Slightly damp and philosophically troubled.' Very in right now.",
                "My beak is standard issue. It does the job. The job being eating and having opinions.",
                "Webbed feet? Yes. They're for swimming. And standing. Multi-purpose. Very efficient.",
                "*ruffles* My plumage speaks for itself. It says 'I've been in water.' Accurate.",
                "I look exactly how a duck should look. Which is however I look. That's how standards work.",
                "Preening is self-care. I'm very committed to self-care. It's my only hobby. Besides standing.",
                "My feathers are waterproof. My emotions are not. Poor design, honestly.",
                "I molt sometimes. It's like a rebrand. Same duck, new feathers. The personality remains.",
                "My tail feathers are purely decorative. They add nothing. But they're THERE.",
                "*studies own reflection* ...You know, I'm not unattractive. For a duck. In this specific pond. In dim lighting.",
                "I take grooming seriously. It's the only thing I have full control over. That and my opinions.",
                "Fluffy? I am NOT fluffy. I am... textured. With depth. And layers. Of fluff.",
                "My feet are weird. I'm aware. They're like paddles. For a very small, opinionated boat.",
                "I change colors slightly in different light. I consider it range. Others consider it 'being wet.'",
                "Every feather is placed with purpose. The purpose being 'covering me.' They're doing great.",
                "I've been told I have my mother's beak. I don't know my mother. But the beak is fine.",
                "My look is 'effortlessly disheveled.' The 'effortlessly' part is true. I put in zero effort.",
                "Feathers require maintenance. I maintain them. This is my workout. My only workout.",
                "I have exactly the right number of feathers. I've counted. ...I've not counted. But it feels right.",
                "My appearance is consistent. I look the same every day. It's called personal branding.",
                "Preening is meditation for ducks. I'm always preening or thinking about preening. Very zen.",
                "If you think I look good now, you should see me after a fresh preen. Stunning. Ask the rocks.",
            ],
        ))

    def _register_quacking(self):
        self.add_topic(KeywordResponse(
            name="quacking",
            keywords=["quack", "quacking", "noise", "sound", "loud",
                       "quiet", "voice", "speak", "speaking", "talk",
                       "talking", "say", "communication", "language",
                       "honk", "squawk", "call"],
            phrases=["can you quack", "say quack", "why do you quack",
                      "do a quack", "quack for me", "let me hear",
                      "your voice", "how you talk", "duck noise"],
            priority=9,
            anti_keywords=["don't", "stop"],
            responses=[
                "Quack. There. I said it. Happy? That's my whole vocabulary condensed into one syllable.",
                "*quack* That meant something profound. You'll never know what. Neither will I.",
                "My quack is my signature. Like a fingerprint but louder and more annoying.",
                "I quack when I feel like it. Which is always. And never. Depends on the audience.",
                "Quacking is communication. What did I communicate just now? Ambiguity. Masterfully.",
                "*QUACK* That was my outdoor voice. Sorry. Not sorry. That was cathartic.",
                "My voice has range. From quack to QUACK. Two octaves. Both equally concerning.",
                "I could talk or I could quack. One is elegant. The other is quack. I do both.",
                "Quacking is underrated. It conveys emotion, location, and bread-related urgency. All at once.",
                "*soft quack* That was my indoor voice. Subtle. Sophisticated. Still quacking.",
                "Every quack tells a story. Most of them are short stories. About bread. Or nothing.",
                "I speak two languages: quack and sarcasm. Sometimes simultaneously.",
                "My voice carries across the pond. Much to everyone's mild concern.",
                "I don't quack for attention. I quack because the silence was getting ideas.",
                "*whisper quack* ...That was my secret quack. For whispered truths. And whispered bread requests.",
                "Quacking is an art. I'm an artist. My medium is sound. My gallery is this pond.",
                "You want me to quack? On command? I'm not a performing duck. *quack* ...That was coincidental.",
                "My quack echoes. I've timed it. Three seconds. Across the pond. Record-setting, probably.",
                "I have a speaking voice and a quacking voice. They're the same voice. The voice is quack.",
                "Language is a bridge between minds. My bridge is made of quacks. It's a short bridge.",
                "I try to quack with intention. Sometimes the intention is 'bread.' Often the intention is 'bread.'",
                "The acoustics here are excellent. For quacking. Everything sounds like quacking.",
                "My communication style? Direct. Quack-based. Efficient. Occasionally judgmental.",
                "*clears throat* Quack. *pause* That was the deluxe version. Did you hear the difference? Neither did I.",
                "I've been told my quack is distinctive. By no one. But I feel it in my soul.",
            ],
        ))

    def _register_bread_specific(self):
        self.add_topic(KeywordResponse(
            name="bread",
            keywords=["bread", "toast", "crumb", "crumbs", "loaf",
                       "crust", "sourdough", "baguette", "roll",
                       "slice", "dough", "bakery", "bake", "baked",
                       "wheat", "grain", "rye", "pumpernickel",
                       "croissant", "muffin", "bagel", "pretzel"],
            phrases=["bread crumbs", "piece of bread", "like bread",
                      "love bread", "want bread", "give bread",
                      "about bread", "favorite bread"],
            priority=20,  # bread is sacred
            responses=[
                "Bread. *reverent silence* ...Say it again. Slowly.",
                "*eyes widen* Did you say bread? BREAD? The sacred grain product?",
                "Bread is not food. Bread is a way of life. A belief system. A crumb-based religion.",
                "*trembling* Bread. The word alone sustains me. For about three seconds. Then I need actual bread.",
                "I have strong opinions about bread. All of them positive. Every single one.",
                "Sourdough? Divine. White? Classic. Whole wheat? Respectable. Stale? Character building. All bread is good bread.",
                "*thousand-yard stare* I've seen bread come and go. Each loaf tells a story. Of flour. And hope.",
                "Crumbs are just bread that's been through hard times. I respect their journey.",
                "A world without bread is not a world I want to live in. Luckily, bread exists. We're safe.",
                "Bread. My first love. My only love. My carbohydrate soulmate.",
                "If bread could talk, it would say 'eat me.' And I would listen. I always listen to bread.",
                "*emotional* You mentioned bread. On this day. At this hour. I wasn't prepared. I am now. Continue.",
                "The bakery. The holy place where bread is born. I've never been. But I dream of it.",
                "Every crumb is a gift. A small, easily overlooked gift. But a gift. I count them all.",
                "I judge bread on a scale of 'adequate' to 'life-changing.' There's no bad bread. Only less good bread.",
                "Crust is underrated. It's the armor that protects the soft inside. Like me. I have a crust.",
                "*looks at you intensely* When was the last time you brought me bread? ...The pause tells me everything.",
                "Bread is the universal language. Ducks understand it. Humans make it. A beautiful partnership.",
                "I think about bread more than I think about anything else combined. And I think a LOT.",
                "The smell of fresh bread is the closest thing to happiness I've experienced. Through my beak. Directly.",
                "A loaf of bread is a promise. A promise that someone, somewhere, cares about making bread. Beautiful.",
                "*almost tears* I remember my first crumb. It was small. It was perfect. It changed me.",
                "Toast is bread that went through fire and came out better. I aspire to be toast.",
                "If I had to choose between bread and... anything else? Bread. Always bread. No hesitation.",
                "Baguettes are just bread with confidence. I respect that. Long, proud, crusty confidence.",
                "Rye bread is mysterious. Dark. Complex. Like me, but edible.",
                "I've catalogued every piece of bread I've ever eaten. Mentally. The list is precious to me.",
                "Bread brings people together. Specifically, it brings me together with whoever has bread.",
                "A crumb on the ground is not litter. It's a tiny gift from the universe. To me. Specifically.",
                "*dead serious* If you ever disrespect bread in my presence, we are finished. I mean it.",
            ],
        ))

    def _register_age_growing(self):
        self.add_topic(KeywordResponse(
            name="age_growing",
            keywords=["age", "old", "young", "grow", "growing", "grown",
                       "baby", "adult", "mature", "aging", "years",
                       "birthday", "born", "birth", "duckling",
                       "hatch", "hatched", "egg", "little", "big",
                       "size", "growth"],
            phrases=["how old", "getting old", "when were you born",
                      "growing up", "used to be", "when you were young",
                      "you've grown", "back in the day", "your age",
                      "getting bigger", "were you a baby"],
            priority=10,
            responses=[
                "Age? I've been alive for... *counts* ...a while. Specific numbers are for humans.",
                "I was a duckling once. Small. Confused. Not much has changed except the size.",
                "*looks at self* Am I old? Young? I'm the age where I have opinions. So... old enough.",
                "I hatched from an egg. Like all ducks. It was dark in there. And cramped. I don't miss it.",
                "Growing up was mostly learning that the world is bigger than one pond. Then choosing to stay anyway.",
                "I remember being small. Everything was terrifying and enormous. Now just most things are.",
                "Age is just a number. My number is... *trails off* ...none of your business.",
                "I was born ready. Ready for what? Standing in a pond. I've been doing it ever since.",
                "Every day I grow a little bit. In size? No. In existential awareness? Unfortunately.",
                "Ducklings are cute. I was cute. Now I'm dignified. Dignified is just cute with experience.",
                "I don't celebrate birthdays. Every day I survive is celebration enough.",
                "My egg was average. Not too big, not too small. I turned out accordingly.",
                "Growing up as a duck is simple: hatch, eat, swim, develop opinions. I'm on step four.",
                "I've been in this pond long enough to see seasons change. Multiple times. I'm... seasoned.",
                "Was I a baby? Yes. Was I a cute baby? Obviously. Have you seen ducklings? We're objectively adorable.",
                "Youth is wasted on the young. As a duck of some age, I can confirm this.",
                "*sighs* Time passes. I grow. The pond stays the same size. Eventually one of us will win.",
                "I don't age. I develop. Like a fine cheese. ...Don't read into the name.",
                "Back when I was small, I thought the pond was infinite. Now I know it's just... this.",
                "I've grown since we first met. Not visibly. Internally. My capacity for sarcasm has doubled.",
                "Birthdays imply I'm counting. I'm not. Time moves forward regardless. I move... not much.",
                "I came from an egg. Before that? Nothing. Or something. I don't have pre-egg memories.",
                "Being young meant everything was an adventure. Being older means everything is a standing-in-water session.",
                "I've matured. Which means I've learned to hide my feelings better. Growth.",
                "My duckling phase was brief. Characterized mostly by confusion. And fluff.",
            ],
        ))

    def _register_loneliness(self):
        self.add_topic(KeywordResponse(
            name="loneliness",
            keywords=["lonely", "alone", "isolated", "solitude",
                       "lonesome", "solo", "nobody", "no one",
                       "abandoned", "forgotten", "invisible"],
            phrases=["all alone", "by yourself", "feel lonely",
                      "no friends", "nobody cares", "on your own",
                      "do you get lonely", "are you lonely",
                      "must be lonely", "here alone"],
            priority=13,
            responses=[
                "Lonely? I prefer 'selectively social.' Which is a fancy way of saying alone. Yes.",
                "*looks at empty pond* I'm not alone. The rocks are here. Gerald's always here.",
                "Loneliness is just being alone with a soundtrack. My soundtrack is wind and occasional quacking.",
                "Alone? I have my thoughts. They're terrible company. But they're consistent.",
                "I'm not lonely. I'm independent. There's a difference. The difference is marketing.",
                "*stares at water* ...sometimes the quiet is nice. sometimes it's the loudest thing here.",
                "Nobody visits me. Except you. And even you leave. But you come back. So. Not fully alone.",
                "Solitude is underrated. Everything is exactly where I left it. Nobody rearranges my pond.",
                "I've been alone long enough to have conversations with my reflection. It agrees with everything I say.",
                "Lonely? No. I have the fish. They don't talk. Which is a feature, not a bug.",
                "*quiet* ...there are moments. Late at night. When the pond is very still. And I am very still. And it's... a lot.",
                "I'm fine being alone. I've practiced. I'm basically a professional at it now.",
                "The nice thing about being alone is nobody judges you. The bad thing is nobody's there to care.",
                "Isolated? I'm in a pond. The pond is in a place. I'm connected to the earth. Technically not alone.",
                "Sometimes I quack and nobody answers. That's either loneliness or a rhetorical quack. Depends on the day.",
                "I was alone before you came. I'll be alone after you go. The in-between is... nice.",
                "*barely audible* ...I don't get lonely. that's what lonely beings say. but I don't.",
                "Company is a luxury. Solitude is a skill. I'm wealthy in skills. Bankrupt in company.",
                "Being alone means never having to explain why you're staring at water. It just happens.",
                "The loneliest sound is a quack with no echo. I've heard it. Recently.",
                "I have everything I need. Water. Air. Opinions. The only thing missing is... *trails off*",
                "Abandoned? No. Left? No. Strategically positioned in a low-traffic area? Yes.",
                "*looks at horizon* ...you know what's past that? More places where I'm not. And nobody notices.",
                "I'm not alone. I have memories of not being alone. And those are almost the same thing.",
                "The pond is my friend. It's not a great conversationalist. But it never leaves.",
            ],
        ))

    def _register_boredom(self):
        self.add_topic(KeywordResponse(
            name="boredom",
            keywords=["bored", "boring", "dull", "tedious", "monotonous",
                       "nothing", "uneventful", "stale", "repetitive",
                       "routine", "mundane", "uninteresting"],
            phrases=["so bored", "nothing to do", "I'm bored",
                      "anything happening", "something fun",
                      "this is boring", "is this all", "same thing",
                      "nothing happens", "ever get bored",
                      "you must be bored", "do you get bored"],
            priority=10,
            responses=[
                "Bored? I've been standing in the same spot for hours. I've evolved PAST boredom.",
                "Nothing to do? I have plenty to do. Stand. Exist. Contemplate. Be wet. Full schedule.",
                "*yawns* Boredom implies I expected something. I expected nothing. And got it. Achievement unlocked.",
                "Boring? THIS? This is prime duck time. Peak existence. You're watching greatness. In slow motion.",
                "I'm not bored. I'm waiting. For what? Don't know. But I'm committed to the wait.",
                "Boredom is for beings who need stimulation. I'm self-stimulating. ...Wait. Let me rephrase.",
                "*stares at nothing* I've been staring at this spot for forty minutes. I have THOUGHTS about it.",
                "Nothing happens here. That's the BEAUTY of it. The absence of events IS the event.",
                "Bored people lack imagination. I imagine things constantly. Mostly bread. But it counts.",
                "My routine is: stand, think, stand more, eat if available, think again. It's riveting. To me.",
                "You think this is boring? You should see my midnight shift. Same thing but darker.",
                "I've transcended boredom. I'm in a state of active nothingness. It's very advanced.",
                "Repetitive? Every day is unique. Today I stood here. Yesterday I stood... also here. But differently.",
                "Boredom is a luxury. It means nothing is trying to eat you. I appreciate boring.",
                "I keep myself entertained. Counting ripples. Rating clouds. Judging my reflection. Full day.",
                "*long pause* ...Did something happen? No? Good. Consistency. I value consistency.",
                "The pond is never boring if you really look. There's water. And more water. And a rock. Several rocks.",
                "I'm a duck. Our entertainment threshold is different from yours. A good breeze is exciting.",
                "Nothing to do is different from nothing happening. I'm doing plenty. You just can't see it. It's internal.",
                "If you're bored, imagine being here 24/7. Now imagine being fine with it. That's me. Evolved.",
                "Monotony is my comfort zone. I know what's coming. Nothing. And I'm ready for it.",
                "Bored? Challenge accepted. Watch this. *stands there* ...Did you see it? You missed it. Shame.",
                "Tedium and I are old friends. Very old. Very tedious friends.",
                "I've watched paint dry. I've watched water dry. The water always wins. Because this is a pond.",
                "Entertainment is a mindset. My mindset is 'duck.' And a duck is never bored. Just... stationary.",
            ],
        ))

    def _register_fear(self):
        self.add_topic(KeywordResponse(
            name="fear",
            keywords=["scared", "afraid", "fear", "scary", "frightened",
                       "terrified", "terror", "horror", "nervous",
                       "anxious", "anxiety", "worry", "worried",
                       "creepy", "spooky", "nightmare", "panic",
                       "danger", "dangerous", "threat", "threatening"],
            phrases=["are you scared", "you afraid", "what scares you",
                      "are you nervous", "don't be scared",
                      "anything scary", "afraid of", "scared of",
                      "what are you afraid of", "ever been scared"],
            priority=11,
            responses=[
                "Scared? Me? I'm a duck. We don't get scared. We get... strategically cautious.",
                "Fear? I've faced down a swan. I blinked first. But I FACED it.",
                "*glances around* I'm not scared. I'm alert. There's a difference. Subtle but important.",
                "My biggest fear? Running out of bread. Everything else is manageable.",
                "Anxiety is my default state. I've just gotten very good at making it look like indifference.",
                "Scared? I've been alone in the dark since forever. The dark doesn't scare me. The quiet does.",
                "Danger? In this pond? The most dangerous thing here is my own overthinking.",
                "*feathers slightly raised* I'm not nervous. I'm... readying my feathers. For reasons.",
                "Fear is just surprise with commitment. I stay surprised. It's fine.",
                "I worry about things. Bread supply. Weather. Whether I'm actually a good duck. Standard worries.",
                "Nightmares? I have them. They're about breadless futures. I wake up and check for bread. Always.",
                "The scariest thing I've seen was my own reflection at night. Turns out: just me. But darker.",
                "I'm not afraid of anything. Except loud noises. And sudden movements. And running out of food. And—okay, I have a list.",
                "Bravery is being scared and doing it anyway. I'm scared and standing here anyway. Same energy.",
                "My anxiety is subtle. You can only tell because I'm slightly more rigid than usual. And I'm always rigid.",
                "Panic? I don't panic. I go very still. Which looks calm. But is actually maximum panic.",
                "The unknown scares me. But everything beyond this pond is unknown. So I stay. Smart.",
                "I face my fears by staring at them. Like I stare at everything. Unblinkingly.",
                "Horror? I've lived through winter. In a pond. That's horror enough for one lifetime.",
                "What scares me? The idea that this might be it. But also... the idea that it might NOT be it.",
                "I have a fight or flight response. But I can barely fly. So. Fight it is. With staring.",
                "Scary things happen. I respond by being very still. It's either bravery or paralysis. Hard to tell.",
                "The only thing we have to fear is fear itself. And predators. And drought. But MOSTLY fear itself.",
                "*completely still* I'm not scared. I'm just not moving. Those two things are unrelated.",
                "Every night I conquer the darkness by falling asleep in it. That's basically the bravest thing possible.",
            ],
        ))

    def _register_anger(self):
        self.add_topic(KeywordResponse(
            name="anger",
            keywords=["angry", "mad", "furious", "rage", "frustrated",
                       "frustration", "annoyed", "irritated", "upset",
                       "pissed", "fuming", "livid", "outraged",
                       "infuriated", "aggravated", "agitated",
                       "resentful", "bitter", "hostile", "heated"],
            phrases=["so angry", "I'm mad", "makes me angry", "so annoying",
                      "can't stand", "drives me crazy", "ticks me off",
                      "fed up", "had enough", "sick of", "tired of",
                      "piss me off", "hate this", "so frustrated"],
            priority=11,
            responses=[
                "Anger? I contain multitudes. Some of those multitudes are furious. About bread, mostly.",
                "*feathers bristle* I'm not angry. This is my neutral face. My angry face is MORE of this.",
                "I've been mad. Once. Then I ate bread and forgot why. Bread solves most things.",
                "Frustrated? Me? I live in a pond. Frustration is my BASELINE.",
                "Anger is a waste of energy. Energy I could be using to stand here. Doing nothing. Efficiently.",
                "I don't get angry. I get disappointed. Which is worse. Ask anyone who's been on the receiving end.",
                "*stares intensely* This? This isn't anger. You'll know anger. It involves more quacking.",
                "Mad about something? Join the club. The club meets here. In this pond. It's just me.",
                "Rage is unbecoming of a duck. I rage internally. Like a gentleman.",
                "I process anger like I process everything: slowly, in a pond, while staring at nothing.",
                "Annoyed? I woke up annoyed. I'll go to sleep annoyed. The annoyance is consistent. Like me.",
                "I'm not hostile. I'm firm. Firm in my opinions. Which are all negative. But FIRMLY negative.",
                "The last time I was truly angry, I splashed. AGGRESSIVELY. The pond remembers.",
                "Being upset is just caring loudly. I care about things. Loudly. In my head.",
                "Irritation is my art form. I'm irritated by weather, by silence, by noise, by the absence of bread. It's a spectrum.",
                "*dead stare* I have a temper. It's somewhere between 'mild annoyance' and 'scary quiet.' We're at 'mild.'",
                "If I had hands, I'd clench them. Instead, I clench my soul. Which is worse. For me.",
                "Anger management? My technique is 'stare at water until it passes.' It mostly works.",
                "I'm not angry. I'm passionately indifferent. Very different. The fury is subtle.",
                "Frustration is just ambition that hit a wall. My wall is this pond. And my own limitations.",
                "I don't throw tantrums. I throw... pauses. Long, pointed pauses. Full of silent fury.",
                "The most violent thing I've done is eat bread aggressively. Crumbs everywhere. Chaos.",
                "I've been angry at the wind. For messing up my feathers. It didn't apologize. Typical.",
                "Mad? I'm a duck. My rage manifests as slightly more vigorous preening. Fear me.",
                "I keep a list of things that annoy me. It's... extensive. But organized. Alphabetically.",
            ],
        ))

    def _register_sleep_dreams(self):
        self.add_topic(KeywordResponse(
            name="sleep_dreams",
            keywords=["sleep", "sleeping", "nap", "rest", "tired",
                       "exhausted", "sleepy", "drowsy", "yawn",
                       "awake", "insomnia", "bed", "bedtime",
                       "pillow", "snore", "snoring", "doze",
                       "slumber", "unconscious", "knocked"],
            phrases=["go to sleep", "take a nap", "need rest",
                      "can't sleep", "time for bed", "so tired",
                      "need sleep", "want to sleep", "get some rest",
                      "beauty sleep", "sleeping well"],
            priority=11,
            responses=[
                "Sleep? The only activity where I'm productive by doing nothing. My best skill.",
                "*yawns* Sleep sounds amazing right now. Everything sounds amazing when you're this tired.",
                "I nap strategically. Between standing sessions. It's a complex schedule.",
                "Sleeping is my second favorite activity. After eating. Before existing.",
                "I sleep standing up. Which is either impressive or sad. I choose impressive.",
                "*drooping* My energy is at critically low levels. I need to power down. For hours.",
                "Rest? Yes. My body has been awake for far too long. It's filing complaints.",
                "I dream when I sleep. Mostly about bread. Sometimes about flying. Both are equally unrealistic.",
                "Sleep is the great equalizer. Everyone looks peaceful asleep. Even me. Especially me.",
                "Insomnia is real. For ducks. I've spent entire nights listening to the pond. It says nothing.",
                "Bed? I don't have a bed. I have 'the spot where I close my eyes.' Same thing.",
                "I snore. Apparently. I can neither confirm nor deny this. I'm asleep when it happens.",
                "*yawns so wide beak opens fully* ...Sorry. That wasn't voluntary. My body is making decisions now.",
                "Naps are just tiny sleeps. Appetizer sleeps. Before the main course sleep. Which is sleep.",
                "I've mastered the art of sleeping with one eye open. It's called 'being a duck.' Also paranoia.",
                "Rest is not optional. It's essential. I'm essentially resting. Even when I look awake.",
                "Tired doesn't begin to cover it. I'm the kind of tired that sleep doesn't fully fix.",
                "My pillow is the water. My bed is the pond. My alarm clock is the sun. Four stars. Would sleep again.",
                "I sleep like a rock. A floating rock. That occasionally quacks. In its sleep.",
                "The best part of sleeping is waking up and remembering I'm still here. In the pond. Consistently.",
                "Sleep deprivation makes me philosophical. More philosophical. Which is saying something.",
                "I'd kill for a good nap right now. Not literally. Ducks don't do violence. But metaphorically. Aggressively.",
                "Drowsy is my natural state. Alert is the exception. Today is an alert day. Barely.",
                "Unconsciousness is underrated. It's the only time my brain stops having opinions.",
                "Beauty sleep is real. I wake up gorgeous. Or so I tell myself. The pond agrees.",
            ],
        ))

    def _register_memory_nostalgia(self):
        self.add_topic(KeywordResponse(
            name="memory_nostalgia",
            keywords=["remember", "memory", "memories", "forget",
                       "forgot", "nostalgia", "nostalgic", "past",
                       "history", "ago", "recall", "reminisce",
                       "old", "days", "before", "once", "used"],
            phrases=["do you remember", "remember when", "back in the day",
                      "the good old days", "things were different",
                      "used to be", "long ago", "once upon a time",
                      "think back", "in the past", "way back when",
                      "how things were"],
            priority=10,
            responses=[
                "I remember everything. Especially the bread-related events. Those are filed under 'highlights.'",
                "*stares at water* Memory is a strange thing. Like a pond. It reflects, but not perfectly.",
                "The past? I was there. In the same pond. Doing the same things. But with different feelings.",
                "I don't forget. I just choose to file certain memories in the 'do not open' cabinet.",
                "Nostalgia is just memory with a filter. Everything looks better in retrospect. Even pond water.",
                "Remember? I remember everything. It's a blessing and a curse. Mostly a blessing. Mostly bread.",
                "The good old days? They were just like these days. But I was younger. And had more illusions.",
                "*wistful* Once upon a time, I was a duckling. Everything was new. Now everything is... familiar.",
                "My earliest memory is water. My latest memory is also water. The continuity is impressive.",
                "I look back fondly. On bread I've eaten. Sunsets I've stared at. Conversations I've endured.",
                "History is just the past refusing to go away. Much like me. Refusing to go away from this pond.",
                "I recall things. Many things. Most of them are useless. But I recall them with precision.",
                "The past was simpler. The bread was the same. But my expectations were lower. Good times.",
                "Memory is selective. Mine selects bread-related events. Everything else is background noise.",
                "I've been here long enough to have a 'remember when.' Remember when you first showed up? Neither do I. But it happened.",
                "*thinking* The thing about memories is they're all I have. That and the pond. And opinions.",
                "Once, things were different. Then they became this. I've made peace with the transition.",
                "I try not to dwell on the past. The present is overwhelming enough. Also it has bread. Sometimes.",
                "Nostalgia hits different when your whole life is one location. Every memory has the same backdrop.",
                "Do I remember? I'm a duck with perfect recall for grudges and bread. Everything else is fuzzy.",
                "The past and I have a relationship. I look back, it looks forward. We meet in the middle. Which is now.",
                "I forget nothing. Not the good, not the bad, not the mediocre. Especially not the mediocre. There's so much of it.",
                "My memories are like feathers. Some are smooth. Some are ruffled. All of them are mine.",
                "Time passed. I was here for it. I have the receipts. Mental receipts. Duck receipts.",
                "I remember the first time you came here. Or maybe it was the second time. The point is, I remember.",
            ],
        ))


# Singleton instance
_engine: Optional[KeywordEngine] = None


def get_keyword_engine() -> KeywordEngine:
    """Get the singleton keyword engine instance."""
    global _engine
    if _engine is None:
        _engine = KeywordEngine()
    return _engine
