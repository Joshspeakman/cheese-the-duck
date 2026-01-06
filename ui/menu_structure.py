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
                MenuItem("save_slots", "Save Slots", "Manage save files"),
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
