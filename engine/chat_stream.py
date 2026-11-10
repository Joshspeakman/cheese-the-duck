"""Structured desktop chat alongside the original terminal log.

One ordered stream contains world messages and real conversations. UI reloads
receive stable IDs, not rewrapped terminal rows. Receipts make retries harmless.
"""
from collections import OrderedDict
from datetime import datetime
import time
import uuid
from engine.frame import line_runs


def plain(text):
    return '\n'.join(''.join(r[0] for r in line_runs(line)) for line in str(text).splitlines())


class ChatMirror(list):
    """Preserve the renderer's 30-entry Classic log and mirror every append."""
    def __init__(self, callback, values=()):
        super().__init__(values);self.callback=callback
    def append(self, value):
        super().append(value);self.callback(*value)
    def __getitem__(self, index):
        result=super().__getitem__(index)
        return ChatMirror(self.callback,result) if isinstance(index,slice) else result


class ChatStream:
    LIMIT=240
    def __init__(self):self.reset()
    def reset(self):
        self.session=uuid.uuid4().hex;self.sequence=0;self.entries=[]
        self.receipts=OrderedDict();self.echoes=[];self.names={'Cheese':'cheese'}
    def append(self, text, channel='world', speaker='', name='', target='', timestamp=None, source=''):
        text=plain(text).strip()
        if not text:return
        self.sequence+=1
        row=dict(id=self.sequence,text=text[:4000],channel=channel,speaker=speaker,name=name,target=target,
                 time=timestamp or datetime.now().strftime('%H:%M'),source=source)
        self.entries.append(row);self.entries=self.entries[-self.LIMIT:]
        return row
    def raw(self,timestamp,text,category):
        text=plain(text).strip();now=time.monotonic()
        self.echoes=[e for e in self.echoes if e['until']>now]
        for e in self.echoes:
            if text in e['texts']:
                self.echoes.remove(e);return
        if text in ('*tilts head* ...','*blinks* ...','*thinking* ...','*considers this* ...','*processing* ...'):return
        speaker='cheese' if category=='duck' else '';name='Cheese' if speaker else ''
        if ': ' in text:
            prefix,rest=text.split(': ',1)
            if prefix in self.names:speaker=self.names[prefix];name=prefix;text=rest
        channel='say' if speaker else 'loot' if category=='discovery' else 'world'
        self.append(text,channel,speaker,name,timestamp=timestamp)
    def player(self,text,target='cheese',channel='say'):
        return self.append(text,channel,'player','You',target)
    def reply(self,key,name,listener,text,channel,source='',timestamp=None,echo=True):
        self.names[name]=key
        row=self.append(text,channel,key,name,listener,timestamp,source)
        if echo:
            for line in str(text).splitlines():
                if line.strip():self.echoes.append({'texts':{plain(line).strip(),name+': '+plain(line).strip()},'until':time.monotonic()+10})
        return row
    def restore(self,exchanges):
        for e in exchanges[-35:]:
            channel=e.get('channel','say' if e['speaker']=='cheese' else 'whisper') if e['listener']=='player' else 'neighbors'
            if e['listener']=='player':self.append(e['heard'],channel,'player','You',e['speaker'],e.get('time','Earlier'))
            self.reply(e['speaker'],e['name'],e['listener'],e['text'],channel,e.get('source',''),e.get('time','Earlier'),False)
    def receipt(self,request,accepted,message=''):
        self.receipts[request]=dict(id=request,accepted=bool(accepted),message=str(message))
        while len(self.receipts)>32:self.receipts.popitem(last=False)
    def snapshot(self,minds=None):
        residents=minds.model.residents if minds else {}
        targets=[{'id':k,'name':r['name']} for k,r in residents.items() if k in minds.present]
        self.names.update({r['name']:k for k,r in residents.items()})
        pending=(residents[minds.pending['key']]['name'] if minds.pending else
                 ('Cheese' if getattr(minds.game,'_pending_talk_future',None) else None)) if minds else None
        return dict(session=self.session,entries=list(self.entries),receipts=list(self.receipts.values()),
                    targets=targets,pending=pending,voice=dict(minds.voice) if minds else {})
