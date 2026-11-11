"""Authoring source for nest routines; emits the shared runtime score.

Each row is a timed physical pose, not a randomly varied idle. Character joints,
contact position, nest compression, lining and a loose prop share one clock.
Run from any directory to regenerate client/animation/nest-routines.json.
"""
import json
from pathlib import Path

ROUTINES = {}


def k(at, **pose):
    return dict(at=at, **pose)


def routine(key, label, duration, prop, track, *, when=None, motive='comfort', effect=None):
    ROUTINES[key] = dict(label=label, duration=duration, prop=prop,
                         when=when or {}, motive=motive, effect=effect or {},
                         track=[k(0), *track, k(1)])


# Joint values x/y/b/w/l/r use the established D10 rig. u/v are small contact
# offsets within the nest. px/py are loose-prop offsets from its inner bowl.
# show controls the prop, turn its orientation, press the bowl, straw the lining.
routine('bowl_test', 'Testing the softness of the nest', 11, 'fibres', [
    k(.18,y=1,b=.4,l=1,press=.2), k(.35,y=1.5,b=.8,press=1,show=1,py=1),
    k(.52,y=-.3,b=-.3,w=.25,press=.1), k(.72,b=.6,r=1,press=.7,show=.5), k(.9,eye='^')])
routine('circle_settle', 'Turning a little hollow to settle into', 16, 'tracks', [
    k(.13,u=-.5,v=.1,l=1,show=1), k(.28,u=-.7,v=-.25,r=1,x=-.6,turn=1,show=1),
    k(.44,u=0,v=-.4,l=1,show=1,turn=2), k(.6,u=.7,v=-.2,r=1,show=1,turn=3),
    k(.75,u=.4,v=.2,l=1,press=.5,show=1,turn=4), k(.9,b=.6,y=.8,press=.8)])
routine('tuck_left_edge', 'Tucking a loose strand into the left rim', 14, 'strand', [
    k(.17,u=-.65,x=-.7,y=1,show=1,px=-17,py=-2), k(.32,u=-.7,x=-1,y=1.7,w=.3,show=1,px=-16,py=-4,turn=-1),
    k(.5,u=-.45,x=.5,y=.8,show=1,px=-9,py=-6,turn=1), k(.7,u=-.25,y=1.8,press=.5,show=1,px=-7,py=1), k(.9,y=.6)])
routine('tuck_right_edge', 'Folding the right edge back into place', 13, 'strand', [
    k(.15,u=.5,x=.8,y=.8,show=1,px=18,py=0), k(.35,u=.7,x=1,y=1.7,w=.4,show=1,px=16,py=-3,turn=1),
    k(.53,u=.3,x=-.5,y=.5,show=1,px=9,py=-5,turn=-1), k(.72,y=1.6,b=.4,show=1,px=5,py=1,press=.8), k(.9,eye='^')])
routine('lift_loose_twig', 'Lifting a crooked twig out of the lining', 17, 'twig', [
    k(.18,x=.8,y=1.4,show=1,px=10,py=0), k(.35,x=1,y=.2,show=1,px=11,py=-7,turn=1,gape=.4),
    k(.5,x=-.6,y=-.5,show=1,px=-2,py=-10,turn=2), k(.68,u=-.4,y=1.1,show=1,px=-19,py=2,turn=1), k(.85,y=.5,eye='^')],motive='care',effect={'tidiness':.012})
routine('crossbrace_twig', 'Bracing a soft spot in the nest rim', 18, 'twig', [
    k(.15,u=.5,y=1.2,show=1,px=19,py=2,turn=1), k(.35,x=.8,y=-.2,show=1,px=10,py=-6),
    k(.55,x=1,y=1.7,w=.4,show=1,px=7,py=-1), k(.68,y=.5,show=1,px=6,py=0), k(.8,y=1.8,b=.5,press=.6,show=1,px=6,py=1)],motive='care',effect={'tidiness':.008})
routine('weave_rim', 'Weaving a strand over and under the rim', 20, 'strand', [
    k(.15,u=.4,x=.7,y=1.5,show=1,px=14,py=0,turn=-1), k(.3,y=.3,show=1,px=12,py=-4,turn=1),
    k(.45,y=1.7,show=1,px=8,py=1,turn=-1), k(.6,y=.5,show=1,px=4,py=-3,turn=1),
    k(.75,y=1.6,w=.3,show=1,px=0,py=1,turn=-1), k(.9,press=.6,eye='^')],motive='care',effect={'tidiness':.01})
