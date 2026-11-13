"""Wave 1b, version 2 (v2 rules): toy_sandbox, dog_house, toy_car, gazebo. Every routine is written out by hand.
Each drawing was printed with rep.py first; heights, parts and the real openings are in the comments of each object."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN


def sandbox():
    # Drawing (96 x 42 cells, 7.3 px a row, standing line row 39): back rim rows 17-39 (170 px+, looked at), side walls cols 7 and 88
    # from 168 px down, sand rows 23-33 (the front sand row is 44 px up), base board top edge row 34 (36 px), nine studs row 35 (29 px),
    # bucket cols 13-20 rows 27-30 (66-87 px), shovel upright cols 78-80 (D grip 102 px, shaft 87-95, blade 80), a ring of ( ) with ~ at its
    # top and bottom (66-102 px).
    o = Obj('toy_sandbox', 'placed',
            fields=dict(pit=(0, 0, 1), mound=(0, 0, 1), firm=(0, 0, 1), tracks=(0, 0, 1), water=(0, 0, 1), frost=(0, 0, 1)),
            containers={'water'},
            physics=[('pit', 'rate', -.0003, 'windy'), ('mound', 'rate', -.0004, 'wet'), ('firm', 'rate', .0004, 'sun'), ('firm', 'rate', -.0004, 'wet'),
                     ('tracks', 'rate', -.0004, 'windy'), ('water', 'rate', .002, 'wet'), ('water', 'rate', -.0003, 'dry&warm'),
                     ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(
                sweep=[('obj.dirt', 'add', -.25)], smooth=[('tracks', 'set', 0)], refill=[('pit', 'mul', .3)], level=[('mound', 'set', 0)],
                mend=[('obj.condition', 'add', .15)], dry=[('obj.wetness', 'add', -.3)],
                dig=[('pit', 'add', .3), ('mound', 'add', .1)], tamp=[('firm', 'add', .3)], pack=[('firm', 'add', .2), ('mound', 'add', -.1)],
                heap=[('mound', 'add', .3), ('pit', 'add', -.1)], furrow=[('tracks', 'add', .25)], trench=[('pit', 'add', .2)],
                print=[('tracks', 'add', .3)], fling=[('obj.dirt', 'add', .15)], fun=[('need.fun', 'add', 2)],
                dent=[('obj.condition', 'add', -.1)], scatter=[('obj.dirt', 'add', .2)], slump=[('pit', 'mul', .6)],
                cave=[('mound', 'mul', .1), ('pit', 'add', .2)], tip=[('water', 'set', 0)], squelch=[('firm', 'add', -.2)],
                crack=[('firm', 'mul', .3)], scrape=[('frost', 'mul', .2)], dustbath=[('need.cleanliness', 'add', 2), ('obj.dirt', 'add', .1)],
                doze=[('need.energy', 'add', 2)], bake=[('need.energy', 'add', 1)]),
            anchors=dict(sand_a=(0.211, 0.805, 'surface'), sand_b=(0.484, 0.805, 'surface'), sand_c=(0.758, 0.805, 'surface'), sand_deep=(0.358, 0.756),
                         board_l=(0.147, 0.829, 'surface'), board_m=(0.611, 0.829, 'surface'), board_r=(0.842, 0.829, 'surface'),
                         stud_1=(0.105, 0.854), stud_3=(0.295, 0.854), stud_6=(0.579, 0.854), stud_9=(0.863, 0.854),
                         wall_l=(0.074, 0.780), wall_r=(0.926, 0.780),
                         bucket_rim=(0.168, 0.659), bucket_side=(0.137, 0.707), bucket_base=(0.168, 0.732),
                         shovel_grip=(0.832, 0.610), shovel_shaft=(0.832, 0.659),
                         ring_l=(0.326, 0.634), ring_r=(0.684, 0.634), ring_near=(0.505, 0.732)))
    # ---------------- care
    o.r('sweep_board', 'Sweeping spilled sand off the base board with a wing', 16, 'wing',
        [k(.12, 'board_l', reach=.6, x=.3, y=.4), k(.3, 'board_l', reach=1, x=.5, y=.6, l=1), k(.5, 'board_m', reach=1, x=.6, y=.6, r=1), k(.7, 'board_r', reach=1, x=.5, y=.5, l=1), k(.88, eye='^')],
        [(.5, 'sweep')], g='care', act=('sweep', 'board'), when=['obj_dirt>.3'], prefer=['grown'])
    o.r('rake_tracks', 'Dragging his feet through the sand until his own prints are gone', 18, 'none',
        [k(.15, 'sand_a', perch=1, x=.3, y=.5, b=.3), k(.3, 'sand_a', perch=1, x=.2, y=.6, b=.5, l=1), k(.5, 'sand_b', perch=1, x=.2, y=.6, b=.5, r=1), k(.7, 'sand_c', perch=1, x=.2, y=.6, b=.5, l=1), k(.88, y=.2, eye='-')],
        [(.5, 'smooth')], g='care', act=('rake', 'tracks'), when=['tracks>.3'], prefer=['curious'],
        say=["Smooth again. No evidence.", "A clean sand floor. Very innocent."])
    o.r('refill_pit', 'Nosing the sand back over the lip of the pit until it is level', 20, 'none',
        [k(.15, x=.3, y=.5), k(.3, 'sand_c', x=1.1, y=1.3, b=.5), k(.5, 'sand_b', x=.4, y=.9, b=.4, mark='fff'), k(.7, 'sand_c', x=1.1, y=1.3, b=.5), k(.88, y=.1, w=.4, eye='-')],
        [(.5, 'refill')], g='care', act=('fill', 'pit'), when=['pit>.3'], prefer=['grown'])
    o.r('plough_heap', 'Ploughing the heap flat with his chest', 18, 'none',
        [k(.15, x=.5, y=.6, eye='>'), k(.35, 'sand_deep', x=.9, y=1, b=.8, mark='hrr'), k(.55, 'sand_a', x=1, y=1.1, b=.9), k(.75, x=.3, y=.4, b=.3, w=.5, eye='^')],
        [(.55, 'level')], g='care', act=('push', 'mound'), when=['mound>.3'], prefer=['grumpy'], obj=[(.35, dict(shake=.3)), (.6, dict(shake=.5))])
    o.r('hammer_stud', 'Hammering a loose stud back down with his bill', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'stud_3', x=1, y=1.5, b=.4, mark='tak'), k(.45, x=.2, y=.4), k(.6, 'stud_3', x=1, y=1.6, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
        [(.6, 'mend')], g='care', act=('mend', 'stud'), when=['obj_condition<.6'],
        say=["Back down. You are welcome, wood.", "One stud. Lifelong enemy now."])
    o.r('fan_sand_dry', 'Standing on the board edge and fanning the soaked sand with both wings', 20, 'none',
        [k(.15, 'board_m', perch=1, x=.2, y=.2, w=.3), k(.3, 'board_m', perch=1, x=.2, y=-.2, w=1, mark='fwp'), k(.5, 'board_m', perch=1, x=.2, y=-.3, w=0), k(.7, 'board_m', perch=1, x=.2, y=-.2, w=1, mark='fwp'), k(.88, y=.2, w=.3, eye='-')],
        [(.5, 'dry')], g='care', act=('dry', 'sand'), when=['obj_wetness>.3'], prefer=['sun'])
    # ---------------- use
    o.r('dig_pit', 'Digging a pit with both feet flying backwards', 20, 'none',
        [k(.15, 'sand_b', perch=1, x=.3, y=.6, b=.3), k(.3, 'sand_b', perch=1, y=1.2, b=1, l=1, mark='dig'), k(.5, 'sand_b', perch=1, y=1.4, b=1.1, r=1), k(.7, 'sand_b', perch=1, y=1.4, b=1.2, l=1), k(.88, x=.2, y=.2, w=.4, eye='^')],
        [(.5, 'dig')], g='use', act=('dig', 'sand'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.3)), (.6, dict(shake=.5))],
        say=["Down we go. Still no treasure. Typical.", "Dug it. Fell in it. In that order."])
    o.r('tamp_sand_flat', 'Slapping the sand down firm with the flat of a wing', 16, 'wing',
        [k(.15, 'sand_deep', reach=.6, x=.3, y=.5, w=.3), k(.3, 'sand_deep', reach=1, x=.3, y=.6, w=1), k(.45, 'sand_deep', reach=.6, x=.3, y=.5, w=.3), k(.6, 'sand_deep', reach=1, x=.3, y=.6, w=1), k(.8, x=.1, w=.4, eye='-')],
        [(.6, 'tamp')], g='use', act=('pat', 'sand'))
    o.r('pat_heap_firm', 'Patting both sides of the heap into a hard dome with a wing apiece', 18, 'wing',
        [k(.15, 'sand_a', reach=.5, x=.3, y=.5, w=.3), k(.3, 'sand_a', reach=1, x=.5, y=.7, b=.3, w=1), k(.5, 'sand_c', reach=1, x=.5, y=.7, b=.5, w=1), k(.7, 'sand_c', reach=.6, x=.2, y=.4, w=.4), k(.88, eye='^')],
        [(.5, 'pack')], g='use', act=('pat', 'mound'), when=['mound>.3'], prefer=['curious'])
    o.r('shove_sand_heap', 'Shoving the loose sand into a heap with his breast', 20, 'none',
        [k(.15, x=.5, y=.5, eye='>'), k(.35, 'sand_c', x=1, y=.9, b=.6, mark='hup'), k(.55, 'sand_b', x=1.1, y=.9, b=.6), k(.75, 'sand_a', x=1.1, y=.9, b=.7), k(.9, eye='^')],
        [(.55, 'heap')], g='use', act=('shove', 'sand'), when=['pit<=.7'], prefer=['grown'])
    o.r('draw_a_furrow', 'Dragging his bill along the front sand in one long straight furrow', 18, 'none',
        [k(.12, 'sand_a', x=1, y=1.3, b=.3), k(.35, 'sand_b', x=1.2, y=1.5, b=.4), k(.6, 'sand_c', x=1.2, y=1.5, b=.4, mark='skrr'), k(.8, x=.2, y=.3, eye='-'), k(.9, eye='^')],
        [(.6, 'furrow')], g='use', act=('drag', 'furrow'), prefer=['curious'])
    o.r('scrape_ring_deeper', 'Scraping along the bottom of the ring with his bill to cut it deeper', 20, 'none',
        [k(.15, x=.4, y=.2), k(.3, 'ring_near', x=1.2, y=-.4, b=.4, mark='scr'), k(.5, 'ring_near', x=1.3, y=-.2, b=.5), k(.7, 'ring_near', x=1.2, y=-.4, b=.4, mark='scr'), k(.88, eye='^')],
        [(.5, 'trench')], g='use', act=('dig', 'ring'), ages=GROWN, prefer=['happy'])
    # ---------------- play
    o.r('sand_angel', 'Flopping flat on his back in the sand and flapping an angel', 18, 'none',
        [k(.15, 'sand_b', perch=1, y=-.4, b=-.5, w=.6, eye='>'), k(.3, 'sand_b', perch=1, y=1.5, b=1.4, w=1, mark='floomp'), k(.5, 'sand_b', perch=1, y=1.5, b=1.4, w=0), k(.7, 'sand_b', perch=1, y=1.5, b=1.4, w=1), k(.9, y=.3, b=.2, eye='^')],
        [(.5, 'print')], g='play', act=('press', 'sand'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.4)), (.6, dict(shake=.4))],
        say=["Angel. Look at the wingspan on that.", "Lie in it, get up, regret nothing."])
    o.r('hop_a_trail', 'Hopping in three jumps from the right sand to the left to lay a trail', 20, 'none',
        [k(.12, 'sand_c', perch=1, x=.4, y=.5, b=.5, l=1), k(.3, y=-.4, b=-.7, w=.5), k(.45, 'sand_b', perch=1, x=.5, y=.5, b=.6, r=1), k(.62, y=-.4, b=-.7, w=.5), k(.78, 'sand_a', perch=1, x=.5, y=.5, b=.6, l=1), k(.9, eye='^')],
        [(.45, 'print')], g='play', act=('hop', 'sand'), prefer=['happy'])
    o.r('stomp_heap_flat', 'Jumping up and down on the heap until it is a pancake', 18, 'none',
        [k(.15, 'sand_c', perch=1, y=-.3, b=-.6, w=.5), k(.3, 'sand_c', perch=1, y=.4, b=1.1, l=1, mark='thud'), k(.45, 'sand_c', perch=1, y=-.4, b=-.9, w=1), k(.6, 'sand_c', perch=1, y=.4, b=1.3, r=1, mark='THUD'), k(.8, y=.2, b=.3, eye='^')],
        [(.6, 'level')], g='play', act=('stamp', 'mound'), when=['mound>.3'], prefer=['grumpy'], obj=[(.3, dict(shake=.5)), (.6, dict(shake=.8))],
        say=["Flattened. It had it coming.", "Heap: gone. Me: taller."])
    o.r('fling_sand_at_wall', 'Flinging billfuls of sand over his shoulder at the left wall', 18, 'none',
        [k(.15, x=.3, y=.4), k(.3, 'sand_a', x=1.1, y=1.4, b=.5, mark='hup'), k(.45, y=-.5, x=-.6, w=.5, eye='>'), k(.6, 'sand_a', x=1.1, y=1.4, b=.5, mark='hup'), k(.75, y=-.5, x=-.7, w=.8, eye='>'), k(.9, eye='-')],
        [(.3, 'fling')], g='play', act=('throw', 'sand'), prefer=['grumpy'], say=["Take that, wall. And that.", "Sand: airborne. Wall: unmoved. Draw."])
    o.r('toss_and_catch', 'Tossing a billful of sand straight up and catching it again', 16, 'none',
        [k(.15, 'sand_b', x=1.4, y=1.4, b=.6), k(.3, x=-.6, y=-1.4, b=-.8, w=.6, eye='O'), k(.45, x=-.6, y=-1.6, b=-1, w=.3, l=1, eye='>'), k(.6, 'sand_b', x=1.4, y=1.4, b=.6, mark='gulp'), k(.8, x=-.3, y=-.3, eye='-')],
        [], g='play', act=('catch', 'sand'), prefer=['happy'])
    o.r('leap_off_board', 'Climbing up on the base board and leaping off into the sand', 16, 'none',
        [k(.15, 'board_l', perch=1, x=.3, y=.2, b=.5), k(.3, 'board_l', perch=1, y=-.4, b=-.6, w=.5), k(.45, y=-.8, b=-1, w=1, eye='O'), k(.62, 'sand_a', perch=1, y=.6, b=1.2, l=1, mark='FOOMP'), k(.82, y=.2, b=.2, w=.5, eye='^')],
        [], g='play', act=('climb', 'board'), prefer=['young', 'happy'])
    o.r('honk_into_bucket', 'Honking through the bucket mouth like a megaphone', 14, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.4, y=-.2, w=.2), k(.35, 'bucket_rim', reach=1, x=1.2, y=.5, w=.3, mark='HONK'), k(.55, 'bucket_rim', reach=1, x=1.2, y=.5, w=.5, mark='HONK', eye='O'), k(.75, x=-.4, y=-.5, eye='^')],
        [(.35, 'fun')], g='play', act=('shout', 'bucket'), shown='head', ages=GROWN, say=["Sounds like a bigger me.", "Bucket has better acoustics than the barn."])
    # ---------------- test
    o.r('taste_sand', 'Tasting a billful of sand and deciding against it', 14, 'none',
        [k(.15, 'sand_a', x=1.4, y=1.4, b=.6), k(.35, x=.4, y=.4, b=.2, eye='-', mark='...'), k(.55, x=-.8, y=-.6, b=-.4, w=.5, eye='>', mark='ptui'), k(.75, y=.8, b=.3, eye='-')],
        [], g='test', act=('taste', 'sand'), prefer=['curious', 'young'], say=["Tastes like the floor. Because it is the floor.", "Sand. Still sand. Zero stars."])
    o.r('knock_left_wall', 'Knocking on both side walls with his bill and listening for hollow', 16, 'none',
        [k(.12, 'wall_l', x=1.2, y=.6, b=.3, mark='tok'), k(.3, 'wall_l', x=.8, y=-.3, b=-.3, l=1, mark='tok'), k(.55, x=-.6, y=-.6, w=.4, eye='-'), k(.75, 'wall_r', x=1.2, y=.6, b=.5, mark='tok'), k(.9, eye='^')],
        [], g='test', act=('knock', 'wall'))
    o.r('tug_stuck_shovel', 'Hauling at the shovel by the grip, then the shaft, to see how deep it is stuck', 18, 'none',
        [k(.15, x=.4, y=-.2), k(.3, 'shovel_grip', x=.8, y=-.3, b=.4, mark='hnh'), k(.5, 'shovel_shaft', x=.9, y=-.3, b=.8, l=1, mark='HNNH'), k(.7, x=-.5, y=-.2, w=.6, eye='>'), k(.88, eye='-')],
        [], g='test', act=('tug', 'shovel'), ages=GROWN)
    o.r('measure_the_ring', 'Pacing the ring from the left arc to the right and counting steps under his breath', 22, 'none',
        [k(.12, 'ring_l', x=.6, y=-.2, b=.2, l=1), k(.32, 'ring_near', x=.9, y=-.4, b=.3, r=1), k(.52, 'ring_r', x=.6, y=-.2, b=.2, l=1), k(.72, x=.2, y=-.1, eye='-', mark='nine'), k(.9, eye='^')],
        [], g='test', act=('measure', 'ring'), ages=GROWN, prefer=['curious'])
    o.r('count_the_studs', 'Tapping each stud along the base board and counting to nine', 20, 'none',
        [k(.12, 'stud_1', x=.8, y=1.4, b=.6, mark='1'), k(.3, 'stud_3', x=1, y=1.2, b=.3, l=1, mark='3'), k(.5, 'stud_6', x=.6, y=1, b=.8, r=1, mark='6'), k(.7, 'stud_9', x=1.1, y=1.4, b=.4, l=1, mark='9'), k(.88, x=-.4, y=-.2, w=.4, eye='-', mark='nine')],
        [], g='test', act=('count', 'studs'), prefer=['curious'])
    o.r('peer_down_the_pit', 'Leaning out over the edge of the pit and peering at the bottom', 18, 'none',
        [k(.15, x=.5, y=.3), k(.35, 'sand_c', x=1.1, y=1.5, b=.6, eye='O'), k(.55, 'sand_b', x=1.3, y=1.9, b=.7, mark='hmm'), k(.75, x=.3, y=.4, eye='-'), k(.9, eye='^')],
        [], g='test', act=('peer', 'pit'), when=['pit>.3'], prefer=['curious'])
    o.r('sniff_wet_sand', 'Snuffling at the sodden sand to find out what it smells of', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_c', x=1, y=1.3, b=.4, mark='snf'), k(.5, 'sand_c', x=1.2, y=1.4, b=.4, mark='snf snf'), k(.7, x=-.2, y=.3, eye='>', mark='ugh'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'sand'), when=['obj_wetness>.3'], prefer=['curious'])
    # ---------------- rest
    o.r('nap_in_the_sand', 'Wriggling flat in the sand and dozing off', 28, 'none',
        [k(.15, 'sand_b', perch=1, x=.4, y=.5), k(.3, 'sand_b', perch=1, y=1.4, b=1.2, w=.3), k(.5, 'sand_b', perch=1, y=1.6, b=1.5, eye='-', mark='z'), k(.75, 'sand_b', perch=1, y=1.6, b=1.5, eye='-', mark='zZ'), k(.9, y=.8, b=.6, eye='o')],
        [(.5, 'doze')], g='rest', act=('nap', 'sand'), when=['tired'], say=["Perfect fit. Of course it is. I wore it in.", "Do not tell the shovel I slept here."])
    o.r('bake_belly_warm', 'Standing spread-winged in the sun-warmed sand with his eyes shut, basking', 30, 'none',
        [k(.15, 'sand_c', perch=1, y=.3, x=.3), k(.3, 'sand_c', perch=1, y=-.6, b=-.2, w=1, eye='-'), k(.55, 'sand_c', perch=1, y=-1.2, b=-.3, w=1, eye='-', mark='ahh'), k(.8, 'sand_c', perch=1, y=-1.2, b=-.3, w=1, eye='-'), k(.92, y=.5, b=.4, eye='^')],
        [(.55, 'bake')], g='rest', act=('warm', 'sand'), when=['sun', 'firm>.2'], prefer=['happy'])
    o.r('lean_on_the_wall', 'Leaning his shoulder against the left wall with his eyes shut', 22, 'none',
        [k(.15, x=.2, y=.2, w=.3), k(.35, 'wall_l', x=.9, y=.3, b=.2, eye='-'), k(.6, 'wall_l', x=1.1, y=.9, b=.9, eye='-', mark='z'), k(.85, 'wall_l', x=1.1, y=1, b=1.2, eye='-')],
        [], g='rest', act=('lean', 'wall'), when=['tired'], prefer=['elder'])
    o.r('sit_on_the_board_edge', 'Sitting on the board edge and watching the light go out', 26, 'none',
        [k(.15, 'board_r', perch=1, y=.3, b=.2), k(.4, 'board_r', perch=1, y=.5, b=.9, eye='-'), k(.7, 'board_r', perch=1, y=.5, b=.9, eye='-', mark='...'), k(.9, 'board_r', perch=1, y=.2, b=.3, eye='o')],
        [], g='rest', act=('sit', 'board'), when=['dusk'], prefer=['happy'], say=["Sun goes down. I stay sat. Efficient.", "Best seat. Cost me nothing."])
    o.r('sulk_at_the_far_wall', 'Standing at the right wall with his back turned and refusing to explain', 24, 'none',
        [k(.15, x=-.5, y=.3, w=.4), k(.35, 'wall_r', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'wall_r', x=-1, y=1.4, b=.9, l=1, eye='-', mark='hmph'), k(.85, 'wall_r', x=-1, y=1.6, b=1.1, eye='-')],
        [], g='rest', act=('sulk', 'wall'), when=['sad'], prefer=['grumpy'], say=["Not sulking. Facing the wall. Different.", "Sand did this to me."])
    # ---------------- weather
    o.r('tip_out_the_rain', 'Tipping the bucket over to empty out the rainwater', 20, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.3, y=-.2, w=.5), k(.35, 'bucket_rim', reach=1, x=.2, y=-.4, b=.4, w=1, mark='hng'), k(.55, 'bucket_rim', reach=1, x=.5, y=.3, b=.7, w=.9, mark='glug'), k(.75, x=-.4, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
        [(.55, 'tip')], g='weather', act=('pour', 'bucket'), when=['water>.3'], ages=GROWN, obj=[(.35, dict(sway=.3)), (.55, dict(shake=.5))])
    o.r('squelch_the_soaked_sand', 'Stomping the soaked sand until it squelches up between his toes', 18, 'none',
        [k(.15, 'sand_a', perch=1, y=.3, x=.3), k(.3, 'sand_a', perch=1, y=.6, b=.6, l=1, mark='squelch'), k(.5, 'sand_b', perch=1, y=.6, b=.7, r=1, mark='squelch'), k(.7, 'sand_c', perch=1, y=.6, b=.7, l=1, eye='O', mark='squelch'), k(.9, eye='^')],
        [(.5, 'squelch')], g='weather', act=('splash', 'sand'), when=['obj_wetness>.5'], prefer=['happy'])
    o.r('prop_the_slumping_heap', 'Pressing his wings against the heap so the rain cannot slump it', 22, 'wing',
        [k(.15, 'sand_deep', reach=.6, x=.3, y=.7), k(.35, 'sand_deep', reach=1, x=.6, y=.8, b=.4, w=1), k(.55, 'sand_a', reach=1, x=.7, y=.9, b=.5, w=1, eye='>'), k(.8, x=.1, eye='-', mark='ugh')],
        [(.55, 'tamp')], g='weather', act=('press', 'mound'), when=['wet', 'mound>.3'])
    o.r('chip_the_crust', 'Hammering the sun-baked crust with his bill until it cracks', 20, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_c', x=1, y=1.4, b=.4, mark='tak'), k(.45, x=.6, y=.5, w=.5), k(.6, 'sand_c', x=1, y=1.5, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
        [(.6, 'crack')], g='weather', act=('chip', 'sand'), when=['firm>.6'], prefer=['grumpy'])
    o.r('scrape_frost_off_board', 'Scraping the frost off the base board with the edge of a wing', 18, 'wing',
        [k(.12, 'board_l', reach=.6, x=.2, y=.5), k(.3, 'board_m', reach=1, x=.3, y=.6, b=.3), k(.5, 'board_m', reach=1, x=.3, y=.7, b=.3, mark='skr'), k(.7, 'board_r', reach=1, x=.3, y=.6, b=.3), k(.88, eye='-')],
        [(.5, 'scrape')], g='weather', act=('scrape', 'board'), when=['cold', 'frost>.3'])
    o.r('dust_bath_in_the_sand', 'Shuffling side to side in the bone-dry sand so the dust flies up through his feathers', 24, 'none',
        [k(.15, 'sand_c', perch=1, y=.6, b=.3), k(.3, 'sand_c', perch=1, x=1, y=.6, b=1.2, w=1, mark='fff'), k(.5, 'sand_c', perch=1, x=-1, y=.6, b=1.4, w=0, l=1), k(.7, 'sand_c', perch=1, x=1, y=.6, b=1.2, w=1, r=1, mark='fff'), k(.9, y=.2, w=.4, eye='^')],
        [(.5, 'dustbath')], g='weather', act=('fluff', 'sand'), when=['dry', 'warm', 'obj_wetness<.3'], prefer=['happy'], say=["Clean now. Dirtier. Same thing.", "Dust bath. Filthy, correct, dignified."])
    # ---------------- show
    o.r('king_of_the_heap', 'Standing atop the heap with his wings spread and announcing himself king', 22, 'none',
        [k(.15, 'sand_deep', y=.3, b=.5), k(.3, 'sand_c', perch=1, y=-.5, b=-.4, w=.6), k(.5, 'sand_c', perch=1, y=-.9, b=-.2, w=1, eye='^', mark='BOW'), k(.75, 'sand_c', perch=1, y=-.9, b=-.2, w=1), k(.9, y=0, eye='o')],
        [], g='show', act=('pose', 'mound'), when=['mound>.3'], prefer=['happy'], say=["King of this exact pile. Bow or leave.", "Long live me. Short pile."])
    o.r('sign_the_sand', 'Writing CHEESE along the front sand with the tip of his bill', 22, 'none',
        [k(.12, 'sand_a', x=1.4, y=1.5, b=.6), k(.3, 'sand_deep', x=1.2, y=1.2, b=.3, l=1), k(.5, 'sand_c', x=1.4, y=1.5, b=.7, r=1), k(.7, x=.3, y=-.4, w=.5, eye='^'), k(.88, x=.1, y=.3, eye='o')],
        [(.5, 'print')], g='show', act=('show', 'sand'), prefer=['curious'], say=["Cheese was here. Cheese is always here.", "Signed it. Let the wind try to forge it."])
    o.r('drum_the_bucket', 'Drumming a roll with both wings at the bucket rim', 18, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.3), k(.3, 'bucket_rim', reach=1, w=.8, mark='rrrr'), k(.42, 'bucket_side', reach=.6, w=.2, mark='rrrr'), k(.56, 'bucket_base', reach=.4, w=.5, mark='dunk'), k(.7, 'bucket_rim', reach=1, w=.9, mark='TSH'), k(.85, y=1, b=.5, w=1, eye='^')],
        [], g='show', act=('drum', 'bucket'), ages=GROWN, say=["Thank you. Tip the bucket.", "Encore? No. I have standards."])
    o.r('tap_dance_the_board', 'Tap-dancing the length of the base board with a click at every stud', 20, 'none',
        [k(.12, 'board_l', perch=1, y=-.3, b=-.3, w=.7, l=1, mark='tk'), k(.32, 'board_m', perch=1, y=-.3, b=-.3, w=.9, r=1, mark='tk'), k(.52, 'board_m', perch=1, y=-.4, b=-.5, w=1, l=1, mark='tk tk'), k(.72, 'board_r', perch=1, y=-.3, b=-.3, w=.9, r=1, mark='tk'), k(.9, y=.4, b=.5, w=0, eye='^')],
        [(.52, 'fun')], g='show', act=('dance', 'board'), prefer=['young', 'happy'])
    o.r('argue_with_the_shovel', 'Jabbing a wing at the shovel grip and arguing whose sandbox this is', 22, 'wing',
        [k(.15, x=.2, y=-.3), k(.35, 'shovel_grip', reach=.8, x=.9, y=-.6, b=-.2, mark='MINE'), k(.55, 'shovel_grip', reach=1, x=1, y=-.6, b=-.3, eye='>', mark='no, MINE'), k(.75, x=-.3, y=-.5, eye='-'), k(.9, eye='^')],
        [], g='show', act=('argue', 'shovel'), ages=GROWN, prefer=['grumpy'])
    # ---------------- mishap
    o.r('head_wedged_in_bucket', 'Diving head first at the bucket mouth, sticking at the shoulders and kicking out', 22, 'none',
        [k(.15, x=.5, eye='>'), k(.3, 'bucket_rim', x=1.2, y=.6, b=.8, mark='oof'), k(.5, 'bucket_rim', x=1.3, y=.6, b=1, l=1, eye='O', mark='mmf'), k(.7, 'bucket_rim', x=1.3, y=.6, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
        [(.7, 'dent')], g='mishap', act=('stuck', 'bucket'), shown='head', ages=GROWN, prefer=['young', 'grumpy'], obj=[(.5, dict(shake=.6)), (.7, dict(shake=1))],
        say=["Wedged by the shoulders. Bucket won.", "I meant to do that. All of it."])
    o.r('trip_on_the_board', 'Tripping over the base board and eating a billful of sand', 16, 'none',
        [k(.15, 'board_l', x=.5, y=.3, l=1), k(.3, x=1.1, y=.8, b=-.4, w=.8, eye='O'), k(.5, 'sand_a', x=1.6, y=1.8, b=1, w=1, mark='FFF'), k(.75, y=.6, b=.4, eye='@'), k(.9, eye='-')],
        [(.5, 'scatter')], g='mishap', act=('slip', 'board'), say=["Face. Sand. Dignity: buried.", "The board moved. It is always the board."])
    o.r('bonk_the_shovel_shaft', 'Marching head down at the shovel shaft and bouncing off it', 16, 'none',
        [k(.15, x=.4, y=.4), k(.3, x=1, y=.3, b=.3, w=.3, mark='hup'), k(.45, 'shovel_shaft', x=1.2, y=.2, b=.4, eye='O', mark='BONK'), k(.65, x=-1, y=-.3, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'shovel'), ages=GROWN, say=["Saw the shaft coming. Chose violence anyway.", "Shaft: unharmed. Skull: negotiating."])
    o.r('climb_out_of_the_pit', 'Sinking to the knees in the sand pit and heaving himself out', 20, 'none',
        [k(.15, 'sand_b', perch=1, x=.4, y=.4), k(.3, 'sand_b', perch=1, x=.2, y=.2, b=1.1, l=1, eye='O'), k(.5, 'sand_b', perch=1, x=.2, y=.3, b=1.6, r=1, w=.6, mark='hnnng'), k(.7, 'sand_b', perch=1, x=.3, y=-.3, b=-.5, w=1, mark='POP'), k(.88, y=.8, eye='-')],
        [(.5, 'slump')], g='mishap', act=('climb', 'pit'), when=['pit>.3'], prefer=['young'])
    o.r('cave_in_the_heap', 'Burrowing at the foot of the heap until the whole top comes down on his head', 20, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_a', x=1, y=1.2, b=.7, l=1, mark='dig'), k(.5, 'sand_a', x=1.2, y=1.5, b=.9, r=1, eye='O'), k(.65, 'sand_a', y=2, b=1.4, w=1, mark='FWUMP', eye='@'), k(.88, y=1.2, b=1, eye='-', mark='...')],
        [(.65, 'cave')], g='mishap', act=('dig', 'mound'), when=['mound>.3'], prefer=['curious'], obj=[(.5, dict(shake=.3)), (.65, dict(shake=1))], say=["I dug. It fell. Physics is a snitch.", "Buried by my own heap. Good work, me."])
    o.r('blow_sand_back_in_his_face', 'Puffing a billful of sand off the board against the wind and wearing it', 16, 'none',
        [k(.15, 'board_m', x=1, y=1.2, b=.4), k(.3, x=-.3, y=-.3, w=.4), k(.45, x=1, y=.6, mark='fff'), k(.6, 'board_m', y=1.2, b=.6, w=.8, eye='@', mark='pfft'), k(.8, x=-.3, y=.4, eye='-')],
        [(.6, 'scatter')], g='mishap', act=('blow', 'sand'), when=['windy'], say=["Blew it away. It came back. Rude.", "Wind: one. Eyes: nil."])
    return o


def dog_house():
    # Drawing (70 x 43 cells, 9.3 px a row, standing line row 40): roof rows 7-21 (180 px+) with the CHEESE sign at row 19 (196 px), eave rows 22-23
    # (158-168 px), left panel cols 10-23 (three planks, bolts at cols 11 16 21 on rows 24 31 38, a knot at cols 15-17 on rows 25 and 33),
    # door frame cols 25-45 with nested frames inside, sill row 38 (19 px), threshold row 40 (0 px), right panel cols 48-59 (bolts col 51, a knot at
    # cols 54-56), the water bowl cols 56-63 rows 40-41 (0 px). Nothing here moves: only the whole house can sway or shake.
    o = Obj('dog_house', 'placed',
            fields=dict(water=(0, 0, 1), frost=(0, 0, 1), warmth=(0, 0, 1)),
            containers={'water'},
            physics=[('warmth', 'rate', .0004, 'sun'), ('warmth', 'rate', -.0006, 'cold'), ('warmth', 'rate', -.0002, 'night'),
                     ('water', 'rate', .003, 'wet'), ('water', 'rate', -.0004, 'dry&warm'),
                     ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(
                scrub=[('obj.dirt', 'add', -.25)], sweep=[('obj.dirt', 'add', -.15)], scour=[('obj.dirt', 'add', -.1)], dry=[('obj.wetness', 'add', -.3)],
                bolt=[('obj.condition', 'add', .15)], slosh=[('water', 'mul', .5)], wipe=[('obj.dirt', 'add', .1), ('need.cleanliness', 'add', 1)],
                fun=[('need.fun', 'add', 2)], bail=[('water', 'set', 0)], scrape=[('frost', 'mul', .2)], cool=[('need.cleanliness', 'add', 1)],
                warm=[('warmth', 'add', -.2), ('need.energy', 'add', 2)], muddy=[('obj.dirt', 'add', .1)], dent=[('obj.condition', 'add', -.1)],
                soak=[('obj.wetness', 'add', .15)]),
            anchors=dict(plank_l=(0.217, 0.833), plank_r=(0.812, 0.833), bolt_l1=(0.159, 0.905), bolt_l2=(0.232, 0.905), bolt_l3=(0.304, 0.905), bolt_r=(0.739, 0.905),
                         knot_l=(0.232, 0.786), knot_r=(0.797, 0.786), frame_l=(0.362, 0.833), frame_l2=(0.362, 0.714), frame_r=(0.652, 0.833), frame_r2=(0.652, 0.714),
                         door_dark=(0.522, 0.810), sill_a=(0.420, 0.905, 'surface'), sill_b=(0.580, 0.905, 'surface'), thr_l=(0.464, 0.952), thr_r=(0.609, 0.952),
                         bowl_l=(0.841, 0.952, 'surface'), bowl_r=(0.899, 0.952, 'surface')))
    # ---------------- care
    o.r('scrub_planks', 'Scrubbing the left planks with a wing until the mud comes off', 18, 'wing',
        [k(.12, 'plank_l', reach=.6, x=.3, y=.4), k(.3, 'plank_l', reach=1, x=.5, y=.6, l=1), k(.5, 'plank_l', reach=1, x=.6, y=.8, b=.3, r=1, mark='skrk'), k(.7, 'plank_l', reach=1, x=.5, y=.5, l=1), k(.88, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'planks'), when=['obj_dirt>.3'], prefer=['grown'])
    o.r('sweep_sill', 'Sweeping the sill clean with the flat of a wing', 16, 'wing',
        [k(.12, 'sill_a', reach=.6, x=.3, y=.5), k(.3, 'sill_a', reach=1, x=.5, y=.7, l=1), k(.55, 'sill_b', reach=1, x=.6, y=.7, r=1), k(.75, 'sill_b', reach=.7, x=.3, y=.4), k(.9, eye='-')],
        [(.55, 'sweep')], g='care', act=('sweep', 'sill'), when=['obj_dirt>.3'])
    o.r('scour_bowl_rim', 'Scouring the bowl rim with his bill until it shines', 16, 'none',
        [k(.12, 'bowl_l', x=.5, y=.8, b=.3), k(.3, 'bowl_l', x=1.2, y=1.6, b=.7, mark='skrr'), k(.55, 'bowl_r', x=1.2, y=1.6, b=.7, mark='skrr'), k(.75, x=.5, y=.8, eye='-'), k(.9, eye='^')],
        [(.55, 'scour')], g='care', act=('scrub', 'bowl'), when=['obj_dirt>.3'])
    o.r('mop_frame_dry', 'Mopping both sides of the door frame dry with his breast and a lot of grunting', 20, 'none',
        [k(.12, 'frame_l', x=.4, y=.4), k(.3, 'frame_l', x=.9, y=.5, b=.4, mark='hff'), k(.5, 'frame_l', x=1, y=.4, b=.6), k(.7, 'frame_r', x=.9, y=.5, b=.4, mark='hff'), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'frame'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.2)), (.7, dict(shake=.2))])
    o.r('hammer_loose_bolt', 'Hammering a loose bolt back down with his bill', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'bolt_l2', x=1, y=1.5, b=.4, mark='tak'), k(.45, x=.2, y=.4), k(.6, 'bolt_l2', x=1, y=1.6, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
        [(.6, 'bolt')], g='care', act=('mend', 'bolt'), when=['obj_condition<.6'])
    # ---------------- use
    o.r('guard_the_bowl', 'Planting himself at the bowl with his wings out and daring the garden to come closer', 22, 'none',
        [k(.15, y=.3, b=.2), k(.35, 'bowl_r', perch=1, x=.6, y=.6, w=1, eye='>'), k(.6, 'bowl_r', perch=1, x=1.2, y=1.2, b=1, w=1, eye='>', mark='hsss'), k(.85, 'bowl_r', perch=1, x=.6, y=.6, w=1, eye='>')],
        [], g='use', act=('guard', 'bowl'), prefer=['grumpy'], say=["Come closer. Go on. I am three bowls tall.", "The bowl is mine. The garden can fetch its own."])
    o.r('knock_then_answer', 'Knocking at the door frame, then turning round and answering it politely', 20, 'none',
        [k(.12, 'frame_l', x=.9, y=.4, mark='knock'), k(.3, 'frame_l', x=.9, y=.5, mark='knock'), k(.5, x=-.7, y=-.5, w=.5, eye='O', mark='Hello?'), k(.7, x=.4, y=.2, b=.3, w=0, eye='^', mark='Coming!'), k(.88, eye='-')],
        [], g='use', act=('knock', 'frame'), say=["Nobody in. Rude of me to answer.", "Knocked. Answered. Still not home."])
    o.r('peer_into_the_dark', 'Poking just his head through the dark doorway and checking both ways', 20, 'none',
        [k(.15, x=.4, y=.2), k(.3, 'door_dark', x=1.4, y=.3, b=.3, eye='O'), k(.5, 'door_dark', x=1.5, y=.4, b=.4, eye='>', mark='hm'), k(.7, 'door_dark', x=1.5, y=.3, b=.4, eye='-'), k(.88, x=.2, eye='-')],
        [], g='use', act=('peer', 'doorway'), shown='head', prefer=['curious'])
    o.r('holler_at_the_door', 'Cupping a wing at the door frame and hollering that dinner is ready', 18, 'wing',
        [k(.15, 'frame_r', reach=.5, x=.2, y=-.3), k(.35, 'frame_r', reach=1, x=.6, y=-.8, b=-.2, mark='DINNER'), k(.55, 'frame_r', reach=1, x=.7, y=-.9, b=-.3, eye='O', mark='DINNER!'), k(.75, x=-.2, y=.2, eye='-', mark='...')],
        [], g='use', act=('shout', 'frame'), prefer=['lonely'], say=["Dinner. Nobody came. More for me.", "There is no dinner. Nobody asked."])
    o.r('splash_the_bowl', 'Dunking his bill and splashing the bowl water all over the doorstep', 16, 'none',
        [k(.15, 'bowl_l', x=.7, y=.9, b=.3), k(.3, 'bowl_l', x=1.2, y=1.6, b=.5, mark='glub'), k(.5, 'bowl_l', x=1.2, y=1.6, b=.6, w=.8, mark='SPLOSH'), k(.75, x=-.4, y=.2, w=.5, eye='O'), k(.9, eye='^')],
        [(.5, 'slosh')], g='use', act=('splash', 'bowl'), when=['water>.2'], prefer=['happy'], say=["More on the doorstep than in the bowl. Fine.", "Wet now. Chose it."])
    o.r('scrape_feet_clean', 'Scraping his feet clean along the threshold, one then the other, before not going in', 18, 'none',
        [k(.12, 'thr_l', x=.3, y=.4, l=1), k(.3, 'thr_l', x=.3, y=.5, b=.3, r=1, mark='skrt'), k(.5, 'thr_r', x=.3, y=.4, b=.2, l=1, mark='skrt'), k(.7, 'thr_r', x=.4, y=.5, b=.3, r=1), k(.88, eye='^')],
        [(.5, 'wipe')], g='use', act=('scrape', 'feet'), prefer=['curious'])
    # ---------------- play
    o.r('hop_up_and_off_the_sill', 'Hopping up on the sill and off again like a step stool', 16, 'none',
        [k(.15, 'sill_a', perch=1, y=-.3, b=-.6, w=.5), k(.3, 'sill_a', perch=1, y=.3, b=.8, l=1), k(.45, y=-.6, b=-.9, w=1), k(.62, 'sill_b', perch=1, y=.3, b=.8, r=1), k(.8, y=-.4, b=-.8, w=.8, eye='^')],
        [], g='play', act=('hop', 'sill'), prefer=['young', 'happy'])
    o.r('race_the_bolts', 'Sprinting along the front of the house and tapping every low bolt with his bill', 18, 'none',
        [k(.12, 'bolt_l1', x=.6, y=1.2, b=.5, mark='tk'), k(.3, 'bolt_l2', x=.7, y=1.3, b=.4, l=1, mark='tk'), k(.48, 'bolt_l3', x=.8, y=1.2, b=.5, r=1, mark='tk'), k(.68, 'bolt_r', x=.9, y=1.3, b=.4, l=1, mark='tk'), k(.88, x=.2, w=.7, eye='^')],
        [(.68, 'fun')], g='play', act=('race', 'bolts'), prefer=['young', 'happy'])
    o.r('flatten_at_the_frame', 'Flattening himself against the door frame and bursting out at nothing', 18, 'none',
        [k(.15, 'frame_r', x=-.3, y=.3, b=.4), k(.35, 'frame_r', x=-.4, y=.6, b=.7, eye='-'), k(.55, 'frame_r', x=-.4, y=.6, b=.7, eye='-', mark='...'), k(.7, y=-.8, b=-.8, w=1, eye='O', mark='BOO'), k(.88, y=.3, eye='^')],
        [], g='play', act=('hide', 'frame'), prefer=['young'], say=["Boo. Nothing. Good.", "Got it. Whatever it was."])
    o.r('spy_at_the_knot', 'Putting an eye to the left knot and squinting like a spy', 16, 'none',
        [k(.15, x=.4, y=-.2), k(.3, 'knot_l', x=1, y=-.4, b=.2, eye='-'), k(.5, 'knot_l', x=1.2, y=-.4, b=.3, eye='O', mark='hmm'), k(.7, 'knot_l', x=1.2, y=-.4, b=.3, eye='>'), k(.88, x=.2, eye='-')],
        [], g='play', act=('peer', 'knot'), ages=GROWN, prefer=['curious'])
    o.r('dig_beside_the_threshold', 'Digging furiously at the ground beside the threshold with both feet, burying nothing', 18, 'none',
        [k(.12, 'thr_l', x=.4, y=.8, b=.5), k(.3, 'thr_l', x=.5, y=1.2, b=1, l=1, mark='dig'), k(.5, 'thr_l', x=.5, y=1.4, b=1.2, r=1, mark='dig dig'), k(.7, 'thr_l', x=.4, y=1.4, b=1.3, l=1), k(.88, y=.2, w=.4, eye='^')],
        [(.5, 'muddy')], g='play', act=('dig', 'ground'), prefer=['happy'], say=["Hole. Empty. Plan: fully on track.", "Dog taught me this. Dog is not credited."])
    o.r('chase_his_tail', 'Spinning in tight circles and snapping at his own tail', 16, 'none',
        [k(.15, 'thr_r', x=.5, y=.3, b=.4, l=1), k(.3, 'thr_r', x=-.7, y=.6, b=.7, r=1), k(.5, 'thr_r', x=.7, y=.4, b=.8, l=1, eye='@'), k(.7, 'thr_r', x=-.7, y=.6, b=.7, r=1), k(.88, x=.1, eye='o')],
        [], g='play', act=('chase', 'tail'), prefer=['young', 'happy'])
    o.r('roll_over_and_play_dead', 'Rolling over and over along the threshold and playing dead', 20, 'none',
        [k(.12, 'thr_l', x=.4, y=.5, b=.6), k(.3, 'thr_r', x=.8, y=1.2, b=1.2, l=1, r=1), k(.5, 'thr_l', y=1.5, b=1.4, eye='-', mark='*thud*'), k(.7, 'thr_l', y=1.5, b=1.4, eye='-', mark='...'), k(.88, y=.4, b=.4, eye='^')],
        [], g='play', act=('roll', 'threshold'), prefer=['happy'], say=["Dead. Convincing. Applaud.", "Rolled over. Dog house approves."])
    # ---------------- test
    o.r('tap_for_hollow', 'Tapping the left planks with his bill to hear which one is hollow', 16, 'none',
        [k(.12, 'plank_l', x=1.2, y=.6, b=.3, mark='tok'), k(.3, 'plank_l', x=.7, y=-.2, b=-.2, l=1, mark='tok'), k(.55, x=-.5, y=-.5, w=.4, eye='-'), k(.75, 'plank_l', x=1.2, y=.6, b=.5, mark='tonk'), k(.9, eye='^')],
        [], g='test', act=('tap', 'planks'))
    o.r('count_the_bolts', 'Tapping each low bolt along the bottom rail and counting under his breath', 20, 'none',
        [k(.1, 'bolt_l1', x=.8, y=1.4, b=.6, mark='1'), k(.28, 'bolt_l2', x=1, y=1.2, b=.3, l=1, mark='2'), k(.46, 'bolt_l3', x=.6, y=1, b=.8, r=1, mark='3'), k(.66, 'bolt_r', x=1.1, y=1.4, b=.4, l=1, mark='4'), k(.86, x=-.4, y=-.2, w=.4, eye='-', mark='four')],
        [], g='test', act=('count', 'bolts'), prefer=['curious'])
    o.r('put_a_shoulder_to_it', 'Putting his shoulder to the door frame to see whether the whole house tips', 18, 'none',
        [k(.12, x=.2, y=.3), k(.3, 'frame_l', x=.8, y=.5, b=.5, mark='hnnh'), k(.5, 'frame_r', x=.9, y=.6, b=.8, l=1, mark='HNNNH'), k(.7, x=-.5, y=-.3, w=.7, eye='-'), k(.88, eye='^')],
        [], g='test', act=('press', 'frame'), ages=GROWN)
    o.r('sniff_the_right_planks', 'Snuffling along the right planks to find out what has been leaning there', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'plank_r', x=1, y=1, b=.4, mark='snf'), k(.5, 'plank_r', x=1.2, y=.8, b=.5, mark='snf snf'), k(.7, x=-.2, y=.3, eye='>', mark='ugh'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'planks'), prefer=['curious'])
    o.r('measure_the_rain_in_the_bowl', 'Plumbing the bowl with a wing to measure how much rain it caught', 16, 'wing',
        [k(.15, 'bowl_l', reach=.6, x=.3, y=.5), k(.35, 'bowl_l', reach=1, x=.5, y=1, b=.4, mark='plip'), k(.55, x=.1, y=.2, w=.6, eye='-', mark='two wings'), k(.75, x=-.2, y=-.2, eye='^')],
        [], g='test', act=('measure', 'bowl'), when=['water>.2'])
    o.r('ring_the_bowl', 'Tapping the bowl rim from side to side to hear what note it is', 16, 'none',
        [k(.12, 'bowl_l', x=1, y=1.4, b=.3, mark='ting'), k(.3, 'bowl_r', x=1, y=1.4, b=.3, mark='tong'), k(.5, x=-.3, y=-.2, eye='-', mark='B flat'), k(.7, 'bowl_l', x=1, y=1.4, b=.5, mark='dink'), k(.88, eye='^')],
        [], g='test', act=('ring', 'bowl'))
    o.r('stand_by_the_frame', 'Standing tall beside the door frame to see which of them is higher', 18, 'none',
        [k(.15, 'door_dark', x=.8, y=.8, b=.3), k(.35, 'frame_l', x=.1, y=-1.6, b=-1.5, w=.4, eye='O'), k(.6, 'frame_l', x=.1, y=-1.8, b=-1.7, w=.6, eye='>'), k(.8, x=-1.2, y=1.4, b=1.4, w=0, eye='-', mark='ugh')],
        [], g='test', act=('compare', 'frame'))
    o.r('crane_at_the_sign', 'Craning at the sign above the door and spelling it out letter by letter', 18, 'wing',
        [k(.15, y=-.8, x=-.2), k(.3, y=-1.2, x=-.4, reach=.8, b=-.3, eye='O'), k(.5, y=-1.5, x=-.4, reach=1, b=-.5, mark='C H E E'), k(.7, y=-1.5, x=-.5, reach=1, b=-.5, eye='>', mark='S E'), k(.88, y=-.2, eye='^')],
        [], g='test', act=('measure', 'sign'), far=True, say=["Six letters. All mine.", "CHEESE. I checked. It is a good name."])
    # ---------------- rest
    o.r('lean_on_warm_planks', 'Leaning his belly against sun-warmed planks with his eyes shut', 24, 'none',
        [k(.15, y=.2, x=.3), k(.35, 'plank_r', x=.8, y=.4, b=.3, eye='-'), k(.6, 'plank_r', x=1, y=.7, b=.7, eye='-', mark='ahh'), k(.85, 'plank_r', x=1, y=.7, b=.7, eye='-')],
        [(.6, 'warm')], g='rest', act=('lean', 'planks'), when=['sun', 'warmth>.3'], prefer=['tired'])
    o.r('sit_on_the_sill_at_dusk', 'Sitting on the sill with his chin up, watching the light go out of the garden', 26, 'none',
        [k(.15, 'sill_b', perch=1, y=.3, b=.2), k(.4, 'sill_b', perch=1, y=.5, b=.9, eye='-'), k(.7, 'sill_b', perch=1, y=.4, b=.9, eye='-', mark='...'), k(.9, 'sill_b', perch=1, y=.1, b=.3, eye='o')],
        [], g='rest', act=('sit', 'sill'), when=['dusk'], prefer=['happy'], say=["Light goes. I stay. Efficient.", "Best seat on the lot, and it is a step."])
    o.r('sulk_at_the_frame', 'Standing at the door frame with his back turned, refusing to explain', 24, 'none',
        [k(.15, x=-.5, y=.3, w=.4), k(.35, 'frame_l2', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'frame_l2', x=-1, y=1.4, b=.9, l=1, eye='-', mark='hmph'), k(.85, 'frame_l2', x=-1, y=1.6, b=1.1, eye='-')],
        [], g='rest', act=('sulk', 'frame'), when=['sad'], prefer=['grumpy'], say=["Not sulking. Facing the other way. Different.", "The house did this. I am saying nothing."])
    o.r('wait_at_the_threshold', 'Waiting at the threshold with his bill pointed down the path', 26, 'none',
        [k(.15, y=.2, x=.2), k(.4, 'thr_l', x=.5, y=-.2, b=.3, eye='>'), k(.65, 'thr_l', x=.7, y=-.3, b=.3, eye='>', mark='...'), k(.85, 'thr_l', x=.4, y=.3, b=.5, eye='-', mark='sigh')],
        [], g='rest', act=('wait', 'threshold'), when=['lonely'])
    # ---------------- weather
    o.r('bail_out_the_rain', 'Bailing the rainwater out of the bowl with quick flicks of a wing', 20, 'wing',
        [k(.15, 'bowl_l', reach=.6, x=.3, y=.6), k(.35, 'bowl_l', reach=1, x=.6, y=1, b=.4, w=.5, mark='flick'), k(.55, 'bowl_l', reach=1, x=.6, y=1, b=.5, mark='flick'), k(.75, x=-.3, y=.2, eye='-', mark='ugh'), k(.9, eye='^')],
        [(.55, 'bail')], g='weather', act=('scoop', 'bowl'), when=['water>.3'], prefer=['grown'])
    o.r('crack_the_bowl_ice', 'Hammering the iced-over bowl with his bill until the top cracks', 18, 'none',
        [k(.15, x=.4, y=.4), k(.3, 'bowl_r', x=1, y=1.3, b=.4, mark='tak'), k(.5, x=.4, y=.4, w=.4), k(.65, 'bowl_r', x=1.1, y=1.5, b=.6, mark='CRACK'), k(.85, x=.1, eye='^')],
        [(.65, 'scrape')], g='weather', act=('chip', 'bowl'), when=['cold', 'frost>.4', 'water>.2'], prefer=['grumpy'])
    o.r('scrape_the_frost', 'Scraping the frost off the left planks with the edge of a wing', 18, 'wing',
        [k(.12, 'plank_l', reach=.6, x=.2, y=.5), k(.3, 'plank_l', reach=1, x=.3, y=.7, b=.3), k(.5, 'plank_l', reach=1, x=.3, y=.7, b=.4, mark='skr'), k(.7, 'plank_r', reach=1, x=.3, y=.6, b=.3), k(.88, eye='-')],
        [(.5, 'scrape')], g='weather', act=('scrape', 'planks'), when=['cold', 'frost>.3'])
    o.r('cool_his_feet', 'Standing in the bowl with the sun on his back to cool his feet', 24, 'none',
        [k(.15, y=.2, b=.1), k(.35, 'bowl_l', perch=1, y=.5, b=.4, l=1, eye='-'), k(.6, 'bowl_l', perch=1, y=.6, b=.6, r=1, eye='-', mark='aah'), k(.85, 'bowl_l', perch=1, y=.4, b=.4, eye='^')],
        [(.6, 'cool')], g='weather', act=('cool', 'bowl'), when=['sun', 'warm', 'water>.3'], prefer=['happy'])
    o.r('shelter_from_the_rain', 'Hugging the right planks as close as he can get while the rain comes down', 28, 'none',
        [k(.15, y=.2, x=.2), k(.35, 'bolt_r', x=-.4, y=.9, b=.7, w=.6), k(.6, 'bolt_r', x=-1.2, y=1.6, b=1.6, w=.8, eye='-', mark='brr'), k(.85, 'bolt_r', x=-1.2, y=1.6, b=1.6, w=.8, eye='-')],
        [], g='weather', act=('shelter', 'planks'), when=['wet', 'obj_wetness<.6'], say=["Dry-ish. The eave tries. I respect it.", "Rain, again. As if I asked."])
    o.r('brace_the_frame_in_a_gale', 'Gripping the door frame with both feet braced while the wind comes through', 22, 'none',
        [k(.15, y=.3, x=.3), k(.35, 'frame_r2', x=.8, y=.6, b=.6, w=.7, l=1), k(.6, 'frame_r2', x=1, y=.8, b=.9, w=1, eye='>', mark='hnng'), k(.85, 'frame_r2', x=.6, y=.6, b=.5, w=.5, r=1)],
        [], g='weather', act=('brace', 'frame'), when=['windy'])
    # ---------------- show
    o.r('bellow_at_the_sign', 'Bellowing up at the sign that this is, in fact, his house', 18, 'none',
        [k(.15, y=-.6, x=-.3), k(.35, y=-1.6, x=-1.2, b=-1.5, w=.5, eye='O', mark='MY HOUSE'), k(.55, y=-1.8, x=-1.2, b=-1.8, w=1, eye='>', mark='MINE'), k(.75, y=-.4, x=-.2, w=.4, eye='^')],
        [], g='show', act=('shout', 'sign'), far=True, say=["Says CHEESE. Spelled it myself.", "Sign agrees. Sign is on my side."])
    o.r('pose_at_the_frame', 'Posing against the door frame like the cover of a magazine about kennels', 22, 'none',
        [k(.15, y=.2, x=.2), k(.35, 'frame_l2', x=.2, y=-.4, b=-.3, w=.5, eye='-'), k(.55, 'frame_r2', x=.3, y=-.6, b=-.3, w=.7, eye='^'), k(.8, 'frame_r2', x=.3, y=-.7, b=-.3, w=.9, eye='^', mark='click')],
        [], g='show', act=('pose', 'frame'), prefer=['happy'], say=["Kennels Monthly. Cover price: nothing.", "Hold still. They are always watching."])
    o.r('give_the_house_tour', 'Giving the house a tour: the bolts, the dark doorway, the planks and the bowl', 28, 'none',
        [k(.1, 'bolt_l2', x=.6, y=.8, w=.5, mark='bolts'), k(.3, 'door_dark', x=.7, y=-.2, w=.8, mark='door'), k(.5, 'plank_r', x=.8, y=.4, w=1, mark='planks'), k(.7, 'bowl_r', perch=1, x=.6, y=.5, w=.9, mark='bowl'), k(.9, y=1, b=.5, w=1, eye='^')],
        [], g='show', act=('present', 'house'), say=["Home. Bolts, a bowl and zero staff.", "Tour ends here. Tipping is encouraged."])
    o.r('argue_with_the_knot', 'Jabbing a wing at the right knot and telling it to stop staring', 20, 'wing',
        [k(.15, y=.1, x=.2), k(.35, 'knot_r', reach=.8, x=.8, y=-.3, b=-.1, eye='>', mark='what'), k(.55, 'knot_r', reach=1, x=1, y=-.4, b=-.2, eye='O', mark='WHAT'), k(.75, x=-.3, y=.1, eye='-', mark='creepy')],
        [], g='show', act=('argue', 'knot'), ages=GROWN, prefer=['grumpy'])
    o.r('tightrope_the_sill', 'Walking the sill like a tightrope with his wings out and his chin up', 20, 'none',
        [k(.12, 'sill_b', perch=1, y=-.2, b=.2, w=.7, l=1), k(.32, 'sill_b', perch=1, y=-.4, b=-.1, w=1, r=1), k(.55, 'sill_a', perch=1, y=-.4, b=-.2, w=1, l=1, eye='O'), k(.78, 'sill_a', perch=1, y=-.2, b=.1, w=.8, r=1), k(.9, y=.3, w=0, eye='^')],
        [], g='show', act=('balance', 'sill'), prefer=['young', 'happy'])
    # ---------------- mishap
    o.r('slip_on_the_wet_sill', 'Skidding along the wet sill and ending up flat on the doorstep', 16, 'none',
        [k(.15, 'sill_a', perch=1, x=.4, y=.2, b=.3, l=1), k(.3, 'sill_a', perch=1, x=.8, y=-.3, b=-.5, w=1, eye='O'), k(.5, 'thr_l', x=1.2, y=1.4, b=1.3, w=1, mark='FWAP'), k(.75, y=.8, b=.6, eye='@'), k(.9, eye='-')],
        [(.5, 'muddy')], g='mishap', act=('slip', 'sill'), when=['obj_wetness>.4'], say=["Floor won. Floor always wins.", "Meant to lie down. Meant to do it dramatically."])
    o.r('jammed_in_the_doorway', 'Charging the doorway too wide and jamming at the shoulders', 22, 'none',
        [k(.15, x=.5, eye='>'), k(.3, 'frame_l', x=1.2, y=.5, b=.7, mark='oof'), k(.5, 'door_dark', x=1.4, y=.5, b=1, l=1, eye='O', mark='mmf'), k(.7, 'door_dark', x=1.4, y=.5, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
        [(.7, 'dent')], g='mishap', act=('stuck', 'doorway'), ages=GROWN, prefer=['young', 'grumpy'], obj=[(.5, dict(shake=.5)), (.7, dict(shake=1))],
        say=["Too wide. Entirely the doorway's fault.", "Popped out. Dignity stayed inside."])
    o.r('tail_snagged_on_a_bolt', 'Backing away and hooking his tail feathers on a bolt', 18, 'none',
        [k(.15, x=-.2, y=.2), k(.35, 'bolt_l3', x=-.9, y=.6, b=.4, l=1, mark='tug'), k(.55, 'bolt_l3', x=-1.2, y=.7, b=.8, w=.6, eye='O', mark='RRIP'), k(.75, x=.6, y=.8, b=.5, eye='@'), k(.9, eye='-')],
        [], g='mishap', act=('hook', 'bolt'), say=["Lost a feather. It is a bolt now.", "Backing up: not my event."])
    o.r('walked_into_the_frame', 'Strolling out with his eyes fixed up at the sign and walking straight at the frame', 16, 'none',
        [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'door_dark', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'frame_r', x=1.3, y=.3, b=.5, eye='O', mark='BONK'), k(.65, x=-1, y=-.2, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'frame'), say=["Looking at the sign. Not looking at the frame. Learned.", "Wood: hard. Beak: also hard. Draw."])
    o.r('stub_a_toe_on_the_bowl', 'Stubbing a toe against the bowl rim and hopping about while the water sloshes', 16, 'none',
        [k(.15, y=.1, x=.2), k(.3, 'bowl_r', x=.4, y=.4, b=.4, l=1, mark='tk'), k(.48, 'bowl_r', x=.2, y=.2, b=1, l=1, eye='O', mark='OW'), k(.68, x=-.2, y=-.4, b=-.7, l=1, w=.8, eye='@'), k(.88, eye='-')],
        [(.48, 'slosh')], g='mishap', act=('kick', 'bowl'), when=['water>.2'], say=["The bowl moved. Never trust a bowl.", "Toe: one. Bowl: two. Bowl is winning."])
    o.r('shake_off_like_a_dog', 'Shaking himself off like a dog and spraying the planks', 16, 'none',
        [k(.15, 'plank_l', x=.2, y=.2, b=.3), k(.3, 'plank_l', x=.3, y=.3, b=.8, w=1, mark='brrrr'), k(.45, 'plank_l', x=.3, y=.3, b=.8, w=0, l=1), k(.6, 'plank_l', x=.3, y=.3, b=.8, w=1, r=1, mark='BRRR'), k(.82, y=.2, w=.3, eye='^')],
        [(.45, 'soak')], g='mishap', act=('shake', 'feathers'), when=['wet'], prefer=['happy'])
    o.r('fit_the_doorway_side_on', 'Turning side-on at the doorway to find out if two ducks would fit', 18, 'none',
        [k(.15, 'door_dark', x=.2, y=.2), k(.35, 'frame_r', x=.6, y=.3, b=.2, w=.5), k(.55, 'frame_l', x=.9, y=.4, b=.4, w=.9, eye='-'), k(.75, 'door_dark', x=.3, y=-.2, w=0, eye='^', mark='two')],
        [], g='use', act=('fit', 'doorway'), say=["Two ducks. Tight. Cosy. Fine.", "Fits. I would be the one at the front."])
    return o


def toy_car():
    # Drawing (66 x 39 cells, 4.9 px a row, tyre bottoms 15 px up): cab rows 7-18 with two panes (top 151 px, pane bottoms 107 px), body box rows 18-29
    # with a trim line at row 23 (73 px) and a short bar at row 20 (87 px), two lamps at row 26 (58 px), tyres cols 11-27 and 40-55 rows 28-35 with hubs at
    # row 31 (34 px) and tread bands at rows 27 and 35, the body's lower edge row 29 (44 px). Nothing here moves: only the whole car can sway or shake.
    o = Obj('toy_car', 'placed',
            fields=dict(lit=(0, 0, 1), frost=(0, 0, 1), rock=(0, 0, 1), warmth=(0, 0, 1)),
            physics=[('lit', 'rate', -.0005, 'always'), ('lit', 'rate', -.004, 'windy'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('rock', 'rate', -.001, 'always'), ('rock', 'rate', .0025, 'windy'), ('warmth', 'rate', .0004, 'sun'), ('warmth', 'rate', -.0006, 'cold'), ('warmth', 'rate', -.0002, 'night')],
            effects=dict(
                polish=[('obj.dirt', 'add', -.25)], mud=[('obj.dirt', 'add', -.2)], wipe=[('obj.dirt', 'add', -.1)], dry=[('obj.wetness', 'add', -.3)],
                steady=[('rock', 'mul', .2)], shove=[('rock', 'add', .6)], rock=[('rock', 'set', 1)], peck=[('lit', 'set', 1)], smother=[('lit', 'set', 0)],
                cup=[('lit', 'add', .4)], honk=[('need.fun', 'add', 2)], chipfrost=[('frost', 'mul', .2)], warm=[('warmth', 'add', -.2), ('need.energy', 'add', 2)],
                toast=[('need.energy', 'add', 2)], muddy=[('obj.dirt', 'add', .1)]),
            anchors=dict(tail_low=(0.138, 0.711), tail_up=(0.138, 0.553), front_low=(0.862, 0.711), front_up=(0.862, 0.553), lamp_l=(0.185, 0.684), lamp_r=(0.800, 0.684),
                         wall_l=(0.200, 0.816), wall_r=(0.800, 0.816), hub_l=(0.292, 0.816), hub_r=(0.708, 0.816), tread_lb=(0.292, 0.921), tread_rb=(0.708, 0.921),
                         tread_lt=(0.292, 0.711), sill_a=(0.431, 0.763), sill_b=(0.554, 0.763), trim_a=(0.246, 0.605), trim_b=(0.492, 0.605), trim_c=(0.769, 0.605),
                         panel_h=(0.585, 0.526), glass_a=(0.446, 0.421), glass_b=(0.600, 0.421), glass_c=(0.385, 0.342)))
    # ---------------- care
    o.r('polish_the_side', 'Polishing the side panel in slow circles with a wing', 18, 'wing',
        [k(.12, 'panel_h', reach=.6, x=.3, y=.3), k(.3, 'panel_h', reach=1, x=.5, y=.4, l=1), k(.5, 'trim_b', reach=1, x=.5, y=.5, r=1, mark='squk'), k(.7, 'panel_h', reach=1, x=.5, y=.4, l=1), k(.88, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'panel'), when=['obj_dirt>.3'], prefer=['grown'], obj=[(.5, dict(glow=.5))])
    o.r('pick_mud_out_of_the_tread', 'Picking dried mud out of the bottom tread, one chunk at a time', 20, 'none',
        [k(.12, 'tread_lb', x=.6, y=1.2, b=.6), k(.3, 'tread_lb', x=1.1, y=1.7, b=.8, mark='pk'), k(.5, 'tread_rb', x=1.1, y=1.6, b=.7, l=1, mark='pk'), k(.7, 'tread_rb', x=1.2, y=1.8, b=.9, mark='pk'), k(.88, x=.2, y=.2, eye='^')],
        [(.5, 'mud')], g='care', act=('scrape', 'tread'), when=['obj_dirt>.3'], prefer=['curious'])
    o.r('wipe_the_lamps_clear', 'Wiping each lamp clear with the underside of a wing', 16, 'wing',
        [k(.12, 'lamp_l', reach=.6, x=.3, y=.3), k(.3, 'lamp_l', reach=1, x=.4, y=.2, w=.3, l=1), k(.55, 'lamp_r', reach=1, x=.4, y=.2, r=1, mark='squk'), k(.75, 'lamp_r', reach=.6, x=.2, y=.1), k(.9, eye='^')],
        [(.55, 'wipe')], g='care', act=('wipe', 'lamp'), when=['obj_dirt>.3'])
    o.r('hold_the_rocking_still', 'Bracing a wing at each end of the car until the rocking stops', 22, 'wing',
        [k(.12, 'tail_low', reach=.6, x=.4, y=.3, b=.3), k(.3, 'tail_low', reach=1, x=.6, y=.5, b=.7, mark='hnh'), k(.55, 'front_low', reach=1, x=.6, y=.5, b=.7, l=1), k(.78, 'front_low', reach=.6, x=.2, y=.2), k(.9, eye='-')],
        [(.55, 'steady')], g='care', act=('brace', 'car'), when=['rock>.3'], obj=[(.3, dict(sway=.5)), (.55, dict(sway=.1))])
    # ---------------- use
    o.r('shove_from_the_tail', 'Putting his breast to the tail and shoving the car forward', 18, 'none',
        [k(.12, 'tail_low', x=.4, y=.4, b=.3), k(.3, 'tail_low', x=1, y=.5, b=.8, l=1, mark='hup'), k(.5, 'tail_low', x=1.3, y=.4, b=1.2, r=1, mark='HNNH'), k(.72, x=-.3, y=-.2, w=.5, eye='O'), k(.88, eye='^')],
        [(.5, 'shove')], g='use', act=('shove', 'tail'), ages=GROWN, obj=[(.3, dict(sway=.4)), (.5, dict(sway=1)), (.7, dict(sway=.4))], say=["It moved. I shall be known as a mover.", "Pushed it. Left it. Maximum effort."])
    o.r('haul_back_by_the_lamp', 'Hauling the front end back by its lamp frame with his bill', 18, 'none',
        [k(.12, x=.4, y=.4), k(.3, 'lamp_r', x=1, y=1, b=.5, mark='hrr'), k(.5, 'lamp_r', x=-.4, y=1.2, b=1, mark='HRRR'), k(.7, 'lamp_r', x=-.6, y=1.3, b=1.1, l=1), k(.88, x=.1, eye='-')],
        [(.5, 'shove')], g='use', act=('pull', 'lamp'), ages=GROWN, obj=[(.3, dict(sway=-.3)), (.5, dict(sway=-.8)), (.7, dict(sway=-.2))])
    o.r('rock_it_from_the_sill', 'Shouldering the sill from side to side to get the whole car rocking', 22, 'none',
        [k(.12, x=.3, y=.4), k(.3, 'sill_a', x=.8, y=.9, b=.6, mark='hup'), k(.5, 'sill_b', x=.9, y=.9, b=.7, l=1), k(.7, 'sill_a', x=.9, y=.9, b=.7, r=1), k(.88, x=.2, w=.5, eye='^')],
        [(.5, 'rock')], g='use', act=('rock', 'car'), obj=[(.3, dict(sway=.5)), (.5, dict(sway=-.9)), (.7, dict(sway=.9)), (.85, dict(sway=-.4))], say=["Rocks nicely. Like a boat. A bad one.", "Car goes left. Car goes right. Duck wins."])
    o.r('peck_the_lamp_awake', 'Pecking the left lamp until it wakes up', 14, 'none',
        [k(.15, x=.4, y=-.3), k(.3, 'lamp_l', x=1, y=.6, b=.3, mark='tk'), k(.5, 'lamp_l', x=1.1, y=.6, b=.3, mark='tk tk', eye='O'), k(.7, x=.1, y=-.4, w=.5, eye='^'), k(.88, eye='o')],
        [(.5, 'peck')], g='use', act=('peck', 'lamp'), when=['lit<.5'], obj=[(.5, dict(glow=1)), (.7, dict(glow=.6))], prefer=['curious'], say=["Awake. You are welcome. Do not blink.", "Lamp on. I fear no dark. I fear some dark."])
    o.r('smother_the_right_lamp', 'Wrapping a wing round the right lamp until the glow goes out', 18, 'wing',
        [k(.15, 'lamp_r', reach=.5, x=.3, y=.3), k(.35, 'lamp_r', reach=1, x=.5, y=.5, b=.4, w=1, mark='fwmp'), k(.6, 'lamp_r', reach=1, x=.5, y=.5, b=.5, w=1), k(.8, x=.1, y=.2, eye='-', mark='night')],
        [(.6, 'smother')], g='use', act=('wrap', 'lamp'), when=['lit>.5'], obj=[(.35, dict(glow=.6)), (.6, dict(glow=0))])
    o.r('press_the_hub_like_a_horn', 'Pressing the left hub like a horn button and answering with a honk of his own', 16, 'none',
        [k(.15, x=.3, y=.4, b=.2), k(.3, 'hub_l', x=.9, y=1.2, b=.6, mark='beep'), k(.5, 'hub_l', x=1, y=1.4, b=.7, eye='O', mark='HONK'), k(.7, x=-.4, y=-.5, w=.7, eye='^'), k(.88, eye='o')],
        [(.5, 'honk')], g='use', act=('press', 'hub'), prefer=['happy'])
    # ---------------- play
    o.r('bounce_off_the_tyre', 'Bouncing off the left tyre wall like a trampoline', 16, 'none',
        [k(.12, 'wall_l', x=.6, y=.3, b=.4), k(.3, 'wall_l', x=1.1, y=.5, b=1.3, l=1, mark='boing'), k(.5, y=-.9, b=-1.2, w=1, eye='O'), k(.68, 'wall_l', x=1.1, y=.5, b=1.4, r=1, mark='BOING'), k(.86, y=.2, b=.3, eye='^')],
        [(.68, 'honk')], g='play', act=('hop', 'tyre'), prefer=['young', 'happy'], obj=[(.3, dict(sway=.3)), (.68, dict(sway=.5))])
    o.r('drum_the_trim_line', 'Drumming along the trim line from one end to the other like a xylophone', 20, 'wing',
        [k(.12, 'trim_a', reach=.7, w=.4, mark='tik'), k(.3, 'trim_a', reach=1, w=.8, mark='tak'), k(.5, 'trim_b', reach=1, w=.8, mark='tik'), k(.7, 'trim_c', reach=1, w=.9, mark='TSH'), k(.88, y=.8, b=.4, w=1, eye='^')],
        [], g='play', act=('drum', 'trim'), ages=GROWN, say=["Car percussion. Four notes, one of them rust.", "I would tour this. The car says no."])
    o.r('race_between_the_hubs', 'Sprinting from the left hub to the right and slapping each with a wing', 16, 'none',
        [k(.12, 'hub_l', x=.5, y=.9, b=.5, l=1, mark='slap'), k(.3, y=-.3, b=-.5, w=.9), k(.5, 'hub_r', x=.6, y=.9, b=.6, r=1, mark='SLAP'), k(.7, y=-.3, b=-.5, w=.9), k(.88, 'hub_l', x=.5, y=.9, b=.5, l=1)],
        [], g='play', act=('race', 'hubs'), prefer=['young', 'happy'])
    o.r('peek_round_each_tyre', 'Peeking round the left tyre, then the right, hunting an invisible rival', 20, 'none',
        [k(.12, 'wall_l', x=-.3, y=.5, b=.4, eye='>'), k(.3, 'wall_l', x=.9, y=-.3, b=.2, eye='O'), k(.5, y=.3, b=-.4, w=.4), k(.68, 'wall_r', x=-.3, y=.5, b=.4, eye='>'), k(.85, 'wall_r', x=.9, y=-.3, b=.2, eye='O')],
        [], g='play', act=('seek', 'tyres'), prefer=['young'])
    o.r('rev_then_boot_the_tail', 'Revving at the left lamp with engine noises, then kicking the tail to launch it', 22, 'none',
        [k(.12, 'lamp_l', x=.8, y=.2, b=.3, mark='brrm'), k(.3, 'lamp_l', x=1, y=.4, b=.6, w=.5, mark='BRRRM'), k(.5, x=-.8, y=-.3, b=-.5, w=1, eye='>'), k(.68, 'tail_low', x=.4, y=.5, b=.8, l=1, mark='KICK'), k(.88, y=.2, eye='^')],
        [(.68, 'shove')], g='play', act=('kick', 'tail'), ages=GROWN, obj=[(.68, dict(sway=.9)), (.85, dict(sway=.2))], say=["Brrm. Kick. Go. Nothing. Brrm again.", "Launched it. In my head it is in Spain."])
    o.r('donut_round_the_tyre', 'Spinning donuts round the right tyre with a wing out for the corners', 18, 'none',
        [k(.12, 'wall_r', x=.6, y=.3, w=.5, l=1), k(.3, 'wall_r', x=.2, y=.5, b=.6, w=1, r=1, mark='eeEEE'), k(.5, 'wall_r', x=.4, y=.6, b=.8, w=1, l=1), k(.7, 'wall_r', x=.2, y=.5, b=.6, w=1, r=1, mark='eeEEE'), k(.88, y=.3, b=.3, eye='@')],
        [], g='play', act=('spin', 'tyre'), prefer=['happy'])
    o.r('nudge_the_tail_like_a_cue', 'Lining up at the tail and tapping it along with the tip of his bill like a billiards cue', 22, 'none',
        [k(.12, x=.2, y=.2, b=.3, eye='-'), k(.3, 'tail_up', x=-.4, y=.4, b=.4), k(.45, 'tail_up', x=.9, y=.5, b=.5, mark='tk'), k(.6, 'tail_up', x=-.4, y=.4, b=.4), k(.75, 'tail_up', x=1, y=.5, b=.5, mark='tk')],
        [], g='play', act=('nudge', 'tail'), ages=GROWN, obj=[(.45, dict(sway=.3)), (.75, dict(sway=.3))])
    # ---------------- test
    o.r('squeeze_the_tyre_wall', 'Squeezing the right tyre wall in his bill to gauge the air', 16, 'none',
        [k(.12, x=.4, y=.4), k(.3, 'wall_r', x=1, y=1, b=.5, mark='squk'), k(.5, 'tread_rb', x=1.2, y=1.4, b=.8, eye='O'), k(.7, x=-.2, y=.6, eye='-', mark='hm'), k(.88, eye='^')],
        [], g='test', act=('squeeze', 'tyre'), prefer=['curious'])
    o.r('knock_along_the_sill', 'Knocking along the sill from end to end and listening for hollow', 18, 'none',
        [k(.12, 'sill_a', x=1, y=1.3, b=.5, mark='tok'), k(.3, 'sill_a', x=.8, y=.4, b=-.3, l=1, mark='tok'), k(.55, x=-.5, y=-.4, w=.4, eye='-'), k(.75, 'sill_b', x=1, y=1.3, b=.6, mark='tonk'), k(.9, eye='^')],
        [], g='test', act=('knock', 'sill'))
    o.r('pace_off_the_length', 'Pacing the car from tail to front to measure it, nine steps, then twelve', 24, 'none',
        [k(.1, 'tail_low', x=.5, y=.3, l=1, mark='1'), k(.3, 'sill_a', x=.6, y=.4, r=1, mark='4'), k(.5, 'sill_b', x=.6, y=.4, l=1, mark='8'), k(.7, 'front_low', x=.6, y=.3, r=1, mark='12'), k(.88, x=-.3, y=-.2, eye='-', mark='twelve')],
        [], g='test', act=('measure', 'car'), prefer=['curious'], say=["Nine steps. Then twelve. Car got longer.", "Twelve ducks. Roughly. Do not check."])
    o.r('sniff_the_tread', 'Sniffing the lower tread to work out what it has been driven through', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'tread_lb', x=1, y=1.3, b=.5, mark='snf'), k(.5, 'tread_lb', x=1.2, y=1.5, b=.6, mark='snf snf'), k(.7, x=-.3, y=.3, eye='>', mark='ugh'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'tread'), prefer=['curious'])
    o.r('tap_the_cabin_glass', 'Tapping the cabin glass to find out whether anyone is driving', 16, 'none',
        [k(.12, 'glass_a', x=.8, y=-.3), k(.3, 'glass_a', x=1.1, y=-.2, b=.2, mark='tok'), k(.5, 'glass_b', x=1.1, y=-.2, b=.2, mark='tok tok'), k(.7, x=-.3, y=-.5, w=.4, eye='-', mark='nobody'), k(.88, eye='^')],
        [], g='test', act=('tap', 'glass'), ages=GROWN, say=["Nobody in. Car has been driving itself. Concerning.", "No answer. Fine. Rude."])
    o.r('lean_on_the_sill_for_weight', 'Hanging his full weight at the sill to see if the springs give', 16, 'none',
        [k(.15, 'sill_b', x=.5, y=.5, b=.3), k(.35, 'sill_b', x=.9, y=.8, b=.9, mark='creak'), k(.55, 'sill_b', x=1, y=.9, b=1.4, eye='O'), k(.8, x=-.2, y=-.2, eye='-', mark='hm')],
        [], g='test', act=('weigh', 'sill'), obj=[(.35, dict(sway=.3)), (.55, dict(sway=.6))], prefer=['curious'])
    o.r('count_the_tyre_rings', 'Counting the rings of the left tyre from the outside in', 20, 'none',
        [k(.1, 'wall_l', x=.4, y=.8, b=.3, mark='1'), k(.3, 'tread_lt', x=.7, y=1, b=.5, mark='2'), k(.5, 'hub_l', x=.5, y=1.2, b=.7, mark='3'), k(.7, 'wall_l', x=-.2, y=.3, eye='-', mark='four?'), k(.88, eye='^')],
        [], g='test', act=('count', 'rings'))
    o.r('listen_for_an_engine', 'Pressing an ear to the side panel and listening for an engine', 18, 'none',
        [k(.12, x=.2, y=-.3), k(.3, 'panel_h', x=.5, y=-.3, b=.3, eye='-'), k(.55, 'panel_h', x=.7, y=-.2, b=.5, eye='-', mark='...'), k(.78, x=-.3, y=-.5, w=.5, eye='O', mark='nothing')],
        [], g='test', act=('listen', 'car'), ages=GROWN)
    o.r('hug_the_tyre_to_measure', 'Hugging the left tyre to see whether his wingspan reaches round it', 18, 'none',
        [k(.12, 'wall_l', x=.4, y=.4, w=.3), k(.3, 'wall_l', x=.6, y=.6, b=.5, w=1, mark='hnf'), k(.55, 'wall_l', x=.7, y=.7, b=.8, w=1, eye='>'), k(.78, x=-.2, y=-.2, w=0, eye='-', mark='not quite')],
        [], g='test', act=('measure', 'tyre'))
    # ---------------- rest
    o.r('nap_against_the_tyre', 'Dozing against the right tyre wall with his bill tucked under a wing', 28, 'none',
        [k(.15, y=.3, x=.3), k(.35, 'wall_r', x=.9, y=.9, b=.6, eye='-'), k(.6, 'wall_r', x=1.5, y=1.8, b=1.6, eye='-', mark='z'), k(.85, 'wall_r', x=1.6, y=2.2, b=2, eye='-', mark='zZ')],
        [(.6, 'toast')], g='rest', act=('nap', 'tyre'), when=['tired'])
    o.r('warm_up_at_the_panel', 'Soaking up the sun with his cheek flat against the warm side panel', 26, 'none',
        [k(.15, y=.3, x=.3), k(.35, 'panel_h', x=.6, y=.4, b=.3, eye='-'), k(.6, 'panel_h', x=.8, y=.7, b=.7, w=.3, eye='-', mark='ahh'), k(.85, 'panel_h', x=.8, y=.7, b=.7, eye='-')],
        [(.6, 'warm')], g='rest', act=('warm', 'panel'), when=['sun', 'warmth>.3'], prefer=['happy'])
    o.r('tell_the_lamp_his_day', 'Sitting nose to nose with the left lamp, telling it about his day', 28, 'none',
        [k(.15, y=.2, x=.2), k(.35, 'lamp_l', x=.6, y=.4, b=.6, eye='-'), k(.6, 'lamp_l', x=.7, y=.5, b=.9, eye='-', mark='...and then'), k(.85, 'lamp_l', x=.5, y=.4, b=.8, eye='^', mark='anyway')],
        [], g='rest', act=('sit', 'lamp'), when=['lonely'], say=["It listens. It is a lamp. Zero interruptions.", "Told it everything. It lit up. Supportive."])
    o.r('sulk_at_the_tail', 'Standing at the tail with his back to the car, muttering', 24, 'none',
        [k(.15, x=-.5, y=.3, w=.4), k(.35, 'tail_low', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'tail_low', x=-1, y=1.4, b=.9, l=1, eye='-', mark='hmph'), k(.85, 'tail_low', x=-1, y=1.6, b=1.1, eye='-')],
        [], g='rest', act=('sulk', 'tail'), when=['sad'], prefer=['grumpy'], say=["Do not look at the car. It knows what it did.", "Fine. Be a car. See if I care."])
    # ---------------- weather
    o.r('wipe_the_frost_off_the_glass', 'Wiping the frost off the cabin glass corner to corner with a wing', 20, 'wing',
        [k(.12, 'glass_a', reach=.7, x=.2, y=-.3), k(.3, 'glass_a', reach=1, x=.4, y=-.2, l=1), k(.5, 'glass_b', reach=1, x=.4, y=-.2, r=1, mark='skr'), k(.68, 'glass_c', reach=1, x=.4, y=-.3, l=1), k(.88, eye='-')],
        [(.5, 'chipfrost')], g='weather', act=('wipe', 'glass'), ages=GROWN, when=['cold', 'frost>.3'])
    o.r('chip_frost_from_the_tread', 'Chipping frost out of the upper tread with the tip of his bill', 18, 'none',
        [k(.12, x=.4, y=.5), k(.3, 'tread_lt', x=1, y=1, b=.4, mark='tk'), k(.5, 'tread_lt', x=1.1, y=1.1, b=.5, mark='tak'), k(.7, 'tread_rb', x=1.1, y=1.3, b=.6, l=1, mark='tk'), k(.88, eye='^')],
        [(.5, 'chipfrost')], g='weather', act=('chip', 'tread'), when=['cold', 'frost>.3'], prefer=['grumpy'])
    o.r('cup_the_lamp_in_the_wind', 'Cupping a wing round the left lamp to keep it alight against the wind', 22, 'wing',
        [k(.12, y=.2, x=.2), k(.3, 'lamp_l', reach=1, x=.5, y=.4, b=.4, w=1, mark='whoosh'), k(.55, 'lamp_l', reach=1, x=.5, y=.5, b=.6, w=1, eye='>'), k(.8, 'lamp_l', reach=.7, x=.3, y=.3, eye='-')],
        [(.55, 'cup')], g='weather', act=('brace', 'lamp'), when=['windy', 'lit>.3'], obj=[(.3, dict(glow=.6)), (.55, dict(glow=1))])
    o.r('chase_raindrops_down_the_glass', 'Chasing the raindrops down the cabin glass with his bill', 20, 'none',
        [k(.12, 'glass_c', x=.6, y=-.3), k(.3, 'glass_c', x=1, y=-.1, b=.2, eye='O'), k(.5, 'glass_a', x=1.1, y=-.1, b=.3, mark='tk'), k(.7, 'glass_b', x=1.1, y=-.1, b=.3, mark='tk'), k(.88, y=-.4, eye='^')],
        [], g='weather', act=('chase', 'drops'), ages=GROWN, when=['wet', 'obj_wetness>.3'], prefer=['happy'])
    o.r('dry_the_hubs_in_the_sun', 'Drying the wet hubs off with his tail feathers while the sun beats down', 20, 'none',
        [k(.12, 'hub_l', x=-.3, y=.5, b=.5), k(.3, 'hub_l', x=-.8, y=.8, b=.8, w=.6, mark='fwp'), k(.5, 'hub_r', x=-.8, y=.8, b=.8, w=.6, mark='fwp'), k(.7, 'hub_r', x=-.4, y=.5, b=.6), k(.88, eye='^')],
        [(.5, 'dry')], g='weather', act=('dry', 'hubs'), when=['sun', 'obj_wetness>.3'])
    o.r('warm_his_wings_at_the_lamp', 'Warming his wings at the lit left lamp on a cold evening', 24, 'none',
        [k(.15, y=.2, x=.2), k(.4, 'lamp_l', x=.5, y=.3, w=1, eye='-'), k(.65, 'lamp_l', x=.6, y=.4, b=.4, w=1, eye='-', mark='ahh'), k(.88, 'lamp_l', x=.4, y=.3, b=.3, w=.5, eye='^')],
        [(.65, 'toast')], g='weather', act=('warm', 'lamp'), when=['cold', 'lit>.5'], obj=[(.4, dict(glow=.6))])
    # ---------------- show
    o.r('preen_in_the_dark_glass', 'Preening at the cabin glass as if it were a mirror', 20, 'none',
        [k(.15, 'glass_a', x=.4, y=-.2, b=.2, eye='O'), k(.35, 'glass_a', x=.5, y=-.3, w=.5, eye='^', mark='hello'), k(.55, 'glass_b', x=.4, y=-.2, w=.8, l=1, eye='^'), k(.78, 'glass_a', x=.5, y=-.3, w=.4, eye='>', mark='lookin good')],
        [], g='show', act=('groom', 'glass'), ages=GROWN, prefer=['happy'], say=["Handsome devil in there. Same as ever.", "Reflection agrees with me. Always does."])
    o.r('whip_the_wing_off_the_hub', 'Whipping a wing off the hub like a magician revealing the trick', 18, 'wing',
        [k(.12, 'hub_r', reach=.5, w=.5, y=.5), k(.3, 'hub_r', reach=1, w=1, x=.5, y=.8, b=.4), k(.5, y=-.4, b=-.4, reach=1, w=1, eye='^', mark='TA-DA'), k(.7, 'hub_r', reach=.6, x=.2, y=.6), k(.88, y=.6, b=.4, eye='^')],
        [], g='show', act=('unwrap', 'hub'), prefer=['happy'], say=["Behold: a hub. It was there the whole time.", "Gasp, please. Gasp. There it is."])
    o.r('flash_a_turn_signal', 'Sweeping a wing twice past the right lamp to flash a left-turn signal, then going straight', 20, 'wing',
        [k(.12, 'lamp_r', reach=.6, x=.3, y=.2), k(.3, 'lamp_r', reach=1, x=.4, y=.3, w=.5, mark='tik'), k(.5, 'lamp_r', reach=1, x=.4, y=.3, w=.5, mark='tik'), k(.7, y=.1, x=-.5, w=.6, eye='>', mark='left'), k(.88, x=.4, eye='-', mark='straight')],
        [], g='show', act=('show', 'lamp'), obj=[(.3, dict(glow=.7)), (.5, dict(glow=.7))], say=["Indicated left. Went straight. Cars do it daily.", "Signal given. Nobody noticed. Perfect."])
    o.r('wave_the_car_in', 'Waving the car in with both wings like a parking attendant', 22, 'none',
        [k(.12, 'tail_up', x=.3, y=.2, w=.5), k(.3, 'tail_up', x=.4, y=-.2, b=-.2, w=1, mark='this way'), k(.5, 'front_up', x=.4, y=-.3, b=-.3, w=.4, l=1, mark='keep coming'), k(.72, 'front_up', x=.5, y=-.2, b=-.2, w=1, eye='O', mark='STOP'), k(.88, y=.2, w=0, eye='^')],
        [], g='show', act=('show', 'car'), ages=GROWN, say=["Perfectly parked. Carless. Still counts.", "Parking attendant. Zero pay. Full authority."])
    o.r('quote_a_price_at_the_hub', 'Sucking his bill at the gap above the tyre like a mechanic about to quote a price', 22, 'none',
        [k(.12, 'sill_a', x=.5, y=.3, b=.3), k(.3, 'sill_a', x=.9, y=.6, b=.5, eye='-', mark='hmmmm'), k(.52, 'sill_a', x=.3, y=.2, b=.2, w=.5, eye='O', mark='ooh'), k(.72, y=-.4, x=-.2, w=.7, eye='^', mark='four hundred'), k(.88, eye='-')],
        [], g='show', act=('show', 'arch'), say=["Four hundred. Cash. Plus a bread.", "Worrying noise. I will not say which. Four hundred."])
    o.r('take_a_bow_in_the_glow', 'Taking a bow beside the lit right lamp as if it were a stage light', 22, 'none',
        [k(.12, 'lamp_r', x=.2, y=.2, w=.5), k(.35, 'lamp_r', x=.2, y=-.3, w=1, eye='^', mark='thank you'), k(.6, 'lamp_r', x=.8, y=1.2, b=1, w=1), k(.85, 'lamp_r', x=.1, y=-.2, w=.5, eye='^')],
        [], g='show', act=('bow', 'lamp'), when=['lit>.5'], obj=[(.35, dict(glow=.8))])
    # ---------------- mishap
    o.r('slip_beside_the_tyre', 'Skidding on wet ground beside the tyre and sliding bill first at it', 16, 'none',
        [k(.15, x=.4, y=.2, b=.3, l=1), k(.3, x=.9, y=-.3, b=-.6, w=1, eye='O'), k(.5, 'wall_l', x=1.5, y=1.4, b=1, w=1, mark='FWAP'), k(.75, y=.8, b=.6, eye='@'), k(.9, eye='-')],
        [(.5, 'muddy')], g='mishap', act=('slip', 'tyre'), when=['obj_wetness>.4'], say=["Wet floor. Car side impact. Both fine.", "Slid. Stopped. Tyre did not move."])
    o.r('lunge_at_his_reflection', 'Lunging at his reflection at the cabin glass to settle who is better looking', 18, 'none',
        [k(.12, y=-.2, x=.2), k(.3, 'glass_a', x=.9, y=-.2, b=.3, eye='>', mark='you'), k(.48, 'glass_a', x=1.5, y=.2, b=.9, eye='O', mark='BONK'), k(.7, x=-1, y=-.3, b=-.3, w=1, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('chase', 'reflection'), ages=GROWN, say=["Reflection won. By a head. Mine.", "Bonk. Same duck. Same pain."])
    o.r('boot_the_tyre_too_hard', 'Booting the lower right tread harder than planned and hopping about on one foot', 16, 'none',
        [k(.12, y=.1, x=.2), k(.3, 'tread_rb', x=.4, y=.4, b=.4, l=1, mark='tk'), k(.48, 'tread_rb', x=.2, y=.2, b=1, l=1, eye='O', mark='OW'), k(.68, x=-.2, y=-.4, b=-.7, l=1, w=.8, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('kick', 'tyre'), say=["Tyre: soft. Tyre: not soft. Foot: sorry.", "I kicked a tyre. I am a man now. A duck."])
    o.r('walk_into_the_panel', 'Wandering along with his eyes fixed up at the cabin and walking straight at the side panel', 16, 'none',
        [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'sill_a', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'panel_h', x=1.3, y=.3, b=.5, eye='O', mark='BONK'), k(.65, x=-1, y=-.2, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'panel'), ages=GROWN, say=["The car was there the whole time. Rude.", "I looked up. Mistake. Panel was waiting."])
    o.r('snag_a_feather_on_the_lamp', 'Backing off and snagging a wing feather at the lamp frame', 18, 'none',
        [k(.15, x=-.2, y=.2), k(.35, 'lamp_r', x=-.9, y=.6, b=.4, l=1, mark='tug'), k(.55, 'front_low', x=-1.2, y=.7, b=.8, w=.6, eye='O', mark='RRIP'), k(.75, x=.6, y=.8, b=.5, eye='@'), k(.9, eye='-')],
        [], g='mishap', act=('hook', 'lamp'), say=["Lost a feather. The lamp has a trophy.", "It grabbed me. I will remember the lamp."])
    o.r('caught_by_the_rebound', 'Leaning in to look at the rocking car and catching the rebound square in his chest', 18, 'none',
        [k(.15, x=.3, y=.3), k(.3, 'panel_h', x=.7, y=.5, b=.3, eye='O'), k(.5, 'sill_a', x=-1.2, y=-.4, b=-.7, w=1, eye='@', mark='OOF'), k(.7, y=1.2, b=1, eye='@'), k(.88, y=.4, b=.4, eye='-')],
        [], g='mishap', act=('catch', 'car'), when=['rock>.3'], obj=[(.3, dict(sway=-.6)), (.5, dict(sway=.9)), (.7, dict(sway=-.2))], say=["It swung back. Of course it swung back.", "Got me. Fair. I started the rocking."])
    return o


def gazebo():
    # Drawing (106 x 54 cells, 8.5 px a row, standing line row 50): finial row 4 (390 px), roof rows 7-26, eave rows 27-28 (about 200 px), two posts of
    # three-wide columns at cols 17-20 and 82-85 (rows 29-47), outer lines at cols 10 and 95, a lattice panel on each side (cols 11-32 and 74-95, rows 40-48:
    # top rail 85 px, base rail 17 px) with diamonds and a flower cluster at row 45 (43 px), a potted plant at each foot (tubs row 50, foliage row 49).
    # The open middle is the floor at the standing line. Nothing here moves: only the whole gazebo can sway.
    o = Obj('gazebo', 'placed',
            fields=dict(leaves=(0, 0, 1), frost=(0, 0, 1), warmth=(0, 0, 1)),
            physics=[('leaves', 'rate', .0006, 'windy'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('warmth', 'rate', .0004, 'sun'), ('warmth', 'rate', -.0006, 'cold'), ('warmth', 'rate', -.0002, 'night')],
            effects=dict(
                sweepleaf=[('leaves', 'set', 0)], scrub=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)], polish=[('obj.dirt', 'add', -.15)],
                soil=[('obj.dirt', 'add', -.1)], scatter=[('leaves', 'mul', .4)], chip=[('frost', 'mul', .2)], warmfeet=[('warmth', 'add', -.2), ('need.energy', 'add', 2)],
                smear=[('obj.dirt', 'add', .1)], scratch=[('need.cleanliness', 'add', 1)], dent=[('obj.condition', 'add', -.1)], crowd=[('need.social', 'add', 2)],
                hush=[('need.energy', 'add', 1)]),
            anchors=dict(floor_l=(0.362, 0.943, 'inside surface'), floor_c=(0.505, 0.943, 'inside surface'), floor_r=(0.667, 0.943, 'inside surface'),
                         tub_l=(0.181, 0.943), tub_r=(0.819, 0.943), foliage_l=(0.133, 0.925), foliage_r=(0.848, 0.925),
                         rail_lo_l=(0.152, 0.906, 'surface'), rail_lo_m=(0.267, 0.906, 'surface'), rail_lo_r=(0.762, 0.906, 'surface'),
                         lat_l=(0.248, 0.830), lat_l2=(0.286, 0.811), lat_r=(0.781, 0.830), flower_l=(0.143, 0.849), flower_r=(0.819, 0.849),
                         rail_up_l=(0.229, 0.755), rail_up_r=(0.762, 0.755), post_l=(0.171, 0.698), post_r=(0.800, 0.698)))
    # ---------------- care
    o.r('sweep_the_leaves', 'Sweeping the floorboards clear of leaves with sideways wing strokes', 20, 'wing',
        [k(.12, 'floor_l', reach=.6, x=.3, y=.5), k(.3, 'floor_l', reach=1, x=.5, y=.7, l=1), k(.5, 'floor_c', reach=1, x=.6, y=.7, r=1, mark='shff'), k(.7, 'floor_r', reach=1, x=.5, y=.7, l=1), k(.88, eye='^')],
        [(.5, 'sweepleaf')], g='care', act=('sweep', 'floor'), when=['leaves>.3'], prefer=['grown'])
    o.r('scrub_the_lattice', 'Scrubbing the left lattice with a wing, one diamond at a time', 22, 'wing',
        [k(.12, 'lat_l', reach=.6, x=.3, y=.3), k(.3, 'lat_l', reach=1, x=.4, y=.4, l=1, mark='skrk'), k(.5, 'lat_l2', reach=1, x=.5, y=.4, r=1, mark='skrk'), k(.7, 'lat_l', reach=1, x=.4, y=.5, l=1), k(.88, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'lattice'), when=['obj_dirt>.3'])
    o.r('mop_the_wet_rail', 'Mopping the wet side rails with his breast and a lot of grunting', 22, 'none',
        [k(.12, 'rail_up_l', x=.3, y=-.3), k(.3, 'rail_up_l', x=.7, y=-.2, b=.3, mark='hff'), k(.5, 'rail_up_l', x=.9, y=-.1, b=.5), k(.7, 'rail_up_r', x=.7, y=-.2, b=.3, mark='hff'), k(.88, x=.1, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'rail'), ages=GROWN, when=['obj_wetness>.3'])
    o.r('wipe_the_post_clean', 'Wiping the right post clean with a wing, as high as he can reach', 18, 'wing',
        [k(.12, 'post_r', reach=.6, x=.4, y=-.3), k(.3, 'post_r', reach=1, x=.5, y=-.5, b=-.2, mark='skrk'), k(.5, 'post_r', reach=1, x=.6, y=-.7, b=-.3, l=1), k(.7, 'post_r', reach=1, x=.5, y=-.5, b=-.2, r=1, mark='skrk'), k(.88, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'post'), ages=GROWN, when=['obj_dirt>.3'])
    o.r('wipe_the_tub_rims', 'Wiping soil off both tub rims with the underside of a wing', 18, 'wing',
        [k(.12, 'tub_l', reach=.6, x=.3, y=.8, b=.3), k(.3, 'tub_l', reach=1, x=.5, y=1, b=.6, w=.3), k(.55, 'tub_r', reach=1, x=.5, y=1, b=.6, w=.3, mark='sff'), k(.75, 'tub_r', reach=.6, x=.2, y=.5), k(.9, eye='^')],
        [(.55, 'soil')], g='care', act=('wipe', 'tub'), when=['obj_dirt>.3'])
    # ---------------- use
    o.r('rest_his_wings_on_the_rail', 'Resting both wings along the right side rail and surveying the garden like a landlord', 24, 'none',
        [k(.15, y=.1, x=.3), k(.35, 'rail_up_r', x=.5, y=-.3, b=.2, w=.6, eye='-'), k(.6, 'rail_up_r', x=.8, y=-.4, b=.3, w=.8, eye='>', mark='hm'), k(.85, 'rail_up_r', x=.7, y=-.4, b=.3, w=.8, eye='>')],
        [], g='use', act=('lean', 'rail'), ages=GROWN)
    o.r('hold_the_entry_open', 'Holding the entry open with a wing for guests who are not coming', 22, 'wing',
        [k(.15, y=.1, x=.2), k(.35, 'floor_c', perch=1, reach=.8, y=-.2, b=-.1, mark='after you'), k(.6, 'floor_c', perch=1, reach=1, y=.4, b=.3, x=.4, eye='^', mark='madam'), k(.85, 'floor_c', perch=1, reach=.5, y=.1, eye='-', mark='...')],
        [], g='use', act=('open', 'entry'), prefer=['lonely'], say=["Nobody came. Door held anyway. Principle.", "After you. After you. Fine, me first."])
    o.r('scratch_his_back_on_the_post', 'Scratching his back up and down the left post with a happy groan', 20, 'none',
        [k(.15, 'post_l', x=-.5, y=.4, b=.4), k(.35, 'post_l', x=-1, y=1, b=1.2, eye='-', mark='ahh'), k(.55, 'post_l', x=-1, y=-1.2, b=-1.2, eye='-', mark='ooh'), k(.75, 'post_l', x=-1, y=1, b=1.2, eye='-'), k(.9, y=0, eye='^')],
        [(.55, 'scratch')], g='use', act=('groom', 'post'), ages=GROWN)
    o.r('rap_the_rail_to_order', 'Rapping the side rails with a wing to call the whole garden to order', 20, 'wing',
        [k(.12, 'rail_up_l', reach=.7, x=.2, y=-.2), k(.3, 'rail_up_l', reach=1, x=.3, y=-.3, w=.5, mark='tok tok'), k(.5, 'rail_up_r', reach=1, x=.3, y=-.3, w=.5, mark='TOK TOK'), k(.72, y=-.5, x=-.3, w=1, eye='O', mark='ORDER'), k(.9, eye='-')],
        [(.5, 'crowd')], g='use', act=('tap', 'rail'), ages=GROWN)
    # ---------------- play
    o.r('spin_round_the_post', 'Whirling round the right post by one wing until he cannot see straight', 18, 'none',
        [k(.12, 'post_r', x=.4, y=.2, w=.4), k(.3, 'post_r', x=.5, y=.3, w=.8, l=1), k(.5, 'post_r', x=-.5, y=.4, b=.4, w=1, r=1, eye='@'), k(.7, 'post_r', x=.6, y=.5, b=.5, w=1, l=1), k(.9, y=.6, b=.8, eye='@', mark='...')],
        [], g='play', act=('spin', 'post'), ages=GROWN, prefer=['young', 'happy'])
    o.r('count_to_ten_at_the_post', 'Counting to ten against the left post with his eyes shut, then spinning round to seek', 22, 'none',
        [k(.12, 'post_l', x=.6, y=.8, b=.5, eye='-', mark='one'), k(.3, 'post_l', x=.7, y=.9, b=.6, eye='-', mark='five'), k(.5, 'post_l', x=.7, y=.9, b=.6, eye='-', mark='TEN'), k(.7, y=-.5, x=-.4, w=1, eye='O', mark='ready!'), k(.88, y=.1, w=.3, eye='>')],
        [], g='play', act=('seek', 'post'), ages=GROWN, prefer=['young'])
    o.r('jump_out_at_the_lattice', 'Flattening himself against the lattice among the flowers and bursting out with a roar', 18, 'none',
        [k(.15, 'flower_r', x=-.3, y=.3, b=.4), k(.35, 'flower_r', x=-.4, y=.6, b=.7, eye='-'), k(.55, 'flower_r', x=-.4, y=.6, b=.7, eye='-', mark='...'), k(.7, y=-.8, b=-.8, w=1, eye='O', mark='RAAH'), k(.88, y=.3, eye='^')],
        [], g='play', act=('hide', 'lattice'), prefer=['young'], say=["RAAH. A flower flinched. I counted it.", "Lattice got the fright of its life."])
    o.r('rake_and_dive_the_leaves', 'Raking the leaves into a heap with his feet and diving flat into it', 24, 'none',
        [k(.12, 'floor_l', perch=1, x=.3, y=.5, b=.3, l=1), k(.3, 'floor_c', perch=1, x=.2, y=.7, b=.6, r=1, mark='shff'), k(.5, y=-.6, b=-.8, w=.8), k(.65, 'floor_c', perch=1, y=1.6, b=1.5, w=1, mark='FFWUMP'), k(.88, y=.3, b=.3, eye='^')],
        [(.65, 'scatter')], g='play', act=('rake', 'leaves'), when=['leaves>.3'], prefer=['happy', 'young'], say=["Leaf pile. Deep. Not deep enough.", "Dived. Landed. Leaves everywhere. Peak duck."])
    o.r('toss_leaves_like_confetti', 'Scooping up a bill of leaves and tossing them over his head like confetti', 20, 'none',
        [k(.12, 'floor_r', x=.8, y=1.3, b=.5), k(.3, 'floor_r', x=1.1, y=1.6, b=.8, mark='fff'), k(.5, y=-1.2, x=-.4, b=-.8, w=1, eye='^', mark='YAY'), k(.7, y=-.4, b=-.3, w=.8), k(.88, y=.2, eye='-')],
        [(.3, 'scatter')], g='play', act=('throw', 'leaves'), when=['leaves>.3'], prefer=['happy'])
    o.r('hop_the_board_seams', 'Hopping the floorboards from the right seam to the left, never touching a crack', 18, 'none',
        [k(.12, 'floor_r', perch=1, x=.3, y=-.3, b=-.4, l=1), k(.3, 'floor_r', perch=1, y=.3, b=.6, r=1, mark='hup'), k(.5, 'floor_c', perch=1, y=-.4, b=-.7, w=.6), k(.7, 'floor_l', perch=1, y=.3, b=.7, l=1, mark='hup'), k(.88, y=-.2, w=.4, eye='^')],
        [], g='play', act=('hop', 'boards'), prefer=['young', 'happy'])
    o.r('race_between_the_tubs', 'Sprinting from the left tub to the right and slapping each plant with a wing', 18, 'none',
        [k(.12, 'foliage_l', x=.6, y=1, b=.5, l=1, mark='slap'), k(.3, y=-.3, b=-.6, w=.9), k(.5, y=-.3, b=-.6, w=1), k(.7, 'foliage_r', x=.6, y=1, b=.5, r=1, mark='SLAP'), k(.88, x=.1, w=.5, eye='^')],
        [], g='play', act=('race', 'tubs'), prefer=['young'])
    # ---------------- test
    o.r('sniff_the_flowers', 'Sniffing the two flower clusters one after the other and rating them', 16, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'flower_l', x=1, y=.6, b=.3, mark='snf'), k(.5, 'flower_l', x=.4, y=.2, eye='-', mark='7/10'), k(.7, 'flower_r', x=1, y=.6, b=.3, mark='snf snf'), k(.88, x=.2, eye='^', mark='8/10')],
        [], g='test', act=('sniff', 'flowers'), prefer=['curious'], say=["Left: six. Right: seven. Both lying about being rose.", "Pollen. In the nose. Rating: sneeze."])
    o.r('knock_the_post_for_hollow', 'Knocking at each post in turn with his bill to hear which one is hollow', 16, 'none',
        [k(.12, 'post_r', x=1, y=-.4, mark='tok'), k(.3, 'post_r', x=.8, y=-.1, b=.3, mark='tok'), k(.5, x=-.4, y=-.5, w=.4, eye='-'), k(.7, 'post_l', x=1, y=-.3, b=.4, mark='tonk'), k(.9, eye='^')],
        [], g='test', act=('knock', 'post'), ages=GROWN)
    o.r('knock_the_tub', 'Knocking the left tub with his bill and listening to the clay answer', 14, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'tub_l', x=1, y=1.5, b=.5, mark='tok'), k(.5, 'tub_l', x=1.1, y=1.6, b=.6, mark='tonk'), k(.7, x=-.2, y=.3, eye='-', mark='hollow'), k(.88, eye='^')],
        [], g='test', act=('knock', 'tub'))
    o.r('count_the_diamonds', 'Counting the lattice diamonds from the post to the flowers', 22, 'none',
        [k(.1, 'lat_l2', x=.8, y=-.2, mark='1'), k(.3, 'lat_l', x=.9, y=.1, b=.2, mark='5'), k(.5, 'lat_l', x=.9, y=.4, b=.4, l=1, mark='11'), k(.7, 'flower_l', x=.9, y=.3, b=.3, r=1, mark='14'), k(.88, x=-.2, eye='-', mark='lost count')],
        [], g='test', act=('count', 'diamonds'), prefer=['curious'])
    o.r('pace_out_the_floor', 'Pacing the floor out in solemn waddles: nine across, nine back', 22, 'none',
        [k(.1, 'floor_r', perch=1, x=.4, y=.1, b=.2, l=1, mark='1'), k(.3, 'floor_c', perch=1, x=.3, y=.2, b=.3, r=1, mark='5'), k(.5, 'floor_l', perch=1, x=.4, y=.1, b=.2, l=1, mark='9'), k(.72, 'floor_c', perch=1, x=.2, y=.2, b=.3, r=1), k(.9, x=-.2, y=-.1, eye='-', mark='nine')],
        [], g='test', act=('measure', 'floor'), prefer=['curious'], say=["Nine across. Nine back. Floor is exactly a floor.", "Measured. It fits. I knew it would."])
    o.r('listen_at_the_post', 'Pressing an ear to the right post to hear whether the roof is humming', 18, 'none',
        [k(.12, 'rail_up_l', x=.2, y=-.2), k(.3, 'post_r', x=.5, y=-.3, b=.3, eye='-'), k(.55, 'post_r', x=.7, y=-.2, b=.5, eye='-', mark='...'), k(.78, x=-.3, y=-.5, w=.5, eye='O', mark='nothing')],
        [], g='test', act=('listen', 'post'), ages=GROWN)
    o.r('hang_off_the_rail', 'Hanging his full weight at the left side rail to see whether it holds a duck', 18, 'none',
        [k(.15, 'rail_up_l', x=.6, y=-.2, b=.2), k(.35, 'rail_up_l', x=1, y=.2, b=.8, mark='creak'), k(.55, 'rail_up_l', x=1, y=.4, b=1.4, eye='O'), k(.8, x=-.1, y=-.3, eye='-', mark='holds')],
        [], g='test', act=('weigh', 'rail'), ages=GROWN)
    o.r('stand_next_to_the_post', 'Standing back to back with the left post to see which of them is taller', 18, 'none',
        [k(.15, 'rail_up_l', x=-.3, y=.2, b=.3), k(.35, 'post_l', x=-.3, y=-1.6, b=-1.4, w=.4, eye='O'), k(.6, 'post_l', x=-.4, y=-1.8, b=-1.7, w=.6, eye='>', mark='taller'), k(.8, x=-1.2, y=1.4, b=1.4, w=0, eye='-', mark='ugh')],
        [], g='test', act=('compare', 'post'), say=["Post wins by a roof. Fair.", "Tall as a post. Almost. Practically."])
    # ---------------- rest
    o.r('lean_back_on_the_lattice', 'Leaning his back against the left lattice with his eyes shut', 24, 'none',
        [k(.15, y=.2, x=.2, w=.3), k(.35, 'lat_l', x=-.5, y=.5, b=.4, eye='-'), k(.6, 'lat_l', x=-.8, y=1.2, b=1.2, eye='-', mark='z'), k(.85, 'lat_l', x=-.8, y=1.3, b=1.5, eye='-')],
        [(.6, 'hush')], g='rest', act=('lean', 'lattice'), when=['tired'])
    o.r('sulk_at_the_rail', 'Sulking along the side rails with his back to the garden', 24, 'none',
        [k(.15, x=-.5, y=.3, w=.4), k(.35, 'rail_up_r', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'rail_up_l', x=-1, y=1.4, b=.9, l=1, eye='-', mark='hmph'), k(.85, 'rail_up_l', x=-1, y=1.6, b=1.1, eye='-')],
        [], g='rest', act=('sulk', 'rail'), ages=GROWN, when=['sad'], prefer=['grumpy'])
    o.r('wait_for_company', 'Waiting at the middle of the floor with his bill turned towards the garden path', 26, 'none',
        [k(.15, y=.2, x=.2), k(.4, 'floor_c', perch=1, x=.5, y=-.2, b=.2, eye='>'), k(.65, 'floor_c', perch=1, x=.7, y=-.3, b=.3, eye='>', mark='...'), k(.85, 'floor_c', perch=1, x=.4, y=.3, b=.5, eye='-', mark='sigh')],
        [], g='rest', act=('wait', 'floor'), when=['lonely'])
    o.r('perch_on_the_base_rail', 'Perching on the right base rail to watch the garden go dark', 28, 'none',
        [k(.15, 'rail_lo_r', perch=1, y=.2, b=.3), k(.4, 'rail_lo_r', perch=1, y=.5, b=.9, eye='-'), k(.7, 'rail_lo_r', perch=1, y=.4, b=.9, eye='-', mark='...'), k(.9, 'rail_lo_r', perch=1, y=.1, b=.3, eye='o')],
        [], g='rest', act=('perch', 'rail'), when=['dusk'], prefer=['happy'])
    # ---------------- weather
    o.r('stand_dry_in_the_rain', 'Standing dead centre with his wings tucked in, listening to the rain hammer the roof', 32, 'none',
        [k(.15, 'floor_l', perch=1, y=.1), k(.35, 'floor_c', perch=1, y=.6, x=.2, b=.6, w=0, eye='-'), k(.6, 'floor_c', perch=1, y=.9, x=.1, b=1.2, w=0, eye='-', mark='drum drum'), k(.85, 'floor_c', perch=1, y=.4, x=.2, b=.5, w=0, eye='^', mark='dry')],
        [], g='weather', act=('shelter', 'floor'), when=['wet'], say=["Dry. Smug. Listen to it fall on someone else.", "Roof works. Roof is my friend today."])
    o.r('chip_the_frost_off_the_rail', 'Chipping the frost off the side rails with the tip of his bill', 20, 'none',
        [k(.12, 'rail_up_l', x=.6, y=-.3), k(.3, 'rail_up_l', x=1, y=-.1, b=.3, mark='tk'), k(.5, 'rail_up_r', x=1, y=-.1, b=.4, mark='tak'), k(.7, 'rail_up_r', x=1, y=-.1, b=.4, mark='tk'), k(.88, eye='-')],
        [(.5, 'chip')], g='weather', act=('chip', 'rail'), ages=GROWN, when=['cold', 'frost>.3'], prefer=['grumpy'])
    o.r('scrape_frost_off_the_lattice', 'Scraping the frost off the right lattice with the edge of a wing', 20, 'wing',
        [k(.12, 'lat_r', reach=.6, x=.2, y=.2), k(.3, 'lat_r', reach=1, x=.3, y=.3, b=.2), k(.5, 'lat_r', reach=1, x=.3, y=.4, b=.3, mark='skr'), k(.7, 'flower_r', reach=1, x=.3, y=.3, b=.2), k(.88, eye='-')],
        [(.5, 'chip')], g='weather', act=('scrape', 'lattice'), when=['cold', 'frost>.3'])
    o.r('hold_the_post_in_the_gale', 'Gripping one post, then the other, with both feet braced while the wind comes through', 22, 'none',
        [k(.15, y=.3, x=.3), k(.35, 'post_l', x=.8, y=.6, b=.6, w=.7, l=1), k(.6, 'post_l', x=1, y=.8, b=.9, w=1, eye='>', mark='hnng'), k(.85, 'post_r', x=.6, y=.6, b=.5, w=.5, r=1)],
        [], g='weather', act=('brace', 'post'), ages=GROWN, when=['windy'])
    o.r('warm_his_feet_on_the_boards', 'Standing on the sun-warmed boards and lifting each foot in turn', 24, 'none',
        [k(.15, y=.1, b=.1), k(.35, 'floor_r', perch=1, y=.4, b=.3, l=1, eye='-'), k(.6, 'floor_r', perch=1, y=.4, b=.4, r=1, eye='-', mark='ahh'), k(.85, 'floor_r', perch=1, y=.3, b=.2, l=1, eye='^')],
        [(.6, 'warmfeet')], g='weather', act=('warm', 'floor'), when=['sun', 'warmth>.3'], prefer=['happy'])
    o.r('cool_off_in_the_draught', 'Holding his wings out at the open sides of the floor to cool off in the breeze', 24, 'none',
        [k(.15, y=.2, b=.2), k(.35, 'floor_l', perch=1, y=-.4, b=-.3, w=1, eye='-', mark='phew'), k(.6, 'floor_r', perch=1, y=-.5, b=-.4, w=1, eye='^', mark='ahh'), k(.85, 'floor_r', perch=1, y=-.2, b=-.1, w=.4, eye='-')],
        [], g='weather', act=('cool', 'floor'), when=['sun', 'warm'], prefer=['happy'], say=["Open sides. Free breeze. Zero rent.", "Fanning myself. Dignity: optional."])
    o.r('wrap_both_wings_round_the_flowers', 'Wrapping both wings round the left flowers to shield them from the gale', 22, 'wing',
        [k(.15, y=.3, x=.2), k(.35, 'flower_l', reach=.8, x=.5, y=.6, b=.4, w=1, mark='whoosh'), k(.6, 'flower_l', reach=1, x=.6, y=.8, b=.6, w=1, eye='>'), k(.85, 'flower_l', reach=.5, x=.3, y=.4, eye='-', mark='there')],
        [], g='weather', act=('wrap', 'flowers'), when=['windy'], prefer=['curious'])
    # ---------------- show
    o.r('bellow_up_at_the_roof', 'Bellowing up at the roof until it answers', 20, 'none',
        [k(.15, y=-.4), k(.35, 'floor_r', perch=1, y=-1.4, x=-.5, b=-.3, w=.5, eye='O', mark='HELLO'), k(.55, 'floor_r', perch=1, y=-1.6, x=-.6, b=-.4, w=1, eye='>', mark='HELLO!'), k(.78, 'floor_r', perch=1, y=-.4, x=-.2, w=.3, eye='-', mark='...hello')],
        [], g='show', act=('shout', 'roof'), say=["Echo is just me, later. Still the best audience.", "Roof says it back. Louder. Cheeky."])
    o.r('waltz_the_floor_alone', 'Waltzing the length of the floor with an invisible partner', 24, 'none',
        [k(.12, 'floor_l', perch=1, x=.2, y=-.2, b=-.2, w=.6, l=1), k(.3, 'floor_c', perch=1, x=.3, y=-.3, b=-.4, w=1, r=1), k(.5, 'floor_r', perch=1, x=.2, y=-.2, b=-.2, w=.6, l=1), k(.7, 'floor_c', perch=1, x=.3, y=-.3, b=-.4, w=1, r=1), k(.88, y=.4, b=.5, w=0, eye='^')],
        [], g='show', act=('dance', 'floor'), prefer=['happy'], say=["My partner is the best lead I ever had.", "One two three. One two floor."])
    o.r('tightrope_the_base_rail', 'Walking the left base rail like a tightrope with his wings out', 20, 'none',
        [k(.12, 'rail_lo_l', perch=1, y=-.2, b=.2, w=.7, l=1), k(.35, 'rail_lo_l', perch=1, y=-.4, b=-.1, w=1, r=1), k(.6, 'rail_lo_m', perch=1, y=-.4, b=-.2, w=1, l=1, eye='O'), k(.8, 'rail_lo_m', perch=1, y=-.2, b=.1, w=.8, r=1), k(.92, y=.3, w=0, eye='^')],
        [], g='show', act=('balance', 'rail'), prefer=['young', 'happy'])
    o.r('serenade_the_flowers', 'Crooning at the left flowers with a wing on his chest', 22, 'none',
        [k(.15, y=.2, x=.2), k(.35, 'flower_l', x=.6, y=-.2, b=.2, w=.5, eye='^', mark='la'), k(.6, 'flower_l', x=.8, y=-.4, b=.1, w=.8, eye='-', mark='LAAAH'), k(.85, 'flower_l', x=.4, y=.3, b=.4, w=.3, eye='^', mark='...')],
        [], g='show', act=('sing', 'flowers'), prefer=['happy'], say=["They leaned in. Wind, probably. Allow me this.", "Flowers: attentive. Roof: jealous."])
    o.r('pose_at_the_rail', 'Posing at the right side rail with one wing against the post like the cover of a magazine about gazebos', 22, 'none',
        [k(.15, y=.2, x=.2), k(.35, 'rail_up_r', x=.2, y=-.4, b=-.3, w=.5, eye='-'), k(.55, 'post_r', x=.3, y=-.6, b=-.3, w=.7, eye='^'), k(.8, 'post_r', x=.3, y=-.7, b=-.3, w=.9, eye='^', mark='click')],
        [], g='show', act=('pose', 'rail'), ages=GROWN, prefer=['happy'], say=["Gazebo Monthly. Cover price: one bread.", "Hold it. Hold it. Perfect. Now with attitude."])
    o.r('strut_in_like_a_bride', 'Strutting up to the middle of the floor with his wings back like a bride on a bad day', 24, 'none',
        [k(.12, 'floor_r', perch=1, x=.2, y=-.4, w=.5), k(.35, 'floor_r', perch=1, x=.3, y=-.6, b=-.3, w=.9, l=1, mark='dum dum de dum'), k(.6, 'floor_c', perch=1, x=.3, y=-.6, b=-.3, w=.9, r=1), k(.85, 'floor_c', perch=1, x=.3, y=-.5, w=.5, eye='^', mark='I do')],
        [], g='show', act=('show', 'entry'), say=["I do. I always do. Nobody asks me.", "Bouquet? No. Beak? Yes. Aisle: also yes."])
    o.r('argue_with_the_echo', 'Arguing with his own echo and losing every round', 24, 'none',
        [k(.15, 'floor_c', perch=1, x=.3, y=-.6, w=.4, mark='I win'), k(.35, 'floor_c', perch=1, x=.5, y=-.9, b=-.2, w=.8, eye='>', mark='I WIN'), k(.55, 'floor_r', perch=1, x=-.4, y=-.5, w=0, eye='O', mark='no I win'), k(.75, 'floor_r', perch=1, x=-.6, y=.4, b=.5, eye='-', mark='...hm')],
        [], g='show', act=('argue', 'roof'), prefer=['grumpy'], say=["Echo gets the last word. Always. Cheat.", "Won the argument. Until it replied."])
    # ---------------- mishap
    o.r('skid_on_the_leaves', 'Skidding on the loose leaves and ending up flat on his back at the entry', 16, 'none',
        [k(.15, 'floor_r', perch=1, x=.4, y=.2, b=.3, l=1), k(.3, 'floor_r', perch=1, x=.8, y=-.3, b=-.5, w=1, eye='O'), k(.5, 'floor_c', x=1.2, y=1.4, b=1.3, w=1, mark='FWAP'), k(.75, y=.8, b=.6, eye='@'), k(.9, eye='-')],
        [(.5, 'smear')], g='mishap', act=('slip', 'floor'), when=['leaves>.4'], say=["Leaves: slippery. Ego: bruised.", "The floor and I are no longer speaking."])
    o.r('head_through_a_diamond', 'Pushing his head through a lattice diamond and having to be a very long duck to get out', 24, 'none',
        [k(.15, x=.5, eye='>'), k(.3, 'lat_r', x=1.2, y=.4, b=.7, mark='oof'), k(.5, 'lat_r', x=1.3, y=.4, b=1, l=1, eye='O', mark='mmf'), k(.7, 'lat_r', x=1.3, y=.4, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
        [(.7, 'dent')], g='mishap', act=('stuck', 'lattice'), shown='head', prefer=['young', 'grumpy'], obj=[(.5, dict(shake=.4)), (.7, dict(shake=.6))],
        say=["Narrow diamond. Wide ambition.", "Out. Bill: stretched. Pride: elsewhere."])
    o.r('bonk_the_post', 'Gazing up at the roof beams and walking straight at the right post', 16, 'none',
        [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'floor_r', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'post_r', x=1.3, y=.2, b=.5, eye='O', mark='BONK'), k(.65, x=-1, y=-.2, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('walk_into', 'post'), ages=GROWN, say=["Looked up. Post did not. Post: rude.", "Roof: beautiful. Post: also there. Noted."])
    o.r('snag_a_feather_in_the_foliage', 'Backing off from the right plant and snagging a wing feather among the foliage', 18, 'none',
        [k(.15, x=-.2, y=.2), k(.35, 'foliage_r', x=-.9, y=.6, b=.4, l=1, mark='tug'), k(.55, 'foliage_r', x=-1.2, y=.7, b=.8, w=.6, eye='O', mark='RRIP'), k(.75, x=.6, y=.8, b=.5, eye='@'), k(.9, eye='-')],
        [], g='mishap', act=('hook', 'foliage'), say=["It kept the feather. Souvenir.", "Plant 1. Duck 0. Plant to be watched."])
    o.r('miss_the_jump_to_the_rail', 'Jumping for the top rail, missing by a wing, and sliding down the lattice', 18, 'none',
        [k(.15, 'lat_l', x=.3, y=.2, b=.4, l=1), k(.3, y=-1, b=-1.2, w=1, eye='O'), k(.45, 'rail_up_l', x=.6, y=-.2, b=-.5, w=1, mark='grab'), k(.62, 'lat_l', x=.4, y=.8, b=.9, w=.6, mark='sliiide'), k(.85, y=.6, b=.5, eye='@')],
        [], g='mishap', act=('climb', 'rail'), ages=GROWN, prefer=['young'], say=["Missed by one wing. It was a big wing.", "Rail: unclimbed. Lattice: slid."])
    o.r('kick_the_tub_showing_off', 'Throwing a high kick at the right tub rim to impress nobody and meeting it', 16, 'none',
        [k(.15, y=-.2, x=.2), k(.3, 'tub_r', x=.4, y=.2, b=-.6, l=1, w=.5), k(.48, 'tub_r', x=.2, y=.2, b=1, l=1, eye='O', mark='OW'), k(.68, x=-.2, y=-.4, b=-.7, l=1, w=.8, eye='@'), k(.88, eye='-')],
        [], g='mishap', act=('kick', 'tub'), say=["Tub: unharmed. Toe: negotiating.", "High kick. Low result."])
    return o


if __name__ == '__main__':
    sandbox().emit()
    dog_house().emit()
    toy_car().emit()
    gazebo().emit()
