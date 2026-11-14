"""Wave 4b: two freshwater fish kept in the koi pond (salmon, trout) and four big saltwater fish kept in a deep sea tank (sturgeon, pufferfish,
swordfish, ancient_dragon_fish; host infinity_pool). Every routine is hand-written.

Koi pond drawing (120 cols x 56 rows, 7.5 px a row, Cheese's feet on row 46): three cattail stems with `#` heads at the left (cols 7/12/17), three tall
ones at the right (cols 103/108/113), a grass tuft at the foot (row 44), two lily pads with `{*}` blooms (left one high, rows 30-32; right one low,
rows 35-38), rippling water rows 29-45, a far edge line, a stone bank round it `( )` and front stones at the rim, row 46. Anchors are (column, row)
of that drawing converted by P().

Infinity pool drawing (124 cols x 60 rows, 7.5 px a row, his feet on row 50): a deep sea tank behind a wall of glass `[ SEA TANK ]`: water window
cols 16-104, rows 33-49 (wave marks on rows 34/37/40/43/46), the floor line of the tank on row 49 (a low ledge he can stand on), a coping with a
row of railing posts `[]` above it (rows 27-29, reed or twig reach only), a pier of rungs at each side (cols 8-12 and 107-112) and a stair under
the floor line. Cheese never touches the water: he works from the edge, wing flat on the glass, bill to the glass, a reed held over the coping,
and a fish comes to the touched spot with the lure. Marks stamp the pond's own leaves, ice, flakes and algae (pond_* marks, never copied onto a
fish) and each species' own visible state."""
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


def P(c, r, *fl):  # koi_pond: 120 cols, 55 rows
    return (round(c / 119, 4), round(r / 55, 4), *([' '.join(fl)] if fl else []))


def Q(c, r, *fl):  # infinity_pool: 124 cols, 59 rows
    return (round(c / 123, 4), round(r / 59, 4), *([' '.join(fl)] if fl else []))


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


