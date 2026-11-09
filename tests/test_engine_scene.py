from engine.scene import overlay_bounds


def test_overlay_covers_opaque_blank_interior_and_styled_borders():
    base = ['pond . . .', 'duck . . .', 'grass . . ']
    final = ['po+-----+.', 'du|     |.', 'gr+-----+ ']
    assert overlay_bounds(base, final) == {'x': 2, 'y': 0, 'w': 7, 'h': 3}
    assert overlay_bounds(base, base) is None
    assert overlay_bounds(['abc'], ['a\x1b[31mb\x1b[0mc']) == {'x': 1, 'y': 0, 'w': 1, 'h': 1}
