"""Wave 3a: acorn, golden_acorn, magic_acorn, pine_cone, snowball, squeaky_toy (loose objects Cheese owns, set down beside him).
Every routine is hand-written. Anchors are (column, row) of each drawing as printed by rep.py <id>, converted to fractions by P()."""
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

DIM = dict(acorn=(18, 15), golden_acorn=(18, 15), magic_acorn=(18, 15), pine_cone=(18, 21), snowball=(44, 33), squeaky_toy=(48, 35))
COUNT = {}


def pm(oid):
    w, rows = DIM[oid]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


COUNT_NEED = {}

DUETS = True  # loose-object duets run since the portable fix in wonder_company.valid; was: bool(os.environ.get('WAVE3A_DUETS'))  # the engine cannot run a duet on a loose object yet (shelters.still_placed releases the friend); see report


def duet(o, *a, **kw):
    if DUETS:
        o.r(*a, **kw)


def acorn():
    # Drawing (18 cols x 15 rows, 3.9 px a row, 59 px tall, standing on its point): stalk row 1 (col 9), flat cap top row 2 `.-----.`, hatched cap rows 3-4
    # `(#+#0#+#)` / `\#+#+#/`, a gap rows 5-6, plain shell rows 7-13 with curved sides (one `\` and a `|` and some dots inside), point `\v/` row 14, tip row 15.
    P = pm('acorn')
    o = Obj('acorn', 'portable', liftable=True,
            parts=dict(stalk='the short stalk on top', cap='the flat hatched cap', shell='the plain curved shell', tip='the pointed bottom it stands on'),
            marks=[('snow', .3, '.:*:.', 'cap_top', 'snow'), ('frost', .3, '*+*', 'cap_l', 'frost'), ('shine', .75, '`*`', 'shell_l', 'glow')],
            fields=dict(shine=(.5, 0, 1), snow=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('shine', 'rate', -.0005, 'wet'), ('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm'),
                     ('frost', 'rate', .0015, 'cold&!snow'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(wipe=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)], brush=[('snow', 'mul', .2)], buff=[('shine', 'add', .3)],
                         scrape=[('frost', 'mul', .2)], mend=[('obj.condition', 'add', .25)], dull=[('shine', 'add', -.25)], chip=[('obj.condition', 'add', -.15)],
                         grit=[('obj.dirt', 'add', .15)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], mate=[('need.social', 'add', 1)]),
            anchors=dict(stalk=P(9, 1), cap_top=P(9, 2, 'surface'), cap_l=P(6, 3), cap_r=P(15, 3), shell_l=P(4, 8), shell_r=P(15, 8), shell_mid=P(9, 8),
                         shell_belly=P(9, 10), shell_lowl=P(4, 10), shell_lowr=P(15, 10), tip=P(9, 14), tip_l=P(6, 14), tip_r=P(15, 14)))
    # ---------------- care
    o.r('wipe_cap_grime', 'Giving the hatched cap a wipe-down with the flat of a wing, grime and all', 16, 'wing',
        [k(.12, 'cap_l', reach=.5, x=.3, y=.5), k(.3, 'cap_l', reach=1, x=.7, y=.9, b=.3), k(.5, 'cap_r', reach=1, x=.8, y=1, b=.4, l=1), k(.7, 'cap_l', reach=1, x=.7, y=.9, b=.3, r=1), k(.88, eye='^')],
        [(.5, 'wipe')], g='care', act=('wipe', 'cap'), when=['obj_dirt>.3'], obj=[(.3, dict(sway=.15)), (.55, dict(sway=-.15))],
        say=["Cap clean. Nut still ignoring me.", "Scrubbed the hatching. Acorn did not thank me."])
    o.r('pat_shell_dry', 'Patting the rain off the shell with a wing until it is dry, left side then right', 16, 'wing',
        [k(.12, 'shell_l', reach=.5, x=.4, y=.4, w=.2, l=1), k(.3, 'shell_l', reach=1, x=.6, y=.8, b=.4, r=1), k(.5, 'shell_mid', reach=1, x=.5, y=1, b=.6, l=1), k(.7, 'shell_r', reach=1, x=.6, y=.8, b=.4), k(.88, eye='-')],
        [(.5, 'dry')], g='care', act=('dry', 'shell'), when=['obj_wetness>.3'], say=["Pat pat. Dry nut. Tiny win.", "Rain on a nut. A new low for weather."])
    o.r('blow_snow_off_cap', 'Blowing the snow off the flat cap with one long breath', 14, 'none',
        [k(.15, 'cap_top', x=.9, y=.9, b=.3), k(.35, 'cap_top', x=1.3, y=1.6, b=.8, mark='fff'), k(.55, 'cap_top', x=1.4, y=1.4, b=.9, mark='FFF'), k(.8, x=.2, eye='^')],
        [(.55, 'brush')], g='care', act=('blow', 'cap'), when=['snow>.3'], obj=[(.35, dict(puff=.5)), (.55, dict(shake=.3))])
    o.r('polish_shell_circles', 'Polishing the shell in slow circles until it throws the light back', 20, 'wing',
        [k(.1, 'shell_l', reach=.5, x=.3, y=.4), k(.26, 'shell_mid', reach=1, x=.6, y=.9, b=.4, l=1), k(.42, 'shell_r', reach=1, x=.6, y=.9, b=.5), k(.58, 'shell_belly', reach=1, x=.6, y=1, b=.5, r=1), k(.74, 'shell_lowl', reach=1, x=.5, y=.9, b=.4), k(.9, eye='^')],
        [(.58, 'buff')], g='care', act=('polish', 'shell'), when=['shine<.65'], obj=[(.4, dict(glow=.3)), (.6, dict(glow=.7)), (.8, dict(glow=.2))],
        say=["Buffed it to a shine. It is a nut.", "Shiny. Smug. The acorn and also me."])
    o.r('chip_frost_off_hatching', 'Chipping the frost out of the cap hatching with the tip of a twig', 18, 'twig',
        [k(.12, 'cap_l', reach=.5, x=.5, y=.5), k(.3, 'cap_top', reach=1, x=.9, y=.7, b=.3, mark='tik'), k(.5, 'cap_r', reach=1, x=1, y=.9, b=.4, mark='tik'), k(.7, 'cap_l', reach=1, x=.9, y=.8, b=.3, mark='tik'), k(.88, eye='-')],
        [(.5, 'scrape')], g='care', act=('chip', 'hatching'), when=['frost>.3'])
    o.r('straighten_the_stalk', 'Nipping the bent stalk straight again with his bill', 16, 'none',
        [k(.12, 'stalk', x=.7, y=.7, b=.2), k(.32, 'stalk', x=1.2, y=1.2, b=.6, mark='nnk'), k(.52, 'stalk', x=1.3, y=1, b=.7, l=1), k(.72, 'stalk', x=1, y=.8, b=.4), k(.88, x=.1, eye='^')],
        [(.52, 'mend')], g='care', act=('straighten', 'stalk'), when=['obj_condition<.7'], obj=[(.32, dict(shake=.3))], say=["Straight. Slightly less sad.", "Stalk fixed. Do not tell it I care."])
    o.r('sweep_grit_from_the_point', 'Sweeping the grit off the point in short wing strokes', 14, 'wing',
        [k(.12, 'tip_l', reach=.5, x=.4, y=.9, b=.6), k(.32, 'tip', reach=1, x=.7, y=1.1, b=.9, l=1), k(.52, 'tip_r', reach=1, x=.7, y=1.1, b=.9, r=1), k(.72, 'tip', reach=1, x=.6, y=1, b=.7), k(.88, eye='-')],
        [(.52, 'wipe')], g='care', act=('sweep', 'point'), when=['obj_dirt>.45'])
    # ---------------- use (carry, drag, roll, hide, spin, rock)
    o.r('carry_by_the_stalk', 'Gripping the stalk and carrying the acorn a few steps, setting it down, and fetching it home', 24, 'none',
        [k(.08, 'stalk', x=.8, y=.7, b=.2), k(.2, 'stalk', x=1.3, y=1.2, b=.6, mark='hup'), k(.36, 'stalk', x=.4, y=-.3, b=-.3, l=1), k(.5, 'stalk', x=.3, y=-.2, r=1),
         k(.62, 'stalk', x=1.1, y=1, b=.7), k(.74, 'stalk', x=1.3, y=1.1, b=.6), k(.88, x=.1, eye='^')],
        [], g='use', act=('carry', 'stalk'), prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1)), (.58, dict(hold=0, ix=3)), (.66, dict(hold=0, ix=3)), (.74, dict(hold=1, ix=3)), (.82, dict(hold=1)), (.9, dict(hold=0))],
        say=["Relocated an acorn. Management material.", "Carried it. Set it down. Carried it back. Peak productivity."])
    o.r('drag_by_the_cap_lip', 'Dragging the acorn along the ground by its cap lip, then back again', 22, 'none',
        [k(.1, 'cap_l', x=.9, y=1, b=.5), k(.24, 'cap_l', x=1.4, y=1.2, b=.9, l=1, mark='hnn'), k(.42, 'cap_l', x=-.3, y=1.1, b=1, r=1), k(.6, 'cap_r', x=-.5, y=1.2, b=1, l=1, mark='hnn'),
         k(.78, 'cap_r', x=.4, y=1, b=.7, r=1), k(.9, eye='-')],
        [(.42, 'grit')], g='use', act=('drag', 'cap'), prefer=['grown'],
        obj=[(.24, dict(ix=0)), (.42, dict(ix=-3)), (.5, dict(ix=-3, shake=.2)), (.68, dict(ix=-1)), (.78, dict(ix=0))])
    o.r('roll_it_along', 'Rolling the acorn off along the ground with his bill, then carting it back by the stalk', 26, 'none',
        [k(.1, 'shell_l', x=.9, y=.9, b=.4), k(.24, 'shell_l', x=1.4, y=1, b=.8, l=1, mark='rrr'), k(.4, x=1.5, y=.4, b=.3, r=1), k(.56, 'stalk', x=1.2, y=1, b=.7),
         k(.72, 'stalk', x=.3, y=-.2, b=-.2, l=1), k(.88, eye='^')],
        [(.24, 'grit')], g='use', act=('roll', 'shell'),
        obj=[(.24, dict(ix=0)), (.32, dict(ix=4, shake=.3)), (.5, dict(ix=6)), (.56, dict(ix=6, hold=0)), (.62, dict(ix=6, hold=1)), (.76, dict(ix=0, hold=1)), (.84, dict(hold=0))],
        say=["Rolled it off. Retrieved it. Rolled it off again in my head.", "Acorns roll. I roll my eyes."])
    o.r('stash_it_out_of_sight', 'Tucking the acorn out of sight to hide it with scrapes of his foot, then digging it out again', 28, 'none',
        [k(.08, 'stalk', x=1, y=1, b=.5), k(.22, 'stalk', x=1.2, y=1, b=.6, l=1), k(.36, 'tip_l', x=1.1, y=1.4, b=1, l=1, mark='skrt'), k(.5, 'tip_l', x=.9, y=1.4, b=1, r=1, mark='skrt'),
         k(.62, 'tip_r', x=.8, y=1.2, b=.8, l=1, mark='psst'), k(.76, 'tip_r', x=1.2, y=1.5, b=1.1, r=1, mark='skrt'), k(.9, eye='^')],
        [(.62, 'grit')], g='use', act=('hide', 'shell'), prefer=['curious'],
        obj=[(.22, dict(hold=0)), (.3, dict(hold=1)), (.4, dict(hold=1, hide=1)), (.46, dict(hold=0, hide=1)), (.62, dict(hide=1)), (.7, dict(hide=1)), (.78, dict(hide=0)), (.84, dict(hide=0))],
        say=["Hidden. Acorn secured. Where? Classified.", "Buried nothing. Merely stored it dirtily."])
    o.r('rock_it_by_the_cap', 'Leaning on the cap with the bill to rock the acorn on its point', 18, 'none',
        [k(.12, 'cap_l', x=.8, y=.8, b=.3), k(.3, 'cap_l', x=1.5, y=1.1, b=.9, mark='hnn'), k(.48, 'cap_r', x=1.1, y=.6, b=.4, r=1), k(.66, 'cap_r', x=1.6, y=1.2, b=1, l=1), k(.84, x=.2, eye='-')],
        [], g='use', act=('rock', 'cap'), obj=[(.3, dict(sway=.5)), (.48, dict(sway=-.6)), (.66, dict(sway=.9)), (.8, dict(sway=0))])
    o.r('weigh_it_in_the_bill', 'Hoisting the acorn by the stalk and bobbing it twice to guess its weight', 18, 'none',
        [k(.1, 'stalk', x=.8, y=.7, b=.2), k(.24, 'stalk', x=1.3, y=1.3, b=.6), k(.4, 'stalk', x=.3, y=-.5, b=-.5, mark='hup'), k(.54, 'stalk', x=.9, y=.8, b=.5), k(.66, 'stalk', x=.2, y=-.6, b=-.6, mark='hup'), k(.8, 'stalk', x=1.1, y=1, b=.5), k(.92, eye='-')],
        [], g='test', act=('weigh', 'acorn'), obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.52, dict(hold=1, iy=1)), (.64, dict(hold=1)), (.8, dict(hold=0))])
    # ---------------- play
    o.r('fling_it_by_the_stalk', 'Swinging the acorn by the stalk and throwing it off, then fetching it back in his bill', 26, 'none',
        [k(.08, 'stalk', x=.8, y=.9, b=.5), k(.2, 'stalk', x=1.3, y=1.2, b=.9, l=1), k(.34, 'stalk', x=-.6, y=-.4, b=-.6, w=.8, mark='HUP'), k(.46, x=1.6, y=-.2, b=-.2, r=1, w=1, eye='>'),
         k(.62, x=1.4, y=.5, b=.3, l=1, r=1), k(.74, 'stalk', x=1.2, y=1, b=.7), k(.88, eye='^')],
        [(.2, 'dull')], g='play', act=('throw', 'stalk'), prefer=['happy', 'young'],
        obj=[(.2, dict(hold=0)), (.3, dict(hold=1)), (.38, dict(hold=1)), (.44, dict(hold=.3, ix=3, iy=-3)), (.5, dict(hold=0, ix=6, iy=0)), (.64, dict(hold=0, ix=6)), (.72, dict(hold=1, ix=6)), (.8, dict(hold=1, ix=0)), (.88, dict(hold=0))],
        say=["Threw it. Went and got it. A complete career.", "Distance: respectable. Dignity: lost in the grass."])
    o.r('boot_it_off_the_belly', 'Kicking the acorn off the belly with one foot and trotting after it', 20, 'none',
        [k(.1, 'shell_belly', x=.3, y=.9, b=.6, l=1), k(.24, 'shell_belly', x=-.6, y=.4, b=1, l=1, mark='pok'), k(.38, x=1.2, y=.2, b=-.3, r=1, w=.5), k(.52, 'stalk', x=1.3, y=1, b=.7), k(.7, 'stalk', x=.3, y=-.2, b=-.2, l=1), k(.86, eye='^')],
        [(.24, 'dull')], g='play', act=('kick', 'belly'), prefer=['grumpy'],
        obj=[(.24, dict(ix=0)), (.32, dict(ix=3, shake=.4)), (.46, dict(ix=5)), (.52, dict(ix=5, hold=1)), (.64, dict(ix=0, hold=1)), (.74, dict(hold=0))])
    o.r('hop_over_it_and_back', 'Hopping over the acorn and back, three times, getting slightly braver', 18, 'none',
        [k(.1, 'tip', x=.6, y=.5, b=.5), k(.22, x=.2, y=-.6, b=-1.2, l=1, r=1, w=.6), k(.34, 'tip_r', x=.2, y=.6, b=.8), k(.46, x=.2, y=-.8, b=-1.4, l=1, r=1, w=.8), k(.58, 'tip_l', x=.2, y=.6, b=.8),
         k(.7, x=.3, y=-1, b=-1.6, l=1, r=1, w=1, eye='^'), k(.84, 'tip', x=.4, y=.5, b=.4)],
        [(.34, 'fun')], g='play', act=('hop', 'shell'), prefer=['happy', 'young'])
    o.r('dribble_it_round', 'Chasing the acorn round in short bill nudges, then toting it back by the cap lip', 24, 'none',
        [k(.08, 'shell_l', x=.8, y=.9, b=.4), k(.18, 'shell_l', x=1.2, y=1, b=.7, mark='tk'), k(.3, 'shell_l', x=1.2, y=1, b=.7, l=1, mark='tk'), k(.42, 'shell_l', x=1.3, y=1, b=.8, r=1, mark='tk'),
         k(.58, 'cap_l', x=1.1, y=1.1, b=.7), k(.74, 'cap_l', x=.3, y=-.1, b=-.3, l=1), k(.88, eye='^')],
        [], g='play', act=('chase', 'shell'), prefer=['curious'],
        obj=[(.18, dict(ix=0)), (.24, dict(ix=1)), (.34, dict(ix=2)), (.46, dict(ix=3)), (.58, dict(ix=3, hold=0)), (.66, dict(ix=3, hold=1)), (.8, dict(ix=0, hold=1)), (.88, dict(hold=0))])
    o.r('flip_it_up_and_catch', 'Tossing the acorn up off the stalk and catching it out of the air', 20, 'none',
        [k(.1, 'cap_l', x=.8, y=.9, b=.4), k(.24, 'cap_l', x=1.3, y=1.3, b=.8, l=1), k(.38, x=.8, y=-1.2, b=-.8, w=.6, eye='O'), k(.5, x=1.1, y=-1.4, b=-.6, w=.4), k(.64, 'stalk', x=1.4, y=.8, b=.6, mark='hap'), k(.82, eye='^')],
        [], g='play', act=('catch', 'acorn'), prefer=['happy'],
        obj=[(.24, dict(hold=1)), (.34, dict(hold=1)), (.42, dict(hold=0, iy=-6)), (.52, dict(hold=0, iy=-6)), (.6, dict(hold=1, iy=0)), (.76, dict(hold=0)) ])
    o.r('balance_on_the_cap', 'Climbing onto the flat cap and balancing there on one foot, wings out', 22, 'none',
        [k(.08, 'cap_top', x=.5, y=.5, b=.4), k(.2, 'cap_top', perch=1, x=-.2, y=-.4, b=-.6, w=.6), k(.34, 'cap_top', perch=1, x=-.4, y=-.6, b=-.8, l=1, w=1), k(.5, 'cap_top', perch=1, x=.5, y=-.2, b=-.3, r=1, w=1),
         k(.66, 'cap_top', perch=1, x=-.5, y=-.7, b=-.7, l=1, w=.8, eye='>'), k(.82, 'cap_top', x=.4, y=.6, b=.4)],
        [], g='show', act=('balance', 'cap'), ages=GROWN, obj=[(.2, dict(sway=.2)), (.34, dict(sway=-.5)), (.5, dict(sway=.7)), (.66, dict(sway=-.4)), (.82, dict(sway=0))],
        say=["Standing on an acorn. Peak athleticism.", "Four seconds. It rolled my ego off."])
    # ---------------- test
    o.r('rap_the_cap', 'Tapping the hatched cap with the bill, three taps, and cocking his head', 14, 'none',
        [k(.14, 'cap_top', x=.9, y=.8, b=.3), k(.28, 'cap_l', x=1.2, y=1.5, b=.7, mark='tok'), k(.42, 'cap_r', x=1.2, y=1.5, b=.7, mark='tok'), k(.56, 'cap_top', x=1.3, y=1.6, b=.8, mark='tok'), k(.76, x=-.2, y=.4, eye='O')],
        [], g='test', act=('tap', 'cap'), obj=[(.28, dict(shake=.2)), (.42, dict(shake=.2)), (.56, dict(shake=.3))])
    o.r('ear_to_the_shell', 'Listening with his head pressed to the shell to hear what is in there', 18, 'none',
        [k(.12, 'shell_l', x=.8, y=.4, b=.3), k(.3, 'shell_l', x=1.3, y=.5, b=.5, eye='-'), k(.52, 'shell_l', x=1.3, y=.6, b=.5, eye='-', mark='...'), k(.7, x=-.3, y=-.3, eye='O'), k(.86, eye='-')],
        [], g='test', act=('listen', 'shell'), say=["Nothing in there. Which is what I expected.", "It sounds like an acorn. Does not help."])
    o.r('peck_the_stalk', 'Pecking the stalk to see if it comes off', 12, 'none',
        [k(.14, 'stalk', x=.8, y=.9, b=.3), k(.28, 'stalk', x=1.4, y=1.3, b=.7, mark='pk'), k(.42, 'stalk', x=1.4, y=1.3, b=.7, mark='pk'), k(.58, 'stalk', x=1.5, y=1.2, b=.8, mark='PK'), k(.8, x=.1, eye='-')],
        [], g='test', act=('peck', 'stalk'), obj=[(.3, dict(shake=.2)), (.58, dict(shake=.4))])
    o.r('mouth_the_cap_rim', 'Mouthing the cap rim for a taste, and spitting', 14, 'none',
        [k(.14, 'cap_l', x=.9, y=.8, b=.3), k(.3, 'cap_l', x=1.2, y=1, b=.5, eye='-'), k(.46, 'cap_l', x=1.2, y=1, b=.5, eye='>', mark='bleh'), k(.62, x=-.6, y=.3, w=.5, eye='>', mark='ptui'), k(.8, eye='-')],
        [], g='test', act=('taste', 'cap'))
    o.r('measure_it_by_the_bill', 'Measuring the acorn with his bill, laid along it from the point up to the stalk', 18, 'none',
        [k(.1, 'tip', x=.5, y=1, b=.8), k(.28, 'shell_belly', x=.7, y=.8, b=.6), k(.46, 'shell_mid', x=.8, y=.6, b=.4), k(.64, 'cap_l', x=.9, y=.4, b=.3), k(.8, 'stalk', x=1, y=.3, b=.2, eye='^')],
        [], g='test', act=('measure', 'shell'), say=["Fifty-nine pixels. Bill: longer. Obviously.", "Measured it. Acorn is acorn-sized."])
    # ---------------- rest
    o.r('lean_on_the_shell', 'Leaning his shoulder on the shell, letting the acorn take a little weight', 22, 'none',
        [k(.12, 'shell_l', x=.7, y=.3, b=.3), k(.3, 'shell_l', x=.9, y=.4, b=.7, w=.2), k(.55, 'shell_l', x=1, y=.5, b=.9, eye='-'), k(.8, 'shell_l', x=.8, y=.4, b=.6, eye='-')],
        [(.55, 'rest')], g='rest', act=('lean', 'shell'), prefer=['tired'], obj=[(.3, dict(sway=.2)), (.55, dict(sway=.3))])
    o.r('curl_up_by_the_point', 'Curling up at the point of the acorn for a nap, bill tucked in', 30, 'none',
        [k(.14, 'shell_lowl', x=.4, y=.8, b=.8), k(.32, 'tip', x=.6, y=1.5, b=1.5, eye='-'), k(.55, 'tip', x=.7, y=1.8, b=1.8, eye='-', mark='zzz'), k(.8, 'shell_lowl', x=.5, y=1.6, b=1.6, eye='-', mark='zz')],
        [(.55, 'rest')], g='rest', act=('nap', 'point'), prefer=['tired'], when=['tired'])
    o.r('sulk_with_his_back_turned', 'Sulking with his tail to the acorn and one wing over his bill', 24, 'none',
        [k(.14, 'shell_mid', x=-.8, y=.6, b=.6), k(.32, 'shell_mid', x=-1.2, y=1, b=1, w=.4, eye='-'), k(.58, 'shell_mid', x=-1.2, y=1.1, b=1.1, eye='-', mark='hmph'), k(.82, 'shell_mid', x=-.8, y=.6, b=.6, eye='>')],
        [], g='rest', act=('sulk', 'shell'), prefer=['sad', 'grumpy'])
    o.r('guard_it_from_the_gap', 'Standing guard at the acorn with chest out, eyes sweeping the yard', 26, 'none',
        [k(.12, 'shell_belly', x=.2, y=-.3, b=-.2, w=.3), k(.3, 'shell_belly', x=-.3, y=-.5, b=-.4, w=.5, eye='>'), k(.5, 'shell_belly', x=.4, y=-.4, b=-.3, w=.5, eye='<'), k(.7, 'shell_belly', x=-.3, y=-.6, b=-.4, w=.6, eye='>'), k(.88, eye='^')],
        [], g='rest', act=('guard', 'shell'), prefer=['curious'], say=["Mine. Look at it and I will hold it against you.", "No squirrels. I have a chest and I am using it."])
    o.r('soak_up_the_sun_on_the_shell', 'Pressing his breast to the sun-warmed shell and soaking in the heat', 22, 'none',
        [k(.14, 'shell_r', x=.7, y=.4, b=.5), k(.34, 'shell_r', x=.9, y=.6, b=1, w=.3, eye='-'), k(.58, 'shell_belly', x=.9, y=.7, b=1.1, eye='-', mark='mmm'), k(.82, 'shell_belly', x=.7, y=.4, b=.6, eye='^')],
        [], g='weather', act=('warm', 'shell'), when=['sun', 'day'])
    # ---------------- weather
    o.r('shake_snow_from_the_cap', 'Shaking the acorn by the cap lip until the snow drops off', 18, 'none',
        [k(.1, 'cap_l', x=.8, y=.9, b=.4), k(.25, 'cap_l', x=1.4, y=1.2, b=.8, l=1, mark='hrr'), k(.4, 'cap_r', x=-.3, y=.9, b=.9, r=1, mark='hrr'), k(.55, 'cap_l', x=1.2, y=1, b=.7, l=1, mark='hrr'), k(.8, x=.1, eye='^')],
        [(.4, 'brush')], g='weather', act=('shake', 'cap'), when=['snow>.4'], obj=[(.25, dict(shake=.5)), (.4, dict(shake=1, puff=.4)), (.55, dict(shake=.6)), (.7, dict(shake=0))])
    o.r('catch_it_in_the_gust', 'Catching the acorn as the gust rolls it off, and carrying it home by the stalk', 22, 'none',
        [k(.1, 'shell_r', x=.5, y=.3, b=.2, w=.4), k(.26, x=1.6, y=.2, b=-.3, l=1, r=1, w=.8, eye='O'), k(.44, x=1.4, y=.8, b=.5), k(.58, 'stalk', x=1.3, y=1, b=.7, mark='gotcha'), k(.74, 'stalk', x=.3, y=-.2, b=-.2, l=1), k(.88, eye='^')],
        [], g='weather', act=('catch', 'shell'), when=['windy'],
        obj=[(.2, dict(ix=0)), (.28, dict(ix=3, shake=.4)), (.42, dict(ix=7)), (.5, dict(ix=7)), (.6, dict(ix=7, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0))])
    o.r('brace_against_the_gust', 'Bracing his feet wide beside the point and hanging on to the stalk while the gust tries for the acorn', 24, 'none',
        [k(.1, 'stalk', x=.8, y=.9, b=.5), k(.26, 'shell_r', x=1.2, y=1.1, b=1, l=1, mark='hff'), k(.5, 'shell_r', x=1.4, y=1.2, b=1.2, r=1, eye='>'), k(.72, 'stalk', x=1.1, y=1, b=.9), k(.88, eye='^')],
        [], g='weather', act=('brace', 'stalk'), when=['windy'], obj=[(.26, dict(sway=.5)), (.5, dict(sway=-.7, shake=.4)), (.72, dict(sway=.2))])
    # ---------------- show
    o.r('bow_to_the_acorn', 'Bowing low to the acorn as if it were royalty', 16, 'none',
        [k(.15, 'cap_top', x=.3, y=-.3, b=-.3, w=.4), k(.35, 'cap_top', x=1.3, y=1.8, b=1.9, w=.8, mark='sire'), k(.6, 'cap_top', x=1.4, y=1.9, b=2, eye='-'), k(.8, x=.1, y=-.4, b=-.3, eye='^')],
        [], g='show', act=('bow', 'acorn'), say=["Your Majesty. Please stop being a nut.", "Bowed. It did not bow back. Typical monarch."])
    o.r('dance_a_ring_round_it', 'Dancing a quick ring around the acorn and ending in a bow', 20, 'none',
        [k(.1, 'shell_l', x=.2, y=-.4, b=-.6, l=1, w=.6), k(.25, 'shell_lowl', x=.4, y=.4, b=.6, r=1, w=1), k(.4, 'tip_l', x=-.2, y=-.6, b=-1, l=1, w=.9), k(.55, 'shell_lowr', x=.6, y=.5, b=.8, r=1, w=1), k(.7, 'shell_r', x=.3, y=-.7, b=-1, l=1, w=.8), k(.86, x=.3, y=1.2, b=1.2, eye='^')],
        [], g='show', act=('dance', 'acorn'), prefer=['happy'])
    # ---------------- mishap
    o.r('slip_on_the_point', 'Slipping off the point after planting a foot on it, and landing flat', 16, 'none',
        [k(.1, 'tip', x=.5, y=.6, b=.3, l=1), k(.26, 'tip', x=1, y=.8, b=.6, l=1, mark='eh'), k(.42, 'tip_r', x=1.6, y=1.6, b=2, l=1, r=1, w=1, eye='O', mark='WHA'), k(.6, x=1.7, y=2, b=2.2, eye='@'), k(.8, x=.4, y=.8, b=.6, eye='-')],
        [(.26, 'chip')], g='mishap', act=('slip', 'point'), prefer=['grumpy'], obj=[(.26, dict(shake=.5)), (.42, dict(sway=.6))], say=["Meant to do that. Face did not.", "Floor and I are on bad terms now."])
    o.r('jam_his_bill_in_the_cap', 'Getting his bill stuck in the cap hatching, tugging, and coming out with a pop', 20, 'none',
        [k(.12, 'cap_r', x=1, y=.8, b=.3), k(.28, 'cap_r', x=1.5, y=1, b=.9, mark='oof'), k(.46, 'cap_r', x=1.6, y=1, b=1.2, l=1, r=1, eye='O', mark='mph'), k(.64, 'cap_r', x=1.7, y=1, b=1.4, l=1, w=1, mark='POP'), k(.8, x=-1.4, y=.3, b=.2, eye='@')],
        [(.46, 'chip')], g='mishap', act=('stuck', 'cap'), prefer=['curious'], obj=[(.28, dict(sway=.4)), (.46, dict(shake=.6)), (.64, dict(sway=-.6))])
    # ---------------- more things a duck can do with an acorn
    o.r('hug_it_wing_round', 'Wrapping both wings round the acorn and pressing his cheek to the cap', 20, 'none',
        [k(.12, 'shell_mid', x=.5, y=.3, b=.4, w=.6), k(.3, 'cap_l', x=1, y=.2, b=.8, w=1.2, eye='-'), k(.52, 'cap_l', x=1.1, y=.2, b=1, w=1.4, eye='-', mark='mwa'), k(.74, 'shell_mid', x=.6, y=.3, b=.5, w=.6), k(.88, eye='^')],
        [(.52, 'mate')], g='rest', act=('wrap', 'shell'), prefer=['lonely', 'sad'], obj=[(.3, dict(sway=.2)), (.52, dict(sway=.3, glow=.2))], say=["Hugged a nut. Tell no one.", "It is warm and does not talk. Ideal."])
    o.r('drum_down_the_shell', 'Drumming a beat down the shell with both feet in turn', 18, 'none',
        [k(.1, 'shell_l', x=.2, y=.5, b=.4, l=1), k(.24, 'shell_lowl', x=.2, y=.7, b=.6, r=1, mark='dum'), k(.38, 'shell_l', x=.3, y=.5, b=.5, l=1, mark='dum'), k(.52, 'shell_lowl', x=.2, y=.7, b=.7, r=1, mark='dum'), k(.68, 'tip_l', x=.3, y=.8, b=.8, l=1, mark='DUM'), k(.86, eye='^')],
        [], g='play', act=('drum', 'shell'), prefer=['happy'], obj=[(.24, dict(shake=.2)), (.52, dict(shake=.3)), (.68, dict(shake=.5))])
    o.r('hook_the_stalk_closer', 'Hooking the stalk with a twig and reeling the acorn in from a few steps off', 22, 'twig',
        [k(.1, 'stalk', reach=.5, x=.6, y=.4, b=.2), k(.28, 'stalk', reach=1, x=1.4, y=.8, b=.6, mark='klk'), k(.46, 'stalk', reach=1, x=.2, y=.5, b=.9, l=1, mark='hnn'), k(.64, 'stalk', reach=1, x=.1, y=.4, b=1, r=1), k(.84, eye='^')],
        [], g='use', act=('hook', 'stalk'), obj=[(.1, dict(ix=3)), (.28, dict(ix=3)), (.46, dict(ix=2, shake=.2)), (.64, dict(ix=0))],
        say=["Fishing for an acorn. I have peaked.", "Hooked it. Landed it. Let it go. Catch and release."])
    o.r('prod_the_cap_with_a_twig', 'Prodding the cap with a twig from arm-and-twig distance to see if it bites', 14, 'twig',
        [k(.12, 'cap_top', reach=.5, x=-.2, y=-.2, b=-.2), k(.3, 'cap_top', reach=1, x=.6, y=-.4, b=-.3, mark='poke'), k(.5, 'cap_r', reach=1, x=.4, y=-.3, b=-.5, eye='O'), k(.7, x=-.5, y=.2, b=.2, eye='-')],
        [], g='test', act=('prod', 'cap'), obj=[(.3, dict(sway=.3)), (.5, dict(sway=-.3))])
    o.r('count_the_hatch_marks', 'Counting the cap hatching mark by mark with the bill, and losing count', 20, 'none',
        [k(.1, 'cap_l', x=.5, y=.7, b=.2), k(.24, 'cap_l', x=1, y=1.4, b=.6, mark='one'), k(.38, 'cap_top', x=1.3, y=1.6, b=.9, l=1, mark='two'), k(.52, 'cap_r', x=1.4, y=1.5, b=.9, r=1, mark='three'), k(.66, 'cap_l', x=1, y=1.4, b=.6, mark='...four?'), k(.82, x=-.4, y=-.2, eye='@')],
        [], g='test', act=('count', 'hatching'), say=["Eleven. Or six. Started again.", "Counted the cap. Lost. Acorn won."])
    o.r('peer_at_my_face_in_the_shine', 'Showing the polished shell his best faces, bill to the shine', 16, 'none',
        [k(.12, 'shell_mid', x=.7, y=.3, b=.2), k(.28, 'shell_mid', x=1.4, y=.4, b=.4, eye='O'), k(.44, 'shell_mid', x=1.4, y=.4, b=.4, eye='>', mark='bleh'), k(.6, 'shell_mid', x=.8, y=.5, b=.3, eye='^'), k(.8, eye='-')],
        [], g='show', act=('show', 'shell'), when=['shine>.65'], obj=[(.28, dict(glow=.4)), (.6, dict(glow=.1))], say=["Handsome duck. Shame about the nut.", "The shell looks back. Fair."])
    o.r('serenade_the_acorn', 'Singing to the acorn with a long wing flung out, then asking for a review', 24, 'none',
        [k(.1, 'cap_l', x=.3, y=-.4, b=-.4, w=.5), k(.26, 'cap_l', x=-.6, y=-1.3, b=-1, w=1, eye='^', mark='laa'), k(.46, 'shell_l', x=1.4, y=-1.5, b=-1.4, w=1.1, mark='LAAA'), k(.66, 'shell_l', x=.6, y=.9, b=.9, eye='O'), k(.82, eye='-')],
        [], g='show', act=('sing', 'acorn'), prefer=['happy'])
    # ---------------- duets with a visiting friend
    duet(o, 'pass_it_to_a_friend', 'Rolling the acorn across to a friend who bats it back to his bill', 26, 'none',
        [k(.1, 'shell_l', x=.8, y=.9, b=.4), k(.22, 'shell_l', x=1.4, y=1, b=.8, l=1, mark='rrr'), k(.4, x=.5, y=.2, b=-.2, w=.6, eye='O'), k(.58, 'shell_belly', x=1, y=.8, b=.5, mark='gotcha'), k(.78, 'shell_belly', x=.3, y=.2, b=.1, eye='^')],
        [(.22, 'mate')], g='play', act=('roll', 'acorn'), prefer=['lonely'],
        obj=[(.22, dict(ix=0)), (.32, dict(ix=4)), (.46, dict(ix=4, shake=.2)), (.54, dict(ix=4)), (.62, dict(ix=0))],
        duo=[k(.2, x=-.3, y=.2, eye='O'), k(.4, 'cap_r', x=1.2, y=.8, b=.6, mark='hup'), k(.55, 'cap_r', x=1.5, y=1, b=.9, l=1, mark='tk'), k(.75, x=.3, y=.2, eye='^')])
    duet(o, 'tug_of_war_over_the_stalk', 'Pulling the stalk in a tug of war while a friend hauls on the cap lip', 22, 'none',
        [k(.1, 'stalk', x=.8, y=.9, b=.5), k(.26, 'stalk', x=1.3, y=1.1, b=1, l=1, mark='hnn'), k(.44, 'stalk', x=1.5, y=1.1, b=1.2, r=1), k(.62, 'stalk', x=1.2, y=1, b=.9, l=1, mark='HNN'), k(.82, eye='^')],
        [], g='play', act=('pull', 'stalk'), obj=[(.26, dict(sway=.5)), (.44, dict(shake=.6, ix=1)), (.62, dict(ix=-1, shake=.4)), (.74, dict(ix=0))],
        duo=[k(.12, 'cap_l', x=.7, y=.8, b=.4), k(.3, 'cap_l', x=1.3, y=1, b=1, l=1, mark='grr'), k(.5, 'cap_l', x=1.5, y=1, b=1.3, r=1), k(.7, 'cap_l', x=1.2, y=.9, b=.9, mark='HNN')])
    duet(o, 'steady_it_while_he_stands_on_cap', 'Stacking himself on the flat cap while a friend steadies the acorn with a wing', 22, 'none',
        [k(.08, 'cap_l', x=.5, y=.5, b=.4), k(.22, 'cap_top', perch=1, x=-.3, y=-.3, b=-.5, w=.7), k(.4, 'cap_top', perch=1, x=-.5, y=-.6, b=-.7, l=1, w=1), k(.58, 'cap_top', perch=1, x=.4, y=-.3, b=-.4, r=1, w=1), k(.74, 'cap_top', perch=1, x=-.2, y=-.5, b=-.5, w=.8, eye='^'), k(.88, 'cap_r', x=.3, y=.5, b=.3)],
        [], g='show', act=('stack', 'cap'), ages=GROWN, obj=[(.22, dict(sway=.1, glow=.2)), (.4, dict(sway=.15)), (.58, dict(sway=-.2)), (.74, dict(sway=0, glow=0))],
        duo=[k(.15, 'shell_belly', x=.4, y=.4, b=.5), k(.32, 'shell_belly', x=.8, y=.7, b=.9, mark='hold it'), k(.55, 'shell_belly', x=.8, y=.7, b=1, l=1), k(.78, 'shell_belly', x=.6, y=.5, b=.6, eye='^')])
    duet(o, 'keep_it_away_from_a_friend', 'Carrying the acorn off by the stalk, holding it high while a friend jumps for it', 24, 'none',
        [k(.1, 'cap_r', x=.8, y=.9, b=.4), k(.24, 'cap_r', x=1.2, y=1.2, b=.8, mark='nyah'), k(.42, 'stalk', x=-.3, y=-.6, b=-.8, l=1, w=.4, eye='^'), k(.6, 'stalk', x=.4, y=-.5, b=-.6, r=1, w=.5), k(.8, 'stalk', x=1.2, y=1, b=.7, mark='fine'), k(.92, eye='^')],
        [], g='play', act=('carry', 'acorn'), prefer=['grumpy'],
        obj=[(.24, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1, iy=-1)), (.66, dict(hold=1)), (.8, dict(hold=0)), (.86, dict(hold=0))],
        duo=[k(.2, x=.5, y=.2, b=.2), k(.4, 'cap_r', x=1, y=-.4, b=-.9, w=.6, mark='gimme'), k(.58, 'cap_r', x=1.2, y=-.6, b=-1.2, w=.8, l=1, r=1), k(.78, 'cap_r', x=1, y=.3, b=.4, eye='>')])
    o.r('sit_down_by_the_point', 'Sitting down by the acorn point without looking, yelping, and rising fast', 14, 'none',
        [k(.14, 'tip', x=.2, y=.4, b=.6), k(.3, 'tip', x=.3, y=.6, b=1.6, mark='sit'), k(.44, 'tip', x=-.2, y=-.6, b=-1.6, l=1, r=1, w=1, eye='O', mark='YOW'), k(.66, 'shell_lowl', x=.8, y=.9, b=.5, l=1, eye='>'), k(.84, eye='-')],
        [(.3, 'dull')], g='mishap', act=('sit', 'tip'), obj=[(.3, dict(shake=.4)), (.44, dict(sway=.5)), (.66, dict(sway=0))],
        say=["Point first. Rump second. Lesson third.", "I sat on it. It won."])
    o.r('stub_a_toe_on_the_shell', 'Kicking the acorn too hard, stubbing a toe on the shell, and hopping on one foot', 16, 'none',
        [k(.12, 'shell_lowl', x=.3, y=.8, b=.6, l=1), k(.26, 'shell_lowl', x=-.5, y=.5, b=1, l=1, mark='pok'), k(.4, 'shell_lowl', x=1, y=1.2, b=1.5, r=1, w=.8, eye='@', mark='OW'), k(.58, x=.4, y=.6, b=-.8, r=1, eye='>'), k(.76, x=.2, y=.5, b=-.8, r=1, eye='>'), k(.9, eye='-')],
        [(.4, 'chip')], g='mishap', act=('kick', 'shell'), prefer=['grumpy'], obj=[(.26, dict(shake=.6)), (.4, dict(sway=.4)), (.7, dict(sway=0))],
        say=["Acorn: one. Toe: nil.", "Kicked a nut. Nut was fine."])
    o.r('toss_it_up_and_get_conked', 'Throwing the acorn straight up by the stalk and getting conked on the crown when it lands', 20, 'none',
        [k(.1, 'stalk', x=.8, y=.9, b=.4), k(.22, 'stalk', x=1.2, y=1.2, b=.8, l=1), k(.36, x=-.2, y=-1.3, b=-.9, w=.6, eye='O'), k(.52, x=-.3, y=-1.5, b=-.4, w=.6, eye='O'), k(.64, 'cap_top', x=.1, y=1.3, b=1.2, eye='@', mark='bonk'), k(.82, x=.2, y=.5, b=.4, eye='>')],
        [], g='mishap', act=('throw', 'acorn'), prefer=['curious'],
        obj=[(.22, dict(hold=1)), (.34, dict(hold=0, iy=-6)), (.5, dict(iy=-6)), (.62, dict(iy=-1)), (.7, dict(iy=0, shake=.3)), (.8, dict(shake=0))],
        say=["Gravity is a bully. I saw it coming. Too late.", "Up it went. Down it came. Skull is a net, apparently."])
    o.r('brood_on_the_cap', 'Sitting on the flat cap like it is an egg, wings tucked in, daring anything to hatch', 24, 'none',
        [k(.1, 'cap_l', x=.5, y=.5, b=.4), k(.24, 'cap_top', perch=1, x=-.2, y=.2, b=.6, w=.4), k(.46, 'cap_top', perch=1, x=-.3, y=.4, b=1, w=.2, eye='-', mark='...'), k(.7, 'cap_top', perch=1, x=-.2, y=.3, b=.8, eye='>'), k(.86, 'cap_top', x=.3, y=.5, b=.3)],
        [], g='rest', act=('sit', 'cap'), ages=GROWN, obj=[(.24, dict(glow=.2)), (.46, dict(glow=.4)), (.7, dict(glow=.2)), (.86, dict(glow=0))],
        say=["Sitting on it. If it hatches, I want credit.", "It is warm now. That is all me."])
    done(o)
    return o


