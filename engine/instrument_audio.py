"""Small deterministic instrument voices, owned by the game's safe mixer lifecycle."""
import array
import math
import threading
from collections import OrderedDict

def synthesize(voice,midi,hold,rate=44100,channels=2):
    hold=max(.06,min(3.,float(hold)));duration=hold+.25
    frequency=440*2**((int(midi)-69)/12)
    if voice=='drum':frequency=70+(int(midi)%6)*34
    n=int(rate*duration);buf=array.array('h');seed=9173+int(midi)*37
    for i in range(n):
        t=i/rate;phase=2*math.pi*frequency*t
        attack=min(1,t/(.035 if voice=='brass' else .005))
        release=max(0,min(1,(duration-t)/.2))
        if voice=='brass':value=(math.sin(phase)+.27*math.sin(phase*2)+.12*math.sin(phase*3))*.7
        elif voice in ('bell','gong','shell','tines'):
            a,b,decay={'bell':(2.76,5.4,1.4),'gong':(1.37,2.76,2.2),'shell':(1.55,3.8,.5),'tines':(2.,4.,.65)}[voice]
            value=(math.sin(phase)+.35*math.sin(phase*a)+.17*math.sin(phase*b))*.65*math.exp(-t/decay)
        elif voice in ('drum','tom','kick','snare','cymbal'):
            seed=(1664525*seed+1013904223)&0xffffffff;noise=seed/2147483648-1
            if voice=='cymbal':value=(noise*.4+math.sin(phase*2.7)*.2+math.sin(phase*4.4)*.2+math.sin(phase*6.2)*.1)*math.exp(-t*2.5)
            elif voice=='snare':value=(noise*.8+math.sin(phase)*.2)*math.exp(-t*14)
            elif voice in ('tom','kick'):value=(math.sin(phase*(1+.2*math.exp(-t*25)))*.8+noise*.08)*math.exp(-t*(7 if voice=='kick' else 5))
            else:value=(math.sin(phase*(1+.18*math.exp(-t*30)))*.55+noise*.45)*math.exp(-t*12)
        else:value=(math.sin(phase)+.3*math.sin(phase*2)+.09*math.sin(phase*4))*.7*math.exp(-t/1.1)
        sample=int(max(-1,min(1,value*attack*release))*.075*32767)
        for _ in range(channels):buf.append(sample)
    return buf.tobytes()

class InstrumentAudio:
    def __init__(self):
        self.lock=threading.RLock();self.active={};self.cache=OrderedDict();self.workers=set();self.closed=False

    def stop_except(self,sessions):
        with self.lock:
            for token,(session,cancel) in list(self.active.items()):
                if session not in sessions:cancel.set()

    def close(self):
        with self.lock:
            self.closed=True
            for session,cancel in self.active.values():cancel.set()
            workers=list(self.workers)
        for worker in workers:
            if worker is not threading.current_thread():worker.join()
        with self.lock:self.active.clear();self.workers.clear()

    def play(self,session,voice,midi,hold,velocity=.6):
        from audio.sound import sound_engine as sound
        if not sound.enabled or not sound._pygame_available or sound._audio_stopping.is_set():return
        token=object();cancel=threading.Event()
        with self.lock:
            if self.closed or len(self.active)>=12:return
            self.active[token]=(session,cancel)
        def run():
            channel=None
            try:
                import pygame
                settings=pygame.mixer.get_init()
                if not settings or settings[1]!=-16:return
                rate,_,channels=settings;key=(voice,int(midi),round(hold,2),rate,channels)
                with self.lock:pcm=self.cache.get(key)
                if pcm is None:
                    pcm=synthesize(voice,midi,hold,rate,channels)
                    with self.lock:
                        self.cache[key]=pcm
                        while len(self.cache)>64:self.cache.popitem(last=False)
                if cancel.is_set() or sound._audio_stopping.is_set() or not sound.enabled:return
                sample=pygame.mixer.Sound(buffer=pcm);channel=sample.play()
                if channel:
                    while channel.get_busy():
                        if cancel.is_set() or sound._audio_stopping.is_set() or not sound.enabled:
                            channel.fadeout(40);break
                        channel.set_volume(max(0,min(1,sound.volume*velocity)))
                        cancel.wait(.02)
            except Exception:
                # Device changes are a silent missed note, not a crashed game.
                pass
            finally:
                with self.lock:
                    self.active.pop(token,None);self.workers.discard(threading.current_thread())
        with self.lock:
            if self.closed:self.active.pop(token,None);return
            worker=sound._start_audio_worker(run)
            if worker is None:self.active.pop(token,None)
            else:self.workers.add(worker)
