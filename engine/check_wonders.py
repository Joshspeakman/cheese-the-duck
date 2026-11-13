"""Wonder machines: every routine end to end in the real game, plus physics,
context choice, ages, storms, interruption and save/reload.

Disposable saves only (CHEESE_SAVE_DIR is a fresh temp directory). Writes
engine/artifacts/animation-milestone/wonder-native.json and wonder-frames.json.
"""
import os, sys, tempfile, json, copy, subprocess, time
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-wonders-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, wonders as W
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine
sys.stdout = host.WIRE
checks = []
frames = []
started = time.time()
QUICK = '--quick' in sys.argv


def check(ok, label):
    assert ok, label
    checks.append(label)


# ---------------------------------------------------------------- static data contract
KNOWN = set(W.FLAGS) | {'dry_axle', 'far_year', 'young', 'grown', 'elder', 'tired', 'lonely', 'sad', 'happy', 'grumpy', 'curious'}
world_probe = W.World.__new__(W.World)
world_probe.weather, world_probe.wet, world_probe.temperature, world_probe.wind, world_probe.hour, world_probe.season, world_probe.outdoors = 'sunny', False, 15, .1, 12, 'spring', True


def known(token):
    token = token.lstrip('!')
    m = W.COMPARE.match(token)
    if m:
        return 'field', m.group(1)
    if token in KNOWN:
        return 'tag', token
    return ('world', token) if world_probe.tag(token) is not None else (None, token)


for item, spec in W.ITEMS.items():
    for field, op, value, when in spec['physics']:
        check(field in spec['fields'] and op in ('rate', 'decay', 'wrap'), item + ' physics row names a real field')
        for t in when.split('&'):
            kind, name = known(t)
            check(kind in ('world', 'field') or name in W.FLAGS or name in ('dry_axle',), item + ' physics condition ' + t + ' is understood')
            if kind == 'field':
                check(name in spec['fields'], item + ' physics compares its own field ' + name)
    for when, rows in spec['triggers']:
        for t in when.split('&'):
            kind, name = known(t)
            check(kind == 'field' and name in spec['fields'], item + ' trigger compares its own field')
    for name, rows in spec['effects'].items():
        check(all(r[0] in spec['fields'] and r[1] in ('set', 'add', 'mul', 'max', 'min', 'wrap') for r in rows), item + ' effect ' + name + ' writes its own bounded fields')
for key, r in W.ROUTINES.items():
    spec = W.ITEMS[r['item']]
    check(not r.get('say') or len(W.LINES.get(r['say'], [])) >= 2, key + ' has authored lines for its speech cue')
    for t in r['when'] + r['prefer']:
        kind, name = known(t)
        check(kind is not None, key + ' context tag ' + t + ' is understood')
        if kind == 'field':
            check(name in spec['fields'], key + ' compares its own object field ' + name)
    check(all(name in spec['effects'] for _, name in r['events']), key + ' events are authored contacts of its own object')
    check([e[0] for e in r['events']] == sorted(e[0] for e in r['events']) and all(0 < e[0] < 1 for e in r['events']), key + ' contacts happen in order inside the routine')
    times = [k[0] for k in r['track']]
    check(times == sorted(times) and times[0] == 0 and times[-1] == 1, key + ' track keyframes are ordered')
per_item = {i: len(W.BY_ITEM[i]) for i in W.ITEMS}
check(len(W.ITEMS) == 32 and all(n >= 4 for n in per_item.values()), 'all 32 wonders have at least four routines')
signatures = {}
for key, r in W.ROUTINES.items():
    parts = tuple(sorted({k for _, q in r['track'] for k in q if k not in ('x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor')}))
    trace = tuple((round(q.get('x', 0)), round(q.get('y', 0)), round(q.get('b', 0)), round(q.get('w', 0)), bool(q.get('contact'))) for _, q in r['track'])
    sig = (r['item'], tuple(name for _, name in r['events']), tuple(sorted({k[1].get('anchor') for k in r['track'] if k[1].get('anchor')})), r['tool'], parts, trace)
    check(sig not in signatures, key + ' differs physically from ' + str(signatures.get(sig)))
    signatures[sig] = key

