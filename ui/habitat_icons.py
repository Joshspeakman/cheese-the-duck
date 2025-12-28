"""
Mini habitat item icons for playfield display.
Each item has a single character (or short string) with color function.
"""
from blessed import Terminal

_term = Terminal()


# Color functions
class ItemColors:
    """Color wrappers for habitat items."""
    RED = lambda s: _term.red(s)
    BRIGHT_RED = lambda s: _term.bright_red(s)
    BLUE = lambda s: _term.blue(s)
    BRIGHT_BLUE = lambda s: _term.bright_blue(s)
    YELLOW = lambda s: _term.yellow(s)
    BRIGHT_YELLOW = lambda s: _term.bright_yellow(s)
    GREEN = lambda s: _term.green(s)
    BRIGHT_GREEN = lambda s: _term.bright_green(s)
    MAGENTA = lambda s: _term.magenta(s)
    BRIGHT_MAGENTA = lambda s: _term.bright_magenta(s)
    CYAN = lambda s: _term.cyan(s)
    BRIGHT_CYAN = lambda s: _term.bright_cyan(s)
    WHITE = lambda s: _term.white(s)
    BRIGHT_WHITE = lambda s: _term.bright_white(s)
    ORANGE = lambda s: _term.color(208)(s)
    PINK = lambda s: _term.color(213)(s)
    GOLD = lambda s: _term.color(220)(s)
    PURPLE = lambda s: _term.color(135)(s)
    BROWN = lambda s: _term.color(130)(s)
    SILVER = lambda s: _term.color(250)(s)
    LIME = lambda s: _term.color(118)(s)
    TEAL = lambda s: _term.color(30)(s)
    CORAL = lambda s: _term.color(209)(s)
    LAVENDER = lambda s: _term.color(183)(s)

C = ItemColors  # Shorthand


