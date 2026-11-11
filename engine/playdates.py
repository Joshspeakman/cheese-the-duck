"""Two real residents sharing one real toy, with bounded completed experiences."""
import copy
import json
from pathlib import Path
from engine import shelters
from engine.visitor_shelters import departing, distance

SCORES=json.loads((Path(__file__).parent/'client/animation/playdates.json').read_text())
TOYS={'toy_seesaw':'seesaw','toy_sandbox':'sandbox','toy_ball':'ball','ball':'ball',
      'toy_trampoline':'trampoline','trampoline':'trampoline'}
MASS={'egg':.2,'hatchling':.3,'duckling':.45,'juvenile':.7,'young_adult':.9,
      'adult':1.,'mature':1.1,'elder':1.,'legendary':1.1}

def active(minds,key):
    p=minds.pond.state.get('plan');scene=p.get('company') if p else None
    return scene if scene and not scene.get('done') and key in ('cheese',scene['partner']) else None

def choose(pond,plan):
    if plan['target'] not in TOYS or plan['target'] not in pond.placed or shelters.adverse(pond.weather_type):return None
    minds=pond.minds;minds.sync();candidates=[];pos=pond.game.renderer.duck_pos
    for key,point in minds.present.items():
        if key=='cheese' or key in minds.housing or key in minds.furnishings or key in minds.gardening or key in minds.musicians or minds.encounter_for(key) or departing(minds,key):continue
        resident=minds.model.residents[key]
        if resident['energy']<.25 or resident['social']<.15:continue
        if distance(point,plan['destination'])>55:continue
        candidates.append((distance(point,plan['destination'])-resident['traits']['sociability']*8,key))
    if not candidates:return None
    _,partner=min(candidates);family=TOYS[plan['target']]
    # Both actors approach the fixed item, never a moving Cheese coordinate.
    destination=list(plan['destination']);spot=[destination[0]+5,destination[1]]
    if spot[0]>pos._play_width-8:spot[0]=destination[0]-5
    if not (2<=spot[0]<=pos._play_width-8 and 2<=spot[1]<=pos._play_height-5):return None
    stage=pond.game.duck.growth_stage;resident=minds.model.residents[partner]
    from world.guest_cast import guest_profile
    profile=guest_profile(resident['cast']) or {};species=profile.get('species','duck')
    adult=stage not in ('hatchling','duckling','elder','legendary')
    last=pond.state['objects'][plan['target']].get('last_playdate')
    options=[k for k,s in SCORES.items() if s['family']==family]
    if family=='seesaw' and (not adult or resident['traits']['confidence']<.4):options=['seesaw_gentle']
    if family=='ball' and (not adult or pond.state['objects'][plan['target']].get('wetness',0)>.4):options=['ball_pass']
    kind=next((k for k in options if k!=last),options[0])
    return {'id':kind,'label':SCORES[kind]['label'],'partner':partner,'token':minds.presence_tokens[partner],
            'destination':destination,'spot':spot,'location':pond.location,'phase':'approach','elapsed':0.,'waited':0.,
            'duration':SCORES[kind]['duration'],'done':False,'young':not adult,
            'mass':[MASS.get(stage,1),{'goose':1.5,'crow':.65,'owl':.8,'toad':.6,'butterfly':.1,'duckling':.45}.get(species,1)],
            'contexts':{k:minds.context(k) for k in ('cheese',partner)}}

def advance(pond,plan,dt):
    if plan['kind']!='item' or plan['target'] not in TOYS or plan['phase']!='act':return False
    minds=pond.minds;scene=plan.get('company')
    if scene is None and not plan.get('company_tried'):
        plan['company_tried']=True;scene=choose(pond,plan)
        if scene:plan['company']=scene;pond._cache=None
    if not scene or scene.get('done'):return False
    key=scene['partner']
    valid=(key in minds.present and minds.presence_tokens[key]==scene['token'] and key not in minds.housing
           and not departing(minds,key) and pond.location==scene['location'] and not shelters.adverse(pond.weather_type)
           and shelters.still_placed(pond,{'id':plan['target'],'destination':scene['destination']}))
    if not valid:
        scene.update(done=True,phase='cancelled');return False
    if distance(minds.present['cheese'],scene['destination'])>3:
        scene.update(done=True,phase='cancelled');return False
    if scene['phase']=='approach':
        scene['waited']+=dt
        if scene['waited']>45:scene.update(done=True,phase='cancelled');return False
        if distance(minds.present[key],scene['spot'])<=1.2:
            scene.update(phase='enter',elapsed=0.)
        return True
    if distance(minds.present[key],scene['spot'])>3:
        scene.update(done=True,phase='cancelled');return False
    scene['elapsed']+=dt
    if scene['phase']=='enter':
        if scene['elapsed']>=3:scene.update(phase='act',elapsed=0.)
        return True
    if scene['phase']=='act' and scene['elapsed']>=scene['duration']:
        scene.update(phase='exit',elapsed=0.)
        note='Cheese and '+minds.model.residents[key]['name']+' '+SCORES[scene['id']]['note']+'.'
        for actor,other in [('cheese',key),(key,'cheese')]:
            minds.model.learn(actor,'share',scene['contexts'][actor],.35,minds.now,note,other)
            minds.model.bond(actor,other,.15,minds.now,note,False)
        obj=pond.state['objects'][plan['target']]
        obj['last_playdate']=scene['id'];obj['playdates']=min(9999,obj.get('playdates',0)+1)
        if TOYS[plan['target']]=='sandbox':obj['sandwork']=scene['id']
        pond.remember('shared',note,.75,key);pond._cache=None
    elif scene['phase']=='exit' and scene['elapsed']>=3:
        scene.update(done=True,phase='done');return False
    return True

def motion(minds,key):
    scene=active(minds,key)
    if not scene or key=='cheese':return None
    plan=minds.pond.state['plan']
    if plan.get('paused'):return None
    return {'target':list(scene['spot']),'facing':False,'phase':scene['phase'],
            'gesture':'walking' if scene['phase'] in ('enter','exit') else 'idle'}

def view(plan):
    scene=plan.get('company')
    if not scene:return None
    return {k:copy.deepcopy(v) for k,v in scene.items() if k not in ('contexts','token')}
