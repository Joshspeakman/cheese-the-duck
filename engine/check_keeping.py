"""Keeping pond core: real catches only, each once; physical limits; physics;
journal commands; save/reload. Disposable saves only."""
import os, sys, tempfile, json, copy, subprocess
from pathlib import Path
from datetime import datetime, timedelta
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-keeping-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, keeping as K
from world.habitat import PlacedItem
from world.fishing import CaughtFish, FishingSpot, BaitType
from world.atmosphere import Weather, WeatherType, Season
from audio.sound import sound_engine
sys.stdout = host.WIRE
checks = []


def check(ok, label):
    assert ok, label
    checks.append(label)


bad = {'keeping': {'clarity': float('nan'), 'fish': [{'species': 'koi', 'catch': 'x', 'hunger': 9, 'size': -3}, {'species': 'swordfish', 'catch': 'y'}, 'junk']}}
k = K.state(bad)
check(k['clarity'] == .8 and len(k['fish']) == 1 and k['fish'][0]['hunger'] == 1 and k['fish'][0]['size'] == 1, 'damaged keeping state is bounded and cleaned')

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
    sound_engine.enabled = False
    p = g.living_pond
    p.state['auto'] = False
    g.day_night.get_current_hour = lambda: 12
    g.day_night.get_current_minute = lambda: 0
    g.atmosphere.current_season = Season.SPRING
    g.atmosphere.current_weather = Weather(WeatherType.SUNNY, .5, 1, datetime.now().isoformat())
    base = datetime(2026, 5, 1)
    def catch(species, size, n):
        c = CaughtFish(species, size, (base + timedelta(minutes=n)).isoformat(), FishingSpot.POND, BaitType.BREAD, False)
        g.fishing.fish_caught.setdefault(species, []).append(c)
        return c
    koi = catch('koi', 62., 1)
    carp = catch('carp', 48., 2)
    puffer = catch('pufferfish', 20., 3)
    minnows = [catch('minnow', 3., 10 + i) for i in range(3)]
    record_before = copy.deepcopy({k: [c.__dict__ for c in v] for k, v in g.fishing.fish_caught.items()})
    g.habitat.owned_items = ['koi_pond']
    g.habitat.placed_items = [PlacedItem('koi_pond', 10, 6)]
    p.sync()
    iid = next(x.instance for x in p.placements if x.item_id == 'koi_pond')
    obj = p.object_state('koi_pond', iid)
    possessions = copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency))
    p._cache = None
    view = p.view() if hasattr(p, 'view') else None
    offered = {(c['species'], c['catch']) for c in K.keepable(p)}
    check(('koi', koi.caught_at) in offered and ('pufferfish', puffer.caught_at) not in offered, 'only freshwater catches that fit are offered for keeping')

    def cmd(text):
        p.command({'action': 'keeping_action', 'target': 'koi_pond', 'instance': iid, 'text': text})
        return K.state(obj)
    k = cmd('keep:koi:' + koi.caught_at)
    check(len(k['fish']) == 1 and k['fish'][0]['species'] == 'koi' and k['fish'][0]['size'] == 62., 'the real 62 cm koi catch moves into the koi pond')
    k = cmd('keep:koi:' + koi.caught_at)
    check(len(k['fish']) == 1, 'the same catch cannot be kept twice')
    k = cmd('keep:koi:1999-01-01T00:00:00')
    check(len(k['fish']) == 1, 'an invented catch is refused')
    ok, msg = K.keep(p, 'koi_pond', iid, 'pufferfish', puffer.caught_at)
    check(not ok and 'salt water' in msg, 'a pufferfish is refused honestly: ' + msg)
    for m in minnows:
        cmd('keep:minnow:' + m.caught_at)
    k = cmd('keep:carp:' + carp.caught_at)
    check(len(k['fish']) == 5, 'carp and three minnows join')
    big = [catch('carp', 50., 20 + i) for i in range(5)]
    record_before = copy.deepcopy({k: [c.__dict__ for c in v] for k, v in g.fishing.fish_caught.items()})
    for c in big:
        cmd('keep:carp:' + c.caught_at)
    k = K.state(obj)
    check(K.used(k) <= K.HOSTS['koi_pond']['capacity'] and len(k['fish']) < 10, 'capacity stops an overcrowded pond: ' + str(round(K.used(k))) + ' cm')
    snap = p.snapshot() if hasattr(p, 'snapshot') else None

    # physics on real kept fish
    f = k['fish'][0]
    h0 = f['hunger']
    K.update(p, 'koi_pond', obj, 3600, True, False, 18, .2, 'sunny', 12, 'spring')
    check(f['hunger'] > h0 + .1, 'kept fish get hungry over an hour')
    k['flakes'] = 1.
    K.update(p, 'koi_pond', obj, 60, True, False, 18, .2, 'sunny', 12, 'spring')
    check(f['hunger'] < h0 + .1, 'floating flakes are actually eaten')
    for x in k['fish']:
        x['hunger'] = 1.
    k['clarity'] = .2
    hp = f['health']
    K.update(p, 'koi_pond', obj, 3600, True, False, 18, .2, 'sunny', 12, 'spring')
    check(f['health'] < hp, 'hungry fish in murky water lose health')
    K.update(p, 'koi_pond', obj, 3600, True, False, -4, .2, 'snowy', 2, 'winter')
    check(k['ice'] > .6, 'the koi pond ices over in the cold')
    K.update(p, 'koi_pond', obj, 3600, True, False, 12, .2, 'sunny', 12, 'fall')
    check(k['leaves'] > .1 and k['ice'] < .6, 'autumn leaves land and the ice melts again')

    # release, then never re-kept
    fid = next(x['id'] for x in k['fish'] if x['species'] == 'koi')
    fish_eco = p.state['ecology'].get('fish', .5)
    k = cmd('release:' + fid)
    check(all(x['id'] != fid for x in k['fish']) and p.state['kept_catches'][fid] == 'released' and p.state['ecology']['fish'] > fish_eco, 'releasing returns the koi to the wild pond')
    k = cmd('keep:koi:' + koi.caught_at)
    check(all(x['id'] != fid for x in k['fish']), 'a released fish cannot be kept again')
    check({k2: [c.__dict__ for c in v] for k2, v in g.fishing.fish_caught.items() if k2 in record_before} == record_before, 'the fishing record itself is never changed')
    check(copy.deepcopy((g.inventory.to_dict(), g.materials.get_all_materials(), g.habitat.currency)) == possessions, 'keeping grants no items or coins')

    # save and reload
    kept = copy.deepcopy(K.state(obj))
    g._save_game()
    g._flush_pending_save()
    g._load_game()
    p = g.living_pond
    p.sync()
    obj = p.object_state('koi_pond', iid)
    check(K.state(obj)['fish'] == kept['fish'] and p.state['kept_catches'][fid] == 'released', 'kept fish and the keeping ledger survive save and reload')

    # drawing the real fish
    fish = K.state(obj)['fish']
    script = ("import {itemSprite} from './engine/client/ultra-items.mjs';let s='';for await(const c of process.stdin)s+=c;const f=JSON.parse(s);"
              "const out=[12,23].map(hour=>{const m=itemSprite('koi_pond',3,{state:{keeping:{fish:f}},context:{hour,living:{ecology:{}}}});return {clipped:m.clipped,ascii:m.art.every(r=>/^[ -~]*$/.test(r)),fishGlyphs:m.art.join('').split('><').length-1+m.art.join('').split('<').length-1}});console.log(JSON.stringify(out))")
    drawn = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', script], input=json.dumps(fish).encode(), cwd=ROOT))
    check(all(not d['clipped'] and d['ascii'] and d['fishGlyphs'] >= len(fish) for d in drawn), 'every kept fish is drawn in the koi pond, day and night')
    print(json.dumps(dict(result='PASS', checks=len(checks), kept=len(fish))))
finally:
    g.living_pond.minds.close()
    g._save_executor.shutdown(wait=True)
    sound_engine.shutdown()
