"""Batch newB: basic_nest, cozy_nest, deluxe_nest, bed_king, bed_small, rocking_horse, skateboard, toy_skateboard, toy_swing.
Every routine is hand-written. Anchors are (column, row) of the drawing (rep.py <id> prints it) turned into fractions by pm().
Usage: rep_newB.py [object ...]   (LENIENT=1 lists every refusal instead of stopping at the first)"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN
if os.environ.get('LENIENT'):
    _r = Obj.r
    def _lenient(self, *a, **kw):
        try:
            _r(self, *a, **kw)
        except AssertionError as e:
            print('REFUSED', e)
    Obj.r = _lenient
    _e = Obj.emit
    def _emit(self, *a, **kw):
        try:
            _e(self, *a, **kw)
        except AssertionError as e:
            print('EMIT REFUSED', e)
    Obj.emit = _emit

DIM = dict(basic_nest=(82, 46), cozy_nest=(92, 52), deluxe_nest=(100, 60), bed_king=(100, 48), bed_small=(78, 39),
           rocking_horse=(84, 61), skateboard=(64, 28), toy_skateboard=(70, 29), toy_swing=(102, 74))


def pm(oid):
    w, rows = DIM[oid]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))


def basic_nest():
    P = pm('basic_nest')
    o = Obj('basic_nest', 'placed',
            parts=dict(rim='the woven rim band across the top of the bowl', grass='the grass blades (\\|/) lining the hollow',
                       twig_end='the outer twig ends poking out left and right', weave='the criss-cross twig wall of the bowl',
                       feather='the pale feather lying on the left rim', leaf='the green leaf (.---.) on the right rim',
                       pebble='the round pebble (.:) lying in the hollow', twig='the loose twig lying across the hollow',
                       crumb='the crumbs scattered on the hollow floor', hollow='the dished floor of the hollow'),
            fields=dict(plush=(.5, 0, 1), crumbs=(0, 0, 1), frost=(0, 0, 1), drift=(0, 0, 1), strewn=(0, 0, 1), warmth=(0, 0, 1)),
            physics=[('plush', 'rate', -.0003, 'always'), ('crumbs', 'rate', .0005, 'always'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'), ('warmth', 'rate', .0006, 'sun'), ('warmth', 'rate', -.0004, 'night')],
            effects=dict(scoop=[('crumbs', 'mul', .15)], rake=[('plush', 'add', .3)], dry=[('obj.wetness', 'add', -.3)], mend=[('obj.condition', 'add', .25)],
                         wipe=[('obj.dirt', 'add', -.25)], groom=[('plush', 'add', .25), ('strewn', 'mul', .4)],
                         press=[('plush', 'add', .2)], tug=[('strewn', 'add', .3)], pull=[('strewn', 'add', .35), ('crumbs', 'mul', .6)],
                         tidy=[('strewn', 'mul', .2)], chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], shake=[('drift', 'mul', .25)],
                         plough=[('drift', 'set', 0)], soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)], warm=[('warmth', 'add', -.2), ('need.fun', 'add', 1)],
                         scuff=[('obj.dirt', 'add', .12)], nick=[('obj.condition', 'add', -.15)], flatten=[('plush', 'add', -.25)],
                         spill=[('crumbs', 'add', .3)], laugh=[('need.fun', 'add', 2)], stuff=[('plush', 'add', .15), ('obj.condition', 'add', .1)]),
            marks=[('frost', .3, '*.*.*', 'weave_l', 'frost'), ('drift', .3, '.:*:.', 'rim_c', 'snow'), ('crumbs', .3, 'o . o', 'crumb', 'dust'),
                   ('strewn', .3, '/ // /', 'twig_end_l', 'plant')],
            anchors=dict(rim_l=P(28, 27), rim_c=P(44, 26, 'surface'), rim_r=P(55, 27, 'surface'), feather=P(22, 27), leaf=P(63, 27), twig_end_l=P(13, 32), twig_end_r=P(73, 32),
                         weave_l=P(30, 36), weave_c=P(46, 39), weave_r=P(60, 36), grass_a=P(25, 30), grass_b=P(37, 30), grass_c=P(41, 31),
                         pebble=P(50, 32), twig=P(46, 31), crumb=P(38, 33), hollow=P(44, 34, 'inside surface')))
    # ---------------- care
    o.r('scoop_crumbs', 'Scooping the crumbs off the hollow floor with a wing and flicking them over the rim', 20, 'wing',
        [k(.12, 'crumb', reach=.6, x=.4, y=1, b=.4), k(.3, 'crumb', reach=1, x=.6, y=1.3, b=.8, l=1, mark='shff'), k(.5, 'rim_c', reach=1, x=.9, y=.5, b=.2, w=.3, mark='fwip'), k(.7, 'crumb', reach=.8, x=.5, y=1.2, b=.7, r=1), k(.9, eye='^')],
        [(.5, 'scoop')], g='care', act=('scoop', 'crumb'), when=['crumbs>.3'], say=["Crumbs out. Whoever left them can explain themselves.", "Hollow swept. I have standards and a wing."])
    o.r('rake_grass', 'Taking a rake to the flattened grass blades with one foot and then the other', 20, 'none',
        [k(.12, 'grass_a', x=.3, y=1, b=.3), k(.3, 'grass_a', x=.5, y=1.3, b=.8, l=1, mark='shff'), k(.5, 'grass_b', x=.6, y=1.4, b=.9, r=1, mark='shff'), k(.7, 'grass_c', x=.4, y=1.2, b=.7, l=1), k(.9, eye='^')],
        [(.5, 'rake')], g='care', act=('rake', 'grass'), when=['plush<.7'], say=["Grass up. Bed fluffed. Thanks not yet received.", "Raked it with my toes. Toes unionising."])
    o.r('dry_weave', 'Drying the twig wall with a wing, left side to the right', 22, 'wing',
        [k(.1, 'weave_l', reach=.5, x=.4, y=.8, b=.2), k(.28, 'weave_l', reach=1, x=.8, y=1, b=.6, l=1), k(.5, 'weave_c', reach=1, x=.9, y=1.1, b=.7, r=1, mark='fff'), k(.72, 'weave_r', reach=1, x=.8, y=1, b=.6, l=1), k(.9, eye='-')],
        [(.5, 'dry')], g='care', act=('dry', 'weave'), when=['obj_wetness>.3'], say=["Wall dried. Wing damp. Net result: still damp.", "Twigs dry. Mood unchanged."])
    o.r('mend_twig_end', 'Mending a springy twig end by poking it back into the weave with his bill', 18, 'none',
        [k(.12, 'twig_end_l', x=.6, y=.8, b=.2), k(.3, 'twig_end_l', x=1.2, y=1.2, b=.7, mark='tk'), k(.48, 'weave_l', x=1.1, y=1.3, b=.8, l=1, mark='tk'), k(.68, 'twig_end_l', x=1, y=1, b=.5, mark='tak'), k(.88, eye='^')],
        [(.48, 'mend')], g='care', act=('mend', 'twig_end'), when=['obj_condition<.6'], say=["Twig back in. Looks structural, which is the main thing.", "Poked it home. It will hold until it doesn't."])
    o.r('wipe_rim', 'Giving the whole woven rim a wipe with the flat of a wing, end to end', 20, 'wing',
        [k(.1, 'rim_l', reach=.5, x=.3, y=.6, b=.2), k(.3, 'rim_l', reach=1, x=.6, y=.9, b=.5, l=1, mark='skrk'), k(.5, 'rim_c', reach=1, x=.7, y=1, b=.6, r=1, mark='skrk'), k(.7, 'rim_r', reach=1, x=.6, y=.9, b=.5, l=1), k(.9, eye='-')],
        [(.5, 'wipe')], g='care', act=('wipe', 'rim'), when=['obj_dirt>.3'])
    o.r('groom_feather', 'Grooming the stray feather flat with his bill and brushing the loose bits back into the weave', 20, 'none',
        [k(.12, 'feather', x=.5, y=.5, b=-.2), k(.3, 'feather', x=1.1, y=.8, b=.3, mark='prrt'), k(.5, 'rim_l', x=.8, y=1, b=.5, l=1), k(.7, 'feather', x=1.2, y=.7, b=.2, mark='prrt'), k(.9, eye='^')],
        [(.5, 'groom')], g='care', act=('groom', 'feather'), when=['strewn>.3'], prefer=['curious'])
    # ---------------- use
    o.r('press_hollow', 'Pressing the hollow deeper with his breast, three firm shoves', 22, 'none',
        [k(.12, 'hollow', x=.3, y=.8, b=.4), k(.3, 'hollow', x=.6, y=1.5, b=1.2, mark='hnf'), k(.46, 'hollow', x=.2, y=.9, b=.4), k(.62, 'hollow', x=.6, y=1.6, b=1.3, l=1, mark='HNF'), k(.8, 'hollow', x=.3, y=1, b=.7), k(.92, eye='-')],
        [(.62, 'press')], g='use', act=('press', 'hollow'), when=['plush<.6'], say=["Hollow deeper. Fit improved. Pride unconcealed.", "Breast first. The only way I do anything."])
    o.r('tug_leaf', 'Tugging the green leaf free of the rim until a few loose bits rain down', 18, 'none',
        [k(.12, 'leaf', x=.5, y=.3, b=.2), k(.3, 'leaf', x=1.2, y=.5, b=.5, mark='nng'), k(.5, 'leaf', x=-.4, y=.2, b=-.2, w=.4, mark='tug'), k(.68, 'leaf', x=1.3, y=.6, b=.6, l=1, mark='NNG'), k(.88, eye='>')],
        [(.5, 'tug')], g='use', act=('tug', 'leaf'), when=['strewn<.7'], obj=[(.3, dict(sway=.1)), (.5, dict(shake=.12)), (.7, dict(sway=0))])
    o.r('pull_twig', 'Pulling the loose twig out from across the hollow and dragging it to the rim', 20, 'none',
        [k(.12, 'twig', x=.4, y=1, b=.4), k(.3, 'twig', x=1, y=1.3, b=.7, mark='hup'), k(.5, 'twig', x=-.6, y=.5, b=-.3, l=1, w=.3), k(.7, 'rim_c', x=.8, y=.7, b=.3, mark='clk'), k(.9, eye='^')],
        [(.5, 'pull')], g='use', act=('pull', 'twig'), when=['strewn<.7'])
    o.r('drag_feather_in', 'Dragging the pale feather by its quill from the left rim down into the grass', 20, 'none',
        [k(.12, 'feather', x=.4, y=.4, b=.1), k(.3, 'feather', x=1.1, y=.7, b=.4, mark='mph'), k(.5, 'grass_a', x=1.2, y=1.1, b=.8, l=1), k(.7, 'grass_b', x=.9, y=1.2, b=.9, mark='pat'), k(.9, eye='^')],
        [(.7, 'stuff')], g='use', act=('drag', 'feather'), when=['plush<.8'], say=["Feather in the lining. Luxury, but cheap luxury.", "Quilled it into the grass. I am an interior designer now."])
    o.r('stack_twig_ends', 'Stacking the stray twig bits against the right end of the weave', 20, 'none',
        [k(.12, 'twig_end_r', x=.4, y=.9, b=.3), k(.3, 'twig_end_r', x=1, y=1.3, b=.8, mark='tk'), k(.5, 'weave_r', x=.9, y=1.2, b=.6, r=1, mark='tk'), k(.7, 'twig_end_r', x=.5, y=.9, b=.4), k(.9, eye='-')],
        [(.5, 'tidy')], g='use', act=('stack', 'twig_end'), when=['strewn>.3'])
    o.r('hook_pebble', 'Hooking the pebble with his bill and nudging it clear of the soft spot', 20, 'none',
        [k(.12, 'pebble', x=.5, y=1, b=.4), k(.3, 'pebble', x=1.2, y=1.4, b=.9, mark='tk'), k(.5, 'hollow', x=.6, y=1.2, b=.6, l=1, mark='tok'), k(.7, 'pebble', x=1.1, y=1.1, b=.7), k(.9, eye='^')],
        [(.5, 'press')], g='use', act=('hook', 'pebble'))
    # ---------------- play
    o.r('throw_pebble', 'Flicking the pebble up off the hollow floor and throwing it across to the rim', 20, 'none',
        [k(.12, 'pebble', x=.5, y=1.1, b=.5), k(.3, 'pebble', x=1.2, y=1.5, b=1, mark='hup'), k(.46, 'pebble', x=-.8, y=-.8, b=-.6, w=.7, mark='FWIP'), k(.62, 'rim_r', x=1, y=.2, b=.2), k(.82, eye='^')],
        [(.46, 'scuff')], g='play', act=('throw', 'pebble'), prefer=['curious'], say=["Pebble thrown. Pebble landed. Pebble has no feelings.", "Good arm. Bad aim. Fantastic confidence."])
    o.r('hide_in_grass', 'Ducking down into the grass blades to hide, bill first, tail still showing', 22, 'none',
        [k(.12, 'grass_b', x=.3, y=.6, b=.3), k(.3, 'grass_b', x=1.3, y=1.8, b=1, mark='shff'), k(.5, 'grass_b', x=1.5, y=2, b=1.2, eye='-'), k(.7, 'grass_c', x=1.4, y=1.9, b=1.1, l=1, mark='...'), k(.9, 'grass_c', x=.4, y=.5, b=.3, eye='O')],
        [], g='play', act=('hide', 'grass'), shown='head', prefer=['curious', 'young'], say=["You cannot see me. I am a very good grass.", "Hid. Won. The grass is a witness."])
    o.r('catch_feather', 'Tossing the pale feather up and catching it out of the air with his bill', 20, 'none',
        [k(.12, 'feather', x=.5, y=.3), k(.3, 'feather', x=1.2, y=-.4, b=-.6, w=.5, mark='fwoo'), k(.5, x=-.3, y=-1, b=-.8, w=.8, eye='O'), k(.66, x=1.2, y=.2, b=.4, l=1, mark='SNAP'), k(.86, 'feather', x=.4, y=.4, eye='^')],
        [(.86, 'laugh')], g='play', act=('catch', 'feather'), prefer=['happy', 'young'])
    o.r('kick_crumbs', 'Kicking the crumbs about the hollow floor in a spray, one foot then the other', 18, 'none',
        [k(.12, 'crumb', x=.2, y=.9, b=.4, l=1), k(.3, 'crumb', x=.4, y=1.2, b=.8, l=1, mark='fsh'), k(.5, 'hollow', x=.3, y=1.3, b=.9, r=1, mark='FSH'), k(.7, 'crumb', x=.3, y=1, b=.6, l=1), k(.88, eye='>')],
        [(.5, 'spill')], g='play', act=('kick', 'crumb'), when=['crumbs<.6'], say=["Crumbs everywhere. This is the fun bit.", "Made a mess on purpose. Sue me."])
    o.r('balance_twig', 'Balancing the loose twig upright on his bill and walking three steps without dropping it', 22, 'none',
        [k(.12, 'twig', x=.5, y=1, b=.4), k(.3, 'twig', x=-.2, y=-.9, b=-.4, w=.5, mark='hup'), k(.5, x=.1, y=-.8, b=-.3, l=1, w=.4, eye='O'), k(.68, x=.2, y=-.8, b=-.3, r=1, w=.4), k(.86, 'rim_c', x=.8, y=.2, b=.1, eye='^', mark='ha')],
        [(.86, 'tidy')], g='play', act=('balance', 'twig'), prefer=['grown'], say=["Three steps. Zero drops. Applaud in bread.", "Twig stayed up. So did my opinion of me."])
    o.r('dance_in_hollow', 'Dancing in the hollow, knees up, until the lining is flat and he is out of breath', 24, 'none',
        [k(.1, 'hollow', perch=1, x=.2, y=-.3, b=-.3, w=.5), k(.28, 'hollow', perch=1, x=.4, y=.2, b=.5, l=1, w=1), k(.46, 'hollow', perch=1, x=.2, y=-.4, b=-.5, r=1, w=.8), k(.64, 'hollow', perch=1, x=.5, y=.3, b=.7, l=1, w=1, mark='hup'), k(.84, 'hollow', perch=1, x=.2, y=.5, b=.4, eye='@')],
        [(.64, 'flatten'), (.84, 'laugh')], g='play', act=('dance', 'hollow'), prefer=['happy'], say=["Danced the bed flat. Worth every blade of grass.", "Left it flatter than I found it. Standard."])
    # ---------------- test
    o.r('tap_weave', 'Tapping along the twig wall with his bill, high to low, for a hollow knock', 20, 'none',
        [k(.12, 'weave_l', x=.7, y=.8, b=.3), k(.3, 'weave_l', x=1.2, y=1.1, b=.6, mark='tok'), k(.48, 'weave_c', x=1.2, y=1.4, b=.8, mark='tok'), k(.66, 'weave_r', x=1.1, y=1.6, b=.9, mark='tonk'), k(.86, eye='-')],
        [], g='test', act=('tap', 'weave'), prefer=['curious'])
    o.r('weigh_pebble', 'Lifting the pebble in his bill to weigh it, then setting it down in the same dent', 20, 'none',
        [k(.12, 'pebble', x=.5, y=1, b=.4), k(.3, 'pebble', x=-.4, y=-.5, b=-.3, w=.4, mark='hmf'), k(.5, x=-.3, y=-.3, b=-.2, w=.3, eye='-', mark='hm'), k(.7, 'pebble', x=1, y=1.2, b=.6, mark='tk'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'pebble'), say=["Heavy for a pebble. Suspicious pebble.", "Weighed it. Verdict: stone."])
    o.r('taste_leaf', 'Nibbling a corner of the green leaf to taste it and regretting it at once', 18, 'none',
        [k(.12, 'leaf', x=.5, y=.4, b=.2), k(.3, 'leaf', x=1.2, y=.6, b=.4, mark='nm'), k(.5, 'leaf', x=1, y=.5, b=.3, eye='-', mark='chew'), k(.7, x=-.4, y=.2, eye='>', mark='bleh'), k(.88, y=.1, eye='-')],
        [], g='test', act=('taste', 'leaf'), say=["Leaf. Tastes like a leaf that hates me.", "Chewed. Judged. Spat."])
    o.r('measure_hollow', 'Stretching a wing across the hollow to measure it against his own width', 22, 'wing',
        [k(.12, 'rim_l', reach=.6, x=.2, y=.5, b=.2), k(.3, 'rim_l', reach=1, x=.5, y=.8, b=.4), k(.5, 'hollow', reach=1, x=.7, y=1.2, b=.6, l=1, mark='hm'), k(.7, 'rim_r', reach=1, x=.5, y=.8, b=.4, r=1), k(.88, eye='^')],
        [], g='test', act=('measure', 'hollow'), prefer=['young'], say=["Fits me with room for bread. Verdict: adequate.", "Hollow is exactly duck-sized. Convenient liar."])
    o.r('listen_to_twig_end', 'Pressing an ear against the right twig end to listen for anything living in the weave', 22, 'none',
        [k(.12, 'twig_end_r', x=.5, y=.7, b=.2), k(.3, 'twig_end_r', x=1, y=1.2, b=.7, eye='-'), k(.5, 'twig_end_r', x=1.1, y=1.3, b=.8, eye='-', mark='...'), k(.7, 'weave_r', x=.9, y=1, b=.5, eye='O'), k(.88, x=0, y=0, eye='>')],
        [], g='test', act=('listen', 'twig_end'), prefer=['curious'])
    o.r('sniff_grass', 'Sniffing the grass lining blade by blade, left to right, for anything off', 20, 'none',
        [k(.12, 'grass_a', x=.6, y=1, b=.4), k(.3, 'grass_a', x=1.2, y=1.4, b=.8, mark='snf'), k(.5, 'grass_b', x=1.2, y=1.5, b=.9, mark='snf'), k(.7, 'grass_c', x=1.2, y=1.4, b=.8, mark='snf snf'), k(.88, eye='^')],
        [], g='test', act=('sniff', 'grass'), prefer=['grumpy'])
    # ---------------- rest
    o.r('lean_on_weave', 'Leaning his shoulder on the sun-warmed twig wall with his eyes shut', 24, 'none',
        [k(.12, 'weave_l', x=.2, y=.3, b=.2), k(.3, 'weave_l', x=-.3, y=.5, b=.6, eye='-'), k(.55, 'weave_l', x=-.4, y=.6, b=.8, eye='-', mark='ahh'), k(.8, 'weave_l', x=-.3, y=.4, b=.5, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'weave'), when=['warmth>.3', 'sun'], say=["Warm twigs. Warm shoulder. Closed my eyes at the world.", "Sun in the weave. I live here now."])
    o.r('warm_feet_on_twig_end', 'Warming one cold foot at a time against the sun-baked twig ends', 22, 'none',
        [k(.12, 'twig_end_r', x=.2, y=.5, b=.2, l=1), k(.35, 'twig_end_r', x=.3, y=.7, b=.4, l=1, eye='-', mark='ahh'), k(.6, 'twig_end_r', x=.3, y=.7, b=.4, r=1, eye='^'), k(.85, 'twig_end_r', x=.1, y=.4, eye='-')],
        [(.6, 'warm')], g='rest', act=('warm', 'twig_end'), when=['warmth>.3', 'sun'])
    o.r('guard_rim', 'Standing guard at the left rim, chest out, glaring at the yard', 24, 'none',
        [k(.12, 'rim_l', x=.3, y=-.2), k(.35, 'rim_l', x=.7, y=-.5, b=-.3, w=.4, eye='>'), k(.6, 'rim_l', x=-.2, y=-.4, b=-.5, l=1, mark='halt'), k(.85, 'rim_l', x=.3, y=-.2, w=.5, eye='-')],
        [], g='rest', act=('guard', 'rim'), prefer=['lonely', 'grumpy'], say=["Nothing came. Guarding works.", "Eyes on the yard. Mind on lunch."])
    o.r('perch_on_rim', 'Perching on the rim at the top with his feet tucked in, watching the yard like a tiny landlord', 26, 'none',
        [k(.12, 'rim_c', perch=1, x=.4, y=-.6, b=-.5, l=1, w=.3), k(.35, 'rim_c', perch=1, x=1, y=-.8, b=.3, r=1, eye='O'), k(.6, 'rim_c', perch=1, x=-.6, y=-.2, b=.5, w=.6, mark='hm'), k(.85, 'rim_c', perch=1, x=.3, y=0, b=.1, eye='-')],
        [], g='rest', act=('perch', 'rim'), prefer=['curious'])
    o.r('sit_on_pebble_side', 'Sitting hunched on the hollow floor beside the pebble, minding his own thoughts', 26, 'none',
        [k(.12, 'hollow', perch=1, x=.4, y=.1, b=.2, l=1), k(.35, 'hollow', perch=1, x=-.3, y=.7, b=.9, eye='-'), k(.6, 'hollow', perch=1, x=-.4, y=.8, b=1.1, w=.4, eye='-', mark='...'), k(.85, 'hollow', perch=1, x=.1, y=.2, b=.4, eye='^')],
        [(.6, 'soak')], g='rest', act=('sit', 'hollow'), when=['warmth>.3', 'dusk'], prefer=['tired'])
    o.r('seek_a_dry_patch', 'Seeking out the driest bit of grass and shuffling his feet until it is his', 22, 'none',
        [k(.12, 'grass_c', x=.4, y=.8, b=.3), k(.3, 'hollow', x=.6, y=1, b=.5, l=1), k(.5, 'hollow', x=.5, y=1.1, b=.7, r=1, mark='shff'), k(.7, 'grass_c', x=.3, y=.8, b=.4, eye='-'), k(.88, eye='^')],
        [], g='rest', act=('seek', 'grass'), prefer=['tired'])
    # ---------------- weather
    o.r('chip_frost_twig_end', 'Chipping the frost off the left twig ends with the edge of his bill', 18, 'none',
        [k(.12, 'twig_end_l', x=.5, y=.7, b=.2), k(.3, 'twig_end_l', x=1.2, y=1, b=.5, mark='skrk'), k(.5, 'weave_l', x=1.3, y=1.1, b=.6, l=1, mark='skrk'), k(.7, 'twig_end_l', x=1.1, y=.8, r=1), k(.88, eye='^')],
        [(.5, 'chip')], g='weather', act=('chip', 'twig_end'), when=['frost>.3'], say=["Frost off the twigs. Fingers I do not have, frozen anyway.", "Chipped it clear. Winter lost a round."])
    o.r('blow_on_frosted_rim', 'Blowing warm breath along the frosted rim until it goes dark and wet', 18, 'none',
        [k(.12, 'rim_l', x=.5, y=.3), k(.3, 'rim_l', x=1, y=.4, b=-.2, mark='haah'), k(.5, 'rim_c', x=1.1, y=.5, b=-.3, w=.3, mark='haaah'), k(.7, 'rim_r', x=.8, y=.3, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'rim'), when=['frost>.3'])
    o.r('shake_snow_off_rim', 'Shaking the snowy rim with a shoulder bump until a clump slides off', 18, 'none',
        [k(.12, 'rim_c', x=.2, y=.2, b=.3), k(.3, 'rim_c', x=.8, y=.4, b=.7, mark='bmp'), k(.5, 'rim_c', x=.9, y=.5, b=.8, l=1, mark='BMP'), k(.7, 'rim_r', x=.3, y=.2, b=.3), k(.88, eye='^')],
        [(.5, 'shake')], g='weather', act=('shake', 'rim'), when=['drift>.3'], obj=[(.3, dict(shake=.12)), (.5, dict(shake=.14)), (.7, dict(shake=0))])
    o.r('kick_drift_off_rim', 'Kicking the right-hand snow drift off the rim in two big sweeps of his foot', 18, 'none',
        [k(.12, 'rim_r', x=.4, y=.5, b=.2, r=1), k(.3, 'rim_r', x=.7, y=1, b=.8, r=1, mark='fff'), k(.5, 'leaf', x=.9, y=1, b=.9, l=1, mark='FFF'), k(.72, 'leaf', x=.2, y=.2, b=-.3, w=.4), k(.88, eye='^')],
        [(.5, 'plough')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Snow kicked off. Foot colder than the snow.", "Rim bare again. Winter can ask nicely next time."])
    o.r('brace_weave_in_wind', 'Bracing his whole back against the windward weave so the gusts have to go round him', 24, 'none',
        [k(.12, 'weave_r', x=.3, y=.4, b=.3), k(.3, 'weave_r', x=-.5, y=.7, b=.9, l=1, eye='-'), k(.55, 'weave_r', x=-.6, y=.9, b=1, r=1, eye='>', mark='hnng'), k(.8, 'weave_r', x=-.3, y=.5, b=.5)],
        [], g='weather', act=('brace', 'weave'), when=['windy'], prefer=['grown'])
    o.r('cool_belly_on_weave', 'Pressing his belly to the shaded centre of the wall to cool off', 22, 'none',
        [k(.12, 'weave_c', x=.3, y=.5, b=.3), k(.3, 'weave_c', x=.7, y=1.1, b=1, eye='-', mark='aah'), k(.55, 'weave_c', x=.8, y=1.2, b=1.2, w=.4, eye='-'), k(.8, 'weave_c', x=.4, y=.6, b=.5, eye='^')],
        [(.55, 'warm')], g='weather', act=('cool', 'weave'), when=['warm'], prefer=['tired'])
    # ---------------- show
    o.r('present_feather', 'Presenting the pale feather to the empty bowl like a prize it has not earned', 22, 'none',
        [k(.12, 'feather', x=.5, y=.4, b=.2), k(.3, 'feather', x=-.3, y=-.7, b=-.4, w=.5), k(.5, 'hollow', x=.9, y=.5, b=.2, w=.6, mark='ta-da'), k(.72, 'hollow', x=.5, y=.2, b=.1, w=.3, eye='^'), k(.9, eye='-')],
        [], g='show', act=('present', 'feather'), prefer=['happy'], say=["Behold. A feather. Be impressed immediately.", "Presented it. Bowl was unmoved. Rude bowl."])
    o.r('pose_on_rim_right', 'Striking a pose on the right rim, one wing out, profile to the yard', 24, 'none',
        [k(.12, 'rim_r', perch=1, x=.2, y=-.3, b=-.2, w=.4), k(.35, 'rim_r', perch=1, x=.7, y=-.7, b=.1, w=1, eye='>'), k(.6, 'rim_r', perch=1, x=.5, y=-.6, b=.1, w=1, l=1, mark='hm'), k(.85, 'rim_r', perch=1, x=.2, y=-.2, w=.3, eye='^')],
        [], g='show', act=('pose', 'rim'), prefer=['happy', 'grown'])
    o.r('bow_to_leaf', 'Bowing low to the green leaf, twice, in case it is somebody important', 20, 'none',
        [k(.12, 'leaf', x=.3, y=.3, b=.1, l=1), k(.3, 'leaf', x=1.2, y=1.8, b=1.2, mark='bow'), k(.48, 'rim_c', x=-.3, y=-.8, b=-.8, w=.7), k(.66, 'rim_c', x=1.3, y=2, b=1.3, r=1, mark='BOW'), k(.86, eye='^')],
        [], g='show', act=('bow', 'leaf'), prefer=['happy'], say=["Leaf did not bow back. Leaf is rude.", "Bowed. Leaf declined to speak first."])
    o.r('show_off_hollow', 'Showing off the hollow end to end with a sweep of the wing, like a landlord', 22, 'wing',
        [k(.12, 'leaf', reach=.5, x=.2, y=.2), k(.3, 'leaf', reach=1, x=.5, y=-.2, w=.7, mark='ta-da'), k(.5, 'feather', reach=1, x=.6, y=.3, b=.1), k(.7, 'leaf', reach=1, x=.5, y=-.2, r=1, mark='ta-da'), k(.88, eye='^')],
        [], g='show', act=('show', 'hollow'), prefer=['happy'])
    o.r('shout_into_weave', 'Shouting the whole word list into the twig wall to see what comes back', 20, 'none',
        [k(.12, 'weave_c', x=.5, y=.5, b=.2), k(.3, 'weave_c', x=1.3, y=.8, b=.5, mark='HEY'), k(.5, 'weave_c', x=.2, y=.4, b=0, eye='-', mark='...'), k(.7, 'weave_c', x=1.4, y=.9, b=.6, mark='HEEEY'), k(.88, eye='>')],
        [], g='show', act=('shout', 'weave'), shown='head', prefer=['grumpy'], say=["Nothing came back. Even the nest ghosts me.", "Told the twigs everything. Twigs silent."])
    o.r('sing_to_grass', 'Singing a slow tune to the grass lining as if it were about to hatch something', 24, 'none',
        [k(.12, 'grass_b', x=.3, y=.7, b=.2), k(.3, 'grass_b', x=.5, y=.9, b=.4, mark='la'), k(.5, 'hollow', x=.4, y=.8, b=.3, w=.3, mark='laa'), k(.7, 'grass_b', x=.5, y=.9, b=.4, mark='laaa'), k(.88, eye='^')],
        [], g='show', act=('sing', 'grass'), prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('slip_on_grass', 'Slipping on the loose grass blades and landing flat on his belly in a heap', 20, 'none',
        [k(.12, 'grass_a', x=.5, y=.5, b=.2), k(.28, 'grass_a', x=.8, y=.2, b=-.5, l=1, r=1, w=.8, mark='whoa'), k(.46, 'hollow', x=1.2, y=2, b=1.3, eye='@', mark='FLUMP'), k(.7, 'hollow', x=.9, y=1.8, b=1.1, eye='-', mark='...'), k(.9, eye='>')],
        [(.46, 'scuff')], g='mishap', act=('slip', 'grass'), prefer=['grumpy'], say=["The grass did that. I saw it.", "Slipped. Meant to. Rehearsed it for weeks."])
    o.r('stuck_in_twig_end', 'Getting a foot stuck in the left twig ends and hopping about until it pops free', 24, 'none',
        [k(.12, 'twig_end_l', x=.3, y=1, b=.4, l=1), k(.3, 'twig_end_l', x=.7, y=1.3, b=.8, l=1, eye='O', mark='huh'), k(.5, 'twig_end_l', x=1, y=1.5, b=1, l=1, r=1, mark='mmf'), k(.7, 'twig_end_l', x=1.3, y=.4, b=-.5, l=1, w=1, mark='POP'), k(.9, x=.4, y=1, b=.5, eye='>')],
        [(.7, 'nick')], g='mishap', act=('stuck', 'twig_end'), prefer=['young'], obj=[(.5, dict(shake=.1)), (.7, dict(shake=.14)), (.85, dict(shake=0))])
    o.r('knock_pebble', 'Knocking the pebble out of its dent so it clacks along the weave', 18, 'none',
        [k(.12, 'pebble', x=.4, y=.9, b=.3), k(.3, 'pebble', x=1.4, y=1.2, b=.7, l=1, mark='tk'), k(.5, 'weave_c', x=.8, y=1.3, b=.5, eye='O', mark='clack'), k(.7, 'hollow', x=.4, y=1, b=.4, eye='>'), k(.88, eye='-')],
        [(.5, 'scuff')], g='mishap', act=('knock', 'pebble'))
    o.r('tilt_rim_leaning', 'Tilting the left rim down by leaning on it too hard and watching the lining slump', 20, 'none',
        [k(.12, 'rim_l', x=.3, y=.4, b=.3), k(.3, 'rim_l', x=.9, y=.9, b=.9, mark='creak'), k(.5, 'rim_l', x=1, y=1.1, b=1.2, l=1, eye='O', mark='CRK'), k(.7, 'rim_l', x=.4, y=.5, b=.4, w=.3), k(.88, eye='>')],
        [(.5, 'flatten')], g='mishap', act=('tilt', 'rim'), obj=[(.3, dict(sway=-.1)), (.5, dict(sway=-.15, shake=.1)), (.75, dict(sway=0))])
    o.r('dig_through_hollow', 'Digging at the floor of the hollow to make it deeper and going through the lining', 22, 'none',
        [k(.12, 'hollow', x=.3, y=1, b=.4), k(.3, 'hollow', x=.6, y=1.5, b=.9, l=1, mark='sck'), k(.48, 'hollow', x=.5, y=1.6, b=1, r=1, mark='sck'), k(.68, 'hollow', x=.6, y=1.8, b=1.2, l=1, eye='O', mark='RIP'), k(.88, x=.3, y=.9, eye='>')],
        [(.68, 'nick')], g='mishap', act=('dig', 'hollow'), prefer=['grumpy'], say=["Dug a bit more than planned. Plan was optional.", "Floor now has a view. Of the floor."])
    o.r('shove_weave_wall', 'Shoving the weave with his whole side to see if the wall gives', 20, 'none',
        [k(.12, 'weave_r', x=.3, y=.4, b=.3), k(.3, 'weave_r', x=.8, y=.7, b=.8, l=1, mark='hnf'), k(.5, 'weave_r', x=1, y=.8, b=1, r=1, mark='HNF'), k(.7, 'weave_r', x=.3, y=.4, b=.3, eye='O'), k(.88, eye='-')],
        [], g='mishap', act=('shove', 'weave'), obj=[(.3, dict(sway=.08)), (.5, dict(sway=.14, shake=.1)), (.7, dict(sway=0))])
    o.emit()
    return o
