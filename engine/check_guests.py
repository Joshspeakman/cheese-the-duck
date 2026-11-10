"""Exercise named guests against the real game, using disposable saves only."""
import os
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-guests-check-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import copy
import json
import time
from datetime import datetime, timedelta
from unittest.mock import patch
from engine import host
from engine.guest_motion import GuestMotion
from engine.scene import snapshot
from world.guest_cast import PROFILES, guest_line
from world.atmosphere import VISITORS, VisitorFriendship
from world.friends import VisitorAnimator, DUCK_NAMES
from dialogue.visitor_dialogue import VisitorDialogueManager
sys.stdout = host.WIRE
checks = []
def check(value, label):
    assert value, label
    checks.append(label)

terminal = host.DesktopInput()
g = host.DesktopGame(terminal=terminal, renderer_factory=host.CanvasRenderer)
terminal.game = g; g.renderer.game = g; g.renderer.present = lambda lines: None
try:
    g._running = True; g._start_new_game(); g._flush_pending_save()
    g._state = 'playing'; g.duck.growth_stage = 'adult'; g.duck.current_action = None
    p = g.living_pond; p.state['auto'] = False
    check({n for names in DUCK_NAMES.values() for n in names} == {p['name'] for p in PROFILES.values() if not p['rare']}, 'all original friend names covered')
    g.renderer._viewport_width, g.renderer._viewport_height = 132, 42
    g.duck_store.set_need('social', 20); g.duck_store.sync_to_duck(g.duck)
    for profile in PROFILES.values():
        if profile['rare']: continue
        manager = VisitorDialogueManager()
        manager.start_visit(profile['archetype'], 'stranger', profile['name'], 1)
        check(guest_line(profile['id'], 'greeting', 'Cheese') in manager.get_next_dialogue('Cheese'), profile['name']+' authored greeting')
        lines = [manager.get_next_dialogue('Cheese') for _ in range(100)]
        check(not any(profile['voice']['personal'] in (line or '') for line in lines), profile['name']+' personal story remains friendship gated')
        manager.start_visit(profile['archetype'], 'friend', profile['name'], 2)
        check(profile['voice']['returning'] in manager.get_next_dialogue('Cheese'), profile['name']+' recognizes return visit')
        lines = [manager.get_next_dialogue('Cheese') for _ in range(150)]
        check(any(profile['voice']['personal'] in (line or '') for line in lines), profile['name']+' opens up to a friend')
        check(any(line and not any(v in line for v in profile['voice'].values()) for line in lines), profile['name']+' retains older dialogue tree')
    distances = []
    for name in ('Vasco', 'Amelia'):
        animator = VisitorAnimator(); animator.set_visitor('adventurous', name)
        start = animator._last_move_time
        for step in range(1, 11): animator.update(start+step*.2, 25, 4)
        distances.append(60-animator._position_x)
        check(all(isinstance(n, int) for n in animator.get_position()), name+' Classic coordinates remain integers')
        check(0 < distances[-1] < 10, name+' smooth bounded steps')
        animator._position_x = animator._target_x; animator._position_y = animator._target_y
        animator.update(start+3, 25, 4)
        check(animator._current_state == 'signature', name+' pauses for signature habit')
    check(distances[1] > distances[0], 'active pilot walks faster than leisurely traveler')

    check(set(VISITORS) == {p['id'] for p in PROFILES.values() if p['rare']}, 'every rare visitor has a named rig')
    out = ROOT/'engine/artifacts/guests'; out.mkdir(parents=True, exist_ok=True)
    fixtures = []
    for key, visitor in VISITORS.items():
        g.atmosphere.current_visitor = (visitor, datetime.now().isoformat())
        g.atmosphere.visitor_friendships[key] = VisitorFriendship(key, visit_count=1, friendship_points=2)
        motion = GuestMotion(); g.guest_motion = motion
        g.renderer.duck_pos.x, g.renderer.duck_pos.y = 65, 24
        states = set(); positions = set(); previous = None
        for i in range(1200):
            motion.tick(g, i*.1)
            actor = motion.snapshot(); states.add(actor['state']); positions.add((round(actor['x'],1),round(actor['y'],1)))
            if previous:
                check(abs(actor['x']-previous['x']) < 1 and abs(actor['y']-previous['y']) < 1, key+' bounded movement')
            previous = actor
        check(len(positions)>40 and {'walking','signature'}<=states, key+' wanders and performs habit')
        before = motion.snapshot(); g._state = 'menu'; motion.tick(g, 120)
        check(before == motion.snapshot(), key+' motion pauses in menus'); g._state='playing'
        frozen = motion.snapshot(); frozen['x'] = -900
        check(motion.snapshot()['x'] != -900, key+' snapshots do not expose mutable state')
        motion.tick(g, 120.1)
        p._guest_chat_at = -100; old = g.atmosphere.visitor_friendships[key].friendship_points
        inventory = copy.deepcopy(g.habitat.owned_items)
        p.command({'action':'guest_chat','target':'stale_guest'})
        check(g.atmosphere.visitor_friendships[key].friendship_points == old, key+' stale commands rejected')
        p.command({'action':'guest_chat','target':key})
        check(g.atmosphere.visitor_friendships[key].friendship_points == old+1, key+' chat reaches existing friendship ledger')
        p.command({'action':'guest_chat','target':key})
        check(g.atmosphere.visitor_friendships[key].friendship_points == old+1, key+' repeated click cooldown')
        motion.tick(g, 120.2)
        check(motion.snapshot()['state'] == 'signature', key+' reacts to attention')
        for action in ('guest_hobby','guest_company'):
            p._guest_chat_at = -100; p.command({'action':action,'target':key})
            check(p._guest_note['id']==key and p._guest_note['text'].startswith(visitor.name), key+' '+action)
        check(g.habitat.owned_items == inventory, key+' chat does not duplicate gifts')
        p._cache = None; frame = snapshot(g,g.renderer)
        check(frame['rareVisitor']['x']==motion.snapshot()['x'], key+' live motion reaches scene')
        check(frame['living']['rare_guest']['id']==key, key+' journal identifies active visitor')
        fixtures.append(frame)
        motion.reaction_until=0
        class DepartureClock(datetime):
            @classmethod
            def now(cls):
                return datetime.now()+timedelta(hours=visitor.stay_duration_hours,seconds=-3)
        with patch('engine.guest_motion.datetime', DepartureClock):
            motion.tick(g,121); motion.tick(g,121.2)
        check(motion.snapshot()['state']=='leaving', key+' departure walks toward edge')
        g.atmosphere.current_visitor=None; motion.tick(g,122)
        check(motion.snapshot() is None, key+' departure removes actor')
    check(g.duck.needs.social > 20, 'social interaction affects actual Cheese needs')
    friendships = {k:v.friendship_points for k,v in g.atmosphere.visitor_friendships.items()}
    g._save_game(); g._flush_pending_save(); g._load_game()
    check({k:v.friendship_points for k,v in g.atmosphere.visitor_friendships.items()}==friendships, 'guest friendships survive actual save/load')
    (out/'scenes.json').write_text(json.dumps(fixtures))
    report={'result':'PASS','guests':len(PROFILES),'rare':len(VISITORS),'checks':len(checks),'save_dir':os.environ['CHEESE_SAVE_DIR']}
    (out/'simulation-checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
finally:
    if hasattr(g,'_save_executor'): g._save_executor.shutdown(wait=True)
    from audio.sound import sound_engine
    sound_engine.shutdown()
    if hasattr(g,'_talk_executor'): g._talk_executor.shutdown(wait=False)
