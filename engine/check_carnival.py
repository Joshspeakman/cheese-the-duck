"""Actual regular/rare/story arrivals, shared plaything work and interrupted memories."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-carnival-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,carnival as company,excursions
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.building import Structure,StructureStatus
from world.atmosphere import Weather,WeatherType,Season,VISITORS
from world.friends import visitor_animator
from world.guest_cast import PROFILES
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(45);checks=[];frames=[];clock=0.
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    friend=g.friends.generate_new_friend()

    def advance(n=1,capture=False,move=True,dt=.2):
        global clock
        for _ in range(n):
            clock+=dt;p.state['elapsed']+=dt;pos=g.renderer.duck_pos;pos._state_start_time-=dt;pos.update(dt);p._activity(dt)
            if g.friends.current_visit and move:
                visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
            for item,obj,outside in __import__('engine.object_history',fromlist=['records']).records(p):
                excursions.update(item,obj,dt,outside,p.weather_type,.2,p.hour,reserved=company.owns(p,item,obj))
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*5)%15==0:frames.append(snapshot(g,g.renderer))
    def reset(item='ferris_wheel',kind='regular',age='adult',score=None):
        g.day_night.get_current_hour=lambda:12;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.cancel();b.carnival_retry.clear()
        for name in ('nest_helpers','structure_helpers','playmates','ground_helpers','textile_helpers','readers','creators','tasks','housing','furnishings','gardening','musicians','coactivities'):getattr(b,name).clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.story_motion.actor=g.story_motion.token=None;g.guest_motion.actor=g.guest_motion.token=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=age
        for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,95)
        g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,9,7)];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=24
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next(a for a in p.placements if a.item_id==item);iid=placement.instance;obj=p.object_state(item,iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},carnival_routines={},carnival_company={});excursions.state(item,obj)
        ok,msg=p.start('item',item,instance=iid)
        if age=='egg':check(not ok,'egg cannot board');return None,None,obj
        check(ok,item+' starts: '+msg);plan=p.state['plan'];w=plan['carnival_work']
        if score:w.update(id=score,label=company.ROUTINES[score]['label']);plan['label']=w['label']
        start=[min(120,w['queue_b'][0]+8),w['queue_b'][1]]
        if kind=='solo':b.sync();return plan,None,obj
        if kind=='regular' or kind.startswith('friend:'):
            selected=friend
            if kind.startswith('friend:'):
                selected=copy.deepcopy(friend);selected.id=kind;selected.name=PROFILES[kind]['name'];g.friends.friends[kind]=selected
            g.friends.start_visit(selected.id);visitor_animator._friend_name=selected.name;visitor_animator._is_leaving=False
            visitor_animator._position_x=start[0];visitor_animator._position_y=start[1];visitor_animator._target_x=start[0];visitor_animator._target_y=start[1];visitor_animator._rest_until=clock+30;visitor_animator._last_move_time=clock;key=selected.id
        elif kind!='story':
            key='friendly_goose' if kind=='rare' else kind;g.atmosphere.current_visitor=(VISITORS[key],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=start[0],y=start[1])
        else:
            key='story:pip';p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=start[0],y=start[1])
        b.sync();b.model.residents[key]['energy']=.9;b.model.residents[key]['mood']=.7;b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
        return plan,key,obj
    def until(stage,capture=False):
        for _ in range(1600):
            advance(capture=capture)
            if p.state['plan'] and p.state['plan']['carnival_work']['stage']==stage:return
            if not p.state['plan']:break
        raise AssertionError('did not reach '+stage+': '+str(p.state.get('plan')))
    def finish(capture=False):
        for _ in range(1600):
            advance(capture=capture)
            if not p.state['plan']:return
        raise AssertionError('ride never finished')
    def possessions():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.habitat.owned_items,g.treasure.to_dict()))
    if '--serve' in sys.argv:
        plan,key,obj=reset(kind='solo');iid=plan['instance'];p.cancel()
        def emit():
            p._cache=None;print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),item='ferris_wheel',copies=[iid]))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_advance':
                if command.get('until')=='finish':finish()
                else:until(command['until'])
            else:p.command(command)
            emit()
        raise SystemExit(0)
    for n,(score,spec) in enumerate(company.ROUTINES.items()):
        plan,key,obj=reset(spec['item'],kind=['regular','rare','story','wise_owl'][n%4],score=score)
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)};inventory=possessions();w=plan['carnival_work'];positions=set();reservation=False
        for _ in range(800):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]));r=company.active(b)
            if r and not reservation:
                reservation=True;check(r['spot']==w['queue_b'] and r['spot']!=w['queue_a'],score+' separate fixed queue destination')
            if w['stage']=='ride':break
        check(w['stage']=='ride' and r and r['phase']=='ready' and len(positions)>3,score+' real independent arrival before boarding')
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),score+' arrival/boarding add no learning')
        if spec['item']=='ferris_wheel':check(w['seat_a']!=w['seat_b'] and w['paired'],score+' each resident has a distinct cabin')
        paused=copy.deepcopy(w);phase=obj['excursion']['phase'];plan['paused']=True;overlap=r['overlap'];advance(10)
        check(w==paused and obj['excursion']['phase']==phase and r['overlap']==overlap,score+' pause freezes both people and mechanism')
        plan['paused']=False;finish(capture=True)
        check(obj['uses']==1 and obj['carnival_routines'].get(score)==1 and obj['carnival_company'].get(key)==1,score+' exactly one original use and one completed duet')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),score+' both brains learn once after exit')
        check(possessions()==inventory,score+' no inventory/currency/travel reward')
        company.complete(p,plan);check(obj['carnival_routines'][score]==1,score+' completion cannot replay')
    # Every real cast identity arrives through its own movement implementation.
    for n,key in enumerate(PROFILES):
        plan,actor,obj=reset('carousel' if n%2 else 'ferris_wheel',kind=key);until('ride')
        r=company.active(b);check(r and r['actor']==actor and r['phase']=='ready',key+' reaches the actual queue')
        if key=='butterfly_fairy':check(r['mode']=='watch' and not plan['carnival_work']['paired'],'butterfly watches without invented feet or a mounted body')
        frames.append(snapshot(g,g.renderer));finish()
        check(obj['carnival_company'].get(actor)==1,key+' completes meaningful shared company')
    ages=('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary')
    for item in company.ITEMS:
        for age in ages:
            plan,key,obj=reset(item,kind='solo',age=age)
            if plan:until('ride');frames.append(snapshot(g,g.renderer));finish();check(obj['uses']==1,item+' '+age+' completes solo at native scale')
    # UI commands preserve the selected copy and reject malformed/foreign scores.
    plan,key,obj=reset(kind='solo');iid=plan['instance'];p.cancel()
    check(not company.request(p,'ferris_wheel',[],iid)[0] and not company.request(p,'ferris_wheel','carousel_first',iid)[0],'malformed and mismatched choices leave the pond alone')
    p.command(dict(action='carnival_action',target='ferris_wheel',instance=iid,text='wheel_leaves'))
    check(p.state['plan']['instance']==iid and p.state['plan']['carnival_work']['id']=='wheel_leaves','notebook request reaches selected physical copy')
    p.state['plan']['paused']=True;p.command(dict(action='resume'))
    check([g.renderer.duck_pos.target_x,g.renderer.duck_pos.target_y]==p.state['plan']['approach_destination'],'resuming approach walks to the boarding queue, not under the wheel')
    finish();check(obj['uses']==1,'requested notebook activity completes original use once')
    plan,key,obj=reset();advance(300,move=False)
    check(not company.active(b) and not plan['carnival_work'].get('paired'),'unreachable guest times out instead of appearing in a cabin')
    finish();check(obj['uses']==1 and not obj['carnival_company'],'failed arrival grants no shared memory')
    plan,key,obj=reset();until('ride');w=copy.deepcopy(plan['carnival_work']);phase=obj['excursion']['phase'];overlap=company.active(b)['overlap']
    g.duck.current_action='feed';advance(10)
    check(plan['carnival_work']==w and phase==obj['excursion']['phase'] and overlap==company.active(b)['overlap'],'direct care freezes the ride and shared clock')
    g.duck.current_action=None;finish()
    plan,key,obj=reset();until('ride');g.habitat.placed_items=[PlacedItem('ferris_wheel',9,7)];p.sync();advance()
    check(not p.state['plan'] and not b.carnival_guests and obj['uses']==0,'a replacement at identical coordinates cannot inherit riders')
    plan,key,obj=reset(kind='solo');twin=PlacedItem('ferris_wheel',1,1);g.habitat.stored_placements.append(twin);p.sync();other=p.object_state('ferris_wheel',twin.instance_id);other['excursion']['phase']=2.3
    until('ride');finish();check(other['excursion']['phase']==2.3 and other['uses']==0,'active ride leaves stored twin phase and history untouched')
    plan,key,obj=reset(kind='butterfly_fairy');until('ride')
    check(company.conversation(p,plan,key)['actual_seat'] is None and company.conversation(p,plan,key)['seating_status']=='watching from the platform','chat facts do not put a hovering spectator in a seat')
    check(company.conversation(p,plan)['actual_seat']==plan['carnival_work']['seat_a'],'Cheese chat facts reflect the actual assigned riding cabin')
    finish()
    plan,key,obj=reset(kind='solo');p.cancel();obj['condition']=.1
    check(not p.start('item','ferris_wheel',instance=plan['instance'])[0],'damaged ride needs repair before boarding')
    # Rain after boarding returns both riders before cancelling the original use.
    plan,key,obj=reset();until('ride');before=b.model.residents[key]['counts']['share'];g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy';advance(1)
    check(plan['carnival_work'].get('withdrawal') and plan['carnival_work']['stage']=='weather_return' and not plan['carnival_work']['done'],'storm begins controlled return while aboard')
    finish(capture=True);check(obj['uses']==0 and not obj['carnival_routines'] and b.model.residents[key]['counts']['share']==before,'storm return grants no completed ride reward')
    plan,key,obj=reset();until('ride');g.friends.current_visit=None;b.sync();advance(1)
    check(not b.carnival_guests and 'companion' not in plan['carnival_work'],'departed friend disappears without a ghost passenger')
    finish();check(obj['uses']==1 and not obj['carnival_company'],'Cheese finishes alone without shared memory')
    plan,key,obj=reset();until('ride');before=b.model.residents[key]['counts']['share'];g.habitat.placed_items=[];p.sync();advance()
    check(not p.state['plan'] and not b.carnival_guests and obj['uses']==0 and b.model.residents[key]['counts']['share']==before,'storing occupied copy releases both without reward')
    plan,key,obj=reset();until('ride');g.renderer.duck_pos.x-=15;advance()
    check(not p.state['plan'] and not b.carnival_guests and obj['uses']==0,'direct displacement cancels staging')
    plan,key,obj=reset();until('ride');iid=plan['instance'];phase=obj['excursion']['phase'];w=copy.deepcopy(plan['carnival_work'])
    g._save_game();g._flush_pending_save();g.renderer.duck_pos.x=10;g.renderer.duck_pos.y=12;g._load_game();p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9;p.sync()
    loaded=p.state['plan'];check(loaded['paused'] and loaded['carnival_work']['stage']==w['stage'] and loaded['carnival_work']['clock']==w['clock'],'save/load preserves paused native ride clock')
    check(not b.carnival_guests and 'companion' not in loaded['carnival_work'],'save/load cannot resurrect transient guest')
    check(p.object_state('ferris_wheel',iid)['excursion']['phase']==phase,'save/load preserves exact wheel angle')
    check(company.valid(p,loaded),'loaded ride still refers to the same placed copy')
    check([g.renderer.duck_pos.x,g.renderer.duck_pos.y]==loaded['carnival_work']['queue_a'],'loading restores the saved seat ground projection')
    p.command(dict(action='resume'));finish()
    check(p.object_state('ferris_wheel',iid)['uses']==1 and not p.object_state('ferris_wheel',iid)['carnival_company'],'resumed ride finishes solo without resurrecting shared credit')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'carnival-frames.json').write_text(json.dumps(frames))
    (out/'carnival-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
