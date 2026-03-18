"""
Habitat ASCII art - visual representations of items in the duck's home.
"""
from typing import Dict, List
from world.shop import get_item


# ASCII art for habitat items when placed
HABITAT_ITEM_ART: Dict[str, List[str]] = {
    # ============ TOYS ============
    "toy_ball": ["  O"],
    "toy_blocks": [" ▄▀▄", " ▀▄▀"],
    "toy_trumpet": [" #)═"],
    "toy_skateboard": ["══╗═╔══"],
    "toy_piano": [" ┌─┬─┐", " │█│█│", " └─┴─┘"],
    "toy_trampoline": [" ╱╲╱╲╱╲", "│BOUNCE│", " ╲╱╲╱╲╱"],
    "toy_slide": ["    ╱", "   ╱ ", "  ╱  ", " ╱___"],
    "toy_swing": [" │ │", " │O│", " └─┘"],
    "toy_seesaw": ["  ___╱", " ═════", "   △  "],
    "toy_sandbox": [" ╔═══╗", " ║ ~ ║", " ╚═══╝"],
    "squeaky_toy": [" (!)"],
    "rubber_duck": [" _", "(O>", "(_)"],
    "frisbee": [" ═○═"],
    "toy_car": [" ▄▀▀▄", " ○──○"],
    "jump_rope": [" ╰╮╭╯"],
    "yo_yo": ["  ●", "  │", "  ●"],
    "kite": ["  ◇", " /│\\", "  │"],
    "skateboard": ["═══╪═══"],
    "trampoline": [" ╱╲╱╲╱╲", "│JUMP!│", " ╲╱╲╱╲╱"],
    "telescope": [" ◎──", " │", " ┴"],
    "easel": [" ┌──┐", " │*│", " ├──┤", " ╱  ╲"],
    "drums": [" ###", " ┌─┐", " │●│", " └─┘"],
    
    # ============ FURNITURE ============
    "chair_wood": [" ┌─┐", " │ │", " └─┘"],
    "chair_throne": [" ╔═╗", " ║^║", " ╚═╝"],
    "table_small": [" ┌───┐", " │   │", " └───┘"],
    "bed_small": [" ┌─────┐", " │░░░░░│", " └─────┘"],
    "bed_king": [" ┌─────────┐", " │░░░░░░░░░│", " └─────────┘"],
    "couch": [" ╔═══╗", " ║░░░║", " ╚═══╝"],
    "bookshelf": [" ║┃┃┃║", " ║┃┃┃║", " ╚═══╝"],
    "bookshelf_wood": [" ║┃┃┃║", " ║┃┃┃║", " ╚═══╝"],
    "desk": [" ┌─────┐", " │     │", " ├─┬─┬─┤"],
    "desk_writing": [" ┌─────┐", " │  ✎  │", " ├─┬─┬─┤"],
    "lamp_floor": [" ┌─┐", " │▓│", " │ │"],
    "mirror": [" ┌───┐", " │ ◐ │", " └───┘"],
    "mirror_standing": [" ┌───┐", " │ ◐ │", " └───┘"],
    "cushion": ["  ▀▀▀"],
    "dresser": [" ┌───┐", " ├───┤", " ├───┤", " └───┘"],
    "piano": [" ┌─┬─┬─┬─┐", " │█│█│█│█│", " └─┴─┴─┴─┘"],
    "wardrobe": [" ┌─────┐", " │ ◊ ◊ │", " │     │", " └─────┘"],
    "sofa_fancy": [" ╔═════╗", " ║▓▓▓▓▓║", " ╚═════╝"],
    "coffee_table": [" ┌─────┐", " └─────┘"],
    "bar_cart": [" ┌───┐", " │🍷│", " └─○─┘"],
    "grandfather_clock": [" ┌─┐", " │⌚│", " │ │", " └─┘"],
    "rocking_horse": ["  ∩", " ╱│╲", "╰───╯"],
    "cabinet": [" ┌───┐", " │▓▓▓│", " └───┘"],
    "fireplace": [" ╔═══╗", " ║^║", " ╠═══╣", " ║ ▓ ║"],
    "tv_stand": [" ┌───┐", " │📺│", " └───┘"],
    "bean_bag": [" ╭───╮", " │ ░ │", " ╰───╯"],
    "golden_throne": [" ╔═^═╗", " ║ ^ ║", " ╚═══╝"],
    
    # ============ WATER FEATURES ============
    "pool_kiddie": [" ╔═══╗", " ║≈≈≈║", " ╚═══╝"],
    "pool_large": [" ╔═════════╗", " ║≈≈≈≈≈≈≈≈≈║", " ║≈≈≈≈≈≈≈≈≈║", " ╚═════════╝"],
    "fountain_small": ["   ╥", "  ║║║", " ╔═══╗", " ║≈≈≈║"],
    "fountain_decorative": ["   ╥", "  ║║║", " ╔═══╗", " ║≈≈≈║"],
    "fountain_grand": ["    ╥", "   ║║║", "  ║║║║║", " ╔═════╗", " ║≈≈≈≈≈║"],
    "pond": [" ╔═══════╗", " ║ ≈ ≈ ≈ ║", " ║≈ ≈ ≈ ≈║", " ╚═══════╝"],
    "sprinkler": [" ╱│╲", "  │ ", "  ●"],
    "sprinkler_system": [" ╱│╲ ╱│╲", "  │   │ "],
    "waterfall": [" ║║║", " ║║║", " ║║║", "╔════╗"],
    "waterfall_mini": [" ║║║", " ║║║", "╔══╗"],
    "hot_tub": [" ╔═════╗", " ║○○○○○║", " ║≈≈≈≈≈║", " ╚═════╝"],
    "hot_tub_deluxe": [" ╔═══════╗", " ║○○○○○○○║", " ║≈≈≈≈≈≈≈║", " ╚═══════╝"],
    "birdbath": ["  ═", " ╔═╗", " ║≈║", "  │"],
    "birdbath_garden": ["  ═", " ╔═╗", " ║≈║", "  │"],
    "water_slide": ["     ╱", "    ╱ ", "   ╱  ", "  ╱   ", " ╱____"],
    "water_slide_mega": ["      ╱", "     ╱ ", "    ╱  ", "   ╱   ", "  ╱    ", " ╱_____"],
    "koi_pond": [" ╔═══════╗", " ║ ><> ≈ ║", " ║≈ <><  ║", " ╚═══════╝"],
    "water_bowl": [" ╔═╗", " ║≈║", " ╚═╝"],
    
    # ============ PLANTS ============
    "flower_rose": [" @"],
    "flower_tulip": [" +"],
    "flower_sunflower": [" *"],
    "flower_pot": [" *", " ┴"],
    "tree_small": ["  A", "  │"],
    "tree_oak": ["  AAA", "  ║║║", "   │"],
    "tree_cherry": ["  ***", "  ║║║", "   │"],
    "cherry_tree": ["  ***", "  ║║║", "   │"],
    "bush_hedge": [" ▓▓▓"],
    "grass_patch": [" ░░░"],
    "grass_floor": [" ░░░"],
    "cactus": [" ┃", " ┃", "╪╪╪"],
    "bamboo": [" ║║║", " ║║║"],
    "bonsai": ["  _/\\_ ", "   ┃"],
    "venus_flytrap": [" ╲◊╱", "  │"],
    "herb_garden": [" +++", " ┴┴┴"],
    "willow_tree": ["  /│\\", " / │ \\", "   │"],
    "mushroom_patch": [" ∩ ∩ ∩"],
    "topiary_duck": [" A", " ◎", " ┴"],
    "fern": [" /\\/\\"],
    "lavender": [" +++"],
    "hedge_maze": [" ▓▓▓▓▓", " ▓   ▓", " ▓▓▓▓▓"],
    "world_tree": ["  AAAAA", " AAAAAAA", "    ║", "    ║", "    ║"],
    
    # ============ STRUCTURES ============
    "dog_house": [" ╱╲", " ╱  ╲", "│____│", "│ ▄▄ │"],
    "picket_fence": [" │ │ │"],
    "stone_wall": [" ▓▓▓▓"],
    "archway": [" ╔═══╗", " ║   ║", " ║   ║"],
    "gazebo": [" ╱▔▔▔╲", "╱     ╲", "│     │"],
    "bridge": [" ╱════╲", "╱      ╲"],
    "tower": [" ┌─┐", " │ │", " │ │", " │ │", " └─┘"],
    "windmill": ["  ─┼─", " ╱ │ ╲", "   │", " ┌─┼─┐"],
    "gate": [" ├═╤═┤"],
    "pergola": [" ═══════", " ║     ║"],
    "shed": [" ╱────╲", "│ SHED │", "└──────┘"],
    "treehouse": ["  AAA", " ╔═══╗", " ║   ║", "   │"],
    "birdhouse": [" ∩", " │O│", " └─┘"],
    "mailbox": [" ╔═╗", " ║@║", "  │"],
    "wishing_well": ["  ╱╲", " │≈≈│", " └──┘"],
    "trellis": [" *╳*", " ╳ ╳", " *╳*"],
    "greenhouse": [" ╔═══╗", " ║+++║", " ║+++║", " ╚═══╝"],
    "castle_tower": [" ▲▲▲", " ║ ║", " ║ ║", " ║ ║"],
    "barn": [" ╱────╲", "│ BARN │", "└──────┘"],
    "fence_section": [" ├──┤"],
    "cosmic_arch": [" *═══*", " ║   ║", " *═══*"],
    
    # ============ BUILT STRUCTURES (from building system) ============
    "basic_nest": [
        "    ____    ",
        "   /    \\   ",
        "  / ~~~~ \\  ",
        " (  ~~~~  ) ",
        "  \\______/  ",
    ],
    "cozy_nest": [
        "     ___     ",
        "   _/   \\_   ",
        "  / ~~~~~ \\  ",
        " / ~~~~~~~ \\ ",
        "(  ~~~~~~~  )",
        " \\__     __/ ",
        "    \\___/    ",
    ],
    "deluxe_nest": [
        "    _____    ",
        "  _/  ♥  \\_  ",
        " / ~~~~~~~ \\ ",
        "/ ~~~~~~~~~ \\",
        "| ~~~~~~~~~ |",
        "| ~~~~~~~~~ |",
        " \\__     __/ ",
        "    \\___/    ",
    ],
    "mud_hut": [
        "    _____    ",
        "   /     \\   ",
        "  /  ___  \\  ",
        " |  |   |  | ",
        " |__|   |__| ",
        " ████████████",
    ],
    "wooden_cottage": [
        "      /\\      ",
        "     /  \\     ",
        "    /____\\    ",
        "   |▓▓  ▓▓|   ",
        "   |▓▓[]▓▓|   ",
        "   |▓▓  ▓▓|   ",
        "   └──────┘   ",
    ],
    "stone_house": [
        "       /\\       ",
        "      /  \\      ",
        "     /____\\     ",
        "   ╔════════╗   ",
        "   ║▓▓ [] ▓▓║   ",
        "   ║▓▓    ▓▓║   ",
        "   ║▓▓ ▄▄ ▓▓║   ",
        "   ╚════════╝   ",
    ],
    "workbench": [
        " ┌──────────┐ ",
        " │ # * # │ ",
        " ├──────────┤ ",
        " │          │ ",
        " └──────────┘ ",
    ],
    "storage_chest": [
        " ╔════════╗ ",
        " ║ ▓▓▓▓▓▓ ║ ",
        " ╠════════╣ ",
        " ║        ║ ",
        " ╚════════╝ ",
    ],
    "garden_plot": [
        " ┌────────┐ ",
        " │ + * +  │ ",
        " │  + + * │ ",
        " └────────┘ ",
    ],
    "bird_bath": [
        "    ═    ",
        "  ╔═══╗  ",
        "  ║≈≈≈║  ",
        "    │    ",
        "   ███   ",
    ],
    "watchtower": [
        "   ┌─┐   ",
        "   │^│   ",
        "  ╔═══╗  ",
        "  ║   ║  ",
        "  ║   ║  ",
        "  ║   ║  ",
        "  ╚═══╝  ",
    ],
    "flower_bed": [
        " * * * * ",
        " ░░░░░░░ ",
    ],
    "stone_path": [
        " ○ ○ ○ ○ ",
    ],
    "pond_fountain": [
        "    ╥    ",
        "   ╥╥╥   ",
        " ╔═════╗ ",
        " ║≈≈≈≈≈║ ",
        " ║≈≈≈≈≈║ ",
        " ╚═════╝ ",
    ],
    
    # ============ DECORATIONS ============
    "garden_gnome": [" ∩", "(◕‿◕)", " △"],
    "duck_statue": [" _", "(◐>", " ╱"],
    "fountain_statue": [" o", " │", "═══"],
    "wind_chimes": [" ╥╥╥"],
    "sundial": [" ⌚"],
    "weather_vane": [" ◄►"],
    "flag_pole": [" ▓▓", "  │", "  │"],
    "tire_swing": [" │", " O", " │"],
    "hammock": [" ╰───╯"],
    "scarecrow": [" ∩", "─╬─", " │"],
    "totem_pole": [" o", " :)", " A"],
    "welcome_mat": ["[QUACK]"],
    "potted_cactus": [" ╪", " ┴"],
    "stepping_stones": [" ○ ○ ○"],
    "garden_bench": [" ╔═══╗", " ╚═══╝"],
    "zen_garden": [" ~~~", " ───"],
    "fairy_lights": [" *.*.*"],
    "pinwheel": [" ╳"],
    "rain_barrel": [" ═", " ▓", " ▓"],
    "wheelbarrow": ["╱▓▓╲○"],
    "tiki_torch": [" ^", "  │"],
    "ice_sculpture": [" ◇"],
    "trophy_case": [" ┌─┐", " │#│", " └─┘"],
    "compass_rose": [" N", "W+E", " S"],
    "sand_castle": [" ▲▲▲", " ▓▓▓"],
    "gong": [" ○"],
    "bubble_machine": [" ○°○"],
    "snow_globe": [" ╭─╮", " │*│", " ╰─╯"],
    
    # ============ LIGHTING ============
    "table_lamp": [" ╲╱", "  │"],
    "floor_lamp": [" ╲╱", "  │", "  │"],
    "chandelier": [" ╥╥╥", "╲▓▓▓╱"],
    "paper_lantern": [" ╭─╮", " │▓│", " ╰─╯"],
    "lava_lamp": [" ╭─╮", " │◉│", " ╰─╯"],
    "neon_sign": ["QUACK"],
    "disco_ball": [" ◇"],
    "candelabra": [" 🕯🕯🕯"],
    "fairy_lamp": [" °°°"],
    "spotlight": [" ╲▓╱"],
    "street_lamp": [" ╲╱", "  │", "  │"],
    "campfire": [" ^", " ╱╲"],
    "lighthouse": [" ╲╱", " ║║", " ║║", "╔══╗"],
    "firefly_swarm": [" *  * *", "  * *"],
    "moon_lamp": [" )"],
    "star_projector": [" ***"],
    "torches": [" ^ ^"],
    "glowsticks": [" ╱╲╱╲"],
    "aurora": [" ~~~", " ≈≈≈"],
    "laser_lights": [" ╲│╱", " ─+─", " ╱│╲"],
    "eternal_flame": [" ^", " ┃"],
    
    # ============ FLOORING ============
    "wooden_planks": ["═══════"],
    "marble_tiles": ["░▓░▓░"],
    "carpet_red": ["▓▓▓▓▓"],
    "tatami_mat": ["║║║║║"],
    "sand_floor": ["~~~~~"],
    "stone_tiles": ["▒▒▒▒▒"],
    "checkered_floor": ["░▓░▓░"],
    "mosaic_tiles": ["◇◆◇◆◇"],
    "ice_floor": ["═════"],
    "cobblestone": ["○○○○○"],
    "lava_floor": ["^^^"],
    "cloud_floor": ["*****"],
    "persian_rug": ["▓░▓░▓"],
    "rainbow_path": ["═════"],
    "glass_floor": ["═════"],
    "rubber_mat": ["▓▓▓▓▓"],
    "autumn_leaves": ["🍂🍂🍂"],
    "snow_floor": ["*****"],
    "galaxy_floor": ["*****"],
    
    # ============ SPECIAL ITEMS ============
    "portal": [" ╭─────╮", " │ ◉◉◉ │", " │ ◉ ◉ │", " │ ◉◉◉ │", " ╰─────╯"],
    "time_machine": [" ╔═══╗", " ║⌚⌚║", " ║⌚⌚║", " ╚═══╝"],
    "rainbow_generator": [" *", " ═══"],
    "weather_machine": [" ╔═══╗", " ║**Y║", " ╚═══╝"],
    "black_hole": ["  ◉"],
    "volcano": ["  ▲", " ╱^╲", "╱___╲"],
    "antigravity": [" ↑↑↑"],
    "tornado": ["  ╲│╱", "  ─●─", "  ╱│╲"],
    "dragon_egg": [" ╭─╮", " │◉│", " ╰─╯"],
    "treasure_chest": [" ╔══╗", " ║$║", " ╚══╝"],
    "magic_carpet": [" ▓░▓░▓"],
    "crystal_ball": [" (◉)"],
    "wormhole": ["  ○", " ◉", "  ○"],
    "force_field": [" ╔═══╗", " ║ ◇ ║", " ╚═══╝"],
    "teleporter": [" ═◎═"],
    "robot_butler": [" ┌─┐", " │◉│", " ├─┤"],
    "hologram": [" ░▒▓"],
    "shrink_ray": [" ═◎"],
    "growth_ray": [" ═◎═══"],
    "cloning_machine": [" ╔═══╗", " ║◎◎◎║", " ╚═══╝"],
    "ufo": ["  ╱╲", " ╱◎◎╲", "  ──"],
    "rainbow_slide": ["    ╱", "   ╱ ", "  ╱══"],
    "genie_lamp": [" ◇", " ╱╲"],
    "infinity_pool": [" ╔═════∞", " ║≈≈≈≈≈║", " ╚═════╝"],
    "bounce_house": [" ╱▓▓▓╲", " ▓▓▓▓▓", " ╲▓▓▓╱"],
    "ferris_wheel": ["  ○", " ╱│╲", "  │"],
    "carousel": [" ○─○─○", "  ─┬─"],
    "jetpack": [" ╬", " ╬", " ^"],
    "submarine": [" ╔════╗", " ║◎═══╗", " ╚════╝"],
    "hot_air_balloon": [" ╭───╮", " │ ▓ │", " ╰───╯", "  │", " [_]"],
    "rocket_ship": ["  ▲", " ╔═╗", " ║ ║", " ╠═╣", " ^"],
    "tardis": [" ┌───┐", " │ ▓ │", " │ ▓ │", " └───┘"],
    "invisible_cloak": [" ░░░"],
    "transmogrifier": [" ╔═╗", " ║?║", " ╚═╝"],
    "money_printer": [" ╔═══╗", " ║$$$║", " ╚═══╝"],
    "perpetual_motion": [" ○─○", " │ │", " ○─○"],
    "DNA_mixer": [" ╔═╗", " ║◉║", " ╚═╝"],
    "dream_catcher": [" ╭○╮", " ╰┬╯"],
    "wish_fountain": [" ╥", " ║", "╔══╗"],
    "dimensional_door": [" ╔═══╗", " ║ ? ║", " ║ ? ║", " ╚═══╝"],
    "philosophers_stone": [" ◇"],
    "nook_radio": ["    │", " ╔══╧══╗", " ║♪ ◎◎ ║", " ╚═════╝"],
}

