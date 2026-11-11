"""Live, bounded rare-guest movement. Uses simulation updates, never render calls.

This is transient staging, not a new friendship/save authority. It follows the
existing visitor's arrival/departure token and resets safely between locations.
"""
from datetime import datetime
import math
import random
import time
from world.guest_cast import guest_profile


def clamp(value, low, high):
    return max(low, min(value, max(low, high)))


def roaming_target(rng, bounds, position, cheese, social=0):
    """Choose a destination once, then walk there independently of Cheese."""
    left, right, top, bottom = bounds
    if rng.random() < min(.15, social * .25):
        return (clamp(cheese[0] + rng.choice((-1, 1)) * rng.uniform(6, 12), left, right),
                clamp(cheese[1] + rng.uniform(-4, 4), top, bottom))
    # Most outings cross the habitat; short local investigations add variety.
    for _ in range(12):
        if rng.random() < .3:
            x, y = position[0] + rng.uniform(-18, 18), position[1] + rng.uniform(-8, 8)
        else:
            x, y = rng.uniform(left, right), rng.uniform(top, bottom)
        target = (clamp(x, left, right), clamp(y, top, bottom))
        if math.hypot(target[0] - position[0], (target[1] - position[1]) * 2) > 8:
            return target
    return ((left + right) / 2, (top + bottom) / 2)


class GuestMotion:
    def __init__(self):
        self.token = None
        self.actor = None
        self.last = None
        self.target = None
        self.rest_until = 0.0
        self.reaction_seen = 0.0
        self.reaction_until = 0.0
        self.rng = random.Random(0)

    def tick(self, game, now=None):
        now = time.monotonic() if now is None else now
        dt = min(.25, max(0.0, now - self.last)) if self.last is not None else 0.0
        self.last = now
        visit = getattr(game.atmosphere, 'current_visitor', None)
        if not visit or not game.duck:
            self.token = self.actor = None
            return
        if game._state != 'playing':
            # Pause gesture timers with the game, rather than expiring in menus.
            self.rest_until += dt
            self.reaction_until += dt
            return
        visitor, arrival = visit
        area = getattr(game.exploration, 'current_area', None)
        token = (visitor.id, arrival, getattr(area, 'id', getattr(area, 'name', 'pond')))
        p = guest_profile(visitor.id)
        if not p:
            self.actor = None
            return
        renderer = game.renderer
        pos = renderer.duck_pos
        cx, cy = getattr(renderer, '_camera_x', 0), getattr(renderer, '_camera_y', 0)
        width, height = getattr(renderer, '_viewport_width', 132), getattr(renderer, '_viewport_height', 42)
        bounds = (cx + 5, cx + width - 7, cy + 2, cy + height - 4)
        def point(x, y):
            return (clamp(x, bounds[0], bounds[1]), clamp(y, bounds[2], bounds[3]))
        if token != self.token:
            self.token = token
            self.rng.seed('|'.join(map(str, token)))
            x, y = point(pos.x + p['radius'] + 12, pos.y - 2)
            self.actor = dict(id=visitor.id, castId=visitor.id, name=visitor.name,
                              x=x, y=y, state='arriving', activity='arriving', facing=False)
            self.target = point(pos.x + 6, pos.y)
            self.rest_until = self.reaction_until = now
            self.reaction_seen = getattr(game.atmosphere, 'visitor_interacted_at', 0)
        a = self.actor
        mind = game.living_pond.minds.motion(visitor.id) if getattr(game, 'living_pond', None) else {}
        pace = p['pace'] * mind.get('pace', 1)
        self.target = point(*self.target)
        # Camera movement is not a teleport: walk back into the current viewport.
        reaction = getattr(game.atmosphere, 'visitor_interacted_at', 0)
        if reaction > self.reaction_seen:
            self.reaction_seen = reaction
            self.reaction_until = now + 3.2
            self.rest_until = max(self.rest_until, now + 3.2)
        leaving = False
        try:
            remaining = visitor.stay_duration_hours * 3600 - (datetime.now() - datetime.fromisoformat(arrival)).total_seconds()
            leaving = remaining <= 6
        except (ValueError, TypeError):
            pass
        meeting=mind.get('meeting')
        if meeting and not leaving:
            self.target=point(*meeting['target']);self.rest_until=now
            dx,dy=self.target[0]-a['x'],self.target[1]-a['y'];distance=math.hypot(dx,dy*2)
            step=min(1,pace*.72*dt/max(.001,distance))
            a['x']+=dx*step;a['y']+=dy*step
            moving=distance>.3
            a.update(state='walking' if moving else 'idle',activity='walking' if moving else 'idle',facing=dx>=0 if moving else meeting['facing'])
            return
        if now < self.reaction_until and not leaving:
            a.update(state='signature', activity='signature', facing=pos.x > a['x'])
            return
        if leaving:
            self.target = point(bounds[1], a['y'])
            self.rest_until = now
        if now < self.rest_until:
            a.update(state=mind.get('gesture', 'signature'), activity=mind.get('gesture', 'signature'))
            return
        dx, dy = self.target[0] - a['x'], self.target[1] - a['y']
        distance = math.hypot(dx, dy * 2)
        if distance < .3:
            if leaving:
                a.update(state='leaving', activity='leaving', facing=True)
                return
            self.rest_until = now + max(2.2, 7 - pace) * mind.get('rest', 1)
            self.target = roaming_target(self.rng, bounds, (a['x'], a['y']), (pos.x, pos.y), mind.get('social', p['social']))
            a.update(state='signature', activity='signature')
        else:
            speed = pace * (.9 if leaving else .72)
            step = min(1.0, speed * dt / distance)
            a['x'] += dx * step
            a['y'] += dy * step
            a.update(state='leaving' if leaving else 'walking', activity='leaving' if leaving else 'walking', facing=dx >= 0)

    def snapshot(self):
        return dict(self.actor) if self.actor else None


