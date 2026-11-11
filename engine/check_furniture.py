"""Furniture use with real arrival, visitor controllers, saves and interruption."""
import os,sys,tempfile,json,random,copy
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-furniture-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,furniture_rests,shelters
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import Weather,WeatherType,VISITORS
sys.stdout=host.WIRE;random.seed(19)
checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=10**9
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    g.habitat.owned_items.extend(furniture_rests.SEATS);p.sync();clock=0;friend=None
    def advance(n,brains=False,capture=True):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
            if brains:
                if g.friends.current_visit:
                    visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id)
                    visitor_animator.update(clock,pos.x,pos.y)
                g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*5)%5==0 and (p.state['plan'] or b.furnishings):
                frames.append(snapshot(g,g.renderer))
    def begin(item,desired=None,stage='adult',energy=90,hour=15,hot=False,autumn=False):
        p.cancel();b.furnishings.clear();b.seat_scenes.clear();b.seat_retry.clear();b.tasks.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None
        g.duck.growth_stage=stage;g.duck.needs.energy=energy;g.duck.needs.hunger=90
        g.duck_store.sync_from_duck(g.duck)
        g.day_night.get_current_hour=lambda:int(hour);g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        g.habitat.placed_items=[PlacedItem(item,10,6)];p.sync();b.sync()
        p.state['cooldowns']={};p.state['objects'][item].update(last_use=-1000,last_seat_routine=None)
        p.state['objects'][item]['seat_routines']={key:0 if key==desired else 10 for key in furniture_rests.ROUTINES} if desired else {}
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=46;pos.y=21
        ok,msg=p.start('item',item);check(ok,'start '+item+': '+msg)
        p.season='fall' if autumn else 'spring';p.state['ecology']['temperature']=29 if hot else 20
        for _ in range(500):
            advance(1)
            if p.state['plan'] and p.state['plan'].get('seat_routine'):break
        plan=p.state['plan'];check(bool(plan and plan.get('seat_routine')),item+' physically arrives before sitting')
        return plan,plan['seat_routine']
    cases=[('perch_watch','chair_wood',{}),('feather_settle','bean_bag',{}),('seat_doze','couch',{'energy':35}),
        ('wing_stretch','chair_wood',{}),('royal_inspection','golden_throne',{}),
        ('quilt_inspection','cushion',{}),('hammock_rock','hammock',{}),('star_seat','chair_throne',{'hour':22}),
        ('autumn_brush','garden_bench',{'autumn':True}),('summer_fan','sofa_fancy',{'hot':True}),
        ('careful_feet','cushion',{'stage':'elder'}),('little_lookout','chair_wood',{'stage':'hatchling'})]
    for key,item,args in cases:
        plan,r=begin(item,key,**args);before=p.state['objects'][item]['uses']
        check(r['id']==key,'context selects '+key+', got '+r['id'])
        check(key==r['id'] and r['label'] in json.dumps(b.prompt('cheese','How is the seat?')),'chat describes actual '+key)
        check(shelters.still_placed(p,plan['seating']),'using the actual placed copy of '+item)
        for _ in range(600):
            advance(1)
            if not p.state['plan']:break
        check(not p.state['plan'] and r['done'],key+' completes and gets up')
        check(p.state['objects'][item]['uses']==before+1,key+' grants one use')
        check(p.state['objects'][item]['seat_routines'][key]==1,key+' stores one real memory')
        after=g.duck.needs.energy;advance(20,capture=False)
        check(g.duck.needs.energy==after,key+' cannot repeat recovery after completion')
    plan,r=begin('couch');r0=r['elapsed'];plan['paused']=True;advance(20)
    check(r['elapsed']==r0,'pause freezes the actual seating clock')
    loaded=LivingPond(p.save());check(loaded.state['plan']['paused'] and not loaded.minds.furnishings,'loaded plans wait; visitor reservations are transient')
    plan['paused']=False;before=p.state['objects']['couch']['uses'];energy=g.duck.needs.energy
    g.habitat.placed_items=[];p.sync();advance(10)
    check(not p.state['plan'] and p.state['objects']['couch']['uses']==before and g.duck.needs.energy==energy,'removal cancels without use or recovery')
    plan,r=begin('hammock');p.weather_type='rainy';advance(1)
    check(not p.state['plan'],'rain ends an outdoor hammock rest')
    p.weather_type='sunny';g.duck.growth_stage='egg';p.state['cooldowns']={}
    check(not p.start('item','hammock')[0],'an egg cannot climb into a hammock')
    p.sync();g.duck.growth_stage='adult';g.habitat.placed_items=[];p.sync()
    check(not p.start('item','chair_wood')[0],'owned but unplaced chairs cannot be used')
    for stage in shelters.AGES[1:]:
        plan,r=begin('cushion',stage=stage);check(plan['seating']['slot']==0,'real reserved seat for '+stage);p.cancel()
    # A regular friend, rare goose and Pip reserve actual independent furniture.
    plan,r=begin('couch',energy=40)
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
    visitor_animator._position_x=70;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    rare=VISITORS['friendly_goose'];g.atmosphere.current_visitor=(rare,datetime.now().isoformat())
    g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=72,y=23)
    p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=86,y=23)
    g.habitat.placed_items.extend([PlacedItem('garden_bench',18,6),PlacedItem('cushion',2,6)]);p.sync();b.sync()
    for key in b.present:
        if key!='cheese':b.model.residents[key]['energy']=.4
    b.tick()
    check(len(b.furnishings)==3,'ordinary guest, rare goose and Pip choose their own available seats')
    reservations=[(r['id'],tuple(r['destination']),r['slot']) for r in b.furnishings.values()]
    reservations.append((plan['seating']['id'],tuple(plan['destination']),plan['seating']['slot']))
    check(len(set(reservations))==4,'all arrivals reserve distinct physical slots')
    destinations={key:list(r['destination']) for key,r in b.furnishings.items()}
    paths={key:set() for key in b.furnishings};shared=set();seen_inside=set();completed=set();starts={key:b.model.residents[key]['counts']['rest'] for key in paths}
    for _ in range(650):
        advance(1,True)
        for key in paths:
            if key in b.present:paths[key].add(tuple(round(v,3) for v in b.present[key]))
            if key not in b.furnishings and key in seen_inside and key not in completed:
                check(b.model.residents[key]['counts']['rest']==starts[key]+1,key+' earns exactly one experience on getting up')
                completed.add(key)
        for key,r in b.furnishings.items():
            assert r['destination']==destinations[key],key+' keeps a fixed furniture destination'
            if r['phase']=='inside':seen_inside.add(key)
        for scene in b.seat_scenes.values():
            seated=furniture_rests.inside(b)
            assert scene['a'] in seated and scene['b'] in seated
            shared.add((scene['a'],scene['b'],scene['id']))
    check(seen_inside==set(paths),'all visitor types really arrive before resting: '+repr((seen_inside,set(paths),b.furnishings,b.present)))
    check(all(len(path)>5 for path in paths.values()),'all visitor types walk through intermediate positions')
    check(bool(shared) and any('cheese' in s[:2] for s in shared),'Cheese and a neighbor share an actually occupied seat')
    check(completed==set(paths),'each visitor completes a real furniture rest')
    check(all(key not in b.furnishings for key in paths),'everyone gets up and resumes independent life')
    check(bool(p.state['objects']['couch']['seat_routines'].get('synchronized_sigh')),'the completed shared pause becomes an object memory')
    check(not LivingPond(p.save()).minds.seat_scenes,'loading never resurrects old shared partners')
    saved=p.save();check(LivingPond(saved).state['objects']['couch']['seat_routines']==p.state['objects']['couch']['seat_routines'],'completed furniture memories survive saves')
    # Replacing the current visit may reuse its name, but not its old arrival.
    b.seat_retry.clear();b.tasks.clear();b.sync()
    for key in b.present:
        if key!='cheese':b.model.residents[key]['energy']=.3
    b.tick();old=b.furnishings[friend.id];before=b.model.residents[friend.id]['counts']['rest']
    g.friends.current_visit.started_at='replacement-visit';advance(1,True)
    check(b.furnishings.get(friend.id) is not old,'replacement visits cannot inherit a chair')
    check(b.model.residents[friend.id]['counts']['rest']==before,'replacement visit grants no old rest reward')
    b.seat_retry.clear();b.tick();visitor_animator.start_leaving();advance(1,True)
    check(friend.id not in b.furnishings,'departure releases the seat immediately')
    # Change weather while remaining visitors are in transit or seated.
    starts={key:b.model.residents[key]['counts']['rest'] for key in b.furnishings}
    p.weather_type='rainy';g.atmosphere.current_weather=Weather(WeatherType.RAINY,.7,1,datetime.now().isoformat());advance(1,True)
    check(not b.furnishings and not b.seat_scenes,'bad weather releases all seats and shared scenes')
    check(all(b.model.residents[key]['counts']['rest']==n for key,n in starts.items()),'interrupted visitors receive no furniture completion')
    shared_scores=[]
    def shared_begin(desired,hour=15,energy=90):
        plan,r=begin('sofa_fancy',energy=energy,hour=hour)
        obj=p.state['objects']['sofa_fancy']
        obj['seat_routines']={key:0 if key==desired else 10 for key in furniture_rests.ROUTINES}
        g.friends.start_visit(friend.id)
        visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
        visitor_animator._position_x=70;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
        b.sync();b.model.residents[friend.id]['energy']=.4;b.tick()
        for _ in range(300):
            advance(1,True)
            if b.seat_scenes:break
        check(bool(b.seat_scenes),'independent arrivals start '+desired)
        scene=next(iter(b.seat_scenes.values()))
        check(scene['id']==desired,'shared conditions select '+desired+', got '+scene['id'])
        return plan,scene
    for key,hour,energy in [('bench_gossip',15,90),('shared_view',15,90),
                            ('synchronized_sigh',15,40),('star_companions',22,90)]:
        plan,seat_scene=shared_begin(key,hour,energy)
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',friend.id)}
        snap=p.snapshot();old=copy.deepcopy(snap);advance(1,True);fresh=p.snapshot()
        check(snap==old and fresh['plan']['seat_routine']['elapsed']>snap['plan']['seat_routine']['elapsed'],'fresh snapshots advance '+key+' without mutating old frames')
        for _ in range(400):
            advance(1,True)
            if not b.seat_scenes:break
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),key+' teaches both real participants once')
        check(p.state['objects']['sofa_fancy']['seat_routines'][key]==1,key+' records one completed moment')
        shared_scores.append(key)
        advance(30,True)
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),key+' does not immediately repeat')
    plan,seat_scene=shared_begin('bench_gossip')
    before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',friend.id)}
    plan['paused']=True;advance(1,True)
    check(not b.seat_scenes,'pausing Cheese releases a shared seating scene')
    check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),'interrupted shared rest grants no shared experience')
    plan['paused']=False;advance(1,True)
    check(not b.seat_scenes,'resuming does not restart an already interrupted shared scene')
    plan,seat_scene=shared_begin('bench_gossip')
    uses=p.state['objects']['sofa_fancy']['uses'];before=b.model.residents[friend.id]['counts']['rest']
    g.habitat.placed_items=[];p.sync();advance(1,True)
    check(not b.furnishings and not b.seat_scenes and not p.state['plan'],'removing a shared sofa releases both participants')
    check(p.state['objects']['sofa_fancy']['uses']==uses and b.model.residents[friend.id]['counts']['rest']==before,'removed shared furniture grants no item use or rest')
    out=ROOT/'engine/artifacts/animation-milestone'
    result={'result':'PASS','checks':len(checks),'nativeFrames':len(frames),'soloScores':len(cases),'sharedScores':shared_scores,'sharedObserved':[list(s) for s in shared],'details':checks}
    (out/'furniture-simulation.json').write_text(json.dumps(result,indent=2));(out/'furniture-frames.json').write_text(json.dumps(frames))
    print(json.dumps({k:v for k,v in result.items() if k!='details'}))
finally:
    b.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
