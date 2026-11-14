"""Shared helper for repertoire generators. Workers import it and never edit it. It is stricter than
check_repertoire.py on purpose: it refuses relabels, stamped acts, undrawable labels, padding effects,
contacts on empty air, gates nothing can reach or that never change, and copied lines.
Version 2 (after the wave-1 acceptance review)."""
import json, os, re, subprocess
from pathlib import Path
ENG = Path(os.environ.get('REP_ENGINE') or Path(__file__).resolve().parent.parent)
OUT = Path(os.environ.get('REP_OUT') or ENG / 'client/animation/repertoire')
AGES = ['hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary']
YOUNG, GROWN = AGES[:2], AGES[2:]
BODY = dict(zip(AGES, (60.4, 78.7, 96.6, 110.2, 117.7, 123.5, 116., 123.5)))  # px, repertoire-reach.json bodyHeight rounded down
TOOLS = dict(none=1.05, wing=1.1, twig=1.6, reed=1.6)  # reach = body height x factor (export-repertoire-reach.mjs)
GROUPS = ('care', 'use', 'play', 'test', 'rest', 'weather', 'show', 'mishap')
POSE = {'x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor', 'perch'}
TAGS = set('''always wet dry snow storm windy calm warm cold sun night day dawn dusk night_late dawn_or_day clear rainbow_sky growing spring summer fall winter
 tired lonely sad !wet !snow !storm !windy !cold !night !night_late !dawn !dusk !summer !fall !winter !rainbow_sky !tired !lonely !sad'''.split())
MOODS = {'young', 'grown', 'elder', 'happy', 'grumpy', 'curious'}  # prefer only: the harness cannot stage them
REAL = dict(obj=('dirt', 'wetness', 'condition'), subject=('hunger', 'mood', 'health', 'trust', 'growth'),
            keeping=('clarity', 'algae', 'leaves', 'ice', 'oxygen', 'plants', 'flakes', 'bell'), need=('fun', 'social', 'energy', 'cleanliness'))
CMP = re.compile(r'^!?([a-z_]+)(<=|>=|<|>)(-?[0-9.]+)$')
# What a routine IS: one verb from this list and the part it acts on. A (verb, part) pair is used once per object.
VERBS = set('''wipe scrub sweep polish dry rake dig scoop pour tip fill drain peck pull push shove lift tilt rock spin roll drag carry stack balance
 hook prod tug squeeze press pat knock tap ring drum sniff listen peer measure count weigh taste test guard hide seek chase race hop
 climb perch sit lean nap sulk shelter wait stamp walk_into slip stuck bow present argue pose sing shout dance mend straighten warm cool
 shake brace chip scrape fluff groom splash float blow catch throw kick nudge wrap unwrap tie fold open close fit show compare'''.split())
INSPECT = {'count', 'compare', 'measure', 'listen', 'sniff', 'peer'}  # at most three of these in all per object
CLEAN = {'wipe', 'scrub', 'sweep', 'polish', 'dry', 'rake', 'scoop', 'chip', 'scrape', 'groom', 'fluff', 'shake', 'blow', 'pour', 'drain', 'tip', 'brush', 'dig'}
UNDRAWABLE = re.compile(r'\b(spin|spins|spinning|spun|cartwheel\w*|somersault\w*|backflip\w*|knot|knots|knotting|knotted)\b')
UNIVERSAL = {'nap', 'shelter', 'sulk', 'wait', 'walk_into', 'slip', 'stuck', 'stamp', 'bow', 'present', 'argue', 'pose'}  # at most one each per object
SHADOW = {'damp', 'wet', 'wetness', 'dirt', 'dirty', 'grime', 'mud', 'muck', 'dust', 'clean', 'cleanliness', 'condition', 'wear'}  # use obj.* instead
NEVER_DRAWN = re.compile(r'\b(behind|under|underneath|beneath)\b(?! (his|her|its|a) (wing|chin|bill|breath))')
# Labels that put his body in/on/through something (not "knocking on the door" or "breathing on the glass").
NEEDS_PERCH = re.compile(r'\b(stand|sit|lie|lying|perch|climb|walk|step|hop|jump|crawl|wriggl|curl|sleep|nap|doz|roll|bounc|slid|dive|diving|squeez|wad|balanc|danc|strut|march|stomp|stamp|settl|ride|riding|surf|skat|tiptoe|bask|flop|sprawl)\w*\b[^.,;]{0,25}?\b(in|into|inside|on|onto|atop|through|across) the\b')
# Places on Cheese's own body for worn things (coarse body grid, x from tail to bill, y from crown to feet).
BODY_SPOTS = dict(crown=(5, 0), brow=(6, 1), eye=(7, 2), bill=(9, 3), cheek=(7, 3), nape=(4, 2), throat=(7, 4), neck=(6, 4),
                  chest=(7, 5), shoulder=(5, 5), back=(3, 5), belly=(6, 7), wing=(4, 6), wing_tip=(2, 7), tail=(0, 6), rump=(1, 7),
                  thigh=(5, 8), foot_l=(4, 9), foot_r=(7, 9))
