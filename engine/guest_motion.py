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
        if now < self.reaction_until and not leaving:
            a.update(state='signature', activity='signature', facing=pos.x > a['x'])
            return
        if leaving:
            self.target = point(bounds[1], a['y'])
            self.rest_until = now
        if now < self.rest_until:
            a.update(state='signature', activity='signature', facing=pos.x > a['x'])
            return
        dx, dy = self.target[0] - a['x'], self.target[1] - a['y']
        distance = math.hypot(dx, dy * 2)
        if distance < .3:
            if leaving:
                a.update(state='leaving', activity='leaving', facing=True)
                return
            self.rest_until = now + max(2.2, 7 - p['pace'])
            radius = p['radius']
            if p['species'] == 'duckling' or self.rng.random() < p['social']:
                self.target = point(pos.x + self.rng.choice((-1, 1)) * self.rng.uniform(4, 9), pos.y + self.rng.uniform(-2, 1))
            else:
                self.target = point(pos.x + self.rng.uniform(-radius, radius), pos.y + self.rng.uniform(-5, 3))
            a.update(state='signature', activity='signature', facing=pos.x > a['x'])
        else:
            speed = p['pace'] * (.9 if leaving else .72)
            step = min(1.0, speed * dt / distance)
            a['x'] += dx * step
            a['y'] += dy * step
            a.update(state='leaving' if leaving else 'walking', activity='leaving' if leaving else 'walking', facing=dx >= 0)

    def snapshot(self):
        return dict(self.actor) if self.actor else None