routine('tamp_floor', 'Patting the nest floor flat with both feet', 13, 'fibres', [
    k(.12,l=1,b=-.2,show=.5), k(.25,l=0,b=.5,press=.8,show=1,px=-5),
    k(.4,r=1,b=-.2,press=.1), k(.55,b=.5,press=.9,show=1,px=5),
    k(.7,l=1,r=1,b=-.5,w=.4), k(.82,b=.8,press=1,show=1,py=2), k(.93,y=.6)])
routine('fluff_center', 'Fluffing the lining with a busy little wing', 16, 'fibres', [
    k(.17,x=.5,y=1.2,w=.3,show=.4), k(.32,w=1,y=.6,straw=.8,show=1,py=-6,turn=1),
    k(.47,w=.2,y=1.5,show=.3), k(.62,w=1.1,y=.4,straw=1,show=1,py=-9,turn=2),
    k(.8,w=.3,b=.5,press=.5,show=.6,py=-2), k(.94,eye='^')],motive='care',effect={'tidiness':.01})
routine('pick_grit', 'Picking an annoying pebble out of the bedding', 15, 'pebble', [
    k(.17,x=.8,y=1.7,show=1,px=8,py=1), k(.33,x=1,y=.4,gape=.5,show=1,px=10,py=-6),
    k(.5,x=-.7,y=-.3,show=1,px=-3,py=-9), k(.65,u=-.5,x=-1,y=.8,show=1,px=-23,py=-2),
    k(.8,show=1,px=-26,py=3,eye='>'), k(.92,y=.8,press=.3)],motive='care',effect={'tidiness':.015})
routine('sweep_crumbs', 'Sweeping crumbs away from the sleeping hollow', 16, 'crumbs', [
    k(.15,y=1.2,show=1,px=-3,py=0), k(.3,w=.3,x=-.5,show=1,px=0,py=0),
    k(.48,w=1.1,x=.6,show=1,px=12,py=1,turn=1), k(.65,w=.4,show=1,px=22,py=3,turn=2),
    k(.8,y=1.4,eye='^',show=.3,px=25,py=4)],motive='care',effect={'tidiness':.02})
routine('straighten_feather', 'Laying a soft feather along the inner edge', 18, 'feather', [
    k(.18,y=1.2,x=.7,show=1,px=12,py=0,turn=2), k(.34,y=.2,x=1,show=1,px=10,py=-7,turn=1),
    k(.5,y=-.3,x=-.5,show=1,px=0,py=-9), k(.67,y=1.2,u=-.25,show=1,px=-10,py=-1),
    k(.84,w=.4,press=.4,show=1,px=-10,py=1,eye='^')],motive='care',effect={'tidiness':.01})
routine('leaf_underlay', 'Sliding a leaf underneath a prickly patch', 19, 'leaf', [
    k(.16,u=.4,x=.5,y=1.6,show=1,px=20,py=1,turn=1), k(.34,x=.8,y=.2,show=1,px=11,py=-7),
    k(.52,u=.2,b=-.4,l=1,show=1,px=5,py=-1,turn=-1), k(.7,b=.7,y=.5,press=.9,show=.7,px=0,py=2),
    k(.88,y=1,eye='^')],motive='care',effect={'tidiness':.01})
routine('mend_gap', 'Working two loose ends back into the rim', 21, 'fork', [
    k(.15,u=-.4,y=1.4,show=1,px=-15,py=0), k(.3,x=-.8,y=.4,show=1,px=-13,py=-5,turn=1),
    k(.45,x=.5,y=1.4,show=1,px=-6,py=0), k(.6,x=1,y=.5,w=.5,show=1,px=6,py=-4,turn=-1),
    k(.78,y=1.6,b=.4,press=.7,show=1,px=0,py=1), k(.92,eye='^')],motive='care',effect={'tidiness':.012})
