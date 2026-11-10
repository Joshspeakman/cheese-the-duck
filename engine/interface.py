"""Read-only desktop UI data. Actions and dialogue remain owned by the game."""
from engine.frame import line_runs
from core.settings import get_settings
import time
import re


def selected_item_id(game, renderer, overlay):
    """Read the original selection; previewing never buys, uses or grants items."""
    overlay = overlay.lower()
    if overlay == 'shop':
        item = renderer.get_selected_shop_item()
        return item.id if item else None
    if overlay == 'inventory':
        items = getattr(renderer, '_inventory_items', [])
        index = getattr(renderer, '_inventory_selected', 0)
        return items[index] if 0 <= index < len(items) else None
    selector = {'crafting': '_crafting_menu', 'building': '_building_menu',
                'use_item': '_use_menu'}.get(overlay)
    if selector:
        selected = getattr(game, selector).get_selected_item()
        data = selected.data if selected else None
        return data if isinstance(data, str) else getattr(data, 'id', None)
    return None


def composed_modal(lines, rect):
    """Preserve custom celebration/interaction compositors as upgraded panels too."""
    def crop(line, start, count):
        result = []
        end = start + count
        offset = 0
        for text, fg, bg, flags in line_runs(line):
            a, b = max(0, start - offset), min(len(text), end - offset)
            if b > a: result.append((text[a:b], fg, bg, flags))
            offset += len(text)
        return result
    x, y, w, h = (rect[key] for key in ('x', 'y', 'w', 'h'))
    title = ''.join(run[0] for run in crop(lines[y], x, w))
    title = re.sub(r'^[\s╔╗╚╝═─+|*★]+|[\s╔╗╚╝═─+|*★]+$', '', title) or 'Event'
    return {'title': title, 'preserveArt': True,
            'lines': [crop(line, x + 1, max(0, w - 2)) for line in lines[y + 1:y + h - 1]]}


def snapshot(game, renderer):
    settings = get_settings()
    result = {
        'state': game._state,
        'hour': game.day_night.get_current_hour() + game.day_night.get_current_minute() / 60,
        'motion': renderer._show_animations and not settings.accessibility.reduced_motion,
        'highContrast': settings.accessibility.high_contrast,
        'modal': renderer.interface_modal,
        'title': renderer.interface_title,
        'fact': renderer._title_fact,
    }
    if game._state != 'playing' or not game.duck:
        return result
    duck = game.duck
    menu = game.master_menu
    items = menu._get_current_items()
    xp, needed, percent = game.progression.get_xp_progress()
    active = game.ui_state.get_active()
    dialog = game._confirmation_dialog
    result.update(
        overlay=active.value,
        itemPreview=selected_item_id(game, renderer, active.name),
        dangerous=bool(dialog and dialog.is_open and dialog.dangerous),
        minigame=bool(game._active_minigame),
        name=duck.name, stage=duck.get_growth_stage_display(), age=duck.get_age_days(),
        mood=duck.get_mood().description,
        emotion={'mood': duck.get_mood().state.value,
                 'action': renderer._closeup_action if renderer._show_closeup and renderer._closeup_action else duck.current_action},
        activity=renderer._get_activity_text(duck),
        action=duck.get_action_message() or ('Waiting to hatch...' if duck.growth_stage == 'egg' else 'Just vibing...'),
        needs={name: getattr(duck.needs, name) for name in ('hunger', 'energy', 'fun', 'cleanliness', 'social')},
        trust=duck.trust,
        cold=bool(duck.cooldown_until and time.time() < duck.cooldown_until),
        attention=getattr(renderer, '_last_consequence_stage', 0),
        currency=game.habitat.currency,
        level=game.progression.level, xp=xp, xpNeeded=needed, xpPercent=percent,
        growth=duck.growth_progress * 100,
        goals=[game.goals.get_completed_count(), game.goals.get_total_count()],
        menu={'title': menu._parent_label or 'Pond menu', 'selected': menu._selected_index,
              'depth': menu.get_depth(), 'items': [
                  {'id': item.id, 'label': item.label, 'children': bool(item.children),
                   'enabled': bool(item.enabled),
                   'completed': bool(item.completed(game) if callable(item.completed) else item.completed)}
                  for item in items]},
        chat=[line_runs(line) for line in renderer.interface_chat],
    )
    return result