K_ADULT, K_SMALL = (2.6, 1.8, 2), (1.4, 1, 1)  # rendered cells per unit of x, y, b (performances.mjs scalePose)
JS = ("import {itemSprite as s,itemWorldScale as w} from './client/ultra-items.mjs';const i=process.argv[1],m=s(i,0,{state:{keeping:{setup:true,fish:[]}}});"
      "console.log(JSON.stringify({w:m.width,art:m.art.map(String),row:7.5*w(i)*(m.detailScale||1)*1.5,"
      "ground:['birdhouse','treehouse'].includes(i)||!m.anchors?.entry?(m.groundRow??m.art.length)-1:m.anchors.entry.y,"
      "named:Object.keys(m.anchors||{}),spec:{construction:m.construction,family:m.family,kind:m.kind,style:m.style,props:m.props,blueprint:m.blueprint,material:m.material},own:Object.fromEntries(Object.entries(m.anchors||{}).map(([k,v])=>[k,typeof v==='object'?v:null]))}))")


def sprite(item):
    return json.loads(subprocess.run(['node', '--input-type=module', '-e', JS, item], cwd=ENG, capture_output=True, text=True, check=True).stdout)


def k(t, at=None, **pose):
    """Keyframe at fraction t. `at` = the anchor being touched (sets contact=1). Only name an anchor on a keyframe that touches it.
    perch=1 stands Cheese ON the touched place (only on anchors flagged 'surface', low enough for the age)."""
    return [t, dict(pose, anchor=at, contact=pose.get('contact', 1)) if at else pose]


def _words(s):
    return set(re.findall(r"[a-z']+", s.lower()))


