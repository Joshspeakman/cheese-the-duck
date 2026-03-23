"""
Main Menu Structure - Defines the hierarchical menu categories and items.

NOTE: Do not use Unicode emoji icons (🦆, 🌍, etc.) in this file.
Use ASCII characters only for terminal compatibility.
"""
from ui.menu_selector import MenuItem, MenuCategory


def build_main_menu_categories() -> list:
    """
    Build the main menu categories with their items.
    Returns a list of MenuCategory objects.
    
    NOTE: Use ASCII icons only, not Unicode emoji.
    """
    return [
        MenuCategory(
            id="care",
            label="Duck Care",
            icon="<>",
            items=[
                MenuItem("feed", "Feed [F]", "Give your duck some food"),
                MenuItem("play", "Play [P]", "Have fun with your duck"),
                MenuItem("clean", "Clean [L]", "Give your duck a bath"),
                MenuItem("pet", "Pet [D]", "Show your duck some love"),
                MenuItem("sleep", "Sleep [Z]", "Put your duck to bed"),
                MenuItem("use", "Use Item [U]", "Use an item on your duck"),
                MenuItem("inventory", "Inventory [I]", "Check your items"),
            ]
        ),
        MenuCategory(
            id="items",
            label="Items & Shop",
            icon="$",
            items=[
                MenuItem("shop", "Shop [B]", "Buy items with coins"),
                MenuItem("trade", "Trading Post [<]", "Trade with visiting merchants"),
                MenuItem("craft", "Crafting [C]", "Create items from materials"),
                MenuItem("build", "Building [R]", "Construct structures"),
                MenuItem("decorate", "Decorations [V]", "Place furniture and decorations"),
            ]
        ),
        MenuCategory(
            id="world",
            label="World",
            icon="*",
            items=[
                MenuItem("explore", "Explore [E]", "Search the current area for resources"),
                MenuItem("travel", "Travel [A]", "Visit other locations"),
                MenuItem("garden", "Garden [9]", "Plant and harvest crops"),
                MenuItem("weather", "Weather [W]", "Weather activities"),
                MenuItem("treasure", "Treasure Hunt [6]", "Search for buried treasure"),
            ]
        ),
        MenuCategory(
            id="activities",
            label="Activities",
            icon="#",
            items=[
                MenuItem("minigames", "Mini-games [J]", "Play games for rewards"),
                MenuItem("tricks", "Tricks [7]", "Teach and perform tricks"),
                MenuItem("festivals", "Festivals [0]", "Seasonal celebrations"),
                MenuItem("photo", "Take Photo [;]", "Capture a moment"),
                MenuItem("diary", "Diary [=]", "Write in your diary"),
            ]
        ),
        MenuCategory(
            id="myduck",
            label="My Duck",
            icon="@",
            items=[
                MenuItem("talk", "Talk [T]", "Have a conversation"),
                MenuItem("stats", "View Stats [S]", "See detailed statistics"),
                MenuItem("goals", "Goals [G]", "View your objectives"),
                MenuItem("scrapbook", "Scrapbook [Y]", "Memory album"),
                MenuItem("titles", "Titles [!]", "Manage duck titles"),
                MenuItem("facts", "Duck Fact [K]", "Learn about ducks"),
            ]
        ),
        MenuCategory(
            id="collections",
            label="Collections",
            icon="+",
            items=[
                MenuItem("collectibles", "Collectibles [']", "View your collection"),
                MenuItem("badges", "Badges", "View earned achievement badges"),
                MenuItem("prestige", "Prestige [8]", "Rebirth for bonuses"),
                MenuItem("secrets", "Secrets Book [\\]", "Hidden discoveries"),
            ]
        ),
        MenuCategory(
            id="settings_cat",
            label="Settings",
            icon="=",
            items=[
                MenuItem("settings", "Settings", "Audio, display, and game options"),
                MenuItem("sound", "Toggle Sound [N]", "Turn sound on/off"),
                MenuItem("music", "Toggle Music [M]", "Turn music on/off"),
                MenuItem("radio", "Radio", "Nook Radio"),
                MenuItem("help", "Help [H]", "View controls and tips"),
                MenuItem("save_slots", "Save Slots [/]", "Manage save files"),
                MenuItem("reset_game", "Reset Game", "WARNING: Deletes ALL progress!"),
                MenuItem("quit", "Return to Title [Q]", "Save game and return to title screen"),
            ]
        ),
    ]


