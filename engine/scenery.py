"""Additional world-space ASCII detail beneath the original actors and scenery.

Deterministic coordinates keep the landscape stable when the camera moves.
Animations use elapsed time; no calls to gameplay's random generator.
"""
import math

PALETTES = {
    'pond': ('#526d55', '#426c70', '#8b9c67'),
    'forest': ('#526a42', '#395642', '#a4a574'),
    'meadow': ('#68814f', '#56714a', '#d9b789'),
    'riverside': ('#647e68', '#426e80', '#a7a18b'),
    'garden': ('#72834f', '#514e37', '#cc9c7b'),
    'mountains': ('#7a8385', '#535e68', '#bdd0c5'),
    'beach': ('#a69b71', '#447e86', '#d6c19a'),
    'swamp': ('#6c7850', '#3c6156', '#a4b382'),
    'urban': ('#7d8978', '#586961', '#c4b38e'),
}
TREE = r"""        .-~~~-.
    .-~( . . . )~-.
   ( . / . . / . .)
    (_ . . | . . _)
      ~--. | .--~
         |:|
        /|:|/
   ..__/__|__/__..""".splitlines()
PINE = r"""       /A
      /..A
     /:..:A
    /__..__A
     /....A
    /:....:A
   /___||___A
       ||""".replace('A', chr(92)).splitlines()
ROCK = r"""        ___
    _.-/ : A__
  _/.:/  .  : A_
 /___/___:_____A""".replace('A', chr(92)).splitlines()
REEDS = r"""   |  !   |
 ! |  | ! |
 |/| /| |/|
~|~|~~|~|~|~""".splitlines()
FENCE = r""" |     |     |     |
=|=====|=====|=====|=
 | . : | . : | . : |""".splitlines()
RUIN = r"""       __..__
   ___/::  ::A___
  |::  .--.   . :|
  | . /    A :  :|
  |::|      | . :|
 _|__|______|____|_""".replace('A', chr(92)).splitlines()

WILLOW = r"""           .-~~~~--._
       _.-~ , . , .  ~-._
     .' , . / , . , A .  '.
    ( . , / . , | . , A . .)
     )| / , . / | A . , A|(
     ||/ . , /  |  A . ,A||
     |/ | , /  /|A  A , |A|
     || | /   |:|:|  A| | |
      | |     |:|:|   | |
        |     |:|:|   |
           __/ | | A__
       _.-~__ /| |A __~-._
     .:______/ | | A______:.
         ,  .  , .  , .""".replace('A', chr(92)).splitlines()
DOCK = r"""      |               |
     _|_______________|_
    /_|___|___|___|___|_/|
   /__|___|___|___|___|/ |
      |  :   |   :    | ~
   ~~~|~~~~~~|~~~~~~~~|~~~""".splitlines()
FLOWERS = r"""  _     _       _     _
 (_@)  (@_)   (_@)  (@_)
  /|    |A     /|    |A
 v | v  | v  v  | v  | v
 ..|....|.......|....|..""".replace('A', chr(92)).splitlines()
BOAT = r"""         /|
        / |
       /__|
    ___|_____....__
    A____________/
  ~~~--~~~~~--~~~~~""".replace('A', chr(92)).splitlines()
CLOUD = ["     .--.      ", "  .-(    ).    ", " (___.__)__)   "]
LAYOUTS = {
    'pond': [(2,5,WILLOW), (96,6,WILLOW), (80,26,DOCK), (8,27,REEDS), (45,34,REEDS)],
    'forest': [(0,4,WILLOW), (25,6,TREE), (75,5,WILLOW), (110,8,TREE), (50,31,ROCK)],
    'meadow': [(0,5,TREE), (96,5,WILLOW), (20,28,FLOWERS), (73,31,FLOWERS)],
    'garden': [(2,7,FENCE), (32,7,FENCE), (90,7,FENCE), (10,24,FLOWERS), (67,28,FLOWERS)],
    'riverside': [(2,6,WILLOW), (95,7,TREE), (80,25,BOAT), (30,33,ROCK)],
    'mountains': [(2,8,PINE), (20,4,PINE), (100,7,PINE), (78,30,ROCK), (12,31,ROCK)],
    'beach': [(4,7,ROCK), (98,9,ROCK), (72,26,BOAT), (18,33,REEDS)],
    'swamp': [(0,5,WILLOW), (91,7,RUIN), (15,26,REEDS), (90,30,REEDS)],
    'urban': [(5,6,TREE), (100,7,TREE), (26,9,FENCE), (90,30,FLOWERS)],
}

def hash2(x, y):
    return ((x * 73856093) ^ (y * 19349663)) & 0xffff

class Landscape:
    def __init__(self, term):
        self.term = term
        self.styles = {key: [term.color_rgb(*bytes.fromhex(c[1:])) for c in colors] for key, colors in PALETTES.items()}

    def row(self, row, camera_x, world_y, biome, season, seconds):
        biome = biome or 'pond'
        styles = self.styles.get(biome, self.styles['pond'])
        water = biome in ('pond', 'beach', 'riverside', 'swamp')
        for x in range(len(row)):
            wx = camera_x + x
            h = hash2(wx, world_y)
            if row[x][0] not in (' ', '.', ',', '`', "'"):
                continue
            char, style = None, styles[0]
            # Irregular banks, ripples and light reflected in water, entirely glyphs.
            bank = 23 + int(3 * math.sin(wx * .055))
            if water and bank < world_y < bank + 11:
                wave = int(wx + world_y * 3 + seconds * 4) % 17
                char = '~' if wave < 4 else ('-' if wave == 6 else '.')
                style = styles[1]
            elif h % 23 == 0:
                char = ',' if int(seconds * 2 + wx / 9) % 3 else "'"
            elif h % 89 == 0:
                char, style = ('*' if season != 'winter' else '+'), styles[2]
            elif h % 11 == 0:
                char = '.'
            if biome == 'mountains' and h % 17 == 0:
                char, style = ':', styles[2]
            if char:
                row[x] = (char, style)
        # Distant banks / ridges and drifting ASCII cloud layers.
        if world_y < 6:
            for x in range(len(row)):
                wx = camera_x + x
                ridge = 3 + int(1.5 * math.sin(wx * .13))
                if world_y == ridge:
                    row[x] = ('_' if wx % 3 else '.', styles[1])
            cloud_x = int(seconds * .7) % 170 - 20
            iy = world_y - 1
            if 0 <= iy < len(CLOUD):
                for dx, char in enumerate(CLOUD[iy]):
                    sx = cloud_x + dx - camera_x
                    if char != ' ' and 0 <= sx < len(row):
                        row[sx] = (char, styles[2])
        for px, py, prop in LAYOUTS.get(biome, LAYOUTS['pond']):
            iy = world_y - py
            if 0 <= iy < len(prop):
                for dx, char in enumerate(prop[iy]):
                    sx = px + dx - camera_x
                    if char != ' ' and 0 <= sx < len(row):
                        if prop in (TREE, WILLOW) and char == ',' and int(seconds * 2 + dx / 3) % 3 == 0:
                            char = "'"
                        row[sx] = (char, styles[0 if iy < len(prop) - 2 else 2])