# Native and renderer sample the same track for every animated object part.
payload = []
for key, r in W.ROUTINES.items():
    parts = sorted({k for _, p in r['track'] for k in p if k not in ('x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor')})
    for i in range(0, 41):
        payload.append(dict(id=key, elapsed=r['duration'] * i / 40, parts=parts))
script = ("import {wonderPose} from './engine/client/wonder-routines.mjs';let s='';for await(const c of process.stdin)s+=c;"
          "console.log(JSON.stringify(JSON.parse(s).map(c=>{const p=wonderPose(c);return c.parts.map(k=>p.object[k]).concat([p.contact])})))")
render = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', script], input=json.dumps(payload).encode(), cwd=ROOT))
agree = all(abs(a - W.pose_value(c, k)) < 1e-9 for vals, c in zip(render, payload) for a, k in zip(vals, c['parts'] + ['contact']))
check(agree, str(len(payload)) + ' native and rendered object-part samples agree')

bad = {'wonder': {'melt': float('nan'), 'detail': float('inf'), 'puddle': -4, 'bogus': 3, 'history': {'ice_polish': 2, 'nope': 1}}}
s = W.state('ice_sculpture', bad)
check(s['melt'] == 0 and s['detail'] == .7 and s['puddle'] == 0 and 'bogus' not in s and s['history'] == {'ice_polish': 2}, 'damaged saved wonder state is bounded and cleaned')