routine('widen_bowl', 'Pushing the lining outward to make more room', 17, 'fibres', [
    k(.18,b=.4,y=.7,press=.5), k(.36,w=1.2,b=.7,show=1,px=14,py=0,turn=1,press=1),
    k(.54,w=.4,x=-.6,y=1,show=1,px=-10,turn=-1,press=.4), k(.72,w=1,b=.8,show=1,px=-18,turn=2,press=1),
    k(.9,b=.5,y=1,eye='^')])
routine('tighten_braid', 'Giving a loose braid a careful tug', 18, 'braid', [
    k(.2,x=.7,y=1.6,show=1,px=14,py=1), k(.38,x=1,y=.7,w=.3,show=1,px=12,py=-3,turn=1),
    k(.56,x=-.8,y=.2,b=-.3,show=1,px=5,py=-5,turn=2), k(.7,x=.5,y=1.5,b=.5,press=.6,show=1,px=7,py=1),
    k(.88,y=.7,eye='^')],motive='care',effect={'tidiness':.01})

routine('curl_sleep', 'Tucking his bill into his feathers for a nap', 27, 'breath', [
    k(.16,x=-.4,y=.6,b=.3,press=.3), k(.3,x=-1,y=1.4,b=.7,eye='-',press=.8),
    k(.5,x=-1,y=1.3,b=.5,eye='-',press=.6,show=.5), k(.7,x=-1,y=1.4,b=.8,eye='-',press=.9,show=1,px=-4,py=-5),
    k(.86,x=-.7,y=.9,b=.5,eye='-',press=.5)],motive='rest')
routine('one_eye_guard', 'Dozing with one suspicious eye on the pond', 24, 'breath', [
    k(.15,x=-.6,y=1,b=.5,eye='-',press=.5), k(.34,x=-.6,y=1,b=.6,eye='-',show=.5),
    k(.43,x=.5,y=.2,eye='>',show=0), k(.55,x=.8,y=-.4,eye='>'),
    k(.68,x=-.5,y=1,b=.6,eye='-',show=.6), k(.87,x=-.6,y=1.2,b=.7,eye='-',press=.7)],motive='rest')
routine('dream_paddle', 'Dreaming of a very small swimming adventure', 25, 'dream', [
    k(.18,x=-.7,y=1.2,b=.6,eye='-',press=.6), k(.33,x=-.7,y=1.1,b=.5,l=1,eye='-',show=.4),
    k(.46,x=-.7,y=1.3,b=.7,r=1,eye='-',show=.8,turn=1), k(.58,x=-.6,y=1.1,b=.5,l=1,w=.25,eye='-',show=1,turn=2),
    k(.74,x=-.7,y=1.3,b=.7,r=1,eye='-',show=.5,turn=3), k(.9,x=-.5,y=1,eye='-')],motive='rest')
routine('startled_awake', 'Waking with a tiny undignified start', 14, 'fibres', [
    k(.2,x=-.7,y=1.2,b=.6,eye='-',press=.7), k(.37,b=-1,y=-.7,w=1,l=1,r=1,eye='O',show=1,py=-8,turn=2,straw=1),
    k(.5,b=.7,y=.5,eye='O',press=1,show=.5,py=-1), k(.65,x=-.6,y=-.3,eye='>'),
    k(.82,x=.5,eye='>',w=.2)],motive='curiosity')
routine('long_yawn', 'Yawning far more dramatically than necessary', 18, 'breath', [
    k(.18,y=.5,b=.3,eye='-'), k(.35,y=-.4,x=.4,gape=.6,eye='-'),
    k(.55,y=-1,x=.6,w=.5,gape=1,eye='-',show=1,px=10,py=-8), k(.7,y=-.5,gape=.6,w=.3,eye='-'),
    k(.86,y=.7,b=.4,eye='-',press=.4)],motive='rest')
routine('stretch_wing', 'Stretching one wing out over the nest', 17, 'feather', [
    k(.18,y=-.5,b=-.3,w=.3,show=.3,px=-6,py=-1), k(.37,x=.4,y=-.8,w=1.25,l=1,show=1,px=15,py=-9,turn=1),
    k(.58,w=1.25,y=-.6,eye='^',show=1,px=20,py=-7,turn=2), k(.73,w=.5,b=.2,show=.7,px=23,py=-2,turn=3),
    k(.9,y=.5,press=.4,show=.2,px=21,py=3)])
