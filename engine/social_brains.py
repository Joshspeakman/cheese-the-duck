"""Small, persistent contextual learning models. No network or language-model dependency.

Each resident learns its own action-value vectors from completed experiences.
Memory and relationships belong to the resident, not to the shared speech model.
All mutation occurs on the simulation thread; prompts/snapshots are copies.
"""
import copy
import hashlib
import math
import re

ACTIONS = ('rest', 'wander', 'observe', 'forage', 'practice', 'restore', 'garden', 'share', 'item', 'chat')
TRAITS = ('curiosity', 'sociability', 'confidence', 'patience', 'care')
AFFINITY = {'rest': 'patience', 'wander': 'confidence', 'observe': 'curiosity',
            'forage': 'curiosity', 'practice': 'confidence', 'restore': 'care',
            'garden': 'patience', 'share': 'sociability', 'item': 'curiosity', 'chat': 'sociability'}
HOBBIES = {'adventurous':'wander', 'scholarly':'observe', 'artistic':'practice',
           'playful':'share', 'mysterious':'observe', 'generous':'restore', 'foodie':'forage', 'athletic':'wander'}
WORDS = {'rest': ('rest','nap','quiet','sleep'), 'wander': ('walk','explore','adventure','travel'),
         'observe': ('read','book','stars','science','bird','watch'), 'forage': ('food','snack','crumb','cook'),
         'practice': ('music','sing','dance','paint','art'), 'restore': ('clean','help','repair'),
         'garden': ('garden','flower','plant','grow'), 'share': ('friend','together','company','picnic')}
LABELS = {'rest':'quiet time', 'wander':'exploring', 'observe':'noticing little things',
          'forage':'finding treats', 'practice':'making things & music', 'restore':'helping the pond',
          'garden':'gardening', 'share':'company', 'item':'familiar belongings', 'chat':'conversation'}


def clamp(n, lo=0., hi=1.): return max(lo, min(hi, float(n)))
def stable(value): return int(hashlib.sha256(str(value).encode()).hexdigest()[:12], 16)
def tokens(text): return set(re.findall(r"[a-z]{3,}", str(text).lower()))
def player_claim(message):
    """An attributed player statement, usable in a prompt before it is saved."""
    message=str(message).strip()[:1000]
    declaration=(r'\b(?:my name is|call me|i (?:love|like|hate|prefer|enjoy|remember)|remember that)\s+\w'
                 r'|\bmy favou?rite(?:\s+[\w\x27-]+){0,5}\s+(?:is|are)\s+\w')
    if re.search(declaration,message,re.I):
        return 'You said: '+message[:300]
    return ''
def action_key(action):
    return {'feed':'forage','play':'practice','clean':'restore','pet':'share','sleep':'rest',
            'talk':'chat','explore':'wander','project':'restore','repair_item':'restore',
            'clean_item':'restore'}.get(action, action if action in ACTIONS else 'item')


def features(context):
    """Nine bounded, meaningful context features plus a bias."""
    return [1., clamp(context.get('energy', .7)), clamp(context.get('social', .7)),
            clamp(context.get('fun', .7)), clamp(context.get('storm', 0)),
            clamp(context.get('night', 0)), clamp(context.get('company', 0)),
            clamp(context.get('familiarity', 0)), clamp(context.get('flowers', .4)),
            clamp(context.get('litter', .1))]