# ---------------------------------------------------------------- live game fixture
t = host.DesktopInput()
g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer)
t.game = g
g.renderer.game = g
g.renderer.present = lambda lines: None
AGES = ('hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary')
WT = {'wet': WeatherType.RAINY, 'snow': WeatherType.SNOWY, 'storm': WeatherType.STORMY, 'rainbow_sky': WeatherType.RAINBOW, 'windy': WeatherType.WINDY}
SEASON = {'spring': Season.SPRING, 'summer': Season.SUMMER, 'fall': Season.FALL, 'winter': Season.WINTER}
try:
    g._running = True
    g._start_new_game()
    g._flush_pending_save()
    g._state = 'playing'
    g.renderer._show_talk = False
    sound_engine.enabled = False
    g.renderer._viewport_width = 132
    g.renderer._viewport_height = 42
    g.renderer._update_camera(132, 42)
    p = g.living_pond
    p.state['auto'] = False
    p.minds.model.state['next_social'] = 1e9

    def conditions(weather='sunny', hour=12, season='spring', temperature=15, wind=.2, age='adult', energy=95, social=95, fun=95):
        g.day_night.get_current_hour = lambda: int(hour)
        g.day_night.get_current_minute = lambda: int((hour % 1) * 60)
        g.atmosphere.current_season = SEASON[season]
        g.atmosphere.current_weather = Weather(WT.get(weather, WeatherType.SUNNY), .7, 1, datetime.now().isoformat())
        g.duck.growth_stage = age
        g.duck.needs.energy, g.duck.needs.hunger, g.duck.needs.social, g.duck.needs.fun, g.duck.needs.cleanliness = energy, 95, social, fun, 95
        g.duck_store.sync_from_duck(g.duck)
        p.sync()
        p.state['ecology'].update(temperature=temperature, wind=wind)

    def own(item):
        p.cancel()
        g.duck.current_action = None
        g.behavior_ai.clear_action()
        g.habitat.owned_items = [item]
        g.habitat.placed_items = [PlacedItem(item, 10, 6)]
        g.habitat.stored_items = []
        g.habitat.stored_placements = []
        g.building.structures = []
        for room in g.decorations.rooms.values():
            room.decorations = []
        p.sync()
        p.state['cooldowns'] = {}
        p._cache = None
        pos = g.renderer.duck_pos
        pos.cancel_movement()
        pos.x, pos.y = 36, 21
        placed = next(x for x in p.placements if x.item_id == item)
        return placed.instance, p.object_state(item, placed.instance)

    def possessions():
        return copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency, g.treasure.to_dict()))

    def step(capture=None):
        p.state['elapsed'] += .2
        pos = g.renderer.duck_pos
        pos._state_start_time -= .2
        pos.update(.2)
        p._activity(.2)
        if capture:
            frames.append(capture())

    def setup_for(key, iid, obj, age=None):
        """Choose real weather/time/season/age/needs and object state that make
        exactly this routine's conditions hold, then verify via eligible()."""
        r = W.ROUTINES[key]
        env = dict(weather='sunny', hour=12, season='spring', temperature=15, wind=.2, age='adult', energy=95, social=95, fun=95)
        reach = [a for a in AGES if a in W.REACH[key]]
        env['age'] = age or ('adult' if 'adult' in reach else reach[0])
        s = W.state(r['item'], obj)
        spec = W.ITEMS[r['item']]['fields']
        for token in r['when']:
            neg = token.startswith('!')
            name = token.lstrip('!')
            m = W.COMPARE.match(name)
            if m:
                field, op, value = m.group(1), m.group(2), float(m.group(3))
                lo, hi = spec[field][1], spec[field][2]
                up = (op in ('>', '>=')) != neg
                s[field] = min(hi, value + .15) if up else max(lo, value - .15)
                if spec[field][2] - spec[field][1] >= 2 and float(value).is_integer():
                    s[field] = value + (1 if up else -1)
            elif name in W.FLAGS:
                field, threshold = W.FLAGS[name]
                s[field] = 0. if neg else 1.
            elif name == 'far_year':
                s['year'] = 2026 if neg else 1885
            elif name == 'dry_axle':
                s['oil'] = .6 if neg else .1
            elif neg:
                if name in ('wet', 'snow', 'storm'):
                    env['weather'] = 'sunny'
                elif name == 'night_late':
                    env['hour'] = min(env['hour'], 21) if env['hour'] >= 5 else 12
            elif name in ('wet', 'snow', 'storm', 'rainbow_sky', 'windy'):
                env['weather'] = name
                if name == 'snow':
                    env['temperature'] = -3
                if name in ('windy', 'storm'):
                    env['wind'] = .8
            elif name in ('dry', 'clear', 'sun', 'calm'):
                env['wind'] = .1 if name == 'calm' else env['wind']
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
            elif name == 'young' and not age:
                env['age'] = next(a for a in reach if a in W.YOUNG)
            elif name == 'elder' and not age:
                env['age'] = next(a for a in reach if a in W.ELDER)
            elif name == 'tired':
                env['energy'] = 30
            elif name == 'lonely':
                env['social'] = 30
            elif name == 'sad':
                env['fun'] = 25
        conditions(**env)
        return env

    # ------------------------------------------------------------ every routine, end to end
    events_seen = []
    original_apply = W.apply

    def recording_apply(s, item, rows):
        for name, authored in W.ITEMS[item]['effects'].items():
            if rows is authored:
                plan = p.state.get('plan') or {}
                pos = g.renderer.duck_pos
                dest = plan.get('destination', [pos.x, pos.y])
                events_seen.append(dict(item=item, name=name, phase=plan.get('phase'), near=abs(pos.x - dest[0]) + abs(pos.y - dest[1]) <= 3))
        return original_apply(s, item, rows)
    W.apply = recording_apply
    review = {'topiary_rain_tuck', 'ice_chisel_feathers', 'sand_tower_raise', 'gong_mighty_bong', 'aurora_lie_and_watch', 'volcano_baking_soda', 'portal_peek_through',
              'time_pull_lever', 'field_rain_shelter', 'robot_high_five', 'dragon_brood', 'zen_rake_spiral', 'booth_storm_hideout', 'cloak_hide_under'}
    keys = list(W.ROUTINES) if not QUICK else [k for k in W.ROUTINES if k in review]
    runs = [(k, a) for k in keys for a in AGES if a in W.REACH[k]] if not QUICK else [(k, None) for k in keys]
    for key, age in runs:
        r = W.ROUTINES[key]
        item = r['item']
        iid, obj = own(item)
        env = setup_for(key, iid, obj, age)
        key_age = key + '@' + env['age']
        check(key in W.eligible(p, item, obj), key_age + ' is eligible in its authored context ' + json.dumps(env))
        before = possessions()
        journal = p.state['sequence']
        history = obj['wonder']['history'].get(key, 0)
        events_seen.clear()
        chat_before = g.renderer.chat.sequence
        ok, msg = W.request(p, item, key, iid)
        check(ok, key_age + ' starts on request: ' + msg)
        plan = p.state['plan']
        check(plan['wonder_work']['id'] == key and plan['label'] == r['label'], key_age + ' runs exactly the requested routine')
        p._activity(.5)
        check(plan['phase'] != 'act' and plan['wonder_work']['elapsed'] == 0 and not events_seen, key_age + ' does nothing before Cheese arrives')
        captured = False
        for n in range(4000):
            if not p.state['plan']:
                break
            cap = None
            if key in review and not captured and (age is None or age == 'adult' or (age == 'hatchling' and 'hatchling' in W.REACH[key])) and plan['wonder_work']['elapsed'] >= r['duration'] * .42:
                captured = True

                def cap(key=key):
                    sc = snapshot(g, g.renderer)
                    sc['review'] = key + ('-' + env['age'] if env['age'] != 'adult' else '')
                    return sc
            step(cap)
        else:
            raise AssertionError(key_age + ' never finished')
        work = plan['wonder_work']
        names = [e['name'] for e in events_seen]
        check(work['done'] and not work.get('interrupted') and work.get('recorded'), key_age + ' completes once: ' + json.dumps(work))
        check(names == [n for _, n in r['events']], key_age + ' applied exactly its authored contacts in order: ' + str(names))
        check(all(e['near'] and e['phase'] == 'act' for e in events_seen), key_age + ' every contact happened at the object during the act')
        check(obj['wonder']['history'].get(key, 0) == history + 1, key_age + ' records one completed sequence')
        check(sum(j['id'] > journal and j['kind'] == 'wonder' and j['text'].startswith(r['label']) for j in p.state['journal']) == 1, key_age + ' Cheese remembers doing it, once')
        check(possessions() == before, key_age + ' grants no items, coins or treasure')
        if r.get('say'):
            said = [e for e in g.renderer.chat.entries if e['id'] > chat_before and e['speaker'] == 'cheese' and e['channel'] == 'say' and e['text'] in W.LINES[r['say']]]
            check(work.get('said') and len(said) == 1, key_age + ' Cheese says one authored line for it in the chat log')
        saved = copy.deepcopy(obj)
        W.complete(p, plan)
        check(obj == saved, key_age + ' completion replay changes nothing')
    W.apply = original_apply

    # ------------------------------------------------------------ physics on real saved state
    def fresh(item):
        o = {}
        W.state(item, o)
        return o
    o = fresh('ice_sculpture')
    conditions(hour=13, temperature=22)
    W.update(p, 'ice_sculpture', o, 600, True, False, 22, .1, 'sunny')
    check(.1 < o['wonder']['melt'] < .3, 'ten minutes of warm sun softens the ice without destroying it')
    W.update(p, 'ice_sculpture', o, 3600, True, False, 22, .1, 'sunny')
    check(o['wonder']['melt'] > .9 and o['wonder']['puddle'] > .3, 'an hour of warm sun melts the swan into a puddle')
    melt = o['wonder']['melt']
    W.update(p, 'ice_sculpture', o, 1200, True, False, -5, .1, 'snowy')
    check(o['wonder']['melt'] < melt and o['wonder']['puddle'] < .3 and o['wonder']['frost'] > .5, 'cold refreezes, freezes the puddle and frosts the ice')
    o = fresh('ice_sculpture')
    o['wonder']['tarp'] = 1
    W.update(p, 'ice_sculpture', o, 300, True, False, 22, .1, 'sunny')
    shaded = o['wonder']['melt']
    o2 = fresh('ice_sculpture')
    W.update(p, 'ice_sculpture', o2, 300, True, False, 22, .1, 'sunny')
    check(shaded < o2['wonder']['melt'] / 2, 'the canvas really slows melting')
    o = fresh('sand_castle')
    o['wonder']['towers'] = 4
    for _ in range(12):
        W.update(p, 'sand_castle', o, 60, True, True, 12, .2, 'rainy')
    check(o['wonder']['towers'] < 4, 'rain slumps the top towers')
    for _ in range(30):
        W.update(p, 'sand_castle', o, 60, True, True, 12, .2, 'rainy')
    check(o['wonder']['towers'] == 0 and o['wonder']['flag'] == 0, 'a long rain washes the castle flat')
    o = fresh('volcano')
    o['wonder']['pressure'] = .95
    for _ in range(4):
        W.update(p, 'volcano', o, 60, True, False, 15, .1, 'sunny')
    check(o['wonder']['eruptions'] == 1 and o['wonder']['pressure'] < .5, 'pressure erupts exactly once and resets')
    o = fresh('volcano')
    o['wonder']['pressure'] = .6
    W.update(p, 'volcano', o, 300, True, True, 10, .2, 'rainy')
    check(o['wonder']['pressure'] < .6, 'rain cools the volcano instead of building pressure')
    o = fresh('dream_catcher')
    conditions(hour=23)
    W.update(p, 'dream_catcher', o, 400, True, False, 10, .1, 'sunny')
    night = o['wonder']['dreams']
    conditions(hour=12)
    o2 = fresh('dream_catcher')
    W.update(p, 'dream_catcher', o2, 400, True, False, 15, .1, 'sunny')
    check(night > .5 and o2['wonder']['dreams'] == 0, 'dreams gather only at night')
    o = fresh('dragon_egg')
    for _ in range(20):
        o['wonder'].update(warmth=max(o['wonder']['warmth'], .9), embers=.9)  # tended: brooded and stoked each visit
        W.update(p, 'dragon_egg', o, 600, True, False, 15, .1, 'sunny')
    check(o['wonder']['incubation'] > .9, 'an egg kept warm and stoked incubates')
    o3 = fresh('dragon_egg')
    o3['wonder'].update(warmth=.9, embers=.9)
    for _ in range(20):
        W.update(p, 'dragon_egg', o3, 600, True, False, 15, .1, 'sunny')
    check(.05 < o3['wonder']['incubation'] < .3, 'left alone, its embers die and development stalls')
    o2 = fresh('dragon_egg')
    for _ in range(20):
        W.update(p, 'dragon_egg', o2, 600, True, False, -4, .1, 'snowy')
    check(o2['wonder']['incubation'] < .01 and o2['wonder']['warmth'] == 0, 'a neglected egg in the snow goes cold and does not develop')
    o = fresh('force_field')
    o['wonder'].update(shield=1, charge=.2)
    for _ in range(10):
        W.update(p, 'force_field', o, 60, True, True, 10, .3, 'rainy')
    check(o['wonder']['shield'] == 0, 'rain drains the dome until it drops')
    o = fresh('topiary_duck')
    conditions(season='summer')
    W.update(p, 'topiary_duck', o, 3600, True, True, 18, .2, 'rainy')
    check(.75 < o['wonder']['growth'] < .95, 'an hour of summer rain makes the hedge noticeably shaggier')
    W.update(p, 'topiary_duck', o, 7200, True, True, 18, .2, 'rainy')
    check(o['wonder']['growth'] == 1, 'left untrimmed through a rainy afternoon it is fully overgrown')
    for item in W.ITEMS:
        o = fresh(item)
        before = copy.deepcopy(o)
        W.update(p, item, o, 900, False, True, -5, .9, 'stormy')
        check(o == before, item + ' does not change while stored indoors')

    # ------------------------------------------------------------ context choice and ages
    iid, obj = own('force_field')
    obj['wonder'].update(shield=1, charge=.8)
    conditions(weather='wet')
    pick = W.best(p, 'force_field', obj)
    check(pick and pick[0] == 'field_rain_shelter' and 'dry spot' in pick[2], 'rain makes the raised dome a shelter: ' + str(pick))
    iid, obj = own('time_machine')
    conditions(weather='wet', age='duckling')
    check(W.best(p, 'time_machine', obj)[0] == 'time_rain_booth', 'a duckling ducks into the time booth in the rain')
    conditions(weather='wet', age='hatchling')
    check('time_rain_booth' not in W.eligible(p, 'time_machine', obj), 'a hatchling cannot reach the booth door, so it is not offered')
    iid, obj = own('force_field')
    obj['wonder'].update(shield=1, charge=.8)
    check(W.best(p, 'force_field', obj)[0] == 'field_rain_shelter', 'a hatchling sits under the raised dome in the rain instead')
    iid, obj = own('time_machine')
    iid, obj = own('topiary_duck')
    conditions(weather='wet', age='duckling', energy=30)
    check(W.best(p, 'topiary_duck', obj)[0] == 'topiary_rain_tuck', 'a tired duckling tucks under the hedge duck in the rain')
    iid, obj = own('tardis')
    conditions(weather='storm')
    check(W.eligible(p, 'tardis', obj) == ['booth_storm_hideout'], 'in a storm only the booth hideout remains for the booth')
    iid, obj = own('gong')
    conditions(weather='storm')
    check(W.eligible(p, 'gong', obj) == [] and not p.start('item', 'gong', instance=iid)[0], 'a storm keeps Cheese away from machinery without shelter')
    conditions()
    iid, obj = own('gong')
    for age in ('hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'):
        conditions(age=age)
        avail = W.eligible(p, 'gong', obj)
        check(('gong_mighty_bong' in avail) == (age not in ('hatchling', 'duckling')) and ('gong_cover_ears' in avail) == (age in ('duckling', 'juvenile')) and ('gong_peck_post' in avail) == (age in ('hatchling', 'duckling')), age + ' gets age-appropriate, reachable gong work: ' + str(avail))
    conditions(age='hatchling')
    ok, msg = W.request(p, 'gong', 'gong_mighty_bong', iid)
    check(not ok and 'little' in msg, 'a hatchling is told plainly why the big bong waits')
    g.duck.growth_stage = 'egg'
    check(not p.start('item', 'gong', instance=iid)[0], 'an egg does not walk over to a gong')
    iid, obj = own('aurora')
    obj['wonder']['power'] = 1
    conditions(hour=23, fun=25)
    check(W.best(p, 'aurora', obj)[0] == 'aurora_lie_and_watch', 'a low evening sends Cheese to lie and watch the lights')
    conditions(hour=12)
    check(W.best(p, 'aurora', obj)[0] == 'aurora_switch_off', 'in daylight he switches the aurora off')
    iid, obj = own('ice_sculpture')
    ok, msg = W.request(p, 'ice_sculpture', 'ice_frost_breath', iid)
    check(not ok and 'right now' in msg, 'an out-of-context request is explained, not faked')
    # Autonomous choice uses the wonder's own needs.
    iid, obj = own('volcano')
    obj['wonder']['pressure'] = .9
    obj['last_use'] = -1000
    conditions()
    p.state['auto'] = True
    p.state['next_decision'] = 0
    p.decide()
    plan = p.state['plan']
    check(any(c['target'] == 'volcano' for c in p.state['decision']) and (not plan or plan['target'] != 'volcano' or plan['wonder_work']['id'] in W.BY_ITEM['volcano']), 'Cheese considers a placed wonder on his own')
    p.state['auto'] = False
    p.cancel()

    # ------------------------------------------------------------ the real pond loop, several wonders placed
    p.cancel()
    group = ['ice_sculpture', 'volcano', 'force_field', 'topiary_duck', 'dream_catcher', 'gong', 'dragon_egg', 'sand_castle']
    g.habitat.owned_items = list(group)
    g.habitat.placed_items = [PlacedItem(item, 2 + (i % 4) * 4, 3 + (i // 4) * 5) for i, item in enumerate(group)]
    p.sync()
    placed = {x.item_id: x.instance for x in p.placements}
    check(set(placed) == set(group), 'eight wonders can be placed together: ' + str(sorted(placed)))
    for item in group:
        p.object_state(item, placed[item])['last_use'] = -1000
    p.state['auto'] = True
    p.state['next_decision'] = 0
    autonomous = {}
    seasons = [('spring', 'sunny', 18, 13), ('summer', 'wet', 20, 15), ('fall', 'windy', 10, 21), ('winter', 'snow', -4, 23)]
    for season, weather, temp, hour in seasons:
        conditions(weather=weather, hour=hour, season=season, temperature=temp)
        for n in range(900):
            p.state['ecology']['temperature'] = temp
            pos = g.renderer.duck_pos
            pos._state_start_time -= 2
            pos.update(2)
            p.advance(2)
            plan = p.state.get('plan')
            if plan and plan.get('wonder_work'):
                autonomous.setdefault(season, set()).add(plan['wonder_work']['id'])
        for item in group:
            ws = p.object_state(item, placed[item])['wonder']
            for f, (d, lo, hi) in W.ITEMS[item]['fields'].items():
                check(lo <= ws[f] <= hi and ws[f] == ws[f], season + ' ' + item + '.' + f + ' stays finite and bounded in the live loop')
    p.state['auto'] = False
    p.cancel()
    group_scene = snapshot(g, g.renderer)
    group_scene['review'] = 'group'
    check(sum(len(v) for v in autonomous.values()) >= 4 and len(autonomous) >= 3, 'Cheese chooses wonder routines on his own across the seasons: ' + json.dumps({k: sorted(v) for k, v in autonomous.items()}))
    ice = p.object_state('ice_sculpture', placed['ice_sculpture'])['wonder']
    check(ice['frost'] > .3, 'the winter hours in the real loop frosted the placed swan')
    conditions()
    before = p.state['sequence']
    p.command({'action': 'wonder_action', 'target': 'gong', 'text': 'gong_soft_tap', 'instance': placed['gong']})
    plan = p.state['plan']
    check(plan and plan['wonder_work']['id'] == 'gong_soft_tap', 'the journal command dispatches through the pond to the chosen routine')
    p.cancel()

    # ------------------------------------------------------------ interruption and save/reload
    iid, obj = own('gong')
    conditions()
    strikes = obj['wonder']['strikes']
    W.request(p, 'gong', 'gong_dinner_call', iid)
    p.cancel()
    check(obj['wonder']['strikes'] == strikes and not obj['wonder']['history'].get('gong_dinner_call'), 'cancelling before the first strike changes nothing')
    W.request(p, 'gong', 'gong_dinner_call', iid)
    plan = p.state['plan']
    for _ in range(2000):
        step()
        if plan['wonder_work']['events']:
            break
    check(obj['wonder']['strikes'] == strikes + 1 and not plan['wonder_work']['done'], 'the first strike lands at contact, before completion')
    facts = W.conversation(p, plan)
    check(facts['object'] == 'gong' and facts['state']['strikes'] == strikes + 1 and 'never grants' in facts['note'], 'chat gets the actual gong state mid-routine')
    facts['state']['strikes'] = 999
    check(obj['wonder']['strikes'] == strikes + 1, 'conversation facts are detached copies')
    before = copy.deepcopy(obj['wonder'])
    plan['paused'] = True
    clock = plan['wonder_work']['elapsed']
    p._activity(20)
    check(plan['wonder_work']['elapsed'] == clock and obj['wonder']['strikes'] == before['strikes'], 'pause holds the routine clock and contacts')
    g._save_game()
    g._flush_pending_save()
    g._load_game()
    p = g.living_pond
    p.sync()
    obj = p.object_state('gong', iid)
    check(obj['wonder']['strikes'] == strikes + 1 and p.state['plan'] and p.state['plan']['paused'], 'save and reload keep the struck gong and the paused routine')
    p.cancel()
    check(obj['wonder']['strikes'] == strikes + 1 and not obj['wonder']['history'].get('gong_dinner_call'), 'cancelling after contact keeps the physical strike without completion credit')
    iid, obj = own('volcano')
    conditions()
    obj['wonder']['ash'] = .6
    ok, _ = W.request(p, 'volcano', 'volcano_sweep_ash', iid)
    plan = p.state['plan']
    g.habitat.store_item('volcano', iid)
    p.sync()
    p._activity(1)
    check(p.state['plan'] is None, 'putting the wonder away cancels the pending routine')

    out = ROOT / 'engine/artifacts/animation-milestone'
    out.mkdir(parents=True, exist_ok=True)
    if not QUICK:
        (out / 'wonder-frames.json').write_text(json.dumps(frames))
        (out / 'wonder-group-scene.json').write_text(json.dumps(group_scene))
        (out / 'wonder-native.json').write_text(json.dumps(dict(result='PASS', routines=len(keys), routineAgeRuns=len(runs), checks=len(checks), frames=len(frames), seconds=round(time.time() - started), autonomousLiveLoop={k: sorted(v) for k, v in autonomous.items()}), indent=2))
    print(json.dumps(dict(result='PASS', routines=len(keys), routineAgeRuns=len(runs), checks=len(checks), frames=len(frames), seconds=round(time.time() - started), autonomous={k: sorted(v) for k, v in autonomous.items()})))
finally:
    g.living_pond.minds.close()
    g._save_executor.shutdown(wait=True)
    if getattr(g, '_talk_executor', None):
        g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
