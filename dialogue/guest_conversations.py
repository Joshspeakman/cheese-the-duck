"""
Guest Conversations - Dynamic multi-turn conversations between visitors and Cheese.
Each conversation is a back-and-forth exchange that reveals character and builds relationships.
"""
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ConversationExchange:
    """A single back-and-forth exchange."""
    guest_line: str
    cheese_response: str
    mood_effect: int = 0
    friendship_bonus: float = 0.0


@dataclass
class GuestConversation:
    """A themed conversation between a guest and Cheese."""
    id: str
    title: str
    guest_personality: str
    min_friendship: str  # "stranger", "acquaintance", "friend", "close_friend", "best_friend"
    exchanges: List[ConversationExchange] = field(default_factory=list)
    topic_tags: List[str] = field(default_factory=list)


# Friendship level ordering for comparisons
FRIENDSHIP_LEVELS = ["stranger", "acquaintance", "friend", "close_friend", "best_friend"]


def _friendship_met(required: str, current: str) -> bool:
    """Check if the current friendship level meets the minimum requirement."""
    try:
        return FRIENDSHIP_LEVELS.index(current) >= FRIENDSHIP_LEVELS.index(required)
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# GUEST CONVERSATIONS — organised by visitor personality
# ---------------------------------------------------------------------------

