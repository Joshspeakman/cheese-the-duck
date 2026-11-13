"""Shared helper for repertoire generators. Workers import it and never edit it. It is stricter than
check_repertoire.py on purpose: it refuses relabels, undrawn keys, contacts on empty air and gates nothing can reach."""
import json, os, re, subprocess
from pathlib import Path
ENG = Path(os.environ.get('REP_ENGINE') or Path(__file__).resolve().parent.parent)
OUT = Path(os.environ.get('REP_OUT') or ENG / 'client/animation/repertoire')
AGES = ['hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary']
YOUNG, GROWN = AGES[:2], AGES[2:]
BODY = dict(zip(AGES, (60.4, 78.7, 96.6, 110.2, 117.7, 123.5, 116., 123.5)))  # px, repertoire-reach.json bodyHeight rounded down
TOOLS = dict(none=1.05, wing=1.1, twig=1.6, reed=1.6)  # reach = body height x factor (export-repertoire-reach.mjs)
GROUPS = ('care', 'use', 'play', 'test', 'rest', 'weather', 'show', 'mishap')
POSE = {'x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor'}
TAGS = set('''always wet dry snow storm windy calm warm cold sun night day dawn dusk night_late dawn_or_day clear rainbow_sky growing spring summer fall winter
 tired lonely sad !wet !snow !storm !windy !cold !night !night_late !dawn !dusk !summer !fall !winter !rainbow_sky !tired !lonely !sad'''.split())
MOODS = {'young', 'grown', 'elder', 'happy', 'grumpy', 'curious'}  # prefer only: the harness cannot stage them
REAL = dict(subject=('hunger', 'mood', 'health', 'trust', 'growth'), keeping=('clarity', 'algae', 'leaves', 'ice', 'oxygen', 'plants', 'flakes', 'bell'), need=('fun', 'social', 'energy', 'cleanliness'))
CMP = re.compile(r'^!?([a-z_]+)(<=|>=|<|>)(-?[0-9.]+)$')
JS = ("import {itemSprite as s,itemWorldScale as w} from './client/ultra-items.mjs';const i=process.argv[1],m=s(i,0,{state:{keeping:{setup:true,fish:[]}}});"
      "console.log(JSON.stringify({w:m.width,art:m.art.map(String),row:7.5*w(i)*(m.detailScale||1)*1.5,ground:m.anchors?.entry?.y??m.art.length-1,named:Object.keys(m.anchors||{})}))")


def sprite(item):
    return json.loads(subprocess.run(['node', '--input-type=module', '-e', JS, item], cwd=ENG, capture_output=True, text=True, check=True).stdout)


def k(t, at=None, **pose):
    """Keyframe at fraction t. `at` = the anchor being touched (sets contact=1). Only name an anchor on a keyframe that touches it."""
    return [t, dict(pose, anchor=at, contact=pose.get('contact', 1)) if at else pose]