class Minds:
    def __init__(self, state):
        self.state = state
        state.setdefault('version', 1)
        state.setdefault('residents', {})
        state.setdefault('exchanges', [])
        state.setdefault('serial', 0)
        state.setdefault('next_social', 35.)
        state['exchanges'] = state['exchanges'][-60:]
        self.residents = state['residents']

    def ensure(self, key, name, profile=None):
        if key in self.residents: return self.residents[key]
        profile = profile or {}
        seed = stable(key + name)
        core = {t: .25 + ((seed >> (i*7)) % 61)/100 for i,t in enumerate(TRAITS)}
        archetype = profile.get('archetype', 'playful')
        hobby = HOBBIES.get(archetype, 'observe')
        core[AFFINITY[hobby]] = max(.72, core[AFFINITY[hobby]])
        if key == 'cheese': core.update(curiosity=.78,confidence=.66,patience=.35,sociability=.54)
        likes = {a: ((stable(key+a)%41)-20)/100 for a in ACTIONS}
        likes[hobby] = .6
        resident = dict(id=key,name=name,cast=profile.get('id',''),archetype=archetype,
            core=core,traits=dict(core),interests=likes,
            weights={a:[0.]*10 for a in ACTIONS},counts={a:0 for a in ACTIONS},
            memories=[],facts=[],relationships={},experiences=0,changes=[],
            goal={'action':hobby,'done':0,'target':4},last_action=None,last_feedback=-1000.,
            mood=.5,energy=.8,social=.7,last_decision=-1000.)
        self.residents[key] = resident
        return resident

    def relationship(self, key, other):
        r=self.residents[key]
        return r['relationships'].setdefault(other,dict(trust=.3,warmth=.3,familiarity=0.,friction=0.,meetings=0))

    def bond(self, key, other, reward, at, note, record=True):
        rel=self.relationship(key,other)
        rel['familiarity']=clamp(rel['familiarity']+.018)
        rel['trust']=clamp(rel['trust']+reward*.018)
        rel['warmth']=clamp(rel['warmth']+reward*.025)
        rel['friction']=clamp(rel['friction']-reward*.02)
        rel['meetings']+=1
        if record:self.remember(key,'relationship',note,at,.65,other)
        return rel

    def remember(self, key, kind, text, at, salience=.5, other=''):
        r=self.residents[key];text=str(text).strip()[:600]
        if not text:return
        recent=r['memories'][-1:]
        if recent and recent[0]['text']==text and at-recent[0]['at']<60:return
        self.state['serial']+=1
        r['memories'].append(dict(id=self.state['serial'],kind=kind,text=text,at=float(at),salience=clamp(salience),other=other))
        # Recent experiences plus salient older milestones survive ordinary chatter.
        if len(r['memories'])>64:
            older=sorted(r['memories'][:-32],key=lambda m:m['salience']-.00002*max(0,at-m['at']),reverse=True)[:32]
            r['memories']=sorted(older+r['memories'][-32:],key=lambda m:m['id'])

    def recall(self, key, query, at, other='', limit=6):
        q=tokens(query)
        def score(m):
            overlap=len(q & tokens(m['text']))/max(1,math.sqrt(len(q)))
            return overlap+(.7 if other and m['other']==other else 0)+m['salience']+.5/(1+max(0,at-m['at'])/900)
        chosen=sorted(self.residents[key]['memories'],key=score,reverse=True)[:limit]
        return copy.deepcopy(sorted(chosen,key=lambda m:m['id']))

    def value(self, key, action, context):
        r=self.residents[key];action=action_key(action);x=features(context)
        learned=sum(w*f for w,f in zip(r['weights'][action],x))
        intrinsic=r['interests'][action]*.5+(r['traits'][AFFINITY[action]]-.5)*.3
        return clamp(learned+intrinsic,-1.5,1.5)

    def rank(self, key, actions, context, at):
        r=self.residents[key]
        rows=[]
        for action in actions:
            a=action_key(action)
            novelty=.12/math.sqrt(1+r['counts'][a])
            jitter=(stable((key,a,int(at/40)))%101)/2000
            urgent=(1-context.get('energy',.7))*1.4 if a=='rest' else (1-context.get('social',.7))*.7 if a=='share' else 0
            if context.get('storm') and a=='rest':urgent+=.5
            score=self.value(key,a,context)+novelty+jitter+urgent
            rows.append((score,a))
        return sorted(rows,reverse=True)

    def learn(self, key, action, context, reward, at, note, other=''):
        r=self.residents[key];a=action_key(action);reward=clamp(reward,-1,1);x=features(context)
        weights=r['weights'][a];prediction=sum(w*f for w,f in zip(weights,x))
        # Normalized online least-mean-squares. Actual outcome, not generated text,
        # supplies the target. Context-specific experience can reverse a prior.
        rate=.22/(1+.012*r['counts'][a]);error=reward-prediction;norm=sum(f*f for f in x)+.1
        r['weights'][a]=[clamp(w+rate*error*f/norm,-2,2) for w,f in zip(weights,x)]
        r['counts'][a]+=1;r['experiences']+=1
        r['interests'][a]=clamp(r['interests'][a]+.025*(reward-r['interests'][a]),-1,1)
        t=AFFINITY[a];before=r['traits'][t]
        # Core temperament remains recognizable; growth is slow and bounded.
        r['traits'][t]=clamp(before+.0025*reward,.08,.92)
        r['traits'][t]=clamp(r['traits'][t],max(.08,r['core'][t]-.23),min(.92,r['core'][t]+.23))
        r['mood']=clamp(r['mood']*.92+(.5+reward*.5)*.08)
        r['last_action']=dict(action=a,context=dict(context),at=at,reward=reward,note=note)
        self.remember(key,'experience',note,at,.55+abs(reward)*.2,other)
        if r['counts'][a] in (3,8,20,50) or (r['counts'][a]>50 and r['counts'][a]%50==0):
            r['changes']=(r['changes']+[dict(at=at,text=('Growing fond of ' if r['interests'][a]>0 else 'Learning when to avoid ')+LABELS[a]+'.',reason=note)])[-12:]
        goal=r['goal']
        if a==goal['action'] and reward>0:
            goal['done']+=1
            if goal['done']>=goal['target']:
                self.remember(key,'milestone','Followed through on a personal goal: '+LABELS[a]+'.',at,.95)
                favorite=max(ACTIONS,key=lambda k:r['interests'][k]+.25/math.sqrt(r['counts'][k]+1))
                r['goal']={'action':favorite,'done':0,'target':min(12,4+r['experiences']//30)}
        return error

    def heard_player(self, key, message, context, at):
        r=self.residents[key];message=str(message).strip()[:1000]
        self.remember(key,'player','You said: '+message,at,.72,'player')
        # Keep explicitly volunteered player facts, attributed as claims. No model
        # output is ever promoted into a fact about the player or game.
        claim=player_claim(message)
        if claim:
            fact={'text':claim,'at':at}
            if not any(f['text']==fact['text'] for f in r['facts']):r['facts']=(r['facts']+[fact])[-12:]
        # Conversation itself builds familiarity. Swearing is not a dislike signal.
        self.bond(key,'player',.18,at,'Spent time talking with you.',False)
        self.learn(key,'chat',context,.2,at,'You made time to talk.', 'player')

    def feedback(self,key,positive,at):
        r=self.residents[key];last=r['last_action']
        if not last or at-last['at']>300:return False,'Share an activity or conversation first.'
        if at-r['last_feedback']<20 or last.get('reviewed'):return False,'Let that encouragement settle first.'
        last['reviewed']=True;r['last_feedback']=at
        note='You encouraged '+LABELS[last['action']]+'.' if positive else 'You asked for a different approach to '+LABELS[last['action']]+'.'
        self.learn(key,last['action'],last['context'],.85 if positive else -.65,at,note,'player')
        r['last_action']['reviewed']=True
        # Feedback concerns an activity, not unconditional friendship manipulation.
        return True,note

    def snapshot(self, key, present=False):
        r=self.residents[key]
        return dict(id=key,name=r['name'],cast=r['cast'],present=present,experiences=r['experiences'],
            traits=[dict(name=t,value=r['traits'][t],change=r['traits'][t]-r['core'][t]) for t in TRAITS],
            interests=[dict(id=a,name=LABELS[a],value=v) for a,v in sorted(r['interests'].items(),key=lambda x:x[1],reverse=True)[:4]],
            goal={**r['goal'],'label':LABELS[r['goal']['action']]},changes=copy.deepcopy(r['changes'][-4:]),
            memories=copy.deepcopy(r['memories'][-8:]),facts=copy.deepcopy(r['facts']),
            relationships=[dict(id=k,name=self.residents.get(k,{}).get('name','You' if k=='player' else k),**v) for k,v in r['relationships'].items()],
            last_action=copy.deepcopy(r['last_action']),mood=r['mood'])
