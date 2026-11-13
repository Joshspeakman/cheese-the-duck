"""Authoring source for the wonder machines and garden curiosities.

Emits client/animation/wonders.json (blueprints, saved fields, weather physics
and contact effects) and client/animation/wonder-routines.json (Cheese's timed
physical sequences). Run from any directory.

Rules of the data:
- A field is saved object state, bounded [min, max]. Only native Python applies
  physics and contact effects; the renderer reads them.
- physics rows: [field, op, value, when]. op 'rate' adds value*dt, 'decay'
  eases toward value with a half-life-like constant, 'wrap' advances cyclically.
- triggers: [condition, effects] fire once whenever the condition is reached.
- effects: lists of [field, op, value]; op set/add/mul/max/min/wrap.
- A routine's events name effects of its own object. Contact happens at those
  moments, not at the start or as a completion bonus.
- when: every tag must hold for Cheese to choose (or be offered) a routine.
  prefer: matching tags make the routine more appealing in that context.
- Pose keys x/y/b/w/l/r/reach/contact/eye/mark follow the D10 work rig; other
  numeric keys (door, lever, dial...) are object parts eased with the same clock.
No routine grants inventory, coins, or rewards: wonders are decoration with
real, persistent physical state.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'client/animation'
ITEMS, ROUTINES = {}, {}


def item(key, kind, w, h, scale, material, skill, verb, fields, physics=(), triggers=(), effects=None, parts=(), shelter=False):
    ITEMS[key] = dict(type=kind, w=w, h=h, scale=scale, material=material, skill=skill, verb=verb, portable=False,
                      fields={k: list(v) for k, v in fields.items()}, physics=[list(r) for r in physics],
                      triggers=[list(t) for t in triggers], effects=effects or {}, parts=list(parts), shelter=shelter)


def k(at, **pose):
    return [at, pose]


def routine(key, obj, label, duration, track, events=(), *, when=(), prefer=(), ages=None, need=None, tool='wing', say=None):
    assert key not in ROUTINES, key
    for _, name in events:
        assert name in ITEMS[obj]['effects'], (key, name)
    ROUTINES[key] = dict(item=obj, label=label, duration=duration, track=[k(0), *track, k(1)], events=[list(e) for e in events],
                         when=list(when), prefer=list(prefer), ages=ages, need=need, tool=tool, say=say)


YOUNG = ['hatchling', 'duckling']
GROWN = ['juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary']

# --------------------------------------------------------------------------- garden curiosities
item('topiary_duck', 'topiary', 120, 112, 0.363, 'leaf', 'gardening', 'Tend',
     dict(growth=(.35, 0, 1), moisture=(.6, 0, 1), snow=(0, 0, 1), blossom=(0, 0, 1), trims=(0, 0, 9999)),
     physics=[('growth', 'rate', .00005, 'growing'), ('growth', 'rate', .0001, 'wet&growing'), ('moisture', 'rate', -.00018, 'dry&warm'),
              ('moisture', 'rate', .004, 'wet'), ('snow', 'rate', .004, 'snow'), ('snow', 'rate', -.003, 'warm'),
              ('blossom', 'decay', 1, 'spring'), ('blossom', 'decay', 0, '!spring')],
     effects=dict(snip_bill=[['growth', 'add', -.12], ['trims', 'add', 1]], snip_tail=[['growth', 'add', -.1], ['trims', 'add', 1]],
                  snip_wing=[['growth', 'add', -.08]], pour=[['moisture', 'add', .45]], shake=[['snow', 'mul', .2]], brush=[['snow', 'set', 0]]),
     parts=['shears', 'can', 'hide'], shelter=True)
routine('topiary_trim_bill', 'topiary_duck', 'Clipping the hedge duck a sharper bill', 26,
        [k(.12, reach=.5, contact=1, anchor='bill', shears=1), k(.3, reach=.9, contact=1, anchor='bill', shears=0, eye='o'), k(.38, shears=1, contact=1, anchor='bill'),
         k(.5, contact=1, anchor='bill', shears=0, mark='*'), k(.68, x=-.8, y=-.3, eye='^', mark='?'), k(.86, w=.4, eye='^')],
        [(.3, 'snip_bill'), (.5, 'snip_bill')], when=['growth>.25'], prefer=['growth>.6'], ages=GROWN, tool='shears')
routine('topiary_tail_flourish', 'topiary_duck', 'Shaping a curly tail on the hedge', 24,
        [k(.15, x=.6, reach=.7, contact=1, anchor='tail', shears=1), k(.33, y=.6, b=.4, contact=1, anchor='tail', shears=0), k(.5, contact=1, anchor='rump', shears=1),
         k(.62, contact=1, anchor='rump', shears=0, mark='*'), k(.82, x=-1, eye='^', w=.7)],
        [(.33, 'snip_tail'), (.62, 'snip_wing')], when=['growth>.2'], prefer=['fall', 'summer'], ages=GROWN, tool='shears')
routine('topiary_water_roots', 'topiary_duck', 'Watering the roots of the hedge duck', 18,
        [k(.15, reach=.4, contact=1, anchor='roots', can=1), k(.35, y=.8, b=.4, contact=1, anchor='roots', can=1, mark='~'), k(.6, contact=1, anchor='roots', can=.4),
         k(.8, can=0, eye='^')],
        [(.38, 'pour')], when=['!wet', '!snow'], prefer=['moisture<.35', 'summer'], tool='can')
routine('topiary_shake_snow', 'topiary_duck', "Shaking the snow off the hedge duck's back", 20,
        [k(.15, reach=1, contact=1, anchor='flank', w=.6), k(.3, contact=1, anchor='flank', b=-.4, w=1, mark='*'), k(.45, contact=1, anchor='flank', b=.4),
         k(.6, contact=1, anchor='flank', w=.8), k(.8, y=.5, eye='O', mark='brr')],
        [(.3, 'shake'), (.6, 'brush')], when=['snow_on'], tool='wing')
routine('topiary_mirror_pose', 'topiary_duck', 'Striking the same pose as the hedge duck', 20,
        [k(.15, x=-.6, eye='o', mark='?'), k(.3, y=-.6, w=1, b=-.4), k(.45, y=-.8, w=1, eye='^'), k(.6, x=.8, y=-.4, l=1, mark='!'), k(.8, w=.5, eye='^', mark='ha')],
        [], when=['dry'], prefer=['happy', 'day'], tool='none', say='topiary_mirror')
routine('topiary_rain_tuck', 'topiary_duck', 'Hunkering down against the hedge duck\'s planter out of the rain', 34,
        [k(.12, x=.8, y=.8, b=.5, hide=.5), k(.28, y=1.4, b=.8, hide=1, eye='-'), k(.5, y=1.4, b=.8, hide=1, eye='-', mark='zz'), k(.72, y=1.2, b=.7, hide=1, eye='o'),
         k(.88, y=.5, hide=.4, w=.3)],
        [], when=['wet'], prefer=['young', 'tired'], tool='none')

item('zen_garden', 'zen', 140, 72, 0.306, 'stone', 'observation', 'Rake',
     dict(raked=(.8, 0, 1), pattern=(0, 0, 3), leaves=(0, 0, 1), stone=(0, 0, 3), calm=(0, 0, 1), rakes=(0, 0, 9999)),
     physics=[('raked', 'rate', -.0005, 'wet'), ('raked', 'rate', -.0002, 'windy'), ('leaves', 'rate', .0002, 'fall'), ('leaves', 'rate', .0001, 'windy'),
              ('calm', 'decay', 0, 'always')],
     effects=dict(rake_start=[['raked', 'set', .25]], rake_waves=[['pattern', 'set', 0], ['raked', 'add', .38]], rake_rings=[['pattern', 'set', 1], ['raked', 'add', .38]],
                  rake_spiral=[['pattern', 'set', 2], ['raked', 'add', .38]], finish=[['raked', 'set', 1], ['rakes', 'add', 1]], gather=[['leaves', 'mul', .35]],
                  lift=[['stone', 'wrap', 1]], breathe=[['calm', 'add', .35]], smooth=[['raked', 'max', .55], ['pattern', 'set', 3]]),
     parts=['rake', 'broom', 'pebble'])
routine('zen_rake_waves', 'zen_garden', 'Raking slow waves through the sand', 30,
        [k(.1, reach=.6, contact=1, anchor='bed_l', rake=1), k(.3, x=.5, contact=1, anchor='bed_c', rake=1), k(.5, x=1, contact=1, anchor='bed_r', rake=1, eye='-'),
         k(.7, x=.4, contact=1, anchor='bed_c', rake=1), k(.88, rake=0, eye='^')],
        [(.1, 'rake_start'), (.5, 'rake_waves'), (.7, 'rake_waves'), (.88, 'finish')], when=['dry'], prefer=['raked<.5', 'day'], ages=GROWN, tool='rake')
routine('zen_rake_rings', 'zen_garden', 'Drawing careful rings around the big stone', 32,
        [k(.12, reach=.8, contact=1, anchor='stone', rake=1), k(.3, x=.6, y=.4, contact=1, anchor='ring_n', rake=1), k(.48, x=1, contact=1, anchor='ring_e', rake=1),
         k(.66, x=.3, y=.5, contact=1, anchor='ring_s', rake=1, eye='-'), k(.86, rake=0, w=.3, eye='^')],
        [(.12, 'rake_start'), (.48, 'rake_rings'), (.66, 'rake_rings'), (.86, 'finish')], when=['dry'], prefer=['dusk', 'calm'], ages=GROWN, tool='rake')
routine('zen_rake_spiral', 'zen_garden', 'Pulling one long spiral from the centre outward', 34,
        [k(.12, contact=1, anchor='bed_c', rake=1), k(.3, x=.3, y=.4, contact=1, anchor='ring_n', rake=1), k(.5, x=.9, contact=1, anchor='ring_e', rake=1),
         k(.7, x=1.2, y=.3, contact=1, anchor='bed_r', rake=1, eye='-'), k(.88, rake=0, eye='^', mark='~')],
        [(.12, 'rake_start'), (.5, 'rake_spiral'), (.7, 'rake_spiral'), (.88, 'finish')], when=['dry'], prefer=['night', 'sad'], ages=GROWN, tool='rake')
routine('zen_sweep_leaves', 'zen_garden', 'Sweeping fallen leaves off the sand', 22,
        [k(.15, reach=.7, contact=1, anchor='bed_l', broom=1), k(.35, x=.5, contact=1, anchor='bed_c', broom=1, mark='~'), k(.55, x=1, contact=1, anchor='bed_r', broom=1),
         k(.75, broom=.3, eye='^')],
        [(.35, 'gather'), (.55, 'gather')], when=['leaves>.25'], prefer=['fall', 'windy'], tool='broom')
routine('zen_move_stone', 'zen_garden', 'Rolling a pebble to a better spot', 20,
        [k(.15, y=1, b=.6, reach=.6, contact=1, anchor='pebble', pebble=0), k(.35, y=1.3, b=.8, contact=1, anchor='pebble', pebble=.5, mark='!'),
         k(.55, x=.6, y=1.2, contact=1, anchor='pebble', pebble=1), k(.78, y=-.3, eye='o', mark='?'), k(.9, eye='^')],
        [(.55, 'lift')], when=['dry'], prefer=['happy'], tool='wing')
routine('zen_sit_breathe', 'zen_garden', 'Sitting at the sand\'s edge and breathing slowly', 30,
        [k(.12, y=.8, b=.6, eye='-'), k(.3, y=.6, b=.3, w=.4, eye='-'), k(.45, y=.8, b=.6, eye='-'), k(.6, y=.6, b=.3, w=.4, eye='-', mark='~'), k(.8, y=.8, b=.6, eye='-'),
         k(.92, eye='^')],
        [(.45, 'breathe'), (.8, 'breathe')], when=['!storm'], prefer=['sad', 'lonely', 'tired', 'dusk'], tool='none')
routine('zen_smooth_after_rain', 'zen_garden', 'Smoothing rain pits out of the sand', 24,
        [k(.15, reach=.7, contact=1, anchor='bed_l', rake=1), k(.4, x=.6, contact=1, anchor='bed_c', rake=1), k(.65, x=1, contact=1, anchor='bed_r', rake=1, mark='~'),
         k(.86, rake=0, eye='^')],
        [(.4, 'smooth'), (.65, 'smooth')], when=['dry', 'raked<.4'], ages=GROWN, tool='rake')

item('ice_sculpture', 'ice', 112, 120, 0.31, 'ice', 'crafting', 'Carve',
     dict(melt=(0, 0, 1), detail=(.7, 0, 1), shine=(.4, 0, 1), puddle=(0, 0, 1), tarp=(0, 0, 1), frost=(0, 0, 1)),
     physics=[('melt', 'rate', .00012, 'warm&!tarp'), ('melt', 'rate', .00004, 'warm&tarp'), ('melt', 'rate', .00018, 'sun&!tarp'), ('puddle', 'rate', .0001, 'warm'),
              ('puddle', 'rate', -.0008, 'cold'), ('melt', 'rate', -.0002, 'cold'), ('detail', 'rate', -.00008, 'warm&!tarp'), ('shine', 'rate', -.00008, 'always'),
              ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.004, 'warm')],
     effects=dict(chisel=[['detail', 'add', .14], ['melt', 'add', .015]], polish=[['shine', 'add', .3], ['frost', 'set', 0]], cover=[['tarp', 'set', 1]],
                  uncover=[['tarp', 'set', 0]], mop=[['puddle', 'mul', .2]], lick=[['detail', 'add', -.02], ['frost', 'set', 0]], breath=[['frost', 'add', .35]],
                  pack=[['melt', 'add', -.12]], mould=[['melt', 'set', .45], ['detail', 'set', .2], ['puddle', 'mul', .3]]),
     parts=['chisel', 'cloth', 'tarp_hold', 'mould'])
routine('ice_chisel_feathers', 'ice_sculpture', 'Chiselling fresh feathers into the ice swan', 28,
        [k(.12, reach=.7, contact=1, anchor='wing', chisel=1), k(.25, contact=1, anchor='wing', chisel=0, b=-.2, mark='tk'), k(.38, contact=1, anchor='wing', chisel=1),
         k(.5, contact=1, anchor='neck', chisel=0, mark='tk'), k(.66, x=-.7, eye='o'), k(.85, eye='^', w=.4)],
        [(.25, 'chisel'), (.5, 'chisel')], when=['melt<.85'], prefer=['detail<.5', 'cold'], ages=GROWN, tool='chisel')
routine('ice_polish', 'ice_sculpture', 'Buffing the ice until it shines', 22,
        [k(.15, reach=.6, contact=1, anchor='breast', cloth=1), k(.32, x=.3, contact=1, anchor='wing', cloth=1, mark='*'), k(.5, contact=1, anchor='neck', cloth=1),
         k(.68, x=-.6, cloth=0, eye='^', mark='*')],
        [(.32, 'polish'), (.5, 'polish')], prefer=['frost>.4', 'day'], tool='cloth')
routine('ice_tarp_shade', 'ice_sculpture', 'Throwing a canvas over the sculpture to keep the sun off', 20,
        [k(.15, reach=1, w=.8, contact=1, anchor='flank', tarp_hold=1), k(.4, y=-.6, w=1, contact=1, anchor='flank', tarp_hold=1), k(.6, contact=1, anchor='base', tarp_hold=.3),
         k(.8, eye='^')],
        [(.6, 'cover')], when=['tarp<.5', 'warm'], prefer=['sun', 'melt>.3'], tool='wing')
routine('ice_tarp_reveal', 'ice_sculpture', 'Tugging the canvas off for the evening', 18,
        [k(.15, reach=1, contact=1, anchor='base', tarp_hold=.3), k(.4, y=-.6, w=1, contact=1, anchor='flank', tarp_hold=1), k(.6, w=1, b=-.4, mark='ta-da'), k(.85, eye='^')],
        [(.45, 'uncover')], when=['tarp>.5'], prefer=['dusk', 'night', 'cold'], tool='wing')
routine('ice_mop_meltwater', 'ice_sculpture', 'Mopping up the meltwater puddle', 18,
        [k(.15, y=1, b=.6, reach=.5, contact=1, anchor='puddle', cloth=1), k(.4, x=.6, y=1.2, contact=1, anchor='puddle', cloth=1, mark='~'), k(.65, x=-.2, contact=1, anchor='puddle', cloth=1),
         k(.85, cloth=0, eye='^')],
        [(.4, 'mop'), (.65, 'mop')], when=['puddle>.2'], tool='cloth')
routine('ice_tongue_test', 'ice_sculpture', 'Licking the ice to see if it is really cold', 16,
        [k(.15, x=.6, y=.2, eye='o', mark='?'), k(.32, x=1.1, y=.1, contact=1, anchor='breast', mark='!'), k(.45, x=1.1, eye='O', mark='!!'), k(.62, x=-.6, b=-.5, w=1, eye='>'),
         k(.85, eye='^', mark='brr')],
        [(.32, 'lick')], ages=YOUNG + ['juvenile'], prefer=['young', 'happy'], tool='none', say='ice_lick')
routine('ice_frost_breath', 'ice_sculpture', 'Huffing frosty breath onto the ice', 16,
        [k(.15, x=.6, eye='o'), k(.32, x=.9, b=-.3, mark='hhh'), k(.5, x=.9, mark='hhh'), k(.7, x=-.4, eye='^', w=.4)],
        [(.32, 'breath'), (.5, 'breath')], when=['cold'], prefer=['winter'], tool='none')
routine('ice_slush_mould', 'ice_sculpture', 'Scooping meltwater slush into the swan mould to set again overnight', 28,
        [k(.12, y=1, b=.6, reach=.5, contact=1, anchor='puddle', mould=0), k(.3, y=.4, contact=1, anchor='base', mould=.5, mark='slsh'), k(.5, y=-.2, contact=1, anchor='breast', mould=1, mark='pat'),
         k(.72, x=-.5, mould=1, eye='o', mark='...'), k(.9, eye='^')],
        [(.5, 'mould')], when=['melt>.6'], prefer=['dusk', 'night'], tool='bucket')
routine('ice_pack_snow', 'ice_sculpture', 'Packing snow into the melted spots', 22,
        [k(.15, y=1, b=.5, reach=.4), k(.3, y=-.2, reach=.8, contact=1, anchor='base', w=.5), k(.5, contact=1, anchor='flank', mark='pat'), k(.7, contact=1, anchor='breast', mark='pat'),
         k(.88, eye='^')],
        [(.5, 'pack'), (.7, 'pack')], when=['snow', 'melt>.15'], tool='wing')

item('sand_castle', 'sandcastle', 132, 96, 0.299, 'sand', 'crafting', 'Build',
     dict(towers=(2, 0, 4), moat=(0, 0, 1), erosion=(0, 0, 1), flag=(0, 0, 1), damp=(.4, 0, 1), builds=(0, 0, 9999)),
     physics=[('erosion', 'rate', .0016, 'wet'), ('erosion', 'rate', .0007, 'windy'), ('damp', 'rate', .003, 'wet'), ('damp', 'rate', -.0012, 'dry&warm'),
              ('moat', 'rate', -.0015, 'dry&warm'), ('moat', 'rate', .002, 'wet')],
     triggers=[('erosion>=.98', [['towers', 'set', 0], ['flag', 'set', 0], ['erosion', 'set', .55]]), ('erosion>=.7&towers>=3', [['towers', 'add', -1]])],
     effects=dict(pat=[['erosion', 'add', -.15]], tower=[['towers', 'add', 1], ['builds', 'add', 1]], dig=[['moat', 'max', .15]], pour=[['moat', 'add', .5]],
                  flag=[['flag', 'set', 1]], wet_sand=[['damp', 'add', .4]], stomp=[['towers', 'set', 0], ['flag', 'set', 0], ['erosion', 'set', .8]],
                  shell=[['erosion', 'add', -.05]]),
     parts=['bucket', 'spade', 'flagstick'])
routine('sand_tower_raise', 'sand_castle', 'Packing a new tower from a bucket of wet sand', 30,
        [k(.12, y=1, b=.6, reach=.4, contact=1, anchor='sandpile', bucket=1), k(.28, y=.2, contact=1, anchor='keep', bucket=1), k(.42, y=-.4, b=-.4, w=.8, contact=1, anchor='keep', bucket=.5, mark='flip'),
         k(.55, contact=1, anchor='keep', bucket=0, mark='pat'), k(.75, x=-.6, eye='o', mark='!'), k(.9, eye='^')],
        [(.12, 'wet_sand'), (.55, 'tower')], when=['towers<4', 'dry'], prefer=['summer', 'happy'], tool='bucket')
routine('sand_dig_moat', 'sand_castle', 'Digging a moat around the walls', 26,
        [k(.15, y=1, b=.6, reach=.6, contact=1, anchor='moat_l', spade=1), k(.35, x=.6, y=1.2, contact=1, anchor='moat_c', spade=1, mark='scoop'),
         k(.55, x=1, y=1.2, contact=1, anchor='moat_r', spade=1), k(.8, spade=0, eye='^')],
        [(.35, 'dig'), (.55, 'dig')], when=['moat<.4', 'dry'], ages=GROWN, tool='spade')
routine('sand_fill_moat', 'sand_castle', 'Pouring pond water into the moat', 20,
        [k(.15, reach=.4, contact=1, anchor='moat_l', bucket=1), k(.35, x=.3, contact=1, anchor='moat_c', bucket=1, mark='~'), k(.6, contact=1, anchor='moat_r', bucket=.3, mark='~'),
         k(.82, eye='^')],
        [(.35, 'pour')], when=['moat<.6', 'moat>.05', '!cold'], tool='bucket')
routine('sand_plant_flag', 'sand_castle', 'Planting a tiny flag on the tallest tower', 16,
        [k(.15, y=-.6, reach=1, w=.8, contact=1, anchor='tip', flagstick=1), k(.4, y=-.8, contact=1, anchor='tip', flagstick=1, mark='!'), k(.6, w=1, b=-.4, eye='^', mark='hup'),
         k(.85, eye='^')],
        [(.4, 'flag')], when=['flag<.5', 'towers>0'], tool='flagstick', say='sand_flag')
routine('sand_patch_walls', 'sand_castle', 'Patting rain-slumped walls back into shape', 24,
        [k(.15, y=.6, reach=.6, contact=1, anchor='wall_l', mark='pat'), k(.35, x=.4, contact=1, anchor='keep', mark='pat'), k(.55, x=.9, contact=1, anchor='wall_r', mark='pat'),
         k(.8, eye='^')],
        [(.15, 'pat'), (.35, 'pat'), (.55, 'pat')], when=['erosion>.2', '!wet'], prefer=['erosion>.5'], tool='wing')
routine('sand_shell_trim', 'sand_castle', 'Pressing little shells into the walls', 22,
        [k(.15, y=1, b=.6, reach=.3, eye='o'), k(.3, y=-.2, contact=1, anchor='wall_l', mark='.'), k(.5, x=.4, contact=1, anchor='keep', mark='.'), k(.7, x=.9, contact=1, anchor='wall_r', mark='.'),
         k(.88, eye='^', w=.4)],
        [(.3, 'shell'), (.5, 'shell'), (.7, 'shell')], when=['towers>0', 'dry'], prefer=['young', 'summer'], tool='wing')
routine('sand_kaiju_stomp', 'sand_castle', 'Stomping the castle flat like a giant monster', 18,
        [k(.12, y=-.8, w=1, b=-.5, eye='>', mark='RAWR'), k(.28, x=.8, l=1, eye='>'), k(.38, x=1, b=.8, contact=1, anchor='keep', mark='STOMP'), k(.5, x=1.2, r=1, contact=1, anchor='wall_r'),
         k(.66, b=-.6, w=1, eye='^', mark='ha!'), k(.85, eye='^')],
        [(.38, 'stomp')], when=['towers>0'], prefer=['grumpy', 'young'], tool='none', say='sand_stomp')

item('gong', 'gong', 104, 124, 0.355, 'bronze', 'music', 'Strike',
     dict(ring=(0, 0, 1), shine=(.6, 0, 1), muted=(0, 0, 1), strikes=(0, 0, 9999), dust=(0, 0, 1)),
     physics=[('ring', 'decay', 0, 'always'), ('ring', 'decay', 0, 'muted>.5'), ('shine', 'rate', -.0004, 'wet'), ('dust', 'rate', .0003, 'dry&windy')],
     effects=dict(tap=[['ring', 'max', .35], ['strikes', 'add', 1], ['muted', 'set', 0]], boom=[['ring', 'set', 1], ['strikes', 'add', 1], ['muted', 'set', 0]],
                  damp=[['ring', 'mul', .1], ['muted', 'set', 1]], tock=[['ring', 'max', .08]], buff=[['shine', 'add', .3], ['dust', 'set', 0]], release=[['muted', 'set', 0]]),
     parts=['mallet', 'cloth', 'ear'])
routine('gong_peck_post', 'gong', 'Pecking the gong post and giggling at the tiny tock', 16,
        [k(.15, x=.6, y=.4, eye='o', mark='?'), k(.3, x=.9, y=.6, contact=1, anchor='post_foot', mark='tok'), k(.45, x=.4, eye='^', mark='hee'), k(.6, x=.9, y=.6, contact=1, anchor='post_foot', mark='tok'),
         k(.8, b=-.4, w=.6, eye='^')],
        [(.3, 'tock'), (.6, 'tock')], ages=YOUNG, prefer=['young', 'happy'], tool='none')
routine('gong_soft_tap', 'gong', 'Tapping the gong softly and listening', 18,
        [k(.15, reach=.6, contact=0, mallet=.5), k(.3, reach=.9, contact=1, anchor='boss', mallet=1, mark='~'), k(.45, x=-.3, mallet=.3, eye='-', mark='bong'), k(.75, x=.4, y=.2, eye='-', mark='~'),
         k(.9, eye='^')],
        [(.3, 'tap')], when=['!night_late'], prefer=['dawn', 'calm'], tool='mallet')
routine('gong_mighty_bong', 'gong', 'Winding up and giving the gong a mighty BONG', 18,
        [k(.12, x=-.8, w=1, b=-.4, mallet=1, eye='>'), k(.25, x=-1.1, w=1, mallet=1, mark='...'), k(.34, x=.9, contact=1, anchor='boss', mallet=1, mark='BONG'), k(.5, x=-.4, b=.6, eye='O', mark='!!'),
         k(.75, eye='@', mark='~'), k(.9, eye='^')],
        [(.34, 'boom')], when=['!night_late'], prefer=['happy', 'day'], ages=GROWN, tool='mallet', say='gong_bong')
routine('gong_dinner_call', 'gong', 'Striking three slow beats to call friends over', 24,
        [k(.12, reach=.8, contact=1, anchor='boss', mallet=1, mark='1'), k(.25, mallet=.3), k(.38, contact=1, anchor='boss', mallet=1, mark='2'), k(.5, mallet=.3),
         k(.62, contact=1, anchor='boss', mallet=1, mark='3'), k(.82, y=-.5, w=.8, eye='^', mark='!')],
        [(.12, 'tap'), (.38, 'tap'), (.62, 'boom')], when=['!night_late'], prefer=['dusk', 'lonely'], ages=GROWN, tool='mallet', say='gong_dinner')
routine('gong_wing_mute', 'gong', 'Hugging the gong to stop it humming', 14,
        [k(.15, x=.6, w=.7, reach=1, contact=1, anchor='rim'), k(.4, x=.9, w=1, contact=1, anchor='boss', eye='-', mark='shh'), k(.7, x=.4, w=.4, eye='^')],
        [(.4, 'damp')], when=['ring>.15'], tool='wing')
routine('gong_polish', 'gong', 'Polishing the bronze face in circles', 24,
        [k(.15, reach=.7, contact=1, anchor='rim', cloth=1), k(.32, x=.3, contact=1, anchor='boss', cloth=1, mark='*'), k(.5, x=.6, contact=1, anchor='rim_r', cloth=1), k(.7, contact=1, anchor='boss', cloth=1),
         k(.88, cloth=0, eye='^', mark='*')],
        [(.32, 'buff'), (.7, 'buff')], prefer=['shine<.4', 'dust>.3'], tool='cloth')
routine('gong_ear_to_bronze', 'gong', 'Pressing an ear to the gong to hear the last of the hum', 20,
        [k(.15, x=.8, y=.3, reach=.4, ear=1), k(.35, x=1.1, y=.3, contact=1, anchor='rim', ear=1, eye='-'), k(.6, x=1.1, eye='-', mark='~'), k(.8, x=.2, eye='o', mark='!')],
        [], when=['ring>.05'], prefer=['young', 'calm'], tool='none')
routine('gong_cover_ears', 'gong', 'Bonging the gong, then clapping both wings over his ears', 16,
        [k(.15, reach=.7, mallet=1, eye='o'), k(.28, contact=1, anchor='boss', mallet=1, mark='bong'), k(.38, x=-.8, b=.6, w=1, mallet=0, eye='>', mark='!!'),
         k(.62, x=-.8, b=.5, w=1, eye='>'), k(.85, w=.3, eye='^')],
        [(.28, 'boom')], when=['!night_late'], ages=YOUNG + ['juvenile'], prefer=['young'], tool='mallet', say='gong_ears')

# --------------------------------------------------------------------------- lights and skies
item('aurora', 'aurora', 132, 112, 0.363, 'glass', 'observation', 'Tune',
     dict(power=(0, 0, 1), hue=(.4, 0, 1), ribbons=(2, 1, 5), glow=(0, 0, 1), drift=(0, 0, 1)),
     physics=[('glow', 'decay', 1, 'powered'), ('glow', 'decay', 0, '!powered'), ('drift', 'wrap', .006, 'powered'), ('hue', 'wrap', .0006, 'powered&night')],
     effects=dict(on=[['power', 'set', 1]], off=[['power', 'set', 0]], hue=[['hue', 'wrap', .18]], ribbon=[['ribbons', 'wrap', 1]], dim=[['power', 'set', .6]]),
     parts=['dial', 'switch'])
routine('aurora_switch_on', 'aurora', 'Flicking on the aurora lamp as the sky darkens', 14,
        [k(.15, reach=.6, contact=1, anchor='switch', switch=0), k(.35, contact=1, anchor='switch', switch=1, mark='click'), k(.55, y=-.6, x=-.6, eye='O', mark='ooh'), k(.85, eye='^')],
        [(.35, 'on')], when=['power<.5'], prefer=['dusk', 'night'], tool='wing', say='aurora_on')
routine('aurora_tune_colour', 'aurora', 'Turning the brass dial through greens and violets', 22,
        [k(.15, reach=.7, contact=1, anchor='dial', dial=0), k(.35, contact=1, anchor='dial', dial=.5, eye='o'), k(.5, y=-.4, x=-.3, eye='O'), k(.65, contact=1, anchor='dial', dial=1),
         k(.85, y=-.5, eye='^', mark='*')],
        [(.35, 'hue'), (.65, 'hue')], when=['power>.5'], prefer=['night'], tool='wing')
routine('aurora_add_ribbon', 'aurora', 'Sliding another lens in for an extra ribbon of light', 18,
        [k(.15, reach=.8, contact=1, anchor='lens', w=.4), k(.4, contact=1, anchor='lens', mark='clk'), k(.6, y=-.6, x=-.4, eye='O', mark='!'), k(.85, eye='^')],
        [(.4, 'ribbon')], when=['power>.5'], tool='wing')
routine('aurora_lie_and_watch', 'aurora', 'Lying back on the grass to watch the lights ripple', 40,
        [k(.12, y=1, b=.8, eye='o'), k(.25, y=1.6, b=1, x=-.4, eye='o'), k(.5, y=1.6, b=1, x=-.4, eye='^', mark='~'), k(.75, y=1.6, b=1, x=-.4, eye='-'), k(.9, y=.8, b=.5, eye='^')],
        [], when=['power>.5', 'dry'], prefer=['night', 'sad', 'lonely'], tool='none', say='aurora_watch')
routine('aurora_bedtime_dim', 'aurora', 'Dimming the aurora down for sleep', 14,
        [k(.15, reach=.6, contact=1, anchor='dial'), k(.4, contact=1, anchor='dial', dial=.2, eye='-'), k(.65, y=.5, b=.4, eye='-', mark='z'), k(.88, eye='-')],
        [(.4, 'dim')], when=['power>.7', 'night'], prefer=['tired'], tool='wing')
routine('aurora_switch_off', 'aurora', 'Switching off the aurora for the morning', 12,
        [k(.2, reach=.6, contact=1, anchor='switch', switch=1), k(.45, contact=1, anchor='switch', switch=0, mark='click'), k(.8, eye='^')],
        [(.45, 'off')], when=['power>.5', 'day'], tool='wing')

item('rainbow_generator', 'rainbow', 124, 112, 0.332, 'glass', 'engineering', 'Crank',
     dict(water=(.5, 0, 1), arc=(0, 0, 1), prism=(.5, 0, 1), mist=(0, 0, 1)),
     physics=[('arc', 'decay', 0, 'always'), ('mist', 'decay', 0, 'always'), ('water', 'rate', .003, 'wet'), ('water', 'rate', -.0004, 'warm&dry')],
     effects=dict(fill=[['water', 'add', .45]], aim=[['prism', 'wrap', .2]], crank=[['mist', 'set', 1], ['arc', 'max', .7], ['water', 'add', -.12]],
                  spray=[['mist', 'set', 1], ['arc', 'set', 1], ['water', 'add', -.2]]),
     parts=['crank', 'can'])
routine('rainbow_drip_splash', 'rainbow_generator', 'Splashing in the drip tray under the tank', 20,
        [k(.15, x=.5, y=.4, eye='o'), k(.3, y=.8, b=.6, contact=1, anchor='drip', mark='plip'), k(.45, b=-.6, w=1, eye='^', mark='*'), k(.6, y=.8, b=.6, contact=1, anchor='drip', mark='splsh'),
         k(.8, w=.8, eye='^', mark='hee')],
        [], when=['water>.3', '!cold'], ages=YOUNG, prefer=['young', 'summer'], tool='none')
routine('rainbow_fill_tank', 'rainbow_generator', 'Topping up the tank with pond water', 18,
        [k(.15, reach=.5, contact=1, anchor='tank', can=1), k(.4, y=-.3, contact=1, anchor='tank', can=1, mark='glug'), k(.65, can=.3), k(.85, eye='^')],
        [(.4, 'fill')], when=['water<.7', '!cold'], tool='can')
routine('rainbow_aim_prism', 'rainbow_generator', 'Turning the knob that tilts the prism toward the sun', 18,
        [k(.15, reach=.8, contact=1, anchor='prism_knob', eye='o'), k(.4, contact=1, anchor='prism_knob', mark='tik'), k(.6, x=-.5, y=-.6, eye='O'), k(.85, eye='^')],
        [(.4, 'aim')], when=['day'], tool='wing')
routine('rainbow_crank_mist', 'rainbow_generator', 'Cranking the mister until a rainbow hangs in the air', 24,
        [k(.12, reach=.7, contact=1, anchor='crank', crank=0), k(.25, contact=1, anchor='crank', crank=.5, mark='crk'), k(.38, contact=1, anchor='crank', crank=1, mark='crk'),
         k(.5, contact=1, anchor='crank', crank=1.5, mark='crk'), k(.66, x=-.7, y=-.6, w=1, eye='O', mark='!!'), k(.88, eye='^')],
        [(.38, 'crank'), (.5, 'crank')], when=['water>.2', 'day', 'dry'], prefer=['sun', 'happy'], ages=GROWN, tool='wing', say='rainbow_make')
routine('rainbow_dance_in_mist', 'rainbow_generator', 'Opening the spray valve and dancing through the rainbow mist', 24,
        [k(.12, reach=.6, contact=1, anchor='valve'), k(.22, contact=1, anchor='valve', mark='psst'), k(.35, x=.7, y=-.5, w=1, l=1, eye='^'), k(.5, x=-.7, w=1, r=1, mark='*'),
         k(.65, x=.6, y=-.6, w=1, l=1, eye='^', mark='~'), k(.85, b=.4, eye='^')],
        [(.22, 'spray')], when=['water>.25', 'warm'], prefer=['young', 'summer'], tool='wing')
routine('rainbow_after_rain', 'rainbow_generator', 'Pointing at a real rainbow, then nudging the prism knob to compare', 20,
        [k(.15, y=-.6, w=.8, eye='O', mark='!'), k(.35, x=-.8, w=1, mark='>'), k(.55, x=.8, reach=.6, contact=1, anchor='prism_knob'), k(.75, eye='^', mark='?')],
        [], when=['rainbow_sky'], tool='none', say='rainbow_compare')

item('weather_machine', 'weather', 136, 128, 0.344, 'metal', 'engineering', 'Adjust',
     dict(setting=(0, 0, 3), charge=(.3, 0, 1), cloud=(0, 0, 1), bolt=(0, 0, 1), runs=(0, 0, 9999)),
     physics=[('cloud', 'decay', 0, 'always'), ('bolt', 'decay', 0, 'always'), ('charge', 'rate', .0012, 'storm'), ('charge', 'rate', .0004, 'sun'), ('charge', 'rate', .0002, 'windy')],
     effects=dict(dial=[['setting', 'wrap', 1]], crank=[['charge', 'add', .2]], fire=[['cloud', 'set', 1], ['charge', 'add', -.35], ['runs', 'add', 1]],
                  zap=[['bolt', 'set', 1]], vent=[['cloud', 'mul', .3]]),
     parts=['dial', 'crank', 'lever'])
routine('weather_tongue_drop', 'weather_machine', 'Catching a drop from the tiny cloud on his tongue', 18,
        [k(.15, y=-.4, eye='o', mark='?'), k(.32, y=-.8, b=-.4, eye='^', mark='ahh'), k(.5, y=-.8, eye='O', mark='plip!'), k(.7, b=.3, eye='^', mark='hee'), k(.88, eye='^')],
        [], when=['cloud>.2'], ages=YOUNG + ['juvenile'], prefer=['young'], tool='none')
routine('weather_set_dial', 'weather_machine', 'Clicking the forecast dial to a new setting', 16,
        [k(.15, reach=.7, contact=1, anchor='dial', dial=0), k(.4, contact=1, anchor='dial', dial=1, mark='click'), k(.65, x=-.4, eye='o', mark='?'), k(.85, eye='^')],
        [(.4, 'dial')], tool='wing')
routine('weather_wind_dynamo', 'weather_machine', 'Winding the dynamo crank to charge the coils', 24,
        [k(.12, reach=.7, contact=1, anchor='crank', crank=0), k(.3, contact=1, anchor='crank', crank=1, b=.3, mark='wrr'), k(.48, contact=1, anchor='crank', crank=2, b=-.3, mark='wrr'),
         k(.66, contact=1, anchor='crank', crank=3, b=.3), k(.86, w=.4, eye='^')],
        [(.3, 'crank'), (.66, 'crank')], when=['charge<.8'], ages=GROWN, tool='wing')
routine('weather_make_cloud', 'weather_machine', 'Pulling the big lever to puff out a tiny private cloud', 22,
        [k(.12, reach=1, contact=1, anchor='lever', lever=0, w=.6), k(.3, y=.5, b=.5, contact=1, anchor='lever', lever=1, mark='CHUNK'), k(.45, x=-.7, y=-.6, eye='O', mark='!'),
         k(.65, y=-.8, w=1, eye='^', mark='~'), k(.88, eye='^')],
        [(.3, 'fire')], when=['charge>.35'], prefer=['warm', 'sun'], ages=GROWN, tool='wing', say='weather_cloud')
routine('weather_catch_spark', 'weather_machine', 'Touching the charged terminal in the rain and getting a static zap', 16,
        [k(.15, x=.6, reach=.8, eye='o'), k(.32, contact=1, anchor='terminal', mark='zt'), k(.42, x=-.9, b=-.6, w=1, eye='@', mark='ZAP'), k(.65, eye='@', mark='~'), k(.88, eye='>')],
        [(.32, 'zap')], when=['wet', 'charge>.6'], prefer=['curious'], ages=GROWN, tool='wing', say='weather_zap')
routine('weather_vent_steam', 'weather_machine', 'Opening the vent to let a muggy cloud drift off', 16,
        [k(.15, reach=.7, contact=1, anchor='vent'), k(.4, contact=1, anchor='vent', mark='fsss'), k(.65, x=-.6, w=.6, mark='~'), k(.88, eye='^')],
        [(.4, 'vent')], when=['cloud>.2'], tool='wing')

# --------------------------------------------------------------------------- space and spectacle
item('portal', 'portal', 140, 132, 0.384, 'stone', 'engineering', 'Dial',
     dict(energy=(0, 0, 1), rune=(0, 0, 5), stability=(1, 0, 1), sent=(0, 0, 9999), swirl=(0, 0, 1)),
     physics=[('energy', 'rate', -.0011, 'always'), ('swirl', 'wrap', .01, 'energized'), ('stability', 'rate', -.002, 'storm&energized'), ('stability', 'rate', .001, 'calm')],
     triggers=[('stability<=.05', [['energy', 'set', 0], ['stability', 'set', .5]])],
     effects=dict(rune=[['rune', 'wrap', 1], ['energy', 'add', .25]], toss=[['sent', 'add', 1]], brace=[['stability', 'add', .3]], spark=[['energy', 'set', 1]],
                  close=[['energy', 'set', 0]]),
     parts=['pebble', 'peek'])
routine('portal_dial_runes', 'portal', 'Pressing the glowing runes on the console in order', 26,
        [k(.12, reach=.8, contact=1, anchor='console_l', mark='1'), k(.3, x=.4, y=-.5, w=.6, contact=1, anchor='console_c', mark='2'), k(.48, x=.9, contact=1, anchor='console_r', mark='3'),
         k(.66, x=-.5, eye='O', mark='!!'), k(.86, eye='^')],
        [(.12, 'rune'), (.3, 'rune'), (.48, 'spark')], when=['!storm'], ages=GROWN, tool='wing')
routine('portal_peek_through', 'portal', 'Poking his head into the low edge of the swirl and pulling back amazed', 22,
        [k(.12, x=.6, eye='o', mark='?'), k(.3, x=1.2, y=-.2, contact=1, anchor='swirl_low', peek=1, eye='O'), k(.48, x=1.2, peek=1, mark='...'), k(.6, x=-.8, b=-.5, w=1, peek=0, eye='@', mark='!!'),
         k(.85, eye='^', mark='?!')],
        [], when=['energy>.4'], tool='none', say='portal_peek')
routine('portal_toss_pebble', 'portal', 'Tossing a pebble in and watching for it to come back', 24,
        [k(.12, y=1, b=.6, reach=.3, pebble=1), k(.28, x=-.4, w=1, pebble=1, eye='>'), k(.38, x=.6, w=.4, pebble=0, mark='toss'), k(.55, x=-.2, eye='o', mark='...'),
         k(.7, y=-.5, eye='O', mark='!'), k(.88, eye='^')],
        [(.38, 'toss')], when=['energy>.4'], prefer=['curious', 'young'], tool='none')
routine('portal_brace_ring', 'portal', 'Bracing the shuddering ring with both wings', 20,
        [k(.15, x=.7, w=1, reach=1, contact=1, anchor='ring_l'), k(.35, x=.9, b=.5, w=1, contact=1, anchor='ring_l', mark='hng'), k(.6, b=.3, contact=1, anchor='ring_l', mark='!'), k(.85, w=.3, eye='^')],
        [(.35, 'brace'), (.6, 'brace')], when=['stability<.7', 'energy>.2'], ages=GROWN, tool='wing')
routine('portal_close_down', 'portal', 'Sweeping a wing across the console runes to close the swirl', 16,
        [k(.15, reach=.8, contact=1, anchor='console_r', w=.6), k(.4, x=-.3, contact=1, anchor='console_l', w=1, mark='fwip'), k(.7, eye='^')],
        [(.4, 'close')], when=['energy>.3'], prefer=['night_late', 'storm'], tool='wing')

item('wormhole', 'wormhole', 132, 120, 0.338, 'void', 'engineering', 'Align',
     dict(aperture=(0, 0, 1), align=(.5, 0, 1), echoes=(0, 0, 9999), boats=(0, 0, 9999), spin=(0, 0, 1)),
     physics=[('spin', 'wrap', .008, 'open'), ('aperture', 'rate', -.0005, 'always'), ('align', 'rate', -.0008, 'windy')],
     effects=dict(open=[['aperture', 'set', 1]], align=[['align', 'add', .25]], whisper=[['echoes', 'add', 1]], boat=[['boats', 'add', 1]], shut=[['aperture', 'set', 0]]),
     parts=['boat', 'cup'])
routine('wormhole_peep_echo', 'wormhole', 'Peeping at the near mouth and hearing it peep back from the far one', 18,
        [k(.15, x=.4, y=-.3, eye='o', mark='peep'), k(.35, x=.2, eye='-', mark='...'), k(.5, x=-.4, y=-.5, eye='O', mark='peep?'), k(.7, b=-.5, w=1, eye='^', mark='!!'), k(.88, eye='^')],
        [], when=['aperture>.5'], ages=YOUNG + ['juvenile'], prefer=['young', 'lonely'], tool='none', say='wormhole_whisper')
routine('wormhole_iris_open', 'wormhole', 'Twisting the brass iris until both mouths yawn open', 18,
        [k(.15, reach=.8, contact=1, anchor='iris'), k(.4, contact=1, anchor='iris', b=.3, mark='krrk'), k(.6, x=-.6, y=-.5, eye='O', mark='!'), k(.85, eye='^')],
        [(.4, 'open')], when=['aperture<.4'], tool='wing')
routine('wormhole_align_mouths', 'wormhole', 'Turning the alignment knob while sighting along both mouths', 22,
        [k(.15, x=-.4, eye='o'), k(.3, reach=.8, contact=1, anchor='align_knob', mark='<'), k(.5, x=.8, contact=1, anchor='align_knob', mark='>'), k(.7, x=.2, eye='-', mark='..'), k(.88, eye='^')],
        [(.3, 'align'), (.5, 'align')], when=['aperture>.3'], ages=GROWN, tool='wing')
routine('wormhole_whisper', 'wormhole', 'Whispering into one mouth and hearing it come out the other', 20,
        [k(.15, x=.8, y=.2, contact=1, anchor='near', cup=1, mark='psst'), k(.35, x=.8, mark='...'), k(.5, x=-.6, eye='O', mark='?'), k(.65, x=1, y=.3, contact=1, anchor='far', cup=1, eye='o'),
         k(.85, eye='^', mark='!')],
        [(.15, 'whisper')], when=['aperture>.5'], prefer=['lonely', 'young'], tool='none', say='wormhole_whisper')
routine('wormhole_paper_boat', 'wormhole', 'Floating a paper boat through the wormhole', 24,
        [k(.12, y=.8, b=.5, boat=1), k(.3, x=.6, reach=.6, contact=1, anchor='near', boat=1, mark='~'), k(.45, x=.6, boat=0, mark='bye'), k(.62, x=1.1, eye='o', mark='...'),
         k(.78, x=1.1, contact=1, anchor='far', boat=1, eye='O', mark='!'), k(.9, eye='^')],
        [(.45, 'boat')], when=['aperture>.5'], prefer=['happy', 'wet'], tool='none')
routine('wormhole_shut', 'wormhole', 'Twisting the iris shut', 14,
        [k(.2, reach=.8, contact=1, anchor='iris'), k(.45, contact=1, anchor='iris', mark='krrk'), k(.8, eye='^')],
        [(.45, 'shut')], when=['aperture>.3'], tool='wing')

item('black_hole', 'blackhole', 112, 116, 0.321, 'void', 'engineering', 'Observe',
     dict(mass=(.3, 0, 1), containment=(1, 0, 1), spin=(0, 0, 1), fed=(0, 0, 9999), hum=(0, 0, 1)),
     physics=[('spin', 'wrap', .012, 'always'), ('containment', 'rate', -.0001, 'always'), ('containment', 'rate', -.0006, 'storm'), ('hum', 'decay', 0, 'always'),
              ('mass', 'rate', .00015, 'fall')],
     triggers=[('containment<=.15', [['hum', 'set', 1], ['containment', 'set', .3]])],
     effects=dict(feed=[['mass', 'add', .06], ['fed', 'add', 1], ['hum', 'set', .6]], tighten=[['containment', 'add', .35]], gauge=[], tap=[['hum', 'set', .4]]),
     parts=['leaf', 'wrench', 'goggles'])
routine('blackhole_feed_leaf', 'black_hole', "Dropping a fallen leaf into the tiny black hole's intake port", 20,
        [k(.12, y=1, b=.6, reach=.3, leaf=1), k(.3, x=.6, reach=.7, contact=1, anchor='port', leaf=1, eye='o'), k(.42, x=.6, leaf=0, mark='fwoop'), k(.6, x=-.6, b=-.4, eye='O', mark='!'),
         k(.85, eye='^', mark='burp?')],
        [(.42, 'feed')], prefer=['fall', 'curious'], tool='none', say='blackhole_feed')
routine('blackhole_tighten_ring', 'black_hole', 'Tightening the containment ring bolts', 24,
        [k(.12, reach=.7, contact=1, anchor='bolt_l', wrench=1), k(.3, contact=1, anchor='bolt_l', wrench=1, b=.3, mark='crk'), k(.5, x=.6, contact=1, anchor='bolt_r', wrench=1),
         k(.66, contact=1, anchor='bolt_r', wrench=1, b=.3, mark='crk'), k(.86, wrench=0, eye='^')],
        [(.3, 'tighten'), (.66, 'tighten')], when=['containment<.8'], prefer=['containment<.4', 'storm'], ages=GROWN, tool='wrench')
routine('blackhole_read_gauge', 'black_hole', 'Squinting at the event-horizon gauge through goggles', 20,
        [k(.15, goggles=1, eye='o'), k(.35, x=.6, y=.2, contact=1, anchor='gauge', goggles=1, eye='o', mark='hm'), k(.6, x=.6, goggles=1, mark='...'), k(.85, goggles=0, eye='^')],
        [(.35, 'gauge')], tool='none', say='blackhole_gauge')
routine('blackhole_stare', 'black_hole', 'Staring into the void until the void stares back', 22,
        [k(.15, x=.6, y=.3, eye='o'), k(.35, x=.9, y=.4, eye='O'), k(.55, x=.9, y=.4, eye='@', mark='...'), k(.7, x=-.7, b=-.5, w=1, eye='>', mark='nope'), k(.88, eye='^')],
        [], prefer=['night', 'sad'], tool='none', say='blackhole_stare')
routine('blackhole_flick', 'black_hole', 'Flicking the glass to see if it does anything', 14,
        [k(.15, reach=.8, contact=0, eye='o'), k(.32, contact=1, anchor='glass_low', mark='tink'), k(.5, x=-.5, eye='O', mark='!'), k(.8, eye='^', mark='?')],
        [(.32, 'tap')], ages=YOUNG + ['juvenile'], prefer=['young'], tool='wing')

item('volcano', 'volcano', 144, 120, 0.366, 'stone', 'engineering', 'Tend',
     dict(pressure=(.2, 0, 1), eruption=(0, 0, 1), ash=(0, 0, 1), warmth=(.5, 0, 1), eruptions=(0, 0, 9999)),
     physics=[('pressure', 'rate', .0007, 'always'), ('pressure', 'rate', -.0012, 'wet'), ('eruption', 'decay', 0, 'always'), ('warmth', 'decay', 1, 'always'),
              ('warmth', 'rate', -.003, 'wet')],
     triggers=[('pressure>=1', [['eruption', 'set', 1], ['pressure', 'set', .1], ['ash', 'add', .4], ['eruptions', 'add', 1]])],
     effects=dict(vent=[['pressure', 'add', -.35]], stir=[['warmth', 'add', .2]], sweep=[['ash', 'mul', .3]], fizz=[['pressure', 'set', 1]], toast=[['warmth', 'add', .05]]),
     parts=['valve', 'broom', 'jug'], shelter=False)
routine('volcano_bleed_valve', 'volcano', 'Turning the pressure valve until it hisses', 22,
        [k(.12, reach=.7, contact=1, anchor='valve', valve=0), k(.32, contact=1, anchor='valve', valve=1, b=.3, mark='hsss'), k(.5, x=-.6, w=.6, eye='o', mark='~'), k(.7, contact=1, anchor='valve', valve=0),
         k(.88, eye='^')],
        [(.32, 'vent')], when=['pressure>.5'], prefer=['pressure>.8'], ages=GROWN, tool='wing')
routine('volcano_baking_soda', 'volcano', 'Pouring fizz into the hopper at the base and running', 22,
        [k(.12, reach=.8, contact=1, anchor='hopper', jug=1, eye='>'), k(.28, y=-.5, contact=1, anchor='hopper', jug=1, mark='glug'), k(.38, x=-1.1, l=1, r=1, jug=0, eye='O', mark='RUN'),
         k(.55, x=-1.2, b=-.5, w=1, eye='^', mark='!!!'), k(.8, x=-.6, eye='^', mark='hah')],
        [(.28, 'fizz')], when=['!wet', 'pressure<.9'], prefer=['happy', 'young'], tool='jug', say='volcano_fizz')
routine('volcano_sweep_ash', 'volcano', 'Sweeping grey ash off the slopes', 22,
        [k(.15, reach=.7, contact=1, anchor='slope_l', broom=1), k(.35, x=.4, contact=1, anchor='base', broom=1, mark='~'), k(.55, x=.9, contact=1, anchor='slope_r', broom=1),
         k(.8, broom=0, eye='^')],
        [(.35, 'sweep'), (.55, 'sweep')], when=['ash>.2'], tool='broom')
routine('volcano_warm_wings', 'volcano', 'Warming cold wings by the glowing vents', 30,
        [k(.12, x=.5, y=.4, b=.5, w=.6, eye='-'), k(.3, x=.6, y=.6, b=.7, w=1, eye='-', mark='ahh'), k(.6, x=.6, y=.6, b=.7, w=1, eye='-'), k(.82, y=.3, w=.4, eye='^')],
        [], when=['cold'], prefer=['winter', 'tired', 'wet'], tool='none', say='volcano_warm')
routine('volcano_stir_magma', 'volcano', 'Stirring the glowing side vent with an iron rod', 22,
        [k(.12, y=-.5, reach=1, contact=1, anchor='vent_low', w=.8), k(.32, contact=1, anchor='vent_low', b=-.3, mark='~'), k(.52, x=.3, contact=1, anchor='vent_low', b=.3, mark='~'), k(.75, eye='^')],
        [(.32, 'stir'), (.52, 'stir')], when=['!wet'], ages=GROWN, tool='wing')
routine('volcano_watch_eruption', 'volcano', 'Watching the little volcano erupt from a safe distance', 22,
        [k(.12, x=-.7, eye='O', mark='!'), k(.3, x=-.9, b=-.4, w=1, eye='O', mark='!!'), k(.55, x=-.8, eye='^', mark='woo'), k(.8, eye='^')],
        [], when=['eruption>.3'], tool='none')

item('tornado', 'tornado', 104, 124, 0.259, 'wind', 'discovery', 'Play',
     dict(spin=(.4, 0, 1), size=(.4, 0, 1), mood=(.6, 0, 1), debris=(0, 0, 1), covered=(0, 0, 1)),
     physics=[('size', 'decay', .3, 'calm'), ('size', 'rate', .002, 'windy'), ('spin', 'decay', .4, 'always'), ('mood', 'rate', -.0004, 'always'),
              ('debris', 'rate', .0006, 'fall&!covered'), ('spin', 'decay', .05, 'covered')],
     effects=dict(feed=[['debris', 'add', .3], ['mood', 'add', .2], ['spin', 'add', .2]], pat=[['mood', 'add', .25], ['spin', 'add', .15]], hush=[['spin', 'mul', .4], ['size', 'mul', .7]],
                  throw=[['spin', 'add', .3], ['mood', 'add', .15]], cover=[['covered', 'set', 1]], uncover=[['covered', 'set', 0], ['spin', 'max', .3]],
                  spit=[['debris', 'mul', .4]]),
     parts=['leaf', 'cloth'])
routine('tornado_feed_leaves', 'tornado', 'Feeding a wing-full of leaves to the little tornado', 20,
        [k(.12, y=1, b=.6, leaf=1), k(.3, x=.6, reach=.6, contact=1, anchor='funnel', leaf=1, eye='o'), k(.42, leaf=0, mark='whoosh'), k(.6, x=-.4, eye='^', mark='!'), k(.85, eye='^')],
        [(.42, 'feed')], when=['!covered'], prefer=['fall', 'windy'], tool='none')
routine('tornado_pat', 'tornado', 'Patting the tornado and getting his feathers swirled', 18,
        [k(.15, x=.6, reach=.8, contact=1, anchor='funnel', eye='^'), k(.35, contact=1, anchor='funnel', b=-.3, mark='fwip'), k(.5, x=-.3, w=1, eye='@', mark='~'), k(.75, w=.3, eye='^', mark='<3')],
        [(.35, 'pat')], when=['!covered'], prefer=['lonely', 'happy'], tool='wing', say='tornado_pat')
routine('tornado_fetch', 'tornado', 'Throwing a pinecone and letting the tornado spit it back', 26,
        [k(.12, x=-.5, w=1, leaf=1, eye='>'), k(.24, x=.6, w=.4, leaf=0, mark='go!'), k(.42, x=.2, eye='o', mark='...'), k(.55, x=-.6, y=-.4, eye='O', mark='!'), k(.68, y=.6, b=.4, leaf=1, mark='got it'),
         k(.88, eye='^')],
        [(.24, 'throw'), (.55, 'spit')], when=['!covered', 'dry'], prefer=['young', 'happy'], tool='none')
routine('tornado_calm', 'tornado', 'Humming the tornado down when the real wind picks up', 22,
        [k(.15, x=.4, w=.6, eye='-', mark='~'), k(.35, x=.6, w=.8, contact=1, anchor='funnel', eye='-', mark='shh'), k(.6, w=.5, eye='-', mark='~'), k(.85, eye='^')],
        [(.35, 'hush'), (.6, 'hush')], when=['size>.55'], prefer=['windy', 'storm'], tool='wing')
routine('tornado_tuck_in', 'tornado', 'Draping a cloth over the jar so the tornado can sleep', 18,
        [k(.15, reach=1, w=.8, contact=1, anchor='lid', cloth=1), k(.42, y=-.5, contact=1, anchor='lid', cloth=1, mark='night'), k(.7, eye='-', mark='z'), k(.88, eye='^')],
        [(.42, 'cover')], when=['!covered', 'night'], tool='cloth', say='tornado_night')
routine('tornado_wake', 'tornado', 'Lifting the cloth so the tornado can spin in the morning', 14,
        [k(.15, reach=1, contact=1, anchor='lid', cloth=1), k(.42, y=-.6, w=1, cloth=0, mark='morning!'), k(.8, eye='^')],
        [(.42, 'uncover')], when=['covered', 'day'], tool='cloth')

item('antigravity', 'antigravity', 124, 120, 0.31, 'metal', 'engineering', 'Calibrate',
     dict(field=(0, 0, 1), rings=(.5, 0, 1), floaters=(3, 0, 6), drift=(0, 0, 1)),
     physics=[('field', 'rate', -.0008, 'always'), ('drift', 'wrap', .006, 'fielded'), ('rings', 'rate', -.0005, 'windy')],
     effects=dict(power=[['field', 'set', 1]], float=[['floaters', 'add', 1]], calibrate=[['rings', 'add', .3]], ground=[['floaters', 'set', 0]], off=[['field', 'set', 0]]),
     parts=['pebble', 'feather'])
routine('antigrav_power_up', 'antigravity', 'Powering up the anti-gravity plate', 16,
        [k(.15, reach=.7, contact=1, anchor='switch'), k(.4, contact=1, anchor='switch', mark='vmmm'), k(.6, y=-.3, eye='O', mark='!'), k(.85, eye='^')],
        [(.4, 'power')], when=['field<.5'], tool='wing')
routine('antigrav_float_pebbles', 'antigravity', 'Setting pebbles on the plate and watching them rise', 22,
        [k(.12, y=1, b=.6, pebble=1), k(.3, x=.6, reach=.6, contact=1, anchor='plate', pebble=1), k(.42, pebble=0, mark='up..'), k(.6, y=-.6, eye='O', mark='!'), k(.85, eye='^')],
        [(.42, 'float')], when=['field>.4'], tool='none')
routine('antigrav_feather_lift', 'antigravity', 'Leaning into the field until his feathers stand on end', 20,
        [k(.15, x=.7, y=-.2, w=.4, eye='o'), k(.35, x=1, y=-.6, w=1, b=-.6, eye='O', mark='!!'), k(.55, x=1, y=-.8, w=1, b=-.8, eye='^', mark='wheee'), k(.75, x=.2, w=.3, eye='^'),
         k(.9, eye='^')],
        [], when=['field>.6'], prefer=['young', 'happy'], tool='none', say='antigrav_float')
routine('antigrav_calibrate', 'antigravity', 'Twisting the lowest floating ring back into line', 24,
        [k(.15, y=-.5, reach=1, contact=1, anchor='ring_low', w=.6), k(.35, contact=1, anchor='ring_low', mark='clk'), k(.55, x=.5, contact=1, anchor='ring_low', mark='clk'), k(.8, eye='^')],
        [(.35, 'calibrate'), (.55, 'calibrate')], when=['rings<.7'], ages=GROWN, tool='wing')
routine('antigrav_power_down', 'antigravity', 'Catching the floating pebbles as the plate powers down', 18,
        [k(.15, reach=.7, contact=1, anchor='switch'), k(.3, contact=1, anchor='switch', mark='vmm..'), k(.45, x=.6, y=-.4, w=1, eye='O', mark='!'), k(.65, y=.6, b=.5, mark='catch'), k(.85, eye='^')],
        [(.3, 'off'), (.45, 'ground')], when=['field>.4'], tool='wing')

item('force_field', 'forcefield', 148, 120, 0.366, 'energy', 'engineering', 'Shelter',
     dict(shield=(0, 0, 1), charge=(.6, 0, 1), hits=(0, 0, 9999), ripple=(0, 0, 1)),
     physics=[('charge', 'rate', -.0018, 'shielded&wet'), ('charge', 'rate', -.0004, 'shielded'), ('charge', 'rate', .0006, 'sun&!shielded'), ('ripple', 'decay', 0, 'always'),
              ('ripple', 'decay', .6, 'shielded&wet')],
     triggers=[('charge<=.02&shield>.1', [['shield', 'set', 0]])],
     effects=dict(raise_=[['shield', 'set', 1]], lower=[['shield', 'set', 0]], charge=[['charge', 'add', .3]], boop=[['ripple', 'set', 1]], shelter=[['hits', 'add', 1]]),
     parts=['crank'], shelter=True)
routine('field_raise_dome', 'force_field', 'Raising the shimmering dome', 16,
        [k(.15, reach=.7, contact=1, anchor='switch'), k(.4, contact=1, anchor='switch', mark='VWOOM'), k(.6, y=-.6, w=.8, eye='O'), k(.85, eye='^')],
        [(.4, 'raise_')], when=['shield<.5', 'charge>.15'], prefer=['wet'], tool='wing')
routine('field_rain_shelter', 'force_field', 'Sitting snug under the dome while rain bounces off', 42,
        [k(.12, x=.6, y=.6, b=.5, eye='o'), k(.25, y=1, b=.8, eye='^', mark='hah'), k(.45, y=1, b=.8, eye='-', mark='~'), k(.65, y=1, b=.8, eye='o', mark='plink'), k(.88, y=.4, eye='^')],
        [(.45, 'shelter')], when=['wet', 'shield>.5'], prefer=['young', 'tired', 'wet'], tool='none', say='field_shelter')
routine('field_wind_charger', 'force_field', 'Cranking the emitter to charge it back up', 24,
        [k(.12, reach=.7, contact=1, anchor='crank', crank=0), k(.32, contact=1, anchor='crank', crank=1, mark='wrr'), k(.52, contact=1, anchor='crank', crank=2, b=.3, mark='wrr'), k(.8, eye='^')],
        [(.32, 'charge'), (.52, 'charge')], when=['charge<.7'], ages=GROWN, tool='wing')
routine('field_boop', 'force_field', 'Booping the dome and watching the ripple run round', 14,
        [k(.15, x=.6, reach=.8, eye='o'), k(.32, contact=1, anchor='dome', mark='boop'), k(.5, x=-.3, y=-.5, eye='O', mark='~'), k(.8, eye='^')],
        [(.32, 'boop')], when=['shield>.5'], prefer=['young', 'happy'], tool='wing')
routine('field_lower_dome', 'force_field', 'Lowering the dome once the weather clears', 14,
        [k(.2, reach=.7, contact=1, anchor='switch'), k(.45, contact=1, anchor='switch', mark='vwm..'), k(.8, eye='^')],
        [(.45, 'lower')], when=['shield>.5', 'dry'], tool='wing')

item('cosmic_arch', 'arch', 150, 132, 0.41, 'stone', 'observation', 'Align',
     dict(align=(0, 0, 1), starlight=(0, 0, 1), traced=(0, 0, 7), moss=(.2, 0, 1)),
     physics=[('starlight', 'decay', 1, 'night&clear'), ('starlight', 'decay', 0, '!night'), ('starlight', 'decay', .2, 'night&!clear'), ('moss', 'rate', .0002, 'wet'),
              ('align', 'rate', -.0002, 'always')],
     effects=dict(turn=[['align', 'add', .25]], trace=[['traced', 'wrap', 1]], scrub=[['moss', 'mul', .4]], wish=[]),
     parts=['brush'])
routine('arch_turn_starwheel', 'cosmic_arch', 'Turning the low star dial until the keystone wheel lines up', 26,
        [k(.12, y=-.4, reach=1, contact=1, anchor='dial_low', w=.7), k(.3, contact=1, anchor='dial_low', b=.3, mark='grnd'), k(.5, contact=1, anchor='dial_low', b=-.2, mark='grnd'), k(.7, x=-.5, y=-.6, eye='O'),
         k(.88, eye='^')],
        [(.3, 'turn'), (.5, 'turn')], when=['align<.8'], prefer=['dusk', 'night'], ages=GROWN, tool='wing')
routine('arch_trace_constellation', 'cosmic_arch', 'Tracing the little constellation carved low on the pillar', 24,
        [k(.12, y=-.5, reach=1, contact=1, anchor='stars_low_a', mark='.'), k(.3, x=.3, y=-.7, contact=1, anchor='stars_low_b', mark='.'), k(.5, x=.7, y=-.5, contact=1, anchor='stars_low_c', mark='*'),
         k(.75, x=-.3, eye='^', mark='?'), k(.9, eye='^')],
        [(.5, 'trace')], when=['starlight>.3'], prefer=['night', 'curious'], tool='wing', say='arch_trace')
routine('arch_sit_beneath', 'cosmic_arch', 'Sitting under the arch and counting stars', 36,
        [k(.12, x=.4, y=.8, b=.6, eye='o'), k(.3, y=.8, b=.6, x=-.2, eye='o', mark='1'), k(.5, y=.8, b=.6, eye='o', mark='2'), k(.7, y=.8, b=.6, eye='-', mark='...'), k(.9, eye='^')],
        [], when=['night', 'dry'], prefer=['lonely', 'sad', 'elder'], tool='none', say='arch_stars')
routine('arch_scrub_moss', 'cosmic_arch', 'Scrubbing moss out of the carved stars', 22,
        [k(.15, reach=.8, contact=1, anchor='pillar_l', brush=1), k(.35, y=-.4, contact=1, anchor='pillar_l', brush=1, mark='scrb'), k(.55, x=.8, contact=1, anchor='pillar_r', brush=1, mark='scrb'),
         k(.8, brush=0, eye='^')],
        [(.35, 'scrub'), (.55, 'scrub')], when=['moss>.3'], tool='brush')
routine('arch_make_wish', 'cosmic_arch', 'Closing his eyes under the keystone and making a wish', 18,
        [k(.15, x=.4, y=-.3, w=.4, eye='-'), k(.4, y=-.5, w=.8, eye='-', mark='...'), k(.65, y=-.3, w=.4, eye='-'), k(.85, eye='^', mark='*')],
        [(.4, 'wish')], when=['starlight>.5'], prefer=['night', 'sad'], tool='none', say='arch_wish')

# --------------------------------------------------------------------------- doors and machines
item('time_machine', 'timemachine', 132, 136, 0.361, 'brass', 'engineering', 'Travel',
     dict(year=(2026, 1, 9999), charge=(.2, 0, 1), flux=(0, 0, 1), door=(0, 0, 1), shine=(.5, 0, 1), trips=(0, 0, 9999)),
     physics=[('flux', 'decay', 0, 'always'), ('charge', 'rate', .0003, 'always'), ('shine', 'rate', -.0004, 'wet')],
     effects=dict(year_up=[['year', 'add', 1]], year_back=[['year', 'add', -10]], year_far=[['year', 'add', -100]], wind=[['charge', 'add', .3]],
                  lever=[['flux', 'set', 1], ['charge', 'add', -.5], ['trips', 'add', 1]], door_open=[['door', 'set', 1]], door_shut=[['door', 'set', 0]],
                  polish=[['shine', 'add', .35]], home=[['year', 'set', 2026]]),
     parts=['lever', 'key', 'cloth'], shelter=True)
routine('time_set_year', 'time_machine', "Rolling the console's year knob back to a different century", 22,
        [k(.12, reach=.8, contact=1, anchor='year_knob', eye='o'), k(.3, contact=1, anchor='year_knob', mark='tk-tk'), k(.48, contact=1, anchor='year_knob', mark='tk-tk'), k(.66, x=-.4, eye='O', mark='?'),
         k(.86, eye='^')],
        [(.3, 'year_back'), (.48, 'year_far')], ages=GROWN, tool='wing', say='time_year')
routine('time_wind_key', 'time_machine', 'Winding the big clockwork key on the side', 24,
        [k(.12, reach=.8, contact=1, anchor='key', key=0), k(.3, contact=1, anchor='key', key=1, b=.3, mark='crk'), k(.48, contact=1, anchor='key', key=2, b=-.2, mark='crk'), k(.66, contact=1, anchor='key', key=3),
         k(.86, eye='^')],
        [(.3, 'wind'), (.66, 'wind')], when=['charge<.8'], ages=GROWN, tool='wing')
routine('time_pull_lever', 'time_machine', 'Stepping in, pulling the lever, and stepping out a second later', 30,
        [k(.1, reach=.6, contact=1, anchor='door', door=1), k(.22, x=.6, contact=1, anchor='lever', door=1, eye='>'), k(.32, contact=1, anchor='lever', lever=1, door=0, mark='KA-CHUNK'),
         k(.48, door=0, lever=1, eye='@', mark='~~~'), k(.62, door=1, lever=0, x=-.6, eye='@', mark='...'), k(.78, door=1, eye='O', mark='!'), k(.9, door=0, eye='^')],
        [(.1, 'door_open'), (.32, 'lever'), (.62, 'door_open'), (.9, 'door_shut')], when=['charge>.45'], ages=GROWN, tool='wing', say='time_trip')
routine('time_polish_brass', 'time_machine', 'Polishing the brass kick plates and door rim', 24,
        [k(.15, reach=.7, contact=1, anchor='brass_low', cloth=1), k(.35, contact=1, anchor='door', cloth=1, mark='*'), k(.55, x=.5, contact=1, anchor='brass_low_r', cloth=1), k(.8, cloth=0, eye='^')],
        [(.35, 'polish'), (.55, 'polish')], prefer=['shine<.5'], tool='cloth')
routine('time_rain_booth', 'time_machine', 'Ducking into the time booth until the rain eases', 40,
        [k(.1, reach=.6, contact=1, anchor='door', door=1), k(.22, x=.8, door=1, eye='o'), k(.35, x=.9, door=.3, eye='^', mark='dry'), k(.7, x=.9, door=.3, eye='-', mark='~'), k(.85, x=.2, door=1, eye='^'),
         k(.95, door=0)],
        [(.1, 'door_open'), (.95, 'door_shut')], when=['wet'], prefer=['young', 'tired'], tool='wing')
routine('time_back_to_now', 'time_machine', 'Setting the year knob back to the present', 16,
        [k(.15, reach=.8, contact=1, anchor='year_knob'), k(.4, contact=1, anchor='year_knob', mark='tk-tk-tk'), k(.7, eye='^', mark='now')],
        [(.4, 'home')], when=['far_year'], tool='wing')

item('tardis', 'booth', 104, 136, 0.361, 'wood', 'observation', 'Visit',
     dict(door=(0, 0, 1), lamp=(0, 0, 1), dust=(.2, 0, 1), knocks=(0, 0, 9999), whoosh=(0, 0, 1)),
     physics=[('lamp', 'decay', 0, 'always'), ('whoosh', 'decay', 0, 'always'), ('dust', 'rate', .0003, 'dry'), ('dust', 'rate', -.001, 'wet')],
     effects=dict(open=[['door', 'set', 1]], shut=[['door', 'set', 0]], knock=[['knocks', 'add', 1], ['lamp', 'set', .6]], lamp=[['lamp', 'set', 1], ['whoosh', 'set', 1]],
                  dust=[['dust', 'mul', .3]]),
     parts=['cloth'], shelter=True)
routine('booth_peek_inside', 'tardis', 'Opening the door and gaping at how big it is inside', 22,
        [k(.12, reach=.6, contact=1, anchor='handle', door=0), k(.25, contact=1, anchor='handle', door=1, mark='creak'), k(.4, x=.6, y=-.3, door=1, eye='O', mark='!!'), k(.6, x=-.6, door=1, eye='@', mark='?!'),
         k(.8, reach=.6, contact=1, anchor='handle', door=0), k(.92, eye='^')],
        [(.25, 'open'), (.8, 'shut')], tool='wing', say='booth_inside')
routine('booth_knock', 'tardis', 'Knocking on the blue door to see if anybody answers', 18,
        [k(.15, reach=.7, contact=1, anchor='door', mark='knock'), k(.3, contact=1, anchor='door', mark='knock'), k(.5, x=-.3, eye='o', mark='...'), k(.7, y=-.4, eye='O', mark='!'), k(.88, eye='^')],
        [(.15, 'knock'), (.3, 'knock')], prefer=['lonely', 'young'], tool='wing', say='booth_knock')
routine('booth_lamp_whoosh', 'tardis', 'Pulling the side chain and hearing a wheezing whoosh from the roof lamp', 18,
        [k(.15, y=-.6, reach=1, w=.9, contact=1, anchor='chain'), k(.35, y=-.8, contact=1, anchor='chain', mark='vworp'), k(.55, x=-.6, eye='O', mark='~'), k(.85, eye='^')],
        [(.35, 'lamp')], ages=GROWN, tool='wing')
routine('booth_dust_panels', 'tardis', 'Dusting the lower blue panels', 22,
        [k(.15, y=-.5, reach=.9, contact=1, anchor='panel_low', cloth=1), k(.35, contact=1, anchor='door', cloth=1, mark='~'), k(.55, y=.5, contact=1, anchor='base', cloth=1), k(.8, cloth=0, eye='^')],
        [(.35, 'dust'), (.55, 'dust')], when=['dust>.3'], tool='cloth')
routine('booth_storm_hideout', 'tardis', 'Hiding inside the booth while the storm grumbles', 44,
        [k(.1, reach=.6, contact=1, anchor='handle', door=1), k(.22, x=.8, door=1), k(.32, x=.9, door=.15, eye='o', mark='safe'), k(.7, x=.9, door=.15, eye='-'), k(.86, x=.2, door=1, eye='^'), k(.95, door=0)],
        [(.1, 'open'), (.95, 'shut')], when=['wet'], prefer=['storm', 'young'], tool='wing')

item('dimensional_door', 'dimdoor', 112, 132, 0.333, 'wood', 'observation', 'Open',
     dict(door=(0, 0, 1), dimension=(0, 0, 4), draft=(0, 0, 1), hinge=(.6, 0, 1)),
     physics=[('draft', 'decay', 0, 'always'), ('hinge', 'rate', -.0004, 'wet')],
     effects=dict(open=[['door', 'set', 1], ['draft', 'set', 1]], shut=[['door', 'set', 0]], knob=[['dimension', 'wrap', 1]], oil=[['hinge', 'add', .4]], knock=[]),
     parts=['can'])
routine('dimdoor_sniff_sill', 'dimensional_door', 'Sniffing the strange draught under the door', 18,
        [k(.15, x=.5, y=.6, b=.5, eye='o'), k(.32, x=.8, y=1, b=.8, contact=1, anchor='sill', mark='snf'), k(.5, x=.8, y=1, eye='O', mark='?!'), k(.7, x=-.5, b=-.4, eye='^', mark='brr'),
         k(.88, eye='^')],
        [], ages=YOUNG + ['juvenile'], prefer=['young', 'curious'], tool='none')
routine('dimdoor_open_peek', 'dimensional_door', 'Opening the door onto somewhere else entirely', 22,
        [k(.12, reach=.6, contact=1, anchor='knob'), k(.28, contact=1, anchor='knob', door=1, mark='creak'), k(.45, x=.5, door=1, eye='O', mark='!'), k(.62, x=-.6, b=-.4, door=1, w=1, eye='@', mark='woah'),
         k(.8, contact=1, anchor='knob', door=0), k(.92, eye='^')],
        [(.28, 'open'), (.8, 'shut')], tool='wing', say='dimdoor_peek')
routine('dimdoor_turn_knob', 'dimensional_door', 'Twisting the knob to a new dimension', 16,
        [k(.15, reach=.6, contact=1, anchor='knob'), k(.4, contact=1, anchor='knob', b=.3, mark='clk'), k(.6, x=-.3, eye='o', mark='?'), k(.85, eye='^')],
        [(.4, 'knob')], ages=GROWN, tool='wing')
routine('dimdoor_oil_hinges', 'dimensional_door', 'Oiling the squeaky hinges', 18,
        [k(.15, reach=.7, contact=1, anchor='hinge_mid', can=1), k(.35, contact=1, anchor='hinge_mid', can=1, mark='drip'), k(.55, y=.6, contact=1, anchor='hinge_low', can=1, mark='drip'),
         k(.8, can=0, eye='^')],
        [(.35, 'oil'), (.55, 'oil')], when=['hinge<.6'], ages=GROWN, tool='can')
routine('dimdoor_knock_back', 'dimensional_door', 'Knocking on the back of the door, just in case', 16,
        [k(.15, x=.9, eye='o'), k(.32, x=1.1, reach=.6, contact=1, anchor='back', mark='knock'), k(.5, eye='o', mark='...'), k(.7, x=-.4, eye='O', mark='knock?'), k(.9, eye='^')],
        [(.32, 'knock')], prefer=['young', 'curious'], tool='wing', say='dimdoor_knock')

item('teleporter', 'teleporter', 116, 116, 0.321, 'metal', 'engineering', 'Beam',
     dict(charge=(.4, 0, 1), beam=(0, 0, 1), lens=(.6, 0, 1), sent=(0, 0, 9999), target=(0, 0, 3)),
     physics=[('beam', 'decay', 0, 'always'), ('charge', 'rate', .0005, 'always'), ('lens', 'rate', -.0005, 'wet')],
     effects=dict(calibrate=[['target', 'wrap', 1]], beam=[['beam', 'set', 1], ['charge', 'add', -.35], ['sent', 'add', 1]], wipe=[['lens', 'add', .35]], stand=[['beam', 'set', .5]]),
     parts=['pebble', 'cloth'])
routine('teleport_calibrate', 'teleporter', 'Tapping coordinates into the teleporter keypad', 18,
        [k(.15, reach=.7, contact=1, anchor='keypad', mark='beep'), k(.32, contact=1, anchor='keypad', mark='boop'), k(.5, contact=1, anchor='keypad', mark='beep'), k(.75, eye='^')],
        [(.5, 'calibrate')], ages=GROWN, tool='wing')
routine('teleport_beam_pebble', 'teleporter', 'Beaming a pebble across the garden', 22,
        [k(.12, y=1, b=.6, pebble=1), k(.28, x=.6, reach=.6, contact=1, anchor='pad', pebble=1), k(.4, pebble=0, mark='set'), k(.52, reach=.7, contact=1, anchor='keypad', mark='beep'),
         k(.62, x=-.6, eye='O', mark='ZZHM'), k(.85, eye='^', mark='!')],
        [(.62, 'beam')], when=['charge>.35'], tool='none')
routine('teleport_stand_on_pad', 'teleporter', 'Standing on the pad, eyes shut, waiting to be beamed', 24,
        [k(.12, x=.6, y=-.2, eye='o'), k(.28, x=.9, y=-.4, eye='-', mark='ready'), k(.48, x=.9, eye='-', mark='...'), k(.62, x=.9, eye='o', mark='?'), k(.78, x=.2, b=.3, eye='>', mark='hmph'),
         k(.9, eye='^')],
        [(.48, 'stand')], when=['charge>.2'], prefer=['young', 'curious'], tool='none', say='teleport_wait')
routine('teleport_wipe_lens', 'teleporter', "Wiping smudges off the pad's sensor ring", 18,
        [k(.15, y=-.5, reach=.9, contact=1, anchor='sensor', cloth=1), k(.4, y=-.6, contact=1, anchor='sensor', cloth=1, mark='squeak'), k(.65, cloth=0, eye='^')],
        [(.4, 'wipe')], when=['lens<.6'], tool='cloth')

item('robot_butler', 'robot', 100, 132, 0.218, 'metal', 'crafting', 'Service',
     dict(battery=(.6, 0, 1), oil=(.6, 0, 1), shine=(.5, 0, 1), bow=(0, 0, 1), wave=(0, 0, 1), greetings=(0, 0, 9999), rust=(0, 0, 1)),
     physics=[('battery', 'rate', -.0001, 'always'), ('bow', 'decay', 0, 'always'), ('wave', 'decay', 0, 'always'), ('rust', 'rate', .0002, 'wet&!oiled'),
              ('oil', 'rate', -.00006, 'always'), ('shine', 'rate', -.00008, 'always')],
     effects=dict(charge=[['battery', 'add', .35]], oil=[['oil', 'add', .4], ['rust', 'mul', .5]], buff=[['shine', 'add', .3]], bow=[['bow', 'set', 1]], wave=[['wave', 'set', 1], ['greetings', 'add', 1]],
                  five=[['wave', 'set', 1]]),
     parts=['can', 'cloth', 'plug'])
routine('robot_wind_up', 'robot_butler', 'Winding the butler\'s key until his eyes light up', 22,
        [k(.12, reach=.7, contact=1, anchor='key'), k(.3, contact=1, anchor='key', b=.3, mark='crk'), k(.48, contact=1, anchor='key', b=-.2, mark='crk'), k(.66, x=-.5, eye='O', mark='bip!'),
         k(.86, eye='^')],
        [(.3, 'charge'), (.48, 'charge')], when=['battery<.75'], tool='wing')
routine('robot_oil_joints', 'robot_butler', 'Oiling the butler\'s squeaky elbows and knees', 24,
        [k(.12, reach=.7, contact=1, anchor='elbow', can=1), k(.3, contact=1, anchor='elbow', can=1, mark='drip'), k(.5, y=.8, contact=1, anchor='knee', can=1, mark='drip'), k(.7, x=-.4, can=0, mark='squeak?'),
         k(.88, eye='^')],
        [(.3, 'oil'), (.5, 'oil')], when=['oil<.6'], prefer=['wet', 'rust>.2'], ages=GROWN, tool='can')
routine('robot_morning_greeting', 'robot_butler', 'Saying good morning and getting a stiff robotic wave back', 18,
        [k(.12, y=-.4, w=.8, eye='^', mark='hi!'), k(.3, reach=.4, eye='o'), k(.45, eye='O', mark='bip'), k(.6, w=1, b=-.3, eye='^', mark='!'), k(.85, eye='^')],
        [(.45, 'wave')], when=['battery>.2'], prefer=['dawn', 'day', 'lonely'], tool='none', say='robot_morning')
routine('robot_teach_bow', 'robot_butler', 'Teaching the butler a proper bow, then bowing back', 26,
        [k(.12, x=.4, b=.8, y=.6, eye='-', mark='like this'), k(.3, x=.4, b=0, y=0, eye='o'), k(.45, eye='o', mark='...'), k(.58, eye='O', mark='bzzt'), k(.72, b=.8, y=.6, eye='^'),
         k(.9, eye='^')],
        [(.58, 'bow')], when=['battery>.3'], prefer=['happy', 'elder'], ages=GROWN, tool='none', say='robot_bow')
routine('robot_high_five', 'robot_butler', 'Going for a high five with the butler\'s tray hand', 16,
        [k(.15, x=.4, y=-.5, w=1, eye='^'), k(.32, x=.7, y=-.6, w=1, contact=1, anchor='hand', mark='CLANK'), k(.5, x=-.3, b=-.3, w=.4, eye='>', mark='ow'), k(.75, eye='^', mark='worth it')],
        [(.32, 'five')], when=['battery>.2'], prefer=['young', 'happy'], tool='wing')
routine('robot_buff_dome', 'robot_butler', 'Buffing the butler\'s dome until it reflects the sky', 20,
        [k(.15, y=-.6, reach=1, contact=1, anchor='dome', cloth=1), k(.4, y=-.7, contact=1, anchor='dome', cloth=1, mark='*'), k(.65, cloth=0, eye='^', mark='*')],
        [(.4, 'buff')], when=['shine<.7'], tool='cloth')

item('cloning_machine', 'cloner', 144, 124, 0.327, 'glass', 'engineering', 'Clone',
     dict(charge=(.4, 0, 1), sample=(0, 0, 1), hologram=(0, 0, 1), cycles=(0, 0, 9999), bubbles=(0, 0, 1)),
     physics=[('hologram', 'rate', -.0012, 'always'), ('bubbles', 'decay', 0, 'always'), ('charge', 'rate', .0003, 'always')],
     effects=dict(load=[['sample', 'set', 1]], run=[['hologram', 'set', 1], ['charge', 'add', -.4], ['cycles', 'add', 1], ['bubbles', 'set', 1]], purge=[['sample', 'set', 0], ['hologram', 'set', 0]],
                  tap=[['bubbles', 'set', .6]]),
     parts=['feather'])
routine('clone_load_feather', 'cloning_machine', 'Plucking a loose feather and loading it into pod A', 18,
        [k(.12, x=-.4, w=.6, eye='o', mark='plk'), k(.3, x=.5, reach=.7, contact=1, anchor='pod_a', feather=1), k(.48, contact=1, anchor='pod_a', feather=0, mark='in'), k(.75, eye='^')],
        [(.48, 'load')], when=['sample<.5'], tool='none')
routine('clone_run_cycle', 'cloning_machine', 'Running a cloning cycle and meeting a glowing duplicate', 28,
        [k(.12, reach=.8, contact=1, anchor='button', mark='beep'), k(.25, x=-.3, eye='o', mark='bloop'), k(.42, x=.9, eye='O', mark='!!'), k(.55, x=.9, w=1, eye='^', mark='hi me'),
         k(.72, x=.9, w=.2, eye='o', mark='...'), k(.88, eye='^')],
        [(.12, 'run')], when=['sample>.5', 'charge>.35'], ages=GROWN, tool='wing', say='clone_meet')
routine('clone_mirror_dance', 'cloning_machine', 'Dancing with the hologram as it copies every move', 26,
        [k(.12, x=.5, w=1, l=1, eye='^'), k(.28, x=.3, w=.2, r=1, b=.4), k(.44, x=.6, y=-.5, w=1, eye='^', mark='~'), k(.6, x=.4, b=.5, l=1), k(.76, y=-.5, w=1, eye='^', mark='*'), k(.9, eye='^')],
        [], when=['hologram>.3'], prefer=['happy', 'lonely'], tool='none')
routine('clone_tap_tube', 'cloning_machine', 'Tapping the tube to watch the bubbles rise', 14,
        [k(.15, reach=.7, contact=1, anchor='tube', mark='tink'), k(.4, x=-.3, y=-.4, eye='O', mark='o o'), k(.75, eye='^')],
        [(.15, 'tap')], prefer=['young'], tool='wing')
routine('clone_purge', 'cloning_machine', 'Flushing the pods with a big green gurgle', 18,
        [k(.15, reach=.8, contact=1, anchor='valve', b=.3), k(.4, contact=1, anchor='valve', mark='GLRRG'), k(.65, x=-.6, eye='>', mark='eww'), k(.88, eye='^')],
        [(.4, 'purge')], when=['sample>.5'], tool='wing')

item('transmogrifier', 'transmog', 136, 124, 0.314, 'metal', 'engineering', 'Transmogrify',
     dict(charge=(.4, 0, 1), hopper=(0, 0, 1), output=(0, 0, 4), cycles=(0, 0, 9999), smoke=(0, 0, 1), jam=(0, 0, 1)),
     physics=[('smoke', 'decay', 0, 'always'), ('charge', 'rate', .0004, 'always'), ('jam', 'rate', .0002, 'wet')],
     effects=dict(drop=[['hopper', 'set', 1]], crank=[['hopper', 'set', 0], ['output', 'wrap', 1], ['cycles', 'add', 1], ['smoke', 'set', 1], ['charge', 'add', -.3]], kick=[['jam', 'set', 0], ['smoke', 'set', .5]],
                  sweep=[['output', 'set', 0]]),
     parts=['leaf', 'broom'])
routine('transmog_drop_leaf', 'transmogrifier', 'Sliding a leaf into the loading drawer', 16,
        [k(.15, y=1, b=.6, leaf=1), k(.35, y=-.5, reach=1, w=.8, contact=1, anchor='drawer', leaf=1), k(.5, leaf=0, mark='plop'), k(.8, eye='^')],
        [(.5, 'drop')], when=['hopper<.5', 'jam<.5'], tool='none')
routine('transmog_crank', 'transmogrifier', 'Cranking the transmogrifier and seeing what pops out', 26,
        [k(.12, reach=.7, contact=1, anchor='crank', b=.3, mark='crk'), k(.28, contact=1, anchor='crank', b=-.2, mark='crk'), k(.44, x=-.4, eye='o', mark='PFOOF'), k(.6, x=.6, y=.8, reach=.6, contact=1, anchor='chute', eye='O'),
         k(.78, y=-.3, eye='^', mark='?!'), k(.9, eye='^')],
        [(.44, 'crank')], when=['hopper>.5', 'charge>.25'], ages=GROWN, tool='wing', say='transmog_result')
routine('transmog_kick', 'transmogrifier', 'Giving the jammed machine a firm kick', 14,
        [k(.15, x=-.3, eye='>'), k(.32, x=.6, l=1, contact=1, anchor='panel', mark='CLONK'), k(.5, x=-.4, b=-.3, eye='@', mark='ow'), k(.75, eye='^', mark='fixed')],
        [(.32, 'kick')], when=['jam>.3'], tool='none', say='transmog_kick')
routine('transmog_sweep_chute', 'transmogrifier', 'Sweeping the odd results out of the chute', 18,
        [k(.15, y=.6, reach=.7, contact=1, anchor='chute', broom=1), k(.4, x=.4, contact=1, anchor='chute', broom=1, mark='swsh'), k(.7, broom=0, eye='^')],
        [(.4, 'sweep')], when=['output>0'], tool='broom')

item('money_printer', 'printer', 120, 112, 0.257, 'metal', 'crafting', 'Print',
     dict(paper=(.5, 0, 1), ink=(.6, 0, 1), stack=(0, 0, 1), jam=(0, 0, 1), runs=(0, 0, 9999), oil=(.5, 0, 1)),
     physics=[('jam', 'rate', .0004, 'wet'), ('oil', 'rate', -.0002, 'always')],
     effects=dict(paper=[['paper', 'add', .5]], crank=[['stack', 'add', .25], ['paper', 'add', -.15], ['ink', 'add', -.05], ['runs', 'add', 1]], clear=[['jam', 'set', 0]],
                  oil=[['oil', 'add', .4]], tidy=[['stack', 'set', 0]]),
     parts=['crank', 'can'])
routine('printer_feed_paper', 'money_printer', 'Feeding a fresh ream into the printer', 16,
        [k(.15, reach=.7, contact=1, anchor='tray', mark='shff'), k(.4, contact=1, anchor='tray', mark='clk'), k(.75, eye='^')],
        [(.4, 'paper')], when=['paper<.6'], tool='wing')
routine('printer_crank_bills', 'money_printer', 'Cranking out a stack of silly Duck Bucks (not real money)', 26,
        [k(.12, reach=.7, contact=1, anchor='crank', crank=0), k(.28, contact=1, anchor='crank', crank=1, mark='chk'), k(.44, contact=1, anchor='crank', crank=2, mark='chk'), k(.6, x=-.4, eye='$'),
         k(.75, x=-.4, w=.8, eye='$', mark='rich!'), k(.9, eye='^')],
        [(.28, 'crank'), (.44, 'crank')], when=['paper>.2', 'jam<.5'], ages=GROWN, tool='wing', say='printer_bucks')
routine('printer_clear_jam', 'money_printer', 'Fishing a crumpled sheet out of the rollers', 20,
        [k(.15, y=.4, reach=.9, contact=1, anchor='rollers', eye='>'), k(.35, contact=1, anchor='rollers', b=.4, mark='hnng'), k(.52, x=-.6, b=-.4, mark='rrip'), k(.8, eye='^')],
        [(.52, 'clear')], when=['jam>.3'], tool='wing', say='printer_jam')
routine('printer_oil_rollers', 'money_printer', 'Oiling the rollers', 16,
        [k(.15, reach=.7, contact=1, anchor='rollers', can=1), k(.4, contact=1, anchor='rollers', can=1, mark='drip'), k(.75, can=0, eye='^')],
        [(.4, 'oil')], when=['oil<.5'], ages=GROWN, tool='can')
routine('printer_make_it_rain', 'money_printer', 'Tossing the play money up and letting it rain down', 18,
        [k(.12, y=.6, b=.5, reach=.5, contact=1, anchor='stack'), k(.28, y=-.6, w=1, b=-.5, eye='^', mark='$$$'), k(.5, y=-.4, w=1, eye='^', mark='$ $'), k(.75, b=.3, eye='^', mark='$'), k(.9, eye='^')],
        [(.28, 'tidy')], when=['stack>.4'], prefer=['happy', 'young'], tool='wing', say='printer_rain')

item('perpetual_motion', 'perpetual', 116, 120, 0.282, 'brass', 'engineering', 'Spin',
     dict(angle=(0, 0, 1), speed=(.35, .2, 1), oil=(.5, 0, 1), squeak=(0, 0, 1), turns=(0, 0, 999999)),
     physics=[('angle', 'wrap', .02, 'always'), ('speed', 'decay', .35, 'always'), ('oil', 'rate', -.0001, 'always'), ('squeak', 'decay', 1, 'dry_axle'), ('squeak', 'decay', 0, '!dry_axle')],
     effects=dict(spin=[['speed', 'add', .35]], oil=[['oil', 'add', .45]], count=[['turns', 'add', 1]], stop=[['speed', 'mul', .8]]),
     parts=['can'])
routine('perpetual_give_spin', 'perpetual_motion', 'Giving the wheel a spin it does not need', 16,
        [k(.15, reach=.8, contact=1, anchor='rim', w=.6), k(.32, x=.4, contact=1, anchor='rim', w=1, mark='whirr'), k(.55, x=-.3, eye='o', mark='~'), k(.85, eye='^')],
        [(.32, 'spin')], tool='wing')
routine('perpetual_try_to_stop', 'perpetual_motion', 'Trying with all his might to stop the wheel and failing', 24,
        [k(.12, x=.6, w=1, reach=1, contact=1, anchor='rim', eye='>'), k(.28, x=.8, b=.6, w=1, contact=1, anchor='rim', mark='hnng'), k(.44, x=.4, b=-.5, w=1, eye='@', mark='!!'),
         k(.6, x=-.8, b=-.4, eye='@', mark='...'), k(.8, eye='>', mark='fine'), k(.92, eye='^')],
        [(.28, 'stop')], prefer=['grumpy', 'curious'], ages=GROWN, tool='wing', say='perpetual_stop')
routine('perpetual_oil_axle', 'perpetual_motion', 'Oiling the axle to quiet its squeak', 16,
        [k(.15, reach=.7, contact=1, anchor='axle', can=1), k(.4, contact=1, anchor='axle', can=1, mark='drip'), k(.75, can=0, eye='^', mark='shh')],
        [(.4, 'oil')], when=['oil<.5'], ages=GROWN, tool='can')
routine('perpetual_count_turns', 'perpetual_motion', 'Counting the turns out loud and losing track', 26,
        [k(.12, x=.3, eye='o', mark='1'), k(.25, mark='2'), k(.38, mark='3'), k(.5, eye='-', mark='4..'), k(.62, eye='o', mark='7?'), k(.76, x=-.3, eye='@', mark='uh'), k(.9, eye='^')],
        [(.5, 'count')], prefer=['young', 'curious', 'tired'], tool='none', say='perpetual_count')

item('DNA_mixer', 'dna', 116, 124, 0.259, 'glass', 'engineering', 'Mix',
     dict(vial_a=(0, 0, 4), vial_b=(0, 0, 4), spin=(0, 0, 1), mixes=(0, 0, 9999), printout=(0, 0, 1), clean=(.7, 0, 1)),
     physics=[('spin', 'decay', 0, 'always'), ('clean', 'rate', -.0002, 'always')],
     effects=dict(load_a=[['vial_a', 'wrap', 1]], load_b=[['vial_b', 'wrap', 1]], spin=[['spin', 'set', 1], ['mixes', 'add', 1], ['printout', 'set', 1], ['clean', 'add', -.2]],
                  read=[['printout', 'set', 0]], rinse=[['clean', 'set', 1]]),
     parts=['feather', 'cloth'])
routine('dna_load_samples', 'DNA_mixer', 'Loading two feather samples into the vials', 20,
        [k(.12, x=-.4, w=.5, feather=1, mark='plk'), k(.3, reach=.7, contact=1, anchor='vial_a', feather=1), k(.42, feather=0, mark='in'), k(.55, x=.6, contact=1, anchor='vial_b', feather=1),
         k(.68, feather=0, mark='in'), k(.85, eye='^')],
        [(.42, 'load_a'), (.68, 'load_b')], ages=GROWN, tool='none')
routine('dna_spin_helix', 'DNA_mixer', 'Spinning the helix centrifuge up to a whine', 22,
        [k(.12, reach=.8, contact=1, anchor='switch', mark='click'), k(.3, x=-.4, eye='o', mark='wheee'), k(.5, x=-.5, eye='O', mark='EEEE'), k(.7, x=-.2, eye='o', mark='ding'), k(.88, eye='^')],
        [(.12, 'spin')], when=['clean>.25'], ages=GROWN, tool='wing')
routine('dna_read_printout', 'DNA_mixer', 'Reading the ridiculous results off the printout', 22,
        [k(.15, reach=.7, contact=1, anchor='slot', mark='rrr'), k(.35, y=.3, eye='o', mark='hm'), k(.55, eye='O', mark='?!'), k(.75, b=-.4, eye='^', mark='HA'), k(.9, eye='^')],
        [(.35, 'read')], when=['printout>.5'], tool='wing', say='dna_result')
routine('dna_rinse_vials', 'DNA_mixer', 'Rinsing the vials clean', 18,
        [k(.15, reach=.7, contact=1, anchor='vial_a', cloth=1), k(.4, x=.5, contact=1, anchor='vial_b', cloth=1, mark='squeak'), k(.75, cloth=0, eye='^')],
        [(.4, 'rinse')], when=['clean<.6'], tool='cloth')

# --------------------------------------------------------------------------- handheld curiosities on stands
item('shrink_ray', 'ray', 112, 96, 0.194, 'metal', 'engineering', 'Zap',
     dict(charge=(.5, 0, 1), dial=(.5, 0, 1), target=(1, .2, 1), zaps=(0, 0, 9999), glow=(0, 0, 1)),
     physics=[('glow', 'decay', 0, 'always'), ('charge', 'rate', .0004, 'always'), ('target', 'decay', 1, 'calm')],
     effects=dict(charge=[['charge', 'add', .35]], dial=[['dial', 'wrap', .25]], zap=[['target', 'mul', .55], ['zaps', 'add', 1], ['glow', 'set', 1], ['charge', 'add', -.3]],
                  blow=[['glow', 'set', 0]], reset=[['target', 'set', 1]]),
     parts=['pebble'])
routine('shrink_charge', 'shrink_ray', 'Pumping the shrink ray\'s capacitor', 18,
        [k(.15, reach=.7, contact=1, anchor='pump', b=.3, mark='pmp'), k(.35, contact=1, anchor='pump', b=-.2, mark='pmp'), k(.6, x=-.3, eye='o', mark='hmmm'), k(.85, eye='^')],
        [(.15, 'charge'), (.35, 'charge')], when=['charge<.7'], ages=GROWN, tool='wing')
routine('shrink_zap_pebble', 'shrink_ray', 'Zapping a pebble on the target plate down to a speck', 22,
        [k(.12, y=1, b=.6, pebble=1), k(.25, x=.6, contact=1, anchor='plate', pebble=0, mark='set'), k(.4, x=-.2, reach=.8, contact=1, anchor='trigger', eye='>'), k(.5, contact=1, anchor='trigger', mark='PEW'),
         k(.66, x=.6, y=.6, eye='O', mark='tiny!'), k(.88, eye='^')],
        [(.5, 'zap')], when=['charge>.3', 'target>.3'], ages=GROWN, tool='wing', say='shrink_zap')
routine('shrink_blow_barrel', 'shrink_ray', 'Blowing the smoke off the barrel like a cowboy', 14,
        [k(.15, x=.5, y=-.3, eye='-'), k(.35, x=.7, mark='fwoo'), k(.6, w=.6, eye='^', mark='*'), k(.85, eye='^')],
        [(.35, 'blow')], when=['glow>.2'], prefer=['happy'], tool='none')
routine('shrink_reset_plate', 'shrink_ray', 'Turning the dial to undo the shrink', 16,
        [k(.15, reach=.7, contact=1, anchor='dial'), k(.4, contact=1, anchor='dial', mark='clk'), k(.6, x=.5, y=.5, eye='O', mark='back!'), k(.85, eye='^')],
        [(.4, 'reset')], when=['target<.7'], tool='wing')

item('growth_ray', 'ray', 112, 96, 0.194, 'metal', 'engineering', 'Zap',
     dict(charge=(.5, 0, 1), dial=(.5, 0, 1), target=(1, 1, 3), zaps=(0, 0, 9999), glow=(0, 0, 1)),
     physics=[('glow', 'decay', 0, 'always'), ('charge', 'rate', .0004, 'always'), ('target', 'decay', 1, 'calm')],
     effects=dict(charge=[['charge', 'add', .35]], zap=[['target', 'add', .7], ['zaps', 'add', 1], ['glow', 'set', 1], ['charge', 'add', -.3]], blow=[['glow', 'set', 0]],
                  reset=[['target', 'set', 1]]),
     parts=['flower'])
routine('growth_charge', 'growth_ray', 'Pumping the growth ray\'s capacitor', 18,
        [k(.15, reach=.7, contact=1, anchor='pump', b=.3, mark='pmp'), k(.35, contact=1, anchor='pump', b=-.2, mark='pmp'), k(.6, x=-.3, eye='o'), k(.85, eye='^')],
        [(.15, 'charge'), (.35, 'charge')], when=['charge<.7'], ages=GROWN, tool='wing')
routine('growth_zap_dandelion', 'growth_ray', 'Zapping a dandelion until it towers over him', 24,
        [k(.12, y=1, b=.6, flower=1), k(.25, x=.6, contact=1, anchor='plate', flower=0, mark='set'), k(.4, x=-.2, reach=.8, contact=1, anchor='trigger', eye='>'), k(.5, contact=1, anchor='trigger', mark='BZOW'),
         k(.66, x=-.4, y=-.8, eye='O', mark='HUGE'), k(.88, eye='^')],
        [(.5, 'zap')], when=['charge>.3', 'target<2.5'], ages=GROWN, tool='wing', say='growth_zap')
routine('growth_sniff_giant', 'growth_ray', 'Sniffing the giant dandelion and sneezing', 16,
        [k(.15, x=.6, y=-.4, eye='-'), k(.35, x=.8, y=-.5, mark='snf'), k(.5, x=.8, eye='>', mark='ah..'), k(.62, x=-.6, b=-.6, w=1, eye='@', mark='CHOO'), k(.85, eye='^')],
        [], when=['target>1.4'], prefer=['young', 'spring'], tool='none')
routine('growth_reset_plate', 'growth_ray', 'Turning the dial to shrink the flower back', 16,
        [k(.15, reach=.7, contact=1, anchor='dial'), k(.4, contact=1, anchor='dial', mark='clk'), k(.85, eye='^')],
        [(.4, 'reset')], when=['target>1.3'], tool='wing')

item('genie_lamp', 'lamp', 100, 84, 0.27, 'brass', 'observation', 'Rub',
     dict(polish=(.4, 0, 1), smoke=(0, 0, 1), wishes=(0, 0, 3), peeks=(0, 0, 9999)),
     physics=[('smoke', 'decay', 0, 'always'), ('polish', 'rate', -.0004, 'wet')],
     effects=dict(rub=[['polish', 'add', .2], ['smoke', 'set', 1]], wish=[['wishes', 'add', 1]], buff=[['polish', 'add', .35]], peek=[['peeks', 'add', 1]]),
     parts=['cloth'])
routine('genie_rub_lamp', 'genie_lamp', 'Rubbing the lamp until purple smoke curls out', 22,
        [k(.12, y=.6, b=.5, reach=.5, contact=1, anchor='belly', w=.6), k(.28, contact=1, anchor='belly', w=1, mark='rub'), k(.42, contact=1, anchor='belly', w=.6, mark='rub'), k(.58, x=-.7, b=-.5, eye='O', mark='!!'),
         k(.8, y=-.5, eye='O', mark='...'), k(.92, eye='^')],
        [(.42, 'rub')], tool='wing', say='genie_smoke')
routine('genie_make_wish', 'genie_lamp', 'Closing his eyes and making one of his three wishes', 20,
        [k(.12, y=.6, b=.4, w=.4, contact=1, anchor='belly'), k(.3, y=-.3, w=.8, eye='-', mark='...'), k(.55, y=-.4, w=.8, eye='-', mark='please'), k(.75, eye='o', mark='?'), k(.9, eye='^')],
        [(.55, 'wish')], when=['smoke>.3', 'wishes<3'], prefer=['sad', 'lonely'], tool='none', say='genie_wish')
routine('genie_polish_spout', 'genie_lamp', 'Polishing the long curly spout', 18,
        [k(.15, reach=.8, contact=1, anchor='spout', cloth=1), k(.4, x=.4, contact=1, anchor='spout', cloth=1, mark='*'), k(.75, cloth=0, eye='^')],
        [(.4, 'buff')], when=['polish<.7'], tool='cloth')
routine('genie_peek_spout', 'genie_lamp', 'Peering down the spout for whoever lives in there', 16,
        [k(.15, x=.7, y=.5, b=.5, eye='o'), k(.35, x=.9, y=.6, contact=1, anchor='spout', eye='O', mark='hello?'), k(.6, x=-.4, eye='o', mark='...'), k(.85, eye='^')],
        [(.35, 'peek')], prefer=['young', 'curious'], tool='none', say='genie_peek')

item('invisible_cloak', 'cloak', 100, 120, 0.282, 'cloth', 'crafting', 'Try',
     dict(shimmer=(.3, 0, 1), folded=(0, 0, 1), hidden=(0, 0, 1), dust=(0, 0, 1)),
     physics=[('shimmer', 'decay', .3, 'always'), ('hidden', 'decay', 0, 'always'), ('shimmer', 'decay', .9, 'windy&folded<.5'), ('dust', 'rate', .0002, 'dry')],
     effects=dict(shake=[['shimmer', 'set', 1], ['dust', 'set', 0]], fold=[['folded', 'set', 1]], hang=[['folded', 'set', 0]], hide=[['hidden', 'set', 1]], peek=[['hidden', 'set', .5]]),
     parts=['cloak'])
routine('cloak_shake_out', 'invisible_cloak', 'Shaking the cloak out so it shimmers in the air', 18,
        [k(.15, reach=.9, contact=1, anchor='hem', w=.6), k(.35, y=-.4, w=1, b=-.3, contact=1, anchor='hem', mark='fwap'), k(.55, w=.8, contact=1, anchor='hem', mark='fwap'), k(.8, eye='^')],
        [(.35, 'shake')], when=['folded<.5'], tool='wing')
routine('cloak_hide_under', 'invisible_cloak', 'Hiding under the cloak and sneaking a look out', 26,
        [k(.12, reach=.9, contact=1, anchor='hem', cloak=1), k(.28, y=.5, b=.6, cloak=1, eye='-', mark='shh'), k(.45, y=.5, b=.6, cloak=1, eye='-'), k(.62, y=.4, cloak=.6, eye='o', mark='peek'),
         k(.8, cloak=0, w=1, b=-.4, eye='^', mark='BOO'), k(.92, eye='^')],
        [(.28, 'hide'), (.62, 'peek'), (.8, 'shake')], when=['folded<.5'], prefer=['young', 'happy', 'lonely'], tool='none', say='cloak_boo')
routine('cloak_fold', 'invisible_cloak', 'Folding the cloak neatly over the stand', 18,
        [k(.15, reach=.8, contact=1, anchor='hem'), k(.4, y=-.4, w=.8, contact=1, anchor='mid', mark='fold'), k(.7, eye='^')],
        [(.4, 'fold')], when=['folded<.5'], prefer=['night', 'wet'], tool='wing')
routine('cloak_hang_up', 'invisible_cloak', 'Unfolding the cloak and shaking it back over the stand', 16,
        [k(.15, reach=.8, contact=1, anchor='mid'), k(.45, y=-.5, w=1, contact=1, anchor='mid', mark='there'), k(.8, eye='^')],
        [(.45, 'hang')], when=['folded>.5'], prefer=['day'], tool='wing')

item('dream_catcher', 'dreamcatcher', 96, 132, 0.295, 'fiber', 'observation', 'Untangle',
     dict(dreams=(0, 0, 1), tangle=(0, 0, 1), sway=(0, 0, 1), feathers=(3, 3, 6), released=(0, 0, 9999)),
     physics=[('dreams', 'rate', .0016, 'night'), ('tangle', 'rate', .0007, 'windy'), ('sway', 'wrap', .01, 'windy'), ('sway', 'wrap', .002, 'calm')],
     effects=dict(untangle=[['tangle', 'add', -.35]], feather=[['feathers', 'add', 1]], release=[['dreams', 'set', 0], ['released', 'add', 1]], watch=[]),
     parts=['feather'])
routine('dream_untangle', 'dream_catcher', 'Picking the wind tangles out of the web', 26,
        [k(.12, y=-.5, reach=.9, contact=1, anchor='web', eye='o'), k(.3, y=-.6, contact=1, anchor='web', mark='pik'), k(.48, y=-.5, x=.3, contact=1, anchor='web_r', mark='pik'), k(.7, eye='^')],
        [(.3, 'untangle'), (.48, 'untangle')], when=['tangle>.25'], ages=GROWN, tool='wing')
routine('dream_hang_feather', 'dream_catcher', 'Tying one of his own moulted feathers to the hoop', 20,
        [k(.12, x=-.4, w=.5, feather=1, mark='plk'), k(.3, y=-.3, reach=.8, contact=1, anchor='tassel', feather=1), k(.5, contact=1, anchor='tassel', feather=0, mark='tie'), k(.8, eye='^', mark='<3')],
        [(.5, 'feather')], when=['feathers<6'], prefer=['spring', 'happy'], tool='none', say='dream_feather')
routine('dream_watch_glow', 'dream_catcher', 'Watching caught dreams glow in the web at night', 30,
        [k(.12, x=.3, y=.6, b=.5, eye='o'), k(.35, y=.6, b=.5, eye='O', mark='~'), k(.6, y=.7, b=.6, eye='-', mark='*'), k(.85, eye='-')],
        [(.6, 'watch')], when=['night', 'dreams>.2'], prefer=['sad', 'tired', 'lonely'], tool='none')
routine('dream_morning_release', 'dream_catcher', 'Shaking last night\'s dreams loose into the morning light', 20,
        [k(.15, y=-.4, reach=.9, contact=1, anchor='web', w=.6), k(.35, contact=1, anchor='web', w=1, mark='shk'), k(.5, x=-.5, y=-.6, eye='O', mark='*  *'), k(.75, eye='^', mark='*'), k(.9, eye='^')],
        [(.35, 'release')], when=['dreams>.3', 'dawn_or_day'], tool='wing', say='dream_release')

item('dragon_egg', 'dragonegg', 112, 104, 0.228, 'stone', 'care', 'Warm',
     dict(warmth=(.4, 0, 1), incubation=(0, 0, 1), wobble=(0, 0, 1), embers=(.5, 0, 1), turns=(0, 0, 9999), shine=(.4, 0, 1)),
     physics=[('warmth', 'rate', -.0012, 'always'), ('warmth', 'rate', -.003, 'cold'), ('incubation', 'rate', .00016, 'warm_egg'), ('wobble', 'decay', 0, 'always'),
              ('embers', 'rate', -.0008, 'always'), ('embers', 'rate', -.004, 'wet'), ('warmth', 'rate', .0016, 'embered')],
     triggers=[('incubation>=.999', [['incubation', 'set', 1], ['wobble', 'set', 1]])],
     effects=dict(brood=[['warmth', 'add', .35], ['wobble', 'set', .4]], turn=[['turns', 'add', 1], ['wobble', 'set', .6]], stoke=[['embers', 'add', .35]], listen=[], buff=[['shine', 'add', .3]],
                  hum=[['warmth', 'add', .1], ['wobble', 'set', .3]]),
     parts=['stick', 'cloth'])
routine('dragon_brood', 'dragon_egg', 'Settling over the dragon egg like a proper duck to keep it warm', 40,
        [k(.12, x=.6, y=.4, b=.5, w=.6, eye='o'), k(.25, x=.8, y=1, b=.9, w=1, contact=1, anchor='shell', eye='^'), k(.5, x=.8, y=1, b=.9, w=1, contact=1, anchor='shell', eye='-', mark='~'),
         k(.75, x=.8, y=1, b=.9, w=1, contact=1, anchor='shell', eye='-'), k(.9, y=.3, w=.4, eye='^')],
        [(.25, 'brood'), (.5, 'brood'), (.75, 'brood')], when=['incubation<1'], prefer=['cold', 'night', 'warmth<.4'], tool='wing', say='dragon_brood')
routine('dragon_turn_egg', 'dragon_egg', 'Gently rolling the egg a quarter turn', 18,
        [k(.15, y=.5, b=.5, reach=.6, contact=1, anchor='shell', w=.6), k(.4, x=.4, y=.6, contact=1, anchor='shell', w=1, mark='roll'), k(.65, eye='o', mark='careful'), k(.88, eye='^')],
        [(.4, 'turn')], when=['incubation<1'], ages=GROWN, tool='wing')
routine('dragon_stoke_embers', 'dragon_egg', 'Poking the embers in the nest back to a glow', 18,
        [k(.15, y=.6, b=.5, reach=.7, contact=1, anchor='embers', stick=1), k(.38, contact=1, anchor='embers', stick=1, mark='pok'), k(.6, x=-.4, eye='o', mark='~'), k(.85, stick=0, eye='^')],
        [(.38, 'stoke')], when=['embers<.6', '!wet'], ages=GROWN, tool='stick')
routine('dragon_ear_to_shell', 'dragon_egg', 'Pressing an ear to the shell and hearing something move', 22,
        [k(.15, x=.7, y=.5, b=.5, eye='o'), k(.35, x=.9, y=.5, contact=1, anchor='shell', eye='-', mark='...'), k(.55, x=.9, eye='O', mark='tap tap'), k(.75, x=-.4, eye='O', mark='!!'), k(.9, eye='^')],
        [(.35, 'listen')], when=['incubation>.2'], prefer=['curious', 'young'], tool='none', say='dragon_listen')
routine('dragon_lullaby', 'dragon_egg', 'Humming a lullaby to the egg at bedtime', 26,
        [k(.12, x=.4, y=.3, b=.3, eye='-', mark='~'), k(.3, w=.4, eye='-', mark='la'), k(.5, w=.2, eye='-', mark='~'), k(.7, w=.4, eye='-', mark='la'), k(.88, eye='^')],
        [(.5, 'hum')], when=['night'], prefer=['tired', 'elder'], tool='none', say='dragon_lullaby')
routine('dragon_polish_scales', 'dragon_egg', 'Polishing the egg\'s scaly shell', 18,
        [k(.15, reach=.6, contact=1, anchor='shell', cloth=1), k(.4, x=.3, contact=1, anchor='shell', cloth=1, mark='*'), k(.75, cloth=0, eye='^')],
        [(.4, 'buff')], when=['shine<.6'], tool='cloth')

assert len(ITEMS) == 32, len(ITEMS)
# Coarse grid: small wonders draw the same geometry on a grid 2-3x coarser and
# scale up by the same factor, so world size and control heights are unchanged
# while each ASCII character renders 2-3x larger (comparable to the keepsakes).
for _k, _v in ITEMS.items():
    _px = 7.5 * _v['scale'] * .62
    _v['grid'] = max(1, min(3, round(2.6 / _px)))
    _v['scale'] = round(_v['scale'] * _v['grid'], 4)
OUT.joinpath('wonders.json').write_text(json.dumps(ITEMS, indent=1) + '\n')
OUT.joinpath('wonder-routines.json').write_text(json.dumps(ROUTINES, indent=1) + '\n')
print(len(ITEMS), 'wonders,', len(ROUTINES), 'routines')
