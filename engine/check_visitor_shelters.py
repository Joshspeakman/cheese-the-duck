"""Physical visitor sheltering with actual movement controllers and camera shifts."""
import os,sys,tempfile,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-guest-shelters-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,shelters,visitor_shelters,shelter_company
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import VISITORS,Weather,WeatherType
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
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    g.renderer._camera_x=g.renderer._camera_y=0
    pos=g.renderer.duck_pos;pos.x=15;pos.y=12
    visitor_animator._position_x=50;visitor_animator._position_y=18;visitor_animator._target_x=65;visitor_animator._target_y=21
    visitor_animator._mind_motion={'meeting':{'target':[65,21],'facing':True}}
    before=(visitor_animator._position_x,visitor_animator._position_y)
    pos.x=95;pos.y=30;g.renderer._update_camera(44,14)
    check((visitor_animator._position_x+g.renderer._camera_x,visitor_animator._position_y+g.renderer._camera_y)==before,'camera scrolling preserves a regular visitor’s world position')
    check([visitor_animator._target_x+g.renderer._camera_x,visitor_animator._target_y+g.renderer._camera_y]==[65,21],'camera scrolling preserves the walking destination')
    check([visitor_animator._mind_motion['meeting']['target'][0]+g.renderer._camera_x,visitor_animator._mind_motion['meeting']['target'][1]+g.renderer._camera_y]==[65,21],'camera changes translate reservation targets once')
    visitor_animator._mind_motion={}
    g.renderer._viewport_width=44;g.renderer._viewport_height=14
    g.habitat.owned_items.extend(['barn','gazebo','dog_house','cozy_nest','birdhouse'])
    g.habitat.placed_items=[PlacedItem('barn',10,5),PlacedItem('gazebo',17,5),PlacedItem('dog_house',2,5),PlacedItem('cozy_nest',4,11),PlacedItem('birdhouse',17,11)]
    g.atmosphere.current_weather=Weather(WeatherType.RAINY,.8,1,datetime.now().isoformat())
    p.sync();pos.x=62;pos.y=18
    check(p.start('rest','barn')[0],'Cheese reserves a real place in the barn')
    check(p.state['plan']['residence']['slot']==0,'the first occupant claims the first slot')
    visitor_animator._position_x=73-g.renderer._camera_x;visitor_animator._position_y=21-g.renderer._camera_y
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._last_move_time=0
    rare=VISITORS['friendly_goose'] if isinstance(VISITORS,dict) else next(v for v in VISITORS if v.id=='friendly_goose')
    g.atmosphere.current_visitor=(rare,datetime.now().isoformat());g.guest_motion.tick(g,0);g.guest_motion.actor.update(x=76,y=21)
    p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,0);g.story_motion.actor.update(x=89,y=20)
    b.sync();b.tick()
    check(len(b.housing)==3,'regular friend, rare visitor and story duckling each choose shelter')
    check(all(r['id'] not in ('cozy_nest','birdhouse') for r in b.housing.values()),'uncovered nests and wildlife birdhouses are excluded')
    reservations=[(r['id'],tuple(r['destination']),r['slot']) for r in b.housing.values()]
    reservations.append(('barn',tuple(p.state['plan']['destination']),p.state['plan']['residence']['slot']))
    check(len(set(reservations))==4,'simultaneous arrivals reserve separate places')
    destinations={k:list(r['destination']) for k,r in b.housing.items()}
    check(any(r['id']!='barn' for r in b.housing.values()),'a full barn sends another visitor to a different shelter')
    check(not b.house_scenes,'approaching residents cannot perform a shared shelter moment')
    paths={k:set() for k in b.housing};clock=0;company=[];company_frames=[]
    def advance(n):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
            visitor_animator._mind_motion=b.motion(friend.id)
            for kind in ('meeting','shelter'):
                reservation=visitor_animator._mind_motion.get(kind)
                if reservation:reservation['target']=[reservation['target'][0]-g.renderer._camera_x,reservation['target'][1]-g.renderer._camera_y]
            visitor_animator.update(clock,pos.x-g.renderer._camera_x,pos.y-g.renderer._camera_y)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            for pair in b.house_scenes.values():
                inside=shelter_company.residents(b)
                assert pair['a'] in inside and pair['b'] in inside,'shared acting requires two real arrivals'
                company.append((pair['a'],pair['b'],pair['performance']))
                if len(company_frames)<60 and int(clock*5)%5==0:company_frames.append(snapshot(g,g.renderer))
            for key in paths:
                if key in b.present:paths[key].add(tuple(round(v,3) for v in b.present[key]))
    advance(500)
    check(all(r['phase']=='inside' for r in b.housing.values()),'every guest arrives and enters using its real movement controller: '+str(b.housing))
    check(all(len(path)>5 for path in paths.values()),'every guest crosses intermediate positions instead of teleporting')
    check(all(r['destination']==destinations[k] for k,r in b.housing.items()),'shelter targets stay independent of Cheese')
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    company_frames.clear()
    fixed=copy.deepcopy(b.present);advance(1000)
    check(all(visitor_shelters.distance(b.present[k],destinations[k])<.8 for k in b.housing),'long waits keep actual visitors inside their reserved shelter')
    check(all(r['recovered']<=.080001 for r in b.housing.values()),'shelter recovery is bounded per visit')
    check(bool(company),'sheltered residents perform actual shared moments')
    check(any('cheese' in pair[:2] for pair in company),'Cheese participates while genuinely waiting inside his house')
    check(len({key for pair in company for key in pair[:2]})>=3,'three roommates take turns instead of excluding the third')
    check(all(b.model.residents[k]['counts']['share']<=3 for k in b.present),'a long wait cannot repeatedly farm shared experience')
    for _ in range(250):
        if shelter_company.for_actor(b,'cheese'):break
        advance(1)
    check(bool(shelter_company.for_actor(b,'cheese')),'an ongoing shared scene can be interrupted')
    learned=b.model.residents['cheese']['counts']['share'];plan=p.state['plan'];plan['paused']=True
    advance(1)
    check(not shelter_company.for_actor(b,'cheese'),'pausing Cheese’s plan cancels his shared acting')
    check(b.model.residents['cheese']['counts']['share']==learned,'an interrupted shared scene grants no experience')
    plan['paused']=False
    observed={pair[2] for pair in company if 'cheese' in pair[:2]}
    check(any(m['kind']=='experience' and any(shelter_company.SCORES[k]['note'] in m['text'] for k in observed) for m in b.model.residents['cheese']['memories']),'an actually completed shared moment becomes a persistent memory')
    p.weather_type='blizzard'
    check('thunder_reassure' not in shelter_company.available_scores(b,'cheese',friend.id),'snow never invents thunder')
    p.weather_type='rainy'
    saved=p.save();loaded=LivingPond(saved)
    check(not loaded.minds.housing,'loading never resurrects stale transient visitor occupancy')
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    frames=[]
    for _ in range(15):advance(1);frames.append(snapshot(g,g.renderer))
    (ROOT/'engine/artifacts/animation-milestone/visitor-shelter-frames.json').write_text(json.dumps(frames))
    (ROOT/'engine/artifacts/animation-milestone/shelter-company-frames.json').write_text(json.dumps(company_frames))
    check('Waiting out the weather' in b.prompt(friend.id,'Are you getting wet?')[0]['content'],'chat knows the guest is genuinely under cover')
    old=b.housing[friend.id];learned=b.model.residents[friend.id]['counts']['rest']
    g.friends.current_visit.started_at='replacement-visit';advance(1)
    check(b.housing.get(friend.id) is not old,'a replacement visit cannot inherit the old reservation')
    check(b.model.residents[friend.id]['counts']['rest']==learned,'replacement visit does not claim a completed shelter experience')
    visitor_animator.start_leaving();advance(1)
    check(friend.id not in b.housing,'departure takes priority over sheltering')
    check(not shelter_company.for_actor(b,friend.id),'departure also cancels shared shelter acting')
    departing_x=visitor_animator._position_x;advance(8)
    check(visitor_animator._position_x!=departing_x,'a departing visitor actually walks away')
    # Removing the rare guest’s shelter releases the old reservation, then a
    # different reachable place can be chosen without a false completion.
    old=b.housing[rare.id];old_rest=b.model.residents[rare.id]['counts']['rest']
    g.habitat.placed_items=[i for i in g.habitat.placed_items if not (i.item_id==old['id'] and shelters.position(i)==old['destination'])]
    p.sync();advance(1)
    check(b.housing.get(rare.id) is not old,'removed shelter releases its occupant')
    check(b.model.residents[rare.id]['counts']['rest']==old_rest,'removed shelter grants no completion')
    advance(500)
    check(all(r['phase']=='inside' for r in b.housing.values()),'remaining guests relocate to available shelter')
    before={k:b.model.residents[k]['counts']['rest'] for k in b.housing}
    p.weather_type='sunny';g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    advance(20)
    check(not b.housing,'clear weather lets the visitors step back outside')
    check(not b.house_scenes,'weather exits cancel unfinished shared moments')
    check(all(b.model.residents[k]['counts']['rest']==n+1 for k,n in before.items()),'each completed shelter wait teaches one real experience')
    after={k:b.model.residents[k]['counts']['rest'] for k in before};advance(4)
    check(all(b.model.residents[k]['counts']['rest']==n for k,n in after.items()),'shelter completion is never repeated')
    result={'result':'PASS','checks':len(checks),'details':checks}
    (ROOT/'engine/artifacts/animation-milestone/visitor-shelter-simulation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'result':'PASS','checks':len(checks)}))
finally:
    b.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