def stamp(tool, tr, obj=()):
    """The track as drawn at adult size, anchors and marks stripped (same as check_repertoire.stamp)."""
    cells = tuple((int(q.get('x', 0) * 2.6 + .5), int(q.get('y', 0) * 1.8 + .5), int(q.get('b', 0) * 2 + .5),
                   round(q.get('l', 0)), round(q.get('r', 0)), round(q.get('w', 0)), round(q.get('reach', 0) * 2), round(q.get('perch', 0)))
                  for t, q in tr)
    cells = tuple(c for i, c in enumerate(cells) if not i or c != cells[i - 1])  # keyframe order, repeats and exact times ignored
    moved = tuple(dict.fromkeys(tuple(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag')) for _, q in obj))
    return (tool if tool in ('none', 'wing') else 'stick', cells, moved)


def _other_stamps(skip):
    out = {}
    for f in OUT.glob('*.json'):
        if f.stem == skip:
            continue
        try:
            for k2, r2 in json.loads(f.read_text())['routines'].items():
                out[stamp(r2['tool'], r2['track'], r2.get('obj', ()))] = k2
        except Exception:
            pass
    return out


def _content(spec, r):
    """check_repertoire.content for a routine of another object's file (anchors are that file's)."""
    anc = spec.get('anchors', {})
    places = tuple((round(anc[q['anchor']]['x'] / .05), round(anc[q['anchor']]['y'] / .05)) if q.get('anchor') in anc else q.get('anchor') for _, q in r['track'] if q.get('anchor'))
    path = []
    for _, q in r['track']:
        step = tuple(round(q.get(j, 0) * 2) / 2 for j in ('x', 'y', 'b', 'w'))
        if not path or path[-1] != step:
            path.append(step)
    moved = tuple(dict.fromkeys(tuple(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag')) for _, q in r.get('obj', ())))
    rows = tuple(tuple(tuple(x) for x in spec['effects'][n]) for _, n in r['events'])
    return rows, places, r['tool'] if r['tool'] in ('none', 'wing') else 'stick', tuple(path), moved


def _other_contents(skip):
    out = {}
    for f in OUT.glob('*.json'):
        if f.stem == skip:
            continue
        try:
            spec = json.loads(f.read_text())
            for k2, r2 in spec['routines'].items():
                out[_content(spec, r2)] = k2
        except Exception:
            pass
    return out


def _known_lines(skip):
    seen = set()
    brief = ENG / 'overhaul/animation-milestone/authoring-brief.md'
    if brief.exists():
        seen |= {m.lower() for m in re.findall(r'"([^"\n]{12,90})"', brief.read_text())}
    for f in OUT.glob('*.json'):
        if f.stem == skip:
            continue
        try:
            seen |= {l.lower() for ls in json.loads(f.read_text()).get('lines', {}).values() for l in ls}
        except Exception:
            pass
    return seen


class Obj:
    def __init__(self, oid, host, fields, effects, anchors, physics=(), triggers=(), on=None, liftable=False, containers=(), marks=(), parts=None):
        """anchors = {name: (x, y)} or (x, y, 'inside' / 'surface' / 'inside surface') fractions of the host sprite;
        on = that sprite for keeping/display (koi_pond, infinity_pool, trophy_case).
        'inside' allows a point within a hollow outline; 'surface' allows perch=1 there.
        containers = field names that really are a held liquid in a drawn vessel (a bowl, a bucket): only those may be called water/rain/puddle."""
        if host == 'wearable':  # worn things: named places on his own body
            bad = [n for n in anchors if n not in BODY_SPOTS]
            assert not bad, f'{oid}: worn things touch places on his body: anchors must be named from {sorted(BODY_SPOTS)} (not {bad})'
            anchors = {n: (BODY_SPOTS[n][0] / 9, BODY_SPOTS[n][1] / 9) for n in anchors}
        item_anchor = host == 'display' and 'item' in anchors  # the shown thing itself, on its own slot (measured on the lowest)
        if item_anchor:
            anchors = {n: a for n, a in anchors.items() if n != 'item'}
        # Rule 1: name the drawing's parts first (from the art source, not guessed from glyphs); every anchor is one of them.
        assert parts and all(isinstance(v, str) and v for v in parts.values()), f'{oid}: parts=dict(name="what the drawing really shows here", ...) is required'
        off_parts = [n for n in anchors if n != 'item' and not any(n == p or n.startswith(p + '_') for p in parts)]
        assert not off_parts, f'{oid}: anchors {off_parts} are not parts of the drawing (name them part or part_side from parts=)'
        self.parts = parts
        if host == 'display':  # the case's own state (fog, prints, rime...) belongs to the case, not the thing shown in it
            copies = [f for f in fields if f in {'fog', 'mist', 'prints', 'rime', 'frost', 'glare', 'dust', 'smudge', 'smear', 'condensation', 'breath', 'scuffs'}]
            assert not copies, f'{oid}: fields {copies} are the case\'s state: author them on trophy_case / cabinet, not on the thing shown'
        flags = {n: (a[2].split() if len(a) > 2 else []) for n, a in anchors.items()}
        self.flags = flags
        self.d = d = dict(object=oid, host=host, fields={f: list(v) for f, v in fields.items()}, physics=[list(p) for p in physics],
                          triggers=[[w, [list(r) for r in rows]] for w, rows in triggers], effects={n: [list(r) for r in rows] for n, rows in effects.items()},
                          anchors={n: dict(x=a[0], y=a[1]) for n, a in anchors.items()}, lines={}, routines={})
        self.liftable, self.sigs, self.group, self.reach, self.far, self.h = liftable, {}, {}, {}, 0, dict.fromkeys(anchors, 0)
        self.acts, self.verbs, self.fired, self.needy, self.used_anchors = set(), {}, {}, 0, set()
        self.spot = {n: (round(a[0] * 8), round(a[1] * 8)) for n, a in anchors.items()}
        assert host in ('placed', 'portable', 'keeping', 'display', 'wearable') and (on is None) == (host not in ('keeping', 'display')), oid + ': host/on'
        assert all(re.fullmatch('[a-z_]+', f) and not f.startswith(('pond_', 'fish_', 'obj_')) and f != 'history' for f in fields), oid + ': field names are [a-z_]+'
        for f in fields:
            assert f not in SHADOW, f'{oid}: field {f} shadows the real drawn wear: use obj.dirt / obj.wetness / obj.condition and gate on obj_dirt etc.'
            assert f not in ('water', 'rain', 'puddle') or f in containers, \
                f'{oid}: field {f} is only allowed for a drawn vessel that holds it: pass containers={{"{f}"}} if that is what it is'
        for n, rows in d['effects'].items():
            for t, op, v in rows:
                a, _, b = t.partition('.')
                ok = t in fields or (b in REAL.get(a, ()) and (a != 'need' or (op == 'add' and abs(v) <= 3)) and (a in ('need', 'obj') or host == 'keeping'))
                assert ok and op in ('set', 'add', 'mul', 'max', 'min', 'wrap'), f'{oid}: effect {n} row {t} {op} would do nothing, or is not allowed'
                assert not (op == 'add' and abs(v) < .1) and not (op == 'mul' and .85 < v < 1.18), f'{oid}: effect {n} row {t} {op} {v} is padding (too small to matter)'
        self.sp = None
        if liftable and host != 'wearable':
            tall = sprite(oid)
            assert (tall['ground']) * tall['row'] <= 70, f'{oid}: liftable=True but it is {(tall["ground"]) * tall["row"]:.0f} px tall; a duck lifts only small things (70 px or less)'
        if host != 'wearable':  # worn things play on Cheese's own body: nothing to measure
            sp = self.sp = sprite(on or oid)
            rows = len(sp['art']) - 1
            for n, a in anchors.items():
                x, y = a[0], a[1]
                cx, cy = round(x * (sp['w'] - 1)), round(y * rows)
                assert n not in sp['named'] and n not in ('contact', 'entry'), f'{oid}: anchor name {n} is taken by the drawing {sp["named"]}'
                near = range(max(0, cy - 1), min(rows, cy + 1) + 1)
                on_ink = any(sp['art'][r][max(0, cx - 4):cx + 5].strip() for r in near)
                inside = any(sp['art'][r][:cx].strip() and sp['art'][r][cx + 1:].strip() for r in near)
                assert on_ink or ('inside' in flags[n] and inside), f'{oid}: anchor {n} is on empty air (flag it (x, y, "inside") only if it is truly within a drawn outline)'
                self.h[n], self.spot[n] = (sp['ground'] - y * rows) * sp['row'], (round(cx * sp['row'] / 22.5), round(cy * sp['row'] / 15))
                self.h[n] = max(0., self.h[n])  # parts drawn in front of the standing line are on the ground in front of him
        if item_anchor:
            slots = json.loads((ENG / 'client/animation/repertoire-reach.json').read_text()).get('displaySlots', {}).get(on, [0])
            self.h['item'], self.spot['item'], self.flags['item'] = float(slots[0]), ('item',), []
            d['anchors']['item'] = dict(x=.5, y=.5)  # resolved at draw time to the thing's own slot
        INKS = ('snow', 'frost', 'leaf', 'water', 'mud', 'glow', 'dust', 'plant')
        POND = ('clarity', 'algae', 'leaves', 'ice', 'oxygen', 'plants', 'flakes', 'bell')
        if host == 'keeping':  # the pond's own state is the truth: no copies of it on the fish
            copies = [f for f in fields if f in {'leaves', 'leafmat', 'litter', 'ice', 'rime', 'crust', 'frost', 'flakes', 'flakeskin', 'algae', 'film', 'scum', 'slime', 'murk', 'clarity'}]
            assert not copies, f'{oid}: fields {copies} copy the pond (use keeping.* effects, pond_* gates and pond_* marks)'
        for f, th, glyphs, a, tone in marks:  # visible state: glyphs stamped at an anchor while the field is above th
            assert (f in fields or (host == 'keeping' and f.startswith('pond_') and f[5:] in POND)) and a in anchors and tone in INKS and 1 <= len(glyphs) <= 8 and re.fullmatch(r'[ -~]+', glyphs) and host in ('placed', 'portable', 'display', 'keeping'), \
                f'{oid}: mark {f}: needs a declared field and anchor, ascii glyphs (1-8), tone in {INKS}, not on worn pieces'
        if marks:
            d['marks'] = [list(m) for m in marks]
        spots = {}
        for n, s in self.spot.items():
            assert s not in spots, f'{oid}: anchors {spots.get(s)} and {n} are the same touch place; merge them or move one'
            spots[s] = n

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
            return
        f = m.group(1)
        if f.startswith(('pond_', 'fish_')):
            assert self.d['host'] == 'keeping', key + ': fish_/pond_ fields need a keeping host'
            return
        if f.startswith('obj_'):
            assert f[4:] in REAL['obj'] and self.d['host'] != 'wearable', key + ': obj_dirt / obj_wetness / obj_condition only, and not on wearables'
            return
        assert f in self.d['fields'], f'{key}: `{tok}` reads an undeclared field'
        (default, lo, hi), v, rising = self.d['fields'][f], float(m.group(3)), (m.group(2) in ('>', '>=')) != tok.startswith('!')
        holds, inside = (default > v, v < hi) if rising else (default < v, v > lo)
        assert inside and (holds or self.moves(f, rising)), f'{key}: `{tok}` can never come true: nothing moves {f} that far'
        if gate:
            assert not holds or self.moves(f, not rising), f'{key}: `{tok}` is always true: nothing ever moves {f} the other way, so it gates nothing'
            decay = [dv for pf, op, dv, _ in self.d['physics'] if pf == f and op == 'decay']
            if decay:
                d0, push = decay[0], max([pv for pf, op, pv, _ in self.d['physics'] if pf == f and op == 'rate' and pv > 0] or [0])
                ok = (d0 + 22 * push > v + .1) if rising else (d0 < v - .1)
                assert ok, (f'{key}: `{tok}` gates on {f}, which decays to {d0} within a minute; Cheese comes back after two. '
                            'Put the push and its consequence in one routine, or use a slow rate field.')

    def _rendered(self, tr, k3, tool):
        poses = []
        for _, q in tr:
            p = (int(q.get('x', 0) * k3[0] + .5), int(q.get('y', 0) * k3[1] + .5), int(q.get('b', 0) * k3[2] + .5),
                 round(q.get('l', 0)), round(q.get('r', 0)), round(q.get('w', 0)) if tool == 'none' else round(q.get('reach', 0) * 2), round(q.get('perch', 0)))
            if not poses or poses[-1] != p:
                poses.append(p)
        return tuple(poses)

    def r(self, slug, label, dur, tool, track, ev=(), *, g, act, when=(), prefer=(), ages=None, say=None, obj=(), pick=None, far=False, shown=None, duo=None):
        """act = (verb, part): what this routine is, e.g. ('tip', 'tyre') or ('peer', 'opening'). shown='head' allows 'through the' / 'into the'
        in the label when only his head goes in (and the track shows it: x forward, contact on that anchor)."""
        d, key, tr = self.d, self.d['object'] + '_' + slug, [[0, {}], *track, [1, {}]]
        when = sorted(when, key=lambda t: (not t.startswith('!'), t == 'storm'))  # the harness stages tokens in order: negations first, storm last
        assert key not in d['routines'] and tool in TOOLS and g in GROUPS and 10 <= dur <= 60 and len(track) >= 3, key + ': id, tool, group, duration or too few keyframes'
        assert [t for t, _ in tr] == sorted({t for t, _ in tr}) and all(set(q) <= POSE for _, q in tr), key + ': track order, or a key the renderer does not draw'
        verb, part = act
        if duo is not None:
            # A duet: a visiting friend does their own part (their own track, their own touches). It only runs while a
            # friend is here, and must be a different act from the solo ones (the partner's touches count in the signature).
            assert d['host'] in ('placed', 'portable', 'keeping', 'display'), key + ': duets happen at an object (not on a worn piece)'
            dtr = [[0, {}], *duo, [1, {}]]
            assert len(duo) >= 3 and all(set(q) <= POSE for _, q in dtr) and [t for t, _ in dtr] == sorted({t for t, _ in dtr}), key + ': duo track keys/order'
            assert any(q.get('anchor') in d['anchors'] and q.get('contact', 0) >= .5 for _, q in dtr), key + ': the partner must touch something (an anchor of this object)'
            self.used_anchors |= {q['anchor'] for _, q in dtr if q.get('anchor')}
        assert verb in VERBS, f'{key}: act verb {verb} is not in the verb list'
        assert (verb, part) not in self.acts, f'{key}: ({verb}, {part}) is already an act of this object; write a different act'
        assert self.verbs.get(verb, 0) < (1 if verb in UNIVERSAL else 3), f'{key}: too many `{verb}` acts (universal acts: one each; others: three)'
        assert verb not in UNIVERSAL or sum(self.verbs.get(u, 0) for u in UNIVERSAL) < 5, f'{key}: at most five stock acts (nap, sulk, bow, slip...) per object; write acts only this object allows'
        assert verb not in INSPECT or sum(self.verbs.get(u, 0) for u in INSPECT) < 3, f'{key}: at most three inspecting acts (count, compare, measure, listen, sniff, peer) per object'
        stem = verb.split('_')[0][:4]
        assert stem in label.lower(), f'{key}: the label must say what the verb says (`{verb}` not in "{label}"); pick the verb that matches the act'
        assert not UNDRAWABLE.search(label.lower()), f'{key}: "{label}" names motion the renderer cannot draw (spin, cartwheel, somersault, knot)'
        perched = any(q.get('perch', 0) > .01 for _, q in tr)
        assert not NEVER_DRAWN.search(label.lower()), f'{key}: "{label}" promises something the renderer never draws (he is never behind or under anything)'
        assert not NEEDS_PERCH.search(label.lower()) or perched or shown == 'head', \
            f'{key}: "{label}" puts him in/on/through the object; use perch on a surface anchor, or shown="head" if only his head goes in'
        [self.token(key, tok, True) for tok in when], [self.token(key, tok, False) for tok in prefer]
        assert 'storm' not in when or (tool == 'none' and 'wet' in when and dur >= 30), key + ': a storm routine is a long tool-free shelter that also lists `wet`'
        for t, name in ev:
            touching = any(abs(qt - t) < .011 and q.get('contact', 0) >= .5 and q.get('anchor') for qt, q in tr)
            assert name in d['effects'] and .1 <= t <= .9 and (touching or far), f'{key}: event {name} at {t} has no touching keyframe'
        for _, name in ev:
            for t2, op, v in d['effects'][name]:
                if t2 in ('obj.dirt', 'obj.wetness') and (op in ('min', 'set') and v < .5 or op == 'add' and v < 0 or op == 'mul' and v < 1):
                    assert verb in CLEAN, f'{key}: cleaning or drying {t2} needs a cleaning verb ({sorted(CLEAN)}), not `{verb}`'
                    assert any(w.startswith(t2.replace('.', '_') + '>') for w in when), f'{key}: cleans or dries {t2} but does not gate on {t2.replace(".", "_")}>...'
        self.far += bool(far)
        held, last = [], None
        for _, q in tr:
            last = q.get('anchor') or last
            held.append(last)
        assert all(a in d['anchors'] for a in held if a), key + ': undeclared anchor'
        self.used_anchors |= {a for a in held if a}
        high = max([self.h[a] for i in range(len(tr) - 1) if max(tr[i][1].get('contact', 0), tr[i + 1][1].get('contact', 0)) > .05 for a in held[i:i + 2] if a] or [0])
        allowed = [a for a in AGES if (not ages or a in ages) and high <= BODY[a] * TOOLS[tool]]
        if perched:
            for i, (_, q) in enumerate(tr):
                if q.get('perch', 0) > .01:
                    a = held[i]
                    assert a and 'surface' in self.flags.get(a, []), f'{key}: perch needs a held anchor flagged "surface"'
                    allowed = [g2 for g2 in allowed if self.h[a] <= .6 * BODY[g2]]
            assert allowed, f'{key}: the perch surface is too high for every allowed age (at most .6 x body height)'
        self.reach[key] = allowed
        assert self.reach[key], f'{key}: contact {high:.0f}px up is out of reach for every allowed age'
        worn, shown = d['host'] == 'wearable', d['host'] == 'display'
        MOVE = {'ix', 'iy', 'hold', 'off'} if worn else {'hold'} if shown else {'ix', 'iy', 'hold', 'hide'}
        WORN = {'off', 'wx', 'wy', 'flap', 'sag', 'ix', 'iy', 'hold'}
        if worn:
            assert all(set(q) <= WORN for _, q in obj), key + ': a worn piece moves with off / wx / wy / flap / sag, or off + hold / ix / iy when taken off'
            assert all(q.get('off', 0) > .5 or not any(abs(q.get(m, 0)) > .01 for m in ('hold', 'ix', 'iy')) for _, q in obj), key + ': hold / ix / iy only once the piece is off (off=1)'
        elif d['host'] == 'keeping':
            assert all(set(q) <= {'lure'} for _, q in obj), key + ': a kept fish answers with lure (it swims to the touched rim spot); the pond itself never moves'
            assert not obj or pick, key + ': lure needs pick= (which fish comes: hungriest or shyest)'
        elif shown:
            assert all(set(q) <= {'hold'} for _, q in obj), key + ': a shown thing can only be lifted out (hold) and put back'
            assert not obj or any(q.get('anchor') == 'item' and q.get('contact', 0) >= .5 for _, q in tr), key + ': lift it by touching it (anchor "item")'
        else:
            assert all(set(q) <= {'sway', 'lift', 'shake', 'glow', 'puff'} | MOVE and (self.liftable or not ({'lift', 'hold'} & set(q))) for _, q in obj), key + ': obj keys (lift/hold need liftable=True)'
            assert not obj or d['host'] in ('placed', 'portable'), key + ': obj reactions would move the whole pond or case, or nothing at all'
            assert d['host'] == 'portable' or not any(MOVE & set(q) for _, q in obj), key + ': only a loose (portable) object can be carried, tossed or hidden'
        if d['host'] == 'placed' and self.sp and self.sp['ground'] * self.sp['row'] > 200:
            assert all(abs(q.get('sway', 0)) <= .15 and abs(q.get('shake', 0)) <= .15 for _, q in obj), key + ': a building does not sway or shake (at most .15) because a duck leaned on it'
        if re.search(r'\b(roll|rolls|rolling|rolled)\b', label.lower()):
            assert any(abs(q.get('ix', 0)) + abs(q.get('iy', 0)) > .5 for _, q in obj) or perched, f'{key}: "{label}" rolls something: the object must move (ix/iy) or he must be perched rolling on it'
        moving = [(t, q) for t, q in obj if any(abs(q.get(m, 0)) > .01 for m in MOVE)]
        if moving:
            last, end = moving[-1][0], [t for t, q in obj if t > moving[-1][0] and not any(abs(q.get(m, 0)) > .01 for m in MOVE)]
            assert end, key + ': a moved, held, hidden or taken-off object must be brought back: end the obj track at rest (all move keys 0)'
            fetched = moving[-1][1].get('hold', 0) > .5 or any(last <= t <= end[0] and q.get('contact', 0) >= .5 for t, q in tr)
            assert fetched, key + ': the object returns to rest only while Cheese holds or touches it (no gliding home on its own)'
        youngest = allowed[0]
        small = self._rendered(tr, K_SMALL if youngest in YOUNG else K_ADULT, tool)
        assert len(set(small)) >= 3, f'{key}: at {youngest} size the body shows fewer than 3 different poses; make the movement bigger'
        if not hasattr(self, '_stamps'):
            self._stamps = _other_stamps(d['object'])
        twin = self._stamps.get(stamp(tool, tr, obj))
        assert not twin, f'{key}: the same drawn track as {twin} on another object (a stamped act); move differently'
        touch = [self.spot[q['anchor']] for _, q in tr if q.get('anchor') and q.get('contact', 0) >= .5]
        touch = tuple(p for i, p in enumerate(touch) if not i or p != touch[i - 1])
        body = self._rendered(tr, K_ADULT, tool)
        moved = tuple(dict.fromkeys(tuple(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag')) for _, q in obj))
        sig = (tuple(tuple(sorted((t, op, (v > 0) - (v < 0)) for t, op, v in d['effects'][n] if not t.startswith('need.'))) for _, n in ev), touch, body,
               tool if tool in ('none', 'wing') else 'stick', moved,
               tuple(dict.fromkeys(self.spot.get(q['anchor']) for _, q in [[0, {}], *duo] if q.get('anchor'))) if duo else None)
        for other, s in self.sigs.items():
            assert sum(a != b for a, b in zip(sig, s)) >= 2, f'{key} is the same act as {other}: change at least two of what it does, where it touches, how the body moves, what it uses, how the object moves'
        touched = frozenset(q['anchor'] for _, q in tr if q.get('anchor') and q.get('contact', 0) >= .5)
        targets = frozenset(t for _, n in ev for t, _, _ in d['effects'][n] if not t.startswith('need.'))
        motion = frozenset(m for _, q in obj for m, v in q.items() if abs(v) > .01)
        place_key = (touched, tool if tool in ('none', 'wing') else 'stick', perched)
        for other, (pk, tg, mo) in getattr(self, 'places_seen', {}).items():
            if pk == place_key and touched:
                assert tg != targets or mo != motion, f'{key} touches the same parts with the same tool as {other} and changes the same thing: that is the same act; touch other parts or do something else to the object'
        self.places_seen = {**getattr(self, 'places_seen', {}), key: (place_key, targets, motion)}
        if not touched and not duo:
            self.untouched = getattr(self, 'untouched', 0) + 1
            assert self.untouched <= 2, f'{key}: at most two routines per object touch nothing (mime in front of the object); act on the object'
        for _, n in ev:
            self.fired[n] = self.fired.get(n, 0) + 1
            only_need = all(t.startswith('need.') for t, _, _ in d['effects'][n])
            assert self.fired[n] <= (2 if only_need else 3), f'{key}: effect {n} is fired by too many routines; an effect is the result of one kind of act'
        self.needy += any(t.startswith('need.') for _, n in ev for t, _, _ in d['effects'][n])
        assert self.needy <= 8, f'{key}: more than 8 routines carry need rows'
        # The harness's own same-act check (check_repertoire.content), so a helper pass means a harness pass.
        anc = d['anchors']
        places = tuple((round(anc[q['anchor']]['x'] / .05), round(anc[q['anchor']]['y'] / .05)) if q.get('anchor') in anc else q.get('anchor') for _, q in tr if q.get('anchor'))
        path = []
        for _, q in tr:
            step = tuple(round(q.get(j, 0) * 2) / 2 for j in ('x', 'y', 'b', 'w'))
            if not path or path[-1] != step:
                path.append(step)
        hmoved = tuple(dict.fromkeys(tuple(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag')) for _, q in obj))
        hc = (tuple(tuple(tuple(x) for x in d['effects'][n]) for _, n in ev), places, tool if tool in ('none', 'wing') else 'stick', tuple(path), hmoved)
        if not hasattr(self, '_contents'):
            self._contents = _other_contents(d['object'])
        twin = self._contents.get(hc)
        assert not twin, f'{key} is a copy of {twin} on another object by the harness check; change the act'
        for other, theirs in getattr(self, 'hcontent', {}).items():
            assert sum(a != b for a, b in zip(hc, theirs)) >= 2, f'{key} is the same act as {other} by the harness check (two of effect/touch/body/tool/object motion must differ)'
        self.hcontent = {**getattr(self, 'hcontent', {}), key: hc}
        self.sigs[key], self.group[g] = sig, self.group.get(g, 0) + 1
        self.acts.add((verb, part))
        self.verbs[verb] = self.verbs.get(verb, 0) + 1
        if say:
            assert 2 <= len(say) <= 3 and all(len(s) <= 90 for s in say), key + ': two or three lines of at most 90 characters'
            known = getattr(self, '_known', None)
            if known is None:
                known = self._known = _known_lines(d['object'])
            for i, s in enumerate(say):
                assert s.lower() not in known, f'{key}: line "{s}" is copied from the brief or another object'
                assert 'goose' not in s.lower(), f'{key}: Cheese is a duck'
                assert not re.search(r'\b(nobody|everyone|everybody)\b', s.lower()), f'{key}: no "nobody/everyone" formula lines'
                for sentence in [x.strip().lower() for x in re.split(r'[.!?]+', s) if len(x.strip()) > 3]:
                    self.sentences = getattr(self, 'sentences', {})
                    self.sentences[sentence] = self.sentences.get(sentence, 0) + 1
                    assert self.sentences[sentence] <= 3, f'{key}: "{sentence}" is used in more than three lines of this object'
                for prev in say[:i]:
                    a, b = _words(s), _words(prev)
                    assert len(a & b) <= .5 * min(len(a), len(b)), f'{key}: line "{s}" repeats "{prev}"; the second line is a different joke'
            self._known |= {s.lower() for s in say}
            d['lines'][key] = list(say)
        d['routines'][key] = dict(label=label, duration=dur, tool=tool, group=g, act=[verb, part], track=tr, events=[list(e) for e in ev], when=list(when),
                                  prefer=list(prefer), ages=ages, say=key if say else None, **({'far': True} if far else {}),
                                  **({'obj': [list(o) for o in obj]} if obj else {}), **({'pick': pick} if pick else {}),
                                  **({'duo': {'track': [[0, {}], *[list(x) for x in duo], [1, {}]]}} if duo else {}))

    def emit(self, need=None, shortfall=None):
        """emit() hands in: the object's full need (48, less any wonder routines it already has).
        emit(need=N) is a draft run only: it writes the file but skips the hand-in thresholds."""
        d, n = self.d, len(self.d['routines'])
        d['parts'] = self.parts
        queue = {o['id']: o for o in json.loads((ENG / 'overhaul/animation-milestone/work-queue.json').read_text())['objects']}
        q0 = queue.get(d['object'], {})
        full = q0.get('need', 48 - q0.get('wonder_routines', 0))  # shared-host items have their own quota (user decision 2026-11-14)
        hand_in = need is None
        if shortfall:  # rule 19: an honest stop with a reason, recorded in the file
            assert hand_in and len(shortfall) > 20, 'shortfall=<the reason, in a sentence>'
            d['shortfall'] = shortfall
            full = n
        need = full if hand_in else need
        used, read = {name for r in d['routines'].values() for _, name in r['events']}, ' '.join(t for r in d['routines'].values() for t in r['when'] + r['prefer'])
        per_age = {a: sum(a in v for v in self.reach.values()) for a in AGES}
        print(d['object'], n, 'routines; in reach per age', per_age, '; groups', self.group, '; verbs', len(self.verbs))
        assert n >= need and used == set(d['effects']), f'{d["object"]}: {n} routines (need {need}); unused effects {set(d["effects"]) - used}'
        assert all(f in read for f in d['fields']), f'{d["object"]}: every field must gate or attract some routine, or it changes nothing anyone can see'
        if hand_in:
            unused = set(d['anchors']) - self.used_anchors
            assert not unused, f'{d["object"]}: anchors no routine uses: {sorted(unused)}'
            lo, hi = max(1, full // 12), max(2, -(-full * 9 // 48))
            assert self.far <= 4 and all(lo <= self.group.get(g, 0) <= hi for g in GROUPS), f'{d["object"]}: groups {self.group} (each {lo}..{hi}), far {self.far}'
            floor, adult = -(-full // 3), -(-full * 2 // 3)
            assert min(per_age.values()) >= floor and per_age['adult'] >= adult, f'{d["object"]}: too few routines in reach for some age {per_age} (floor {floor}, adult {adult})'
        head = ',\n'.join(f' {json.dumps(key)}: {json.dumps(v)}' for key, v in d.items() if key != 'routines')
        body = ',\n'.join(f'  {json.dumps(key)}: {json.dumps(r)}' for key, r in d['routines'].items())
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / (d['object'] + '.json')).write_text('{\n' + head + ',\n "routines": {\n' + body + '\n }\n}\n')


if __name__ == '__main__':
    # rep.py <sprite id>: the drawing with y fraction, height in px above the standing line, an x ruler in tenths,
    # and the drawing's own anchors (real door / seat / opening) marked with digits. rep.py <sprite id> --mark <generator.py>:
    # also letters at each anchor that generator declares for that sprite.
    import sys
    sp = sprite(sys.argv[1])
    n, ruler = len(sp['art']) - 1, [' '] * sp['w']
    for tenth in range(10):
        ruler[round(tenth * (sp['w'] - 1) / 10)] = str(tenth)
    # The blueprint the drawing is built from (what each part really is), from the workshop sources.
    for src in sorted((ENG / 'client').glob('*-workshop.mjs')) + sorted((ENG / 'client/animation').glob('*.json')):
        text = src.read_text()
        m = re.search(r'["\']?\b' + re.escape(sys.argv[1]) + r'\b["\']?\s*:\s*\{', text)
        if m:
            print('  blueprint (' + src.name + '):', re.sub(r'\s+', ' ', text[m.start():m.start() + 420]))
            break
    art = [list(r) for r in sp['art']]
    legend = []
    for i, (name, a) in enumerate(sorted((k2, v) for k2, v in sp['own'].items() if v and 'x' in v and 'y' in v)):
        ch = str(i % 10)
        legend.append(f'{ch}={name}({a["x"] / max(1, sp["w"] - 1):.2f},{a["y"] / max(1, n):.2f})')
        ry, rx = int(round(a['y'])), int(round(a['x']))
        if 0 <= ry <= n and 0 <= rx < sp['w']:
            art[ry][rx] = ch
    if '--mark' in sys.argv:
        src = Path(sys.argv[sys.argv.index('--mark') + 1]).read_text()
        block = re.search(r"Obj\(\s*'" + re.escape(sys.argv[1]) + r"'.*?anchors=dict\((.*?)\)\)", src, re.S)
        if '--object' in sys.argv:  # an object measured on another sprite (on='trophy_case', 'koi_pond', ...)
            block = re.search(r"Obj\(\s*'" + re.escape(sys.argv[sys.argv.index('--object') + 1]) + r"'.*?anchors=dict\((.*?)\)\)", src, re.S)
        if block:
            for i, m in enumerate(re.finditer(r"(\w+)=\(([0-9.]+),\s*([0-9.]+)", block.group(1))):
                ch = chr(65 + i % 26)
                legend.append(f'{ch}={m.group(1)}')
                ry, rx = round(float(m.group(3)) * n), round(float(m.group(2)) * (sp['w'] - 1))
                art[ry][rx] = ch
    print(sys.argv[1], '- art source:', {k: v for k, v in sp.get('spec', {}).items() if v}, '\n  names taken by the drawing:', sp['named'], '\n  drawing anchors:', ' '.join(legend), '\n   y   px |' + ''.join(ruler) + '|')
    [print(f'{y / n:.2f} {(sp["ground"] - y) * sp["row"]:4.0f} |{"".join(row)}|') for y, row in enumerate(art) if ''.join(row).strip()]