class StoryMotion:
    """Story participants have their own world positions, not a duck offset.

    Props stay where the encounter began; living actors explore between habits.
    Staging is transient and never advances story choices or awards rewards.
    """
    MOBILE = {'lost_duckling': 3.5, 'frog_choir': 2.4, 'migration': 4.8, 'night_lights': 2.5}

    def __init__(self):
        self.token = self.actor = self.target = None
        self.last = None
        self.rest_until = 0
        self.step = None
        self.rng = random.Random(0)

    def tick(self, game, now=None):
        now = time.monotonic() if now is None else now
        dt = min(.25, max(0, now - self.last)) if self.last is not None else 0
        self.last = now
        pond = getattr(game, 'living_pond', None)
        story = pond.state.get('story') if pond else None
        area = getattr(game.exploration, 'current_area', None)
        if not game.duck or not story or (area and area.name != 'Home Pond'):
            self.token = self.actor = self.target = None
            return
        if game._state != 'playing':
            self.rest_until += dt
            return
        r, pos = game.renderer, game.renderer.duck_pos
        cx, cy = getattr(r, '_camera_x', 0), getattr(r, '_camera_y', 0)
        w, h = getattr(r, '_viewport_width', 132), getattr(r, '_viewport_height', 42)
        bounds = (cx + 8, cx + max(16, w - 9), cy + 4, cy + max(8, h - 5))
        token = (id(game.duck), id(story), story['id'])
        if token != self.token:
            self.token = token
            self.rng.seed(str(pond.state['seed']) + ':' + story['id'])
            x, y = roaming_target(self.rng, bounds, (pos.x, pos.y), (pos.x, pos.y))
            self.actor = dict(id='story:' + story['id'], storyId=story['id'], x=x, y=y,
                              state='signature', activity='signature', facing=True)
            self.target = (x, y)
            self.rest_until = now + 2.5
            self.step = story['step']
        a = self.actor
        if self.step != story['step']:
            self.step = story['step']
            self.rest_until = now + 3
            a.update(state='quacking', activity='quacking', facing=pos.x > a['x'])
        speed = self.MOBILE.get(story['id'], 0)
        meeting=pond.minds.motion('story:pip').get('meeting') if story['id']=='lost_duckling' else None
        if meeting:
            self.target=tuple(meeting['target']);self.rest_until=now
            dx,dy=self.target[0]-a['x'],self.target[1]-a['y'];distance=math.hypot(dx,dy*2)
            step=min(1,speed*dt/max(.001,distance));a['x']+=dx*step;a['y']+=dy*step
            a.update(state='walking' if distance>.3 else 'idle',activity='walking' if distance>.3 else 'idle',facing=dx>=0 if distance>.3 else meeting['facing'])
            return
        if now < self.rest_until or not speed:
            return
        dx, dy = self.target[0] - a['x'], self.target[1] - a['y']
        distance = math.hypot(dx, dy * 2)
        if distance < .3:
            self.target = roaming_target(self.rng, bounds, (a['x'], a['y']), (pos.x, pos.y))
            self.rest_until = now + self.rng.uniform(2.2, 5.5)
            a.update(state='signature', activity='signature')
        else:
            step = min(1, speed * dt / distance)
            a['x'] += dx * step
            a['y'] += dy * step
            a.update(state='walking', activity='walking', facing=dx >= 0)

    def snapshot(self):
        return dict(self.actor) if self.actor else None
