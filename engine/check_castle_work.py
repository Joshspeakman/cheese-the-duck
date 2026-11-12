"""Native physical bounce house controls, material care and actual contacts."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-surface-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,carnival as company,excursions,surface_play as surface,castle_work as castle
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
            if capture and int(clock*5)%3==0:frames.append(snapshot(g,g.renderer))
    def reset(item='bounce_house',kind='regular',age='adult',score=None):
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
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=26  # Exterior ground corridor, also used by the --serve UI fixture.
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next(a for a in p.placements if a.item_id==item);iid=placement.instance;obj=p.object_state(item,iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},carnival_routines={},carnival_company={});excursions.state(item,obj)
        ok,msg=p.start('item',item,instance=iid,carnival_choice=score) if score else p.start('item',item,instance=iid)
        if age=='egg':check(not ok,'egg cannot board');return None,None,obj
        check(ok,item+' starts: '+msg);plan=p.state['plan'];w=plan['carnival_work']
        if score:w.update(id=score,label=company.PROGRAMS[score]['label']);plan['label']=w['label']
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
        plan,key,obj=reset(kind='solo');iid=plan['instance'];p.cancel();castle.state(obj)['motor']='off'
        def emit():
            p._cache=None;print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),item='bounce_house',copies=[iid]))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_advance':
                if command.get('until')=='finish':finish()
                elif command.get('seconds'):advance(round(command['seconds']/.2))
                else:until(command['until'])
            else:p.command(command)
            emit()
        raise SystemExit(0)
    for score,spec in castle.ROUTINES.items():
        for at,field,value in spec['effects']:
            where=castle.station(dict(id=score,ride_elapsed=at*spec['duration']))
            expected=dict(motor='switch',vent='valve',door='door',latch='buckle',flag='flag_rope',hose='hose',kink='hose',dust_fraction='grill',mesh_fraction='door',roof_fraction='drain',prints_fraction='apron',inspection='gauge' if value=='pressure' else 'seam').get(field,field)
            check(where['name']==expected and where['travel']==1,score+' physically reaches '+expected+' before changing '+field)
    for n,(score,spec) in enumerate(castle.ROUTINES.items()):
        plan,key,obj=reset(kind=['regular','rare','story','wise_owl'][n%4],score=score);w=plan['carnival_work'];s=castle.state(obj)
        s.update(dust=.8,mesh_wet=.7,roof_water=.6,prints=.9)
        for _,field,value in spec['effects']:
            if field in castle.MOVING:s[field]=s['targets'][field]=1-value
            elif field in ('motor','latch'):s[field]='off' if field=='motor' and value=='on' else 'on' if field=='motor' else 1-value
        inventory=possessions();condition=obj['condition'];learning={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        until('service',capture=n%3==0)
        native=score in castle.PHYSICAL_SCORES
        check(castle.physical_active(plan)==native,score+' uses its intended native or legacy controller')
        if native:check(company.active(b) is None and not w['paired'],score+' adult native pilot stays solo despite a present visitor')
        else:check(company.active(b)['phase']=='ready',score+' visitor reaches independent work spot')
        check(not w['events'] and obj['uses']==0,score+' arrival does not operate any control or grant a use')
        before_targets=copy.deepcopy(s['targets']);before_motor=s['motor'];advance(5)
        check(s['targets']==before_targets and s['motor']==before_motor,score+' no operation before physical contact')
        finish(capture=True)
        check(w['events']==list(range(len(spec['effects']))),score+' every authored contact applies exactly once')
        final={field:value for _,field,value in spec['effects']}
        for field,value in final.items():
            if field in castle.MOVING:check(s['targets'][field]==value and abs(s[field]-value)<.002,score+' reaches real '+field+' endpoint')
            elif field in ('motor','latch'):check(s[field]==value,score+' preserves real '+field+' setting')
            elif field.endswith('_fraction'):
                f={'dust_fraction':'dust','mesh_fraction':'mesh_wet','roof_fraction':'roof_water','prints_fraction':'prints'}[field]
                check(s[f]<w['start'][f]*value+.02,score+' removes actual stored '+f)
            elif field=='inspection':check(obj['castle_inspections'].get(value)==sum(e[1]=='inspection' and e[2]==value for e in spec['effects']) and w['inspection']['condition']==round(condition,3),score+' records observation without an invented repair')
        check(obj['uses']==1 and obj['carnival_routines'].get(score)==1,score+' one original use and routine completion')
        if native:
            check(not obj['carnival_company'],score+' adult solo completion grants no companion credit')
            check(all(b.model.residents[k]['counts']['share']==v for k,v in learning.items()),score+' adult solo work grants neither brain a shared memory')
        else:
            check(obj['carnival_company'].get(key)==1,score+' shared completion credits the present companion once')
            check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in learning.items()),score+' both brains remember finished work once')
        check(possessions()==inventory,score+' consumes and creates no tools, repair supplies or currency')
        check(abs(obj['condition']-(condition-.006))<1e-8,score+' does not secretly repair the house')
        company.complete(p,plan);check(obj['carnival_routines'][score]==1,score+' completion is idempotent')
        if score=='castle_pressure_check':
            check(len(w['inspections'])==2 and w['inspections'][1]['pressure']>w['inspections'][0]['pressure']+.2,'diagnostic compares real pressure before and after closing the valve')
    # Other ages still exercise the existing shared start-control path.
    for age,legacy_score in ((age,score) for age in ('young_adult','elder') for score in sorted(castle.PHYSICAL_SCORES)):
        plan,key,obj=reset(age=age,score=legacy_score);until('service')
        check(not castle.physical_active(plan) and company.active(b)['phase']=='ready',age+' retains shared legacy '+legacy_score)
        finish();check(obj['uses']==1 and obj['carnival_routines'].get(legacy_score)==1 and obj['carnival_company'].get(key)==1,age+' legacy '+legacy_score+' completes with shared credit')
    for n,key in enumerate(PROFILES):
        score=list(castle.ROUTINES)[n%24];plan,actor,obj=reset(kind=key,score=score,age='young_adult' if score in castle.PHYSICAL_SCORES else 'adult');until('service');advance(80);frames.append(snapshot(g,g.renderer))
        r=company.active(b);check(r and r['actor']==actor and r['phase']=='ready',key+' reaches a real control activity')
        if key=='butterfly_fairy':check(r['mode']=='watch' and castle.conversation(p,plan,key,r)['body_status']=='watching from outside','butterfly observes controls without invented gripping limbs')
        finish();check(obj['carnival_company'].get(actor)==1,key+' receives one meaningful work memory')
    for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset(kind='solo',age=age,score='castle_door_open')
        if plan:until('service');advance(90);frames.append(snapshot(g,g.renderer));finish();check(obj['castle']['door']==1,age+' can use the reachable low door cord')
    for score in ('castle_start','castle_roof_drain','castle_door_close','castle_tie_left'):
        plan,key,obj=reset(score=score);until('service');advance(30);plan['paused']=True;p._activity(0);before=copy.deepcopy((obj['castle'],obj['excursion']['inflation'],plan['carnival_work']));advance(20)
        check((obj['castle'],obj['excursion']['inflation'],plan['carnival_work'])==before,score+' pause freezes fabric, fan, strokes and contact history')
        plan['paused']=False;g.duck.current_action='feed';advance(20)
        check((obj['castle'],obj['excursion']['inflation'],plan['carnival_work'])==before,score+' direct care cannot advance a hidden control worker')
        g.duck.current_action=None;finish()
    # A cancelled press is not a press. A completed press survives cancellation.
    plan,key,obj=reset(kind='solo',score='castle_stop');s=castle.state(obj);s['motor']='on';until('service');advance(10);p.cancel()
    check(s['motor']=='on' and obj['uses']==0,'cancel before switch contact preserves on setting and no use')
    plan,key,obj=reset(score='castle_stop');s=castle.state(obj);s['motor']='on';until('service');advance(80);p.cancel()
    check(s['motor']=='off' and obj['uses']==0 and not obj['carnival_company'],'cancel after switch contact keeps off setting without completion credit')
    for score in ('castle_roof_drain','castle_door_close','castle_flag_down'):
        plan,key,obj=reset(score=score);until('service');s=castle.state(obj);s['roof_water']=.9
        g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy';finish(capture=True)
        check(obj['uses']==1 and not plan['carnival_work'].get('interrupted'),score+' weather-closing work remains useful in actual rain')
    plan,key,obj=reset(score='castle_start');until('service');g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy';advance()
    check(plan['carnival_work'].get('interrupted') and not p.state['plan'],'storm interrupts native blower work and releases its reservation')
    finish();check(obj['uses']==0 and not obj['carnival_company'],'interrupted control work grants no original-use or shared completion')
    plan,key,obj=reset(age='young_adult',score='castle_start');until('service');g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy';advance()
    check(plan['carnival_work'].get('withdrawal') and plan['carnival_work']['stage']=='service_exit','legacy blower worker withdraws through its existing exit stage in a storm')
    finish();check(obj['uses']==0 and not obj['carnival_company'],'interrupted legacy blower work grants no completion credit')
    plan,key,obj=reset(kind='solo',score='castle_stop');until('service');finish();p.state['cooldowns']={};obj['last_use']=-1000
    check(not p.start('item','bounce_house',instance=plan['instance'])[0],'play cannot magically override a stopped blower')
    p.command(dict(action='carnival_action',target='bounce_house',instance=plan['instance'],text='castle_start'));finish();p.state['cooldowns']={};obj['last_use']=-1000
    check(p.start('item','bounce_house',instance=plan['instance'])[0],'using real start control makes bouncing available again');p.cancel()
    plan,key,obj=reset(score='castle_door_open');until('service');advance(100);w=copy.deepcopy(plan['carnival_work']);iid=plan['instance'];saved=copy.deepcopy(obj['castle'])
    g._save_game();g._flush_pending_save();g.renderer.duck_pos.x=48;g.renderer.duck_pos.y=26;g._load_game();p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9;p.sync();loaded=p.state['plan']
    check(loaded['paused'] and loaded['carnival_work']['clock']==w['clock'] and loaded['carnival_work']['events']==w['events'],'load preserves exact material time and consumed contact events')
    check(not loaded['carnival_work'].get('interrupted') and loaded['carnival_work']['physical']['phase']=='approach' and [g.renderer.duck_pos.x,g.renderer.duck_pos.y]==[48,26],'native load reacquires from the actual grounded exterior root without teleporting')
    check(p.object_state('bounce_house',iid)['castle']==saved,'load preserves every actual control and material quantity')
    check(not b.carnival_guests and 'companion' not in loaded['carnival_work'],'load does not resurrect a helper')
    p.command(dict(action='resume'));finish();obj=p.object_state('bounce_house',iid)
    check(obj['uses']==1 and obj['castle']['door']==1 and not obj['carnival_company'],'resumed control completes once without false shared credit')
    plan,key,obj=reset(score='castle_door_close');until('service');g.habitat.placed_items=[PlacedItem('bounce_house',9,7)];p.sync();advance()
    check(not p.state['plan'] and obj['uses']==0 and not b.carnival_guests,'same-coordinate replacement cannot inherit a work session')
    plan,key,obj=reset(score='castle_vent_open');until('service');g.habitat.placed_items=[];p.sync();advance()
    check(not p.state['plan'] and obj['uses']==0 and not b.carnival_guests,'storage cancels physical work without completion')
    plan,key,obj=reset(kind='solo',score='castle_start');twin=PlacedItem('bounce_house',1,1);g.habitat.stored_placements.append(twin);p.sync();other=p.object_state('bounce_house',twin.instance_id);castle.state(other)['motor']='off';until('service');finish()
    check(other['castle']['motor']=='off' and other['uses']==0,'stored twin keeps its independent controls')
    # Context chooses work because material needs it, and respects a deliberate
    # shutdown. No chores are invented for a clean, ready object.
    plan,key,obj=reset(kind='solo');iid=plan['instance'];p.cancel();s=castle.state(obj)
    check(castle.next_work(p,obj) is None,'fresh ready house does not invent a maintenance task')
    s.update(roof_water=.8,mesh_wet=.8)
    check(castle.next_work(p,obj)[0]=='castle_after_rain','stored water selects actual fabric drying')
    check(p.start('item','bounce_house',automatic=True,instance=iid)[0] and p.state['plan']['carnival_work']['id']=='castle_after_rain','automatic original item path performs needed material work')
    finish();p.state['cooldowns']={};obj['last_use']=-1000
    g.day_night.get_current_hour=lambda:22;p.sync();p.hour=22
    check(p.start('item','bounce_house',automatic=True,instance=iid)[0] and p.state['plan']['carnival_work']['id']=='castle_close_night','night selects shutting down the actual empty house')
    finish();check(s['motor']=='off' and s['latch']==1 and s['flag']==0 and not s['power_hold'],'autonomous night closing keeps the morning reopening available')
    p.state['cooldowns']={};obj['last_use']=-1000;g.day_night.get_current_hour=lambda:12;p.sync();p.hour=12
    check(p.start('item','bounce_house',automatic=True,instance=iid)[0] and p.state['plan']['carnival_work']['id']=='castle_open_day','daytime reopens a house closed by its residents')
    finish();check(castle.ready(obj)[0],'opening procedure restores actual bounce preconditions')
    p.state['cooldowns']={};obj['last_use']=-1000
    check(p.start('item','bounce_house',instance=iid,carnival_choice='castle_stop')[0],'player can explicitly switch the blower off');finish()
    p.state['cooldowns']={};obj['last_use']=-1000
    check(s['power_hold'] and castle.next_work(p,obj) is None and not p.start('item','bounce_house',automatic=True,instance=iid)[0],'autonomy never overrides a player-requested shutdown')
    s.update(power_hold=False,motor='auto');g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy'
    check(castle.next_work(p,obj) is None,'storms favor finding shelter instead of outdoor chores')
    plan,key,obj=reset(kind='solo');until('play');check(obj['castle']['prints']>=.04,'physical boarding leaves tracks on the apron');p.cancel()
    # Multi-part work saves applied effects, current route and inspection
    # history, then completes once without resurrecting its previous helper.
    plan,key,obj=reset(score='castle_pressure_check');until('service');advance(360);iid=plan['instance'];w=copy.deepcopy(plan['carnival_work'])
    check(len(w.get('inspections',[]))==1 and len(w['events'])>1,'procedure has a real first reading and intermediate control work before save')
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9;p.sync();loaded=p.state['plan'];obj=p.object_state('bounce_house',iid)
    check(loaded['paused'] and loaded['carnival_work']['events']==w['events'] and loaded['carnival_work']['inspections']==w['inspections'],'procedure save keeps consumed contacts and first measured pressure')
    p.command(dict(action='resume'));finish()
    check(obj['uses']==1 and obj['castle_inspections']['pressure']==2 and not obj['carnival_company'],'resumed procedure records only its two real readings and one completion')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'castle-care-frames.json').write_text(json.dumps(frames));(out/'castle-care-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
