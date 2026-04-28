"""Tests for event animation sprite data."""

from ui import sprite_library as sprites


def _categories():
    return (
        sprites.CREATURES,
        sprites.FOOD,
        sprites.OBJECTS,
        sprites.HUMANS,
        sprites.CELESTIAL,
        sprites.PROPS,
        sprites.VEHICLES,
    )


def test_sprite_frames_are_rectangular():
    for category in _categories():
        for sprite_name, frames in category.items():
            heights = {len(lines) for lines in frames.values()}
            assert len(heights) == 1, sprite_name

            widths = {
                len(line)
                for lines in frames.values()
                for line in lines
            }
            assert len(widths) == 1, sprite_name


def test_sprite_frames_are_ascii():
    for category in _categories():
        for sprite_name, frames in category.items():
            for frame_name, lines in frames.items():
                for line in lines:
                    assert line.isascii(), f"{sprite_name}/{frame_name}"