def salmon():
    # Salmon: silver-red, mid-water, morning and evening, huge leaps, swims against a current. Own state: run (how hard it is driving against
    # the current he made: drawn as streaks), spray (spray left by a leap: drawn), homing (how sure it is of its home bank).
    o = Obj('salmon', 'keeping', on='koi_pond',
            fields=dict(run=(0, 0, 1), spray=(0, 0, 1), homing=(0, 0, 1)),
            physics=[('run', 'rate', -.0004, 'always'), ('spray', 'rate', -.004, 'always'), ('homing', 'rate', -.0003, 'always')],
            effects=dict(skim=[('keeping.leaves', 'mul', .4)], scrub=[('keeping.algae', 'mul', .5)], thin=[('keeping.plants', 'mul', .75)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], clear=[('keeping.clarity', 'add', .15)],
                         churn=[('keeping.oxygen', 'add', .3), ('run', 'add', .3)], scatter=[('keeping.flakes', 'add', .4)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         leap=[('spray', 'set', 1), ('subject.hunger', 'add', -.2), ('run', 'add', .25)],
                         lead=[('homing', 'add', .2), ('subject.trust', 'add', .1)], stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         calm=[('run', 'mul', .4), ('subject.mood', 'add', .1)], crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('spray', .3, "'.:.'", 'bloom_r', 'water'), ('run', .4, '>>>>', 'run_m', 'water'), ('pond_flakes', .3, '.:.:.', 'run_l', 'dust'),
                   ('pond_leaves', .3, ';"~;"', 'rapid', 'leaf'), ('pond_ice', .3, '*-*-*', 'cove', 'frost'), ('pond_algae', .3, '"v"v"', 'stone_l', 'plant')],
            anchors=dict(run_l=P(28, 43), run_m=P(58, 41), run_r=P(88, 39), rapid=P(70, 43), cove=P(40, 39), pad_low=P(86, 37), bloom_r=P(81, 35),
                         cattail_l=P(7, 31), reed_low=P(8, 38), tuft=P(11, 44), bank_r=P(95, 40),
                         stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('hook_the_drift_out_of_the_run', 'Hooking the drifted leaves out of the salmon\'s run with a reed and dragging them to the tuft', 22, 'reed',
        [k(.12, 'run_r', reach=.5, x=.3, y=.4, b=.3), k(.32, 'run_m', reach=1, x=.6, y=.8, b=.6, mark='hook'), k(.52, 'rapid', reach=1, x=.8, y=.9, b=.8, l=1, mark='drag'),
         k(.72, 'tuft', reach=.8, x=.4, y=.5, b=.4, r=1), k(.88, eye='^')],
        [(.52, 'skim')], g='care', act=('hook', 'drift'), when=['pond_leaves>.3'], prefer=['windy'],
        say=["Leaves out of the lane. It can leap at nothing now.", "Raked the run. Salmon will not say thanks, being airborne."])
    o.r('scrub_the_landing_stone_green', 'Scrubbing the green film off the left stone where the salmon\'s spray comes down, one wing swiping', 18, 'wing',
        [k(.12, 'stone_l', reach=.5, x=.2, y=.8, b=.4), k(.3, 'stone_l', reach=1, x=.4, y=1.3, b=.9, l=1, mark='skrk'), k(.5, 'stone_l', reach=1, x=.5, y=1.2, b=.8, r=1, mark='skrk'),
         k(.7, 'stone_m', reach=1, x=.3, y=1, b=.6), k(.88, y=.1, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'stone'), when=['pond_algae>.4'])
    o.r('pull_the_pads_off_the_leap_lane', 'Pulling the right-hand pad aside with a twig so the leap lane stays open above the water', 22, 'twig',
        [k(.08, 'pad_low', reach=.4, x=.1, y=-.2), k(.24, 'bloom_r', reach=.9, x=.8, y=.9, b=.2, mark='hook'), k(.41, 'bloom_r', reach=1, x=1.1, y=1, b=1, l=1), k(.6, 'pad_low', reach=1, x=.4, y=.3, b=-.5, w=.2, mark='slide'), k(.78, 'pad_low', reach=.6, x=-.3, y=-.6, b=-.2, r=1), k(.92, eye='-')],
        [(.41, 'thin')], g='care', act=('pull', 'pads'), when=['pond_plants>.7'])
    o.r('look_over_the_torn_fin', 'Peering at the salmon\'s tail fin for a ragged edge from the last bad landing, bill almost touching the water', 22, 'none',
        [k(.07, x=.6, y=.2, b=.2), k(.2, 'run_l', x=1.6, y=2.3, b=1.4, eye='o'), k(.38, 'run_l', x=1.8, y=2.5, b=1.7, eye='O', l=1, mark='hm'), k(.55, 'run_m', x=1.5, y=2.1, b=1.3, r=1, mark='tsk'), k(.75, 'run_m', x=.7, y=.6, b=.3, w=.5, eye='^'), k(.9, eye='-')],
        [(.38, 'tend')], g='care', act=('peer', 'fin'), pick='shyest', when=['fish_health<.8'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        say=["Fin intact. Pride dented, which heals itself.", "Frayed at the tip. Join the club, mate."])
    o.r('beat_a_current_into_the_pond', 'Beating both wings flat on the pond to whip up a current that runs the length of the lane', 22, 'wing',
        [k(.06, 'run_l', reach=.4, x=.1, y=.1), k(.2, 'run_l', reach=1, x=.7, y=.9, b=-.8, l=1, mark='SPLSH'), k(.34, 'run_m', reach=1, x=.8, y=1, b=.5, r=1, mark='SPLSH'), k(.5, 'run_m', reach=1, x=.8, y=.9, b=-.9, l=1, mark='SPLASH'), k(.66, 'rapid', reach=1, x=.9, y=1, b=.4, r=1), k(.82, 'run_r', reach=1, x=.7, y=.8, b=-.6, l=1), k(.94, eye='@')],
        [(.5, 'churn')], g='care', act=('splash', 'current'), when=['pond_oxygen<.5'], prefer=['summer'],
        say=["River simulated. Fish is thrilled, duck is soaked.", "Made a current by hand. Got a free workout."])
    o.r('wipe_the_grit_off_the_snout', 'Wiping the grit off the salmon\'s hooked snout with the back of a wing as it noses up to the rim', 20, 'wing',
        [k(.12, 'run_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'run_l', reach=1, x=.4, y=1.4, b=1.1, mark='wp'), k(.5, 'run_l', reach=1, x=.3, y=1.6, b=1.3, l=1, mark='wp wp'),
         k(.7, 'run_l', reach=1, x=.3, y=1.3, b=1), k(.88, eye='^')],
        [(.5, 'tend')], g='care', act=('wipe', 'snout'), pick='hungriest', prefer=['fish_health<.9', 'happy'], obj=[(.28, dict(lure=1)), (.65, dict(lure=1))])
    o.r('tug_the_trailing_stem_out_of_the_murk', 'Tugging a trailing lily stem out of the clouded water with a reed so the lane runs clear again', 22, 'reed',
        [k(.12, 'bloom_r', reach=.5, x=.3, y=.3, b=.3), k(.3, 'pad_low', reach=1, x=.6, y=.7, b=.6, mark='grab'), k(.5, 'pad_low', reach=1, x=.9, y=.5, b=.9, l=1, r=1, mark='hff'),
         k(.7, 'tuft', reach=1, x=.3, y=.4, b=-.4, w=.4, mark='pop'), k(.88, eye='-')],
        [(.5, 'clear')], g='care', act=('tug', 'stem'), when=['pond_clarity<.6'])
    # ---------------- use
    o.r('throw_flakes_up_the_lane', 'Flinging a wingful of flakes up the lane so they drift down on the current into the waiting salmon', 18, 'wing',
        [k(.1, 'run_l', reach=.3, x=.2), k(.28, 'run_l', reach=.9, x=.4, y=-.3, b=.6), k(.46, 'run_m', reach=1, x=.6, y=-.9, b=-.8, mark='fwip'), k(.64, 'rapid', reach=.7, x=.2, y=-.4, b=-.2), k(.82, eye='o')],
        [(.46, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.3'], prefer=['dawn', 'dusk'], say=["Flakes up, salmon down. The usual physics.", "Dinner from upstream. Very authentic."])
    o.r('hold_a_flake_high_for_the_leap', 'Holding a flake pinched in his bill high above the water until the salmon launches up and snatches it', 22, 'none',
        [k(.12, x=.3, y=-.2, w=.2), k(.3, 'run_m', x=.9, y=-.5, b=-.2, eye='o', mark='...'), k(.46, 'run_m', x=1.2, y=-.9, b=-.5, w=.4, eye='O', mark='WHAP'), k(.64, x=-.7, y=.1, b=.3, w=.8, eye='>'),
         k(.84, eye='^')],
        [(.46, 'leap')], g='use', act=('lift', 'flake'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))],
        say=["Took it mid-air and left. Rude, impressive.", "Almost lost the bill. Worth it."])
    o.r('rap_the_cattail_dinner_bell', 'Rapping the left cattail three times with his bill, the evening bell the salmon swims to', 18, 'none',
        [k(.12, 'cattail_l', x=1.2, y=-.4, b=.2, mark='tok'), k(.3, 'cattail_l', x=1.3, y=-.5, b=.3, l=1, mark='tok'), k(.48, x=-.2, y=0, w=.2), k(.66, 'cattail_l', x=1.4, y=-.6, b=.4, r=1, mark='TOK'),
         k(.86, eye='^')],
        [(.66, 'call')], g='use', act=('tap', 'cattail'), when=['pond_bell<.4'], prefer=['dusk', 'dawn'])
    o.r('hand_feed_a_flake_at_the_rim', 'Holding one flake out in his bill just over the rim for the shy salmon to rise and take', 20, 'none',
        [k(.1, x=.2, y=.3), k(.26, 'run_l', x=1.7, y=2, b=.8, eye='o'), k(.44, 'run_l', x=1.9, y=2.2, b=.9, l=1, eye='O', mark='slurp'), k(.6, 'run_l', x=1.4, y=1.5, b=.5), k(.8, x=.5, y=.5, w=.3, eye='^')],
        [(.44, 'feed')], g='use', act=('carry', 'flake'), pick='shyest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1)), (.78, dict(lure=0))],
        say=["It took the flake and my full confidence.", "One flake. It looked at me like I owed it more."])
    o.r('draw_it_up_the_home_bank', 'Dragging a wingtip along the water toward the right bank so the salmon swims the way it remembers home', 26, 'wing',
        [k(.07, 'run_l', reach=.4, x=.3, y=.4), k(.22, 'run_l', reach=1, x=.7, y=.5, b=.7), k(.4, 'run_m', reach=1, x=.9, y=.5, b=.2, l=1), k(.58, 'rapid', reach=1, x=1.1, y=.5, b=.8, r=1), k(.76, 'bank_r', reach=1, x=1.3, y=.4, b=.3, l=1), k(.92, eye='^')],
        [(.4, 'lead')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['homing<.7'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.75, dict(lure=1))],
        say=["It knows the bank better than I do. I just hold the wing.", "Led it home. It would have gone anyway."])
    o.r('pat_the_silver_flank', 'Patting the salmon\'s silver flank with the back of a wing as it holds still against the rim', 20, 'wing',
        [k(.09, 'run_r', reach=.4, x=.1, y=.5, b=.2), k(.25, 'run_r', reach=.8, x=.5, y=1, b=.9, mark='pat'), k(.43, 'run_r', reach=1, x=.6, y=1.2, b=1, r=1, mark='pat'), k(.6, 'run_r', reach=1, x=.4, y=1, b=.7, l=1, mark='pat pat'), k(.78, 'run_r', reach=.5, x=.2, y=.6, b=.4), k(.92, eye='^')],
        [(.43, 'stroke')], g='use', act=('pat', 'flank'), pick='shyest', prefer=['fish_trust<.8', 'lonely'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))])
    o.r('raise_the_twig_hoop_for_a_leap', 'Raising a twig bent in a loop at arm\'s length over the water until the salmon sails through it', 24, 'twig',
        [k(.1, 'bloom_r', reach=.5, x=.2, y=-.1), k(.28, 'bloom_r', reach=1, x=.4, y=-.5, b=-.2, mark='hup'), k(.46, 'bloom_r', reach=1, x=.5, y=-.8, b=-.4, w=.4, mark='WHOOSH'),
         k(.66, 'pad_low', reach=1, x=.3, y=-.3, b=-.2), k(.86, eye='^')],
        [(.46, 'leap')], g='use', act=('lift', 'hoop'), pick='hungriest', prefer=['fish_trust>.4', 'happy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1))],
        say=["Through the hoop clean, not a drop touched. Show-off.", "Hoop work. This is why they give me a twig."])
    # ---------------- play
    o.r('race_the_leaps_along_the_bank', 'Racing the salmon along the bank, bounding after every leap it throws', 20, 'none',
        [k(.06, 'run_l', x=.6, y=.2, b=.2), k(.2, 'run_m', x=1.3, y=.3, b=-.8, l=1, w=.3), k(.35, 'rapid', x=1.6, y=.2, b=.4, r=1, w=.6), k(.5, 'run_r', x=1.9, y=.3, b=-1, l=1, w=.8, mark='hup'), k(.66, 'bank_r', x=1.4, y=.3, b=.3, r=1, w=.5), k(.84, 'bank_r', x=.4, y=.5, b=.6, eye='@')],
        [(.5, 'fun')], g='play', act=('race', 'bank'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=1))],
        say=["Lost by four leaps. It cheats with vertical.", "Raced a fish. Lost to the one with fins."])
    o.r('kick_spray_back_at_the_leaper', 'Kicking the spray back at the salmon off the front stone, a foot flicking out after every splash', 18, 'none',
        [k(.12, 'stone_m', x=.4, y=.4, b=.3, l=1), k(.3, 'stone_m', x=.6, y=.1, b=-.6, r=1, w=.4, mark='fwsh'), k(.5, 'stone_m', x=.5, y=.2, b=-.7, l=1, w=.5, mark='fwsh'),
         k(.7, 'stone_m', x=.4, y=.3, b=.2, r=1), k(.88, eye='@')],
        [], g='play', act=('kick', 'spray'), prefer=['young', 'curious'], when=['spray>.3'])
    o.r('hop_with_every_leap', 'Hopping in step with each leap, wings out, trying to clear the same height from the stone', 20, 'none',
        [k(.1, 'stone_r', x=.3, y=.3, b=.3), k(.24, 'stone_r', x=.4, y=-.2, b=-1.2, w=.8, l=1, r=1), k(.4, 'stone_r', x=.4, y=.8, b=.9), k(.56, 'stone_r', x=.5, y=-.3, b=-1.5, w=1, l=1, r=1, mark='HUP'),
         k(.74, 'stone_r', x=.3, y=.9, b=1), k(.9, eye='>')],
        [], g='play', act=('hop', 'step'), pick='hungriest', prefer=['young', 'happy'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('push_a_leaf_boat_against_the_run', 'Pushing a fallen leaf upstream with a wing and watching the current bring it right back past him', 24, 'wing',
        [k(.12, 'run_r', reach=.5, x=.3, y=.5, b=.3), k(.3, 'run_m', reach=1, x=.5, y=.8, b=.6, mark='shff'), k(.5, 'rapid', reach=1, x=.6, y=.9, b=.7, l=1), k(.7, 'run_m', reach=1, x=.7, y=.7, b=.5, r=1, mark='boop'),
         k(.88, eye='o')],
        [], g='play', act=('push', 'leaf'), when=['pond_leaves>.2'], pick='shyest', prefer=['curious'], obj=[(.55, dict(lure=1)), (.8, dict(lure=1))])
    o.r('chase_the_silver_glint', 'Chasing the silver glint that flickers over the pads with a wing, never quite pinning it', 18, 'wing',
        [k(.12, 'run_l', reach=.7, x=.4, y=.7, b=.5), k(.3, 'pad_low', reach=1, x=.9, y=.5, b=.3, l=1, mark='fwp'), k(.5, 'bloom_r', reach=1, x=-.5, y=.4, b=.5, r=1, mark='fwp'),
         k(.7, 'pad_low', reach=1, x=.9, y=.6, b=.4, l=1), k(.88, y=.4, eye='@')],
        [], g='play', act=('chase', 'glint'), prefer=['curious', 'young'], when=['spray>.3'])
    o.r('jig_on_the_stone_for_the_run', 'Jigging on the middle stone, wings flapping to a beat while the run goes on below him', 22, 'none',
        [k(.1, 'stone_m', x=.3, y=.3, b=.4, perch=1), k(.26, 'stone_m', x=.4, y=-.3, b=-.7, w=.8, l=1, perch=1), k(.42, 'stone_m', x=.4, y=.6, b=.9, w=.2, r=1, perch=1),
         k(.58, 'stone_m', x=.4, y=-.4, b=-.8, w=1, l=1, perch=1, mark='hup'), k(.74, 'stone_m', x=.3, y=.5, b=.8, r=1, perch=1), k(.9, 'stone_m', x=.2, y=.2, b=.3, perch=1, eye='^')],
        [(.58, 'fun')], g='play', act=('dance', 'stone'), prefer=['happy', 'young'], when=['run>.3'])
    # ---------------- test
    o.r('measure_the_leap_on_the_cattail', 'Measuring the height of the leap against the tall left cattail with a reed notched at each splash', 24, 'reed',
        [k(.12, 'tuft', reach=.5, x=.3, y=.4, b=.3), k(.3, 'reed_low', reach=1, x=.5, y=.6, b=.5), k(.5, 'cattail_l', reach=1, x=.6, y=-.4, b=-.2, mark='mark'), k(.7, 'cattail_l', reach=1, x=.5, y=-.7, b=-.4, w=.3, mark='more'),
         k(.9, eye='O', mark='huge')],
        [], g='test', act=('measure', 'leap'), prefer=['curious'], when=['spray>.3'], say=["Four of me, straight up. I am not the unit that matters.", "Notched the reed. Salmon notched the sky."])
    o.r('count_the_leaps_from_the_stone', 'Counting each leap out loud with a bill dip, losing the number at the fourth', 20, 'none',
        [k(.1, 'run_m', x=.7, y=.9, b=.5, mark='1'), k(.26, 'run_m', x=.8, y=1, b=.6, mark='2'), k(.42, 'rapid', x=.9, y=1, b=.6, l=1, mark='3'), k(.6, 'rapid', x=.9, y=1.1, b=.7, r=1, mark='5?'),
         k(.8, eye='-', mark='lost')],
        [], g='test', act=('count', 'leaps'), pick='hungriest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('feel_which_way_the_water_pulls', 'Holding a wingtip just over the surface to feel which way the current pulls and how hard', 22, 'wing',
        [k(.12, 'run_l', reach=.5, x=.2, y=.6, b=.4), k(.3, 'run_l', reach=1, x=.3, y=.9, b=.7), k(.5, 'run_m', reach=1, x=.4, y=1, b=.8, mark='tug'), k(.7, 'run_r', reach=1, x=.4, y=1, b=.8, l=1),
         k(.9, eye='o')],
        [], g='test', act=('test', 'current'), when=['run>.3'], prefer=['curious'])
    o.r('peer_at_the_scale_sheen', 'Peering close at the scale sheen as the salmon turns, to see whether the red is coming in yet', 20, 'none',
        [k(.12, x=.3, y=.6, b=.5), k(.3, 'run_r', x=1, y=1.5, b=1, eye='o'), k(.5, 'run_r', x=1.1, y=1.7, b=1.2, eye='O', mark='...'), k(.7, 'run_r', x=.5, y=.8, b=.5, w=.5, eye='>'), k(.9, eye='-')],
        [], g='test', act=('peer', 'scales'), pick='shyest', prefer=['curious', 'happy'], obj=[(.28, dict(lure=1)), (.6, dict(lure=1))])
    o.r('listen_for_the_slap_of_the_landing', 'Listening with a tilted head at the rim for the flat slap that tells how far a leap carried', 20, 'none',
        [k(.12, x=-.2, y=.7, b=.5), k(.3, 'stone_l', x=-.6, y=1.5, b=1.1, eye='-'), k(.55, 'stone_l', x=-.7, y=1.7, b=1.3, eye='-', mark='...'), k(.76, 'stone_l', x=-.3, y=.8, b=.5, eye='o'), k(.9, eye='^')],
        [], g='test', act=('listen', 'slap'), prefer=['curious', 'dusk'])
    o.r('taste_the_spray_off_his_bill', 'Licking the spray off his bill to taste whether the home stream is in it', 16, 'none',
        [k(.15, 'cove', x=.5, y=.8, b=.4), k(.35, 'cove', x=.6, y=1, b=.6, mark='sp'), k(.55, x=-.5, y=-.4, b=-.3, w=.4, eye='-', mark='hm'), k(.75, x=.1, y=.3, eye='>'), k(.9, eye='-')],
        [], g='test', act=('taste', 'spray'), when=['spray>.3'], prefer=['curious'])
    o.r('set_his_hop_against_the_leap', 'Setting his own best hop beside the salmon\'s leap and comparing the two against the cattail', 22, 'wing',
        [k(.12, 'tuft', reach=.5, x=.3, y=.4, b=.3), k(.3, 'reed_low', reach=1, x=.4, y=.6, b=.5), k(.5, 'cattail_l', reach=1, x=.5, y=-.3, b=-.8, w=.6, mark='me'), k(.7, 'cattail_l', reach=1, x=.5, y=-.6, b=-.2, mark='it'),
         k(.9, eye='-', mark='ok')],
        [], g='test', act=('compare', 'height'), pick='hungriest', prefer=['curious', 'young'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- rest
    o.r('nap_on_the_warm_middle_stone', 'Dozing on the middle stone with a wing over his bill while the salmon sleeps off the morning run', 26, 'none',
        [k(.1, 'stone_m', x=.4, y=1.1, b=1.2, eye='-', perch=1), k(.3, 'stone_m', x=-.9, y=2, b=1.9, eye='-', perch=1), k(.6, 'stone_m', x=-1.1, y=2.4, b=2.5, eye='-', mark='zzz', perch=1), k(.8, 'stone_m', x=-.4, y=1, b=1, eye='o', perch=1), k(.92, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'stone'), when=['tired'], prefer=['fish_hunger>.4'])
    o.r('sit_at_the_tuft_for_the_dusk_run', 'Sitting at the tuft with his feet folded to watch the dusk run begin', 24, 'none',
        [k(.1, 'tuft', x=.5, y=.3, b=.4), k(.3, 'tuft', x=.1, y=.7, b=1, l=1, eye='-'), k(.55, 'tuft', x=-.1, y=.9, b=1.8, eye='-', mark='...'), k(.76, 'tuft', x=.4, y=.3, b=.6, r=1, eye='o'), k(.9, eye='^')],
        [(.55, 'rest')], g='rest', act=('sit', 'tuft'), when=['dusk'], prefer=['tired', 'lonely'])
    o.r('wait_for_the_first_leap', 'Waiting stock-still at the rim for the first leap of the morning to break the water', 22, 'none',
        [k(.1, 'run_m', x=1, y=1, b=.5, eye='o'), k(.3, 'run_m', x=1.2, y=1.2, b=.7, eye='o'), k(.5, 'run_m', x=1.2, y=1.2, b=.7, l=1), k(.68, 'run_m', x=1.4, y=1.6, b=1.1, eye='O', mark='...'), k(.86, 'run_m', x=.3, y=.4, b=.3, eye='^')],
        [], g='rest', act=('wait', 'leap'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('lean_on_the_left_cattail', 'Leaning his shoulder against the left cattail stem, bill toward the water, letting the run go by', 20, 'none',
        [k(.08, 'cattail_l', x=-.5, y=.2, b=.3), k(.24, 'cattail_l', x=-.9, y=.5, b=.7, l=1, eye='-'), k(.46, 'cattail_l', x=-1, y=.7, b=1.1, eye='-', mark='hm'), k(.66, 'cattail_l', x=-.7, y=.6, b=.8, r=1), k(.84, x=.5, y=.2, b=.2, eye='O')],
        [], g='rest', act=('lean', 'cattail'), prefer=['tired', 'sad'])
    o.r('sulk_when_it_will_not_jump', 'Sulking with his back to the pond because the salmon has been low all day and will not jump for anyone', 22, 'none',
        [k(.08, x=-.9, y=.5, b=.6), k(.25, 'run_r', x=-1.8, y=1.2, b=1.1, eye='-'), k(.46, 'run_r', x=-2.2, y=1.6, b=1.7, eye='-', mark='tsk'), k(.64, 'run_r', x=-2, y=1.5, b=1.5, l=1), k(.84, x=-.7, y=.4, b=.4, eye='-')],
        [], g='rest', act=('sulk', 'pond'), when=['sad'])
    # ---------------- weather
    o.r('chip_the_ice_off_the_run', 'Chipping the ice back from the rim so the salmon has an open stretch to run in', 22, 'none',
        [k(.06, 'stone_l', x=.5, y=.7, b=.2), k(.2, 'run_l', x=1.5, y=2, b=.6, mark='tk'), k(.36, 'run_l', x=1.7, y=2.4, b=1, r=1, mark='TK'), k(.5, 'run_m', x=1.5, y=2.2, b=.8, l=1, mark='crk'), k(.66, 'run_m', x=1.7, y=2.4, b=1.1, r=1, mark='CRK'), k(.84, x=.4, y=.2, eye='^')],
        [(.5, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('scrape_the_frost_off_the_middle_stone', 'Scraping the white frost off the middle stone with a wing so his footing is clean for the morning run', 18, 'wing',
        [k(.09, 'stone_m', reach=.4, x=.1, y=.5, b=.2), k(.27, 'stone_m', reach=1, x=.8, y=1.6, b=1.1, l=1, mark='skrr'), k(.45, 'stone_m', reach=1, x=1, y=1.7, b=1.2, mark='skrrr'), k(.63, 'stone_r', reach=1, x=.7, y=1.4, b=.9, r=1), k(.8, 'stone_r', reach=.5, x=.2, y=.5, b=.3), k(.92, eye='-')],
        [(.45, 'thaw')], g='weather', act=('scrape', 'frost'), when=['pond_ice>.3'])
    o.r('stand_out_the_rain_by_the_cattail', 'Sheltering with his bill tucked at the low reed while the rain pocks the lane and the salmon keeps leaping through it', 30, 'none',
        [k(.09, 'reed_low', x=-.6, y=.6, b=.7), k(.27, 'reed_low', x=-1.1, y=1.7, b=1.5, eye='-'), k(.5, 'reed_low', x=-1.3, y=1.9, b=1.8, l=1, eye='-', mark='pit pat'), k(.72, 'reed_low', x=-1.2, y=1.8, b=1.7, r=1, mark='drip'), k(.9, x=.1, y=.2, b=.2, eye='^')],
        [], g='weather', act=('shelter', 'reed'), when=['wet'])
    o.r('warm_a_foot_on_the_sunny_stone', 'Warming one foot and then the other at the sunny right stone while the salmon idles along the lane', 18, 'none',
        [k(.1, 'stone_r', x=.4, y=.4, b=.8, l=1), k(.3, 'stone_r', x=.3, y=.7, b=1.1, l=1, eye='-'), k(.52, 'stone_r', x=.3, y=.7, b=1.1, r=1, eye='-', mark='mm'), k(.72, 'stone_r', x=.4, y=.4, b=.5, w=.3, eye='^')],
        [], g='weather', act=('warm', 'foot'), when=['sun'], prefer=['tired'])
    o.r('brace_against_the_gust_at_the_bank', 'Bracing his chest into the gust at the right bank so the ripples run flat past the salmon', 18, 'none',
        [k(.07, 'bank_r', x=1, y=.1, b=1), k(.22, 'bank_r', x=1.5, y=.4, b=1.5, w=.4, mark='whoo'), k(.4, 'bank_r', x=1.7, y=.5, b=1.7, l=1, w=.9), k(.58, 'bank_r', x=1.5, y=.3, b=1.3, r=1, w=.6), k(.76, 'bank_r', x=.9, y=.2, b=.8), k(.9, eye='-')],
        [], g='weather', act=('brace', 'gust'), when=['windy'])
    o.r('shake_the_spray_out_of_his_wings', 'Shaking the spray out of his feathers after a landing splash, a full-body shudder from bill to tail', 16, 'none',
        [k(.12, 'stone_l', x=.3, y=.4, b=.3), k(.28, 'stone_l', x=-.6, y=.2, b=-.5, w=1, l=1, mark='brrr'), k(.44, 'stone_l', x=.7, y=.6, b=.7, w=.8, r=1, mark='brrr'), k(.6, 'stone_l', x=-.5, y=.1, b=-.4, w=1, l=1, r=1),
         k(.82, eye='-')],
        [], g='weather', act=('shake', 'spray'), when=['wet'], prefer=['spray>.3'])
    # ---------------- show
    o.r('bow_to_the_high_leaper', 'Bowing low to the salmon as it tops out its leap and drops back, a bill-dip at the rim', 16, 'none',
        [k(.1, 'run_m', x=.9, y=1.2, b=.9), k(.3, 'run_m', x=1.4, y=2.6, b=2.1, eye='-'), k(.52, 'run_m', x=1.5, y=2.8, b=2.2, eye='-', mark='sir'), k(.7, 'run_m', x=.8, y=.7, b=.6), k(.88, x=.1, y=-.5, w=.7, eye='^')],
        [], g='show', act=('bow', 'leaper'), pick='hungriest', prefer=['happy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed. It dripped on my head. A blessing.", "Gave it the bow. It gave me spray."])
    o.r('present_the_leap_to_nobody', 'Sweeping a wing up and out to present the leap to the empty bank, like a ringmaster with a very wet circus', 20, 'wing',
        [k(.08, 'run_r', reach=.4, x=.1, y=.1), k(.26, 'run_r', reach=.9, x=.3, y=-.6, b=-.6), k(.44, 'run_m', reach=1, x=.2, y=-.9, b=-.8, mark='tadaa'), k(.62, 'run_l', reach=1, x=.3, y=-.7, b=-.5, l=1), k(.8, 'run_l', reach=.6, x=.5, y=-.1, b=.1), k(.92, eye='^')],
        [], g='show', act=('present', 'leap'), pick='shyest', prefer=['happy'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_over_who_jumps_higher', 'Arguing nose to bill over who jumps higher, jabbing a wing at the water between squawks', 20, 'wing',
        [k(.09, 'run_m', reach=.4, x=.7, y=.2, b=.2), k(.25, 'run_m', reach=1, x=1.3, b=-.1, mark='NO'), k(.41, 'run_m', reach=1, x=1.5, y=-.1, b=-.3, l=1, mark='NO!'), k(.57, 'run_m', reach=.7, x=.6, y=.5, b=.6, r=1), k(.73, 'run_m', reach=1, x=1.4, y=-.1, b=-.2, mark='NOPE'), k(.9, eye='-')],
        [], g='show', act=('argue', 'height'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Twelve to nothing, and it still disputes the scoring.", "Lost to a fish. A fish with no legs."])
    o.r('pose_on_the_stone_mid_leap', 'Freezing in a mid-leap pose on the left stone, wings flung up, while the salmon is the real thing below him', 18, 'none',
        [k(.12, 'stone_l', x=.3, y=-.2, w=.4, perch=1), k(.3, 'stone_l', x=.5, y=-.5, b=-.5, w=.8, perch=1), k(.6, 'stone_l', x=.6, y=-.7, b=-.8, w=1, perch=1, eye='^', mark='ta-da'), k(.85, 'stone_l', x=.2, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'stone'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sing_the_run_up_the_river', 'Singing the run up the river in a slow low voice, a bill-bob for every leap that answers', 22, 'none',
        [k(.08, 'run_r', x=1, y=1.2, b=1), k(.26, 'run_r', x=1.4, y=2, b=1.7, eye='-', mark='la'), k(.44, 'rapid', x=1.5, y=2.3, b=2, eye='-', mark='laaa', w=.4), k(.62, 'run_l', x=1.4, y=1.9, b=1.6, eye='-', mark='la'), k(.8, x=.3, y=.4, b=.3, eye='^')],
        [], g='show', act=('sing', 'run'), pick='shyest', prefer=['lonely', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))], say=["It leapt on the high note. Critics will call it feedback.", "Sang upstream. Nobody was listening, except the fish."])
    # ---------------- mishap
    o.r('slip_on_the_wet_front_stone', 'Slipping on the wet right stone, both feet out, and catching the rim with a flap of wings', 16, 'none',
        [k(.08, 'stone_r', x=.7, y=.7, b=.7), k(.22, 'stone_r', x=1.4, y=-.3, b=-.9, l=1, r=1, w=1, mark='whoa!'), k(.36, 'stone_r', x=1.6, y=1.4, b=1.8, w=.7, eye='O', mark='THUD'), k(.56, 'stone_r', x=.6, y=.8, b=.9, eye='>'), k(.74, x=.2, y=.2, b=.2, eye='-')],
        [], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('jammed_between_two_cattail_stems', 'Jamming his head between two cattail stems chasing a glimpse of silver and hauling himself back out', 24, 'none',
        [k(.07, x=.8, y=.6, b=.6), k(.2, 'reed_low', x=1.8, b=1, eye='O'), k(.38, 'reed_low', x=2, y=.1, b=1.3, l=1, eye='@', mark='mmph'), k(.56, 'reed_low', x=1.9, y=.2, b=1.2, r=1, w=.5, mark='mf'), k(.7, 'reed_low', x=1.4, y=-.4, b=-.9, w=1, mark='POP'), k(.86, x=1.2, y=1, b=.8, eye='-')],
        [], g='mishap', act=('stuck', 'stems'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_cattail_watching_the_sky', 'Striding along the bank with his bill in the air for the next leap and meeting the cattail head on', 20, 'none',
        [k(.12, 'run_l', x=.3, y=-.6, b=.2), k(.3, 'tuft', x=.4, y=-.8, b=.3, l=1), k(.5, 'cattail_l', x=1.3, y=-.3, b=1.3, eye='@', mark='BONK'), k(.7, 'reed_low', x=-.8, y=.4, b=.4, w=.6, eye='x'),
         k(.88, y=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'cattail'), prefer=['curious'])
    o.r('flinch_when_it_leaps_at_his_face', 'Hopping back when the salmon rockets out of the water at his bill and drenches him head to foot', 16, 'none',
        [k(.08, 'run_l', x=1.2, y=1.8, b=.9), k(.22, 'run_l', x=1.5, y=2.1, b=1.2, eye='o', mark='...'), k(.34, x=-1.5, y=-1, b=-1.6, l=1, r=1, w=1, eye='O', mark='AAH'), k(.5, x=-.9, y=.1, b=-.2, w=.6, eye='>'), k(.7, x=.1, y=.4, b=.3, eye='-')],
        [], g='mishap', act=('hop', 'face'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))],
        say=["Cold, wet and entirely on purpose.", "It leapt. I flew. Physics split the difference."])
    o.r('stamp_at_the_scattered_spray', 'Stamping at the spray drifting over the stone as if the pond could be ordered back to calm', 16, 'none',
        [k(.1, 'stone_r', x=.6, y=.7, b=.3), k(.2, 'stone_r', x=.4, y=0, b=-1.1, l=1, mark='STMP'), k(.3, 'stone_r', x=.5, y=.5, b=.5), k(.42, 'stone_r', x=.4, y=0, b=-1.1, r=1, mark='STMP'),
         k(.58, 'stone_r', x=.5, y=.5, b=.5), k(.86, eye='-')],
        [(.42, 'calm')], g='mishap', act=('stamp', 'spray'), prefer=['grumpy'], when=['run>.3'])
    # ---------------- duets (a friend takes their own part)
    o.r('herd_it_up_the_lane_from_both_banks', 'Walking the salmon up the lane with a friend on the far stone, wings sweeping it forward from both banks', 24, 'wing',
        [k(.1, 'run_l', reach=.6, x=.3, y=.5, b=.3), k(.28, 'run_m', reach=1, x=.5, y=.6, b=.5, l=1, mark='shoo'), k(.46, 'rapid', reach=1, x=.6, y=.6, b=.5, r=1, mark='shoo'),
         k(.66, 'run_r', reach=1, x=.7, y=.6, b=.5, l=1), k(.86, eye='^')],
        [(.46, 'lead')], g='use', act=('guard', 'lane'), pick='hungriest', when=['homing<.7'], prefer=['happy'], obj=[(.2, dict(lure=1)), (.48, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.12, 'bank_r', x=.3, y=.4, b=.3), k(.3, 'bank_r', x=.8, y=.7, b=.6, l=1, mark='shoo'), k(.5, 'run_r', x=.9, y=.8, b=.7, r=1, mark='shoo'), k(.7, 'rapid', x=.9, y=.8, b=.7, l=1), k(.86, eye='^')],
        say=["Two ducks, one fish, no argument. It is going upstream anyway.", "Herded it a metre. It would have gone ten."])
    o.r('toss_a_flake_between_us_for_the_leap', 'Tossing a flake back and forth with a friend over the lane so the salmon launches at it each time', 24, 'none',
        [k(.07, 'run_l', x=.6, y=.1, b=.1), k(.2, 'run_l', x=1.3, y=-.9, b=-1.2, w=.7, l=1, mark='fwip'), k(.34, 'run_m', x=1.4, y=.6, b=.8, eye='o'), k(.48, 'run_m', x=1.2, y=-.9, b=-1.2, w=.7, r=1, mark='fwip'), k(.64, 'run_m', x=1.4, y=.7, b=.9, eye='O'), k(.82, eye='^')],
        [(.34, 'leap')], g='play', act=('throw', 'flake'), pick='hungriest', prefer=['happy', 'young'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.12, 'run_r', x=.4, y=.3, b=.3), k(.3, 'run_r', x=1, y=.4, b=.5, eye='o'), k(.46, 'run_m', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.62, 'run_r', x=1, y=.4, b=.5), k(.8, eye='^')])
    o.r('judge_the_leaps_with_a_friend', 'Scoring each leap with a friend at the other end of the rim, wing up for a number and wing down for a groan', 24, 'wing',
        [k(.1, 'run_l', reach=.5, x=.4, y=.2, b=.3), k(.26, 'run_l', reach=1, x=.5, y=-.3, b=-.2, mark='9'), k(.42, 'run_l', reach=1, x=.5, y=.5, b=.5, mark='6'), k(.6, 'run_l', reach=1, x=.5, y=-.4, b=-.3, mark='10!'),
         k(.8, eye='^')],
        [], g='show', act=('show', 'scores'), pick='shyest', prefer=['happy', 'curious'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.15, 'run_r', x=.4, y=.2, b=.3), k(.34, 'run_r', x=.5, y=-.3, w=.9, mark='8'), k(.5, 'run_r', x=.5, y=.5, b=.5, mark='4'), k(.68, 'run_r', x=.5, y=-.4, w=.9, mark='10'), k(.84, eye='^')],
        say=["Ten from me, nine from the other judge. Fish gets zero for tripping on the landing.", "Scored it. It was a ten. The fish does not know scoring."])
    return done(o)


def trout():
    # Trout: small, spotted, spooky, mid-water, active at morning, jumpy: rises in quick flurries at dawn. Own state: rise (how ready it is to rise: builds at dawn,
    # falls after), rings (the rings a rise leaves on the water: drawn), spook (how wary it is of Cheese: clumsy noise raises it, stillness settles it).
    o = Obj('trout', 'keeping', on='koi_pond',
            fields=dict(rise=(0, 0, 1), rings=(0, 0, 1), spook=(0, 0, 1)),
            physics=[('rise', 'rate', .003, 'dawn'), ('rise', 'rate', -.002, '!dawn'), ('rings', 'rate', -.005, 'always'), ('spook', 'rate', -.0004, 'always')],
            effects=dict(scoop=[('keeping.leaves', 'mul', .35)], rake=[('keeping.algae', 'mul', .5)], shove=[('keeping.plants', 'mul', .75)], sweep=[('keeping.flakes', 'mul', .3)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], air=[('keeping.oxygen', 'add', .3)],
                         sprinkle=[('keeping.flakes', 'add', .35), ('rise', 'add', .2)], call=[('keeping.bell', 'add', .5)],
                         flurry=[('rings', 'set', 1), ('subject.hunger', 'add', -.2), ('rise', 'mul', .5)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)],
                         dimple=[('rings', 'set', 1), ('subject.mood', 'add', .15)], settle=[('spook', 'mul', .3), ('subject.trust', 'add', .1)],
                         scare=[('spook', 'set', 1)], tickle=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         crack=[('keeping.ice', 'mul', .3)], clear=[('keeping.ice', 'mul', .6)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('rings', .3, 'o O o', 'glide', 'water'), ('pond_flakes', .3, '.:.:.', 'edge_far', 'dust'), ('pond_leaves', .3, ';"~;"', 'shelf', 'leaf'),
                   ('pond_ice', .3, '*-*-*', 'rise_l', 'frost'), ('pond_algae', .3, '"v"v"', 'stone_r', 'plant')],
            anchors=dict(rise_l=P(28, 43), glide=P(58, 41), rise_r=P(88, 39), edge_far=P(70, 43), shelf=P(40, 39), mud_edge=P(48, 43), pad_low=P(86, 37), bloom_r=P(81, 35),
                         cattail_l=P(7, 31), reed_low=P(8, 38), tuft=P(11, 44), bank_r=P(95, 40),
                         stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('dip_the_net_reed_for_leaves', 'Dipping a reed in and out along the shelf to scoop the sodden leaves out before they cloud the cold water', 22, 'reed',
        [k(.05, 'rise_r', reach=.4, x=.5, y=.2), k(.19, 'shelf', reach=1, x=.9, y=1.2, b=.9, l=1), k(.33, 'shelf', reach=.5, x=.2, y=.2, b=-.3, mark='lift'), k(.48, 'mud_edge', reach=1, x=1, y=1.3, b=1, r=1),
         k(.62, 'mud_edge', reach=.6, x=.3, y=.1, b=-.4, mark='flip'), k(.8, 'tuft', reach=.7, x=.6, y=.6, b=.3), k(.93, eye='^')],
        [(.62, 'scoop')], g='care', act=('scoop', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'],
        say=["Leaves out. Trout rose to check my work, then left a review of ripples.", "Scooped the soggy ones first. Trout hate soggy."])
    o.r('rake_the_algae_off_the_shelf', 'Raking the green fuzz off the shallow shelf with a reed, short strokes toward himself', 20, 'reed',
        [k(.07, 'shelf', reach=.6, x=.4, y=.5, b=.3), k(.2, 'shelf', reach=1, x=1.1, y=.9, b=.5, l=1, mark='rk'), k(.32, 'shelf', reach=.8, x=.4, y=.5, b=.9, mark='rk'), k(.46, 'shelf', reach=1, x=1.2, y=1, b=.6, r=1, mark='rk'),
         k(.6, 'shelf', reach=.8, x=.5, y=.6, b=1), k(.78, 'rise_l', reach=1, x=.9, y=.9, b=.5), k(.92, eye='-')],
        [(.46, 'rake')], g='care', act=('rake', 'shelf'), when=['pond_algae>.4'])
    o.r('nudge_the_left_pad_aside_for_light', 'Nudging the left pad aside with a twig so the cold lane gets its morning light back', 22, 'twig',
        [k(.06, 'bloom_r', reach=.3, x=.1, y=0), k(.22, 'bloom_r', reach=.9, x=.7, y=.4, b=-.2), k(.4, 'pad_low', reach=1, x=1.3, y=.8, b=.3, l=1, r=1, mark='shove'), k(.58, 'pad_low', reach=1, x=1.5, y=1, b=.6, mark='shove'),
         k(.76, 'bloom_r', reach=.5, x=.4, y=.2, b=-.1), k(.92, eye='^')],
        [(.58, 'shove')], g='care', act=('push', 'pad'), when=['pond_plants>.7'])
    o.r('sweep_the_flake_skin_off_the_top', 'Sweeping the left-over flake skin off the surface with the flat of a wing before it sours', 18, 'wing',
        [k(.08, 'rise_r', reach=.5, x=.6, y=.5, b=.2), k(.24, 'glide', reach=1, x=.8, y=.7, b=.6, mark='sw'), k(.4, 'edge_far', reach=1, x=1.1, y=.8, b=.9, l=1, mark='sw'), k(.56, 'rise_l', reach=1, x=.9, y=.7, b=.5, r=1),
         k(.74, 'rise_l', reach=.5, x=.3, y=.3, b=.2), k(.9, eye='-')],
        [(.4, 'sweep')], g='care', act=('sweep', 'flakes'), when=['pond_flakes>.3'])
    o.r('look_the_spots_over_for_pale_patches', 'Peering at the speckled flanks for any pale patch, turning his head side to side at the rim', 22, 'none',
        [k(.05, x=.3, y=.4, b=.2), k(.17, 'rise_l', x=1.4, y=1.9, b=1.1, eye='o'), k(.3, 'rise_l', x=1.2, y=2.1, b=1.3, r=1, eye='O'), k(.46, 'rise_l', x=1.6, y=2.1, b=1.2, l=1, mark='hm'),
         k(.62, 'glide', x=1.3, y=1.8, b=1), k(.78, x=.5, y=.5, b=.3, w=.4, eye='^'), k(.9, eye='-')],
        [(.46, 'tend')], g='care', act=('peer', 'spots'), pick='shyest', when=['fish_health<.8'], obj=[(.2, dict(lure=1)), (.62, dict(lure=1))],
        say=["Spots all accounted for. I counted twice, at the rim of shame.", "No pale patches. Healthier than my last three weeks."])
    o.r('kick_the_water_awake_with_a_foot', 'Kicking the surface in short wet kicks from the front stone until the sluggish water wakes and bubbles', 20, 'none',
        [k(.06, 'stone_l', x=.5, y=.5, b=.3, l=1), k(.2, 'rise_l', x=.9, y=1.2, b=.4, l=1, w=.3, mark='plsh'), k(.34, 'rise_l', x=.9, y=1.2, b=.3, r=1, w=.5, mark='plsh'), k(.5, 'glide', x=1, y=1.3, b=.5, l=1, w=.3, mark='PLSH'),
         k(.68, 'glide', x=.9, y=1.2, b=.4, r=1, w=.5, mark='PLSH'), k(.86, eye='@')],
        [(.5, 'air')], g='care', act=('kick', 'ripples'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('wipe_the_lip_clean_of_grit', 'Wiping the grit from the trout\'s upturned lip with a feather-edge of wing while it hangs at the surface', 20, 'wing',
        [k(.07, 'glide', reach=.4, x=.3, y=.7, b=.3), k(.22, 'glide', reach=.9, x=.5, y=1.3, b=.9, mark='wp'), k(.4, 'glide', reach=1, x=.6, y=1.5, b=1.2, r=1, mark='wp'), k(.55, 'glide', reach=1, x=.5, y=1.3, b=1, l=1),
         k(.72, 'glide', reach=.5, x=.2, y=.7, b=.4), k(.9, eye='^')],
        [(.4, 'tend')], g='care', act=('wipe', 'lip'), pick='hungriest', prefer=['fish_health<.9', 'happy'], obj=[(.2, dict(lure=1)), (.55, dict(lure=1)), (.8, dict(lure=1))])
    # ---------------- use
    o.r('sprinkle_flakes_a_pinch_at_a_time', 'Sprinkling flakes a pinch at a time down the glide so the trout has to rise for each one', 22, 'wing',
        [k(.06, 'rise_r', reach=.3, x=.2, w=.2), k(.18, 'glide', reach=.9, x=.5, y=-.2, b=.3, mark='pt'), k(.3, 'glide', reach=.5, x=.1, y=.1, b=-.2), k(.43, 'edge_far', reach=.9, x=.5, y=-.3, b=.3, mark='pt'),
         k(.55, 'edge_far', reach=.5, x=.1, y=.1, b=-.2), k(.68, 'rise_l', reach=.9, x=.5, y=-.2, b=.3, mark='pt'), k(.85, eye='o')],
        [(.43, 'sprinkle')], g='use', act=('pour', 'flakes'), when=['pond_flakes<.3'], prefer=['dawn'], say=["Pinch, rise. Pinch, rise. It is bossing me about.", "A flake at a time. Dinner as a dance with a leash."])
    o.r('tap_three_quick_on_the_front_stone', 'Tapping three quick beats on the middle stone with a toe, the dawn bell the trout knows', 16, 'none',
        [k(.08, 'stone_m', x=.5, y=.7, b=.6, l=1), k(.2, 'stone_m', x=.6, y=.9, b=.9, r=1, mark='tk'), k(.32, 'stone_m', x=.5, y=.8, b=.7, l=1, mark='tk'), k(.44, 'stone_m', x=.6, y=.9, b=.9, r=1, mark='TK'),
         k(.6, x=.2, y=.2, b=.2, w=.3), k(.84, eye='^')],
        [(.44, 'call')], g='use', act=('tap', 'stone'), when=['pond_bell<.4'], prefer=['dawn'])
    o.r('let_a_crumb_slide_off_the_bill', 'Letting a single crumb slide off the very tip of his bill into the open mouth of the trout at the rim', 20, 'none',
        [k(.06, x=.3, y=.5, b=.3), k(.2, 'rise_r', x=1.5, y=1.9, b=.8, eye='o'), k(.36, 'rise_r', x=1.8, y=2.3, b=1, eye='O', mark='...'), k(.5, 'rise_r', x=1.7, y=2.1, b=.9, l=1, mark='plip'),
         k(.66, 'rise_r', x=.9, y=1, b=.5, w=.4), k(.84, eye='^')],
        [(.5, 'feed')], g='use', act=('tip', 'crumb'), pick='shyest', when=['fish_hunger>.4'], obj=[(.2, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=0))],
        say=["Took it and a bit of my nerve.", "Crumb accepted. Dignity declined."])
    o.r('dimple_the_surface_with_a_twig', 'Dimpling the surface with a twig tip in a slow rhythm until the trout comes up to see what is rising', 24, 'twig',
        [k(.07, 'glide', reach=.5, x=.3, y=.2), k(.2, 'glide', reach=1, x=.6, y=.6, b=.3, mark='dp'), k(.32, 'glide', reach=.7, x=.4, y=.3, b=.1), k(.46, 'glide', reach=1, x=.7, y=.7, b=.4, mark='dp'),
         k(.6, 'glide', reach=.7, x=.4, y=.3, b=.1), k(.74, 'glide', reach=1, x=.8, y=.8, b=.5, l=1, mark='DP'), k(.9, eye='o')],
        [(.74, 'dimple')], g='use', act=('tap', 'surface'), pick='hungriest', prefer=['curious', 'happy'], obj=[(.25, dict(lure=1)), (.6, dict(lure=1)), (.8, dict(lure=1))])
    o.r('pat_the_chin_when_it_hangs_still', 'Patting the trout\'s chin with the back of a wing when it hangs still at the rim, one slow tickle at a time', 22, 'wing',
        [k(.08, 'rise_l', reach=.4, x=.2, y=1, b=.5), k(.24, 'rise_l', reach=.8, x=.4, y=1.7, b=1.2, mark='tck'), k(.4, 'rise_l', reach=1, x=.3, y=1.8, b=1.4, l=1, mark='tck'), k(.56, 'rise_l', reach=1, x=.4, y=1.7, b=1.3, r=1, mark='tck'),
         k(.74, 'rise_l', reach=.5, x=.2, y=.9, b=.6), k(.9, eye='^')],
        [(.4, 'tickle')], g='use', act=('pat', 'chin'), pick='shyest', when=['spook<.5'], prefer=['fish_trust<.8', 'lonely'], obj=[(.22, dict(lure=1)), (.7, dict(lure=1))])
    o.r('balance_a_twig_on_the_water_to_lead', 'Laying a twig flat at the water\'s skin and walking it slowly along the rim so the trout trails the tip', 26, 'twig',
        [k(.05, 'rise_l', reach=.4, x=.3, y=.3, b=.2), k(.18, 'rise_l', reach=1, x=.6, y=.6, b=.5), k(.34, 'glide', reach=1, x=.8, y=.6, b=.3, l=1), k(.5, 'edge_far', reach=1, x=1, y=.6, b=.5, r=1),
         k(.68, 'rise_r', reach=1, x=1.2, y=.6, b=.3, l=1), k(.86, eye='^')],
        [(.5, 'dimple')], g='use', act=('balance', 'twig'), pick='hungriest', when=['rise>.3'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.5, dict(lure=1)), (.72, dict(lure=1))],
        say=["Followed the twig the whole way. Faithful to anything that floats.", "A twig, a trout, a tiny parade."])
    # ---------------- play
    o.r('sprint_the_shelf_with_the_flurry', 'Sprinting along the shelf in short rushes as the trout flurries from ring to ring ahead of him', 20, 'none',
        [k(.05, 'rise_l', x=.7, y=.3, b=.3), k(.15, 'glide', x=1.4, y=.4, b=-.9, l=1, w=.4), k(.25, 'glide', x=.8, y=.5, b=.5, r=1), k(.36, 'edge_far', x=1.5, y=.3, b=-1, l=1, w=.7, mark='hup'),
         k(.48, 'edge_far', x=.8, y=.5, b=.6, r=1), k(.6, 'rise_r', x=1.6, y=.3, b=-1.1, l=1, w=.9, mark='HUP'), k(.78, 'rise_r', x=.5, y=.4, b=.4, eye='@')],
        [(.6, 'fun')], g='play', act=('race', 'shelf'), pick='hungriest', when=['rise>.3'], prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.3, dict(lure=1)), (.46, dict(lure=1)), (.64, dict(lure=1))],
        say=["Lost by six rings. It rises faster than I can sprint.", "Raced a trout. Beat it on the way back. It was not racing."])
    o.r('spin_on_the_stone_at_each_rise', 'Spinning round on the left stone to follow each rise, wings out, until the whole bank blurs', 22, 'none',
        [k(.06, 'stone_l', x=.3, y=.4, b=.4, perch=1), k(.2, 'stone_l', x=1.2, y=-.4, b=-.6, w=.8, l=1, perch=1), k(.34, 'stone_l', x=-1.2, y=.3, b=.8, w=1, r=1, perch=1), k(.5, 'stone_l', x=1.3, y=-.3, b=-.8, w=1, l=1, perch=1, mark='whirr'),
         k(.66, 'stone_l', x=-1, y=.5, b=.9, w=.8, r=1, perch=1), k(.84, 'stone_l', x=.2, y=1, b=1.2, perch=1, eye='@', mark='dizzy')],
        [], g='play', act=('spin', 'stone'), prefer=['young', 'happy'], when=['rings>.3'])
    o.r('chase_the_rings_with_a_wing', 'Chasing the widening rings across the surface with a wing, tapping each before it fades', 20, 'wing',
        [k(.07, 'glide', reach=.5, x=.5, y=.5, b=.3), k(.2, 'glide', reach=1, x=.9, y=.6, b=.6, mark='tp'), k(.33, 'edge_far', reach=1, x=1.1, y=.7, b=.5, l=1, mark='tp'), k(.46, 'rise_r', reach=1, x=1.3, y=.6, b=.7, r=1, mark='tp'),
         k(.6, 'rise_r', reach=.8, x=.8, y=.4, b=.3), k(.78, 'glide', reach=1, x=.9, y=.5, b=.6, l=1), k(.92, eye='@')],
        [], g='play', act=('chase', 'rings'), prefer=['curious', 'young'], when=['rings>.3'])
    o.r('seek_the_shy_one_along_the_far_edge', 'Hunting along the far edge for the trout that has gone quiet, bill sweeping slowly side to side', 22, 'none',
        [k(.06, 'rise_l', x=.7, y=.9, b=.6), k(.2, 'mud_edge', x=1.2, y=1.3, b=.9, eye='o'), k(.34, 'edge_far', x=1.4, y=1.5, b=1.1, eye='o', mark='?'), k(.5, 'rise_r', x=1.5, y=1.5, b=1.2, l=1, mark='?'),
         k(.66, 'rise_r', x=1.3, y=1.4, b=1.1, eye='O', mark='there!'), k(.84, x=.3, y=.4, eye='^')],
        [], g='play', act=('seek', 'trout'), pick='shyest', prefer=['young', 'curious'], when=['spook>.3'], obj=[(.66, dict(lure=1)), (.84, dict(lure=1))])
    o.r('hop_in_time_with_the_flurry', 'Hopping in time with the flurry of rises, three hops to a burst, wings out like a conductor', 18, 'none',
        [k(.06, 'stone_m', x=.3, y=.3, b=.2), k(.16, 'stone_m', x=.4, y=-.2, b=-1.3, w=.6, l=1, r=1), k(.26, 'stone_m', x=.3, y=.4, b=.6), k(.38, 'stone_m', x=.4, y=-.3, b=-1.4, w=.8, l=1, r=1),
         k(.5, 'stone_m', x=.3, y=.4, b=.6), k(.62, 'stone_m', x=.5, y=-.4, b=-1.6, w=1, l=1, r=1, mark='HUP'), k(.78, 'stone_m', x=.3, y=.5, b=.8, eye='>')],
        [(.38, 'fun')], g='play', act=('hop', 'stone'), pick='hungriest', prefer=['young', 'happy'], obj=[(.38, dict(lure=1)), (.7, dict(lure=1))])
    o.r('pitch_crumbs_at_three_rings', 'Pitching three crumbs in quick succession at three rings, one wing flick each, and counting the answers', 20, 'wing',
        [k(.06, 'rise_l', reach=.4, x=.2), k(.2, 'rise_l', reach=1, x=.5, y=-.3, b=-.5, mark='flk'), k(.32, 'glide', reach=1, x=.5, y=-.3, b=-.5, l=1, mark='flk'), k(.44, 'rise_r', reach=1, x=.5, y=-.3, b=-.5, r=1, mark='flk'),
         k(.6, 'rise_r', reach=.5, x=.3, y=.2, b=.2, eye='o', mark='1 2 3'), k(.8, eye='^')],
        [(.44, 'sprinkle')], g='play', act=('throw', 'crumbs'), prefer=['happy', 'curious'], when=['pond_flakes<.4'])
    # ---------------- test
    o.r('count_the_freckles_on_a_flank', 'Counting the freckles down one flank with a bill-bob for each, then starting over after losing count', 22, 'none',
        [k(.05, 'rise_r', x=1.0, y=1.4, b=.6, mark='1'), k(.16, 'rise_r', x=1.1, y=1.5, b=.7, mark='5'), k(.28, 'glide', x=1.2, y=1.5, b=.8, l=1, mark='11'), k(.4, 'glide', x=1.3, y=1.6, b=.9, r=1, mark='20?'),
         k(.52, x=-.4, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.66, 'rise_r', x=1.0, y=1.4, b=.6, mark='1'), k(.84, eye='-')],
        [], g='test', act=('count', 'freckles'), pick='shyest', prefer=['curious'], obj=[(.15, dict(lure=1)), (.5, dict(lure=1))])
    o.r('time_the_rises_by_the_sun', 'Counting rises against a slow bill-nod to time the flurry, lifting a toe at each ring', 20, 'none',
        [k(.06, 'edge_far', x=.7, y=.9, b=.4), k(.2, 'edge_far', x=.9, y=1, b=.5, l=1, mark='one'), k(.34, 'edge_far', x=.8, y=1, b=.5, r=1, mark='two'), k(.5, 'edge_far', x=1, y=1.1, b=.6, l=1, mark='three'),
         k(.64, 'edge_far', x=1.1, y=1.2, b=.7, r=1, mark='four'), k(.84, eye='-', mark='lots')],
        [], g='test', act=('count', 'rises'), prefer=['curious', 'dawn'], when=['rise>.3'])
    o.r('judge_the_chill_with_a_wingtip', 'Brushing a wingtip across the cold surface to judge whether the trout will rise or sulk today', 22, 'wing',
        [k(.06, 'rise_l', reach=.4, x=.1, y=.6, b=.3), k(.21, 'rise_l', reach=.9, x=.3, y=.9, b=.7, mark='brr'), k(.38, 'shelf', reach=1, x=.4, y=1, b=.8), k(.54, 'glide', reach=1, x=.4, y=1, b=.8, l=1, mark='hm'),
         k(.72, 'glide', reach=.5, x=.2, y=.5, b=.3), k(.9, eye='o')],
        [], g='test', act=('test', 'chill'), prefer=['curious'], when=['rise<.7'])
    o.r('listen_for_the_plop_of_a_rise', 'Listening hard at the rim, head cocked, for the tiny plop that gives a rise away before it shows', 20, 'none',
        [k(.07, x=-.4, y=.5, b=.3), k(.22, 'stone_m', x=-.9, y=1.2, b=.8, eye='-'), k(.4, 'stone_m', x=-1, y=1.4, b=1, eye='-', mark='...'), k(.58, 'stone_m', x=-1.1, y=1.5, b=1, eye='o', mark='plip'),
         k(.76, 'stone_m', x=.2, y=.5, b=.3, eye='O'), k(.9, eye='^')],
        [], g='test', act=('listen', 'plop'), prefer=['curious', 'dawn'])
    o.r('compare_the_length_to_the_wild_ones', 'Holding a wing out along the trout\'s length and then past it, comparing it with the longest wild ones he has heard of', 24, 'wing',
        [k(.06, 'rise_l', reach=.4, x=.2, y=.7, b=.3), k(.2, 'rise_l', reach=.9, x=.3, y=.9, b=.6), k(.36, 'glide', reach=1, x=.5, y=.8, b=.4, r=1, mark='so'), k(.52, 'rise_r', reach=1, x=.9, y=.8, b=.4, l=1, mark='far?'),
         k(.7, 'glide', reach=.7, x=.3, y=.4, b=.2), k(.88, eye='-', mark='bigger')],
        [], g='test', act=('compare', 'lengths'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.25, dict(lure=1)), (.5, dict(lure=1))])
    o.r('weigh_the_trout_by_eye', 'Squinting along a reed held flat over the trout to weigh it by eye, his head rocking like a scale', 22, 'reed',
        [k(.06, 'rise_l', reach=.4, x=.2, y=.3), k(.2, 'glide', reach=.9, x=.5, y=.9, b=.5, eye='-'), k(.35, 'glide', reach=1, x=.6, y=1, b=.6, l=1, mark='rock'), k(.5, 'glide', reach=1, x=.5, y=.6, b=.3, r=1, mark='rock'),
         k(.66, 'glide', reach=.8, x=.4, y=.8, b=.5, eye='o', mark='two'), k(.86, eye='^')],
        [], g='test', act=('weigh', 'trout'), pick='shyest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- rest
    o.r('doze_on_the_left_stone', 'Dozing on the left stone in the first sun, bill tucked into his chest feathers', 26, 'none',
        [k(.08, 'stone_l', x=.3, y=.9, b=.9, eye='-', perch=1), k(.26, 'stone_l', x=-.6, y=1.7, b=1.7, eye='-', perch=1), k(.52, 'stone_l', x=-.8, y=2.1, b=2.3, eye='-', mark='zzz', perch=1), k(.74, 'stone_l', x=-.3, y=.9, b=.9, eye='o', perch=1),
         k(.9, eye='^')],
        [(.52, 'rest')], g='rest', act=('nap', 'stone'), when=['tired'], prefer=['dawn'])
    o.r('sit_at_the_bank_in_the_dawn', 'Sitting at the right bank with his feet folded, watching the first pink rings spread', 24, 'none',
        [k(.08, 'bank_r', x=.4, y=.4, b=.8), k(.28, 'bank_r', x=.1, y=.8, b=1.5, eye='-'), k(.52, 'bank_r', x=-.1, y=1, b=1.9, eye='o', mark='...'), k(.74, 'bank_r', x=.5, y=.4, b=.7, l=1), k(.9, eye='^')],
        [(.52, 'rest')], g='rest', act=('sit', 'bank'), when=['dawn'], prefer=['tired', 'lonely'])
    o.r('hold_dead_still_for_the_first_rise', 'Holding dead still at the rim, not a feather out of place, until the trout trusts the shadow and rises', 28, 'none',
        [k(.06, 'glide', x=.8, y=1.2, b=.7, eye='o'), k(.25, 'glide', x=.9, y=1.4, b=.9, eye='o'), k(.5, 'glide', x=.9, y=1.4, b=.9, l=1), k(.7, 'glide', x=1, y=1.6, b=1, eye='O', mark='...'), k(.9, 'glide', x=.5, y=.7, b=.4, eye='^')],
        [(.7, 'settle')], g='rest', act=('wait', 'rise'), pick='shyest', when=['spook>.3'], obj=[(.55, dict(lure=1)), (.85, dict(lure=1))],
        say=["Still enough that a dragonfly would have applied for the job.", "Trust takes a motionless duck. I have a talent."])
    o.r('prop_himself_on_the_low_reed', 'Propping a shoulder on the low reed and letting the dawn mist roll past his eyes', 20, 'none',
        [k(.07, 'reed_low', x=-.5, y=.3, b=.4), k(.25, 'reed_low', x=-.9, y=.6, b=.8, eye='-'), k(.5, 'reed_low', x=-1.1, y=.8, b=1.1, eye='-', mark='...'), k(.7, 'reed_low', x=-.8, y=.7, b=.9, r=1), k(.88, x=.4, y=.3, eye='O')],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'sad'])
    o.r('sulk_when_it_will_not_rise', 'Sulking at the empty water with his bill pointed at the sky because the trout has ignored every rise-bait of his', 22, 'none',
        [k(.08, x=-.8, y=.2, b=.5), k(.25, 'rise_r', x=-1.5, y=-.7, b=1.2, eye='-'), k(.5, 'rise_r', x=-1.8, y=-1, b=1.9, eye='-', mark='psh'), k(.7, 'rise_r', x=-1.6, y=-.8, b=1.6, l=1), k(.86, x=-.5, y=.2, eye='-')],
        [], g='rest', act=('sulk', 'water'), when=['sad'])
    # ---------------- weather
    o.r('tap_the_skin_of_ice_with_a_bill', 'Tapping the thin skin of ice back from the rim with his bill so the trout has a patch of open water to rise in', 22, 'none',
        [k(.06, 'stone_m', x=.7, y=.9, b=.4), k(.18, 'rise_l', x=1.6, y=2.2, b=.9, mark='tk'), k(.3, 'rise_l', x=1.8, y=2.5, b=1.2, r=1, mark='tk'), k(.44, 'glide', x=1.6, y=2.3, b=1, mark='TK'),
         k(.58, 'glide', x=1.8, y=2.5, b=1.3, l=1, mark='CRK'), k(.76, x=.5, y=.5, b=.2, eye='^')],
        [(.58, 'crack')], g='weather', act=('tap', 'ice'), when=['pond_ice>.3'])
    o.r('sweep_the_rime_off_with_a_reed', 'Sweeping the rime off the shelf and bank stones with a reed in long cold strokes', 20, 'reed',
        [k(.07, 'bank_r', reach=.5, x=.3, y=.6, b=.2), k(.2, 'bank_r', reach=1, x=.9, y=1.2, b=.7, mark='shh'), k(.35, 'shelf', reach=1, x=1.1, y=1.4, b=.9, l=1, mark='shh'), k(.5, 'mud_edge', reach=1, x=1, y=1.5, b=1, r=1),
         k(.68, 'mud_edge', reach=.6, x=.4, y=.5, b=.4), k(.86, eye='-')],
        [(.35, 'clear')], g='weather', act=('sweep', 'rime'), when=['pond_ice>.3'])
    o.r('huddle_into_the_reeds_from_the_rain', 'Huddling with his back against the low reed while rain pocks the pond and the trout keeps rising', 30, 'none',
        [k(.07, 'reed_low', x=-.7, y=.8, b=.9), k(.25, 'reed_low', x=-1.2, y=1.8, b=1.8, eye='-'), k(.5, 'reed_low', x=-1.4, y=2.1, b=2.1, eye='-', mark='plink'), k(.74, 'reed_low', x=-1.3, y=2, b=1.9, r=1, mark='plink'),
         k(.9, x=.1, y=.3, b=.3, eye='^')],
        [], g='weather', act=('shelter', 'reed'), when=['wet'])
    o.r('warm_his_back_at_the_cattail_in_the_sun', 'Turning his back to the early sun at the left cattail and letting it dry the dew off his feathers', 20, 'none',
        [k(.08, 'cattail_l', x=-.3, y=.3, b=.6), k(.28, 'cattail_l', x=-.6, y=.6, b=1, w=.4, eye='-'), k(.52, 'cattail_l', x=-.7, y=.7, b=1.1, w=.8, eye='-', mark='ahh'), k(.74, 'cattail_l', x=-.4, y=.4, b=.7, w=.4), k(.9, eye='^')],
        [], g='weather', act=('warm', 'back'), when=['sun'], prefer=['dawn', 'tired'])
    o.r('lean_into_the_gust_along_the_bank', 'Leaning into the gust along the bank with both wings half open to flatten the whitecaps on the trout\'s glide', 18, 'none',
        [k(.06, 'bank_r', x=1.1, y=.2, b=.9), k(.22, 'bank_r', x=1.6, y=.5, b=1.4, w=.7, mark='whsh'), k(.4, 'bank_r', x=1.8, y=.6, b=1.7, w=1, l=1), k(.58, 'bank_r', x=1.6, y=.5, b=1.4, w=.8, r=1), k(.78, 'bank_r', x=.8, y=.3, b=.7), k(.92, eye='-')],
        [], g='weather', act=('brace', 'wind'), when=['windy'])
    o.r('cool_a_wingtip_at_the_edge_on_a_warm_noon', 'Cooling a wingtip at the water\'s edge on a warm noon, dabbing the underside of his feathers where the trout hangs in the shade', 20, 'wing',
        [k(.06, 'rise_l', reach=.4, x=.2, y=.5, b=.4), k(.2, 'rise_l', reach=.9, x=.5, y=1, b=.9, eye='-'), k(.38, 'rise_l', reach=1, x=.6, y=1.1, b=1.1, mark='ahh'), k(.56, 'shelf', reach=1, x=.5, y=1, b=.9, l=1), k(.74, 'shelf', reach=.5, x=.3, y=.5, b=.4),
         k(.9, eye='^')],
        [], g='weather', act=('cool', 'wingtip'), when=['warm'], prefer=['summer'])
    # ---------------- show
    o.r('bow_to_the_spotted_riser', 'Bowing to the spotted riser as it breaks the surface right at his bill, a deep and dripping dip', 16, 'none',
        [k(.08, 'glide', x=.7, y=1.1, b=.8), k(.28, 'glide', x=1.2, y=2.4, b=2, eye='-'), k(.5, 'glide', x=1.3, y=2.6, b=2.2, eye='-', mark='sir'), k(.7, 'glide', x=.7, y=.6, b=.5), k(.86, x=.1, y=-.4, w=.6, eye='^')],
        [], g='show', act=('bow', 'riser'), pick='hungriest', prefer=['happy'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed to a riser. It rose to my forehead.", "Respect shown. Ripples returned."])
    o.r('present_a_flurry_of_rings', 'Presenting a flurry of rings to an invisible crowd with one long sweep of the wing, a small and damp circus', 20, 'wing',
        [k(.07, 'rise_l', reach=.4, x=.1, y=.1), k(.24, 'rise_l', reach=.9, x=.2, y=-.6, b=-.5), k(.42, 'glide', reach=1, x=.2, y=-.8, b=-.7, mark='tadaa'), k(.6, 'rise_r', reach=1, x=.3, y=-.6, b=-.4, r=1), k(.78, 'rise_r', reach=.6, x=.5, y=-.1),
         k(.92, eye='^')],
        [], g='show', act=('present', 'rings'), pick='shyest', prefer=['happy'], obj=[(.45, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_the_freckle_count', 'Arguing over the freckle count with the trout, jabbing a wing at the spot he swears he already counted', 20, 'wing',
        [k(.06, 'glide', reach=.4, x=.6, y=.3, b=.3), k(.2, 'glide', reach=1, x=1.1, y=.1, b=.1, mark='TWENTY'), k(.36, 'glide', reach=1, x=1.3, y=0, b=-.1, l=1, mark='TWENTY'), k(.52, 'glide', reach=.6, x=.5, y=.6, b=.7, r=1),
         k(.7, 'glide', reach=1, x=1.2, y=0, b=0, mark='TWENTY-ONE'), k(.88, eye='-')],
        [], g='show', act=('argue', 'freckles'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It insists on twenty-one. It has the spots, I have the arithmetic.", "Lost the count and the argument. Two for two."])
    o.r('pose_on_the_stone_with_a_rising_trout', 'Freezing in the pose of a leaping fish on the right stone, wings slashed back, while the real one rises below him', 18, 'none',
        [k(.07, 'stone_r', x=.4, y=-.1, w=.3, perch=1), k(.22, 'stone_r', x=.9, y=-.7, b=-.7, w=.7, perch=1), k(.46, 'stone_r', x=1.1, y=-.9, b=-1, w=1, perch=1, eye='^', mark='so fast'), k(.72, 'stone_r', x=.4, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'stone'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('cheer_the_flurry_from_the_bank', 'Cheering the flurry from the bank, calling every rise by number with a wing thrown up', 18, 'wing',
        [k(.06, 'bank_r', reach=.3, x=.2, y=-.1), k(.18, 'bank_r', reach=1, x=.4, y=-.5, b=-.4, mark='ONE'), k(.3, 'bank_r', reach=1, x=.5, y=-.6, b=-.5, l=1, mark='TWO'), k(.44, 'bank_r', reach=1, x=.5, y=-.7, b=-.6, r=1, mark='THREE'),
         k(.58, 'bank_r', reach=1, x=.6, y=-.8, b=-.8, l=1, r=1, mark='FOUR!'), k(.76, 'bank_r', reach=.4, x=.2, y=0), k(.9, eye='^')],
        [], g='show', act=('shout', 'rises'), prefer=['happy', 'young'], when=['rise>.3'], say=["Seven rises, no encore. A tough crowd, the water.", "Cheered till my bill hurt. Trout carried on regardless."])
    # ---------------- mishap
    o.r('slip_on_the_dewy_front_stone', 'Slipping on the dew-slick middle stone, a wing-flap save that rocks the whole bank and sends the trout down', 16, 'none',
        [k(.06, 'stone_m', x=.5, y=.4, b=.4), k(.18, 'stone_m', x=1.2, y=-.5, b=-1.1, l=1, r=1, w=.9, mark='whoa'), k(.3, 'stone_m', x=1.7, y=1.2, b=1.9, w=.6, eye='O', mark='THUD'), k(.46, 'stone_m', x=.6, y=.8, b=1, eye='>'),
         k(.62, x=.1, y=.3, b=.2, eye='-')],
        [(.3, 'scare')], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('bill_wedged_in_the_reed_stems', 'Wedging his bill between the two low reed stems after a flash of fin and tugging free with a twang', 22, 'none',
        [k(.06, x=.9, y=.5, b=.5), k(.18, 'reed_low', x=1.9, y=.3, b=.6, eye='O'), k(.34, 'reed_low', x=2.1, y=.4, b=.9, l=1, eye='@', mark='mm'), k(.5, 'reed_low', x=2, y=.5, b=1.1, r=1, mark='mmf'),
         k(.64, 'reed_low', x=1.2, y=-.4, b=-.9, w=1, mark='TWANG'), k(.82, x=1.1, y=.9, b=.6, eye='-')],
        [], g='mishap', act=('stuck', 'reed'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_cattail_chasing_a_ring', 'Following a ring along the bank with his eyes only and bumping the tall cattail head first', 18, 'none',
        [k(.06, 'rise_l', x=.5, y=.6, b=.3), k(.2, 'rise_l', x=.7, y=.7, b=.4, l=1), k(.34, 'tuft', x=.7, y=.5, b=.4, r=1), k(.5, 'cattail_l', x=1.6, y=-.4, b=1.6, eye='@', mark='CLONK'), k(.66, 'cattail_l', x=-1, y=.3, b=.3, w=.8, eye='x'),
         k(.84, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'cattail'), prefer=['curious'])
    o.r('flinch_from_the_rise_at_his_bill', 'Flinching back as the trout takes a crumb off the very tip of his bill with a smack and a splash', 16, 'none',
        [k(.06, 'rise_r', x=1.1, y=1.7, b=.8), k(.18, 'rise_r', x=1.3, y=1.9, b=1, eye='o'), k(.28, x=-1.4, y=-.7, b=-1.3, l=1, r=1, w=.9, eye='O', mark='SMACK'), k(.42, x=-.8, y=.2, b=-.1, w=.6, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [(.18, 'flurry')], g='mishap', act=('hop', 'splash'), pick='hungriest', prefer=['young', 'curious'], obj=[(.18, dict(lure=1)), (.45, dict(lure=1))],
        say=["Smacked the bill like a cymbal. Rude, quick, correct.", "I was a crumb for half a second. Humbling."])
    o.r('stamp_the_rings_flat', 'Stamping at the rings spreading from a missed rise, as if the trout could be made to try again', 16, 'none',
        [k(.05, 'stone_r', x=.7, y=.8, b=.4), k(.16, 'stone_r', x=.5, y=-.1, b=-1.2, l=1, mark='STMP'), k(.26, 'stone_r', x=.6, y=.6, b=.6), k(.38, 'stone_r', x=.5, y=-.1, b=-1.2, r=1, mark='STMP'),
         k(.5, 'stone_r', x=.6, y=.6, b=.6), k(.64, 'stone_r', x=.5, y=-.2, b=-1.3, l=1, r=1, mark='STMP!'), k(.84, eye='-')],
        [(.38, 'scare')], g='mishap', act=('stamp', 'rings'), prefer=['grumpy'], when=['rings>.3'])
    # ---------------- duets (a friend takes their own part)
    o.r('hold_still_together_for_the_rise', 'Standing statue-still beside a friend on the far stone, the two shadows quiet until the trout trusts them and rises', 28, 'none',
        [k(.06, 'rise_l', x=.9, y=1.1, b=.6), k(.24, 'rise_l', x=1, y=1.3, b=.8, eye='o'), k(.5, 'rise_l', x=1, y=1.3, b=.8, l=1), k(.7, 'rise_l', x=1.1, y=1.5, b=1, eye='O', mark='...'), k(.88, 'rise_l', x=.5, y=.6, b=.4, eye='^')],
        [(.7, 'settle')], g='rest', act=('perch', 'shadow'), pick='shyest', when=['spook>.3'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.1, 'stone_r', x=.4, y=.5, b=.4), k(.3, 'stone_r', x=.5, y=.8, b=.7, eye='-'), k(.55, 'stone_r', x=.5, y=.8, b=.7), k(.76, 'stone_r', x=.5, y=.9, b=.8, eye='o', mark='...'), k(.9, eye='^')],
        say=["Two ducks holding their breath. The fish is the only one breathing.", "Silent as a pair of garden gnomes. It came up for us."])
    o.r('feed_it_from_both_banks_in_turn', 'Dropping a crumb in turn with a friend from the opposite bank so the trout dashes from one ring to the other', 24, 'none',
        [k(.06, 'rise_l', x=.5, y=.3, b=.2), k(.2, 'rise_l', x=1.2, y=-.4, b=-.9, w=.6, mark='plip'), k(.34, 'glide', x=1, y=.3, b=.4, eye='o'), k(.5, 'rise_l', x=1.3, y=-.5, b=-.9, w=.6, l=1, mark='plip'), k(.66, 'rise_l', x=.9, y=.6, b=.5, eye='O'),
         k(.84, eye='^')],
        [(.5, 'flurry')], g='use', act=('tip', 'crumbs'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))],
        duo=[k(.1, 'rise_r', x=.5, y=.3, b=.2), k(.28, 'rise_r', x=1.1, y=.4, b=.5, eye='o'), k(.42, 'rise_r', x=1.2, y=-.4, b=-.9, w=.6, l=1, mark='plip'), k(.6, 'rise_r', x=1, y=.3, b=.4), k(.8, eye='^')])
    o.r('read_the_rings_aloud_to_a_friend', 'Reading the rings aloud to a friend at the other end of the shelf, the two trading guesses on which rise came first', 24, 'wing',
        [k(.06, 'shelf', reach=.4, x=.3, y=.4, b=.3), k(.2, 'glide', reach=.9, x=.5, y=.5, b=.5, mark='that one'), k(.36, 'glide', reach=1, x=.6, y=.6, b=.6, l=1), k(.52, 'edge_far', reach=1, x=.7, y=.6, b=.5, r=1, mark='no, THAT one'),
         k(.72, 'shelf', reach=.6, x=.3, y=.3, b=.2), k(.88, eye='-')],
        [], g='test', act=('show', 'rings'), pick='hungriest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.1, 'mud_edge', x=.5, y=.4, b=.3), k(.26, 'mud_edge', x=.9, y=.7, b=.6, eye='o', mark='no'), k(.46, 'rise_r', x=1, y=.8, b=.7, l=1, mark='that one'), k(.66, 'mud_edge', x=.7, y=.6, b=.5, r=1), k(.84, eye='^')],
        say=["We agreed on nothing. Excellent teamwork.", "Two readers, one ripple. The fish wrote the book."])
    return done(o)


def sturgeon():
    # Sturgeon: ancient armoured bottom-cruiser with barbels, active at night, slow and huge. Lives in the sea tank (infinity_pool); Cheese watches from the edge:
    # wing flat on the tank wall, bill to the wall, a reed over the coping. Own state: silt (floor silt it stirs at night: drawn), pellets (sunk pellets on the floor:
    # drawn), lap (how settled its slow circuit is: built by leading it along the wall).
    o = Obj('sturgeon', 'keeping', on='infinity_pool',
            fields=dict(silt=(0, 0, 1), pellets=(0, 0, 1), lap=(0, 0, 1)),
            physics=[('silt', 'rate', .0005, 'night'), ('silt', 'rate', -.0008, '!night'), ('pellets', 'rate', -.0008, 'always'), ('lap', 'rate', -.0003, 'always')],
            effects=dict(scrub=[('keeping.algae', 'mul', .5)], rake=[('keeping.leaves', 'mul', .35)], sweep=[('silt', 'mul', .25), ('keeping.clarity', 'add', .12)],
                         polish=[('keeping.clarity', 'add', .15)], tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)],
                         call=[('keeping.bell', 'add', .5)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)],
                         sink=[('pellets', 'set', 1), ('keeping.flakes', 'add', .35)], husk=[('pellets', 'mul', .2)],
                         lead=[('lap', 'add', .25), ('subject.trust', 'add', .1)], stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         rise=[('subject.hunger', 'add', -.2), ('lap', 'add', .2)], crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('silt', .3, '~=~=~', 'base_m', 'mud'), ('pellets', .3, '.:.:.', 'base_r', 'dust'), ('pond_flakes', .3, ".':.'", 'skin_l', 'dust'), ('pond_leaves', .3, ';"~;"', 'skin_m', 'leaf'),
                   ('pond_ice', .3, '*-*-*', 'high_l', 'frost'), ('pond_algae', .3, '"v"v"', 'base_l', 'plant')],
            anchors=dict(base_l=Q(24, 46), base_m=Q(62, 46), base_r=Q(94, 46), low_l=Q(36, 43), low_r=Q(80, 43), high_l=Q(28, 40), high_m=Q(62, 40),
                         skin_l=Q(34, 34), skin_m=Q(68, 34), coping=Q(40, 28), ledge_l=Q(30, 49, 'surface'), ledge_m=Q(62, 49, 'surface'), ledge_r=Q(92, 49, 'surface'),
                         pier_l=Q(10, 41), pier_r=Q(110, 41), lip=Q(40, 52, 'surface')))
    # ---------------- care
    o.r('wipe_the_green_off_the_wall_foot', 'Wiping the green film off the foot of the tank wall in long flat strokes from the left corner to the right', 24, 'wing',
        [k(.06, 'base_l', reach=.4, x=.2, y=.9, b=.4), k(.17, 'base_l', reach=1, x=.5, y=1.5, b=1, mark='wsh'), k(.3, 'base_m', reach=1, x=.8, y=1.7, b=1.2, l=1, mark='wsh'), k(.45, 'base_m', reach=1, x=1, y=1.6, b=1.1),
         k(.6, 'base_r', reach=1, x=1.2, y=1.7, b=1.3, r=1, mark='wsh'), k(.78, 'base_r', reach=.5, x=.5, y=.7, b=.4), k(.92, eye='^')],
        [(.45, 'scrub')], g='care', act=('wipe', 'algae'), when=['pond_algae>.4'],
        say=["The wall is clear. The sturgeon will never know. Neither will the algae.", "Wiped it spotless. Spotless water, spotted duck."])
    o.r('rake_the_leaves_off_the_top_with_a_reed', 'Raking the leaves off the top of the tank with a reed held over the coping, drawing them to the left corner', 26, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.3, y=-.1), k(.2, 'coping', reach=1, x=.5, y=-.3, b=-.2, mark='rk'), k(.34, 'skin_m', reach=1, x=.6, y=-.2, b=-.1, l=1, mark='rk'), k(.5, 'skin_l', reach=1, x=.7, y=-.1, b=.1, r=1, mark='rk'),
         k(.66, 'skin_l', reach=.7, x=.3, y=0, b=-.2), k(.84, eye='-')],
        [(.5, 'rake')], g='care', act=('rake', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'])
    o.r('sweep_the_silt_cloud_off_the_view', 'Sweeping a wing over the wall to follow and thin the brown cloud the sturgeon keeps rooting up along the floor', 22, 'wing',
        [k(.07, 'base_r', reach=.4, x=.3, y=.7, b=.3), k(.2, 'base_r', reach=1, x=.7, y=1.1, b=.7, mark='shh'), k(.35, 'low_r', reach=1, x=.8, y=1.3, b=.9, l=1, mark='shh'), k(.5, 'base_m', reach=1, x=.9, y=1.4, b=1, r=1),
         k(.68, 'low_l', reach=1, x=.8, y=1.2, b=.8, mark='shh'), k(.88, eye='-')],
        [(.5, 'sweep')], g='care', act=('sweep', 'silt'), when=['silt>.3'], prefer=['night'])
    o.r('polish_the_wall_with_a_wing_corner', 'Polishing the wall with the tip of a wing in small circles until the cloudy patch at eye height clears', 22, 'wing',
        [k(.08, 'high_l', reach=.5, x=.2, y=.3, b=.2), k(.22, 'high_l', reach=1, x=.5, y=.4, b=.4, mark='sqk'), k(.36, 'high_m', reach=1, x=.6, y=.5, b=.5, l=1, mark='sqk'), k(.5, 'high_m', reach=1, x=.5, y=.4, b=.4, r=1, mark='sqk'),
         k(.66, 'low_r', reach=1, x=.6, y=.8, b=.7), k(.84, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'wall'), when=['pond_clarity<.6'])
    o.r('peer_at_the_armour_plates', 'Peering at the bony plates along the sturgeon\'s back as it rolls past the wall, looking for any chip or crack', 22, 'none',
        [k(.06, x=.5, y=.6, b=.4), k(.18, 'low_l', x=1.5, y=1.9, b=1.0, eye='o'), k(.32, 'low_l', x=1.7, y=2.1, b=1.2, eye='O', mark='hm'), k(.5, 'base_m', x=1.4, y=2.0, b=1.1, l=1), k(.66, 'base_r', x=1.5, y=2.2, b=1.3, r=1, mark='ok'),
         k(.84, x=.6, y=.6, b=.3, w=.4, eye='^')],
        [(.5, 'tend')], g='care', act=('peer', 'plates'), pick='shyest', when=['fish_health<.8'], obj=[(.18, dict(lure=1)), (.5, dict(lure=1)), (.66, dict(lure=1))],
        say=["Every plate present. Armour older than my family tree.", "No chips. It has been through worse than a tank."])
    o.r('shove_the_sunk_husks_along_with_a_wing', 'Brushing the sunk pellet husks along the floor line with a wing so they do not pile at the left corner', 20, 'wing',
        [k(.08, 'base_l', reach=.5, x=.4, y=1.0, b=.5), k(.24, 'base_l', reach=1, x=.9, y=1.5, b=1.0, l=1), k(.4, 'base_m', reach=1, x=1.1, y=1.6, b=1.2, mark='shh'), k(.58, 'base_r', reach=1, x=1.2, y=1.7, b=1.3, r=1, mark='shh'),
         k(.76, 'base_r', reach=.5, x=.6, y=.8, b=.5), k(.9, eye='-')],
        [(.58, 'husk')], g='care', act=('shove', 'husks'), when=['pellets>.3'])
    # ---------------- use
    o.r('knock_three_slow_at_the_wall_foot', 'Knocking three slow beats at the foot of the wall with his bill, the night bell the old fish has always known', 18, 'none',
        [k(.07, 'base_l', x=1.3, y=1.5, b=.8, mark='tok'), k(.2, 'base_l', x=1.5, y=1.7, b=1, mark='tok'), k(.34, x=.1, y=.2, b=.1, w=.3), k(.5, 'base_l', x=1.5, y=1.7, b=1.1, l=1, mark='TOK'), k(.7, x=.4, y=.5, b=.4, eye='^')],
        [(.5, 'call')], g='use', act=('knock', 'wall'), when=['pond_bell<.4'], prefer=['night', 'dusk'])
    o.r('press_a_pellet_to_the_wall_for_the_snout', 'Pressing one pellet flat to the wall with his bill while the long snout hoovers at it from the other side', 22, 'none',
        [k(.06, x=.4, y=.7, b=.4), k(.2, 'low_l', x=1.7, y=1.9, b=.9, eye='o', mark='...'), k(.36, 'low_l', x=1.9, y=2.1, b=1.1, eye='O', mark='SHLRP'), k(.52, 'low_l', x=1.8, y=2.0, b=1, l=1),
         k(.7, x=.6, y=.8, b=.5, w=.4, eye='^'), k(.88, eye='-')],
        [(.36, 'feed')], g='use', act=('press', 'pellet'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.2, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=0))],
        say=["Hoovered it from the other side. It could have sucked my bill off.", "Sturgeons eat like a drain. A very old drain."])
    o.r('lob_pellets_up_and_over_the_coping', 'Lobbing a wingful of sinking pellets up and over the coping so they patter down to the floor', 20, 'wing',
        [k(.08, 'skin_l', reach=.3, x=.1, y=.1), k(.22, 'skin_l', reach=.9, x=.4, y=-.2, b=.5), k(.38, 'skin_l', reach=1, x=.5, y=-.9, b=-.9, w=.2, mark='fwup'), k(.54, x=-.3, y=.1, b=-.2, eye='o'),
         k(.72, x=.1, y=.3, b=.2, eye='^')],
        [(.38, 'sink')], g='use', act=('throw', 'pellets'), when=['pellets<.4'], prefer=['night', 'dusk'], say=["Lobbed. Patter, patter, silence. Dinner is served in the dark.", "Pellets down the well. The old fish will find them."])
    o.r('draw_the_old_one_along_the_wall', 'Drawing a wingtip slowly along the foot of the wall so the sturgeon follows it from end to end at its own pace', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.9, b=.5), k(.18, 'base_l', reach=1, x=.5, y=1.1, b=.6), k(.34, 'base_m', reach=1, x=.7, y=1.2, b=.7, l=1), k(.52, 'base_m', reach=1, x=.9, y=1.2, b=.7),
         k(.7, 'base_r', reach=1, x=1.1, y=1.3, b=.8, r=1), k(.88, eye='^')],
        [(.52, 'lead')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['lap<.7'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.72, dict(lure=1))],
        say=["It took the whole song to cross the tank. Ancient and unhurried.", "Led it a lap. It leads me on all the rest."])
    o.r('pat_the_wall_where_the_snout_rests', 'Patting the wall with the back of a wing where the sturgeon rests its snout, slow as a bedtime stroke', 22, 'wing',
        [k(.08, 'low_r', reach=.4, x=.2, y=.9, b=.5), k(.22, 'low_r', reach=.9, x=.5, y=1.5, b=1.0, mark='pat'), k(.4, 'low_r', reach=1, x=.4, y=1.7, b=1.2, l=1, mark='pat'), k(.58, 'low_r', reach=1, x=.5, y=1.6, b=1.1, r=1, mark='pat'),
         k(.76, 'low_r', reach=.5, x=.3, y=.9, b=.6), k(.9, eye='^')],
        [(.4, 'stroke')], g='use', act=('pat', 'wall'), pick='shyest', prefer=['fish_trust<.8', 'lonely'], obj=[(.2, dict(lure=1)), (.62, dict(lure=1))])
    o.r('tap_the_ledge_for_the_floor_to_hum', 'Tapping a slow toe on the front ledge so the floor hums and the sturgeon turns toward the sound', 20, 'none',
        [k(.06, 'ledge_l', x=.3, y=.6, b=.8, l=1, perch=1), k(.2, 'ledge_l', x=.4, y=.9, b=1.2, r=1, mark='tmp', perch=1), k(.36, 'ledge_l', x=.3, y=.8, b=1.1, l=1, mark='tmp', perch=1), k(.52, 'ledge_l', x=.4, y=.9, b=1.2, r=1, mark='TMP', perch=1),
         k(.7, 'ledge_l', x=.3, y=.5, b=.5, perch=1), k(.88, eye='^')],
        [(.52, 'call')], g='use', act=('tap', 'ledge'), when=['pond_bell<.4'], prefer=['night'])
    o.r('hold_a_flake_up_at_the_water_line', 'Holding one flake pinched in his bill up at the water line until the old sturgeon rises all the way to the top for it', 24, 'none',
        [k(.06, x=.3, y=-.3, w=.2), k(.2, 'skin_l', x=.8, y=-.5, b=-.2, eye='o'), k(.36, 'skin_l', x=1, y=-.8, b=-.4, eye='O', mark='...'), k(.5, 'skin_l', x=1.1, y=-.9, b=-.6, w=.3, l=1, mark='SHLUP'),
         k(.68, x=-.4, y=.1, b=.2, w=.7, eye='>'), k(.86, eye='^')],
        [(.5, 'rise')], g='use', act=('lift', 'flake'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.62, dict(lure=1))],
        say=["Came all the way up for a flake. Took thirty years of effort.", "Rare sight. Up, snap, gone. Back to the floor."])
    # ---------------- play
    o.r('race_it_down_the_wall_and_win', 'Racing the sturgeon down the length of the wall at a brisk walk and winning by a full lap', 20, 'none',
        [k(.05, 'base_l', x=.6, y=.3, b=.2), k(.2, 'low_l', x=1.2, y=.4, b=-.6, l=1, w=.4), k(.36, 'high_m', x=1.4, y=.3, b=.3, r=1, w=.6), k(.52, 'low_r', x=1.7, y=.4, b=-.8, l=1, w=.8, mark='hup'),
         k(.68, 'base_r', x=1.6, y=.4, b=.4, r=1, w=.7, eye='@', mark='WON'), k(.84, 'base_r', x=.4, y=.6, b=.5, eye='^')],
        [(.52, 'fun')], g='play', act=('race', 'wall'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.56, dict(lure=1)), (.74, dict(lure=1))],
        say=["Won by a lap. It was not aware of the race.", "Victory by walking. It never even clocked me."])
    o.r('hunt_the_old_one_through_the_dark', 'Hunting along the wall in the dark for the sturgeon, bill bobbing at each shadow that might be armour', 22, 'none',
        [k(.06, 'base_l', x=.8, y=1.0, b=.6), k(.2, 'low_l', x=1.2, y=1.4, b=.9, eye='o', mark='?'), k(.34, 'high_l', x=1.3, y=1.2, b=.8, eye='o', mark='?'), k(.5, 'high_m', x=1.4, y=1.3, b=.9, l=1, mark='?'),
         k(.66, 'low_r', x=1.5, y=1.5, b=1.1, eye='O', mark='there!'), k(.84, x=.4, y=.4, eye='^')],
        [], g='play', act=('seek', 'sturgeon'), pick='shyest', prefer=['young', 'curious'], when=['night'], obj=[(.66, dict(lure=1)), (.84, dict(lure=1))])
    o.r('hop_the_ledge_beside_its_slow_pass', 'Hopping from foot to foot along the front ledge, keeping pace with its slow pass along the wall', 22, 'none',
        [k(.06, 'ledge_l', x=.3, y=.4, b=.4, l=1, perch=1), k(.2, 'ledge_l', x=.5, y=-.2, b=-.9, w=.6, r=1, perch=1), k(.34, 'ledge_m', x=.6, y=.6, b=.8, l=1, perch=1), k(.5, 'ledge_m', x=.5, y=-.3, b=-1.0, w=.8, r=1, perch=1),
         k(.66, 'ledge_r', x=.6, y=.6, b=.8, l=1, perch=1), k(.84, 'ledge_r', x=.4, y=.2, b=.3, perch=1, eye='^')],
        [], g='play', act=('hop', 'ledge'), pick='hungriest', prefer=['young', 'happy'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('draw_a_fish_in_the_breath_fog', 'Breathing a fog patch on the wall and tracing a little fish in it with a wingtip, which the sturgeon noses along', 24, 'wing',
        [k(.06, 'high_m', reach=.4, x=.4, y=.5, b=.3), k(.2, 'high_m', reach=.6, x=.9, y=.9, b=.6, mark='haaa'), k(.34, 'high_m', reach=1, x=.5, y=.5, b=.4, mark='~~'), k(.5, 'low_r', reach=1, x=.6, y=.8, b=.6, l=1, mark='><>'),
         k(.68, 'low_r', reach=1, x=.5, y=.9, b=.7, r=1), k(.86, eye='^')],
        [], g='play', act=('blow', 'fog'), pick='shyest', prefer=['happy', 'curious'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))],
        say=["Drew a fish. The fish looked at the fish. Neither impressed.", "My art career begins in breath."])
    o.r('chase_the_shadow_along_the_floor_line', 'Chasing the long armoured shadow along the floor line with a wingtip, never catching up with it', 20, 'wing',
        [k(.07, 'base_l', reach=.6, x=.5, y=.8, b=.4), k(.2, 'base_m', reach=1, x=1.1, y=.6, b=.3, l=1, mark='fwp'), k(.36, 'base_r', reach=1, x=-.4, y=.9, b=.6, r=1, mark='fwp'), k(.52, 'base_m', reach=1, x=1.2, y=.7, b=.4, l=1),
         k(.7, 'base_l', reach=1, x=1.3, y=.8, b=.5, eye='@'), k(.86, y=.5, eye='-')],
        [], g='play', act=('chase', 'shadow'), pick='hungriest', prefer=['happy', 'young'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('waltz_the_ledge_at_its_pace', 'Waltzing very slowly along the front ledge, one step to each sweep of the old fish\'s tail', 26, 'none',
        [k(.05, 'ledge_l', x=.2, y=.2, b=.3, perch=1), k(.18, 'ledge_l', x=.5, y=.1, b=-.4, w=.5, l=1, perch=1), k(.32, 'ledge_m', x=.3, y=.4, b=.6, w=.2, perch=1), k(.46, 'ledge_m', x=.5, y=0, b=-.5, w=.6, r=1, perch=1),
         k(.62, 'ledge_r', x=.3, y=.5, b=.7, perch=1), k(.8, 'ledge_r', x=.4, y=0, b=-.3, w=.4, perch=1, eye='^')],
        [(.46, 'fun')], g='play', act=('dance', 'ledge'), prefer=['happy', 'lonely'], when=['night'])
    # ---------------- test
    o.r('measure_it_in_wing_spans', 'Measuring the sturgeon along the wall with his wing, spanning it out and counting spans aloud until it runs out of wall', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.6, b=.3, mark='1'), k(.16, 'low_l', reach=1, x=.6, y=.9, b=.6, mark='2'), k(.3, 'high_l', reach=1, x=.6, y=.8, b=.5, mark='3'), k(.44, 'high_m', reach=1, x=.7, y=.9, b=.6, l=1, mark='4'),
         k(.58, 'low_r', reach=1, x=.8, y=1.0, b=.7, mark='5'), k(.72, 'base_r', reach=1, x=.9, y=1.1, b=.8, r=1, mark='6!'), k(.9, eye='O', mark='long')],
        [], g='test', act=('measure', 'length'), pick='hungriest', prefer=['curious'], obj=[(.2, dict(lure=1)), (.45, dict(lure=1)), (.7, dict(lure=1))],
        say=["Six wing spans and a bit. It keeps growing between counts.", "Seven spans, if you count the tail it denies."])
    o.r('count_the_plates_down_the_back', 'Counting the armour plates down the long back with a bill dip for each, losing count at the tail', 24, 'none',
        [k(.06, 'low_l', x=.9, y=1.5, b=.7, mark='1'), k(.18, 'low_l', x=1.0, y=1.6, b=.8, mark='4'), k(.3, 'high_l', x=1.1, y=1.6, b=.8, l=1, mark='9'), k(.44, 'high_m', x=1.2, y=1.7, b=.9, mark='14'),
         k(.58, 'low_r', x=1.3, y=1.8, b=1, r=1, mark='19?'), k(.72, x=-.4, y=.2, b=-.1, w=.4, eye='>', mark='again'), k(.88, eye='-')],
        [], g='test', act=('count', 'plates'), pick='shyest', prefer=['curious'], obj=[(.15, dict(lure=1)), (.5, dict(lure=1)), (.66, dict(lure=1))])
    o.r('lay_an_ear_to_the_ledge_for_the_floor', 'Laying his head sideways on the front ledge to hear the slow drag of the old fish\'s belly along the floor', 24, 'none',
        [k(.06, 'ledge_m', x=.1, y=.7, b=.8, perch=1), k(.22, 'ledge_m', x=-.8, y=1.5, b=1.5, eye='-', perch=1), k(.44, 'ledge_m', x=-1.0, y=1.9, b=1.9, eye='-', mark='...', perch=1), k(.66, 'ledge_m', x=-.9, y=1.7, b=1.7, eye='o', mark='shhk', perch=1),
         k(.84, 'ledge_m', x=.2, y=.6, b=.5, perch=1, eye='^')],
        [], g='test', act=('listen', 'floor'), prefer=['curious', 'night'])
    o.r('compare_the_age_in_the_scale_rings', 'Holding a wing up to the sturgeon\'s plate rings and comparing them with the ring count his own feathers could claim', 22, 'wing',
        [k(.06, 'low_l', reach=.4, x=.3, y=.7, b=.4), k(.2, 'low_l', reach=1, x=.5, y=1.0, b=.7), k(.36, 'high_l', reach=1, x=.7, y=.9, b=.6, mark='hm'), k(.52, 'high_m', reach=1, x=.6, y=.5, b=.3, r=1, mark='older'),
         k(.7, 'low_r', reach=.7, x=.3, y=.4, b=.2), k(.88, eye='-', mark='sigh')],
        [], g='test', act=('compare', 'age'), pick='hungriest', prefer=['curious', 'young'], obj=[(.25, dict(lure=1)), (.55, dict(lure=1))])
    o.r('peer_at_the_long_whiskers_in_the_dark', 'Peering at the four long barbels feeling along the floor, close enough that his bill fogs the wall', 22, 'none',
        [k(.06, x=.4, y=.8, b=.5), k(.2, 'low_l', x=1.6, y=2.0, b=1.0, eye='o', mark='fog'), k(.36, 'base_m', x=1.8, y=2.4, b=1.3, eye='O'), k(.52, 'base_m', x=1.9, y=2.5, b=1.4, l=1, mark='twitch'),
         k(.7, 'base_r', x=1.5, y=2.0, b=1.0, r=1), k(.86, eye='-')],
        [], g='test', act=('peer', 'barbels'), pick='shyest', when=['night'], prefer=['curious'], obj=[(.2, dict(lure=1)), (.55, dict(lure=1))])
    o.r('sniff_the_brine_at_the_wall_seam', 'Sniffing the brine along the seam where the wall meets the floor, then sneezing at the salt', 18, 'none',
        [k(.07, 'base_l', x=.5, y=1.2, b=.6), k(.2, 'base_l', x=1.4, y=2.0, b=1.0, mark='snf'), k(.38, 'base_m', x=1.6, y=2.2, b=1.2, eye='-', mark='snf'), k(.56, x=-1.1, y=-.7, b=-.4, w=.7, eye='>', mark='ACHOO'),
         k(.76, x=.1, y=.3, b=.2, eye='-')],
        [], g='test', act=('sniff', 'brine'), prefer=['curious', 'young'])
    o.r('count_the_laps_from_the_ledge', 'Counting the sturgeon\'s laps from the ledge with a toe lift for each, the whole tank taking a lazy hour', 26, 'none',
        [k(.05, 'ledge_l', x=.4, y=.7, b=.8, l=1, perch=1), k(.2, 'ledge_l', x=.5, y=.8, b=.9, r=1, perch=1, mark='lap one'), k(.38, 'ledge_m', x=.5, y=.8, b=.9, l=1, perch=1, mark='lap two'), k(.56, 'ledge_m', x=.6, y=.9, b=1, r=1, perch=1, eye='-', mark='lap three'),
         k(.76, 'ledge_r', x=.5, y=.7, b=.8, perch=1, eye='-', mark='...'), k(.9, 'ledge_r', x=.2, y=.3, b=.3, perch=1, eye='^')],
        [], g='test', act=('count', 'laps'), prefer=['curious', 'tired'], when=['lap>.3'])
    # ---------------- rest
    o.r('doze_off_on_the_middle_ledge', 'Dozing off on the middle ledge with his bill on his chest while the old fish makes its rounds', 28, 'none',
        [k(.08, 'ledge_m', x=.2, y=.9, b=.9, eye='-', perch=1), k(.28, 'ledge_m', x=-.5, y=1.6, b=1.6, eye='-', perch=1), k(.52, 'ledge_m', x=-.8, y=2.0, b=2.2, eye='-', mark='zzz', perch=1), k(.76, 'ledge_m', x=-.2, y=.8, b=.8, eye='o', perch=1),
         k(.9, eye='^')],
        [(.52, 'rest')], g='rest', act=('nap', 'ledge'), when=['tired'], prefer=['night'])
    o.r('sit_at_the_lip_in_the_late_dark', 'Sitting at the front lip with his feet tucked, watching the slow shadow turn at the end of the wall', 26, 'none',
        [k(.08, 'lip', x=.2, y=.5, b=.7), k(.3, 'lip', x=-.2, y=.9, b=1.4, eye='-'), k(.55, 'lip', x=-.4, y=1.1, b=1.8, eye='o'), k(.78, 'lip', x=.4, y=.4, b=.6, l=1, eye='^')],
        [(.55, 'rest')], g='rest', act=('sit', 'lip'), when=['night_late'], prefer=['tired', 'lonely'])
    o.r('wait_for_the_whiskers_at_the_base', 'Waiting stock-still by the base of the wall for the long whiskers to come feeling along it', 24, 'none',
        [k(.08, 'base_m', x=.9, y=1.5, b=.9, eye='o'), k(.3, 'base_m', x=1.0, y=1.7, b=1.1, eye='o'), k(.52, 'base_m', x=1.0, y=1.7, b=1.1, l=1), k(.7, 'base_m', x=1.2, y=1.9, b=1.3, eye='O', mark='...'), k(.88, 'base_m', x=.4, y=.7, b=.4, eye='^')],
        [], g='rest', act=('wait', 'whiskers'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('lean_on_the_left_pier_post', 'Leaning his shoulder against the left pier post while the old fish does the rounds', 22, 'none',
        [k(.07, 'pier_l', x=-.4, y=.3, b=.5), k(.24, 'pier_l', x=-.8, y=.6, b=.9, eye='-'), k(.46, 'pier_l', x=-1.0, y=.8, b=1.2, eye='-', mark='...'), k(.66, 'pier_l', x=-.7, y=.6, b=.8, r=1), k(.84, x=.4, y=.2, b=.2, eye='O')],
        [], g='rest', act=('lean', 'post'), prefer=['tired', 'sad'])
    o.r('sulk_when_the_old_one_stays_down', 'Sulking at the wall with his tail to the water because the sturgeon has not shown itself all evening', 24, 'none',
        [k(.08, x=-.7, y=.4, b=.7), k(.26, 'base_r', x=-1.6, y=.9, b=1.4, eye='-'), k(.5, 'base_r', x=-2, y=1.2, b=2.0, eye='-', mark='humph'), k(.72, 'base_r', x=-1.7, y=1.0, b=1.7, l=1), k(.88, x=-.5, y=.3, eye='-')],
        [], g='rest', act=('sulk', 'tank'), when=['sad'])
    # ---------------- weather
    o.r('chip_the_frost_from_the_wall_foot', 'Chipping the frost from the foot of the wall with his bill so the sturgeon\'s long night is clearly seen', 22, 'none',
        [k(.06, 'ledge_l', x=.6, y=.9, b=.4, perch=1), k(.18, 'base_l', x=1.5, y=2.0, b=.8, mark='tk'), k(.32, 'base_l', x=1.7, y=2.3, b=1.1, r=1, mark='TK'), k(.46, 'base_m', x=1.6, y=2.2, b=1, l=1, mark='crk'),
         k(.62, 'low_l', x=1.5, y=1.8, b=.9, r=1, mark='CRK'), k(.8, x=.4, y=.3, eye='^')],
        [(.46, 'crack')], g='weather', act=('chip', 'frost'), when=['pond_ice>.3'])
    o.r('scrape_the_hoar_from_the_pier_post', 'Scraping the hoar off the right pier post with a wing so he can lean against it without his feathers sticking', 20, 'wing',
        [k(.08, 'pier_r', reach=.5, x=.3, y=.4, b=.2), k(.24, 'pier_r', reach=1, x=.6, y=.8, b=.5, mark='skrr'), k(.4, 'pier_r', reach=1, x=.7, y=.9, b=.6, l=1, mark='skrr'), k(.58, 'pier_r', reach=1, x=.5, y=.7, b=.5, r=1),
         k(.76, 'low_r', reach=.6, x=.4, y=.5, b=.3), k(.9, eye='-')],
        [(.4, 'thaw')], g='weather', act=('scrape', 'hoar'), when=['pond_ice>.3'])
    o.r('shelter_by_the_post_from_the_rain', 'Sheltering at the right pier post with his bill tucked while the rain pocks the tank and the sturgeon rolls on through it', 30, 'none',
        [k(.08, 'pier_r', x=-.5, y=.7, b=.8), k(.28, 'pier_r', x=-1.0, y=1.6, b=1.5, eye='-'), k(.52, 'pier_r', x=-1.2, y=2.0, b=1.9, eye='-', mark='pit'), k(.76, 'pier_r', x=-1.1, y=1.9, b=1.7, l=1, mark='pat'),
         k(.9, x=.2, y=.2, eye='^')],
        [], g='weather', act=('shelter', 'post'), when=['wet'])
    o.r('warm_each_foot_on_the_sunny_ledge', 'Warming one foot and then the other on the sun-baked right ledge while the old fish sleeps below', 20, 'none',
        [k(.08, 'ledge_r', x=.3, y=.4, b=.7, l=1, perch=1), k(.3, 'ledge_r', x=.2, y=.7, b=1.0, l=1, eye='-', perch=1), k(.54, 'ledge_r', x=.2, y=.7, b=1.0, r=1, eye='-', mark='ahh', perch=1), k(.76, 'ledge_r', x=.4, y=.3, b=.4, w=.3, perch=1, eye='^')],
        [], g='weather', act=('warm', 'foot'), when=['sun'], prefer=['tired'])
    o.r('brace_at_the_pier_in_the_gust', 'Bracing his chest into the gust at the right pier so the leaves skid past the tank without dropping in', 18, 'none',
        [k(.06, 'pier_r', x=1.0, y=.1, b=1.0), k(.2, 'pier_r', x=1.5, y=.4, b=1.5, w=.5, mark='whoo'), k(.38, 'pier_r', x=1.7, y=.5, b=1.7, l=1, w=.9), k(.56, 'pier_r', x=1.5, y=.3, b=1.3, r=1, w=.7), k(.76, 'pier_r', x=.8, y=.2, b=.7),
         k(.9, eye='-')],
        [], g='weather', act=('brace', 'gust'), when=['windy'])
    o.r('cool_his_bill_at_the_wall_on_a_hot_noon', 'Cooling his bill against the wall on a hot noon, then his cheek, then the other cheek, while the deep one stays down', 20, 'none',
        [k(.07, 'high_l', x=.9, y=.6, b=.5), k(.22, 'high_l', x=1.3, y=.9, b=.8, eye='-', mark='ahh'), k(.4, 'high_l', x=1.1, y=1.0, b=.9, eye='-', l=1), k(.6, 'high_m', x=1.3, y=.9, b=.8, eye='-', r=1), k(.8, x=.4, y=.3, eye='^')],
        [], g='weather', act=('cool', 'bill'), when=['warm'], prefer=['summer'])
    # ---------------- show
    o.r('bow_to_the_ancient_one', 'Bowing deeply to the ancient fish as it glides by the wall, a long and formal bill-dip', 18, 'none',
        [k(.08, 'low_l', x=.6, y=1.1, b=.9), k(.26, 'low_l', x=1.3, y=2.6, b=2.1, eye='-'), k(.5, 'low_l', x=1.4, y=2.8, b=2.3, eye='-', mark='your honour'), k(.7, 'low_l', x=.7, y=.7, b=.6), k(.86, x=.1, y=-.5, w=.7, eye='^')],
        [], g='show', act=('bow', 'sturgeon'), pick='hungriest', prefer=['happy'], obj=[(.26, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed. It turned its head three degrees. A great honour.", "Respects paid. In this tank, the old fish is the landlord."])
    o.r('present_the_old_one_to_the_dark', 'Presenting the old fish to the dark with a grand wing sweep along the wall, a ringmaster introducing a monument', 22, 'wing',
        [k(.07, 'base_l', reach=.4, x=.1, y=.2), k(.24, 'low_l', reach=.9, x=.3, y=-.3, b=-.3), k(.42, 'high_m', reach=1, x=.3, y=-.5, b=-.4, mark='ladies and'), k(.6, 'low_r', reach=1, x=.4, y=-.3, b=-.2, l=1, mark='gentle-fish'),
         k(.78, 'base_r', reach=.6, x=.4, y=0), k(.92, eye='^')],
        [], g='show', act=('present', 'sturgeon'), pick='shyest', prefer=['happy'], obj=[(.45, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_for_the_blunt_nose', 'Arguing with the sturgeon over whose nose is the nobler one, bill to snout against the wall', 20, 'wing',
        [k(.08, 'low_r', reach=.5, x=.7, y=.9, b=.6), k(.24, 'low_r', reach=1, x=1.2, y=.8, b=.5, mark='MINE'), k(.4, 'low_r', reach=1, x=1.3, y=.7, b=.4, l=1, mark='MINE'), k(.56, 'low_r', reach=.6, x=.6, y=1.0, b=.8, r=1),
         k(.74, 'low_r', reach=1, x=1.2, y=.8, b=.5, mark='NO, MINE'), k(.9, eye='-')],
        [], g='show', act=('argue', 'nose'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["A prehistoric nose against a duck bill. The nose is older.", "Lost on seniority."])
    o.r('pose_on_the_ledge_like_a_prow', 'Posing on the left ledge like a ship\'s prow, bill high, while the old fish slides along the wall like a submarine', 18, 'none',
        [k(.06, 'ledge_l', x=.3, y=-.3, w=.3, perch=1), k(.24, 'ledge_l', x=.8, y=-.7, b=-.4, w=.6, perch=1), k(.5, 'ledge_l', x=1.0, y=-1.0, b=-.7, w=1, perch=1, eye='^', mark='full ahead'), k(.74, 'ledge_l', x=.3, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'ledge'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sing_the_old_one_a_slow_hymn', 'Singing the old fish a slow hymn in a low voice, every note held as long as one of its own laps', 26, 'none',
        [k(.06, 'low_r', x=.8, y=1.0, b=.8), k(.22, 'low_r', x=1.1, y=1.8, b=1.5, eye='-', mark='laaa'), k(.42, 'base_r', x=1.3, y=2.1, b=1.9, eye='-', mark='laaaa'), k(.62, 'base_m', x=1.2, y=1.9, b=1.6, eye='-', mark='laaa', w=.3),
         k(.82, x=.4, y=.5, b=.3, eye='^')],
        [], g='show', act=('sing', 'hymn'), pick='shyest', when=['night'], prefer=['lonely', 'sad'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        say=["It stayed for the verse. Fell asleep at the chorus.", "Low and long, like the fish. We both held it."])
    # ---------------- mishap
    o.r('slip_on_the_wet_ledge', 'Slipping on the rain-wet ledge, feet skating out in both directions, and slapping the wall to stop', 16, 'none',
        [k(.07, 'ledge_r', x=.6, y=.6, b=.5, perch=1), k(.2, 'ledge_r', x=1.3, y=-.3, b=-.8, l=1, r=1, w=1, mark='whoa!', perch=1), k(.34, 'low_r', x=1.7, y=1.3, b=1.8, w=.7, eye='O', mark='SLAP'), k(.52, 'ledge_r', x=.7, y=.8, b=.9, perch=1, eye='>'),
         k(.7, x=.2, y=.2, b=.2, eye='-')],
        [], g='mishap', act=('slip', 'ledge'), when=['wet'], prefer=['young'])
    o.r('head_stuck_between_two_pier_rungs', 'Poking his head between two rungs of the left pier after a flicker of armour and having to wriggle out', 24, 'none',
        [k(.06, x=.9, y=.5, b=.5), k(.2, 'pier_l', x=1.9, y=.1, b=1.0, eye='O'), k(.38, 'pier_l', x=2.1, y=.2, b=1.3, l=1, eye='@', mark='mmph'), k(.56, 'pier_l', x=2.0, y=.3, b=1.2, r=1, w=.5, mark='mf'),
         k(.7, 'pier_l', x=1.5, y=-.4, b=-.8, w=1, mark='POP'), k(.86, x=1.1, y=1.0, b=.7, eye='-')],
        [], g='mishap', act=('stuck', 'rungs'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_wall_following_the_snout', 'Following the snout along the wall with his eyes only and bumping the wall hard with his bill', 18, 'none',
        [k(.06, 'base_l', x=.6, y=.7, b=.4), k(.2, 'low_l', x=.7, y=.8, b=.5, l=1), k(.34, 'high_m', x=.8, y=.6, b=.4, r=1), k(.5, 'high_m', x=1.8, y=.2, b=1.4, eye='@', mark='BONK'), k(.66, 'high_m', x=-1.0, y=.3, b=.2, w=.8, eye='x'),
         k(.84, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'wall'), prefer=['curious'], when=['night'])
    o.r('jump_back_from_the_rising_snout', 'Jumping back with a squawk when the great snout surges up the wall right at his bill and the whole armoured body rolls', 18, 'none',
        [k(.06, 'base_m', x=1.0, y=1.8, b=.9), k(.18, 'base_m', x=1.3, y=2.1, b=1.2, eye='o', mark='...'), k(.28, x=-1.4, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='GAH'), k(.44, x=-.8, y=.3, b=-.1, w=.7, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'snout'), pick='hungriest', prefer=['young', 'curious'], obj=[(.18, dict(lure=1)), (.45, dict(lure=1))],
        say=["Thirty years asleep, then it surges. Fair play.", "My feathers have not recovered."])
    o.r('stamp_the_silt_cloud_flat', 'Stamping at the cloud on the floor line that rose when he threw the pellets, as if the silt would obey', 16, 'none',
        [k(.06, 'ledge_m', x=.7, y=.9, b=.5, perch=1), k(.18, 'ledge_m', x=.6, y=0, b=-1.1, l=1, mark='STMP', perch=1), k(.3, 'ledge_m', x=.7, y=.6, b=.6, perch=1), k(.42, 'ledge_m', x=.6, y=0, b=-1.1, r=1, mark='STMP', perch=1),
         k(.56, 'ledge_m', x=.7, y=.6, b=.6, perch=1), k(.7, 'ledge_m', x=.6, y=-.1, b=-1.3, l=1, r=1, mark='STMP!', perch=1), k(.88, eye='-')],
        [], g='mishap', act=('stamp', 'cloud'), when=['silt>.3'], prefer=['grumpy'])
    # ---------------- duets (a friend takes their own part)
    o.r('walk_the_old_one_down_the_wall_between_us', 'Drawing the old fish from one end of the wall while a friend draws from the other, the sturgeon sliding between the two wingtips', 28, 'wing',
        [k(.05, 'base_l', reach=.5, x=.3, y=.8, b=.4), k(.2, 'low_l', reach=1, x=.5, y=1.0, b=.6), k(.38, 'high_m', reach=1, x=.7, y=.9, b=.6, l=1), k(.56, 'low_r', reach=1, x=.8, y=1.0, b=.7, r=1), k(.76, 'base_r', reach=1, x=.9, y=1.1, b=.8),
         k(.9, eye='^')],
        [(.38, 'lead')], g='use', act=('guard', 'wall'), pick='hungriest', when=['lap<.7'], prefer=['happy'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.62, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.1, 'base_r', x=.4, y=.8, b=.4), k(.28, 'low_r', x=.6, y=1.0, b=.6, l=1), k(.46, 'high_m', x=.8, y=1.0, b=.6, r=1), k(.66, 'low_l', x=.9, y=1.1, b=.7), k(.84, 'base_l', x=.5, y=.7, b=.4, eye='^')],
        say=["Two ducks, one fish, no agreement. It chose the middle.", "Pulled from both ends. The old fish took neither."])
    o.r('swap_pellets_through_the_dark_with_a_friend', 'Pressing pellets to the wall in turn with a friend at the far end, the old fish crossing the dark to each in order', 26, 'none',
        [k(.05, 'low_l', x=.7, y=1.0, b=.6), k(.2, 'low_l', x=1.6, y=1.9, b=.9, eye='o', mark='tp'), k(.36, 'low_l', x=1.4, y=1.2, b=.6, w=.4), k(.52, 'high_m', x=1.7, y=1.7, b=.9, mark='tp'), k(.7, 'high_m', x=.8, y=.7, b=.4, eye='O'),
         k(.86, eye='^')],
        [(.52, 'feed')], g='play', act=('catch', 'pellets'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.25, dict(lure=1)), (.56, dict(lure=1))],
        duo=[k(.12, 'low_r', x=.6, y=.9, b=.5), k(.3, 'low_r', x=1.5, y=1.8, b=.8, mark='tp'), k(.46, 'low_r', x=1.3, y=1.1, b=.5), k(.62, 'low_r', x=1.6, y=1.7, b=.9, l=1, mark='tp'), k(.8, eye='^')])
    o.r('trade_guesses_on_its_age_with_a_friend', 'Trading guesses on the old fish\'s age with a friend at the other end of the wall, each guess louder and older than the last', 24, 'none',
        [k(.06, 'base_l', x=.7, y=.9, b=.4, mark='fifty'), k(.2, 'low_l', x=.9, y=1.0, b=.6, mark='eighty'), k(.36, 'high_l', x=1.1, y=1.0, b=.7, l=1, mark='a century'), k(.52, 'high_l', x=1.2, y=.6, b=.5, w=.5, mark='two!'),
         k(.7, 'low_l', x=.7, y=.7, b=.4, eye='-', mark='fine'), k(.86, eye='^')],
        [], g='test', act=('weigh', 'years'), pick='shyest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.1, 'base_r', x=.7, y=.9, b=.4, mark='sixty'), k(.28, 'low_r', x=.9, y=1.0, b=.6, mark='a hundred'), k(.44, 'high_m', x=1.1, y=1.0, b=.7, r=1, mark='two!'), k(.62, 'low_r', x=.8, y=.9, b=.5, eye='-'), k(.8, eye='^')],
        say=["Two hundred, by consensus. The fish stayed silent. A good sign.", "Settled on 'old'. The fish confirmed with a long blink."])
    return done(o)


def pufferfish():
    # Pufferfish: small, slow, mid-water, fused beak, balloons when startled. Lives in the sea tank; Cheese works from the edge (wall, coping, ledge). Own state:
    # puff (how inflated it is: a startle sets it, it sinks back slowly, drawn), nerve (how jumpy it is: startles raise it, calm lowers it), crumbs (hard crumbs
    # still floating for its beak: drawn).
    o = Obj('pufferfish', 'keeping', on='infinity_pool',
            fields=dict(puff=(0, 0, 1), nerve=(0, 0, 1), crumbs=(0, 0, 1)),
            physics=[('puff', 'rate', -.003, 'always'), ('nerve', 'rate', -.0004, 'always'), ('crumbs', 'rate', -.002, 'always')],
            effects=dict(scrub=[('keeping.algae', 'mul', .5)], rake=[('keeping.leaves', 'mul', .35)], polish=[('keeping.clarity', 'add', .15)], tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)],
                         husk=[('crumbs', 'mul', .2)], call=[('keeping.bell', 'add', .5)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12), ('crumbs', 'set', 1)],
                         crumble=[('crumbs', 'set', 1), ('keeping.flakes', 'add', .35)], lead=[('subject.trust', 'add', .1), ('nerve', 'mul', .6)],
                         stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)], startle=[('puff', 'set', 1), ('nerve', 'add', .3)],
                         soothe=[('nerve', 'mul', .3), ('puff', 'mul', .4), ('subject.trust', 'add', .1)], snap=[('subject.hunger', 'add', -.2), ('subject.mood', 'add', .15)],
                         crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('puff', .3, '*(O)*', 'bob_m', 'water'), ('crumbs', .3, '.o.o.', 'puff_r', 'dust'), ('pond_flakes', .3, ".':.'", 'skin_m', 'dust'), ('pond_leaves', .3, ';"~;"', 'top_m', 'leaf'),
                   ('pond_ice', .3, '*-*-*', 'top_l', 'frost'), ('pond_algae', .3, '"v"v"', 'base_m', 'plant')],
            anchors=dict(puff_l=Q(36, 43), puff_r=Q(80, 43), bob_l=Q(20, 43), bob_m=Q(58, 43), bob_r=Q(98, 43), top_l=Q(30, 37), top_m=Q(58, 37), skin_m=Q(68, 34), sign=Q(24, 33),
                         base_m=Q(62, 46), coping=Q(40, 28), ledge_l=Q(30, 49, 'surface'), ledge_r=Q(92, 49, 'surface'), lip=Q(80, 52, 'surface'), pier_l=Q(10, 41), pier_r=Q(110, 41)))
    # ---------------- care
    o.r('wipe_the_wall_clean_at_beak_height', 'Wiping the green fuzz off the wall at beak height in neat overlapping rows so its tiny eyes can see out', 22, 'wing',
        [k(.07, 'bob_l', reach=.4, x=.1, y=.3, b=.2), k(.19, 'bob_l', reach=1, x=.3, y=.4, b=.4, mark='wip'), k(.31, 'bob_m', reach=1, x=.4, y=.5, b=.5, l=1, mark='wip'), k(.43, 'bob_r', reach=1, x=.5, y=.5, b=.4, mark='wip'),
         k(.57, 'puff_r', reach=1, x=.6, y=.8, b=.7, r=1, mark='wip'), k(.72, 'puff_l', reach=1, x=.5, y=.8, b=.6), k(.9, eye='^')],
        [(.43, 'scrub')], g='care', act=('wipe', 'algae'), when=['pond_algae>.4'], say=["Eyes unblocked. It looked at me and promptly puffed. Gratitude, probably.", "Clean wall. Same fish. Same opinion of me."])
    o.r('rake_the_floating_leaves_with_a_reed_tip', 'Raking the floating leaves toward the left corner with the tip of a reed held out over the coping', 24, 'reed',
        [k(.07, 'skin_m', reach=.4, x=.2, y=-.2), k(.21, 'coping', reach=1, x=.4, y=-.4, b=-.3, mark='rk'), k(.35, 'top_m', reach=1, x=.6, y=-.3, b=-.1, l=1, mark='rk'), k(.5, 'top_l', reach=1, x=.8, y=-.2, b=.1, r=1, mark='rk'),
         k(.67, 'top_l', reach=.7, x=.3, y=-.1, b=-.2), k(.84, eye='-')],
        [(.5, 'rake')], g='care', act=('rake', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'])
    o.r('polish_a_porthole_at_eye_level', 'Polishing a clear round porthole in the wall with the wing tip so he can look the puffer in both eyes', 20, 'wing',
        [k(.08, 'bob_m', reach=.5, x=.3, y=.4, b=.3), k(.2, 'bob_m', reach=1, x=.5, y=.3, b=.5, mark='sqk'), k(.34, 'bob_r', reach=1, x=.6, y=.4, b=.4, r=1, mark='sqk'), k(.48, 'bob_r', reach=1, x=.5, y=.5, b=.5, l=1, mark='sqk'),
         k(.64, 'bob_m', reach=1, x=.7, y=.6, b=.5), k(.8, eye='o', mark='clear')],
        [(.48, 'polish')], g='care', act=('polish', 'wall'), when=['pond_clarity<.6'])
    o.r('peer_for_any_bent_spine', 'Peering at the little spines along a puffed flank for any bent or broken one, bill an inch from the wall', 22, 'none',
        [k(.06, x=.4, y=.5, b=.3), k(.18, 'bob_l', x=1.3, y=1.3, b=.7, eye='o'), k(.32, 'bob_l', x=1.5, y=1.5, b=.9, eye='O', mark='hm'), k(.48, 'bob_m', x=1.4, y=1.5, b=.9, r=1), k(.62, 'bob_r', x=1.5, y=1.6, b=1, l=1, mark='ok'),
         k(.8, x=.5, y=.6, b=.3, w=.4, eye='^')],
        [(.48, 'tend')], g='care', act=('peer', 'spines'), pick='shyest', when=['fish_health<.8'], prefer=['puff>.3'], obj=[(.2, dict(lure=1)), (.5, dict(lure=1)), (.64, dict(lure=1))],
        say=["All spines straight. Alarming for a creature that cannot hold a grudge.", "No bent ones. It has better posture than me."])
    o.r('sweep_the_beak_crumbs_off_the_lip', 'Sweeping the soggy beak crumbs off the front lip and over the edge with the back of a wing', 18, 'wing',
        [k(.08, 'lip', reach=.4, x=.2, y=.5, b=.4, perch=1), k(.24, 'lip', reach=1, x=.5, y=.6, b=.9, l=1, mark='sh', perch=1), k(.42, 'lip', reach=1, x=.6, y=.5, b=.7, r=1, mark='sh', perch=1), k(.6, 'lip', reach=.6, x=.3, y=.4, b=.4, perch=1),
         k(.8, eye='-')],
        [(.42, 'husk')], g='care', act=('sweep', 'crumbs'), when=['crumbs>.3'])
    # ---------------- use
    o.r('knock_two_light_on_the_wall', 'Knocking two light taps on the wall with a wing knuckle, the soft bell it only half minds', 16, 'wing',
        [k(.08, 'puff_l', reach=.4, x=.2, y=.7, b=.4), k(.2, 'puff_l', reach=1, x=.4, y=.9, b=.6, mark='tk'), k(.32, 'puff_l', reach=.4, x=.1, y=.6, b=.3), k(.46, 'puff_l', reach=1, x=.4, y=.9, b=.6, l=1, mark='tk'),
         k(.64, eye='^')],
        [(.46, 'call')], g='use', act=('knock', 'wall'), when=['pond_bell<.4'], prefer=['dusk', 'dawn'])
    o.r('press_a_hard_crumb_to_the_wall', 'Pressing a hard crumb flat to the wall with his bill, the fused beak chomping at it from the other side', 22, 'none',
        [k(.06, x=.5, y=.8, b=.4), k(.18, 'bob_m', x=1.5, y=1.5, b=.8, eye='o', mark='...'), k(.32, 'bob_m', x=1.7, y=1.7, b=1, eye='O', mark='CRNCH'), k(.46, 'bob_m', x=1.6, y=1.6, b=.9, l=1, mark='crnch'),
         k(.64, x=.5, y=.8, b=.4, w=.4, eye='^'), k(.84, eye='-')],
        [(.32, 'feed')], g='use', act=('press', 'crumb'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.18, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=0))],
        say=["Crunched it like a tiny wood chipper.", "A beak made for rocks, eating my crumb with feeling."])
    o.r('scatter_hard_crumbs_over_the_coping', 'Scattering a pinch of hard crumbs up and over the coping so they bob in the water for the beak to hunt', 18, 'wing',
        [k(.09, 'skin_m', reach=.3, x=.1, y=.1), k(.23, 'skin_m', reach=.9, x=.3, y=-.3, b=.6), k(.4, 'skin_m', reach=1, x=.5, y=-.8, b=-.8, mark='fwp'), k(.56, x=-.2, y=0, b=-.1, eye='o'), k(.76, eye='^')],
        [(.4, 'crumble')], g='use', act=('throw', 'crumbs'), when=['pond_flakes<.4', 'crumbs<.4'], prefer=['happy'], say=["Crumbs over the top. Chomp, chomp, tiny ferocity.", "Fed it from above like a god. A small, disappointed god."])
    o.r('walk_it_slowly_along_the_wall', 'Dragging a wingtip along the wall at a slow walk so the puffer ambles after it, nerves quieting as it goes', 26, 'wing',
        [k(.06, 'puff_l', reach=.4, x=.3, y=.7, b=.3), k(.2, 'puff_l', reach=1, x=.5, y=.8, b=.5), k(.36, 'bob_m', reach=1, x=.7, y=.7, b=.4, l=1), k(.54, 'bob_r', reach=1, x=.9, y=.7, b=.4), k(.72, 'puff_r', reach=1, x=1.1, y=.8, b=.5, r=1),
         k(.9, eye='^')],
        [(.54, 'lead')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['nerve>.3'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.54, dict(lure=1)), (.76, dict(lure=1))],
        say=["Walked it round. It forgot to be afraid, which is a start.", "Wing, wall, puffer. Slow therapy."])
    o.r('stroke_the_wall_in_slow_circles', 'Stroking the wall in slow circles with the back of a wing where the puffer hangs near, a lullaby without notes', 22, 'wing',
        [k(.07, 'bob_l', reach=.4, x=.2, y=.5, b=.3), k(.22, 'bob_l', reach=.9, x=.3, y=.7, b=.7, mark='circ'), k(.38, 'bob_l', reach=1, x=.4, y=.8, b=.8, l=1, mark='circ'), k(.54, 'bob_l', reach=1, x=.3, y=.7, b=.7, r=1, mark='circ'),
         k(.72, 'bob_l', reach=.5, x=.2, y=.5, b=.4), k(.9, eye='^')],
        [(.38, 'stroke')], g='use', act=('pat', 'wall'), pick='shyest', prefer=['fish_trust<.8', 'lonely'], obj=[(.2, dict(lure=1)), (.62, dict(lure=1))])
    o.r('prod_the_wall_sharp_to_see_it_pop', 'Prodding the wall once, sharp, with a wingtip just to see the puffer go off like a balloon', 16, 'wing',
        [k(.08, 'bob_m', reach=.4, x=.2, y=.4, b=.2), k(.2, 'bob_m', reach=.4, x=-.2, y=.1, b=-.2, eye='>'), k(.32, 'bob_m', reach=1, x=.9, y=.5, b=.8, mark='BOP'), k(.5, 'bob_m', reach=.5, x=.3, y=.3, b=.2, eye='O', mark='POOF'),
         k(.7, eye='^')],
        [(.32, 'startle')], g='use', act=('prod', 'wall'), pick='shyest', obj=[(.2, dict(lure=1)), (.5, dict(lure=1))], prefer=['curious', 'young'],
        say=["Poof. The wall is now mostly puffer.", "Prodded it once. Balloon season is open.", "That was cheap and I would do it again."])
    o.r('lay_a_calm_wing_flat_on_the_wall', 'Laying one calm wing flat against the wall beside the ballooned puffer, breathing slow until it shrinks', 28, 'wing',
        [k(.06, 'puff_r', reach=.4, x=.3, y=.6, b=.3), k(.2, 'puff_r', reach=1, x=.5, y=.9, b=.8, eye='-'), k(.4, 'puff_r', reach=1, x=.5, y=1.1, b=1.1, eye='-', mark='shhh'), k(.62, 'puff_r', reach=1, x=.5, y=1.0, b=1, l=1, eye='-'),
         k(.8, 'puff_r', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(.4, 'soothe')], g='use', act=('press', 'wing'), pick='shyest', when=['puff>.3'], obj=[(.2, dict(lure=1)), (.6, dict(lure=1))],
        say=["Down it went, one sigh at a time. Contagious.", "Slow breath. The puffer copied me and remembered itself."])
    # ---------------- play
    o.r('puff_up_back_at_the_puffer', 'Puffing his own chest out against the wall in a stand-off, eye to eye with a puffer doing the very same', 20, 'none',
        [k(.06, 'bob_r', x=.4, y=.4, b=.4), k(.18, 'bob_r', x=1.1, y=.1, b=1.6, w=.4, eye='O', mark='HUFF'), k(.32, 'bob_r', x=1.3, y=0, b=2.1, w=.7, l=1, eye='@', mark='HUFF'), k(.5, 'bob_r', x=1.2, y=.1, b=2.3, w=.9, r=1, mark='hmmmf'),
         k(.66, 'bob_r', x=.6, y=.5, b=.7, w=.2, eye='>'), k(.84, eye='-')],
        [(.32, 'startle')], g='play', act=('blow', 'chest'), pick='hungriest', prefer=['young', 'grumpy'], obj=[(.2, dict(lure=1)), (.55, dict(lure=1))],
        say=["Neither of us won. We both turned a bit purple.", "Stand-off. I blinked first. I always blink first."])
    o.r('spin_on_the_ledge_like_a_loose_balloon', 'Spinning on the ledge with his wings floated out like a balloon that has lost its string', 22, 'none',
        [k(.05, 'ledge_l', x=.3, y=.3, b=.3, perch=1), k(.18, 'ledge_l', x=1.0, y=-.5, b=-.6, w=.7, l=1, perch=1), k(.32, 'ledge_l', x=-1.1, y=.2, b=.5, w=.9, r=1, perch=1), k(.46, 'ledge_l', x=1.2, y=-.4, b=-.7, w=1, l=1, perch=1, mark='fwoo'), k(.62, 'ledge_l', x=-.9, y=.5, b=.8, w=.7, r=1, perch=1), k(.8, 'ledge_l', x=.3, y=.9, b=1.2, perch=1, eye='@', mark='dizzy')],
        [(.46, 'fun')], g='play', act=('spin', 'ledge'), prefer=['young', 'happy'], when=['puff>.3'])
    o.r('seek_the_small_one_among_the_bobs', 'Hunting along the wall at mid height for the small one that has tucked itself into a corner and gone invisible', 22, 'none',
        [k(.06, 'bob_l', x=.7, y=.8, b=.5), k(.2, 'puff_l', x=1.1, y=1.2, b=.8, eye='o', mark='?'), k(.34, 'top_l', x=1.2, y=.8, b=.7, eye='o', mark='?'), k(.5, 'top_m', x=1.3, y=.9, b=.8, l=1, mark='?'), k(.64, 'puff_r', x=1.4, y=1.3, b=1, eye='O', mark='there'),
         k(.82, x=.4, y=.4, eye='^')],
        [], g='play', act=('seek', 'puffer'), pick='shyest', prefer=['young', 'curious'], obj=[(.64, dict(lure=1)), (.84, dict(lure=1))])
    o.r('flick_crumbs_for_a_beak_snap_count', 'Flicking hard crumbs over the top one at a time and counting the beak snaps that follow from the wall side', 22, 'wing',
        [k(.06, 'skin_m', reach=.4, x=.2, y=0), k(.18, 'skin_m', reach=1, x=.4, y=-.5, b=-.4, mark='flk'), k(.3, 'skin_m', reach=.5, x=.1, y=.1, b=0, mark='1'), k(.42, 'skin_m', reach=1, x=.4, y=-.5, b=-.4, l=1, mark='flk'),
         k(.55, 'skin_m', reach=.5, x=.1, y=.1, b=0, mark='2'), k(.7, 'skin_m', reach=1, x=.4, y=-.6, b=-.5, r=1, mark='flk'), k(.86, eye='o', mark='3')],
        [(.42, 'snap')], g='play', act=('catch', 'crumbs'), pick='hungriest', prefer=['happy', 'curious'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('send_a_bubble_up_the_wall_to_pop', 'Blowing one fat bubble against the wall and letting it climb past the puffer, which swivels both eyes after it', 20, 'none',
        [k(.06, 'puff_l', x=.5, y=.7, b=.5), k(.2, 'puff_l', x=1.4, y=1.3, b=.9, mark='bbl'), k(.34, 'bob_l', x=1.2, y=.8, b=.6, eye='o'), k(.5, 'top_l', x=1.1, y=.1, b=.3, eye='O', mark='pop'), k(.68, 'top_l', x=.4, y=.2, b=.2, eye='^'),
         k(.86, eye='-')],
        [], g='play', act=('blow', 'bubble'), pick='shyest', prefer=['happy', 'young'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('chase_the_glint_of_a_spine', 'Chasing the little glint from a spine across the wall with a wingtip, quick dabs that never land', 18, 'wing',
        [k(.06, 'puff_l', reach=.6, x=.5, y=.7, b=.4), k(.18, 'bob_l', reach=1, x=.9, y=.5, b=.2, l=1, mark='fwp'), k(.3, 'bob_m', reach=1, x=-.4, y=.7, b=.5, r=1, mark='fwp'), k(.44, 'bob_r', reach=1, x=1.0, y=.5, b=.2, l=1),
         k(.6, 'puff_r', reach=1, x=1.1, y=.6, b=.4, eye='@'), k(.8, y=.4, eye='-')],
        [], g='play', act=('chase', 'spine'), pick='hungriest', prefer=['young', 'happy'], when=['puff>.3'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- test
    o.r('measure_the_balloon_against_a_wing', 'Measuring how wide the ballooned puffer is by spreading a wing against the wall, then letting it settle and measuring again', 26, 'wing',
        [k(.05, 'bob_m', reach=.5, x=.3, y=.5, b=.3), k(.18, 'bob_l', reach=1, x=.5, y=.5, b=.4, mark='this'), k(.3, 'bob_r', reach=1, x=.6, y=.5, b=.4, l=1, mark='wide'), k(.46, 'bob_m', reach=.5, x=.2, y=.6, b=.5, eye='-', mark='...'),
         k(.62, 'bob_m', reach=1, x=.4, y=.7, b=.6, r=1, mark='less'), k(.8, eye='O', mark='half')],
        [], g='test', act=('measure', 'balloon'), pick='hungriest', when=['puff>.3'], prefer=['curious'], obj=[(.25, dict(lure=1)), (.55, dict(lure=1))],
        say=["Three wing widths ballooned, one and a half relaxed. Physics is rude.", "It doubles and halves on a whim. Not a reliable specimen."])
    o.r('count_the_spines_one_by_one', 'Counting the spines along a puffed side with a bill dip each time, keeping pace with a fish that will not hold still', 22, 'none',
        [k(.05, 'bob_l', x=1.0, y=1.2, b=.5, mark='1'), k(.16, 'bob_l', x=1.1, y=1.3, b=.6, mark='6'), k(.28, 'bob_m', x=1.2, y=1.3, b=.7, l=1, mark='13'), k(.42, 'bob_m', x=1.3, y=1.4, b=.8, mark='20'), k(.56, 'bob_r', x=1.4, y=1.5, b=.9, r=1, mark='27?'),
         k(.7, x=-.3, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.88, eye='-')],
        [], g='test', act=('count', 'spines'), pick='shyest', prefer=['curious'], obj=[(.15, dict(lure=1)), (.5, dict(lure=1)), (.62, dict(lure=1))])
    o.r('compare_his_chest_with_its_balloon', 'Comparing his puffed-out chest with the puffer\'s, wing across his own front and then across the wall', 24, 'wing',
        [k(.06, 'bob_m', reach=.4, x=.3, y=.4, b=.4), k(.2, 'bob_m', reach=.4, x=.2, y=.2, b=1.5, mark='mine'), k(.36, 'bob_m', reach=1, x=.5, y=.5, b=.5, l=1, mark='yours'), k(.52, 'bob_m', reach=.4, x=.1, y=.1, b=1.8, r=1),
         k(.7, 'bob_m', reach=1, x=.4, y=.5, b=.4, mark='ha!'), k(.88, eye='^')],
        [], g='test', act=('compare', 'chests'), pick='hungriest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))])
    o.r('time_the_slow_sink_back', 'Counting seconds on the toes as the ballooned puffer slowly shrinks back, lifting a foot for every ten', 24, 'none',
        [k(.05, 'puff_l', x=.8, y=.9, b=.5, eye='o', mark='ten'), k(.2, 'puff_l', x=.9, y=1.0, b=.6, l=1, mark='twenty'), k(.35, 'puff_l', x=1.0, y=1.0, b=.6, r=1, mark='thirty'), k(.5, 'puff_l', x=1.0, y=1.1, b=.7, l=1, mark='forty'),
         k(.66, 'puff_l', x=1.1, y=1.1, b=.7, r=1, eye='-', mark='...'), k(.86, eye='^', mark='done')],
        [], g='test', act=('count', 'seconds'), prefer=['curious', 'tired'], when=['puff>.3'])
    o.r('peer_at_the_two_eyes_that_look_two_ways', 'Peering at the puffer\'s two eyes which swivel apart and look in two directions at once', 20, 'none',
        [k(.06, x=.5, y=.7, b=.4), k(.18, 'bob_r', x=1.5, y=1.4, b=.8, eye='o'), k(.34, 'bob_r', x=1.7, y=1.5, b=.9, eye='O', mark='hm'), k(.5, 'bob_r', x=1.4, y=1.2, b=.7, l=1, eye='@', mark='ow'), k(.68, x=.4, y=.4, b=.2, w=.5, eye='>'),
         k(.86, eye='-')],
        [], g='test', act=('peer', 'eyes'), pick='shyest', prefer=['curious'], obj=[(.2, dict(lure=1)), (.5, dict(lure=1))])
    o.r('tap_the_sign_to_see_who_looks', 'Tapping the sign letters with a wingtip, one letter at a time, to see whether the puffer looks up to read them', 20, 'wing',
        [k(.06, 'top_l', reach=.5, x=.2, y=-.1, b=.1), k(.2, 'sign', reach=1, x=.4, y=-.5, b=-.2, mark='S'), k(.34, 'sign', reach=1, x=.5, y=-.5, b=-.3, l=1, mark='E'), k(.48, 'sign', reach=1, x=.6, y=-.6, b=-.3, mark='A'),
         k(.64, 'top_l', reach=.6, x=.3, y=-.1, eye='o'), k(.82, eye='-')],
        [], g='test', act=('test', 'letters'), prefer=['curious', 'young'])
    # ---------------- rest
    o.r('sleep_off_the_fright_on_the_ledge', 'Sleeping off a fright on the left ledge, wing over his bill and one eye cracked at the puffer', 26, 'none',
        [k(.08, 'ledge_l', x=.2, y=.7, b=.9, eye='-', perch=1), k(.28, 'ledge_l', x=-.6, y=1.5, b=1.8, eye='-', perch=1), k(.52, 'ledge_l', x=-.9, y=2.0, b=2.3, eye='-', mark='zzz', w=.3, perch=1), k(.76, 'ledge_l', x=-.2, y=.8, b=.8, eye='o', perch=1),
         k(.9, eye='^')],
        [(.52, 'rest')], g='rest', act=('nap', 'ledge'), when=['tired'])
    o.r('sit_at_the_lip_watching_it_hover', 'Sitting at the front lip with his feet folded, watching the puffer hover in one spot as if it has forgotten how to leave', 24, 'none',
        [k(.08, 'lip', x=.3, y=.4, b=.8, perch=1), k(.3, 'lip', x=-.1, y=.8, b=1.5, eye='-', perch=1), k(.54, 'lip', x=-.3, y=1.0, b=1.9, eye='o', mark='...', perch=1), k(.78, 'lip', x=.4, y=.4, b=.6, l=1, perch=1, eye='^')],
        [(.54, 'rest')], g='rest', act=('sit', 'lip'), prefer=['tired', 'lonely'])
    o.r('wait_for_the_puff_to_go_down', 'Waiting dead still at the wall for the ballooned puffer to let its breath out and trust him again', 26, 'none',
        [k(.08, 'bob_m', x=.8, y=1.2, b=.7, eye='o'), k(.3, 'bob_m', x=.9, y=1.4, b=.9, eye='o'), k(.52, 'bob_m', x=.9, y=1.4, b=.9, l=1), k(.7, 'bob_m', x=1.0, y=1.5, b=1.0, eye='O', mark='...'), k(.88, 'bob_m', x=.4, y=.6, b=.4, eye='^')],
        [(.7, 'soothe')], g='rest', act=('wait', 'puff'), pick='shyest', when=['puff>.3'], obj=[(.5, dict(lure=1)), (.82, dict(lure=1))])
    o.r('lean_on_the_right_pier_with_a_sigh', 'Leaning on the right pier with a long sigh, bill resting on his chest, watching nothing in particular puff', 20, 'none',
        [k(.07, 'pier_r', x=-.4, y=.3, b=.5), k(.24, 'pier_r', x=-.8, y=.6, b=.9, eye='-'), k(.46, 'pier_r', x=-1.0, y=.8, b=1.2, eye='-', mark='sigh'), k(.66, 'pier_r', x=-.7, y=.6, b=.8, l=1), k(.84, x=.4, y=.2, b=.2, eye='O')],
        [], g='rest', act=('lean', 'pier'), prefer=['tired', 'sad'])
    o.r('sulk_when_it_hides_all_day', 'Sulking with his back to the tank because the puffer has hidden in the corner and refuses to be admired', 22, 'none',
        [k(.08, x=-.8, y=.5, b=.7), k(.26, 'base_m', x=-1.5, y=1.1, b=1.3, eye='-'), k(.5, 'base_m', x=-1.9, y=1.5, b=1.9, eye='-', mark='fine'), k(.7, 'base_m', x=-1.6, y=1.2, b=1.6, r=1), k(.86, x=-.5, y=.3, eye='-')],
        [], g='rest', act=('sulk', 'corner'), when=['sad'])
    # ---------------- weather
    o.r('fluff_up_against_the_cold', 'Fluffing every feather out against the cold in a round puff, bill buried in the ruff, a duck copying a puffer', 20, 'none',
        [k(.07, 'ledge_r', x=.3, y=.4, b=.6, perch=1), k(.2, 'ledge_r', x=.1, y=.1, b=1.4, w=.4, eye='-', perch=1), k(.4, 'ledge_r', x=-.2, y=0, b=2.0, w=.8, eye='-', mark='fluff', perch=1), k(.6, 'ledge_r', x=-.3, y=-.1, b=2.2, w=1, eye='-', perch=1),
         k(.82, 'ledge_r', x=.2, y=.2, b=.5, perch=1, eye='^')],
        [], g='weather', act=('fluff', 'feathers'), when=['cold'], prefer=['tired'])
    o.r('prod_the_ice_skin_at_the_top', 'Prodding the thin skin of ice at the top of the tank with a reed held out over the coping until it cracks', 24, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.2, y=-.2), k(.2, 'coping', reach=1, x=.5, y=-.3, b=-.1, mark='tk'), k(.34, 'top_m', reach=1, x=.6, y=-.3, b=0, l=1, mark='TK'), k(.5, 'top_m', reach=1, x=.7, y=-.2, b=.1, r=1, mark='CRK'),
         k(.68, 'top_l', reach=.7, x=.3, y=-.1, b=-.1), k(.86, eye='^')],
        [(.5, 'crack')], g='weather', act=('prod', 'ice'), when=['pond_ice>.3'])
    o.r('sweep_the_frost_flower_off_the_wall', 'Sweeping the frost flowers off the wall in wide wing arcs so the puffer is not looking out at white', 20, 'wing',
        [k(.08, 'puff_l', reach=.5, x=.3, y=.7, b=.3), k(.22, 'bob_l', reach=1, x=.6, y=.8, b=.6, mark='shff'), k(.38, 'bob_m', reach=1, x=.8, y=.8, b=.7, l=1, mark='shff'), k(.54, 'bob_r', reach=1, x=1.0, y=.8, b=.8, r=1, mark='shff'),
         k(.7, 'puff_r', reach=.7, x=.7, y=.6, b=.5), k(.88, eye='-')],
        [(.38, 'thaw')], g='weather', act=('sweep', 'frost'), when=['pond_ice>.3'])
    o.r('shelter_at_the_lip_from_the_rain', 'Sheltering low at the front lip with a wing over his head while the rain taps the tank and the puffer ignores it', 30, 'none',
        [k(.08, 'lip', x=-.4, y=.8, b=1.0, perch=1), k(.26, 'lip', x=-.9, y=1.6, b=1.7, w=.5, eye='-', perch=1), k(.5, 'lip', x=-1.1, y=1.9, b=2.1, w=.8, eye='-', mark='tap tap', perch=1), k(.74, 'lip', x=-1.0, y=1.8, b=1.9, w=.8, r=1, perch=1),
         k(.9, 'lip', x=.1, y=.3, b=.4, perch=1, eye='^')],
        [], g='weather', act=('shelter', 'lip'), when=['wet'])
    o.r('warm_his_back_to_the_noon_sun', 'Turning his back to the noon sun at the right pier and letting it soak into his feathers', 20, 'none',
        [k(.09, 'pier_r', x=-.5, y=.1, b=.8), k(.3, 'pier_r', x=-.9, y=.4, b=1.3, w=.5, eye='-'), k(.5, 'pier_r', x=-1, y=.5, b=1.5, w=1, eye='-', mark='ahh'), k(.7, 'pier_r', x=-.6, y=.3, b=.9, w=.5, l=1), k(.88, eye='^')],
        [], g='weather', act=('warm', 'back'), when=['sun'], prefer=['tired'])
    o.r('balance_on_the_ledge_in_the_gust', 'Balancing on the ledge in the gust, wings out like a tightrope walker, rocking with every puff', 20, 'none',
        [k(.06, 'ledge_r', x=.4, y=.2, b=.5, perch=1), k(.2, 'ledge_r', x=.7, y=0, b=.9, w=.6, l=1, perch=1), k(.36, 'ledge_r', x=.3, y=.2, b=.4, w=.9, r=1, perch=1, mark='whoo'), k(.52, 'ledge_r', x=.8, y=-.1, b=1.0, w=.7, l=1, perch=1),
         k(.68, 'ledge_r', x=.4, y=.2, b=.5, w=.5, r=1, perch=1), k(.86, 'ledge_r', x=.2, y=.1, b=.3, perch=1, eye='^')],
        [], g='weather', act=('balance', 'ledge'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_round_little_boss', 'Bowing to the round little boss with a solemn bill dip, the puffer swelling slightly in acknowledgement', 16, 'none',
        [k(.08, 'bob_m', x=.5, y=.9, b=.7), k(.28, 'bob_m', x=1.0, y=2.0, b=1.8, eye='-'), k(.5, 'bob_m', x=1.1, y=2.2, b=1.9, eye='-', mark='sir'), k(.68, 'bob_m', x=.6, y=.7, b=.5), k(.86, x=.1, y=-.4, w=.6, eye='^')],
        [], g='show', act=('bow', 'puffer'), pick='hungriest', prefer=['happy'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))], say=["It swelled a bit. We understand each other.", "Bowed to a pufferfish. The day has peaked."])
    o.r('present_the_puffer_with_a_flourish', 'Presenting the puffer with a flourish, one wing sweeping out like a magician revealing a balloon', 20, 'wing',
        [k(.07, 'bob_l', reach=.4, x=.1, y=.1), k(.22, 'bob_l', reach=.9, x=.3, y=-.4, b=-.3), k(.4, 'bob_m', reach=1, x=.4, y=-.7, b=-.6, mark='behold'), k(.56, 'bob_r', reach=1, x=.3, y=-.5, b=-.4, l=1), k(.74, 'bob_r', reach=.6, x=.5, y=0),
         k(.9, eye='^')],
        [], g='show', act=('present', 'puffer'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_about_who_is_rounder', 'Arguing with the puffer about which of them is rounder, jabbing a wing at its belly and then at his own', 20, 'wing',
        [k(.07, 'bob_m', reach=.5, x=.6, y=.3, b=.4), k(.22, 'bob_m', reach=1, x=1.1, y=.2, b=.3, mark='ROUNDER'), k(.38, 'bob_m', reach=.5, x=.4, y=.4, b=1.4, l=1, mark='ME'), k(.54, 'bob_m', reach=1, x=1.2, y=.1, b=.2, r=1, mark='YOU'),
         k(.72, 'bob_m', reach=.5, x=.4, y=.5, b=1.2, mark='ME'), k(.88, eye='-')],
        [], g='show', act=('argue', 'belly'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It won. Rounder by an arc.", "I have been out-rounded by a fish the size of a pear."])
    o.r('pose_with_a_puffed_chest_on_the_ledge', 'Striking a heroic pose on the right ledge with a chest as big as it will go, while the real puffer does it better', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.1, b=.3, w=.3, perch=1), k(.24, 'ledge_r', x=.6, y=-.5, b=1.4, w=.7, perch=1), k(.5, 'ledge_r', x=.8, y=-.8, b=2.0, w=1, perch=1, eye='^', mark='big'), k(.74, 'ledge_r', x=.3, y=0, b=.4, w=.3, perch=1)],
        [], g='show', act=('pose', 'ledge'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('shout_the_alarm_at_a_phantom', 'Shouting a mock alarm at nothing and watching the puffer balloon before he has finished the word', 16, 'none',
        [k(.07, 'bob_l', x=.4, y=.2, b=.3), k(.2, 'bob_l', x=-.5, y=-.6, b=-.6, w=.9, eye='O', mark='LOOK OUT'), k(.32, 'bob_l', x=1.3, y=.7, b=.6, eye='o', mark='...'), k(.5, 'bob_l', x=1.1, y=.3, b=.3, l=1, r=1, mark='sorry'), k(.7, eye='-')],
        [(.2, 'startle')], g='show', act=('shout', 'alarm'), pick='shyest', prefer=['young', 'curious'], far=True, obj=[(.2, dict(lure=1)), (.5, dict(lure=1))],
        say=["There was nothing there. It believed me anyway.", "False alarm, true balloon."])
    # ---------------- mishap
    o.r('slip_on_the_damp_ledge_edge', 'Slipping on the damp left ledge and flailing both wings against the wall as the puffer balloons in sympathy', 16, 'none',
        [k(.07, 'ledge_l', x=.6, y=.7, b=.7, perch=1), k(.2, 'ledge_l', x=1.2, y=-.4, b=-.9, l=1, r=1, w=1, mark='whoa!', perch=1), k(.34, 'bob_l', x=1.6, y=.9, b=1.7, w=.8, eye='O', mark='SLAP'), k(.52, 'ledge_l', x=.7, y=.7, b=.9, perch=1, eye='>'),
         k(.7, x=.2, y=.2, b=.2, eye='-')],
        [], g='mishap', act=('slip', 'ledge'), when=['wet'], prefer=['young'])
    o.r('wedged_in_the_pier_rungs_after_the_glimmer', 'Wedging his bill between two rungs of the left pier after a glimmer of spine, then yanking free with a twang', 22, 'none',
        [k(.06, x=.8, y=.5, b=.5), k(.18, 'pier_l', x=1.8, y=.1, b=.9, eye='O'), k(.36, 'pier_l', x=2.0, y=.2, b=1.2, l=1, eye='@', mark='mm'), k(.52, 'pier_l', x=1.9, y=.3, b=1.1, r=1, mark='mmf'), k(.66, 'pier_l', x=1.3, y=-.3, b=-.8, w=1, mark='TWANG'),
         k(.84, x=1, y=.9, b=.6, eye='-')],
        [], g='mishap', act=('stuck', 'rungs'), prefer=['young', 'grumpy'])
    o.r('bump_the_wall_chasing_a_spine_glint', 'Following a spine glint along the wall with his eyes only and bumping the wall with a clunk', 18, 'none',
        [k(.07, 'puff_l', x=.8, y=.5, b=.3), k(.22, 'bob_l', x=.9, y=.6, b=.4, l=1), k(.36, 'bob_m', x=1, y=.5, b=.3, r=1), k(.48, 'bob_r', x=2.1, y=.1, b=1.6, eye='@', mark='CLUNK'), k(.64, 'bob_r', x=-1.3, y=.4, b=.1, w=.9, eye='x'), k(.84, y=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'wall'), prefer=['curious'])
    o.r('leap_back_from_the_sudden_balloon', 'Leaping back with a yelp when the puffer swells to ten times its size an inch from his bill', 16, 'none',
        [k(.06, 'bob_m', x=1.1, y=1.5, b=.8), k(.18, 'bob_m', x=1.3, y=1.7, b=1, eye='o', mark='...'), k(.28, x=-1.4, y=-.9, b=-1.4, l=1, r=1, w=1, eye='O', mark='YELP'), k(.44, x=-.8, y=.2, b=-.1, w=.7, eye='>'), k(.62, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'balloon'), pick='hungriest', prefer=['young', 'curious'], obj=[(.18, dict(lure=1)), (.45, dict(lure=1))],
        say=["It was small, then it was a planet.", "Swore I saw a face on it. A cross one."])
    o.r('stamp_after_the_crumb_cloud', 'Stamping at the crumb cloud blown over the lip after a clumsy toss, as if crumbs could be told off', 16, 'none',
        [k(.06, 'lip', x=.7, y=.8, b=.5, perch=1), k(.18, 'lip', x=.5, y=-.1, b=-1.2, l=1, mark='STMP', perch=1), k(.3, 'lip', x=.6, y=.6, b=.6, perch=1), k(.42, 'lip', x=.5, y=-.1, b=-1.3, r=1, mark='STMP', perch=1),
         k(.56, 'lip', x=.6, y=.6, b=.6, perch=1), k(.7, 'lip', x=.5, y=-.2, b=-1.5, l=1, r=1, mark='STMP!', perch=1), k(.88, eye='-')],
        [], g='mishap', act=('stamp', 'crumbs'), when=['crumbs>.3'], prefer=['grumpy'])
    # ---------------- duets
    o.r('pass_a_hard_crumb_down_the_wall', 'Pressing a hard crumb to the wall for the puffer while a friend does the same two spots along, so it hops from beak to beak', 26, 'none',
        [k(.05, 'puff_l', x=.7, y=1.0, b=.5), k(.2, 'puff_l', x=1.6, y=1.6, b=.8, eye='o', mark='tp'), k(.36, 'puff_l', x=.8, y=.7, b=.4, w=.4), k(.52, 'bob_m', x=1.7, y=1.6, b=.9, mark='tp'), k(.7, 'bob_m', x=.9, y=.8, b=.5, eye='O'),
         k(.86, eye='^')],
        [(.52, 'snap')], g='use', act=('catch', 'crumb'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.25, dict(lure=1)), (.56, dict(lure=1))],
        duo=[k(.12, 'puff_r', x=.6, y=.9, b=.5), k(.3, 'puff_r', x=1.5, y=1.5, b=.8, mark='tp'), k(.46, 'puff_r', x=.8, y=.7, b=.4), k(.62, 'bob_r', x=1.6, y=1.5, b=.9, l=1, mark='tp'), k(.8, eye='^')],
        say=["Beak to beak, crumb to crumb. A puffer relay.", "Two ducks feeding one balloon. The usual civic duty."])
    o.r('calm_it_from_both_sides_of_the_wall', 'Laying a calm wing on the wall to one side of the ballooned puffer while a friend does the same on the other, until it sinks', 28, 'wing',
        [k(.06, 'bob_l', reach=.4, x=.3, y=.6, b=.3), k(.2, 'bob_l', reach=1, x=.5, y=.8, b=.7, eye='-'), k(.42, 'bob_l', reach=1, x=.5, y=1.0, b=1.0, eye='-', mark='shhh'), k(.64, 'bob_l', reach=1, x=.5, y=.9, b=.9, l=1),
         k(.82, 'bob_l', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(.42, 'soothe')], g='rest', act=('guard', 'balloon'), pick='shyest', when=['puff>.3'], obj=[(.2, dict(lure=1)), (.6, dict(lure=1))],
        duo=[k(.1, 'bob_r', x=.4, y=.6, b=.3), k(.26, 'bob_r', x=.6, y=.9, b=.8, eye='-'), k(.46, 'bob_r', x=.6, y=1.0, b=1.0, eye='-', mark='shhh'), k(.68, 'bob_r', x=.6, y=.9, b=.9, r=1), k(.84, eye='^')],
        say=["Two quiet wings and one fat balloon. It deflated out of politeness.", "A puffer talked down. Wings only, no words."])
    o.r('guess_the_number_of_spines_with_a_friend', 'Guessing the number of spines with a friend at the other end of the wall, each of them sure and each wildly off', 24, 'none',
        [k(.05, 'bob_l', x=1.2, y=.7, b=.8, mark='forty'), k(.19, 'bob_l', x=1.3, y=.9, b=1.0, mark='sixty'), k(.33, 'bob_m', x=1.4, y=.8, b=1.1, l=1, mark='a hundred?'), k(.5, 'bob_m', x=1.3, y=.3, b=.6, w=.6, mark='nope'), k(.68, 'bob_m', x=.9, y=.5, b=.5, eye='-', mark='fine'), k(.86, eye='^')],
        [], g='test', act=('compare', 'spines'), pick='shyest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.1, 'bob_r', x=.8, y=1.0, b=.5, mark='thirty'), k(.28, 'bob_r', x=.9, y=1.1, b=.6, mark='eighty'), k(.44, 'bob_m', x=1.0, y=1.0, b=.6, r=1, mark='ninety'), k(.62, 'bob_r', x=.7, y=.7, b=.4, eye='-'), k(.8, eye='^')],
        say=["Ninety and a hundred. The fish counted none. Fair.", "Nobody was right. The puffer kept the answer."])
    return done(o)


def swordfish():
    # Swordfish: fast, top-dwelling surface slasher with a long sword, active at morning and evening, very jumpy. Lives in the sea tank; Cheese stays at the edge.
    # Own state: wake (the foam streak of its pass along the top: drawn, fades fast), slash (how wound up it is for a run: builds at dawn and dusk, spent by a strike).
    o = Obj('swordfish', 'keeping', on='infinity_pool',
            fields=dict(wake=(0, 0, 1), slash=(0, 0, 1)),
            physics=[('slash', 'rate', .003, 'dawn'), ('slash', 'rate', .003, 'dusk'), ('slash', 'rate', -.002, 'day'), ('wake', 'rate', -.006, 'always')],
            effects=dict(scrub=[('keeping.algae', 'mul', .5)], rake=[('keeping.leaves', 'mul', .35)], polish=[('keeping.clarity', 'add', .15)], foam=[('keeping.flakes', 'mul', .3)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], call=[('keeping.bell', 'add', .5)],
                         scatter=[('keeping.flakes', 'add', .4), ('wake', 'set', 1)], strike=[('wake', 'set', 1), ('subject.hunger', 'add', -.2), ('slash', 'mul', .5)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], tease=[('slash', 'add', .25), ('subject.trust', 'add', .1)],
                         soothe=[('slash', 'mul', .4), ('subject.mood', 'add', .15)], crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('wake', .3, '=====', 'skin_l', 'water'), ('pond_flakes', .3, ".':.'", 'skin_r', 'dust'), ('pond_leaves', .3, ';"~;"', 'top_m', 'leaf'), ('pond_ice', .3, '*-*-*', 'top_l', 'frost'),
                   ('pond_algae', .3, '"v"v"', 'flank_l', 'plant')],
            anchors=dict(low_l=Q(36, 43), low_r=Q(80, 43), flank_l=Q(24, 46), flank_r=Q(94, 46), top_l=Q(30, 37), top_m=Q(58, 37), top_r=Q(88, 37), skin_l=Q(34, 34), skin_r=Q(76, 34),
                         sign=Q(24, 33), coping=Q(40, 28), ledge_l=Q(30, 49, 'surface'), ledge_r=Q(92, 49, 'surface'), pier_l=Q(10, 41), pier_r=Q(110, 41), lip=Q(60, 52, 'surface')))
    # ---------------- care
    o.r('wipe_the_high_wall_clear_of_green', 'Wiping the green off the upper wall with long upward swipes of a wing so the top run is clear to watch', 22, 'wing',
        [k(.05, 'flank_l', reach=.4, x=.2, y=.6, b=.3), k(.15, 'low_l', reach=1, x=.4, y=.5, b=.4, mark='whp'), k(.27, 'top_l', reach=1, x=.5, y=.2, b=.2, l=1, mark='whp'), k(.4, 'top_m', reach=1, x=.6, y=0, b=0, mark='whp'),
         k(.54, 'top_r', reach=1, x=.7, y=.1, b=.1, r=1, mark='whp'), k(.7, 'low_r', reach=.8, x=.5, y=.4, b=.3), k(.9, eye='^')],
        [(.4, 'scrub')], g='care', act=('wipe', 'algae'), when=['pond_algae>.4'],
        say=["Green gone. It sped past to inspect the work.", "Scrubbed the top run. The sword saw itself and showed off."])
    o.r('rake_the_leaf_mat_off_the_top_run', 'Raking the matted leaves off the top run with a reed held out over the coping so the fast one does not slash at them', 24, 'reed',
        [k(.06, 'skin_r', reach=.4, x=.2, y=-.2), k(.2, 'coping', reach=1, x=.5, y=-.4, b=-.3, mark='rk'), k(.34, 'skin_r', reach=1, x=.6, y=-.3, b=-.1, l=1, mark='rk'), k(.48, 'skin_l', reach=1, x=.8, y=-.2, b=0, r=1, mark='rk'),
         k(.64, 'skin_l', reach=.7, x=.3, y=-.1, b=-.2), k(.84, eye='-')],
        [(.48, 'rake')], g='care', act=('rake', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'])
    o.r('polish_a_clean_pane_for_the_sword', 'Polishing a clean pane at the top of the wall in tight circles so the sword and the long eye can be seen properly', 22, 'wing',
        [k(.07, 'top_l', reach=.5, x=.3, y=.2, b=.2), k(.19, 'top_l', reach=1, x=.5, y=.3, b=.4, mark='sqk'), k(.32, 'top_m', reach=1, x=.6, y=.2, b=.3, l=1, mark='sqk'), k(.46, 'top_m', reach=1, x=.5, y=.3, b=.4, r=1, mark='sqk'),
         k(.6, 'top_r', reach=1, x=.7, y=.4, b=.4, mark='sqk'), k(.8, eye='o', mark='clear')],
        [(.46, 'polish')], g='care', act=('polish', 'pane'), when=['pond_clarity<.6'])
    o.r('peer_down_the_length_of_the_sword', 'Peering all the way down the length of the sword for any chip or crack in the tip, tracking its slow turn at the wall', 22, 'none',
        [k(.05, x=.4, y=.4, b=.3), k(.16, 'low_l', x=1.6, y=1.4, b=.9, eye='o'), k(.28, 'top_l', x=1.8, y=.7, b=.8, eye='O', mark='hm'), k(.42, 'top_m', x=1.9, y=.6, b=.7, r=1), k(.56, 'top_r', x=2.0, y=.5, b=.7, l=1, mark='ok'),
         k(.74, x=.5, y=.5, b=.3, w=.4, eye='^')],
        [(.42, 'tend')], g='care', act=('peer', 'sword'), pick='shyest', when=['fish_health<.8'], obj=[(.16, dict(lure=1)), (.42, dict(lure=1)), (.58, dict(lure=1))],
        say=["Tip intact. A dangerous thing, to have a point.", "No chips. It has been cutting nothing with real discipline."])
    o.r('brush_the_foam_skin_off_the_water_line', 'Brushing the thick foam skin off the water line with a wing so the top run is not a swamp of bubbles', 18, 'wing',
        [k(.06, 'skin_r', reach=.4, x=.1, y=0), k(.19, 'skin_r', reach=1, x=.4, y=-.2, b=.2, mark='shh'), k(.33, 'skin_l', reach=1, x=.6, y=-.1, b=.3, l=1, mark='shh'), k(.5, 'skin_l', reach=1, x=.7, y=-.1, b=.2, r=1),
         k(.68, 'skin_r', reach=.6, x=.3, y=0, b=.1), k(.86, eye='-')],
        [(.33, 'foam')], g='care', act=('sweep', 'foam'), when=['pond_flakes>.3'])
    # ---------------- use
    o.r('rap_the_sign_with_a_wing_edge', 'Rapping the sign with the edge of a wing three times, the loud bell the sword has learned to answer', 16, 'wing',
        [k(.06, 'top_l', reach=.4, x=.2, y=-.1), k(.17, 'sign', reach=1, x=.5, y=-.6, b=-.3, mark='tok'), k(.28, 'sign', reach=.5, x=.2, y=-.2, b=0), k(.4, 'sign', reach=1, x=.6, y=-.7, b=-.3, l=1, mark='tok'),
         k(.52, 'sign', reach=.5, x=.2, y=-.2, b=0), k(.64, 'sign', reach=1, x=.7, y=-.8, b=-.4, r=1, mark='TOK'), k(.84, eye='^')],
        [(.64, 'call')], g='use', act=('knock', 'sign'), when=['pond_bell<.4'], prefer=['dawn', 'dusk'])
    o.r('flip_a_wingful_of_flakes_across_the_top', 'Flipping a wingful of flakes across the top of the tank so they skitter on the water and the sword comes slashing', 18, 'wing',
        [k(.08, 'skin_l', reach=.3, x=.1, y=0), k(.2, 'skin_l', reach=.9, x=.3, y=-.3, b=.5), k(.34, 'skin_r', reach=1, x=.5, y=-.9, b=-.8, mark='fwip'), k(.5, x=-.3, y=0, b=-.2, eye='o'), k(.7, eye='^')],
        [(.34, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.3'], prefer=['dawn', 'dusk'], say=["Flakes across the top. Streak, slash, gone.", "It hit the water so hard I got wet from the wall."])
    o.r('dangle_a_flake_on_a_reed_for_the_slash', 'Dangling a flake on the end of a reed a hand above the water line, snatching it back as the sword slashes up at it', 24, 'reed',
        [k(.05, 'coping', reach=.4, x=.2, y=-.1), k(.16, 'coping', reach=1, x=.5, y=-.4, b=-.2, mark='...'), k(.3, 'skin_l', reach=1, x=.7, y=-.5, b=-.3, l=1), k(.44, 'skin_l', reach=1, x=.3, y=-.9, b=-.9, w=.3, eye='O', mark='SHNK'),
         k(.6, 'skin_r', reach=.8, x=-.3, y=.2, b=.2), k(.78, eye='>')],
        [(.44, 'strike')], g='use', act=('lift', 'flake'), pick='hungriest', when=['slash>.3'], obj=[(.16, dict(lure=1)), (.34, dict(lure=1)), (.5, dict(lure=1))],
        say=["Slashed it clean. I held on to the reed and a bit of pride.", "Missed the flake. Hit the dream."])
    o.r('trail_a_wingtip_fast_along_the_wall', 'Trailing a wingtip fast along the upper wall in quick jerks to tease the sword into one long hot run', 20, 'wing',
        [k(.05, 'top_l', reach=.5, x=.3, y=.2, b=.2), k(.14, 'top_l', reach=1, x=.5, y=.3, b=.4, l=1), k(.24, 'top_m', reach=1, x=.9, y=.3, b=.3), k(.34, 'top_m', reach=1, x=1.2, y=.3, b=.3, r=1), k(.46, 'top_r', reach=1, x=1.5, y=.3, b=.3, l=1),
         k(.6, 'top_r', reach=.8, x=1.2, y=.2, b=.2), k(.8, eye='@')],
        [(.34, 'tease')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['slash<.7'], obj=[(.1, dict(lure=1)), (.25, dict(lure=1)), (.4, dict(lure=1)), (.58, dict(lure=1))],
        say=["Teased it into a streak. I could not tell which end was which.", "I move a wingtip, it moves the world."])
    o.r('settle_a_wing_on_the_wall_to_slow_it', 'Settling a still wing flat against the wall at mid height until the keyed-up fish slows to a hover and stops slashing', 26, 'wing',
        [k(.06, 'low_r', reach=.4, x=.3, y=.7, b=.4), k(.2, 'low_r', reach=1, x=.5, y=.9, b=.8, eye='-'), k(.42, 'low_r', reach=1, x=.5, y=1.1, b=1.1, eye='-', mark='easy'), k(.64, 'low_r', reach=1, x=.5, y=1.0, b=1.0, l=1),
         k(.82, 'low_r', reach=.5, x=.3, y=.5, b=.4, eye='^')],
        [(.42, 'soothe')], g='use', act=('press', 'wall'), pick='shyest', when=['slash>.4'], obj=[(.2, dict(lure=1)), (.62, dict(lure=1))],
        say=["It stopped. Hovered. Looked, for once, like a fish.", "Slow wing, slow sword. A deal was struck."])
    o.r('hold_a_flake_to_the_wall_for_the_bill', 'Holding a flake flat to the wall with the tip of his bill while the long sword turns and the small mouth takes it from the other side', 22, 'none',
        [k(.05, x=.4, y=.6, b=.4), k(.18, 'low_l', x=1.7, y=1.4, b=.8, eye='o', mark='...'), k(.32, 'low_l', x=1.9, y=1.5, b=1.0, eye='O', mark='SNP'), k(.46, 'low_l', x=1.8, y=1.4, b=.9, l=1), k(.64, x=.5, y=.7, b=.4, w=.4, eye='^'),
         k(.84, eye='-')],
        [(.32, 'feed')], g='use', act=('press', 'flake'), pick='shyest', when=['fish_hunger>.4'], obj=[(.18, dict(lure=1)), (.48, dict(lure=1)), (.66, dict(lure=0))])
    o.r('raise_a_reed_hoop_for_the_streak', 'Raising a reed bent in a hoop at the top of the tank with both ends held, so the swordfish threads it at speed', 24, 'reed',
        [k(.05, 'top_r', reach=.4, x=.2, y=.1), k(.18, 'skin_r', reach=1, x=.5, y=-.2, b=-.1), k(.32, 'skin_r', reach=1, x=.6, y=-.4, b=-.3, w=.2, mark='steady'), k(.46, 'skin_r', reach=1, x=.5, y=-.6, b=-.5, l=1, r=1, eye='O', mark='ZIP'),
         k(.62, 'top_r', reach=.8, x=.3, y=0, b=0, eye='o'), k(.82, eye='^')],
        [(.46, 'strike')], g='use', act=('lift', 'hoop'), pick='hungriest', prefer=['fish_trust>.4', 'happy'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.58, dict(lure=1))],
        say=["Through the hoop and out the other side. I did not see it.", "A hoop for a streak. We call it a ride."])
    # ---------------- play
    o.r('race_the_streak_and_lose_gloriously', 'Racing the streak along the wall at a flat run, wings back, and losing before he has taken three strides', 18, 'none',
        [k(.04, 'flank_l', x=.7, y=.2, b=.3), k(.12, 'low_l', x=1.5, y=.2, b=-1.0, l=1, w=.5), k(.22, 'top_m', x=1.9, y=.1, b=-.4, r=1, w=.9, mark='WHOO'), k(.32, 'top_r', x=2.0, y=.1, b=-1.1, l=1, w=1),
         k(.46, 'low_r', x=1.2, y=.5, b=.8, r=1, eye='@'), k(.64, 'flank_r', x=.4, y=.7, b=1.0, eye='x', mark='lost'), k(.84, eye='-')],
        [(.46, 'fun')], g='play', act=('race', 'streak'), pick='hungriest', prefer=['young', 'happy'], obj=[(.1, dict(lure=1)), (.26, dict(lure=1)), (.4, dict(lure=1)), (.55, dict(lure=1))],
        say=["Lost by nine wall lengths. It lapped me before I started.", "The only race with a finish line I never saw."])
    o.r('duck_when_the_sword_comes_at_the_wall', 'Ducking low with a whoop each time the sword jabs at the wall, springing straight up again after it passes', 18, 'none',
        [k(.05, 'low_l', x=.5, y=.5, b=.3), k(.15, 'low_l', x=-.5, y=1.4, b=1.9, w=.4, eye='>', mark='WHOA'), k(.26, 'low_l', x=.9, y=.1, b=-1.2, w=.7, l=1, r=1), k(.4, 'low_r', x=-.6, y=1.5, b=2.0, w=.4, eye='>', mark='WHOA'),
         k(.52, 'low_r', x=1, y=.1, b=-1.3, w=.8, l=1, r=1), k(.68, 'low_r', x=.4, y=.4, b=.4), k(.86, eye='@')],
        [], g='play', act=('hop', 'sword'), pick='hungriest', prefer=['young', 'curious'], obj=[(.1, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=1))])
    o.r('fence_the_swordfish_with_a_reed', 'Fencing with a reed against the wall while the sword jabs back from the other side, lunge for lunge', 22, 'reed',
        [k(.05, 'low_r', reach=.4, x=.4, y=.2, b=.2), k(.16, 'low_r', reach=1, x=1.1, y=.1, b=.5, l=1, mark='haa'), k(.26, 'low_r', reach=.5, x=.2, y=.3, b=-.2), k(.38, 'top_r', reach=1, x=1.3, y=0, b=.6, r=1, mark='HAA'),
         k(.5, 'top_r', reach=.5, x=.2, y=.2, b=-.3), k(.64, 'low_r', reach=1, x=1.4, y=.1, b=.7, l=1, mark='TOUCHE'), k(.84, eye='@')],
        [], g='play', act=('prod', 'reed'), pick='hungriest', prefer=['happy', 'young'], obj=[(.16, dict(lure=1)), (.4, dict(lure=1)), (.64, dict(lure=1))],
        say=["Parried twice. Hit once, by accident. Honour satisfied.", "Reed versus sword is not a fair fight, but it is a loud one."])
    o.r('follow_the_wake_along_the_top', 'Following the white wake along the top with a wingtip, always three strides back from the fish that made it', 20, 'wing',
        [k(.05, 'skin_l', reach=.5, x=.4, y=-.1, b=.1), k(.17, 'skin_l', reach=1, x=.8, y=-.2, b=.2, l=1, mark='fwp'), k(.3, 'skin_r', reach=1, x=1.2, y=-.2, b=.2, r=1), k(.44, 'top_r', reach=1, x=1.5, y=0, b=.3, l=1, mark='fwp'),
         k(.58, 'top_r', reach=.7, x=.8, y=.2, b=.4), k(.76, eye='@')],
        [], g='play', act=('chase', 'wake'), when=['wake>.3'], prefer=['young', 'happy'])
    o.r('fence_steps_on_the_ledge', 'Fencing with a bill-point along the left ledge in short darting steps, lunge and recover, as the real sword flashes past', 22, 'none',
        [k(.05, 'ledge_l', x=.4, y=.2, b=.4, perch=1), k(.14, 'ledge_l', x=1.1, y=-.1, b=.1, l=1, w=.5, perch=1, mark='haa'), k(.24, 'ledge_l', x=.3, y=.3, b=.6, perch=1), k(.34, 'ledge_l', x=1.3, y=-.2, b=0, r=1, w=.7, perch=1, mark='HAA'),
         k(.46, 'ledge_l', x=.2, y=.4, b=.7, perch=1), k(.6, 'ledge_l', x=1.5, y=-.3, b=-.2, l=1, w=1, perch=1, mark='TOUCHE'), k(.8, 'ledge_l', x=.3, y=.4, b=.4, perch=1, eye='^')],
        [(.34, 'fun')], g='play', act=('dance', 'ledge'), pick='hungriest', prefer=['happy', 'young'], obj=[(.25, dict(lure=1)), (.55, dict(lure=1))])
    o.r('count_the_slashes_against_the_wall', 'Counting each slash against the wall as a toe lift, unable to keep up past six', 18, 'none',
        [k(.05, 'low_l', x=.8, y=.6, b=.4, l=1, mark='1'), k(.15, 'low_r', x=.8, y=.6, b=.4, r=1, mark='2'), k(.26, 'low_l', x=.9, y=.6, b=.5, l=1, mark='3'), k(.37, 'low_r', x=.9, y=.6, b=.5, r=1, mark='4'),
         k(.5, 'low_l', x=1, y=.6, b=.6, l=1, r=1, mark='5-6-7'), k(.68, x=-.4, y=.1, b=-.2, w=.4, eye='>', mark='lost'), k(.86, eye='-')],
        [], g='play', act=('count', 'slashes'), pick='hungriest', prefer=['curious'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.46, dict(lure=1))])
    # ---------------- test
    o.r('measure_the_sword_against_a_reed', 'Holding a reed up beside the sword to measure how much of the fish is sword and how much is fish', 24, 'reed',
        [k(.05, 'low_l', reach=.4, x=.3, y=.4, b=.2), k(.18, 'low_l', reach=1, x=.6, y=.5, b=.4, mark='this'), k(.32, 'top_l', reach=1, x=.7, y=.2, b=.3, l=1, mark='much'), k(.46, 'top_m', reach=1, x=.9, y=.2, b=.3, mark='sword'),
         k(.62, 'low_l', reach=.7, x=.4, y=.6, b=.5, eye='o', mark='a third'), k(.8, eye='-')],
        [], g='test', act=('measure', 'sword'), pick='shyest', prefer=['curious'], obj=[(.25, dict(lure=1)), (.5, dict(lure=1))],
        say=["A third of it is sword. The rest is attitude.", "Longer than my leg. Longer than my patience."])
    o.r('count_the_passes_between_pier_posts', 'Counting how many times the swordfish crosses the tank between the two pier posts while he draws a breath', 22, 'none',
        [k(.05, 'pier_l', x=.5, y=.5, b=.3, mark='1'), k(.17, 'pier_r', x=.5, y=.5, b=.3, mark='2'), k(.29, 'pier_l', x=.6, y=.5, b=.4, l=1, mark='3'), k(.4, 'pier_r', x=.6, y=.5, b=.4, r=1, mark='4'),
         k(.52, 'pier_l', x=.7, y=.5, b=.5, l=1, mark='5'), k(.66, x=-.3, y=0, b=-.2, w=.5, eye='>', mark='enough'), k(.84, eye='-')],
        [], g='test', act=('count', 'passes'), prefer=['curious'], when=['slash>.3'])
    o.r('listen_for_the_whoosh_before_the_streak', 'Listening hard at the wall for the whoosh that comes before the streak, bill cocked at the sound', 20, 'none',
        [k(.06, x=-.4, y=.6, b=.5), k(.2, 'low_l', x=-1.2, y=1.7, b=1.4, eye='-'), k(.38, 'low_l', x=-1.5, y=2.1, b=1.9, eye='-', mark='...'), k(.56, 'low_l', x=-1.6, y=2.2, b=2.1, eye='o', mark='whsh'), k(.74, 'low_l', x=.4, y=.6, b=.4, eye='O'),
         k(.9, eye='^')],
        [], g='test', act=('listen', 'whoosh'), prefer=['curious', 'dawn'])
    o.r('compare_its_speed_with_his_best_dash', 'Setting his own best dash from pier to pier against a streak of the swordfish, comparing the two with a wing in the air', 26, 'wing',
        [k(.05, 'pier_l', reach=.4, x=.3, y=.3, b=.3), k(.14, 'low_l', reach=.8, x=1.0, y=.2, b=-.7, l=1, mark='me'), k(.26, 'low_r', reach=.8, x=1.2, y=.2, b=-.5, r=1), k(.4, 'pier_r', reach=.6, x=.4, y=.4, b=.5, eye='O', mark='done'),
         k(.5, 'pier_r', reach=1, x=.7, y=.5, b=.5, mark='it?'), k(.66, 'pier_l', reach=1, x=.6, y=.4, b=.4, l=1, mark='twice'), k(.86, eye='-')],
        [], g='test', act=('compare', 'speed'), pick='hungriest', prefer=['curious', 'young'], obj=[(.3, dict(lure=1)), (.58, dict(lure=1))])
    o.r('squint_at_the_big_round_eye', 'Squinting at the big round eye that tracks every move he makes, bill an inch from the wall at the top', 20, 'none',
        [k(.05, x=.5, y=.3, b=.3), k(.17, 'top_m', x=1.4, y=.4, b=.7, eye='o'), k(.3, 'top_m', x=1.6, y=.5, b=.9, eye='O', mark='hm'), k(.44, 'top_r', x=1.5, y=.4, b=.8, l=1, eye='@'), k(.6, 'top_r', x=.6, y=.2, b=.3, w=.4, eye='>', mark='it blinked'),
         k(.8, eye='-')],
        [], g='test', act=('peer', 'eye'), pick='shyest', prefer=['curious'], obj=[(.2, dict(lure=1)), (.46, dict(lure=1))])
    o.r('sniff_the_spray_from_the_top', 'Sniffing the sea spray flung over the coping by a hard turn, then sneezing salt', 18, 'none',
        [k(.06, 'skin_l', x=.3, y=-.5, b=.3), k(.2, 'skin_l', x=.7, y=-.9, b=.4, mark='snf'), k(.36, 'skin_l', x=.8, y=-1.0, b=.5, eye='-', mark='snf'), k(.52, x=-1.2, y=-.4, b=-.3, w=.8, eye='>', mark='ACHOO'), k(.72, x=.1, y=.2, eye='-')],
        [], g='test', act=('sniff', 'spray'), prefer=['curious', 'young'])
    # ---------------- rest
    o.r('doze_after_the_morning_run', 'Dozing on the right ledge after the morning run, bill on his chest, one foot tucked', 26, 'none',
        [k(.08, 'ledge_r', x=.2, y=.8, b=.9, eye='-', perch=1), k(.28, 'ledge_r', x=-.4, y=1.5, b=1.7, eye='-', l=1, perch=1), k(.52, 'ledge_r', x=-.7, y=1.9, b=2.1, eye='-', mark='zzz', l=1, perch=1), k(.76, 'ledge_r', x=-.2, y=.7, b=.7, eye='o', perch=1),
         k(.9, eye='^')],
        [(.52, 'rest')], g='rest', act=('nap', 'ledge'), when=['tired'], prefer=['dawn'])
    o.r('sit_on_the_lip_between_runs', 'Sitting at the front lip with his feet tucked in the lull between runs, watching the tank for the next streak', 24, 'none',
        [k(.08, 'lip', x=.3, y=.4, b=.8, perch=1), k(.3, 'lip', x=0, y=.8, b=1.5, eye='-', perch=1), k(.54, 'lip', x=-.2, y=1.0, b=1.9, eye='o', mark='...', perch=1), k(.78, 'lip', x=.5, y=.4, b=.6, perch=1, eye='^')],
        [(.54, 'rest')], g='rest', act=('sit', 'lip'), when=['day'], prefer=['tired', 'lonely'])
    o.r('wait_for_the_first_streak_of_the_day', 'Waiting stock-still at the wall for the first streak of the day to cut the water, wings pinned', 24, 'none',
        [k(.08, 'top_m', x=.9, y=.5, b=.7, eye='o'), k(.28, 'top_m', x=1.0, y=.6, b=.9, eye='o'), k(.5, 'top_m', x=1.0, y=.6, b=.9, l=1), k(.7, 'top_m', x=1.1, y=.7, b=1.0, eye='O', mark='...'), k(.88, 'top_m', x=.4, y=.3, b=.4, eye='^')],
        [], g='rest', act=('wait', 'streak'), pick='shyest', prefer=['lonely', 'curious'], when=['slash>.3'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('lean_on_the_left_post_and_watch_it_fly', 'Leaning on the left pier post with his arms folded, watching the swordfish carve the top of the tank', 22, 'none',
        [k(.07, 'pier_l', x=-.4, y=.2, b=.5), k(.24, 'pier_l', x=-.8, y=.5, b=.9, eye='-'), k(.46, 'pier_l', x=-1.0, y=.6, b=1.1, eye='o', mark='whew'), k(.66, 'pier_l', x=-.7, y=.5, b=.8, r=1), k(.84, x=.4, y=.2, b=.2, eye='O')],
        [], g='rest', act=('lean', 'post'), prefer=['tired', 'sad'])
    o.r('sulk_when_it_will_not_come_to_the_top', 'Sulking at the base of the wall with his bill in the air because the swordfish has gone deep and will not play', 22, 'none',
        [k(.08, x=-.8, y=-.2, b=.6), k(.26, 'flank_r', x=-1.6, y=-.9, b=1.2, eye='-'), k(.5, 'flank_r', x=-2, y=-1.2, b=1.9, eye='-', mark='tch'), k(.7, 'flank_r', x=-1.7, y=-1, b=1.6, l=1), k(.86, x=-.5, y=-.2, eye='-')],
        [], g='rest', act=('sulk', 'tank'), when=['sad'])
    # ---------------- weather
    o.r('fold_in_against_the_cold_wind_off_the_top', 'Folding both wings in tight against the cold that comes off the top of the tank, bill buried in the chest', 20, 'none',
        [k(.07, 'pier_l', x=-.2, y=.3, b=.8), k(.22, 'pier_l', x=-.5, y=.8, b=1.4, w=.2, eye='-'), k(.44, 'pier_l', x=-.7, y=1.0, b=1.8, eye='-', mark='brr'), k(.64, 'pier_l', x=-.6, y=.9, b=1.6, l=1, r=1), k(.84, x=.2, y=.2, b=.3, eye='^')],
        [], g='weather', act=('fold', 'wings'), when=['cold'], prefer=['tired'])
    o.r('chip_the_ice_along_the_top_run', 'Chipping the ice skin along the top run with a reed held out over the coping so the swordfish has a lane to slash in', 26, 'reed',
        [k(.06, 'skin_l', reach=.4, x=.2, y=-.2), k(.19, 'coping', reach=1, x=.5, y=-.4, b=-.2, mark='tk'), k(.32, 'skin_l', reach=1, x=.7, y=-.4, b=-.1, l=1, mark='TK'), k(.46, 'skin_r', reach=1, x=.8, y=-.3, b=0, r=1, mark='CRK'),
         k(.62, 'skin_r', reach=1, x=.9, y=-.4, b=-.1, l=1, mark='CRK'), k(.8, eye='^')],
        [(.46, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('scrape_the_rime_off_the_flank_wall', 'Scraping the rime off the lower wall with the side of a wing in flat downward strokes', 18, 'wing',
        [k(.07, 'low_l', reach=.5, x=.3, y=.6, b=.3), k(.21, 'low_l', reach=1, x=.6, y=1.0, b=.8, mark='skrr'), k(.36, 'flank_l', reach=1, x=.7, y=1.2, b=1.0, l=1, mark='skrr'), k(.52, 'flank_l', reach=1, x=.8, y=1.3, b=1.1, r=1),
         k(.7, 'low_r', reach=.6, x=.4, y=.7, b=.4), k(.88, eye='-')],
        [(.36, 'thaw')], g='weather', act=('scrape', 'rime'), when=['pond_ice>.3'])
    o.r('huddle_at_the_post_in_the_rain', 'Huddling against the right pier post with his bill tucked while the rain stipples the top of the tank and the sword keeps slashing', 30, 'none',
        [k(.07, 'pier_r', x=-.6, y=.8, b=.9), k(.26, 'pier_r', x=-1.1, y=1.7, b=1.7, eye='-'), k(.5, 'pier_r', x=-1.3, y=2.0, b=2.0, l=1, eye='-', mark='pit pat'), k(.74, 'pier_r', x=-1.2, y=1.9, b=1.8, r=1, mark='pit'),
         k(.9, x=.1, y=.2, b=.2, eye='^')],
        [], g='weather', act=('shelter', 'post'), when=['wet'])
    o.r('spread_a_wing_to_dry_in_the_sun', 'Spreading one wing wide at the left ledge to dry in the sun after a splash and then the other', 20, 'none',
        [k(.08, 'ledge_l', x=.3, y=.4, b=.6, perch=1), k(.26, 'ledge_l', x=.2, y=.5, b=.9, w=.8, l=1, eye='-', perch=1), k(.5, 'ledge_l', x=.2, y=.5, b=.9, w=1, eye='-', mark='ahh', perch=1), k(.72, 'ledge_l', x=.3, y=.4, b=.6, w=.5, r=1, perch=1),
         k(.9, eye='^')],
        [], g='weather', act=('dry', 'wings'), when=['sun'], prefer=['happy'])
    o.r('cool_both_feet_at_the_lip_on_a_hot_noon', 'Cooling his feet one at a time on the cold front lip on a hot noon, the swordfish a blur beyond the wall', 18, 'none',
        [k(.08, 'lip', x=.2, y=.5, b=.8, l=1, perch=1), k(.28, 'lip', x=.1, y=.7, b=1.1, l=1, eye='-', mark='ahh', perch=1), k(.5, 'lip', x=.1, y=.7, b=1.1, r=1, eye='-', perch=1), k(.74, 'lip', x=.3, y=.4, b=.5, perch=1, eye='^')],
        [], g='weather', act=('cool', 'feet'), when=['warm'], prefer=['summer'])
    # ---------------- show
    o.r('bow_to_the_flash_of_silver', 'Bowing to the flash of silver as the swordfish tops out against the wall and falls away, a crisp and speedy dip', 14, 'none',
        [k(.08, 'top_m', x=.6, y=.6, b=.6), k(.24, 'top_m', x=1.1, y=1.7, b=1.7, eye='-'), k(.44, 'top_m', x=1.2, y=1.9, b=1.9, eye='-', mark='sir'), k(.62, 'top_m', x=.6, y=.5, b=.4), k(.8, x=.1, y=-.4, w=.6, eye='^')],
        [], g='show', act=('bow', 'swordfish'), pick='hungriest', prefer=['happy'], obj=[(.24, dict(lure=1)), (.62, dict(lure=1))], say=["Bowed. Its sword went past my ear. Respect, both ways.", "I bow fast, it passes faster."])
    o.r('present_the_blade_to_the_morning', 'Presenting the long blade to the morning with a sweep of the wing along the top of the tank, a herald without a trumpet', 20, 'wing',
        [k(.07, 'top_l', reach=.4, x=.1, y=.1), k(.22, 'top_l', reach=.9, x=.3, y=-.3, b=-.3), k(.4, 'top_m', reach=1, x=.3, y=-.5, b=-.5, mark='the blade'), k(.58, 'top_r', reach=1, x=.4, y=-.4, b=-.3, r=1), k(.76, 'top_r', reach=.6, x=.5, y=0),
         k(.9, eye='^')],
        [], g='show', act=('present', 'blade'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_over_who_is_the_sharper', 'Arguing with the swordfish about which of them is the sharper, jabbing his bill at the sword and then at his own head', 22, 'none',
        [k(.06, 'low_l', x=.8, y=.5, b=.5), k(.2, 'low_l', x=1.4, y=.4, b=.3, mark='SHARPER'), k(.36, 'low_l', x=.4, y=.5, b=.7, l=1, mark='ME'), k(.52, 'low_l', x=1.5, y=.3, b=.2, r=1, mark='YOU'), k(.7, 'low_l', x=.4, y=.5, b=.6, eye='-', mark='ME!'),
         k(.86, eye='-')],
        [], g='show', act=('argue', 'edge'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It is a fish on a stick. I am, regardless, sharper.", "Lost on points. It had several."])
    o.r('pose_on_the_ledge_with_a_bill_raised_like_a_sword', 'Posing on the right ledge with his bill thrust up like a sword, wings back, hero of a very small ship', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.2, w=.3, perch=1), k(.24, 'ledge_r', x=.7, y=-.8, b=-.4, w=.6, perch=1), k(.5, 'ledge_r', x=.9, y=-1.2, b=-.7, w=1, perch=1, eye='^', mark='en garde'), k(.74, 'ledge_r', x=.3, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'ledge'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('shout_a_countdown_for_the_run', 'Shouting a countdown from the left post and flinging both wings up at zero as the swordfish tears down the tank', 18, 'none',
        [k(.06, 'pier_l', x=.3, y=-.1, b=.3), k(.18, 'pier_l', x=.5, y=-.4, b=-.2, w=.4, mark='THREE'), k(.3, 'pier_l', x=.6, y=-.5, b=-.3, w=.6, l=1, mark='TWO'), k(.42, 'pier_l', x=.7, y=-.6, b=-.4, w=.8, r=1, mark='ONE'),
         k(.56, 'pier_l', x=.9, y=-.9, b=-.8, w=1, mark='GO!'), k(.74, 'pier_l', x=.3, y=0, b=.1), k(.9, eye='@')],
        [], g='show', act=('shout', 'countdown'), pick='hungriest', prefer=['happy', 'young'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))], when=['slash>.3'],
        say=["Three, two, one. It was already at the far end.", "Starter's pistol for an animal that does not need one."])
    # ---------------- mishap
    o.r('slip_on_the_splashed_ledge', 'Slipping on the spray-slick ledge, one foot out front, and catching himself on the wall with a loud clap', 16, 'none',
        [k(.07, 'ledge_l', x=.6, y=.5, b=.5, perch=1), k(.19, 'ledge_l', x=1.3, y=-.3, b=-.9, l=1, r=1, w=1, mark='whoa!', perch=1), k(.32, 'low_l', x=1.7, y=1.4, b=1.8, w=.7, eye='O', mark='CLAP'), k(.5, 'ledge_l', x=.7, y=.6, b=.8, perch=1, eye='>'),
         k(.68, x=.2, y=.2, b=.2, eye='-')],
        [], g='mishap', act=('slip', 'spray'), when=['wet'], prefer=['young'])
    o.r('head_caught_between_the_pier_rungs', 'Poking his head between the right pier rungs to get a view of the sword up close and wriggling out the long way', 24, 'none',
        [k(.06, x=.8, y=.5, b=.5), k(.19, 'pier_r', x=1.9, y=.1, b=1.0, eye='O'), k(.36, 'pier_r', x=2.1, y=.2, b=1.3, l=1, eye='@', mark='mmph'), k(.54, 'pier_r', x=2.0, y=.3, b=1.2, r=1, w=.5, mark='mf'), k(.68, 'pier_r', x=1.5, y=-.4, b=-.8, w=1, mark='POP'),
         k(.86, x=1.1, y=1.0, b=.7, eye='-')],
        [], g='mishap', act=('stuck', 'rungs'), prefer=['young', 'grumpy'])
    o.r('track_the_streak_straight_into_the_wall', 'Tracking the streak along the top with his eyes only and bumping the wall nose first', 16, 'none',
        [k(.06, 'flank_l', x=.5, y=-.6, b=.3), k(.2, 'low_l', x=.6, y=-.7, b=.4, l=1), k(.34, 'top_l', x=.7, y=-.8, b=.4, r=1), k(.48, 'top_m', x=1.9, y=.0, b=1.5, eye='@', mark='THUNK'), k(.64, 'top_m', x=-1.1, y=.3, b=.1, w=.9, eye='x'),
         k(.82, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'wall'), prefer=['curious'])
    o.r('flinch_when_the_sword_hits_the_wall', 'Flinching back with a squawk when the sword smacks the wall right where his bill was resting, the whole tank shivering', 16, 'none',
        [k(.06, 'top_m', x=1.2, y=.7, b=.7), k(.16, 'top_m', x=1.4, y=.8, b=.9, eye='o', mark='...'), k(.24, x=-1.5, y=-1.0, b=-1.5, l=1, r=1, w=1, eye='O', mark='THWACK'), k(.4, x=-.9, y=.2, b=-.2, w=.7, eye='>'), k(.6, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'wall'), pick='hungriest', prefer=['young', 'curious'], obj=[(.16, dict(lure=1)), (.4, dict(lure=1))],
        say=["Eight inches from my face. It missed on purpose, I tell myself.", "That sword has a will of its own. And a hell of an aim."])
    o.r('stamp_at_the_spray_puddle', 'Stamping at the puddle of spray on the lip, as if the swordfish could be made to stop splashing', 16, 'none',
        [k(.06, 'lip', x=.7, y=.8, b=.5, perch=1), k(.17, 'lip', x=.5, y=-.1, b=-1.2, l=1, mark='STMP', perch=1), k(.28, 'lip', x=.6, y=.6, b=.6, perch=1), k(.4, 'lip', x=.5, y=-.1, b=-1.3, r=1, mark='STMP', perch=1),
         k(.54, 'lip', x=.6, y=.6, b=.6, perch=1), k(.68, 'lip', x=.5, y=-.2, b=-1.5, l=1, r=1, mark='STMP!', perch=1), k(.88, eye='-')],
        [], g='mishap', act=('stamp', 'puddle'), prefer=['grumpy'], when=['wake>.3'])
    # ---------------- duets
    o.r('hold_two_hoops_for_one_streak', 'Holding a reed hoop at the left of the tank while a friend holds another at the right, so the swordfish threads both in one pass', 28, 'reed',
        [k(.05, 'top_l', reach=.4, x=.2, y=.1), k(.18, 'skin_l', reach=1, x=.5, y=-.2, b=-.1), k(.32, 'skin_l', reach=1, x=.6, y=-.4, b=-.3, w=.2, mark='steady'), k(.46, 'skin_l', reach=1, x=.5, y=-.6, b=-.5, l=1, r=1, eye='O', mark='ZIP'),
         k(.62, 'top_l', reach=.8, x=.3, y=0, eye='o'), k(.8, eye='^')],
        [(.46, 'strike')], g='play', act=('hook', 'hoops'), pick='hungriest', prefer=['happy'], when=['slash>.3'], obj=[(.2, dict(lure=1)), (.42, dict(lure=1)), (.6, dict(lure=1))],
        duo=[k(.1, 'top_r', x=.3, y=.2, b=.2), k(.28, 'skin_r', x=.6, y=-.2, b=.2, w=.3), k(.44, 'skin_r', x=.7, y=-.4, b=-.2, w=.5, mark='steady'), k(.6, 'skin_r', x=.8, y=-.7, b=-.5, l=1, r=1, w=.8, eye='O', mark='ZIP'), k(.8, eye='^')],
        say=["One streak, two hoops, perfect. I only missed my hoop.", "A pass through both. The fish is the only one who looks calm."])
    o.r('flank_the_swordfish_from_the_two_ends', 'Tapping the left wall end in quick beats while a friend taps the right, the swordfish bouncing between the two sounds', 24, 'none',
        [k(.05, 'flank_l', x=.9, y=1.0, b=.6), k(.16, 'flank_l', x=1.3, y=1.4, b=.8, mark='tk'), k(.28, 'low_l', x=1.2, y=.9, b=.6, l=1), k(.4, 'flank_l', x=1.4, y=1.5, b=.9, r=1, mark='tk'), k(.56, 'low_l', x=1.2, y=.9, b=.6, eye='o'),
         k(.74, 'flank_l', x=.6, y=.7, b=.4), k(.88, eye='^')],
        [(.4, 'tease')], g='use', act=('tap', 'ends'), pick='hungriest', when=['slash<.7'], obj=[(.2, dict(lure=1)), (.45, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.1, 'flank_r', x=.8, y=1.0, b=.5), k(.22, 'flank_r', x=1.2, y=1.4, b=.8), k(.34, 'low_r', x=1.1, y=.9, b=.6, r=1, mark='tk'), k(.5, 'flank_r', x=1.3, y=1.5, b=.9, l=1, mark='tk'), k(.68, 'low_r', x=1.1, y=.9, b=.6), k(.84, eye='^')],
        say=["Ping, pong, fish. The slowest ball game ever, played at speed.", "Tap-tap left, tap-tap right, whoosh. Teamwork is exhausting."])
    o.r('keep_score_of_the_slashes_with_a_friend', 'Keeping score of the slashes with a friend, one tallying left to right and the other right to left, each with a different total', 24, 'wing',
        [k(.05, 'pier_l', reach=.4, x=.3, y=.4, b=.2, mark='1'), k(.16, 'low_l', reach=1, x=.5, y=.5, b=.4, mark='2'), k(.28, 'top_l', reach=1, x=.6, y=.3, b=.3, l=1, mark='3'), k(.4, 'top_m', reach=1, x=.7, y=.3, b=.3, r=1, mark='4'),
         k(.54, 'top_r', reach=1, x=.8, y=.3, b=.3, mark='5'), k(.7, 'pier_r', reach=.5, x=.4, y=.4, b=.2, eye='-', mark='6?'), k(.86, eye='^')],
        [], g='test', act=('count', 'tallies'), pick='shyest', prefer=['curious', 'happy'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))],
        duo=[k(.1, 'pier_r', x=.4, y=.4, b=.3, mark='1'), k(.24, 'top_r', x=.5, y=.3, b=.3, mark='2'), k(.38, 'top_m', x=.6, y=.3, b=.4, l=1, mark='3'), k(.54, 'top_l', x=.7, y=.3, b=.3, r=1, mark='4'), k(.7, 'pier_l', x=.4, y=.4, b=.3, eye='-', mark='7?'), k(.84, eye='^')],
        say=["Six and seven. The fish ignored the dispute and scored eleven.", "Two scorers, two totals. A fish keeps the real count."])
    return done(o)


def ancient_dragon_fish():
    # Ancient dragon fish: a very long glowing serpent with long whiskers, mid-water, active at night, a legend in the sea tank. Cheese works from the edge.
    # Own state: glow (builds after dark, fades by day: drawn), coil (how tightly it lies wound up: it uncoils to follow a wingtip, drawn), trail (the glow it
    # leaves along the wall as it uncoils: drawn, fades).
    o = Obj('ancient_dragon_fish', 'keeping', on='infinity_pool',
            fields=dict(glow=(0, 0, 1), coil=(0, 0, 1), trail=(0, 0, 1)),
            physics=[('glow', 'rate', .003, 'night'), ('glow', 'rate', -.004, '!night'), ('coil', 'rate', .0004, 'always'), ('trail', 'rate', -.003, 'always')],
            effects=dict(scrub=[('keeping.algae', 'mul', .5)], rake=[('keeping.leaves', 'mul', .35)], polish=[('keeping.clarity', 'add', .15)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], call=[('keeping.bell', 'add', .5)],
                         tribute=[('keeping.flakes', 'add', .4), ('subject.mood', 'add', .15)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)],
                         uncoil=[('coil', 'mul', .3), ('trail', 'set', 1), ('subject.trust', 'add', .1)], rise=[('subject.hunger', 'add', -.2), ('trail', 'set', 1)],
                         stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)], crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('glow', .3, '. * .', 'body_m', 'glow'), ('trail', .3, '~*~*~', 'low_l', 'glow'), ('coil', .5, '(OOO)', 'low_r', 'water'), ('pond_flakes', .3, ".':.'", 'skin_m', 'dust'),
                   ('pond_leaves', .3, ';"~;"', 'body_l', 'leaf'), ('pond_ice', .3, '*-*-*', 'body_r', 'frost'), ('pond_algae', .3, '"v"v"', 'base_l', 'plant')],
            anchors=dict(low_l=Q(36, 43), low_m=Q(58, 43), low_r=Q(86, 43), mid_l=Q(24, 40), body_l=Q(30, 37), body_m=Q(62, 37), body_r=Q(92, 37), skin_m=Q(68, 34), sign=Q(24, 33),
                         coping=Q(40, 28), base_l=Q(24, 46), ledge_l=Q(30, 49, 'surface'), ledge_r=Q(92, 49, 'surface'), pier_l=Q(10, 41), pier_r=Q(110, 41), lip=Q(60, 52, 'surface')))
    # ---------------- care
    o.r('wipe_the_green_so_the_glow_shows_true', 'Wiping the green film off the wall in slow curved strokes so the serpent\'s glow shows true, the wing moving like a lantern-tender', 24, 'wing',
        [k(.05, 'base_l', reach=.4, x=.2, y=.8, b=.4), k(.14, 'base_l', reach=1, x=.5, y=1.2, b=.8, mark='wsh'), k(.25, 'low_l', reach=1, x=.5, y=.9, b=.6, l=1, mark='wsh'), k(.38, 'mid_l', reach=1, x=.4, y=.4, b=.3, mark='wsh'),
         k(.52, 'low_m', reach=1, x=.6, y=.8, b=.6, r=1, mark='wsh'), k(.68, 'low_r', reach=1, x=.8, y=1.0, b=.7), k(.86, eye='^')],
        [(.38, 'scrub')], g='care', act=('wipe', 'algae'), when=['pond_algae>.4'],
        say=["Wall clear. It glowed twice as bright to say thanks.", "Cleaned the window. The legend grants no review."])
    o.r('rake_the_dark_leaf_mat_with_a_reed', 'Raking the dark leaf mat off the top of the water with a reed held out over the coping so the glow can reach the open air', 26, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.3, y=-.2), k(.19, 'coping', reach=1, x=.6, y=-.5, b=-.3, mark='rk'), k(.33, 'body_m', reach=1, x=.7, y=-.3, b=-.1, l=1, mark='rk'), k(.48, 'body_l', reach=1, x=.9, y=-.1, b=.1, r=1, mark='rk'),
         k(.66, 'body_l', reach=.7, x=.4, y=0, b=-.1), k(.84, eye='-')],
        [(.48, 'rake')], g='care', act=('rake', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'])
    o.r('polish_a_lens_in_the_wall_for_the_glow', 'Polishing a clear lens in the wall at chest height with small circles so every scale\'s glow can be seen through it', 22, 'wing',
        [k(.07, 'mid_l', reach=.5, x=.3, y=.3, b=.3), k(.2, 'mid_l', reach=1, x=.4, y=.2, b=.4, mark='sqk'), k(.34, 'body_l', reach=1, x=.5, y=.2, b=.3, l=1, mark='sqk'), k(.48, 'body_m', reach=1, x=.6, y=.3, b=.4, r=1, mark='sqk'),
         k(.64, 'low_m', reach=1, x=.7, y=.6, b=.6), k(.82, eye='o', mark='clear')],
        [(.48, 'polish')], g='care', act=('polish', 'lens'), when=['pond_clarity<.6'])
    o.r('peer_for_a_loose_jewel_scale', 'Peering along the serpent\'s glowing flank for any loose or missing scale as it unrolls past the wall', 22, 'none',
        [k(.05, x=.5, y=.5, b=.4), k(.15, 'low_l', x=1.5, y=1.3, b=.9, eye='o'), k(.27, 'mid_l', x=1.7, y=.8, b=.9, eye='O', mark='hm'), k(.4, 'body_l', x=1.8, y=.6, b=.8, l=1), k(.54, 'body_m', x=1.9, y=.6, b=.8, r=1, mark='ok'),
         k(.7, 'low_r', x=1.6, y=1.2, b=.9), k(.86, x=.6, y=.5, b=.3, w=.4, eye='^')],
        [(.54, 'tend')], g='care', act=('peer', 'scales'), pick='shyest', when=['fish_health<.8'], obj=[(.15, dict(lure=1)), (.4, dict(lure=1)), (.7, dict(lure=1))],
        say=["Every scale in place. It must have a good lawyer.", "A thousand jewels, none loose. Better kept than my feathers."])
    o.r('shoo_the_leaf_shadow_off_the_wall', 'Brushing the shadow of floating leaves off the wall with the tip of a wing where the glow should fall', 18, 'wing',
        [k(.07, 'body_r', reach=.5, x=.4, y=.1, b=.2), k(.2, 'body_r', reach=1, x=.7, y=.1, b=.3, mark='shh'), k(.34, 'body_m', reach=1, x=.9, y=.2, b=.3, l=1, mark='shh'), k(.5, 'body_l', reach=1, x=1.1, y=.2, b=.4, r=1),
         k(.68, 'body_l', reach=.6, x=.5, y=.1, b=.2), k(.86, eye='-')],
        [], g='care', act=('sweep', 'shadow'), prefer=['curious'], when=['glow>.3'])
    # ---------------- use
    o.r('tap_the_pier_post_for_a_slow_gong', 'Tapping the left pier post slowly with his bill, a gong beat that carries along the dark and brings the serpent unwinding', 20, 'none',
        [k(.06, 'pier_l', x=1.2, y=.6, b=.6, mark='dong'), k(.19, 'pier_l', x=1.3, y=.7, b=.7), k(.31, x=.1, y=.1, w=.3), k(.45, 'pier_l', x=1.4, y=.8, b=.8, l=1, mark='DONG'), k(.62, x=.3, y=.4, b=.3, eye='^'), k(.84, eye='-')],
        [(.45, 'call')], g='use', act=('tap', 'pier'), when=['pond_bell<.4'], prefer=['night', 'dusk'])
    o.r('fling_a_tribute_of_flakes_into_the_dark', 'Flinging a tribute of flakes up over the coping into the dark like an offering, the serpent\'s light rising slowly to meet them', 20, 'wing',
        [k(.07, 'body_m', reach=.3, x=.1, y=0), k(.2, 'body_m', reach=.9, x=.3, y=-.3, b=.6), k(.36, 'skin_m', reach=1, x=.5, y=-.9, b=-.9, mark='fwoo'), k(.52, x=-.3, y=0, b=-.2, eye='o'), k(.72, eye='^')],
        [(.36, 'tribute')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.4'], prefer=['night'], say=["A tribute to a legend: flakes and a bad pun.", "Flakes up over the wall. The legend is not above supper."])
    o.r('press_a_flake_to_the_wall_for_the_whiskers', 'Pressing one flake to the wall with his bill, the long whiskers drifting against the other side to find it', 22, 'none',
        [k(.06, x=.4, y=.7, b=.4), k(.18, 'low_m', x=1.7, y=1.7, b=.9, eye='o', mark='...'), k(.31, 'low_m', x=1.9, y=1.9, b=1.1, eye='O', mark='whff'), k(.45, 'low_m', x=1.8, y=1.8, b=1.0, l=1), k(.62, x=.6, y=.8, b=.5, w=.4, eye='^'),
         k(.82, eye='-')],
        [(.31, 'feed')], g='use', act=('press', 'flake'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.18, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=0))],
        say=["Whiskers first, then the mouth. It tastes by touch.", "One flake, a lot of ceremony."])
    o.r('unwind_the_serpent_with_a_slow_wingtip', 'Drawing a wingtip slowly along the wall so the tightly wound serpent unwinds a coil at a time and glides after it', 30, 'wing',
        [k(.04, 'low_r', reach=.4, x=.2, y=.7, b=.3), k(.14, 'low_r', reach=1, x=.4, y=.9, b=.5), k(.26, 'low_m', reach=1, x=.5, y=.9, b=.5, l=1), k(.4, 'low_l', reach=1, x=.6, y=.8, b=.5), k(.54, 'mid_l', reach=1, x=.7, y=.5, b=.4, r=1),
         k(.7, 'body_l', reach=1, x=.8, y=.2, b=.3, l=1), k(.88, eye='^')],
        [(.4, 'uncoil')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['coil>.4'], obj=[(.1, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.72, dict(lure=1))],
        say=["Unwound it yard by glowing yard. Longer than the wall.", "It followed the wingtip without hurry. Plenty to hurry about."])
    o.r('pat_the_wall_at_the_great_brow', 'Patting the wall with the back of a wing where the great brow rests, slow strokes like soothing a very large cat', 22, 'wing',
        [k(.06, 'body_l', reach=.4, x=.2, y=.2, b=.3), k(.2, 'body_l', reach=.9, x=.4, y=.3, b=.5, mark='pat'), k(.36, 'body_l', reach=1, x=.5, y=.3, b=.6, l=1, mark='pat'), k(.52, 'body_l', reach=1, x=.4, y=.3, b=.5, r=1, mark='pat'),
         k(.7, 'body_l', reach=.5, x=.2, y=.2, b=.3), k(.88, eye='^')],
        [(.36, 'stroke')], g='use', act=('pat', 'brow'), pick='shyest', prefer=['fish_trust<.8', 'lonely'], obj=[(.22, dict(lure=1)), (.64, dict(lure=1))])
    o.r('dangle_a_flake_for_the_legend_to_rise', 'Dangling a flake on a reed over the coping until the serpent rolls all the way up the wall to claim it, lit from within', 26, 'reed',
        [k(.05, 'coping', reach=.4, x=.2, y=-.1), k(.17, 'coping', reach=1, x=.5, y=-.5, b=-.2, mark='...'), k(.32, 'skin_m', reach=1, x=.7, y=-.6, b=-.3, l=1), k(.48, 'skin_m', reach=1, x=.4, y=-1.0, b=-.9, w=.3, eye='O', mark='GULP'),
         k(.64, 'body_m', reach=.8, x=-.3, y=.2, b=.2), k(.82, eye='>')],
        [(.48, 'rise')], g='use', act=('lift', 'flake'), pick='hungriest', when=['glow>.4'], obj=[(.17, dict(lure=1)), (.36, dict(lure=1)), (.54, dict(lure=1))],
        say=["Rose from the dark, took the flake, left the dark in my head.", "It surfaced like a lamp coming on."])
    # ---------------- play
    o.r('race_its_tail_down_the_wall', 'Racing the tail of the serpent down the wall, running the whole length and finding there is more serpent than wall', 22, 'none',
        [k(.04, 'base_l', x=.6, y=.2, b=.2), k(.13, 'low_l', x=1.3, y=.3, b=-.7, l=1, w=.4), k(.24, 'low_m', x=1.7, y=.2, b=.2, r=1, w=.7), k(.36, 'low_r', x=2.0, y=.3, b=-.9, l=1, w=1, mark='whew'), k(.5, 'pier_r', x=1.4, y=.4, b=.8, r=1),
         k(.66, 'pier_r', x=.5, y=.6, b=1.0, eye='@', mark='more?'), k(.84, eye='-')],
        [(.36, 'fun')], g='play', act=('race', 'tail'), pick='hungriest', prefer=['young', 'happy'], obj=[(.1, dict(lure=1)), (.26, dict(lure=1)), (.4, dict(lure=1)), (.56, dict(lure=1))],
        say=["Ran the wall's length. The tail was still on the other side of the sign.", "Still not at the tail. It has a second tail."])
    o.r('chase_the_beads_of_glow_with_a_wing', 'Chasing the drifting beads of glow along the wall with quick wing dabs, popping one only to see it re-form', 20, 'wing',
        [k(.06, 'low_l', reach=.6, x=.5, y=.7, b=.4), k(.18, 'mid_l', reach=1, x=.9, y=.4, b=.3, l=1, mark='fwp'), k(.3, 'body_l', reach=1, x=-.3, y=.3, b=.5, r=1, mark='fwp'), k(.44, 'body_m', reach=1, x=1.0, y=.2, b=.3, l=1, mark='pop'),
         k(.6, 'low_m', reach=1, x=1.1, y=.7, b=.5, eye='@'), k(.8, y=.4, eye='-')],
        [], g='play', act=('chase', 'glow'), pick='hungriest', prefer=['young', 'happy'], when=['trail>.3'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('step_a_slow_dance_in_the_glow', 'Stepping a slow solo dance at the front lip in the dark, every move made a beat after the serpent\'s shimmer', 26, 'none',
        [k(.05, 'lip', x=.2, y=.2, b=.3, perch=1), k(.17, 'lip', x=.5, y=0, b=-.4, w=.5, l=1, perch=1), k(.3, 'lip', x=.1, y=.4, b=.6, w=.2, perch=1), k(.44, 'lip', x=.6, y=-.1, b=-.5, w=.7, r=1, perch=1), k(.58, 'lip', x=.2, y=.5, b=.7, perch=1),
         k(.74, 'lip', x=.5, y=-.2, b=-.3, w=.9, l=1, perch=1, mark='ta-da'), k(.9, 'lip', x=.2, y=.2, b=.3, perch=1, eye='^')],
        [(.44, 'fun')], g='play', act=('dance', 'lip'), prefer=['happy', 'lonely'], when=['night'])
    o.r('look_for_the_serpent_by_its_own_light', 'Hunting along the wall for the serpent by following the faint glow it leaves in the dark, bill dipping at each smudge', 24, 'none',
        [k(.05, 'low_l', x=.7, y=.9, b=.5), k(.17, 'mid_l', x=1.0, y=.7, b=.7, eye='o', mark='?'), k(.3, 'body_l', x=1.2, y=.5, b=.7, eye='o', mark='?'), k(.43, 'body_m', x=1.3, y=.6, b=.8, l=1, mark='?'), k(.58, 'body_r', x=1.4, y=.5, b=.8, r=1, mark='?'),
         k(.72, 'low_r', x=1.5, y=1.1, b=1.0, eye='O', mark='found you'), k(.88, x=.4, y=.4, eye='^')],
        [], g='play', act=('seek', 'serpent'), pick='shyest', prefer=['young', 'curious'], when=['night'], obj=[(.72, dict(lure=1)), (.88, dict(lure=1))])
    o.r('balance_a_flake_on_his_bill_for_the_trail', 'Carrying a flake at the tip of his bill and swaying along the wall so the serpent trails the flake in a long glittering line', 24, 'none',
        [k(.05, 'low_l', x=.4, y=.3, b=.3), k(.17, 'low_l', x=.9, y=-.3, b=.5, w=.3), k(.3, 'low_m', x=1.1, y=-.4, b=.6, l=1, w=.5), k(.44, 'low_m', x=1.2, y=-.4, b=.5, w=.5), k(.58, 'low_r', x=1.3, y=-.3, b=.6, r=1, w=.4),
         k(.74, 'low_r', x=.8, y=0, b=.4, eye='^'), k(.9, eye='-')],
        [], g='play', act=('balance', 'flake'), pick='hungriest', prefer=['happy', 'young'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.7, dict(lure=1))])
    o.r('hop_the_ledge_in_time_with_its_flicker', 'Hopping the ledge in time with the flicker of its scales, one hop for each ripple of light that runs down its length', 20, 'none',
        [k(.05, 'ledge_l', x=.3, y=.3, b=.3, perch=1), k(.15, 'ledge_l', x=.4, y=-.2, b=-1.1, l=1, r=1, perch=1), k(.26, 'ledge_l', x=.3, y=.4, b=.7, perch=1), k(.38, 'ledge_r', x=.5, y=-.3, b=-1.3, w=.6, l=1, r=1, perch=1),
         k(.5, 'ledge_r', x=.3, y=.4, b=.7, perch=1), k(.64, 'ledge_r', x=.5, y=-.4, b=-1.5, w=.9, l=1, r=1, perch=1, mark='HUP'), k(.82, 'ledge_r', x=.3, y=.5, b=.8, perch=1, eye='>')],
        [], g='play', act=('hop', 'ledge'), pick='hungriest', prefer=['young', 'happy'], when=['glow>.3'], obj=[(.2, dict(lure=1)), (.5, dict(lure=1)), (.72, dict(lure=1))])
    # ---------------- test
    o.r('pace_out_its_length_along_the_ledge', 'Pacing out the serpent\'s length from the left ledge to the right, a toe-lift for every pace and a loud count at the far end', 30, 'none',
        [k(.04, 'ledge_l', x=.3, y=.4, b=.5, l=1, perch=1, mark='1'), k(.14, 'ledge_l', x=.4, y=.5, b=.6, r=1, perch=1, mark='4'), k(.26, 'lip', x=.4, y=.5, b=.6, l=1, perch=1, mark='9'), k(.4, 'lip', x=.5, y=.6, b=.7, r=1, perch=1, mark='14'),
         k(.55, 'ledge_r', x=.5, y=.6, b=.7, l=1, perch=1, mark='19'), k(.7, 'ledge_r', x=.4, y=.5, b=.6, r=1, perch=1, eye='O', mark='more!'), k(.88, 'ledge_r', x=.2, y=.2, b=.3, perch=1, eye='-')],
        [], g='test', act=('measure', 'serpent'), pick='hungriest', prefer=['curious'], obj=[(.15, dict(lure=1)), (.4, dict(lure=1)), (.65, dict(lure=1))],
        say=["Twenty-three paces and the tail was still unfinished. Legends are poor for stock-taking.", "A whole wall of serpent. The measure is mostly in the awe."])
    o.r('count_the_jewel_scales_on_one_flank', 'Counting the jewel scales on one flank with a bill dip each, giving up when the whole flank starts to flicker', 24, 'none',
        [k(.05, 'low_m', x=1.0, y=1.4, b=.7, mark='1'), k(.16, 'low_m', x=1.1, y=1.5, b=.8, mark='8'), k(.28, 'low_r', x=1.2, y=1.5, b=.9, l=1, mark='15'), k(.4, 'body_r', x=1.3, y=.9, b=.8, mark='26'), k(.54, 'body_m', x=1.3, y=.7, b=.8, r=1, mark='40?'),
         k(.68, x=-.3, y=.1, b=-.2, w=.4, eye='>', mark='again'), k(.86, eye='-')],
        [], g='test', act=('count', 'scales'), pick='shyest', prefer=['curious'], obj=[(.15, dict(lure=1)), (.5, dict(lure=1)), (.62, dict(lure=1))])
    o.r('read_the_sign_by_its_light', 'Reading the tank sign by the serpent\'s glow alone, going close and then far to find where the letters fade', 22, 'wing',
        [k(.05, 'mid_l', reach=.4, x=.3, y=.4, b=.3), k(.18, 'sign', reach=1, x=.5, y=-.5, b=-.2, mark='S'), k(.32, 'mid_l', reach=.5, x=.2, y=.6, b=.5, eye='o', mark='far'), k(.46, 'sign', reach=1, x=.6, y=-.5, b=-.3, l=1, mark='E'),
         k(.62, 'low_l', reach=.5, x=.2, y=.7, b=.6, eye='-', mark='fainter'), k(.8, eye='^')],
        [], g='test', act=('test', 'light'), prefer=['curious'], when=['glow>.4'])
    o.r('listen_for_the_low_hum_of_the_deep', 'Listening with his head against the left pier post for the low hum the old serpent makes in the dark', 24, 'none',
        [k(.06, x=-.4, y=.6, b=.5), k(.2, 'pier_l', x=-1.0, y=1.4, b=1.2, eye='-'), k(.4, 'pier_l', x=-1.3, y=1.8, b=1.6, eye='-', mark='mmm'), k(.6, 'pier_l', x=-1.4, y=1.9, b=1.8, eye='o', mark='MMM'), k(.78, 'pier_l', x=.3, y=.6, b=.4, eye='O'),
         k(.92, eye='^')],
        [], g='test', act=('listen', 'hum'), prefer=['curious', 'night'])
    o.r('weigh_the_legend_against_the_fact', 'Weighing the legend against the fact with a wing in each hand-spread, one up, one down, and neither quite sure which holds the serpent', 24, 'wing',
        [k(.05, 'low_l', reach=.4, x=.3, y=.6, b=.3), k(.18, 'low_l', reach=1, x=.5, y=.6, b=.4, mark='legend'), k(.34, 'low_m', reach=1, x=.5, y=.8, b=.6, l=1, mark='fact'), k(.5, 'low_m', reach=1, x=.5, y=.5, b=.3, r=1, mark='legend'),
         k(.68, 'low_r', reach=1, x=.6, y=.8, b=.6, mark='...'), k(.86, eye='-', mark='both')],
        [], g='test', act=('weigh', 'legend'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.25, dict(lure=1)), (.55, dict(lure=1))])
    o.r('count_the_coils_and_lose_the_count', 'Counting the coils where the serpent lies wound up, a toe lift for each, until the coils start counting him back', 26, 'none',
        [k(.05, 'low_r', x=.8, y=.8, b=.5, l=1, mark='one'), k(.17, 'low_r', x=.9, y=.9, b=.6, r=1, mark='two'), k(.3, 'low_m', x=1.0, y=.9, b=.6, l=1, mark='three'), k(.44, 'low_m', x=1.0, y=1.0, b=.7, r=1, mark='four'),
         k(.58, 'low_l', x=1.1, y=1.1, b=.8, l=1, eye='o', mark='five?'), k(.74, 'low_l', x=.3, y=.4, b=.2, eye='@', mark='wait'), k(.9, eye='-')],
        [], g='test', act=('count', 'coils'), prefer=['curious'], when=['coil>.5'])
    # ---------------- rest
    o.r('doze_off_in_the_green_light', 'Dozing off on the left ledge in the green light of its glow, bill on his chest, the wall shivering with light', 28, 'none',
        [k(.08, 'ledge_l', x=.2, y=.9, b=.9, eye='-', perch=1), k(.26, 'ledge_l', x=-.5, y=1.6, b=1.7, eye='-', perch=1), k(.5, 'ledge_l', x=-.8, y=2.1, b=2.3, eye='-', mark='zzz', perch=1), k(.74, 'ledge_l', x=-.3, y=.9, b=.9, eye='o', perch=1),
         k(.9, eye='^')],
        [(.5, 'rest')], g='rest', act=('nap', 'ledge'), when=['tired', 'night'])
    o.r('sit_at_the_lip_and_watch_it_wind', 'Sitting at the front lip with his feet tucked, watching the long body wind and unwind in the dark like a ribbon', 26, 'none',
        [k(.1, 'lip', x=.4, y=.2, b=.6, perch=1), k(.34, 'lip', x=0, y=.6, b=1.3, l=1, eye='-', perch=1), k(.58, 'lip', x=-.4, y=.9, b=1.8, eye='o', mark='...', perch=1), k(.8, 'lip', x=.5, y=.3, b=.5, r=1, perch=1, eye='^')],
        [(.58, 'rest')], g='rest', act=('sit', 'lip'), when=['dusk'], prefer=['tired', 'lonely'])
    o.r('wait_for_the_first_glimmer', 'Waiting stock-still by the wall at dusk for the first glimmer along the dark to wake', 24, 'none',
        [k(.08, 'body_m', x=.9, y=.5, b=.7, eye='o'), k(.3, 'body_m', x=1.0, y=.6, b=.9, eye='o'), k(.5, 'body_m', x=1.0, y=.6, b=.9, l=1), k(.7, 'body_m', x=1.1, y=.7, b=1.0, eye='O', mark='...'), k(.88, 'body_m', x=.4, y=.3, b=.4, eye='^')],
        [], g='rest', act=('wait', 'glimmer'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('lean_on_the_right_post_and_gaze', 'Leaning on the right pier post with his chin on a wing, gazing at the slow river of light along the wall', 22, 'none',
        [k(.09, 'pier_r', x=-.3, y=.1, b=.4), k(.26, 'pier_r', x=-.9, y=.4, b=1, eye='-'), k(.5, 'pier_r', x=-1.2, y=.5, b=1.3, eye='o', mark='ahh', l=1), k(.7, 'pier_r', x=-.8, y=.4, b=.9), k(.88, x=.5, y=.1, b=.1, eye='O')],
        [], g='rest', act=('lean', 'post'), prefer=['tired', 'sad'])
    o.r('sulk_when_the_glow_stays_down', 'Sulking at the dark wall with his back to the water because the old serpent has not lit up for anyone all night', 24, 'none',
        [k(.1, x=-.9, y=.3, b=.8), k(.3, 'base_l', x=-1.9, y=.8, b=1.6, eye='-'), k(.54, 'base_l', x=-2.3, y=1.1, b=2.2, eye='-', mark='tsk'), k(.74, 'base_l', x=-1.9, y=.9, b=1.8, r=1), k(.9, x=-.6, y=.2, eye='-')],
        [], g='rest', act=('sulk', 'dark'), when=['sad'])
    # ---------------- weather
    o.r('wrap_both_wings_round_himself_in_the_cold', 'Wrapping both wings round himself against the cold night, bill tucked, the only warm thing a glowing fish ahead', 22, 'none',
        [k(.07, 'ledge_r', x=-.2, y=.4, b=.9, perch=1), k(.22, 'ledge_r', x=-.4, y=.8, b=1.5, w=.3, eye='-', perch=1), k(.44, 'ledge_r', x=-.6, y=1.1, b=2.0, w=.8, eye='-', mark='brr', perch=1), k(.66, 'ledge_r', x=-.5, y=1.0, b=1.8, w=1, l=1, r=1, perch=1),
         k(.86, 'ledge_r', x=.2, y=.3, b=.4, perch=1, eye='^')],
        [], g='weather', act=('wrap', 'wings'), when=['cold'], prefer=['night', 'tired'])
    o.r('scoop_the_ice_plates_from_the_top', 'Scooping the thin plates of ice off the top of the tank with a reed held out over the coping so the glow can breathe', 26, 'reed',
        [k(.06, 'skin_m', reach=.4, x=.2, y=-.2), k(.19, 'coping', reach=1, x=.5, y=-.4, b=-.2, mark='clk'), k(.33, 'body_m', reach=1, x=.7, y=-.3, b=0, l=1, mark='clk'), k(.48, 'body_r', reach=1, x=.9, y=-.2, b=.1, r=1, mark='CRK'),
         k(.64, 'body_r', reach=.7, x=.4, y=-.1, b=-.1), k(.84, eye='^')],
        [(.48, 'crack')], g='weather', act=('scoop', 'ice'), when=['pond_ice>.3'])
    o.r('wipe_the_frost_flowers_off_the_lens', 'Wiping the frost flowers off the clear lens in the wall with a quick wing so the light can come through', 18, 'wing',
        [k(.08, 'mid_l', reach=.5, x=.3, y=.3, b=.3), k(.22, 'mid_l', reach=1, x=.5, y=.2, b=.5, mark='shff'), k(.38, 'body_l', reach=1, x=.6, y=.2, b=.4, l=1, mark='shff'), k(.54, 'body_r', reach=1, x=.9, y=.1, b=.3, r=1),
         k(.72, 'low_r', reach=.6, x=.6, y=.8, b=.5), k(.88, eye='-')],
        [(.38, 'thaw')], g='weather', act=('wipe', 'frost'), when=['pond_ice>.3'])
    o.r('shelter_with_a_wing_over_his_head_in_the_rain', 'Sheltering low on the left ledge with a wing over his head while the rain freckles the tank and the serpent glows right through it', 30, 'none',
        [k(.07, 'ledge_l', x=-.5, y=.8, b=1.0, perch=1), k(.25, 'ledge_l', x=-1.0, y=1.6, b=1.7, w=.5, eye='-', perch=1), k(.5, 'ledge_l', x=-1.2, y=1.9, b=2.1, w=.9, eye='-', mark='pit pit', perch=1), k(.74, 'ledge_l', x=-1.1, y=1.8, b=1.9, w=.9, l=1, perch=1),
         k(.9, 'ledge_l', x=.1, y=.3, b=.4, perch=1, eye='^')],
        [], g='weather', act=('shelter', 'ledge'), when=['wet'])
    o.r('straighten_every_feather_after_the_gust', 'Straightening every ruffled feather after a gust, preening wing to chest to tail in order, the glow for a mirror', 22, 'none',
        [k(.06, 'pier_r', x=.3, y=.3, b=.5, w=.2), k(.2, 'pier_r', x=-.4, y=.9, b=.9, w=.6, mark='nib'), k(.36, 'pier_r', x=.4, y=1.1, b=1.2, w=.3, l=1, mark='nib'), k(.52, 'pier_r', x=-.5, y=.8, b=.8, w=.7, r=1, mark='nib'),
         k(.7, 'pier_r', x=.2, y=.4, b=.4, w=.2), k(.88, eye='^')],
        [], g='weather', act=('straighten', 'feathers'), when=['windy'], prefer=['happy'])
    # ---------------- show
    o.r('bow_to_the_old_lamp_of_the_deep', 'Bowing low to the old lamp of the deep as its head glides up to the wall, a long respectful dip with the bill nearly touching', 18, 'none',
        [k(.08, 'body_l', x=.6, y=.8, b=.8), k(.26, 'body_l', x=1.2, y=1.8, b=2.0, eye='-'), k(.5, 'body_l', x=1.3, y=2.0, b=2.3, eye='-', mark='o great one'), k(.7, 'body_l', x=.7, y=.5, b=.6), k(.86, x=.1, y=-.4, w=.7, eye='^')],
        [], g='show', act=('bow', 'dragon'), pick='hungriest', prefer=['happy'], obj=[(.26, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed. It drifted past. The entire tank went green with approval.", "A duck bows to a legend. It glows twice as long."])
    o.r('present_the_serpent_to_the_stars', 'Presenting the serpent to the night sky with a sweeping arc of the wing along the whole wall, an usher for a legend', 22, 'wing',
        [k(.06, 'base_l', reach=.4, x=.1, y=.2), k(.18, 'low_l', reach=.8, x=.3, y=-.1, b=-.2), k(.32, 'body_l', reach=1, x=.3, y=-.4, b=-.4), k(.46, 'body_m', reach=1, x=.3, y=-.6, b=-.5, mark='behold'), k(.62, 'body_r', reach=1, x=.4, y=-.5, b=-.4, l=1),
         k(.78, 'body_r', reach=.6, x=.5, y=0), k(.92, eye='^')],
        [], g='show', act=('present', 'dragon'), pick='shyest', prefer=['happy'], obj=[(.46, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_which_of_them_is_the_older_legend', 'Arguing with the serpent over which of them is the older legend, a wing jab at the glow and a hand-on-chest claim for himself', 22, 'wing',
        [k(.06, 'low_m', reach=.5, x=.6, y=.5, b=.5), k(.2, 'low_m', reach=1, x=1.0, y=.4, b=.3, mark='OLDER'), k(.36, 'low_m', reach=.4, x=.3, y=.4, b=1.4, l=1, mark='ME'), k(.52, 'low_m', reach=1, x=1.1, y=.3, b=.2, r=1, mark='YOU'),
         k(.7, 'low_m', reach=.4, x=.3, y=.4, b=1.3, mark='ME'), k(.88, eye='-')],
        [], g='show', act=('argue', 'legend'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["I am the younger legend. By about a thousand years.", "Lost to a fish with scales like gems. I have feathers."])
    o.r('pose_in_the_green_light_like_a_statue', 'Posing on the right ledge as a statue in the green light, one wing on his chest and the other pointed at the stars', 18, 'none',
        [k(.06, 'ledge_r', x=.3, y=-.1, w=.3, perch=1), k(.24, 'ledge_r', x=.6, y=-.5, b=-.3, w=.6, perch=1), k(.5, 'ledge_r', x=.8, y=-.8, b=-.5, w=1, perch=1, eye='^', mark='behold'), k(.74, 'ledge_r', x=.3, y=0, w=.2, perch=1)],
        [], g='show', act=('pose', 'ledge'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sing_the_serpent_an_old_lullaby', 'Singing the serpent an old lullaby in a low voice, slow and wobbly, while its glow pulses to the long notes', 26, 'none',
        [k(.07, 'low_m', x=.9, y=1.2, b=.9), k(.24, 'low_m', x=1.2, y=2, b=1.7, eye='-', mark='laaa'), k(.44, 'low_m', x=1.4, y=2.3, b=2.1, eye='-', mark='laaaa'), k(.64, 'low_r', x=1.3, y=2, b=1.8, eye='-', mark='laaa', w=.4), k(.84, x=.5, y=.6, b=.4, eye='^')],
        [], g='show', act=('sing', 'lullaby'), pick='shyest', when=['night'], prefer=['lonely', 'sad'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        say=["It flickered on the chorus. My favourite review.", "Sang a lullaby to a thing that could swallow the sea. It listened."])
    # ---------------- mishap
    o.r('slip_on_the_ledge_in_the_dark', 'Slipping on the unseen wet patch of the ledge in the dark, feet out front, and clutching the wall on the way down', 16, 'none',
        [k(.08, 'ledge_l', x=.8, y=.7, b=.7, perch=1), k(.21, 'ledge_l', x=1.7, y=-.6, b=-1.2, l=1, r=1, w=1, mark='whoa!', perch=1), k(.34, 'low_l', x=2.0, y=1.6, b=2.2, w=.7, eye='O', mark='GRAB'), k(.52, 'ledge_l', x=.9, y=.9, b=1.1, perch=1, eye='>'), k(.7, x=.3, y=.3, b=.3, eye='-')],
        [], g='mishap', act=('slip', 'dark'), when=['wet'], prefer=['young'])
    o.r('head_wedged_between_two_pier_rungs', 'Wedging his head between two pier rungs reaching for a glow bead and having to twist free feather by feather', 24, 'none',
        [k(.07, x=1.1, y=.8, b=.7), k(.2, 'pier_l', x=2.4, y=.4, b=1.3, eye='O'), k(.38, 'pier_l', x=2.6, y=.5, b=1.6, l=1, eye='@', mark='mmph'), k(.55, 'pier_l', x=2.5, y=.6, b=1.5, r=1, w=.6, mark='mf'), k(.7, 'pier_l', x=1.9, y=-.2, b=-1.1, w=1, mark='POP'), k(.88, x=1.4, y=1.2, b=.9, eye='-')],
        [], g='mishap', act=('stuck', 'rungs'), prefer=['young', 'grumpy'])
    o.r('bump_the_wall_staring_up_at_the_glow', 'Staring up at the glow as it curls over the sign and bumping the wall hard with his bill', 16, 'none',
        [k(.07, 'low_l', x=.6, y=-.5, b=.2), k(.22, 'mid_l', x=.7, y=-.8, b=.3, l=1), k(.36, 'body_l', x=.8, y=-.9, b=.3, r=1), k(.5, 'body_m', x=2.2, y=-.2, b=1.7, eye='@', mark='DONK'), k(.66, 'body_m', x=-1.4, y=.4, w=1, eye='x'), k(.84, y=.5, eye='-')],
        [], g='mishap', act=('walk_into', 'wall'), prefer=['curious'], when=['night'])
    o.r('jump_back_when_the_glow_flares', 'Jumping back with a yelp when the whole serpent flares white right at his bill, the wall lit like a lightning strike', 16, 'none',
        [k(.06, 'body_l', x=1.1, y=.6, b=.7), k(.16, 'body_l', x=1.3, y=.7, b=.9, eye='o', mark='...'), k(.25, x=-1.5, y=-1.0, b=-1.5, l=1, r=1, w=1, eye='O', mark='BLINK'), k(.42, x=-.9, y=.2, b=-.2, w=.7, eye='>'), k(.6, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'flare'), pick='hungriest', prefer=['young', 'curious'], when=['glow>.4'], obj=[(.16, dict(lure=1)), (.42, dict(lure=1))],
        say=["White-out. I was a duck in a flashbulb.", "Eyes are still green. The serpent chuckled, probably."])
    o.r('stamp_the_dark_to_find_the_edge', 'Stamping about in the dark at the lip to find where the ledge ends, then stamping at the dark itself for good measure', 16, 'none',
        [k(.07, 'lip', x=.8, y=.7, b=.4, perch=1), k(.2, 'lip', x=.6, b=-1, l=1, mark='STMP', perch=1), k(.33, 'lip', x=.7, y=.5, b=.5, perch=1), k(.46, 'lip', x=.6, b=-1.1, r=1, mark='STMP', perch=1), k(.6, 'lip', x=.7, y=.5, b=.5, perch=1), k(.74, 'lip', x=.6, y=-.1, b=-1.4, l=1, r=1, mark='STMP!', perch=1), k(.9, eye='-')],
        [], g='mishap', act=('stamp', 'dark'), prefer=['grumpy'], when=['night'])
    # ---------------- duets
    o.r('hold_the_serpent_between_two_wings', 'Standing at the left end of the wall while a friend stands at the right, the serpent\'s whole glowing length stretched between the two of them', 28, 'wing',
        [k(.05, 'low_l', reach=.5, x=.3, y=.7, b=.4), k(.16, 'low_l', reach=1, x=.5, y=.7, b=.5), k(.3, 'mid_l', reach=1, x=.6, y=.4, b=.4, l=1, mark='this end'), k(.48, 'mid_l', reach=1, x=.5, y=.3, b=.3),
         k(.66, 'low_l', reach=.7, x=.4, y=.5, b=.4, r=1), k(.84, eye='^')],
        [(.3, 'uncoil')], g='use', act=('guard', 'length'), pick='hungriest', when=['coil>.4'], prefer=['happy'], obj=[(.15, dict(lure=1)), (.35, dict(lure=1)), (.6, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.1, 'low_r', x=.4, y=.7, b=.4), k(.26, 'low_r', x=.7, y=.7, b=.5, l=1), k(.44, 'low_r', x=.8, y=.6, b=.4, mark='that end'), k(.64, 'low_r', x=.7, y=.7, b=.5, r=1), k(.84, eye='^')],
        say=["Both ends held. The middle is the part nobody is holding.", "Two ducks, one serpent, a strange knot of respect."])
    o.r('trade_gong_beats_between_the_two_posts', 'Tapping the left post twice and listening while a friend answers on the right post, the serpent\'s glow rolling across to each beat', 24, 'none',
        [k(.05, 'pier_l', x=1.2, y=.5, b=.5, mark='dong'), k(.16, 'pier_l', x=1.3, y=.6, b=.6, l=1, mark='dong'), k(.3, x=-.3, y=.2, b=.2, w=.3, eye='o'), k(.5, 'pier_l', x=1.4, y=.7, b=.7, r=1, mark='DONG'), k(.7, x=.2, y=.3, b=.3, eye='^'),
         k(.86, eye='-')],
        [(.5, 'call')], g='play', act=('ring', 'posts'), pick='hungriest', when=['pond_bell<.4'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))],
        duo=[k(.12, 'pier_r', x=.3, y=.4, b=.3), k(.34, 'pier_r', x=1.1, y=.6, b=.6, mark='dong'), k(.46, 'pier_r', x=1.2, y=.7, b=.7, l=1, mark='dong'), k(.64, 'pier_r', x=1.3, y=.7, b=.7, r=1, mark='DONG'), k(.84, eye='^')],
        say=["Left, right, glow. A very slow ping-pong.", "A call, an answer, a long luminous silence."])
    o.r('sing_a_round_with_a_friend_for_the_deep', 'Singing a round with a friend, each coming in a beat apart and the serpent\'s glow riding the overlap', 28, 'none',
        [k(.05, 'low_m', x=.7, y=1.0, b=.8), k(.18, 'low_m', x=1.0, y=1.6, b=1.4, eye='-', mark='row'), k(.34, 'low_m', x=1.1, y=1.9, b=1.8, eye='-', mark='row row'), k(.52, 'low_m', x=1.2, y=2.0, b=1.9, eye='-', l=1, mark='row row row'),
         k(.7, 'low_r', x=1.0, y=1.7, b=1.5, eye='-', mark='...'), k(.86, eye='^')],
        [], g='show', act=('sing', 'round'), pick='shyest', when=['glow>.3'], prefer=['happy', 'lonely'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.12, 'low_l', x=.7, y=.9, b=.7), k(.3, 'low_l', x=.9, y=1.4, b=1.2, eye='-', mark='la'), k(.46, 'low_l', x=1.0, y=1.7, b=1.6, eye='-', mark='la la'), k(.64, 'low_l', x=1.1, y=1.8, b=1.7, eye='-', r=1, mark='la la la'), k(.82, eye='^')],
        say=["Off by a whole bar and the fish loved it.", "A round sung to the deep. It came back around."])

    # ---------------- extra acts
    o.r('thread_the_glow_through_a_reed_hoop', 'Holding a reed bent into a hoop out over the coping so the serpent can thread its glowing length through it in a long lazy S', 28, 'reed',
        [k(.05, 'body_r', reach=.4, x=.2, y=.1), k(.18, 'body_m', reach=1, x=.5, y=-.2, b=-.1), k(.33, 'skin_m', reach=1, x=.6, y=-.5, b=-.3, w=.2, mark='steady'), k(.5, 'skin_m', reach=1, x=.5, y=-.7, b=-.5, l=1, r=1, eye='O', mark='SWOOSH'),
         k(.66, 'body_m', reach=.8, x=.3, y=0, b=0, eye='o'), k(.84, eye='^')],
        [(.5, 'uncoil')], g='use', act=('lift', 'hoop'), pick='hungriest', prefer=['fish_trust>.4', 'happy'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.6, dict(lure=1))],
        say=["Through the ring, all of it, and the ring did not blink.", "The hoop is now a halo. I decline credit."])
    o.r('match_his_bill_to_a_whisker', 'Holding his bill up beside one trailing whisker on the wall and comparing the two, the whisker winning by several lengths', 22, 'none',
        [k(.06, x=.4, y=.5, b=.3), k(.19, 'low_m', x=1.4, y=1.4, b=.8, eye='o'), k(.34, 'low_m', x=1.0, y=1.6, b=1.1, l=1, mark='mine'), k(.5, 'low_l', x=1.8, y=1.2, b=.9, r=1, mark='its'), k(.66, 'low_r', x=1.9, y=1.1, b=.9, eye='O', mark='more'),
         k(.84, eye='-')],
        [], g='test', act=('compare', 'whiskers'), pick='shyest', prefer=['curious', 'young'], obj=[(.25, dict(lure=1)), (.55, dict(lure=1))])
    o.r('cool_his_cheek_on_the_wall_in_the_muggy_dark', 'Cooling one cheek and then the other against the cool wall on a muggy night, the glow rippling past an inch away', 20, 'none',
        [k(.07, 'mid_l', x=.9, y=.5, b=.6), k(.22, 'mid_l', x=1.3, y=.7, b=.9, eye='-', mark='ahh'), k(.4, 'mid_l', x=1.1, y=.8, b=1.0, eye='-', l=1), k(.6, 'body_l', x=1.2, y=.5, b=.9, eye='-', r=1), k(.8, x=.4, y=.3, eye='^')],
        [], g='weather', act=('cool', 'cheek'), when=['warm'], prefer=['night', 'tired'])
    return done(o)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['salmon', 'trout', 'sturgeon', 'pufferfish', 'swordfish', 'ancient_dragon_fish']:
        globals()[n]().emit()
