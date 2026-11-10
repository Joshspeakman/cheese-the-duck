"""Desktop clicks must use the current game's menu and confirmation rules."""
from types import SimpleNamespace as NS
from engine.host import DesktopInput
from engine.interface import composed_modal


def terminal():
    term = DesktopInput()
    items = [NS(id='care', enabled=True), NS(id='locked', enabled=False)]
    menu = NS(_get_current_items=lambda: items, _selected_index=0)
    term.game = NS(_state='playing', master_menu=menu, _active_minigame=None,
                   _confirmation_dialog=None, renderer=NS(interface_modal=None))
    return term


def test_click_returns_enter_for_the_original_menu_handler():
    term = terminal()
    key = term.choose({'target': 'menu', 'id': 'care', 'context': 'care|locked'})
    assert key.name == 'KEY_ENTER'
    assert term.game.master_menu._selected_index == 0


def test_stale_or_locked_click_cannot_execute():
    term = terminal()
    assert not term.choose({'target': 'menu', 'id': 'care', 'context': 'old-menu'})
    assert not term.choose({'target': 'menu', 'id': 'locked', 'context': 'care|locked'})
    term.game.renderer.interface_modal = {'title': 'Inventory'}
    assert not term.choose({'target': 'menu', 'id': 'care', 'context': 'care|locked'})
    term.game.renderer.interface_modal = None
    term.game._confirmation_dialog = NS(is_open=True)
    assert not term.choose({'target': 'menu', 'id': 'care', 'context': 'care|locked'})


def test_title_click_cannot_bypass_save_erasure_confirmation():
    term = terminal()
    term.game._state = 'title'
    term.game.renderer.interface_title = {'options': ['Continue', 'New Game', 'Quit']}
    command = {'target': 'title', 'index': 1, 'context': 'Continue|New Game|Quit'}
    assert term.choose(command).name == 'KEY_ENTER'
    assert term.game._title_menu_index == 1
    term.game._title_confirm_new_game = True
    assert not term.choose(command)
    term.game._title_confirm_new_game = False
    assert not term.choose(dict(command, index=10))
    assert not term.choose(dict(command, context='New Game|Quit'))


def test_custom_overlay_keeps_its_literal_content_and_colors():
    lines = ['..╔═ INTERACTING ═╗..', '..║\x1b[33mWhat the fuck! \x1b[0m║..', '..╚═══════════════╝..']
    result = composed_modal(lines, {'x': 2, 'y': 0, 'w': 17, 'h': 3})
    assert result['title'] == 'INTERACTING'
    assert ''.join(run[0] for run in result['lines'][0]).startswith('What the fuck!')
    assert result['lines'][0][0][1] != '#e2dfca'


def test_item_preview_uses_the_original_selection_without_executing_it():
    from engine.interface import selected_item_id
    renderer = NS(get_selected_shop_item=lambda: NS(id='hat_blue'),
                  _inventory_items=['bread', 'medicine'], _inventory_selected=1)
    selector = NS(get_selected_item=lambda: NS(data=NS(id='stone_hammer')))
    game = NS(_crafting_menu=selector, _building_menu=selector)
    assert selected_item_id(game, renderer, 'SHOP') == 'hat_blue'
    assert selected_item_id(game, renderer, 'INVENTORY') == 'medicine'
    assert selected_item_id(game, renderer, 'CRAFTING') == 'stone_hammer'
    renderer._inventory_selected = 2
    assert selected_item_id(game, renderer, 'INVENTORY') is None
    assert selected_item_id(game, renderer, 'NONE') is None


def test_all_live_shop_categories_are_reachable_in_desktop_renderer():
    from engine.host import CanvasRenderer
    from world.shop import ItemCategory, SHOP_ITEMS, get_items_by_category
    renderer = CanvasRenderer(DesktopInput())
    assert renderer._shop_categories == [category.name for category in ItemCategory]
    reached = set()
    for index, category in enumerate(ItemCategory):
        renderer._shop_category_index = index
        for item_index, item in enumerate(get_items_by_category(category)):
            renderer._shop_item_index = item_index
            assert renderer.get_selected_shop_item().id == item.id
            reached.add(item.id)
    assert reached == set(SHOP_ITEMS)


def test_ultra_item_catalog_tracks_all_live_registries():
    import json
    from pathlib import Path
    from engine.export_items import catalog
    text = (Path(__file__).resolve().parents[1] / 'engine/client/item-catalog.mjs').read_text()
    exported = json.loads(text.split('export const ITEM_CATALOG = ', 1)[1].rstrip(';\n'))
    assert exported == json.loads(json.dumps(catalog()))


def test_wearable_catalog_tracks_shop_outfits_and_seasonal_clothes():
    import json
    from pathlib import Path
    from engine.export_wearables import catalog
    text = (Path(__file__).resolve().parents[1] / 'engine/client/wearable-catalog.mjs').read_text()
    exported = json.loads(text.split('export const WEARABLE_CATALOG = ', 1)[1].rstrip(';\n'))
    assert exported == catalog()


def test_scene_exposes_all_equipped_wardrobes_without_changing_them():
    from engine.scene import equipped_wearables
    shop = {'head': 'hat_blue', 'neck': 'scarf_red'}
    seasonal = {'head': 'winter_santa_hat', 'feet': 'winter_snow_boots'}
    outfit = NS(hat='hat_red', body='sweater_cozy')
    game = NS(habitat=NS(equipped_cosmetics=shop), outfits=NS(current_outfit=outfit),
              seasonal_clothing=NS(wardrobe=NS(equipped=seasonal)))
    result = equipped_wearables(game)
    assert list(result.values()) == ['winter_santa_hat', 'winter_snow_boots', 'hat_red', 'sweater_cozy', 'hat_blue', 'scarf_red']
    result['head'] = 'hat_chef'
    assert shop == {'head': 'hat_blue', 'neck': 'scarf_red'}
    assert seasonal == {'head': 'winter_santa_hat', 'feet': 'winter_snow_boots'}
    assert outfit.hat == 'hat_red'
