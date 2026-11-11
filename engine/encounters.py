"""Transient rendezvous and paired activities, driven only by simulation time.

Each participant walks to a fixed reservation. Visit tokens prevent a later
visitor inheriting an unfinished scene. Only completed scenes teach memories.
"""
import math
from engine.shelters import adverse

DURATIONS = {'greeting':12, 'call_response':18, 'wing_bump':12, 'shy_hello':16,
             'pebble_inspection':22, 'duet':24, 'crumb_search':24, 'puddle_splash':20,
             'leaf_chase':22, 'snow_tracks':24, 'stargaze':28, 'sunbeam_doze':26}

def distance(a,b):return math.hypot(a[0]-b[0],(a[1]-b[1])*2)

def performance(minds,a,b,action):
    p=minds.pond; ra,rb=minds.model.residents[a],minds.model.residents[b]
    warmth=ra['relationships'].get(b,{}).get('warmth',.3)
    if p.hour<6 or p.hour>=20:return 'stargaze' if not adverse(p.weather_type) else 'call_response'
    if 'snow' in p.weather_type and p.weather_type!='heavy_snow':return 'snow_tracks'
    if p.weather_type in ('drizzle','rainy','spring_showers'):return 'puddle_splash'
    if p.season=='fall' and action in ('forage','practice'):return 'leaf_chase'
    if action=='practice':return 'duet'
    if action=='forage':return 'crumb_search'
    if action=='observe':return 'pebble_inspection'
    if min(ra['traits']['confidence'],rb['traits']['confidence'])<.35:return 'shy_hello'
    if warmth>.65:return 'wing_bump'
    if max(ra['energy'],rb['energy'])<.4:return 'sunbeam_doze'
    return 'greeting'

def create(minds,a,b,action,reward):
    p=minds.pond
    if any(k in (c['a'],c['b']) for c in minds.coactivities.values() for k in (a,b)):
        return None
    if 'cheese' in (a,b) and (p.state['plan'] or not p.available()):return None
    pa,pb=minds.present[a],minds.present[b]
    r=minds.game.renderer;cx=getattr(r,'_camera_x',0);cy=getattr(r,'_camera_y',0)
    x=max(cx+14,min(cx+getattr(r,'_viewport_width',132)-18,(pa[0]+pb[0])/2))
    y=max(cy+5,min(cy+getattr(r,'_viewport_height',42)-8,(pa[1]+pb[1])/2))
    # The meeting place stays fixed even if someone is moved or leaves.
    spots={a:[round(x-5),round(y)],b:[round(x+5),round(y)]}
    if 'cheese' in spots:
        pos=r.duck_pos;dest=spots['cheese']
        if pos.frozen or not (2<=dest[0]<=pos._play_width-8 and 2<=dest[1]<=pos._play_height-5):return None
    kind=performance(minds,a,b,action)
    result={'a':a,'b':b,'action':action,'performance':kind,'phase':'approach',
            'created':minds.now,'duration':DURATIONS[kind],'elapsed':0.,'spots':spots,
            'location':p.location,'tokens':{k:minds.presence_tokens[k] for k in (a,b)},
            'reward':reward,'contexts':{a:minds.context(a),b:minds.context(b)}}
    if 'cheese' in spots:
        minds.game.behavior_ai.cancel_pending_movement();minds.game.behavior_ai.clear_action()
        r.duck_pos.move_to(*spots['cheese'])
        if [r.duck_pos.target_x,r.duck_pos.target_y]!=spots['cheese']:return None
    return result

def advance(minds,scene,dt):
    """Return running, cancelled, or completed; no rewards are applied here."""
    p=minds.pond; keys=(scene['a'],scene['b'])
    if scene['location']!=p.location or any(k not in minds.present or minds.presence_tokens[k]!=scene['tokens'][k] for k in keys):return 'cancelled'
    if 'cheese' in keys and (not p.available() or p.state['plan']):return 'cancelled'
    visit=minds.game.friends.current_visit
    if visit and visit.friend_id in keys:
        from world.friends import visitor_animator
        if visitor_animator._is_leaving:return 'cancelled'
    rare=minds.game.guest_motion.actor
    if rare and rare['id'] in keys and rare.get('state')=='leaving':return 'cancelled'
    positions=[distance(minds.present[k],scene['spots'][k]) for k in keys]
    if scene['phase']=='approach':
        if minds.now-scene['created']>45:return 'cancelled'
        if 'cheese' in keys and distance(minds.present['cheese'],scene['spots']['cheese'])<=2 and not scene.get('waiting'):
            pos=minds.game.renderer.duck_pos;pos.cancel_movement();pos.set_state_by_name('thinking',50)
            scene['waiting']=True
        if max(positions)<=2:
            scene['phase']='act';scene['elapsed']=0.
            if 'cheese' in keys:
                pos=minds.game.renderer.duck_pos;pos.cancel_movement();pos.set_state_by_name('thinking',scene['duration']+2)
    else:
        if max(positions)>5:return 'cancelled'
        scene['elapsed']=min(scene['duration'],scene['elapsed']+dt)
        if scene['elapsed']>=scene['duration']:return 'completed'
    return 'running'

def snapshot(scene):
    return {k:scene[k] for k in ('a','b','performance','phase','spots','elapsed','duration')}
