"""Read-only scene snapshots for Ultra. Classic composition is kept unchanged."""
from engine.frame import line_runs
from core.settings import get_settings
from ui.ascii_art import get_mini_duck
from ui.habitat_art import get_item_art, get_structure_art


def plain_cells(line):
    return [(char, fg, bg, flags) for text, fg, bg, flags in line_runs(line) for char in text]


def equipped_wearables(game):
    """Expose all saved wardrobe systems without equipping or granting anything.

    Shop selections come last so a newly equipped shop item wins a visual slot
    conflict with an older seasonal/outfit selection.
    """
    result = {}
    wardrobe = getattr(getattr(game, 'seasonal_clothing', None), 'wardrobe', None)
    for slot, item in getattr(wardrobe, 'equipped', {}).items():
        if item:
            result['seasonal:' + slot] = item
    outfit = getattr(getattr(game, 'outfits', None), 'current_outfit', None)
    for slot in ('hat', 'face', 'neck', 'body', 'wings', 'feet', 'held', 'special'):
        item = getattr(outfit, slot, None)
        if item:
            result['outfit:' + slot] = item
    result.update(game.habitat.equipped_cosmetics)
    return result


def overlay_bounds(base, final):
    """Bounds of a composed modal, including its blank interior and borders."""
    xs, ys = [], []
    for y, (before, after) in enumerate(zip(base, final)):
        if before == after:
            continue
        a, b = plain_cells(before), plain_cells(after)
        for x in range(max(len(a), len(b))):
            if (a[x] if x < len(a) else None) != (b[x] if x < len(b) else None):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return {'x': min(xs), 'y': min(ys), 'w': max(xs) - min(xs) + 1, 'h': max(ys) - min(ys) + 1}


def snapshot(game, renderer):
    area = game.exploration.current_area
    weather = game.atmosphere.current_weather
    duck = game.duck
    pos = renderer.duck_pos
    items, structures, visitor = [], [], None
    at_home = not area or area.name == 'Home Pond'
    if at_home:
        for item in game.habitat.get_visible_placed_items():
            x, y = item.get_display_position()
            items.append({'id': item.item_id, 'x': x * 132 / 20, 'y': y * 42 / 12,
                          'art': get_item_art(item.item_id)})
        for i, structure in enumerate(game.building.structures):
            if structure.status.value != 'complete':
                continue
            p = getattr(structure, 'position', None)
            structures.append({'id': structure.blueprint_id, 'x': p[0] * 132 / 10 if p else 8 + i * 12,
                               'y': p[1] * 42 / 8 if p else 32,
                               'art': get_structure_art(structure.blueprint_id)})
    if game.friends.current_visit:
        friend = game.friends.get_friend_by_id(game.friends.current_visit.friend_id)
        if friend:
            from world.friends import visitor_animator
            x, y = visitor_animator.get_position()
            visitor = {'name': friend.name, 'x': x + renderer._camera_x, 'y': y + renderer._camera_y,
                       'personality': friend.personality.value, 'art': visitor_animator.get_current_art()}
    interaction = renderer.interaction_animator.get_render_data()
    active = None
    if interaction:
        lines, position, visible, _ = interaction
        active = {'art': lines, 'x': position[0], 'y': position[1], 'showDuck': visible}
    return {
        'location': area.name if area else 'Home Pond', 'biome': area.biome.value if area else 'pond',
        'season': game.atmosphere.current_season.value,
        'hour': game.day_night.get_current_hour() + game.day_night.get_current_minute() / 60,
        'weather': weather.weather_type.value if weather else 'sunny',
        'intensity': weather.intensity if weather else 0,
        'motion': renderer._show_animations and not get_settings().accessibility.reduced_motion,
        'particles': renderer._show_particles if hasattr(renderer, '_show_particles') else True,
        'weatherEffects': renderer._show_weather_effects,
        'camera': {'x': renderer._camera_x, 'y': renderer._camera_y,
                   'w': renderer._viewport_width, 'h': renderer._viewport_height},
        'duck': {'x': pos.x, 'y': pos.y, 'facing': pos.facing_right, 'state': pos.get_state(),
                 'stage': duck.growth_stage, 'mood': duck.get_mood().state.value,
                 'name': duck.name, 'away': renderer._cheese_away,
                 'hidden': renderer.interaction_animator.should_hide_duck(),
                 'cosmetics': equipped_wearables(game),
                 'art': get_mini_duck(duck.growth_stage, pos.get_state(), pos.facing_right, pos.get_animation_frame())},
        'items': items, 'structures': structures, 'visitor': visitor, 'interaction': active,
    }
