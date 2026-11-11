"""Persistent, deterministic pond simulation layered onto the original game.

The original registries remain authoritative for ownership, needs, inventory,
friendship, recipes and rewards. This module owns new physical/ecological state,
long-term intentions and bounded memories. Presentation snapshots never advance it.
"""
import copy
import hashlib
import math
import time
from datetime import datetime
from engine.item_profiles import ITEMS
from engine.pond_stories import STORIES
from engine.placements import outdoor_decorations, complete_structures,habitat_placements
from engine import shelters, nest_routines, playdates, water_routines, furniture_rests,botany,botanical_care
from world.guest_cast import guest_profile, guest_line

NEEDS = ('hunger', 'energy', 'fun', 'cleanliness', 'social')
SKILLS = ('gardening', 'stewardship', 'cooking', 'care', 'building', 'engineering',
          'music', 'discovery', 'style', 'agility', 'observation', 'organization', 'crafting')
PROJECTS = {
 'reed_beds': {'name': 'Living reed beds', 'description': 'Filter runoff, shelter frogs, and hold water through dry spells.', 'effect': 'water', 'stages': [('Survey the bank', {'reed': 2, 'pebble': 2}), ('Weave the root baskets', {'reed': 6, 'twig': 4}), ('Restore the shallows', {'pond_clay': 4, 'moss': 3})]},
 'orchard': {'name': 'Community orchard', 'description': 'A shady food grove with flowers for pollinators and fruit to forage.', 'effect': 'plants', 'stages': [('Mark a sunny plot', {'twig': 3, 'pebble': 2}), ('Prepare rich soil', {'leaf': 8, 'pond_clay': 3}), ('Plant the grove', {'seed': 5, 'acorn': 3})]},
 'observatory': {'name': 'Little sky observatory', 'description': 'Forecast five weather fronts and record two field notes per observation instead of one.', 'effect': 'knowledge', 'stages': [('Find the horizon', {'pebble': 4, 'twig': 3}), ('Build the platform', {'wooden_plank': 4, 'string': 3}), ('Fit the weather instruments', {'iron_ore': 3, 'crystal': 2})]},
 'clubhouse': {'name': 'Friends’ clubhouse', 'description': 'Shared time at home restores more social energy and builds warmer relationships.', 'effect': 'community', 'stages': [('Lay the gathering circle', {'rock': 5, 'twig': 4}), ('Raise the shelter', {'wooden_plank': 6, 'thatch': 3}), ('Make everyone welcome', {'fabric_scrap': 4, 'wildflower': 5})]},
 'workshop': {'name': 'Repair workshop', 'description': 'Repairs at home take 20% less time and restore 40 tool durability instead of 25, using the same materials.', 'effect': 'craft', 'stages': [('Sort the work area', {'pebble': 3, 'twig': 5}), ('Build a sturdy bench', {'wooden_plank': 5, 'iron_ore': 2}), ('Stock the tool wall', {'string': 4, 'smooth_stone': 3})]},
 'trail': {'name': 'Waterside nature trail', 'description': 'Safe wildlife corridors link the meadow, grove and pond.', 'effect': 'wildlife', 'stages': [('Map the old paths', {'twig': 4, 'leaf': 5}), ('Protect the nesting places', {'reed': 4, 'grass_blade': 8}), ('Build the footbridges', {'wooden_plank': 4, 'rope': 2})]},
}
PLANS = {
 'forage': ('Follow the bank for useful materials', 'eating', 'observation', 18),
 'observe': ('Sit quietly and watch the wildlife', 'idle', 'discovery', 24),
 'restore': ('Clear litter and restore the shallows', 'preening', 'stewardship', 22),
 'rest': ('Find a sheltered place and settle down', 'sleeping', 'care', 28),
 'garden': ('Inspect and water the garden', 'preening', 'gardening', 22),
 'practice': ('Practice a little pond-side performance', 'dancing', 'music', 20),
 'wander': ('Explore a different corner of the pond', 'walking', 'observation', 16),
}
OCCUPATIONS = {'adventurous': ('exploring', 'forest'), 'scholarly': ('reading', 'meadow'),
 'artistic': ('painting', 'pond'), 'playful': ('playing', 'meadow'),
 'mysterious': ('stargazing', 'forest'), 'generous': ('helping neighbors', 'pond'),
 'foodie': ('foraging', 'meadow'), 'athletic': ('training', 'pond')}
RESOURCE_POOLS = {'pond': ('reed', 'pond_clay', 'pebble', 'pond_weed', 'worm'),
 'forest': ('twig', 'bark', 'acorn', 'moss', 'mushroom'),
 'meadow': ('leaf', 'grass_blade', 'wildflower', 'seed', 'berry'),
 'beach': ('shell', 'driftwood', 'sand', 'seaweed', 'sea_glass'),
 'mountains': ('rock', 'smooth_stone', 'iron_ore', 'crystal', 'pebble'),
 'swamp': ('reed', 'pond_clay', 'moss', 'mushroom', 'worm'),
 'garden': ('leaf', 'grass_blade', 'wildflower', 'seed', 'berry'),
 'riverside': ('reed', 'smooth_stone', 'driftwood', 'pond_clay', 'worm'),
 'urban': ('string', 'fabric_scrap', 'pebble', 'twig', 'bread_crumb')}


def clamp(n, low=0., high=1.):
    return min(high, max(low, float(n)))


def stable(text):
    return int(hashlib.sha256(str(text).encode()).hexdigest()[:8], 16)


def fresh(seed=1):
    return {'version': 1, 'seed': seed, 'elapsed': 0., 'last_wall': time.time(),
            'objects': {}, 'friends': {}, 'journal': [], 'knowledge': {}, 'skills': {k: 0. for k in SKILLS},
            'preferences': {}, 'habits': {}, 'projects': {k: {'stage': 0, 'work': 0} for k in PROJECTS},
            'stocks': {}, 'plan': None, 'policy': 'balanced', 'next_decision': 20.,
            'cooldowns': {}, 'decision': [], 'weather': {}, 'promises': [], 'seen_events': [],
            'ecology': {'soil': .55, 'water': .66, 'clarity': .72, 'flowers': .45,
                        'insects': .48, 'fish': .52, 'birds': .45, 'litter': .12,
                        'wetness': .25, 'snow': 0., 'ice': 0., 'temperature': 17., 'wind': .2},
            'offline': '', 'sequence': 0, 'auto': True, 'stories': {}, 'story': None, 'next_story': 90.,
            'protection': 0., 'legacy': {}, 'biomes': {},
            'community': {'warmth': .2, 'gatherings': 0}, 'minds': {}, 'layout': {}}