# Action ID to method name mapping
# Used by game.py to route menu selections to the appropriate handler
MENU_ACTIONS = {
    # Duck Care
    "feed": "_perform_interaction_feed",
    "play": "_perform_interaction_play", 
    "clean": "_perform_interaction_clean",
    "pet": "_perform_interaction_pet",
    "sleep": "_perform_interaction_sleep",
    "use": "_show_use_menu",
    "inventory": "_toggle_inventory",
    
    # Items & Shop
    "shop": "_toggle_shop",
    "trade": "_show_trading_menu",
    "craft": "_show_crafting_menu",
    "build": "_show_building_menu",
    "decorate": "_show_decorations_menu",
    
    # World
    "explore": "_do_explore",
    "travel": "_show_areas_menu",
    "garden": "_show_garden_menu",
    "garden_view": "_show_garden_view",
    "garden_water": "_water_all_plants",
    "garden_harvest": "_harvest_all_plants",
    "weather": "_show_weather_activities",
    "treasure": "_show_treasure_hunt",
    
    # Activities
    "minigames": "_show_minigames_menu",
    "tricks": "_show_tricks_menu",
    "festivals": "_show_festival_menu",
    "photo": "_take_diary_photo",
    "diary": "_show_enhanced_diary",
    
    # My Duck
    "talk": "_start_talk_mode",
    "stats": "_toggle_stats",
    "goals": "_toggle_goals",
    "scrapbook": "_show_scrapbook",
    "titles": "_show_titles_menu",
    "facts": "_show_duck_fact",
    
    # Collections
    "collectibles": "_show_collectibles_album",
    "badges": "_show_badges_menu",
    "prestige": "_show_prestige_menu",
    "secrets": "_show_secrets_book",
    
    # Settings
    "settings": "_open_settings_menu",
    "sound": "_toggle_sound",
    "music": "_toggle_music",
    "radio": "_show_radio_menu",
    "nook_radio_toggle": "_toggle_nook_radio",
    "help": "_toggle_help",
    "save_slots": "_show_save_slots_menu",
    "reset_game": "_start_reset_confirmation",
    "quit": "_return_to_title",
}


# =============================================================================
# MASTER MENU TREE - Hierarchical menu structure for MasterMenuPanel
# =============================================================================

def _get_crafting_items(game):
    """Build crafting submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.crafting import RECIPES as CRAFTING_RECIPES, CraftingCategory
        
        # Group by category
        categories = {}
        for recipe_id, recipe in CRAFTING_RECIPES.items():
            cat_name = recipe.category.value if hasattr(recipe.category, 'value') else str(recipe.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if can craft
            can_craft = False
            if game and hasattr(game, 'crafting') and hasattr(game, 'materials'):
                skill = game.crafting.crafting_skill if hasattr(game.crafting, 'crafting_skill') else 0
                level = game.progression.level if hasattr(game, 'progression') and game.progression else 0
                can_craft, _ = recipe.can_craft(game.materials, skill=skill, level=level)
            
            categories[cat_name].append(MasterMenuItem(
                id=f"craft_{recipe_id}",
                label=recipe.name,
                action=f"craft_{recipe_id}",
                completed=can_craft,  # Show * if craftable
                enabled=True
            ))
        
        # Create category submenus
        for cat_name, cat_items in sorted(categories.items()):
            items.append(MasterMenuItem(
                id=f"craft_cat_{cat_name}",
                label=cat_name.replace('_', ' ').title(),
                children=cat_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="craft_none", label="No recipes", enabled=False))
    
    return items


def _get_building_items(game):
    """Build building submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.building import BLUEPRINTS as STRUCTURE_BLUEPRINTS
        
        # Group by type
        types = {}
        for bp_id, bp in STRUCTURE_BLUEPRINTS.items():
            type_name = bp.structure_type.value if hasattr(bp.structure_type, 'value') else str(bp.structure_type)
            if type_name not in types:
                types[type_name] = []
            
            # Check if owned/built
            owned = False
            if game and hasattr(game, 'building'):
                owned = bp_id in [s.blueprint_id for s in game.building.structures if s.status.value == 'complete']
            
            # Check unlock level
            unlocked = True
            if game and hasattr(game, 'progression') and game.progression:
                unlocked = game.progression.level >= bp.unlock_level
            
            types[type_name].append(MasterMenuItem(
                id=f"build_{bp_id}",
                label=bp.name,
                action=f"build_{bp_id}",
                completed=owned,
                enabled=unlocked
            ))
        
        for type_name, type_items in sorted(types.items()):
            items.append(MasterMenuItem(
                id=f"build_type_{type_name}",
                label=type_name.replace('_', ' ').title(),
                children=type_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="build_none", label="No blueprints", enabled=False))
    
    return items


