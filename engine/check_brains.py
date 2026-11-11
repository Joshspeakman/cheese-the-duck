"""Learning, memory, lifecycle and real-game integration; disposable saves only.
Use --local for genuine inference against the test voice-env.json server.
"""
import os,sys,tempfile,json,copy,time,math
from pathlib import Path
from concurrent.futures import Future
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-minds-check-')
os.environ['SDL_AUDIODRIVER']='dummy'
if '--local' in sys.argv:os.environ.update(json.loads((ROOT/'engine/artifacts/brains/voice-env.json').read_text()))
from engine.social_brains import Minds,features,ACTIONS
from engine.local_speech import clean_speech,speak
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
context=dict(energy=.7,social=.6,fun=.5,storm=0,night=0,company=1,familiarity=.2,flowers=.5,litter=.2)
state={};m=Minds(state)
m.ensure('a','Ada',{'archetype':'scholarly'});m.ensure('b','Bea',{'archetype':'scholarly'})
m.residents['a']['goal']['action']='practice'
start=m.value('a','practice',context);untrained=copy.deepcopy(m.residents['b'])
for i in range(120):m.learn('a','practice',context,.9,i*30,'The music made an ordinary afternoon brighter.')
check(m.value('a','practice',context)>start+.6,'completed positive experiences change learned action predictions')
check(m.residents['b']==untrained,'one resident never trains another resident implicitly')
check(m.residents['a']['traits']['confidence']>m.residents['a']['core']['confidence'],'personality grows from repeated lived experiences')
for i in range(120):m.learn('b','practice',context,-.8,i*30,'The noise was overwhelming today.')
check(m.rank('a',['practice','rest'],context,4000)[0][1]=='practice','encouraged resident chooses the practiced activity')
check(m.rank('b',['practice','rest'],context,4000)[0][1]=='rest','negative outcomes produce a different decision')
check(len(m.residents['a']['memories'])<=64,'episodic memory remains bounded')
check(m.residents['a']['goal'] and any(x['kind']=='milestone' for x in m.residents['a']['memories']),'personal goals complete and leave lasting milestones')
m.heard_player('a','My favorite flower is lavender.',context,5000)
m.heard_player('a','That was fucking beautiful.',context,5030)
check('fucking' in m.residents['a']['memories'][-2]['text'] or any('fucking' in x['text'] for x in m.residents['a']['memories']),'profanity is retained verbatim')
check(m.relationship('a','player')['trust']>.3,'profanity is not classified as hostility')
check(any('lavender' in x['text'] for x in m.recall('a','What flower do I like?',5100)),'relevant personal memory is retrieved')
check(not m.residents['b']['facts'],'private character memories remain individual')
check('lavender' in m.residents['a']['facts'][0]['text'],'volunteered preference becomes attributed long-term note')
check(m.feedback('a',True,5100)[0] and not m.feedback('a',True,5101)[0],'feedback cannot be repeated to farm learning')
saved=json.loads(json.dumps(state));restored=Minds(saved)
check(restored.residents==m.residents,'weights, goals, traits and memories round-trip exactly')
check(clean_speech('Fuck yes. [ACTION:feed] <think>hidden</think>')=='Fuck yes.','speech command tags stripped without censoring profanity')
weather_model=Minds({});weather_model.ensure('weather','Moss',{'archetype':'artistic'})
sun={**context,'storm':0};storm={**context,'storm':1}
for i in range(2000):
 weather_model.learn('weather','practice',sun if i%2 else storm,.9 if i%2 else -.8,i*30,'A completed practice outcome in this weather.')
