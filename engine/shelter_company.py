"""Shared, physically arrived shelter moments. Never changes walking positions."""
import copy
import json
from pathlib import Path
from engine import shelters

SCORES=json.loads((Path(__file__).parent/'client/animation/home-company.json').read_text())

def residents(minds):
    if not minds.game:return {}
    result={k:r for k,r in minds.housing.items() if r['phase']=='inside'}
    p=minds.pond;plan=p.state.get('plan')
    if plan and not plan.get('paused') and plan['phase']=='act' and plan.get('residence',{}).get('inside'):
        r=plan['residence'];routine=r.get('routine')
        if (not routine or routine.get('done')) and p.game.duck.growth_stage!='egg':result['cheese']=r
    # Real coordinates must still be at the home, even before its owner has
    # processed a drag, removal, weather exit or visit replacement this frame.
    return {k:r for k,r in result.items() if k in minds.present and shelters.still_placed(p,r)
            and abs(minds.present[k][0]-r['destination'][0])+abs(minds.present[k][1]-r['destination'][1])*2<=3}

def available_scores(minds,a,b):
    p=minds.pond;ra=minds.model.residents[a];rb=minds.model.residents[b]
    result=['doorstep_forecast','polite_shuffle']
    if p.weather_type in ('thunderstorm','summer_storm','storm','stormy'):result.insert(0,'thunder_reassure')
    rain=any(v in p.weather_type for v in ('rain','drizzle','shower'))
    if rain:result.insert(0,'rain_count')
    if (rain or p.weather_type in ('hail','sleet')) and max(ra['traits']['curiosity'],rb['traits']['curiosity'])>.55:result.append('roof_rhythm')
    if p.hour>=20 or p.hour<6 or min(minds.context(a)['energy'],minds.context(b)['energy'])<.4:result.insert(0,'sleepy_company')
    return result

def for_actor(minds,key):
    return next((s for s in minds.house_scenes.values() if key in (s['a'],s['b'])),None)

def tick(minds,dt):
    current=residents(minds);busy=set()
    for pair,s in list(minds.house_scenes.items()):
        keys=(s['a'],s['b'])
        valid=all(k in current and minds.presence_tokens[k]==s['tokens'][k]
                  and current[k]['id']==s['home'] and current[k]['destination']==s['destination']
                  and current[k]['slot']==s['slots'][k] for k in keys)
        if not valid or s['performance'] not in available_scores(minds,*keys):
            minds.house_scenes.pop(pair);continue
        busy.update(keys);s['elapsed']=min(s['duration'],s['elapsed']+dt)
        if s['elapsed']<s['duration']:continue
        spec=SCORES[s['performance']]
        names=[minds.model.residents[k]['name'] for k in keys]
        note=' and '.join(names)+' '+spec['note']+' in the '+s['home'].replace('_',' ')+'.'
        learned=False
        for k,other in (keys,keys[::-1]):
            r=current[k];completed=r.setdefault('company_history',[])
            r['company_history']=(completed+[s['performance']])[-6:];r['company_after']=minds.now+24
            # A long storm can contain many visible moments, but one shelter
            # stay supplies at most one learning/bond outcome for each partner.
            token=other+':'+s['tokens'][other];seen=r.setdefault('company_partners',[])
            if token not in seen:
                minds.model.learn(k,'share',s['contexts'][k],.24,minds.now,note,other)
                minds.model.bond(k,other,.1,minds.now,note,False)
                r['company_partners']=(seen+[token])[-8:];learned=True
        if learned:minds.pond.remember('shared',note,.65,s['b'])
        minds.house_scenes.pop(pair);minds.pond._cache=None
    # Fixed slots determine facing and roles. No rendezvous or following Cheese.
    groups={}
    for key,r in current.items():
        if key in busy or minds.now<r.get('company_after',r.get('started',minds.now-7)+6):continue
        groups.setdefault((r['id'],tuple(r['destination'])),[]).append(key)
    for (home,destination),keys in groups.items():
        keys.sort(key=lambda k:(len(current[k].get('company_history',[])),current[k].get('company_after',0),current[k]['slot']))
        for n in range(0,len(keys)-1,2):
            a,b=sorted(keys[n:n+2],key=lambda k:current[k]['slot']);ra,rb=current[a],current[b]
            choices=available_scores(minds,a,b)
            recent=ra.get('company_history',[])[-2:]+rb.get('company_history',[])[-2:]
            kind=next((k for k in choices if k not in recent),choices[0])
            minds.house_scenes[a+'|'+b]={'a':a,'b':b,'performance':kind,'phase':'act','elapsed':0.,
                'duration':SCORES[kind]['duration'],'home':home,'destination':list(destination),
                'slots':{a:ra['slot'],b:rb['slot']},'tokens':{k:minds.presence_tokens[k] for k in (a,b)},
                'contexts':{k:minds.context(k) for k in (a,b)}}
            minds.pond._cache=None

def snapshot(minds):
    return [{k:copy.deepcopy(s[k]) for k in ('a','b','performance','phase','elapsed','duration','home','destination','slots')}
            for s in minds.house_scenes.values()]