# Item color mapping - use blessed terminal colors
from blessed import Terminal
_term = Terminal()

# Color functions for items
ITEM_COLORS = {
    # Toys - bright playful colors
    "toy_ball": _term.bright_red,
    "toy_blocks": _term.bright_yellow,
    "toy_trumpet": _term.color(220),  # Gold
    "toy_skateboard": _term.color(130),  # Brown
    "toy_piano": _term.bright_white,
    "toy_trampoline": _term.bright_magenta,
    "toy_slide": _term.bright_cyan,
    "toy_swing": _term.color(130),  # Brown
    "toy_seesaw": _term.green,
    "toy_sandbox": _term.yellow,
    "squeaky_toy": _term.bright_yellow,
    "rubber_duck": _term.bright_yellow,
    "frisbee": _term.bright_red,
    "toy_car": _term.bright_red,
    "jump_rope": _term.color(213),  # Pink
    "yo_yo": _term.bright_green,
    "kite": _term.bright_magenta,
    "skateboard": _term.color(208),  # Orange
    "trampoline": _term.color(135),  # Purple
    "telescope": _term.color(250),  # Silver
    "easel": _term.color(130),  # Brown
    "drums": _term.color(208),  # Orange
    
    # Furniture - earthy/natural tones
    "chair_wood": _term.color(130),  # Brown
    "chair_throne": _term.color(220),  # Gold
    "table_small": _term.color(130),  # Brown
    "bed_small": _term.color(135),  # Purple
    "bed_king": _term.color(220),  # Gold
    "couch": _term.bright_red,
    "bookshelf": _term.color(130),  # Brown
    "bookshelf_wood": _term.color(130),  # Brown
    "desk": _term.color(130),  # Brown
    "desk_writing": _term.color(30),  # Teal
    "lamp_floor": _term.bright_yellow,
    "mirror": _term.color(250),  # Silver
    "mirror_standing": _term.color(250),  # Silver
    "cushion": _term.bright_magenta,
    "dresser": _term.color(130),  # Brown
    "piano": _term.bright_white,
    "wardrobe": _term.color(130),  # Brown
    "sofa_fancy": _term.color(135),  # Purple
    "coffee_table": _term.color(130),  # Brown
    "bar_cart": _term.color(250),  # Silver
    "grandfather_clock": _term.color(130),  # Brown
    "rocking_horse": _term.color(130),  # Brown
    "cabinet": _term.color(130),  # Brown
    "fireplace": _term.color(208),  # Orange (fire)
    "tv_stand": _term.color(130),  # Brown
    "bean_bag": _term.bright_cyan,
    "golden_throne": _term.color(220),  # Gold
    
    # Water features - blues
    "pool_kiddie": _term.bright_blue,
    "pool_large": _term.bright_blue,
    "fountain_small": _term.bright_cyan,
    "fountain_decorative": _term.bright_cyan,
    "fountain_grand": _term.bright_cyan,
    "pond": _term.bright_blue,
    "sprinkler": _term.bright_cyan,
    "sprinkler_system": _term.bright_cyan,
    "waterfall": _term.bright_cyan,
    "waterfall_mini": _term.bright_cyan,
    "hot_tub": _term.blue,
    "hot_tub_deluxe": _term.blue,
    "birdbath": _term.color(250),  # Silver
    "birdbath_garden": _term.color(250),  # Silver
    "water_slide": _term.bright_cyan,
    "water_slide_mega": _term.bright_cyan,
    
    # Radio
    "nook_radio": _term.color(130),  # Brown
    "koi_pond": _term.bright_blue,
    "water_bowl": _term.bright_blue,
    
    # Plants - greens
    "flower_rose": _term.bright_red,
    "flower_tulip": _term.bright_magenta,
    "flower_sunflower": _term.bright_yellow,
    "flower_pot": _term.color(213),  # Pink
    "tree_small": _term.green,
    "tree_oak": _term.green,
    "tree_cherry": _term.color(213),  # Pink
    "cherry_tree": _term.color(213),  # Pink
    "bush_hedge": _term.green,
    "grass_patch": _term.bright_green,
    "grass_floor": _term.bright_green,
    "cactus": _term.green,
    "bamboo": _term.bright_green,
    "bonsai": _term.green,
    "venus_flytrap": _term.bright_green,
    "herb_garden": _term.green,
    "willow_tree": _term.green,
    "fern": _term.bright_green,
    "ivy": _term.green,
    "topiary": _term.bright_green,
    "zen_garden": _term.color(130),  # Brown (sand)
    "crystal_tree": _term.bright_cyan,
    "rainbow_flowers": _term.bright_magenta,
    
    # Decorations - varied
    "rug_small": _term.bright_red,
    "rug_fancy": _term.color(135),  # Purple
    "rug_persian": _term.color(135),  # Purple
    "lamp_desk": _term.bright_yellow,
    "picture_frame": _term.color(220),  # Gold
    "clock_wall": _term.color(130),  # Brown
    "plant_hanging": _term.green,
    "curtains": _term.bright_red,
    "chandelier": _term.color(220),  # Gold
    "trophy_case": _term.color(220),  # Gold
    "aquarium": _term.bright_blue,
    "globe": _term.bright_blue,
    "jukebox": _term.color(208),  # Orange
    "arcade_machine": _term.bright_magenta,
    "pinball_machine": _term.bright_cyan,
    "vending_machine": _term.bright_red,
    "neon_sign": _term.bright_magenta,
    "disco_ball": _term.bright_white,
    "stage_lights": _term.bright_magenta,
    "fog_machine": _term.white,
    "bubble_machine": _term.bright_cyan,
    
    # Food/Kitchen - warm colors
    "food_bowl": _term.color(208),  # Orange
    "hay_pile": _term.yellow,
    "treat_dispenser": _term.bright_yellow,
    
    # Special/Magic - bright/mystical colors
    "golden_egg": _term.color(220),  # Gold
    "magic_wand": _term.bright_magenta,
    "crystal_ball": _term.bright_cyan,
    "enchanted_mirror": _term.bright_cyan,
    "rainbow_generator": _term.bright_magenta,
    "time_machine": _term.bright_cyan,
    "teleporter": _term.bright_magenta,
    "hologram_projector": _term.bright_cyan,
    "aurora_generator": _term.bright_green,
    "dimensional_door": _term.bright_magenta,
    "philosophers_stone": _term.color(220),  # Gold
}