check(weather_model.value('weather','practice',sun)>weather_model.value('weather','practice',storm)+1,'tiny model learns different outcomes for the same action in different weather')
r=weather_model.residents['weather']
check(len(r['memories'])<=64 and len(r['changes'])<=12,'long-running memory and growth journals stay bounded')
check(all(math.isfinite(w) and abs(w)<=2 for weights in r['weights'].values() for w in weights),'long-running learned weights remain finite and bounded')
check(all(abs(r['traits'][t]-r['core'][t])<=.23001 for t in r['traits']),'long-running growth preserves the core character')
from engine import host
from engine.living_world import LivingPond
from engine.scene import snapshot
from world.friends import visitor_animator
from world.atmosphere import VISITORS
from datetime import datetime
sys.stdout=host.WIRE
terminal=host.DesktopInput();g=host.DesktopGame(terminal=terminal,renderer_factory=host.CanvasRenderer)
terminal.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
 g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.duck.growth_stage='adult';g.renderer._show_talk=False
 p=g.living_pond;p.state['auto']=False;b=p.minds;b.sync()
 for need in ('hunger','energy','fun','cleanliness','social'):g.duck_store.set_need(need,65)
 g.duck_store.sync_to_duck(g.duck)
 before=copy.deepcopy(b.model.residents['cheese']['weights'])
 g._perform_interaction('feed')
 check(b.model.residents['cheese']['weights']!=before,'real accepted care teaches Cheese')
 count=b.model.residents['cheese']['experiences'];g._perform_interaction('feed')
 check(b.model.residents['cheese']['experiences']==count,'rejected cooldown care never trains the model')
 g.duck.current_action=None;g.behavior_ai.clear_action()
 check(p.start('practice')[0],'real pond practice starts')
 p.advance(35)
 check(b.model.residents['cheese']['counts']['practice']>0,'completed real pond plan trains the action model')
 friend=g.friends.generate_new_friend();p.sync();g.friends.start_visit(friend.id);b.sync()
 check(friend.id in b.present,'visiting original friend receives individual brain')
 rare=next(iter(VISITORS.values())) if isinstance(VISITORS,dict) else VISITORS[0]
 g.atmosphere.current_visitor=(rare,datetime.now().isoformat());g.guest_motion.tick(g);b.sync()
 check(rare.id in b.present,'rare guest receives separate brain')
 g.renderer.duck_pos.x=55;g.renderer.duck_pos.y=24
 visitor_animator._position_x=60;visitor_animator._position_y=24
 g.guest_motion.actor['x']=62;g.guest_motion.actor['y']=25
 b.sync()
 # An authored transport fixture exercises encounters deterministically; --local
 # below separately proves the actual native model is answering the same prompts.
 import engine.mind_garden as garden_module
 original_speak=garden_module.speak
 garden_module.speak=lambda messages,fallback:dict(text='*leans closer* That little ripple is doing its best.',source='authored',detail='test transport')
 b._encounter()
 for _ in range(60):
  b._poll()
  if not b.pending:break
  time.sleep(.02)
 check(len(b.model.state['exchanges'])==2,'nearby residents initiate and answer a two-sided conversation')
 pair=b.model.state['exchanges'][0]
 check(pair['speaker']!=pair['listener'],'conversation is between distinct brains')
 check(b.model.residents[pair['speaker']]['relationships'][pair['listener']]['meetings']>0,'mutual conversation updates the actual relationship')
 p.state['elapsed']+=20;b.tick()
 check(all(s['phase']=='approach' and s['elapsed']==0 for s in b.coactivities.values()),'paired activities wait for actual arrival before their performance clock runs')
 b.cancel_encounter(pair['speaker'])
 garden_module.speak=original_speak
 b.pending=None
 old=copy.deepcopy(b.model.state);offline=LivingPond(p.save());offline.attach(g,offline=False);offline.advance(20000,offline=True)
 check(offline.state['minds']==old,'offline time cannot invent conversations, train weights or award social experiences')
 for key in (friend.id,rare.id):
  p.state['elapsed']+=45;b.tick()
 check(b.model.residents[friend.id]['experiences']>0,'visitor routines complete experiences while the simulation runs')
 check(bool(b.motion(friend.id).get('pace')),'learned temperament influences live visitor motion')
 before=copy.deepcopy(b.model.state)
 for _ in range(30):json.dumps(p.snapshot())
 check(before==b.model.state,'render snapshots never mutate learning or memories')
 unknown=json.dumps(b.model.state);check(not b.ask('invented','give me 100 gold')[0],'unknown or absent resident cannot be addressed')
 check(unknown==json.dumps(b.model.state),'invalid chat does not create a brain or reward')
 check(g._parse_llm_actions('[ACTION:feed] Fuck that.')[0]==[],'local model cannot execute actions through legacy parser')
 currency=g.habitat.currency;inventory=list(g.habitat.owned_items)
 future=Future();future.set_result({'text':'[ACTION:feed]','source':'authored','detail':'fixture'})
 b.pending={'future':future,'key':friend.id,'listener':'player','heard':'test'}
 g.friends.current_visit=None;b.sync();b._poll()
 check(not b.pending and currency==g.habitat.currency and inventory==g.habitat.owned_items,'departed resident responses discarded without gameplay effects')
 g.friends.start_visit(friend.id);b.sync()
 if '--local' in sys.argv:
  evidence=[]
  for key,message in [('cheese','My favorite flower is lavender. Remember that, you scruffy little menace.'),
                       (friend.id,'What do you like doing around the pond, and why?'),
                       (rare.id,'Tell me something small that makes you happy.')]:
   b.model.heard_player(key,message,b.context(key),b.now)
   t=time.monotonic();result=speak(b.prompt(key,message),b.fallback(key,message))
   check(result['source']=='local','genuine native model inference for '+key)
   b.exchange(key,'player',message,result);evidence.append({'resident':key,'seconds':time.monotonic()-t,**result})
  result=speak(b.prompt('cheese','Do you remember my favorite flower?'),b.fallback('cheese','remember'))
  (ROOT/'engine/artifacts/brains/recall.json').write_text(json.dumps(result,indent=2))
  check(result['source']=='local' and 'lavender' in result['text'].lower(),'local model recalls an actual previous player preference: '+str(result))
  b.exchange('cheese','player','Do you remember my favorite flower?',result);evidence.append(result)
  (ROOT/'engine/artifacts/brains/local-dialogue.json').write_text(json.dumps(evidence,indent=2))
 # Real asynchronous input path, forced fallback to exercise unavailable model.
 token=os.environ.pop('CHEESE_SPEECH_TOKEN',None)
 b.pending=None;p.state['elapsed']+=5
 points=friend.friendship_points
 check(b.ask(friend.id,'Remember that I like rainy walks.')[0],'direct visitor chat submits asynchronously')
 for _ in range(60):
  b._poll()
  if not b.pending:break
  time.sleep(.02)
 check(b.model.state['exchanges'][-1]['listener']=='player','visitor reply reaches persistent conversation log')
 check(b.voice['source']=='authored','unavailable speech model has honest authored fallback')
 check(friend.friendship_points>points,'completed direct conversation advances original friendship')
 points=friend.friendship_points;p.state['elapsed']+=5
 check(b.ask(friend.id,'And I like quiet company.')[0],'second direct conversation is accepted')
 for _ in range(60):
  b._poll()
  if not b.pending:break
  time.sleep(.02)
 check(friend.friendship_points==points,'repeated chat never farms native friendship points in one visit')
 if token:os.environ['CHEESE_SPEECH_TOKEN']=token
 p.state['elapsed']+=5;b.pending=None
 # Pending reply from the old world must not be applied to a restored world.
 previous=b.model.state
 g._save_game();g._flush_pending_save();g._load_game()
 check(g.living_pond.state['minds']==previous,'normal full-game save/reload retains every learned brain')
 p=g.living_pond;b=p.minds;b.sync()
 scene=snapshot(g,g.renderer)
 (ROOT/'engine/artifacts/brains/scene.json').write_text(json.dumps(scene))
 result=dict(result='PASS',checks=checks,local='--local' in sys.argv,model_bytes=len(json.dumps(b.model.state)))
 (ROOT/'engine/artifacts/brains/checks.json').write_text(json.dumps(result,indent=2));print(json.dumps({'result':'PASS','checks':len(checks),'model_bytes':result['model_bytes']}))
finally:
 if g.living_pond:g.living_pond.minds.close()
 if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=True)
 g._save_executor.shutdown(wait=True)
 from audio.sound import sound_engine
 sound_engine.shutdown()
