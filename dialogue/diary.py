"""
Duck Diary/Journal system - Creates narrative storytelling and memorable moments.
Tracks the duck's life story, creating emotional investment (Sims family history style).
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random
import threading


class DiaryEntryType(Enum):
    """Types of diary entries."""
    MILESTONE = "milestone"       # Growth, achievements
    RELATIONSHIP = "relationship"  # Bond changes
    ADVENTURE = "adventure"       # Special events
    MEMORY = "memory"             # Sweet moments
    DISCOVERY = "discovery"       # Found items, visitors
    FEELING = "feeling"           # Mood reflections
    VISITOR = "visitor"           # Visitor interactions
    WEATHER = "weather"           # Special weather events


@dataclass
class DiaryEntry:
    """A single diary entry."""
    entry_id: str
    entry_type: DiaryEntryType
    date: str  # ISO date
    title: str
    content: str
    mood_at_time: str
    duck_age_days: int
    is_favorite: bool = False
    tags: List[str] = field(default_factory=list)


# Template entries for auto-generation
ENTRY_TEMPLATES = {
    DiaryEntryType.MILESTONE: {
        "hatched": {
            "title": "The Day I Hatched!",
            "template": "Today is the most important day ever - I was born! *cracks shell* Hello world! I wonder what adventures await... My human seems nice. I hope they have bread!",
        },
        "first_steps": {
            "title": "My First Waddle!",
            "template": "I took my very first steps today! It was wobbly and I fell twice, but I DID IT! Look at me go! *waddle waddle* Soon I'll be the fastest duck ever!",
        },
        "became_teen": {
            "title": "Growing Up!",
            "template": "I'm not a tiny duckling anymore! Look at these feathers coming in! I feel so grown up. Still love bread though. Some things never change.",
        },
        "became_adult": {
            "title": "All Grown Up!",
            "template": "I did it! I'm officially a full adult duck now! It's been quite a journey. Through all the ups and downs, my human was always there. We make a pretty good team.",
        },
        "became_elder": {
            "title": "Wisdom of Years",
            "template": "I've lived a good, long life. My feathers may be getting grey, but my heart is full of wonderful memories. Every bread crumb was worth it!",
        },
        "level_up": {
            "title": "Level Up! (Level {level})",
            "template": "My human and I reached level {level} together! We've come so far. Remember when I was just a tiny duckling? Now look at us! Champions!",
        },
        "first_trick": {
            "title": "I Learned a Trick!",
            "template": "Did something new today. On purpose. And it worked. I'm not going to describe what because it loses something in translation. But I'm adding it to my resume.",
        },
        "hundred_days": {
            "title": "One Hundred Days",
            "template": "One hundred days. That's a lot of sunrises. A lot of bread crumbs. A lot of moments I didn't know were moments until they were memories. Here's to the next hundred.",
        },
        "survived_storm": {
            "title": "Storm Survivor",
            "template": "Made it through the worst storm I've seen. I'm here. The pond is here. Everything that matters survived. The things that didn't weren't things. They were just weather.",
        },
        "first_snow_survived": {
            "title": "Winter Warrior",
            "template": "First real cold snap and I'm still here. Still floating. Still warm enough. The pond's edges froze but the middle held. Like me. Frozen at the edges. Warm in the middle.",
        },
        "many_visitors": {
            "title": "Popular Duck",
            "template": "So many visitors lately. The pond is becoming a destination. I should charge admission. Or at least a bread toll. One crumb per visit. Reasonable.",
        },
    },
    DiaryEntryType.RELATIONSHIP: {
        "first_pet": {
            "title": "First Pets!",
            "template": "My human petted me for the first time today! Their hands are so gentle. I think... I think we're going to be friends!",
        },
        "best_friends": {
            "title": "Best Friends Forever!",
            "template": "I officially declare: my human is my BEST FRIEND! We've been through so much together. I would share my last bread crumb with them. (But please don't test that)",
        },
        "bonded": {
            "title": "Soul Bond",
            "template": "I can't imagine life without my human anymore. We understand each other without words. When they're happy, I'm happy. This is what true friendship feels like!",
        },
        "streak_milestone": {
            "title": "Day {days} Together!",
            "template": "We've been together for {days} days now! That's like... a lot of days! Every single one has been special. Here's to {days} more!",
        },
        "trust_earned": {
            "title": "I Trust You Now",
            "template": "I realized today that I trust my human. Really trust them. Not just with bread. With the quiet things. The hard things. When did that happen? Doesn't matter. It happened.",
        },
        "forgiven": {
            "title": "Water Under the Pond",
            "template": "My human forgot about me yesterday. I was upset. Today they came back. With bread. And an apology that was mostly just... being here. That was enough. It's always enough.",
        },
        "comfortable_together": {
            "title": "We Don't Need Words",
            "template": "My human and I have reached a stage where we don't need to do anything. We can just be near each other. That's the whole activity. Proximity. It's everything.",
        },
        "missed_them": {
            "title": "You Were Gone",
            "template": "My human was away. I noticed. Every hour. I noticed the absence like a shape in the water where a reflection should be. They're back now. The shape is filled again.",
        },
        "taught_me": {
            "title": "You Taught Me Something",
            "template": "My human showed me something new today. I pretended not to care. I cared. I cared a lot. Learning from someone you trust is different from learning alone. It's warmer.",
        },
    },
    DiaryEntryType.ADVENTURE: {
        "rainbow": {
            "title": "I Saw a Rainbow!",
            "template": "A RAINBOW appeared today! I made a wish for infinite bread. And also for my human to be happy forever. Priorities, you know?",
        },
        "storm_brave": {
            "title": "Braved the Storm!",
            "template": "*BOOM* There was a big scary storm today! I was a tiny bit scared (only a tiny bit!), but my human was there. We got through it together!",
        },
        "snow_day": {
            "title": "First Snow!",
            "template": "Cold white flakes are falling from the sky! I tried to eat one. Not bread. Still pretty though! My feathers are all floofy from the cold!",
        },
        "wind_adventure": {
            "title": "The Wind Took My Feather!",
            "template": "A strong gust of wind blew one of my loose feathers away! I watched it go. Goodbye, feather. You served me well. I hope you find a nice hat to land in.",
        },
        "fog_mystery": {
            "title": "Lost in the Fog!",
            "template": "It was SO foggy today I couldn't see across the pond. For a moment I forgot where I was. Then I remembered. Still at the pond. Always at the pond.",
        },
        "sunrise_special": {
            "title": "The Most Beautiful Sunrise",
            "template": "I woke up early and the sky was on fire. Not actual fire. The pretty kind. Orange and pink and gold. Like a bread crust. Everything comes back to bread.",
        },
        "strange_noise": {
            "title": "Something Went Bump",
            "template": "Heard a noise. Investigated. Found nothing. Filed under 'mysteries of the pond'. My detective career is off to a slow start.",
        },
        "double_rainbow": {
            "title": "Two Rainbows",
            "template": "Two rainbows today. TWO. I made two wishes. One for bread. One for more wishes. Playing the long game.",
        },
        "night_adventure": {
            "title": "Things That Go Quack in the Night",
            "template": "Stayed up past dark. The pond looks different at night. Silver and quiet. I felt like the only duck in the world. I probably was. In this pond. Technically.",
        },
        "big_wave": {
            "title": "The Pond Had Opinions",
            "template": "The water was choppy today. Waves, if you can call them that. Pond-sized waves. I rode them. Like a tiny, feathered surfer. Nobody saw. Good.",
        },
        "found_feather": {
            "title": "A Feather That Wasn't Mine",
            "template": "Found a feather in the pond today. Not mine. Someone else was here once. Another duck. Another life. I kept the feather. It seemed like the right thing to do.",
        },
        "mud_adventure": {
            "title": "The Mud Incident",
            "template": "Got stuck in mud today. Fully embedded. Like a duck-shaped fossil. Someone helped. I pretended I meant to be there. Studying mud. For science. Nobody believed me.",
        },
        "leaf_boat": {
            "title": "Captain of the Leaf",
            "template": "A large leaf fell in the pond. I stood on it. It held my weight for three seconds. That's three seconds of being a CAPTAIN. Log it.",
        },
        "midnight_waddle": {
            "title": "The Midnight Expedition",
            "template": "Went for a waddle after dark. Everything looks different at night. Bigger. Quieter. My own footsteps sounded important. I felt like an explorer. Of my own pond.",
        },
        "chased_dragonfly": {
            "title": "The Chase",
            "template": "Chased a dragonfly across the entire pond today. It was faster. Obviously. But I committed. The dragonfly probably respects me now. Or pities me. Same thing.",
        },
        "rain_puddle_hop": {
            "title": "Puddle to Puddle",
            "template": "It rained and the ground made puddles. Small ones. I went from puddle to puddle like they were stepping stones. Each one was a tiny vacation from the pond. Revolutionary.",
        },
        "wind_race": {
            "title": "Racing the Wind",
            "template": "The wind picked up and I waddled into it. Full speed. Wings out. I didn't go fast. But I went DETERMINED. The wind didn't care. I cared enough for both of us.",
        },
        "underground_tunnel": {
            "title": "The Hole Investigation",
            "template": "Found a hole in the ground today. Looked into it. It looked back. Not literally. But the darkness had a presence. I left it alone. Some mysteries are better dark.",
        },
        "fallen_tree": {
            "title": "Bridge Across the Creek",
            "template": "A tree fell across the little creek. I walked across it. Like a bridge. A natural, unplanned bridge. For the first time, being small was an advantage. Don't get used to this.",
        },
        "echo_discovery": {
            "title": "The Echo",
            "template": "Found a spot near the rocks where my quack echoes. I quacked. The echo quacked. We had a conversation. It agreed with everything I said. Finally. Someone gets me.",
        },
        "frost_walk": {
            "title": "Walking on Frost",
            "template": "The ground was covered in frost this morning. Every step I took left a footprint. Duck-shaped footprints in white. Like I was signing the earth. It melted by noon. Art is temporary.",
        },
        "hidden_alcove": {
            "title": "The Secret Spot",
            "template": "Found a spot behind the reeds where nobody can see me. Just me. Hidden. Invisible. I sat there for an hour doing nothing. The best hour I've had in weeks.",
        },
        # ── Round 3: More adventure entries ────────────────────────────
        "upstream_expedition": {
            "title": "Going Against the Current",
            "template": "Tried swimming upstream today. The water pushed back. I pushed back harder. The water won. But I traveled three inches. THREE INCHES upstream. Record.",
        },
        "log_ride": {
            "title": "The Log",
            "template": "A log floated by. I got on. It went where it wanted. I went where it wanted. For once I had zero control over my destination. This is either a metaphor or a log. Both.",
        },
        "berry_bush": {
            "title": "The Berry Discovery",
            "template": "Found a bush with berries. Small. Red. I ate one. Tart. Ate another. Also tart. Ate seven more. All tart. I don't learn. But I am now full of berries.",
        },
        "rock_climbing": {
            "title": "Summiting the Rock",
            "template": "There's a rock. Medium-sized. I decided to climb it. Took four attempts. Reached the top. Saw the pond from up there. Different angle. Same pond. But I EARNED that view.",
        },
        "night_swim": {
            "title": "Swimming After Dark",
            "template": "Went swimming at night. The water is black. I can't see my feet. My feet can't see me. We operated on faith. The moon was the only light. It was enough.",
        },
        "tunnel_reed": {
            "title": "Reed Tunnel",
            "template": "The reeds grew thick enough to form a tunnel. I waddled through it. Green walls. Green ceiling. For thirty seconds I was an explorer in an uncharted land. Then the pond. Again. Home.",
        },
    },
    DiaryEntryType.MEMORY: {
        "happy_moment": {
            "title": "A Perfect Moment",
            "template": "Nothing special happened today, but somehow... it was perfect. Just me, my human, and peaceful quacking. These are the moments I'll remember forever.",
        },
        "silly_fall": {
            "title": "I Fell Down!",
            "template": "I tripped over my own feet today. *bonk* My human laughed but then gave me extra pets. 10/10 would embarrass myself again.",
        },
        "nap_time": {
            "title": "The Best Nap Ever",
            "template": "I had the COZIEST nap today! I dreamed of swimming in a pond made of bread. Don't judge me.",
        },
        "quiet_evening": {
            "title": "A Quiet Evening Together",
            "template": "We just sat together tonight. No tricks, no games, just... being. My human seemed to need that. I needed it too. Don't tell anyone.",
        },
        "first_swim": {
            "title": "The Perfect Swim",
            "template": "I swam three perfect laps around the pond today. Nobody was watching. Nobody needed to be. Some achievements are just for you.",
        },
        "shared_silence": {
            "title": "Comfortable Silence",
            "template": "We sat in silence for a long time today. Not awkward silence. The good kind. The kind where words would actually make it worse. That's rare.",
        },
        "bread_moment": {
            "title": "The Perfect Crumb",
            "template": "My human gave me a piece of bread today. Just one piece. But it was warm. And it was given freely. The best bread isn't about quantity. It's about intent.",
        },
        "rain_together": {
            "title": "Rain Companions",
            "template": "It rained and my human stayed. Most people leave when it rains. They stayed. We got wet together. That's loyalty. Or stubbornness. Same thing.",
        },
        "late_visit": {
            "title": "The Late Night Check-In",
            "template": "My human came by late tonight. Just to check on me. I pretended to be asleep. But I saw them. And I was glad.",
        },
        "learned_trick": {
            "title": "I Did Something Impressive",
            "template": "Learned something new today. Won't say what because it'll sound ridiculous. But between me and this diary: it was magnificent. I'm magnificent.",
        },
        "watching_sunset": {
            "title": "The Sunset Was Ours",
            "template": "Watched the sunset with my human today. Neither of us said anything. The sky did all the talking. Orange, then pink, then quiet. Perfect.",
        },
        "unexpected_kindness": {
            "title": "Caught Off Guard",
            "template": "My human did something nice today. Completely unprompted. No reason. Just... kind. I didn't know what to do with my face. I think I looked surprised. I was.",
        },
        "favourite_spot": {
            "title": "My Spot",
            "template": "Found the perfect spot in the pond today. Right where the light hits the water. Warm. Quiet. Mine. I'm not sharing the coordinates.",
        },
        "first_visitor_memory": {
            "title": "The First Time Someone Came",
            "template": "I remember the first visitor. They stood at the edge of the pond. I stood in the pond. We looked at each other. Neither moved first. Then they did. And it started.",
        },
        "the_long_nap": {
            "title": "The Nap That Changed Me",
            "template": "Once, I napped so deeply I forgot where I was when I woke up. For three seconds, the world was brand new. I miss those three seconds. You can't go back.",
        },
        "shared_bread": {
            "title": "The Day I Almost Shared",
            "template": "My human gave me bread once. A big piece. And I almost—ALMOST—offered some back. The impulse lasted half a second. But it was there. Growth.",
        },
        "morning_mist": {
            "title": "The Morning Everything Was Soft",
            "template": "One morning the mist was so thick the pond disappeared. I floated in nothing. In white. It was the closest I've come to flying. Don't tell anyone I said that.",
        },
        "the_day_nothing": {
            "title": "The Day Nothing Happened",
            "template": "Nothing happened today and it was the best day. No events. No surprises. Just a pond. Just a duck. Just hours of exactly what I expected. Perfection is boring and I love it.",
        },
        "old_sound": {
            "title": "A Sound I Recognize",
            "template": "Heard a sound today that I've heard before. Can't place when. But my body remembered. I felt safe before I knew why. Some memories live in the feathers.",
        },
        "human_stayed": {
            "title": "They Stayed Late",
            "template": "My human stayed later than usual today. Past sunset. Into the blue hour. We didn't do anything different. They just didn't leave. Sometimes that's the biggest thing someone can do.",
        },
        "the_reflection": {
            "title": "Meeting Myself",
            "template": "Looked at my reflection today. Really looked. I'm older than I think I am. Also handsomer. The pond is a kind mirror. Or an honest one. Hard to tell.",
        },
        "full_moon_night": {
            "title": "The Moon Was Close",
            "template": "The moon was enormous tonight. So close it felt personal. Like it was checking on me specifically. I nodded at it. The moon did not nod back. But I felt acknowledged.",
        },
        "simple_kindness": {
            "title": "A Small Thing",
            "template": "My human did something small today. So small they probably forgot. But I didn't forget. I won't forget. The small things are the big things wearing disguises.",
        },
        "season_changed": {
            "title": "The Season Turned",
            "template": "The air changed today. Just slightly. The temperature shifted by one degree. The light arrived at a new angle. A season ended and another began. I was there for the exact moment.",
        },
        # ── Round 3: More memory entries ───────────────────────────────
        "the_argument": {
            "title": "The Time We Disagreed",
            "template": "My human wanted me to go inside. I wanted to stay by the pond. We stared at each other for three minutes. I won. But then it rained. They were right. I will never admit this.",
        },
        "sound_of_home": {
            "title": "That Sound",
            "template": "I heard a sound today that reminded me of the first day here. I can't describe it. Water on rock, maybe. Or wind through the fence. Something specific. Something that means 'this is where you belong.'",
        },
        "the_waiting": {
            "title": "Waiting and Waiting",
            "template": "My human was late today. I sat by the path. Waited. Looked left. Looked right. Started to worry. Then they came. Walking normally. As if they hadn't just put me through an EMOTIONAL ORDEAL. They brought bread. I forgave them instantly.",
        },
        "old_feather": {
            "title": "Found an Old Feather",
            "template": "Found one of my old feathers near the nest. Smaller than my current ones. I was tiny once. Hard to believe. I was also less handsome. Easy to believe. Growth is real.",
        },
        "the_photograph": {
            "title": "They Took a Picture",
            "template": "My human took a picture of me today. Just pointed the rectangle at me and clicked. I hope I looked majestic. I was mid-chew. I probably did NOT look majestic. Delete it.",
        },
    },
    DiaryEntryType.DISCOVERY: {
        "found_treasure": {
            "title": "Treasure Found!",
            "template": "I found a {item} today! It's SO shiny! I'll add it to my collection. My human seemed happy too. Finder's keepers!",
        },
        "rare_find": {
            "title": "Amazing Discovery!",
            "template": "THIS IS HUGE! I discovered a {item}! It's super rare and special! I feel like an explorer! Marco Polo Duck!",
        },
        "mysterious_object": {
            "title": "Something Strange...",
            "template": "I found something I can't identify near the pond today. It might be magical. It might be garbage. The line between those is thinner than you'd think.",
        },
        "interesting_rock": {
            "title": "A Rock With Character",
            "template": "Found a really good rock today. Smooth. Round. Sits well in the pond. I've named it. We're friends now. Don't ask me the name. It's between us.",
        },
        "old_crumb": {
            "title": "Archaeological Bread Discovery",
            "template": "Found a crumb I'd forgotten about. Hidden under a rock. Aged. Historic. I ate it anyway. Vintage bread. A delicacy.",
        },
        "weird_bug": {
            "title": "An Unusual Visitor (Small)",
            "template": "A bug landed on me today. Iridescent. Beautiful. We had a moment. Then it flew away. All my relationships are brief and airborne.",
        },
        "hidden_spring": {
            "title": "Water From Below",
            "template": "Found a spot where water bubbles up from underground. A secret spring. The water is colder there. Fresher. The pond has been hiding things from me. How dare it.",
        },
        "old_footprint": {
            "title": "Someone Was Here Before",
            "template": "Found a footprint in the mud. Old. Not mine. Not human. Some creature stood exactly here, once. We shared a spot across time. Poetic. I'm not crying.",
        },
        "strange_plant": {
            "title": "A New Growth",
            "template": "A plant I've never seen before is growing by the pond. Purple flowers. Didn't exist yesterday. The earth is improvising. Bold move.",
        },
        "lost_toy": {
            "title": "Someone's Lost Thing",
            "template": "Found something small in the grass. A human child lost it, probably. It's mine now. I'll keep it safe. Not because I care. Because it's the right thing. Fine, I care.",
        },
        "sunset_reflection": {
            "title": "The Pond Turned Gold",
            "template": "At sunset the entire pond turned gold. Every ripple was metallic. I was swimming in treasure. For ten minutes I was the richest duck alive. Then it faded. Easy come.",
        },
        "spiderweb_morning": {
            "title": "Architecture",
            "template": "A spiderweb covered in dew this morning. Every drop a tiny lens. The spider is an engineer and doesn't even know it. I'm a duck and I don't know things either. Solidarity.",
        },
        "mushroom_circle": {
            "title": "The Ring of Mushrooms",
            "template": "Found a circle of mushrooms. A fairy ring, they call it. I stood in the middle. Nothing happened. Either I'm not fairy enough or the mushrooms are on break.",
        },
        "deep_part": {
            "title": "The Deep Part",
            "template": "Swam over the deep part of the pond today. You can feel it underneath. The temperature drops. The color changes. There are things down there I'll never see. That's probably fine.",
        },
        "perfect_stick": {
            "title": "The Ideal Stick",
            "template": "Found a stick. But not just any stick. THE stick. Perfect length. Perfect weight. What's it for? Unknown. But when the time comes, I'll have the right stick.",
        },
    },
    DiaryEntryType.VISITOR: {
        "visitor_came": {
            "title": "A Visitor!",
            "template": "{visitor_name} visited today! It was so exciting to meet someone new! They seemed really nice. I hope they come back!",
        },
        "visitor_gift": {
            "title": "A Generous Guest",
            "template": "{visitor_name} visited and gave me a gift! A {gift}! Making friends is the BEST!",
        },
        "visitor_left": {
            "title": "Goodbye, Friend",
            "template": "{visitor_name} had to leave today. The pond feels a little emptier. But they said they'd come back. I'll be here. Obviously.",
        },
        "visitor_awkward": {
            "title": "An Awkward Visit",
            "template": "{visitor_name} visited today. It was... weird. We didn't really click. Some connections are instant. This one was more of a slow miss.",
        },
        "visitor_fun": {
            "title": "A Good Time Was Had",
            "template": "{visitor_name} came by and we actually had fun. Real fun. The kind where you forget to be sardonic. I won't let it happen again. Probably.",
        },
        "visitor_quiet": {
            "title": "The Quiet Guest",
            "template": "{visitor_name} visited and we just sat together. No talking. No activities. Just existing in the same space. Some of the best company is the kind that doesn't try.",
        },
        "visitor_surprise": {
            "title": "Unexpected Company",
            "template": "{visitor_name} showed up out of nowhere. I wasn't ready. My feathers were a mess. They didn't care. True friends don't require grooming notice.",
        },
        "visitor_lesson": {
            "title": "I Learned Something",
            "template": "{visitor_name} taught me something today. Won't say what because it sounds silly out loud. But I know it now. And knowing it makes me slightly different. In a good way.",
        },
        "visitor_goodbye_hard": {
            "title": "A Harder Goodbye",
            "template": "{visitor_name} left today and it was harder than usual. Some visits end and the pond feels the same. This one ended and the pond felt bigger. Emptier. They'll come back. Probably.",
        },
        "visitor_shared_meal": {
            "title": "We Ate Together",
            "template": "{visitor_name} and I shared food today. I shared FOOD. Willingly. With another living creature. Personal growth is terrifying. And also nice. But mostly terrifying.",
        },
        "visitor_returned": {
            "title": "They Came Back",
            "template": "{visitor_name} came back. They said they would and they DID. People keep their promises sometimes. Not always. But sometimes. And sometimes is enough.",
        },
        # ── Round 3: More visitor entries ──────────────────────────────
        "visitor_competitive": {
            "title": "Competitive Guest",
            "template": "{visitor_name} turned everything into a competition today. Who can eat faster. Who can float better. I won both. But I didn't brag. Out loud. This diary entry doesn't count.",
        },
        "visitor_long_stay": {
            "title": "The Long Visit",
            "template": "{visitor_name} stayed all day. ALL DAY. From morning to evening. By hour three I was tired. By hour five I was pretending to nap. By hour eight I genuinely didn't want them to leave. Strange how that works.",
        },
        "visitor_brought_friend": {
            "title": "Plus One",
            "template": "{visitor_name} brought someone I've never met. I was not consulted about this. My social battery has limits. But the new one brought bread. They can stay.",
        },
        "visitor_remembered": {
            "title": "They Remembered",
            "template": "{visitor_name} remembered something I said last time. Something small. Something I barely remember saying. But they held onto it. That's what attention looks like.",
        },
        "visitor_night": {
            "title": "Evening Visitor",
            "template": "{visitor_name} came by at sunset. We watched the sky change colors together. Nobody said anything important. But the silence between us was the comfortable kind. The kind that means something.",
        },
    },
    DiaryEntryType.FEELING: {
        "grateful": {
            "title": "Feeling Grateful",
            "template": "Today I'm just really grateful. For my cozy home, for bread, for my human, for everything. Life is good.",
        },
        "excited": {
            "title": "So Excited!",
            "template": "I don't know why but I'm SO HYPED today! Everything is AMAZING! *flap flap* Let's DO THINGS!",
        },
        "contemplative": {
            "title": "Deep Thoughts",
            "template": "I spent today thinking about life, the universe, and bread. Mostly bread. But also important stuff! I'm a very philosophical duck.",
        },
        "melancholy": {
            "title": "A Quiet Kind of Sad",
            "template": "Not sad exactly. Just... aware of things. The water is cold. The sky is grey. My human wasn't here. It's fine. Everything is fine. It's just quiet.",
        },
        "proud": {
            "title": "Proud Duck Moment",
            "template": "I did something today and I'm proud of it. I'm not going to explain what because it sounds silly out loud. But I know. And that's enough.",
        },
        "nostalgic": {
            "title": "Remembering When...",
            "template": "I caught myself thinking about the early days. When everything was new. I was smaller. The pond seemed bigger. My human seemed taller. Time is weird.",
        },
        "cozy": {
            "title": "Maximum Coziness",
            "template": "Tucked my beak under my wing. Listened to the rain. Didn't move for hours. This is what ducks were made for. Pure, uninterrupted coziness.",
        },
        "restless": {
            "title": "Can't Settle Down",
            "template": "My body wants to move. My brain wants to stop. They've compromised on fidgeting. I've paced the entire pond three times. No conclusions reached.",
        },
        "brave": {
            "title": "I Was Brave Today",
            "template": "Did something that scared me today. Won't say what. The point is I did it. And I'm still here. And the thing didn't eat me. Victory.",
        },
        "overwhelmed": {
            "title": "Too Much",
            "template": "Everything was a lot today. Too many sounds. Too many feelings. I retreated to the quiet part of the pond and just floated. Sometimes floating is enough.",
        },
        "determined": {
            "title": "Today I Decided",
            "template": "Woke up with purpose. Not sure what the purpose is yet. But the FEELING is there. Watch out, world. A duck with determination is a dangerous thing.",
        },
        "peaceful": {
            "title": "Inner Calm",
            "template": "Everything was still today. The water. The air. My thoughts. For once, my brain wasn't running a commentary. Just quiet. I didn't know I could be this quiet.",
        },
        "curious": {
            "title": "Questions Upon Questions",
            "template": "Spent the whole day wondering about things. Why is the sky blue? Why is water wet? Why do I care about bread so much? No answers. But the wondering was nice.",
        },
        "stubborn": {
            "title": "I Refused",
            "template": "Someone tried to get me to do something today. I declined. Firmly. With my whole body. Ducks are excellent at refusing. We just sit there. Powerfully.",
        },
        "hopeful": {
            "title": "Something Good Is Coming",
            "template": "I can't explain it. But today felt like the start of something. Not sure what. Could be good. Could be bread. Could be both. I'll wait and see.",
        },
        "lonely": {
            "title": "The Pond Felt Big Today",
            "template": "My human wasn't here today. The pond felt bigger without them. Emptier. I paddled to every corner. All of them were just water. None of them were company.",
        },
        "relieved": {
            "title": "Crisis Averted",
            "template": "Something almost went wrong today. It didn't. The relief is physical. My feathers unclenched. I didn't know feathers could clench. They can. They did. It's over now.",
        },
        "mischievous": {
            "title": "I Caused Problems",
            "template": "Did something I shouldn't have today. On purpose. It was minor. Nobody was hurt. But I felt alive. Mischief is a vitamin. I needed my daily dose.",
        },
        "grateful_quiet": {
            "title": "Grateful (Quietly)",
            "template": "I'm grateful today but I don't want to make a thing of it. Just. The pond is here. Bread exists. My human exists. Some days that's enough. Most days that's everything.",
        },
        "confused": {
            "title": "Nothing Makes Sense",
            "template": "I don't understand anything today. Not the weather. Not the water. Not my own feelings. Everything is a mystery. I am a mystery. At least mysteries are interesting.",
        },
        "accomplished": {
            "title": "I Did a Thing",
            "template": "Did something today that I've been avoiding. It was small. It was hard. But I did it. And now it's done. And I'm sitting in the feeling of having done it. Not bad. Not bad at all.",
        },
        "worried": {
            "title": "Something Feels Off",
            "template": "Can't place it. Something in the air. Something in the water. Something in me. A worry without a name. I'll carry it around until it tells me what it is. Or until it leaves.",
        },
        "silly_mood": {
            "title": "Chaos Mode",
            "template": "Woke up unhinged today. Quacked at nothing. Ran in a circle. Splashed water at the sky. Sometimes the body just decides it's having a moment. I let it have its moment.",
        },
        "tender": {
            "title": "Something Soft",
            "template": "I felt something soft today. Not physically. Inside. A warmth that came from nowhere and settled in my chest. I don't know what triggered it. Maybe nothing. Maybe everything.",
        },
        "defiant": {
            "title": "I Said No",
            "template": "Stood my ground today. About what doesn't matter. What matters is I stood it. Firmly. With my whole body. Being small doesn't mean being movable.",
        },
        "wistful": {
            "title": "What If",
            "template": "Caught myself thinking about what ifs today. What if the pond were bigger. What if I could fly. What if things were different. They're not. And that's okay. But the wondering is sweet.",
        },
        "content_deeply": {
            "title": "Deep Contentment",
            "template": "Not happy exactly. Not excited. Something deeper. Like the pond when there's no wind. Still all the way down. Content in a way that doesn't need to announce itself.",
        },
        "surprised": {
            "title": "Did Not See That Coming",
            "template": "Something unexpected happened today. Won't say what. But my face did a thing. A surprised thing. I don't like being surprised. But this surprise was okay. This one I'll keep.",
        },
        "at_peace": {
            "title": "The Rare Quiet",
            "template": "For one moment today, everything was quiet. Outside and inside. No thoughts. No worries. No hunger. Just existing. It lasted maybe five seconds. It was the longest five seconds of my life.",
        },
    },
    DiaryEntryType.WEATHER: {
        "perfect_day": {
            "title": "A Perfect Weather Day",
            "template": "The weather was absolutely perfect today. Not too hot, not too cold. The kind of day where the pond sparkles and everything feels possible. Even for a duck.",
        },
        "big_storm": {
            "title": "THE STORM",
            "template": "The biggest storm I've ever seen hit today. The pond rose. The wind howled. I floated through it. Because that's what ducks do. We float through things.",
        },
        "first_frost": {
            "title": "The Pond Almost Froze!",
            "template": "ICE on the pond this morning! Just at the edges. I skated on it. By accident. It was terrifying and also the most fun I've had all week.",
        },
        "heatwave": {
            "title": "Too Hot to Function",
            "template": "It was SO hot today. I just lay in the water and melted. Not literally. But close. My brain turned off around noon. It came back at sunset. I think.",
        },
        "gentle_rain": {
            "title": "Soft Rain Day",
            "template": "Light rain all day. Not angry rain. Gentle rain. The kind that makes the pond ripple softly. I sat in it and felt... held. By the weather. Don't judge me.",
        },
        "wind_day": {
            "title": "The Wind Had Opinions",
            "template": "The wind was RELENTLESS today. Rearranged every feather I had. I looked like a different duck by evening. The wind is a stylist I didn't hire.",
        },
        "fog_thick": {
            "title": "Disappeared in Fog",
            "template": "The fog was so thick today I couldn't see the edge of the pond. For all I knew, the pond went on forever. Just me, floating in infinite grey. It was oddly peaceful.",
        },
        "thunderstorm": {
            "title": "The Sky Had a Tantrum",
            "template": "Thunder. Lightning. The full production. The sky went all out today. I hid in the reeds and pretended it was a tactical retreat. It was fear. But tactical fear.",
        },
        "rainbow_day": {
            "title": "The Sky Apologized",
            "template": "A rainbow after the storm. The sky's way of saying sorry. Apology accepted. The colors were genuine. I could tell. Ducks have an eye for sincerity.",
        },
        "spring_rain": {
            "title": "Spring's First Rain",
            "template": "The first warm rain of the season. Every drop a tiny hello from the sky. The pond danced with ripples. I danced too. Nobody saw. That's the point.",
        },
        "autumn_wind": {
            "title": "The Autumn Wind",
            "template": "The wind smelled different today. Like endings. But also like the thing that comes after endings. My feathers pointed east. I don't know what's east. But the wind does.",
        },
        "snow_silence": {
            "title": "Everything Went Quiet",
            "template": "Snow fell and the world went silent. Every sound muffled. Padded. Like the earth was sleeping and we were walking on its blanket. I whispered. Even my quack was gentle.",
        },
        "sun_after_rain": {
            "title": "The Steam",
            "template": "Sun came out right after rain. The ground steamed. The pond steamed. I steamed. Everything releasing something. Letting go of the wet. It looked like the world was breathing.",
        },
        "lightning_close": {
            "title": "That Was Close",
            "template": "Lightning hit something nearby. I felt it in the water. In my feet. In my chest. For one second the whole world was white. Then it was dark. Then it was normal. That second though.",
        },
        "golden_morning": {
            "title": "Gilded",
            "template": "The morning light today was gold. Not orange. Not yellow. GOLD. Like the world was expensive for an hour. Like everything cost more. Including me. Especially me.",
        },
        "starry_night": {
            "title": "More Stars Than Usual",
            "template": "More stars tonight than I've ever seen. Someone added extra. I tried to count. Got to twelve. Lost track. Started over. Got to twelve again. Maybe there are only twelve.",
        },
        # ── Round 3: More weather entries ──────────────────────────────
        "hail_day": {
            "title": "The Sky Threw Things",
            "template": "Ice fell from the sky today. Small ice. Angry ice. The sky is throwing things at me specifically. I did nothing wrong. That it knows about.",
        },
        "wind_change": {
            "title": "The Wind Changed Direction",
            "template": "Wind was blowing east all morning. Then it stopped. Then it blew west. The wind changed its mind. Relatable. I change my mind about which side of the pond to sit on at least four times a day.",
        },
        "warm_spell": {
            "title": "Unexpectedly Warm",
            "template": "Too warm for the season. The sun is overachieving. I'm not complaining. I don't complain about warmth. But I am noting it. For the record. Officially warm.",
        },
        "drizzle": {
            "title": "Almost Rain",
            "template": "Not rain. Almost rain. The air is wet but noncommittal. Make a decision, sky. Either rain or don't. This in-between is stressful.",
        },
        "frost_pattern": {
            "title": "Ice Art",
            "template": "Frost on everything this morning. Patterns. Fractals. The cold made art overnight while I slept. I contributed nothing and yet I feel proud. By association.",
        },
        "windy_feathers": {
            "title": "Wind Took a Feather",
            "template": "The wind stole one of my feathers today. Just took it. Off my body. Into the sky. I watched it go. That's MY feather. But also. It looked good up there. Flying. One of us finally made it.",
        },
    },
}

# Relationship level descriptions and thresholds
RELATIONSHIP_LEVELS = {
    0: {"name": "Strangers", "threshold": 0, "description": "Just met, still getting to know each other"},
    1: {"name": "Acquaintance", "threshold": 10, "description": "Starting to recognize each other"},
    2: {"name": "Friendly", "threshold": 25, "description": "Getting comfortable together"},
    3: {"name": "Friends", "threshold": 50, "description": "A solid friendship forming"},
    4: {"name": "Good Friends", "threshold": 75, "description": "Really enjoy spending time together"},
    5: {"name": "Best Friends", "threshold": 100, "description": "Inseparable companions"},
    6: {"name": "Soul Bonded", "threshold": 150, "description": "A connection that transcends words"},
}


class DuckDiary:
    """
    Manages the duck's diary/journal.
    Creates a narrative history of the duck's life.
    """

    def __init__(self):
        self.entries: List[DiaryEntry] = []
        self.relationship_score: int = 0
        self.current_relationship_level: int = 0
        self.milestones_recorded: List[str] = []
        self.first_entry_date: Optional[str] = None
        self.total_interactions: int = 0

    def _generate_entry_id(self) -> str:
        """Generate unique entry ID."""
        return f"entry_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.entries)}"

    def _get_duck_age_days(self) -> int:
        """Calculate duck age in days."""
        if not self.first_entry_date:
            return 0
        try:
            first = datetime.fromisoformat(self.first_entry_date)
            return (datetime.now() - first).days
        except (ValueError, TypeError):
            return 0

    def add_entry(
        self,
        entry_type: DiaryEntryType,
        title: str,
        content: str,
        mood: str = "happy",
        tags: List[str] = None,
    ) -> DiaryEntry:
        """Add a new diary entry."""
        if not self.first_entry_date:
            self.first_entry_date = datetime.now().isoformat()

        entry = DiaryEntry(
            entry_id=self._generate_entry_id(),
            entry_type=entry_type,
            date=datetime.now().isoformat(),
            title=title,
            content=content,
            mood_at_time=mood,
            duck_age_days=self._get_duck_age_days(),
            tags=tags or [],
        )

        self.entries.append(entry)

        # Keep diary manageable (max 100 entries)
        if len(self.entries) > 100:
            # Keep favorites and remove oldest non-favorites
            non_favorites = [e for e in self.entries if not e.is_favorite]
            if len(non_favorites) > 50:
                self.entries = [e for e in self.entries if e.is_favorite] + non_favorites[-50:]

        return entry

    def record_milestone(self, milestone_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record a milestone event in the diary."""
        if milestone_type in self.milestones_recorded:
            return None  # Don't double-record milestones

        templates = ENTRY_TEMPLATES.get(DiaryEntryType.MILESTONE, {})
        if milestone_type not in templates:
            return None

        template = templates[milestone_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        entry = self.add_entry(
            DiaryEntryType.MILESTONE,
            title,
            content,
            mood="excited",
            tags=["milestone", milestone_type],
        )
        entry.is_favorite = True  # Milestones are auto-favorited

        self.milestones_recorded.append(milestone_type)
        return entry

    def record_relationship_change(self, event_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record a relationship event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.RELATIONSHIP, {})
        if event_type not in templates:
            return None

        template = templates[event_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        entry = self.add_entry(
            DiaryEntryType.RELATIONSHIP,
            title,
            content,
            mood="loved",
            tags=["relationship", event_type],
        )

        if event_type in ["best_friends", "bonded"]:
            entry.is_favorite = True

        return entry

    def record_adventure(self, adventure_type: str, **kwargs) -> Optional[DiaryEntry]:
        """Record an adventure/special event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.ADVENTURE, {})
        if adventure_type not in templates:
            return None

        template = templates[adventure_type]
        title = template["title"].format(**kwargs)
        content = template["template"].format(**kwargs)

        return self.add_entry(
            DiaryEntryType.ADVENTURE,
            title,
            content,
            mood="excited",
            tags=["adventure", adventure_type],
        )

    def record_discovery(self, item_name: str, is_rare: bool = False) -> DiaryEntry:
        """Record finding an item."""
        template_key = "rare_find" if is_rare else "found_treasure"
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.DISCOVERY, {})
        template = templates.get(template_key, templates.get("found_treasure"))

        title = template["title"].format(item=item_name)
        content = template["template"].format(item=item_name)

        entry = self.add_entry(
            DiaryEntryType.DISCOVERY,
            title,
            content,
            mood="excited",
            tags=["discovery", "rare" if is_rare else "common"],
        )

        if is_rare:
            entry.is_favorite = True

        return entry

    def record_visitor(self, visitor_name: str, gift: Optional[str] = None) -> DiaryEntry:
        """Record a visitor event."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.VISITOR, {})

        if gift:
            template = templates["visitor_gift"]
            content = template["template"].format(visitor_name=visitor_name, gift=gift)
            title = template["title"]
        else:
            template = templates["visitor_came"]
            content = template["template"].format(visitor_name=visitor_name)
            title = template["title"]

        return self.add_entry(
            DiaryEntryType.VISITOR,
            title,
            content,
            mood="friendly",
            tags=["visitor", visitor_name.lower().replace(" ", "_")],
        )

    def record_feeling(self, feeling_type: str = None) -> Optional[DiaryEntry]:
        """Record a random feeling/reflection entry."""
        templates = ENTRY_TEMPLATES.get(DiaryEntryType.FEELING, {})

        if feeling_type and feeling_type in templates:
            template = templates[feeling_type]
        else:
            feeling_type = random.choice(list(templates.keys()))
            template = templates[feeling_type]

        return self.add_entry(
            DiaryEntryType.FEELING,
            template["title"],
            template["template"],
            mood=feeling_type,
            tags=["feeling", feeling_type],
        )

    def record_random_memory(self) -> Optional[DiaryEntry]:
        """Record a random sweet memory (call occasionally)."""
        if random.random() > 0.3:  # 30% chance to record
            return None

        templates = ENTRY_TEMPLATES.get(DiaryEntryType.MEMORY, {})
        memory_type = random.choice(list(templates.keys()))
        template = templates[memory_type]

        return self.add_entry(
            DiaryEntryType.MEMORY,
            template["title"],
            template["template"],
            mood="content",
            tags=["memory", memory_type],
        )

    def increase_relationship(self, amount: int = 1) -> Optional[Tuple[int, str]]:
        """
        Increase relationship score.
        Returns (new_level, level_name) if level changed, None otherwise.
        """
        self.relationship_score += amount
        self.total_interactions += 1

        # Check for level up
        for level, data in sorted(RELATIONSHIP_LEVELS.items(), reverse=True):
            if self.relationship_score >= data["threshold"]:
                if level > self.current_relationship_level:
                    self.current_relationship_level = level

                    # Record relationship milestone
                    if level == 5:
                        self.record_relationship_change("best_friends")
                    elif level == 6:
                        self.record_relationship_change("bonded")

                    return (level, data["name"])
                break

        return None

    def get_relationship_info(self) -> Dict:
        """Get current relationship status."""
        level_data = RELATIONSHIP_LEVELS.get(self.current_relationship_level, RELATIONSHIP_LEVELS[0])
        next_level = self.current_relationship_level + 1

        progress = 0
        if next_level in RELATIONSHIP_LEVELS:
            current_threshold = level_data["threshold"]
            next_threshold = RELATIONSHIP_LEVELS[next_level]["threshold"]
            if next_threshold > current_threshold:
                progress = ((self.relationship_score - current_threshold) /
                           (next_threshold - current_threshold)) * 100

        return {
            "level": self.current_relationship_level,
            "name": level_data["name"],
            "description": level_data["description"],
            "score": self.relationship_score,
            "progress_to_next": min(100, progress),
            "total_interactions": self.total_interactions,
        }

    def get_recent_entries(self, count: int = 10) -> List[DiaryEntry]:
        """Get most recent diary entries."""
        return sorted(self.entries, key=lambda e: e.date, reverse=True)[:count]

    def get_favorite_entries(self) -> List[DiaryEntry]:
        """Get all favorite entries."""
        return [e for e in self.entries if e.is_favorite]

    def get_entries_by_type(self, entry_type: DiaryEntryType) -> List[DiaryEntry]:
        """Get entries of a specific type."""
        return [e for e in self.entries if e.entry_type == entry_type]

    def toggle_favorite(self, entry_id: str) -> bool:
        """Toggle favorite status of an entry."""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                entry.is_favorite = not entry.is_favorite
                return entry.is_favorite
        return False

    def get_stats(self) -> Dict:
        """Get diary statistics."""
        return {
            "total_entries": len(self.entries),
            "favorites": len([e for e in self.entries if e.is_favorite]),
            "milestones": len([e for e in self.entries if e.entry_type == DiaryEntryType.MILESTONE]),
            "adventures": len([e for e in self.entries if e.entry_type == DiaryEntryType.ADVENTURE]),
            "days_documented": self._get_duck_age_days(),
            "relationship_level": self.current_relationship_level,
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "entries": [
                {
                    "entry_id": e.entry_id,
                    "entry_type": e.entry_type.value,
                    "date": e.date,
                    "title": e.title,
                    "content": e.content,
                    "mood_at_time": e.mood_at_time,
                    "duck_age_days": e.duck_age_days,
                    "is_favorite": e.is_favorite,
                    "tags": e.tags,
                }
                for e in self.entries
            ],
            "relationship_score": self.relationship_score,
            "current_relationship_level": self.current_relationship_level,
            "milestones_recorded": self.milestones_recorded,
            "first_entry_date": self.first_entry_date,
            "total_interactions": self.total_interactions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DuckDiary":
        """Create from dictionary."""
        diary = cls()
        diary.relationship_score = data.get("relationship_score", 0)
        diary.current_relationship_level = data.get("current_relationship_level", 0)
        diary.milestones_recorded = data.get("milestones_recorded", [])
        diary.first_entry_date = data.get("first_entry_date")
        diary.total_interactions = data.get("total_interactions", 0)

        for e_data in data.get("entries", []):
            try:
                entry = DiaryEntry(
                    entry_id=e_data["entry_id"],
                    entry_type=DiaryEntryType(e_data["entry_type"]),
                    date=e_data["date"],
                    title=e_data["title"],
                    content=e_data["content"],
                    mood_at_time=e_data.get("mood_at_time", "happy"),
                    duck_age_days=e_data.get("duck_age_days", 0),
                    is_favorite=e_data.get("is_favorite", False),
                    tags=e_data.get("tags", []),
                )
                diary.entries.append(entry)
            except (KeyError, TypeError, ValueError):
                continue

        return diary


# Lazy singleton pattern with thread-safe initialization
_duck_diary: Optional[DuckDiary] = None
_duck_diary_lock = threading.Lock()


def get_duck_diary() -> DuckDiary:
    """Get the global duck diary instance (lazy initialization). Thread-safe."""
    global _duck_diary
    if _duck_diary is None:
        with _duck_diary_lock:
            if _duck_diary is None:
                _duck_diary = DuckDiary()
    return _duck_diary


# Direct instance for backwards compatibility
duck_diary = DuckDiary()
