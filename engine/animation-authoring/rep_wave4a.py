"""Wave 4a: six freshwater fish kept in the koi pond: catfish, bass, carp, ghost_fish, golden_koi, minnow.
Every routine is hand-written. Cheese stays on the rim (row 46 of the koi_pond drawing, 120 cols x 55 rows, 7.5 px a row); a kept fish is drawn at the rim
spot he touches (lure + pick). Drawing: three cattail stems with `#` heads at the left (cols 7/12/17), three tall ones at the right (cols 103/108/113),
a grass tuft at the foot (row 44), two lily pads with `{*}` blooms (left one high, rows 30-32; right one low, rows 35-38), rippling water rows 29-45,
a far edge line at row 27, a stone bank round it `( )`, and front stones at the rim, row 46 and the rows just in front of it.
Anchors below are (column, row) of that drawing converted by P(). Marks stamp visible state: the pond's own leaves, ice, flakes and algae (pond_* marks, never copied onto the fish) and each fish's own
sunk pellets, silt, glow and rings."""
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
W, ROWS = 120, 55


def P(c, r, *fl):
    return (round(c / (W - 1), 4), round(r / ROWS, 4), *([' '.join(fl)] if fl else []))


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


def catfish():
    # Catfish: bottom dweller, evening and night, whiskers (barbels). Own state: feel (how well it and Cheese read each other through the barbels),
    # pellets (sunk pellets resting on the bottom, drawn).
    o = Obj('catfish', 'keeping', on='koi_pond',
            fields=dict(feel=(0, 0, 1), pellets=(0, 0, 1)),
            physics=[('feel', 'rate', -.0003, 'always'), ('pellets', 'rate', -.0008, 'always')],
            effects=dict(skim=[('keeping.leaves', 'mul', .4)], scrape=[('keeping.algae', 'mul', .5)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], husk=[('pellets', 'mul', .2), ('keeping.clarity', 'add', .15)],
                         shade=[('keeping.plants', 'mul', .75)], sink=[('pellets', 'set', 1), ('keeping.flakes', 'add', .35)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         read=[('feel', 'add', .25), ('subject.trust', 'add', .1)], lead=[('feel', 'add', .15), ('subject.trust', 'add', .1)],
                         stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)], crack=[('keeping.ice', 'mul', .3)],
                         thaw=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('pellets', .3, '.:.:.', 'bed_m', 'dust'), ('pond_leaves', .3, '"~;"~', 'edge_far', 'leaf'), ('pond_ice', .3, '*-*-*', 'bed_l', 'frost')],
            anchors=dict(bed_l=P(28, 43), bed_m=P(58, 41), bed_r=P(88, 39), pad_low=P(86, 37), tuft=P(11, 44), reed_low=P(8, 38),
                         bank_r=P(95, 40), edge_far=P(70, 43), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46)))
    # ---------------- care
    o.r('skim_the_leaf_mat', 'Raking the mat of fallen leaves off the dark water with a reed and heaping it at the left bank', 22, 'reed',
        [k(.14, 'bed_r', reach=.6, x=.3, y=.3, w=.2), k(.34, 'bed_m', reach=1, x=.7, y=.4, b=.4, mark='shk'), k(.54, 'bed_l', reach=1, x=.8, y=.5, b=.5, mark='shk'), k(.76, 'tuft', reach=.8, x=.4, y=.6, b=.3), k(.9, eye='^')],
        [(.54, 'skim')], g='care', act=('rake', 'leaf_mat'), when=['pond_leaves>.3'], prefer=['windy'], say=["Leaves out. Cat did not even look up.", "Heaped the lot by the tuft. Compost, if it asks."])
    o.r('scrape_the_belly_stone_green', 'Scraping the green slime off the stone where the catfish rubs its belly, flat edge of a wing', 18, 'wing',
        [k(.12, 'stone_r', reach=.6, x=.2, y=.8, b=.4), k(.3, 'stone_r', reach=1, x=.4, y=1.3, b=.9, l=1, mark='sksk'), k(.5, 'bank_r', reach=1, x=.5, y=1.1, b=.8, mark='sksk'), k(.7, 'bank_r', reach=1, x=.3, y=.9, b=.7, r=1), k(.88, y=.1, eye='^')],
        [(.5, 'scrape')], g='care', act=('scrape', 'slime'), when=['pond_algae>.4'], say=["Slime off. The cat can rub on bare rock like an adult.", "Scraped a rock for a fish. Tomorrow I scrape for me."])
    o.r('unwind_a_weed_thread_from_a_barbel', 'Unwinding a thread of weed from one barbel, whisker by whisker, with the very tip of his bill', 24, 'none',
        [k(.12, x=.4, y=.5, b=.4), k(.3, 'bed_l', x=1.1, y=1.7, b=.9, eye='-'), k(.48, 'bed_l', x=1.3, y=1.9, b=1.2, l=1, mark='tug'), k(.66, 'bed_l', x=.9, y=1.3, b=.8, r=1, mark='plip'), k(.84, y=.2, w=.3, eye='^')],
        [(.48, 'tend')], g='care', act=('unwrap', 'barbel'), pick='shyest', when=['fish_health<.8'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        say=["Off. It sat still for the whole thing. Brave, or asleep.", "Whisker one, whisker two. Cat is spotless now, weirdly."])
    o.r('sweep_the_husks_off_the_shelf', 'Sweeping the sunk pellet husks off the shallow shelf with a wing before they cloud the water', 18, 'wing',
        [k(.12, 'bed_m', reach=.5, x=.3, y=.7, b=.4), k(.3, 'bed_m', reach=1, x=.6, y=1.3, b=.9, mark='shff'), k(.5, 'edge_far', reach=1, x=.7, y=1.4, b=1, l=1, mark='shff'), k(.7, 'bed_r', reach=1, x=.5, y=1.2, b=.8, r=1), k(.88, eye='-')],
        [(.5, 'husk')], g='care', act=('sweep', 'husks'), when=['pellets>.3'], prefer=['curious'])
    o.r('comb_the_silt_from_the_barbels', 'Combing silt out of the long whiskers with the flat of a wing while the cat holds its chin to the rim', 22, 'wing',
        [k(.12, 'bed_m', reach=.5, x=.2, y=.9, b=.5), k(.3, 'bed_m', reach=1, x=.4, y=1.5, b=1.1, mark='scrt'), k(.5, 'bed_m', reach=1, x=.3, y=1.7, b=1.3, l=1, r=1, mark='scrt'), k(.7, 'bed_m', reach=1, x=.3, y=1.4, b=1, mark='scrt'), k(.88, eye='^')],
        [(.5, 'tend')], g='care', act=('groom', 'barbels'), pick='hungriest', prefer=['fish_health<.9', 'happy'], obj=[(.28, dict(lure=1)), (.65, dict(lure=1))])
    o.r('hook_the_overgrown_pads_back', 'Hooking the overgrown lily pad over with a twig and pulling it back off the dark corner it shades', 22, 'twig',
        [k(.12, 'pad_low', reach=.5, x=.3, y=.2), k(.3, 'pad_low', reach=1, x=.6, y=.5, b=.4, mark='hnk'), k(.5, 'pad_low', reach=1, x=.8, y=.4, b=.7, l=1), k(.7, 'pad_low', reach=1, x=-.2, y=-.4, b=-.4, w=.4, mark='pop'), k(.88, eye='-')],
        [(.5, 'shade')], g='care', act=('pull', 'pads'), when=['pond_plants>.7'])
    # ---------------- use
    o.r('toss_pellets_over_the_deep_edge', 'Flicking a wingful of sinking pellets over the deep edge so they patter down onto the bottom', 16, 'wing',
        [k(.15, 'bed_m', reach=.5, w=.4), k(.35, 'bed_m', reach=1, b=-.4, w=1, mark='pt pt pt'), k(.6, x=-.4, y=.3, eye='o'), k(.85, eye='^')],
        [(.35, 'sink')], g='use', act=('throw', 'pellets'), when=['pellets<.4'], prefer=['dusk'], say=["Pellets down. Now we wait for the whiskers.", "Dinner is served at the bottom. Where cats keep their standards."])
    o.r('hold_a_pellet_to_the_hungriest_cat', 'Dangling one pellet from his bill just above the deep edge until the hungriest cat sucks it in', 20, 'none',
        [k(.12, x=.4, y=.6, b=.5), k(.3, 'bed_l', x=1.3, y=1.7, b=1, eye='o', mark='...'), k(.5, 'bed_l', x=1.2, y=1.9, b=1.2, eye='O', mark='slurp'), k(.72, 'bed_l', x=.6, y=.8, b=.5, w=.4, eye='^'), k(.9, eye='-')],
        [(.5, 'feed')], g='use', act=('carry', 'pellet'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1)), (.78, dict(lure=0))],
        say=["Whole pellet, no chewing. A cat that trusts the system.", "That mouth could take my bill off. It chose not to."])
    o.r('knock_three_slow_on_the_rim', 'Knocking three slow beats on the right stone with his bill so the cat feels dinner through the rock', 18, 'none',
        [k(.12, 'stone_r', x=1.2, y=1.5, b=.6, mark='tok'), k(.3, 'stone_r', x=1.3, y=1.6, b=.8, mark='tok'), k(.48, x=-.2, y=.1, w=.2), k(.66, 'stone_r', x=1.4, y=1.7, b=.9, l=1, mark='TOK'), k(.86, eye='^')],
        [(.66, 'call')], g='use', act=('knock', 'stone'), when=['pond_bell<.4'], prefer=['dusk', 'night'])
    o.r('press_a_wingtip_for_it_to_read', 'Pressing one wingtip flat on the water so the cat reads it with its whiskers, tip to heel', 22, 'wing',
        [k(.12, 'bed_m', reach=.5, x=.2, y=.6, b=.4), k(.3, 'bed_m', reach=1, x=.3, y=1, b=.8, mark='...'), k(.5, 'edge_far', reach=1, x=.4, y=1.1, b=.9, r=1, mark='hm'), k(.7, 'bed_m', reach=1, x=.3, y=1, b=.8), k(.9, eye='^')],
        [(.5, 'read')], g='use', act=('press', 'wingtip'), pick='shyest', when=['feel<.7'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('draw_the_cat_along_the_floor_row', 'Dragging a wingtip along the water over the deep row so the cat feels its way after it, left to right', 26, 'wing',
        [k(.1, 'bed_l', reach=.6, x=.2, y=.7, b=.4), k(.28, 'bed_m', reach=1, x=.4, y=.9, b=.5, l=1), k(.5, 'edge_far', reach=1, x=.5, y=.9, b=.6, r=1), k(.7, 'bed_r', reach=1, x=.5, y=.9, b=.6, l=1), k(.9, eye='^')],
        [(.5, 'lead')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['feel<.8'], obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.5, dict(lure=1)), (.75, dict(lure=1))],
        say=["Followed me blind, the whole way. Lovely, trusting idiot.", "Led a cat by the wing. Nobody leads me."])
    o.r('stroke_the_flat_head_with_a_wing', 'Stroking the cat\'s broad flat head with the back of a wing as it rests its chin at the rim', 20, 'wing',
        [k(.12, 'bed_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'bed_l', reach=1, x=.3, y=1.4, b=1.1, mark='pat'), k(.5, 'bed_l', reach=1, x=.2, y=1.5, b=1.3, l=1, mark='pat pat'), k(.7, 'bed_l', reach=1, x=.3, y=1.3, b=1), k(.9, eye='^')],
        [(.5, 'stroke')], g='use', act=('pat', 'head'), pick='shyest', prefer=['fish_trust<.8', 'lonely'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))])
    o.r('tap_a_toe_until_it_noses_up', 'Tapping a toe on the lowest stone over and over until the cat noses at the sound with its whiskers', 20, 'none',
        [k(.12, 'stone_l', x=.3, y=.8, b=.6, l=1), k(.3, 'stone_l', x=.4, y=1.1, b=.9, r=1, mark='tp'), k(.5, 'stone_l', x=.3, y=1, b=.8, l=1, mark='tp'), k(.7, 'bed_l', x=1, y=1.3, b=.9, r=1, mark='tp tp'), k(.88, eye='-')],
        [(.7, 'stroke')], g='use', act=('tap', 'toe'), pick='hungriest', prefer=['young', 'happy'], obj=[(.5, dict(lure=1)), (.75, dict(lure=1))])
    # ---------------- play
    o.r('race_the_cat_along_the_bank', 'Racing the cat along the right bank at a bounding trot, the whiskers just keeping up', 20, 'none',
        [k(.1, 'bed_l', x=.5, y=.5, b=.4), k(.28, 'bed_m', x=1, y=.6, b=-.5, l=1, w=.5), k(.46, 'edge_far', x=1.2, y=.6, b=-.7, r=1, w=.7, mark='hup'), k(.64, 'bed_r', x=1.3, y=.6, b=-.5, l=1, w=.5), k(.84, 'bank_r', x=.3, y=.4, b=.3, eye='@')],
        [(.46, 'fun')], g='play', act=('race', 'bank'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=1))],
        say=["Lost, narrowly. It does not even use legs.", "Cat won by a barbel. I want a recount."])
    o.r('blow_bubbles_down_to_it', 'Blowing a string of bubbles into the water so the cat noses up through the rising beads', 18, 'none',
        [k(.12, x=.3, y=.6, b=.5), k(.3, 'bed_m', x=1.2, y=1.8, b=1, eye='-', mark='bbl'), k(.5, 'bed_m', x=1.3, y=2, b=1.3, eye='-', mark='bbl bbl'), k(.7, 'bed_m', x=.8, y=1.1, b=.6, eye='O'), k(.88, eye='^')],
        [], g='play', act=('blow', 'bubbles'), pick='shyest', prefer=['young', 'happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))], say=["It popped one with its face. Good form.", "Blew bubbles at a fish. This is what ducks are for."])
    o.r('send_a_leaf_over_its_head', 'Floating a drifting leaf over the cat\'s dark patch with the tip of a wing and watching it nose it', 22, 'wing',
        [k(.12, 'bed_r', reach=.5, x=.2, y=.5, b=.3), k(.3, 'bed_r', reach=1, x=.5, y=.8, b=.6, mark='fwp'), k(.5, 'edge_far', reach=1, x=.6, y=.9, b=.7, l=1), k(.7, 'bed_m', reach=1, x=.7, y=.9, b=.7, r=1, mark='bmp'), k(.88, eye='o')],
        [], g='play', act=('float', 'leaf'), pick='shyest', when=['pond_leaves>.2'], prefer=['curious'], obj=[(.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('drum_the_bank_for_the_shivers', 'Drumming both feet on the front stone to send shivers down the bank for the whiskers to pick up', 18, 'none',
        [k(.12, 'stone_m', x=.2, y=.4, b=-.5, l=1), k(.28, 'stone_m', x=.3, y=.5, b=-.7, r=1, mark='thud'), k(.44, 'stone_m', x=.2, y=.4, b=-.6, l=1, mark='thud'), k(.6, 'stone_m', x=.3, y=.5, b=-.7, r=1, mark='thud'), k(.8, 'bed_m', x=.9, y=1.1, b=.7, eye='O')],
        [], g='play', act=('drum', 'bank'), pick='hungriest', prefer=['young', 'grumpy'], obj=[(.5, dict(lure=1)), (.85, dict(lure=1))])
    o.r('look_for_it_in_the_shaded_pads', 'Hunting for the cat in the shade of the right-hand pads, one wing flicking each pad over', 22, 'wing',
        [k(.12, 'bed_r', reach=.5, x=.8, y=.9, b=.4), k(.3, 'pad_low', reach=1, x=1.1, y=.8, b=.9, eye='o'), k(.5, 'pad_low', reach=1, x=1.3, y=1.2, b=1.3, l=1, eye='O', mark='huh'), k(.7, 'bed_r', reach=1, x=.9, y=1.2, b=1.1, r=1, eye='>'), k(.88, eye='^', mark='there')],
        [], g='play', act=('seek', 'cat'), pick='shyest', prefer=['young', 'curious'], obj=[(.55, dict(lure=1)), (.8, dict(lure=1))])
    o.r('chase_the_whisker_shadow_with_a_wing', 'Chasing the cat\'s long whisker shadow along the water with a wing, never quite pinning it', 18, 'wing',
        [k(.12, 'bed_l', reach=.7, x=.4, y=.7, b=.5), k(.3, 'bed_m', reach=1, x=.9, y=.6, b=.3, w=0, l=1, mark='fwp'), k(.5, 'edge_far', reach=1, x=-.5, y=.8, b=.7, r=1, mark='fwp'), k(.7, 'bed_m', reach=1, x=.9, y=.7, b=.4, l=1), k(.88, y=.4, eye='@')],
        [], g='play', act=('chase', 'shadow'), pick='hungriest', prefer=['happy'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('skip_a_pellet_to_the_far_edge', 'Skipping a pellet across the water off the bill so it lands at the far edge and the cat goes after it', 20, 'none',
        [k(.12, x=.5, y=.6, b=.4), k(.3, 'bed_l', x=1.4, y=1.2, b=.8, mark='...'), k(.46, x=-.6, y=-.8, b=-.9, w=.8, l=1, mark='fwip'), k(.62, 'edge_far', x=.4, y=.4, b=.3, eye='O'), k(.84, 'bed_r', x=.6, y=.7, b=.4, eye='^')],
        [], g='play', act=('throw', 'pellet'), pick='hungriest', prefer=['happy', 'curious'], obj=[(.62, dict(lure=1)), (.85, dict(lure=1))])
    # ---------------- test
    o.r('measure_the_whisker_span', 'Holding a reed across the cat\'s whiskers to see how far they spread, then against his own wing', 24, 'reed',
        [k(.12, 'bed_m', reach=.5, x=.3, y=.5, b=.3), k(.3, 'bed_m', reach=1, x=.5, y=.9, b=.6), k(.5, 'bed_l', reach=1, x=.5, y=.9, b=.7, l=1, mark='hm'), k(.7, 'bed_m', reach=.8, x=-.2, y=.5, w=.5, b=.4), k(.9, eye='O', mark='huge')],
        [], g='test', act=('measure', 'whiskers'), pick='shyest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1))], say=["Wider than my wings. It is mostly moustache.", "Spanned it twice. Still not a fair measure."])
    o.r('peer_into_the_great_mouth', 'Peering down into the cat\'s wide open mouth to see how far the dark goes', 18, 'none',
        [k(.12, x=.4, y=.7, b=.5), k(.3, 'bed_m', x=1, y=1.9, b=1.2, eye='O'), k(.5, 'bed_m', x=1.1, y=2.2, b=1.4, eye='@', mark='...'), k(.7, x=-.7, y=-.4, b=-.3, w=.6, eye='>'), k(.88, eye='-')],
        [], g='test', act=('peer', 'mouth'), pick='hungriest', prefer=['curious', 'young'], obj=[(.28, dict(lure=1)), (.6, dict(lure=1))], say=["Big enough for my head. I did not test that.", "Looked in. Saw a lot of cat."])
    o.r('listen_at_the_bottom_edge', 'Listening with an ear to the stones at dusk for the slow sounds of a cat moving along the bottom', 20, 'none',
        [k(.12, x=-.2, y=.8, b=.6), k(.3, 'stone_l', x=-.6, y=1.6, b=1.2, eye='-'), k(.55, 'stone_l', x=-.7, y=1.8, b=1.4, eye='-', mark='...'), k(.78, 'stone_l', x=-.3, y=.8, b=.6, eye='o'), k(.9, eye='^')],
        [], g='test', act=('listen', 'bottom'), prefer=['curious', 'dusk'], say=["Heard a cat think. Mostly about pellets.", "Stone says nothing. Cat says even less."])
    o.r('count_the_sunk_pellets', 'Counting the sunk pellets still resting down below, one tap of the bill on the water for each', 22, 'none',
        [k(.12, 'bed_m', x=.8, y=1.2, b=.5, mark='1'), k(.3, 'bed_m', x=.9, y=1.4, b=.7, mark='2'), k(.48, 'edge_far', x=1, y=1.4, b=.7, l=1, mark='3'), k(.66, 'bed_r', x=1, y=1.5, b=.8, mark='4'), k(.84, eye='-', mark='some')],
        [], g='test', act=('count', 'pellets'), when=['pellets>.3'], prefer=['curious'])
    o.r('sniff_the_silt_the_cat_stirs', 'Sniffing the brown plume where the cat rooted along the bottom, then sneezing it off', 16, 'none',
        [k(.15, x=.4, y=1, b=.4), k(.35, 'edge_far', x=1.4, y=1.7, b=1, mark='snf'), k(.55, 'edge_far', x=1.3, y=1.9, b=1.2, eye='-'), k(.75, x=-1, y=-.6, b=-.4, w=.7, eye='>', mark='ACHOO'), k(.9, eye='-')],
        [], g='test', act=('sniff', 'silt'), prefer=['curious', 'young'])
    o.r('sound_the_depth_with_a_reed', 'Sounding the deep edge with a reed to find how far down the cat lies at night', 22, 'reed',
        [k(.12, 'bed_r', reach=.5, x=.3, y=.4, b=.3), k(.3, 'bed_r', reach=1, x=.6, y=1.3, b=.9, mark='plink'), k(.5, 'bed_m', reach=1, x=.7, y=1.6, b=1.2, mark='plink'), k(.7, 'bed_l', reach=1, x=.7, y=1.9, b=1.4, l=1, mark='plink'), k(.88, eye='o')],
        [], g='test', act=('test', 'depth'), when=['night'], prefer=['curious'])
    o.r('weigh_it_against_the_wild_record', 'Stretching a wing out past the cat\'s length and comparing it with how long a wild one could grow', 22, 'wing',
        [k(.12, 'bed_l', reach=.5, x=.3, y=.7, b=.4), k(.3, 'bed_l', reach=1, x=.4, y=1, b=.6), k(.5, 'bed_r', reach=1, x=.6, y=.8, b=.4, r=1, mark='whoa'), k(.7, 'bed_m', reach=.7, x=.2, y=.4, b=.3), k(.88, eye='-', mark='bigger')],
        [], g='test', act=('compare', 'size'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- rest
    o.r('nap_by_the_stone_after_dark', 'Dozing off on the middle stone while the cat patrols the bottom, one eye on the bank', 26, 'none',
        [k(.12, 'stone_m', x=.2, y=.8, b=.8, eye='-'), k(.3, 'stone_m', x=-.3, y=1.4, b=1.5, eye='-', perch=1), k(.6, 'stone_m', x=-.5, y=1.8, b=2, eye='-', mark='zz', perch=1), k(.82, 'stone_m', x=-.2, y=.6, b=.6, eye='o'), k(.92, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'stone'), when=['tired', 'night'])
    o.r('sit_at_the_bank_for_the_dark', 'Sitting at the bank with his feet tucked, watching the water go black and the cat come up', 24, 'none',
        [k(.12, 'tuft', x=.2, y=.6, b=.7), k(.3, 'tuft', x=-.2, y=1, b=1.3, eye='-'), k(.6, 'tuft', x=-.3, y=1.2, b=1.5, eye='o'), k(.82, x=.3, y=.4, b=.4, eye='^')],
        [(.6, 'rest')], g='rest', act=('sit', 'bank'), when=['dusk'], prefer=['tired', 'lonely'])
    o.r('lean_on_a_low_reed_and_wait', 'Leaning his shoulder to the low reed and waiting for a whisker to break the water', 20, 'none',
        [k(.12, 'reed_low', x=-.3, y=.4, b=.5), k(.3, 'reed_low', x=-.6, y=.7, b=.9, eye='-'), k(.55, 'reed_low', x=-.7, y=.9, b=1, eye='-', mark='...'), k(.78, x=.4, y=.4, b=.3, eye='O'), k(.9, eye='^')],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'sad'])
    o.r('wait_for_the_whiskers_to_show', 'Waiting stock-still at the rim for the first whisker to break the black water', 22, 'none',
        [k(.12, 'bed_l', x=.7, y=1.3, b=.8, eye='o'), k(.35, 'bed_l', x=.8, y=1.5, b=1, eye='o'), k(.6, 'bed_l', x=.8, y=1.5, b=1, eye='O', mark='...'), k(.8, 'bed_l', x=.4, y=.8, b=.5, eye='^')],
        [], g='rest', act=('wait', 'whisker'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sulk_at_the_empty_water', 'Sulking at the water with his back to the bank because the cat has not come up all day', 22, 'none',
        [k(.12, x=-.6, y=.9, b=.9), k(.3, 'bed_r', x=-1.4, y=1.8, b=1.6, eye='-'), k(.55, 'bed_r', x=-1.7, y=2.1, b=2, eye='-', mark='hmph'), k(.8, x=-.5, y=.7, b=.6, eye='-')],
        [], g='rest', act=('sulk', 'water'), when=['sad'])
    # ---------------- weather
    o.r('chip_the_ice_off_the_bank_hole', 'Chipping the ice back from the rim to keep a breathing hole open for the cat', 22, 'none',
        [k(.12, 'stone_l', x=.8, y=1.1, b=.5), k(.3, 'bed_l', x=1.2, y=1.7, b=1, mark='tk'), k(.5, 'bed_l', x=1.3, y=1.9, b=1.2, l=1, mark='TK'), k(.7, 'bed_l', x=1.2, y=1.8, b=1.1, r=1, mark='crk'), k(.88, y=.1, eye='^')],
        [(.5, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('scrape_the_rime_off_the_front_stone', 'Scraping the white rime off the left stone with a wing so the cat\'s landing ledge is clear', 18, 'wing',
        [k(.12, 'stone_l', reach=.5, x=.2, y=.8, b=.4), k(.3, 'bed_l', reach=1, x=.4, y=1.3, b=.9, mark='skrr'), k(.5, 'bed_l', reach=1, x=.5, y=1.4, b=1, r=1, mark='skrr'), k(.7, 'stone_l', reach=1, x=.3, y=1, b=.7), k(.88, eye='-')],
        [(.5, 'thaw')], g='weather', act=('scrape', 'rime'), when=['pond_ice>.3'])
    o.r('splash_the_dull_water_awake', 'Beating the surface with both wings in short slaps to put air back into the sluggish water', 20, 'wing',
        [k(.12, 'bed_m', reach=.6, x=.3, y=.4, b=.3), k(.3, 'bed_m', reach=1, x=.4, y=.5, b=-.3, l=1, mark='SPLSH'), k(.48, 'edge_far', reach=1, x=.5, y=.5, b=-.4, r=1, mark='SPLSH'), k(.66, 'bed_r', reach=1, x=.5, y=.5, b=-.3, l=1, mark='SPLSH'), k(.86, eye='@')],
        [(.48, 'stir')], g='weather', act=('splash', 'air'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('stand_out_the_rain_at_the_reed', 'Sheltering at the low reed with his bill tucked while the rain pocks the water over the cat', 30, 'none',
        [k(.12, 'reed_low', x=-.3, y=.5, b=.6), k(.3, 'reed_low', x=-.8, y=1.3, b=1.2, eye='-'), k(.6, 'reed_low', x=-.9, y=1.5, b=1.4, eye='-', mark='drip'), k(.85, x=.2, y=.3, b=.3, eye='^')],
        [], g='weather', act=('shelter', 'reed'), when=['wet'])
    o.r('warm_a_foot_on_the_sun_stone', 'Warming one foot and then the other at the sunny right-hand stone beside the cat\'s deep corner', 18, 'none',
        [k(.12, 'stone_r', x=.2, y=.6, b=.5, l=1), k(.3, 'stone_r', x=.2, y=.8, b=.7, l=1, eye='-'), k(.55, 'stone_r', x=.2, y=.8, b=.7, r=1, eye='-', mark='ahh'), k(.8, x=.3, y=.3, b=.3, eye='^')],
        [], g='weather', act=('warm', 'foot'), when=['sun'], prefer=['tired'])
    o.r('brace_at_the_bank_in_the_gust', 'Bracing his chest at the right bank against the gust so the blown leaves skid past the cat\'s corner', 18, 'none',
        [k(.12, 'bank_r', x=.6, y=.2, b=.6), k(.3, 'bank_r', x=1, y=.5, b=1, w=.6, mark='whoo'), k(.5, 'bank_r', x=1.1, y=.6, b=1.2, w=.8, l=1), k(.72, 'bank_r', x=.8, y=.4, b=.8, r=1, w=.4), k(.88, eye='-')],
        [], g='weather', act=('brace', 'gust'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_big_cat', 'Bowing low to the big cat as it comes up out of the black, a respectful bill-dip at the rim', 16, 'none',
        [k(.12, 'bed_m', x=.5, y=.8, b=.6), k(.35, 'bed_m', x=.9, y=2.1, b=1.6, eye='-'), k(.6, 'bed_m', x=.9, y=2.2, b=1.7, eye='-', mark='sir'), k(.82, x=.2, y=-.3, w=.4, eye='^')],
        [], g='show', act=('bow', 'cat'), pick='hungriest', prefer=['happy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed. It blinked. We are even.", "Respect costs a neck muscle. Worth it."])
    o.r('present_the_cat_to_the_dark', 'Sweeping a wing out over the black water to present the cat to nobody, a ringmaster with no ring', 20, 'wing',
        [k(.12, 'bed_r', reach=.5, x=.2, y=.2, w=.2), k(.3, 'bed_m', reach=1, x=.2, y=-.2, b=-.3), k(.5, 'bed_l', reach=1, x=.2, y=-.3, b=-.4, mark='tadaa'), k(.7, 'bed_l', reach=1, x=.4, y=-.2, b=-.2), k(.88, eye='^')],
        [], g='show', act=('present', 'cat'), pick='shyest', prefer=['happy'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_the_moustache_rights', 'Arguing with the cat nose to nose about whose moustache is the better one, jabbing a wing at the water', 20, 'wing',
        [k(.12, 'bed_m', reach=.6, x=.5, y=.5, b=.5), k(.3, 'bed_m', reach=1, x=.9, y=.3, b=.2, mark='NOPE'), k(.5, 'bed_m', reach=1, x=1, y=.2, b=.1, r=1, mark='NOPE'), k(.7, 'bed_m', reach=.6, x=.3, y=.4, b=.3), k(.88, eye='-')],
        [], g='show', act=('argue', 'moustache'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Mine is only two lines. It has a moustache and a mood.", "Lost the argument. Kept the grudge."])
    o.r('pose_at_the_stone_with_the_cat', 'Holding a heroic pose on the left stone while the cat sits below him like a sponsor', 18, 'none',
        [k(.12, 'stone_l', x=.3, y=-.2, w=.4, perch=1), k(.3, 'stone_l', x=.5, y=-.5, b=-.2, w=.8, perch=1), k(.6, 'stone_l', x=.6, y=-.6, b=-.2, w=1, perch=1, eye='^', mark='ta-da'), k(.85, 'stone_l', x=.2, y=0, w=.3, perch=1)],
        [], g='show', act=('pose', 'stone'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sing_the_cat_a_night_song', 'Singing a low night song at the water for the cat, a slow bill-bob to every whisker twitch', 22, 'none',
        [k(.12, 'bed_m', x=.7, y=.9, b=.8), k(.3, 'bed_m', x=1, y=1.6, b=1.3, eye='-', mark='la'), k(.5, 'bed_m', x=1.1, y=1.9, b=1.7, eye='-', mark='laaa'), k(.7, 'bed_m', x=1, y=1.5, b=1.2, eye='-', mark='la'), k(.86, eye='^')],
        [], g='show', act=('sing', 'cat'), pick='shyest', when=['night'], prefer=['lonely', 'sad'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))], say=["It stayed for the chorus. Left before the bridge.", "Low notes only. The cat has standards, mostly bass."])
    # ---------------- mishap
    o.r('slip_on_the_wet_rim_stone', 'Slipping on the wet left stone, both feet out, and catching the rim with a flap of wings', 16, 'none',
        [k(.12, 'stone_l', x=.4, y=.5, b=.4), k(.3, 'stone_l', x=1, y=.2, b=-.6, l=1, r=1, w=1, mark='whoa!'), k(.5, 'stone_l', x=1.3, y=1, b=1.2, w=.8, eye='O'), k(.72, 'stone_l', x=.4, y=.5, b=.5, eye='>'), k(.88, eye='-')],
        [], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('jammed_between_two_reed_stems', 'Jamming his head between the two low reeds after a glimpse of whisker and having to haul himself out', 24, 'none',
        [k(.12, x=.5, y=.4, b=.4), k(.3, 'reed_low', x=1.2, y=.2, b=.8, eye='O'), k(.5, 'reed_low', x=1.3, y=.2, b=1.1, l=1, eye='@', mark='mmf'), k(.7, 'reed_low', x=1.2, y=.3, b=1, r=1, w=1, mark='POP'), k(.86, x=1.6, y=.9, b=.6, eye='-')],
        [], g='mishap', act=('stuck', 'reed'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_tall_dark_stem', 'Striding straight at the left cattail stem in the dark, staring at the water for a whisker', 20, 'none',
        [k(.12, 'bed_l', x=.5, y=.6, b=.4), k(.3, 'tuft', x=.5, y=.1, b=.6), k(.5, 'reed_low', x=1.3, y=-.3, b=1.3, eye='@', mark='BONK'), k(.7, 'reed_low', x=-.8, y=.4, b=.4, w=.6, eye='x'), k(.88, y=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'cattail'), when=['night_late'])
    o.r('hop_back_from_the_snapping_jaws', 'Hopping back from the rim when the cat\'s big mouth snaps at a bill-tip that looked like a pellet', 16, 'none',
        [k(.12, 'bed_m', x=.8, y=1.4, b=.7), k(.28, 'bed_m', x=1, y=1.6, b=1, eye='o', mark='...'), k(.42, x=-1.2, y=-.8, b=-1.4, l=1, r=1, w=1, eye='O', mark='YIKES'), k(.6, x=-.6, y=.3, b=.2, eye='>'), k(.82, x=.2, y=.2, eye='-')],
        [], g='mishap', act=('hop', 'jaws'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))], say=["It mistook my face for a snack. Fair, mostly.", "Jaws. In a pond. Eight inches from my bill."])
    o.r('stamp_the_pellet_cloud_flat', 'Stamping at the pellet cloud that billowed up over the cat after a clumsy toss', 16, 'none',
        [k(.12, 'bed_m', x=.8, y=1, b=.6), k(.3, 'edge_far', x=.6, y=.2, b=-.8, l=1, mark='STMP'), k(.5, 'edge_far', x=.7, y=.2, b=-.8, r=1, mark='STMP'), k(.7, 'edge_far', x=.6, y=.6, b=.3, l=1, eye='>'), k(.86, eye='-')],
        [(.3, 'husk')], g='mishap', act=('stamp', 'cloud'), when=['pellets>.5'], prefer=['grumpy'])
    # ---------------- duets (a friend takes their own part)
    o.r('answer_each_others_knocks_to_the_cat', 'Knocking on the left stone while a friend answers on the right, passing the beat across the bank for the cat to follow', 24, 'none',
        [k(.1, 'stone_l', x=1.1, y=1.3, b=.6, mark='tok'), k(.3, 'stone_l', x=1.2, y=1.4, b=.7, l=1, mark='tok'), k(.5, 'stone_m', x=.3, y=.3, b=-.3, w=.4), k(.7, 'stone_l', x=1.2, y=1.4, b=.7, r=1, mark='tok tok'), k(.88, eye='^')],
        [(.7, 'call')], g='play', act=('ring', 'stones'), pick='hungriest', prefer=['happy'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.2, 'stone_r', x=.3, y=.4, b=-.3), k(.4, 'stone_r', x=1.2, y=1.4, b=.7, mark='tok'), k(.6, 'stone_r', x=1.3, y=1.5, b=.8, l=1, mark='tok'), k(.8, 'stone_r', x=.4, y=.4, b=.3, eye='^')])
    o.r('hold_the_bank_weed_while_a_friend_unpicks_it', 'Hauling the tangled weed back from the whiskers with a wing while a friend picks it off with a bill', 26, 'wing',
        [k(.1, 'bed_m', reach=.6, x=.2, y=.6, b=.4), k(.3, 'bed_m', reach=1, x=.5, y=1, b=.8, mark='hff'), k(.5, 'bed_m', reach=1, x=.2, y=.8, b=1, l=1, mark='hff'), k(.7, 'bed_m', reach=1, x=.3, y=.9, b=.7), k(.88, eye='-')],
        [(.5, 'tend')], g='care', act=('tug', 'tangle'), pick='shyest', when=['fish_health<.8'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.15, 'bed_l', x=.4, y=.6, b=.4), k(.34, 'bed_l', x=1.2, y=1.6, b=1, eye='-'), k(.55, 'bed_l', x=1.3, y=1.8, b=1.2, r=1, mark='plick'), k(.8, 'bed_l', x=.5, y=.7, b=.5, eye='^')])
    o.r('compare_whisker_counts_with_a_friend', 'Comparing counts with a friend, one at each end of the rim, over how many barbels the cat really has', 24, 'none',
        [k(.1, 'bed_l', x=.8, y=1.2, b=.5, mark='1'), k(.3, 'bed_l', x=.9, y=1.3, b=.6, mark='2'), k(.5, 'bed_r', x=.9, y=1.1, b=.6, l=1, eye='-', mark='6?'), k(.7, 'bed_l', x=.8, y=1.2, b=.5, mark='8!'), k(.88, eye='^')],
        [], g='test', act=('count', 'barbels'), pick='shyest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.75, dict(lure=1))],
        duo=[k(.15, 'bed_r', x=.7, y=1, b=.5, eye='o'), k(.35, 'bed_r', x=.8, y=1.1, b=.6, mark='4'), k(.55, 'bed_l', x=.9, y=1.2, b=.6, r=1, mark='8'), k(.78, 'bed_r', x=.5, y=.7, b=.4, eye='^')],
        say=["Eight. Argued down from eleven. Whiskers do not hold still.", "Two ducks counting a fish. Fish keeps the number."])
    return done(o)


def bass():
    # Bass: mid-water ambusher, morning and evening, very jumpy. Own state: lunge (how wound up it is: leaps raise it, rest lowers it; too high and it
    # overshoots the rim), ring (ripple rings left on the water by a leap or a strike, drawn).
    o = Obj('bass', 'keeping', on='koi_pond',
            fields=dict(lunge=(0, 0, 1), ring=(0, 0, 1)),
            physics=[('lunge', 'rate', -.0003, 'always'), ('ring', 'rate', -.004, 'always')],
            effects=dict(scoop=[('keeping.leaves', 'mul', .35)], scour=[('keeping.algae', 'mul', .5)], thin=[('keeping.plants', 'mul', .75)],
                         skim=[('keeping.flakes', 'mul', .3)], tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)],
                         rescue=[('subject.health', 'add', .15), ('lunge', 'mul', .4)], scatter=[('keeping.flakes', 'add', .4)],
                         leaptake=[('subject.hunger', 'add', -.2), ('lunge', 'add', .25), ('ring', 'set', 1)], call=[('keeping.bell', 'add', .5)],
                         trick=[('lunge', 'add', .3), ('subject.trust', 'add', .1)], dimple=[('ring', 'set', 1), ('subject.mood', 'add', .15)],
                         lead=[('lunge', 'add', .15), ('subject.trust', 'add', .1)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)],
                         crack=[('keeping.ice', 'mul', .3)], defrost=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('ring', .3, 'o O o', 'surf_m', 'water'), ('pond_flakes', .3, '.:.:.', 'lane', 'dust'), ('pond_ice', .3, '*=*=*', 'surf_l', 'frost')],
            anchors=dict(surf_l=P(28, 43), surf_m=P(58, 41), surf_r=P(88, 39), lane=P(70, 43), cove=P(40, 39), pad_low=P(86, 37), bloom_r=P(81, 35), cattail_l=P(7, 31),
                         reed_low=P(8, 38), bank_r=P(95, 40), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46)))
    # ---------------- care
    o.r('scoop_the_leaves_from_the_leaping_lane', 'Scooping the drifted leaves out of the open lane the bass leaps from, one long pull of a reed', 20, 'reed',
        [k(.14, 'surf_r', reach=.6, x=.3, y=.4, w=.2), k(.34, 'lane', reach=1, x=.6, y=.6, b=.4, mark='swsh'), k(.56, 'cove', reach=1, x=.8, y=.7, b=.6, mark='swsh'), k(.78, 'surf_l', reach=.8, x=.4, y=.5, b=.3), k(.9, eye='^')],
        [(.56, 'scoop')], g='care', act=('scoop', 'leaves'), prefer=['pond_leaves>.3', 'windy'], say=["Lane's clear. Now it can hit the water properly.", "Leaves out. It doesn't thank anyone. Standard fish."])
    o.r('pull_the_pads_off_the_launch_water', 'Hooking the thick lily pad back with a twig to open water for a clean leap', 22, 'twig',
        [k(.12, 'pad_low', reach=.5, x=.2, y=.4, b=.3), k(.3, 'pad_low', reach=1, x=.5, y=.7, b=.5, mark='hnk'), k(.5, 'bloom_r', reach=1, x=.6, y=.5, b=.8, l=1, r=1), k(.7, 'pad_low', reach=1, x=-.1, y=-.2, b=-.2, w=.4, mark='pop'), k(.88, eye='-')],
        [(.5, 'thin')], g='care', act=('pull', 'pads'), when=['pond_plants>.7'])
    o.r('sweep_the_flake_film_to_the_rim', 'Sweeping the film of old flakes off the surface in to the rim with a wing before it sours', 18, 'wing',
        [k(.12, 'lane', reach=.5, x=.3, y=.9, b=.4), k(.3, 'lane', reach=1, x=.6, y=1.3, b=.8, mark='shff'), k(.5, 'surf_m', reach=1, x=.7, y=1.4, b=1, l=1, mark='shff'), k(.7, 'surf_l', reach=1, x=.5, y=1.2, b=.8, r=1), k(.88, eye='-')],
        [(.5, 'skim')], g='care', act=('sweep', 'film'), when=['pond_flakes>.3'])
    o.r('rub_the_algae_off_the_pad_stems', 'Rubbing the green off the reed stem at the left bank where the bass lies up waiting', 18, 'wing',
        [k(.12, 'reed_low', reach=.6, x=.2, y=.7, b=.4), k(.3, 'reed_low', reach=1, x=.3, y=1.2, b=.9, l=1, mark='sqk'), k(.5, 'reed_low', reach=1, x=.4, y=1.4, b=1.1, mark='sqk'), k(.7, 'tuft_dummy', reach=1)] if False else
        [k(.12, 'reed_low', reach=.6, x=.2, y=.7, b=.4), k(.3, 'reed_low', reach=1, x=.3, y=1.2, b=.9, l=1, mark='sqk'), k(.5, 'reed_low', reach=1, x=.4, y=1.4, b=1.1, mark='sqk'), k(.7, 'reed_low', reach=1, x=.2, y=1, b=.8, r=1), k(.88, eye='^')],
        [(.5, 'scour')], g='care', act=('scrub', 'stem'), when=['pond_algae>.4'])
    o.r('shove_the_stranded_bass_back_in', 'Nudging the bass that overshot and landed flapping at the rim back over the lip with a wing', 20, 'wing',
        [k(.12, 'stone_m', reach=.6, x=.3, y=.9, b=.6, eye='O'), k(.3, 'stone_m', reach=1, x=.5, y=1.5, b=1.2, mark='flap'), k(.5, 'surf_m', reach=1, x=.7, y=1.4, b=1, l=1, mark='shff'), k(.7, 'surf_m', reach=1, x=.4, y=.8, b=.6, w=0), k(.88, y=.2, eye='^')],
        [(.5, 'rescue')], g='care', act=('nudge', 'jumper'), pick='hungriest', when=['lunge>.7'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))],
        say=["Back in. It will do that again by lunchtime.", "Saved a fish from the stones. It had no plan."])
    o.r('dab_the_scraped_chin', 'Dabbing the bass\'s scraped chin from the last landing with the damp tip of a wing', 18, 'wing',
        [k(.12, 'surf_l', reach=.5, x=.2, y=.9, b=.5), k(.3, 'surf_l', reach=1, x=.3, y=1.3, b=1, mark='dab'), k(.5, 'surf_l', reach=1, x=.2, y=1.5, b=1.2, r=1, mark='dab dab'), k(.7, 'surf_l', reach=.5, x=.2, y=.8, b=.6), k(.88, eye='-')],
        [(.5, 'tend')], g='care', act=('pat', 'chin'), pick='shyest', when=['fish_health<.8'], obj=[(.3, dict(lure=1)), (.65, dict(lure=1))])
    # ---------------- use
    o.r('fling_flakes_in_a_high_arc', 'Flinging a wingful of flakes in a high arc so they spatter down over the open lane', 16, 'wing',
        [k(.15, 'lane', reach=.5, w=.5), k(.35, 'lane', reach=1, x=-.4, y=-.8, b=-.8, w=1, mark='fwip'), k(.6, x=-.4, y=.2, eye='o'), k(.85, eye='^')],
        [(.35, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.3'], prefer=['dawn', 'dusk'])
    o.r('hold_a_flake_high_for_the_leap', 'Lifting one flake in his bill just out of the water so the hungriest bass has to leap for it', 22, 'none',
        [k(.12, x=.4, y=.4, b=.4), k(.3, 'surf_m', x=1, y=.3, b=.7, eye='o', mark='...'), k(.46, 'surf_m', x=1.2, y=-.8, b=-.9, w=.4, eye='O', mark='SPLOSH'), k(.64, 'surf_m', x=.4, y=.4, b=.4, w=.8, eye='>'), k(.86, eye='^')],
        [(.46, 'leaptake')], g='use', act=('lift', 'flake'), pick='hungriest', when=['fish_hunger>.4'], prefer=['dawn', 'dusk'], obj=[(.25, dict(lure=1)), (.5, dict(lure=1)), (.75, dict(lure=0))],
        say=["Took it clean out of my bill. The splash was extra.", "It leapt. I flinched. Both of us pretend it did not happen."])
    o.r('tick_the_stone_for_supper', 'Ticking the left stone with his bill in short quick beats so the bass bunches in the shallows', 16, 'none',
        [k(.12, 'stone_l', x=1.1, y=1.3, b=.5, mark='tk'), k(.26, 'stone_l', x=1.2, y=1.4, b=.6, mark='tk'), k(.4, 'stone_l', x=1.1, y=1.3, b=.5, l=1, mark='tk'), k(.58, 'stone_l', x=1.3, y=1.5, b=.6, r=1, mark='TK'), k(.8, eye='^')],
        [(.58, 'call')], g='use', act=('ring', 'stone'), when=['pond_bell<.4'], prefer=['dawn', 'dusk'])
    o.r('hold_a_reed_hoop_over_the_water', 'Holding a reed bent into a hoop at arm\'s length above the water for the bass to leap clean through', 24, 'reed',
        [k(.12, 'surf_r', reach=.5, x=.3, y=-.2, b=.4), k(.3, 'surf_r', reach=1, x=.5, y=-.5, b=.8, w=.3), k(.5, 'surf_r', reach=1, x=.6, y=-.7, b=1, l=1, mark='SPLSH'), k(.7, 'surf_r', reach=1, x=.4, y=-.4, b=.7, r=1, mark='PLOP'), k(.9, eye='^')],
        [(.5, 'trick')], g='use', act=('lift', 'hoop'), pick='hungriest', when=['lunge<.8'], prefer=['curious', 'grown'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))],
        say=["Through the hoop. Nobody applauded. I applauded.", "Circus fish. I am the ringmaster. Good arrangement."])
    o.r('skitter_the_reed_tip_on_the_surface', 'Skittering a reed tip along the surface so it dimples like prey and the bass strikes at it', 20, 'reed',
        [k(.12, 'surf_l', reach=.5, x=.3, y=.3, b=.3), k(.3, 'cove', reach=1, x=.5, y=.5, b=.6, mark='tk tk'), k(.5, 'lane', reach=1, x=.6, y=.6, b=.8, mark='tk tk'), k(.7, 'surf_r', reach=1, x=.7, y=.6, b=.9, l=1, mark='STRK'), k(.88, eye='O')],
        [(.7, 'dimple')], g='use', act=('tap', 'surface'), pick='hungriest', prefer=['dawn', 'dusk', 'curious'], obj=[(.5, dict(lure=1)), (.75, dict(lure=1))])
    o.r('walk_a_wingtip_along_the_pad_edge', 'Walking a wingtip along the edge of the pads so the bass shadows it from the cover', 24, 'wing',
        [k(.1, 'cove', reach=.6, x=.2, y=.5, b=.3), k(.28, 'lane', reach=1, x=.3, y=.6, b=.4, l=1), k(.5, 'surf_r', reach=1, x=.4, y=.6, b=.4, r=1), k(.7, 'pad_low', reach=1, x=.4, y=.5, b=.4, l=1), k(.9, eye='^')],
        [(.5, 'lead')], g='use', act=('chase', 'wingtip'), pick='shyest', obj=[(.12, dict(lure=1)), (.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('feed_one_at_the_pad_corner', 'Offering a flake at the corner of the pad where the bass waits in the shadow, bill held very still', 22, 'none',
        [k(.12, x=.5, y=.5, b=.4), k(.3, 'surf_r', x=1.2, y=1.2, b=.9, eye='-'), k(.5, 'surf_r', x=1.3, y=1.4, b=1.1, eye='O', mark='snap'), k(.7, 'surf_r', x=.6, y=.7, b=.5, w=.4, eye='^'), k(.88, eye='-')],
        [(.5, 'feed')], g='use', act=('carry', 'flake'), pick='shyest', when=['fish_hunger>.4'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1)), (.8, dict(lure=0))])
    # ---------------- play
    o.r('race_the_bass_along_the_edge', 'Racing the bass along the front edge at full tilt, wings out, losing by two lengths', 20, 'none',
        [k(.1, 'surf_l', x=.5, y=.4, b=.4), k(.28, 'cove', x=1.1, y=.5, b=-.6, l=1, w=.6), k(.46, 'lane', x=1.4, y=.5, b=-.8, r=1, w=.8, mark='whoosh'), k(.64, 'surf_r', x=1.5, y=.5, b=-.6, l=1, w=.7), k(.84, 'bank_r', x=.3, y=.5, b=.5, eye='@')],
        [(.46, 'fun')], g='play', act=('race', 'edge'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=1))],
        say=["Lost by two lengths. Mine were shorter.", "Fish does not run. Fish still wins. Rigged."])
    o.r('toss_a_leaf_up_for_the_bass', 'Tossing a wet leaf up off the bill for the bass to rise and snap it out of the air', 20, 'none',
        [k(.12, 'surf_m', x=.8, y=1, b=.5), k(.3, 'surf_m', x=1.2, y=1.3, b=.8, mark='...'), k(.44, x=-.6, y=-1.2, b=-1, w=.6, eye='O', mark='fwup'), k(.6, 'lane', x=.5, y=.2, b=-.2, w=.3, mark='SNAP'), k(.82, eye='^')],
        [], g='play', act=('throw', 'leaf'), pick='hungriest', when=['pond_leaves>.2'], prefer=['happy', 'young'], obj=[(.28, dict(lure=1)), (.6, dict(lure=1))])
    o.r('splash_back_at_the_tail_slap', 'Splashing back at the bass with a wing every time it slaps its tail on the water', 18, 'wing',
        [k(.12, 'surf_m', reach=.5, x=.3, y=.3, b=.3), k(.3, 'surf_m', reach=1, x=.5, y=.4, b=-.4, mark='SLAP'), k(.48, 'surf_m', reach=1, x=.5, y=.4, b=-.5, l=1, mark='SPLSH'), k(.66, 'surf_m', reach=1, x=.5, y=.4, b=-.4, r=1, mark='SLAP'), k(.86, eye='@')],
        [], g='play', act=('splash', 'tail'), pick='hungriest', prefer=['young', 'happy'], obj=[(.28, dict(lure=1)), (.7, dict(lure=1))])
    o.r('hide_and_leap_from_the_pad', 'Ducking out of sight at the pad then popping up with a shout just as the bass comes by', 22, 'none',
        [k(.12, 'pad_low', x=.2, y=1.1, b=1.2), k(.3, 'pad_low', x=-.3, y=1.5, b=1.6, eye='-'), k(.5, 'pad_low', x=-.4, y=1.6, b=1.7, eye='o', mark='...'), k(.62, 'pad_low', x=.8, y=-.8, b=-1, w=1, eye='O', mark='BOO'), k(.84, x=.2, y=.2, eye='^')],
        [], g='play', act=('seek', 'bass'), pick='shyest', prefer=['young', 'curious'], obj=[(.5, dict(lure=1)), (.85, dict(lure=1))])
    o.r('hop_the_stones_beside_the_arc', 'Hopping from the left stone to the right in time with each arc the bass throws over the water', 22, 'none',
        [k(.1, 'stone_l', x=.4, y=.2, b=-.9, l=1), k(.3, 'stone_m', x=.5, y=.1, b=-1.2, r=1, w=.5, mark='hup'), k(.5, 'stone_m', x=.5, y=.1, b=-1.2, l=1, w=.7), k(.7, 'stone_r', x=.5, y=.1, b=-1.3, r=1, w=.8, mark='hup'), k(.88, 'stone_r', x=.2, y=.3, b=.4, eye='^')],
        [], g='play', act=('hop', 'arc'), pick='hungriest', prefer=['young', 'happy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('catch_the_spray_in_his_bill', 'Catching a leap\'s spray in his open bill, tongue out, and swallowing most of it', 16, 'none',
        [k(.12, 'surf_m', x=.5, y=.5, b=.4), k(.3, 'surf_m', x=.8, y=-.5, b=-.5, w=.4, eye='o'), k(.48, 'surf_m', x=1.1, y=-.9, b=-.8, w=.6, eye='O', mark='gulp'), k(.7, 'surf_m', x=.3, y=.3, b=.3, eye='>'), k(.88, eye='^')],
        [], g='play', act=('catch', 'spray'), pick='hungriest', prefer=['happy', 'ring>.3'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('spin_a_wake_with_both_wings', 'Spinning on the spot and stirring a wake with his wings so the bass circles the whirl', 20, 'wing',
        [k(.1, 'lane', reach=.6, x=.3, y=.4, b=.4), k(.28, 'lane', reach=1, x=.7, y=-.3, b=-.6, l=1, mark='swrl'), k(.48, 'lane', reach=1, x=-.6, y=-.4, b=-.6, r=1, mark='swrl'), k(.68, 'lane', reach=1, x=.6, y=-.3, b=-.5, l=1), k(.86, y=.5, b=.5, eye='@')],
        [], g='play', act=('spin', 'wake'), pick='shyest', prefer=['happy'], obj=[(.35, dict(lure=1)), (.7, dict(lure=1))])
    # ---------------- test
    o.r('measure_the_leap_on_a_stem', 'Measuring how high a leap clears by holding a reed against the left cattail stem', 24, 'reed',
        [k(.12, 'cattail_l', reach=.5, x=-.2, y=-.6, b=.3), k(.3, 'cattail_l', reach=1, x=-.3, y=-1, b=.6), k(.5, 'surf_l', reach=1, x=.3, y=.8, b=.8, mark='hm'), k(.7, 'cattail_l', reach=1, x=-.3, y=-1, b=.5, l=1), k(.9, eye='O', mark='four')],
        [], g='test', act=('measure', 'leap'), prefer=['curious'], ages=GROWN, say=["Four reeds high. Showy. I measured it twice, it did not blink.", "Height of a leap, taken with a plant. Science."])
    o.r('count_the_leaps_in_a_minute', 'Counting leaps by tapping a foot at the rim, one tap for each, until the bass stops', 22, 'none',
        [k(.12, 'stone_m', x=.3, y=.6, b=.3, l=1, mark='1'), k(.3, 'stone_m', x=.4, y=.4, b=-.3, r=1, mark='2'), k(.5, 'stone_m', x=.3, y=.5, b=-.4, l=1, mark='3'), k(.7, 'stone_m', x=.4, y=.4, b=-.3, r=1, mark='4'), k(.86, eye='-', mark='show-off')],
        [], g='test', act=('count', 'leaps'), pick='hungriest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))])
    o.r('peer_at_the_big_jaw_line', 'Peering along the big jaw line to see how far back the mouth runs past the eye', 18, 'none',
        [k(.12, x=.4, y=.8, b=.4), k(.3, 'surf_r', x=1, y=1.7, b=1, eye='o'), k(.5, 'surf_r', x=1.2, y=2, b=1.3, eye='@', mark='...'), k(.7, 'surf_r', x=.5, y=.9, b=.6, eye='-'), k(.88, eye='-')],
        [], g='test', act=('peer', 'jaw'), pick='shyest', prefer=['curious', 'young'], obj=[(.3, dict(lure=1)), (.65, dict(lure=1))])
    o.r('listen_for_the_slap_before_it_comes', 'Listening at the rim with his head cocked for the sound of a bass lining up its leap', 18, 'none',
        [k(.2, 'stone_r', x=.6, y=.6, b=.1), k(.4, 'stone_r', x=.6, y=1.1, b=.3, r=1), k(.62, 'stone_r', x=.7, y=1.2, b=.3, r=1, eye='-', mark='...'), k(.8, 'surf_r', x=1.5, y=-.8, b=-.6, w=.6, eye='O', mark='!')],
        [], g='test', act=('listen', 'slap'), prefer=['curious', 'dawn'])
    o.r('sniff_the_spray_for_insect', 'Sniffing a handful of spray for whatever the bass was after on the surface', 16, 'none',
        [k(.15, x=.4, y=.8, b=.4), k(.35, 'lane', x=1.2, y=1.7, b=.9, mark='snf'), k(.55, 'lane', x=1.1, y=1.9, b=1.1, eye='-', mark='snf'), k(.78, x=-.5, y=-.2, b=-.2, w=.4, eye='O'), k(.9, eye='-')],
        [], g='test', act=('sniff', 'spray'), prefer=['curious', 'young'])
    o.r('compare_the_spiny_back_with_the_record', 'Comparing the bass\'s spiny back fin with how tall a wild one stands, wing held beside it', 22, 'wing',
        [k(.12, 'surf_m', reach=.5, x=.3, y=.9, b=.4), k(.3, 'surf_m', reach=1, x=.4, y=1.2, b=.7), k(.5, 'cove', reach=1, x=.5, y=1.1, b=.7, r=1, mark='hm'), k(.7, 'surf_m', reach=.7, x=.3, y=.6, b=.5), k(.88, eye='-', mark='spikier')],
        [], g='test', act=('compare', 'spines'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))], say=['Spikier than me. Bigger chip on its shoulder too.', 'Held a wing to a fin. Mine is the softer argument.'])
    o.r('dip_a_toe_in_the_pad_shade', 'Dipping one toe at the edge of the pad shade to test how much colder the bass\'s cover is', 18, 'none',
        [k(.12, 'stone_r', x=.2, y=.5, b=.4), k(.3, 'pad_low', x=.4, y=.9, b=.9, l=1, eye='-'), k(.5, 'pad_low', x=.4, y=1.1, b=1.1, l=1, eye='>', mark='brr'), k(.72, 'stone_r', x=.2, y=.4, b=.4, eye='O'), k(.88, eye='-')],
        [], g='test', act=('test', 'shade'), prefer=['curious', 'warm'])
    # ---------------- rest
    o.r('nap_between_the_two_rises', 'Napping through the quiet noon at the middle stone, bill tucked, between the morning and evening rises', 28, 'none',
        [k(.12, 'stone_m', x=.2, y=.7, b=.8, eye='-'), k(.3, 'stone_m', x=-.4, y=1.3, b=1.6, eye='-', perch=1), k(.6, 'stone_m', x=-.6, y=1.7, b=2.1, eye='-', mark='zz', perch=1), k(.82, 'stone_m', x=-.2, y=.5, b=.5, eye='o'), k(.92, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'stone'), when=['tired', 'day'])
    o.r('sit_for_the_first_rise_at_dusk', 'Sitting at the right stone as the light goes, leaning forward for the dusk rises to begin', 24, 'none',
        [k(.14, 'stone_r', x=.7, y=.3, b=1.2), k(.34, 'stone_r', x=.9, y=.4, b=1.8, eye='o'), k(.58, 'stone_r', x=.9, y=.4, b=1.8, l=1, mark='...'), k(.78, 'surf_r', x=1.3, y=.5, b=.9, eye='O')],
        [(.58, 'rest')], g='rest', act=('sit', 'stone'), when=['dusk'], prefer=['tired', 'lonely'], say=['Sat. Waited. Nothing rose. Then everything did.', 'Dusk rises are punctual. Mine is the timing of a sulk.'])
    o.r('lean_to_the_cattail_and_sigh', 'Leaning his side to the left cattail stem and sighing at the flat calm water', 20, 'none',
        [k(.12, 'cattail_l', x=-.3, y=.3, b=.5), k(.3, 'cattail_l', x=-.6, y=.6, b=.9, eye='-'), k(.55, 'cattail_l', x=-.7, y=.8, b=1.1, eye='-', mark='sigh'), k(.78, x=.4, y=.4, b=.3, eye='O'), k(.9, eye='^')],
        [], g='rest', act=('lean', 'cattail'), when=['calm'], prefer=['tired', 'sad'])
    o.r('wait_for_the_first_ring_of_dawn', 'Waiting at the rim in the grey dawn, bill hovering, for the first ring to spread from a rise', 24, 'none',
        [k(.16, 'surf_m', x=1.4, y=.4, b=.2, eye='o'), k(.4, 'surf_m', x=1.5, y=.5, b=.2, r=1), k(.62, 'surf_m', x=1.5, y=.5, b=.2, eye='O', mark='...'), k(.84, 'surf_m', x=.9, y=.2, w=.3, eye='^')],
        [], g='rest', act=('wait', 'ring'), pick='shyest', when=['dawn'], prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sulk_with_his_back_to_the_calm', 'Sulking with his back to the flat water because no bass will so much as ripple it', 22, 'none',
        [k(.14, x=-.4, y=.2, b=.2), k(.3, 'surf_l', x=-1.1, y=.4, b=.5, l=1), k(.52, 'surf_l', x=-1.2, y=.5, b=.6, r=1, mark='hmph'), k(.76, 'surf_l', x=-.8, y=.2, b=.3, eye='-')],
        [], g='rest', act=('sulk', 'calm'), when=['sad'])
    # ---------------- weather
    o.r('crack_the_ice_along_the_lane', 'Cracking the ice along the lane with quick bill jabs so the bass has water to rise in', 22, 'none',
        [k(.12, 'surf_l', x=.3, y=.6, b=.2), k(.26, 'cove', x=1.6, y=.1, b=-.4, mark='ck'), k(.4, 'cove', x=1.7, y=.9, b=.6, l=1, mark='CRK'), k(.56, 'lane', x=1.6, y=.1, b=-.4, mark='ck'), k(.7, 'lane', x=1.7, y=.9, b=.6, r=1, mark='CRK'), k(.88, eye='^')],
        [(.4, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('flake_the_crust_off_the_rim', 'Flaking the frost crust off the left rim with the edge of a wing so the bass can strike there again', 18, 'wing',
        [k(.12, 'surf_l', reach=.5, x=.2, y=.7, b=.4), k(.3, 'surf_l', reach=1, x=.4, y=1.2, b=.8, mark='skrr'), k(.5, 'surf_l', reach=1, x=.5, y=1.3, b=1, r=1, mark='skrr'), k(.7, 'surf_l', reach=1, x=.3, y=1, b=.7), k(.88, eye='-')],
        [(.5, 'defrost')], g='weather', act=('scrape', 'crust'), when=['pond_ice>.3'])
    o.r('slap_the_heavy_water_awake', 'Slapping the heavy surface with the flat of both wings to churn air back in for the bass', 20, 'wing',
        [k(.1, 'surf_m', reach=.4, y=-.2, b=-.7, l=1, r=1), k(.28, 'lane', reach=1, x=.3, y=.8, b=1.1, mark='SPLSH'), k(.46, 'lane', reach=.4, y=-.3, b=-.8, r=1), k(.64, 'lane', reach=1, x=.4, y=.9, b=1.2, mark='SPLSH'), k(.82, 'surf_r', reach=1, x=.3, y=.4, b=.4, eye='@')],
        [(.64, 'stir')], g='weather', act=('splash', 'air'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('take_the_rain_at_the_stems', 'Taking the rain at the low reed with both wings pulled over his head while drops pock rings across the water', 30, 'none',
        [k(.15, 'reed_low', x=.2, y=.4, b=.4, w=.5), k(.34, 'reed_low', x=-.2, y=.9, b=.9, w=1, eye='-'), k(.6, 'reed_low', x=-.2, y=1, b=1, w=1, l=1, mark='drip'), k(.8, 'reed_low', x=.3, y=.4, b=.4, w=.4, eye='^')],
        [], g='weather', act=('shelter', 'stems'), when=['wet'])
    o.r('cool_both_feet_at_the_shaded_rim', 'Cooling both feet in turn at the shaded right stone while the bass lies deep out of the heat', 18, 'none',
        [k(.12, 'stone_r', x=.6, y=.2, b=1.3, l=1), k(.3, 'stone_r', x=.7, y=.3, b=1.6, l=1, r=1, eye='-', mark='ahh'), k(.6, 'stone_r', x=.6, y=.2, b=1.4, r=1, mark='...'), k(.8, x=.3, y=.3, b=.3, eye='^')],
        [], g='weather', act=('cool', 'feet'), when=['warm', 'sun'], prefer=['tired'])
    o.r('brace_against_the_chop', 'Bracing at the right bank against the gust that chops the water too rough for a clean leap', 18, 'none',
        [k(.12, 'bank_r', x=1.3, y=.2, b=.9, w=.2), k(.3, 'bank_r', x=1.5, y=.3, b=1.5, w=1, mark='whoo'), k(.52, 'bank_r', x=1.6, y=.4, b=1.7, w=1, r=1), k(.74, 'bank_r', x=1.2, y=.2, b=1, w=.5, l=1), k(.88, eye='-')],
        [], g='weather', act=('brace', 'chop'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_champion_leaper', 'Bowing deeply to the bass that cleared the reed, wings flung wide and the bill almost touching the water', 16, 'none',
        [k(.14, 'surf_m', x=-.3, y=-.2, b=-.2, w=.8), k(.32, 'surf_m', x=1.4, y=1.8, b=.9, w=1, eye='-'), k(.52, 'surf_m', x=1.5, y=2.4, b=1.4, w=.6, eye='-', mark='champ'), k(.72, 'surf_m', y=-.6, b=-.3, w=.3, eye='^')],
        [], g='show', act=('bow', 'leaper'), pick='hungriest', prefer=['happy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["Bowed to a fish. It leapt in thanks. Or panic.", "Respect, cleared with a reed to spare."])
    o.r('present_the_bass_to_the_pond', 'Presenting the bass to the pond with a long low sweep of the wing, announcing a record', 20, 'wing',
        [k(.1, 'lane', reach=.3, x=.5, y=-.4, b=-.5), k(.3, 'surf_m', reach=1, x=.5, y=-.6, b=-.6, l=1), k(.5, 'surf_m', reach=1, x=.6, y=-.8, b=-.7, r=1, mark='AND'), k(.7, 'surf_l', reach=1, x=.3, y=-.4, b=-.3), k(.88, eye='^')],
        [], g='show', act=('present', 'bass'), pick='shyest', prefer=['happy'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('argue_the_leap_height', 'Arguing with the bass about the height of that last leap, bill to bill, a wing jabbing the sky', 20, 'wing',
        [k(.12, 'surf_m', reach=.6, x=1.1, y=.3, b=.8), k(.3, 'surf_m', reach=1, x=1.4, y=.1, b=.4, mark='HIGHER'), k(.46, 'surf_m', reach=.3, x=.3, y=.1, b=.3), k(.62, 'surf_m', reach=1, x=1.5, y=.1, b=.4, l=1, mark='HIGHER'), k(.8, 'surf_m', reach=.5, x=.8, y=.3, b=.5), k(.9, eye='-')],
        [], g='show', act=('argue', 'height'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=["It claims five reeds. I saw four. Sworn statement.", "Fish and I disagree on air. Air takes no side."])
    o.r('pose_with_the_arc_behind_him', 'Striking a victory pose at the left stone as the bass hangs at the top of its arc', 18, 'none',
        [k(.12, 'stone_l', y=-.4, b=-.2, w=.9, perch=1), k(.3, 'stone_l', x=.3, y=-.9, b=-.5, w=1, l=1, perch=1), k(.5, 'stone_l', x=.4, y=-1, b=-.6, w=1, r=1, perch=1, eye='^', mark='ta-da'), k(.7, 'stone_l', x=.1, y=-.3, b=-.2, w=.6, perch=1), k(.86, 'stone_l', perch=1)],
        [], g='show', act=('pose', 'arc'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('shout_the_score_at_the_cattails', 'Shouting the leap score across to the right-hand cattails, one wing flung out', 18, 'wing',
        [k(.12, 'bank_r', reach=.5, x=.3, y=-.1, b=.3), k(.3, 'bank_r', reach=1, x=.6, y=-.5, b=-.4, w=0, mark='TEN'), k(.5, 'bank_r', reach=1, x=.7, y=-.6, b=-.5, mark='TEN!'), k(.72, 'bank_r', reach=.6, x=.3, y=0, b=.2), k(.88, eye='^')],
        [], g='show', act=('shout', 'cattails'), prefer=['happy', 'young'], say=["Ten. Out of ten. Fish wrote the score card.", "Told the reeds. Reeds did not clap, reeds never do."])
    # ---------------- mishap
    o.r('slip_on_the_splashed_stone', 'Slipping on the wet front stone the bass has splashed, one foot out, a quick flap to save it', 16, 'none',
        [k(.12, 'stone_m', x=.7, y=.9, b=.6), k(.28, 'stone_m', x=.4, y=-.2, b=-.9, r=1, w=.6, mark='whoa!'), k(.42, 'stone_m', x=1.5, y=1.4, b=1.6, w=1, eye='O'), k(.6, 'stone_m', x=.9, y=.4, b=.9, l=1, eye='>'), k(.8, eye='-')],
        [], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('caught_between_two_stems', 'Jamming his head between two reed stems after a bass, then hauling himself out with a pop', 24, 'none',
        [k(.1, x=.8, y=.6, b=.6), k(.28, 'reed_low', x=1.6, y=.5, b=.4, eye='O'), k(.48, 'reed_low', x=1.7, y=.6, b=.5, r=1, eye='@', mark='mmf'), k(.62, 'reed_low', x=1.4, y=.2, b=1.4, l=1, mark='mmff'), k(.76, 'reed_low', x=.6, y=-.4, b=-.6, w=1, mark='POP'), k(.9, x=1.2, y=1, b=.6, eye='-')],
        [], g='mishap', act=('stuck', 'stems'), prefer=['young', 'grumpy'])
    o.r('stride_at_the_bank_watching_the_rise', 'Striding at the right bank with his eye on the rings and meeting the cattail stem bill first', 20, 'none',
        [k(.1, 'surf_r', x=.3, y=.6, b=.3, l=1), k(.26, 'bank_r', x=.4, y=.5, b=.4, r=1), k(.42, 'bank_r', x=.5, y=.4, b=.5, l=1), k(.56, 'bank_r', x=1.7, y=-.1, b=1.6, eye='@', mark='BONK'), k(.72, 'bank_r', x=-1.1, y=.5, b=.2, w=.8, eye='x'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'bank'), prefer=['curious'])
    o.r('hop_back_from_the_soaking_splash', 'Hopping back from the rim when a leap lands in his face and soaks him from bill to belly', 16, 'none',
        [k(.12, 'surf_m', x=.8, y=1.2, b=.7), k(.28, 'surf_m', x=1, y=1.4, b=.9, eye='o', mark='...'), k(.42, x=-1.2, y=-.8, b=-1.4, l=1, r=1, w=1, eye='O', mark='SPLASH'), k(.6, x=-.6, y=.3, b=.2, eye='>'), k(.82, x=.2, y=.2, eye='-')],
        [], g='mishap', act=('hop', 'spray'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))], say=["Soaked. It did that on purpose and I respect it.", "A fish just got the last word and it was wet."])
    o.r('stamp_the_wet_prints_away', 'Stamping the wet prints off the stone in a sulk after the soaking, left foot and then right', 16, 'none',
        [k(.12, 'stone_l', x=.5, y=.5, b=.3), k(.24, 'stone_l', x=.4, y=-.2, b=-1.1, l=1, mark='STMP'), k(.36, 'stone_l', x=.5, y=.6, b=.5), k(.5, 'stone_l', x=.4, y=-.2, b=-1.1, r=1, mark='STMP'), k(.66, 'stone_l', x=.7, y=.6, b=.4, l=1, eye='>'), k(.84, eye='-')],
        [], g='mishap', act=('stamp', 'prints'), prefer=['grumpy'])
    # ---------------- duets
    o.r('hoop_and_flake_with_a_friend', 'Holding the reed hoop out while a friend dangles a flake through it so the bass has to leap the hoop to reach it', 26, 'reed',
        [k(.1, 'surf_l', reach=.5, x=.3, y=-.2, b=.4), k(.3, 'surf_l', reach=1, x=.5, y=-.5, b=.8), k(.5, 'surf_l', reach=1, x=.6, y=-.7, b=1, l=1, mark='SPLSH'), k(.7, 'surf_l', reach=1, x=.4, y=-.4, b=.7, r=1), k(.88, eye='^')],
        [(.5, 'leaptake')], g='use', act=('hook', 'hoop'), pick='hungriest', when=['fish_hunger>.4'], prefer=['happy'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))],
        duo=[k(.15, 'surf_r', x=.4, y=.2, b=.4), k(.34, 'surf_r', x=1, y=.3, b=.8, eye='o', mark='...'), k(.5, 'surf_r', x=1.2, y=-.7, b=-.8, w=.4, eye='O'), k(.72, 'surf_r', x=.5, y=.4, b=.4, eye='^')])
    o.r('swap_leap_counts_with_a_friend', 'Trading leap counts with a friend along the rim, each one tapping a different stone and arguing the total', 24, 'none',
        [k(.1, 'stone_l', x=.3, y=.5, b=.3, l=1, mark='1'), k(.3, 'stone_l', x=.4, y=.4, b=-.3, r=1, mark='2'), k(.5, 'stone_m', x=.4, y=.4, b=-.3, l=1, mark='5?'), k(.7, 'stone_l', x=.3, y=.5, b=.3, r=1, mark='4!'), k(.88, eye='^')],
        [], g='test', act=('count', 'rises'), pick='hungriest', prefer=['curious', 'happy'], obj=[(.35, dict(lure=1)), (.75, dict(lure=1))],
        duo=[k(.15, 'stone_r', x=.4, y=.5, b=.3, r=1), k(.35, 'stone_r', x=.5, y=.4, b=-.3, l=1, mark='3'), k(.55, 'stone_r', x=.4, y=.4, b=-.3, r=1, mark='6'), k(.78, 'stone_r', x=.3, y=.5, b=.3, eye='^')],
        say=["We counted twelve. Fish says four. It was there.", "Two ducks, one pond, no agreement. Fish abstains."])
    o.r('double_dare_the_pad_ambush', 'Splitting at the pad edge with a friend, one on each side, so the bass has nowhere to hide when it breaks cover', 24, 'wing',
        [k(.1, 'bloom_r', reach=.6, x=.3, y=.4, b=.5), k(.3, 'pad_low', reach=1, x=.5, y=.3, b=.7, eye='o'), k(.5, 'pad_low', reach=1, x=.6, y=.3, b=.9, l=1, eye='O', mark='NOW'), k(.7, 'surf_r', reach=1, x=.5, y=.7, b=.6, r=1, eye='>'), k(.88, eye='^')],
        [], g='play', act=('guard', 'cover'), pick='shyest', prefer=['young', 'happy'], obj=[(.55, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.15, 'surf_l', x=.4, y=.5, b=.4), k(.34, 'cove', x=.8, y=.6, b=.5, eye='o'), k(.55, 'lane', x=1.1, y=.8, b=.8, l=1, mark='GO'), k(.78, 'surf_r', x=.5, y=.5, b=.4, eye='^')])
    return done(o)


def carp():
    # Carp: heavy bottom dweller that roots in the mud, any hour, barbels, grazes algae off the stones. Own state: silt (the mud cloud it throws up,
    # drawn), root (how readily it roots where he points).
    o = Obj('carp', 'keeping', on='koi_pond',
            fields=dict(silt=(0, 0, 1), root=(0, 0, 1)),
            physics=[('silt', 'rate', .0005, 'day'), ('silt', 'rate', -.0008, 'night'), ('root', 'rate', -.0003, 'always')],
            effects=dict(scour=[('keeping.algae', 'mul', .5)], settle=[('silt', 'mul', .2), ('keeping.clarity', 'add', .15)],
                         skim=[('keeping.leaves', 'mul', .4)], thin=[('keeping.plants', 'mul', .75)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], sink=[('silt', 'add', .3), ('keeping.flakes', 'add', .4)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         lead=[('root', 'add', .2), ('subject.trust', 'add', .1)], tickle=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('silt', .3, '~=~=~', 'floor_m', 'mud'), ('pond_algae', .3, '"v"v"', 'stone_l', 'plant'), ('pond_leaves', .3, ';"~;', 'floor_r', 'leaf'), ('pond_ice', .3, '*-*-*', 'shelf', 'frost')],
            anchors=dict(floor_l=P(28, 43), floor_m=P(58, 41), floor_r=P(88, 39), mud_edge=P(48, 43), shelf=P(40, 39), pad_low=P(86, 37), reed_low=P(8, 38), tuft=P(11, 44),
                         bank_r=P(95, 40), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('scrub_the_green_film_off_the_stones', 'Scrubbing the green film off the left front stone with the flat of a wing, in slow heavy circles', 22, 'wing',
        [k(.16, 'stone_l', reach=.5, x=.4, y=.9, b=.6), k(.36, 'stone_l', reach=1, x=.7, y=1.5, b=1.3, l=1, mark='sqk'), k(.58, 'stone_l', reach=1, x=.9, y=1.7, b=1.5, r=1, mark='sqk'), k(.8, 'stone_l', reach=1, x=.6, y=1.2, b=1, mark='sqk'), k(.92, eye='^')],
        [(.58, 'scour')], g='care', act=('scrub', 'film'), when=['pond_algae>.3'], say=["Stone's bare. The carp will have to eat actual food.", "Scrubbed a rock for a fish that eats rocks. Circular."])
    o.r('sweep_the_silt_cloud_to_the_rim', 'Sweeping the brown silt cloud in towards the rim with long strokes of a wing so it settles', 20, 'wing',
        [k(.16, 'floor_m', reach=.5, x=.4, y=.7, b=.6), k(.34, 'floor_m', reach=1, x=.8, y=1.2, b=1.2, mark='shhh'), k(.54, 'mud_edge', reach=1, x=.9, y=1.4, b=1.3, l=1, mark='shhh'), k(.74, 'floor_l', reach=1, x=.8, y=1.2, b=1.1, r=1), k(.9, eye='-')],
        [(.54, 'settle')], g='care', act=('sweep', 'silt'), when=['silt>.3'], prefer=['curious'], say=['Swept the brown out. It will be back by teatime.', 'Silt in, silt out. Carp is unfazed. Carp is the reason.'])
    o.r('rake_the_leaf_litter_off_the_deep_corner', 'Raking the leaf litter off the water in the deep right corner with a reed, three slow pulls', 24, 'reed',
        [k(.16, 'floor_r', reach=.5, x=.3, y=.5, b=.4), k(.34, 'floor_r', reach=1, x=.7, y=.8, b=.8, mark='swsh'), k(.52, 'floor_m', reach=1, x=.8, y=.9, b=.9, mark='swsh'), k(.7, 'mud_edge', reach=1, x=.9, y=.9, b=1, l=1, mark='swsh'), k(.88, eye='^')],
        [(.52, 'skim')], g='care', act=('rake', 'litter'), when=['pond_leaves>.3'], prefer=['windy'], say=["Litter gone. The carp is already making more.", "Raked a pond. Pond stays unimpressed, for leaves are leaves."])
    o.r('dig_the_choking_weed_out_by_the_bank', 'Digging a clump of choking weed out of the shallows by the right bank with his bill, tugging it clear', 22, 'none',
        [k(.16, 'bank_r', x=.7, y=.6, b=.6), k(.36, 'bank_r', x=1.3, y=1.7, b=1.4, mark='nnk'), k(.56, 'bank_r', x=1.4, y=1.9, b=1.6, l=1, mark='TUG'), k(.76, 'bank_r', x=-.5, y=-.3, b=-.3, w=.6, mark='plop'), k(.9, eye='-')],
        [(.56, 'thin')], g='care', act=('dig', 'weeds'), when=['pond_plants>.7'])
    o.r('groom_the_coarse_scales', 'Grooming grit out of the big coarse scales along the carp\'s flank with a bill and a wing together', 24, 'wing',
        [k(.16, 'floor_l', reach=.5, x=.5, y=.9, b=.6), k(.34, 'floor_l', reach=1, x=.8, y=1.5, b=1.3, mark='rsp'), k(.54, 'shelf', reach=1, x=.9, y=1.5, b=1.4, l=1, mark='rsp'), k(.74, 'floor_l', reach=1, x=.7, y=1.3, b=1.1, r=1), k(.9, eye='^')],
        [(.54, 'tend')], g='care', act=('groom', 'scales'), pick='shyest', when=['fish_health<.9'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        say=["Gritty fish. Scrubbed and still gritty.", "Scales like roof tiles. Very pleasing, very much not mine."])
    o.r('pull_a_pad_back_off_the_mud_corner', 'Hooking the nearest lily pad back off the sunny mud corner with a twig so the carp can root in the warmth', 22, 'twig',
        [k(.16, 'pad_low', reach=.5, x=.3, y=.3, b=.3), k(.34, 'pad_low', reach=1, x=.6, y=.6, b=.6, mark='hnk'), k(.52, 'pad_low', reach=1, x=.8, y=.5, b=.9, l=1, r=1), k(.72, 'pad_low', reach=1, x=-.2, y=-.3, b=-.3, w=.4, mark='pop'), k(.88, eye='-')],
        [(.52, 'thin')], g='care', act=('pull', 'lily'), when=['pond_plants>.7'])
    # ---------------- use
    o.r('drop_a_handful_of_sinkers_at_the_mud_line', 'Dropping a wingful of sinking pellets just short of the mud line so the carp can find them by scent', 18, 'wing',
        [k(.18, 'mud_edge', reach=.5, x=.2, y=.2, w=.2), k(.4, 'mud_edge', reach=1, x=.1, y=.4, b=-.3, mark='plk plk'), k(.62, 'mud_edge', reach=1, x=0, y=.6, b=.3, mark='plk'), k(.84, eye='o')],
        [(.4, 'sink')], g='use', act=('throw', 'pellets'), when=['pond_flakes<.4'], prefer=['dusk', 'dawn'], say=["Sinkers down. Now the mud goes brown, the pond goes smug.", "Dinner is served. Cutlery at the bottom."])
    o.r('offer_a_pellet_at_the_mud_edge', 'Holding a pellet in his bill just at the mud edge until the hungriest carp sucks it out with its lips', 22, 'none',
        [k(.16, x=.5, y=.6, b=.6), k(.36, 'mud_edge', x=1.1, y=1.5, b=1.3, eye='o', mark='...'), k(.56, 'mud_edge', x=1.2, y=1.8, b=1.5, eye='O', mark='smack'), k(.76, 'mud_edge', x=.6, y=.8, b=.7, w=.4, eye='^'), k(.9, eye='-')],
        [(.56, 'feed')], g='use', act=('carry', 'pellet'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.35, dict(lure=1)), (.65, dict(lure=1)), (.8, dict(lure=0))],
        say=["Lips like a vacuum. Nearly had my bill.", "Fed a carp by hand. It sucked and judged."])
    o.r('rap_twice_on_the_right_stone', 'Rapping twice on the right stone with his bill, a pause, and twice again so the carp links stone with supper', 20, 'none',
        [k(.16, 'stone_r', x=1.3, y=1.6, b=.8, mark='tok tok'), k(.34, 'stone_r', x=1.2, y=1.4, b=.7, mark='tok tok'), k(.5, x=.2, y=.3, b=.2, w=.3), k(.68, 'stone_r', x=1.4, y=1.7, b=.9, r=1, mark='TOK TOK'), k(.86, eye='^')],
        [(.68, 'call')], g='use', act=('ring', 'stones'), when=['pond_bell<.4'], prefer=['dusk'])
    o.r('trail_a_wing_along_the_mud_edge', 'Trailing a wing along the mud edge and the carp following it, nosing the bottom the whole way', 26, 'wing',
        [k(.14, 'floor_l', reach=.6, x=.3, y=.9, b=.6), k(.32, 'mud_edge', reach=1, x=.5, y=1, b=.8, l=1), k(.52, 'floor_m', reach=1, x=.6, y=1, b=.8, r=1), k(.72, 'floor_r', reach=1, x=.6, y=1, b=.8, l=1), k(.9, eye='^')],
        [(.52, 'lead')], g='use', act=('drag', 'wing'), pick='hungriest', when=['root<.7'], obj=[(.16, dict(lure=1)), (.34, dict(lure=1)), (.54, dict(lure=1)), (.76, dict(lure=1))],
        say=["Followed my wing like a dog. A very big, very wet dog.", "It nosed the bottom the whole way. Efficient, if brown."])
    o.r('tickle_the_barbels_with_a_reed', 'Tickling the carp\'s twin barbels with the very end of a reed while it holds still at the rim', 20, 'reed',
        [k(.16, 'floor_l', reach=.5, x=.3, y=.6, b=.5), k(.36, 'floor_l', reach=1, x=.5, y=1.1, b=1, mark='tck'), k(.56, 'floor_l', reach=1, x=.5, y=1.3, b=1.2, l=1, r=1, mark='tck tck'), k(.76, 'floor_l', reach=1, x=.4, y=1, b=.9), k(.9, eye='^')],
        [(.56, 'tickle')], g='use', act=('prod', 'barbels'), pick='shyest', obj=[(.3, dict(lure=1)), (.7, dict(lure=1))])
    o.r('show_the_shy_one_a_flake', 'Showing the shy carp a flake over the far pad edge and letting it come for it, bill unmoving', 22, 'none',
        [k(.16, x=.4, y=.5, b=.5), k(.36, 'floor_r', x=1, y=1.3, b=1.2, eye='-'), k(.56, 'floor_r', x=1.1, y=1.5, b=1.4, eye='O', mark='gulp'), k(.76, 'floor_r', x=.6, y=.7, b=.7, w=.5, eye='^'), k(.9, eye='-')],
        [(.56, 'feed')], g='use', act=('show', 'flake'), pick='shyest', when=['fish_hunger>.4'], obj=[(.35, dict(lure=1)), (.65, dict(lure=1)), (.8, dict(lure=0))])
    # ---------------- play
    o.r('waltz_the_bank_beside_the_carp', 'Waltzing slowly along the bank in time with the carp\'s heavy swim, three steps and a turn', 24, 'none',
        [k(.14, 'stone_l', x=.3, y=.3, b=.6, l=1), k(.32, 'stone_m', x=.5, y=.3, b=-.4, r=1, w=.6), k(.5, 'stone_m', x=.4, y=.3, b=.6, l=1, w=.8, mark='la'), k(.68, 'stone_r', x=.5, y=.3, b=-.4, r=1, w=.6), k(.86, 'stone_r', x=.2, y=.3, b=.4, eye='^')],
        [(.5, 'fun')], g='play', act=('dance', 'bank'), pick='hungriest', prefer=['happy'], obj=[(.18, dict(lure=1)), (.4, dict(lure=1)), (.62, dict(lure=1)), (.8, dict(lure=1))])
    o.r('blow_bubbles_back_at_the_carp', 'Blowing bubbles back at the carp every time it burps one up at the rim, trading them like ping pong', 20, 'none',
        [k(.14, x=.3, y=.7, b=.5), k(.32, 'floor_m', x=1.3, y=2, b=1.2, eye='-', mark='blp'), k(.5, 'floor_m', x=1.4, y=2.1, b=1.4, eye='O', mark='blp blp'), k(.68, 'floor_m', x=.9, y=1.2, b=.8, eye='>', mark='bloop'), k(.86, eye='^')],
        [], g='play', act=('blow', 'bubbles'), pick='hungriest', prefer=['happy', 'young'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))], say=["It won on volume. I won on spit.", "Bubble rally. No clear winner. Fish is warm."])
    o.r('push_a_leaf_along_its_rooting_track', 'Pushing a floating leaf along the carp\'s rooting track with a reed, the carp bumping it back', 24, 'reed',
        [k(.14, 'floor_l', reach=.5, x=.3, y=.4, b=.4), k(.32, 'mud_edge', reach=1, x=.6, y=.7, b=.7, mark='swsh'), k(.5, 'floor_m', reach=1, x=.7, y=.8, b=.9, l=1, mark='bmp'), k(.68, 'floor_r', reach=1, x=.7, y=.8, b=.9, r=1, mark='swsh'), k(.86, eye='o')],
        [], g='play', act=('float', 'leaf'), pick='shyest', when=['pond_leaves>.2'], prefer=['young', 'curious'], obj=[(.52, dict(lure=1)), (.75, dict(lure=1))])
    o.r('hide_a_toe_for_the_carp_to_find', 'Wiggling a toe over the edge of the stone and hiding it again when the carp noses near', 20, 'none',
        [k(.14, 'stone_m', x=.2, y=.4, b=.7, l=1), k(.3, 'stone_m', x=.4, y=.8, b=1, l=1, mark='wgl'), k(.46, 'stone_m', x=.5, y=1, b=1.2, l=1, eye='o'), k(.58, 'stone_m', x=-.3, y=.3, b=.4, w=.5, eye='O', mark='!'), k(.78, 'stone_m', x=.4, y=.8, b=1, l=1, mark='wgl'), k(.9, eye='^')],
        [], g='play', act=('hide', 'toe'), pick='hungriest', prefer=['young', 'happy'], obj=[(.36, dict(lure=1)), (.7, dict(lure=1))])
    o.r('balance_a_pellet_on_his_bill_for_it', 'Balancing a pellet on his bill and dipping slowly to the water, the carp rising in time with the dip', 22, 'none',
        [k(.14, x=.6, y=-.5, b=.2), k(.32, 'floor_l', x=.8, y=-.2, b=.6, mark='...'), k(.5, 'floor_l', x=1.2, y=.8, b=1.1), k(.64, 'floor_l', x=1.3, y=1.4, b=1.3, eye='O', mark='gulp'), k(.84, x=.5, y=-.3, b=.2, eye='^')],
        [], g='play', act=('balance', 'pellet'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.34, dict(lure=1)), (.66, dict(lure=1))])
    o.r('chase_the_plume_it_stirs_up', 'Chasing the brown plume the carp stirs up along the mud edge, snapping at the swirls', 18, 'none',
        [k(.14, 'floor_l', x=.9, y=.8, b=.4, l=1), k(.3, 'mud_edge', x=1.1, y=.9, b=.5, r=1, mark='snp'), k(.48, 'floor_m', x=1.2, y=.9, b=.5, l=1, mark='snp'), k(.66, 'floor_r', x=1.2, y=.9, b=.5, r=1), k(.84, y=.4, eye='@')],
        [], g='play', act=('chase', 'plume'), prefer=['young', 'happy'], when=['silt>.3'])
    # ---------------- test
    o.r('count_the_plate_scales', 'Counting the plate scales down the carp\'s flank, a tap of the bill for each one', 22, 'none',
        [k(.14, 'floor_l', x=.9, y=1.3, b=.8, mark='1'), k(.3, 'floor_l', x=1, y=1.5, b=.9, mark='2'), k(.46, 'shelf', x=1, y=1.5, b=.9, l=1, mark='3'), k(.62, 'shelf', x=1.1, y=1.7, b=1, r=1, mark='4'), k(.8, eye='-', mark='armour')],
        [], g='test', act=('count', 'scales'), pick='hungriest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.65, dict(lure=1))])
    o.r('sniff_the_fresh_mud_line', 'Sniffing the fresh mud line it has just turned over and sneezing a blob of it away', 16, 'none',
        [k(.16, x=.5, y=1, b=.6), k(.36, 'mud_edge', x=1.5, y=1.9, b=1.2, mark='snf'), k(.54, 'mud_edge', x=1.4, y=2.1, b=1.4, eye='-'), k(.72, x=-.9, y=-.5, b=-.4, w=.8, eye='>', mark='ACHOO'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'mud'), prefer=['curious', 'young'], when=['silt>.3'])
    o.r('taste_the_silt_off_a_wingtip', 'Tasting the silt off a wingtip to find out what a carp finds delicious in it', 18, 'wing',
        [k(.16, 'mud_edge', reach=.5, x=.3, y=.8, b=.5), k(.34, 'mud_edge', reach=1, x=.5, y=1.2, b=.9), k(.52, x=1.4, y=.5, b=.4, mark='...'), k(.7, x=-1, y=-.6, b=-.3, w=.6, eye='>', mark='bleh'), k(.88, eye='-')],
        [], g='test', act=('taste', 'silt'), prefer=['curious', 'young'])
    o.r('listen_for_the_gulp_at_the_surface', 'Listening for the carp\'s greedy gulp at the surface, ear low over the water, bill pointed away', 20, 'none',
        [k(.16, 'floor_m', x=-.4, y=1.2, b=.9), k(.36, 'floor_m', x=-.5, y=1.5, b=1.2, eye='-'), k(.54, 'floor_m', x=-.5, y=1.5, b=1.2, r=1, mark='...'), k(.7, 'floor_m', x=.8, y=.5, b=.5, eye='O', mark='gulp!'), k(.88, eye='^')],
        [], g='test', act=('listen', 'gulp'), prefer=['curious', 'lonely'])
    o.r('test_the_mud_with_a_toe', 'Testing the soft mud at the bank edge with one toe, sinking an inch and pulling it out with a sound', 18, 'none',
        [k(.16, 'bank_r', x=.3, y=.5, b=.6), k(.34, 'bank_r', x=.3, y=.9, b=1.3, l=1, eye='>'), k(.5, 'bank_r', x=.3, y=1, b=1.5, l=1, mark='squelch'), k(.7, 'bank_r', x=-.5, y=-.2, b=-.5, l=1, w=.6, mark='SHLUP'), k(.88, eye='-')],
        [], g='test', act=('test', 'mud'), prefer=['curious', 'young'], say=['Mud. Toe. Sound. Good enough as a review.', 'It took my foot an inch. Mud keeps what it likes.'])
    o.r('compare_the_length_with_the_wild_record', 'Stretching a reed along the carp\'s back and comparing it with how long a wild one has been caught', 24, 'reed',
        [k(.16, 'floor_l', reach=.5, x=.3, y=.6, b=.5), k(.34, 'floor_l', reach=1, x=.5, y=.9, b=.8), k(.54, 'floor_r', reach=1, x=.7, y=.8, b=.7, l=1, mark='hm'), k(.74, 'floor_m', reach=.7, x=.2, y=.4, b=.4), k(.9, eye='O', mark='huge')],
        [], g='test', act=('compare', 'length'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.34, dict(lure=1)), (.6, dict(lure=1))])
    o.r('measure_the_rooting_trench', 'Pacing the length of the trench it has rooted along the bottom with a reed held at the water line', 22, 'reed',
        [k(.16, 'floor_l', reach=.5, x=.3, y=.4, b=.4), k(.34, 'mud_edge', reach=1, x=.5, y=.6, b=.6, l=1), k(.54, 'floor_m', reach=1, x=.7, y=.7, b=.8, r=1, mark='1'), k(.74, 'floor_r', reach=1, x=.8, y=.7, b=.8, l=1, mark='2'), k(.9, eye='-', mark='long')],
        [], g='test', act=('measure', 'trench'), prefer=['curious'], when=['silt>.3'])
    # ---------------- rest
    o.r('nap_in_the_tuft_beside_the_carp', 'Dozing off at the grass tuft with one foot over the edge while the carp roots away happily', 28, 'none',
        [k(.16, 'tuft', x=.1, y=.9, b=1, eye='-'), k(.36, 'tuft', x=-.5, y=1.5, b=1.9, l=1, eye='-', mark='zz'), k(.6, 'tuft', x=-.7, y=1.9, b=2.4, eye='-', mark='zzz'), k(.8, 'tuft', x=-.2, y=.6, b=.7, eye='o'), k(.92, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'tuft'), when=['tired'])
    o.r('sit_by_the_stone_and_let_it_root', 'Sitting by the left stone with his feet tucked, watching the carp work the bottom for an hour', 24, 'none',
        [k(.16, 'stone_l', x=.8, y=.1, b=1.4), k(.36, 'stone_l', x=1, y=.2, b=2, l=1, eye='o'), k(.6, 'stone_l', x=1, y=.2, b=2, r=1, eye='-', mark='...'), k(.8, 'floor_l', x=1.3, y=.6, b=1, eye='O')],
        [(.6, 'rest')], g='rest', act=('sit', 'stone'), prefer=['tired', 'lonely'])
    o.r('lean_on_the_reed_and_watch_the_mud', 'Leaning his shoulder to the low reed and watching the carp throw up clouds, one eye half shut', 20, 'none',
        [k(.16, 'reed_low', x=-.5, y=.2, b=.9), k(.36, 'reed_low', x=-.9, y=.4, b=1.3, eye='-'), k(.58, 'reed_low', x=-1, y=.4, b=1.4, l=1, eye='-', mark='...'), k(.8, x=.5, y=.5, b=.3, eye='O'), k(.9, eye='^')],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'sad'])
    o.r('wait_for_the_first_bubble_line', 'Waiting at the rim for the first string of bubbles that says the carp is awake and working', 22, 'none',
        [k(.16, 'floor_m', x=.5, y=1.5, b=1.4, eye='o'), k(.4, 'floor_m', x=.6, y=1.7, b=1.6, eye='o'), k(.62, 'floor_m', x=.6, y=1.7, b=1.6, l=1, eye='O', mark='...'), k(.82, 'floor_m', x=.2, y=.9, b=.7, eye='^')],
        [], g='rest', act=('wait', 'bubbles'), pick='shyest', prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sulk_at_the_clouded_water', 'Sulking at the clouded water, one wing over his bill, because the carp stirred it up on purpose', 22, 'none',
        [k(.16, x=-.5, y=.4, b=.5, w=.4), k(.34, 'floor_r', x=-1.2, y=.9, b=.9, w=.8, eye='-'), k(.54, 'floor_r', x=-1.3, y=1, b=1, w=.9, eye='-', mark='hmph'), k(.76, x=-.6, y=.4, b=.4, w=.3, eye='-')],
        [], g='rest', act=('sulk', 'cloud'), when=['sad'])
    # ---------------- weather
    o.r('hack_the_ice_off_the_mud_corner', 'Hacking the ice off the mud corner with heavy bill stabs so the carp can still breathe and root', 22, 'none',
        [k(.14, 'shelf', x=.8, y=1.1, b=.7), k(.28, 'shelf', x=1.4, y=1.9, b=1.4, l=1, mark='CHK'), k(.42, 'shelf', x=1.5, y=1.6, b=.9, mark='ck'), k(.58, 'shelf', x=1.4, y=1.9, b=1.4, r=1, mark='CHK'), k(.72, 'mud_edge', x=1.3, y=1.7, b=1.2, mark='ck'), k(.88, eye='^')],
        [(.58, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('rub_the_rime_off_the_left_edge', 'Rubbing the rime off the shelf edge with the side of a wing so the sunk pellets are not iced over', 18, 'wing',
        [k(.14, 'shelf', reach=.4, x=.3, y=1, b=.6), k(.32, 'shelf', reach=1, x=.5, y=1.5, b=1.2, mark='skrr'), k(.5, 'shelf', reach=1, x=.6, y=1.6, b=1.3, l=1, mark='skrr'), k(.68, 'mud_edge', reach=1, x=.5, y=1.4, b=1.1), k(.86, eye='-')],
        [(.5, 'thaw')], g='weather', act=('scrape', 'rime'), when=['pond_ice>.3'])
    o.r('thrash_the_air_back_into_the_pond', 'Thrashing both wings over the still, warm water to put air back for the sluggish carp', 20, 'wing',
        [k(.14, 'floor_m', reach=.4, x=.2, y=.3, b=-.5), k(.3, 'floor_m', reach=1, x=.3, y=.8, b=.9, l=1, mark='SPLSH'), k(.46, 'floor_m', reach=.4, x=.1, y=.2, b=-.6, r=1), k(.62, 'mud_edge', reach=1, x=.3, y=.9, b=1, mark='SPLSH'), k(.78, 'floor_r', reach=1, x=.3, y=.9, b=1, l=1, mark='SPLSH'), k(.9, eye='@')],
        [(.62, 'stir')], g='weather', act=('splash', 'air'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('crouch_out_the_rain_at_the_tuft', 'Crouching out the rain at the grass tuft, wings shut tight, rain dripping off his bill', 30, 'none',
        [k(.16, 'tuft', x=.1, y=.5, b=.8), k(.36, 'tuft', x=-.3, y=1.1, b=1.6, eye='-'), k(.62, 'tuft', x=-.4, y=1.3, b=1.8, r=1, eye='-', mark='drip'), k(.84, 'tuft', x=.3, y=.5, b=.5, eye='^')],
        [], g='weather', act=('shelter', 'tuft'), when=['wet'])
    o.r('bask_the_belly_on_the_sun_stone', 'Basking at the middle stone with his belly to the sun and both wings out while the carp warms the shallows', 22, 'none',
        [k(.16, 'stone_m', x=.1, y=.6, b=1, w=.6, perch=1), k(.36, 'stone_m', x=.1, y=.8, b=1.5, w=1, eye='-', perch=1), k(.62, 'stone_m', x=.1, y=.8, b=1.6, w=1, eye='-', mark='ahh', perch=1), k(.82, 'stone_m', x=.2, y=.4, b=.5, w=.3, perch=1, eye='^')],
        [], g='weather', act=('warm', 'belly'), when=['sun'], prefer=['tired'])
    o.r('plant_his_feet_against_the_gale', 'Planting both feet and leaning into the gale at the bank while the carp roots on in the lee', 18, 'none',
        [k(.14, 'bank_r', x=.9, y=.4, b=1.1, l=1), k(.32, 'bank_r', x=1.5, y=.5, b=1.7, w=.5, r=1, mark='whoo'), k(.52, 'bank_r', x=1.6, y=.6, b=1.9, w=.9), k(.72, 'bank_r', x=1.3, y=.4, b=1.2, w=.4, l=1), k(.88, eye='-')],
        [], g='weather', act=('brace', 'gale'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_old_carp', 'Bowing slowly to the old carp, who has seen more ducks than he has had breakfasts', 18, 'none',
        [k(.16, 'floor_m', x=.1, y=.5, b=.4, w=.4), k(.36, 'floor_m', x=.9, y=1.4, b=1.1, w=.8, eye='-'), k(.56, 'floor_m', x=1, y=2, b=1.6, w=.4, eye='-', mark='elder'), k(.78, 'floor_m', x=.2, y=-.2, b=-.1, w=.2, eye='^')],
        [], g='show', act=('bow', 'carp'), pick='hungriest', prefer=['happy'], obj=[(.34, dict(lure=1)), (.72, dict(lure=1))], say=["It nodded back, probably. Gills move like that.", "Bowed to a carp older than my pond. Seemed fair."])
    o.r('present_the_carp_to_the_cattails', 'Presenting the carp to the cattails with a slow sweep of the wing, as though they might buy it', 22, 'wing',
        [k(.14, 'floor_l', reach=.3, x=.2, y=-.1, b=.3), k(.34, 'floor_l', reach=1, x=.3, y=-.4, b=-.2, l=1), k(.54, 'reed_low', reach=1, x=.3, y=-.5, b=-.3, r=1, mark='behold'), k(.74, 'floor_l', reach=1, x=.2, y=-.3, b=-.1), k(.9, eye='^')],
        [], g='show', act=('present', 'carp'), pick='shyest', prefer=['happy'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))])
    o.r('argue_with_it_about_the_mud', 'Arguing with the carp nose to nose over who owns the mud, a wing stabbing at the floor', 22, 'wing',
        [k(.14, 'floor_m', reach=.5, x=.9, y=.7, b=.7), k(.3, 'floor_m', reach=1, x=1.2, y=1, b=1, mark='MINE'), k(.44, 'floor_m', reach=.3, x=.4, y=.5, b=.4), k(.6, 'floor_m', reach=1, x=1.3, y=1.1, b=1.1, r=1, mark='MINE'), k(.78, 'floor_m', reach=.5, x=.7, y=.7, b=.7), k(.9, eye='-')],
        [], g='show', act=('argue', 'mud'), pick='hungriest', prefer=['grumpy'], obj=[(.3, dict(lure=1)), (.65, dict(lure=1))], say=["Carp says it is its mud. Carp has priors.", "Lost to a fish with a vacuum for a face."])
    o.r('pose_like_a_carp_on_the_stone', 'Posing at the left stone with lips pouted and his wings drooped like a carp\'s fins, deadly serious', 18, 'none',
        [k(.16, 'stone_l', x=.5, y=.4, b=.4, w=.3, perch=1), k(.34, 'stone_l', x=.9, y=.8, b=.8, w=.6, perch=1, eye='O', mark='pout'), k(.56, 'stone_l', x=1, y=.9, b=.9, w=.6, l=1, perch=1, eye='O', mark='pout'), k(.78, 'stone_l', x=.4, y=.3, b=.3, w=.3, perch=1, eye='^')],
        [], g='show', act=('pose', 'lips'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.75, dict(lure=1))])
    o.r('show_off_the_big_one_to_nobody', 'Showing the carp to a crowd of cattails, one wing out, the whole bank his gallery', 22, 'wing',
        [k(.14, 'floor_r', reach=.4, x=.3, y=.1, b=.3), k(.34, 'floor_r', reach=1, x=.6, y=-.3, b=-.3, mark='LOOK'), k(.54, 'floor_r', reach=1, x=.7, y=-.4, b=-.4, r=1, mark='LOOK'), k(.74, 'floor_r', reach=.6, x=.3, y=0, b=.2), k(.88, eye='^')],
        [], g='show', act=('show', 'carp'), pick='hungriest', prefer=['happy', 'young'], obj=[(.4, dict(lure=1)), (.72, dict(lure=1))])
    # ---------------- mishap
    o.r('slip_in_the_mud_at_the_bank', 'Slipping in the mud churned up at the bank, both feet shooting forward, ending sat in a heap', 18, 'none',
        [k(.14, 'bank_r', x=.8, y=.6, b=.5), k(.3, 'bank_r', x=1.2, y=-.1, b=-.8, l=1, r=1, w=.8, mark='whoa'), k(.46, 'bank_r', x=.3, y=1.4, b=2, w=1, eye='O', mark='SPLAT'), k(.66, 'bank_r', x=-.2, y=1.1, b=1.6, eye='>'), k(.84, x=.2, y=.4, b=.5, eye='-')],
        [], g='mishap', act=('slip', 'mud'), when=['wet'], prefer=['young'])
    o.r('bill_stuck_in_the_mud_line', 'Burying his bill to the eyes in the soft bank mud after a pellet and pulling free with a loud pop', 24, 'none',
        [k(.14, 'mud_edge', x=1, y=1, b=.8), k(.32, 'mud_edge', x=1.8, y=2.2, b=1.5, eye='O'), k(.5, 'mud_edge', x=1.9, y=2.3, b=1.6, l=1, eye='@', mark='mmph'), k(.68, 'mud_edge', x=1.7, y=1.8, b=1.3, r=1, mark='mmmph'), k(.8, x=-1, y=-.6, b=-1, w=1, mark='POP'), k(.92, y=.8, eye='-')],
        [], g='mishap', act=('stuck', 'bill'), prefer=['young', 'grumpy'])
    o.r('walk_the_bank_into_a_reed', 'Walking the bank with his head turned to the water and meeting the low reed bill first', 18, 'none',
        [k(.14, 'stone_l', x=.2, y=.7, b=.3, r=1), k(.3, 'tuft', x=.4, y=.9, b=.4, l=1), k(.46, 'reed_low', x=1.8, y=.2, b=1.5, eye='@', mark='BONK'), k(.64, 'reed_low', x=-1, y=.3, b=.1, w=.9, eye='x'), k(.84, x=.2, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'reed'), prefer=['curious'])
    o.r('startle_back_at_the_gulp', 'Hopping back with a yelp when the carp gulps at the surface just under his bill', 16, 'none',
        [k(.14, 'floor_l', x=.9, y=1.5, b=1), k(.28, 'floor_l', x=1, y=1.7, b=1.2, eye='o', mark='...'), k(.4, x=-1.4, y=-1, b=-1.6, l=1, r=1, w=1, eye='O', mark='GLUP'), k(.58, x=-.8, y=.2, b=-.2, eye='>'), k(.8, x=.1, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'gulp'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))], say=["It gulped at my face. Rude, but also fair.", "Big mouth, no warning. Like a politician, scaly."])
    o.r('stamp_on_the_silt_in_a_sulk', 'Stamping the silt-brown stone flat after a clumsy toss, left foot and then right', 16, 'none',
        [k(.14, 'stone_m', x=.7, y=.9, b=.4), k(.26, 'stone_m', x=.5, y=-.1, b=-1.2, l=1, mark='STMP'), k(.38, 'stone_m', x=.6, y=.7, b=.6), k(.52, 'stone_m', x=.5, y=-.1, b=-1.2, r=1, mark='STMP'), k(.7, 'stone_m', x=.8, y=.5, b=.3, eye='>'), k(.86, eye='-')],
        [(.52, 'settle')], g='mishap', act=('stamp', 'silt'), when=['silt>.5'], prefer=['grumpy'])
    # ---------------- duets
    o.r('two_sets_of_sinkers_from_both_ends', 'Dropping sinkers at the left end of the bank while a friend drops theirs at the right, the carp torn between them', 24, 'wing',
        [k(.14, 'floor_l', reach=.5, x=.1, y=.2, w=.2), k(.36, 'floor_l', reach=1, x=0, y=.3, b=-.4, mark='plk'), k(.56, 'floor_l', reach=1, x=0, y=.6, b=.4, mark='plk plk'), k(.78, eye='o')],
        [(.36, 'sink')], g='use', act=('pour', 'pellets'), pick='hungriest', when=['pond_flakes<.4'], prefer=['happy'], obj=[(.5, dict(lure=1)), (.78, dict(lure=1))],
        duo=[k(.18, 'floor_r', x=.2, y=.3, b=.4), k(.4, 'floor_r', x=.8, y=.9, b=.9, mark='plk'), k(.6, 'floor_r', x=.9, y=1.1, b=1, l=1, mark='plk plk'), k(.8, 'floor_r', x=.3, y=.4, b=.3, eye='^')],
        say=["Two dinners at once. It chose the wetter one.", "Equal pellets both ends. The carp invented a third end."])
    o.r('haul_the_weed_with_a_friend', 'Hauling a long tangle of weed out of the shallows with a friend, both bills clamped, heave and heave', 26, 'none',
        [k(.14, 'mud_edge', x=.6, y=.7, b=.7), k(.32, 'mud_edge', x=1.2, y=1.5, b=1.4, mark='hff'), k(.5, 'mud_edge', x=1.3, y=1.7, b=1.7, l=1, mark='HEAVE'), k(.68, 'mud_edge', x=-.4, y=-.2, b=-.5, w=.8, mark='plop'), k(.86, eye='^')],
        [(.5, 'thin')], g='care', act=('tug', 'tangle'), when=['pond_plants>.7'], prefer=['happy'],
        duo=[k(.16, 'floor_l', x=.6, y=.7, b=.7), k(.34, 'floor_l', x=1.2, y=1.5, b=1.4), k(.52, 'floor_l', x=1.3, y=1.7, b=1.7, r=1, mark='HEAVE'), k(.72, 'floor_l', x=-.3, y=-.2, b=-.5, w=.8, eye='^')])
    o.r('mud_wave_with_a_friend_in_time', 'Rolling a wave of footfalls down the stones with a friend in time, the carp swimming along to the beat', 24, 'none',
        [k(.14, 'stone_l', x=.3, y=.3, b=-.5, l=1), k(.32, 'stone_m', x=.4, y=.3, b=-.7, r=1), k(.5, 'stone_r', x=.4, y=.3, b=-.5, l=1, mark='tum'), k(.68, 'stone_m', x=.4, y=.3, b=-.7, r=1), k(.86, 'stone_l', x=.3, y=.3, b=-.4, l=1, eye='^')],
        [], g='play', act=('drum', 'bank'), pick='hungriest', prefer=['happy', 'young'], obj=[(.32, dict(lure=1)), (.58, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.18, 'stone_r', x=.3, y=.3, b=-.5, r=1), k(.4, 'stone_m', x=.4, y=.3, b=-.7, l=1), k(.6, 'stone_l', x=.4, y=.3, b=-.5, r=1, mark='tum'), k(.82, 'stone_m', x=.3, y=.3, b=-.4, eye='^')])
    return done(o)


def ghost_fish():
    # Ghost fish: pale, shy, mid-water, active at night, glows after dark. Own state: glow (how brightly it shines: builds after dark, fades by day, drawn),
    # trace (a glimmering line left on the water where a wingtip drew it, drawn), hush (how settled it is with him: stillness raises it).
    o = Obj('ghost_fish', 'keeping', on='koi_pond',
            fields=dict(glow=(0, 0, 1), trace=(0, 0, 1), hush=(0, 0, 1)),
            physics=[('glow', 'rate', .003, 'night'), ('glow', 'rate', -.004, '!night'), ('trace', 'rate', -.003, 'always'), ('hush', 'rate', -.0003, 'always')],
            effects=dict(skim=[('keeping.leaves', 'mul', .4)], scour=[('keeping.algae', 'mul', .5)], tidy=[('keeping.clarity', 'add', .15)],
                         thin=[('keeping.plants', 'mul', .75)], tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)],
                         scatter=[('keeping.flakes', 'add', .4)], feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         hush=[('hush', 'add', .25), ('subject.trust', 'add', .1)], glimmer=[('trace', 'set', 1), ('subject.mood', 'add', .15)],
                         stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)], crack=[('keeping.ice', 'mul', .3)],
                         thaw=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('glow', .3, '. * .', 'dark_m', 'glow'), ('trace', .3, '~*~*~', 'deep', 'glow'), ('pond_ice', .3, '*-*-*', 'dark_l', 'frost'), ('pond_leaves', .3, ';~";~', 'dark_r', 'leaf')],
            anchors=dict(dark_l=P(28, 43), dark_m=P(58, 41), dark_r=P(88, 39), deep=P(40, 39), edge_far=P(70, 43), pad_low=P(86, 37), bloom_r=P(81, 35), cattail_l=P(7, 31),
                         reed_low=P(8, 38), tuft=P(11, 44), bank_r=P(95, 40), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('lift_the_leaves_without_a_ripple', 'Lifting the fallen leaves off the water one at a time with a reed, careful not to cause a single ripple', 26, 'reed',
        [k(.2, 'dark_r', reach=.4, x=.2, y=.3, b=.2, l=1), k(.38, 'dark_r', reach=1, x=.4, y=.5, b=.6, mark='sh'), k(.56, 'edge_far', reach=1, x=.5, y=.6, b=.7, r=1, mark='sh'), k(.74, 'deep', reach=1, x=.5, y=.6, b=.7, l=1, mark='sh'), k(.9, eye='-')],
        [(.56, 'skim')], g='care', act=('scoop', 'leaves'), when=['pond_leaves>.3'], prefer=['curious'], say=["Not one ripple. A ghost would approve of that.", "Lifted them out like eggs. Dull, but the fish stayed."])
    o.r('sweep_the_grit_so_the_glow_shows', 'Sweeping the grit out of the shallows with a wing so the glow will show clear through the water', 20, 'wing',
        [k(.2, 'dark_l', reach=.4, x=.3, y=.7, b=.4), k(.38, 'dark_l', reach=1, x=.6, y=1.2, b=1, r=1, mark='shff'), k(.56, 'dark_m', reach=1, x=.7, y=1.3, b=1.1, mark='shff'), k(.74, 'dark_r', reach=1, x=.6, y=1.1, b=.9, l=1), k(.9, eye='-')],
        [(.56, 'tidy')], g='care', act=('sweep', 'grit'), when=['pond_clarity<.6'], say=['Grit out, glow in. Housework with a theme.', 'Cleared the shallows. It still would not come close.'])
    o.r('open_up_the_moonlight_between_the_pads', 'Hooking the thick pad aside with a twig to open a window of moonlight on the water', 22, 'twig',
        [k(.2, 'pad_low', reach=.4, x=.2, y=.2, b=.2), k(.4, 'pad_low', reach=1, x=.4, y=.4, b=.5, r=1, mark='hnk'), k(.58, 'bloom_r', reach=1, x=.6, y=.4, b=.7, mark='slip'), k(.76, 'pad_low', reach=1, x=-.1, y=-.4, b=-.3, mark='pop'), k(.9, eye='^')],
        [(.58, 'thin')], g='care', act=('pull', 'pad'), when=['pond_plants>.7'], prefer=['night'])
    o.r('wipe_the_rim_green_so_it_gleams', 'Wiping the green slime off the rim stone with a wing so the glow does not die against it', 18, 'wing',
        [k(.2, 'stone_r', reach=.4, x=.2, y=.7, b=.4), k(.38, 'stone_r', reach=1, x=.3, y=1.1, b=.8, l=1, mark='sqk'), k(.58, 'stone_r', reach=1, x=.3, y=1.3, b=1, mark='sqk'), k(.76, 'stone_r', reach=1, x=.2, y=1, b=.7, r=1), k(.9, eye='^')],
        [(.58, 'scour')], g='care', act=('wipe', 'slime'), when=['pond_algae>.4'])
    o.r('ease_a_weed_strand_off_the_pale_fin', 'Easing a strand of weed off the pale fin with the very tip of his bill, holding his breath', 24, 'none',
        [k(.2, x=.3, y=.4, b=.2), k(.38, 'dark_l', x=.8, y=.9, b=.4, eye='-'), k(.56, 'dark_l', x=.9, y=1.1, b=.5, l=1, mark='...'), k(.72, 'dark_l', x=.5, y=.5, b=.3, r=1, mark='plip'), k(.88, eye='^')],
        [(.56, 'tend')], g='care', act=('unwrap', 'fin'), pick='shyest', when=['fish_health<.8'], obj=[(.36, dict(lure=1)), (.7, dict(lure=1))], say=["Off. Not a ripple from either of us.", "It stayed. Ghosts leave early. This one gave me a pass."])
    o.r('pat_the_flank_dry_of_scum', 'Patting scum off the pale flank with the soft back of a wing while it hangs at the rim', 20, 'wing',
        [k(.2, 'dark_m', reach=.4, x=.2, y=.6, b=.3), k(.4, 'dark_m', reach=1, x=.3, y=1, b=.7, mark='pat'), k(.58, 'dark_m', reach=1, x=.2, y=1.2, b=.9, l=1, mark='pat'), k(.76, 'dark_m', reach=.5, x=.2, y=.7, b=.4), k(.9, eye='-')],
        [(.58, 'tend')], g='care', act=('pat', 'flank'), pick='hungriest', prefer=['fish_health<.9'], obj=[(.36, dict(lure=1)), (.72, dict(lure=1))])
    # ---------------- use
    o.r('scatter_flakes_by_dim_light', 'Scattering a thin handful of flakes over the dim water so they glint down in its glow', 16, 'wing',
        [k(.2, 'dark_m', reach=.4, w=.3), k(.4, 'dark_m', reach=1, x=-.2, y=-.4, b=-.3, mark='tss'), k(.62, x=-.2, y=.1, eye='o'), k(.84, eye='^')],
        [(.4, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.4'], prefer=['night'])
    o.r('offer_a_flake_to_the_glow', 'Offering a flake in his bill to the pale shape rising out of the dark water', 22, 'none',
        [k(.2, x=.4, y=.4, b=.3), k(.4, 'dark_r', x=.9, y=.9, b=.5, eye='o', mark='...'), k(.58, 'dark_r', x=1, y=1.2, b=.7, eye='O', mark='sip'), k(.76, 'dark_r', x=.5, y=.6, b=.3, w=.3, eye='^'), k(.9, eye='-')],
        [(.58, 'feed')], g='use', act=('carry', 'flake'), pick='hungriest', when=['fish_hunger>.4'], prefer=['night'], obj=[(.38, dict(lure=1)), (.66, dict(lure=1)), (.82, dict(lure=0))],
        say=["Took it. Said nothing. Perfect guest.", "A flake, taken by a ghost. I will tell nobody."])
    o.r('tap_the_stone_soft_as_a_heartbeat', 'Tapping the left stone soft as a heartbeat, so only the pale fish hears supper is on', 18, 'none',
        [k(.2, 'stone_l', x=.8, y=.9, b=.3, mark='tp'), k(.4, 'stone_l', x=.8, y=.9, b=.3, mark='tp'), k(.6, 'stone_l', x=.8, y=.9, b=.3, l=1, mark='tp'), k(.8, eye='^')],
        [(.6, 'call')], g='use', act=('tap', 'stone'), when=['pond_bell<.4'], prefer=['night'])
    o.r('hum_it_a_lullaby_at_the_rim', 'Humming a lullaby at the water, soft and flat, until the pale fish stops flinching at his shadow', 26, 'none',
        [k(.2, 'dark_l', x=.4, y=.5, b=.3, eye='-'), k(.38, 'dark_l', x=.6, y=.8, b=.6, eye='-', mark='mmm'), k(.58, 'dark_l', x=.6, y=.9, b=.7, eye='-', mark='mmmm'), k(.78, 'dark_l', x=.5, y=.7, b=.5, eye='-', mark='mm'), k(.9, eye='^')],
        [(.58, 'hush')], g='use', act=('sing', 'lullaby'), pick='shyest', when=['hush<.7'], prefer=['lonely', 'sad'], obj=[(.4, dict(lure=1)), (.75, dict(lure=1))],
        say=["Hummed it a lullaby. It stayed. Better reviews than my band.", "Soft enough that the water forgot me."])
    o.r('draw_a_glimmer_line_with_a_wingtip', 'Drawing a wingtip slowly across the water so the pale fish leaves a glimmering line in its wake', 24, 'wing',
        [k(.2, 'dark_l', reach=.4, x=.2, y=.4, b=.3), k(.4, 'deep', reach=1, x=.4, y=.5, b=.5, l=1), k(.6, 'dark_m', reach=1, x=.5, y=.5, b=.5, r=1, mark='...'), k(.8, 'edge_far', reach=1, x=.5, y=.5, b=.5, l=1), k(.92, eye='^')],
        [(.6, 'glimmer')], g='use', act=('drag', 'wingtip'), pick='shyest', when=['night'], prefer=['trace<.3'], obj=[(.24, dict(lure=1)), (.45, dict(lure=1)), (.65, dict(lure=1)), (.85, dict(lure=1))],
        say=["A line of light. I did that. With a wing.", "Wrote my name in fish glow. Reads 'ow', the fish moved."])
    o.r('stroke_the_cool_side_once', 'Stroking the cool pale side once, very lightly, with the back of a wing', 18, 'wing',
        [k(.2, 'dark_r', reach=.4, x=.2, y=.5, b=.3), k(.4, 'dark_r', reach=1, x=.3, y=.9, b=.6, mark='...'), k(.6, 'dark_r', reach=1, x=.3, y=1, b=.7, r=1), k(.8, 'dark_r', reach=.4, x=.2, y=.5, b=.3), k(.92, eye='^')],
        [(.6, 'stroke')], g='use', act=('press', 'side'), pick='shyest', prefer=['fish_trust>.4', 'lonely'], obj=[(.38, dict(lure=1)), (.72, dict(lure=1))])
    # ---------------- play
    o.r('play_peekaboo_with_the_glow', 'Ducking down out of sight of the glow and popping up when it brightens, three rounds', 22, 'none',
        [k(.2, 'dark_m', x=.3, y=1.3, b=1.2), k(.36, 'dark_m', x=.2, y=1.8, b=1.7, eye='-'), k(.5, 'dark_m', x=.7, y=-.2, b=-.5, w=.8, eye='O', mark='boo'), k(.64, 'dark_m', x=.2, y=1.8, b=1.7, eye='-'), k(.78, 'dark_m', x=.7, y=-.2, b=-.5, w=.8, eye='O', mark='boo!'), k(.9, eye='^')],
        [(.5, 'fun')], g='play', act=('seek', 'glow'), pick='shyest', when=['glow>.4'], prefer=['young', 'happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('puff_a_bubble_to_see_it_glow', 'Puffing one fat bubble down into the dark to watch it light up as the fish noses through it', 18, 'none',
        [k(.2, x=.3, y=.6, b=.4), k(.4, 'dark_r', x=.9, y=1.5, b=.8, eye='-', mark='bbl'), k(.58, 'dark_r', x=1, y=1.7, b=1, eye='O', mark='bloop'), k(.78, 'dark_r', x=.6, y=.9, b=.5, eye='O'), k(.9, eye='^')],
        [], g='play', act=('blow', 'bubble'), pick='shyest', when=['glow>.4'], prefer=['young', 'curious'], obj=[(.4, dict(lure=1)), (.75, dict(lure=1))])
    o.r('creep_after_the_glimmer_in_the_shallows', 'Creeping after a glimmer along the shallows on tiptoe, every foot placed in turn, never quite close', 24, 'none',
        [k(.16, 'dark_l', x=.4, y=.2, b=.2, l=1), k(.32, 'deep', x=.5, y=.2, b=.2, r=1), k(.48, 'dark_m', x=.6, y=.1, b=.2, l=1), k(.64, 'edge_far', x=.7, y=.1, b=.2, r=1, mark='psst'), k(.8, 'dark_r', x=.8, y=.1, b=.2, l=1), k(.92, eye='o')],
        [], g='play', act=('chase', 'glimmer'), pick='hungriest', prefer=['young', 'happy'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.6, dict(lure=1)), (.82, dict(lure=1))])
    o.r('hop_over_the_stones_to_the_pulse', 'Hopping over the stones one at a time to the slow pulse of the glow, left, middle, right', 22, 'none',
        [k(.14, 'stone_l', x=.2, y=-.1, b=-.7, l=1), k(.32, 'stone_m', x=.2, y=-.1, b=-1, r=1, mark='pulse'), k(.5, 'stone_r', x=.2, y=-.1, b=-.7, l=1, mark='pulse'), k(.68, 'stone_m', x=.2, y=-.1, b=-1, r=1, mark='pulse'), k(.86, 'stone_l', x=.2, y=.1, b=.2, eye='^')],
        [], g='play', act=('hop', 'pulse'), pick='hungriest', when=['glow>.4'], prefer=['happy', 'young'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    o.r('catch_a_shining_flake_in_his_bill', 'Snapping at a glinting flake as it drifts down past the glow and catching it on the second try', 18, 'none',
        [k(.2, 'dark_m', x=.6, y=.1, b=.2), k(.38, 'dark_m', x=1, y=.6, b=.5, eye='o', mark='snap'), k(.54, 'dark_m', x=1, y=1.2, b=.8, eye='>', mark='miss'), k(.7, 'dark_m', x=1.3, y=1.5, b=1, eye='O', mark='SNAP'), k(.86, eye='^')],
        [], g='play', act=('catch', 'flake'), pick='hungriest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.74, dict(lure=1))])
    o.r('send_a_leaf_boat_across_its_glow', 'Floating a leaf boat out over the glow and watching the fish circle round the lit patch of water', 22, 'reed',
        [k(.2, 'dark_l', reach=.4, x=.2, y=.3, b=.3), k(.4, 'deep', reach=1, x=.4, y=.5, b=.5, mark='fwp'), k(.6, 'dark_m', reach=1, x=.5, y=.6, b=.6, l=1, mark='fwp'), k(.8, 'edge_far', reach=1, x=.6, y=.6, b=.6, r=1), k(.92, eye='o')],
        [], g='play', act=('float', 'leaf'), pick='shyest', when=['pond_leaves>.2'], prefer=['curious'], obj=[(.6, dict(lure=1)), (.85, dict(lure=1))])
    o.r('dance_the_ripples_in_a_ring', 'Dancing a slow ring along the rim to the rings spreading out from the fish, bow and sway', 24, 'none',
        [k(.14, 'dark_l', x=.2, y=.4, b=.6, l=1, w=.3), k(.3, 'dark_m', x=.3, y=.4, b=.2, r=1, w=.6), k(.46, 'edge_far', x=.2, y=.4, b=.6, l=1, w=.8, mark='la'), k(.62, 'dark_r', x=.3, y=.4, b=.2, r=1, w=.6), k(.78, 'dark_r', x=.2, y=.5, b=.6, w=.3), k(.9, eye='^')],
        [], g='play', act=('dance', 'ripples'), pick='hungriest', prefer=['happy', 'lonely'], obj=[(.2, dict(lure=1)), (.45, dict(lure=1)), (.7, dict(lure=1))])
    # ---------------- test
    o.r('cup_a_wing_to_test_the_glow', 'Cupping a wing over the glowing patch to see how bright it still is in the shade', 18, 'wing',
        [k(.2, 'dark_m', reach=.4, x=.2, y=.6, b=.3), k(.4, 'dark_m', reach=1, x=.4, y=1, b=.9, mark='...'), k(.6, 'dark_m', reach=1, x=.3, y=1.3, b=1.2, eye='O', mark='still'), k(.8, 'dark_m', reach=.4, x=.2, y=.5, b=.3), k(.92, eye='-')],
        [], g='test', act=('test', 'brightness'), when=['glow>.4'], prefer=['curious'])
    o.r('compare_lit_and_unlit_water', 'Comparing the lit patch and the dark patch of the water with a bill dipped in each, left and then right', 20, 'none',
        [k(.2, 'dark_l', x=.7, y=1, b=.4, mark='dark'), k(.4, 'dark_l', x=.8, y=1.3, b=.6), k(.6, 'dark_m', x=.8, y=1.3, b=.6, l=1, mark='lit'), k(.8, 'dark_m', x=.6, y=.7, b=.4, eye='O', mark='hm'), k(.92, eye='^')],
        [], g='test', act=('compare', 'patches'), when=['glow>.4'], prefer=['curious', 'happy'])
    o.r('count_the_pulses_of_the_glow', 'Counting the slow pulses of the glow with one foot raised each time it brightens', 22, 'none',
        [k(.16, 'dark_r', x=.3, y=.4, b=.3, l=1, mark='1'), k(.34, 'dark_r', x=.3, y=.4, b=.3, r=1, mark='2'), k(.52, 'dark_r', x=.3, y=.4, b=.3, l=1, mark='3'), k(.7, 'dark_r', x=.3, y=.4, b=.3, r=1, mark='4'), k(.88, eye='-', mark='slow')],
        [], g='test', act=('count', 'pulses'), pick='hungriest', when=['glow>.4'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))], say=['Slow. It breathes light like a snore.', 'Counted six, then it dimmed. Rude to a counter.'])
    o.r('peer_at_the_pale_scales', 'Peering close at the pale scales, trying to see through them to the rim stones past', 18, 'none',
        [k(.2, x=.4, y=.6, b=.4), k(.4, 'dark_m', x=1, y=1.6, b=.9, eye='o'), k(.58, 'dark_m', x=1.1, y=1.9, b=1.1, eye='@', mark='...'), k(.76, 'dark_m', x=.4, y=.7, b=.4, eye='O'), k(.9, eye='-')],
        [], g='test', act=('peer', 'scales'), pick='shyest', prefer=['curious', 'young'], obj=[(.38, dict(lure=1)), (.7, dict(lure=1))])
    o.r('listen_to_the_dark_for_its_turning', 'Listening to the dark water for the faint sound of its turning, head slowly lowered', 22, 'none',
        [k(.2, 'dark_l', x=-.3, y=.5, b=.3), k(.4, 'dark_l', x=-.5, y=1.1, b=.7, eye='-'), k(.6, 'dark_l', x=-.5, y=1.2, b=.8, l=1, eye='-', mark='...'), k(.8, 'dark_l', x=.2, y=.4, b=.3, eye='O'), k(.92, eye='^')],
        [], g='test', act=('listen', 'dark'), prefer=['curious', 'night'])
    o.r('sound_how_deep_it_hangs', 'Sounding the water with a reed to learn how deep the pale fish hangs by day', 22, 'reed',
        [k(.2, 'dark_r', reach=.4, x=.2, y=.5, b=.3), k(.4, 'dark_r', reach=1, x=.5, y=1, b=.8, mark='plink'), k(.58, 'dark_m', reach=1, x=.6, y=1.2, b=1, l=1, mark='plink'), k(.76, 'dark_l', reach=1, x=.6, y=1.4, b=1.2, r=1, mark='plink'), k(.9, eye='-')],
        [], g='test', act=('measure', 'depth'), when=['day'], prefer=['curious'])
    o.r('hold_it_beside_the_biggest_on_record', 'Holding a wing out to the pale fish\'s length and picturing the biggest ghost fish ever seen beside it', 22, 'wing',
        [k(.2, 'dark_r', reach=.4, x=.7, y=.2, b=.2), k(.4, 'dark_r', reach=1, x=1, y=.3, b=.2, r=1), k(.6, 'dark_l', reach=1, x=.9, y=.1, b=.1, l=1, mark='hm'), k(.8, 'dark_m', reach=.6, x=.5, y=.5, b=.5), k(.92, eye='-', mark='small')],
        [], g='test', act=('compare', 'size'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.38, dict(lure=1)), (.64, dict(lure=1))])
    # ---------------- rest
    o.r('nap_at_the_tuft_while_it_glows', 'Napping at the grass tuft with the glow reflecting off his closed eyelids', 28, 'none',
        [k(.2, 'tuft', x=.1, y=.6, b=.7, eye='-'), k(.4, 'tuft', x=-.2, y=1, b=1.3, eye='-', mark='zz'), k(.62, 'tuft', x=-.3, y=1.2, b=1.5, r=1, eye='-', mark='zzz'), k(.82, 'tuft', x=0, y=.4, b=.4, eye='o'), k(.92, eye='^')],
        [(.62, 'rest')], g='rest', act=('nap', 'tuft'), when=['tired', 'night'])
    o.r('sit_up_late_for_the_glow', 'Sitting up late at the middle stone, chin on his chest, to see the glow come on', 24, 'none',
        [k(.2, 'stone_m', x=.2, y=.3, b=.9), k(.4, 'stone_m', x=.1, y=.6, b=1.6, eye='-'), k(.6, 'stone_m', x=0, y=.7, b=1.7, l=1, eye='o', mark='...'), k(.8, 'dark_m', x=.8, y=.4, b=.5, eye='O')],
        [(.6, 'rest')], g='rest', act=('sit', 'stone'), when=['night_late'], prefer=['tired', 'lonely'])
    o.r('lean_on_the_cattail_in_the_dark', 'Leaning on the left cattail stem in the dark, a single eye on the shape that comes and goes', 20, 'none',
        [k(.2, 'cattail_l', x=-.2, y=.3, b=.4), k(.4, 'cattail_l', x=-.4, y=.5, b=.7, eye='-'), k(.6, 'cattail_l', x=-.5, y=.5, b=.8, l=1, eye='o', mark='...'), k(.8, x=.3, y=.3, b=.2, eye='O'), k(.9, eye='^')],
        [], g='rest', act=('lean', 'cattail'), prefer=['tired', 'sad'])
    o.r('wait_for_the_glow_to_come_on', 'Waiting at the rim for the first faint glow to come on in the water as the light goes', 22, 'none',
        [k(.2, 'dark_m', x=.4, y=.8, b=.5, eye='o'), k(.4, 'dark_m', x=.4, y=.8, b=.5, eye='o'), k(.6, 'dark_m', x=.5, y=1, b=.6, r=1, eye='O', mark='...'), k(.8, 'dark_m', x=.2, y=.5, b=.3, eye='^')],
        [], g='rest', act=('wait', 'glow'), pick='shyest', when=['dusk'], prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sulk_in_the_unlit_water', 'Sulking at the water that will not light up for him, head hung and wings wrapped tight', 22, 'none',
        [k(.2, x=-.2, y=.5, b=.3, w=.5), k(.4, 'dark_l', x=-.5, y=1, b=.7, w=1, eye='-'), k(.6, 'dark_l', x=-.6, y=1.1, b=.8, w=1, l=1, eye='-', mark='hmph'), k(.8, x=-.3, y=.5, b=.3, w=.4, eye='-')],
        [], g='rest', act=('sulk', 'water'), when=['sad'])
    # ---------------- weather
    o.r('prick_the_ice_open_for_the_glow', 'Pricking a clear patch in the ice with light bill taps so the glow has a window to shine out of', 22, 'none',
        [k(.18, 'dark_l', x=.5, y=.7, b=.4), k(.34, 'deep', x=.9, y=1.1, b=.7, mark='tk'), k(.5, 'deep', x=1, y=1.3, b=.8, r=1, mark='tk'), k(.66, 'dark_m', x=.9, y=1.2, b=.7, l=1, mark='crk'), k(.82, 'dark_m', x=.4, y=.5, b=.3, eye='^')],
        [(.66, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('scrape_the_rime_from_the_glass_shallows', 'Scraping the rime off the left shallows with a wing so the glow does not frost over', 18, 'wing',
        [k(.2, 'dark_l', reach=.4, x=.2, y=.6, b=.3), k(.38, 'dark_l', reach=1, x=.4, y=1, b=.7, mark='skrr'), k(.56, 'dark_l', reach=1, x=.4, y=1.2, b=.9, l=1, mark='skrr'), k(.74, 'dark_l', reach=1, x=.3, y=.9, b=.6), k(.9, eye='-')],
        [(.56, 'thaw')], g='weather', act=('scrape', 'rime'), when=['pond_ice>.3'])
    o.r('fan_the_still_water_with_a_wing_pair', 'Fanning the stale still water in slow sweeps with both wings so air gets down to the fish', 22, 'wing',
        [k(.16, 'dark_m', reach=.4, y=-.3, b=-.4, l=1), k(.32, 'dark_m', reach=1, x=.2, y=.5, b=.5, mark='fff'), k(.48, 'dark_m', reach=.4, y=-.3, b=-.4, r=1), k(.64, 'dark_r', reach=1, x=.2, y=.5, b=.5, mark='fff'), k(.8, 'dark_r', reach=1, x=.2, y=.5, b=.5, l=1, mark='fff'), k(.92, eye='-')],
        [(.64, 'stir')], g='weather', act=('shake', 'water'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('wait_out_the_rain_at_the_tuft', 'Waiting out the rain at the tuft with his head tucked low, listening to the drops on the water', 30, 'none',
        [k(.2, 'tuft', x=.2, y=.7, b=.8), k(.4, 'tuft', x=-.1, y=1.2, b=1.5, eye='-'), k(.64, 'tuft', x=-.2, y=1.3, b=1.6, l=1, eye='-', mark='drip'), k(.84, 'tuft', x=.3, y=.5, b=.5, eye='^')],
        [], g='weather', act=('shelter', 'tuft'), when=['wet'])
    o.r('shade_the_water_from_the_glare', 'Tilting a wing out over the water to throw shade so the pale fish dares come up in the daylight', 22, 'wing',
        [k(.18, 'dark_m', reach=.4, x=.2, y=.3, b=.3), k(.36, 'dark_m', reach=1, x=.3, y=.1, b=.4, mark='...'), k(.56, 'dark_m', reach=1, x=.3, y=.1, b=.5, l=1), k(.76, 'dark_m', reach=1, x=.3, y=.1, b=.4, r=1), k(.9, eye='^')],
        [], g='weather', act=('tilt', 'wing'), pick='shyest', when=['sun'], prefer=['curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('crouch_low_against_the_gust', 'Crouching low at the bank against the gust so no leaf lands on the water over the fish', 18, 'none',
        [k(.16, 'bank_r', x=.3, y=.6, b=1, l=1), k(.32, 'bank_r', x=.4, y=.9, b=1.7, w=.9, mark='whoo'), k(.52, 'bank_r', x=.4, y=1, b=1.9, w=1, r=1), k(.72, 'bank_r', x=.3, y=.7, b=1.2, w=.5), k(.88, eye='-')],
        [], g='weather', act=('brace', 'gust'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_ghost_of_the_pond', 'Bowing to the ghost of the pond, with a wing across his chest, as it drifts by', 18, 'none',
        [k(.2, 'dark_r', x=.2, y=.2, b=.2, w=.9), k(.4, 'dark_r', x=.7, y=1.7, b=1, w=.9, eye='-'), k(.6, 'dark_r', x=.8, y=2, b=1.3, w=.7, eye='-', mark='milord'), k(.8, 'dark_r', x=0, y=-.2, b=-.1, w=.3, eye='^')],
        [], g='show', act=('bow', 'ghost'), pick='shyest', prefer=['happy'], obj=[(.38, dict(lure=1)), (.72, dict(lure=1))], say=["Bowed to a haunting. We got on.", "Very pale, very polite. Better manners than mine."])
    o.r('present_the_glow_to_the_empty_bank', 'Presenting the glow to the empty bank with a hushed sweep of the wing, a showman whispering', 22, 'wing',
        [k(.18, 'dark_m', reach=.3, x=.3, y=-.3, b=-.3), k(.36, 'dark_m', reach=1, x=.4, y=-.5, b=-.5, l=1), k(.56, 'dark_l', reach=1, x=.4, y=-.6, b=-.6, r=1, mark='ssh'), k(.76, 'dark_l', reach=1, x=.3, y=-.3, b=-.3), k(.9, eye='^')],
        [], g='show', act=('present', 'glow'), pick='shyest', when=['glow>.4'], prefer=['happy'], obj=[(.4, dict(lure=1)), (.75, dict(lure=1))])
    o.r('argue_in_a_whisper', 'Arguing with the pale fish in a furious whisper about who is supposed to be the ghost here', 20, 'none',
        [k(.18, 'dark_m', x=.9, y=.5, b=.4), k(.34, 'dark_m', x=1.2, y=.4, b=.3, mark='psst'), k(.5, 'dark_m', x=1.3, y=.3, b=.3, r=1, mark='psst!'), k(.66, 'dark_m', x=1.2, y=.4, b=.3, l=1, mark='psst'), k(.82, 'dark_m', x=.6, y=.5, b=.4), k(.92, eye='-')],
        [], g='show', act=('argue', 'ghost'), pick='hungriest', prefer=['grumpy'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))], say=["It claims the haunting. I claim the tenancy.", "Lost a whisper fight to a fish. Dignity gone, haunting intact."])
    o.r('pose_in_the_glow_like_a_statue', 'Posing at the right stone in the glow like a statue, one foot up, never so much as blinking', 20, 'none',
        [k(.18, 'stone_r', x=.2, y=-.2, w=.3, l=1, perch=1), k(.36, 'stone_r', x=.3, y=-.4, b=-.2, w=.5, l=1, perch=1), k(.6, 'stone_r', x=.3, y=-.4, b=-.2, w=.5, l=1, perch=1, eye='-', mark='...'), k(.82, 'stone_r', x=.1, y=-.1, w=.2, perch=1)],
        [], g='show', act=('pose', 'statue'), pick='shyest', when=['glow>.4'], prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('show_it_off_to_the_far_cattails', 'Showing the glowing fish off to the far cattails with a pointed wing, in a thrilled whisper', 20, 'wing',
        [k(.18, 'bank_r', reach=.3, x=.2, y=-.1, b=.2), k(.36, 'bank_r', reach=1, x=.5, y=-.4, b=-.3, mark='psst'), k(.56, 'bank_r', reach=1, x=.6, y=-.5, b=-.4, r=1, mark='LOOK'), k(.76, 'bank_r', reach=.5, x=.2, y=0, b=.1), k(.9, eye='^')],
        [], g='show', act=('show', 'cattails'), prefer=['happy', 'young'], say=["Showed them the glow. Cattails nodded in the wind. Agreed.", "Whispered a fish to the reeds. They kept it quiet."])
    # ---------------- mishap
    o.r('slip_on_the_dewy_stone', 'Slipping on the dewy stone in the dark, both feet gone, and landing with a muffled flump', 16, 'none',
        [k(.16, 'stone_l', x=.5, y=.3, b=.3), k(.32, 'stone_l', x=1.2, y=-.3, b=-.5, l=1, r=1, w=.5, mark='eep'), k(.48, 'stone_l', x=1.4, y=.8, b=1.8, w=.8, eye='O', mark='flump'), k(.68, 'stone_l', x=.8, y=.6, b=1.1, eye='>'), k(.84, eye='-')],
        [], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('stuck_in_the_crook_of_a_reed', 'Poking his head into the crook between two reeds after a glimmer and then needing to back out slowly', 24, 'none',
        [k(.16, x=.5, y=.5, b=.4), k(.32, 'reed_low', x=1.7, y=.3, b=.5, eye='O'), k(.5, 'reed_low', x=1.8, y=.4, b=.6, eye='@', mark='...'), k(.66, 'reed_low', x=1.5, y=.3, b=1.2, l=1, mark='mm'), k(.8, 'reed_low', x=.6, y=-.2, b=-.5, w=.9, mark='pop'), k(.92, x=1.1, y=.8, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'crook'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_dark_stem', 'Walking straight at the left cattail in the dark after a glimmer, and meeting the stem with his bill', 20, 'none',
        [k(.14, 'dark_l', x=.4, y=.2, b=.2, r=1), k(.3, 'tuft', x=.5, y=.1, b=.3, l=1), k(.46, 'reed_low', x=1.6, y=-.2, b=1.4, eye='@', mark='thok'), k(.62, 'reed_low', x=-.9, y=.3, b=.1, w=.8, eye='x'), k(.84, x=.2, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'cattail'), when=['night_late'])
    o.r('jump_back_from_the_sudden_flare', 'Jumping back from the rim when the glow flares up in his face all at once, wings out', 16, 'none',
        [k(.14, 'dark_m', x=.9, y=1.4, b=.9), k(.28, 'dark_m', x=1, y=1.6, b=1, eye='o', mark='...'), k(.4, x=-1.3, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='GAH'), k(.6, x=-.7, y=.3, b=-.1, eye='>'), k(.82, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'flare'), pick='hungriest', when=['glow>.5'], prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))], say=["It lit up. I did not. We are not alike.", "A flash, a shriek, a duck three feet back. Textbook."])
    o.r('stamp_the_scare_out_of_his_feet', 'Stamping the scare out of his feet after the flare, left then right, muttering into his chest', 16, 'none',
        [k(.16, 'stone_m', x=.4, y=.6, b=.5), k(.28, 'stone_m', x=.3, y=0, b=-1, l=1, mark='stmp'), k(.4, 'stone_m', x=.4, y=.5, b=.5), k(.54, 'stone_m', x=.3, y=0, b=-1, r=1, mark='stmp'), k(.7, 'stone_m', x=.5, y=.7, b=.3, eye='>'), k(.86, eye='-')],
        [], g='mishap', act=('stamp', 'feet'), prefer=['grumpy'])
    # ---------------- duets
    o.r('pass_the_lullaby_down_the_rim', 'Humming the lullaby at the left end of the rim while a friend takes it up at the right, the pale fish hanging between them', 26, 'none',
        [k(.16, 'dark_l', x=1.1, y=1.3, b=1.1, eye='-'), k(.34, 'deep', x=1.3, y=1.7, b=1.4, eye='-', mark='mmm'), k(.52, 'deep', x=1.4, y=1.9, b=1.6, l=1, r=1, eye='-', mark='mmmm'), k(.7, 'dark_l', x=1, y=1.2, b=1, eye='-'), k(.86, eye='^')],
        [(.52, 'hush')], g='use', act=('sing', 'chorus'), pick='shyest', when=['hush<.7'], prefer=['lonely', 'happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))],
        duo=[k(.18, 'dark_r', x=.3, y=.4, b=.3), k(.38, 'dark_r', x=.5, y=.7, b=.5, eye='-', mark='mmm'), k(.58, 'dark_r', x=.6, y=.8, b=.6, r=1, eye='-', mark='mmmm'), k(.78, 'dark_r', x=.3, y=.4, b=.3, eye='^')],
        say=["Passed the lullaby on. The fish stayed. Rare tribute.", "A duet in a whisper. It had perfect pitch, probably."])
    o.r('light_chain_with_a_friend_the_fish_follows', 'Drawing a glimmer line with a wing while a friend draws another from the far side, the fish tracing both', 26, 'wing',
        [k(.14, 'dark_r', reach=.4, x=1, y=-.2, b=-.4), k(.32, 'edge_far', reach=1, x=1.3, y=.9, b=1, l=1), k(.5, 'dark_m', reach=1, x=1.5, y=1.2, b=1.3, r=1, mark='...'), k(.68, 'deep', reach=1, x=1.3, y=.9, b=1, l=1, r=1), k(.86, eye='^')],
        [(.5, 'glimmer')], g='play', act=('wrap', 'light'), pick='shyest', when=['night'], prefer=['happy'], obj=[(.2, dict(lure=1)), (.45, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.16, 'dark_r', x=.3, y=.4, b=.3), k(.34, 'edge_far', x=.6, y=.8, b=.6, r=1), k(.52, 'dark_m', x=.7, y=.9, b=.7, l=1, mark='...'), k(.7, 'deep', x=.7, y=.9, b=.7, r=1), k(.86, eye='^')])
    o.r('count_the_pulses_back_to_back', 'Counting the glow\'s pulses out loud while a friend counts them silently, then swapping totals at the rim', 24, 'none',
        [k(.14, 'dark_m', x=.3, y=.5, b=.3, mark='1'), k(.3, 'dark_m', x=.4, y=.6, b=.4, mark='2'), k(.46, 'dark_m', x=.4, y=.6, b=.4, l=1, mark='3'), k(.64, 'dark_l', x=.5, y=.7, b=.5, mark='6?'), k(.82, 'dark_l', x=.2, y=.4, b=.3, eye='^')],
        [], g='test', act=('count', 'beats'), pick='hungriest', when=['glow>.4'], prefer=['curious'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.16, 'dark_r', x=.3, y=.4, b=.3), k(.34, 'dark_r', x=.4, y=.5, b=.4, eye='-'), k(.52, 'dark_r', x=.4, y=.5, b=.4, r=1, eye='-', mark='...'), k(.7, 'dark_m', x=.5, y=.7, b=.5, mark='5'), k(.86, eye='^')],
        say=["Six. Or five. Glow pulses when it wants to.", "Counted aloud and a friend counted silent. Silence won."])
    return done(o)


def golden_koi():
    # Golden koi: rare, top dweller, morning fish with barbels, shimmers at dawn. Own state: shimmer (how it glints: builds at dawn, fades after, drawn at the
    # right bloom), rise (how readily it rises to a wingtip).
    o = Obj('golden_koi', 'keeping', on='koi_pond',
            fields=dict(shimmer=(0, 0, 1), rise=(0, 0, 1)),
            physics=[('shimmer', 'rate', .004, 'dawn'), ('shimmer', 'rate', -.003, '!dawn'), ('rise', 'rate', -.0003, 'always')],
            effects=dict(skim=[('keeping.leaves', 'mul', .4)], scour=[('keeping.algae', 'mul', .5)], thin=[('keeping.plants', 'mul', .75)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], scatter=[('keeping.flakes', 'add', .4)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         lead=[('rise', 'add', .2), ('subject.trust', 'add', .1)], kiss=[('subject.trust', 'add', .1), ('subject.mood', 'add', .15)],
                         glint=[('shimmer', 'set', 1), ('subject.mood', 'add', .15)], stroke=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)],
                         crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('shimmer', .3, '.*~*.', 'bloom_r', 'glow'), ('pond_leaves', .3, ';"~;"', 'run', 'leaf'), ('pond_ice', .3, '*=*=*', 'sheen_l', 'frost')],
            anchors=dict(sheen_l=P(28, 43), sheen_m=P(58, 41), sheen_r=P(88, 39), run=P(70, 43), pad_low=P(86, 37), bloom_r=P(81, 35), tuft=P(11, 44),
                         reed_low=P(8, 38), bank_r=P(95, 40), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('fish_the_leaves_off_the_golden_run', 'Fishing the leaves off the stretch of surface the golden koi rises through, with a long slow pull of a reed', 22, 'reed',
        [k(.15, 'sheen_r', reach=.5, x=.6, y=-.2, b=.2, w=0), k(.35, 'run', reach=1, x=.9, y=.1, b=.5, mark='swsh'), k(.55, 'sheen_m', reach=1, x=1, y=.2, b=.7, mark='swsh'), k(.75, 'sheen_l', reach=1, x=.7, y=.2, b=.4), k(.9, eye='^')],
        [(.55, 'skim')], g='care', act=('scoop', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'], say=["Clean run for the gold. Leaves had it coming.", "Fished out a whole autumn. It hasn't noticed."])
    o.r('wipe_the_stones_where_it_sunbathes', 'Wiping the green off the middle stone where the golden koi lies up to catch the early sun', 18, 'wing',
        [k(.15, 'stone_m', reach=.5, x=.5, y=1.2, b=.3), k(.33, 'stone_m', reach=1, x=.9, y=1.6, b=.9, r=1, mark='sqk'), k(.53, 'stone_m', reach=1, x=1, y=1.8, b=1, mark='sqk'), k(.73, 'stone_m', reach=1, x=.6, y=1.3, b=.7, l=1), k(.88, eye='^')],
        [(.53, 'scour')], g='care', act=('wipe', 'stone'), when=['pond_algae>.4'])
    o.r('prune_the_crowded_blooms', 'Pruning back the crowded bloom with a twig, hooking the stem and pulling it clear of the gold\'s lane', 22, 'twig',
        [k(.15, 'pad_low', reach=.4, x=.3, y=.1, b=.2), k(.35, 'bloom_r', reach=1, x=.6, y=.2, b=.6, mark='hnk'), k(.55, 'bloom_r', reach=1, x=.8, y=.3, b=.8, l=1, r=1), k(.75, 'bloom_r', reach=1, x=0, y=-.5, b=-.4, w=.5, mark='snap'), k(.9, eye='-')],
        [(.55, 'thin')], g='care', act=('pull', 'blooms'), when=['pond_plants>.7'])
    o.r('untangle_the_long_barbels_from_a_stem', 'Untangling the long barbels from a pad stem one at a time with the very tip of a wing', 24, 'wing',
        [k(.15, 'pad_low', reach=.4, x=.3, y=.4, b=.3), k(.34, 'pad_low', reach=1, x=.5, y=.8, b=.7, eye='-'), k(.54, 'sheen_r', reach=1, x=.6, y=1, b=.9, l=1, mark='tug'), k(.72, 'sheen_r', reach=1, x=.4, y=.6, b=.5, r=1, mark='plip'), k(.88, eye='^')],
        [(.54, 'tend')], g='care', act=('unwrap', 'barbels'), pick='shyest', when=['fish_health<.8'], obj=[(.32, dict(lure=1)), (.7, dict(lure=1))], say=["Free. It looked at me like I owed it gold. Fair.", "One stem, two barbels, a lot of thanks left unspoken."])
    o.r('polish_a_dull_patch_of_gold_scales', 'Polishing a dull patch on the golden flank with the soft inside of a wing until it throws light again', 22, 'wing',
        [k(.15, 'sheen_m', reach=.5, x=.3, y=.8, b=.4), k(.33, 'sheen_m', reach=1, x=.5, y=1.3, b=.9, mark='rub'), k(.5, 'sheen_m', reach=1, x=.6, y=1.5, b=1.1, l=1, mark='rub rub'), k(.7, 'sheen_m', reach=1, x=.4, y=1.2, b=.8, r=1), k(.88, eye='^', mark='shine')],
        [(.5, 'tend')], g='care', act=('polish', 'scales'), pick='hungriest', prefer=['fish_health<.9', 'happy'], obj=[(.3, dict(lure=1)), (.68, dict(lure=1))])
    # ---------------- use
    o.r('tilt_a_wing_to_throw_the_light', 'Tilting a wing at the sun so a glint slides over the water and the golden koi rises to meet it', 22, 'wing',
        [k(.12, 'sheen_l', reach=.5, x=.1, y=-.3, b=.1), k(.3, 'sheen_m', reach=1, x=.3, y=-.7, b=-.3, mark='...'), k(.5, 'sheen_m', reach=1, x=.5, y=-.9, b=-.5, l=1, mark='flash'), k(.7, 'run', reach=1, x=.5, y=-.7, b=-.3), k(.88, eye='O')],
        [(.5, 'glint')], g='use', act=('tilt', 'wing'), pick='shyest', when=['dawn_or_day'], prefer=['sun', 'happy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))],
        say=["Threw a sunbeam. It chased it. Me neither, so far.", "Gold fish, gold light. Redundant, shining."])
    o.r('scatter_flakes_in_the_first_light', 'Scattering flakes over the water in the first light so each one lands in a glint of gold', 16, 'wing',
        [k(.15, 'sheen_m', reach=.5, w=.2), k(.35, 'sheen_m', reach=1, x=.1, y=-.7, b=-.5, mark='tss'), k(.6, x=.2, y=-.1, eye='o'), k(.85, eye='^')],
        [(.35, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.4'], prefer=['dawn'])
    o.r('hold_a_flake_to_the_dawn_surface', 'Holding a flake just at the surface until the golden koi rolls up out of the pink water and sips it', 22, 'none',
        [k(.15, x=.3, y=.4, b=.3), k(.35, 'sheen_r', x=1, y=1, b=.7, eye='o', mark='...'), k(.52, 'sheen_r', x=1.1, y=1.3, b=.9, eye='O', mark='sip'), k(.7, 'sheen_r', x=.5, y=.6, b=.4, w=.5, eye='^'), k(.88, eye='-')],
        [(.52, 'feed')], g='use', act=('carry', 'flake'), pick='hungriest', when=['fish_hunger>.4'], prefer=['dawn'], obj=[(.35, dict(lure=1)), (.62, dict(lure=1)), (.8, dict(lure=0))],
        say=["Sipped from my bill. A nibble of royalty.", "Hand-fed a golden fish. Do not tell the others, they are plain."])
    o.r('tap_the_stone_for_the_morning_call', 'Tapping the left stone with his bill in a bright quick pattern for the morning feed call', 16, 'none',
        [k(.15, 'stone_l', x=1.2, y=1.2, b=.4, mark='tik'), k(.3, 'stone_l', x=1.3, y=1.3, b=.5, l=1, mark='tik tik'), k(.46, x=.2, y=.1, w=.4), k(.62, 'stone_l', x=1.3, y=1.4, b=.5, r=1, mark='TIK'), k(.84, eye='^')],
        [(.62, 'call')], g='use', act=('tap', 'stone'), when=['pond_bell<.4'], prefer=['dawn'])
    o.r('lead_it_through_the_blooms_with_a_wingtip', 'Leading the golden koi through the blooms on a wingtip, round one pad and out past the next', 26, 'wing',
        [k(.12, 'sheen_l', reach=.5, x=.2, y=.4, b=.2), k(.3, 'sheen_m', reach=1, x=.6, y=.2, b=.4), k(.5, 'bloom_r', reach=1, x=.8, y=.1, b=.6, r=1), k(.7, 'pad_low', reach=1, x=.8, y=.2, b=.6, l=1), k(.88, 'sheen_r', reach=1, x=.5, y=.4, b=.3)],
        [(.5, 'lead')], g='use', act=('chase', 'wingtip'), pick='hungriest', when=['rise<.8'], obj=[(.15, dict(lure=1)), (.32, dict(lure=1)), (.55, dict(lure=0)), (.75, dict(lure=1))],
        say=["It looped a lily like it owned the lease.", "Led a gold fish about. Nobody had to bribe it."])
    o.r('offer_the_bill_tip_to_be_mouthed', 'Offering the very tip of his bill to be mouthed, gently, by the golden koi as it noses up', 20, 'none',
        [k(.15, x=.3, y=.5, b=.4), k(.34, 'sheen_l', x=1, y=1.3, b=.8, eye='-', mark='...'), k(.52, 'sheen_l', x=1.1, y=1.5, b=1, eye='-', mark='mwah'), k(.7, 'sheen_l', x=.6, y=.8, b=.5, w=.3, eye='^'), k(.88, eye='-')],
        [(.52, 'kiss')], g='use', act=('press', 'bill'), pick='shyest', prefer=['fish_trust<.8', 'happy'], obj=[(.34, dict(lure=1)), (.65, dict(lure=1))])
    o.r('stroke_the_gold_down_its_back', 'Stroking down the golden back with a wing from head to tail in one slow, careful pass', 22, 'wing',
        [k(.12, 'sheen_r', reach=.5, x=.3, y=.7, b=.3), k(.3, 'sheen_r', reach=1, x=.4, y=1, b=.6, mark='...'), k(.5, 'run', reach=1, x=.5, y=1.1, b=.8, r=1), k(.7, 'sheen_m', reach=1, x=.5, y=1.1, b=.8, l=1), k(.88, eye='^')],
        [(.5, 'stroke')], g='use', act=('pat', 'back'), pick='shyest', prefer=['fish_trust>.4'], obj=[(.32, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    # ---------------- play
    o.r('race_the_gold_along_the_pads', 'Racing the golden koi from pad to pad along the far side, arms out, a streak of gold well ahead', 20, 'none',
        [k(.1, 'sheen_l', x=.4, y=-.3, b=.2, w=.5), k(.28, 'run', x=1, y=-.4, b=-.7, l=1, w=1), k(.46, 'sheen_r', x=1.4, y=-.4, b=-.9, r=1, w=1, mark='whoosh'), k(.64, 'pad_low', x=1.5, y=-.2, b=-.6, l=1, w=.9), k(.84, 'bank_r', x=.4, y=.4, b=.3, eye='@')],
        [(.46, 'fun')], g='play', act=('race', 'pads'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=1))],
        say=["Lost to an ornament. Of course. It is gold.", "Beaten by a flake with fins. Pride in the bin."])
    o.r('pop_up_from_the_bloom_with_a_cheep', 'Ducking at the right bloom, then popping up with a cheep just as the golden koi comes round it', 22, 'none',
        [k(.14, 'bloom_r', x=.3, y=1.2, b=1.3, w=.2), k(.32, 'bloom_r', x=.2, y=1.6, b=1.7, eye='-'), k(.5, 'bloom_r', x=.5, y=-.9, b=-1, w=1, eye='O', mark='CHEEP'), k(.66, 'bloom_r', x=.2, y=1.6, b=1.6, eye='-'), k(.8, 'bloom_r', x=.5, y=-.7, b=-.8, w=.9, mark='CHEEP!'), k(.92, eye='^')],
        [], g='play', act=('seek', 'koi'), pick='shyest', prefer=['young', 'curious'], obj=[(.5, dict(lure=1)), (.82, dict(lure=1))])
    o.r('trade_bubbles_with_the_gold', 'Trading bubbles with the golden koi, one for one, until it blows a bigger one that bursts on his bill', 20, 'none',
        [k(.14, x=.4, y=.4, b=.4), k(.3, 'sheen_m', x=1.1, y=1.5, b=1, mark='blp'), k(.48, 'sheen_m', x=1.2, y=1.7, b=1.2, eye='O', mark='blp blp'), k(.66, 'sheen_m', x=1.4, y=1.9, b=1.4, eye='@', mark='POP'), k(.84, x=.4, y=.6, b=.5, eye='^')],
        [], g='play', act=('blow', 'bubbles'), pick='shyest', prefer=['happy', 'young'], obj=[(.32, dict(lure=1)), (.66, dict(lure=1))])
    o.r('send_a_leaf_round_the_bloom', 'Sending a drifting leaf round the right bloom with a reed for the golden koi to nose home', 24, 'reed',
        [k(.14, 'sheen_r', reach=.5, x=.4, y=.1, b=.3), k(.32, 'pad_low', reach=1, x=.7, y=.3, b=.6, mark='fwp'), k(.5, 'bloom_r', reach=1, x=.8, y=.2, b=.7, l=1, mark='fwp'), k(.68, 'run', reach=1, x=.8, y=.3, b=.6, r=1, mark='bmp'), k(.86, eye='o')],
        [], g='play', act=('float', 'leaf'), pick='hungriest', when=['pond_leaves>.2'], prefer=['curious'], obj=[(.5, dict(lure=1)), (.75, dict(lure=1))])
    o.r('spin_in_the_gold_light_of_the_surface', 'Spinning on the spot at the rim with both wings out, the golden koi circling the glints he throws', 22, 'none',
        [k(.12, 'sheen_m', x=.3, y=-.2, b=-.3, w=.6), k(.28, 'sheen_m', x=1, y=-.5, b=-.8, w=1, l=1), k(.44, 'sheen_m', x=-1, y=-.5, b=-.8, w=1, r=1, mark='whee'), k(.6, 'sheen_m', x=1, y=-.5, b=-.8, w=1, l=1), k(.78, 'sheen_m', x=.2, y=.4, b=.5, w=.3, eye='@'), k(.9, eye='^')],
        [], g='play', act=('spin', 'rim'), pick='hungriest', prefer=['happy', 'young'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('snap_at_the_sparkles_it_throws', 'Snapping at the sparkles that skip off its scales across the water, missing nearly every one', 18, 'none',
        [k(.14, 'sheen_l', x=.7, y=.4, b=.3), k(.3, 'sheen_m', x=1.2, y=.6, b=.5, eye='o', mark='snap'), k(.46, 'run', x=1.3, y=.7, b=.6, l=1, eye='>', mark='miss'), k(.62, 'sheen_r', x=1.4, y=.8, b=.7, r=1, mark='SNAP'), k(.82, y=.3, eye='@')],
        [], g='play', act=('catch', 'sparkles'), pick='hungriest', when=['shimmer>.4'], prefer=['happy'], obj=[(.34, dict(lure=1)), (.66, dict(lure=1))])
    o.r('hop_the_stones_to_the_flash', 'Hopping stone to stone at the rim in time with each flash from the gold, one hop for every flash', 20, 'none',
        [k(.12, 'stone_l', x=.3, y=-.3, b=-.8, w=.5, l=1), k(.3, 'stone_m', x=.3, y=-.3, b=-1.1, w=.7, r=1, mark='hup'), k(.5, 'stone_r', x=.3, y=-.3, b=-.8, w=.7, l=1, mark='hup'), k(.7, 'stone_m', x=.3, y=-.3, b=-1.1, w=.7, r=1), k(.86, 'stone_l', x=.2, y=.2, b=.3, eye='^')],
        [], g='play', act=('hop', 'flash'), pick='hungriest', prefer=['young', 'happy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))])
    # ---------------- test
    o.r('count_the_gold_flecks_on_its_flank', 'Counting the gold flecks along its flank, bill tap by bill tap, from gill to tail', 24, 'none',
        [k(.12, 'sheen_l', x=.9, y=1.1, b=.6, mark='1'), k(.28, 'sheen_l', x=1, y=1.3, b=.7, mark='2'), k(.44, 'sheen_m', x=1, y=1.3, b=.7, l=1, mark='3'), k(.6, 'sheen_m', x=1.1, y=1.5, b=.8, r=1, mark='4'), k(.78, eye='-', mark='lots')],
        [], g='test', act=('count', 'flecks'), pick='hungriest', prefer=['curious'], obj=[(.3, dict(lure=1)), (.65, dict(lure=1))])
    o.r('hold_it_up_against_the_sunrise', 'Holding a wing up beside the sunrise and then beside the golden koi to see which is more gold', 22, 'wing',
        [k(.14, 'sheen_m', reach=.4, x=.2, y=-.8, b=-.2), k(.32, 'sheen_m', reach=1, x=.3, y=-1.2, b=-.4, mark='hm'), k(.5, 'sheen_r', reach=1, x=.5, y=.9, b=.6, l=1), k(.68, 'sheen_r', reach=1, x=.5, y=.9, b=.6, r=1, mark='koi'), k(.86, eye='-', mark='koi')],
        [], g='test', act=('compare', 'gold'), pick='hungriest', when=['dawn'], prefer=['curious', 'happy'], obj=[(.5, dict(lure=1)), (.75, dict(lure=1))])
    o.r('peer_at_the_sunrise_in_its_scales', 'Peering close at the tiny sunrise reflected in each scale, bill almost on the water', 18, 'none',
        [k(.14, x=.4, y=.7, b=.4), k(.32, 'sheen_l', x=1, y=1.7, b=1, eye='o'), k(.5, 'sheen_l', x=1.1, y=2, b=1.2, eye='@', mark='...'), k(.7, 'sheen_l', x=.5, y=.9, b=.6, eye='O'), k(.88, eye='^')],
        [], g='test', act=('peer', 'scales'), pick='shyest', prefer=['curious', 'young'], obj=[(.3, dict(lure=1)), (.66, dict(lure=1))])
    o.r('listen_to_the_dawn_start_over_the_pond', 'Listening to the dawn start up over the pond, head high, waiting for the first gold ring', 22, 'none',
        [k(.14, 'tuft', x=-.4, y=-.5, b=.2), k(.34, 'tuft', x=-.6, y=-.8, b=.3, eye='o'), k(.54, 'tuft', x=-.6, y=-.9, b=.3, l=1, eye='-', mark='...'), k(.74, 'sheen_m', x=.8, y=.2, b=.4, eye='O', mark='!'), k(.9, eye='^')],
        [], g='test', act=('listen', 'dawn'), when=['dawn'], prefer=['curious', 'lonely'])
    o.r('measure_the_whole_gold_with_a_reed', 'Measuring the golden koi nose to tail with a reed laid flat along the water', 24, 'reed',
        [k(.14, 'sheen_l', reach=.5, x=.3, y=.4, b=.3), k(.32, 'sheen_l', reach=1, x=.5, y=.6, b=.6), k(.52, 'run', reach=1, x=.7, y=.7, b=.8, l=1, mark='hm'), k(.72, 'sheen_r', reach=1, x=.7, y=.7, b=.8, r=1), k(.88, eye='-', mark='grown')],
        [], g='test', act=('measure', 'koi'), pick='hungriest', prefer=['curious', 'grown'], obj=[(.32, dict(lure=1)), (.6, dict(lure=1))])
    o.r('sniff_the_bloom_it_rises_beside', 'Sniffing the bloom the golden koi rises beside, then sneezing a lily dust cloud off his bill', 16, 'none',
        [k(.14, 'pad_low', x=.4, y=.4, b=.3), k(.34, 'bloom_r', x=.9, y=.5, b=.5, mark='snf'), k(.54, 'bloom_r', x=.9, y=.7, b=.6, eye='-'), k(.72, x=-.9, y=-.6, b=-.3, w=.7, eye='>', mark='ACHOO'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'bloom'), prefer=['curious', 'young'])
    o.r('test_the_water_warmth_with_a_wingtip', 'Testing the water\'s warmth with a wingtip, since the golden koi only comes up for the warm top layer', 18, 'wing',
        [k(.14, 'sheen_m', reach=.4, x=.2, y=.6, b=.3), k(.34, 'sheen_m', reach=1, x=.3, y=1, b=.7, mark='...'), k(.54, 'sheen_r', reach=1, x=.3, y=1.1, b=.8, l=1, eye='-'), k(.74, 'sheen_r', reach=.5, x=.2, y=.6, b=.3, eye='^'), k(.88, eye='^')],
        [], g='test', act=('test', 'warmth'), prefer=['curious', 'warm'])
    # ---------------- rest
    o.r('doze_at_the_stone_in_the_warm_sun', 'Dozing at the right stone with his back to the warm sun while the golden koi slides in and out of the lilies', 28, 'none',
        [k(.14, 'stone_r', x=.2, y=.5, b=.6, w=.3), k(.34, 'stone_r', x=0, y=.9, b=1.2, w=.5, eye='-', mark='zz'), k(.6, 'stone_r', x=-.1, y=1.1, b=1.4, w=.5, l=1, eye='-', mark='zzz'), k(.8, 'stone_r', x=.2, y=.4, b=.4, w=.2, eye='o'), k(.92, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'stone'), when=['tired', 'day'])
    o.r('sit_to_watch_the_sunrise_on_the_pond', 'Sitting at the left stone, wings loose, to watch the sunrise light the pond up gold from the far edge', 26, 'none',
        [k(.14, 'stone_l', x=.5, y=-.2, b=1, w=.2), k(.34, 'stone_l', x=.7, y=-.4, b=1.6, w=.4, eye='-'), k(.6, 'stone_l', x=.7, y=-.5, b=1.7, w=.4, r=1, eye='o', mark='...'), k(.82, 'sheen_l', x=1, y=.3, b=.7, eye='O')],
        [(.6, 'rest')], g='rest', act=('sit', 'stone'), when=['dawn'], prefer=['tired', 'lonely'])
    o.r('lean_on_the_tall_stems_and_dream', 'Leaning against the low reed and dreaming of a fish that was made of actual gold', 20, 'none',
        [k(.14, 'reed_low', x=-.4, y=-.2, b=.5), k(.34, 'reed_low', x=-.7, y=-.4, b=.8, eye='-'), k(.58, 'reed_low', x=-.8, y=-.4, b=.9, l=1, eye='-', mark='...'), k(.8, x=.4, y=.3, b=.3, eye='O'), k(.9, eye='^')],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'sad'])
    o.r('wait_for_the_gold_to_rise', 'Waiting at the rim, still as a post, for the golden koi to rise into the first light', 24, 'none',
        [k(.14, 'sheen_m', x=.9, y=.9, b=.7, eye='o'), k(.4, 'sheen_m', x=1, y=1, b=.9, eye='o'), k(.62, 'sheen_m', x=1, y=1.1, b=.9, r=1, eye='O', mark='...'), k(.8, 'sheen_m', x=.4, y=.5, b=.3, eye='^')],
        [], g='rest', act=('wait', 'gold'), pick='shyest', when=['dawn'], prefer=['lonely', 'curious'], obj=[(.5, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sulk_when_the_gold_stays_down', 'Sulking at the rim because the golden koi has stayed down all morning and shown nothing', 22, 'none',
        [k(.14, x=-.3, y=.2, b=.2, w=.3), k(.34, 'sheen_r', x=-.9, y=.5, b=.5, w=.6, eye='-'), k(.54, 'sheen_r', x=-1, y=.6, b=.6, w=.6, l=1, r=1, eye='-', mark='hmph'), k(.76, x=-.4, y=.2, b=.2, w=.3, eye='-')],
        [], g='rest', act=('sulk', 'rim'), when=['sad'])
    # ---------------- weather
    o.r('crack_the_ice_off_the_gold_run', 'Cracking the ice off the golden koi\'s run with a spray of light bill taps, one pane after the next', 22, 'none',
        [k(.12, 'sheen_l', x=.5, y=.6, b=.3), k(.26, 'sheen_m', x=1.4, y=.8, b=.4, mark='tck'), k(.4, 'sheen_m', x=1.5, y=.9, b=.4, l=1, mark='tck'), k(.54, 'run', x=1.5, y=.9, b=.4, r=1, mark='CRK'), k(.68, 'sheen_r', x=1.4, y=.8, b=.4, mark='tck'), k(.86, eye='^')],
        [(.54, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('brush_the_crust_from_the_left_sheen', 'Brushing the frost crust off the left shallows with a wing so the dawn gold can show on the water again', 18, 'wing',
        [k(.14, 'sheen_l', reach=.4, x=.1, y=.2, w=.3), k(.32, 'sheen_l', reach=1, x=.2, y=.5, b=.3, w=.4, mark='shh'), k(.5, 'sheen_m', reach=1, x=.3, y=.4, b=-.2, w=.6, r=1, mark='shh'), k(.68, 'sheen_m', reach=1, x=.2, y=.3, b=-.1, w=.4), k(.86, eye='^')],
        [(.5, 'thaw')], g='weather', act=('scrape', 'crust'), when=['pond_ice>.3'])
    o.r('flap_the_warm_air_into_the_pond', 'Flapping both wings over the heavy water in broad sweeps to mix warm air down to the golden koi', 22, 'wing',
        [k(.12, 'sheen_m', reach=.4, y=-.4, b=-.6, l=1, r=1), k(.28, 'sheen_m', reach=1, x=.2, y=.6, b=.6, mark='SPLSH'), k(.44, 'sheen_m', reach=.4, y=-.5, b=-.7, l=1, r=1), k(.6, 'run', reach=1, x=.2, y=.6, b=.7, mark='SPLSH'), k(.76, 'sheen_r', reach=1, x=.2, y=.6, b=.7, mark='SPLSH'), k(.9, eye='@')],
        [(.6, 'stir')], g='weather', act=('shake', 'air'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('huddle_out_the_rain_with_wings_wide', 'Huddling out the rain at the grass tuft with wings spread wide like an umbrella over the bill', 30, 'none',
        [k(.14, 'tuft', x=.2, y=.4, b=.5, w=.6), k(.34, 'tuft', x=-.2, y=.8, b=1, w=1, eye='-'), k(.62, 'tuft', x=-.3, y=.9, b=1.1, w=1, r=1, eye='-', mark='drip'), k(.84, 'tuft', x=.3, y=.4, b=.4, w=.5, eye='^')],
        [], g='weather', act=('shelter', 'tuft'), when=['wet'])
    o.r('warm_the_bill_in_the_morning_sun', 'Warming his bill and chest in the first sun at the stone while the water goes from grey to gold', 20, 'none',
        [k(.14, 'stone_l', x=.1, y=-.6, b=.4, w=.4, perch=1), k(.34, 'stone_l', x=.2, y=-.9, b=.6, w=.8, perch=1, eye='-'), k(.58, 'stone_l', x=.2, y=-1, b=.7, w=.9, perch=1, eye='-', mark='ahh'), k(.8, 'stone_l', x=.2, y=-.3, b=.3, w=.3, perch=1, eye='^')],
        [], g='weather', act=('warm', 'bill'), when=['sun'], prefer=['dawn', 'tired'])
    o.r('lean_into_the_wind_by_the_bank', 'Leaning into the wind at the bank, wings clamped, while ripples chase each other across the gold', 18, 'none',
        [k(.14, 'bank_r', x=1.1, y=.1, b=.8, w=.2), k(.32, 'bank_r', x=1.6, y=.2, b=1.3, w=.7, mark='whoo'), k(.5, 'bank_r', x=1.7, y=.3, b=1.5, w=.8, r=1), k(.7, 'bank_r', x=1.3, y=.1, b=.9, w=.4, l=1), k(.86, eye='-')],
        [], g='weather', act=('brace', 'wind'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_rising_gold', 'Bowing grandly to the golden koi as it breaks the surface, one wing sweeping out to the side', 18, 'none',
        [k(.14, 'sheen_r', x=0, y=-.2, w=1), k(.34, 'sheen_r', x=1.2, y=1.4, b=.7, w=1, eye='-'), k(.54, 'sheen_r', x=1.3, y=1.9, b=1.1, w=.4, eye='-', mark='sire'), k(.76, 'sheen_r', x=0, y=-.5, b=-.2, w=.4, eye='^')],
        [], g='show', act=('bow', 'gold'), pick='hungriest', prefer=['happy'], obj=[(.34, dict(lure=1)), (.72, dict(lure=1))], say=["Bowed to a fish with a halo. Totally earned.", "Kowtowed to a koi. It did not pay me. Rude."])
    o.r('present_the_gold_to_the_sun', 'Presenting the golden koi to the sun itself with an upward sweep of the wing, a showman to the sky', 22, 'wing',
        [k(.14, 'sheen_l', reach=.3, x=.1, y=-.4, b=-.3), k(.32, 'sheen_m', reach=1, x=.3, y=-.8, b=-.5, l=1), k(.52, 'sheen_m', reach=1, x=.4, y=-1.1, b=-.7, r=1, mark='BEHOLD'), k(.72, 'sheen_m', reach=1, x=.2, y=-.6, b=-.4), k(.88, eye='^')],
        [], g='show', act=('present', 'koi'), pick='shyest', prefer=['happy'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))])
    o.r('argue_over_which_of_them_shines', 'Arguing with the golden koi about which of them shines brighter, flashing a wing at its flank', 22, 'wing',
        [k(.12, 'sheen_m', reach=.5, x=.9, y=.1, b=.8), k(.28, 'sheen_m', reach=1, x=1.3, y=-.3, b=.3, mark='ME'), k(.44, 'sheen_m', reach=.3, x=.2, y=-.2, b=.2), k(.6, 'sheen_m', reach=1, x=1.4, y=-.3, b=.3, l=1, mark='ME'), k(.78, 'sheen_m', reach=.5, x=.8, y=.2, b=.6), k(.9, eye='-')],
        [], g='show', act=('argue', 'shine'), pick='hungriest', prefer=['grumpy'], obj=[(.28, dict(lure=1)), (.64, dict(lure=1))], say=["It shines on its own. I need a lamp. Unfair.", "Argued with a mirror that has fins. Lost to the mirror."])
    o.r('pose_with_one_wing_gilded', 'Striking a pose at the middle stone with one wing held up gilded in the light, hip out', 20, 'none',
        [k(.14, 'stone_m', x=.1, y=-.4, b=-.1, w=.4, perch=1), k(.34, 'stone_m', x=.3, y=-.8, b=-.4, w=1, l=1, perch=1), k(.56, 'stone_m', x=.4, y=-.9, b=-.5, w=1, r=1, perch=1, eye='^', mark='gilded'), k(.78, 'stone_m', x=.2, y=-.3, b=-.1, w=.4, perch=1)],
        [], g='show', act=('pose', 'wing'), pick='shyest', prefer=['happy'], obj=[(.4, dict(lure=1)), (.8, dict(lure=1))])
    o.r('sing_up_the_dawn_for_the_gold', 'Singing the dawn up for the golden koi, bill raised, a bright flat note at the top of each phrase', 24, 'none',
        [k(.14, 'tuft', x=-.3, y=-.6, b=.3), k(.32, 'sheen_l', x=.2, y=-.9, b=.2, w=.6, eye='O', mark='la'), k(.5, 'sheen_l', x=.3, y=-1.1, b=.1, w=.8, eye='^', mark='LAAA'), k(.68, 'sheen_l', x=.2, y=-.9, b=.2, w=.6, mark='la'), k(.86, 'sheen_l', x=.6, y=.6, b=.5, eye='^')],
        [], g='show', act=('sing', 'dawn'), pick='shyest', when=['dawn'], prefer=['happy', 'lonely'], obj=[(.4, dict(lure=1)), (.75, dict(lure=1))], say=["Sang. It shimmered. We are collaborators.", "A note for the sun. The sun took its time."])
    # ---------------- mishap
    o.r('slip_on_the_dew_wet_rim', 'Slipping on the dew-wet rim stone in a skid of both feet, flapping gold-edged wings to catch the air', 16, 'none',
        [k(.14, 'stone_l', x=.4, y=.4, b=.4, w=.2), k(.28, 'stone_l', x=1.1, y=-.4, b=-.7, l=1, r=1, w=1, mark='whoo'), k(.44, 'stone_l', x=1.3, y=.9, b=1.5, w=.9, eye='O'), k(.64, 'stone_l', x=.7, y=.5, b=.8, w=.3, eye='>'), k(.82, eye='-')],
        [], g='mishap', act=('slip', 'rim'), when=['wet'], prefer=['young'])
    o.r('stuck_in_a_bloom_stem_lunging_for_gold', 'Lunging at the gold with his head through a bloom stem and having to wriggle back out in a slow twist', 24, 'none',
        [k(.14, x=.7, y=.4, b=.5), k(.3, 'bloom_r', x=1.6, y=.1, b=.5, eye='O'), k(.48, 'bloom_r', x=1.7, y=.2, b=.6, r=1, eye='@', mark='mmf'), k(.62, 'bloom_r', x=1.4, y=.1, b=1.3, l=1, mark='mmfff'), k(.76, 'bloom_r', x=.7, y=-.5, b=-.5, w=.9, mark='POP'), k(.9, x=1.1, y=.9, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'bloom'), shown='head', prefer=['young', 'grumpy'])
    o.r('walk_into_the_stem_dazzled', 'Walking blind straight at the low reed, dazzled by a flash off the water, and meeting it bill first', 20, 'none',
        [k(.12, 'sheen_m', x=.2, y=-.6, b=.1, w=.4, r=1), k(.28, 'tuft', x=.3, y=-.5, b=.2, w=.4, l=1), k(.44, 'reed_low', x=1.7, y=-.1, b=1.4, w=.2, eye='@', mark='BONK'), k(.6, 'reed_low', x=-1, y=.4, b=.1, w=.9, eye='x'), k(.84, x=.2, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'reed'), when=['dawn'])
    o.r('hop_back_from_the_gold_flash', 'Hopping back from the rim with one wing over his eyes as the golden koi flashes at the surface', 16, 'none',
        [k(.14, 'sheen_m', x=.9, y=1.3, b=.8), k(.28, 'sheen_m', x=1, y=1.5, b=1, eye='o', mark='...'), k(.4, x=-1.3, y=-.9, b=-1.5, l=1, r=1, w=1, eye='O', mark='AH'), k(.58, x=-.7, y=.1, b=-.1, w=.8, eye='>'), k(.8, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'glare'), pick='hungriest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1))], say=["It flashed. I flinched. It saw.", "Blinded by a fish. Mark it on the wall of shame."])
    o.r('stamp_off_the_spilt_flakes', 'Stamping about the stones after a flake toss goes wild and half of it lands on his own head', 16, 'none',
        [k(.14, 'stone_m', x=.7, y=.9, b=.4), k(.26, 'stone_m', x=.5, y=0, b=-1.2, l=1, w=.7, mark='STMP'), k(.38, 'stone_m', x=.6, y=.5, b=.5, w=.3), k(.5, 'stone_m', x=.5, y=0, b=-1.2, r=1, w=.7, mark='STMP'), k(.68, 'stone_m', x=.8, y=.6, b=.3, eye='>'), k(.86, eye='-')],
        [], g='mishap', act=('stamp', 'flakes'), prefer=['grumpy'])
    # ---------------- duets
    o.r('bounce_the_glint_between_two_wings', 'Tilting a wing to throw a glint to a friend\'s wing across the water, the golden koi leaping to catch each pass', 26, 'wing',
        [k(.12, 'sheen_l', reach=.4, x=.1, y=-.3, b=.1), k(.3, 'sheen_m', reach=1, x=.3, y=-.7, b=-.3), k(.5, 'run', reach=1, x=.5, y=-.9, b=-.5, r=1, mark='flash'), k(.7, 'sheen_r', reach=1, x=.5, y=-.7, b=-.3, l=1), k(.88, eye='^')],
        [(.5, 'glint')], g='play', act=('throw', 'glint'), pick='hungriest', when=['dawn_or_day'], prefer=['happy'], obj=[(.3, dict(lure=1)), (.55, dict(lure=1)), (.75, dict(lure=1))],
        duo=[k(.16, 'sheen_r', reach=.4, x=.1, y=-.3, b=.1), k(.34, 'sheen_r', reach=1, x=.4, y=-.8, b=-.4, mark='flash'), k(.54, 'run', reach=1, x=.5, y=-.9, b=-.5, l=1), k(.74, 'sheen_m', reach=1, x=.4, y=-.7, b=-.3), k(.9, eye='^')],
        say=["Bounced a sunbeam off a pal. Caught on the fish.", "Light, passed hand to hand. Fish took the receipt."])
    o.r('four_wing_polish_down_the_flank', 'Polishing the golden flank from both ends at once with a friend, wing meeting wing at the middle', 26, 'wing',
        [k(.14, 'run', reach=.5, x=1, y=.3, b=.9), k(.32, 'sheen_l', reach=1, x=1.4, y=.5, b=1.6, mark='rub'), k(.52, 'sheen_m', reach=1, x=1.5, y=.6, b=1.8, l=1, mark='rub rub'), k(.72, 'sheen_m', reach=1, x=1.2, y=.4, b=1.3, r=1), k(.88, eye='^')],
        [(.52, 'tend')], g='care', act=('polish', 'flank'), pick='hungriest', when=['fish_health<.9'], prefer=['happy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.16, 'sheen_r', reach=.5, x=.3, y=.8, b=.5), k(.34, 'sheen_r', reach=1, x=.5, y=1.3, b=.9, mark='rub'), k(.54, 'sheen_m', reach=1, x=.6, y=1.5, b=1.1, r=1, mark='rub'), k(.74, 'sheen_m', reach=1, x=.5, y=1.2, b=.8, l=1), k(.9, eye='^')])
    o.r('count_the_gold_rings_in_turn', 'Counting the gold rings the koi leaves on the water with a friend, taking alternate rings, never agreeing', 24, 'none',
        [k(.12, 'sheen_l', x=.6, y=.9, b=.5, mark='1'), k(.3, 'sheen_m', x=.7, y=1, b=.5, mark='3'), k(.48, 'run', x=.7, y=1, b=.5, l=1, mark='5'), k(.66, 'sheen_r', x=.7, y=1, b=.5, r=1, mark='7?'), k(.84, eye='^')],
        [], g='test', act=('count', 'rings'), pick='shyest', when=['shimmer>.4'], prefer=['curious', 'happy'], obj=[(.34, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.14, 'sheen_r', x=.6, y=.9, b=.5), k(.34, 'run', x=.7, y=1, b=.5, mark='2'), k(.52, 'sheen_m', x=.7, y=1, b=.5, r=1, mark='4'), k(.7, 'sheen_l', x=.7, y=1, b=.5, l=1, mark='6'), k(.86, eye='^')],
        say=["Odd for me, even for them, nobody for the koi.", "Seven rings. Eight if you are generous. I am not."])
    return done(o)


def minnow():
    # Minnow: tiny silver fish that live as a school, top water, any hour. The kept minnow stands for the school: it is drawn at the rim spot he touches.
    # Own state: swirl (how tight the school is: herding raises it, a scare breaks it, drawn as a swirl on the water), flakeskin (flakes still floating,
    # drawn).
    o = Obj('minnow', 'keeping', on='koi_pond',
            fields=dict(swirl=(0, 0, 1)),
            physics=[('swirl', 'rate', -.0004, 'always')],
            effects=dict(skim=[('keeping.leaves', 'mul', .4)], thin=[('keeping.plants', 'mul', .75)], scour=[('keeping.algae', 'mul', .5)],
                         film=[('keeping.flakes', 'mul', .3)], rejoin=[('swirl', 'add', .25), ('subject.mood', 'add', .15)],
                         tend=[('subject.health', 'add', .12), ('subject.trust', 'add', .1)], scatter=[('keeping.flakes', 'add', .4)],
                         feed=[('subject.hunger', 'add', -.25), ('subject.trust', 'add', .12)], call=[('keeping.bell', 'add', .5)],
                         herd=[('swirl', 'add', .25), ('subject.trust', 'add', .1)], lead=[('swirl', 'add', .2), ('subject.mood', 'add', .15)],
                         nibble=[('subject.mood', 'add', .15), ('subject.trust', 'add', .1)], burst=[('swirl', 'mul', .3)],
                         crack=[('keeping.ice', 'mul', .3)], thaw=[('keeping.ice', 'mul', .6)], stir=[('keeping.oxygen', 'add', .3)],
                         fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            marks=[('swirl', .3, 'o~o~o', 'swirl_m', 'water'), ('pond_flakes', .3, '.:.:.', 'shoal', 'dust'), ('pond_leaves', .3, ';"~;"', 'cove', 'leaf'), ('pond_ice', .3, '*-*-*', 'swirl_l', 'frost')],
            anchors=dict(swirl_l=P(28, 43), swirl_m=P(58, 41), swirl_r=P(88, 39), shoal=P(70, 43), cove=P(40, 39), tuft=P(11, 44), reed_low=P(8, 38),
                         bank_r=P(95, 40), stone_l=P(30, 46, 'surface'), stone_m=P(41, 46, 'surface'), stone_r=P(86, 46, 'surface')))
    # ---------------- care
    o.r('lift_the_leaves_out_of_the_school_lane', 'Lifting the drifted leaves out of the narrow lane the school swims in, leaf after leaf with a reed', 22, 'reed',
        [k(.1, 'swirl_r', reach=.5, x=.2, y=.2, b=.2, l=1), k(.24, 'shoal', reach=1, x=.4, y=.4, b=.4, mark='sh'), k(.38, 'swirl_m', reach=1, x=.4, y=.4, b=-.2, r=1, mark='sh'), k(.52, 'cove', reach=1, x=.4, y=.4, b=.4, l=1, mark='sh'), k(.7, 'swirl_l', reach=.8, x=.3, y=.3, b=.2), k(.88, eye='^')],
        [(.38, 'skim')], g='care', act=('scoop', 'leaves'), when=['pond_leaves>.3'], prefer=['windy'], say=["Leaves out. The school wheeled past like I'd done them a favour.", "Twelve leaves, one reed. A very small victory."])
    o.r('rub_the_algae_off_the_nursery_stone', 'Rubbing the algae off the left stone where the minnows graze in the shallows, quick short strokes', 18, 'wing',
        [k(.1, 'stone_l', reach=.5, x=.5, y=.6, b=.2), k(.22, 'stone_l', reach=1, x=.8, y=1, b=.5, l=1, mark='sk'), k(.34, 'stone_l', reach=1, x=.9, y=1.1, b=.6, r=1, mark='sk'), k(.46, 'stone_l', reach=1, x=.8, y=1, b=.5, l=1, mark='sk'), k(.62, 'stone_l', reach=1, x=.7, y=.9, b=.4), k(.86, eye='^')],
        [(.46, 'scour')], g='care', act=('scrub', 'algae'), when=['pond_algae>.4'])
    o.r('pull_the_weed_back_so_the_school_can_turn', 'Pulling a thick weed bed back off the cove with a twig so the school has room to turn', 22, 'twig',
        [k(.12, 'cove', reach=.5, x=.4, y=.2, b=.3), k(.3, 'cove', reach=1, x=.7, y=.4, b=.7, mark='hnk'), k(.46, 'swirl_m', reach=1, x=.9, y=.5, b=.9, l=1), k(.62, 'cove', reach=1, x=-.1, y=-.4, b=-.3, w=.4, mark='pop'), k(.84, eye='-')],
        [(.46, 'thin')], g='care', act=('pull', 'weed'), when=['pond_plants>.7'])
    o.r('sweep_the_flake_scum_off_the_shoal', 'Sweeping the scum of old flakes off the shoal with a wing, before it sours the school\'s water', 18, 'wing',
        [k(.1, 'shoal', reach=.5, x=.3, y=.8, b=.3), k(.24, 'shoal', reach=1, x=.6, y=1.2, b=.7, mark='sh'), k(.4, 'swirl_r', reach=1, x=.7, y=1.3, b=.9, l=1, mark='sh'), k(.56, 'swirl_m', reach=1, x=.5, y=1.2, b=.7, r=1), k(.76, eye='-')],
        [(.4, 'film')], g='care', act=('sweep', 'scum'), when=['pond_flakes>.3'])
    o.r('shoo_the_stray_back_to_the_shoal', 'Shooing a straggling minnow back to the others with small flicks of a wing, left to right', 22, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.26, 'swirl_l', reach=1, x=.5, y=.7, b=.5, l=1, mark='shoo'), k(.42, 'swirl_m', reach=1, x=.5, y=.7, b=.5, r=1, mark='shoo'), k(.58, 'shoal', reach=1, x=.5, y=.7, b=.5, l=1, mark='shoo'), k(.76, 'shoal', reach=.5, x=.3, y=.4, b=.3), k(.9, eye='^')],
        [(.58, 'rejoin')], g='care', act=('nudge', 'stray'), pick='shyest', when=['swirl<.5'], obj=[(.2, dict(lure=1)), (.4, dict(lure=1)), (.6, dict(lure=1)), (.8, dict(lure=1))],
        say=["Back with the others. It clearly has no plans.", "Herded a fish one inch. Sheepdog duck."])
    o.r('free_a_minnow_caught_in_the_weed', 'Freeing a minnow caught in a weed strand with the very tip of his bill, a peck and a gentle pull', 22, 'none',
        [k(.1, x=.4, y=.4, b=.3), k(.24, 'swirl_l', x=1, y=1.3, b=.6, eye='-'), k(.38, 'swirl_l', x=1.2, y=1.6, b=.9, l=1, mark='nip'), k(.52, 'swirl_l', x=1.3, y=1.7, b=1, r=1, mark='tug'), k(.68, 'swirl_l', x=.6, y=.8, b=.4, w=.4, mark='plip'), k(.86, eye='^')],
        [(.52, 'tend')], g='care', act=('unwrap', 'minnow'), pick='shyest', when=['fish_health<.8'], obj=[(.22, dict(lure=1)), (.6, dict(lure=1))])
    # ---------------- use
    o.r('pinch_out_flakes_for_the_whole_school', 'Pinching a few flakes out over the water in little pinches so the whole school bunches round them', 16, 'wing',
        [k(.12, 'swirl_m', reach=.5, w=.2), k(.26, 'swirl_m', reach=1, y=-.2, b=-.2, mark='tss'), k(.4, 'shoal', reach=1, y=-.2, b=-.2, mark='tss'), k(.58, x=.1, y=.1, eye='o'), k(.82, eye='^')],
        [(.4, 'scatter')], g='use', act=('throw', 'flakes'), when=['pond_flakes<.3'], prefer=['dawn', 'dusk'])
    o.r('feed_crumbs_one_at_a_time', 'Feeding crumbs one at a time into the water, each one vanishing into a different mouth', 22, 'none',
        [k(.1, x=.3, y=.3, b=.3), k(.22, 'swirl_r', x=1, y=1, b=.6, mark='plip'), k(.34, 'swirl_r', x=1, y=1.1, b=.6, l=1, mark='plip'), k(.46, 'swirl_m', x=1.1, y=1.2, b=.7, mark='plip plip'), k(.58, 'swirl_m', x=1.1, y=1.2, b=.7, eye='O', mark='gone'), k(.76, 'swirl_m', x=.5, y=.5, b=.3, w=.3, eye='^')],
        [(.46, 'feed')], g='use', act=('carry', 'crumb'), pick='hungriest', when=['fish_hunger>.4'], obj=[(.24, dict(lure=1)), (.52, dict(lure=1)), (.7, dict(lure=0))],
        say=["Crumb in, crumb gone. Seven mouths, one bill.", "Fed a school with a bill. Tiny logistics, huge ego."])
    o.r('rattle_the_stone_in_quick_taps', 'Rattling the right stone in quick light taps so the school bolts to the sound of supper', 14, 'none',
        [k(.1, 'stone_r', x=1, y=1.1, b=.4, mark='tk'), k(.2, 'stone_r', x=1.1, y=1.2, b=.4, l=1, mark='tk'), k(.3, 'stone_r', x=1, y=1.1, b=.4, r=1, mark='tk'), k(.4, 'stone_r', x=1.1, y=1.2, b=.4, l=1, mark='tk'), k(.56, 'stone_r', x=1.2, y=1.3, b=.5, r=1, mark='TKTK'), k(.8, eye='^')],
        [(.56, 'call')], g='use', act=('knock', 'stone'), when=['pond_bell<.4'], prefer=['dusk'])
    o.r('ribbon_the_school_behind_a_wingtip', 'Trailing a wingtip in a loose figure of eight so the school ribbons after it, tight as a scarf', 24, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.24, 'swirl_m', reach=1, x=.5, y=.6, b=.5, l=1), k(.38, 'shoal', reach=1, x=.6, y=.6, b=.5, r=1), k(.52, 'swirl_r', reach=1, x=.6, y=.6, b=.5, l=1), k(.66, 'shoal', reach=1, x=.5, y=.6, b=.5, r=1), k(.8, 'swirl_m', reach=.6, x=.3, y=.4, b=.3), k(.92, eye='^')],
        [(.52, 'lead')], g='use', act=('drag', 'wingtip'), pick='hungriest', when=['swirl<.7'], obj=[(.12, dict(lure=1)), (.28, dict(lure=1)), (.45, dict(lure=1)), (.62, dict(lure=1)), (.78, dict(lure=1))],
        say=["Ribboned a school. It wore me like a scarf.", "A figure of eight, drawn by a duck, finished by a hundred fish."])
    o.r('drum_the_surface_in_a_slow_pulse', 'Drumming a slow pulse on the water with a wingtip so the school beats open and shut in answer', 22, 'wing',
        [k(.1, 'swirl_m', reach=.5, x=.3, y=.4, b=.4), k(.24, 'swirl_m', reach=1, x=.4, y=.7, b=.7, mark='pum'), k(.36, 'swirl_m', reach=.4, x=.3, y=.3, b=.3), k(.5, 'swirl_m', reach=1, x=.4, y=.7, b=.7, mark='pum'), k(.62, 'swirl_m', reach=.4, x=.3, y=.3, b=.3), k(.76, 'swirl_m', reach=1, x=.4, y=.7, b=.7, mark='PUM'), k(.9, eye='^')],
        [(.5, 'herd')], g='use', act=('drum', 'surface'), pick='shyest', when=['swirl<.7'], prefer=['happy', 'young'], obj=[(.26, dict(lure=1)), (.5, dict(lure=1)), (.78, dict(lure=1))])
    o.r('dangle_a_toe_for_the_nibblers', 'Dangling a toe at the left stone until the minnows nibble it, then trying hard not to giggle', 20, 'none',
        [k(.1, 'stone_l', x=.2, y=.3, b=.7, l=1), k(.24, 'stone_l', x=.3, y=.6, b=1, l=1, mark='...'), k(.4, 'swirl_l', x=.4, y=.9, b=1.2, l=1, eye='O', mark='tickle'), k(.52, 'swirl_l', x=.4, y=.9, b=1.3, l=1, eye='>', mark='hee'), k(.68, 'swirl_l', x=.3, y=.7, b=1, l=1, eye='-'), k(.86, eye='^')],
        [(.4, 'nibble')], g='use', act=('tap', 'toe'), pick='hungriest', prefer=['happy', 'young'], obj=[(.28, dict(lure=1)), (.6, dict(lure=1))], say=["They nibble. I giggle. Neither party admits anything.", "A toe is the best flake. Said the school."])
    o.r('stir_a_reed_round_in_a_whirl', 'Stirring a reed round and round in the water until the school is spinning in one bright whirl', 24, 'reed',
        [k(.1, 'swirl_r', reach=.5, x=.3, y=.4, b=.3), k(.24, 'shoal', reach=1, x=.5, y=.5, b=.5, l=1, mark='swrl'), k(.38, 'swirl_m', reach=1, x=.5, y=.5, b=.5, r=1, mark='swrl'), k(.52, 'cove', reach=1, x=.5, y=.5, b=.5, l=1, mark='swrl'), k(.66, 'swirl_m', reach=1, x=.5, y=.5, b=.5, r=1, mark='swrl'), k(.82, eye='@')],
        [(.52, 'herd')], g='use', act=('spin', 'swirl'), pick='hungriest', when=['swirl<.7'], prefer=['curious'], obj=[(.28, dict(lure=1)), (.55, dict(lure=1)), (.8, dict(lure=1))])
    # ---------------- play
    o.r('chase_the_school_down_the_rim', 'Chasing the school along the rim in bounds, bill snapping after the back of the pack', 18, 'none',
        [k(.08, 'swirl_l', x=.5, y=.5, b=-.4, l=1), k(.2, 'cove', x=.8, y=.6, b=-.5, r=1, w=.5), k(.32, 'swirl_m', x=1, y=.6, b=-.5, l=1, w=.6, mark='snp'), k(.44, 'shoal', x=1.1, y=.6, b=-.5, r=1, w=.6), k(.58, 'swirl_r', x=1.2, y=.6, b=-.5, l=1, w=.6, mark='snp'), k(.78, 'bank_r', x=.3, y=.4, b=.3, eye='@')],
        [(.44, 'fun')], g='play', act=('chase', 'school'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.3, dict(lure=1)), (.46, dict(lure=1)), (.62, dict(lure=1))],
        say=["Never caught one. They move as one thought, a mean one.", "Chased silver. Got wet air. Fine day."])
    o.r('slap_the_water_and_watch_it_burst', 'Slapping the water flat with a wing and watching the tight school burst out like a firework', 16, 'wing',
        [k(.12, 'swirl_m', reach=.5, x=.3, y=.3, b=.4), k(.26, 'swirl_m', reach=1, x=.4, y=.3, b=-.8, mark='SLAP'), k(.4, 'swirl_m', reach=.3, x=-.3, y=-.3, b=-.5, eye='O', mark='pssh'), k(.56, 'shoal', reach=.3, x=-.2, y=-.2, b=-.3), k(.74, 'swirl_r', reach=.5, x=.3, y=.3, b=.2, eye='@'), k(.88, eye='^')],
        [(.26, 'burst')], g='play', act=('splash', 'school'), when=['swirl>.3'], prefer=['young', 'happy'])
    o.r('twirl_with_the_swirl', 'Twirling at the rim in time with the school\'s own swirl, a step to every turn of the silver', 22, 'none',
        [k(.1, 'swirl_l', x=.3, y=.3, b=.4, l=1, w=.4), k(.24, 'swirl_m', x=-.4, y=.3, b=-.4, r=1, w=.7), k(.38, 'swirl_m', x=.4, y=.3, b=.4, l=1, w=.7, mark='la'), k(.52, 'shoal', x=-.4, y=.3, b=-.4, r=1, w=.7), k(.66, 'swirl_r', x=.4, y=.3, b=.4, l=1, w=.6), k(.82, 'swirl_r', x=0, y=.3, b=.2, eye='^')],
        [], g='play', act=('dance', 'swirl'), pick='hungriest', when=['swirl>.3'], prefer=['happy', 'young'], obj=[(.14, dict(lure=1)), (.4, dict(lure=1)), (.66, dict(lure=1))])
    o.r('seek_the_one_that_hides_in_the_shoal', 'Seeking the one minnow that has hidden in the shoal, a bill on each flash until it gives itself away', 22, 'none',
        [k(.1, 'shoal', x=.7, y=.7, b=.5, eye='o'), k(.24, 'swirl_m', x=.8, y=.9, b=.6, eye='o', mark='that one?'), k(.4, 'swirl_r', x=.9, y=1, b=.7, l=1, eye='O', mark='no'), k(.56, 'cove', x=.9, y=1, b=.7, r=1, eye='o', mark='that?'), k(.72, 'swirl_l', x=1, y=1.1, b=.8, eye='O', mark='YES'), k(.88, eye='^')],
        [], g='play', act=('seek', 'minnow'), pick='shyest', prefer=['young', 'curious'], obj=[(.28, dict(lure=1)), (.5, dict(lure=1)), (.75, dict(lure=1))])
    o.r('race_the_shoal_with_hopping_feet', 'Racing the shoal from stone to stone on hopping feet, always a step short of the silver', 18, 'none',
        [k(.08, 'stone_l', x=.5, y=.1, b=-.8, l=1, w=.4), k(.2, 'stone_m', x=.7, y=.1, b=-.9, r=1, w=.6), k(.34, 'stone_m', x=.9, y=.1, b=-1, l=1, w=.7, mark='hup'), k(.5, 'stone_r', x=1.1, y=.1, b=-1, r=1, w=.7), k(.66, 'stone_r', x=1.1, y=.1, b=-1, l=1, w=.7, mark='hup'), k(.84, 'stone_r', x=.3, y=.3, b=.4, eye='@')],
        [], g='play', act=('race', 'shoal'), pick='hungriest', prefer=['young', 'happy'], obj=[(.14, dict(lure=1)), (.34, dict(lure=1)), (.54, dict(lure=1)), (.7, dict(lure=1))])
    o.r('puff_a_curtain_of_bubbles', 'Puffing a curtain of tiny bubbles into the water so the school weaves in and out of it', 18, 'none',
        [k(.1, x=.3, y=.4, b=.3), k(.22, 'swirl_r', x=1, y=1.4, b=.8, mark='bl'), k(.34, 'shoal', x=1.1, y=1.5, b=.9, l=1, eye='-', mark='bl bl'), k(.46, 'swirl_m', x=1.2, y=1.6, b=1, r=1, mark='bl bl bl'), k(.6, 'cove', x=1.1, y=1.5, b=.9, l=1, mark='bl bl'), k(.78, 'cove', x=.7, y=.9, b=.5, eye='O'), k(.9, eye='^')],
        [], g='play', act=('blow', 'bubbles'), pick='shyest', prefer=['young', 'happy'], obj=[(.26, dict(lure=1)), (.5, dict(lure=1)), (.72, dict(lure=1))])
    o.r('steer_a_leaf_through_the_shoal', 'Steering a leaf through the shoal with a reed, the school parting round it and closing up again', 24, 'reed',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.3, b=.3), k(.26, 'cove', reach=1, x=.5, y=.5, b=.5, mark='fwp'), k(.42, 'swirl_m', reach=1, x=.6, y=.6, b=.6, l=1, mark='fwp'), k(.58, 'shoal', reach=1, x=.6, y=.6, b=.6, r=1, mark='fwp'), k(.74, 'swirl_r', reach=1, x=.6, y=.6, b=.6, l=1), k(.9, eye='o')],
        [], g='play', act=('float', 'leaf'), pick='hungriest', when=['pond_leaves>.2'], prefer=['curious'], obj=[(.4, dict(lure=1)), (.62, dict(lure=1)), (.8, dict(lure=1))])
    # ---------------- test
    o.r('count_the_school_by_sixes', 'Counting the school in sixes with a tap of the bill on the water, then giving up and starting over', 24, 'none',
        [k(.1, 'swirl_l', x=.8, y=1, b=.5, mark='6'), k(.22, 'swirl_m', x=.9, y=1.1, b=.6, l=1, mark='12'), k(.36, 'swirl_m', x=.9, y=1.1, b=.6, r=1, mark='18'), k(.5, 'shoal', x=1, y=1.2, b=.7, l=1, mark='2?'), k(.64, 'shoal', x=1, y=1.2, b=.7, eye='>', mark='again'), k(.82, eye='-')],
        [], g='test', act=('count', 'minnows'), pick='hungriest', prefer=['curious'], obj=[(.26, dict(lure=1)), (.56, dict(lure=1))], say=["Eleven. Twenty. Nineteen. It will not hold still for a number.", "Counted sixes, lost the sixth, started the whole job over."])
    o.r('measure_the_length_of_the_whole_school', 'Measuring the length of the whole school end to end with a reed laid across the water', 24, 'reed',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.28, 'swirl_l', reach=1, x=.5, y=.6, b=.5), k(.46, 'shoal', reach=1, x=.7, y=.7, b=.7, l=1, mark='hm'), k(.64, 'swirl_r', reach=1, x=.7, y=.7, b=.7, r=1), k(.84, eye='-', mark='long')],
        [], g='test', act=('measure', 'school'), prefer=['curious'], when=['swirl>.3'])
    o.r('peer_close_at_a_silver_flank', 'Peering close at one silver flank, trying to find the one stripe all of them seem to share', 18, 'none',
        [k(.1, x=.4, y=.6, b=.4), k(.26, 'swirl_m', x=1, y=1.7, b=1, eye='o'), k(.42, 'swirl_m', x=1.1, y=2, b=1.2, eye='@', mark='...'), k(.58, 'swirl_m', x=.5, y=.9, b=.6, eye='-'), k(.76, 'swirl_m', x=1, y=1.8, b=1.1, eye='o', mark='hm'), k(.9, eye='-')],
        [], g='test', act=('peer', 'flank'), pick='shyest', prefer=['curious', 'young'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))])
    o.r('listen_for_the_flick_of_a_thousand_fins', 'Listening at the water for the tiny flick of a thousand fins turning together', 20, 'none',
        [k(.1, 'swirl_r', x=-.3, y=.8, b=.4), k(.28, 'swirl_r', x=-.5, y=1.2, b=.8, eye='-'), k(.46, 'swirl_r', x=-.6, y=1.3, b=.9, l=1, eye='-', mark='...'), k(.62, 'swirl_r', x=-.6, y=1.3, b=.9, r=1, eye='-', mark='tick'), k(.8, 'swirl_r', x=.5, y=.4, b=.3, eye='O'), k(.92, eye='^')],
        [], g='test', act=('listen', 'flicks'), prefer=['curious', 'lonely'])
    o.r('compare_the_silver_to_the_sky', 'Comparing the silver of the school with the sky, a wing held up to each in turn', 20, 'wing',
        [k(.1, 'swirl_m', reach=.4, x=.2, y=.4, b=.3), k(.26, 'swirl_m', reach=1, x=.3, y=-.7, b=-.2, mark='sky'), k(.44, 'swirl_m', reach=1, x=.5, y=.9, b=.6, l=1, mark='fish'), k(.6, 'swirl_m', reach=1, x=.3, y=-.7, b=-.2, mark='sky'), k(.78, 'swirl_m', reach=.6, x=.4, y=.8, b=.5, r=1, eye='-', mark='fish'), k(.9, eye='-')],
        [], g='test', act=('compare', 'silver'), prefer=['curious', 'sun'])
    o.r('sniff_the_cloud_of_flake_dust', 'Sniffing the cloud of flake dust the school churns up and sneezing it back at them', 16, 'none',
        [k(.1, 'shoal', x=.4, y=.7, b=.3), k(.26, 'shoal', x=1.1, y=1.5, b=.9, mark='snf'), k(.42, 'shoal', x=1.2, y=1.7, b=1, eye='-', mark='snf'), k(.58, x=-.9, y=-.5, b=-.4, w=.7, eye='>', mark='ACHOO'), k(.76, 'swirl_r', x=.5, y=.8, b=.3, eye='O'), k(.9, eye='-')],
        [], g='test', act=('sniff', 'dust'), when=['pond_flakes>.3'], prefer=['curious', 'young'])
    o.r('test_how_shallow_the_nursery_runs', 'Testing how shallow the nursery water runs with a reed, three plunges in a row at the left rim', 20, 'reed',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.24, 'swirl_l', reach=1, x=.5, y=.8, b=.7, mark='plk'), k(.38, 'swirl_l', reach=.4, x=.3, y=.3, b=.3), k(.5, 'swirl_l', reach=1, x=.5, y=.9, b=.8, mark='plk'), k(.62, 'swirl_l', reach=.4, x=.3, y=.3, b=.3), k(.76, 'swirl_l', reach=1, x=.6, y=1, b=.9, mark='PLK'), k(.9, eye='o')],
        [], g='test', act=('test', 'shallows'), prefer=['curious'])
    # ---------------- rest
    o.r('nap_at_the_tuft_to_the_flicker', 'Napping at the grass tuft to the flicker of the school in the corner of one half-open eye', 26, 'none',
        [k(.1, 'tuft', x=.1, y=.4, b=.5, eye='-'), k(.28, 'tuft', x=-.2, y=.7, b=1, w=.2, eye='-', mark='zz'), k(.48, 'tuft', x=-.3, y=.9, b=1.1, w=.3, eye='o'), k(.64, 'tuft', x=-.4, y=1, b=1.2, w=.2, eye='-', mark='zzz'), k(.82, 'tuft', x=0, y=.3, b=.3, eye='^')],
        [(.64, 'rest')], g='rest', act=('nap', 'tuft'), when=['tired'])
    o.r('sit_at_the_stone_and_watch_it_wheel', 'Sitting at the middle stone and watching the school wheel round and round until his eyes go in circles', 24, 'none',
        [k(.1, 'stone_m', x=.3, y=.3, b=1), k(.26, 'stone_m', x=.5, y=.3, b=1.4, l=1, eye='o'), k(.42, 'stone_m', x=-.5, y=.3, b=1.4, r=1, eye='o'), k(.58, 'stone_m', x=.5, y=.3, b=1.4, l=1, eye='@', mark='...'), k(.76, 'swirl_m', x=1, y=.5, b=.7, eye='@')],
        [(.58, 'rest')], g='rest', act=('sit', 'stone'), prefer=['tired', 'lonely'])
    o.r('lean_on_the_reed_with_the_school_passing', 'Leaning his shoulder to the low reed while the school passes in front of him once, then once more', 20, 'none',
        [k(.1, 'reed_low', x=-.3, y=.1, b=.5), k(.26, 'reed_low', x=-.5, y=.3, b=.8, eye='-'), k(.42, 'reed_low', x=-.6, y=.3, b=.9, l=1, eye='o'), k(.58, 'reed_low', x=-.6, y=.3, b=.9, r=1, eye='-', mark='...'), k(.8, x=.3, y=.3, b=.3, eye='O')],
        [], g='rest', act=('lean', 'reed'), prefer=['tired', 'sad'])
    o.r('wait_for_the_school_to_return', 'Waiting at the rim for the school to come back round the cove after a scare', 22, 'none',
        [k(.1, 'cove', x=.5, y=.9, b=.6, eye='o'), k(.3, 'cove', x=.5, y=.9, b=.6, eye='o'), k(.5, 'swirl_m', x=.6, y=1, b=.7, l=1, eye='O', mark='...'), k(.7, 'swirl_m', x=.6, y=1, b=.7, r=1, eye='O'), k(.86, 'swirl_m', x=.2, y=.4, b=.3, eye='^')],
        [], g='rest', act=('wait', 'school'), pick='shyest', when=['swirl<.5'], prefer=['lonely', 'curious'], obj=[(.55, dict(lure=1)), (.82, dict(lure=1))])
    o.r('sulk_when_it_scatters_again', 'Sulking at the empty water because the school scatters every time he leans out to say hello', 22, 'none',
        [k(.1, x=-.3, y=.2, b=.3), k(.26, 'swirl_r', x=-.8, y=.5, b=.6, w=.4, eye='-'), k(.44, 'swirl_r', x=-.9, y=.6, b=.7, w=.5, l=1, eye='-', mark='hmph'), k(.6, 'swirl_r', x=-1, y=.6, b=.7, w=.5, r=1, eye='-'), k(.8, x=-.4, y=.2, b=.3, eye='-')],
        [], g='rest', act=('sulk', 'school'), when=['sad'])
    # ---------------- weather
    o.r('stab_a_gap_in_the_ice_for_the_school', 'Stabbing a gap in the ice with short sharp pecks so the school has somewhere to rise', 20, 'none',
        [k(.1, 'swirl_l', x=.7, y=.7, b=.4), k(.2, 'cove', x=1.4, y=1.2, b=.8, mark='pk'), k(.3, 'cove', x=1.5, y=1.3, b=.9, l=1, mark='pk'), k(.4, 'cove', x=1.5, y=1.3, b=.9, r=1, mark='PK'), k(.52, 'swirl_m', x=1.5, y=1.3, b=.9, l=1, mark='pk'), k(.66, 'swirl_m', x=1.4, y=1.2, b=.8, mark='CRK'), k(.84, eye='^')],
        [(.66, 'crack')], g='weather', act=('chip', 'ice'), when=['pond_ice>.3'])
    o.r('flick_the_frost_off_the_nursery_rim', 'Flicking the frost crust off the nursery rim in quick brushes of a wing so it does not trap the fry', 16, 'wing',
        [k(.1, 'swirl_l', reach=.4, x=.2, y=.6, b=.3), k(.24, 'swirl_l', reach=1, x=.4, y=.9, b=.6, mark='fk'), k(.38, 'swirl_l', reach=1, x=.4, y=1, b=.7, l=1, mark='fk'), k(.52, 'swirl_l', reach=1, x=.4, y=1, b=.7, r=1, mark='fk'), k(.7, 'swirl_l', reach=.6, x=.3, y=.8, b=.5), k(.86, eye='-')],
        [(.52, 'thaw')], g='weather', act=('wipe', 'frost'), when=['pond_ice>.3'])
    o.r('thrash_the_still_water_for_air', 'Thrashing the still water with both wings to give the packed school air, a wild flurry', 18, 'wing',
        [k(.1, 'swirl_m', reach=.4, y=-.4, b=-.7, l=1, r=1), k(.22, 'swirl_m', reach=1, x=.3, y=.7, b=.8, mark='SPLSH'), k(.34, 'shoal', reach=.4, y=-.4, b=-.7, l=1), k(.46, 'shoal', reach=1, x=.3, y=.7, b=.8, mark='SPLSH'), k(.58, 'swirl_r', reach=.4, y=-.4, b=-.7, r=1), k(.7, 'swirl_r', reach=1, x=.3, y=.7, b=.8, mark='SPLSH'), k(.86, eye='@')],
        [(.46, 'stir')], g='weather', act=('shake', 'water'), when=['pond_oxygen<.5'], prefer=['summer'])
    o.r('curl_up_out_of_the_rain_at_the_stone', 'Curling up out of the rain at the right stone with his bill under a wing, the school pocking the surface', 30, 'none',
        [k(.1, 'stone_r', x=.2, y=.3, b=.7, perch=1), k(.3, 'stone_r', x=-.2, y=.8, b=1.4, w=.6, eye='-', perch=1), k(.58, 'stone_r', x=-.3, y=1, b=1.6, w=.8, r=1, eye='-', mark='drip', perch=1), k(.82, 'stone_r', x=.3, y=.4, b=.5, w=.3, eye='^', perch=1)],
        [], g='weather', act=('shelter', 'stone'), when=['wet'])
    o.r('squint_the_glare_off_the_silver', 'Squinting at the glare off the school\'s silver and shading his eyes with a wing', 18, 'wing',
        [k(.1, 'swirl_m', reach=.4, x=.2, y=.3, b=.3), k(.26, 'swirl_m', reach=1, x=.1, y=-.5, b=.2, eye='>'), k(.44, 'swirl_m', reach=1, x=.2, y=-.6, b=.3, l=1, eye='>', mark='ow'), k(.62, 'swirl_m', reach=1, x=.2, y=-.5, b=.2, r=1, eye='-'), k(.8, eye='^')],
        [], g='weather', act=('cool', 'eyes'), when=['sun'], prefer=['happy'])
    o.r('crouch_against_the_gale_at_the_bank', 'Crouching against the gale at the bank so the school can wait out the chop in the lee of him', 18, 'none',
        [k(.1, 'bank_r', x=.6, y=.3, b=.8), k(.24, 'bank_r', x=1, y=.4, b=1.4, w=.7, mark='whoo'), k(.4, 'bank_r', x=1.1, y=.4, b=1.6, w=.9, l=1), k(.56, 'bank_r', x=1.1, y=.4, b=1.6, w=.9, r=1), k(.74, 'bank_r', x=.8, y=.3, b=1, w=.4), k(.88, eye='-')],
        [], g='weather', act=('brace', 'gale'), when=['windy'])
    # ---------------- show
    o.r('bow_to_the_school_in_unison', 'Bowing to the school in a quick series, one dip per wheel of the silver', 16, 'none',
        [k(.1, 'swirl_m', x=.3, y=.7, b=.5), k(.22, 'swirl_m', x=.9, y=1.7, b=1.1, eye='-'), k(.34, 'swirl_m', x=.2, y=.2, b=.1), k(.46, 'swirl_m', x=.9, y=1.7, b=1.1, eye='-', mark='sirs'), k(.58, 'swirl_m', x=.2, y=.2, b=.1), k(.7, 'swirl_m', x=.9, y=1.7, b=1.1, eye='-'), k(.86, eye='^')],
        [], g='show', act=('bow', 'school'), pick='hungriest', prefer=['happy'], obj=[(.24, dict(lure=1)), (.48, dict(lure=1)), (.72, dict(lure=1))], say=["Bowed three times. The school bowed once, for all of them.", "Honoured a crowd of fish. I deserve a medal. A flake."])
    o.r('present_the_school_as_one_fish', 'Presenting the school to the bank as one very large fish with a long wing sweep', 20, 'wing',
        [k(.1, 'swirl_l', reach=.3, x=.3, y=-.2, b=.2), k(.26, 'swirl_m', reach=1, x=.3, y=-.4, b=-.3, l=1), k(.42, 'shoal', reach=1, x=.4, y=-.5, b=-.4, r=1, mark='ONE'), k(.58, 'swirl_r', reach=1, x=.4, y=-.5, b=-.4, l=1), k(.76, 'swirl_r', reach=.6, x=.2, y=-.2, b=.1), k(.9, eye='^')],
        [], g='show', act=('present', 'shoal'), pick='shyest', when=['swirl>.3'], prefer=['happy'], obj=[(.3, dict(lure=1)), (.6, dict(lure=1))])
    o.r('argue_with_a_whole_school', 'Arguing with the whole school at once, a bill-jab at every one that dares to flick back', 20, 'none',
        [k(.1, 'swirl_m', x=.8, y=.4, b=.5), k(.24, 'swirl_m', x=1.2, y=.4, b=.3, mark='HEY'), k(.34, 'swirl_r', x=1.3, y=.3, b=.3, r=1, mark='YOU'), k(.46, 'swirl_l', x=1.3, y=.3, b=.3, l=1, mark='AND YOU'), k(.62, 'swirl_m', x=1.2, y=.4, b=.3, mark='ALL OF YOU'), k(.8, 'swirl_m', x=.6, y=.5, b=.4), k(.9, eye='-')],
        [], g='show', act=('argue', 'school'), pick='hungriest', prefer=['grumpy'], obj=[(.26, dict(lure=1)), (.64, dict(lure=1))], say=["Fifty of them, one of me. Naturally I won.", "It turned as one and left. Argument ended by exit."])
    o.r('pose_in_the_swirl_like_a_sculpture', 'Posing at the left stone with a wing extended and one foot up, the school wheeling round him like a sculpture', 20, 'none',
        [k(.1, 'stone_l', x=.1, y=-.2, w=.4, perch=1), k(.26, 'stone_l', x=.4, y=-.5, b=-.2, w=.9, l=1, perch=1), k(.46, 'stone_l', x=.5, y=-.6, b=-.3, w=1, l=1, perch=1, eye='^', mark='art'), k(.66, 'stone_l', x=.3, y=-.3, b=-.1, w=.7, r=1, perch=1), k(.84, 'stone_l', perch=1)],
        [], g='show', act=('pose', 'sculpture'), pick='shyest', when=['swirl>.3'], prefer=['happy'], obj=[(.3, dict(lure=1)), (.7, dict(lure=1))])
    o.r('shout_the_count_at_the_cattails', 'Shouting the count of the school across to the cattails, then changing it as they turn', 18, 'wing',
        [k(.1, 'bank_r', reach=.4, x=.3, y=-.1, b=.3), k(.24, 'bank_r', reach=1, x=.6, y=-.4, b=-.3, mark='FORTY'), k(.4, 'bank_r', reach=1, x=.6, y=-.4, b=-.3, l=1, mark='FIFTY'), k(.56, 'bank_r', reach=1, x=.6, y=-.4, b=-.3, r=1, mark='SEVENTY'), k(.74, 'bank_r', reach=.5, x=.3, y=0, b=.2), k(.88, eye='^')],
        [], g='show', act=('shout', 'count'), prefer=['happy', 'young'], say=["Counted out loud. The school inflated its own numbers.", "Told the cattails: more fish than reeds. They did not argue."])
    # ---------------- mishap
    o.r('slip_on_the_wet_stone_chasing_silver', 'Slipping on the wet stone while chasing silver, feet scrabbling as he skates to a stop in a splash', 16, 'none',
        [k(.1, 'stone_m', x=.7, y=.6, b=.3), k(.22, 'stone_m', x=1.3, y=-.4, b=-.6, l=1, w=.5, mark='whoa'), k(.34, 'stone_m', x=1.5, y=.4, b=1, r=1, w=.9, mark='skrr'), k(.5, 'stone_m', x=1.6, y=1, b=1.7, w=.8, eye='O', mark='SPLOSH'), k(.7, 'stone_m', x=.9, y=.7, b=.8, eye='>'), k(.86, eye='-')],
        [], g='mishap', act=('slip', 'stone'), when=['wet'], prefer=['young'])
    o.r('bill_wedged_between_two_stems', 'Wedging his bill between two reed stems after a straggler and pulling free with a twang', 22, 'none',
        [k(.1, x=.8, y=.4, b=.4), k(.24, 'reed_low', x=1.6, y=.2, b=.4, eye='O'), k(.4, 'reed_low', x=1.7, y=.3, b=.5, l=1, eye='@', mark='mm'), k(.54, 'reed_low', x=1.6, y=.3, b=.9, r=1, mark='mmf'), k(.68, 'reed_low', x=.9, y=-.3, b=-.8, w=1, mark='TWANG'), k(.86, x=1, y=.8, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'stems'), prefer=['young', 'grumpy'])
    o.r('walk_into_the_stem_counting', 'Walking along the bank counting the school and meeting the cattail stem with a loud thunk', 18, 'none',
        [k(.1, 'swirl_r', x=.3, y=.8, b=.3, l=1, mark='31'), k(.24, 'bank_r', x=.4, y=.8, b=.3, r=1, mark='32'), k(.4, 'bank_r', x=.5, y=.9, b=.4, l=1, mark='33'), k(.54, 'bank_r', x=1.7, y=.1, b=1.5, eye='@', mark='THUNK'), k(.7, 'bank_r', x=-1, y=.4, b=.1, w=.9, eye='x', mark='...'), k(.86, x=.2, y=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'bank'), prefer=['curious'])
    o.r('flinch_when_the_school_leaps_at_his_face', 'Flinching back with a yell when the whole school flicks up at the surface at his bill, a hundred tiny splashes', 16, 'none',
        [k(.1, 'swirl_m', x=.9, y=1.4, b=.8), k(.22, 'swirl_m', x=1, y=1.6, b=1, eye='o', mark='...'), k(.32, x=-1.3, y=-.9, b=-1.4, l=1, r=1, w=1, eye='O', mark='AAH'), k(.5, x=-.7, y=.2, b=-.1, w=.7, eye='>'), k(.7, x=.2, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'splashes'), pick='hungriest', prefer=['young', 'curious'], obj=[(.22, dict(lure=1)), (.5, dict(lure=1))], say=["A hundred minnows. One duck. Immediate retreat.", "They flicked. I flew. Very efficient, both sides."])
    o.r('stamp_the_pond_back_into_calm', 'Stamping at the scattered ripples after the school bursts, as if the pond could be ordered back to calm', 16, 'none',
        [k(.1, 'stone_r', x=.6, y=.7, b=.3), k(.2, 'stone_r', x=.4, y=0, b=-1.1, l=1, mark='STMP'), k(.3, 'stone_r', x=.5, y=.5, b=.5), k(.42, 'stone_r', x=.4, y=0, b=-1.1, r=1, mark='STMP'), k(.54, 'stone_r', x=.5, y=.5, b=.5), k(.68, 'stone_r', x=.4, y=0, b=-1.1, l=1, r=1, mark='STMP'), k(.86, eye='-')],
        [], g='mishap', act=('stamp', 'ripples'), prefer=['grumpy'])
    # ---------------- duets
    o.r('herd_the_school_from_both_ends', 'Herding the school from the left rim with a friend herding from the right until it balls up in the middle', 24, 'wing',
        [k(.1, 'swirl_l', reach=.5, x=.3, y=.4, b=.3), k(.26, 'swirl_l', reach=1, x=.5, y=.6, b=.5, l=1, mark='shoo'), k(.42, 'cove', reach=1, x=.6, y=.6, b=.5, r=1, mark='shoo'), k(.6, 'swirl_m', reach=1, x=.7, y=.6, b=.5, l=1, mark='shoo'), k(.78, eye='^')],
        [(.42, 'herd')], g='use', act=('guard', 'shoal'), pick='hungriest', when=['swirl<.7'], prefer=['happy'], obj=[(.2, dict(lure=1)), (.45, dict(lure=1)), (.65, dict(lure=1))],
        duo=[k(.12, 'swirl_r', x=.3, y=.4, b=.3), k(.3, 'swirl_r', x=.8, y=.7, b=.6, l=1, mark='shoo'), k(.48, 'shoal', x=.9, y=.8, b=.7, r=1, mark='shoo'), k(.66, 'swirl_m', x=.9, y=.8, b=.7, l=1, mark='shoo'), k(.84, eye='^')],
        say=["Ball formed. Both ends took credit. Minnows took a vote.", "Two ducks, one school. It chose the middle."])
    o.r('toss_flakes_back_and_forth_over_the_school', 'Tossing flakes back and forth with a friend over the school, so it surges after each flake in the air', 24, 'none',
        [k(.1, 'swirl_l', x=.4, y=.3, b=.3), k(.24, 'swirl_l', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.38, 'swirl_m', x=1, y=.4, b=.5, eye='o'), k(.52, 'swirl_m', x=.9, y=-.6, b=-.9, w=.5, r=1, mark='fwip'), k(.68, 'swirl_m', x=1, y=.4, b=.5, eye='O'), k(.84, eye='^')],
        [(.38, 'fun')], g='play', act=('throw', 'flake'), pick='hungriest', prefer=['happy', 'young'], obj=[(.4, dict(lure=1)), (.7, dict(lure=1))],
        duo=[k(.12, 'swirl_r', x=.4, y=.3, b=.3), k(.3, 'swirl_r', x=1, y=.4, b=.5, eye='o'), k(.46, 'swirl_m', x=.9, y=-.6, b=-.9, w=.5, l=1, mark='fwip'), k(.62, 'swirl_r', x=1, y=.4, b=.5), k(.8, eye='^')])
    o.r('tally_the_school_with_a_friend', 'Tallying the school with a friend, bill to bill over a count that will not stay still, finishing with a shrug', 24, 'none',
        [k(.1, 'cove', x=1.3, y=.3, b=1.1, mark='20'), k(.24, 'shoal', x=1.5, y=.4, b=1.4, l=1, mark='25'), k(.38, 'swirl_r', x=1.5, y=.4, b=1.4, r=1, mark='30?'), k(.54, 'swirl_r', x=-.4, y=-.5, b=-.6, w=.9, mark='forty'), k(.7, 'shoal', x=1.1, y=.3, b=1, eye='-', mark='shrug'), k(.86, eye='^')],
        [], g='test', act=('count', 'fry'), pick='shyest', prefer=['curious', 'happy'], obj=[(.3, dict(lure=1)), (.62, dict(lure=1))],
        duo=[k(.12, 'swirl_r', x=.7, y=.8, b=.4, mark='22'), k(.3, 'swirl_r', x=.8, y=.9, b=.5, mark='28'), k(.46, 'shoal', x=.8, y=.9, b=.5, r=1, mark='35'), k(.62, 'swirl_m', x=.9, y=1, b=.6, l=1, mark='41'), k(.8, eye='-')],
        say=["Twenty. Forty. Never the same fish twice. Fine.", "Two counters, one school, forty-one answers. Math is fluid."])
    return done(o)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['catfish', 'bass', 'carp', 'ghost_fish', 'golden_koi', 'minnow']:
        globals()[n]().emit()