GUEST_CONVERSATIONS: Dict[str, List[GuestConversation]] = {

    # ===================================================================
    #  ADVENTUROUS
    # ===================================================================
    "adventurous": [
        GuestConversation(
            id="adv_mountain_tale",
            title="The Mountain",
            guest_personality="adventurous",
            min_friendship="stranger",
            topic_tags=["adventure", "nature", "philosophy"],
            exchanges=[
                ConversationExchange(
                    guest_line="Have you ever climbed a mountain?",
                    cheese_response="I've climbed this rock. It was sufficient.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="No but like, a REAL mountain. Snow on top. Wind in your feathers.",
                    cheese_response="Wind in my feathers happens when I walk briskly. Same concept. Smaller scale.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The view from the top changes you. You see everything differently.",
                    cheese_response="I see everything from pond level. It's mostly ankles. I'm at peace with this.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Don't you ever want MORE though?",
                    cheese_response="I have bread. I have water. I have a rock. More would be greedy.",
                    mood_effect=3,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You're impossible. But I kind of respect it.",
                    cheese_response="Respect is acceptable. Bread is better. But respect will do.",
                    mood_effect=2,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="adv_ocean_crossing",
            title="Across the Ocean",
            guest_personality="adventurous",
            min_friendship="acquaintance",
            topic_tags=["adventure", "ocean", "travel"],
            exchanges=[
                ConversationExchange(
                    guest_line="I once flew across the entire ocean. Non-stop.",
                    cheese_response="I once walked to the other side of the pond. I needed a nap afterward.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The water below was endless. Just blue in every direction.",
                    cheese_response="That sounds deeply stressful. My pond has edges. Edges are comforting.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="There was a storm halfway through. Lightning everywhere.",
                    cheese_response="Lightning. Near water. And you did this VOLUNTARILY.",
                    mood_effect=1,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="When I landed I kissed the ground. It was the best dirt I ever tasted.",
                    cheese_response="Interesting. I also eat things off the ground. We have that in common.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You should try it someday. The ocean, I mean.",
                    cheese_response="I'll put it on my list. Right after 'sit here' and before 'continue sitting here.'",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
            ],
        ),
        GuestConversation(
            id="adv_dare_challenge",
            title="The Dare",
            guest_personality="adventurous",
            min_friendship="friend",
            topic_tags=["games", "challenge", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="I dare you to do something you've never done before. Right now.",
                    cheese_response="I'm going to blink with my left eye before my right. Exhilarating.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="That doesn't count! Something BOLD.",
                    cheese_response="I'll face slightly north instead of slightly south. My heart is racing.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Cheese, you're the least adventurous duck I've ever met.",
                    cheese_response="Thank you. I've been working on that. It takes dedication to be this still.",
                    mood_effect=2,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Okay fine. I dare you to say something NICE.",
                    cheese_response="Your feathers are... not the worst I've seen. *long pause* Was that nice enough.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="adv_lost_in_forest",
            title="Lost in the Forest",
            guest_personality="adventurous",
            min_friendship="acquaintance",
            topic_tags=["adventure", "nature", "stories"],
            exchanges=[
                ConversationExchange(
                    guest_line="I got lost in a forest once. Three days. No food.",
                    cheese_response="No food for three days. That's not an adventure, that's a tragedy.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I survived on berries and stream water. It was amazing.",
                    cheese_response="Amazing. The word you want is 'preventable.'",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I found my way out by following the stars.",
                    cheese_response="I find my way to bread by following the bread smell. Both valid navigation.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="When I finally saw civilization again, I almost cried.",
                    cheese_response="Civilization means bakeries. I would also cry. *understands deeply*",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Next time I get lost, you should come with me.",
                    cheese_response="I will be here. At the pond. Not lost. You're welcome to join ME.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
            ],
        ),
        GuestConversation(
            id="adv_meaning_of_freedom",
            title="What Freedom Means",
            guest_personality="adventurous",
            min_friendship="close_friend",
            topic_tags=["philosophy", "freedom", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="Don't you ever feel trapped? Just sitting here every day?",
                    cheese_response="Trapped implies I want to leave. I don't. The pond chose me. I chose back.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But freedom is about going wherever you want.",
                    cheese_response="I want to be here. So I am here. That IS freedom. With better snacks.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I need the open sky. The unknown. The rush.",
                    cheese_response="I need bread and moderate temperatures. We are built differently.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Maybe. But I think deep down you understand the call of the wild.",
                    cheese_response="Deep down I understand the call of carbohydrates. Close enough.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I'm glad we're friends, Cheese. Even if you won't fly with me.",
                    cheese_response="I'm glad too. Someone has to stay behind and guard the good bread.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="adv_treasure_map",
            title="The Treasure Map",
            guest_personality="adventurous",
            min_friendship="friend",
            topic_tags=["adventure", "treasure", "games"],
            exchanges=[
                ConversationExchange(
                    guest_line="I found a treasure map! Want to help me decode it?",
                    cheese_response="Does the treasure involve bread. If not, I have concerns about the definition of treasure.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="It could be gold, jewels, ancient artifacts!",
                    cheese_response="None of those are bread. Your priorities are fascinating.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Think of the glory! The discovery! Being the FIRST to find it!",
                    cheese_response="I was the first to find this specific patch of mud. No one celebrates that.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You're impossible. I'm going anyway. Wish me luck.",
                    cheese_response="Luck. Also, if you find any bread-related treasure, you know where I am.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="adv_late_night_stars",
            title="Under the Stars",
            guest_personality="adventurous",
            min_friendship="close_friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="It's late. Can't sleep. Do you ever wonder if we're just... passing through?",
                    cheese_response="Passing through where. I've been at this pond for years. I'm not passing. I've arrived.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Through life. Through time. Like, what's the POINT of all the adventures?",
                    cheese_response="You're asking a duck about existential dread at midnight. This is where your adventures led you.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Maybe the point is the connections we make. Like this one. Right now.",
                    cheese_response="*looks at stars* Connections are. Fine. The pond is quiet. You're here. That's. It's fine.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You know, for a duck who won't go anywhere, you're the best company.",
                    cheese_response="That's because I'm always here. Reliability is underrated. The stars agree. Probably.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="adv_bread_trail",
            title="Trail Bread",
            guest_personality="adventurous",
            min_friendship="acquaintance",
            topic_tags=["bread", "adventure", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="On the trail I eat hardtack. Bread that lasts MONTHS. Practically indestructible.",
                    cheese_response="Bread that lasts months. That's not bread. That's a building material with delusions.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="It's efficient! Lightweight, calorie-dense, keeps you going for days!",
                    cheese_response="Fresh bread is gone in seconds. Because it's WORTH eating immediately. Speed is a compliment.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You can't carry fresh bread up a mountain. It would get squished.",
                    cheese_response="Then don't go up the mountain. Stay near the bakery. Problem solved. You're welcome.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Your entire worldview is designed to keep you near bread, isn't it?",
                    cheese_response="It's a perfectly rational worldview. Bread is stationary. I am stationary. Harmony.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="adv_gossip_scholarly",
            title="About That Bookworm",
            guest_personality="adventurous",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="That scholarly duck was here yesterday. Lectured me about wind patterns for an HOUR.",
                    cheese_response="I got a lecture about atmospheric pressure last week. My eyes were open. I may have been asleep.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="How do you LISTEN to all that? I was ready to fly away after five minutes.",
                    cheese_response="I don't listen. I hear. There's a difference. One requires effort I'm unwilling to provide.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Nice duck though. Brought me a book about migration routes. Actually helpful.",
                    cheese_response="They brought me a book about pond ecology. I sat on it. Made an excellent cushion.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="We should all hang out together sometime. The three of us.",
                    cheese_response="You'd climb things. They'd explain things. I'd sit. Everyone in their role. Fine.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="adv_winter_survival",
            title="Winter Survival",
            guest_personality="adventurous",
            min_friendship="acquaintance",
            topic_tags=["seasonal", "winter", "survival"],
            exchanges=[
                ConversationExchange(
                    guest_line="Winter's coming. I once survived three days in a blizzard with just a tarp.",
                    cheese_response="Winter's coming. I plan to be cold. At the pond. As usual.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You need an emergency plan! Shelter, food storage, thermal insulation!",
                    cheese_response="My plan: fluff feathers. Eat bread. Wait. Spring arrives. Plan complete.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What if the pond freezes over?",
                    cheese_response="Then I stand on the pond instead of in it. Adaptation. Very adventurous of me.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You're the calmest creature alive. Nothing rattles you.",
                    cheese_response="The cold rattles me. Literally. My bill chatters. But I do it with dignity.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="adv_remember_the_storm",
            title="Remember That Storm",
            guest_personality="adventurous",
            min_friendship="close_friend",
            topic_tags=["memory", "friendship", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="Remember that big storm? When I showed up soaking wet and you just... made room on the rock?",
                    cheese_response="I remember. You dripped on my dry spot. I allowed it. That was significant.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="We sat there in silence for hours. Watching the lightning.",
                    cheese_response="Good silence. Not the awkward kind. The kind where nobody needs to say the thing.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That's when I knew we were real friends. Not just pond acquaintances.",
                    cheese_response="I knew when you didn't try to make conversation. Just sat. Quietly. CORRECTLY.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="Best storm ever.",
                    cheese_response="Second best. The one where bread blew in from the bakery down the road. That was the best.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  SCHOLARLY
    # ===================================================================
    "scholarly": [
        GuestConversation(
            id="sch_duck_philosophy",
            title="On Being a Duck",
            guest_personality="scholarly",
            min_friendship="stranger",
            topic_tags=["philosophy", "ducks", "identity"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been reading about the philosophy of identity. What makes you... you?",
                    cheese_response="Feathers. Bread preferences. A general sense of mild disapproval.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="No, I mean on a deeper level. Cogito ergo sum. I think therefore I am.",
                    cheese_response="I sit therefore I am. Less Latin. More practical.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="But what IS consciousness? How do you know you're really here?",
                    cheese_response="The bread is real. I eat the bread. The bread disappears. That's enough proof.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You've just described empiricism in the most duck way possible.",
                    cheese_response="I have described bread. You have described a word. I think I win.",
                    mood_effect=2,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You know, you might actually be a philosopher.",
                    cheese_response="I am a duck. Ducks and philosophers have one thing in common. We both sit by ponds.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_history_lesson",
            title="Duck History",
            guest_personality="scholarly",
            min_friendship="acquaintance",
            topic_tags=["history", "ducks", "knowledge"],
            exchanges=[
                ConversationExchange(
                    guest_line="Did you know ducks have been around for over 80 million years?",
                    cheese_response="I know. I feel every single one of those years. Especially on Mondays.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Ancient Egyptians kept ducks! You would have been revered.",
                    cheese_response="I would have been warm. That's the important part. Desert climate. Ideal.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="They even mummified some ducks. Preserved for eternity.",
                    cheese_response="Being wrapped in cloth forever. Sounds like a weighted blanket situation. I'm in.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You'd prefer being mummified to... living by a pond?",
                    cheese_response="I'd prefer being mummified WITH bread. Best of both worlds.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_weather_debate",
            title="Weather Theory",
            guest_personality="scholarly",
            min_friendship="friend",
            topic_tags=["weather", "science", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been studying meteorological patterns. Rain is actually quite complex.",
                    cheese_response="Rain is wet. It falls. Complexity resolved.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But the atmospheric pressure systems, the humidity gradients—",
                    cheese_response="Wet. Falls. Down. I've summarized your entire field of study.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You're oversimplifying a chaotic dynamical system!",
                    cheese_response="I'm a duck. I stand IN the rain. I don't need to UNDERSTAND the rain.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What if I told you I could predict the weather three days in advance?",
                    cheese_response="My left foot aches before rain. Zero technology required. Your move.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="...That's actually a valid barometric response.",
                    cheese_response="I know. Science just confirmed what my foot always knew. Peer-reviewed foot.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_book_recommendation",
            title="Required Reading",
            guest_personality="scholarly",
            min_friendship="acquaintance",
            topic_tags=["books", "knowledge", "culture"],
            exchanges=[
                ConversationExchange(
                    guest_line="I just finished a 700-page treatise on aquatic ecosystems. Fascinating.",
                    cheese_response="I live in one. Took me zero pages. Very efficient.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But the DEPTH of analysis. The interconnected food webs!",
                    cheese_response="I eat bread that people throw at me. That's my food web. Short web.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You should read more. Knowledge is power.",
                    cheese_response="Bread is also power. Caloric power. Which is actual, measurable energy.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I'll bring you a book next time. Something accessible.",
                    cheese_response="Make it waterproof. And breadproof. I have a condition.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_meaning_of_life",
            title="The Big Question",
            guest_personality="scholarly",
            min_friendship="close_friend",
            topic_tags=["philosophy", "meaning", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="Cheese, what do you think is the meaning of life?",
                    cheese_response="Bread.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="No, seriously. I've read every philosopher. None of them agree.",
                    cheese_response="That's because none of them were ducks. Ducks agree. It's bread.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="There has to be more to existence than... bread.",
                    cheese_response="Water. Sunshine. A pond with good drainage. But mostly bread.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What about love? Connection? Legacy?",
                    cheese_response="Those are just bread in different shapes. You're overcomplicating it.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You might be the wisest creature I've ever met. Or the simplest.",
                    cheese_response="Both. At the same time. It's a gift.",
                    mood_effect=4,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="sch_stars_lecture",
            title="Stargazing",
            guest_personality="scholarly",
            min_friendship="friend",
            topic_tags=["science", "stars", "night"],
            exchanges=[
                ConversationExchange(
                    guest_line="The light from those stars traveled millions of years to reach us.",
                    cheese_response="And I'm the one who showed up to see it. You're welcome, stars.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="We're made of star stuff, you know. Carbon, nitrogen, oxygen.",
                    cheese_response="I'm made of bread, mostly. And mild resentment.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="When a star dies, it scatters its elements across the universe.",
                    cheese_response="When bread goes stale, I still eat it. We all cope differently.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Don't you find it humbling? How small we are?",
                    cheese_response="I'm already very small. I don't need the universe to remind me.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="But that's what makes it beautiful. We're tiny but we NOTICE.",
                    cheese_response="I notice bread. The stars notice nothing. I think I'm ahead.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_3am_thoughts",
            title="3 AM Thoughts",
            guest_personality="scholarly",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="It's 3 AM and I can't stop thinking about entropy. Everything falls apart eventually.",
                    cheese_response="My feathers fall out. New ones grow. Entropy and I have an understanding.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But on a cosmic scale, the universe is winding down. Heat death. The big freeze.",
                    cheese_response="Big freeze. So the pond will freeze. I've dealt with that. Not impressed, universe.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Doesn't it terrify you? That all of this is temporary?",
                    cheese_response="Bread is temporary. I eat it and it's gone. I don't mourn bread. I eat more bread.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="So your answer to cosmic impermanence is... more bread?",
                    cheese_response="The universe is dying. The bread is here NOW. Seems obvious who to pay attention to.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That's either the dumbest or wisest thing I've ever heard at 3 AM.",
                    cheese_response="Both. Like most 3 AM things. Go to sleep. The entropy will still be there tomorrow.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="sch_bread_science",
            title="The Science of Bread",
            guest_personality="scholarly",
            min_friendship="acquaintance",
            topic_tags=["bread", "science", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="Bread is actually a remarkable feat of biochemistry. Yeast metabolizing sugars, producing CO2—",
                    cheese_response="You're describing bread's SOUL. Not its science. Show some respect.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The Maillard reaction creates over 600 flavor compounds during baking.",
                    cheese_response="Six hundred. *reverently* I knew bread was complex. I KNEW it.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Technically, bread is just a foam. A matrix of gluten filled with gas bubbles.",
                    cheese_response="You call it foam. I call it perfection. We are using different dictionaries.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Nutritionally, whole grain bread contains significant B vitamins and fiber—",
                    cheese_response="I don't need to know WHY bread is perfect. I experience it. Empirically. Daily.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You love bread more than any creature I've studied.",
                    cheese_response="Don't study it. Don't explain it. Just bring some next time. Applied science.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_gossip_mysterious",
            title="That Mysterious Visitor",
            guest_personality="scholarly",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="That mysterious duck keeps telling me about prophecies. I find it scientifically unfounded.",
                    cheese_response="They told me about one too. It involved bread. I'm choosing to believe that particular prophecy.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="They claim they've been to 'places beyond knowing.' That's not even a LOCATION.",
                    cheese_response="I've been to the far side of the pond. That's a location. They could learn from me.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I tried to ask them about their methodology and they just... disappeared into fog.",
                    cheese_response="Convenient. When I don't want to answer questions, I just stare. Less theatrical. More effective.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Maybe some things aren't meant to be understood scientifically.",
                    cheese_response="Did you just... admit that. Out loud. I'm going to remember this forever.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="sch_teach_quantum",
            title="Quantum Physics for Ducks",
            guest_personality="scholarly",
            min_friendship="acquaintance",
            topic_tags=["teaching", "science", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Let me explain quantum superposition. A particle can be in two states at once until observed.",
                    cheese_response="Like bread. It's both mine and not-mine until I eat it. Then it's definitely mine.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="That's... not quite... but actually there's a philosophical argument there—",
                    cheese_response="I know. I'm philosophically advanced. It surprised me too.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Schr\u00f6dinger's cat is the famous thought experiment. A cat in a box, both alive and dead.",
                    cheese_response="I don't like this. The cat should be let out of the box. This is not a fun experiment.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="It's THEORETICAL. No actual cat. It's about observation changing reality.",
                    cheese_response="Observation changes nothing. I observe bread. It stays bread. Reality is stable here.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You're a surprisingly tough student to teach.",
                    cheese_response="I'm not a tough student. You're a complicated teacher. Bread is simple. Be more like bread.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="sch_summer_solstice",
            title="Summer Solstice",
            guest_personality="scholarly",
            min_friendship="friend",
            topic_tags=["seasonal", "summer", "science"],
            exchanges=[
                ConversationExchange(
                    guest_line="Today is the summer solstice. The longest day. Maximum solar exposure.",
                    cheese_response="I know. I've been warm for an unreasonable amount of time. My pond is approaching soup temperature.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Ancient civilizations built monuments aligned to this exact day. Stonehenge, for instance.",
                    cheese_response="I aligned myself to this rock. Same energy. Smaller budget.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="After today, the days get shorter. We're already heading toward winter.",
                    cheese_response="We JUST got warm and you're already bringing up winter. You're the worst kind of scientist.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I'm just stating astronomical facts!",
                    cheese_response="State them at the pond's suggestion box. Which is that log. No one checks it.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  ARTISTIC
    # ===================================================================
    "artistic": [
        GuestConversation(
            id="art_pond_painting",
            title="Painting the Pond",
            guest_personality="artistic",
            min_friendship="stranger",
            topic_tags=["art", "nature", "beauty"],
            exchanges=[
                ConversationExchange(
                    guest_line="The way the light hits the pond right now... it's breathtaking.",
                    cheese_response="It's wet. The light makes it wet and also visible. Both true.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I want to paint this moment. The golden hour, the reflections...",
                    cheese_response="If you paint me, make sure you get the good side. All sides are the good side.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Art captures what words can't express.",
                    cheese_response="Words can express bread. Paintings of bread aren't edible. Words win.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You're so literal. Don't you see the beauty around you?",
                    cheese_response="I see mud. Reeds. Water. One frog. All beautiful. In a mud-and-frog way.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_music_debate",
            title="The Sound of Music",
            guest_personality="artistic",
            min_friendship="acquaintance",
            topic_tags=["music", "art", "culture"],
            exchanges=[
                ConversationExchange(
                    guest_line="Music is the purest form of emotional expression.",
                    cheese_response="Quacking is pretty pure. No instruments required. Very raw.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Have you ever been moved to tears by a melody?",
                    cheese_response="I was moved to tears by a strong wind once. Similar experience, probably.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I composed a song about this pond once. It was in B minor.",
                    cheese_response="The pond is in C level. Sea level. Geography joke. You're welcome.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Do you want to hear it?",
                    cheese_response="Will it involve bread references. If so, yes. If not, also yes. But with less enthusiasm.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="*sings a short, haunting melody about water and moonlight*",
                    cheese_response="*sits very still* That was. Fine. That was fine. Don't look at my eyes. They're just wet because pond.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="art_poetry_slam",
            title="Duck Poetry",
            guest_personality="artistic",
            min_friendship="friend",
            topic_tags=["poetry", "art", "words"],
            exchanges=[
                ConversationExchange(
                    guest_line="Write a poem with me. I'll start: 'The water gleams—'",
                    cheese_response="'The bread descends.' There. Poem complete. Very efficient.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="We need more lines! 'The water gleams, the reeds stand tall—'",
                    cheese_response="'The bread descends. I eat it all.' Rhyming AND narrative. Peak literature.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Okay that was actually pretty good. One more verse?",
                    cheese_response="'Dawn arrives with gentle light. Bread again. The world is right.' I should publish.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You're secretly creative. I KNEW it.",
                    cheese_response="I'm not creative. Bread is my muse. The muse is doing all the work.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="art_color_theory",
            title="Color Theory",
            guest_personality="artistic",
            min_friendship="acquaintance",
            topic_tags=["art", "colors", "beauty"],
            exchanges=[
                ConversationExchange(
                    guest_line="What's your favorite color? Mine changes with the seasons.",
                    cheese_response="Bread-colored. Golden brown. The color of purpose.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="That's just... that's just beige. You like beige.",
                    cheese_response="I like the color of BREAD. Beige wishes it was bread-colored.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Colors evoke emotions. Red is passion, blue is calm—",
                    cheese_response="Bread-colored is satisfaction. Mold-colored is betrayal. Simple system.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You see the entire world through bread, don't you.",
                    cheese_response="And the world is better for it. Bread-colored glasses. Patent pending.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_self_portrait",
            title="The Self-Portrait",
            guest_personality="artistic",
            min_friendship="close_friend",
            topic_tags=["art", "identity", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been painting self-portraits. Trying to capture my true self.",
                    cheese_response="My reflection is in the pond. It looks exactly like me but wetter. Perfect portrait.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But a portrait isn't just how you look. It's how you FEEL inside.",
                    cheese_response="Inside I feel like a duck with bread. Outside I look like a duck without bread. The duality.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="If I painted YOUR portrait, I'd paint you in soft morning light. Serene but sharp.",
                    cheese_response="*very still* You'd paint me. That's. That's a thing someone would do. For me.",
                    mood_effect=5,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="Of course I would. You're worth painting, Cheese.",
                    cheese_response="I'm going to go float for a bit. No reason. Pond-related reasons. *turns away*",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="art_sunset_critique",
            title="Sunset Reviews",
            guest_personality="artistic",
            min_friendship="friend",
            topic_tags=["nature", "art", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Rate this sunset. One to ten.",
                    cheese_response="Six. The orange is derivative. Seen it before. Yesterday, in fact.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="A SIX? Look at those purples! The gradient!",
                    cheese_response="The gradient is adequate. But there's no bread in it. Minus two points for that.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You can't subtract points for lack of bread in a SUNSET.",
                    cheese_response="I just did. Four. Final answer. The sun should try harder.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What would a ten-out-of-ten sunset look like to you?",
                    cheese_response="Same sunset. But someone brings me bread during it. Context matters.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_mortality_moonlight",
            title="Moonlight Thoughts",
            guest_personality="artistic",
            min_friendship="close_friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="The moonlight makes everything look like a painting that's about to fade.",
                    cheese_response="Things fade. Bread goes stale. The moon wanes. I remain. Not everything fades.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Do you ever think about legacy? What you'll leave behind?",
                    cheese_response="I'll leave behind this rock. With a very worn sitting spot. My life's work.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I want to create something that outlasts me. A painting. A song. Something ETERNAL.",
                    cheese_response="A good bread recipe is eternal. Someone baked the first sourdough thousands of years ago. We still eat it.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That's... actually beautiful. Bread as humanity's greatest collaboration.",
                    cheese_response="Every loaf connects to every other loaf. All the way back. *stares at moon* I think about this a lot.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
                ConversationExchange(
                    guest_line="Cheese, you're a poet and you don't even know it.",
                    cheese_response="I know it. I just don't acknowledge it. Acknowledgment ruins things.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_bread_as_art",
            title="Bread as Art",
            guest_personality="artistic",
            min_friendship="acquaintance",
            topic_tags=["bread", "art", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been thinking about bread as an art form. The scoring, the crust patterns—",
                    cheese_response="Finally. Someone who understands. Bread is SCULPTED. It has FORM. It has MEANING.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="The golden ratio appears in the spiral of a croissant. Mathematics and beauty, unified.",
                    cheese_response="I don't know math. But I know a croissant when I see one. And it's always beautiful.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Some might say bread is craft, not art. What do you think?",
                    cheese_response="Bread is bread. It transcends your categories. You can't put bread in a box. Unless it's a breadbox.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But is eating bread destroying art? Like burning a painting?",
                    cheese_response="Eating bread is the POINT of bread. Art that fulfills its purpose. The highest form.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="art_gossip_playful",
            title="That Playful One",
            guest_personality="artistic",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="That playful duck tried to get me to play tag. I was in the middle of sketching.",
                    cheese_response="They tried to get me to play hide and seek. I hid by not moving. Won immediately.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Do they ever just... sit still? For even a moment?",
                    cheese_response="No. I've watched. It's exhausting. They vibrate with unspent games.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="They gave me a nickname. 'Paintbrush.' I don't hate it.",
                    cheese_response="They tried to call me C-Bread. I shut it down. But. Secretly. It wasn't terrible.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I suppose every pond needs someone who makes you laugh.",
                    cheese_response="Agreed. I provide the disapproval. They provide the chaos. Ecosystem balance.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_autumn_palette",
            title="Autumn Colors",
            guest_personality="artistic",
            min_friendship="stranger",
            topic_tags=["seasonal", "autumn", "art"],
            exchanges=[
                ConversationExchange(
                    guest_line="Autumn is the most beautiful season. Look at those reds and golds.",
                    cheese_response="The leaves are dying. You find death beautiful. Noted.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="It's not death, it's transformation! The trees are letting go gracefully.",
                    cheese_response="I never let go. Of anything. Especially bread. I am the opposite of a tree.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The fallen leaves on the pond look like a mosaic. Natural art.",
                    cheese_response="Natural clutter. They clog up my swimming area. But. The orange ones are. Acceptable.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I want to paint you surrounded by autumn leaves. A masterpiece.",
                    cheese_response="Surrounded by leaves. Looking mildly inconvenienced. Yes. That captures my autumn perfectly.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="art_remember_first_visit",
            title="The First Sketch",
            guest_personality="artistic",
            min_friendship="close_friend",
            topic_tags=["memory", "friendship", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="I still have that first sketch I did of you. It's terrible. I love it.",
                    cheese_response="I remember. You kept staring at me. I thought you were judging. Turns out you were drawing.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You were so suspicious. You kept turning your back to me.",
                    cheese_response="I was giving you my GOOD side. I didn't say which side. All sides are good. But differently.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="The sketch has a note at the bottom. 'Grumpy duck. Interesting eyes. Will return.'",
                    cheese_response="You did return. Multiple times. I stopped turning away around the third visit.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Best decision I ever made. Coming back.",
                    cheese_response="Second best. The best decision was when you brought bread that one time. But. Yes. Coming back was also good.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  PLAYFUL
    # ===================================================================
    "playful": [
        GuestConversation(
            id="play_riddle_game",
            title="Riddle Time",
            guest_personality="playful",
            min_friendship="stranger",
            topic_tags=["games", "riddles", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="Riddle me this: What has feathers but can't fly?",
                    cheese_response="An insult. That's what that is.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Haha, no! A pillow! Get it?",
                    cheese_response="I got it. I wish I hadn't. My turn. What's warm, golden, and the meaning of life.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Um... the sun?",
                    cheese_response="Bread. The answer is always bread. Worst riddle-guesser I've ever met.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="That's not even a riddle! That's just... bread propaganda!",
                    cheese_response="All good riddles are bread propaganda. This is well known.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="play_hide_and_seek",
            title="Hide and Seek",
            guest_personality="playful",
            min_friendship="acquaintance",
            topic_tags=["games", "fun", "challenge"],
            exchanges=[
                ConversationExchange(
                    guest_line="Let's play hide and seek! I'll count, you hide!",
                    cheese_response="I'm in the pond. I will continue to be in the pond. Your turn to seek.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You didn't even TRY to hide!",
                    cheese_response="I went slightly to the left. It was a bold strategic move.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="That's... okay, MY turn to hide. Count to ten!",
                    cheese_response="One. Two. Ten. I see you behind that reed. That reed is thin.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You skipped eight numbers!",
                    cheese_response="I'm efficient. Also, I never stopped watching. Blinking is optional.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="play_would_you_rather",
            title="Would You Rather",
            guest_personality="playful",
            min_friendship="friend",
            topic_tags=["games", "philosophy", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="Would you rather fly or breathe underwater?",
                    cheese_response="I can already do both of those. Poorly. But technically.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Okay, would you rather have unlimited bread or one perfect day?",
                    cheese_response="Unlimited bread IS one perfect day. Every day. You just described my ideal life.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Would you rather lose your memory or never make new memories?",
                    cheese_response="... *stares at pond* That's dark. For a game. You went dark.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Sorry! Light one: would you rather be slightly bigger or slightly smaller?",
                    cheese_response="Slightly bigger. More surface area for bread absorption. This is basic science.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Everything comes back to bread with you.",
                    cheese_response="Everything comes FROM bread. I'm just acknowledging the source.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
            ],
        ),
        GuestConversation(
            id="play_impressions",
            title="Duck Impressions",
            guest_personality="playful",
            min_friendship="friend",
            topic_tags=["humor", "fun", "gossip"],
            exchanges=[
                ConversationExchange(
                    guest_line="Watch this! *puffs up feathers* 'I'm Cheese and I love bread.' How was that?",
                    cheese_response="Inaccurate. I didn't hear enough judgment in the delivery.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Okay okay. *deadpan* 'I'm sitting here. This is fine. Bread.'",
                    cheese_response="Better. But my silences are more loaded than that. Years of practice.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*stares blankly at nothing for ten seconds*",
                    cheese_response="NOW you're getting it. That's the stuff. Pure, unfiltered duck energy.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I think I pulled something trying to be that still.",
                    cheese_response="Stillness takes effort. Mine looks effortless. That's the trick.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
            ],
        ),
        GuestConversation(
            id="play_prank_war",
            title="The Prank War",
            guest_personality="playful",
            min_friendship="close_friend",
            topic_tags=["games", "pranks", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="I put a fake snake by your rock. Did it scare you?",
                    cheese_response="I saw it. I stared at it. It blinked first. Because it's rubber.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Aw man. You're unpranakble.",
                    cheese_response="I replaced your bread stash with slightly different bread. Three days ago. You didn't notice.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="WHAT. That's... diabolical. I thought that rye tasted different!",
                    cheese_response="The long game. Ducks are patient. PATIENT.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Okay, truce. TRUCE. You win. You're terrifying.",
                    cheese_response="Truce accepted. The bread has already been switched back. Two days ago.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="play_nickname_game",
            title="Nickname Brainstorm",
            guest_personality="playful",
            min_friendship="acquaintance",
            topic_tags=["names", "fun", "identity"],
            exchanges=[
                ConversationExchange(
                    guest_line="I'm going to give you a cool nickname. How about... THE CHEESINATOR.",
                    cheese_response="No.",
                    mood_effect=0,
                    friendship_bonus=0.05,
                ),
                ConversationExchange(
                    guest_line="Cheddar? Brie? Gouda? Keep it in the cheese family!",
                    cheese_response="My name is Cheese. Not a category. Cheese. Singular. Sufficient.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What about... C-Money?",
                    cheese_response="I don't have money. I have bread. Call me C-Bread and we'll negotiate.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="C-BREAD. I love it. C-Bread it is!",
                    cheese_response="I've already changed my mind. Cheese. Just Cheese. The negotiation is over.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
            ],
        ),
        GuestConversation(
            id="play_late_night_what_is_fun",
            title="What Even Is Fun",
            guest_personality="playful",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="Hey Cheese. Late night question. Why do we play? Like, what IS fun?",
                    cheese_response="Fun is when bad things aren't happening. I have fun most of the time. By that measure.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="No but REAL fun. Laughing so hard you can't breathe. Pure joy.",
                    cheese_response="I can't breathe when I eat bread too fast. Same thing. Different stimulus.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What if I just... stopped being playful? What if one day I don't feel like playing?",
                    cheese_response="Then you sit. At the pond. With me. Being not-playful is also a valid activity.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You'd let me just... sit? No pressure to be fun?",
                    cheese_response="I've never pressured you to be anything. That's the advantage of low expectations. Welcome anytime.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="play_bread_olympics",
            title="Bread Olympics",
            guest_personality="playful",
            min_friendship="acquaintance",
            topic_tags=["bread", "games", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="I invented a game. Bread skipping. Like stone skipping but with bread!",
                    cheese_response="You SKIP bread. Across water. Where I can't reach it. This is a CRIME not a game.",
                    mood_effect=0,
                    friendship_bonus=0.05,
                ),
                ConversationExchange(
                    guest_line="Relax! I only use stale bread. The good stuff is for eating.",
                    cheese_response="ALL bread is good stuff. Stale bread is experienced bread. It has CHARACTER.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What if the game was... who can eat bread the fastest?",
                    cheese_response="That's not a game. That's my morning routine. But. I accept the challenge.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Ready, set— hey you already started!",
                    cheese_response="*already finished* The game started when you said bread. Keep up.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="play_staring_contest",
            title="Staring Contest",
            guest_personality="playful",
            min_friendship="stranger",
            topic_tags=["competition", "challenge", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="Staring contest! Starting now! Don't blink!",
                    cheese_response="*stares* I haven't blinked in four minutes. This is just my face. You've made a tactical error.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="How are you doing that?! My eyes are BURNING!",
                    cheese_response="Ducks have a third eyelid. We moisturize while appearing to stare. Evolution chose violence.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*blinks* OKAY FINE you win! That's cheating though!",
                    cheese_response="It's not cheating. It's biological superiority. In this one specific meaningless area.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Rematch. But next time I pick the game.",
                    cheese_response="Pick a game where the winner sits still. I have a natural advantage in all stillness-based competitions.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="play_gossip_athletic",
            title="About the Athlete",
            guest_personality="playful",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="That athletic duck challenged me to a race. I made it twenty feet before I got distracted by a butterfly.",
                    cheese_response="Twenty feet. A personal best for someone with your attention span.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="They were SO serious about it. 'Proper form! Engage your core!' My core doesn't engage.",
                    cheese_response="My core has never been engaged. My core is happily single.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I think deep down they want to play, you know? But they call it 'training.'",
                    cheese_response="And I call sitting 'meditation.' We all rebrand our preferences.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="We should prank them. Put a whoopee cushion on the finish line.",
                    cheese_response="No. But also. Where would one find a whoopee cushion. Hypothetically.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  MYSTERIOUS
    # ===================================================================
    "mysterious": [
        GuestConversation(
            id="mys_late_night_truths",
            title="Midnight Revelations",
            guest_personality="mysterious",
            min_friendship="stranger",
            topic_tags=["night", "mystery", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="*appears from shadows* The pond looks different at night. Deeper.",
                    cheese_response="It's the same depth. I checked. With my feet. Twice.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Some things can only be said in the dark.",
                    cheese_response="Like what. Actually, don't tell me. Actually, do. No. Maybe.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Do you ever feel like the pond watches you back?",
                    cheese_response="The pond is water. It doesn't watch. The frogs, however. Those are suspicious.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*whispers* Maybe the frogs know something we don't.",
                    cheese_response="The frogs know where bugs are. That's their whole deal. Mystery solved.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You're very grounding, you know that? *melts back into shadows*",
                    cheese_response="I'm a duck. In a pond. Grounding is literally what I do. Come back anytime.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="mys_the_prophecy",
            title="The Ancient Prophecy",
            guest_personality="mysterious",
            min_friendship="acquaintance",
            topic_tags=["prophecy", "mystery", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="There's an old prophecy about a duck who sits by a pond and changes the world.",
                    cheese_response="I sit by a pond. But the only thing I've changed is the bread-to-water ratio.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The prophecy says the duck will speak truths that reshape reality.",
                    cheese_response="Bread is good. The pond is wet. Reality reshaped. You're welcome.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*eyes narrow* You joke, but there's something about you, Cheese.",
                    cheese_response="Yes. Feathers. And an attitude. Both well-documented.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The prophecy also mentions bread. Specifically.",
                    cheese_response="... go on. I'm listening. The prophecy has my attention. Continue. SLOWLY.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="mys_secret_knowledge",
            title="What the Pond Remembers",
            guest_personality="mysterious",
            min_friendship="friend",
            topic_tags=["mystery", "history", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="They say every pond has a memory. Every stone holds a story.",
                    cheese_response="My rock's story is 'duck sat on it for extended periods.' Not a page-turner.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But what about before you? Who was here before?",
                    cheese_response="A slightly different arrangement of mud. Very dramatic backstory.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I've traveled far. Seen ponds that whisper. Yours is... quiet. Deliberately.",
                    cheese_response="My pond is well-mannered. It doesn't gossip. Unlike SOME visitors.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Keep your secrets then, Cheese. For now.",
                    cheese_response="My secret is that I have no secrets. Which is itself a kind of secret. Wait.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="mys_dream_talk",
            title="Dream Interpretation",
            guest_personality="mysterious",
            min_friendship="close_friend",
            topic_tags=["dreams", "mystery", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="I dreamed of you last night. You were standing in an infinite field of wheat.",
                    cheese_response="Wheat. Which becomes flour. Which becomes bread. That's not a dream, that's a VISION.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You were glowing. And all the other ducks were watching you.",
                    cheese_response="I don't glow. Unless the moonlight hits right. Then I glow a LITTLE.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Dreams reveal our deepest truths. What do YOU dream about?",
                    cheese_response="Bread. Sometimes a really big bread. Once the bread talked. It said my name. Best dream.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That's... oddly beautiful. In a very Cheese way.",
                    cheese_response="All my ways are Cheese ways. I have no other ways available.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="mys_disappearing_act",
            title="The Vanishing Visitor",
            guest_personality="mysterious",
            min_friendship="acquaintance",
            topic_tags=["mystery", "absence", "philosophy"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been away. You probably didn't notice.",
                    cheese_response="I noticed. The pond was thirteen percent less mysterious. I measured.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*slight smile* Where I went, I cannot say.",
                    cheese_response="Okay. I won't ask. I'll just assume it involved being dramatic somewhere else.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I brought you something. From nowhere. From everywhere.",
                    cheese_response="If it's bread, it's the best gift from nowhere. If it's not bread, it's still. Fine.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="It's a stone. From a place you'll never visit. But it remembers you.",
                    cheese_response="*looks at stone* ... I'll put it next to my rock. My rock could use company. Maybe.",
                    mood_effect=4,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="mys_void_talks",
            title="The Void Between Stars",
            guest_personality="mysterious",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="*arrives silently* The spaces between the stars. That's where the real truth lives.",
                    cheese_response="The space between my meals. That's where the real suffering lives. Same energy.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Have you ever stared into darkness so complete that you forgot you existed?",
                    cheese_response="I close my eyes sometimes. Then I remember bread exists. And then I exist again. Bread anchors me to reality.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What if the darkness is not the absence of light but a presence of its own?",
                    cheese_response="What if hunger is not the absence of bread but. Wait. No. It's definitely the absence of bread.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*smiles in the dark* You ground everything in bread. It's almost like a religion.",
                    cheese_response="It's not ALMOST. Bread rises. It nourishes. It asks nothing in return. Draw your own conclusions.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="mys_forbidden_bread",
            title="The Forbidden Loaf",
            guest_personality="mysterious",
            min_friendship="acquaintance",
            topic_tags=["bread", "mystery", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="*leans in* They say there exists a bread so perfect that one bite changes you forever.",
                    cheese_response="Every bread changes me. Every bite is a small transformation. This is not news.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="No. This bread was baked once. In a hidden bakery. By someone who understood the OLD recipes.",
                    cheese_response="Old recipes. *moves closer* How old. Ancient old? Secret old? I'm listening. CAREFULLY.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Some say it was sourdough with a starter older than civilization itself.",
                    cheese_response="A starter older than civilization. That's not bread. That's a deity. I would worship it.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I could tell you where it is. For a price.",
                    cheese_response="Name your price. Except bread. I won't trade bread for bread. That's just bread with extra steps.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="*vanishes* Perhaps next time. When the moon is right.",
                    cheese_response="THE MOON IS RIGHT NOW. Come back. COME BACK WITH THE BREAD INFORMATION.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
            ],
        ),
        GuestConversation(
            id="mys_remember_first_night",
            title="That First Night",
            guest_personality="mysterious",
            min_friendship="close_friend",
            topic_tags=["memory", "friendship", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="Do you remember when we first met? You didn't flinch. Everyone flinches.",
                    cheese_response="You appeared from fog at midnight. I was already having a weird night. You fit right in.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I tested you. Said something cryptic about the pond remembering.",
                    cheese_response="And I said the pond doesn't remember because it's water. You looked offended. It was perfect.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Most ducks avoid me. Too strange. Too quiet. Too many dramatic pauses.",
                    cheese_response="I like quiet. Dramatic pauses are just silence with ambition. I respect that.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="You're the only one who lets me be mysterious without mocking it.",
                    cheese_response="I'm deadpan. You're cryptic. We both confuse everyone else. Alliance of the misunderstood.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="mys_winter_solstice",
            title="Winter Solstice",
            guest_personality="mysterious",
            min_friendship="acquaintance",
            topic_tags=["seasonal", "winter", "mystery"],
            exchanges=[
                ConversationExchange(
                    guest_line="*appears from frost* Tonight is the longest night. The dark holds dominion.",
                    cheese_response="The longest night. Which means the longest wait for breakfast. TRUE darkness.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Ancient beings used to light fires to call the sun back. To defy the dark.",
                    cheese_response="I defy the dark by sitting in it. Unbothered. The dark will tire of me before I tire of it.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="After tonight, the light returns. One minute more each day.",
                    cheese_response="One more minute of light. One more minute closer to warm bread. The math is promising.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="*places a small candle by the pond* For the longest night. A small defiance.",
                    cheese_response="*watches the flame* ... you didn't have to do that. But the pond looks. Better. With that.",
                    mood_effect=5,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="mys_gossip_generous",
            title="The Generous One",
            guest_personality="mysterious",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="*glances around* That generous one. They give and give. It's... suspicious.",
                    cheese_response="Suspicious how. They bring bread. Bread is not suspicious. Bread is trustworthy.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Nobody gives without wanting something. There's always a hidden agenda.",
                    cheese_response="Their agenda is bringing me bread. If that's hidden, I don't want it found. Leave it hidden.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="They tried to give ME a gift. A smooth stone. 'For your collection,' they said.",
                    cheese_response="Did you take it.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="... yes. *pulls out stone* It's actually quite nice.",
                    cheese_response="The mysterious one. With a nice stone. From the generous one. You're less mysterious than you think.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  GENEROUS
    # ===================================================================
    "generous": [
        GuestConversation(
            id="gen_gift_giving",
            title="The Gift Economy",
            guest_personality="generous",
            min_friendship="stranger",
            topic_tags=["gifts", "generosity", "bread"],
            exchanges=[
                ConversationExchange(
                    guest_line="I brought you something! Three kinds of bread! Sourdough, rye, and pumpernickel!",
                    cheese_response="Three. Three breads. *processes this* I need a moment. This is a lot of feelings.",
                    mood_effect=5,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I also brought some seeds and a little cake!",
                    cheese_response="You're overwhelming me with provisions and I don't know how to process generosity at this volume.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Sharing is just what I do! Everyone deserves good food.",
                    cheese_response="Correct. EVERYONE. But especially me. Starting with me. Ending also with me.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I'll bring more next time!",
                    cheese_response="More. *stares into the middle distance* More bread. A concept I can support.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="gen_sharing_lesson",
            title="The Art of Sharing",
            guest_personality="generous",
            min_friendship="acquaintance",
            topic_tags=["sharing", "philosophy", "friendship"],
            exchanges=[
                ConversationExchange(
                    guest_line="You know what makes me happy? Making others happy.",
                    cheese_response="You know what makes ME happy? Bread. We arrive at happiness from different directions.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But don't you feel joy when you share something with a friend?",
                    cheese_response="I share the pond. The pond is shared. Joy: unclear. Wetness: confirmed.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Maybe try sharing a piece of bread with someone. See how it feels.",
                    cheese_response="Share. Bread. You want me to... GIVE AWAY bread. I need to sit down. I'm already sitting.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Even just a crumb! The smallest gesture counts.",
                    cheese_response="A crumb. I... *long pause* I could do a crumb. One crumb. SMALL crumb. Don't push it.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="That's growth, Cheese. I'm proud of you.",
                    cheese_response="Don't be proud. I said COULD. Conditional. The crumb remains hypothetical.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="gen_helping_others",
            title="Community Service",
            guest_personality="generous",
            min_friendship="friend",
            topic_tags=["community", "helping", "kindness"],
            exchanges=[
                ConversationExchange(
                    guest_line="I spent all morning helping the ducklings at the south pond learn to swim.",
                    cheese_response="They're ducks. They can swim. That's the whole thing. Were you... teaching water to a duck.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Some of them were scared! They needed encouragement!",
                    cheese_response="The appropriate encouragement for swimming is: be in water. Congratulations, you're swimming.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Don't you ever help anyone, Cheese?",
                    cheese_response="I help people feel better about their own life choices. By comparison.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You help more than you admit. You helped ME feel less lonely once.",
                    cheese_response="I was sitting here. You approached. I didn't leave. That counts as help, apparently.",
                    mood_effect=4,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="gen_potluck",
            title="The Pond Potluck",
            guest_personality="generous",
            min_friendship="friend",
            topic_tags=["food", "community", "bread"],
            exchanges=[
                ConversationExchange(
                    guest_line="I'm organizing a potluck! Everyone brings something to share!",
                    cheese_response="I'll bring my presence. That's what I'm contributing. My presence and my judgment.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You have to bring FOOD. That's the whole point of a potluck!",
                    cheese_response="I have bread. But that bread is mine. Philosophically and legally.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What if everyone brings bread? A bread potluck!",
                    cheese_response="... that's the best idea anyone has ever had at this pond. In recorded history.",
                    mood_effect=5,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Really?! I'll spread the word!",
                    cheese_response="Spread the word. And the butter. Bring butter. For the bread. This is important.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Cheese, you're actually excited about something!",
                    cheese_response="I'm not excited. I'm bread-motivated. Very different. Entirely different. Completely.",
                    mood_effect=4,
                    friendship_bonus=0.15,
                ),
            ],
        ),
        GuestConversation(
            id="gen_compliment_chain",
            title="Compliment Chain",
            guest_personality="generous",
            min_friendship="close_friend",
            topic_tags=["kindness", "friendship", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="I think you're wonderful, Cheese. Just the way you are.",
                    cheese_response="I. What. That's. Okay. *shuffles feathers* That's a sentence you just said.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Your honesty, your consistency, the way you're always just... here.",
                    cheese_response="Being here is the bare minimum and you're making it sound NOBLE.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Say something nice about yourself. Go on. Try.",
                    cheese_response="I have. Adequate feathers. And my bread identification skills are. Above average.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="That's a start! I think you're brave for just being you.",
                    cheese_response="Stop. I can only handle a finite amount of warmth. My capacity is almost full. Almost.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="gen_rainy_day_care",
            title="Rainy Day",
            guest_personality="generous",
            min_friendship="acquaintance",
            topic_tags=["weather", "care", "kindness"],
            exchanges=[
                ConversationExchange(
                    guest_line="It's raining! I brought you a little umbrella for your rock!",
                    cheese_response="I'm a duck. Water is my medium. But. That's. You brought an umbrella. For me.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I also brought warm bread. Fresh from the bakery. Still steaming!",
                    cheese_response="Warm bread. In the rain. This is the best moment in pond history. Don't tell the other moments.",
                    mood_effect=5,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="You deserve nice things, Cheese. Everyone does.",
                    cheese_response="I deserve bread. You provided bread. The system works. *quietly appreciates*",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Same time next rainy day?",
                    cheese_response="I will be here. Obviously. Being here is my primary skill.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="gen_why_give",
            title="Why I Give",
            guest_personality="generous",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="Cheese, can I be honest? Sometimes giving is exhausting. But I can't stop.",
                    cheese_response="You can stop. Sit here. Do nothing. I've made a career of it.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But if I stop giving, who am I? What's left?",
                    cheese_response="A duck. At a pond. That's enough. Being enough without doing is. Hard. But possible.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Do you think people only like me because I give them things?",
                    cheese_response="I like you. And you've given me bread, so I can't be objective. But. I'd still like you. Probably. Yes.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="*quiet* That means a lot coming from you. You don't say things you don't mean.",
                    cheese_response="I don't. Wasting words is like wasting bread. Unacceptable. So when I say it. I mean it.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="gen_bread_sharing_debate",
            title="To Share or Not to Share",
            guest_personality="generous",
            min_friendship="acquaintance",
            topic_tags=["bread", "sharing", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="I think bread is best when shared. Breaking bread together is sacred!",
                    cheese_response="Bread is sacred. Agreed. The breaking-together part is where you lost me.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But sharing doubles the joy! Half a loaf shared is worth more than a whole loaf alone!",
                    cheese_response="Half a loaf is half a loaf. Math doesn't care about your feelings. That's fifty percent less bread.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What if I gave you a WHOLE loaf and we shared a SECOND loaf?",
                    cheese_response="Now you're thinking. One whole loaf for me. Then we discuss sharing the second. From a position of bread security.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Deal! See, sharing works when everyone has enough first!",
                    cheese_response="Correct. Bread security first. Then generosity. You should write a book. I'll endorse it. From the pond.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="gen_teach_gratitude",
            title="Gratitude Lesson",
            guest_personality="generous",
            min_friendship="friend",
            topic_tags=["teaching", "gratitude", "friendship"],
            exchanges=[
                ConversationExchange(
                    guest_line="I think you should practice gratitude! Every morning, name three things you're thankful for.",
                    cheese_response="Bread. Bread. And bread. There. Practiced. Can I go back to sitting now.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="THREE DIFFERENT things! Not just bread three times!",
                    cheese_response="Sourdough. Whole wheat. Rye. Three DIFFERENT breads. I'm improving.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Something that ISN'T bread. Please. One thing.",
                    cheese_response="... the pond. Because without it I'd have to stand on land all day. And the pond holds bread crumbs.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="That still connected to bread but I'll take it. What about friends? Are you grateful for friends?",
                    cheese_response="I'm grateful for friends who bring bread. And also for friends who don't. Slightly less. But still. Grateful.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="gen_remember_first_gift",
            title="The First Gift",
            guest_personality="generous",
            min_friendship="close_friend",
            topic_tags=["memory", "friendship", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="Remember the first thing I ever gave you? That little piece of cornbread?",
                    cheese_response="I remember. It was warm. And you just. Handed it to me. Without wanting anything back.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You looked at me like I was trying to trick you.",
                    cheese_response="Free bread seemed impossible. A stranger with free bread. My threat assessment was high.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="And then you ate it SO fast and just... stared at me. Waiting for more.",
                    cheese_response="I wasn't waiting for more. I was processing. Slowly. That someone would just. Give.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="And I've been bringing bread ever since.",
                    cheese_response="And I've been here ever since. The system works. Don't fix what isn't broken. *sits closer*",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="gen_gossip_foodie",
            title="About the Foodie",
            guest_personality="generous",
            min_friendship="friend",
            topic_tags=["gossip", "visitors", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="That foodie duck critiqued my homemade bread. Said the crumb structure was 'uneven.'",
                    cheese_response="Uneven crumb structure. In free bread. They criticized FREE BREAD. Unacceptable.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I just wanted to share! I baked it with love!",
                    cheese_response="Love is the best ingredient. I don't know what crumb structure is and I refuse to learn.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="They DID eat three pieces though. While critiquing.",
                    cheese_response="Eating three pieces while complaining is the highest form of food appreciation. They liked it. Obviously.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I suppose that's true. I'll bring more next time. Even if they judge.",
                    cheese_response="Bring more. I won't judge. I'll eat. Silently. With visible satisfaction. No notes.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  FOODIE
    # ===================================================================
    "foodie": [
        GuestConversation(
            id="food_bread_ranking",
            title="The Great Bread Debate",
            guest_personality="foodie",
            min_friendship="stranger",
            topic_tags=["food", "bread", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="Okay, definitive bread ranking. Sourdough is obviously number one.",
                    cheese_response="Sourdough is top three. But whole wheat has a reliability that sourdough can't match.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Whole wheat? WHOLE WHEAT? That's the minivan of breads!",
                    cheese_response="Minivans are reliable. Whole wheat is reliable. I see no insult here.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What about brioche? Rich, buttery, golden—",
                    cheese_response="Brioche is bread that went to finishing school. Respectable. Slightly pretentious.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="And your number one? The BEST bread?",
                    cheese_response="The bread in front of me. Right now. The best bread is the bread that exists.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="That's... surprisingly deep for a bread opinion.",
                    cheese_response="All bread opinions are deep. Bread is not a shallow topic.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
            ],
        ),
        GuestConversation(
            id="food_cooking_lesson",
            title="Cooking Lesson",
            guest_personality="foodie",
            min_friendship="acquaintance",
            topic_tags=["food", "cooking", "culture"],
            exchanges=[
                ConversationExchange(
                    guest_line="I've been learning to bake! Made my first loaf yesterday!",
                    cheese_response="You. Can MAKE bread. From scratch. *stares with unprecedented intensity*",
                    mood_effect=4,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Yeah! Flour, water, yeast, salt. It's actually pretty simple!",
                    cheese_response="You just described the four sacred elements. Casually. Like it's nothing.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Want me to bring you some next time?",
                    cheese_response="Want you to. WANT. I NEED you to. This is not a want situation. This is urgent.",
                    mood_effect=5,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="Haha, deal! Any preferences? Seeds? Herbs?",
                    cheese_response="Surprise me. No wait. Plain. No wait. Seeds. No. Both. BRING BOTH.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_restaurant_review",
            title="Restaurant Critics",
            guest_personality="foodie",
            min_friendship="friend",
            topic_tags=["food", "review", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="I visited a fancy restaurant. Deconstructed salad. Foam everywhere.",
                    cheese_response="Foam is not food. Foam is what happens when I get angry in the pond.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The bread basket was incredible though. Three kinds, with whipped butter.",
                    cheese_response="A bread BASKET. Multiple breads. Organized. With butter. This is civilization.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="The main course was a tiny portion on a huge plate.",
                    cheese_response="Tiny food on big plate. That's the opposite of what food should be. Big food. No plate. Just bread.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="What would your ideal restaurant look like?",
                    cheese_response="A pond. With a bread menu. No reservations required. Open always. That's it. Perfect.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I'd eat there. Every day.",
                    cheese_response="You already do. This IS that restaurant. The pond. You're here. Bread happens.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_taste_test",
            title="Blind Taste Test",
            guest_personality="foodie",
            min_friendship="friend",
            topic_tags=["food", "bread", "games"],
            exchanges=[
                ConversationExchange(
                    guest_line="Close your eyes! I'm going to see if you can identify breads by taste alone!",
                    cheese_response="My eyes are closed. My bread-sense is heightened. I was born for this moment.",
                    mood_effect=3,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Okay, first one! *offers bread piece*",
                    cheese_response="Wheat. White. Day-old. Bakery on the east side. They use too much salt. Next.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That... that was exactly right. How did you—",
                    cheese_response="I know bread like you know disappointment. Intimately and from experience.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Second one! This is harder!",
                    cheese_response="Rye. Caraway seeds. Three days old. Slightly stale. Still perfect. All bread is perfect.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="You're a bread savant. I'm in awe.",
                    cheese_response="Savant is a strong word. I prefer 'dedicated professional.' In the bread arts.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_worst_meal",
            title="Food Crimes",
            guest_personality="foodie",
            min_friendship="acquaintance",
            topic_tags=["food", "humor", "stories"],
            exchanges=[
                ConversationExchange(
                    guest_line="What's the worst thing you've ever eaten?",
                    cheese_response="A leaf. I thought it was bread. It was not bread. The betrayal still stings.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Someone once served me cold soup and called it 'gazpacho.'",
                    cheese_response="Cold soup. That's just aggressive water. With pretensions.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="And they served bread on the side but it was GLUTEN-FREE.",
                    cheese_response="That's not bread. That's a crumbly lie. A structural failure with ambition.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="EXACTLY. We understand each other on a food level.",
                    cheese_response="Food-level understanding is the deepest kind. Everything else is surface.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_perfect_meal",
            title="Last Meal",
            guest_personality="foodie",
            min_friendship="close_friend",
            topic_tags=["food", "philosophy", "deep_talks"],
            exchanges=[
                ConversationExchange(
                    guest_line="If you could have one perfect meal, what would it be?",
                    cheese_response="Bread. Fresh. Warm. By this pond. At sunrise. With someone who understands bread.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="That's it? Just bread?",
                    cheese_response="'Just bread.' There's no 'just' about bread. Bread is the foundation of everything.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What if I baked that bread? Fresh, just for you?",
                    cheese_response="Then it wouldn't be just bread. It would be bread made by someone who. By a friend. *pause*",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
                ConversationExchange(
                    guest_line="I'll do it. One day. The perfect bread for the perfect duck.",
                    cheese_response="I'll be here. At the pond. Where I always am. Waiting. Not impatiently. But waiting.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="food_late_night_hunger",
            title="Midnight Cravings",
            guest_personality="foodie",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="It's midnight and I can't stop thinking about food. Is that weird?",
                    cheese_response="It's midnight and I can't stop thinking about bread. We're both normal. By our standards.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Do you think our relationship with food says something about who we are?",
                    cheese_response="I eat bread. I am Cheese. Both things are true. Beyond that I don't analyze.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Sometimes I think the best meals are the ones eaten in silence. No reviews. Just... being present.",
                    cheese_response="Every meal I eat is in silence. And presence. You've just described my entire life as profound.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Maybe you've had it figured out all along. The rest of us just overcomplicate eating.",
                    cheese_response="Bread. Water. Quiet. The recipe for a life. I should write a cookbook. One page long.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="food_ancient_bread",
            title="Bread Through the Ages",
            guest_personality="foodie",
            min_friendship="friend",
            topic_tags=["bread", "history", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="The oldest bread ever found was 14,000 years old. Flatbread, baked by Natufian hunters.",
                    cheese_response="Fourteen thousand years old. And still bread. Bread endures. Everything else is temporary.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Imagine the first creature to bake bread. They changed EVERYTHING.",
                    cheese_response="The first baker. The most important person who ever lived. I think about them daily.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Egyptian bread was dense and gritty. Sand in the grain. Wore teeth down.",
                    cheese_response="Worth it. Gritty bread is still bread. I'd trade teeth for bread. I barely use teeth anyway.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="French baguettes only became a thing in the 1920s. Relatively new!",
                    cheese_response="1920s. Bread was already ancient. The baguette just showed up and got famous. Classic overachiever.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="What do you think bread will be like in the future?",
                    cheese_response="Still bread. Hopefully still here. With me. At the pond. Some things shouldn't change.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_taste_competition",
            title="The Taste-Off",
            guest_personality="foodie",
            min_friendship="acquaintance",
            topic_tags=["competition", "food", "challenge"],
            exchanges=[
                ConversationExchange(
                    guest_line="I challenge you to a taste-off. I describe a bread, you identify it.",
                    cheese_response="You've challenged me to my own sport. Bold. Foolish. But bold.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Dense, slightly sweet, dark crust, hint of caraway.",
                    cheese_response="Pumpernickel. Next. That was the warmup. I want a real challenge.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Okay. Flaky. Buttery layers. Crescent shape. You can HEAR the crunch.",
                    cheese_response="Croissant. But calling a croissant bread is reductive. It's bread that went to art school.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Final round. Chewy. Circular. Hole in the middle. Boiled then baked.",
                    cheese_response="Bagel. And that description doesn't do it justice. A bagel is a bread HUG. For your mouth.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Three for three. I'm... impressed. And slightly intimidated.",
                    cheese_response="You should be. Bread knowledge is power. Real power. The only power that matters.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="food_spring_foraging",
            title="Spring Foraging",
            guest_personality="foodie",
            min_friendship="acquaintance",
            topic_tags=["seasonal", "spring", "food"],
            exchanges=[
                ConversationExchange(
                    guest_line="Spring is here! Wild garlic, dandelion greens, fresh herbs everywhere!",
                    cheese_response="Spring is here. Bread tourists return. People with picnics. The season of abundance.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You should try foraging! Nature provides an incredible pantry!",
                    cheese_response="Nature provides bread when humans drop it. That's my foraging system. Optimized.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="But fresh herbs on bread? Wild garlic butter on sourdough? Come ON.",
                    cheese_response="... you make a compelling case. But only because you said the word sourdough.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I'll forage some herbs and bring bread. We'll do a spring tasting at the pond.",
                    cheese_response="Tasting at the pond. I'll clear my schedule. Which is empty. But still. Cleared. For this.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="food_remember_first_bread",
            title="First Bread Memory",
            guest_personality="foodie",
            min_friendship="close_friend",
            topic_tags=["memory", "bread", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="What's the first bread you ever remember eating?",
                    cheese_response="White bread. Plain. From a child's hand. I was very small. The bread was very big. Best day.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="A child gave you bread? That's... really sweet.",
                    cheese_response="They threw it at me, technically. But the intent was good. I chose to believe that.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="My first bread memory is my grandmother's kitchen. Warm loaves on the windowsill.",
                    cheese_response="Windowsill bread. The steam rising. The crust cracking. I wasn't there but I can see it. In my bread-mind.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="We should always remember where we started. Food connects us to the past.",
                    cheese_response="Every bread connects to every bread before it. All the way back. Fourteen thousand years of breadline. We're part of it.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
    ],

    # ===================================================================
    #  ATHLETIC
    # ===================================================================
    "athletic": [
        GuestConversation(
            id="ath_morning_swim",
            title="Swim Training",
            guest_personality="athletic",
            min_friendship="stranger",
            topic_tags=["exercise", "swimming", "competition"],
            exchanges=[
                ConversationExchange(
                    guest_line="Just did fifty laps of the big lake. New personal record!",
                    cheese_response="I did zero laps. Of anything. Also a personal record. Unbroken since birth.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You should train with me! Swimming is great exercise!",
                    cheese_response="I swim when I need to get from here to slightly over there. That's enough.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Don't you want to be faster? Stronger?",
                    cheese_response="Faster at what. Sitting. I'm already the fastest sitter at this pond.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You're hopeless! But I respect the commitment to rest.",
                    cheese_response="Rest is an underrated discipline. I've mastered it. Years of training.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_race_challenge",
            title="The Big Race",
            guest_personality="athletic",
            min_friendship="acquaintance",
            topic_tags=["competition", "racing", "fun"],
            exchanges=[
                ConversationExchange(
                    guest_line="Race you to the other side of the pond! Ready? GO!",
                    cheese_response="No. *doesn't move* I win by default. You left. The pond is mine now.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="*comes back panting* That's not how racing works!",
                    cheese_response="I was here when you left. I'm here when you returned. I never lost the pond. I win.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You have to MOVE for it to be a race!",
                    cheese_response="You moved. You ended up back here. Net movement: zero. I achieved zero with less effort.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="I... can't argue with that logic.",
                    cheese_response="Efficiency. It's not laziness if you call it strategy.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_migration_stories",
            title="Migration Season",
            guest_personality="athletic",
            min_friendship="friend",
            topic_tags=["travel", "exercise", "nature"],
            exchanges=[
                ConversationExchange(
                    guest_line="Migration season's coming. You going south this year?",
                    cheese_response="South. North. I'm going to this exact spot. Year-round residency.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="The flock covers thousands of miles! The endurance! The teamwork!",
                    cheese_response="Thousands of miles to find a pond. I already have a pond. Math says I win.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="But the JOURNEY! The V-formation! The wind beneath your wings!",
                    cheese_response="The wind beneath my wings is here. At ground level. It's called a breeze. Sufficient.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="You'll miss me when I'm gone. Admit it.",
                    cheese_response="The pond will be quieter. That's not the same as missing you. Except that it is.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="ath_fitness_tips",
            title="Fitness Advice",
            guest_personality="athletic",
            min_friendship="acquaintance",
            topic_tags=["exercise", "health", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Cheese, I've designed a workout routine just for you!",
                    cheese_response="My current routine: wake up, eat, sit, eat, float, eat, sleep. Optimized.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="That's not a routine, that's a retirement plan!",
                    cheese_response="I've been retired since birth. It's been wonderful.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Just try one wing-stretch! One! For me!",
                    cheese_response="*extends one wing approximately two inches* There. Fitness achieved. I'm winded.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I'll take it. Tiny progress is still progress.",
                    cheese_response="Don't get used to it. That was my annual exercise. See you next year for the other wing.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_medal_ceremony",
            title="Champion Duck",
            guest_personality="athletic",
            min_friendship="close_friend",
            topic_tags=["competition", "achievement", "friendship"],
            exchanges=[
                ConversationExchange(
                    guest_line="I won a race today. First place. Fastest duck in the region.",
                    cheese_response="Congratulations. Genuinely. That's. That's an accomplishment.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Thanks! I trained for months. Blood, sweat, and feathers.",
                    cheese_response="I once stayed awake past my bedtime. So I understand sacrifice. On a smaller scale.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I want to give you my medal. You believed in me. Sort of.",
                    cheese_response="I didn't believe in you. I believed you would come back and tell me about it. Same thing. Almost.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="Take it. Seriously. It means something to me that you're here.",
                    cheese_response="*looks at medal* I'll put it next to my rock. Don't make this a thing. It's already a thing, isn't it.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="ath_stretching_debate",
            title="The Stretching Debate",
            guest_personality="athletic",
            min_friendship="friend",
            topic_tags=["exercise", "debate", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Static stretching before exercise is actually bad. Dynamic warmup is better.",
                    cheese_response="I do neither. My warmup is existing. My cooldown is also existing.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Your muscles must be so stiff! When's the last time you stretched?",
                    cheese_response="I yawned aggressively last Tuesday. Several muscle groups were involved.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="A yawn! That's not a stretch!",
                    cheese_response="It involved opening my bill to maximum capacity. That's extreme sport by duck standards.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Maximum capacity... for bread?",
                    cheese_response="Obviously for bread. Everything at maximum capacity is for bread.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_late_night_body",
            title="The Body Question",
            guest_personality="athletic",
            min_friendship="friend",
            topic_tags=["philosophy", "night", "deep_talks", "late_night"],
            exchanges=[
                ConversationExchange(
                    guest_line="Late night thought. My whole identity is being fast. What happens when I slow down?",
                    cheese_response="You become me. And it's fine here. Slow is underrated.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="But I've ALWAYS been the fast one. Since I was a duckling.",
                    cheese_response="I've always been the sitting one. We both got assigned a thing. Yours just involves more sweating.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="What if I wake up one day and I can't do it anymore?",
                    cheese_response="Then you come to the pond. And we sit. And it's quiet. And that's enough.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
                ConversationExchange(
                    guest_line="You always make things sound simple.",
                    cheese_response="Things ARE simple. Ducks complicate them. Sit. Eat. Be here. The rest is optional.",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
        GuestConversation(
            id="ath_carb_debate",
            title="Carb Loading",
            guest_personality="athletic",
            min_friendship="acquaintance",
            topic_tags=["bread", "exercise", "debate"],
            exchanges=[
                ConversationExchange(
                    guest_line="Bread is actually great for athletes. Complex carbohydrates. Sustained energy.",
                    cheese_response="I knew it. SCIENCE says bread is great. I've been an athlete this whole time.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Well, in moderation. As part of a balanced—",
                    cheese_response="SCIENCE SAYS BREAD IS GREAT. I heard you. Don't walk it back now.",
                    mood_effect=3,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="I carb-load before big races. Pasta mostly. But bread works too.",
                    cheese_response="I carb-load before sitting. And during sitting. And after sitting. Perpetual carb-loading.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="That's not carb-loading. That's just... eating bread all the time.",
                    cheese_response="You have your terminology. I have mine. The bread doesn't care what we call it.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_pushup_challenge",
            title="The Push-Up Challenge",
            guest_personality="athletic",
            min_friendship="friend",
            topic_tags=["competition", "challenge", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Push-up contest! Right now! I'll go first — one, two, three—",
                    cheese_response="I'll go second. *lies flat on rock* Zero. New personal best. In the lying-down category.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="That's not even a push-up attempt! You're just lying there!",
                    cheese_response="I'm resting between sets. The set happened to have zero repetitions. Unconventional training method.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="Come on, ONE push-up. Just one. I'll be so proud of you.",
                    cheese_response="*lifts head slightly* Does this count. I lifted something. Against gravity. That's the whole concept.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="I... you know what, I'll count it. One push-up. Cheese's first ever.",
                    cheese_response="Also my last. Retire at the top. That's what champions do.",
                    mood_effect=4,
                    friendship_bonus=0.25,
                ),
            ],
        ),
        GuestConversation(
            id="ath_teach_form",
            title="Proper Form",
            guest_personality="athletic",
            min_friendship="acquaintance",
            topic_tags=["teaching", "exercise", "humor"],
            exchanges=[
                ConversationExchange(
                    guest_line="Your posture is terrible. Let me teach you proper form.",
                    cheese_response="My posture is 'duck sitting on rock.' It's the only form I have. It's been peer-reviewed.",
                    mood_effect=1,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="Chest up! Shoulders back! Core engaged!",
                    cheese_response="I'm a DUCK. My chest goes forward. My shoulders don't go back. My core is filled with bread.",
                    mood_effect=2,
                    friendship_bonus=0.1,
                ),
                ConversationExchange(
                    guest_line="At least try standing tall. Like THIS. See? Proud. Powerful.",
                    cheese_response="*stands slightly taller* I look like a duck who's heard a strange noise. This isn't power. This is alarm.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You know what, your natural form has its own kind of efficiency.",
                    cheese_response="Thank you. Millions of years of evolution optimized me for sitting and bread. Respect the design.",
                    mood_effect=3,
                    friendship_bonus=0.2,
                ),
            ],
        ),
        GuestConversation(
            id="ath_remember_first_race",
            title="The First Race",
            guest_personality="athletic",
            min_friendship="close_friend",
            topic_tags=["memory", "friendship", "nostalgia"],
            exchanges=[
                ConversationExchange(
                    guest_line="Remember when you actually raced me that one time? You paddled about ten feet and stopped.",
                    cheese_response="I remember. Ten feet was ambitious. I had to nap for an hour afterward.",
                    mood_effect=2,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="But you actually TRIED. For one brief moment, you competed.",
                    cheese_response="I was motivated. There was a bread crumb floating at the ten-foot mark. Let's be honest about the motivation.",
                    mood_effect=3,
                    friendship_bonus=0.15,
                ),
                ConversationExchange(
                    guest_line="You reached that bread crumb before I did. Technically, you won.",
                    cheese_response="I won. My only victory. Bread-motivated. I'd like it noted in the official records.",
                    mood_effect=4,
                    friendship_bonus=0.2,
                ),
                ConversationExchange(
                    guest_line="Undefeated champion of the ten-foot bread dash. You should be proud.",
                    cheese_response="I am. Quietly. Don't make a thing of it. *is clearly making a thing of it internally*",
                    mood_effect=5,
                    friendship_bonus=0.3,
                ),
            ],
        ),
    ],
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_random_conversation(
    personality: str,
    friendship_level: str,
) -> Optional[GuestConversation]:
    """Get a random conversation appropriate for the friendship level.

    Parameters
    ----------
    personality:
        The guest's personality key (e.g. "adventurous", "scholarly").
    friendship_level:
        The current friendship level between Cheese and the guest.

    Returns
    -------
    A randomly-chosen ``GuestConversation`` whose *min_friendship* requirement
    is satisfied by *friendship_level*, or ``None`` if nothing qualifies.
    """
    conversations = GUEST_CONVERSATIONS.get(personality, [])
    if not conversations:
        return None

    eligible = [
        c for c in conversations
        if _friendship_met(c.min_friendship, friendship_level)
    ]

    if not eligible:
        return None

    return random.choice(eligible)


def get_conversation_by_topic(
    personality: str,
    topic: str,
) -> Optional[GuestConversation]:
    """Get a conversation about a specific topic.

    Parameters
    ----------
    personality:
        The guest's personality key.
    topic:
        A topic tag to match against (e.g. "bread", "philosophy", "games").

    Returns
    -------
    A randomly-chosen ``GuestConversation`` whose *topic_tags* include *topic*,
    or ``None`` if no match is found.
    """
    conversations = GUEST_CONVERSATIONS.get(personality, [])
    if not conversations:
        return None

    matches = [c for c in conversations if topic in c.topic_tags]

    if not matches:
        return None

    return random.choice(matches)


def get_all_conversations_for_personality(personality: str) -> List[GuestConversation]:
    """Return every conversation script for a given personality."""
    return list(GUEST_CONVERSATIONS.get(personality, []))


def get_all_topic_tags() -> List[str]:
    """Return a sorted, deduplicated list of every topic tag in the data."""
    tags: set = set()
    for convos in GUEST_CONVERSATIONS.values():
        for c in convos:
            tags.update(c.topic_tags)
    return sorted(tags)
