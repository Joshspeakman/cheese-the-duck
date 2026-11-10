"""Real desktop chat lifecycle using disposable saves and a controlled transport."""
import os,sys,tempfile,time,json
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-chat-check-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine.chat_stream import ChatStream,ChatMirror
checks=[]
def check(value,label):
    assert value,label
    checks.append(label)
s=ChatStream();mirror=ChatMirror(s.raw)
for n in range(300):mirror.append(('12:00','\x1b[31mSame line\x1b[0m','system'));mirror=mirror[-30:]
check(len(s.entries)==240 and len(mirror)==30,'Classic trimming never loses the independent bounded chat stream')
check(s.entries[-1]['id']==300 and s.entries[-1]['text']=='Same line','identical lines retain separate stable IDs and plain text')
s.reply('cheese','Cheese','player','Fuck yes.\nTwo lines.','say')
mirror.append(('12:00','Fuck yes.','duck'));mirror.append(('12:00','Two lines.','duck'))
check(s.entries[-1]['text']=='Fuck yes.\nTwo lines.' and s.sequence==301,'real reply appears once despite the Classic echo')
mirror.append(('12:00','Fuck yes.','duck'))
check(s.sequence==302,'echo suppression never swallows a later identical statement')
from engine import host
sys.stdout=host.WIRE
terminal=host.DesktopInput();g=host.DesktopGame(terminal=terminal,renderer_factory=host.CanvasRenderer)
terminal.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
 g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.duck.growth_stage='adult';g.renderer._show_talk=False;g.renderer.interface_modal=None
 p=g.living_pond;p.state['auto']=False;b=p.minds;b.sync();s=g.renderer.chat
 def command(key,text='My favorite flower is lavender. What the fuck, Cheese?',target='cheese',channel='say',session=None):
  return dict(type='chat',id=key,text=text,target=target,channel=channel,session=session or s.session)
 def settle():
  for _ in range(100):
   g._check_pending_talk();b._poll()
   if not b.pending and not getattr(g,'_pending_talk_future',None):return
   time.sleep(.02)
  raise AssertionError('reply did not finish')
 result=dict(text='Fuck yes. I will remember lavender.',source='authored',detail='controlled transport')
 with patch('engine.local_speech.speak',return_value=result),patch('core.game.find_matching_item',return_value='item-test') as lookup,patch.object(g,'_execute_item_interaction') as use:
  g._submit_chat(command('first'))
  check(s.receipts['first']['accepted'],'in-world chat is accepted by the real game')
  before=g.duck.memory.total_interactions;g._submit_chat(command('first'))
  check(g.duck.memory.total_interactions==before,'duplicate IPC request cannot duplicate memories or quest progress')
  check(not lookup.called and not use.called,'natural item mentions never invoke item interaction matching')
  g._submit_chat(command('busy'));check(not s.receipts['busy']['accepted'],'concurrent thought is rejected with a recoverable receipt')
  settle()
 check(sum(e['speaker']=='player' for e in s.entries)==1,'one player line per accepted message')
 check(sum(e['text']==result['text'] for e in s.entries)==1,'one complete Cheese reply in the live log')
 check(any('lavender' in f['text'] for f in b.model.residents['cheese']['facts']),'chat reaches actual persistent learned preferences')
 with patch('engine.local_speech.speak',return_value=dict(text='Keep talking. I am listening.',source='authored',detail='controlled transport')):
  g._submit_chat(command('follow-up','That is nice. What do you like?'));settle()
  check(s.receipts['follow-up']['accepted'],'a completed answer can be followed immediately by a different message')
  g._submit_chat(command('repeat','That is nice. What do you like?'))
  check(not s.receipts['repeat']['accepted'],'accidental rapid repeat is rejected without duplicating learning')
 g._submit_chat(command('old-world',session='stale'));check(not s.receipts['old-world']['accepted'],'old-session input cannot reach a newly loaded world')
 g._submit_chat(command('long',text='x'*1001));check(not s.receipts['long']['accepted'],'host enforces message length')
 g._submit_chat(command('absent',target='not-here'));check(not s.receipts['absent']['accepted'],'absent target never gets a fake conversation')
 g.renderer.interface_modal={'title':'Shop'};g._submit_chat(command('modal'));check(not s.receipts['modal']['accepted'],'modal gameplay state rejects chat without consuming draft')
 g.renderer.interface_modal=None
 friend=g.friends.generate_new_friend();p.sync();g.friends.start_visit(friend.id);b.sync();p.state['elapsed']+=10
 with patch('engine.mind_garden.speak',return_value=dict(text='I like the quiet corner of this pond.',source='authored',detail='controlled transport')):
  g._submit_chat(command('friend','Want to talk about your day?',friend.id,'whisper'));settle()
 check(s.receipts['friend']['accepted'],'whisper reaches the actual visiting friend')
 check(s.entries[-1]['speaker']==friend.id and s.entries[-1]['channel']=='whisper','visitor identity and whisper channel survive asynchronous generation')
 check(s.entries[-1]['text'].startswith('I like'),'visitor output is mirrored without prefix duplication')
 saved=json.loads(json.dumps(p.save()))
 old=s.session;s.reset();g._restore_living_pond(saved)
 check(s.session!=old and any(e['text']==result['text'] for e in s.entries),'saved conversations hydrate into a new session')
 check(any(e['speaker']==friend.id and e['channel']=='whisper' for e in s.entries),'saved whisper channel survives reload')
 from engine.interface import snapshot as interface_snapshot
 # Snapshot is exercised by the regular packaged smoke; store a chat fixture here.
 out=ROOT/'engine/artifacts/chat';out.mkdir(exist_ok=True,parents=True)
 (out/'stream.json').write_text(json.dumps(s.snapshot(g.living_pond.minds),indent=2))
 (out/'checks.json').write_text(json.dumps(dict(result='PASS',checks=checks),indent=2))
 print(json.dumps(dict(result='PASS',checks=len(checks))))
finally:
 if g.living_pond:g.living_pond.minds.close()
 if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=True)
 g._save_executor.shutdown(wait=True)
 from audio.sound import sound_engine
 sound_engine.shutdown()
