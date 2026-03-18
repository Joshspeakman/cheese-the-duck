"""
Render context data object.

Provides a pure-data snapshot of everything the renderer needs to draw a
single frame.  This replaces the pattern of passing the entire ``Game``
instance into the renderer, decoupling rendering from game logic.

Usage:
    ctx = build_render_context(game)
    renderer.render_frame_from_context(ctx)   # future migration target
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game


@dataclass
class RenderContext:
    """Immutable snapshot of all data the renderer needs for one frame.

    Every field is a plain Python type (no live game objects) so the renderer
    has zero back-references into game state.

    Attributes:
        duck_x: Duck x position in playfield coordinates.
        duck_y: Duck y position in playfield coordinates.
        duck_state: Current animation state name (e.g. ``"idle"``, ``"sleeping"``).
        duck_animation_frame: Current animation frame index.
        duck_facing_right: ``True`` if the duck faces right.
        duck_growth_stage: Growth stage string (``"egg"``, ``"duckling"``,
            ``"juvenile"``, ``"adult"``, ``"elder"``).
        duck_name: Display name of the duck.
        duck_mood: Current mood state string.
        duck_needs: Mapping of need names to their 0.0 -- 1.0 values.
        duck_trust: Trust level (0.0 -- 1.0).
        duck_cosmetics: List of equipped cosmetic item IDs.
        time_of_day: Current time period key (``"dawn"``, ``"morning"``, etc.).
        season: Current season string (``"spring"``, ``"summer"``, etc.).
        weather_type: Weather particle-type string or ``None``.
        weather_intensity: Weather intensity 0.0 -- 1.0.
        current_biome: Biome enum value string (``"pond"``, ``"forest"``, etc.).
        current_location: Location name string or ``None``.
        chat_messages: Recent chat log entries as ``(role, text)`` tuples.
        action_message: One-shot action message or ``None``.
        status_text: Status bar text string.
        level: Player/duck level.
        xp_progress: XP progress toward next level (0.0 -- 1.0).
        growth_progress: Growth progress toward next stage (0.0 -- 1.0).
        goals_completed: Number of completed goals.
        goals_total: Total number of goals.
        coins: Current coin balance.
        terminal_width: Terminal width in columns.
        terminal_height: Terminal height in rows.
        particles: Pre-computed particle positions from :class:`ParticleSystem`.
        visitors: Visitor info dicts for rendering.
        habitat_items: Placed habitat item dicts.
        active_overlay: Name of the currently active overlay (e.g.
            ``"help"``, ``"stats"``, ``"shop"``), or empty string.
        menu_items: Current menu item labels or ``None`` if no menu.
        menu_selected: Currently highlighted menu index.
    """

    # Duck state
    duck_x: int = 0
    duck_y: int = 0
    duck_state: str = "idle"
    duck_animation_frame: int = 0
    duck_facing_right: bool = True
    duck_growth_stage: str = "duckling"
    duck_name: str = "Cheese"
    duck_mood: str = "content"
    duck_needs: Dict[str, float] = field(default_factory=lambda: {
        "hunger": 1.0, "energy": 1.0, "fun": 1.0,
        "cleanliness": 1.0, "social": 1.0,
    })
    duck_trust: float = 0.5
    duck_cosmetics: List[str] = field(default_factory=list)

    # World state
    time_of_day: str = "midday"
    season: str = "spring"
    weather_type: Optional[str] = None
    weather_intensity: float = 0.0
    current_biome: str = "pond"
    current_location: Optional[str] = None

    # Chat / messages
    chat_messages: List[Tuple[str, str]] = field(default_factory=list)
    action_message: Optional[str] = None
    status_text: str = ""

    # Progression
    level: int = 1
    xp_progress: float = 0.0
    growth_progress: float = 0.0
    goals_completed: int = 0
    goals_total: int = 0
    coins: int = 0

    # Terminal
    terminal_width: int = 80
    terminal_height: int = 24

    # Particles (pre-computed by ParticleSystem)
    particles: List[Tuple[int, int, str, Tuple[int, int, int]]] = field(default_factory=list)

    # World objects
    visitors: List[Dict[str, Any]] = field(default_factory=list)
    habitat_items: List[Dict[str, Any]] = field(default_factory=list)

    # UI overlay state
    active_overlay: str = ""
    menu_items: Optional[List[str]] = None
    menu_selected: int = 0


def build_render_context(game: "Game") -> RenderContext:
    """Extract all rendering data from a live Game instance.

    This function is the single point of coupling between the game logic and
    the rendering layer.  It reads attributes from the Game, Duck, Atmosphere,
    Exploration, Habitat, and Friends subsystems and packs them into a plain
    :class:`RenderContext` dataclass.

    Args:
        game: The running ``Game`` instance.

    Returns:
        A fully populated ``RenderContext`` snapshot.
    """
    ctx = RenderContext()

    duck = game.duck
    if duck is None:
        return ctx

    # ── Duck state ───────────────────────────────────────────────────────
    renderer = game.renderer
    duck_pos = renderer.duck_pos
    ctx.duck_x = duck_pos.x
    ctx.duck_y = duck_pos.y
    ctx.duck_state = duck_pos.get_state() if hasattr(duck_pos, "get_state") else "idle"
    ctx.duck_animation_frame = duck_pos.get_animation_frame() if hasattr(duck_pos, "get_animation_frame") else 0
    ctx.duck_facing_right = duck_pos.facing_right
    ctx.duck_growth_stage = duck.growth_stage.value if hasattr(duck.growth_stage, "value") else str(duck.growth_stage)
    ctx.duck_name = duck.name
    ctx.duck_mood = duck.get_mood().state.value if hasattr(duck.get_mood().state, "value") else str(duck.get_mood().state)
    ctx.duck_trust = getattr(duck, "trust", 0.5)

    # Needs
    needs = {}
    if hasattr(duck, "needs"):
        for need_name in ("hunger", "energy", "fun", "cleanliness", "social"):
            val = getattr(duck.needs, need_name, None)
            if val is not None:
                needs[need_name] = float(val) if not callable(val) else float(val())
            else:
                needs[need_name] = 1.0
    ctx.duck_needs = needs

    # Cosmetics
    if hasattr(game, "habitat") and game.habitat:
        equipped = game.habitat.equipped_cosmetics
        ctx.duck_cosmetics = list(equipped.keys()) if isinstance(equipped, dict) else list(equipped)

    # ── World / Atmosphere ───────────────────────────────────────────────
    if hasattr(game, "atmosphere") and game.atmosphere:
        atmo = game.atmosphere
        if atmo.current_season:
            ctx.season = atmo.current_season.value
        if atmo.current_weather:
            ctx.weather_type = atmo.current_weather.weather_type.value
            ctx.weather_intensity = atmo.current_weather.intensity

    # Time of day — use centralised TimeManager
    try:
        from core.time_system import get_current_time_of_day
        ctx.time_of_day = get_current_time_of_day().value
    except Exception:
        ctx.time_of_day = "midday"

    # Exploration
    if hasattr(game, "exploration") and game.exploration and game.exploration.current_area:
        ctx.current_location = game.exploration.current_area.name
        ctx.current_biome = game.exploration.current_area.biome.value

    # ── Progression ──────────────────────────────────────────────────────
    if hasattr(game, "progression") and game.progression:
        ctx.level = getattr(game.progression, "level", 1)
        xp = getattr(game.progression, "xp", 0)
        xp_needed = getattr(game.progression, "xp_for_next_level", 100)
        ctx.xp_progress = min(1.0, xp / max(1, xp_needed)) if xp_needed else 0.0

    if hasattr(duck, "growth_progress"):
        ctx.growth_progress = float(duck.growth_progress)

    if hasattr(game, "goals") and game.goals:
        active = getattr(game.goals, "active_goals", [])
        completed = sum(1 for g in active if getattr(g, "completed", False))
        ctx.goals_completed = completed
        ctx.goals_total = len(active)

    if hasattr(game, "habitat") and game.habitat:
        ctx.coins = getattr(game.habitat, "currency", 0)

    # ── Terminal ─────────────────────────────────────────────────────────
    if hasattr(game, "terminal") and game.terminal:
        ctx.terminal_width = max(game.terminal.width, 60)
        ctx.terminal_height = max(game.terminal.height, 20)

    # ── Visitors ─────────────────────────────────────────────────────────
    if hasattr(game, "friends") and game.friends and game.friends.current_visit:
        visit = game.friends.current_visit
        friend = game.friends.get_friend_by_id(visit.friend_id)
        if friend:
            ctx.visitors = [{
                "id": friend.id,
                "name": friend.name,
                "species": getattr(friend, "species", "duck"),
                "x": getattr(visit, "x", 0),
                "y": getattr(visit, "y", 0),
            }]

    # ── Habitat items ────────────────────────────────────────────────────
    if hasattr(game, "habitat") and game.habitat:
        is_home = (ctx.current_location == "Home Pond" or ctx.current_location is None)
        if is_home:
            placed = game.habitat.get_visible_placed_items() if hasattr(game.habitat, "get_visible_placed_items") else []
            ctx.habitat_items = [
                {"id": getattr(item, "id", ""), "name": getattr(item, "name", ""),
                 "x": getattr(item, "x", 0), "y": getattr(item, "y", 0)}
                for item in placed
            ]

    # ── Chat messages ────────────────────────────────────────────────────
    if hasattr(renderer, "_chat_log"):
        recent = renderer._chat_log[-10:]  # Last 10 entries
        ctx.chat_messages = [(entry[2] if len(entry) > 2 else "system", entry[1]) for entry in recent]

    # ── Active overlay ───────────────────────────────────────────────────
    if renderer._show_help:
        ctx.active_overlay = "help"
    elif renderer._show_stats:
        ctx.active_overlay = "stats"
    elif renderer._show_talk:
        ctx.active_overlay = "talk"
    elif renderer._show_inventory:
        ctx.active_overlay = "inventory"
    elif renderer._show_shop:
        ctx.active_overlay = "shop"
    elif renderer._show_celebration:
        ctx.active_overlay = "celebration"
    elif renderer._menu_overlay_active:
        ctx.active_overlay = "menu"
    else:
        ctx.active_overlay = ""

    # ── Action message ───────────────────────────────────────────────────
    if renderer._message_queue:
        ctx.action_message = renderer._message_queue[-1]

    return ctx
