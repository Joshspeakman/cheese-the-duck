"""Ponds v3: the 14 kept fish at their own quota (what only this fish allows: lure acts, species signature, duets, own fields) and the two pond hosts
(koi_pond, infinity_pool). The shared pond chores (leaves, ice, algae, flakes, bell) live on the hosts, not on the fish.
Every routine is hand-written; anchors are (column, row) of rep.py koi_pond / infinity_pool as fractions of the sprite."""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN
if os.environ.get('LENIENT'):  # draft mode: list every refusal instead of stopping at the first
    _r = Obj.r
    def _lenient(self, *a, **kw):
        try:
            _r(self, *a, **kw)
        except AssertionError as e:
            print('REFUSED', e)
    Obj.r = _lenient

COUNT = {}


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


def koi():
    o = Obj('koi', 'keeping', on='koi_pond', 
            parts=dict(shallow='the rippling shallow water along the front rim', pad='the lily pads floating on the water', stone='the front rim stones'),
            fields={'trick': (0, 0, 1), 'rhythm': (0, 0, 1)},
            physics=[('trick', 'rate', -0.0002, 'always'), ('rhythm', 'rate', -0.0004, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                call=[['rhythm', 'add', 0.4]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                kiss=[['subject.trust', 'add', 0.1], ['subject.mood', 'add', 0.15]],
                tickle=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                lead=[['trick', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                unsnag=[['subject.health', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            anchors=dict(
                shallow_l=(0.2353, 0.7818),
                shallow_m=(0.4874, 0.7455),
                shallow_r=(0.7395, 0.7091),
                pad_r=(0.7227, 0.6727),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364),
            ))
    o.r('net_leaves', 'Netting fallen leaves off the koi pond with a reed, drawing them in to the rim in two long sweeps', 22, 'reed',
        [k(.15, 'pad_r', reach=.7, x=.3, y=.2, w=.3), k(.35, 'shallow_m', reach=1, x=.5, y=.5, b=.3, mark='swsh'), k(.55, 'shallow_l', reach=1, x=.7, y=.6, b=.4, mark='swsh'), k(.78, 'stone_l', reach=.6, x=.2, y=.4, eye='^'), k(.9, eye='-')],
        [], g='care', act=('sweep', 'leaves'), prefer=['pond_leaves>.3', 'windy'],
        say=['Leaves out. Pond looks smug about it.', 'Fished out a lot of leaves. Zero fish. Fine.'])
    o.r('draw_a_weed_off_the_fin', "Slowly pulling a trailing strand of weed off the shy koi's fin with the tip of his bill", 22, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'shallow_l', x=1.2, y=1.3, b=.8, eye='-'), k(.5, 'shallow_l', x=1.1, y=1.5, b=1, l=1, mark='tug'), k(.7, 'shallow_l', x=.5, y=.7, b=.5, w=.4, mark='plip'), k(.88, eye='^')],
        [(0.5, 'unsnag')], g='care', act=('pull', 'weed'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.25, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Weed off. Koi blinked. Gratitude, I think.', 'You had a salad on your fin. Hold still.'])
    o.r('hand_feed_the_hungriest', 'Carrying a single flake in his bill just at the surface until the hungriest koi rises and takes it', 20, 'none',
        [k(.12, x=.9, y=.4, b=.8), k(.3, 'shallow_l', x=1.2, y=1.6, b=1, eye='o', mark='...'), k(.5, 'shallow_l', x=1.1, y=1.8, b=1.1, eye='O', mark='gulp'), k(.72, 'shallow_l', x=.5, y=.6, b=.4, w=.4, eye='^'), k(.9, eye='-')],
        [(0.5, 'feed')], g='use', act=('carry', 'flake'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1}), (0.78, {'lure': 0})],
        say=['Took it right out of my bill. Eight out of ten, rude.', 'Hand-fed a koi. Trust me. Mostly its.'])
    o.r('let_the_shy_one_kiss_his_bill', 'Tapping his bill to the water so the shy koi comes up and kisses the tip of it', 20, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_m', x=1.3, y=1.4, b=.9, eye='-', mark='...'), k(.5, 'shallow_m', x=1.4, y=1.6, b=1, eye='-', mark='mwah'), k(.72, 'shallow_m', x=.8, y=.9, b=.6, eye='^'), k(.9, eye='-')],
        [(0.5, 'kiss')], g='use', act=('tap', 'lips'), prefer=['fish_trust<.8', 'happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Fish lips. Very wet. Ten out of ten.', 'It kissed me and left. Story of my life.'])
    o.r('tickle_its_chin_with_a_wing_tip', 'Patting the koi under its chin with the tip of a wing while it hangs still at the surface', 20, 'wing',
        [k(.12, 'shallow_m', reach=.5, x=.3, y=.8, b=.5), k(.3, 'shallow_m', reach=1, x=.5, y=1.2, b=.9, mark='tck'), k(.5, 'shallow_m', reach=1, x=.5, y=1.3, b=1, r=1, mark='tck tck'), k(.72, 'shallow_m', reach=.6, x=.3, y=.8, b=.6), k(.9, eye='^')],
        [(0.5, 'tickle')], g='use', act=('pat', 'chin'), pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('walk_the_rim_with_a_wing_trailing', 'Walking the rim with a wing trailing at the surface and the koi chasing the wingtip all the way', 26, 'wing',
        [k(.1, 'shallow_l', reach=.6, x=.2, y=.7, b=.4), k(.28, 'shallow_m', reach=1, x=.4, y=1.1, b=.9, l=1), k(.5, 'shallow_r', reach=1, x=.5, y=.8, b=.5, r=1), k(.7, 'shallow_m', reach=1, x=.4, y=.8, b=.5, l=1), k(.9, eye='^')],
        [(0.5, 'lead')], g='play', act=('chase', 'wingtip'), pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.75, {'lure': 1})],
        say=['It followed me the whole length. That is a first.', 'Led a fish on a wing. I am a very small parade.'])
    o.r('hold_a_reed_ring_at_the_surface', 'Hooking a reed bent into a ring just at the surface until the koi noses at it, once, twice', 24, 'reed',
        [k(.12, 'shallow_r', reach=.5, x=.3, y=.4, b=.4), k(.3, 'shallow_r', reach=1, x=.5, y=.8, b=.7), k(.5, 'shallow_r', reach=1, x=.5, y=.8, b=.8, l=1, mark='plip'), k(.7, 'shallow_r', reach=1, x=.4, y=.7, b=.7, r=1, mark='plip'), k(.9, eye='^')],
        [(0.5, 'lead')], g='show', act=('hook', 'ring'), prefer=['curious', 'trick<.7'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('drum_the_three_stones_in_turn', 'Drumming the three front stones in turn, left to right, to teach the koi the dinner call', 22, 'none',
        [k(.1, 'stone_l', x=1.2, y=1.3, b=.5, mark='tok'), k(.3, 'stone_m', x=1.2, y=1.3, b=.5, l=1, mark='tok'), k(.5, 'stone_r', x=1.3, y=1.3, b=.5, r=1, mark='tok'), k(.7, 'stone_m', x=1.2, y=1.4, b=.6, mark='TOK'), k(.9, eye='^')],
        [(0.5, 'call')], g='use', act=('drum', 'stones'), when=['rhythm<.6'], pick='hungriest',
        obj=[(0.6, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('race_the_koi_along_the_rim', 'Having a race with the koi along the rim, sprinting from the left stones to the right while it keeps pace in the water', 20, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.3, 'shallow_m', x=1.2, y=.4, b=-.5, r=1, w=.5), k(.5, 'shallow_r', x=1.3, y=.4, b=-.6, l=1, w=.6), k(.72, 'shallow_r', x=.6, y=.5, b=.6, eye='O', mark='whew'), k(.9, eye='^')],
        [(0.5, 'fun')], g='play', act=('race', 'koi'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.35, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Lost by a fin. Rigged. Fish cut corners.', "Race over. The koi wasn't even trying."])
    o.r('blow_bubbles_at_the_surface', 'Blowing bubbles at the surface until the koi blows a few back at him', 20, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_l', x=1.2, y=1.4, b=.9, mark='blub'), k(.5, 'shallow_l', x=1.3, y=1.5, b=1, l=1, mark='blub blub'), k(.7, 'shallow_l', x=1.1, y=1.3, b=.9, eye='O', mark='blub'), k(.88, eye='^')],
        [(0.5, 'tickle')], g='play', act=('blow', 'bubbles'), prefer=['happy', 'young'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Bubble conversation. Mostly it won.', 'Blub. Blub. It said blub. Excellent.'])
    o.r('watch_the_shadow_glide_in', "Leaning out over the rim to peer at the koi's shadow glide in past the pad, nose up, eyes wide", 20, 'none',
        [k(.12, x=.5, y=.6, b=.4), k(.3, 'shallow_m', x=1, y=.9, b=.8, eye='o'), k(.52, 'shallow_m', x=1.2, y=1.1, b=.9, eye='O', mark='...'), k(.74, 'shallow_m', x=.5, y=.5, b=.4, w=.4, eye='^'), k(.9, eye='-')],
        [], g='test', act=('peer', 'shadow'), prefer=['curious'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.6, {'lure': 1})],
        say=['A big orange shadow. Mine now, spiritually.', 'Looks like a coin with ambitions.'])
    o.r('squint_at_two_reflections', "Squinting at his own reflection and the koi's side by side in the water, comparing the fashion", 20, 'none',
        [k(.15, x=.4, y=.7, b=.4), k(.35, 'shallow_l', x=1, y=1.5, b=1, eye='O'), k(.55, 'shallow_l', x=1.1, y=1.6, b=1.1, l=1, eye='>', mark='hm'), k(.76, 'shallow_l', x=.8, y=1, b=.6, w=.5, eye='^'), k(.9, eye='-')],
        [], g='test', act=('compare', 'reflection'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.7, {'lure': 1})],
        say=['I have the better bill. It has the better coat.', 'Two pretty faces. One of them is mine.'])
    o.r('wait_for_a_koi_to_rise', 'Waiting with his bill an inch above the water for a koi to rise and look at him', 24, 'none',
        [k(.15, 'stone_m', x=.8, y=.9, b=.6, eye='o'), k(.4, 'stone_m', x=1.4, y=1.7, b=1.5, eye='o'), k(.65, 'stone_m', x=1.9, y=2.2, b=2, eye='O', mark='...'), k(.85, x=.1, y=.2, b=.3, eye='-')],
        [], g='rest', act=('wait', 'surface'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.3, {'lure': 0}), (0.55, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Come up. Say hello. No? Fine.', 'Waited. It rose. It looked. I won.'])
    o.r('argue_with_the_koi_over_the_flakes', 'Arguing with the koi over the last flake, jabbing his bill at the water and being ignored', 18, 'none',
        [k(.15, x=.7, y=.4, b=.4, eye='>'), k(.3, 'shallow_r', x=1.4, y=1.2, b=.8, w=.7, mark='MINE'), k(.5, x=-.3, y=.3, b=.6, l=1, r=1), k(.7, 'shallow_r', x=1.5, y=1.3, b=.9, w=1, mark='MINE!'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'koi'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It ate it. I said it was mine. It heard nothing.', 'Argued with a fish. Lost on volume.'])
    o.r('sing_the_koi_a_slow_song', 'Singing the koi a slow song from the rim, a wing over his heart, while it hangs listening', 24, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, 'shallow_m', reach=1, x=.3, y=.8, b=.5, w=.4, mark='laaa'), k(.5, 'shallow_m', reach=1, x=.4, y=.9, b=.6, w=.5, l=1, mark='LAAA'), k(.7, 'shallow_m', reach=1, x=.3, y=.7, b=.5, r=1, mark='la'), k(.88, eye='^')],
        [(0.5, 'cheer')], g='show', act=('sing', 'koi'), prefer=['happy', 'lonely'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=["It listens. It hasn't left. That is a review.", 'A love song for a fish. I would do it again.'])
    o.r('bill_caught_in_a_koi_s_hungry_mouth', 'Dipping a bill to the surface and getting stuck as the koi clamps on, hauling him down the rim until it lets go', 22, 'none',
        [k(.15, 'stone_l', x=.8, y=.9, b=.6), k(.32, 'stone_l', x=1.3, y=1.6, b=1, eye='O', mark='mmf'), k(.5, 'stone_l', x=.6, y=1.9, b=1.6, l=1, eye='@', mark='mrrf'), k(.68, 'stone_l', x=-.5, y=1.1, b=.8, r=1, w=1, mark='POP'), k(.86, x=-.8, y=.4, b=.5, eye='>')],
        [], g='mishap', act=('stuck', 'bill'), prefer=['young', 'grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1}), (0.7, {'lure': 0})],
        say=['It has a mouth like a hoover. Bill: stuck. Dignity: gone.', 'Let go! It did. Eventually. Hostile fish.'])
    o.r('leap_back_from_a_sudden_splash', 'Hopping back from a sudden splash as the koi surges up, landing on his tail with wings flung wide', 16, 'none',
        [k(.15, 'stone_r', x=.8, y=.9, b=.6), k(.3, 'stone_r', x=-.2, y=-.8, b=-1.3, w=1, eye='O', mark='WAH'), k(.5, x=-1.2, y=-1.2, b=-1.6, w=1, l=1, r=1, eye='@'), k(.72, x=-.4, y=.9, b=1.1, w=.4, eye='>', mark='plop'), k(.9, eye='-')],
        [], g='mishap', act=('hop', 'back'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.45, {'lure': 1})],
        say=['It attacked. A fish. It attacked me.', 'Splashed. Jumped. Pretended I meant to.'])
    o.r('count_the_koi_with_a_friend', 'Counting the koi one by one with a friend leaning over the rim beside him, and arguing the total', 22, 'none',
        [k(.12, x=.5, y=.5, b=.4), k(.3, 'shallow_l', x=1, y=1.2, b=.8, mark='one'), k(.5, 'shallow_m', x=1.1, y=1.3, b=.9, l=1, mark='two'), k(.7, 'shallow_m', x=.9, y=1.1, b=.8, eye='>', mark='THREE'), k(.88, eye='-')],
        [], g='test', act=('count', 'koi'), prefer=['curious', 'happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})],
        duo=[k(.15, x=.5, y=.5, b=.4), k(.35, 'shallow_r', x=1.1, y=1.2, b=.8, mark='one'), k(.55, 'shallow_m', x=1.1, y=1.3, b=.9, r=1, mark='FOUR'), k(.75, 'shallow_m', x=.9, y=1.1, b=.8, eye='>', mark='no'), k(.9, eye='-')])
    o.r('herd_the_koi_from_both_ends_of_the_rim', 'Chasing the koi along the rim from the left while a friend runs from the right, the koi caught between them', 24, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.3, 'shallow_l', x=1.3, y=.4, b=-.5, r=1, w=.5), k(.5, 'shallow_r', x=1.4, y=.4, b=-.6, l=1, w=.6), k(.7, 'shallow_r', x=.6, y=.6, b=.6, eye='O', mark='gotcha'), k(.88, eye='^')],
        [], g='play', act=('chase', 'koi'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.15, {'lure': 1}), (0.4, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Pincer movement. Koi slipped away. Embarrassing.', 'We herded one fish for ten minutes. We won.'],
        duo=[k(.1, 'shallow_r', x=.6, y=.5, b=.6, r=1), k(.3, 'shallow_r', x=1.3, y=.4, b=-.5, l=1, w=.5), k(.5, 'shallow_r', x=1.4, y=.4, b=-.6, r=1, w=.6), k(.7, 'shallow_r', x=.6, y=.6, b=.6, eye='O', mark='gotcha'), k(.88, eye='^')])
    o.r('shade_the_koi_from_the_noon_glare', 'Cooling the koi with the shade of a spread wing held out over the water at noon', 20, 'wing',
        [k(.12, 'shallow_r', reach=.5, x=.3, y=.6, b=.4), k(.3, 'shallow_r', reach=1, x=.4, y=.7, b=.5, w=.9), k(.55, 'shallow_r', reach=1, x=.3, y=.8, b=.6, w=1, l=1, mark='shh'), k(.78, 'shallow_r', reach=.6, x=.2, y=.5, w=.4, eye='^'), k(.9, eye='-')],
        [(.55, 'cheer')], g='weather', act=('cool', 'koi'), when=['sun'], pick='hungriest',
        obj=[(.25, {'lure': 1}), (.6, {'lure': 1}), (.8, {'lure': 0})], say=['It sat in my shadow. The sun lost.', 'A wing is a parasol if you are brave.'])
    return o


def goldfish():
    o = Obj('goldfish', 'keeping', on='koi_pond', 
            parts=dict(shallow='the rippling shallow water along the front rim', pad='the lily pads floating on the water', tuft='the grass tuft at the pond foot', reed='the reed stems at the pond edge', stone='the front rim stones'),
            fields={'learned': (0, 0, 1)},
            physics=[('learned', 'rate', -0.0003, 'always')],
            effects=dict(
                unsnag=[['subject.health', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                call=[['learned', 'add', 0.35]],
                feed=[['subject.hunger', 'add', -0.2], ['subject.trust', 'add', 0.1]],
                tickle=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                lead=[['learned', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            anchors=dict(
                shallow_l=(0.2353, 0.7818),
                shallow_m=(0.4874, 0.7455),
                shallow_r=(0.7395, 0.7091),
                pad_r=(0.7227, 0.6727),
                tuft=(0.0924, 0.8),
                reed_low=(0.0672, 0.6909),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364),
            ))
    o.r('untangle_the_line_from_its_tail', "Unwrapping a thread of pond weed from the goldfish's fan tail with a patient bill, one twist at a time", 24, 'none',
        [k(.12, x=.4, y=.5, b=.5), k(.3, 'shallow_m', x=1, y=1.4, b=1, eye='-'), k(.5, 'shallow_m', x=1.1, y=1.6, b=1.1, l=1, mark='tweak'), k(.7, 'shallow_m', x=.5, y=.7, b=.5, w=.4, mark='plip'), k(.88, eye='^')],
        [(0.5, 'unsnag')], g='care', act=('unwrap', 'tail'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.25, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('tap_the_surface_for_the_dinner_call', 'Tapping the surface with his bill to the dinner call, twice quick and once slow, until the goldfish learn it', 20, 'none',
        [k(.12, 'shallow_l', x=1.3, y=1.4, b=.8, mark='tp'), k(.26, 'shallow_l', x=1.3, y=1.4, b=.8, l=1, mark='tp'), k(.42, x=-.2, y=-.2, b=-.2, w=.3), k(.58, 'shallow_l', x=1.4, y=1.5, b=.9, r=1, mark='TAP'), k(.85, eye='^')],
        [(0.58, 'call')], g='use', act=('tap', 'surface'), when=['learned<.7'], prefer=['dusk', 'dawn'], pick='hungriest',
        obj=[(0.4, {'lure': 0}), (0.65, {'lure': 1})],
        say=['Tap tap tap. They are learning. One of them is.', 'A call. Dinner. They remember for a whole minute.'])
    o.r('dangle_a_flake_and_snatch_it_back', 'Showing a flake at the surface, letting the goldfish rise for it, then snatching it up and showing it again', 22, 'none',
        [k(.12, 'shallow_r', x=.8, y=.9, b=.6), k(.28, 'shallow_r', x=1.2, y=1.4, b=1, eye='o', mark='...'), k(.42, 'shallow_r', x=.2, y=-.4, b=-.5, w=.5, eye='>', mark='nope'), k(.58, 'shallow_r', x=1.3, y=1.6, b=1.1, eye='O'), k(.78, 'shallow_r', x=.6, y=.8, b=.5, eye='^', mark='gulp')],
        [(0.78, 'feed')], g='use', act=('show', 'flake'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.45, {'lure': 0}), (0.55, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Nope. Again. Nope. Fine, take it.', 'I am the dinner service. With a sense of humour.'])
    o.r('let_it_nibble_the_tip_of_his_bill', 'Letting the goldfish tap-tap-nibble the very tip of his bill, holding still and trying not to laugh', 20, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'shallow_m', x=1.4, y=1.6, b=1.1, eye='-'), k(.5, 'shallow_m', x=1.4, y=1.7, b=1.2, l=1, eye='-', mark='ti hi'), k(.7, 'shallow_m', x=1.2, y=1.5, b=1, r=1, w=.3, eye='>'), k(.88, eye='^')],
        [(0.5, 'tickle')], g='use', act=('tap', 'bill'), prefer=['happy', 'lonely'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Nibbles. Little ones. I am a very long snack.', 'Tickles. Do not tell anyone I laughed.'])
    o.r('trail_a_wing_so_it_zigzags_after_it', 'Dragging a wing along the surface so the goldfish zigzags after the tip, left, right, left again', 24, 'wing',
        [k(.1, 'shallow_l', reach=.6, x=.2, y=.6, b=.4), k(.26, 'shallow_m', reach=1, x=.4, y=.7, b=.5, l=1), k(.42, 'shallow_l', reach=1, x=.3, y=.7, b=.5, r=1), k(.58, 'shallow_r', reach=1, x=.5, y=.7, b=.5, l=1), k(.76, 'shallow_m', reach=1, x=.4, y=.7, b=.5), k(.9, eye='^')],
        [(0.58, 'lead')], g='use', act=('drag', 'wing'), when=['learned<.8'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.45, {'lure': 1}), (0.6, {'lure': 1}), (0.78, {'lure': 1})])
    o.r('count_the_flakes_by_the_snatches', 'Dropping flakes one by one and counting each snatch aloud until the goldfish stops being hungry', 24, 'none',
        [k(.12, 'pad_r', x=.7, y=.8, b=.5, mark='1'), k(.3, 'pad_r', x=.9, y=1, b=.7, l=1, mark='2'), k(.5, 'pad_r', x=1, y=1.1, b=.8, mark='3'), k(.7, 'pad_r', x=1.1, y=1.2, b=.9, r=1, mark='4'), k(.88, eye='-', mark='ten')],
        [(0.5, 'feed')], g='test', act=('count', 'flakes'), when=['fish_hunger>.5'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Eight flakes. It always wants nine.', 'Counted. Fed. Insatiable. I know the feeling.'])
    o.r('hoist_a_flake_for_it_to_leap_at', 'Lifting a flake up high between his bill tips so the goldfish has to leap clear of the water for it', 22, 'none',
        [k(.12, 'shallow_l', x=.6, y=.5, b=.5), k(.3, 'shallow_l', x=.5, y=-.7, b=-.5, eye='o'), k(.5, 'shallow_l', x=.6, y=-1, b=-.8, eye='O', mark='hup'), k(.7, 'shallow_l', x=.8, y=.3, b=.4, w=.5, eye='^', mark='gulp'), k(.9, eye='-')],
        [(0.7, 'feed')], g='show', act=('lift', 'flake'), when=['fish_hunger>.4'], ages=GROWN, pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 0})],
        say=['Jumped. A tiny fish. A tiny, majestic fish.', 'It got air. I got a flake-shaped hole in my pride.'])
    o.r('weave_a_wing_between_the_stems', 'Chasing the goldfish with a wing, weaving between the stems of the reeds at the pond edge, the goldfish threading after it', 22, 'wing',
        [k(.1, 'reed_low', reach=.6, x=.2, y=.5, b=.3), k(.3, 'tuft', reach=1, x=.4, y=.8, b=.6, r=1), k(.5, 'reed_low', reach=1, x=.3, y=.7, b=.5, l=1), k(.7, 'shallow_l', reach=1, x=.5, y=.7, b=.6), k(.88, eye='^')],
        [(0.7, 'lead')], g='show', act=('chase', 'stems'), when=['learned<.8'], pick='hungriest',
        obj=[(0.15, {'lure': 1}), (0.35, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('play_red_light_green_light_along_the_rim', 'Playing a race of red light, green light with the goldfish, dashing along the rim and freezing the moment it freezes', 24, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.26, 'shallow_m', x=1.2, y=.3, b=-.5, r=1, w=.5), k(.4, 'shallow_m', x=.3, y=.2, b=.2, w=.2, eye='O', mark='red!'), k(.56, 'shallow_r', x=1.3, y=.3, b=-.6, l=1, w=.6), k(.72, 'shallow_r', x=.3, y=.2, b=.2, eye='O', mark='RED!'), k(.9, eye='^')],
        [(0.56, 'fun')], g='play', act=('race', 'goldfish'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.74, {'lure': 1})],
        say=['It froze first. I moved. It is cheating by being a fish.', 'Green light. Red light. It won. It always wins.'])
    o.r('hop_the_stones_in_time_with_its_darts', "Hopping along the front stones in time with the goldfish's darts, one hop to each dash", 22, 'none',
        [k(.1, 'stone_l', x=.3, y=.4, b=-.6, l=1), k(.28, 'stone_m', x=.4, y=.4, b=-.9, r=1, w=.4), k(.46, 'stone_m', x=.3, y=.4, b=-.6, l=1), k(.64, 'stone_r', x=.4, y=.4, b=-.9, r=1, w=.5), k(.84, 'stone_r', x=.3, y=.3, b=-.5, eye='^')],
        [], g='play', act=('hop', 'stones'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('drum_the_ripples_back_and_forth', 'Drumming the rippling surface with his bill and watching the goldfish dart in over each ring', 20, 'none',
        [k(.12, 'stone_r', x=1.2, y=1.3, b=.6, mark='ba'), k(.3, 'stone_m', x=1.2, y=1.3, b=.6, l=1, mark='da'), k(.48, 'tuft', x=1.3, y=1.4, b=.7, r=1, mark='ba'), k(.66, 'stone_m', x=1.3, y=1.4, b=.7, mark='DUM'), k(.86, eye='^')],
        [], g='play', act=('drum', 'ripples'), prefer=['happy', 'young'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.35, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('peer_close_at_its_scales', "Peering close at the goldfish's scales as it hangs at the surface, trying to see where one ends", 20, 'none',
        [k(.12, x=.5, y=.6, b=.4), k(.3, 'shallow_l', x=1, y=1.2, b=.8, eye='o'), k(.5, 'shallow_l', x=1.2, y=1.5, b=1, eye='O', mark='...'), k(.72, 'shallow_l', x=.6, y=.6, b=.5, w=.4, eye='^'), k(.9, eye='-')],
        [], g='test', act=('peer', 'scales'), prefer=['curious'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('hold_up_a_tail_feather_to_compare_tails', "Holding up a tail feather of his own beside the goldfish's fan tail to compare which is the better tail", 20, 'wing',
        [k(.12, 'shallow_m', reach=.5, x=.3, y=.4, b=.3), k(.3, 'shallow_m', reach=1, x=.3, y=.8, b=.8, w=.4, l=1), k(.5, 'shallow_r', reach=1, x=.4, y=.7, b=.7, w=.6, r=1, mark='hm'), k(.72, 'shallow_r', reach=.6, x=.2, y=.5, b=.4, w=.3, eye='>'), k(.9, eye='^')],
        [], g='test', act=('compare', 'tails'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('wait_for_it_to_remember_him', 'Waiting at the rim for the goldfish to remember who he is, with an expectant nod each time it surfaces', 26, 'none',
        [k(.15, 'shallow_m', x=.8, y=.9, b=.6, eye='o'), k(.4, 'shallow_m', x=1.2, y=1.1, b=.9, eye='O', mark='hi'), k(.62, 'shallow_m', x=.8, y=.8, b=.6, eye='-', mark='...'), k(.82, 'shallow_m', x=1.3, y=1.2, b=1, eye='O', mark='HI')],
        [], g='rest', act=('wait', 'goldfish'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.55, {'lure': 0}), (0.8, {'lure': 1})],
        say=['Hi. No? Hi again. Third time, it knows me.', 'It forgets me every lap. I am introduced forever.'])
    o.r('cool_his_feet_while_it_nibbles_his_toes', 'Cooling his feet at the rim on a hot day while the goldfish noses at his toes', 24, 'none',
        [k(.12, x=.2, y=.3, b=.5, l=1), k(.32, 'stone_l', x=.3, y=1.2, b=1.2, l=1, eye='-', mark='ahh'), k(.54, 'stone_l', x=.3, y=1.4, b=1.4, r=1, eye='-', mark='ti hi'), k(.76, 'stone_l', x=.2, y=1, b=1, l=1, eye='>', mark='heh'), k(.9, eye='^')],
        [], g='weather', act=('cool', 'feet'), when=['sun'], prefer=['warm', 'happy'], pick='shyest',
        obj=[(0.32, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Cool feet. A nibble. Do not tell my toes.', 'Toe-nibbling. The sign said nothing about teeth. Great.'])
    o.r('argue_with_the_goldfish_about_its_memory', 'Arguing with the goldfish about its memory, wing jabbing, and getting no answer at all', 20, 'none',
        [k(.15, x=.6, y=.4, b=.4, eye='>'), k(.3, 'stone_m', x=1.3, y=1.3, b=.8, w=.8, mark='REMEMBER'), k(.5, x=-.3, y=.3, b=.6, l=1, r=1), k(.7, 'stone_m', x=1.4, y=1.4, b=.9, w=1, mark='ME!'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'goldfish'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=["I fed you at noon. You said thanks. You don't remember.", 'It has no idea who I am. Good fight.'])
    o.r('sing_the_goldfish_a_lullaby_in_threes', 'Singing the goldfish a lullaby in threes, since that is all it will remember, one verse at a time', 24, 'none',
        [k(.12, x=.2, y=.3, b=.3), k(.3, 'shallow_r', x=.8, y=.7, b=.5, mark='la'), k(.5, 'shallow_r', x=.9, y=.8, b=.6, l=1, w=.3, mark='la la'), k(.7, 'shallow_r', x=.8, y=.7, b=.5, r=1, w=.4, mark='la la la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'goldfish'), prefer=['sad', 'lonely'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Three verses. It remembers none. The song is a gift.', 'Soft song. Soft fish. Mine, for three seconds.'])
    o.r('hop_up_when_it_nips_a_toe', 'Hopping up with a yelp when the goldfish nips one toe, then glaring at the water', 16, 'none',
        [k(.15, 'stone_r', x=.3, y=.8, b=.6, l=1), k(.32, 'stone_r', x=-.3, y=-.6, b=-1.2, w=.9, l=1, eye='O', mark='YIP'), k(.5, x=-.5, y=-.8, b=-1.4, w=1, l=1, r=1, eye='@'), k(.72, x=.5, y=.9, b=.9, l=1, eye='>', mark='huh')],
        [], g='mishap', act=('hop', 'toes'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.4, {'lure': 1})],
        say=['It bit my toe. It is the size of a thumb.', 'Nipped. By a flake-sized monster.'])
    o.r('ring_dance_round_the_pond_with_a_friend', 'Dancing a ring round the pond edge with a friend, hop and swap, the goldfish circling to match', 26, 'none',
        [k(.1, 'stone_l', x=.3, y=.4, b=-.6, l=1), k(.28, 'shallow_l', x=.4, y=.4, b=-.9, r=1, w=.5), k(.46, 'shallow_m', x=.3, y=.4, b=-.6, l=1, w=.6, mark='la'), k(.64, 'stone_r', x=.4, y=.4, b=-.9, r=1, w=.5), k(.84, 'stone_r', x=.3, y=.3, b=-.5, eye='^')],
        [], g='play', act=('dance', 'rim'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.54, {'lure': 1}), (0.72, {'lure': 1})],
        duo=[k(.1, 'stone_r', x=.3, y=.4, b=-.6, r=1), k(.28, 'shallow_r', x=.4, y=.4, b=-.9, l=1, w=.5), k(.46, 'shallow_m', x=.3, y=.4, b=-.6, r=1, w=.6), k(.64, 'stone_l', x=.4, y=.4, b=-.9, l=1, w=.5), k(.84, 'stone_l', x=.3, y=.3, b=-.5, eye='^')])
    o.r('search_the_pads_together_for_the_goldfish', 'Seeking through the pads together for a goldfish that has gone missing, a wing on every stem', 24, 'wing',
        [k(.12, 'shallow_r', reach=.5, x=.3, y=.4, b=.4), k(.3, 'pad_r', reach=1, x=.6, y=.2, b=.5, eye='o'), k(.5, 'pad_r', reach=1, x=.7, y=.1, b=.7, l=1, eye='O', mark='huh'), k(.7, 'shallow_r', reach=1, x=.5, y=.4, b=.5, r=1, eye='>'), k(.88, eye='^', mark='there')],
        [], g='test', act=('seek', 'goldfish'), prefer=['curious'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Found it. It was right there. It was always right there.', 'Two ducks, one fish, one hide and seek that it did not agree to.'],
        duo=[k(.15, 'shallow_m', reach=.5, x=.3, y=.4, b=.4), k(.34, 'pad_r', reach=1, x=.6, y=.2, b=.5, r=1), k(.54, 'pad_r', reach=1, x=.5, y=.3, b=.6, eye='o'), k(.74, 'shallow_r', reach=1, x=.5, y=.4, b=.5, l=1), k(.9, eye='^')])
    return o


def catfish():
    o = Obj('catfish', 'keeping', on='koi_pond', 
            parts=dict(bed='the water over the pond bed', pad='the lily pads floating on the water', bank='the stone bank round the pond', edge='the far edge of the water', stone='the front rim stones'),
            fields={'feel': (0, 0, 1)},
            physics=[('feel', 'rate', -0.0003, 'always')],
            effects=dict(
                ease=[['subject.trust', 'add', 0.12]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                read=[['feel', 'add', 0.25], ['subject.trust', 'add', 0.1]],
                lead=[['feel', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            anchors=dict(
                bed_l=(0.2353, 0.7818),
                bed_m=(0.4874, 0.7455),
                bed_r=(0.7395, 0.7091),
                pad_low=(0.7227, 0.6727),
                bank_r=(0.7983, 0.7273),
                edge_far=(0.5882, 0.7818),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
            ))
    o.r('unwind_a_weed_thread_from_a_barbel', 'Unwrapping a thread of weed from one barbel, whisker by whisker, with the very tip of his bill', 24, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'bed_l', x=1.1, y=1.7, b=.9, eye='-'), k(.48, 'bed_l', x=1.3, y=1.9, b=1.2, l=1, mark='tug'), k(.66, 'bed_l', x=.9, y=1.3, b=.8, r=1, mark='plip'), k(.84, y=.2, w=.3, eye='^')],
        [(0.48, 'tend')], g='care', act=('unwrap', 'barbel'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Off. It sat still for the whole thing. Brave, or asleep.', 'Whisker one, whisker two. Cat is spotless now, weirdly.'])
    o.r('comb_the_silt_from_the_barbels', 'Grooming silt out of the long whiskers with the flat of a wing while the cat holds its chin to the rim', 22, 'wing',
        [k(.12, 'bed_m', reach=.5, x=.2, y=.9, b=.5), k(.3, 'bed_m', reach=1, x=.4, y=1.5, b=1.1, mark='scrt'), k(.5, 'bed_m', reach=1, x=.3, y=1.7, b=1.3, l=1, r=1, mark='scrt'), k(.7, 'bed_m', reach=1, x=.3, y=1.4, b=1, mark='scrt'), k(.88, eye='^')],
        [(0.5, 'tend')], g='care', act=('groom', 'barbels'), prefer=['fish_health<.9', 'happy'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('hold_a_pellet_to_the_hungriest_cat', 'Carrying one pellet in his bill, dangling it just above the deep edge until the hungriest cat sucks it in', 20, 'none',
        [k(.12, x=.4, y=.6, b=.5), k(.3, 'bed_l', x=1.3, y=1.7, b=1, eye='o', mark='...'), k(.5, 'bed_l', x=1.2, y=1.9, b=1.2, eye='O', mark='slurp'), k(.72, 'bed_l', x=.6, y=.8, b=.5, w=.4, eye='^'), k(.9, eye='-')],
        [(0.5, 'feed')], g='use', act=('carry', 'pellet'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1}), (0.78, {'lure': 0})],
        say=['Whole pellet, no chewing. A cat that trusts the system.', 'That mouth could take my bill off. It chose not to.'])
    o.r('press_a_wingtip_for_it_to_read', 'Pressing one wingtip flat on the water so the cat reads it with its whiskers, tip to heel', 22, 'wing',
        [k(.12, 'bed_m', reach=.5, x=.2, y=.6, b=.4), k(.3, 'bed_m', reach=1, x=.3, y=1, b=.8, mark='...'), k(.5, 'edge_far', reach=1, x=.4, y=1.1, b=.9, r=1, mark='hm'), k(.7, 'bed_m', reach=1, x=.3, y=1, b=.8), k(.9, eye='^')],
        [(0.5, 'read')], g='use', act=('press', 'wingtip'), when=['feel<.7'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('draw_the_cat_along_the_floor_row', 'Dragging a wingtip along the water over the deep row so the cat feels its way after it, left to right', 26, 'wing',
        [k(.1, 'bed_l', reach=.6, x=.2, y=.7, b=.4), k(.28, 'bed_m', reach=1, x=.4, y=.9, b=.5, l=1), k(.5, 'edge_far', reach=1, x=.5, y=.9, b=.6, r=1), k(.7, 'bed_r', reach=1, x=.5, y=.9, b=.6, l=1), k(.9, eye='^')],
        [(0.5, 'lead')], g='use', act=('drag', 'wingtip'), when=['feel<.8'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Followed me blind, the whole way. Lovely, trusting idiot.', 'Led a cat by the wing. I do not follow.'])
    o.r('stroke_the_flat_head_with_a_wing', "Patting the cat's broad flat head with the back of a wing as it rests its chin at the rim", 20, 'wing',
        [k(.12, 'bed_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'bed_l', reach=1, x=.3, y=1.4, b=1.1, mark='pat'), k(.5, 'bed_l', reach=1, x=.2, y=1.5, b=1.3, l=1, mark='pat pat'), k(.7, 'bed_l', reach=1, x=.3, y=1.3, b=1), k(.9, eye='^')],
        [(0.5, 'stroke')], g='use', act=('pat', 'head'), prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('race_the_cat_along_the_bank', 'Having a race with the cat along the right bank at a bounding trot, the whiskers just keeping up', 20, 'none',
        [k(.1, 'bed_l', x=.5, y=.5, b=.4), k(.28, 'bed_m', x=1, y=.6, b=-.5, l=1, w=.5), k(.46, 'edge_far', x=1.2, y=.6, b=-.7, r=1, w=.7, mark='hup'), k(.64, 'bed_r', x=1.3, y=.6, b=-.5, l=1, w=.5), k(.84, 'bank_r', x=.3, y=.4, b=.3, eye='@')],
        [(0.46, 'fun')], g='play', act=('race', 'bank'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Lost, narrowly. It does not even use legs.', 'Cat won by a barbel. I want a recount.'])
    o.r('blow_bubbles_down_to_it', 'Blowing a string of bubbles into the water so the cat noses up through the rising beads', 18, 'none',
        [k(.12, x=.3, y=.6, b=.5), k(.3, 'bed_m', x=1.2, y=1.8, b=1, eye='-', mark='bbl'), k(.5, 'bed_m', x=1.3, y=2, b=1.3, eye='-', mark='bbl bbl'), k(.7, 'bed_m', x=.8, y=1.1, b=.6, eye='O'), k(.88, eye='^')],
        [], g='play', act=('blow', 'bubbles'), prefer=['young', 'happy'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It popped one with its face. Good form.', 'Blew bubbles at a fish. This is what ducks are for.'])
    o.r('drum_the_bank_for_the_shivers', 'Drumming both feet on the front stone to send shivers down the bank for the whiskers to pick up', 18, 'none',
        [k(.12, 'stone_m', x=.2, y=.4, b=-.5, l=1), k(.28, 'stone_m', x=.3, y=.5, b=-.7, r=1, mark='thud'), k(.44, 'stone_m', x=.2, y=.4, b=-.6, l=1, mark='thud'), k(.6, 'stone_m', x=.3, y=.5, b=-.7, r=1, mark='thud'), k(.8, 'bed_m', x=.9, y=1.1, b=.7, eye='O')],
        [], g='play', act=('drum', 'bank'), prefer=['young', 'grumpy'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.85, {'lure': 1})])
    o.r('look_for_it_in_the_shaded_pads', 'Seeking the cat in the shade of the right-hand pads, one wing flicking each pad over', 22, 'wing',
        [k(.12, 'bed_r', reach=.5, x=.8, y=.9, b=.4), k(.3, 'pad_low', reach=1, x=1.1, y=.8, b=.9, eye='o'), k(.5, 'pad_low', reach=1, x=1.3, y=1.2, b=1.3, l=1, eye='O', mark='huh'), k(.7, 'bed_r', reach=1, x=.9, y=1.2, b=1.1, r=1, eye='>'), k(.88, eye='^', mark='there')],
        [], g='play', act=('seek', 'cat'), prefer=['young', 'curious'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('measure_the_whisker_span', "Holding a reed across the cat's whiskers to measure how far they spread, then against his own wing", 24, 'reed',
        [k(.12, 'bed_m', reach=.5, x=.3, y=.5, b=.3), k(.3, 'bed_m', reach=1, x=.5, y=.9, b=.6), k(.5, 'bed_l', reach=1, x=.5, y=.9, b=.7, l=1, mark='hm'), k(.7, 'bed_m', reach=.8, x=-.2, y=.5, w=.5, b=.4), k(.9, eye='O', mark='huge')],
        [], g='test', act=('measure', 'whiskers'), prefer=['curious'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Wider than my wings. It is mostly moustache.', 'Spanned it twice. Still not a fair measure.'])
    o.r('peer_into_the_great_mouth', "Peering down into the cat's wide open mouth to see how far the dark goes", 18, 'none',
        [k(.12, x=.4, y=.7, b=.5), k(.3, 'bed_l', x=1, y=1.9, b=1.2, eye='O'), k(.5, 'bed_l', x=1.1, y=2.2, b=1.4, eye='@', mark='...'), k(.7, x=-.7, y=-.4, b=-.3, w=.6, eye='>'), k(.88, eye='-')],
        [], g='test', act=('peer', 'mouth'), prefer=['curious', 'young'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Big enough for my head. I did not test that.', 'Looked in. Saw a lot of cat.'])
    o.r('weigh_it_against_the_wild_record', "Stretching a wing out past the cat's length and weighing it against how long a wild one could grow", 22, 'wing',
        [k(.12, 'bed_l', reach=.5, x=.3, y=.7, b=.4), k(.3, 'bed_l', reach=1, x=.4, y=1, b=.6), k(.5, 'bed_r', reach=1, x=.6, y=.8, b=.4, r=1, mark='whoa'), k(.7, 'bed_m', reach=.7, x=.2, y=.4, b=.3), k(.88, eye='-', mark='bigger')],
        [], g='test', act=('weigh', 'size'), prefer=['curious', 'grown'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('wait_for_the_whiskers_to_show', 'Waiting stock-still at the rim for the first whisker to break the black water', 22, 'none',
        [k(.12, 'pad_low', x=.7, y=1.3, b=.8, eye='o'), k(.35, 'pad_low', x=.8, y=1.5, b=1, eye='o'), k(.6, 'pad_low', x=.8, y=1.5, b=1, eye='O', mark='...'), k(.8, 'pad_low', x=.4, y=.8, b=.5, eye='^')],
        [], g='rest', act=('wait', 'whisker'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_cat_to_the_dark', 'Sweeping a wing out over the black water to present the cat to nobody, a ringmaster with no ring', 20, 'wing',
        [k(.12, 'bed_r', reach=.5, x=.2, y=.2, w=.2), k(.3, 'bed_m', reach=1, x=.2, y=-.2, b=-.3), k(.5, 'bank_r', reach=1, x=.2, y=-.3, b=-.4, mark='tadaa'), k(.7, 'bank_r', reach=1, x=.4, y=-.2, b=-.2), k(.88, eye='^')],
        [], g='show', act=('present', 'cat'), prefer=['happy'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_the_moustache_rights', 'Arguing with the cat nose to nose about whose moustache is the better one, jabbing a wing at the water', 20, 'wing',
        [k(.12, 'bed_m', reach=.6, x=.5, y=.5, b=.5), k(.3, 'bed_m', reach=1, x=.9, y=.3, b=.2, mark='NOPE'), k(.5, 'bed_m', reach=1, x=1, y=.2, b=.1, r=1, mark='NOPE'), k(.7, 'bed_m', reach=.6, x=.3, y=.4, b=.3), k(.88, eye='-')],
        [], g='show', act=('argue', 'moustache'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Mine is only two lines. It has a moustache and a mood.', 'Lost the argument. Kept the grudge.'])
    o.r('pose_at_the_stone_with_the_cat', 'Holding a heroic pose on the left stone while the cat sits below him like a sponsor', 18, 'none',
        [k(.12, 'stone_l', x=.3, y=-.2, w=.4, perch=1), k(.3, 'stone_l', x=.5, y=-.5, b=-.2, w=.8, perch=1), k(.6, 'stone_l', x=.6, y=-.6, b=-.2, w=1, perch=1, eye='^', mark='ta-da'), k(.85, 'stone_l', x=.2, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'stone'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('sing_the_cat_a_night_song', 'Singing a low night song at the water for the cat, a slow bill-bob to every whisker twitch', 22, 'none',
        [k(.12, 'bed_r', x=.7, y=.9, b=.8), k(.3, 'bed_r', x=1, y=1.6, b=1.3, eye='-', mark='la'), k(.5, 'bed_r', x=1.1, y=1.9, b=1.7, eye='-', mark='laaa'), k(.7, 'bed_r', x=1, y=1.5, b=1.2, eye='-', mark='la'), k(.86, eye='^')],
        [], g='show', act=('sing', 'cat'), when=['night'], prefer=['lonely', 'sad'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It stayed for the chorus. Left before the bridge.', 'Low notes only. The cat has standards, mostly bass.'])
    o.r('hop_back_from_the_snapping_jaws', "Hopping back from the rim when the cat's big mouth snaps at a bill-tip that looked like a pellet", 16, 'none',
        [k(.12, 'stone_m', x=.8, y=1.4, b=.7), k(.28, 'stone_m', x=1, y=1.6, b=1, eye='o', mark='...'), k(.42, x=-1.2, y=-.8, b=-1.4, l=1, r=1, w=1, eye='O', mark='YIKES'), k(.6, x=-.6, y=.3, b=.2, eye='>'), k(.82, x=.2, y=.2, eye='-')],
        [], g='mishap', act=('hop', 'jaws'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['It mistook my face for a snack. Fair, mostly.', 'Jaws. In a pond. Eight inches from my bill.'])
    o.r('compare_whisker_counts_with_a_friend', 'Comparing counts with a friend, one at each end of the rim, over how many barbels the cat really has', 24, 'none',
        [k(.1, 'bed_l', x=.8, y=1.2, b=.5, mark='1'), k(.3, 'bed_l', x=.9, y=1.3, b=.6, mark='2'), k(.5, 'bed_r', x=.9, y=1.1, b=.6, l=1, eye='-', mark='6?'), k(.7, 'bed_l', x=.8, y=1.2, b=.5, mark='8!'), k(.88, eye='^')],
        [], g='test', act=('count', 'barbels'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Eight. Argued down from eleven. Whiskers do not hold still.', 'Two ducks counting a fish. Fish keeps the number.'],
        duo=[k(.15, 'bed_r', x=.7, y=1, b=.5, eye='o'), k(.35, 'bed_r', x=.8, y=1.1, b=.6, mark='4'), k(.55, 'bed_l', x=.9, y=1.2, b=.6, r=1, mark='8'), k(.78, 'bed_r', x=.5, y=.7, b=.4, eye='^')])
    o.r('brace_a_wing_against_the_gust_at_the_bank', 'Bracing a wing against the gust at the bank so the cat can hold its whiskers in the lee', 22, 'wing',
        [k(.12, 'bank_r', reach=.4, x=-.3, y=.4, b=.5), k(.3, 'bank_r', reach=1, x=-.6, y=.5, b=.9, w=.8), k(.55, 'bank_r', reach=1, x=-.8, y=.6, b=1.2, w=1, r=1, mark='fff'), k(.78, 'bank_r', reach=.6, x=-.3, y=.4, b=.6, eye='^'), k(.9, eye='-')],
        [(.55, 'ease')], g='weather', act=('brace', 'wing'), when=['windy'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.65, {'lure': 1})], say=['The cat stayed under my wing. The gust took my dignity.', 'Windbreak duty. Whiskers undisturbed. Mine, not so much.'])
    return o


def bass():
    o = Obj('bass', 'keeping', on='koi_pond', 
            parts=dict(surf='the water surface near the rim', lane='the open stretch of water in front of the pads', cove='the sheltered water between the pads', pad='the lily pads floating on the water', bloom='the lily bloom on its pad', bank='the stone bank round the pond', stone='the front rim stones'),
            fields={'lunge': (0, 0, 1), 'ring': (0, 0, 1)},
            physics=[('lunge', 'rate', -0.0003, 'always'), ('ring', 'rate', -0.004, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                rescue=[['subject.health', 'add', 0.15], ['lunge', 'mul', 0.4]],
                leaptake=[['subject.hunger', 'add', -0.2], ['lunge', 'add', 0.25], ['ring', 'set', 1]],
                trick=[['lunge', 'add', 0.3], ['subject.trust', 'add', 0.1]],
                dimple=[['ring', 'set', 1], ['subject.mood', 'add', 0.15]],
                lead=[['lunge', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('ring', 0.3, 'o O o', 'surf_m', 'water')],
            anchors=dict(
                surf_l=(0.2353, 0.7818),
                surf_m=(0.4874, 0.7455),
                surf_r=(0.7395, 0.7091),
                lane=(0.5882, 0.7818),
                cove=(0.3361, 0.7091),
                pad_low=(0.7227, 0.6727),
                bloom_r=(0.6807, 0.6364),
                bank_r=(0.7983, 0.7273),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364),
            ))
    o.r('shove_the_stranded_bass_back_in', 'Nudging the bass that overshot and landed flapping at the rim back over the lip with a wing', 20, 'wing',
        [k(.12, 'stone_m', reach=.6, x=.3, y=.9, b=.6, eye='O'), k(.3, 'stone_m', reach=1, x=.5, y=1.5, b=1.2, mark='flap'), k(.5, 'surf_m', reach=1, x=.7, y=1.4, b=1, l=1, mark='shff'), k(.7, 'surf_m', reach=1, x=.4, y=.8, b=.6, w=0), k(.88, y=.2, eye='^')],
        [(0.5, 'rescue')], g='care', act=('nudge', 'jumper'), when=['lunge>.7'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Back in. It will do that again by lunchtime.', 'Saved a fish from the stones. It had no plan.'])
    o.r('dab_the_scraped_chin', "Patting the bass's scraped chin from the last landing with the damp tip of a wing", 18, 'wing',
        [k(.12, 'surf_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'surf_l', reach=1, x=.3, y=1.3, b=1, mark='dab'), k(.5, 'surf_l', reach=1, x=.2, y=1.5, b=1.2, r=1, mark='dab dab'), k(.7, 'surf_l', reach=.5, x=.2, y=.8, b=.6), k(.88, eye='-')],
        [(0.5, 'tend')], g='care', act=('pat', 'chin'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('hold_a_flake_high_for_the_leap', 'Lifting one flake in his bill just out of the water so the hungriest bass has to leap for it', 22, 'none',
        [k(.12, x=.4, y=.4, b=.4), k(.3, 'surf_m', x=1, y=.3, b=.7, eye='o', mark='...'), k(.46, 'surf_m', x=1.2, y=-.8, b=-.9, w=.4, eye='O', mark='SPLOSH'), k(.64, 'surf_m', x=.4, y=.4, b=.4, w=.8, eye='>'), k(.86, eye='^')],
        [(0.46, 'leaptake')], g='use', act=('lift', 'flake'), when=['fish_hunger>.4'], prefer=['dawn', 'dusk'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.5, {'lure': 1}), (0.75, {'lure': 0})],
        say=['Took it clean out of my bill. The splash was extra.', 'It leapt. I flinched. Both of us pretend it did not happen.'])
    o.r('hold_a_reed_hoop_over_the_water', "Lifting a reed bent into a hoop at arm's length above the water for the bass to leap clean through", 24, 'reed',
        [k(.12, 'surf_r', reach=.5, x=.3, y=-.2, b=.4), k(.3, 'surf_r', reach=1, x=.5, y=-.5, b=.8, w=.3), k(.5, 'surf_r', reach=1, x=.6, y=-.7, b=1, l=1, mark='SPLSH'), k(.7, 'surf_r', reach=1, x=.4, y=-.4, b=.7, r=1, mark='PLOP'), k(.9, eye='^')],
        [(0.5, 'trick')], g='show', act=('lift', 'hoop'), when=['lunge<.8'], prefer=['curious', 'grown'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Through the hoop. No applause. I applauded.', 'Circus fish. I am the ringmaster. Good arrangement.'])
    o.r('skitter_the_reed_tip_on_the_surface', 'Tapping a reed tip along the surface so it dimples like prey and the bass strikes at it', 20, 'reed',
        [k(.12, 'surf_l', reach=.5, x=.3, y=.3, b=.3), k(.3, 'cove', reach=1, x=.5, y=.5, b=.6, mark='tk tk'), k(.5, 'lane', reach=1, x=.6, y=.6, b=.8, mark='tk tk'), k(.7, 'surf_r', reach=1, x=.7, y=.6, b=.9, l=1, mark='STRK'), k(.88, eye='O')],
        [(0.7, 'dimple')], g='use', act=('tap', 'surface'), prefer=['dawn', 'dusk', 'curious'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('walk_a_wingtip_along_the_pad_edge', 'Walking a wingtip along the edge of the pads so the bass chases it from the cover', 24, 'wing',
        [k(.1, 'cove', reach=.6, x=.2, y=.5, b=.3), k(.28, 'lane', reach=1, x=.3, y=.6, b=.4, l=1), k(.5, 'surf_r', reach=1, x=.4, y=.6, b=.4, r=1), k(.7, 'pad_low', reach=1, x=.4, y=.5, b=.4, l=1), k(.9, eye='^')],
        [(0.5, 'lead')], g='use', act=('chase', 'wingtip'), pick='shyest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('race_the_bass_along_the_edge', 'Having a race with the bass along the front edge at full tilt, wings out, losing by two lengths', 20, 'none',
        [k(.1, 'surf_l', x=.5, y=.4, b=.4), k(.28, 'cove', x=1.1, y=.5, b=-.6, l=1, w=.6), k(.46, 'lane', x=1.4, y=.5, b=-.8, r=1, w=.8, mark='whoosh'), k(.64, 'surf_r', x=1.5, y=.5, b=-.6, l=1, w=.7), k(.84, 'bank_r', x=.3, y=.5, b=.5, eye='@')],
        [(0.46, 'fun')], g='play', act=('race', 'edge'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Lost by two lengths. Mine were shorter.', 'Fish does not run. Fish still wins. Rigged.'])
    o.r('splash_back_at_the_tail_slap', 'Splashing back at the bass with a wing every time it slaps its tail on the water', 18, 'wing',
        [k(.12, 'surf_m', reach=.5, x=.3, y=.3, b=.3), k(.3, 'surf_m', reach=1, x=.5, y=.4, b=-.4, mark='SLAP'), k(.48, 'surf_m', reach=1, x=.5, y=.4, b=-.5, l=1, mark='SPLSH'), k(.66, 'surf_m', reach=1, x=.5, y=.4, b=-.4, r=1, mark='SLAP'), k(.86, eye='@')],
        [], g='play', act=('splash', 'tail'), prefer=['young', 'happy', 'ring>.3'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('hide_and_leap_from_the_pad', 'Playing seek, ducking out of sight at the pad then popping up with a shout just as the bass comes by', 22, 'none',
        [k(.12, 'pad_low', x=.2, y=1.1, b=1.2), k(.3, 'pad_low', x=-.3, y=1.5, b=1.6, eye='-'), k(.5, 'pad_low', x=-.4, y=1.6, b=1.7, eye='o', mark='...'), k(.62, 'pad_low', x=.8, y=-.8, b=-1, w=1, eye='O', mark='BOO'), k(.84, x=.2, y=.2, eye='^')],
        [], g='play', act=('seek', 'bass'), prefer=['young', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.85, {'lure': 1})])
    o.r('count_the_leaps_in_a_minute', 'Counting leaps by tapping a foot at the rim, one tap for each, until the bass stops', 22, 'none',
        [k(.12, 'stone_m', x=.3, y=.6, b=.3, l=1, mark='1'), k(.3, 'stone_m', x=.4, y=.4, b=-.3, r=1, mark='2'), k(.5, 'stone_m', x=.3, y=.5, b=-.4, l=1, mark='3'), k(.7, 'stone_m', x=.4, y=.4, b=-.3, r=1, mark='4'), k(.86, eye='-', mark='show-off')],
        [], g='test', act=('count', 'leaps'), prefer=['curious'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('peer_at_the_big_jaw_line', 'Peering along the big jaw line to see how far back the mouth runs past the eye', 18, 'none',
        [k(.12, x=.4, y=.8, b=.4), k(.3, 'surf_r', x=1, y=1.7, b=1, eye='o'), k(.5, 'surf_r', x=1.2, y=2, b=1.3, eye='@', mark='...'), k(.7, 'surf_r', x=.5, y=.9, b=.6, eye='-'), k(.88, eye='-')],
        [], g='test', act=('peer', 'jaw'), prefer=['curious', 'young'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('wait_for_the_first_ring_of_dawn', 'Waiting at the rim in the grey dawn, bill hovering, for the first ring to spread from a rise', 24, 'none',
        [k(.16, 'surf_m', x=1.4, y=.4, b=.2, eye='o'), k(.4, 'surf_m', x=1.5, y=.5, b=.2, r=1), k(.62, 'surf_m', x=1.5, y=.5, b=.2, eye='O', mark='...'), k(.84, 'surf_m', x=.9, y=.2, w=.3, eye='^')],
        [], g='rest', act=('wait', 'ring'), when=['dawn'], prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_bass_to_the_pond', 'Presenting the bass to the pond with a long low sweep of the wing, announcing a record', 20, 'wing',
        [k(.1, 'lane', reach=.3, x=.5, y=-.4, b=-.5), k(.3, 'surf_m', reach=1, x=.5, y=-.6, b=-.6, l=1), k(.5, 'surf_m', reach=1, x=.6, y=-.8, b=-.7, r=1, mark='AND'), k(.7, 'surf_l', reach=1, x=.3, y=-.4, b=-.3), k(.88, eye='^')],
        [], g='show', act=('present', 'bass'), prefer=['happy'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_the_leap_height', 'Arguing with the bass about the height of that last leap, bill to bill, a wing jabbing the sky', 20, 'wing',
        [k(.12, 'surf_l', reach=.6, x=1.1, y=.3, b=.8), k(.3, 'surf_l', reach=1, x=1.4, y=.1, b=.4, mark='HIGHER'), k(.46, 'surf_l', reach=.3, x=.3, y=.1, b=.3), k(.62, 'surf_l', reach=1, x=1.5, y=.1, b=.4, l=1, mark='HIGHER'), k(.8, 'surf_l', reach=.5, x=.8, y=.3, b=.5), k(.9, eye='-')],
        [], g='show', act=('argue', 'height'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It claims five reeds. I saw four. Sworn statement.', 'Fish and I disagree on air. Air takes no side.'])
    o.r('pose_with_the_arc_behind_him', 'Striking a victory pose at the left stone as the bass hangs at the top of its arc', 18, 'none',
        [k(.12, 'stone_l', y=-.4, b=-.2, w=.9, perch=1), k(.3, 'stone_l', x=.3, y=-.9, b=-.5, w=1, l=1, perch=1), k(.5, 'stone_l', x=.4, y=-1, b=-.6, w=1, r=1, perch=1, eye='^', mark='ta-da'), k(.7, 'stone_l', x=.1, y=-.3, b=-.2, w=.6, perch=1), k(.86, 'stone_l', perch=1)],
        [], g='show', act=('pose', 'arc'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('hop_back_from_the_soaking_splash', 'Hopping back from the rim when a leap lands in his face and soaks him from bill to belly', 16, 'none',
        [k(.12, 'cove', x=.8, y=1.2, b=.7), k(.28, 'cove', x=1, y=1.4, b=.9, eye='o', mark='...'), k(.42, x=-1.2, y=-.8, b=-1.4, l=1, r=1, w=1, eye='O', mark='SPLASH'), k(.6, x=-.6, y=.3, b=.2, eye='>'), k(.82, x=.2, y=.2, eye='-')],
        [], g='mishap', act=('hop', 'spray'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Soaked. It did that on purpose and I respect it.', 'A fish just got the last word and it was wet.'])
    o.r('hoop_and_flake_with_a_friend', 'Hooking the reed hoop out while a friend dangles a flake through it so the bass has to leap the hoop to reach it', 26, 'reed',
        [k(.1, 'surf_l', reach=.5, x=.3, y=-.2, b=.4), k(.3, 'surf_l', reach=1, x=.5, y=-.5, b=.8), k(.5, 'surf_l', reach=1, x=.6, y=-.7, b=1, l=1, mark='SPLSH'), k(.7, 'surf_l', reach=1, x=.4, y=-.4, b=.7, r=1), k(.88, eye='^')],
        [(0.5, 'leaptake')], g='use', act=('hook', 'hoop'), when=['fish_hunger>.4'], prefer=['happy'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})],
        duo=[k(.15, 'surf_r', x=.4, y=.2, b=.4), k(.34, 'surf_r', x=1, y=.3, b=.8, eye='o', mark='...'), k(.5, 'surf_r', x=1.2, y=-.7, b=-.8, w=.4, eye='O'), k(.72, 'surf_r', x=.5, y=.4, b=.4, eye='^')])
    o.r('swap_leap_counts_with_a_friend', 'Trading leap counts with a friend along the rim, each one tapping a different stone and arguing the total', 24, 'none',
        [k(.1, 'stone_l', x=.3, y=.5, b=.3, l=1, mark='1'), k(.3, 'stone_l', x=.4, y=.4, b=-.3, r=1, mark='2'), k(.5, 'stone_m', x=.4, y=.4, b=-.3, l=1, mark='5?'), k(.7, 'stone_l', x=.3, y=.5, b=.3, r=1, mark='4!'), k(.88, eye='^')],
        [], g='test', act=('count', 'rises'), prefer=['curious', 'happy'], pick='hungriest',
        obj=[(0.35, {'lure': 1}), (0.75, {'lure': 1})],
        say=['We counted twelve. Fish says four. It was there.', 'Two ducks, one pond, no agreement. Fish abstains.'],
        duo=[k(.15, 'stone_r', x=.4, y=.5, b=.3, r=1), k(.35, 'stone_r', x=.5, y=.4, b=-.3, l=1, mark='3'), k(.55, 'stone_r', x=.4, y=.4, b=-.3, r=1, mark='6'), k(.78, 'stone_r', x=.3, y=.5, b=.3, eye='^')])
    o.r('double_dare_the_pad_ambush', 'Guarding the pad edge with a friend, one on each side, so the bass has nowhere to hide when it breaks cover', 24, 'wing',
        [k(.1, 'bloom_r', reach=.6, x=.3, y=.4, b=.5), k(.3, 'pad_low', reach=1, x=.5, y=.3, b=.7, eye='o'), k(.5, 'pad_low', reach=1, x=.6, y=.3, b=.9, l=1, eye='O', mark='NOW'), k(.7, 'surf_r', reach=1, x=.5, y=.7, b=.6, r=1, eye='>'), k(.88, eye='^')],
        [], g='play', act=('guard', 'cover'), prefer=['young', 'happy'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.8, {'lure': 1})],
        duo=[k(.15, 'surf_l', x=.4, y=.5, b=.4), k(.34, 'cove', x=.8, y=.6, b=.5, eye='o'), k(.55, 'lane', x=1.1, y=.8, b=.8, l=1, mark='GO'), k(.78, 'surf_r', x=.5, y=.5, b=.4, eye='^')])
    o.r('catch_the_rain_dimples_in_his_bill', 'Catching raindrops in his bill at the rim while the bass rises to every dimple they make', 20, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'surf_l', x=1, y=-.8, b=-.4, eye='o', mark='plip'), k(.5, 'surf_l', x=1.1, y=-1, b=-.5, l=1, eye='O', mark='plip plip'), k(.7, 'surf_l', x=.8, y=-.3, b=.2, w=.4, eye='^'), k(.88, eye='-')],
        [(.5, 'cheer')], g='weather', act=('catch', 'raindrops'), when=['wet'], pick='hungriest',
        obj=[(.3, {'lure': 1}), (.6, {'lure': 1}), (.8, {'lure': 0})], say=['Drank the sky. The bass drank the lake.', 'Rain bites back. I bit first.'])
    return o


def carp():
    o = Obj('carp', 'keeping', on='koi_pond', 
            parts=dict(floor='the water over the pond floor', mud='the muddy edge of the water', shelf='the shelf of shallow water along the bank', reed='the reed stems at the pond edge', stone='the front rim stones'),
            fields={'silt': (0, 0, 1), 'root': (0, 0, 1)},
            physics=[('silt', 'rate', 0.0005, 'day'), ('silt', 'rate', -0.0008, 'night'), ('root', 'rate', -0.0003, 'always')],
            effects=dict(
                ease=[['subject.trust', 'add', 0.12]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                sink=[['silt', 'add', 0.3]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                lead=[['root', 'add', 0.2], ['subject.trust', 'add', 0.1]],
                tickle=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('silt', 0.3, '~=~=~', 'floor_m', 'mud')],
            anchors=dict(
                floor_l=(0.2353, 0.7818),
                floor_m=(0.4874, 0.7455),
                floor_r=(0.7395, 0.7091),
                mud_edge=(0.4034, 0.7818),
                shelf=(0.3361, 0.7091),
                reed_low=(0.0672, 0.6909),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364, 'surface'),
            ))
    o.r('groom_the_coarse_scales', "Grooming grit out of the big coarse scales along the carp's flank with a bill and a wing together", 24, 'wing',
        [k(.16, 'floor_l', reach=.5, x=.5, y=.9, b=.6), k(.34, 'floor_l', reach=1, x=.8, y=1.5, b=1.3, mark='rsp'), k(.54, 'shelf', reach=1, x=.9, y=1.5, b=1.4, l=1, mark='rsp'), k(.74, 'floor_l', reach=1, x=.7, y=1.3, b=1.1, r=1), k(.9, eye='^')],
        [(0.54, 'tend')], g='care', act=('groom', 'scales'), when=['fish_health<.9'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Gritty fish. Scrubbed and still gritty.', 'Scales like roof tiles. Very pleasing, very much not mine.'])
    o.r('offer_a_pellet_at_the_mud_edge', 'Carrying a pellet in his bill just at the mud edge until the hungriest carp sucks it out with its lips', 22, 'none',
        [k(.16, x=.5, y=.6, b=.6), k(.36, 'mud_edge', x=1.1, y=1.5, b=1.3, eye='o', mark='...'), k(.56, 'mud_edge', x=1.2, y=1.8, b=1.5, eye='O', mark='smack'), k(.76, 'mud_edge', x=.6, y=.8, b=.7, w=.4, eye='^'), k(.9, eye='-')],
        [(0.56, 'feed')], g='use', act=('carry', 'pellet'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.35, {'lure': 1}), (0.65, {'lure': 1}), (0.8, {'lure': 0})],
        say=['Lips like a vacuum. Nearly had my bill.', 'Fed a carp by hand. It sucked and judged.'])
    o.r('trail_a_wing_along_the_mud_edge', 'Dragging a wing along the mud edge and the carp following it, nosing the bottom the whole way', 26, 'wing',
        [k(.14, 'floor_l', reach=.6, x=.3, y=.9, b=.6), k(.32, 'mud_edge', reach=1, x=.5, y=1, b=.8, l=1), k(.52, 'floor_m', reach=1, x=.6, y=1, b=.8, r=1), k(.72, 'floor_r', reach=1, x=.6, y=1, b=.8, l=1), k(.9, eye='^')],
        [(0.52, 'lead')], g='use', act=('drag', 'wing'), when=['root<.7'], pick='hungriest',
        obj=[(0.16, {'lure': 1}), (0.34, {'lure': 1}), (0.54, {'lure': 1}), (0.76, {'lure': 1})],
        say=['Followed my wing like a dog. A very big, very wet dog.', 'It nosed the bottom the whole way. Efficient, if brown.'])
    o.r('tickle_the_barbels_with_a_reed', "Prodding the carp's twin barbels with the very end of a reed while it holds still at the rim", 20, 'reed',
        [k(.16, 'floor_l', reach=.5, x=.3, y=.6, b=.5), k(.36, 'floor_l', reach=1, x=.5, y=1.1, b=1, mark='tck'), k(.56, 'floor_l', reach=1, x=.5, y=1.3, b=1.2, l=1, r=1, mark='tck tck'), k(.76, 'floor_l', reach=1, x=.4, y=1, b=.9), k(.9, eye='^')],
        [(0.56, 'tickle')], g='use', act=('prod', 'barbels'), prefer=['silt>.3'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('show_the_shy_one_a_flake', 'Showing the shy carp a flake over the far pad edge and letting it come for it, bill unmoving', 22, 'none',
        [k(.16, x=.4, y=.5, b=.5), k(.36, 'floor_r', x=1, y=1.3, b=1.2, eye='-'), k(.56, 'floor_r', x=1.1, y=1.5, b=1.4, eye='O', mark='gulp'), k(.76, 'floor_r', x=.6, y=.7, b=.7, w=.5, eye='^'), k(.9, eye='-')],
        [(0.56, 'feed')], g='show', act=('show', 'flake'), when=['fish_hunger>.4'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.65, {'lure': 1}), (0.8, {'lure': 0})])
    o.r('waltz_the_bank_beside_the_carp', "Dancing a waltz slowly along the bank in time with the carp's heavy swim, three steps and a turn", 24, 'none',
        [k(.14, 'stone_l', x=.3, y=.3, b=.6, l=1), k(.32, 'stone_m', x=.5, y=.3, b=-.4, r=1, w=.6), k(.5, 'stone_m', x=.4, y=.3, b=.6, l=1, w=.8, mark='la'), k(.68, 'stone_r', x=.5, y=.3, b=-.4, r=1, w=.6), k(.86, 'stone_r', x=.2, y=.3, b=.4, eye='^')],
        [(0.5, 'fun')], g='play', act=('dance', 'bank'), prefer=['happy'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.4, {'lure': 1}), (0.62, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('blow_bubbles_back_at_the_carp', 'Blowing bubbles back at the carp every time it burps one up at the rim, trading them like ping pong', 20, 'none',
        [k(.14, x=.3, y=.7, b=.5), k(.32, 'floor_m', x=1.3, y=2, b=1.2, eye='-', mark='blp'), k(.5, 'floor_m', x=1.4, y=2.1, b=1.4, eye='O', mark='blp blp'), k(.68, 'floor_m', x=.9, y=1.2, b=.8, eye='>', mark='bloop'), k(.86, eye='^')],
        [], g='play', act=('blow', 'bubbles'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It won on volume. I won on spit.', 'Bubble rally. No clear winner. Fish is warm.'])
    o.r('hide_a_toe_for_the_carp_to_find', 'Hide-and-seek with a toe: wiggling it over the edge of the stone and hiding it again when the carp noses near', 20, 'none',
        [k(.14, 'stone_m', x=.2, y=.4, b=.7, l=1), k(.3, 'stone_m', x=.4, y=.8, b=1, l=1, mark='wgl'), k(.46, 'stone_m', x=.5, y=1, b=1.2, l=1, eye='o'), k(.58, 'stone_m', x=-.3, y=.3, b=.4, w=.5, eye='O', mark='!'), k(.78, 'stone_m', x=.4, y=.8, b=1, l=1, mark='wgl'), k(.9, eye='^')],
        [], g='play', act=('hide', 'toe'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.36, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('count_the_plate_scales', "Counting the plate scales down the carp's flank, a tap of the bill for each one", 22, 'none',
        [k(.14, 'floor_l', x=.9, y=1.3, b=.8, mark='1'), k(.3, 'floor_l', x=1, y=1.5, b=.9, mark='2'), k(.46, 'shelf', x=1, y=1.5, b=.9, l=1, mark='3'), k(.62, 'shelf', x=1.1, y=1.7, b=1, r=1, mark='4'), k(.8, eye='-', mark='armour')],
        [], g='test', act=('count', 'scales'), prefer=['curious'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('compare_the_length_with_the_wild_record', "Stretching a reed along the carp's back and comparing it with how long a wild one has been caught", 24, 'reed',
        [k(.16, 'floor_l', reach=.5, x=.3, y=.6, b=.5), k(.34, 'floor_l', reach=1, x=.5, y=.9, b=.8), k(.54, 'floor_r', reach=1, x=.7, y=.8, b=.7, l=1, mark='hm'), k(.74, 'floor_m', reach=.7, x=.2, y=.4, b=.4), k(.9, eye='O', mark='huge')],
        [], g='test', act=('compare', 'length'), prefer=['curious', 'grown'], pick='hungriest',
        obj=[(0.34, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('wait_for_the_first_bubble_line', 'Waiting at the rim for the first string of bubbles that says the carp is awake and working', 22, 'none',
        [k(.16, 'floor_r', x=.5, y=1.5, b=1.4, eye='o'), k(.4, 'floor_r', x=.6, y=1.7, b=1.6, eye='o'), k(.62, 'floor_r', x=.6, y=1.7, b=1.6, l=1, eye='O', mark='...'), k(.82, 'floor_r', x=.2, y=.9, b=.7, eye='^')],
        [], g='rest', act=('wait', 'bubbles'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_carp_to_the_cattails', 'Presenting the carp to the cattails with a slow sweep of the wing, as though they might buy it', 22, 'wing',
        [k(.14, 'floor_l', reach=.3, x=.2, y=-.1, b=.3), k(.34, 'floor_l', reach=1, x=.3, y=-.4, b=-.2, l=1), k(.54, 'reed_low', reach=1, x=.3, y=-.5, b=-.3, r=1, mark='behold'), k(.74, 'floor_l', reach=1, x=.2, y=-.3, b=-.1), k(.9, eye='^')],
        [], g='show', act=('present', 'carp'), prefer=['happy'], pick='shyest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('argue_with_it_about_the_mud', 'Arguing with the carp nose to nose over who owns the mud, a wing stabbing at the floor', 22, 'wing',
        [k(.14, 'floor_m', reach=.5, x=.9, y=.7, b=.7), k(.3, 'floor_m', reach=1, x=1.2, y=1, b=1, mark='MINE'), k(.44, 'floor_m', reach=.3, x=.4, y=.5, b=.4), k(.6, 'floor_m', reach=1, x=1.3, y=1.1, b=1.1, r=1, mark='MINE'), k(.78, 'floor_m', reach=.5, x=.7, y=.7, b=.7), k(.9, eye='-')],
        [], g='show', act=('argue', 'mud'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.65, {'lure': 1})],
        say=['Carp says it is its mud. Carp has priors.', 'Lost to a fish with a vacuum for a face.'])
    o.r('pose_like_a_carp_on_the_stone', "Striking a pose at the left stone with lips pouted and his wings drooped like a carp's fins, deadly serious", 18, 'none',
        [k(.16, 'stone_l', x=.5, y=.4, b=.4, w=.3, perch=1), k(.34, 'stone_l', x=.9, y=.8, b=.8, w=.6, perch=1, eye='O', mark='pout'), k(.56, 'stone_l', x=1, y=.9, b=.9, w=.6, l=1, perch=1, eye='O', mark='pout'), k(.78, 'stone_l', x=.4, y=.3, b=.3, w=.3, perch=1, eye='^')],
        [], g='show', act=('pose', 'lips'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('startle_back_at_the_gulp', 'Hopping back with a yelp when the carp gulps at the surface just under his bill', 16, 'none',
        [k(.14, 'floor_l', x=.9, y=1.5, b=1), k(.28, 'floor_l', x=1, y=1.7, b=1.2, eye='o', mark='...'), k(.4, x=-1.4, y=-1, b=-1.6, l=1, r=1, w=1, eye='O', mark='GLUP'), k(.58, x=-.8, y=.2, b=-.2, eye='>'), k(.8, x=.1, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'gulp'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['It gulped at my face. Rude, but also fair.', 'Big mouth, no warning. Like a politician, scaly.'])
    o.r('two_sets_of_sinkers_from_both_ends', 'Pouring sinkers at the left end of the bank while a friend drops theirs at the right, the carp torn between them', 24, 'wing',
        [k(.14, 'floor_l', reach=.5, x=.1, y=.2, w=.2), k(.36, 'floor_l', reach=1, x=0, y=.3, b=-.4, mark='plk'), k(.56, 'floor_l', reach=1, x=0, y=.6, b=.4, mark='plk plk'), k(.78, eye='o')],
        [(0.36, 'sink')], g='use', act=('pour', 'pellets'), when=['pond_flakes<.4'], prefer=['happy'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.78, {'lure': 1})],
        say=['Two dinners at once. It chose the wetter one.', 'Equal pellets both ends. The carp invented a third end.'],
        duo=[k(.18, 'floor_r', x=.2, y=.3, b=.4), k(.4, 'floor_r', x=.8, y=.9, b=.9, mark='plk'), k(.6, 'floor_r', x=.9, y=1.1, b=1, l=1, mark='plk plk'), k(.8, 'floor_r', x=.3, y=.4, b=.3, eye='^')])
    o.r('mud_wave_with_a_friend_in_time', 'Drumming a wave of footfalls down the stones with a friend in time, the carp swimming along to the beat', 24, 'none',
        [k(.14, 'floor_l', x=.3, y=.3, b=-.5, l=1), k(.32, 'floor_m', x=.4, y=.3, b=-.7, r=1), k(.5, 'floor_r', x=.4, y=.3, b=-.5, l=1, mark='tum'), k(.68, 'floor_m', x=.4, y=.3, b=-.7, r=1), k(.86, 'floor_l', x=.3, y=.3, b=-.4, l=1, eye='^')],
        [], g='play', act=('drum', 'bank'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.32, {'lure': 1}), (0.58, {'lure': 1}), (0.8, {'lure': 1})],
        duo=[k(.18, 'floor_r', x=.3, y=.3, b=-.5, r=1), k(.4, 'floor_m', x=.4, y=.3, b=-.7, l=1), k(.6, 'floor_l', x=.4, y=.3, b=-.5, r=1, mark='tum'), k(.82, 'floor_m', x=.3, y=.3, b=-.4, eye='^')])
    o.r('warm_a_foot_by_the_sluggish_carp', 'Warming a cold foot on the mud edge while the sluggish carp noses past in the chill', 22, 'none',
        [k(.12, x=.2, y=.4, b=.4), k(.3, 'mud_edge', x=.6, y=.9, b=.9, l=1, eye='-'), k(.55, 'mud_edge', x=.5, y=1, b=1.1, r=1, eye='-', mark='mm'), k(.78, 'mud_edge', x=.3, y=.6, b=.6, eye='^'), k(.9, eye='-')],
        [(.55, 'ease')], g='weather', act=('warm', 'foot'), when=['cold'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.65, {'lure': 1})], say=['Two cold things sharing a mud edge. Romantic.', 'The carp moves at winter speed. I admire it.'])
    return o


def ghost_fish():
    o = Obj('ghost_fish', 'keeping', on='koi_pond', 
            parts=dict(dark='the shaded dark water under the pads', deep='the deepest middle of the water', edge='the far edge of the water', stone='the front rim stones', bank='the stone bank round the pond', pad='the lily pads floating on the water'),
            fields={'glow': (0, 0, 1), 'trace': (0, 0, 1), 'hush': (0, 0, 1)},
            physics=[('glow', 'rate', 0.003, 'night'), ('glow', 'rate', -0.004, '!night'), ('trace', 'rate', -0.003, 'always'), ('hush', 'rate', -0.0003, 'always')],
            effects=dict(
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                hush=[['hush', 'add', 0.25], ['subject.trust', 'add', 0.1]],
                glimmer=[['trace', 'set', 1], ['subject.mood', 'add', 0.15]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('glow', 0.3, '. * .', 'dark_m', 'glow'), ('trace', 0.3, '~*~*~', 'deep', 'glow')],
            anchors=dict(
                dark_l=(0.2353, 0.7818),
                dark_m=(0.4874, 0.7455),
                dark_r=(0.7395, 0.7091),
                deep=(0.3361, 0.7091),
                edge_far=(0.5882, 0.7818),
                stone_r=(0.7227, 0.8364, 'surface'),
                bank_r=(0.7983, 0.7273),
                pad_low=(0.7227, 0.6727),
            ))
    o.r('ease_a_weed_strand_off_the_pale_fin', 'Unwrapping a strand of weed from the pale fin with the very tip of his bill, holding his breath', 24, 'none',
        [k(.2, x=.3, y=.4, b=.2), k(.38, 'dark_l', x=.8, y=.9, b=.4, eye='-'), k(.56, 'dark_l', x=.9, y=1.1, b=.5, l=1, mark='...'), k(.72, 'dark_l', x=.5, y=.5, b=.3, r=1, mark='plip'), k(.88, eye='^')],
        [(0.56, 'tend')], g='care', act=('unwrap', 'fin'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.36, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Off. Not a ripple from either of us.', 'It stayed. Ghosts leave early. This one gave me a pass.'])
    o.r('pat_the_flank_dry_of_scum', 'Patting scum off the pale flank with the soft back of a wing while it hangs at the rim', 20, 'wing',
        [k(.2, 'dark_m', reach=.4, x=.2, y=.6, b=.3), k(.4, 'dark_m', reach=1, x=.3, y=1, b=.7, mark='pat'), k(.58, 'dark_m', reach=1, x=.2, y=1.2, b=.9, l=1, mark='pat'), k(.76, 'dark_m', reach=.5, x=.2, y=.7, b=.4), k(.9, eye='-')],
        [(0.58, 'tend')], g='care', act=('pat', 'flank'), prefer=['fish_health<.9'], pick='hungriest',
        obj=[(0.36, {'lure': 1}), (0.72, {'lure': 1})])
    o.r('offer_a_flake_to_the_glow', 'Carrying a flake in his bill to the pale shape rising out of the dark water', 22, 'none',
        [k(.2, x=.4, y=.4, b=.3), k(.4, 'dark_r', x=.9, y=.9, b=.5, eye='o', mark='...'), k(.58, 'dark_r', x=1, y=1.2, b=.7, eye='O', mark='sip'), k(.76, 'dark_r', x=.5, y=.6, b=.3, w=.3, eye='^'), k(.9, eye='-')],
        [(0.58, 'feed')], g='use', act=('carry', 'flake'), when=['fish_hunger>.4'], prefer=['night'], pick='hungriest',
        obj=[(0.38, {'lure': 1}), (0.66, {'lure': 1}), (0.82, {'lure': 0})],
        say=['Took it. Said nothing. Perfect guest.', 'A flake, taken by a ghost. I will tell no one.'])
    o.r('hum_it_a_lullaby_at_the_rim', 'Singing a lullaby at the water, soft and flat, until the pale fish stops flinching at his shadow', 26, 'none',
        [k(.2, 'dark_l', x=.4, y=.5, b=.3, eye='-'), k(.38, 'dark_l', x=.6, y=.8, b=.6, eye='-', mark='mmm'), k(.58, 'dark_l', x=.6, y=.9, b=.7, eye='-', mark='mmmm'), k(.78, 'dark_l', x=.5, y=.7, b=.5, eye='-', mark='mm'), k(.9, eye='^')],
        [(0.58, 'hush')], g='use', act=('sing', 'lullaby'), when=['hush<.7'], prefer=['lonely', 'sad'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Hummed it a lullaby. It stayed. Better reviews than my band.', 'Soft enough that the water forgot me.'])
    o.r('draw_a_glimmer_line_with_a_wingtip', 'Dragging a wingtip slowly across the water so the pale fish leaves a glimmering line in its wake', 24, 'wing',
        [k(.2, 'dark_l', reach=.4, x=.2, y=.4, b=.3), k(.4, 'deep', reach=1, x=.4, y=.5, b=.5, l=1), k(.6, 'dark_m', reach=1, x=.5, y=1.1, b=.5, r=1, mark='...'), k(.8, 'edge_far', reach=1, x=.5, y=.5, b=.5, l=1), k(.92, eye='^')],
        [(0.6, 'glimmer')], g='use', act=('drag', 'wingtip'), when=['night'], prefer=['trace<.3'], pick='shyest',
        obj=[(0.24, {'lure': 1}), (0.45, {'lure': 1}), (0.65, {'lure': 1}), (0.85, {'lure': 1})],
        say=['A line of light. I did that. With a wing.', "Wrote my name in fish glow. Reads 'ow', the fish moved."])
    o.r('stroke_the_cool_side_once', 'Pressing the cool pale side once, very lightly, with the back of a wing', 18, 'wing',
        [k(.2, 'dark_r', reach=.4, x=.2, y=.5, b=.3), k(.4, 'dark_r', reach=1, x=.3, y=.9, b=.6, mark='...'), k(.6, 'dark_r', reach=1, x=.3, y=1, b=.7, r=1), k(.8, 'dark_r', reach=.4, x=.2, y=.5, b=.3), k(.92, eye='^')],
        [(0.6, 'stroke')], g='use', act=('press', 'side'), prefer=['fish_trust>.4', 'lonely'], pick='shyest',
        obj=[(0.38, {'lure': 1}), (0.72, {'lure': 1})])
    o.r('play_peekaboo_with_the_glow', 'Playing seek: ducking down out of sight of the glow and popping up when it brightens, three rounds', 22, 'none',
        [k(.2, 'dark_m', x=.3, y=1.3, b=1.2), k(.36, 'dark_m', x=.2, y=1.8, b=1.7, eye='-'), k(.5, 'dark_m', x=.7, y=-.2, b=-.5, w=.8, eye='O', mark='boo'), k(.64, 'dark_m', x=.2, y=1.8, b=1.7, eye='-'), k(.78, 'dark_m', x=.7, y=-.2, b=-.5, w=.8, eye='O', mark='boo!'), k(.9, eye='^')],
        [(0.5, 'fun')], g='play', act=('seek', 'glow'), when=['glow>.4'], prefer=['young', 'happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('puff_a_bubble_to_see_it_glow', 'Blowing one fat bubble down into the dark to watch it light up as the fish noses through it', 18, 'none',
        [k(.2, x=.3, y=.6, b=.4), k(.4, 'dark_r', x=.9, y=1.5, b=.8, eye='-', mark='bbl'), k(.58, 'dark_r', x=1, y=1.7, b=1, eye='O', mark='bloop'), k(.78, 'dark_r', x=.6, y=.9, b=.5, eye='O'), k(.9, eye='^')],
        [], g='play', act=('blow', 'bubble'), when=['glow>.4'], prefer=['young', 'curious'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('creep_after_the_glimmer_in_the_shallows', 'Chasing a glimmer along the shallows on tiptoe, every foot placed in turn, never quite close', 24, 'none',
        [k(.16, 'dark_l', x=.4, y=.2, b=.2, l=1), k(.32, 'deep', x=.5, y=.2, b=.2, r=1), k(.48, 'dark_m', x=.6, y=.1, b=.2, l=1), k(.64, 'edge_far', x=.7, y=.1, b=.2, r=1, mark='psst'), k(.8, 'dark_r', x=.8, y=.1, b=.2, l=1), k(.92, eye='o')],
        [], g='play', act=('chase', 'glimmer'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.6, {'lure': 1}), (0.82, {'lure': 1})])
    o.r('count_the_pulses_of_the_glow', 'Counting the slow pulses of the glow with one foot raised each time it brightens', 22, 'none',
        [k(.16, 'dark_l', x=.3, y=.4, b=.3, l=1, mark='1'), k(.34, 'dark_l', x=.3, y=.4, b=.3, r=1, mark='2'), k(.52, 'dark_l', x=.3, y=.4, b=.3, l=1, mark='3'), k(.7, 'dark_l', x=.3, y=.4, b=.3, r=1, mark='4'), k(.88, eye='-', mark='slow')],
        [], g='test', act=('count', 'pulses'), when=['glow>.4'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Slow. It breathes light like a snore.', 'Counted six, then it dimmed. Rude to a counter.'])
    o.r('peer_at_the_pale_scales', 'Peering close at the pale scales, trying to see through them to the rim stones past', 18, 'none',
        [k(.2, x=.4, y=.6, b=.4), k(.4, 'deep', x=1, y=1.6, b=.9, eye='o'), k(.58, 'deep', x=1.1, y=1.9, b=1.1, eye='@', mark='...'), k(.76, 'deep', x=.4, y=.7, b=.4, eye='O'), k(.9, eye='-')],
        [], g='test', act=('peer', 'scales'), prefer=['curious', 'young'], pick='shyest',
        obj=[(0.38, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('wait_for_the_glow_to_come_on', 'Waiting at the rim for the first faint glow to come on in the water as the light goes', 22, 'none',
        [k(.2, 'pad_low', x=.4, y=.8, b=.5, eye='o'), k(.4, 'pad_low', x=.4, y=.8, b=.5, eye='o'), k(.6, 'pad_low', x=.5, y=1, b=.6, r=1, eye='O', mark='...'), k(.8, 'pad_low', x=.2, y=.5, b=.3, eye='^')],
        [], g='rest', act=('wait', 'glow'), when=['dusk'], prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('shade_the_water_from_the_glare', 'Tilting a wing out over the water to throw shade so the pale fish dares come up in the daylight', 22, 'wing',
        [k(.18, 'dark_m', reach=.4, x=.2, y=.3, b=.3), k(.36, 'dark_m', reach=1, x=.3, y=.1, b=.4, mark='...'), k(.56, 'dark_m', reach=1, x=.3, y=.1, b=.5, l=1), k(.76, 'dark_m', reach=1, x=.3, y=.1, b=.4, r=1), k(.9, eye='^')],
        [], g='weather', act=('tilt', 'wing'), when=['sun'], prefer=['curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_glow_to_the_empty_bank', 'Presenting the glow to the empty bank with a hushed sweep of the wing, a showman whispering', 22, 'wing',
        [k(.18, 'dark_m', reach=.3, x=.3, y=-.3, b=-.3), k(.36, 'dark_m', reach=1, x=.4, y=-.5, b=-.5, l=1), k(.56, 'dark_l', reach=1, x=.4, y=-.6, b=-.6, r=1, mark='ssh'), k(.76, 'dark_l', reach=1, x=.3, y=-.3, b=-.3), k(.9, eye='^')],
        [], g='show', act=('present', 'glow'), when=['glow>.4'], prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('argue_in_a_whisper', 'Arguing with the pale fish in a furious whisper about who is supposed to be the ghost here', 20, 'none',
        [k(.18, 'edge_far', x=.9, y=.5, b=.4), k(.34, 'edge_far', x=1.2, y=.4, b=.3, mark='psst'), k(.5, 'edge_far', x=1.3, y=.3, b=.3, r=1, mark='psst!'), k(.66, 'edge_far', x=1.2, y=.4, b=.3, l=1, mark='psst'), k(.82, 'edge_far', x=.6, y=.5, b=.4), k(.92, eye='-')],
        [], g='show', act=('argue', 'ghost'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It claims the haunting. I claim the tenancy.', 'Lost a whisper fight to a fish. Dignity gone, haunting intact.'])
    o.r('pose_in_the_glow_like_a_statue', 'Striking a pose at the right stone in the glow like a statue, one foot up, never so much as blinking', 20, 'none',
        [k(.18, 'stone_r', x=.2, y=-.2, w=.3, l=1, perch=1), k(.36, 'stone_r', x=.3, y=-.4, b=-.2, w=.5, l=1, perch=1), k(.6, 'stone_r', x=.3, y=-.4, b=-.2, w=.5, l=1, perch=1, eye='-', mark='...'), k(.82, 'stone_r', x=.1, y=-.1, w=.2, perch=1)],
        [], g='show', act=('pose', 'statue'), when=['glow>.4'], prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('jump_back_from_the_sudden_flare', 'Hopping back from the rim when the glow flares up in his face all at once, wings out', 16, 'none',
        [k(.14, 'bank_r', x=.9, y=1.4, b=.9), k(.28, 'bank_r', x=1, y=1.6, b=1, eye='o', mark='...'), k(.4, x=-1.3, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='GAH'), k(.6, x=-.7, y=.3, b=-.1, eye='>'), k(.82, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'flare'), when=['glow>.5'], prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['It lit up. I did not. We are not alike.', 'A flash, a shriek, a duck three feet back. Textbook.'])
    o.r('pass_the_lullaby_down_the_rim', 'Singing the lullaby at the left end of the rim while a friend takes it up at the right, the pale fish hanging between them', 26, 'none',
        [k(.16, 'dark_l', x=1.1, y=1.3, b=1.1, eye='-'), k(.34, 'deep', x=1.3, y=1.7, b=1.4, eye='-', mark='mmm'), k(.52, 'deep', x=1.4, y=1.9, b=1.6, l=1, r=1, eye='-', mark='mmmm'), k(.7, 'dark_l', x=1, y=1.2, b=1, eye='-'), k(.86, eye='^')],
        [(0.52, 'hush')], g='show', act=('sing', 'chorus'), when=['hush<.7'], prefer=['lonely', 'happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Passed the lullaby on. The fish stayed. Rare tribute.', 'A duet in a whisper. It had perfect pitch, probably.'],
        duo=[k(.18, 'dark_r', x=.3, y=.4, b=.3), k(.38, 'dark_r', x=.5, y=.7, b=.5, eye='-', mark='mmm'), k(.58, 'dark_r', x=.6, y=.8, b=.6, r=1, eye='-', mark='mmmm'), k(.78, 'dark_r', x=.3, y=.4, b=.3, eye='^')])
    o.r('light_chain_with_a_friend_the_fish_follows', 'Dragging a glimmer line with a wing while a friend draws another from the far side, the fish tracing both', 26, 'wing',
        [k(.14, 'dark_r', reach=.4, x=1, y=-.2, b=-.4), k(.32, 'edge_far', reach=1, x=1.3, y=.9, b=1, l=1), k(.5, 'dark_m', reach=1, x=1.5, y=1.2, b=1.3, r=1, mark='...'), k(.68, 'deep', reach=1, x=1.3, y=.9, b=1, l=1, r=1), k(.86, eye='^')],
        [(0.5, 'glimmer')], g='play', act=('drag', 'glimmer'), when=['night'], prefer=['happy'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.45, {'lure': 1}), (0.7, {'lure': 1})],
        duo=[k(.16, 'dark_r', x=.3, y=.4, b=.3), k(.34, 'edge_far', x=.6, y=.8, b=.6, r=1), k(.52, 'dark_m', x=.7, y=.9, b=.7, l=1, mark='...'), k(.7, 'deep', x=.7, y=.9, b=.7, r=1), k(.86, eye='^')])
    o.r('count_the_pulses_back_to_back', "Counting the glow's pulses out loud while a friend counts them silently, then swapping totals at the rim", 24, 'none',
        [k(.14, 'dark_m', x=.3, y=.5, b=.3, mark='1'), k(.3, 'dark_m', x=.4, y=.6, b=.4, mark='2'), k(.46, 'dark_m', x=.4, y=.6, b=.4, l=1, mark='3'), k(.64, 'dark_l', x=.5, y=.7, b=.5, mark='6?'), k(.82, 'dark_l', x=.2, y=.4, b=.3, eye='^')],
        [], g='test', act=('count', 'beats'), when=['glow>.4'], prefer=['curious'], pick='hungriest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Six. Or five. Glow pulses when it wants to.', 'Counted aloud and a friend counted silent. Silence won.'],
        duo=[k(.16, 'dark_r', x=.3, y=.4, b=.3), k(.34, 'dark_r', x=.4, y=.5, b=.4, eye='-'), k(.52, 'dark_r', x=.4, y=.5, b=.4, r=1, eye='-', mark='...'), k(.7, 'dark_m', x=.5, y=.7, b=.5, mark='5'), k(.86, eye='^')])
    return o


def golden_koi():
    o = Obj('golden_koi', 'keeping', on='koi_pond', 
            parts=dict(sheen='the sunlit surface of the water', run='the running stretch of surface water', pad='the lily pads floating on the water', bloom='the lily bloom on its pad', bank='the stone bank round the pond', stone='the front rim stones'),
            fields={'shimmer': (0, 0, 1), 'rise': (0, 0, 1)},
            physics=[('shimmer', 'rate', 0.004, 'dawn'), ('shimmer', 'rate', -0.003, '!dawn'), ('rise', 'rate', -0.0003, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                lead=[['rise', 'add', 0.2], ['subject.trust', 'add', 0.1]],
                kiss=[['subject.trust', 'add', 0.1], ['subject.mood', 'add', 0.15]],
                glint=[['shimmer', 'set', 1], ['subject.mood', 'add', 0.15]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('shimmer', 0.3, '.*~*.', 'bloom_r', 'glow')],
            anchors=dict(
                sheen_l=(0.2353, 0.7818),
                sheen_m=(0.4874, 0.7455),
                sheen_r=(0.7395, 0.7091),
                run=(0.5882, 0.7818),
                pad_low=(0.7227, 0.6727),
                bloom_r=(0.6807, 0.6364),
                bank_r=(0.7983, 0.7273),
                stone_m=(0.3445, 0.8364, 'surface'),
            ))
    o.r('untangle_the_long_barbels_from_a_stem', 'Unwrapping the long barbels from a pad stem one at a time with the very tip of a wing', 24, 'wing',
        [k(.15, 'pad_low', reach=.4, x=.3, y=.4, b=.3), k(.34, 'pad_low', reach=1, x=.5, y=.8, b=.7, eye='-'), k(.54, 'sheen_r', reach=1, x=.6, y=1, b=.9, l=1, mark='tug'), k(.72, 'sheen_r', reach=1, x=.4, y=.6, b=.5, r=1, mark='plip'), k(.88, eye='^')],
        [(0.54, 'tend')], g='care', act=('unwrap', 'barbels'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.32, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Free. It looked at me like I owed it gold. Fair.', 'One stem, two barbels, a lot of thanks left unspoken.'])
    o.r('polish_a_dull_patch_of_gold_scales', 'Polishing a dull patch on the golden flank with the soft inside of a wing until it throws light again', 22, 'wing',
        [k(.15, 'sheen_m', reach=.5, x=.3, y=.8, b=.4), k(.33, 'sheen_m', reach=1, x=.5, y=1.3, b=.9, mark='rub'), k(.5, 'sheen_m', reach=1, x=.6, y=1.5, b=1.1, l=1, mark='rub rub'), k(.7, 'sheen_m', reach=1, x=.4, y=1.2, b=.8, r=1), k(.88, eye='^', mark='shine')],
        [(0.5, 'tend')], g='care', act=('polish', 'scales'), prefer=['fish_health<.9', 'happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.68, {'lure': 1})])
    o.r('tilt_a_wing_to_throw_the_light', 'Tilting a wing at the sun so a glint slides over the water and the golden koi rises to meet it', 22, 'wing',
        [k(.12, 'sheen_l', reach=.5, x=.1, y=-.3, b=.1), k(.3, 'sheen_m', reach=1, x=.3, y=-.7, b=-.3, mark='...'), k(.5, 'sheen_m', reach=1, x=.5, y=-.9, b=-.5, l=1, mark='flash'), k(.7, 'run', reach=1, x=.5, y=-.7, b=-.3), k(.88, eye='O')],
        [(0.5, 'glint')], g='use', act=('tilt', 'wing'), when=['dawn_or_day'], prefer=['sun', 'happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Threw a sunbeam. It chased it. Me neither, so far.', 'Gold fish, gold light. Redundant, shining.'])
    o.r('hold_a_flake_to_the_dawn_surface', 'Carrying a flake just to the surface until the golden koi rises up out of the pink water and sips it', 22, 'none',
        [k(.15, x=.3, y=.4, b=.3), k(.35, 'sheen_r', x=1, y=1, b=.7, eye='o', mark='...'), k(.52, 'sheen_r', x=1.1, y=1.3, b=.9, eye='O', mark='sip'), k(.7, 'sheen_r', x=.5, y=.6, b=.4, w=.5, eye='^'), k(.88, eye='-')],
        [(0.52, 'feed')], g='use', act=('carry', 'flake'), when=['fish_hunger>.4'], prefer=['dawn'], pick='hungriest',
        obj=[(0.35, {'lure': 1}), (0.62, {'lure': 1}), (0.8, {'lure': 0})],
        say=['Sipped from my bill. A nibble of royalty.', 'Hand-fed a golden fish. Do not tell the others, they are plain.'])
    o.r('lead_it_through_the_blooms_with_a_wingtip', 'Leading the golden koi through the blooms as it chases a wingtip, round one pad and out past the next', 26, 'wing',
        [k(.12, 'sheen_l', reach=.5, x=.2, y=.4, b=.2), k(.3, 'sheen_m', reach=1, x=.6, y=.2, b=.4), k(.5, 'bloom_r', reach=1, x=.8, y=.1, b=.6, r=1), k(.7, 'pad_low', reach=1, x=.8, y=.2, b=.6, l=1), k(.88, 'sheen_r', reach=1, x=.5, y=.4, b=.3)],
        [(0.5, 'lead')], g='use', act=('chase', 'wingtip'), when=['rise<.8'], pick='hungriest',
        obj=[(0.15, {'lure': 1}), (0.32, {'lure': 1}), (0.55, {'lure': 0}), (0.75, {'lure': 1})],
        say=['It looped a lily like it owned the lease.', 'Led a gold fish about. No bribe was needed.'])
    o.r('offer_the_bill_tip_to_be_mouthed', 'Pressing the very tip of his bill to be mouthed, gently, by the golden koi as it noses up', 20, 'none',
        [k(.15, x=.6, y=.2, b=.8), k(.34, 'sheen_l', x=1, y=1.3, b=.8, eye='-', mark='...'), k(.52, 'sheen_l', x=1.1, y=1.5, b=1, eye='-', mark='mwah'), k(.7, 'sheen_l', x=.6, y=.8, b=.5, w=.3, eye='^'), k(.88, eye='-')],
        [(0.52, 'kiss')], g='use', act=('press', 'bill'), prefer=['fish_trust<.8', 'happy'], pick='shyest',
        obj=[(0.34, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('race_the_gold_along_the_pads', 'Having a race with the golden koi from pad to pad along the far side, arms out, a streak of gold well ahead', 20, 'none',
        [k(.1, 'sheen_l', x=.4, y=-.3, b=.2, w=.5), k(.28, 'run', x=1, y=-.4, b=-.7, l=1, w=1), k(.46, 'sheen_r', x=1.4, y=-.4, b=-.9, r=1, w=1, mark='whoosh'), k(.64, 'pad_low', x=1.5, y=-.2, b=-.6, l=1, w=.9), k(.84, 'bank_r', x=.4, y=.4, b=.3, eye='@')],
        [(0.46, 'fun')], g='play', act=('race', 'pads'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Lost to an ornament. Of course. It is gold.', 'Beaten by a flake with fins. Pride in the bin.'])
    o.r('pop_up_from_the_bloom_with_a_cheep', 'Playing seek, ducking at the right bloom, then popping up with a cheep just as the golden koi comes round it', 22, 'none',
        [k(.14, 'bloom_r', x=.3, y=1.2, b=1.3, w=.2), k(.32, 'bloom_r', x=.2, y=1.6, b=1.7, eye='-'), k(.5, 'bloom_r', x=.5, y=-.9, b=-1, w=1, eye='O', mark='CHEEP'), k(.66, 'bloom_r', x=.2, y=1.6, b=1.6, eye='-'), k(.8, 'bloom_r', x=.5, y=-.7, b=-.8, w=.9, mark='CHEEP!'), k(.92, eye='^')],
        [], g='play', act=('seek', 'koi'), prefer=['young', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.82, {'lure': 1})])
    o.r('trade_bubbles_with_the_gold', 'Trading bubbles with the golden koi, one for one, until it blows a bigger one that bursts on his bill', 20, 'none',
        [k(.14, x=.4, y=.4, b=.4), k(.3, 'sheen_m', x=1.1, y=1.5, b=1, mark='blp'), k(.48, 'sheen_m', x=1.2, y=1.7, b=1.2, eye='O', mark='blp blp'), k(.66, 'sheen_m', x=1.4, y=1.9, b=1.4, eye='@', mark='POP'), k(.84, x=.4, y=.6, b=.5, eye='^')],
        [], g='play', act=('blow', 'bubbles'), prefer=['happy', 'young'], pick='shyest',
        obj=[(0.32, {'lure': 1}), (0.66, {'lure': 1})])
    o.r('count_the_gold_flecks_on_its_flank', 'Counting the gold flecks along its flank, bill tap by bill tap, from gill to tail', 24, 'none',
        [k(.12, 'sheen_l', x=.9, y=1.1, b=.6, mark='1'), k(.28, 'sheen_l', x=1, y=1.3, b=.7, mark='2'), k(.44, 'sheen_m', x=1, y=1.3, b=.7, l=1, mark='3'), k(.6, 'sheen_m', x=1.1, y=1.5, b=.8, r=1, mark='4'), k(.78, eye='-', mark='lots')],
        [], g='test', act=('count', 'flecks'), prefer=['curious'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('hold_it_up_against_the_sunrise', 'Comparing a wing held up beside the sunrise and then beside the golden koi to see which is more gold', 22, 'wing',
        [k(.14, 'sheen_m', reach=.4, x=.2, y=-.8, b=-.2), k(.32, 'sheen_m', reach=1, x=.3, y=-1.2, b=-.4, mark='hm'), k(.5, 'sheen_r', reach=1, x=.5, y=.9, b=.6, l=1), k(.68, 'sheen_r', reach=1, x=.5, y=.9, b=.6, r=1, mark='koi'), k(.86, eye='-', mark='koi')],
        [], g='test', act=('compare', 'gold'), when=['dawn'], prefer=['curious', 'happy'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('wait_for_the_gold_to_rise', 'Waiting at the rim, still as a post, for the golden koi to rise into the first light', 24, 'none',
        [k(.14, 'sheen_r', x=.9, y=.9, b=.7, eye='o'), k(.4, 'sheen_r', x=1, y=1, b=.9, eye='o'), k(.62, 'sheen_r', x=1, y=1.1, b=.9, r=1, eye='O', mark='...'), k(.8, 'sheen_r', x=.4, y=.5, b=.3, eye='^')],
        [], g='rest', act=('wait', 'gold'), when=['dawn'], prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_gold_to_the_sun', 'Presenting the golden koi to the sun itself with an upward sweep of the wing, a showman to the sky', 22, 'wing',
        [k(.14, 'sheen_l', reach=.3, x=.1, y=-.4, b=-.3), k(.32, 'sheen_m', reach=1, x=.3, y=-.8, b=-.5, l=1), k(.52, 'sheen_m', reach=1, x=.4, y=-1.1, b=-.7, r=1, mark='BEHOLD'), k(.72, 'sheen_m', reach=1, x=.2, y=-.6, b=-.4), k(.88, eye='^')],
        [], g='show', act=('present', 'koi'), prefer=['happy'], pick='shyest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('argue_over_which_of_them_shines', 'Arguing with the golden koi about which of them shines brighter, flashing a wing at its flank', 22, 'wing',
        [k(.12, 'sheen_m', reach=.5, x=.9, y=.1, b=.8), k(.28, 'sheen_m', reach=1, x=1.3, y=-.3, b=.3, mark='ME'), k(.44, 'sheen_m', reach=.3, x=.2, y=-.2, b=.2), k(.6, 'sheen_m', reach=1, x=1.4, y=-.3, b=.3, l=1, mark='ME'), k(.78, 'sheen_m', reach=.5, x=.8, y=.2, b=.6), k(.9, eye='-')],
        [], g='show', act=('argue', 'shine'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.64, {'lure': 1})],
        say=['It shines on its own. I need a lamp. Unfair.', 'Argued with a mirror that has fins. Lost to the mirror.'])
    o.r('pose_with_one_wing_gilded', 'Striking a pose at the middle stone with one wing held up gilded in the light, hip out', 20, 'none',
        [k(.14, 'stone_m', x=.1, y=-.4, b=-.1, w=.4, perch=1), k(.34, 'stone_m', x=.3, y=-.8, b=-.4, w=1, l=1, perch=1), k(.56, 'stone_m', x=.4, y=-.9, b=-.5, w=1, r=1, perch=1, eye='^', mark='gilded'), k(.78, 'stone_m', x=.2, y=-.3, b=-.1, w=.4, perch=1)],
        [], g='show', act=('pose', 'wing'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('hop_back_from_the_gold_flash', 'Hopping back from the rim with one wing over his eyes as the golden koi flashes at the surface', 16, 'none',
        [k(.14, 'bank_r', x=.9, y=1.3, b=.8), k(.28, 'bank_r', x=1, y=1.5, b=1, eye='o', mark='...'), k(.4, x=-1.3, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='AH'), k(.58, x=-.7, y=.1, b=-.1, w=.8, eye='>'), k(.8, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'glare'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['It flashed. I flinched. It saw.', 'Blinded by a fish. Mark it on the wall of shame.'])
    o.r('bounce_the_glint_between_two_wings', "Tilting a wing to throw a glint to a friend's wing across the water, the golden koi leaping to catch each pass", 26, 'wing',
        [k(.12, 'sheen_l', reach=.4, x=.1, y=-.3, b=.1), k(.3, 'sheen_m', reach=1, x=.3, y=-.7, b=.6), k(.5, 'run', reach=1, x=.5, y=-.9, b=-.5, r=1, mark='flash'), k(.7, 'sheen_r', reach=1, x=.5, y=-.7, b=-.3, l=1), k(.88, eye='^')],
        [(0.5, 'cheer')], g='play', act=('throw', 'glint'), when=['dawn_or_day'], prefer=['happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1}), (0.75, {'lure': 1})],
        say=['Bounced a sunbeam off a pal. Caught on the fish.', 'Light, passed hand to hand. Fish took the receipt.'],
        duo=[k(.16, 'sheen_r', reach=.4, x=.1, y=-.3, b=.1), k(.34, 'sheen_r', reach=1, x=.4, y=-.8, b=-.4, mark='flash'), k(.54, 'run', reach=1, x=.5, y=-.9, b=-.5, l=1), k(.74, 'sheen_m', reach=1, x=.4, y=-.7, b=-.3), k(.9, eye='^')])
    o.r('count_the_gold_rings_in_turn', 'Counting the gold rings the koi leaves on the water with a friend, taking alternate rings, never agreeing', 24, 'none',
        [k(.12, 'sheen_l', x=.6, y=.9, b=.5, mark='1'), k(.3, 'sheen_m', x=.7, y=1, b=.5, mark='3'), k(.48, 'run', x=.7, y=1, b=.5, l=1, mark='5'), k(.66, 'sheen_r', x=.7, y=1, b=.5, r=1, mark='7?'), k(.84, eye='^')],
        [], g='test', act=('count', 'rings'), when=['shimmer>.4'], prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.34, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Odd for me, even for them, none for the koi.', 'Seven rings. Eight if you are generous. I am not.'],
        duo=[k(.14, 'sheen_r', x=.6, y=.9, b=.5), k(.34, 'run', x=.7, y=1, b=.5, mark='2'), k(.52, 'sheen_m', x=.7, y=1, b=.5, r=1, mark='4'), k(.7, 'sheen_l', x=.7, y=1, b=.5, l=1, mark='6'), k(.86, eye='^')])
    o.r('brace_a_wing_against_the_gust_to_still_the_bloom', 'Bracing a wing against the gust to hold the bloom still for the gold to rise beside', 22, 'wing',
        [k(.12, 'bloom_r', reach=.4, x=.2, y=.4, b=.5), k(.3, 'bloom_r', reach=1, x=.4, y=.5, b=.8, w=.8), k(.55, 'bloom_r', reach=1, x=.5, y=.6, b=1, w=1, l=1, mark='fff'), k(.78, 'bloom_r', reach=.6, x=.2, y=.4, b=.6, eye='^'), k(.9, eye='-')],
        [(.55, 'cheer')], g='weather', act=('brace', 'bloom'), when=['windy'], pick='hungriest',
        obj=[(.3, {'lure': 1}), (.65, {'lure': 1})], say=['The bloom stayed put. So did the gold. I did not.', 'Held a flower still in a gale. Put that on a medal.'])
    return o


def minnow():
    o = Obj('minnow', 'keeping', on='koi_pond', 
            parts=dict(swirl='the open water along the rim', shoal='the shallow water at the stones', cove='the sheltered water between the pads', bank='the stone bank round the pond', stone='the front rim stones'),
            fields={'swirl': (0, 0, 1)},
            physics=[('swirl', 'rate', -0.0004, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                rejoin=[['swirl', 'add', 0.25], ['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                herd=[['swirl', 'add', 0.25], ['subject.trust', 'add', 0.1]],
                lead=[['swirl', 'add', 0.2], ['subject.mood', 'add', 0.15]],
                nibble=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('swirl', 0.3, 'o~o~o', 'swirl_m', 'water')],
            anchors=dict(
                swirl_l=(0.2353, 0.7818),
                swirl_m=(0.4874, 0.7455),
                swirl_r=(0.7395, 0.7091),
                shoal=(0.5882, 0.7818),
                cove=(0.3361, 0.7091),
                bank_r=(0.7983, 0.7273),
                stone_l=(0.2521, 0.8364, 'surface'),
            ))
    o.r('shoo_the_stray_back_to_the_shoal', 'Nudging a straggling minnow back to the others with small flicks of a wing, left to right', 22, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.26, 'swirl_l', reach=1, x=.5, y=.7, b=.5, l=1, mark='shoo'), k(.42, 'swirl_m', reach=1, x=.5, y=.7, b=.5, r=1, mark='shoo'), k(.58, 'shoal', reach=1, x=.5, y=.7, b=.5, l=1, mark='shoo'), k(.76, 'shoal', reach=.5, x=.3, y=.4, b=.3), k(.9, eye='^')],
        [(0.58, 'rejoin')], g='care', act=('nudge', 'stray'), when=['swirl<.5'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.6, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Back with the others. It clearly has no plans.', 'Herded a fish one inch. Sheepdog duck.'])
    o.r('free_a_minnow_caught_in_the_weed', 'Unwrapping a minnow caught in a weed strand with the very tip of his bill, a peck and a gentle pull', 22, 'none',
        [k(.1, x=.4, y=.4, b=.3), k(.24, 'swirl_l', x=1, y=1.3, b=.6, eye='-'), k(.38, 'swirl_l', x=1.2, y=1.6, b=.9, l=1, mark='nip'), k(.52, 'swirl_l', x=1.3, y=1.7, b=1, r=1, mark='tug'), k(.68, 'swirl_l', x=.6, y=.8, b=.4, w=.4, mark='plip'), k(.86, eye='^')],
        [(0.52, 'tend')], g='care', act=('unwrap', 'minnow'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.22, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('feed_crumbs_one_at_a_time', 'Carrying crumbs one at a time to the water, each one vanishing into a different mouth', 22, 'none',
        [k(.1, x=.3, y=.3, b=.3), k(.22, 'swirl_r', x=1, y=1, b=.6, mark='plip'), k(.34, 'swirl_r', x=1, y=1.1, b=.6, l=1, mark='plip'), k(.46, 'swirl_m', x=1.1, y=1.2, b=.7, mark='plip plip'), k(.58, 'swirl_m', x=1.1, y=1.2, b=.7, eye='O', mark='gone'), k(.76, 'swirl_m', x=.5, y=.5, b=.3, w=.3, eye='^')],
        [(0.46, 'feed')], g='use', act=('carry', 'crumb'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.24, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 0})],
        say=['Crumb in, crumb gone. Seven mouths, one bill.', 'Fed a school with a bill. Tiny logistics, huge ego.'])
    o.r('ribbon_the_school_behind_a_wingtip', 'Dragging a wingtip in a loose figure of eight so the school ribbons after it, tight as a scarf', 24, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.24, 'swirl_m', reach=1, x=.5, y=.6, b=.5, l=1), k(.38, 'shoal', reach=1, x=.6, y=.6, b=.5, r=1), k(.52, 'swirl_r', reach=1, x=.6, y=.6, b=.5, l=1), k(.66, 'shoal', reach=1, x=.5, y=.6, b=.5, r=1), k(.8, 'swirl_m', reach=.6, x=.3, y=.4, b=.3), k(.92, eye='^')],
        [(0.52, 'lead')], g='use', act=('drag', 'wingtip'), when=['swirl<.7'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.28, {'lure': 1}), (0.45, {'lure': 1}), (0.62, {'lure': 1}), (0.78, {'lure': 1})],
        say=['Ribboned a school. It wore me like a scarf.', 'A figure of eight, drawn by a duck, finished by a hundred fish.'])
    o.r('dangle_a_toe_for_the_nibblers', 'Dangling a toe at the left stone until the minnows tap and nibble it, then trying hard not to giggle', 20, 'none',
        [k(.1, 'stone_l', x=.2, y=.3, b=.7, l=1), k(.24, 'stone_l', x=.3, y=.6, b=1, l=1, mark='...'), k(.4, 'swirl_l', x=.4, y=.9, b=1.2, l=1, eye='O', mark='tickle'), k(.52, 'swirl_l', x=.4, y=.9, b=1.3, l=1, eye='>', mark='hee'), k(.68, 'swirl_l', x=.3, y=.7, b=1, l=1, eye='-'), k(.86, eye='^')],
        [(0.4, 'nibble')], g='use', act=('tap', 'toe'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.6, {'lure': 1})],
        say=['They nibble. I giggle. Neither party admits anything.', 'A toe is the best flake. Said the school.'])
    o.r('chase_the_school_down_the_rim', 'Chasing the school along the rim in bounds, bill snapping after the back of the pack', 18, 'none',
        [k(.08, 'swirl_l', x=.5, y=.5, b=-.4, l=1), k(.2, 'cove', x=.8, y=.6, b=-.5, r=1, w=.5), k(.32, 'swirl_m', x=1, y=.6, b=-.5, l=1, w=.6, mark='snp'), k(.44, 'shoal', x=1.1, y=.6, b=-.5, r=1, w=.6), k(.58, 'swirl_r', x=1.2, y=.6, b=-.5, l=1, w=.6, mark='snp'), k(.78, 'bank_r', x=.3, y=.4, b=.3, eye='@')],
        [(0.44, 'fun')], g='play', act=('chase', 'school'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.3, {'lure': 1}), (0.46, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Never caught one. They move as one thought, a mean one.', 'Chased silver. Got wet air. Fine day.'])
    o.r('seek_the_one_that_hides_in_the_shoal', 'Seeking the one minnow that has hidden in the shoal, a bill on each flash until it gives itself away', 22, 'none',
        [k(.1, 'shoal', x=.7, y=.7, b=.5, eye='o'), k(.24, 'swirl_m', x=.8, y=.9, b=.6, eye='o', mark='that one?'), k(.4, 'swirl_r', x=.9, y=1, b=.7, l=1, eye='O', mark='no'), k(.56, 'cove', x=.9, y=1, b=.7, r=1, eye='o', mark='that?'), k(.72, 'swirl_l', x=1, y=1.1, b=.8, eye='O', mark='YES'), k(.88, eye='^')],
        [], g='play', act=('seek', 'minnow'), prefer=['young', 'curious'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.5, {'lure': 1}), (0.75, {'lure': 1})])
    o.r('puff_a_curtain_of_bubbles', 'Blowing a curtain of tiny bubbles into the water so the school weaves in and out of it', 18, 'none',
        [k(.1, x=.3, y=.4, b=.3), k(.22, 'swirl_r', x=1, y=1.4, b=.8, mark='bl'), k(.34, 'shoal', x=1.1, y=1.5, b=.9, l=1, eye='-', mark='bl bl'), k(.46, 'swirl_m', x=1.2, y=1.6, b=1, r=1, mark='bl bl bl'), k(.6, 'cove', x=1.1, y=1.5, b=.9, l=1, mark='bl bl'), k(.78, 'cove', x=.7, y=.9, b=.5, eye='O'), k(.9, eye='^')],
        [], g='play', act=('blow', 'bubbles'), prefer=['young', 'happy'], pick='shyest',
        obj=[(0.26, {'lure': 1}), (0.5, {'lure': 1}), (0.72, {'lure': 1})])
    o.r('count_the_school_by_sixes', 'Counting the school in sixes with a tap of the bill on the water, then giving up and starting over', 24, 'none',
        [k(.1, 'swirl_l', x=.8, y=1, b=.5, mark='6'), k(.22, 'swirl_m', x=.9, y=1.1, b=.6, l=1, mark='12'), k(.36, 'swirl_m', x=.9, y=1.1, b=.6, r=1, mark='18'), k(.5, 'shoal', x=1, y=1.2, b=.7, l=1, mark='2?'), k(.64, 'shoal', x=1, y=1.2, b=.7, eye='>', mark='again'), k(.82, eye='-')],
        [], g='test', act=('count', 'minnows'), prefer=['curious'], pick='hungriest',
        obj=[(0.26, {'lure': 1}), (0.56, {'lure': 1})],
        say=['Eleven. Twenty. Nineteen. It will not hold still for a number.', 'Counted sixes, lost the sixth, started the whole job over.'])
    o.r('peer_close_at_a_silver_flank', 'Peering close at one silver flank, trying to find the one stripe all of them seem to share', 18, 'none',
        [k(.1, x=.4, y=.6, b=.4), k(.26, 'swirl_l', x=1, y=1.7, b=1, eye='o'), k(.42, 'swirl_l', x=1.1, y=2, b=1.2, eye='@', mark='...'), k(.58, 'swirl_l', x=.5, y=.9, b=.6, eye='-'), k(.76, 'swirl_l', x=1, y=1.8, b=1.1, eye='o', mark='hm'), k(.9, eye='-')],
        [], g='test', act=('peer', 'flank'), prefer=['curious', 'young'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('wait_for_the_school_to_return', 'Waiting at the rim for the school to come back round the cove after a scare', 22, 'none',
        [k(.1, 'cove', x=.5, y=.9, b=.6, eye='o'), k(.3, 'cove', x=.5, y=.9, b=.6, eye='o'), k(.5, 'swirl_m', x=.6, y=1, b=.7, l=1, eye='O', mark='...'), k(.7, 'swirl_m', x=.6, y=1, b=.7, r=1, eye='O'), k(.86, 'swirl_m', x=.2, y=.4, b=.3, eye='^')],
        [], g='rest', act=('wait', 'school'), when=['swirl<.5'], prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.82, {'lure': 1})])
    o.r('bow_to_the_school_in_unison', 'Bowing to the school in a quick series, one dip per wheel of the silver', 16, 'none',
        [k(.1, 'shoal', x=.3, y=.7, b=.5), k(.22, 'shoal', x=.9, y=1.7, b=1.1, eye='-'), k(.34, 'shoal', x=.2, y=.2, b=.1), k(.46, 'shoal', x=.9, y=1.7, b=1.1, eye='-', mark='sirs'), k(.58, 'shoal', x=.2, y=.2, b=.1), k(.7, 'shoal', x=.9, y=1.7, b=1.1, eye='-'), k(.86, eye='^')],
        [], g='show', act=('bow', 'school'), prefer=['happy'], pick='hungriest',
        obj=[(0.24, {'lure': 1}), (0.48, {'lure': 1}), (0.72, {'lure': 1})],
        say=['Bowed three times. The school bowed once, for all of them.', 'Honoured a crowd of fish. I deserve a medal. A flake.'])
    o.r('present_the_school_as_one_fish', 'Presenting the school to the bank as one very large fish with a long wing sweep', 20, 'wing',
        [k(.1, 'swirl_l', reach=.3, x=.3, y=-.2, b=.2), k(.26, 'swirl_m', reach=1, x=.3, y=-.4, b=-.3, l=1), k(.42, 'shoal', reach=1, x=.4, y=-.5, b=-.4, r=1, mark='ONE'), k(.58, 'swirl_r', reach=1, x=.4, y=-.5, b=-.4, l=1), k(.76, 'swirl_r', reach=.6, x=.2, y=-.2, b=.1), k(.9, eye='^')],
        [], g='show', act=('present', 'shoal'), when=['swirl>.3'], prefer=['happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('argue_with_a_whole_school', 'Arguing with the whole school at once, a bill-jab at every one that dares to flick back', 20, 'none',
        [k(.1, 'swirl_m', x=.8, y=.4, b=.5), k(.24, 'swirl_m', x=1.2, y=.4, b=.3, mark='HEY'), k(.34, 'swirl_r', x=1.3, y=.3, b=.3, r=1, mark='YOU'), k(.46, 'swirl_l', x=1.3, y=.3, b=.3, l=1, mark='AND YOU'), k(.62, 'swirl_m', x=1.2, y=.4, b=.3, mark='ALL OF YOU'), k(.8, 'swirl_m', x=.6, y=.5, b=.4), k(.9, eye='-')],
        [], g='show', act=('argue', 'school'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.26, {'lure': 1}), (0.64, {'lure': 1})],
        say=['Fifty of them, one of me. Naturally I won.', 'It turned as one and left. Argument ended by exit.'])
    o.r('pose_in_the_swirl_like_a_sculpture', 'Striking a pose at the left stone with a wing extended and one foot up, the school wheeling round him like a sculpture', 20, 'none',
        [k(.1, 'stone_l', x=.1, y=-.2, w=.4, perch=1), k(.26, 'stone_l', x=.4, y=-.5, b=-.2, w=.9, l=1, perch=1), k(.46, 'stone_l', x=.5, y=-.6, b=-.3, w=1, l=1, perch=1, eye='^', mark='art'), k(.66, 'stone_l', x=.3, y=-.3, b=-.1, w=.7, r=1, perch=1), k(.84, 'stone_l', perch=1)],
        [], g='show', act=('pose', 'sculpture'), when=['swirl>.3'], prefer=['happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('flinch_when_the_school_leaps_at_his_face', 'Hopping back with a yell when the whole school flicks up at the surface at his bill, a hundred tiny splashes', 16, 'none',
        [k(.1, 'swirl_r', x=.9, y=1.4, b=.8), k(.22, 'swirl_r', x=1, y=1.6, b=1, eye='o', mark='...'), k(.32, x=-1.3, y=-.9, b=-1.4, l=1, r=1, w=1, eye='O', mark='AAH'), k(.5, x=-.7, y=.2, b=-.1, w=.7, eye='>'), k(.7, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'splashes'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.22, {'lure': 1}), (0.5, {'lure': 1})],
        say=['A hundred minnows. One duck. Immediate retreat.', 'They flicked. I flew. Very efficient, both sides.'])
    o.r('herd_the_school_from_both_ends', 'Chasing the school (herding it) from the left rim with a friend herding from the right until it balls up in the middle', 24, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.26, 'swirl_l', reach=1, x=.5, y=.6, b=.5, l=1, mark='shoo'), k(.42, 'cove', reach=1, x=.6, y=.6, b=.5, r=1, mark='shoo'), k(.6, 'swirl_m', reach=1, x=.7, y=.6, b=.5, l=1, mark='shoo'), k(.78, eye='^')],
        [(0.42, 'herd')], g='use', act=('chase', 'shoal'), when=['swirl<.7'], prefer=['happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.45, {'lure': 1}), (0.65, {'lure': 1})],
        say=['Ball formed. Both ends took credit. Minnows took a vote.', 'Two ducks, one school. It chose the middle.'],
        duo=[k(.12, 'swirl_r', x=.3, y=.4, b=.3), k(.3, 'swirl_r', x=.8, y=.7, b=.6, l=1, mark='shoo'), k(.48, 'shoal', x=.9, y=.8, b=.7, r=1, mark='shoo'), k(.66, 'swirl_m', x=.9, y=.8, b=.7, l=1, mark='shoo'), k(.84, eye='^')])
    o.r('toss_flakes_back_and_forth_over_the_school', 'Throwing flakes back and forth with a friend over the school, so it surges after each flake in the air', 24, 'none',
        [k(.1, 'swirl_l', x=.4, y=.3, b=.3), k(.24, 'swirl_l', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.38, 'swirl_m', x=1, y=.4, b=.5, eye='o'), k(.52, 'swirl_m', x=.9, y=-.6, b=-.9, w=.5, r=1, mark='fwip'), k(.68, 'swirl_m', x=1, y=.4, b=.5, eye='O'), k(.84, eye='^')],
        [(0.38, 'fun')], g='play', act=('throw', 'flake'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.4, {'lure': 1}), (0.7, {'lure': 1})],
        duo=[k(.12, 'swirl_r', x=.4, y=.3, b=.3), k(.3, 'swirl_r', x=1, y=.4, b=.5, eye='o'), k(.46, 'swirl_m', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.62, 'swirl_r', x=1, y=.4, b=.5), k(.8, eye='^')])
    o.r('tally_the_school_with_a_friend', 'Tallying the school with a friend, bill to bill over a count that will not stay still, finishing with a shrug', 24, 'none',
        [k(.1, 'cove', x=1.3, y=.3, b=1.1, mark='20'), k(.24, 'shoal', x=1.5, y=.4, b=1.4, l=1, mark='25'), k(.38, 'swirl_r', x=1.5, y=.4, b=1.4, r=1, mark='30?'), k(.54, 'swirl_r', x=-.4, y=-.5, b=-.6, w=.9, mark='forty'), k(.7, 'shoal', x=1.1, y=.3, b=1, eye='-', mark='shrug'), k(.86, eye='^')],
        [], g='test', act=('count', 'fry'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Twenty. Forty. Never the same fish twice. Fine.', 'Two counters, one school, forty-one answers. Math is fluid.'],
        duo=[k(.12, 'swirl_r', x=.7, y=.8, b=.4, mark='22'), k(.3, 'swirl_r', x=.8, y=.9, b=.5, mark='28'), k(.46, 'shoal', x=.8, y=.9, b=.5, r=1, mark='35'), k(.62, 'swirl_m', x=.9, y=1, b=.6, l=1, mark='41'), k(.8, eye='-')])
    o.r('tap_the_rain_beat_for_the_school', 'Tapping the surface with a wing to the beat of the rain so the school rises to meet each drop', 20, 'wing',
        [k(.12, 'swirl_r', reach=.5, x=.3, y=.6, b=.4), k(.3, 'swirl_r', reach=1, x=.4, y=.8, b=.6, w=.5, mark='tp'), k(.5, 'swirl_l', reach=1, x=.4, y=.8, b=.6, l=1, w=.5, mark='tp tp'), k(.7, 'swirl_r', reach=1, x=.4, y=.8, b=.6, r=1, mark='tp'), k(.88, eye='^')],
        [(.5, 'cheer')], g='weather', act=('tap', 'rain'), when=['wet'], pick='hungriest',
        obj=[(.3, {'lure': 1}), (.55, {'lure': 1}), (.75, {'lure': 1})], say=['They rose to my beat. I am a conductor of fish.', 'Rain plus wing. A school came. Music.'])
    return o


def salmon():
    o = Obj('salmon', 'keeping', on='koi_pond', 
            parts=dict(run='the running stretch of surface water', rapid='the stretch of rippled water', pad='the lily pads floating on the water', bloom='the lily bloom on its pad', cattail='the cattail stems at the pond edge', reed='the reed stems at the pond edge', tuft='the grass tuft at the pond foot', bank='the stone bank round the pond', stone='the front rim stones'),
            fields={'run': (0, 0, 1), 'spray': (0, 0, 1), 'homing': (0, 0, 1)},
            physics=[('run', 'rate', -0.0004, 'always'), ('spray', 'rate', -0.004, 'always'), ('homing', 'rate', -0.0003, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                leap=[['spray', 'set', 1], ['subject.hunger', 'add', -0.2], ['run', 'add', 0.25]],
                lead=[['homing', 'add', 0.2], ['subject.trust', 'add', 0.1]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('spray', 0.3, "'.:.'", 'bloom_r', 'water'), ('run', 0.4, '>>>>', 'run_m', 'water')],
            anchors=dict(
                run_l=(0.2353, 0.7818),
                run_m=(0.4874, 0.7455),
                run_r=(0.7395, 0.7091),
                rapid=(0.5882, 0.7818),
                pad_low=(0.7227, 0.6727),
                bloom_r=(0.6807, 0.6364),
                cattail_l=(0.0588, 0.5636),
                reed_low=(0.0672, 0.6909),
                tuft=(0.0924, 0.8),
                bank_r=(0.7983, 0.7273),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364, 'surface'),
            ))
    o.r('look_over_the_torn_fin', "Peering at the salmon's tail fin for a ragged edge from the last bad landing, bill almost touching the water", 22, 'none',
        [k(.07, x=.6, y=.2, b=.2), k(.2, 'run_l', x=1.6, y=2.3, b=1.4, eye='o'), k(.38, 'run_l', x=1.8, y=2.5, b=1.7, eye='O', l=1, mark='hm'), k(.55, 'run_m', x=1.5, y=2.1, b=1.3, r=1, mark='tsk'), k(.75, 'run_m', x=.7, y=.6, b=.3, w=.5, eye='^'), k(.9, eye='-')],
        [(0.38, 'tend')], g='care', act=('peer', 'fin'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Fin intact. Pride dented, which heals itself.', 'Frayed at the tip. Join the club, mate.'])
    o.r('wipe_the_grit_off_the_snout', "Taking a wipe at the grit off the salmon's hooked snout with the back of a wing as it noses up to the rim", 20, 'wing',
        [k(.12, 'run_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'run_l', reach=1, x=.4, y=1.7, b=1.1, mark='wp'), k(.5, 'run_l', reach=1, x=.3, y=2.2, b=1.3, l=1, mark='wp wp'), k(.7, 'run_l', reach=1, x=.3, y=1.3, b=1), k(.88, eye='^')],
        [(0.5, 'tend')], g='care', act=('wipe', 'snout'), prefer=['fish_health<.9', 'happy'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.65, {'lure': 1})])
    o.r('hold_a_flake_high_for_the_leap', 'Lifting a flake pinched in his bill high above the water until the salmon launches up and snatches it', 22, 'none',
        [k(.12, x=.3, y=-.2, w=.2), k(.3, 'run_m', x=.9, y=-.5, b=-.2, eye='o', mark='...'), k(.46, 'run_m', x=1.2, y=-.9, b=-.5, w=.4, eye='O', mark='WHAP'), k(.64, x=-.7, y=.1, b=.3, w=.8, eye='>'), k(.84, eye='^')],
        [(0.46, 'leap')], g='use', act=('lift', 'flake'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Took it mid-air and left. Rude, impressive.', 'Almost lost the bill. Worth it.'])
    o.r('hand_feed_a_flake_at_the_rim', 'Carrying one flake out in his bill just over the rim for the shy salmon to rise and take', 20, 'none',
        [k(.1, x=.2, y=.3), k(.26, 'run_l', x=1.7, y=2, b=.8, eye='o'), k(.44, 'run_l', x=1.9, y=2.2, b=.9, l=1, eye='O', mark='slurp'), k(.6, 'run_l', x=1.4, y=1.5, b=.5), k(.8, x=.5, y=.5, w=.3, eye='^')],
        [(0.44, 'feed')], g='care', act=('carry', 'flake'), when=['fish_hunger>.4'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1}), (0.78, {'lure': 0})],
        say=['It took the flake and my full confidence.', 'One flake. It looked at me like I owed it more.'])
    o.r('draw_it_up_the_home_bank', 'Dragging a wingtip along the water toward the right bank so the salmon swims the way it remembers home', 26, 'wing',
        [k(.07, 'run_l', reach=.4, x=.3, y=.4), k(.22, 'run_l', reach=1, x=.7, y=.5, b=.7), k(.4, 'run_m', reach=1, x=.9, y=.5, b=.2, l=1), k(.58, 'rapid', reach=1, x=1.1, y=.5, b=.8, r=1), k(.76, 'bank_r', reach=1, x=1.3, y=.4, b=.3, l=1), k(.92, eye='^')],
        [(0.4, 'lead')], g='use', act=('drag', 'wingtip'), when=['homing<.7'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.75, {'lure': 1})],
        say=['It knows the bank better than I do. I just hold the wing.', 'Led it home. It would have gone anyway.'])
    o.r('pat_the_silver_flank', "Patting the salmon's silver flank with the back of a wing as it holds still against the rim", 20, 'wing',
        [k(.09, 'run_r', reach=.4, x=.1, y=.5, b=.2), k(.25, 'run_r', reach=.8, x=.5, y=1, b=.9, mark='pat'), k(.43, 'run_r', reach=1, x=.6, y=1.2, b=1, r=1, mark='pat'), k(.6, 'run_r', reach=1, x=.4, y=1, b=.7, l=1, mark='pat pat'), k(.78, 'run_r', reach=.5, x=.2, y=.6, b=.4), k(.92, eye='^')],
        [(0.43, 'stroke')], g='use', act=('pat', 'flank'), prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('raise_the_twig_hoop_for_a_leap', "Lifting a twig bent in a loop at arm's length over the water until the salmon sails through it", 24, 'twig',
        [k(.1, 'bloom_r', reach=.5, x=.2, y=-.1), k(.28, 'bloom_r', reach=1, x=.4, y=-.5, b=-.2, mark='hup'), k(.46, 'bloom_r', reach=1, x=.5, y=-1.4, b=-.4, w=.4, mark='WHOOSH'), k(.66, 'pad_low', reach=1, x=.3, y=-.3, b=-.2), k(.86, eye='^')],
        [(0.46, 'leap')], g='show', act=('lift', 'hoop'), prefer=['fish_trust>.4', 'happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Through the hoop clean, not a drop touched. Show-off.', 'Hoop work. This is why they give me a twig.'])
    o.r('race_the_leaps_along_the_bank', 'Having a race with the salmon along the bank, bounding after every leap it throws', 20, 'none',
        [k(.06, 'run_l', x=.6, y=.2, b=.2), k(.2, 'run_m', x=1.3, y=.3, b=-.8, l=1, w=.3), k(.35, 'rapid', x=1.6, y=.2, b=.4, r=1, w=.6), k(.5, 'run_r', x=1.9, y=.3, b=-1, l=1, w=.8, mark='hup'), k(.66, 'bank_r', x=1.4, y=.3, b=.3, r=1, w=.5), k(.84, 'bank_r', x=.4, y=.5, b=.6, eye='@')],
        [(0.5, 'fun')], g='play', act=('race', 'bank'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Lost by four leaps. It cheats with vertical.', 'Raced a fish. Lost to the one with fins.'])
    o.r('hop_with_every_leap', 'Hopping in step with each leap, wings out, trying to clear the same height from the stone', 20, 'none',
        [k(.1, 'stone_r', x=.3, y=.3, b=.3), k(.24, 'stone_r', x=.4, y=-.2, b=-1.2, w=.8, l=1, r=1), k(.4, 'stone_r', x=.4, y=.8, b=.9), k(.56, 'stone_r', x=.5, y=-.3, b=-1.5, w=1, l=1, r=1, mark='HUP'), k(.74, 'stone_r', x=.3, y=.9, b=1), k(.9, eye='>')],
        [], g='play', act=('hop', 'step'), prefer=['young', 'happy', 'run>.3'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('push_a_leaf_boat_against_the_run', 'Pushing a fallen leaf upstream with a wing and watching the current bring it right back past him', 24, 'wing',
        [k(.12, 'run_r', reach=.5, x=.3, y=.5, b=.3), k(.3, 'run_m', reach=1, x=.5, y=.8, b=.6, mark='shff'), k(.5, 'rapid', reach=1, x=.6, y=.9, b=.7, l=1), k(.7, 'run_m', reach=1, x=.7, y=.7, b=.5, r=1, mark='boop'), k(.88, eye='o')],
        [], g='play', act=('push', 'leaf'), when=['pond_leaves>.2'], prefer=['curious'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('count_the_leaps_from_the_stone', 'Counting each leap out loud with a bill dip, losing the number at the fourth', 20, 'none',
        [k(.1, 'run_m', x=.9, y=.5, b=.8, mark='1'), k(.26, 'run_m', x=.8, y=1, b=.6, mark='2'), k(.42, 'rapid', x=.9, y=1, b=.6, l=1, mark='3'), k(.6, 'rapid', x=.9, y=1.1, b=.7, r=1, mark='5?'), k(.8, eye='-', mark='lost')],
        [], g='test', act=('count', 'leaps'), prefer=['curious'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('set_his_hop_against_the_leap', "Setting his own best hop beside the salmon's leap and comparing the two against the cattail", 22, 'wing',
        [k(.12, 'tuft', reach=.5, x=.3, y=.4, b=.3), k(.3, 'reed_low', reach=1, x=.4, y=.6, b=.5), k(.5, 'cattail_l', reach=1, x=.5, y=-.3, b=-.8, w=.6, mark='me'), k(.7, 'cattail_l', reach=1, x=.5, y=-.6, b=-.2, mark='it'), k(.9, eye='-', mark='ok')],
        [], g='test', act=('compare', 'height'), prefer=['curious', 'young'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('wait_for_the_first_leap', 'Waiting stock-still at the rim for the first leap of the morning to break the water', 22, 'none',
        [k(.1, 'run_m', x=1, y=1, b=.5, eye='o'), k(.3, 'run_m', x=1.2, y=1.2, b=.7, eye='o'), k(.5, 'run_m', x=1.2, y=1.2, b=.7, l=1), k(.68, 'run_m', x=1.4, y=1.6, b=1.1, eye='O', mark='...'), k(.86, 'run_m', x=.3, y=.4, b=.3, eye='^')],
        [], g='rest', act=('wait', 'leap'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_over_who_jumps_higher', 'Arguing nose to bill over who jumps higher, jabbing a wing at the water between squawks', 20, 'wing',
        [k(.09, 'run_m', reach=.4, x=.7, y=.2, b=.2), k(.25, 'run_m', reach=1, x=1.3, b=-.1, mark='NO'), k(.41, 'run_m', reach=1, x=1.5, y=-.1, b=-.3, l=1, mark='NO!'), k(.57, 'run_m', reach=.7, x=.6, y=.5, b=.6, r=1), k(.73, 'run_m', reach=1, x=1.4, y=-.1, b=-.2, mark='NOPE'), k(.9, eye='-')],
        [], g='show', act=('argue', 'height'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Twelve to nothing, and it still disputes the scoring.', 'Lost to a fish. A fish with no legs.'])
    o.r('pose_on_the_stone_mid_leap', 'Freezing in a mid-leap pose on the left stone, wings flung up, while the salmon is the real thing below him', 18, 'none',
        [k(.12, 'stone_l', x=.3, y=-.2, w=.4, perch=1), k(.3, 'stone_l', x=.5, y=-.5, b=-.5, w=.8, perch=1), k(.6, 'stone_l', x=.6, y=-.7, b=-.8, w=1, perch=1, eye='^', mark='ta-da'), k(.85, 'stone_l', x=.2, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'stone'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('flinch_when_it_leaps_at_his_face', 'Hopping back when the salmon rockets out of the water at his bill and drenches him head to foot', 16, 'none',
        [k(.08, 'run_l', x=1.2, y=1.8, b=.9), k(.22, 'run_l', x=1.5, y=2.1, b=1.2, eye='o', mark='...'), k(.34, x=-1.5, y=-1, b=-1.6, l=1, r=1, w=1, eye='O', mark='AAH'), k(.5, x=-.9, y=.1, b=-.2, w=.6, eye='>'), k(.7, x=.1, y=.4, b=.3, eye='-')],
        [], g='mishap', act=('hop', 'face'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Cold, wet and entirely on purpose.', 'It leapt. I flew. Physics split the difference.'])
    o.r('herd_it_up_the_lane_from_both_banks', 'Chasing the salmon up the lane with a friend on the far stone, wings sweeping it forward from both banks', 24, 'wing',
        [k(.1, 'run_l', reach=.6, x=.3, y=.5, b=.3), k(.28, 'run_m', reach=1, x=.5, y=.6, b=.5, l=1, mark='shoo'), k(.46, 'rapid', reach=1, x=.6, y=.9, b=.8, r=1, mark='shoo'), k(.66, 'run_r', reach=1, x=.7, y=.6, b=.5, l=1), k(.86, eye='^')],
        [(0.46, 'lead')], g='use', act=('chase', 'salmon'), when=['homing<.7'], prefer=['happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.48, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Two ducks, one fish, no argument. It is going upstream anyway.', 'Herded it a metre. It would have gone ten.'],
        duo=[k(.12, 'bank_r', x=.3, y=.4, b=.3), k(.3, 'bank_r', x=.8, y=.7, b=.6, l=1, mark='shoo'), k(.5, 'run_r', x=.9, y=.8, b=.7, r=1, mark='shoo'), k(.7, 'rapid', x=.9, y=.8, b=.7, l=1), k(.86, eye='^')])
    o.r('toss_a_flake_between_us_for_the_leap', 'Throwing a flake back and forth with a friend over the lane so the salmon launches at it each time', 24, 'none',
        [k(.07, 'run_l', x=.6, y=.1, b=.1), k(.2, 'run_l', x=1.3, y=-.9, b=-1.2, w=.7, l=1, mark='fwip'), k(.34, 'run_m', x=1.4, y=.6, b=.8, eye='o'), k(.48, 'run_m', x=1.2, y=-.9, b=-1.2, w=.7, r=1, mark='fwip'), k(.64, 'run_m', x=1.4, y=.7, b=.9, eye='O'), k(.82, eye='^')],
        [(0.34, 'leap')], g='play', act=('throw', 'flake'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.4, {'lure': 1}), (0.7, {'lure': 1})],
        duo=[k(.12, 'run_r', x=.4, y=.3, b=.3), k(.3, 'run_r', x=1, y=.4, b=.5, eye='o'), k(.46, 'run_m', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.62, 'run_r', x=1, y=.4, b=.5), k(.8, eye='^')])
    o.r('judge_the_leaps_with_a_friend', 'Showing scores for each leap with a friend at the other end of the rim, wing up for a number and wing down for a groan', 24, 'wing',
        [k(.1, 'run_l', reach=.5, x=.4, y=.2, b=.3), k(.26, 'run_l', reach=1, x=.5, y=-.3, b=-.2, mark='9'), k(.42, 'run_l', reach=1, x=.5, y=.5, b=.5, mark='6'), k(.6, 'run_l', reach=1, x=.5, y=-.4, b=-.3, mark='10!'), k(.8, eye='^')],
        [], g='show', act=('show', 'scores'), prefer=['happy', 'curious'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Ten from me, nine from the other judge. Fish gets zero for tripping on the landing.', 'Scored it. It was a ten. The fish does not know scoring.'],
        duo=[k(.15, 'run_r', x=.4, y=.2, b=.3), k(.34, 'run_r', x=.5, y=-.3, w=.9, mark='8'), k(.5, 'run_r', x=.5, y=.5, b=.5, mark='4'), k(.68, 'run_r', x=.5, y=-.4, w=.9, mark='10'), k(.84, eye='^')])
    o.r('catch_the_rain_as_it_leaps', 'Catching raindrops on his bill at the stones while the salmon leaps up into the rain', 20, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'run_l', x=1, y=-.9, b=-.4, eye='o', mark='plip'), k(.5, 'run_m', x=1.1, y=-1, b=-.5, l=1, eye='O', mark='plip plip'), k(.7, 'run_l', x=.8, y=-.3, b=.2, w=.4, eye='^'), k(.88, eye='-')],
        [(.5, 'cheer')], g='weather', act=('catch', 'rain'), when=['wet'], prefer=['spray>.3'], pick='hungriest',
        obj=[(.3, {'lure': 1}), (.6, {'lure': 1}), (.8, {'lure': 0})], say=['The fish jumped up. The rain came down. I stood there.', 'Wet from both ends. Still counts as a day out.'])
    return o


def trout():
    o = Obj('trout', 'keeping', on='koi_pond', 
            parts=dict(rise='the surface of the water near the rim', glide='the long calm stretch of water', edge='the far edge of the water', shelf='the shelf of shallow water along the bank', mud='the muddy edge of the water', stone='the front rim stones'),
            fields={'rise': (0, 0, 1), 'rings': (0, 0, 1), 'spook': (0, 0, 1)},
            physics=[('rise', 'rate', 0.003, 'dawn'), ('rise', 'rate', -0.002, '!dawn'), ('rings', 'rate', -0.005, 'always'), ('spook', 'rate', -0.0004, 'always')],
            effects=dict(
                hush=[['spook', 'mul', 0.2], ['subject.mood', 'add', 0.12]],
                scare=[['spook', 'set', 1], ['rings', 'set', 1]],
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                flurry=[['rings', 'set', 1], ['subject.hunger', 'add', -0.2], ['rise', 'mul', 0.5]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                dimple=[['rings', 'set', 1], ['subject.mood', 'add', 0.15]],
                settle=[['spook', 'mul', 0.3], ['subject.trust', 'add', 0.1]],
                tickle=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('rings', 0.3, 'o O o', 'glide', 'water')],
            anchors=dict(
                rise_l=(0.2353, 0.7818),
                glide=(0.4874, 0.7455),
                rise_r=(0.7395, 0.7091),
                edge_far=(0.5882, 0.7818),
                shelf=(0.3361, 0.7091),
                mud_edge=(0.4034, 0.7818),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364, 'surface'),
            ))
    o.r('look_the_spots_over_for_pale_patches', 'Peering at the speckled flanks for any pale patch, turning his head side to side at the rim', 22, 'none',
        [k(.05, x=.3, y=.4, b=.2), k(.17, 'rise_l', x=1.4, y=1.9, b=1.1, eye='o'), k(.3, 'rise_l', x=1.2, y=2.1, b=1.3, r=1, eye='O'), k(.46, 'rise_l', x=1.6, y=2.1, b=1.2, l=1, mark='hm'), k(.62, 'glide', x=1.3, y=1.8, b=1), k(.78, x=.5, y=.5, b=.3, w=.4, eye='^'), k(.9, eye='-')],
        [(0.46, 'tend')], g='care', act=('peer', 'spots'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Spots all accounted for. I counted twice, at the rim of shame.', 'No pale patches. Healthier than my last three weeks.'])
    o.r('wipe_the_lip_clean_of_grit', "Giving a wipe to the grit from the trout's upturned lip with a feather-edge of wing while it hangs at the surface", 20, 'wing',
        [k(.07, 'glide', reach=.4, x=.3, y=.7, b=.3), k(.22, 'glide', reach=.9, x=.5, y=1.3, b=.9, mark='wp'), k(.4, 'glide', reach=1, x=.6, y=1.5, b=1.2, r=1, mark='wp'), k(.55, 'glide', reach=1, x=.5, y=1.3, b=1, l=1), k(.72, 'glide', reach=.5, x=.2, y=.7, b=.4), k(.9, eye='^')],
        [(0.4, 'tend')], g='care', act=('wipe', 'lip'), prefer=['fish_health<.9', 'happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.55, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('let_a_crumb_slide_off_the_bill', 'Letting a single crumb slide off the very tip of his bill into the open mouth of the trout at the rim', 20, 'none',
        [k(.06, x=.3, y=.5, b=.3), k(.2, 'rise_r', x=1.5, y=1.9, b=.8, eye='o'), k(.36, 'rise_r', x=1.8, y=2.3, b=1, eye='O', mark='...'), k(.5, 'rise_r', x=1.7, y=2.1, b=.9, l=1, mark='plip'), k(.66, 'rise_r', x=.9, y=1, b=.5, w=.4), k(.84, eye='^')],
        [(0.5, 'feed')], g='use', act=('tip', 'crumb'), when=['fish_hunger>.4'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.5, {'lure': 1}), (0.7, {'lure': 0})],
        say=['Took it and a bit of my nerve.', 'Crumb accepted. Dignity declined.'])
    o.r('dimple_the_surface_with_a_twig', 'Tapping the surface with a twig tip in a slow rhythm until the trout comes up to see what is rising', 24, 'twig',
        [k(.07, 'glide', reach=.5, x=.3, y=.2), k(.2, 'glide', reach=1, x=.6, y=.6, b=.3, mark='dp'), k(.32, 'glide', reach=.7, x=.4, y=.3, b=.1), k(.46, 'glide', reach=1, x=.7, y=.7, b=.4, mark='dp'), k(.6, 'glide', reach=.7, x=.4, y=.3, b=.1), k(.74, 'glide', reach=1, x=.8, y=.8, b=.5, l=1, mark='DP'), k(.9, eye='o')],
        [(0.74, 'dimple')], g='use', act=('tap', 'surface'), prefer=['curious', 'happy'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.6, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('pat_the_chin_when_it_hangs_still', "Patting the trout's chin with the back of a wing when it hangs still at the rim, one slow tickle at a time", 22, 'wing',
        [k(.08, 'rise_l', reach=.4, x=.2, y=1, b=.5), k(.24, 'rise_l', reach=.8, x=.4, y=1.7, b=1.2, mark='tck'), k(.4, 'rise_l', reach=1, x=.3, y=1.8, b=1.4, l=1, mark='tck'), k(.56, 'rise_l', reach=1, x=.4, y=1.7, b=1.3, r=1, mark='tck'), k(.74, 'rise_l', reach=.5, x=.2, y=.9, b=.6), k(.9, eye='^')],
        [(0.4, 'tickle')], g='use', act=('pat', 'chin'), when=['spook<.5'], prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.22, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('balance_a_twig_on_the_water_to_lead', "Balancing a twig flat at the water's skin and walking it slowly along the rim so the trout trails the tip", 26, 'twig',
        [k(.05, 'rise_l', reach=.4, x=.3, y=.3, b=.2), k(.18, 'rise_l', reach=1, x=.6, y=.6, b=.5), k(.34, 'glide', reach=1, x=.8, y=.6, b=.3, l=1), k(.5, 'edge_far', reach=1, x=1, y=.6, b=.5, r=1), k(.68, 'rise_r', reach=1, x=1.2, y=.6, b=.3, l=1), k(.86, eye='^')],
        [(0.5, 'dimple')], g='play', act=('balance', 'twig'), when=['rise>.3'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.5, {'lure': 1}), (0.72, {'lure': 1})],
        say=['Followed the twig the whole way. Faithful to anything that floats.', 'A twig, a trout, a tiny parade.'])
    o.r('sprint_the_shelf_with_the_flurry', 'Having a race along the shelf in short rushes as the trout flurries from ring to ring ahead of him', 20, 'none',
        [k(.05, 'rise_l', x=.7, y=.3, b=.3), k(.15, 'glide', x=1.4, y=.4, b=-.9, l=1, w=.4), k(.25, 'glide', x=.8, y=.5, b=.5, r=1), k(.36, 'edge_far', x=1.5, y=.3, b=-1, l=1, w=.7, mark='hup'), k(.48, 'edge_far', x=.8, y=.5, b=.6, r=1), k(.6, 'rise_r', x=1.6, y=.3, b=-1.1, l=1, w=.9, mark='HUP'), k(.78, 'rise_r', x=.5, y=.4, b=.4, eye='@')],
        [(0.6, 'fun')], g='play', act=('race', 'shelf'), when=['rise>.3'], prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.3, {'lure': 1}), (0.46, {'lure': 1}), (0.64, {'lure': 1})],
        say=['Lost by six rings. It rises faster than I can sprint.', 'Raced a trout. Beat it on the way back. It was not racing.'])
    o.r('seek_the_shy_one_along_the_far_edge', 'Seeking along the far edge for the trout that has gone quiet, bill sweeping slowly side to side', 22, 'none',
        [k(.06, 'rise_l', x=.7, y=.9, b=.6), k(.2, 'mud_edge', x=1.2, y=1.3, b=.9, eye='o'), k(.34, 'edge_far', x=1.4, y=1.5, b=1.1, eye='o', mark='?'), k(.5, 'rise_r', x=1.5, y=1.5, b=1.2, l=1, mark='?'), k(.66, 'rise_r', x=1.3, y=1.4, b=1.1, eye='O', mark='there!'), k(.84, x=.3, y=.4, eye='^')],
        [], g='play', act=('seek', 'trout'), when=['spook>.3'], prefer=['young', 'curious'], pick='shyest',
        obj=[(0.66, {'lure': 1}), (0.84, {'lure': 1})])
    o.r('hop_in_time_with_the_flurry', 'Hopping in time with the flurry of rises, three hops to a burst, wings out like a conductor', 18, 'none',
        [k(.06, 'stone_m', x=.3, y=.3, b=.2), k(.16, 'stone_m', x=.4, y=-.2, b=-1.3, w=.6, l=1, r=1), k(.26, 'stone_m', x=.3, y=.4, b=.6), k(.38, 'stone_m', x=.4, y=-.3, b=-1.4, w=.8, l=1, r=1), k(.5, 'stone_m', x=.3, y=.4, b=.6), k(.62, 'stone_m', x=.5, y=-.4, b=-1.6, w=1, l=1, r=1, mark='HUP'), k(.78, 'stone_m', x=.3, y=.5, b=.8, eye='>')],
        [(0.38, 'fun')], g='play', act=('hop', 'stone'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.38, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('count_the_freckles_on_a_flank', 'Counting the freckles down one flank with a bill-bob for each, then starting over after losing count', 22, 'none',
        [k(.05, 'rise_r', x=1, y=1.4, b=.6, mark='1'), k(.16, 'rise_r', x=1.1, y=1.5, b=.7, mark='5'), k(.28, 'glide', x=1.2, y=1.5, b=.8, l=1, mark='11'), k(.4, 'glide', x=1.3, y=1.6, b=.9, r=1, mark='20?'), k(.52, x=-.4, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.66, 'rise_r', x=1, y=1.4, b=.6, mark='1'), k(.84, eye='-')],
        [], g='test', act=('count', 'freckles'), prefer=['curious'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.5, {'lure': 1})])
    o.r('compare_the_length_to_the_wild_ones', "Holding a wing out along the trout's length and then past it, comparing it with the longest wild ones he has heard of", 24, 'wing',
        [k(.06, 'rise_l', reach=.4, x=.2, y=.7, b=.3), k(.2, 'rise_l', reach=.9, x=.3, y=.9, b=.6), k(.36, 'glide', reach=1, x=.5, y=.8, b=.4, r=1, mark='so'), k(.52, 'rise_r', reach=1, x=.9, y=.8, b=.4, l=1, mark='far?'), k(.7, 'glide', reach=.7, x=.3, y=.4, b=.2), k(.88, eye='-', mark='bigger')],
        [], g='test', act=('compare', 'lengths'), prefer=['curious', 'grown'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.5, {'lure': 1})])
    o.r('weigh_the_trout_by_eye', 'Squinting along a reed held flat over the trout to weigh it by eye, his head rocking like a scale', 22, 'reed',
        [k(.06, 'rise_l', reach=.4, x=.2, y=.3), k(.2, 'glide', reach=.9, x=.5, y=.9, b=.5, eye='-'), k(.35, 'glide', reach=1, x=.6, y=1, b=.6, l=1, mark='rock'), k(.5, 'glide', reach=1, x=.5, y=.6, b=.3, r=1, mark='rock'), k(.66, 'glide', reach=.8, x=.4, y=.8, b=.5, eye='o', mark='two'), k(.86, eye='^')],
        [], g='test', act=('weigh', 'trout'), prefer=['curious'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('hold_dead_still_for_the_first_rise', 'Waiting dead still at the rim, not a feather out of place, until the trout trusts the shadow and rises', 28, 'none',
        [k(.06, 'glide', x=.8, y=1.2, b=.7, eye='o'), k(.25, 'glide', x=.9, y=1.4, b=.9, eye='o'), k(.5, 'glide', x=.9, y=1.4, b=.9, l=1), k(.7, 'glide', x=1, y=1.6, b=1, eye='O', mark='...'), k(.9, 'glide', x=.5, y=.7, b=.4, eye='^')],
        [(0.7, 'settle')], g='rest', act=('wait', 'rise'), when=['spook>.3'], pick='shyest',
        obj=[(0.55, {'lure': 1}), (0.85, {'lure': 1})],
        say=['Still enough that a dragonfly would have applied for the job.', 'Trust takes a motionless duck. I have a talent.'])
    o.r('bow_to_the_spotted_riser', 'Bowing to the spotted riser as it breaks the surface right at his bill, a deep and dripping dip', 16, 'none',
        [k(.08, 'glide', x=.7, y=1.1, b=.8), k(.28, 'glide', x=1.2, y=2.4, b=2, eye='-'), k(.5, 'glide', x=1.3, y=2.6, b=2.2, eye='-', mark='sir'), k(.7, 'glide', x=.7, y=.6, b=.5), k(.86, x=.1, y=-.4, w=.6, eye='^')],
        [], g='show', act=('bow', 'riser'), prefer=['happy'], pick='hungriest',
        obj=[(0.28, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Bowed to a riser. It rose to my forehead.', 'Respect shown. Ripples returned.'])
    o.r('present_a_flurry_of_rings', 'Presenting a flurry of rings to an invisible crowd with one long sweep of the wing, a small and damp circus', 20, 'wing',
        [k(.07, 'rise_l', reach=.4, x=.1, y=.1), k(.24, 'rise_l', reach=.9, x=.2, y=-.6, b=-.5), k(.42, 'glide', reach=1, x=.2, y=-.8, b=-.7, mark='tadaa'), k(.6, 'stone_r', reach=1, x=.3, y=-.6, b=-.4, r=1), k(.78, 'stone_r', reach=.6, x=.5, y=-.1), k(.92, eye='^')],
        [], g='show', act=('present', 'rings'), prefer=['happy', 'rings>.3'], pick='shyest',
        obj=[(0.45, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_the_freckle_count', 'Arguing over the freckle count with the trout, jabbing a wing at the spot he swears he already counted', 20, 'wing',
        [k(.06, 'glide', reach=.4, x=.6, y=.3, b=.3), k(.2, 'glide', reach=1, x=1.1, y=.1, b=.1, mark='TWENTY'), k(.36, 'glide', reach=1, x=1.3, y=0, b=-.1, l=1, mark='TWENTY'), k(.52, 'glide', reach=.6, x=.5, y=.6, b=.7, r=1), k(.7, 'glide', reach=1, x=1.2, y=0, b=0, mark='TWENTY-ONE'), k(.88, eye='-')],
        [], g='show', act=('argue', 'freckles'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It insists on twenty-one. It has the spots, I have the arithmetic.', 'Lost the count and the argument. Two for two.'])
    o.r('pose_on_the_stone_with_a_rising_trout', 'Freezing in the pose of a leaping fish on the right stone, wings slashed back, while the real one rises below him', 18, 'none',
        [k(.07, 'stone_r', x=.4, y=-.1, w=.3, perch=1), k(.22, 'stone_r', x=.9, y=-.7, b=-.7, w=.7, perch=1), k(.46, 'stone_r', x=1.1, y=-.9, b=-1, w=1, perch=1, eye='^', mark='so fast'), k(.72, 'stone_r', x=.4, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'stone'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('flinch_from_the_rise_at_his_bill', 'Hopping back as the trout takes a crumb off the very tip of his bill with a smack and a splash', 16, 'none',
        [k(.06, 'rise_r', x=1.1, y=1.7, b=.8), k(.18, 'rise_r', x=1.3, y=1.9, b=1, eye='o'), k(.28, x=-1.4, y=-.7, b=-1.3, l=1, r=1, w=.9, eye='O', mark='SMACK'), k(.42, x=-.8, y=.2, b=-.1, w=.6, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [(0.18, 'flurry'), (0.18, 'scare')], g='mishap', act=('hop', 'splash'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.45, {'lure': 1})],
        say=['Smacked the bill like a cymbal. Rude, quick, correct.', 'I was a crumb for half a second. Humbling.'])
    o.r('hold_still_together_for_the_rise', 'Perching statue-still beside a friend on the far stone, the two shadows quiet until the trout trusts them and rises', 28, 'none',
        [k(.06, 'rise_l', x=.9, y=1.1, b=.6), k(.24, 'rise_l', x=1, y=1.3, b=.8, eye='o'), k(.5, 'rise_l', x=1, y=1.3, b=.8, l=1), k(.7, 'rise_l', x=1.1, y=1.9, b=1.4, eye='O', mark='...'), k(.88, 'rise_l', x=.5, y=.6, b=.4, eye='^')],
        [(0.7, 'hush')], g='rest', act=('perch', 'shadow'), when=['spook>.3'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Two ducks holding their breath. The fish is the only one breathing.', 'Silent as a pair of garden gnomes. It came up for us.'],
        duo=[k(.1, 'stone_r', x=.4, y=.5, b=.4), k(.3, 'stone_r', x=.5, y=.8, b=.7, eye='-'), k(.55, 'stone_r', x=.5, y=.8, b=.7), k(.76, 'stone_r', x=.5, y=.9, b=.8, eye='o', mark='...'), k(.9, eye='^')])
    o.r('feed_it_from_both_banks_in_turn', 'Tipping a crumb in turn with a friend from the opposite bank so the trout dashes from one ring to the other', 24, 'none',
        [k(.06, 'rise_l', x=.5, y=.3, b=.2), k(.2, 'rise_l', x=1.2, y=-.4, b=-.9, w=.6, mark='plip'), k(.34, 'glide', x=1, y=.3, b=.4, eye='o'), k(.5, 'rise_l', x=1.3, y=-.5, b=-.9, w=.6, l=1, mark='plip'), k(.66, 'rise_l', x=.9, y=.6, b=.5, eye='O'), k(.84, eye='^')],
        [(0.5, 'flurry')], g='use', act=('tip', 'crumbs'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.62, {'lure': 1})],
        duo=[k(.1, 'rise_r', x=.5, y=.3, b=.2), k(.28, 'rise_r', x=1.1, y=.4, b=.5, eye='o'), k(.42, 'rise_r', x=1.2, y=-.4, b=-.9, w=.6, l=1, mark='plip'), k(.6, 'rise_r', x=1, y=.3, b=.4), k(.8, eye='^')])
    o.r('read_the_rings_aloud_to_a_friend', 'Showing a friend the rings by reading them aloud at the other end of the shelf, the two trading guesses on which rise came first', 24, 'wing',
        [k(.06, 'shelf', reach=.4, x=.3, y=.4, b=.3), k(.2, 'glide', reach=.9, x=.5, y=.5, b=.5, mark='that one'), k(.36, 'glide', reach=1, x=.6, y=.6, b=.6, l=1), k(.52, 'edge_far', reach=1, x=.7, y=.6, b=.5, r=1, mark='no, THAT one'), k(.72, 'shelf', reach=.6, x=.3, y=.3, b=.2), k(.88, eye='-')],
        [], g='test', act=('show', 'rings'), prefer=['curious', 'happy'], pick='hungriest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['We agreed on nothing. Excellent teamwork.', 'Two readers, one ripple. The fish wrote the book.'],
        duo=[k(.1, 'mud_edge', x=.5, y=.4, b=.3), k(.26, 'mud_edge', x=.9, y=.7, b=.6, eye='o', mark='no'), k(.46, 'rise_r', x=1, y=.8, b=.7, l=1, mark='that one'), k(.66, 'mud_edge', x=.7, y=.6, b=.5, r=1), k(.84, eye='^')])
    o.r('cool_the_trouts_pool_with_a_wing_breeze', 'Cooling the trout\'s shady edge with a slow wing-fanned breeze on a warm noon', 22, 'wing',
        [k(.12, 'rise_l', reach=.5, x=.3, y=.6, b=.4), k(.3, 'rise_l', reach=1, x=.4, y=.8, b=.6, w=.7), k(.5, 'glide', reach=1, x=.5, y=.8, b=.7, l=1, w=1, mark='fff'), k(.7, 'rise_l', reach=1, x=.4, y=.8, b=.6, r=1, w=.7), k(.88, eye='^')],
        [(.5, 'cheer')], g='weather', act=('cool', 'pool'), when=['warm'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.6, {'lure': 1}), (.8, {'lure': 0})], say=['One trout, one breeze, no complaints.', 'A fan made of me. Lowest rank, best job.'])
    return o


def sturgeon():
    o = Obj('sturgeon', 'keeping', on='infinity_pool', 
            parts=dict(base='the foot of the tank wall', low='the lower glass of the tank', high='the upper glass of the tank', skin='the water line under the coping', ledge='the stone ledge in front of the tank'),
            fields={'silt': (0, 0, 1), 'lap': (0, 0, 1)},
            physics=[('silt', 'rate', 0.0005, 'night'), ('silt', 'rate', -0.0008, '!night'), ('lap', 'rate', -0.0003, 'always')],
            effects=dict(
                ease=[['subject.trust', 'add', 0.12]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                lead=[['lap', 'add', 0.25], ['subject.trust', 'add', 0.1]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                rise=[['subject.hunger', 'add', -0.2], ['lap', 'add', 0.2]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('silt', 0.3, '~=~=~', 'base_m', 'mud')],
            anchors=dict(
                base_l=(0.1951, 0.7797),
                base_m=(0.5041, 0.7797),
                base_r=(0.7642, 0.7797),
                low_l=(0.2927, 0.7288),
                low_r=(0.6504, 0.7288),
                high_l=(0.2276, 0.678),
                high_m=(0.5041, 0.678),
                skin_l=(0.2764, 0.5763),
                ledge_l=(0.2439, 0.8305, 'surface'),
                ledge_m=(0.5041, 0.8305, 'surface'),
                ledge_r=(0.748, 0.8305, 'surface'),
            ))
    o.r('peer_at_the_armour_plates', "Peering at the bony plates along the sturgeon's back as it glides past the wall, looking for any chip or crack", 22, 'none',
        [k(.06, x=.5, y=.6, b=.4), k(.18, 'low_l', x=1.5, y=1.9, b=1, eye='o'), k(.32, 'low_l', x=1.7, y=2.1, b=1.2, eye='O', mark='hm'), k(.5, 'base_m', x=1.4, y=2, b=1.1, l=1), k(.66, 'base_r', x=1.5, y=2.2, b=1.3, r=1, mark='ok'), k(.84, x=.6, y=.6, b=.3, w=.4, eye='^')],
        [(0.5, 'tend')], g='care', act=('peer', 'plates'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.18, {'lure': 1}), (0.5, {'lure': 1}), (0.66, {'lure': 1})],
        say=['Every plate present. Armour older than my family tree.', 'No chips. It has been through worse than a tank.'])
    o.r('press_a_pellet_to_the_wall_for_the_snout', 'Pressing one pellet flat to the wall with his bill while the long snout hoovers at it from the other side', 22, 'none',
        [k(.06, x=.4, y=.7, b=.4), k(.2, 'low_l', x=1.7, y=1.9, b=.9, eye='o', mark='...'), k(.36, 'low_l', x=1.9, y=2.1, b=1.1, eye='O', mark='SHLRP'), k(.52, 'low_l', x=1.8, y=2, b=1, l=1), k(.7, x=.6, y=.8, b=.5, w=.4, eye='^'), k(.88, eye='-')],
        [(0.36, 'feed')], g='use', act=('press', 'pellet'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.52, {'lure': 1}), (0.7, {'lure': 0})],
        say=['Hoovered it from the other side. It could have sucked my bill off.', 'Sturgeons eat like a drain. A very old drain.'])
    o.r('draw_the_old_one_along_the_wall', 'Dragging a wingtip slowly along the foot of the wall so the sturgeon follows it from end to end at its own pace', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.9, b=.5), k(.18, 'base_l', reach=1, x=.5, y=1.1, b=.6), k(.34, 'base_m', reach=1, x=.7, y=1.2, b=.7, l=1), k(.52, 'base_m', reach=1, x=.9, y=1.2, b=.7), k(.7, 'base_r', reach=1, x=1.1, y=1.3, b=.8, r=1), k(.88, eye='^')],
        [(0.52, 'lead')], g='use', act=('drag', 'wingtip'), when=['lap<.7'], pick='hungriest',
        obj=[(0.12, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.72, {'lure': 1})],
        say=['It took the whole song to cross the tank. Ancient and unhurried.', 'Led it a lap. It leads me on all the rest.'])
    o.r('pat_the_wall_where_the_snout_rests', 'Patting the wall with the back of a wing where the sturgeon rests its snout, slow as a bedtime stroke', 22, 'wing',
        [k(.08, 'low_r', reach=.4, x=.2, y=.9, b=.5), k(.22, 'low_r', reach=.9, x=.5, y=1.5, b=1, mark='pat'), k(.4, 'low_r', reach=1, x=.4, y=1.7, b=1.2, l=1, mark='pat'), k(.58, 'low_r', reach=1, x=.5, y=1.6, b=1.1, r=1, mark='pat'), k(.76, 'low_r', reach=.5, x=.3, y=.9, b=.6), k(.9, eye='^')],
        [(0.4, 'stroke')], g='care', act=('pat', 'wall'), prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('hold_a_flake_up_at_the_water_line', 'Lifting one flake pinched in his bill up at the water line until the old sturgeon rises all the way to the top for it', 24, 'none',
        [k(.06, x=.3, y=-.3, w=.2), k(.2, 'skin_l', x=.8, y=-.5, b=-.2, eye='o'), k(.36, 'skin_l', x=1, y=-.8, b=-.4, eye='O', mark='...'), k(.5, 'skin_l', x=1.1, y=-.9, b=-.6, w=.3, l=1, mark='SHLUP'), k(.68, x=-.4, y=.1, b=.2, w=.7, eye='>'), k(.86, eye='^')],
        [(0.5, 'rise')], g='use', act=('lift', 'flake'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Came all the way up for a flake. Took thirty years of effort.', 'Rare sight. Up, snap, gone. Back to the floor.'])
    o.r('race_it_down_the_wall_and_win', 'Having a race with the sturgeon down the length of the wall at a brisk walk and winning by a full lap', 20, 'none',
        [k(.05, 'base_l', x=.6, y=.3, b=.2), k(.2, 'low_l', x=1.2, y=.4, b=-.6, l=1, w=.4), k(.36, 'high_m', x=1.4, y=.3, b=.3, r=1, w=.6), k(.52, 'low_r', x=1.7, y=.4, b=-.8, l=1, w=.8, mark='hup'), k(.68, 'base_r', x=1.6, y=.4, b=.4, r=1, w=.7, eye='@', mark='WON'), k(.84, 'base_r', x=.4, y=.6, b=.5, eye='^')],
        [(0.52, 'fun')], g='play', act=('race', 'wall'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.56, {'lure': 1}), (0.74, {'lure': 1})],
        say=['Won by a lap. It was not aware of the race.', 'Victory by walking. It never even clocked me.'])
    o.r('hop_the_ledge_beside_its_slow_pass', 'Hopping from foot to foot along the front ledge, keeping pace with its slow pass along the wall', 22, 'none',
        [k(.06, 'ledge_l', x=.3, y=.4, b=.4, l=1, perch=1), k(.2, 'ledge_l', x=.5, y=-.2, b=-.9, w=.6, r=1, perch=1), k(.34, 'ledge_m', x=.6, y=.6, b=.8, l=1, perch=1), k(.5, 'ledge_m', x=.5, y=-.3, b=-1, w=.8, r=1, perch=1), k(.66, 'ledge_r', x=.6, y=.6, b=.8, l=1, perch=1), k(.84, 'ledge_r', x=.4, y=.2, b=.3, perch=1, eye='^')],
        [], g='play', act=('hop', 'ledge'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('draw_a_fish_in_the_breath_fog', 'Blowing a fog patch on the wall and tracing a little fish in it with a wingtip, which the sturgeon noses along', 24, 'wing',
        [k(.06, 'high_m', reach=.4, x=.4, y=.5, b=.3), k(.2, 'high_m', reach=.6, x=.9, y=.9, b=.6, mark='haaa'), k(.34, 'high_m', reach=1, x=.5, y=.5, b=.4, mark='~~'), k(.5, 'low_r', reach=1, x=.6, y=.8, b=.6, l=1, mark='><>'), k(.68, 'low_r', reach=1, x=.5, y=.9, b=.7, r=1), k(.86, eye='^')],
        [], g='play', act=('blow', 'fog'), prefer=['happy', 'curious'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Drew a fish. The fish looked at the fish. Neither impressed.', 'My art career begins in breath.'])
    o.r('measure_it_in_wing_spans', 'Measuring the sturgeon along the wall with his wing, spanning it out and counting spans aloud until it runs out of wall', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.6, b=.3, mark='1'), k(.16, 'low_l', reach=1, x=.6, y=.9, b=.6, mark='2'), k(.3, 'high_l', reach=1, x=.6, y=.8, b=.5, mark='3'), k(.44, 'high_m', reach=1, x=.7, y=.9, b=.6, l=1, mark='4'), k(.58, 'low_r', reach=1, x=.8, y=1, b=.7, mark='5'), k(.72, 'base_r', reach=1, x=.9, y=1.1, b=.8, r=1, mark='6!'), k(.9, eye='O', mark='long')],
        [], g='test', act=('measure', 'length'), prefer=['curious'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.45, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Six wing spans and a bit. It keeps growing between counts.', 'Seven spans, if you count the tail it denies.'])
    o.r('count_the_plates_down_the_back', 'Counting the armour plates down the long back with a bill dip for each, losing count at the tail', 24, 'none',
        [k(.06, 'low_l', x=.9, y=1.5, b=.7, mark='1'), k(.18, 'low_l', x=1, y=1.6, b=.8, mark='4'), k(.3, 'high_l', x=1.1, y=1.6, b=.8, l=1, mark='9'), k(.44, 'high_m', x=1.2, y=1.7, b=.9, mark='14'), k(.58, 'low_r', x=1.3, y=1.8, b=1, r=1, mark='19?'), k(.72, x=-.4, y=.2, b=-.1, w=.4, eye='>', mark='again'), k(.88, eye='-')],
        [], g='test', act=('count', 'plates'), prefer=['curious'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.5, {'lure': 1}), (0.66, {'lure': 1})])
    o.r('wait_for_the_whiskers_at_the_base', 'Waiting stock-still by the base of the wall for the long whiskers to come feeling along it', 24, 'none',
        [k(.08, 'base_m', x=.9, y=1.5, b=.9, eye='o'), k(.3, 'base_m', x=1, y=1.7, b=1.1, eye='o'), k(.52, 'base_m', x=1, y=1.7, b=1.1, l=1), k(.7, 'base_m', x=1.2, y=1.9, b=1.3, eye='O', mark='...'), k(.88, 'base_m', x=.4, y=.7, b=.4, eye='^')],
        [], g='rest', act=('wait', 'whiskers'), prefer=['lonely', 'curious', 'silt>.3'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('bow_to_the_ancient_one', 'Bowing deeply to the ancient fish as it glides by the wall, a long and formal bill-dip', 18, 'none',
        [k(.08, 'low_l', x=.6, y=1.1, b=.9), k(.26, 'low_l', x=1.3, y=2.6, b=2.1, eye='-'), k(.5, 'low_l', x=1.4, y=2.8, b=2.3, eye='-', mark='your honour'), k(.7, 'low_l', x=.7, y=.7, b=.6), k(.86, x=.1, y=-.5, w=.7, eye='^')],
        [], g='show', act=('bow', 'sturgeon'), prefer=['happy'], pick='hungriest',
        obj=[(0.26, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Bowed. It turned its head three degrees. A great honour.', 'Respects paid. In this tank, the old fish is the landlord.'])
    o.r('present_the_old_one_to_the_dark', 'Presenting the old fish to the dark with a grand wing sweep along the wall, a ringmaster introducing a monument', 22, 'wing',
        [k(.07, 'base_l', reach=.4, x=.1, y=.2), k(.24, 'low_l', reach=.9, x=.3, y=-.3, b=-.3), k(.42, 'high_m', reach=1, x=.3, y=-.5, b=-.4, mark='ladies and'), k(.6, 'low_r', reach=1, x=.4, y=-.3, b=-.2, l=1, mark='gentle-fish'), k(.78, 'base_r', reach=.6, x=.4, y=0), k(.92, eye='^')],
        [], g='show', act=('present', 'sturgeon'), prefer=['happy'], pick='shyest',
        obj=[(0.45, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_for_the_blunt_nose', 'Arguing with the sturgeon over whose nose is the nobler one, bill to snout against the wall', 20, 'wing',
        [k(.08, 'low_r', reach=.5, x=.7, y=.9, b=.6), k(.24, 'low_r', reach=1, x=1.2, y=.8, b=.5, mark='MINE'), k(.4, 'low_r', reach=1, x=1.3, y=.7, b=.4, l=1, mark='MINE'), k(.56, 'low_r', reach=.6, x=.6, y=1, b=.8, r=1), k(.74, 'low_r', reach=1, x=1.2, y=.8, b=.5, mark='NO, MINE'), k(.9, eye='-')],
        [], g='show', act=('argue', 'nose'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['A prehistoric nose against a duck bill. The nose is older.', 'Lost on seniority.'])
    o.r('pose_on_the_ledge_like_a_prow', "Striking a pose on the left ledge like a ship's prow, bill high, while the old fish slides along the wall like a submarine", 18, 'none',
        [k(.06, 'ledge_l', x=.3, y=-.3, w=.3, perch=1), k(.24, 'ledge_l', x=.8, y=-.7, b=-.4, w=.6, perch=1), k(.5, 'ledge_l', x=1, y=-1, b=-.7, w=1, perch=1, eye='^', mark='full ahead'), k(.74, 'ledge_l', x=.3, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'ledge'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('jump_back_from_the_rising_snout', 'Hopping back with a squawk when the great snout surges up the wall right at his bill and the whole armoured body surges', 18, 'none',
        [k(.06, 'base_r', x=1, y=1.8, b=.9), k(.18, 'base_r', x=1.3, y=2.1, b=1.2, eye='o', mark='...'), k(.28, x=-1.4, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='GAH'), k(.44, x=-.8, y=.3, b=-.1, w=.7, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'snout'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.45, {'lure': 1})],
        say=['Thirty years asleep, then it surges. Fair play.', 'My feathers have not recovered.'])
    o.r('walk_the_old_one_down_the_wall_between_us', 'Dragging the old fish from one end of the wall while a friend draws from the other, the sturgeon sliding between the two wingtips', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.8, b=.4), k(.2, 'low_l', reach=1, x=.5, y=1, b=.6), k(.38, 'high_m', reach=1, x=.7, y=.9, b=.6, l=1), k(.56, 'low_r', reach=1, x=.8, y=1, b=.7, r=1), k(.76, 'base_r', reach=1, x=.9, y=1.1, b=.8), k(.9, eye='^')],
        [(0.38, 'lead')], g='use', act=('drag', 'sturgeon'), when=['lap<.7'], prefer=['happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.62, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Two ducks, one fish, no agreement. It chose the middle.', 'Pulled from both ends. The old fish took neither.'],
        duo=[k(.1, 'base_r', x=.4, y=.8, b=.4), k(.28, 'low_r', x=.6, y=1, b=.6, l=1), k(.46, 'high_m', x=.8, y=1, b=.6, r=1), k(.66, 'low_l', x=.9, y=1.1, b=.7), k(.84, 'base_l', x=.5, y=.7, b=.4, eye='^')])
    o.r('swap_pellets_through_the_dark_with_a_friend', 'Pressing pellets to the wall in turn with a friend at the far end, the old fish crossing the dark to each in order', 26, 'none',
        [k(.05, 'low_l', x=.7, y=1, b=.6), k(.2, 'low_l', x=1.6, y=1.9, b=.9, eye='o', mark='tp'), k(.36, 'low_l', x=1.4, y=1.2, b=.6, w=.4), k(.52, 'high_m', x=1.7, y=1.7, b=.9, mark='tp'), k(.7, 'high_m', x=.8, y=.7, b=.4, eye='O'), k(.86, eye='^')],
        [(0.52, 'feed')], g='play', act=('press', 'pellets'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.56, {'lure': 1})],
        duo=[k(.12, 'low_r', x=.6, y=.9, b=.5), k(.3, 'low_r', x=1.5, y=1.8, b=.8, mark='tp'), k(.46, 'low_r', x=1.3, y=1.1, b=.5), k(.62, 'low_r', x=1.6, y=1.7, b=.9, l=1, mark='tp'), k(.8, eye='^')])
    o.r('trade_guesses_on_its_age_with_a_friend', "Weighing up guesses on the old fish's age with a friend at the other end of the wall, each guess louder and older than the last", 24, 'none',
        [k(.06, 'base_l', x=.7, y=.9, b=.4, mark='fifty'), k(.2, 'low_l', x=.9, y=1, b=.6, mark='eighty'), k(.36, 'high_l', x=1.1, y=1, b=.7, l=1, mark='a century'), k(.52, 'high_l', x=1.2, y=.6, b=.5, w=.5, mark='two!'), k(.7, 'low_l', x=.7, y=.7, b=.4, eye='-', mark='fine'), k(.86, eye='^')],
        [], g='test', act=('weigh', 'years'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Two hundred, by consensus. The fish stayed silent. A good sign.', "Settled on 'old'. The fish confirmed with a long blink."],
        duo=[k(.1, 'base_r', x=.7, y=.9, b=.4, mark='sixty'), k(.28, 'low_r', x=.9, y=1, b=.6, mark='a hundred'), k(.44, 'high_m', x=1.1, y=1, b=.7, r=1, mark='two!'), k(.62, 'low_r', x=.8, y=.9, b=.5, eye='-'), k(.8, eye='^')])
    o.r('wrap_a_wing_round_himself_in_the_cold', 'Wrapping a wing round himself against the cold off the glass while the old sturgeon cruises past', 24, 'none',
        [k(.12, x=.2, y=.4, b=.5, w=.5), k(.3, 'base_l', x=.4, y=.8, b=.9, w=.8, eye='-'), k(.55, 'base_l', x=.3, y=.9, b=1.2, w=1, l=1, eye='-', mark='brr'), k(.78, 'base_l', x=.2, y=.6, b=.7, w=.6, eye='^'), k(.9, eye='-')],
        [(.55, 'ease')], g='weather', act=('wrap', 'wing'), when=['cold'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.65, {'lure': 1})], say=['The sturgeon has been cold since the Triassic. I give up after a minute.', 'Wing around me, fish around the tank. We are both coping.'])
    return o


def pufferfish():
    o = Obj('pufferfish', 'keeping', on='infinity_pool', 
            parts=dict(puff='the tank glass at beak height', bob='the tank glass at eye height', top='the top run of water in the tank', skin='the water line under the coping', ledge='the stone ledge in front of the tank'),
            fields={'puff': (0, 0, 1), 'nerve': (0, 0, 1), 'crumbs': (0, 0, 1)},
            physics=[('puff', 'rate', -0.003, 'always'), ('nerve', 'rate', -0.0004, 'always'), ('crumbs', 'rate', -0.002, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12], ['crumbs', 'set', 1]],
                lead=[['subject.trust', 'add', 0.1], ['nerve', 'mul', 0.6]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
                startle=[['puff', 'set', 1], ['nerve', 'add', 0.3]],
                soothe=[['nerve', 'mul', 0.3], ['puff', 'mul', 0.4], ['subject.trust', 'add', 0.1]],
                snap=[['subject.hunger', 'add', -0.2], ['subject.mood', 'add', 0.15]],
            ),
            marks=[('puff', 0.3, '*(O)*', 'bob_m', 'water'), ('crumbs', 0.3, '.o.o.', 'puff_r', 'dust')],
            anchors=dict(
                puff_l=(0.2927, 0.7288),
                puff_r=(0.6504, 0.7288),
                bob_l=(0.1626, 0.7288),
                bob_m=(0.4715, 0.7288),
                bob_r=(0.7967, 0.7288),
                top_l=(0.2439, 0.6271),
                top_m=(0.4715, 0.6271),
                skin_m=(0.5528, 0.5763),
                ledge_r=(0.748, 0.8305, 'surface'),
            ))
    o.r('peer_for_any_bent_spine', 'Peering at the little spines along a puffed flank for any bent or broken one, bill an inch from the wall', 22, 'none',
        [k(.06, x=.4, y=.5, b=.3), k(.18, 'bob_l', x=1.3, y=1.3, b=.7, eye='o'), k(.32, 'bob_l', x=1.5, y=1.5, b=.9, eye='O', mark='hm'), k(.48, 'bob_m', x=1.4, y=1.5, b=.9, r=1), k(.62, 'bob_r', x=1.5, y=1.6, b=1, l=1, mark='ok'), k(.8, x=.5, y=.6, b=.3, w=.4, eye='^')],
        [(0.48, 'tend')], g='care', act=('peer', 'spines'), when=['fish_health<.8'], prefer=['puff>.3'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.5, {'lure': 1}), (0.64, {'lure': 1})],
        say=['All spines straight. Alarming for a creature that cannot hold a grudge.', 'No bent ones. It has better posture than me.'])
    o.r('press_a_hard_crumb_to_the_wall', 'Pressing a hard crumb flat to the wall with his bill, the fused beak chomping at it from the other side', 22, 'none',
        [k(.06, x=.5, y=.8, b=.4), k(.18, 'bob_m', x=1.5, y=1.5, b=.8, eye='o', mark='...'), k(.32, 'bob_m', x=1.7, y=1.7, b=1, eye='O', mark='CRNCH'), k(.46, 'bob_m', x=1.6, y=1.6, b=.9, l=1, mark='crnch'), k(.64, x=.5, y=.8, b=.4, w=.4, eye='^'), k(.84, eye='-')],
        [(0.32, 'feed')], g='use', act=('press', 'crumb'), when=['fish_hunger>.4'], prefer=['crumbs<.4'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.5, {'lure': 1}), (0.7, {'lure': 0})],
        say=['Crunched it like a tiny wood chipper.', 'A beak made for rocks, eating my crumb with feeling.'])
    o.r('walk_it_slowly_along_the_wall', 'Dragging a wingtip along the wall at a slow walk so the puffer ambles after it, nerves quieting as it goes', 26, 'wing',
        [k(.06, 'puff_l', reach=.4, x=.3, y=.7, b=.3), k(.2, 'puff_l', reach=1, x=.5, y=.8, b=.5), k(.36, 'bob_m', reach=1, x=.7, y=.7, b=.4, l=1), k(.54, 'bob_r', reach=1, x=.9, y=.7, b=.4), k(.72, 'puff_r', reach=1, x=1.1, y=.8, b=.5, r=1), k(.9, eye='^')],
        [(0.54, 'lead')], g='use', act=('drag', 'wingtip'), when=['nerve>.3'], pick='hungriest',
        obj=[(0.14, {'lure': 1}), (0.34, {'lure': 1}), (0.54, {'lure': 1}), (0.76, {'lure': 1})],
        say=['Walked it round. It forgot to be afraid, which is a start.', 'Wing, wall, puffer. Slow therapy.'])
    o.r('stroke_the_wall_in_slow_circles', 'Patting the wall in slow circles with the back of a wing where the puffer hangs near, a lullaby without notes', 22, 'wing',
        [k(.07, 'bob_l', reach=.4, x=.2, y=.5, b=.3), k(.22, 'bob_l', reach=.9, x=.3, y=.7, b=.7, mark='circ'), k(.38, 'bob_l', reach=1, x=.4, y=.8, b=.8, l=1, mark='circ'), k(.54, 'bob_l', reach=1, x=.3, y=.7, b=.7, r=1, mark='circ'), k(.72, 'bob_l', reach=.5, x=.2, y=.5, b=.4), k(.9, eye='^')],
        [(0.38, 'stroke')], g='care', act=('pat', 'wall'), prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('prod_the_wall_sharp_to_see_it_pop', 'Prodding the wall once, sharp, with a wingtip just to see the puffer go off like a balloon', 16, 'wing',
        [k(.08, 'bob_m', reach=.4, x=.2, y=.4, b=.2), k(.2, 'bob_m', reach=.4, x=-.2, y=.1, b=-.2, eye='>'), k(.32, 'bob_m', reach=1, x=.9, y=.5, b=.8, mark='BOP'), k(.5, 'bob_m', reach=.5, x=.3, y=.3, b=.2, eye='O', mark='POOF'), k(.7, eye='^')],
        [(0.32, 'startle')], g='show', act=('prod', 'wall'), prefer=['curious', 'young'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.5, {'lure': 1})],
        say=['Poof. The wall is now mostly puffer.', 'Prodded it once. Balloon season is open.', 'That was cheap and I would do it again.'])
    o.r('lay_a_calm_wing_flat_on_the_wall', 'Pressing one calm wing flat against the wall beside the ballooned puffer, breathing slow until it shrinks', 28, 'wing',
        [k(.06, 'puff_r', reach=.4, x=.3, y=.6, b=.3), k(.2, 'puff_r', reach=1, x=.5, y=.9, b=.8, eye='-'), k(.4, 'puff_r', reach=1, x=.5, y=1.1, b=1.1, eye='-', mark='shhh'), k(.62, 'puff_r', reach=1, x=.5, y=1, b=1, l=1, eye='-'), k(.8, 'puff_r', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(0.4, 'soothe')], g='use', act=('press', 'wing'), when=['puff>.3'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Down it went, one sigh at a time. Contagious.', 'Slow breath. The puffer copied me and remembered itself.'])
    o.r('puff_up_back_at_the_puffer', 'Blowing his own chest out against the wall in a stand-off, eye to eye with a puffer doing the very same', 20, 'none',
        [k(.06, 'bob_r', x=.4, y=.4, b=.4), k(.18, 'bob_r', x=1.1, y=.1, b=1.6, w=.4, eye='O', mark='HUFF'), k(.32, 'bob_r', x=1.3, y=0, b=2.1, w=.7, l=1, eye='@', mark='HUFF'), k(.5, 'bob_r', x=1.2, y=.1, b=2.3, w=.9, r=1, mark='hmmmf'), k(.66, 'bob_r', x=.6, y=.5, b=.7, w=.2, eye='>'), k(.84, eye='-')],
        [(0.32, 'startle')], g='play', act=('blow', 'chest'), prefer=['young', 'grumpy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Neither of us won. We both turned a bit purple.', 'Stand-off. I blinked first. I always blink first.'])
    o.r('seek_the_small_one_among_the_bobs', 'Seeking along the wall at mid height for the small one that has tucked itself into a corner and gone invisible', 22, 'none',
        [k(.06, 'bob_l', x=.7, y=.8, b=.5), k(.2, 'puff_l', x=1.1, y=1.2, b=.8, eye='o', mark='?'), k(.34, 'top_l', x=1.2, y=.8, b=.7, eye='o', mark='?'), k(.5, 'top_m', x=1.3, y=.9, b=.8, l=1, mark='?'), k(.64, 'puff_r', x=1.4, y=1.3, b=1, eye='O', mark='there'), k(.82, x=.4, y=.4, eye='^')],
        [], g='play', act=('seek', 'puffer'), prefer=['young', 'curious'], pick='shyest',
        obj=[(0.64, {'lure': 1}), (0.84, {'lure': 1})])
    o.r('flick_crumbs_for_a_beak_snap_count', 'Flicking hard crumbs over the top one at a time and catching the beak snaps that follow from the wall side', 22, 'wing',
        [k(.06, 'skin_m', reach=.4, x=.2, y=0), k(.18, 'skin_m', reach=1, x=.4, y=-.5, b=-.4, mark='flk'), k(.3, 'skin_m', reach=.5, x=.1, y=.1, b=0, mark='1'), k(.42, 'skin_m', reach=1, x=.4, y=-.5, b=-.4, l=1, mark='flk'), k(.55, 'skin_m', reach=.5, x=.1, y=.1, b=0, mark='2'), k(.7, 'skin_m', reach=1, x=.4, y=-.6, b=-.5, r=1, mark='flk'), k(.86, eye='o', mark='3')],
        [(0.42, 'snap')], g='play', act=('catch', 'crumbs'), prefer=['happy', 'curious'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('measure_the_balloon_against_a_wing', 'Measuring how wide the ballooned puffer is by spreading a wing against the wall, then letting it settle and measuring again', 26, 'wing',
        [k(.05, 'bob_m', reach=.5, x=.3, y=.5, b=.3), k(.18, 'bob_l', reach=1, x=.5, y=.5, b=.4, mark='this'), k(.3, 'bob_r', reach=1, x=.6, y=.5, b=.4, l=1, mark='wide'), k(.46, 'bob_m', reach=.5, x=.2, y=.6, b=.5, eye='-', mark='...'), k(.62, 'bob_m', reach=1, x=.4, y=.7, b=.6, r=1, mark='less'), k(.8, eye='O', mark='half')],
        [], g='test', act=('measure', 'balloon'), when=['puff>.3'], prefer=['curious'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Three wing widths ballooned, one and a half relaxed. Physics is rude.', 'It doubles and halves on a whim. Not a reliable specimen.'])
    o.r('count_the_spines_one_by_one', 'Counting the spines along a puffed side with a bill dip each time, keeping pace with a fish that will not hold still', 22, 'none',
        [k(.05, 'bob_l', x=1, y=1.2, b=.5, mark='1'), k(.16, 'bob_l', x=1.1, y=1.3, b=.6, mark='6'), k(.28, 'bob_m', x=1.2, y=1.3, b=.7, l=1, mark='13'), k(.42, 'bob_m', x=1.3, y=1.4, b=.8, mark='20'), k(.56, 'bob_r', x=1.4, y=1.5, b=.9, r=1, mark='27?'), k(.7, x=-.3, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.88, eye='-')],
        [], g='test', act=('count', 'spines'), prefer=['curious'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.5, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('wait_for_the_puff_to_go_down', 'Waiting dead still at the wall for the ballooned puffer to let its breath out and trust him again', 26, 'none',
        [k(.08, 'bob_m', x=.8, y=1.2, b=.7, eye='o'), k(.3, 'bob_m', x=.9, y=1.4, b=.9, eye='o'), k(.52, 'bob_m', x=.9, y=2.0, b=.9, l=1), k(.7, 'bob_m', x=1, y=1.5, b=1, eye='O', mark='...'), k(.88, 'bob_m', x=.4, y=.6, b=.4, eye='^')],
        [(0.7, 'soothe')], g='rest', act=('wait', 'puff'), when=['puff>.3'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.82, {'lure': 1})])
    o.r('present_the_puffer_with_a_flourish', 'Presenting the puffer with a flourish, one wing sweeping out like a magician revealing a balloon', 20, 'wing',
        [k(.07, 'top_l', reach=.4, x=.1, y=.1), k(.22, 'top_l', reach=.9, x=.3, y=-.4, b=-.3), k(.4, 'top_m', reach=1, x=.4, y=-1.3, b=-.6, mark='behold'), k(.56, 'top_m', reach=1, x=.3, y=-.5, b=-.4, l=1), k(.74, 'top_m', reach=.6, x=.5, y=0), k(.9, eye='^')],
        [], g='show', act=('present', 'puffer'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_about_who_is_rounder', 'Arguing with the puffer about which of them is rounder, jabbing a wing at its belly and then at his own', 20, 'wing',
        [k(.07, 'bob_l', reach=.5, x=.6, y=.3, b=.4), k(.22, 'bob_l', reach=1, x=1.1, y=.2, b=.3, mark='ROUNDER'), k(.38, 'bob_l', reach=.5, x=.4, y=.4, b=1.4, l=1, mark='ME'), k(.54, 'bob_l', reach=1, x=1.2, y=.1, b=.2, r=1, mark='YOU'), k(.72, 'bob_l', reach=.5, x=.4, y=.5, b=1.2, mark='ME'), k(.88, eye='-')],
        [], g='show', act=('argue', 'belly'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It won. Rounder by an arc.', 'I have been out-rounded by a fish the size of a pear.'])
    o.r('pose_with_a_puffed_chest_on_the_ledge', 'Striking a heroic pose on the right ledge with a chest as big as it will go, while the real puffer does it better', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.1, b=.3, w=.3, perch=1), k(.24, 'ledge_r', x=.6, y=-.5, b=1.4, w=.7, perch=1), k(.5, 'ledge_r', x=.8, y=-.8, b=2, w=1, perch=1, eye='^', mark='big'), k(.74, 'ledge_r', x=.3, y=0, b=.4, w=.3, perch=1)],
        [], g='show', act=('pose', 'ledge'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('leap_back_from_the_sudden_balloon', 'Hopping back with a yelp when the puffer swells to ten times its size an inch from his bill', 16, 'none',
        [k(.06, 'bob_m', x=1.1, y=1.5, b=.8), k(.18, 'bob_m', x=1.3, y=1.7, b=1, eye='o', mark='...'), k(.28, x=-1.4, y=-.9, b=-1.4, l=1, r=1, w=1, eye='O', mark='YELP'), k(.44, x=-.8, y=.2, b=-.1, w=.7, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'balloon'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.45, {'lure': 1})],
        say=['It was small, then it was a planet.', 'Swore I saw a face on it. A cross one.'])
    o.r('pass_a_hard_crumb_down_the_wall', 'Pressing a hard crumb to the wall for the puffer while a friend does the same two spots along, so it hops from beak to beak', 26, 'none',
        [k(.05, 'puff_l', x=.7, y=1, b=.5), k(.2, 'puff_l', x=1.6, y=1.6, b=.8, eye='o', mark='tp'), k(.36, 'puff_l', x=.8, y=.7, b=.4, w=.4), k(.52, 'bob_m', x=1.7, y=1.6, b=.9, mark='tp'), k(.7, 'bob_m', x=.9, y=.8, b=.5, eye='O'), k(.86, eye='^')],
        [(0.52, 'snap')], g='use', act=('press', 'beak'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.56, {'lure': 1})],
        say=['Beak to beak, crumb to crumb. A puffer relay.', 'Two ducks feeding one balloon. The usual civic duty.'],
        duo=[k(.12, 'puff_r', x=.6, y=.9, b=.5), k(.3, 'puff_r', x=1.5, y=1.5, b=.8, mark='tp'), k(.46, 'puff_r', x=.8, y=.7, b=.4), k(.62, 'bob_r', x=1.6, y=1.5, b=.9, l=1, mark='tp'), k(.8, eye='^')])
    o.r('calm_it_from_both_sides_of_the_wall', 'Guarding a calm wing on the wall to one side of the ballooned puffer while a friend does the same on the other, until it sinks', 28, 'wing',
        [k(.06, 'bob_l', reach=.4, x=.3, y=.6, b=.3), k(.2, 'bob_l', reach=1, x=.5, y=.8, b=.7, eye='-'), k(.42, 'bob_l', reach=1, x=.5, y=1, b=1, eye='-', mark='shhh'), k(.64, 'bob_l', reach=1, x=.5, y=.9, b=.9, l=1), k(.82, 'bob_l', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(0.42, 'soothe')], g='rest', act=('guard', 'balloon'), when=['puff>.3'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Two quiet wings and one fat balloon. It deflated out of politeness.', 'A puffer talked down. Wings only, no words.'],
        duo=[k(.1, 'bob_r', x=.4, y=.6, b=.3), k(.26, 'bob_r', x=.6, y=.9, b=.8, eye='-'), k(.46, 'bob_r', x=.6, y=1, b=1, eye='-', mark='shhh'), k(.68, 'bob_r', x=.6, y=.9, b=.9, r=1), k(.84, eye='^')])
    o.r('guess_the_number_of_spines_with_a_friend', 'Weighing up the number of spines with a friend at the other end of the wall, each of them sure and each wildly off', 24, 'none',
        [k(.05, 'bob_l', x=1.2, y=.7, b=.8, mark='forty'), k(.19, 'bob_l', x=1.3, y=.9, b=1, mark='sixty'), k(.33, 'bob_m', x=1.4, y=.8, b=1.1, l=1, mark='a hundred?'), k(.5, 'bob_m', x=1.3, y=.3, b=.6, w=.6, mark='nope'), k(.68, 'bob_m', x=.9, y=.5, b=.5, eye='-', mark='fine'), k(.86, eye='^')],
        [], g='test', act=('weigh', 'spines'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.35, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Ninety and a hundred. The fish counted none. Fair.', 'Both of us wrong. The puffer kept the answer.'],
        duo=[k(.1, 'bob_r', x=.8, y=1, b=.5, mark='thirty'), k(.28, 'bob_r', x=.9, y=1.1, b=.6, mark='eighty'), k(.44, 'bob_m', x=1, y=1, b=.6, r=1, mark='ninety'), k(.62, 'bob_r', x=.7, y=.7, b=.4, eye='-'), k(.8, eye='^')])
    o.r('cool_the_glass_with_a_flapped_breeze', 'Cooling the sun-warmed glass with a flapped breeze so the puffer stops sulking at the top', 20, 'wing',
        [k(.12, 'puff_l', reach=.5, x=.2, y=.5, b=.4), k(.3, 'puff_l', reach=1, x=.3, y=.7, b=.6, w=.8), k(.5, 'puff_r', reach=1, x=.3, y=1.3, b=.7, l=1, w=1, mark='fff'), k(.7, 'puff_l', reach=1, x=.3, y=.7, b=.6, r=1, w=.8), k(.88, eye='^')],
        [(.5, 'cheer')], g='weather', act=('cool', 'glass'), when=['sun'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.6, {'lure': 1})], say=['The puffer relaxed one spine. A victory.', 'I fanned a fish tank. Career peak.'])
    return o


def swordfish():
    o = Obj('swordfish', 'keeping', on='infinity_pool', 
            parts=dict(low='the lower glass of the tank', flank='the side glass of the tank', top='the top run of water in the tank', skin='the water line under the coping', coping='the coping along the top of the tank', ledge='the stone ledge in front of the tank', pier='the stone pier at the end of the tank'),
            fields={'wake': (0, 0, 1), 'slash': (0, 0, 1)},
            physics=[('slash', 'rate', 0.003, 'dawn'), ('slash', 'rate', 0.003, 'dusk'), ('slash', 'rate', -0.002, 'day'), ('wake', 'rate', -0.006, 'always')],
            effects=dict(
                double=[['wake', 'set', 1], ['subject.hunger', 'add', -0.25], ['slash', 'mul', 0.4]],
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                strike=[['wake', 'set', 1], ['subject.hunger', 'add', -0.2], ['slash', 'mul', 0.5]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                tease=[['slash', 'add', 0.25], ['subject.trust', 'add', 0.1]],
                soothe=[['slash', 'mul', 0.4], ['subject.mood', 'add', 0.15]],
                fun=[['need.fun', 'add', 2]],
            ),
            marks=[('wake', 0.3, '=====', 'skin_l', 'water')],
            anchors=dict(
                low_l=(0.2927, 0.7288),
                low_r=(0.6504, 0.7288),
                flank_l=(0.1951, 0.7797),
                flank_r=(0.7642, 0.7797),
                top_l=(0.2439, 0.6271),
                top_m=(0.4715, 0.6271),
                top_r=(0.7154, 0.6271),
                skin_l=(0.2764, 0.5763),
                skin_r=(0.6179, 0.5763),
                coping=(0.3252, 0.4746),
                ledge_r=(0.748, 0.8305, 'surface'),
                pier_l=(0.0813, 0.6949),
                pier_r=(0.8943, 0.6949),
            ))
    o.r('peer_down_the_length_of_the_sword', 'Peering all the way down the length of the sword for any chip or crack in the tip, tracking its slow turn at the wall', 22, 'none',
        [k(.05, x=.4, y=.4, b=.3), k(.16, 'low_l', x=1.6, y=1.4, b=.9, eye='o'), k(.28, 'top_l', x=1.8, y=.7, b=.8, eye='O', mark='hm'), k(.42, 'top_m', x=1.9, y=.6, b=.7, r=1), k(.56, 'top_r', x=2, y=.5, b=.7, l=1, mark='ok'), k(.74, x=.5, y=.5, b=.3, w=.4, eye='^')],
        [(0.42, 'tend')], g='care', act=('peer', 'sword'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.16, {'lure': 1}), (0.42, {'lure': 1}), (0.58, {'lure': 1})],
        say=['Tip intact. A dangerous thing, to have a point.', 'No chips. It has been cutting nothing with real discipline.'])
    o.r('dangle_a_flake_on_a_reed_for_the_slash', 'Lifting a flake on the end of a reed a hand above the water line, snatching it back as the sword slashes up at it', 24, 'reed',
        [k(.05, 'coping', reach=.4, x=.2, y=-.1), k(.16, 'coping', reach=1, x=.5, y=-.4, b=-.2, mark='...'), k(.3, 'skin_l', reach=1, x=.7, y=-.5, b=-.3, l=1), k(.44, 'skin_l', reach=1, x=.3, y=-.9, b=-.9, w=.3, eye='O', mark='SHNK'), k(.6, 'skin_r', reach=.8, x=-.3, y=.2, b=.2), k(.78, eye='>')],
        [(0.44, 'strike')], g='use', act=('lift', 'flake'), when=['slash>.3'], pick='hungriest',
        obj=[(0.16, {'lure': 1}), (0.34, {'lure': 1}), (0.5, {'lure': 1})],
        say=['Slashed it clean. I held on to the reed and a bit of pride.', 'Missed the flake. Hit the dream.'])
    o.r('trail_a_wingtip_fast_along_the_wall', 'Dragging a wingtip fast along the upper wall in quick jerks to tease the sword into one long hot run', 20, 'wing',
        [k(.05, 'top_l', reach=.5, x=.3, y=.2, b=.2), k(.14, 'top_l', reach=1, x=.5, y=.3, b=.4, l=1), k(.24, 'top_m', reach=1, x=.9, y=.3, b=.3), k(.34, 'top_m', reach=1, x=1.2, y=.3, b=.3, r=1), k(.46, 'top_r', reach=1, x=1.5, y=.3, b=.3, l=1), k(.6, 'top_r', reach=.8, x=1.2, y=.2, b=.2), k(.8, eye='@')],
        [(0.34, 'tease')], g='use', act=('drag', 'wingtip'), when=['slash<.7'], pick='hungriest',
        obj=[(0.1, {'lure': 1}), (0.25, {'lure': 1}), (0.4, {'lure': 1}), (0.58, {'lure': 1})],
        say=['Teased it into a streak. I could not tell which end was which.', 'I move a wingtip, it moves the world.'])
    o.r('settle_a_wing_on_the_wall_to_slow_it', 'Pressing a still wing flat against the wall at mid height until the keyed-up fish slows to a hover and stops slashing', 26, 'wing',
        [k(.06, 'low_r', reach=.4, x=.3, y=.7, b=.4), k(.2, 'low_r', reach=1, x=.5, y=.9, b=.8, eye='-'), k(.42, 'low_r', reach=1, x=.5, y=1.5, b=1.4, eye='-', mark='easy'), k(.64, 'low_r', reach=1, x=.5, y=1, b=1, l=1), k(.82, 'low_r', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(0.42, 'soothe')], g='use', act=('press', 'wall'), when=['slash>.4'], pick='shyest',
        obj=[(0.2, {'lure': 1}), (0.62, {'lure': 1})],
        say=['It stopped. Hovered. Looked, for once, like a fish.', 'Slow wing, slow sword. A deal was struck.'])
    o.r('hold_a_flake_to_the_wall_for_the_bill', 'Pressing a flake flat to the wall with the tip of his bill while the long sword turns and the small mouth takes it from the other side', 22, 'none',
        [k(.05, x=.4, y=.6, b=.4), k(.18, 'low_l', x=1.7, y=1.4, b=.8, eye='o', mark='...'), k(.32, 'low_l', x=1.9, y=1.5, b=1, eye='O', mark='SNP'), k(.46, 'low_l', x=1.8, y=1.4, b=.9, l=1), k(.64, x=.5, y=.7, b=.4, w=.4, eye='^'), k(.84, eye='-')],
        [(0.32, 'feed')], g='use', act=('press', 'flake'), when=['fish_hunger>.4'], pick='shyest',
        obj=[(0.18, {'lure': 1}), (0.48, {'lure': 1}), (0.66, {'lure': 0})])
    o.r('raise_a_reed_hoop_for_the_streak', 'Lifting a reed bent in a hoop at the top of the tank with both ends held, so the swordfish threads it at speed', 24, 'reed',
        [k(.05, 'top_r', reach=.4, x=.2, y=.1), k(.18, 'skin_r', reach=1, x=.5, y=-.2, b=-.1), k(.32, 'skin_r', reach=1, x=.6, y=-.4, b=-.3, w=.2, mark='steady'), k(.46, 'skin_r', reach=1, x=.5, y=-.6, b=-.5, l=1, r=1, eye='O', mark='ZIP'), k(.62, 'top_r', reach=.8, x=.3, y=0, b=0, eye='o'), k(.82, eye='^')],
        [(0.46, 'strike')], g='show', act=('lift', 'hoop'), prefer=['fish_trust>.4', 'happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.58, {'lure': 1})],
        say=['Through the hoop and out the other side. I did not see it.', 'A hoop for a streak. We call it a ride.'])
    o.r('race_the_streak_and_lose_gloriously', 'Having a race with the streak along the wall at a flat run, wings back, and losing before he has taken three strides', 18, 'none',
        [k(.04, 'flank_l', x=.7, y=.2, b=.3), k(.12, 'low_l', x=1.5, y=.2, b=-1, l=1, w=.5), k(.22, 'top_m', x=1.9, y=.1, b=-.4, r=1, w=.9, mark='WHOO'), k(.32, 'top_r', x=2, y=.1, b=-1.1, l=1, w=1), k(.46, 'low_r', x=1.2, y=.5, b=.8, r=1, eye='@'), k(.64, 'flank_r', x=.4, y=.7, b=1, eye='x', mark='lost'), k(.84, eye='-')],
        [(0.46, 'fun')], g='play', act=('race', 'streak'), prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.1, {'lure': 1}), (0.26, {'lure': 1}), (0.4, {'lure': 1}), (0.55, {'lure': 1})],
        say=['Lost by nine wall lengths. It lapped me before I started.', 'The only race with a finish line I never saw.'])
    o.r('duck_when_the_sword_comes_at_the_wall', 'Ducking low with a whoop each time the sword jabs at the wall, hopping straight up again after it passes', 18, 'none',
        [k(.05, 'low_l', x=.5, y=.5, b=.3), k(.15, 'low_l', x=-.5, y=1.4, b=1.9, w=.4, eye='>', mark='WHOA'), k(.26, 'low_l', x=.9, y=.1, b=-1.2, w=.7, l=1, r=1), k(.4, 'low_r', x=-.6, y=1.5, b=2, w=.4, eye='>', mark='WHOA'), k(.52, 'low_r', x=1, y=.1, b=-1.3, w=.8, l=1, r=1), k(.68, 'low_r', x=.4, y=.4, b=.4), k(.86, eye='@')],
        [], g='play', act=('hop', 'sword'), prefer=['young', 'curious', 'wake>.3'], pick='hungriest',
        obj=[(0.1, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.7, {'lure': 1})])
    o.r('fence_the_swordfish_with_a_reed', 'Prodding with a reed in a fence against the wall while the sword jabs back from the other side, lunge for lunge', 22, 'reed',
        [k(.05, 'low_r', reach=.4, x=.4, y=.2, b=.2), k(.16, 'low_r', reach=1, x=1.1, y=.1, b=.5, l=1, mark='haa'), k(.26, 'low_r', reach=.5, x=.2, y=.3, b=-.2), k(.38, 'top_r', reach=1, x=1.3, y=0, b=.6, r=1, mark='HAA'), k(.5, 'top_r', reach=.5, x=.2, y=.2, b=-.3), k(.64, 'low_r', reach=1, x=1.4, y=.1, b=.7, l=1, mark='TOUCHE'), k(.84, eye='@')],
        [], g='play', act=('prod', 'reed'), prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.16, {'lure': 1}), (0.4, {'lure': 1}), (0.64, {'lure': 1})],
        say=['Parried twice. Hit once, by accident. Honour satisfied.', 'Reed versus sword is not a fair fight, but it is a loud one.'])
    o.r('measure_the_sword_against_a_reed', 'Holding a reed up beside the sword to measure how much of the fish is sword and how much is fish', 24, 'reed',
        [k(.05, 'low_l', reach=.4, x=.3, y=.4, b=.2), k(.18, 'low_l', reach=1, x=.6, y=.5, b=.4, mark='this'), k(.32, 'top_l', reach=1, x=.7, y=.2, b=.3, l=1, mark='much'), k(.46, 'top_m', reach=1, x=.9, y=.2, b=.3, mark='sword'), k(.62, 'low_l', reach=.7, x=.4, y=.6, b=.5, eye='o', mark='a third'), k(.8, eye='-')],
        [], g='test', act=('measure', 'sword'), prefer=['curious'], pick='shyest',
        obj=[(0.25, {'lure': 1}), (0.5, {'lure': 1})],
        say=['A third of it is sword. The rest is attitude.', 'Longer than my leg. Longer than my patience.'])
    o.r('wait_for_the_first_streak_of_the_day', 'Waiting stock-still at the wall for the first streak of the day to cut the water, wings pinned', 24, 'none',
        [k(.08, 'top_m', x=.9, y=.5, b=.7, eye='o'), k(.28, 'top_m', x=1, y=.6, b=.9, eye='o'), k(.5, 'top_m', x=1, y=.6, b=.9, l=1), k(.7, 'top_m', x=1.1, y=.7, b=1, eye='O', mark='...'), k(.88, 'top_m', x=.4, y=.3, b=.4, eye='^')],
        [], g='rest', act=('wait', 'streak'), when=['slash>.3'], prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_over_who_is_the_sharper', 'Arguing with the swordfish about which of them is the sharper, jabbing his bill at the sword and then at his own head', 22, 'none',
        [k(.06, 'low_l', x=.8, y=.5, b=.5), k(.2, 'low_l', x=1.4, y=.4, b=.3, mark='SHARPER'), k(.36, 'low_l', x=.4, y=.5, b=.7, l=1, mark='ME'), k(.52, 'low_l', x=1.5, y=.3, b=.2, r=1, mark='YOU'), k(.7, 'low_l', x=.4, y=.5, b=.6, eye='-', mark='ME!'), k(.86, eye='-')],
        [], g='show', act=('argue', 'edge'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['It is a fish on a stick. I am, regardless, sharper.', 'Lost on points. It had several.'])
    o.r('pose_on_the_ledge_with_a_bill_raised_like_a_sword', 'Striking a pose on the right ledge with his bill thrust up like a sword, wings back, hero of a very small ship', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.2, w=.3, perch=1), k(.24, 'ledge_r', x=.7, y=-.8, b=-.4, w=.6, perch=1), k(.5, 'ledge_r', x=.9, y=-1.2, b=-.7, w=1, perch=1, eye='^', mark='en garde'), k(.74, 'ledge_r', x=.3, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'ledge'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('shout_a_countdown_for_the_run', 'Shouting a countdown from the left post and flinging both wings up at zero as the swordfish tears down the tank', 18, 'none',
        [k(.06, 'pier_l', x=.3, y=-.1, b=.3), k(.18, 'pier_l', x=.5, y=-.4, b=-.2, w=.4, mark='THREE'), k(.3, 'pier_l', x=.6, y=-.5, b=-.3, w=.6, l=1, mark='TWO'), k(.42, 'pier_l', x=.7, y=-.6, b=-.4, w=.8, r=1, mark='ONE'), k(.56, 'pier_l', x=.9, y=-.9, b=-.8, w=1, mark='GO!'), k(.74, 'pier_l', x=.3, y=0, b=.1), k(.9, eye='@')],
        [], g='show', act=('shout', 'countdown'), when=['slash>.3'], prefer=['happy', 'young'], pick='hungriest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Three, two, one. It was already at the far end.', "Starter's pistol for an animal that does not need one."])
    o.r('flinch_when_the_sword_hits_the_wall', 'Hopping back with a squawk when the sword smacks the wall right where his bill was resting, the whole tank shivering', 16, 'none',
        [k(.06, 'top_l', x=1.2, y=.7, b=.7), k(.16, 'top_l', x=1.4, y=.8, b=.9, eye='o', mark='...'), k(.24, x=-1.5, y=-1, b=-1.5, l=1, r=1, w=1, eye='O', mark='THWACK'), k(.4, x=-.9, y=.2, b=-.2, w=.7, eye='>'), k(.6, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'wall'), prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.16, {'lure': 1}), (0.4, {'lure': 1})],
        say=['Eight inches from my face. It missed on purpose, I tell myself.', 'That sword has a will of its own. And a hell of an aim.'])
    o.r('hold_two_hoops_for_one_streak', 'Hooking a reed hoop at the left of the tank while a friend holds another at the right, so the swordfish threads both in one pass', 28, 'reed',
        [k(.05, 'top_l', reach=.4, x=.2, y=.1), k(.18, 'skin_l', reach=1, x=.5, y=-.2, b=-.1), k(.32, 'skin_l', reach=1, x=.6, y=-.4, b=.4, w=.2, mark='steady'), k(.46, 'skin_l', reach=1, x=.5, y=-.6, b=-.5, l=1, r=1, eye='O', mark='ZIP'), k(.62, 'top_l', reach=.8, x=.3, y=0, eye='o'), k(.8, eye='^')],
        [(0.46, 'double')], g='play', act=('hook', 'hoops'), when=['slash>.3'], prefer=['happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.42, {'lure': 1}), (0.6, {'lure': 1})],
        say=['One streak, two hoops, perfect. I only missed my hoop.', 'A pass through both. The fish is the only one who looks calm.'],
        duo=[k(.1, 'top_r', x=.3, y=.2, b=.2), k(.28, 'skin_r', x=.6, y=-.2, b=.2, w=.3), k(.44, 'skin_r', x=.7, y=-.4, b=-.2, w=.5, mark='steady'), k(.6, 'skin_r', x=.8, y=-.7, b=-.5, l=1, r=1, w=.8, eye='O', mark='ZIP'), k(.8, eye='^')])
    o.r('keep_score_of_the_slashes_with_a_friend', 'Counting the slashes with a friend, one tallying left to right and the other right to left, each with a different total', 24, 'wing',
        [k(.05, 'pier_l', reach=.4, x=.3, y=.4, b=.2, mark='1'), k(.16, 'low_l', reach=1, x=.5, y=.5, b=.4, mark='2'), k(.28, 'top_l', reach=1, x=.6, y=.3, b=.3, l=1, mark='3'), k(.4, 'top_m', reach=1, x=.7, y=.3, b=.3, r=1, mark='4'), k(.54, 'top_r', reach=1, x=.8, y=.3, b=.3, mark='5'), k(.7, 'pier_r', reach=.5, x=.4, y=.4, b=.2, eye='-', mark='6?'), k(.86, eye='^')],
        [], g='test', act=('count', 'tallies'), prefer=['curious', 'happy'], pick='shyest',
        obj=[(0.3, {'lure': 1}), (0.62, {'lure': 1})],
        say=['Six and seven. The fish ignored the dispute and scored eleven.', 'Two scorers, two totals. A fish keeps the real count.'],
        duo=[k(.1, 'pier_r', x=.4, y=.4, b=.3, mark='1'), k(.24, 'top_r', x=.5, y=.3, b=.3, mark='2'), k(.38, 'top_m', x=.6, y=.3, b=.4, l=1, mark='3'), k(.54, 'top_l', x=.7, y=.3, b=.3, r=1, mark='4'), k(.7, 'pier_l', x=.4, y=.4, b=.3, eye='-', mark='7?'), k(.84, eye='^')])
    o.r('brace_a_wing_against_the_spray_off_the_top', 'Bracing a wing against the spray flung off the top run while the sword cuts across above', 22, 'wing',
        [k(.12, 'low_l', reach=.4, x=.1, y=.4, b=.5), k(.3, 'low_l', reach=1, x=-.2, y=.5, b=.9, w=.8), k(.55, 'low_r', reach=1, x=-.5, y=.6, b=1.1, w=1, r=1, mark='psh'), k(.78, 'low_r', reach=.6, x=-.2, y=.4, b=.6, eye='^'), k(.9, eye='-')],
        [(.55, 'cheer')], g='weather', act=('brace', 'spray'), when=['windy'], pick='hungriest',
        obj=[(.3, {'lure': 1}), (.65, {'lure': 1})], say=['Spray in the face from a fish with an attitude.', 'Braced. Wet. Not once looked at the sword.'])
    return o


def ancient_dragon_fish():
    o = Obj('ancient_dragon_fish', 'keeping', on='infinity_pool', 
            parts=dict(low='the lower glass of the tank', mid='the middle glass of the tank', body='the tank glass along the fish', skin='the water line under the coping', coping='the coping along the top of the tank', base='the foot of the tank wall', ledge='the stone ledge in front of the tank', lip='the front lip of the pool'),
            fields={'glow': (0, 0, 1), 'coil': (0, 0, 1), 'trail': (0, 0, 1)},
            physics=[('glow', 'rate', 0.003, 'night'), ('glow', 'rate', -0.004, '!night'), ('coil', 'rate', 0.0004, 'always'), ('trail', 'rate', -0.003, 'always')],
            effects=dict(
                cheer=[['subject.mood', 'add', 0.15]],
                tend=[['subject.health', 'add', 0.12], ['subject.trust', 'add', 0.1]],
                feed=[['subject.hunger', 'add', -0.25], ['subject.trust', 'add', 0.12]],
                uncoil=[['coil', 'mul', 0.3], ['trail', 'set', 1], ['subject.trust', 'add', 0.1]],
                rise=[['subject.hunger', 'add', -0.2], ['trail', 'set', 1]],
                stroke=[['subject.mood', 'add', 0.15], ['subject.trust', 'add', 0.1]],
            ),
            marks=[('glow', 0.3, '. * .', 'body_m', 'glow'), ('trail', 0.3, '~*~*~', 'low_l', 'glow'), ('coil', 0.5, '(OOO)', 'low_r', 'water')],
            anchors=dict(
                low_l=(0.2927, 0.7288),
                low_m=(0.4715, 0.7288),
                low_r=(0.6992, 0.7288),
                mid_l=(0.1951, 0.678),
                body_l=(0.2439, 0.6271),
                body_m=(0.5041, 0.6271),
                body_r=(0.748, 0.6271),
                skin_m=(0.5528, 0.5763),
                coping=(0.3252, 0.4746),
                base_l=(0.1951, 0.7797),
                ledge_l=(0.2439, 0.8305, 'surface'),
                ledge_r=(0.748, 0.8305, 'surface'),
                lip=(0.4878, 0.8814, 'surface'),
            ))
    o.r('peer_for_a_loose_jewel_scale', "Peering along the serpent's glowing flank for any loose or missing scale as it unrolls past the wall", 22, 'none',
        [k(.05, x=.5, y=.5, b=.4), k(.15, 'low_l', x=1.5, y=1.3, b=.9, eye='o'), k(.27, 'mid_l', x=1.7, y=.8, b=.9, eye='O', mark='hm'), k(.4, 'body_l', x=1.8, y=.6, b=.8, l=1), k(.54, 'body_m', x=1.9, y=.6, b=.8, r=1, mark='ok'), k(.7, 'low_r', x=1.6, y=1.2, b=.9), k(.86, x=.6, y=.5, b=.3, w=.4, eye='^')],
        [(0.54, 'tend')], g='care', act=('peer', 'scales'), when=['fish_health<.8'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.4, {'lure': 1}), (0.7, {'lure': 1})],
        say=['Every scale in place. It must have a good lawyer.', 'A thousand jewels, none loose. Better kept than my feathers.'])
    o.r('press_a_flake_to_the_wall_for_the_whiskers', 'Pressing one flake to the wall with his bill, the long whiskers drifting against the other side to find it', 22, 'none',
        [k(.06, x=.4, y=.7, b=.4), k(.18, 'low_m', x=1.7, y=1.7, b=.9, eye='o', mark='...'), k(.31, 'low_m', x=1.9, y=1.9, b=1.1, eye='O', mark='whff'), k(.45, 'low_m', x=1.8, y=1.8, b=1, l=1), k(.62, x=.6, y=.8, b=.5, w=.4, eye='^'), k(.82, eye='-')],
        [(0.31, 'feed')], g='use', act=('press', 'flake'), when=['fish_hunger>.4'], pick='hungriest',
        obj=[(0.18, {'lure': 1}), (0.5, {'lure': 1}), (0.7, {'lure': 0})],
        say=['Whiskers first, then the mouth. It tastes by touch.', 'One flake, a lot of ceremony.'])
    o.r('unwind_the_serpent_with_a_slow_wingtip', 'Dragging a wingtip slowly along the wall so the tightly wound serpent unwinds a coil at a time and glides after it', 30, 'wing',
        [k(.04, 'low_r', reach=.4, x=.2, y=.7, b=.3), k(.14, 'low_r', reach=1, x=.4, y=.9, b=.5), k(.26, 'low_m', reach=1, x=.5, y=.9, b=.5, l=1), k(.4, 'low_l', reach=1, x=.6, y=.8, b=.5), k(.54, 'mid_l', reach=1, x=.7, y=.5, b=.4, r=1), k(.7, 'body_l', reach=1, x=.8, y=.2, b=.3, l=1), k(.88, eye='^')],
        [(0.4, 'uncoil')], g='use', act=('drag', 'wingtip'), when=['coil>.4'], pick='hungriest',
        obj=[(0.1, {'lure': 1}), (0.3, {'lure': 1}), (0.5, {'lure': 1}), (0.72, {'lure': 1})],
        say=['Unwound it yard by glowing yard. Longer than the wall.', 'It followed the wingtip without hurry. Plenty to hurry about.'])
    o.r('pat_the_wall_at_the_great_brow', 'Patting the wall with the back of a wing where the great brow rests, slow strokes like soothing a very large cat', 22, 'wing',
        [k(.06, 'body_l', reach=.4, x=.2, y=.2, b=.3), k(.2, 'body_l', reach=.9, x=.4, y=.3, b=.5, mark='pat'), k(.36, 'body_l', reach=1, x=.5, y=.3, b=.6, l=1, mark='pat'), k(.52, 'body_l', reach=1, x=.4, y=.3, b=.5, r=1, mark='pat'), k(.7, 'body_l', reach=.5, x=.2, y=.2, b=.3), k(.88, eye='^')],
        [(0.36, 'stroke')], g='use', act=('pat', 'brow'), prefer=['fish_trust<.8', 'lonely'], pick='shyest',
        obj=[(0.22, {'lure': 1}), (0.64, {'lure': 1})])
    o.r('dangle_a_flake_for_the_legend_to_rise', 'Lifting a flake on a reed over the coping until the serpent rises all the way up the wall to claim it, lit from within', 26, 'reed',
        [k(.05, 'coping', reach=.4, x=.2, y=-.1), k(.17, 'coping', reach=1, x=.5, y=-.5, b=-.2, mark='...'), k(.32, 'skin_m', reach=1, x=.7, y=-1.2, b=-.3, l=1), k(.48, 'skin_m', reach=1, x=.4, y=-1, b=-.9, w=.3, eye='O', mark='GULP'), k(.64, 'body_m', reach=.8, x=-.3, y=.2, b=.2), k(.82, eye='>')],
        [(0.48, 'rise')], g='use', act=('lift', 'flake'), when=['glow>.4'], pick='hungriest',
        obj=[(0.17, {'lure': 1}), (0.36, {'lure': 1}), (0.54, {'lure': 1})],
        say=['Rose from the dark, took the flake, left the dark in my head.', 'It surfaced like a lamp coming on.'])
    o.r('chase_the_beads_of_glow_with_a_wing', 'Chasing the drifting beads of glow along the wall with quick wing dabs, popping one only to see it re-form', 20, 'wing',
        [k(.06, 'low_l', reach=.6, x=.5, y=.7, b=.4), k(.18, 'mid_l', reach=1, x=.9, y=.4, b=.3, l=1, mark='fwp'), k(.3, 'body_l', reach=1, x=-.3, y=.3, b=.5, r=1, mark='fwp'), k(.44, 'body_m', reach=1, x=1, y=.2, b=.3, l=1, mark='pop'), k(.6, 'low_m', reach=1, x=1.1, y=.7, b=.5, eye='@'), k(.8, y=.4, eye='-')],
        [], g='play', act=('chase', 'glow'), when=['trail>.3'], prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.6, {'lure': 1})])
    o.r('look_for_the_serpent_by_its_own_light', 'Seeking along the wall for the serpent by following the faint glow it leaves in the dark, bill dipping at each smudge', 24, 'none',
        [k(.05, 'low_l', x=.7, y=.9, b=.5), k(.17, 'mid_l', x=1, y=.7, b=.7, eye='o', mark='?'), k(.3, 'body_l', x=1.2, y=.5, b=.7, eye='o', mark='?'), k(.43, 'body_m', x=1.3, y=.6, b=.8, l=1, mark='?'), k(.58, 'body_r', x=1.4, y=.5, b=.8, r=1, mark='?'), k(.72, 'low_r', x=1.5, y=1.1, b=1, eye='O', mark='found you'), k(.88, x=.4, y=.4, eye='^')],
        [], g='play', act=('seek', 'serpent'), when=['night'], prefer=['young', 'curious'], pick='shyest',
        obj=[(0.72, {'lure': 1}), (0.88, {'lure': 1})])
    o.r('hop_the_ledge_in_time_with_its_flicker', 'Hopping the ledge in time with the flicker of its scales, one hop for each ripple of light that runs down its length', 20, 'none',
        [k(.05, 'ledge_l', x=.3, y=.3, b=.3, perch=1), k(.15, 'ledge_l', x=.4, y=-.2, b=-1.1, l=1, r=1, perch=1), k(.26, 'ledge_l', x=.3, y=.4, b=.7, perch=1), k(.38, 'ledge_r', x=.5, y=-.3, b=-1.3, w=.6, l=1, r=1, perch=1), k(.5, 'ledge_r', x=.3, y=.4, b=.7, perch=1), k(.64, 'ledge_r', x=.5, y=-.4, b=-1.5, w=.9, l=1, r=1, perch=1, mark='HUP'), k(.82, 'ledge_r', x=.3, y=.5, b=.8, perch=1, eye='>')],
        [], g='play', act=('hop', 'ledge'), when=['glow>.3'], prefer=['young', 'happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.5, {'lure': 1}), (0.72, {'lure': 1})])
    o.r('pace_out_its_length_along_the_ledge', "Measuring by pacing out the serpent's length from the left ledge to the right, a toe-lift for every pace and a loud count at the far end", 30, 'none',
        [k(.04, 'ledge_l', x=.3, y=.4, b=.5, l=1, perch=1, mark='1'), k(.14, 'ledge_l', x=.4, y=.5, b=.6, r=1, perch=1, mark='4'), k(.26, 'lip', x=.4, y=.5, b=.6, l=1, perch=1, mark='9'), k(.4, 'lip', x=.5, y=.6, b=.7, r=1, perch=1, mark='14'), k(.55, 'ledge_r', x=.5, y=.6, b=.7, l=1, perch=1, mark='19'), k(.7, 'ledge_r', x=.4, y=.5, b=.6, r=1, perch=1, eye='O', mark='more!'), k(.88, 'ledge_r', x=.2, y=.2, b=.3, perch=1, eye='-')],
        [], g='test', act=('measure', 'serpent'), prefer=['curious'], pick='hungriest',
        obj=[(0.15, {'lure': 1}), (0.4, {'lure': 1}), (0.65, {'lure': 1})],
        say=['Twenty-three paces and the tail was still unfinished. Legends are poor for stock-taking.', 'A whole wall of serpent. The measure is mostly in the awe.'])
    o.r('count_the_jewel_scales_on_one_flank', 'Counting the jewel scales on one flank with a bill dip each, giving up when the whole flank starts to flicker', 24, 'none',
        [k(.05, 'low_m', x=1, y=1.4, b=.7, mark='1'), k(.16, 'low_m', x=1.1, y=1.5, b=.8, mark='8'), k(.28, 'low_r', x=1.2, y=1.5, b=.9, l=1, mark='15'), k(.4, 'body_r', x=1.3, y=.9, b=.8, mark='26'), k(.54, 'body_m', x=1.3, y=.7, b=.8, r=1, mark='40?'), k(.68, x=-.3, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.86, eye='-')],
        [], g='test', act=('count', 'scales'), prefer=['curious'], pick='shyest',
        obj=[(0.15, {'lure': 1}), (0.5, {'lure': 1}), (0.62, {'lure': 1})])
    o.r('weigh_the_legend_against_the_fact', 'Weighing the legend against the fact with a wing in each hand-spread, one up, one down, and neither quite sure which holds the serpent', 24, 'wing',
        [k(.05, 'low_l', reach=.4, x=.3, y=.6, b=.3), k(.18, 'low_l', reach=1, x=.5, y=.6, b=.4, mark='legend'), k(.34, 'low_m', reach=1, x=.5, y=.8, b=.6, l=1, mark='fact'), k(.5, 'low_m', reach=1, x=.5, y=.5, b=.3, r=1, mark='legend'), k(.68, 'low_r', reach=1, x=.6, y=.8, b=.6, mark='...'), k(.86, eye='-', mark='both')],
        [], g='test', act=('weigh', 'legend'), prefer=['curious', 'grown'], pick='hungriest',
        obj=[(0.25, {'lure': 1}), (0.55, {'lure': 1})])
    o.r('wait_for_the_first_glimmer', 'Waiting stock-still by the wall at dusk for the first glimmer along the dark to wake', 24, 'none',
        [k(.08, 'body_m', x=.9, y=.5, b=.7, eye='o'), k(.3, 'body_m', x=1, y=.6, b=.9, eye='o'), k(.5, 'body_m', x=1, y=1.2, b=.9, l=1), k(.7, 'body_m', x=1.1, y=.7, b=1, eye='O', mark='...'), k(.88, 'body_m', x=.4, y=.3, b=.4, eye='^')],
        [], g='rest', act=('wait', 'glimmer'), prefer=['lonely', 'curious'], pick='shyest',
        obj=[(0.5, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('present_the_serpent_to_the_stars', 'Presenting the serpent to the night sky with a sweeping arc of the wing along the whole wall, an usher for a legend', 22, 'wing',
        [k(.06, 'base_l', reach=.4, x=.1, y=.2), k(.18, 'low_l', reach=.8, x=.3, y=-.1, b=-.2), k(.32, 'body_l', reach=1, x=.3, y=-.4, b=-.4), k(.46, 'body_m', reach=1, x=.5, y=-1, b=-.9, mark='behold'), k(.62, 'body_r', reach=1, x=.4, y=-.5, b=-.4, l=1), k(.78, 'body_r', reach=.6, x=.5, y=0), k(.92, eye='^')],
        [], g='show', act=('present', 'dragon'), prefer=['happy'], pick='shyest',
        obj=[(0.46, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('argue_which_of_them_is_the_older_legend', 'Arguing with the serpent over which of them is the older legend, a wing jab at the glow and a hand-on-chest claim for himself', 22, 'wing',
        [k(.06, 'low_m', reach=.5, x=.6, y=.5, b=.5), k(.2, 'low_m', reach=1, x=1, y=.4, b=.3, mark='OLDER'), k(.36, 'low_m', reach=.4, x=.3, y=.4, b=1.4, l=1, mark='ME'), k(.52, 'low_m', reach=1, x=1.1, y=.3, b=.2, r=1, mark='YOU'), k(.7, 'low_m', reach=.4, x=.3, y=.4, b=1.3, mark='ME'), k(.88, eye='-')],
        [], g='show', act=('argue', 'legend'), prefer=['grumpy'], pick='hungriest',
        obj=[(0.3, {'lure': 1}), (0.7, {'lure': 1})],
        say=['I am the younger legend. By about a thousand years.', 'Lost to a fish with scales like gems. I have feathers.'])
    o.r('pose_in_the_green_light_like_a_statue', 'Striking a pose on the right ledge as a statue in the green light, one wing on his chest and the other pointed at the stars', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.1, w=.3, perch=1), k(.24, 'ledge_r', x=.6, y=-.5, b=-.3, w=.6, perch=1), k(.5, 'ledge_r', x=.8, y=-.8, b=-.5, w=1, perch=1, eye='^', mark='behold'), k(.74, 'ledge_r', x=.3, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'ledge'), prefer=['happy'], pick='shyest',
        obj=[(0.4, {'lure': 1}), (0.8, {'lure': 1})])
    o.r('jump_back_when_the_glow_flares', 'Hopping back with a yelp when the whole serpent flares white right at his bill, the wall lit like a lightning strike', 16, 'none',
        [k(.06, 'body_l', x=1.1, y=.6, b=.7), k(.16, 'body_l', x=1.3, y=.7, b=.9, eye='o', mark='...'), k(.25, x=-1.5, y=-1, b=-1.5, l=1, r=1, w=1, eye='O', mark='BLINK'), k(.42, x=-.9, y=.2, b=-.2, w=.7, eye='>'), k(.6, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'flare'), when=['glow>.4'], prefer=['young', 'curious'], pick='hungriest',
        obj=[(0.16, {'lure': 1}), (0.42, {'lure': 1})],
        say=['White-out. I was a duck in a flashbulb.', 'Eyes are still green. The serpent chuckled, probably.'])
    o.r('hold_the_serpent_between_two_wings', "Standing guard at the left end of the wall while a friend stands at the right, the serpent's whole glowing length stretched between the two of them", 28, 'wing',
        [k(.05, 'low_l', reach=.5, x=.3, y=.7, b=.4), k(.16, 'low_l', reach=1, x=.5, y=.7, b=.5), k(.3, 'mid_l', reach=1, x=.6, y=.4, b=.4, l=1, mark='this end'), k(.48, 'mid_l', reach=1, x=.5, y=.3, b=.3), k(.66, 'low_l', reach=.7, x=.4, y=.5, b=.4, r=1), k(.84, eye='^')],
        [(0.3, 'uncoil')], g='show', act=('guard', 'length'), when=['coil>.4'], prefer=['happy'], pick='hungriest',
        obj=[(0.15, {'lure': 1}), (0.35, {'lure': 1}), (0.6, {'lure': 1}), (0.8, {'lure': 1})],
        say=['Both ends held. The middle is the part no one is holding.', 'Two ducks, one serpent, a strange knot of respect.'],
        duo=[k(.1, 'low_r', x=.4, y=.7, b=.4), k(.26, 'low_r', x=.7, y=.7, b=.5, l=1), k(.44, 'low_r', x=.8, y=.6, b=.4, mark='that end'), k(.64, 'low_r', x=.7, y=.7, b=.5, r=1), k(.84, eye='^')])
    o.r('thread_the_glow_through_a_reed_hoop', 'Lifting a reed bent into a hoop out over the coping so the serpent can thread its glowing length through it in a long lazy S', 28, 'reed',
        [k(.05, 'body_r', reach=.4, x=.2, y=.1), k(.18, 'body_m', reach=1, x=.5, y=-.2, b=-.1), k(.33, 'skin_m', reach=1, x=.6, y=-1.1, b=-.3, w=.2, mark='steady'), k(.5, 'skin_m', reach=1, x=.5, y=-.7, b=-.5, l=1, r=1, eye='O', mark='SWOOSH'), k(.66, 'body_m', reach=.8, x=.3, y=0, b=0, eye='o'), k(.84, eye='^')],
        [(0.5, 'uncoil')], g='play', act=('lift', 'hoop'), prefer=['fish_trust>.4', 'happy'], pick='hungriest',
        obj=[(0.2, {'lure': 1}), (0.4, {'lure': 1}), (0.6, {'lure': 1})],
        say=['Through the ring, all of it, and the ring did not blink.', 'The hoop is now a halo. I decline credit.'])
    o.r('catch_the_rain_on_the_coping', 'Catching rain from the coping on the tip of his bill while the old serpent rises to watch the drops', 22, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'low_l', x=1.3, y=-1.2, b=-.8, eye='o', mark='plip'), k(.5, 'low_l', x=1.1, y=-.9, b=-.4, l=1, eye='O', mark='plip plip'), k(.7, 'low_l', x=.8, y=-.3, b=.2, w=.4, eye='^'), k(.88, eye='-')],
        [(.5, 'cheer')], g='weather', act=('catch', 'drops'), when=['wet'], pick='shyest',
        obj=[(.3, {'lure': 1}), (.6, {'lure': 1}), (.8, {'lure': 0})], say=['The legend watched me drink rain. It was unimpressed.', 'Wet beak, old fish. Each of us has a hobby.'])
    return o

def koi_pond():
    o = Obj('koi_pond', 'placed', 
            parts=dict(shallow='the rippling shallow water along the front rim', pad='the lily pads floating on the water', bloom='the lily bloom on its pad', tuft='the grass tuft at the pond foot', reed='the reed stems at the pond edge', cattail='the cattail stems at the pond edge', bank='the stone bank round the pond', stone='the front rim stones', mud='the muddy edge of the water', edge='the far edge of the water', cove='the sheltered water between the pads'),
            fields={},
            marks=[('pond_leaves', .3, ';"~;"', 'shallow_m', 'leaf'), ('pond_ice', .3, '*-*-*', 'shallow_l', 'frost'), ('pond_algae', .3, '"v"v"', 'stone_m', 'plant'), ('pond_flakes', .3, ".':.'", 'shallow_r', 'dust')],
            effects=dict(
                polish_stones=[['obj.dirt', 'min', 0.1]],
                dry_stones=[['obj.wetness', 'min', 0.15]],
                oxy_blow=[['keeping.oxygen', 'add', 0.3]],
                flakes_tip=[['keeping.flakes', 'add', 0.35]],
                bell_knock=[['keeping.bell', 'add', 0.5]],
                koi_scoop=[['keeping.leaves', 'mul', 0.35]],
                koi_scour=[['keeping.algae', 'mul', 0.5]],
                koi_thin=[['keeping.plants', 'mul', 0.75]],
                koi_crack=[['keeping.ice', 'mul', 0.3]],
                koi_stir=[['keeping.oxygen', 'add', 0.3]],
                koi_scatter=[['keeping.flakes', 'add', 0.5]],
                koi_call=[['keeping.bell', 'add', 0.5]],
                goldfish_tidy=[['keeping.clarity', 'add', 0.15]],
                goldfish_scoop=[['keeping.leaves', 'mul', 0.4]],
                goldfish_thin=[['keeping.plants', 'mul', 0.75]],
                goldfish_crack=[['keeping.ice', 'mul', 0.3]],
                goldfish_stir=[['keeping.oxygen', 'add', 0.3]],
                goldfish_scour=[['keeping.algae', 'mul', 0.5]],
                goldfish_cloud=[['keeping.clarity', 'add', -0.2], ['keeping.flakes', 'add', 0.6]],
            ),
            anchors=dict(
                shallow_l=(0.2353, 0.7818),
                shallow_m=(0.4874, 0.7455),
                shallow_r=(0.7395, 0.7091),
                pad_r=(0.7227, 0.6727),
                bloom_r=(0.6807, 0.6364),
                pad_l=(0.3445, 0.5636),
                tuft=(0.0924, 0.8),
                reed_low=(0.0672, 0.6909),
                cattail_l=(0.0588, 0.5636),
                bank_r=(0.7983, 0.7273, 'surface'),
                stone_l=(0.2521, 0.8364, 'surface'),
                stone_m=(0.3445, 0.8364, 'surface'),
                stone_r=(0.7227, 0.8364, 'surface'),
                mud_edge=(0.4034, 0.7818),
                edge_far=(0.5882, 0.7818),
                cove=(0.3361, 0.7091),
            ))
    o.r('scrub_the_front_stones', 'Scrubbing the green off the front stones with the side of a wing, left stone and then the middle one', 18, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.4), k(.3, 'stone_l', reach=1, x=.5, y=1.2, b=.8, l=1, mark='sqk'), k(.5, 'stone_m', reach=1, x=.5, y=1.3, b=.9, r=1, mark='sqk'), k(.7, 'stone_m', reach=1, x=.4, y=1.2, b=.8), k(.88, eye='^')],
        [(0.5, 'koi_scour')], g='care', act=('scrub', 'stones'), when=['pond_algae>.4'])
    o.r('thin_out_the_lily_pads', 'Thinning the crowded lily pads with a twig, hooking one over and pulling it loose from the bloom', 22, 'twig',
        [k(.12, 'pad_r', reach=.6, x=.3, y=.3), k(.3, 'pad_r', reach=1, x=.6, y=.5, b=.4, mark='hnk'), k(.5, 'bloom_r', reach=1, x=.5, y=.2, b=.6, l=1), k(.7, 'pad_r', reach=1, x=.2, y=-.3, b=-.3, w=.4, mark='pop'), k(.88, eye='-')],
        [(0.5, 'koi_thin')], g='care', act=('pull', 'lily'), when=['pond_plants>.7'])
    o.r('scatter_flakes', 'Throwing a wingful of flakes out across the water so they drift down in a fan', 16, 'wing',
        [k(.15, 'shallow_m', reach=.6, w=.6), k(.35, 'shallow_m', reach=1, b=-.3, w=1, mark='~~~'), k(.6, x=-.3, y=.2, eye='o'), k(.85, eye='^')],
        [(0.35, 'koi_scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.4'], prefer=['dawn', 'dusk'])
    o.r('rap_the_stone_for_dinner', 'Ringing the dinner bell by rapping the middle front stone with his bill in the dinner rhythm until the whole pond hears it', 18, 'none',
        [k(.12, 'stone_m', x=1.3, y=1.4, b=.6, mark='tok'), k(.28, 'stone_m', x=1.3, y=1.4, b=.6, l=1, mark='tok'), k(.44, x=-.3, y=-.2, b=-.2, w=.3), k(.6, 'stone_m', x=1.4, y=1.5, b=.7, r=1, mark='tok tok'), k(.85, eye='^')],
        [(0.6, 'koi_call')], g='use', act=('ring', 'stone'), when=['pond_bell<.4'], prefer=['dusk'])
    o.r('balance_on_the_front_stone_with_wings_out', 'Balancing on the left front stone with both wings out while the koi circles to watch', 22, 'none',
        [k(.12, 'stone_l', perch=1, x=.1, y=.2, b=.3), k(.3, 'stone_l', perch=1, x=.3, y=-.3, b=-.2, w=.8, l=1), k(.5, 'stone_l', perch=1, x=.4, y=-.5, b=-.4, w=1, l=1, eye='O', mark='...'), k(.7, 'stone_l', perch=1, x=.3, y=-.3, b=-.2, w=.8, r=1), k(.88, y=.3, b=.4, eye='^')],
        [], g='play', act=('balance', 'stone'), prefer=['curious', 'grown'])
    o.r('dance_a_shuffle_along_the_stones', 'Dancing a quick shuffle from one front stone to the next, wings flapping in time', 22, 'none',
        [k(.12, 'stone_l', perch=1, x=.2, y=-.2, b=-.5, l=1), k(.3, 'stone_l', perch=1, x=.4, y=-.4, b=-.7, r=1, w=.6, mark='tap'), k(.5, 'stone_m', perch=1, x=.3, y=-.4, b=-.7, l=1, w=.8, mark='tap'), k(.7, 'stone_m', perch=1, x=.4, y=-.4, b=-.7, r=1, w=.6, mark='tap'), k(.88, y=.4, b=.4, eye='^')],
        [], g='play', act=('dance', 'stones'), prefer=['happy', 'young'])
    o.r('sniff_the_pond_water', 'Sniffing the pond water at the right rim, nostrils flaring, trying to name what it smells of', 14, 'none',
        [k(.15, x=.4, y=.7, b=.4), k(.35, 'shallow_r', x=1.1, y=1.3, b=.9, mark='snf'), k(.55, 'shallow_r', x=1.2, y=1.4, b=1, l=1, mark='snf snf'), k(.8, x=-.3, y=-.2, w=.4, eye='O')],
        [], g='test', act=('sniff', 'water'), prefer=['curious'])
    o.r('taste_a_sip_of_the_pond', 'Taking a sip of pond at the left rim and pulling a face at the green taste', 14, 'none',
        [k(.15, x=.4, y=.8, b=.5), k(.35, 'shallow_l', x=1.2, y=1.6, b=1, eye='-', mark='slp'), k(.55, x=-.8, y=-.6, b=-.3, w=.7, l=1, eye='>', mark='bleh'), k(.8, y=.4, b=.3, eye='-')],
        [], g='test', act=('taste', 'water'), prefer=['curious', 'pond_algae>.3'],
        say=['Pond. Regrettable. A little koi, a lot of algae.', 'Tastes like a wet lawn. I am not sure why I did it.'])
    o.r('lay_an_ear_to_the_water_to_listen', "Laying his head sideways at the water to listen for the koi's tiny gulps", 20, 'none',
        [k(.15, x=.4, y=.6, b=.5), k(.4, 'shallow_m', x=.3, y=1.7, b=1.3, eye='-'), k(.62, 'shallow_m', x=.3, y=1.8, b=1.4, l=1, eye='-', mark='...'), k(.85, x=-.5, y=-.5, w=.4, eye='O')],
        [], g='test', act=('listen', 'pond'), prefer=['curious', 'lonely'])
    o.r('count_the_pads_and_the_bloom', 'Counting the lily pads across the water with his bill, the low pad, the bloom, and the high pad', 20, 'none',
        [k(.12, 'pad_r', x=1, y=.1, b=.5, mark='1'), k(.32, 'bloom_r', x=1.2, y=-.4, b=.5, mark='2'), k(.54, 'pad_l', x=1.4, y=-1, b=.2, l=1, mark='3'), k(.78, x=.2, y=-.4, w=.4, eye='-', mark='3 and a flower')],
        [], g='test', act=('count', 'pads'), prefer=['curious'], ages=GROWN)
    o.r('tap_the_ice_to_test_it', 'Testing the skin of ice by tapping it at the rim with a wing tip to find out how thick it is', 16, 'wing',
        [k(.15, 'shallow_m', reach=.5, x=.3, y=.7, b=.4), k(.32, 'shallow_m', reach=1, x=.5, y=1, b=.7, mark='tik'), k(.5, 'shallow_l', reach=1, x=.5, y=1, b=.7, l=1, mark='tik'), k(.7, 'shallow_l', reach=1, x=.4, y=.9, b=.6, mark='tik'), k(.88, eye='-', mark='hm')],
        [], g='test', act=('test', 'ice'), when=['pond_ice>.2'])
    o.r('curl_up_in_the_grass_tuft', 'Curling up against the grass tuft at the pond edge for a nap, with a koi ripple in his ear', 28, 'none',
        [k(.15, x=.4, y=.5, b=.5), k(.4, 'tuft', x=.2, y=1.6, b=1.5, eye='-'), k(.7, 'tuft', x=.2, y=1.9, b=1.8, w=.3, eye='-', mark='zzz'), k(.9, x=-.2, y=-.2, w=.3, eye='O')],
        [], g='rest', act=('nap', 'tuft'), when=['tired'])
    o.r('sit_down_on_the_front_stone_and_watch', 'Sitting down on the bank stones with his feet nearly in the water, watching the koi circle', 26, 'none',
        [k(.15, 'bank_r', perch=1, x=.3, y=.2, b=.8), k(.4, 'bank_r', perch=1, x=.2, y=.5, b=1.4, eye='o'), k(.65, 'bank_r', perch=1, x=.2, y=.4, b=1.5, l=1, eye='o', mark='...'), k(.85, 'bank_r', perch=1, x=.1, y=.2, b=1, eye='-')],
        [], g='rest', act=('sit', 'bank'), prefer=['tired', 'lonely'])
    o.r('lean_against_the_reed_stem', 'Leaning back against the tall cattail stem and sighing at the water', 18, 'none',
        [k(.15, x=.4, y=.2, b=.2, r=1), k(.4, 'cattail_l', x=-.9, y=.5, b=1, w=.4), k(.7, 'cattail_l', x=-1, y=.7, b=1.3, eye='-', mark='sigh', l=1), k(.9, x=.3, y=.2, b=.3)],
        [], g='rest', act=('lean', 'cattail'), prefer=['tired', 'sad'])
    o.r('chip_the_ice_skin_at_the_rim', 'Chipping the skin of ice off the rim with his bill, breaking a gap for the koi to breathe at', 20, 'none',
        [k(.12, x=.4, y=.7, b=.5), k(.3, 'shallow_l', x=1.3, y=1.5, b=1, mark='tak'), k(.5, 'shallow_m', x=1.3, y=1.6, b=1.1, l=1, mark='TAK'), k(.7, 'shallow_m', x=1, y=1.3, b=.9, r=1, mark='crk'), k(.88, eye='^')],
        [(0.5, 'koi_crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'],
        say=['Hole made. Fish can breathe. You are welcome, fish.', 'Ice cracked. Ice complained.'])
    o.r('flap_the_surface_to_stir_the_air_in', 'Splashing the surface with both wings in turn at the rim to churn fresh air down into the water', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.3, y=.7, b=.5), k(.3, 'shallow_m', reach=1, x=.4, y=.9, b=.7, w=1, l=1, mark='SPLAT'), k(.5, 'shallow_r', reach=1, x=.5, y=.9, b=.8, w=1, r=1, mark='SPLAT'), k(.7, 'shallow_m', reach=1, x=.4, y=.9, b=.7, w=1, l=1, mark='splat'), k(.88, eye='^')],
        [(0.5, 'koi_stir')], g='weather', act=('splash', 'surface'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('hunker_in_the_reeds_in_the_rain', 'Sheltering at the low reed stem with his tail to the rain, drops whipping the ripples flat', 32, 'none',
        [k(.12, 'reed_low', x=-.5, y=.9, b=1.3, l=1), k(.3, 'reed_low', x=-1.2, y=1.8, b=2.1, w=.2, eye='-'), k(.58, 'reed_low', x=-1.3, y=2, b=2.4, r=1, eye='-', mark='drip'), k(.82, 'reed_low', x=-.6, y=1.1, b=1.6, eye='>')],
        [], g='weather', act=('shelter', 'reeds'), when=['wet'])
    o.r('bask_on_the_warm_front_stone', 'Basking on the warm middle stone with his wings half open and his eyes shut', 26, 'none',
        [k(.15, 'stone_m', perch=1, x=-.2, y=-.3, b=.6), k(.45, 'stone_m', perch=1, x=-.4, y=-.8, b=1.2, w=.5, eye='-'), k(.7, 'stone_m', perch=1, x=-.5, y=-1, b=1.4, w=.8, eye='-', mark='mm'), k(.9, 'stone_m', perch=1, y=.2, b=.4, eye='^')],
        [], g='weather', act=('warm', 'stones'), when=['sun'], prefer=['tired'])
    o.r('scrape_the_frost_off_the_stones', 'Scraping the frost off the front stones with the edge of a wing before the koi rise', 18, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.5), k(.3, 'stone_l', reach=1, x=.5, y=1.2, b=.9, mark='skrt'), k(.5, 'stone_m', reach=1, x=.5, y=1.3, b=1, l=1, mark='skrt'), k(.7, 'stone_r', reach=1, x=.4, y=1.2, b=.9, r=1, mark='skrt'), k(.88, eye='-')],
        [(0.5, 'koi_crack')], g='weather', act=('scrape', 'frost'), when=['pond_ice>.2'])
    o.r('strike_a_pose_on_the_middle_stone', 'Striking a pose on the right front stone with one wing out over the water, a statue by the pond', 20, 'none',
        [k(.12, 'stone_r', perch=1, x=.2, y=-.3, b=-.2, w=.3), k(.38, 'stone_r', perch=1, x=.5, y=-1, b=.4, w=1, l=1), k(.65, 'stone_r', perch=1, x=.5, y=-1.3, b=.6, w=.6, r=1, mark='...'), k(.88, y=.3, b=.3, eye='^')],
        [], g='show', act=('pose', 'stone'), prefer=['happy'])
    o.r('shout_across_the_pond_at_the_cattails', 'Shouting across the pond at the far cattails, wings cupped round his bill, to hear it echo', 14, 'wing',
        [k(.15, x=.6, y=-.2, b=.5), k(.35, reach=1, x=1.5, y=-1.8, b=-1, w=.7, mark='HOOOY'), k(.6, reach=.6, x=1.4, y=-1.9, b=-.9, r=1, w=.5, mark='HOOOY'), k(.85, x=-.4, y=.4, b=.5, eye='-')],
        [], g='show', act=('shout', 'cattails'), prefer=['happy', 'young'], far=True)
    o.r('skid_off_the_wet_stone', 'Slipping off the wet front stone and ending flat on his belly at the rim, bill almost in the water', 16, 'none',
        [k(.15, 'stone_l', x=.4, y=.3, b=.4, l=1), k(.3, x=.6, y=-.4, b=-.8, w=1, l=1, r=1, eye='O', mark='WAH'), k(.5, 'shallow_l', x=1.3, y=1.9, b=1.7, w=.8, eye='@', mark='splat'), k(.8, x=.2, y=.6, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'stones'), when=['wet'], prefer=['young'])
    o.r('back_into_the_reeds_in_the_dark', 'Walking backwards, bumping a reed stem at night while watching the water and bouncing off with a squeak', 14, 'none',
        [k(.15, x=-.4, y=.8, b=.7, r=1), k(.3, 'mud_edge', x=-1.4, y=.6, b=1.3, eye='O', mark='oof'), k(.5, x=1, y=-.8, b=-1, w=.9, l=1, eye='@'), k(.8, x=.3, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'reeds'), when=['night'])
    o.r('sweep_the_leaves_in_from_both_banks', 'Making a rake of both wings to bring the floating leaves in from both banks with a friend until they meet in a heap at the middle', 24, 'wing',
        [k(.12, 'shallow_l', reach=.6, x=.3, y=.7, b=.4), k(.3, 'shallow_l', reach=1, x=.5, y=.9, b=.7, mark='swsh'), k(.5, 'shallow_m', reach=1, x=.6, y=1, b=.8, l=1, mark='swsh'), k(.7, 'shallow_m', reach=1, x=.5, y=.9, b=.7, r=1), k(.88, eye='^')],
        [(0.5, 'koi_scoop')], g='care', act=('rake', 'surface'), prefer=['pond_leaves>.3', 'happy'],
        duo=[k(.12, 'shallow_r', reach=.6, x=.3, y=.7, b=.4), k(.3, 'shallow_r', reach=1, x=.5, y=.9, b=.7, mark='swsh'), k(.5, 'shallow_m', reach=1, x=.6, y=1, b=.8, r=1, mark='swsh'), k(.7, 'shallow_m', reach=1, x=.5, y=.9, b=.7, l=1), k(.88, eye='^')])
    o.r('pour_flakes_while_a_friend_scatters', 'Pouring a thin line of flakes from his bill while a friend scatters wings of them from the far rim', 22, 'none',
        [k(.12, x=.5, y=.7, b=.5), k(.3, 'shallow_l', x=1.2, y=1.5, b=1, mark='...'), k(.5, 'shallow_l', x=1.3, y=1.6, b=1.1, l=1, mark='tssss'), k(.7, 'shallow_l', x=.8, y=1, b=.6, w=.4, eye='O'), k(.88, eye='^')],
        [(0.5, 'koi_scatter')], g='use', act=('pour', 'flakes'), when=['pond_flakes<.4'], prefer=['happy'],
        duo=[k(.12, 'shallow_r', reach=.6, w=.5), k(.34, 'shallow_r', reach=1, b=-.3, w=1, mark='~~~'), k(.6, x=-.3, y=.2, eye='o'), k(.82, eye='^')])
    o.r('nudge_a_cattail_head_to_make_it_nod', 'Nudging the nearest cattail head with a twig until the whole stem nods back and forth', 18, 'twig',
        [k(.12, 'cattail_l', reach=.6, x=.3, y=-.5, b=-.2), k(.3, 'cattail_l', reach=1, x=.6, y=-.9, b=.3, mark='bop'), k(.5, 'cattail_l', reach=1, x=.6, y=-.9, b=.4, l=1, mark='bop'), k(.7, x=-.3, y=-.5, w=.4, eye='O', mark='nod'), k(.88, eye='^')],
        [], g='play', act=('nudge', 'cattail'), prefer=['young', 'happy'], ages=GROWN)
    o.r('lean_on_the_right_bank_stones', 'Leaning his shoulder against the right bank stones and watching the koi pass below', 22, 'none',
        [k(.15, x=.3, y=.2, b=.3, r=1), k(.4, 'stone_r', x=-.9, y=.5, b=1, w=.4, eye='o'), k(.7, 'bank_r', x=-1, y=1.2, b=1.3, eye='-', mark='...', l=1), k(.9, x=.2, y=.2, b=.3)],
        [], g='rest', act=('lean', 'bank'), prefer=['tired', 'lonely'])
    o.r('fish_a_leaf_out_by_its_stem', 'Pulling a floating leaf out by its stem with the tip of his bill and flicking it onto the bank', 18, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_l', x=1.3, y=1.5, b=1, mark='snk'), k(.5, 'shallow_l', x=.3, y=.3, b=-.3, w=.4, l=1, mark='fwip'), k(.72, 'tuft', x=.6, y=.8, b=.4, eye='^'), k(.9, eye='-')],
        [(0.5, 'goldfish_scoop')], g='care', act=('pull', 'leaf'), prefer=['pond_leaves>.3', 'curious'],
        say=['One leaf. Out. The pond acts like it never happened.', 'Bill-fishing. Catch of the day: foliage.'])
    o.r('brush_the_grit_off_the_stones', 'Sweeping the grit off the front stones in short strokes so none of it washes back into the water', 20, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.5), k(.3, 'stone_l', reach=1, x=.4, y=1.1, b=.8, l=1, mark='shk'), k(.5, 'stone_m', reach=1, x=.5, y=1.2, b=.9, mark='shk'), k(.7, 'stone_r', reach=1, x=.4, y=1.1, b=.8, r=1), k(.88, eye='^')],
        [(0.5, 'goldfish_tidy')], g='care', act=('sweep', 'grit'), when=['pond_clarity<.6'])
    o.r('uproot_a_clump_of_weed', 'Digging up a clump of weed at the shallow end with a long steady pull of his bill', 22, 'none',
        [k(.12, x=.5, y=.7, b=.5), k(.3, 'shallow_r', x=1.2, y=1.6, b=1.1, mark='hnn'), k(.5, 'shallow_r', x=.8, y=1.8, b=1.5, l=1, mark='HNNG'), k(.7, 'shallow_r', x=-.5, y=.4, b=-.3, w=.8, r=1, mark='plop'), k(.88, y=.5, eye='^')],
        [(0.5, 'goldfish_thin')], g='care', act=('dig', 'weeds'), when=['pond_plants>.7'])
    o.r('kick_the_ice_loose_at_the_edge', 'Kicking the ice loose at the edge with the flat of a foot, one hard stab at a time, until a gap opens', 20, 'none',
        [k(.12, x=.2, y=.2, b=.5, l=1), k(.3, 'stone_l', x=.3, y=.5, b=-.3, l=1, mark='crk'), k(.48, 'stone_m', x=.3, y=.5, b=-.4, r=1, mark='CRK'), k(.66, 'stone_m', x=.4, y=.6, b=-.2, l=1, mark='crunch'), k(.86, eye='^')],
        [(0.48, 'goldfish_crack')], g='weather', act=('kick', 'ice'), when=['pond_ice>.3'])
    o.r('wipe_the_slime_off_the_reed_foot', 'Taking a wipe at the green slime off the foot of the reeds with the back of a wing, stem after stem', 18, 'wing',
        [k(.12, 'reed_low', reach=.6, x=.2, y=.5, b=.4), k(.3, 'reed_low', reach=1, x=.3, y=.7, b=.7, mark='sqk'), k(.5, 'tuft', reach=1, x=.4, y=.9, b=.9, l=1, mark='sqk'), k(.7, 'reed_low', reach=1, x=.3, y=.7, b=.7, r=1), k(.88, eye='-')],
        [(0.5, 'goldfish_scour')], g='care', act=('wipe', 'reeds'), when=['pond_algae>.4'])
    o.r('shake_a_wing_in_long_strokes_over_the_water', 'Shaking a wing in long slow strokes over the water to stir some air into the shallows', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.2, y=.4, b=.3), k(.3, 'shallow_m', reach=1, x=.3, y=.3, b=-.4, w=.8, mark='fff'), k(.5, 'shallow_r', reach=1, x=.4, y=.3, b=-.5, w=1, r=1, mark='FFF'), k(.7, 'shallow_l', reach=1, x=.3, y=.3, b=-.4, w=.8, l=1, mark='fff'), k(.88, eye='-')],
        [(0.5, 'goldfish_stir')], g='weather', act=('shake', 'wings'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('tip_the_whole_pile_in_at_once', 'Tipping the whole pile of flakes in at once and watching the water cloud up as the goldfish goes mad', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.3, y=.4, b=.4), k(.3, 'shallow_m', reach=1, x=.4, y=.7, b=.8, w=1, mark='FOOMF'), k(.5, x=-.7, y=-.4, b=-.6, w=.8, eye='O', mark='oops'), k(.7, 'shallow_r', reach=.5, x=.3, y=.8, b=.6, l=1, eye='>'), k(.88, eye='-')],
        [(0.3, 'goldfish_cloud')], g='mishap', act=('tip', 'pile'), prefer=['young', 'grumpy'],
        say=['Too many. Pond now looks like soup. Fish: delighted.', 'I meant to pour less. I meant a lot of things.'])
    o.r('foot_stuck_in_the_tuft', 'Tugging a foot out of a gap between the rim stones after it jammed there, hopping round in a circle', 22, 'none',
        [k(.15, 'tuft', x=-.4, y=.4, b=.4), k(.32, 'stone_m', x=-.6, y=.7, b=.8, l=1, eye='O', mark='huh'), k(.5, 'stone_m', x=-.9, y=1, b=1.3, l=1, r=1, w=.6, eye='@', mark='mrf'), k(.7, 'stone_m', x=-.4, y=.4, b=-.6, w=1, mark='PTHWOP'), k(.88, y=.6, b=.5, eye='-')],
        [], g='mishap', act=('tug', 'foot'), prefer=['grumpy', 'young'])
    o.r('knock_three_slow_on_the_right_stone', 'Knocking three slow beats on the right front stone with his bill, the pond\'s own dinner bell', 18, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'stone_r', x=1.2, y=1.3, b=.6, mark='tok'), k(.5, 'stone_r', x=1.3, y=1.5, b=.8, l=1, mark='tok'), k(.7, 'stone_r', x=1.4, y=1.5, b=.9, r=1, mark='TOK'), k(.9, eye='^')],
        [(.7, 'bell_knock')], g='use', act=('knock', 'stone'), when=['pond_bell<.4'], say=['Three knocks. Dinner. The water has no idea.', 'Rang it myself. Self-service dinner.'])
    o.r('tip_a_trickle_of_flakes_from_his_bill', 'Tipping a thin trickle of flakes from his bill along the shallows so they spread evenly', 20, 'none',
        [k(.12, x=.4, y=.7, b=.5), k(.3, 'shallow_l', x=1.2, y=1.5, b=1), k(.5, 'shallow_m', x=1.3, y=1.6, b=1.1, l=1, mark='tss'), k(.7, 'shallow_r', x=1.2, y=1.5, b=1, r=1, mark='tss'), k(.88, eye='^')],
        [(.5, 'flakes_tip')], g='use', act=('tip', 'flakes'), when=['pond_flakes<.4'])
    o.r('blow_a_long_breath_across_the_ripples', 'Blowing a long breath low across the shallows to wake the sleepy water at the rim', 18, 'none',
        [k(.12, x=.3, y=.6, b=.5), k(.3, 'shallow_r', x=1.3, y=1.7, b=1.2, eye='-'), k(.55, 'shallow_r', x=1.4, y=1.9, b=1.4, eye='-', mark='fffff'), k(.8, x=-.2, y=-.4, w=.4, eye='O'), k(.9, eye='^')],
        [(.55, 'oxy_blow')], g='use', act=('blow', 'ripples'), when=['pond_oxygen<.5'], say=['Pond resuscitation. Mouth to surface.', 'Huffed at the water until it perked up.'])
    o.r('hide_low_in_the_reed_foot_and_pop_out', 'Hide-and-seek low in the reed foot, counting to three, then popping out with a shout', 20, 'none',
        [k(.12, 'reed_low', x=.5, y=1.2, b=1.4, eye='-'), k(.3, 'cattail_l', x=.4, y=1.6, b=1.8, eye='o'), k(.5, x=1.4, y=-.6, b=-.8, w=.8, eye='O', mark='BOO'), k(.72, x=.6, y=.3, b=.3, eye='^'), k(.9, eye='-')],
        [], g='play', act=('hide', 'reed'), prefer=['young', 'curious'])
    o.r('race_the_rim_from_end_to_end', 'Having a race along the front rim stones from the left end to the right, against his own shadow', 20, 'none',
        [k(.08, 'mud_edge', x=.6, y=.5, b=.6, l=1), k(.28, 'edge_far', x=1.2, y=.4, b=-.5, r=1, w=.5), k(.5, 'cove', x=1.3, y=.4, b=-.7, l=1, w=.7, mark='zoom'), k(.7, 'cove', x=.6, y=.5, b=.6, eye='O', mark='whew'), k(.9, eye='^')],
        [], g='play', act=('race', 'rim'), prefer=['happy', 'young'])
    o.r('kick_the_shallows_into_rings', 'Kicking the shallows with alternate feet at the rim to send rings out to the pads', 18, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'shallow_l', x=.8, y=.9, b=.9, l=1, mark='plsh'), k(.5, 'mud_edge', x=.8, y=.9, b=.9, r=1, mark='plsh'), k(.7, 'shallow_l', x=.8, y=.9, b=.9, l=1, mark='plsh'), k(.88, eye='^')],
        [], g='play', act=('kick', 'ripples'), prefer=['young', 'happy'])
    o.r('sing_a_slow_song_to_the_cattails', 'Singing a slow song to the cattails across the water with a wing over his heart', 24, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, 'cattail_l', reach=1, x=.3, y=-.8, b=.2, w=.4, mark='laaa'), k(.5, 'cattail_l', reach=1, x=.4, y=-.9, b=.3, w=.5, l=1, mark='LAAA'), k(.7, 'cattail_l', reach=1, x=.3, y=-.7, b=.2, r=1, mark='la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'cattail'), ages=GROWN, prefer=['happy', 'lonely'])
    o.r('show_off_a_rim_walk_with_wings_out', 'Showing off a slow tightrope walk along the rim stones, wings out and chin high', 22, 'none',
        [k(.1, 'stone_l', perch=1, x=.2, y=-.3, b=-.2, w=.6), k(.3, 'stone_m', perch=1, x=.3, y=-.5, b=-.4, w=1, l=1), k(.55, 'stone_r', perch=1, x=.3, y=-.6, b=-.5, w=1, r=1, mark='ta-da'), k(.8, 'stone_r', perch=1, x=.2, y=.2, b=.2, w=.4, eye='^')],
        [], g='show', act=('show', 'rim'), prefer=['happy'])
    o.r('hop_back_from_the_cold_shock_of_a_splash', 'Hopping back from the rim with a squeak as the water slaps up cold at his chest', 14, 'none',
        [k(.15, 'edge_far', x=.8, y=.9, b=.6), k(.3, 'edge_far', x=.2, y=-.8, b=-1.3, w=1, eye='O', mark='YEEP'), k(.5, x=-1, y=-.8, b=-1.4, w=1, l=1, r=1, eye='@'), k(.72, x=-.4, y=.9, b=1, w=.4, eye='>', mark='brr'), k(.9, eye='-')],
        [], g='mishap', act=('hop', 'chest'), prefer=['young', 'curious'])
    o.r('drying_the_rim_stones_with_a_wing', 'Drying the soaked front stones with long wing strokes so nobody skids on them', 20, 'wing',
        [k(.12, 'stone_l', reach=.5, x=.3, y=.9, b=.5), k(.3, 'stone_l', reach=1, x=.5, y=1.2, b=.9, mark='fwp'), k(.5, 'stone_m', reach=1, x=.5, y=2.5, b=1, l=1, mark='fwp'), k(.7, 'stone_r', reach=1, x=.4, y=1.2, b=.9, r=1), k(.88, eye='^')],
        [(.5, 'dry_stones')], g='care', act=('dry', 'stones'), when=['obj_wetness>.3'])
    o.r('polishing_the_rim_stones_with_a_wing', 'Polishing the dull front stones with the back of a wing until they gleam', 22, 'wing',
        [k(.12, 'stone_r', reach=.5, x=.3, y=.9, b=.5), k(.3, 'stone_r', reach=1, x=.5, y=1.3, b=1, mark='sqk'), k(.5, 'stone_m', reach=1, x=.5, y=1.4, b=1.1, r=1, mark='sqk'), k(.7, 'stone_l', reach=1, x=.4, y=1.3, b=1, l=1, mark='sqk'), k(.88, eye='^')],
        [(.5, 'polish_stones')], g='care', act=('polish', 'stones'), when=['obj_dirt>.3'])
    o.r('catch_snowflakes_on_his_bill_at_the_rim', 'Catching snowflakes on his bill at the rim while the ripples go quiet', 20, 'none',
        [k(.12, x=.3, y=.4, b=.4), k(.3, 'cove', x=1, y=-.9, b=-.4, eye='o', mark='ahh'), k(.5, 'cove', x=1.1, y=-1, b=-.5, l=1, eye='O'), k(.7, 'cove', x=.8, y=-.3, b=.2, w=.4, eye='^'), k(.88, eye='-')],
        [], g='weather', act=('catch', 'snowflakes'), when=['snow'])
    o.r('tap_the_bank_stones_for_a_loose_one', 'Tapping the bank stones one after the other with his bill to find which one rocks', 20, 'none',
        [k(.12, 'stone_m', x=.8, y=1, b=.6, mark='tk'), k(.3, 'bank_r', x=1.1, y=.5, b=.5, mark='tk'), k(.5, 'stone_m', x=1.1, y=1.2, b=.8, l=1, mark='tk'), k(.7, 'bank_r', x=1.2, y=.5, b=.6, r=1, mark='tok'), k(.88, eye='-')],
        [], g='test', act=('tap', 'bank'), prefer=['curious'])
    return o

def infinity_pool():
    o = Obj('infinity_pool', 'placed', 
            parts=dict(base='the foot of the tank wall', low='the lower glass of the tank', high='the upper glass of the tank', skin='the water line under the coping', coping='the coping along the top of the tank', ledge='the stone ledge in front of the tank', pier='the stone pier at the end of the tank', lip='the front lip of the pool', puff='the tank glass at beak height', bob='the tank glass at eye height', top='the top run of water in the tank', sign='the SEA TANK sign on the glass', mid='the middle glass of the tank', body='the tank glass along the fish'),
            fields={},
            marks=[('pond_leaves', .3, ';"~;"', 'skin_m', 'leaf'), ('pond_ice', .3, '*-*-*', 'high_l', 'frost'), ('pond_algae', .3, '"v"v"', 'base_l', 'plant'), ('pond_flakes', .3, ".':.'", 'skin_l', 'dust')],
            effects=dict(
                tin_spill=[['keeping.flakes', 'add', 0.5]],
                sturgeon_scrub=[['keeping.algae', 'mul', 0.5]],
                sturgeon_rake=[['keeping.leaves', 'mul', 0.35]],
                sturgeon_sweep=[['keeping.clarity', 'add', 0.12]],
                sturgeon_polish=[['keeping.clarity', 'add', 0.15]],
                sturgeon_call=[['keeping.bell', 'add', 0.5]],
                sturgeon_sink=[['keeping.flakes', 'add', 0.35]],
                sturgeon_crack=[['keeping.ice', 'mul', 0.3]],
                sturgeon_thaw=[['keeping.ice', 'mul', 0.6]],
                pufferfish_call=[['keeping.bell', 'add', 0.5]],
                pufferfish_crack=[['keeping.ice', 'mul', 0.3]],
                pufferfish_thaw=[['keeping.ice', 'mul', 0.6]],
                swordfish_scrub=[['keeping.algae', 'mul', 0.5]],
                swordfish_polish=[['keeping.clarity', 'add', 0.15]],
                swordfish_foam=[['keeping.flakes', 'mul', 0.3]],
                swordfish_call=[['keeping.bell', 'add', 0.5]],
                swordfish_scatter=[['keeping.flakes', 'add', 0.4]],
                swordfish_thaw=[['keeping.ice', 'mul', 0.6]],
                ancient_dragon_fish_call=[['keeping.bell', 'add', 0.5]],
                ancient_dragon_fish_thaw=[['keeping.ice', 'mul', 0.6]],
            ),
            anchors=dict(
                base_l=(0.1951, 0.7797),
                base_m=(0.5041, 0.7797),
                base_r=(0.7642, 0.7797),
                low_l=(0.2927, 0.7288),
                low_r=(0.6992, 0.7288),
                high_l=(0.2276, 0.678),
                high_m=(0.5041, 0.678),
                skin_l=(0.2764, 0.5763),
                skin_m=(0.5528, 0.5763),
                coping=(0.3252, 0.4746),
                ledge_l=(0.2439, 0.8305, 'surface'),
                ledge_m=(0.5041, 0.8305, 'surface'),
                ledge_r=(0.748, 0.8305, 'surface'),
                pier_l=(0.0813, 0.6949),
                pier_r=(0.8943, 0.6949),
                lip=(0.4878, 0.8814, 'surface'),
                puff_r=(0.6504, 0.7288),
                bob_l=(0.1626, 0.7288),
                bob_m=(0.4715, 0.7288),
                bob_r=(0.7967, 0.7288),
                top_l=(0.2439, 0.6271),
                top_m=(0.4715, 0.6271),
                sign=(0.1951, 0.5593),
                top_r=(0.7154, 0.6271),
                skin_r=(0.6179, 0.5763),
                mid_l=(0.1951, 0.678),
                body_r=(0.748, 0.6271),
            ))
    o.r('wipe_the_green_off_the_wall_foot', 'Taking a wipe at the green film off the foot of the tank wall in long flat strokes from the left corner to the right', 24, 'wing',
        [k(.06, 'base_l', reach=.4, x=.2, y=.9, b=.4), k(.17, 'base_l', reach=1, x=.5, y=1.5, b=1, mark='wsh'), k(.3, 'base_m', reach=1, x=.8, y=1.7, b=1.2, l=1, mark='wsh'), k(.45, 'base_m', reach=1, x=1, y=1.6, b=1.1), k(.6, 'base_r', reach=1, x=1.2, y=1.7, b=1.3, r=1, mark='wsh'), k(.78, 'base_r', reach=.5, x=.5, y=.7, b=.4), k(.92, eye='^')],
        [(0.45, 'sturgeon_scrub')], g='care', act=('wipe', 'film'), when=['pond_setup>.5', 'pond_algae>.4'],
        say=['The wall is clear. The sturgeon will never know. Neither will the algae.', 'Wiped it spotless. Spotless water, spotted duck.'])
    o.r('rake_the_leaves_off_the_top_with_a_reed', 'Using a reed as a rake on the leaves off the top of the tank with a reed held over the coping, drawing them to the left corner', 26, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.3, y=-.1), k(.2, 'coping', reach=1, x=.5, y=-.3, b=-.2, mark='rk'), k(.34, 'skin_m', reach=1, x=.6, y=-.2, b=-.1, l=1, mark='rk'), k(.5, 'skin_l', reach=1, x=.7, y=-.1, b=.1, r=1, mark='rk'), k(.66, 'skin_l', reach=.7, x=.3, y=0, b=-.2), k(.84, eye='-')],
        [(0.5, 'sturgeon_rake')], g='care', act=('rake', 'leaves'), when=['pond_setup>.5', 'pond_leaves>.3'], prefer=['windy'])
    o.r('sweep_the_silt_cloud_off_the_view', 'Sweeping a wing over the wall to follow and thin the brown cloud the sturgeon keeps rooting up along the floor', 22, 'wing',
        [k(.07, 'base_r', reach=.4, x=.3, y=.7, b=.3), k(.2, 'base_r', reach=1, x=.7, y=1.1, b=.7, mark='shh'), k(.35, 'low_r', reach=1, x=.8, y=1.3, b=.9, l=1, mark='shh'), k(.5, 'base_m', reach=1, x=.9, y=1.4, b=1, r=1), k(.68, 'low_l', reach=1, x=.8, y=1.2, b=.8, mark='shh'), k(.88, eye='-')],
        [(0.5, 'sturgeon_sweep')], g='care', act=('sweep', 'silt'), when=['pond_setup>.5'], prefer=['night'])
    o.r('polish_the_wall_with_a_wing_corner', 'Polishing the wall with the tip of a wing in small circles until the cloudy patch at eye height clears', 22, 'wing',
        [k(.08, 'high_l', reach=.5, x=.2, y=.3, b=.2), k(.22, 'high_l', reach=1, x=.5, y=.4, b=.4, mark='sqk'), k(.36, 'high_m', reach=1, x=.6, y=.5, b=.5, l=1, mark='sqk'), k(.5, 'high_m', reach=1, x=.5, y=.4, b=.4, r=1, mark='sqk'), k(.66, 'low_r', reach=1, x=.6, y=.8, b=.7), k(.84, eye='^')],
        [(0.5, 'sturgeon_polish')], g='care', act=('polish', 'wall'), when=['pond_setup>.5', 'pond_clarity<.6'])
    o.r('knock_three_slow_at_the_wall_foot', 'Knocking three slow beats at the foot of the wall with his bill, the night bell the old fish has always known', 18, 'none',
        [k(.07, 'base_l', x=1.3, y=1.5, b=.8, mark='tok'), k(.2, 'base_l', x=1.5, y=1.7, b=1, mark='tok'), k(.34, x=.1, y=.2, b=.1, w=.3), k(.5, 'base_l', x=1.5, y=1.7, b=1.1, l=1, mark='TOK'), k(.7, x=.4, y=.5, b=.4, eye='^')],
        [(0.5, 'sturgeon_call')], g='use', act=('knock', 'wall'), when=['pond_setup>.5', 'pond_bell<.4'], prefer=['night', 'dusk'])
    o.r('lob_pellets_up_and_over_the_coping', 'Throwing a wingful of sinking pellets up and over the coping so they patter down to the floor', 20, 'wing',
        [k(.08, 'skin_l', reach=.3, x=.1, y=.1), k(.22, 'skin_l', reach=.9, x=.4, y=-.2, b=.5), k(.38, 'skin_l', reach=1, x=.5, y=-.9, b=-.9, w=.2, mark='fwup'), k(.54, x=-.3, y=.1, b=-.2, eye='o'), k(.72, x=.1, y=.3, b=.2, eye='^')],
        [(0.38, 'sturgeon_sink')], g='use', act=('throw', 'pellets'), when=['pond_setup>.5'], prefer=['night', 'dusk'],
        say=['Lobbed. Patter, patter, silence. Dinner is served in the dark.', 'Pellets down the well. The old fish will find them.'])
    o.r('tap_the_ledge_for_the_floor_to_hum', 'Tapping a slow toe on the front ledge so the floor hums and the sturgeon turns toward the sound', 20, 'none',
        [k(.06, 'ledge_l', x=.3, y=.6, b=.8, l=1, perch=1), k(.2, 'ledge_l', x=.4, y=.9, b=1.2, r=1, mark='tmp', perch=1), k(.36, 'ledge_l', x=.3, y=.8, b=1.1, l=1, mark='tmp', perch=1), k(.52, 'ledge_l', x=.4, y=.9, b=1.2, r=1, mark='TMP', perch=1), k(.7, 'ledge_l', x=.3, y=.5, b=.5, perch=1), k(.88, eye='^')],
        [(0.52, 'sturgeon_call')], g='use', act=('tap', 'ledge'), when=['pond_setup>.5', 'pond_bell<.4'], prefer=['night'])
    o.r('waltz_the_ledge_at_its_pace', "Dancing a waltz very slowly along the front ledge, one step to each sweep of the old fish's tail", 26, 'none',
        [k(.05, 'ledge_l', x=.2, y=.2, b=.3, perch=1), k(.18, 'ledge_l', x=.5, y=.1, b=-.4, w=.5, l=1, perch=1), k(.32, 'ledge_m', x=.3, y=.4, b=.6, w=.2, perch=1), k(.46, 'ledge_m', x=.5, y=0, b=-.5, w=.6, r=1, perch=1), k(.62, 'ledge_r', x=.3, y=.5, b=.7, perch=1), k(.8, 'ledge_r', x=.4, y=0, b=-.3, w=.4, perch=1, eye='^')],
        [], g='play', act=('dance', 'ledge'), when=['pond_setup>.5', 'night'], prefer=['happy', 'lonely'])
    o.r('lay_an_ear_to_the_ledge_for_the_floor', "Listening with his head sideways on the front ledge for the slow drag of the old fish's belly along the floor", 24, 'none',
        [k(.06, 'lip', x=.1, y=.7, b=.8, perch=1), k(.22, 'lip', x=-.8, y=1.5, b=1.5, eye='-', perch=1), k(.44, 'lip', x=-1, y=1.9, b=1.9, eye='-', mark='...', perch=1), k(.66, 'lip', x=-.9, y=1.7, b=1.7, eye='o', mark='shhk', perch=1), k(.84, 'lip', x=.2, y=.6, b=.5, perch=1, eye='^')],
        [], g='test', act=('listen', 'floor'), when=['pond_setup>.5'], prefer=['curious', 'night'])
    o.r('sniff_the_brine_at_the_wall_seam', 'Sniffing the brine along the seam where the wall meets the floor, then sneezing at the salt', 18, 'none',
        [k(.07, 'base_l', x=.5, y=1.2, b=.6), k(.2, 'base_l', x=1.4, y=2, b=1, mark='snf'), k(.38, 'base_m', x=1.6, y=2.2, b=1.2, eye='-', mark='snf'), k(.56, x=-1.1, y=-.7, b=-.4, w=.7, eye='>', mark='ACHOO'), k(.76, x=.1, y=.3, b=.2, eye='-')],
        [], g='test', act=('sniff', 'brine'), when=['pond_setup>.5'], prefer=['curious', 'young'])
    o.r('doze_off_on_the_middle_ledge', 'Taking a nap on the middle ledge with his bill on his chest while the old fish makes its rounds', 28, 'none',
        [k(.08, 'ledge_m', x=.2, y=.9, b=.9, eye='-', perch=1), k(.28, 'ledge_m', x=-.5, y=1.6, b=1.6, eye='-', perch=1), k(.52, 'ledge_m', x=-.8, y=2, b=2.2, eye='-', mark='zzz', perch=1), k(.76, 'ledge_m', x=-.2, y=.8, b=.8, eye='o', perch=1), k(.9, eye='^')],
        [], g='rest', act=('nap', 'ledge'), when=['pond_setup>.5', 'tired'], prefer=['night'])
    o.r('sit_at_the_lip_in_the_late_dark', 'Sitting at the left end of the ledge with his feet tucked, watching the slow shadow turn at the end of the wall', 26, 'none',
        [k(.08, 'ledge_l', x=.2, y=.5, b=.7), k(.3, 'ledge_l', x=-.2, y=.9, b=1.4, eye='-'), k(.55, 'ledge_l', x=-.4, y=1.1, b=1.8, eye='o'), k(.78, 'ledge_l', x=.4, y=.4, b=.6, l=1, eye='^')],
        [], g='rest', act=('sit', 'ledge_l'), when=['pond_setup>.5'], prefer=['tired', 'lonely'])
    o.r('lean_on_the_left_pier_post', 'Leaning his shoulder against the left pier post while the old fish does the rounds', 22, 'none',
        [k(.07, 'pier_l', x=-.4, y=.3, b=.5), k(.24, 'pier_l', x=-.8, y=.6, b=.9, eye='-'), k(.46, 'pier_l', x=-1, y=.8, b=1.2, eye='-', mark='...'), k(.66, 'pier_l', x=-.7, y=.6, b=.8, r=1), k(.84, x=.4, y=.2, b=.2, eye='O')],
        [], g='rest', act=('lean', 'post'), when=['pond_setup>.5'], prefer=['tired', 'sad'])
    o.r('chip_the_frost_from_the_wall_foot', "Chipping the frost from the foot of the wall with his bill so the sturgeon's long night is clearly seen", 22, 'none',
        [k(.06, 'ledge_l', x=.6, y=.9, b=.4, perch=1), k(.18, 'base_l', x=1.5, y=2, b=.8, mark='tk'), k(.32, 'base_l', x=1.7, y=2.3, b=1.1, r=1, mark='TK'), k(.46, 'base_m', x=1.6, y=2.2, b=1, l=1, mark='crk'), k(.62, 'low_l', x=1.5, y=1.8, b=.9, r=1, mark='CRK'), k(.8, x=.4, y=.3, eye='^')],
        [(0.46, 'sturgeon_crack')], g='weather', act=('chip', 'frost'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('scrape_the_hoar_from_the_pier_post', 'Scraping the hoar off the right pier post with a wing so he can lean against it without his feathers sticking', 20, 'wing',
        [k(.08, 'pier_r', reach=.5, x=.3, y=.4, b=.2), k(.24, 'pier_r', reach=1, x=.6, y=.8, b=.5, mark='skrr'), k(.4, 'pier_r', reach=1, x=.7, y=.9, b=.6, l=1, mark='skrr'), k(.58, 'pier_r', reach=1, x=.5, y=.7, b=.5, r=1), k(.76, 'low_r', reach=.6, x=.4, y=.5, b=.3), k(.9, eye='-')],
        [(0.4, 'sturgeon_thaw')], g='weather', act=('scrape', 'hoar'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('shelter_by_the_post_from_the_rain', 'Sheltering at the right pier post with his bill tucked while the rain pocks the tank and the sturgeon swims on through it', 30, 'none',
        [k(.08, 'pier_r', x=-.5, y=.7, b=.8), k(.28, 'pier_r', x=-1, y=1.6, b=1.5, eye='-'), k(.52, 'pier_r', x=-1.2, y=2, b=1.9, eye='-', mark='pit'), k(.76, 'pier_r', x=-1.1, y=1.9, b=1.7, l=1, mark='pat'), k(.9, x=.2, y=.2, eye='^')],
        [], g='weather', act=('shelter', 'post'), when=['pond_setup>.5', 'wet'])
    o.r('warm_each_foot_on_the_sunny_ledge', 'Warming one foot and then the other on the sun-baked right ledge while the old fish sleeps below', 20, 'none',
        [k(.08, 'ledge_r', x=.3, y=.4, b=.7, l=1, perch=1), k(.3, 'ledge_r', x=.2, y=.7, b=1, l=1, eye='-', perch=1), k(.54, 'ledge_r', x=.2, y=.7, b=1, r=1, eye='-', mark='ahh', perch=1), k(.76, 'ledge_r', x=.4, y=.3, b=.4, w=.3, perch=1, eye='^')],
        [], g='rest', act=('warm', 'foot'), when=['pond_setup>.5', 'sun'], prefer=['tired'])
    o.r('brace_at_the_pier_in_the_gust', 'Bracing his chest into the gust at the right pier so the leaves skid past the tank without dropping in', 18, 'none',
        [k(.06, 'low_r', x=1, y=.1, b=1), k(.2, 'pier_r', x=1.5, y=.4, b=1.5, w=.5, mark='whoo'), k(.38, 'pier_r', x=1.7, y=.5, b=1.7, l=1, w=.9), k(.56, 'pier_r', x=1.5, y=.3, b=1.3, r=1, w=.7), k(.76, 'pier_r', x=.8, y=.2, b=.7), k(.9, eye='-')],
        [], g='weather', act=('brace', 'gust'), when=['pond_setup>.5', 'windy'])
    o.r('cool_his_bill_at_the_wall_on_a_hot_noon', 'Cooling his bill against the wall on a hot noon, then his cheek, then the other cheek, while the deep one stays down', 20, 'none',
        [k(.07, 'high_l', x=.9, y=.6, b=.5), k(.22, 'high_l', x=1.3, y=.9, b=.8, eye='-', mark='ahh'), k(.4, 'high_l', x=1.1, y=1, b=.9, eye='-', l=1), k(.6, 'high_m', x=1.3, y=.9, b=.8, eye='-', r=1), k(.8, x=.4, y=.3, eye='^')],
        [], g='rest', act=('cool', 'bill'), when=['pond_setup>.5', 'warm'], prefer=['summer'])
    o.r('slip_on_the_wet_ledge', 'Slipping on the rain-wet ledge, feet skating out in both directions, and slapping the wall to stop', 16, 'none',
        [k(.07, 'ledge_r', x=.6, y=.6, b=.5, perch=1), k(.2, 'ledge_r', x=1.3, y=-.3, b=-.8, l=1, r=1, w=1, mark='whoa!', perch=1), k(.34, 'low_r', x=1.7, y=1.3, b=1.8, w=.7, eye='O', mark='SLAP'), k(.52, 'ledge_r', x=.7, y=.8, b=.9, perch=1, eye='>'), k(.7, x=.2, y=.2, b=.2, eye='-')],
        [], g='mishap', act=('slip', 'ledge'), when=['pond_setup>.5', 'wet'], prefer=['young'])
    o.r('head_stuck_between_two_pier_rungs', 'Getting his head stuck between two rungs of the left pier and having to wriggle out', 24, 'none',
        [k(.06, x=.9, y=.5, b=.5), k(.2, 'low_l', x=1.9, y=.1, b=1, eye='O'), k(.38, 'pier_l', x=2.1, y=.2, b=1.3, l=1, eye='@', mark='mmph'), k(.56, 'pier_l', x=2, y=.3, b=1.2, r=1, w=.5, mark='mf'), k(.7, 'pier_l', x=1.5, y=-.4, b=-.8, w=1, mark='POP'), k(.86, x=1.1, y=1, b=.7, eye='-')],
        [], g='mishap', act=('stuck', 'rungs'), prefer=['young', 'grumpy'])
    o.r('knock_two_light_on_the_wall', 'Knocking two light taps on the wall with a wing knuckle, the soft bell it only half minds', 16, 'wing',
        [k(.08, 'low_l', reach=.4, x=.2, y=.7, b=.4), k(.2, 'low_l', reach=1, x=.4, y=.9, b=.6, mark='tk'), k(.32, 'low_l', reach=.4, x=.1, y=.6, b=.3), k(.46, 'low_l', reach=1, x=.4, y=.9, b=.6, l=1, mark='tk'), k(.64, eye='^')],
        [(0.46, 'pufferfish_call')], g='use', act=('knock', 'glass'), when=['pond_setup>.5', 'pond_bell<.4'], prefer=['dusk', 'dawn'])
    o.r('tap_the_sign_to_see_who_looks', 'Testing the sign letters by tapping them with a wingtip, one letter at a time, to see whether the puffer looks up to read them', 20, 'wing',
        [k(.06, 'top_l', reach=.5, x=.2, y=-.1, b=.1), k(.2, 'sign', reach=1, x=.4, y=-.5, b=-.2, mark='S'), k(.34, 'sign', reach=1, x=.5, y=-.5, b=-.3, l=1, mark='E'), k(.48, 'sign', reach=1, x=.6, y=-.6, b=-.3, mark='A'), k(.64, 'top_l', reach=.6, x=.3, y=-.1, eye='o'), k(.82, eye='-')],
        [], g='test', act=('test', 'letters'), when=['pond_setup>.5'], prefer=['curious', 'young'])
    o.r('prod_the_ice_skin_at_the_top', 'Prodding the thin skin of ice at the top of the tank with a reed held out over the coping until it cracks', 24, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.2, y=-.2), k(.2, 'coping', reach=1, x=.5, y=-.3, b=-.1, mark='tk'), k(.34, 'top_m', reach=1, x=.6, y=-.3, b=0, l=1, mark='TK'), k(.5, 'top_m', reach=1, x=.7, y=-.2, b=.1, r=1, mark='CRK'), k(.68, 'top_l', reach=.7, x=.3, y=-.1, b=-.1), k(.86, eye='^')],
        [(0.5, 'pufferfish_crack')], g='weather', act=('prod', 'ice'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('sweep_the_frost_flower_off_the_wall', 'Sweeping the frost flowers off the wall in wide wing arcs so the puffer is not looking out at white', 20, 'wing',
        [k(.08, 'low_l', reach=.5, x=.3, y=.7, b=.3), k(.22, 'bob_l', reach=1, x=.6, y=.8, b=.6, mark='shff'), k(.38, 'bob_m', reach=1, x=.8, y=.8, b=.7, l=1, mark='shff'), k(.54, 'bob_r', reach=1, x=1, y=.8, b=.8, r=1, mark='shff'), k(.7, 'puff_r', reach=.7, x=.7, y=.6, b=.5), k(.88, eye='-')],
        [(0.38, 'pufferfish_thaw')], g='care', act=('sweep', 'frost'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('balance_on_the_ledge_in_the_gust', 'Balancing on the ledge in the gust, wings out like a tightrope walker, rocking with every puff', 20, 'none',
        [k(.06, 'ledge_m', x=.4, y=.2, b=.5, perch=1), k(.2, 'ledge_r', x=.7, y=0, b=.9, w=.6, l=1, perch=1), k(.36, 'ledge_r', x=.3, y=.2, b=.4, w=.9, r=1, perch=1, mark='whoo'), k(.52, 'ledge_r', x=.8, y=-.1, b=1, w=.7, l=1, perch=1), k(.68, 'ledge_r', x=.4, y=.2, b=.5, w=.5, r=1, perch=1), k(.86, 'ledge_r', x=.2, y=.1, b=.3, perch=1, eye='^')],
        [], g='weather', act=('balance', 'ledge'), when=['windy'])
    o.r('bump_the_wall_chasing_a_spine_glint', 'Walking along the tank watching only the water and bumping the glass with a clunk', 18, 'none',
        [k(.07, 'low_l', x=.8, y=.5, b=.3), k(.22, 'bob_l', x=.9, y=.6, b=.4, l=1), k(.36, 'bob_m', x=1, y=.5, b=.3, r=1), k(.48, 'bob_r', x=2.1, y=.1, b=1.6, eye='@', mark='CLUNK'), k(.64, 'bob_r', x=-1.3, y=.4, b=.1, w=.9, eye='x'), k(.84, y=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'wall'), when=['pond_setup>.5'], prefer=['curious'])
    o.r('wipe_the_high_wall_clear_of_green', 'Taking a wipe at the green off the upper wall with long upward swipes of a wing so the top run is clear to watch', 22, 'wing',
        [k(.05, 'base_l', reach=.4, x=.2, y=.6, b=.3), k(.15, 'low_l', reach=1, x=.4, y=.5, b=.4, mark='whp'), k(.27, 'top_l', reach=1, x=.5, y=.2, b=.2, l=1, mark='whp'), k(.4, 'top_m', reach=1, x=.6, y=0, b=0, mark='whp'), k(.54, 'top_r', reach=1, x=.7, y=.1, b=.1, r=1, mark='whp'), k(.7, 'low_r', reach=.8, x=.5, y=.4, b=.3), k(.9, eye='^')],
        [(0.4, 'swordfish_scrub')], g='care', act=('wipe', 'wall'), when=['pond_setup>.5', 'pond_algae>.4'],
        say=['Green gone. It sped past to inspect the work.', 'Scrubbed the top run. The sword saw itself and showed off.'])
    o.r('polish_a_clean_pane_for_the_sword', 'Polishing a clean pane at the top of the wall in tight circles so the sword and the long eye can be seen properly', 22, 'wing',
        [k(.07, 'top_l', reach=.5, x=.3, y=.2, b=.2), k(.19, 'top_l', reach=1, x=.5, y=.3, b=.4, mark='sqk'), k(.32, 'top_m', reach=1, x=.6, y=.2, b=.3, l=1, mark='sqk'), k(.46, 'top_m', reach=1, x=.5, y=.3, b=.4, r=1, mark='sqk'), k(.6, 'top_r', reach=1, x=.7, y=.4, b=.4, mark='sqk'), k(.8, eye='o', mark='clear')],
        [(0.46, 'swordfish_polish')], g='care', act=('polish', 'pane'), when=['pond_setup>.5', 'pond_clarity<.6'])
    o.r('brush_the_foam_skin_off_the_water_line', 'Sweeping the thick foam skin off the water line with a wing so the top run is not a swamp of bubbles', 18, 'wing',
        [k(.06, 'skin_r', reach=.4, x=.1, y=0), k(.19, 'skin_r', reach=1, x=.4, y=-.2, b=.2, mark='shh'), k(.33, 'skin_l', reach=1, x=.6, y=-.1, b=.3, l=1, mark='shh'), k(.5, 'skin_l', reach=1, x=.7, y=-.1, b=.2, r=1), k(.68, 'skin_r', reach=.6, x=.3, y=0, b=.1), k(.86, eye='-')],
        [(0.33, 'swordfish_foam')], g='care', act=('sweep', 'foam'), when=['pond_setup>.5', 'pond_flakes>.3'])
    o.r('rap_the_sign_with_a_wing_edge', 'Knocking the sign with the edge of a wing three times, the loud bell the sword has learned to answer', 16, 'wing',
        [k(.06, 'top_l', reach=.4, x=.2, y=-.1), k(.17, 'sign', reach=1, x=.5, y=-.6, b=-.3, mark='tok'), k(.28, 'sign', reach=.5, x=.2, y=-.2, b=0), k(.4, 'sign', reach=1, x=.6, y=-.7, b=-.3, l=1, mark='tok'), k(.52, 'sign', reach=.5, x=.2, y=-.2, b=0), k(.64, 'sign', reach=1, x=.7, y=-.8, b=-.4, r=1, mark='TOK'), k(.84, eye='^')],
        [(0.64, 'swordfish_call')], g='use', act=('knock', 'sign'), when=['pond_setup>.5', 'pond_bell<.4'], prefer=['dawn', 'dusk'])
    o.r('flip_a_wingful_of_flakes_across_the_top', 'Throwing a wingful of flakes across the top of the tank so they skitter on the water and the sword comes slashing', 18, 'wing',
        [k(.08, 'skin_m', reach=.3, x=.1, y=0), k(.2, 'skin_m', reach=.9, x=.3, y=-.3, b=.5), k(.34, 'skin_m', reach=1, x=.5, y=-.9, b=-.8, mark='fwip'), k(.5, x=-.3, y=0, b=-.2, eye='o'), k(.7, eye='^')],
        [(0.34, 'swordfish_scatter')], g='use', act=('throw', 'flakes'), when=['pond_setup>.5', 'pond_flakes<.3'], prefer=['dawn', 'dusk'],
        say=['Flakes across the top. Streak, slash, gone.', 'It hit the water so hard I got wet from the wall.'])
    o.r('scrape_the_rime_off_the_flank_wall', 'Scraping the rime off the lower wall with the side of a wing in flat downward strokes', 18, 'wing',
        [k(.07, 'low_l', reach=.5, x=.3, y=.6, b=.3), k(.21, 'low_l', reach=1, x=.6, y=1, b=.8, mark='skrr'), k(.36, 'base_l', reach=1, x=.7, y=1.2, b=1, l=1, mark='skrr'), k(.52, 'base_l', reach=1, x=.8, y=1.3, b=1.1, r=1), k(.7, 'low_r', reach=.6, x=.4, y=.7, b=.4), k(.88, eye='-')],
        [(0.36, 'swordfish_thaw')], g='care', act=('scrape', 'rime'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('spread_a_wing_to_dry_in_the_sun', 'Spreading one wing wide at the left ledge to dry in the sun after a splash and then the other', 20, 'none',
        [k(.08, 'lip', x=.3, y=.4, b=.6, perch=1), k(.26, 'ledge_l', x=.2, y=.5, b=.9, w=.8, l=1, eye='-', perch=1), k(.5, 'ledge_l', x=.2, y=.5, b=.9, w=1, eye='-', mark='ahh', perch=1), k(.72, 'ledge_l', x=.3, y=.4, b=.6, w=.5, r=1, perch=1), k(.9, eye='^')],
        [], g='weather', act=('dry', 'wings'), when=['sun'], prefer=['happy'])
    o.r('tap_the_pier_post_for_a_slow_gong', 'Tapping the left pier post slowly with his bill, a gong beat that carries along the dark and brings the serpent unwinding', 20, 'none',
        [k(.06, 'pier_l', x=1.2, y=.6, b=.6, mark='dong'), k(.19, 'pier_l', x=1.3, y=.7, b=.7), k(.31, x=.1, y=.1, w=.3), k(.45, 'pier_l', x=1.4, y=.8, b=.8, l=1, mark='DONG'), k(.62, x=.3, y=.4, b=.3, eye='^'), k(.84, eye='-')],
        [(0.45, 'ancient_dragon_fish_call')], g='use', act=('tap', 'pier'), when=['pond_setup>.5', 'pond_bell<.4'], prefer=['night', 'dusk'])
    o.r('read_the_sign_by_its_light', "Testing the tank sign by the serpent's glow alone, going close and then far to find where the letters fade", 22, 'wing',
        [k(.05, 'mid_l', reach=.4, x=.3, y=.4, b=.3), k(.18, 'sign', reach=1, x=.5, y=-.5, b=-.2, mark='S'), k(.32, 'mid_l', reach=.5, x=.2, y=.6, b=.5, eye='o', mark='far'), k(.46, 'sign', reach=1, x=.6, y=-.5, b=-.3, l=1, mark='E'), k(.62, 'low_l', reach=.5, x=.2, y=.7, b=.6, eye='-', mark='fainter'), k(.8, eye='^')],
        [], g='test', act=('test', 'light'), when=['pond_setup>.5'], prefer=['curious'])
    o.r('wipe_the_frost_flowers_off_the_lens', 'Taking a wipe at the frost flowers off the clear lens in the wall with a quick wing so the light can come through', 18, 'wing',
        [k(.08, 'mid_l', reach=.5, x=.3, y=.3, b=.3), k(.22, 'mid_l', reach=1, x=.5, y=.2, b=.5, mark='shff'), k(.38, 'top_l', reach=1, x=.6, y=.2, b=.4, l=1, mark='shff'), k(.54, 'body_r', reach=1, x=.9, y=.1, b=.3, r=1), k(.72, 'low_r', reach=.6, x=.6, y=.8, b=.5), k(.88, eye='-')],
        [(0.38, 'ancient_dragon_fish_thaw')], g='weather', act=('wipe', 'frost'), when=['pond_setup>.5', 'pond_ice>.3'])
    o.r('sing_a_slow_shanty_to_the_glass', 'Singing a slow shanty to the glass with a wing held up, as if the tank were a crowd', 24, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, 'bob_m', reach=1, x=.3, y=.6, b=.4, w=.4, mark='laaa'), k(.5, 'bob_m', reach=1, x=.4, y=.7, b=.5, w=.5, l=1, mark='LAAA'), k(.7, 'bob_m', reach=1, x=.3, y=.6, b=.4, r=1, mark='la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'glass'), when=['pond_setup>.5'], prefer=['happy', 'lonely'], say=['The tank clapped. Slowly. Wetly.', 'A shanty for the glass. It did not request one.'])
    o.r('shout_a_depth_sounding_down_the_tank', 'Shouting a depth sounding down the length of the tank, a wing cupped at his bill, then waiting for it to come back', 16, 'wing',
        [k(.15, x=.6, y=-.2, b=.5), k(.35, reach=1, x=1.5, y=-1.8, b=-1, w=.7, mark='FIVE FATHOMS'), k(.6, reach=.6, x=1.4, y=-2.8, b=-.9, r=1, w=.5, mark='...'), k(.85, x=-.4, y=.4, b=.5, eye='-')],
        [], g='show', far=True, act=('shout', 'depth'), when=['pond_setup>.5'], prefer=['happy', 'young'])
    o.r('show_the_empty_yard_a_wing_flourish', 'Showing the empty yard a wing flourish over the top of the tank, headline act of the whole property', 16, 'wing',
        [k(.15, reach=.3, x=-.6, y=.3, b=.6, r=1), k(.38, 'top_m', reach=1, x=.9, y=-.2, w=.8, b=-.3), k(.62, 'top_m', reach=1, x=1.1, y=-.4, w=.5, b=-.6, l=1, mark='ta-da'), k(.85, reach=0, y=.6, b=.5, eye='^')],
        [], g='show', act=('show', 'tank'), when=['pond_setup>.5'], prefer=['happy'])
    o.r('drum_a_march_on_the_ledge', 'Drumming a marching beat on the front ledge with both feet, left foot, right foot, left', 18, 'none',
        [k(.12, 'ledge_l', perch=1, x=.2, y=.2, b=-.5, l=1), k(.3, 'ledge_l', perch=1, x=.3, y=.3, b=-.7, r=1, mark='thud'), k(.5, 'ledge_m', perch=1, x=.3, y=.3, b=-.6, l=1, mark='thud'), k(.7, 'ledge_l', perch=1, x=.3, y=.3, b=-.7, r=1, mark='THUD'), k(.88, 'ledge_l', perch=1, y=.2, b=.2, eye='^')],
        [], g='show', act=('drum', 'ledge'), prefer=['happy', 'young'])
    o.r('have_a_race_along_the_ledge', 'Having a race along the front ledge from the left end to the right, against his own reflection', 20, 'none',
        [k(.08, 'ledge_l', x=.6, y=.5, b=.6, l=1), k(.28, 'lip', x=1.2, y=.4, b=-.5, r=1, w=.5), k(.5, 'ledge_r', x=1.3, y=1.3, b=-.7, l=1, w=.7, mark='zoom'), k(.7, 'ledge_r', x=.6, y=.5, b=.6, eye='O', mark='whew'), k(.9, eye='^')],
        [], g='play', act=('race', 'ledge'), prefer=['happy', 'young'])
    o.r('blow_bubbles_at_the_glass_to_watch_them_rise', 'Blowing bubbles at the glass at eye level and watching them climb the wall of the tank', 20, 'none',
        [k(.12, x=.3, y=.6, b=.5), k(.3, 'bob_l', x=1.2, y=.8, b=.9, mark='blub'), k(.5, 'bob_l', x=1.3, y=.9, b=1, l=1, mark='blub blub'), k(.7, 'bob_l', x=1.1, y=.8, b=.9, eye='O'), k(.88, eye='^')],
        [], g='play', act=('blow', 'bubbles'), when=['pond_setup>.5'], prefer=['young', 'happy'])
    o.r('chase_his_reflection_across_the_top_run', 'Chasing his own reflection across the top run of the tank with a wing, left to right and back', 22, 'wing',
        [k(.1, 'top_l', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'top_m', reach=1, x=.5, y=-.4, b=.3, l=1), k(.5, 'top_r', reach=1, x=.6, y=-.4, b=.4, r=1), k(.7, 'top_m', reach=1, x=.5, y=-.4, b=.3, l=1), k(.88, eye='^')],
        [], g='play', act=('chase', 'reflection'), when=['pond_setup>.5'], prefer=['curious', 'young'])
    o.r('measure_the_water_depth_with_a_reed', 'Measuring the water depth against the glass with a reed, then against his own leg, then giving up', 22, 'reed',
        [k(.12, 'coping', reach=.5, x=.3, y=.4, b=.3), k(.32, 'low_l', reach=1, x=.5, y=.9, b=.7, mark='1'), k(.55, 'base_l', reach=1, x=.6, y=1.1, b=.9, l=1, mark='2'), k(.78, 'coping', reach=.6, x=.2, y=.2, eye='-', mark='deep'), k(.9, eye='-')],
        [], g='test', act=('measure', 'depth'), when=['pond_setup>.5'], prefer=['curious'])
    o.r('hop_back_from_a_slap_of_spray', 'Hopping back from the wall with a yell as the water slaps up and over the coping into his face', 14, 'none',
        [k(.15, 'low_r', x=.8, y=.9, b=.6), k(.3, 'low_r', x=.2, y=-.8, b=-1.3, w=1, eye='O', mark='AH'), k(.5, x=-1, y=-1.7, b=-1.4, w=1, l=1, r=1, eye='@'), k(.72, x=-.4, y=.9, b=1, w=.4, eye='>', mark='brr'), k(.9, eye='-')],
        [], g='mishap', act=('hop', 'spray'), when=['pond_setup>.5'], prefer=['young', 'curious'])
    o.r('tug_a_bill_free_of_the_pier_rungs', 'Tugging his bill free of the pier rungs after leaning in too far to see the water, with a pop', 20, 'none',
        [k(.15, 'base_r', x=.6, y=.7, b=.5), k(.35, 'pier_r', x=1.2, y=.9, b=.9, eye='O', mark='mf'), k(.55, 'pier_r', x=1.4, y=1, b=1.1, l=1, w=.5, mark='mmf'), k(.72, 'pier_r', x=-.8, y=.4, b=1.2, r=1, w=1, mark='POP'), k(.88, x=-.4, y=.5, b=.5, eye='>')],
        [], g='mishap', act=('tug', 'bill'), prefer=['young', 'grumpy'])
    o.r('tip_the_whole_tin_of_flakes_in_at_once', 'Tipping the whole tin of flakes over the coping at once and watching them sink in a mass', 18, 'wing',
        [k(.15, 'skin_r', reach=.5, x=.3, y=.4, b=.4), k(.35, 'skin_r', reach=1, x=.5, y=.6, b=.7, w=.7, mark='plop'), k(.55, 'skin_r', reach=1, x=.5, y=.8, b=.9, w=1, l=1, mark='PLOP'), k(.78, 'skin_r', reach=.5, x=.2, y=.4, eye='O'), k(.9, eye='-')],
        [(.55, 'tin_spill')], g='mishap', act=('tip', 'tin'), when=['pond_setup>.5'], prefer=['curious', 'young'])
    return o


FISH = [koi, goldfish, catfish, bass, carp, ghost_fish, golden_koi, minnow, salmon, trout, sturgeon, pufferfish, swordfish, ancient_dragon_fish]

HOSTS = [koi_pond, infinity_pool]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in FISH + HOSTS:
        if only and fn.__name__ not in only:
            continue
        o = done(fn())
        try:
            o.emit()
        except AssertionError as e:
            if not os.environ.get('LENIENT'):
                raise
            print('EMIT', str(e)[:300])
