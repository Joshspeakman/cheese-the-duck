"""Generic native validation for repertoire objects (one harness for all 609).

usage: .venv/bin/python engine/check_repertoire.py [--objects a,b,c] [--min 48] [--quick]
Static: tokens known, effects valid, tracks ordered, contacts ordered, >= --min routines,
distinct within the object, distinct from same-host siblings. Native: every routine at
every age that can reach it, in DesktopGame with disposable saves: eligible in a
synthesised authored context, nothing before arrival, exact contacts in order at the
object, one completion and memory, no items/coins, replay no-op.
"""
import os, sys, tempfile, json, copy, time
from pathlib import Path
from datetime import datetime, timedelta
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-repertoire-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, repertoire as R, keeping as K, wonders as W
from world.habitat import PlacedItem
from world.fishing import CaughtFish, FishingSpot, BaitType
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine
args = sys.argv[1:]
only = set(args[args.index('--objects') + 1].split(',')) if '--objects' in args else None
MIN = int(args[args.index('--min') + 1]) if '--min' in args else None   # default: each object's own need
QUICK = '--quick' in args
FRAMES = int(args[args.index('--frames') + 1]) if '--frames' in args else 0   # review frames per object
frames_out = []
sys.stdout = host.WIRE
checks, started = [], time.time()
AGES = ('hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary')
POSE = ('x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor', 'perch')


def check(ok, label):
    assert ok, label
    checks.append(label)


check(not R.LOAD_ERRORS, 'every repertoire file loads: ' + '; '.join(R.LOAD_ERRORS))
objects = [] if '--hosts' in args else sorted(o for o in R.OBJECTS if only is None or o in only)


def contact_at(r, t):
    track = r['track']
    a, b = track[0], track[-1]
    for i in range(1, len(track)):
        if t <= track[i][0]:
            a, b = track[i - 1], track[i]
            break
    u = max(0., min(1., (t - a[0]) / max(.001, b[0] - a[0])))
    u = u * u * (3 - 2 * u)
    return a[1].get('contact', 0) + (b[1].get('contact', 0) - a[1].get('contact', 0)) * u


