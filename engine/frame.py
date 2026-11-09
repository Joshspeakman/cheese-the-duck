"""Convert the content compositor's styled strings into explicit glyph runs.

Only color/style SGR is decoded. There is no cursor, terminal state, shell or
terminal emulation; each submission is an immutable complete frame.
"""
import re
from functools import lru_cache

SGR = re.compile(r'\x1b\[([0-9;]*)m|\x1b\([AB]')
PALETTE = ('#161b19', '#d77869', '#92b77b', '#dfbd75', '#7ca5b7', '#b79ac4', '#86c4bd', '#dfded0',
           '#737c73', '#ff9585', '#b7de95', '#ffe091', '#9acbe6', '#d5b4e3', '#a8eee1', '#fff5db')
FG, BG = '#e2dfca', '#101b19'

def color256(n):
    if n < 16:
        return PALETTE[n]
    if n < 232:
        n -= 16
        values = (0, 95, 135, 175, 215, 255)
        return '#%02x%02x%02x' % (values[n // 36], values[n // 6 % 6], values[n % 6])
    return '#%02x%02x%02x' % ((8 + (n - 232) * 10,) * 3)

@lru_cache(maxsize=4096)
def line_runs(line):
    fg, bg, flags = FG, BG, 0
    runs = []
    start = 0
    def add(s):
        if not s:
            return
        # Control bytes cannot become drawing commands. Keep all printable text verbatim.
        s = ''.join(c for c in s if c >= ' ' and c != '\x7f')
        if not s:
            return
        style = (fg, bg, flags)
        if runs and runs[-1][1:] == style:
            runs[-1] = (runs[-1][0] + s,) + style
        else:
            runs.append((s,) + style)
    for match in SGR.finditer(line):
        add(line[start:match.start()])
        start = match.end()
        if match.group(1) is None:
            continue
        codes = [int(n or '0') for n in match.group(1).split(';')]
        i = 0
        while i < len(codes):
            n = codes[i]
            if n == 0: fg, bg, flags = FG, BG, 0
            elif n == 1: flags |= 1
            elif n == 2: flags |= 2
            elif n == 7: flags |= 4
            elif n == 22: flags &= ~3
            elif n == 27: flags &= ~4
            elif n == 39: fg = FG
            elif n == 49: bg = BG
            elif 30 <= n <= 37: fg = PALETTE[n - 30]
            elif 90 <= n <= 97: fg = PALETTE[n - 90 + 8]
            elif 40 <= n <= 47: bg = PALETTE[n - 40]
            elif 100 <= n <= 107: bg = PALETTE[n - 100 + 8]
            elif n in (38, 48) and i + 2 < len(codes):
                color = None
                if codes[i + 1] == 5:
                    color = color256(max(0, min(255, codes[i + 2])))
                    i += 2
                elif codes[i + 1] == 2 and i + 4 < len(codes):
                    color = '#%02x%02x%02x' % tuple(max(0, min(255, c)) for c in codes[i + 2:i + 5])
                    i += 4
                if color:
                    if n == 38: fg = color
                    else: bg = color
            i += 1
    add(line[start:])
    return tuple(runs)
