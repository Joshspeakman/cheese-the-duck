"""Exact regular-visitor scalar adapter; never writes an actor position."""
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


def release_owned(pond,actor,lease):
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
