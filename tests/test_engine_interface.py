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