def _get_areas_items(game):
    """Build travel/areas submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.exploration import BiomeType, AREA_ART
        
        # Get discovered areas
        discovered = set()
        current_area = None
        if game and hasattr(game, 'exploration') and game.exploration:
            discovered = game.exploration.discovered_areas
            if game.exploration.current_area:
                current_area = game.exploration.current_area.name
        
        # Group locations by biome (simplified)
        for area_name in sorted(AREA_ART.keys()):
            is_current = (area_name == current_area)
            is_discovered = area_name in discovered or area_name == "Home Pond"
            
            items.append(MasterMenuItem(
                id=f"travel_{area_name.lower().replace(' ', '_')}",
                label=f"{'@' if is_current else ' '} {area_name}",
                action=f"travel_{area_name}",
                completed=is_discovered,
                enabled=is_discovered or area_name == "Home Pond"
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="travel_none", label="No areas", enabled=False))
    
    return items


def _get_minigames_items(game):
    """Build minigames submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.minigames import MiniGameType
        
        games_list = [
            ("bread_catch", "Bread Catch", "Catch falling bread!"),
            ("bug_chase", "Bug Chase", "Chase the bugs!"),
            ("memory_match", "Memory Match", "Match the pairs!"),
            ("duck_race", "Duck Race", "Race other ducks!"),
        ]
        
        for game_id, name, desc in games_list:
            # Check high score
            has_score = False
            if game and hasattr(game, 'minigame_high_scores'):
                has_score = game.minigame_high_scores.get(game_id, 0) > 0
            
            items.append(MasterMenuItem(
                id=f"minigame_{game_id}",
                label=name,
                action=f"minigame_{game_id}",
                completed=has_score
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="minigame_none", label="No games", enabled=False))
    
    return items


