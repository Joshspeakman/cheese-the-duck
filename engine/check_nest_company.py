"""Shared nest care through real commands, movement controllers and saves."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-nest-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,nest_routines as nest,nest_company as company
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import Weather,WeatherType,Season,VISITORS
from world.building import Structure,StructureStatus
from world.decorations import PlacedDecoration,RoomType
from world.guest_cast import PROFILES
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(24);checks=[];frames=[];clock=0.
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    friend=g.friends.generate_new_friend()
    def reset(core='weave_rim',age='adult',kind='regular',item='basic_nest'):
        p.cancel();b.nest_helpers.clear();b.nest_retry.clear();b.tasks.clear();b.housing.clear();b.house_scenes.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.guest_motion.actor=g.guest_motion.token=None;g.story_motion.actor=g.story_motion.token=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=age
        for need in ('hunger','energy','fun','cleanliness','social'):setattr(g.duck.needs,need,90)
        g.duck_store.sync_from_duck(g.duck)
        g.atmosphere.current_season=Season.SUMMER;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        g.habitat.owned_items=[item,item];g.habitat.placed_items=[PlacedItem(item,10,6),PlacedItem(item,17,6)]
        for room in g.decorations.rooms.values():room.decorations=[]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=60;pos.y=21
        p.sync();p.state['cooldowns'].clear();p.weather_type='sunny';p.season='summer';p.hour=12;p.state['ecology'].update(temperature=30,snow=0)
        iid=g.habitat.placed_items[0].instance_id;obj=p.object_state(item,iid)
        if kind=='regular':
            g.friends.start_visit(friend.id);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._position_x=75;visitor_animator._position_y=20;visitor_animator._last_move_time=clock;key=friend.id
            visitor_animator._target_x=75;visitor_animator._target_y=20;visitor_animator._rest_until=clock+1000
        elif kind=='story':
            key='story:pip';p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=75,y=20)
            g.story_motion.target=(75,20);g.story_motion.rest_until=clock+1000
        else:
            key=kind;g.atmosphere.current_visitor=(VISITORS[key],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=75,y=20)
            g.guest_motion.target=(75,20);g.guest_motion.rest_until=clock+1000
        b.sync();b.model.residents[key]['energy']=.9;b.model.residents[key]['mood']=.7;b.tasks[key]=dict(action='observe',until=b.now+1000,context=b.context(key))
        ok,message=nest.request(p,item,core,iid);check(ok,'actual nest request: '+message)
        return p.state['plan'],key,obj
    def advance(count=1,capture=False,move=True):
        global clock
        for _ in range(count):
            clock+=.1;p.state['elapsed']+=.1;pos=g.renderer.duck_pos;pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
            if g.friends.current_visit and move:
                visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%7==0:frames.append(snapshot(g,g.renderer))
    def arrive(capture=False):
        for _ in range(900):
            advance(capture=capture);r=company.active(b)
            if r and r['phase']=='inside':return r
            if not p.state['plan']:break
        raise AssertionError('helper never arrived: '+str((company.snapshot(b),p.state['plan'])))
    def finish(capture=False):
        for _ in range(1000):
            advance(capture=capture)
            if not p.state['plan'] and not b.nest_helpers:return
        raise AssertionError('nest visit never finished')
    def own_native(item):
        # Remove the preceding fixture's physical obstacles before creating the
        # next source; otherwise layout migration quite correctly stores the
        # temporary habitat copies when the crafted buildings disappear.
        p.cancel();g.habitat.placed_items=[];g.habitat.stored_placements=[];g.habitat.stored_items=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        p.sync()
        reset(item=item);p.cancel();g.habitat.owned_items=[];g.habitat.placed_items=[];g.building.structures=[]
        if item in ('basic_nest','cozy_nest','deluxe_nest'):
            g.building.structures=[Structure(item,(5,4),StructureStatus.COMPLETE),Structure(item,(8,4),StructureStatus.COMPLETE)]
        else:
            g.decorations.owned_decorations[item]=2
            for room in ('garden','pond'):g.decorations.rooms[room].unlocked=True
            g.decorations.rooms['garden'].decorations=[PlacedDecoration(item,RoomType.GARDEN,(9,0),datetime.now().isoformat())]
            g.decorations.rooms['pond'].decorations=[PlacedDecoration(item,RoomType.POND,(7,0),datetime.now().isoformat())]
        p.sync();p.state['cooldowns'].clear();p._cache=None
        return [a.instance for a in p.placements if a.item_id==item]
    selected={}
    cases=[('left_rim','tuck_left_edge','adult','regular'),('right_rim','crossbrace_twig','adult','friendly_goose'),
        ('weave_tension','weave_rim','adult','regular'),('lining_fan','fluff_center','adult','regular'),
        ('tamp_rhythm','tamp_floor','adult','story'),('lining_inspect','straighten_feather','adult','regular'),
        ('quiet_guard','chin_on_rim','adult','regular'),('summer_fan','heat_fan','adult','regular'),
        ('young_support','weave_rim','hatchling','regular'),('patient_company','weave_rim','elder','regular'),
        ('hover_observer','weave_rim','adult','butterfly_fairy')]
    for index,(expected,core,age,kind) in enumerate(cases):
        plan,key,obj=reset(core,age,kind,sorted(nest.NESTS)[index%5]);uses=obj['uses'];history=copy.deepcopy(obj['nest'])
        belongings=copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
        twin=p.object_state(plan['target'],g.habitat.placed_items[1].instance_id);other=copy.deepcopy(twin)
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        paths=set()
        for _ in range(900):
            advance(capture=True);paths.add(tuple(round(v,3) for v in b.present[key]));r=company.active(b)
            if r and r['phase'] in ('approach','enter'):
                check(r['work']['elapsed']==0 and obj['nest']==history,'waiting never touches or completes the nest remotely')
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(paths)>3,expected+' physically arrives from beside the nest')
        check(r['score']==expected,expected+' chosen by the actual age/core/species')
        advance(35,capture=True)
        a=p._plan_view()['residence']['routine'];v=company.snapshot(b)[0]['routine']
        check(a['elapsed']==v['elapsed'] and a['company']['role']=='a' and v['company']['role']=='b',expected+' shares the same native clock')
        check(plan['residence']['slot']==0 and key not in b.housing,expected+' helper occupies no interior nest place')
        finish(capture=True)
        check(obj['uses']==uses+1,expected+' records one original rest visit')
        check(twin==other,expected+' does not change a second nest')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),expected+' both learn once after real shared completion')
        check(obj['nest_company'].get(expected)==1,expected+' is remembered on the exact physical copy')
        check(belongings==(g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()),expected+' creates no inventory, treasure, material or currency reward')
        selected[expected]=True
    check(set(selected)==set(company.SCORES),'every complementary score was selected in a real session')
    plan,key,obj=reset();arrive();before=b.model.residents[key]['counts']['share'];visitor_animator._position_x+=10;b.sync()
    check(company.snapshot(b)==[],'a displaced helper is never snapped back to the rim by rendering');b.tick()
    check(not b.nest_helpers and b.model.residents[key]['counts']['share']==before,'displacement releases the reservation without a completed memory')
    plan,key,obj=reset();r=arrive();advance(60);plan['paused']=True;clock_before=r['work']['elapsed'];state=copy.deepcopy(obj);overlap=r['overlap'];advance(30)
    check(obj==state and r['overlap']==overlap and r['work']['elapsed']==clock_before,'pause freezes both participants and all material contacts')
    prompt=b.prompt(key,'What are we doing?')[0]['content'];facts=json.loads(prompt.split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    check(facts['shared_activity']['status']=='paused' and facts['nest_materials']['right_rim'] in ('loose','tucked'),'chat reads actual paused work and bedding')
    loaded=LivingPond(p.save());check(not loaded.minds.nest_helpers and loaded.state['plan']['paused'],'load preserves the nest but discards a transient helper reservation');loaded.minds.close()
    p.cancel();check(not b.nest_helpers,'cancellation immediately releases independent visitor movement')
    plan,key,obj=reset();share=b.model.residents[key]['counts']['share'];advance(400,move=False)
    check(not b.nest_helpers,'an unreachable helper times out');finish()
    check(b.model.residents[key]['counts']['share']==share,'a missed invitation creates no shared memory')
    for reason in ('leave','replacement_visit','storm','care','move_nest','replace_nest','store_nest'):
        plan,key,obj=reset();r=arrive();advance(35);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='leave':g.friends.current_visit=None
        elif reason=='replacement_visit':g.friends.current_visit.started_at='replacement'
        elif reason=='storm':g.atmosphere.current_weather=Weather(WeatherType.STORMY,.8,1,datetime.now().isoformat());p.weather_type='stormy'
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move_nest':g.habitat.placed_items[0].x+=2;p.sync()
        elif reason=='replace_nest':g.habitat.placed_items[0]=PlacedItem(plan['target'],10,6);p.sync()
        else:g.habitat.store_item(plan['target'],plan['instance']);p.sync()
        advance(4)
        check(not b.nest_helpers and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' does not complete or remember unfinished shared work')
    plan,key,obj=reset();p.cancel()
    for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;ok,_=nest.request(p,'basic_nest','weave_rim',g.habitat.placed_items[0].instance_id)
        check(ok==(age!='egg'),age+' respects physical ability to enter a nest');p.cancel()
    g.duck.growth_stage='adult'
    for choice in ([],{},'missing'):
        check(not nest.request(p,'basic_nest',choice)[0],'malformed or unknown activity rejected')
    for identity in ([],{},3,'x'*129):
        check(not nest.request(p,'basic_nest','weave_rim',identity)[0],'malformed copy identity cannot fall back to a different nest')
    check(not nest.request(p,'basic_nest','rain_listen')[0],'uncovered nest never offers canopy listening')
    plan,key,obj=reset();arrive()
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age
        for cast,profile in PROFILES.items():
            resident='cast:'+cast;b.model.ensure(resident,profile.get('name',cast),profile)
            result=company.choose(b,plan,resident)
            check(result in company.SCORES,cast+' has a fitting companion role beside '+age)
            if profile['species'] in ('toad','butterfly','duckling'):check(result in ('lining_inspect','hover_observer','patient_company'),cast+' does not overreach with invented limbs beside '+age)
    g.duck.growth_stage='adult';b.model.residents[key]['mood']=.1
    check(company.choose(b,plan,key)=='patient_company','a gloomy visitor chooses patient company instead of energetic helping')
    for item in sorted(nest.NESTS):
        copies=own_native(item);identity=copies[0];obj=p.object_state(item,identity);source='structure' if item.endswith('_nest') and item not in ('golden_nest',) else 'decoration'
        check(obj['_source']==source,item+' retains its original inventory system')
        check(nest.request(p,item,'fluff_center',identity)[0],item+' accepts a command for its actual native source');finish()
        check(obj['uses']==1 and p.object_state(item,copies[1])['uses']==0,item+' leaves its second native copy alone')
    out=ROOT/'engine/artifacts/animation-milestone';(out/'nest-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=sorted(selected));(out/'nest-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
    if '--serve' in sys.argv:
        item='basic_nest';own_native(item);reply=None
        def emit():
            p._cache=None
            copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item,reply=reply))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];own_native(item)
            elif command.get('type')=='test_advance':
                until=command.get('until')
                if until=='finish':finish()
                else:
                    for _ in range(900):
                        advance();work=(p.state['plan'] or {}).get('residence',{}).get('routine',{})
                        if until=='contact' and work.get('contacts'):break
                        if until=='waiting' and company.waiting(b):break
            elif command.get('type')=='test_store':
                for room in g.decorations.rooms.values():
                    for placed in list(room.decorations):
                        if placed.instance_id==command['instance']:g.decorations.remove_decoration(room.room_type.value,placed.position)
                p.sync()
            elif command.get('type')=='pond':reply=p.command(command);p.sync()
            emit()
finally:
    p.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
