"""Exercise authored routines with the real game, isolated save directory/audio."""
import os
import sys
import tempfile
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ['CHEESE_SAVE_DIR'] = tempfile.mkdtemp(prefix='cheese-nest-scores-')
os.environ['SDL_AUDIODRIVER'] = 'dummy'
from engine import host, nest_routines as routines
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.atmosphere import WeatherType, Weather
from datetime import datetime
sys.stdout = host.WIRE
checks = []
def check(ok, message):
    assert ok, message
    checks.append(message)
t = host.DesktopInput()
g = host.DesktopGame(terminal=t, renderer_factory=host.CanvasRenderer)
t.game = g; g.renderer.game = g; g.renderer.present = lambda lines: None
try:
    g._running=True; g._start_new_game(); g._flush_pending_save()
    g._state='playing'; g.renderer._show_talk=False
    g.duck.growth_stage='adult'; g.duck.current_action=None
    p=g.living_pond; p.state['auto']=False
    for need in ('hunger','energy','fun','cleanliness','social'):g.duck_store.set_need(need,65)
    g.duck_store.sync_to_duck(g.duck)
    g.habitat.owned_items.extend(routines.NESTS)
    g.habitat.placed_items=[PlacedItem('basic_nest',5,5),PlacedItem('deluxe_nest',10,5)]
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    p.sync();pos=g.renderer.duck_pos;pos.x=8;pos.y=20
    check(p.start('rest','basic_nest')[0],'ordinary rest starts at an owned placed nest')
    plan=p.state['plan'];p._activity(2)
    check(not plan['residence'].get('routine'),'distant Cheese does not act at the nest')
    walked=[]
    for _ in range(600):
        pos.update(.2);p._activity(.2);walked.append((pos.x,pos.y))
        if plan['phase']=='act':break
    check(len(set(walked))>8 and plan['phase']=='act','Cheese actually walks to the nest before performing')
    check(bool(plan['residence'].get('routine')),'arrival selects a contextual routine')
    first=plan['residence']['routine']['id'];duration=routines.ROUTINES[first]['duration']
    earlier=p.snapshot();earlier_elapsed=earlier['plan']['residence']['routine']['elapsed'];p._activity(.1)
    later=p.snapshot()
    check(later['plan']['residence']['routine']['elapsed']>earlier_elapsed and earlier['plan']['residence']['routine']['elapsed']==earlier_elapsed,'every frame receives the current acting clock without mutating previous snapshots')
    check(later['plan']['label']==routines.ROUTINES[first]['label'],'the live status names the actual routine')
    prompt=p.minds.prompt('cheese','What are you doing?')[0]['content']
    check(routines.ROUTINES[first]['label'] in prompt,'natural chat receives the verified physical action')
    before=p.state['objects']['basic_nest']['uses']
    live_frames=[]
    for n in range(int(duration/.2)+2):
        pos.update(.2);p._activity(.2)
        if n%3==0:
            g.renderer.render_frame(g)
            live_frames.append(snapshot(g,g.renderer))
    (ROOT/'engine/artifacts/animation-milestone/nest-live-frames.json').write_text(json.dumps(live_frames))
    obj=p.state['objects']['basic_nest']
    check(obj['routines'].get(first)==1,'finishing the whole routine records it once')
    for _ in range(60):p._activity(.2)
    check(p.state['plan'] is None and obj['uses']==before+1,'one ordinary visit ends with one normal rest completion')
    saved=p.save();loaded=LivingPond(saved)
    check(loaded.state['objects']['basic_nest']['routines']==obj['routines'],'learned object history survives a save round trip')
    check(routines.ROUTINES[first]['label'].lower() in p.state['journal'][-1]['text'],'a completed visit remembers its actual routine')

    p.state['cooldowns'].clear()
    g.atmosphere.current_weather=Weather(WeatherType.RAINY,.8,1,datetime.now().isoformat())
    check(p.start('rest','deluxe_nest')[0],'a covered nest accepts a rainy visit')
    plan=p.state['plan'];pos.x,pos.y=plan['destination'];p._activity(9)
    check(plan['phase']=='act','covered-nest fixture reached the acting phase')
    selected=[];seen=None;positions=[]
    for _ in range(1500):
        # The original animator expires timed states using wall time. Advance
        # that clock too, so accelerated simulation cannot conceal late wandering.
        pos._state_start_time-=.2;pos.update(.2);p._activity(.2);positions.append((pos.x,pos.y))
        current=plan['residence']['routine']
        identity=(current['id'],p.state['objects']['deluxe_nest'].get('routine_visits',0))
        if identity!=seen and not current.get('done'):selected.append(current['id']);seen=identity
    check(len(set(selected))>=8,'a long rainy wait produces varied physical routines')
    check(all(a!=b for a,b in zip(selected,selected[1:])),'consecutive routines are not repeated')
    check(plan['residence']['restored']<=10 and plan['residence'].get('tidied',0)<=.060001,'storm needs and tidying remain capped for the entire visit')
    check(p.state['objects']['deluxe_nest']['uses']==0,'routine changes do not farm visit rewards')
    check(len(set(positions))==1,'the physical duck remains sheltered throughout a long storm')
    ctx=routines.context(p,plan)
    check(not routines.eligible(routines.ROUTINES['thunder_duck'],ctx),'rain without thunder never triggers the thunder reaction')
    check(routines.eligible(routines.ROUTINES['rain_listen'],ctx),'rain under a canopy can trigger listening')
    ctx['roof']=False
    check(not routines.eligible(routines.ROUTINES['rain_listen'],ctx),'uncovered nests cannot claim canopy shelter')
    ctx.update(weather='rainbow',roof=True)
    check(not routines.eligible(routines.ROUTINES['drip_watch'],ctx),'rainbows do not count as rainfall')
    ctx.update(stage='egg')
    check(not any(routines.eligible(s,ctx) for s in routines.ROUTINES.values()),'eggs never perform walking, weaving or bill actions')

    # Canceling mid-action must not update its history or consume anything.
    plan['residence']['routine']={'id':'weave_rim','elapsed':3.,'done':False,'label':routines.ROUTINES['weave_rim']['label']}
    history=dict(p.state['objects']['deluxe_nest'].get('routines',{}))
    p.cancel();p._activity(30)
    check(p.state['objects']['deluxe_nest'].get('routines',{})==history,'canceling a partial action grants no completion')
    p.state['cooldowns'].clear();check(p.start('rest','deluxe_nest')[0],'a later visit can resume using the nest')
    plan=p.state['plan'];pos.x,pos.y=plan['destination'];p._activity(9)
    plan['residence']['routine']={'id':'rain_listen','elapsed':5.,'done':False,'label':routines.ROUTINES['rain_listen']['label']}
    p.weather_type='sunny';before=p.state['objects']['deluxe_nest'].get('routines',{}).get('rain_listen',0)
    p._activity(.2)
    check(plan['residence']['routine'].get('interrupted'),'a weather-specific action stops when its weather disappears')
    check(p.state['objects']['deluxe_nest'].get('routines',{}).get('rain_listen',0)==before,'interrupted weather action is not recorded as complete')
    p._activity(20)
    check(p.state['plan'] is None,'clear weather releases the canopy wait')
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    p.state['cooldowns'].clear();p.start('rest','basic_nest');plan=p.state['plan'];pos.x,pos.y=plan['destination'];p._activity(9)
    elapsed=plan['residence']['routine']['elapsed'];plan['paused']=True;p._activity(30)
    check(plan['residence']['routine']['elapsed']==elapsed,'paused routines do not advance')
    saved=p.save();loaded=LivingPond(saved)
    check(loaded.state['plan']['paused'] and loaded.state['plan']['residence']['routine']['elapsed']==elapsed,'saving an occupied nest preserves its score and pauses on load')
    pos.x=90;pos.y=25;p.command({'action':'resume'});p._activity(.2)
    check(plan['phase']=='approach' and not plan['residence']['inside'],'resuming from elsewhere walks back instead of teleporting inside')
    check(plan['residence']['routine']['elapsed']==elapsed,'walking back preserves the unfinished routine clock')
    for _ in range(800):
        pos.update(.2);p._activity(.2)
        if plan['phase']=='act':break
    check(plan['phase']=='act' and plan['residence']['inside'],'an interrupted visitor can physically re-enter his nest')
    p.cancel()
    check(pos.get_state()=='idle' and not pos._is_directed_movement,'canceling indefinite shelter occupancy restores free movement')
    result={'result':'PASS','checks':len(checks),'authoredScores':len(routines.ROUTINES),'rainyWaitRoutines':selected,'details':checks}
    (ROOT/'engine/artifacts/animation-milestone/nest-simulation.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({'result':'PASS','checks':len(checks),'rainyWaitDistinct':len(set(selected))}))
finally:
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    from audio.sound import sound_engine
    sound_engine.shutdown()
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
