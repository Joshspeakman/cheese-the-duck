"""Exact regular, rare and story scalar adapters; never write actor positions."""
from world.friends import visitor_animator
from world.guest_cast import guest_profile


def regular(pond):
    g=pond.game;visit=g.friends.current_visit
    if not visit:return None
    friend=g.friends.get_friend_by_id(visit.friend_id)
    if not friend:return None
    cast=guest_profile(friend.name)
    personality=friend.personality.value if hasattr(friend.personality,'value') else str(friend.personality)
    if (not cast or cast.get('rare') or cast.get('species')!='duck'
        or visitor_animator._friend_name!=friend.name or visitor_animator._personality!=personality.lower()
        or visitor_animator._is_leaving):return None
    return dict(actor=friend.id,cast=cast['id'],adapter='regular',token=str(visit.started_at),location=pond.location,
                root=[float(visitor_animator._position_x+g.renderer._camera_x),float(visitor_animator._position_y+g.renderer._camera_y)],
                facing=getattr(visitor_animator,'_facing_right',False))


def stop_regular(pond,actor):
    """Release yesterday's destination, without teleporting or extending a visit."""
    live=regular(pond)
    if live and live['actor']==actor:
        visitor_animator._target_x=visitor_animator._position_x
        visitor_animator._target_y=visitor_animator._position_y
        visitor_animator._rest_until=max(visitor_animator._rest_until,visitor_animator._last_move_time+.3)


def _release_regular(pond,actor,lease):
    """Drop only this attempt's old motion intent, including a replaced token."""
    live=regular(pond)
    if not live or live['actor']!=actor:return
    if live['token']==lease.get('token'):
        stop_regular(pond,actor);return
    meeting=getattr(visitor_animator,'_mind_motion',{}).get('meeting',{})
    target=lease.get('target')
    actual=[visitor_animator._target_x+pond.game.renderer._camera_x,visitor_animator._target_y+pond.game.renderer._camera_y]
    if (isinstance(meeting,dict) and meeting.get('owner')==lease.get('attempt') and isinstance(target,list) and len(target)==2
        and all(abs(actual[i]-target[i])<1e-7 for i in (0,1))):stop_regular(pond,actor)


SPECIAL=('traveling_merchant','celebrity_duck','lost_duckling')
IDENTITY=('actor','cast','adapter','token','location')


def identity(actor):
    keys=IDENTITY+({'rare':('motion_token',),'story':('motion_token','story_step','render_id')}.get(actor['adapter'],()))
    return {k:actor[k] for k in keys}


def rare(pond):
    import json,math
    from datetime import datetime
    g=pond.game;visit=getattr(g.atmosphere,'current_visitor',None);m=getattr(g,'guest_motion',None)
    if not visit or not m:return None
    visitor,arrival=visit
    if visitor.id not in SPECIAL:return None
    area=getattr(g.exploration,'current_area',None)
    token=(visitor.id,arrival,getattr(area,'id',getattr(area,'name','pond')))
    a=m.actor
    try:
        remaining=visitor.stay_duration_hours*3600-(datetime.now()-datetime.fromisoformat(arrival)).total_seconds()
        if not math.isfinite(remaining) or remaining<=6 or m.token!=token or not a or a['id']!=visitor.id or a.get('castId')!=visitor.id:return None
        root=[float(a['x']),float(a['y'])]
        if not all(math.isfinite(v) for v in root):return None
    except (ValueError,TypeError,KeyError):return None
    return dict(actor=visitor.id,cast=visitor.id,adapter='rare',token=arrival,location=pond.location,
                motion_token=json.dumps(token),root=root,facing=a['facing'],remaining_seconds=remaining)


def story(pond):
    import json,math
    g=pond.game;s=pond.state.get('story');m=getattr(g,'story_motion',None);area=getattr(g.exploration,'current_area',None)
    if not isinstance(s,dict) or s.get('id')!='lost_duckling' or not m or (area and area.name!='Home Pond'):return None
    token=(id(g.duck),id(s),s['id']);a=m.actor
    if m.token!=token or m.step!=s.get('step') or not a or a.get('id')!='story:lost_duckling' or a.get('storyId')!='lost_duckling':return None
    try:
        root=[float(a['x']),float(a['y'])]
        if not all(math.isfinite(v) for v in root):return None
    except (ValueError,TypeError,KeyError):return None
    return dict(actor='story:pip',cast='lost_duckling',adapter='story',token=str(id(s)),location=pond.location,
                motion_token=json.dumps(token),story_step=str(s['step']),render_id='story:lost_duckling',root=root,facing=a['facing'])


def candidates(pond):return [a for a in (regular(pond),rare(pond),story(pond)) if a]


def live(pond,operator):
    if not isinstance(operator,dict):return None
    getter={'regular':regular,'rare':rare,'story':story}.get(operator.get('adapter'))
    a=getter(pond) if getter else None
    return a if a and identity(a)==operator else None


def release_owned(pond,actor,lease):
    adapter=lease.get('contract',{}).get('operator',{}).get('adapter')
    if adapter=='regular':return _release_regular(pond,actor,lease)
    mover=getattr(pond.game,{'rare':'guest_motion','story':'story_motion'}.get(adapter,''),None)
    if mover:mover.release_meeting(lease.get('attempt'))