class Obj:
    def __init__(self, oid, host, fields, effects, anchors, physics=(), triggers=(), on=None, liftable=False):
        """anchors = {name: (x, y)} fractions of the host sprite; on = that sprite for keeping/display (koi_pond, infinity_pool, trophy_case)."""
        self.d = d = dict(object=oid, host=host, fields={f: list(v) for f, v in fields.items()}, physics=[list(p) for p in physics],
                          triggers=[[w, [list(r) for r in rows]] for w, rows in triggers], effects={n: [list(r) for r in rows] for n, rows in effects.items()},
                          anchors={n: dict(x=x, y=y) for n, (x, y) in anchors.items()}, lines={}, routines={})
        self.liftable, self.sigs, self.group, self.reach, self.far, self.h = liftable, {}, {}, {}, 0, dict.fromkeys(anchors, 0)
        self.spot = {n: (round(x * 8), round(y * 8)) for n, (x, y) in anchors.items()}  # where a touch is, on a coarse grid (about 15 px once measured)
        assert host in ('placed', 'portable', 'keeping', 'display', 'wearable') and (on is None) == (host not in ('keeping', 'display')), oid + ': host/on'
        assert all(re.fullmatch('[a-z_]+', f) and not f.startswith(('pond_', 'fish_')) and f != 'history' for f in fields), oid + ': field names are [a-z_]+'
        for n, rows in d['effects'].items():
            for t, op, v in rows:
                a, _, b = t.partition('.')
                ok = t in fields or (b in REAL.get(a, ()) and (a != 'need' or (op == 'add' and abs(v) <= 3)) and (a == 'need' or host == 'keeping'))
                assert ok and op in ('set', 'add', 'mul', 'max', 'min', 'wrap'), f'{oid}: effect {n} row {t} {op} would do nothing, or is not allowed'
        if host != 'wearable':  # worn things play on Cheese's own body: nothing to measure
            sp = sprite(on or oid)
            rows = len(sp['art']) - 1
            for n, (x, y) in anchors.items():
                cx, cy = round(x * (sp['w'] - 1)), round(y * rows)
                assert n not in sp['named'] and n not in ('contact', 'entry'), f'{oid}: anchor name {n} is taken by the drawing {sp["named"]}'
                assert any(sp['art'][r][max(0, cx - 4):cx + 5].strip() for r in range(max(0, cy - 1), min(rows, cy + 1) + 1)), f'{oid}: anchor {n} is on empty air'
                self.h[n], self.spot[n] = (sp['ground'] - y * rows) * sp['row'], (round(cx * sp['row'] / 22.5), round(cy * sp['row'] / 15))
                assert self.h[n] >= 0, f'{oid}: anchor {n} is below the ground line'

    def moves(self, f, rising):
        rows = [r[1:] for rws in [*self.d['effects'].values(), *[t[1] for t in self.d['triggers']]] for r in rws if r[0] == f]
        phys = [(op, v) for pf, op, v, _ in self.d['physics'] if pf == f]
        if rising:
            return any(op in ('set', 'max', 'wrap') or (op == 'add' and v > 0) for op, v in rows) or any(op != 'rate' or v > 0 for op, v in phys)
        return any(op in ('set', 'min', 'wrap', 'mul') or (op == 'add' and v < 0) for op, v in rows) or any(op != 'rate' or v < 0 for op, v in phys)

    def token(self, key, tok, gate):
        m = CMP.match(tok)
        if not m:
            assert tok in TAGS or (not gate and tok.lstrip('!') in MOODS), f'{key}: `{tok}` is not a tag the harness can stage in {"when" if gate else "prefer"}'
        elif m.group(1).startswith(('pond_', 'fish_')):
            assert self.d['host'] == 'keeping', key + ': fish_/pond_ fields need a keeping host'
        else:
            (default, lo, hi), v, rising = self.d['fields'][m.group(1)], float(m.group(3)), (m.group(2) in ('>', '>=')) != tok.startswith('!')
            holds, inside = (default > v, v < hi) if rising else (default < v, v > lo)
            assert inside and (holds or self.moves(m.group(1), rising)), f'{key}: `{tok}` can never come true: nothing moves {m.group(1)} that far'

    def r(self, slug, label, dur, tool, track, ev=(), *, g, when=(), prefer=(), ages=None, say=None, obj=(), pick=None, far=False):
        d, key, tr = self.d, self.d['object'] + '_' + slug, [[0, {}], *track, [1, {}]]
        when = sorted(when, key=lambda t: (not t.startswith('!'), t == 'storm'))  # the harness stages tokens in order: negations first, storm last
        assert key not in d['routines'] and tool in TOOLS and g in GROUPS and 10 <= dur <= 60 and len(track) >= 3, key + ': id, tool, group, duration or too few keyframes'
        assert [t for t, _ in tr] == sorted({t for t, _ in tr}) and all(set(q) <= POSE for _, q in tr), key + ': track order, or a key the renderer does not draw'
        [self.token(key, tok, True) for tok in when], [self.token(key, tok, False) for tok in prefer]
        assert 'storm' not in when or (tool == 'none' and 'wet' in when and dur >= 30), key + ': a storm routine is a long tool-free shelter that also lists `wet`'
        for t, name in ev:
            touching = any(abs(qt - t) < .011 and q.get('contact', 0) >= .5 and q.get('anchor') for qt, q in tr)
            assert name in d['effects'] and .1 <= t <= .9 and (touching or far), f'{key}: event {name} at {t} has no touching keyframe'
        self.far += bool(far)
        held, last = [], None
        for _, q in tr:
            last = q.get('anchor') or last
            held.append(last)
        assert all(a in d['anchors'] for a in held if a), key + ': undeclared anchor'
        high = max([self.h[a] for i in range(len(tr) - 1) if max(tr[i][1].get('contact', 0), tr[i + 1][1].get('contact', 0)) > .05 for a in held[i:i + 2] if a] or [0])
        self.reach[key] = [a for a in AGES if (not ages or a in ages) and high <= BODY[a] * TOOLS[tool]]
        assert self.reach[key], f'{key}: contact {high:.0f}px up is out of reach for every allowed age'
        assert all(set(q) <= {'sway', 'lift', 'shake', 'glow', 'puff'} and (self.liftable or 'lift' not in q) for _, q in obj), key + ': obj keys (lift needs liftable=True)'
        assert not obj or d['host'] in ('placed', 'portable'), key + ': obj reactions would move the whole pond or case, or nothing at all'
        touch = [self.spot[q['anchor']] for _, q in tr if q.get('anchor') and q.get('contact', 0) >= .5]
        touch = tuple(p for i, p in enumerate(touch) if not i or p != touch[i - 1])  # touching the same place again is not a new touch
        body = tuple(dict.fromkeys(tuple(round(q.get(j, 0) * 2) for j in 'xybw') for _, q in tr))
        sig = (tuple(tuple(sorted((t, op, (v > 0) - (v < 0)) for t, op, v in d['effects'][n])) for _, n in ev), touch, body, tool if tool in ('none', 'wing') else 'stick')
        for other, s in self.sigs.items():
            assert sum(a != b for a, b in zip(sig, s)) >= 2, f'{key} is the same act as {other}: change at least two of what it does, where it touches, how the body moves, what it uses'
        self.sigs[key], self.group[g] = sig, self.group.get(g, 0) + 1
        if say:
            assert len(say) >= 2 and all(len(s) <= 90 for s in say), key + ': two or three lines of at most 90 characters'
            d['lines'][key] = list(say)
        d['routines'][key] = dict(label=label, duration=dur, tool=tool, group=g, track=tr, events=[list(e) for e in ev], when=list(when), prefer=list(prefer), ages=ages,
                                  say=key if say else None, **({'obj': [list(o) for o in obj]} if obj else {}), **({'pick': pick} if pick else {}))

    def emit(self, need=48):
        d, n = self.d, len(self.d['routines'])
        used, read = {name for r in d['routines'].values() for _, name in r['events']}, ' '.join(t for r in d['routines'].values() for t in r['when'] + r['prefer'])
        per_age = {a: sum(a in v for v in self.reach.values()) for a in AGES}
        assert n >= need and used == set(d['effects']), f'{d["object"]}: {n} routines; unused effects {set(d["effects"]) - used}'
        assert all(f in read for f in d['fields']), f'{d["object"]}: every field must gate or attract some routine, or it changes nothing anyone can see'
        if need >= 48:  # a smaller `need` is a draft run, never a hand-in
            assert self.far <= 4 and all(4 <= self.group.get(g, 0) <= 9 for g in GROUPS), f'{d["object"]}: groups {self.group}, far {self.far}'
            assert min(per_age.values()) >= 16 and per_age['adult'] >= 32, f'{d["object"]}: too few routines in reach for some age {per_age}'
        head = ',\n'.join(f' {json.dumps(key)}: {json.dumps(v)}' for key, v in d.items() if key != 'routines')
        body = ',\n'.join(f'  {json.dumps(key)}: {json.dumps(r)}' for key, r in d['routines'].items())
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / (d['object'] + '.json')).write_text('{\n' + head + ',\n "routines": {\n' + body + '\n }\n}\n')
        print(d['object'], n, 'routines; in reach per age', per_age, '; groups', self.group)


if __name__ == '__main__':  # python3 engine/animation-authoring/rep.py <sprite id>: the drawing with y fraction, height in px and an x ruler in tenths
    import sys
    sp = sprite(sys.argv[1])
    n, ruler = len(sp['art']) - 1, [' '] * sp['w']
    for tenth in range(10):
        ruler[round(tenth * (sp['w'] - 1) / 10)] = str(tenth)
    print(sys.argv[1], '- anchor names already taken by the drawing:', sp['named'], '\n   y   px |' + ''.join(ruler) + '|')
    [print(f'{y / n:.2f} {(sp["ground"] - y) * sp["row"]:4.0f} |{row}|') for y, row in enumerate(sp['art']) if row.strip()]