def golden_acorn():
    # Same 18 x 15 drawing as the plain acorn (59 px, on its point) with three sparkle glyphs that are light, not parts: a `.` at the left of the cap,
    # a `*` above the right shoulder and a `+` at the right of the shell. Nothing there can be touched, so the touches are the same cap, shell and point.
    P = pm('golden_acorn')
    o = Obj('golden_acorn', 'portable', liftable=True,
            parts=dict(stalk='the short stalk on top', cap='the flat hatched cap', shell='the plain curved shell', tip='the pointed bottom it stands on'),
            marks=[('snow', .3, '.:*:.', 'cap_top', 'snow'), ('frost', .3, '*+*', 'cap_l', 'frost'), ('luster', .8, '`*`', 'shell_l', 'glow')],
            fields=dict(luster=(.5, 0, 1), snow=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('luster', 'rate', -.0004, 'wet'), ('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm'),
                     ('frost', 'rate', .0015, 'cold&!snow'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(wipe=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)], sweep=[('snow', 'mul', .2)], buff=[('luster', 'add', .35)],
                         scrape=[('frost', 'mul', .2)], mend=[('obj.condition', 'add', .3)], dull=[('luster', 'add', -.3)], dent=[('obj.condition', 'add', -.2)],
                         smudge=[('obj.dirt', 'add', .15)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], pride=[('need.social', 'add', 1)]),
            anchors=dict(stalk=P(9, 1), cap_top=P(9, 2, 'surface'), cap_l=P(6, 3), cap_r=P(15, 3), shell_l=P(4, 8), shell_r=P(15, 8), shell_mid=P(9, 8),
                         shell_belly=P(9, 10), shell_lowl=P(4, 10), shell_lowr=P(15, 10), tip=P(9, 14), tip_l=P(6, 14), tip_r=P(15, 14)))
    # ---------------- care
    o.r('huff_and_buff_the_cap', 'Huffing a breath on the cap and polishing it with the wing tip until it gleams again', 18, 'wing',
        [k(.1, 'cap_top', reach=.4, x=.9, y=.7, b=.3, mark='haa'), k(.26, 'cap_l', reach=1, x=.5, y=1, b=.5, l=1), k(.42, 'cap_top', reach=1, x=.6, y=1.1, b=.6), k(.58, 'cap_r', reach=1, x=.6, y=1, b=.5, r=1), k(.74, 'cap_top', reach=1, x=.4, y=.8, b=.3), k(.9, eye='^')],
        [(.58, 'buff')], g='care', act=('polish', 'cap'), when=['luster<.65'], obj=[(.42, dict(glow=.5)), (.62, dict(glow=1)), (.82, dict(glow=.3))],
        say=["Gleam restored. I am a professional.", "Shinier than my future."])
    o.r('wipe_off_the_beak_prints', 'Giving the shell a wipe-down to get the bill prints off, side to side with a wing', 16, 'wing',
        [k(.1, 'shell_l', reach=.4, x=.3, y=.5), k(.26, 'shell_l', reach=1, x=.5, y=.9, b=.4, l=1), k(.44, 'shell_mid', reach=1, x=.6, y=1, b=.5), k(.62, 'shell_r', reach=1, x=.5, y=.9, b=.4, r=1), k(.8, eye='-')],
        [(.44, 'wipe')], g='care', act=('wipe', 'shell'), when=['obj_dirt>.3'], say=["Prints gone. Evidence destroyed.", "Wiped it. Now it is only suspicious."])
    o.r('pat_the_wet_off_carefully', 'Patting the stalk and cap rim dry with the very tip of a wing', 18, 'wing',
        [k(.1, 'stalk', reach=.4, x=.2, y=.6, b=.1), k(.28, 'stalk', reach=1, x=.4, y=.8, b=.3, mark='pat'), k(.46, 'cap_l', reach=1, x=.5, y=.8, b=.4, l=1, mark='pat'), k(.64, 'cap_r', reach=1, x=.5, y=.8, b=.4, mark='pat'), k(.82, eye='-')],
        [(.46, 'dry')], g='care', act=('dry', 'stalk'), when=['obj_wetness>.3'])
    o.r('sweep_the_snow_off_the_cap', 'Sweeping the snow off the flat cap with sideways wing strokes', 14, 'wing',
        [k(.12, 'cap_top', reach=.4, x=.3, y=.6), k(.3, 'cap_top', reach=1, x=-.2, y=.8, b=.4, mark='shh'), k(.48, 'cap_top', reach=1, x=.9, y=.9, b=.5, mark='shh'), k(.66, 'cap_l', reach=1, x=.5, y=.7, b=.3), k(.84, eye='^')],
        [(.48, 'sweep')], g='care', act=('sweep', 'cap'), when=['snow>.3'], obj=[(.3, dict(puff=.4)), (.48, dict(puff=.6))])
    o.r('rub_out_a_scuff', 'Mending a scuff in the shell by rubbing it out in tight circles with his chest feathers', 20, 'none',
        [k(.12, 'shell_lowl', x=.4, y=.5, b=.4), k(.28, 'shell_belly', x=.6, y=.7, b=.7, l=1, mark='sqk'), k(.46, 'shell_lowr', x=.6, y=.7, b=.8, r=1, mark='sqk'), k(.64, 'shell_belly', x=.5, y=.6, b=.7, mark='sqk'), k(.84, x=.1, eye='^')],
        [(.46, 'mend')], g='care', act=('mend', 'shell'), when=['obj_condition<.7'], obj=[(.28, dict(glow=.3)), (.64, dict(glow=.6))], say=["Scuff gone. Not a mark on me. Or it.", "Mended with my chest. Professional chest."])
    o.r('pick_the_dirt_from_the_hatching', 'Scrubbing the dirt out of the cap hatching with a twig, one cross-hatch at a time', 20, 'twig',
        [k(.1, 'cap_l', reach=.5, x=.4, y=.4), k(.26, 'cap_l', reach=1, x=.8, y=.7, b=.3, mark='tik'), k(.42, 'cap_top', reach=1, x=.9, y=.7, b=.4, mark='tik'), k(.58, 'cap_r', reach=1, x=.9, y=.7, b=.4, mark='tik'), k(.74, 'cap_top', reach=1, x=.8, y=.6, b=.3), k(.9, eye='^')],
        [(.58, 'wipe')], g='care', act=('scrub', 'hatching'), when=['obj_dirt>.5'])
    # ---------------- use
    o.r('tiptoe_it_to_a_safer_spot', 'Carrying the acorn by the stalk, tiptoeing it a few steps off as if it might wake up', 26, 'none',
        [k(.08, 'stalk', x=.6, y=.9, b=.4), k(.2, 'stalk', x=1, y=1.1, b=.5, mark='easy'), k(.34, 'stalk', x=.2, y=-.4, b=-.2, l=1), k(.46, 'stalk', x=.1, y=-.5, b=-.1, r=1), k(.58, 'stalk', x=.2, y=-.4, b=-.2, l=1),
         k(.7, 'stalk', x=.9, y=.9, b=.5), k(.82, 'stalk', x=.7, y=.7, b=.4), k(.94, eye='^')],
        [], g='use', act=('carry', 'stalk'), prefer=['curious'],
        obj=[(.2, dict(hold=0)), (.3, dict(hold=1)), (.5, dict(hold=1)), (.62, dict(hold=0, ix=4)), (.66, dict(hold=0, ix=4)), (.74, dict(hold=1, ix=4)), (.84, dict(hold=1)), (.9, dict(hold=0))],
        say=["Moved it. It is safer now. Probably.", "Tiptoed. A duck of rare delicacy."])
    o.r('stash_it_and_look_round', 'Scraping a pocket to hide the acorn, dropping it in and looking about for thieves, then unearthing it', 30, 'none',
        [k(.08, 'stalk', x=.9, y=1, b=.5), k(.2, 'stalk', x=1.1, y=1.1, b=.6), k(.32, 'tip_r', x=.9, y=1.5, b=1.1, r=1, mark='skrt'), k(.42, 'tip_r', x=-.5, y=-.6, b=-.3, w=.5, eye='<'),
         k(.52, x=.6, y=-.5, b=-.3, w=.5, eye='>'), k(.66, 'tip_l', x=1.1, y=1.6, b=1.2, l=1, mark='skrt'), k(.8, 'tip_l', x=1.2, y=1.4, b=1, eye='^'), k(.92, eye='-')],
        [], g='use', act=('hide', 'gleam'), prefer=['curious'],
        obj=[(.2, dict(hold=0)), (.26, dict(hold=1)), (.34, dict(hold=1, hide=1)), (.4, dict(hold=0, hide=1)), (.56, dict(hide=1)), (.66, dict(hide=1)), (.74, dict(hide=0)), (.8, dict(hide=0))],
        say=["Stashed. Unseen. Probably a pigeon saw.", "Gold is secure. My nerves are not."])
    o.r('heave_it_a_hand_along', 'Pushing the acorn along the ground with his shoulder and finding it weighs a lot more than it looks', 22, 'none',
        [k(.1, 'shell_l', x=.2, y=.5, b=.5), k(.24, 'shell_l', x=.9, y=.8, b=1.2, l=1, mark='hnnng'), k(.4, 'shell_l', x=1.1, y=.9, b=1.4, r=1, mark='HNNNG'), k(.54, 'shell_l', x=.9, y=.7, b=1, eye='>'), k(.72, 'cap_l', x=1.2, y=1, b=.6, eye='-'), k(.88, eye='^')],
        [(.4, 'dull')], g='use', act=('push', 'shell'), ages=GROWN, obj=[(.24, dict(ix=0)), (.4, dict(ix=1, shake=.3)), (.54, dict(ix=1)), (.62, dict(ix=1, hold=0)), (.74, dict(ix=0))],
        say=["Heavy. Gold is heavy. So is regret.", "Moved it a hand's width. Sweating. Worth it."])
    o.r('roll_it_slow_and_fetch', 'Rolling it a short way with the bill, wincing at every bump, then fetching it back by the stalk', 26, 'none',
        [k(.1, 'shell_lowr', x=.5, y=.8, b=.5), k(.22, 'shell_lowr', x=1.2, y=1, b=.8, mark='ngh'), k(.34, x=.5, y=.4, b=.2, eye='>'), k(.46, x=.9, y=.6, b=.3, l=1, r=1), k(.6, 'stalk', x=1.2, y=1, b=.7), k(.74, 'stalk', x=.3, y=-.2, b=-.2, l=1), k(.88, eye='^')],
        [(.22, 'smudge')], g='use', act=('roll', 'shell'),
        obj=[(.22, dict(ix=0)), (.3, dict(ix=3, shake=.2)), (.46, dict(ix=5)), (.54, dict(ix=5)), (.62, dict(ix=5, hold=1)), (.76, dict(ix=0, hold=1)), (.84, dict(hold=0))],
        say=["Rolled it. Dirt got it. I am furious.", "Fetched it by the stalk. Very gentlemanly."])
    o.r('weigh_the_gold_in_the_bill', 'Hoisting the acorn off the ground by the stalk, grunting, and judging its weight', 20, 'none',
        [k(.08, 'stalk', x=.6, y=.8, b=.4), k(.2, 'stalk', x=1.2, y=1.2, b=1, l=1, mark='hnnh'), k(.36, 'stalk', x=1.1, y=.6, b=1.3, r=1, eye='>'), k(.5, 'stalk', x=1, y=.9, b=1.4, l=1, r=1), k(.66, 'stalk', x=1.2, y=1.2, b=.9), k(.82, eye='-')],
        [], g='test', act=('weigh', 'acorn'), obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1, iy=1)), (.68, dict(hold=0))],
        say=["Heavier than bread. Barely.", "Weighed it. Judged it. Gold weighs gold."])
    o.r('tilt_it_to_catch_the_sun', 'Tilting the acorn by the cap so a flash of sun swings off the shell', 18, 'none',
        [k(.12, 'cap_l', x=.7, y=.8, b=.3), k(.3, 'cap_l', x=1.3, y=1.1, b=.8, mark='hup'), k(.5, 'cap_r', x=-.2, y=1, b=.8, eye='O'), k(.68, 'cap_l', x=1, y=.9, b=.6), k(.84, eye='^')],
        [], g='use', act=('tilt', 'shell'), when=['sun'], obj=[(.3, dict(sway=.5, glow=.4)), (.5, dict(sway=-.5, glow=1)), (.68, dict(sway=.2, glow=.5)), (.82, dict(sway=0, glow=0))],
        say=["Flash! Blind. Worth it.", "Made a small sun. A small sun. Unrequested but welcome."])
    # ---------------- play
    o.r('lob_it_and_catch_it_soft', 'Lobbing the acorn a hand above the ground and catching it softly on the way down', 20, 'none',
        [k(.1, 'stalk', x=.7, y=1, b=.5), k(.24, 'stalk', x=1.2, y=1.3, b=.9), k(.36, x=.6, y=-1.4, b=-.9, w=.5, eye='O'), k(.5, x=.8, y=-.8, b=-.2, w=.3), k(.62, 'shell_belly', x=1.3, y=1.2, b=1, mark='ooh'), k(.8, x=.2, eye='^')],
        [], g='play', act=('catch', 'acorn'), prefer=['happy'],
        obj=[(.24, dict(hold=1)), (.32, dict(hold=1)), (.4, dict(hold=0, iy=-4)), (.5, dict(hold=0, iy=-4)), (.58, dict(hold=1, iy=0)), (.74, dict(hold=0))])
    o.r('hop_round_it_in_delight', 'Hopping in a circle round the acorn, one wing up, while the gleam follows him', 18, 'none',
        [k(.1, 'shell_l', x=.2, y=-.5, b=-1, l=1, w=.5), k(.26, 'shell_lowl', x=.3, y=.4, b=.5, r=1, w=.9), k(.42, 'tip_l', x=.2, y=-.6, b=-1.2, l=1, r=1, w=.9), k(.58, 'shell_lowr', x=.3, y=.4, b=.6, l=1, w=.8), k(.74, 'shell_r', x=.2, y=-.7, b=-1.2, r=1, w=1), k(.88, eye='^')],
        [(.26, 'fun')], g='play', act=('hop', 'acorn'), prefer=['happy'], obj=[(.26, dict(glow=.3)), (.58, dict(glow=.6)), (.74, dict(glow=.2))])
    o.r('race_a_lap_round_it', 'Running a race round the acorn with a wing out, daring it to keep up', 18, 'none',
        [k(.08, 'tip', x=.3, y=.6, b=.6), k(.22, 'tip_l', x=1.4, y=.2, b=-.4, l=1, w=.6), k(.38, 'shell_lowl', x=1.5, y=.2, b=-.5, r=1, w=.8), k(.54, 'shell_l', x=1.6, y=.2, b=-.5, l=1, w=1), k(.7, 'shell_r', x=1.4, y=.3, b=-.4, r=1, w=.8), k(.86, 'tip', x=.2, y=.5, b=.5, eye='^')],
        [], g='play', act=('race', 'acorn'), prefer=['young'], say=["Lapped it. It did not try. Cheat.", "I win. It cannot even run."])
    o.r('keep_it_high_from_the_wind', 'Lifting the acorn by the cap lip and lowering it again, over and over, like a trophy', 24, 'none',
        [k(.1, 'cap_r', x=.8, y=1, b=.5), k(.22, 'cap_r', x=1.3, y=1.3, b=1, mark='hup'), k(.36, 'cap_r', x=.5, y=-.8, b=-.8, w=.5, eye='^'), k(.5, 'cap_r', x=1.2, y=1.2, b=.9), k(.64, 'cap_r', x=.4, y=-.9, b=-.9, w=.6, eye='^'), k(.8, 'cap_r', x=1, y=1, b=.7), k(.92, eye='-')],
        [], g='play', act=('lift', 'cap'), prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.32, dict(hold=1)), (.44, dict(hold=1, iy=-1)), (.5, dict(hold=1)), (.62, dict(hold=1, iy=-1)), (.72, dict(hold=1)), (.82, dict(hold=0))])
    o.r('bat_it_back_and_forth_gently', 'Nudging the acorn to and fro along the ground with the bill, a hand each way', 18, 'none',
        [k(.1, 'shell_l', x=.7, y=.8, b=.4), k(.24, 'shell_l', x=1.2, y=.9, b=.6, mark='tk'), k(.4, 'shell_r', x=-.3, y=.8, b=.6, r=1, mark='tk'), k(.56, 'shell_l', x=1.2, y=.9, b=.6, l=1, mark='tk'), k(.74, 'shell_mid', x=.6, y=.6, b=.4), k(.9, eye='^')],
        [], g='play', act=('nudge', 'shell'), obj=[(.24, dict(ix=1)), (.4, dict(ix=-1)), (.56, dict(ix=1)), (.7, dict(ix=0)), (.74, dict(ix=0, shake=.2))])
    # ---------------- test
    o.r('bite_it_to_see_if_it_is_real', 'Testing the cap rim with a bite to see if it is real, then wincing', 14, 'none',
        [k(.12, 'cap_l', x=.9, y=.8, b=.3), k(.3, 'cap_l', x=1.4, y=1.2, b=.8, mark='crk'), k(.46, 'cap_l', x=1.4, y=1.2, b=.9, eye='O'), k(.62, x=-.9, y=.3, w=.6, eye='>', mark='ow'), k(.8, eye='-')],
        [], g='test', act=('test', 'cap'), say=["Hard. Real. My tooth: also hard. No teeth.", "It is real gold. I tested it with my face."])
    o.r('rap_it_for_the_ring', 'Rapping the shell with the bill and listening for the ring of good gold', 16, 'none',
        [k(.12, 'shell_mid', x=.8, y=.9, b=.3), k(.28, 'shell_mid', x=1.3, y=1.4, b=.7, mark='tink'), k(.44, x=-.4, y=-.4, eye='O'), k(.6, 'shell_lowl', x=1.3, y=1.4, b=.7, mark='tink'), k(.76, x=-.3, y=-.4, eye='^', mark='ding')],
        [], g='test', act=('ring', 'shell'), obj=[(.28, dict(shake=.2, glow=.3)), (.6, dict(shake=.2, glow=.5))])
    o.r('count_it_twice', 'Counting the acorns by the stalk, one, and counting again in case it multiplied', 18, 'none',
        [k(.1, 'stalk', x=.6, y=.7, b=.2, mark='one'), k(.26, 'cap_top', x=.8, y=.9, b=.4), k(.4, 'tip', x=.5, y=1.2, b=.9, mark='...one'), k(.56, 'stalk', x=1, y=1, b=.5, mark='again'), k(.72, 'tip', x=.5, y=1.2, b=1, eye='^', mark='one'), k(.88, eye='-')],
        [], g='test', act=('count', 'acorn'), say=["One. Still one. Suspicious.", "Counted twice. Both ones. Money is simple."])
    o.r('stretch_my_face_in_the_gold', 'Showing the gold shell his best faces and watching them stretch out of shape', 16, 'none',
        [k(.12, 'shell_mid', x=.5, y=.3, b=.2), k(.28, 'shell_mid', x=1.5, y=.5, b=.4, eye='O'), k(.46, 'shell_mid', x=1.5, y=.6, b=.5, eye='>', mark='bwah'), k(.62, 'shell_belly', x=1.4, y=.7, b=.6, eye='^'), k(.8, eye='-')],
        [], g='show', act=('show', 'shell'), obj=[(.28, dict(glow=.4)), (.62, dict(glow=.2))], say=["Long face. Accurate.", "In the gold I look expensive. Fine."])
    o.r('sniff_the_cold_metal', 'Sniffing along the stalk and down the shell for the smell of money', 14, 'none',
        [k(.12, 'stalk', x=.6, y=.5, b=.2), k(.28, 'stalk', x=1, y=.7, b=.3, mark='snff'), k(.46, 'shell_r', x=1, y=.7, b=.4, mark='snff'), k(.64, 'shell_lowr', x=1, y=.8, b=.5), k(.8, x=-.4, eye='-', mark='meh')],
        [], g='test', act=('sniff', 'stalk'))
    o.r('knock_it_with_a_twig', 'Knocking the shell once with a twig from a respectful distance', 14, 'twig',
        [k(.1, 'shell_r', reach=.4, x=.6, y=.3, b=.4), k(.3, 'shell_mid', reach=1, x=.9, y=.1, b=.6, mark='tock'), k(.46, 'shell_r', reach=1, x=.2, y=-.5, b=-.3), k(.64, 'shell_mid', reach=1, x=1, y=.2, b=.7, mark='tock'), k(.82, eye='^')],
        [], g='test', act=('knock', 'shell'), obj=[(.34, dict(sway=.3, glow=.2))])
    # ---------------- rest
    o.r('sit_on_it_like_an_egg', 'Sitting on the flat cap like a hen on an egg, wings out over the gold', 30, 'none',
        [k(.08, 'cap_top', x=.5, y=.6, b=.3), k(.2, 'cap_top', perch=1, x=-.2, y=.3, b=1.2, w=.6), k(.4, 'cap_top', perch=1, x=-.4, y=.6, b=1.8, w=.8, eye='-'), k(.62, 'cap_top', perch=1, x=-.3, y=.7, b=1.9, eye='-', mark='mmm'), k(.84, 'cap_top', x=.2, y=.4, b=.6, eye='^')],
        [(.62, 'rest')], g='rest', act=('sit', 'cap'), ages=GROWN, obj=[(.2, dict(sway=.1)), (.62, dict(sway=.1))], say=["Hatching it. Nothing yet. Patience.", "It is warm from my bum. Do not tell."])
    o.r('doze_with_a_wing_over_it', 'Napping with a wing flopped over the acorn so no thief can take it', 30, 'none',
        [k(.12, 'shell_mid', x=.4, y=.4, b=.7, w=.4), k(.32, 'shell_mid', x=.6, y=.8, b=1.4, w=1, eye='-'), k(.56, 'shell_mid', x=.6, y=1, b=1.6, w=1, eye='-', mark='zzz'), k(.8, 'shell_mid', x=.5, y=.9, b=1.5, w=1, eye='-', mark='zz')],
        [(.56, 'rest')], g='rest', act=('nap', 'acorn'), prefer=['tired'], when=['tired'])
    o.r('guard_it_chest_out', 'Guarding the acorn with his chest puffed and one foot raised, daring the yard', 24, 'none',
        [k(.1, 'shell_belly', x=.2, y=-.8, b=-.4, w=.8), k(.28, 'shell_belly', x=.4, y=-1, b=-.6, l=1, w=1, eye='>'), k(.5, 'shell_belly', x=.2, y=-1, b=-.6, r=1, w=1), k(.7, 'shell_belly', x=.4, y=-1, b=-.6, l=1, w=1, eye='>'), k(.88, eye='^')],
        [(.5, 'pride')], g='rest', act=('guard', 'acorn'), prefer=['grumpy'])
    o.r('slump_against_it_broke', 'Sulking against the shell, tail down, because he cannot spend it', 26, 'none',
        [k(.12, 'shell_r', x=.6, y=-.4, b=-.3, w=.5), k(.3, 'shell_r', x=.9, y=.9, b=1.2, eye='-'), k(.55, 'shell_r', x=1.1, y=1.6, b=1.9, eye='-', mark='sigh'), k(.8, 'shell_r', x=.8, y=.6, b=.8, eye='>', mark='hmph')],
        [], g='rest', act=('sulk', 'gold'), prefer=['sad'], say=["Rich. Unspendable. Solid.", "Gold acorn. Zero bread. Systemic failure."])
    # ---------------- weather
    o.r('squint_at_the_flash', 'Peering through a squint at the flash of sun off the shell, head turned to dodge it', 18, 'none',
        [k(.12, 'shell_mid', x=.5, y=.3, b=.2), k(.3, 'shell_mid', x=1.3, y=.4, b=.5, eye='O'), k(.46, 'shell_mid', x=-.8, y=-.3, w=.6, eye='-', mark='ack'), k(.64, 'shell_mid', x=1, y=.3, b=.4, eye='O'), k(.82, eye='^')],
        [], g='weather', act=('peer', 'glint'), when=['sun', 'day'], obj=[(.3, dict(glow=.6)), (.46, dict(glow=1)), (.64, dict(glow=.5)), (.8, dict(glow=0))])
    o.r('chip_the_frost_off_the_shell', 'Chipping the frost off the shell with a twig tip, a little at a time', 20, 'twig',
        [k(.1, 'shell_l', reach=.5, x=.4, y=.4), k(.26, 'shell_l', reach=1, x=.8, y=.7, b=.3, mark='tik'), k(.44, 'shell_mid', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.62, 'shell_r', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.8, eye='-')],
        [(.44, 'scrape')], g='weather', act=('chip', 'shell'), when=['frost>.3'])
    o.r('pin_it_down_in_the_gust', 'Bracing against the gust, pinning the acorn down by the stalk with his bill', 24, 'none',
        [k(.1, 'stalk', x=.8, y=.9, b=.5), k(.26, 'stalk', x=1.3, y=1.3, b=1, l=1, mark='hff'), k(.48, 'stalk', x=1.5, y=1.2, b=1.3, r=1, eye='>'), k(.7, 'stalk', x=1.2, y=1, b=.9, l=1), k(.88, eye='^')],
        [], g='weather', act=('brace', 'stalk'), when=['windy'], obj=[(.26, dict(sway=.5)), (.48, dict(sway=-.7, shake=.4)), (.7, dict(sway=.2))])
    o.r('dash_after_it_in_the_wind', 'Chasing the acorn as the wind rolls it off, and carrying it home, panting', 24, 'none',
        [k(.1, 'shell_r', x=.4, y=.3, b=.2, w=.4), k(.24, x=1.7, y=.2, b=-.3, l=1, r=1, w=.9, eye='O'), k(.42, x=1.5, y=.8, b=.6), k(.56, 'stalk', x=1.3, y=1, b=.8, mark='MINE'), k(.72, 'stalk', x=.3, y=-.3, b=-.3, l=1), k(.88, eye='^')],
        [], g='weather', act=('chase', 'acorn'), when=['windy'],
        obj=[(.18, dict(ix=0)), (.26, dict(ix=3, shake=.4)), (.4, dict(ix=7)), (.5, dict(ix=7)), (.6, dict(ix=7, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0))],
        say=["Not the gold. Anything but the gold.", "Ran, grabbed, panted. Cardio."])
    # ---------------- show
    o.r('bow_to_the_gold', 'Bowing three times to the gold acorn, lower each time', 18, 'none',
        [k(.1, 'cap_top', x=.2, y=.5, b=.4), k(.24, 'cap_top', x=1.1, y=1.4, b=1.4, mark='sire'), k(.4, 'cap_top', x=1.3, y=1.7, b=1.7, mark='sire'), k(.56, 'cap_top', x=1.5, y=1.9, b=2, mark='SIRE'), k(.74, x=.1, y=-.3, b=-.2, eye='^')],
        [], g='show', act=('bow', 'gold'), say=["Your Shininess.", "Bowed thrice. It did not blink."])
    o.r('dance_a_jig_in_the_glow', 'Dancing a jig beside the gold while it throws light across him', 20, 'none',
        [k(.1, 'shell_belly', x=.2, y=-.4, b=-.6, l=1, w=.6), k(.24, 'shell_belly', x=.4, y=.5, b=.7, r=1, w=1), k(.4, 'shell_belly', x=-.2, y=-.7, b=-1, l=1, w=.9), k(.56, 'shell_belly', x=.5, y=.6, b=.8, r=1, w=1), k(.74, 'shell_belly', x=.3, y=-.7, b=-1, l=1, w=.8), k(.88, eye='^')],
        [], g='show', act=('dance', 'gold'), prefer=['happy'], obj=[(.24, dict(glow=.4)), (.56, dict(glow=.8)), (.8, dict(glow=.3))])
    o.r('serenade_it_with_a_ballad', 'Singing the acorn a slow ballad with a wing pressed to his chest', 24, 'none',
        [k(.1, 'cap_l', x=.3, y=-.3, b=-.3, w=.4), k(.28, 'cap_l', x=-.5, y=-1, b=-.8, w=.7, eye='-', mark='laa'), k(.48, 'shell_l', x=1.2, y=-1.2, b=-1.2, w=.9, mark='LAAA'), k(.68, 'shell_l', x=.5, y=.8, b=.9, eye='^', mark='sniff'), k(.84, eye='-')],
        [], g='show', act=('sing', 'gold'), prefer=['lonely'])
    # ---------------- mishap
    o.r('slip_on_the_shine', 'Slipping a foot off the slick shell and landing flat on his chest', 16, 'none',
        [k(.1, 'shell_lowl', x=.5, y=.6, b=.3, r=1), k(.26, 'shell_lowl', x=1, y=.9, b=.7, r=1, mark='eh'), k(.42, 'tip_l', x=1.5, y=1.7, b=2, l=1, r=1, w=1, eye='O', mark='WHA'), k(.6, x=1.7, y=2, b=2.2, eye='@'), k(.8, x=.4, y=.8, b=.6, eye='-')],
        [(.26, 'dent')], g='mishap', act=('slip', 'shell'), prefer=['grumpy'], obj=[(.26, dict(shake=.5)), (.42, dict(sway=.6))], say=["Gold is slippery. Noted. Humiliating.", "Down I went. The acorn stayed shiny."])
    o.r('stick_my_bill_in_the_crosshatch', 'Wedging his bill in the cap hatching to get a better look and getting stuck fast', 22, 'none',
        [k(.12, 'cap_l', x=1, y=.7, b=.3), k(.28, 'cap_l', x=1.5, y=.9, b=1, mark='mm'), k(.44, 'cap_l', x=1.6, y=1, b=1.4, l=1, r=1, eye='O', mark='MPH'), k(.62, 'cap_l', x=1.7, y=1, b=1.5, w=1, mark='POP'), k(.8, x=-1.5, y=.4, b=.3, eye='@')],
        [(.44, 'dent')], g='mishap', act=('stuck', 'hatching'), prefer=['curious'], obj=[(.28, dict(sway=.4)), (.44, dict(shake=.6)), (.62, dict(sway=-.6))])
    # ---------------- more gold-only acts
    o.r('cool_off_on_the_cold_gold', 'Pressing his hot cheek and breast to the cold shell to cool off', 22, 'none',
        [k(.12, 'shell_l', x=.6, y=.4, b=.5), k(.3, 'shell_l', x=1, y=.5, b=.9, w=.3, eye='-'), k(.52, 'shell_belly', x=1, y=.7, b=1.2, eye='-', mark='ahh'), k(.76, 'shell_r', x=.8, y=.5, b=.8, eye='^')],
        [], g='weather', act=('cool', 'shell'), when=['warm', 'day'], say=["Cold gold. Best thing it has ever done.", "Money is cool. Literally. Briefly."])
    o.r('shake_it_for_a_rattle', 'Holding the acorn by the stalk and shaking it by his ear for a rattle, and getting none', 18, 'none',
        [k(.1, 'stalk', x=.7, y=.9, b=.4), k(.24, 'stalk', x=1.2, y=1.2, b=.8), k(.38, 'stalk', x=-.4, y=.2, b=.3, l=1, mark='shk'), k(.5, 'stalk', x=-.5, y=.1, b=.2, r=1, mark='shk'), k(.64, 'stalk', x=-.4, y=.2, b=.3, eye='O', mark='...'), k(.8, 'stalk', x=1, y=1, b=.6)],
        [], g='test', act=('shake', 'shell'), obj=[(.24, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1, shake=.6)), (.66, dict(hold=1)), (.78, dict(hold=0))],
        say=["Solid. No rattle. Dull inside.", "Shook it. Nothing. Same as my last plan."])
    o.r('hurl_it_in_a_huff_and_fetch', 'Throwing the acorn at the grass in a huff, then scuttling after it, sorry', 24, 'none',
        [k(.08, 'cap_r', x=.8, y=1, b=.6), k(.2, 'cap_r', x=1.3, y=1.3, b=1, l=1), k(.34, x=-.7, y=-.6, b=-.7, w=1, eye='>', mark='BAH'), k(.5, x=1.3, y=.5, b=.4, l=1, r=1), k(.62, 'cap_r', x=1.4, y=1.1, b=.9, eye='O', mark='oh no'), k(.78, 'cap_r', x=.4, y=-.1, b=-.2, l=1), k(.9, eye='-')],
        [(.62, 'smudge')], g='play', act=('throw', 'cap'), prefer=['grumpy'],
        obj=[(.2, dict(hold=0)), (.3, dict(hold=1)), (.36, dict(hold=.2, ix=4, iy=-2)), (.44, dict(hold=0, ix=7, iy=0)), (.54, dict(ix=7)), (.64, dict(hold=1, ix=7)), (.78, dict(hold=1, ix=0)), (.86, dict(hold=0))],
        say=["Threw the gold. Found it. Never again. Possibly.", "Rage, grass, apology. In that order."])
    o.r('drag_it_like_a_heavy_sack', 'Dragging the acorn off by the stalk like a heavy sack, then dragging it all the way back', 26, 'none',
        [k(.08, 'stalk', x=.7, y=.9, b=.5), k(.22, 'stalk', x=1.3, y=1.2, b=1.2, l=1, mark='hnn'), k(.4, 'stalk', x=-.4, y=1, b=1.4, r=1), k(.56, 'stalk', x=-.5, y=1.1, b=1.5, l=1, mark='hnn'), k(.72, 'stalk', x=.3, y=.9, b=1.2, r=1), k(.88, eye='^')],
        [], g='use', act=('drag', 'stalk'), ages=GROWN, obj=[(.22, dict(ix=0)), (.4, dict(ix=-3)), (.48, dict(ix=-3, shake=.2)), (.6, dict(ix=-2)), (.74, dict(ix=0))])
    o.r('burnish_the_whole_shell', 'Grooming the whole shell from point to cap with long burnishing wing strokes', 24, 'wing',
        [k(.08, 'tip_r', reach=.4, x=.3, y=.8, b=.7), k(.22, 'shell_lowr', reach=1, x=.5, y=.9, b=.6, l=1), k(.36, 'shell_r', reach=1, x=.5, y=.8, b=.5), k(.5, 'shell_l', reach=1, x=.5, y=.8, b=.5, r=1), k(.64, 'shell_lowl', reach=1, x=.5, y=.9, b=.6), k(.78, 'tip_l', reach=1, x=.4, y=.9, b=.7, l=1), k(.92, eye='^')],
        [(.5, 'buff')], g='care', act=('groom', 'shell'), when=['luster<.55'], obj=[(.36, dict(glow=.3)), (.5, dict(glow=.7)), (.64, dict(glow=1)), (.84, dict(glow=.2))])
    o.r('stand_on_it_like_a_podium', 'Perching on the flat cap with a wing raised like a medal winner', 22, 'none',
        [k(.08, 'cap_top', x=.5, y=.5, b=.4), k(.2, 'cap_top', perch=1, x=-.1, y=-.5, b=-.7, w=.6), k(.38, 'cap_top', perch=1, x=-.2, y=-.9, b=-1, l=1, w=1.2, eye='^', mark='yes'), k(.58, 'cap_top', perch=1, x=-.1, y=-1, b=-1.1, r=1, w=1.3, eye='^', mark='YES'), k(.76, 'cap_top', perch=1, x=.1, y=-.7, b=-.8, w=1, eye='^'), k(.9, 'cap_top', x=.3, y=.5, b=.4)],
        [], g='show', act=('perch', 'cap'), ages=GROWN, obj=[(.2, dict(sway=.1)), (.4, dict(sway=-.2, glow=.3)), (.58, dict(sway=.3, glow=.5)), (.76, dict(sway=0))],
        say=["Gold medal. On a gold acorn. Tidy.", "First place. Only competitor: me."])
    o.r('bellow_a_warning', 'Shouting a warning at the whole yard, wings up, bill pointed at the sky', 16, 'none',
        [k(.15, x=.4, y=.9, b=.8), k(.35, x=-.8, y=-1.5, b=-1.1, w=1, eye='O', mark='MINE'), k(.55, x=-1, y=-1.8, b=-1.3, w=1.2, mark='MINE!!'), k(.75, x=.2, y=.7, b=.6, eye='>')],
        [], g='show', act=('shout', 'yard'), far=True, prefer=['grumpy'], say=["Whole yard on notice. One acorn. Mine.", "Shouted it. Pigeons nodded. Fine."])
    o.r('lose_the_gold_on_his_foot', 'Lifting the acorn by the stalk to show it off and dropping it on his own foot', 20, 'none',
        [k(.1, 'stalk', x=.7, y=.9, b=.5), k(.24, 'stalk', x=1.2, y=1.2, b=1, l=1), k(.4, 'stalk', x=.3, y=-.8, b=-.8, w=.5, eye='^', mark='behold'), k(.54, 'stalk', x=.2, y=1, b=.6, r=1, eye='O', mark='oop'), k(.7, x=.4, y=.9, b=-.6, l=1, eye='@', mark='YOWCH'), k(.88, eye='>')],
        [(.54, 'dent')], g='mishap', act=('lift', 'stalk'), prefer=['happy'],
        obj=[(.24, dict(hold=0)), (.34, dict(hold=1)), (.46, dict(hold=1, iy=-1)), (.56, dict(hold=0, iy=0, shake=.4)), (.74, dict(shake=0))],
        say=["Gold is heavy. Feet are soft. Maths.", "Dropped a fortune on my toe."])
    o.r('tug_and_topple_backwards', 'Tugging the stalk against the weight of the gold until it lets go and he topples onto his tail', 20, 'none',
        [k(.1, 'stalk', x=.6, y=.8, b=.5), k(.26, 'stalk', x=-.4, y=1, b=1.3, l=1, mark='hnn'), k(.42, 'cap_r', x=-.6, y=1.1, b=1.5, r=1, mark='HNNN'), k(.56, x=-1.6, y=-.4, b=-.6, w=1, eye='O', mark='whoa'), k(.74, x=-1.5, y=1.7, b=2.1, eye='@'), k(.9, x=.2, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('tug', 'stalk'), prefer=['curious'], obj=[(.26, dict(shake=.2)), (.42, dict(shake=.4)), (.56, dict(sway=.3)), (.7, dict(sway=0, shake=0))],
        say=["The acorn won. Gold has leverage.", "Flat on my back. The acorn stood there."])
    o.r('dig_it_a_firm_footing', 'Digging a little footing at the point with both feet so the gold stands firm', 22, 'none',
        [k(.1, 'tip', x=.5, y=1, b=.8, l=1), k(.26, 'tip_l', x=.6, y=1.4, b=1.2, l=1, mark='skrt'), k(.42, 'tip_r', x=.6, y=1.4, b=1.2, r=1, mark='skrt'), k(.58, 'tip', x=.6, y=1.4, b=1.3, l=1, mark='skrt'), k(.76, 'tip', x=.3, y=.9, b=.6, eye='^'), k(.9, eye='-')],
        [], g='care', act=('dig', 'tip'), obj=[(.42, dict(shake=.2)), (.58, dict(shake=.3)), (.76, dict(sway=0))], say=["Planted it. Plumb as a plank.", "Firm footing. For a nut. Sure."])
    o.r('rake_the_grit_from_the_point', 'Giving the point a rake with one foot, clearing the grit a scrape at a time', 18, 'none',
        [k(.12, 'tip_l', x=.3, y=.9, b=.7, l=1), k(.28, 'tip_l', x=.5, y=1.2, b=1.1, l=1, mark='skrt'), k(.44, 'tip', x=.5, y=1.2, b=1.1, r=1, mark='skrt'), k(.6, 'tip_r', x=.5, y=1.2, b=1.1, l=1, mark='skrt'), k(.8, eye='^')],
        [(.44, 'wipe')], g='care', act=('rake', 'tip'), when=['obj_dirt>.4'], say=["Gold out of the gutter.", "Raked it clean. Foot: filthy."])
    o.r('wrap_the_gleam_up_at_night', 'Wrapping both wings round the gold to keep the glint from the moon', 24, 'none',
        [k(.12, 'shell_l', x=.3, y=.4, b=.6, w=.6), k(.3, 'shell_mid', x=.8, y=.4, b=1, w=1.4, eye='-'), k(.52, 'shell_r', x=.9, y=.5, b=1.2, w=1.6, eye='-', mark='shh'), k(.76, 'shell_mid', x=.5, y=.4, b=.8, w=.8, eye='>')],
        [(.52, 'pride')], g='rest', act=('wrap', 'shell'), when=['night'], prefer=['curious'], obj=[(.3, dict(glow=.3)), (.52, dict(glow=.1))],
        say=["Moon: look elsewhere.", "Covered. Not a glint. Rent due."])
    done(o)
    return o


def magic_acorn():
    # Same 18 x 15 acorn drawing (59 px, on its point) with sparkle glyphs round it: `*` at the cap's left, `.` and `*` at the shoulders, a `*` inside the shell.
    # They are its light, not parts, so every touch is on the cap, the shell or the point. Its own nature: it glows (`glow` and `puff` draw at the touch).
    P = pm('magic_acorn')
    o = Obj('magic_acorn', 'portable', liftable=True,
            parts=dict(stalk='the short stalk on top', cap='the flat hatched cap', shell='the plain curved shell', tip='the pointed bottom it stands on'),
            fields=dict(aura=(.3, 0, 1), snow=(0, 0, 1)),
            physics=[('aura', 'rate', .0012, 'night'), ('aura', 'rate', -.001, 'day'), ('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm')],
            effects=dict(wipe=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)], melt=[('snow', 'mul', .2)], stoke=[('aura', 'add', .35)], dim=[('aura', 'mul', .3)],
                         mend=[('obj.condition', 'add', .25)], zap=[('obj.condition', 'add', -.15)], smudge=[('obj.dirt', 'add', .15)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], awe=[('need.social', 'add', 1)]),
            anchors=dict(stalk=P(9, 1), cap_top=P(9, 2, 'surface'), cap_l=P(6, 3), cap_r=P(15, 3), shell_l=P(4, 8), shell_r=P(15, 8), shell_mid=P(9, 8),
                         shell_belly=P(9, 10), shell_lowl=P(4, 10), shell_lowr=P(15, 10), tip=P(9, 14), tip_l=P(6, 14), tip_r=P(15, 14)))
    # ---------------- care
    o.r('rub_the_glow_awake', 'Rubbing the cap with a wing until the glow wakes up and brightens', 20, 'wing',
        [k(.1, 'cap_top', reach=.4, x=.4, y=.5, b=.2), k(.26, 'cap_l', reach=1, x=.8, y=.7, b=.5, l=1, mark='fff'), k(.42, 'cap_top', reach=1, x=.7, y=.9, b=.6), k(.58, 'cap_r', reach=1, x=.8, y=.7, b=.5, r=1, mark='fff'), k(.74, 'cap_top', reach=1, x=.5, y=.5, b=.3, eye='O'), k(.9, eye='^')],
        [(.58, 'stoke')], g='care', act=('polish', 'cap'), when=['aura<.5'], obj=[(.26, dict(glow=.3)), (.42, dict(glow=.6)), (.58, dict(glow=1)), (.82, dict(glow=.8))],
        say=["There. Brighter. Do not ask what it is for.", "Glow up. Literally. I worked for that pun."])
    o.r('cup_wings_round_the_glare', 'Cupping both wings round the shell to take the glare down to something bearable', 18, 'none',
        [k(.1, 'shell_l', x=.3, y=.4, b=.4, w=.4), k(.28, 'shell_mid', x=.6, y=.5, b=.7, w=1.2, eye='-'), k(.5, 'shell_mid', x=.7, y=.6, b=.9, w=1.4, eye='-', mark='shh'), k(.72, 'shell_r', x=.4, y=.4, b=.5, w=.6), k(.88, eye='^')],
        [(.5, 'dim')], g='care', act=('wrap', 'shell'), when=['aura>.6'], obj=[(.28, dict(glow=.8)), (.5, dict(glow=.2)), (.72, dict(glow=.1))],
        say=["Dimmed it. Retinas saved.", "Turned the light down. Like a very strange lamp."])
    o.r('scuff_the_grime_off_the_stalk', 'Dragging the stalk and cap rim through his chest feathers to rub the grime off', 16, 'none',
        [k(.1, 'stalk', x=.5, y=.7, b=.3), k(.28, 'stalk', x=.8, y=.9, b=.6, mark='skk'), k(.46, 'cap_l', x=.9, y=.9, b=.7, l=1, mark='skk'), k(.64, 'cap_r', x=.8, y=.9, b=.6, r=1), k(.82, eye='-')],
        [(.46, 'wipe')], g='care', act=('wipe', 'stalk'), when=['obj_dirt>.3'], say=["Clean stalk. I smell of acorn now.", "Rubbed it on my chest. Dignity: negotiable."])
    o.r('shake_the_wet_off_its_shell', 'Patting the beaded wet off the shell with his wing, bead by bead', 18, 'wing',
        [k(.1, 'shell_r', reach=.4, x=.3, y=.5, b=.3), k(.26, 'shell_r', reach=1, x=.6, y=.7, b=.5, mark='pat'), k(.44, 'shell_lowr', reach=1, x=.6, y=.8, b=.6, l=1, mark='pat'), k(.62, 'shell_belly', reach=1, x=.5, y=.7, b=.5, r=1), k(.8, eye='-')],
        [(.44, 'dry')], g='care', act=('dry', 'shell'), when=['obj_wetness>.3'])
    o.r('breathe_the_snow_to_steam', 'Puffing warm breath over the cap until the snow on it melts into steam', 16, 'none',
        [k(.12, 'cap_top', x=.8, y=.9, b=.3), k(.3, 'cap_top', x=1.2, y=1.4, b=.7, mark='haaa'), k(.5, 'cap_l', x=1.3, y=1.4, b=.8, mark='haaa'), k(.7, 'cap_r', x=1.2, y=1.3, b=.7, mark='haaa'), k(.86, eye='^')],
        [(.5, 'melt')], g='care', act=('warm', 'cap'), when=['snow>.3'], obj=[(.3, dict(puff=.4)), (.5, dict(puff=.8, glow=.4))])
    o.r('straighten_the_scorched_stalk', 'Nipping the singed stalk straight again, flinching at every crackle', 18, 'none',
        [k(.1, 'stalk', x=.6, y=.6, b=.2), k(.28, 'stalk', x=1.2, y=1.1, b=.7, mark='zt'), k(.46, x=-.8, y=.2, b=.1, w=.6, eye='>'), k(.62, 'stalk', x=1.3, y=1.2, b=.8, mark='nnk'), k(.8, x=.1, eye='^')],
        [(.62, 'mend')], g='care', act=('straighten', 'stalk'), when=['obj_condition<.7'], obj=[(.28, dict(glow=.5, shake=.2)), (.62, dict(glow=.3))])
    # ---------------- use
    o.r('carry_it_like_a_lantern', 'Carrying the acorn by the stalk through the dark like a lantern, lighting a few steps ahead', 26, 'none',
        [k(.08, 'stalk', x=.8, y=.8, b=.4), k(.2, 'stalk', x=1.3, y=1.1, b=.7, mark='up'), k(.34, 'stalk', x=.6, y=-.2, b=-.3, l=1, eye='O'), k(.48, 'stalk', x=.7, y=-.1, b=-.2, r=1), k(.62, 'stalk', x=.6, y=-.2, b=-.3, l=1),
         k(.76, 'stalk', x=1.2, y=1, b=.7), k(.9, eye='^')],
        [], g='use', act=('carry', 'stalk'), when=['night'], prefer=['curious'],
        obj=[(.2, dict(hold=0)), (.32, dict(hold=1, glow=.6)), (.55, dict(hold=1, glow=1)), (.66, dict(hold=0, ix=4, glow=.8)), (.7, dict(ix=4, glow=.6)), (.78, dict(hold=1, ix=4, glow=.6)), (.88, dict(hold=1, glow=.2)), (.94, dict(hold=0))],
        say=["Lantern duck. Smug, bright, lost.", "Walked it round the yard. The yard did not thank me."])
    o.r('smother_it_in_a_wing', 'Scooping the acorn into his wing and bundling it away in the dirt, glow leaking through', 28, 'none',
        [k(.08, 'cap_l', x=.8, y=1, b=.5, w=.5), k(.22, 'stalk', x=1.2, y=1.1, b=.7), k(.36, 'tip_l', x=.9, y=1.5, b=1.1, l=1, mark='skrt'), k(.5, 'tip_l', x=-.3, y=-.5, b=-.2, w=.5, eye='<'), k(.64, 'tip_r', x=1, y=1.4, b=1.1, r=1, mark='skrt'), k(.72, 'tip_r', x=1.2, y=1.6, b=1.2, l=1, mark='skrt'), k(.8, 'tip_r', x=1.1, y=1.3, b=1, eye='^'), k(.92, eye='-')],
        [(.64, 'smudge')], g='use', act=('hide', 'acorn'), prefer=['curious'],
        obj=[(.22, dict(hold=0)), (.28, dict(hold=1)), (.38, dict(hold=1, hide=1)), (.44, dict(hold=0, hide=1)), (.58, dict(hide=1, glow=.5)), (.68, dict(hide=1)), (.74, dict(hide=0, glow=.7)), (.84, dict(glow=0))],
        say=["Buried. Still glowing through the dirt. Subtle.", "It lit up the hole. Terrible at secrets."])
    o.r('roll_it_and_follow_the_light', 'Rolling the acorn off with the bill and following its glow, then toting it back by the cap', 26, 'none',
        [k(.1, 'shell_r', x=.7, y=.9, b=.4), k(.24, 'shell_r', x=1.3, y=1, b=.8, r=1, mark='rrr'), k(.4, x=1.4, y=.3, b=.2, l=1, eye='O'), k(.56, 'cap_r', x=1.2, y=1, b=.8), k(.72, 'cap_r', x=.3, y=-.2, b=-.2, r=1), k(.88, eye='^')],
        [(.24, 'smudge')], g='use', act=('roll', 'shell'),
        obj=[(.24, dict(ix=0)), (.34, dict(ix=4, glow=.5)), (.5, dict(ix=7, glow=.6)), (.56, dict(ix=7, hold=0)), (.62, dict(ix=7, hold=1)), (.76, dict(ix=0, hold=1, glow=.3)), (.84, dict(hold=0, glow=0))])
    o.r('toss_it_so_the_glow_arcs', 'Tossing the acorn up and catching it in his bill, the glow drawing an arc', 20, 'none',
        [k(.1, 'stalk', x=.7, y=1, b=.5), k(.22, 'stalk', x=1.2, y=1.3, b=.9, l=1), k(.34, x=.7, y=-1.5, b=-1, w=.7, eye='O', mark='whee'), k(.5, x=1, y=-1, b=-.4), k(.62, 'stalk', x=1.4, y=1, b=.6, mark='hap'), k(.8, eye='^')],
        [], g='play', act=('throw', 'acorn'), prefer=['happy'],
        obj=[(.22, dict(hold=1)), (.3, dict(hold=1)), (.38, dict(hold=0, iy=-5, glow=1)), (.5, dict(iy=-5, glow=1)), (.58, dict(hold=1, iy=0, glow=.6)), (.74, dict(hold=0, glow=0))])
    o.r('warm_his_feet_at_the_glow', 'Holding his chilled feet up to the glow in turn and wiggling his toes', 26, 'none',
        [k(.1, 'tip_l', x=.3, y=.8, b=.7), k(.28, 'tip_l', x=.3, y=1.2, b=1.1, l=1, eye='-', mark='ahh'), k(.5, 'tip_r', x=.3, y=1.2, b=1.1, r=1, eye='-'), k(.7, 'tip_r', x=.2, y=1, b=.9, l=1, r=1), k(.86, eye='^')],
        [(.5, 'rest')], g='rest', act=('warm', 'point'), when=['cold', 'night'], obj=[(.28, dict(glow=.5)), (.5, dict(glow=.7))])
    o.r('sing_it_louder', 'Singing a long note at the acorn and watching the glow swell with it', 22, 'none',
        [k(.1, 'cap_top', x=.3, y=-.3, b=-.3, w=.4), k(.26, 'cap_top', x=-.6, y=-1.1, b=-.9, w=.8, mark='laa', eye='^'), k(.46, 'cap_top', x=-.8, y=-1.5, b=-1.2, w=1.1, mark='LAAAA'), k(.66, 'cap_top', x=.6, y=.6, b=.7, eye='O'), k(.84, eye='-')],
        [(.46, 'stoke')], g='use', act=('sing', 'acorn'), when=['aura<.5'], obj=[(.26, dict(glow=.3)), (.46, dict(glow=.9)), (.66, dict(glow=.6))],
        say=["The note went in. The light came out. Acorn Karaoke.", "Apparently it likes my voice. Only one."])
    o.r('rock_it_by_the_cap', 'Rocking the acorn on its point with the bill against the cap to make the light swing', 18, 'none',
        [k(.12, 'cap_l', x=.3, y=1.2, b=1.2, w=.4), k(.3, 'cap_l', x=-.4, y=1.7, b=1.7, l=1, mark='hnn'), k(.48, 'cap_r', x=-.8, y=.4, b=.5, r=1, w=.6), k(.66, 'cap_l', x=-.3, y=1.9, b=1.9, l=1, r=1), k(.84, x=.2, y=-.3, eye='-')],
        [], g='use', act=('rock', 'cap'), obj=[(.3, dict(sway=.5, glow=.3)), (.48, dict(sway=-.6, glow=.5)), (.66, dict(sway=.9, glow=.7)), (.8, dict(sway=0, glow=.2))])
    # ---------------- play
    o.r('chase_the_light_it_throws', 'Hopping about after the little lights it throws off, snapping at the spots', 22, 'none',
        [k(.1, 'cap_l', x=.5, y=.6, b=.3), k(.24, 'shell_l', x=1.3, y=.9, b=.6, l=1, mark='snap'), k(.4, 'shell_lowl', x=1.2, y=1, b=.8, r=1, mark='snap'), k(.56, 'shell_r', x=1.3, y=.9, b=.6, l=1, mark='snap'), k(.72, 'cap_r', x=1.2, y=.8, b=.5, r=1), k(.88, eye='@')],
        [(.4, 'fun')], g='play', act=('chase', 'glow'), prefer=['young', 'happy'], obj=[(.24, dict(glow=.6)), (.4, dict(glow=.9)), (.56, dict(glow=.6)), (.72, dict(glow=.3))])
    o.r('kick_it_and_watch_it_wobble', 'Kicking the acorn over with the flat of his foot and trotting after the light', 20, 'none',
        [k(.1, 'shell_belly', x=.2, y=.7, b=.7, l=1), k(.24, 'shell_belly', x=-.7, y=.3, b=1.1, l=1, mark='pok'), k(.38, x=1.2, y=.1, b=-.4, r=1, w=.5), k(.52, 'stalk', x=1.3, y=1, b=.7), k(.7, 'stalk', x=.3, y=-.3, b=-.2, l=1), k(.86, eye='^')],
        [(.24, 'zap')], g='play', act=('kick', 'belly'), prefer=['grumpy'],
        obj=[(.24, dict(ix=0)), (.32, dict(ix=3, shake=.4, glow=.8)), (.46, dict(ix=5)), (.52, dict(ix=5, hold=1)), (.66, dict(ix=0, hold=1)), (.76, dict(hold=0, glow=0))])
    o.r('hold_it_under_his_chin_to_spook', 'Holding the glowing acorn up under his chin and pulling a spooky face', 20, 'none',
        [k(.1, 'stalk', x=.8, y=1, b=.5), k(.24, 'stalk', x=1.2, y=1.2, b=.8), k(.4, 'stalk', x=.3, y=-.7, b=-.7, w=.5, eye='O', mark='oooOOO'), k(.56, 'stalk', x=.3, y=-.8, b=-.8, w=.9, eye='@', mark='BOO'), k(.74, 'stalk', x=1.1, y=1, b=.6), k(.9, eye='^')],
        [], g='show', act=('show', 'face'), when=['night'], prefer=['happy'],
        obj=[(.24, dict(hold=0)), (.34, dict(hold=1, glow=.6)), (.5, dict(hold=1, iy=-1, glow=1)), (.66, dict(hold=1, glow=.5)), (.78, dict(hold=0, glow=0))], say=["Boo. Nobody was there. It still counts.", "Spooked myself. Very efficient."])
    o.r('juggle_light_between_wings', 'Bouncing the acorn from wing to wing so the glow skips back and forth', 22, 'wing',
        [k(.1, 'shell_mid', reach=.4, x=.3, y=.4, b=.3), k(.24, 'shell_l', reach=1, x=.2, y=-.4, b=-.5, l=1, mark='hup'), k(.4, 'shell_r', reach=1, x=.2, y=-.5, b=-.6, r=1, mark='hup'), k(.56, 'shell_l', reach=1, x=.2, y=-.5, b=-.5, l=1, mark='hup'), k(.72, 'shell_mid', reach=1, x=.3, y=.4, b=.2), k(.88, eye='^')],
        [], g='play', act=('balance', 'wings'), prefer=['happy'],
        obj=[(.24, dict(sway=.4, glow=.4)), (.4, dict(sway=-.4, glow=.7)), (.56, dict(sway=.5, glow=1)), (.72, dict(sway=0, glow=.4)), (.84, dict(glow=0))])
    # ---------------- test
    o.r('listen_for_the_hum', 'Pressing an ear to the cap to catch the hum that comes with the glow', 18, 'none',
        [k(.12, 'cap_l', x=.7, y=.3, b=.3), k(.3, 'cap_l', x=1.2, y=.5, b=.5, eye='-'), k(.52, 'cap_l', x=1.3, y=.6, b=.6, eye='-', mark='mmmm'), k(.7, x=-.4, y=-.3, eye='O'), k(.86, eye='-')],
        [], g='test', act=('listen', 'cap'), obj=[(.3, dict(glow=.3)), (.52, dict(glow=.6)), (.7, dict(glow=.2))], say=["It hums. Low. Off-key. Like my cousin.", "Hum confirmed. Source unknown. Tolerated."])
    o.r('tap_for_a_chime', 'Tapping the shell with the bill and hearing a small chime answer', 14, 'none',
        [k(.12, 'shell_mid', x=.8, y=.9, b=.3), k(.28, 'shell_mid', x=1.3, y=1.4, b=.7, mark='tink'), k(.44, 'shell_lowl', x=1.3, y=1.4, b=.7, mark='tink'), k(.6, x=-.3, y=-.5, eye='O', mark='ding'), k(.78, eye='^')],
        [], g='test', act=('ring', 'shell'), obj=[(.28, dict(glow=.4)), (.44, dict(glow=.7)), (.6, dict(glow=.3))])
    o.r('weigh_the_light_thing', 'Lifting the acorn by the stalk and finding it lighter than the glow suggests', 18, 'none',
        [k(.1, 'stalk', x=.7, y=.9, b=.4), k(.24, 'stalk', x=1.2, y=1.2, b=.7), k(.4, 'stalk', x=.4, y=-1, b=-1, mark='hup'), k(.54, 'stalk', x=.3, y=-1.1, b=-1, eye='O'), k(.7, 'stalk', x=1, y=1, b=.5), k(.86, eye='-')],
        [], g='test', act=('weigh', 'acorn'), obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.5, dict(hold=1, iy=-1)), (.66, dict(hold=1)), (.78, dict(hold=0))], say=["Light as air. Smug as a nut.", "Weighs nothing. Costs my whole attention."])
    o.r('stare_into_the_glow', 'Staring into the glow from a bill-length away until his eyes water', 20, 'none',
        [k(.12, 'shell_mid', x=.6, y=.3, b=.2), k(.28, 'shell_mid', x=1.5, y=.4, b=.4, eye='O'), k(.48, 'shell_mid', x=1.6, y=.4, b=.4, eye='@', mark='...'), k(.66, 'shell_mid', x=-.5, y=-.2, b=.1, w=.5, eye='-', mark='ow'), k(.84, eye='-')],
        [], g='test', act=('peer', 'glow'), obj=[(.28, dict(glow=.5)), (.48, dict(glow=1)), (.66, dict(glow=.4))], say=["Saw a colour. Did not have a name for it.", "Stared. It stared back. Neither blinked. I lost."])
    o.r('smell_the_sparks', 'Sniffing at the cap and sneezing when the sparks tickle', 14, 'none',
        [k(.12, 'cap_r', x=.7, y=.7, b=.3), k(.3, 'cap_r', x=1.2, y=.9, b=.5, mark='snff'), k(.48, 'cap_r', x=1.4, y=1, b=.6, eye='O'), k(.62, x=-1, y=.9, b=.5, w=.5, eye='>', mark='ACHOO'), k(.8, eye='-')],
        [], g='test', act=('sniff', 'cap'), obj=[(.3, dict(puff=.3)), (.62, dict(puff=.8))])
    o.r('count_the_sparkles', 'Counting the sparkles round the acorn with a wing tip and getting a different number each time', 22, 'wing',
        [k(.1, 'cap_l', reach=.4, x=.2, y=.2), k(.24, 'shell_l', reach=1, x=.3, y=.3, b=.2, mark='one'), k(.38, 'cap_r', reach=1, x=.4, y=.2, mark='two'), k(.52, 'shell_r', reach=1, x=.3, y=.3, b=.3, mark='three'), k(.66, 'shell_lowl', reach=1, x=.3, y=.4, b=.4, mark='...six?'), k(.82, eye='@')],
        [], g='test', act=('count', 'sparkles'), obj=[(.24, dict(glow=.3)), (.52, dict(glow=.6)), (.66, dict(glow=.2))])
    # ---------------- rest
    o.r('doze_in_its_glow', 'Dozing against the acorn with the glow rising and falling like breath', 30, 'none',
        [k(.12, 'shell_lowl', x=.4, y=.6, b=.9), k(.3, 'shell_l', x=.5, y=.9, b=1.4, eye='-'), k(.55, 'shell_l', x=.5, y=1.1, b=1.6, eye='-', mark='zzz'), k(.8, 'shell_l', x=.4, y=.9, b=1.4, eye='-', mark='zz')],
        [(.55, 'rest')], g='rest', act=('nap', 'glow'), when=['tired'], obj=[(.3, dict(glow=.3)), (.55, dict(glow=.7)), (.8, dict(glow=.3))])
    o.r('lean_in_the_warm_light', 'Leaning his shoulder on the shell, the glow warm on his feathers', 22, 'none',
        [k(.12, 'shell_lowr', x=-.5, y=.5, b=.8, r=1), k(.3, 'shell_lowr', x=-.8, y=.8, b=1.3, w=.6, eye='-'), k(.55, 'shell_lowr', x=-1, y=1, b=1.7, eye='-', mark='mm'), k(.8, 'shell_lowr', x=-.6, y=.5, b=.9, l=1, eye='-')],
        [], g='rest', act=('lean', 'shell'), prefer=['tired'], obj=[(.3, dict(sway=.2, glow=.3)), (.55, dict(sway=.3, glow=.5))])
    o.r('wait_for_it_to_pulse', 'Sitting square in front of the acorn, waiting for the glow to pulse on the beat', 26, 'none',
        [k(.12, 'shell_belly', x=.2, y=.1, b=.8, eye='-'), k(.34, 'shell_belly', x=.4, y=.9, b=1.6, eye='-', mark='...'), k(.56, 'shell_belly', x=-.5, y=-.7, b=.6, eye='O', mark='now?'), k(.78, 'shell_belly', x=.3, y=.8, b=1.5, eye='>')],
        [], g='rest', act=('wait', 'glow'), prefer=['curious'], obj=[(.34, dict(glow=.2)), (.56, dict(glow=1)), (.78, dict(glow=.2))], say=["Waiting for the pulse. Pulse is on its own schedule.", "Five more minutes of waiting. I am patient for no one else."])
    o.r('sulk_in_its_light', 'Sulking with his back turned to the acorn, the glow still casting his shadow', 24, 'none',
        [k(.14,'shell_lowl',x=-1.4,y=.2,b=.9,r=1), k(.32,'shell_lowl',x=-1.8,y=.6,b=1.4,w=.6,eye='-'), k(.58,'tip_l',x=-1.9,y=.9,b=1.7,eye='-',mark='hmph'), k(.82,'shell_lowl',x=-1.1,y=.3,b=.8,l=1,eye='>')],
        [], g='rest', act=('sulk', 'glow'), prefer=['sad', 'grumpy'])
    # ---------------- weather
    o.r('shield_the_glow_from_the_gust', 'Shielding the glow from the gust with a wing flung out, so it does not blow out', 24, 'none',
        [k(.1, 'shell_l', x=.5, y=.5, b=.5, w=.5), k(.26, 'shell_mid', x=.8, y=.7, b=1, w=1.4, mark='hff'), k(.5, 'shell_mid', x=.9, y=.8, b=1.2, w=1.5, eye='>'), k(.72, 'shell_r', x=.6, y=.5, b=.7, w=.8), k(.88, eye='^')],
        [], g='weather', act=('brace', 'glow'), when=['windy'], obj=[(.26, dict(sway=.5, glow=.5)), (.5, dict(sway=-.6, glow=.8)), (.72, dict(sway=.2, glow=.4))])
    o.r('catch_it_before_it_blows_off', 'Lunging after the acorn as the gust rolls it away, light flickering, and carrying it home', 22, 'none',
        [k(.1, 'shell_lowr', x=.2, y=.5, b=.9, w=.7), k(.24, x=2, y=-.3, b=-.6, l=1, r=1, w=1.1, eye='O'), k(.42, x=1.2, y=1.2, b=.9, l=1), k(.58, 'cap_r', x=1.5, y=1.3, b=1.1, mark='got it'), k(.74, 'cap_r', x=.2, y=-.4, b=-.5, r=1), k(.88, eye='^')],
        [], g='weather', act=('catch', 'shell'), when=['windy'],
        obj=[(.2, dict(ix=0)), (.28, dict(ix=3, shake=.4, glow=.3)), (.42, dict(ix=7, glow=.6)), (.5, dict(ix=7)), (.6, dict(ix=7, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0, glow=0))])
    o.r('read_the_ground_by_its_light', 'Pacing the dark with his bill to the ground in the pool of light, hunting for crumbs', 26, 'none',
        [k(.1, 'tip', x=.6, y=1, b=.7), k(.24, 'tip_l', x=1.3, y=1.5, b=1, l=1, mark='hm'), k(.4, 'shell_lowl', x=1.3, y=1.5, b=1.1, r=1), k(.56, 'shell_lowr', x=1.4, y=1.5, b=1.1, l=1, mark='hm'), k(.72, 'tip_r', x=1.2, y=1.4, b=1, r=1), k(.88, eye='-', mark='none')],
        [], g='weather', act=('seek', 'crumbs'), when=['night', 'aura>.5'], say=["Light is good. Crumbs are absent.", "Searched by acorn light. Found dirt. Rich dirt."])
    # ---------------- show
    o.r('bow_to_the_light', 'Bowing slowly to the glowing acorn, wings out, as the light climbs his back', 18, 'none',
        [k(.12, 'cap_top', x=.2, y=-.4, b=-.4, w=.6), k(.34, 'cap_top', x=1.2, y=1.7, b=1.8, w=1, mark='oh great one'), k(.58, 'cap_top', x=1.4, y=1.9, b=2, w=.8, eye='-'), k(.8, x=.1, y=-.4, b=-.3, eye='^')],
        [(.34, 'awe')], g='show', act=('bow', 'light'), obj=[(.34, dict(glow=.5)), (.58, dict(glow=.9)), (.8, dict(glow=.3))], say=["Bowed. It brightened. Good. Respect works.", "I do not know what it is. I bow anyway."])
    o.r('present_the_glow_to_nobody', 'Sweeping a wing at the glowing acorn like the main act of a very small show', 18, 'wing',
        [k(.1, 'tip_l', reach=.4, x=.6, y=.9, b=.7, w=.3), k(.3, 'shell_lowl', reach=1, x=.2, y=.4, b=.4, mark='ta-daa'), k(.5, 'shell_r', reach=1, x=-.6, y=-.8, b=-.6, l=1), k(.7, 'cap_top', reach=1, x=.2, y=-1.2, b=-.9, r=1), k(.88, eye='^')],
        [(.3, 'awe')], g='show', act=('present', 'glow'), obj=[(.3, dict(glow=.5)), (.5, dict(glow=1)), (.7, dict(glow=.4))], say=["Behold. A nut that lights up. Applause.", "No tickets. No refunds. Just glow."])
    o.r('argue_with_the_light', 'Arguing with the glow, bill to the cap, as it flares up at every point he makes', 22, 'none',
        [k(.1, 'cap_top', x=.5, y=.6, b=.2, w=.6), k(.24, 'cap_top', x=1.6, y=.8, b=.4, mark='no'), k(.38, 'cap_l', x=-.3, y=.6, b=.8, l=1, mark='YES'), k(.52, 'cap_top', x=1.6, y=.8, b=.4, w=1, mark='no'), k(.68, 'cap_r', x=-.4, y=.9, b=1, r=1, eye='>'), k(.84, eye='-')],
        [], g='show', act=('argue', 'cap'), prefer=['grumpy'], obj=[(.24, dict(glow=.5)), (.52, dict(glow=.9)), (.7, dict(glow=.3))])
    o.r('pose_in_the_glow', 'Posing with one wing up and the glow lighting his face from below', 20, 'none',
        [k(.12, 'shell_belly', x=.2, y=.7, b=.8, w=.4), k(.3, 'shell_belly', x=.6, y=-1.3, b=-1, l=1, w=1, eye='^'), k(.55, 'shell_belly', x=.8, y=-1.5, b=-1.2, l=1, w=1.2, eye='^', mark='ta-da'), k(.8, 'shell_belly', x=.1, y=.6, b=.7, eye='^')],
        [], g='show', act=('pose', 'glow'), prefer=['happy'], obj=[(.3, dict(glow=.4)), (.55, dict(glow=.8)), (.8, dict(glow=.3))])
    o.r('dance_in_the_pulse', 'Dancing a quick jig beside the acorn, step for step with its pulse', 20, 'none',
        [k(.1, 'shell_l', x=.2, y=-.4, b=-.6, l=1, w=.6), k(.25, 'shell_lowl', x=.4, y=.4, b=.6, r=1, w=1), k(.4, 'tip_l', x=-.2, y=-.6, b=-1, l=1, w=.9), k(.55, 'shell_lowr', x=.6, y=.5, b=.8, r=1, w=1), k(.7, 'shell_r', x=.3, y=-.7, b=-1, l=1, w=.8), k(.86, x=.3, y=1.1, b=1.2, eye='^')],
        [], g='show', act=('dance', 'glow'), prefer=['happy'], obj=[(.25, dict(glow=.4)), (.4, dict(glow=1)), (.55, dict(glow=.4)), (.7, dict(glow=1)), (.86, dict(glow=.2))])
    o.r('perch_on_its_cap_in_the_light', 'Hopping up onto the flat cap and standing in the full glow, wings out, like a spell', 22, 'none',
        [k(.08, 'cap_top', x=.5, y=.5, b=.4), k(.2, 'cap_top', perch=1, x=-.2, y=-.5, b=-.7, w=.6), k(.4, 'cap_top', perch=1, x=-.4, y=-.8, b=-.9, l=1, w=1.2, eye='O', mark='ooo'), k(.6, 'cap_top', perch=1, x=-.2, y=-1, b=-1.1, r=1, w=1.3, eye='^'), k(.78, 'cap_top', perch=1, x=.1, y=-.6, b=-.7, w=1), k(.9, 'cap_top', x=.3, y=.5, b=.4)],
        [], g='show', act=('perch', 'cap'), ages=GROWN, obj=[(.2, dict(sway=.1, glow=.4)), (.4, dict(sway=-.2, glow=.8)), (.6, dict(sway=.3, glow=1)), (.78, dict(sway=0, glow=.4))], say=["Wizard duck. Power level: acorn.", "Stood in the light. Felt something. Probably hunger."])
    # ---------------- mishap
    o.r('slip_off_the_glassy_shell', 'Skidding a foot off the smooth shell and landing in a heap, the glow flaring', 16, 'none',
        [k(.1, 'shell_lowr', x=.5, y=.6, b=.3, l=1), k(.26, 'shell_lowr', x=1, y=.9, b=.7, l=1, mark='eh'), k(.42, 'tip_r', x=1.5, y=1.7, b=2, l=1, r=1, w=1, eye='O', mark='WHOA'), k(.6, x=1.7, y=2, b=2.2, eye='@'), k(.8, x=.4, y=.8, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'shell'), prefer=['grumpy'], obj=[(.26, dict(shake=.5, glow=.6)), (.42, dict(sway=.6, glow=1)), (.7, dict(glow=.2))], say=["Floor and I had a moment. It won.", "Slipped on a magic nut. Lawsuit pending."])
    o.r('bonk_into_the_bright_spot', 'Looking at the stars and bonking bill-first into the glowing acorn', 14, 'none',
        [k(.12, x=.6, y=-.9, b=-.2, w=.3, eye='o'), k(.28, 'cap_r', x=1.7, y=.4, b=.8, mark='BONK'), k(.44, 'cap_r', x=-1.2, y=-.7, b=-.8, l=1, w=.9, eye='@'), k(.62, x=-.5, y=.8, b=.6, eye='>', mark='ugh'), k(.8, eye='-')],
        [(.28, 'zap')], g='mishap', act=('walk_into', 'acorn'), when=['night'], obj=[(.28, dict(shake=.6, glow=1)), (.44, dict(sway=.4, glow=.5))])
    o.r('get_zapped_by_a_spark', 'Pecking the stalk and getting a small blue spark right in the bill', 16, 'none',
        [k(.14, 'stalk', x=.9, y=.9, b=.4), k(.3, 'stalk', x=1.5, y=1.3, b=.8, mark='pk'), k(.42, 'stalk', x=1.5, y=1.3, b=.8, eye='O', mark='ZAP'), k(.58, x=-1.4, y=-.4, b=-.9, l=1, r=1, w=1, eye='@'), k(.78, x=-.2, y=.5, b=.4, eye='-', mark='ow')],
        [(.42, 'zap')], g='mishap', act=('shake', 'stalk'), obj=[(.3, dict(glow=.6)), (.42, dict(glow=1, shake=.5, puff=.8)), (.6, dict(glow=.3))], say=["Zapped. Bill tingles. Might be a power.", "Acorn bit me. Back. Bit it back. Zapped again."])
    o.r('stuck_to_the_cap_by_a_spark', 'Pressing his bill to the cap and finding it will not come away, until a pop frees it', 22, 'none',
        [k(.12, 'cap_top', x=.6, y=1.2, b=.6), k(.28, 'cap_top', x=1, y=1.8, b=1.3, mark='mm'), k(.44, 'cap_top', x=1.1, y=1.9, b=1.8, l=1, eye='O', mark='MPH'), k(.62, 'cap_top', x=1.2, y=2, b=1.9, r=1, w=.6, mark='POP'), k(.8, x=-1, y=.8, b=.8, eye='@')],
        [], g='mishap', act=('stuck', 'cap'), prefer=['curious'], obj=[(.28, dict(glow=.5)), (.44, dict(shake=.5, glow=1)), (.62, dict(sway=-.5, glow=.6))])
    o.r('stamp_the_sparks_out', 'Stamping at the little sparks that drift off the shoulders, one foot then the other', 18, 'none',
        [k(.12, 'tip_r', x=-.5, y=.2, b=-.5, r=1), k(.28, 'tip_r', x=-.3, y=.4, b=1.6, r=1, w=.5, mark='STOMP'), k(.44, 'tip_l', x=-.5, y=.2, b=-.6, l=1), k(.6, 'tip_l', x=-.3, y=.4, b=1.7, l=1, w=.5, mark='STOMP'), k(.76, x=-.2, y=-.4, eye='>')],
        [], g='mishap', act=('stamp', 'sparks'), prefer=['grumpy'], obj=[(.28, dict(shake=.5, glow=.5)), (.6, dict(shake=.7, glow=.8))])
    # ---------------- more acts that only a glowing acorn allows
    o.r('hook_the_stalk_from_the_dark', 'Hooking the stalk with a twig from a few steps off and reeling the glow in through the dark', 22, 'twig',
        [k(.1, 'stalk', reach=.5, x=.7, y=.2, b=.3), k(.26, 'stalk', reach=1, x=1.5, y=.7, b=.7, l=1, mark='klk'), k(.44, 'stalk', reach=1, x=.1, y=.4, b=1, r=1, mark='hnn'), k(.62, 'stalk', reach=1, x=-.1, y=.3, b=1.1), k(.84, eye='^')],
        [], g='use', act=('hook', 'stalk'), when=['night'], obj=[(.1, dict(ix=3, glow=.5)), (.26, dict(ix=3, glow=.6)), (.44, dict(ix=2, shake=.2, glow=.8)), (.62, dict(ix=0, glow=.7)), (.8, dict(glow=.2))],
        say=["Fished a light out of the dark. Nothing bit.", "Reeled it in. Gentle. Like a very bright trout."])
    o.r('prod_the_cap_for_sparks', 'Prodding the cap with a twig from arm-and-twig distance to see if it throws sparks', 14, 'twig',
        [k(.12, 'cap_top', reach=.5, x=-.3, y=-.3, b=-.3), k(.3, 'cap_l', reach=1, x=.7, y=-.5, b=-.2, mark='poke'), k(.46, 'cap_r', reach=1, x=.5, y=-.4, b=-.4, eye='O'), k(.62, 'cap_top', reach=1, x=-.6, y=-.6, b=-.5, mark='poke', eye='@'), k(.82, eye='-')],
        [], g='test', act=('prod', 'cap'), obj=[(.3, dict(puff=.3, glow=.5)), (.46, dict(puff=.6, glow=.8)), (.62, dict(puff=.9, glow=1))])
    o.r('drum_a_beat_for_the_glow', 'Drumming a beat down the shell with both feet, the glow flickering in time', 18, 'none',
        [k(.1, 'shell_r', x=-.2, y=.4, b=.3, r=1), k(.24, 'shell_lowr', x=-.2, y=.6, b=.9, l=1, mark='dum'), k(.38, 'shell_r', x=-.3, y=.4, b=.4, r=1, mark='dum'), k(.52, 'shell_lowr', x=-.2, y=.6, b=1, l=1, mark='dum'), k(.68, 'tip_r', x=-.3, y=.8, b=1.2, r=1, mark='DUM'), k(.86, eye='^')],
        [(.52, 'fun')], g='play', act=('drum', 'shell'), prefer=['happy'], obj=[(.24, dict(glow=.4)), (.38, dict(glow=.9)), (.52, dict(glow=.4)), (.68, dict(glow=1))])
    o.r('sweep_dust_off_the_point', 'Sweeping the dust off the point with flicks of the wing, the sparks scattering', 14, 'wing',
        [k(.12, 'tip_r', reach=.4, x=.5, y=1, b=.8), k(.32, 'tip', reach=1, x=.8, y=1.3, b=1.1, r=1), k(.52, 'tip_l', reach=1, x=.8, y=1.3, b=1.1, l=1), k(.72, 'tip', reach=1, x=.6, y=1.1, b=.9), k(.88, eye='-')],
        [(.52, 'wipe')], g='care', act=('sweep', 'point'), when=['obj_dirt>.45'], obj=[(.32, dict(puff=.3)), (.52, dict(puff=.5))])
    o.r('hop_over_the_light', 'Hopping over the acorn and back, the glow flaring each time he clears it', 18, 'none',
        [k(.1, 'tip', x=.5, y=.4, b=.6), k(.22, x=.3, y=-.8, b=-1.4, l=1, r=1, w=.7), k(.34, 'tip_l', x=.3, y=.5, b=.9), k(.46, x=.3, y=-.9, b=-1.5, l=1, r=1, w=.9), k(.58, 'tip_r', x=.3, y=.5, b=.9), k(.7, x=.2, y=-1.1, b=-1.7, l=1, r=1, w=1, eye='^'), k(.84, 'tip', x=.4, y=.4, b=.5)],
        [], g='play', act=('hop', 'acorn'), prefer=['happy', 'young'], obj=[(.22, dict(glow=.5)), (.46, dict(glow=.8)), (.7, dict(glow=1)), (.84, dict(glow=.2))])
    o.r('stand_guard_over_the_beacon', 'Standing guard over the glowing acorn with his chest out, scanning the dark for visitors', 26, 'none',
        [k(.1, 'shell_belly', x=.3, y=-.5, b=-.2, w=.5), k(.3, 'shell_belly', x=-.5, y=-.9, b=-.5, w=.7, eye='<'), k(.5, 'shell_belly', x=.7, y=-.8, b=-.4, w=.8, eye='>'), k(.7, 'shell_belly', x=-.5, y=-1, b=-.5, w=.7, eye='<'), k(.88, eye='^')],
        [], g='rest', act=('guard', 'acorn'), when=['night'], obj=[(.3, dict(glow=.5)), (.5, dict(glow=.7)), (.7, dict(glow=.5))], say=["Nothing is stealing the light. Not on my watch.", "Guarding a nut at midnight. Career highlight."])
    o.r('step_back_to_find_where_it_fades', 'Stepping back from the acorn a bill-length at a time to see where the glow stops', 24, 'none',
        [k(.1, 'tip', x=.4, y=.2, b=.2), k(.26, 'shell_mid', x=1, y=.3, b=.3), k(.42, 'cap_l', x=1.6, y=.2, b=.2, mark='here?'), k(.58, 'stalk', x=2, y=.1, b=.1, mark='here?'), k(.74, 'stalk', x=2.2, y=-.2, b=-.1, eye='O', mark='...'), k(.88, eye='^')],
        [], g='test', act=('measure', 'glow'), when=['night'], obj=[(.26, dict(glow=.4)), (.58, dict(glow=.8)), (.74, dict(glow=.3))])
    o.r('hold_a_wing_over_it_in_the_rain', 'Holding a wing out over the acorn to keep the rain off its glow, drip by drip', 26, 'none',
        [k(.1, 'cap_top', x=.3, y=-.2, b=.4, w=.5), k(.28, 'cap_top', x=.1, y=.5, b=1.2, w=1.5, mark='drip'), k(.5, 'cap_top', x=.2, y=.7, b=1.5, w=1.6, eye='>'), k(.72, 'cap_top', x=.1, y=.5, b=1.2, w=1.5, eye='-', mark='drip'), k(.88, eye='^')],
        [], g='weather', act=('shelter', 'acorn'), when=['wet', '!storm'], obj=[(.28, dict(glow=.5)), (.5, dict(glow=.8)), (.72, dict(glow=.6))], say=["Umbrella duty. Acorn gets dry. I do not.", "Rain hisses off the glow. I hold the wing. Fair."])
    done(o)
    return o


def pine_cone():
    # Drawing (18 cols x 21 rows, 4.2 px a row, 84 px tall, upright): a frill of bristles rows 1-2 (80-84 px), the stem row 3 (75 px), then overlapping scales in rows
    # of `(<><><>)` from row 4 (67 px, narrow) widening to row 8-14 (54-25 px, widest), narrowing again to row 17, a bristle tail `\|/` row 18 and `v` row 19 to the foot.
    # A hatchling reaches row 6 and below (63 px); older ducks reach the upper scales; the frill and stem need a bigger duck or a twig.
    P = pm('pine_cone')
    o = Obj('pine_cone', 'portable', liftable=True,
            fields=dict(snow=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('snow', 'rate', .002, 'snow'), ('snow', 'rate', -.002, 'warm'), ('frost', 'rate', .0015, 'cold&!snow'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(wipe=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)], brush=[('snow', 'mul', .2)], scrape=[('frost', 'mul', .2)],
                         mend=[('obj.condition', 'add', .25)], snag=[('obj.condition', 'add', -.15)], grit=[('obj.dirt', 'add', .15)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], mate=[('need.social', 'add', 1)]),
            anchors=dict(frill_l=P(3, 1), frill_r=P(14, 1), stalk=P(9, 3), top_l=P(5, 5), top_r=P(15, 5), mid_l=P(3, 8), mid=P(9, 8), mid_r=P(15, 8),
                         waist_l=P(2, 11), belly=P(9, 12), waist_r=P(16, 11), low_l=P(4, 15), low=P(9, 15), low_r=P(14, 15), base_l=P(6, 18), base_r=P(12, 18), tip=P(9, 20)))
    # ---------------- care
    o.r('wipe_the_flank_clean', 'Wiping the dirt out of the scales along the flank with a wing, row by row', 18, 'wing',
        [k(.1, 'mid_l', reach=.5, x=.3, y=.5, b=.3), k(.26, 'mid_l', reach=1, x=.6, y=.9, b=.5, l=1), k(.42, 'waist_l', reach=1, x=.6, y=1, b=.6), k(.58, 'low_l', reach=1, x=.5, y=1, b=.7, r=1), k(.74, 'low', reach=1, x=.5, y=1, b=.7), k(.9, eye='^')],
        [(.42, 'wipe')], g='care', act=('wipe', 'flank'), when=['obj_dirt>.3'], say=["Scales scrubbed. All of them. Hundreds.", "Clean cone. Prickly as ever. Same personality."])
    o.r('pat_the_wet_from_the_scales', 'Patting the wet out from between the scales with the flat of a wing', 18, 'wing',
        [k(.1, 'top_r', reach=.5, x=.3, y=.4, w=.2), k(.28, 'mid_r', reach=1, x=.5, y=.8, b=.4, l=1, mark='pat'), k(.46, 'waist_r', reach=1, x=.5, y=.9, b=.5, r=1, mark='pat'), k(.64, 'low_r', reach=1, x=.5, y=.9, b=.6, l=1), k(.82, eye='-')],
        [(.46, 'dry')], g='care', act=('dry', 'scales'), when=['obj_wetness>.3'])
    o.r('puff_the_snow_out_of_the_crown', 'Puffing the snow out of the crown scales and the stem with short breaths', 16, 'none',
        [k(.12, 'stalk', x=.9, y=.9, b=.3), k(.3, 'stalk', x=1.3, y=1.5, b=.7, mark='fff'), k(.5, 'top_l', x=1.3, y=1.5, b=.8, mark='fff'), k(.7, 'top_r', x=1.2, y=1.4, b=.7, mark='fff'), k(.86, eye='^')],
        [(.5, 'brush')], g='care', act=('blow', 'stalk'), ages=GROWN, when=['snow>.3'], obj=[(.3, dict(puff=.4)), (.5, dict(puff=.7))])
    o.r('chip_the_frost_between_scales', 'Chipping the frost out between the scales with a twig tip, a row at a time', 20, 'twig',
        [k(.1, 'mid_l', reach=.5, x=.4, y=.4), k(.28, 'mid_l', reach=1, x=.8, y=.7, b=.3, mark='tik'), k(.46, 'mid', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.64, 'mid_r', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.8, eye='-')],
        [(.46, 'scrape')], g='care', act=('scrape', 'scales'), when=['frost>.3'])
    o.r('smooth_the_bristle_frill', 'Nipping the bent bristle frill straight again, one bristle at a time', 20, 'none',
        [k(.1, 'frill_l', x=.6, y=.3, b=.2), k(.26, 'frill_l', x=1.1, y=.9, b=.6, mark='nk'), k(.42, 'stalk', x=1.2, y=1, b=.7, mark='nk'), k(.58, 'frill_r', x=1.2, y=.9, b=.6, l=1, mark='nk'), k(.76, 'frill_r', x=.9, y=.7, b=.4), k(.9, eye='^')],
        [(.42, 'mend')], g='care', act=('straighten', 'frill'), ages=GROWN, when=['obj_condition<.7'], obj=[(.26, dict(shake=.2))])
    o.r('sweep_grit_off_the_tail', 'Sweeping the grit off the bristle tail and foot with small wing flicks', 14, 'wing',
        [k(.12, 'base_l', reach=.5, x=.4, y=.8, b=.6), k(.3, 'tip', reach=1, x=.7, y=1.2, b=1, l=1), k(.5, 'base_r', reach=1, x=.7, y=1.2, b=1, r=1), k(.7, 'tip', reach=1, x=.6, y=1, b=.8), k(.86, eye='-')],
        [(.5, 'wipe')], g='care', act=('sweep', 'tail'), when=['obj_dirt>.45'])
    # ---------------- use
    o.r('carry_it_by_the_stem', 'Gripping the stem and carrying the cone off a few steps, setting it down, and fetching it home', 26, 'none',
        [k(.08, 'stalk', x=.9, y=.7, b=.2), k(.2, 'stalk', x=1.4, y=1.2, b=.7, mark='hup'), k(.36, 'stalk', x=.5, y=-.3, b=-.3, l=1), k(.5, 'stalk', x=.4, y=-.2, b=-.2, r=1), k(.62, 'stalk', x=1.2, y=1, b=.7),
         k(.76, 'stalk', x=1.4, y=1.1, b=.6), k(.9, eye='^')],
        [], g='use', act=('carry', 'stem'), ages=GROWN,
        obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1)), (.58, dict(hold=0, ix=3)), (.66, dict(hold=0, ix=3)), (.74, dict(hold=1, ix=3)), (.82, dict(hold=1)), (.92, dict(hold=0))],
        say=["Prickly. Carried anyway. That is called dedication.", "Walked it over. Walked it back. Pointless. Nice."])
    o.r('roll_it_in_a_wobbly_arc', 'Rolling the cone along the ground with the bill, where it wobbles off in a curve, then fetching it back', 26, 'none',
        [k(.1, 'low_l', x=.8, y=.9, b=.4), k(.24, 'low_l', x=1.4, y=1, b=.8, l=1, mark='rrr'), k(.4, x=1.4, y=.4, b=.3, r=1, eye='O'), k(.56, 'belly', x=1.3, y=1, b=.7), k(.72, 'belly', x=.4, y=-.1, b=-.2, l=1), k(.88, eye='^')],
        [(.24, 'grit')], g='use', act=('roll', 'flank'),
        obj=[(.24, dict(ix=0)), (.32, dict(ix=3, iy=1, shake=.3)), (.46, dict(ix=5, iy=-1)), (.54, dict(ix=5, hold=0)), (.6, dict(ix=5, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0))],
        say=["Cones do not roll straight. Cones have opinions.", "It curved. I followed. We both ended up somewhere."])
    o.r('twirl_it_on_its_foot', 'Flicking the stem round so the cone spins on its foot like a clumsy top', 16, 'none',
        [k(.15, 'stalk', x=1, y=1, b=.4), k(.3, 'stalk', x=1.6, y=1.3, b=.8, l=1, mark='fwip'), k(.5, x=-.2, y=.3, w=.5, eye='O'), k(.7, x=-.4, y=-.2, w=.9, eye='O'), k(.88, eye='^')],
        [], g='use', act=('spin', 'foot'), ages=GROWN, obj=[(.3, dict(shake=.4)), (.45, dict(sway=1)), (.6, dict(sway=-1)), (.75, dict(sway=.4)), (.88, dict(sway=0))])
    o.r('shove_it_over_a_hand', 'Putting a shoulder to the belly of the cone and shoving it along the ground', 20, 'none',
        [k(.1, 'belly', x=.2, y=.5, b=.6), k(.24, 'belly', x=.9, y=.8, b=1.3, l=1, mark='hnng'), k(.4, 'belly', x=1.1, y=.9, b=1.5, r=1, mark='HNNG'), k(.58, 'belly', x=.9, y=.7, b=1, eye='>'), k(.74, 'waist_l', x=1.2, y=1, b=.6, eye='-'), k(.9, eye='^')],
        [(.4, 'grit')], g='use', act=('push', 'belly'), obj=[(.24, dict(ix=0)), (.4, dict(ix=2, shake=.3)), (.58, dict(ix=2)), (.66, dict(ix=2, hold=0)), (.8, dict(ix=0))])
    o.r('drag_it_by_the_foot_bristles', 'Dragging the cone along by its tail bristles, bill clamped, then dragging it back', 24, 'none',
        [k(.1, 'base_l', x=.8, y=1.1, b=.8), k(.24, 'tip', x=1.3, y=1.3, b=1.2, l=1, mark='hnn'), k(.42, 'tip', x=-.4, y=1.2, b=1.3, r=1), k(.6, 'base_r', x=-.5, y=1.2, b=1.3, l=1, mark='hnn'), k(.78, 'base_r', x=.4, y=1, b=1, r=1), k(.9, eye='-')],
        [], g='use', act=('drag', 'tail'), ages=GROWN, obj=[(.24, dict(ix=0)), (.42, dict(ix=-3)), (.5, dict(ix=-3, shake=.2)), (.68, dict(ix=-1)), (.8, dict(ix=0))])
    o.r('stash_it_in_the_leaves', 'Rolling the cone into a hollow, scuffing leaves over it, then digging it out', 28, 'none',
        [k(.08, 'belly', x=.9, y=.9, b=.6), k(.2, 'belly', x=1.2, y=1, b=.8, l=1, mark='rrr'), k(.34, 'tip', x=1, y=1.5, b=1.2, l=1, mark='skrt'), k(.48, 'base_l', x=-.2, y=-.5, b=-.2, w=.5, eye='<'),
         k(.6, 'base_r', x=1, y=1.4, b=1.1, r=1, mark='skrt'), k(.74, 'tip', x=1.2, y=1.6, b=1.3, l=1, mark='skrt'), k(.9, eye='^')],
        [], g='use', act=('hide', 'cone'), prefer=['curious'],
        obj=[(.2, dict(ix=0)), (.3, dict(ix=1)), (.4, dict(ix=1, hide=1)), (.5, dict(ix=1, hide=1)), (.66, dict(ix=1, hide=1)), (.72, dict(ix=1, hide=0)), (.78, dict(ix=0, hide=0))],
        say=["Hid a pinecone. Secret known only to me and every squirrel.", "Under the leaves. Very sneaky. Very prickly."])
    # ---------------- play
    o.r('lob_it_by_the_stem_and_fetch', 'Swinging the cone by the stem and lobbing it off, then waddling after it to fetch it back', 26, 'none',
        [k(.08, 'stalk', x=.9, y=.9, b=.5), k(.2, 'stalk', x=1.4, y=1.3, b=.9, l=1), k(.34, 'stalk', x=-.7, y=-.5, b=-.6, w=.8, mark='HUP'), k(.46, x=1.7, y=-.2, b=-.2, r=1, w=1, eye='>'), k(.62, x=1.4, y=.5, b=.4, l=1, r=1),
         k(.74, 'stalk', x=1.3, y=1, b=.7), k(.88, eye='^')],
        [(.2, 'fun')], g='play', act=('throw', 'stem'), ages=GROWN, prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.3, dict(hold=1)), (.38, dict(hold=1)), (.44, dict(hold=.3, ix=3, iy=-3)), (.5, dict(hold=0, ix=6, iy=0)), (.64, dict(ix=6)), (.72, dict(hold=1, ix=6)), (.8, dict(hold=1, ix=0)), (.88, dict(hold=0))])
    o.r('boot_it_off_the_belly', 'Booting the cone off its belly with one foot, wincing at the prickles, and hobbling after it', 20, 'none',
        [k(.1, 'belly', x=.3, y=.9, b=.6, l=1), k(.24, 'belly', x=-.6, y=.4, b=1, l=1, mark='pok'), k(.34, x=-.8, y=.3, b=.4, r=1, eye='>', mark='ow'), k(.5, x=1.2, y=.2, b=-.3, w=.5), k(.66, 'belly', x=1.3, y=1, b=.7), k(.84, eye='^')],
        [(.24, 'snag')], g='play', act=('kick', 'belly'), prefer=['grumpy'],
        obj=[(.24, dict(ix=0)), (.32, dict(ix=3, shake=.4)), (.46, dict(ix=5)), (.58, dict(ix=5, hold=1)), (.72, dict(ix=0, hold=1)), (.8, dict(hold=0))])
    o.r('hop_over_it_back_and_forth', 'Hopping over the cone and back, three times, each hop a bit higher', 18, 'none',
        [k(.1,'low',x=-.4,y=.8,b=1), k(.2,x=-.9,y=-1,b=-1.8,l=1,r=1,w=1), k(.32,'base_r',x=-.5,y=.9,b=1.2), k(.44,x=-1,y=-1.2,b=-2,l=1,r=1,w=1.1), k(.56,'base_l',x=-.5,y=.9,b=1.2), k(.68,x=-1.1,y=-1.4,b=-2.2,l=1,r=1,w=1.2,eye='^'), k(.84,'low',x=-.3,y=.7,b=.9)],
        [], g='play', act=('hop', 'cone'), prefer=['happy', 'young'])
    o.r('bat_it_between_two_wings', 'Batting the cone left and right along the ground with alternate wing swipes', 18, 'wing',
        [k(.1, 'mid_l', reach=.5, x=.3, y=.5, b=.3), k(.24, 'mid_l', reach=1, x=.6, y=.7, b=.6, l=1, mark='tk'), k(.4, 'mid_r', reach=1, x=-.2, y=.7, b=.6, r=1, mark='tk'), k(.56, 'mid_l', reach=1, x=.6, y=.7, b=.6, l=1, mark='tk'), k(.74, 'mid', reach=1, x=.4, y=.5, b=.4), k(.9, eye='^')],
        [], g='play', act=('knock', 'flank'), obj=[(.24, dict(ix=1)), (.4, dict(ix=-1)), (.56, dict(ix=1)), (.72, dict(ix=0, shake=.2))])
    o.r('toss_and_catch_in_the_bill', 'Tossing the cone up by the stem and snapping at it in the air', 20, 'none',
        [k(.1,'stalk',x=1,y=1.4,b=.9), k(.22,'stalk',x=1.6,y=1.9,b=1.4,l=1,r=1), k(.36,x=.2,y=-1.8,b=-1.4,w=.9,eye='O'), k(.5,x=.4,y=-2,b=-1,w=.7), k(.64,'stalk',x=1.8,y=1.4,b=1.1,mark='hap'), k(.82,eye='^')],
        [], g='play', act=('catch', 'cone'), ages=GROWN, prefer=['happy'],
        obj=[(.24, dict(hold=1)), (.34, dict(hold=1)), (.42, dict(hold=0, iy=-6)), (.52, dict(iy=-6)), (.6, dict(hold=1, iy=0)), (.76, dict(hold=0))])
    o.r('drum_up_the_scales', 'Drumming a rolling beat up the scales with the bill, low to high', 18, 'none',
        [k(.1, 'low', x=.6, y=.8, b=.4), k(.24, 'belly', x=1, y=1, b=.5, mark='tkk'), k(.4, 'mid', x=1, y=1, b=.5, mark='tkk'), k(.56, 'top_r', x=1.1, y=1, b=.5, mark='tkk'), k(.72, 'stalk', x=1.2, y=.9, b=.4, mark='TKK'), k(.88, eye='^')],
        [], g='play', act=('drum', 'scales'), ages=GROWN, obj=[(.24, dict(shake=.2)), (.4, dict(shake=.2)), (.56, dict(shake=.3)), (.72, dict(shake=.4))])
    # ---------------- test
    o.r('sniff_the_woody_scent', 'Sniffing along the scales from foot to crown for the smell of the woods', 16, 'none',
        [k(.12, 'low_l', x=.6, y=.8, b=.5), k(.3, 'waist_l', x=1, y=.8, b=.4, mark='snff'), k(.48, 'mid_l', x=1, y=.7, b=.3, mark='snff'), k(.66, 'top_l', x=1, y=.6, b=.2, mark='SNFF'), k(.82, x=-.3, eye='O')],
        [], g='test', act=('sniff', 'scales'))
    o.r('press_a_cheek_and_regret_it', 'Pressing his cheek to the scales to feel them and yelping', 14, 'none',
        [k(.12, 'waist_r', x=.6, y=.3, b=.3), k(.3, 'waist_r', x=1.2, y=.4, b=.6, eye='-'), k(.44, 'waist_r', x=1.4, y=.4, b=.7, eye='O', mark='YIP'), k(.6, x=-1, y=-.4, b=-.7, w=.9, eye='>'), k(.8, eye='-')],
        [], g='test', act=('press', 'scales'), say=["Pointy. Obviously pointy. I knew that.", "Tested my cheek. Results: ow."])
    o.r('peck_one_scale_loose', 'Pecking one scale to see if it comes off', 12, 'none',
        [k(.14, 'mid_r', x=.8, y=.9, b=.3), k(.28, 'mid_r', x=1.4, y=1.3, b=.7, mark='pk'), k(.42, 'mid_r', x=1.4, y=1.3, b=.7, mark='pk'), k(.58, 'mid_r', x=1.5, y=1.2, b=.8, mark='PK'), k(.8, x=.1, eye='-')],
        [], g='test', act=('peck', 'scale'), obj=[(.28, dict(shake=.2)), (.58, dict(shake=.4))])
    o.r('count_the_rows_of_scales', 'Counting the rows of scales up the cone with the bill, and giving up at the bristles', 22, 'none',
        [k(.1, 'low', x=.5, y=.7, b=.3), k(.24, 'belly', x=1, y=1.1, b=.6, mark='four'), k(.4, 'mid', x=1.3, y=1.4, b=.9, mark='...nine'), k(.56, 'top_l', x=1.4, y=1.6, b=1, mark='twelve?'), k(.72, 'stalk', x=1.2, y=1.2, b=.5, eye='@'), k(.88, eye='-')],
        [], g='test', act=('count', 'rows'), ages=GROWN, say=["Lots. More than lots. Cone is mostly scale.", "Lost count at row nine. Blamed the cone."])
    o.r('taste_a_scale_and_spit', 'Mouthing a scale on the flank for a taste, and spitting woodchips', 14, 'none',
        [k(.14,'mid_l',x=1.4,y=.4,b=1.2), k(.3,'mid_l',x=1.7,y=.6,b=1.5,eye='-',l=1), k(.46,'mid_l',x=1.7,y=.6,b=1.5,eye='>',mark='bleh',r=1), k(.62,x=-1.1,y=.9,b=.2,w=.9,eye='>',mark='ptui'), k(.8,eye='-')],
        [], g='test', act=('taste', 'scale'))
    o.r('hold_his_ear_to_the_belly', 'Putting an ear to the belly of the cone and listening for a rustle', 18, 'none',
        [k(.12,'belly',x=-.2,y=.9,b=.9,l=1), k(.3,'belly',x=.5,y=1.2,b=1.3,eye='-'), k(.52,'belly',x=.6,y=1.3,b=1.4,eye='-',mark='...',r=1), k(.7,x=-.6,y=-.8,b=-.2,eye='O'), k(.86,eye='-')],
        [], g='test', act=('listen', 'belly'), say=["Rustle. Wind. Not the cone. Cone has nothing to say.", "Nothing inside. It is a very tight cone."])
    o.r('prod_the_bristles_with_a_twig', 'Prodding the bristles on the tail with a twig to see if they spring back', 14, 'twig',
        [k(.12, 'base_l', reach=.5, x=.2, y=.2, b=.3), k(.3, 'tip', reach=1, x=.6, y=.5, b=.5, mark='poke'), k(.46, 'base_r', reach=1, x=.4, y=.4, b=.4, eye='O'), k(.7, x=-.5, y=.2, b=.2, eye='-')],
        [], g='test', act=('prod', 'tail'), obj=[(.3, dict(sway=.3)), (.46, dict(sway=-.3))])
    o.r('squeeze_the_cone_between_wings', 'Hugging the cone tight between both wings to see if it gives', 18, 'none',
        [k(.12, 'waist_l', x=.4, y=.3, b=.4, w=.6), k(.3, 'belly', x=.8, y=.4, b=.8, w=1.3), k(.5, 'belly', x=.9, y=.5, b=1, w=1.5, eye='O', mark='SQUEEZE'), k(.7, x=-.8, y=-.3, b=-.6, w=1, eye='>', mark='ow'), k(.86, eye='-')],
        [], g='test', act=('squeeze', 'cone'), obj=[(.3, dict(sway=.2)), (.5, dict(shake=.3))])
    o.r('size_himself_up_against_it', 'Standing back to back with the cone to see which of them is taller', 20, 'none',
        [k(.12,'low_r',x=-.6,y=.9,b=.9), k(.3,'mid_r',x=-1,y=-.9,b=-.8,w=.7), k(.5,'top_r',x=-1.4,y=-1.6,b=-1.4,w=.9,eye='^',mark='taller'), k(.7,'low_r',x=-.6,y=.8,b=.7,eye='-'), k(.86,eye='^')],
        [], g='test', act=('compare', 'height'))
    # ---------------- rest
    o.r('lean_back_first_and_wince', 'Leaning his back against the flank of the cone, wincing at each scale, and settling anyway', 22, 'none',
        [k(.12, 'low_l', x=-.6, y=.4, b=.5), k(.3, 'waist_l', x=-.9, y=.6, b=.9, eye='>', mark='ow'), k(.52, 'waist_l', x=-1, y=.8, b=1.1, eye='-'), k(.78, 'waist_l', x=-.8, y=.6, b=.8, eye='-')],
        [(.52, 'rest')], g='rest', act=('lean', 'flank'), prefer=['tired'], obj=[(.3, dict(sway=.2)), (.52, dict(sway=.3))])
    o.r('nap_curled_at_the_foot', 'Curling up beside the cone with his bill tucked in, asleep with the bristles tickling', 30, 'none',
        [k(.14,'base_l',x=-.3,y=1.2,b=1.2,l=1), k(.32,'tip',x=-.5,y=2,b=2.2,eye='-'), k(.55,'tip',x=-.6,y=2.4,b=2.6,eye='-',mark='zzz'), k(.8,'base_r',x=-.4,y=2,b=2.3,eye='-',mark='zz')],
        [(.55, 'rest')], g='rest', act=('nap', 'foot'), prefer=['tired'], when=['tired'])
    o.r('sit_square_and_wait', 'Sitting square in front of the cone and waiting for it to open up and say something', 26, 'none',
        [k(.12, 'belly', x=.2, y=.3, b=.9, eye='-'), k(.34, 'belly', x=.1, y=.5, b=1.2, eye='-'), k(.56, 'belly', x=-.1, y=.6, b=1.2, eye='>', mark='...'), k(.78, 'belly', x=.2, y=.5, b=1, eye='-')],
        [], g='rest', act=('wait', 'cone'), prefer=['curious'], say=["Still a cone. I give it ten more minutes.", "Not one word. Respect to the cone."])
    o.r('sulk_with_his_back_turned', 'Sulking with his tail to the cone and one wing over his bill', 24, 'none',
        [k(.14,'mid_l',x=-1.4,y=.2,b=.9,r=1), k(.32,'mid_l',x=-1.9,y=.5,b=1.3,w=.7,eye='-'), k(.58,'mid_l',x=-2,y=.7,b=1.5,w=.7,eye='-',mark='hmph'), k(.82,'mid_l',x=-1.2,y=.2,b=.9,l=1,eye='>')],
        [], g='rest', act=('sulk', 'cone'), prefer=['sad', 'grumpy'])
    o.r('stand_guard_chest_out', 'Standing guard at the cone with his chest out, scanning the yard for squirrels', 26, 'none',
        [k(.1, 'belly', x=.3, y=-.4, b=-.2, w=.4), k(.3, 'belly', x=-.4, y=-.7, b=-.5, w=.6, eye='<'), k(.5, 'belly', x=.6, y=-.6, b=-.4, w=.6, eye='>'), k(.7, 'belly', x=-.4, y=-.8, b=-.5, w=.7, eye='<'), k(.88, eye='^')],
        [], g='rest', act=('guard', 'cone'), prefer=['grumpy'], say=["Squirrels, be warned. This cone is mine.", "Guarding a pinecone. I have standards. Low ones."])
    # ---------------- weather
    o.r('warm_up_on_the_sunny_side', 'Pressing his belly to the sun-warmed flank of the cone and soaking it up', 22, 'none',
        [k(.14,'low_r',x=.2,y=1,b=.9,l=1), k(.34,'waist_r',x=.4,y=1.3,b=1.6,w=.6,eye='-'), k(.58,'waist_r',x=.5,y=1.5,b=1.7,w=.8,eye='-',mark='mmm'), k(.82,'low_r',x=.3,y=.9,b=.8,r=1,eye='^')],
        [], g='weather', act=('warm', 'flank'), when=['sun', 'day'])
    o.r('catch_it_as_the_gust_rolls_it', 'Lunging after the cone as the gust rolls it off in a curve, and carrying it home by the stem', 22, 'none',
        [k(.1, 'belly', x=.4, y=.3, b=.2, w=.4), k(.26, x=1.8, y=.1, b=-.3, l=1, r=1, w=.8, eye='O'), k(.44, x=1.4, y=.8, b=.5), k(.58, 'stalk', x=1.3, y=1, b=.7, mark='gotcha'), k(.74, 'stalk', x=.3, y=-.2, b=-.2, l=1), k(.88, eye='^')],
        [], g='weather', act=('catch', 'flank'), ages=GROWN, when=['windy'],
        obj=[(.2, dict(ix=0)), (.28, dict(ix=3, iy=1, shake=.4)), (.42, dict(ix=7, iy=-1)), (.5, dict(ix=7)), (.6, dict(ix=7, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0))])
    o.r('plant_his_feet_against_the_wind', 'Bracing both feet wide at the foot of the cone and hanging on to its bristles while the gust shoves', 24, 'none',
        [k(.1, 'base_l', x=.8, y=.9, b=.6), k(.26, 'base_l', x=1.2, y=1.1, b=1.1, l=1, mark='hff'), k(.5, 'base_r', x=1.4, y=1.2, b=1.3, r=1, eye='>'), k(.72, 'base_r', x=1.1, y=1, b=.9), k(.88, eye='^')],
        [], g='weather', act=('brace', 'tail'), when=['windy'], obj=[(.26, dict(sway=.5)), (.5, dict(sway=-.7, shake=.4)), (.72, dict(sway=.2))])
    o.r('shelter_in_its_lee_from_the_rain', 'Huddling at the cone on the side away from the rain, tail tucked, bill down', 28, 'none',
        [k(.12, 'low_r', x=-.3, y=.5, b=.7), k(.3, 'waist_r', x=-.6, y=.9, b=1.3, w=.3, eye='-'), k(.56, 'waist_r', x=-.7, y=1.1, b=1.5, eye='-', mark='drip'), k(.8, 'low_r', x=-.4, y=.7, b=1, eye='>')],
        [], g='weather', act=('shelter', 'cone'), when=['wet', '!storm'], obj=[(.3, dict(sway=.1))], say=["Shelter: one pinecone. It helps eight percent.", "Rain on one side, scales on the other. Even."])
    # ---------------- show
    o.r('bow_to_the_cone', 'Bowing low to the pinecone as if it were a very short tree', 16, 'none',
        [k(.15,'low',x=.6,y=-.8,b=-.8,w=.8,r=1), k(.35,'low',x=1.8,y=2.4,b=2.6,w=1.2,mark='sire'), k(.6,'low',x=1.9,y=2.6,b=2.8,eye='-'), k(.8,x=.3,y=-.9,b=-.6,l=1,eye='^')],
        [], g='show', act=('bow', 'cone'), say=["Your Evergreenness.", "Bowed to a pinecone. No witnesses. Good."])
    o.r('present_the_cone_to_nobody', 'Sweeping a wing at the cone like a very small forest', 16, 'wing',
        [k(.15,'base_r',reach=.4,x=.6,y=.9,b=.8,w=.3), k(.35,'low_r',reach=1,x=-.3,y=.5,b=.3,mark='behold'), k(.55,'waist_r',reach=1,x=-.6,y=-.3,b=-.5,r=1), k(.75,'mid_r',reach=1,x=-.4,y=-1,b=-.9), k(.9,eye='^')],
        [], g='show', act=('present', 'cone'), say=["Ladies, gentlemen, woodland.", "The forest. Compact edition."])
    o.r('argue_with_the_bristles', 'Arguing with the bristle tail, bill to bill, and losing on points', 20, 'none',
        [k(.1, 'tip', x=.5, y=.7, b=.6, w=.6), k(.24, 'base_l', x=1.6, y=1, b=.9, mark='no'), k(.38, 'base_r', x=-.4, y=.5, b=1.3, l=1, mark='YES'), k(.52, 'tip', x=1.6, y=1, b=.9, w=1, mark='no'), k(.68, 'base_l', x=-.3, y=.9, b=1.4, r=1, eye='>'), k(.84, eye='-')],
        [], g='show', act=('argue', 'tail'), prefer=['grumpy'])
    o.r('stand_like_a_tree_beside_it', 'Standing stock still beside the cone with both wings up, being a tree', 22, 'none',
        [k(.12, 'belly', x=.2, y=.6, b=.6, w=.4), k(.3, 'belly', x=.3, y=-1.3, b=-1.1, w=1.2, eye='^'), k(.55, 'belly', x=.4, y=-1.5, b=-1.3, w=1.4, eye='^', mark='rustle'), k(.8, 'belly', x=.1, y=.6, b=.7, eye='-')],
        [], g='show', act=('pose', 'tree'), prefer=['happy'])
    o.r('dance_round_it_like_a_maypole', 'Dancing a ring round the cone like a tiny maypole', 20, 'none',
        [k(.1,'mid_l',x=.6,y=.3,b=-1.4,l=1,w=1.1), k(.25,'low_l',x=-.5,y=-.2,b=1.2,r=1,w=.4), k(.4,'base_l',x=.7,y=.4,b=-1.6,l=1,w=1.2), k(.55,'low_r',x=-.6,y=-.3,b=1.3,r=1,w=.4), k(.7,'mid_r',x=.8,y=.5,b=-1.5,l=1,w=1.1), k(.86,x=.4,y=1.8,b=1.9,eye='^')],
        [], g='show', act=('dance', 'cone'), prefer=['happy'])
    o.r('sing_to_the_cone', 'Singing to the pinecone with a wing to his chest, pausing for the applause', 24, 'none',
        [k(.1, 'low', x=.3, y=-.3, b=-.3, w=.4), k(.28, 'low', x=-.5, y=-1, b=-.8, w=.7, eye='-', mark='laa'), k(.48, 'belly', x=1.2, y=-1.2, b=-1.2, w=.9, mark='LAAA'), k(.68, 'low', x=.6, y=.8, b=.9, eye='O'), k(.84, eye='-')],
        [(.48, 'mate')], g='show', act=('sing', 'cone'), prefer=['lonely'])
    # ---------------- mishap
    o.r('slip_on_a_scale', 'Planting a foot on the lowest scales, skidding off, and landing flat', 16, 'none',
        [k(.1,'low_l',x=-.3,y=.2,b=.8,r=1), k(.26,'low_l',x=-.9,y=.4,b=1.4,r=1,mark='eh'), k(.42,'base_l',x=-1.6,y=1,b=-1,l=1,r=1,w=1.2,eye='O',mark='WHA'), k(.6,x=-1.9,y=2.3,b=2.6,eye='@'), k(.8,x=-.5,y=1.2,b=1,eye='-')],
        [], g='mishap', act=('slip', 'scale'), prefer=['grumpy'], obj=[(.26, dict(shake=.5)), (.42, dict(sway=.6))])
    o.r('walk_into_it_in_the_dark', 'Bumping bill-first into the cone in the dark and recoiling with a squawk', 14, 'none',
        [k(.15,'low_r',x=1.9,y=1,b=1.2,mark='bonk'), k(.3,'low_r',x=-1.8,y=-1.1,b=-1,l=1,r=1,w=1,eye='@',mark='YOWCH'), k(.5,x=-.8,y=.9,b=.7,eye='>'), k(.76,eye='-')],
        [(.15, 'snag')], g='mishap', act=('walk_into', 'cone'), when=['night'], obj=[(.15, dict(shake=.6)), (.3, dict(sway=.4))])
    o.r('catch_a_foot_between_scales', 'Catching a foot between two scales near the tail and hopping about until it pops free', 22, 'none',
        [k(.12, 'base_r', x=.7, y=.9, b=.6, r=1), k(.28, 'base_r', x=1, y=1.2, b=1.1, r=1, mark='hm'), k(.44, 'base_r', x=1.3, y=1.3, b=1.4, r=1, eye='O', mark='MPH'), k(.62, 'base_r', x=1.5, y=1.2, b=1.2, w=1, mark='POP'), k(.8, x=-1.2, y=.5, b=.3, eye='@')],
        [(.44, 'snag')], g='mishap', act=('stuck', 'tail'), prefer=['curious'], obj=[(.28, dict(sway=.3)), (.44, dict(shake=.6)), (.62, dict(sway=-.5))])
    o.r('stomp_round_it_in_a_huff', 'Stomping round the cone in a temper, kicking up dust at every step', 18, 'none',
        [k(.12, 'base_l', x=.4, y=.6, b=.5, l=1), k(.26, 'base_l', x=.6, y=.8, b=1.2, r=1, mark='STOMP'), k(.4, 'base_r', x=.4, y=.5, b=.4, l=1), k(.54, 'base_r', x=.7, y=.9, b=1.3, r=1, mark='STOMP'), k(.7, x=.3, y=.2, eye='>')],
        [(.54, 'grit')], g='mishap', act=('stamp', 'foot'), prefer=['grumpy'], obj=[(.26, dict(shake=.5)), (.54, dict(shake=.8))])
    # ---------------- three more things a cone allows
    o.r('wobble_it_by_the_stem', 'Waggling the stem side to side with the bill until the cone rocks on its foot bristles', 18, 'none',
        [k(.12, 'stalk', x=.7, y=.8, b=.4), k(.28, 'stalk', x=1.8, y=1, b=.9, mark='hnn'), k(.44, 'stalk', x=.2, y=1, b=.7, r=1), k(.6, 'stalk', x=1.9, y=1.1, b=1, l=1), k(.78, x=.3, y=.2, eye='^')],
        [], g='use', act=('rock', 'foot'), ages=GROWN, obj=[(.28, dict(sway=.6)), (.44, dict(sway=-.7)), (.6, dict(sway=.9)), (.76, dict(sway=0))])
    o.r('hook_it_closer_with_a_twig', 'Hooking the stem with a twig from a few steps off and reeling the cone in', 22, 'twig',
        [k(.1, 'stalk', reach=.5, x=.7, y=.3, b=.3), k(.28, 'stalk', reach=1, x=1.6, y=.8, b=.8, mark='klk'), k(.46, 'stalk', reach=1, x=.1, y=.5, b=1.1, l=1, mark='hnn'), k(.64, 'stalk', reach=1, x=.2, y=.4, b=1.2, r=1), k(.84, eye='^')],
        [], g='use', act=('hook', 'stem'), obj=[(.1, dict(ix=3)), (.28, dict(ix=3)), (.46, dict(ix=2, shake=.2)), (.64, dict(ix=0))], say=["Fished a pinecone out of the yard. Caught nothing else.", "Hooked. Landed. Released. Cone looked unmoved."])
    o.r('whip_the_wet_off_the_cone', 'Gripping the stem and whipping the cone about to fling the wet out of its scales', 20, 'none',
        [k(.1, 'stalk', x=.8, y=.9, b=.4), k(.22, 'stalk', x=1.4, y=1.2, b=.8), k(.38, 'stalk', x=-.6, y=.3, b=.2, l=1, w=.5, mark='fwip'), k(.52, 'stalk', x=1.5, y=.4, b=.3, r=1, w=.5, mark='fwip'), k(.66, 'stalk', x=-.5, y=.3, b=.2, l=1, mark='fwip'), k(.82, 'stalk', x=1, y=1, b=.5)],
        [(.52, 'dry')], g='weather', act=('shake', 'cone'), ages=GROWN, when=['obj_wetness>.3'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1, shake=.7)), (.7, dict(hold=1)), (.8, dict(hold=0))], say=["Wet pinecone. Wetter me.", "Whipped it. Rain went everywhere but away."])
    done(o)
    return o


