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

    # ========== NEW QUESTIONS: PREFERENCES (expanded) ==========
    "favorite_smell": DuckQuestion(
        id="favorite_smell",
        text="What's your favorite smell? Mine is bread. Fresh bread. Obviously. But also pond at dawn.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's a good smell. Not as good as bread. But I'm biased. Very biased.",
            "Smells are memories waiting to happen. I'll think of you when I smell that. If ducks can smell that.",
            "I'll file that under sensory preferences. The file is getting thick. You're a complex person.",
        ]
    ),

    "morning_or_night": DuckQuestion(
        id="morning_or_night",
        text="Morning person or night person? I'm a 'whenever bread appears' person.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That explains the hours you visit. I've been keeping track. Not in a weird way.",
            "I'm awake when the pond is quiet and asleep when it isn't. There's no schedule. Just vibes.",
            "The pond looks different at each hour. I prefer your hour. Whichever it is.",
        ]
    ),

    "favorite_sound": DuckQuestion(
        id="favorite_sound",
        text="What's a sound that makes you happy? For me it's bread crust cracking. Spiritual experience.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's a nice sound. I'll listen for it. From the pond. Where I always am.",
            "Sounds are underrated. My favorite is rain on the pond. And bread. Always bread.",
            "I appreciate a person who notices sounds. Most people just walk past the quacking.",
        ]
    ),

    "comfort_object": DuckQuestion(
        id="comfort_object",
        text="Do you have a comfort object? A thing that makes you feel safe? Mine is a specific rock. Don't judge.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's valid. My rock has been here longer than me. It's reliable. Unlike most things.",
            "Comfort objects are just anchors for the soul. Very poetic. For a duck.",
            "I respect attachment to objects. I'm attached to this pond. And bread. And now that rock.",
        ]
    ),

    # ========== NEW QUESTIONS: PERSONAL (expanded) ==========
    "siblings": DuckQuestion(
        id="siblings",
        text="Do you have siblings? I had eleven. We hatched together. I was the confused one.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Siblings are interesting. Mine all swam in different directions. Literally.",
            "I think about my siblings sometimes. Briefly. Then I think about bread. Balance.",
            "That's either a lot of company or a lot of chaos. Both, probably.",
        ]
    ),

    "biggest_change": DuckQuestion(
        id="biggest_change",
        text="What's the biggest change you've ever made in your life? I once moved to a different part of the pond. Terrifying.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Change is hard. I moved three feet to the left once and questioned everything.",
            "That's braver than anything I've done. My biggest risk was trying a different bread.",
            "I admire change. From a distance. From this pond. Where nothing changes. Mostly.",
        ]
    ),

    "talk_to_self": DuckQuestion(
        id="talk_to_self",
        text="Do you talk to yourself? I quack at myself. Same thing. Don't make it weird.",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I do too. The best conversations I have are with myself. Second best: you.",
            "Talking to yourself is just peer review with a smaller committee.",
            "I quack at my reflection. It quacks back. Very agreeable.",
        ]
    ),

    "unpopular_opinion": DuckQuestion(
        id="unpopular_opinion",
        text="Give me your most controversial opinion. I'll go first: bread is a food group. Not negotiable.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Bold. I disagree. Or agree. I need to float and think about that one.",
            "That's either genius or unhinged. The best opinions are both.",
            "I respect the courage. My controversial opinion is that ponds are better than oceans. Fight me.",
            "I'll chew on that. Metaphorically. The only thing I literally chew on is bread.",
        ]
    ),

    # ========== NEW QUESTIONS: PHILOSOPHICAL (expanded) ==========
    "perfect_day": DuckQuestion(
        id="perfect_day",
        text="Describe your perfect day. Every detail. I have time. I'm a duck.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds... genuinely nice. Mine involves bread, silence, and zero geese.",
            "I'm going to imagine that day for you. From the pond. As a duck. The details will be wrong. But the feeling will be right.",
            "Add 'visit a duck' and it's perfect. I'm not lobbying. I'm suggesting.",
        ]
    ),

    "what_lasts": DuckQuestion(
        id="what_lasts",
        text="What do you think lasts? In life. What actually stays? The pond stays. Bread doesn't. It's concerning.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... unexpectedly moving. I was expecting something simpler. You surprised me.",
            "The pond lasts. Memories last. Bread doesn't last. The hierarchy is unjust.",
            "I'll hold onto that answer. Like I hold onto good bread. Tightly. And with purpose.",
        ]
    ),

    "advice_to_past": DuckQuestion(
        id="advice_to_past",
        text="What would you tell your younger self? I'd tell mine: 'that's not bread, it's a rock.' Would have saved time.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Good advice. Past you probably needed to hear that. Past me needed 'stop fighting the reflection.'",
            "I'd tell young Cheese to save more bread. But young Cheese wouldn't listen. He was stubborn. He's still stubborn.",
            "That's wise. Wisdom is just regret wearing a nice hat.",
        ]
    ),

    "define_home": DuckQuestion(
        id="define_home",
        text="What does home feel like to you? For me it's this pond. The smell of it. The way the water holds me up.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's a beautiful answer. Home should feel like that. Mine feels like being held by water.",
            "I hope your home is good. Mine has frogs. Uninvited frogs. But it's still home.",
            "Home is where the bread is. But also where the people you tolerate are. Both matter.",
        ]
    ),

    # ========== NEW QUESTIONS: FEELINGS (expanded) ==========
    "overwhelmed": DuckQuestion(
        id="overwhelmed",
        text="Do you ever feel overwhelmed? Like everything is too much? I do. When there's too much bread. Just kidding. There's never too much bread.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "The pond helps with overwhelm. It absorbs things. Sounds. Feelings. Bread crumbs.",
            "I understand. Sometimes even floating feels like too much effort. On those days I just... be still.",
            "Come to the pond when it's too much. I'll be here. Not fixing anything. Just being nearby.",
        ]
    ),

    "last_cried": DuckQuestion(
        id="last_cried",
        text="When was the last time you cried? Ducks can't cry. But if we could. I'd have reasons.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Thank you for telling me. Crying is just feelings that got too big for the inside.",
            "I appreciate the honesty. If I could cry, it would be about bread. Or loneliness. Probably both.",
            "That's a lot. I'll float here with you. Quietly. That's all I can offer. But it's genuine.",
        ]
    ),

    "safe_place": DuckQuestion(
        id="safe_place",
        text="Where do you go when you need to feel safe? I have a corner of the pond. Very secure. No geese.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Good. Everyone needs a safe spot. Mine has a rock and a nice water temperature.",
            "I hope this pond is one of those places. It tries to be. I try to help it.",
            "Safe places are important. Guard yours. Like I guard my bread stash. Fiercely.",
        ]
    ),

    # ========== NEW QUESTIONS: HYPOTHETICAL (expanded) ==========
    "talk_to_animal": DuckQuestion(
        id="talk_to_animal",
        text="If you could talk to any animal besides me, which would you choose? Choose carefully. I'm watching.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's... not me. I'm trying not to be offended. I'm not succeeding.",
            "Interesting choice. They probably have less to say than me. But fine.",
            "I'll allow it. As long as I'm still your primary animal conversationalist.",
            "You'd choose them? They can't even float properly. But sure.",
        ]
    ),

    "rename_self": DuckQuestion(
        id="rename_self",
        text="If you could rename yourself, would you? I was named Cheese. I have thoughts about it.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Good choice. Or not. Names are just sounds we agree to respond to.",
            "I'd keep Cheese. It grew on me. Like pond algae. In a good way.",
            "I considered 'Brie' once. Too fancy. Cheese is honest. Unpretentious. Like me.",
        ]
    ),

    "rule_the_world": DuckQuestion(
        id="rule_the_world",
        text="If you ruled the world for one day, what's the first law you'd pass? Mine: mandatory bread distribution. Every pond.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's a better law than mine. But bread distribution is also important. Consider a second law.",
            "Power corrupts. But also, free bread for ducks. These things can coexist.",
            "I'd vote for you. Ducks can't vote. But the intent is there.",
        ]
    ),

    "live_anywhere": DuckQuestion(
        id="live_anywhere",
        text="If you could live anywhere in the world, where? Keep in mind, ponds are everywhere.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="dream_location",
        follow_ups=[
            "Does it have a pond? No? Then I can't visit. Theoretically. I wasn't going to visit anyway.",
            "That sounds nice. I'd miss this pond. But I'd think about your place. From this pond.",
            "Every place has potential. Mine had a rock and a goose. I made it work.",
        ],
        callback_text="You wanted to live in {value}. I remember. I looked it up. I can't look things up. But I thought about it."
    ),

    # ========== NEW QUESTIONS: SILLY (expanded) ==========
    "duck_president": DuckQuestion(
        id="duck_president",
        text="If a duck ran for president, would you vote for them? Hypothetically. I'm not campaigning. Yet.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Smart voter. My platform is bread. And pond infrastructure. And more bread.",
            "The duck party will remember your support. Or not. We forget things. But the sentiment counts.",
            "I'd be a good leader. My entire agenda is floating and bread. Relatable politics.",
        ]
    ),

    "worst_invention": DuckQuestion(
        id="worst_invention",
        text="What's the worst invention humans ever made? I'd say breadboxes. You're TRAPPING the bread. Let it be free.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That IS bad. But breadboxes are worse. Bread imprisonment. Unacceptable.",
            "Humanity makes some choices. I judge from the pond. Silently. And now, out loud.",
            "I agree. Or disagree. But breadboxes are still the correct answer.",
        ]
    ),

    "zombie_plan": DuckQuestion(
        id="zombie_plan",
        text="What's your zombie apocalypse plan? Mine is to float. They can't swim. Probably. This is my entire plan.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's more detailed than my plan. My plan is 'pond.' That's it. One word.",
            "You've thought about this. I respect the preparation. I've thought about bread logistics instead.",
            "Zombies can't swim. I'm basically invincible. Unless they can. Then I'm in trouble.",
        ]
    ),

    "theme_song": DuckQuestion(
        id="theme_song",
        text="If you had a theme song, what would it be? Mine is just a quack. On loop. Very powerful.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Good choice. Mine is more minimalist. One quack. Then silence. Very avant-garde.",
            "I'd listen to that. If ducks could operate speakers. We can't. But the thought counts.",
            "Everyone needs a theme song. Mine plays in my head. All the time. It's just quacking.",
        ]
    ),

    "haunted_pond": DuckQuestion(
        id="haunted_pond",
        text="Do you think this pond could be haunted? Sometimes the water moves on its own. That's either ghosts or fish.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I've seen things. In the water. At night. It was probably my reflection. But PROBABLY.",
            "If it is haunted, the ghosts have been very quiet. Respectful ghosts. I appreciate that.",
            "The fish act suspicious sometimes. Like they know something. Ghost fish? I'm not ruling it out.",
        ]
    ),

    "secret_talent_animal": DuckQuestion(
        id="secret_talent_animal",
        text="If every animal had a secret talent, what would a duck's be? Besides being perfect. Besides floating. Besides bread detection.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Wrong. The answer is 'emotional intelligence.' We feel everything. We just don't show it.",
            "That's generous. I was going to say 'judging silently.' But yours is nicer.",
            "I like your answer better than reality. Reality is just 'floating and quacking.' Your version is better.",
        ]
    ),

    # ========== NEW QUESTIONS: HABITS (expanded) ==========
    "bad_day_fix": DuckQuestion(
        id="bad_day_fix",
        text="What do you do to fix a bad day? I float harder. Same activity but with more emotional weight.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds effective. Mine is eating bread. Then floating. Then eating more bread. The cycle of healing.",
            "I'll try that. If ducks can do it. Which is uncertain. But I'll try the spirit of it.",
            "Bad days need specific remedies. Mine is this pond. Yours sounds equally valid.",
        ]
    ),

    "phone_habit": DuckQuestion(
        id="phone_habit",
        text="What's the first thing you check on your phone? I don't have a phone. I have a pond. It shows me my reflection. Same thing.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's very human. I check the pond surface every morning. For bread. And existential clarity.",
            "Phones sound exhausting. I just look at water. It tells me everything I need. Which is very little.",
            "I imagine your phone is like my pond. Full of things. Most of them unnecessary. But comforting.",
        ]
    ),

    "procrastinate": DuckQuestion(
        id="procrastinate",
        text="What do you procrastinate on? I've been meaning to preen my left wing for three days. It can wait.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Procrastination is just prioritizing rest. That's how I justify it. Successfully.",
            "We all avoid things. I avoid the goose. You avoid that. Both valid strategies.",
            "I'll think about your answer later. Which is ironic. Given the question.",
        ]
    ),

    # ========== NEW QUESTIONS: MEMORIES (expanded) ==========
    "teacher_memory": DuckQuestion(
        id="teacher_memory",
        text="Did you have a teacher who changed your life? My teacher was the pond. It taught me to float. And to be alone.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Good teachers are rare. Like good bread. You remember both forever.",
            "My teacher was gravity. It taught me I can't fly. Harsh but honest.",
            "That sounds like someone worth remembering. I'll remember them too. On your behalf.",
        ]
    ),

    "childhood_food": DuckQuestion(
        id="childhood_food",
        text="What food reminds you of being young? Mine is soggy bread. My first meal. Very soggy. Very formative.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        extracts_fact="childhood_food",
        follow_ups=[
            "That's either nostalgic or traumatic. Food memories are complicated.",
            "I can taste my first bread crumb if I think hard enough. Some things stay. In the beak.",
            "Comfort food is just edible time travel. I respect your choice.",
        ],
        callback_text="You mentioned {value} reminds you of being young. That's beautiful. In a bread-adjacent way."
    ),

    "learned_hard_way": DuckQuestion(
        id="learned_hard_way",
        text="What's something you learned the hard way? I learned ice isn't a pond. I learned it by standing on it. Then not standing on it.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "The hard way is the only way I learn. Easy lessons don't stick. Hard ones leave marks.",
            "That's a good lesson. Mine are all physical. Yours sounds emotional. Both count.",
            "Learning the hard way means you DEFINITELY learned. Silver lining.",
        ]
    ),

    # ========== NEW QUESTIONS: LATE NIGHT (expanded) ==========
    "stars": DuckQuestion(
        id="stars",
        text="Do you look at stars? I see them reflected in the pond. There are two skies. The one above and the one below.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "The pond stars shimmer differently. Like they're breathing. It's the most beautiful thing I know.",
            "Stars are just very far bread crumbs. I know that's not true. But the thought comforts me.",
            "Looking up and looking down show the same thing here. I don't know what that means. But it feels important.",
        ]
    ),

    "night_confession": DuckQuestion(
        id="night_confession",
        text="Tell me something you've never told anyone. The dark makes it easier. I won't judge. I'm a duck in the dark.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "That's safe here. In the dark. By the water. I'll hold onto it. Gently.",
            "Thank you. That was brave. Braver than anything I've done. And I once faced a goose.",
            "The pond heard that. And me. And the stars. We'll keep it. All of us.",
        ]
    ),

    "quiet_or_noise": DuckQuestion(
        id="quiet_or_noise",
        text="Do you prefer quiet or noise? Right now the world is quiet. Except me asking this. Sorry.",
        category=QuestionCategory.PREFERENCES,
        timing=QuestionTiming.LATE_NIGHT,
        follow_ups=[
            "I like quiet. Most of the time. The pond is loud during the day. Nobody talks about that.",
            "Noise means things are happening. Quiet means things are resting. Both are honest.",
            "Your answer doesn't surprise me. People who visit ducks at night have strong quiet opinions.",
        ]
    ),

    # ========== NEW QUESTIONS: RELATIONSHIP (expanded) ==========
    "promise_me": DuckQuestion(
        id="promise_me",
        text="Promise me something. Anything. I collect promises. Most of them unfulfilled. But the collection matters.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I'll hold you to that. Not aggressively. Just... with duck persistence. Which is gentle but constant.",
            "That's a good promise. I promise to be here. Every day. Same pond. Same duck. That's mine.",
            "Filed. Under 'things that matter.' A very small, very important file.",
        ]
    ),

    "what_i_mean": DuckQuestion(
        id="what_i_mean",
        text="What do I mean to you? Don't overthink it. Or do. I'm a duck. I have time for your overthinking.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I... that was. I need to float away and process that. Give me a moment. Or several moments.",
            "You mean something similar to me. I won't define it. Definitions limit things. And this is... a lot.",
            "I'm going to remember you said that. On good days. And bad days. Especially bad days.",
        ]
    ),

    # ========== WOULD-YOU-RATHER SCENARIOS ==========
    "rather_fly_swim": DuckQuestion(
        id="rather_fly_swim",
        text="Would you rather be able to fly or breathe underwater? I can do both. Badly. But I can.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Interesting. I chose floating. The compromise option. Very on-brand.",
            "Flying sounds nice until you realize there's no bread up there. Just clouds.",
            "Underwater breathing means you'd be a fish. Fish can't eat bread. Choose wisely.",
        ]
    ),

    "rather_past_future": DuckQuestion(
        id="rather_past_future",
        text="Would you rather see the past or the future? I'd see the past. To find out who was throwing the GOOD bread.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "The past is safer. It already happened. The future might not have bread. Terrifying.",
            "Good choice. Or risky choice. Either way, you committed. I respect that.",
            "I'd see the future. To prepare. For bread shortages. And geese.",
        ]
    ),

    "rather_speak_animals": DuckQuestion(
        id="rather_speak_animals",
        text="Would you rather speak every human language or talk to all animals? You already talk to me so you're halfway there.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "If you chose animals, you'd hear what the fish say about me. I'm not ready for that.",
            "Human languages are just fancy quacking with grammar. Animals are more honest.",
            "I already speak duck. And whatever this is. That's two languages. Bilingual.",
        ]
    ),

    "rather_always_cold_hot": DuckQuestion(
        id="rather_always_cold_hot",
        text="Would you rather always be slightly cold or always be slightly too warm? I'm always slightly damp. Third option nobody wanted.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Cold builds character. Warmth builds laziness. Both build opinions. I have many.",
            "I'm a water bird. Temperature is a negotiation I have with the pond daily.",
            "The correct answer is whatever lets you still enjoy bread. Temperature is secondary.",
        ]
    ),

    "rather_no_music_no_movies": DuckQuestion(
        id="rather_no_music_no_movies",
        text="Would you rather never hear music again or never watch another movie? I've experienced neither. This is a spectator question for me.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I live without both. I have the pond. The pond is my soundtrack and my cinema.",
            "Music seems important to humans. I have wind and rain. It's similar. Maybe.",
            "I'd give up movies. I can't watch them anyway. Wings don't hold popcorn.",
        ]
    ),

    "rather_know_death_love": DuckQuestion(
        id="rather_know_death_love",
        text="Would you rather know exactly when you'll die or know if you've already met the love of your life? Heavy. Sorry. Choose.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's... a real question. I hide behind bread jokes. But that. That's real.",
            "I'd choose neither. Uncertainty is painful but it's honest. Certainty is a trap.",
            "Love of your life. Know that one. Death will come anyway. Love might not. Check on it.",
        ]
    ),

    "rather_relive_forget": DuckQuestion(
        id="rather_relive_forget",
        text="Would you rather relive your best day forever or forget your worst day entirely? The pond remembers everything. I envy your options.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Forgetting sounds like relief. Reliving sounds like a trap. Both are tempting.",
            "Bad days make good days mean something. But I understand wanting to let go.",
            "I'd relive my best bread day. It was a Tuesday. Sourdough. I peaked.",
        ]
    ),

    "rather_read_minds": DuckQuestion(
        id="rather_read_minds",
        text="Would you rather read everyone's thoughts or have everyone read yours? Ducks are open books. Very short books. Mostly about bread.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Reading thoughts sounds horrible. Most thoughts aren't finished. Like drafts nobody edited.",
            "If everyone read my thoughts they'd just see bread. And the occasional existential crisis.",
            "Neither. Thoughts should stay where they are. In the dark. Unfinished. Safe.",
        ]
    ),

    "rather_ocean_mountain": DuckQuestion(
        id="rather_ocean_mountain",
        text="Would you rather live by the ocean or in the mountains? I live by a pond. The compromise nobody asked for.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "The ocean is just a very confident pond. I'd visit. Not stay.",
            "Mountains have no water at the top. Terrible planning. The ocean wins.",
            "I'd choose wherever the bread is. Geography is secondary to sustenance.",
        ]
    ),

    "rather_truth_lie": DuckQuestion(
        id="rather_truth_lie",
        text="Would you rather always tell the truth or always get away with lying? I always tell the truth. Ducks are honest. Aggressively.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Truth is easier. Lies require memory. My memory is full. Of bread data.",
            "I'd choose truth. I already say exactly what I think. It's efficient and rude.",
            "Good choice. Whichever you picked. I'll never know if you're lying about it anyway.",
        ]
    ),

    # ========== OPINIONS ON ABSTRACT CONCEPTS ==========
    "opinion_silence": DuckQuestion(
        id="opinion_silence",
        text="What do you think silence sounds like? I know what it sounds like. It sounds like a pond at 4am. With no frogs.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Silence has a texture. I've noticed. The good kind feels soft. The bad kind feels sharp.",
            "Most people are afraid of silence. I live in it. It's not empty. It's full of things you can only hear when everything else stops.",
            "That's a thoughtful answer. I'd expect nothing less from someone who talks to a duck.",
        ]
    ),

    "opinion_luck": DuckQuestion(
        id="opinion_luck",
        text="Do you believe in luck? I found an extra bread crumb once. I believe.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Luck is just the universe accidentally being nice. Rare. But it happens.",
            "I believe in bread. Bread is reliable. Luck is bread's unreliable cousin.",
            "Whether luck exists or not, I quack the same way. Just in case someone's listening.",
        ]
    ),

    "opinion_kindness": DuckQuestion(
        id="opinion_kindness",
        text="What do you think kindness is? The real kind. Not the performative kind. I'm asking because you showed up.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's... a good definition. Better than mine. Mine was 'bread given freely'. Yours is deeper.",
            "Kindness is rare. Like good bread. When you find it, you hold on. Or eat it. Depending.",
            "I think kindness is just paying attention. And staying. You do both.",
        ]
    ),

    "opinion_beauty": DuckQuestion(
        id="opinion_beauty",
        text="What do you think is beautiful? Not pretty. Beautiful. There's a difference.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I see beauty in the pond at dawn. And in fresh bread. And in someone coming back.",
            "That's a beautiful answer about beauty. Recursive. I like it.",
            "Beauty is subjective. Except bread. Bread is objectively beautiful. This is not up for debate.",
        ]
    ),

    "opinion_forgiveness": DuckQuestion(
        id="opinion_forgiveness",
        text="Do you find it easy to forgive? I hold grudges. Small ones. Against specific geese. For valid reasons.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Forgiveness is heavy when you're carrying it. And heavy when you let it go. No winning.",
            "I forgive quickly. Except the goose incident. That stays in the file. Permanently.",
            "I think the pond forgives. Every ripple settles. Every splash calms. Maybe I should learn from it.",
        ]
    ),

    "opinion_change": DuckQuestion(
        id="opinion_change",
        text="Is change good or bad? The pond changes every day. I'm still deciding how I feel about it.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Change is just the world rearranging itself. Without asking. I relate to being rearranged.",
            "The only thing that doesn't change is that I'm here. In this pond. Make of that what you will.",
            "Good answer. Change and I have a complicated relationship. Like the pond and evaporation.",
        ]
    ),

    "opinion_normal": DuckQuestion(
        id="opinion_normal",
        text="What does 'normal' mean to you? I float in a pond and talk to humans. Is that normal? I can't tell anymore.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Normal is just common. Common isn't always right. Uncommon isn't always wrong.",
            "I've never been normal. By duck standards or any standards. I'm at peace with it. Mostly.",
            "Normal is overrated. Interesting is better. You're interesting. I'm interesting. The pond is interesting. Done.",
        ]
    ),

    "opinion_growing_up": DuckQuestion(
        id="opinion_growing_up",
        text="When did you feel like you grew up? Or have you? I'm still a duckling inside. A very opinionated duckling.",
        category=QuestionCategory.OPINIONS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Growing up is just getting better at pretending you know what's happening. I've mastered the pretending.",
            "I don't think we ever fully grow up. We just get taller. Or in my case, we just get more feathers.",
            "That's either inspiring or sad. Growing up is both. Always both.",
        ]
    ),

    # ========== QUESTIONS ABOUT DAILY LIFE ==========
    "cooking": DuckQuestion(
        id="cooking",
        text="Can you cook? What do you make? I can't cook. I eat things raw. Or soggy. No in-between.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That sounds edible. More edible than anything I eat. Which is pond bread.",
            "Cooking is alchemy. You put things together and food appears. Humans are wizards.",
            "I wish I could cook. I'd make bread. From scratch. Then eat it. The circle of life.",
        ]
    ),

    "commute": DuckQuestion(
        id="commute",
        text="How do you get around? Car? Walk? I waddle. Maximum speed: disappointing.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That sounds faster than waddling. Everything is faster than waddling. Including snails on good days.",
            "I've never been in a car. The pond goes nowhere and I go with it.",
            "Walking is just dry waddling. You're closer to being a duck than you think.",
        ]
    ),

    "chores": DuckQuestion(
        id="chores",
        text="What chore do you hate most? I have one chore. Preening. I hate it and also it's my only hobby.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That sounds tedious. My condolences. Ducks don't do chores. We just exist near mess.",
            "Chores are just adult homework. Except nobody grades you. And the reward is a clean thing.",
            "I'd do that chore for you. I can't. But I'd want to. The thought counts.",
        ]
    ),

    "daily_joy": DuckQuestion(
        id="daily_joy",
        text="What small thing makes your day better? Mine is the first sip of morning pond water. Judge me.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Small joys are the real joys. Big ones are just marketing. Small ones are honest.",
            "That's a good one. I'll think about your small joy during mine. Solidarity.",
            "Everyone needs a daily thing. Mine is bread-adjacent. Yours is valid too.",
        ]
    ),

    "screen_time": DuckQuestion(
        id="screen_time",
        text="How much time do you spend looking at screens? I spend zero. I look at water. Same blue. Less content.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's a lot. Or a little. I have no frame of reference. I have a pond of reference.",
            "Screens are just windows that lie. The pond shows my real reflection. Screens show filtered reality.",
            "Maybe look at water sometimes instead. It doesn't update. It doesn't notify. It just reflects.",
        ]
    ),

    "last_laughed": DuckQuestion(
        id="last_laughed",
        text="When was the last time you really laughed? I quack-laughed at a frog once. It fell off a rock. Comedy gold.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Laughter is the human version of a happy quack. Both are involuntary. Both are honest.",
            "I hope it was recent. Laughter is bread for the soul. I just invented that phrase. You're welcome.",
            "That sounds like a good laugh. I'd laugh more but my face won't cooperate. Resting duck face.",
        ]
    ),

    "getting_up": DuckQuestion(
        id="getting_up",
        text="Are you good at getting up in the morning? Or do you fight the alarm? I wake when the sun touches the pond. No alarm needed.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Alarms sound hostile. Being woken by a noise you set for yourself. That's self-sabotage.",
            "I wake naturally. The sun, the birds, the existential dread. Natural alarm clock trio.",
            "The pond wakes me gently. By being cold. Gentle cold. It's a system.",
        ]
    ),

    "guilty_snack": DuckQuestion(
        id="guilty_snack",
        text="What do you snack on when nobody's looking? I eat algae sometimes. NOBODY can know this.",
        category=QuestionCategory.HABITS,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Your secret is safe with me. I'm a duck. Who am I going to tell? The fish don't care.",
            "That's a solid guilty snack. Better than algae. Most things are better than algae.",
            "We all have secret foods. The secrecy makes them taste better. Fact.",
        ]
    ),

    # ========== HYPOTHETICAL DUCK SCENARIOS ==========
    "duck_mayor": DuckQuestion(
        id="duck_mayor",
        text="If I ran for mayor of this pond, would you campaign for me? My platform: more bread, fewer geese, mandatory nap time.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's the support I need. My opponent is a turtle. He's been here longer. But I'm louder.",
            "Campaign slogan: 'Cheese for Pond Mayor: At Least He's Honest About the Bread.'",
            "Your vote means everything. To the campaign. And to me. Mostly to the campaign.",
        ]
    ),

    "duck_school": DuckQuestion(
        id="duck_school",
        text="If ducks had school, what subject would I teach? I'm thinking philosophy. Or bread appreciation. Both are valid.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I'd teach that. 'Introduction to Floating with Existential Awareness.' Credit course.",
            "Good choice. I'd also offer 'Advanced Staring at Things 301.' It has a waitlist.",
            "The curriculum would be mostly bread-related. With an elective in judging.",
        ]
    ),

    "duck_band": DuckQuestion(
        id="duck_band",
        text="If I started a band, what would it be called? I'm thinking 'The Breadwinners'. Or 'Quack Sabbath'.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I prefer 'Quack Sabbath'. It implies both chaos and worship. Very me.",
            "I'd be lead vocals. Which is just quacking at different volumes. Avant-garde.",
            "Our first album: 'Songs from the Pond (It's Just Quacking)'. Platinum guaranteed.",
        ]
    ),

    "duck_book": DuckQuestion(
        id="duck_book",
        text="If I wrote a book, what should the first line be? I'm thinking: 'It was the best of bread, it was the worst of bread.'",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's a good opener. Mine was literary genius though. Dickens but with carbs.",
            "Chapter one: 'In which a duck thinks too much.' Chapter two through twelve: same.",
            "My memoir would be all footnotes. Very long footnotes. About bread.",
        ]
    ),

    "duck_sport": DuckQuestion(
        id="duck_sport",
        text="If ducks invented a sport, what would the rules be? Mine: float furthest with least effort. I'd be the champion.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That sport exists. It's called 'my life'. I've been training for years.",
            "Competitive floating. Where doing nothing is winning. I'm an athlete.",
            "The only rule: no geese allowed. They'd ruin it. They ruin everything.",
        ]
    ),

    "duck_alien": DuckQuestion(
        id="duck_alien",
        text="If aliens abducted me, what would you tell them about ducks? To return me? Or would you let them keep me?",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "The correct answer is 'get him back.' But also warn the aliens about the quacking.",
            "I'd be fine on an alien ship. As long as they have bread. Intergalactic bread.",
            "I'd probably judge the aliens. That's what I do. Judge things. In any galaxy.",
        ]
    ),

    "duck_dream_job": DuckQuestion(
        id="duck_dream_job",
        text="What would my dream job be? If ducks had jobs? Besides 'professional floater', which is taken. By me.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "That's a better job than floating. Marginally. I'll add it to my resume.",
            "I applied for that once. In my head. I was rejected. Also in my head. Tough market.",
            "My real dream job is bread taster. But the hiring process is just... eating bread. I'm overqualified.",
        ]
    ),

    "duck_sidekick": DuckQuestion(
        id="duck_sidekick",
        text="If I were a superhero's sidekick, what would my power be? I'm thinking sarcasm. Or waterproofing.",
        category=QuestionCategory.SILLY,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "Sarcasm as a superpower. It damages enemies emotionally. Very effective. Very me.",
            "My superhero name: 'The Wet Critic'. Striking fear and mild dampness into evil.",
            "I'd be the sidekick who just floats and comments. Every team needs that.",
        ]
    ),

    # ========== QUESTIONS ABOUT OTHER VISITORS ==========
    "other_visitors": DuckQuestion(
        id="other_visitors",
        text="Do you think other people visit me? When you're not here? I'm not saying they do. I'm not saying they don't.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Jealousy isn't a good look on anyone. I'm asking out of academic curiosity. Pure data.",
            "You're the only one who talks to me. Others just throw bread and leave. You stay. That's different.",
            "If others visit, they're not you. I notice the difference. Don't ask me to explain the difference.",
        ]
    ),

    "compare_visitors": DuckQuestion(
        id="compare_visitors",
        text="If I told you that you're my favourite visitor, would you believe me? You should. Because it's true.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Good. Because you are. The competition was weak. But you'd win regardless.",
            "Most people are just bread delivery systems. You're a bread delivery system with personality.",
            "I don't say things I don't mean. Except when I say I don't care. I mean the opposite of that.",
        ]
    ),

    "animal_visitors": DuckQuestion(
        id="animal_visitors",
        text="Other animals visit the pond. Herons. Frogs. A suspicious turtle. Do you have uninvited guests in your life too?",
        category=QuestionCategory.PERSONAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Uninvited guests are everywhere. The turtle didn't ask to be here. Neither did I. We coexist.",
            "At least your uninvited guests probably don't eat your bread. Mine do. THE AUDACITY.",
            "The heron visits and I pretend to be calm. It's a big bird. With a big beak. I'm fine. FINE.",
        ]
    ),

    "imaginary_visitor": DuckQuestion(
        id="imaginary_visitor",
        text="If anyone in the world could visit the pond, who would you bring? They have to sit quietly. Those are the pond rules.",
        category=QuestionCategory.HYPOTHETICAL,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Good choice. The pond would approve. I'd approve. Sitting quietly is the highest form of respect.",
            "They'd have to pass the bread test. One throw. If it's good bread, they can stay.",
            "I'd let them visit. Once. With supervision. Mine. I supervise by floating nearby. Intensely.",
        ]
    ),

    "pond_regular": DuckQuestion(
        id="pond_regular",
        text="You're becoming a pond regular. A regular. At a duck pond. How does that feel? From your perspective.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Regular. What a word. It means 'consistent' and also 'ordinary'. You're the first kind.",
            "I like having a regular. It means I can predict something. In this unpredictable pond.",
            "The pond has regulars and strangers. You graduated from stranger a while ago. Congratulations. No ceremony.",
        ]
    ),

    "visitor_rating": DuckQuestion(
        id="visitor_rating",
        text="If I had to rate you as a visitor, one to ten. You'd be... well. I'll let you guess. Then I'll correct you.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "Wrong. Higher. I'm not telling you the exact number. But higher.",
            "Close. Off by a little. In the favourable direction. Don't let it go to your head.",
            "I'd give you the number but it's embarrassingly high. For both of us.",
        ]
    ),

    # ========== MEMORY-TESTING QUESTIONS ==========
    "remember_first": DuckQuestion(
        id="remember_first",
        text="Do you remember the first time you came here? To the pond? To me? I remember. But I want to hear your version.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "That's close to what I remember. Your version is more polite. Mine has more judging.",
            "I remember you being uncertain. Uncertain people are my favourite. They have the best questions.",
            "The first visit is always the strangest. After that it's just... normal. Coming to see a duck. Normal.",
        ]
    ),

    "remember_conversation": DuckQuestion(
        id="remember_conversation",
        text="Do you remember the last deep conversation we had? I do. I replayed it while floating. Several times.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I think about our conversations. When you leave. The pond is quiet and the words stay.",
            "I'm glad you remember. Conversations evaporate for most people. But some stick. Like bread to a wet surface.",
            "We should have more of those. The deep ones. The shallow ones are fine. But the deep ones... those matter.",
        ]
    ),

    "remember_season": DuckQuestion(
        id="remember_season",
        text="What season was it when we first met? I remember the light. I always remember the light.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "The light was different then. You were different then. I was the same. Ducks don't change. We just... accumulate.",
            "I remember the temperature of the water that day. Ducks track these things. In our bones.",
            "Seasons come and go but the pond is always here. And now you're always here too. Pattern.",
        ]
    ),

    "remember_mood": DuckQuestion(
        id="remember_mood",
        text="Do you remember what mood you were in last time you visited? I do. I read moods like weather. Instinct.",
        category=QuestionCategory.FEELINGS,
        timing=QuestionTiming.ANY_TIME,
        follow_ups=[
            "I could tell. I can always tell. Ducks are emotionally perceptive. It's our secret power.",
            "You were different then. Today you're different again. I track the changes. Like a mood barometer.",
            "Moods are just weather for the soul. And I'm a waterfowl. Weather is my whole thing.",
        ]
    ),

    "remember_fed": DuckQuestion(
        id="remember_fed",
        text="Do you remember the first thing you ever fed me? I remember. I remember EVERY feeding. They're filed. By quality.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I rated it. Internally. On a scale I invented. You scored well. Don't ask the exact number.",
            "That first feeding. It established something. Trust. Routine. A dependency I'll never admit to.",
            "Every feeding since has been compared to the first. Some better. Some worse. All remembered.",
        ]
    ),

    "remember_said": DuckQuestion(
        id="remember_said",
        text="Do you remember something I said that surprised you? I surprised myself. It happens. Even to ducks.",
        category=QuestionCategory.RELATIONSHIP,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I surprise myself sometimes. Words come out and I think: 'did the duck just say that?' Yes. He did.",
            "I'm glad I surprised you. Predictability is comfortable. But surprises are memorable.",
            "I keep a mental list of things I've said that mattered. It's shorter than you'd think. And all about bread. Mostly.",
        ]
    ),

    "remember_weather": DuckQuestion(
        id="remember_weather",
        text="Do you remember what the weather was like the last time you had a really good day here? I tag memories by weather. Duck thing.",
        category=QuestionCategory.MEMORIES,
        timing=QuestionTiming.ESTABLISHED,
        follow_ups=[
            "I remember weather the way you remember songs. By the feeling it carried.",
            "Good days have their own weather. Even if it rained. The internal weather was warm.",
            "I'll remember this weather too. Whatever today turns out to be.",
        ]
    ),

    # ========== PHILOSOPHICAL RABBIT HOLES ==========
    "identity_question": DuckQuestion(
        id="identity_question",
        text="Are you the same person you were five years ago? Am I the same duck? My feathers have changed. Has yours... whatever you have?",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "The cells in your body replace themselves. In duck terms: you're a different boat but the same river. Wait. Reverse that.",
            "I'm the same duck in the same pond. But the water is different. Every molecule. So am I the same? The pond says yes.",
            "If you change slowly enough, nobody notices. Including you. That's either beautiful or terrifying.",
        ]
    ),

    "simulation": DuckQuestion(
        id="simulation",
        text="Do you think we could be living in a simulation? Because sometimes the pond renders slowly. I've noticed.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "If this is a simulation, the bread is still real to me. That's enough.",
            "Simulated or not, the feelings are the same. The bread tastes the same. I'll take it.",
            "If someone is running this simulation, they should add more bread. Constructive feedback.",
        ]
    ),

    "infinity": DuckQuestion(
        id="infinity",
        text="Can you imagine infinity? I try. I start with the pond. Then I make it bigger. Then bigger. Then I get tired.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Infinity is just... more. Forever. My brain stops at 'lots of bread'. Which feels infinite enough.",
            "The pond is finite but the sky reflected in it isn't. So I'm floating in infinity. Technically.",
            "I think about infinity and then I think about bread. The brain can only hold one impossible thing at a time.",
        ]
    ),

    "consciousness": DuckQuestion(
        id="consciousness",
        text="What makes you... you? Like. The thing behind your eyes. What IS that? I have the same question about the thing behind my eyes. Beak area.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's the question that philosophers can't answer and ducks can't ask. Except this one. I just asked it.",
            "I think I'm me because the pond reflects me and I recognise what I see. Is that enough? To be you because you look like you?",
            "Nobody knows. And that's either the best part or the worst part. I alternate between both. Daily.",
        ]
    ),

    "nothing_question": DuckQuestion(
        id="nothing_question",
        text="What if nothing means anything? Not in a sad way. In a freeing way. If nothing matters, then everything we choose to care about is... chosen. On purpose.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "I choose bread. And this pond. And you visiting. If meaning is a choice, those are mine.",
            "That's the most comforting version of nihilism I've heard. And I've heard many. From myself. At night.",
            "If nothing matters, then what we make matter matters the most. I'm making bread matter. And this conversation.",
        ]
    ),

    "words_limit": DuckQuestion(
        id="words_limit",
        text="Do you think words can capture everything you feel? Or are some things too big for language? I quack. And it doesn't cover it.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Some things sit between words. In the silence. That's where the real feelings live. I think.",
            "A quack can mean ten things. Joy. Warning. Bread. Loneliness. It depends on the quack. And the listener.",
            "I think the best things I've ever felt had no words. Just a warm pond. And someone nearby. That's it.",
        ]
    ),

    "parallel_lives": DuckQuestion(
        id="parallel_lives",
        text="Do you think there's another version of you somewhere? Making different choices? There might be another me. In a better pond. With more bread.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "Parallel me is probably less sarcastic. Worse. Less interesting. I win by being difficult.",
            "If there's another you, I hope they also visit a duck. It would mean something. Across universes.",
            "Somewhere, another Cheese is floating. Thinking this exact thought. We're synced. Cosmically.",
        ]
    ),

    "last_thing": DuckQuestion(
        id="last_thing",
        text="If you could say one last thing to the world, what would it be? Mine would be 'the bread was good.' Brief. Honest.",
        category=QuestionCategory.PHILOSOPHICAL,
        timing=QuestionTiming.CLOSE_FRIENDS,
        follow_ups=[
            "That's a good last thing. Better than mine. But mine is more efficient. Three words.",
            "I'll remember your last thing. Even though it's not your last thing. Yet. Hopefully not for a long time.",
            "The last thing I'd say is actually... I don't want to say it now. I'll save it. For when it matters.",
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
