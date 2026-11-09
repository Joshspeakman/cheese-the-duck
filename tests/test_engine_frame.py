from engine.frame import line_runs, FG, BG
from engine.scenery import Landscape
from blessed import Terminal

def test_color_runs_and_reset_do_not_bleed():
    assert line_runs('\x1b[38;2;255;123;0mA\x1b[0mB') == (('A', '#ff7b00', BG, 0), ('B', FG, BG, 0))

def test_uncensored_content_is_literal():
    text = 'What the fuck? <script> & bread'
    assert ''.join(run[0] for run in line_runs(text)) == text

def test_styles_and_256_palette():
    runs = line_runs('\x1b[1;7;38;5;196mX\x1b[22;27mY')
    assert runs[0][1:] == ('#ff0000', BG, 5)
    assert runs[1][3] == 0

def test_landscape_world_coordinates_stay_stable_when_camera_moves():
    landscape = Landscape(Terminal(force_styling=True))
    a, b = [(' ', None)] * 70, [(' ', None)] * 50
    landscape.row(a, 0, 20, 'pond', 'summer', 5)
    landscape.row(b, 20, 20, 'pond', 'summer', 5)
    assert a[20:] == b

def test_all_biomes_draw_ascii_without_touching_random_state():
    import random
    from engine.scenery import PALETTES
    state = random.getstate()
    landscape = Landscape(Terminal(force_styling=True))
    for biome in PALETTES:
        for y in range(42):
            row = [(' ', None)] * 132
            landscape.row(row, 0, y, biome, 'winter', 7)
            assert all(len(c) == 1 and 32 <= ord(c) <= 126 for c, _ in row)
    assert random.getstate() == state
