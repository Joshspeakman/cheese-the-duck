"""Real animator rendezvous, scene completion and interruption with isolated saves."""
import os,sys,tempfile,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-encounters-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,encounters
from world.friends import visitor_animator
from world.atmosphere import VISITORS
from datetime import datetime
sys.stdout=host.WIRE
checks=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.duck.growth_stage='adult';g.renderer._show_talk=False
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=10**9
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id);p.sync();b.sync()
    pos=g.renderer.duck_pos;pos.x=45;pos.y=24
    visitor_animator._position_x=65;visitor_animator._position_y=24;visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
    visitor_animator._last_move_time=0;visitor_animator._roam_bounds=(2,120,1,36)
    b.sync();s=encounters.create(b,'cheese',friend.id,'practice',.5)
    check(bool(s),'present actors reserve a fixed meeting place')
    b.coactivities['pair']=s;fixed=copy.deepcopy(s['spots']);before=b.model.residents['cheese']['counts']['practice']
    check(p.busy,'a shared scene reserves Cheese from unrelated autonomous routines')
    positions=[]
    for i in range(500):
        p.state['elapsed']+=.2
        pos.update(.2);visitor_animator._mind_motion=b.motion(friend.id)
        meeting=visitor_animator._mind_motion.get('meeting')
        if meeting:meeting['target']=[meeting['target'][0]-g.renderer._camera_x,meeting['target'][1]-g.renderer._camera_y]
        visitor_animator.update((i+1)*.2,pos.x,pos.y);b.tick()
        positions.append((pos.x,visitor_animator._position_x))
        assert s['spots']==fixed,'meeting point moved during the scene'
        if not b.coactivities:break
    check(len(set(positions))>5,'both participants travel through real intermediate positions')
    check(s['spots']==fixed,'meeting point stays fixed for the whole rendezvous and performance')
    check(not b.coactivities,'shared performance completes and releases its reservations')
    check(b.model.residents['cheese']['counts']['practice']==before+1,'one complete performance teaches one shared experience: '+str({'before':before,'after':b.model.residents['cheese']['counts']['practice'],'scene':s,'positions':b.present,'available':p.available()}))
    after=b.model.residents['cheese']['counts']['practice'];p.state['elapsed']+=2;b.tick()
    check(b.model.residents['cheese']['counts']['practice']==after,'completion never repeats')
    check(not p.busy,'completed pair returns to independent wandering')
    # A new visit with the same resident ID cannot inherit an earlier meeting.
    b.sync();s=encounters.create(b,'cheese',friend.id,'observe',.5);b.coactivities['pair']=s
    b.presence_tokens[friend.id]='different visit'
    check(encounters.advance(b,s,1)=='cancelled','visit token change cancels stale choreography')
    b.cancel_encounter('cheese');b.sync()
    s=encounters.create(b,'cheese',friend.id,'observe',.5);b.coactivities['pair']=s
    check(not p.start('item','missing-object')[0] and b.coactivities,'invalid item requests preserve current shared activity')
    p.cancel();check(not b.coactivities and not pos._is_directed_movement,'user interruption releases both actors')
    b.sync();s=encounters.create(b,'cheese',friend.id,'observe',.5);b.coactivities['pair']=s
    visitor_animator.start_leaving()
    check(encounters.advance(b,s,1)=='cancelled','departing friend leaves immediately without a completion reward')
    b.cancel_encounter('cheese');visitor_animator._is_leaving=False
    # Two NPCs reserve their own spots; Cheese is not the moving reference point.
    rare=next(iter(VISITORS.values())) if isinstance(VISITORS,dict) else VISITORS[0]
    g.atmosphere.current_visitor=(rare,datetime.now().isoformat());g.guest_motion.tick(g,0)
    g.guest_motion.actor.update(x=80,y=24);b.sync()
    s=encounters.create(b,friend.id,rare.id,'observe',.5);b.coactivities['npc-pair']=s
    check(bool(s) and not p.busy,'two visitors can meet independently of Cheese')
    start=g.guest_motion.actor['x'];pos.x=10
    for i in range(20):g.guest_motion.tick(g,(i+1)*.2)
    check(g.guest_motion.actor['x']!=start,'rare guest walks toward its own reservation')
    check(s['spots'][rare.id][0]>50,'moving Cheese does not drag the visitors meeting')
    b.cancel_encounter(friend.id)
    p.weather_type='rainbow';check(encounters.performance(b,'cheese',friend.id,'observe')!='puddle_splash','rainbow does not count as rainfall')
    result={'result':'PASS','checks':len(checks),'details':checks}
    (ROOT/'engine/artifacts/animation-milestone/encounter-simulation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'result':'PASS','checks':len(checks)}))
finally:
    b.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
