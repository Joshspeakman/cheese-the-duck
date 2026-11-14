"""Wave 3b: scarf_red and scarf_winter (worn), ancient_amulet and lucky_charm (shown in the trophy case), koi and goldfish (kept in the koi pond).
Every routine is hand-written. Worn things touch named places on his own body (rep.BODY_SPOTS); shown things touch the case and the thing itself ('item');
kept fish touch the pond rim and water. Anchors of the drawn hosts are (column, row) of rep.py <host> converted by P()."""
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
COUNT_NEED = {}
DIM = dict(trophy_case=(106, 77), koi_pond=(120, 55))


def pm(host):
    w, rows = DIM[host]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


def scarf_red():
    # Worn: red rib scarf. Drawing: a round wrap with a ribbed band (rows of `v`), a knot under the neck, two hanging tails of ribbing, the left one
    # longer, both ending in `: | | :` fringe. Anchors are places on his own body: knot = throat, wraps = neck/nape/shoulder, tail uppers = chest,
    # fringe ends = belly. Nothing about the scarf is drawn off his body unless an act takes it off (off / hold / ix).
    o = Obj('scarf_red', 'wearable',
            fields=dict(knot=(.8, 0, 1), neat=(.7, 0, 1), soaked=(0, 0, 1), snow=(0, 0, 1), frayed=(0, 0, 1), soiled=(0, 0, 1)),
            physics=[('knot', 'rate', -.0006, 'windy'), ('neat', 'rate', -.0005, 'windy'), ('soaked', 'rate', .002, 'wet'), ('soaked', 'rate', -.001, 'dry&warm'),
                     ('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm'), ('frayed', 'rate', .0004, 'always'), ('soiled', 'rate', .0004, 'always')],
            effects=dict(snug=[('knot', 'set', 1)], slack=[('knot', 'set', .1)], neaten=[('neat', 'set', 1)], ruffle=[('neat', 'add', -.4)],
                         wring=[('soaked', 'mul', .2)], flick=[('snow', 'set', 0)], snip=[('frayed', 'set', 0)], scrub=[('soiled', 'mul', .2)],
                         cosy=[('need.energy', 'add', 2)], fun=[('need.fun', 'add', 2)]),
            anchors=dict(crown=0, throat=0, neck=0, nape=0, shoulder=0, back=0, belly=0, bill=0, foot_l=0, foot_r=0, thigh=0, rump=0))
    # ---------------- care
    o.r('tug_the_knot_snug', 'Hauling the slipped knot back up snug under his chin with the flat of a wing', 14, 'wing',
        [k(.12, 'throat', reach=.5, x=-.3, y=.3, b=.2), k(.3, 'throat', reach=1, x=-.6, y=.6, b=.5, mark='hff'), k(.5, 'throat', reach=1, x=-.2, y=.9, b=.4, l=1), k(.75, 'neck', reach=.6, x=-.1, y=.3, w=.3), k(.9, eye='^')],
        [(.5, 'snug')], g='care', act=('tug', 'knot'), when=['knot<.5'], prefer=['grown'], obj=[(.3, dict(wy=.3)), (.55, dict(wy=0))],
        say=["Snug. Slightly throttled, mostly fine.", "Knot back up. Dignity pending."])
    o.r('smooth_the_ribbing', 'Smoothing the ribbing flat down the long tail with a wing, chest to fringe', 18, 'wing',
        [k(.12, 'throat', reach=.5, x=.2, y=.4), k(.3, 'throat', reach=1, x=.5, y=.9, b=.4), k(.5, 'belly', reach=1, x=.5, y=1.2, b=.7, l=1), k(.7, 'belly', reach=1, x=.4, y=1.3, b=.8), k(.88, y=.1, w=.4, eye='^')],
        [(.5, 'neaten')], g='care', act=('straighten', 'ribs'), when=['neat<.5'], prefer=['curious'], obj=[(.3, dict(wx=.2)), (.6, dict(wx=0))])
    o.r('comb_the_fringe', 'Combing the fringe straight with his bill, one end and then the other', 16, 'none',
        [k(.12, 'belly', x=1, y=1.5, b=.7, mark='nib'), k(.3, 'belly', x=.8, y=1.4, b=.9, l=1), k(.55, 'foot_r', x=1, y=1.5, b=.7, r=1, mark='nib'), k(.75, 'foot_r', x=.8, y=1.4, b=.9), k(.9, y=.2, eye='^')],
        [(.55, 'neaten')], g='care', act=('groom', 'fringe'), when=['neat<.6'], prefer=['happy'])
    o.r('nip_off_a_loose_thread', 'Nipping a loose thread off the ribbing and pulling it clean away', 14, 'none',
        [k(.15, 'throat', x=.8, y=1.2, b=.4), k(.35, 'throat', x=1.3, y=1.6, b=.7, mark='nnk'), k(.55, 'throat', x=-.6, y=-.4, b=-.3, w=.4, l=1, eye='O'), k(.78, y=.4, eye='-')],
        [(.35, 'snip')], g='care', act=('pull', 'thread'), when=['frayed>.35'], obj=[(.35, dict(wy=.2)), (.6, dict(wy=0))])
    o.r('scrub_the_wraps_clean', 'Scrubbing the grubby wraps round the neck with the side of a wing', 18, 'wing',
        [k(.12, 'neck', reach=.5, x=-.3, y=.6, b=.3), k(.3, 'neck', reach=1, x=-.5, y=.8, b=.5, l=1), k(.5, 'shoulder', reach=1, x=-.5, y=.8, b=.5, mark='sqk'), k(.7, 'nape', reach=1, x=-.7, y=.7, b=.5, r=1), k(.88, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'wraps'), when=['soiled>.3'], obj=[(.3, dict(wx=-.2)), (.6, dict(wx=0))], say=["Scrubbed a scarf while wearing it. Gymnastic.", "Red again. The grime can sue."])
    o.r('lay_it_out_to_dry', 'Slipping the soaked scarf off, shaking it out and laying it flat beside him until it stops dripping', 28, 'none',
        [k(.1, 'neck', x=1, y=.9, b=.5), k(.22, 'neck', x=1.2, y=.6, b=.7, mark='hup'), k(.36, 'neck', x=.6, y=.5, b=.3), k(.5, 'belly', x=.5, y=1.2, b=.7), k(.65, 'belly', x=.4, y=1.3, b=.8, eye='-'), k(.78, 'neck', x=1.1, y=.9, b=.6), k(.9, 'neck', x=.3, y=.4, b=.2, eye='^')],
        [(.65, 'wring')], g='care', act=('dry', 'scarf'), when=['soaked>.3'],
        obj=[(.22, dict(off=1, hold=1)), (.4, dict(off=1, ix=2)), (.7, dict(off=1, ix=2)), (.8, dict(off=1, hold=1)), (.88, dict(off=0))],
        say=["Spread out like a duck at a spa. Wool, I mean.", "Drip all you like. I'm not wearing a swamp."])
    o.r('fold_it_and_set_it_down', 'Taking the scarf off, folding it in three with bill and wing, and wearing it again after', 26, 'wing',
        [k(.1, 'neck', reach=.4, x=.8, y=.9, b=.4), k(.24, 'neck', reach=1, x=1, y=.6, b=.7, mark='hup'), k(.4, 'throat', reach=1, x=.5, y=1.2, b=.9, l=1), k(.55, 'throat', reach=1, x=.5, y=1.3, b=1, r=1), k(.7, 'belly', reach=1, x=.5, y=1.2, b=.9), k(.84, 'neck', reach=1, x=.9, y=.8, b=.6), k(.94, eye='^')],
        [(.55, 'neaten')], g='care', act=('fold', 'scarf'), when=['neat<.4'], obj=[(.24, dict(off=1, hold=1)), (.4, dict(off=1, ix=1)), (.62, dict(off=1, ix=1)), (.72, dict(off=1, hold=1)), (.86, dict(off=0))])
    # ---------------- use
    o.r('wrap_an_extra_turn', 'Hooking the long tail round the neck for another turn and tucking the end in', 18, 'wing',
        [k(.1, 'throat', reach=.5, x=-.2, y=.5, b=.3), k(.28, 'throat', reach=1, x=-.4, y=.8, b=.6), k(.46, 'nape', reach=1, x=-.8, y=.5, b=.6, l=1), k(.64, 'neck', reach=1, x=-.6, y=.8, b=.7, r=1), k(.82, 'throat', reach=.6, x=-.2, y=.5, b=.4), k(.92, eye='^')],
        [(.82, 'cosy')], g='use', act=('wrap', 'neck'), when=['cold'], obj=[(.3, dict(wx=.2)), (.5, dict(wx=-.2)), (.7, dict(wx=0))],
        say=["Third lap round the neck. Sheep did the work, I take the credit.", "Wrapped like a parcel. Return to sender, no."])
    o.r('hunch_it_up_over_the_bill', 'Hunching the scarf up over his bill until only his eyes show', 20, 'none',
        [k(.12, x=-.3, y=.4, b=.3), k(.3, 'neck', x=-1.6, y=2.4, b=1.8, eye='-'), k(.55, 'neck', x=-1.9, y=2.8, b=2.2, eye='-', mark='mmf'), k(.8, 'neck', x=.2, y=.3, b=.3, eye='O')],
        [(.55, 'cosy')], g='use', act=('hide', 'bill'), when=['cold'], obj=[(.3, dict(wy=-.4)), (.6, dict(wy=-.5)), (.85, dict(wy=0))])
    o.r('carry_it_off_in_his_bill', 'Pulling the scarf off, carrying it a few steps by one end and putting it back on', 24, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.22, 'neck', x=1.3, y=1.2, b=.7, mark='hup'), k(.38, x=.4, y=-.3, b=-.3, l=1), k(.52, x=.3, y=-.2, r=1), k(.68, 'neck', x=1.2, y=1, b=.6), k(.8, 'neck', x=.3, y=.4, b=.3, eye='^')],
        [], g='use', act=('carry', 'scarf'), prefer=['grown'],
        obj=[(.22, dict(off=1, hold=1)), (.4, dict(off=1, hold=1)), (.55, dict(off=1, hold=1)), (.7, dict(off=1, hold=1)), (.82, dict(off=0))])
    o.r('slacken_the_knot_to_cool_off', 'Working the knot loose and letting both tails hang slack to cool his throat', 16, 'none',
        [k(.12, x=.2, y=.9, b=.3), k(.3, 'throat', x=.9, y=1.5, b=.7, mark='nnf'), k(.5, 'throat', x=.5, y=1, b=.8, l=1), k(.7, 'neck', x=.2, y=.6, b=.3, eye='-', mark='ahh'), k(.88, y=-.2, w=.3, eye='^')],
        [(.5, 'slack')], g='use', act=('unwrap', 'knot'), when=['knot>.6', 'warm'], prefer=['sad'], obj=[(.3, dict(sag=.4)), (.6, dict(sag=.7))])
    o.r('flip_a_tail_over_the_shoulder', 'Flicking the long tail up and over his shoulder with a quick wing', 14, 'wing',
        [k(.12, 'belly', reach=.5, x=.2, y=.4, b=.2), k(.3, 'throat', reach=1, x=-.4, y=-.4, b=-.5, w=.3), k(.5, 'shoulder', reach=1, x=-.6, y=-.8, b=-.8, r=1, mark='fwip'), k(.72, 'back', reach=.5, x=-.2, y=-.2, w=.5, eye='^')],
        [], g='use', act=('throw', 'tail'), prefer=['happy'], obj=[(.3, dict(wx=.2)), (.5, dict(flap=.8)), (.8, dict(flap=0, wx=0))],
        say=["Over the shoulder. Looks expensive now.", "Dashing. Slightly lopsided. Dashing."])
    o.r('cross_the_tails_into_a_bow', 'Crossing the two tails under his chin and knotting them into a bow', 20, 'wing',
        [k(.1, 'belly', reach=.5, x=.3, y=.6, b=.3), k(.28, 'throat', reach=1, x=.7, y=.9, b=.6, mark='hnf'), k(.46, 'neck', reach=1, x=.8, y=.9, b=.7, l=1), k(.64, 'throat', reach=1, x=.6, y=1, b=.6, r=1), k(.82, 'belly', reach=.6, x=.3, y=.5, b=.4), k(.92, y=-.1, w=.4, eye='^')],
        [(.64, 'snug')], g='use', act=('tie', 'tails'), when=['knot<.5'], prefer=['curious'], say=["A bow. Somebody mistook me for a present.", "Tied it myself. Do not ask how."])
    o.r('drag_it_along_behind', 'Slipping the scarf off by one end and trailing it along the ground like a tail', 22, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.25, 'neck', x=1.3, y=1.1, b=.7, mark='hup'), k(.42, x=-.6, y=.5, b=.9, l=1), k(.58, x=-.7, y=.5, b=1, r=1), k(.74, 'neck', x=1.1, y=.9, b=.6), k(.88, eye='^')],
        [], g='use', act=('drag', 'scarf'), prefer=['young'],
        obj=[(.25, dict(off=1, hold=1)), (.42, dict(off=1, ix=-3)), (.62, dict(off=1, ix=-3)), (.76, dict(off=1, hold=1)), (.86, dict(off=0))])
    o.r('tuck_the_tails_against_his_belly', 'Pressing both loose tails flat against his belly so the wind cannot lift them', 16, 'wing',
        [k(.12, 'throat', reach=.5, x=.2, y=.4, b=.3), k(.3, 'belly', reach=1, x=.4, y=1, b=.7, l=1), k(.5, 'belly', reach=1, x=.5, y=1.1, b=.9, r=1), k(.7, 'belly', reach=1, x=.3, y=.8, b=.6), k(.88, eye='-')],
        [(.5, 'snug')], g='use', act=('push', 'tails'), when=['windy'], obj=[(.15, dict(flap=.7)), (.5, dict(flap=.2)), (.75, dict(flap=0))])
    # ---------------- play
    o.r('snap_at_the_swinging_fringe', 'Snapping at the swinging fringe, spinning round after it and never quite catching it', 18, 'none',
        [k(.12, 'belly', x=1.2, y=.8, b=.4, r=1, mark='snap'), k(.3, x=-1, y=-.3, b=-.5, w=.8, eye='O'), k(.5, 'foot_l', x=-1.2, y=.9, b=.4, l=1, mark='snap'), k(.7, x=1, y=-.3, b=-.5, w=.8, eye='O'), k(.88, y=.4, b=.5, eye='@')],
        [(.5, 'fun')], g='play', act=('chase', 'fringe'), prefer=['young', 'happy'], obj=[(.3, dict(flap=.6)), (.7, dict(flap=.6)), (.9, dict(flap=0))],
        say=["Almost. It's quick, this fringe.", "It was behind me the whole time."])
    o.r('spin_till_the_tails_stream', 'Spinning round and round so both tails stream out sideways', 16, 'none',
        [k(.15, x=.2, y=-.3, b=-.3, w=.4), k(.35, x=.8, y=-.5, b=-.8, w=1, l=1), k(.55, x=-.8, y=-.5, b=-.8, w=1, r=1, mark='whee'), k(.75, x=.6, y=-.4, b=-.6, w=1, l=1), k(.9, y=.5, b=.5, eye='@')],
        [], g='play', act=('spin', 'scarf'), prefer=['windy', 'happy'], obj=[(.3, dict(flap=.6)), (.55, dict(flap=1)), (.75, dict(flap=1)), (.9, dict(flap=0))])
    o.r('toss_it_up_and_catch_it', 'Pulling the scarf off, tossing it up in his bill and catching it again on the way down', 20, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.24, 'neck', x=1.3, y=1.1, b=.7, mark='hup'), k(.4, x=.3, y=-1.2, b=-.9, w=.6), k(.52, x=.4, y=-.8, b=-.5, eye='O'), k(.64, 'belly', x=.8, y=.5, b=.5), k(.78, 'neck', x=1, y=.9, b=.6), k(.9, eye='^')],
        [], g='play', act=('throw', 'scarf'), prefer=['happy'],
        obj=[(.24, dict(off=1, hold=1)), (.4, dict(off=1, iy=3)), (.52, dict(off=1, iy=2)), (.64, dict(off=1, hold=1)), (.8, dict(off=0))])
    o.r('race_the_gust_with_both_tails_out', 'Racing a gust along the ground with both tails streaming out sideways', 18, 'none',
        [k(.12, x=.5, y=-.2, b=.3), k(.3, x=1.2, y=-.4, b=-.5, w=.6, l=1), k(.5, x=1.5, y=-.4, b=-.6, w=.8, r=1), k(.7, x=1.2, y=-.4, b=-.5, w=.6, l=1), k(.88, x=.2, y=.4, b=.5, eye='O')],
        [], g='play', act=('race', 'wind'), when=['windy'], prefer=['young'], obj=[(.2, dict(flap=.5)), (.5, dict(flap=1)), (.8, dict(flap=.4)), (.92, dict(flap=0))])
    o.r('pull_against_his_own_fringe', 'Gripping one fringe end in his bill and leaning back as if it were an opponent', 18, 'none',
        [k(.12, 'belly', x=1, y=1.3, b=.5), k(.3, 'belly', x=.2, y=1.6, b=1.2, l=1, mark='grr'), k(.5, 'foot_r', x=-.5, y=1.7, b=1.4, r=1, w=.4, mark='GRR'), k(.7, 'belly', x=-.6, y=1.5, b=1.1, w=.6), k(.88, y=.8, b=.6, eye='-')],
        [(.5, 'ruffle')], g='play', act=('pull', 'fringe'), when=['neat>.5'], prefer=['grumpy'], obj=[(.3, dict(wy=.3)), (.5, dict(wy=.5)), (.75, dict(wy=0))],
        say=["Won. Against myself. Humbling.", "Fringe fought dirty. It's a very good scarf."])
    o.r('whirl_it_round_like_a_lasso', 'Whirling the scarf round over his head by one end like a lasso', 20, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.22, 'neck', x=1.3, y=1, b=.7, mark='hup'), k(.38, x=.2, y=-.8, b=-.5, w=.9, l=1), k(.52, 'bill', x=.5, y=-1, b=-.7, w=1, r=1, mark='wheet'), k(.66, x=-.2, y=-.8, b=-.5, w=.9, l=1), k(.8, 'neck', x=1, y=.8, b=.5), k(.9, eye='^')],
        [(.52, 'ruffle')], g='play', act=('spin', 'lasso'), when=['neat>.5'], prefer=['happy'],
        obj=[(.22, dict(off=1, hold=1)), (.5, dict(off=1, hold=1)), (.7, dict(off=1, hold=1)), (.82, dict(off=0))])
    o.r('hop_back_and_forth_over_it', 'Laying the scarf out flat and hopping back and forth over it, three times', 24, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.2, 'neck', x=1.2, y=.8, b=.6, mark='hup'), k(.34, x=.3, y=-.3, b=-1, w=.6), k(.46, x=.2, y=.4, b=.6, l=1), k(.58, x=-.3, y=-.3, b=-1, w=.6), k(.7, x=-.2, y=.4, b=.6, r=1), k(.82, 'neck', x=1, y=.9, b=.6), k(.92, eye='^')],
        [], g='play', act=('hop', 'scarf'), prefer=['young', 'happy'],
        obj=[(.2, dict(off=1, hold=1)), (.3, dict(off=1, ix=2)), (.72, dict(off=1, ix=2)), (.8, dict(off=1, hold=1)), (.9, dict(off=0))])
    o.r('shuffle_off_as_somebody_old', 'Hauling a tail up over the crown like a bonnet and shuffling off, bent over, muttering', 22, 'wing',
        [k(.1, 'belly', reach=.5, x=.2, y=.4, b=.3), k(.26, 'throat', reach=1, x=-.2, y=-.4, b=-.3, w=.3), k(.4, 'crown', reach=1, x=-.3, y=.2, b=.6, mark='hmph'), k(.58, 'crown', reach=.6, x=.6, y=.8, b=1, l=1), k(.74, 'crown', reach=.6, x=.6, y=.8, b=1, r=1), k(.9, y=.2, eye='^')],
        [], g='play', act=('wrap', 'crown'), prefer=['happy', 'curious'], obj=[(.4, dict(wy=-.5)), (.74, dict(wy=-.5)), (.9, dict(wy=0))],
        say=["Back in my day, scarves were longer.", "Nobody can prove that bonnet is not just my head."])
    # ---------------- test
    o.r('sniff_the_wool', 'Sniffing the wool at the shoulder and the nape for the smell of the shop', 14, 'none',
        [k(.15, x=-.4, y=.9, b=.2), k(.35, 'shoulder', x=-.9, y=1.3, b=.4, mark='snf'), k(.55, 'nape', x=-.9, y=1.3, b=.5, l=1, mark='snf'), k(.8, x=.2, y=-.2, w=.3, eye='O')],
        [], g='test', act=('sniff', 'wool'), prefer=['curious'])
    o.r('count_the_ribs_with_his_bill', 'Counting the ribs down the long tail with his bill, neck to fringe', 20, 'none',
        [k(.12, 'neck', x=-.4, y=1.1, b=.3, mark='1'), k(.3, 'throat', x=.6, y=1.2, b=.4, mark='2'), k(.5, 'belly', x=.7, y=1.3, b=.5, r=1, mark='3'), k(.7, 'belly', x=.6, y=1.6, b=.7, mark='4'), k(.88, eye='-', mark='lots')],
        [], g='test', act=('count', 'ribs'), prefer=['curious'], say=["Lots of ribs. No bones.", "Four. Or forty. Lost count."])
    o.r('taste_a_fringe_end', 'Chewing a fringe end to test it and spitting the fluff out', 14, 'none',
        [k(.15, 'belly', x=1.3, y=1.6, b=.8), k(.35, 'belly', x=1, y=1.4, b=1, eye='-', mark='...'), k(.55, x=-.8, y=-.6, b=-.3, w=.7, l=1, eye='>', mark='ptui'), k(.8, y=.5, b=.3, eye='-')],
        [], g='test', act=('taste', 'fringe'), prefer=['curious', 'young'])
    o.r('hold_both_tail_ends_together', 'Holding the two tail ends together against each other to see which one hangs longer', 18, 'wing',
        [k(.12, 'belly', reach=.6, x=.3, y=.8, b=.4), k(.3, 'thigh', reach=1, x=.4, y=1.4, b=.9, l=1), k(.5, 'belly', reach=1, x=.3, y=1.1, b=.7), k(.7, 'thigh', reach=1, x=.4, y=1.5, b=1, r=1), k(.88, eye='-', mark='hm')],
        [], g='test', act=('compare', 'tails'), prefer=['curious'], say=["The left one is longer. Always has been.", "Uneven. Like my legs on a bad day."])
    o.r('weigh_it_in_his_bill', 'Pulling the scarf off, bobbing it twice in his bill to weigh it, and putting it back', 22, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.22, 'neck', x=1.3, y=1.1, b=.7, mark='hup'), k(.36, x=.4, y=-.6, b=-.6), k(.48, x=.9, y=.8, b=.5), k(.6, x=.3, y=-.6, b=-.6), k(.74, 'neck', x=1, y=.9, b=.6), k(.88, eye='-')],
        [], g='test', act=('weigh', 'scarf'), prefer=['curious'],
        obj=[(.22, dict(off=1, hold=1)), (.4, dict(off=1, hold=1)), (.62, dict(off=1, hold=1)), (.76, dict(off=0))])
    o.r('pluck_a_rib_to_hear_it_twang', 'Hooking a rib of the ribbing with his bill and letting it snap back', 14, 'none',
        [k(.15, 'throat', x=.8, y=1, b=.3), k(.3, 'throat', x=1.4, y=1.5, b=.7, mark='nnk'), k(.45, x=-.8, y=-.6, b=-.4, w=.6, eye='O', mark='boing'), k(.7, x=.2, y=.2, b=.2, eye='-')],
        [], g='test', act=('tug', 'rib'), prefer=['curious', 'young'], obj=[(.3, dict(wy=.3)), (.45, dict(wy=0))])
    # ---------------- rest
    o.r('sink_into_the_wraps_for_a_nap', 'Napping with his head sunk down into the wraps, tail ends in his lap', 28, 'none',
        [k(.15, x=-.2, y=.5, b=.4), k(.4, 'neck', x=-.9, y=2.2, b=1.5, eye='-'), k(.7, 'nape', x=-1, y=2.5, b=1.8, w=.3, eye='-', mark='zzz'), k(.9, x=.2, y=.2, b=.3, eye='O')],
        [], g='rest', act=('nap', 'wraps'), shown='head', when=['tired'], say=["Wool pillow. Worn by me.", "Out cold. Warm at the front."])
    o.r('sulk_with_a_tail_across_his_face', 'Dragging a tail across his face and sulking with his bill hidden in it', 20, 'wing',
        [k(.15, 'belly', reach=.5, x=.4, y=.6, b=.3), k(.4, 'throat', reach=1, x=-.6, y=1.2, b=.9, eye='-'), k(.7, 'neck', reach=1, x=-.8, y=1.5, b=1.1, eye='-', mark='hmph'), k(.9, reach=0, x=.1, y=.2, b=.3)],
        [], g='rest', act=('sulk', 'tail'), when=['sad'], obj=[(.4, dict(wy=-.4)), (.7, dict(wy=-.5)), (.92, dict(wy=0))])
    o.r('wait_with_a_foot_tapping', 'Waiting with one foot tapping and his bill propped against the knot', 22, 'none',
        [k(.15, x=.2, y=.4, b=.4, l=1), k(.4, 'throat', x=.4, y=1.1, b=.9, r=1, eye='-'), k(.65, 'throat', x=.3, y=1, b=.9, l=1, mark='tap'), k(.88, x=-.2, y=.2, b=.3, w=.4, eye='O')],
        [], g='rest', act=('wait', 'knot'), prefer=['lonely'], say=["Nobody. Fine. The knot and I will wait.", "Still here. The wool is patient, I am not."])
    o.r('plump_it_into_a_cushion', 'Taking the scarf off, plumping it into a cushion and settling down next to it with a sigh', 28, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.4), k(.22, 'neck', x=1.3, y=1.1, b=.7, mark='hup'), k(.36, 'rump', x=.4, y=.6, b=1.2), k(.5, 'rump', x=.2, y=1, b=1.8, eye='-', mark='ahh'), k(.68, 'rump', x=.3, y=.8, b=1.6, l=1), k(.8, 'neck', x=1, y=.9, b=.6), k(.9, eye='^')],
        [], g='rest', act=('sit', 'cushion'), prefer=['tired'],
        obj=[(.22, dict(off=1, hold=1)), (.4, dict(off=1, ix=1)), (.7, dict(off=1, ix=1)), (.78, dict(off=1, hold=1)), (.88, dict(off=0))],
        say=["Best seat in the yard. Made of me.", "Cushion. Warm. Mine. Do not sit."])
    # ---------------- weather
    o.r('wring_out_the_long_tail', 'Wringing the rain out of the soaked tail with both wings, neck to fringe', 18, 'wing',
        [k(.12, 'throat', reach=.5, x=.2, y=.7, b=.4), k(.3, 'belly', reach=1, x=.2, y=1.3, b=.9, l=1, mark='squeeze'), k(.5, 'belly', reach=1, x=.2, y=1.5, b=1.1, r=1, mark='drip'), k(.7, 'thigh', reach=1, x=.2, y=1.6, b=1.1), k(.88, y=.2, eye='-')],
        [(.5, 'wring')], g='weather', act=('squeeze', 'tail'), when=['soaked>.3'])
    o.r('shake_the_snow_off', 'Shaking the snow off the scarf, wings out, whole body rattling', 16, 'none',
        [k(.12, x=.2, y=.5, b=.3), k(.3, 'shoulder', x=.8, y=.1, b=-.5, w=1, l=1, mark='brrr'), k(.5, 'throat', x=-.8, y=.1, b=-.7, w=1, r=1), k(.7, 'belly', x=.8, y=.1, b=-.5, w=1, l=1), k(.88, eye='-')],
        [(.5, 'flick')], g='weather', act=('shake', 'snow'), when=['snow>.3'], prefer=['happy'], obj=[(.3, dict(flap=.8)), (.7, dict(flap=.8)), (.88, dict(flap=0))])
    o.r('brace_into_the_gale', 'Bracing into the gale, legs planted wide, with both tails snapping out sideways', 22, 'none',
        [k(.12, x=.4, y=.3, b=.5), k(.3, x=1.2, y=.9, b=1.3, w=.5, l=1), k(.55, x=1.4, y=1.2, b=1.5, w=.4, r=1, eye='>', mark='fwoom'), k(.8, x=.5, y=.5, b=.6, eye='-')],
        [], g='weather', act=('brace', 'wind'), when=['windy'], obj=[(.15, dict(flap=.5)), (.4, dict(flap=1)), (.7, dict(flap=1)), (.9, dict(flap=0))], say=["Scarf is going to Narnia. I am staying.", "Wind: one. Neck: still attached."])
    o.r('hold_out_the_tails_to_the_sun', 'Holding both damp tails out wide to the sun, turning them over to dry', 26, 'wing',
        [k(.12, 'throat', reach=.5, x=-.2, y=.3, b=.3), k(.3, 'belly', reach=1, x=-.4, y=-.2, b=.4, w=.5, mark='fff'), k(.5, 'belly', reach=1, x=-.5, y=-.3, b=.2, l=1, w=.8), k(.7, 'thigh', reach=1, x=-.4, y=-.2, b=.4, r=1), k(.88, eye='^')],
        [(.5, 'wring')], g='weather', act=('dry', 'tails'), when=['sun', 'soaked>.3'], obj=[(.3, dict(flap=.4)), (.5, dict(flap=.7)), (.8, dict(flap=0))])
    o.r('hunch_through_the_downpour_under_a_tail_hood', 'Pulling the long tail up over his crown as a hood and hunching out the downpour', 32, 'none',
        [k(.12, 'neck', x=.2, y=.4, b=.4), k(.3, 'crown', x=-.6, y=1.2, b=1.3, eye='-', mark='patter'), k(.55, 'crown', x=-.8, y=1.6, b=1.6, w=.3, eye='-', mark='drip'), k(.8, 'crown', x=-.4, y=1, b=1.1, eye='>')],
        [], g='weather', act=('shelter', 'hood'), when=['storm', 'wet'], obj=[(.3, dict(wy=-.5)), (.6, dict(wy=-.6)), (.9, dict(wy=0))])
    # ---------------- show
    o.r('show_off_the_long_tail', 'Swishing the long tail out with a wing and turning slowly to show it off', 16, 'wing',
        [k(.15, 'belly', reach=.6, x=-.2, y=-.4, b=-.3, l=1), k(.4, 'belly', reach=1, x=.3, y=-.7, b=-.7, w=.5), k(.65, 'throat', reach=1, x=-.3, y=-.8, b=-.9, r=1, mark='ta-da'), k(.85, reach=0, y=.4, b=.3, eye='^')],
        [], g='show', act=('present', 'scarf'), prefer=['happy'], obj=[(.4, dict(flap=.6)), (.7, dict(flap=.2)), (.88, dict(flap=0))])
    o.r('bow_with_both_tails_swinging', 'Bowing so deep that both tails swing forward past his bill', 14, 'none',
        [k(.15, x=-.5, y=-.8, b=-.6, w=.6, l=1), k(.4, 'belly', x=1.4, y=1.8, b=1.1, w=.9, r=1), k(.65, 'foot_l', x=1.5, y=2, b=1.3, w=1, mark='...'), k(.88, x=-.4, y=-.7, b=-.4, w=.3, eye='^')],
        [], g='show', act=('bow', 'scarf'), prefer=['happy'], obj=[(.4, dict(flap=.5)), (.65, dict(flap=.2)), (.9, dict(flap=0))])
    o.r('strike_a_pose_with_a_tail_out', 'Freezing with one tail held out at arm length and the other over the shoulder', 18, 'wing',
        [k(.12, 'belly', reach=.4, x=-.2, y=-.4, b=-.3), k(.35, 'belly', reach=1, x=.4, y=-1, b=.6, w=1, l=1), k(.6, 'shoulder', reach=1, x=.4, y=-1.2, b=.8, w=.4, r=1, mark='...'), k(.85, y=.3, b=.2, eye='^')],
        [], g='show', act=('pose', 'tails'), prefer=['happy'], obj=[(.35, dict(wx=.2)), (.6, dict(flap=.2)), (.88, dict(flap=0, wx=0))])
    o.r('argue_with_the_knot', 'Arguing with his own knot, jabbing his bill at it until it gives', 16, 'none',
        [k(.15, x=.5, y=.5, b=.2, eye='>'), k(.3, 'throat', x=1.4, y=1.3, b=.7, w=1, mark='GAH'), k(.5, 'neck', x=-.6, y=-.2, b=-.3, w=.4, l=1), k(.7, 'throat', x=1.5, y=1.4, b=.8, w=1, r=1, mark='GAH'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'knot'), prefer=['grumpy'], say=["Knot: winning. Bill: sore.", "Argued with wool. Lost on points."])
    o.r('dance_the_fringe_into_a_blur', 'Dancing a fast shuffle so the fringe on both tails whips round in a blur', 20, 'none',
        [k(.12, x=.2, y=-.2, b=-.3, l=1), k(.3, 'belly', x=.5, y=-.5, b=-.7, r=1, w=.6, mark='tap'), k(.5, 'foot_r', x=-.5, y=-.6, b=-.9, l=1, w=.8, mark='tap'), k(.7, 'belly', x=.5, y=-.5, b=-.7, r=1, w=.6), k(.88, y=.4, b=.5, eye='^')],
        [(.5, 'fun')], g='show', act=('dance', 'fringe'), prefer=['happy', 'young'], obj=[(.3, dict(flap=.7)), (.6, dict(flap=.9)), (.85, dict(flap=0))])
    # ---------------- mishap
    o.r('tread_on_the_long_tail', 'Treading on the long tail end mid-stride and going over beak first', 16, 'none',
        [k(.15, 'foot_l', x=.4, y=.5, b=.3, l=1), k(.3, x=.5, y=-.3, b=-.7, w=1, l=1, r=1, eye='O', mark='WHA'), k(.5, x=1.2, y=1.8, b=1.5, w=.8, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'tail'), prefer=['young'], say=["Tripped on myself. Impressive.", "My scarf. My trap. My arse."])
    o.r('choke_on_his_own_wraps', 'Yanking the wraps too tight and sticking there, gasping, until they let go', 18, 'none',
        [k(.15, 'neck', x=.2, y=.8, b=.3), k(.35, 'neck', x=-1.2, y=-.5, b=-.4, w=.5, eye='O', mark='gak'), k(.6, 'throat', x=-1.4, y=-.6, b=-.2, w=.8, l=1, r=1, eye='@', mark='hkk'), k(.85, x=.2, y=.4, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'wraps'), prefer=['grumpy'], obj=[(.35, dict(wy=-.4)), (.6, dict(wy=-.6)), (.85, dict(wy=0))])
    o.r('catch_the_sagging_scarf', 'Lunging to catch the scarf as it slides loose from his neck and hauling it back up', 16, 'wing',
        [k(.12, x=.2, y=.4, b=.4), k(.3, 'shoulder', reach=1, x=-.5, y=.7, b=.9, eye='O', mark='whoa'), k(.5, 'neck', reach=1, x=-.7, y=.8, b=1.1, l=1), k(.7, 'throat', reach=1, x=-.2, y=.5, b=.6), k(.88, eye='-')],
        [], g='mishap', act=('catch', 'scarf'), when=['knot<.4'], obj=[(.2, dict(sag=.5)), (.4, dict(sag=1)), (.6, dict(sag=.4)), (.8, dict(sag=0))])
    o.r('chase_it_down_the_yard', 'Chasing the scarf down the yard after a gust whips it off his neck', 24, 'none',
        [k(.1, 'neck', x=.8, y=.4, b=.3, eye='O'), k(.28, x=1.2, y=-.2, b=-.5, w=.6, l=1, mark='HEY'), k(.46, x=1.5, y=-.3, b=-.7, w=.8, r=1), k(.64, 'neck', x=1.3, y=1, b=.8, eye='>'), k(.8, 'neck', x=.4, y=.4, b=.3, eye='^')],
        [], g='mishap', act=('chase', 'scarf'), when=['windy'],
        obj=[(.1, dict(off=1)), (.28, dict(off=1, ix=3)), (.46, dict(off=1, ix=6)), (.64, dict(off=1, hold=1)), (.82, dict(off=0))],
        say=["Come back. I paid for you. Probably.", "The wind took it. I took it back."])
    o.r('peck_at_the_dangling_fringe', 'Pecking at the dangling fringe mistaking it for worms, then glaring at it', 14, 'none',
        [k(.15, 'belly', x=.9, y=1.4, b=.6, mark='pk'), k(.32, 'belly', x=1.3, y=1.7, b=.9, r=1, mark='pk'), k(.5, x=-.6, y=-.4, b=-.3, w=.6, eye='O'), k(.72, 'foot_r', x=1.1, y=1.5, b=.8, eye='>', mark='pk'), k(.9, eye='-')],
        [(.32, 'ruffle')], g='mishap', act=('peck', 'fringe'), prefer=['young', 'curious'], when=['neat>.5'])
    # @@END scarf_red
    return done(o)


def scarf_winter():
    # Worn: thick blue cable-knit scarf (wool, heavy). Drawing: a big round collar loop, a band of `~` across the middle, and two hanging ends of
    # cable twists (`()` and `)(` columns) with a fringe `: | | :` at the bottom of each. Heavy, so it sags, gathers snow, pills and holds frost.
    # Body places as on scarf_red: collar = neck/nape/shoulder, knot = throat, the ends hang over belly and thigh.
    o = Obj('scarf_winter', 'wearable',
            fields=dict(wraps=(.5, 0, 1), neat=(.7, 0, 1), soaked=(0, 0, 1), snow=(0, 0, 1), frost=(0, 0, 1), pills=(0, 0, 1)),
            physics=[('wraps', 'rate', -.0005, 'windy'), ('neat', 'rate', -.0004, 'windy'), ('soaked', 'rate', .002, 'wet'), ('soaked', 'rate', -.0007, 'dry&warm'),
                     ('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm'), ('frost', 'rate', .0015, 'cold&!snow'), ('frost', 'rate', -.002, 'warm'),
                     ('pills', 'rate', .0004, 'always')],
            effects=dict(wind=[('wraps', 'set', 1)], loose=[('wraps', 'set', .1)], plump=[('neat', 'set', 1)], tangle=[('neat', 'add', -.4)],
                         wring=[('soaked', 'mul', .25)], flick=[('snow', 'set', 0)], crack=[('frost', 'mul', .1)], pick=[('pills', 'set', 0)],
                         cosy=[('need.energy', 'add', 2)], fun=[('need.fun', 'add', 2)]),
            anchors=dict(crown=0, brow=0, cheek=0, bill=0, nape=0, neck=0, shoulder=0, back=0, throat=0, belly=0, thigh=0, foot_l=0, foot_r=0, wing=0))
    # ---------------- care
    o.r('pick_the_pills_off', 'Nipping the woollen pills off the cable knit one by one and flicking them away', 16, 'none',
        [k(.12, 'shoulder', x=-.4, y=1, b=.4), k(.28, 'shoulder', x=-.9, y=1.5, b=.7, mark='nip'), k(.44, 'nape', x=-1, y=1.4, b=.8, l=1, mark='nip'), k(.6, 'nape', x=-.5, y=.6, b=.3, w=.5, eye='>', mark='ptui'), k(.8, x=.2, y=.3, eye='^')],
        [(.44, 'pick')], g='care', act=('peck', 'pills'), when=['pills>.35'], prefer=['curious'], say=["Bobbles gone. The scarf looks hurt.", "Forty pills picked. A duck has hobbies."])
    o.r('chip_the_frost_off_the_cables', 'Chipping the frost crust off the cable twists with the tip of a wing', 18, 'wing',
        [k(.12, 'throat', reach=.5, x=-.2, y=.7, b=.4), k(.3, 'throat', reach=1, x=.3, y=1, b=.7, mark='tik'), k(.5, 'belly', reach=1, x=.4, y=1.2, b=.8, l=1, mark='tik'), k(.7, 'thigh', reach=1, x=.3, y=1.3, b=.9, r=1, mark='tik'), k(.88, eye='-')],
        [(.5, 'crack')], g='care', act=('chip', 'cables'), when=['frost>.3'], obj=[(.3, dict(wx=.2)), (.6, dict(wx=0))])
    o.r('knead_the_cables_plump', 'Kneading the flattened cable twists back up with both wings until they stand out round again', 20, 'wing',
        [k(.12, 'throat', reach=.5, x=.1, y=.5, b=.4), k(.3, 'throat', reach=1, x=.2, y=.9, b=.8, l=1), k(.5, 'belly', reach=1, x=.2, y=1, b=1, r=1), k(.7, 'thigh', reach=1, x=.2, y=1.1, b=1.1, l=1), k(.88, y=.1, w=.4, eye='^')],
        [(.5, 'plump')], g='care', act=('fluff', 'cables'), when=['neat<.5'], prefer=['happy'], obj=[(.3, dict(wy=.2)), (.5, dict(wy=-.2)), (.7, dict(wy=.2)), (.88, dict(wy=0))])
    o.r('sweep_the_snow_off_the_collar', 'Sweeping the snow off the thick collar loop with a wing, round from nape to throat', 16, 'wing',
        [k(.12, 'nape', reach=.5, x=-.3, y=.4, b=.2), k(.3, 'shoulder', reach=1, x=-.6, y=.8, b=.4, mark='fff'), k(.5, 'neck', reach=1, x=-.4, y=.9, b=.5, l=1), k(.7, 'throat', reach=1, x=-.2, y=1, b=.5, r=1), k(.88, eye='^')],
        [(.5, 'flick')], g='care', act=('sweep', 'collar'), when=['snow>.3'], obj=[(.4, dict(flap=.4)), (.7, dict(flap=0))])
    o.r('press_the_water_out_against_his_belly', 'Pressing the sodden wool flat against his belly with a wing to squeeze the water out of it', 22, 'wing',
        [k(.12, 'throat', reach=.5, x=.2, y=.7, b=.5), k(.3, 'belly', reach=1, x=.3, y=1.2, b=1.1, l=1, mark='squish'), k(.5, 'belly', reach=1, x=.3, y=1.5, b=1.4, mark='drip'), k(.7, 'belly', reach=1, x=.2, y=1.3, b=1.2, r=1, mark='squish'), k(.88, y=.2, eye='-')],
        [(.5, 'wring')], g='care', act=('press', 'wool'), when=['soaked>.3'], say=["Pressed a sponge to my stomach. Great morning.", "It weighs more than I do. Allegedly."])
    o.r('spread_it_flat_to_dry', 'Hauling the sodden scarf off and spreading it out flat beside him with both wings', 28, 'wing',
        [k(.1, 'neck', reach=.4, x=.8, y=.9, b=.5), k(.24, 'neck', reach=1, x=1, y=.7, b=.8, mark='hup'), k(.4, 'belly', reach=1, x=.4, y=1.2, b=1, w=.3, l=1), k(.56, 'belly', reach=1, x=.5, y=1.3, b=1.1, r=1), k(.72, 'neck', reach=1, x=1, y=.8, b=.8), k(.86, 'throat', reach=.6, x=.3, y=.5, b=.4), k(.94, eye='^')],
        [(.56, 'wring')], g='care', act=('open', 'scarf'), when=['soaked>.3'],
        obj=[(.24, dict(off=1, hold=1)), (.4, dict(off=1, ix=2)), (.6, dict(off=1, ix=3)), (.74, dict(off=1, hold=1)), (.88, dict(off=0))])
    o.r('turn_the_collar_roll_back_down', 'Turning the collar roll back down turn by turn after it has bunched up round his ears', 18, 'wing',
        [k(.12, 'cheek', reach=.4, x=-.2, y=.3, b=.3), k(.3, 'cheek', reach=1, x=-.5, y=.5, b=.6), k(.5, 'nape', reach=1, x=-.7, y=.7, b=.7, l=1), k(.7, 'neck', reach=1, x=-.4, y=.8, b=.6, r=1), k(.88, y=-.1, eye='^')],
        [(.7, 'plump')], g='care', act=('fold', 'collar'), when=['neat<.4'], prefer=['curious'], obj=[(.3, dict(wy=-.3)), (.6, dict(wy=.2)), (.8, dict(wy=0))])
    # ---------------- use
    o.r('wind_the_loops_up_to_the_ears', 'Winding the loops up round his neck, turn after turn, until he is mostly scarf', 22, 'wing',
        [k(.1, 'throat', reach=.5, x=-.2, y=.5, b=.3), k(.26, 'neck', reach=1, x=-.5, y=.8, b=.6, l=1), k(.42, 'nape', reach=1, x=-.8, y=.8, b=.8, r=1), k(.58, 'shoulder', reach=1, x=-.6, y=.9, b=.9, l=1), k(.74, 'throat', reach=1, x=-.3, y=.7, b=.6), k(.9, eye='-')],
        [(.74, 'wind'), (.74, 'cosy')], g='use', act=('wrap', 'wraps'), when=['cold', 'wraps<.5'], obj=[(.3, dict(wx=.3)), (.5, dict(wx=-.3)), (.7, dict(wx=.2)), (.88, dict(wx=0))],
        say=["Wound up. Ready for any season but this one.", "I am a duck-shaped bun of wool."])
    o.r('unwind_a_turn_in_the_warmth', 'Unwinding a turn of the heavy wrap and letting it hang slack off one shoulder', 16, 'none',
        [k(.12, x=.2, y=.9, b=.3), k(.3, 'shoulder', x=-.8, y=1.5, b=.8, mark='nnf'), k(.5, 'neck', x=-.5, y=1, b=.9, l=1), k(.7, 'shoulder', x=-.2, y=.5, b=.4, eye='-', mark='ahh'), k(.88, y=-.2, w=.3, eye='^')],
        [(.5, 'loose')], g='use', act=('unwrap', 'wraps'), when=['wraps>.6', 'warm'], prefer=['sad'], obj=[(.3, dict(sag=.4)), (.6, dict(sag=.8))])
    o.r('knot_the_ends_at_the_nape', 'Reaching both ends round to the nape and knotting them there out of the wind', 22, 'wing',
        [k(.1, 'belly', reach=.5, x=.3, y=.7, b=.3), k(.28, 'back', reach=1, x=-.6, y=.5, b=.4), k(.46, 'nape', reach=1, x=-.9, y=.8, b=.7, l=1, mark='hnf'), k(.64, 'nape', reach=1, x=-1, y=.9, b=.8, r=1), k(.82, 'shoulder', reach=.6, x=-.3, y=.5, b=.4), k(.92, eye='^')],
        [(.64, 'wind')], g='use', act=('tie', 'ends'), when=['wraps<.4'], prefer=['curious'])
    o.r('roll_it_up_into_a_bundle', 'Pulling the scarf off, rolling it into a tight bundle with bill and wing, and unrolling it back round his neck', 28, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.5), k(.22, 'neck', x=1.3, y=1.1, b=.8, mark='hup'), k(.36, 'belly', x=.6, y=1.4, b=1.2, w=.4, l=1), k(.5, 'belly', x=.5, y=1.6, b=1.4, w=.5, r=1, mark='rrr'), k(.64, 'foot_l', x=.5, y=1.5, b=1.2, l=1), k(.78, 'neck', x=1.1, y=.9, b=.7), k(.9, eye='^')],
        [], g='use', act=('roll', 'scarf'), prefer=['curious'],
        obj=[(.22, dict(off=1, hold=1)), (.38, dict(off=1, ix=1)), (.5, dict(off=1, ix=2)), (.66, dict(off=1, ix=2)), (.8, dict(off=1, hold=1)), (.9, dict(off=0))],
        say=["A bundle. Now it travels. Very practical.", "Rolled it up. Unrolled it. Productive afternoon."])
    o.r('heft_both_ends_and_carry_them', 'Pulling the scarf off and carrying it a few steps with a heavy end hooked over each wing', 22, 'wing',
        [k(.1, 'neck', reach=.5, x=.7, y=.9, b=.5), k(.24, 'neck', reach=1, x=1, y=.8, b=.9, mark='hup'), k(.4, 'wing', reach=1, x=.3, y=.2, b=.5, l=1), k(.56, 'wing', reach=1, x=.3, y=.2, b=.5, r=1), k(.72, 'neck', reach=1, x=1, y=.8, b=.8), k(.88, 'throat', reach=.5, x=.2, y=.4, b=.3)],
        [], g='use', act=('carry', 'ends'), prefer=['grown'],
        obj=[(.24, dict(off=1, hold=1)), (.4, dict(off=1, hold=1)), (.6, dict(off=1, hold=1)), (.74, dict(off=1, hold=1)), (.86, dict(off=0))])
    o.r('haul_it_up_until_one_eye_shows', 'Hauling the whole scarf up over his bill and crown until just one eye shows', 22, 'none',
        [k(.12, x=-.3, y=.5, b=.4), k(.3, 'bill', x=-1.5, y=2.2, b=1.6, eye='-'), k(.52, 'crown', x=-1.8, y=2.6, b=2, eye='-', mark='mmf'), k(.74, 'crown', x=-1.2, y=1.6, b=1.2, eye='o'), k(.9, y=.2, eye='O')],
        [(.52, 'cosy')], g='use', act=('hide', 'crown'), when=['cold'], obj=[(.3, dict(wy=-.5)), (.55, dict(wy=-.7)), (.9, dict(wy=0))])
    o.r('swing_both_ends_back_over_his_shoulders', 'Flinging both ends back over his shoulders at once with a sweep of the wings', 16, 'wing',
        [k(.12, 'belly', reach=.5, x=.2, y=.4, b=.3), k(.3, 'throat', reach=1, x=-.2, y=-.4, b=-.4, w=.4), k(.5, 'shoulder', reach=1, x=-.7, y=-.7, b=-.8, w=.8, l=1, r=1, mark='fwump'), k(.7, 'back', reach=.6, x=-.3, y=-.3, w=.5, eye='^')],
        [], g='use', act=('throw', 'ends'), prefer=['happy'], obj=[(.3, dict(wx=.2)), (.5, dict(flap=.8)), (.8, dict(flap=0, wx=0))])
    o.r('heave_the_wraps_up_off_his_shoulders', 'Heaving the sagging wraps up off his shoulders with both wings to take the weight', 16, 'wing',
        [k(.12, 'shoulder', reach=.5, x=-.2, y=.7, b=.6), k(.3, 'shoulder', reach=1, x=-.2, y=.3, b=1.2, l=1, w=.3, mark='hnnh'), k(.5, 'neck', reach=1, x=-.2, y=-.2, b=-.3, r=1, eye='^'), k(.72, 'throat', reach=.6, x=0, y=.3, b=.3), k(.88, eye='-')],
        [], g='use', act=('lift', 'wraps'), when=['wraps>.7'], obj=[(.2, dict(sag=.6)), (.4, dict(sag=1)), (.55, dict(sag=.2)), (.8, dict(sag=0))])
    # ---------------- play
    o.r('spin_so_the_heavy_ends_swing_wide', 'Spinning on the spot so the two heavy ends swing out wide and wrap his legs', 16, 'none',
        [k(.15, x=.2, y=-.3, b=-.3, w=.4), k(.35, x=.9, y=-.6, b=-.9, w=1, l=1), k(.55, 'thigh', x=-.9, y=-.6, b=-.9, w=1, r=1, mark='whump'), k(.75, 'foot_l', x=.7, y=-.4, b=-.6, w=1, l=1), k(.9, y=.6, b=.7, eye='@')],
        [(.55, 'fun')], g='play', act=('spin', 'ends'), prefer=['happy', 'young'], obj=[(.35, dict(flap=.6)), (.55, dict(flap=1)), (.8, dict(flap=.4)), (.92, dict(flap=0))], say=["The ends have more momentum than I do.", "Spun. Wrapped. Mildly bound."])
    o.r('tug_of_war_with_his_own_cable', 'Gripping the end of the cable in his bill and hauling backwards against his own neck', 20, 'none',
        [k(.12, 'thigh', x=1, y=1.4, b=.6), k(.3, 'thigh', x=.1, y=1.7, b=1.4, l=1, mark='grr'), k(.5, 'belly', x=-.6, y=1.8, b=1.7, w=.4, r=1, mark='GRRR'), k(.7, 'belly', x=-.7, y=1.5, b=1.3, w=.7), k(.88, y=.8, b=.6, eye='-')],
        [(.5, 'tangle')], g='play', act=('pull', 'cable'), when=['neat>.5'], prefer=['grumpy'], obj=[(.3, dict(wy=.4)), (.5, dict(wy=.6)), (.75, dict(wy=0))])
    o.r('fling_it_up_and_duck_into_it', 'Whipping the scarf off, flinging it up and ducking his head so it drops back round his neck', 22, 'none',
        [k(.1, 'neck', x=.8, y=.9, b=.5), k(.22, 'neck', x=1.4, y=1.1, b=.8, mark='hup'), k(.36, x=.3, y=-1.4, b=-1, w=.8, eye='O'), k(.5, x=.4, y=-.9, b=-.6, eye='O'), k(.64, 'neck', x=.6, y=1.8, b=1.4, eye='>'), k(.78, 'neck', x=-.3, y=.4, b=.2, w=.5, eye='^', mark='ta-da')],
        [], g='play', act=('catch', 'loop'), prefer=['happy'],
        obj=[(.22, dict(off=1, hold=1)), (.38, dict(off=1, iy=4)), (.52, dict(off=1, iy=2)), (.66, dict(off=1, iy=1)), (.78, dict(off=0))])
    o.r('march_on_the_spot_like_a_drum_major', 'Marching in place with his knees high, the heavy ends swinging like a drum major sash', 20, 'none',
        [k(.12, x=.2, y=-.3, b=-.4, l=1), k(.28, x=.4, y=-.4, b=-.6, r=1, w=.5), k(.44, x=.2, y=-.4, b=-.6, l=1, w=.5), k(.6, x=.4, y=-.4, b=-.6, r=1, w=.5, mark='hup'), k(.76, x=.2, y=-.3, b=-.4, l=1), k(.9, y=.3, b=.3, eye='^')],
        [], g='play', act=('hop', 'ends'), prefer=['happy', 'young'], obj=[(.28, dict(flap=.3)), (.5, dict(flap=.6)), (.7, dict(flap=.6)), (.9, dict(flap=0))])
    o.r('rock_from_foot_to_foot_like_a_pendulum', 'Rocking from foot to foot so the heavy ends swing like a pendulum and tick', 18, 'none',
        [k(.14, x=.2, y=.2, b=.4, l=1), k(.3, x=-.2, y=.3, b=.6, r=1, mark='tick'), k(.46, x=.2, y=.3, b=.6, l=1, mark='tock'), k(.62, x=-.2, y=.3, b=.6, r=1, mark='tick'), k(.78, x=.2, y=.2, b=.4, l=1, mark='tock'), k(.9, eye='-')],
        [], g='play', act=('rock', 'ends'), prefer=['curious'], obj=[(.3, dict(sag=.3)), (.46, dict(sag=-.3)), (.62, dict(sag=.3)), (.78, dict(sag=-.3)), (.9, dict(sag=0))])
    o.r('belly_slide_along_the_snow', 'Belly-sliding along the snow with both ends streaming out', 18, 'none',
        [k(.12, x=.5, y=.3, b=.6), k(.3, x=1.4, y=1.6, b=1.8, w=.6, l=1, r=1, mark='shhh'), k(.55, x=1.6, y=1.9, b=2, w=.8, eye='O'), k(.78, x=.8, y=1, b=1.2, eye='^'), k(.9, y=.3, b=.3)],
        [], g='play', act=('race', 'snow'), when=['snow>.3'], prefer=['young', 'happy'], obj=[(.3, dict(flap=.7)), (.55, dict(flap=1)), (.85, dict(flap=0))], say=["Toboggan. Scarf. Terrible plan, ten stars.", "Slid until the snow ran out. Then some more."])
    o.r('hold_both_ends_out_as_wings', 'Holding both ends out wide as wings and flapping them as if about to take off', 18, 'wing',
        [k(.12, 'belly', reach=.4, x=.1, y=.2, b=.3), k(.3, 'thigh', reach=1, x=.3, y=-.5, b=-.5, w=1, l=1), k(.5, 'belly', reach=1, x=.4, y=-.9, b=-.9, w=1, r=1, mark='flap flap'), k(.7, 'thigh', reach=1, x=.3, y=-.5, b=-.5, w=1, l=1), k(.88, y=.4, b=.5, eye='-')],
        [], g='play', act=('fluff', 'ends'), prefer=['young', 'happy'], obj=[(.3, dict(flap=.7)), (.5, dict(flap=1)), (.7, dict(flap=.7)), (.9, dict(flap=0))])
    o.r('totter_about_as_a_ghost', 'Throwing the scarf up over his head like a sheet and tottering about going wooo', 22, 'none',
        [k(.12, 'neck', x=.3, y=.6, b=.3), k(.28, 'crown', x=-.8, y=1.6, b=1.2, eye='-', mark='wooo'), k(.46, 'brow', x=-.4, y=1, b=.9, l=1, w=.6), k(.64, 'crown', x=-.8, y=1.6, b=1.2, r=1, w=.6, mark='WOOO'), k(.82, 'brow', x=-.3, y=.8, b=.6, eye='O')],
        [], g='play', act=('wrap', 'head'), prefer=['young', 'curious'], obj=[(.28, dict(wy=-.6)), (.5, dict(wy=-.7)), (.7, dict(wy=-.7)), (.9, dict(wy=0))], say=["Boo. Nobody scared. Boo again.", "Very frightening. For a nap."])
    # ---------------- test
    o.r('count_the_cable_twists', 'Counting the cable twists down one end with his bill, throat to fringe', 20, 'none',
        [k(.12, 'throat', x=.5, y=1, b=.4, mark='1'), k(.3, 'throat', x=.7, y=1.3, b=.6, mark='2'), k(.5, 'belly', x=.8, y=1.4, b=.7, r=1, mark='3'), k(.7, 'thigh', x=.7, y=1.6, b=.9, mark='4'), k(.88, eye='-', mark='lots')],
        [], g='test', act=('count', 'cables'), prefer=['curious'])
    o.r('tap_the_frozen_cable', 'Tapping the stiff frozen cable with his bill to hear it ring', 14, 'none',
        [k(.15, 'belly', x=1.2, y=1.2, b=.5, mark='tik'), k(.3, x=-.5, y=-.4, b=-.2, w=.4), k(.45, 'thigh', x=1.3, y=1.4, b=.7, l=1, mark='tik'), k(.6, x=-.5, y=-.4, b=-.2), k(.78, 'belly', x=1.2, y=1.3, b=.6, r=1, mark='tik'), k(.92, eye='^')],
        [], g='test', act=('tap', 'frost'), when=['frost>.2'], prefer=['curious'], say=["Rings like a bell. A very small bell.", "Frozen solid. Like my enthusiasm on Mondays."])
    o.r('sniff_the_damp_wool', 'Sniffing the damp wool of the collar and recoiling at the smell of wet sheep', 14, 'none',
        [k(.15, x=-.4, y=.9, b=.2), k(.35, 'neck', x=-.9, y=1.4, b=.4, mark='snf'), k(.55, x=-.8, y=-.6, b=-.3, w=.7, l=1, eye='>', mark='bleah'), k(.8, y=.3, eye='-')],
        [], g='test', act=('sniff', 'collar'), when=['soaked>.2'], prefer=['curious'], say=["Wet sheep. A whole flock, in fact.", "Smells like a farm. I was never at the farm."])
    o.r('hang_his_weight_on_one_end', 'Gripping one end in his bill and hanging his whole weight back from it to test the knit', 20, 'none',
        [k(.12, 'belly', x=.9, y=1.2, b=.5), k(.3, 'belly', x=-.3, y=1, b=1.3, mark='hnn'), k(.5, 'thigh', x=-.8, y=.9, b=1.6, l=1, r=1, w=.6, mark='HNN'), k(.7, 'thigh', x=-.6, y=.8, b=1.3, w=.4), k(.88, eye='^')],
        [], g='test', act=('test', 'ends'), prefer=['curious', 'grown'], obj=[(.3, dict(wy=.3)), (.5, dict(wy=.5)), (.75, dict(wy=0))], say=["Holds. Tough knit. Unlike me.", "Hung off it like a bat. A heavy bat."])
    o.r('judge_the_weight_of_a_loop', 'Hefting a loop of the collar between both wings and bobbing it to judge the weight', 16, 'wing',
        [k(.12, 'neck', reach=.5, x=-.1, y=.6, b=.5), k(.3, 'shoulder', reach=1, x=-.2, y=.2, b=-.2, mark='hup'), k(.46, 'nape', reach=1, x=-.2, y=.8, b=.8, l=1), k(.62, 'shoulder', reach=1, x=-.2, y=.2, b=-.2), k(.8, eye='-', mark='hm')],
        [], g='test', act=('weigh', 'wraps'), prefer=['curious'])
    o.r('pinch_the_wool_to_see_how_thick', 'Pinching the thick wool between his bill and wing tip to see how deep the knit goes', 18, 'wing',
        [k(.12, 'cheek', reach=.5, x=-.3, y=.5, b=.3), k(.3, 'cheek', reach=1, x=-.8, y=.9, b=.6, mark='nnk'), k(.5, 'shoulder', reach=1, x=-.9, y=.9, b=.7, l=1), k(.7, 'neck', reach=1, x=-.5, y=.7, b=.5, r=1), k(.88, eye='o', mark='whoa')],
        [], g='test', act=('measure', 'wool'), prefer=['curious'], say=["Two fingers thick. I have no fingers.", "Thick. Like a cheese rind but kind."])
    o.r('press_an_ear_to_the_frozen_cable', 'Pressing his ear against the frozen cable to hear the ice crackle in it', 18, 'none',
        [k(.15, x=.2, y=.6, b=.4), k(.32, 'cheek', x=-.6, y=1.2, b=.8, eye='-'), k(.52, 'cheek', x=-.6, y=1.2, b=.9, l=1, eye='-', mark='crk'), k(.7, 'cheek', x=-.7, y=1.3, b=.9, mark='crkk'), k(.88, x=-.6, y=-.6, b=-.2, w=.4, eye='O')],
        [], g='test', act=('listen', 'cables'), when=['frost>.3'], prefer=['curious'])
    # ---------------- rest
    o.r('nap_with_his_head_in_the_collar', 'Napping with his head sunk deep in the collar loop and the ends in a heap', 28, 'none',
        [k(.15, x=-.2, y=.5, b=.4), k(.4, 'neck', x=-1.1, y=2.4, b=1.6, eye='-'), k(.7, 'nape', x=-1.2, y=2.7, b=2, w=.3, eye='-', mark='zzz'), k(.9, x=.2, y=.2, b=.3, eye='O')],
        [], g='rest', act=('nap', 'collar'), shown='head', when=['tired'])
    o.r('sulk_with_his_chin_in_the_wraps', 'Sulking with his chin dropped into the wraps and the heavy ends hanging limp', 20, 'none',
        [k(.15, x=-.4, y=.4, b=.3, l=1), k(.4, 'throat', x=-.9, y=1.8, b=1.2, eye='-'), k(.7, 'throat', x=-1, y=2, b=1.4, w=.3, eye='-', mark='hmph'), k(.9, x=-.2, y=.3, b=.4)],
        [], g='rest', act=('sulk', 'ends'), when=['sad'], obj=[(.4, dict(sag=.4)), (.7, dict(sag=.7)), (.92, dict(sag=0))], say=["Not in the mood. The scarf agrees. It's heavy with it.", "You can all go and stuff a sock."])
    o.r('stamp_both_feet_and_wait_in_the_cold', 'Waiting out the cold with his bill buried to the nostrils, stamping to keep his feet alive', 24, 'none',
        [k(.15, x=-.2, y=.8, b=.4, l=1), k(.35, 'throat', x=-.7, y=1.5, b=.8, r=1, mark='stp'), k(.55, 'throat', x=-.6, y=1.4, b=.8, l=1, mark='stp'), k(.75, 'throat', x=-.6, y=1.5, b=.8, r=1, mark='stp'), k(.9, eye='-')],
        [], g='rest', act=('wait', 'scarf'), when=['cold'], prefer=['lonely'])
    o.r('drape_an_end_over_a_cold_foot', 'Draping the end of the scarf over one cold foot and shuffling it warm', 22, 'wing',
        [k(.12, 'thigh', reach=.5, x=.2, y=.6, b=.5), k(.3, 'foot_l', reach=1, x=.4, y=1.3, b=1.1, l=1, mark='ahh'), k(.5, 'foot_l', reach=1, x=.3, y=1.5, b=1.3, l=1, eye='-'), k(.7, 'foot_l', reach=.8, x=.3, y=1.3, b=1.1, l=1), k(.88, eye='^')],
        [], g='rest', act=('warm', 'foot'), when=['cold'], prefer=['tired'], obj=[(.3, dict(sag=.5)), (.6, dict(sag=.8)), (.85, dict(sag=0))], say=["Foot warm. Other foot offended.", "A scarf is also a sock, if you shut up about it."])
    # ---------------- weather
    o.r('shake_the_snow_out_of_the_ends', 'Shaking the snow out of both ends, wings out, till it flies off in clumps', 16, 'none',
        [k(.12, x=.4, y=.9, b=.6, l=1), k(.28, 'belly', x=1, y=.3, b=-.7, w=1, r=1, mark='brrr'), k(.44, 'thigh', x=-1, y=.3, b=-.9, w=1, l=1, mark='fff'), k(.6, 'belly', x=1, y=.3, b=-.7, w=1, r=1), k(.76, 'thigh', x=-.6, y=.5, b=-.4, w=.7), k(.9, eye='-')],
        [(.44, 'flick')], g='weather', act=('shake', 'ends'), when=['snow>.4'], obj=[(.3, dict(flap=.8)), (.7, dict(flap=.8)), (.88, dict(flap=0))])
    o.r('turn_his_back_to_the_gale', 'Turning his back to the gale and bracing, the heavy ends barely lifting off his chest', 22, 'none',
        [k(.12, x=-.4, y=.3, b=.5), k(.3, 'back', x=-1.2, y=.9, b=1.3, w=.4, l=1), k(.55, 'back', x=-1.4, y=1.2, b=1.5, w=.3, r=1, eye='>', mark='fwoom'), k(.8, x=-.5, y=.5, b=.6, eye='-')],
        [], g='weather', act=('brace', 'ends'), when=['windy'], obj=[(.15, dict(flap=.3)), (.4, dict(flap=.6)), (.7, dict(flap=.6)), (.9, dict(flap=0))])
    o.r('hunch_through_the_downpour_with_the_collar_up', 'Hunching with the thick collar up past his ears while the downpour hammers the wool', 32, 'none',
        [k(.12, 'neck', x=.2, y=.4, b=.4), k(.3, 'cheek', x=-.7, y=1.4, b=1.3, eye='-', mark='patter'), k(.55, 'cheek', x=-.9, y=1.7, b=1.6, w=.3, eye='-', mark='drip'), k(.8, 'neck', x=-.4, y=1, b=1.1, eye='>')],
        [], g='weather', act=('shelter', 'scarf'), when=['storm', 'wet'], obj=[(.3, dict(wy=-.4)), (.6, dict(wy=-.5)), (.9, dict(wy=0))])
    o.r('wring_the_meltwater_from_the_fringe', 'Wringing the cold meltwater out of a dripping fringe with both wings', 18, 'wing',
        [k(.12, 'thigh', reach=.5, x=.2, y=.8, b=.5), k(.3, 'thigh', reach=1, x=.2, y=1.4, b=1, l=1, mark='squeeze'), k(.5, 'foot_r', reach=1, x=.2, y=1.6, b=1.2, r=1, mark='drip'), k(.7, 'foot_r', reach=1, x=.2, y=1.7, b=1.3), k(.88, y=.2, eye='-')],
        [(.5, 'wring')], g='weather', act=('squeeze', 'fringe'), when=['soaked>.3'], say=["Wrung. A whole puddle came out of a tassel.", "Freezing meltwater down my leg. Splendid."])
    o.r('breathe_on_the_frozen_cable', 'Huffing long breaths onto the frozen cable until it creaks and gives', 20, 'none',
        [k(.12, 'belly', x=.7, y=1, b=.5), k(.3, 'belly', x=1.2, y=1.4, b=.8, mark='haaa'), k(.5, 'throat', x=1.3, y=1.4, b=.9, mark='haaa'), k(.7, 'throat', x=1.2, y=1.3, b=.8, eye='-', mark='crk'), k(.88, eye='^')],
        [(.5, 'crack')], g='weather', act=('blow', 'frost'), when=['frost>.3'], prefer=['curious'])
    # ---------------- show
    o.r('turn_slowly_to_show_off_the_cables', 'Turning slowly with a wing swept along the cable twists like a model on a plinth', 16, 'wing',
        [k(.15, 'throat', reach=.6, x=-.2, y=-.4, b=-.3, l=1), k(.4, 'belly', reach=1, x=.3, y=-.7, b=-.7, w=.5), k(.65, 'thigh', reach=1, x=-.3, y=-.8, b=-.9, r=1, mark='ta-da'), k(.85, reach=0, y=.4, b=.3, eye='^')],
        [], g='show', act=('present', 'cables'), prefer=['happy'], obj=[(.4, dict(wx=.2)), (.65, dict(wx=-.2)), (.88, dict(wx=0))])
    o.r('bow_with_the_heavy_ends_swinging', 'Bowing so low that the heavy ends swing forward and thud into the ground', 14, 'none',
        [k(.15, x=-.5, y=-.8, b=-.6, w=.6, l=1), k(.4, 'thigh', x=1.4, y=1.8, b=1.1, w=.9, r=1), k(.65, 'foot_r', x=1.5, y=2.1, b=1.4, w=1, mark='thud'), k(.88, x=-.4, y=-.7, b=-.4, w=.3, eye='^')],
        [], g='show', act=('bow', 'ends'), prefer=['happy'], obj=[(.4, dict(sag=.5)), (.65, dict(sag=.8)), (.9, dict(sag=0))])
    o.r('pop_the_collar_and_pose', 'Popping the thick collar up round his bill, chin high, wing on hip, giving it attitude', 18, 'wing',
        [k(.12, 'neck', reach=.4, x=-.2, y=.3, b=.3), k(.35, 'cheek', reach=1, x=-.4, y=-1, b=.6, w=.3, l=1), k(.6, 'cheek', reach=1, x=-.3, y=-1.3, b=.8, w=1, r=1, mark='...'), k(.85, y=.3, b=.2, eye='^')],
        [], g='show', act=('pose', 'collar'), prefer=['happy'], obj=[(.35, dict(wy=-.4)), (.6, dict(wy=-.5)), (.88, dict(wy=0))])
    o.r('argue_with_the_wraps', 'Arguing with the wraps that keep riding up, jabbing at them with his bill', 16, 'none',
        [k(.15, x=.5, y=.5, b=.2, eye='>'), k(.3, 'neck', x=1.3, y=1.1, b=.7, w=1, mark='OI'), k(.5, 'nape', x=-1, y=-.2, b=-.3, w=.4, l=1), k(.7, 'neck', x=1.4, y=1.2, b=.8, w=1, r=1, mark='OI!'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'wraps'), prefer=['grumpy'], say=["Stay down. I mean it. It doesn't.", "Wool: 1. Neck: 0. Dignity: gone."])
    o.r('hum_a_carol_into_the_collar', 'Singing a carol into the collar until it comes out as a thick muffled hum', 20, 'none',
        [k(.12, x=.2, y=.3, b=.3), k(.3, 'neck', x=-.9, y=1.4, b=.7, mark='hmm'), k(.5, 'neck', x=-.9, y=1.2, b=.6, l=1, w=.4, mark='hm hm'), k(.7, 'throat', x=-1, y=1.3, b=.7, r=1, w=.5, mark='HMMM'), k(.88, eye='^')],
        [(.5, 'fun')], g='show', act=('sing', 'collar'), prefer=['happy'], say=["Deck the halls. Mumble. Mumble. Wool.", "A choir of one, muffled."])
    # ---------------- mishap
    o.r('tread_on_a_heavy_end', 'Treading on a heavy end and skidding forward with it dragging at his neck', 16, 'none',
        [k(.15, 'foot_r', x=.4, y=.5, b=.3, r=1), k(.3, x=.6, y=-.3, b=-.7, w=1, l=1, r=1, eye='O', mark='WHA'), k(.5, x=1.3, y=1.9, b=1.6, w=.8, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'ends'), prefer=['young'])
    o.r('chin_jammed_in_the_high_collar', 'Jamming his chin in the high collar and having to turn his whole body to look anywhere', 18, 'none',
        [k(.15, 'cheek', x=-.3, y=.6, b=.3), k(.35, 'cheek', x=-1, y=1.8, b=1.2, eye='O', mark='mmf'), k(.55, x=-1, y=1.8, b=1.2, w=.5, l=1, r=1, eye='@', mark='mrrf'), k(.75, 'cheek', x=-.5, y=.5, b=.5, w=.3, eye='-'), k(.9, y=.3, eye='^')],
        [], g='mishap', act=('stuck', 'collar'), prefer=['grumpy'], obj=[(.35, dict(wy=-.5)), (.6, dict(wy=-.6)), (.85, dict(wy=0))], say=["Can't turn my head. Hello, side of a hedge.", "Stuck in a scarf. Smothered by love and wool."])
    o.r('whacked_in_the_face_by_his_own_end', 'Turning too fast and getting whacked in the face by a swinging end', 14, 'none',
        [k(.15, x=.4, y=.3, b=.3), k(.3, x=1, y=-.4, b=-.5, w=.6, eye='O'), k(.45, 'cheek', x=-1.2, y=.8, b=.7, eye='@', mark='WHUMP'), k(.7, 'cheek', x=-.6, y=.4, b=.4, w=.4, eye='>'), k(.9, y=.3, eye='-')],
        [], g='mishap', act=('knock', 'ends'), prefer=['young'], obj=[(.3, dict(flap=.8)), (.45, dict(flap=1)), (.7, dict(flap=0))], say=["Hit myself with a scarf. Weapon: knitted.", "Assaulted by wool. Crime scene: me."])
    o.r('shrug_the_scarf_off_and_haul_it_back', 'Feeling the whole scarf slide off his neck, flop to the ground, and hauling it up again', 22, 'none',
        [k(.12, x=.2, y=.4, b=.4), k(.28, 'shoulder', x=-.6, y=.9, b=.8, eye='O', mark='oh'), k(.44, 'back', x=-.4, y=1.2, b=1.2, eye='@', mark='flop'), k(.6, 'neck', x=.9, y=1.5, b=1.1, l=1), k(.76, 'neck', x=.4, y=.5, b=.5, mark='hup'), k(.9, eye='-')],
        [], g='mishap', act=('lift', 'scarf'), when=['wraps<.4'],
        obj=[(.2, dict(off=0)), (.34, dict(off=1)), (.46, dict(off=1, ix=1)), (.6, dict(off=1, ix=1)), (.7, dict(off=1, hold=1)), (.84, dict(off=0))])
    # @@END scarf_winter
    return done(o)


def ancient_amulet():
    # Host trophy_case (106 cols x 77 rows, 7.2 px a row, standing line row 75). Centre door seam col 53 rows 14-60; lowest shelf ledge row 61-62 (93-100 px),
    # three `[____]` stands on it at row 60 (108 px); trim bars rows 62 and 65 (93 and 72 px); (=) plates on the left frame rows 63/53/43/33 (86/158/230/302 px);
    # base slats every fifth column rows 67-71 (57-28 px) with an `o` stud at each end (35 px); bottom rail row 72 (21 px). The thing itself is `item`
    # (115 px, the lowest slot). The amulet drawing: a cord loop above, rays of dots round a medallion with an eye in the middle.
    P = pm('trophy_case')
    o = Obj('ancient_amulet', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), dull=(.3, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('dull', 'rate', .0004, 'always')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)], shine=[('dull', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)], smudge=[('obj.dirt', 'add', .15)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_c=P(86, 69), stud_l=P(10, 70), stud_r=P(95, 70), rail=P(53, 72), trim_lo=P(50, 65), trim_hi=P(50, 62),
                         sill=P(40, 63), ledge=P(30, 61), stand_l=P(22, 60), plate_lo=P(11, 63), plate_hi=P(11, 53), seam_lo=P(53, 58), frame_r=P(92, 57)))
    # ---------------- care
    o.r('wipe_the_breath_mist_off', 'Wiping the breath mist off the glass in wide arcs with the side of a wing', 16, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.2), k(.3, 'sill', reach=1, x=.7, y=-.4, b=-.3, w=.3), k(.5, 'trim_hi', reach=1, x=.7, y=-.5, b=-.3), k(.7, 'stand_l', reach=1, x=.6, y=-.6, b=-.4, l=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['grown'], say=["Clear. Now the amulet can see me.", "Mist gone. Evidence gone."])
    o.r('buff_the_nose_prints_off', 'Buffing the nose prints off the lower pane with the tip of a wing', 18, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.3, y=-.2, b=.2), k(.3, 'trim_lo', reach=1, x=.6, y=-.3, b=.4, mark='squeak'), k(.5, 'sill', reach=1, x=.6, y=-.3, b=.4, r=1), k(.7, 'frame_r', reach=1, x=.6, y=-.3, b=.5, l=1), k(.88, y=-.2, eye='-')],
        [(.5, 'buff')], g='care', act=('wipe', 'prints'), when=['prints>.3'], prefer=['curious'])
    o.r('sweep_the_ledge_with_a_twig', 'Sweeping the dust off the lowest ledge and round the stand with the end of a twig', 18, 'twig',
        [k(.12, 'ledge', reach=.6, x=.3, y=.2), k(.3, 'ledge', reach=1, x=.5, y=.4, b=.3, mark='shff'), k(.5, 'stand_l', reach=1, x=.5, y=.3, b=.4), k(.7, 'trim_hi', reach=1, x=.5, y=.4, b=.3, l=1), k(.88, eye='^')],
        [(.5, 'clean')], g='care', act=('sweep', 'ledge'), when=['obj_dirt>.3'])
    o.r('scrub_the_frame_plates', 'Scrubbing the plates on the frame with the end of a twig, low plate and then the high one', 20, 'twig',
        [k(.12, 'plate_lo', reach=.6, x=.3, y=.2), k(.3, 'plate_lo', reach=1, x=.5, y=.4, b=.3, mark='sqk'), k(.5, 'plate_hi', reach=1, x=.4, y=-.6, b=-.4, mark='sqk'), k(.7, 'plate_hi', reach=1, x=.4, y=-.7, b=-.5, l=1), k(.88, eye='-')],
        [(.5, 'clean')], g='care', act=('scrub', 'plates'), when=['obj_dirt>.4'], ages=GROWN)
    o.r('rub_the_end_studs_bright', 'Rubbing the two end studs of the base with his bill till they shine', 18, 'none',
        [k(.12, 'stud_l', x=1.2, y=1, b=.5, mark='rub'), k(.3, 'stud_l', x=1, y=.6, b=.7, l=1), k(.55, 'stud_r', x=1.3, y=1, b=.5, r=1, mark='rub'), k(.75, 'stud_r', x=1.1, y=.8, b=.6), k(.9, eye='^')],
        [(.55, 'shine')], g='care', act=('polish', 'studs'), when=['dull>.4'], prefer=['happy'])
    # ---------------- use
    o.r('squash_his_bill_against_the_glass', 'Squashing his bill flat against the lower pane for a closer look', 16, 'none',
        [k(.15, x=.6, y=-.3, b=.2, l=1), k(.35, 'sill', x=1.5, y=-.6, b=.4, eye='O', mark='mmf'), k(.6, 'sill', x=1.6, y=-.8, b=.5, r=1, eye='O'), k(.85, x=-.3, y=-.2, w=.3, eye='-')],
        [(.35, 'nose')], g='use', act=('press', 'glass'), prefer=['curious', 'young'])
    o.r('huff_a_fog_onto_the_glass', 'Huffing a long breath at the glass until the pane fogs up', 14, 'none',
        [k(.15, 'trim_lo', x=1.3, y=-.4, b=-.3), k(.35, 'trim_hi', x=1.4, y=-.6, b=-.5, mark='haaa'), k(.6, 'trim_hi', x=1.4, y=-.6, b=-.5, w=.4, eye='O'), k(.85, x=-.3, y=-.2, eye='^')],
        [(.35, 'huff')], g='use', act=('blow', 'glass'), prefer=['curious'])
    o.r('count_the_rays_with_a_twig', 'Counting the rays round the medallion with the point of a twig, one dot at a time', 22, 'twig',
        [k(.12, 'item', reach=.6, x=.3, y=-.4), k(.3, 'item', reach=1, x=.6, y=-.8, b=.3, mark='1'), k(.48, 'item', reach=1, x=.5, y=-.9, b=.4, l=1, mark='2'), k(.66, 'item', reach=1, x=.6, y=-1, b=.3, r=1, mark='3'), k(.86, eye='-', mark='lots')],
        [], g='use', act=('count', 'rays'), prefer=['curious'], say=["Twenty-odd rays. One amulet. Poor ratio.", "Lost count at nine. Blamed the amulet."])
    o.r('lift_it_out_to_look_closer', 'Lifting the amulet out of its place in his bill and turning it in the light', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=.9, y=-1, b=-.4), k(.58, 'item', x=.7, y=-.6, eye='O'), k(.72, 'item', x=1.2, y=-.5), k(.88, eye='^')],
        [], g='use', act=('lift', 'amulet'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.76, dict(hold=1)), (.86, dict(hold=0))],
        say=["Out of the case. Sirens: none. Result.", "Held it up. It caught the light and my ego."])
    o.r('swing_it_gently_by_the_cord', 'Dangling the amulet by its cord in his bill and watching the medallion swing', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.5, b=.2), k(.4, 'item', x=1.5, y=-.4, b=.3, l=1), k(.55, 'item', x=1.5, y=-.4, b=.3, r=1, eye='O'), k(.7, 'item', x=1.3, y=-.5, b=.2), k(.88, eye='-')],
        [(.55, 'fun')], g='use', act=('rock', 'cord'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=0))])
    o.r('mouth_the_cord_and_spit', 'Mouthing the cord of the lifted amulet to taste it and spitting out the fluff', 16, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.45, 'item', x=1.1, y=-.8, b=.4, eye='-', mark='...'), k(.62, 'item', x=-.4, y=-.9, b=-.4, w=.8, l=1, eye='>', mark='ptui'), k(.8, 'item', x=1, y=-.5, b=.2), k(.9, eye='-')],
        [(.62, 'smudge')], g='use', act=('taste', 'cord'), ages=GROWN, prefer=['young', 'curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.7, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))], say=["Old. Dusty. Tastes like a museum's armpit.", "Ancient. Tastes ancient. Spat."])
    o.r('hold_it_to_his_ear', 'Holding the lifted amulet up beside his ear to hear whether it hums', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.45, 'item', x=-.3, y=-.7, b=.5, eye='-'), k(.62, 'item', x=-.4, y=-.7, b=.6, l=1, eye='-', mark='...'), k(.8, 'item', x=1, y=-.5, b=.2, eye='O'), k(.9, eye='^')],
        [], g='use', act=('listen', 'amulet'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.7, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))])
    o.r('rub_it_bright_on_his_chest_feathers', 'Rubbing the lifted amulet over his chest feathers until the medallion shines', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.2), k(.4, 'item', x=.4, y=.5, b=.8, l=1, mark='rub'), k(.55, 'item', x=.3, y=.7, b=.9, r=1, mark='rub'), k(.72, 'item', x=1, y=-.4, b=.2), k(.88, eye='^')],
        [(.55, 'clean')], g='use', act=('polish', 'medallion'), ages=GROWN, when=['obj_dirt>.3'],
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Buffed on my own chest. The amulet got lucky.", "Shiny. Smells like duck. Fair trade."])
    # ---------------- play
    o.r('hop_up_at_the_ledge', 'Hopping up at the lowest ledge to rap the glass above it, again and again', 14, 'none',
        [k(.15, x=.5, y=.3, b=.5), k(.3, x=.3, y=-.6, b=-.9, w=.8), k(.42, 'ledge', x=1.2, y=-.8, b=-1, w=.5, mark='tk'), k(.6, x=.2, y=.4, b=.8, l=1, eye='@', mark='thud'), k(.85, eye='-')],
        [], g='play', act=('hop', 'ledge'), prefer=['young', 'happy'])
    o.r('drum_along_the_slats', 'Drumming his bill along the base slats from the left end to the right', 16, 'none',
        [k(.12, 'slat_a', x=1.3, y=1.2, b=.4, mark='tk'), k(.3, 'stud_l', x=1.3, y=1.3, b=.5, mark='tk'), k(.5, 'rail', x=1.3, y=1.3, b=.5, l=1, mark='tk'), k(.7, 'slat_c', x=1.3, y=1.2, b=.4, r=1, mark='tk'), k(.9, eye='^')],
        [(.5, 'fun')], g='play', act=('drum', 'slats'), prefer=['happy', 'young'])
    o.r('sprint_the_length_of_the_rail', 'Sprinting the length of the bottom rail from stud to stud, tapping each on the way', 18, 'none',
        [k(.1, 'stud_l', x=.5, y=.6, b=.5, l=1), k(.3, 'rail', x=1.1, y=.5, b=-.4, r=1, w=.4), k(.5, 'rail', x=1.2, y=.5, b=-.5, l=1, w=.5), k(.7, 'slat_c', x=1.1, y=.5, b=-.4, r=1), k(.88, 'stud_r', x=.5, y=.6, b=.5, eye='^', mark='pip')],
        [], g='play', act=('race', 'rail'), prefer=['young', 'happy'])
    o.r('shoulder_the_case_to_see_if_it_budges', 'Putting his shoulder to the foot of the case and shoving to see if it budges', 18, 'none',
        [k(.12, x=.2, y=.4, b=.4), k(.3, 'slat_a', x=1.1, y=.5, b=1.2, l=1, mark='hnng'), k(.55, 'slat_a', x=1.3, y=.7, b=1.5, r=1, mark='HNNG'), k(.75, x=-.4, y=.2, b=.5, w=.5, eye='>'), k(.9, eye='-')],
        [], g='play', act=('push', 'case'), prefer=['grumpy', 'grown'], say=["Not an inch. Solid case. Rude.", "Heavier than it looks. So am I."])
    o.r('boot_the_bottom_rail', 'Booting the bottom rail like a football and hopping about clutching the sore foot', 14, 'none',
        [k(.15, x=.2, y=.3, b=.4, l=1), k(.3, 'rail', x=.3, y=.5, b=-.2, l=1, mark='thwk'), k(.5, x=-.5, y=-.2, b=-.6, r=1, w=.6, eye='O', mark='OW'), k(.7, x=.2, y=.3, b=.4, r=1), k(.88, eye='-')],
        [], g='play', act=('kick', 'rail'), prefer=['grumpy'], say=["That's for the glass. And the price.", "Kicked the rail. Foot hurts. Rail won."])
    o.r('peek_round_the_right_stud', 'Peeking round the right stud, ducking back out of sight and peeking again', 18, 'none',
        [k(.12, 'stud_r', x=.9, y=.6, b=.5), k(.28, 'stud_r', x=1.6, y=.9, b=1.3, eye='o'), k(.44, x=-.3, y=.2, b=.4, eye='-'), k(.62, 'stud_r', x=1.6, y=.9, b=1.4, l=1, eye='o', mark='!'), k(.8, x=-.3, y=-.2, b=.2, w=.4, eye='^')],
        [], g='play', act=('seek', 'stud'), prefer=['young', 'curious'])
    # ---------------- test
    o.r('knock_on_the_base_for_the_hollow', 'Knocking once on a base slat and cocking his head to hear it ring', 14, 'none',
        [k(.15, x=.5, y=.5, b=.3), k(.35, 'slat_c', x=1.4, y=1.4, b=.7, mark='tok'), k(.55, x=-.6, y=-.6, b=-.2, w=.4, eye='O'), k(.8, x=.3, y=.4, b=.2, eye='-')],
        [], g='test', act=('knock', 'base'), prefer=['curious'], say=["Hollow. Like my wallet.", "Nobody inside. Only the amulet, upstairs."])
    o.r('ear_against_the_slats', 'Pressing his ear against the slats to hear if the amulet hums above', 18, 'none',
        [k(.15, x=.5, y=.4, b=.3), k(.4, 'slat_a', x=1.2, y=.8, b=.8, eye='-'), k(.65, 'slat_a', x=1.2, y=.6, b=1, l=1, eye='-', mark='...'), k(.85, x=-.5, y=-.4, w=.4, eye='O')],
        [], g='test', act=('listen', 'base'), prefer=['curious'])
    o.r('measure_the_case_with_a_wing', 'Measuring the foot of the case against his wing, stud to stud', 20, 'wing',
        [k(.12, 'stud_l', reach=.6, x=.3, y=.4, b=.2), k(.3, 'slat_a', reach=1, x=.4, y=.5, b=.4), k(.5, 'rail', reach=1, x=.4, y=.5, b=.4, l=1), k(.7, 'slat_c', reach=1, x=.4, y=.5, b=.4, r=1), k(.88, 'stud_r', reach=.8, x=.2, y=.4, b=.3, eye='-', mark='hm')],
        [], g='test', act=('measure', 'case'), prefer=['curious'])
    o.r('sniff_along_the_slats', 'Running his bill along the slats, sniffing for something old', 16, 'none',
        [k(.12, 'slat_c', x=1, y=.9, b=.5), k(.35, 'rail', x=1.1, y=1.2, b=.6), k(.58, 'slat_a', x=1.2, y=1.1, b=.6, mark='sniff'), k(.8, x=-.3, y=-.3, w=.4, eye='>'), k(.92, eye='^')],
        [], g='test', act=('sniff', 'slats'), prefer=['curious'])
    o.r('lick_the_polished_rail', 'Licking the polished bottom rail to test whether it is real brass', 14, 'none',
        [k(.15, 'rail', x=1.2, y=1.6, b=.8), k(.35, 'rail', x=1.4, y=1.8, b=1, eye='-', mark='...'), k(.55, x=-.7, y=-.6, b=-.3, w=.7, l=1, eye='>', mark='bleh'), k(.8, y=.5, b=.3, eye='-')],
        [], g='test', act=('taste', 'rail'), prefer=['curious', 'young'], say=["Tastes like the inside of a coin.", "Not brass. Disappointing. Still licked."])
    o.r('rattle_the_door_seam', 'Heaving at the door seam with his shoulder to see whether the case is locked', 18, 'none',
        [k(.12, x=.3, y=-.2, b=.3), k(.3, 'seam_lo', x=1, y=-.6, b=.8, mark='hnng'), k(.5, 'seam_lo', x=1.2, y=-.7, b=1, l=1, mark='rattle'), k(.7, x=-.4, y=-.2, b=.3, w=.5, eye='>'), k(.88, eye='-')],
        [], g='test', act=('shake', 'doors'), ages=GROWN, prefer=['curious', 'grumpy'])
    o.r('squint_at_his_own_face_beside_it', 'Squinting at his own face in the glass, held up beside the medallion to compare', 18, 'none',
        [k(.15, x=.4, y=-.4, b=.2), k(.32, x=.9, y=-.6, b=.4, eye='O'), k(.5, x=.6, y=-.7, b=.2, eye='>', mark='hm'), k(.68, x=1, y=-.6, b=.4, w=.6, eye='^'), k(.86, x=.2, y=-.2, eye='-')],
        [], g='test', act=('compare', 'reflection'), prefer=['curious', 'happy'], say=["I am more handsome. It is more expensive.", "Same eyes, near enough. Mine are cheaper."])
    # @@PLAY2
    o.r('crane_up_at_it_left_right_and_straight_up', 'Craning his neck up at the amulet, left then right then straight up', 20, 'none',
        [k(.15, x=.3, y=-.8, b=-.2), k(.35, x=.9, y=-1.2, b=-.4, eye='O'), k(.55, x=-.9, y=-1.2, b=-.4, l=1, eye='O'), k(.8, x=0, y=-1.6, b=-.6, w=.4, eye='^', mark='ooh')],
        [], g='use', act=('peer', 'amulet'), prefer=['curious', 'young'])
    # ---------------- rest
    o.r('doze_off_with_his_bill_at_the_rail', 'Dozing off with his bill resting at the bottom rail and the amulet glinting overhead', 28, 'none',
        [k(.15, x=.6, y=.5, b=.3), k(.4, 'rail', x=.5, y=1.5, b=1.2, eye='-'), k(.7, 'rail', x=.5, y=1.8, b=1.4, eye='-', mark='zzz'), k(.9, x=-.3, y=-.3, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'base'), when=['tired'], say=["Guarding the amulet. Eyes shut. Tactic.", "Wake me when it opens."])
    o.r('lean_a_shoulder_on_the_end_stud', 'Leaning his shoulder against the end stud and sighing at the case', 18, 'none',
        [k(.15, x=.5, y=.2, b=.2, l=1), k(.4, 'stud_r', x=-.9, y=.5, b=1, w=.4), k(.7, 'stud_r', x=-1, y=.7, b=1.3, eye='-', mark='sigh', r=1), k(.9, x=.3, y=.2, b=.3)],
        [], g='rest', act=('lean', 'stud'), prefer=['tired', 'sad'])
    o.r('sulk_with_his_back_to_the_slats', 'Turning his tail to the case and sulking with his back against the slats', 22, 'none',
        [k(.15, x=-.9, y=.1, b=.2, l=1), k(.4, 'slat_a', x=-1.5, y=.9, b=1.2, w=.2, eye='-'), k(.7, 'slat_a', x=-1.6, y=1.1, b=1.4, w=.7, r=1, eye='-', mark='hmph'), k(.9, x=-.4, y=.4, b=.5)],
        [], g='rest', act=('sulk', 'case'), when=['sad'])
    o.r('sit_square_and_wait_for_the_doors', 'Sitting square in front of the doors, waiting for somebody to open them', 24, 'none',
        [k(.15, x=.4, y=.1, b=.4, l=1, eye='O'), k(.4, x=.1, y=.7, b=1.3, eye='-'), k(.65, x=.3, y=-.7, b=1.3, w=.5, eye='O', mark='...'), k(.85, x=.1, y=.2, b=.6, r=1, eye='-')],
        [], g='rest', act=('wait', 'doors'), prefer=['curious', 'lonely'], say=["Any door now.", "I can wait. I have time and bread."])
    o.r('prop_his_chin_on_the_rail_and_stare', 'Propping his chin at the bottom rail and staring up at the amulet for a long time', 26, 'none',
        [k(.15, x=.5, y=.5, b=.8), k(.4, 'rail', x=1, y=1.6, b=1.6, eye='o'), k(.6, 'rail', x=1, y=1.7, b=1.7, eye='o', mark='...'), k(.85, x=.2, y=.4, b=.7, eye='-')],
        [], g='rest', act=('sit', 'rail'), prefer=['sad', 'lonely'])
    # ---------------- weather
    o.r('dry_the_rain_streaks_off_the_glass', 'Drying the rain streaks off the lower pane with a wing, top to bottom', 18, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.3, y=-.2), k(.3, 'sill', reach=1, x=.6, y=-.4, b=-.2, w=.3), k(.5, 'trim_lo', reach=1, x=.6, y=-.2, b=.3), k(.7, 'frame_r', reach=1, x=.5, y=-.2, b=.2, l=1), k(.88, eye='^')],
        [(.5, 'dry')], g='weather', act=('dry', 'glass'), when=['obj_wetness>.3'])
    o.r('huddle_against_the_foot_in_the_storm', 'Huddling against the foot of the case with his tail to the storm, rain drumming on the glass', 32, 'none',
        [k(.12, 'slat_a', x=-.3, y=.6, b=.9), k(.3, 'slat_a', x=-.7, y=1.2, b=1.5, w=.3, eye='-'), k(.58, 'slat_c', x=-.8, y=1.4, b=1.7, eye='-', mark='drip'), k(.82, 'slat_c', x=-.4, y=.8, b=1.1, eye='>')],
        [], g='weather', act=('brace', 'case'), when=['storm', 'wet'])
    o.r('warm_his_back_on_the_sunny_glass', 'Warming his back against the sun-heated foot of the case with his eyes shut', 24, 'none',
        [k(.15, x=-.3, y=.4, b=.5), k(.5, 'slat_c', x=-.6, y=.8, b=1.2, eye='-'), k(.7, 'slat_c', x=-.6, y=.9, b=1.4, eye='-', mark='mm'), k(.9, y=.2, b=.2, eye='^')],
        [], g='weather', act=('warm', 'case'), when=['sun'], prefer=['cold', 'tired'])
    o.r('follow_the_moonlight_up_the_medallion', 'Leaning back and following a thread of moonlight across the medallion, left to right', 22, 'none',
        [k(.15, 'stud_l', x=.1, y=-.4, b=.5), k(.35, 'stud_l', x=.3, y=-1.2, b=.9, eye='O'), k(.55, 'stud_l', x=.8, y=-1.6, b=1.1, l=1, eye='O', mark='ooh'), k(.78, x=0, y=-1, b=-.3, eye='-')],
        [], g='weather', act=('peer', 'glint'), when=['night'], prefer=['curious'], say=["Moon on the medallion. Moody. Good.", "It glints at night. Show-off."])
    # ---------------- show
    o.r('bow_low_at_the_foot_of_the_case', 'Bowing low at the foot of the case, bill brushing the bottom rail', 16, 'none',
        [k(.15, x=-.5, y=-.9, b=-.6, w=.6, l=1), k(.4, 'rail', x=1.4, y=1.7, b=1, w=.9, r=1), k(.65, 'rail', x=1.5, y=1.9, b=1.3, w=1, mark='...'), k(.88, x=-.4, y=-.7, b=-.4, w=.3, eye='^')],
        [], g='show', act=('bow', 'amulet'), prefer=['happy'])
    o.r('sweep_a_wing_up_toward_the_amulet', 'Sweeping a wing up toward the amulet for an invisible audience', 16, 'wing',
        [k(.15, reach=.2, x=-.4, y=-.6, b=-.5, l=1), k(.38, reach=1, x=.7, y=-.8, w=.4, b=-.7), k(.62, reach=1, x=.7, y=-1, w=.4, b=-.9, r=1, mark='ta-da'), k(.85, reach=0, y=.4, b=.3, eye='^')],
        [], g='show', act=('present', 'amulet'), prefer=['happy'], say=["Behold. Do not touch. I mean me.", "Ancient. Glittering. Mine, in spirit."])
    o.r('pose_beside_the_end_stud', 'Posing at the end of the case with one wing out, like a second trophy', 18, 'none',
        [k(.15, x=-.2, y=-.3, b=-.3, w=.6, r=1), k(.4, 'stud_l', x=.4, y=-1.1, b=.6, w=1, r=1), k(.7, 'stud_l', x=.4, y=-1.3, b=.8, w=.4, l=1, mark='...'), k(.9, y=.3, b=.2, eye='^')],
        [], g='show', act=('pose', 'case'), prefer=['happy'])
    o.r('argue_with_the_glass', 'Arguing with the glass, jabbing his bill at it and being ignored', 18, 'none',
        [k(.15, x=.9, y=.1, b=.3, eye='>'), k(.3, 'sill', x=1.6, y=-.5, b=.2, w=.6, mark='HEY'), k(.45, x=-.2, y=.3, b=.6, l=1, r=1), k(.7, 'sill', x=1.6, y=-.6, b=.1, w=1, mark='HEY!'), k(.9, y=.8, b=.7, eye='-')],
        [], g='show', act=('argue', 'glass'), prefer=['grumpy'], say=["Open up. I know you are in there.", "Glass: smug. Amulet: smugger."])
    o.r('shout_up_at_the_amulet_to_come_down', 'Shouting up at the amulet to come out, a wing cupped at his bill', 14, 'wing',
        [k(.15, x=.3, y=-.6, b=-.3), k(.35, reach=1, x=1.6, y=-2.2, b=-1.6, w=1, mark='OI'), k(.6, reach=.6, x=1.7, y=-2.3, b=-1.7, w=1, l=1, mark='OI'), k(.85, x=-.2, y=.2, eye='-')],
        [], g='show', far=True, act=('shout', 'amulet'), prefer=['grumpy'], say=["Come down here and say that.", "Nothing. It has a good lawyer."])
    o.r('serenade_the_amulet', 'Serenading the amulet with a long wobbly note and a wing over his heart', 22, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, reach=1, x=.3, y=-.9, b=-.3, w=.4, mark='laaa'), k(.5, reach=1, x=.4, y=-1.1, b=-.5, w=.5, l=1, mark='LAAA'), k(.7, reach=1, x=.3, y=-.8, b=-.2, r=1, mark='la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'amulet'), prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('stamp_at_the_rail_until_somebody_opens', 'Stamping at the rail until somebody opens up', 14, 'none',
        [k(.15, x=.3, y=.4, b=.3, l=1), k(.3, 'rail', x=.3, y=.6, b=.8, l=1, mark='STOMP'), k(.5, x=-.2, y=-.4, b=-.7, r=1, w=.6), k(.7, 'rail', x=.3, y=.6, b=.9, r=1, mark='STOMP'), k(.9, eye='-')],
        [], g='mishap', act=('stamp', 'rail'), prefer=['grumpy'])
    o.r('bump_the_case_in_the_dark', 'Bumping the case at night and bouncing back with a squeak', 14, 'none',
        [k(.15, x=.7, y=.1, b=.3), k(.3, 'slat_c', x=1.3, y=.3, b=.8, eye='O', mark='oof'), k(.5, x=-.9, y=-.4, b=-.7, w=.8, eye='@'), k(.8, x=.1, y=.3, b=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'case'), when=['night'])
    o.r('skid_on_the_wet_ground_at_the_foot', 'Skidding on wet ground at the foot of the case and ending flat against the rail', 16, 'none',
        [k(.15, 'slat_a', x=.4, y=.3, b=.4, l=1), k(.3, x=.5, y=-.4, b=-.8, w=1, l=1, r=1, eye='O', mark='WAH'), k(.5, 'rail', x=1.2, y=1.8, b=1.5, w=.8, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('slip', 'rail'), when=['obj_wetness>.3'], prefer=['young'])
    o.r('stuck_to_the_fogged_glass', 'Pressing his bill to the fogged glass so hard it sticks, and peeling it off with a pop', 22, 'none',
        [k(.15, x=.6, y=-.2, b=.2), k(.32, 'sill', x=1.6, y=-.6, b=.5, eye='O', mark='mmf'), k(.5, 'sill', x=1.6, y=-.6, b=.6, l=1, eye='@', mark='mrf'), k(.68, 'sill', x=1.8, y=-.6, b=.9, r=1, w=1, mark='POP'), k(.85, x=-1, y=.8, b=.8, eye='@')],
        [(.68, 'nose')], g='mishap', act=('stuck', 'glass'), when=['fog>.3'], prefer=['grumpy'], say=["Stuck. Own fault. Own breath.", "Pop. Nose still attached. Mostly."])
    o.r('topple_over_craning_too_far_back', 'Craning back on tiptoe to see the top of the case and toppling over backwards', 18, 'none',
        [k(.15, x=.2, y=-1, b=-.6), k(.35, x=-.2, y=-1.6, b=-1, w=.6, eye='O'), k(.55, x=-1.2, y=-2, b=-1.4, w=1, l=1, r=1, eye='@', mark='whoa'), k(.75, x=-1, y=1, b=1.8, w=.5, eye='@', mark='thud'), k(.9, y=.4, eye='-')],
        [], g='mishap', act=('balance', 'tiptoes'), prefer=['young'], say=["Looked up. Fell down. Physics is rude.", "Backwards. Elegant. No witnesses."])
    # ---------------- duets (a friend takes their own part)
    o.r('two_wipers_clear_the_mist', 'Clearing the breath mist off the glass with a friend, one wiping up and the other down', 20, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.2), k(.3, 'sill', reach=1, x=.6, y=-.4, b=-.3, w=.3), k(.5, 'trim_hi', reach=1, x=.6, y=-.5, b=-.4, l=1), k(.7, 'sill', reach=1, x=.5, y=-.3, b=-.2, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'glass'), when=['fog>.3'], prefer=['happy'],
        duo=[k(.12, 'trim_hi', reach=.6, x=.3, y=-.4, b=-.3), k(.3, 'trim_hi', reach=1, x=.6, y=-.5, b=-.4), k(.5, 'sill', reach=1, x=.5, y=-.3, b=-.2, r=1), k(.7, 'trim_hi', reach=1, x=.6, y=-.5, b=-.4, l=1), k(.88, eye='^')])
    o.r('take_turns_rapping_the_slats', 'Rapping the base slats in turn with a friend until they get a tune out of it', 22, 'none',
        [k(.12, 'slat_a', x=1.2, y=1.2, b=.4, mark='tk'), k(.28, x=-.3, y=-.3, b=-.3, w=.4), k(.44, 'slat_a', x=1.3, y=1.3, b=.5, l=1, mark='tk'), k(.6, x=-.3, y=-.3, b=-.3, w=.4), k(.76, 'slat_a', x=1.3, y=1.2, b=.4, r=1, mark='tk'), k(.9, eye='^')],
        [], g='play', act=('tap', 'slats'), prefer=['happy', 'young'],
        duo=[k(.2, x=-.3, y=-.3, b=-.3, w=.4), k(.36, 'slat_c', x=1.3, y=1.2, b=.5, mark='tk'), k(.52, x=-.3, y=-.3, b=-.3, w=.4), k(.68, 'slat_c', x=1.3, y=1.3, b=.5, l=1, mark='tk'), k(.84, 'slat_c', x=1.2, y=1.2, b=.4, r=1, mark='tk')])
    o.r('stand_back_to_back_and_compare_heights', 'Standing back to back with a friend at the foot of the case to see who is taller', 20, 'none',
        [k(.15, x=.2, y=-.3, b=-.2), k(.35, 'stud_l', x=-.5, y=-1, b=-.4, w=.4, eye='O'), k(.55, 'stud_l', x=-.5, y=-1.3, b=-.6, w=.5, l=1, mark='hm'), k(.75, x=.4, y=-.6, b=-.3, eye='>'), k(.9, eye='-')],
        [], g='test', act=('measure', 'heights'), prefer=['curious', 'happy'],
        duo=[k(.15, x=.2, y=-.3, b=-.2), k(.35, 'stud_l', x=-.5, y=-1.4, b=-.5, w=.4), k(.55, 'stud_l', x=-.5, y=-1.6, b=-.8, w=.5, r=1), k(.75, x=.4, y=-.8, b=-.3, eye='^'), k(.9, eye='-')])
    o.r('lift_it_out_to_show_a_friend', 'Lifting the amulet out in his bill and holding it up for a friend to inspect', 26, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=1.7, y=-1.8, b=-1.2, w=.6), k(.6, 'item', x=1.8, y=-1.9, b=-1.1, w=.8, eye='^'), k(.76, 'item', x=1.2, y=-.5), k(.9, eye='^')],
        [], g='show', act=('show', 'amulet'), ages=GROWN, prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.9, b=.2, eye='O'), k(.62, 'item', x=.9, y=-1, b=.3, eye='O', mark='ooh'), k(.8, x=-.2, y=-.4, eye='^')])
    # @@END ancient_amulet
    return done(o)


