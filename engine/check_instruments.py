"""Music clocks, actual arrivals, interrupted sessions and safe synthesized voices."""
import os,sys,tempfile,json,copy,random,array,time
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-music-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,shelters,instrument_sessions as music
from engine.instrument_audio import synthesize,InstrumentAudio
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import Weather,WeatherType,VISITORS,Season
sys.stdout=host.WIRE;random.seed(41);checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
class Recorder:
    def __init__(self):self.notes=[];self.sessions=set()
    def play(self,*args):self.notes.append(args)
    def stop_except(self,sessions):self.sessions=set(sessions)
    def close(self):self.sessions.clear()
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=10**9;b.instrument_audio=Recorder()
    g.habitat.owned_items.extend(music.INSTRUMENTS);g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat());p.sync()
    for item in music.INSTRUMENTS:
        check(p.state['objects'].get(item) is not None,item+' has persistent condition')
    clock=0.
    def advance(n,brains=False,capture=True):
        global clock
        for _ in range(n):
            clock+=.1;p.state['elapsed']+=.1
            pos=g.renderer.duck_pos;pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
            if brains:
                if g.friends.current_visit:
                    visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
                g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%10==0 and (p.state['plan'] or b.musicians):frames.append(snapshot(g,g.renderer))
    def reset(item='piano',stage='adult'):
        p.cancel();b.musicians.clear();b.music_scenes.clear();b.music_retry.clear();b.tasks.clear();b.furnishings.clear();b.gardening.clear();b.housing.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None
        g.duck.growth_stage=stage;g.duck.needs.energy=90;g.duck.needs.hunger=90;g.duck_store.sync_from_duck(g.duck)
        g.habitat.placed_items=[PlacedItem(item,10,6)];p.sync();b.sync();p.weather_type='sunny';p.season='spring';p.hour=12
        p.state['cooldowns']={};p.state['objects'][item]['last_use']=-1000
        p.state['objects'][item]['music_scores']={};b.model.residents['cheese']['mood']=.5;b.model.residents['cheese']['traits']['confidence']=.5
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        ok,msg=p.start('item',item);check(ok,'start '+item+' '+stage+': '+msg)
        return p.state['plan']
    for item in music.INSTRUMENTS:
        plan=reset(item);before=p.state['objects'][item]['uses'];learned=b.model.residents['cheese']['counts']['practice'];start=len(b.instrument_audio.notes)
        for _ in range(1200):
            advance(1)
            if not p.state['plan']:break
        score=plan.get('music_score',{});check(score.get('done') and p.state['objects'][item]['uses']==before+1,item+' arrived and finished exactly once')
        check(b.model.residents['cheese']['counts']['practice']==learned+1,item+' teaches music after finishing')
        check(len(b.instrument_audio.notes)-start==len(music.SCORES[score['id']]['notes']),item+' emits each note exactly once')
        check(p.state['objects'][item]['music_scores']=={score['id']:1},item+' records the actual completed phrase')
    for stage in shelters.AGES[1:]:
        plan=reset('toy_piano',stage)
        for _ in range(1200):
            advance(1,capture=stage=='hatchling')
            if not p.state['plan']:break
        check(plan['music_score']['done'],stage+' plays a complete phrase without changing age')
        expected='first_keys' if stage in ('hatchling','duckling') else 'old_refrain' if stage in ('elder','legendary') else 'pond_waltz'
        check(plan['music_score']['id']==expected,stage+' selects '+expected)
    reset();p.cancel()
    for key,changes in [('quiet_lullaby',{'hour':23}),('rain_on_keys',{'weather_type':'rainy'}),('autumn_walk',{'season':'fall'})]:
        p.hour=12;p.weather_type='sunny';p.season='spring'
        for k,v in changes.items():setattr(p,k,v)
        check(music.choose(p,'piano')==key,'context selects '+key)
    plan=reset();advance(170);score=plan['music_score'];before=copy.deepcopy(score);count=len(b.instrument_audio.notes);plan['paused']=True;advance(30,True)
    check(score==before and len(b.instrument_audio.notes)==count and plan['music_session'] not in b.instrument_audio.sessions,'pause freezes the phrase and stops its sound')
    saved=LivingPond(p.save());check(saved.state['plan']['paused'] and not saved.minds.musicians,'load preserves Cheese clock and discards transient visitor sessions');saved.minds.close()
    plan['paused']=False;before=p.state['objects']['piano']['uses'];g.habitat.placed_items=[];p.sync();advance(1,True)
    check(not p.state['plan'] and p.state['objects']['piano']['uses']==before,'putting an instrument away cancels without completing')
    check(not b.instrument_audio.sessions,'removed instrument releases audio')
    plan=reset();advance(170);plan['music_score']['id']='unknown';advance(1)
    check(not p.state['plan'],'unknown saved phrase cancels safely')
    # A long frame consumes missed beats without a loud burst on resume.
    s=music.make_score(p,'piano');notes=len(b.instrument_audio.notes);music.clock(b,'piano',s,9.923,'late')
    check(len(b.instrument_audio.notes)-notes<=1 and s['cursor']>1,'late frames skip stale notes instead of replaying a burst')
    # Two actual visitors and Pip follow fixed reservations, independent of Cheese.
    plan=reset('piano');friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._position_x=74;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    g.atmosphere.current_visitor=(VISITORS['friendly_goose'],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=85,y=24)
    p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=42,y=22)
    g.habitat.placed_items.extend([PlacedItem('drums',18,6),PlacedItem('wind_chimes',4,6)]);p.sync();b.sync()
    keys=[k for k in b.present if k!='cheese'];starts={k:b.model.residents[k]['counts']['practice'] for k in b.present}
    for key in keys:b.model.residents[key]['energy']=.9;b.tasks[key]=dict(action='practice',until=b.now+50,context=b.context(key))
    b.tick();check(len(b.musicians)==3,'regular, rare and story visitors independently reserve instruments')
    destinations={k:list(r['spot']) for k,r in b.musicians.items()};paths={k:set() for k in keys};arrived=set();paired=False;shared_score=None
    for _ in range(1600):
        advance(1,True)
        for k in keys:
            paths[k].add(tuple(round(n,3) for n in b.present[k]))
            if k in b.musicians:
                r=b.musicians[k];assert r['spot']==destinations[k]
                if r['phase']=='inside':arrived.add(k)
        if b.music_scenes:
            paired=True;s=next(iter(b.music_scenes.values()));shared_score=s['score']['id']
            check(b.model.residents[s['a']]['counts']['practice']==starts[s['a']],'duet rewards wait for a finished phrase') if s['score']['elapsed']==0 else None
            a=p._plan_view()['music_score'] if s['a']=='cheese' else next(r['score'] for r in music.snapshot(b) if r['actor']==s['a'])
            z=p._plan_view()['music_score'] if s['b']=='cheese' else next(r['score'] for r in music.snapshot(b) if r['actor']==s['b'])
            assert a['elapsed']==z['elapsed'] and a['role']!=z['role']
        if not p.state['plan'] and not b.musicians:break
    check(all(len(path)>5 for path in paths.values()) and arrived==set(keys),'all three visitor controllers walk and arrive before playing')
    check(paired and shared_score=='two_wing_answer','actual neighboring pianists perform a question-and-answer duet')
    check(b.model.residents['cheese']['counts']['practice']==starts['cheese']+2,'Cheese learns once for the duet and once for his own finished phrase')
    check(all(b.model.residents[k]['counts']['practice']>=starts[k]+1 for k in keys),'every visitor learns from their completed playing')
    check(not b.musicians and not b.music_scenes,'finished musicians leave instruments for independent life')
    # Visitors also duet with each other while Cheese stays elsewhere.
    reset('piano');p.cancel();g.renderer.duck_pos.x=105;g.renderer.duck_pos.y=28
    g.friends.start_visit(friend.id);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
    visitor_animator._position_x=61;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    g.atmosphere.current_visitor=(VISITORS['friendly_goose'],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=73,y=21)
    b.sync();others=(friend.id,'friendly_goose');counts={k:b.model.residents[k]['counts']['practice'] for k in ('cheese',)+others}
    for key in others:b.model.residents[key]['energy']=.9;b.tasks[key]=dict(action='practice',until=b.now+50,context=b.context(key))
    b.tick();saw_pair=False
    for _ in range(1400):
        advance(1,True)
        for duet in b.music_scenes.values():
            assert 'cheese' not in (duet['a'],duet['b']);saw_pair=True
        if not b.musicians:break
    check(saw_pair and all(b.model.residents[k]['counts']['practice']==counts[k]+2 for k in others),'two visiting musicians independently finish a duet and their own phrases')
    check(b.model.residents['cheese']['counts']['practice']==counts['cheese'],'Cheese cannot receive credit for another pair playing together')
    # Replacement visit, storm and cancel never manufacture finished music.
    b.music_retry.clear();b.tasks[friend.id]=dict(action='practice',until=b.now+50,context=b.context(friend.id));b.tick();check(friend.id in b.musicians,'later visitor practice reserves anew')
    before=b.model.residents[friend.id]['counts']['practice'];g.friends.current_visit.started_at='different-visit';advance(1,True)
    check(friend.id not in b.musicians and b.model.residents[friend.id]['counts']['practice']==before,'replaced visitor loses the old reservation without learning')
    b.music_retry.clear();b.tasks[friend.id]=dict(action='practice',until=b.now+50,context=b.context(friend.id));b.tick();p.weather_type='stormy';advance(1,True)
    check(not b.musicians and b.model.residents[friend.id]['counts']['practice']==before,'storm interrupts visitor music without reward')
    plan=reset();advance(170);before=b.model.residents['cheese']['counts']['practice'];p.cancel();advance(1,True)
    check(b.model.residents['cheese']['counts']['practice']==before and not b.instrument_audio.sessions,'canceling Cheese gives no completion and stops audio')
    plan=reset();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._position_x=70;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    b.sync();b.tasks[friend.id]=dict(action='practice',until=b.now+50,context=b.context(friend.id));b.tick()
    for _ in range(400):
        advance(1,True)
        if b.music_scenes:break
    check(bool(b.music_scenes),'new pianists arrive before a shared phrase can start')
    elapsed=plan['music_score']['elapsed'];counts={k:b.model.residents[k]['counts']['practice'] for k in ('cheese',friend.id)}
    g.duck.current_action='feed';advance(10,True)
    check(not b.music_scenes and plan['music_score']['elapsed']==elapsed and p._plan_view()['paused'],'direct care interrupts the duet and freezes Cheese without claiming he still plays')
    check(all(b.model.residents[k]['counts']['practice']==v for k,v in counts.items()),'interrupted duet has no completion learning')
    g.duck.current_action=None;p.cancel()
    for _ in range(600):
        advance(1,True)
        if friend.id not in b.musicians:break
    check(b.model.residents[friend.id]['counts']['practice']==counts[friend.id]+1 and b.model.residents['cheese']['counts']['practice']==counts['cheese'],'remaining visitor finishes only their own phrase')
    g.duck.growth_stage='egg';check(not p.start('item','piano')[0],'eggs cannot play keyboards')
    from world.guest_cast import PROFILES
    key=next(k for k,v in PROFILES.items() if v['species']=='butterfly');b.model.ensure(key,'Flutter',PROFILES[key]);b.present[key]=(66,21)
    g.habitat.placed_items.extend([PlacedItem('wind_chimes',4,6)]);p.sync()
    check(all(music.INSTRUMENTS[r['id']]['type']=='chimes' for r in music.candidates(b,key)) and music.candidates(b,key),'butterflies choose light chimes, not valves or drumsticks')
    # PCM: deterministic, bounded, distinct timbres, stereo format and short tail.
    waves={voice:synthesize(voice,60,.2,8000,2) for voice in ('piano','brass','drum','bell','shell','gong','tines','tom','snare','cymbal','kick')}
    check(len(waves['piano'])==int(8000*.45)*4,'stereo PCM duration follows note duration')
    for voice,pcm in waves.items():
        samples=array.array('h',pcm);check(max(map(abs,samples))<4000 and samples[0]==0,voice+' has bounded attack and no clipping')
        check(pcm==synthesize(voice,60,.2,8000,2),voice+' is deterministic')
    check(len(set(waves.values()))==11,'instrument families have distinct audible waveforms')
    from audio.sound import sound_engine
    audio=InstrumentAudio();sound_engine.enabled=True
    audio.play('test','piano',60,.2,.2);time.sleep(.15)
    check(bool(audio.active),'real dummy-SDL note is owned by a registered worker')
    audio.stop_except(set())
    for _ in range(100):
        if not audio.active:break
        time.sleep(.02)
    check(not audio.active,'canceling safely drains instrument workers')
    sound_engine.enabled=False;audio.play('muted','piano',60,.2)
    check(not audio.active,'muted game starts no audio worker')
    sound_engine.enabled=True
    for midi in (60,64,67):audio.play('closing','piano',midi,.4,.1)
    audio.close()
    check(not audio.active and not audio.workers,'closing joins every owned mixer worker before shutdown')
    audio.play('after-close','piano',60,.2)
    check(not audio.active,'closed instrument service cannot restart playback')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(exist_ok=True)
    (out/'instrument-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),scores=len(music.SCORES),instruments=len(music.INSTRUMENTS),frames=len(frames))
    (out/'instrument-native.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