routine('foot_tuck', 'Warming one foot beneath his belly', 21, 'breath', [
    k(.18,l=1,x=-.4,y=1,press=.3), k(.35,l=1,b=.6,x=-.5,y=1.4,eye='-',press=.8),
    k(.55,l=1,b=.5,x=-.5,y=1.2,eye='-',show=.5), k(.72,l=1,b=.7,y=1.4,eye='-',show=.7,py=-3),
    k(.88,y=.8,b=.3,press=.4)],when={'temperature':'cold'},motive='rest')
routine('tail_wriggle', 'Wriggling his tail until the hollow is just right', 13, 'fibres', [
    k(.15,b=.4,tail=-1,press=.4,show=.3), k(.3,b=.7,tail=1,press=.9,show=1,px=-7,turn=1),
    k(.45,b=.4,tail=-1,press=.4,show=1,px=7,turn=-1), k(.6,b=.8,tail=1,press=1,show=.8,px=-5),
    k(.78,b=.6,y=.8,tail=-.5,press=.7,eye='^')])
routine('chin_on_rim', 'Resting his chin on the edge and watching', 23, 'none', [
    k(.18,u=.4,x=.8,y=1,b=.3), k(.35,u=.6,x=1.2,y=1.8,b=.4,press=.5),
    k(.55,u=.6,x=1.1,y=1.7,b=.4,eye='-',press=.5), k(.7,u=.6,x=1.1,y=1.7,b=.4,eye='O'),
    k(.86,u=.3,x=.7,y=.8)],motive='curiosity')
routine('satisfied_sigh', 'Sinking into the nest with a contented sigh', 20, 'breath', [
    k(.18,y=-.5,b=-.2,w=.3), k(.38,y=.6,b=.7,press=.9,gape=.3,eye='^',show=.4,px=8,py=-3),
    k(.55,x=-.5,y=1.1,b=.8,eye='-',press=1,show=1,px=13,py=-6),
    k(.75,x=-.7,y=1.3,b=.6,eye='-',press=.7,show=.4,px=17,py=-9), k(.9,x=-.4,y=.7)],when={'mood':'content'})
routine('grumpy_rearrange', 'Rearranging the nest with unnecessary force', 15, 'fibres', [
    k(.15,y=1.3,x=.6,eye='>',show=.3), k(.3,w=1.2,x=-.7,b=-.3,eye='>',show=1,px=-15,py=-8,straw=1),
    k(.47,y=1.7,b=.8,eye='>',press=1), k(.62,w=1.1,x=.8,eye='>',show=1,px=18,py=-7,turn=2,straw=1),
    k(.8,b=.8,y=.7,eye='>',press=1)],when={'mood':'grumpy'},motive='care')
routine('shy_hide', 'Peeking over the rim before sinking out of sight', 20, 'none', [
    k(.15,x=-.7,y=.6,b=.4,press=.5), k(.35,y=1.4,b=1,v=.3,press=1,eye='-'),
    k(.55,y=-.6,b=-.3,v=-.2,eye='O'), k(.67,x=.8,y=-.5,b=-.2,v=-.2),
    k(.82,y=1.5,b=.9,v=.3,press=1,eye='-')],when={'mood':'shy'})
routine('bored_twig_tap', 'Tapping a twig against the rim', 18, 'twig', [
    k(.15,y=1.2,x=.6,show=1,px=13,py=0), k(.3,y=-.3,x=.8,show=1,px=12,py=-7,turn=1),
    k(.43,y=1.5,show=1,px=14,py=0), k(.56,y=-.2,show=1,px=11,py=-7,turn=1),
    k(.69,y=1.6,show=1,px=14,py=0,eye='>'), k(.84,y=.5,show=1,px=19,py=2)],when={'mood':'bored'},motive='curiosity')
routine('proud_inspect', 'Inspecting his nest as if he built a palace', 19, 'none', [
    k(.15,y=-.6,b=-.3), k(.32,x=-1,y=.5,w=.3), k(.5,x=1,y=.7,w=.5),
    k(.68,y=-.8,b=-.3,w=.8,eye='^'), k(.85,y=-.3,x=.5,eye='^')],when={'bond':.4},motive='curiosity')

