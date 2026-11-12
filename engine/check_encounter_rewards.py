"""Completion-owned encounter rewards through production invitation/tick paths.

Speech inference is held pending (not replaced by invented conversation). Native
rendezvous, refusal, arrival, completion and save boundaries remain production.
"""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from concurrent.futures import Future
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-encounter-rewards-')
os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,encounters
from engine.living_world import LivingPond
from world.friends import visitor_animator
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(46);checks=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
class PendingSpeech:
    def __init__(self):self.submissions=[]
    def submit(self,*args,**kwargs):
        self.submissions.append((args,kwargs));return Future()
    def shutdown(self,**kwargs):pass
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.duck.growth_stage='adult';g.renderer._show_talk=False;sound_engine.enabled=False
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=10**9;b.executor=PendingSpeech()
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id);p.sync();b.sync();key=friend.id;pos=g.renderer.duck_pos
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    def reset():
        p.cancel();b.pending=None;b.pair_cooldowns.clear();b.tasks.clear();b.utterances.clear();b.executor.submissions.clear()
        p.state['elapsed']+=200;b.next_tick=p.state['elapsed'];b.last_at=p.state['elapsed'];b.housing_last=p.state['elapsed']
        pos.cancel_movement();pos.x=45;pos.y=24;pos.set_state_by_name('idle',0)
        visitor_animator._position_x=65;visitor_animator._position_y=24;visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
        visitor_animator._last_move_time=p.state['elapsed'];visitor_animator._roam_bounds=(2,120,1,36)
        g.duck.current_action=None;g.behavior_ai.clear_action()
        b.sync()
        for actor in ('cheese',key):
            r=b.model.residents[actor];r['social']=.4
            r['interests'].update(observe=.1,practice=.9,share=.1,forage=.1)
        b.tasks[key]=dict(action='rest',until=b.now+10000,context=b.context(key))
    def ledger():
        return copy.deepcopy({actor:{field:b.model.residents[actor][field] for field in ('counts','experiences','relationships','social','memories')} for actor in ('cheese',key)})
    def events():
        return {actor:(dict(b.model.residents[actor]['counts']),b.model.residents[actor]['relationships'].get(key if actor=='cheese' else 'cheese',{}).get('meetings',0)) for actor in ('cheese',key)}
    def step(move=True):
        p.state['elapsed']+=.2;pos._state_start_time-=.2;pos.update(.2)
        if move:
            visitor_animator._mind_motion=b.motion(key)
            meeting=visitor_animator._mind_motion.get('meeting')
            if meeting:meeting['target']=[meeting['target'][0]-g.renderer._camera_x,meeting['target'][1]-g.renderer._camera_y]
            visitor_animator.update(p.state['elapsed'],pos.x,pos.y)
        b.tick()
    # This native refusal was previously credited before create returned None.
    reset();ok,message=p.start('rest');check(ok,'native rest plan starts: '+message);before=ledger();journal=copy.deepcopy(p.state['journal'])
    check(encounters.create(b,'cheese',key,'practice',.5) is None,'actual encounter creation refuses while Cheese has another plan')
    b._encounter()
    check(not b.coactivities and ledger()==before,'refused invitation gives no learning, bond, social restoration or completed memories')
    check(p.state['journal']==journal and not b.executor.submissions and b.pending is None,'refused invitation records no shared journal or speech request')
    p.cancel()
    # Successful creation is still only a reservation and spoken invitation.
    reset();before=ledger();journal=copy.deepcopy(p.state['journal']);b._encounter()
    check(len(b.coactivities)==1 and len(b.executor.submissions)==1,'successful production invitation reserves scene and requests speech once')
    check(ledger()==before and p.state['journal']==journal,'successful invitation itself gives no completed-activity rewards')
    scene=next(iter(b.coactivities.values()));fixed=copy.deepcopy(scene['spots']);initial=events();positions=set()
    for _ in range(500):
        step();positions.add((round(pos.x,3),round(visitor_animator._position_x,3)))
        if scene['phase']=='act':break
    check(scene['phase']=='act' and len(positions)>5 and scene['spots']==fixed,'both real animators arrive at the fixed scene before performance')
    check(events()==initial,'arrival alone gives no learning or bond')
    # Save excludes transient reservations; reloading cannot finish a ghost pair.
    saved=json.loads(json.dumps(p.save()));restored=LivingPond(saved)
    try:
        check(not restored.minds.coactivities,'in-progress encounters cancel on save/reload rather than serializing reward markers')
        check(restored.state['minds']==saved['minds'],'reload preserves existing minds without awarding unfinished encounter')
    finally:restored.minds.close()
    for _ in range(600):
        if not b.coactivities:break
        step()
    check(not b.coactivities,'completed encounter releases both reservations')
    check(scene.get('rewarded') is True and scene['elapsed']==scene['duration'],'production tick marks a completed encounter rewarded')
    for actor in ('cheese',key):
        after=b.model.residents[actor];prior=before[actor];other=key if actor=='cheese' else 'cheese'
        check(after['counts']['practice']==prior['counts']['practice']+1 and after['counts']['share']==prior['counts']['share'],'completion learns exactly one selected activity for '+actor)
        check(after['experiences']==prior['experiences']+1 and after['relationships'][other]['meetings']==prior['relationships'].get(other,{}).get('meetings',0)+1,'completion bonds and teaches once for '+actor)
        check(after['social']>prior['social'],'social restoration belongs to completed performance for '+actor)
    check(len(p.state['journal'])==len(journal)+1 and p.state['journal'][-1]['kind']=='shared','completion adds one truthful shared journal entry')
    # Re-delivery of the same completed scene through the production tick is
    # harmless, even if a caller accidentally re-inserts its released object.
    before_events=events();journal=copy.deepcopy(p.state['journal']);b.coactivities['duplicate']=scene
    step(move=False)
    for _ in range(8):step(move=False)
    check(events()==before_events and p.state['journal']==journal and not b.coactivities,'duplicate completion produces no additional learning, bond or memory')
    restored=LivingPond(json.loads(json.dumps(p.save())))
    try:
        check(not restored.minds.coactivities and all(restored.minds.model.residents[k]['counts']==b.model.residents[k]['counts'] for k in ('cheese',key)),'completed rewards persist on reload without replaying reservations')
    finally:restored.minds.close()
    # Cancel at approach and during the shared performance; no result reward.
    for phase in ('approach','act'):
        reset();before_events=events();journal=copy.deepcopy(p.state['journal']);b._encounter();scene=next(iter(b.coactivities.values()))
        if phase=='act':
            for _ in range(500):
                step()
                if scene['phase']=='act':break
            check(scene['phase']=='act','cancellation fixture reaches actual shared performance')
        p.cancel();step(move=False)
        check(not b.coactivities and events()==before_events and p.state['journal']==journal and not scene.get('rewarded'),'cancelled '+phase+' gives no shared completion credit')
    # A failed rendezvous times out; tokens cannot transfer credit to another visit.
    reset();before_events=events();b._encounter();scene=next(iter(b.coactivities.values()))
    for _ in range(250):
        step(move=False)
        if not b.coactivities:break
    check(not b.coactivities and events()==before_events and not scene.get('rewarded'),'failed arrival times out with no completion credit')
    print(json.dumps(dict(result='PASS',checks=len(checks),save_dir=os.environ['CHEESE_SAVE_DIR'])))
finally:
    b.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