def get_item_color(item_id: str):
    """Get the color function for an item.
    
    Returns:
        A blessed terminal color function, or None for no color.
    """
    return ITEM_COLORS.get(item_id)


def get_item_art(item_id: str) -> List[str]:
    """Get ASCII art for an item."""
    if item_id in HABITAT_ITEM_ART:
        return HABITAT_ITEM_ART[item_id].copy()
    
    # Default placeholder
    return ["[?]"]


def get_structure_art(structure_id: str) -> List[str]:
    """Get ASCII art for a built structure."""
    if structure_id in HABITAT_ITEM_ART:
        return HABITAT_ITEM_ART[structure_id].copy()
    
    # Default placeholder for unknown structures
    return ["[?]"]


def get_structure_color(structure_id: str):
    """Get color function for a structure."""
    # Structure color mappings
    STRUCTURE_COLORS = {
        "basic_nest": "yellow",
        "cozy_nest": "yellow",
        "deluxe_nest": "bright_yellow",
        "mud_hut": "red",
        "wooden_cottage": "yellow",
        "stone_house": "white",
        "workbench": "cyan",
        "storage_chest": "yellow",
        "garden_plot": "green",
        "bird_bath": "bright_cyan",
        "watchtower": "yellow",
        "flower_bed": "magenta",
        "stone_path": "white",
        "pond_fountain": "bright_cyan",
    }
    
    color_name = STRUCTURE_COLORS.get(structure_id)
    if color_name:
        # This will be resolved to actual terminal color in renderer
        return color_name
    return None