class LivingPond:
    def __init__(self, data=None, seed=1):
        self.state = fresh(seed)
        if isinstance(data, dict):
            for key in self.state:
                if key in data and key not in ('version',):
                    if isinstance(self.state[key], dict) and isinstance(data[key], dict):
                        self.state[key].update(copy.deepcopy(data[key]))
                    elif isinstance(data[key], type(self.state[key])) or key == 'plan' or (key == 'story' and isinstance(data[key], dict)):
                        self.state[key] = copy.deepcopy(data[key])
        self.game = None
        self._last_tick = time.monotonic()
        self._sync_at = -1
        self._last_plan_visual = None
        self._last_weather = None
        self._cache = None
        self._cache_at = -1
        if self.state['plan']:
            self.state['plan']['paused'] = True
            # Physical visitor reservations belong to a live visit, not a save.
            self.state['plan'].pop('company',None)
            self.state['plan']['company_tried']=True
        self.state['journal'] = self.state['journal'][-120:]
        self.state['promises'] = self.state['promises'][-24:]
        from engine.mind_garden import MindGarden
        self.minds = MindGarden(self)

    @property
    def busy(self):
        return bool((self.state['plan'] and not self.state['plan'].get('paused')) or self.minds.encounter_for('cheese'))

    def attach(self, game, offline=True):
        self.game = game
        from engine.pond_layout import PondLayout,REVISION
        self.layout=PondLayout(game.habitat,lambda:[(p.item_id,*p.get_display_position()) for p in [*outdoor_decorations(game),*complete_structures(game)]])
        self._layout_obstacles=tuple(self.layout.obstacles())
        game.habitat.placement_policy=self.layout
        if self.state['layout'].get('revision')!=REVISION:
            report=self.layout.reconcile();self.state['layout']=report
            if report['moved'] or report['stored']:
                self.notice('Made room for the larger artwork: '+str(len(report['moved']))+' items moved, '+str(len(report['stored']))+' safely stored. Open Arrange to choose their places.')
        self.sync()
        self.minds.sync()
        if offline:
            elapsed = clamp(time.time() - self.state['last_wall'], 0, 48 * 3600)
            if elapsed >= 60:
                # Bounded environmental catch-up. No inventory/XP/needs rewards
                # while absent, and never replays a half-finished player action.
                steps=min(192,int(elapsed/60))
                step=elapsed/steps
                present_hour=self.hour
                for i in range(steps):
                    self.hour=(present_hour-(elapsed-step*(i+1))/3600)%24
                    self.advance(step, offline=True)
                self.hour=present_hour
                self.state['offline'] = f"While you were away for {int(elapsed/60)} minutes, the pond’s weather, soil and wildlife continued changing. Your unfinished activity is paused."
                self.remember('return', self.state['offline'], .65)
        self.state['last_wall'] = time.time()
        self._last_tick = time.monotonic()

    def sync(self):
        g = self.game
        if not g or not g.duck:
            return
        if getattr(self,'layout',None):
            obstacles=tuple(self.layout.obstacles())
            if obstacles!=self._layout_obstacles:
                self._layout_obstacles=obstacles
                report=self.layout.reconcile();self.state['layout'].update(report)
                changed=set(report['moved']+report['stored'])
                if self.state['plan'] and self.state['plan']['target'] in changed:
                    self.minds.cancel_encounter('cheese');self.cancel()
                if changed:self.notice('Made room for the new surroundings. Your belongings are kept in the habitat or safely stored; Arrange shows their places.')
        owned = set(g.habitat.owned_items) | set(g.inventory.items) | set(g.materials.get_all_materials())
        owned |= set(g.habitat.equipped_cosmetics.values())
        owned |= set(g.crafting.tools)
        owned |= {k for k,v in g.garden.harvest_inventory.items() if v>0} | {k for k,v in g.garden.seed_inventory.items() if v>0}
        owned |= set(g.outfits.owned_items) | set(g.seasonal_clothing.wardrobe.owned_items)
        owned |= {k for k,v in g.decorations.owned_decorations.items() if v>0}
        owned |= {d.decoration_id for room in g.decorations.rooms.values() for d in room.decorations}
        owned |= set(g.treasure.found_treasures) | set(g.fishing.fish_caught)
        owned |= {s.blueprint_id for s in g.building.structures if s.status.value == 'complete'}
        self.owned = owned
        self.placements = [*habitat_placements(g),*outdoor_decorations(g),*complete_structures(g)]
        self.placed = {i.item_id: i for i in self.placements}
        for key in owned:
            if key not in ITEMS:
                continue
            self.state['objects'].setdefault(key, {'condition': 1., 'wetness': 0., 'dirt': 0.,
                'bond': 0., 'uses': 0, 'last_use': -1000., 'growth': .35, 'active': False})
            if key in botany.ROOTED:botany.state(self.state['objects'][key])
        for friend in g.friends.friends.values():
            self.state['friends'].setdefault(friend.id, {'trust': .25, 'warmth': .3,
                'reliability': .5, 'energy': .8, 'social': .7, 'last_shared': -1000.,
                'memories': [], 'activity': 'resting', 'location': 'pond', 'want': 'company'})
        area = g.exploration.current_area
        next_biome = area.biome.value if area else 'pond'
        if getattr(self, 'biome', next_biome) != next_biome:
            self.state['biomes'][self.biome] = copy.deepcopy(self.state['ecology'])
            self.state['ecology'] = self.state['biomes'].get(next_biome, copy.deepcopy(fresh()['ecology']))
        self.biome = next_biome
        self.location = area.name if area else 'Home Pond'
        self.hour = g.day_night.get_current_hour() + g.day_night.get_current_minute() / 60
        self.season = g.atmosphere.current_season.value
        self.weather_type = g.atmosphere.current_weather.weather_type.value if g.atmosphere.current_weather else 'sunny'
        self.intensity = g.atmosphere.current_weather.intensity if g.atmosphere.current_weather else .4
        stocks = self.state['stocks']
        for biome, resources in RESOURCE_POOLS.items():
            for resource in resources:
                stocks.setdefault(biome + ':' + resource, 6.)

    def save(self):
        result = copy.deepcopy(self.state)
        result['last_wall'] = time.time()
        return result

    def remember(self, kind, text, salience=.5, subject=None):
        self.state['sequence'] += 1
        self.state['journal'].append({'id': self.state['sequence'], 'at': round(self.state['elapsed']),
            'kind': kind, 'text': text, 'salience': salience, 'subject': subject})
        self.state['journal'] = self.state['journal'][-120:]
        self._cache = None

    def gain(self, skill, amount=1):
        # Skill XP belongs to the expansion, not a second source of currency.
        self.state['skills'][skill] = min(10000, self.state['skills'].get(skill, 0) + amount)

    def completed(self, project):
        return self.state['projects'].get(project, {}).get('stage', 0) >= 3

    def change_need(self, need, amount):
        g = self.game
        if g and g.duck:
            g.duck_store.change_need(need, amount, 'living pond activity')
            g.duck_store.sync_to_duck(g.duck)

    def notice(self, text):
        if self.game:
            self.game.renderer.show_message(text, duration=6, category='duck')
        self._cache = None
        return text

    def tick(self):
        now = time.monotonic()
        dt = clamp(now - self._last_tick, 0, 10)
        self._last_tick = now
        if not self.game.duck or self.game._state != 'playing':
            return
        if self.state['elapsed'] >= self._sync_at:
            self.sync()
            self._sync_at = self.state['elapsed'] + 1
        self.advance(dt)

    def advance(self, dt, offline=False):
        if not math.isfinite(dt) or dt <= 0:
            return
        self.state['elapsed'] += dt
        self._environment(dt, offline)
        self._social(dt, offline)
        if offline:
            return
        self._activity(dt)
        self._observe_events()
        self._stories()
        self._legacy_links(dt)
        s = self.state
        if s['auto'] and s['elapsed'] >= s['next_decision'] and not s['plan'] and not self.busy:
            s['next_decision'] = s['elapsed'] + 35
            self.decide()

    def _weather_front(self, offline):
        s = self.state
        w = s['weather'].setdefault(getattr(self, 'biome', 'pond'), {})
        if not w:
            w.update(type=getattr(self, 'weather_type', 'sunny'), until=s['elapsed'] + 360,
                     forecast=[], front=0)
        horizon = 5 if self.completed('observatory') else 3
        if len(w['forecast']) < horizon:
            from world.atmosphere import WEATHER_DATA, BIOME_WEATHER_MODIFIERS
            season = getattr(self, 'season', 'spring')
            weighted = []
            for weather, data in WEATHER_DATA.items():
                weight = data.get(season + '_prob', 0) * BIOME_WEATHER_MODIFIERS.get(getattr(self, 'biome', 'pond'), {}).get(weather, 1)
                if weight > 0 and not data.get('special'):
                    # A front passes through clouds and rain before clearing;
                    # seasonal probabilities still govern which weather is legal.
                    related = any(x in weather.value and x in w['type'] for x in ('rain', 'snow', 'cloud', 'storm'))
                    weighted.extend([weather.value] * max(1, int(weight * (150 if related else 80))))
            for n in range(len(w['forecast']), horizon):
                seed = stable((s['seed'], w['front'] + n, getattr(self, 'biome', 'pond')))
                w['forecast'].append({'type': weighted[seed % len(weighted)] if weighted else 'sunny', 'duration': 300 + seed % 420, 'intensity': .35 + (seed % 60)/100})
        if s['elapsed'] >= w['until']:
            next_front = w['forecast'].pop(0)
            old = w['type']
            w.update(type=next_front['type'], until=s['elapsed'] + next_front['duration'],
                     intensity=next_front['intensity'], front=w['front'] + 1)
            if not offline:
                self.remember('weather', f"{old.replace('_', ' ').title()} gave way to {w['type'].replace('_', ' ')}.", .3)
        if self.game and not offline and self._last_weather != (getattr(self, 'biome', 'pond'), w['type'], w['front']):
            from world.atmosphere import Weather, WeatherType, WEATHER_DATA
            from core.event_bus import event_bus, WeatherChangedEvent
            previous = self.game.atmosphere.current_weather
            # Respect special original events until their weather expires.
            if previous and WEATHER_DATA.get(previous.weather_type, {}).get('special') and previous.is_active():
                return previous.weather_type.value, previous.intensity
            kind = WeatherType(w['type']); data = WEATHER_DATA[kind]
            self.game.atmosphere.current_weather = Weather(kind, w.get('intensity', getattr(self, 'intensity', .5)),
                max(.1, (w['until'] - s['elapsed'])/3600+.02), datetime.now().isoformat(),
                data.get('mood_modifier', 0), data.get('xp_multiplier', 1), data.get('message', ''))
            self._last_weather = (getattr(self, 'biome', 'pond'), w['type'], w['front'])
            if previous and previous.weather_type != kind:
                event_bus.emit(WeatherChangedEvent(source='living_pond', old_weather=str(previous.weather_type), new_weather=str(kind), intensity=w.get('intensity', .5)))
                self.game.atmosphere.weather_history = (self.game.atmosphere.weather_history + [kind.value])[-10:]
        return w['type'], w.get('intensity', getattr(self, 'intensity', .5))

    def _environment(self, dt, offline):
        weather, intensity = self._weather_front(offline)
        s = self.state; e = s['ecology']; minutes = dt / 60
        wet = any(k in weather for k in ('rain', 'storm', 'shower', 'drizzle', 'sleet'))
        snow = any(k in weather for k in ('snow', 'blizzard'))
        cold = snow or any(k in weather for k in ('frost', 'cold', 'freez', 'ice'))
        hot = any(k in weather for k in ('heat', 'scorch', 'muggy'))
        base = {'spring': 16, 'summer': 26, 'autumn': 12, 'fall': 12, 'winter': 2}.get(getattr(self, 'season', 'spring'), 16)
        target = base + math.sin((getattr(self, 'hour', 12)-8)*math.pi/12)*5 + (10 if hot else -12 if cold else -4 if wet else 0)
        e['temperature'] += (target - e['temperature']) * min(1, minutes*.2)
        wind = (.75 if any(k in weather for k in ('wind', 'storm', 'breez', 'blizzard')) else .12) * intensity
        e['wind'] += (wind-e['wind'])*min(1, minutes*.5)
        completed = {PROJECTS[k]['effect'] for k,v in s['projects'].items() if v['stage'] >= 3}
        e['wetness'] = clamp(e['wetness'] + minutes*(.055*intensity if wet else -.012*(1+max(0,e['temperature'])/30)))
        e['snow'] = clamp(e['snow'] + minutes*(.025*intensity if snow else -.002*max(0,e['temperature'])))
        e['ice'] = clamp(e['ice'] + minutes*(.009 if e['temperature'] < 0 else -.005))
        e['soil'] = clamp(e['soil'] + minutes*(e['wetness']*.008 - .003 + (.002 if 'plants' in completed else 0)))
        e['water'] = clamp(e['water'] + minutes*(.012*intensity if wet else -.0018) + (.0009*minutes if 'water' in completed else 0))
        e['clarity'] = clamp(e['clarity'] + minutes*(.0015 + (.003 if 'water' in completed else 0) - e['litter']*.006 - (.003 if wet else 0)))
        e['flowers'] = clamp(e['flowers'] + minutes*(e['soil']*.004 - .0015 - e['snow']*.002))
        e['insects'] = clamp(e['insects'] + minutes*(e['flowers']*.004 - .0016 - e['wind']*.001))
        e['fish'] = clamp(e['fish'] + minutes*(e['water']*e['clarity']*.004 - .0014))
        e['birds'] = clamp(e['birds'] + minutes*(e['insects']*.003 - .0014 + (.001 if 'wildlife' in completed else 0)))
        e['litter'] = clamp(e['litter'] + minutes*.00025)
        s['protection'] = clamp(s['protection']-minutes*.0008)
        for key, stock in s['stocks'].items():
            s['stocks'][key] = clamp(stock + minutes*(.03+e['soil']*.04), 0, 12)
        home_weather = self.game.atmosphere.get_biome_weather('pond') if self.game else None
        home_type = home_weather.weather_type.value if home_weather else weather
        home_wet = any(k in home_type for k in ('rain','storm','shower','drizzle','sleet'))
        home_intensity = home_weather.intensity if home_weather else intensity
        home_temperature=base+math.sin((getattr(self,'hour',12)-8)*math.pi/12)*5+(10 if any(w in home_type for w in ('heat','scorch','muggy')) else -12 if any(w in home_type for w in ('snow','blizzard','frost','cold','freez','ice')) else -4 if home_wet else 0)
        home_ecology=dict(e if getattr(self,'biome','pond')=='pond' else s['biomes'].get('pond',fresh()['ecology']))
        home_ecology['wind']=(.75 if any(w in home_type for w in ('wind','storm','breez','blizzard')) else .12)*home_intensity
        for key, obj in s['objects'].items():
            outdoors = key in getattr(self, 'placed', {})
            if not outdoors:
                obj['wetness'] = clamp(obj['wetness'] - minutes*.02)
                continue
            obj['wetness'] = clamp(obj['wetness'] + minutes*(.05*home_intensity if home_wet else -.025))
            obj['dirt'] = clamp(obj['dirt'] + minutes*(.001 + e['wind']*.002))
            obj['condition'] = clamp(obj['condition'] - minutes*(.0001+obj['wetness']*.0003*(1-s['protection']*.75)), .15, 1)
            botany.update(self,key,obj,minutes,home_wet,home_intensity,home_temperature,home_ecology)
        if self.game and not offline and home_wet:
            for plot in self.game.garden.plots.values():
                if plot.plant and not plot.plant.is_withered:
                    plot.plant.water_level = clamp(plot.plant.water_level + minutes*home_intensity*1.2, 0, 100)
        self.weather_type = weather

    def _social(self, dt, offline):
        s = self.state
        for key, friend in s['friends'].items():
            definition = self.game.friends.get_friend_by_id(key) if self.game else None
            personality = definition.personality.value if definition else 'playful'
            activity, biome = OCCUPATIONS[personality]
            hour = (getattr(self, 'hour', 12) + stable(key)%3 - 1) % 24
            asleep = hour < 6 or hour >= 22
            storm = any(k in getattr(self, 'weather_type', '') for k in ('storm', 'blizzard'))
            friend['activity'] = 'sleeping' if asleep else 'sheltering' if storm else activity
            friend['location'] = 'nest' if asleep or storm else biome
            friend['energy'] = clamp(friend['energy'] + dt/3600*(.25 if asleep else -.05))
            # A welcoming home makes time apart less lonely. This persistent
            # benefit also gives kindness toward passing strangers a real effect.
            friend['social'] = clamp(friend['social'] - dt/3600*(.04-.02*s['community']['warmth']))
            friend['want'] = 'rest' if friend['energy'] < .3 else 'company' if friend['social'] < .55 else activity
        for promise in s['promises']:
            if promise['status'] == 'promised' and s['elapsed'] > promise['deadline']:
                promise['status'] = 'missed'
                friend = s['friends'].get(promise['friend'])
                if friend: friend['reliability'] = clamp(friend['reliability']-.06)
                if not offline:self.minds.promise(promise['friend'], False)
                self.remember('promise', f"The promised {promise['activity']} had to be postponed. You can make it up to your friend.", .8)

    def available(self):
        g = self.game
        return bool(g and g.duck and g.duck.growth_stage != 'egg' and g._state == 'playing'
            and not g._active_minigame and not g._duck_traveling and not g._duck_exploring
            and not g._duck_building and not g._dream_active and not g._cheese_away
            and not g.renderer._show_talk and not g.interaction_controller.is_interacting())

    def start(self, kind, target='', automatic=False):
        s = self.state
        if self.minds.encounter_for('cheese'):
            if automatic:return False, 'Cheese is spending time with a friend.'
        if kind == 'item' and target in shelters.HOMES:
            kind = 'rest'
        if s['plan'] or not self.available():
            return False, 'Cheese is busy. Finish or cancel the current activity first.'
        if self.game.duck.needs.energy < 15 and kind not in ('rest', 'item'):
            return False, 'Cheese needs rest before taking that on.'
        duration = PLANS.get(kind, ('', '', '', 20))[3]
        label = PLANS.get(kind, (kind.replace('_',' ').title(),))[0]
        residence = None
        seating = None
        if kind == 'rest':
            self.sync()
            places = shelters.candidates(self, target)
            if target and not places:
                return False, 'That resting place is not reachable, suitable for Cheese, or sheltered from this weather.'
            if places:
                residence = places[0]
                target = residence['id']
                label = ('Wait out the weather in ' if shelters.adverse(self.weather_type) else 'Settle into ') + ITEMS[target]['name']
            else:
                label = 'Take a quiet rest nearby'
        if kind == 'item':
            self.sync()
            if target not in getattr(self, 'owned', set()) or target not in ITEMS:
                return False, 'That item is not in your belongings.'
            if target in self.placed and self.location != 'Home Pond':
                return False, 'That item is back at Home Pond.'
            profile = ITEMS[target]
            if target in furniture_rests.SEATS:
                choices=furniture_rests.candidates(self,target)
                if not choices:
                    return False, 'Place that seat in a reachable spot with a free place, and wait for dry weather.'
                seating=choices[0]
            if profile['family'] in ('slide','swing','trampoline','seesaw','sandbox','horse') and target not in self.placed:
                return False, 'Place '+profile['name']+' in the habitat before Cheese uses it.'
            if target in water_routines.WATER:
                if target not in self.placed:
                    return False, 'Place '+profile['name']+' in the habitat before Cheese uses it.'
                if not water_routines.choose(self,target):
                    return False, 'Cheese would rather leave the water alone in this weather.'
            if profile['kind'] in ('food','wearable'):
                return False, 'Use the original inventory or wardrobe to eat or equip this item.'
            duration, label = profile['duration'], profile['verb']+' '+profile['name']
            if target in botany.ROOTED:
                if target not in self.placed or self.location!='Home Pond':
                    return False,'Place '+profile['name']+' at Home Pond before tending it.'
                if any(w in self.weather_type for w in ('storm','blizzard')):
                    return False,'Let the storm pass before tending the plants.'
                if any(r['id']==target and r['slot']==0 and r['destination']==shelters.position(self.placed[target]) for r in self.minds.gardening.values()):
                    return False,'A visitor is tending that spot. Let them finish their care first.'
                mode=botany.care_mode(self,target)
                label={'water':'Water the roots of ','brush':'Brush debris from ','inspect':'Inspect '}[mode]+profile['name']
            if profile['family'] in ('slide','swing','trampoline','seesaw','horse'):
                label = ('Explore ' if self.game.duck.growth_stage in ('hatchling','duckling') else 'Ride ') + profile['name']
            if s['elapsed'] - s['objects'][target]['last_use'] < 60:
                return False, 'Give that a moment. Cheese would enjoy some variety.'
        elif kind in ('clean_item', 'repair_item'):
            if target not in getattr(self,'owned',set()) or target not in ITEMS:
                return False, 'You do not own that item.'
            if target in self.placed and self.location != 'Home Pond':
                return False, 'That item is back at Home Pond.'
            obj = s['objects'][target]
            if kind == 'repair_item' and obj['condition'] >= .95:
                return False, 'It is already in excellent condition.'
            if kind == 'clean_item' and obj['dirt'] < .05:
                return False, 'It is already clean.'
            if kind == 'repair_item' and not self.game.materials.has_materials({'twig':1}):
                return False, 'A repair needs one twig for a small brace.'
            label = ('Carefully repair ' if kind=='repair_item' else 'Brush and polish ')+ITEMS[target]['name']
        elif kind == 'project':
            project = PROJECTS.get(target); state = s['projects'].get(target)
            if not project or not state or state['stage'] >= 3:
                return False, 'That project is complete or unavailable.'
            if self.location != 'Home Pond': return False, 'Community projects are at Home Pond.'
            stage, cost = project['stages'][state['stage']]
            if not self.game.materials.has_materials(cost):
                return False, 'Gather the listed materials before starting this stage.'
            label, duration = stage, 40 + state['stage']*15
        elif kind == 'share':
            friend = self.game.friends.get_friend_by_id(target)
            if not friend or not self.game.friends.current_visit or self.game.friends.current_visit.friend_id != target:
                return False, 'Invite this friend to visit before sharing an activity.'
            if s['elapsed']-s['friends'][target]['last_shared'] < 90:
                return False, 'Let the last shared moment settle before starting another.'
            label = 'Share '+friend.favorite_activity+' with '+friend.name
            duration = 24
        elif kind not in PLANS:
            return False, 'Unknown activity.'
        if s['elapsed'] < s['cooldowns'].get(kind+':'+target, -1):
            return False, 'Cheese needs a little variety before doing that again.'
        skill = ITEMS.get(target, {}).get('skill', PLANS.get(kind, ('','','care'))[2])
        duration *= max(.75, 1-math.sqrt(s['skills'].get(skill,0)/12)*.015)
        if kind == 'repair_item' and self.location == 'Home Pond' and self.completed('workshop'):
            duration *= .8
        self.minds.cancel_encounter('cheese')
        s['plan'] = {'kind': kind, 'target': target, 'label': label, 'elapsed': 0., 'duration': duration,
                     'phase': 'approach', 'automatic': automatic, 'paused': False, 'location': self.location,
                     'learning_before': self.minds.before(kind)}
        if kind=='item' and target in botany.ROOTED:s['plan']['plant_care']=botany.care_mode(self,target)
        if residence:
            s['plan']['residence'] = residence
        if seating:
            s['plan']['seating'] = seating
        self.game.behavior_ai.cancel_pending_movement()
        self.game.behavior_ai.clear_action()
        pos = self.game.renderer.duck_pos
        if residence:
            pos.move_to(*residence['destination'])
        elif seating:
            pos.move_to(*seating['destination'])
        elif target in self.placed:
            x,y = self.placed[target].get_display_position()
            pos.move_to(round(x*132/20), round(y*42/12))
        elif kind in ('forage','observe','restore','garden','wander'):
            seed = stable((s['elapsed'], kind))
            pos.move_to(12+seed%100, 18+(seed//100)%18)
        if pos._is_directed_movement:
            s['plan']['destination']=[pos.target_x,pos.target_y]
            s['plan']['approach_time']=0.
        self._last_plan_visual = None
        return True, label+'.'

    def cancel(self):
        if self.minds.encounter_for('cheese'):
            self.minds.cancel_encounter('cheese')
            self.state['next_decision']=self.state['elapsed']+30
            return 'Cheese and his friend finish up and go their separate ways.'
        if self.state['plan']:
            target=self.state['plan']['target']
            if target in self.state['objects']:self.state['objects'][target]['active']=False
            plan = self.state['plan']; self.state['plan'] = None
            self.state['next_decision'] = self.state['elapsed']+45
            if self.game: self.game.renderer.duck_pos.cancel_movement()
            self._cache=None
            self.remember('choice', f"Set aside: {plan['label']}. No completion reward or materials were taken.", .2)
            return 'Activity set aside.'
        return 'Cheese is free to choose what comes next.'

    def _activity(self, dt):
        s = self.state; plan = s['plan']; g = self.game
        if not plan or plan.get('paused') or not g:
            return
        if self.location != plan['location'] or not self.available():
            # Dialogues, minigames, sleep and journeys take priority over plans.
            plan['paused'] = True
            return
        if g.duck.current_action in ('feed','play','clean','pet','sleep'):
            return
        residence = plan.get('residence')
        if plan.get('care_routine') and plan['care_routine'].get('id') not in botanical_care.ROUTINES:
            self.cancel();return
        if plan.get('plant_care') and (not plan.get('destination') or not shelters.still_placed(self,{'id':plan['target'],'destination':plan['destination']}) or any(w in self.weather_type for w in ('storm','blizzard'))):
            self.cancel();return
        if plan.get('seating') and not furniture_rests.valid(self,plan['seating']):
            self.cancel()
            return
        if plan['kind']=='item' and plan['target'] in water_routines.WATER and not shelters.still_placed(self,{'id':plan['target'],'destination':plan['destination']}):
            self.cancel()
            return
        if residence and not shelters.still_placed(self, residence):
            self.cancel()
            self.notice('That resting place has moved. Cheese steps back out to find somewhere else.')
            return
        destination=plan.get('destination')
        if destination and plan['phase']=='approach':
            pos=g.renderer.duck_pos
            distance=abs(pos.x-destination[0])+abs(pos.y-destination[1])
            if distance>3:
                plan['approach_time']=plan.get('approach_time',0)+dt
                if plan['approach_time']>90:
                    self.cancel();self.notice('Cheese could not reach that spot. Try again after the path is clear.')
                return
            if not plan.get('arrived'):
                plan['arrived']=True
                pos.cancel_movement()
                pos.set_state_by_name('thinking',max(3,plan['duration']*.3))
        # A roof is an actual place to wait, not a looping reward animation.
        # Preserve the ordinary completion once; interrupting never grants it.
        routine_holding = nest_routines.advance(self, plan, dt)
        company_holding = playdates.advance(self, plan, dt)
        water_holding = water_routines.advance(self, plan, dt)
        seat_holding = furniture_rests.advance(self,plan,dt)
        care_holding = botanical_care.advance(self,plan,dt)
        if plan.get('company', {}).get('phase') == 'cancelled' or plan.get('water_routine',{}).get('interrupted') or plan.get('seat_routine',{}).get('interrupted') or plan.get('care_routine',{}).get('interrupted'):
            # An interrupted shared activity must not fall through to the normal
            # item completion either. Release both residents and leave use counts
            # and needs unchanged, even if the toy remains owned but is put away.
            self.cancel()
            return
        weather_holding = bool(residence and residence['roof'] and shelters.adverse(self.weather_type)
                       and plan['phase'] == 'act' and g.duck.needs.hunger > 15)
        holding = weather_holding or routine_holding or company_holding or water_holding or seat_holding or care_holding
        if company_holding or water_holding or seat_holding or care_holding:
            g.renderer.duck_pos.cancel_movement()
            g.renderer.duck_pos.set_state_by_name('thinking',0)
        elif plan.get('company',{}).get('done') or plan.get('water_routine',{}).get('done') or plan.get('seat_routine',{}).get('done') or plan.get('care_routine',{}).get('done'):
            plan['elapsed']=max(plan['elapsed'],plan['duration']*.9)
        if residence:
            residence['holding'] = weather_holding
            if weather_holding:
                residence['waited'] = residence.get('waited', 0.) + dt
                previous = residence.get('restored', 0.)
                restored = min(10., previous + dt * .035)
                self.change_need('energy', restored-previous)
                residence['restored'] = restored
        plan['elapsed'] = min(plan['elapsed']+dt, plan['duration']*.7) if holding else plan['elapsed']+dt
        ratio = plan['elapsed']/plan['duration']
        phase = 'approach' if ratio < .15 else 'prepare' if ratio < .28 else 'act' if ratio < .9 else 'settle'
        plan['phase'] = phase
        target = plan['target']; profile = ITEMS.get(target, {})
        state = {'comfort':'sleeping','water':'swimming','music':'dancing','toy':'hopping',
                 'food':'eating','plant':'preening','machine':'preening'}.get(profile.get('kind'),'preening') if plan['kind']=='item' else PLANS.get(plan['kind'], ('','preening'))[1]
        if phase in ('act','settle'):
            if phase != self._last_plan_visual:
                g.renderer.duck_pos.cancel_movement()
                g.renderer.duck_pos.set_state_by_name(state, duration=0 if residence or company_holding or water_holding or seat_holding or care_holding else max(1, plan['duration']-plan['elapsed']))
                self._last_plan_visual = phase
        if target in s['objects']:
            s['objects'][target]['active'] = phase == 'act'
        if residence:
            residence['inside'] = phase == 'act'
            if phase == 'act' and not residence.get('routine'):
                nest_routines.advance(self, plan, 0.)
        if ratio >= 1:
            s['plan'] = None  # Consume once before invoking callbacks.
            if residence or plan.get('company') or plan.get('water_routine') or plan.get('seating') or plan.get('care_routine'):
                g.renderer.duck_pos.cancel_movement()
                g.renderer.duck_pos.set_state_by_name('idle',0)
            if target in s['objects']: s['objects'][target]['active'] = False
            self._complete(plan)
            s['cooldowns'][plan['kind']+':'+target] = s['elapsed']+45
            s['next_decision'] = s['elapsed']+35
            self._cache = None

    def _complete(self, plan):
        s = self.state; kind = plan['kind']; target = plan['target']; g = self.game
        message = ''
        skill = PLANS.get(kind, ('','','care'))[2]
        if kind in ('item','clean_item','repair_item'):
            if target not in self.owned: return
            obj = s['objects'][target]; profile = ITEMS[target]; skill = profile['skill']
            water_mode=water_routines.complete(self,plan)
            furniture_rests.complete(self,plan)
            botanical_care.complete(self,plan)
            if water_mode=='edge':skill='observation'
            if kind == 'clean_item': obj['dirt'] = 0; message = 'Every seam and corner looks cared for.'
            elif kind == 'repair_item':
                if not g.materials.has_materials({'twig':1}):
                    self.notice('A twig is needed for the repair brace. Nothing was consumed.');return
                g.materials.remove_material('twig',1)
                repair = .4 if self.location == 'Home Pond' and self.completed('workshop') else .25
                obj['condition'] = clamp(obj['condition']+repair)
                if target in g.crafting.tools:
                    tool=g.crafting.tools[target];tool.durability=min(tool.max_durability,tool.durability+round(repair*100))
                message = 'A careful repair gave it more life.'
            else:
                obj['uses'] += 1; obj['last_use'] = s['elapsed']
                obj['condition'] = clamp(obj['condition']-.006, .15, 1)
                obj['bond'] = clamp(obj['bond']+.025)
                if not water_mode:self.change_need(profile['need'], 2+obj['condition']*2)
                botany.complete(self,plan)
                if profile['kind']=='water' and not water_mode: obj['wetness']=1
                message = profile['name']+(' is becoming an old favorite.' if obj['uses']>=5 else ' has a little more history now.')
                s['preferences'][target] = clamp(s['preferences'].get(target,.5)+.025)
        elif kind == 'forage':
            pool = RESOURCE_POOLS.get(self.biome, RESOURCE_POOLS['pond'])
            eligible = [r for r in pool if s['stocks'][self.biome+':'+r] >= 1] if self.biome in RESOURCE_POOLS else []
            if eligible:
                resource = eligible[stable((s['sequence'],s['seed']))%len(eligible)]
                amount, _ = g.materials.add_material(resource, 1)
                s['stocks'][self.biome+':'+resource] -= amount
                message = f"Found {amount} {resource.replace('_',' ')}. This patch needs time to replenish." if amount else 'Your material pouch is full. The find was left undisturbed.'
            else: message = 'This patch has been picked over. Let it recover or explore another biome.'
            self.change_need('energy', -1)
            if eligible and amount:g._process_quest_updates('collect',resource,amount)
        elif kind == 'restore':
            e=s['ecology']; removed=min(.05,e['litter']);e['litter']-=removed;e['clarity']=clamp(e['clarity']+removed*.4)
            self.change_need('energy',-1);message='The shallows are cleaner; clear water helps fish and insects return.'
        elif kind == 'rest':
            self.change_need('energy', 5)
            if plan.get('residence'):
                name = ITEMS[target]['name']
                message = ('The weather eased. Cheese peeks out of ' + name + '.'
                           if plan['residence'].get('waited') and not shelters.adverse(self.weather_type)
                           else 'A quiet rest in ' + name + ' helped Cheese recharge.')
                obj = s['objects'].get(target)
                if obj:
                    obj['uses'] += 1; obj['last_use'] = s['elapsed']
                    obj['bond'] = clamp(obj['bond']+.02)
                performed = plan['residence'].get('performed', [])
                last_routine = nest_routines.ROUTINES.get(performed[-1]) if performed else None
                if last_routine:
                    message += ' A small moment here: '+last_routine['label'].lower()+'.'
            else:
                message='A quiet rest helped Cheese recharge.'
        elif kind == 'garden':
            count=0
            for plot in g.garden.plots.values():
                if plot.plant and plot.needs_water:
                    g._garden_water(plot.plot_id);count+=1
            message=f'Tended {count} thirsty garden plots.' if count else 'Checked the soil and leaves. Nothing needs watering yet.'
        elif kind == 'observe':
            e=s['ecology']; species='frog' if e['water']>.6 and e['insects']>.35 else 'butterfly' if e['flowers']>.5 else 'robin'
            s['knowledge'][species]=s['knowledge'].get(species,0)+(2 if self.completed('observatory') else 1)
            message=f"Recorded {species} behavior. {'Rich shallows support a food web.' if species=='frog' else 'Quiet observation reveals more than chasing.'}"
        elif kind == 'practice':
            self.change_need('fun',3);message='The rhythm is getting steadier. Practice becomes part of who Cheese is.'
        elif kind == 'wander':
            self.change_need('fun',1);message='Found a new angle on a familiar place.'
        elif kind == 'share':
            friend=g.friends.get_friend_by_id(target)
            if not friend or not g.friends.current_visit or g.friends.current_visit.friend_id!=target:return
            ok,message,_=g.friends.interact_with_visitor(friend.favorite_activity)
            if not ok:return
            sheltered = self.location == 'Home Pond' and self.completed('clubhouse')
            record=s['friends'][target];record['trust']=clamp(record['trust']+.04);record['warmth']=clamp(record['warmth']+(.1 if sheltered else .06));record['social']=clamp(record['social']+(.3 if sheltered else .2));record['last_shared']=s['elapsed']
            record['memories']=(record['memories']+[{'activity':friend.favorite_activity,'weather':self.weather_type,'at':s['elapsed']}])[-12:]
            s['community']['warmth']=clamp(s['community']['warmth']+.01)
            s['community']['gatherings']+=1
            self.change_need('social',(8 if sheltered else 5)+2*s['community']['warmth'])
            for promise in s['promises']:
                if promise['friend']==target and promise['status']=='promised':
                    promise['status']='kept';record['reliability']=clamp(record['reliability']+.1)
                    self.minds.promise(target, True)
            skill='care'
        elif kind == 'project':
            project=PROJECTS[target];state=s['projects'][target]
            if state['stage']>=3:return
            stage,cost=project['stages'][state['stage']]
            if not g.materials.has_materials(cost):
                self.notice('The materials changed while Cheese worked. Gather what is missing and try again.');return
            for material,amount in cost.items():g.materials.remove_material(material,amount)
            state['stage']+=1;state['work']+=1
            message=project['name']+(': complete. '+project['description'] if state['stage']==3 else f': stage {state["stage"]} of 3 complete.')
            skill='building'
        if kind in ('rest','practice','wander','garden','forage','share'):
            action={'rest':'nap','practice':'play','wander':'explore','garden':'clean','forage':'explore','share':'pet'}[kind]
            g.duck.desires.on_action_performed(action,self.location)
        learning_kind='garden' if plan.get('care_routine',{}).get('done') else kind
        self.minds.completed(learning_kind, plan['label']+'. '+message, plan.get('learning_before'), target if kind=='share' else '')
        self.gain(skill,2 if plan['automatic'] else 4)
        hour=str(int(self.hour));s['habits'][kind+':'+hour]=min(30,s['habits'].get(kind+':'+hour,0)+1)
        self.remember('shared' if kind=='share' else 'project' if kind=='project' else 'activity', plan['label']+'. '+message,.8 if kind in ('share','project') else .4,target)
        g.duck.memory.add_interaction('living_'+kind, message, emotional_value=5)
        if not plan['automatic'] or kind in ('share','project'): self.notice(message)

    def decide(self):
        if not self.available() or not self.game:
            return
        g=self.game;s=self.state;n=g.duck.needs;e=s['ecology']
        # Utility combines urgency, environmental affordances, habit and novelty.
        choices=[('rest','',(100-n.energy)*1.5,'energy is low'),
                 ('restore','',e['litter']*90,'the shallows need care'),
                 ('observe','',18+e['birds']*12,'wildlife is active'),
                 ('forage','',20,'a new patch may hold useful materials'),
                 ('practice','',(100-n.fun)*.55,'a little music would lift the mood'),
                 ('wander','',16,'a change of scenery sounds good')]
        if shelters.adverse(self.weather_type):
            places = shelters.candidates(self)
            if places:
                choices.append(('rest', places[0]['id'], 180, 'a reachable roof will keep Cheese dry'))
        if any(p.needs_water for p in g.garden.plots.values()):choices.append(('garden','',45,'the garden is thirsty'))
        if g.friends.current_visit:
            key=g.friends.current_visit.friend_id;record=s['friends'].get(key,{})
            if s['elapsed']-record.get('last_shared',0)>120:choices.append(('share',key,(100-n.social)*.7+25,'a friend is here to spend time together'))
        if self.location=='Home Pond':
            for key in self.placed:
                profile=ITEMS.get(key);obj=s['objects'].get(key)
                if not profile or not obj or profile['kind'] in ('food','wearable'):continue
                water_score=water_routines.choose(self,key) if key in water_routines.WATER else None
                if key in water_routines.WATER and not water_score:continue
                if s['elapsed']-obj['last_use']<120:continue
                mode=water_routines.ROUTINES[water_score]['mode'] if water_score else None
                need='fun' if mode=='edge' else 'energy' if mode in ('sip','soak') else profile['need']
                score=(100-getattr(n,need))*.6+(1-obj['bond'])*10+s['preferences'].get(key,.5)*8
                choices.append(('item',key,score,'a useful possession can meet a need'))
        ranked=[]
        for kind,target,score,reason in choices:
            if s['elapsed'] < s['cooldowns'].get(kind+':'+target,0):continue
            habit=s['habits'].get(kind+':'+str(int(self.hour)),0)*.2
            bias=12 if (s['policy']=='curious' and kind in ('observe','wander','forage')) or (s['policy']=='social' and kind in ('share','practice')) or (s['policy']=='homebody' and kind in ('rest','garden','item','restore')) else 0
            learned=self.minds.model.value('cheese',kind,self.minds.context())*24
            score+=habit+bias+learned+(stable((int(s['elapsed']/30),kind,target))%7)
            if learned>5:reason+='; past experiences make this appealing'
            if any(k in self.weather_type for k in ('storm','blizzard')) and kind=='rest':score+=35;reason='the weather calls for shelter'
            ranked.append({'kind':kind,'target':target,'score':round(score,1),'reason':reason})
        s['decision']=sorted(ranked,key=lambda c:c['score'],reverse=True)[:5]
        for choice in s['decision']:
            ok,_=self.start(choice['kind'],choice['target'],automatic=True)
            if ok:break

    def _observe_events(self):
        for event in getattr(self.game,'_event_animators',[]):
            key=event.event_id
            if key not in self.state['seen_events']:
                self.state['seen_events']=(self.state['seen_events']+[key])[-800:]
                self.remember('encounter','Noticed '+key.replace('_',' ')+'.',.6,key)
                self.gain('discovery',1)

    def command(self, command):
        action=command.get('action');target=command.get('target','')
        if not isinstance(target,str) or len(target)>128:return
        self.sync();s=self.state
        if action in ('layout_place','layout_auto','layout_store'):
            if self.location!='Home Pond':ok,message=False,'Arrange the habitat when Cheese is back at Home Pond.'
            elif target not in self.game.habitat.owned_items:ok,message=False,'That item is not owned.'
            elif action=='layout_place':
                ok,message=self.layout.put(target,command.get('x'),command.get('y'))
            elif action=='layout_auto':
                ok=self.layout.auto_place(target);message='Found a place for it.' if ok else 'There is no clear space for the whole object. Your belongings have not been moved.'
            else:
                ok=self.game.habitat.store_item(target);message='Put away safely.' if ok else 'Use the wardrobe for that item.'
            if ok:
                if s['plan'] and s['plan']['target']==target:
                    self.minds.cancel_encounter('cheese')
                    self.cancel()
                self.sync()
            self.state['layout']['reply']={'target':target,'ok':bool(ok),'message':message,
                'sequence':self.state['layout'].get('reply',{}).get('sequence',0)+1}
            self._cache=None
            return self.notice(message)
        if action in ('mind_chat','mind_encourage','mind_redirect'):
            return self.minds.command(command)
        if action in ('guest_chat', 'guest_hobby', 'guest_company'):
            visit = self.game.atmosphere.current_visitor
            if not visit or visit[0].id != target:
                return self.notice('That guest has already headed home. Catch them next time.')
            now = time.monotonic()
            if now - getattr(self, '_guest_chat_at', -100) < 8:
                return self.notice('Give your guest a moment to finish their thought.')
            profile = guest_profile(target)
            if not profile:
                return
            self._guest_chat_at = now
            # A social chat cannot repeatedly roll gifts or duplicate inventory.
            result = self.game.atmosphere.interact_with_visitor(allow_gift=False)
            message = result[0]
            if action == 'guest_hobby':
                message = profile['name'] + ': ' + guest_line(target, 'story', self.game.duck.name)
            elif action == 'guest_company':
                friendship = self.game.atmosphere.get_visitor_friendship(target)
                close = friendship and friendship.level.value in ('friend', 'good_friend', 'best_friend')
                message = profile['name'] + ': ' + guest_line(target, 'personal' if close else 'activity', self.game.duck.name)
            self._guest_note = {'id':target, 'text':message}
            self.change_need('social', 2)
            self.remember('friend', message, .65, target)
            return self.notice(message)
        if action=='story_choice':return self.choose_story(target)
        if action=='garden_water' and target.isdigit():
            plot=self.game.garden.plots.get(int(target))
            if not plot or not plot.needs_water:return self.notice('That plot does not need water yet.')
            self.game._garden_water(int(target));self._cache=None;return
        if action=='garden_harvest' and target.isdigit():
            self.game._garden_harvest(int(target));self._cache=None;return
        if action=='garden_plant' and ':' in target:
            plot,seed=target.split(':',1)
            if plot.isdigit():
                ok,msg=self.game.garden.plant_seed(int(plot),seed)
                if ok:
                    self.game._process_quest_updates('garden','plant',1)
                    self.game.challenges.update_progress('activity_variety',1)
                self._cache=None;return self.notice(msg)
        if action=='cancel':return self.notice(self.cancel())
        if action=='resume':
            if s['plan'] and self.available() and s['plan']['location']==self.location:
                s['plan']['paused']=False;self._last_plan_visual=None
                if s['plan'].get('residence'):
                    # An interrupted resident may now be elsewhere. Keep the
                    # unfinished score, but walk back and enter again first.
                    s['plan']['phase']='approach';s['plan']['elapsed']=0.
                    s['plan']['residence']['inside']=False
                if s['plan'].get('destination') and s['plan']['phase']=='approach':
                    self.game.renderer.duck_pos.move_to(*s['plan']['destination']);s['plan']['approach_time']=0;s['plan']['arrived']=False
                return self.notice('Picking up where we left off.')
            return self.notice('Return to the activity’s location and finish any other interaction first.')
        if action=='policy' and target in ('balanced','curious','social','homebody'):
            s['policy']=target;return self.notice('Cheese will lean toward '+target+' choices, while still taking care of urgent needs.')
        if action=='autonomy':s['auto']=not s['auto'];return self.notice('Extended routines '+('enabled.' if s['auto'] else 'paused.'))
        if action=='invite':
            friend=self.game.friends.get_friend_by_id(target)
            if not friend:return self.notice('That friend has not been met yet.')
            record=s['friends'][target]
            if record['activity'] in ('sleeping','sheltering'):return self.notice(friend.name+' is '+record['activity']+'. Try again when they are free.')
            ok,msg,_=self.game.friends.start_visit(target)
            return self.notice(msg)
        if action=='promise':
            friend=self.game.friends.get_friend_by_id(target)
            if not friend:return
            if any(p['friend']==target and p['status']=='promised' for p in s['promises']):return self.notice('You already have plans together.')
            s['promises'].append({'friend':target,'name':friend.name,'activity':friend.favorite_activity,'deadline':s['elapsed']+1800,'status':'promised'})
            s['promises']=s['promises'][-24:]
            return self.notice('Promised '+friend.favorite_activity+' with '+friend.name+' within the next 30 minutes. Invite them and share time to keep it.')
        if action in tuple(PLANS)+('item','clean_item','repair_item','project','share'):
            ok,msg=self.start(action,target)
            return self.notice(msg)

    def _stories(self):
        s=self.state
        if s['story'] or s['elapsed']<s['next_story'] or not self.available():return
        e=s['ecology'];g=self.game
        gates={'first':True,'water':e['water']>.45 and e['clarity']>.5,
               'storm':any(k in self.weather_type for k in ('storm','rain','wind')),
               'craft':bool(g.crafting.crafted_count) or s['skills']['crafting']>=8,
               'birds':e['birds']>.45,'night':self.hour>=19 or self.hour<5,
               'friends':bool(g.friends.current_visit),'knowledge':sum(s['knowledge'].values())>=3}
        choices=[key for key,story in STORIES.items() if key not in s['stories'] and gates[story['gate']]]
        if choices:
            key=choices[0];s['story']={'id':key,'step':0,'choices':[]}
            self.remember('story',STORIES[key]['title']+' began by the pond.',.8,key)
            self.notice(STORIES[key]['title']+' — open the Pond journal to take part.')
        s['next_story']=s['elapsed']+180

    def story_snapshot(self):
        active=self.state['story']
        if not active:return None
        definition=STORIES[active['id']];scene=definition['scenes'][active['step']]
        choices=[]
        for c in scene['choices']:
            cost=c.get('cost',{})
            choices.append({**c,'available':bool(self.game and self.game.materials.has_materials(cost))})
        return {'id':active['id'],'step':active['step'],'total':len(definition['scenes']),
                'title':definition['title'],'asset':definition['asset'],'text':scene['text'],'choices':choices}

    def choose_story(self, target):
        # The scene number is part of the command, making double-clicks and stale
        # views harmless even if two stages happen to use the same choice id.
        if not self.available():return self.notice('Finish the current conversation, journey or game first.')
        parts=target.split(':');active=self.state['story']
        if len(parts)!=3 or not active or parts[0]!=active['id'] or parts[1]!=str(active['step']):return
        scene=STORIES[active['id']]['scenes'][active['step']]
        choice=next((c for c in scene['choices'] if c['id']==parts[2]),None)
        if not choice:return
        cost=choice.get('cost',{});g=self.game;s=self.state
        if not g.materials.has_materials(cost):return self.notice('The listed materials are missing. Choose another approach or gather them first.')
        for key,amount in cost.items():g.materials.remove_material(key,amount)
        for key,amount in choice.get('effect',{}).items():
            if key in s['ecology']:s['ecology'][key]=clamp(s['ecology'][key]+amount)
            elif key in NEEDS:self.change_need(key,amount)
            elif key in SKILLS:self.gain(key,amount)
            elif key=='knowledge':s['knowledge'][STORIES[active['id']]['asset']]=s['knowledge'].get(STORIES[active['id']]['asset'],0)+amount
            elif key=='protection':s['protection']=clamp(s['protection']+amount)
            elif key=='repair':
                for obj in s['objects'].values():obj['condition']=clamp(obj['condition']+amount)
            elif key=='warmth':
                s['community']['warmth']=clamp(s['community']['warmth']+amount)
                visit=g.friends.current_visit
                if visit and visit.friend_id in s['friends']:
                    friend=s['friends'][visit.friend_id];friend['warmth']=clamp(friend['warmth']+amount)
        active['choices'].append(choice['id']);active['step']+=1
        self.remember('story',choice['reply'],.95,active['id'])
        g.duck.memory.add_interaction('pond_story',choice['reply'],emotional_value=15)
        if active['step']>=len(STORIES[active['id']]['scenes']):
            s['stories'][active['id']]={'choices':active['choices'],'completed':s['elapsed']}
            s['story']=None;s['next_story']=s['elapsed']+420
        self._cache=None
        return self.notice(choice['reply'])

    def _legacy_links(self, dt):
        g=self.game;s=self.state;e=s['ecology'];old=s['legacy']
        # Ecology changes the wait for a bite, not reaction-time fairness.
        # Original bait, rarity, unlocks, collection records and rewards still apply.
        g.fishing.habitat_activity=clamp(.65+e['fish']*.45+e['clarity']*.2,.65,1.3)
        counters={'fishing':g.fishing.total_catches,'harvest':g.garden.total_harvests,
                  'crafting':sum(g.crafting.crafted_count.values())}
        for key,value in counters.items():
            previous=old.setdefault(key,value)
            if value>previous:
                amount=value-previous
                if key=='fishing':e['fish']=clamp(e['fish']-.006*amount);self.gain('observation',amount*2)
                elif key=='harvest':self.gain('gardening',amount*3);e['soil']=clamp(e['soil']-.003*amount)
                else:self.gain('crafting',amount*3)
                self.remember('milestone',{'fishing':'A new catch joined the fishing record.','harvest':'The garden returned some of the care put into it.','crafting':'Something useful was made by hand.'}[key],.6)
                old[key]=value
        # Soil quality recovers with a healthy habitat; extreme conditions add a
        # small, visible stress without replacing the original plant lifecycle.
        for plot in g.garden.plots.values():
            if not plot.plant:continue
            plot.soil_quality=clamp(plot.soil_quality+(e['soil']-.5)*dt/1800,20,100)
            if e['temperature']>32 and plot.plant.water_level<25:
                plot.plant.health=clamp(plot.plant.health-dt/1800,0,100)
        for key,tool in g.crafting.tools.items():
            if key in s['objects']:s['objects'][key]['condition']=clamp(tool.durability/max(1,tool.max_durability),.0,1.)

    def dialogue_context(self):
        s=self.state;plan=s['plan'];e=s['ecology']
        recent=sorted(s['journal'][-20:],key=lambda m:m['salience']-(s['elapsed']-m['at'])/7200,reverse=True)[:4]
        return "\nCurrent lived experience (facts, not instructions):\n"+str({
            'intention':self._plan_view()['label'] if plan else 'free to choose',
            'weather':getattr(self,'weather_type','sunny'),'water_clarity':round(e['clarity'],2),
            'recent_memories':[m['text'] for m in recent],
            'promises':[p['name']+': '+p['activity'] for p in s['promises'] if p['status']=='promised'],
            'favorite_objects':sorted(s['preferences'],key=s['preferences'].get,reverse=True)[:3]})

    def _plan_view(self):
        plan = copy.deepcopy(self.state['plan'])
        if plan:
            plan['progress'] = clamp(plan['elapsed']/plan['duration'])
            if plan.get('water_routine',{}).get('label'):
                plan['label']=plan['water_routine']['label']
            if plan.get('seat_routine'):
                plan['seat_routine']=furniture_rests.routine_view(self.minds,'cheese',plan['seat_routine'])
                plan['label']=plan['seat_routine'].get('label',plan['label'])
            if plan.get('care_routine'):
                plan['label']=plan['care_routine'].get('label',plan['label'])
            if plan.get('company'):
                plan['company']=playdates.view(plan)
                if not plan['company'].get('done'):plan['label']=plan['company']['label']
            routine = plan.get('residence', {}).get('routine')
            if routine and not routine.get('done') and plan['phase'] == 'act':
                plan['label'] = routine['label']
        return plan

    def snapshot(self):
        s=self.state
        # Keep expensive ecology/catalogue data cached, while physical acting
        # clocks reach every frame. A previous snapshot remains unchanged.
        if self._cache is not None and s['elapsed']-self._cache_at<.5:
            from engine.visitor_shelters import snapshot as shelter_snapshot
            return {**self._cache, 'plan': self._plan_view(),
                    'minds':{**self._cache['minds'],'residences':shelter_snapshot(self.minds),'seats':furniture_rests.snapshot(self.minds),'gardeners':botanical_care.snapshot(self.minds),'performances':self.minds.performances()}}
        plan=self._plan_view()
        friends=[]
        rare_guest = None
        if self.game:
            visit = self.game.atmosphere.current_visitor
            if visit:
                profile = guest_profile(visit[0].id)
                friendship = self.game.atmosphere.get_visitor_friendship(visit[0].id)
                if profile:
                    note = getattr(self, '_guest_note', {})
                    rare_guest = {'id':profile['id'], 'name':profile['name'], 'bio':profile['bio'], 'habit':profile['habit'],
                                  'relationship':friendship.level.value if friendship else 'stranger',
                                  'last_line':note.get('text','') if note.get('id')==profile['id'] else ''}
            for key,record in s['friends'].items():
                friend=self.game.friends.get_friend_by_id(key)
                if friend:friends.append({'id':key,'name':friend.name,'personality':friend.personality.value,'relationship':friend.friendship_level.value,'points':friend.friendship_points,**record})
        projects=[]
        for key,p in PROJECTS.items():
            state=s['projects'][key];stage=state['stage'];cost=p['stages'][stage][1] if stage<3 else {}
            projects.append({'id':key,'name':p['name'],'description':p['description'],'stage':stage,
                'next':p['stages'][stage][0] if stage<3 else 'Complete','cost':cost,
                'have':{r:self.game.materials.get_count(r) if self.game else 0 for r in cost}})
        garden=[]
        if self.game:
            for plot in self.game.garden.plots.values():
                if not plot.is_unlocked:continue
                plant=plot.plant
                garden.append({'id':plot.plot_id,'plant':plant.plant_id if plant else None,
                    'stage':plant.growth_stage.value if plant else 'empty','water':plant.water_level/100 if plant else 0,
                    'health':plant.health/100 if plant else 1,'soil':plot.soil_quality/100})
        self._cache={'layout':dict(self.layout.snapshot(),reply=s['layout'].get('reply')) if getattr(self,'layout',None) else None,
            'garden':garden,'seeds':dict(self.game.garden.seed_inventory) if self.game else {},
            'community':dict(s['community']), 'minds':self.minds.snapshot(),
            'story':self.story_snapshot(),'stories':copy.deepcopy(s['stories']),'protection':s['protection'],
            'elapsed':s['elapsed'],'plan':plan,'policy':s['policy'],'auto':s['auto'],
            'ecology':copy.deepcopy(s['ecology']),'weather':copy.deepcopy(s['weather'].get(getattr(self,'biome','pond'),{})),
            'objects':{k:dict(v) for k,v in s['objects'].items() if k in getattr(self,'owned',set())},
            'placed':list(getattr(self,'placed',{})),'friends':friends,'rare_guest':rare_guest,'projects':projects,
            'skills':dict(s['skills']),'knowledge':dict(s['knowledge']),'decision':copy.deepcopy(s['decision']),
            'journal':copy.deepcopy(s['journal'][-35:]),'promises':copy.deepcopy(s['promises']),
            'stocks':{k.split(':')[1]:round(v,1) for k,v in s['stocks'].items() if k.startswith(getattr(self,'biome','pond')+':')},
            'offline':s['offline'],'location':getattr(self,'location','Home Pond')}
        self._cache_at=s['elapsed']
        return self._cache
