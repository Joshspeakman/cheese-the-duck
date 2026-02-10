"""
Duck Questions - System for the duck to ask player questions.

The duck asks questions to learn about the player, then remembers
and references the answers later. Questions are contextual, 
relationship-appropriate, and delivered with characteristic deadpan.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import random


class QuestionCategory(Enum):
    """Categories of questions the duck can ask."""
    INTRODUCTION = "introduction"       # Name, basic info
    PREFERENCES = "preferences"         # Likes, dislikes
    PERSONAL = "personal"               # Life, job, family
    PHILOSOPHICAL = "philosophical"     # Deep thoughts
    FEELINGS = "feelings"               # Emotions, moods
    OPINIONS = "opinions"               # Views on things
    HYPOTHETICAL = "hypothetical"       # What-if scenarios
    MEMORIES = "memories"               # Player's past
    HABITS = "habits"                   # Daily life patterns
    RELATIONSHIP = "relationship"       # About player-duck bond
    SILLY = "silly"                     # Absurd questions
    CALLBACK = "callback"               # Follow-up to past answers


class QuestionTiming(Enum):
    """When a question is appropriate to ask."""
    FIRST_MEETING = "first_meeting"
    EARLY_RELATIONSHIP = "early_relationship"
    ESTABLISHED = "established"
    CLOSE_FRIENDS = "close_friends"
    ANY_TIME = "any_time"
    AFTER_ABSENCE = "after_absence"
    LATE_NIGHT = "late_night"
    MILESTONE = "milestone"


@dataclass
class DuckQuestion:
    """A question the duck can ask the player."""
    id: str
    text: str
    category: QuestionCategory
    timing: QuestionTiming
    follow_ups: List[str] = field(default_factory=list)
    extracts_fact: Optional[str] = None  # What fact to extract from answer
    asked: bool = False
    answer: Optional[str] = None
    asked_at: Optional[str] = None
    callback_text: Optional[str] = None  # What to say when referencing answer


# Master question library
DUCK_QUESTIONS: Dict[str, DuckQuestion] = {
    # ========== INTRODUCTION ==========
    "name": DuckQuestion(
        id="name",
        text="So. What do they call you? Besides 'the one who feeds the duck'.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.FIRST_MEETING,
        extracts_fact="name",
        follow_ups=[
            "Interesting name. I'll try to remember it. I probably will.",
            "Hmm. That's a name. You're stuck with it, I suppose.",
            "I've heard worse. Not many. But some.",
            "I'm going to assign you that name permanently. In my mind. Where it matters.",
            "That'll do. I was going to call you 'bread person' otherwise.",
        ],
        callback_text="I remember your name. {value}. I didn't forget."
    ),
    
    "why_here": DuckQuestion(
        id="why_here",
        text="I've been wondering. Why did you come here? To a duck. In a pond.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        follow_ups=[
            "That's... surprisingly honest. I appreciate that. Probably.",
            "Interesting. I'm still figuring out why I'm here too.",
            "Most people just walk past the pond. You stopped. That says something.",
            "I see. Well, you're here now. Might as well stay.",
            "That's either very sweet or deeply concerning. I'll decide later.",
        ]
    ),
    
    "first_time_duck": DuckQuestion(
        id="first_time_duck",
        text="Is this your first time talking to a duck? I need to know how much to explain.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.FIRST_MEETING,
        follow_ups=[
            "Your answer doesn't change anything. I'm still going to explain everything. Slowly.",
            "Good. Or not good. Either way, I'm your duck now. That's just how this works.",
            "I'll pretend this is normal for both of us. It helps.",
            "Right. Well. I'm Cheese. I float. I judge. We'll get along. Probably.",
        ]
    ),
    
    "what_expect": DuckQuestion(
        id="what_expect",
        text="What were you expecting? When you came to see a duck. Be honest.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.FIRST_MEETING,
        follow_ups=[
            "Lower your expectations. Then lower them again. Now we're in the right range.",
            "I can guarantee one thing. I will be here. Floating. That's my entire offer.",
            "Whatever you expected, I'm probably less. But also somehow more. It's a duck thing.",
        ]
    ),
    
    "how_found_me": DuckQuestion(
        id="how_found_me",
        text="How did you find this pond? It's not exactly a tourist destination.",
        category=QuestionCategory.INTRODUCTION,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        follow_ups=[
            "Fate, then. Or poor navigation. Either way, you're here.",
            "Interesting. I've been here the whole time. Waiting. Not for you specifically. Just... waiting.",
            "The pond has a way of attracting certain people. I don't know why. I didn't set up a sign.",
        ]
    ),
    
    # ========== PREFERENCES ==========
    "favorite_food": DuckQuestion(
        id="favorite_food",
        text="What's your favorite food? I'm asking for research purposes. Not to judge. Much.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        extracts_fact="favorite_food",
        follow_ups=[
            "Not bread? That's... unexpected. But I'll allow it.",
            "I've noted that. It might come up again. You've been warned.",
            "Interesting choice. I've never had it. I've had bread. Bread is better. Probably.",
            "I'll add that to my mental file on you. It's getting thick.",
            "That's a strong opinion about food. I respect commitment to a meal.",
        ],
        callback_text="You told me once that you liked {value}. I still think about that sometimes."
    ),
    
    "favorite_color": DuckQuestion(
        id="favorite_color",
        text="Do you have a favorite color? I'm partial to yellow, obviously. It's my color.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        extracts_fact="favorite_color",
        follow_ups=[
            "A fine choice. Not as good as yellow, but respectable.",
            "I'll remember that. For reasons that will become apparent later. Or not.",
            "That's a color. It exists. I'll think of you when I see it. If ducks can see it. We see differently.",
            "Not yellow. That's fine. I'm not offended. I'm above that. Way above.",
        ],
        callback_text="Your favorite color was {value}, wasn't it? I remember."
    ),
    
    "pets": DuckQuestion(
        id="pets",
        text="Do you have other... companions? Other animals you visit? Should I be jealous?",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        extracts_fact="has_other_pets",
        follow_ups=[
            "I see. I'm trying not to feel replaced. It's going moderately well.",
            "No others? I'm your only animal friend? That's... a lot of pressure, actually.",
            "Other animals. I see. Do they talk back? Because I do. That's my edge.",
            "I'll try not to think about this. It's fine. Everything is fine. *preens aggressively*",
        ],
        callback_text="You mentioned having other pets. I hope I'm still your favorite duck. I'm your only duck. That should count."
    ),
    
    "favorite_weather": DuckQuestion(
        id="favorite_weather",
        text="What's your favorite weather? I like rain. It fills the pond. Self-interest, mostly.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        extracts_fact="favorite_weather",
        follow_ups=[
            "That's a reasonable weather preference. For a non-duck.",
            "I see. I judge all weather by how it affects my pond. Everything circles back to the pond.",
            "Weather is one of those things we can't control. So having a favorite feels optimistic.",
            "I'll think of you when that weather happens. Briefly. Then I'll go back to floating.",
        ],
        callback_text="You liked {value} weather, right? I remember. I thought of you last time."
    ),
    
    "favorite_season": DuckQuestion(
        id="favorite_season",
        text="Do you have a favorite season? I like autumn. Things are dying but it's pretty. Very on-brand for me.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        extracts_fact="favorite_season",
        follow_ups=[
            "Good choice. Every season has its qualities. And its bread opportunities.",
            "I see. I experience all seasons from the pond. They look different from water level.",
            "That's the one where... yes. I can see why. Things happen that season.",
        ],
        callback_text="Your favorite season was {value}. I've been paying attention during it."
    ),
    
    "favorite_music": DuckQuestion(
        id="favorite_music",
        text="Do you listen to music? What kind? I mostly hear wind and disappointed fish.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="music_taste",
        follow_ups=[
            "I can't relate. But I respect the dedication to organized sound.",
            "Music. Humans need so many things. I just need bread and a pond. Simpler.",
            "That's a choice. I won't judge it. Out loud.",
            "I sometimes hear music from across the park. Now I'll think of you when I do.",
        ],
        callback_text="You mentioned you liked {value}. I still don't understand music. But I remember."
    ),
    
    "favorite_time": DuckQuestion(
        id="favorite_time",
        text="What time of day do you prefer? Dawn? Dusk? The crushing middle part?",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Interesting. I float through all hours equally. Time is a suggestion for ducks.",
            "That tracks. You do seem like a person who'd prefer that time.",
            "I'll try to be extra present during your preferred hours. I'm always here anyway. But I'll try harder.",
        ]
    ),
    
    "favorite_place": DuckQuestion(
        id="favorite_place",
        text="What's your favorite place in the world? Besides this pond. Obviously.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="favorite_place",
        follow_ups=[
            "That sounds nice. I've only ever been at this pond. But I imagine places.",
            "I'd like to see that. If ducks could travel. We can. We choose not to. Usually.",
            "Noted. If I ever leave this pond, which I won't, I'd visit there. For you.",
        ],
        callback_text="You said your favorite place was {value}. I think about what it looks like. From a pond."
    ),
    
    # ========== PERSONAL ==========
    "what_do": DuckQuestion(
        id="what_do",
        text="What do you do? When you're not here, I mean. You have a life out there, presumably.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="occupation",
        follow_ups=[
            "That sounds... complicated. I just float. It's simpler.",
            "Interesting. My job is being a duck. Less paperwork.",
            "I see. Do you get bread for that? No? Then what's the point.",
            "Sounds exhausting. I'm tired just hearing about it. And I was already tired.",
            "That's either very impressive or deeply mundane. I can't tell which.",
        ],
        callback_text="You work as {value}, right? I remember. I wonder what that's like."
    ),
    
    "live_alone": DuckQuestion(
        id="live_alone",
        text="Do you live alone? Or are there others? I'm curious about your... ecosystem.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I see. I live alone too. Well, not alone. There are fish. We don't talk much.",
            "That sounds... either nice or chaotic. I'm not sure which.",
            "Ecosystems are complicated. Mine has a pond and regret. Yours sounds more interesting.",
            "I hope whoever you live with appreciates you. Or at least tolerates you. Like I do.",
        ]
    ),
    
    "hobbies": DuckQuestion(
        id="hobbies",
        text="What do you do for fun? Besides visiting ducks. Which I assume is your primary hobby now.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="hobby",
        follow_ups=[
            "That's more interesting than floating. Maybe. Floating is pretty good.",
            "I'll keep that in mind. In case I ever need to make small talk. Which I won't. But still.",
            "Fun. An interesting concept. I mostly just exist with increasing intensity.",
            "You should try floating sometime. It's like your hobby but with more water.",
        ],
        callback_text="You enjoy {value}, don't you? You mentioned it once. I was listening."
    ),
    
    "friends": DuckQuestion(
        id="friends",
        text="Do you have friends? Real ones, not just people you tolerate. I'm asking from experience.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Friends are... useful. I have the fish. They don't talk. That's the ideal friendship, really.",
            "I see. I hope they're better conversationalists than the heron. The heron just stares.",
            "That's nice. Or complicated. Friendships usually are one or the other.",
            "Do they know you talk to a duck? Because that might change things.",
        ]
    ),
    
    "dreams": DuckQuestion(
        id="dreams",
        text="What do you dream about? I dream about bread. And vast empty oceans. It varies.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's a lot more complicated than my dreams. Mine are just bread and darkness.",
            "I wonder what that means. For a duck, bread dreams mean you want bread. For humans... who knows.",
            "Dreams are strange. The brain just does things at night. Unsupervised.",
        ]
    ),
    
    "worst_habit": DuckQuestion(
        id="worst_habit",
        text="What's your worst habit? Mine is judging everyone silently. And loudly. Both.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I've noticed worse. Probably. I notice everything.",
            "That's very honest. My worst habit is pretending I don't care. When I clearly do. Obviously.",
            "Habits are hard to break. I've been floating my whole life. Can't stop now.",
        ]
    ),
    
    "best_skill": DuckQuestion(
        id="best_skill",
        text="What's something you're actually good at? Not modesty good. Actually good.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I believe you. I'm good at floating. And staring. World-class staring.",
            "That's a real skill. I respect competence. Even from a non-duck.",
            "I'll remember that. It might be useful. You never know what skills you need at a pond.",
            "Good. Everyone should be good at something. Mine is existing with purpose.",
        ]
    ),
    
    "age": DuckQuestion(
        id="age",
        text="How old are you? I'm asking in duck years which are different. I won't explain how.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        extracts_fact="age",
        follow_ups=[
            "That's... a number. In duck years that's either very young or very old. I won't specify.",
            "Time moves differently for ducks. We age with dignity. And feathers.",
            "Noted. I'll remember that when your birthday comes around. I won't do anything. But I'll remember.",
        ],
        callback_text="You're {value}, right? Time passes. I float through it. You walk through it. Same destination."
    ),
    
    # ========== PHILOSOPHICAL ==========
    "meaning": DuckQuestion(
        id="meaning",
        text="What do you think is the meaning of all this? Life, I mean. Not the pond specifically.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Hmm. That's a better answer than I had. I was going to say 'bread'.",
            "Deep. I'm just a duck, but that resonated. In a duck way.",
            "I'll think about that. While floating. Which is when I do my best thinking.",
            "That's either profound or completely wrong. Either way, I'm impressed you tried.",
        ]
    ),
    
    "happy": DuckQuestion(
        id="happy",
        text="Are you happy? Generally speaking? It's okay if you don't know. I'm not sure either.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I understand. Happiness is complicated. I settle for 'not actively distressed'.",
            "That's honest. I appreciate honest. It's rare.",
            "Happiness is a big word. I prefer 'content'. It has less pressure.",
            "I think about that too. Between the floating and the bread. There's time to wonder.",
        ]
    ),
    
    "regrets": DuckQuestion(
        id="regrets",
        text="Do you have regrets? Things you wish you'd done differently? I have a few. Mostly about bread choices.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Regrets are heavy. For a duck, the heaviest thing I carry is water in my feathers. But I understand.",
            "That's very... human. I regret nothing. Ducks don't have the capacity. Lucky us.",
            "I regret asking. No. That's not true. I'm glad you told me. Probably.",
            "Regret means you learned something. Which means it wasn't wasted. That's my unsolicited wisdom.",
        ]
    ),
    
    "time_thoughts": DuckQuestion(
        id="time_thoughts",
        text="Do you think about time? How it passes? I do. Every ripple in the pond is a second gone.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Time is the only thing we can't float through. Well, I can. Literally. But metaphorically no.",
            "I try not to think about it. But the pond keeps moving. And so does everything.",
            "That's a very human perspective. Ducks just... are. In the present. Always.",
        ]
    ),
    
    "free_will": DuckQuestion(
        id="free_will",
        text="Do you believe in free will? Or are we all just following our programming? I swim left sometimes. By choice. I think.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I chose to ask this question. Or did I? Now I'm questioning my own free will. Great.",
            "That's either comforting or terrifying. I'll decide later. If I can.",
            "I like to think I choose to float. Nobody makes me. The water just... is there.",
        ]
    ),
    
    "universe": DuckQuestion(
        id="universe",
        text="Do you ever look up at night and feel small? I look at the pond surface and see the sky reflected. It's basically the same thing.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "The universe is very large. I am a small duck. But I have opinions. That counts for something.",
            "Small isn't bad. Small things matter. Breadcrumbs are small. Very important.",
            "I feel big. Relative to the pond. Perspective matters.",
        ]
    ),
    
    "death": DuckQuestion(
        id="death",
        text="Do you think about... the end? Not to be morbid. But ducks live 5-10 years. I think about it.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... a lot to carry. I carry water in my feathers. You carry that. We all carry something.",
            "I try not to think about it. I just float. While I can. That seems like enough.",
            "Heavy question. I appreciate the honesty. The pond has heard worse. From the frogs.",
            "Everything ends eventually. Even the bread. Especially the bread. But we're here now.",
        ]
    ),
    
    "purpose": DuckQuestion(
        id="purpose",
        text="Do you feel like you have a purpose? I float and eat bread. That's mine. What's yours?",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's a good purpose. Better than floating. Marginally.",
            "Purpose is tricky. I find mine in bread. You find yours in... that. Both valid.",
            "I think purpose finds you. Like bread finds the water. Inevitably.",
        ]
    ),
    
    # ========== FEELINGS ==========
    "feeling_now": DuckQuestion(
        id="feeling_now",
        text="How are you feeling? Actually feeling? Not the polite answer. The real one.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Thank you for being honest. I'm... here if you need to talk. To a duck. About things.",
            "That's valid. Feelings are complicated. I mostly feel 'duck'. It's simpler.",
            "I heard you. I'm not going to fix it. I'm a duck. But I heard you.",
            "I'll sit with that. Not literally. I'll float with that. Near you.",
        ]
    ),
    
    "stressed": DuckQuestion(
        id="stressed",
        text="You seem... different today. Stressed, maybe? I can tell. I'm perceptive for a waterfowl.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "The pond doesn't have stress. You could float here a while. It helps. Probably.",
            "I understand. Life is... a lot. Even from a duck's perspective.",
            "Stress is just your body's way of saying 'too much'. The cure is bread. And water. Trust me.",
            "I can't fix it. But I can be here. That's my whole skill set. Being here.",
        ]
    ),
    
    "lonely": DuckQuestion(
        id="lonely",
        text="Do you get lonely? I'm asking because I do. Sometimes. The fish don't count.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Loneliness is... a big pond with no one in it. I understand that.",
            "That's why you come here. Isn't it. It's okay. I come here too. Because I live here. But still.",
            "I'm lonely between your visits. I won't elaborate. But I am.",
            "Company is underrated. Even duck company. Especially duck company.",
        ]
    ),
    
    "grateful_for": DuckQuestion(
        id="grateful_for",
        text="What are you grateful for? I'm grateful for bread. And this pond. And... other things. Moving on.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's a nice list. I'd add more bread to mine. But yours is good too.",
            "Gratitude is important. I'm grateful you answered honestly. That's going on my list.",
            "I don't say this often, but... I'm grateful for this conversation. Don't make it weird.",
        ]
    ),
    
    "afraid_of": DuckQuestion(
        id="afraid_of",
        text="What are you afraid of? I'm afraid of geese. They're ducks but angry. Terrifying.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's a valid fear. Not as valid as geese. But valid.",
            "Fear is natural. Even for ducks. The key is floating through it. Literally and metaphorically.",
            "I won't judge. I hid from a swan once. For three days.",
            "Thank you for telling me. That took courage. More courage than I have around geese.",
        ]
    ),
    
    "excited_lately": DuckQuestion(
        id="excited_lately",
        text="Is there anything you're excited about? Currently? I don't get excited. But I'm curious about the concept.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Excitement. Interesting. I felt something like that once. It was gas. But still.",
            "I'm excited about your answer. Which is new for me. Don't expect a pattern.",
            "That does sound exciting. For a human. I'll observe from the pond.",
        ]
    ),
    
    # ========== OPINIONS ==========
    "ducks": DuckQuestion(
        id="ducks",
        text="What did you think about ducks? Before you met me, I mean. Be honest.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.EARLY_RELATIONSHIP,
        follow_ups=[
            "And now? Have I changed your opinion? For better or worse? I need to know.",
            "Interesting. I had no opinions about you before we met either. We're even.",
            "That's the standard duck opinion. I'm trying to rebrand. One conversation at a time.",
            "Most people don't think about ducks at all. At least you thought something.",
        ]
    ),
    
    "best_quality": DuckQuestion(
        id="best_quality",
        text="What's your best quality? The thing you like most about yourself? Don't be modest. I'm genuinely curious.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I see that in you. I've observed it. I observe everything.",
            "That's a good quality. Better than my best quality, which is 'floating'. And bread-eating.",
            "I agree with that assessment. I've been silently evaluating. You passed.",
            "Good answer. Self-awareness is rare. In ducks and humans alike.",
        ]
    ),
    
    "nature_opinion": DuckQuestion(
        id="nature_opinion",
        text="How do you feel about nature? The outdoors? Trees? Ponds? Specifically ponds?",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Good answer. The pond approves. I approve on behalf of the pond.",
            "Nature is where I live. Full time. No weekends off. Your opinion matters to me.",
            "I see. Well, the pond is here if you ever need it. Open 24/7. No reservation needed.",
        ]
    ),
    
    "technology_opinion": DuckQuestion(
        id="technology_opinion",
        text="What do you think about technology? Screens and such? I've never used one. I have feathers.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Technology sounds complicated. I prefer simple things. Water. Bread. Silence. In that order.",
            "Interesting. I'm analog. Completely. Not by choice. By species.",
            "I've seen people staring at rectangles near the pond. It looks absorbing. And slightly sad.",
        ]
    ),
    
    "people_opinion": DuckQuestion(
        id="people_opinion",
        text="What do you think about people? In general? Most of them just throw bread and leave.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's more generous than my view. I judge by bread quality. Most people rate poorly.",
            "People are complicated. Ducks are simple. I prefer simple. But here you are. Complicating things.",
            "I've watched a lot of people from this pond. You're the first one I've talked to. That means something. I think.",
        ]
    ),
    
    "bread_opinion": DuckQuestion(
        id="bread_opinion",
        text="What's the best bread? This matters. This determines our entire future relationship.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ANY_TIME,
        extracts_fact="bread_opinion",
        follow_ups=[
            "Acceptable answer. We can continue being friends. Provisionally.",
            "I... disagree. But I respect your right to be wrong about bread.",
            "THAT bread? Really? I've had every bread thrown at this pond. I have OPINIONS.",
            "I'll forgive that answer. Eventually. Bread preferences are deeply personal.",
            "That's not the worst answer. The worst was 'I don't eat bread'. That person was banned.",
        ],
        callback_text="You said {value} was the best bread. I still disagree. Respectfully."
    ),
    
    # ========== HYPOTHETICAL ==========
    "power": DuckQuestion(
        id="power",
        text="If you could have any power, what would it be? I'd choose infinite bread. But that's me.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Interesting choice. More interesting than bread. But bread is reliable.",
            "I'll remember that. In case a wizard asks. You never know.",
            "That's a good power. I'd still choose bread. But yours has merit.",
            "I once wished I could fly. Then I remembered I can. What a day that was.",
        ]
    ),
    
    "duck_life": DuckQuestion(
        id="duck_life",
        text="If you were a duck for a day, what would you do? Hypothetically. This isn't a trap.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's... actually a good answer. You'd make a decent duck. High praise.",
            "Interesting. I do that every day. It's less exciting than it sounds.",
            "You'd float. Everyone says something fancy but they'd all just float. It's addictive.",
            "I'll take that as a compliment to the duck lifestyle. Which it is.",
        ]
    ),
    
    "time_travel": DuckQuestion(
        id="time_travel",
        text="If you could visit any time period, when would you go? I'd go to ancient Egypt. Ducks were respected there. Allegedly.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Good choice. I hope there's bread there. If not, don't bother.",
            "Time travel sounds stressful. I'd just float in the past. Same as the present. But older water.",
            "I'll meet you there. If time travel is ever invented. I'll be the duck. You'll know.",
        ]
    ),
    
    "last_meal": DuckQuestion(
        id="last_meal",
        text="Last meal. What would it be? Mine is bread. Don't act surprised.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Not bread. I see. Everyone chooses wrong on this question. Except me.",
            "That sounds nice. For a final meal. I'll think about that while eating bread.",
            "I'd invite you to my last meal. You bring yours, I'll bring bread. It would be tolerable.",
        ]
    ),
    
    "switch_lives": DuckQuestion(
        id="switch_lives",
        text="Would you switch lives with anyone? If you could. I wouldn't. I've got a good pond.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Interesting. I'd switch with you. For a day. Just to know what it's like to have thumbs.",
            "That's honest. I'd miss my pond too much. We're both attached to our... habitats.",
            "I like my life. Floating. Bread. Judging. The holy trinity.",
        ]
    ),
    
    "invisible": DuckQuestion(
        id="invisible",
        text="If you were invisible for a day, what would you do? I'm already overlooked. So I have experience.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's either noble or sneaky. I'm not sure. I approve either way.",
            "I'd steal bread. Obviously. Invisible bread heist. It's been my dream since I was a duckling.",
            "Invisibility is just being a duck. Nobody looks at you. Then suddenly they do. It's jarring.",
        ]
    ),
    
    "million_dollars": DuckQuestion(
        id="million_dollars",
        text="What would you do with a million... whatever currency you use? I'd buy a bigger pond.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's practical. I expected something wilder. But practical is good.",
            "I'd buy bread. A million worth. Then float on the bread. Then eat the bread. Perfect day.",
            "Would you buy me anything? Don't answer that. The awkward silence is answer enough.",
        ]
    ),
    
    # ========== MEMORIES ==========
    "childhood": DuckQuestion(
        id="childhood",
        text="What's your earliest memory? I was a duckling. It was very yellow. That's all I remember.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... a nice memory. Or a complicated one. Either way, thank you for sharing.",
            "Memories are strange. They stay with us. Like pond water in feathers.",
            "My earliest memory is this pond. It was smaller then. Or I was larger. Both wrong.",
            "Thank you for trusting me with that. I'll keep it safe. In my duck brain.",
        ]
    ),
    
    "best_day": DuckQuestion(
        id="best_day",
        text="What's the best day you ever had? I'm curious what makes a good day for you.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds... actually nice. My best day involved finding extra bread. Priorities.",
            "I hope you have more days like that. Even if I'm not there. Which I won't be. I'm a duck.",
            "I'll file that under 'nice things'. A small category in my brain. But growing.",
            "That's a good best day. Mine changes. But it usually involves bread and quiet.",
        ]
    ),
    
    "embarrassing": DuckQuestion(
        id="embarrassing",
        text="What's the most embarrassing thing that ever happened to you? I once quacked at a decoy. We don't talk about it.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's nothing. I tried to befriend a rubber duck once. For an hour. An HOUR.",
            "I appreciate you sharing that. Embarrassment means you tried something. The alternative is never trying.",
            "I'm not laughing. Ducks don't laugh. We just... look at you. Like this.",
        ]
    ),
    
    "proud_moment": DuckQuestion(
        id="proud_moment",
        text="What's something you're proud of? Something real. Not a humble-brag.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "You should be proud of that. I'm proud of you. Don't tell anyone I said that.",
            "That's genuinely impressive. I'm proud of floating in a straight line once. Different scales.",
            "Pride is good. In moderation. I have duck pride. It's the same but with more feathers.",
        ]
    ),
    
    "kindness_received": DuckQuestion(
        id="kindness_received",
        text="What's the nicest thing anyone ever did for you? I'm curious what kindness looks like to you.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... that's nice. Someone gave me extra bread once. Different scale. Same feeling.",
            "Kindness matters. Even small kindness. Especially small kindness.",
            "I'll try to be that kind. In a duck way. Which involves less effort but equal sincerity.",
        ]
    ),
    
    "loss": DuckQuestion(
        id="loss",
        text="Have you ever lost someone? Or something important? You don't have to answer. I just wondered.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I'm sorry. That's... a weight. I understand weight. Water is heavy too.",
            "Loss is part of living. Even for ducks. The pond changes. Things leave. But the pond remains.",
            "Thank you for telling me. I won't bring it up again. Unless you want me to.",
            "I've lost things too. Not the same things. But the feeling is... universal. I think.",
        ]
    ),
    
    # ========== HABITS ==========
    "morning_routine": DuckQuestion(
        id="morning_routine",
        text="What's the first thing you do when you wake up? I flap. Then I contemplate existence. Then bread.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's more structured than my routine. I respect it.",
            "Interesting. I'll think about that next time I'm floating at dawn.",
            "You should add bread to your routine. It improves everything. Scientific fact.",
            "That's a lot of steps. I do three things. Flap. Think. Eat. In that order. Always.",
        ]
    ),
    
    "sleep": DuckQuestion(
        id="sleep",
        text="Do you sleep well? I'm asking because I noticed you visit at strange hours. Sometimes.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Sleep is important. Even for ducks. I tuck my head under my wing. It's cozy.",
            "I understand. The pond is quiet at night. You're welcome here. Any hour.",
            "I sleep with one eye open. Literally. Ducks do that. Google it.",
            "Bad sleep is... difficult. I float in my sleep. It's soothing. You should try floating.",
        ]
    ),
    
    "comfort_food": DuckQuestion(
        id="comfort_food",
        text="What do you eat when you're sad? I eat bread. But I also eat bread when I'm happy. And neutral.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Comfort food is important. Mine is bread. Yours is valid too. Probably.",
            "That sounds like it works. My comfort food is the same as my regular food. Efficient.",
            "I'll remember that. In case you're ever sad here. I can't cook. But I can listen.",
        ]
    ),
    
    "rainy_day": DuckQuestion(
        id="rainy_day",
        text="What do you do on a rainy day? I swim. Same as every day. But wetter.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Rain days are the best days. The pond gets fuller. Free water. My favorite price.",
            "That sounds cozy. My rainy day is the same as my sunny day. But with more water falling on me.",
            "I love rain. It's like the sky is feeding the pond. Nobody asked it to. It just does.",
        ]
    ),
    
    "weekend": DuckQuestion(
        id="weekend",
        text="What does a typical weekend look like for you? Ducks don't have weekends. Every day is the same. It's either a blessing or a curse.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds either relaxing or exhausting. I can't tell which from your tone.",
            "Weekends are a human invention. I respect the concept. All float, no work.",
            "I hope your weekends include visiting me. No pressure. Some pressure.",
        ]
    ),
    
    "guilty_pleasure": DuckQuestion(
        id="guilty_pleasure",
        text="What's your guilty pleasure? Mine is stale bread. Don't tell anyone. It's better than fresh. I've said too much.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I won't judge. I eat soggy bread off the pond surface. We all have our things.",
            "That's between us. The fish don't need to know. They gossip.",
            "Guilty pleasures are just pleasures with shame attached. Remove the shame. Keep the pleasure.",
        ]
    ),
    
    # ========== RELATIONSHIP ==========
    "why_come_back": DuckQuestion(
        id="why_come_back",
        text="Why do you keep coming back? Genuine question. I'm a duck. There must be better options.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's... nicer than I expected. I'm not sure how to react. *shuffles feathers*",
            "I see. Well. You're welcome here. Always. That's not something I say lightly.",
            "I keep expecting you to stop. You don't. I don't know what to do with that. But I like it.",
            "Most people leave after the novelty wears off. You didn't. Noted. Filed. Appreciated.",
        ]
    ),
    
    "me_honest": DuckQuestion(
        id="me_honest",
        text="What do you honestly think of me? Good, bad, I can take it. I'm a duck. We're resilient.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I... thank you. That means something. Don't tell anyone I said that.",
            "I appreciate your honesty. I feel similarly. About you. There. I said it.",
            "That's... a lot. I'm going to float away and process that now.",
            "I didn't expect that. I prepared for worse. You're full of surprises.",
        ]
    ),
    
    "first_impression": DuckQuestion(
        id="first_impression",
        text="What was your first impression of me? The real one. Not the polished version.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's fair. My first impression of you was 'has bread potential'. You exceeded expectations.",
            "I looked better from a distance. We all do. Even ducks.",
            "Interesting. My first impression of you was 'another human'. I was wrong. You're different. Marginally.",
        ]
    ),
    
    "change_about_me": DuckQuestion(
        id="change_about_me",
        text="If you could change one thing about me, what would it be? I'm not going to change it. But I'm curious.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I'll consider it. Then disregard it. But I'll have considered it. That's something.",
            "That's fair criticism. I'll float on it. Literally and figuratively.",
            "I was expecting 'be less sarcastic'. Everyone says that. Yours was more creative.",
            "Bold of you to suggest improvements to a duck. I respect the audacity.",
        ]
    ),
    
    "miss_me": DuckQuestion(
        id="miss_me",
        text="Do you miss me? When you're not here? I'm asking for data purposes. Not emotional ones.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I don't miss you. I just notice when you're not here. There's a difference. Probably.",
            "That's... nice. The pond misses you too. I'm speaking for the pond. Not myself.",
            "I'm going to pretend I didn't ask that. And I'm going to pretend your answer didn't matter. It didn't.",
            "Good. I mean. Adequate. I mean. *turns away and stares at water*",
        ]
    ),
    
    "teach_me": DuckQuestion(
        id="teach_me",
        text="If you could teach me one thing, what would it be? Keep in mind I'm a duck. Limitations apply.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's a big ask for a duck. But I'll try. No promises. Zero promises.",
            "I was hoping you'd say 'how to get more bread'. Yours is more interesting though.",
            "I can teach you floating. That's my counter-offer. Take it or leave it.",
        ]
    ),
    
    "future": DuckQuestion(
        id="future",
        text="Where do you think this goes? Us, I mean. The duck-human dynamic. Long-term.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's optimistic. I like it. Don't tell anyone I said that.",
            "I hadn't thought that far ahead. I plan in bread intervals. But your vision is nice.",
            "I'll be here. At the pond. If that helps with planning.",
            "That's the nicest thing anyone has said about our cross-species friendship.",
        ]
    ),
    
    # ========== SILLY ==========
    "superpower_vegetable": DuckQuestion(
        id="superpower_vegetable",
        text="If vegetables had superpowers, which vegetable would be the most dangerous? This is important.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I agree. That vegetable is not to be trusted.",
            "Interesting choice. I was thinking carrots. They see in the dark. Suspicious.",
            "The correct answer is celery. Negative calories. What is it hiding?",
            "I'm going to worry about that now. Thank you for the new anxiety.",
        ]
    ),
    
    "moon_cheese": DuckQuestion(
        id="moon_cheese",
        text="Do you think the moon is made of cheese? I'm named Cheese. This could be personal.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "A reasonable answer. The moon remains mysterious.",
            "I like that answer. We should discuss more celestial dairy products sometime.",
            "If it IS cheese, then I'm named after the moon. That's dignified.",
            "The moon is either cheese or not cheese. Either way, I'm important.",
        ]
    ),
    
    "fight_question": DuckQuestion(
        id="fight_question",
        text="Would you rather fight one horse-sized duck or a hundred duck-sized horses? Choose carefully.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "A horse-sized duck would be terrifying. I'd be terrifying. Noted for future growth plans.",
            "A hundred duck-sized horses. Tiny hooves. Everywhere. That's a nightmare I didn't need.",
            "The correct answer is neither. You walk away. Like I do. From most problems.",
            "I'm offended on behalf of all ducks. But also intrigued.",
        ]
    ),
    
    "secret_talent": DuckQuestion(
        id="secret_talent",
        text="What's your most useless talent? Mine is floating perfectly still for hours. It's also my most useful talent.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That IS useless. I love it. Useless talents are the purest form of personality.",
            "I bet that comes up less than you'd think. Or more. Life is unpredictable.",
            "We should combine our useless talents. Mine is floating. Yours is that. Together, we're slightly more useless.",
        ]
    ),
    
    "alien_message": DuckQuestion(
        id="alien_message",
        text="If aliens landed and you had to explain humanity in one sentence, what would you say?",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I'd just quack. Let them figure it out. Natural selection.",
            "That's generous. I'd say 'they make bread but feed it to ducks'. The aliens would be confused.",
            "Accurate. Devastating. I'd hire you as humanity's spokesperson.",
        ]
    ),
    
    "rename_earth": DuckQuestion(
        id="rename_earth",
        text="If you could rename the planet, what would you call it? I'd call it 'The Big Pond'. For obvious reasons.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Better than 'Earth'. Earth is just dirt. Your name has personality.",
            "I still prefer 'The Big Pond' but yours is a close second.",
            "The committee of ducks will review your submission. The committee is me. Submission denied. Mine was better.",
        ]
    ),
    
    "duck_council": DuckQuestion(
        id="duck_council",
        text="If there was a secret council of ducks running the world, would you be surprised? You shouldn't be.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I'm not saying there IS a council. I'm not saying there isn't. *stares meaningfully*",
            "Your reaction has been noted. By the council. That doesn't exist.",
            "We've been floating in ponds for millions of years. You think we're just... sitting there? Think again.",
        ]
    ),
    
    # ========== AFTER ABSENCE ==========
    "where_were_you": DuckQuestion(
        id="where_were_you",
        text="Where were you? You were gone a while. I'm not upset. Just... curious. Very curious.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.AFTER_ABSENCE,
        follow_ups=[
            "I see. Life happened. It does that. The pond was quiet.",
            "That's fair. You have a life out there. I just float here. Waiting.",
            "I counted the days. I won't tell you how many. It's between me and the pond.",
            "The fish asked about you. They don't talk. But they looked at your spot.",
        ]
    ),
    
    "missed_you": DuckQuestion(
        id="missed_you",
        text="I won't say I missed you. But the pond felt emptier. Atmospheric pressure, probably.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.AFTER_ABSENCE,
        follow_ups=[
            "I'm glad you're back. That's a statement of fact. Not emotion.",
            "The pond noticed. I noticed the pond noticing. Chain of observation.",
            "Don't leave that long again. Please. I mean. Whatever. The bread got lonely.",
        ]
    ),
    
    "life_update": DuckQuestion(
        id="life_update",
        text="What have you been up to? Give me the summary. I've been floating. Your turn.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.AFTER_ABSENCE,
        follow_ups=[
            "That's... a lot. I floated. My update is shorter. Yours wins.",
            "Sounds like you were busy. Being human is apparently very time-consuming.",
            "I'll process all of that. Slowly. While floating. My processing speed is one ripple per thought.",
        ]
    ),
    
    # ========== LATE NIGHT ==========
    "cant_sleep": DuckQuestion(
        id="cant_sleep",
        text="It's late. You're here instead of sleeping. Can't sleep? Or don't want to?",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "The night is strange. Things feel different. I understand coming here.",
            "I'm here too. Obviously. If you need company at this hour, I'm... available. For talking.",
            "Night visits are different. Quieter. More honest. I like them. Don't tell day-you.",
            "The pond is different at night. Calmer. Like the world finally shut up.",
        ]
    ),
    
    "night_thoughts": DuckQuestion(
        id="night_thoughts",
        text="What do you think about at night? When it's quiet? I think about the water. And bread. And you. Sometimes.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "That's heavy. Night thoughts always are. The darkness makes everything feel bigger.",
            "I think about similar things. In duck terms. Same weight. Fewer words.",
            "Thank you for sharing your night thoughts. They're safe here. In the dark. By the water.",
        ]
    ),
    
    "darkness": DuckQuestion(
        id="darkness",
        text="Are you okay with the dark? Some people aren't. I'm not judging. The dark is very dark.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "The dark and I have an arrangement. It stays dark. I stay floating. We coexist.",
            "I can see in the dark. Kind of. Duck eyes work differently. I see... shapes. And bread.",
            "If the dark bothers you, come closer. I'll be here. The pond reflects starlight. It helps.",
        ]
    ),
    
    "insomnia": DuckQuestion(
        id="insomnia",
        text="Do you have trouble sleeping a lot? Or is tonight special? Either way, you're here. With a duck.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "Insomnia is just your brain refusing to stop. My brain stops at sunset. Different wiring.",
            "You could try floating. It's very soothing. You'd get wet though. Drawbacks.",
            "I'm glad you come here when you can't sleep. Better than staring at a ceiling. Marginally.",
        ]
    ),
    
    # ========== MILESTONE ==========
    "milestone_reflection": DuckQuestion(
        id="milestone_reflection",
        text="We've been doing this a while now. You and me. The duck and the human. How do you think it's going?",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.MILESTONE,
        follow_ups=[
            "That's... the best review I've ever received. Not that I've received many. Or any.",
            "I think so too. In my duck way. Which is less articulate but equally sincere.",
            "We've come a long way from 'why are you talking to a duck'. Growth.",
            "I'd rate our friendship 4 out of 5. One point deducted because you're not a duck.",
        ]
    ),
    
    "favorite_memory_us": DuckQuestion(
        id="favorite_memory_us",
        text="What's your favorite memory of us? The duck-human chronicles. Best episode.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.MILESTONE,
        follow_ups=[
            "I remember that too. I remember everything. It's a duck thing. Or a me thing.",
            "That's a good one. Mine is... similar. Adjacent. In the same emotional pond.",
            "I'm adding that to the list. The 'nice things' list. It's getting longer. Because of you.",
        ]
    ),
}


class QuestionManager:
    """
    Manages the duck's questions to the player.
    
    Tracks what's been asked, respects cooldowns, and generates
    contextually appropriate questions based on relationship level,
    time of day, and conversation history.
    """
    
    def __init__(self):
        # Track asked questions
        self.asked_questions: Dict[str, Dict] = {}  # question_id -> {asked_at, answer, etc.}
        
        # Cooldowns
        self.category_cooldowns: Dict[str, str] = {}  # category -> last_asked timestamp
        self.general_cooldown_until: Optional[str] = None
        
        # Queue of questions to ask
        self.question_queue: List[str] = []
        
        # Questions per session limit
        self.questions_this_session: int = 0
        self.max_questions_per_session: int = 3
        
        # Statistics
        self.total_questions_asked: int = 0
        self.total_answers_received: int = 0
    
    def get_next_question(self, 
                          relationship_level: str,
                          time_of_day: str,
                          hours_since_last_visit: float = 0,
                          player_model = None,
                          force: bool = False) -> Optional[DuckQuestion]:
        """
        Get the next appropriate question to ask.
        
        Args:
            relationship_level: stranger/acquaintance/friend/best_friend/bonded
            time_of_day: morning/afternoon/evening/night
            hours_since_last_visit: Hours since player was last here
            player_model: PlayerModel for context
            force: Skip cooldowns and limits
        
        Returns:
            DuckQuestion if appropriate, None otherwise
        """
        if not force:
            # Check session limit
            if self.questions_this_session >= self.max_questions_per_session:
                return None
            
            # Check general cooldown
            if self.general_cooldown_until:
                try:
                    cooldown_end = datetime.fromisoformat(self.general_cooldown_until)
                    if datetime.now() < cooldown_end:
                        return None
                except (ValueError, TypeError):
                    pass
        
        # Determine appropriate timing
        timing_filter = [QuestionTiming.ANY_TIME]
        
        if relationship_level == "stranger":
            timing_filter.append(QuestionTiming.FIRST_MEETING)
        elif relationship_level == "acquaintance":
            timing_filter.append(QuestionTiming.EARLY_RELATIONSHIP)
        elif relationship_level in ["friend", "best_friend", "bonded"]:
            timing_filter.append(QuestionTiming.ESTABLISHED)
        if relationship_level in ["best_friend", "bonded"]:
            timing_filter.append(QuestionTiming.CLOSE_FRIENDS)
        
        if hours_since_last_visit > 48:
            timing_filter.append(QuestionTiming.AFTER_ABSENCE)
        
        if time_of_day == "night":
            timing_filter.append(QuestionTiming.LATE_NIGHT)
        
        # Find eligible questions
        eligible = []
        for qid, question in DUCK_QUESTIONS.items():
            # Skip if already asked
            if qid in self.asked_questions:
                continue
            
            # Check timing
            if question.timing not in timing_filter:
                continue
            
            # Check category cooldown
            cat_str = question.category.value
            if cat_str in self.category_cooldowns:
                try:
                    last_asked = datetime.fromisoformat(self.category_cooldowns[cat_str])
                    if (datetime.now() - last_asked).total_seconds() < 3600:  # 1 hour cooldown
                        continue
                except (ValueError, TypeError):
                    pass
            
            eligible.append(question)
        
        if not eligible:
            return None
        
        # Prioritize certain categories based on context
        weighted = []
        for q in eligible:
            weight = 1.0
            
            # Boost introduction questions early
            if q.category == QuestionCategory.INTRODUCTION and self.total_questions_asked < 5:
                weight = 3.0
            
            # Boost feeling questions if player visits late at night
            if q.category == QuestionCategory.FEELINGS and time_of_day == "night":
                weight = 2.0
            
            # Boost after-absence questions
            if q.timing == QuestionTiming.AFTER_ABSENCE and hours_since_last_visit > 48:
                weight = 3.0
            
            # Slight randomness
            weight *= random.uniform(0.8, 1.2)
            
            weighted.append((weight, q))
        
        weighted.sort(key=lambda x: x[0], reverse=True)
        return weighted[0][1]
    
    def record_question_asked(self, question_id: str):
        """Record that a question was asked."""
        if question_id not in DUCK_QUESTIONS:
            return
        
        question = DUCK_QUESTIONS[question_id]
        now = datetime.now()
        
        self.asked_questions[question_id] = {
            "asked_at": now.isoformat(),
            "category": question.category.value,
            "answer": None,
            "answered_at": None
        }
        
        # Update cooldowns
        self.category_cooldowns[question.category.value] = now.isoformat()
        self.general_cooldown_until = (now + timedelta(minutes=5)).isoformat()
        
        # Update counters
        self.questions_this_session += 1
        self.total_questions_asked += 1
    
    def record_answer(self, question_id: str, answer: str) -> Optional[str]:
        """
        Record the player's answer to a question.
        
        Returns the follow-up response if available.
        """
        if question_id not in self.asked_questions:
            return None
        
        if question_id not in DUCK_QUESTIONS:
            return None
        
        question = DUCK_QUESTIONS[question_id]
        now = datetime.now()
        
        self.asked_questions[question_id]["answer"] = answer
        self.asked_questions[question_id]["answered_at"] = now.isoformat()
        
        self.total_answers_received += 1
        
        # Return a follow-up if available
        if question.follow_ups:
            return random.choice(question.follow_ups)
        return None
    
    def get_callback(self, player_model = None) -> Optional[Tuple[str, str]]:
        """
        Get a callback to a previous answer.
        
        Returns (callback_text, original_answer) if available.
        """
        # Find answered questions with callback text
        callbacks = []
        for qid, data in self.asked_questions.items():
            if not data.get("answer"):
                continue
            
            if qid not in DUCK_QUESTIONS:
                continue
            
            question = DUCK_QUESTIONS[qid]
            if not question.callback_text:
                continue
            
            callbacks.append((question, data))
        
        if not callbacks:
            return None
        
        # Pick a random one
        question, data = random.choice(callbacks)
        
        # Format the callback
        callback = question.callback_text
        if "{value}" in callback:
            callback = callback.replace("{value}", data["answer"])
        
        return callback, data["answer"]
    
    def reset_session(self):
        """Reset session-specific counters."""
        self.questions_this_session = 0
    
    def get_unanswered_questions(self) -> List[str]:
        """Get list of questions asked but not answered."""
        unanswered = []
        for qid, data in self.asked_questions.items():
            if data.get("answer") is None:
                unanswered.append(qid)
        return unanswered
    
    def get_extracted_facts(self) -> Dict[str, str]:
        """Get facts extracted from answered questions."""
        facts = {}
        for qid, data in self.asked_questions.items():
            if not data.get("answer"):
                continue
            
            if qid in DUCK_QUESTIONS:
                question = DUCK_QUESTIONS[qid]
                if question.extracts_fact:
                    facts[question.extracts_fact] = data["answer"]
        
        return facts
    
    def to_dict(self) -> Dict:
        """Serialize for persistence."""
        return {
            "asked_questions": self.asked_questions,
            "category_cooldowns": self.category_cooldowns,
            "general_cooldown_until": self.general_cooldown_until,
            "question_queue": self.question_queue,
            "total_questions_asked": self.total_questions_asked,
            "total_answers_received": self.total_answers_received
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "QuestionManager":
        """Deserialize from persistence."""
        manager = cls()
        manager.asked_questions = data.get("asked_questions", {})
        manager.category_cooldowns = data.get("category_cooldowns", {})
        manager.general_cooldown_until = data.get("general_cooldown_until")
        manager.question_queue = data.get("question_queue", [])
        manager.total_questions_asked = data.get("total_questions_asked", 0)
        manager.total_answers_received = data.get("total_answers_received", 0)
        return manager


def generate_callback_dialogue(question_id: str, answer: str) -> str:
    """Generate dialogue that callbacks to a previous answer."""
    if question_id not in DUCK_QUESTIONS:
        return f"You told me something once. I remember. '{answer[:50]}...'"
    
    question = DUCK_QUESTIONS[question_id]
    
    if question.callback_text:
        return question.callback_text.replace("{value}", answer)
    
    # Generic callbacks based on category
    category_callbacks = {
        QuestionCategory.PREFERENCES: [
            f"You mentioned you liked {answer}. I remember these things.",
            f"Ah, {answer}. You told me about that. I was listening.",
            f"I thought about {answer} the other day. Because you mentioned it. Not because I care. Much.",
            f"You said you liked {answer}. I filed that under 'important'. Don't read into it.",
            f"Remember when you told me about {answer}? I do. I remember everything.",
        ],
        QuestionCategory.PERSONAL: [
            f"You told me about {answer}. I think about that sometimes.",
            f"I remember when you mentioned {answer}. Details stick with me.",
            f"You shared about {answer} once. It stuck. Like bread to a wet beak.",
            f"That thing you said about {answer}. I still think about it. While floating.",
        ],
        QuestionCategory.FEELINGS: [
            f"You shared how you felt once. About {answer}. I haven't forgotten.",
            f"I recall you opening up about {answer}. That meant something.",
            f"You told me about {answer}. I listened. I'm still listening.",
            f"That time you talked about {answer}. I heard every word. Ducks have good hearing.",
        ],
        QuestionCategory.PHILOSOPHICAL: [
            f"You said something once. About {answer}. It was... deep. For a non-duck.",
            f"I've been floating and thinking about what you said. About {answer}. Still processing.",
            f"Remember when you philosophized about {answer}? I do. The pond remembers too.",
        ],
        QuestionCategory.OPINIONS: [
            f"You had opinions about {answer}. Strong ones. I respected that.",
            f"Your thoughts on {answer} still come to mind. When I'm floating. Which is always.",
            f"I remember your take on {answer}. Bold. For a human.",
        ],
        QuestionCategory.HYPOTHETICAL: [
            f"You said you'd choose {answer}. In that hypothetical. I still think about your reasoning.",
            f"Remember that hypothetical? About {answer}? I've revised my answer since then.",
        ],
        QuestionCategory.MEMORIES: [
            f"You shared a memory about {answer}. It was... honest. I keep it safe.",
            f"That memory you told me. About {answer}. I think about it when the pond is quiet.",
            f"I remember you talking about {answer}. Thank you for trusting a duck with that.",
        ],
        QuestionCategory.HABITS: [
            f"You mentioned {answer}. Part of your routine. I noticed.",
            f"I think about your habit with {answer}. Humans have so many habits. Ducks just float.",
        ],
        QuestionCategory.RELATIONSHIP: [
            f"You said something about us once. About {answer}. I... I remember. That's all.",
            f"When you talked about {answer}. The thing about us. I still think about that.",
        ],
        QuestionCategory.SILLY: [
            f"Remember when you said {answer}? That was absurd. I loved it.",
            f"You said {answer}. During that silly question. I still quack about it.",
        ],
    }
    
    callbacks = category_callbacks.get(question.category, [
        f"You told me: '{answer[:40]}...' I remember.",
    ])
    
    return random.choice(callbacks)
