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
                MenuItem("feed", "Feed", "Give your duck some food (F/1)"),
                MenuItem("play", "Play", "Have fun with your duck (P/2)"),
                MenuItem("clean", "Clean", "Give your duck a bath (L/3)"),
                MenuItem("pet", "Pet", "Show your duck some love (D/4)"),
                MenuItem("sleep", "Sleep", "Put your duck to bed (Z/5)"),
            ]
        ),
        MenuCategory(
            id="world",
            label="World & Building",
            icon="*",
            items=[
                MenuItem("explore", "Explore", "Search the current area for resources"),
                MenuItem("travel", "Travel", "Visit other locations"),
                MenuItem("craft", "Crafting", "Create items from materials"),
                MenuItem("build", "Building", "Construct structures"),
                MenuItem("decorate", "Decorations", "Place furniture and decorations"),
                MenuItem("trade", "Trading Post", "Trade with visiting merchants"),
                MenuItem("use", "Use Item", "Interact with placed items"),
            ]
        ),
        MenuCategory(
            id="social",
            label="Social & Info",
            icon="@",
            items=[
                MenuItem("talk", "Talk to Duck", "Have a conversation"),
                MenuItem("stats", "View Stats", "See detailed statistics"),
                MenuItem("inventory", "Inventory", "Check your items"),
                MenuItem("goals", "Goals", "View your objectives"),
                MenuItem("shop", "Shop", "Buy items with coins"),
            ]
        ),
        MenuCategory(
            id="activities",
            label="Activities",
            icon="#",
            items=[
                MenuItem("minigames", "Mini-games", "Play games for rewards"),
                MenuItem("tricks", "Tricks", "Teach and perform tricks"),
                MenuItem("garden", "Garden", "Plant and harvest crops"),
                MenuItem("festivals", "Festivals", "Seasonal celebrations"),
                MenuItem("diary", "Enhanced Diary", "Write in your diary"),
                MenuItem("photo", "Take Photo", "Capture a moment"),
            ]
        ),
        MenuCategory(
            id="collections",
            label="Collections & Legacy",
            icon="+",
            items=[
                MenuItem("collectibles", "Collectibles Album", "View your collection"),
                MenuItem("prestige", "Prestige/Legacy", "Rebirth for bonuses"),
                MenuItem("titles", "Titles & Nicknames", "Manage duck titles"),
                MenuItem("scrapbook", "Scrapbook", "Memory album"),
                MenuItem("secrets", "Secrets Book", "Hidden discoveries"),
            ]
        ),
        MenuCategory(
            id="other",
            label="Other",
            icon="=",
            items=[
                MenuItem("facts", "Random Duck Fact", "Learn about ducks"),
                MenuItem("settings", "Settings", "Audio, display, and game options"),
                MenuItem("sound", "Toggle Sound", "Turn sound on/off"),
                MenuItem("music", "Toggle Music", "Turn music on/off"),
                # MenuItem("save_slots", "Save Slots", "Manage save files"),  # Hidden for now
                MenuItem("help", "Help", "View controls and tips"),
                MenuItem("reset_game", "Reset Game", "WARNING: Deletes ALL progress!"),
                MenuItem("quit", "Save & Quit", "Save game and exit"),
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
    
    # World & Building
    "explore": "_do_explore",
    "travel": "_show_areas_menu",
    "craft": "_show_crafting_menu",
    "build": "_show_building_menu",
    "decorate": "_show_decorations_menu",
    "trade": "_show_trading_menu",
    "use": "_show_use_menu",
    
    # Social & Info
    "talk": "_start_talk_mode",
    "stats": "_toggle_stats",
    "inventory": "_toggle_inventory",
    "goals": "_toggle_goals",
    "shop": "_toggle_shop",
    
    # Activities
    "minigames": "_show_minigames_menu",
    "tricks": "_show_tricks_menu",
    "garden": "_show_garden_menu",
    "garden_view": "_show_garden_view",
    "garden_water": "_water_all_plants",
    "garden_harvest": "_harvest_all_plants",
    "festivals": "_show_festival_menu",
    "diary": "_show_enhanced_diary",
    "photo": "_take_diary_photo",
    
    # Collections & Legacy
    "collectibles": "_show_collectibles_album",
    "prestige": "_show_prestige_menu",
    "titles": "_show_titles_menu",
    "scrapbook": "_show_scrapbook",
    "secrets": "_show_secrets_book",
    
    # Other
    "facts": "_show_duck_fact",
    "settings": "_open_settings_menu",
    "sound": "_toggle_sound",
    "music": "_toggle_music",
    "save_slots": "_show_save_slots_menu",
    "help": "_toggle_help",
    "reset_game": "_start_reset_confirmation",
    "quit": "_quit_game",
}


# =============================================================================
# MASTER MENU TREE - Hierarchical menu structure for MasterMenuPanel
# =============================================================================

def _get_crafting_items(game):
    """Build crafting submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.crafting import CRAFTING_RECIPES, CraftingCategory
        
        # Group by category
        categories = {}
        for recipe_id, recipe in CRAFTING_RECIPES.items():
            cat_name = recipe.category.value if hasattr(recipe.category, 'value') else str(recipe.category)
            if cat_name not in categories:
                categories[cat_name] = []
            
            # Check if can craft
            can_craft = False
            if game and hasattr(game, 'crafting') and hasattr(game, 'materials'):
                result = game.crafting.can_craft(recipe_id, game.materials)
                can_craft = result.get('can_craft', False)
            
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
    except ImportError:
        items.append(MasterMenuItem(id="craft_none", label="No recipes", enabled=False))
    
    return items


def _get_building_items(game):
    """Build building submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.building import STRUCTURE_BLUEPRINTS
        
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
            if game and hasattr(game, 'duck') and game.duck:
                unlocked = game.duck.level >= bp.unlock_level
            
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
    except ImportError:
        items.append(MasterMenuItem(id="build_none", label="No blueprints", enabled=False))
    
    return items


def _get_areas_items(game):
    """Build travel/areas submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.exploration import BiomeType
        from ui.location_art import AREA_ART
        
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
    except ImportError:
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
    except ImportError:
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
    except ImportError:
        items.append(MasterMenuItem(id="shop_none", label="Shop unavailable", enabled=False))
    
    return items


def _get_tricks_items(game):
    """Build tricks submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from duck.tricks import TRICK_LIBRARY, TrickCategory
        
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
    except ImportError:
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
        from world.garden import SEED_SHOP
        
        # Seeds submenu
        seed_items = []
        for seed_id, seed_data in SEED_SHOP.items():
            name = seed_data.get('name', seed_id)
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
    except ImportError:
        pass
    
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
    except ImportError:
        items.append(MasterMenuItem(id="decor_none", label="No decorations", enabled=False))
    
    return items


def _get_collectibles_items(game):
    """Build collectibles submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from world.collectibles import COLLECTION_SETS, COLLECTIBLES
        
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
                        owned = col_id in game.collectibles.owned_collectibles
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
    except ImportError:
        items.append(MasterMenuItem(id="col_none", label="No collectibles", enabled=False))
    
    return items


def _get_titles_items(game):
    """Build titles submenu items dynamically."""
    from ui.menu_selector import MasterMenuItem
    items = []
    
    try:
        from duck.titles import TITLE_LIBRARY, TitleCategory
        
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
    except ImportError:
        items.append(MasterMenuItem(id="titles_none", label="No titles", enabled=False))
    
    return items


def build_master_menu_tree():
    """
    Build the master menu tree structure.
    Returns a list of MasterMenuItem for the root level.
    """
    from ui.menu_selector import MasterMenuItem
    
    return [
        # Duck Care (quick actions)
        MasterMenuItem(
            id="care",
            label="Duck Care",
            children=[
                MasterMenuItem(id="feed", label="Feed", action="feed"),
                MasterMenuItem(id="play", label="Play", action="play"),
                MasterMenuItem(id="clean", label="Clean", action="clean"),
                MasterMenuItem(id="pet", label="Pet", action="pet"),
                MasterMenuItem(id="sleep", label="Sleep", action="sleep"),
            ]
        ),
        
        # World & Building
        MasterMenuItem(
            id="world",
            label="World",
            children=[
                MasterMenuItem(id="explore", label="Explore", action="explore"),
                MasterMenuItem(id="travel", label="Travel", children=_get_areas_items),
                MasterMenuItem(id="craft", label="Crafting", children=_get_crafting_items),
                MasterMenuItem(id="build", label="Building", children=_get_building_items),
                MasterMenuItem(id="decorate", label="Decorations", children=_get_decorations_items),
                MasterMenuItem(id="trade", label="Trading Post", action="trade"),
                MasterMenuItem(id="use", label="Use Item", action="use"),
            ]
        ),
        
        # Social & Info
        MasterMenuItem(
            id="social",
            label="Social",
            children=[
                MasterMenuItem(id="talk", label="Talk to Duck", action="talk"),
                MasterMenuItem(id="stats", label="View Stats", action="stats"),
                MasterMenuItem(id="inventory", label="Inventory", action="inventory"),
                MasterMenuItem(id="goals", label="Goals", action="goals"),
                MasterMenuItem(id="shop", label="Shop", children=_get_shop_items),
            ]
        ),
        
        # Activities
        MasterMenuItem(
            id="activities",
            label="Activities",
            children=[
                MasterMenuItem(id="minigames", label="Mini-games", children=_get_minigames_items),
                MasterMenuItem(id="tricks", label="Tricks", children=_get_tricks_items),
                MasterMenuItem(id="garden", label="Garden", children=_get_garden_items),
                MasterMenuItem(id="festivals", label="Festivals", action="festivals"),
                MasterMenuItem(id="diary", label="Enhanced Diary", action="diary"),
                MasterMenuItem(id="photo", label="Take Photo", action="photo"),
            ]
        ),
        
        # Collections & Legacy
        MasterMenuItem(
            id="collections",
            label="Collections",
            children=[
                MasterMenuItem(id="collectibles", label="Collectibles", children=_get_collectibles_items),
                MasterMenuItem(id="prestige", label="Prestige", action="prestige"),
                MasterMenuItem(id="titles", label="Titles", children=_get_titles_items),
                MasterMenuItem(id="scrapbook", label="Scrapbook", action="scrapbook"),
                MasterMenuItem(id="secrets", label="Secrets Book", action="secrets"),
            ]
        ),
        
        # Other
        MasterMenuItem(
            id="other",
            label="Other",
            children=[
                MasterMenuItem(id="facts", label="Duck Fact", action="facts"),
                MasterMenuItem(id="settings", label="Settings", action="settings"),
                MasterMenuItem(id="sound", label="Toggle Sound", action="sound"),
                MasterMenuItem(id="music", label="Toggle Music", action="music"),
                # MasterMenuItem(id="save_slots", label="Save Slots", action="save_slots"),  # Hidden for now
                MasterMenuItem(id="help", label="Help", action="help"),
                MasterMenuItem(id="quit", label="Save & Quit", action="quit"),
            ]
        ),
    ]
