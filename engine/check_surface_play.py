"""Native spring floors, short flights, independent company and safe landings."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-surface-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,carnival as company,excursions,surface_play as surface
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
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=24
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next(a for a in p.placements if a.item_id==item);iid=placement.instance;obj=p.object_state(item,iid)
        obj.update(last_use=-1000,uses=0,dirt=0,wetness=0,condition=1,excursion={},carnival_routines={},carnival_company={});excursions.state(item,obj)
        ok,msg=p.start('item',item,instance=iid)
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
        selected=sys.argv[sys.argv.index('--serve')+1] if len(sys.argv)>sys.argv.index('--serve')+1 else 'bounce_house'
        plan,key,obj=reset(selected,kind='solo');iid=plan['instance'];p.cancel()
        def emit():
            p._cache=None;print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),item=selected,copies=[iid]))),flush=True)
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
    parity=[]
    for n,(score,spec) in enumerate(surface.ROUTINES.items()):
        plan,key,obj=reset(spec['item'],kind=['regular','rare','story','wise_owl'][n%4],score=score)
        w=plan['carnival_work'];before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)};inventory=possessions();positions=set();seen=set()
        for _ in range(800):
            advance(capture=n in (0,1,4,11,14,15,18,20,26));positions.add(tuple(round(v,3) for v in b.present[key]));seen.add(w['stage'])
            if w['stage']=='play':break
        r=company.active(b)
        check(w['stage']=='play' and r and r['phase']=='ready' and len(positions)>3,score+' walks independently to the entry')
        check(r['spot']==w['queue_b'] and r['spot']!=w['queue_a'] and w['paired'],score+' separate approach and playing lanes')
        check('board_a' in seen and 'board_b' in seen,score+' enters one at a time through the doorway/fringe')
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),score+' arrival and entry grant no learning')
        frames.append(snapshot(g,g.renderer));max_jump=max_lift=max_press=0.;expected={role:len(spec['leaps'][role]) for role in ('a','b')}
        captured_air=captured_mid=False
        while w['stage']=='play':
            v=surface.controls(w);s=obj['excursion']['surface']
            # A stage transition can precede the first play sample by a frame.
            if w['clock']>0:
                assert all(abs(s[role][k]-v[role][k])<1e-7 for role in ('a','b') for k in ('jump','press','u','v','impact')),score+' native controls'
            max_jump=max(max_jump,s['a']['jump'],s['b']['jump']);max_lift=max(max_lift,s['lift']);max_press=max(max_press,s['a']['press'],s['b']['press'])
            if len(parity)<1800 and int(w['clock']*5)%13==0:parity.append(dict(work=copy.deepcopy(w),expected=v))
            if not captured_air and max(s['a']['jump'],s['b']['jump'])>.3:
                facts=company.conversation(p,plan)
                check(facts['body_status']=='in the air above the spring floor' if s['a']['jump']>.05 else facts['body_status']=='on the surface',score+' chat knows whether Cheese is airborne')
                check(facts['company']==b.model.residents[key]['name'],score+' chat names actual shared company')
                frames.append(snapshot(g,g.renderer));captured_air=True
            if not captured_mid and w['clock']>spec['duration']*.45:
                frames.append(snapshot(g,g.renderer));captured_mid=True
            advance(capture=n in (0,1,4,11,14,15,18,20,26))
        check(w['landings']==expected and obj.get('soft_landings',0)==sum(expected.values()),score+' counts each actual landing exactly once')
        if any(expected.values()):check(max_jump>.4 and max_press>.2,score+' feet leave the compressing floor')
        if spec['item']=='magic_carpet':check(max_lift>0 and max_jump==0,score+' carpet rises under seated riders without invented jumping')
        finish(capture=n in (0,14,18));check(obj['uses']==1 and obj['carnival_routines'].get(score)==1 and obj['carnival_company'].get(key)==1,score+' one original use and completed duet after both exit')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),score+' both learning brains remember the shared play once')
        check(not obj['excursion']['surface']['active'] and obj['excursion']['surface']['lift']==0,score+' returns to rest after exit')
        check(possessions()==inventory,score+' inventory/currency/travel unchanged')
        company.complete(p,plan);check(obj['carnival_routines'][score]==1,score+' cannot replay completion')
    payload=json.dumps([x['work'] for x in parity])
    script="import{surfaceControls}from './engine/client/surface-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(surfaceControls)));"
    actual=json.loads(subprocess.run(['node','--input-type=module','-e',script],input=payload,text=True,capture_output=True,check=True,cwd=ROOT).stdout)
    for entry,other in zip(parity,actual):
        for role in ('a','b'):
            for k,v in entry['expected'][role].items():
                assert abs(v-other[role][k])<1e-8 if isinstance(v,(int,float)) else v==other[role][k],(entry['work']['id'],k)
        assert abs(entry['expected']['lift']-other['lift'])<1e-8
    check(len(actual)==len(parity),'native and renderer control samplers agree across '+str(len(parity))+' actual frames')
    for n,key in enumerate(PROFILES):
        item='magic_carpet' if n%2 else 'bounce_house';plan,actor,obj=reset(item,kind=key);until('play');advance(25)
        r=company.active(b);check(r and r['actor']==actor and r['phase']=='ready',key+' reaches the shared surface independently')
        if key=='butterfly_fairy':
            check(r['mode']=='watch' and not plan['carnival_work']['paired'] and company.conversation(p,plan,key)['body_status']=='watching beside the entry','butterfly watches without false legs, landing or seat')
            check(obj['excursion']['surface']['b']['jump']==0,'spectator cannot depress or jump from the floor')
        frames.append(snapshot(g,g.renderer));finish();check(obj['carnival_company'].get(actor)==1,key+' shared company is remembered after exit')
    for item in sorted(surface.ITEMS):
        for tag,hour,season,age,energy,fun in [('tired',12,'spring','adult',30,95),('young',12,'spring','duckling',95,95),('grumpy',12,'spring','adult',95,25),('autumn',12,'fall','adult',95,95),('night',23,'spring','adult',95,95),('dusk',19,'spring','adult',95,95)]:
            plan,key,obj=reset(item,kind='solo',age=age);iid=plan['instance'];p.cancel()
            g.day_night.get_current_hour=lambda value=hour:value;g.atmosphere.current_season=Season.FALL if season=='fall' else Season.SPRING
            g.duck.needs.energy=energy;g.duck.needs.fun=fun;g.duck_store.sync_from_duck(g.duck);p.sync()
            ok,message=p.start('item',item,instance=iid);check(ok,item+' '+tag+' context starts');plan=p.state['plan'];prefix='bounce' if item=='bounce_house' else 'carpet'
            suffix={'tired':'quiet','young':'first','grumpy':'grumble','night':'moon','autumn':'leaf' if prefix=='bounce' else 'balance','dusk':'echo' if prefix=='bounce' else 'evening'}[tag]
            check(plan['carnival_work']['id']==prefix+'_'+suffix,item+' '+tag+' chooses appropriate native program')
            until('play');advance(60);frame=snapshot(g,g.renderer);frames.append(frame)
            check(frame['hour']==hour and frame['season']==season,item+' '+tag+' actual time and season reach the world')
            if hour>=18:check(obj['excursion']['lights']==1,item+' '+tag+' evening lights use native time')
            finish();check(obj['uses']==1,item+' '+tag+' selected program finishes once')
    for item in sorted(surface.ITEMS):
        for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
            plan,key,obj=reset(item,kind='solo',age=age)
            if not plan:continue
            check(plan['carnival_work']['factors']['a']==surface.scale(age),item+' '+age+' native age-specific jump strength')
            until('play');advance(25);frames.append(snapshot(g,g.renderer));finish();check(obj['uses']==1,item+' '+age+' completes at own body scale')
        plan,key,obj=reset(item);until('play');advance(55);w=plan['carnival_work'];saved=copy.deepcopy(w);floor=copy.deepcopy(obj['excursion']['surface']);inflation=obj['excursion']['inflation'];overlap=company.active(b)['overlap'];plan['paused']=True;advance(20)
        check(w==saved and obj['excursion']['surface']==floor and obj['excursion']['inflation']==inflation and company.active(b)['overlap']==overlap,item+' pause freezes floor, lift, participants and shared time')
        plan['paused']=False;g.duck.current_action='feed';advance(20)
        check(w==saved and obj['excursion']['surface']==floor and company.active(b)['overlap']==overlap,item+' direct care freezes the actual surface')
        g.duck.current_action=None;finish()
        plan,key,obj=reset(item,score='carpet_climb' if item=='magic_carpet' else 'bounce_together');until('play');advance(65)
        before=b.model.residents[key]['counts']['share'];height=obj['excursion']['surface']['lift'];g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.sync();p.weather_type='stormy';advance()
        check(plan['carnival_work'].get('withdrawal') and plan['carnival_work']['stage']=='land' and not plan['carnival_work']['done'],item+' storm starts controlled landing while aboard')
        if item=='magic_carpet':check(0<obj['excursion']['surface']['lift']<=height,item+' storm lowers a genuinely raised carpet without teleporting')
        finish(capture=True);check(obj['uses']==0 and not obj['carnival_routines'] and b.model.residents[key]['counts']['share']==before,item+' interrupted play grants no completed-use or shared reward')
        plan,key,obj=reset(item);until('play');advance(30);g.friends.current_visit=None;b.sync();advance()
        check(not b.carnival_guests and 'companion' not in plan['carnival_work'] and all(v==0 for v in obj['excursion']['surface']['b'].values()),item+' departing visitor leaves no ghost weight or passenger')
        finish();check(obj['uses']==1 and not obj['carnival_company'],item+' Cheese finishes alone without shared credit')
        plan,key,obj=reset(item);until('play');before=b.model.residents[key]['counts']['share'];g.habitat.placed_items=[];p.sync();advance()
        check(not p.state['plan'] and not b.carnival_guests and obj['uses']==0 and b.model.residents[key]['counts']['share']==before,item+' storing the occupied copy releases both without rewards')
        plan,key,obj=reset(item);until('play');g.habitat.placed_items=[PlacedItem(item,9,7)];p.sync();advance()
        check(not p.state['plan'] and not b.carnival_guests and obj['uses']==0,item+' identical-coordinate replacement cannot inherit play')
        plan,key,obj=reset(item,kind='solo');twin=PlacedItem(item,1,1);g.habitat.stored_placements.append(twin);p.sync();other=p.object_state(item,twin.instance_id);other['excursion']['inflation']=.45
        until('play');finish();check(other['excursion']['inflation']==.45 and other['uses']==0,item+' stored twin retains its own condition and history')
        plan,key,obj=reset(item,kind='solo');p.cancel();obj['condition']=.1
        check(not p.start('item',item,instance=plan['instance'])[0],item+' damaged surface needs repair first')
        plan,key,obj=reset(item);until('land');g.friends.current_visit=None;b.sync();advance(2)
        check(all(v==0 for v in obj['excursion']['surface']['b'].values()),item+' landing cannot restore departed guest pressure');finish()
        plan,key,obj=reset(item,kind='solo');iid=plan['instance'];p.cancel();choice='carpet_banks' if item=='magic_carpet' else 'bounce_echo'
        p.command(dict(action='carnival_action',target=item,instance=iid,text=choice))
        check(p.state['plan']['instance']==iid and p.state['plan']['carnival_work']['id']==choice,item+' notebook chooses exact copy and program')
        finish();check(obj['uses']==1,item+' notebook activity completes original action')
        plan,key,obj=reset(item,score='carpet_climb' if item=='magic_carpet' else 'bounce_together');until('play');advance(75)
        iid=plan['instance'];w=copy.deepcopy(plan['carnival_work']);floor=copy.deepcopy(obj['excursion']['surface'])
        g._save_game();g._flush_pending_save();g.renderer.duck_pos.x=10;g.renderer.duck_pos.y=12;g._load_game();p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9;p.sync();loaded=p.state['plan']
        check(loaded['paused'] and loaded['carnival_work']['clock']==w['clock'] and loaded['carnival_work']['events']==w['events'],item+' load preserves paused time and landing history')
        check(not b.carnival_guests and 'companion' not in loaded['carnival_work'],item+' load cannot resurrect a transient passenger')
        check(all(v==0 for v in p.object_state(item,iid)['excursion']['surface']['b'].values()),item+' load drops absent guest weight immediately')
        check(p.object_state(item,iid)['excursion']['surface']['lift']==floor['lift'] and company.valid(p,loaded),item+' load preserves height and exact placed surface')
        check([g.renderer.duck_pos.x,g.renderer.duck_pos.y]==loaded['carnival_work']['queue_a'],item+' load restores the ground projection')
        p.command(dict(action='resume'));finish();check(p.object_state(item,iid)['uses']==1 and not p.object_state(item,iid)['carnival_company'],item+' resume finishes solo with no duplicated shared credit')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'surface-play-frames.json').write_text(json.dumps(frames))
    (out/'surface-play-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),parity=len(parity)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),parity=len(parity))))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
