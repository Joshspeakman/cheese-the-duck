"""Actual regular/rare/story arrivals, shared ground work and interrupted memories."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-ground-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,groundworks,ground_company as company
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

    def advance(n=1,capture=False,move=True):
        global clock
        for _ in range(n):
            clock+=.1;p.state['elapsed']+=.1;pos=g.renderer.duck_pos;pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
            if g.friends.current_visit and move:
                visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%10==0:frames.append(snapshot(g,g.renderer))
    def reset(item='marble_tiles',kind='regular',stage='adult'):
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.cancel();b.ground_helpers.clear();b.ground_retry.clear();b.textile_helpers.clear();b.textile_retry.clear();b.readers.clear();b.creators.clear();b.tasks.clear();b.housing.clear();b.furnishings.clear();b.gardening.clear();b.musicians.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None;g.guest_motion.actor=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item=='stone_path':g.building.structures=[Structure(item,(8,6),status=StructureStatus.COMPLETE)]
        elif groundworks.ITEMS[item]['portable']:g.materials.add_material(item,1)
        else:g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None;obj=p.object_state(item,iid);obj['last_use']=-1000;obj['uses']=0;obj['dirt']=0;obj['wetness']=0;obj['ground'].update(powder=.8,frost=0,tracks=[],furrows=[]);obj['ground_routines']={}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan'];dest=plan.get('destination',plan['ground_work']['origin']);start=[dest[0]+19,dest[1]]
        if kind=='regular':
            g.friends.start_visit(friend.id);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
            visitor_animator._position_x=start[0];visitor_animator._position_y=start[1];visitor_animator._last_move_time=clock;key=friend.id
        elif kind!='story':
            key='friendly_goose' if kind=='rare' else kind;g.atmosphere.current_visitor=(VISITORS[key],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=start[0],y=start[1])
        else:
            key='story:pip';p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=start[0],y=start[1])
        b.sync();b.model.residents[key]['energy']=.9;b.model.residents[key]['mood']=.7;b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
        return plan,key,obj
    def arrive(capture=False):
        for _ in range(1200):
            advance(capture=capture)
            r=company.active(b)
            if r and r['phase']=='inside':return r
            if not p.state['plan']:break
        raise AssertionError('friend did not arrive to help')
    def finish(capture=False):
        for _ in range(1400):
            advance(capture=capture)
            if not p.state['plan'] and not b.ground_helpers:return
        raise AssertionError('ground work did not finish')
    # Native and renderer must sample the same material coordinates for both roles.
    payload=[dict(id=s['preview'],elapsed=groundworks.ROUTINES[s['preview']]['duration']*i/100,duet=key,company=dict(id=key,role='b')) for key,s in company.SCORES.items() for i in range(101)]
    script="import {groundPose} from './engine/client/ground-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>{let p=groundPose(w);return {u:p.actorU,v:p.actorV,press:p.actorPress,contact:p.contact,ownerU:p.u,ownerV:p.v}})))"
    samples=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
    check(all(all(abs(a[k]-v)<1e-9 for k,v in company.controls(w,w['duet']).items()) and abs(a['ownerU']-groundworks.controls(w)['u'])<1e-9 and abs(a['ownerV']-groundworks.controls(w)['v'])<1e-9 for w,a in zip(payload,samples)),str(len(payload))+' shared contact samples agree between native and renderer')
    for index,(score,spec) in enumerate(company.SCORES.items()):
        kind='butterfly_fairy' if score=='hover_observer' else ('regular','rare','story')[index%3]
        plan,key,obj=reset(spec['item'],kind);plan['ground_work']['id']=spec['preview'];plan['ground_work']['label']=groundworks.ROUTINES[spec['preview']]['label']
        # Use an adult partner for pattern/footwork roles; the separate lifecycle
        # cases below exercise young story visitors' deliberately patient role.
        if kind=='story' and score not in ('careful_company','lava_edge_pair','cloud_shapes','rainbow_colors','galaxy_patient','galaxy_watch','ice_bubbles','stone_spotter','winding_guide','joint_sweep','sand_rake_pair','sand_track_compare','sand_smooth_pair','snow_prints','snow_crystal_watch'):
            plan,key,obj=reset(spec['item'],'regular');plan['ground_work']['id']=spec['preview']
        b.model.residents[key]['traits']['confidence']=.8 if score=='mosaic_story' else .2
        b.model.residents[key]['traits']['patience']=.9 if score=='galaxy_patient' else .2
        obj['wetness']=.3 if score in ('pebble_echo','checker_echo') else 0
        if score=='joint_sweep':obj['dirt']=.8
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)};uses=obj['uses'];positions=set();r=None;waiting_checked=False;approach_checked=False
        for _ in range(1000):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]));r=company.active(b)
            if r and r['phase'] in ('approach','enter') and plan['phase']=='act' and not waiting_checked:check(plan['ground_work']['elapsed']==0,score+' waits for the arriving partner');waiting_checked=True
            if r and r['phase']=='approach' and not approach_checked:
                approach_checked=True;facts=json.loads(b.prompt(key,'What are you making together?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check('ground_work' not in facts,score+' does not report nearby surface facts before arrival')
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(positions)>3,score+' has an independent physical arrival')
        check(r['score']==score,score+' selected from actual material, age and temperament: '+r['score'])
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),score+' arrival alone earns no shared learning')
        advance(40,capture=True);owner=p._plan_view()['ground_work'];guest=company.snapshot(b)[0]['routine']
        check(owner['elapsed']==guest['elapsed'] and owner['company']['role']=='a' and guest['company']['role']=='b',score+' shares one native clock with distinct roles')
        finish(capture=True)
        check(obj['uses']==uses+1,score+' does not duplicate the original item use')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),score+' both residents learn exactly once at completion')
        check(obj.get('ground_company',{}).get(score)==1,score+' is recorded on the actual physical copy')
        if score=='sand_rake_pair':
            marks=obj['ground']['furrows'];check(len(marks)==6 and {t['by'] for t in marks}=={'cheese',key},'both authors retain three physical furrows')
            check(all(t['u1']<=.45 if t['by']=='cheese' else t['u0']>=.64 for t in marks),'the two rake paths have separate lanes')
            check(all(any('two separate sets' in m['text'] for m in b.model.residents[k]['memories']) for k in ('cheese',key)),'both remember the two sets of furrows they actually made')
        if score=='snow_prints':check(len(obj['ground']['tracks'])==7 and {t['by'] for t in obj['ground']['tracks']}=={'cheese',key},'seven snow impressions belong to their actual makers')
        if score=='hover_observer':check(all(t['by']=='cheese' for t in obj['ground']['furrows']),'flying observers make no invented raking contacts')
        after={k:b.model.residents[k]['counts']['share'] for k in before};company.complete(b,plan)
        check(all(b.model.residents[k]['counts']['share']==v for k,v in after.items()),score+' cannot repeat a completion')
    # A delayed frame must not release native movement during the exit gesture.
    plan,key,obj=reset('galaxy_floor');r=arrive();before=b.model.residents[key]['counts']['share']
    for _ in range(1000):
        advance()
        if plan['phase']=='settle':break
    check(plan['phase']=='settle','shared work reaches its exit gesture before completion')
    pos=g.renderer.duck_pos;anchor=(pos.x,pos.y);pos._state_start_time-=60
    pos.update(.3);pos.update(.3)
    check(pos.get_state()!='idle' and (pos.x,pos.y)==anchor,'a wall-clock delay cannot trigger wandering during settling')
    finish();check(b.model.residents[key]['counts']['share']==before+1,'settling after a delayed frame preserves the actual shared memory')
    # Different species leave different actual prints, and conversation can name them.
    for cast,shape in [('grumpy_toad','toad'),('mysterious_crow','talon'),('friendly_goose','webbed')]:
        plan,key,obj=reset('sand_floor',cast);plan['ground_work']['id']='sand_tracks';r=arrive()
        while len([t for t in obj['ground']['tracks'] if t['by']==key])<2:advance(capture=True)
        check(all(t['shape']==shape for t in obj['ground']['tracks'] if t['by']==key),cast+' leaves its own kind of footprint')
        facts=json.loads(b.prompt(key,'What marks have we made?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
        check(any(x['shape']==shape and x['name']==b.model.residents[key]['name'] for x in facts['ground_work']['footprint_trails']),cast+' speech receives its observed trail')
        finish(capture=True)
        check(any(shape+' prints' in m['text'] for m in b.model.residents[key]['memories']),cast+' remembers the actual mark shape')
    for stage in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset('marble_tiles',stage=stage);r=arrive(capture=stage in ('hatchling','elder'))
        expected='careful_company' if stage in ('hatchling','duckling','elder','legendary') else company.choose(b,plan,key)
        check(r['score']==expected,stage+' receives matching company');finish()
    p.cancel();g.duck.growth_stage='egg';check(not p.start('item','marble_tiles')[0],'an egg cannot start a shared floor walk');g.duck.growth_stage='adult'
    plan,key,obj=reset();b.model.residents[key]['mood']=.1;check(company.choose(b,plan,key)=='careful_company','low mood favors quiet patient company')
    b.model.residents[key]['mood']=.7;b.model.residents[key]['energy']=.35;check(company.choose(b,plan,key)=='careful_company','tired guests choose less demanding company')
    plan,key,obj=reset();p.hour=23;r=arrive();check(r['score']=='night_edge','night chooses a quiet shared edge view');p.cancel();advance()
    plan,key,obj=reset('sand_floor');r=arrive();advance(60);before=copy.deepcopy(obj);clock_before=plan['ground_work']['elapsed'];overlap=r['overlap'];plan['paused']=True;advance(50)
    check(obj==before and plan['ground_work']['elapsed']==clock_before and r['overlap']==overlap,'pause freezes both actors and their material')
    saved=LivingPond(p.save());check(not saved.minds.ground_helpers and saved.state['plan']['paused'],'save restores material work without phantom helper reservations');saved.minds.close()
    facts=json.loads(b.prompt(key,'What are we working on?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check(facts['shared_activity']['status']=='paused' and facts['ground_work']['material']=='sand','paused speech describes the actual nearby surface')
    visitor_animator._position_x+=8;b.sync();check(company.snapshot(b)==[],'paused displaced guest is not drawn back onto the surface')
    facts=json.loads(b.prompt(key,'Are you next to Cheese?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check('shared_activity' not in facts and 'ground_work' not in facts,'displaced visitor cannot claim the old shared work');b.tick();check(not b.ground_helpers,'displacement releases the reservation')
    plan,key,obj=reset();before=b.model.residents[key]['counts']['share'];advance(330,move=False)
    check(not b.ground_helpers and plan['ground_work']['elapsed']>0,'unreachable partner times out and Cheese continues alone');finish();check(b.model.residents[key]['counts']['share']==before,'missed invitation grants no shared learning')
    for reason in ('depart','new_visit','storm','care','move','replace'):
        plan,key,obj=reset();r=arrive();advance(40);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='depart':g.friends.current_visit=None
        elif reason=='new_visit':g.friends.current_visit.started_at='replacement-visit'
        elif reason=='storm':p.weather_type='stormy'
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        else:g.habitat.placed_items=[PlacedItem('marble_tiles',10,6)];p.sync()
        advance(3)
        check(not b.ground_helpers and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' interrupts without claiming a shared completion')
    # Cleaning and smoothing affect only their own copy/half, at real contact.
    plan,key,obj=reset('stone_tiles');obj['dirt']=.8;plan['ground_work']['id']='seam_brush';g.habitat.placed_items[0].x=6;g.habitat.placed_items.append(PlacedItem('stone_tiles',14,6));p.sync()
    p.cancel();p.state['cooldowns']={};obj['last_use']=-1000;p.start('item','stone_tiles',instance=g.habitat.placed_items[0].instance_id);plan=p.state['plan'];other=p.object_state('stone_tiles',g.habitat.placed_items[1].instance_id);other['dirt']=.8
    # Move the existing visitor near the newly selected left copy before the invitation.
    visitor_animator._position_x=plan['destination'][0]+18;visitor_animator._position_y=plan['destination'][1];b.sync();b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
    r=arrive();before=b.model.residents[key]['counts']['share'];uses=obj['uses']
    while not r['events']:advance()
    check(abs(obj['dirt']-.75)<1e-9 and other['dirt']==.8,'helper brush changes only the selected copy after contact')
    p.cancel();advance(3);check(abs(obj['dirt']-.75)<1e-9 and obj['uses']==uses and b.model.residents[key]['counts']['share']==before,'cancel retains only the cleaning already performed')
    plan,key,obj=reset('sand_floor');plan['ground_work']['id']='sand_smooth';obj['ground']['tracks']=[dict(u=.25,v=.5,life=1,by='cheese',shape='webbed'),dict(u=.8,v=.5,life=1,by=key,shape='webbed')];r=arrive()
    while not r['events']:advance()
    check(len(obj['ground']['tracks'])==1 and obj['ground']['tracks'][0]['u']==.25,'helper smooths only the right-hand trail');finish();check(not obj['ground']['tracks'],'Cheese later clears the left-hand trail')
    # Save after real paired contact: retain both authors, not their reservation.
    plan,key,obj=reset('sand_floor');r=arrive()
    while not r['events']:advance()
    before=copy.deepcopy(obj['ground']);plan['paused']=True;g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;b=p.minds;p.sync()
    loaded=p.object_state('sand_floor',plan['instance']);check(not b.ground_helpers and p.state['plan']['paused'] and loaded['ground']==before,'full save preserves both physical marks and discards old helper')
    p.state['plan']['paused']=False;advance(10);check(not b.ground_helpers and p.state['plan']['ground_work']['duet']=='sand_rake_pair','resume keeps the drawing lane without reinviting or duplicating contacts')
    for core in ('wet_footing','frost_edge'):
        plan,key,obj=reset('stone_tiles');plan['ground_work']['id']=core;check(company.choose(b,plan,key) is None,'no shared invitation during '+core)
    for item in groundworks.ITEMS:
        plan,key,obj=reset(item)
        for cast,profile in PROFILES.items():
            b.model.ensure('cast:'+cast,profile.get('name',cast),profile)
            check(company.choose(b,plan,'cast:'+cast) in company.SCORES,cast+' has an eligible role for '+item)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'ground-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(company.SCORES));(out/'ground-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