# Mini icons for habitat items: (char, color_func)
# These are single characters (or 2-char max) for compact playfield display
HABITAT_ICONS = {
    # ============ TOYS ============
    "toy_ball": ("●", C.BRIGHT_RED),
    "toy_blocks": ("▦", C.BRIGHT_YELLOW),
    "toy_trumpet": ("♪", C.GOLD),
    "toy_skateboard": ("═", C.BROWN),
    "toy_piano": ("♫", C.BRIGHT_WHITE),
    "toy_trampoline": ("⌂", C.BRIGHT_MAGENTA),
    "toy_slide": ("╱", C.BRIGHT_CYAN),
    "toy_swing": ("◯", C.BROWN),
    "toy_seesaw": ("⇌", C.GREEN),
    "toy_sandbox": ("▒", C.YELLOW),
    "squeaky_toy": ("!", C.BRIGHT_YELLOW),
    "rubber_duck": ("♦", C.BRIGHT_YELLOW),
    "frisbee": ("◎", C.BRIGHT_RED),
    "toy_car": ("▄", C.BRIGHT_RED),
    "jump_rope": ("∿", C.PINK),
    "yo_yo": ("◉", C.BRIGHT_GREEN),
    "kite": ("◇", C.BRIGHT_MAGENTA),
    "skateboard": ("═", C.ORANGE),
    "trampoline": ("⌂", C.PURPLE),
    "telescope": ("◎", C.SILVER),
    "easel": ("▭", C.BROWN),
    "drums": ("◉", C.ORANGE),
    
    # ============ FURNITURE ============
    "chair_wood": ("▌", C.BROWN),
    "chair_throne": ("♔", C.GOLD),
    "table_small": ("▬", C.BROWN),
    "bed_small": ("▀", C.PURPLE),
    "bed_king": ("▀", C.GOLD),
    "couch": ("▐", C.BRIGHT_RED),
    "bookshelf": ("▓", C.BROWN),
    "bookshelf_wood": ("▓", C.BROWN),
    "desk": ("▬", C.BROWN),
    "desk_writing": ("▬", C.TEAL),
    "lamp_floor": ("⌐", C.BRIGHT_YELLOW),
    "mirror": ("◐", C.SILVER),
    "mirror_standing": ("◐", C.SILVER),
    "cushion": ("●", C.PINK),
    "dresser": ("▓", C.BROWN),
    "piano": ("♪", C.BRIGHT_WHITE),
    "wardrobe": ("▌", C.PURPLE),
    "sofa_fancy": ("▐", C.BRIGHT_MAGENTA),
    "coffee_table": ("▬", C.BROWN),
    "bar_cart": ("▯", C.SILVER),
    "grandfather_clock": ("◷", C.BROWN),
    "rocking_horse": ("◠", C.BROWN),
    "cabinet": ("▓", C.TEAL),
    "fireplace": ("🔥", C.ORANGE),
    "tv_stand": ("▣", C.SILVER),
    "bean_bag": ("◖", C.LIME),
    "golden_throne": ("♛", C.GOLD),
    
    # ============ WATER FEATURES ============
    "pool_kiddie": ("≈", C.BRIGHT_CYAN),
    "pool_large": ("≋", C.BRIGHT_BLUE),
    "fountain_small": ("⍨", C.BRIGHT_CYAN),
    "fountain_decorative": ("⍨", C.TEAL),
    "fountain_grand": ("⍨", C.BRIGHT_BLUE),
    "pond": ("≈", C.TEAL),
    "sprinkler": ("╦", C.BRIGHT_CYAN),
    "sprinkler_system": ("╩", C.BRIGHT_CYAN),
    "waterfall": ("║", C.BRIGHT_BLUE),
    "waterfall_mini": ("│", C.BRIGHT_CYAN),
    "hot_tub": ("○", C.BRIGHT_CYAN),
    "hot_tub_deluxe": ("◎", C.TEAL),
    "birdbath": ("╤", C.SILVER),
    "birdbath_garden": ("╤", C.GREEN),
    "water_slide": ("╲", C.BRIGHT_CYAN),
    "water_slide_mega": ("╲", C.BRIGHT_BLUE),
    "koi_pond": ("≋", C.ORANGE),
    "wave_pool": ("≈", C.BRIGHT_BLUE),
    "lazy_river": ("～", C.TEAL),
    "aquarium_large": ("▣", C.BRIGHT_CYAN),
    
    # ============ PLANTS ============
    "plant_small": ("♣", C.GREEN),
    "plant_potted": ("♠", C.GREEN),
    "plant_fern": ("❧", C.BRIGHT_GREEN),
    "plant_cactus": ("┃", C.LIME),
    "flower_pot": ("✿", C.PINK),
    "flower_rose": ("❀", C.BRIGHT_RED),
    "flower_daisy": ("✾", C.BRIGHT_YELLOW),
    "flower_tulip": ("✿", C.BRIGHT_MAGENTA),
    "flower_sunflower": ("✺", C.BRIGHT_YELLOW),
    "bush_small": ("♧", C.GREEN),
    "bush_hedge": ("▓", C.GREEN),
    "tree_small": ("♠", C.BRIGHT_GREEN),
    "tree_bonsai": ("♣", C.GREEN),
    "tree_cherry": ("✿", C.PINK),
    "tree_palm": ("╫", C.LIME),
    "tree_pine": ("▲", C.GREEN),
    "tree_oak": ("♠", C.BROWN),
    "tree_willow": ("≀", C.GREEN),
    "flower_garden": ("❀", C.LAVENDER),
    "flower_exotic": ("✻", C.CORAL),
    "mushroom_patch": ("●", C.BROWN),
    "bamboo": ("║", C.LIME),
    "bamboo_grove": ("║", C.BRIGHT_GREEN),
    "topiary": ("◆", C.GREEN),
    "bonsai_zen": ("♣", C.TEAL),
    "cactus_garden": ("┃", C.GREEN),
    "orchid": ("✿", C.PURPLE),
    "lotus": ("❁", C.PINK),
    "venus_flytrap": ("✦", C.LIME),
    "giant_flower": ("✼", C.BRIGHT_MAGENTA),
    "carnivore_plant": ("✦", C.BRIGHT_GREEN),
    "magic_beanstalk": ("╠", C.LIME),
    "crystal_tree": ("◆", C.BRIGHT_CYAN),
    
    # ============ DECORATIONS ============
    "lamp_table": ("○", C.BRIGHT_YELLOW),
    "lamp_lava": ("○", C.ORANGE),
    "lamp_neon": ("○", C.BRIGHT_MAGENTA),
    "rug_small": ("▬", C.BRIGHT_RED),
    "rug_fancy": ("▬", C.GOLD),
    "poster": ("▭", C.BRIGHT_CYAN),
    "poster_duck": ("▭", C.BRIGHT_YELLOW),
    "painting": ("▭", C.PURPLE),
    "painting_duck": ("▭", C.GOLD),
    "statue_small": ("♙", C.SILVER),
    "statue_duck": ("♙", C.GOLD),
    "statue_garden": ("♙", C.GREEN),
    "globe": ("◎", C.BRIGHT_BLUE),
    "clock_wall": ("◷", C.BROWN),
    "clock_cuckoo": ("◷", C.ORANGE),
    "flag_duck": ("⚑", C.BRIGHT_YELLOW),
    "pennant": ("▷", C.BRIGHT_RED),
    "string_lights": ("*", C.BRIGHT_YELLOW),
    "disco_ball": ("◎", C.SILVER),
    "trophy": ("⚱", C.GOLD),
    "trophy_gold": ("⚱", C.BRIGHT_YELLOW),
    "crown_display": ("♛", C.GOLD),
    "chandelier": ("✧", C.GOLD),
    "tapestry": ("▓", C.PURPLE),
    "mobile": ("☆", C.BRIGHT_CYAN),
    "wind_chime": ("♫", C.SILVER),
    "lantern": ("◯", C.ORANGE),
    "lantern_paper": ("◯", C.BRIGHT_RED),
    "fairy_lights": ("✦", C.BRIGHT_MAGENTA),
    "banner": ("▌", C.BRIGHT_RED),
    "garland": ("≈", C.GREEN),
    "dreamcatcher": ("◎", C.LAVENDER),
    "crystal": ("◆", C.BRIGHT_CYAN),
    "gem_display": ("◆", C.BRIGHT_MAGENTA),
    "aurora_lamp": ("≋", C.BRIGHT_CYAN),
    "rainbow_arch": ("◠", C.BRIGHT_MAGENTA),
    "hologram": ("◇", C.BRIGHT_CYAN),
    "galaxy_projector": ("✦", C.PURPLE),
    "ice_sculpture": ("◇", C.BRIGHT_CYAN),
    "diamond_display": ("◆", C.BRIGHT_WHITE),
    
    # ============ OUTDOOR ============
    "fence_wood": ("╫", C.BROWN),
    "fence_picket": ("╫", C.BRIGHT_WHITE),
    "fence_fancy": ("╫", C.GOLD),
    "path_stone": ("▪", C.SILVER),
    "path_brick": ("▪", C.BRIGHT_RED),
    "bench": ("▬", C.BROWN),
    "bench_park": ("▬", C.GREEN),
    "gazebo": ("⌂", C.BRIGHT_WHITE),
    "pergola": ("╬", C.BROWN),
    "umbrella_patio": ("◠", C.BRIGHT_RED),
    "umbrella_beach": ("◠", C.BRIGHT_YELLOW),
    "sandbox": ("▒", C.YELLOW),
    "swing_set": ("◯", C.BRIGHT_RED),
    "garden_gnome": ("♙", C.BRIGHT_RED),
    "bird_feeder": ("╤", C.BROWN),
    "butterfly_house": ("▭", C.BRIGHT_MAGENTA),
    "beehive": ("▓", C.BRIGHT_YELLOW),
    "nest_box": ("▓", C.BROWN),
    "hammock": ("～", C.LIME),
    "fire_pit": ("◎", C.ORANGE),
    "bbq_grill": ("▓", C.SILVER),
    "picnic_table": ("▬", C.BROWN),
    "tent": ("△", C.BRIGHT_GREEN),
    "telescope_yard": ("◎", C.PURPLE),
    "weather_vane": ("╬", C.SILVER),
    "mailbox": ("▌", C.BRIGHT_RED),
    "wishing_well": ("○", C.SILVER),
    "sundial": ("◎", C.GOLD),
    "windmill": ("╳", C.BROWN),
    "lighthouse": ("▲", C.BRIGHT_WHITE),
    "treehouse": ("▲", C.BROWN),
    "castle_small": ("♜", C.SILVER),
    "roller_coaster": ("≈", C.BRIGHT_RED),
    "ferris_wheel": ("◎", C.BRIGHT_CYAN),
    "rocket_ship": ("▲", C.SILVER),
    
    # ============ SPECIAL/LEGENDARY ============
    "golden_statue": ("♛", C.GOLD),
    "rainbow_fountain": ("⍨", C.BRIGHT_MAGENTA),
    "enchanted_tree": ("♠", C.BRIGHT_MAGENTA),
    "meteor": ("★", C.ORANGE),
    "ufo": ("◎", C.BRIGHT_GREEN),
    "time_machine": ("◎", C.PURPLE),
    "portal": ("◎", C.BRIGHT_CYAN),
    "dragon_egg": ("◎", C.BRIGHT_RED),
    "treasure_chest": ("▓", C.GOLD),
    "magic_mirror": ("◐", C.BRIGHT_MAGENTA),
    "wizard_tower": ("▲", C.PURPLE),
    "enchanted_pond": ("≈", C.BRIGHT_MAGENTA),
    "fairy_garden": ("✿", C.LAVENDER),
    "unicorn_stable": ("▓", C.PINK),
    "stargate": ("○", C.BRIGHT_CYAN),
    "warp_pipe": ("║", C.BRIGHT_GREEN),
    "infinity_pool": ("≋", C.TEAL),
    "cloud_maker": ("○", C.BRIGHT_WHITE),
    "aurora_generator": ("≈", C.BRIGHT_CYAN),
    "moon_rock": ("◎", C.SILVER),
    "star_fragment": ("★", C.BRIGHT_YELLOW),
    "cosmic_egg": ("◎", C.PURPLE),
    "black_hole": ("◉", C.PURPLE),
    "quack_shrine": ("♛", C.BRIGHT_YELLOW),
}


def get_habitat_icon(item_id: str):
    """
    Get the mini icon for a habitat item.
    Returns (char, color_func) tuple or None if not found.
    """
    return HABITAT_ICONS.get(item_id)


def render_habitat_icon(item_id: str) -> str:
    """
    Render a habitat item icon as a colored string.
    Returns the colored character or '?' if item not found.
    """
    icon = HABITAT_ICONS.get(item_id)
    if icon:
        char, color_func = icon
        return color_func(char) if color_func else char
    return "?"