# These three require a canopy. Uncovered nests never claim to provide shelter.
routine('rain_listen', 'Listening to rain patter on the canopy', 24, 'drops', [
    k(.18,x=-.6,y=-.7,show=.5,px=-18,py=-14), k(.36,x=.8,y=-1,show=1,px=20,py=-10,turn=1),
    k(.52,x=.3,y=-.6,eye='-',show=.7,px=17,py=-2,turn=2), k(.7,y=.8,b=.5,press=.6,show=1,px=-21,py=-5),
    k(.88,x=-.5,y=1,eye='-',press=.6)],when={'roof':True,'weather':'rain'},motive='rest')
routine('drip_watch', 'Following a drip down the canopy edge', 20, 'drop', [
    k(.15,x=.8,y=-1,show=1,px=23,py=-17), k(.34,x=1,y=-.5,show=1,px=23,py=-10),
    k(.5,x=1.1,y=1.2,show=1,px=23,py=-2), k(.65,x=.6,y=1.8,show=1,px=23,py=4,turn=1),
    k(.82,x=-.5,y=-.4,eye='O')],when={'roof':True,'weather':'rain'},motive='curiosity')
routine('thunder_duck', 'Ducking low at a rumble of thunder', 16, 'fibres', [
    k(.2,x=.4,y=-.7,eye='O'), k(.31,y=1.5,b=1,w=.7,v=.3,press=1,show=1,py=-2,straw=.8),
    k(.55,y=1.5,b=.9,eye='-',v=.3,press=.9), k(.73,x=.6,y=-.3,b=.1,eye='O'),
    k(.88,x=-.4,y=.5,b=.4)],when={'roof':True,'weather':'storm'})
routine('wind_brace', 'Holding the nest lining down in a gust', 19, 'strand', [
    k(.16,x=.7,y=-.6,show=1,px=-15,py=-5,turn=-1), k(.32,b=.7,w=.9,y=1,press=1,show=1,px=5,py=-10,turn=1),
    k(.5,b=.8,w=1,y=1.5,press=1,show=1,px=16,py=-4,turn=2), k(.7,y=1.6,x=.7,show=1,px=12,py=1,press=.8),
    k(.88,b=.4,eye='>')],when={'weather':'wind'},motive='care')
routine('cold_huddle', 'Burrowing down into the warm lining', 28, 'breath', [
    k(.16,x=-.5,y=.8,b=.4,straw=.4), k(.32,x=-.9,y=1.5,b=1,press=1,straw=.8,blanket=.2),
    k(.5,x=-.9,y=1.3,b=.8,eye='-',press=.9,show=.5,px=6,py=-4),
    k(.7,x=-1,y=1.5,b=1,eye='-',press=1,show=1,px=10,py=-7), k(.9,x=-.6,y=.9,b=.4,eye='-')],when={'temperature':'cold'},motive='rest')
routine('heat_fan', 'Fanning himself without giving up his comfortable spot', 22, 'air', [
    k(.15,y=-.4,w=.3,gape=.3), k(.29,w=1.2,gape=.5,show=1,px=12,py=-6),
    k(.43,w=.2,y=.3,gape=.4,show=.2), k(.57,w=1.2,y=-.3,gape=.5,show=1,px=16,py=-5,turn=1),
    k(.72,w=.2,gape=.3), k(.86,w=.9,show=.7,px=19,py=-4)],when={'temperature':'hot'})
routine('spring_feather', 'Catching a loose spring feather before it escapes', 19, 'feather', [
    k(.15,y=-.6,x=-.6,show=1,px=-17,py=-13), k(.32,y=-.8,x=.5,w=.5,show=1,px=0,py=-17,turn=1),
    k(.48,x=1,w=1,show=1,px=18,py=-10,turn=2), k(.65,x=.5,y=1.1,show=1,px=9,py=-2),
    k(.84,y=1.5,press=.4,show=.5,px=0,py=1,eye='^')],when={'season':'spring'},motive='curiosity')
routine('blossom_brush', 'Brushing spring petals out of the sleeping hollow', 16, 'petals', [
    k(.17,x=.6,y=1.4,show=1,px=0,py=-2), k(.35,w=.7,x=-.6,show=1,px=-9,py=-3,turn=1),
    k(.53,w=1.1,x=.5,show=1,px=16,py=-4,turn=2), k(.7,w=.3,y=-.5,show=1,px=24,py=0,turn=3),
    k(.87,y=.7,eye='^')],when={'season':'spring'},motive='care',effect={'tidiness':.015})
