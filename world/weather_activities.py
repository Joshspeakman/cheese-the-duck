"""
Weather Activities System - Weather-specific interactions and events.
Different activities available based on current weather conditions.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
import random


class WeatherType(Enum):
    """Types of weather."""
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORMY = "stormy"
    SNOWY = "snowy"
    FOGGY = "foggy"
    WINDY = "windy"
    HOT = "hot"
    COLD = "cold"


class ActivityType(Enum):
    """Types of weather activities."""
    PLAY = "play"
    EXPLORE = "explore"
    COLLECT = "collect"
    SPECIAL = "special"


@dataclass
class WeatherActivity:
    """A weather-specific activity."""
    id: str
    name: str
    description: str
    weather_types: List[WeatherType]
    activity_type: ActivityType
    duration_seconds: int = 30
    cooldown_minutes: int = 15
    coins_reward: Tuple[int, int] = (10, 30)
    xp_reward: Tuple[int, int] = (5, 15)
    special_drops: List[str] = field(default_factory=list)
    drop_chance: float = 0.1
    mood_bonus: int = 10
    ascii_animation: List[str] = field(default_factory=list)
    success_messages: List[str] = field(default_factory=list)


# Define weather activities
WEATHER_ACTIVITIES: Dict[str, WeatherActivity] = {
    # Sunny activities
    "sunbathing": WeatherActivity(
        id="sunbathing",
        name="Sunbathing",
        description="Cheese relaxes in the warm sunshine!",
        weather_types=[WeatherType.SUNNY, WeatherType.HOT],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=30,
        coins_reward=(15, 25),
        xp_reward=(10, 20),
        mood_bonus=20,
        ascii_animation=[
            "  * * *   ",
            "   \\|/   ",
            "  --d--   ",
            "   ~~~~   ",
            "  Ahhh... ",
        ],
        success_messages=[
            "Cheese soaks up the vitamin D!",
            "What a beautiful day for a duck!",
            "Cheese feels warm and happy!",
        ]
    ),
    
    "butterfly_chase": WeatherActivity(
        id="butterfly_chase",
        name="Chase Butterflies",
        description="Chase beautiful butterflies through the meadow!",
        weather_types=[WeatherType.SUNNY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 25),
        special_drops=["butterfly_wing", "flower_petal"],
        drop_chance=0.3,
        mood_bonus=15,
        ascii_animation=[
            "  ~.  .~  ",
            "    d     ",
            "   ~~>    ",
            " *waddle* ",
        ],
        success_messages=[
            "Cheese chased 5 butterflies!",
            "Almost caught one!",
            "So many pretty colors!",
        ]
    ),
    
    # Rainy activities
    "puddle_splash": WeatherActivity(
        id="puddle_splash",
        name="Puddle Splashing",
        description="Jump and splash in rain puddles!",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=15,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=25,
        ascii_animation=[
            "   ','    ",
            "   ~d~    ",
            "  *SPLASH* ",
            "   ~~~~    ",
        ],
        success_messages=[
            "SPLASH! Water everywhere!",
            "Puddles are the best!",
            "Cheese is soaking wet and happy!",
        ]
    ),
    
    "worm_hunting": WeatherActivity(
        id="worm_hunting",
        name="Worm Hunting",
        description="Rain brings worms to the surface!",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.COLLECT,
        duration_seconds=30,
        cooldown_minutes=25,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        special_drops=["juicy_worm", "giant_worm"],
        drop_chance=0.5,
        mood_bonus=10,
        ascii_animation=[
            "  ','     ",
            "  d  ?    ",
            " ~~S~~    ",
            "  Found!  ",
        ],
        success_messages=[
            "Cheese found 3 juicy worms!",
            "Protein snack time!",
            "The early duck gets the worm!",
        ]
    ),
    
    "rainbow_watch": WeatherActivity(
        id="rainbow_watch",
        name="Rainbow Watching",
        description="Wait for a rainbow after the rain!",
        weather_types=[WeatherType.RAINY, WeatherType.CLOUDY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=45,
        cooldown_minutes=60,
        coins_reward=(50, 100),
        xp_reward=(30, 50),
        special_drops=["rainbow_feather"],
        drop_chance=0.2,
        mood_bonus=30,
        ascii_animation=[
            "      (=)        ",
            "  (*)     (*)   ",
            "      d         ",
            "   *amazed*     ",
        ],
        success_messages=[
            "A beautiful rainbow appeared!",
            "Cheese made a rainbow wish!",
            "Seven colors of joy!",
        ]
    ),
    
    # Snowy activities
    "snowball_play": WeatherActivity(
        id="snowball_play",
        name="Snowball Fun",
        description="Roll around and play in the snow!",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=20,
        ascii_animation=[
            "  * * *   ",
            "    o d   ",
            "   *roll*  ",
            "  * * *   ",
        ],
        success_messages=[
            "Cheese made a snowball!",
            "Brrr but fun!",
            "Snow duck mode activated!",
        ]
    ),
    
    "snow_angel": WeatherActivity(
        id="snow_angel",
        name="Snow Duck Angel",
        description="Make a duck-shaped angel in the snow!",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=15,
        cooldown_minutes=30,
        coins_reward=(30, 50),
        xp_reward=(20, 35),
        mood_bonus=25,
        ascii_animation=[
            "  *     *  ",
            "    \\d/   ",
            "    /  \\   ",
            "  *flap*   ",
        ],
        success_messages=[
            "Perfect snow duck angel!",
            "It looks just like Cheese!",
            "Art in the snow!",
        ]
    ),
    
    "icicle_collect": WeatherActivity(
        id="icicle_collect",
        name="Icicle Collection",
        description="Carefully collect pretty icicles!",
        weather_types=[WeatherType.SNOWY, WeatherType.COLD],
        activity_type=ActivityType.COLLECT,
        duration_seconds=30,
        cooldown_minutes=25,
        coins_reward=(25, 45),
        xp_reward=(15, 30),
        special_drops=["crystal_icicle", "frozen_dewdrop"],
        drop_chance=0.35,
        ascii_animation=[
            "   |||    ",
            "     |     ",
            "    d      ",
            "  *clink*  ",
        ],
        success_messages=[
            "Found some beautiful icicles!",
            "So cold and sparkly!",
            "Nature's crystals!",
        ]
    ),
    
    # Stormy activities
    "storm_watch": WeatherActivity(
        id="storm_watch",
        name="Storm Watching",
        description="Watch the dramatic storm from safety!",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=40,
        cooldown_minutes=45,
        coins_reward=(40, 80),
        xp_reward=(25, 45),
        mood_bonus=10,
        ascii_animation=[
            "  ! (*) !   ",
            "   ','      ",
            "  [d]       ",
            " *window*   ",
        ],
        success_messages=[
            "The storm is intense!",
            "Cheese watches from inside, cozy and dry.",
            "Nature's power is amazing!",
        ]
    ),
    
    "thunder_count": WeatherActivity(
        id="thunder_count",
        name="Count Thunder",
        description="Count the seconds between lightning and thunder!",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=30,
        coins_reward=(30, 60),
        xp_reward=(20, 40),
        special_drops=["static_feather"],
        drop_chance=0.15,
        ascii_animation=[
            "   !      ",
            "  1...2...3",
            "   BOOM!  ",
            "   d !    ",
        ],
        success_messages=[
            "That was close! Only 3 seconds!",
            "The storm is far away now.",
            "Cheese is getting good at counting!",
        ]
    ),
    
    # Windy activities
    "kite_flying": WeatherActivity(
        id="kite_flying",
        name="Fly a Kite",
        description="The wind is perfect for kite flying!",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=35,
        cooldown_minutes=25,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        mood_bonus=20,
        ascii_animation=[
            "      <>   ",
            "     /     ",
            "    /      ",
            "   d       ",
        ],
        success_messages=[
            "The kite soars high!",
            "Look at it dance in the wind!",
            "Cheese is a master kite flyer!",
        ]
    ),
    
    "leaf_catch": WeatherActivity(
        id="leaf_catch",
        name="Catch Leaves",
        description="Catch swirling autumn leaves in the wind!",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.COLLECT,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        special_drops=["golden_leaf", "red_maple_leaf"],
        drop_chance=0.4,
        ascii_animation=[
            "  ~ ~ ~    ",
            "    ~~     ",
            "    d      ",
            "  *catch*  ",
        ],
        success_messages=[
            "Caught 5 colorful leaves!",
            "They're so pretty!",
            "A perfect collection!",
        ]
    ),
    
    # Foggy activities
    "fog_explore": WeatherActivity(
        id="fog_explore",
        name="Mysterious Fog Walk",
        description="Explore the mysterious foggy landscape!",
        weather_types=[WeatherType.FOGGY],
        activity_type=ActivityType.EXPLORE,
        duration_seconds=40,
        cooldown_minutes=35,
        coins_reward=(35, 70),
        xp_reward=(25, 45),
        special_drops=["mist_crystal", "fog_essence"],
        drop_chance=0.25,
        mood_bonus=5,
        ascii_animation=[
            "  ......  ",
            "  .d....  ",
            "  ...?..  ",
            " *spooky* ",
        ],
        success_messages=[
            "What was that shadow?",
            "Cheese found something in the mist!",
            "Mysterious and exciting!",
        ]
    ),
    
    # Cloudy activities
    "cloud_shapes": WeatherActivity(
        id="cloud_shapes",
        name="Cloud Watching",
        description="Find fun shapes in the clouds!",
        weather_types=[WeatherType.CLOUDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=20,
        coins_reward=(15, 30),
        xp_reward=(10, 25),
        mood_bonus=15,
        ascii_animation=[
            "  (*)(*)  ",
            "   (o o)  ",
            "    d     ",
            "  *dream* ",
        ],
        success_messages=[
            "That cloud looks like a duck!",
            "Cheese sees a giant bread loaf!",
            "So peaceful and relaxing.",
        ]
    ),
    
    # Hot weather activities
    "pond_swim": WeatherActivity(
        id="pond_swim",
        name="Cool Swim",
        description="Take a refreshing swim in the pond!",
        weather_types=[WeatherType.HOT, WeatherType.SUNNY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=25,
        ascii_animation=[
            "   * *    ",
            "   d~     ",
            "  ~~~~    ",
            " *splash* ",
        ],
        success_messages=[
            "So refreshing!",
            "Perfect temperature!",
            "Cheese is a natural swimmer!",
        ]
    ),

    # ==================== EXPANDED WEATHER ACTIVITIES ====================

    # Sunny - additional
    "bread_picnic": WeatherActivity(
        id="bread_picnic",
        name="Bread Picnic",
        description="Cheese declares a bread picnic. the sun is his excuse.",
        weather_types=[WeatherType.SUNNY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=30,
        cooldown_minutes=40,
        coins_reward=(20, 45),
        xp_reward=(15, 25),
        mood_bonus=25,
        ascii_animation=[
            "  * * *   ",
            "   \\|/   ",
            "  d [=]   ",
            " *crumbs* ",
        ],
        success_messages=[
            "Cheese ate bread in sunlight. peak existence achieved.",
            "the picnic was one duck and a crumb. it was perfect.",
            "Cheese rates this picnic 10/10. attendance was low. quality was high.",
            "outdoor dining. fancy. for a duck.",
        ]
    ),

    "shadow_chase": WeatherActivity(
        id="shadow_chase",
        name="Chase Your Shadow",
        description="Cheese has beef with his own shadow again.",
        weather_types=[WeatherType.SUNNY],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=25,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=15,
        ascii_animation=[
            "  * * *   ",
            "   d -->  ",
            "  _d_     ",
            " *stomp*  ",
        ],
        success_messages=[
            "the shadow got away. it always gets away.",
            "Cheese stepped on his shadow. he considers this a victory.",
            "the shadow mimicked everything. very rude.",
            "Cheese and his shadow have reached a truce. for now.",
        ]
    ),

    "dandelion_blow": WeatherActivity(
        id="dandelion_blow",
        name="Blow Dandelions",
        description="Cheese found dandelions. wishes incoming.",
        weather_types=[WeatherType.SUNNY, WeatherType.CLOUDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=15,
        cooldown_minutes=30,
        coins_reward=(10, 25),
        xp_reward=(10, 20),
        special_drops=["dandelion_fluff"],
        drop_chance=0.3,
        mood_bonus=20,
        ascii_animation=[
            "    .*. .  ",
            "   d ~.  ",
            "  *poof*  ",
            "  . . . . ",
        ],
        success_messages=[
            "Cheese wished for bread. obviously.",
            "the dandelion seeds scattered. carrying bread-related wishes.",
            "Cheese blew too hard. sneezed. wish still counts.",
            "three wishes. all bread. no regrets.",
        ]
    ),

    "pebble_skip": WeatherActivity(
        id="pebble_skip",
        name="Skip Pebbles",
        description="Cheese tries to skip pebbles across the pond. 'tries' is doing heavy lifting.",
        weather_types=[WeatherType.SUNNY, WeatherType.CLOUDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=20,
        coins_reward=(15, 35),
        xp_reward=(10, 25),
        mood_bonus=10,
        ascii_animation=[
            "         ",
            "  d . .  ",
            " ~~~~.~~ ",
            "  *plop* ",
        ],
        success_messages=[
            "zero skips. the pebble sank immediately. Cheese blames the water.",
            "one skip. a personal record. Cheese is insufferable about it.",
            "the pebble hit a fish. the fish was unimpressed.",
            "Cheese skipped a pebble twice. he's basically an olympian now.",
        ]
    ),

    # Rainy - additional
    "rain_song": WeatherActivity(
        id="rain_song",
        name="Rain Concert",
        description="Cheese quacks along with the rain. he calls it music.",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=25,
        cooldown_minutes=30,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=20,
        ascii_animation=[
            "  ','  '  ",
            "  ' d '   ",
            "  QUACK!  ",
            " *encore* ",
        ],
        success_messages=[
            "Cheese performed a solo. the audience was rain.",
            "standing ovation. from puddles.",
            "Cheese hit a high note. or a regular note. hard to tell with quacking.",
            "the rain provided backup vocals. professional collaboration.",
        ]
    ),

    "mud_art": WeatherActivity(
        id="mud_art",
        name="Mud Art",
        description="Cheese creates art in the mud. he's the artist AND the critic.",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=30,
        cooldown_minutes=35,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        special_drops=["mud_sculpture"],
        drop_chance=0.2,
        mood_bonus=15,
        ascii_animation=[
            "  ','     ",
            "  d ~~~   ",
            " %%% %%   ",
            " *art!*   ",
        ],
        success_messages=[
            "Cheese drew a self-portrait. it looks like a blob. he's proud.",
            "abstract mud art. or random footprints. Cheese says both count.",
            "the art gallery is the ground. admission is free.",
            "Cheese signed his work with a footprint. very official.",
        ]
    ),

    "raindrop_catch": WeatherActivity(
        id="raindrop_catch",
        name="Catch Raindrops",
        description="Cheese catches raindrops in his beak. it's less impressive than it sounds.",
        weather_types=[WeatherType.RAINY],
        activity_type=ActivityType.COLLECT,
        duration_seconds=20,
        cooldown_minutes=20,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=15,
        ascii_animation=[
            " ' ' ' '  ",
            "   d ^    ",
            "  *gulp*  ",
            "  'free!' ",
        ],
        success_messages=[
            "Cheese caught 14 raindrops. a new personal best.",
            "free water from the sky. Cheese calls this 'the economy.'",
            "raindrop catching: the sport no one asked for.",
            "Cheese is hydrated. aggressively so.",
        ]
    ),

    # Snowy - additional
    "snow_taste": WeatherActivity(
        id="snow_taste",
        name="Snow Tasting",
        description="Cheese is tasting snow. he's looking for the bread flavour.",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.EXPLORE,
        duration_seconds=15,
        cooldown_minutes=25,
        coins_reward=(10, 25),
        xp_reward=(10, 20),
        mood_bonus=10,
        ascii_animation=[
            "  * * *   ",
            "   d ~    ",
            " *lick*   ",
            " 'cold.'  ",
        ],
        success_messages=[
            "verdict: tastes like cold nothing. disappointing.",
            "Cheese licked the snow. it was not bread. shocking.",
            "snow flavour review: zero stars. no bread notes.",
            "Cheese tried yellow snow. just kidding. he has standards.",
        ]
    ),

    "snowduck_build": WeatherActivity(
        id="snowduck_build",
        name="Build a Snow Duck",
        description="Cheese builds a snow version of himself. narcissism? or art?",
        weather_types=[WeatherType.SNOWY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=35,
        cooldown_minutes=40,
        coins_reward=(30, 60),
        xp_reward=(25, 40),
        special_drops=["snow_feather"],
        drop_chance=0.2,
        mood_bonus=25,
        ascii_animation=[
            "  * * *   ",
            "  d  O    ",
            "    OOO   ",
            " *build*  ",
        ],
        success_messages=[
            "the snow duck is complete. it's handsome. not as handsome as Cheese.",
            "Cheese built a friend. it'll melt. just like all relationships.",
            "the snow duck has a bread nose. artistic vision.",
            "Cheese is having a conversation with snow-Cheese. it's going well.",
        ]
    ),

    "ice_slide": WeatherActivity(
        id="ice_slide",
        name="Ice Sliding",
        description="Cheese slides on ice. on purpose this time.",
        weather_types=[WeatherType.SNOWY, WeatherType.COLD],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=20,
        ascii_animation=[
            "  * * *   ",
            "    d~>   ",
            " ========  ",
            " *wheee!* ",
        ],
        success_messages=[
            "Cheese slid gracefully. for about two seconds. then fell.",
            "ice sliding champion. population: Cheese.",
            "Cheese went fast. too fast. couldn't stop. worth it.",
            "ducks on ice. a sport Cheese invented. just now.",
        ]
    ),

    # Stormy - additional
    "blanket_fort": WeatherActivity(
        id="blanket_fort",
        name="Blanket Fort",
        description="Cheese builds a blanket fort. storms require fortification.",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=25,
        cooldown_minutes=35,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        mood_bonus=30,
        ascii_animation=[
            "   (*)    ",
            "  /===\\   ",
            "  | d |   ",
            "  *cozy*  ",
        ],
        success_messages=[
            "fort established. storm can't reach Cheese in here.",
            "Cheese is safe. and cozy. the fort has a bread stash.",
            "structural integrity: questionable. emotional security: maximum.",
            "blanket fort protocol activated. no storms allowed inside.",
        ]
    ),

    "lightning_art": WeatherActivity(
        id="lightning_art",
        name="Lightning Sketching",
        description="Cheese tries to draw lightning before it disappears. never works.",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=30,
        coins_reward=(30, 55),
        xp_reward=(20, 35),
        special_drops=["storm_sketch"],
        drop_chance=0.15,
        mood_bonus=10,
        ascii_animation=[
            "   !  !   ",
            "  d ~~    ",
            " *draw!*  ",
            "  'too    ",
        ],
        success_messages=[
            "Cheese drew a zigzag. close enough.",
            "the lightning was too fast. Cheese drew a line. art.",
            "attempt 47. still just scribbles. Cheese calls it impressionism.",
            "Cheese captured lightning on paper. metaphorically.",
        ]
    ),

    "storm_story": WeatherActivity(
        id="storm_story",
        name="Storm Stories",
        description="Cheese tells dramatic stories timed to thunder. for atmosphere.",
        weather_types=[WeatherType.STORMY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=35,
        cooldown_minutes=40,
        coins_reward=(35, 65),
        xp_reward=(25, 40),
        mood_bonus=15,
        ascii_animation=[
            "   (*)    ",
            "  d '...' ",
            "   BOOM!  ",
            " *gasp!*  ",
        ],
        success_messages=[
            "the story was about bread. the thunder made it epic.",
            "Cheese timed the plot twist with thunder. professional storytelling.",
            "scary story about a world without bread. truly horrifying.",
            "the thunder provided sound effects. best collaboration yet.",
        ]
    ),

    # Windy - additional
    "feather_race": WeatherActivity(
        id="feather_race",
        name="Feather Race",
        description="Cheese races a loose feather in the wind. it's winning.",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=20,
        cooldown_minutes=20,
        coins_reward=(15, 35),
        xp_reward=(10, 25),
        mood_bonus=15,
        ascii_animation=[
            "    ~>    ",
            "   d  ~>  ",
            "  *run!*  ",
            "  ~>      ",
        ],
        success_messages=[
            "the feather won. Cheese is not bitter. VERY not bitter.",
            "Cheese caught the feather. briefly. then it escaped.",
            "final score: wind 1, Cheese 0.",
            "Cheese claims he let the feather win. sportsmanship.",
        ]
    ),

    "wind_singing": WeatherActivity(
        id="wind_singing",
        name="Wind Harmonizing",
        description="Cheese quacks into the wind. he calls it a duet.",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=20,
        cooldown_minutes=25,
        coins_reward=(15, 30),
        xp_reward=(10, 25),
        mood_bonus=15,
        ascii_animation=[
            "  ~~~ ~~  ",
            "   d ~~   ",
            "  QUACK~  ",
            " *duet!*  ",
        ],
        success_messages=[
            "the wind and Cheese harmonized. or clashed. art is subjective.",
            "Cheese's voice carried on the wind. neighbours were concerned.",
            "beautiful duet. the wind didn't consent to participate.",
            "Cheese sang into the void. the void hummed back.",
        ]
    ),

    "paper_plane": WeatherActivity(
        id="paper_plane",
        name="Paper Plane Launch",
        description="Cheese launches paper planes into the wind. aeronautical research.",
        weather_types=[WeatherType.WINDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=25,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        special_drops=["paper_plane_design"],
        drop_chance=0.25,
        mood_bonus=15,
        ascii_animation=[
            "   ~~>    ",
            "  d  >    ",
            "     >>   ",
            " *launch* ",
        ],
        success_messages=[
            "the plane went far. or the wind stole it. same result.",
            "Cheese wrote 'bread' on the plane. a message to the world.",
            "aerodynamics achieved. the plane flew. briefly.",
            "new distance record. Cheese is basically an engineer.",
        ]
    ),

    # Foggy - additional
    "fog_hide": WeatherActivity(
        id="fog_hide",
        name="Fog Hide and Seek",
        description="Cheese hides in the fog. from whom? unclear. but he's hidden.",
        weather_types=[WeatherType.FOGGY],
        activity_type=ActivityType.PLAY,
        duration_seconds=25,
        cooldown_minutes=30,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=15,
        ascii_animation=[
            "  ......  ",
            "  ..d...  ",
            "  ......  ",
            " *hidden* ",
        ],
        success_messages=[
            "Cheese hid so well he lost himself.",
            "invisible in the fog. Cheese's lifelong dream.",
            "nobody found him. nobody was looking. still counts.",
            "Cheese emerged from the fog dramatically. no one was there to see.",
        ]
    ),

    "fog_poetry": WeatherActivity(
        id="fog_poetry",
        name="Fog Poetry",
        description="the fog makes Cheese philosophical. brace yourself.",
        weather_types=[WeatherType.FOGGY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=20,
        cooldown_minutes=35,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=10,
        ascii_animation=[
            "  ......  ",
            "  .d....  ",
            "  'hmm.'  ",
            " *ponder* ",
        ],
        success_messages=[
            "poem: 'bread, fog, bread, fog, bread.' Cheese cries.",
            "Cheese composed a haiku. it was just quacking.",
            "the fog inspired deep thoughts. about bread. always bread.",
            "existential crisis resolved. it was just fog.",
        ]
    ),

    "fog_sounds": WeatherActivity(
        id="fog_sounds",
        name="Mysterious Sounds",
        description="Cheese listens to strange sounds in the fog. most are just frogs.",
        weather_types=[WeatherType.FOGGY],
        activity_type=ActivityType.EXPLORE,
        duration_seconds=30,
        cooldown_minutes=30,
        coins_reward=(25, 50),
        xp_reward=(20, 35),
        special_drops=["fog_bell", "mystery_sound"],
        drop_chance=0.2,
        mood_bonus=5,
        ascii_animation=[
            "  ......  ",
            "  .d ?..  ",
            "  . !! .  ",
            " *listen* ",
        ],
        success_messages=[
            "it was a frog. it's always a frog. Cheese is not disappointed.",
            "unidentified sound. Cheese chose not to investigate further.",
            "the fog whispered. or the wind did. Cheese prefers mystery.",
            "Cheese heard something. decided ignorance is bliss.",
        ]
    ),

    # Cloudy - additional
    "cloud_diary": WeatherActivity(
        id="cloud_diary",
        name="Cloud Diary",
        description="Cheese narrates the clouds. it's his soap opera.",
        weather_types=[WeatherType.CLOUDY],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=25,
        cooldown_minutes=25,
        coins_reward=(15, 35),
        xp_reward=(10, 25),
        mood_bonus=15,
        ascii_animation=[
            "  (*)(*)  ",
            "  (    )  ",
            "    d     ",
            " *drama!* ",
        ],
        success_messages=[
            "plot twist: the big cloud ate the small cloud. riveting.",
            "Cheese named every cloud. he forgot all the names.",
            "today's cloud drama: betrayal, reunion, and bread shapes.",
            "the clouds performed. Cheese was the only audience. five stars.",
        ]
    ),

    "grey_day_nap": WeatherActivity(
        id="grey_day_nap",
        name="Strategic Nap",
        description="overcast sky. perfect napping conditions. Cheese is a professional.",
        weather_types=[WeatherType.CLOUDY],
        activity_type=ActivityType.PLAY,
        duration_seconds=30,
        cooldown_minutes=40,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=25,
        ascii_animation=[
            "  (  )(  )",
            "    zzz   ",
            "    d     ",
            " *nap..* ",
        ],
        success_messages=[
            "Cheese napped. strategically. with intent.",
            "power nap complete. Cheese is 2% more powerful.",
            "the nap was grey. the mood was grey. everything was grey. and perfect.",
            "Cheese dreamed of bread. every nap, every time.",
        ]
    ),

    # Hot weather - additional
    "shade_hunt": WeatherActivity(
        id="shade_hunt",
        name="Shade Hunting",
        description="Cheese hunts for the best shade spot. competitive shading.",
        weather_types=[WeatherType.HOT],
        activity_type=ActivityType.EXPLORE,
        duration_seconds=25,
        cooldown_minutes=20,
        coins_reward=(20, 40),
        xp_reward=(15, 30),
        mood_bonus=20,
        ascii_animation=[
            "   * *    ",
            "  [===]   ",
            "    d     ",
            " *shade!* ",
        ],
        success_messages=[
            "prime shade located. Cheese claims this spot. forever.",
            "shade acquired. temperature: tolerable. duck: relieved.",
            "the shade moved with the sun. Cheese followed. commitment.",
            "best shade in the pond area. Cheese is the shade critic now.",
        ]
    ),

    "water_splash": WeatherActivity(
        id="water_splash",
        name="Splash Attack",
        description="too hot. only solution: violent splashing.",
        weather_types=[WeatherType.HOT],
        activity_type=ActivityType.PLAY,
        duration_seconds=15,
        cooldown_minutes=15,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=20,
        ascii_animation=[
            "   * *    ",
            "  ~d~~    ",
            " *SPLASH* ",
            "  ~~~~~   ",
        ],
        success_messages=[
            "everything is wet now. mission accomplished.",
            "Cheese splashed everything within a three-foot radius.",
            "the splash was therapeutic. and aggressive.",
            "cooling achieved. dignity lost. fair trade.",
        ]
    ),

    # Cold weather - additional
    "huddle_warm": WeatherActivity(
        id="huddle_warm",
        name="Warm Huddle",
        description="Cheese fluffs up into a perfect sphere. survival mode.",
        weather_types=[WeatherType.COLD],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=20,
        cooldown_minutes=20,
        coins_reward=(15, 30),
        xp_reward=(10, 20),
        mood_bonus=20,
        ascii_animation=[
            "          ",
            "   (d)    ",
            "  *poof*  ",
            "  round.  ",
        ],
        success_messages=[
            "Cheese achieved maximum fluffiness. he is now a sphere.",
            "body heat: conserved. appearance: ridiculous. worth it.",
            "Cheese is round now. cold weather turns ducks into circles.",
            "maximum insulation achieved. Cheese cannot move. acceptable trade.",
        ]
    ),

    "warm_drink": WeatherActivity(
        id="warm_drink",
        name="Warm Pond Water",
        description="Cheese drinks warm pond water. it's basically tea. it's not.",
        weather_types=[WeatherType.COLD],
        activity_type=ActivityType.SPECIAL,
        duration_seconds=15,
        cooldown_minutes=25,
        coins_reward=(10, 25),
        xp_reward=(10, 20),
        mood_bonus=15,
        ascii_animation=[
            "          ",
            "   d U    ",
            "  *sip*   ",
            "  warm.   ",
        ],
        success_messages=[
            "Cheese sipped warm water. he calls it 'pond tea.' it's just water.",
            "cozy. warm. the water tastes like pond. as expected.",
            "Cheese is warm inside now. the outside is still cold. partial victory.",
            "warm water consumed. Cheese's internal temperature: slightly improved.",
        ]
    ),
}


@dataclass
class ActivityProgress:
    """Progress for an in-progress activity."""
    activity_id: str
    started_at: str
    duration_seconds: int
    completed: bool = False


class WeatherActivitiesSystem:
    """
    System for weather-specific activities.
    """
    
    def __init__(self):
        self.activity_cooldowns: Dict[str, str] = {}  # activity_id -> last_completed
        self.current_activity: Optional[ActivityProgress] = None
        self.completed_activities: Dict[str, int] = {}  # activity_id -> times completed
        self.total_activities_done: int = 0
        self.items_collected: List[str] = []
    
    def get_available_activities(self, weather: str) -> List[WeatherActivity]:
        """Get activities available for current weather."""
        try:
            weather_type = WeatherType(weather.lower())
        except ValueError:
            weather_type = WeatherType.CLOUDY  # Default
        
        now = datetime.now()
        available = []
        
        for activity in WEATHER_ACTIVITIES.values():
            if weather_type not in activity.weather_types:
                continue
            
            # Check cooldown
            if activity.id in self.activity_cooldowns:
                last_done = datetime.fromisoformat(self.activity_cooldowns[activity.id])
                cooldown_seconds = activity.cooldown_minutes * 60
                if (now - last_done).total_seconds() < cooldown_seconds:
                    continue
            
            available.append(activity)
        
        return available
    
    def start_activity(self, activity_id: str, weather: str) -> Optional[WeatherActivity]:
        """Start a weather activity."""
        if self.current_activity:
            return None  # Already doing something
        
        available = self.get_available_activities(weather)
        activity = next((a for a in available if a.id == activity_id), None)
        
        if not activity:
            return None
        
        self.current_activity = ActivityProgress(
            activity_id=activity_id,
            started_at=datetime.now().isoformat(),
            duration_seconds=activity.duration_seconds
        )
        
        return activity
    
    def check_activity_complete(self) -> Optional[Tuple[WeatherActivity, Dict]]:
        """Check if current activity is complete and return results."""
        if not self.current_activity:
            return None
        
        started = datetime.fromisoformat(self.current_activity.started_at)
        elapsed = (datetime.now() - started).total_seconds()
        
        if elapsed < self.current_activity.duration_seconds:
            return None  # Not done yet
        
        # Complete the activity
        activity = WEATHER_ACTIVITIES.get(self.current_activity.activity_id)
        if not activity:
            self.current_activity = None
            return None
        
        # Calculate rewards
        coins = random.randint(*activity.coins_reward)
        xp = random.randint(*activity.xp_reward)
        
        # Check for special drops
        special_drop = None
        if activity.special_drops and random.random() < activity.drop_chance:
            special_drop = random.choice(activity.special_drops)
            self.items_collected.append(special_drop)
        
        message = random.choice(activity.success_messages) if activity.success_messages else f"Completed {activity.name}!"
        
        # Update tracking
        self.activity_cooldowns[activity.id] = datetime.now().isoformat()
        self.completed_activities[activity.id] = self.completed_activities.get(activity.id, 0) + 1
        self.total_activities_done += 1
        self.current_activity = None
        
        results = {
            "coins": coins,
            "xp": xp,
            "mood_bonus": activity.mood_bonus,
            "special_drop": special_drop,
            "message": message,
        }
        
        return activity, results
    
    def get_activity_progress(self) -> Optional[Tuple[float, WeatherActivity]]:
        """Get progress of current activity (0.0 to 1.0)."""
        if not self.current_activity:
            return None
        
        activity = WEATHER_ACTIVITIES.get(self.current_activity.activity_id)
        if not activity:
            return None
        
        started = datetime.fromisoformat(self.current_activity.started_at)
        elapsed = (datetime.now() - started).total_seconds()
        progress = min(1.0, elapsed / self.current_activity.duration_seconds)
        
        return progress, activity
    
    def render_activity_selection(self, weather: str) -> List[str]:
        """Render available activities for selection."""
        lines = [
            "+===============================================+",
            f"|      *️ WEATHER ACTIVITIES ({weather.upper()})        |",
            "+===============================================+",
        ]
        
        activities = self.get_available_activities(weather)
        
        if not activities:
            lines.append("|  No activities available right now!           |")
            lines.append("|  Check back when the weather changes,         |")
            lines.append("|  or wait for cooldowns to reset.              |")
        else:
            for i, activity in enumerate(activities, 1):
                lines.append(f"|  [{i}] {activity.name:<35}  |")
                desc = activity.description[:40]
                lines.append(f"|      {desc:<40}  |")
                lines.append(f"|      (t) {activity.duration_seconds}s  $ {activity.coins_reward[0]}-{activity.coins_reward[1]}  * {activity.xp_reward[0]}-{activity.xp_reward[1]} XP |")
                lines.append("|                                               |")
        
        lines.extend([
            "+===============================================+",
            "|  Select an activity number or [B] to go back  |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_activity_progress(self) -> List[str]:
        """Render current activity in progress."""
        progress_data = self.get_activity_progress()
        if not progress_data:
            return []
        
        progress, activity = progress_data
        
        # Progress bar
        bar_width = 30
        filled = int(progress * bar_width)
        bar = "#" * filled + "." * (bar_width - filled)
        
        lines = [
            "+===============================================+",
            f"|      (o) {activity.name.upper():<30}  |",
            "+===============================================+",
        ]
        
        # Add animation
        if activity.ascii_animation:
            for anim_line in activity.ascii_animation:
                lines.append(f"|  {anim_line:^43}  |")
        
        lines.extend([
            "|                                               |",
            f"|  [{bar}]  |",
            f"|  {int(progress * 100):>42}%  |",
            "+===============================================+",
        ])
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "activity_cooldowns": self.activity_cooldowns,
            "completed_activities": self.completed_activities,
            "total_activities_done": self.total_activities_done,
            "items_collected": self.items_collected[-50:],  # Keep last 50
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WeatherActivitiesSystem":
        """Create from dictionary."""
        system = cls()
        system.activity_cooldowns = data.get("activity_cooldowns", {})
        system.completed_activities = data.get("completed_activities", {})
        system.total_activities_done = data.get("total_activities_done", 0)
        system.items_collected = data.get("items_collected", [])
        return system


# Global instance
weather_activities_system = WeatherActivitiesSystem()
