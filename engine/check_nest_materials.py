"""Actual-game bedding contacts, independent visitors and save boundaries."""
import os, sys, tempfile, copy, json, math
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-nest-materials-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host, nest_routines as routines, nest_materials as material, visitor_shelters, shelter_company
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import Weather, WeatherType, Season
from world.friends import visitor_animator
from audio.sound import sound_engine
sys.stdout=host.WIRE
checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    def reset(item='basic_nest',stage='adult'):
        p.cancel();g.duck.growth_stage=stage;g.duck.current_action=None;g.behavior_ai.clear_action()
        for need in ('hunger','energy','fun','cleanliness','social'):setattr(g.duck.needs,need,80)
        g.duck_store.sync_from_duck(g.duck)
        g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.7,1,datetime.now().isoformat())
        g.habitat.owned_items=[item,item];g.habitat.placed_items=[PlacedItem(item,10,6),PlacedItem(item,17,6)]
        for room in g.decorations.rooms.values():room.decorations=[]
        p.sync();p.hour=12;p.season='spring';p.weather_type='sunny';p.state['ecology'].update(temperature=18,snow=0)
        p.state['cooldowns'].clear();b.housing.clear();b.house_scenes.clear()
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=35;pos.y=21
        first,second=g.habitat.placed_items
        return first.instance_id,p.object_state(item,first.instance_id),p.object_state(item,second.instance_id)
    def step(dt=.2,capture=False):
        p.state['elapsed']+=dt;pos=g.renderer.duck_pos;pos._state_start_time-=dt;pos.update(dt);p._activity(dt)
        if capture:frames.append(snapshot(g,g.renderer))
    def arrive(item,identity):
        ok,message=p.start('rest',item,instance=identity)
        check(ok,'start actual nest visit: '+message)
        plan=p.state['plan']
        for _ in range(800):
            if plan['phase']=='act':return plan
            step()
        raise AssertionError('arrival timed out')
    # Every material-changing score crosses its real contacts, never on approach.
    for item in sorted(material.NESTS):
        for key,spec in routines.ROUTINES.items():
            if not spec.get('contacts'):continue
            iid,obj,twin=reset(item)
            before=copy.deepcopy(obj['nest']);plan=arrive(item,iid)
            check(obj['nest']==before,item+' no contact on the way in')
            gate=spec['when'];p.season=gate.get('season','spring')
            p.hour={'night':22,'dawn':6,'noon':12,'day':12}.get(gate.get('time'),12)
            p.weather_type={'wind':'windy','rain':'rainy','storm':'thunderstorm'}.get(gate.get('weather'),'sunny')
            p.state['ecology'].update(temperature=0 if gate.get('temperature')=='cold' else 30 if gate.get('temperature')=='hot' else 18,snow=1 if gate.get('snow') else 0)
            if gate.get('mood')=='grumpy':g.duck.needs.fun=20
            g.duck_store.sync_from_duck(g.duck)
            if gate.get('material'):obj['nest'][gate['material']]=1
            obj['bond']=.8;plan['residence']['routine']=dict(id=key,elapsed=0.,label=spec['label'],done=False)
            work=plan['residence']['routine'];other=copy.deepcopy(twin);uses=obj['uses']
            belongings=copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
            first=spec['contacts'][0]['at']*spec['duration']
            routines.advance(p,plan,first-.001)
            check(obj['nest']['touches']==0,key+' does not anticipate contact')
            for _ in range(math.ceil(spec['duration']/.2)+2):
                if work.get('done'):break
                step(capture=item=='basic_nest')
            check(work['done'] and not work.get('interrupted'),item+' finishes '+key)
            check(len(work['contacts'])==len(spec['contacts']),key+' crosses every contact once')
            check(obj['nest']['touches']==len(spec['contacts']),key+' no duplicate material movement')
            check(twin==other,key+' leaves another copy alone')
            check(obj['uses']==uses,key+' contacts grant no premature rest reward')
            check(belongings==(g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()),key+' materials are not duplicated inventory rewards')
    iid,obj,twin=reset();plan=arrive('basic_nest',iid)
    work=plan['residence']['routine']=dict(id='tuck_left_edge',elapsed=0.,label='Tucking the left edge',done=False)
    routines.advance(p,plan,10)
    check(obj['nest']['left']==1 and not work['done'],'tucked edge exists before the visit finishes')
    uses=obj['uses'];history=copy.deepcopy(obj.get('routines',{}));p.cancel()
    check(obj['nest']['left']==1 and obj['uses']==uses and obj.get('routines',{})==history,'cancel preserves physical tuck without a completion reward')
    saved=p.save();loaded=LivingPond(saved)
    check(loaded.object_state('basic_nest',iid)['nest']==obj['nest'],'exact nest material state survives load')
    loaded.minds.close()
    p.state['cooldowns'].clear();plan=arrive('basic_nest',iid)
    work=plan['residence']['routine']=dict(id='tamp_floor',elapsed=0.,label='Patting the lining',done=False)
    routines.advance(p,plan,4);first=copy.deepcopy(obj['nest']);clock=work['elapsed'];plan['paused']=True;step(20)
    check(obj['nest']==first and work['elapsed']==clock,'pausing freezes contacts and the acting clock')
    saved=p.save();loaded=LivingPond(saved);loaded.attach(g,offline=False)
    resumed=loaded.state['plan'];resumed['paused']=False
    routines.advance(loaded,resumed,3.3)
    check(loaded.object_state('basic_nest',iid)['nest']['touches']==first['touches']+1,'resuming fires only the next foot contact')
    loaded.minds.close();p.cancel()
    # Deposits follow actual weather and exposure, not winter/day labels.
    exposed={};covered={}
    material.update('basic_nest',exposed,600,True,'snowy',-3,.5,.8,'winter')
    material.update('deluxe_nest',covered,600,True,'snowy',-3,.5,.8,'winter')
    check(0<covered['nest']['snow']<exposed['nest']['snow'],'a canopy protects the bedding from most snowfall')
    dry={};material.update('basic_nest',dry,600,True,'sunny',-3,.2,.8,'winter')
    check(dry['nest']['snow']==dry['nest']['frost']==0,'cold dry sunshine does not invent snow or frost')
    frozen={};material.update('basic_nest',frozen,600,True,'rainbow',2,.2,.8,'winter')
    check(frozen['nest']['frost']==0,'rainbow is not freezing rain')
    initial=copy.deepcopy(exposed);material.update('basic_nest',exposed,900,False,'snowy',-3,1,1,'winter')
    check(exposed==initial,'stored bedding does not collect outdoor weather')
    material.update('basic_nest',exposed,600,True,'sunny',20,.2,.8,'winter')
    check(exposed['nest']['snow']<initial['nest']['snow'],'snow melts on a warm winter afternoon')
    invalid={'nest':{'left':float('nan'),'right':float('inf'),'touches':'oops'}}
    check(all(math.isfinite(v) for v in material.state(invalid).values()),'malformed legacy bedding normalizes to finite defaults')
    # A real guest chooses a covered nest and walks to its own reserved slot.
    iid,obj,twin=reset('deluxe_nest');g.atmosphere.current_weather=Weather(WeatherType.RAINY,.8,1,datetime.now().isoformat());p.sync()
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
    visitor_animator._position_x=45-g.renderer._camera_x;visitor_animator._position_y=20-g.renderer._camera_y;visitor_animator._last_move_time=0
    clock=0;paths=set();seen=set();completed=set()
    for _ in range(1800):
        clock+=.2;p.state['elapsed']+=.2
        visitor_animator._mind_motion=b.motion(friend.id)
        for kind in ('meeting','shelter'):
            reservation=visitor_animator._mind_motion.get(kind)
            if reservation:reservation['target']=[reservation['target'][0]-g.renderer._camera_x,reservation['target'][1]-g.renderer._camera_y]
        visitor_animator.update(clock,g.renderer.duck_pos.x-g.renderer._camera_x,g.renderer.duck_pos.y-g.renderer._camera_y)
        b.tick();paths.add(tuple(b.present.get(friend.id,[])))
        housing=b.housing.get(friend.id)
        if housing and housing.get('routine'):
            work=housing['routine'];seen.add(work['id'])
            if work['done']:completed.add(work['id'])
            if int(clock*5)%9==0:frames.append(snapshot(g,g.renderer))
    check(len(paths)>8,'visitor crosses real intermediate walking positions')
    check(housing and housing['phase']=='inside' and len(seen)>=5,'visitor selects varied personal routines after arriving')
    check(len(completed)>=4,'visitor genuinely completes several routines')
    check(b.model.residents[friend.id]['counts']['rest']==1,'a long stay learns one settling experience, not one per repeated routine')
    check(sum(obj.get('guest_routines',{}).values())>0 or sum(twin.get('guest_routines',{}).values())>0,'visitor routine history belongs to the physical nest')
    check(obj['uses']==twin['uses']==0,'visitor choreography does not farm Cheese item uses')
    check(p.start('rest',housing['id'],instance=housing['instance'])[0],'Cheese can reserve the other place beside an arrived visitor')
    shared=[];plan=p.state['plan']
    for _ in range(1400):
        clock+=.2;step();visitor_animator._mind_motion=b.motion(friend.id)
        for kind in ('meeting','shelter'):
            reservation=visitor_animator._mind_motion.get(kind)
            if reservation:reservation['target']=[reservation['target'][0]-g.renderer._camera_x,reservation['target'][1]-g.renderer._camera_y]
        visitor_animator.update(clock,g.renderer.duck_pos.x-g.renderer._camera_x,g.renderer.duck_pos.y-g.renderer._camera_y);b.tick()
        pair=shelter_company.for_actor(b,'cheese')
        if pair:
            shared.append(pair['performance'])
            check(not plan['residence'].get('routine') or plan['residence']['routine']['done'],'shared acting never overlaps Cheese’s solo routine')
            check(not housing.get('routine') or housing['routine']['done'],'shared acting never overlaps the visitor’s solo routine')
            if len(shared)%10==0:frames.append(snapshot(g,g.renderer))
    check(bool(shared),'real roommates use the quiet gaps for shared shelter moments')
    check(plan['residence']['slot']!=housing['slot'],'Cheese and guest retain separate nest places')
    p.cancel();b.house_scenes.clear()
    housing['routine']=dict(id='rain_listen',elapsed=2.,label=routines.ROUTINES['rain_listen']['label'],done=False)
    b.present[friend.id]=list(housing['destination'])
    check(friend.id not in shelter_company.residents(b),'an acting visitor cannot simultaneously start a shared scene')
    check('Listening to rain patter' in b.prompt(friend.id,'What are you doing?')[0]['content'],'speech describes the visitor’s actual nest routine')
    previous=copy.deepcopy(p.object_state(housing['id'],housing));g.habitat.store_item(housing['id'],housing['instance']);p.sync();visitor_shelters.tick(b,.2)
    check(friend.id not in b.housing,'storing the occupied nest releases its visitor')
    check(previous==p.object_state(housing['id'],housing),'removing the nest does not complete an interrupted action')
    from world.guest_cast import PROFILES
    for profile in PROFILES.values():
        choices=routines.visitor_choices(profile['species'])
        check(bool(choices) and choices<=set(routines.ROUTINES),profile['id']+' has authored physical shelter choices')
        if profile['species']=='butterfly':check(not choices&{'tamp_floor','foot_tuck','toe_trace','curl_sleep'},'butterfly never performs bill or webbed-foot nest actions')
        if profile['species']=='toad':check(not choices&{'stretch_wing','curl_sleep','heat_fan'},'toad never acts out feather or wing gestures')
    result=dict(result='PASS',checks=len(checks),frames=len(frames),visitorRoutines=sorted(seen),details=checks)
    out=ROOT/'engine/artifacts/animation-milestone'
    (out/'nest-materials-simulation.json').write_text(json.dumps(result,indent=2))
    (out/'nest-materials-frames.json').write_text(json.dumps(frames))
    samples=[]
    for item in sorted(material.NESTS):
        sample={};material.state(sample);before=copy.deepcopy(sample)
        for name in ('tuck_left_edge','tuck_right_edge','crossbrace_twig','straighten_feather','leaf_underlay','pick_grit','toe_trace'):
            spec=routines.ROUTINES[name];material.contacts(sample,{},spec,0,spec['duration'])
        settled=copy.deepcopy(sample)
        material.update(item,sample,2400,True,'snowy',-3,.3,.8,'winter')
        samples.append(dict(id=item,before=before,settled=settled,snow=sample))
    (out/'nest-materials-review.json').write_text(json.dumps(samples))
    print(json.dumps({k:result[k] for k in ('result','checks','frames','visitorRoutines')}))
finally:
    p.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