routine('summer_bug', 'Following a beetle around the nest rim', 25, 'beetle', [
    k(.15,u=-.4,x=-.5,y=1.4,show=1,px=-22,py=1), k(.32,u=-.25,y=1.7,show=1,px=-8,py=3),
    k(.5,u=.4,x=.8,y=1.5,show=1,px=12,py=3), k(.68,u=.6,x=1,y=.3,show=1,px=24,py=-3),
    k(.84,x=.7,y=-.6,show=1,px=27,py=-9,eye='O')],when={'season':'summer','time':'day'},motive='curiosity')
routine('dusk_firefly', 'Watching a firefly blink over the bedding', 27, 'firefly', [
    k(.16,x=-.7,y=-.8,show=.5,px=-22,py=-13), k(.34,x=.3,y=-1.2,show=1,px=-2,py=-20),
    k(.49,x=1,y=-.6,show=.2,px=22,py=-13), k(.65,x=.7,y=.2,show=1,px=18,py=-5),
    k(.82,x=-.5,y=-.6,w=.3,show=.6,px=-7,py=-16,eye='^')],when={'season':'summer','time':'night'},motive='curiosity')
routine('fall_leaf_catch', 'Catching an autumn leaf on the rim', 18, 'leaf', [
    k(.15,y=-.6,x=-.5,show=1,px=-21,py=-16,turn=-1), k(.32,y=-.8,x=.7,w=.6,show=1,px=5,py=-19,turn=1),
    k(.48,x=1,y=.6,w=1,show=1,px=18,py=-6,turn=2), k(.66,x=.4,y=1.6,show=1,px=8,py=0,turn=1),
    k(.84,y=.3,eye='^',show=.7,px=6,py=2)],when={'season':'fall'},motive='curiosity')
routine('acorn_roll', 'Rolling an acorn away from the soft spot', 21, 'acorn', [
    k(.18,x=-.6,y=1.5,show=1,px=-13,py=2), k(.34,x=.7,y=1.7,show=1,px=-2,py=2,turn=1),
    k(.49,x=.2,y=.5,show=1,px=12,py=3,turn=2), k(.65,u=.5,x=1,y=1.5,show=1,px=21,py=3,turn=3),
    k(.82,x=.7,y=.7,show=1,px=27,py=5,turn=4,eye='^')],when={'season':'fall'},motive='care',effect={'tidiness':.008})
routine('snow_shake', 'Shaking powdery snow off the outer rim', 17, 'snow', [
    k(.14,x=-.5,y=.8,show=1,px=-15,py=-2), k(.3,x=1,w=1,tail=1,show=1,px=9,py=-8,turn=1,straw=.7),
    k(.44,x=-1,w=.8,tail=-1,show=1,px=-13,py=-7,turn=2), k(.6,x=.8,w=.6,tail=1,show=1,px=21,py=1,turn=3),
    k(.8,y=.6,b=.4,press=.5,eye='>')],when={'season':'winter','snow':True},motive='care')
routine('frost_peck', 'Investigating the frost along the outer braid', 20, 'frost', [
    k(.18,u=.5,x=.8,y=1.1,show=1,px=20,py=1), k(.34,u=.6,x=1,y=1.8,show=1,px=20,py=1,gape=.3),
    k(.45,x=-.7,y=-.6,eye='O',show=1,px=22,py=-3,turn=1), k(.63,x=.5,y=.8,show=.7,px=20,py=2),
    k(.82,x=-.4,y=.5,w=.4,eye='>')],when={'season':'winter','temperature':'cold'},motive='curiosity')
routine('dawn_lookout', 'Rising over the rim to greet the morning', 23, 'none', [
    k(.15,x=-.6,y=1.1,b=.6,eye='-',press=.7), k(.32,y=-.7,b=-.3,v=-.15),
    k(.5,x=-.8,y=-.8,b=-.4,v=-.2), k(.66,x=1,y=-.7,w=.5,b=-.3,v=-.2),
    k(.83,y=-.4,w=.8,eye='^',gape=.4)],when={'time':'dawn'},motive='curiosity')
