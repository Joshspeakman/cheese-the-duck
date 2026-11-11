"""Read-only scene snapshots for Ultra. Classic composition is kept unchanged."""
from engine.frame import line_runs
from engine.placements import outdoor_decorations,habitat_placements,complete_structures
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
    from engine import headwear
    area = game.exploration.current_area
    weather = game.atmosphere.current_weather
    duck = game.duck
    pos = renderer.duck_pos
    items, structures, visitor = [], [], None
    at_home = not area or area.name == 'Home Pond'
    if at_home:
        for item in habitat_placements(game):
            items.append({'id': item.item_id, 'instance': item.instance, 'x': item.x, 'y': item.y,
                          'art': get_item_art(item.item_id)})
        for decoration in outdoor_decorations(game):
            items.append({'id':decoration.item_id,'instance':decoration.instance,'x':decoration.x,'y':decoration.y,'art':get_item_art(decoration.item_id)})
        for structure in complete_structures(game):
            structures.append({'id':structure.item_id,'instance':structure.instance,'x':structure.x,'y':structure.y,
                               'art':get_structure_art(structure.item_id)})
    if game.friends.current_visit:
        friend = game.friends.get_friend_by_id(game.friends.current_visit.friend_id)
        if friend:
            from world.friends import visitor_animator
            x, y = visitor_animator._position_x, visitor_animator._position_y
            visitor = {'id': friend.id, 'state': visitor_animator._current_state,
                       'facing': x < pos.x - renderer._camera_x if visitor_animator._current_state == 'signature' else getattr(visitor_animator, '_facing_right', True),
                       'activity': visitor_animator._current_state, 'name': friend.name, 'x': x + renderer._camera_x, 'y': y + renderer._camera_y,
                       'personality': friend.personality.value, 'art': visitor_animator.get_current_art()}
    rare = None
    if game.atmosphere.current_visitor:
        definition, _ = game.atmosphere.current_visitor
        species = {'friendly_goose':'goose','wise_owl':'owl','lost_duckling':'baby_duck',
                   'traveling_merchant':'baby_duck','celebrity_duck':'baby_duck',
                   'mysterious_crow':'crow','butterfly_fairy':'butterfly','grumpy_toad':'toad'}
        rare = {'personality': {'traveling_merchant':'adventurous','celebrity_duck':'generous'}.get(definition.id), 'id':definition.id,'name':definition.name,'asset':species.get(definition.id,'bird_flying'),
                'art':definition.ascii_art,'x':pos.x+17,'y':pos.y+2}
        motion = getattr(game, 'guest_motion', None)
        actor = motion.snapshot() if motion else None
        if actor and actor['id'] == definition.id:
            rare.update(actor)
    interaction = renderer.interaction_animator.get_render_data()
    active = None
    if interaction:
        lines, position, visible, _ = interaction
        active = {'art': lines, 'x': position[0], 'y': position[1], 'showDuck': visible}
    events = []
    for animator in getattr(game, '_event_animators', []):
        state = getattr(animator.state, 'value', str(animator.state))
        if state in ('waiting', 'finished'):
            continue
        x, y = animator.get_position()
        particles = animator.get_particles() if hasattr(animator, 'get_particles') else []
        events.append({'id': animator.event_id, 'family': type(animator).__name__,
                       'state': state, 'x': x + renderer._camera_x, 'y': y + renderer._camera_y,
                       'art': animator.get_sprite(),
                       'particles': [[px + renderer._camera_x, py + renderer._camera_y, c]
                                     for px, py, c in particles[:100]]})
    return {
        'events': events, 'rareVisitor':rare,
        'storyActor': game.story_motion.snapshot() if getattr(game, 'story_motion', None) else None,
        'living': game.living_pond.snapshot() if getattr(game, 'living_pond', None) else None,
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
                 'apparel': headwear.snapshot(getattr(game,'living_pond',None)),
                 'hatCare': headwear.care_snapshot(getattr(game,'living_pond',None)),
                 'motion': renderer._show_animations and not get_settings().accessibility.reduced_motion,
                 'art': get_mini_duck(duck.growth_stage, pos.get_state(), pos.facing_right, pos.get_animation_frame())},
        'items': items, 'structures': structures, 'visitor': visitor, 'interaction': active,
    }