def content(oid, r):
    """What a routine physically is, independent of names: effect rows, touched
    places by position, tool class, coarse body path with repeats removed."""
    spec = R.OBJECTS[oid]
    rows = tuple(tuple(tuple(x) for x in spec['effects'][n]) for _, n in r['events'])
    anc = spec.get('anchors', {})
    places = tuple((round(anc[q['anchor']]['x'] / .05), round(anc[q['anchor']]['y'] / .05)) if q.get('anchor') in anc else q.get('anchor')
                   for _, q in r['track'] if q.get('anchor'))
    path = []
    for _, q in r['track']:
        step = tuple(round(q.get(k, 0) * 2) / 2 for k in ('x', 'y', 'b', 'w'))
        if not path or path[-1] != step:
            path.append(step)
    moved = tuple(dict.fromkeys(tuple(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag')) for _, q in r.get('obj', ())))
    return rows, places, r['tool'] if r['tool'] in ('none', 'wing') else 'stick', tuple(path), (r.get('act') or [None])[0], moved


def stamp(r):
    """The track as drawn at adult size, anchors and marks stripped: the same body
    moving at the same moments. Two objects never share one (stamped acts)."""
    cells = tuple((round(t, 2), int(q.get('x', 0) * 2.6 + .5), int(q.get('y', 0) * 1.8 + .5), int(q.get('b', 0) * 2 + .5),
                   round(q.get('l', 0)), round(q.get('r', 0)), round(q.get('w', 0)), round(q.get('reach', 0) * 2), round(q.get('perch', 0)))
                  for t, q in r['track'])
    moved = tuple((round(t, 2), *(round(q.get(m, 0)) for m in ('ix', 'iy', 'hold', 'hide', 'off', 'wx', 'wy', 'flap', 'sag'))) for t, q in r.get('obj', ()))
    return (r['tool'] if r['tool'] in ('none', 'wing') else 'stick', cells, moved)


STAMPS = {}
for _o in R.OBJECTS:
    for _k in R.by_object(_o):
        STAMPS.setdefault(stamp(R.ROUTINES[_k]), []).append((_o, _k))
STRICT = '--strict' in args
incomplete = {}

# One index of every routine's physical content, built once (scales to all objects).
CONTENT = {}
for _o in R.OBJECTS:
    for _k in R.by_object(_o):
        CONTENT.setdefault(content(_o, R.ROUTINES[_k]), []).append((_o, _k))
check('--hosts' in args or only is None or set(objects) == only, 'requested objects exist: ' + str(sorted((only or set()) - set(objects))))
KNOWN = set(W.FLAGS) | {'dry_axle', 'far_year'} | set(R.CHEESE_TAGS)
probe = W.World.__new__(W.World)
probe.weather, probe.wet, probe.temperature, probe.wind, probe.hour, probe.season, probe.outdoors = 'sunny', False, 15, .1, 12, 'spring', True


def kind_of(token, fields):
    t = token.lstrip('!')
    m = W.COMPARE.match(t)
    if m:
        f = m.group(1)
        return 'field' if f in fields or f[4:] in R.OBJ_STATE and f.startswith('obj_') or (f.startswith('pond_') and f[5:] in K.POND) or (f.startswith('fish_') and (f[5:] in K.FISH or f == 'fish_count')) else None
    return 'tag' if t in KNOWN or probe.tag(t) is not None else None


def signature(r):
    parts = tuple(sorted({k for _, q in r['track'] for k in q if k not in POSE}))
    trace = tuple((round(q.get('x', 0)), round(q.get('y', 0)), round(q.get('b', 0)), round(q.get('w', 0)), bool(q.get('contact'))) for _, q in r['track'])
    anchors = tuple(sorted({q['anchor'] for _, q in r['track'] if q.get('anchor')}))
    obj = tuple(sorted({k for _, q in r.get('obj', []) for k in q}))
    return (tuple(n for _, n in r['events']), anchors, r['tool'], parts, obj, trace)


reach_ok = True
for oid in objects:
    spec = R.OBJECTS[oid]
    fields = spec.get('fields', {})
    keys = R.by_object(oid)
    need = R.need(oid) if MIN is None else MIN
    if len(keys) < need and MIN is None and not STRICT:
        incomplete[oid] = f'{len(keys)}/{need}'   # authored so far; listed, every routine still checked
    else:
        check(len(keys) >= need, oid + f' has {len(keys)} routines (need {need})')
    for f, op, v, when in spec.get('physics', []):
        check(f in fields and op in ('rate', 'decay', 'wrap') and all(kind_of(t, fields) for t in when.split('&')), oid + ' physics row ' + f + ' ' + when)
    for name, rows in spec.get('effects', {}).items():
        check(all((t in fields or t.startswith('subject.') or t.startswith('need.') or t.startswith('keeping.') or t.startswith('obj.')) and op in ('set', 'add', 'mul', 'max', 'min', 'wrap') for t, op, _ in rows), oid + ' effect ' + name)
    sigs = {}
    far = 0
    mine_seen = []
    for k in keys:
        r = R.ROUTINES[k]
        for t in r['when'] + r['prefer']:
            check(kind_of(t, fields), k + ' tag ' + t + ' is understood')
        check(all(n in spec['effects'] for _, n in r['events']), k + ' events are this object\'s effects')
        times = [q[0] for q in r['track']]
        check(times == sorted(times) and times[0] == 0 and times[-1] == 1, k + ' track ordered 0..1')
        check([e[0] for e in r['events']] == sorted(e[0] for e in r['events']) and all(0 < e[0] < 1 for e in r['events']), k + ' contacts ordered inside the routine')
        anchors = {q['anchor'] for _, q in r['track'] if q.get('anchor')}
        check(all(a in spec.get('anchors', {}) or a in ('contact', 'entry') for a in anchors) or spec.get('named_anchors'), k + ' anchors are declared: ' + str(anchors))
        if r.get('say'):
            check(len(spec.get('lines', {}).get(r['say'], [])) >= 2, k + ' has two authored lines for its cue')
        sig = signature(r)
        check(sig not in sigs, k + ' is physically distinct from ' + str(sigs.get(sig)))
        sigs[sig] = k
        far += bool(r.get('far'))
        for at, name in r['events']:
            check(r.get('far') or contact_at(r, at) >= .5, k + ' effect ' + name + ' lands on a touch, not on air')
        mine = content(oid, r)
        stamped = [k2 + ' on ' + o2 for o2, k2 in STAMPS.get(stamp(r), []) if o2 != oid]
        check(not stamped, k + ' is not a stamped copy (same drawn track) of ' + ', '.join(stamped))
        copies = [k2 + ' on ' + o2 for o2, k2 in CONTENT.get(mine, []) if o2 != oid]
        check(not copies, k + ' is not a copy of ' + ', '.join(copies))
        # Within an object, two routines are the same act unless at least two of
        # (what it does, where it touches, how the body moves, what it uses) differ.
        for other, theirs in mine_seen:
            check(sum(a != b for a, b in zip(mine, theirs)) >= 2, k + ' is a different act from ' + other + ' (two of effect/touch/body/tool/verb/object motion must differ)')
        mine_seen.append((k, mine))
        if R.REACH:
            check(bool(R.REACH.get(k)), k + ' is reachable by some age')
    check(far <= 4, oid + ' has at most four far (throw/shout/breath) acts')
    if need >= 12 and MIN is None and R.REACH and oid not in incomplete:
        for a in AGES:
            n = sum(a in R.REACH.get(k, ()) for k in keys)
            floor = -(-need * (2 if a == 'adult' else 1) // 3)
            check(n >= floor, oid + f' gives {a} {n} reachable routines (floor {floor})')

# ---------------------------------------------------------------- native runs
t = host.DesktopInput()
g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer)
t.game = g
g.renderer.game = g
g.renderer.present = lambda lines: None
WT = {'wet': WeatherType.RAINY, 'snow': WeatherType.SNOWY, 'storm': WeatherType.STORMY, 'rainbow_sky': WeatherType.RAINBOW, 'windy': WeatherType.WINDY}
SEASON = {'spring': Season.SPRING, 'summer': Season.SUMMER, 'fall': Season.FALL, 'winter': Season.WINTER}
SEA = set(K.SEA)
try:
    g._running = True
    g._start_new_game()
    g._flush_pending_save()
    g._state = 'playing'
    g.renderer._show_talk = False
    g.renderer._viewport_width, g.renderer._viewport_height = 132, 42
    g.renderer._update_camera(132, 42)  # visitors walk in viewport coordinates
    g.renderer._show_talk = False
    sound_engine.enabled = False
    p = g.living_pond
    p.state['auto'] = False
    p.minds.model.state['next_social'] = 1e9
    serial = [0]

    def conditions(weather='sunny', hour=12, season='spring', temperature=15, wind=.2, age='adult', energy=95, social=95, fun=95):
        g.day_night.get_current_hour = lambda: int(hour)
        g.day_night.get_current_minute = lambda: 0
        g.atmosphere.current_season = SEASON[season]
        g.atmosphere.current_weather = Weather(WT.get(weather, WeatherType.SUNNY), .7, 1, datetime.now().isoformat())
        g.duck.growth_stage = age
        g.duck.needs.energy, g.duck.needs.hunger, g.duck.needs.social, g.duck.needs.fun, g.duck.needs.cleanliness = energy, 95, social, fun, 95
        g.duck_store.sync_from_duck(g.duck)
        p.sync()
        p.state['ecology'].update(temperature=temperature, wind=wind)

    def reset():
        p.cancel()
        p.state['cooldowns'] = {}
        for o in [*p.state['instances'].values(), *p.state['objects'].values()]:
            if isinstance(o, dict):
                o['last_use'] = -1e9
        g.duck.current_action = None
        g.behavior_ai.clear_action()
        g.habitat.owned_items, g.habitat.placed_items, g.habitat.stored_items, g.habitat.stored_placements = [], [], [], []
        g.building.structures = []
        for room in g.decorations.rooms.values():
            room.decorations = []
        # Disposable save: empty the bags between objects so capacity never refuses a grant.
        g.inventory.items.clear()
        g.materials.stacks.clear()
        p.state['grounds'] = {}
        pos = g.renderer.duck_pos
        pos.cancel_movement()
        pos.x, pos.y = 36, 21

    def give(oid):
        """Set up the object's real host; returns (host item, instance, state obj)."""
        reset()
        kind = (R.OBJECTS.get(oid) or R.QUEUE[oid]).get('host', 'placed')
        if kind == 'placed':
            # Each object stands outside through its own real system.
            from world.shop import get_item
            from world.decorations import DECORATIONS
            from world.building import BLUEPRINTS, Structure, StructureStatus
            from world.garden import PLANTS, PlantedPlant, GrowthStage
            g.building.structures = [s for s in g.building.structures if s.blueprint_id != oid]
            for room in g.decorations.rooms.values():
                room.decorations = [d for d in room.decorations if d.decoration_id != oid]
            if get_item(oid):
                g.habitat.owned_items = [oid]
                g.habitat.placed_items = [PlacedItem(oid, 10, 6)]
            elif oid in DECORATIONS:
                room = next(r for r in ('pond', 'garden') if not DECORATIONS[oid].allowed_rooms or r in [x.value for x in DECORATIONS[oid].allowed_rooms])
                g.decorations.rooms[room].unlocked = True
                g.decorations.owned_decorations[oid] = max(1, g.decorations.owned_decorations.get(oid, 0))
                ok, msg = g.decorations.place_decoration(oid, room, (2, 2))
                assert ok, oid + ': ' + msg
            elif oid in BLUEPRINTS:
                g.building.structures.append(Structure(oid, (1, 1), StructureStatus.COMPLETE))  # (4,3) collides with the nest
            elif oid in PLANTS:
                plot = next(iter(g.garden.plots.values()))
                plot.is_unlocked = True
                plot.plant = PlantedPlant(oid, plot.plot_id, '2026-05-01T08:00:00', '2026-05-01T08:00:00', GrowthStage.FLOWERING)
            p.sync()
            found = R.host_of(p, oid) if oid in R.OBJECTS else _probe_host(oid, kind)
            assert found, oid + ' stands outside through its real system'
            return oid, found[1]
        if kind == 'keeping':
            hostitem = 'infinity_pool' if oid in SEA else 'koi_pond'
            g.habitat.owned_items = [hostitem]
            g.habitat.placed_items = [PlacedItem(hostitem, 10, 6)]
            p.sync()
            iid = next(x.instance for x in p.placements if x.item_id == hostitem)
            serial[0] += 1
            c = CaughtFish(oid, 30. if oid not in SEA else 200., (datetime(2026, 1, 1) + timedelta(minutes=serial[0])).isoformat(), FishingSpot.POND, BaitType.BREAD, False)
            g.fishing.fish_caught.setdefault(oid, []).append(c)
            if hostitem != 'koi_pond':
                K.setup(p, hostitem, iid, True)
            ok, msg = K.keep(p, hostitem, iid, oid, c.caught_at)
            assert ok, msg
            return hostitem, iid
        if kind == 'display':
            own(oid)
            g.habitat.owned_items = ['trophy_case']
            g.habitat.placed_items = [PlacedItem('trophy_case', 10, 6)]
            p.sync()
            iid = next(x.instance for x in p.placements if x.item_id == 'trophy_case')
            from engine import display
            ok, msg = display.show(p, 'trophy_case', iid, oid, R.displayable())
            assert ok, msg
            return 'trophy_case', iid
        if kind == 'wearable':
            if oid not in g.outfits.owned_items:
                g.outfits.owned_items.append(oid)
            g.outfits.current_outfit.neck = oid  # worn on the body, as these routines require
            p.sync()
            return oid, None
        if kind == 'portable':
            own(oid)
            p.sync()
            return oid, None
        raise AssertionError('unknown host ' + kind)

    def _probe_host(oid, kind):
        """host_of for an object with no repertoire file yet."""
        R.OBJECTS[oid] = dict(object=oid, host=kind, routines={}, effects={})
        try:
            return R.host_of(p, oid)
        finally:
            del R.OBJECTS[oid]

    def own(oid):
        from engine.item_profiles import ITEMS
        src = ITEMS[oid]['sources'][0].split('.')[0] if ITEMS.get(oid, {}).get('sources') else 'items'
        from world.decorations import DECORATIONS
        from world.garden import SEEDS
        from world.materials import MATERIALS
        if src == 'crafting':
            if oid in MATERIALS:
                g.materials.add_material(oid, 1)
            else:
                g.crafting._add_tool(oid, oid.replace('_', ' ').title())
        elif oid in SEEDS and src == 'garden':
            g.garden.seed_inventory[oid] = max(1, g.garden.seed_inventory.get(oid, 0))
        elif oid in DECORATIONS and src == 'decorations':
            g.decorations.owned_decorations[oid] = max(1, g.decorations.owned_decorations.get(oid, 0))
        elif src == 'materials':
            g.materials.add_material(oid, 1)
        elif src == 'treasure':
            from world.treasure import FoundTreasure, TreasureLocation
            g.treasure.found_treasures[oid] = [FoundTreasure(oid, datetime.now().isoformat(), TreasureLocation.BEACH)]
        elif src == 'collectibles':
            g.collectibles.collect(oid, 'test')
        else:
            g.inventory.add_item(oid)

    def setup_for(key, hostitem, iid, age):
        r = R.ROUTINES[key]
        oid = r['object']
        fields = R.OBJECTS[oid].get('fields', {})
        s = R.state(oid, R.store(p, {'target': hostitem, 'instance': iid}, {'object': oid}) if R.OBJECTS[oid].get('host') == 'wearable' else p.object_state(hostitem, iid))
        env = dict(weather='sunny', hour=12, season='spring', temperature=15, wind=.2, age=age, energy=95, social=95, fun=95)
        for token in r['when']:
            neg = token.startswith('!')
            name = token.lstrip('!')
            m = W.COMPARE.match(name)
            if m:
                f, op, v = m.group(1), m.group(2), float(m.group(3))
                up = (op in ('>', '>=')) != neg
                if f.startswith('obj_'):
                    real = R.store(p, {'target': hostitem, 'instance': iid}, {'object': oid}) if R.OBJECTS[oid].get('host') == 'wearable' else p.object_state(hostitem, iid)
                    real[f[4:]] = min(1., v + .15) if up else max(0., v - .15)
                    continue
                if f.startswith('pond_') or f.startswith('fish_'):
                    k = K.state(p.object_state(hostitem, iid))
                    targets = [k] if f.startswith('pond_') else [x for x in k['fish'] if x['species'] == oid]
                    for tgt in targets:
                        tgt[f[5:]] = min(1., v + .15) if up else max(0., v - .15)
                    continue
                lo, hi = fields[f][1], fields[f][2]
                s[f] = min(hi, v + .15) if up else max(lo, v - .15)
                if hi - lo >= 2 and float(v).is_integer():
                    s[f] = v + (1 if up else -1)
            elif name in W.FLAGS:
                s[W.FLAGS[name][0]] = 0. if neg else 1.
            elif neg:
                if name in ('wet', 'snow', 'storm'):
                    env['weather'] = 'sunny'
                elif name == 'night_late':
                    env['hour'] = 12
            elif name in ('wet', 'snow', 'storm', 'rainbow_sky', 'windy'):
                env['weather'] = name
                env['temperature'] = -3 if name == 'snow' else env['temperature']
                env['wind'] = .8 if name in ('windy', 'storm') else env['wind']
            elif name == 'calm':
                env['wind'] = .1
            elif name == 'cold':
                env['temperature'] = -3
            elif name == 'warm':
                env['temperature'] = 18
            elif name in ('night', 'night_late'):
                env['hour'] = 23
            elif name == 'dawn':
                env['hour'] = 6
            elif name == 'dusk':
                env['hour'] = 18
            elif name in ('day', 'dawn_or_day'):
                env['hour'] = 12
            elif name in SEASON:
                env['season'] = name
            elif name == 'tired':
                env['energy'] = 30
            elif name == 'lonely':
                env['social'] = 30
            elif name == 'sad':
                env['fun'] = 25
        conditions(**env)
        return env

    def possessions():
        return copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency))

    applied = []
    original_apply = R.apply

    def recording(s, oid, rows, pond=None, subject=None, host=None, objstate=None):
        for name, authored in R.OBJECTS[oid]['effects'].items():
            if rows is authored:
                plan = p.state.get('plan') or {}
                pos = g.renderer.duck_pos
                dest = plan.get('destination', [pos.x, pos.y])
                applied.append(dict(name=name, near=abs(pos.x - dest[0]) + abs(pos.y - dest[1]) <= 3, phase=plan.get('phase')))
        return original_apply(s, oid, rows, pond, subject, host, objstate)
    R.apply = recording
    runs = 0
    if '--hosts' in args:
        # Every object in the work queue can really be set up and found as a host.
        hosted, failed = [], []
        for oid in sorted(only or R.QUEUE):
            kind = R.QUEUE[oid]['host']
            if kind == 'portable' or kind == 'wearable' or kind == 'display':
                pass
            try:
                give(oid)
                found = R.host_of(p, oid) if oid in R.OBJECTS else _probe_host(oid, kind)
            except (AssertionError, StopIteration, KeyError) as e:
                found, why = None, repr(e)[:80]
            else:
                why = ''
            if found:
                hosted.append(oid)
            else:
                failed.append(oid + ':' + kind + ':' + (R.QUEUE[oid]['sources'][0]) + ':' + why)
        check(not failed, 'every object can be set up through its real system and found: ' + ' | '.join(failed))
        print(json.dumps(dict(result='PASS', hosts=len(hosted), checks=len(checks), seconds=round(time.time() - started))))
        raise SystemExit(0)

    from world.friends import visitor_animator
    b = p.minds
    clock = [0.]
    joined = [False]
    pal = []

    def bring_friend():
        """A visiting friend arrives beside Cheese (a duet needs one)."""
        if not pal:
            pal.append(g.friends.generate_new_friend())
        friend = pal[0]
        g.friends.start_visit(friend.id)
        visitor_animator._friend_name = friend.name
        visitor_animator._is_leaving = False
        pos = g.renderer.duck_pos
        visitor_animator._position_x, visitor_animator._position_y = pos.x + 14, pos.y
        visitor_animator._last_move_time = clock[0]
        b.sync()
        b.model.residents[friend.id]['energy'] = .9
        b.tasks[friend.id] = dict(action='observe', until=b.now + 200, context=b.context(friend.id))
        joined[0] = False
        return friend.id

    def visitors_step(dt):
        clock[0] += dt
        pos = g.renderer.duck_pos
        if g.friends.current_visit:
            visitor_animator._mind_motion = b.motion(g.friends.current_visit.friend_id)
            visitor_animator.update(clock[0], pos.x, pos.y)
        b.tick()

    def send_friend_home():
        b.wonder_guests.clear()
        b.tasks.clear()
        b.wonder_retry.clear()  # a released friend is barred for a while; each test run starts fresh
        g.friends.current_visit = None

    def review_pick(oid, key, age):
        if '--review' in args:
            return key in args[args.index('--review') + 1].split(',') and age == ([a for a in AGES if a in R.REACH.get(key, AGES)] or ['adult'])[0]
        keys = R.by_object(oid)
        step = max(1, len(keys) // FRAMES)
        i = keys.index(key)
        return i % step == 0 and i // step < FRAMES and age == ([a for a in AGES if a in R.REACH.get(key, AGES)] or ['adult'])[0]

    def first_touch(key):
        r = R.ROUTINES[key]
        if '--frame-at' in args:
            return float(args[args.index('--frame-at') + 1])
        if r['events']:
            return r['events'][0][0]
        touching = [t for t, q in r['track'] if q.get('contact', 0) >= .5]
        return touching[0] if touching else .45

    duets = []
    for oid in objects:
        for key in R.by_object(oid):
            duet = bool(R.ROUTINES[key].get('duo'))
            ages = [a for a in AGES if a in R.REACH.get(key, AGES)] if R.REACH else list(AGES)
            if QUICK:
                ages = ages[:1]
            for age in ages:
                r = R.ROUTINES[key]
                hostitem, iid = give(oid)
                env = setup_for(key, hostitem, iid, age)
                friend_key = bring_friend() if duet else None
                label = key + '@' + age
                obj = R.store(p, {'target': hostitem, 'instance': iid}, {'object': oid}) if R.OBJECTS[oid].get('host') == 'wearable' else p.object_state(hostitem, iid)
                check(key in R.eligible(p, oid, obj), label + ' eligible in its authored context ' + json.dumps(env))
                before = possessions()
                seq = p.state['sequence']
                applied.clear()
                ok, msg = R.request(p, oid, key, iid)
                check(ok, label + ' starts: ' + msg)
                plan = p.state['plan']
                check(plan.get('rep_work', {}).get('id') == key, label + ' runs exactly the requested routine')
                p._activity(.5)
                check(not applied, label + ' nothing happens before arrival')
                for _ in range(5000):
                    if not p.state['plan']:
                        break
                    p.state['elapsed'] += .2
                    pos = g.renderer.duck_pos
                    pos._state_start_time -= .2
                    pos.update(.2)
                    p._activity(.2)
                    if duet:
                        visitors_step(.2)
                        gr = b.wonder_guests.get(friend_key)
                        joined[0] = joined[0] or bool(gr and gr.get('duet') and gr['phase'] == 'inside' and (p.state['plan'] or {}).get('rep_work', {}).get('elapsed', 0) > 0)
                    if _ % 5 == 0:
                        p.sync()  # the real loop syncs every second
                    pw = (p.state['plan'] or {}).get('rep_work') or {}
                    if FRAMES and review_pick(oid, key, age) and not pw.get('_captured') and pw.get('elapsed', 0) >= R.ROUTINES[key]['duration'] * first_touch(key):
                        from engine.scene import snapshot
                        sc = snapshot(g, g.renderer)
                        sc['review'] = key + '@' + age
                        sc['camera'] = {'x': 0, 'y': 0, 'w': 132, 'h': 42}  # the harness never runs the render loop that moves the camera
                        frames_out.append(sc)
                        pw['_captured'] = True
                else:
                    raise AssertionError(label + ' never finished')
                work = plan['rep_work']
                if duet:
                    check(joined[0], label + ' the friend walked over and did their own part')
                    duets.append(key)
                    send_friend_home()
                check(work['done'] and not work.get('interrupted') and work.get('recorded'), label + ' completes once')
                check([a['name'] for a in applied] == [n for _, n in r['events']], label + ' exact contacts in order')
                check(all(a['near'] and a['phase'] == 'act' for a in applied), label + ' contacts at the object during the act')
                check(sum(j['id'] > seq and j['kind'] == 'repertoire' for j in p.state['journal']) == 1, label + ' remembered once')
                check(possessions() == before, label + ' no items or coins')
                saved = copy.deepcopy(obj)
                R.complete(p, plan)
                check(obj == saved, label + ' completion replay changes nothing')
                runs += 1
        # Autonomous choice rotates: repeated picks in one context reach every eligible routine.
        hostitem, iid = give(oid)
        obj = R.store(p, {'target': hostitem, 'instance': iid}, {'object': oid}) if R.OBJECTS[oid].get('host') == 'wearable' else p.object_state(hostitem, iid)
        pool = set(R.eligible(p, oid, obj))
        saved_hist = dict(R.state(oid, obj)['history'])
        picked = set()
        for _ in range(4 * len(pool) + 4):
            choice = R.best(p, oid, obj)
            if not choice:
                break
            picked.add(choice[0])
            hist = R.state(oid, obj)['history']  # state() rebuilds the dict: always fetch it fresh
            hist[choice[0]] = hist.get(choice[0], 0) + 1
        R.state(oid, obj)['history'] = saved_hist
        check(picked == pool, oid + f' autonomous picks rotate through all {len(pool)} eligible routines (missed {sorted(pool - picked)})')
    R.apply = original_apply
    if FRAMES:
        (ROOT / 'engine/artifacts/animation-milestone').mkdir(parents=True, exist_ok=True)
        (ROOT / 'engine/artifacts/animation-milestone/rep-frames.json').write_text(json.dumps(frames_out))
    print(json.dumps(dict(result='PASS', incomplete=incomplete, duet_runs=len(duets), objects=len(objects), routines=sum(len(R.by_object(o)) for o in objects), runs=runs, checks=len(checks), seconds=round(time.time() - started))))
finally:
    g.living_pond.minds.close()
    g._save_executor.shutdown(wait=True)
    sound_engine.shutdown()
