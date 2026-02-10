"""
Area-specific random events for Cheese the Duck.

150+ bespoke events tied to specific exploration areas, plus a spontaneous
travel system where Cheese occasionally wanders off to a different unlocked area.

Each area (22 total across 9 biomes) gets 6-8 unique events with Cheese's
signature deadpan commentary. Events have effects, animations, and cooldowns.
"""
import random
import time
from typing import Dict, List, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from duck.duck import Duck


@dataclass
class AreaEvent:
    """An event specific to a location."""
    id: str
    area: str              # Area name (must match exploration.py area names)
    name: str
    message: str           # Cheese's deadpan comment
    effects: Dict[str, float]
    mood_change: int
    probability: float     # 0.0 to 1.0 per check
    cooldown: float = 600  # seconds
    has_animation: bool = False
    animation_id: Optional[str] = None  # Key into the animation factory
    sound: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════
# AREA EVENTS — 22 areas × ~7 events each = 154 events
# ═══════════════════════════════════════════════════════════════════════════

AREA_EVENTS: Dict[str, List[AreaEvent]] = {

    # ─── POND BIOME ──────────────────────────────────────────────────────

    "Home Pond": [
        AreaEvent(
            id="hp_lily_pad_throne", area="Home Pond",
            name="Lily Pad Throne",
            message="*climbs onto lily pad* This is my throne. The pond is my kingdom. "
                    "Population: me. Subjects: fish. They don't know they're subjects yet.",
            effects={"fun": 8, "energy": 5}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="lily_pad",
        ),
        AreaEvent(
            id="hp_fish_staring", area="Home Pond",
            name="Fish Staring Contest",
            message="*stares into water* There's a fish down there. We've been staring at each other "
                    "for three minutes. It blinked. I win. Again.",
            effects={"fun": 5}, mood_change=4, probability=0.05,
        ),
        AreaEvent(
            id="hp_perfect_ripple", area="Home Pond",
            name="Perfect Ripple",
            message="*dips beak* ...Did you SEE that ripple? Perfect circle. I should be a physicist. "
                    "Or a professional ripple maker. Is that a job? It should be.",
            effects={"fun": 10}, mood_change=7, probability=0.03,
            has_animation=True, animation_id="ripple",
        ),
        AreaEvent(
            id="hp_frog_debate", area="Home Pond",
            name="Frog Debate",
            message="*addresses frog* Your croaking technique is AMATEUR at best. "
                    "My quack has LAYERS. Emotional DEPTH. "
                    "...The frog left. I win by default.",
            effects={"social": 8, "fun": 5}, mood_change=5, probability=0.04,
            has_animation=True, animation_id="frog_hop",
        ),
        AreaEvent(
            id="hp_algae_snack", area="Home Pond",
            name="Mystery Algae",
            message="*nibbles algae* ...This tastes like regret and pond water. "
                    "So, exactly what I expected. I'll have more.",
            effects={"hunger": 8, "cleanliness": -5}, mood_change=2, probability=0.05,
            sound="eat",
        ),
        AreaEvent(
            id="hp_dragonfly_buzz", area="Home Pond",
            name="Dragonfly Encounter",
            message="*watches dragonfly* It's just... hovering there. Menacingly. "
                    "I respect the power move but this is MY airspace.",
            effects={"fun": 6}, mood_change=3, probability=0.04,
            has_animation=True, animation_id="dragonfly",
        ),
        AreaEvent(
            id="hp_old_bread", area="Home Pond",
            name="Ancient Bread Discovery",
            message="*finds bread at bottom* This bread has been here since before I was born. "
                    "It's basically an artifact. A soggy, disappointing artifact. "
                    "I ate it anyway.",
            effects={"hunger": 12, "cleanliness": -3}, mood_change=4, probability=0.03,
            sound="eat",
        ),
    ],

    "Deep End": [
        AreaEvent(
            id="de_dark_below", area="Deep End",
            name="The Dark Below",
            message="*peers into depths* ...Something moved down there. Something BIG. "
                    "I'm not scared. I just prefer the shallow end. Strategically.",
            effects={"fun": -3, "energy": -2}, mood_change=-4, probability=0.04,
        ),
        AreaEvent(
            id="de_bubble_discovery", area="Deep End",
            name="Bubble Discovery",
            message="*finds bubble stream* Bubbles! Coming from nowhere! "
                    "Either the pond is breathing or there's a fish down there having a party "
                    "I wasn't invited to. Rude.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="bubbles",
        ),
        AreaEvent(
            id="de_cold_current", area="Deep End",
            name="Cold Current",
            message="*shivers* Cold spot. COLD SPOT. My feathers just filed a complaint. "
                    "This is unauthorized temperature change.",
            effects={"energy": -5, "cleanliness": 5}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="de_lost_coin", area="Deep End",
            name="Lost Coin",
            message="*finds coin on bottom* Someone's wish didn't come true. "
                    "Their loss. My coin now. I wish for more coins.",
            effects={"fun": 15}, mood_change=8, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="de_big_fish", area="Deep End",
            name="Big Fish Sighting",
            message="*freezes* That fish is bigger than me. BIGGER. THAN. ME. "
                    "We made eye contact. I'm going to pretend that didn't happen.",
            effects={"fun": -5, "energy": 5}, mood_change=-2, probability=0.03,
        ),
        AreaEvent(
            id="de_echo_quack", area="Deep End",
            name="Echo Quack",
            message="QUACK! ...quack... ...quack... My quack echoes down here. "
                    "I sound even more impressive than usual. Which is saying something.",
            effects={"fun": 8, "social": 3}, mood_change=5, probability=0.04,
            sound="quack",
        ),
        AreaEvent(
            id="de_underwater_plant", area="Deep End",
            name="Weird Plant",
            message="*inspects plant* This plant is just... waving at me. Underwater. "
                    "No wind. Just vibes. I respect it.",
            effects={"fun": 4}, mood_change=3, probability=0.05,
        ),
    ],

    # ─── FOREST BIOME ────────────────────────────────────────────────────

    "Forest Edge": [
        AreaEvent(
            id="fe_stick_find", area="Forest Edge",
            name="Perfect Stick",
            message="*finds stick* This is the perfect stick. Every duck dreams of a stick like this. "
                    "You wouldn't understand. It's a duck thing.",
            effects={"fun": 12}, mood_change=8, probability=0.04,
        ),
        AreaEvent(
            id="fe_pinecone_ambush", area="Forest Edge",
            name="Pinecone Ambush",
            message="*gets hit by pinecone* OW. The TREES are attacking me. "
                    "I KNEW they couldn't be trusted. Tall, silent, suspicious.",
            effects={"fun": -5, "energy": -3}, mood_change=-4, probability=0.04,
            has_animation=True, animation_id="falling_object",
        ),
        AreaEvent(
            id="fe_squirrel_standoff", area="Forest Edge",
            name="Squirrel Standoff",
            message="*locks eyes with squirrel* ...You think you're better than me? "
                    "With your fluffy tail and your ACORN HOARDING? "
                    "This forest isn't big enough for both of us.",
            effects={"fun": 6, "social": 5}, mood_change=4, probability=0.04,
            has_animation=True, animation_id="squirrel",
        ),
        AreaEvent(
            id="fe_leaf_pile", area="Forest Edge",
            name="Leaf Pile",
            message="*dives into leaves* WHOOSH! Leaf pile! Best thing about autumn! "
                    "...I have a leaf in my beak. I'm keeping it.",
            effects={"fun": 15, "cleanliness": -8}, mood_change=8, probability=0.03,
            has_animation=True, animation_id="nice_breeze",
        ),
        AreaEvent(
            id="fe_spider_web", area="Forest Edge",
            name="Spider Web",
            message="*walks into web* AUGH! Web! WEB ON MY FACE! "
                    "Spider, wherever you are, this means WAR.",
            effects={"fun": -8, "cleanliness": -5}, mood_change=-6, probability=0.04,
        ),
        AreaEvent(
            id="fe_mushroom_ring", area="Forest Edge",
            name="Fairy Ring",
            message="*finds mushroom circle* ...The mushrooms are in a circle. "
                    "That's either magical or concerning. I'm going to stand in the middle. "
                    "For science.",
            effects={"fun": 10}, mood_change=6, probability=0.02,
        ),
        AreaEvent(
            id="fe_bird_song", area="Forest Edge",
            name="Bird Song",
            message="*hears singing* A bird is singing. It's... okay. "
                    "Not as good as my quacking. But okay. "
                    "I'll allow it. This time.",
            effects={"fun": 5, "social": 3}, mood_change=4, probability=0.05,
            has_animation=True, animation_id="bird_friend",
        ),
    ],

    "Ancient Oak": [
        AreaEvent(
            id="ao_acorn_rain", area="Ancient Oak",
            name="Acorn Rain",
            message="*acorns falling* The oak is BOMBING me! Tiny wooden grenades! "
                    "I didn't even DO anything to this tree! ...Recently!",
            effects={"fun": -3, "energy": -2}, mood_change=-3, probability=0.05,
            has_animation=True, animation_id="falling_object",
        ),
        AreaEvent(
            id="ao_owl_stare", area="Ancient Oak",
            name="Owl Stare",
            message="*looks up* There's an owl staring at me. Just... staring. "
                    "We've been doing this for five minutes. "
                    "I think it's judging me. Fair enough.",
            effects={"social": 5}, mood_change=2, probability=0.04,
        ),
        AreaEvent(
            id="ao_tree_hollow", area="Ancient Oak",
            name="Tree Hollow",
            message="*finds hollow* There's a tiny room inside this tree. "
                    "WITH FURNITURE. Acorn furniture. Someone LIVES here. "
                    "I'm leaving before they charge rent.",
            effects={"fun": 12}, mood_change=7, probability=0.03,
        ),
        AreaEvent(
            id="ao_bark_reading", area="Ancient Oak",
            name="Bark Reading",
            message="*examines bark* Someone carved 'J + M' in this bark. "
                    "Amateurs. I carved 'CHEESE WAS HERE' three trees over. Much better.",
            effects={"fun": 6}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="ao_woodpecker", area="Ancient Oak",
            name="Woodpecker Noise",
            message="*cringe* That woodpecker has been going for twenty minutes. "
                    "TWENTY. MINUTES. My head hurts in sympathy. "
                    "How does it not have a concussion?",
            effects={"fun": -4, "energy": -3}, mood_change=-3, probability=0.04,
            has_animation=True, animation_id="bird_friend",
        ),
        AreaEvent(
            id="ao_ancient_wisdom", area="Ancient Oak",
            name="Ancient Wisdom",
            message="*sits under tree* This tree is probably a thousand years old. "
                    "It's seen everything. Wars. Love. Weather. "
                    "...And now it's seen a duck sitting under it. Lucky tree.",
            effects={"fun": 5, "energy": 8}, mood_change=6, probability=0.03,
        ),
        AreaEvent(
            id="ao_caterpillar", area="Ancient Oak",
            name="Caterpillar Chat",
            message="*watches caterpillar* You're going to be a butterfly someday? "
                    "That's... ambitious. I'm already perfect. No transformation needed.",
            effects={"fun": 6, "social": 3}, mood_change=4, probability=0.04,
        ),
    ],

    "Mushroom Grove": [
        AreaEvent(
            id="mg_glowing_mushroom", area="Mushroom Grove",
            name="Glowing Mushroom",
            message="*stares* This mushroom is GLOWING. Either it's magical or radioactive. "
                    "Both options are equally exciting and terrifying.",
            effects={"fun": 12}, mood_change=7, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="mg_spore_cloud", area="Mushroom Grove",
            name="Spore Cloud",
            message="*walks through spores* PFFT— *cough* WHO AUTHORIZED THIS DUST? "
                    "The mushrooms are GASSING me! This is biological warfare!",
            effects={"cleanliness": -10, "energy": -5}, mood_change=-5, probability=0.05,
        ),
        AreaEvent(
            id="mg_tiny_door", area="Mushroom Grove",
            name="Tiny Door",
            message="*finds tiny door in mushroom* ...There's a door. In the mushroom. "
                    "A TINY door. I'm too big to fit. This is discrimination.",
            effects={"fun": 15}, mood_change=8, probability=0.02,
        ),
        AreaEvent(
            id="mg_slug_race", area="Mushroom Grove",
            name="Slug Race",
            message="*watches slugs* Two slugs. Racing. I've been watching for ten minutes. "
                    "They've moved half an inch. This is the most riveting thing I've ever seen.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="mg_mushroom_bounce", area="Mushroom Grove",
            name="Mushroom Bounce",
            message="*jumps on mushroom* BOING! It's bouncy! BOING BOING! "
                    "...I'm going to pretend I'm too dignified for this. *boing*",
            effects={"fun": 15, "energy": -5}, mood_change=9, probability=0.03,
        ),
        AreaEvent(
            id="mg_beetle_parade", area="Mushroom Grove",
            name="Beetle Parade",
            message="*watches beetles march* They're marching. In formation. "
                    "They have better discipline than most armies. "
                    "I'm both impressed and slightly threatened.",
            effects={"fun": 7}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="mg_weird_smell", area="Mushroom Grove",
            name="Mysterious Aroma",
            message="*sniffs* Something smells like... old cheese? In a mushroom grove? "
                    "Wait. Is there another Cheese here? IMPOSTER!",
            effects={"fun": 5, "hunger": -3}, mood_change=2, probability=0.05,
        ),
    ],

    # ─── MEADOW BIOME ────────────────────────────────────────────────────

    "Sunny Meadow": [
        AreaEvent(
            id="sm_flower_crown", area="Sunny Meadow",
            name="Flower Crown",
            message="*wearing flowers* A flower landed on my head. I'm leaving it there. "
                    "I am now royalty. Address me accordingly.",
            effects={"fun": 12, "social": 5}, mood_change=8, probability=0.03,
        ),
        AreaEvent(
            id="sm_bee_chase", area="Sunny Meadow",
            name="Bee Chase",
            message="*runs* BEE! BEE! BIG BEE! I didn't DO anything! "
                    "I was just STANDING here! Being BEAUTIFUL! "
                    "IS THAT A CRIME?!",
            effects={"fun": -5, "energy": -8}, mood_change=-6, probability=0.04,
            has_animation=True, animation_id="dragonfly",
        ),
        AreaEvent(
            id="sm_grass_whistle", area="Sunny Meadow",
            name="Grass Whistle",
            message="*holds grass between wings* FFFTTT— ...That's not a whistle. "
                    "That's just air. Through grass. "
                    "I'm going back to quacking. At least that works.",
            effects={"fun": 6}, mood_change=3, probability=0.05,
        ),
        AreaEvent(
            id="sm_sunbathing", area="Sunny Meadow",
            name="Premium Sunbathing",
            message="*flops in sun* This is it. This is the spot. Perfect sun angle. "
                    "Perfect grass softness. I'm never moving. Cancel everything.",
            effects={"energy": 12, "fun": 8}, mood_change=8, probability=0.04,
        ),
        AreaEvent(
            id="sm_dandelion_wish", area="Sunny Meadow",
            name="Dandelion Wish",
            message="*blows dandelion* I wish for... no. That's between me and the dandelion. "
                    "It was definitely something cool though. Definitely not bread.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
            has_animation=True, animation_id="nice_breeze",
        ),
        AreaEvent(
            id="sm_grasshopper", area="Sunny Meadow",
            name="Grasshopper Leap",
            message="*watches grasshopper* It jumped THAT high?! With THOSE legs?! "
                    "I refuse to be outdone by an insect. *attempts jump* "
                    "...We don't talk about what just happened.",
            effects={"fun": 8, "energy": -3}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="sm_warm_rock", area="Sunny Meadow",
            name="Warm Rock",
            message="*sits on rock* This rock is warm. From the sun. "
                    "It's like a tiny heated seat. Nature's furniture. "
                    "I'm claiming this rock. It's mine now.",
            effects={"energy": 10, "fun": 5}, mood_change=6, probability=0.04,
        ),
    ],

    "Butterfly Garden": [
        AreaEvent(
            id="bg_butterfly_landing", area="Butterfly Garden",
            name="Butterfly Landing",
            message="*a butterfly lands on beak* ...Don't. Move. This is the greatest honor. "
                    "A butterfly CHOSE me. Me specifically. Obviously.",
            effects={"fun": 15, "social": 8}, mood_change=10, probability=0.04,
            has_animation=True, animation_id="butterfly",
        ),
        AreaEvent(
            id="bg_color_explosion", area="Butterfly Garden",
            name="Color Explosion",
            message="*looks around* Every direction, just... colors. Flapping colors. "
                    "I don't have the emotional range for this. ...It's nice. FINE. It's nice.",
            effects={"fun": 12}, mood_change=8, probability=0.04,
        ),
        AreaEvent(
            id="bg_nectar_taste", area="Butterfly Garden",
            name="Nectar Tasting",
            message="*licks flower* ...Sweet. Really sweet. I can see why the butterflies are obsessed. "
                    "I'm not obsessed. I'm just... researching. *licks again*",
            effects={"hunger": 5, "fun": 8}, mood_change=5, probability=0.05,
        ),
        AreaEvent(
            id="bg_cocoon_watch", area="Butterfly Garden",
            name="Cocoon Watch",
            message="*stares at cocoon* Someone's in there. Just... becoming beautiful. "
                    "What a flex. I didn't need a cocoon. I was born this way.",
            effects={"fun": 6}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="bg_flower_maze", area="Butterfly Garden",
            name="Flower Maze",
            message="*surrounded by flowers* I'm lost. In a garden. The flowers are taller than me. "
                    "This is humiliating. Don't tell anyone.",
            effects={"fun": 5, "energy": -3}, mood_change=2, probability=0.04,
        ),
        AreaEvent(
            id="bg_hummingbird", area="Butterfly Garden",
            name="Hummingbird Encounter",
            message="*watches hummingbird* It's just... hovering. Wings going at 900mph. "
                    "Show-off. I could do that if I wanted to. I just don't want to.",
            effects={"fun": 8, "social": 3}, mood_change=5, probability=0.03,
        ),
        AreaEvent(
            id="bg_pollen_sneeze", area="Butterfly Garden",
            name="Pollen Sneeze",
            message="*sneezes violently* AQCK— The flowers are ATTACKING! "
                    "With INVISIBLE DUST! This is a trap! A beautiful, fragrant trap!",
            effects={"fun": -3, "cleanliness": -5}, mood_change=-3, probability=0.05,
        ),
    ],

    # ─── RIVERSIDE BIOME ─────────────────────────────────────────────────

    "Pebble Beach": [
        AreaEvent(
            id="pb_flat_pebble", area="Pebble Beach",
            name="Skipping Stone",
            message="*finds flat pebble* This is a PERFECT skipping stone. "
                    "Three skips. Maybe four. *throws* ...It sank immediately. "
                    "The river is wrong. Not me.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="pb_crayfish", area="Pebble Beach",
            name="Crayfish Encounter",
            message="*gets pinched* OW! A crayfish! With ATTITUDE! "
                    "Listen here you tiny lobster, I am a DUCK. I outrank you. "
                    "OW! IT DID IT AGAIN!",
            effects={"fun": -5, "energy": -3}, mood_change=-4, probability=0.04,
        ),
        AreaEvent(
            id="pb_bottle_message", area="Pebble Beach",
            name="Message in Bottle",
            message="*finds bottle* A message in a bottle! It says... 'Help, I'm stuck on an island.' "
                    "Hmm. Sounds like a them problem. Cool bottle though.",
            effects={"fun": 12}, mood_change=7, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="pb_pebble_stack", area="Pebble Beach",
            name="Pebble Stack",
            message="*stacks pebbles* One... two... three... FOUR! New record! "
                    "*wind blows them over* ...I'm going to fight the wind.",
            effects={"fun": 8, "energy": -3}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="pb_splash_contest", area="Pebble Beach",
            name="Splash Contest",
            message="*does cannonball* SPLASH! Biggest splash on this beach! "
                    "There's no competition because I'm the only one here. Undefeated!",
            effects={"fun": 12, "cleanliness": 8}, mood_change=7, probability=0.04,
            sound="splash",
        ),
        AreaEvent(
            id="pb_sand_pattern", area="Pebble Beach",
            name="Sand Art",
            message="*draws in sand* I'm making a self-portrait. In sand. "
                    "It's beautiful. ...It looks like a circle with a line. "
                    "That's what I look like. Deal with it.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="pb_current_ride", area="Pebble Beach",
            name="River Ride",
            message="*floats downstream* Wheeeee— wait where am I going. "
                    "WHERE AM I GOING. *paddles back* ...Scenic route. Planned it.",
            effects={"fun": 10, "energy": -5}, mood_change=6, probability=0.03,
        ),
    ],

    "Waterfall": [
        AreaEvent(
            id="wf_mist_bath", area="Waterfall",
            name="Mist Bath",
            message="*stands in mist* Free spa treatment. The waterfall just... sprays you. "
                    "No appointment needed. Five stars.",
            effects={"cleanliness": 15, "energy": 5}, mood_change=7, probability=0.04,
        ),
        AreaEvent(
            id="wf_rainbow_spot", area="Waterfall",
            name="Rainbow Sighting",
            message="*gasps* A rainbow. In the mist. I'm standing IN a rainbow. "
                    "I'm basically a unicorn right now. A duck unicorn. A duckcorn.",
            effects={"fun": 18}, mood_change=10, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="wf_roar_meditation", area="Waterfall",
            name="Waterfall Meditation",
            message="*sits by waterfall* The sound is... actually peaceful. "
                    "I'm going to meditate. *closes eyes* ...I'm thinking about bread. "
                    "That counts as meditation.",
            effects={"energy": 12, "fun": 5}, mood_change=7, probability=0.04,
        ),
        AreaEvent(
            id="wf_slippery_rocks", area="Waterfall",
            name="Slippery Rocks",
            message="*slips* WHOAAA— *catches self* I MEANT to do that. "
                    "That was a DANCE MOVE. A very advanced one.",
            effects={"fun": -3, "energy": -5}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="wf_hidden_cave", area="Waterfall",
            name="Hidden Cave",
            message="*finds cave behind waterfall* A CAVE! Behind the waterfall! "
                    "Just like in movies! It's dark and wet and— actually this is just a wet hole. "
                    "Still cool though.",
            effects={"fun": 15}, mood_change=8, probability=0.02,
        ),
        AreaEvent(
            id="wf_salmon_jump", area="Waterfall",
            name="Salmon Leap",
            message="*watches salmon* That fish just JUMPED up the waterfall. "
                    "The ENTIRE waterfall. Show-off. I could do that. I just... choose not to.",
            effects={"fun": 8, "social": 3}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="wf_drenched", area="Waterfall",
            name="Completely Drenched",
            message="*soaked through* I got too close to the waterfall. I look like a drowned— "
                    "I look like a WET duck. Which is normal. For a duck. This is fine.",
            effects={"cleanliness": 12, "energy": -3}, mood_change=1, probability=0.05,
        ),
    ],

    # ─── GARDEN BIOME ────────────────────────────────────────────────────

    "Vegetable Patch": [
        AreaEvent(
            id="vp_tomato_accident", area="Vegetable Patch",
            name="Tomato Incident",
            message="*tomato falls on head* ...Did that tomato just ATTACK me? "
                    "From the VINE? I've been assassinated by produce.",
            effects={"fun": -3, "cleanliness": -8}, mood_change=-3, probability=0.04,
            has_animation=True, animation_id="falling_object",
        ),
        AreaEvent(
            id="vp_carrot_pull", area="Vegetable Patch",
            name="Carrot Discovery",
            message="*pulls carrot* It's HUGE! This carrot is bigger than my head! "
                    "I don't even like carrots but THIS one is mine now.",
            effects={"hunger": 10, "fun": 8}, mood_change=6, probability=0.04,
            sound="eat",
        ),
        AreaEvent(
            id="vp_scarecrow_stare", area="Vegetable Patch",
            name="Scarecrow Standoff",
            message="*stares at scarecrow* ...Is that thing LOOKING at me? "
                    "It's stuffed with straw. It can't look at me. "
                    "...IT MOVED. I saw it. Maybe.",
            effects={"fun": 5}, mood_change=2, probability=0.05,
        ),
        AreaEvent(
            id="vp_earthworm_feast", area="Vegetable Patch",
            name="Worm Bonanza",
            message="*digs* WORMS! SO MANY WORMS! This is like a buffet! "
                    "An all-you-can-eat DIRT buffet! Christmas came early!",
            effects={"hunger": 15, "fun": 10}, mood_change=8, probability=0.03,
            sound="eat",
        ),
        AreaEvent(
            id="vp_sprinkler_surprise", area="Vegetable Patch",
            name="Sprinkler Surprise",
            message="*gets sprayed* THE GARDEN IS FIGHTING BACK! "
                    "Automated water assault! I— okay this is actually refreshing.",
            effects={"cleanliness": 12, "fun": 8}, mood_change=5, probability=0.04,
            sound="splash",
        ),
        AreaEvent(
            id="vp_lettuce_bed", area="Vegetable Patch",
            name="Lettuce Bed",
            message="*lies on lettuce* This lettuce is the perfect bed. "
                    "Soft. Green. Slightly wet. I'm a salad now. A happy salad.",
            effects={"energy": 8, "fun": 5}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="vp_garden_gnome", area="Vegetable Patch",
            name="Garden Gnome Encounter",
            message="*stares at gnome* Why is this tiny man SMILING at me? "
                    "In MY garden? With that BEARD? ...I don't trust him. "
                    "But I respect the hat.",
            effects={"fun": 6}, mood_change=3, probability=0.05,
        ),
    ],

    "Tool Shed": [
        AreaEvent(
            id="ts_cobweb_face", area="Tool Shed",
            name="Cobweb Face",
            message="*walks into cobweb* EVERY. SINGLE. TIME. "
                    "This shed is BOOBY TRAPPED. By SPIDERS.",
            effects={"fun": -5, "cleanliness": -8}, mood_change=-5, probability=0.05,
        ),
        AreaEvent(
            id="ts_shiny_tools", area="Tool Shed",
            name="Shiny Tools",
            message="*admires tools* So many shiny things! I don't know what any of them DO "
                    "but I want ALL of them. That wrench is BEAUTIFUL.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="ts_paint_can", area="Tool Shed",
            name="Paint Can Discovery",
            message="*finds paint* There's paint in here. I could paint something. "
                    "Like the shed. Or myself. Or your screen. Don't tempt me.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="ts_mouse_friend", area="Tool Shed",
            name="Shed Mouse",
            message="*sees mouse* A mouse! Living in the shed! It has a whole SETUP. "
                    "Tiny bed. Tiny food stash. I'm not jealous. ...Okay I'm a little jealous.",
            effects={"social": 8, "fun": 6}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="ts_old_radio", area="Tool Shed",
            name="Old Radio",
            message="*finds radio* It's playing static. Very atmospheric. "
                    "I feel like I'm in a horror movie. Except I'm the monster. "
                    "QUACK. Terrifying.",
            effects={"fun": 6}, mood_change=3, probability=0.04,
        ),
        AreaEvent(
            id="ts_nap_spot", area="Tool Shed",
            name="Cozy Corner",
            message="*finds blanket pile* Someone left blankets in here. "
                    "On a shelf. At perfect duck height. "
                    "I'm choosing to believe this was left FOR me.",
            effects={"energy": 12, "fun": 5}, mood_change=6, probability=0.03,
        ),
        AreaEvent(
            id="ts_pot_crash", area="Tool Shed",
            name="Pot Crash",
            message="*knocks over flower pot* CRASH! ...That was there when I got here. "
                    "I saw nothing. You saw nothing.",
            effects={"fun": -3}, mood_change=-2, probability=0.05,
            has_animation=True, animation_id="loud_noise",
        ),
    ],

    # ─── MOUNTAINS BIOME ─────────────────────────────────────────────────

    "Foothills": [
        AreaEvent(
            id="fh_echo_valley", area="Foothills",
            name="Echo Valley",
            message="QUAAAACK! ...quaaack... ...quack... "
                    "I just had a conversation with a mountain. It agrees with everything I say.",
            effects={"fun": 10, "social": 5}, mood_change=7, probability=0.04,
            sound="quack",
        ),
        AreaEvent(
            id="fh_mountain_goat", area="Foothills",
            name="Mountain Goat",
            message="*sees goat on cliff* How did you GET up there? "
                    "You have HOOVES. That cliff is VERTICAL. "
                    "I refuse to be impressed. *is impressed*",
            effects={"fun": 8, "social": 3}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="fh_altitude_drama", area="Foothills",
            name="Altitude Drama",
            message="*panting* We're so... high up... the air is... thin... "
                    "...We're twelve feet above sea level. But still.",
            effects={"energy": -5}, mood_change=-2, probability=0.05,
        ),
        AreaEvent(
            id="fh_rock_slide", area="Foothills",
            name="Tiny Rockslide",
            message="*pebbles tumble* ROCKSLIDE! EVERY DUCK FOR THEMSELVES! "
                    "*three pebbles roll past* ...Okay it was small. "
                    "But my reaction was APPROPRIATE.",
            effects={"fun": -3, "energy": -3}, mood_change=-3, probability=0.04,
            has_animation=True, animation_id="falling_object",
        ),
        AreaEvent(
            id="fh_cool_rock", area="Foothills",
            name="Geologically Interesting Rock",
            message="*examines rock* This rock has LAYERS. Like an onion. "
                    "Or a cake. ...Now I want cake. Why did the rock do this to me.",
            effects={"fun": 6}, mood_change=4, probability=0.05,
        ),
        AreaEvent(
            id="fh_mountain_view", area="Foothills",
            name="Mountain Vista",
            message="*looks at view* ...Okay. This is... actually beautiful. "
                    "I can see the pond from here. It looks so small. "
                    "Everything looks small when you're this awesome.",
            effects={"fun": 12, "energy": 5}, mood_change=8, probability=0.03,
        ),
        AreaEvent(
            id="fh_wild_berries", area="Foothills",
            name="Wild Berries",
            message="*finds berries* Mountain berries! They taste like... effort. "
                    "And altitude. And purple. I'm having more.",
            effects={"hunger": 10, "fun": 5}, mood_change=5, probability=0.04,
            sound="eat",
        ),
    ],

    "Crystal Cave": [
        AreaEvent(
            id="cc_sparkle_ceiling", area="Crystal Cave",
            name="Sparkle Ceiling",
            message="*looks up* The ceiling is SPARKLING. Like tiny stars. Underground. "
                    "This is the fanciest cave I've ever been in. "
                    "...It's the ONLY cave I've been in. Still fancy.",
            effects={"fun": 15}, mood_change=9, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="cc_crystal_hum", area="Crystal Cave",
            name="Crystal Hum",
            message="*listens* The crystals are... humming. They're SINGING to me. "
                    "Not well. But they're trying. I appreciate the effort.",
            effects={"fun": 10, "energy": 5}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="cc_reflection", area="Crystal Cave",
            name="Crystal Mirror",
            message="*sees reflection* OH— it's me. In the crystal. "
                    "Looking extremely handsome. As expected. "
                    "This cave has excellent taste.",
            effects={"fun": 12, "social": 3}, mood_change=7, probability=0.04,
        ),
        AreaEvent(
            id="cc_dark_passage", area="Crystal Cave",
            name="Dark Passage",
            message="*peers into darkness* There's a passage going deeper. "
                    "Into darkness. Where no light reaches. "
                    "I'm going to not go there. Today. Maybe tomorrow. Probably not.",
            effects={"fun": -3}, mood_change=-2, probability=0.05,
        ),
        AreaEvent(
            id="cc_bat_colony", area="Crystal Cave",
            name="Bat Colony",
            message="*bats fly past* AAAA— I mean. Hello, bats. Fellow flying creatures. "
                    "...I can fly too, you know. I just CHOOSE to waddle.",
            effects={"fun": -5, "energy": -3}, mood_change=-4, probability=0.04,
        ),
        AreaEvent(
            id="cc_dripping_water", area="Crystal Cave",
            name="Cave Drip",
            message="*drip* ...*drip* ...*drip* ...If that water drips on me ONE more time I'm— "
                    "*drip* ...I'm leaving. I'm LEAVING.",
            effects={"fun": -3, "cleanliness": 3}, mood_change=-2, probability=0.05,
        ),
        AreaEvent(
            id="cc_crystal_collect", area="Crystal Cave",
            name="Crystal Fragment",
            message="*picks up crystal* Mine. This is mine now. It's beautiful. "
                    "It matches my eyes. ...I don't know what color my eyes are "
                    "but I'm sure they match.",
            effects={"fun": 15}, mood_change=8, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
    ],

    # ─── BEACH BIOME ─────────────────────────────────────────────────────

    "Sandy Shore": [
        AreaEvent(
            id="ss_sandcastle", area="Sandy Shore",
            name="Sandcastle Construction",
            message="*builds sandcastle* It's a FORTRESS. With a MOAT. "
                    "No one can breach Fort Cheese. "
                    "*wave destroys it* ...The ocean has chosen war.",
            effects={"fun": 12, "energy": -5}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="ss_seagull_theft", area="Sandy Shore",
            name="Seagull Confrontation",
            message="*yells at seagull* THAT'S MY SPOT! I was SITTING there! "
                    "Seagulls have NO respect for property rights!",
            effects={"fun": -5, "social": -3}, mood_change=-4, probability=0.04,
            has_animation=True, animation_id="bird_friend",
        ),
        AreaEvent(
            id="ss_shell_collection", area="Sandy Shore",
            name="Shell Collection",
            message="*collects shells* This one's pink. This one's spirally. "
                    "This one has something LIVING in it. "
                    "I'm putting that one back.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="ss_tide_pool", area="Sandy Shore",
            name="Tide Pool Discovery",
            message="*finds tide pool* A tiny ocean! With tiny fish! And tiny crabs! "
                    "I am a GIANT to them. Fear me, tiny creatures. FEAR ME.",
            effects={"fun": 12, "social": 3}, mood_change=7, probability=0.03,
        ),
        AreaEvent(
            id="ss_buried_treasure", area="Sandy Shore",
            name="Buried Treasure",
            message="*digs in sand* I found... a bottle cap. And a wrapper. "
                    "And someone's lost flip-flop. This is either treasure or garbage. "
                    "...Treasure. Definitely treasure.",
            effects={"fun": 8}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="ss_wave_dodge", area="Sandy Shore",
            name="Wave Dodge",
            message="*running from waves* The ocean is CHASING me! "
                    "I'm a duck! I should LIKE water! But not when it's AGGRESSIVE!",
            effects={"fun": 8, "energy": -5}, mood_change=3, probability=0.05,
        ),
        AreaEvent(
            id="ss_sunset_beach", area="Sandy Shore",
            name="Beach Sunset",
            message="*watches ocean* ...The sun is setting over the water. "
                    "And I'm just... here. A duck on a beach. Watching a sunset. "
                    "This is acceptable.",
            effects={"fun": 10, "energy": 8}, mood_change=8, probability=0.03,
        ),
    ],

    "Shipwreck Cove": [
        AreaEvent(
            id="sc_pirate_hat", area="Shipwreck Cove",
            name="Pirate Hat",
            message="*finds hat* A PIRATE HAT! Captain Cheese of the High Seas! "
                    "ARRR! Surrender your bread or walk the plank! "
                    "...The plank is a twig. But still.",
            effects={"fun": 18, "social": 5}, mood_change=10, probability=0.02,
        ),
        AreaEvent(
            id="sc_anchor_discovery", area="Shipwreck Cove",
            name="Anchor Found",
            message="*finds anchor* There's an ANCHOR here. From a SHIP. "
                    "An actual ship was HERE. And crashed. "
                    "They should have hired a duck navigator.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="sc_treasure_map", area="Shipwreck Cove",
            name="Treasure Map",
            message="*finds soggy paper* Is this... a TREASURE MAP? "
                    "It says 'X marks the spot.' The X is smudged. "
                    "This is the worst treasure map ever. I love it.",
            effects={"fun": 15}, mood_change=8, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="sc_barnacle_city", area="Shipwreck Cove",
            name="Barnacle City",
            message="*inspects hull* The barnacles have built a CIVILIZATION on this wreck. "
                    "Tiny barnacle houses. Barnacle roads. A barnacle government. "
                    "I respect their commitment.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="sc_ghost_story", area="Shipwreck Cove",
            name="Spooky Noises",
            message="*hears creaking* The ship is making noises. Spooky noises. "
                    "Ghost ship noises. I'm not scared. "
                    "...I'm leaving at a NORMAL pace. Completely normal.",
            effects={"fun": -5, "energy": -3}, mood_change=-4, probability=0.04,
            has_animation=True, animation_id="loud_noise",
        ),
        AreaEvent(
            id="sc_cannon_sit", area="Shipwreck Cove",
            name="Cannon Seat",
            message="*sits in cannon* I'm in a CANNON. A real cannon! "
                    "Don't light it. Seriously. Please don't light it. "
                    "...Unless it would be really funny.",
            effects={"fun": 12}, mood_change=7, probability=0.03,
        ),
        AreaEvent(
            id="sc_sea_glass", area="Shipwreck Cove",
            name="Sea Glass",
            message="*finds sea glass* Smooth. Round. Green. The ocean made this. "
                    "The ocean is a better artist than me. I'm not bitter.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
    ],

    # ─── SWAMP BIOME ─────────────────────────────────────────────────────

    "Misty Marsh": [
        AreaEvent(
            id="mm_fog_thick", area="Misty Marsh",
            name="Lost in Fog",
            message="*can't see anything* The fog is so thick I can't see my own feet. "
                    "...Do I have feet? *looks down* Oh good. Still there.",
            effects={"fun": -3, "energy": -3}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="mm_firefly_show", area="Misty Marsh",
            name="Firefly Show",
            message="*watches fireflies* ...They're just... glowing. Flying. Glowing and flying. "
                    "Like tiny stars with ambition. I can't compete with this.",
            effects={"fun": 15}, mood_change=9, probability=0.03,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="mm_frog_chorus", area="Misty Marsh",
            name="Frog Chorus",
            message="*listening* The frogs are singing. All of them. At once. "
                    "It's either a concert or a protest. Hard to tell with frogs.",
            effects={"fun": 8, "social": 5}, mood_change=5, probability=0.04,
            has_animation=True, animation_id="frog_hop",
        ),
        AreaEvent(
            id="mm_quicksand_scare", area="Misty Marsh",
            name="Quicksand Scare",
            message="*sinking* I'M SINKING! THE MARSH IS EATING ME! "
                    "Oh wait. It's only ankle deep. But the DRAMA was real.",
            effects={"fun": -5, "energy": -5, "cleanliness": -10}, mood_change=-5, probability=0.04,
        ),
        AreaEvent(
            id="mm_swamp_gas", area="Misty Marsh",
            name="Swamp Gas",
            message="*bubble pops* ...What was THAT smell?! "
                    "The swamp just BURPED at me! How DARE—  *another bubble* "
                    "I'm leaving. With dignity. *quickly*",
            effects={"fun": -3, "cleanliness": -5}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="mm_water_lily", area="Misty Marsh",
            name="Giant Water Lily",
            message="*finds huge lily pad* This lily pad could be a BED. "
                    "A floating bed. In a swamp. ...This is either genius or a terrible idea.",
            effects={"fun": 10, "energy": 5}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="lily_pad",
        ),
        AreaEvent(
            id="mm_heron_standoff", area="Misty Marsh",
            name="Heron Standoff",
            message="*looks up at heron* ...You're very tall. And thin. "
                    "And you eat fish. We have things in common. "
                    "...Please don't eat me. I'm mostly feathers.",
            effects={"social": 5, "fun": -2}, mood_change=1, probability=0.04,
        ),
    ],

    "Cypress Hollow": [
        AreaEvent(
            id="ch_hanging_moss", area="Cypress Hollow",
            name="Moss Curtain",
            message="*walks through moss* It's like a curtain. A green, damp curtain. "
                    "To a secret world. ...It's just more swamp. But MYSTERIOUS swamp.",
            effects={"fun": 6}, mood_change=3, probability=0.05,
        ),
        AreaEvent(
            id="ch_turtle_log", area="Cypress Hollow",
            name="Turtle on a Log",
            message="*stares at turtle* You've been on that log all day. "
                    "ALL DAY. Do you have PLANS? A SCHEDULE? "
                    "...Actually your lifestyle is kind of goals.",
            effects={"fun": 8, "social": 3}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="ch_spooky_roots", area="Cypress Hollow",
            name="Spooky Roots",
            message="*trips on root* The TREES are trying to GRAB me! "
                    "With their FEET! Tree feet! "
                    "...Roots. They're called roots. I knew that.",
            effects={"fun": -3, "energy": -3}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="ch_glowing_fungus", area="Cypress Hollow",
            name="Glowing Fungus",
            message="*finds glowing fungus* The mushrooms here glow. "
                    "In the dark. Like nightlights. For the swamp. "
                    "Nature has a lighting budget. Impressive.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="ch_owl_hoot", area="Cypress Hollow",
            name="Owl Question",
            message="*hears owl* 'WHO?' the owl asks. "
                    "ME. That's who. CHEESE. Remember the name.",
            effects={"fun": 6, "social": 3}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="ch_hollow_tree", area="Cypress Hollow",
            name="Hollow Tree Hideout",
            message="*finds hollow tree* This tree is empty inside. "
                    "Like my soul on Mondays. ...Perfect hiding spot though.",
            effects={"energy": 8, "fun": 5}, mood_change=4, probability=0.04,
        ),
        AreaEvent(
            id="ch_swamp_treasure", area="Cypress Hollow",
            name="Swamp Treasure",
            message="*finds something in mud* It's... a rusty key. To nothing. "
                    "But I HAVE a key now. I'm a key owner. "
                    "This changes everything.",
            effects={"fun": 12}, mood_change=7, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
    ],

    "Sunken Ruins": [
        AreaEvent(
            id="sr_ancient_writing", area="Sunken Ruins",
            name="Ancient Writing",
            message="*examines wall* There's writing on these stones. Ancient. Mysterious. "
                    "It says... I can't read it. But I'm SURE it says 'Cheese was here.'",
            effects={"fun": 10}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="sr_collapsed_pillar", area="Sunken Ruins",
            name="Collapsed Pillar",
            message="*inspects pillar* This pillar fell over. Thousands of years ago. "
                    "And nobody picked it up. That's some advanced laziness. Respect.",
            effects={"fun": 6}, mood_change=3, probability=0.05,
        ),
        AreaEvent(
            id="sr_underwater_room", area="Sunken Ruins",
            name="Underwater Room",
            message="*peers into flooded room* There's a room down there. Underwater. "
                    "With FURNITURE. Someone lived here. Before the swamp took over. "
                    "Worst. Landlord. Ever.",
            effects={"fun": 12}, mood_change=7, probability=0.03,
        ),
        AreaEvent(
            id="sr_echo_chamber", area="Sunken Ruins",
            name="Echo Chamber",
            message="QUACK QUACK QUACK! *echoes for 30 seconds* "
                    "This room makes me sound MAGNIFICENT. I'm never leaving. "
                    "...Okay I'll leave. But I'll be back.",
            effects={"fun": 15, "social": 5}, mood_change=8, probability=0.03,
            sound="quack",
        ),
        AreaEvent(
            id="sr_artifact", area="Sunken Ruins",
            name="Ancient Artifact",
            message="*finds old cup* This cup is ANCIENT. Probably priceless. "
                    "Probably cursed. I'm keeping it. If I turn into a frog "
                    "that's future me's problem.",
            effects={"fun": 18}, mood_change=10, probability=0.02,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="sr_mysterious_glow", area="Sunken Ruins",
            name="Mysterious Glow",
            message="*sees glow in distance* Something is glowing. In the ruins. "
                    "It's either magical or radioactive. Both are exciting. "
                    "One significantly less safe.",
            effects={"fun": 10}, mood_change=5, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="sr_ancient_trap", area="Sunken Ruins",
            name="Ancient Trap",
            message="*step* *click* ...Was that a trap? Did I just trigger an ancient trap? "
                    "Nothing happened. Either the trap broke or I'm already cursed. "
                    "Probably fine.",
            effects={"fun": -5, "energy": -3}, mood_change=-4, probability=0.04,
        ),
    ],

    # ─── URBAN BIOME ─────────────────────────────────────────────────────

    "Park Fountain": [
        AreaEvent(
            id="pf_coin_diving", area="Park Fountain",
            name="Coin Diving",
            message="*dives for coins* People throw MONEY in here! "
                    "Just THROW it! Into WATER! Humans are incredible. "
                    "I'm rich. Rich in wet pennies.",
            effects={"fun": 12}, mood_change=7, probability=0.04,
            has_animation=True, animation_id="found_shiny",
        ),
        AreaEvent(
            id="pf_kid_bread", area="Park Fountain",
            name="Kid with Bread",
            message="*a kid throws bread* BREAD! FROM THE SKY! "
                    "Thank you, tiny human! You are my favorite human! "
                    "...Until the bread runs out.",
            effects={"hunger": 15, "social": 8}, mood_change=8, probability=0.04,
            sound="eat",
        ),
        AreaEvent(
            id="pf_fountain_dance", area="Park Fountain",
            name="Fountain Dance",
            message="*splashes in fountain* The water goes UP! Then DOWN! "
                    "And I'M in it! I'm part of the fountain now! "
                    "The most beautiful part!",
            effects={"fun": 15, "cleanliness": 10}, mood_change=9, probability=0.03,
            sound="splash",
        ),
        AreaEvent(
            id="pf_pigeon_mob", area="Park Fountain",
            name="Pigeon Mob",
            message="*surrounded by pigeons* There are... so many pigeons. "
                    "They're everywhere. Looking at me. With their little eyes. "
                    "I am outnumbered. But never outmatched.",
            effects={"social": -5, "fun": -3}, mood_change=-4, probability=0.04,
        ),
        AreaEvent(
            id="pf_ice_cream_drop", area="Park Fountain",
            name="Dropped Ice Cream",
            message="*finds dropped ice cream* Someone dropped their ice cream! "
                    "Tragic for them. FANTASTIC for me. "
                    "Chocolate. My second favorite flavor after bread.",
            effects={"hunger": 12, "fun": 10}, mood_change=8, probability=0.03,
            sound="eat",
        ),
        AreaEvent(
            id="pf_dog_encounter", area="Park Fountain",
            name="Dog Encounter",
            message="*sees dog approaching* DOG! BIG DOG! "
                    "It's on a leash. I'm safe. Probably. "
                    "...It's wagging its tail. I don't trust that tail.",
            effects={"fun": -5, "energy": 5}, mood_change=-3, probability=0.04,
        ),
        AreaEvent(
            id="pf_busker_music", area="Park Fountain",
            name="Street Music",
            message="*hears guitar* A human is making music. With strings. "
                    "It's... not bad. I could do better. With quacking. "
                    "But I appreciate the effort.",
            effects={"fun": 8, "social": 5}, mood_change=5, probability=0.04,
        ),
    ],

    "Rooftop Garden": [
        AreaEvent(
            id="rg_city_view", area="Rooftop Garden",
            name="City Panorama",
            message="*looks out over city* I can see EVERYTHING from up here. "
                    "Cars. Buildings. People. They're all tiny. "
                    "Like ants. I am above them. Literally and figuratively.",
            effects={"fun": 12, "energy": 5}, mood_change=8, probability=0.03,
        ),
        AreaEvent(
            id="rg_herb_sniff", area="Rooftop Garden",
            name="Herb Garden",
            message="*sniffs herbs* Rosemary. Basil. Thyme. I know these smells. "
                    "I'm basically a chef. A duck chef. "
                    "My specialty is eating things raw.",
            effects={"fun": 6, "hunger": 3}, mood_change=4, probability=0.05,
        ),
        AreaEvent(
            id="rg_wind_gust", area="Rooftop Garden",
            name="Rooftop Wind",
            message="*nearly blown away* THE WIND! It's AGGRESSIVE up here! "
                    "I'm a duck, not a kite! ...Although being a kite sounds fun.",
            effects={"fun": -3, "energy": -3}, mood_change=-2, probability=0.05,
            has_animation=True, animation_id="nice_breeze",
        ),
        AreaEvent(
            id="rg_potted_plant_nap", area="Rooftop Garden",
            name="Potted Plant Nap",
            message="*sits in large pot* This pot is the perfect size for a duck. "
                    "I'm a potted duck now. A rare species. Very valuable.",
            effects={"energy": 10, "fun": 8}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="rg_airplane_watch", area="Rooftop Garden",
            name="Airplane Watching",
            message="*watches plane* I could fly like that. If I wanted to. "
                    "I just don't want to. The plane needs FUEL. "
                    "I run on bread and spite.",
            effects={"fun": 6}, mood_change=3, probability=0.04,
        ),
        AreaEvent(
            id="rg_cat_visitor", area="Rooftop Garden",
            name="Rooftop Cat",
            message="*spots cat* A cat. On MY roof. Staring at me. "
                    "We've reached a mutual understanding: neither of us belongs here. "
                    "But neither of us is leaving.",
            effects={"social": 5, "fun": -3}, mood_change=1, probability=0.04,
        ),
        AreaEvent(
            id="rg_rainwater_pool", area="Rooftop Garden",
            name="Rooftop Puddle",
            message="*finds puddle* Rain collected up here! A rooftop pool! "
                    "Very exclusive. Very private. Very... three inches deep. "
                    "But it's MINE.",
            effects={"cleanliness": 8, "fun": 8}, mood_change=6, probability=0.04,
            sound="splash",
        ),
    ],

    "Storm Drain": [
        AreaEvent(
            id="sd_echo_tunnel", area="Storm Drain",
            name="Tunnel Echo",
            message="QUAAACK! *massive echo* ...I sound like GOD down here. "
                    "The drain acoustics are INCREDIBLE. This is my recording studio now.",
            effects={"fun": 12, "social": 5}, mood_change=7, probability=0.04,
            sound="quack",
        ),
        AreaEvent(
            id="sd_lost_ball", area="Storm Drain",
            name="Lost Tennis Ball",
            message="*finds ball* A ball! Down HERE? Some kid is DEVASTATED right now. "
                    "Their loss. My ball. It's green. I like green.",
            effects={"fun": 10}, mood_change=6, probability=0.04,
        ),
        AreaEvent(
            id="sd_graffiti", area="Storm Drain",
            name="Underground Art",
            message="*examines graffiti* Someone PAINTED down here. In a drain. "
                    "It's actually... really good. Better than my sand drawings. "
                    "I'm not jealous. I'm INSPIRED.",
            effects={"fun": 8}, mood_change=5, probability=0.04,
        ),
        AreaEvent(
            id="sd_rat_territory", area="Storm Drain",
            name="Rat Territory",
            message="*sees rat* A rat! IN MY DRAIN! "
                    "...Okay it's probably THEIR drain. "
                    "But I'm bigger. So it's a negotiation.",
            effects={"social": -3, "fun": -3}, mood_change=-3, probability=0.05,
        ),
        AreaEvent(
            id="sd_water_rush", area="Storm Drain",
            name="Water Rush",
            message="*water flows through* WHOA! Sudden water! The drain is ACTIVE! "
                    "I'm surfing! I'm surfing in a drain! "
                    "This is either cool or unhygienic! BOTH!",
            effects={"fun": 10, "cleanliness": -10, "energy": -5}, mood_change=4, probability=0.04,
            sound="splash",
        ),
        AreaEvent(
            id="sd_pennywise_joke", area="Storm Drain",
            name="Creepy Drain",
            message="*sees drain grate above* ...I've seen movies about storm drains. "
                    "None of them end well. But I'm a DUCK. "
                    "Nothing scary about a duck in a drain. Totally normal.",
            effects={"fun": -5}, mood_change=-3, probability=0.04,
        ),
        AreaEvent(
            id="sd_underground_stream", area="Storm Drain",
            name="Underground Stream",
            message="*discovers stream* There's a whole river down here! Underground! "
                    "Secret river! For secret ducks! ...Just me. The secret duck.",
            effects={"fun": 10, "cleanliness": 5}, mood_change=6, probability=0.03,
        ),
    ],
}


# ═══════════════════════════════════════════════════════════════════════════
# SPONTANEOUS TRAVEL — Cheese sometimes wanders to a different area
# ═══════════════════════════════════════════════════════════════════════════

# Messages for when Cheese decides to wander off
SPONTANEOUS_TRAVEL_MESSAGES = [
    "*waddles away* ...I got bored. Don't take it personally. "
    "Actually, do take it personally.",
    "*stands up abruptly* Something is calling me. "
    "It might be adventure. It might be bread. Let's find out.",
    "*looks around* ...I've memorized every blade of grass here. "
    "Time for new grass. Different grass. Exotic grass.",
    "*yawns* This place is... fine. But I heard {destination} "
    "has better vibes. Allegedly.",
    "*stretches* The wanderlust has struck. I must go. "
    "Don't wait up. Or do. I don't control you.",
    "*sniffs air* I smell... possibility. And it's coming from "
    "{destination}. Or that might be mud. Either way.",
    "*decisive quack* You know what? Change of scenery. "
    "I've made an executive decision. Follow me or don't.",
    "*restless shuffling* Cheese doesn't stay in one place forever. "
    "Cheese goes where Cheese wants. Cheese speaks in third person now.",
    "*philosophical stare* Every great explorer knew when to move on. "
    "I'm like Columbus. But with better ethics. And feathers.",
    "*packs imaginary bag* Right. We're going. NOW. "
    "Why? Because I SAID so. That's why.",
]

# Messages for arriving at the new location
SPONTANEOUS_ARRIVAL_MESSAGES = [
    "*looks around* ...Yep. Different. This'll do. For now.",
    "*nods approvingly* Ah, {destination}. Just as I remember it. "
    "...I've never been here before. But JUST AS I REMEMBER IT.",
    "*settles in* New place. New opportunities. Same incredible duck.",
    "*surveys area* I have ARRIVED. You may begin being impressed.",
    "*dramatic entrance* I'm HERE. The wait is over. "
    "What do you mean nobody was waiting?",
]


class SpontaneousTravelSystem:
    """
    Manages Cheese's tendency to randomly wander to different unlocked areas.
    
    Cheese has a small chance each game tick to decide to travel somewhere
    new, provided they've been in one place long enough and the destination
    is already unlocked/discovered.
    """

    def __init__(self):
        self._last_travel_time: float = time.time()
        self._min_time_before_wander: float = 600.0  # 10 min minimum in one place
        self._wander_chance: float = 0.003           # ~0.3% per check
        self._wander_cooldown: float = 1800.0        # 30 min between wanders
        self._is_traveling: bool = False

    def check_spontaneous_travel(
        self,
        current_area_name: str,
        available_areas: list,
    ) -> Optional[Dict[str, Any]]:
        """
        Roll for spontaneous travel. Returns travel info dict or None.
        
        Args:
            current_area_name: Name of current area
            available_areas: List of BiomeArea objects the duck can access
            
        Returns:
            Dict with 'destination' (BiomeArea), 'depart_message', 'arrive_message'
            or None if no travel triggered.
        """
        now = time.time()

        # Respect cooldown
        if now - self._last_travel_time < self._wander_cooldown:
            return None

        # Must have been in one place for minimum time
        if now - self._last_travel_time < self._min_time_before_wander:
            return None

        # Need at least 2 areas to wander between
        other_areas = [a for a in available_areas if a.name != current_area_name]
        if not other_areas:
            return None

        # Roll
        if random.random() > self._wander_chance:
            return None

        # Pick destination (weighted toward less-visited areas)
        weights = []
        for area in other_areas:
            # Less visited = more interesting
            visit_weight = max(1, 10 - area.times_visited)
            weights.append(visit_weight)

        destination = random.choices(other_areas, weights=weights, k=1)[0]
        self._last_travel_time = now

        # Build messages
        depart_msg = random.choice(SPONTANEOUS_TRAVEL_MESSAGES)
        depart_msg = depart_msg.replace("{destination}", destination.name)

        arrive_msg = random.choice(SPONTANEOUS_ARRIVAL_MESSAGES)
        arrive_msg = arrive_msg.replace("{destination}", destination.name)

        return {
            "destination": destination,
            "depart_message": depart_msg,
            "arrive_message": arrive_msg,
        }

    def record_travel(self):
        """Record that travel occurred (resets the cooldown timer)."""
        self._last_travel_time = time.time()

    def to_dict(self) -> dict:
        return {"last_travel_time": self._last_travel_time}

    @classmethod
    def from_dict(cls, data: dict) -> "SpontaneousTravelSystem":
        system = cls()
        system._last_travel_time = data.get("last_travel_time", time.time())
        return system


# ═══════════════════════════════════════════════════════════════════════════
# AREA EVENT SYSTEM — checks and fires location-specific events
# ═══════════════════════════════════════════════════════════════════════════

class AreaEventSystem:
    """
    Manages area-specific random events.
    
    Checks the current exploration area against AREA_EVENTS and fires
    events with deadpan Cheese commentary and optional animations.
    """

    def __init__(self):
        self._last_event_times: Dict[str, float] = {}
        self._events_triggered_count: Dict[str, int] = {}

    def check_area_events(self, area_name: str) -> Optional[AreaEvent]:
        """
        Roll for an area-specific event.
        
        Args:
            area_name: Current area name (must match keys in AREA_EVENTS)
            
        Returns:
            AreaEvent if one fires, None otherwise.
        """
        events = AREA_EVENTS.get(area_name)
        if not events:
            return None

        now = time.time()

        for event in events:
            # Check cooldown
            last = self._last_event_times.get(event.id, 0)
            if now - last < event.cooldown:
                continue

            # Roll
            if random.random() < event.probability:
                self._last_event_times[event.id] = now
                self._events_triggered_count[event.id] = (
                    self._events_triggered_count.get(event.id, 0) + 1
                )
                return event

        return None

    def apply_area_event(self, duck: "Duck", event: AreaEvent) -> Dict[str, float]:
        """Apply an area event's effects to the duck."""
        changes = {}
        for need, change in event.effects.items():
            if hasattr(duck.needs, need):
                old = getattr(duck.needs, need)
                new = max(0, min(100, old + change))
                setattr(duck.needs, need, new)
                changes[need] = new - old
        return changes

    def to_dict(self) -> dict:
        return {
            "last_event_times": self._last_event_times,
            "events_triggered_count": self._events_triggered_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AreaEventSystem":
        system = cls()
        system._last_event_times = data.get("last_event_times", {})
        system._events_triggered_count = data.get("events_triggered_count", {})
        return system


# Global instances
area_event_system = AreaEventSystem()
spontaneous_travel = SpontaneousTravelSystem()
