"""Real arrivals, joint toy use, interruption and bounded learning."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-playdates-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,playdates
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import Weather,WeatherType,VISITORS
sys.stdout=host.WIRE
random.seed(63)
checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.duck.growth_stage='adult';g.renderer._show_talk=False
    p=g.living_pond;p.state['auto']=False;b=p.minds;b.model.state['next_social']=10**9
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._last_move_time=0
    g.renderer._camera_x=g.renderer._camera_y=0;g.renderer._viewport_width=132;g.renderer._viewport_height=42
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    g.habitat.owned_items.extend(playdates.TOYS);g.habitat.placed_items=[];p.sync();clock=0;paths=set()
    def advance(n):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2)
            b.sync();p._activity(.2)
            visitor_animator._mind_motion=b.motion(friend.id)
            for kind in ('meeting','shelter'):
                r=visitor_animator._mind_motion.get(kind)
                if r:r['target']=[r['target'][0]-g.renderer._camera_x,r['target'][1]-g.renderer._camera_y]
            visitor_animator.update(clock,pos.x-g.renderer._camera_x,pos.y-g.renderer._camera_y)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            paths.add((round(visitor_animator._position_x,3),round(visitor_animator._position_y,3)))
            company=p.state.get('plan',{}).get('company') if p.state.get('plan') else None
            if company and company['phase'] in ('enter','act','exit') and int(clock*5)%5==0:frames.append(snapshot(g,g.renderer))
    def begin(item):
        if p.state['plan']:p.cancel()
        g.habitat.placed_items=[PlacedItem(item,10,7)];p.sync();p.state['cooldowns']={};p.state['objects'][item]['last_use']=-1000
        g.duck.growth_stage='adult';g.duck.needs.energy=90;g.duck.needs.hunger=90
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.set_state_by_name('idle',0);pos.x=46;pos.y=24
        visitor_animator._position_x=92;visitor_animator._position_y=28;visitor_animator._is_leaving=False;visitor_animator._mind_motion={}
        b.sync();b.model.residents[friend.id]['energy']=.8;b.model.residents[friend.id]['social']=.8
        ok,msg=p.start('item',item);check(ok,'start owned placed '+item+': '+msg)
        for _ in range(500):
            advance(1)
            if p.state['plan'].get('company'):break
        check(bool(p.state['plan'].get('company')),item+' invites a real nearby guest')
        return p.state['plan'],p.state['plan']['company']
    for item in ['toy_seesaw','toy_sandbox','toy_ball','toy_trampoline']:
        plan,company=begin(item);old=b.model.residents['cheese']['counts']['share'];paths.clear()
        check(company['phase']=='approach' and company['elapsed']==0,item+' does not act before the guest arrives')
        check(company['spot']!=[g.renderer.duck_pos.x,g.renderer.duck_pos.y],item+' reserves an independent partner destination')
        for _ in range(600):
            advance(1)
            if company.get('done'):break
        check(company['phase']=='done',item+' completes actual joint play')
        check(len(paths)>5,item+' guest reaches the toy through intermediate positions')
        check(b.model.residents['cheese']['counts']['share']==old+1,item+' teaches exactly one shared experience')
        advance(60)
        check(b.model.residents['cheese']['counts']['share']==old+1,item+' never repeats the completed reward')
        check(p.state['plan'] is None,item+' releases Cheese back to ordinary movement')
    check(p.state['objects']['toy_sandbox'].get('sandwork') in ('sandbox_castle','sandbox_channels'),'finished sand work persists in the object state')
    plan,company=begin('toy_seesaw');old=b.model.residents['cheese']['counts']['share']
    for _ in range(300):
        advance(1)
        if company['phase']=='act':break
    check(company['phase']=='act','interruption fixture reaches physical paired play')
    saved=p.save();loaded=LivingPond(saved)
    check('company' not in loaded.state['plan'] and loaded.state['plan']['paused'],'save reload never resurrects an old visitor reservation')
    company_elapsed=company['elapsed'];plan['paused']=True;advance(10)
    check(company['elapsed']==company_elapsed,'pausing does not advance the shared score')
    plan['paused']=False;uses=p.state['objects']['toy_seesaw']['uses'];g.habitat.placed_items=[];p.sync();advance(1)
    check(company['phase']=='cancelled','putting away the actual toy cancels shared play')
    check(b.model.residents['cheese']['counts']['share']==old,'interrupted play never earns a completion')
    check(p.state['plan'] is None and g.renderer.duck_pos._state_str=='idle','cancelling shared play releases Cheese immediately')
    advance(180)
    check(p.state['objects']['toy_seesaw']['uses']==uses,'a cancelled invitation never grants an ordinary item completion later')
    check(playdates.motion(b,friend.id) is None,'the visitor also loses the cancelled toy reservation')
    plan,company=begin('toy_ball');old=b.model.residents['cheese']['counts']['share']
    g.friends.current_visit.started_at='replacement';advance(1)
    check(company['phase']=='cancelled','replacement visit cannot inherit a toy invitation')
    check(b.model.residents['cheese']['counts']['share']==old,'replacement visit grants no shared reward')
    plan,company=begin('toy_ball');old=b.model.residents['cheese']['counts']['share']
    visitor_animator._position_x=110;visitor_animator._position_y=28;b.sync()
    company.update(phase='approach',elapsed=0,waited=46)
    advance(1)
    check(company['phase']=='cancelled' and p.state['plan'] is None,'an unreachable partner times out and releases both residents: '+company['phase'])
    check(b.model.residents['cheese']['counts']['share']==old,'waiting for an absent partner earns no shared experience')
    plan,company=begin('toy_ball');p.cancel()
    check(playdates.motion(b,friend.id) is None and g.renderer.duck_pos._state_str=='idle','player cancellation releases the invitation and held pose')
    plan,company=begin('toy_trampoline');p.weather_type='thunderstorm';advance(1)
    check(company['phase']=='cancelled','a storm interrupts outdoor paired play')
    p.weather_type='sunny';g.friends.current_visit=None
    rare=VISITORS['friendly_goose'] if isinstance(VISITORS,dict) else next(v for v in VISITORS if v.id=='friendly_goose')
    g.atmosphere.current_visitor=(rare,datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=92,y=28)
    plan,company=begin('toy_seesaw');trail=set()
    for _ in range(600):
        advance(1);trail.add((round(g.guest_motion.actor['x'],3),round(g.guest_motion.actor['y'],3)))
        if company.get('done'):break
    check(company['partner']=='friendly_goose' and company['phase']=='done','a rare guest joins and completes shared toy play')
    check(len(trail)>5,'rare guest walks independently to the toy')
    g.atmosphere.current_visitor=None;g.guest_motion.tick(g,clock)
    p.state['story']={'id':'lost_duckling','step':0,'started':clock};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=92,y=28)
    plan,company=begin('toy_ball');trail=set()
    for _ in range(600):
        advance(1);trail.add((round(g.story_motion.actor['x'],3),round(g.story_motion.actor['y'],3)))
        if company.get('done'):break
    check(company['partner']=='story:pip' and company['phase']=='done','Pip joins and completes shared ball play')
    check(len(trail)>5,'story visitor uses real movement to join')
    p.cancel();g.duck.growth_stage='egg'
    check(not p.start('item','toy_seesaw')[0],'an egg cannot climb onto and operate a seesaw')
    result={'result':'PASS','checks':len(checks),'details':checks,'nativeFrames':len(frames)}
    out=ROOT/'engine/artifacts/animation-milestone';(out/'playdate-simulation.json').write_text(json.dumps(result,indent=2));(out/'playdate-frames.json').write_text(json.dumps(frames))
    print(json.dumps({k:v for k,v in result.items() if k!='details'}))
finally:
    b.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