def snowball():
    # Drawing (44 cols x 33 rows, 3.2 px a row, 81 px tall): a round ball from row 9 (78 px, flat rim `_____`) to row 30 (10 px), sides `(` and `)`, dotted and starred
    # snow texture all over it, a rounded patch `.---.` / `(  +  )` / `'---'` at the middle (rows 17-19, 52-45 px), a small round lump `(o)` low on the right
    # (row 24, 29 px), and the drawing's own `contact` knob at the right edge (row 19, 45 px). Everything at row 14 and below (63 px) is in a hatchling's reach.
    P = pm('snowball')
    o = Obj('snowball', 'portable', liftable=False,
            fields=dict(chill=(.8, 0, 1), crust=(0, 0, 1)),
            physics=[('chill', 'rate', -.003, 'warm'), ('chill', 'rate', .002, 'cold'), ('crust', 'rate', .0015, 'cold&!snow'), ('crust', 'rate', -.002, 'warm')],
            effects=dict(firm=[('chill', 'add', .35)], reshape=[('obj.condition', 'add', .3)], mop=[('obj.wetness', 'add', -.3)], wipe=[('obj.dirt', 'add', -.25)],
                         scrape=[('crust', 'mul', .2)], crack=[('obj.condition', 'add', -.2)], muddy=[('obj.dirt', 'add', .15)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], cool=[('need.cleanliness', 'add', 1)]),
            anchors=dict(crown=P(22, 9), shoulder_l=P(8, 13), shoulder_r=P(36, 13), mid_l=P(6, 17), mid_r=P(40, 17), patch=P(22, 18), center=P(22, 22),
                         low_l=P(8, 23), low_r=P(30, 22), lump=P(38, 24), base_l=P(14, 28), base=P(22, 29), base_r=P(30, 28), foot=P(22, 31)))
    # ---------------- care
    o.r('pat_it_firm_with_both_wings', 'Patting the soft snowball firm all round with both wings, like a baker', 20, 'wing',
        [k(.1, 'low_l', reach=.5, x=.3, y=.6, b=.4), k(.24, 'mid_l', reach=1, x=.5, y=.9, b=.6, l=1, mark='pap'), k(.4, 'shoulder_l', reach=1, x=.5, y=.7, b=.5, r=1, mark='pap'), k(.56, 'shoulder_r', reach=1, x=.5, y=.7, b=.5, l=1, mark='pap'),
         k(.72, 'mid_r', reach=1, x=.5, y=.9, b=.6, r=1, mark='pap'), k(.9, eye='^')],
        [(.56, 'firm')], g='care', act=('pat', 'ball'), when=['chill<.7'], obj=[(.24, dict(shake=.2)), (.56, dict(shake=.3)), (.72, dict(shake=.2))],
        say=["Packed it tight. It is very proud. Cold, but proud.", "Pat pat. Snow behaves for exactly ninety seconds."])
    o.r('shape_the_slumped_side_round', 'Shaping the slumped side back into a round with the flat of a wing', 22, 'wing',
        [k(.1, 'base_l', reach=.5, x=.4, y=.8, b=.6), k(.26, 'low_l', reach=1, x=.6, y=.9, b=.7, l=1), k(.42, 'mid_l', reach=1, x=.7, y=1, b=.8, mark='fsh'), k(.58, 'shoulder_l', reach=1, x=.6, y=.9, b=.6, r=1), k(.74, 'mid_l', reach=1, x=.5, y=.8, b=.5), k(.9, eye='^')],
        [(.58, 'reshape')], g='care', act=('mend', 'side'), when=['obj_condition<.7'], obj=[(.42, dict(sway=.1)), (.58, dict(shake=.2))], say=["Round again. Mostly. Round-ish.", "Reshaped the lump. I am a sculptor now."])
    o.r('scrub_the_grit_off_the_rim', 'Brushing the grit off the flat rim and shoulders with short wing strokes', 18, 'wing',
        [k(.1, 'shoulder_l', reach=.5, x=.3, y=.5), k(.28, 'crown', reach=1, x=.6, y=.8, b=.5, mark='sk'), k(.46, 'shoulder_r', reach=1, x=.6, y=.8, b=.5, l=1, mark='sk'), k(.64, 'crown', reach=1, x=.5, y=.7, b=.4, r=1), k(.82, eye='-')],
        [(.46, 'wipe')], g='care', act=('sweep', 'rim'), ages=GROWN, when=['obj_dirt>.3'])
    o.r('mop_up_the_melt_at_its_foot', 'Mopping the melt-water off the foot of the ball with his breast feathers', 18, 'none',
        [k(.12, 'base_l', x=.4, y=.9, b=.9), k(.3, 'base', x=.6, y=1.1, b=1.2, l=1, mark='shp'), k(.48, 'base_r', x=.6, y=1.1, b=1.2, r=1, mark='shp'), k(.66, 'base', x=.5, y=1, b=1.1), k(.84, eye='-')],
        [(.48, 'mop')], g='care', act=('dry', 'foot'), when=['obj_wetness>.3'], say=["Mopped. Melting is just crying with extra steps.", "Dry foot. Wet duck. Net zero."])
    o.r('chip_the_crust_off_with_a_twig', 'Chipping the hard crust off the shoulders with the tip of a twig', 20, 'twig',
        [k(.1, 'shoulder_l', reach=.5, x=.4, y=.4), k(.26, 'shoulder_l', reach=1, x=.8, y=.7, b=.3, mark='tik'), k(.42, 'crown', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.58, 'shoulder_r', reach=1, x=.9, y=.8, b=.4, mark='tik'), k(.76, eye='-')],
        [(.42, 'scrape')], g='care', act=('chip', 'crust'), when=['crust>.3'])
    o.r('smooth_the_seam_with_his_bill', 'Smoothing the cracked line down the middle with the side of his bill', 18, 'none',
        [k(.12, 'patch', x=.5, y=.6, b=.5), k(.3, 'center', x=.9, y=.8, b=.8, mark='shh'), k(.5, 'low_r', x=1, y=.9, b=.9, l=1), k(.7, 'center', x=.8, y=.7, b=.7), k(.86, eye='^')],
        [(.5, 'reshape')], g='care', act=('straighten', 'seam'), when=['obj_condition<.6'], obj=[(.3, dict(sway=.1))])
    # ---------------- use
    o.r('shove_it_off_and_fetch', 'Shoving the snowball off across the ground with his chest and trotting after it', 24, 'none',
        [k(.1, 'low_l', x=.2, y=.6, b=.8), k(.24, 'mid_l', x=.8, y=.8, b=1.5, l=1, mark='hnnng'), k(.4, 'mid_l', x=1.2, y=.8, b=1.7, r=1, mark='HNNNG'), k(.56, x=1.4, y=.3, b=.3, l=1, r=1), k(.7, 'mid_r', x=.9, y=.9, b=.7, mark='whoa'), k(.86, eye='^')],
        [(.4, 'muddy')], g='use', act=('shove', 'ball'), ages=GROWN,
        obj=[(.24, dict(ix=0)), (.4, dict(ix=3, shake=.2)), (.52, dict(ix=7)), (.64, dict(ix=7)), (.72, dict(ix=0)), (.8, dict(ix=0))],
        say=["Shoved it. It rolled. I followed. A team.", "Snowball: heavy. Me: heavier. Mostly."])
    o.r('roll_it_a_lap_round_the_yard', 'Rolling the snowball in a long loop with his shoulder, steering with the feet', 28, 'none',
        [k(.08, 'shoulder_l', x=.5, y=.6, b=.9), k(.2, 'mid_l', x=1, y=.7, b=1.4, l=1, mark='rrr'), k(.34, 'mid_l', x=1.3, y=.6, b=1.5, r=1), k(.48, 'low_l', x=1.2, y=.7, b=1.3, l=1), k(.62, 'low_r', x=1.2, y=.7, b=1.3, r=1), k(.76, 'mid_r', x=.9, y=.7, b=1, l=1), k(.9, eye='^')],
        [(.34, 'muddy')], g='use', act=('roll', 'ball'), ages=GROWN, obj=[(.2, dict(ix=0)), (.34, dict(ix=2, iy=-1)), (.48, dict(ix=4, iy=0)), (.62, dict(ix=3, iy=1)), (.76, dict(ix=1, iy=0)), (.86, dict(ix=0))])
    o.r('bunt_it_along_the_ground', 'Butting the ball along the ground with his head, small bumps, three at a time', 20, 'none',
        [k(.1, 'low_l', x=.4, y=.8, b=.6), k(.22, 'mid_l', x=1.5, y=1.2, b=1, mark='bmp'), k(.36, 'mid_l', x=1.5, y=1.2, b=1, l=1, mark='bmp'), k(.5, 'mid_l', x=1.6, y=1.2, b=1.1, r=1, mark='BMP'), k(.7, 'mid_r', x=.6, y=.5, b=.4), k(.86, eye='^')],
        [], g='use', act=('nudge', 'ball'), obj=[(.22, dict(ix=1)), (.36, dict(ix=2)), (.5, dict(ix=3)), (.62, dict(ix=3)), (.7, dict(ix=1)), (.78, dict(ix=0)) ])
    o.r('kick_it_hard_and_regret_it', 'Kicking the snowball as hard as he can and finding it is mostly ice', 18, 'none',
        [k(.1, 'base_l', x=.2, y=.6, b=.5, l=1), k(.24, 'base_l', x=-.7, y=.5, b=1, l=1, mark='KICK'), k(.36, x=-1.4, y=.2, b=-.3, r=1, eye='O', mark='YOW'), k(.52, x=-.6, y=.8, b=.8, eye='>'), k(.8, eye='-')],
        [(.24, 'crack')], g='play', act=('kick', 'base'), prefer=['grumpy'], obj=[(.24, dict(shake=.4)), (.4, dict(sway=.3))], say=["Ice. It was mostly ice. Toe disagrees with me.", "Kicked a snowball. Snowball: unmoved. Toe: furious."])
    o.r('dig_a_toe_into_the_lump', 'Working the small round lump near the foot with his bill to see if it will pop out', 20, 'none',
        [k(.12, 'lump', x=.7, y=.9, b=.8), k(.3, 'lump', x=1.2, y=1.3, b=1.1, mark='dg'), k(.48, 'lump', x=1.3, y=1.4, b=1.2, l=1, mark='dg'), k(.64, 'lump', x=1.4, y=1.3, b=1.1, r=1, mark='DG'), k(.82, x=-.2, eye='-')],
        [], g='test', act=('dig', 'lump'), obj=[(.3, dict(shake=.2)), (.64, dict(shake=.3))], say=["It does not come out. It is a lump with plans.", "Dug at it. Lump holds."])
    # ---------------- play
    o.r('race_it_down_the_yard', 'Giving the snowball a push and racing it, nose to nose, to the far side and back', 24, 'none',
        [k(.08, 'low_l', x=.4, y=.8, b=.9), k(.2, 'mid_l', x=1, y=.8, b=1.3, l=1, mark='GO'), k(.34, x=1.7, y=.2, b=-.5, l=1, r=1, w=.8), k(.5, x=1.8, y=.1, b=-.6, l=1, r=1, w=.9, eye='>'), k(.66, 'mid_r', x=1.3, y=.8, b=.9, mark='huff'), k(.82, eye='^')],
        [(.2, 'fun')], g='play', act=('race', 'ball'), ages=GROWN, prefer=['young'],
        obj=[(.2, dict(ix=0)), (.3, dict(ix=3)), (.44, dict(ix=7)), (.56, dict(ix=7)), (.66, dict(ix=3)), (.74, dict(ix=0))], say=["Lost to a snowball. It cheated: no legs.", "Race. Rematch. Rematch. Rematch."])
    o.r('hop_up_and_bounce_off_its_side', 'Taking a run-up and bouncing off the side of the ball with both feet, flop-landing', 20, 'none',
        [k(.1, x=-.4, y=.4, b=.5, w=.3), k(.24, x=1.3, y=-.5, b=-.8, l=1, r=1, w=.7), k(.38, 'mid_l', x=1.9, y=.8, b=-1.4, l=1, r=1, w=1.1, mark='BOING'), k(.54, x=-1.3, y=1, b=2, w=.9, eye='@'), k(.72, x=.3, y=.6, b=.6, eye='-')],
        [], g='play', act=('hop', 'side'), prefer=['happy', 'young'], obj=[(.38, dict(shake=.5)), (.54, dict(sway=.4)), (.7, dict(sway=0))])
    o.r('headbutt_it_a_few_hands', 'Heading the snowball a few hands along the ground, one thud at a time, and giving it a bow', 22, 'none',
        [k(.1, 'shoulder_l', x=.5, y=.9, b=.9), k(.22, 'shoulder_l', x=1.7, y=1.5, b=1.2, mark='thud'), k(.34, 'shoulder_l', x=1.7, y=1.5, b=1.2, l=1, mark='thud'), k(.48, 'shoulder_l', x=1.8, y=1.6, b=1.3, r=1, mark='THUD'), k(.66, 'shoulder_l', x=.8, y=2, b=2, eye='-')],
        [], g='play', act=('knock', 'shoulder'), ages=GROWN, obj=[(.22, dict(ix=1, shake=.2)), (.34, dict(ix=2, shake=.2)), (.48, dict(ix=3, shake=.4)), (.62, dict(ix=3)), (.72, dict(ix=0))])
    o.r('chase_it_down_the_slope', 'Giving it a push and chasing it round in a circle, always a step too late', 26, 'none',
        [k(.08, 'mid_r', x=.6, y=.7, b=.9), k(.18, 'mid_r', x=1.1, y=.8, b=1.3, r=1, mark='hup'), k(.32, x=1.6, y=.3, b=-.3, l=1, r=1, w=.8, eye='O'), k(.5, x=1.5, y=.4, b=.1, r=1, l=1, w=.7), k(.68, 'mid_l', x=1.2, y=.8, b=.9, mark='ha'), k(.84, eye='^')],
        [], g='play', act=('chase', 'ball'), obj=[(.18, dict(ix=0)), (.26, dict(ix=-2, iy=1)), (.4, dict(ix=-5, iy=0)), (.54, dict(ix=-4, iy=-1)), (.66, dict(ix=-1, iy=0)), (.74, dict(ix=0))])
    o.r('dance_a_ring_round_the_ball', 'Dancing a stomping ring round the snowball, kicking up flakes', 20, 'none',
        [k(.1, 'base_l', x=.3, y=-.3, b=-.8, l=1, w=.5), k(.24, 'low_l', x=.6, y=.5, b=.8, r=1, w=1.2), k(.4, 'mid_l', x=-.3, y=-.6, b=-1.2, l=1, w=1), k(.56, 'mid_r', x=.7, y=.4, b=.9, r=1, w=1.2), k(.72, 'base_r', x=.4, y=-.5, b=-1, l=1, w=.9), k(.88, x=.2, y=1.6, b=1.5, eye='^')],
        [], g='show', act=('dance', 'ball'), prefer=['happy'], obj=[(.4, dict(shake=.2)), (.56, dict(shake=.2))])
    # ---------------- test
    o.r('lick_it_to_see_what_cold_is', 'Licking the ball with the tip of his bill and freezing mid-lick', 14, 'none',
        [k(.12, 'mid_l', x=.9, y=.9, b=1), k(.3, 'mid_l', x=1.5, y=1, b=1.1, eye='-'), k(.46, 'mid_l', x=1.6, y=1, b=1.1, eye='O', mark='ow'), k(.62, x=-.9, y=.3, w=.7, eye='>', mark='cold'), k(.8, eye='-')],
        [], g='test', act=('taste', 'side'), say=["Cold. Wet. Like a bad idea.", "Tastes like snow. Tastes like regret. Same thing."])
    o.r('touch_it_with_one_foot', 'Dabbing the ball with one foot, then the other, to find out how cold it is', 16, 'none',
        [k(.12, 'base_l', x=.2, y=.3, b=.2, l=1), k(.26, 'base_l', x=.3, y=.4, b=.5, l=1, mark='eep'), k(.44, 'base_r', x=.3, y=.4, b=.5, r=1, mark='eep'), k(.62, x=-.3, y=.2, b=.1, l=1, r=1, eye='O'), k(.8, eye='-')],
        [], g='test', act=('test', 'ball'))
    o.r('listen_to_it_crunch', 'Pressing an ear to the ball and squeezing it to listen to the crunch', 18, 'none',
        [k(.12, 'shoulder_r', x=.5, y=.3, b=.4), k(.3, 'shoulder_r', x=1, y=.4, b=.7, eye='-'), k(.5, 'shoulder_r', x=1.1, y=.5, b=.8, w=.6, eye='-', mark='crnch'), k(.68, x=-.3, y=-.3, eye='O'), k(.84, eye='-')],
        [], g='test', act=('listen', 'ball'))
    o.r('count_the_flecks_and_give_up', 'Counting the flecks across the snow with the bill, and losing track in the stars', 22, 'none',
        [k(.1, 'low_l', x=.5, y=.5, b=.3), k(.24, 'mid_l', x=1, y=.8, b=.6, mark='one'), k(.4, 'center', x=1.1, y=.9, b=.6, mark='...twelve'), k(.56, 'mid_r', x=1.2, y=.9, b=.6, mark='nine?'), k(.72, 'shoulder_r', x=1.2, y=1, b=.6, eye='@'), k(.88, eye='-')],
        [], g='test', act=('count', 'flecks'), ages=GROWN)
    o.r('peer_at_the_round_patch', 'Peering at the round patch in the middle, tapping it with the bill, and cocking his head', 18, 'none',
        [k(.12, 'patch', x=.7, y=.3, b=.3), k(.28, 'patch', x=1.4, y=.4, b=.5, eye='O'), k(.44, 'patch', x=1.5, y=.6, b=.5, mark='tk'), k(.6, 'patch', x=1.5, y=.6, b=.5, mark='tk'), k(.78, x=-.3, y=.3, eye='O', mark='hm')],
        [], g='show', act=('peer', 'patch'), obj=[(.44, dict(shake=.1)), (.6, dict(shake=.1))], say=["No idea what the patch is. I respect that.", "It is a patch. It does not volunteer more."])
    o.r('weigh_up_the_ball_against_himself', 'Standing shoulder to shoulder with the snowball to see who is bigger', 20, 'none',
        [k(.12, 'mid_r', x=-.5, y=.5, b=.5), k(.3, 'mid_r', x=-.8, y=-.4, b=-.3, w=.5), k(.5, 'shoulder_r', x=-.9, y=-1, b=-.6, w=.6, eye='^', mark='bigger'), k(.7, 'mid_r', x=-.4, y=.4, b=.3, eye='-'), k(.86, eye='^')],
        [], g='test', act=('compare', 'size'), say=["Same size. I am better looking.", "We are even. Do not tell the ball."])
    # ---------------- rest
    o.r('lean_back_on_the_cold_side', 'Leaning his back on the ball and cooling off, slowly sliding down', 22, 'none',
        [k(.12, 'mid_r', x=-.7, y=.3, b=.5), k(.3, 'mid_r', x=-1, y=.6, b=1, eye='-'), k(.5, 'low_r', x=-1.1, y=.9, b=1.4, eye='-', mark='ahh'), k(.76, 'low_r', x=-.9, y=.7, b=1.1, eye='^')],
        [(.5, 'cool')], g='rest', act=('lean', 'side'), obj=[(.3, dict(sway=.1))])
    o.r('curl_up_in_its_lee', 'Curling up at the foot of the ball with his bill tucked in, dozing as the flakes settle', 30, 'none',
        [k(.14, 'base_r', x=-.3, y=.9, b=1.1), k(.32, 'foot', x=-.5, y=1.9, b=2, eye='-'), k(.55, 'foot', x=-.6, y=2.3, b=2.4, eye='-', mark='zzz'), k(.8, 'base_l', x=-.4, y=2, b=2.2, eye='-', mark='zz')],
        [(.55, 'rest')], g='rest', act=('nap', 'foot'), when=['tired'])
    o.r('sit_by_it_and_wait_for_it_to_melt', 'Sitting beside the ball and waiting for it to melt, glaring at the sun', 28, 'none',
        [k(.12, 'low_r', x=.1, y=.4, b=1.1, eye='-'), k(.34, 'low_r', x=0, y=.7, b=1.4, eye='-'), k(.56, 'low_r', x=.2, y=-.7, b=.5, eye='>', mark='...'), k(.78, 'low_r', x=.1, y=.6, b=1.3, eye='-')],
        [], g='rest', act=('wait', 'ball'), prefer=['curious'], say=["Watched it all afternoon. It lost, like me.", "Waiting for it to melt. It waits for me to leave."])
    o.r('turn_his_tail_on_it_and_sulk', 'Sulking with his tail pressed to the ball and a wing over his bill', 24, 'none',
        [k(.14, 'mid_l', x=-1.1, y=.4, b=.8, r=1), k(.32, 'mid_l', x=-1.7, y=.9, b=1.3, w=.6, eye='-'), k(.58, 'mid_l', x=-1.8, y=1, b=1.4, w=.6, eye='-', mark='hmph'), k(.82, 'mid_l', x=-1.2, y=.4, b=.8, l=1, eye='>')],
        [], g='rest', act=('sulk', 'ball'), prefer=['sad', 'grumpy'])
    o.r('stand_guard_against_the_sun', 'Standing guard at the ball with his wings out wide to throw a little shade on it', 26, 'none',
        [k(.1, 'shoulder_l', x=.3, y=-.5, b=-.3, w=.6), k(.3, 'mid_l', x=-.3, y=-.9, b=-.6, w=1.4, eye='<'), k(.5, 'center', x=.5, y=-.8, b=-.5, w=1.5, eye='>'), k(.7, 'mid_r', x=-.3, y=-.9, b=-.6, w=1.4, eye='<'), k(.88, eye='^')],
        [], g='rest', act=('guard', 'ball'), when=['sun', 'warm'], say=["Shade duty. Sun, you shall not pass.", "It is melting. I am the umbrella. Nobody asked."])
    # ---------------- weather
    o.r('watch_it_drip_in_the_warm', 'Watching the melt run off the foot of the ball and shaking his head', 22, 'none',
        [k(.12, 'base', x=.3, y=.9, b=1), k(.3, 'base', x=.5, y=1.3, b=1.3, eye='O', mark='drip'), k(.5, 'base_r', x=.5, y=1.4, b=1.4, eye='-', mark='drip'), k(.7, 'base_l', x=.3, y=1.1, b=1.2, eye='>', mark='drip'), k(.86, eye='-')],
        [], g='weather', act=('peer', 'drip'), when=['warm', 'chill<.6'], say=["Drip. Drip. That is a goodbye.", "Dying slowly. Dramatic little ball."])
    o.r('press_his_belly_to_the_cold', 'Pressing his belly flat to the cold side of the ball to cool off', 20, 'none',
        [k(.12, 'low_l', x=.5, y=.5, b=.9), k(.3, 'mid_l', x=.8, y=.7, b=1.5, w=.5, eye='-'), k(.52, 'mid_l', x=.9, y=.8, b=1.7, w=.7, eye='-', mark='ahhh'), k(.76, 'low_l', x=.6, y=.5, b=.9, eye='^')],
        [(.52, 'cool')], g='weather', act=('cool', 'belly'), when=['warm', 'day'])
    o.r('shield_it_from_the_gust_with_wings', 'Spreading both wings round the ball to keep the gust from scouring its flakes', 24, 'none',
        [k(.1, 'shoulder_l', x=.4, y=.4, b=.5, w=.6), k(.26, 'mid_l', x=.6, y=.5, b=1, w=1.4, mark='hff'), k(.5, 'center', x=.7, y=.6, b=1.2, w=1.6, eye='>'), k(.72, 'mid_r', x=.5, y=.5, b=.8, w=1.2), k(.88, eye='^')],
        [], g='weather', act=('brace', 'ball'), when=['windy'], obj=[(.26, dict(sway=.3)), (.5, dict(sway=-.4, shake=.3)), (.72, dict(sway=.1))])
    o.r('lunge_to_stop_it_rolling_off', 'Lunging to stop the snowball as the gust sends it rolling, and rolling it back by the shoulder', 22, 'none',
        [k(.1, 'mid_r', x=.4, y=.3, b=.4, w=.4), k(.24, x=1.9, y=.1, b=-.4, l=1, r=1, w=.9, eye='O'), k(.42, 'mid_l', x=1.5, y=.8, b=1.1), k(.58, 'low_l', x=1.2, y=.8, b=1.4, mark='hnn'), k(.76, 'mid_l', x=.6, y=.5, b=.5), k(.9, eye='^')],
        [], g='weather', act=('catch', 'ball'), ages=GROWN, when=['windy'],
        obj=[(.18, dict(ix=0)), (.26, dict(ix=3, shake=.3)), (.38, dict(ix=8)), (.46, dict(ix=8)), (.58, dict(ix=6)), (.72, dict(ix=1)), (.82, dict(ix=0))])
    o.r('brush_the_fresh_snow_off_the_top', 'Brushing the fresh flakes off the flat rim with a wing, then looking at the clean top', 16, 'wing',
        [k(.12, 'shoulder_r', reach=.5, x=.3, y=.3), k(.3, 'crown', reach=1, x=.5, y=.7, b=.4, mark='shh'), k(.5, 'shoulder_l', reach=1, x=.5, y=.7, b=.4, l=1, mark='shh'), k(.7, eye='^')],
        [(.5, 'wipe')], g='care', act=('fluff', 'rim'), ages=GROWN, when=['obj_dirt>.2'])
    # ---------------- show
    o.r('bow_to_the_snowball', 'Bowing low to the snowball with a flourish, wings sweeping the snow', 16, 'none',
        [k(.14, 'base', x=.8, y=-.7, b=-.7, w=.9, r=1), k(.34, 'base', x=1.9, y=2.5, b=2.7, w=1.3, mark='your coldness'), k(.6, 'base', x=2, y=2.7, b=2.9, eye='-'), k(.8, x=.4, y=-.8, b=-.5, l=1, eye='^')],
        [], g='show', act=('bow', 'ball'), say=["Your Frostiness.", "Bowed. It did not melt with joy. Rude."])
    o.r('present_the_ball_to_the_yard', 'Sweeping a wing at the snowball like a very round exhibit', 18, 'wing',
        [k(.12, 'base_r', reach=.4, x=.5, y=.8, b=.7, w=.3), k(.32, 'low_r', reach=1, x=-.2, y=.4, b=.2, mark='behold'), k(.52, 'mid_r', reach=1, x=-.5, y=-.4, b=-.4, r=1), k(.72, 'shoulder_r', reach=1, x=-.3, y=-.9, b=-.8), k(.88, eye='^')],
        [], g='show', act=('present', 'ball'), say=["Behold: a spherical event.", "Ladies, gentlemen, orb."])
    o.r('argue_with_the_patch', 'Arguing with the round patch, bill to patch, and losing the debate', 20, 'none',
        [k(.1, 'patch', x=.4, y=.5, b=.5, w=.6), k(.24, 'patch', x=1.7, y=.7, b=.7, mark='no'), k(.38, 'low_l', x=-.5, y=.5, b=1.4, l=1, mark='YES'), k(.52, 'patch', x=1.7, y=.7, b=.7, w=1, mark='no'), k(.68, 'mid_r', x=-.4, y=.8, b=1.5, r=1, eye='>'), k(.84, eye='-')],
        [], g='show', act=('argue', 'patch'), prefer=['grumpy'])
    o.r('pose_like_a_snow_sculptor', 'Posing beside the ball with a wing on his hip like a sculptor admiring his work', 22, 'none',
        [k(.12, 'low_r', x=-.2, y=.8, b=.9, w=.3), k(.3, 'mid_r', x=-.6, y=-1.2, b=-1.1, l=1, w=.8, eye='^'), k(.55, 'mid_r', x=-.8, y=-1.4, b=-1.3, l=1, w=1, eye='^', mark='behold'), k(.8, 'low_r', x=-.2, y=.7, b=.8, eye='-')],
        [], g='show', act=('pose', 'sculptor'), prefer=['happy'])
    o.r('sing_a_carol_to_the_snowball', 'Singing a carol at the snowball with a wing to his chest and flakes in his bill', 26, 'none',
        [k(.1, 'center', x=.3, y=-.3, b=-.3, w=.4), k(.28, 'center', x=-.5, y=-1.1, b=-.9, w=.8, eye='-', mark='laa'), k(.48, 'patch', x=1.3, y=-1.3, b=-1.3, w=1, mark='LAAA'), k(.68, 'center', x=.6, y=.8, b=.9, eye='O'), k(.84, eye='-')],
        [], g='show', act=('sing', 'ball'), prefer=['lonely'])
    # ---------------- mishap
    o.r('skate_off_the_icy_edge', 'Putting a foot on the icy rim at the foot, skating off it, and landing on his back', 16, 'none',
        [k(.1, 'base_l', x=-.2, y=.3, b=.8, r=1), k(.26, 'base_l', x=-.7, y=.5, b=1.3, r=1, mark='eh'), k(.42, 'foot', x=-1.5, y=1.2, b=-1, l=1, r=1, w=1.2, eye='O', mark='WHA'), k(.6, x=-1.9, y=2.2, b=2.7, eye='@'), k(.8, x=-.5, y=1, b=.9, eye='-')],
        [], g='mishap', act=('slip', 'edge'), prefer=['grumpy'], obj=[(.26, dict(shake=.3)), (.42, dict(sway=.4))], say=["Ice. Ice everywhere. Ice was the plan.", "Flat on my back. Snowball watched. Smug."])
    o.r('freeze_his_bill_to_it', 'Pressing his bill to the ball to taste a flake and freezing fast to it, tugging until it unsticks', 22, 'none',
        [k(.12, 'mid_l', x=1, y=.8, b=.6), k(.28, 'mid_l', x=1.6, y=1, b=1.1, mark='mm'), k(.44, 'mid_l', x=1.7, y=1.1, b=1.5, l=1, r=1, eye='O', mark='MPH'), k(.62, 'mid_l', x=1.8, y=1.1, b=1.6, w=1, mark='SPLOP'), k(.8, x=-1.5, y=.5, b=.4, eye='@')],
        [(.62, 'crack')], g='mishap', act=('stuck', 'bill'), prefer=['curious'], obj=[(.28, dict(sway=.2)), (.44, dict(shake=.5)), (.62, dict(sway=-.4))])
    o.r('walk_into_it_after_dark', 'Bumping into the pale bulk of the snowball in the dark and sitting down hard', 14, 'none',
        [k(.15, 'mid_r', x=1.8, y=.8, b=1.2, mark='bonk'), k(.3, 'mid_r', x=-1.6, y=-.9, b=-.8, l=1, r=1, w=1, eye='@'), k(.5, x=-.7, y=1.4, b=2, eye='>', mark='ugh'), k(.76, eye='-')],
        [(.15, 'crack')], g='mishap', act=('walk_into', 'ball'), when=['night'], obj=[(.15, dict(shake=.5)), (.3, dict(sway=.3))])
    o.r('stamp_a_hole_in_the_snow', 'Stamping both feet round the foot of the ball in a temper, churning up slush', 18, 'none',
        [k(.12, 'base_l', x=.3, y=.4, b=.4, l=1), k(.26, 'base_l', x=.5, y=.6, b=1.4, r=1, mark='STOMP'), k(.4, 'base_r', x=.3, y=.4, b=.4, l=1), k(.54, 'base_r', x=.5, y=.6, b=1.5, r=1, mark='STOMP'), k(.7, x=.2, y=.3, eye='>')],
        [(.54, 'muddy')], g='mishap', act=('stamp', 'foot'), prefer=['grumpy'], obj=[(.26, dict(shake=.3)), (.54, dict(shake=.5))])
    # ---------------- more acts
    o.r('press_the_patch_to_hear_a_click', 'Pressing the round patch in with the bill to hear whether it clicks', 16, 'none',
        [k(.12, 'patch', x=.7, y=.5, b=.4), k(.3, 'patch', x=1.5, y=.8, b=.8, mark='pshh'), k(.48, 'patch', x=1.7, y=.9, b=.9, l=1, eye='-'), k(.66, 'patch', x=.3, y=.2, b=.1, eye='O', mark='...'), k(.82, eye='-')],
        [], g='use', act=('press', 'patch'), obj=[(.3, dict(shake=.1)), (.48, dict(shake=.2))], say=["No click. It just takes it.", "Pressed the patch. Patch absorbed the insult."])
    o.r('rap_the_crown_with_a_twig', 'Rapping the flat rim with a twig, three raps, listening for an echo', 14, 'twig',
        [k(.12, 'crown', reach=.5, x=.3, y=-.2, b=-.1), k(.3, 'crown', reach=1, x=.8, y=-.4, b=-.3, mark='tok'), k(.46, 'shoulder_r', reach=1, x=.6, y=-.4, b=-.4, mark='tok'), k(.62, 'crown', reach=1, x=.9, y=-.5, b=-.5, mark='TOK'), k(.8, eye='O')],
        [], g='test', act=('tap', 'rim'), ages=GROWN, obj=[(.3, dict(shake=.1)), (.62, dict(shake=.2))])
    o.r('prod_the_lump_with_a_twig', 'Prodding the little round lump with a twig tip to see if it moves', 14, 'twig',
        [k(.12, 'lump', reach=.5, x=.2, y=.2, b=.3), k(.3, 'lump', reach=1, x=.6, y=.5, b=.5, mark='poke'), k(.48, 'lump', reach=1, x=.5, y=.5, b=.5, eye='O', mark='poke'), k(.7, x=-.4, y=.1, b=.1, eye='-')],
        [], g='test', act=('prod', 'lump'), obj=[(.3, dict(shake=.1))])
    o.r('hug_the_whole_ball_round', 'Throwing both wings round as much of the ball as he can reach, cheek to the cold', 22, 'none',
        [k(.12, 'mid_l', x=.5, y=.5, b=.7, w=.7), k(.3, 'center', x=.9, y=.7, b=1.2, w=1.5, eye='-'), k(.52, 'center', x=1, y=.8, b=1.4, w=1.7, eye='-', mark='mwa'), k(.74, 'mid_l', x=.6, y=.5, b=.8, w=.8), k(.88, eye='^')],
        [(.52, 'rest')], g='rest', act=('wrap', 'ball'), prefer=['lonely', 'sad'], obj=[(.3, dict(sway=.1)), (.52, dict(sway=.15))], say=["Hugged a snowball. I am very cold and very fine.", "Do not mention the hug. The ball will deny it."])
    o.r('scoop_loose_flakes_back_on', 'Scooping loose flakes from the foot with a wing and patting them back onto the thin spot', 24, 'wing',
        [k(.1, 'base_l', reach=.5, x=.4, y=1, b=.9), k(.24, 'base', reach=1, x=.5, y=1.2, b=1.1, l=1, mark='scp'), k(.4, 'low_l', reach=1, x=.5, y=.8, b=.8, mark='pap'), k(.56, 'base_r', reach=1, x=.5, y=1.2, b=1.1, r=1, mark='scp'), k(.72, 'low_r', reach=1, x=.5, y=.8, b=.8, mark='pap'), k(.9, eye='^')],
        [(.72, 'reshape')], g='care', act=('scoop', 'flakes'), when=['obj_condition<.8'], obj=[(.4, dict(shake=.1)), (.72, dict(shake=.2))])
    o.r('splash_in_the_melt_puddle', 'Splashing round the foot of the ball in its melt puddle, flinging drops with both wings', 20, 'none',
        [k(.1, 'base_l', x=.3, y=.6, b=.6, l=1), k(.24, 'base', x=.5, y=.9, b=1.2, r=1, w=.9, mark='splsh'), k(.4, 'base_r', x=.3, y=.6, b=-.4, l=1, w=1.1), k(.56, 'base', x=.6, y=1, b=1.3, r=1, w=1, mark='SPLSH'), k(.74, 'base_l', x=.3, y=.5, b=.5, w=.7, eye='^'), k(.88, eye='^')],
        [(.56, 'fun')], g='play', act=('splash', 'foot'), when=['obj_wetness>.3'], prefer=['happy', 'young'])
    o.r('span_it_with_both_wings', 'Spreading both wings round the ball as wide as they will go to measure how fat it is', 20, 'none',
        [k(.12, 'mid_l', x=.3, y=.3, b=.4, w=.6), k(.3, 'mid_l', x=.4, y=.2, b=.6, w=1.5), k(.48, 'center', x=.5, y=.2, b=.7, w=1.6, mark='this much'), k(.66, 'mid_r', x=.4, y=.2, b=.6, w=1.5), k(.84, eye='^')],
        [], g='test', act=('measure', 'girth'), say=["Wider than my wings. Fine. Fat ball.", "Measured it. Needed more wing."])
    o.r('rock_it_on_the_flat_base', 'Leaning on the shoulder with both feet braced to rock the heavy ball over its flat base', 20, 'none',
        [k(.1, 'shoulder_l', x=.4, y=.6, b=.7), k(.26, 'shoulder_l', x=1.2, y=.5, b=1.4, l=1, mark='hnng'), k(.42, 'shoulder_l', x=1.5, y=.4, b=1.6, r=1, mark='HNNG'), k(.58, 'shoulder_l', x=1, y=.3, b=1, eye='>'), k(.76, 'mid_l', x=.3, y=.3, b=.4, eye='-'), k(.9, eye='^')],
        [], g='use', act=('rock', 'ball'), ages=GROWN, obj=[(.26, dict(sway=.3)), (.42, dict(sway=.8, shake=.2)), (.58, dict(sway=-.5)), (.76, dict(sway=0))])
    done(o)
    return o