def get_item_size(item_id: str) -> tuple:
    """Get the width and height of an item's art."""
    art = get_item_art(item_id)
    if not art:
        return (1, 1)
    height = len(art)
    width = max(len(line) for line in art) if art else 1
    return (width, height)


def render_habitat_grid(placed_items, width: int = 40, height: int = 15) -> List[str]:
    """
    Render the habitat as a grid with placed items.
    
    Args:
        placed_items: List of PlacedItem objects
        width: Grid width in characters
        height: Grid height in lines
    
    Returns:
        List of strings representing the habitat
    """
    # Create empty grid
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Place items
    for placed in placed_items:
        art = get_item_art(placed.item_id)
        
        # Place each line of the art
        for y_offset, line in enumerate(art):
            y_pos = placed.y + y_offset
            if 0 <= y_pos < height:
                for x_offset, char in enumerate(line):
                    x_pos = placed.x + x_offset
                    if 0 <= x_pos < width:
                        grid[y_pos][x_pos] = char
    
    # Convert grid to strings
    return [''.join(row) for row in grid]


def render_item_preview(item_id: str) -> List[str]:
    """Render an item for preview in the shop."""
    art = get_item_art(item_id)
    item = get_item(item_id)
    
    if not item:
        return art
    
    # Add a frame around the item
    max_width = max(len(line) for line in art) if art else 3
    max_width = max(max_width, len(item.name) + 2)
    
    result = []
    result.append("┌" + "─" * (max_width + 2) + "┐")
    
    for line in art:
        padding = max_width - len(line)
        result.append("│ " + line + " " * padding + " │")
    
    result.append("└" + "─" * (max_width + 2) + "┘")
    result.append(f" {item.name}")
    result.append(f" ${item.cost}")
    
    return result
