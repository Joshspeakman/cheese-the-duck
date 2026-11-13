"""Wave 2a: barn, shed, greenhouse, mud_hut, stone_house, wooden_cottage. Every routine is hand-written.
Anchors are given as (column, row) of each drawing (printed with rep.py <id>) and converted to fractions by P()."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN
import os
if os.environ.get('LENIENT'):  # draft mode: list every refusal instead of stopping at the first
    _r = Obj.r
    def _lenient(self, *a, **kw):
        try:
            _r(self, *a, **kw)
        except AssertionError as e:
            print('REFUSED', e)
    Obj.r = _lenient

DIM = dict(barn=(108, 61), shed=(86, 52), greenhouse=(108, 57), mud_hut=(82, 47), stone_house=(96, 57), wooden_cottage=(98, 58))


def pm(oid):
    w, rows = DIM[oid]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))


def barn():
    # Drawing (108 x 62 cells, 9.3 px a row, standing line row 58): roof rows 2-34 (looked at), a left and right bay with a shuttered window each
    # (rows 36-46, sill row 47 at 102 px, glass cols 19-20 / 84-86), plank walls below with nail heads (rows 48, 52, 55) and ring knobs (rows 48, 56),
    # a big double door cols 36-73: two leaves, plank lines every 5 cols, a brace on each leaf running down to the middle (left leaf `\` cols 38-52,
    # right leaf `/` cols 69-55), seam at cols 53-54, ring knobs at rows 43 and 51 (cols 41, 60), nail heads on rows 41 48 55, a latch box
    # `.-|--.` cols 65-70 row 53 (47 px), door lip row 56 (19 px), step row 57 (9 px), threshold row 58. A planter with a leafy plant sits at far left.
    P = pm('barn')
    o = Obj('barn', 'placed',
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), warmth=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('warmth', 'rate', .0006, 'sun'), ('warmth', 'rate', -.0004, 'night')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], sweep=[('obj.dirt', 'add', -.15)], buff=[('obj.dirt', 'add', -.2)], dry=[('obj.wetness', 'add', -.3)],
                         flick=[('obj.wetness', 'add', -.2)], spray=[('obj.wetness', 'add', .15)], hammer=[('obj.condition', 'add', .2)], dent=[('obj.condition', 'add', -.15)],
                         scrape=[('frost', 'mul', .2)], melt=[('frost', 'mul', .4)], kick=[('drift', 'set', 0)], plough=[('drift', 'mul', .3)],
                         soak=[('warmth', 'add', -.25), ('need.energy', 'add', 2)], tidy=[('need.cleanliness', 'add', 1)], laugh=[('need.fun', 'add', 2)],
                         chat=[('need.social', 'add', 1)], scuff=[('obj.dirt', 'add', .12)]),
            anchors=dict(planter=P(11, 58), plank_l=P(19, 54), stud_l=P(16, 52), stud_l2=P(26, 52), ring_l=P(15, 56), ring_l2=P(28, 56), jamb_l=P(34, 54),
                         brace_l=P(50, 53), knob_l=P(41, 51), seam=P(53, 52), brace_r=P(57, 53), latch=P(67, 53), knob_r=P(60, 51), stud_d1=P(41, 55),
                         stud_d2=P(65, 55), jamb_r=P(73, 54), lip_a=P(40, 56, 'surface'), lip_b=P(68, 56, 'surface'), step_a=P(44, 57, 'surface'),
                         step_b=P(62, 57, 'surface'), thresh=P(54, 58, 'surface'), plank_r=P(84, 54), stud_r=P(86, 52), ring_r=P(80, 56), ring_r2=P(93, 56),
                         pane_l=P(19, 42), sill_r=P(86, 47)))
    # ---------------- care
    o.r('scrub_boards', 'Scrubbing the left boards with a wing until the stains come up', 20, 'wing',
        [k(.1, 'plank_l', reach=.6, x=.5, y=.7, b=.2), k(.24, 'plank_l', reach=1, x=.8, y=1, b=.6, l=1), k(.38, 'stud_l', reach=1, x=.9, y=.7, b=.2, r=1, mark='skrk'), k(.54, 'plank_l', reach=1, x=.9, y=1.1, b=.8, l=1, mark='skrk'), k(.72, 'ring_l', reach=1, x=.6, y=.6, b=.3, r=1), k(.9, eye='^')],
        [(.54, 'scrub')], g='care', act=('scrub', 'boards'), when=['obj_dirt>.3'], prefer=['grown'],
        say=["Barn was filthy. Now it is only my fault.", "Boards clean. Wing filthy. Fair trade."])
    o.r('sweep_step', 'Sweeping the step and the door lip with the flat of a wing', 16, 'wing',
        [k(.12, 'step_a', reach=.5, x=.3, y=.6), k(.3, 'step_a', reach=1, x=.5, y=.9, b=.3, l=1), k(.55, 'lip_a', reach=1, x=.6, y=.8, r=1), k(.75, 'lip_a', reach=.6, x=.3, y=.4), k(.9, eye='-')],
        [(.55, 'sweep')], g='care', act=('sweep', 'step'), when=['obj_dirt>.3'])
    o.r('mop_jambs', 'Mopping both door jambs dry with his breast and a lot of grunting', 20, 'none',
        [k(.12, 'jamb_l', x=.4, y=.4), k(.3, 'jamb_l', x=.9, y=.5, b=.4, mark='hff'), k(.5, 'jamb_l', x=1, y=.4, b=.6), k(.72, 'jamb_r', x=.9, y=.5, b=.4, mark='hff'), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'jambs'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.2)), (.72, dict(shake=.2))])
    o.r('hammer_stud', 'Hammering a loose stud head flat with his bill, three taps and a verdict', 18, 'none',
        [k(.1, x=.7, y=.9, b=.3), k(.24, 'stud_l2', x=1.2, y=1.8, b=.9, l=1, mark='tak'), k(.4, x=.3, y=.6, b=-.3), k(.56, 'stud_l2', x=1.3, y=2, b=1, r=1, mark='tak'), k(.7, x=.2, y=.5, b=-.2, w=.4), k(.82, 'stud_l2', x=1.4, y=2.1, b=1.1, mark='TAK'), k(.94, eye='^')],
        [(.82, 'hammer')], g='care', act=('mend', 'stud'), when=['obj_condition<.6'], say=["Stud flat. Barn holds. Send thanks in bread.", "Hammered it with my face. Worked."])
    o.r('comb_planter', 'Combing the planter leaves straight with his bill, one stem at a time', 18, 'none',
        [k(.12, 'planter', x=.5, y=.8, b=.3), k(.3, 'planter', x=.8, y=1.3, b=.5, mark='frp'), k(.5, 'planter', x=.9, y=1.5, b=.8, l=1), k(.7, 'planter', x=.7, y=1.2, b=.5, r=1), k(.88, x=.1, eye='^')],
        [(.5, 'tidy')], g='care', act=('groom', 'planter'), prefer=['curious'], say=["Neat leaves. Barn looks almost loved.", "Combed a plant. Dignity: intact. Mostly."])
    o.r('wipe_latch', 'Wiping the latch box with the tip of a wing, finger-trim and all', 14, 'wing',
        [k(.15, 'latch', reach=.5, x=.3, y=.2), k(.35, 'latch', reach=1, x=.5, y=.4, mark='shk'), k(.55, 'latch', reach=1, x=.6, y=.4, b=.2, mark='shk'), k(.8, eye='-')],
        [(.55, 'buff')], g='care', act=('wipe', 'latch'), when=['obj_dirt>.5'])
    # ---------------- use
    o.r('knock_leaf', 'Knocking at the left leaf, then waiting to be told to come in', 20, 'none',
        [k(.12, 'stud_d1', x=1, y=.8, b=.3, mark='knock'), k(.3, 'stud_d1', x=1, y=.9, b=.4, l=1, mark='knock'), k(.5, x=-.6, y=-.4, w=.4, eye='O', mark='Hello?'), k(.7, x=.2, y=.2, b=.8, r=1, eye='-', mark='...'), k(.88, eye='^')],
        [], g='use', act=('knock', 'leaf'), prefer=['lonely'], say=["Barn said nothing. Rude. Also barns.", "Knocked twice. The cows can wait."])
    o.r('tug_latch', 'Tugging the latch box with his bill until the whole door rattles', 16, 'none',
        [k(.12, 'latch', x=.7, y=.6), k(.3, 'latch', x=1.2, y=.8, b=.5, mark='hup'), k(.5, 'latch', x=1.4, y=1, b=.8, l=1, r=1, mark='RRRK'), k(.72, x=-.4, y=-.2, w=.6, eye='-'), k(.88, eye='^')],
        [], g='use', act=('tug', 'latch'), prefer=['curious'], obj=[(.3, dict(shake=.3)), (.5, dict(shake=.8)), (.72, dict(shake=.2))])
    o.r('shoulder_leaf', 'Putting a shoulder to the right leaf to see if the whole door gives', 22, 'none',
        [k(.08, x=-.3, y=.1, b=-.2), k(.26, 'stud_d2', x=1.3, y=.9, b=1.2, l=1, mark='hnnh'), k(.46, 'stud_d2', x=1.5, y=1.1, b=1.6, r=1, mark='HNNNH'), k(.62, 'stud_d2', x=1.2, y=.6, b=.8), k(.78, x=-.8, y=-.5, b=-.4, w=.9, eye='-'), k(.92, eye='^')],
        [], g='use', act=('push', 'leaf'), ages=GROWN, obj=[(.3, dict(sway=.2)), (.5, dict(shake=.5)), (.7, dict(sway=0))],
        say=["Door won. I will be back. With a bigger shoulder.", "It did not budge. Neither did my pride."])
    o.r('hang_off_ring', 'Hanging off the far right ring knob with his whole weight', 18, 'none',
        [k(.12, 'ring_r2', x=.5, y=.9, b=.2), k(.3, 'ring_r2', x=1.2, y=1.2, b=.8, mark='hup'), k(.5, 'ring_r2', x=1.3, y=1.4, b=1.2, l=1, r=1, w=.7), k(.7, 'ring_r2', x=1.2, y=1, b=.9, eye='>'), k(.88, y=.2, eye='^')],
        [], g='use', act=('pull', 'ring'), ages=GROWN, obj=[(.5, dict(sway=.3))], say=["Ring held. I am extremely heavy. Know it.", "Hung there. Barn took the weight. Ring took offence."])
    o.r('squint_at_seam', 'Pushing his head up to the seam between the leaves and squinting for movement', 20, 'none',
        [k(.15, x=.4, y=.2), k(.3, 'seam', x=1.4, y=-.2, b=.2, eye='O'), k(.5, 'seam', x=1.5, y=-.3, b=.3, eye='>', mark='hm'), k(.7, 'seam', x=1.5, y=-.2, b=.3, eye='-'), k(.88, x=.2, eye='-')],
        [], g='use', act=('peer', 'seam'), shown='head', prefer=['curious'])
    o.r('holler_for_farmer', 'Cupping a wing at the left leaf and hollering for a farmer who is not there', 20, 'wing',
        [k(.1, 'knob_l', reach=.6, x=.5, y=-.5, b=.3), k(.3, 'knob_l', reach=1, x=1, y=-1.1, b=-.5, mark='OI'), k(.5, 'brace_l', reach=1, x=1.2, y=-1.3, b=-.7, l=1, eye='O', mark='OOI!'), k(.7, 'brace_l', reach=.7, x=-.4, y=.5, b=.6, r=1, eye='-', mark='...'), k(.9, eye='>')],
        [], g='use', act=('shout', 'knob'), prefer=['lonely'], say=["Farmer is out. Barn is mine. Good arrangement.", "Nobody answered. I will call that approval."])
    # ---------------- play
    o.r('race_the_rings', 'Sprinting the length of the front and rapping every ring knob as he goes', 18, 'none',
        [k(.1, 'ring_l', x=.6, y=1.2, b=.5, mark='tk'), k(.3, 'ring_l2', x=.7, y=1.3, b=.4, l=1, mark='tk'), k(.5, 'ring_r', x=.8, y=1.2, b=.5, r=1, mark='tk'), k(.7, 'ring_r2', x=.9, y=1.3, b=.4, l=1, mark='tk'), k(.88, x=.2, w=.7, eye='^')],
        [(.7, 'laugh')], g='play', act=('race', 'rings'), prefer=['young', 'happy'])
    o.r('walk_the_lip', 'Walking the door lip end to end with his wings out like a plank walker', 20, 'none',
        [k(.12, 'lip_a', perch=1, y=-.2, w=.8), k(.3, 'lip_a', perch=1, y=.2, b=.3, w=1, l=1), k(.55, 'lip_b', perch=1, y=.2, b=.2, w=1, r=1), k(.78, 'lip_b', perch=1, y=-.3, b=-.4, w=.7, eye='^')],
        [], g='play', act=('balance', 'lip'), prefer=['young'])
    o.r('bounce_on_step', 'Bouncing on the step as if it were a springboard, then off', 16, 'none',
        [k(.15, 'step_a', perch=1, y=-.3, b=-.6, w=.5), k(.3, 'step_a', perch=1, y=.3, b=.8, l=1), k(.45, 'step_b', perch=1, y=-.6, b=-.9, w=1), k(.62, 'step_b', perch=1, y=.3, b=.8, r=1), k(.8, y=-.4, b=-.8, w=.8, eye='^')],
        [], g='play', act=('hop', 'step'), prefer=['young', 'happy'])
    o.r('flatten_at_jamb', 'Flattening himself against the left jamb and bursting out at nothing', 20, 'none',
        [k(.1, 'jamb_l', x=-.6, y=.5, b=.7), k(.3, 'jamb_l', x=-.7, y=1, b=1.2, l=1, eye='-'), k(.5, 'jamb_l', x=-.7, y=1, b=1.3, r=1, eye='-', mark='...'), k(.64, x=1.3, y=-1.1, b=-1.1, w=1, eye='O', mark='BOO'), k(.8, x=.3, y=.6, b=.3, eye='^')],
        [], g='play', act=('hide', 'jamb'), prefer=['young'], say=["Boo. Barn did not flinch. Damn.", "Jumped out. Jamb unmoved. Tough crowd."])
    o.r('peek_round_right_jamb', 'Creeping along the lip and peeking round the right jamb with one eye', 20, 'none',
        [k(.12, 'lip_a', x=.2, y=.3, b=.2), k(.35, 'lip_b', x=.2, y=.4, b=.4, l=1), k(.6, 'jamb_r', x=.9, y=-.3, b=.3, eye='O'), k(.8, 'jamb_r', x=1.1, y=-.4, b=.4, eye='>', mark='psst'), k(.92, eye='-')],
        [], g='play', act=('seek', 'jamb'), prefer=['curious'])
    o.r('drum_right_boards', 'Drumming a march along the right boards with his bill', 18, 'none',
        [k(.12, 'plank_r', x=1, y=.6, b=.3, mark='tok'), k(.3, 'stud_r', x=.8, y=.2, b=-.2, l=1, mark='tok'), k(.5, 'plank_r', x=1.1, y=.7, b=.4, r=1, mark='tok tok'), k(.7, 'stud_r', x=.8, y=.2, b=-.2, l=1, mark='TOK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'boards'), prefer=['happy'], say=["Barn has a good beat. Poor tempo discipline.", "Planks on the downbeat. Studs on the off."])
    # ---------------- test
    o.r('tap_for_hollow', 'Tapping the right boards with his bill to hear where they sound hollow', 18, 'none',
        [k(.1, 'plank_r', x=1.4, y=.9, b=.6, mark='tok'), k(.26, 'stud_r', x=.9, y=-.5, b=-.5, l=1, mark='tok'), k(.44, 'plank_r', x=.2, y=-.8, b=-.1, w=.8, eye='-'), k(.62, 'ring_r', x=1.5, y=1.1, b=.8, r=1, mark='tonk'), k(.8, eye='^')],
        [], g='test', act=('tap', 'wall'))
    o.r('count_studs', 'Touching each stud head along the left wall and counting under his breath', 22, 'none',
        [k(.08, 'stud_l', x=1.1, y=1.7, b=.9, mark='1'), k(.26, 'stud_l2', x=1.3, y=1.5, b=.2, r=1, mark='2'), k(.46, 'stud_d1', x=.9, y=1.3, b=1.1, l=1, mark='3'), k(.66, 'stud_d2', x=1.4, y=1.8, b=.5, r=1, mark='4'), k(.86, x=-.7, y=-.5, w=.7, eye='-', mark='four')],
        [], g='test', act=('count', 'studs'), prefer=['curious'])
    o.r('hang_on_left_ring', 'Hanging off the left ring knob to weigh how heavy the leaf feels', 18, 'none',
        [k(.15, 'ring_l2', x=.5, y=.9), k(.35, 'ring_l2', x=1.2, y=1.3, b=1, l=1, mark='hnn'), k(.55, 'ring_l2', x=1.3, y=1.4, b=1.1, r=1, eye='>'), k(.78, x=-.3, y=-.2, w=.5, eye='-', mark='heavy')],
        [], g='test', act=('weigh', 'ring'), ages=GROWN)
    o.r('measure_against_jamb', 'Standing back to the right jamb to see how much of him reaches the top', 20, 'none',
        [k(.12, 'jamb_r', x=-.4, y=.3, b=.2), k(.3, 'jamb_r', x=-.5, y=-.8, b=-.5, w=.8, mark='...'), k(.55, 'jamb_r', x=1.2, y=1.2, b=.9, eye='O'), k(.75, 'jamb_r', x=-.3, y=.2, b=.3, l=1, eye='-', mark='short'), k(.9, eye='>')],
        [], g='test', act=('measure', 'jamb'), prefer=['young'], say=["Door is tall. I am a duck. Nobody lied.", "Reached the middle of the jamb. Statistically fine."])
    o.r('compare_braces', 'Following the left brace down with his bill, then the right brace to see which is longer', 22, 'none',
        [k(.12, 'brace_l', x=.8, y=.4), k(.3, 'brace_l', x=1.1, y=.8, b=.4, mark='hm'), k(.5, 'brace_r', x=1.1, y=.8, b=.4, l=1), k(.7, 'brace_r', x=.9, y=.5, b=.2, eye='-', mark='same'), k(.88, eye='>')],
        [], g='test', act=('compare', 'braces'), prefer=['curious'])
    o.r('prod_pane', 'Prodding the left window pane and then the right sill with a twig to make sure both are shut', 20, 'twig',
        [k(.15, 'pane_l', reach=.6, x=.3, y=-.2), k(.35, 'pane_l', reach=1, x=.5, y=-.4, w=.4, mark='tk'), k(.55, 'sill_r', reach=1, x=.6, y=-.5, mark='tk tk'), k(.8, x=-.2, y=-.1, eye='-')],
        [], g='test', act=('prod', 'pane'))
    # ---------------- rest
    o.r('lean_warm_boards', 'Leaning a shoulder against the sun-warmed left boards and soaking it up', 24, 'none',
        [k(.12, 'plank_l', x=.2, y=.3, b=.2), k(.3, 'plank_l', x=-.3, y=.5, b=.5, eye='-'), k(.55, 'plank_l', x=-.4, y=.6, b=.7, eye='-', mark='ahh'), k(.8, 'plank_l', x=-.3, y=.4, b=.5, eye='^')],
        [(.55, 'soak')], g='rest', act=('lean', 'boards'), when=['warmth>.3', 'sun'], say=["Warm boards. This is the correct use of a barn.", "Sun in the planks. Heat in my shoulder. Peace."])
    o.r('lean_on_right_jamb', 'Propping himself against the far right wall with his arms folded, looking unimpressed', 20, 'none',
        [k(.12, 'plank_r', x=.3, y=.3), k(.35, 'plank_r', x=-.2, y=.9, b=.5, eye='-'), k(.6, 'ring_r', x=-.3, y=.9, b=.9, l=1, eye='-', mark='hm'), k(.82, 'ring_r', x=-.2, y=.4, b=.4, eye='>')],
        [], g='rest', act=('lean', 'wall'), prefer=['grumpy'])
    o.r('sit_on_step', 'Sitting on the step with his feet tucked, watching the yard go nowhere', 24, 'none',
        [k(.12, 'step_a', perch=1, y=-.2, b=.2), k(.3, 'step_a', perch=1, y=.4, b=.9, eye='-'), k(.6, 'step_a', perch=1, y=.5, b=1, eye='-', mark='...'), k(.85, 'step_a', perch=1, y=.1, b=.4, eye='^')],
        [], g='rest', act=('sit', 'step'), say=["Yard did nothing. Fantastic yard.", "Sat. Looked. Left with my opinions intact."])
    o.r('sulk_at_leaf', 'Turning his back to the big door and refusing to look at it', 20, 'none',
        [k(.15, 'thresh', x=.2, y=.2), k(.35, 'thresh', x=-.7, y=.9, b=.6, eye='-', mark='hmph'), k(.6, 'thresh', x=-.8, y=1, b=.9, l=1, eye='>'), k(.85, 'thresh', x=-.5, y=.3, b=.3, eye='-')],
        [], g='rest', act=('sulk', 'leaf'), prefer=['grumpy', 'sad'], say=["Not looking at you. Door. Barn. Whoever.", "Sulking is a full-time job. Pays nothing."])
    o.r('wait_at_threshold', 'Waiting at the door lip for someone with a key who is clearly not coming', 26, 'none',
        [k(.15, 'lip_b', y=.2), k(.35, 'lip_b', x=.3, y=.3, b=.3, l=1, eye='-'), k(.6, 'lip_a', x=-.2, y=.3, b=.2, r=1, eye='>', mark='...'), k(.85, 'lip_a', x=.2, y=.2, eye='-')],
        [], g='rest', act=('wait', 'lip'), prefer=['lonely'])
    o.r('warm_feet_on_lip', 'Warming one foot, then the other, against the sun-baked door lip', 22, 'none',
        [k(.12, 'lip_b', x=.2, y=.4, l=1), k(.35, 'lip_b', x=.3, y=.6, b=.3, l=1, eye='-', mark='ahh'), k(.6, 'lip_b', x=.3, y=.6, b=.3, r=1, eye='^'), k(.85, 'lip_b', x=.1, y=.3, eye='-')],
        [(.6, 'chat')], g='rest', act=('warm', 'lip'), when=['warmth>.3', 'sun'])
    # ---------------- weather
    o.r('scrape_frost_latch', 'Scraping the frost off the latch box with the edge of his bill', 18, 'none',
        [k(.12, 'latch', x=.5, y=.6), k(.3, 'latch', x=1.2, y=.8, b=.4, mark='skrk'), k(.5, 'latch', x=1.3, y=.9, b=.5, l=1, mark='skrk'), k(.72, 'latch', x=1.1, y=.6, r=1), k(.88, eye='^')],
        [(.5, 'scrape')], g='weather', act=('scrape', 'latch'), when=['frost>.3'], say=["Latch iced over. Chipped it free. Hero stuff.", "Frost off the latch. Cold in the nostrils."])
    o.r('breathe_on_ring', 'Huffing warm breath at the iced ring knob until the frost goes', 18, 'none',
        [k(.12, 'knob_r', x=.5, y=.2), k(.3, 'knob_r', x=1, y=-.2, b=.2, mark='haah'), k(.5, 'knob_r', x=1.1, y=-.3, b=.3, w=.3, mark='haaah'), k(.72, 'knob_r', x=.7, y=0, eye='^'), k(.88, eye='-')],
        [(.5, 'melt')], g='weather', act=('blow', 'ring'), when=['frost>.3'])
    o.r('kick_drift_off_step', 'Kicking the snow drift off the step in two big sweeps of his foot', 18, 'none',
        [k(.12, 'step_a', x=.2, y=.4, b=.3), k(.3, 'step_a', x=.3, y=.7, b=.6, l=1, mark='fff'), k(.5, 'step_a', x=.3, y=.7, b=.7, r=1, mark='FFF'), k(.72, 'step_b', x=.2, y=.4, b=.3, l=1), k(.88, eye='^')],
        [(.5, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Snow kicked. Step visible. Feet colder. Worth it.", "Drift gone. Dignity airborne."])
    o.r('plough_the_threshold', 'Ploughing a trench along the threshold, chest first, drift piled up before him', 20, 'none',
        [k(.12, 'thresh', x=.4, y=.8, b=.6), k(.3, 'thresh', x=.7, y=1.2, b=1, mark='hrrn'), k(.5, 'thresh', x=.8, y=1.3, b=1.1, l=1, r=1), k(.72, 'thresh', x=.5, y=.8, b=.7), k(.88, y=.2, w=.5, eye='^')],
        [(.5, 'plough')], g='weather', act=('push', 'drift'), when=['drift>.5'])
    o.r('peck_off_beads', 'Pecking the beads of rain off the lower left boards one at a time', 20, 'none',
        [k(.12, 'plank_l', x=.6, y=.9, b=.3), k(.3, 'plank_l', x=1.1, y=1.4, b=.5, mark='tp'), k(.5, 'ring_l', x=1.2, y=1.5, b=.7, l=1, mark='tp'), k(.7, 'plank_l', x=1.1, y=1.3, b=.5, r=1, mark='tp'), k(.88, eye='^')],
        [(.5, 'flick')], g='weather', act=('peck', 'beads'), when=['obj_wetness>.3'])
    o.r('shake_dry_at_wall', 'Shaking the rain off his back with the lower boards at his shoulder', 18, 'none',
        [k(.12, 'plank_l', x=.2, y=.3, b=.2), k(.3, 'plank_l', x=-.2, y=.7, b=.6, w=1, mark='brrr'), k(.5, 'plank_l', x=.2, y=.7, b=.8, w=1, l=1), k(.7, 'plank_l', x=-.2, y=.5, b=.5, w=1, r=1), k(.88, eye='^')],
        [(.5, 'spray')], g='weather', act=('shake', 'feathers'), when=['wet', 'obj_wetness<.6'])
    # ---------------- mishap
    o.r('skid_on_frost', 'Skidding along the frosted threshold with both feet going different ways', 14, 'none',
        [k(.15, 'thresh', y=.2, b=.2), k(.3, 'thresh', x=.5, y=.4, b=-.2, l=1, w=.7, eye='O'), k(.5, 'thresh', x=-.5, y=.9, b=.9, r=1, w=1, mark='WHOA'), k(.7, 'thresh', y=1.3, b=1.4, eye='@', mark='*thud*'), k(.88, y=.4, b=.4, eye='-')],
        [(.5, 'scrape')], g='mishap', act=('slip', 'threshold'), when=['frost>.5'], say=["Frost is a liar. A lying, white liar.", "Feet went north. Duck went south. Barn watched."])
    o.r('bill_frozen_to_ring', 'Licking the iced ring knob, freezing there, and tearing himself free', 24, 'none',
        [k(.15, 'ring_l', x=.7, y=.8, b=.3), k(.3, 'ring_l', x=1.4, y=1.1, b=.6, eye='O', mark='mm'), k(.5, 'ring_l', x=1.5, y=1.2, b=.8, l=1, r=1, eye='@', mark='mmf!'), k(.7, 'ring_l', x=1.6, y=1.3, b=1, w=1, mark='POP'), k(.88, x=-.2, y=.6, eye='>')],
        [(.7, 'melt')], g='mishap', act=('stuck', 'ring'), when=['frost>.5'], say=["Ring tastes like regret. And iron. Mostly regret.", "Frozen to a door ring. Bill is not for kissing."])
    o.r('walk_into_the_leaf', 'Marching confidently at the left leaf and meeting it', 16, 'none',
        [k(.15, y=.1, b=.1), k(.35, x=.6, y=.2, b=.3, l=1), k(.55, 'brace_l', x=1.5, y=.6, b=.8, eye='@', mark='BONK'), k(.75, x=-.8, y=.4, b=.5, w=.6, eye='O'), k(.9, eye='-')],
        [], g='mishap', act=('walk_into', 'leaf'), say=["Door was closed. Door has always been closed.", "Walked straight into it. It had a point."])
    o.r('peck_stud_too_hard', 'Whacking a stud head so hard the board creaks and the stud skews', 14, 'none',
        [k(.15, 'stud_r', x=.4, y=.4), k(.3, 'stud_r', x=1.4, y=1.7, b=.7, mark='TOK'), k(.5, 'stud_r', x=1.5, y=1.8, b=.9, eye='@', mark='CRK'), k(.72, x=-.4, y=.4, w=.6, eye='O'), k(.88, eye='-')],
        [(.5, 'dent')], g='mishap', act=('peck', 'stud'), prefer=['grumpy'], say=["Cracked it. Barn will live. I am less sure.", "Hit it harder than the stud deserved."])
    o.r('stamp_on_step', 'Stamping up and down on the step after the knock got no answer', 16, 'none',
        [k(.15, 'step_b', perch=1, y=.4, b=.4, l=1), k(.3, 'step_b', perch=1, y=.5, b=.7, r=1, mark='STOMP'), k(.5, 'step_b', perch=1, y=.5, b=.8, l=1, mark='STOMP'), k(.72, 'step_b', perch=1, y=.3, w=.7, eye='>'), k(.88, eye='-')],
        [(.5, 'scuff')], g='mishap', act=('stamp', 'step'), prefer=['grumpy'])
    o.r('catch_wing_on_stud', 'Catching a wingtip on a stud while turning and spinning round to get free', 18, 'wing',
        [k(.15, 'stud_l2', reach=.5, x=.4, y=.3), k(.35, 'stud_l2', reach=1, x=-.3, y=.4, b=.4, eye='O'), k(.55, 'stud_l2', reach=.6, x=.4, y=.6, b=.7, l=1, r=1, mark='ack'), k(.75, y=.8, b=.9, eye='@'), k(.9, eye='-')],
        [], g='mishap', act=('catch', 'stud'))
    # ---------------- show
    o.r('pose_in_doorway', 'Striking a proud farmer pose in front of the big door, wings on hips', 20, 'none',
        [k(.15, 'step_b', y=.1, b=.1), k(.35, 'step_b', x=-.3, y=-.5, b=.8, w=.6, eye='^'), k(.6, 'step_b', x=1, y=-.7, b=.2, w=.9, l=1, eye='-', mark='ahem'), k(.85, 'step_b', x=-.3, y=.9, b=.9, w=.6, eye='^')],
        [], g='show', act=('pose', 'doors'), prefer=['happy'], say=["Farm owner. Do not ask what farm.", "Posed. Nobody photographed it. Their loss."])
    o.r('bow_to_the_barn', 'Bowing very low to the big door as if it were royalty', 18, 'none',
        [k(.15, 'brace_r', y=.2), k(.35, 'brace_r', x=.4, y=1.2, b=.9, w=.6, eye='-'), k(.6, 'brace_r', x=.5, y=1.6, b=1.2, w=.8, mark='milord'), k(.85, 'brace_r', y=.2, eye='^')],
        [], g='show', act=('bow', 'doors'))
    o.r('present_the_barn', 'Sweeping a wing along the whole front of the barn like an estate agent', 20, 'wing',
        [k(.15, 'brace_l', reach=.5, x=.2, y=-.2), k(.35, 'brace_l', reach=1, x=.3, y=-.6, b=-.2, mark='behold'), k(.6, 'brace_r', reach=1, x=.4, y=-.7, b=-.3, mark='charming'), k(.85, x=-.1, y=-.2, eye='^')],
        [], g='show', act=('present', 'front'), say=["Spacious. Lots of potential. No viewings.", "Two doors, one planter, zero offers."])
    o.r('argue_with_latch', 'Arguing with the far right ring knob, pecking it for every point', 20, 'none',
        [k(.12, 'ring_r', x=.6, y=.6, b=.2), k(.3, 'ring_r', x=1, y=.9, b=.4, mark='no'), k(.5, 'ring_r', x=1.2, y=1, b=.6, l=1, mark='YES'), k(.7, 'ring_r', x=1, y=.8, b=.4, r=1, mark='no'), k(.88, x=-.3, y=.2, w=.7, eye='>')],
        [], g='show', act=('argue', 'ring'), prefer=['grumpy'], say=["Ring refuses to explain. Ring is a coward.", "Won the argument. Ring has not conceded."])
    o.r('sing_to_the_planter', 'Serenading the planter with a ballad and wing flourishes', 22, 'none',
        [k(.15, 'planter', x=.2, y=-.2), k(.35, 'planter', x=-.2, y=-.8, b=.8, w=.8, mark='laa'), k(.6, 'planter', x=1.2, y=-.9, b=-.4, w=1, l=1, eye='^', mark='LAAA'), k(.85, 'planter', x=-.1, y=-.3, eye='-')],
        [], g='show', act=('sing', 'planter'), prefer=['happy'])
    o.r('dance_on_step', 'Dancing a jig down from the door lip, over the step and out to the threshold', 20, 'none',
        [k(.12, 'lip_a', perch=1, y=-.3, b=-.6, l=1, w=.6), k(.3, 'step_a', perch=1, y=.3, b=.5, r=1, w=1), k(.5, 'thresh', perch=1, y=-.4, b=-.7, l=1, w=1, mark='tada'), k(.7, 'step_b', perch=1, y=.4, b=.6, r=1, w=.8), k(.88, eye='^')],
        [], g='show', act=('dance', 'lip'), prefer=['happy'])
    return o


def shed():
    # Drawing (86 x 53 cells, 9.3 px a row, standing line row 49): shingled roof rows 20-27 and eave beam rows 25-26 (looked at), left window cols 11-24
    # (shutters `//`, glass cols 14-20, rail row 35 at 130 px, sill row 41 at 74 px), plank wall below with studs row 42 (65 px) and a ring knob row 45 (37 px),
    # door cols 28-53 (jambs `|||`, panel rails rows 31 36 40 43, latch `.--|-|` row 44 at 47 px, foot strip row 46, lip row 47 at 19 px, step row 48 at 9 px,
    # threshold row 49), right wall cols 54-65 with studs (rows 35 42 49) and ring knobs (rows 29 37 45), a T-headed tool at col 59 row 38 (102 px), a
    # slanting handle and a J hook (col 65 row 40, 84 px), and a barrel cols 66-80 (rim row 43 at 56 px, belly curve row 45, hoop row 46 at 28 px, staves below).
    P = pm('shed')
    o = Obj('shed', 'placed',
            fields=dict(leaves=(0, 0, 1), drift=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('leaves', 'rate', .002, 'fall'), ('leaves', 'rate', -.001, 'windy'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], buff=[('obj.dirt', 'add', -.2)], brush=[('obj.dirt', 'add', -.15)], dry=[('obj.wetness', 'add', -.3)],
                         spray=[('obj.wetness', 'add', .12)], seat=[('obj.condition', 'add', .2)], dent=[('obj.condition', 'add', -.15)],
                         rake=[('leaves', 'mul', .3)], scoop=[('drift', 'set', 0)], flick=[('drift', 'mul', .4)], clear=[('frost', 'mul', .2)], peep=[('frost', 'mul', .5)],
                         scuff=[('obj.dirt', 'add', .12)], tidy=[('need.cleanliness', 'add', 1)], laugh=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(plank_l=P(13, 46), stud_l=P(16, 42), stud_l2=P(26, 42), ring_l=P(15, 45), sill_l=P(17, 41), glass_l=P(17, 38), jamb_l=P(29, 44),
                         panel_rail=P(40, 43), latch=P(49, 44), door_foot=P(44, 45), lip_a=P(34, 47, 'surface'), lip_b=P(47, 47, 'surface'), step_a=P(35, 48, 'surface'),
                         step_b=P(47, 48, 'surface'), thresh=P(40, 49, 'surface'), plank_r=P(58, 46), stud_r=P(61, 42), ring_r=P(54, 45), tool_t=P(59, 38),
                         hook_j=P(65, 40), barrel_rim=P(73, 43, 'surface'), barrel_hoop=P(73, 46), barrel_stave=P(69, 48), barrel_belly=P(67, 45)))
    # ---------------- care
    o.r('scrub_left_planks', 'Scrubbing the left planks with a wing until the stains give up', 18, 'wing',
        [k(.12, 'plank_l', reach=.6, x=.3, y=.5), k(.3, 'plank_l', reach=1, x=.6, y=.8, b=.4, l=1), k(.5, 'ring_l', reach=1, x=.7, y=.9, b=.6, r=1, mark='skrk'), k(.7, 'stud_l', reach=1, x=.5, y=.5, l=1), k(.88, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'planks'), when=['obj_dirt>.3'], say=["Shed looked lived in. Now it looks cleaned in.", "Planks scrubbed. Wing ruined. Worth it for a plank."])
    o.r('wipe_left_glass', 'Wiping the left window glass in wide circles until he can see his own face', 18, 'wing',
        [k(.12, 'glass_l', reach=.5, x=.2, y=-.3), k(.3, 'glass_l', reach=1, x=.5, y=-.6, w=.4, mark='squk'), k(.5, 'glass_l', reach=1, x=.6, y=-.8, l=1, mark='squk'), k(.72, 'sill_l', reach=1, x=.5, y=-.2, r=1), k(.88, eye='^')],
        [(.5, 'buff')], g='care', act=('wipe', 'glass'), when=['obj_dirt>.3'], ages=GROWN, say=["Glass clear. Handsome duck in there. Poor lighting.", "Wiped it. The window did not say thank you."])
    o.r('sweep_dust_off_sill', 'Sweeping the dust off the left window sill with the flat of a wing', 16, 'wing',
        [k(.12, 'sill_l', reach=.5, x=.2, y=-.3), k(.3, 'sill_l', reach=1, x=.5, y=-.5, l=1), k(.5, 'sill_l', reach=1, x=.6, y=-.6, b=.4, r=1, mark='fff'), k(.75, eye='-')],
        [(.5, 'brush')], g='care', act=('sweep', 'sill'), when=['obj_dirt>.5'], ages=GROWN)
    o.r('rub_hoop_dry', 'Rubbing the barrel hoop dry with his breast, grunting the whole way round', 20, 'none',
        [k(.12, 'barrel_hoop', x=.4, y=.5, b=.3), k(.3, 'barrel_hoop', x=.9, y=.7, b=.7, mark='hff'), k(.5, 'barrel_belly', x=1, y=.6, b=.9, l=1), k(.72, 'barrel_hoop', x=.9, y=.5, b=.5, r=1, mark='hff'), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'barrel'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.2)), (.72, dict(shake=.2))])
    o.r('tap_ring_plate_back', 'Tapping the left ring knob plate flat again with three firm pecks', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'ring_l', x=1, y=1.5, b=.4, mark='tak'), k(.45, x=.2, y=.4, l=1), k(.62, 'ring_l', x=1, y=1.6, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
        [(.62, 'seat')], g='care', act=('mend', 'ring'), when=['obj_condition<.6'], say=["Plate back flat. Shed holds. Applause not required.", "Tap, tap, done. I should bill by the tap."])
    o.r('straighten_the_tool', 'Nudging the leaning T-headed tool upright again with the tip of a wing', 18, 'wing',
        [k(.12, 'tool_t', reach=.5, x=.2, y=-.3), k(.32, 'tool_t', reach=1, x=.5, y=-.6, b=.3, mark='shff'), k(.52, 'hook_j', reach=1, x=.5, y=-.4, b=.5, l=1), k(.72, x=-.3, y=-.2, w=.4, eye='^')],
        [(.52, 'tidy')], g='care', act=('straighten', 'tool'), ages=GROWN, obj=[(.32, dict(sway=.3)), (.52, dict(sway=.1))])
    # ---------------- use
    o.r('rap_door_panel', 'Rapping the door panel rail with his bill in a knock-knock-knock rhythm', 18, 'none',
        [k(.12, 'panel_rail', x=1, y=.8, b=.3, mark='knock'), k(.3, 'panel_rail', x=1, y=.9, b=.5, l=1, mark='knock'), k(.5, x=-.6, y=-.4, w=.4, eye='O', mark='Anyone?'), k(.7, x=.2, y=.2, b=.8, r=1, eye='-')],
        [], g='use', act=('knock', 'panel'), prefer=['lonely'], say=["Shed said nothing. Shed keeps its secrets.", "Knocked. Even the rakes ignored me."])
    o.r('flick_the_latch', 'Lifting the latch with the tip of his bill and letting it clack back down', 16, 'none',
        [k(.12, 'latch', x=.6, y=.6), k(.3, 'latch', x=1.3, y=-.6, b=-.4, mark='click'), k(.5, 'latch', x=1.1, y=.8, b=.6, l=1, mark='CLACK'), k(.72, x=-.3, y=-.2, w=.5, eye='^')],
        [], g='use', act=('lift', 'latch'), prefer=['curious'], obj=[(.3, dict(shake=.2)), (.5, dict(shake=.6))], say=["Clack. It does that. I do that. We bond.", "Latch up, latch down. Riveting work."])
    o.r('rock_the_barrel', 'Rocking the barrel with his shoulder to feel whether anything sloshes', 22, 'none',
        [k(.12, 'barrel_belly', x=.2, y=.4), k(.3, 'barrel_belly', x=.8, y=.6, b=.7, mark='hnnh'), k(.5, 'barrel_belly', x=1, y=.7, b=1, l=1, mark='HNNH'), k(.72, x=-.4, y=-.2, w=.7, eye='-', mark='...')],
        [], g='use', act=('rock', 'barrel'), ages=GROWN, obj=[(.3, dict(sway=.3)), (.5, dict(sway=.9)), (.72, dict(sway=.1))], say=["Barrel sloshed. Or I did. Hard to tell.", "Shoulder hurts. Barrel has no shoulder. Unfair."])
    o.r('nudge_the_handle', 'Nudging the slanted tool handle with a wing to set it swaying', 16, 'wing',
        [k(.12, 'tool_t', reach=.5, x=.2, y=-.3), k(.32, 'hook_j', reach=1, x=.5, y=-.4, mark='tk'), k(.5, 'hook_j', reach=1, x=.6, y=-.5, b=.4, l=1), k(.72, x=-.2, y=-.2, w=.4, eye='O')],
        [], g='use', act=('nudge', 'handle'), ages=GROWN, obj=[(.32, dict(sway=.5)), (.5, dict(sway=-.5)), (.72, dict(sway=.2))])
    o.r('peer_at_left_glass', 'Pressing his bill to the left window glass and cupping a wing against the glare', 20, 'none',
        [k(.15, x=.3, y=-.2), k(.3, 'glass_l', x=1.4, y=-.5, b=.2, eye='O'), k(.5, 'glass_l', x=1.5, y=-.6, b=.3, w=.5, eye='>', mark='hm'), k(.72, 'glass_l', x=1.4, y=-.5, b=.3, eye='-'), k(.88, x=.2, eye='-')],
        [], g='use', act=('peer', 'glass'), ages=GROWN, prefer=['curious'])
    o.r('holler_at_window', 'Hollering a greeting up at the left window and waiting for a face to show', 18, 'wing',
        [k(.15, 'sill_l', reach=.5, x=.2, y=-.3), k(.35, 'sill_l', reach=1, x=.6, y=-.9, b=-.2, mark='OI'), k(.55, 'sill_l', reach=1, x=.7, y=-1, b=-.3, eye='O', mark='OOI!'), k(.75, x=-.2, y=.3, b=.6, eye='-', mark='...')],
        [], g='use', act=('shout', 'window'), ages=GROWN, prefer=['lonely'], say=["Window did not answer. Window has no manners.", "Greeted a window. Window left me on read."])
    # ---------------- play
    o.r('hop_barrel_rim', 'Hopping up to the barrel rim, standing tall, and hopping off again', 18, 'none',
        [k(.15, 'barrel_hoop', x=.4, y=.3, b=-.7, w=.6), k(.35, 'barrel_rim', perch=1, y=.2, b=.5, w=1, mark='ta-da'), k(.55, 'barrel_rim', perch=1, y=-.4, b=-.8, w=1), k(.78, 'barrel_hoop', y=.2, b=.4, l=1, eye='^')],
        [(.35, 'laugh')], g='play', act=('hop', 'barrel'), ages=GROWN, prefer=['young', 'happy'])
    o.r('drum_the_staves', 'Drumming a gallop along the barrel staves with his bill', 18, 'none',
        [k(.12, 'barrel_stave', x=1, y=1, b=.5, mark='tok'), k(.3, 'barrel_hoop', x=.8, y=.2, b=-.2, l=1, mark='tak'), k(.5, 'barrel_stave', x=1.1, y=1.1, b=.7, r=1, mark='tok tok'), k(.7, 'barrel_belly', x=.8, y=.3, b=-.2, l=1, mark='TAK'), k(.88, eye='^')],
        [(.7, 'laugh')], g='play', act=('drum', 'staves'), prefer=['happy'], say=["Barrel has a good bottom end. Poor song structure.", "Four-four time. The barrel plays in three."])
    o.r('flatten_at_barrel', 'Flattening himself against the barrel and bursting out at nothing', 18, 'none',
        [k(.15, 'barrel_stave', x=-.3, y=.3, b=.4), k(.35, 'barrel_stave', x=-.4, y=.9, b=.8, eye='-'), k(.55, 'barrel_stave', x=-.4, y=1, b=.9, l=1, eye='-', mark='...'), k(.7, y=-.8, b=-.8, w=1, eye='O', mark='RAWR'), k(.88, y=.3, eye='^')],
        [], g='play', act=('hide', 'barrel'), prefer=['young'], say=["Ambush. Target: nothing. Success rate: complete.", "Barrel did not scream. Weak ambush victim."])
    o.r('sprint_the_steps', 'Sprinting from one end of the step to the other and skidding to a halt at the threshold', 16, 'none',
        [k(.12, 'step_a', x=.4, y=.4, b=.3), k(.32, 'step_b', x=.8, y=.7, b=.6, l=1, w=.5, mark='zoom'), k(.55, 'thresh', x=.2, y=.9, b=1, r=1, mark='skrt'), k(.78, 'thresh', y=.2, w=.7, eye='^')],
        [], g='play', act=('race', 'step'), prefer=['young', 'happy'])
    o.r('spin_at_threshold', 'Spinning like a top at the threshold until the shed seems to rotate', 16, 'none',
        [k(.12, 'thresh', x=.5, y=.3, b=.3, l=1), k(.3, 'thresh', x=-.7, y=.6, b=.7, w=.7, r=1), k(.5, 'thresh', x=.7, y=.4, b=.8, w=1, l=1, eye='@'), k(.7, 'thresh', x=-.7, y=.6, b=.7, w=.7, r=1), k(.88, x=.1, eye='o')],
        [], g='play', act=('spin', 'threshold'), prefer=['young', 'happy'])
    o.r('scratch_beside_step', 'Scratching up the ground beside the step with both feet, burying nothing', 18, 'none',
        [k(.12, 'step_a', x=.4, y=.9, b=.5), k(.3, 'step_a', x=.5, y=1.2, b=1, l=1, mark='scr'), k(.5, 'step_a', x=.5, y=1.4, b=1.2, r=1, mark='scr scr'), k(.7, 'step_a', x=.4, y=1.4, b=1.3, l=1), k(.88, y=.2, w=.4, eye='^')],
        [(.5, 'scuff')], g='play', act=('dig', 'ground'), prefer=['happy'], say=["Hole. Empty. Plan on track.", "Dug deeper. Found more ground. Disappointing."])
    # ---------------- test
    o.r('tap_staves_for_full', 'Tapping up the barrel staves with his bill to guess whether it is full', 18, 'none',
        [k(.12, 'barrel_stave', x=1, y=1, b=.5, mark='tok'), k(.3, 'barrel_belly', x=.7, y=-.1, b=-.2, l=1, mark='tok'), k(.55, x=-.5, y=-.5, w=.4, eye='-'), k(.75, 'barrel_hoop', x=1.1, y=.6, b=.5, mark='tonk'), k(.9, eye='^')],
        [], g='test', act=('tap', 'barrel'), say=["Sounds full. Or sounds sulky. Same noise.", "Hollow at the top, solid below. Like a duck."])
    o.r('count_the_studs', 'Touching each stud head along the left wall and counting under his breath', 20, 'none',
        [k(.1, 'stud_l', x=.8, y=-.4, b=-.3, mark='1'), k(.28, 'stud_l2', x=1, y=-.2, b=.3, l=1, mark='2'), k(.5, 'stud_r', x=.6, y=-.4, b=-.4, r=1, mark='3'), k(.7, 'ring_r', x=1.1, y=1.4, b=.4, l=1, mark='4'), k(.88, x=-.4, w=.4, eye='-', mark='four')],
        [], g='test', act=('count', 'studs'), prefer=['curious'])
    o.r('size_up_the_sill', 'Craning up to see whether the left sill is within his reach, and deciding it is not', 18, 'none',
        [k(.12, 'sill_l', x=.2, y=-.4, b=-.6), k(.3, 'sill_l', x=.6, y=-.9, b=-1, w=.6, mark='...'), k(.55, 'sill_l', x=1, y=-1.2, b=-1.2, w=1, eye='O', mark='nnng'), k(.75, x=-.4, y=.9, b=.8, eye='-', mark='no'), k(.9, eye='>')],
        [], g='test', act=('measure', 'sill'), ages=GROWN, say=["Sill is exactly one duck too high. Standard.", "Tall house, short duck. Law of nature."])
    o.r('listen_at_the_door', 'Pressing an ear to the lower door panel and listening for anything inside', 20, 'none',
        [k(.15, 'door_foot', x=.3, y=.5), k(.35, 'door_foot', x=.8, y=1.4, b=.9, eye='-', mark='...'), k(.6, 'door_foot', x=.9, y=1.5, b=1, l=1, eye='O', mark='!'), k(.8, x=-.3, y=-.4, eye='-', mark='nothing')],
        [], g='test', act=('listen', 'door'), prefer=['curious'])
    o.r('sniff_the_barrel_rim', 'Sniffing along the barrel rim to find out what it used to hold', 18, 'none',
        [k(.15, 'barrel_belly', x=.4, y=.5), k(.32, 'barrel_rim', x=1.2, y=-.4, b=-.3, mark='snf'), k(.52, 'barrel_rim', x=1.4, y=-.5, b=-.2, l=1, mark='snf snf'), k(.74, x=-.4, y=.4, eye='>', mark='ugh'), k(.9, eye='-')],
        [], g='test', act=('sniff', 'rim'), say=["Smells of old apples and bad decisions.", "Pickles. Possibly regret. Possibly both."])
    o.r('stomp_the_step', 'Stomping the step twice to see if it takes his weight', 14, 'none',
        [k(.15, 'step_b', y=.3, b=.3, l=1), k(.3, 'step_b', y=.5, b=.8, r=1, mark='THUD'), k(.5, 'step_b', y=.5, b=.9, l=1, mark='THUD'), k(.72, x=-.2, w=.5, eye='^', mark='fine'), k(.88, eye='-')],
        [], g='test', act=('test', 'step'))
    # ---------------- rest
    o.r('sit_on_barrel_rim', 'Sitting on the barrel rim with his feet dangling over the hoop', 24, 'none',
        [k(.12, 'barrel_rim', perch=1, y=-.2, b=.2), k(.3, 'barrel_rim', perch=1, y=.4, b=.9, eye='-'), k(.6, 'barrel_rim', perch=1, y=.5, b=1, l=1, eye='-', mark='...'), k(.85, 'barrel_rim', perch=1, y=.1, b=.4, r=1, eye='^')],
        [(.6, 'rest')], g='rest', act=('sit', 'barrel'), ages=GROWN, say=["Throne. Round. Slightly damp. Slightly mine.", "Legs dangling. Barrel steady. Life is acceptable."])
    o.r('lean_on_door_jamb', 'Propping a shoulder against the door jamb with his arms folded', 22, 'none',
        [k(.1, 'jamb_l', x=.6, y=.2, b=.6, l=1), k(.3, 'jamb_l', x=-.5, y=.4, b=.2, eye='-'), k(.5, 'jamb_l', x=-.6, y=.5, b=.4, w=.8, eye='-', mark='hm'), k(.7, 'jamb_l', x=-.2, y=1, b=1.1, r=1, eye='>'), k(.88, eye='-')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    o.r('sulk_at_the_step', 'Sitting hunched at the step and refusing to look at the shed', 22, 'none',
        [k(.15, 'step_a', perch=1, x=.2, y=.2, b=.3), k(.35, 'step_a', perch=1, x=-.7, y=.9, b=.8, eye='-', mark='hmph'), k(.6, 'step_a', perch=1, x=-.8, y=1, b=1, r=1, eye='>'), k(.85, 'step_a', perch=1, x=-.5, y=.3, b=.4, eye='-')],
        [], g='rest', act=('sulk', 'step'), prefer=['grumpy', 'sad'], say=["Shed knows what it did. I am waiting.", "Sulking at a shed. New low. Comfortable."])
    o.r('wait_at_the_door', 'Waiting at the door for whoever keeps the key to come back', 28, 'none',
        [k(.12, 'lip_a', x=.4, y=.5, b=.5), k(.3, 'lip_a', x=-.4, y=.2, b=.1, l=1, eye='-'), k(.5, 'lip_b', x=.8, y=.9, b=.9, r=1, eye='>', mark='...'), k(.7, 'lip_b', x=-.3, y=.3, b=-.2, w=.6, eye='-'), k(.9, 'lip_a', y=.5, eye='-')],
        [], g='rest', act=('wait', 'door'), prefer=['lonely'])
    o.r('warm_back_against_wall', 'Turning his back to the right wall and soaking up what the sun left in it', 22, 'none',
        [k(.12, 'plank_r', x=-.2, y=.3, b=.2), k(.35, 'plank_r', x=-.3, y=.8, b=.6, eye='-', mark='ahh'), k(.6, 'plank_r', x=-.4, y=.9, b=.8, l=1, eye='^'), k(.85, 'plank_r', x=-.2, y=.4, b=.4, eye='-')],
        [], g='rest', act=('warm', 'wall'), when=['sun'])
    o.r('lean_on_ring_post', 'Hooking his chin over the right ring knob and leaning his whole weight there', 20, 'none',
        [k(.12, 'ring_r', x=.4, y=.3), k(.32, 'ring_r', x=1.1, y=.8, b=.7, eye='-', mark='mm'), k(.58, 'ring_r', x=1.2, y=.9, b=.9, r=1, eye='-'), k(.82, 'ring_r', x=.8, y=.4, b=.4, eye='^')],
        [], g='rest', act=('lean', 'ring'), prefer=['curious'])
    # ---------------- weather
    o.r('scoop_snow_off_rim', 'Scooping the snow off the barrel rim with a wing, again and again', 20, 'wing',
        [k(.12, 'barrel_rim', reach=.5, x=.3, y=.4), k(.3, 'barrel_rim', reach=1, x=.6, y=.8, b=.4, l=1, mark='fsh'), k(.5, 'barrel_belly', reach=1, x=.7, y=.9, b=.6, r=1, mark='fsh'), k(.72, 'barrel_rim', reach=.8, x=.4, y=.4, l=1), k(.88, eye='^')],
        [(.5, 'scoop')], g='weather', act=('scoop', 'rim'), when=['drift>.3'], say=["Snow lid off. Barrel has no thanks to give.", "Cold wings. Clean rim. Jury still out."])
    o.r('flick_snow_off_sill', 'Flicking the snow off the left sill in two sharp wing strokes', 16, 'wing',
        [k(.12, 'sill_l', reach=.5, x=.2, y=-.4), k(.3, 'sill_l', reach=1, x=.5, y=-.5, w=.3, mark='fff'), k(.5, 'sill_l', reach=1, x=.6, y=-.6, b=.5, l=1, mark='FFF'), k(.75, eye='^')],
        [(.5, 'flick')], g='weather', act=('fluff', 'sill'), when=['drift>.5'], ages=GROWN)
    o.r('scratch_frost_off_glass', 'Scratching the frost off the left glass with the edge of his bill', 18, 'none',
        [k(.12, 'glass_l', x=.4, y=-.3, b=-.4), k(.3, 'glass_l', x=1.1, y=-.6, b=-.2, mark='skrk'), k(.5, 'glass_l', x=1.2, y=-.7, b=.2, l=1, mark='skrk'), k(.72, 'glass_l', x=.9, y=-.4, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='weather', act=('scrape', 'glass'), when=['frost>.3'], ages=GROWN)
    o.r('huff_a_peephole', 'Huffing a round peephole in the frosted glass, then squinting through it', 20, 'none',
        [k(.12, 'sill_l', x=.5, y=-.2), k(.3, 'sill_l', x=1, y=-.6, b=-.3, mark='haah'), k(.5, 'sill_l', x=1.1, y=-.7, b=-.2, w=.4, mark='haaah'), k(.75, 'glass_l', x=1.3, y=-.5, b=.2, eye='O', mark='ha!'), k(.9, eye='-')],
        [(.5, 'peep')], g='weather', act=('blow', 'glass'), when=['frost>.3'], ages=GROWN, shown='head')
    o.r('rake_leaves_to_heap', 'Raking the fallen leaves toward the step with both feet, one heap at a time', 20, 'none',
        [k(.12, 'step_a', x=.3, y=.8, b=.4), k(.3, 'step_a', x=.4, y=1.1, b=.9, l=1, mark='sh sh'), k(.5, 'step_b', x=.4, y=1.2, b=1, r=1, mark='sh sh'), k(.72, 'step_b', x=.3, y=.8, b=.6, l=1), k(.88, eye='^')],
        [(.5, 'rake')], g='weather', act=('rake', 'leaves'), when=['leaves>.3'], say=["Leaves in a heap. Wind will undo it. Wind is rude.", "Raked it with my feet. Calling it landscaping."])
    o.r('shelter_at_barrel_flank', 'Pressing flat against the barrel flank with his wings over his head while the rain drums', 30, 'none',
        [k(.12, 'barrel_belly', x=.2, y=.4, b=.3), k(.3, 'barrel_belly', x=-.3, y=.9, b=.8, w=1, eye='-'), k(.55, 'barrel_belly', x=-.4, y=1, b=1, w=1, l=1, eye='>', mark='drip'), k(.8, 'barrel_belly', x=-.2, y=.5, b=.4, w=.6, eye='-')],
        [(.55, 'spray')], g='weather', act=('shelter', 'barrel'), when=['wet', 'obj_wetness<.6'])
    # ---------------- mishap
    o.r('skid_on_frosty_lip', 'Skidding along the frosted door lip with both feet going different ways', 16, 'none',
        [k(.1, 'lip_a', x=.3, y=.3, b=.3, r=1), k(.28, 'lip_b', x=.9, y=.6, b=-.3, l=1, w=.9, eye='O'), k(.46, 'lip_b', x=-.9, y=1.1, b=1.1, r=1, w=1, mark='WHOA'), k(.62, 'lip_a', x=-.2, y=1.5, b=1.6, eye='@', mark='*thud*'), k(.8, y=.6, b=.7, eye='-')],
        [(.46, 'scuff')], g='mishap', act=('slip', 'lip'), when=['frost>.5'], say=["Frost lied. Lip lied. Duck fell for both.", "Down. Not out. Mostly down."])
    o.r('march_into_barrel', 'Marching confidently at the barrel and meeting its rim with his face', 18, 'none',
        [k(.1, x=.3, y=.3, b=.5, l=1), k(.3, x=.9, y=.5, b=.2, r=1), k(.5, 'barrel_rim', x=1.7, y=.9, b=1, w=.8, eye='@', mark='BONK'), k(.7, 'barrel_hoop', x=-1, y=.6, b=.7, l=1, eye='O'), k(.9, eye='-')],
        [], g='mishap', act=('walk_into', 'barrel'), say=["Barrel was there before I was. Etiquette says it wins.", "Rim got my face. Barrel got the last word."])
    o.r('whack_panel_too_hard', 'Whacking the panel rail so hard the plank creaks and the nail skews', 16, 'none',
        [k(.1, 'panel_rail', x=.8, y=.7, b=.3, l=1), k(.28, 'panel_rail', x=1.6, y=1.9, b=.9, mark='TOK'), k(.48, 'panel_rail', x=1.7, y=2, b=1.2, r=1, eye='@', mark='CRK'), k(.68, x=-.7, y=.1, b=-.4, w=.8, eye='O'), k(.86, eye='-')],
        [(.48, 'dent')], g='mishap', act=('knock', 'rail'), prefer=['grumpy'], say=["Nail skewed. Shed will forgive me. Shed has no say.", "Hit it. It hit back. Lesson ignored."])
    o.r('wing_snagged_on_hook', 'Catching a wingtip at the J hook and flapping himself free in a panic', 18, 'wing',
        [k(.15, 'hook_j', reach=.6, x=.4, y=-.3), k(.35, 'hook_j', reach=1, x=-.3, y=.4, b=.4, w=.8, eye='O'), k(.55, 'hook_j', reach=.7, x=.4, y=.7, b=.8, l=1, r=1, mark='ack'), k(.75, y=.8, b=.9, eye='@'), k(.9, eye='-')],
        [], g='mishap', act=('catch', 'hook'), ages=GROWN)
    o.r('bill_stuck_in_latch', 'Jamming his bill at the latch loop and finding it will not come out', 22, 'none',
        [k(.15, 'latch', x=.6, y=.6, b=.2), k(.3, 'latch', x=1.4, y=.9, b=.6, eye='O', mark='mm'), k(.5, 'latch', x=1.5, y=1, b=.8, l=1, r=1, eye='@', mark='mmf!'), k(.7, 'jamb_l', x=1.6, y=1.2, b=1, w=1, mark='POP'), k(.88, x=-.2, y=.6, eye='>')],
        [], g='mishap', act=('stuck', 'latch'), prefer=['curious'], obj=[(.5, dict(shake=.5)), (.7, dict(shake=.2))], say=["Latch ate my bill. I got it back. Barely.", "Not my best poke. Possibly my worst."])
    o.r('shove_barrel_and_bounce', 'Shoving the barrel with a running start and bouncing straight back off it', 18, 'none',
        [k(.12, y=.2, b=.3, l=1), k(.3, 'barrel_hoop', x=1.2, y=.5, b=.9, eye='>'), k(.5, 'barrel_hoop', x=1.5, y=.6, b=1.1, w=.5, mark='BOMF'), k(.7, x=-1, y=.6, b=.6, w=1, r=1, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('shove', 'barrel'), ages=GROWN, obj=[(.5, dict(sway=.4)), (.7, dict(sway=0))])
    # ---------------- show
    o.r('pose_on_barrel_rim', 'Posing on the barrel rim like the figurehead of a very small ship', 20, 'none',
        [k(.15, 'barrel_rim', perch=1, y=.1, b=.1), k(.35, 'barrel_rim', perch=1, x=1.2, y=-.7, b=.2, w=1, eye='^'), k(.6, 'barrel_rim', perch=1, x=1.4, y=-.9, b=.3, w=.6, l=1, eye='-', mark='ahoy'), k(.85, 'barrel_rim', perch=1, y=.1, eye='^')],
        [], g='show', act=('pose', 'rim'), ages=GROWN, prefer=['happy'], say=["Ahoy. Nothing. Fine. Sail on.", "Figurehead of a shed. Sails: none."])
    o.r('bow_to_the_window', 'Bowing very low to the left window as if someone had waved', 20, 'none',
        [k(.1, 'ring_l', x=.3, y=.5, b=.2, l=1), k(.3, 'ring_l', x=1, y=1.6, b=1.1, w=.8, eye='-'), k(.5, 'ring_l', x=1.2, y=2, b=1.6, w=1, mark='madam'), k(.7, 'ring_l', x=.2, y=.6, b=.4, r=1), k(.88, eye='^')],
        [], g='show', act=('bow', 'window'))
    o.r('present_the_tool', 'Gesturing at the leaning tool with both wings like a salesman', 22, 'wing',
        [k(.1, 'stud_r', reach=.6, x=.5, y=-.4, b=.4, l=1), k(.3, 'hook_j', reach=1, x=.9, y=-.9, b=-.4, mark='behold'), k(.5, 'tool_t', reach=1, x=1, y=-1, b=-.6, r=1, mark='gently used'), k(.72, 'tool_t', reach=.8, x=.2, y=.3, b=.5, eye='^'), k(.9, eye='-')],
        [], g='show', act=('present', 'tool'), ages=GROWN, say=["Fine tool. Previous owner: the shed. Cash only.", "Gently used. Gently leaning. Gently overpriced."])
    o.r('argue_with_hook', 'Arguing with the T-headed tool and its hook, winning every point', 20, 'wing',
        [k(.12, 'tool_t', reach=.5, x=.6, y=.2, b=.2), k(.3, 'hook_j', reach=1, x=1, y=.3, b=.4, mark='no'), k(.5, 'tool_t', reach=1, x=1.2, y=.4, b=.6, l=1, mark='YES'), k(.7, 'hook_j', reach=1, x=1, y=.3, b=.4, r=1, mark='no'), k(.88, x=-.3, y=.2, w=.7, eye='>')],
        [], g='show', act=('argue', 'hook'), ages=GROWN, prefer=['grumpy'], say=["Hook says nothing. Smug about it.", "Won on points. The hook counts nothing."])
    o.r('sing_at_the_barrel', 'Singing at the barrel lid so it booms the chorus back', 24, 'none',
        [k(.1, 'barrel_stave', x=.5, y=-.4, b=.4), k(.3, 'barrel_belly', x=-.6, y=-1, b=1, w=.9, mark='laa'), k(.5, 'barrel_rim', x=1.5, y=-1.2, b=-.6, w=1, l=1, eye='^', mark='LAAA'), k(.72, 'barrel_rim', x=.4, y=.4, b=.8, r=1, eye='-', mark='...'), k(.9, eye='-')],
        [], g='show', act=('sing', 'barrel'), ages=GROWN, prefer=['happy'])
    o.r('dance_down_the_steps', 'Dancing a jig from the top step round to the barrel and back', 22, 'none',
        [k(.1, 'step_b', perch=1, y=-.5, b=-.8, l=1, w=.7), k(.26, 'step_a', perch=1, y=.5, b=.8, r=1, w=1.2), k(.42, 'thresh', perch=1, x=.6, y=-.6, b=-.9, l=1, w=1, mark='tada'), k(.6, 'lip_a', perch=1, x=-.5, y=.6, b=.9, r=1, w=.5), k(.78, 'step_b', perch=1, y=-.4, b=-.6, l=1, w=.9), k(.92, eye='^')],
        [], g='show', act=('dance', 'steps'), prefer=['happy'])
    return o


def greenhouse():
    # Drawing (108 x 58 cells, 9.3 px a row, standing line row 54): glass roof rows 28-33, glazing bars rows 34 39 44 (186 140 93 px) and a ledge row 49
    # (47 px) across two glass blocks (left cols 10-45, right cols 67-100); flowers `(*)` stand on the floor behind the lowest panes (rows 47-48, 56-65 px);
    # a base band rows 50-52 (37 / 28 / 19 px) with ironwork between; centre door cols 45-67 (jambs, panel rails rows 33 38 43, ring knobs row 34 and 42,
    # studs rows 40 and 47, latch `.--|-.` row 49, foot strip row 51, step row 53, threshold row 54); two pots `(o)` `(__)` at cols 89-96 rows 53-55.
    P = pm('greenhouse')
    o = Obj('greenhouse', 'placed',
            fields=dict(fog=(0, 0, 1), heat=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('fog', 'rate', .002, 'night'), ('fog', 'rate', -.003, 'sun'), ('heat', 'rate', .0009, 'sun'), ('heat', 'rate', -.0006, '!sun'),
                     ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(wipefog=[('fog', 'set', 0)], doodle=[('fog', 'mul', .6)], scrub=[('obj.dirt', 'add', -.25)], sweep=[('obj.dirt', 'add', -.15)],
                         dry=[('obj.wetness', 'add', -.3)], spray=[('obj.wetness', 'add', .12)], bar=[('obj.condition', 'add', .2)], crack=[('obj.condition', 'add', -.15)],
                         scrape=[('frost', 'mul', .2)], cool=[('heat', 'add', -.25), ('need.energy', 'add', 2)], tidy=[('need.cleanliness', 'add', 1)],
                         laugh=[('need.fun', 'add', 2)], scuff=[('obj.dirt', 'add', .12)], bask=[('heat', 'add', -.2)]),
            anchors=dict(glass_lo=P(22, 48), pane_l=P(14, 46), pane_l2=P(30, 46), bar_l=P(22, 44), pane_hi=P(30, 36), flower_l=P(14, 48), flower_l2=P(38, 48),
                         flower_r=P(76, 48), flower_r2=P(88, 48), ledge_l=P(24, 49, 'surface'), ledge_r=P(82, 49, 'surface'), plinth_l=P(30, 51), plinth_r=P(80, 51),
                         foot_l=P(20, 53), foot_r=P(36, 53), jamb_l=P(46, 45), jamb_r=P(66, 45), knob_l=P(49, 42), knob_r=P(62, 42), latch=P(60, 49), stud_d=P(51, 47),
                         door_foot=P(55, 51), step_a=P(50, 53, 'surface'), step_b=P(60, 53, 'surface'), thresh=P(55, 54, 'surface'), pot_a=P(90, 53), pot_b=P(95, 53),
                         pane_r=P(94, 46)))
    # ---------------- care
    o.r('scrub_lower_panes', 'Scrubbing the grime off the lower panes with a wing, one square at a time', 20, 'wing',
        [k(.08, 'glass_lo', reach=.6, x=.6, y=.8, b=.2), k(.22, 'pane_l', reach=1, x=.9, y=.9, b=.7, l=1), k(.4, 'pane_l2', reach=1, x=1, y=1, b=.3, r=1, mark='sqk'), k(.6, 'glass_lo', reach=1, x=.9, y=1.2, b=.8, l=1, mark='sqk'), k(.8, eye='^')],
        [(.6, 'scrub')], g='care', act=('scrub', 'panes'), when=['obj_dirt>.3'], say=["Panes scrubbed. Now the flowers can see how little I care.", "Wiped it all. Spotless. Suspicious."])
    o.r('sweep_the_ledge', 'Sweeping the ledge clear along its length with the flat of a wing', 18, 'wing',
        [k(.1, 'ledge_l', reach=.5, x=.4, y=.7, b=.4), k(.3, 'ledge_l', reach=1, x=.7, y=.9, b=.9, r=1, mark='fff'), k(.52, 'plinth_l', reach=1, x=.5, y=1.1, b=1.2, l=1, mark='fff'), k(.74, 'plinth_l', reach=.7, x=.2, y=.4, b=.3), k(.9, eye='-')],
        [(.52, 'sweep')], g='care', act=('sweep', 'ledge'), when=['obj_dirt>.5'])
    o.r('mop_plinth_dry', 'Mopping the plinth band dry from end to end with his breast', 22, 'none',
        [k(.1, 'plinth_l', x=.7, y=.2, b=.8), k(.28, 'plinth_l', x=1.1, y=.4, b=1.3, mark='hff'), k(.5, 'foot_l', x=1.2, y=.6, b=1.6, l=1), k(.7, 'foot_r', x=1, y=.3, b=1, r=1, mark='hff'), k(.9, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'plinth'), when=['obj_wetness>.3'], obj=[(.28, dict(shake=.2)), (.7, dict(shake=.2))])
    o.r('seat_a_glazing_bar', 'Pressing a slipped glazing bar back into its groove with a firm bill-shove', 16, 'none',
        [k(.12, x=.8, y=-.6, b=.2), k(.3, 'bar_l', x=1.1, y=-.9, b=-.5, mark='nng'), k(.46, 'bar_l', x=1.3, y=-.7, b=.4, l=1), k(.64, 'bar_l', x=1.4, y=-.9, b=.6, r=1, mark='CLK'), k(.82, eye='^')],
        [(.64, 'bar')], g='care', act=('mend', 'bar'), when=['obj_condition<.6'], ages=GROWN, say=["Bar seated. Glass saved. Zero applause. Typical.", "Pushed it in with my face. Tradition."])
    o.r('line_up_the_pots', 'Shuffling both pots into line with his bill so the sprouts face front', 18, 'none',
        [k(.1, 'pot_a', x=.6, y=1, b=.5), k(.3, 'pot_a', x=1.2, y=1.5, b=.9, l=1, mark='scrt'), k(.5, 'pot_b', x=1.3, y=1.5, b=1, r=1, mark='scrt'), k(.7, 'pot_b', x=.5, y=.9, b=.4), k(.88, x=.1, eye='^')],
        [(.5, 'tidy')], g='care', act=('straighten', 'pots'), prefer=['curious'], say=["Pots straight. Plants unimpressed. Pots grateful. Allegedly.", "Lined them up. Soldiers of soil."])
    o.r('rub_off_the_sill_dust', 'Wiping the dust off the lower ledge with the tip of a wing', 14, 'wing',
        [k(.14, 'ledge_r', reach=.5, x=.3, y=.6), k(.34, 'ledge_r', reach=1, x=.5, y=.7, b=.4, mark='shk'), k(.56, 'pane_r', reach=1, x=.6, y=.8, b=.5, l=1, mark='shk'), k(.8, eye='-')],
        [(.56, 'sweep')], g='care', act=('wipe', 'ledge'), when=['obj_dirt>.3'], ages=GROWN)
    # ---------------- use
    o.r('rap_the_door_frame', 'Rapping the door frame twice and then politely waiting for tea', 20, 'none',
        [k(.1, 'jamb_l', x=1.1, y=.9, b=.3, mark='tok'), k(.26, 'jamb_l', x=1.2, y=1, b=.6, l=1, mark='tok'), k(.46, 'knob_l', x=-.8, y=-.5, w=.5, eye='O', mark='Tea?'), k(.66, x=.1, y=.3, b=.9, r=1, eye='-', mark='...'), k(.86, eye='^')],
        [], g='use', act=('knock', 'frame'), prefer=['lonely'], say=["Tea not forthcoming. Plants rarely host.", "Knocked on a glass house. Brave. Pointless."])
    o.r('tap_glass_at_flower', 'Tapping the glass in front of the left flower to see whether it nods', 18, 'none',
        [k(.1, 'flower_l', x=1, y=1.4, b=.7, mark='tk'), k(.28, 'flower_l', x=1.2, y=1.6, b=.9, mark='tk'), k(.44, x=-.5, y=-.4, w=.8, eye='O'), k(.62, 'flower_l', x=1, y=1.4, b=.5, l=1, mark='tk tk'), k(.8, x=-.2, eye='-', mark='no nod')],
        [], g='use', act=('tap', 'flower'), prefer=['curious'], say=["Flower ignored me. I respect the craft.", "Tapped twice. Bloom stayed rude and upright."])
    o.r('look_the_flowers_over', 'Pressing his bill to the glass and looking the left flowers over like a judge', 22, 'none',
        [k(.1, 'flower_l', x=.5, y=.9, b=.3), k(.3, 'flower_l2', x=1.4, y=.8, b=.8, eye='>', mark='hm'), k(.5, 'flower_l', x=1.5, y=.9, b=1, l=1, eye='-', mark='hmm'), k(.7, 'flower_l2', x=1.4, y=.8, b=.8, r=1, eye='O'), k(.88, x=.2, eye='^')],
        [], g='use', act=('peer', 'flowers'), prefer=['curious'])
    o.r('test_the_latch', 'Testing the latch with the tip of his bill, then testing it again out of spite', 18, 'none',
        [k(.1, 'latch', x=.7, y=.8, b=.3), k(.26, 'latch', x=1.4, y=.5, b=.8, l=1, mark='click'), k(.44, 'door_foot', x=1.2, y=.9, b=.6, w=.5), k(.62, 'latch', x=1.5, y=.7, b=.9, r=1, mark='CLICK'), k(.82, eye='^')],
        [], g='use', act=('test', 'latch'), obj=[(.26, dict(shake=.2)), (.62, dict(shake=.4))], say=["Latch works. Door is not open. Tragic combination.", "Clicked it twice. Second one was spite."])
    o.r('tell_the_flowers_off', 'Squaring up to the right flowers and telling them a long, loud story', 22, 'none',
        [k(.1, 'flower_r', x=.4, y=.4, b=.2), k(.3, 'flower_r', x=-.3, y=-.8, b=-.4, w=.9, mark='AND THEN'), k(.5, 'flower_r2', x=-.2, y=-1, b=-.6, w=1, l=1, mark='AND THEN'), k(.7, 'flower_r2', x=.8, y=.7, b=.9, r=1, eye='>', mark='the end'), k(.88, eye='^')],
        [], g='use', act=('shout', 'flowers'), prefer=['lonely'], say=["Told them everything. Not one asked a question.", "Flowers listen well. Mostly because they cannot leave."])
    o.r('sniff_the_pot_soil', 'Sniffing the pots one after the other and sneezing at the second', 16, 'none',
        [k(.12, 'pot_a', x=.8, y=1.3, b=.7, mark='snf'), k(.3, 'pot_a', x=1.1, y=1.6, b=1, l=1, mark='snf'), k(.5, 'pot_b', x=1.3, y=1.7, b=1.2, r=1, mark='snf'), k(.66, x=-.9, y=-.5, b=-.4, w=1, eye='O', mark='ACHOO'), k(.84, eye='-')],
        [], g='use', act=('sniff', 'pots'))
    # ---------------- play
    o.r('hop_the_ledge_ends', 'Hopping up to the left ledge, along it, and off with a flap', 18, 'none',
        [k(.1, 'step_a', x=.3, y=.2, b=-.6, w=.5), k(.26, 'ledge_l', perch=1, y=.3, b=.8, l=1), k(.44, 'ledge_l', perch=1, x=.6, y=-.5, b=-.9, w=1, mark='hup'), k(.62, 'ledge_l', perch=1, x=.2, y=.5, b=.9, r=1), k(.8, 'step_a', y=-.4, b=-.7, w=.9, eye='^')],
        [(.62, 'laugh')], g='play', act=('hop', 'ledge'), ages=GROWN, prefer=['young', 'happy'])
    o.r('race_the_panes', 'Sprinting along the glass and knocking every low pane with his bill', 20, 'none',
        [k(.08, 'pane_l', x=.6, y=1.1, b=.6, mark='tk'), k(.24, 'pane_l2', x=.8, y=1.3, b=.3, l=1, mark='tk'), k(.42, 'pane_r', x=.9, y=1.1, b=.5, r=1, mark='tk'), k(.6, 'glass_lo', x=1, y=1.2, b=.4, l=1, mark='tk'), k(.82, x=.2, w=.8, eye='^')],
        [], g='play', act=('race', 'panes'), ages=GROWN, prefer=['young'])
    o.r('walk_the_right_ledge', 'Walking the right ledge with his wings out like a tightrope walker', 22, 'none',
        [k(.08, 'ledge_r', perch=1, y=-.2, w=.8, b=.2), k(.26, 'ledge_r', perch=1, x=.4, y=.3, b=.5, w=1, l=1), k(.46, 'ledge_r', perch=1, x=-.4, y=.4, b=.7, w=1, r=1, mark='whoa'), k(.66, 'ledge_r', perch=1, x=.3, y=-.3, b=-.4, w=.7), k(.86, eye='^')],
        [], g='play', act=('balance', 'ledge'), ages=GROWN, prefer=['young'])
    o.r('flatten_at_right_jamb', 'Flattening himself against the right jamb and jumping out at the flowers', 20, 'none',
        [k(.1, 'jamb_r', x=-.8, y=.6, b=.6, r=1), k(.3, 'jamb_r', x=-.9, y=1.1, b=1.1, eye='-'), k(.48, 'jamb_r', x=-.8, y=1.2, b=1.2, l=1, eye='-', mark='...'), k(.62, x=1.4, y=-1, b=-1, w=1, eye='O', mark='RAH'), k(.8, x=.4, y=.6, b=.4, eye='^')],
        [], g='play', act=('hide', 'jamb'), prefer=['young'], say=["Ambushed a flower. It lost. Nobody else saw.", "Jumped out. The jamb did not jump. Weird."])
    o.r('dig_in_the_right_pot', 'Digging at the soil of the right pot with his bill until the sprout leans', 18, 'none',
        [k(.1, 'pot_b', x=.8, y=1.2, b=.5), k(.28, 'pot_b', x=1.3, y=1.9, b=1.1, l=1, mark='dig'), k(.46, 'pot_b', x=1.4, y=2.1, b=1.3, r=1, mark='dig dig'), k(.66, 'pot_a', x=.5, y=1, b=.4, eye='>'), k(.84, eye='^')],
        [(.46, 'scuff')], g='play', act=('dig', 'pot'), prefer=['happy'], say=["Dug a hole. Sprout seems fine. Relocated my guilt.", "Soil in my bill. Plan unclear. Mood excellent."])
    o.r('drum_the_ironwork', 'Drumming a march along the ironwork band with his bill', 20, 'none',
        [k(.08, 'plinth_l', x=1.1, y=1.1, b=.4, mark='tk'), k(.24, 'foot_l', x=.8, y=.4, b=-.4, l=1, mark='tak'), k(.42, 'foot_r', x=1.2, y=1.2, b=.6, r=1, mark='tk tk'), k(.62, 'plinth_r', x=.9, y=.4, b=-.3, l=1, mark='TAK'), k(.84, eye='^')],
        [(.62, 'laugh')], g='play', act=('drum', 'plinth'), prefer=['happy'])
    # ---------------- test
    o.r('listen_at_the_glass', 'Laying his ear against the glass to hear whether the plants are talking', 22, 'none',
        [k(.1, 'glass_lo', x=.5, y=.8, b=.4), k(.3, 'glass_lo', x=1, y=1.4, b=1, eye='-', mark='...'), k(.52, 'glass_lo', x=1, y=1.5, b=1.2, l=1, eye='O', mark='!'), k(.74, x=-.6, y=-.4, w=.5, eye='-', mark='no')],
        [], g='test', act=('listen', 'glass'), prefer=['curious'], say=["Heard nothing. Plants are keeping it classified.", "Leaf rustle, maybe. Might be rude."])
    o.r('count_the_flowers', 'Counting the flowers pane by pane and losing track at six', 22, 'none',
        [k(.08, 'flower_l', x=.8, y=1.3, b=.6, mark='1'), k(.22, 'flower_l2', x=1, y=1.1, b=.2, l=1, mark='2'), k(.38, 'flower_r', x=.9, y=1.3, b=.7, r=1, mark='3'), k(.54, 'flower_r2', x=1, y=1.1, b=.3, l=1, mark='4'), k(.72, x=-.5, y=-.7, w=.7, eye='@', mark='six?'), k(.9, eye='-')],
        [], g='test', act=('count', 'flowers'), prefer=['curious'])
    o.r('compare_the_beds', 'Comparing the left flower bed with the right by marching between them and squinting', 24, 'none',
        [k(.08, 'flower_l2', x=.6, y=.9, b=.4), k(.26, 'flower_l2', x=1.1, y=.7, b=.9, eye='>', mark='hm'), k(.5, 'flower_r', x=1.1, y=.7, b=.9, l=1, mark='hmm'), k(.7, 'flower_r', x=-.4, y=-.5, b=-.2, w=.9, r=1, eye='-', mark='same')],
        [], g='test', act=('compare', 'beds'))
    o.r('lick_the_glass', 'Licking the glass once to confirm that it is, in fact, glass', 16, 'none',
        [k(.14, 'pane_l2', x=.6, y=.3, b=.3), k(.34, 'pane_l2', x=1.5, y=.4, b=-.6, mark='lick'), k(.56, 'pane_l2', x=1.6, y=.6, b=-.3, l=1, eye='@'), k(.76, x=-.6, y=.2, b=.5, w=.7, eye='>', mark='bleh')],
        [], g='test', act=('taste', 'glass'), prefer=['curious'], say=["Glass. Confirmed. Tastes like a mistake.", "Licked it. Now I know. Nobody asked."])
    o.r('prod_the_high_pane', 'Prodding the high pane with a twig to see whether it rattles', 20, 'twig',
        [k(.12, 'pane_hi', reach=.6, x=.3, y=-.6, b=-.3), k(.32, 'pane_hi', reach=1, x=.7, y=-1, b=-.6, mark='tk'), k(.52, 'pane_hi', reach=1, x=.8, y=-1.1, b=-.4, l=1, mark='tk tk'), k(.74, x=-.3, y=-.3, w=.5, eye='-')],
        [], g='test', act=('prod', 'pane'), ages=GROWN, obj=[(.32, dict(shake=.2)), (.52, dict(shake=.3))])
    o.r('measure_up_to_the_ledge', 'Stretching up to find out how high the ledge rim runs on him', 18, 'none',
        [k(.12, 'plinth_l', x=.2, y=-.5, b=-.6), k(.3, 'plinth_l', x=.6, y=-1, b=-1.1, w=.6, mark='...'), k(.52, 'ledge_l', x=1, y=-1.4, b=-1.3, w=1, eye='O', mark='nnng'), k(.72, x=-.6, y=.7, b=.9, eye='-', mark='knee')],
        [], g='test', act=('measure', 'ledge'), say=["Ledge comes to my chest. Pleased. Smug.", "Not tall. Not short. A very precise duck."])
    # ---------------- rest
    o.r('lean_on_sunny_glass', 'Leaning his shoulder against the sun-warmed glass and soaking it up', 26, 'none',
        [k(.1, 'glass_lo', x=.3, y=.4, b=.3), k(.28, 'glass_lo', x=-.4, y=.8, b=.7, eye='-'), k(.52, 'glass_lo', x=-.5, y=.9, b=.9, eye='-', mark='ahh'), k(.78, 'glass_lo', x=-.3, y=.5, b=.5, l=1, eye='^')],
        [(.52, 'cool')], g='rest', act=('lean', 'glass'), when=['heat>.3', 'sun'], say=["Warm glass. Warm duck. Slow plan.", "Sunbathing against a window. Ten out of ten, no notes."])
    o.r('sit_on_the_right_ledge', 'Sitting on the left ledge with his feet tucked, watching the flowers grow', 28, 'none',
        [k(.1, 'ledge_l', perch=1, y=-.2, b=.1), k(.3, 'ledge_l', perch=1, y=.5, b=1, eye='-'), k(.6, 'ledge_l', perch=1, y=.6, b=1.2, l=1, eye='-', mark='...'), k(.86, 'ledge_l', perch=1, y=.1, b=.4, r=1, eye='^')],
        [], g='rest', act=('sit', 'ledge'), ages=GROWN, say=["Flowers grew. Possibly. I blinked.", "Sat. Watched. Nothing happened, slowly."])
    o.r('sulk_at_the_pots', 'Hunching beside the pots with his back to the glass, refusing all flowers', 24, 'none',
        [k(.12, 'plinth_r', x=.1, y=.3, b=.4), k(.32, 'plinth_r', x=-.8, y=1, b=.9, eye='-', mark='hmph'), k(.58, 'foot_r', x=-.9, y=1.1, b=1.1, r=1, eye='>'), k(.84, 'foot_r', x=-.5, y=.4, b=.5, eye='-')],
        [], g='rest', act=('sulk', 'pots'), prefer=['grumpy', 'sad'], say=["The flowers know what they did. So do I.", "Sulking next to plants. They never apologise."])
    o.r('wait_at_the_step', 'Waiting at the step for the gardener, who is clearly a myth', 28, 'none',
        [k(.1, 'step_a', x=.5, y=.5, b=.5), k(.3, 'step_a', x=-.3, y=.3, b=.1, l=1, eye='-'), k(.52, 'step_b', x=.7, y=.8, b=.9, r=1, eye='>', mark='...'), k(.74, 'step_b', x=-.2, y=.3, b=-.2, w=.6, eye='-'), k(.92, eye='-')],
        [], g='rest', act=('wait', 'step'), prefer=['lonely'])
    o.r('warm_feet_on_the_sill', 'Warming his feet against the sun-baked ironwork until his toes tingle', 24, 'none',
        [k(.1, 'plinth_r', x=.3, y=.6, l=1), k(.32, 'plinth_r', x=.4, y=.9, b=.6, l=1, eye='-', mark='ahh'), k(.56, 'plinth_r', x=.4, y=.9, b=.6, r=1, eye='^'), k(.82, 'plinth_r', x=.1, y=.3, eye='-')],
        [(.56, 'bask')], g='rest', act=('warm', 'plinth'), when=['heat>.3', 'sun'])
    o.r('prop_himself_on_the_jamb', 'Propping himself against the left jamb with a very flat expression', 22, 'none',
        [k(.1, 'stud_d', x=.7, y=.3, b=.7, r=1), k(.3, 'stud_d', x=-.6, y=.5, b=.1, eye='-'), k(.5, 'jamb_r', x=-.7, y=.6, b=.3, w=.9, eye='>', mark='hm'), k(.7, 'jamb_r', x=-.1, y=1.2, b=1.3, l=1, eye='-'), k(.9, eye='-')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    # ---------------- weather
    o.r('wipe_the_fogged_pane', 'Dragging a wing down the fogged pane until the flowers swim into view', 18, 'wing',
        [k(.1, 'pane_l', reach=.5, x=.3, y=.4, b=.3), k(.3, 'pane_l', reach=1, x=.6, y=.7, b=.7, l=1, mark='squk'), k(.5, 'glass_lo', reach=1, x=.7, y=.9, b=1, r=1, mark='squk'), k(.72, 'pane_l2', reach=.8, x=.4, y=.5, b=.4, l=1), k(.9, eye='^')],
        [(.5, 'wipefog')], g='weather', act=('wipe', 'pane'), when=['fog>.3'], say=["Fog gone. Flowers still rude. Visibility is overrated.", "Squeaked the pane clear. Squeak was the best bit."])
    o.r('write_in_the_fog', 'Pecking an angry face at the fogged glass and adding a beak', 20, 'none',
        [k(.1, 'pane_l2', x=.6, y=-.2, b=.2), k(.28, 'glass_lo', x=1.2, y=.5, b=.6, mark='sqk'), k(.46, 'pane_l2', x=1.1, y=-.4, b=-.3, l=1, mark='sqk'), k(.64, 'glass_lo', x=1.3, y=.7, b=.8, r=1, mark='sqk'), k(.84, x=-.4, y=-.1, w=.6, eye='^')],
        [(.64, 'doodle')], g='weather', act=('peck', 'fog'), when=['fog>.4'], ages=GROWN, say=["Face drawn. Looks like me. Rude of it.", "Fog art. Gone by lunch. Like all my masterpieces."])
    o.r('chip_frost_off_the_bar', 'Chipping the frost off the lowest bar with the edge of his bill', 18, 'none',
        [k(.1, 'bar_l', x=.6, y=-.8, b=.2), k(.28, 'bar_l', x=1.3, y=-1, b=-.2, mark='tk'), k(.46, 'bar_l', x=1.4, y=-.8, b=.5, l=1, mark='tk'), k(.66, 'bar_l', x=1.1, y=-.5, b=.2, r=1), k(.84, eye='^')],
        [(.46, 'scrape')], g='weather', act=('chip', 'bar'), when=['frost>.3'], ages=GROWN)
    o.r('fan_himself_by_the_glass', 'Fanning himself with both wings beside the sun-hot glass and panting', 22, 'none',
        [k(.1, 'pane_r', x=-.2, y=.3, b=.2), k(.3, 'pane_r', x=-.5, y=.4, b=.8, w=1, eye='o', mark='pant'), k(.5, 'flower_r2', x=-.5, y=.5, b=1, w=.5, l=1, mark='pant'), k(.72, 'flower_r2', x=-.3, y=.3, b=.6, w=1, r=1), k(.9, eye='-')],
        [(.5, 'bask')], g='weather', act=('cool', 'glass'), when=['heat>.5', 'sun'], say=["Greenhouse. Greenhouse effect. Greenhouse duck.", "Too hot for feathers. Too stubborn for shade."])
    o.r('chase_raindrops_down', 'Chasing the raindrops down the pane with his bill, one race at a time', 20, 'none',
        [k(.1, 'pane_l', x=.6, y=-.4, b=-.2), k(.28, 'pane_l2', x=1, y=.4, b=.6, l=1, mark='tk'), k(.48, 'glass_lo', x=1.2, y=1.2, b=1, r=1, mark='tk'), k(.66, 'pane_l2', x=.9, y=-.2, b=-.3, l=1, eye='O'), k(.84, 'glass_lo', x=1.2, y=1.2, b=.9, eye='^')],
        [], g='weather', act=('chase', 'drops'), when=['obj_wetness>.3'], ages=GROWN, prefer=['happy'])
    o.r('shelter_at_the_jamb', 'Pressing flat against the door jamb with wings over his head as the rain drums', 32, 'none',
        [k(.06, 'jamb_l', x=.4, y=.8, b=.2, l=1), k(.2, 'jamb_l', x=-.7, y=1.4, b=1.3, w=.9, eye='-'), k(.4, 'jamb_l', x=-.8, y=1.5, b=1.6, w=1, r=1, eye='>', mark='drip'), k(.58, 'jamb_l', x=-.6, y=1.3, b=1.2, w=.5), k(.78, 'jamb_l', x=-.2, y=.7, b=.5, l=1, eye='-'), k(.92, eye='-')],
        [(.4, 'spray')], g='weather', act=('shelter', 'jamb'), when=['wet', 'obj_wetness<.6'])
    # ---------------- mishap
    o.r('slip_on_the_wet_step', 'Skidding along the wet step with one foot going east and the other going to the pub', 16, 'none',
        [k(.1, 'step_a', x=.3, y=.3, b=.4, l=1), k(.26, 'step_b', x=.9, y=.5, b=-.2, r=1, w=.9, eye='O'), k(.44, 'step_b', x=-.9, y=1, b=1.2, l=1, w=1, mark='WHEE'), k(.6, 'step_a', x=-.2, y=1.6, b=1.7, eye='@', mark='*thud*'), k(.8, y=.5, b=.6, eye='-')],
        [(.44, 'scuff')], g='mishap', act=('slip', 'step'), when=['obj_wetness>.5'], say=["Step is wet. Step is smug. I am horizontal.", "Left foot to the pub. Right foot to follow."])
    o.r('walk_nose_first_into_glass', 'Marching up to a clean pane and discovering it is not open air', 18, 'none',
        [k(.1, x=.4, y=.2, b=.4, l=1), k(.3, x=1, y=.3, b=.1, r=1), k(.5, 'pane_l', x=1.8, y=.8, b=.9, w=.6, eye='@', mark='BONK'), k(.7, 'glass_lo', x=-1, y=.5, b=.6, l=1, eye='O'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'pane'), ages=GROWN, say=["Glass is a trick. I demand a sign.", "Flower saw it. Flower said nothing. Flower snickered."])
    o.r('peck_a_pane_too_hard', 'Pecking a pane so hard the whole glass rings and a hairline crack runs out', 16, 'none',
        [k(.1, 'pane_l2', x=.8, y=.5, b=.3, l=1), k(.28, 'pane_l2', x=1.7, y=1.3, b=.9, mark='TOCK'), k(.46, 'pane_l2', x=1.8, y=1.4, b=1.1, r=1, eye='@', mark='CRK'), k(.66, x=-.8, y=.1, b=-.4, w=.8, eye='O'), k(.84, eye='-')],
        [(.46, 'crack')], g='mishap', act=('peck', 'glass'), ages=GROWN, prefer=['grumpy'], say=["Pane cracked. Pane was asking for it. Probably.", "That was my own reflection. Hit it first."])
    o.r('bill_wedged_in_ironwork', 'Poking his bill at a gap between the ironwork bars and finding it narrower coming back out', 24, 'none',
        [k(.1, 'plinth_l', x=.6, y=.7, b=.4), k(.28, 'plinth_l', x=1.5, y=1, b=.9, eye='O', mark='mm'), k(.48, 'plinth_l', x=1.6, y=1.2, b=1.2, l=1, r=1, eye='@', mark='mmf!'), k(.68, 'foot_l', x=1.7, y=1.4, b=1.4, w=1, mark='POP'), k(.86, x=-.3, y=.5, eye='>')],
        [], g='mishap', act=('stuck', 'ironwork'), prefer=['curious'], say=["Gap grew a grip. Gap lets go. Gap smirks.", "Bill in, bill out. The ironwork won the middle."])
    o.r('stub_his_toe_on_a_pot', 'Stubbing a toe against the round pot and hopping in a furious circle', 16, 'none',
        [k(.1, 'pot_a', x=.5, y=.5, b=.5, l=1), k(.26, 'pot_a', x=1.2, y=1, b=1.1, r=1, mark='OW'), k(.44, 'foot_r', x=-.6, y=.4, b=-.9, l=1, w=.9, eye='O', mark='ow ow'), k(.62, 'foot_r', x=.7, y=.5, b=-.6, r=1, w=.8, mark='ow'), k(.82, eye='>')],
        [], g='mishap', act=('kick', 'pot'), say=["Pot did nothing. Pot won anyway.", "Toe hurts. Pot is not sorry."])
    o.r('stamp_at_his_reflection', 'Stamping at his reflection in a low pane and getting stamped back', 16, 'none',
        [k(.1, 'pane_l', x=.5, y=.7, b=.3, l=1), k(.26, 'pane_l', x=.9, y=.9, b=.8, r=1, mark='STOMP'), k(.44, 'pane_l2', x=.9, y=1, b=1, l=1, mark='STOMP'), k(.62, 'pane_l2', x=1.1, y=.6, b=.5, w=.8, eye='>'), k(.82, eye='-')],
        [], g='mishap', act=('stamp', 'reflection'), prefer=['grumpy'])
    # ---------------- show
    o.r('pose_by_the_door', 'Striking a pose beside the glass door like a very small botanist', 22, 'none',
        [k(.1, 'knob_r', x=.9, y=-.5, b=.2, l=1), k(.3, 'knob_r', x=-.4, y=-.8, b=.9, w=.7, eye='^'), k(.52, 'jamb_r', x=1.2, y=-.9, b=.3, w=1, r=1, eye='-', mark='ahem'), k(.74, 'jamb_r', x=-.4, y=.8, b=1, w=.5, eye='^'), k(.9, eye='-')],
        [], g='show', act=('pose', 'door'), prefer=['happy'], say=["Botanist. Do not check the papers.", "Posed with plants. They stayed in character."])
    o.r('bow_to_the_flowers', 'Bowing deeply to the whole left bed as if it had applauded', 20, 'none',
        [k(.1, 'flower_l2', x=.5, y=.6, b=.3, l=1), k(.3, 'flower_l2', x=1.1, y=1.7, b=1.2, w=.8, eye='-'), k(.5, 'flower_l', x=1.2, y=2, b=1.7, w=1, mark='thank you'), k(.7, 'flower_l', x=.3, y=.7, b=.5, r=1), k(.88, eye='^')],
        [], g='show', act=('bow', 'flowers'))
    o.r('present_the_glasshouse', 'Sweeping a wing along the glass like an estate agent selling the sun', 22, 'wing',
        [k(.1, 'pane_l', reach=.6, x=.4, y=-.2, b=.2), k(.3, 'pane_l2', reach=1, x=.5, y=-.7, b=-.3, mark='light'), k(.5, 'pane_r', reach=1, x=.6, y=-.8, b=-.4, r=1, mark='airy'), k(.72, 'pane_r', reach=.8, x=.2, y=.3, b=.6, eye='^'), k(.9, eye='-')],
        [], g='show', act=('present', 'glasshouse'), ages=GROWN, say=["Light, airy, no roof worries. One flaw: plants.", "Three panes, no offers. Market is brutal."])
    o.r('argue_with_a_flower', 'Squaring up to the right flower, bill to bud, and arguing the finer points', 22, 'none',
        [k(.1, 'flower_r2', x=.7, y=.7, b=.4), k(.28, 'flower_r2', x=1.2, y=.9, b=.7, mark='no'), k(.46, 'flower_r', x=1.3, y=1, b=.9, l=1, mark='YES'), k(.64, 'flower_r2', x=1.2, y=.8, b=.6, r=1, mark='no'), k(.82, x=-.4, y=.3, w=.7, eye='>')],
        [], g='show', act=('argue', 'flower'), prefer=['grumpy'], say=["Flower lost. Flower never moved. Counting it a win.", "It won on points. I won on volume."])
    o.r('serenade_the_pots', 'Serenading the pots with a slow ballad and a sweeping wing', 24, 'none',
        [k(.1, 'pot_b', x=.5, y=-.3, b=.3), k(.3, 'pot_a', x=-.5, y=-1, b=.9, w=.8, mark='laa'), k(.52, 'pot_b', x=1.3, y=-1.1, b=-.5, w=1, l=1, eye='^', mark='LAAA'), k(.74, 'pot_a', x=.3, y=.4, b=.7, r=1, eye='-'), k(.9, eye='-')],
        [], g='show', act=('sing', 'pots'), prefer=['happy'], say=["Sang to the sprouts. They leaned away. Critics.", "Two pots, one voice. Standing ovation: absent."])
    o.r('dance_across_the_floor_steps', 'Dancing a quickstep from the left step to the right and finishing at the threshold', 22, 'none',
        [k(.08, 'step_a', perch=1, y=-.4, b=-.7, l=1, w=.8), k(.24, 'step_b', perch=1, x=.5, y=.4, b=.8, r=1, w=1.1), k(.42, 'step_a', perch=1, x=-.5, y=-.5, b=-.8, l=1, w=1, mark='tada'), k(.6, 'thresh', perch=1, x=.4, y=.5, b=.9, r=1, w=.6), k(.78, 'thresh', perch=1, y=-.3, b=-.6, w=1), k(.92, eye='^')],
        [], g='show', act=('dance', 'steps'), prefer=['happy'])
    return o


def mud_hut():
    # Drawing (82 x 48 cells, 9.3 px a row, standing line row 44): thatch roof rows 8-24 (looked at), eave beam rows 26-27 (168-158 px); left wall corner of
    # woven stakes `!|/|` cols 9-18 rows 29-43; left window frame cols 12-26 rows 28-37 (shutters `//`, rail row 34 at 93 px, lower frame row 37 at 65 px,
    # sill `===` row 39 at 47 px); door cols 28-53 (jambs, panel rails rows 28 31 34 37 40, ring knob row 32 at 112 px, studs row 38 at 56 px, latch
    # `.---||` row 39 at 47 px, foot strip row 41, lip row 42 at 19 px, step row 43 at 9 px, threshold row 44); right window cols 56-72 the same (sill row 39);
    # daub bumps `~` `_..` at the base (rows 40-43); two pots `(o)` `(__)` with sprouts at cols 62-70 rows 42-44.
    P = pm('mud_hut')
    o = Obj('mud_hut', 'placed',
            fields=dict(heat=(0, 0, 1), leaves=(0, 0, 1), drift=(0, 0, 1)),
            physics=[('heat', 'rate', .0007, 'sun'), ('heat', 'rate', -.0005, '!sun'), ('leaves', 'rate', .002, 'fall'), ('leaves', 'rate', -.001, 'windy'),
                     ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm')],
            effects=dict(pat=[('obj.condition', 'add', .15)], scrub=[('obj.dirt', 'add', -.25)], chip=[('obj.dirt', 'add', -.2)], wipe=[('obj.dirt', 'add', -.15)],
                         fan=[('obj.wetness', 'add', -.3)], spray=[('obj.wetness', 'add', .12)], dent=[('obj.condition', 'add', -.15)],
                         crumble=[('obj.condition', 'add', -.12)], rake=[('leaves', 'mul', .3)], kick=[('drift', 'set', 0)], cool=[('heat', 'add', -.25), ('need.energy', 'add', 2)],
                         bask=[('heat', 'add', -.2)], tidy=[('need.cleanliness', 'add', 1)], laugh=[('need.fun', 'add', 2)], scuff=[('obj.dirt', 'add', .12)]),
            anchors=dict(stake_l=P(12, 43), stake_l2=P(13, 38), wattle_hi=P(11, 33), sill_l=P(18, 39, 'surface'), sill_r=P(62, 39, 'surface'), frame_l=P(19, 37),
                         frame_r=P(63, 37), rail_l=P(18, 34), rail_r=P(63, 34), jamb_l=P(29, 40), rail_low=P(40, 40), stud_d1=P(36, 38), stud_d2=P(49, 38), latch=P(45, 39),
                         knob=P(35, 32), panel_mid=P(40, 35), door_foot=P(44, 41), lip_a=P(35, 42, 'surface'), lip_b=P(47, 42, 'surface'), step_a=P(36, 43, 'surface'),
                         step_b=P(46, 43, 'surface'), thresh=P(41, 44, 'surface'), lump_l=P(20, 43), daub_l=P(24, 41), daub_r=P(58, 41), pot_a=P(63, 43), pot_b=P(68, 43),
                         sprout=P(66, 42), eave=P(35, 26), thatch=P(40, 25)))
    # ---------------- care
    o.r('pat_the_daub_smooth', 'Patting the soft daub flat beside the door with both wings, humming', 22, 'wing',
        [k(.09, 'daub_l', reach=.6, x=.5, y=.7, b=.3), k(.25, 'daub_l', reach=1, x=.8, y=.9, b=.8, l=1, mark='pap'), k(.43, 'lump_l', reach=1, x=.9, y=1.2, b=1.1, r=1, mark='pap'), k(.61, 'daub_l', reach=1, x=.7, y=.8, b=.5, l=1, mark='pap'), k(.8, eye='^')],
        [(.61, 'pat')], g='care', act=('pat', 'daub'), when=['obj_wetness>.3', 'obj_condition<.7'], say=["Wall smooth. Slightly duck-shaped. Calling it art.", "Patted it flat. Wall feels loved. Wall is mud."])
    o.r('scrub_the_door_panels', 'Scrubbing the door panels with a wing until the old marks are only memories', 20, 'wing',
        [k(.08, 'rail_low', reach=.6, x=.6, y=.5, b=.3), k(.26, 'stud_d1', reach=1, x=.9, y=.7, b=.7, l=1), k(.44, 'rail_low', reach=1, x=1, y=.9, b=.2, r=1, mark='skrk'), k(.64, 'stud_d2', reach=1, x=.8, y=.7, b=.8, l=1, mark='skrk'), k(.84, eye='^')],
        [(.44, 'scrub')], g='care', act=('scrub', 'panels'), when=['obj_dirt>.3'])
    o.r('flap_the_daub_dry', 'Flapping both wings at the wet daub to hurry the drying along', 24, 'none',
        [k(.1, 'daub_r', x=-.2, y=.5, b=.2, w=.5), k(.3, 'daub_r', x=-.4, y=.4, b=.9, w=1, mark='fwp'), k(.5, 'daub_r', x=-.5, y=.3, b=.2, w=.3, mark='fwp'), k(.7, 'daub_r', x=-.4, y=.4, b=.9, w=1, l=1, mark='fwp'), k(.88, x=.1, eye='^')],
        [(.5, 'fan')], g='care', act=('dry', 'daub'), when=['obj_wetness>.3'], say=["Flapped it dry. Mud is slow. I am slower.", "Wings aching. Wall drier. Zero thanks, as usual."])
    o.r('chip_dried_crumbs_off_sill', 'Chipping the dried crumbs off the left sill with the edge of his bill', 16, 'none',
        [k(.1, 'sill_l', x=.8, y=.4, b=.3), k(.28, 'sill_l', x=1.3, y=.7, b=.6, mark='tk'), k(.48, 'frame_l', x=1.4, y=.9, b=.9, l=1, mark='tk'), k(.68, 'sill_l', x=1, y=.5, b=.4, r=1), k(.86, eye='^')],
        [(.48, 'chip')], g='care', act=('chip', 'sill'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('tuck_the_right_pot_straight', 'Shouldering both pots straight again so the sprouts face the road', 18, 'none',
        [k(.1, 'pot_a', x=.5, y=.8, b=.6, l=1), k(.3, 'pot_a', x=1.1, y=1.4, b=1, mark='scrt'), k(.5, 'sprout', x=.9, y=-.3, b=.2, r=1), k(.7, 'pot_b', x=1.2, y=1.5, b=1.1, mark='scrt'), k(.88, x=.1, eye='^')],
        [(.5, 'tidy')], g='care', act=('straighten', 'pots'), say=["Pots straight. Sprouts nod in hut-approved agreement.", "Shoved them into line. They shoved back, politely."])
    o.r('wipe_the_right_sill', 'Wiping the right sill clean with the flat of a wing in three long strokes', 16, 'wing',
        [k(.1, 'sill_r', reach=.5, x=.3, y=.4, b=.2), k(.3, 'sill_r', reach=1, x=.6, y=.5, b=.5, r=1, mark='shk'), k(.5, 'frame_r', reach=1, x=.5, y=.6, b=.7, l=1, mark='shk'), k(.72, 'sill_r', reach=.8, x=.3, y=.3, b=.3), k(.9, eye='-')],
        [(.5, 'wipe')], g='care', act=('wipe', 'sill'), when=['obj_dirt>.5'], ages=GROWN)
    # ---------------- use
    o.r('rap_the_lower_panel', 'Rapping the lower door panel with his bill and listening for any reply', 20, 'none',
        [k(.09, 'rail_low', x=1.1, y=.9, b=.5, l=1, mark='tok'), k(.27, 'rail_low', x=1.2, y=1, b=.7, mark='tok'), k(.47, x=-.7, y=-.3, b=-.2, w=.4, eye='O', mark='Anyone?'), k(.67, x=.3, y=.4, b=.9, r=1, eye='-', mark='...'), k(.86, eye='^')],
        [], g='use', act=('knock', 'panel'), prefer=['lonely'], say=["Mud walls. Door did not mind. Nobody home anyway.", "Knocked hard. Hut stayed calm. Annoying."])
    o.r('hook_and_pull_the_latch', 'Hooking the latch under his bill and pulling until the door shudders', 18, 'none',
        [k(.1, 'latch', x=.6, y=.9, b=.4), k(.28, 'latch', x=1.3, y=1.2, b=.9, l=1, mark='hup'), k(.46, 'latch', x=1.5, y=1.4, b=1.3, r=1, mark='RRRK'), k(.66, 'door_foot', x=-.6, y=.3, b=-.4, w=.8, eye='-'), k(.86, eye='^')],
        [], g='use', act=('pull', 'latch'), prefer=['curious'], obj=[(.28, dict(shake=.2)), (.46, dict(shake=.7)), (.66, dict(shake=.1))], say=["Latch held. Door held. Duck held a grudge.", "Pulled until my neck complained. Neck wins."])
    o.r('peer_at_left_frame', 'Pressing his bill up to the lower window frame and squinting at the dark', 22, 'none',
        [k(.1, x=.3, y=-.3, b=-.2), k(.28, 'frame_l', x=1.4, y=-.6, b=.3, eye='O'), k(.5, 'frame_l', x=1.5, y=-.7, b=.4, l=1, eye='>', mark='hm'), k(.7, 'frame_l', x=1.4, y=-.5, b=.4, eye='-'), k(.88, x=.2, eye='-')],
        [], g='use', act=('peer', 'window'), ages=GROWN, prefer=['curious'])
    o.r('shout_at_the_right_window', 'Cupping a wing at the right window and shouting that dinner is ready', 20, 'wing',
        [k(.1, 'sill_r', reach=.6, x=.2, y=-.4, b=.2), k(.3, 'sill_r', reach=1, x=.7, y=-1, b=-.3, mark='DINNER'), k(.5, 'frame_r', reach=1, x=.8, y=-1.1, b=-.4, eye='O', mark='DINNER!'), k(.7, 'frame_r', reach=.6, x=-.2, y=.4, b=.7, eye='-', mark='...')],
        [], g='use', act=('shout', 'window'), ages=GROWN, prefer=['lonely'], say=["No dinner existed. Pure theatre.", "Someone owes me an answer. Or a bun."])
    o.r('sniff_the_daub_for_straw', 'Sniffing along the daub at the left wall and picking out straw by smell', 18, 'none',
        [k(.1, 'daub_l', x=.5, y=.9, b=.4), k(.3, 'lump_l', x=1.2, y=1.3, b=.8, mark='snf'), k(.5, 'daub_l', x=1.4, y=1.1, b=.7, l=1, mark='snf snf'), k(.7, x=-.6, y=-.2, w=.5, eye='>', mark='straw'), k(.88, eye='-')],
        [], g='use', act=('sniff', 'daub'), prefer=['curious'], say=["Mud, straw, history. Mostly mud.", "Sniffed a wall. Smelled of cows. Hut has range."])
    o.r('shove_the_door_with_a_shoulder', 'Putting his full shoulder to the door to see whether the hut gives', 22, 'none',
        [k(.09, x=-.2, y=.2, b=-.3), k(.27, 'panel_mid', x=1.2, y=.7, b=1.2, l=1, mark='hnnh'), k(.45, 'panel_mid', x=1.4, y=.9, b=1.6, r=1, mark='HNNNH'), k(.62, 'panel_mid', x=1, y=.5, b=.7), k(.8, x=-.9, y=-.6, b=-.4, w=1, eye='-')],
        [], g='use', act=('push', 'door'), ages=GROWN, obj=[(.27, dict(sway=.1)), (.45, dict(shake=.4)), (.62, dict(sway=0))], say=["Hut did not give. Hut has the whole county behind it.", "Shoulder sore. Door fresh. Rematch tomorrow."])
    # ---------------- play
    o.r('hop_the_sills', 'Hopping up to the left sill and across to the right one with a flap', 22, 'none',
        [k(.08, 'sill_l', perch=1, y=-.3, b=-.7, w=.6), k(.24, 'sill_l', perch=1, x=.5, y=.4, b=.8, l=1), k(.44, 'sill_r', perch=1, x=-.4, y=-.6, b=-1, w=1, mark='hup'), k(.62, 'sill_r', perch=1, y=.5, b=.9, r=1), k(.82, y=-.4, b=-.8, w=.9, eye='^')],
        [(.62, 'laugh')], g='play', act=('hop', 'sill'), ages=GROWN, prefer=['young', 'happy'])
    o.r('run_the_stakes', 'Running past the woven stakes with his bill out, rattling every one', 18, 'none',
        [k(.08, 'stake_l', x=.9, y=1.1, b=.5, mark='tk'), k(.26, 'stake_l2', x=1, y=.6, b=-.2, l=1, mark='tk tk'), k(.44, 'wattle_hi', x=.8, y=-.8, b=-.7, r=1, mark='tk'), k(.62, 'stake_l2', x=1.1, y=.7, b=.2, l=1, mark='tk'), k(.82, x=.2, w=.8, eye='^')],
        [], g='play', act=('race', 'stakes'), prefer=['young'], obj=[(.26, dict(shake=.2)), (.44, dict(shake=.3))])
    o.r('hide_in_the_stake_corner', 'Flattening himself against the woven corner and bursting out with a rattle', 20, 'none',
        [k(.1, 'stake_l', x=-.7, y=.6, b=.6), k(.3, 'stake_l', x=-.8, y=1.1, b=1.3, l=1, eye='-'), k(.5, 'stake_l2', x=-.8, y=1.2, b=1.4, r=1, eye='-', mark='...'), k(.66, 'stake_l2', x=1.4, y=-1.1, b=-1.2, w=1, eye='O', mark='RAWR'), k(.84, y=.4, b=.4, eye='^')],
        [], g='play', act=('hide', 'corner'), prefer=['young'], say=["Ambush. Corner approved. Corner is mud-based.", "Burst out. Stakes rattled. Nobody else cared."])
    o.r('mud_boat_the_threshold', 'Skating along the threshold on his belly, bill out, making boat noises', 18, 'none',
        [k(.1, 'thresh', x=.4, y=.6, b=.6), k(.3, 'thresh', x=1, y=1.3, b=1.7, w=.4, mark='vroom'), k(.5, 'thresh', x=1.4, y=1.8, b=1.9, w=.8, l=1, r=1, mark='VROOM'), k(.7, 'thresh', x=.8, y=1, b=1.1, w=.4), k(.88, y=.3, b=.2, eye='^')],
        [(.5, 'scuff')], g='play', act=('float', 'threshold'), prefer=['young', 'happy'], say=["Belly boat. Threshold sea. Sea disappointed.", "Slid for one metre. Counts as a voyage."])
    o.r('drum_the_pots', 'Drumming a quick beat along the rims of both pots with his bill', 20, 'none',
        [k(.07, 'pot_a', x=.6, y=.5, b=.3), k(.2, 'pot_a', x=1.1, y=1.3, b=.9, mark='tok'), k(.34, 'sprout', x=.9, y=.1, b=-.4, l=1, mark='tak'), k(.5, 'pot_b', x=1.3, y=1.4, b=.8, r=1, mark='tok tok'), k(.66, 'pot_b', x=.8, y=.4, b=-.5, l=1, mark='TAK'), k(.82, 'pot_a', x=1.2, y=1.2, b=.6, r=1, mark='tok'), k(.94, eye='^')],
        [(.66, 'laugh')], g='play', act=('drum', 'pots'), prefer=['happy'])
    o.r('walk_the_left_sill', 'Walking the left sill end to end with his wings out like a plank walker', 22, 'none',
        [k(.08, 'sill_l', perch=1, y=-.2, w=.8, b=.2), k(.26, 'sill_l', perch=1, x=.5, y=.3, b=.6, w=1, r=1), k(.46, 'frame_l', perch=0, x=-.3, y=.4, b=.7, w=1, l=1, mark='whoa'), k(.66, 'sill_l', perch=1, x=.3, y=-.3, b=-.4, w=.7), k(.86, eye='^')],
        [], g='play', act=('balance', 'sill'), ages=GROWN, prefer=['young'])
    # ---------------- test
    o.r('tap_the_daub_for_hollow', 'Tapping the daub beside the right window to hear where it has come away', 18, 'none',
        [k(.09, 'daub_r', x=1.3, y=1, b=.6, mark='tok'), k(.27, 'daub_r', x=.9, y=-.4, b=-.4, l=1, mark='tok'), k(.46, x=-.4, y=-.7, w=.7, eye='-'), k(.64, 'daub_r', x=1.5, y=1.2, b=.8, r=1, mark='tonk'), k(.82, eye='^')],
        [], g='test', act=('tap', 'daub'), say=["Sounds hollow behind that bit. Probably my head.", "Tap, tap, tonk. A wall with feelings."])
    o.r('count_the_stakes', 'Touching each woven stake in order from the ground up and counting aloud', 22, 'none',
        [k(.08, 'stake_l', x=.9, y=1.5, b=.7, mark='1'), k(.25, 'stake_l2', x=1.1, y=.8, b=.2, r=1, mark='2'), k(.42, 'wattle_hi', x=.7, y=-.9, b=-.8, l=1, mark='3'), k(.6, 'wattle_hi', x=.9, y=-1.1, b=-1, w=.6, mark='4'), k(.8, x=-.5, y=.4, b=.5, eye='-', mark='four')],
        [], g='test', act=('count', 'stakes'), ages=GROWN, prefer=['curious'])
    o.r('press_a_bill_print', 'Pressing his bill against the soft daub and leaning back to admire the print', 18, 'none',
        [k(.1, 'daub_l', x=.6, y=.8, b=.4), k(.3, 'daub_l', x=1.6, y=1.6, b=1.2, mark='squ'), k(.5, 'daub_l', x=-.4, y=-.2, b=.1, w=.5, eye='O'), k(.7, 'daub_l', x=.7, y=1.1, b=.9, l=1, eye='^', mark='ha')],
        [(.3, 'scuff')], g='test', act=('press', 'daub'), when=['obj_wetness>.3'], prefer=['curious'], say=["Signed it. Bill-shaped. Archaeology will love this.", "Daub remembers. Daub is a snitch."])
    o.r('nibble_a_daub_crumb', 'Nibbling a dry crumb of daub, chewing hard, and rating it', 18, 'none',
        [k(.1, 'lump_l', x=.6, y=1.2, b=.8), k(.3, 'lump_l', x=1.5, y=1.8, b=1.4, mark='crk'), k(.5, 'lump_l', x=.3, y=.4, b=.3, l=1, eye='-', mark='chew'), k(.7, x=-.7, y=-.4, w=.8, eye='>', mark='grit')],
        [(.3, 'crumble')], g='test', act=('taste', 'daub'), say=["Straw and grit. Two stars. Crunch bonus.", "Tastes like the wall. Rude to eat the wall."])
    o.r('size_up_the_two_windows', 'Marching between the two window sills and squinting at which one sits higher', 24, 'none',
        [k(.08, 'sill_l', x=.4, y=-.6, b=-.5), k(.26, 'sill_l', x=.8, y=-.9, b=-.9, w=.7, mark='hm'), k(.5, 'sill_r', x=.8, y=-.9, b=-.9, l=1, mark='hmm'), k(.7, 'sill_r', x=-.3, y=.5, b=.6, w=.9, r=1, eye='-', mark='same')],
        [], g='test', act=('compare', 'windows'), ages=GROWN)
    o.r('prod_the_thatch_edge', 'Prodding the thatch edge with a twig to hear whether anything rustles', 22, 'twig',
        [k(.1, 'eave', reach=.6, x=.3, y=-.8, b=-.4), k(.3, 'thatch', reach=1, x=.7, y=-1.2, b=-.8, mark='shk'), k(.5, 'thatch', reach=1, x=.8, y=-1.3, b=-.6, l=1, mark='shk shk'), k(.7, 'eave', reach=.8, x=-.3, y=-.3, b=.2, eye='-', mark='nothing')],
        [], g='test', act=('prod', 'thatch'), ages=GROWN, obj=[(.3, dict(shake=.2))])
    # ---------------- rest
    o.r('lean_against_the_warm_daub', 'Leaning his back against the sun-warmed daub and letting it hold him up', 26, 'none',
        [k(.1, 'daub_r', x=-.3, y=.3, b=.3), k(.28, 'daub_r', x=-.5, y=.7, b=.8, eye='-'), k(.52, 'daub_r', x=-.6, y=.8, b=1, eye='-', mark='ahh'), k(.76, 'daub_r', x=-.4, y=.4, b=.5, l=1, eye='^')],
        [(.52, 'cool')], g='rest', act=('lean', 'daub'), when=['heat>.3', 'sun'], say=["Warm wall. Better than most relationships.", "Leaned. Wall held. Rare reliability."])
    o.r('sit_on_the_right_sill', 'Sitting on the right sill with his feet tucked, letting the afternoon go by', 30, 'none',
        [k(.07, 'sill_r', perch=1, x=.4, y=-.3, b=-.4, w=.4), k(.2, 'sill_r', perch=1, x=-.2, y=.7, b=1.3, eye='-'), k(.42, 'sill_r', perch=1, x=-.3, y=.9, b=1.5, l=1, eye='-', mark='...'), k(.66, 'sill_r', perch=1, x=.1, y=.3, b=.8, r=1, w=.5, eye='-'), k(.88, 'sill_r', perch=1, y=-.2, b=.2, eye='^')],
        [], g='rest', act=('sit', 'sill'), ages=GROWN, say=["Afternoon passed. I did nothing. Good use.", "Feet tucked. Mind empty. Perfect hut posture."])
    o.r('sulk_at_the_stakes', 'Hunching at the stake corner with his back to the whole hut', 26, 'none',
        [k(.06, 'stake_l', x=.5, y=.2, b=.8), k(.22, 'stake_l', x=-.6, y=.8, b=.4, w=.4, eye='-', mark='hmph'), k(.42, 'stake_l2', x=-1, y=1.6, b=1.5, l=1, eye='>'), k(.62, 'stake_l2', x=-.8, y=1.3, b=1.2, r=1, eye='-'), k(.82, 'stake_l', x=-.3, y=.4, b=.6, eye='-')],
        [], g='rest', act=('sulk', 'corner'), prefer=['grumpy', 'sad'], say=["Not speaking to the hut. Hut is not speaking either.", "Sulking in a corner. Corners are underrated."])
    o.r('wait_by_the_door', 'Waiting by the door for the hut owner to come home, any year now', 28, 'none',
        [k(.1, 'lip_a', x=.4, y=.6, b=.5), k(.3, 'lip_a', x=-.4, y=.2, b=.1, l=1, eye='-'), k(.5, 'lip_b', x=.8, y=.9, b=.9, r=1, eye='>', mark='...'), k(.7, 'lip_b', x=-.3, y=.3, b=-.2, w=.6, eye='-'), k(.9, 'lip_a', y=.5, eye='-')],
        [], g='rest', act=('wait', 'door'), prefer=['lonely'])
    o.r('toast_his_feet_at_the_step', 'Toasting one foot and then the other against the sun-baked step', 26, 'none',
        [k(.06, 'step_a', x=.5, y=.8, b=.2, l=1), k(.2, 'step_a', x=.7, y=1.2, b=.9, l=1, eye='-', mark='ahh'), k(.36, 'step_a', x=.2, y=.5, b=.3, w=.4), k(.54, 'step_b', x=.7, y=1.2, b=.9, r=1, eye='^'), k(.72, 'step_b', x=.3, y=.4, b=.4, l=1, eye='-'), k(.9, eye='-')],
        [(.54, 'bask')], g='rest', act=('warm', 'step'), when=['heat>.3', 'sun'])
    o.r('prop_on_the_door_jamb', 'Propping himself against the door jamb with his arms folded like a bouncer', 24, 'none',
        [k(.07, 'jamb_l', x=-.8, y=.2, b=1.1, l=1), k(.24, 'jamb_l', x=.9, y=.4, b=-.3, eye='-'), k(.42, 'jamb_l', x=-.3, y=1.4, b=1.7, w=.4, eye='>', mark='hm'), k(.6, 'jamb_l', x=-.9, y=.9, b=.4, r=1, eye='-'), k(.8, 'jamb_l', x=.3, y=-.2, b=-.6, w=1, eye='-'), k(.93, eye='-')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    # ---------------- weather
    o.r('kick_the_drift_off_the_step', 'Kicking the snow drift off the step in three vicious sweeps', 18, 'none',
        [k(.1, 'step_b', x=.3, y=.5, b=.4), k(.28, 'step_b', x=.4, y=.8, b=.7, l=1, mark='fff'), k(.46, 'step_a', x=.4, y=.8, b=.8, r=1, mark='FFF'), k(.64, 'step_a', x=.3, y=.5, b=.4, l=1, mark='ff'), k(.84, eye='^')],
        [(.46, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Step cleared. Boots would help. I have no boots.", "Snow gone. Toes gone too. Fair swap."])
    o.r('rake_leaves_to_the_stakes', 'Raking the blown leaves toward the stakes with both feet', 20, 'none',
        [k(.1, 'lump_l', x=.4, y=.9, b=.5), k(.28, 'stake_l', x=.5, y=1.2, b=1, l=1, mark='sh sh'), k(.46, 'stake_l', x=.5, y=1.3, b=1.1, r=1, mark='sh sh'), k(.66, 'lump_l', x=.3, y=.8, b=.6, l=1), k(.84, eye='^')],
        [(.46, 'rake')], g='weather', act=('rake', 'leaves'), when=['leaves>.3'], say=["Leaves in a corner. Wind in a mood. Standoff.", "Raked them. Wind is already redoing it. Spite."])
    o.r('cool_belly_on_the_shade_wall', 'Pressing his belly flat to the shady side of the daub to cool off', 22, 'none',
        [k(.1, 'daub_l', x=.2, y=.4, b=.4), k(.3, 'daub_l', x=-.3, y=.9, b=1.1, w=.7, eye='-'), k(.5, 'daub_l', x=-.4, y=1, b=1.3, w=.4, l=1, mark='ahhh'), k(.74, 'daub_l', x=-.2, y=.5, b=.6, r=1, eye='^')],
        [(.5, 'bask')], g='weather', act=('cool', 'daub'), when=['heat>.5'])
    o.r('listen_to_rain_on_thatch', 'Standing very still and listening to the rain drum overhead', 24, 'none',
        [k(.1, 'lip_a', x=.2, y=-.6, b=-.2), k(.3, 'lip_a', x=-.3, y=-1, b=-.6, w=.8, eye='-', mark='...'), k(.55, 'lip_a', x=-.4, y=1.1, b=1.2, l=1, eye='O', mark='pat pat'), k(.8, 'lip_a', x=-.2, y=-.4, b=-.1, eye='^')],
        [], g='weather', act=('listen', 'thatch'), when=['obj_wetness>.3'], say=["Rain on thatch. Free percussion. Mud-hut-only seats.", "Drip, drip, drip. The hut applauds slowly."])
    o.r('shelter_at_the_jamb', 'Pressing flat against the door jamb with wings over his head as the rain drums', 30, 'none',
        [k(.1, 'jamb_l', x=.2, y=.5, b=.4), k(.3, 'jamb_l', x=-.5, y=1, b=1, w=1, eye='-'), k(.55, 'jamb_l', x=-.6, y=1.2, b=1.3, w=1, r=1, eye='>', mark='drip'), k(.82, 'jamb_l', x=-.3, y=.6, b=.5, w=.6, eye='-')],
        [(.55, 'spray')], g='weather', act=('shelter', 'jamb'), when=['wet', 'obj_wetness<.6'])
    o.r('hold_the_shutter_in_the_gale', 'Holding the left shutter shut with a wing against the gale', 24, 'wing',
        [k(.1, 'frame_l', reach=.5, x=.3, y=-.4, b=.3), k(.3, 'frame_l', reach=1, x=-.2, y=-.7, b=.9, mark='hnn'), k(.5, 'rail_l', reach=1, x=-.3, y=-.8, b=1.1, l=1, mark='HNN'), k(.74, 'frame_l', reach=.7, x=.2, y=-.3, b=.4, r=1, eye='^')],
        [], g='weather', act=('brace', 'shutter'), when=['windy', 'obj_condition<.8'], ages=GROWN, obj=[(.3, dict(shake=.5)), (.5, dict(shake=.8)), (.74, dict(shake=.1))])
    # ---------------- mishap
    o.r('slide_off_the_wet_step', 'Skidding along the wet step and landing flat with a dignified splat', 16, 'none',
        [k(.09, 'step_a', x=.3, y=.4, b=.5, r=1), k(.25, 'step_b', x=1, y=.7, b=-.3, l=1, w=.8, eye='O'), k(.43, 'step_b', x=-1, y=1.2, b=1.3, r=1, w=1, mark='WHEE'), k(.6, 'step_a', x=-.3, y=1.7, b=1.8, eye='@', mark='*splat*'), k(.8, y=.5, b=.6, eye='-')],
        [(.43, 'scuff')], g='mishap', act=('slip', 'step'), when=['obj_wetness>.5'], say=["Mud floor met mud duck. Even match.", "Slipped elegantly. The elegance was invisible."])
    o.r('walk_into_the_corner_stakes', 'Marching round the corner at full tilt and meeting the woven stakes', 18, 'none',
        [k(.1, x=.3, y=.3, b=.5, l=1), k(.3, x=.9, y=.5, b=.2, r=1), k(.5, 'wattle_hi', x=1.8, y=-.9, b=-1, w=.8, eye='@', mark='BONK'), k(.7, 'stake_l2', x=-1, y=.6, b=.7, l=1, eye='O'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'stakes'), say=["Stakes were there. Corner did not warn me.", "Face first into hut. Hut did not apologise."])
    o.r('knock_off_a_daub_flake', 'Hammering one spot too hard so a flake of daub drops and the wall looks hurt', 16, 'none',
        [k(.1, 'daub_r', x=.8, y=.7, b=.3, l=1), k(.28, 'daub_r', x=1.6, y=1.9, b=.9, mark='TOK'), k(.46, 'daub_r', x=1.7, y=2, b=1.2, r=1, eye='@', mark='CRK'), k(.66, x=-.7, y=.1, b=-.4, w=.8, eye='O'), k(.84, eye='-')],
        [(.46, 'dent')], g='mishap', act=('peck', 'flake'), prefer=['grumpy'], say=["Bit fell off. Wall will manage. Wall must.", "Too hard. Hut is mud. Mud keeps the receipts."])
    o.r('bill_caught_between_stakes', 'Poking his bill between two stakes and discovering the gap bites back', 26, 'none',
        [k(.07, 'stake_l2', x=.4, y=.5, b=.8, l=1), k(.2, 'stake_l2', x=1.6, y=.7, b=.4, eye='O', mark='mm'), k(.38, 'stake_l2', x=1.8, y=.9, b=1.4, r=1, eye='@', mark='mmf!'), k(.55, 'stake_l', x=1.9, y=1.7, b=1.8, l=1, w=.6, mark='mmFF'), k(.72, 'stake_l', x=-.7, y=.3, b=-.6, w=1, mark='POP'), k(.9, x=-.2, y=.6, eye='>')],
        [], g='mishap', act=('stuck', 'stakes'), prefer=['curious'], say=["Stakes took my bill. Stakes returned it. Bruised.", "Bill stuck. Pride stuck deeper."])
    o.r('stub_a_toe_on_a_pot', 'Stubbing a toe against the wide pot and hopping about in a furious circle', 18, 'none',
        [k(.07, 'pot_b', x=.8, y=.9, b=.9, r=1), k(.22, 'pot_b', x=1.5, y=1.6, b=1.5, l=1, mark='OW'), k(.38, 'sprout', x=-.9, y=-.3, b=-1.1, r=1, w=1, eye='O', mark='ow ow'), k(.54, 'pot_a', x=.4, y=.8, b=-.5, l=1, w=.6, mark='ow'), k(.7, 'pot_a', x=.9, y=.3, b=-.8, r=1, w=.9, mark='ow!'), k(.86, eye='>')],
        [], g='mishap', act=('kick', 'pot'), say=["Pot is fine. Duck is a bruise with a bill.", "Toe lost the argument. Pot gloated."])
    o.r('stamp_at_the_shut_door', 'Stamping up and down at the lip when the door still will not open', 16, 'none',
        [k(.09, 'lip_a', x=.4, y=.5, b=.5, l=1), k(.25, 'lip_a', x=.5, y=.6, b=.9, r=1, mark='STOMP'), k(.43, 'lip_b', x=.5, y=.6, b=1, l=1, mark='STOMP'), k(.62, 'lip_b', x=.9, y=.3, b=.4, w=.8, eye='>'), k(.82, eye='-')],
        [], g='mishap', act=('stamp', 'lip'), prefer=['grumpy'])
    # ---------------- show
    o.r('pose_in_the_doorway', 'Posing at the threshold like the owner of an enormous mud empire', 24, 'none',
        [k(.06, 'thresh', x=1.1, y=-.8, b=-.3, w=.4), k(.22, 'thresh', x=-.7, y=.9, b=1.1, w=.9, l=1, eye='^'), k(.4, 'thresh', x=1.5, y=-1.1, b=-.5, w=1, eye='-', mark='ahem'), k(.58, 'thresh', x=-.2, y=.4, b=.6, w=.5, r=1), k(.78, 'thresh', x=.8, y=-.6, b=-.2, w=.8, eye='^'), k(.92, eye='-')],
        [], g='show', act=('pose', 'doorway'), prefer=['happy'], say=["Lord of the daub. Duke of damp. Do bow.", "Empire of mud. Population: one duck."])
    o.r('bow_to_the_hut', 'Bowing deeply to the door, as to a very old and very damp relative', 22, 'none',
        [k(.07, 'knob', x=.2, y=-.4, b=-.3, w=.4), k(.24, 'knob', x=.9, y=1.4, b=.9, w=.5, eye='-'), k(.42, 'knob', x=1.2, y=2.1, b=1.8, w=1, mark='grandpa'), k(.6, 'knob', x=.8, y=1.2, b=.8, r=1), k(.78, 'knob', x=-.2, y=-.4, b=-.4, w=.6, eye='^'), k(.92, eye='-')],
        [], g='show', act=('bow', 'door'))
    o.r('present_the_hut', 'Sweeping a wing along the whole front of the hut like a tour guide', 24, 'wing',
        [k(.07, 'stake_l2', reach=.5, x=.7, y=-.5, b=.4, l=1), k(.22, 'sill_l', reach=1, x=.2, y=-.9, b=-.5, mark='behold'), k(.4, 'rail_low', reach=1, x=.9, y=-.3, b=.6, mark='authentic'), k(.58, 'rail_r', reach=1, x=.3, y=-.8, b=-.6, r=1, mark='thatched'), k(.76, 'sill_r', reach=.6, x=.1, y=.5, b=.9, eye='^'), k(.92, eye='-')],
        [], g='show', act=('present', 'hut'), ages=GROWN, say=["Authentic. Eco. Slightly soggy. Book now.", "Fine property. Only two sills, one duck, no taxes."])
    o.r('argue_with_the_latch', 'Arguing with the latch, pecking it for every point and conceding none', 24, 'none',
        [k(.06, 'latch', x=1.1, y=.4, b=.9, l=1), k(.2, 'latch', x=1.5, y=1.1, b=.5, mark='no'), k(.36, 'door_foot', x=.4, y=.3, b=1.3, r=1, w=.5, mark='YES'), k(.52, 'latch', x=1.7, y=1.5, b=1.1, l=1, mark='no'), k(.68, 'door_foot', x=-.6, y=-.2, b=-.3, w=1, eye='>'), k(.84, 'latch', x=1.2, y=.6, b=.4, r=1, mark='!'), k(.94, eye='-')],
        [], g='show', act=('argue', 'latch'), prefer=['grumpy'], say=["Latch refuses to explain. Latch is a coward.", "Won on points. Latch does not do points."])
    o.r('sing_up_at_the_thatch', 'Singing up at the thatch with a wing flung wide and no mercy', 24, 'none',
        [k(.1, 'lip_b', x=.3, y=-.5, b=.3), k(.3, 'lip_b', x=-.4, y=-1, b=-.6, w=.9, mark='laa'), k(.5, 'lip_b', x=-.5, y=-1.3, b=-.9, w=1, l=1, eye='^', mark='LAAA'), k(.72, 'lip_b', x=.3, y=.4, b=.7, r=1, eye='-', mark='...'), k(.9, eye='-')],
        [], g='show', act=('sing', 'thatch'), prefer=['happy'])
    o.r('dance_around_the_pots', 'Dancing a jig between the two pots and the step', 22, 'none',
        [k(.08, 'step_b', perch=1, y=-.5, b=-.8, l=1, w=.7), k(.25, 'pot_a', x=.6, y=.6, b=.8, r=1, w=1.2), k(.42, 'pot_b', x=-.6, y=-.5, b=-.8, l=1, w=1, mark='tada'), k(.6, 'sprout', x=.5, y=.6, b=.9, r=1, w=.5), k(.78, 'step_b', perch=1, y=-.4, b=-.6, l=1, w=.9), k(.92, eye='^')],
        [], g='show', act=('dance', 'pots'), prefer=['happy'])
    return o


def stone_house():
    # Drawing (96 x 58 cells, 9.3 px a row, standing line row 54): eave beams rows 51-53 (looked at); two wings of dressed stone (courses every 3 rows
    # with `.:'` flecks), each with a shuttered window (frame row 33 / 44, rail row 39 at 140 px, lower sill rows 45-46 at 84-74 px); a lantern `.-.` `|*|` `'-'`
    # at cols 38-40 rows 35-37 (168 px); centre door cols 40-62 (jambs, panel rails rows 34 39 44 49, ring knobs rows 35 43 51, studs rows 41 48, foot strip rows
    # 50-51, lip row 52 at 19 px, step row 53 at 9 px, wide threshold slab row 54 and 56); stone base rows 47-54 with flecks.
    P = pm('stone_house')
    o = Obj('stone_house', 'placed',
            fields=dict(warmth=(0, 0, 1), frost=(0, 0, 1), leaves=(0, 0, 1)),
            physics=[('warmth', 'rate', .0006, 'sun'), ('warmth', 'rate', -.0003, 'night'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('leaves', 'rate', .002, 'fall'), ('leaves', 'rate', -.001, 'windy')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], polish=[('obj.dirt', 'add', -.2)], wipe=[('obj.dirt', 'add', -.15)], dry=[('obj.wetness', 'add', -.3)],
                         spray=[('obj.wetness', 'add', .12)], repoint=[('obj.condition', 'add', .2)], crack=[('obj.condition', 'add', -.15)],
                         scrape=[('frost', 'mul', .2)], chip=[('frost', 'mul', .4)], rake=[('leaves', 'mul', .3)], cool=[('warmth', 'add', -.25), ('need.energy', 'add', 2)],
                         bask=[('warmth', 'add', -.2)], tidy=[('need.cleanliness', 'add', 1)], laugh=[('need.fun', 'add', 2)], scuff=[('obj.dirt', 'add', .12)]),
            anchors=dict(stone_l=P(16, 48), stone_l2=P(26, 48), course_l=P(20, 50), base_l=P(20, 53), found_l=P(15, 54), sill_l=P(22, 46), frame_l=P(21, 44), rail_l=P(21, 39),
                         jamb_l=P(41, 50), rail_door=P(50, 49), knob_hi=P(44, 43), kn_a=P(44, 51), kn_b=P(57, 51), stud_d1=P(46, 48), stud_d2=P(54, 48), door_foot=P(50, 50),
                         lip_a=P(45, 52, 'surface'), lip_b=P(56, 52, 'surface'), step_a=P(45, 53, 'surface'), step_b=P(58, 53, 'surface'), thresh_a=P(50, 54, 'surface'),
                         thresh_b=P(60, 54, 'surface'), stone_r=P(80, 48), stone_r2=P(88, 51), sill_r=P(75, 46), found_r=P(83, 54), jamb_r=P(62, 50), lantern=P(39, 36)))
    # ---------------- care
    o.r('scrub_the_left_stones', 'Scrubbing the left wing stones with a wing, course by course', 21, 'wing',
        [k(.11, 'base_l', reach=.5, x=.5, y=.8, b=.5), k(.26, 'course_l', reach=1, x=.9, y=1, b=.9, l=1), k(.4, 'stone_l', reach=1, x=1, y=.8, b=.3, r=1, mark='skrk'), k(.58, 'stone_l2', reach=1, x=.8, y=.7, b=.9, l=1, mark='skrk'), k(.77, 'course_l', reach=.8, x=.4, y=.5, b=.3), k(.92, eye='^')],
        [(.58, 'scrub')], g='care', act=('scrub', 'stones'), when=['obj_dirt>.3'], say=["Scrubbed it. Stone looks smug. Stone always does.", "Wing sore. Wall clean. Bargain."])
    o.r('polish_the_knob_plates', 'Huffing at the lower knob plates and buffing them bright with a wing', 17, 'wing',
        [k(.13, 'kn_a', reach=.5, x=.3, y=.4, b=.4), k(.31, 'kn_a', reach=1, x=.5, y=.6, b=.8, mark='shk'), k(.5, 'kn_b', reach=1, x=.6, y=.7, b=.6, r=1, mark='shk'), k(.72, 'kn_b', reach=.8, x=.3, y=.4, b=.2, l=1), k(.9, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'knob'), when=['obj_dirt>.3'])
    o.r('mop_the_step_dry', 'Mopping the step and the stone lip dry with his breast, grunting', 21, 'none',
        [k(.11, 'step_a', x=.8, y=.3, b=1.1), k(.27, 'step_a', x=1.2, y=.6, b=1.6, mark='hff'), k(.45, 'lip_a', x=1.1, y=.5, b=1.3, l=1), k(.63, 'lip_b', x=1, y=.6, b=1.5, r=1, mark='hff'), k(.8, 'step_b', x=.4, y=.2, b=.7), k(.93, eye='^')],
        [(.45, 'dry')], g='care', act=('dry', 'step'), when=['obj_wetness>.3'], obj=[(.27, dict(shake=.2)), (.63, dict(shake=.2))])
    o.r('press_mortar_back', 'Pressing a crumbled bit of mortar back into its stone seam with his bill', 17, 'none',
        [k(.12, x=.9, y=.6, b=.3), k(.29, 'course_l', x=1.2, y=1.6, b=.9, l=1, mark='nng'), k(.46, x=.2, y=.4, b=-.3), k(.62, 'course_l', x=1.4, y=1.8, b=1.1, r=1, mark='nng'), k(.8, x=.1, y=.3, w=.4, eye='^')],
        [(.62, 'repoint')], g='care', act=('mend', 'mortar'), when=['obj_condition<.6'], say=["Seam sealed. House holds. Nobody thanks the duck.", "Mortar mortared. Poetry in grit."])
    o.r('sweep_dust_off_the_slab', 'Sweeping the dust off the threshold slab with a wing, edge to edge', 17, 'wing',
        [k(.12, 'thresh_a', reach=.5, x=.4, y=.9, b=.6), k(.3, 'thresh_a', reach=1, x=.6, y=1.1, b=1, l=1, mark='fff'), k(.5, 'thresh_b', reach=1, x=.7, y=1.2, b=1.1, r=1, mark='fff'), k(.7, 'thresh_b', reach=.6, x=.2, y=.4, b=.3), k(.9, eye='-')],
        [(.5, 'wipe')], g='care', act=('sweep', 'slab'), when=['obj_dirt>.5'])
    o.r('preen_in_the_polish', 'Smoothing his feathers with the polished knob plate for a mirror', 20, 'none',
        [k(.1, 'kn_a', x=.6, y=.9, b=.4), k(.28, 'kn_a', x=1.1, y=.6, b=.1, w=.6, eye='O'), k(.46, 'kn_b', x=1, y=.8, b=.5, w=.9, l=1, mark='primp'), k(.66, 'kn_b', x=.3, y=-.2, b=-.3, w=.5, r=1, eye='^'), k(.86, eye='-')],
        [(.46, 'tidy')], g='care', act=('groom', 'feathers'), when=['obj_dirt<.4'], prefer=['happy'], say=["Handsome duck. Bent in the middle. Still handsome.", "Plate shows me my best side. All of it."])
    # ---------------- use
    o.r('knock_the_lower_plate', 'Knocking with his bill at the lower knob plate, three slow and one fast', 20, 'none',
        [k(.1, 'kn_a', x=1.1, y=1, b=.6, mark='toc'), k(.25, 'kn_a', x=1.3, y=1.1, b=.8, l=1, mark='toc'), k(.4, 'kn_a', x=1.2, y=1.2, b=1, mark='toc'), k(.54, 'kn_a', x=1.4, y=1.2, b=.9, r=1, mark='tocktock'), k(.7, x=-.7, y=-.4, w=.5, eye='O', mark='Hello?'), k(.88, eye='^')],
        [], g='use', act=('knock', 'plate'), prefer=['lonely'], say=["Stone house. Wood door. Wooden silence.", "Knocked. Echo answered. Echo is rude."])
    o.r('lean_into_the_big_door', 'Putting a shoulder to the heavy door to see if anything inside notices', 22, 'none',
        [k(.08, 'jamb_l', x=-.2, y=.2, b=-.4), k(.24, 'door_foot', x=1, y=.9, b=1.4, l=1, mark='hnnh'), k(.42, 'door_foot', x=1.2, y=1.1, b=1.8, r=1, mark='HNNNH'), k(.6, 'rail_door', x=1.1, y=.8, b=.9), k(.77, x=-1, y=-.6, b=-.5, w=1, eye='-')],
        [], g='use', act=('push', 'door'), ages=GROWN, obj=[(.24, dict(sway=.1)), (.42, dict(shake=.3)), (.6, dict(sway=0))], say=["Door won. It is oak. I am a duck.", "Shoulder sore. Door fresh. Oak has stamina."])
    o.r('peek_at_the_left_window', 'Rising on tiptoe at the left window frame and peering for signs of life', 22, 'none',
        [k(.11, x=.3, y=-.3, b=-.3), k(.28, 'frame_l', x=1.5, y=-.7, b=-.7, eye='O'), k(.46, 'frame_l', x=1.6, y=-.8, b=-.6, l=1, eye='>', mark='hm'), k(.64, 'frame_l', x=1.5, y=-.6, b=-.5, eye='-'), k(.82, x=.2, y=.2, eye='-')],
        [], g='use', act=('peer', 'window'), ages=GROWN, prefer=['curious'])
    o.r('holler_up_at_the_lantern', 'Cupping a wing and hollering up at the lantern as if it had a say', 20, 'twig',
        [k(.1, 'lantern', reach=.6, x=.2, y=-.8, b=-.5), k(.3, 'lantern', reach=1, x=.6, y=-1.2, b=-.8, mark='OI'), k(.5, 'lantern', reach=1, x=.7, y=-1.3, b=-.9, l=1, eye='O', mark='OI!'), k(.72, x=-.2, y=.3, b=.6, eye='-', mark='...')],
        [], g='use', act=('shout', 'lantern'), ages=GROWN, prefer=['lonely'], say=["Lantern does not answer. Lantern is the strong silent type.", "Shouted at a light. Light stayed on. Smug."])
    o.r('haul_the_upper_plate', 'Hanging off the upper door plate to ring the house like a bell', 20, 'none',
        [k(.1, 'knob_hi', x=.6, y=-.8, b=-.5), k(.28, 'knob_hi', x=1.2, y=-.6, b=-.9, w=.6, mark='hup'), k(.46, 'knob_hi', x=1.3, y=-.4, b=.9, l=1, r=1, mark='DONG'), k(.64, 'knob_hi', x=.8, y=.3, b=.3, w=.9, eye='O'), k(.82, eye='^')],
        [], g='use', act=('pull', 'plate'), ages=GROWN, obj=[(.46, dict(shake=.3))], say=["Plate went clunk. House heard. House stayed put.", "Pulled the door plate. Nothing opened. Typical stone."])
    o.r('sniff_the_stone_flecks', 'Sniffing along the left wall flecks to find out who has been here', 20, 'none',
        [k(.09, 'found_l', x=.6, y=1.2, b=.8), k(.26, 'base_l', x=1.2, y=.8, b=.3, mark='snf'), k(.44, 'stone_l', x=1.3, y=.9, b=.4, l=1, mark='snf snf'), k(.63, x=-.5, y=-.2, w=.6, eye='>', mark='cats?'), k(.82, eye='-')],
        [], g='use', act=('sniff', 'flecks'), prefer=['curious'], say=["Moss, damp, and someone's lunch. Good house.", "Sniffed the wall. It smelled back. Intense."])
    # ---------------- play
    o.r('bounce_up_the_step', 'Bouncing from the step to the lip and back like a springboard', 18, 'none',
        [k(.1, 'step_a', perch=1, y=-.4, b=-.9, w=.7), k(.25, 'lip_a', perch=1, y=.5, b=1, l=1), k(.4, 'lip_a', perch=1, x=.5, y=-.7, b=-1.1, w=1, mark='hup'), k(.57, 'step_b', perch=1, y=.5, b=1, r=1), k(.75, 'step_b', y=-.5, b=-.8, w=.9, eye='^')],
        [(.57, 'laugh')], g='play', act=('hop', 'step'), prefer=['young', 'happy'])
    o.r('tick_down_the_courses', 'Running his bill down the left wall and ticking every stone course', 20, 'none',
        [k(.09, 'course_l', x=.9, y=-.9, b=-.6, mark='tk'), k(.25, 'stone_l', x=1, y=.1, b=.2, l=1, mark='tk'), k(.42, 'stone_l2', x=1.1, y=.9, b=.7, r=1, mark='tk'), k(.58, 'base_l', x=1.2, y=1.5, b=1.2, l=1, mark='tk'), k(.76, 'found_l', x=.6, y=.9, b=.4, mark='tk'), k(.92, eye='^')],
        [], g='play', act=('race', 'courses'), prefer=['young'])
    o.r('flatten_at_the_right_wing', 'Flattening against the right wing and leaping out with a startling quack', 20, 'none',
        [k(.1, 'stone_r', x=-.7, y=.5, b=.7, l=1), k(.26, 'stone_r', x=-.9, y=1, b=1.3, eye='-'), k(.44, 'stone_r2', x=-.9, y=1.1, b=1.4, r=1, eye='-', mark='...'), k(.58, x=1.5, y=-1.2, b=-1.1, w=1, eye='O', mark='QUACK'), k(.76, x=.4, y=.5, b=.5, eye='^')],
        [], g='play', act=('hide', 'wing'), prefer=['young'], say=["Quack. House shrugged. House is stone.", "Leapt out. The wing did not flinch. Wing is stone."])
    o.r('balance_the_lip', 'Walking the stone lip heel to toe with his wings held out', 22, 'none',
        [k(.08, 'lip_a', perch=1, y=-.3, w=.9, b=.1), k(.24, 'lip_a', perch=1, x=.4, y=.4, b=.6, w=1, l=1), k(.44, 'lip_b', perch=1, x=-.4, y=.4, b=.8, w=1.1, r=1, mark='whoa'), k(.64, 'lip_b', perch=1, x=.3, y=-.4, b=-.4, w=.8), k(.84, eye='^')],
        [], g='play', act=('balance', 'lip'), ages=GROWN, prefer=['young'])
    o.r('rattle_the_door_studs', 'Rattling a march along the door studs with his bill', 18, 'none',
        [k(.09, 'stud_d1', x=1, y=1, b=.5, mark='tk'), k(.25, 'stud_d2', x=.8, y=.2, b=-.3, l=1, mark='tak'), k(.42, 'stud_d1', x=1.1, y=1, b=.7, r=1, mark='tk tk'), k(.6, 'stud_d2', x=.8, y=.2, b=-.3, l=1, mark='TAK'), k(.8, eye='^')],
        [(.6, 'laugh')], g='play', act=('drum', 'studs'), prefer=['happy'])
    o.r('skid_round_the_slab', 'Skidding in circles round the threshold slab on one foot, arms out', 18, 'none',
        [k(.1, 'thresh_a', x=.4, y=.4, b=.4, l=1), k(.27, 'thresh_b', x=-.7, y=.7, b=.8, w=.9, r=1), k(.45, 'thresh_b', x=.8, y=.4, b=.9, w=1, l=1, eye='@'), k(.62, 'thresh_a', x=-.7, y=.7, b=.7, w=.8, r=1), k(.8, x=.1, y=.2, eye='o')],
        [], g='play', act=('spin', 'slab'), prefer=['young', 'happy'])
    # ---------------- test
    o.r('rap_the_stone_for_a_ring', 'Rapping the right wing stones one after another, listening for a ring', 20, 'none',
        [k(.09, 'stone_r', x=1.3, y=1, b=.6, mark='tok'), k(.25, 'stone_r', x=.9, y=-.3, b=-.5, l=1, mark='tok'), k(.43, 'stone_r2', x=1.4, y=1.2, b=.8, r=1, mark='tok'), k(.6, 'found_r', x=1.2, y=1.6, b=1.2, mark='tok'), k(.78, x=-.6, y=-.6, w=.7, eye='-', mark='dead')],
        [], g='test', act=('tap', 'stones'), say=["Solid. Dead solid. Like the conversation.", "Rapped every stone. All of them said no."])
    o.r('count_the_courses', 'Counting the stone courses with his bill from the ground to the window sill', 24, 'none',
        [k(.08, 'found_l', x=.9, y=1.5, b=.7, mark='1'), k(.24, 'base_l', x=1, y=1, b=.5, r=1, mark='2'), k(.4, 'course_l', x=1.1, y=.2, b=-.3, l=1, mark='3'), k(.56, 'stone_l', x=.8, y=-.3, b=-.7, mark='4'), k(.72, 'sill_l', x=.7, y=-.9, b=-1, w=.7, r=1, mark='5'), k(.9, x=-.4, eye='-', mark='five')],
        [], g='test', act=('count', 'courses'), ages=GROWN, prefer=['curious'])
    o.r('measure_the_sill_against_himself', 'Standing tall at the left sill and settling who is the higher of the two', 20, 'none',
        [k(.11, 'sill_l', x=.2, y=-.6, b=-.8), k(.29, 'sill_l', x=.7, y=-1.1, b=-1.2, w=.7, mark='...'), k(.48, 'sill_l', x=1.1, y=-1.5, b=-1.4, w=1, eye='O', mark='nnng'), k(.68, x=-.7, y=.8, b=.9, eye='-', mark='sill')],
        [], g='test', act=('measure', 'sill'), ages=GROWN, say=["Sill wins by a head. Mine.", "Higher than me. Measured. Resentful."])
    o.r('compare_the_two_wings', 'Marching from the left wing to the right and squinting at which is older', 26, 'none',
        [k(.09, 'stone_l2', x=.5, y=.7, b=.3), k(.24, 'stone_l2', x=1.2, y=.6, b=.9, eye='>', mark='hm'), k(.5, 'stone_r', x=1.1, y=.6, b=.9, l=1, mark='hmm'), k(.7, 'stone_r', x=-.5, y=-.6, b=-.3, w=.9, r=1, eye='-', mark='twins')],
        [], g='test', act=('compare', 'wings'))
    o.r('lick_a_pale_fleck', 'Licking one of the pale flecks of the stone to see if it is salt', 18, 'none',
        [k(.1, 'stone_l', x=.5, y=.7, b=.8), k(.3, 'stone_l', x=1.6, y=1.4, b=1.5, mark='lick'), k(.5, 'stone_l', x=.2, y=.4, b=.4, l=1, eye='-', mark='...'), k(.7, x=-.8, y=-.4, w=.9, eye='>', mark='blech')],
        [], g='test', act=('taste', 'fleck'), say=["Not salt. Not sugar. Stone. Noted.", "Tastes like a cold floor. Walls are surprisingly floors."])
    o.r('prod_the_lantern', 'Prodding the lantern base with a twig to see whether it swings', 20, 'twig',
        [k(.11, 'rail_l', reach=.6, x=.3, y=-.9, b=-.4), k(.3, 'lantern', reach=1, x=.7, y=-1.3, b=-.8, mark='tk'), k(.5, 'lantern', reach=1, x=.8, y=-1.4, b=-.6, l=1, mark='tk tk'), k(.72, x=-.3, y=-.3, w=.5, eye='-', mark='fixed')],
        [], g='test', act=('prod', 'lantern'), ages=GROWN, obj=[(.3, dict(shake=.1)), (.5, dict(shake=.2))])
    # ---------------- rest
    o.r('lean_against_the_warm_wall', 'Leaning his back against the sun-warmed stone wing and sighing', 26, 'none',
        [k(.1, 'stone_r', x=-.3, y=.3, b=.3), k(.27, 'stone_r', x=-.5, y=.7, b=.8, eye='-'), k(.5, 'stone_r2', x=-.6, y=.8, b=1, eye='-', mark='ahh'), k(.74, 'stone_r2', x=-.4, y=.4, b=.5, l=1, eye='^')],
        [(.5, 'cool')], g='rest', act=('lean', 'wall'), when=['warmth>.3', 'sun'], say=["Warm stone. Slow thoughts. Excellent trade.", "The wall kept the sun for me. Kind wall."])
    o.r('sit_on_the_stone_step', 'Sitting on the step with his feet tucked, doing a very small amount of nothing', 28, 'none',
        [k(.08, 'step_b', perch=1, x=.3, y=-.3, b=-.3, w=.4), k(.22, 'step_b', perch=1, x=-.2, y=.8, b=1.4, eye='-'), k(.44, 'step_b', perch=1, x=-.3, y=1, b=1.6, l=1, eye='-', mark='...'), k(.68, 'step_a', perch=1, x=.1, y=.3, b=.9, r=1, w=.5, eye='-'), k(.88, 'step_a', perch=1, y=-.2, b=.2, eye='^')],
        [], g='rest', act=('sit', 'step'), say=["Doing nothing. Stone house approves. Stone house always approves.", "Sat. Counted pebbles. Lost count at one."])
    o.r('sulk_at_the_foundation', 'Hunching at the foot of the wall with his back to the whole house', 27, 'none',
        [k(.05, 'found_l', x=.9, y=-.3, b=-.5, w=.5), k(.19, 'found_l', x=-.4, y=.6, b=.3, eye='-', mark='hmph'), k(.34, 'base_l', x=-.9, y=1.8, b=1.7, eye='>'), k(.52, 'base_l', x=-1.1, y=1.5, b=1.3, r=1, eye='-'), k(.7, 'found_l', x=-.6, y=.9, b=.6, l=1, w=.4), k(.88, 'found_l', x=-.2, y=.2, eye='-')],
        [], g='rest', act=('sulk', 'foundation'), prefer=['grumpy', 'sad'], say=["House ignored me first. Sulk is retaliation.", "Cold stone. Colder duck. Stubbornness is insulation."])
    o.r('wait_at_the_lip', 'Waiting at the stone lip for the owners, who moved out some centuries ago', 30, 'none',
        [k(.06, 'lip_a', x=.8, y=.2, b=.2, w=.5), k(.2, 'lip_a', x=-.2, y=.8, b=1, l=1, eye='-'), k(.38, 'lip_b', x=.3, y=.1, b=-.3, eye='>', mark='...'), k(.56, 'lip_b', x=-.5, y=.6, b=.8, r=1, w=.4, eye='-'), k(.74, 'lip_a', x=.6, y=-.2, b=-.5, eye='-'), k(.92, 'lip_a', y=.4, eye='-')],
        [], g='rest', act=('wait', 'lip'), prefer=['lonely'])
    o.r('warm_toes_on_the_slab', 'Toasting one toe and then the other against the sun-baked threshold slab', 28, 'none',
        [k(.05, 'thresh_a', x=.8, y=.4, b=-.3, r=1), k(.18, 'thresh_a', x=.2, y=1.5, b=1.4, l=1, eye='-', mark='ahh'), k(.34, 'thresh_a', x=.6, y=.2, b=.1, w=.6), k(.5, 'thresh_b', x=.1, y=1.5, b=1.5, r=1, eye='^'), k(.68, 'thresh_b', x=.5, y=.6, b=.2, w=.3, l=1, eye='-'), k(.86, eye='-')],
        [(.5, 'bask')], g='rest', act=('warm', 'slab'), when=['warmth>.3', 'sun'])
    o.r('prop_the_jamb_up', 'Propping the door jamb up with his shoulder as if it needed him', 24, 'none',
        [k(.07, 'jamb_r', x=.9, y=.3, b=-.3, w=.5), k(.22, 'jamb_r', x=-.3, y=1.2, b=1.4, l=1, eye='-'), k(.4, 'jamb_r', x=-.7, y=.5, b=.5, r=1, eye='>', mark='hm'), k(.58, 'jamb_r', x=-.4, y=1.6, b=1.7, eye='-'), k(.77, 'jamb_r', x=-.1, y=.2, b=.2, w=.9, eye='-'), k(.92, eye='-')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    # ---------------- weather
    o.r('scrape_frost_off_the_step', 'Scraping the frost off the step with the edge of his bill, stroke by stroke', 18, 'none',
        [k(.1, 'step_a', x=.5, y=.9, b=.6), k(.28, 'step_a', x=1.3, y=1.3, b=1, mark='skrk'), k(.46, 'step_b', x=1.4, y=1.4, b=1.2, l=1, mark='skrk'), k(.64, 'step_b', x=1.1, y=1, b=.8, r=1), k(.82, eye='^')],
        [(.46, 'scrape')], g='weather', act=('scrape', 'step'), when=['frost>.3'], say=["Frost off the step. Duck's bill: blunt. Worth it.", "Scraped it clean. Feet are still cold. Dignity: also cold."])
    o.r('chip_ice_off_the_sill', 'Chipping a crust of ice off the left sill with the edge of his bill', 18, 'none',
        [k(.1, 'sill_l', x=.5, y=-.6, b=-.4), k(.3, 'sill_l', x=1.3, y=-.9, b=-.7, mark='tk'), k(.48, 'sill_l', x=1.4, y=-.7, b=.4, l=1, mark='tk'), k(.66, 'frame_l', x=1.1, y=-.4, b=.1, r=1), k(.84, eye='^')],
        [(.48, 'chip')], g='weather', act=('chip', 'sill'), when=['frost>.3'], ages=GROWN)
    o.r('rake_the_fallen_leaves', 'Raking the blown leaves toward the corner of the step with both feet', 22, 'none',
        [k(.05, 'thresh_b', x=.2, y=1.1, b=1.1, r=1), k(.17, 'thresh_a', x=.6, y=1.7, b=1.7, l=1, mark='sh sh'), k(.31, 'thresh_a', x=.1, y=.9, b=.5, w=.5), k(.46, 'step_a', x=.7, y=1.8, b=1.9, r=1, mark='sh sh'), k(.62, 'step_a', x=.2, y=.6, b=.3, l=1), k(.8, 'step_b', x=.4, y=1.3, b=1.2, eye='^')],
        [(.46, 'rake')], g='weather', act=('rake', 'leaves'), when=['leaves>.3'], say=["Leaves raked. Sky has plenty more. Sky is not sorry.", "Heap built. Wind plans a rematch."])
    o.r('cool_off_against_the_shade', 'Pressing his belly flat to the cool shaded stone until the sun mellows', 24, 'none',
        [k(.06, 'base_l', x=.6, y=1.3, b=1.1), k(.22, 'base_l', x=-.5, y=.5, b=1.8, w=.9, eye='-'), k(.4, 'course_l', x=-.8, y=.8, b=2, w=.4, l=1, mark='ahhh'), k(.58, 'course_l', x=-.4, y=1.2, b=1.3, w=.8, r=1), k(.78, 'base_l', x=.1, y=.3, b=.4, eye='^'), k(.92, eye='-')],
        [(.4, 'bask')], g='weather', act=('cool', 'stone'), when=['warmth>.5'])
    o.r('listen_for_the_drip', 'Standing very still and listening to the eaves drip, drip, drip', 26, 'none',
        [k(.06, 'lip_b', x=.9, y=.1, b=.3), k(.2, 'lip_b', x=-.6, y=-1.3, b=-.9, w=.5, eye='-', mark='...'), k(.38, 'lip_b', x=-.2, y=.5, b=1.5, l=1, eye='O', mark='plip'), k(.55, 'lip_b', x=-.7, y=-.9, b=-.5, w=.8, eye='-'), k(.72, 'lip_b', x=.2, y=1.2, b=.9, r=1, mark='plip'), k(.9, 'lip_b', x=-.2, y=-.2, eye='^')],
        [], g='weather', act=('listen', 'eaves'), when=['obj_wetness>.3'], say=["Plip. Plip. Plip. Drum solo, stone-house edition.", "Eaves drip. I judge their timing."])
    o.r('shelter_beside_the_door', 'Pressing flat against the right jamb with wings over his head as the rain drums', 34, 'none',
        [k(.05, 'jamb_r', x=.8, y=.3, b=.9, l=1), k(.16, 'jamb_r', x=-.4, y=1.1, b=.8, w=.6, eye='-'), k(.3, 'jamb_r', x=-.9, y=1.7, b=1.9, w=1, r=1, eye='>', mark='drip'), k(.5, 'jamb_r', x=-1, y=1.8, b=2, w=1, eye='>', mark='drip drip'), k(.68, 'jamb_r', x=-.5, y=1.2, b=1.1, w=.6, l=1), k(.86, 'jamb_r', x=-.1, y=.4, b=.3, eye='-')],
        [(.5, 'spray')], g='weather', act=('shelter', 'door'), when=['wet', 'obj_wetness<.6'])
    # ---------------- mishap
    o.r('skate_off_the_icy_step', 'Skating off the icy step and landing in a dignified heap beside the slab', 18, 'none',
        [k(.05, 'step_b', x=.7, y=.2, b=.9, l=1), k(.17, 'step_b', x=-.3, y=.8, b=-.6, r=1, w=.6, eye='O'), k(.3, 'step_a', x=1.2, y=1.1, b=-1.1, w=1, mark='WHEE'), k(.46, 'thresh_a', x=-1.2, y=1.8, b=.6, l=1, w=.8), k(.62, 'thresh_a', x=.2, y=1.9, b=1.9, eye='@', mark='*thud*'), k(.8, y=.6, b=.7, eye='-')],
        [(.46, 'scuff')], g='mishap', act=('slip', 'step'), when=['frost>.5'], say=["Ice. Stone. Duck. Order of arrival: wrong.", "Slipped like I meant it. I did not mean it."])
    o.r('walk_into_the_door_foot', 'Marching up to the door at full speed and meeting the lower boards face-first', 18, 'none',
        [k(.1, x=.3, y=.3, b=.5, l=1), k(.3, x=.9, y=.5, b=.2, r=1), k(.5, 'door_foot', x=1.8, y=.9, b=1, w=.8, eye='@', mark='BONK'), k(.7, 'jamb_l', x=-1, y=.6, b=.7, l=1, eye='O'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'boards'), say=["Door was shut. Door is always shut. Rude.", "Bill first. Brain second. Order unchanged."])
    o.r('crack_a_mortar_line', 'Hammering the same seam too hard until the old mortar cracks along the course', 18, 'none',
        [k(.06, 'course_l', x=.3, y=.4, b=-.2, w=.4), k(.2, 'course_l', x=1.9, y=1.2, b=1.2, l=1, mark='TOK'), k(.34, 'course_l', x=.7, y=.2, b=-.5), k(.5, 'course_l', x=2, y=1.6, b=1.6, r=1, mark='TOK'), k(.62, 'course_l', x=2.1, y=1.8, b=1.9, eye='@', mark='CRK'), k(.78, x=-.9, y=.5, b=-.7, w=.9, eye='O'), k(.92, eye='-')],
        [(.62, 'crack')], g='mishap', act=('peck', 'seam'), prefer=['grumpy'], say=["Seam went. House will cope. House has options.", "Too hard. Stone remembers. Stone files grievances."])
    o.r('bill_jammed_at_the_plate', 'Jamming his bill at the knob plate and wrenching it out with a pop', 28, 'none',
        [k(.05, 'kn_b', x=1.1, y=.1, b=-.4, w=.4), k(.16, 'kn_b', x=2, y=1.2, b=1.1, eye='O', mark='mm'), k(.3, 'kn_b', x=1.9, y=.9, b=.5, l=1, r=1, mark='mmf'), k(.46, 'kn_a', x=2.1, y=1.9, b=1.9, eye='@', mark='mmFF!'), k(.62, 'kn_a', x=.4, y=.2, b=-.9, w=1, mark='POP'), k(.78, x=-.6, y=.9, b=.4, eye='>'), k(.92, eye='-')],
        [], g='mishap', act=('stuck', 'plate'), prefer=['curious'], say=["Plate ate my bill. Gave it back, bent.", "Bill jammed. Dignity jammed harder."])
    o.r('stub_a_toe_on_the_lip', 'Stubbing a toe against the stone lip and hopping about in a fury', 20, 'none',
        [k(.05, 'lip_a', x=.4, y=.3, b=-.4, w=.5), k(.17, 'lip_a', x=1.9, y=1.1, b=1.7, r=1, mark='OW'), k(.3, 'lip_a', x=.2, y=-.4, b=-1.2, l=1, w=1, eye='O', mark='ow ow'), k(.46, 'lip_b', x=-.6, y=.9, b=-.4, r=1, w=.7, mark='ow'), k(.62, 'step_b', x=.7, y=-.2, b=-1, l=1, w=1, mark='ow!'), k(.8, 'step_b', x=.2, y=.5, b=.4, eye='>')],
        [], g='mishap', act=('kick', 'lip'), say=["Lip was fine. Toe was not. Lip gloated.", "Stone is hard. Noted. Ow."])
    o.r('stamp_at_the_big_door', 'Stamping both feet at the lip when the big door refuses to open', 18, 'none',
        [k(.06, 'thresh_b', x=-.5, y=1.5, b=.2, w=.5), k(.2, 'thresh_b', x=.2, y=1, b=1.5, r=1, mark='STOMP'), k(.34, 'thresh_b', x=-.8, y=.5, b=.2, l=1), k(.5, 'thresh_a', x=.4, y=1.9, b=1.6, l=1, mark='STOMP'), k(.66, 'thresh_a', x=1.3, y=-.5, b=-.8, w=1, eye='>'), k(.84, eye='-')],
        [], g='mishap', act=('stamp', 'lip'), prefer=['grumpy'])
    # ---------------- show
    o.r('pose_beside_the_lantern', 'Posing at the threshold like the lord of the manor, chin up at the lantern', 26, 'none',
        [k(.05, 'thresh_b', x=-.4, y=.4, b=.7, w=.6), k(.2, 'thresh_b', x=1.6, y=-1.3, b=-.8, w=.4, eye='^'), k(.36, 'thresh_a', x=.4, y=.9, b=1.4, w=1, l=1), k(.54, 'thresh_a', x=1.7, y=-.9, b=-.4, w=.7, eye='-', mark='ahem'), k(.72, 'thresh_b', x=-.8, y=.6, b=.9, w=1, r=1, eye='^'), k(.9, eye='-')],
        [], g='show', act=('pose', 'threshold'), prefer=['happy'], say=["Lord of the manor. Do not ask which manor.", "Posed under a lantern. Gentry lighting."])
    o.r('bow_to_the_stone', 'Bowing very low to the old stone wing as to a grandmother', 24, 'none',
        [k(.05, 'stone_l', x=.9, y=-.7, b=-.6, w=.8, l=1), k(.2, 'stone_l', x=-.3, y=.8, b=1.1, w=.3, eye='-'), k(.36, 'course_l', x=.7, y=2, b=2, w=.6, mark='madam'), k(.52, 'course_l', x=1.3, y=1.7, b=1.5, w=1, r=1), k(.7, 'stone_l', x=.5, y=-.2, b=-.2, w=.4, eye='^'), k(.9, eye='-')],
        [], g='show', act=('bow', 'wing'))
    o.r('present_the_house', 'Sweeping a wing along the whole stone front like an estate agent with a pointer', 26, 'wing',
        [k(.05, 'stone_l2', reach=.4, x=-.4, y=.8, b=1, r=1), k(.19, 'frame_l', reach=1, x=.8, y=-.6, b=-.7, mark='behold'), k(.34, 'jamb_l', reach=1, x=.2, y=.3, b=.8, l=1, mark='oak door'), k(.5, 'jamb_r', reach=1, x=1, y=-.9, b=-.9, mark='original'), k(.66, 'sill_r', reach=1, x=-.2, y=-.4, b=.3, r=1), k(.82, 'stone_r', reach=.6, x=.6, y=.7, b=1.2, eye='^'), k(.94, eye='-')],
        [], g='show', act=('present', 'house'), ages=GROWN, say=["Solid. Historic. Priced to ignore.", "Two wings, one duck. Cosy for ducks."])
    o.r('argue_with_the_door', 'Arguing with the big door, bill to oak, conceding nothing', 26, 'none',
        [k(.05, 'kn_a', x=.4, y=1.4, b=-.3, w=.6), k(.18, 'kn_a', x=1.9, y=.5, b=.9, mark='no'), k(.3, 'door_foot', x=-.2, y=.8, b=1.7, l=1, mark='YES'), k(.44, 'kn_b', x=1.5, y=1.9, b=.3, r=1, mark='no'), k(.6, 'stud_d1', x=-.8, y=-.5, b=-.6, w=1, eye='>'), k(.76, 'kn_a', x=1.8, y=.9, b=1.2, mark='!'), k(.92, eye='-')],
        [], g='show', act=('argue', 'door'), prefer=['grumpy'], say=["Door says nothing. Wins by default. Cheat.", "Last word is mine. Door has the last everything else."])
    o.r('sing_at_the_two_windows', 'Singing a duet with himself, one verse at each window', 26, 'none',
        [k(.07, 'frame_l', x=.3, y=-.5, b=.3), k(.22, 'frame_l', x=-.4, y=-1, b=-.6, w=.9, mark='laa'), k(.4, 'sill_l', x=1.5, y=-1.2, b=-.9, w=1, l=1, eye='^', mark='LAAA'), k(.6, 'sill_r', x=.3, y=.4, b=.7, r=1, eye='-', mark='...'), k(.8, 'sill_r', x=-.4, y=-1, b=-.6, w=.9, eye='^', mark='laaa'), k(.93, eye='-')],
        [], g='show', act=('sing', 'windows'), ages=GROWN, prefer=['happy'])
    o.r('dance_the_stone_steps', 'Dancing a jig from the step to the lip and over to the slab', 24, 'none',
        [k(.07, 'step_a', perch=1, y=-.5, b=-.8, l=1, w=.7), k(.22, 'lip_a', perch=1, y=.5, b=.8, r=1, w=1.2), k(.38, 'lip_b', perch=1, x=.6, y=-.6, b=-.9, l=1, w=1, mark='tada'), k(.55, 'step_b', perch=1, x=-.5, y=.6, b=.9, r=1, w=.5), k(.72, 'thresh_b', perch=1, y=-.4, b=-.6, l=1, w=.9), k(.9, eye='^')],
        [], g='show', act=('dance', 'steps'), prefer=['happy'])
    return o


def wooden_cottage():
    # Drawing (98 x 59 cells, 9.3 px a row, standing line row 55): eave beams rows 52-53 (looked at); left and right windows cols 13-33 / 69-87 (curtain strokes,
    # rail row 40 at 140 px, lower frame row 45 at 93 px, sill rows 46-47 at 84-74 px); plank walls below with studs row 53 (19 px) and ring knobs rows 49 52;
    # centre door cols 31-61 (jambs, panel rails rows 35 40 45 50, ring knobs rows 36 44 52, studs rows 42 49 53, foot strip row 51, lip row 53 at 19 px, step
    # row 54 at 9 px, threshold row 55); a planter `[======]` with a few `(*)` flowers and climbing vine strokes on each side (rows 48-55); a small round tub
    # `/__\` `|o |` `|__|` at cols 89-92 rows 51-53 (19-37 px).
    P = pm('wooden_cottage')
    o = Obj('wooden_cottage', 'placed',
            fields=dict(bloom=(0, 0, 1), leaves=(0, 0, 1), drift=(0, 0, 1), heat=(0, 0, 1)),
            physics=[('bloom', 'rate', .0006, 'sun'), ('bloom', 'rate', -.0003, '!sun'), ('leaves', 'rate', .002, 'fall'), ('leaves', 'rate', -.001, 'windy'),
                     ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'), ('heat', 'rate', .0007, 'sun'), ('heat', 'rate', -.0005, '!sun')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], wipe=[('obj.dirt', 'add', -.15)], sweep=[('obj.dirt', 'add', -.2)], dry=[('obj.wetness', 'add', -.3)],
                         spray=[('obj.wetness', 'add', .12)], hammer=[('obj.condition', 'add', .2)], dent=[('obj.condition', 'add', -.15)], kick=[('drift', 'set', 0)],
                         scoop=[('drift', 'mul', .3)], rake=[('leaves', 'mul', .3)], cool=[('heat', 'add', -.25), ('need.energy', 'add', 2)], bask=[('heat', 'add', -.2)],
                         tidy=[('need.cleanliness', 'add', 1)], laugh=[('need.fun', 'add', 2)], chat=[('need.social', 'add', 1)], scuff=[('obj.dirt', 'add', .12)]),
            anchors=dict(planter_l=P(16, 55), flower_l=P(14, 50), flower_l2=P(16, 51), flower_r=P(77, 50), flower_r2=P(79, 51), planter_r=P(80, 55), vine_l=P(26, 52),
                         vine_l2=P(33, 49), vine_r=P(70, 52), vine_r2=P(68, 49), board_l=P(19, 48), stud_l=P(21, 53), stud_l2=P(31, 53), sill_l=P(23, 47), frame_l=P(23, 45),
                         jamb_l=P(32, 50), jamb_r=P(61, 50), knob_a=P(45, 52), knob_b=P(58, 52), knob_hi=P(45, 44), stud_d1=P(45, 49), stud_d2=P(54, 49),
                         rail_low=P(50, 50), door_foot=P(51, 51), lip_a=P(43, 53, 'surface'), lip_b=P(56, 53, 'surface'), step_a=P(45, 54, 'surface'), step_b=P(56, 54, 'surface'),
                         thresh=P(50, 55, 'surface'), board_r=P(84, 48), stud_r=P(71, 53), stud_r2=P(86, 53), sill_r=P(77, 47), frame_r=P(77, 45), tub=P(91, 53), tub_lid=P(90, 51)))
    # ---------------- care
    o.r('scrub_the_left_boards', 'Scrubbing the left boards with a wing until the grime comes up in streaks', 20, 'wing',
        [k(.04, 'board_l', reach=.5, x=.4, y=.9, b=.3), k(.16, 'board_l', reach=1, x=.9, y=1.3, b=1, l=1), k(.31, 'stud_l', reach=1, x=1.1, y=1.1, b=.4, r=1, mark='skrk'), k(.47, 'board_l', reach=1, x=.7, y=1.6, b=1.2, mark='skrk'), k(.63, 'stud_l2', reach=1, x=1, y=.8, b=.7, l=1), k(.8, 'board_l', reach=.6, x=.3, y=.5, b=.2), k(.93, eye='^')],
        [(.47, 'scrub')], g='care', act=('scrub', 'boards'), when=['obj_dirt>.3'], say=["Boards scrubbed. Cottage looks smug. Cottage always has.", "Streaks gone. Wing ruined. Pride restored."])
    o.r('wipe_the_window_frame', 'Wiping the lower window frame and sill with the flat of a wing', 17, 'wing',
        [k(.06, 'sill_l', reach=.5, x=.6, y=-.5, b=-.2), k(.2, 'frame_l', reach=1, x=.2, y=-.9, b=-.7, l=1), k(.36, 'sill_l', reach=1, x=.9, y=-.2, b=.4, mark='shk'), k(.55, 'frame_l', reach=1, x=.3, y=-.8, b=-.5, r=1, mark='shk'), k(.74, 'sill_l', reach=.7, x=.5, y=.1, b=.5), k(.9, eye='-')],
        [(.55, 'wipe')], g='care', act=('wipe', 'frame'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('blot_the_planter_dry', 'Blotting the left planter rim dry with his breast, stroke by damp stroke', 22, 'none',
        [k(.05, 'planter_l', x=.5, y=1.5, b=1.5), k(.19, 'planter_l', x=.9, y=1.9, b=1.9, l=1, mark='hff'), k(.35, 'flower_l', x=.3, y=.4, b=.5, w=.5), k(.52, 'planter_l', x=1, y=2, b=1.8, r=1, mark='hff'), k(.7, 'flower_l2', x=.4, y=.5, b=.4), k(.88, eye='^')],
        [(.52, 'dry')], g='care', act=('dry', 'planter'), when=['obj_wetness>.3'], obj=[(.19, dict(shake=.2)), (.52, dict(shake=.2))])
    o.r('hammer_a_lifted_stud', 'Hammering a lifted stud head back down with a bill and a lot of faith', 17, 'none',
        [k(.05, x=.2, y=1.1, b=-.2), k(.18, 'stud_l2', x=1.5, y=1.9, b=1.3, l=1, mark='tak'), k(.31, x=-.3, y=.4, b=-.7), k(.45, 'stud_l2', x=1.6, y=2.1, b=1.5, r=1, mark='tak'), k(.58, x=.2, y=.7, b=-.4, w=.5), k(.72, 'stud_l2', x=1.7, y=2.2, b=1.7, mark='TAK'), k(.88, eye='^')],
        [(.72, 'hammer')], g='care', act=('mend', 'stud'), when=['obj_condition<.6'], say=["Stud down. Cottage secure. Duck exhausted.", "Hammered it with my face. Nobody saw. Good."])
    o.r('comb_the_right_vine', 'Combing the right vine tendrils back into line with his bill', 20, 'none',
        [k(.06, 'vine_r', x=.8, y=.5, b=.9), k(.2, 'vine_r', x=1.2, y=1.1, b=1.4, mark='frp'), k(.36, 'vine_r2', x=.9, y=.1, b=-.2, l=1), k(.52, 'vine_r2', x=1.3, y=.6, b=.3, r=1, mark='frp'), k(.7, 'vine_r', x=.6, y=1.2, b=1.2, l=1), k(.88, eye='^')],
        [(.52, 'tidy')], g='care', act=('straighten', 'vine'), prefer=['curious'], say=["Vine combed. Vine unrepentant. Vine will sprawl again.", "Neat as a duck can make a plant."])
    o.r('sweep_the_cottage_step', 'Sweeping the dust off the step and the lip with a wing and a flourish', 17, 'wing',
        [k(.05, 'lip_a', reach=.5, x=.7, y=.2, b=.6), k(.18, 'step_a', reach=1, x=.2, y=1, b=1.5, r=1, mark='fff'), k(.34, 'step_a', reach=1, x=.9, y=.4, b=.2), k(.5, 'step_b', reach=1, x=.3, y=1.1, b=1.6, l=1, mark='fff'), k(.68, 'lip_b', reach=.8, x=.8, y=.1, b=.4), k(.86, eye='-')],
        [(.5, 'sweep')], g='care', act=('sweep', 'step'), when=['obj_dirt>.5'])
    # ---------------- use
    o.r('knock_at_the_low_rail', 'Knocking at the low rail, then both lower knobs, then the high one, then a pause for the owner', 21, 'none',
        [k(.05, 'rail_low', x=1.4, y=1.2, b=1.1, mark='toc'), k(.15, 'knob_a', x=1.5, y=1.3, b=1.3, l=1, mark='toc'), k(.25, 'knob_b', x=1.5, y=1.2, b=1.2, mark='toc'), k(.42, 'knob_hi', x=-.9, y=-.2, b=-.4, w=.6, eye='O', mark='Afternoon!'), k(.62, x=.4, y=.9, b=1.4, r=1, eye='-', mark='...'), k(.82, eye='^')],
        [], g='use', act=('knock', 'rail'), prefer=['lonely'], say=["Cottage did not answer. Probably writing a will.", "Knocked three times. Politely. Nobody cares."])
    o.r('shout_up_at_the_left_window', 'Cupping a wing and shouting up at the left window for someone to look out', 19, 'wing',
        [k(.06, 'sill_l', reach=.5, x=.4, y=-.3, b=.4, l=1), k(.2, 'sill_l', reach=1, x=-.2, y=-1.2, b=-.9, mark='OI'), k(.38, 'frame_l', reach=1, x=.5, y=-1.4, b=-1.1, w=.5, eye='O', mark='OI!'), k(.56, 'frame_l', reach=.8, x=-.4, y=.6, b=.9, r=1, eye='-', mark='...'), k(.75, x=.3, y=.2, eye='>')],
        [], g='use', act=('shout', 'window'), ages=GROWN, prefer=['lonely'], say=["Window stayed shut. Curtain twitched. Possibly the wind.", "Called up. Heard crickets. In daytime. Bold."])
    o.r('sniff_the_blossoms', 'Sniffing every flower along the left planter, then sneezing at the last one', 21, 'none',
        [k(.05, 'planter_l', x=.7, y=1.4, b=1.2), k(.17, 'flower_l', x=1.1, y=.5, b=.4, l=1, mark='snf'), k(.31, 'flower_l2', x=1.3, y=.9, b=.9, r=1, mark='snf'), k(.46, 'flower_l', x=1.5, y=1.3, b=1.4, mark='snf snf'), k(.62, x=-1.2, y=-.8, b=-.9, w=1, eye='O', mark='ACHOO'), k(.8, eye='-')],
        [(.46, 'laugh')], g='use', act=('sniff', 'blossoms'), when=['bloom>.3'], prefer=['happy'], say=["Smells like a garden. Garden has opinions about my face.", "Sneezed on a daisy. It will recover. Probably."])
    o.r('shoulder_the_oak_door', 'Putting a shoulder to the oak door and testing the cottage for give', 22, 'none',
        [k(.05, 'jamb_l', x=-.6, y=.1, b=-.6, w=.4), k(.17, 'stud_d1', x=1.3, y=.5, b=1.5, l=1, mark='hnnh'), k(.3, 'stud_d1', x=1.6, y=.8, b=2, r=1, mark='HNNNH'), k(.46, 'door_foot', x=1.1, y=.3, b=.6), k(.6, x=-1.1, y=-.8, b=-.9, w=1, eye='-'), k(.78, x=-.2, y=.3, eye='^')],
        [], g='use', act=('push', 'door'), ages=GROWN, obj=[(.17, dict(sway=.1)), (.3, dict(shake=.4)), (.46, dict(sway=0))], say=["Door held. House held. Even the vines held. Ganging up.", "Shoulder gone. Pride gone. Door fine."])
    o.r('tug_a_vine_tendril', 'Tugging a vine tendril sideways to see how firmly it is attached', 18, 'none',
        [k(.06, 'vine_r2', x=.9, y=.8, b=.9), k(.2, 'vine_r2', x=1.4, y=1.2, b=1.6, l=1, mark='hup'), k(.36, 'vine_l2', x=1.6, y=.9, b=1.1, r=1, mark='RRRP'), k(.52, 'vine_l2', x=-.5, y=.2, b=-.6, w=.8, eye='O'), k(.7, x=.2, y=.5, b=.5, eye='-', mark='attached')],
        [], g='use', act=('tug', 'vine'), prefer=['curious'], obj=[(.2, dict(shake=.2)), (.36, dict(shake=.5)), (.52, dict(shake=.1))])
    o.r('squint_at_the_right_window', 'Raising himself to the right window frame and squinting at the curtain', 21, 'none',
        [k(.06, x=.3, y=-.6, b=-.9), k(.2, 'frame_r', x=1.7, y=-1, b=-1.1, eye='O'), k(.36, 'frame_r', x=1.8, y=-1.2, b=-1, l=1, eye='>', mark='hm'), k(.54, 'sill_r', x=1.5, y=-.7, b=-.7, eye='-'), k(.72, x=.2, y=.4, b=.4, eye='-')],
        [], g='use', act=('peer', 'frame'), ages=GROWN, prefer=['curious'])
    # ---------------- play
    o.r('bounce_the_stairs', 'Bouncing from step to lip and back like a very small trampoline', 19, 'none',
        [k(.05, 'step_b', perch=1, x=.5, y=-.6, b=-1, w=.9, l=1), k(.17, 'lip_b', perch=1, x=-.2, y=.6, b=1.2, r=1), k(.31, 'lip_a', perch=1, y=-.9, b=-1.3, w=1.1, mark='hup'), k(.47, 'step_a', perch=1, x=.4, y=.7, b=1.1, l=1), k(.63, 'step_a', y=-.7, b=-.9, w=1, eye='^')],
        [(.47, 'laugh')], g='play', act=('hop', 'step'), prefer=['young', 'happy'])
    o.r('zigzag_between_planters', 'Zigzagging between the two planters at top speed, bill out, bumping neither', 20, 'none',
        [k(.04, 'planter_l', x=.6, y=1.5, b=1.4), k(.16, 'flower_l2', x=1.1, y=-.3, b=-.5, l=1, w=.6, mark='zip'), k(.3, 'stud_l2', x=.4, y=1.3, b=1.1, r=1), k(.46, 'stud_r', x=1, y=-.4, b=-.6, l=1, w=.7), k(.62, 'flower_r', x=.5, y=1.2, b=1.3, r=1, mark='zip'), k(.78, 'planter_r', x=.9, y=-.2, b=-.3, w=.9, eye='^')],
        [], g='play', act=('race', 'planters'), prefer=['young'])
    o.r('vanish_into_the_vines', 'Flattening against the left vines, rustling gently, then bursting out with a roar', 22, 'none',
        [k(.05, 'vine_l', x=-.8, y=.7, b=.9, r=1), k(.2, 'vine_l', x=-1, y=1.4, b=1.6, eye='-'), k(.36, 'vine_l2', x=-1, y=1.5, b=1.7, l=1, eye='-', mark='rustle'), k(.5, 'vine_l2', x=1.7, y=-1.4, b=-1.3, w=1, eye='O', mark='RAWR'), k(.68, x=.5, y=.7, b=.6, eye='^')],
        [], g='play', act=('hide', 'vines'), prefer=['young'], say=["Ambush. Vine kept my secret. Vine kept my feathers too.", "Roared. Nothing flinched. Plants are cowards."])
    o.r('rattle_the_door_studs', 'Rattling a quick tune along the low door studs with his bill', 18, 'none',
        [k(.05, 'stud_d1', x=1.2, y=1.3, b=.7, mark='tk'), k(.17, 'stud_d2', x=.7, y=.4, b=-.5, l=1, mark='tak'), k(.31, 'stud_d1', x=1.3, y=1.4, b=.9, r=1, mark='tk tk'), k(.47, 'stud_d2', x=.6, y=.3, b=-.6, l=1, mark='TAK'), k(.64, 'stud_d1', x=1.1, y=1.1, b=.5, mark='tk'), k(.82, eye='^')],
        [(.64, 'chat')], g='play', act=('drum', 'studs'), prefer=['happy'])
    o.r('scratch_at_the_right_planter', 'Scratching soil out of the right planter with both feet until the flowers wobble', 20, 'none',
        [k(.05, 'planter_r', x=.7, y=1.3, b=.8), k(.18, 'planter_r', x=.9, y=1.7, b=1.5, l=1, mark='scr'), k(.33, 'planter_r', x=.8, y=1.9, b=1.9, r=1, mark='scr scr'), k(.5, 'flower_r2', x=.3, y=.2, b=.4, w=.5, eye='O'), k(.68, 'planter_r', x=.8, y=1.8, b=1.7, l=1), k(.86, eye='^')],
        [(.33, 'scuff')], g='play', act=('dig', 'planter'), prefer=['happy'], say=["Soil out. Flowers tilt. Landscaping is destruction with intent.", "Dug a crater. Planter reports a draught."])
    o.r('rock_the_little_tub', 'Rocking the little tub on its base with his shoulder to feel what is inside', 19, 'none',
        [k(.05, 'tub', x=-.1, y=.8, b=.4), k(.19, 'tub', x=.9, y=.9, b=1.3, l=1, mark='hnnh'), k(.34, 'tub_lid', x=1.1, y=.5, b=.9, r=1, mark='HNNH'), k(.5, 'tub', x=1.2, y=1.1, b=1.6, mark='clunk'), k(.7, x=-.8, y=-.4, b=-.5, w=.8, eye='-')],
        [], g='play', act=('rock', 'tub'), obj=[(.19, dict(sway=.3)), (.34, dict(sway=.8)), (.5, dict(sway=.4)), (.7, dict(sway=0))], say=["Tub rocked. Tub rolled its eyes. Tubs have no eyes.", "Clunk. Something inside. Or the tub itself. Concerning."])
    # ---------------- test
    o.r('tap_the_right_boards', 'Tapping the right boards from the ground up to hear which sound hollow', 20, 'none',
        [k(.05, 'stud_r', x=1.5, y=1.7, b=1.5, mark='tok'), k(.18, 'board_r', x=1.1, y=.1, b=-.2, l=1, mark='tok'), k(.34, x=-.6, y=-.7, b=-.6, w=.7, eye='-'), k(.5, 'board_r', x=1.5, y=.7, b=.4, r=1, mark='tonk'), k(.68, 'stud_r2', x=1.4, y=1.5, b=1.4, mark='tok'), k(.86, eye='^')],
        [], g='test', act=('tap', 'boards'), say=["Hollow at the top. Solid at the bottom. Like most cottages.", "Tapped the whole wall. It tapped nothing back."])
    o.r('count_the_blossoms', 'Counting the blossoms across both planters and arriving at five, then six', 24, 'none',
        [k(.04, 'flower_l', x=1, y=1.1, b=.8, mark='1'), k(.15, 'flower_l2', x=1.1, y=1.3, b=1.1, l=1, mark='2'), k(.3, 'flower_r', x=1, y=1.1, b=.7, r=1, mark='3'), k(.44, 'flower_r2', x=1.2, y=1.3, b=1.2, l=1, mark='4'), k(.58, 'planter_r', x=.8, y=1.6, b=1.6, mark='5'), k(.74, x=-.7, y=-.6, b=-.6, w=.9, eye='@', mark='six?'), k(.9, eye='-')],
        [], g='test', act=('count', 'blossoms'), prefer=['curious'])
    o.r('measure_up_to_the_sill', 'Stretching up to the left sill to see how much of him reaches the ledge', 19, 'none',
        [k(.05, 'sill_l', x=.1, y=-.8, b=-.9), k(.2, 'sill_l', x=.6, y=-1.4, b=-1.4, w=.8, mark='...'), k(.38, 'sill_l', x=1.2, y=-1.7, b=-1.7, w=1, eye='O', mark='nnng'), k(.56, 'frame_l', x=.4, y=.9, b=1.1, eye='-', mark='short'), k(.76, eye='>')],
        [], g='test', act=('measure', 'sill'), ages=GROWN, say=["Not quite. A bun on the sill would help me.", "Sill 1, duck 0. Measured. Seething."])
    o.r('compare_the_two_planters', 'Pacing from the left planter to the right and judging which has the better flowers', 24, 'none',
        [k(.05, 'planter_l', x=.6, y=1.5, b=1.4), k(.2, 'flower_l', x=.9, y=.7, b=.6, eye='>', mark='hm'), k(.46, 'flower_r', x=.9, y=.7, b=.6, l=1, mark='hmm'), k(.62, 'planter_r', x=.3, y=1.3, b=1.3, r=1), k(.78, x=-.5, y=-.5, b=-.5, w=.9, eye='-', mark='left')],
        [], g='test', act=('compare', 'planters'))
    o.r('nibble_a_vine_leaf', 'Nibbling one vine leaf, chewing it solemnly, and writing it off as lettuce at best', 20, 'none',
        [k(.05, 'vine_r', x=.6, y=.9, b=.9), k(.2, 'vine_r2', x=1.5, y=.6, b=.3, mark='nip'), k(.36, 'vine_r2', x=.3, y=-.3, b=-.5, l=1, eye='-', mark='chew'), k(.55, x=-1, y=-.5, b=-.7, w=1, eye='>', mark='bleh'), k(.75, eye='-')],
        [], g='test', act=('taste', 'leaf'), say=["Bitter. Leafy. Cottage taste profile: lawn.", "Nibbled a leaf. The vine took it personally."])
    o.r('listen_at_the_tub', 'Rapping the little tub and listening hard for what answers', 18, 'none',
        [k(.06, 'stud_r2', x=-.4, y=1.6, b=-.6, w=.6), k(.2, 'tub_lid', x=1, y=.4, b=1.8, l=1, mark='tok'), k(.38, 'tub', x=.4, y=2, b=.7, eye='-', mark='...'), k(.58, 'tub', x=-.9, y=-.4, b=-1.2, w=1, eye='O', mark='!'), k(.78, eye='^')],
        [], g='test', act=('listen', 'tub'), prefer=['curious'])
    # ---------------- rest
    o.r('lean_against_the_warm_planks', 'Leaning his back against the sun-warmed right planks and letting them hold him', 27, 'none',
        [k(.06, 'board_r', x=-.5, y=.2, b=.7, l=1), k(.2, 'board_r', x=-.8, y=.6, b=1.2, eye='-'), k(.4, 'board_r', x=-.9, y=.8, b=1.5, eye='-', mark='ahh'), k(.62, 'stud_r2', x=-.6, y=.5, b=.9, r=1, eye='^'), k(.85, 'stud_r2', x=-.2, y=.2, b=.2, eye='-')],
        [(.4, 'cool')], g='rest', act=('lean', 'planks'), when=['heat>.3', 'sun'], say=["Warm planks. Every cottage should come with them.", "Leaned. Planks held. The only reliable relationship."])
    o.r('sit_on_the_cottage_step', 'Sitting on the step with his wings folded and his thoughts elsewhere', 30, 'none',
        [k(.05, 'step_b', perch=1, x=.5, y=-.2, b=-.5, w=.5), k(.18, 'step_b', perch=1, x=-.4, y=.7, b=1.5, eye='-'), k(.4, 'step_b', perch=1, x=-.5, y=.9, b=1.7, l=1, eye='-', mark='...'), k(.62, 'step_a', perch=1, x=.2, y=.4, b=1, r=1, w=.4, eye='-'), k(.84, 'step_a', perch=1, y=-.2, b=.2, eye='^')],
        [], g='rest', act=('sit', 'step'), say=["Thoughts elsewhere. Body on a step. Excellent split.", "Sat. A bee passed. We did not speak."])
    o.r('sulk_at_the_left_vines', 'Hunching in a heap at the left vines with his back to the cottage', 27, 'none',
        [k(.04, 'vine_l', x=1, y=-.4, b=-.7, w=.6), k(.17, 'vine_l', x=-.4, y=.7, b=.5, eye='-', mark='hmph'), k(.33, 'vine_l2', x=-1, y=1.9, b=1.9, eye='>'), k(.51, 'vine_l', x=-1.2, y=1.6, b=1.5, r=1, eye='-'), k(.69, 'planter_l', x=-.7, y=1, b=.8, l=1, w=.5), k(.88, 'planter_l', x=-.2, y=.3, eye='-')],
        [], g='rest', act=('sulk', 'vines'), prefer=['grumpy', 'sad'], say=["Vines are on the house's side. I can tell.", "Sulk intensity: maximum. Audience: botanical."])
    o.r('wait_by_the_lip', 'Waiting by the door lip for the resident, who has clearly gone for flowers', 30, 'none',
        [k(.05, 'lip_b', x=.9, y=.3, b=.1, w=.5), k(.19, 'lip_b', x=-.3, y=.9, b=1.1, l=1, eye='-'), k(.36, 'lip_a', x=.2, y=.2, b=-.4, eye='>', mark='...'), k(.54, 'lip_a', x=-.6, y=.7, b=.9, r=1, w=.4, eye='-'), k(.72, 'lip_b', x=.6, y=-.1, b=-.6, eye='-'), k(.9, 'lip_b', y=.5, eye='-')],
        [], g='rest', act=('wait', 'lip'), prefer=['lonely'])
    o.r('warm_feet_on_the_step', 'Warming each foot in turn against the sunlit step', 26, 'none',
        [k(.04, 'step_a', x=.9, y=.5, b=-.2, r=1), k(.17, 'step_a', x=.3, y=1.6, b=1.5, l=1, eye='-', mark='ahh'), k(.32, 'step_a', x=.7, y=.1, b=.2, w=.7), k(.5, 'step_b', x=.2, y=1.6, b=1.6, r=1, eye='^'), k(.68, 'step_b', x=.6, y=.5, b=.1, w=.4, l=1, eye='-'), k(.86, eye='-')],
        [(.5, 'bask')], g='rest', act=('warm', 'step'), when=['heat>.3', 'sun'])
    o.r('prop_the_right_jamb', 'Propping the right jamb up with his shoulder like a bouncer who has seen things', 24, 'none',
        [k(.06, 'jamb_r', x=1, y=.4, b=-.2, w=.4), k(.2, 'jamb_r', x=-.4, y=1.3, b=1.5, l=1, eye='-'), k(.38, 'jamb_r', x=-.8, y=.6, b=.6, r=1, eye='>', mark='hm'), k(.55, 'jamb_r', x=-.5, y=1.7, b=1.8, eye='-'), k(.75, 'jamb_r', x=-.1, y=.3, b=.3, w=.8, eye='-'), k(.9, eye='-')],
        [], g='rest', act=('lean', 'jamb'), prefer=['grumpy'])
    # ---------------- weather
    o.r('kick_the_snow_off_the_lip', 'Kicking the snow drift off the lip and step in big swinging sweeps', 18, 'none',
        [k(.05, 'lip_b', x=.1, y=.9, b=.8), k(.17, 'lip_b', x=.4, y=1.3, b=1.4, l=1, mark='fff'), k(.31, 'step_b', x=.6, y=.6, b=.5), k(.46, 'step_b', x=.3, y=1.4, b=1.5, r=1, mark='FFF'), k(.62, 'step_a', x=.5, y=.7, b=.6, l=1, mark='ff'), k(.8, eye='^')],
        [(.46, 'kick')], g='weather', act=('kick', 'drift'), when=['drift>.3'], say=["Snow gone. Step bare. Feet numb. Cottage grateful. Probably.", "Kicked until the snow gave up. Toes gave up first."])
    o.r('scoop_snow_off_the_planter', 'Scooping the snow off the right planter in great wing-fulls', 19, 'wing',
        [k(.05, 'planter_r', reach=.4, x=.3, y=1.1, b=1.2), k(.19, 'planter_r', reach=1, x=.8, y=1.5, b=1.6, l=1, mark='fsh'), k(.34, 'flower_r', reach=1, x=.5, y=.5, b=.7, r=1, mark='fsh'), k(.5, 'planter_r', reach=1, x=.9, y=1.6, b=1.7, mark='fsh'), k(.7, 'flower_r2', reach=.6, x=.3, y=.4, b=.4, l=1), k(.88, eye='^')],
        [(.5, 'scoop')], g='weather', act=('scoop', 'planter'), when=['drift>.5'])
    o.r('rake_the_leaf_litter', 'Raking the blown leaves against the foot of the left vines with both feet', 21, 'none',
        [k(.05, 'thresh', x=.1, y=1.2, b=1.2, r=1), k(.17, 'step_a', x=.5, y=1.8, b=1.8, l=1, mark='sh sh'), k(.31, 'step_a', x=.1, y=.5, b=.3, w=.4), k(.45, 'vine_l', x=.8, y=1.9, b=2, r=1, mark='sh sh'), k(.6, 'vine_l', x=.3, y=.7, b=.4, l=1), k(.78, 'planter_l', x=.4, y=1.2, b=1.1, eye='^')],
        [(.45, 'rake')], g='weather', act=('rake', 'leaves'), when=['leaves>.3'], say=["Leaves in a pile. Pile in the wind. Sigh.", "Raked. Redone by wind in nine seconds. Sure."])
    o.r('cool_off_beside_the_planter', 'Flopping against the shady planter edge and fanning himself with both wings', 23, 'none',
        [k(.04, 'planter_r', x=.5, y=1.6, b=1.5), k(.18, 'planter_r', x=-.4, y=.6, b=2, w=.9, eye='o', mark='pant'), k(.34, 'flower_r', x=-.6, y=.9, b=1.4, w=.4, l=1, mark='pant'), k(.52, 'planter_r', x=-.5, y=1.4, b=1.8, w=1, r=1), k(.72, 'planter_r', x=.1, y=.3, b=.4, eye='^'), k(.9, eye='-')],
        [(.34, 'bask')], g='weather', act=('cool', 'planter'), when=['heat>.5', 'sun'], say=["Hot. Bothered. Feathered. Planter is a mercy.", "Panting at a planter. Nobody saw. Everyone did."])
    o.r('shelter_at_the_left_jamb', 'Pressing flat against the left jamb with wings over his head while the rain drums', 34, 'none',
        [k(.04, 'jamb_l', x=.9, y=.1, b=1, w=.5), k(.15, 'jamb_l', x=-.5, y=1.2, b=.7, eye='-'), k(.28, 'jamb_l', x=-1, y=1.8, b=2, w=1, l=1, eye='>', mark='drip'), k(.47, 'jamb_l', x=-1.1, y=1.9, b=2.1, w=.8, eye='>', mark='drip drip'), k(.66, 'jamb_l', x=-.6, y=1.2, b=1, w=.5, r=1), k(.84, 'jamb_l', x=-.1, y=.4, b=.3, eye='-')],
        [(.47, 'spray')], g='weather', act=('shelter', 'jamb'), when=['wet', 'obj_wetness<.6'])
    o.r('hold_the_window_shut_in_a_gust', 'Pinning the left window frame shut with a wing while the gust tries it', 24, 'wing',
        [k(.05, 'sill_l', reach=.5, x=.6, y=-.4, b=-.3), k(.18, 'frame_l', reach=1, x=-.3, y=-.8, b=1.1, mark='hnn'), k(.33, 'frame_l', reach=1, x=-.6, y=-.9, b=1.4, w=.4, l=1, mark='HNN'), k(.5, 'sill_l', reach=1, x=-.2, y=-.3, b=.6), k(.68, 'frame_l', reach=.8, x=-.5, y=-.7, b=1.3, r=1, mark='hnn'), k(.86, eye='^')],
        [], g='weather', act=('brace', 'window'), when=['windy', 'obj_condition<.8'], ages=GROWN, obj=[(.18, dict(shake=.5)), (.33, dict(shake=.8)), (.68, dict(shake=.4))])
    # ---------------- mishap
    o.r('skid_off_the_wet_step', 'Skidding off the wet step with his feet racing ahead of the rest of him', 17, 'none',
        [k(.04, 'step_b', x=.5, y=.4, b=-.5, l=1), k(.15, 'step_a', x=-.4, y=.9, b=.9, r=1, w=.8, eye='O'), k(.28, 'step_a', x=1.4, y=.2, b=-1.2, w=1, mark='WHOOP'), k(.42, 'thresh', x=-1.2, y=1.6, b=1.1, l=1, w=1), k(.58, 'thresh', x=.4, y=1.9, b=2, eye='@', mark='*splat*'), k(.78, y=.7, b=.8, eye='-')],
        [(.42, 'scuff')], g='mishap', act=('slip', 'step'), when=['obj_wetness>.5'], say=["Wet step. Dry wit. Wet duck.", "Feet had a plan. Floor had a better one."])
    o.r('walk_into_the_vine_tangle', 'Marching confidently at the right vines and coming away wearing half of them', 20, 'none',
        [k(.05, x=.4, y=.2, b=.7, l=1), k(.2, x=1, y=.4, b=.1, r=1), k(.35, 'vine_r', x=1.9, y=1, b=1.3, w=.7, eye='@', mark='BWUP'), k(.52, 'vine_r2', x=.3, y=.3, b=.6, w=1, l=1, mark='ptoo'), k(.7, 'vine_r', x=-1, y=.8, b=1.1, r=1, eye='O'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'vines'), say=["Vines won. I left with vines. Best possible loss.", "Never trust a wall that wriggles."])
    o.r('wing_tangled_in_the_vines', 'Catching a wing at the left vines and cartwheeling about until it comes free', 24, 'wing',
        [k(.05, 'vine_l', reach=.4, x=.5, y=.5, b=.4), k(.18, 'vine_l', reach=1, x=-.7, y=1, b=1.5, eye='O'), k(.34, 'vine_l2', reach=.6, x=.8, y=.4, b=-.4, l=1, r=1, mark='ack'), k(.5, 'vine_l2', reach=1, x=-1, y=1.8, b=1.9, eye='@', mark='mmf'), k(.66, 'vine_l', reach=.2, x=1.4, y=-.4, b=-1, w=1, mark='POP'), k(.84, y=.6, b=.7, eye='>')],
        [], g='mishap', act=('stuck', 'vines'), ages=GROWN, prefer=['curious'], say=["Vine took my wing hostage. Negotiated in flapping.", "Tangled. Untangled. Still tangled, spiritually."])
    o.r('crack_the_frame_with_a_peck', 'Pecking the window frame so hard the paint flakes and the board sighs', 17, 'none',
        [k(.05, 'frame_r', x=.2, y=-.4, b=-.7, w=.4), k(.18, 'frame_r', x=2, y=-.7, b=-1.6, l=1, mark='TOK'), k(.32, 'frame_r', x=.6, y=-.3, b=-.9), k(.47, 'frame_r', x=2.1, y=-.9, b=-1.8, r=1, mark='TOK'), k(.6, 'frame_r', x=2.2, y=-1, b=-2, eye='@', mark='CRK'), k(.76, x=-.8, y=.6, b=.7, w=.9, eye='O'), k(.9, eye='-')],
        [(.6, 'dent')], g='mishap', act=('peck', 'frame'), ages=GROWN, prefer=['grumpy'], say=["Paint came off. Board sulked. I regret nothing.", "Frame cracked. Window will be sensible about it."])
    o.r('stub_a_toe_on_the_tub', 'Stubbing a toe against the little tub and spinning round in a rage', 19, 'none',
        [k(.04, 'tub', x=.2, y=.2, b=-.5, r=1), k(.15, 'tub', x=1.9, y=1.2, b=1.6, l=1, mark='OW'), k(.28, 'tub_lid', x=-.5, y=-.7, b=-1.3, r=1, w=1, eye='O', mark='ow ow'), k(.44, 'tub', x=.7, y=1.5, b=-.2, l=1, w=.7, mark='ow'), k(.6, 'stud_r2', x=-1, y=.1, b=-1, r=1, w=1, mark='ow!'), k(.8, eye='>')],
        [], g='mishap', act=('kick', 'tub'), say=["Tub is fine. I am a limp with feathers.", "Toe met tub. Tub won. Toe wants a lawyer."])
    o.r('stamp_at_the_locked_door', 'Stamping at the door lip with his wings clamped when the latch ignores him', 17, 'none',
        [k(.05, 'lip_a', x=-.2, y=.8, b=.1, w=.2), k(.19, 'lip_a', x=0, y=1.1, b=1.8, r=1, mark='STOMP'), k(.33, 'lip_a', x=-.2, y=.7, b=.1), k(.48, 'lip_b', x=.1, y=1.1, b=1.9, l=1, mark='STOMP'), k(.64, 'lip_b', x=1, y=-.1, b=-.4, w=1.1, eye='>'), k(.82, eye='-')],
        [], g='mishap', act=('stamp', 'lip'), prefer=['grumpy'])
    # ---------------- show
    o.r('pose_between_the_planters', 'Posing at the threshold between both planters like a very well-off hobbit', 25, 'none',
        [k(.04, 'thresh', x=.6, y=.7, b=1.2, w=.5), k(.19, 'thresh', x=1.8, y=-1.4, b=-.9, w=.3, eye='^'), k(.35, 'thresh', x=-.3, y=.2, b=1.6, w=1, r=1), k(.52, 'thresh', x=1.9, y=-1, b=-.6, w=.6, eye='-', mark='ahem'), k(.7, 'thresh', x=-.9, y=.9, b=.8, w=1, l=1, eye='^'), k(.9, eye='-')],
        [], g='show', act=('pose', 'planters'), prefer=['happy'], say=["Landowner. Hobbit-adjacent. Do not touch the flowers.", "Flowers left, flowers right, ego centre."])
    o.r('bow_to_the_blossoms', 'Bowing slowly to the flowers on both sides as if they had applauded', 23, 'none',
        [k(.04, 'flower_l', x=.7, y=-.6, b=-.5, w=.9, l=1), k(.17, 'flower_l', x=-.2, y=.9, b=1.2, w=.3, eye='-'), k(.31, 'flower_l2', x=1, y=1.9, b=1.9, w=.8, mark='ladies'), k(.46, 'flower_r', x=-.3, y=.7, b=.9, w=.5, r=1), k(.6, 'flower_r2', x=1, y=2, b=2, w=1, mark='gentlemen'), k(.78, 'flower_r2', x=.2, y=-.3, b=-.3, w=.6, eye='^'), k(.92, eye='-')],
        [], g='show', act=('bow', 'blossoms'))
    o.r('present_the_cottage', 'Sweeping a wing along the cottage front like an agent who has never seen it', 25, 'wing',
        [k(.04, 'vine_l', reach=.4, x=-.5, y=.9, b=1.1, r=1), k(.17, 'frame_l', reach=1, x=.7, y=-.5, b=-.8, mark='behold'), k(.31, 'jamb_l', reach=1, x=.3, y=.4, b=.7, l=1, mark='oak door'), k(.47, 'jamb_r', reach=1, x=.9, y=-.8, b=-1, mark='bijou'), k(.63, 'frame_r', reach=1, x=-.1, y=-.5, b=.2, r=1, mark='sunny'), k(.8, 'board_r', reach=.6, x=.5, y=.8, b=1.2, eye='^'), k(.93, eye='-')],
        [], g='show', act=('present', 'cottage'), ages=GROWN, say=["Charming. Compact. Ducks only. Viewings by appointment.", "Original features include me. Do not scratch."])
    o.r('argue_with_the_tub', 'Arguing with the little tub, nose to rim, until it wins by going silent', 24, 'none',
        [k(.04, 'tub', x=.4, y=1.5, b=-.2, w=.6), k(.16, 'tub_lid', x=2, y=.5, b=.9, mark='no'), k(.29, 'tub', x=-.2, y=.9, b=1.7, l=1, mark='YES'), k(.43, 'tub_lid', x=1.6, y=1.9, b=.2, r=1, mark='no'), k(.58, 'tub', x=-.9, y=-.5, b=-.5, w=1, eye='>'), k(.74, 'tub', x=1.9, y=.8, b=1.3, mark='!'), k(.9, eye='-')],
        [], g='show', act=('argue', 'tub'), prefer=['grumpy'], say=["Tub refuses to engage. Classic tub.", "Won. Tub keeps rim-high. Moral victory."])
    o.r('serenade_the_left_window', 'Serenading the left window with a wing flung wide, no shame whatsoever', 26, 'none',
        [k(.04, 'frame_l', x=.4, y=-.4, b=.5), k(.19, 'sill_l', x=-.6, y=-1.2, b=-1, w=.9, mark='laa'), k(.36, 'sill_l', x=1.7, y=-1.5, b=-1.4, w=1, l=1, eye='^', mark='LAAA'), k(.54, 'frame_l', x=.2, y=.5, b=.9, r=1, eye='-', mark='...'), k(.72, 'sill_l', x=-.5, y=-1.1, b=-.9, w=.9, eye='^', mark='laaa'), k(.9, eye='-')],
        [], g='show', act=('sing', 'window'), ages=GROWN, prefer=['happy'])
    o.r('dance_a_jig_up_the_steps', 'Dancing a jig up the step and across the lip and down to the threshold', 25, 'none',
        [k(.04, 'step_a', perch=1, x=.5, y=-.7, b=-1, l=1, w=.8), k(.17, 'step_b', perch=1, y=.6, b=1.1, r=1, w=1.3), k(.3, 'lip_b', perch=1, x=-.5, y=-.7, b=-1.1, l=1, w=1, mark='tada'), k(.46, 'lip_a', perch=1, x=.6, y=.7, b=1, r=1, w=.4), k(.62, 'thresh', perch=1, x=-.2, y=-.5, b=-.7, l=1, w=1), k(.8, 'thresh', perch=1, y=.4, b=.5, eye='^'), k(.93, eye='-')],
        [], g='show', act=('dance', 'steps'), prefer=['happy'])
    return o


if __name__ == '__main__':
    barn().emit()
    shed().emit()
    greenhouse().emit()
    mud_hut().emit()
    stone_house().emit()
    wooden_cottage().emit()