def squeaky_toy():
    # Drawing (48 cols x 35 rows, 3.9 px a row, 128 px tall): a rubber duck toy. Head circle rows 3-13 (eye `O` row 7, a sparkle `..` row 4), a bill `_______` / `\_____>`
    # at rows 9-10 pointing right (100-113 px up), a water-line of `~` at row 14, a bowl-shaped body rows 15-28 with a small wing `.--.` / `/ . \` / `'----'` at rows 18-20
    # (66-50 px), a tail `<(` low on the left at row 22, stitch-like ticks on row 27, a flat base `____` at row 29 (23 px) and a row of ripples `~~~` at rows 30-31.
    # A hatchling reaches row 19 and below (wing, tail, belly, base); head, bill and eye need a grown duck. Its own nature is the squeak: pressing it deflates it for a while.
    P = pm('squeaky_toy')
    o = Obj('squeaky_toy', 'portable', liftable=True,
            fields=dict(plump=(1, 0, 1), frost=(0, 0, 1)),
            physics=[('plump', 'rate', .003, 'always'), ('frost', 'rate', .0015, 'cold&!snow'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(squish=[('plump', 'add', -.4)], massage=[('plump', 'add', .4)], wipe=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)],
                         scrape=[('frost', 'mul', .2)], mend=[('obj.condition', 'add', .25)], chew=[('obj.condition', 'add', -.15)], muddy=[('obj.dirt', 'add', .15)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], mate=[('need.social', 'add', 1)]),
            anchors=dict(tail=P(6, 22), back_l=P(9, 18), flank_l=P(10, 26), wing_a=P(18, 19), wing_b=P(21, 19), belly_a=P(16, 22, 'inside'), belly_c=P(24, 24, 'inside'), belly_b=P(30, 22, 'inside'),
                         belly_low=P(24, 27), chest=P(40, 19), chest_hi=P(40, 12), neck_b=P(26, 12), eye_spot=P(36, 7), bill_up=P(45, 9), bill_tip=P(46, 10), crest=P(31, 4),
                         base_l=P(14, 29, 'surface'), base_mid=P(24, 29, 'surface'), base_r=P(34, 29, 'surface'), ripple=P(20, 30)))
    # ---------------- care
    o.r('massage_the_belly_back_to_plump', 'Rubbing the flat belly in slow circles with a wing until it plumps back up', 22, 'wing',
        [k(.1, 'belly_a', reach=.5, x=.3, y=.7, b=.4), k(.26, 'belly_c', reach=1, x=.6, y=1, b=.7, l=1), k(.42, 'belly_b', reach=1, x=.6, y=1, b=.8), k(.58, 'belly_low', reach=1, x=.5, y=1.2, b=.9, r=1), k(.74, 'belly_c', reach=1, x=.5, y=1, b=.7), k(.9, eye='^')],
        [(.58, 'massage')], g='care', act=('polish', 'belly'), when=['plump<.6'], obj=[(.26, dict(sway=.1)), (.42, dict(sway=-.1)), (.58, dict(sway=.15))],
        say=["Plumped it. A toy with a belly. Understood.", "Rubbed it round. It sighed. Rubber does that."])
    o.r('mop_the_wet_off_its_back', 'Mopping the wet off its back and flank with the flat of a wing', 18, 'wing',
        [k(.1, 'back_l', reach=.5, x=.3, y=.5, b=.3), k(.28, 'back_l', reach=1, x=.6, y=.8, b=.5, l=1, mark='pat'), k(.46, 'flank_l', reach=1, x=.6, y=1, b=.7, r=1, mark='pat'), k(.64, 'belly_a', reach=1, x=.5, y=.9, b=.6), k(.82, eye='-')],
        [(.46, 'dry')], g='care', act=('dry', 'flank'), when=['obj_wetness>.3'])
    o.r('rub_the_grime_off_the_wing', 'Rubbing the grime out of the little wing with his chest feathers', 18, 'none',
        [k(.12, 'wing_a', x=.5, y=.7, b=.7), k(.3, 'wing_a', x=.8, y=.9, b=1, l=1, mark='sqk'), k(.48, 'wing_b', x=.8, y=.9, b=1, r=1, mark='sqk'), k(.66, 'wing_a', x=.6, y=.8, b=.8), k(.84, eye='^')],
        [(.48, 'wipe')], g='care', act=('wipe', 'wing'), when=['obj_dirt>.3'], say=["Wing clean. Squeak free. Thank God.", "Scrubbed it. Now it smells of me."])
    o.r('chip_the_frost_off_the_tail', 'Chipping the frost off the tail and base with a twig, tapping it loose', 20, 'twig',
        [k(.1, 'tail', reach=.5, x=.4, y=.5), k(.26, 'tail', reach=1, x=.8, y=.8, b=.4, mark='tik'), k(.44, 'flank_l', reach=1, x=.9, y=.9, b=.5, mark='tik'), k(.62, 'base_l', reach=1, x=.9, y=.9, b=.6, mark='tik'), k(.8, eye='-')],
        [(.44, 'scrape')], g='care', act=('chip', 'tail'), when=['frost>.3'])
    o.r('straighten_the_bent_bill', 'Nipping the bent bill tip straight, then flinching as it squeaks', 18, 'none',
        [k(.1, 'bill_up', x=.6, y=.2, b=.2), k(.26, 'bill_tip', x=1.1, y=.5, b=.5, mark='nk'), k(.42, 'bill_tip', x=1.2, y=.6, b=.6, l=1, mark='squk'), k(.58, x=-.8, y=.4, b=.2, w=.6, eye='>'), k(.76, 'bill_tip', x=1, y=.4, b=.4, eye='^')],
        [(.42, 'mend')], g='care', act=('straighten', 'bill'), ages=GROWN, when=['obj_condition<.7'], obj=[(.26, dict(shake=.2)), (.42, dict(shake=.3))])
    o.r('sweep_the_ripples_flat', 'Sweeping the ripples at its base flat with sideways wing strokes', 16, 'wing',
        [k(.12, 'ripple', reach=.5, x=.4, y=.9, b=.7), k(.3, 'base_l', reach=1, x=.6, y=1.1, b=.9, l=1, mark='shh'), k(.5, 'base_mid', reach=1, x=.6, y=1.1, b=.9, r=1), k(.7, 'base_r', reach=1, x=.5, y=1, b=.8), k(.86, eye='-')],
        [(.5, 'wipe')], g='care', act=('sweep', 'ripples'), when=['obj_dirt>.45'])
    # ---------------- use (the squeak, the carrying)
    o.r('squeeze_a_squeak_out_of_it', 'Putting his full weight on the belly with a wing and getting one long squeak', 16, 'wing',
        [k(.12, 'belly_a', reach=.5, x=.2, y=.7, b=.5), k(.28, 'belly_c', reach=1, x=.5, y=1.2, b=1.2, mark='hup'), k(.44, 'belly_c', reach=1, x=.5, y=1.4, b=1.6, l=1, r=1, mark='SQUEEEK'), k(.62, 'belly_c', reach=.4, x=-.3, y=.3, b=.2, w=.6, eye='O'), k(.8, eye='^')],
        [(.44, 'squish')], g='use', act=('squeeze', 'belly'), when=['plump>.5'], obj=[(.28, dict(sway=.1)), (.44, dict(shake=.5, sway=-.2)), (.62, dict(sway=.1))],
        say=["Squeak. Perfect. Five stars. Maybe six.", "One squeak, one smile. Good ratio."])
    o.r('play_it_a_tune_with_his_feet', 'Playing a tune on the belly by stamping it, left foot low and right foot high', 22, 'none',
        [k(.1, 'belly_low', x=.2, y=.7, b=.8, l=1), k(.24, 'belly_low', x=.3, y=.9, b=1.3, l=1, mark='squk'), k(.38, 'belly_b', x=.2, y=.7, b=1, r=1, mark='SQK'), k(.52, 'belly_low', x=.3, y=.9, b=1.4, l=1, mark='squk'), k(.66, 'belly_b', x=.2, y=.7, b=1.1, r=1, mark='SQEEK'), k(.84, eye='^')],
        [], g='play', act=('drum', 'belly'), when=['plump>.5'], prefer=['happy'], obj=[(.24, dict(shake=.3)), (.38, dict(shake=.4)), (.52, dict(shake=.3)), (.66, dict(shake=.5))])
    o.r('carry_it_by_the_tail', 'Gripping the tail in his bill and trotting the toy a few steps off, setting it down, and fetching it back', 26, 'none',
        [k(.08, 'tail', x=.8, y=.9, b=.6), k(.2, 'tail', x=1.3, y=1.3, b=1.1, mark='hup'), k(.36, 'tail', x=.5, y=.2, b=-.2, l=1), k(.5, 'tail', x=.4, y=.3, b=-.1, r=1), k(.62, 'tail', x=1.2, y=1.2, b=.9),
         k(.76, 'tail', x=1.4, y=1.2, b=.8), k(.9, eye='^')],
        [], g='use', act=('carry', 'tail'), ages=GROWN,
        obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.5, dict(hold=1)), (.58, dict(hold=0, ix=4)), (.66, dict(hold=0, ix=4)), (.74, dict(hold=1, ix=4)), (.82, dict(hold=1)), (.92, dict(hold=0))],
        say=["Carried a duck by the tail. It squeaked. Fair.", "Delivered it. Then collected it. Logistics."])
    o.r('drag_it_by_the_bill_along', 'Hooking the bill with his own and dragging the toy along the ground, squeaking as it bumps, then back', 24, 'none',
        [k(.1, 'bill_tip', x=.7, y=1.2, b=.9), k(.24, 'bill_tip', x=1.3, y=1.5, b=1.3, l=1, mark='hnn'), k(.42, 'bill_tip', x=-.4, y=1.3, b=1.4, r=1, mark='sqk'), k(.6, 'bill_tip', x=-.5, y=1.3, b=1.4, l=1, mark='sqk'), k(.78, 'bill_tip', x=.4, y=1.1, b=1.1, r=1), k(.9, eye='-')],
        [(.42, 'muddy')], g='use', act=('drag', 'bill'), ages=GROWN, obj=[(.24, dict(ix=0)), (.42, dict(ix=-3)), (.5, dict(ix=-3, shake=.2)), (.66, dict(ix=-1)), (.78, dict(ix=0))])
    o.r('tip_it_onto_its_side_and_right_it', 'Putting his shoulder to its chest, tipping it onto its side, and heaving it upright again', 26, 'none',
        [k(.1, 'chest', x=.3, y=.3, b=.5), k(.24, 'chest', x=1, y=.4, b=1.2, l=1, mark='hnng'), k(.4, 'chest', x=1.2, y=.3, b=1.4, r=1, eye='>'), k(.54, 'back_l', x=1.1, y=.8, b=1.3, mark='hup'), k(.72, 'back_l', x=1.2, y=.9, b=1.5, l=1, r=1, mark='HUP'), k(.88, eye='^')],
        [], g='use', act=('tilt', 'chest'), ages=GROWN, obj=[(.24, dict(sway=.4)), (.4, dict(sway=1, shake=.2)), (.54, dict(sway=1)), (.72, dict(sway=-.4)), (.84, dict(sway=0))])
    o.r('roll_it_flat_out_to_the_side', 'Rolling the toy over and over with his bill and following it, then rolling it home again', 26, 'none',
        [k(.1, 'flank_l', x=.7, y=1, b=.9), k(.22, 'flank_l', x=1.3, y=1.2, b=1.2, l=1, mark='rrr'), k(.38, x=1.4, y=.4, b=.3, r=1, eye='O'), k(.52, 'belly_c', x=1.3, y=1, b=.9, mark='sqk'), k(.68, 'belly_c', x=.4, y=.2, b=-.2, l=1), k(.86, eye='^')],
        [(.22, 'muddy')], g='use', act=('roll', 'flank'), obj=[(.22, dict(ix=0)), (.3, dict(ix=3, shake=.2)), (.44, dict(ix=6)), (.52, dict(ix=6)), (.62, dict(ix=3)), (.74, dict(ix=0))])
    o.r('stash_it_away_from_the_flock', 'Dragging the toy into a hollow and scuffing leaves over it, squeaking, then digging it out', 30, 'none',
        [k(.08, 'tail', x=.9, y=1.1, b=.7), k(.2, 'tail', x=1.3, y=1.2, b=1, l=1), k(.34, 'base_l', x=1, y=1.5, b=1.2, l=1, mark='skrt'), k(.46, 'base_l', x=-.3, y=-.5, b=-.2, w=.5, eye='<', mark='sqk'), k(.6, 'base_mid', x=1, y=1.4, b=1.1, r=1, mark='skrt'),
         k(.7, 'base_mid', x=1.1, y=1.5, b=1.2, r=1, mark='skrt'), k(.78, 'base_mid', x=1.2, y=1.6, b=1.3, l=1, mark='skrt'), k(.92, eye='^')],
        [], g='use', act=('hide', 'toy'), prefer=['curious'],
        obj=[(.2, dict(hold=0)), (.28, dict(hold=1)), (.38, dict(hold=1, hide=1)), (.44, dict(hold=0, hide=1)), (.58, dict(hide=1)), (.66, dict(hide=1)), (.72, dict(hide=0)), (.8, dict(hide=0))],
        say=["Buried a squeaky toy. It squeaked from underground. Subtle.", "Nobody will find it. Everyone will hear it."])
    # ---------------- play
    o.r('fetch_it_by_the_tail', 'Swinging the toy by the tail and flinging it off, then galloping after it to fetch it back', 26, 'none',
        [k(.08, 'tail', x=.8, y=1, b=.7), k(.2, 'tail', x=1.4, y=1.4, b=1.2, l=1), k(.34, 'tail', x=-.7, y=-.5, b=-.7, w=.8, mark='HUP'), k(.46, x=1.7, y=-.2, b=-.2, r=1, w=1, eye='>'), k(.6, x=1.5, y=.5, b=.4, l=1, r=1),
         k(.74, 'tail', x=1.3, y=1.1, b=.8), k(.88, eye='^')],
        [(.2, 'fun')], g='play', act=('throw', 'tail'), ages=GROWN, prefer=['happy', 'young'],
        obj=[(.2, dict(hold=0)), (.3, dict(hold=1)), (.38, dict(hold=1)), (.44, dict(hold=.3, ix=3, iy=-3)), (.5, dict(hold=0, ix=6, iy=0)), (.62, dict(ix=6)), (.7, dict(hold=1, ix=6)), (.8, dict(hold=1, ix=0)), (.88, dict(hold=0))],
        say=["Threw a duck. Fetched a duck. Dog energy.", "It squeaked on landing. I count that as applause."])
    o.r('bounce_off_the_belly_and_squeak', 'Taking a run-up and bouncing off the belly with both feet to set off a big squeak', 18, 'none',
        [k(.1, x=-.5, y=.4, b=.6, w=.3), k(.24, x=1.3, y=-.5, b=-.9, l=1, r=1, w=.7), k(.38, 'belly_a', x=2, y=.9, b=-1.5, l=1, r=1, w=1.1, mark='SQUEEK'), k(.54, x=-1.4, y=1, b=2, w=.9, eye='@'), k(.72, x=.3, y=.6, b=.6, eye='-')],
        [(.38, 'squish')], g='play', act=('hop', 'belly'), when=['plump>.5'], prefer=['happy', 'young'], obj=[(.38, dict(shake=.6, sway=-.3)), (.54, dict(sway=.3)), (.7, dict(sway=0))])
    o.r('squeak_it_in_time_with_a_march', 'Marching round the toy, pressing a squeak with each step in time', 22, 'none',
        [k(.1, 'belly_a', x=.3, y=.7, b=.6, l=1), k(.22, 'belly_a', x=.4, y=.8, b=1.2, l=1, mark='sq'), k(.34, 'belly_c', x=.3, y=.7, b=.6, r=1), k(.46, 'belly_c', x=.4, y=.8, b=1.2, r=1, mark='sq'), k(.58, 'belly_b', x=.3, y=.7, b=.6, l=1), k(.7, 'belly_b', x=.4, y=.8, b=1.2, l=1, mark='SQ'), k(.86, eye='^')],
        [], g='play', act=('dance', 'belly'), when=['plump>.5'], prefer=['happy'], obj=[(.22, dict(shake=.2)), (.46, dict(shake=.3)), (.7, dict(shake=.4))])
    o.r('race_it_by_a_kick', 'Booting the toy off its flank and racing it across the ground, squeaking all the way', 20, 'none',
        [k(.1, 'flank_l', x=.2, y=.7, b=.8, l=1), k(.24, 'flank_l', x=-.7, y=.4, b=1.2, l=1, mark='pok'), k(.38, x=1.5, y=.2, b=-.3, r=1, w=.6, eye='>'), k(.54, 'belly_a', x=1.3, y=1, b=.8, mark='sqk'), k(.72, 'belly_a', x=.4, y=-.1, b=-.2, l=1), k(.86, eye='^')],
        [(.24, 'chew')], g='play', act=('kick', 'flank'), prefer=['grumpy'],
        obj=[(.24, dict(ix=0)), (.32, dict(ix=3, shake=.4)), (.46, dict(ix=5)), (.54, dict(ix=5, hold=1)), (.66, dict(ix=0, hold=1)), (.76, dict(hold=0))])
    o.r('catch_it_when_it_is_tossed_up', 'Tossing the toy up by the tail and catching it in his bill, squeaking when it lands', 20, 'none',
        [k(.1, 'tail', x=.8, y=1.1, b=.8), k(.24, 'tail', x=1.4, y=1.5, b=1.2, l=1), k(.38, x=.4, y=-1.5, b=-1, w=.7, eye='O'), k(.5, x=.6, y=-1.6, b=-.6, w=.5), k(.64, 'tail', x=1.5, y=1.2, b=1, mark='sqk'), k(.82, eye='^')],
        [], g='play', act=('catch', 'toy'), ages=GROWN,
        obj=[(.24, dict(hold=1)), (.34, dict(hold=1)), (.42, dict(hold=0, iy=-5)), (.52, dict(iy=-5)), (.6, dict(hold=1, iy=0)), (.76, dict(hold=0))])
    o.r('shake_it_by_the_neck', 'Shaking the toy by the neck like a rag, squeaking at every shake', 18, 'none',
        [k(.1, 'neck_b', x=.9, y=1, b=.6), k(.22, 'neck_b', x=1.5, y=1.4, b=1, mark='hup'), k(.36, 'neck_b', x=-.6, y=.4, b=.3, l=1, mark='sqk'), k(.5, 'neck_b', x=1.6, y=.5, b=.4, r=1, mark='sqk'), k(.64, 'neck_b', x=-.5, y=.4, b=.3, l=1, mark='SQK'), k(.82, eye='>')],
        [(.5, 'chew')], g='play', act=('shake', 'neck'), ages=GROWN, prefer=['grumpy'],
        obj=[(.22, dict(hold=0)), (.32, dict(hold=1)), (.5, dict(hold=1, shake=.8)), (.7, dict(hold=1)), (.8, dict(hold=0))], say=["Shook it. It squealed. Satisfying.", "Rag-dolled a duck. We are not telling anyone."])
    # ---------------- test
    o.r('hunt_the_squeak_by_pressing', 'Pressing the belly, the wing and the back in turn to find where the squeak lives', 24, 'none',
        [k(.1, 'belly_a', x=.4, y=.8, b=.6), k(.24, 'belly_a', x=.8, y=1, b=1, mark='nothing'), k(.4, 'wing_a', x=.8, y=1, b=1, l=1, mark='nothing'), k(.56, 'back_l', x=.8, y=1, b=1, r=1, mark='nothing'), k(.7, 'belly_low', x=.9, y=1.2, b=1.2, eye='O', mark='SQK'), k(.86, eye='^')],
        [(.7, 'squish')], g='test', act=('press', 'belly'), when=['plump>.5'], obj=[(.24, dict(sway=.1)), (.7, dict(shake=.4))], say=["Found it. Low and left. Typical squeak.", "Squeak hides in the belly. As do I."])
    o.r('ear_to_the_belly', 'Pressing an ear to the belly and listening for the squeak to settle', 18, 'none',
        [k(.12, 'belly_b', x=-.4, y=.9, b=.9, l=1), k(.3, 'belly_b', x=.3, y=1.3, b=1.3, eye='-'), k(.52, 'belly_b', x=.4, y=1.4, b=1.4, eye='-', mark='psssh', r=1), k(.7, x=-.6, y=-.8, b=-.2, eye='O'), k(.86, eye='-')],
        [], g='test', act=('listen', 'belly'))
    o.r('sniff_the_rubber', 'Sniffing along the back and flank for the smell of warm rubber', 16, 'none',
        [k(.12,'tail',x=.4,y=1.2,b=1.1), k(.28,'flank_l',x=1.4,y=1.5,b=1.4,mark='snff'), k(.46,'back_l',x=1.5,y=.9,b=.5,mark='snff',l=1), k(.64,'wing_a',x=1.6,y=.4,b=.1,r=1), k(.8,x=-.8,y=.3,eye='O',mark='bleh')],
        [], g='test', act=('sniff', 'back'))
    o.r('chew_the_bill_for_flavour', 'Chewing the bill end for a taste, getting a squeak and a mouthful of nothing', 16, 'none',
        [k(.12, 'bill_tip', x=1, y=1, b=.5), k(.3, 'bill_tip', x=1.6, y=1.3, b=.9, eye='-', mark='gnm'), k(.46, 'bill_tip', x=1.7, y=1.3, b=.9, eye='>', mark='sqk'), k(.62, x=-.8, y=.4, w=.6, eye='>', mark='ptui'), k(.8, eye='-')],
        [(.46, 'chew')], g='test', act=('taste', 'bill'), ages=GROWN)
    o.r('stare_the_eye_down', 'Staring into the painted eye, nose to nose, until one of them blinks', 22, 'none',
        [k(.12, 'eye_spot', x=.8, y=.3, b=.3), k(.3, 'eye_spot', x=1.7, y=.4, b=.5, eye='O'), k(.5, 'eye_spot', x=1.8, y=.5, b=.5, eye='@', mark='...'), k(.7, 'eye_spot', x=-.5, y=-.2, b=-.1, eye='-', mark='ha'), k(.86, eye='^')],
        [], g='show', act=('peer', 'eye'), ages=GROWN, say=["It blinked first. It does not have eyelids. Still counts.", "Staring contest: won. Opponent: rubber."])
    o.r('lift_the_tail_and_judge_the_weight', 'Lifting the toy by the tail and bobbing it twice to judge its weight', 18, 'none',
        [k(.1, 'tail', x=.8, y=1, b=.6), k(.24, 'tail', x=1.4, y=1.4, b=1.1, mark='hup'), k(.4, 'tail', x=.4, y=-.5, b=-.6), k(.54, 'tail', x=.9, y=.8, b=.5), k(.68, 'tail', x=.3, y=-.6, b=-.7, mark='hup'), k(.84, eye='-')],
        [], g='test', act=('weigh', 'toy'), ages=GROWN, obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.5, dict(hold=1, iy=1)), (.64, dict(hold=1)), (.78, dict(hold=0))])
    o.r('squeak_it_at_every_height', 'Pressing the toy low, then the chest, then the bill to compare how the squeaks differ in pitch', 24, 'none',
        [k(.1, 'belly_low', x=.5, y=1.1, b=1), k(.24, 'belly_low', x=.7, y=1.4, b=1.4, mark='low'), k(.42, 'chest', x=.8, y=1, b=1, mark='mid'), k(.6, 'chest_hi', x=.9, y=.6, b=.6, mark='high'), k(.76, 'bill_up', x=1, y=.4, b=.4, mark='HIGH'), k(.9, eye='^')],
        [], g='test', act=('compare', 'pitch'), ages=GROWN, when=['plump>.5'])
    # ---------------- rest
    o.r('nap_with_his_cheek_on_its_back', 'Napping with his cheek on its rounded back and a wing over its wing', 30, 'none',
        [k(.14, 'back_l', x=.2, y=.9, b=1.2, l=1), k(.32, 'back_l', x=.3, y=1.5, b=1.8, eye='-'), k(.55, 'back_l', x=.4, y=1.9, b=2.1, w=.5, eye='-', mark='zzz'), k(.8, 'back_l', x=.3, y=1.6, b=1.8, eye='-', mark='zz')],
        [(.55, 'rest')], g='rest', act=('nap', 'back'), when=['tired'], prefer=['tired'])
    o.r('sit_square_and_wait_for_it_to_reinflate', 'Sitting square in front of the toy, waiting for the flat belly to puff back out', 28, 'none',
        [k(.12,'belly_c',x=.6,y=1.2,b=1.9,eye='-'), k(.34,'belly_c',x=.4,y=1.6,b=2.1,eye='-'), k(.56,'belly_c',x=-.6,y=-.9,b=.2,eye='O',mark='...pfft'), k(.78,'belly_c',x=.5,y=1.4,b=1.9,eye='>')],
        [], g='rest', act=('wait', 'toy'), when=['plump<.6'], say=["Waiting for it to re-inflate. Longest minute ever.", "It will pop back. Probably. Squeaking."])
    o.r('lean_on_the_rounded_flank', 'Leaning his back against the rounded flank and rocking gently with it', 22, 'none',
        [k(.12, 'flank_l', x=-.6, y=.2, b=.6), k(.3, 'flank_l', x=-.9, y=.5, b=1.1, eye='-'), k(.52, 'flank_l', x=-1, y=.7, b=1.3, eye='-', mark='ahh'), k(.78, 'flank_l', x=-.7, y=.4, b=.8, eye='-')],
        [], g='rest', act=('lean', 'flank'), prefer=['tired'], obj=[(.3, dict(sway=.15)), (.52, dict(sway=-.15)), (.7, dict(sway=.1))])
    o.r('sulk_with_a_wing_on_its_tail', 'Sulking with his bill on the toy tail and one wing over his eyes', 24, 'none',
        [k(.14, 'tail', x=-.4, y=.9, b=.9), k(.32, 'tail', x=-.7, y=1.5, b=1.5, w=.6, eye='-'), k(.58, 'tail', x=-.8, y=1.7, b=1.7, w=.6, eye='-', mark='hmph'), k(.82, 'tail', x=-.5, y=1, b=1, eye='>')],
        [], g='rest', act=('sulk', 'tail'), prefer=['sad', 'grumpy'])
    o.r('stand_guard_beside_the_duck', 'Standing guard beside the toy with his chest out, watching the yard for rival ducks', 26, 'none',
        [k(.1, 'belly_a', x=.3, y=-.5, b=-.2, w=.4), k(.3, 'belly_a', x=-.5, y=-.9, b=-.5, w=.6, eye='<'), k(.5, 'belly_c', x=.6, y=-.8, b=-.4, w=.7, eye='>'), k(.7, 'belly_a', x=-.4, y=-.9, b=-.5, w=.6, eye='<'), k(.88, eye='^')],
        [], g='rest', act=('guard', 'toy'), prefer=['grumpy'], say=["Rival ducks, back off. It is my duck.", "Guarding a toy. It guards nothing back."])
    o.r('balance_along_the_base_rim', 'Balancing along the flat rim at the base from end to end with his wings out', 24, 'none',
        [k(.08, 'base_l', x=.5, y=.5, b=.4), k(.2, 'base_l', perch=1, x=-.2, y=-.4, b=-.6, w=.7), k(.36, 'base_mid', perch=1, x=-.4, y=-.6, b=-.8, l=1, w=1), k(.52, 'base_r', perch=1, x=-.2, y=-.4, b=-.6, r=1, w=1.1), k(.68, 'base_mid', perch=1, x=-.5, y=-.7, b=-.8, l=1, w=1), k(.84, 'base_l', x=.3, y=.5, b=.3)],
        [], g='play', act=('balance', 'rim'), obj=[(.2, dict(sway=.1)), (.36, dict(sway=-.1)), (.52, dict(sway=.15)), (.68, dict(sway=-.1)), (.84, dict(sway=0))])
    # ---------------- weather
    o.r('bask_on_the_sun_warm_rubber', 'Pressing his breast to the sun-warmed back of the toy and soaking in the heat', 22, 'none',
        [k(.14, 'back_l', x=.4, y=.5, b=.8), k(.34, 'flank_l', x=.7, y=.8, b=1.3, w=.4, eye='-'), k(.58, 'flank_l', x=.8, y=1, b=1.5, eye='-', mark='mmm'), k(.82, 'back_l', x=.5, y=.5, b=.8, eye='^')],
        [(.58, 'rest')], g='weather', act=('warm', 'back'), when=['sun', 'day'])
    o.r('tip_the_rain_off_its_head', 'Standing on his toes to tip the rain pooled on its head down off the crown', 24, 'none',
        [k(.1, 'chest', x=.3, y=.4, b=.5), k(.26, 'chest_hi', x=.6, y=-.3, b=-.7, w=.5, mark='hup'), k(.44, 'crest', x=.9, y=-.5, b=-.9, l=1, w=.8, mark='splash'), k(.62, 'chest_hi', x=-.3, y=.6, b=.8, eye='>'), k(.82, eye='-')],
        [(.44, 'dry')], g='weather', act=('tip', 'crown'), ages=GROWN, when=['wet', '!storm', 'obj_wetness>.3'], obj=[(.26, dict(sway=.3)), (.44, dict(sway=-.4, shake=.3)), (.62, dict(sway=.1))])
    o.r('brace_it_against_the_gust', 'Planting his feet at the base and leaning on the chest so the gust cannot blow the toy over', 24, 'none',
        [k(.1, 'chest', x=.5, y=.4, b=.7), k(.26, 'chest', x=1.1, y=.6, b=1.3, l=1, mark='hff'), k(.5, 'chest', x=1.3, y=.6, b=1.5, r=1, eye='>'), k(.72, 'chest', x=1, y=.5, b=1, l=1), k(.88, eye='^')],
        [], g='weather', act=('brace', 'chest'), ages=GROWN, when=['windy'], obj=[(.26, dict(sway=.4)), (.5, dict(sway=-.6, shake=.3)), (.72, dict(sway=.2))])
    o.r('catch_it_as_the_wind_rolls_it', 'Sprinting after the toy as the gust rolls it off squeaking, and carrying it home by the tail', 22, 'none',
        [k(.1, 'belly_b', x=.4, y=.3, b=.2, w=.4), k(.26, x=1.8, y=.1, b=-.3, l=1, r=1, w=.9, eye='O'), k(.44, x=1.4, y=.8, b=.5, mark='sqk'), k(.58, 'tail', x=1.3, y=1, b=.8, mark='gotcha'), k(.74, 'tail', x=.3, y=-.2, b=-.2, l=1), k(.88, eye='^')],
        [], g='weather', act=('chase', 'toy'), ages=GROWN, when=['windy'],
        obj=[(.18, dict(ix=0)), (.28, dict(ix=3, shake=.4)), (.42, dict(ix=7)), (.5, dict(ix=7)), (.6, dict(ix=7, hold=1)), (.74, dict(ix=0, hold=1)), (.84, dict(hold=0))])
    # ---------------- show
    o.r('bow_to_the_squeaker', 'Bowing deeply to the toy, which squeaks in reply as his bill touches the belly', 18, 'none',
        [k(.14, 'belly_low', x=.5, y=-.8, b=-.6, w=.8, r=1), k(.34, 'belly_low', x=1.8, y=2.6, b=2.8, w=1.2, mark='sqk'), k(.6, 'belly_low', x=1.9, y=2.7, b=2.9, eye='-'), k(.8, x=.3, y=-.9, b=-.5, l=1, eye='^')],
        [(.34, 'mate')], g='show', act=('bow', 'toy'), obj=[(.34, dict(shake=.3))], say=["Bowed. It squeaked back. Politest duck in the yard.", "Mutual respect. Mostly squeak."])
    o.r('present_the_toy_with_a_squeak', 'Sweeping a wing at the toy like a game-show prize, ending on a squeaked fanfare', 20, 'wing',
        [k(.12, 'tail', reach=.4, x=.6, y=.8, b=.7, w=.3), k(.32, 'belly_a', reach=1, x=-.2, y=.4, b=.2, mark='behold'), k(.52, 'wing_b', reach=1, x=-.5, y=-.4, b=-.5, r=1), k(.72, 'belly_c', reach=1, x=.2, y=1, b=1.1, mark='SQEEEK'), k(.88, eye='^')],
        [], g='show', act=('present', 'toy'), when=['plump>.5'], obj=[(.72, dict(shake=.5))], say=["Behold. Fanfare by squeak.", "Prize of the day. Terms and conditions: it squeaks."])
    o.r('argue_with_the_bill', 'Arguing with the toy bill to bill, each of his points answered with a squeak', 22, 'none',
        [k(.1, 'bill_tip', x=.4, y=.6, b=.4, w=.6), k(.24, 'bill_tip', x=1.7, y=.9, b=.6, mark='no'), k(.38, 'bill_up', x=-.4, y=.4, b=.9, l=1, mark='YES'), k(.52, 'bill_tip', x=1.7, y=.9, b=.6, w=1, mark='no'), k(.68, 'bill_up', x=-.3, y=.8, b=1, r=1, eye='>'), k(.84, eye='-')],
        [], g='show', act=('argue', 'bill'), ages=GROWN, prefer=['grumpy'], obj=[(.24, dict(shake=.2)), (.52, dict(shake=.3))])
    o.r('match_its_pose_beak_up', 'Matching its stiff pose, bill up and chest out, and holding it for the camera', 22, 'none',
        [k(.12, 'chest', x=.2, y=.5, b=.6, w=.3), k(.3, 'chest', x=.7, y=-1.3, b=-1, w=.6, eye='^'), k(.55, 'chest', x=.8, y=-1.5, b=-1.2, w=.8, eye='^', mark='cheese'), k(.8, 'chest', x=.1, y=.6, b=.7, eye='-')],
        [], g='show', act=('pose', 'toy'), prefer=['happy'])
    o.r('dance_a_squeaky_two_step', 'Dancing a two-step beside the toy, tapping the tail and the base for squeaks', 22, 'none',
        [k(.1, 'tail', x=.2, y=-.4, b=-.6, l=1, w=.6), k(.24, 'base_l', x=.4, y=.4, b=.7, r=1, w=1, mark='sq'), k(.4, 'tail', x=-.2, y=-.6, b=-1, l=1, w=.9), k(.56, 'base_mid', x=.6, y=.5, b=.8, r=1, w=1, mark='sq'), k(.72, 'tail', x=.3, y=-.7, b=-1, l=1, w=.8), k(.88, x=.3, y=1.2, b=1.2, eye='^')],
        [], g='show', act=('dance', 'tail'), prefer=['happy'], obj=[(.24, dict(shake=.2)), (.56, dict(shake=.3))])
    o.r('sing_along_to_the_squeak', 'Singing along to the squeak, holding the same note and running out of breath', 24, 'none',
        [k(.1,'belly_a',x=.8,y=.4,b=.9,w=.2), k(.28,'belly_a',x=-1.2,y=-1.6,b=-1.4,w=1.2,eye='-',mark='laa',l=1), k(.48,'belly_c',x=1.8,y=-1.9,b=-1.7,w=1.5,mark='LAAA',r=1), k(.68,'belly_a',x=.9,y=1.1,b=1.4,eye='O',mark='wheeze'), k(.84,eye='-')],
        [(.48, 'mate')], g='show', act=('sing', 'toy'), prefer=['lonely'])
    # ---------------- mishap
    o.r('slip_off_the_wet_ripples', 'Planting a foot on the wet ripples at the base, skidding off, and landing flat', 16, 'none',
        [k(.1,'ripple',x=.6,y=-.3,b=.4,l=1), k(.26,'ripple',x=1.1,y=-.5,b=-.6,l=1,r=1,mark='eh'), k(.42,'base_l',x=2,y=-1.3,b=1.8,r=1,w=1.4,eye='O',mark='WHA'), k(.6,x=2.2,y=1.8,b=2.9,eye='@'), k(.8,x=.6,y=.9,b=.6,eye='-')],
        [], g='mishap', act=('slip', 'ripples'), prefer=['grumpy'], obj=[(.26, dict(shake=.3)), (.42, dict(sway=.4))], say=["Rubber. Wet. Floor. Bad plan.", "I fell. It squeaked. I fell harder."])
    o.r('squeaked_in_the_dark', 'Bumping chest-first into the toy in the dark and setting off a loud squeak', 14, 'none',
        [k(.15, 'belly_a', x=1.8, y=.8, b=1.2, mark='SQEEK'), k(.3, 'belly_a', x=-1.7, y=-1, b=-.9, l=1, r=1, w=1, eye='@'), k(.5, x=-.7, y=1.2, b=1.8, eye='>', mark='ugh'), k(.76, eye='-')],
        [], g='mishap', act=('walk_into', 'toy'), when=['night', 'plump>.5'], obj=[(.15, dict(shake=.6)), (.3, dict(sway=.3))])
    o.r('get_a_foot_wedged_in_the_tail_curl', 'Wedging a foot in the curl of the tail and hopping about with the toy until it pops free', 22, 'none',
        [k(.12,'tail',x=-.5,y=1.1,b=.9,l=1), k(.28,'tail',x=-.9,y=1.5,b=1.4,l=1,mark='hm'), k(.44,'tail',x=-1.2,y=1.8,b=1.8,l=1,r=1,eye='O',mark='SQK'), k(.62,'tail',x=-1.5,y=1.1,b=-.5,w=1.3,mark='POP'), k(.8,x=1,y=.2,b=.4,eye='@')],
        [], g='mishap', act=('stuck', 'tail'), prefer=['curious'], obj=[(.28, dict(sway=.3)), (.44, dict(shake=.6)), (.62, dict(sway=-.5))])
    o.r('stomp_on_the_ripples_in_a_huff', 'Stomping round the base in a temper, kicking spray off the ripples', 18, 'none',
        [k(.12,'ripple',x=-.2,y=.9,b=-.4,r=1), k(.26,'ripple',x=-.4,y=1.1,b=1.9,l=1,w=.5,mark='STOMP'), k(.4,'base_mid',x=-.2,y=.8,b=-.5,r=1), k(.54,'base_mid',x=-.4,y=1.2,b=2,l=1,w=.5,mark='STOMP'), k(.7,x=-.3,y=-.3,eye='>')],
        [(.54, 'muddy')], g='mishap', act=('stamp', 'ripples'), prefer=['grumpy'], obj=[(.26, dict(shake=.3)), (.54, dict(shake=.5))])
    # ---------------- three more acts only a squeaky toy allows
    o.r('hook_it_in_by_the_tail', 'Hooking the tail with a twig from a few steps off and reeling the toy in, squeaking over the bumps', 22, 'twig',
        [k(.1, 'tail', reach=.5, x=.7, y=.3, b=.3), k(.26, 'tail', reach=1, x=1.6, y=.8, b=.8, mark='klk'), k(.44, 'tail', reach=1, x=.1, y=.5, b=1.1, l=1, mark='sqk'), k(.62, 'tail', reach=1, x=.2, y=.4, b=1.2, r=1, mark='sqk'), k(.84, eye='^')],
        [], g='use', act=('hook', 'tail'), obj=[(.1, dict(ix=3)), (.26, dict(ix=3)), (.44, dict(ix=2, shake=.2)), (.62, dict(ix=0, shake=.2))], say=["Fished a duck out of the grass. Bait: none.", "Reeled it in. It squeaked the whole way. Complained."])
    o.r('huddle_at_its_side_in_the_rain', 'Huddling against the toy flank with his bill down, rain drumming on the rubber', 28, 'none',
        [k(.12, 'flank_l', x=-.3, y=.6, b=.9), k(.3, 'flank_l', x=-.6, y=1.1, b=1.5, w=.3, eye='-'), k(.56, 'flank_l', x=-.7, y=1.3, b=1.7, eye='-', mark='drip'), k(.8, 'flank_l', x=-.4, y=.8, b=1.1, eye='>')],
        [], g='weather', act=('shelter', 'toy'), when=['wet', '!storm'], obj=[(.3, dict(sway=.1))], say=["The rain drums it like a drum. A squeaky drum.", "Shelter: rubber. Smells of rubber. Fine."])
    o.r('hug_the_toy_and_squeak_it', 'Hugging the toy tight between both wings until it gives a long wheezy squeak, and holding on', 22, 'none',
        [k(.12, 'belly_a', x=.4, y=.5, b=.7, w=.8), k(.3, 'belly_c', x=.7, y=.7, b=1.2, w=1.5, eye='-'), k(.5, 'belly_c', x=.8, y=.8, b=1.5, w=1.7, eye='-', mark='SQUEEEEK'), k(.72, 'belly_a', x=.5, y=.5, b=.8, w=.9), k(.88, eye='^')],
        [], g='rest', act=('wrap', 'toy'), prefer=['lonely', 'sad'], obj=[(.3, dict(sway=.1)), (.5, dict(shake=.3))], say=["Hugged a toy. It squeaked. Great hug.", "Do not tell anyone. It is a very small duck."])
    done(o)
    return o


if __name__ == '__main__':
    for n in sys.argv[1:] or ['acorn', 'golden_acorn', 'magic_acorn', 'pine_cone', 'snowball', 'squeaky_toy']:
        globals()[n]().emit(need=COUNT_NEED.get(n))
