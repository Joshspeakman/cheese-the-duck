"""Visitors at the wonders: real regular/rare/story arrivals joining Cheese, an idle
visitor working a free wonder (with egg Cheese watching), credit only on completion,
and no double booking with other company modules. Disposable saves only."""
import os, sys, tempfile, json, copy, random, re
from pathlib import Path
from datetime import datetime
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-wonder-company-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, wonders as W, wonder_company as company
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather, WeatherType, Season, VISITORS
from world.friends import visitor_animator
from audio.sound import sound_engine
sys.stdout = host.WIRE
random.seed(52)
checks, frames = [], []
clock = 0.


def check(ok, label):
    assert ok, label
    checks.append(label)


# No other company module may book a visitor who is busy at a wonder.
for f in sorted((ROOT / 'engine').glob('*.py')):
    text = f.read_text()
    if f.name != 'wonder_company.py' and re.search(r'key in (minds|self)\.readers', text) and 'wonder_guests' not in text:
        raise AssertionError(f.name + ' books visitors without excluding wonder guests')
check(True, 'every company module that excludes readers also excludes wonder guests')

t = host.DesktopInput()
g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer)
t.game = g
g.renderer.game = g
g.renderer.present = lambda lines: None
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
    b = p.minds
    p.state['auto'] = False
    b.model.state['next_social'] = 1e9
    g.day_night.get_current_hour = lambda: 12
    g.day_night.get_current_minute = lambda: 0
    g.atmosphere.current_season = Season.SPRING
    g.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
    friend = g.friends.generate_new_friend()

    def advance(n=1, capture=None):
        global clock
        for _ in range(n):
            clock += .1
            p.state['elapsed'] += .1
            pos = g.renderer.duck_pos
            pos._state_start_time -= .1
            pos.update(.1)
            p._activity(.1)
            if g.friends.current_visit:
                visitor_animator._mind_motion = b.motion(g.friends.current_visit.friend_id)
                visitor_animator.update(clock, pos.x, pos.y)
            g.guest_motion.tick(g, clock)
            g.story_motion.tick(g, clock)
            b.tick()
            if capture and capture():
                frames.append(snapshot(g, g.renderer))

    def place(item, stage='adult'):
        p.cancel()
        b.wonder_guests.clear()
        b.wonder_retry.clear()
        b.wonder_next = 0
        b.readers.clear()
        b.tasks.clear()
        b.housing.clear()
        g.friends.current_visit = None
        g.atmosphere.current_visitor = None
        p.state['story'] = None
        g.story_motion.actor = None
        g.guest_motion.actor = None
        g.duck.current_action = None
        g.behavior_ai.clear_action()
        g.duck.growth_stage = stage
        g.renderer.duck_pos.frozen = stage == 'egg'  # as host.py does every frame
        g.duck.needs.energy = g.duck.needs.hunger = 95
        g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items = [item]
        g.habitat.placed_items = [PlacedItem(item, 10, 6)]
        g.habitat.stored_items = []
        g.habitat.stored_placements = []
        pos = g.renderer.duck_pos
        pos.cancel_movement()
        pos.x, pos.y = 48, 21
        p.sync()
        p.state['ecology'].update(temperature=18, wind=.2)
        p.state['cooldowns'] = {}
        iid = next(a.instance for a in p.placements if a.item_id == item)
        return iid, p.object_state(item, iid)

    def bring(kind, near):
        start = [near[0] + 19, near[1]]
        if kind == 'regular':
            g.friends.start_visit(friend.id)
            visitor_animator._friend_name = friend.name
            visitor_animator._is_leaving = False
            visitor_animator._position_x, visitor_animator._position_y = start
            visitor_animator._last_move_time = clock
            key = friend.id
        elif kind == 'rare':
            key = 'friendly_goose'
            g.atmosphere.current_visitor = (VISITORS[key], datetime.now().isoformat())
            g.guest_motion.tick(g, clock)
            g.guest_motion.actor.update(x=start[0], y=start[1])
        else:
            key = 'story:pip'
            p.state['story'] = {'id': 'lost_duckling', 'step': 0, 'started': 0}
            g.story_motion.tick(g, clock)
            g.story_motion.actor.update(x=start[0], y=start[1])
        b.sync()
        b.model.residents[key]['energy'] = .9
        b.tasks[key] = dict(action='observe', until=b.now + 200, context=b.context(key))
        return key

    def bonds(key):
        return b.model.relationship('cheese', key)['familiarity'], b.model.relationship(key, 'cheese')['familiarity']

    # ------------------------------------------------------------ joining Cheese
    for kind, item, routine, stage in (('regular', 'gong', 'gong_dinner_call', 'adult'), ('rare', 'volcano', 'volcano_bleed_valve', 'adult'),
                                       ('story', 'zen_garden', 'zen_sit_breathe', 'duckling')):
        iid, obj = place(item, stage)
        if routine == 'volcano_bleed_valve':
            obj['wonder']['pressure'] = .8
        ok, msg = W.request(p, item, routine, iid)
        check(ok, kind + ' scene: Cheese starts ' + routine + ': ' + msg)
        plan = p.state['plan']
        key = bring(kind, plan['destination'])
        before = bonds(key)
        sequence = p.state['sequence']
        moved = []
        for _ in range(3000):
            advance(capture=lambda: kind == 'regular' and company.snapshot(b) and company.snapshot(b)[0]['phase'] == 'inside' and plan['wonder_work']['elapsed'] > 9 and len(frames) < 1)
            r = b.wonder_guests.get(key)
            if r and r['phase'] == 'approach':
                moved.append(list(b.present[key]))
            if not p.state['plan']:
                break
        check(len(moved) > 3 and moved[0] != moved[-1], kind + ' visitor walked over under their own movement')
        check(plan['wonder_work'].get('recorded'), kind + ' scene: Cheese completed his own routine')
        after = bonds(key)
        notes = [j for j in p.state['journal'] if j['id'] > sequence and j['kind'] == 'neighbors' and j['subject'] == key]
        check(after[0] > before[0] and after[1] > before[1] and len(notes) == 1, kind + ' visitor and Cheese bond once over a shared, completed routine: ' + str(notes))
        expected = company.style(b, key, routine)
        check(any(n['text'].startswith(b.model.residents[key]['name']) for n in notes) and obj.get('wonder_company', {}).get(expected) == 1, kind + ' visitor reacted in their own personality style: ' + expected)
        advance(30)
        check(key not in b.wonder_guests, kind + ' visitor is released after the routine')

    # A visitor also joins Cheese's generic repertoire routines (kept koi).
    from engine import repertoire as REP, keeping as KP
    from world.fishing import CaughtFish, FishingSpot, BaitType
    iid, obj = place('koi_pond')
    c = CaughtFish('koi', 44., '2026-05-02T09:00:00', FishingSpot.POND, BaitType.BREAD, False)
    g.fishing.fish_caught['koi'] = [c]
    ok, msg = KP.keep(p, 'koi_pond', iid, 'koi', c.caught_at)
    check(ok, 'a real koi catch is kept for the company test: ' + msg)
    ok, msg = REP.request(p, 'koi', 'koi_net_leaves', iid)
    check(ok, 'Cheese starts netting leaves on the koi pond: ' + msg)
    plan = p.state['plan']
    key = bring('regular', plan['destination'])
    before = bonds(key)
    sequence = p.state['sequence']
    joined = False
    for _ in range(3000):
        advance()
        r = b.wonder_guests.get(key)
        joined = joined or bool(r and r['key'] == 'rep_work' and r['phase'] == 'inside')
        if not p.state['plan']:
            break
    notes = [j for j in p.state['journal'] if j['id'] > sequence and j['kind'] == 'neighbors' and j['subject'] == key]
    check(joined and plan['rep_work'].get('recorded'), 'the visitor walked over and joined a repertoire routine')
    check(bonds(key)[0] > before[0] and len(notes) == 1, 'shared credit for a completed repertoire routine, once')

    # Cancel part way: no shared credit, physical contacts already made remain.
    iid, obj = place('gong')
    W.request(p, 'gong', 'gong_dinner_call', iid)
    plan = p.state['plan']
    key = bring('regular', plan['destination'])
    before = bonds(key)
    for _ in range(3000):
        advance()
        r = b.wonder_guests.get(key)
        if r and r['phase'] == 'inside' and plan['wonder_work']['events']:
            break
    strikes = obj['wonder']['strikes']
    p.cancel()
    advance(5)
    check(bonds(key) == before and key not in b.wonder_guests and obj['wonder']['strikes'] == strikes and strikes >= 1,
          'cancelling mid-routine keeps the strike but gives no shared credit and releases the visitor')

    # ------------------------------------------------------------ a visitor works a free wonder, egg Cheese watching
    iid, obj = place('gong', 'egg')
    check(not p.start('item', 'gong', instance=iid)[0], 'egg Cheese does not walk to the gong himself')
    advance(80)  # the game settles an egg in its nest spot before anything else happens
    settled = (g.renderer.duck_pos.x, g.renderer.duck_pos.y)
    egg_pos = (g.renderer.duck_pos.x, g.renderer.duck_pos.y, g.duck.facing if hasattr(g.duck, 'facing') else None)
    skills = copy.deepcopy(p.state['skills'])
    needs = (g.duck.needs.energy, g.duck.needs.fun, g.duck.needs.social)
    key = bring('regular', [30, 22])
    history = dict(obj['wonder']['history'])
    gong_before = {k: v for k, v in obj['wonder'].items() if k != 'history'}
    applied = []
    original_apply = W.apply
    W.apply = lambda s, item, rows: (applied.append((item, [r[0] for r in rows])), original_apply(s, item, rows))[1]
    sequence = p.state['sequence']
    seen_inside = False
    for _ in range(6000):
        advance(capture=lambda: (lambda s: bool(s) and s[0]['mode'] == 'operate' and s[0]['phase'] == 'inside' and s[0]['routine']['elapsed'] > 6 and len(frames) < 2)(company.snapshot(b)))
        r = b.wonder_guests.get(key)
        seen_inside = seen_inside or bool(r and r['phase'] == 'inside' and r['mode'] == 'operate')
        assert (g.renderer.duck_pos.x, g.renderer.duck_pos.y) == settled, 'egg moved during the visitor routine'
        if obj.get('wonder_visitors', {}).get(key):
            break
    check(seen_inside, 'an idle visitor volunteered and walked over to work the free gong')
    W.apply = original_apply
    done = list(obj.get('wonder_visitor_routines', {}))
    check(len(done) == 1 and obj['wonder_visitors'][key] == 1 and done[0] not in company.VISITOR_SKIP, 'the visitor completed one real routine on the gong: ' + str(done))
    check(obj['wonder']['history'] == history, "the visitor's run does not count as Cheese's own history")
    authored = [n for _, n in W.ROUTINES[done[0]]['events']]
    check(len([a for a in applied if a[0] == 'gong']) >= len(authored) and {k: v for k, v in obj['wonder'].items() if k != 'history'} != gong_before,
          'every authored contact of their routine was applied to the actual gong: ' + str(authored))
    egg_notes = [j for j in p.state['journal'] if j['id'] > sequence and j['kind'] == 'egg']
    check(len(egg_notes) == 1 and 'From inside the shell' in egg_notes[0]['text'], 'egg Cheese only gains a heard-it memory')
    now_pos = (g.renderer.duck_pos.x, g.renderer.duck_pos.y, g.duck.facing if hasattr(g.duck, 'facing') else None)
    changed_skills = {k: (skills.get(k), v) for k, v in p.state['skills'].items() if skills.get(k) != v}
    check(now_pos == egg_pos and not changed_skills, 'the egg never moved, turned or learned a skill from it: ' + json.dumps(dict(before=egg_pos, after=now_pos, skills=changed_skills)))
    vis = [j for j in p.state['journal'] if j['id'] > sequence and j['kind'] == 'neighbors' and j['subject'] == key]
    check(len(vis) == 1, 'the visitor remembers their own go at the wonder once')

    # A visitor also works a placed repertoire object (test fixture, three routines).
    from engine import repertoire as REP
    fx = json.loads((ROOT / 'engine/tests/fixtures/rep-tire-swing.json').read_text())
    REP.OBJECTS['tire_swing'] = fx
    for k2, r2 in fx['routines'].items():
        REP.ROUTINES[k2] = dict(r2, object='tire_swing')
        REP.REACH[k2] = ['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary']
    REP.BY_OBJECT['tire_swing'] = list(fx['routines'])
    iid, obj = place('tire_swing', 'egg')
    advance(80)
    needs = (g.duck.needs.energy, g.duck.needs.fun, g.duck.needs.social, g.duck.needs.cleanliness)
    key = bring('regular', [30, 22])
    rep_applied = []
    original_rep_apply = REP.apply
    REP.apply = lambda s2, oid, rows, *a, **kw: (rep_applied.append((oid, [r[0] for r in rows])), original_rep_apply(s2, oid, rows, *a, **kw))[1]
    seen_inside = False
    for _ in range(6000):
        advance()
        r = b.wonder_guests.get(key)
        seen_inside = seen_inside or bool(r and r['phase'] == 'inside' and r['mode'] == 'operate' and r.get('family') == 'rep')
        if obj.get('wonder_visitors', {}).get(key):
            break
    REP.apply = original_rep_apply
    done = list(obj.get('wonder_visitor_routines', {}))
    check(seen_inside and len(done) == 1 and done[0] in fx['routines'], 'a visitor walked over and worked a repertoire routine on the tyre swing: ' + str(done))
    authored = [n for _, n in fx['routines'][done[0]]['events']]
    check(len([x for x in rep_applied if x[0] == 'tire_swing']) >= len(authored), 'every authored contact landed on the real tyre swing: ' + str(authored))
    check((g.duck.needs.energy, g.duck.needs.fun, g.duck.needs.social, g.duck.needs.cleanliness) == needs or g.duck.growth_stage == 'egg',
          "the visitor's go never changes Cheese's needs")
    check(not any(row.startswith('need.') for _, rows in rep_applied for row in rows), 'visitor contacts carry no need rows')
    for k2 in fx['routines']:
        REP.ROUTINES.pop(k2, None)
        REP.REACH.pop(k2, None)
    REP.OBJECTS.pop('tire_swing', None)
    REP.BY_OBJECT.pop('tire_swing', None)

    # Cheese takes over a copy a visitor is working: the visitor steps aside.
    iid, obj = place('gong')
    key = bring('regular', [30, 22])
    for _ in range(4000):
        advance()
        r = b.wonder_guests.get(key)
        if r and r['mode'] == 'operate' and r['phase'] == 'inside':
            break
    check(r and r['phase'] == 'inside', 'visitor is working the gong')
    ok, _ = W.request(p, 'gong', 'gong_polish', iid)
    advance(3)
    check(ok and (key not in b.wonder_guests or b.wonder_guests[key]['mode'] == 'company'), 'when Cheese starts on that exact gong, the visitor stops operating it')

    out = ROOT / 'engine/artifacts/animation-milestone'
    (out / 'wonder-company-frames.json').write_text(json.dumps(frames))
    (out / 'wonder-company-native.json').write_text(json.dumps(dict(result='PASS', checks=len(checks), frames=len(frames)), indent=2))
    print(json.dumps(dict(result='PASS', checks=len(checks), frames=len(frames))))
finally:
    g.living_pond.minds.close()
    g._save_executor.shutdown(wait=True)
    if getattr(g, '_talk_executor', None):
        g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