def lucky_charm():
    # Host trophy_case, same drawing as for the amulet (stands at row 60, 108 px; slats rows 67-71; studs row 70; rail row 72; trim rows 62 and 65; plates on the left
    # frame). The charm itself is `item` (115 px): a small cord loop above, a bar and a leafed charm hanging below it. What it IS here is luck: rituals, touching wood.
    P = pm('trophy_case')
    o = Obj('lucky_charm', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), gleam=(.4, 0, 1), wish=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('gleam', 'rate', -.0004, 'always'), ('wish', 'rate', -.0005, 'always')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)], shine=[('gleam', 'set', 1)],
                         wish=[('wish', 'add', .4)], clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_b=P(56, 69), slat_c=P(86, 69), stud_l=P(10, 70), stud_r=P(95, 70), rail=P(53, 72), trim_lo=P(50, 65),
                         sill=P(40, 63), ledge_m=P(62, 61), stand_m=P(47, 60), plate_lo=P(11, 63), seam_lo=P(53, 58)))
    # ---------------- care
    o.r('sweep_the_mist_away_in_long_strokes', 'Sweeping the breath mist off the pane in long strokes with the whole wing, sill to trim', 16, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.2, y=-.3, b=.2), k(.3, 'sill', reach=1, x=.7, y=-.5, b=-.4, w=.4, l=1), k(.5, 'trim_lo', reach=1, x=.8, y=-.5, b=-.5, w=.5), k(.7, 'sill', reach=1, x=.6, y=-.4, b=-.3, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('sweep', 'mist'), when=['fog>.3'], prefer=['grown'])
    o.r('scour_the_nose_prints_with_his_bill', 'Scouring the nose prints off the lower pane with the side of his bill, round and round', 18, 'none',
        [k(.12, x=.4, y=.2, b=.3), k(.3, 'trim_lo', x=1.2, y=-.2, b=.5, mark='sqk'), k(.5, 'sill', x=1.3, y=-.3, b=.6, l=1, mark='sqk'), k(.7, 'trim_lo', x=1.2, y=-.2, b=.5, r=1), k(.88, y=-.2, eye='-')],
        [(.5, 'buff')], g='care', act=('scrub', 'prints'), when=['prints>.3'], prefer=['curious'])
    o.r('rake_the_dust_off_the_stand', 'Raking the dust off the stand and ledge with the point of a twig, one stroke at a time', 20, 'twig',
        [k(.12, 'ledge_m', reach=.6, x=.3, y=.2), k(.3, 'ledge_m', reach=1, x=.6, y=.4, b=.3, mark='shff'), k(.5, 'stand_m', reach=1, x=.5, y=.3, b=.4), k(.7, 'ledge_m', reach=1, x=.6, y=.4, b=.3, l=1), k(.88, eye='^')],
        [(.5, 'clean')], g='care', act=('rake', 'stand'), when=['obj_dirt>.3'])
    o.r('polish_the_slats_one_by_one', 'Polishing the base slats one by one with the flat of a wing until they gleam', 22, 'wing',
        [k(.1, 'slat_a', reach=.6, x=.3, y=.8, b=.4), k(.28, 'slat_a', reach=1, x=.5, y=1, b=.7, l=1), k(.46, 'slat_b', reach=1, x=.5, y=1.1, b=.8, r=1), k(.64, 'slat_c', reach=1, x=.5, y=1, b=.7, l=1), k(.82, 'slat_c', reach=.6, x=.3, y=.8, b=.5), k(.92, eye='^')],
        [(.46, 'shine')], g='care', act=('polish', 'slats'), when=['gleam<.5'], prefer=['happy'])
    o.r('rub_the_frame_plate_bright', 'Rubbing the frame plate bright with the tip of a wing, low then high up the rim', 16, 'wing',
        [k(.12, 'plate_lo', reach=.6, x=.3, y=-.2, b=.2), k(.3, 'plate_lo', reach=1, x=.5, y=-.4, b=.4, mark='sqk'), k(.5, 'trim_lo', reach=1, x=.5, y=-.2, b=.3, l=1), k(.7, 'plate_lo', reach=1, x=.4, y=-.5, b=.5, r=1), k(.88, eye='-')],
        [(.5, 'shine')], g='care', act=('polish', 'plate'), when=['gleam<.5'], ages=GROWN)
    # ---------------- use
    o.r('knock_three_times_on_the_wood', 'Knocking three times on the wooden base for luck, bill to the middle slat', 16, 'none',
        [k(.12, 'slat_b', x=1.3, y=1.3, b=.4, mark='tok'), k(.3, x=-.4, y=-.3, b=-.2, w=.3), k(.44, 'slat_b', x=1.4, y=1.4, b=.5, l=1, mark='tok'), k(.6, x=-.4, y=-.3, b=-.2, w=.3), k(.76, 'slat_b', x=1.4, y=1.4, b=.5, r=1, mark='TOK'), k(.9, eye='^')],
        [(.76, 'wish')], g='use', act=('knock', 'slats'), when=['wish<.6'], prefer=['curious'], say=["Knocked on wood. Technically it is also a case.", "Three knocks. The charm owes me one."])
    o.r('press_his_brow_to_the_glass_and_wish', 'Pressing his brow against the pane with his eyes screwed shut, wishing hard', 18, 'none',
        [k(.15, x=.5, y=-.2, b=.3), k(.35, 'sill', x=1.3, y=-.7, b=.6, eye='-', mark='mmm'), k(.6, 'sill', x=1.4, y=-.8, b=.7, eye='-', mark='please'), k(.82, x=-.2, y=-.3, w=.3, eye='O')],
        [(.35, 'nose'), (.6, 'wish')], g='use', act=('press', 'glass'), when=['wish<.6'], prefer=['sad', 'lonely'], say=["Wished for bread. Specific bread. It heard.", "I wished. Nothing. Luck is slow today."])
    o.r('huff_on_the_pane_and_write_luck_in_the_mist', 'Huffing on the pane and pecking LUCK into the mist with his bill', 18, 'none',
        [k(.12, x=.3, y=-.2, b=.2), k(.3, 'trim_lo', x=1.3, y=-.5, b=.4, mark='haaa'), k(.5, 'sill', x=1.2, y=-.4, b=.5, l=1, mark='tk tk'), k(.7, 'sill', x=1.2, y=-.4, b=.5, r=1, mark='tk'), k(.88, eye='^')],
        [(.3, 'huff')], g='use', act=('blow', 'pane'), prefer=['happy', 'young'], say=["LUCK. In fog. It will be gone by lunch. So will the luck.", "Fogged a wish onto the glass. Public. Brave."])
    o.r('cross_his_wings_over_each_other_for_luck', 'Folding one wing tightly over the other and screwing up his face for luck', 16, 'none',
        [k(.15, x=.2, y=.3, b=.3), k(.35, x=.3, y=.6, b=.7, w=.4, eye='-'), k(.55, x=.2, y=.7, b=.8, w=.8, l=1, eye='-', mark='...'), k(.75, x=.2, y=.4, b=.4, w=.4, eye='O'), k(.9, eye='^')],
        [], g='use', act=('fold', 'wings'), prefer=['curious', 'young'])
    o.r('lift_the_charm_out_into_the_light', 'Lifting the charm out of its place in his bill and turning it to see the leaf in the light', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=.6, y=-1.2, b=-.8, l=1), k(.58, 'item', x=.4, y=-.5, b=.3, r=1, eye='O'), k(.72, 'item', x=1.1, y=-.5), k(.88, eye='^')],
        [], g='use', act=('lift', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.76, dict(hold=1)), (.86, dict(hold=0))])
    o.r('kiss_the_charm_for_luck', 'Kissing the lifted charm with a loud smack and holding it still for a moment', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.42, 'item', x=.3, y=-.4, b=-.2, eye='-', mark='MWAH'), k(.6, 'item', x=1.2, y=-.5, b=.1, eye='^'), k(.78, 'item', x=1, y=-.4)],
        [(.42, 'wish')], g='use', act=('tap', 'charm'), ages=GROWN, when=['wish<.6'], prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.38, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Smooch. It tasted of metal and false hope.", "Kissed it. Luck for a duck. No refunds."])
    o.r('spin_the_charm_on_its_cord', 'Spinning the lifted charm on its cord with a flick of his bill and watching the leaf whirl', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.2), k(.4, 'item', x=1.6, y=-.4, b=.4, l=1, mark='fwip'), k(.58, 'item', x=1.4, y=-.5, b=.3, eye='@'), k(.76, 'item', x=1.1, y=-.4), k(.9, eye='^')],
        [(.58, 'fun')], g='use', act=('spin', 'cord'), ages=GROWN, prefer=['happy', 'young'],
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))], say=["Round and round. It is making me dizzy for it.", "Spun the luck. It came out spinning."])
    o.r('carry_the_charm_for_a_lucky_lap', 'Carrying the lifted charm a lap round the case, strutting, and setting it back', 26, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.5, b=.2, mark='hup'), k(.38, 'item', x=.8, y=-.3, b=.5, l=1), k(.52, 'item', x=.8, y=-.3, b=.5, r=1, eye='^'), k(.66, 'item', x=.8, y=-.3, b=.5, l=1), k(.8, 'item', x=1.2, y=-.4), k(.9, eye='^')],
        [], g='use', act=('carry', 'charm'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.36, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('squint_at_the_charm_up_close', 'Squinting at the lifted charm up close, cross-eyed, to find which part is the lucky one', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.2, y=-.4, b=.2), k(.42, 'item', x=1.7, y=.1, b=.5, eye='@', mark='hm'), k(.6, 'item', x=1.7, y=.2, b=.6, eye='@'), k(.78, 'item', x=1.1, y=-.4), k(.9, eye='-')],
        [], g='test', act=('peer', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    # ---------------- play
    o.r('hopscotch_along_the_slats', 'Hopscotching along the base slats, one foot then two, never stepping on a gap', 20, 'none',
        [k(.1, 'slat_a', x=.3, y=.6, b=-.6, l=1), k(.28, 'slat_b', x=.4, y=.6, b=-.9, l=1, r=1), k(.46, 'slat_b', x=.3, y=.6, b=-.6, r=1), k(.64, 'slat_c', x=.4, y=.6, b=-.9, l=1, r=1), k(.82, 'slat_c', x=.3, y=.6, b=-.6, l=1), k(.92, eye='^')],
        [], g='play', act=('hop', 'slats'), prefer=['young', 'happy'], say=["Do not step on a crack. Cracks are my enemies.", "Hopscotch alone. I am winning. Also losing."])
    o.r('spin_three_times_before_knocking', 'Spinning three full times on the spot before touching the case, for luck', 18, 'none',
        [k(.12, x=.2, y=-.3, b=-.3, w=.4), k(.3, x=.9, y=-.5, b=-.8, w=1, l=1), k(.48, x=-.9, y=-.5, b=-.8, w=1, r=1), k(.66, x=.9, y=-.5, b=-.8, w=1, l=1), k(.82, 'rail', x=1.1, y=1.1, b=.6, eye='@', mark='tok'), k(.92, eye='^')],
        [], g='play', act=('spin', 'case'), prefer=['curious', 'happy'])
    o.r('balance_on_one_foot_to_keep_the_luck', 'Balancing on one foot with both wings out and his eyes shut to keep his luck from tipping', 22, 'none',
        [k(.12, x=.1, y=.5, b=.9), k(.3, x=.8, y=-.6, b=-.8, w=.7, l=1, eye='-'), k(.5, x=1.2, y=-1, b=-1.2, w=1, l=1, eye='-', mark='...'), k(.7, x=.6, y=-.4, b=-.6, w=.8, l=1, eye='-'), k(.88, y=.8, b=1, eye='O')],
        [], g='play', act=('balance', 'foot'), prefer=['curious', 'grown'])
    o.r('count_the_studs_out_for_luck', 'Counting out the studs, eeny meeny, to decide which end of the case is the lucky one', 18, 'none',
        [k(.12, 'stud_l', x=1.2, y=1.2, b=.5, mark='eeny'), k(.32, 'stud_r', x=1.2, y=1.2, b=.5, l=1, mark='meeny'), k(.52, 'stud_l', x=1.2, y=1.2, b=.5, r=1, mark='miny'), k(.72, 'stud_r', x=1.3, y=1.3, b=.6, mark='MO'), k(.9, eye='^')],
        [], g='play', act=('count', 'studs'), prefer=['young', 'curious'], say=["Right one. Left one. The right one. Final.", "Eeny meeny. It was always going to be the right."])
    o.r('shuffle_a_jig_along_the_bottom_rail', 'Shuffling a little jig along the bottom rail to bring the luck out', 20, 'none',
        [k(.12, 'rail', x=.3, y=.4, b=-.5, l=1), k(.3, 'rail', x=.4, y=.5, b=-.7, r=1, w=.5, mark='tap'), k(.5, 'slat_b', x=.3, y=.4, b=-.7, l=1, w=.7, mark='tap'), k(.7, 'rail', x=.4, y=.5, b=-.7, r=1, w=.5, mark='tap'), k(.88, y=.3, b=.3, eye='^')],
        [], g='play', act=('dance', 'rail'), prefer=['happy', 'young'])
    o.r('toss_a_peck_at_each_stand', 'Pecking at the nearest stand and the ledge above it, pretending the charm will fall into his bill', 18, 'none',
        [k(.12, x=.4, y=-.4, b=.2), k(.3, 'stand_m', x=1.3, y=-.6, b=-.6, mark='pk'), k(.48, x=-.3, y=-.3, b=-.3, w=.4, eye='O'), k(.66, 'ledge_m', x=1.4, y=-.8, b=-.8, l=1, mark='pk'), k(.86, y=.4, b=.3, eye='-')],
        [], g='play', act=('peck', 'stand'), ages=GROWN, prefer=['grumpy', 'young'], say=["Fall, charm. Fall. Gravity, do your job.", "Pecked a plinth. Plinth: stoic."])
    # ---------------- test
    o.r('peer_between_the_slats', 'Pushing his bill between two slats and peering at the gap between them for a stashed luck', 18, 'none',
        [k(.12, x=.4, y=.3, b=.3), k(.3, 'slat_a', x=1.5, y=1, b=.7, eye='o'), k(.5, 'slat_a', x=1.6, y=1.1, b=.8, l=1, eye='O', mark='hm'), k(.7, 'slat_b', x=1.5, y=1, b=.7, eye='o'), k(.88, x=-.3, y=-.2, eye='-')],
        [], g='test', act=('peer', 'slats'), prefer=['curious', 'young'])
    o.r('nibble_the_end_stud_to_test_it', 'Nibbling the end stud to test whether it is real metal and wincing', 14, 'none',
        [k(.15, 'stud_r', x=1.3, y=1.3, b=.6), k(.35, 'stud_r', x=1.5, y=1.5, b=.8, eye='-', mark='...'), k(.55, x=-.8, y=-.5, b=-.3, w=.6, l=1, eye='>', mark='ow'), k(.8, y=.5, b=.3, eye='-')],
        [], g='test', act=('taste', 'stud'), prefer=['curious', 'young'], say=["Tin. Bent my dignity.", "Metal. A good, loud no."])
    o.r('sniff_the_frame_plate_for_clover', 'Sniffing the frame plate all over for the smell of clover', 14, 'none',
        [k(.15, x=-.3, y=.3, b=.3), k(.35, 'plate_lo', x=1, y=-.4, b=.6, mark='snf'), k(.55, 'plate_lo', x=1.2, y=-.5, b=.8, l=1, mark='snf snf'), k(.78, x=.2, y=-.4, w=.4, eye='O')],
        [], g='test', act=('sniff', 'plate'), ages=GROWN, prefer=['curious'])
    o.r('weigh_the_charm_in_his_bill', 'Hefting the lifted charm in his bill, bobbing it up and down to see what luck weighs', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.5, b=.2), k(.36, 'item', x=.3, y=-.8, b=-.6), k(.5, 'item', x=1, y=.4, b=.7), k(.64, 'item', x=.3, y=-.8, b=-.6), k(.78, 'item', x=1, y=-.4), k(.9, eye='-')],
        [], g='test', act=('weigh', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('count_the_stands_along_the_ledge', 'Counting the stands along the ledge with his bill and finding only one of them occupied', 20, 'none',
        [k(.12, 'stand_m', x=1.2, y=-.7, b=.2, mark='one'), k(.3, 'ledge_m', x=1.2, y=-.8, b=.3, mark='two'), k(.48, 'stand_m', x=1.3, y=-.7, b=.3, l=1, mark='three'), k(.68, x=-.3, y=-.5, w=.4, eye='O', mark='one taken'), k(.88, eye='-')],
        [], g='test', act=('count', 'stands'), ages=GROWN, prefer=['curious'], say=["Three stands. One charm. The maths is rude.", "Two empty stands. Pre-lucky."])
    o.r('rap_the_glass_before_it_with_a_twig', 'Rapping the glass in front of the charm with a twig to see whether the luck answers', 16, 'twig',
        [k(.12, 'item', reach=.6, x=.3, y=-.5), k(.3, 'item', reach=1, x=.6, y=-.8, b=.3, mark='tink'), k(.5, x=-.4, y=-.5, w=.4, eye='O'), k(.7, 'item', reach=1, x=.7, y=-.8, b=.3, mark='tink'), k(.9, eye='-')],
        [], g='test', act=('tap', 'item'), prefer=['curious'])
    o.r('press_an_ear_to_the_rail', 'Pressing an ear to the bottom rail to hear whether luck is knocking back', 18, 'none',
        [k(.15, x=.4, y=.5, b=.6), k(.4, 'rail', x=-.5, y=1.8, b=1.5, eye='-'), k(.62, 'rail', x=-.6, y=1.9, b=1.6, l=1, eye='-', mark='...'), k(.85, x=-.5, y=-.5, b=-.2, w=.4, eye='O')],
        [], g='test', act=('listen', 'rail'), prefer=['curious', 'lonely'], say=["Nothing knocks back. Bad luck is quiet.", "Heard my own pulse. Not a lucky sound."])
    # ---------------- rest
    o.r('curl_up_at_the_stud_with_a_wing_over_his_eyes', 'Curling up at the end stud with a wing over his eyes for a luckless afternoon nap', 28, 'none',
        [k(.15, x=.4, y=.4, b=.5), k(.4, 'stud_l', x=.3, y=1.5, b=1.4, w=.4, eye='-'), k(.7, 'stud_l', x=.3, y=1.8, b=1.7, w=.5, eye='-', mark='zzz'), k(.9, x=-.3, y=-.3, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'case'), when=['tired'])
    o.r('lean_into_the_slats_with_a_sigh', 'Leaning his whole weight against the slats and sighing at the charm above', 18, 'none',
        [k(.15, x=.5, y=.2, b=.2, r=1), k(.4, 'slat_c', x=-1, y=.4, b=1.1, w=.5), k(.7, 'slat_c', x=-1.1, y=.6, b=1.4, eye='-', mark='sigh', l=1), k(.9, x=.3, y=.2, b=.3)],
        [], g='rest', act=('lean', 'slats'), prefer=['tired', 'sad'])
    o.r('turn_his_back_on_the_charm_and_sulk', 'Turning his back on the charm and sulking because it has brought him nothing', 22, 'none',
        [k(.15, x=-.7, y=.5, b=.6, r=1), k(.4, 'slat_b', x=-1.2, y=1.6, b=1.8, w=.4, eye='-'), k(.7, 'stud_l', x=-1.3, y=1.8, b=2, w=.2, l=1, eye='-', mark='hmph'), k(.9, x=-.2, y=.6, b=.7)],
        [], g='rest', act=('sulk', 'charm'), when=['sad'], say=["Lucky, they said. Hah.", "Got rained on. Charm unaffected. Fine."])
    o.r('sit_with_his_wing_tips_crossed_and_wait', 'Sitting very still with his wing tips crossed, waiting for the luck to arrive', 24, 'none',
        [k(.15, x=.2, y=.1, b=.5), k(.4, x=.1, y=.5, b=1.1, w=.3, eye='-'), k(.65, x=.2, y=-.4, b=1.2, w=.4, eye='O', mark='...'), k(.85, x=.1, y=.2, b=.6, eye='-')],
        [], g='rest', act=('wait', 'charm'), prefer=['lonely', 'curious'])
    o.r('sit_down_beside_the_end_stud_and_stare', 'Sitting down beside the end stud with his bill resting against it, staring at nothing', 22, 'none',
        [k(.15, x=.4, y=.3, b=.7), k(.4, 'stud_r', x=.6, y=1, b=1.4, eye='-'), k(.62, 'stud_r', x=.6, y=1.2, b=1.6, l=1, eye='-', mark='...'), k(.85, x=.1, y=.2, b=.5, eye='O')],
        [], g='rest', act=('sit', 'stud'), prefer=['sad', 'tired'])
    # ---------------- weather
    o.r('dry_the_rain_off_the_frame_plate', 'Drying the rain off the frame plate and the trim below it with a wing', 18, 'wing',
        [k(.12, 'plate_lo', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'plate_lo', reach=1, x=.5, y=-.4, b=.3, w=.3), k(.5, 'trim_lo', reach=1, x=.5, y=-.2, b=.4, l=1), k(.7, 'sill', reach=1, x=.4, y=-.3, b=.3, r=1), k(.88, eye='-')],
        [(.5, 'dry')], g='weather', act=('dry', 'plate'), when=['obj_wetness>.3'], ages=GROWN)
    o.r('brace_his_back_against_the_rail_in_the_storm', 'Bracing his back against the bottom rail in the storm, rain pelting the glass', 32, 'none',
        [k(.12, 'rail', x=-.3, y=.6, b=.9), k(.3, 'rail', x=-.8, y=1.2, b=1.6, w=.3, eye='-'), k(.58, 'rail', x=-.9, y=1.4, b=1.8, eye='-', mark='drip'), k(.82, 'rail', x=-.4, y=.8, b=1.1, eye='>')],
        [], g='weather', act=('brace', 'rail'), when=['storm', 'wet'])
    o.r('sunbathe_against_the_warm_slats', 'Sunbathing against the warm slats with his wings half open, face to the sky', 26, 'none',
        [k(.15, x=-.3, y=-.3, b=.5), k(.45, 'slat_a', x=-.5, y=-.9, b=1, w=.5, eye='-'), k(.7, 'slat_a', x=-.6, y=-1, b=1.2, w=.7, eye='-', mark='mm'), k(.9, y=.2, b=.2, eye='^')],
        [], g='weather', act=('warm', 'slats'), when=['sun'], prefer=['tired'])
    o.r('tiptoe_past_the_case_at_night', 'Tiptoeing back and forth past the case at night so as not to wake any bad luck', 24, 'none',
        [k(.12, x=.3, y=-.3, b=-.4, l=1, eye='o'), k(.3, 'stud_l', x=.5, y=-.4, b=-.5, r=1, mark='shh'), k(.5, 'rail', x=.5, y=-.4, b=-.5, l=1, eye='O'), k(.7, 'stud_r', x=.5, y=-.4, b=-.5, r=1, mark='shh'), k(.88, y=.2, eye='-')],
        [], g='weather', act=('guard', 'case'), when=['night'], say=["Shh. Luck is sleeping. Do not wake the luck.", "Night patrol. Armed with a bill and good manners."])
    # ---------------- show
    o.r('bow_to_the_charm_with_a_flourish', 'Bowing to the charm with a flourish of one wing and a click of his heels', 16, 'none',
        [k(.15, x=-.4, y=-.8, b=-.5, w=.5, l=1), k(.4, 'rail', x=1.3, y=1.6, b=1, w=1, r=1, mark='ta-da'), k(.62, 'rail', x=1.4, y=1.8, b=1.2, w=.9), k(.86, x=-.3, y=-.6, b=-.3, w=.4, eye='^')],
        [], g='show', act=('bow', 'charm'), prefer=['happy'])
    o.r('flourish_a_wing_at_the_charm_like_a_game_show', 'Flourishing a wing at the charm like the prize on a game show', 16, 'wing',
        [k(.15, reach=.2, x=-.3, y=-.5, b=-.4, l=1), k(.38, reach=1, x=.6, y=-.9, w=.5, b=-.8), k(.62, reach=1, x=.6, y=-1.1, w=.5, b=-1, r=1, mark='dun-dun'), k(.85, reach=0, y=.4, b=.3, eye='^')],
        [], g='show', act=('present', 'charm'), prefer=['happy'], say=["And here, tonight's star prize: a charm.", "Applause. There was none. I imagined some."])
    o.r('strike_a_pose_beside_the_end_stud', 'Striking a pose beside the end stud, one foot raised, as if the case were a podium', 18, 'none',
        [k(.15, x=.3, y=-.5, b=-.5, w=.3), k(.4, 'stud_r', x=1, y=-.9, b=-1, w=1, l=1), k(.7, 'stud_r', x=1.3, y=-1.2, b=-1.2, w=1, r=1, mark='...'), k(.9, y=.4, b=.3, eye='^')],
        [], g='show', act=('pose', 'stud'), prefer=['happy'])
    o.r('argue_with_the_charm_over_the_luck', 'Arguing with the charm, jabbing a wing at it over the luck it owes him', 18, 'wing',
        [k(.15, reach=.3, x=.5, y=-.2, b=.2, eye='>'), k(.3, 'item', reach=1, x=.9, y=-.7, b=.2, w=.6, mark='OI'), k(.5, reach=.4, x=-.3, y=.2, b=.5, l=1), k(.7, 'item', reach=1, x=1, y=-.7, b=.2, w=.8, r=1, mark='OI!'), k(.9, y=.7, b=.6, eye='-')],
        [], g='show', act=('argue', 'charm'), prefer=['grumpy'])
    o.r('shout_for_luck_at_the_charm', 'Shouting at the charm to bring some luck, now, with both wings up', 14, 'wing',
        [k(.15, x=.3, y=-.6, b=-.3), k(.35, reach=1, x=.9, y=-1.4, b=-.6, w=.6, mark='LUCK'), k(.6, reach=.6, x=.9, y=-1.4, b=-.6, l=1, w=.5, mark='NOW'), k(.85, x=-.2, y=.2, eye='-')],
        [], g='show', far=True, act=('shout', 'charm'), prefer=['grumpy'], say=["Luck. Please. I said please. Mostly.", "Nothing. It is on hold."])
    o.r('whisper_a_lullaby_to_the_charm', 'Whispering a lullaby to the charm through the glass so its luck sleeps well', 22, 'none',
        [k(.12, x=.2, y=.3, b=.3), k(.3, 'sill', x=1, y=-.5, b=.5, mark='hush'), k(.5, 'sill', x=1.1, y=-.4, b=.6, l=1, mark='la la'), k(.7, 'sill', x=1, y=-.5, b=.5, w=.3, mark='lu lu'), k(.88, eye='-')],
        [], g='show', act=('sing', 'charm'), prefer=['sad', 'lonely'])
    # ---------------- mishap
    o.r('stamp_the_bad_luck_off', 'Stamping hard beside the studs to shake off the bad luck, then hopping about', 16, 'none',
        [k(.15, x=.2, y=-.3, b=-.5, l=1), k(.3, 'stud_l', x=.1, y=.5, b=.7, l=1, mark='STOMP'), k(.5, x=-.2, y=-.6, b=-.9, r=1, w=.8, eye='O', mark='OW'), k(.7, 'stud_l', x=.1, y=.4, b=.6, r=1, mark='STOMP'), k(.9, eye='-')],
        [], g='mishap', act=('stamp', 'studs'), prefer=['grumpy'], say=["Out, bad luck. Out. Ow. My foot.", "Stamped it. It stayed. I limped."])
    o.r('bump_the_doors_at_dusk', 'Backing into the doors at dusk while bowing and bouncing off with a clunk', 14, 'none',
        [k(.15, x=-.6, y=.2, b=.4), k(.3, 'seam_lo', x=-1.1, y=.2, b=.8, eye='O', mark='clunk'), k(.5, x=.7, y=-.4, b=-.7, w=.8, eye='@'), k(.8, x=.1, y=.3, b=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'case'), ages=GROWN, when=['dusk'])
    o.r('skid_across_the_wet_ground_into_the_slats', 'Skidding on wet ground at the foot of the case and ending in a heap against the slats', 16, 'none',
        [k(.15, 'slat_b', x=.4, y=.3, b=.4, r=1), k(.3, x=.6, y=-.4, b=-.8, w=1, l=1, r=1, eye='O', mark='WAAH'), k(.5, 'slat_a', x=1.2, y=1.7, b=1.6, w=.8, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('slip', 'slats'), when=['obj_wetness>.3'], prefer=['young'])
    o.r('rap_the_wood_too_hard_and_hurt_his_bill', 'Rapping the wood for luck much too hard and hopping about clutching his bill', 14, 'none',
        [k(.15, x=.4, y=.4, b=.3), k(.3, 'slat_c', x=1.6, y=1.5, b=.8, mark='TOK'), k(.45, x=-.9, y=-.6, b=-.8, w=.8, l=1, r=1, eye='>', mark='YOW'), k(.7, x=.3, y=.4, b=.4, eye='-'), k(.88, eye='@')],
        [], g='mishap', act=('peck', 'wood'), prefer=['young', 'grumpy'], say=["Knocked on wood. Wood knocked back.", "Bill hurts. Luck, apparently, is pain."])
    o.r('leap_for_the_charm_and_land_on_his_tail', 'Leaping up for the charm, missing, and landing on his tail at the foot of the rail', 18, 'none',
        [k(.15, x=.3, y=.3, b=.9), k(.3, x=.8, y=-1, b=-1.5, w=1, eye='O'), k(.45, x=.4, y=-1.4, b=-1.9, w=1, l=1, r=1, eye='@', mark='hup'), k(.62, 'rail', x=-.9, y=1.8, b=2, w=.6, eye='@', mark='plop'), k(.85, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('hop', 'rail'), prefer=['young'], say=["Landed on my tail. It is my tail's turn to complain.", "Missed by a mile. A tall mile."])
    # ---------------- duets (a friend takes their own part)
    o.r('two_ducks_buffing_the_rail', 'Buffing the bottom rail with a friend, one working in from each end until it gleams', 22, 'wing',
        [k(.1, 'stud_l', reach=.6, x=.3, y=.8, b=.4), k(.28, 'rail', reach=1, x=.5, y=1, b=.7, l=1), k(.48, 'rail', reach=1, x=.5, y=1.1, b=.8, r=1), k(.68, 'slat_b', reach=1, x=.5, y=1, b=.7), k(.88, eye='^')],
        [(.48, 'shine')], g='care', act=('wipe', 'rail'), when=['gleam<.5'], prefer=['happy'],
        duo=[k(.1, 'stud_r', reach=.6, x=.3, y=.8, b=.4), k(.3, 'rail', reach=1, x=.5, y=1, b=.7, r=1), k(.5, 'rail', reach=1, x=.5, y=1.1, b=.8, l=1), k(.7, 'slat_b', reach=1, x=.5, y=1, b=.7), k(.88, eye='^')])
    o.r('knock_on_the_wood_together_on_three', 'Knocking on the wood together with a friend on a count of three for double the luck', 20, 'none',
        [k(.15, x=.2, y=.1, b=.3, mark='one'), k(.3, x=.2, y=.1, b=.3, mark='two'), k(.46, 'rail', x=1.4, y=1.4, b=.6, mark='THREE'), k(.62, 'rail', x=1.3, y=1.3, b=.5, l=1, mark='tok'), k(.8, eye='^')],
        [], g='use', act=('knock', 'rail'), when=['wish<.6'], prefer=['happy', 'lonely'],
        duo=[k(.15, x=.2, y=.1, b=.3), k(.3, x=.2, y=.1, b=.3), k(.46, 'slat_c', x=1.4, y=1.4, b=.6, mark='THREE'), k(.62, 'slat_c', x=1.3, y=1.3, b=.5, r=1, mark='tok'), k(.8, eye='^')])
    o.r('hopscotch_a_race_with_a_friend_along_the_slats', 'Racing a friend along the slats in a game of hopscotch, hop for hop', 22, 'none',
        [k(.1, 'slat_a', x=.3, y=.6, b=-.6, l=1), k(.3, 'slat_b', x=.5, y=.6, b=-.9, r=1), k(.5, 'slat_b', x=.4, y=.6, b=-.6, l=1, w=.4), k(.7, 'slat_c', x=.5, y=.6, b=-1, l=1, r=1), k(.9, eye='^', mark='won')],
        [], g='play', act=('race', 'slats'), prefer=['happy', 'young'],
        duo=[k(.1, 'slat_a', x=.3, y=.6, b=-.6, r=1), k(.3, 'slat_a', x=.4, y=.6, b=-.9, l=1), k(.5, 'slat_b', x=.5, y=.6, b=-.9, r=1), k(.7, 'slat_b', x=.4, y=.6, b=-.6, l=1), k(.9, 'slat_c', x=.3, y=.6, b=-.6, r=1, mark='bah')])
    o.r('swap_places_to_look_at_the_charm', 'Swapping places with a friend by the stand so each can look at the charm from the other side', 22, 'none',
        [k(.12, x=.3, y=-.4, b=-.2), k(.3, 'stand_m', x=1.1, y=-1.2, b=-.5, eye='O'), k(.5, x=-.6, y=-.4, b=.4, l=1), k(.7, 'ledge_m', x=1.2, y=-1.2, b=-.6, eye='O', mark='ooh'), k(.9, eye='-')],
        [], g='test', act=('compare', 'stands'), ages=GROWN, prefer=['curious', 'happy'],
        duo=[k(.12, x=.3, y=-.4, b=-.2), k(.34, 'ledge_m', x=1.2, y=-1.2, b=-.6), k(.54, x=-.6, y=-.4, b=.4, r=1), k(.74, 'stand_m', x=1.1, y=-1.2, b=-.5, eye='O', mark='ahh'), k(.9, eye='-')])
    # @@END lucky_charm
    return done(o)


def koi():
    # Host koi_pond (120 cols x 55 rows, 7.5 px a row, standing line row 46 where he stands at the rim). Left: three cattail stems with `#` heads (cols 7/12/17, heads
    # at rows 31 and 28), a grass tuft `\|/\|/` at the foot (row 44). Right: three tall cattails (cols 103/108/113). Two lily pads with blooms `{*}`: the left one high
    # (row 30-32, 112-120 px), the right one low (rows 35-38, 67-82 px). Rippling water rows 29-45 (127 px down to 7 px), a far edge line at row 27 (142 px), a stone
    # bank round it `( )`, and the front stones at the rim, row 46 (0 px). The koi is drawn at the rim spot he touches: lure + pick.
    P = pm('koi_pond')
    o = Obj('koi', 'keeping', on='koi_pond',
            fields=dict(trick=(0, 0, 1), rhythm=(0, 0, 1)),
            physics=[('trick', 'rate', -.0002, 'always'), ('rhythm', 'rate', -.0004, 'always')],
            effects=dict(scoop=[('keeping.leaves', 'mul', .35)], scour=[('keeping.algae', 'mul', .5)], thin=[('keeping.plants', 'mul', .75)],
                         crack=[('keeping.ice', 'mul', .3)], stir=[('keeping.oxygen', 'add', .3)], scatter=[('keeping.flakes', 'add', .5)],
                         call=[('keeping.bell', 'add', .5), ('rhythm', 'add', .4)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)],
                         kiss=[('subject.trust', 'add', .1), ('subject.mood', 'add', .15)], tickle=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         lead=[('trick', 'add', .15), ('subject.trust', 'add', .1)], unsnag=[('subject.health', 'add', .15), ('subject.trust', 'add', .1)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(shallow_l=P(28, 43), shallow_m=P(58, 41), shallow_r=P(88, 39), pad_r=P(86, 37), bloom_r=P(81, 35), pad_l=P(41, 31),
                         tuft=P(11, 44), reed_low=P(8, 38), cattail_l=P(7, 31), bank_r=P(95, 40),
                         stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46)))
    # ---------------- care
    o.r('net_leaves', 'Netting fallen leaves off the koi pond with a reed, drawing them in to the rim in two long sweeps', 22, 'reed',
        [k(.15, 'pad_r', reach=.7, x=.3, y=.2, w=.3), k(.35, 'shallow_m', reach=1, x=.5, y=.5, b=.3, mark='swsh'), k(.55, 'shallow_l', reach=1, x=.7, y=.6, b=.4, mark='swsh'), k(.78, 'stone_l', reach=.6, x=.2, y=.4, eye='^'), k(.9, eye='-')],
        [(.35, 'scoop'), (.55, 'scoop')], g='care', act=('scoop', 'leaves'), prefer=['pond_leaves>.3', 'windy'], say=["Leaves out. Pond looks smug about it.", "Fished out a lot of leaves. Zero fish. Fine."])
    o.r('scrub_the_front_stones', 'Scrubbing the green off the front stones with the side of a wing, left stone and then the middle one', 18, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.4), k(.3, 'stone_l', reach=1, x=.5, y=1.2, b=.8, l=1, mark='sqk'), k(.5, 'stone_m', reach=1, x=.5, y=1.3, b=.9, r=1, mark='sqk'), k(.7, 'stone_m', reach=1, x=.4, y=1.2, b=.8), k(.88, eye='^')],
        [(.5, 'scour')], g='weather', act=('scrub', 'stones'), when=['pond_algae>.4'])
    o.r('thin_out_the_lily_pads', 'Thinning the crowded lily pads with a twig, hooking one over and pulling it loose from the bloom', 22, 'twig',
        [k(.12, 'pad_r', reach=.6, x=.3, y=.3), k(.3, 'pad_r', reach=1, x=.6, y=.5, b=.4, mark='hnk'), k(.5, 'bloom_r', reach=1, x=.5, y=.2, b=.6, l=1), k(.7, 'pad_r', reach=1, x=.2, y=-.3, b=-.3, w=.4, mark='pop'), k(.88, eye='-')],
        [(.5, 'thin')], g='care', act=('pull', 'lily'), when=['pond_plants>.7'])
    o.r('draw_a_weed_off_the_fin', 'Slowly drawing a trailing strand of weed off the shy koi\'s fin with the tip of his bill', 22, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'shallow_l', x=1.2, y=1.3, b=.8, eye='-'), k(.5, 'shallow_l', x=1.1, y=1.5, b=1, l=1, mark='tug'), k(.7, 'shallow_l', x=.5, y=.7, b=.5, w=.4, mark='plip'), k(.88, eye='^')],
        [(.5, 'unsnag')], g='care', act=('pull', 'weed'), pick='shyest', when=['fish_health<.8'], obj=[(.25, dict(lure=1)), (.6, dict(lure=1))],
        say=["Weed off. Koi blinked. Gratitude, I think.", "You had a salad on your fin. Hold still."])
    # ---------------- use
    o.r('scatter_flakes', 'Flicking a wingful of flakes out across the water so they drift down in a fan', 16, 'wing',
        [k(.15, 'shallow_m', reach=.6, w=.6), k(.35, 'shallow_m', reach=1, b=-.3, w=1, mark='~~~'), k(.6, x=-.3, y=.2, eye='o'), k(.85, eye='^')],
        [(.35, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.4'], prefer=['dawn', 'dusk'])
    o.r('rap_the_stone_for_dinner', 'Rapping the middle front stone with his bill in the dinner rhythm until the fish come crowding', 18, 'none',
        [k(.12, 'stone_m', x=1.3, y=1.4, b=.6, mark='tok'), k(.28, 'stone_m', x=1.3, y=1.4, b=.6, l=1, mark='tok'), k(.44, x=-.3, y=-.2, b=-.2, w=.3), k(.6, 'stone_m', x=1.4, y=1.5, b=.7, r=1, mark='tok tok'), k(.85, eye='^')],
        [(.6, 'call')], g='use', act=('ring', 'stone'), when=['pond_bell<.4'], prefer=['dusk'])
    o.r('hand_feed_the_hungriest', 'Holding a single flake in his bill just at the surface until the hungriest koi rises and takes it', 20, 'none',
        [k(.12, x=.5, y=.7, b=.5), k(.3, 'shallow_l', x=1.2, y=1.6, b=1, eye='o', mark='...'), k(.5, 'shallow_l', x=1.1, y=1.8, b=1.1, eye='O', mark='gulp'), k(.72, 'shallow_l', x=.5, y=.6, b=.4, w=.4, eye='^'), k(.9, eye='-')],
        [(.5, 'feed')], g='use', act=('carry', 'flake'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1)), (.78, dict(lure=0))],
        say=["Took it right out of my bill. Eight out of ten, rude.", "Hand-fed a koi. Trust me. Mostly its."])
    o.r('let_the_shy_one_kiss_his_bill', 'Dipping his bill to the water so the shy koi comes up and kisses the tip of it', 20, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_m', x=1.3, y=1.4, b=.9, eye='-', mark='...'), k(.5, 'shallow_m', x=1.4, y=1.6, b=1, eye='-', mark='mwah'), k(.72, 'shallow_m', x=.8, y=.9, b=.6, eye='^'), k(.9, eye='-')],
        [(.5, 'kiss')], g='use', act=('tap', 'lips'), pick='shyest', prefer=['fish_trust<.8', 'happy'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))],
        say=["Fish lips. Very wet. Ten out of ten.", "It kissed me and left. Story of my life."])
    o.r('tickle_its_chin_with_a_wing_tip', 'Tickling the koi under its chin with the tip of a wing while it hangs still at the surface', 20, 'wing',
        [k(.12, 'shallow_m', reach=.5, x=.3, y=.8, b=.5), k(.3, 'shallow_m', reach=1, x=.5, y=1.2, b=.9, mark='tck'), k(.5, 'shallow_m', reach=1, x=.5, y=1.3, b=1, r=1, mark='tck tck'), k(.72, 'shallow_m', reach=.6, x=.3, y=.8, b=.6), k(.9, eye='^')],
        [(.5, 'tickle')], g='use', act=('pat', 'chin'), pick='shyest', obj=[(.28, dict(lure=1)), (.65, dict(lure=1))])
    o.r('walk_the_rim_with_a_wing_trailing', 'Walking the rim with a wing trailing at the surface and the koi following the wingtip all the way', 26, 'wing',
        [k(.1, 'shallow_l', reach=.6, x=.2, y=.7, b=.4), k(.28, 'shallow_m', reach=1, x=.4, y=.8, b=.5, l=1), k(.5, 'shallow_r', reach=1, x=.5, y=.8, b=.5, r=1), k(.7, 'shallow_m', reach=1, x=.4, y=.8, b=.5, l=1), k(.9, eye='^')],
        [(.5, 'lead')], g='use', act=('chase', 'wingtip'), pick='hungriest', obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.75, dict(lure=1))], say=["It followed me the whole length. Nobody else does.", "Led a fish on a wing. I am a very small parade."])
    o.r('hold_a_reed_ring_at_the_surface', 'Holding a reed bent into a ring just at the surface until the koi noses at it, once, twice', 24, 'reed',
        [k(.12, 'shallow_r', reach=.5, x=.3, y=.4, b=.4), k(.3, 'shallow_r', reach=1, x=.5, y=.8, b=.7), k(.5, 'shallow_r', reach=1, x=.5, y=.8, b=.8, l=1, mark='plip'), k(.7, 'shallow_r', reach=1, x=.4, y=.7, b=.7, r=1, mark='plip'), k(.9, eye='^')],
        [(.5, 'lead')], g='use', act=('hook', 'ring'), pick='hungriest', prefer=['curious', 'trick<.7'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('drum_the_three_stones_in_turn', 'Drumming the three front stones in turn, left to right, to teach the koi the dinner call', 22, 'none',
        [k(.1, 'stone_l', x=1.2, y=1.3, b=.5, mark='tok'), k(.3, 'stone_m', x=1.2, y=1.3, b=.5, l=1, mark='tok'), k(.5, 'stone_r', x=1.3, y=1.3, b=.5, r=1, mark='tok'), k(.7, 'stone_m', x=1.2, y=1.4, b=.6, mark='TOK'), k(.9, eye='^')],
        [(.5, 'call')], g='use', act=('drum', 'stones'), pick='hungriest', when=['rhythm<.6'], obj=[(.6, dict(lure=1)), (.8, dict(lure=1))])
    # ---------------- play
    o.r('race_the_koi_along_the_rim', 'Racing the koi along the rim, sprinting from the left stones to the right while it keeps pace in the water', 20, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.3, 'shallow_m', x=1.2, y=.4, b=-.5, r=1, w=.5), k(.5, 'shallow_r', x=1.3, y=.4, b=-.6, l=1, w=.6), k(.72, 'shallow_r', x=.6, y=.5, b=.6, eye='O', mark='whew'), k(.9, eye='^')],
        [(.5, 'fun')], g='play', act=('race', 'koi'), pick='hungriest', prefer=['happy', 'young'], obj=[(.12, dict(lure=1)), (.35, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))],
        say=["Lost by a fin. Rigged. Fish cut corners.", "Race over. The koi wasn't even trying."])
    o.r('blow_bubbles_at_the_surface', 'Blowing bubbles at the surface until the koi blows a few back at him', 20, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_l', x=1.2, y=1.4, b=.9, mark='blub'), k(.5, 'shallow_l', x=1.3, y=1.5, b=1, l=1, mark='blub blub'), k(.7, 'shallow_l', x=1.1, y=1.3, b=.9, eye='O', mark='blub'), k(.88, eye='^')],
        [(.5, 'tickle')], g='play', act=('blow', 'bubbles'), pick='shyest', prefer=['happy', 'young'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))], say=["Bubble conversation. Mostly it won.", "Blub. Blub. It said blub. Excellent."])
    o.r('balance_on_the_front_stone_with_wings_out', 'Balancing on the left front stone with both wings out while the koi circles to watch', 22, 'none',
        [k(.12, 'stone_l', perch=1, x=.1, y=.2, b=.3), k(.3, 'stone_l', perch=1, x=.3, y=-.3, b=-.2, w=.8, l=1), k(.5, 'stone_l', perch=1, x=.4, y=-.5, b=-.4, w=1, l=1, eye='O', mark='...'), k(.7, 'stone_l', perch=1, x=.3, y=-.3, b=-.2, w=.8, r=1), k(.88, y=.3, b=.4, eye='^')],
        [], g='play', act=('balance', 'stone'), prefer=['curious', 'grown'])
    o.r('flick_a_splash_and_dodge_the_return', 'Flicking a splash at the koi with a wing and ducking away as it splashes straight back', 18, 'wing',
        [k(.12, 'shallow_r', reach=.6, x=.3, y=.7, b=.5), k(.3, 'shallow_r', reach=1, x=.4, y=.8, b=.7, w=.8, mark='splsh'), k(.5, x=-1, y=-.4, b=-.7, w=.8, l=1, eye='O', mark='WAH'), k(.72, x=-.4, y=.3, b=.3, eye='>'), k(.9, eye='^')],
        [], g='play', act=('splash', 'koi'), pick='hungriest', prefer=['young', 'happy'], obj=[(.28, dict(lure=1)), (.45, dict(lure=1))])
    o.r('duck_into_the_reeds_and_pop_out_at_it', 'Ducking low into the reed foot, then popping out at the koi as it noses over to look', 20, 'none',
        [k(.12, 'reed_low', x=.5, y=1.2, b=1.4, eye='-'), k(.3, 'reed_low', x=.4, y=1.5, b=1.7, eye='o'), k(.5, 'shallow_l', x=1.5, y=-.5, b=-.8, w=.8, eye='O', mark='BOO'), k(.7, 'shallow_l', x=.8, y=.2, b=.3, eye='^'), k(.9, eye='-')],
        [], g='play', act=('seek', 'koi'), pick='shyest', prefer=['young', 'curious'], obj=[(.35, dict(lure=1)), (.65, dict(lure=1))], say=["Boo. The koi did not jump. It yawned.", "Hide and seek. It lost, then won, then left."])
    o.r('dance_a_shuffle_along_the_stones', 'Dancing a quick shuffle from one front stone to the next, wings flapping in time', 22, 'none',
        [k(.12, 'stone_l', perch=1, x=.2, y=-.2, b=-.5, l=1), k(.3, 'stone_l', perch=1, x=.4, y=-.4, b=-.7, r=1, w=.6, mark='tap'), k(.5, 'stone_m', perch=1, x=.3, y=-.4, b=-.7, l=1, w=.8, mark='tap'), k(.7, 'stone_m', perch=1, x=.4, y=-.4, b=-.7, r=1, w=.6, mark='tap'), k(.88, y=.4, b=.4, eye='^')],
        [], g='play', act=('dance', 'stones'), prefer=['happy', 'young'])
    # ---------------- test
    o.r('watch_the_shadow_glide_in', 'Leaning out over the rim to watch the koi\'s shadow glide in past the pad, nose up, eyes wide', 20, 'none',
        [k(.12, x=.5, y=.6, b=.4), k(.3, 'shallow_m', x=1, y=.9, b=.8, eye='o'), k(.52, 'shallow_m', x=1.2, y=1.1, b=.9, eye='O', mark='...'), k(.74, 'shallow_m', x=.5, y=.5, b=.4, w=.4, eye='^'), k(.9, eye='-')],
        [], g='test', act=('peer', 'shadow'), pick='shyest', prefer=['curious'], obj=[(.35, dict(lure=1)), (.6, dict(lure=1))], say=["A big orange shadow. Mine now, spiritually.", "Looks like a coin with ambitions."])
    o.r('hold_a_wing_up_to_measure_the_koi', 'Holding a wing out over the water to measure the koi from nose to tail, and guessing again', 22, 'wing',
        [k(.12, 'shallow_l', reach=.6, x=.3, y=.6, b=.4), k(.3, 'shallow_l', reach=1, x=.4, y=.8, b=.6, w=.4), k(.5, 'shallow_m', reach=1, x=.5, y=.8, b=.6, l=1, w=.8, mark='hm'), k(.72, 'shallow_m', reach=1, x=.4, y=.7, b=.5, r=1), k(.9, eye='-')],
        [], g='test', act=('measure', 'koi'), pick='hungriest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))])
    o.r('sniff_the_pond_water', 'Sniffing the pond water at the right rim, nostrils flaring, trying to name what it smells of', 14, 'none',
        [k(.15, x=.4, y=.7, b=.4), k(.35, 'shallow_r', x=1.1, y=1.3, b=.9, mark='snf'), k(.55, 'shallow_r', x=1.2, y=1.4, b=1, l=1, mark='snf snf'), k(.8, x=-.3, y=-.2, w=.4, eye='O')],
        [], g='test', act=('sniff', 'water'), prefer=['curious'])
    o.r('taste_a_sip_of_the_pond', 'Taking a sip of pond at the left rim and pulling a face at the green taste', 14, 'none',
        [k(.15, x=.4, y=.8, b=.5), k(.35, 'shallow_l', x=1.2, y=1.6, b=1, eye='-', mark='slp'), k(.55, x=-.8, y=-.6, b=-.3, w=.7, l=1, eye='>', mark='bleh'), k(.8, y=.4, b=.3, eye='-')],
        [], g='test', act=('taste', 'water'), prefer=['curious', 'pond_algae>.3'], say=["Pond. Regrettable. A little koi, a lot of algae.", "Tastes like a wet lawn. I am not sure why I did it."])
    o.r('lay_an_ear_to_the_water_to_listen', 'Laying his head sideways at the water to listen for the koi\'s tiny gulps', 20, 'none',
        [k(.15, x=.4, y=.6, b=.5), k(.4, 'shallow_m', x=.3, y=1.7, b=1.3, eye='-'), k(.62, 'shallow_m', x=.3, y=1.8, b=1.4, l=1, eye='-', mark='...'), k(.85, x=-.5, y=-.5, w=.4, eye='O')],
        [], g='test', act=('listen', 'pond'), prefer=['curious', 'lonely'])
    o.r('count_the_pads_and_the_bloom', 'Counting the lily pads across the water with his bill, the low pad, the bloom, and the high pad', 20, 'none',
        [k(.12, 'pad_r', x=1, y=.1, b=.5, mark='1'), k(.32, 'bloom_r', x=1.2, y=-.4, b=.5, mark='2'), k(.54, 'pad_l', x=1.4, y=-1, b=.2, l=1, mark='3'), k(.78, x=.2, y=-.4, w=.4, eye='-', mark='3 and a flower')],
        [], g='test', act=('count', 'pads'), ages=GROWN, prefer=['curious'])
    o.r('tap_the_ice_to_test_it', 'Tapping the skin of ice at the rim with a wing tip to find out how thick it is', 16, 'wing',
        [k(.15, 'shallow_m', reach=.5, x=.3, y=.7, b=.4), k(.32, 'shallow_m', reach=1, x=.5, y=1, b=.7, mark='tik'), k(.5, 'shallow_l', reach=1, x=.5, y=1, b=.7, l=1, mark='tik'), k(.7, 'shallow_l', reach=1, x=.4, y=.9, b=.6, mark='tik'), k(.88, eye='-', mark='hm')],
        [], g='test', act=('test', 'ice'), when=['pond_ice>.2'])
    o.r('squint_at_two_reflections', 'Squinting at his own reflection and the koi\'s side by side in the water, comparing the fashion', 20, 'none',
        [k(.15, x=.4, y=.7, b=.4), k(.35, 'shallow_l', x=1, y=1.5, b=1, eye='O'), k(.55, 'shallow_l', x=1.1, y=1.6, b=1.1, l=1, eye='>', mark='hm'), k(.76, 'shallow_l', x=.8, y=1, b=.6, w=.5, eye='^'), k(.9, eye='-')],
        [], g='test', act=('compare', 'reflection'), pick='shyest', prefer=['curious', 'happy'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))], say=["I have the better bill. It has the better coat.", "Two pretty faces. One of them is mine."])
    # ---------------- rest
    o.r('curl_up_in_the_grass_tuft', 'Curling up against the grass tuft at the pond edge for a nap, with a koi ripple in his ear', 28, 'none',
        [k(.15, x=.4, y=.5, b=.5), k(.4, 'tuft', x=.2, y=1.6, b=1.5, eye='-'), k(.7, 'tuft', x=.2, y=1.9, b=1.8, w=.3, eye='-', mark='zzz'), k(.9, x=-.2, y=-.2, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'tuft'), when=['tired'])
    o.r('sit_down_on_the_front_stone_and_watch', 'Sitting down on the left front stone with his feet nearly in the water, watching the koi circle', 26, 'none',
        [k(.15, 'stone_l', perch=1, x=.3, y=.2, b=.8), k(.4, 'stone_l', perch=1, x=.2, y=.5, b=1.4, eye='o'), k(.65, 'stone_l', perch=1, x=.2, y=.4, b=1.5, l=1, eye='o', mark='...'), k(.85, 'stone_l', perch=1, x=.1, y=.2, b=1, eye='-')],
        [(.4, 'rest')], g='rest', act=('sit', 'stone'), prefer=['tired', 'lonely'])
    o.r('lean_against_the_reed_stem', 'Leaning back against the low reed stem and sighing at the water', 18, 'none',
        [k(.15, x=.4, y=.2, b=.2, r=1), k(.4, 'reed_low', x=-.9, y=.5, b=1, w=.4), k(.7, 'reed_low', x=-1, y=.7, b=1.3, eye='-', mark='sigh', l=1), k(.9, x=.3, y=.2, b=.3)],
        [], g='rest', act=('lean', 'reeds'), prefer=['tired', 'sad'])
    o.r('wait_for_a_koi_to_rise', 'Waiting with his bill an inch above the water for a koi to rise and look at him', 24, 'none',
        [k(.15, 'shallow_m', x=.8, y=.9, b=.6, eye='o'), k(.4, 'shallow_m', x=1.4, y=1.7, b=1.5, eye='o'), k(.65, 'shallow_m', x=1.9, y=2.2, b=2, eye='O', mark='...'), k(.85, x=.1, y=.2, b=.3, eye='-')],
        [], g='rest', act=('wait', 'surface'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.3, dict(lure=0)), (.55, dict(lure=1)), (.8, dict(lure=1))], say=["Come up. Say hello. No? Fine.", "Waited. It rose. It looked. I won."])
    o.r('sulk_at_the_edge_of_the_pond', 'Turning his tail to the pond and sulking while the koi carry on without him', 22, 'none',
        [k(.15, x=-.7, y=.4, b=.4, l=1), k(.4, 'tuft', x=-1.4, y=1, b=1.2, eye='-'), k(.7, 'tuft', x=-1.5, y=1.2, b=1.4, w=.6, r=1, eye='-', mark='hmph'), k(.9, x=-.3, y=.3, b=.4)],
        [], g='rest', act=('sulk', 'pond'), when=['sad'])
    # ---------------- weather
    o.r('chip_the_ice_skin_at_the_rim', 'Chipping the skin of ice off the rim with his bill, breaking a gap for the koi to breathe at', 20, 'none',
        [k(.12, x=.4, y=.7, b=.5), k(.3, 'shallow_l', x=1.3, y=1.5, b=1, mark='tak'), k(.5, 'shallow_m', x=1.3, y=1.6, b=1.1, l=1, mark='TAK'), k(.7, 'shallow_m', x=1, y=1.3, b=.9, r=1, mark='crk'), k(.88, eye='^')],
        [(.5, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'], say=["Hole made. Fish can breathe. You are welcome, fish.", "Ice cracked. Ice complained."])
    o.r('flap_the_surface_to_stir_the_air_in', 'Slapping the surface with both wings in turn at the rim to churn fresh air down into the water', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.3, y=.7, b=.5), k(.3, 'shallow_m', reach=1, x=.4, y=.9, b=.7, w=1, l=1, mark='SPLAT'), k(.5, 'shallow_r', reach=1, x=.5, y=.9, b=.8, w=1, r=1, mark='SPLAT'), k(.7, 'shallow_m', reach=1, x=.4, y=.9, b=.7, w=1, l=1, mark='splat'), k(.88, eye='^')],
        [(.5, 'stir')], g='weather', act=('splash', 'surface'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('hunker_in_the_reeds_in_the_rain', 'Hunkering at the low reed stem with his tail to the rain, drops whipping the ripples flat', 32, 'none',
        [k(.12, 'reed_low', x=-.5, y=.9, b=1.3, l=1), k(.3, 'reed_low', x=-1.2, y=1.8, b=2.1, w=.2, eye='-'), k(.58, 'reed_low', x=-1.3, y=2, b=2.4, r=1, eye='-', mark='drip'), k(.82, 'reed_low', x=-.6, y=1.1, b=1.6, eye='>')],
        [], g='weather', act=('shelter', 'reeds'), when=['wet'])
    o.r('bask_on_the_warm_front_stone', 'Basking on the warm middle stone with his wings half open and his eyes shut', 26, 'none',
        [k(.15, 'stone_m', perch=1, x=-.2, y=-.3, b=.6), k(.45, 'stone_m', perch=1, x=-.4, y=-.8, b=1.2, w=.5, eye='-'), k(.7, 'stone_m', perch=1, x=-.5, y=-1, b=1.4, w=.8, eye='-', mark='mm'), k(.9, 'stone_m', perch=1, y=.2, b=.4, eye='^')],
        [], g='weather', act=('warm', 'stones'), when=['sun'], prefer=['tired'])
    o.r('scrape_the_frost_off_the_stones', 'Scraping the frost off the front stones with the edge of a wing before the koi rise', 18, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.5), k(.3, 'stone_l', reach=1, x=.5, y=1.2, b=.9, mark='skrt'), k(.5, 'stone_m', reach=1, x=.5, y=1.3, b=1, l=1, mark='skrt'), k(.7, 'stone_r', reach=1, x=.4, y=1.2, b=.9, r=1, mark='skrt'), k(.88, eye='-')],
        [(.5, 'crack')], g='weather', act=('scrape', 'frost'), when=['pond_ice>.2'])
    # ---------------- show
    o.r('bow_to_the_koi', 'Bowing deep to the koi at the rim, bill almost skimming the water', 16, 'none',
        [k(.15, x=-.4, y=-.8, b=-.5, w=.6, l=1), k(.4, 'shallow_l', x=1.4, y=1.8, b=1.1, w=.9, r=1), k(.65, 'shallow_l', x=1.5, y=2, b=1.3, w=1, mark='...'), k(.88, x=-.3, y=-.6, b=-.3, w=.3, eye='^')],
        [], g='show', act=('bow', 'koi'), prefer=['happy'])
    o.r('flourish_a_wing_at_the_koi', 'Flourishing a wing at the koi like the headline act of the whole yard', 16, 'wing',
        [k(.15, reach=.3, x=-.6, y=.3, b=.6, r=1), k(.38, 'shallow_m', reach=1, x=.9, y=-.2, w=.8, b=-.3), k(.62, 'shallow_r', reach=1, x=1.1, y=-.4, w=.5, b=-.6, l=1, mark='ta-da'), k(.85, reach=0, y=.6, b=.5, eye='^')],
        [], g='show', act=('present', 'koi'), prefer=['happy'])
    o.r('strike_a_pose_on_the_middle_stone', 'Striking a pose on the middle front stone with one wing out over the water, a statue by the pond', 20, 'none',
        [k(.12, 'stone_m', perch=1, x=.2, y=-.3, b=-.2, w=.3), k(.38, 'stone_m', perch=1, x=.5, y=-1, b=.4, w=1, l=1), k(.65, 'stone_m', perch=1, x=.5, y=-1.3, b=.6, w=.6, r=1, mark='...'), k(.88, y=.3, b=.3, eye='^')],
        [], g='show', act=('pose', 'stone'), prefer=['happy'])
    o.r('argue_with_the_koi_over_the_flakes', 'Arguing with the koi over the last flake, jabbing his bill at the water and being ignored', 18, 'none',
        [k(.15, x=.7, y=.4, b=.4, eye='>'), k(.3, 'shallow_r', x=1.4, y=1.2, b=.8, w=.7, mark='MINE'), k(.5, x=-.3, y=.3, b=.6, l=1, r=1), k(.7, 'shallow_r', x=1.5, y=1.3, b=.9, w=1, mark='MINE!'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'koi'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It ate it. I said it was mine. It heard nothing.", "Argued with a fish. Lost on volume."])
    o.r('shout_across_the_pond_at_the_cattails', 'Shouting across the pond at the far cattails, wings cupped round his bill, to hear it echo', 14, 'wing',
        [k(.15, x=.6, y=-.2, b=.5), k(.35, reach=1, x=1.5, y=-1.8, b=-1, w=.7, mark='HOOOY'), k(.6, reach=.6, x=1.4, y=-1.9, b=-.9, r=1, w=.5, mark='HOOOY'), k(.85, x=-.4, y=.4, b=.5, eye='-')],
        [], g='show', far=True, act=('shout', 'cattails'), prefer=['happy', 'young'])
    o.r('sing_the_koi_a_slow_song', 'Singing the koi a slow song from the rim, a wing over his heart, while it hangs listening', 24, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, 'shallow_m', reach=1, x=.3, y=.8, b=.5, w=.4, mark='laaa'), k(.5, 'shallow_m', reach=1, x=.4, y=.9, b=.6, w=.5, l=1, mark='LAAA'), k(.7, 'shallow_m', reach=1, x=.3, y=.7, b=.5, r=1, mark='la'), k(.88, eye='^')],
        [(.5, 'kiss')], g='show', act=('sing', 'koi'), pick='shyest', prefer=['happy', 'lonely'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It listens. It hasn't left. That is a review.", "A love song for a fish. I would do it again."])
    # ---------------- mishap
    o.r('skid_off_the_wet_stone', 'Skidding off the wet front stone and ending flat on his belly at the rim, bill almost in the water', 16, 'none',
        [k(.15, 'stone_l', x=.4, y=.3, b=.4, l=1), k(.3, x=.6, y=-.4, b=-.8, w=1, l=1, r=1, eye='O', mark='WAH'), k(.5, 'shallow_l', x=1.3, y=1.9, b=1.7, w=.8, eye='@', mark='splat'), k(.8, x=.2, y=.6, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'stones'), when=['wet'], prefer=['young'])
    o.r('bill_caught_in_a_koi_s_hungry_mouth', 'Dipping a bill to the surface and having the koi clamp on, hauling him down the rim until it lets go', 22, 'none',
        [k(.15, 'shallow_l', x=.8, y=.9, b=.6), k(.32, 'shallow_l', x=1.3, y=1.6, b=1, eye='O', mark='mmf'), k(.5, 'shallow_l', x=.6, y=1.9, b=1.6, l=1, eye='@', mark='mrrf'), k(.68, 'shallow_l', x=-.5, y=1.1, b=.8, r=1, w=1, mark='POP'), k(.86, x=-.8, y=.4, b=.5, eye='>')],
        [], g='mishap', act=('stuck', 'bill'), pick='hungriest', prefer=['young', 'grumpy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.7, dict(lure=0))], say=["It has a mouth like a hoover. Bill: stuck. Dignity: gone.", "Let go! It did. Eventually. Hostile fish."])
    o.r('back_into_the_reeds_in_the_dark', 'Backing into the reed stem at night while watching the water and bouncing off with a squeak', 14, 'none',
        [k(.15, x=-.4, y=.8, b=.7, r=1), k(.3, 'reed_low', x=-1.4, y=.6, b=1.3, eye='O', mark='oof'), k(.5, x=1, y=-.8, b=-1, w=.9, l=1, eye='@'), k(.8, x=.3, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'reeds'), when=['night'])
    o.r('leap_back_from_a_sudden_splash', 'Leaping back from a sudden splash as the koi surges up, landing on his tail with wings flung wide', 16, 'none',
        [k(.15, 'shallow_r', x=.8, y=.9, b=.6), k(.3, 'shallow_r', x=-.2, y=-.8, b=-1.3, w=1, eye='O', mark='WAH'), k(.5, x=-1.2, y=-1.2, b=-1.6, w=1, l=1, r=1, eye='@'), k(.72, x=-.4, y=.9, b=1.1, w=.4, eye='>', mark='plop'), k(.9, eye='-')],
        [], g='mishap', act=('hop', 'back'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.45, dict(lure=1))], say=["It attacked. A fish. It attacked me.", "Splashed. Jumped. Pretended I meant to."])
    o.r('stamp_at_the_stone_when_the_koi_ignores_him', 'Stamping at the middle stone when the koi turns tail and swims off, then hopping about holding one foot', 16, 'none',
        [k(.15, x=.2, y=-.3, b=-.5, l=1), k(.3, 'stone_m', x=.1, y=.5, b=.8, l=1, mark='STOMP'), k(.5, x=-.2, y=-.6, b=-.9, r=1, w=.8, eye='O', mark='OW'), k(.7, 'stone_m', x=.1, y=.4, b=.7, r=1, mark='STOMP'), k(.9, eye='-')],
        [], g='mishap', act=('stamp', 'stones'), prefer=['grumpy'])
    # ---------------- duets (a friend takes their own part)
    o.r('sweep_the_leaves_in_from_both_banks', 'Sweeping the floating leaves in from both banks with a friend until they meet in a heap at the middle', 24, 'wing',
        [k(.12, 'shallow_l', reach=.6, x=.3, y=.7, b=.4), k(.3, 'shallow_l', reach=1, x=.5, y=.9, b=.7, mark='swsh'), k(.5, 'shallow_m', reach=1, x=.6, y=1, b=.8, l=1, mark='swsh'), k(.7, 'shallow_m', reach=1, x=.5, y=.9, b=.7, r=1), k(.88, eye='^')],
        [(.5, 'scoop')], g='care', act=('rake', 'surface'), prefer=['pond_leaves>.3', 'happy'],
        duo=[k(.12, 'shallow_r', reach=.6, x=.3, y=.7, b=.4), k(.3, 'shallow_r', reach=1, x=.5, y=.9, b=.7, mark='swsh'), k(.5, 'shallow_m', reach=1, x=.6, y=1, b=.8, r=1, mark='swsh'), k(.7, 'shallow_m', reach=1, x=.5, y=.9, b=.7, l=1), k(.88, eye='^')])
    o.r('pour_flakes_while_a_friend_scatters', 'Pouring a thin line of flakes from his bill while a friend scatters wings of them from the far rim', 22, 'none',
        [k(.12, x=.5, y=.7, b=.5), k(.3, 'shallow_l', x=1.2, y=1.5, b=1, mark='...'), k(.5, 'shallow_l', x=1.3, y=1.6, b=1.1, l=1, mark='tssss'), k(.7, 'shallow_l', x=.8, y=1, b=.6, w=.4, eye='O'), k(.88, eye='^')],
        [(.5, 'scatter')], g='use', act=('pour', 'flakes'), when=['pond_flakes<.4'], prefer=['happy'],
        duo=[k(.12, 'shallow_r', reach=.6, w=.5), k(.34, 'shallow_r', reach=1, b=-.3, w=1, mark='~~~'), k(.6, x=-.3, y=.2, eye='o'), k(.82, eye='^')])
    o.r('count_the_koi_with_a_friend', 'Counting the koi one by one with a friend leaning over the rim beside him, and arguing the total', 22, 'none',
        [k(.12, x=.5, y=.5, b=.4), k(.3, 'shallow_l', x=1, y=1.2, b=.8, mark='one'), k(.5, 'shallow_m', x=1.1, y=1.3, b=.9, l=1, mark='two'), k(.7, 'shallow_m', x=.9, y=1.1, b=.8, eye='>', mark='THREE'), k(.88, eye='-')],
        [], g='test', act=('count', 'koi'), prefer=['curious', 'happy'], pick='hungriest', obj=[(.3, dict(lure=1)), (.6, dict(lure=1))],
        duo=[k(.15, x=.5, y=.5, b=.4), k(.35, 'shallow_r', x=1.1, y=1.2, b=.8, mark='one'), k(.55, 'shallow_m', x=1.1, y=1.3, b=.9, r=1, mark='FOUR'), k(.75, 'shallow_m', x=.9, y=1.1, b=.8, eye='>', mark='no'), k(.9, eye='-')])
    o.r('herd_the_koi_from_both_ends_of_the_rim', 'Running along the rim from the left while a friend runs from the right, the koi caught between them', 24, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.3, 'shallow_l', x=1.3, y=.4, b=-.5, r=1, w=.5), k(.5, 'shallow_m', x=1.4, y=.4, b=-.6, l=1, w=.6), k(.7, 'shallow_m', x=.6, y=.6, b=.6, eye='O', mark='gotcha'), k(.88, eye='^')],
        [], g='play', act=('chase', 'koi'), pick='hungriest', prefer=['happy', 'young'], obj=[(.15, dict(lure=1)), (.4, dict(lure=1)), (.6, dict(lure=1))],
        duo=[k(.1, 'shallow_r', x=.6, y=.5, b=.6, r=1), k(.3, 'shallow_r', x=1.3, y=.4, b=-.5, l=1, w=.5), k(.5, 'shallow_m', x=1.4, y=.4, b=-.6, r=1, w=.6), k(.7, 'shallow_m', x=.6, y=.6, b=.6, eye='O', mark='gotcha'), k(.88, eye='^')],
        say=["Pincer movement. Koi slipped away. Embarrassing.", "We herded one fish for ten minutes. We won."])
    o.r('nudge_a_cattail_head_to_make_it_nod', 'Nudging the nearest cattail head with a twig until the whole stem nods back and forth', 18, 'twig',
        [k(.12, 'cattail_l', reach=.6, x=.3, y=-.5, b=-.2), k(.3, 'cattail_l', reach=1, x=.6, y=-.9, b=.3, mark='bop'), k(.5, 'cattail_l', reach=1, x=.6, y=-.9, b=.4, l=1, mark='bop'), k(.7, x=-.3, y=-.5, w=.4, eye='O', mark='nod'), k(.88, eye='^')],
        [], g='play', act=('nudge', 'cattail'), ages=GROWN, prefer=['young', 'happy'])
    o.r('lean_on_the_right_bank_stones', 'Leaning his shoulder against the right bank stones and watching the koi pass below', 22, 'none',
        [k(.15, x=.3, y=.2, b=.3, r=1), k(.4, 'bank_r', x=-.9, y=.5, b=1, w=.4, eye='o'), k(.7, 'bank_r', x=-1, y=.6, b=1.3, eye='-', mark='...', l=1), k(.9, x=.2, y=.2, b=.3)],
        [], g='rest', act=('lean', 'bank'), prefer=['tired', 'lonely'])
    # @@END koi
    return done(o)


def goldfish():
    # Host koi_pond (see koi). A goldfish is small, quick and greedy: it zigzags after a wing, darts at flakes one by one, nibbles toes and bill, can be trained to
    # come to a call, and cannot be trusted to remember him. The same rim spots as koi, played differently: a small lure that darts, not a heavy one that glides.
    P = pm('koi_pond')
    o = Obj('goldfish', 'keeping', on='koi_pond',
            fields=dict(learned=(0, 0, 1)),
            physics=[('learned', 'rate', -.0003, 'always')],
            effects=dict(tidy=[('keeping.clarity', 'add', .15)], scoop=[('keeping.leaves', 'mul', .4)], thin=[('keeping.plants', 'mul', .75)],
                         unsnag=[('subject.health', 'add', .15), ('subject.trust', 'add', .1)], crack=[('keeping.ice', 'mul', .3)], stir=[('keeping.oxygen', 'add', .3)],
                         scour=[('keeping.algae', 'mul', .5)], call=[('keeping.bell', 'add', .5), ('learned', 'add', .35)], scatter=[('keeping.flakes', 'add', .4)],
                         feed=[('subject.hunger', 'add', -.2), ('subject.trust', 'add', .1)], tickle=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         lead=[('learned', 'add', .15), ('subject.trust', 'add', .1)], cloud=[('keeping.clarity', 'add', -.2), ('keeping.flakes', 'add', .6)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(shallow_l=P(28, 43), shallow_m=P(58, 41), shallow_r=P(88, 39), pad_r=P(86, 37), tuft=P(11, 44), reed_low=P(8, 38),
                         stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46)))
    # ---------------- care
    o.r('fish_a_leaf_out_by_its_stem', 'Fishing a floating leaf out by its stem with the tip of his bill and flicking it onto the bank', 18, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_l', x=1.3, y=1.5, b=1, mark='snk'), k(.5, 'shallow_l', x=.3, y=.3, b=-.3, w=.4, l=1, mark='fwip'), k(.72, 'tuft', x=.6, y=.8, b=.4, eye='^'), k(.9, eye='-')],
        [(.5, 'scoop')], g='care', act=('pull', 'leaf'), prefer=['pond_leaves>.3', 'curious'], say=["One leaf. Out. The pond acts like it never happened.", "Bill-fishing. Catch of the day: foliage."])
    o.r('brush_the_grit_off_the_stones', 'Brushing the grit off the front stones in short strokes so none of it washes back into the water', 20, 'wing',
        [k(.12, 'stone_l', reach=.6, x=.3, y=.9, b=.5), k(.3, 'stone_l', reach=1, x=.4, y=1.1, b=.8, l=1, mark='shk'), k(.5, 'stone_m', reach=1, x=.5, y=1.2, b=.9, mark='shk'), k(.7, 'stone_r', reach=1, x=.4, y=1.1, b=.8, r=1), k(.88, eye='^')],
        [(.5, 'tidy')], g='care', act=('sweep', 'grit'), when=['pond_clarity<.6'])
    o.r('uproot_a_clump_of_weed', 'Uprooting a clump of weed at the shallow end with a long steady pull of his bill', 22, 'none',
        [k(.12, x=.5, y=.7, b=.5), k(.3, 'shallow_r', x=1.2, y=1.6, b=1.1, mark='hnn'), k(.5, 'shallow_r', x=.8, y=1.8, b=1.5, l=1, mark='HNNG'), k(.7, 'shallow_r', x=-.5, y=.4, b=-.3, w=.8, r=1, mark='plop'), k(.88, y=.5, eye='^')],
        [(.5, 'thin')], g='care', act=('dig', 'weeds'), when=['pond_plants>.7'])
    o.r('untangle_the_line_from_its_tail', 'Untangling a thread of pond weed from the goldfish\'s fan tail with a patient bill, one twist at a time', 24, 'none',
        [k(.12, x=.4, y=.5, b=.5), k(.3, 'shallow_m', x=1, y=1.4, b=1, eye='-'), k(.5, 'shallow_m', x=1.1, y=1.6, b=1.1, l=1, mark='tweak'), k(.7, 'shallow_m', x=.5, y=.7, b=.5, w=.4, mark='plip'), k(.88, eye='^')],
        [(.5, 'unsnag')], g='care', act=('unwrap', 'tail'), pick='shyest', when=['fish_health<.8'], obj=[(.25, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- use
    o.r('tap_the_surface_for_the_dinner_call', 'Tapping the surface with his bill to the dinner call, twice quick and once slow, until the goldfish learn it', 20, 'none',
        [k(.12, 'shallow_l', x=1.3, y=1.4, b=.8, mark='tp'), k(.26, 'shallow_l', x=1.3, y=1.4, b=.8, l=1, mark='tp'), k(.42, x=-.2, y=-.2, b=-.2, w=.3), k(.58, 'shallow_l', x=1.4, y=1.5, b=.9, r=1, mark='TAP'), k(.85, eye='^')],
        [(.58, 'call')], g='use', act=('tap', 'surface'), when=['learned<.7'], prefer=['dusk', 'dawn'], pick='hungriest', obj=[(.4, dict(lure=0)), (.65, dict(lure=1))], say=["Tap tap tap. They are learning. One of them is.", "A call. Dinner. They remember for a whole minute."])
    o.r('tip_flakes_from_a_wing_tip', 'Tipping flakes out one at a time from the point of a wing, each one gone before it lands', 16, 'wing',
        [k(.15, 'shallow_m', reach=.6, w=.4), k(.35, 'shallow_m', reach=1, x=.2, b=-.2, w=.7, mark='tp'), k(.55, 'shallow_r', reach=1, x=.3, b=-.3, w=.8, mark='tp'), k(.78, x=-.2, y=.2, eye='o'), k(.9, eye='^')],
        [(.35, 'scatter')], g='use', act=('tip', 'flakes'), when=['pond_flakes<.4'])
    o.r('dangle_a_flake_and_snatch_it_back', 'Showing a flake at the surface, letting the goldfish rise for it, then snatching it up and showing it again', 22, 'none',
        [k(.12, 'shallow_r', x=.8, y=.9, b=.6), k(.28, 'shallow_r', x=1.2, y=1.4, b=1, eye='o', mark='...'), k(.42, 'shallow_r', x=.2, y=-.4, b=-.5, w=.5, eye='>', mark='nope'), k(.58, 'shallow_r', x=1.3, y=1.6, b=1.1, eye='O'), k(.78, 'shallow_r', x=.6, y=.8, b=.5, eye='^', mark='gulp')],
        [(.78, 'feed')], g='use', act=('show', 'flake'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.25, dict(lure=1)), (.45, dict(lure=0)), (.55, dict(lure=1)), (.8, dict(lure=1))], say=["Nope. Again. Nope. Fine, take it.", "I am the dinner service. With a sense of humour."])
    o.r('let_it_nibble_the_tip_of_his_bill', 'Letting the goldfish nibble the very tip of his bill, holding still and trying not to laugh', 20, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'shallow_m', x=1.4, y=1.6, b=1.1, eye='-'), k(.5, 'shallow_m', x=1.4, y=1.7, b=1.2, l=1, eye='-', mark='ti hi'), k(.7, 'shallow_m', x=1.2, y=1.5, b=1, r=1, w=.3, eye='>'), k(.88, eye='^')],
        [(.5, 'tickle')], g='use', act=('tap', 'bill'), pick='shyest', prefer=['happy', 'lonely'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))], say=["Nibbles. Little ones. I am a very long snack.", "Tickles. Do not tell anyone I laughed."])
    o.r('trail_a_wing_so_it_zigzags_after_it', 'Trailing a wing along the surface so the goldfish zigzags after the tip, left, right, left again', 24, 'wing',
        [k(.1, 'shallow_l', reach=.6, x=.2, y=.6, b=.4), k(.26, 'shallow_m', reach=1, x=.4, y=.7, b=.5, l=1), k(.42, 'shallow_l', reach=1, x=.3, y=.7, b=.5, r=1), k(.58, 'shallow_r', reach=1, x=.5, y=.7, b=.5, l=1), k(.76, 'shallow_m', reach=1, x=.4, y=.7, b=.5), k(.9, eye='^')],
        [(.58, 'lead')], g='use', act=('drag', 'wing'), pick='hungriest', when=['learned<.8'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.45, dict(lure=1)), (.6, dict(lure=1)), (.78, dict(lure=1))])
    o.r('count_the_flakes_by_the_snatches', 'Dropping flakes one by one and counting each snatch aloud until the goldfish stops being hungry', 24, 'none',
        [k(.12, 'shallow_r', x=.7, y=.8, b=.5, mark='1'), k(.3, 'shallow_r', x=.9, y=1, b=.7, l=1, mark='2'), k(.5, 'shallow_r', x=1, y=1.1, b=.8, mark='3'), k(.7, 'shallow_r', x=1.1, y=1.2, b=.9, r=1, mark='4'), k(.88, eye='-', mark='ten')],
        [(.5, 'feed')], g='use', act=('count', 'flakes'), pick='hungriest', when=['fish_hunger>.5'], obj=[(.25, dict(lure=1)), (.6, dict(lure=1))], say=["Eight flakes. It always wants nine.", "Counted. Fed. Insatiable. I know the feeling."])
    o.r('hoist_a_flake_for_it_to_leap_at', 'Hoisting a flake up high between his bill tips so the goldfish has to leap clear of the water for it', 22, 'none',
        [k(.12, 'shallow_l', x=.6, y=.5, b=.5), k(.3, 'shallow_l', x=.5, y=-.7, b=-.5, eye='o'), k(.5, 'shallow_l', x=.6, y=-1, b=-.8, eye='O', mark='hup'), k(.7, 'shallow_l', x=.8, y=.3, b=.4, w=.5, eye='^', mark='gulp'), k(.9, eye='-')],
        [(.7, 'feed')], g='use', act=('lift', 'flake'), pick='hungriest', when=['fish_hunger>.4'], ages=GROWN, obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=0))], say=["Jumped. A tiny fish. A tiny, majestic fish.", "It got air. I got a flake-shaped hole in my pride."])
    o.r('weave_a_wing_between_the_stems', 'Weaving a wing between the stems of the reeds at the pond edge, the goldfish threading after it', 22, 'wing',
        [k(.1, 'reed_low', reach=.6, x=.2, y=.5, b=.3), k(.3, 'tuft', reach=1, x=.4, y=.8, b=.6, r=1), k(.5, 'reed_low', reach=1, x=.3, y=.7, b=.5, l=1), k(.7, 'shallow_l', reach=1, x=.5, y=.7, b=.6), k(.88, eye='^')],
        [(.7, 'lead')], g='use', act=('chase', 'stems'), pick='hungriest', when=['learned<.8'], obj=[(.15, dict(lure=1)), (.35, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    # ---------------- play
    o.r('blow_a_big_bubble_and_watch_it_pop', 'Blowing a big bubble at the surface and watching the goldfish dart up to burst it', 18, 'none',
        [k(.12, x=.4, y=.6, b=.4), k(.3, 'shallow_l', x=1.2, y=1.4, b=.9, mark='blooo'), k(.5, 'shallow_l', x=1.4, y=1.6, b=1.1, eye='O', mark='bloooo'), k(.66, x=-.5, y=-.4, b=-.3, w=.6, eye='O', mark='POP'), k(.88, eye='^')],
        [], g='play', act=('blow', 'bubble'), pick='shyest', prefer=['young', 'happy'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))], say=["Pop. Both of us jumped. One of us pretended not to.", "Biggest bubble yet. Smallest audience."])
    o.r('play_red_light_green_light_along_the_rim', 'Playing red light, green light with the goldfish, dashing along the rim and freezing the moment it freezes', 24, 'none',
        [k(.1, 'shallow_l', x=.6, y=.5, b=.6, l=1), k(.26, 'shallow_m', x=1.2, y=.3, b=-.5, r=1, w=.5), k(.4, 'shallow_m', x=.3, y=.2, b=.2, w=.2, eye='O', mark='red!'), k(.56, 'shallow_r', x=1.3, y=.3, b=-.6, l=1, w=.6), k(.72, 'shallow_r', x=.3, y=.2, b=.2, eye='O', mark='RED!'), k(.9, eye='^')],
        [(.56, 'fun')], g='play', act=('race', 'goldfish'), pick='hungriest', prefer=['young', 'happy'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.74, dict(lure=1))], say=["It froze first. I moved. It is cheating by being a fish.", "Green light. Red light. It won. It always wins."])
    o.r('circle_a_wing_and_spin_it_round', 'Circling a wing over the water and turning with it so the goldfish swims round in a ring after him', 22, 'wing',
        [k(.1, 'shallow_m', reach=.6, x=.2, y=.5, b=.3), k(.28, 'shallow_m', reach=1, x=.5, y=.5, b=.4, w=.5, l=1), k(.46, 'shallow_r', reach=1, x=.6, y=.5, b=.4, w=.6, r=1), k(.64, 'shallow_l', reach=1, x=.5, y=.5, b=.4, w=.5, l=1), k(.82, 'shallow_m', reach=.6, x=.3, y=.4, b=.3, eye='@'), k(.92, eye='^')],
        [], g='play', act=('spin', 'goldfish'), pick='hungriest', prefer=['happy', 'young'], obj=[(.15, dict(lure=1)), (.32, dict(lure=1)), (.5, dict(lure=1)), (.68, dict(lure=1)), (.85, dict(lure=1))])
    o.r('walk_the_stones_with_a_flake_on_his_bill', 'Balancing a flake on the tip of his bill and walking the front stones without dropping it', 24, 'none',
        [k(.12, 'stone_l', perch=1, x=.9, y=.1, b=.3, eye='o'), k(.3, 'stone_l', perch=1, x=1.2, y=-.1, b=.5, l=1, w=.5, eye='O'), k(.5, 'stone_m', perch=1, x=1.2, y=-.1, b=.5, r=1, w=.6, eye='O'), k(.7, 'stone_m', perch=1, x=1, y=.1, b=.3, l=1, w=.4, mark='hm'), k(.88, y=.3, b=.2, eye='^')],
        [], g='play', act=('balance', 'flake'), ages=GROWN, prefer=['curious', 'happy'])
    o.r('hop_the_stones_in_time_with_its_darts', 'Hopping along the front stones in time with the goldfish\'s darts, one hop to each dash', 22, 'none',
        [k(.1, 'stone_l', x=.3, y=.4, b=-.6, l=1), k(.28, 'stone_m', x=.4, y=.4, b=-.9, r=1, w=.4), k(.46, 'stone_m', x=.3, y=.4, b=-.6, l=1), k(.64, 'stone_r', x=.4, y=.4, b=-.9, r=1, w=.5), k(.84, 'stone_r', x=.3, y=.3, b=-.5, eye='^')],
        [], g='play', act=('hop', 'stones'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=1))])
    o.r('drum_the_ripples_back_and_forth', 'Drumming the rippling surface with his bill and watching the goldfish dart in over each ring', 20, 'none',
        [k(.12, 'shallow_r', x=1.2, y=1.3, b=.6, mark='ba'), k(.3, 'shallow_m', x=1.2, y=1.3, b=.6, l=1, mark='da'), k(.48, 'shallow_l', x=1.3, y=1.4, b=.7, r=1, mark='ba'), k(.66, 'shallow_m', x=1.3, y=1.4, b=.7, mark='DUM'), k(.86, eye='^')],
        [], g='play', act=('drum', 'ripples'), pick='shyest', prefer=['happy', 'young'], obj=[(.15, dict(lure=1)), (.35, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    # ---------------- test
    o.r('peer_close_at_its_scales', 'Peering close at the goldfish\'s scales as it hangs at the surface, trying to see where one ends', 20, 'none',
        [k(.12, x=.5, y=.6, b=.4), k(.3, 'shallow_l', x=1, y=1.2, b=.8, eye='o'), k(.5, 'shallow_l', x=1.2, y=1.5, b=1, eye='O', mark='...'), k(.72, 'shallow_l', x=.6, y=.6, b=.5, w=.4, eye='^'), k(.9, eye='-')],
        [], g='test', act=('peer', 'scales'), pick='shyest', prefer=['curious'], obj=[(.28, dict(lure=1)), (.62, dict(lure=1))])
    o.r('count_the_scales_down_its_flank', 'Counting the scales down its flank, nose to tail, losing count at the fins and starting again', 22, 'none',
        [k(.12, 'shallow_l', x=.6, y=2, b=1.6, mark='1'), k(.3, 'shallow_m', x=.7, y=2.2, b=1.8, mark='2'), k(.5, 'shallow_m', x=.8, y=2.4, b=2, l=1, mark='3'), k(.7, 'shallow_r', x=.7, y=2.2, b=1.8, eye='>', mark='no'), k(.88, eye='-', mark='lots')],
        [], g='test', act=('count', 'scales'), pick='hungriest', prefer=['curious'], obj=[(.28, dict(lure=1)), (.6, dict(lure=1))], say=["Forty. Fifty. It moved. Start again.", "Scales: many. Patience: fewer."])
    o.r('hold_up_a_tail_feather_to_compare_tails', 'Holding up a tail feather of his own beside the goldfish\'s fan tail to compare which is the better tail', 20, 'wing',
        [k(.12, 'shallow_m', reach=.5, x=.3, y=.4, b=.3), k(.3, 'shallow_m', reach=1, x=.3, y=.8, b=.8, w=.4, l=1), k(.5, 'shallow_r', reach=1, x=.4, y=.7, b=.7, w=.6, r=1, mark='hm'), k(.72, 'shallow_r', reach=.6, x=.2, y=.5, b=.4, w=.3, eye='>'), k(.9, eye='^')],
        [], g='test', act=('compare', 'tails'), pick='shyest', prefer=['curious', 'happy'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('listen_to_the_bubbles_pop', 'Cocking an ear to the surface to listen to the tiny bubbles pop around the goldfish\'s mouth', 18, 'none',
        [k(.15, x=.3, y=.7, b=.5), k(.4, 'shallow_r', x=.3, y=1.8, b=1.4, eye='-'), k(.62, 'shallow_r', x=.3, y=1.9, b=1.5, l=1, eye='-', mark='pip'), k(.85, x=-.4, y=-.5, w=.4, eye='O')],
        [], g='test', act=('listen', 'bubbles'), pick='shyest', prefer=['curious', 'lonely'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))])
    o.r('sniff_a_single_flake', 'Sniffing a single flake held up in his bill and pulling a face at the smell', 14, 'none',
        [k(.15, x=.4, y=.4, b=.3), k(.35, 'shallow_r', x=1.2, y=1.1, b=.8, mark='snf'), k(.55, x=-.6, y=-.4, b=-.3, w=.6, l=1, eye='>', mark='gah'), k(.8, y=.3, eye='-')],
        [], g='test', act=('sniff', 'flakes'), prefer=['curious', 'young'])
    o.r('dip_a_reed_to_measure_the_shallows', 'Dipping a reed at the shallow end to find how deep the water goes, and noting it with a nod', 20, 'reed',
        [k(.12, 'shallow_r', reach=.5, x=.2, y=.4, b=.3), k(.3, 'shallow_r', reach=1, x=.4, y=.8, b=.7, mark='plnk'), k(.5, 'shallow_m', reach=1, x=.5, y=.9, b=.8, l=1, mark='plnk'), k(.7, 'shallow_l', reach=1, x=.4, y=.8, b=.7, r=1), k(.88, eye='-', mark='deep')],
        [], g='test', act=('measure', 'depth'), prefer=['curious'])
    # ---------------- rest
    o.r('doze_with_his_chin_on_the_stone', 'Dozing off with his chin resting against the middle stone and the goldfish dimpling the water nearby', 28, 'none',
        [k(.15, x=.5, y=.5, b=.5), k(.4, 'stone_m', x=.7, y=1.5, b=1.4, eye='-'), k(.7, 'stone_m', x=.7, y=1.8, b=1.7, w=.3, eye='-', mark='zzz'), k(.9, x=-.3, y=-.3, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'stone'), when=['tired'])
    o.r('sit_beside_the_tuft_and_hum', 'Sitting beside the grass tuft with his feet tucked, humming to himself while the goldfish circles', 24, 'none',
        [k(.15, x=.3, y=.4, b=.7), k(.4, 'tuft', x=.2, y=.8, b=1.4, eye='o'), k(.65, 'tuft', x=.2, y=.7, b=1.5, l=1, eye='-', mark='hm hm'), k(.85, x=.1, y=.2, b=.8, eye='^')],
        [(.4, 'rest')], g='rest', act=('sit', 'tuft'), prefer=['sad', 'lonely'])
    o.r('lean_back_against_the_reed_foot', 'Leaning back against the foot of the reeds with his wings loose, watching the water go gold', 22, 'none',
        [k(.15, x=.3, y=.2, b=.3, l=1), k(.4, 'reed_low', x=-.8, y=.6, b=1.1, w=.4), k(.7, 'reed_low', x=-.9, y=.8, b=1.4, w=.3, eye='-', mark='ahh', r=1), k(.9, x=.2, y=.2, b=.3)],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'happy'])
    o.r('wait_for_it_to_remember_him', 'Waiting at the rim for the goldfish to remember who he is, with an expectant nod each time it surfaces', 26, 'none',
        [k(.15, 'shallow_m', x=.8, y=.9, b=.6, eye='o'), k(.4, 'shallow_m', x=1.2, y=1.1, b=.9, eye='O', mark='hi'), k(.62, 'shallow_m', x=.8, y=.8, b=.6, eye='-', mark='...'), k(.82, 'shallow_m', x=1.3, y=1.2, b=1, eye='O', mark='HI')],
        [], g='rest', act=('wait', 'goldfish'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.35, dict(lure=1)), (.55, dict(lure=0)), (.8, dict(lure=1))], say=["Hi. No? Hi again. Third time, it knows me.", "It forgets me every lap. I am introduced forever."])
    o.r('turn_away_from_a_fish_that_forgot_him', 'Turning away from a goldfish that forgot him again, sulking with his bill sunk against his chest', 22, 'none',
        [k(.15, x=-.8, y=.4, b=.4, r=1), k(.4, 'tuft', x=-1.3, y=1, b=1.1, eye='-'), k(.7, 'tuft', x=-1.4, y=1.2, b=1.3, w=.5, l=1, eye='-', mark='hmph'), k(.9, x=-.3, y=.4, b=.4)],
        [], g='rest', act=('sulk', 'goldfish'), when=['sad'], say=["Forgot me. Again. Three seconds, they said.", "I remembered its name. It did not remember mine. Fine."])
    # ---------------- weather
    o.r('kick_the_ice_loose_at_the_edge', 'Kicking the ice loose at the edge with the flat of a foot, one hard stab at a time, until a gap opens', 20, 'none',
        [k(.12, x=.2, y=.2, b=.5, l=1), k(.3, 'stone_l', x=.3, y=.5, b=-.3, l=1, mark='crk'), k(.48, 'stone_m', x=.3, y=.5, b=-.4, r=1, mark='CRK'), k(.66, 'stone_m', x=.4, y=.6, b=-.2, l=1, mark='crunch'), k(.86, eye='^')],
        [(.48, 'crack')], g='weather', act=('kick', 'ice'), when=['pond_ice>.3'])
    o.r('wipe_the_slime_off_the_reed_foot', 'Wiping the green slime off the foot of the reeds with the back of a wing, stem after stem', 18, 'wing',
        [k(.12, 'reed_low', reach=.6, x=.2, y=.5, b=.4), k(.3, 'reed_low', reach=1, x=.3, y=.7, b=.7, mark='sqk'), k(.5, 'tuft', reach=1, x=.4, y=.9, b=.9, l=1, mark='sqk'), k(.7, 'reed_low', reach=1, x=.3, y=.7, b=.7, r=1), k(.88, eye='-')],
        [(.5, 'scour')], g='weather', act=('wipe', 'reeds'), when=['pond_algae>.4'])
    o.r('shake_a_wing_in_long_strokes_over_the_water', 'Shaking a wing in long slow strokes over the water to stir some air into the shallows', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.2, y=.4, b=.3), k(.3, 'shallow_m', reach=1, x=.3, y=.3, b=-.4, w=.8, mark='fff'), k(.5, 'shallow_r', reach=1, x=.4, y=.3, b=-.5, w=1, r=1, mark='FFF'), k(.7, 'shallow_l', reach=1, x=.3, y=.3, b=-.4, w=.8, l=1, mark='fff'), k(.88, eye='-')],
        [(.5, 'stir')], g='weather', act=('shake', 'wings'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('huddle_at_the_grass_tuft_while_it_pours', 'Huddling at the grass tuft with his tail to the weather while the rain pocks the water', 32, 'none',
        [k(.12, 'tuft', x=-.3, y=.7, b=.8, l=1), k(.3, 'tuft', x=-.9, y=1.4, b=1.4, w=.3, eye='-'), k(.58, 'tuft', x=-1, y=1.6, b=1.6, r=1, eye='-', mark='patter'), k(.82, 'tuft', x=-.5, y=.9, b=.9, eye='>')],
        [], g='weather', act=('shelter', 'tuft'), when=['wet'])
    o.r('cool_his_feet_while_it_nibbles_his_toes', 'Cooling his feet at the rim on a hot day while the goldfish noses at his toes', 24, 'none',
        [k(.12, x=.2, y=.3, b=.5, l=1), k(.32, 'shallow_l', x=.3, y=1.2, b=1.2, l=1, eye='-', mark='ahh'), k(.54, 'shallow_l', x=.3, y=1.4, b=1.4, r=1, eye='-', mark='ti hi'), k(.76, 'shallow_l', x=.2, y=1, b=1, l=1, eye='>', mark='heh'), k(.9, eye='^')],
        [], g='weather', act=('cool', 'feet'), when=['sun'], pick='shyest', prefer=['warm', 'happy'], obj=[(.32, dict(lure=1)), (.62, dict(lure=1))], say=["Cool feet. A nibble. Nobody tell my toes.", "Toe-nibbling. Nobody warned me. Great."])
    # ---------------- show
    o.r('bow_so_low_the_goldfish_bumps_him', 'Bowing so low to the goldfish that it bumps his bill to say hello', 16, 'none',
        [k(.15, x=-.5, y=-.8, b=-.6, w=.6, l=1), k(.4, 'shallow_r', x=1.4, y=1.9, b=1.1, w=.9, r=1), k(.62, 'shallow_r', x=1.5, y=2.1, b=1.3, w=1, mark='bonk'), k(.86, x=-.3, y=-.6, b=-.3, w=.3, eye='^')],
        [], g='show', act=('bow', 'goldfish'), pick='hungriest', prefer=['happy'], obj=[(.45, dict(lure=1)), (.7, dict(lure=1))])
    o.r('present_the_goldfish_to_the_empty_yard', 'Presenting the goldfish to the empty yard with a sweep of one wing, as though it were a famous guest', 18, 'wing',
        [k(.15, reach=.3, x=-.5, y=-.3, b=-.4, r=1), k(.38, 'shallow_l', reach=1, x=.7, y=.2, w=.6, b=-.5), k(.62, 'shallow_m', reach=1, x=.8, y=-.2, w=.5, b=-.7, l=1, mark='tada'), k(.85, reach=0, y=.4, b=.3, eye='^')],
        [], g='show', act=('present', 'goldfish'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))])
    o.r('strike_a_pose_on_the_far_stone', 'Striking a proud pose on the left front stone, bill up, one foot raised, as if guarding the pond', 20, 'none',
        [k(.12, 'stone_l', perch=1, x=.2, y=-.4, b=-.3, w=.4), k(.38, 'stone_l', perch=1, x=.7, y=-1.2, b=.2, w=.9, l=1), k(.65, 'stone_l', perch=1, x=.8, y=-1.4, b=.4, w=.5, r=1, mark='...'), k(.88, y=.3, b=.3, eye='^')],
        [], g='show', act=('pose', 'stone'), prefer=['happy'])
    o.r('argue_with_the_goldfish_about_its_memory', 'Arguing with the goldfish about its memory, wing jabbing, and getting no answer at all', 20, 'none',
        [k(.15, x=.6, y=.4, b=.4, eye='>'), k(.3, 'shallow_m', x=1.3, y=1.3, b=.8, w=.8, mark='REMEMBER'), k(.5, x=-.3, y=.3, b=.6, l=1, r=1), k(.7, 'shallow_m', x=1.4, y=1.4, b=.9, w=1, mark='ME!'), k(.9, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'goldfish'), pick='hungriest', prefer=['grumpy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))], say=["I fed you at noon. You said thanks. You don't remember.", "It has no idea who I am. Good fight."])
    o.r('call_it_by_name_across_the_pond', 'Calling the goldfish by its name across the whole pond, a wing cupped at his bill, over and over', 16, 'wing',
        [k(.15, x=.4, y=-.5, b=-.2), k(.35, reach=1, x=1.2, y=-1.6, b=-.6, w=.7, mark='GOLDIEE'), k(.6, reach=.6, x=1.3, y=-1.7, b=-.7, l=1, mark='GOLDIEEE'), k(.85, x=-.3, y=.3, eye='-')],
        [], g='show', far=True, act=('shout', 'goldfish'), prefer=['lonely', 'grumpy'], say=["Goldie. Goldie. It is not called Goldie. I do not know its name.", "Called it. Nothing. It is on a break."])
    o.r('sing_the_goldfish_a_lullaby_in_threes', 'Singing the goldfish a lullaby in threes, since that is all it will remember, one verse at a time', 24, 'none',
        [k(.12, x=.2, y=.3, b=.3), k(.3, 'shallow_r', x=.8, y=.7, b=.5, mark='la'), k(.5, 'shallow_r', x=.9, y=.8, b=.6, l=1, w=.3, mark='la la'), k(.7, 'shallow_r', x=.8, y=.7, b=.5, r=1, w=.4, mark='la la la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'goldfish'), pick='shyest', prefer=['sad', 'lonely'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Three verses. It remembers none. The song is a gift.", "Soft song. Soft fish. Mine, for three seconds."])
    # ---------------- mishap
    o.r('skid_on_a_spilled_flake_at_the_rim', 'Skidding on a spilled flake at the rim and ending flat against the front stone', 16, 'none',
        [k(.15, 'stone_m', x=.6, y=.5, b=.7, r=1), k(.3, x=1, y=-.7, b=-1.1, w=.7, l=1, eye='O', mark='WHOA'), k(.5, 'stone_l', x=1.6, y=2.1, b=1.9, w=.5, r=1, eye='@', mark='splat'), k(.8, x=.3, y=.8, b=.8, eye='-')],
        [], g='mishap', act=('slip', 'rim'), prefer=['young'])
    o.r('back_into_the_reeds_at_dusk', 'Backing into the reed stem at dusk while counting flakes and bouncing off', 14, 'none',
        [k(.15, x=-.5, y=.5, b=.5, l=1), k(.3, 'reed_low', x=-1.3, y=.4, b=1, eye='O', mark='whap'), k(.5, x=.9, y=-.6, b=-.9, w=.9, r=1, eye='@'), k(.8, x=.2, y=.4, b=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'reeds'), when=['dusk'])
    o.r('tip_the_whole_pile_in_at_once', 'Tipping the whole pile of flakes in at once and watching the water cloud up as the goldfish goes mad', 20, 'wing',
        [k(.12, 'shallow_m', reach=.6, x=.3, y=.4, b=.4), k(.3, 'shallow_m', reach=1, x=.4, y=.7, b=.8, w=1, mark='FOOMF'), k(.5, x=-.7, y=-.4, b=-.6, w=.8, eye='O', mark='oops'), k(.7, 'shallow_r', reach=.5, x=.3, y=.8, b=.6, l=1, eye='>'), k(.88, eye='-')],
        [(.3, 'cloud')], g='mishap', act=('tip', 'pile'), prefer=['young', 'grumpy'], say=["Too many. Pond now looks like soup. Fish: delighted.", "I meant to pour less. I meant a lot of things."])
    o.r('hop_up_when_it_nips_a_toe', 'Hopping up with a yelp when the goldfish nips one toe, then glaring at the water', 16, 'none',
        [k(.15, 'shallow_l', x=.3, y=.8, b=.6, l=1), k(.32, 'shallow_l', x=-.3, y=-.6, b=-1.2, w=.9, l=1, eye='O', mark='YIP'), k(.5, x=-.5, y=-.8, b=-1.4, w=1, l=1, r=1, eye='@'), k(.72, x=.5, y=.9, b=.9, l=1, eye='>', mark='huh')],
        [], g='mishap', act=('hop', 'toes'), pick='hungriest', prefer=['young', 'curious'], obj=[(.25, dict(lure=1)), (.4, dict(lure=1))], say=["It bit my toe. It is the size of a thumb.", "Nipped. By a flake-sized monster."])
    o.r('foot_stuck_in_the_tuft', 'Catching a foot in the grass tuft while backing off the rim and hopping round in a circle trying to free it', 22, 'none',
        [k(.15, 'tuft', x=-.4, y=.4, b=.4), k(.32, 'tuft', x=-.6, y=.7, b=.8, l=1, eye='O', mark='huh'), k(.5, 'tuft', x=-.9, y=1, b=1.3, l=1, r=1, w=.6, eye='@', mark='mrf'), k(.7, 'tuft', x=-.4, y=.4, b=-.6, w=1, mark='PTHWOP'), k(.88, y=.6, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'foot'), prefer=['grumpy', 'young'])
    # ---------------- duets (a friend takes their own part)
    o.r('pass_a_flake_between_two_bills', 'Passing a flake from his bill to a friend\'s bill over the water, a little too slowly for the goldfish', 22, 'none',
        [k(.12, 'shallow_r', x=.7, y=.8, b=.6), k(.3, 'shallow_r', x=1.4, y=1.2, b=.9, mark='...'), k(.5, 'shallow_r', x=1.5, y=1.3, b=1, l=1, eye='O', mark='hup'), k(.7, 'shallow_r', x=.8, y=.9, b=.6, eye='^'), k(.88, eye='-')],
        [], g='use', act=('carry', 'flake'), pick='hungriest', prefer=['happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.15, x=.4, y=.5, b=.4), k(.34, 'shallow_m', x=1.4, y=1.3, b=.9, eye='o'), k(.55, 'shallow_m', x=1.5, y=1.4, b=1, r=1, mark='nom'), k(.75, 'shallow_m', x=.9, y=.9, b=.6, eye='^')])
    o.r('ring_dance_round_the_pond_with_a_friend', 'Dancing a ring round the pond edge with a friend, hop and swap, the goldfish circling to match', 26, 'none',
        [k(.1, 'stone_l', x=.3, y=.4, b=-.6, l=1), k(.28, 'shallow_l', x=.4, y=.4, b=-.9, r=1, w=.5), k(.46, 'shallow_m', x=.3, y=.4, b=-.6, l=1, w=.6, mark='la'), k(.64, 'stone_r', x=.4, y=.4, b=-.9, r=1, w=.5), k(.84, 'stone_r', x=.3, y=.3, b=-.5, eye='^')],
        [], g='play', act=('dance', 'rim'), pick='hungriest', prefer=['happy', 'young'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.54, dict(lure=1)), (.72, dict(lure=1))],
        duo=[k(.1, 'stone_r', x=.3, y=.4, b=-.6, r=1), k(.28, 'shallow_r', x=.4, y=.4, b=-.9, l=1, w=.5), k(.46, 'shallow_m', x=.3, y=.4, b=-.6, r=1, w=.6), k(.64, 'stone_l', x=.4, y=.4, b=-.9, l=1, w=.5), k(.84, 'stone_l', x=.3, y=.3, b=-.5, eye='^')])
    o.r('search_the_pads_together_for_the_goldfish', 'Searching the pads together for a goldfish that has gone missing, a wing on every stem', 24, 'wing',
        [k(.12, 'shallow_r', reach=.5, x=.3, y=.4, b=.4), k(.3, 'pad_r', reach=1, x=.6, y=.2, b=.5, eye='o'), k(.5, 'pad_r', reach=1, x=.7, y=.1, b=.7, l=1, eye='O', mark='huh'), k(.7, 'shallow_r', reach=1, x=.5, y=.4, b=.5, r=1, eye='>'), k(.88, eye='^', mark='there')],
        [], g='test', act=('seek', 'goldfish'), prefer=['curious'], pick='shyest', obj=[(.55, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.15, 'shallow_m', reach=.5, x=.3, y=.4, b=.4), k(.34, 'pad_r', reach=1, x=.6, y=.2, b=.5, r=1), k(.54, 'pad_r', reach=1, x=.5, y=.3, b=.6, eye='o'), k(.74, 'shallow_r', reach=1, x=.5, y=.4, b=.5, l=1), k(.9, eye='^')],
        say=["Found it. It was right there. It was always right there.", "Two ducks, one fish, one hide and seek that it did not agree to."])
    # @@END goldfish
    return done(o)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['scarf_red', 'scarf_winter', 'ancient_amulet', 'lucky_charm', 'koi', 'goldfish']:
        globals()[n]().emit(need=COUNT_NEED.get(n))