def _get_shop_items(game):
    """Build shop submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.shop import SHOP_ITEMS, ItemCategory
        
        # Group by category
        categories = {}
        for item_id, item in SHOP_ITEMS.items():
            cat_name = item.category.value if hasattr(item.category, 'value') else str(item.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if owned
            owned = False
            if game and hasattr(game, 'duck') and game.duck:
                if hasattr(game.duck, 'inventory'):
                    owned = item_id in game.duck.inventory
            
            # Check unlock (level is on progression, not duck)
            unlocked = True
            if game and hasattr(game, 'progression') and game.progression:
                unlocked = game.progression.level >= item.unlock_level
            
            categories[cat_name].append(MasterMenuItem(
                id=f"shop_{item_id}",
                label=f"{item.name} ({item.cost}c)",
                action=f"shop_{item_id}",
                completed=owned,
                enabled=unlocked
            ))
        
        for cat_name, cat_items in sorted(categories.items()):
            items.append(MasterMenuItem(
                id=f"shop_cat_{cat_name}",
                label=cat_name.replace('_', ' ').title(),
                children=cat_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="shop_none", label="Shop unavailable", enabled=False))
    
    return items


def _get_tricks_items(game):
    """Build tricks submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from duck.tricks import TRICKS as TRICK_LIBRARY, TrickCategory
        
        # Group by category
        categories = {}
        for trick_id, trick in TRICK_LIBRARY.items():
            cat_name = trick.category.value if hasattr(trick.category, 'value') else str(trick.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if learned
            learned = False
            if game and hasattr(game, 'tricks') and game.tricks:
                learned = trick_id in game.tricks.learned_tricks
            
            categories[cat_name].append(MasterMenuItem(
                id=f"trick_{trick_id}",
                label=trick.name,
                action=f"trick_{trick_id}",
                completed=learned
            ))
        
        for cat_name, cat_items in sorted(categories.items()):
            items.append(MasterMenuItem(
                id=f"tricks_cat_{cat_name}",
                label=cat_name.replace('_', ' ').title(),
                children=cat_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="tricks_none", label="No tricks", enabled=False))
    
    return items


def _get_garden_items(game):
    """Build garden submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    # Garden actions
    items.append(MasterMenuItem(id="garden_view", label="View Garden", action="garden_view"))
    items.append(MasterMenuItem(id="garden_water", label="Water Plants", action="garden_water"))
    items.append(MasterMenuItem(id="garden_harvest", label="Harvest", action="garden_harvest"))
    
    try:
        from world.garden import SEEDS as SEED_SHOP
        
        # Seeds submenu
        seed_items = []
        for seed_id, seed_data in SEED_SHOP.items():
            name = seed_data.get('plant', seed_id).replace('_', ' ').title()
            cost = seed_data.get('cost', 0)
            seed_items.append(MasterMenuItem(
                id=f"garden_plant_{seed_id}",
                label=f"{name} ({cost}c)",
                action=f"garden_plant_{seed_id}"
            ))
        
        if seed_items:
            items.append(MasterMenuItem(
                id="garden_seeds",
                label="Plant Seeds",
                children=seed_items
            ))
    except ImportError as e:
        pass  # Module not available
    
    return items


def _get_decorations_items(game):
    """Build decorations submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.decorations import DECORATIONS, DecorationCategory
        
        # Group by category
        categories = {}
        for dec_id, dec in DECORATIONS.items():
            cat_name = dec.category.value if hasattr(dec.category, 'value') else str(dec.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if owned (in unlocked_decorations list or currently placed)
            owned = False
            if game and hasattr(game, 'home') and game.home:
                # Check if decoration is unlocked or placed
                if hasattr(game.home, 'unlocked_decorations'):
                    owned = dec_id in game.home.unlocked_decorations
                elif hasattr(game.home, 'decorations'):
                    owned = dec_id in game.home.decorations.values()
            
            categories[cat_name].append(MasterMenuItem(
                id=f"decor_{dec_id}",
                label=f"{dec.name} ({dec.price}c)",
                action=f"decor_{dec_id}",
                completed=owned
            ))
        
        for cat_name, cat_items in sorted(categories.items()):
            items.append(MasterMenuItem(
                id=f"decor_cat_{cat_name}",
                label=cat_name.replace('_', ' ').title(),
                children=cat_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="decor_none", label="No decorations", enabled=False))
    
    return items


def _get_collectibles_items(game):
    """Build collectibles submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.collectibles import SETS as COLLECTION_SETS, COLLECTIBLES
        
        for set_id, set_data in COLLECTION_SETS.items():
            # Count owned in set
            owned_count = 0
            total_count = 0
            set_items = []
            
            for col_id, col in COLLECTIBLES.items():
                if col.set_id == set_id:
                    total_count += 1
                    owned = False
                    if game and hasattr(game, 'collectibles') and game.collectibles:
                        owned = col_id in game.collectibles.owned
                        if owned:
                            owned_count += 1
                    
                    set_items.append(MasterMenuItem(
                        id=f"col_{col_id}",
                        label=col.name,
                        action=f"col_{col_id}",
                        completed=owned,
                        enabled=owned  # Can only view owned ones
                    ))
            
            items.append(MasterMenuItem(
                id=f"col_set_{set_id}",
                label=f"{set_data.name} ({owned_count}/{total_count})",
                children=set_items,
                completed=(owned_count == total_count and total_count > 0)
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="col_none", label="No collectibles", enabled=False))
    
    return items


def _get_titles_items(game):
    """Build titles submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from duck.titles import TITLES as TITLE_LIBRARY, TitleCategory
        
        # Group by category
        categories = {}
        for title_id, title in TITLE_LIBRARY.items():
            cat_name = title.category.value if hasattr(title.category, 'value') else str(title.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if earned
            earned = False
            equipped = False
            if game and hasattr(game, 'titles') and game.titles:
                earned = title_id in game.titles.earned_titles
                equipped = game.titles.equipped_title == title_id
            
            prefix = "@ " if equipped else ""
            categories[cat_name].append(MasterMenuItem(
                id=f"title_{title_id}",
                label=f"{prefix}{title.name}",
                action=f"title_{title_id}",
                completed=earned,
                enabled=earned
            ))
        
        for cat_name, cat_items in sorted(categories.items()):
            items.append(MasterMenuItem(
                id=f"titles_cat_{cat_name}",
                label=cat_name.replace('_', ' ').title(),
                children=cat_items
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="titles_none", label="No titles", enabled=False))
    
    return items


def _get_radio_items(game):
    """Build Nook Radio menu item — requires owning the nook_radio shop item."""
    from ui.menu_selector import MasterMenuItem
    items = []

    # Check if player owns the Nook Radio item
    if not hasattr(game, 'habitat') or not game.habitat.owns_item("nook_radio"):
        items.append(MasterMenuItem(
            id="radio_locked",
            label="Buy Nook Radio from the shop!",
            enabled=False
        ))
        return items

    try:
        from audio.radio import get_radio_player

        radio = get_radio_player()

        if not radio.player_available:
            items.append(MasterMenuItem(
                id="radio_status",
                label=radio.player_status,
                enabled=False
            ))
            return items

        if radio.is_playing:
            items.append(MasterMenuItem(
                id="radio_nook_radio",
                label="▶ Nook Radio (Playing)",
                action="radio_nook_radio",
                completed=True
            ))
            items.append(MasterMenuItem(
                id="radio_stop",
                label="■ Radio Off",
                action="radio_stop"
            ))
        else:
            items.append(MasterMenuItem(
                id="radio_nook_radio",
                label="♪ Nook Radio",
                action="radio_nook_radio"
            ))
    except ImportError as e:
        items.append(MasterMenuItem(id="radio_none", label="Radio unavailable", enabled=False))

    return items


def _get_nook_radio_item(game):
    """Build Nook Radio menu item with dynamic label showing play status."""
    from ui.menu_selector import MasterMenuItem
    
    try:
        from audio.radio import get_radio_player
        radio = get_radio_player()
        
        if not radio.player_available:
            return [MasterMenuItem(
                id="nook_radio",
                label="Nook Radio (unavailable)",
                action="nook_radio_toggle",
                enabled=False
            )]
        
        if radio.is_playing:
            return [MasterMenuItem(
                id="nook_radio",
                label="♪ Nook Radio ♪ (playing)",
                action="nook_radio_toggle"
            )]
        else:
            return [MasterMenuItem(
                id="nook_radio",
                label="Nook Radio",
                action="nook_radio_toggle"
            )]
    except ImportError as e:
        return [MasterMenuItem(
            id="nook_radio",
            label="Nook Radio (unavailable)",
            action="nook_radio_toggle",
            enabled=False
        )]


def build_master_menu_tree():
    """
    Build the master menu tree structure.
    Returns a list of MasterMenuItem for the root level.
    """
    from ui.menu_selector import MasterMenuItem
    
    return [
        # Duck Care (quick actions + item use + inventory)
        MasterMenuItem(
            id="care",
            label="Duck Care",
            children=[
                MasterMenuItem(id="feed", label="Feed [F]", action="feed"),
                MasterMenuItem(id="play", label="Play [P]", action="play"),
                MasterMenuItem(id="clean", label="Clean [L]", action="clean"),
                MasterMenuItem(id="pet", label="Pet [D]", action="pet"),
                MasterMenuItem(id="sleep", label="Sleep [Z]", action="sleep"),
                MasterMenuItem(id="use", label="Use Item [U]", action="use"),
                MasterMenuItem(id="inventory", label="Inventory [I]", action="inventory"),
            ]
        ),
        
        # Items & Shop (all commerce and crafting)
        MasterMenuItem(
            id="items",
            label="Items & Shop",
            children=[
                MasterMenuItem(id="shop", label="Shop [B]", action="shop"),
                MasterMenuItem(id="trade", label="Trading Post [<]", action="trade"),
                MasterMenuItem(id="craft", label="Crafting [C]", children=_get_crafting_items),
                MasterMenuItem(id="build", label="Building [R]", children=_get_building_items),
                MasterMenuItem(id="decorate", label="Decorations [V]", children=_get_decorations_items),
            ]
        ),
        
        # World (exploration, travel, outdoor)
        MasterMenuItem(
            id="world",
            label="World",
            children=[
                MasterMenuItem(id="explore", label="Explore [E]", action="explore"),
                MasterMenuItem(id="travel", label="Travel [A]", children=_get_areas_items),
                MasterMenuItem(id="garden", label="Garden [9]", children=_get_garden_items),
                MasterMenuItem(id="weather", label="Weather [W]", action="weather"),
                MasterMenuItem(id="treasure", label="Treasure Hunt [6]", action="treasure"),
            ]
        ),
        
        # Activities
        MasterMenuItem(
            id="activities",
            label="Activities",
            children=[
                MasterMenuItem(id="minigames", label="Mini-games [J]", children=_get_minigames_items),
                MasterMenuItem(id="tricks", label="Tricks [7]", children=_get_tricks_items),
                MasterMenuItem(id="festivals", label="Festivals [0]", action="festivals"),
                MasterMenuItem(id="photo", label="Take Photo [;]", action="photo"),
                MasterMenuItem(id="diary", label="Diary [=]", action="diary"),
            ]
        ),
        
        # My Duck (duck info, conversation, progression)
        MasterMenuItem(
            id="myduck",
            label="My Duck",
            children=[
                MasterMenuItem(id="talk", label="Talk [T]", action="talk"),
                MasterMenuItem(id="stats", label="View Stats [S]", action="stats"),
                MasterMenuItem(id="goals", label="Goals [G]", action="goals"),
                MasterMenuItem(id="scrapbook", label="Scrapbook [Y]", action="scrapbook"),
                MasterMenuItem(id="titles", label="Titles [!]", children=_get_titles_items),
                MasterMenuItem(id="facts", label="Duck Fact [K]", action="facts"),
            ]
        ),
        
        # Collections
        MasterMenuItem(
            id="collections",
            label="Collections",
            children=[
                MasterMenuItem(id="collectibles", label="Collectibles [']", children=_get_collectibles_items),
                MasterMenuItem(id="badges", label="Badges", action="badges"),
                MasterMenuItem(id="prestige", label="Prestige [8]", action="prestige"),
                MasterMenuItem(id="secrets", label="Secrets Book [\\]", action="secrets"),
            ]
        ),
        
        # Settings
        MasterMenuItem(
            id="settings_cat",
            label="Settings",
            children=[
                MasterMenuItem(id="settings", label="Settings", action="settings"),
                MasterMenuItem(id="sound", label="Toggle Sound [N]", action="sound"),
                MasterMenuItem(id="music", label="Toggle Music [M]", action="music"),
                MasterMenuItem(id="radio", label="Radio", children=_get_radio_items),
                MasterMenuItem(id="help", label="Help [H]", action="help"),
                MasterMenuItem(id="save_slots", label="Save Slots [/]", action="save_slots"),
            ]
        ),

        # Save & return to title (at root level for easy access)
        MasterMenuItem(id="quit", label="Return to Title [Q]", action="quit"),
    ]
