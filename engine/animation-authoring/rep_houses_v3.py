"""Houses, version 3: barn, shed, greenhouse, mud_hut, stone_house, wooden_cottage. Every routine is hand-written.
Each house names its real parts first (from home-workshop.mjs: the blueprint props and the glyphs the drawing really shows);
anchors are (column, row) of the drawing (rep.py <id> prints it) turned into fractions by pm().
Usage: rep_houses_v3.py [object ...]   (LENIENT=1 lists every refusal instead of stopping at the first)"""
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

DIM = dict(barn=(108, 61), shed=(86, 52), greenhouse=(108, 57), mud_hut=(82, 47), stone_house=(96, 57), wooden_cottage=(98, 58))


def pm(oid):
    w, rows = DIM[oid]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))



def barn():
    P = pm('barn')
    o = Obj('barn', 'placed',
            parts=dict(board='the red plank walls left and right of the doors, a plank line every five columns',
                       nail='the nail heads (o) set along the plank rows', plate='the (=) plates set in the boards and in each door leaf',
                       jamb='the door frame posts either side of the doors', leaf='the two door leaves, upright planks, left and right',
                       brace='the diagonal brace down each leaf', seam='the line where the two leaves meet',
                       crate='the little .-|--. box shape at the foot of the right leaf',
                       window='the four-pane window glass in each side bay (cross mullion, glints)', sill='the ledge under each window',
                       lip='the door base line, 19 px up', step='the lower door-frame line, 9 px up', thresh='the standing line in front of the doors',
                       hay='the hay bundle stacked at the left foot', loft='the loft hatch high up the front, out of reach', vane='the weathervane on the ridge, out of reach'),
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), warmth=(0, 0, 1), strewn=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('warmth', 'rate', .0006, 'sun'), ('warmth', 'rate', -.0004, 'night')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], sweep=[('obj.dirt', 'add', -.15)], wipe=[('obj.dirt', 'add', -.2)], dry=[('obj.wetness', 'add', -.3)],
                         flick=[('obj.wetness', 'add', -.2)], spray=[('obj.wetness', 'add', .15)], hammer=[('obj.condition', 'add', .2)], dent=[('obj.condition', 'add', -.15)],
                         scuff=[('obj.dirt', 'add', .12)], tidy=[('strewn', 'mul', .5)], chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], grind=[('frost', 'mul', .6)],
                         kick=[('drift', 'set', 0)], plough=[('drift', 'mul', .3)], soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)],
                         warm=[('warmth', 'add', -.2), ('need.fun', 'add', 1)], tug=[('strewn', 'add', .35)], tumble=[('strewn', 'add', .3)],
                         burrow=[('strewn', 'add', .25)], rake=[('strewn', 'mul', .2)], laugh=[('need.fun', 'add', 2)]),
            marks=[('frost', .3, '*.*.*', 'lip_a', 'frost'), ('frost', .3, '*.*', 'window_l', 'frost'), ('drift', .3, '.:*:.', 'step_a', 'snow'), ('strewn', .3, '/ // /', 'hay_foot', 'plant')],
            anchors=dict(hay_top=P(12, 57, 'surface'), hay_foot=P(12, 59), board_l=P(22, 54), board_r=P(86, 54), nail_l=P(16, 52), nail_l2=P(30, 52), nail_r=P(81, 52),
                         plate_l=P(15, 56), plate_r=P(93, 56), jamb_l=P(33, 53), jamb_r=P(74, 53), leaf_l_foot=P(40, 54), leaf_r=P(63, 46),
                         brace_l=P(47, 48), brace_r=P(60, 48), seam=P(53, 50), crate=P(67, 54), plate_dl=P(41, 51), 
                         window_l=P(18, 45), window_r=P(84, 45), sill_r=P(84, 47),
                         lip_a=P(40, 56, 'surface'), lip_b=P(66, 56, 'surface'), step_a=P(45, 57, 'surface'), step_b=P(62, 57, 'surface'), thresh=P(54, 58, 'surface')))
    # ---------------- care
    o.r('scrub_boards', 'Scrubbing the left boards with a wing until the red comes back', 20, 'wing',
        [k(.1, 'board_l', reach=.6, x=.5, y=.7, b=.2), k(.26, 'board_l', reach=1, x=.8, y=1, b=.6, l=1), k(.42, 'nail_l', reach=1, x=.9, y=.7, b=.2, r=1, mark='skrk'), k(.6, 'board_l', reach=1, x=.9, y=1.1, b=.8, l=1, mark='skrk'), k(.78, 'plate_l', reach=.8, x=.6, y=.6, b=.3, r=1), k(.92, eye='^')],
        [(.6, 'scrub')], g='care', act=('scrub', 'board'), when=['obj_dirt>.3'], prefer=['grown'],
        say=["Barn was filthy. Now it is only my fault.", "Boards clean. Wing filthy. Fair trade."])
    o.r('sweep_lip', 'Sweeping the dust off the door lip, end to end, with the flat of a wing', 18, 'wing',
        [k(.12, 'lip_a', reach=.5, x=.3, y=.6), k(.3, 'lip_a', reach=1, x=.5, y=.9, b=.3, l=1), k(.55, 'lip_b', reach=1, x=.6, y=.8, r=1), k(.75, 'lip_b', reach=.6, x=.3, y=.4), k(.9, eye='-')],
        [(.55, 'sweep')], g='care', act=('sweep', 'lip'), when=['obj_dirt>.3'], say=["Lip swept. Dust relocated to the yard.", "Door lip has never been this smug."])
    o.r('dry_jambs', 'Drying both door posts with his breast and a lot of grunting', 20, 'none',
        [k(.12, 'jamb_l', x=.6, y=.2), k(.3, 'jamb_l', x=1.3, y=.9, b=.8, l=1, mark='hff'), k(.5, 'jamb_l', x=1.4, y=.1, b=-.4, w=.4), k(.72, 'jamb_r', x=1.2, y=.8, b=.7, r=1, mark='hff'), k(.88, x=.2, w=.3, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'jamb'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.1)), (.72, dict(shake=.1))])
    o.r('hammer_nail', 'Mending a raised nail head: hammering it flat with his bill, three taps and a verdict', 18, 'none',
        [k(.1, x=.7, y=.9, b=.3), k(.24, 'nail_l2', x=1.2, y=1.8, b=.9, l=1, mark='tak'), k(.4, x=.3, y=.6, b=-.3), k(.56, 'nail_l2', x=1.3, y=2, b=1, r=1, mark='tak'), k(.7, x=.2, y=.5, b=-.2, w=.4), k(.82, 'nail_l2', x=1.4, y=2.1, b=1.1, mark='TAK'), k(.94, eye='^')],
        [(.82, 'hammer')], g='care', act=('mend', 'nail'), when=['obj_condition<.6'], say=["Nail flat. Barn holds. Send thanks in bread.", "Hammered it with my face. Worked."])
    o.r('wipe_window', 'Reaching a wing up to wipe a clear streak across the left window glass', 20, 'wing',
        [k(.1, 'window_l', reach=.4, x=.2, y=-.1, b=-.1), k(.28, 'window_l', reach=1, x=.6, y=-.7, b=-.5, l=1, mark='squk'), k(.46, 'window_l', reach=1, x=1.1, y=-.9, b=-.6, r=1, mark='squk'), k(.64, 'window_l', reach=.8, x=.2, y=-.5, b=-.3, l=1), k(.8, reach=.2, y=-.2, w=.5, eye='O'), k(.92, eye='^')],
        [(.46, 'wipe')], g='care', act=('wipe', 'window'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('rake_hay', 'Using both feet to rake the strewn hay back against the stack', 20, 'none',
        [k(.12, 'hay_foot', x=.3, y=.9, b=.4), k(.3, 'hay_foot', x=.6, y=1.3, b=.8, l=1, mark='shff'), k(.48, 'hay_foot', x=.5, y=1.4, b=.9, r=1, mark='shff'), k(.68, 'hay_foot', x=.3, y=1.1, b=.6, l=1), k(.88, y=.2, w=.5, eye='^')],
        [(.48, 'rake')], g='care', act=('rake', 'hay'), when=['strewn>.3'], say=["Hay back in the pile. Hay will be out again by noon.", "Raked it tidy. The pile looks suspicious."])
    o.r('fluff_hay_top', 'Fluffing the squashed top of the hay stack back up with his bill', 18, 'none',
        [k(.12, 'hay_top', x=.4, y=.4, b=.2), k(.3, 'hay_top', x=1, y=.9, b=.5, mark='fff'), k(.5, 'hay_top', x=.5, y=-.2, b=-.4, w=.5, mark='fwip'), k(.7, 'hay_top', x=1.1, y=.7, b=.4, l=1), k(.88, x=-.2, eye='^')],
        [(.5, 'tidy')], g='care', act=('fluff', 'hay'), when=['strewn>.3'])
    # ---------------- use
    o.r('shoulder_leaf', 'Pushing a shoulder against the left leaf to see whether the doors give', 18, 'none',
        [k(.12, 'leaf_l_foot', x=.2, y=.4), k(.3, 'leaf_l_foot', x=-.5, y=.8, b=.6, mark='hup'), k(.5, 'leaf_l_foot', x=-.7, y=.9, b=1, l=1, r=1, mark='hhn'), k(.72, 'leaf_l_foot', x=-.2, y=.4, b=.3), k(.88, x=.3, y=.6, eye='-')],
        [], g='use', act=('push', 'leaf'), obj=[(.5, dict(shake=.1))], say=["Left leaf. Zero give. Respect, I suppose.", "Shoulder hurts. Door unbothered."])
    o.r('knock_right_leaf', 'Knocking on the right leaf, then waiting to be told to come in', 18, 'none',
        [k(.12, 'leaf_r', x=.5, y=-.2), k(.28, 'leaf_r', x=1.1, y=-.3, b=.3, mark='tok'), k(.42, 'leaf_r', x=.2, y=-.1, b=-.2, w=.4), k(.58, 'leaf_r', x=1.2, y=-.3, b=.4, mark='tok tok'), k(.76, x=-.4, y=-.6, b=-.3, w=.7, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'leaf'), say=["Knocked twice. Barn has the manners of a barn.", "Waited politely. Door waited rudely."])
    o.r('pull_hay_strand', 'Pulling a long strand out of the hay stack and letting it trail', 18, 'none',
        [k(.12, 'hay_top', x=.4, y=.5), k(.3, 'hay_top', x=1, y=.9, b=.4, mark='mmf'), k(.5, 'hay_top', x=-.5, y=.4, b=-.3, w=.6, mark='fwip'), k(.7, 'hay_foot', x=.3, y=1.2, b=.5), k(.88, eye='^')],
        [(.5, 'tug')], g='use', act=('pull', 'hay'), say=["Hay came out. So did a bit of the pile. Fine.", "Strand acquired. Strand dropped. Hay is everywhere."])
    o.r('peer_at_seam', 'Pushing his bill up to the seam between the leaves to peer for movement', 20, 'none',
        [k(.12, 'seam', x=.5, y=-.4, b=-.3), k(.32, 'seam', x=1.2, y=-.9, b=-.6, w=.4, eye='O'), k(.55, 'seam', x=1.3, y=-1, b=-.7, l=1, mark='...'), k(.78, x=-.3, y=-.3, b=-.1, eye='-'), k(.9, eye='>')],
        [], g='use', act=('peer', 'seam'), prefer=['curious'])
    o.r('shout_up_loft', 'Cupping a wing and shouting up at the loft hatch for whoever left the hay', 18, 'none',
        [k(.15, x=-.2, y=-.9, b=-.2), k(.35, x=-.5, y=-1.4, b=-.5, w=.6, mark='HOY'), k(.58, x=-.7, y=-1.6, b=-.6, w=.8, l=1, mark='HOOOY'), k(.8, x=-.3, y=-.6, b=-.2, eye='-')],
        [(.58, 'laugh')], g='use', act=('shout', 'loft'), far=True, say=["Only the echo answers up there.", "Shouted at the hatch. Hatch shrugged."])
    # ---------------- play
    o.r('climb_hay_slide', 'Climbing the hay stack and sliding down its slope on his belly', 20, 'none',
        [k(.12, 'hay_foot', x=.3, y=.4, b=.3), k(.3, 'hay_top', perch=1, x=.2, y=-.4, b=-.4, w=.7, mark='hup'), k(.5, 'hay_top', perch=1, x=.8, y=.9, b=.8), k(.68, 'hay_foot', x=1.2, y=1.1, b=1.2, w=.6, mark='fwoosh'), k(.88, y=.3, eye='^')],
        [(.68, 'tumble')], g='play', act=('climb', 'hay'), prefer=['happy', 'young'], say=["Top of the hay. King of nothing. Down again.", "Slid all the way down. Would slide again."])
    o.r('race_the_lip', 'Running a race along the door lip from the left end to the right, wings out', 16, 'none',
        [k(.1, 'lip_a', perch=1, x=.3, y=.1, w=.6), k(.3, 'lip_a', perch=1, x=.6, y=.4, b=.6, l=1, w=1), k(.5, 'lip_b', perch=1, x=.8, y=.3, b=.2, r=1, w=1, mark='zoom'), k(.72, 'lip_b', perch=1, x=.4, y=.5, b=.5, w=.8), k(.9, eye='^')],
        [], g='play', act=('race', 'lip'), prefer=['happy'])
    o.r('hide_at_the_jamb', 'Trying to hide flat against the left post, then bursting out at nothing', 18, 'none',
        [k(.12, 'jamb_l', x=-.2, y=.2), k(.3, 'jamb_l', x=-.9, y=.8, b=.7, eye='O'), k(.52, 'jamb_l', x=-1, y=.9, b=.9, mark='shh'), k(.7, x=1.2, y=-.4, b=-.5, w=1, l=1, r=1, mark='BAH'), k(.88, eye='^')],
        [], g='play', act=('hide', 'jamb'), prefer=['young'])
    o.r('drum_right_boards', 'Drumming a march along the right boards and nails with his bill', 18, 'none',
        [k(.12, 'board_r', x=1, y=.6, b=.3, mark='tok'), k(.3, 'nail_r', x=.8, y=.2, b=-.2, l=1, mark='tok'), k(.5, 'board_r', x=1.1, y=.7, b=.4, r=1, mark='tok tok'), k(.7, 'nail_r', x=.8, y=.2, b=-.2, l=1, mark='TOK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'board'), prefer=['happy'], say=["Barn has a good beat. Poor tempo discipline.", "Planks on the downbeat. Nails on the off."])
    o.r('balance_the_step', 'Balancing along the lower door line with his wings out like a plank walker', 18, 'none',
        [k(.12, 'step_a', perch=1, y=-.2, w=.5), k(.32, 'step_a', perch=1, x=.3, b=.3, l=1, w=1), k(.55, 'step_b', perch=1, x=.5, b=.5, r=1, w=1, mark='whoa'), k(.78, 'step_b', perch=1, y=.2, b=.2, w=.7), k(.92, eye='^')],
        [], g='play', act=('balance', 'step'))
    o.r('seek_round_the_post', 'Creeping out to seek round the right post with one eye', 18, 'none',
        [k(.12, 'lip_a', x=.2, y=.3, b=.2), k(.35, 'lip_b', x=.2, y=.4, b=.4, l=1), k(.6, 'jamb_r', x=.9, y=-.3, b=.3, eye='O'), k(.8, 'jamb_r', x=1.1, y=-.4, b=.4, eye='>', mark='psst'), k(.92, eye='-')],
        [], g='play', act=('seek', 'jamb'), prefer=['curious'])
    o.r('dig_hay_hollow', 'Digging a hollow at the foot of the hay stack, hay flying everywhere', 20, 'none',
        [k(.12, 'thresh', x=.4, y=1, b=.4), k(.3, 'thresh', x=.9, y=1.6, b=.9, l=1, mark='fff'), k(.5, 'hay_foot', x=1, y=1.8, b=1, r=1, mark='fff'), k(.7, 'thresh', x=.7, y=1.5, b=.8, l=1, r=1), k(.88, y=.4, w=.7, eye='^')],
        [(.5, 'burrow')], g='play', act=('dig', 'hay'), prefer=['happy'], say=["Hole in the hay. Mine. Staying out of the plans.", "Dug it. The barn will want it back."])
    # ---------------- test
    o.r('tap_for_hollow', 'Tapping the right boards from the bottom up to hear where they sound hollow', 18, 'none',
        [k(.1, 'board_r', x=1.4, y=.9, b=.6, mark='tok'), k(.28, 'plate_r', x=.9, y=-.5, b=-.5, l=1, mark='tok'), k(.46, 'board_r', x=.2, y=-.8, b=-.1, w=.8, eye='-'), k(.64, 'board_r', x=1.5, y=1.1, b=.8, r=1, mark='tonk'), k(.82, eye='^')],
        [], g='test', act=('tap', 'board'))
    o.r('count_nail_heads', 'Touching each nail head along the left wall and counting under his breath', 22, 'none',
        [k(.08, 'nail_l', x=1.1, y=1.7, b=.9, mark='1'), k(.28, 'nail_l2', x=1.3, y=1.5, b=.2, r=1, mark='2'), k(.48, 'plate_dl', x=.9, y=1.3, b=1.1, l=1, mark='3'), k(.68, 'plate_l', x=1.4, y=1.8, b=.5, r=1, mark='4'), k(.86, x=-.7, y=-.5, w=.7, eye='-', mark='four')],
        [], g='test', act=('count', 'nail'), prefer=['curious'])
    o.r('measure_up_the_post', 'Trying to measure himself against the right post to see how much of him reaches the top', 20, 'none',
        [k(.12, 'jamb_r', x=-.4, y=.3, b=.2), k(.3, 'jamb_r', x=-.5, y=-.8, b=-.5, w=.8, mark='...'), k(.55, 'jamb_r', x=1.2, y=1.2, b=.9, eye='O'), k(.75, 'jamb_r', x=-.3, y=.2, b=.3, l=1, eye='-', mark='short'), k(.9, eye='>')],
        [], g='test', act=('measure', 'jamb'), prefer=['young'], say=["Door is tall. I am a duck. No lies told.", "Reached the middle of the post. Statistically fine."])
    o.r('tap_the_braces', 'Tapping down the left brace from the top to the foot, then up the right', 22, 'none',
        [k(.12, 'brace_l', x=.8, y=.4), k(.3, 'brace_l', x=1.1, y=.8, b=.4, mark='hm'), k(.5, 'brace_r', x=1.1, y=.8, b=.4, l=1), k(.7, 'brace_r', x=.9, y=.5, b=.2, eye='-', mark='same'), k(.88, eye='>')],
        [], g='test', act=('tap', 'brace'), prefer=['curious'])
    o.r('taste_a_hay_strand', 'Nibbling a stalk off the hay stack and chewing it solemnly to taste it', 18, 'none',
        [k(.12, 'hay_top', x=.5, y=.4, b=.2), k(.3, 'hay_top', x=1.1, y=.6, b=.3, mark='nm'), k(.5, 'hay_foot', x=.1, y=1.1, b=.3, eye='-', mark='chew'), k(.68, x=.3, y=.5, b=.2, eye='O'), k(.86, x=-.2, y=.1, eye='-', mark='bleh')],
        [], g='test', act=('taste', 'hay'), say=["Hay. Tastes like hay. I was hoping for a trick.", "Chewed it. Regret is mostly fibre."])
    o.r('prod_the_sill', 'Prodding the right sill with a twig to see if the window is shut', 20, 'twig',
        [k(.15, 'sill_r', reach=.6, x=.3, y=-.2), k(.35, 'sill_r', reach=1, x=.5, y=-.4, w=.4, mark='tk'), k(.55, 'window_r', reach=1, x=.6, y=-.5, mark='tk tk'), k(.8, x=-.2, y=-.1, eye='-')],
        [], g='test', act=('prod', 'sill'))
    o.r('knock_the_crate', 'Knocking on the little box at the foot of the right leaf to hear if it is empty', 18, 'none',
        [k(.12, 'crate', x=.6, y=.9, b=.4), k(.3, 'crate', x=1.2, y=1.4, b=.8, mark='tonk'), k(.46, x=.1, y=.3, b=.2, eye='-', mark='...'), k(.62, 'crate', x=1.3, y=1.5, b=.9, l=1, mark='tonk'), k(.82, x=-.2, y=.2, eye='>')],
        [], g='test', act=('knock', 'crate'), prefer=['curious'])
    # ---------------- rest
    o.r('lean_warm_boards', 'Leaning a shoulder against the sun-warmed left boards and soaking it up', 24, 'none',
        [k(.12, 'board_l', x=.2, y=.3, b=.2), k(.3, 'board_l', x=-.3, y=.5, b=.5, eye='-'), k(.55, 'board_l', x=-.4, y=.6, b=.7, eye='-', mark='ahh'), k(.8, 'board_l', x=-.3, y=.4, b=.5, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'board'), when=['warmth>.3', 'sun'], say=["Warm boards. This is the correct use of a barn.", "Sun in the planks. Heat in my shoulder. Peace."])
    o.r('sit_on_the_step', 'Sitting on the lower door line with his feet tucked, watching the yard go nowhere', 24, 'none',
        [k(.12, 'step_a', perch=1, y=-.2, b=.2), k(.3, 'step_a', perch=1, y=.4, b=.9, eye='-'), k(.6, 'step_a', perch=1, y=.5, b=1, eye='-', mark='...'), k(.85, 'step_a', perch=1, y=.1, b=.4, eye='^')],
        [], g='rest', act=('sit', 'step'), say=["Yard did nothing. Fantastic yard.", "Sat. Looked. Left with my opinions intact."])
    o.r('nap_on_the_hay', 'Taking a nap on top of the hay stack with his bill tucked into a wing', 30, 'none',
        [k(.15, 'hay_top', perch=1, y=.2, b=.3), k(.35, 'hay_top', perch=1, y=.8, b=1, eye='-'), k(.6, 'hay_top', perch=1, y=1, b=1.2, eye='-', mark='zzz'), k(.85, 'hay_top', perch=1, y=.3, b=.5, eye='^')],
        [(.6, 'soak')], g='rest', act=('nap', 'hay'), prefer=['tired'], say=["Hay nap. Straw in my ear. Zero complaints.", "Slept on the pile. Pile slept on me."])
    o.r('warm_feet_on_lip', 'Warming one foot, then the other, against the sun-baked door lip', 22, 'none',
        [k(.12, 'lip_b', perch=1, x=.2, y=.4, l=1), k(.35, 'lip_b', perch=1, x=.3, y=.6, b=.3, l=1, eye='-', mark='ahh'), k(.6, 'lip_b', perch=1, x=.3, y=.6, b=.3, r=1, eye='^'), k(.85, 'lip_b', perch=1, x=.1, y=.3, eye='-')],
        [(.6, 'warm')], g='rest', act=('warm', 'lip'), when=['warmth>.3', 'sun'])
    o.r('lean_on_the_right_post', 'Leaning on the right post with his wings folded, unimpressed', 20, 'none',
        [k(.12, 'board_r', x=.3, y=.3), k(.35, 'jamb_r', x=-.2, y=.9, b=.5, eye='-'), k(.6, 'jamb_r', x=-.3, y=.9, b=.9, l=1, eye='-', mark='hm'), k(.82, 'jamb_r', x=-.2, y=.4, b=.4, eye='>')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    o.r('perch_on_the_hay', 'Perching on the hay stack to survey the yard like a very small farmer', 24, 'none',
        [k(.14, 'hay_top', perch=1, x=.2, y=-.3, b=-.2, w=.4), k(.35, 'hay_top', perch=1, x=.6, y=-.6, b=.2, eye='O'), k(.6, 'hay_top', perch=1, x=-.5, y=-.4, b=.3, w=.3, mark='hm'), k(.85, 'hay_top', perch=1, x=.2, y=-.2, eye='-')],
        [], g='rest', act=('perch', 'hay'), prefer=['curious'])
    o.r('guard_the_doors', 'Standing guard on the line before the doors with his chest out', 24, 'none',
        [k(.15, 'thresh', perch=1, y=.2), k(.35, 'thresh', perch=1, x=.6, y=-.5, b=-.3, w=.4, eye='>'), k(.6, 'thresh', perch=1, x=-.2, y=-.4, b=-.5, l=1, mark='halt'), k(.85, 'thresh', perch=1, x=.3, y=-.2, w=.5, eye='-')],
        [], g='rest', act=('guard', 'leaf'), prefer=['lonely'])
    # ---------------- weather
    o.r('chip_frost_off_lip', 'Chipping the frost off the door lip with the edge of his bill', 18, 'none',
        [k(.12, 'lip_a', x=.5, y=.6), k(.3, 'lip_a', x=1.2, y=.8, b=.4, mark='skrk'), k(.5, 'lip_b', x=1.3, y=.9, b=.5, l=1, mark='skrk'), k(.72, 'lip_b', x=1.1, y=.6, r=1), k(.88, eye='^')],
        [(.5, 'chip')], g='weather', act=('chip', 'lip'), when=['frost>.3'], say=["Lip iced over. Chipped it free. Hero stuff.", "Frost off the lip. Cold in the nostrils."])
    o.r('blow_on_frosted_glass', 'Blowing warm breath at the frosted left window glass until it clears', 18, 'none',
        [k(.12, 'window_l', x=.5, y=-.2), k(.3, 'window_l', x=1, y=-.4, b=-.2, mark='haah'), k(.5, 'window_l', x=1.1, y=-.5, b=-.3, w=.3, mark='haaah'), k(.72, 'window_l', x=.7, y=-.2, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'window'), when=['frost>.3'])
    o.r('kick_drift_off_step', 'Kicking the snow drift off the step in two big sweeps of his foot', 18, 'none',
        [k(.12, 'step_a', x=.2, y=.4, b=.3), k(.3, 'step_a', x=.3, y=.7, b=.6, l=1, mark='fff'), k(.5, 'step_a', x=.3, y=.7, b=.7, r=1, mark='FFF'), k(.72, 'step_b', x=.2, y=.4, b=.3, l=1), k(.88, eye='^')],
        [(.5, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Snow kicked. Step visible. Feet colder. Worth it.", "Drift gone. Dignity airborne."])
    o.r('plough_the_threshold', 'Pushing a trench along the standing line, chest first, drift piled up before him', 20, 'none',
        [k(.12, 'thresh', x=.4, y=.8, b=.6), k(.3, 'thresh', x=.7, y=1.2, b=1, mark='hrrn'), k(.5, 'thresh', x=.8, y=1.3, b=1.1, l=1, r=1), k(.72, 'thresh', x=.5, y=.8, b=.7), k(.88, y=.2, w=.5, eye='^')],
        [(.5, 'plough')], g='weather', act=('push', 'drift'), when=['drift>.5'])
    o.r('peck_off_rain_beads', 'Scraping the beads of rain off the lower left boards with the edge of his bill', 20, 'none',
        [k(.12, 'board_l', x=.6, y=.9, b=.3), k(.3, 'board_l', x=1.1, y=1.4, b=.5, mark='tp'), k(.5, 'plate_l', x=1.2, y=1.5, b=.7, l=1, mark='tp'), k(.7, 'board_l', x=1.1, y=1.3, b=.5, r=1, mark='tp'), k(.88, eye='^')],
        [(.5, 'flick')], g='weather', act=('scrape', 'board'), when=['obj_wetness>.3'])
    o.r('shake_the_rain_off', 'Shaking the rain off his back with the lower boards at his shoulder', 18, 'none',
        [k(.12, 'board_l', x=.2, y=.3, b=.2), k(.3, 'board_l', x=-.2, y=.7, b=.6, w=1, mark='brrr'), k(.5, 'board_l', x=.2, y=.7, b=.8, w=1, l=1), k(.7, 'board_l', x=-.2, y=.5, b=.5, w=1, r=1), k(.88, eye='^')],
        [(.5, 'spray')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    # ---------------- mishap
    o.r('skid_on_frosted_lip', 'Slipping off the frosted lip with both feet going different ways', 14, 'none',
        [k(.15, 'lip_a', perch=1, y=.2, b=.2), k(.3, 'lip_a', perch=1, x=.5, y=.4, b=-.2, l=1, w=.7, eye='O'), k(.5, 'step_a', x=-.5, y=.9, b=.9, r=1, w=1, mark='WHOA'), k(.7, 'thresh', y=1.3, b=1.4, eye='@', mark='*thud*'), k(.88, y=.4, b=.4, eye='-')],
        [(.5, 'grind')], g='mishap', act=('slip', 'lip'), when=['frost>.5'], say=["Frost is a liar. A lying, white liar.", "Feet went north. Duck went south. Barn watched."])
    o.r('bill_wedged_in_seam', 'Squeezing his bill into the seam between the leaves, wriggling, and tearing back out', 24, 'none',
        [k(.15, 'seam', x=.7, y=.5, b=.2), k(.3, 'seam', x=1.4, y=.4, b=.6, eye='O', mark='mm'), k(.5, 'seam', x=1.5, y=.4, b=.8, l=1, r=1, eye='@', mark='mmf!'), k(.7, 'seam', x=1.6, y=.5, b=1, w=1, mark='POP'), k(.88, x=-.2, y=.6, eye='>')],
        [(.5, 'scuff')], g='mishap', shown='head', act=('squeeze', 'seam'), say=["Seam bit back. Barn doors have a grudge.", "Bill freed. Pride still in the gap."])
    o.r('walk_into_the_leaf', 'Walking straight at the left leaf, eyes shut, and meeting it', 16, 'none',
        [k(.15, y=.1, b=.1), k(.35, x=.6, y=.2, b=.3, l=1), k(.55, 'brace_l', x=1.5, y=.6, b=.8, eye='@', mark='BONK'), k(.75, x=-.8, y=.4, b=.5, w=.6, eye='O'), k(.9, eye='-')],
        [], g='mishap', act=('walk_into', 'leaf'), say=["Door was closed. Door has always been closed.", "Walked straight into it. It had a point."])
    o.r('stamp_on_the_step', 'Stamping up and down on the step after the knock got no answer', 16, 'none',
        [k(.15, 'step_b', perch=1, y=.4, b=.4, l=1), k(.3, 'step_b', perch=1, y=.5, b=.7, r=1, mark='STOMP'), k(.5, 'step_b', perch=1, y=.5, b=.8, l=1, mark='STOMP'), k(.72, 'step_b', perch=1, y=.3, w=.7, eye='>'), k(.88, eye='-')],
        [(.5, 'scuff')], g='mishap', act=('stamp', 'step'), prefer=['grumpy'])
    o.r('catch_wing_on_nail', 'Catching a wingtip on a nail head while turning and tearing loose again', 18, 'wing',
        [k(.15, 'nail_r', reach=.5, x=.4, y=.3), k(.35, 'nail_r', reach=1, x=-.3, y=.4, b=.4, eye='O'), k(.55, 'nail_r', reach=.6, x=.4, y=.6, b=.7, l=1, r=1, mark='ack'), k(.75, y=.8, b=.9, eye='@'), k(.9, eye='-')],
        [(.55, 'dent')], g='mishap', act=('catch', 'nail'))
    # ---------------- show
    o.r('bow_to_the_barn', 'Bowing very low to the big doors as if they were royalty', 18, 'none',
        [k(.15, 'brace_r', y=.2), k(.35, 'brace_r', x=.4, y=1.2, b=.9, w=.6, eye='-'), k(.6, 'brace_r', x=.5, y=1.6, b=1.2, w=.8, mark='milord'), k(.85, 'brace_r', y=.2, eye='^')],
        [], g='show', act=('bow', 'brace'))
    o.r('present_the_barn', 'Showing off the whole front of the barn with a sweeping wing, like an estate agent', 20, 'wing',
        [k(.12, 'brace_l', reach=.4, x=-.3, y=.1, b=.2, l=1), k(.3, 'brace_l', reach=1, x=.1, y=-.8, b=-.5, mark='behold'), k(.5, 'seam', reach=.8, x=.6, y=-.5, b=.3, r=1), k(.7, 'brace_r', reach=1, x=.9, y=-.9, b=-.6, mark='charming'), k(.88, x=-.2, y=-.2, w=.3, eye='^')],
        [], g='show', act=('show', 'front'), say=["Spacious. Lots of potential. No viewings.", "Two doors, one hay stack, zero offers."])
    o.r('sing_to_the_hay', 'Singing a ballad to the hay stack with wing flourishes', 22, 'none',
        [k(.15, 'plate_l', x=.2, y=-.2), k(.35, 'hay_foot', x=-.2, y=-.8, b=.8, w=.8, mark='laa'), k(.6, 'hay_foot', x=1.2, y=-.9, b=-.4, w=1, l=1, eye='^', mark='LAAA'), k(.85, 'hay_foot', x=-.1, y=-.3, eye='-')],
        [], g='show', act=('sing', 'hay'), prefer=['happy'])
    o.r('dance_down_the_front', 'Dancing a jig from the left end of the lip, down the step and out to the line', 20, 'none',
        [k(.12, 'lip_a', perch=1, y=-.3, b=-.6, l=1, w=.6), k(.3, 'step_a', perch=1, y=.3, b=.5, r=1, w=1), k(.5, 'thresh', perch=1, y=-.4, b=-.7, l=1, w=1, mark='tada'), k(.7, 'step_b', perch=1, y=.4, b=.6, r=1, w=.8), k(.88, eye='^')],
        [], g='show', act=('dance', 'lip'), prefer=['happy'])
    o.emit()
    return o


def shed():
    P = pm('shed')
    o = Obj('shed', 'placed',
            parts=dict(board='the plank walls left and right of the door, a plank line every five columns', nail='the nail heads (o) set along the plank rows',
                       plate='the (=) plates set in the boards', window='the four-pane window glass in the left wall (cross mullion, glints)', sill='the ledge under the window, 75 px up',
                       jamb='the door frame post at the left of the door', panel='the two raised panel frames on the door leaf, upper and lower', crate='the little .--|-| box shape at the foot of the door',
                       lip='the door foot strip, 19 px up', step='the lower door-frame line, 9 px up', thresh='the standing line in front of the door',
                       tool='the T-headed tool leaning on the right wall, with its slanting handle', hook='the J-hook tool beside it', barrel='the barrel at the right: rim, hoops and staves',
                       hoop='the iron hoop round the barrel belly', roof='the corrugated tin roof, out of reach'),
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), warmth=(0, 0, 1), leaves=(0, 0, 1), askew=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('warmth', 'rate', .0006, 'sun'), ('warmth', 'rate', -.0004, 'night'), ('leaves', 'rate', .0025, 'windy'), ('leaves', 'rate', -.0003, 'calm')],
            effects=dict(scrub=[('obj.dirt', 'add', -.3)], sweep=[('obj.dirt', 'add', -.15)], wipe=[('obj.dirt', 'add', -.2)], dry=[('obj.wetness', 'add', -.3)],
                         dab=[('obj.wetness', 'add', -.25)], flick=[('obj.wetness', 'add', -.2)], hammer=[('obj.condition', 'add', .2)], dent=[('obj.condition', 'add', -.15)], scuff=[('obj.dirt', 'add', .12)],
                         chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], thaw=[('frost', 'mul', .5)], scoop=[('drift', 'mul', .2)], trench=[('drift', 'mul', .35)],
                         straighten=[('askew', 'set', 0)], jostle=[('askew', 'add', .4)], tilt=[('askew', 'add', .3)], rake=[('leaves', 'mul', .2)], toss=[('leaves', 'mul', .5)],
                         soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)], laugh=[('need.fun', 'add', 2)], hush=[('need.energy', 'add', 1)]),
            marks=[('frost', .3, '*.*.*', 'lip_a', 'frost'), ('frost', .3, '*.*', 'barrel_hoop', 'frost'), ('drift', .3, '.:*:.', 'barrel_rim', 'snow'), ('drift', .3, '.:*:.', 'step_a', 'snow'),
                   ('leaves', .3, '~ , ~ ,', 'step_b', 'leaf'), ('askew', .3, '\\ /', 'tool_t', 'dust')],
            anchors=dict(nail_l=P(16, 42), nail_l2=P(26, 49), plate_l=P(15, 45), window_l=P(19, 38), sill_l=P(17, 41), jamb_l=P(28, 44),
                         panel_u=P(40, 36), panel_l=P(40, 45), crate=P(46, 44), lip_a=P(34, 47, 'surface'), lip_b=P(46, 47, 'surface'), step_a=P(36, 48, 'surface'),
                         step_b=P(46, 48, 'surface'), thresh=P(41, 49, 'surface'), board_r=P(58, 46), nail_r=P(61, 49), plate_r=P(54, 45),
                         tool_t=P(59, 38), tool_h=P(63, 39), hook=P(64, 40), barrel_rim=P(73, 43, 'surface'), barrel_hoop=P(73, 46), barrel_stave=P(69, 48)))
    # ---------------- care
    o.r('scrub_barrel_staves', 'Scrubbing the barrel staves with a wing, hoop to foot', 20, 'wing',
        [k(.1, 'barrel_hoop', reach=.5, x=.3, y=.5), k(.26, 'barrel_hoop', reach=1, x=.6, y=.9, b=.3, l=1, mark='skrk'), k(.44, 'barrel_stave', reach=1, x=.8, y=1.2, b=.8, r=1, mark='skrk'), k(.64, 'barrel_stave', reach=1, x=1, y=1.4, b=1, l=1, mark='skrk'), k(.84, 'barrel_hoop', reach=.6, x=.3, y=.4, b=.2), k(.94, eye='^')],
        [(.64, 'scrub')], g='care', act=('scrub', 'barrel'), when=['obj_dirt>.3'], say=["Barrel was grey. Barrel is now brown. Progress.", "Scrubbed until my wing hurt. Barrel does not say thanks."])
    o.r('sweep_the_step', 'Sweeping the dust off the step and flicking it towards the yard with a wing', 18, 'wing',
        [k(.12, 'step_a', reach=.4, x=.1, y=.7, b=.3, l=1), k(.3, 'step_a', reach=1, x=.5, y=1, b=.5, r=1), k(.5, 'step_b', reach=1, x=.9, y=1.1, b=.4, l=1, mark='shff'), k(.7, 'thresh', reach=.8, x=.7, y=.8, b=.2, r=1), k(.88, eye='-')],
        [(.5, 'sweep')], g='care', act=('sweep', 'step'), when=['obj_dirt>.3'])
    o.r('wipe_the_window', 'Reaching up with a wing to wipe a clear arc over the window glass', 20, 'wing',
        [k(.1, 'sill_l', reach=.4, x=.2, y=-.1, b=-.2), k(.28, 'window_l', reach=1, x=.5, y=-.6, b=-.5, l=1, mark='squk'), k(.46, 'window_l', reach=1, x=.9, y=-.8, b=-.6, r=1, mark='squk'), k(.64, 'window_l', reach=.8, x=.4, y=-.4, b=-.3, l=1), k(.8, reach=.2, y=-.2, w=.5, eye='O'), k(.92, eye='^')],
        [(.46, 'wipe')], g='care', act=('wipe', 'window'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('dry_the_door_foot', 'Dragging his breast along the door foot to dry the strip after the rain', 20, 'none',
        [k(.12, 'lip_a', x=.8, y=.3, b=.2), k(.3, 'lip_a', x=1.2, y=.5, b=.7, mark='fsh'), k(.5, 'lip_b', x=1.3, y=.4, b=.8, l=1, mark='fsh'), k(.7, 'lip_b', x=.9, y=.6, b=.4, r=1), k(.88, x=.2, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'lip'), when=['obj_wetness>.3'])
    o.r('mend_the_lower_panel', 'Mending the lower door panel by hammering its loose rail back in with his bill', 18, 'none',
        [k(.1, x=.6, y=.8, b=.3), k(.24, 'panel_l', x=1.2, y=1.7, b=.8, l=1, mark='tak'), k(.4, 'nail_l2', x=.4, y=.7, b=-.3), k(.56, 'panel_l', x=1.3, y=1.9, b=1, r=1, mark='tak'), k(.72, x=.1, y=.4, w=.5), k(.84, 'panel_l', x=1.4, y=2, b=1.1, mark='TAK'), k(.94, eye='^')],
        [(.84, 'hammer')], g='care', act=('mend', 'panel'), when=['obj_condition<.6'], say=["Rail back in. Door looks smug.", "Three taps and a headache. Fixed."])
    o.r('straighten_the_tools', 'Straightening the leaning T-headed tool and its handle with a wing', 20, 'wing',
        [k(.1, 'tool_h', reach=.3, x=-.1, y=-.1, b=.1, r=1), k(.28, 'tool_t', reach=1, x=.2, y=-1.0, b=-.6, l=1, mark='nnf'), k(.48, 'tool_h', reach=.7, x=.8, y=-.3, b=-.1), k(.66, 'hook', reach=1, x=.5, y=-.7, b=-.5, w=.5, r=1), k(.84, x=-.4, y=0, b=.2, eye='^')],
        [(.48, 'straighten')], g='care', act=('straighten', 'tool'), when=['askew>.3'], ages=GROWN, say=["Tools upright. Wall looks organised. Lie.", "Straightened the lot. They lean on principle."])
    o.r('rake_leaves_off_the_step', 'Using both feet to rake the blown leaves off the step into a heap', 20, 'none',
        [k(.12, 'step_b', x=.2, y=.8, b=.3), k(.3, 'step_b', x=.6, y=1.2, b=.7, l=1, mark='shff'), k(.48, 'step_a', x=.5, y=1.3, b=.8, r=1, mark='shff'), k(.68, 'step_a', x=.3, y=1, b=.5, l=1), k(.86, y=.2, w=.5, eye='^')],
        [(.48, 'rake')], g='care', act=('rake', 'leaves'), when=['leaves>.3'], say=["Leaves in a heap. Wind will undo it. Wind is petty.", "Raked. Step is a step again."])
    # ---------------- use
    o.r('push_the_door', 'Pushing a shoulder against the shed door to test whether it is latched', 18, 'none',
        [k(.12, 'panel_l', x=.2, y=.2), k(.3, 'panel_l', x=-.6, y=.7, b=.6, mark='hup'), k(.5, 'panel_l', x=-.8, y=.8, b=1, l=1, r=1, mark='hnn'), k(.72, 'panel_l', x=-.1, y=.3, b=.3), k(.88, x=.3, y=.5, eye='-')],
        [], g='use', act=('push', 'door'), obj=[(.5, dict(shake=.1))], say=["Latched. Whatever is in there stays in there.", "Shoulder met door. Door won."])
    o.r('knock_on_the_panel', 'Knocking on the lower panel, then listening for footsteps that never come', 20, 'none',
        [k(.12, 'panel_l', x=.5, y=-.1), k(.28, 'panel_l', x=1.2, y=-.2, b=.3, mark='tok'), k(.42, 'panel_l', x=.1, y=-.3, b=-.2, w=.4), k(.58, 'panel_l', x=1.3, y=-.2, b=.4, mark='tok tok'), k(.76, x=-.5, y=-.6, b=-.3, w=.7, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'panel'))
    o.r('tug_the_hook', 'Tugging the J-hook tool with a wing to see whether it comes off the wall', 18, 'wing',
        [k(.12, 'hook', reach=.5, x=.3, y=-.3), k(.3, 'hook', reach=1, x=.5, y=-.6, b=.4, l=1, mark='hnf'), k(.48, 'hook', reach=1, x=-.3, y=-.4, b=.8, r=1, mark='hrrn'), k(.66, 'tool_h', reach=.6, x=.4, y=-.5, b=.3), k(.86, x=-.2, y=-.2, eye='O')],
        [(.48, 'jostle')], g='use', act=('tug', 'hook'), ages=GROWN, say=["Hook held. Tools wobbled. Wall judged me.", "Pulled. Nothing came off but my confidence."])
    o.r('peer_over_the_barrel_rim', 'Hopping up to peer over the barrel rim for whatever is inside', 22, 'none',
        [k(.12, 'barrel_stave', x=.2, y=.2, b=.2), k(.3, 'barrel_rim', perch=1, x=.4, y=-.2, b=-.5, w=.5), k(.5, 'barrel_rim', perch=1, x=1, y=.9, b=.2, eye='O', mark='...'), k(.72, 'barrel_rim', perch=1, x=.3, y=.1, b=-.3, w=.4, eye='>'), k(.9, eye='-')],
        [], g='use', act=('peer', 'barrel'), prefer=['curious'], say=["Barrel top is a lid. Disappointing lid.", "Looked in. It looked back, flat and wooden."])
    o.r('listen_to_the_tin_roof', 'Cocking his head to listen for the tin roof ticking as the sun warms it', 22, 'none',
        [k(.15, x=.3, y=-.5, b=-.2, l=1, eye='O'), k(.35, x=-.6, y=-1.4, b=-.8, w=.5, mark='...'), k(.58, x=-.9, y=-1.8, b=.3, r=1, w=.2, eye='-', mark='tik'), k(.8, x=.4, y=.4, b=.5, eye='^')],
        [], g='use', act=('listen', 'roof'), far=True, when=['warmth>.3', 'sun'], prefer=['curious'], say=["Roof ticks when warm. Roof, you talk too much.", "Heard the tin tick. It is gossiping about the sun."])
    # ---------------- play
    o.r('hop_onto_the_barrel', 'Taking a run and a hop onto the barrel rim, then straight off again', 18, 'none',
        [k(.1, 'step_b', perch=1, x=.2, y=.2, b=.3), k(.28, 'barrel_stave', x=.8, y=.4, b=-.6, l=1, w=.8), k(.46, 'barrel_rim', perch=1, x=.4, y=-.4, b=-.9, r=1, w=1, mark='hup'), k(.64, 'barrel_rim', perch=1, x=-.2, y=-.2, b=.5, w=.6), k(.84, 'thresh', y=.6, b=.7, w=.4), k(.94, eye='^')],
        [], g='play', act=('hop', 'barrel'), prefer=['happy'])
    o.r('race_round_the_barrel', 'Running a race from the door foot to the barrel, round the hoop and back', 16, 'none',
        [k(.1, 'lip_b', perch=1, x=.5, y=.1, b=.2, w=.5), k(.3, 'barrel_stave', x=1, y=.4, b=.4, l=1, w=1, mark='zoom'), k(.5, 'barrel_hoop', x=.9, y=.5, b=.5, r=1, w=1), k(.7, 'barrel_stave', x=.8, y=.3, b=.3, l=1, w=.8), k(.9, 'lip_b', perch=1, y=.3, eye='^')],
        [], g='play', act=('race', 'barrel'), prefer=['happy'])
    o.r('hide_among_the_tools', 'Flattening himself against the wall to hide among the leaning tools', 20, 'none',
        [k(.12, 'board_r', x=-.2, y=.3), k(.3, 'tool_h', x=-.9, y=.7, b=.6, eye='O'), k(.52, 'board_r', x=-1, y=.9, b=.9, mark='shh'), k(.7, x=1.2, y=-.4, b=-.5, w=1, l=1, r=1, mark='RAH'), k(.88, eye='^')],
        [], g='play', act=('hide', 'tool'), prefer=['young'])
    o.r('drum_the_hoop', 'Drumming a steady beat on the barrel hoop and staves with his bill', 18, 'none',
        [k(.12, 'barrel_hoop', x=1, y=.4, b=.3, mark='bom'), k(.3, 'barrel_stave', x=.9, y=.8, b=-.3, l=1, mark='bom'), k(.5, 'barrel_hoop', x=1.2, y=.5, b=.4, r=1, mark='bom bom'), k(.7, 'barrel_stave', x=.8, y=.7, b=-.2, l=1, mark='BOM'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'hoop'), prefer=['happy'], say=["Barrel has the deepest voice in the yard.", "Drummed it hollow. Empty. Like my plans."])
    o.r('balance_on_the_foot_strip', 'Balancing along the door foot with his wings out, end to end', 18, 'none',
        [k(.12, 'lip_a', perch=1, y=-.2, w=.6), k(.32, 'lip_a', perch=1, x=.4, b=.3, r=1, w=1), k(.55, 'lip_b', perch=1, x=.6, b=.5, l=1, w=1, mark='eep'), k(.78, 'lip_b', perch=1, y=.2, b=.2, w=.7), k(.92, eye='^')],
        [], g='play', act=('balance', 'lip'))
    o.r('throw_the_leaves', 'Throwing a wingful of the blown leaves in the air above the step', 18, 'wing',
        [k(.12, 'step_b', reach=.4, x=.1, y=.9, b=.4), k(.28, 'step_b', reach=1, x=.3, y=1.4, b=.9, l=1, mark='scoop'), k(.48, 'step_b', reach=.2, x=.4, y=-.8, b=-.8, r=1, w=1, mark='WHEE'), k(.68, 'step_a', reach=.6, x=.2, y=.5, b=.3), k(.86, y=.1, eye='^')],
        [(.48, 'toss')], g='play', act=('throw', 'leaves'), when=['leaves>.3'], prefer=['happy'], say=["Leaves went up. Leaves came down. Peak cinema.", "Threw them high. Gravity did the rest."])
    # ---------------- test
    o.r('tap_the_boards', 'Tapping the right wall from the nails to the plate to hear where it sounds hollow', 18, 'none',
        [k(.1, 'nail_r', x=1.3, y=.8, b=.6, mark='tok'), k(.26, 'board_r', x=.8, y=-.4, b=-.4, l=1, mark='tok'), k(.44, 'plate_r', x=.2, y=-.7, b=-.1, w=.8, eye='-'), k(.62, 'board_r', x=1.5, y=1, b=.8, r=1, mark='tonk'), k(.8, eye='^')],
        [], g='test', act=('tap', 'board'))
    o.r('count_the_plates', 'Touching each plate on the walls and counting under his breath', 22, 'none',
        [k(.08, 'plate_l', x=1.1, y=1.5, b=.9, mark='1'), k(.28, 'nail_l', x=1.3, y=1.3, b=.2, r=1, mark='2'), k(.5, 'plate_r', x=.9, y=1.2, b=1.1, l=1, mark='3'), k(.7, 'nail_r', x=1.4, y=1.7, b=.5, r=1, mark='4'), k(.86, x=-.7, y=-.5, w=.7, eye='-', mark='four')],
        [], g='test', act=('count', 'plate'), prefer=['curious'])
    o.r('weigh_the_barrel', 'Leaning his whole weight into the barrel to weigh whether it is full', 20, 'none',
        [k(.12, 'barrel_hoop', x=.3, y=.4, b=.2), k(.3, 'barrel_stave', x=-.4, y=.8, b=.7, mark='hnn'), k(.5, 'barrel_rim', x=-.6, y=.9, b=1, l=1, r=1, mark='hnnf'), k(.7, 'barrel_rim', x=-.1, y=.3, b=.3, w=.5, eye='-', mark='full'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'barrel'), ages=GROWN)
    o.r('taste_the_tool_head', 'Touching his tongue to the cold T-head of the tool to taste what it is made of', 20, 'none',
        [k(.12, 'tool_t', x=.4, y=-.3, b=-.2), k(.3, 'tool_t', x=1.1, y=-.5, b=.2, mark='lk'), k(.5, x=.1, y=.1, eye='O', mark='bleh'), k(.7, x=-.3, y=.6, b=.3, eye='-', mark='iron'), k(.86, eye='>')],
        [], g='test', act=('taste', 'tool'), ages=GROWN)
    o.r('prod_the_sill', 'Prodding the window sill and glass with a twig to see if it is shut', 20, 'twig',
        [k(.12, 'sill_l', reach=.8, x=.1, y=-.4, b=-.2), k(.3, 'window_l', reach=1, x=.9, y=-.8, b=-.5, w=.4, mark='tk'), k(.5, 'sill_l', reach=1, x=.5, y=-.2, b=.2, mark='tk tk'), k(.72, 'window_l', reach=.6, x=.3, y=-.6, b=-.3), k(.9, x=-.4, y=-.2, eye='-')],
        [], g='test', act=('prod', 'sill'))
    o.r('hook_a_tool_with_a_twig', 'Hooking the J-hook tool with a twig to see whether it will come down', 22, 'twig',
        [k(.14, 'hook', reach=.5, x=.2, y=-.4), k(.32, 'hook', reach=1, x=.5, y=-.7, b=-.3, mark='tk'), k(.52, 'tool_t', reach=1, x=-.2, y=-.8, b=-.5, w=.3, mark='scrk'), k(.72, 'hook', reach=.7, x=.4, y=-.5, b=-.2), k(.9, x=-.3, y=-.2, eye='-')],
        [(.52, 'tilt')], g='test', act=('hook', 'tool'), say=["Twig caught the hook. Hook caught nothing. Even.", "Fished at the wall. Wall kept its tools."])
    # ---------------- rest
    o.r('lean_on_the_barrel', 'Leaning his back against the sun-warmed barrel and soaking it up', 24, 'none',
        [k(.1, 'barrel_stave', x=.5, y=.1, b=.1, l=1), k(.3, 'barrel_stave', x=-.8, y=.6, b=.3, eye='-'), k(.55, 'barrel_hoop', x=-1.1, y=.5, b=.9, eye='-', mark='ahh'), k(.8, 'barrel_hoop', x=-.6, y=.2, b=.6, r=1, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'barrel'), when=['warmth>.3', 'sun'], say=["Warm barrel. Back against it. Done thinking.", "Staves hold the heat. I hold the staves."])
    o.r('sit_on_the_shed_step', 'Sitting on the step with his feet tucked, looking at the yard and not the shed', 24, 'none',
        [k(.12, 'step_a', perch=1, x=.3, y=-.4, b=.1, l=1), k(.3, 'step_a', perch=1, x=-.1, y=.2, b=.6, eye='-'), k(.6, 'step_a', perch=1, x=-.2, y=.3, b=1.3, eye='-', mark='...'), k(.85, 'step_a', perch=1, x=.2, y=-.1, b=.2, r=1, eye='^')],
        [], g='rest', act=('sit', 'step'))
    o.r('nap_on_the_door_foot', 'Taking a nap curled along the door foot with his bill under his wing', 30, 'none',
        [k(.15, 'lip_a', perch=1, y=.1, b=.3), k(.35, 'lip_a', perch=1, y=.9, b=1.1, eye='-'), k(.6, 'lip_a', perch=1, y=1.1, b=1.3, eye='-', mark='zzz'), k(.85, 'lip_a', perch=1, y=.3, b=.5, eye='^')],
        [(.6, 'hush')], g='rest', act=('nap', 'lip'), prefer=['tired'], say=["Door foot nap. Hard bed. Strong dreams.", "Slept on a strip. Woke up striped."])
    o.r('perch_on_the_barrel', 'Perching on the barrel rim like a lookout with nothing to look out for', 24, 'none',
        [k(.14, 'barrel_rim', perch=1, x=.1, y=-.4, b=-.3, w=.5), k(.36, 'barrel_rim', perch=1, x=.7, y=-.6, b=.1, eye='O'), k(.6, 'barrel_rim', perch=1, x=-.6, y=-.3, b=.3, w=.3, mark='hm'), k(.86, 'barrel_rim', perch=1, x=.2, y=-.1, eye='-')],
        [], g='rest', act=('perch', 'barrel'), prefer=['curious'])
    o.r('sulk_at_the_tools', 'Sulking at the wall with his back to the tools, as though they started it', 20, 'none',
        [k(.15, 'board_r', x=.2, y=.2), k(.35, 'board_r', x=-.7, y=.9, b=.6, eye='-', mark='hmph'), k(.6, 'board_r', x=-.8, y=1, b=.9, l=1, eye='>'), k(.85, 'board_r', x=-.5, y=.3, b=.3, eye='-')],
        [], g='rest', act=('sulk', 'tool'), prefer=['grumpy', 'sad'], say=["The tools know what they did.", "Not speaking to the T-thing. Or its friend."])
    o.r('guard_the_shed_door', 'Standing guard on the line before the shed door, chin up', 24, 'none',
        [k(.12, 'thresh', perch=1, x=.4, y=-.1, b=.2, r=1), k(.34, 'thresh', perch=1, x=1, y=-.9, b=-.6, w=.8, eye='>'), k(.58, 'thresh', perch=1, x=-.5, y=-.7, b=-.2, l=1, w=.3, mark='halt'), k(.86, 'thresh', perch=1, x=.1, y=0, b=.1, w=.6, eye='-')],
        [], g='rest', act=('guard', 'door'), prefer=['lonely'])
    o.r('lean_on_the_door_post', 'Leaning on the door post with one foot crossed over the other', 20, 'none',
        [k(.12, 'jamb_l', x=.3, y=.3), k(.35, 'jamb_l', x=-.2, y=.8, b=.5, l=1, eye='-'), k(.6, 'jamb_l', x=-.3, y=.9, b=.9, r=1, eye='-', mark='hm'), k(.82, 'jamb_l', x=-.2, y=.4, b=.4, eye='>')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    # ---------------- weather
    o.r('chip_frost_off_the_foot', 'Chipping the frost off the door foot strip with the edge of his bill', 18, 'none',
        [k(.1, 'lip_b', x=.9, y=1.1, b=.6, r=1), k(.28, 'lip_b', x=1.5, y=1.4, b=.9, mark='tk'), k(.48, 'lip_a', x=1.6, y=1.5, b=1, l=1, mark='tk'), k(.7, 'lip_a', x=.7, y=1, b=.5), k(.88, x=-.2, w=.4, eye='^')],
        [(.48, 'chip')], g='weather', act=('chip', 'lip'), when=['frost>.3'], say=["Foot strip iced over. Chipped it free.", "Frost off the door. Nostrils still frozen."])
    o.r('blow_on_the_frosted_hoop', 'Blowing warm breath along the frosted barrel hoop until it drips', 18, 'none',
        [k(.12, 'barrel_stave', x=.5, y=.2), k(.3, 'barrel_hoop', x=1, y=-.2, b=.2, mark='haah'), k(.5, 'barrel_stave', x=1.1, y=-.3, b=.3, w=.3, mark='haaah'), k(.72, 'barrel_hoop', x=.7, y=0, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'hoop'), when=['frost>.3'])
    o.r('scoop_snow_off_the_barrel', 'Scooping the snow cap off the barrel rim in wingfuls', 20, 'wing',
        [k(.12, 'barrel_rim', reach=.4, x=.2, y=-.4, b=-.3), k(.3, 'barrel_rim', reach=1, x=.5, y=-.2, b=.2, l=1, mark='fsh'), k(.5, 'barrel_rim', reach=1, x=.7, y=-.3, b=.4, r=1, mark='fsh'), k(.7, 'barrel_stave', reach=.6, x=.3, y=.4, b=.2), k(.88, eye='^')],
        [(.5, 'scoop')], g='weather', act=('scoop', 'drift'), when=['drift>.3'], ages=GROWN)
    o.r('dig_a_trench_to_the_door', 'Digging a trench through the drift in front of the door, chest first', 22, 'none',
        [k(.12, 'thresh', x=.4, y=.9, b=.5), k(.3, 'step_b', x=.8, y=1.3, b=1, mark='hrrn'), k(.5, 'step_a', x=.9, y=1.4, b=1.1, l=1, r=1), k(.72, 'thresh', x=.5, y=.9, b=.7), k(.88, y=.2, w=.5, eye='^')],
        [(.5, 'trench')], g='weather', act=('dig', 'drift'), when=['drift>.5'])
    o.r('dab_the_rain_off_the_tools', 'Using a dry wing to wipe the rain off the T-head of the tool', 20, 'wing',
        [k(.12, 'tool_h', reach=.5, x=.2, y=-.3), k(.3, 'tool_t', reach=1, x=.4, y=-.6, b=-.4, mark='squk'), k(.5, 'tool_t', reach=1, x=.7, y=-.7, b=-.5, r=1, mark='squk'), k(.7, 'hook', reach=.8, x=.5, y=-.4, b=-.3, l=1), k(.88, eye='^')],
        [(.5, 'dab')], g='weather', act=('wipe', 'tool'), when=['obj_wetness>.3'], ages=GROWN)
    o.r('shelter_in_the_door_foot', 'Pressing against the door to shelter from the rain while the tin roof drums', 34, 'none',
        [k(.12, 'panel_l', x=-.2, y=.3), k(.3, 'jamb_l', x=-.5, y=.8, b=.6, w=1, eye='-', mark='drum'), k(.55, 'panel_l', x=-.6, y=.9, b=.9, w=1, eye='>', mark='drum drum'), k(.8, 'jamb_l', x=-.3, y=.4, b=.4, w=.6, eye='^')],
        [], g='weather', act=('shelter', 'roof'), when=['wet', 'storm'], say=["Roof sounds like a drum kit. Door post is my umbrella.", "Rain on tin. Duck on door. Both of us are loud."])
    # ---------------- mishap
    o.r('bill_frozen_to_the_hoop', 'Licking the iced barrel hoop, getting stuck there, and tearing free', 24, 'none',
        [k(.15, 'barrel_hoop', x=.7, y=.8, b=.3), k(.3, 'barrel_hoop', x=1.4, y=1.1, b=.6, eye='O', mark='mm'), k(.5, 'barrel_hoop', x=1.5, y=1.2, b=.8, l=1, r=1, eye='@', mark='mmf!'), k(.7, 'barrel_hoop', x=1.6, y=1.3, b=1, w=1, mark='POP'), k(.88, x=-.2, y=.6, eye='>')],
        [(.7, 'thaw')], g='mishap', act=('stuck', 'hoop'), when=['frost>.5'], say=["Hoop tastes like regret. And iron. Mostly regret.", "Frozen to a hoop. Bill is not for kissing."])
    o.r('walk_into_the_shed_door', 'Walking straight at the shed door, thinking it was open, and meeting it', 16, 'none',
        [k(.12, x=.2, y=-.2, b=-.1), k(.3, x=.9, y=-.5, b=.5, r=1, w=.4), k(.5, 'panel_u', x=1.9, y=.2, b=1.1, eye='@', mark='THUNK'), k(.72, x=-1.1, y=.7, b=.2, l=1, w=.9, eye='O'), k(.9, y=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'door'), say=["It was latched. It is always latched.", "Face first into a door. Classic me."])
    o.r('wing_caught_on_the_hook', 'Catching a wingtip on the J-hook while turning and tearing loose again', 18, 'wing',
        [k(.15, 'hook', reach=.5, x=.4, y=-.2), k(.35, 'hook', reach=1, x=-.3, y=-.3, b=.4, eye='O'), k(.55, 'hook', reach=.6, x=.4, y=-.1, b=.7, l=1, r=1, mark='ack'), k(.75, y=.8, b=.9, eye='@'), k(.9, eye='-')],
        [(.55, 'dent')], g='mishap', act=('catch', 'hook'), ages=GROWN)
    o.r('knock_the_tool_askew', 'Knocking the T-headed tool crooked with a clumsy bill and flinching', 18, 'none',
        [k(.15, 'tool_h', x=.5, y=-.2, b=-.1), k(.32, 'tool_h', x=1.2, y=-.4, b=.3, eye='O', mark='clk'), k(.5, 'tool_t', x=1.3, y=-.5, b=.2, l=1, mark='KLANG'), k(.7, x=-.5, y=.3, b=.5, w=.7, eye='>'), k(.88, eye='-')],
        [(.5, 'jostle')], g='mishap', act=('knock', 'tool'), ages=GROWN)
    o.r('trip_on_the_step_line', 'Kicking the step line by accident while running and sprawling over the barrel foot', 16, 'none',
        [k(.15, 'step_b', y=.1, b=.2), k(.32, 'step_b', x=.6, y=.5, b=-.2, l=1, w=.7), k(.5, 'barrel_stave', x=1.2, y=1.2, b=1.2, eye='@', mark='OOF'), k(.72, 'barrel_stave', y=1.4, b=1.4, eye='-'), k(.88, y=.4, b=.5, eye='>')],
        [(.5, 'scuff')], g='mishap', act=('kick', 'step'), say=["Step line and I disagreed. It stayed put.", "Sprawled by the barrel. Barrel kept quiet."])
    # ---------------- show
    o.r('show_off_the_tools', 'Showing off the tools one by one with a wing, like a very small salesman', 22, 'wing',
        [k(.14, 'tool_t', reach=.5, x=.2, y=-.5, b=-.2), k(.32, 'tool_t', reach=1, x=.3, y=-.8, b=-.4, mark='behold'), k(.5, 'tool_h', reach=1, x=.4, y=-.7, b=-.3, l=1), k(.68, 'hook', reach=1, x=.5, y=-.8, b=-.4, r=1, mark='and this'), k(.86, x=-.1, y=-.2, w=.3, eye='^')],
        [], g='show', act=('show', 'tool'), say=["Premium tools. Used once. By a duck.", "Hoe, hook, handle. Offers welcome."])
    o.r('sing_to_the_barrel', 'Singing a ballad into the barrel and listening to it come back hollow', 22, 'none',
        [k(.15, 'barrel_rim', x=.3, y=-.4, b=.2), k(.35, 'board_r', x=-.2, y=-.9, b=.8, w=.8, mark='laa'), k(.6, 'barrel_rim', x=1.2, y=-1, b=-.4, w=1, l=1, eye='^', mark='LAAA'), k(.85, 'board_r', x=-.1, y=-.3, eye='-')],
        [], g='show', act=('sing', 'barrel'), prefer=['happy'])
    o.r('dance_on_the_door_foot', 'Dancing a quick jig along the door foot and down the step', 18, 'none',
        [k(.12, 'lip_a', perch=1, y=-.4, b=-.7, l=1, w=.7), k(.3, 'lip_b', perch=1, y=.4, b=.6, r=1, w=1), k(.5, 'step_b', perch=1, y=-.5, b=-.8, l=1, w=1, mark='tada'), k(.7, 'step_a', perch=1, y=.3, b=.5, r=1, w=.8), k(.88, eye='^')],
        [], g='show', act=('dance', 'lip'), prefer=['happy'])
    o.r('pat_the_crate', 'Patting the little box at the door foot with a wing as if it were a pet', 18, 'wing',
        [k(.12, 'crate', reach=.4, x=.2, y=.5, b=.2), k(.3, 'crate', reach=1, x=.5, y=.8, b=.5, l=1, mark='pat'), k(.5, 'crate', reach=1, x=.6, y=.9, b=.6, r=1, mark='pat pat'), k(.7, 'crate', reach=.6, x=.2, y=.4, b=.3, w=.3), k(.88, eye='^')],
        [], g='show', act=('pat', 'crate'), prefer=['happy'], say=["Good box. Sit. It sat.", "Patted it twice. Box did not wag."])
    o.r('pull_at_the_lower_panel', 'Pulling at the lower panel rail with his bill to see if the door will open', 18, 'none',
        [k(.12, 'nail_l2', x=.7, y=.4, b=.3), k(.3, 'panel_l', x=1.5, y=.6, b=.9, l=1, mark='hnf'), k(.5, 'panel_l', x=1.7, y=.7, b=1.1, r=1, mark='hnnf'), k(.7, 'nail_l2', x=.4, y=.3, b=.4, w=.6), k(.88, x=-.3, eye='>')],
        [], g='use', act=('pull', 'panel'), obj=[(.5, dict(sway=.1))], say=["Pulled. Panel pulled back. Stalemate.", "Door does not open for ducks, it turns out."])
    o.r('scrape_rain_beads_off_the_staves', 'Scraping the rain beads off the barrel staves with the edge of his bill', 20, 'none',
        [k(.1, 'barrel_stave', x=.4, y=1.2, b=.7, l=1), k(.28, 'barrel_stave', x=1.0, y=1.8, b=.4, mark='tp'), k(.46, 'barrel_hoop', x=1.4, y=1.2, b=1, r=1, mark='tp'), k(.66, 'barrel_stave', x=.8, y=1.6, b=.2, l=1, mark='tp'), k(.86, x=-.1, w=.4, eye='^')],
        [(.46, 'flick')], g='weather', act=('scrape', 'barrel'), when=['obj_wetness>.3'])
    o.emit()
    return o


def greenhouse():
    P = pm('greenhouse')
    o = Obj('greenhouse', 'placed',
            parts=dict(pane='the glass pane bays of the side walls, divided by vertical bars', rail='the horizontal glazing rails across the walls', post='the vertical end posts at the outer corners',
                       planter='the flower planters along the front wall, each with its flowers', flower='the (*) blossoms on tall stems above each planter',
                       bench='the potting bench running in front of the whole wall, a top and a front edge', pot='the two small pots at the far right foot',
                       door='the door leaf in the middle, upright planks with raised panels', box='the little .--|-. box shape at the foot of the door',
                       step='the lower door-frame line, 9 px up', thresh='the standing line in front of the door', roof='the glass roof, glazing bars and glints, out of reach'),
            fields=dict(mist=(0, 0, 1), frost=(0, 0, 1), warmth=(0, 0, 1), petals=(0, 0, 1)),
            physics=[('mist', 'rate', .0025, 'cold'), ('mist', 'rate', .0025, 'wet'), ('mist', 'rate', -.002, 'warm'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('warmth', 'rate', .0008, 'sun'), ('warmth', 'rate', -.0005, 'night')],
            effects=dict(clear=[('mist', 'mul', .3)], polish=[('obj.dirt', 'add', -.2)], sweep=[('petals', 'mul', .2), ('need.cleanliness', 'add', 1)], scrub=[('obj.dirt', 'add', -.3)],
                         dry=[('obj.wetness', 'add', -.3)], shower=[('petals', 'add', .3)], mend=[('obj.condition', 'add', .2)], crack=[('obj.condition', 'add', -.15)],
                         perk=[('petals', 'mul', .5)], sneeze=[('petals', 'add', .3)], shed=[('petals', 'add', .25)], snap=[('petals', 'add', .35)], smudge=[('obj.dirt', 'add', .12)],
                         chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], flick=[('obj.wetness', 'add', -.25)], spray=[('obj.wetness', 'add', .15)],
                         fan=[('warmth', 'add', -.3), ('need.energy', 'add', 1)], soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)], laugh=[('need.fun', 'add', 2)], hush=[('need.energy', 'add', 1)]),
            marks=[('mist', .3, ':. .: :.', 'pane_l_hi', 'water'), ('mist', .3, '.: :. .:', 'pane_r_hi', 'water'), ('frost', .3, '*.*.*', 'pane_l_low', 'frost'),
                   ('frost', .3, '*.*.*', 'pane_r_low', 'frost'), ('petals', .3, '* . * .', 'bench_a', 'plant')],
            anchors=dict(planter_l1=P(16, 52, 'surface'), planter_l2=P(28, 52, 'surface'), planter_r1=P(76, 52), planter_r2=P(88, 52), flower_l1=P(16, 47), flower_l2=P(28, 47), flower_r1=P(76, 47),
                         bench_a=P(24, 50, 'surface'), bench_b=P(70, 50, 'surface'), bench_front=P(58, 52), pane_l_low=P(21, 46), pane_l_hi=P(22, 41), pane_r_low=P(82, 46), pane_r_hi=P(84, 41),
                         rail_l=P(24, 44), rail_l_low=P(24, 49, 'surface'), rail_r_low=P(82, 49, 'surface'), post_l=P(12, 52), post_r=P(96, 50), door_panel=P(50, 43),
                         step_a=P(48, 53, 'surface'), thresh=P(55, 54, 'surface'), pot_a=P(90, 54, 'surface'), pot_b=P(94, 54, 'surface')))
    # ---------------- care
    o.r('wipe_the_mist_off', 'Reaching up with a wing to wipe a clear window through the mist on the glass', 20, 'wing',
        [k(.1, 'pane_l_hi', reach=.4, x=.2, y=-.2, b=-.2), k(.28, 'pane_l_hi', reach=1, x=.7, y=-.7, b=-.5, r=1, mark='squk'), k(.46, 'pane_l_low', reach=1, x=.5, y=-.2, b=-.1, l=1, mark='squk'), k(.64, 'pane_l_hi', reach=.8, x=.9, y=-.9, b=-.6, r=1), k(.8, reach=.2, y=-.2, w=.5, eye='O'), k(.92, eye='^')],
        [(.46, 'clear')], g='care', act=('wipe', 'pane'), when=['mist>.3'], ages=GROWN, say=["Wiped a peephole. Mist filed a complaint.", "Clear patch. Duck-shaped smear. Art."])
    o.r('polish_the_glazing_rail', 'Polishing the glazing rail end to end with his breast until it shines', 20, 'none',
        [k(.1, 'rail_l_low', x=.6, y=.4, b=.2), k(.3, 'rail_l_low', x=1.1, y=.8, b=.6, l=1, mark='sqk'), k(.5, 'rail_r_low', x=.4, y=.6, b=.4, r=1), k(.7, 'rail_r_low', x=1.2, y=.9, b=.7, mark='sqk'), k(.88, x=.2, w=.3, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'rail'), when=['obj_dirt>.3'], say=["Rail shines. I can see my own bill in it. Gorgeous.", "Polished with my chest. Chest is now the cleanest part."])
    o.r('sweep_up_the_petals', 'Sweeping the fallen petals off the bench top into a little heap with a wing', 18, 'wing',
        [k(.1, 'bench_a', reach=.4, x=.2, y=.5, b=.2), k(.28, 'bench_a', reach=1, x=.6, y=.9, b=.5, l=1, mark='shff'), k(.48, 'bench_b', reach=1, x=.9, y=1.1, b=.4, r=1, mark='shff'), k(.68, 'bench_b', reach=.7, x=.4, y=.7, b=.2), k(.86, eye='-')],
        [(.48, 'sweep')], g='care', act=('sweep', 'petals'), when=['petals>.3'], say=["Petals in a heap. Pretty heap. Still a heap.", "Swept up the confetti the flowers threw."])
    o.r('scrub_the_pots', 'Scrubbing both small pots with a wing until the clay shows through', 20, 'wing',
        [k(.1, 'pot_a', reach=.4, x=.3, y=.9, b=.4), k(.28, 'pot_a', reach=1, x=.7, y=1.3, b=.8, l=1, mark='skrk'), k(.48, 'pot_b', reach=1, x=.9, y=1.5, b=1, r=1, mark='skrk'), k(.68, 'pot_b', reach=.8, x=.5, y=1, b=.5, l=1), k(.86, eye='^')],
        [(.48, 'scrub')], g='care', act=('scrub', 'pot'), when=['obj_dirt>.3'])
    o.r('dry_the_bench_top', 'Dragging his belly along the bench top to dry the dripped condensation', 20, 'none',
        [k(.12, 'bench_a', perch=1, x=.4, y=.5, b=.7), k(.3, 'bench_a', perch=1, x=.9, y=.8, b=1, mark='fsh'), k(.5, 'bench_b', perch=1, x=1, y=.9, b=1.1, l=1, mark='fsh'), k(.7, 'bench_b', perch=1, x=.4, y=.5, b=.6), k(.88, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'bench'), when=['obj_wetness>.3'])
    o.r('mend_a_glazing_bar', 'Mending a loose glazing bar by leaning on it until it clicks back into the post', 18, 'none',
        [k(.1, 'post_l', x=.5, y=.5, b=.3), k(.26, 'post_l', x=1.3, y=.9, b=.9, l=1, mark='nnf'), k(.42, 'post_l', x=1.5, y=1, b=1.1, r=1, mark='nnnf'), k(.6, 'post_l', x=1.6, y=1.1, b=1.2, w=.4, mark='CLICK'), k(.78, x=.1, y=.4, b=.3), k(.9, eye='^')],
        [(.6, 'mend')], g='care', act=('mend', 'post'), when=['obj_condition<.6'], say=["Bar clicked in. Glasshouse stands. Glasshouse stares.", "Fixed it with my whole weight. Technique."])
    o.r('straighten_the_flowers', 'Straightening the bent flower stems with a wing so the blossoms face front', 20, 'wing',
        [k(.1, 'flower_l1', reach=.5, x=-.2, y=-.1, b=.1, r=1), k(.28, 'flower_l1', reach=1, x=.3, y=-1.1, b=-.7, mark='nnf'), k(.48, 'flower_l2', reach=1, x=.9, y=-.5, b=-.2, l=1, r=1), k(.68, 'flower_r1', reach=.8, x=.1, y=-.9, b=-.6, w=.4), k(.86, x=-.5, y=.1, b=.2, eye='^')],
        [(.48, 'perk')], g='care', act=('straighten', 'flower'), when=['petals>.3'], prefer=['happy'], ages=GROWN)
    # ---------------- use
    o.r('sniff_the_blossoms', 'Sniffing every blossom along the left planters, then sneezing at the last one', 22, 'none',
        [k(.1, 'flower_l1', x=.6, y=-.3, b=-.2), k(.28, 'flower_l1', x=1.2, y=-.1, b=.2, mark='sniff'), k(.46, 'flower_l2', x=1.2, y=-.2, b=.1, mark='sniff'), k(.66, 'flower_l2', x=1.6, y=-.4, b=-.3, w=.6, eye='O', mark='ah'), k(.82, 'flower_l2', x=-.8, y=.9, b=1, w=.8, eye='@', mark='CHOO')],
        [(.82, 'sneeze')], g='use', act=('sniff', 'planter'), prefer=['curious'], say=["Smells green. Smells posh. Smells of sneezing.", "Petals everywhere. My fault. Nose's fault."])
    o.r('nudge_a_flower_stem', 'Nudging a tall flower stem with his bill to see how far it will bob', 18, 'none',
        [k(.12, 'flower_r1', x=.5, y=-.5, b=-.3), k(.3, 'flower_r1', x=1, y=-.7, b=-.5, w=.3, mark='bop'), k(.5, 'flower_r1', x=.2, y=-.4, b=-.2, eye='O'), k(.68, 'flower_r1', x=1.1, y=-.7, b=-.5, l=1, mark='bop'), k(.86, x=-.2, eye='^')],
        [(.68, 'shed')], g='use', act=('nudge', 'flower'))
    o.r('push_the_glass_house_door', 'Pushing at the door leaf with a shoulder until the whole front hums', 18, 'none',
        [k(.12, 'door_panel', x=.1, y=.2, b=.2), k(.3, 'door_panel', x=-.7, y=.6, b=.8, mark='hup'), k(.5, 'door_panel', x=-.9, y=.7, b=1.1, r=1, mark='hnn'), k(.72, 'door_panel', x=-.2, y=.3, b=.4, l=1), k(.88, x=.4, y=.4, eye='-')],
        [], g='use', act=('push', 'door'), obj=[(.5, dict(shake=.1))])
    o.r('knock_on_a_pane', 'Knocking on a glass pane with his bill and waiting for a reply', 18, 'none',
        [k(.12, 'pane_r_low', x=.6, y=-.1), k(.28, 'pane_r_low', x=1.3, y=-.2, b=.3, mark='tink'), k(.44, 'pane_r_low', x=.2, y=-.2, b=-.2, w=.3), k(.6, 'pane_r_low', x=1.4, y=-.2, b=.4, mark='tink tink'), k(.78, x=-.6, y=-.5, b=-.3, w=.6, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'pane'), say=["Knocked on glass. Glass said nothing, clearly.", "Only plants home. Plants are snobs."])
    o.r('press_a_bill_print', 'Pressing his bill flat against the glass to leave a print and a bit of breath', 20, 'none',
        [k(.12, 'pane_l_low', x=.4, y=.1, b=.1), k(.3, 'pane_l_low', x=1.5, y=.3, b=.5, mark='mmp'), k(.5, 'pane_l_low', x=1.7, y=.4, b=.6, eye='-'), k(.7, x=-.2, y=-.2, b=-.1, eye='O', mark='pop'), k(.86, eye='^')],
        [(.5, 'smudge')], g='use', act=('press', 'pane'), prefer=['curious'])
    # ---------------- play
    o.r('hop_up_on_the_bench', 'Taking a run and a hop onto the bench, then a hop off the far end', 18, 'none',
        [k(.1, 'step_a', perch=1, x=.2, y=.2, b=.3), k(.26, 'bench_front', x=.6, y=.3, b=-.7, l=1, w=.8), k(.44, 'bench_a', perch=1, x=.3, y=-.4, b=-.9, r=1, w=1, mark='hup'), k(.64, 'bench_b', perch=1, x=.4, y=-.2, b=-.5, l=1, w=.7), k(.84, 'thresh', y=.5, b=.8, w=.4), k(.94, eye='^')],
        [], g='play', act=('hop', 'bench'), prefer=['happy', 'young'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('race_the_bench', 'Running a race along the bench top, past every planter, and back', 16, 'none',
        [k(.1, 'bench_a', perch=1, x=.5, y=.1, b=.2, w=.5), k(.3, 'bench_b', perch=1, x=.9, y=.3, b=.6, l=1, w=1, mark='zoom'), k(.5, 'bench_b', perch=1, x=-.4, y=.2, b=.3, r=1, w=.4), k(.7, 'bench_a', perch=1, x=.8, y=.4, b=.7, l=1, w=1), k(.9, 'bench_a', perch=1, y=.2, eye='^')],
        [], g='play', act=('race', 'bench'), prefer=['happy'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('hide_in_the_planters', 'Trying to hide flat among the planter stems, rustling, then bursting out with a roar', 20, 'none',
        [k(.12, 'planter_l2', x=-.2, y=.3), k(.3, 'planter_l2', x=-.9, y=.9, b=.8, eye='O'), k(.52, 'planter_l1', x=-1, y=1, b=1, mark='shh'), k(.7, 'planter_l1', x=1.3, y=-.5, b=-.6, w=1, l=1, r=1, mark='RAWR'), k(.88, eye='^')],
        [(.7, 'shed')], g='play', act=('hide', 'planter'), prefer=['young'])
    o.r('peek_from_pane_to_pane', 'Playing a game of hide and seek from one glass bay to the next', 20, 'none',
        [k(.12, 'pane_l_low', x=.4, y=-.2), k(.28, 'pane_l_low', x=1, y=-.4, b=.3, eye='O'), k(.44, 'rail_l_low', x=-.2, y=.4, b=.5), k(.6, 'pane_r_low', x=1.1, y=-.4, b=.3, eye='>', mark='boo'), k(.78, 'rail_r_low', x=-.3, y=.3, b=.4, eye='^')],
        [], g='play', act=('seek', 'pane'), prefer=['curious'])
    o.r('drum_the_pots', 'Drumming a clay beat on the two small pots with his bill', 18, 'none',
        [k(.12, 'pot_a', x=.9, y=1.1, b=.4, mark='tok'), k(.3, 'pot_b', x=.8, y=1.3, b=-.2, l=1, mark='tonk'), k(.5, 'pot_a', x=1.1, y=1.2, b=.5, r=1, mark='tok tok'), k(.7, 'pot_b', x=.7, y=1.4, b=-.1, l=1, mark='TONK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'pot'), prefer=['happy'], say=["Pots have rhythm. Plants have none.", "Clay on the downbeat. Glass on the chorus."])
    o.r('dig_at_a_planter_foot', 'Digging a quick hole at the planter foot with both feet, soil flying', 20, 'none',
        [k(.12, 'planter_r2', x=.4, y=1, b=.5), k(.3, 'planter_r2', x=.9, y=1.6, b=1, l=1, mark='fff'), k(.5, 'planter_r1', x=1, y=1.8, b=1.1, r=1, mark='fff'), k(.7, 'planter_r2', x=.7, y=1.4, b=.7, l=1, r=1), k(.88, y=.3, w=.6, eye='^')],
        [(.5, 'shed')], g='play', act=('dig', 'planter'), prefer=['happy'])
    # ---------------- test
    o.r('tap_the_glass_for_ring', 'Tapping along the glass from pane to pane to hear which ones ring', 18, 'none',
        [k(.1, 'pane_l_low', x=1.2, y=.2, b=.5, mark='ting'), k(.28, 'rail_l_low', x=.8, y=-.1, b=-.2, l=1, mark='tock'), k(.46, 'pane_l_low', x=.2, y=-.6, b=-.1, w=.8, eye='-'), k(.64, 'pane_r_low', x=1.5, y=.4, b=.8, r=1, mark='tonk'), k(.82, eye='^')],
        [], g='test', act=('tap', 'pane'))
    o.r('count_the_blossoms', 'Touching each flower stem across both sides and counting aloud', 22, 'none',
        [k(.08, 'flower_l1', x=1, y=-.2, b=.2, mark='1'), k(.26, 'flower_l2', x=1.2, y=-.1, b=.1, mark='2'), k(.46, 'flower_r1', x=1.1, y=0, b=.5, l=1, mark='3'), k(.66, 'planter_r1', x=1.3, y=.9, b=.8, r=1, mark='5?'), k(.84, x=-.6, y=-.4, w=.7, eye='-', mark='six')],
        [], g='test', act=('count', 'flower'), prefer=['curious'])
    o.r('measure_up_to_the_bench', 'Stretching up beside the bench to measure how much of him is bench height', 20, 'none',
        [k(.12, 'bench_front', x=-.3, y=.2, b=.2), k(.3, 'bench_front', x=-.5, y=-.9, b=-.6, w=.8, mark='...'), k(.55, 'bench_front', x=.9, y=1.1, b=.8, eye='O'), k(.75, 'bench_front', x=-.2, y=.1, b=.3, l=1, eye='-', mark='short'), k(.9, eye='>')],
        [], g='test', act=('measure', 'bench'), prefer=['young'])
    o.r('taste_a_dropped_petal', 'Picking up a petal with his bill and tasting it with the face of a food critic', 18, 'none',
        [k(.12, 'bench_a', x=.4, y=.7, b=.3), k(.3, 'bench_a', x=1.1, y=.9, b=.4, mark='nm'), k(.5, x=.1, y=.2, eye='-', mark='chew'), k(.68, x=.3, y=.4, b=.2, eye='O'), k(.86, x=-.2, y=.1, eye='-', mark='soap')],
        [], g='test', act=('taste', 'flower'), say=["Tastes like perfume. Tastes like a bad idea.", "Petal. Soap. Lawn. In that order."])
    o.r('weigh_a_pot_with_a_shove', 'Leaning into the small pot to weigh whether it is full of soil', 20, 'none',
        [k(.12, 'pot_a', x=.3, y=.6, b=.3), k(.3, 'pot_a', x=-.5, y=.9, b=.8, mark='hnn'), k(.5, 'planter_r2', x=-.7, y=1, b=1.1, l=1, r=1, mark='hnnf'), k(.7, 'planter_r2', x=-.1, y=.4, b=.4, w=.5, eye='-', mark='full'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'pot'))
    o.r('test_the_glass_for_give', 'Testing the glass for give by leaning his whole chest into the pane', 20, 'none',
        [k(.12, 'pane_r_low', x=.1, y=.3, b=.2), k(.3, 'pane_r_low', x=-.6, y=.7, b=.7, mark='hup'), k(.5, 'pane_r_low', x=-.8, y=.8, b=1, l=1, mark='hnn'), k(.7, 'pane_r_low', x=-.2, y=.3, b=.3, w=.4, eye='-', mark='solid'), k(.88, eye='>')],
        [], g='test', act=('test', 'pane'), obj=[(.5, dict(shake=.1))])
    # ---------------- rest
    o.r('lean_on_the_end_post', 'Leaning on the end post with one foot crossed over the other, in no hurry', 22, 'none',
        [k(.12, 'post_r', x=.4, y=.1, b=.1, r=1), k(.32, 'post_r', x=-.3, y=.7, b=.4, eye='-'), k(.58, 'post_r', x=-.5, y=.8, b=.8, l=1, eye='-', mark='hm'), k(.82, 'post_r', x=-.1, y=.2, b=.2, eye='^')],
        [], g='rest', act=('lean', 'post'))
    o.r('nap_on_the_bench', 'Taking a nap stretched along the bench top among the dropped petals', 30, 'none',
        [k(.15, 'bench_b', perch=1, x=.2, y=.2, b=.4), k(.35, 'bench_b', perch=1, x=.3, y=1, b=1.2, eye='-'), k(.6, 'bench_b', perch=1, x=.2, y=1.2, b=1.4, eye='-', mark='zzz'), k(.85, 'bench_b', perch=1, x=.1, y=.3, b=.5, eye='^')],
        [(.6, 'hush')], g='rest', act=('nap', 'bench'), prefer=['tired'], say=["Bench nap. Petals for a pillow. Posh.", "Slept among the leftovers. Woke up scented."])
    o.r('sit_by_the_pots', 'Sitting on the pot rims with his wings folded, watching the glass fog up', 24, 'none',
        [k(.12, 'pot_a', perch=1, x=.2, y=-.3, b=.1), k(.3, 'pot_a', perch=1, x=-.1, y=.3, b=.7, eye='-'), k(.58, 'pot_b', perch=1, x=-.2, y=.4, b=1.1, eye='-', mark='...'), k(.84, 'pot_b', perch=1, x=.1, y=0, b=.3, r=1, eye='^')],
        [], g='rest', act=('sit', 'pot'))
    o.r('warm_up_on_the_sunny_glass', 'Warming his back against the sun-heated glass until his feathers steam', 24, 'none',
        [k(.12, 'pane_l_low', x=.3, y=.3, b=.2), k(.3, 'pane_l_low', x=-.5, y=.6, b=.6, eye='-'), k(.55, 'pane_l_low', x=-.7, y=.7, b=.9, eye='-', mark='ahh'), k(.8, 'pane_l_low', x=-.2, y=.3, b=.4, l=1, eye='^')],
        [(.55, 'soak')], g='rest', act=('warm', 'pane'), when=['warmth>.3', 'sun'], say=["Glass hot as a pan. I am a very happy egg.", "Steam rising off my back. Bliss, with side effects."])
    o.r('perch_on_the_planter_edge', 'Perching on the planter edge to look at the flowers at eye level', 22, 'none',
        [k(.14, 'planter_l1', perch=1, x=.1, y=-.3, b=-.2, w=.4), k(.36, 'planter_l1', perch=1, x=.8, y=-.5, b=.2, eye='O'), k(.62, 'planter_l2', perch=1, x=-.4, y=-.4, b=.4, w=.3, mark='hm'), k(.86, 'planter_l2', perch=1, x=.2, y=-.1, eye='-')],
        [], g='rest', act=('perch', 'planter'), prefer=['curious'])
    o.r('guard_the_glass_door', 'Standing guard on the line before the glass door, wings tight', 24, 'none',
        [k(.12, 'thresh', perch=1, x=.2, y=-.2, b=.1, l=1), k(.34, 'thresh', perch=1, x=.8, y=-.8, b=-.5, w=.6, eye='>'), k(.58, 'thresh', perch=1, x=-.6, y=-.5, b=-.1, r=1, w=.2, mark='halt'), k(.86, 'thresh', perch=1, x=.2, y=.1, b=.2, w=.5, eye='-')],
        [], g='rest', act=('guard', 'door'), prefer=['lonely'])
    # ---------------- weather
    o.r('chip_frost_off_the_pane', 'Chipping the frost off the lowest pane with the edge of his bill', 18, 'none',
        [k(.1, 'pane_r_low', x=.8, y=.7, b=.5, l=1), k(.28, 'pane_r_low', x=1.4, y=.9, b=.9, mark='tk'), k(.46, 'rail_r_low', x=1.5, y=.5, b=.7, r=1, mark='tk'), k(.68, 'pane_r_low', x=.6, y=.6, b=.4), k(.86, x=-.2, w=.4, eye='^')],
        [(.46, 'chip')], g='weather', act=('chip', 'pane'), when=['frost>.3'], say=["Frost off the glass. Now the plants can see me.", "Chipped a window. Window is thrilled."])
    o.r('blow_on_the_frozen_rail', 'Blowing warm breath along the frozen glazing rail until it drips', 18, 'none',
        [k(.12, 'rail_l_low', x=.5, y=.1), k(.3, 'rail_l_low', x=1, y=-.3, b=.3, mark='haah'), k(.5, 'rail_l', x=1.1, y=-.4, b=.2, w=.3, mark='haaah'), k(.72, 'rail_l_low', x=.7, y=-.1, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'rail'), when=['frost>.3'])
    o.r('shake_off_the_glass_drips', 'Shaking the roof drips off his back with the end post at his shoulder', 18, 'none',
        [k(.12, 'post_l', x=.2, y=.3, b=.2), k(.3, 'post_l', x=-.2, y=.7, b=.6, w=1, mark='brrr'), k(.5, 'post_l', x=.2, y=.7, b=.8, w=1, r=1), k(.7, 'post_l', x=-.2, y=.5, b=.5, w=1, l=1), k(.88, eye='^')],
        [(.5, 'spray')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    o.r('dry_the_dripping_pane', 'Wiping the condensation drips off the glass edge with a dry wing', 18, 'wing',
        [k(.12, 'pane_l_low', reach=.4, x=.1, y=.4, b=.2), k(.3, 'pane_l_low', reach=1, x=.5, y=.7, b=.5, l=1, mark='squk'), k(.5, 'rail_l_low', reach=1, x=.7, y=.5, b=.4, r=1, mark='squk'), k(.7, 'pane_l_low', reach=.7, x=.3, y=.6, b=.3), k(.88, eye='-')],
        [(.5, 'flick')], g='weather', act=('dry', 'pane'), when=['obj_wetness>.3'])
    o.r('cool_off_on_the_bench', 'Trying to cool off against the shaded bench front, fanning himself with both wings', 22, 'none',
        [k(.12, 'bench_front', x=.2, y=.4, b=.4), k(.3, 'bench_front', x=-.2, y=.9, b=.8, w=1, mark='puff'), k(.52, 'bench_front', x=-.3, y=1, b=1, w=.6, l=1, r=1, mark='fff'), k(.74, 'bench_front', x=-.1, y=.6, b=.5, w=1), k(.9, eye='^')],
        [(.52, 'fan')], g='weather', act=('cool', 'bench'), when=['warmth>.6', 'sun'], say=["Greenhouse in summer is a kettle with windows.", "Fanned myself. Plants are fine. I am a ham."])
    o.r('shelter_among_the_planters', 'Pressing between the planters to shelter from the rain drumming on the glass roof', 34, 'none',
        [k(.1, 'planter_r1', x=.2, y=.1, b=.1, r=1), k(.3, 'planter_r2', x=-.9, y=.7, b=.8, w=.6, eye='-', mark='drum'), k(.55, 'planter_r1', x=-1, y=1.1, b=1.2, w=.6, l=1, eye='>', mark='drum drum'), k(.8, 'planter_r2', x=-.2, y=.2, b=.3, w=1, eye='^')],
        [], g='weather', act=('shelter', 'planter'), when=['wet', 'storm'], say=["Rain on glass. Duck in flowers. Cinema.", "Roof leaks sound. I leak nothing. Winning."])
    # ---------------- mishap
    o.r('walk_into_the_clear_glass', 'Walking straight at the glass wall, thinking it was open air, and meeting it', 16, 'none',
        [k(.12, x=.1, y=-.1, b=-.2), k(.3, x=.8, y=-.6, b=.4, l=1, w=.5), k(.5, 'pane_l_low', x=2, y=.1, b=1.2, eye='@', mark='DUNK'), k(.72, x=-1.2, y=.8, b=.1, r=1, w=.8, eye='O'), k(.9, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'pane'), say=["Glass. Invisible. Bastard.", "Greenhouse is mostly door-shaped lies."])
    o.r('slip_on_the_wet_step', 'Slipping off the wet door step with his feet racing ahead of the rest of him', 14, 'none',
        [k(.15, 'step_a', perch=1, y=.2, b=.2), k(.3, 'step_a', perch=1, x=.6, y=.5, b=-.3, l=1, w=.7, eye='O'), k(.5, 'thresh', x=-.6, y=1, b=1, r=1, w=1, mark='WHOA'), k(.7, 'thresh', y=1.4, b=1.4, eye='@', mark='*splat*'), k(.88, y=.4, b=.4, eye='-')],
        [(.5, 'spray')], g='mishap', act=('slip', 'step'), when=['wet', 'obj_wetness>.3'], say=["Step was a lake. Dignity was a duck.", "Feet left first. Rest followed, sulking."])
    o.r('snap_a_stem_with_a_wing', 'Catching a wingtip on a flower stem and snapping the blossom off by mistake', 18, 'wing',
        [k(.14, 'flower_l2', reach=.5, x=.3, y=-.3), k(.34, 'flower_l2', reach=1, x=-.4, y=-.4, b=.5, eye='O'), k(.54, 'flower_l2', reach=.6, x=.5, y=-.2, b=.8, l=1, r=1, mark='SNAP'), k(.74, y=.8, b=.9, eye='@'), k(.9, eye='-')],
        [(.54, 'snap')], g='mishap', act=('catch', 'flower'), ages=GROWN, say=["Snapped one. Blamed the stem. The stem knows.", "Flower down. Wing innocent. Alibi pending."])
    o.r('kick_the_pot_by_accident', 'Kicking the small pot by accident and hopping about on one foot', 16, 'none',
        [k(.15, 'pot_a', x=.3, y=.6, b=.3), k(.32, 'pot_a', x=.7, y=.8, b=-.4, l=1, w=.5), k(.5, 'pot_a', x=1.2, y=1.3, b=.9, r=1, eye='@', mark='CLONK'), k(.7, x=-.3, y=.6, b=-.6, l=1, eye='O', mark='ow ow'), k(.88, y=.3, eye='-')],
        [(.5, 'crack')], g='mishap', act=('kick', 'pot'), say=["Pot unharmed. Foot is a rumour now.", "Kicked clay. Clay won. Standard."])
    o.r('peck_the_glass_too_hard', 'Pecking the glass so hard it rings and a hairline crack shows', 16, 'none',
        [k(.15, 'pane_r_low', x=.5, y=.2, b=.2), k(.3, 'pane_r_low', x=1.4, y=.5, b=.8, mark='tak'), k(.48, 'pane_r_low', x=1.7, y=.7, b=1, eye='@', mark='CRK'), k(.7, x=-.5, y=.3, w=.7, eye='O'), k(.88, eye='-')],
        [(.48, 'crack')], g='mishap', act=('peck', 'pane'), prefer=['grumpy'], say=["Cracked it. Slightly. Quietly. Moving on.", "Hairline crack. Glass will outlive the embarrassment."])
    # ---------------- show
    o.r('bow_to_the_blossoms', 'Bowing slowly to the flowers on both sides as if they had applauded', 20, 'none',
        [k(.14, 'planter_l2', y=.1), k(.34, 'planter_l2', x=.3, y=1.3, b=1, w=.5, eye='-'), k(.54, 'planter_r1', x=.4, y=1.6, b=1.2, w=.8, mark='thank you'), k(.78, 'planter_r1', y=.1, w=.3, eye='^')],
        [], g='show', act=('bow', 'flower'), prefer=['happy'])
    o.r('sing_to_the_planters', 'Singing a lullaby to the planters, one flower at a time', 22, 'none',
        [k(.14, 'planter_r2', x=.2, y=-.3), k(.34, 'planter_r1', x=-.2, y=-.9, b=.7, w=.8, mark='laa'), k(.58, 'planter_l1', x=1.1, y=-1, b=-.4, w=1, r=1, eye='^', mark='LAAA'), k(.84, 'planter_l1', x=-.1, y=-.3, eye='-')],
        [], g='show', act=('sing', 'planter'), prefer=['happy'])
    o.r('dance_across_the_bench', 'Dancing a jig along the bench top, hopping off the end with a twirl of his wings', 20, 'none',
        [k(.12, 'bench_a', perch=1, y=-.3, b=-.6, l=1, w=.6), k(.3, 'bench_a', perch=1, x=.4, y=.4, b=.5, r=1, w=1), k(.5, 'bench_b', perch=1, y=-.5, b=-.9, l=1, w=1, mark='tada'), k(.7, 'step_a', perch=1, x=.3, y=.3, b=.6, r=1, w=.8), k(.88, 'thresh', eye='^')],
        [], g='show', act=('dance', 'bench'), prefer=['happy'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('show_off_the_glass_house', 'Showing off the whole glass house with a sweeping wing like a very small estate agent', 20, 'wing',
        [k(.1, 'post_l', reach=.3, x=-.5, y=.3, b=.3, l=1), k(.28, 'rail_l_low', reach=1, x=.3, y=-1.1, b=-.7, mark='behold'), k(.48, 'door_panel', reach=.9, x=.8, y=-.3, b=.4, r=1), k(.68, 'rail_r_low', reach=1, x=.5, y=-1.0, b=-.8, l=1, mark='sunny'), k(.86, x=-.4, y=.1, w=.3, eye='^')],
        [], g='show', act=('show', 'house'), say=["Cosy. Bright. Slightly damp. Price on request.", "Full of plants. No ducks. Gap in the market."])
    o.r('hook_a_flower_down_with_a_twig', 'Hooking a high flower stem down with a twig to get his nose into it', 22, 'twig',
        [k(.14, 'flower_r1', reach=.5, x=.2, y=-.5), k(.32, 'flower_r1', reach=1, x=.6, y=-.8, b=-.3, mark='tk'), k(.52, 'flower_r1', reach=1, x=-.2, y=-.4, b=.3, w=.3, mark='nnf'), k(.72, 'flower_r1', reach=.6, x=.8, y=-.2, b=.4, eye='-', mark='sniff'), k(.9, eye='^')],
        [(.52, 'shower')], g='use', act=('hook', 'flower'), say=["Got the stem. Got the flower. Got a petal shower.", "Twig did the reaching. Nose did the bad decisions."])
    o.r('balance_on_the_glazing_rail', 'Balancing along the low glazing rail with his wings out, one careful foot at a time', 20, 'none',
        [k(.12, 'rail_l_low', perch=1, x=.2, y=-.1, w=.5, l=1), k(.3, 'rail_l_low', perch=1, x=.6, y=.2, b=.4, w=1, r=1), k(.52, 'rail_l_low', perch=1, x=-.3, y=-.3, b=.8, w=1, l=1, mark='eep'), k(.74, 'rail_l_low', perch=1, x=.5, y=.3, b=.3, w=.8), k(.9, eye='^')],
        [], g='play', act=('balance', 'rail'), prefer=['happy'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('wipe_a_smiley_in_the_mist', 'Using a wingtip to wipe a smiley into the misted right pane', 18, 'wing',
        [k(.1, 'pane_r_hi', reach=.4, x=.1, y=-.3, b=-.3), k(.26, 'pane_r_hi', reach=1, x=.5, y=-.6, b=-.4, r=1, mark='sq'), k(.42, 'pane_r_hi', reach=1, x=.2, y=-.4, b=-.6, l=1, mark='sq'), k(.6, 'pane_r_hi', reach=1, x=.8, y=-.8, b=-.5, r=1, mark='squeee'), k(.78, reach=.2, y=-.2, w=.4, eye='^')],
        [(.6, 'clear')], g='play', act=('wipe', 'smiley'), when=['mist>.3'], ages=GROWN, prefer=['happy'], say=["Drew a face. It looks like the landlord.", "Smiley on the glass. The plants look unconvinced."])
    o.emit()
    return o


def mud_hut():
    P = pm('mud_hut')
    o = Obj('mud_hut', 'placed',
            parts=dict(wall='the clay walls left and right of the door, a ~._ texture and a thick base line', window='the two small windows high in the clay (cross mullion, glints)',
                       sill='the ledge line under each window, 47 px up', reed='the bundle of five reeds with feathery heads, leaning at the left and tied with a band',
                       tie='the band round the reeds', pot='the two small pots at the right foot, one rounded, one with a lid', door='the low door leaf with two raised panels',
                       crate='the little .---| box shape at the foot of the door', lip='the door foot strip, 19 px up', step='the lower door-frame line, 9 px up',
                       thresh='the standing line in front of the door', eave='the thatch eave beam above the walls, 160 px up', roof='the thatched roof, out of reach'),
            fields=dict(splatter=(0, 0, 1), frost=(0, 0, 1), warmth=(0, 0, 1), loose=(0, 0, 1)),
            physics=[('splatter', 'rate', .003, 'wet'), ('splatter', 'rate', -.0004, 'dry'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('warmth', 'rate', .0007, 'sun'), ('warmth', 'rate', -.0004, 'night')],
            effects=dict(scrape=[('splatter', 'mul', .2)], rub=[('splatter', 'mul', .4)], wipe=[('obj.dirt', 'add', -.2)], sweep=[('obj.dirt', 'add', -.15)], scrub=[('obj.dirt', 'add', -.3)],
                         dry=[('obj.wetness', 'add', -.3)], shake=[('obj.wetness', 'add', .15)], press=[('obj.condition', 'add', .2)], crumble=[('obj.condition', 'add', -.15)],
                         scuff=[('obj.dirt', 'add', .12)], chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)],                          tie=[('loose', 'set', 0)], tug=[('loose', 'add', .35)], rustle=[('loose', 'add', .3)], soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)],
                         cool=[('warmth', 'add', -.3), ('need.fun', 'add', 1)], laugh=[('need.fun', 'add', 2)], hush=[('need.energy', 'add', 1)], splash=[('splatter', 'add', .3)]),
            marks=[('splatter', .3, "'. ' .'", 'wall_l', 'mud'), ('splatter', .3, ". '. '", 'wall_r', 'mud'), ('frost', .3, '*.*.*', 'sill_l', 'frost'), ('frost', .3, '*.*.*', 'sill_r', 'frost'),
                   ('loose', .3, '\\ | /', 'reed_mid', 'plant')],
            anchors=dict(wall_l=P(21, 41), wall_r=P(60, 41), window_l=P(19, 36), window_r=P(63, 36), sill_l=P(17, 39, 'surface'), sill_r=P(62, 39, 'surface'),
                         reed_tie=P(11, 39), reed_mid=P(13, 35), reed_foot=P(12, 42), pot_a=P(64, 43, 'surface'), pot_b=P(68, 44, 'surface'), door_panel_l=P(36, 38),
                         door_panel_u=P(36, 33), crate=P(46, 40), lip_a=P(35, 42, 'surface'), lip_b=P(46, 42, 'surface'), step_a=P(38, 43, 'surface'), step_b=P(44, 43, 'surface'),
                         thresh=P(41, 44, 'surface'), eave=P(40, 27)))
    # ---------------- care
    o.r('scrub_the_clay_pots', 'Scrubbing both clay pots with a wing until the colour comes back', 20, 'wing',
        [k(.1, 'pot_a', reach=.5, x=.2, y=.9, b=.4), k(.26, 'pot_a', reach=1, x=.6, y=1.2, b=.9, r=1, mark='skrk'), k(.44, 'pot_b', reach=1, x=.8, y=1.4, b=.7, l=1, mark='skrk'), k(.62, 'pot_b', reach=1, x=1, y=1.5, b=1.1, r=1), k(.82, 'pot_a', reach=.5, x=.3, y=.8, b=.4), k(.94, eye='^')],
        [(.62, 'scrub')], g='care', act=('scrub', 'pot'), when=['obj_dirt>.3'], say=["Pots clean. Hands, wings, feet: filthy.", "Rubbed the clay till it blushed."])
    o.r('wipe_the_little_window', 'Reaching up with a wing to wipe the clay smears off the left window', 20, 'wing',
        [k(.1, 'sill_l', reach=.5, x=.1, y=-.1, b=.2, l=1), k(.28, 'window_l', reach=1, x=.5, y=-.4, b=-.3, mark='squk'), k(.46, 'window_l', reach=1, x=.9, y=-.5, b=-.5, r=1, mark='squk'), k(.64, 'window_l', reach=.7, x=.3, y=-.3, b=-.2), k(.8, reach=.2, y=-.1, w=.4, eye='O'), k(.92, eye='^')],
        [(.46, 'wipe')], g='care', act=('wipe', 'window'), when=['obj_dirt>.3'])
    o.r('sweep_the_doorstep', 'Sweeping the grit off the doorstep and the foot strip with a wing', 18, 'wing',
        [k(.1, 'step_b', reach=.4, x=.2, y=.8, b=.2, r=1), k(.28, 'step_b', reach=1, x=.6, y=1.1, b=.6, l=1, mark='shff'), k(.48, 'lip_b', reach=1, x=.9, y=1, b=.5, r=1), k(.68, 'step_a', reach=1, x=.5, y=1.2, b=.4, l=1, mark='shff'), k(.86, eye='-')],
        [(.48, 'sweep')], g='care', act=('sweep', 'step'), when=['obj_dirt>.3'])
    o.r('dry_the_window_sill', 'Dragging his breast along the sill line to dry the rain off the clay', 20, 'none',
        [k(.12, 'sill_r', x=.5, y=-.2, b=.2), k(.3, 'sill_r', x=1, y=-.1, b=.6, mark='fsh'), k(.5, 'sill_r', x=1.2, y=0, b=.8, l=1, mark='fsh'), k(.7, 'wall_r', x=.7, y=.3, b=.4, r=1), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'sill'), when=['obj_wetness>.3'])
    o.r('press_the_crumbling_clay', 'Mending a crumbling patch of the wall by pressing it flat with his breast', 18, 'none',
        [k(.1, 'wall_l', x=.4, y=.6, b=.3), k(.26, 'wall_l', x=-.8, y=.8, b=.8, mark='nnf'), k(.44, 'wall_l', x=-1, y=.9, b=1, l=1, r=1, mark='nnnf'), k(.62, 'wall_l', x=-1.1, y=1, b=1.2, w=.4, mark='PAT'), k(.8, x=.1, y=.4, b=.2), k(.92, eye='^')],
        [(.62, 'press')], g='care', act=('mend', 'wall'), when=['obj_condition<.6'], say=["Clay patched. Hut is back in business.", "Smooth as a pebble. Smug as a duck."])
    o.r('tie_a_stray_reed_back', 'Tucking a stray reed back in and trying to tie the band tight again', 20, 'none',
        [k(.1, 'reed_mid', x=.5, y=-.2), k(.26, 'reed_mid', x=1.1, y=-.4, b=.3, mark='nnf'), k(.44, 'reed_tie', x=1.2, y=.2, b=.6, l=1), k(.62, 'reed_tie', x=1.4, y=.4, b=.8, r=1, mark='tight'), k(.82, x=-.2, y=0, eye='^')],
        [(.62, 'tie')], g='care', act=('tie', 'reeds'), when=['loose>.3'], say=["Reed tied. Bundle looks organised. Fraud.", "Stuffed it back in. Reeds hate me now."])
    o.r('scrape_the_mud_splatter', 'Scraping the splattered mud off the foot of the wall with the edge of his bill', 20, 'none',
        [k(.1, 'wall_r', x=.7, y=1.1, b=.6, l=1), k(.28, 'wall_r', x=1.4, y=1.5, b=.9, mark='skrk'), k(.46, 'wall_l', x=1.5, y=1.6, b=1, r=1, mark='skrk'), k(.66, 'wall_l', x=.8, y=1.2, b=.6, l=1), k(.86, x=-.1, w=.4, eye='^')],
        [(.46, 'scrape')], g='care', act=('scrape', 'wall'), when=['splatter>.3'], say=["Mud off the wall. Mud on my bill. Cycle of life.", "Scraped it clean. Next rain will undo the work."])
    # ---------------- use
    o.r('push_the_low_door', 'Pushing a shoulder against the low door to check it is not stuck', 18, 'none',
        [k(.12, 'door_panel_l', x=.2, y=.3, b=.1), k(.3, 'door_panel_l', x=-.7, y=.8, b=.7, mark='hup'), k(.5, 'door_panel_l', x=-.8, y=.9, b=1, l=1, mark='hnn'), k(.72, 'door_panel_l', x=-.3, y=.4, b=.3, r=1), k(.88, x=.2, y=.5, eye='-')],
        [], g='use', act=('push', 'door'), obj=[(.5, dict(shake=.1))])
    o.r('knock_on_the_door_panel', 'Knocking on the upper door panel and listening for a very small resident', 20, 'none',
        [k(.12, 'door_panel_u', x=.5, y=-.4, b=-.2), k(.28, 'door_panel_u', x=1.2, y=-.5, b=-.1, mark='tok'), k(.44, 'door_panel_u', x=.2, y=-.3, b=-.4, w=.4), k(.6, 'door_panel_u', x=1.3, y=-.5, b=-.1, mark='tok tok'), k(.78, x=-.5, y=-.6, b=-.3, w=.7, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'door'), say=["Knocked. Hut stayed small and silent.", "No answer. Lucky for them, I brought opinions."])
    o.r('pull_a_reed_loose', 'Pulling a long reed half out of the bundle to hear it whistle', 18, 'none',
        [k(.12, 'reed_mid', x=.4, y=-.3), k(.3, 'reed_mid', x=1, y=-.6, b=.4, mark='mmf'), k(.5, 'reed_mid', x=-.6, y=-.4, b=-.5, w=.5, mark='fwoot'), k(.7, x=.3, y=.8, b=.4), k(.88, eye='^')],
        [(.5, 'tug')], g='use', act=('pull', 'reeds'), say=["Reed whistled. Reed also fell out. Same noise.", "Pulled one. The rest got ideas."])
    o.r('sniff_the_pots', 'Sniffing into each pot for whatever the hut keeps in them', 20, 'none',
        [k(.12, 'pot_a', x=.5, y=1, b=.5), k(.3, 'pot_a', x=1.2, y=1.3, b=.7, eye='O', mark='sniff'), k(.5, 'pot_b', x=1.3, y=1.4, b=.8, mark='sniff'), k(.7, 'pot_b', x=.5, y=.7, b=.3, eye='-', mark='dust'), k(.88, eye='>')],
        [], g='use', act=('sniff', 'pot'), prefer=['curious'])
    o.r('peer_at_the_right_window', 'Craning up to peer at the right window for whoever lives here', 20, 'none',
        [k(.12, 'sill_r', x=.3, y=-.2, b=-.2), k(.32, 'window_r', x=1.1, y=-.8, b=-.6, w=.4, eye='O'), k(.56, 'window_r', x=1.3, y=-.9, b=-.7, l=1, mark='...'), k(.78, x=-.3, y=-.3, b=-.1, eye='-'), k(.9, eye='>')],
        [], g='use', act=('peer', 'window'), prefer=['curious'])
    o.r('shout_up_at_the_thatch', 'Cupping a wing and shouting up at the thatch for the mice he hopes live there', 18, 'none',
        [k(.15, x=-.1, y=-.8, b=-.1), k(.35, x=-.6, y=-1.3, b=-.6, w=.6, mark='OI'), k(.58, x=-.8, y=-1.5, b=-.7, w=.9, l=1, mark='OIIII'), k(.8, x=-.2, y=-.5, b=-.2, eye='-')],
        [(.58, 'laugh')], g='use', act=('shout', 'roof'), far=True, say=["Shouted at the thatch. Thatch rustled. Mice, or sarcasm.", "Roof said nothing. Roof has a good poker face."])
    # ---------------- play
    o.r('hide_among_the_reeds', 'Trying to hide flat in the reeds, rustling, then bursting out with a roar', 20, 'none',
        [k(.12, 'reed_foot', x=-.3, y=.3), k(.3, 'reed_foot', x=-1, y=.8, b=.8, eye='O'), k(.5, 'reed_tie', x=-1.1, y=.9, b=1, mark='shh'), k(.68, 'reed_tie', x=1.2, y=-.6, b=-.6, w=1, l=1, r=1, mark='RAH'), k(.88, eye='^')],
        [(.68, 'rustle')], g='play', act=('hide', 'reeds'), prefer=['young'])
    o.r('hop_up_on_the_sill', 'Taking a hop up on the sill line, a wobble, and a hop off again', 18, 'none',
        [k(.12, 'wall_l', x=.3, y=.2, b=.3), k(.28, 'sill_l', perch=1, x=.3, y=-.5, b=-.8, l=1, w=.9, mark='hup'), k(.48, 'sill_l', perch=1, x=.8, y=-.2, b=.3, r=1, w=.5, mark='eep'), k(.7, 'wall_l', x=.4, y=.4, b=.6, w=.3), k(.88, eye='^')],
        [], g='play', act=('hop', 'sill'), prefer=['happy', 'young'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('race_round_the_pots', 'Running a race round the two pots and back to the door', 16, 'none',
        [k(.08, 'lip_b', perch=1, x=-.3, y=.3, b=.4, w=.2), k(.28, 'pot_a', x=1.3, y=.9, b=-.4, l=1, w=1, mark='zoom'), k(.46, 'pot_b', x=-.2, y=.1, b=.9, r=1, w=.6), k(.66, 'pot_a', x=1.1, y=.8, b=-.3, l=1, r=1, w=1), k(.88, 'lip_b', perch=1, x=.2, y=-.1, eye='^')],
        [], g='play', act=('race', 'pot'), prefer=['happy'])
    o.r('balance_on_the_foot_strip', 'Balancing along the foot strip of the door with his wings out', 18, 'none',
        [k(.12, 'lip_a', perch=1, x=-.2, y=-.3, w=.6, r=1), k(.34, 'lip_a', perch=1, x=.5, y=.2, b=.5, l=1, w=1), k(.58, 'lip_b', perch=1, x=.8, b=.7, r=1, w=1, mark='whoa'), k(.8, 'lip_b', perch=1, x=.1, y=.3, b=.2, w=.7), k(.92, eye='^')],
        [], g='play', act=('balance', 'lip'))
    o.r('drum_a_tune_on_the_clay', 'Drumming a tune on the wall and the lid of the pot with his bill', 18, 'none',
        [k(.12, 'wall_r', x=.9, y=.9, b=.2, mark='tom'), k(.3, 'pot_b', x=.8, y=1.2, b=-.2, l=1, mark='tonk'), k(.5, 'wall_r', x=1.1, y=1, b=.3, r=1, mark='tom tom'), k(.7, 'pot_b', x=.7, y=1.3, b=-.1, l=1, mark='TONK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'wall'), prefer=['happy'], say=["Clay has the deepest voice here. Dull, but deep.", "Wall on the verse, pot on the chorus."])
    o.r('dig_along_the_wall_foot', 'Digging a trench along the foot of the wall with both feet, clay flying', 20, 'none',
        [k(.1, 'thresh', x=.2, y=1.4, b=.9), k(.3, 'wall_r', x=1.2, y=.9, b=1.4, l=1, mark='fff'), k(.5, 'thresh', x=.6, y=1.5, b=1.2, r=1, mark='fff'), k(.7, 'wall_r', x=1.4, y=1.1, b=.6, l=1, r=1), k(.88, y=.3, w=.9, eye='^')],
        [(.5, 'splash')], g='play', act=('dig', 'wall'), prefer=['happy'])
    # ---------------- test
    o.r('tap_the_wall_for_hollow', 'Tapping the clay wall from the foot up to hear where it is thin', 18, 'none',
        [k(.1, 'wall_l', x=1.3, y=1, b=.7, mark='tok'), k(.26, 'window_l', x=.8, y=-.4, b=-.4, l=1, mark='tok'), k(.44, 'wall_l', x=.2, y=-.7, b=-.1, w=.8, eye='-'), k(.62, 'wall_l', x=1.6, y=1.2, b=.9, r=1, mark='tonk'), k(.8, eye='^')],
        [], g='test', act=('tap', 'wall'))
    o.r('count_the_reeds', 'Touching each reed in the bundle and counting aloud', 22, 'none',
        [k(.08, 'reed_foot', x=1.1, y=.7, b=.5, mark='1'), k(.26, 'reed_mid', x=1.3, y=-.2, b=.2, r=1, mark='2'), k(.46, 'reed_tie', x=.9, y=.1, b=.9, l=1, mark='3'), k(.66, 'reed_mid', x=1.4, y=-.5, b=.3, r=1, mark='4?'), k(.84, x=-.7, y=-.5, w=.7, eye='-', mark='five')],
        [], g='test', act=('count', 'reeds'), prefer=['curious'])
    o.r('weigh_the_lidded_pot', 'Leaning into the lidded pot to weigh what is inside', 20, 'none',
        [k(.1, 'pot_b', x=.7, y=.4, b=.1, l=1), k(.3, 'pot_b', x=-.9, y=.6, b=1.1, mark='hnn'), k(.5, 'crate', x=-.4, y=1.3, b=.6, r=1, mark='hnnf'), k(.7, 'pot_b', x=.1, y=.3, b=.8, w=.7, eye='-', mark='heavy'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'pot'))
    o.r('taste_the_clay_wall', 'Licking the clay wall to taste what the hut is made of', 18, 'none',
        [k(.12, 'wall_r', x=.5, y=.4, b=.2), k(.3, 'wall_r', x=1.2, y=.6, b=.3, mark='lk'), k(.5, x=.1, y=.2, eye='O', mark='bleh'), k(.68, x=-.2, y=.6, b=.3, eye='-', mark='salty'), k(.86, eye='>')],
        [], g='test', act=('taste', 'wall'), say=["Tastes of dirt. Hut is made of dirt. Consistent.", "Wall tastes of nothing and low expectations."])
    o.r('prod_the_thatch_eave', 'Prodding the thatch eave with a twig to see what is nesting up there', 22, 'twig',
        [k(.14, 'eave', reach=.6, x=.3, y=-.7, b=-.3), k(.32, 'eave', reach=1, x=.6, y=-1.1, b=-.5, mark='tk'), k(.52, 'eave', reach=1, x=-.1, y=-1.2, b=-.6, w=.3, mark='rustle'), k(.72, 'eave', reach=.6, x=.5, y=-.8, b=-.3), k(.9, x=-.3, y=-.2, eye='-')],
        [], g='test', act=('prod', 'eave'), ages=GROWN)
    # ---------------- rest
    o.r('lean_on_the_warm_clay', 'Leaning his back against the sun-warmed clay wall and soaking it up', 24, 'none',
        [k(.1, 'wall_r', x=.5, y=.1, b=.1, l=1), k(.3, 'wall_r', x=-.8, y=.5, b=.3, eye='-'), k(.55, 'wall_r', x=-1.1, y=.6, b=.9, eye='-', mark='ahh'), k(.8, 'wall_r', x=-.5, y=.2, b=.6, r=1, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'wall'), when=['warmth>.3', 'sun'], say=["Clay holds the sun all day. Wise old mud.", "Warm back, cold opinions. Perfect."])
    o.r('sit_on_the_hut_step', 'Sitting on the doorstep with his feet tucked and his chin down', 24, 'none',
        [k(.12, 'step_b', perch=1, x=.2, y=-.3, b=.2, r=1), k(.3, 'step_b', perch=1, x=-.2, y=.3, b=.7, eye='-'), k(.6, 'step_b', perch=1, x=-.3, y=.4, b=1.2, eye='-', mark='...'), k(.85, 'step_b', perch=1, x=.1, y=-.1, b=.3, l=1, eye='^')],
        [], g='rest', act=('sit', 'step'))
    o.r('nap_on_the_sill', 'Taking a nap on the sill line with his head tucked in a wing', 30, 'none',
        [k(.15, 'sill_r', perch=1, x=.4, y=.4, b=.7, l=1), k(.35, 'sill_r', perch=1, x=-.2, y=1.2, b=.9, eye='-'), k(.6, 'sill_r', perch=1, x=-.3, y=1.4, b=1.6, eye='-', mark='zzz'), k(.85, 'sill_r', perch=1, x=.3, y=.1, b=.2, r=1, eye='^')],
        [(.6, 'hush')], g='rest', act=('nap', 'sill'), prefer=['tired'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'], say=["Sill nap. Thatch overhead. Zero stress.", "Slept on a ledge. Dreamt of bigger ledges."])
    o.r('perch_on_the_pot_lid', 'Perching on the rim of the round pot like a very small lord', 22, 'none',
        [k(.12, 'pot_a', perch=1, x=.6, y=-.1, b=.3, w=.2, l=1), k(.36, 'pot_a', perch=1, x=-.1, y=-.9, b=-.3, eye='O', w=.7), k(.62, 'pot_a', perch=1, x=-.9, y=-.1, b=.6, w=.1, mark='hm'), k(.86, 'pot_a', perch=1, x=.4, y=-.3, b=0, r=1, eye='-')],
        [], g='rest', act=('perch', 'pot'), prefer=['curious'])
    o.r('guard_the_low_door', 'Standing guard on the line before the low door, chin up', 24, 'none',
        [k(.12, 'thresh', perch=1, x=.3, y=-.2, b=.2, l=1), k(.34, 'thresh', perch=1, x=1.1, y=-.7, b=-.5, w=.7, eye='>'), k(.58, 'thresh', perch=1, x=-.4, y=-.8, b=-.1, r=1, w=.2, mark='halt'), k(.86, 'thresh', perch=1, x=.2, y=.1, b=.1, w=.5, eye='-')],
        [], g='rest', act=('guard', 'door'), prefer=['lonely'])
    o.r('lean_on_the_reed_bundle', 'Leaning into the reed bundle like a very prickly armchair', 22, 'none',
        [k(.12, 'reed_foot', x=.4, y=.2, b=.2), k(.34, 'reed_tie', x=-.6, y=.5, b=.6, r=1, eye='-'), k(.6, 'reed_tie', x=-.8, y=.6, b=1, eye='-', mark='ouch'), k(.84, 'reed_foot', x=-.2, y=.2, b=.3, l=1, eye='>')],
        [], g='rest', act=('lean', 'reeds'), prefer=['grumpy'])
    # ---------------- weather
    o.r('chip_frost_off_the_sill', 'Chipping the frost off the sill line with the edge of his bill', 18, 'none',
        [k(.1, 'sill_l', x=.9, y=.1, b=.5, l=1), k(.28, 'sill_l', x=1.5, y=.3, b=.9, mark='tk'), k(.48, 'sill_r', x=1.6, y=.4, b=1, r=1, mark='tk'), k(.7, 'sill_r', x=.7, y=.2, b=.5), k(.88, x=-.2, w=.4, eye='^')],
        [(.48, 'chip')], g='weather', act=('chip', 'sill'), when=['frost>.3'], say=["Frost off the sill. Hut looks relieved.", "Chip, chip. Cold in the nostrils."])
    o.r('blow_on_the_frosted_glass', 'Blowing warm breath at the frosted left window until it clears', 18, 'none',
        [k(.1, 'window_l', x=.2, y=-.5, b=-.4, r=1), k(.3, 'window_l', x=1.3, y=-.7, b=.1, mark='haah'), k(.5, 'window_l', x=.9, y=-.3, b=-.1, w=.6, l=1, mark='haaah'), k(.72, 'window_l', x=1.4, y=-.9, b=.2, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'window'), when=['frost>.3'])
    o.r('shake_the_rain_off', 'Shaking the rain off his back beside the wall, spraying the clay', 18, 'none',
        [k(.12, 'wall_l', x=.1, y=.3, b=.1), k(.3, 'wall_l', x=-.3, y=.6, b=.5, w=1, mark='brrr'), k(.5, 'wall_l', x=.3, y=.8, b=.9, w=1, r=1), k(.7, 'wall_l', x=-.3, y=.4, b=.4, w=1, l=1), k(.88, eye='^')],
        [(.5, 'shake')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    o.r('cool_off_against_the_wall', 'Trying to cool off against the shaded clay, wings out, panting', 22, 'none',
        [k(.12, 'wall_l', x=.2, y=.4, b=.3), k(.3, 'wall_l', x=-.3, y=.8, b=.7, w=1, mark='puff'), k(.52, 'wall_l', x=-.4, y=.9, b=.9, w=.7, l=1, r=1, mark='fff'), k(.74, 'wall_l', x=-.2, y=.5, b=.4, w=1), k(.9, eye='^')],
        [(.52, 'cool')], g='weather', act=('cool', 'wall'), when=['warmth>.6', 'sun'], say=["Cool clay. Hot duck. Fair swap.", "Hut keeps the shade like a cellar. I keep my cool, barely."])
    o.r('rub_the_splatter_off_the_pots', 'Using the flat of his bill to wipe the rain-splashed mud off the pots', 18, 'none',
        [k(.12, 'pot_b', x=.6, y=1, b=.4), k(.3, 'pot_b', x=1.2, y=1.4, b=.7, mark='skrk'), k(.5, 'pot_a', x=1.3, y=1.5, b=.9, l=1, mark='skrk'), k(.7, 'pot_a', x=.8, y=1.1, b=.5, r=1), k(.88, eye='^')],
        [(.5, 'rub')], g='weather', act=('wipe', 'pots'), when=['splatter>.3'])
    o.r('shelter_in_the_door_nook', 'Pressing into the corner of the low door to shelter from the rain dripping off the thatch', 34, 'none',
        [k(.1, 'door_panel_l', x=.1, y=.2, b=.2, l=1), k(.3, 'lip_a', x=-.8, y=.7, b=.5, w=.7, eye='-', mark='drip'), k(.55, 'door_panel_l', x=-1, y=.9, b=1, w=.7, r=1, eye='>', mark='drip drip'), k(.8, 'lip_a', x=-.4, y=.3, b=.3, w=1, eye='^')],
        [], g='weather', act=('shelter', 'door'), when=['wet', 'storm'], say=["Thatch drips on everything but me. Skill.", "Rain drums the roof. I drum my toes."])
    # ---------------- mishap
    o.r('slip_on_the_muddy_step', 'Slipping off the mud-spattered step with his feet racing ahead of the rest of him', 14, 'none',
        [k(.15, 'step_a', perch=1, y=.2, b=.2), k(.3, 'step_a', perch=1, x=.5, y=.5, b=-.3, l=1, w=.7, eye='O'), k(.5, 'thresh', x=-.4, y=1.1, b=1.1, r=1, w=1, mark='WHOA'), k(.7, 'thresh', y=1.5, b=1.5, eye='@', mark='*splat*'), k(.88, y=.4, b=.5, eye='-')],
        [(.5, 'splash')], g='mishap', act=('slip', 'step'), when=['splatter>.3'], say=["Mud has opinions about feet. Loud ones.", "Down on the step. Up on the shame."])
    o.r('bill_stuck_in_the_reeds', 'Getting his bill stuck among the reed heads and tearing back out with a pop', 24, 'none',
        [k(.15, 'reed_tie', x=.6, y=-.2, b=.2), k(.3, 'reed_mid', x=1.4, y=-.3, b=.6, eye='O', mark='mm'), k(.5, 'reed_mid', x=1.5, y=-.3, b=.8, l=1, r=1, eye='@', mark='mmf!'), k(.7, 'reed_mid', x=1.6, y=-.2, b=1, w=1, mark='POP'), k(.88, x=-.3, y=.4, eye='>')],
        [(.7, 'scuff')], g='mishap', act=('stuck', 'reeds'), say=["Reeds got my bill. Reeds always collect.", "Pulled free. Left dignity in the bundle."])
    o.r('walk_into_the_low_door', 'Walking straight at the low door without ducking and meeting the frame', 16, 'none',
        [k(.12, x=.3, y=-.3, b=-.2), k(.3, x=1, y=-.6, b=.3, l=1, w=.3), k(.5, 'door_panel_l', x=2.1, y=.3, b=1, eye='@', mark='CLUNK'), k(.72, x=-1.2, y=.9, b=.3, r=1, w=.8, eye='O'), k(.9, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'door'), say=["Door is low. I am lower. Door still won.", "Ducked too late. Duck by name, not by habit."])
    o.r('kick_a_pot_by_accident', 'Kicking the round pot by accident and hopping about on one foot', 16, 'none',
        [k(.15, 'pot_a', x=.3, y=.7, b=.3), k(.32, 'pot_a', x=.8, y=.9, b=-.5, l=1, w=.5), k(.5, 'pot_a', x=1.3, y=1.4, b=.9, r=1, eye='@', mark='CLONK'), k(.7, x=-.3, y=.6, b=-.6, l=1, eye='O', mark='ow ow'), k(.88, y=.3, eye='-')],
        [(.5, 'crumble')], g='mishap', act=('kick', 'pot'), say=["Pot is fine. My toe is a rumour now.", "Kicked clay. Clay stayed clay. I stayed hurt."])
    o.r('catch_a_wing_on_the_sill', 'Catching a wingtip on the sill line and tearing a chip of clay loose', 18, 'wing',
        [k(.12, 'sill_l', reach=.7, x=.9, y=.1, b=-.3, r=1), k(.3, 'sill_l', reach=1, x=-.7, y=-.5, b=.6, l=1, eye='O'), k(.5, 'sill_l', reach=.5, x=.8, y=.1, b=.4, mark='ack'), k(.7, y=.6, b=1.2, r=1, eye='@'), k(.88, x=-.2, eye='-')],
        [(.5, 'crumble')], g='mishap', act=('catch', 'sill'), ages=GROWN)
    # ---------------- show
    o.r('show_off_the_pots', 'Showing the two pots off with a sweeping wing like a market stall', 20, 'wing',
        [k(.12, 'pot_a', reach=.4, x=-.5, y=.4, b=.3, l=1), k(.3, 'pot_a', reach=1, x=.2, y=-.6, b=-.6, mark='behold'), k(.5, 'pot_b', reach=1, x=.9, y=-.3, b=-.2, r=1), k(.7, 'pot_b', reach=1, x=.6, y=-.9, b=-.7, l=1, mark='fresh clay'), k(.86, x=-.3, y=0, w=.3, eye='^')],
        [], g='show', act=('show', 'pot'), say=["Handmade pots. By someone else. Price: bread.", "One round, one lidded, both empty. Premium."])
    o.r('sing_to_the_thatch', 'Singing a lullaby up at the thatch from the lower step', 22, 'none',
        [k(.14, 'step_a', perch=1, x=.2, y=-.4, b=.1), k(.34, 'step_b', perch=1, x=-.4, y=-1.1, b=-.5, w=.8, mark='laa'), k(.6, 'step_a', perch=1, x=-.8, y=-1.4, b=.2, w=1, l=1, eye='^', mark='LAAA'), k(.86, 'step_b', perch=1, x=.1, y=-.2, eye='-')],
        [], g='show', act=('sing', 'roof'), prefer=['happy'])
    o.r('dance_down_the_door_foot', 'Dancing a jig along the foot strip and down the step to the line', 20, 'none',
        [k(.12, 'lip_a', perch=1, y=-.4, b=-.6, l=1, w=.7), k(.3, 'lip_b', perch=1, x=.4, y=.4, b=.6, r=1, w=1), k(.5, 'step_b', perch=1, y=-.5, b=-.9, l=1, w=1, mark='tada'), k(.7, 'step_a', perch=1, x=.3, y=.3, b=.5, r=1, w=.8), k(.88, 'thresh', perch=1, eye='^')],
        [], g='show', act=('dance', 'lip'), prefer=['happy'])
    o.r('tap_the_little_box', 'Tapping the little box at the foot of the door to hear if it is hollow', 18, 'none',
        [k(.12, 'crate', x=.6, y=.9, b=.4), k(.3, 'crate', x=1.3, y=1.3, b=.7, mark='tonk'), k(.46, x=.1, y=.3, b=.2, eye='-', mark='...'), k(.62, 'crate', x=1.4, y=1.4, b=.8, l=1, mark='tonk'), k(.82, x=-.2, y=.2, eye='>')],
        [], g='test', act=('tap', 'crate'), prefer=['curious'])
    o.r('blow_a_reed_whistle', 'Blowing across the end of a loosened reed to make it whistle', 18, 'none',
        [k(.12, 'reed_mid', x=.3, y=-.3, b=-.2), k(.3, 'reed_mid', x=1.2, y=-.5, b=.2, w=.3, mark='fwoo'), k(.5, 'reed_mid', x=1.4, y=-.6, b=.4, w=.5, l=1, mark='fweeee'), k(.7, 'reed_mid', x=.8, y=-.2, b=-.1, w=.7, r=1, eye='^'), k(.88, eye='-')],
        [], g='play', act=('blow', 'reeds'), when=['loose>.3'], prefer=['happy'], say=["Whistled. The reeds booed. Tough crowd.", "One note. Perfect pitch for a duck."])
    o.r('press_a_footprint_in_the_clay', 'Pressing his foot print into the soft clay at the wall foot, then another', 18, 'none',
        [k(.12, 'wall_r', x=.2, y=.8, b=.6, l=1), k(.3, 'wall_r', x=.8, y=1.3, b=1.3, l=1, mark='squelch'), k(.5, 'wall_l', x=.4, y=1, b=.7, r=1), k(.7, 'wall_l', x=1, y=1.5, b=1.4, r=1, mark='squelch'), k(.88, x=-.3, y=.3, eye='^')],
        [(.7, 'scuff')], g='play', act=('press', 'wall'), when=['splatter>.3'], prefer=['happy'], say=["Left two prints in the wall foot. Evidence of me.", "Mud holds a grudge and a footprint."])
    o.r('fluff_the_reed_heads', 'Fluffing the feathery reed heads with a wingtip like a very serious hairdresser', 20, 'wing',
        [k(.12, 'reed_mid', reach=.4, x=-.2, y=-.6, b=-.3, l=1), k(.3, 'reed_mid', reach=1, x=.4, y=-1.1, b=-.7, mark='fluff'), k(.5, 'reed_tie', reach=1, x=.9, y=-.5, b=-.1, r=1), k(.7, 'reed_mid', reach=1, x=.2, y=-1.0, b=-.6, w=.3, mark='ooh'), k(.88, x=-.3, y=-.1, eye='^')],
        [], g='show', act=('fluff', 'reeds'), prefer=['happy'], say=["Reeds styled. They look windswept and unhappy.", "Little curl on the left. Hut approves, silently."])
    o.emit()
    return o


def stone_house():
    P = pm('stone_house')
    o = Obj('stone_house', 'placed',
            parts=dict(stone='the stone walls left and right of the door: courses of blocks with joints and .:\' speckle', course='the horizontal course lines between the stone blocks',
                       window='the two tall windows (cross mullion, glints and shutter strips)', sill='the ledge under each window, 75 px up',
                       plate='the (=) plates set in the door planks', door='the door leaf, upright planks with two raised panels',
                       chest='the little /_(=)\\ chest shape at the foot of the door', lantern='the lantern hung beside the door, out of reach',
                       lip='the door foot strip, 19 px up', step='the lower door-frame line, 9 px up', slab='the wide stone step slab in front of the door',
                       chimney='the tall chimney with banded stonework on the right, out of reach', roof='the slate roof, out of reach'),
            fields=dict(moss=(0, 0, 1), frost=(0, 0, 1), drift=(0, 0, 1), chill=(0, 0, 1)),
            physics=[('moss', 'rate', .0004, 'wet'), ('moss', 'rate', -.0002, 'warm'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'), ('chill', 'rate', .0008, 'cold'), ('chill', 'rate', -.0006, 'sun')],
            effects=dict(scrape=[('moss', 'mul', .2)], wipe=[('obj.dirt', 'add', -.2)], sweep=[('obj.dirt', 'add', -.15)], scrub=[('obj.dirt', 'add', -.3)],
                         dry=[('obj.wetness', 'add', -.3)], flick=[('obj.wetness', 'add', -.2)], spray=[('obj.wetness', 'add', .15)], seat=[('obj.condition', 'add', .2)],
                         crack=[('obj.condition', 'add', -.15)], scuff=[('obj.dirt', 'add', .12)], chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], grind=[('frost', 'mul', .6)],
                         kick=[('drift', 'set', 0)], scoop=[('drift', 'mul', .3)], rub=[('moss', 'mul', .5)], warm=[('chill', 'add', -.3), ('need.energy', 'add', 1)],
                         chilled=[('chill', 'add', .3), ('need.energy', 'add', 1)], soak=[('chill', 'add', -.25), ('need.energy', 'add', 2)], laugh=[('need.fun', 'add', 2)],
                         ),
            marks=[('moss', .3, ',:;,:', 'stone_l', 'plant'), ('moss', .3, ':;,;:', 'stone_r', 'plant'), ('frost', .3, '*.*.*', 'lip_a', 'frost'), ('drift', .3, '.:*:.', 'slab_a', 'snow')],
            anchors=dict(stone_l=P(22, 50), stone_l_lo=P(26, 54), stone_r=P(74, 50), stone_r_lo=P(70, 54), course_l=P(18, 47), window_l=P(22, 41), sill_l=P(22, 46), window_r=P(75, 41),
                         sill_r=P(75, 46), plate_l=P(44, 51), plate_r=P(57, 51), door_panel_l=P(50, 49), chest=P(54, 50), lantern=P(34, 37),
                         lip_a=P(40, 52, 'surface'), lip_b=P(60, 52, 'surface'), step_a=P(42, 53, 'surface'), step_b=P(56, 53, 'surface'), slab_a=P(44, 54, 'surface'), slab_b=P(58, 54, 'surface')))
    # ---------------- care
    o.r('scrape_moss_off_the_stones', 'Scraping the moss off the lower stones with the edge of his bill', 20, 'none',
        [k(.1, 'stone_l_lo', x=.6, y=1.2, b=.7, l=1), k(.28, 'stone_l_lo', x=1.3, y=1.7, b=1, mark='skrk'), k(.46, 'stone_l', x=1.4, y=1.3, b=.5, r=1, mark='skrk'), k(.66, 'stone_r_lo', x=1.1, y=1.6, b=.9, l=1, mark='skrk'), k(.86, x=-.2, w=.5, eye='^')],
        [(.46, 'scrape')], g='care', act=('scrape', 'stone'), when=['moss>.3'], say=["Moss off the stone. Moss will be back. Moss is committed.", "Scraped it green. Stone looks naked."])
    o.r('sweep_the_stone_slab', 'Sweeping the grit off the wide stone slab in front of the door with a wing', 18, 'wing',
        [k(.1, 'slab_a', reach=.4, x=.1, y=.9, b=.3, r=1), k(.28, 'slab_a', reach=1, x=.7, y=1.2, b=.7, l=1, mark='shff'), k(.48, 'slab_b', reach=1, x=.9, y=1.1, b=.5, r=1, mark='shff'), k(.7, 'step_b', reach=.8, x=.4, y=.9, b=.3, l=1), k(.88, eye='-')],
        [(.48, 'sweep')], g='care', act=('sweep', 'slab'), when=['obj_dirt>.3'])
    o.r('wipe_the_tall_window', 'Reaching up with a wing to wipe the smoke film off the left window', 20, 'wing',
        [k(.1, 'sill_l', reach=.5, x=.3, y=-.2, b=-.1, r=1), k(.28, 'window_l', reach=1, x=.2, y=-.8, b=-.6, l=1, mark='squk'), k(.46, 'window_l', reach=1, x=.8, y=-1, b=-.7, r=1, mark='squk'), k(.64, 'window_l', reach=.8, x=.5, y=-.6, b=-.4, l=1), k(.8, reach=.2, y=-.2, w=.5, eye='O'), k(.92, eye='^')],
        [(.46, 'wipe')], g='care', act=('wipe', 'window'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('dry_the_window_ledge', 'Dragging his breast along the right window ledge to dry it', 20, 'none',
        [k(.12, 'sill_r', x=.4, y=-.3, b=.3, l=1), k(.3, 'sill_r', x=1.1, y=-.1, b=.9, mark='fsh'), k(.5, 'sill_r', x=1.3, y=0, b=1, l=1, r=1, mark='fsh'), k(.7, 'window_r', x=.7, y=-.4, b=.4), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'sill'), when=['obj_wetness>.3'], ages=GROWN)
    o.r('scrub_the_door_plates', 'Scrubbing the two (=) plates on the door with a wing until they shine', 20, 'wing',
        [k(.1, 'plate_l', reach=.4, x=.3, y=.5, b=.3), k(.26, 'plate_l', reach=1, x=.6, y=.8, b=.6, r=1, mark='skrk'), k(.46, 'plate_r', reach=1, x=.8, y=.9, b=.7, l=1, mark='skrk'), k(.64, 'plate_r', reach=1, x=1, y=1, b=.9, r=1), k(.84, 'plate_l', reach=.5, x=.3, y=.5, b=.3), k(.94, eye='^')],
        [(.64, 'scrub')], g='care', act=('scrub', 'plate'), when=['obj_dirt>.3'])
    o.r('set_a_loose_stone_back', 'Mending a loose stone by shouldering it back into its course', 18, 'none',
        [k(.1, 'course_l', x=.5, y=.6, b=.3), k(.26, 'stone_l', x=-.9, y=.9, b=.9, mark='nnf'), k(.44, 'stone_l', x=-1.2, y=1, b=1.1, l=1, r=1, mark='nnnf'), k(.62, 'stone_l', x=-1.3, y=1.1, b=1.3, w=.4, mark='THUD'), k(.8, x=.1, y=.4, b=.2), k(.92, eye='^')],
        [(.62, 'seat')], g='care', act=('mend', 'stone'), when=['obj_condition<.6'], say=["Stone back in its row. House stands. I fall over.", "Shoved it into place. Stone saw it coming."])
    o.r('rub_the_moss_off_the_ledge', 'Polishing the moss off the left ledge with his breast in slow circles', 20, 'none',
        [k(.12, 'sill_l', x=.5, y=-.1, b=.4), k(.3, 'sill_l', x=1, y=.1, b=.8, l=1, mark='fsh'), k(.5, 'window_l', x=.9, y=-.6, b=-.2, r=1), k(.7, 'sill_l', x=1.2, y=.2, b=.9, l=1, r=1, mark='fsh'), k(.88, eye='-')],
        [(.7, 'rub')], g='care', act=('polish', 'ledge'), when=['moss>.3'], ages=GROWN)
    # ---------------- use
    o.r('push_the_oak_door', 'Pushing a shoulder against the heavy door to see if it gives', 18, 'none',
        [k(.12, 'door_panel_l', x=.3, y=.2, b=.2, r=1), k(.3, 'door_panel_l', x=-.9, y=.7, b=.7, mark='hup'), k(.5, 'door_panel_l', x=-1.1, y=.8, b=1.1, l=1, r=1, mark='hnn'), k(.72, 'door_panel_l', x=-.4, y=.4, b=.4), k(.88, x=.2, y=.5, eye='-')],
        [], g='use', act=('push', 'door'), obj=[(.5, dict(shake=.1))], say=["Heavy door. Heavier opinion of me.", "Shoulder met oak. Oak is winning."])
    o.r('knock_with_a_plate', 'Knocking on the door beside the plates and waiting for a servant', 20, 'none',
        [k(.12, 'plate_l', x=.5, y=-.2), k(.28, 'plate_l', x=1.3, y=-.3, b=.3, mark='tok'), k(.44, 'plate_r', x=.1, y=-.2, b=-.2, w=.4), k(.6, 'plate_r', x=1.4, y=-.3, b=.4, mark='tok tok'), k(.78, x=-.4, y=-.6, b=-.3, w=.7, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'plate'))
    o.r('peer_into_the_window', 'Craning up on tiptoe to peer into the tall right window'.replace('on tiptoe ', ''), 22, 'none',
        [k(.12, 'sill_r', x=.2, y=-.3, b=-.3), k(.32, 'window_r', x=1.2, y=-.9, b=-.8, w=.4, eye='O'), k(.56, 'window_r', x=1.4, y=-1, b=-.9, l=1, mark='...'), k(.78, 'sill_r', x=-.2, y=-.2, b=-.1, eye='-'), k(.9, eye='>')],
        [], g='use', act=('peer', 'window'), prefer=['curious'], ages=GROWN)
    o.r('hang_on_a_door_plate', 'Pulling down on the lower door plate with his whole weight to see what moves', 18, 'none',
        [k(.15, 'plate_r', x=.5, y=.9, b=.3), k(.35, 'plate_r', x=1.2, y=1.3, b=1, l=1, mark='hnn'), k(.55, 'plate_r', x=1.3, y=1.4, b=1.1, r=1, eye='>'), k(.78, x=-.3, y=-.2, w=.5, eye='-', mark='nothing')],
        [], g='use', act=('pull', 'plate'), ages=GROWN)
    o.r('shout_up_the_chimney', 'Cupping a wing and shouting up at the chimney for Father Winter', 18, 'none',
        [k(.15, x=-.1, y=-.8, b=-.1), k(.35, x=-.6, y=-1.3, b=-.6, w=.6, mark='HOY'), k(.58, x=-.9, y=-1.6, b=-.8, w=.9, r=1, mark='HOOOY'), k(.8, x=-.2, y=-.5, b=-.2, eye='-')],
        [(.58, 'laugh')], g='use', act=('shout', 'chimney'), far=True, say=["Shouted at the chimney. It coughed soot. Rude.", "Echo came back as smoke. Smoke has no manners."])
    # ---------------- play
    o.r('hop_up_the_stone_slab', 'Taking a run and a hop up onto the wide slab, then a hop off again', 18, 'none',
        [k(.1, 'step_a', perch=1, x=.1, y=.2, b=.3), k(.28, 'slab_a', perch=1, x=.5, y=-.4, b=-.9, l=1, w=.9, mark='hup'), k(.46, 'slab_b', perch=1, x=.9, y=.3, b=.2, r=1, w=.5), k(.66, 'slab_b', perch=1, x=-.3, y=-.5, b=-.6, l=1, w=1), k(.86, 'step_b', y=.5, b=.8, w=.4), k(.94, eye='^')],
        [], g='play', act=('hop', 'slab'), prefer=['happy', 'young'])
    o.r('race_along_the_lip', 'Running a race along the door foot from end to end, wings out', 16, 'none',
        [k(.1, 'lip_a', perch=1, x=-.2, y=.2, b=.5, w=.3), k(.3, 'lip_a', perch=1, x=1, y=.5, b=.1, l=1, w=1, mark='zoom'), k(.5, 'lip_b', perch=1, x=.6, y=.2, b=.6, r=1, w=.7), k(.72, 'lip_b', perch=1, x=1.1, y=.6, b=.2, l=1, w=1), k(.9, eye='^')],
        [], g='play', act=('race', 'lip'), prefer=['happy'])
    o.r('hide_at_the_corner_stones', 'Trying to hide flat against the corner stones, then bursting out at nothing', 18, 'none',
        [k(.12, 'stone_r', x=-.3, y=.2), k(.3, 'stone_r', x=-1.1, y=.7, b=.9, eye='O'), k(.52, 'stone_r_lo', x=-1.2, y=.9, b=1.1, mark='shh'), k(.7, 'stone_r_lo', x=1.3, y=-.5, b=-.7, w=1, l=1, r=1, mark='BAH'), k(.88, eye='^')],
        [], g='play', act=('hide', 'stone'), prefer=['young'])
    o.r('hop_from_stone_to_stone', 'Hopping from course to course up the wall as far as he can reach', 20, 'none',
        [k(.1, 'stone_l_lo', x=.3, y=.2, b=-.3), k(.26, 'stone_l', x=.5, y=-.4, b=-.8, l=1, w=.6, mark='hup'), k(.42, 'course_l', x=.7, y=-.7, b=-.9, r=1, w=.8, mark='hup'), k(.6, 'stone_l', x=.2, y=.2, b=.6, l=1), k(.78, 'stone_l_lo', x=.4, y=.5, b=.9, r=1, w=.4), k(.9, eye='^')],
        [], g='play', act=('hop', 'stone'), prefer=['young'], ages=GROWN)
    o.r('drum_on_the_stones', 'Drumming a slow beat against the stone blocks with his bill', 18, 'none',
        [k(.12, 'stone_l', x=.9, y=.5, b=.2, mark='tok'), k(.3, 'course_l', x=.8, y=1.1, b=-.2, l=1, mark='tok'), k(.5, 'stone_l', x=1.1, y=.6, b=.3, r=1, mark='tok tok'), k(.7, 'course_l', x=.7, y=1.2, b=-.1, l=1, mark='TOK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'stone'), prefer=['happy'], say=["Stone has no rhythm. Wonderful bass.", "Stone on the downbeat. Moss on the hi-hat."])
    o.r('balance_on_the_slab_edge', 'Balancing along the edge of the step slab with his wings out', 18, 'none',
        [k(.12, 'slab_a', perch=1, x=-.3, y=-.2, w=.5, r=1), k(.34, 'slab_a', perch=1, x=.4, y=.3, b=.6, l=1, w=1), k(.58, 'slab_b', perch=1, x=.9, b=.8, r=1, w=1, mark='whoa'), k(.8, 'slab_b', perch=1, x=.2, y=.2, b=.3, w=.6), k(.92, eye='^')],
        [], g='play', act=('balance', 'slab'))
    # ---------------- test
    o.r('tap_the_stone_for_hollow', 'Tapping the stone courses from the bottom up to hear where they ring hollow', 18, 'none',
        [k(.1, 'stone_r_lo', x=1.2, y=1.1, b=.8, mark='tok'), k(.26, 'stone_r', x=.7, y=-.3, b=-.5, l=1, mark='tok'), k(.44, 'window_r', x=.1, y=-.9, b=-.2, w=.8, eye='-'), k(.62, 'stone_r', x=1.6, y=.9, b=.9, r=1, mark='tonk'), k(.8, eye='^')],
        [], g='test', act=('tap', 'stone'))
    o.r('count_the_courses', 'Touching each course line up the left wall and counting under his breath', 22, 'none',
        [k(.08, 'stone_l_lo', x=1.1, y=1.4, b=.9, mark='1'), k(.28, 'stone_l', x=1.3, y=1.2, b=.2, r=1, mark='2'), k(.5, 'course_l', x=.9, y=1, b=1.1, l=1, mark='3'), k(.7, 'sill_l', x=1.4, y=.3, b=.4, r=1, mark='4'), k(.86, x=-.7, y=-.5, w=.7, eye='-', mark='four')],
        [], g='test', act=('count', 'course'), prefer=['curious'])
    o.r('test_the_stone_for_cold', 'Testing the stone for cold with his breast, then the other cheek', 22, 'none',
        [k(.12, 'stone_r', x=.2, y=.2, b=.3), k(.3, 'stone_r', x=-.8, y=.6, b=.8, eye='O', mark='eek'), k(.5, 'stone_l', x=.3, y=.4, b=.3), k(.68, 'stone_l', x=-.9, y=.7, b=.9, r=1, eye='O', mark='eek'), k(.86, x=.1, y=.2, eye='-')],
        [(.68, 'chilled')], g='test', act=('test', 'stone'), when=['chill>.3'], say=["Cold. Stone is cold. Report filed.", "Cheek cold. Opinion colder."])
    o.r('taste_the_cold_stone', 'Licking the corner stone to taste the cold and the moss', 18, 'none',
        [k(.12, 'stone_l_lo', x=.5, y=.6, b=.3), k(.3, 'stone_l_lo', x=1.2, y=.8, b=.4, mark='lk'), k(.5, x=.1, y=.2, eye='O', mark='bleh'), k(.68, x=-.2, y=.6, b=.3, eye='-', mark='dirt'), k(.86, eye='>')],
        [], g='test', act=('taste', 'stone'))
    o.r('prod_the_lantern', 'Prodding the lantern with a twig to see if it swings', 22, 'twig',
        [k(.14, 'lantern', reach=.5, x=.2, y=-.8, b=-.3), k(.32, 'lantern', reach=1, x=.6, y=-1.2, b=-.6, mark='tk'), k(.52, 'lantern', reach=1, x=-.1, y=-1.3, b=-.7, w=.3, mark='tink'), k(.72, 'lantern', reach=.6, x=.5, y=-.9, b=-.3), k(.9, x=-.3, y=-.2, eye='-')],
        [], g='test', act=('prod', 'lantern'), ages=GROWN, say=["Lantern did not swing. Lantern is bolted. Lantern is loyal.", "Poked it. It glowered. Lanterns do that."])
    o.r('measure_the_step', 'Trying to measure himself against the step lines to see how high he stands', 20, 'none',
        [k(.12, 'step_a', x=-.4, y=.2, b=.2), k(.3, 'lip_a', x=-.5, y=-.8, b=-.6, w=.8, mark='...'), k(.55, 'step_a', x=1.1, y=1.1, b=.8, eye='O'), k(.75, 'step_a', x=-.2, y=.2, b=.3, l=1, eye='-', mark='ankle'), k(.9, eye='>')],
        [], g='test', act=('measure', 'step'), prefer=['young'])
    # ---------------- rest
    o.r('lean_on_the_sunny_stone', 'Leaning his back against the sun-warmed stone and soaking up the heat', 24, 'none',
        [k(.1, 'stone_r', x=.6, y=.1, b=.1, l=1), k(.3, 'stone_r', x=-.9, y=.5, b=.3, eye='-'), k(.55, 'stone_r_lo', x=-1.2, y=.6, b=.9, eye='-', mark='ahh'), k(.8, 'stone_r_lo', x=-.6, y=.1, b=.6, r=1, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'stone'), when=['chill<.4', 'sun'] if False else ['sun'], say=["Warm stone. This is why they built houses of it.", "Heat in the rock, none in my plans."])
    o.r('sit_on_the_slab', 'Sitting on the stone slab with his wings folded and his thoughts elsewhere', 24, 'none',
        [k(.12, 'slab_b', perch=1, x=.4, y=-.5, b=.1, r=1), k(.3, 'slab_b', perch=1, x=-.3, y=.1, b=.6, eye='-'), k(.6, 'slab_b', perch=1, x=-.4, y=.2, b=1.2, eye='-', mark='...'), k(.85, 'slab_b', perch=1, x=0, y=-.2, b=.3, l=1, eye='^')],
        [], g='rest', act=('sit', 'slab'))
    o.r('sulk_at_the_chimney_side', 'Sulking with his back to the house, facing the yard like it owes him bread', 22, 'none',
        [k(.14, 'stone_l', x=.7, y=-.1, b=.1, r=1), k(.34, 'stone_l', x=-1.2, y=.5, b=1.1, eye='-', mark='hmph'), k(.58, 'stone_l_lo', x=-.6, y=1.4, b=.6, l=1, eye='>'), k(.84, 'stone_l_lo', x=-.9, y=.1, b=.2, r=1, eye='-')],
        [], g='rest', act=('sulk', 'stone'), prefer=['grumpy', 'sad'], say=["The house knows what it did.", "Sulking in stone's shadow. Roomy."])
    o.r('perch_on_the_window_ledge', 'Perching on the low door foot like a gargoyle without the budget', 24, 'none',
        [k(.14, 'lip_b', perch=1, x=.9, y=-.8, b=-.5, w=.2, l=1), k(.36, 'lip_b', perch=1, x=.2, y=-.2, b=.5, eye='O'), k(.6, 'lip_b', perch=1, x=-.8, y=-.6, b=.1, w=.8, mark='hm'), k(.86, 'lip_b', perch=1, x=.5, y=.2, b=.6, r=1, eye='-')],
        [], g='rest', act=('perch', 'lip'), prefer=['curious'])
    o.r('warm_feet_on_the_slab', 'Warming one foot, then the other, on the sun-baked slab', 22, 'none',
        [k(.12, 'slab_a', perch=1, x=.8, y=.1, b=.5, r=1), k(.35, 'slab_a', perch=1, x=-.2, y=.9, b=.9, r=1, eye='-', mark='ahh'), k(.6, 'slab_a', perch=1, x=-.1, y=.8, b=.2, l=1, eye='^'), k(.85, 'slab_a', perch=1, x=.6, y=-.2, b=.7, eye='-')],
        [(.6, 'warm')], g='rest', act=('warm', 'slab'), when=['chill>.3', 'sun'])
    o.r('guard_the_stone_door', 'Standing guard on the step before the stone house, chest out', 24, 'none',
        [k(.12, 'door_panel_l', x=.6, y=-.1, b=.3, l=1), k(.34, 'slab_a', perch=1, x=1.1, y=-1, b=-.7, w=.9, eye='>'), k(.58, 'slab_a', perch=1, x=-.7, y=-.9, b=-.3, r=1, w=.4, mark='halt'), k(.86, 'slab_a', perch=1, x=.2, y=.1, b=.1, w=.7, eye='-')],
        [], g='rest', act=('guard', 'door'), prefer=['lonely'])
    # ---------------- weather
    o.r('chip_frost_off_the_foot_strip', 'Chipping the frost off the door foot with the edge of his bill', 18, 'none',
        [k(.1, 'lip_b', x=1.1, y=1.3, b=.4, r=1), k(.28, 'lip_b', x=1.7, y=1.6, b=.8, mark='tk'), k(.48, 'lip_a', x=1.8, y=1.4, b=1.1, l=1, mark='tk'), k(.7, 'lip_a', x=.9, y=1.1, b=.6, r=1), k(.88, x=-.2, w=.5, eye='^')],
        [(.48, 'chip')], g='weather', act=('chip', 'lip'), when=['frost>.3'], say=["Frost chipped off. Step smug about its shine.", "Foot strip free. Beak slightly less so."])
    o.r('blow_on_the_frosted_window', 'Blowing warm breath at the frosted ledge until it drips', 18, 'none',
        [k(.1, 'sill_l', x=1.2, y=-.8, b=-.5, r=1), k(.3, 'sill_l', x=.6, y=-.2, b=.4, mark='haah'), k(.5, 'window_l', x=1.5, y=-1, b=-.1, w=.7, l=1, mark='haaah'), k(.72, 'sill_l', x=.2, y=-.6, b=.1, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'sill'), when=['frost>.3'], ages=GROWN)
    o.r('kick_the_drift_off_the_slab', 'Kicking the snow drift off the slab in two long swipes of his foot', 18, 'none',
        [k(.12, 'slab_a', x=.3, y=.5, b=.4, r=1), k(.3, 'slab_a', x=.4, y=.8, b=.8, l=1, mark='fff'), k(.5, 'slab_b', x=.4, y=.9, b=.9, r=1, mark='FFF'), k(.72, 'slab_b', x=.3, y=.5, b=.4, l=1), k(.88, eye='^')],
        [(.5, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Slab clear. Foot frozen. Net gain: slab.", "Snow flew. I did not."])
    o.r('scoop_snow_off_the_step', 'Scooping the snow off the step lines in wingfuls', 20, 'wing',
        [k(.12, 'step_a', reach=.4, x=.1, y=.9, b=.4), k(.3, 'step_a', reach=1, x=.5, y=1.2, b=.8, l=1, mark='fsh'), k(.5, 'step_b', reach=1, x=.7, y=1.1, b=.9, r=1, mark='fsh'), k(.7, 'lip_b', reach=.7, x=.4, y=.7, b=.3), k(.88, eye='^')],
        [(.5, 'scoop')], g='weather', act=('scoop', 'drift'), when=['drift>.5'])
    o.r('shake_the_rain_off_by_the_stones', 'Shaking the rain off his back with the corner stones at his shoulder', 18, 'none',
        [k(.12, 'stone_l_lo', x=.2, y=.2, b=.2), k(.3, 'stone_l_lo', x=-.2, y=.7, b=.7, w=1, mark='brrr'), k(.5, 'stone_l_lo', x=.3, y=.8, b=.9, w=1, l=1), k(.7, 'stone_l_lo', x=-.3, y=.5, b=.5, w=1, r=1), k(.88, eye='^')],
        [(.5, 'spray')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    o.r('shelter_in_the_door_recess', 'Pressing into the door recess to shelter from the rain while the slate roof sheds it', 34, 'none',
        [k(.1, 'door_panel_l', x=.6, y=.5, b=.8, l=1), k(.3, 'lip_a', x=-.3, y=1.2, b=.2, w=.3, eye='-', mark='drip'), k(.55, 'door_panel_l', x=-1.4, y=.3, b=1.4, w=.9, eye='>', mark='drip drip'), k(.8, 'lip_a', x=.1, y=.9, b=.6, w=.5, r=1, eye='^')],
        [], g='weather', act=('shelter', 'door'), when=['wet', 'storm'], say=["Slate sheds, I shelter, the weather loses.", "Dry doorway. Wet yard. Great seats."])
    # ---------------- mishap
    o.r('slip_on_the_icy_step', 'Slipping on the iced step with both feet going different ways', 14, 'none',
        [k(.12, 'step_a', perch=1, x=.2, y=.1, b=.5, r=1), k(.3, 'step_a', perch=1, x=-.4, y=.8, b=-.6, l=1, w=1, eye='O'), k(.5, 'slab_a', x=.9, y=.3, b=1.3, r=1, w=.5, mark='WHOA'), k(.7, 'slab_a', x=.2, y=1.7, b=1.6, eye='@', mark='*thud*'), k(.88, y=.2, b=.7, eye='-')],
        [(.5, 'grind')], g='mishap', act=('slip', 'step'), when=['frost>.5'], say=["Ice has a sense of humour. Stone has none.", "Feet north, duck south, step unmoved."])
    o.r('walk_into_the_oak_door', 'Walking straight at the stone house door, thinking it was open, and meeting it', 16, 'none',
        [k(.12, x=.4, y=-.2, b=-.1), k(.3, x=1.1, y=-.5, b=.4, r=1, w=.4), k(.5, 'door_panel_l', x=2, y=.1, b=1.1, eye='@', mark='THONK'), k(.72, x=-1, y=.8, b=.3, l=1, w=.9, eye='O'), k(.9, y=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'door'), say=["Solid oak. Solid regret.", "Door was closed. I was optimistic."])
    o.r('catch_a_wing_on_the_stone_edge', 'Catching a wingtip on a rough stone edge and tearing loose again', 18, 'wing',
        [k(.12, 'stone_l', reach=.5, x=.7, y=.2, b=-.2, l=1), k(.3, 'stone_l', reach=1, x=-.6, y=-.4, b=.5, r=1, eye='O'), k(.5, 'course_l', reach=.5, x=.6, y=0, b=.5, mark='ack'), k(.7, y=.7, b=1.1, l=1, eye='@'), k(.88, x=-.3, eye='-')],
        [(.5, 'crack')], g='mishap', act=('catch', 'stone'), ages=GROWN)
    o.r('kick_a_stone_by_accident', 'Kicking the corner stone by accident and hopping about on one foot', 16, 'none',
        [k(.15, 'stone_r_lo', x=.4, y=.7, b=.3), k(.32, 'stone_r_lo', x=.9, y=1, b=-.5, l=1, w=.5), k(.5, 'stone_r_lo', x=1.4, y=1.4, b=.9, r=1, eye='@', mark='CLONK'), k(.7, x=-.3, y=.6, b=-.6, l=1, eye='O', mark='ow ow'), k(.88, y=.3, eye='-')],
        [(.5, 'scuff')], g='mishap', act=('kick', 'stone'), say=["Stone: 1. Toe: 0. Stone barely noticed.", "Kicked the house. House kicked back, slowly."])
    # ---------------- show
    o.r('bow_to_the_lantern', 'Bowing low to the lantern like a footman who has lost the carriage', 20, 'none',
        [k(.14, 'plate_l', y=.1), k(.34, 'step_a', perch=1, x=.4, y=1.3, b=1, w=.5, eye='-'), k(.54, 'step_a', perch=1, x=.5, y=1.5, b=1.3, w=.8, mark='your lordship'), k(.78, 'step_a', perch=1, y=.1, w=.3, eye='^')],
        [], g='show', act=('bow', 'lantern'), prefer=['happy'])
    o.r('show_off_the_stone_house', 'Showing off the stone house with a sweeping wing like a very small estate agent', 20, 'wing',
        [k(.1, 'stone_l_lo', reach=.7, x=.4, y=-.3, b=-.2, l=1), k(.28, 'course_l', reach=1, x=-.6, y=-.6, b=-.3, mark='behold'), k(.48, 'door_panel_l', reach=.5, x=1.2, y=-.9, b=-.6, r=1), k(.68, 'stone_r', reach=1, x=-.2, y=-.4, b=.2, l=1, mark='slate roof'), k(.86, x=.2, y=.4, w=.6, eye='^')],
        [], g='show', act=('show', 'house'), say=["Solid. Draughty. Built to outlive the buyer.", "Chimney included. Duck optional."])
    o.r('sing_to_the_slate_roof', 'Singing a ballad up at the slate roof from the middle of the slab', 22, 'none',
        [k(.14, 'slab_a', perch=1, x=.9, y=-.1, b=.5), k(.34, 'step_b', perch=1, x=-.1, y=-1.6, b=-.9, w=.3, mark='laa'), k(.6, 'slab_a', perch=1, x=-1.2, y=-.7, b=.7, w=.6, r=1, eye='^', mark='LAAA'), k(.86, 'step_b', perch=1, x=.5, y=.2, b=-.2, l=1, eye='-')],
        [], g='show', act=('sing', 'roof'), prefer=['happy'])
    o.r('dance_across_the_slab', 'Dancing a jig across the slab and up onto the door foot', 20, 'none',
        [k(.12, 'slab_a', perch=1, x=.7, y=.3, b=-.3, r=1, w=1), k(.3, 'slab_b', perch=1, x=-.3, y=-.7, b=1, l=1, w=.4), k(.5, 'step_b', perch=1, x=.9, y=.2, b=-1.2, r=1, w=.7, mark='tada'), k(.7, 'lip_b', perch=1, x=-.5, y=-.3, b=.9, l=1, w=1), k(.88, 'lip_a', perch=1, x=.4, eye='^')],
        [], g='show', act=('dance', 'slab'), prefer=['happy'])
    o.r('tug_a_rope_of_moss', 'Tugging a long rope of moss off the stone with his bill', 18, 'none',
        [k(.12, 'stone_l', x=.5, y=.2, b=.2), k(.3, 'stone_l', x=1.3, y=.4, b=.7, mark='mmf'), k(.5, 'course_l', x=-.7, y=-.3, b=-.6, w=.6, mark='frrp'), k(.7, 'stone_l_lo', x=.4, y=1, b=.5), k(.88, eye='^')],
        [(.5, 'rub')], g='use', act=('tug', 'moss'), when=['moss>.3'], say=["Moss came off in one long green sigh.", "Held up the moss. Stone looked bald."])
    o.r('dry_the_wet_plates', 'Drying the rain off the door plates with a dry wing', 18, 'wing',
        [k(.12, 'plate_l', reach=.5, x=.2, y=.4, b=.2), k(.3, 'plate_l', reach=1, x=.6, y=.7, b=.6, r=1, mark='squk'), k(.5, 'plate_r', reach=1, x=.8, y=.8, b=.5, l=1, mark='squk'), k(.7, 'chest', reach=.7, x=.4, y=.6, b=.3), k(.88, eye='-')],
        [(.5, 'flick')], g='weather', act=('dry', 'plate'), when=['obj_wetness>.3'])
    o.r('climb_the_step_lines', 'Climbing the step lines one at a time up to the door foot, then jumping down', 18, 'none',
        [k(.1, 'slab_b', perch=1, x=.2, y=.1, b=.4), k(.28, 'step_b', perch=1, x=.3, y=-.5, b=-.7, l=1, w=.7, mark='hup'), k(.46, 'lip_b', perch=1, x=.6, y=-.7, b=-.9, r=1, w=.9, mark='hup'), k(.64, 'lip_b', perch=1, x=-.4, y=.1, b=.3, w=.4), k(.82, 'slab_b', x=.7, y=.5, b=1.1, l=1, r=1, w=1, mark='HAH'), k(.92, eye='^')],
        [], g='play', act=('climb', 'step'), prefer=['happy', 'young'])
    o.r('weigh_the_chest_shape', 'Leaning into the chest shape at the foot of the door to weigh whether it is full', 20, 'none',
        [k(.1, 'chest', x=.6, y=.3, b=.1, r=1), k(.3, 'chest', x=-1.1, y=.5, b=1, mark='hnn'), k(.5, 'plate_r', x=-.3, y=1.2, b=.4, l=1, mark='hnnf'), k(.7, 'chest', x=.2, y=.4, b=.9, w=.6, eye='-', mark='hollow'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'chest'))
    o.emit()
    return o


def wooden_cottage():
    P = pm('wooden_cottage')
    o = Obj('wooden_cottage', 'placed',
            parts=dict(brace='the timber cross-braces (\\ and / diagonals) and the centre post set into the wall planks', plank='the wall planks between the braces, with nail heads (o)',
                       plate='the (=) plates set in the planks', window='the two windows with cross mullion, glints and curtain strips', sill='the ledge under each window, 75 px up',
                       planter='the two flower boxes at the foot of the walls', flower='the (*) blossoms standing in each box',
                       mail='the small mailbox at the far right: a curved lid, a round latch and a box', door='the door leaf, upright planks with raised panels',
                       chest='the little chest shape with a (=) plate at the foot of the door', lip='the door foot strip, 19 px up', step='the lower door-frame line, 9 px up',
                       thresh='the standing line in front of the door', chimney='the tall banded chimney on the right, out of reach', roof='the shingle roof, out of reach'),
            fields=dict(bloom=(0, 0, 1), leaves=(0, 0, 1), drift=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('bloom', 'rate', .0008, 'growing'), ('bloom', 'rate', -.0006, 'cold'), ('leaves', 'rate', .0025, 'windy'), ('leaves', 'rate', -.0003, 'calm'),
                     ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(scrub=[('obj.dirt', 'add', -.3)], wipe=[('obj.dirt', 'add', -.2)], polish=[('obj.dirt', 'add', -.15)], dry=[('obj.wetness', 'add', -.3)],
                         shake=[('obj.wetness', 'add', .15)], mend=[('obj.condition', 'add', .2)], crack=[('obj.condition', 'add', -.15)], scuff=[('obj.dirt', 'add', .12)],
                         sweep=[('leaves', 'mul', .2)], rake=[('leaves', 'mul', .4)], kick=[('drift', 'set', 0)], scoop=[('drift', 'mul', .3)],
                         chip=[('frost', 'mul', .2)], huff=[('frost', 'mul', .4)], nip=[('bloom', 'mul', .6)], snap=[('bloom', 'mul', .5)],
                         soak=[('need.energy', 'add', 2)], laugh=[('need.fun', 'add', 2)], hush=[('need.energy', 'add', 1)]),
            marks=[('bloom', .5, '* * *', 'flower_l', 'plant'), ('bloom', .5, '* * *', 'flower_r', 'plant'), ('leaves', .3, '~ , ~ ,', 'step_b', 'leaf'),
                   ('drift', .3, '.:*:.', 'step_a', 'snow'), ('frost', .3, '*.*.*', 'sill_l', 'frost')],
            anchors=dict(planter_l=P(15, 54, 'surface'), planter_r=P(81, 55, 'surface'), flower_l=P(13, 50), flower_r=P(81, 50), mail_top=P(92, 51, 'surface'), mail=P(94, 53),
                         brace_l=P(24, 50), brace_r=P(74, 50), plank_l=P(26, 53), plate_l=P(28, 49), plate_r=P(75, 49), window_l=P(24, 43), sill_l=P(22, 47), window_r=P(76, 43),
                         sill_r=P(76, 47), door_panel_l=P(50, 50), chest=P(56, 52), lip_a=P(42, 53, 'surface'), lip_b=P(58, 53, 'surface'), step_a=P(44, 54, 'surface'),
                         step_b=P(56, 54, 'surface'), thresh=P(51, 55, 'surface')))
    # ---------------- care
    o.r('scrub_the_timber_planks', 'Scrubbing the planks between the braces with a wing until the grain shows', 20, 'wing',
        [k(.1, 'plank_l', reach=.4, x=.5, y=.5, b=.1), k(.26, 'plank_l', reach=1, x=.9, y=.8, b=.4, r=1, mark='skrk'), k(.44, 'brace_l', reach=1, x=.5, y=.4, b=.7, l=1, mark='skrk'), k(.62, 'plank_l', reach=1, x=1.1, y=1, b=.5, r=1), k(.8, 'plate_l', reach=.5, x=.2, y=.5, b=.2), k(.92, eye='^')],
        [(.62, 'scrub')], g='care', act=('scrub', 'plank'), when=['obj_dirt>.3'], say=["Timber was grey. Now timber is grey and damp.", "Scrubbed the planks. Wing has opinions."])
    o.r('sweep_the_leaves_off_the_step', 'Sweeping the blown leaves off the step towards the yard with a wing', 18, 'wing',
        [k(.1, 'step_b', reach=.4, x=.2, y=.7, b=.4, r=1), k(.28, 'step_b', reach=1, x=.8, y=1, b=.8, l=1, mark='shff'), k(.48, 'step_a', reach=1, x=1, y=1.2, b=.3, r=1, mark='shff'), k(.68, 'lip_a', reach=.7, x=.5, y=.6, b=.5, l=1), k(.86, eye='-')],
        [(.48, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], say=["Leaves in the yard. Yard did not ask.", "Swept the step. The wind is already reconsidering."])
    o.r('wipe_the_window_curtains', 'Reaching up with a wing to wipe the dust off the left window glass', 20, 'wing',
        [k(.1, 'sill_l', reach=.5, x=.2, y=-.2, b=.1, l=1), k(.28, 'window_l', reach=1, x=.6, y=-.7, b=-.4, r=1, mark='squk'), k(.46, 'window_l', reach=1, x=1, y=-.9, b=-.6, l=1, mark='squk'), k(.64, 'window_l', reach=.8, x=.3, y=-.5, b=-.3, r=1), k(.8, reach=.2, y=-.3, w=.4, eye='O'), k(.92, eye='^')],
        [(.46, 'wipe')], g='care', act=('wipe', 'window'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('dry_the_planter_edge', 'Dragging his breast along the right flower box to dry the rim', 20, 'none',
        [k(.12, 'planter_r', x=.4, y=.5, b=.5, r=1), k(.3, 'planter_r', x=1, y=.9, b=.9, mark='fsh'), k(.5, 'planter_r', x=1.2, y=1, b=1, l=1, r=1, mark='fsh'), k(.7, 'flower_r', x=.6, y=-.2, b=.2), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'planter'), when=['obj_wetness>.3'])
    o.r('nail_a_brace_back', 'Mending a loose brace by leaning on it until the nails bite again', 18, 'none',
        [k(.1, 'brace_r', x=-.2, y=.8, b=.6, r=1), k(.26, 'brace_r', x=.9, y=1.4, b=.3, l=1, mark='nnf'), k(.42, 'brace_r', x=-.6, y=.5, b=1.4, r=1, mark='nnnf'), k(.6, 'brace_r', x=1.9, y=1.5, b=.8, w=.7, mark='CLICK'), k(.78, x=.5, y=-.2, b=-.2), k(.9, eye='^')],
        [(.6, 'mend')], g='care', act=('mend', 'brace'), when=['obj_condition<.6'], say=["Brace holds. Cottage stands. I lie down.", "Hammered with my chest. Chest has regrets."])
    o.r('nip_the_wilted_heads', 'Pulling the wilted heads off the flowers with his bill, one by one', 20, 'none',
        [k(.1, 'flower_l', x=.5, y=-.2, b=-.1), k(.28, 'flower_l', x=1.1, y=-.4, b=.2, mark='nip'), k(.46, 'flower_l', x=-.3, y=-.3, b=-.4, w=.4, mark='fwip'), k(.64, 'flower_r', x=1, y=-.3, b=.1, l=1, mark='nip'), k(.84, x=-.2, eye='^')],
        [(.64, 'nip')], g='care', act=('pull', 'flower'), when=['bloom>.5'], say=["Wilted heads off. The cottage looks brighter and slightly smug.", "Neater now. Flowers can hold a grudge."])
    o.r('polish_the_mailbox', 'Polishing the mailbox lid with a wing until he can see a duck in it', 18, 'wing',
        [k(.1, 'mail', reach=.4, x=.3, y=.3, b=.1), k(.26, 'mail_top', reach=1, x=.6, y=.5, b=.5, l=1, mark='squk'), k(.44, 'mail_top', reach=1, x=.9, y=.6, b=.6, r=1, mark='squk'), k(.64, 'mail', reach=1, x=.5, y=.4, b=.3, l=1), k(.84, x=-.3, eye='^')],
        [(.44, 'polish')], g='care', act=('polish', 'mail'), when=['obj_dirt>.3'])
    # ---------------- use
    o.r('knock_at_the_cottage_door', 'Knocking at the door, a polite pause, then knocking at the chest shape as well', 20, 'none',
        [k(.12, 'door_panel_l', x=.6, y=-.2, b=.1), k(.28, 'door_panel_l', x=1.3, y=-.3, b=.4, mark='tok'), k(.44, 'door_panel_l', x=.1, y=-.1, b=-.2, w=.4), k(.6, 'chest', x=1.4, y=.5, b=.6, mark='tok tok'), k(.78, x=-.5, y=-.6, b=-.3, w=.7, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('knock', 'door'), say=["Knocked. Doormat unmoved. Doormat is not here.", "Polite knock, polite wait, polite sulk."])
    o.r('push_the_cottage_door', 'Pushing a shoulder against the cottage door to test it for give', 18, 'none',
        [k(.12, 'door_panel_l', x=.1, y=.3, b=.2, r=1), k(.3, 'door_panel_l', x=-1, y=.6, b=.6, mark='hup'), k(.5, 'door_panel_l', x=-1.2, y=.7, b=1.2, l=1, r=1, mark='hnn'), k(.72, 'door_panel_l', x=-.5, y=.3, b=.5), k(.88, x=.3, y=.5, eye='-')],
        [], g='use', act=('push', 'door'), obj=[(.5, dict(shake=.1))])
    o.r('peer_into_the_mailbox', 'Peering into the mailbox through the lid slot for anything with his name on it', 20, 'none',
        [k(.12, 'mail_top', x=.3, y=-.1, b=.2), k(.3, 'mail_top', x=1.3, y=.7, b=.5, eye='O'), k(.52, 'mail_top', x=1.5, y=.8, b=.6, l=1, mark='...'), k(.74, 'mail_top', x=-.2, y=.2, b=.1, eye='-'), k(.9, eye='>')],
        [], g='use', act=('peer', 'mail'), prefer=['curious'], say=["Mailbox: empty. Typical. I never get bread by post.", "Looked in. It looked emptier."])
    o.r('sniff_the_flower_box', 'Sniffing along the left flower box, then sneezing into the nearest bloom', 22, 'none',
        [k(.1, 'planter_l', x=.7, y=.6, b=.3), k(.28, 'flower_l', x=1.2, y=-.1, b=.2, mark='sniff'), k(.46, 'flower_l', x=1.6, y=-.4, b=-.3, w=.6, eye='O', mark='ah'), k(.64, 'flower_l', x=-.8, y=.9, b=1, w=.8, eye='@', mark='CHOO'), k(.84, eye='-')],
        [(.64, 'snap')], g='use', act=('sniff', 'flower'), when=['bloom>.5'], prefer=['curious'], say=["Smells of spring and bad decisions.", "Sneezed. Three blooms retired."])
    o.r('shout_up_the_chimney', 'Cupping a wing and shouting up at the chimney for someone to light the fire', 18, 'none',
        [k(.15, x=.1, y=-.7, b=-.2, r=1), k(.35, x=-.7, y=-1.4, b=-.7, w=.7, mark='LIGHT IT'), k(.58, x=-1, y=-1.7, b=-.9, w=1, l=1, mark='PLEASE'), k(.8, x=-.3, y=-.4, b=-.1, eye='-')],
        [(.58, 'laugh')], g='use', act=('shout', 'chimney'), far=True, say=["Asked the chimney nicely. Chimney is cold on principle.", "Smoke is a polite word for no."])
    # ---------------- play
    o.r('hide_in_the_flower_box', 'Trying to hide among the flowers, rustling, then popping up with a roar', 20, 'none',
        [k(.12, 'planter_r', x=-.2, y=.4, b=.2), k(.3, 'planter_r', x=-.9, y=1, b=.9, eye='O'), k(.5, 'flower_r', x=-1.1, y=.8, b=1.2, mark='shh'), k(.68, 'flower_r', x=1.4, y=-.7, b=-.7, w=1, l=1, r=1, mark='RAWR'), k(.88, eye='^')],
        [(.68, 'snap')], g='play', act=('hide', 'planter'), prefer=['young'])
    o.r('hop_up_on_the_mailbox', 'Hopping up on the mailbox lid and clucking about the view', 18, 'none',
        [k(.1, 'mail', x=.3, y=.2, b=.4), k(.28, 'mail_top', perch=1, x=.4, y=-.6, b=-.8, l=1, w=.8, mark='hup'), k(.5, 'mail_top', perch=1, x=-.2, y=-.8, b=.2, r=1, w=.4), k(.7, 'mail_top', perch=1, x=.6, y=-.3, b=-.5, w=.9, mark='cluck'), k(.88, 'mail', y=.6, b=.7, eye='^')],
        [], g='play', act=('hop', 'mail'), prefer=['happy', 'young'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
    o.r('weave_between_the_flower_boxes', 'Running a race between the two flower boxes, bill out, bumping neither', 16, 'none',
        [k(.08, 'planter_l', x=.8, y=.3, b=.1, w=.4), k(.28, 'lip_a', perch=1, x=1.1, y=.3, b=.4, l=1, w=1, mark='zoom'), k(.48, 'lip_b', perch=1, x=.2, y=.1, b=.6, r=1, w=.6), k(.68, 'planter_r', x=1.2, y=.4, b=.2, l=1, r=1, w=1), k(.9, 'planter_r', y=.2, eye='^')],
        [], g='play', act=('race', 'planter'), prefer=['happy'])
    o.r('seek_round_the_braces', 'Playing hide and seek round the braces, peeking out of each diagonal', 20, 'none',
        [k(.12, 'brace_l', x=-.3, y=.3, b=.2), k(.3, 'plank_l', x=1.1, y=-.3, b=.3, eye='O'), k(.48, 'brace_r', x=-.4, y=.4, b=.5), k(.66, 'plate_r', x=1.2, y=-.4, b=.3, eye='>', mark='boo'), k(.84, eye='^')],
        [], g='play', act=('seek', 'brace'), prefer=['curious'])
    o.r('drum_the_planks', 'Drumming a quick tune on the planks and the plates with his bill', 18, 'none',
        [k(.12, 'plank_l', x=.9, y=.8, b=.3, mark='tok'), k(.3, 'plate_l', x=.7, y=.3, b=-.3, l=1, mark='tak'), k(.5, 'plank_l', x=1.1, y=.9, b=.4, r=1, mark='tok tok'), k(.7, 'plate_l', x=.6, y=.3, b=-.2, l=1, mark='TAK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'plank'), prefer=['happy'], say=["Timber has a good beat. Plates keep time.", "Planks on the off-beat. Cottage taps its toe."])
    o.r('balance_on_the_door_foot', 'Balancing along the door foot with his wings out, one careful foot at a time', 18, 'none',
        [k(.12, 'lip_a', perch=1, x=.1, y=-.3, w=.7, l=1), k(.32, 'lip_a', perch=1, x=.7, y=.2, b=.7, r=1, w=1), k(.58, 'lip_b', perch=1, x=-.1, b=.4, l=1, w=1, mark='whoa'), k(.8, 'lip_b', perch=1, x=.4, y=.3, b=.1, w=.6), k(.92, eye='^')],
        [], g='play', act=('balance', 'lip'))
    o.r('climb_the_cottage_steps', 'Climbing the step lines one by one and jumping off at the top', 18, 'none',
        [k(.1, 'thresh', perch=1, x=.2, y=.1, b=.5), k(.28, 'step_b', perch=1, x=.4, y=-.5, b=-.6, r=1, w=.5, mark='hup'), k(.46, 'lip_b', perch=1, x=.8, y=-.8, b=-1, l=1, w=.8, mark='hup'), k(.64, 'lip_b', perch=1, x=-.3, y=.2, b=.4, w=.3), k(.82, 'thresh', x=.9, y=.6, b=1.2, l=1, r=1, w=1, mark='HAH'), k(.92, eye='^')],
        [], g='play', act=('climb', 'step'), prefer=['happy', 'young'])
    # ---------------- test
    o.r('tap_the_planks_for_hollow', 'Tapping the planks from the nails up to the braces to hear which are hollow', 18, 'none',
        [k(.1, 'plank_l', x=1.2, y=.7, b=.8, mark='tok'), k(.26, 'plate_l', x=.8, y=-.3, b=-.5, l=1, mark='tok'), k(.44, 'brace_l', x=.1, y=-.8, b=-.2, w=.8, eye='-'), k(.62, 'plank_l', x=1.7, y=1.1, b=1, r=1, mark='tonk'), k(.8, eye='^')],
        [], g='test', act=('tap', 'plank'))
    o.r('count_the_blooms', 'Touching each flower in both boxes and counting aloud, five, then six', 22, 'none',
        [k(.08, 'flower_l', x=1, y=-.3, b=.2, mark='1'), k(.26, 'planter_l', x=1.1, y=.8, b=.1, mark='2'), k(.46, 'flower_r', x=1.2, y=-.2, b=.5, l=1, mark='3'), k(.66, 'planter_r', x=1.3, y=.9, b=.8, r=1, mark='5?'), k(.84, x=-.6, y=-.4, w=.7, eye='-', mark='six')],
        [], g='test', act=('count', 'flower'), prefer=['curious'])
    o.r('weigh_the_mailbox', 'Leaning into the mailbox to weigh whether anything has arrived', 20, 'none',
        [k(.12, 'mail', x=.4, y=.5, b=.2, l=1), k(.3, 'mail', x=-.7, y=.7, b=.9, mark='hnn'), k(.5, 'plate_r', x=-.9, y=.6, b=1.1, r=1, mark='hnnf'), k(.7, 'mail', x=-.1, y=.3, b=.3, w=.5, eye='-', mark='light'), k(.88, eye='>')],
        [], g='test', act=('weigh', 'mail'))
    o.r('taste_a_petal', 'Nibbling a petal off the flower box and tasting it with a critic\'s face', 18, 'none',
        [k(.12, 'planter_l', x=.5, y=.6, b=.3), k(.3, 'flower_l', x=1.2, y=-.2, b=.2, mark='nm'), k(.5, x=.1, y=.2, eye='-', mark='chew'), k(.68, x=.3, y=.4, b=.2, eye='O'), k(.86, x=-.2, y=.1, eye='-', mark='soap')],
        [], g='test', act=('taste', 'flower'), say=["Petal. Perfume. Disappointment.", "Tastes like a bad idea with a ribbon."])
    o.r('test_a_brace_with_a_lean', 'Testing the right brace with a lean to see whether it takes his weight', 20, 'none',
        [k(.1, 'brace_r', x=.7, y=-.2, b=.5, l=1), k(.3, 'brace_r', x=-1.1, y=.4, b=.3, mark='hup'), k(.5, 'brace_r', x=-.5, y=1.2, b=1.5, r=1, mark='hnn'), k(.7, 'brace_r', x=.3, y=.6, b=-.2, w=.8, eye='-', mark='solid'), k(.88, eye='>')],
        [], g='test', act=('test', 'brace'), obj=[(.5, dict(shake=.1))])
    o.r('prod_the_right_sill', 'Prodding the right sill and glass with a twig to see if the window is shut', 20, 'twig',
        [k(.1, 'sill_r', reach=.5, x=.7, y=-.1, b=-.4, r=1), k(.3, 'window_r', reach=1, x=.2, y=-1.2, b=-.2, w=.2, mark='tk'), k(.5, 'sill_r', reach=.8, x=1, y=-.5, b=.4, mark='tk tk'), k(.72, 'window_r', reach=1, x=-.3, y=-.2, b=-.6), k(.9, x=.1, y=-.4, eye='-')],
        [], g='test', act=('prod', 'sill'))
    # ---------------- rest
    o.r('lean_on_the_warm_planks', 'Leaning his back against the sun-warmed planks and letting them hold him', 24, 'none',
        [k(.1, 'plank_l', x=.7, y=.3, b=.1, r=1), k(.3, 'brace_l', x=-1, y=.5, b=.5, eye='-'), k(.55, 'brace_l', x=-1.3, y=.6, b=.8, eye='-', mark='ahh'), k(.8, 'plank_l', x=-.7, y=.2, b=.6, l=1, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'plank'), when=['sun'], say=["Warm planks. Warm duck. Warm nothing else.", "Sun in the timber. Peace in the beak."])
    o.r('sit_on_the_cottage_step', 'Sitting on the lower step with his wings folded, watching the road not arrive', 24, 'none',
        [k(.12, 'step_a', perch=1, x=.5, y=-.4, b=.2, l=1), k(.3, 'step_a', perch=1, x=-.2, y=.3, b=.9, eye='-'), k(.6, 'step_a', perch=1, x=-.3, y=.4, b=1.3, eye='-', mark='...'), k(.85, 'step_a', perch=1, x=.1, y=-.2, b=.2, r=1, eye='^')],
        [], g='rest', act=('sit', 'step'))
    o.r('nap_on_the_mailbox', 'Taking a nap curled on the mailbox lid with his bill under a wing', 30, 'none',
        [k(.15, 'mail_top', perch=1, x=.3, y=.4, b=.7, r=1), k(.35, 'mail_top', perch=1, x=-.3, y=1.3, b=1, eye='-'), k(.6, 'mail_top', perch=1, x=-.4, y=1.5, b=1.5, eye='-', mark='zzz'), k(.85, 'mail_top', perch=1, x=.2, y=.2, b=.3, l=1, eye='^')],
        [(.6, 'hush')], g='rest', act=('nap', 'mail'), prefer=['tired'], ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'], say=["Mailbox nap. Post arrives, I stay.", "Slept on the lid. Dreamt of parcels."])
    o.r('warm_feet_on_the_door_foot', 'Warming one foot, then the other, on the sun-baked door foot', 22, 'none',
        [k(.12, 'lip_b', perch=1, x=-.1, y=.6, b=.6, l=1), k(.35, 'lip_b', perch=1, x=.5, y=.2, b=.1, l=1, eye='-', mark='ahh'), k(.6, 'lip_b', perch=1, x=.6, y=.3, b=.2, r=1, eye='^'), k(.85, 'lip_b', perch=1, x=-.2, y=.8, b=.7, eye='-')],
        [], g='rest', act=('warm', 'lip'), when=['sun'])
    o.r('guard_the_cottage_door', 'Standing guard at the cottage door, wings tucked, mail at his back', 24, 'none',
        [k(.12, 'chest', x=.6, y=-.2, b=.3, r=1), k(.34, 'thresh', perch=1, x=1.2, y=-1.1, b=-.8, w=.9, eye='>'), k(.58, 'thresh', perch=1, x=-.9, y=-.5, b=-.4, l=1, w=.5, mark='halt'), k(.86, 'thresh', perch=1, x=.3, y=.2, b=.2, w=.8, eye='-')],
        [], g='rest', act=('guard', 'door'), prefer=['lonely'])
    o.r('sulk_by_the_flower_box', 'Sulking by the flower box with his back to the cottage', 22, 'none',
        [k(.14, 'planter_r', x=.2, y=.3, b=.2), k(.34, 'planter_r', x=-.9, y=1.2, b=.9, eye='-', mark='hmph'), k(.58, 'flower_r', x=-.7, y=.8, b=1.1, r=1, eye='>'), k(.84, 'planter_r', x=-.4, y=.4, b=.4, l=1, eye='-')],
        [], g='rest', act=('sulk', 'planter'), prefer=['grumpy', 'sad'], say=["The flowers can hear me not talking.", "Petals aren't impressed. Neither am I."])
    # ---------------- weather
    o.r('chip_frost_off_the_sill', 'Chipping the frost off the left sill with the edge of his bill', 18, 'none',
        [k(.1, 'sill_l', x=.8, y=-.6, b=-.2, l=1), k(.28, 'sill_l', x=1.4, y=-.2, b=.6, mark='tk'), k(.48, 'window_l', x=1.5, y=-.7, b=.2, r=1, mark='tk'), k(.7, 'sill_l', x=.5, y=-.1, b=.3), k(.88, x=-.2, w=.4, eye='^')],
        [(.48, 'chip')], g='weather', act=('chip', 'sill'), when=['frost>.3'], ages=GROWN, say=["Sill de-iced. Curtain twitched. I was seen.", "Chip, chip, drip. Good morning, window."])
    o.r('huff_the_frosted_planter', 'Blowing warm breath along the frosted box rim until it drips', 18, 'none',
        [k(.12, 'planter_l', x=.5, y=.5, b=.4), k(.3, 'planter_l', x=1, y=.2, b=.5, mark='haah'), k(.5, 'flower_l', x=1.1, y=-.1, b=.3, w=.3, mark='haaah'), k(.72, 'planter_l', x=.7, y=.4, eye='^'), k(.88, eye='-')],
        [(.5, 'huff')], g='weather', act=('blow', 'planter'), when=['frost>.3'])
    o.r('kick_the_drift_off_the_step', 'Kicking the snow drift off the step in one long swipe and one short one', 18, 'none',
        [k(.12, 'step_a', x=.2, y=.7, b=.2, l=1), k(.3, 'step_a', x=.5, y=.9, b=.7, r=1, mark='fff'), k(.5, 'step_b', x=.3, y=1, b=.9, l=1, mark='FFF'), k(.72, 'lip_b', x=.2, y=.5, b=.4, r=1), k(.88, eye='^')],
        [(.5, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Step cleared. Toes iced. Even.", "Snow went flying. Duck stayed grounded."])
    o.r('scoop_snow_off_the_flower_box', 'Scooping the snow off the right flower box in wingfuls', 20, 'wing',
        [k(.12, 'planter_r', reach=.4, x=.1, y=.8, b=.3), k(.3, 'planter_r', reach=1, x=.6, y=1.1, b=.8, l=1, mark='fsh'), k(.5, 'flower_r', reach=1, x=.7, y=.2, b=.5, r=1, mark='fsh'), k(.7, 'planter_r', reach=.7, x=.4, y=.8, b=.3), k(.88, eye='^')],
        [(.5, 'scoop')], g='weather', act=('scoop', 'drift'), when=['drift>.5'], ages=GROWN)
    o.r('shake_off_the_rain_at_the_braces', 'Shaking the rain off his back with the brace at his shoulder', 18, 'none',
        [k(.12, 'brace_l', x=.1, y=.4, b=.1), k(.3, 'brace_l', x=-.3, y=.6, b=.8, w=1, mark='brrr'), k(.5, 'brace_l', x=.4, y=.9, b=.6, w=1, r=1), k(.7, 'brace_l', x=-.4, y=.4, b=.3, w=1, l=1), k(.88, eye='^')],
        [(.5, 'shake')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    o.r('shelter_beside_the_chest', 'Pressing against the door beside the chest shape to shelter from the rain', 34, 'none',
        [k(.1, 'lip_a', x=.8, y=.2, b=.9, r=1), k(.3, 'door_panel_l', x=-.6, y=1.1, b=.3, w=.4, eye='-', mark='drip'), k(.55, 'lip_a', x=-1.2, y=.4, b=1.5, w=.8, l=1, eye='>', mark='drip drip'), k(.8, 'door_panel_l', x=.2, y=.7, b=.8, w=.6, eye='^')],
        [], g='weather', act=('shelter', 'door'), when=['wet', 'storm'], say=["Rain rattles the shingles. I rattle nothing.", "Dry patch the size of a duck. Reserved."])
    # ---------------- mishap
    o.r('walk_into_the_clear_pane', 'Walking straight at the left window, thinking it was a gap, and meeting the glass', 16, 'none',
        [k(.12, x=.5, y=-.4, b=-.3), k(.3, x=1.2, y=-.8, b=.5, r=1, w=.3), k(.5, 'window_l', x=2.3, y=-.2, b=1.3, eye='@', mark='BOCK'), k(.72, x=-1.3, y=.9, b=.4, l=1, w=1, eye='O'), k(.9, y=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'window'), ages=GROWN, say=["Glass, with a curtain on it. Cheating.", "Pane stayed. Dignity left."])
    o.r('slip_on_the_wet_step', 'Slipping off the wet step with his feet racing ahead of the rest of him', 14, 'none',
        [k(.12, 'step_b', perch=1, x=.7, y=.2, b=.3, l=1), k(.3, 'step_b', perch=1, x=-.5, y=.9, b=-.7, r=1, w=.8, eye='O'), k(.5, 'thresh', x=1, y=.2, b=1.4, l=1, w=.4, mark='WHOA'), k(.7, 'thresh', x=.1, y=1.8, b=1.5, eye='@', mark='*splat*'), k(.88, y=.3, b=.6, eye='-')],
        [(.5, 'shake')], g='mishap', act=('slip', 'step'), when=['wet', 'obj_wetness>.3'], say=["Wet step, dry humour. Mostly dry.", "Down went the duck. Up went the sky."])
    o.r('wing_snagged_on_a_brace', 'Catching a wingtip on a brace end while turning and tearing loose', 18, 'wing',
        [k(.1, 'brace_l', reach=.4, x=1.1, y=.5, b=.2, r=1), k(.3, 'brace_l', reach=1, x=-.2, y=-.8, b=1, l=1, eye='O'), k(.5, 'plank_l', reach=.9, x=1.0, y=.4, b=-.3, mark='ack'), k(.7, y=1.1, b=.7, r=1, eye='@'), k(.88, x=.4, eye='-')],
        [(.5, 'crack')], g='mishap', act=('catch', 'brace'), ages=GROWN)
    o.r('kick_the_flower_box', 'Kicking the flower box by accident and hopping about on one foot', 16, 'none',
        [k(.12, 'planter_l', x=-.2, y=1.1, b=.7), k(.3, 'planter_l', x=1.3, y=.6, b=-.9, l=1, w=.9), k(.5, 'planter_l', x=.6, y=1.9, b=1.3, r=1, eye='@', mark='CLONK'), k(.7, x=-.8, y=.2, b=-.2, r=1, eye='O', mark='ow ow'), k(.88, y=.5, eye='-')],
        [(.5, 'scuff')], g='mishap', act=('kick', 'planter'), say=["Box unmoved. Toe now a philosophy.", "Kicked the flowers' home. They noticed."])
    # ---------------- show
    o.r('show_off_the_cottage', 'Showing off the cottage front with a sweeping wing like a very small estate agent', 20, 'wing',
        [k(.1, 'planter_l', reach=.6, x=-.2, y=.5, b=.4, r=1), k(.28, 'window_l', reach=1, x=.4, y=-1.2, b=-.8, mark='behold'), k(.48, 'chest', reach=.7, x=1, y=-.2, b=.1, l=1), k(.68, 'window_r', reach=1, x=-.3, y=-1.0, b=-.7, r=1, mark='roses'), k(.86, x=.3, y=.3, w=.5, eye='^')],
        [], g='show', act=('show', 'cottage'), say=["Quaint. Flowery. Post box included.", "Two windows, one duck, no offers."])
    o.r('sing_to_the_flower_boxes', 'Singing a ballad to the flower boxes with a flourish of wings', 22, 'none',
        [k(.14, 'planter_r', x=.7, y=-.1, b=.4), k(.34, 'flower_r', x=-.4, y=-1.4, b=-.7, w=.5, mark='laa'), k(.6, 'lip_a', perch=1, x=-1.1, y=-.6, b=.8, w=.8, l=1, eye='^', mark='LAAA'), k(.86, 'lip_a', perch=1, x=.5, y=.3, b=-.1, r=1, eye='-')],
        [], g='show', act=('sing', 'planter'), prefer=['happy'])
    o.r('dance_up_the_cottage_steps', 'Dancing a jig up the step and along the door foot to the post', 20, 'none',
        [k(.12, 'step_a', perch=1, x=.9, y=.1, b=-.4, l=1, w=.5), k(.3, 'lip_a', perch=1, x=-.6, y=-.5, b=.9, r=1, w=1), k(.5, 'lip_b', perch=1, x=.8, y=.4, b=-1.1, l=1, w=.8, mark='tada'), k(.7, 'step_b', perch=1, x=-.3, y=-.4, b=.6, r=1, w=.4), k(.88, 'thresh', perch=1, x=.3, eye='^')],
        [], g='show', act=('dance', 'step'), prefer=['happy'])
    o.r('argue_with_the_mailbox', 'Nudging the mailbox latch with his bill again and again, as if arguing with it', 22, 'none',
        [k(.12, 'mail', x=.8, y=.2, b=.3, l=1), k(.3, 'mail', x=1.2, y=.5, b=.6, mark='no'), k(.5, 'flower_r', x=1.4, y=.4, b=.8, r=1, mark='YES'), k(.7, 'mail', x=1.1, y=.6, b=.5, mark='no'), k(.88, x=-.4, y=.3, w=.7, eye='>')],
        [], g='show', act=('nudge', 'mail'), prefer=['grumpy'], say=["Mailbox refuses to explain. Mailbox is a coward.", "Won the argument. Latch has not conceded."])
    o.r('rake_the_leaf_heap', 'Using both feet to rake the blown leaves into a heap at the foot of the box', 20, 'none',
        [k(.12, 'planter_l', x=.2, y=.8, b=.3), k(.3, 'thresh', x=.7, y=1.3, b=.8, r=1, mark='shff'), k(.48, 'planter_l', x=.5, y=1.4, b=.9, l=1, mark='shff'), k(.68, 'thresh', x=.3, y=1, b=.6, r=1), k(.86, y=.2, w=.5, eye='^')],
        [(.48, 'rake')], g='weather', act=('rake', 'leaves'), when=['leaves>.3'])
    o.r('tap_the_mailbox_lid', 'Tapping the mailbox lid with his bill to hear if the post has come', 18, 'none',
        [k(.12, 'mail_top', x=.5, y=.2, b=.1, l=1), k(.3, 'mail_top', x=1.3, y=.6, b=.5, mark='tonk'), k(.46, 'planter_r', x=.1, y=-.2, b=-.4, w=.5), k(.62, 'mail_top', x=1.5, y=.7, b=.7, r=1, mark='tonk'), k(.8, eye='>')],
        [], g='test', act=('tap', 'mail'))
    o.r('perch_on_the_flower_box_rim', 'Perching on the left flower box rim to watch the road for visitors', 24, 'none',
        [k(.14, 'planter_l', perch=1, x=-.3, y=-.7, b=-.4, w=.6, r=1), k(.36, 'planter_l', perch=1, x=1, y=-.3, b=.3, eye='O'), k(.6, 'planter_l', perch=1, x=-.8, y=-.2, b=.6, w=.2, mark='hm'), k(.86, 'planter_l', perch=1, x=.3, y=.2, b=.1, l=1, eye='-')],
        [], g='rest', act=('perch', 'planter'), prefer=['curious'])
    o.emit()
    return o


if __name__ == '__main__':
    names = sys.argv[1:] or ['barn', 'shed', 'greenhouse', 'mud_hut', 'stone_house', 'wooden_cottage']
    for n in names:
        globals()[n]()