routine('noon_doze', 'Nodding off in the midday warmth', 26, 'breath', [
    k(.15,y=.5,eye='-'), k(.3,y=1.5,b=.5,eye='-',press=.5), k(.43,y=-.6,b=-.2,eye='O'),
    k(.58,y=.8,b=.5,eye='-',press=.5), k(.74,x=-.7,y=1.4,b=.7,eye='-',show=.5,press=.8),
    k(.91,x=-.8,y=1.3,b=.6,eye='-',show=.8,py=-4)],when={'time':'noon'},motive='rest')
routine('moon_watch', 'Watching moonlight from his nest', 28, 'none', [
    k(.18,y=-.6,x=.3), k(.36,y=-1.3,x=.8,w=.2), k(.54,y=-1.1,x=-.5,eye='^'),
    k(.72,y=-.5,x=.3,w=.4), k(.89,y=.7,b=.4,eye='-',press=.4)],when={'time':'night','weather':'clear'},motive='rest')
routine('bedtime_tuck', 'Drawing the soft lining close for the night', 25, 'fibres', [
    k(.16,y=1.3,x=-.7,show=.4,px=-12), k(.33,w=.7,y=.5,show=1,px=-3,py=-4,straw=.6,blanket=.5),
    k(.5,y=1.4,x=.7,show=.7,px=12,py=-1,blanket=.2), k(.67,w=.5,b=.7,press=.8,straw=.7,blanket=0),
    k(.84,x=-.8,y=1.4,b=.7,eye='-',press=.8)],when={'time':'night'},motive='rest')
routine('sniff_lining', 'Checking the nest lining with a skeptical little sniff', 15, 'fibres', [
    k(.2,x=.7,y=1.6,gape=.2,show=.3,px=7,py=0), k(.38,x=1,y=1.4,show=.5,px=8,py=-2),
    k(.53,x=-.8,y=-.4,eye='>'), k(.7,w=.7,show=1,px=16,py=-6,turn=1), k(.88,y=.7,eye='^')],motive='care')
routine('toe_trace', 'Tracing a tiny groove in the lining with one toe', 18, 'groove', [
    k(.18,l=1,y=1.5,show=.2,px=-7), k(.36,l=1,u=-.25,y=1.7,show=.6,px=-4,turn=1),
    k(.55,u=.25,r=1,y=1.7,show=1,px=4,turn=2), k(.73,y=.4,x=.4,show=1,px=7,turn=3),
    k(.88,y=-.3,w=.3,eye='^')],motive='curiosity')
routine('polish_pebble', 'Turning a smooth pebble before setting it beside the nest', 22, 'pebble', [
    k(.17,x=.7,y=1.5,show=1,px=10,py=1), k(.35,x=.8,y=.4,w=.4,show=1,px=9,py=-6,turn=1),
    k(.52,x=.5,y=-.4,w=.7,show=1,px=7,py=-8,turn=2), k(.69,u=.4,y=1.2,show=1,px=21,py=1,turn=3),
    k(.85,y=-.2,eye='^',show=1,px=24,py=3)],motive='curiosity')

# Explicit grip intervals tie picked-up material to the posed bill, across every
# body size. Before and after these intervals it follows the authored loose path.
for key, intervals in {
    'tuck_left_edge':[(.25,.61)], 'tuck_right_edge':[(.27,.63)],
    'lift_loose_twig':[(.26,.64)], 'crossbrace_twig':[(.22,.55)],
    'weave_rim':[(.18,.3),(.36,.45),(.51,.6)],
    'pick_grit':[(.26,.59)], 'straighten_feather':[(.26,.62)],
    'leaf_underlay':[(.23,.54)], 'mend_gap':[(.23,.43),(.51,.73)],
    'tighten_braid':[(.25,.65)], 'bored_twig_tap':[(.22,.74)],
    'spring_feather':[(.46,.7)], 'fall_leaf_catch':[(.45,.7)],
    'polish_pebble':[(.26,.65)],
}.items():
    ROUTINES[key]['grips'] = intervals

if __name__ == '__main__':
    target = Path(__file__).resolve().parents[1] / 'client/animation/nest-routines.json'
    target.write_text(json.dumps({'version':1, 'routines':ROUTINES}, indent=2) + '\n')
    print(f'Wrote {len(ROUTINES)} authored nest scores to {target}')
