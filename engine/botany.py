"""Persistent rooted plants. Cut ingredients and stored plants do not grow."""
import json
from pathlib import Path
BLUEPRINTS=json.loads((Path(__file__).parent/'client/animation/botanical.json').read_text())
ROOTED={k:v for k,v in BLUEPRINTS.items() if v['rooted']}

def clamp(v,lo=0.,hi=1.):return min(hi,max(lo,v))

def state(obj):
    value=obj.setdefault('botany',{})
    for key,default in dict(moisture=.55,health=.9,bloom=.65,care_count=0,last_care=None).items():
        value.setdefault(key,default)
    return value

def update(pond,item,obj,minutes,rain,intensity,temperature,ecology=None):
    if item not in ROOTED or item not in pond.placed:return
    p=ROOTED[item];b=state(obj);e=ecology if ecology is not None else pond.state['ecology']
    minutes=max(0,minutes)
    succulent=p['type']=='succulent';container=p['container'] in ('pot','dish')
    # Pots dry faster than rooted soil; cacti retain moisture. Storage freezes
    # these biological clocks without inventing growth or offline rewards.
    evaporation=.003*(1+max(0,temperature-12)/18)*(1+e['wind']*.5)*(1.4 if container else .7)*(.3 if succulent else 1)
    absorption=.03*intensity if rain and temperature>0 else 0
    b['moisture']=clamp(b['moisture']+minutes*(absorption-evaporation))
    low,high=(.08,.72) if succulent else (.4,.98) if item in ('willow_tree','mushroom_patch','venus_flytrap') else (.25,.88)
    stress=max(0,low-b['moisture'])+max(0,b['moisture']-high)*.8
    b['health']=clamp(b['health']+minutes*(.0006 if stress==0 else -.002*stress),.15,1)
    dormant=getattr(pond,'season','spring')=='winter' or temperature<3
    if not dormant and low<=b['moisture']<=high:
        obj['growth']=clamp(obj.get('growth',.35)+minutes*.0015*b['health']*e['soil'])
    target=0. if dormant else b['health']*clamp(obj.get('growth',.35)*1.4)
    if item in ('tree_cherry','cherry_tree') and getattr(pond,'season','spring')!='spring':target*=.2
    b['bloom']=clamp(b['bloom']+(target-b['bloom'])*min(1,minutes*.02))

def care_mode(pond,item):
    b=state(pond.state['objects'][item])
    game=getattr(pond,'game',None)
    thirsty_crops=item=='garden_plot' and game and any(p.is_unlocked and p.needs_water for p in game.garden.plots.values())
    if (thirsty_crops or b['moisture']<(.25 if ROOTED[item]['type']=='succulent' else .5)) and pond.state['ecology']['water']>.15 and pond.state['ecology']['temperature']>3:
        return 'water'
    if pond.state['objects'][item]['dirt']>.25:return 'brush'
    return 'inspect'

def complete(pond,plan):
    item=plan['target']
    if item not in ROOTED or plan['kind']!='item' or plan.get('plant_care_done'):return
    # Re-entrant callbacks cannot water twice. The activity lifecycle additionally
    # consumes its plan before any reward or learning callbacks are invoked.
    plan['plant_care_done']=True
    if item not in pond.placed:return
    b=state(pond.state['objects'][item]);mode=plan.get('plant_care','inspect')
    if mode=='water':
        e=pond.state['ecology']
        if e['water']<=.15 or e['temperature']<=3:return
        target=.4 if ROOTED[item]['type']=='succulent' else .72
        amount=max(0,target-b['moisture'])
        # Fill only what the soil can hold; the water comes from this pond.
        b['moisture']+=amount;e['water']=clamp(e['water']-amount*.006)
        game=getattr(pond,'game',None)
        if item=='garden_plot' and game:
            for plot in game.garden.plots.values():
                if not plot.is_unlocked or not plot.needs_water or e['water']<=.15:continue
                before=plot.plant.water_level
                game._garden_water(plot.plot_id)
                e['water']=clamp(e['water']-max(0,plot.plant.water_level-before)/100*.006)
    elif mode=='brush':pond.state['objects'][item]['dirt']=max(0,pond.state['objects'][item]['dirt']-.3)
    b['care_count']=min(99999,b['care_count']+1);b['last_care']=mode
