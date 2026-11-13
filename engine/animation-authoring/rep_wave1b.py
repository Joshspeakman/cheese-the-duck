"""Wave 1b repertoires: toy_sandbox, dog_house, toy_car, gazebo. Every routine is written out by hand."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN


def sandbox():
    P = lambda c, r: (round(c / 95, 3), round(r / 41, 3))
    o = Obj('toy_sandbox', 'placed',
            fields=dict(damp=(0, 0, 1), mound=(0, 0, 1), pit=(0, 0, 1), firm=(0, 0, 1), tracks=(0, 0, 1), pail=(0, 0, 1)),
            physics=[('damp', 'rate', .0015, 'wet'), ('damp', 'rate', -.0004, 'dry&warm'), ('pail', 'rate', .002, 'wet'), ('pail', 'rate', -.0003, 'dry&warm'),
                     ('tracks', 'rate', -.0004, 'windy'), ('pit', 'rate', -.0003, 'windy'), ('mound', 'rate', -.0004, 'wet'), ('firm', 'rate', -.0003, 'wet')],
            effects=dict(
                sweep=[('obj.dirt', 'add', -.25)], wipe=[('obj.dirt', 'add', -.15)], level=[('mound', 'set', 0)], refill=[('pit', 'mul', .3), ('tracks', 'add', .1)],
                rake=[('tracks', 'set', 0), ('firm', 'add', -.1)], stand=[('obj.condition', 'add', .05)], crack=[('firm', 'mul', .3), ('obj.dirt', 'add', .1)],
                dig=[('pit', 'add', .3), ('mound', 'add', .1)], heap=[('mound', 'add', .3), ('pit', 'add', -.1)], pack=[('firm', 'add', .3), ('mound', 'add', .2)],
                tamp=[('firm', 'add', .3), ('tracks', 'add', .1)], trench=[('pit', 'add', .2), ('tracks', 'add', .2)], angel=[('tracks', 'add', .3), ('firm', 'add', -.2)],
                fling=[('obj.dirt', 'add', .15), ('pit', 'add', .1)], fun=[('need.fun', 'add', 2)], stomp=[('mound', 'mul', .2), ('need.fun', 'add', 1)],
                trace=[('tracks', 'add', .25), ('pit', 'add', .05)], squeeze=[('firm', 'add', .2), ('damp', 'add', -.1)], bail=[('pail', 'set', 0), ('damp', 'add', .25)],
                ring=[('obj.dirt', 'add', -.05), ('pail', 'add', -.05)], twirl=[('tracks', 'add', .15), ('firm', 'add', -.05)], doze=[('need.energy', 'add', 2)], bake=[('damp', 'mul', .5), ('need.energy', 'add', 1)], squash=[('damp', 'add', -.2), ('firm', 'add', .2)],
                dustbath=[('need.cleanliness', 'add', 2), ('obj.dirt', 'add', .1)], prop=[('mound', 'add', .15)], press=[('tracks', 'add', .3), ('firm', 'add', .2)],
                crown=[('mound', 'add', -.1), ('need.fun', 'add', 1)], scatter=[('obj.dirt', 'add', .2)], whack=[('obj.condition', 'add', -.05)],
                slump=[('pit', 'mul', .6), ('tracks', 'add', .15)], cave=[('mound', 'mul', .1), ('pit', 'add', .2), ('obj.dirt', 'add', .1)], dent=[('obj.condition', 'add', -.03)]),
            anchors=dict(sand_front=P(48, 33), sand_left=P(22, 32), sand_right=P(72, 32), sand_mid=P(44, 31), board_edge=P(30, 34),
                         stud_a=P(19, 35), stud_c=P(37, 35), stud_e=P(55, 35), stud_h=P(82, 35),
                         bucket_rim=P(17, 27), bucket_side=P(13, 29), bucket_in=P(17, 29), bucket_base=P(16, 30),
                         moat_left=P(31, 26), moat_right=P(65, 26), moat_top=P(48, 24), moat_bottom=P(48, 30),
                         shovel_grip=P(79, 25), shovel_shaft=P(79, 27), shovel_blade=P(79, 28),
                         wall_left_low=P(8, 31), wall_right_low=P(87, 31)))
    # ---------------- care
    o.r('sweep_board', 'Sweeping stray sand off the base board with a wing', 16, 'wing',
        [k(.15, 'board_edge', reach=.6, x=.3, y=.5), k(.35, 'board_edge', reach=1, x=.5, y=.6, l=1), k(.55, 'stud_c', reach=1, x=.6, y=.6, r=1), k(.75, 'stud_e', reach=1, x=.5, y=.5, l=1), k(.9, eye='^')],
        [(.55, 'sweep')], g='care', prefer=['grown'])
    o.r('level_heap', 'Ploughing the heap flat with his chest', 18, 'none',
        [k(.15, x=.4, y=.6, eye='>'), k(.35, 'sand_mid', x=.9, y=1, b=.8, mark='hrr'), k(.55, 'sand_left', x=1, y=1.1, b=.9), k(.75, x=.3, y=.4, b=.3, w=.5, eye='^')],
        [(.55, 'level')], g='care', when=['mound>.3'], prefer=['grumpy'], obj=[(.35, dict(shake=.3)), (.6, dict(shake=.5))])
    o.r('refill_pit', 'Kicking the sand back into the pit until it is level', 18, 'none',
        [k(.15, x=.3, y=.4), k(.3, 'sand_front', y=.8, b=.6, l=1, mark='fff'), k(.5, 'sand_front', y=.8, b=.6, r=1), k(.7, 'sand_front', y=.8, b=.6, l=1), k(.88, y=.2, w=.4, eye='-')],
        [(.5, 'refill')], g='care', when=['pit>.3'], prefer=['young'])
    o.r('rake_prints', 'Raking his own footprints out of the sand with the bill', 16, 'none',
        [k(.15, y=.7, x=.5), k(.35, 'sand_right', x=1.2, y=1.3, b=.3, mark='skrr'), k(.55, 'sand_mid', x=1.2, y=1.3, b=.3), k(.75, y=.5, x=.3, eye='-'), k(.9, eye='^')],
        [(.55, 'rake')], g='care', when=['tracks>.3'], prefer=['curious'])
    o.r('stand_shovel', 'Hauling the leaning shovel upright and jamming its blade in', 20, 'wing',
        [k(.15, 'shovel_shaft', reach=.7, x=.4, y=-.2, w=.4), k(.35, 'shovel_shaft', reach=1, x=.2, y=-.4, b=.5, w=1, mark='hnh'), k(.55, 'shovel_blade', reach=1, x=.3, b=.9, w=.6), k(.75, 'shovel_blade', x=.4, b=.4, l=1, w=.3, mark='thk'), k(.9, eye='^')],
        [(.55, 'stand')], g='care', ages=GROWN, obj=[(.35, dict(sway=.5)), (.55, dict(shake=.6)), (.75, dict(sway=0))])
    o.r('wipe_bucket', 'Wiping caked sand off the bucket with the underside of a wing', 16, 'wing',
        [k(.15, 'bucket_side', reach=.7, x=.2, y=-.3, w=.4), k(.35, 'bucket_side', reach=1, x=.2, y=-.3, w=.8, b=.2), k(.55, 'bucket_rim', reach=1, x=-.2, y=-.5, w=1), k(.75, y=-.1, eye='-'), k(.9, eye='^')],
        [(.55, 'wipe')], g='care', ages=GROWN)
    # ---------------- use
    o.r('dig_pit', 'Digging a pit with both feet flying backwards', 20, 'none',
        [k(.15, x=.3, y=.6), k(.3, 'sand_front', y=1.2, b=1, l=1, mark='dig'), k(.5, 'sand_front', y=1.4, b=1.1, r=1), k(.7, 'sand_front', y=1.4, b=1.2, l=1), k(.88, x=.2, y=.2, w=.4, eye='^')],
        [(.5, 'dig')], g='use', prefer=['happy', 'young'], obj=[(.3, dict(shake=.3)), (.6, dict(shake=.5))], say=["Down we go. Still no treasure. Typical.", "Hole. Mine. Keep your feet out of it."])
    o.r('heap_mound', 'Shoving the sand into a mound against the left side with his breast', 20, 'none',
        [k(.15, x=.5, y=.5, eye='>'), k(.35, 'sand_left', x=1, y=.9, b=.6, mark='hup'), k(.55, 'sand_mid', x=1.1, y=.9, b=.6), k(.75, 'sand_left', x=1.1, y=.9, b=.7), k(.9, eye='^')],
        [(.55, 'heap')], g='use', when=['pit<=.7'], prefer=['grown'])
    o.r('pack_cake', 'Packing damp sand into the bucket and rapping the bottom flat', 22, 'wing',
        [k(.15, 'bucket_in', reach=.6, x=.4, y=.5, w=.5), k(.35, 'bucket_in', reach=1, x=.4, y=.7, w=.8, b=.3), k(.55, 'bucket_in', reach=1, x=.5, y=.7, w=.2, b=.5, mark='pat pat'), k(.75, 'bucket_base', reach=1, x=.3, y=.4, w=.9, mark='tok'), k(.9, eye='^')],
        [(.55, 'pack')], g='use', when=['damp>.3'], prefer=['curious'])
    o.r('pat_down', 'Patting the heap down firm with the flat of a wing', 16, 'wing',
        [k(.15, 'sand_mid', reach=.6, x=.3, y=.5, w=.3), k(.3, 'sand_mid', reach=1, x=.3, y=.6, w=1), k(.45, 'sand_mid', reach=.6, x=.3, y=.5, w=.3), k(.6, 'sand_mid', reach=1, x=.3, y=.6, w=1), k(.8, x=.1, w=.4, eye='-'), k(.9, eye='^')],
        [(.6, 'tamp')], g='use', when=['mound>.3'])
    o.r('shovel_trench', 'Hauling the shovel by its grip to scrape a trench through the sand', 22, 'none',
        [k(.12, 'shovel_grip', x=.4, y=-.3, b=.3), k(.3, 'shovel_grip', x=.6, y=-.2, b=.6, w=.5, mark='hhh'), k(.5, 'sand_front', x=.9, y=.7, b=.8, w=.5), k(.7, 'sand_front', x=1, y=.8, b=.9, w=.7), k(.88, y=-.1, eye='^')],
        [(.5, 'trench')], g='use', ages=GROWN, obj=[(.3, dict(sway=.6)), (.5, dict(shake=.5)), (.7, dict(sway=-.4))])
    o.r('trace_moat', 'Tracing the moat ring around the middle with his bill', 22, 'none',
        [k(.12, 'moat_bottom', x=1, y=1.4, b=.4), k(.3, 'moat_left', x=1.1, y=.5, b=.2), k(.5, 'moat_top', x=1.1, y=.2), k(.7, 'moat_right', x=1.1, y=.5, b=.2), k(.88, y=.2, eye='-')],
        [(.5, 'trace')], g='use', ages=GROWN, prefer=['curious'])
    # ---------------- play
    o.r('sand_angel', 'Flopping flat on his back and flapping a sand angel', 18, 'none',
        [k(.15, y=-.4, b=-.5, w=.6, eye='>'), k(.3, 'sand_mid', y=1.5, b=1.4, w=1, mark='floomp'), k(.5, 'sand_mid', y=1.5, b=1.4, w=0), k(.7, 'sand_mid', y=1.5, b=1.4, w=1), k(.9, y=.3, b=.2, eye='^')],
        [(.5, 'angel')], g='play', prefer=['happy', 'young'], obj=[(.3, dict(shake=.4)), (.6, dict(shake=.4))], say=["Angel. Obviously. Look at the span.", "Lie in it, get up, regret nothing."])
    o.r('stud_sprint', 'Sprinting the length of the base board and clicking each stud with a foot', 18, 'none',
        [k(.12, 'stud_a', x=.5, y=.7, l=1, mark='tk'), k(.3, 'stud_c', x=.7, y=.5, r=1, mark='tk'), k(.5, 'stud_e', x=.8, y=.5, l=1, mark='tk'), k(.7, 'stud_h', x=.9, y=.4, r=1, mark='tk'), k(.9, x=.2, w=.7, eye='^')],
        [(.5, 'fun')], g='play', prefer=['happy', 'young'])
    o.r('mound_stomp', 'Jumping up and down on the mound until it is a pancake', 18, 'none',
        [k(.15, y=-.3, b=-.6, w=.5), k(.3, 'sand_right', y=.4, b=1.1, l=1, mark='thud'), k(.45, y=-.4, b=-.9, w=1), k(.6, 'sand_right', y=.4, b=1.3, r=1, mark='THUD'), k(.8, y=.2, b=.3, eye='^')],
        [(.6, 'stomp')], g='play', when=['mound>.3'], prefer=['grumpy'], obj=[(.3, dict(shake=.5)), (.6, dict(shake=.8))], say=["Flattened. It had it coming.", "Heap: gone. Me: taller."])
    o.r('hopscotch_trail', 'Hopping across the sand in three jumps to lay a trail of prints', 20, 'none',
        [k(.12, 'sand_left', x=.4, y=.5, b=.5, l=1), k(.3, y=-.4, b=-.7, w=.5), k(.45, 'sand_mid', x=.5, y=.5, b=.6, r=1), k(.62, y=-.4, b=-.7, w=.5), k(.78, 'sand_right', x=.5, y=.5, b=.6, l=1), k(.9, eye='^')],
        [(.45, 'press')], g='play', when=['damp>.3'], prefer=['happy'])
    o.r('sand_fling', 'Flinging bills of sand over his shoulder at the wall', 18, 'none',
        [k(.15, x=.3, y=.4), k(.3, 'sand_front', x=1.1, y=1.4, b=.5, mark='hup'), k(.45, y=-.5, x=-.6, w=.5, eye='>'), k(.6, 'sand_front', x=1.1, y=1.4, b=.5, mark='hup'), k(.75, y=-.5, x=-.7, w=.8, eye='>'), k(.9, eye='-')],
        [(.3, 'fling')], g='play', prefer=['grumpy'], say=["Take that, wall. And that.", "Sand: airborne. Wall: unmoved. Draw."])
    o.r('bucket_megaphone', 'Honking into the bucket like a megaphone', 14, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.4, y=-.2, w=.2), k(.35, 'bucket_in', x=1.2, y=.5, w=.3, mark='HONK'), k(.55, 'bucket_in', x=1.2, y=.5, w=.5, mark='HONK', eye='O'), k(.75, x=-.4, y=-.5, eye='^')],
        [(.35, 'fun')], g='play', say=["Sounds like a bigger me.", "HONK. It's got a better echo than the barn."])
    # ---------------- test
    o.r('taste_sand', 'Tasting a billful of sand and deciding against it', 14, 'none',
        [k(.15, 'sand_front', x=.9, y=1.2, b=.4), k(.35, x=.2, y=.3, eye='-', mark='...'), k(.55, x=-.3, y=-.2, eye='>', mark='ptui'), k(.75, y=.4, eye='-')],
        [], g='test', prefer=['curious', 'young'], say=["Tastes like the floor. Because it is the floor.", "Sand. Still sand. Zero stars."])
    o.r('squeeze_damp', 'Squeezing damp sand under a foot to see if it holds its shape', 16, 'none',
        [k(.15, y=.4, x=.3), k(.3, 'sand_left', y=.8, b=.4, l=1), k(.5, 'sand_left', y=.9, b=.5, l=1, eye='O'), k(.7, x=-.2, y=.7, eye='-', mark='hm'), k(.9, eye='^')],
        [(.5, 'squeeze')], g='test', when=['damp>.3'], prefer=['curious'])
    o.r('probe_depth', 'Sinking his bill down the pit to find where the bottom is', 18, 'none',
        [k(.15, x=.5, y=.5), k(.35, 'sand_mid', x=1, y=1.6, b=.4, eye='O'), k(.55, 'sand_mid', x=1.3, y=1.9, b=.6, mark='hmm'), k(.75, x=.3, y=.4, eye='-'), k(.9, eye='^')],
        [], g='test', when=['pit>.3'], prefer=['curious'])
    o.r('knock_walls', 'Knocking on the side walls with his bill and listening for hollow', 16, 'none',
        [k(.12, 'wall_left_low', x=.8, y=.3, mark='tok'), k(.3, 'wall_left_low', x=.5, y=.3, mark='tok'), k(.55, x=.2, y=.2, eye='-'), k(.75, 'wall_right_low', x=.8, y=.3, mark='tok'), k(.9, eye='^')],
        [], g='test', say=["Hollow on one side. Suspicious.", "It's just wood. Disappointing wood."])
    o.r('lean_on_shovel', 'Putting his full weight on the shovel to see if it holds a duck', 16, 'none',
        [k(.15, 'shovel_shaft', x=.6, y=.2, b=.2), k(.35, 'shovel_shaft', x=.9, y=.6, b=.7, w=.3, mark='crk'), k(.55, 'shovel_shaft', x=1, y=.7, b=.9, w=.5, eye='O'), k(.8, x=.1, y=.1, eye='-')],
        [(.55, 'dent')], g='test', ages=GROWN, obj=[(.35, dict(sway=.4)), (.55, dict(sway=.8, shake=.4))])
    o.r('ring_bucket', 'Banging the bucket with his bill and rating the note', 16, 'wing',
        [k(.15, 'bucket_side', reach=.6, x=.5, y=-.1), k(.3, 'bucket_rim', x=.5, y=.1, mark='ting'), k(.5, 'bucket_base', x=.4, y=.5, mark='dunk'), k(.7, y=.2, eye='-', mark='B flat'), k(.9, eye='^')],
        [], g='test')
    # ---------------- rest
    o.r('nap_in_hollow', 'Wriggling into the pit and dozing off', 28, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_mid', y=1.4, b=1.2, w=.3), k(.5, 'sand_mid', y=1.6, b=1.5, eye='-', mark='z'), k(.75, 'sand_mid', y=1.6, b=1.5, eye='-', mark='zZ'), k(.9, y=.8, b=.6, eye='o')],
        [(.5, 'doze')], g='rest', when=['pit>.3', 'tired'], say=["Perfect fit. Of course it is. I dug it.", "Do not tell the shovel I slept in its hole."])
    o.r('bake_belly', 'Spreading flat on the warm sand to bake his belly', 30, 'none',
        [k(.15, y=.3, x=.3), k(.3, 'sand_front', y=1.6, b=1.5, w=.6), k(.55, 'sand_front', y=1.6, b=1.5, w=.2, eye='-', mark='ahh'), k(.8, 'sand_front', y=1.5, b=1.4, w=.2, eye='-'), k(.92, y=.5, b=.4, eye='^')],
        [(.55, 'bake')], g='rest', when=['sun', 'damp>.2'], prefer=['happy'])
    o.r('lean_on_wall', 'Leaning on the left wall with his eyes shut', 22, 'none',
        [k(.15, x=.2, y=.2), k(.35, 'wall_left_low', x=.7, y=.3, b=.2, eye='-'), k(.6, 'wall_left_low', x=.8, y=.4, b=.3, eye='-', mark='z'), k(.85, 'wall_left_low', x=.8, y=.4, b=.3, eye='-')],
        [], g='rest', when=['tired'], prefer=['elder'])
    o.r('shelter_behind_bucket', 'Wedging in behind the bucket out of the wind', 26, 'none',
        [k(.15, y=.3, x=.3), k(.35, 'bucket_side', x=-.2, y=.8, b=.8, w=.6), k(.6, 'bucket_side', x=-.2, y=1, b=1, w=.8, eye='-', mark='brr'), k(.85, 'bucket_side', y=.9, b=.9, eye='-')],
        [], g='rest', when=['windy'])
    o.r('sulk_in_corner', 'Sulking in the corner with his back to the sandbox', 24, 'none',
        [k(.15, x=-.3, y=.3), k(.35, 'wall_right_low', x=-.4, y=.9, b=.5, eye='>'), k(.6, 'wall_right_low', x=-.5, y=1, b=.6, eye='-', mark='hmph'), k(.85, 'wall_right_low', x=-.5, y=1, b=.6, eye='-')],
        [], g='rest', when=['sad'], prefer=['grumpy'], say=["I'm not sulking. I'm facing the wall. Different.", "Leave me. I'm busy being betrayed by sand."])
    o.r('perch_shovel_grip', 'Balancing on the shovel grip and keeping watch with one eye shut', 26, 'none',
        [k(.15, y=-.3, b=-.5, w=.7), k(.35, 'shovel_grip', y=-.6, b=-.3, w=.8, l=1), k(.6, 'shovel_grip', y=-.5, b=0, w=.4, eye='-'), k(.85, 'shovel_grip', y=-.5, b=0, w=.4, eye='-', mark='z')],
        [], g='rest', ages=GROWN, obj=[(.35, dict(sway=.4)), (.6, dict(sway=.1))], say=["Lookout. Nothing has happened. Perfect shift.", "Eyes shut, ears open. Mostly shut."])
    # ---------------- weather
    o.r('tip_out_rain', 'Tipping the bucket over to empty out the rainwater', 20, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.3, y=-.2, w=.5), k(.35, 'bucket_rim', reach=1, x=.2, y=-.4, b=.4, w=1, mark='hng'), k(.55, 'bucket_in', reach=1, x=.5, y=.3, b=.7, w=.9, mark='glug'), k(.75, x=-.4, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
        [(.55, 'bail')], g='weather', when=['pail>.3'], ages=GROWN, obj=[(.35, dict(sway=.3)), (.55, dict(shake=.5))])
    o.r('squelch_stomp', 'Stomping in the soaked sand and watching it squelch up between his toes', 18, 'none',
        [k(.15, y=.3, x=.3), k(.3, 'sand_front', y=.6, b=.6, l=1, mark='squelch'), k(.5, 'sand_front', y=.6, b=.7, r=1, mark='squelch'), k(.7, 'sand_front', y=.6, b=.7, l=1, eye='O', mark='squelch'), k(.9, eye='^')],
        [(.5, 'squash')], g='weather', when=['damp>.5'], prefer=['happy'])
    o.r('redraw_blown_tracks', 'Hurrying to redraw his scoured tracks with the bill before the wind takes them', 20, 'none',
        [k(.12, 'sand_front', x=1, y=1.5, b=.4), k(.3, 'sand_right', x=1.1, y=1.5, b=.3, eye='>', mark='oi'), k(.5, 'sand_right', x=1.4, y=1.7, b=.4), k(.7, x=-.5, y=-.2, w=.6, eye='>'), k(.9, eye='-')],
        [(.3, 'trace')], g='weather', when=['windy', 'tracks>.2'], prefer=['grumpy'])
    o.r('hold_pit_edge', 'Pressing his chest to the lip of the pit as the wind blows it full', 20, 'none',
        [k(.15, x=.4, y=.6), k(.35, 'sand_front', x=.8, y=1.2, b=.8, w=.3), k(.55, 'sand_front', x=.8, y=1.3, b=1, w=.6, eye='>', mark='nnh'), k(.8, x=.2, y=.4, eye='-')],
        [(.55, 'prop')], g='weather', when=['windy', 'pit>.3'])
    o.r('dust_bath', 'Rolling in the bone-dry sand and flapping dust all over himself', 24, 'none',
        [k(.15, y=.6, b=.3), k(.3, 'sand_mid', y=1.4, b=1.2, w=1, mark='fff'), k(.5, 'sand_mid', y=1.4, b=1.2, w=0, l=1), k(.7, 'sand_mid', y=1.4, b=1.2, w=1, r=1), k(.9, y=.2, w=.4, eye='^')],
        [(.5, 'dustbath')], g='weather', when=['dry', 'warm', 'damp<.3'], prefer=['happy'], say=["Clean now. Dirtier. Same thing.", "Dust bath. Filthy, correct, dignified."])
    o.r('prop_slumping_heap', 'Propping the sagging heap up with his wing against the rain', 22, 'wing',
        [k(.15, 'sand_left', reach=.6, x=.3, y=.7), k(.35, 'sand_left', reach=1, x=.6, y=.8, b=.4, w=1), k(.55, 'sand_mid', reach=1, x=.7, y=.9, b=.5, w=1, eye='>'), k(.8, x=.1, eye='-', mark='ugh')],
        [(.55, 'prop')], g='weather', when=['wet', 'mound>.3'])
    o.r('hammer_crust', 'Hammering the sun-baked crust with his bill until it cracks', 20, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_right', x=1, y=1.4, b=.4, mark='tak'), k(.45, 'sand_right', x=.6, y=.5, w=.5), k(.6, 'sand_right', x=1, y=1.5, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
        [(.6, 'crack')], g='weather', when=['sun', 'firm>.6'], prefer=['grumpy'])
    # ---------------- show
    o.r('king_of_the_heap', 'Standing on the heap with his wings spread and announcing himself king of it', 22, 'none',
        [k(.15, y=.3, b=.5), k(.3, 'sand_mid', y=-.5, b=-.4, w=.6), k(.5, 'sand_mid', y=-.9, b=-.2, w=1, eye='^', mark='BOW'), k(.75, 'sand_mid', y=-.9, b=-.2, w=1), k(.9, y=0, eye='o')],
        [(.5, 'crown')], g='show', when=['mound>.3'], prefer=['happy'], say=["King of this exact pile. Bow or leave.", "Long live me. Short pile."])
    o.r('sign_the_sand', 'Writing CHEESE in the sand with the tip of his bill', 22, 'none',
        [k(.12, 'sand_left', x=1, y=1.3, b=.3), k(.3, 'sand_mid', x=1, y=1.3, b=.3), k(.5, 'sand_right', x=1, y=1.3, b=.3), k(.7, x=.3, y=.2, eye='^'), k(.88, x=.1, eye='o')],
        [(.5, 'trace')], g='show', when=['damp>.2'], prefer=['curious'], say=["Cheese was here. Cheese is always here.", "Signed it. Let the wind try to forge it."])
    o.r('drumroll_bucket', 'Drumming a roll on the bucket and taking a bow', 18, 'wing',
        [k(.15, 'bucket_rim', reach=.6, x=.3), k(.3, 'bucket_rim', reach=1, w=.8, mark='rrrr'), k(.45, 'bucket_side', reach=.4, w=.2, mark='rrrr'), k(.6, 'bucket_rim', reach=1, w=.9, mark='TSH'), k(.8, y=1, b=.5, w=1, eye='^')],
        [(.6, 'ring')], g='show', say=["Thank you. Tip the bucket.", "Encore? No. I have standards."])
    o.r('tightrope_board', 'Walking the base board like a tightrope with his wings out', 20, 'none',
        [k(.15, 'board_edge', y=.2, b=.3, w=.8, l=1), k(.35, 'stud_c', y=.2, b=.3, w=1, r=1), k(.55, 'stud_e', y=.2, b=.4, w=1, l=1, eye='O'), k(.75, 'stud_h', y=.2, b=.2, w=.8, r=1), k(.9, y=0, w=.6, eye='^')],
        [(.55, 'fun')], g='show', prefer=['young', 'happy'])
    o.r('moat_ballet', 'Tiptoeing round the moat ring with his bill in the air', 24, 'none',
        [k(.12, 'moat_bottom', y=-.6, b=-.3, w=.7, l=1), k(.3, 'moat_left', y=-.8, b=-.3, w=.9, r=1), k(.5, 'moat_top', y=-.8, b=-.4, w=1, l=1), k(.7, 'moat_right', y=-.8, b=-.3, w=.9, r=1), k(.9, y=.5, b=.6, w=0, eye='^')],
        [(.5, 'twirl')], g='show', ages=GROWN)
    o.r('shovel_salute', 'Presenting the shovel upright like a sword and saluting it', 18, 'wing',
        [k(.15, 'shovel_grip', reach=.7, x=.2, y=-.3, w=.5), k(.35, 'shovel_grip', reach=1, x=.1, y=-.7, w=1, mark='huh'), k(.6, 'shovel_shaft', reach=1, x=.1, y=-.7, w=1, eye='O'), k(.8, y=-.2, w=0, eye='^')],
        [], g='show', ages=GROWN)
    # ---------------- mishap
    o.r('wedged_in_bucket', 'Diving head first into the bucket, sticking at the shoulders and kicking out', 22, 'none',
        [k(.15, x=.5, eye='>'), k(.3, 'bucket_in', x=1.2, y=.6, b=.8, mark='oof'), k(.5, 'bucket_in', x=1.3, y=.6, b=1, l=1, eye='O', mark='mmf'), k(.7, 'bucket_in', x=1.3, y=.6, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
        [(.7, 'dent')], g='mishap', prefer=['young', 'grumpy'], ages=GROWN, obj=[(.5, dict(shake=.6)), (.7, dict(shake=1))], say=["Wedged by the shoulders. Bucket: won.", "I meant to do that. All of it."])
    o.r('trip_on_board', 'Tripping over the base board and landing bill first in the sand', 16, 'none',
        [k(.15, 'board_edge', x=.5, y=.3, l=1), k(.3, x=1.1, y=.8, b=-.4, w=.8, eye='O'), k(.5, 'sand_front', x=1.6, y=1.8, b=1, w=1, mark='FFF'), k(.75, y=.6, b=.4, eye='@'), k(.9, eye='-')],
        [(.5, 'scatter')], g='mishap', say=["Face. Sand. Dignity: buried.", "The board moved. It's always the board."])
    o.r('shovel_whack', 'Stepping on the shovel blade and getting the handle in the face', 16, 'none',
        [k(.15, x=.4, y=.4, l=1), k(.3, 'shovel_blade', x=.4, y=.5, b=.3, l=1, mark='step'), k(.45, 'shovel_grip', x=-.8, y=-.8, b=-.4, w=1, eye='O', mark='BONK'), k(.7, x=-.2, y=.5, eye='@'), k(.9, eye='-')],
        [(.45, 'whack')], g='mishap', ages=GROWN, obj=[(.3, dict(sway=.5)), (.45, dict(shake=1)), (.65, dict(sway=-.3))], say=["OW. Shit. Okay. Zero stars, would touch again.", "Handle to the face. Fair. I started it."])
    o.r('knee_deep_in_pit', 'Sinking to the knee in the pit and heaving himself out', 20, 'none',
        [k(.15, x=.4, y=.4), k(.3, 'sand_mid', x=.2, y=.2, b=1.1, l=1, eye='O'), k(.5, 'sand_mid', x=.2, y=.3, b=1.4, r=1, w=.6, mark='hnnng'), k(.7, 'sand_mid', x=.3, y=-.3, b=-.5, w=1, mark='POP'), k(.88, y=.8, eye='-')],
        [(.5, 'slump')], g='mishap', when=['pit>.3'], prefer=['young'])
    o.r('cave_in', 'Digging under the heap until it collapses on his head', 20, 'none',
        [k(.15, x=.4, y=.5), k(.3, 'sand_left', x=1, y=1.2, b=.7, l=1, mark='dig'), k(.5, 'sand_left', x=1.2, y=1.5, b=.9, r=1, eye='O'), k(.65, 'sand_left', y=2, b=1.4, w=1, mark='FWUMP', eye='@'), k(.88, y=1.2, b=1, eye='-', mark='...')],
        [(.65, 'cave')], g='mishap', when=['mound>.3'], prefer=['curious'], obj=[(.5, dict(shake=.3)), (.65, dict(shake=1))], say=["I dug. It fell. Physics is a snitch.", "Buried by my own heap. Good work, me."])
    return o


def dog_house():
    P = lambda c, r: (round(c / 69, 3), round(r / 42, 3))
    o = Obj('dog_house', 'placed',
            fields=dict(warmth=(0, 0, 1), damp=(0, 0, 1), bowl=(0, 0, 1), frost=(0, 0, 1), scent=(0, 0, 1)),
            physics=[('warmth', 'rate', .0004, 'sun'), ('warmth', 'rate', -.0006, 'cold'), ('warmth', 'rate', -.0002, 'night'), ('damp', 'rate', .0015, 'wet'),
                     ('damp', 'rate', -.0005, 'dry&warm'), ('bowl', 'rate', .003, 'wet'), ('bowl', 'rate', -.0004, 'dry&warm'), ('frost', 'rate', .0015, 'cold'),
                     ('frost', 'rate', -.002, 'warm'), ('scent', 'rate', -.0002, 'always')],
            effects=dict(
                scrub=[('obj.dirt', 'add', -.25), ('obj.wetness', 'add', .1)], sweep=[('obj.dirt', 'add', -.15)], wipe=[('damp', 'mul', .5), ('obj.wetness', 'add', -.3)],
                bolt=[('obj.condition', 'add', .05)], scour=[('obj.dirt', 'add', -.2)], tip=[('bowl', 'set', 0), ('damp', 'add', .05)],
                huddle=[('warmth', 'add', .15), ('need.energy', 'add', 2)], watch=[('need.fun', 'add', 2)], mark=[('scent', 'set', 1)],
                hop=[('need.fun', 'add', 2), ('obj.dirt', 'add', .05)], shove=[('bowl', 'mul', .5), ('obj.dirt', 'add', .1)], doze=[('need.energy', 'add', 3), ('damp', 'add', -.05)],
                dry=[('damp', 'mul', .4)], scrape=[('frost', 'mul', .2)], crack=[('bowl', 'mul', .5), ('frost', 'add', -.2)], slosh=[('bowl', 'mul', .4), ('damp', 'add', .1)],
                leap=[('obj.dirt', 'add', .03), ('scent', 'add', .1)], snag=[('obj.condition', 'add', -.03)], tour=[('scent', 'add', .2)], warm=[('warmth', 'add', .1)], rub=[('scent', 'add', .3), ('obj.dirt', 'add', .05)]),
            anchors=dict(plank_left=P(16, 34), plank_right=P(55, 34), knot_left=P(16, 33), knot_right=P(55, 33), bolt_a=P(11, 38), bolt_b=P(16, 38), bolt_c=P(21, 38), bolt_d=P(51, 38),
                         frame_left=P(23, 34), frame_right=P(48, 34), threshold=P(35, 38), doorsill=P(35, 40), doorway_dark=P(35, 35), inner_dish=P(38, 37),
                         bowl_rim=P(59, 40), bowl_edge=P(57, 40), eave_left=P(20, 22)))
    # ---------------- care
    o.r('scrub_planks', 'Scrubbing the left planks with a wing dipped in the bowl', 18, 'wing',
        [k(.15, 'bowl_rim', reach=.6, x=.4, y=.7), k(.3, 'plank_left', reach=1, x=.5, y=.3, w=.8, l=1), k(.5, 'knot_left', reach=1, x=.5, y=.2, w=1, r=1), k(.7, 'plank_left', reach=1, x=.5, y=.3, w=.8, l=1), k(.88, y=.1, eye='^')],
        [(.5, 'scrub')], g='care')
    o.r('sweep_sill', 'Sweeping the doorsill clean with the flat of a wing', 14, 'wing',
        [k(.15, 'doorsill', reach=.6, x=.3, y=.8), k(.35, 'doorsill', reach=1, x=.4, y=.8, w=.8, l=1), k(.55, 'threshold', reach=1, x=.4, y=.8, w=.8, r=1), k(.8, x=.1, y=.3, eye='-')],
        [(.55, 'sweep')], g='care', prefer=['grown'])
    o.r('wipe_planks_dry', 'Mopping the damp off the front planks with his breast', 18, 'none',
        [k(.15, x=.3, y=.3), k(.3, 'plank_right', x=.6, y=.5, b=.4, w=.2), k(.5, 'frame_right', x=.7, y=.6, b=.5, w=.2), k(.7, 'plank_right', x=.6, y=.5, b=.4), k(.9, eye='^')],
        [(.5, 'wipe')], g='care', when=['damp>.3'], prefer=['curious'])
    o.r('hammer_bolt', 'Hammering a loose bolt back in with his bill', 16, 'none',
        [k(.15, y=.6, x=.4), k(.3, 'bolt_a', x=1, y=1.2, b=.4, mark='tk'), k(.45, y=-.3, x=.3), k(.6, 'bolt_b', x=1, y=1.2, b=.4, mark='TK'), k(.8, y=.1, eye='^')],
        [(.6, 'bolt')], g='care', ages=YOUNG + ['juvenile'], say=["Bolt's back. House holds. I am structural.", "Hit it with my face. Efficient."])
    o.r('scour_bowl', 'Scouring the outside bowl out with his bill', 16, 'none',
        [k(.15, y=.6, x=.4), k(.3, 'bowl_rim', x=1.1, y=1.4, b=.4), k(.5, 'bowl_edge', x=1.2, y=1.5, b=.5, mark='scrk'), k(.7, 'bowl_rim', x=1.1, y=1.4, b=.4), k(.88, eye='^')],
        [(.5, 'scour')], g='care', prefer=['grumpy'])
    o.r('scrub_doorframe', 'Rubbing a muddy doorframe clean with his own belly feathers', 18, 'none',
        [k(.15, x=.2), k(.35, 'frame_left', x=.4, y=.3, b=.5, w=.3), k(.55, 'threshold', x=.4, y=.5, b=.8, w=.3), k(.75, 'frame_left', x=.4, y=.3, b=.5, w=.3), k(.9, eye='-')],
        [(.55, 'scrub')], g='care', prefer=['happy'])
    # ---------------- use
    o.r('enter_turn_sit', 'Stepping into the doorway, turning round three times and sitting', 22, 'none',
        [k(.12, 'threshold', x=.4, y=.2), k(.3, 'doorway_dark', x=.6, y=.2, l=1), k(.5, 'doorway_dark', x=.2, y=.3, b=.3, r=1, w=.3), k(.7, 'doorway_dark', x=0, y=.5, b=1, w=.4), k(.88, 'doorway_dark', y=.6, b=1, eye='-')],
        [(.7, 'huddle')], g='use', when=['warmth<.6'], prefer=['tired', 'elder'], say=["Turned three times. Nothing came of it. Still correct.", "Circled thrice. Dog logic, applied to a goose."])
    o.r('guard_the_door', 'Planting himself on the doorsill to glare at the garden', 24, 'none',
        [k(.15, 'doorsill', x=.4, y=-.2, b=.2), k(.35, 'doorsill', x=.6, y=-.6, b=.4, w=.5, eye='>'), k(.6, 'doorsill', x=.6, y=-.6, b=.4, w=.3, eye='>', mark='grr'), k(.85, 'doorsill', x=.6, y=-.4, b=.4, eye='-')],
        [(.35, 'watch')], g='use', prefer=['grumpy'], say=["Nobody enters. Nobody asked to. Doing great.", "On guard. Mostly against boredom."])
    o.r('scent_mark_frame', 'Rubbing his cheek up the frame to mark the whole house as his', 18, 'none',
        [k(.15, x=.2), k(.3, 'frame_left', x=.8, y=.2, b=.3), k(.5, 'frame_left', x=.8, y=-.3, b=.1, w=.3), k(.7, 'frame_right', x=.8, y=.2, b=.3, w=.3, eye='^'), k(.9, eye='^')],
        [(.5, 'mark')], g='use', when=['scent<.5'], prefer=['happy'], say=["Mine. Smells like me. Smells like bread, apparently.", "Marked. Legally binding in several ponds."])
    o.r('peek_out_dark', 'Poking just his head out of the dark doorway and checking both ways', 18, 'none',
        [k(.12, 'doorway_dark', x=.2, y=.3, b=.4), k(.3, 'frame_left', x=1, y=.3, b=.4, eye='o'), k(.5, 'frame_right', x=1, y=.3, b=.4, eye='O'), k(.7, 'doorway_dark', x=.2, y=.3, b=.4, eye='-'), k(.88, eye='-')],
        [], g='use', prefer=['curious', 'young'])
    o.r('drag_bowl_nearer', 'Dragging the water bowl by its rim up against the doorstep', 20, 'none',
        [k(.12, 'bowl_rim', x=.6, y=.5, b=.3), k(.3, 'bowl_rim', x=-.5, y=.4, b=.7, w=.4, mark='hnng'), k(.5, 'bowl_edge', x=-.6, y=.4, b=.8, w=.5, mark='hnng'), k(.7, 'doorsill', x=-.2, y=.3, b=.3), k(.88, eye='^')],
        [(.5, 'shove')], g='use', ages=GROWN, when=['bowl<=.7'])
    o.r('rummage_back_corner', 'Rummaging through the back of the kennel for the best sitting spot', 22, 'none',
        [k(.12, 'threshold', x=.5, y=.5), k(.3, 'doorway_dark', x=.8, y=.9, b=.5), k(.5, 'inner_dish', x=1, y=1, b=.7, mark='rrt'), k(.7, 'inner_dish', x=.8, y=.7, b=.8, w=.4), k(.88, 'doorway_dark', y=.4, eye='^')],
        [(.5, 'warm')], g='use', when=['cold'], prefer=['curious'])
    # ---------------- play
    o.r('bark_through_door', 'Barking out of the doorway like he is the dog', 14, 'none',
        [k(.15, 'doorway_dark', x=.3, y=-.1), k(.35, 'frame_right', x=.8, y=-.5, b=-.2, w=.5, mark='WOOF'), k(.55, 'frame_right', x=.9, y=-.5, b=-.2, w=.8, mark='WOOF', eye='O'), k(.8, 'doorway_dark', y=-.1, eye='^')],
        [(.35, 'watch')], g='play', prefer=['happy', 'young'], say=["WOOF. Goose accent. Nobody noticed.", "I am a dog now. Bark on."])
    o.r('doorway_hops', 'Hopping in over the sill and out again, over and over', 18, 'none',
        [k(.12, 'doorsill', y=-.3, b=-.5, w=.5), k(.3, 'threshold', y=-.4, b=-.7, w=.7), k(.5, 'doorsill', y=-.3, b=-.5, w=.5, l=1), k(.7, 'threshold', y=-.4, b=-.7, w=.7, r=1), k(.88, y=0, eye='^')],
        [(.5, 'hop')], g='play', prefer=['young', 'happy'])
    o.r('bowl_hockey', 'Slapping the bowl across the path with his bill and chasing it', 20, 'none',
        [k(.12, 'bowl_rim', x=1, y=1.3, b=.4), k(.3, x=-.4, y=-.3, w=.5, eye='>', mark='tchk'), k(.45, 'bowl_edge', x=1.2, y=1.4, b=.5, r=1), k(.65, x=.7, y=.2, b=.3, w=.3), k(.85, eye='^')],
        [(.45, 'shove')], g='play', when=['bowl>.1'], prefer=['happy'])
    o.r('spy_through_knothole', 'Spying through the knothole in the left planks like a secret agent', 18, 'none',
        [k(.12, y=.2, x=.2, eye='-'), k(.3, 'knot_left', x=.9, y=.5, b=.5, eye='O'), k(.55, 'knot_left', x=1, y=.5, b=.5, eye='@', mark='psst'), k(.75, 'knot_left', x=1, y=.5, b=.5, eye='O'), k(.9, y=.2, eye='-')],
        [], g='play', prefer=['curious'], ages=YOUNG + ['juvenile'])
    o.r('jump_scare_from_dark', 'Lurking in the dark doorway and bursting out at nothing', 16, 'none',
        [k(.15, 'doorway_dark', y=.5, b=.8, eye='-'), k(.45, 'doorway_dark', y=.8, b=1, w=.2, eye='>'), k(.62, 'threshold', x=1, y=-.6, b=-.7, w=1, mark='BOO'), k(.82, 'doorsill', y=0, b=.2, eye='^')],
        [(.62, 'leap')], g='play', prefer=['young'], say=["BOO. No one was there. Still counts.", "Jumped out, nobody screamed. Tough crowd."])
    o.r('wall_circuit', 'Running laps round the front and slapping each wall in passing', 22, 'none',
        [k(.12, 'plank_left', x=.5, w=.6, l=1), k(.3, 'frame_left', x=.6, w=.6, r=1), k(.5, 'frame_right', x=.6, w=.6, l=1), k(.7, 'plank_right', x=.6, w=.6, r=1), k(.88, eye='^')],
        [(.5, 'leap')], g='play', prefer=['happy', 'young'])
    # ---------------- test
    o.r('knock_planks', 'Knocking along the planks with his bill for the one that sounds hollow', 18, 'none',
        [k(.12, 'plank_left', x=.8, y=.3, mark='tok'), k(.3, 'plank_left', x=.8, y=.3, mark='tok'), k(.5, 'plank_right', x=.8, y=.3, mark='tok'), k(.7, 'plank_right', x=.8, y=.3, mark='tonk', eye='O'), k(.88, y=.1, eye='-')],
        [], g='test', prefer=['curious'])
    o.r('count_bolts', 'Tapping each bolt along the bottom rail and counting under his breath', 18, 'none',
        [k(.12, 'bolt_a', x=.9, y=.9, b=.2, mark='1'), k(.3, 'bolt_b', x=.9, y=.9, b=.2, mark='2'), k(.5, 'bolt_c', x=.9, y=.9, b=.2, mark='3'), k(.7, 'bolt_d', x=.9, y=.9, b=.2, mark='...5'), k(.88, y=.3, eye='-', mark='lost it')],
        [], g='test', prefer=['curious'])
    o.r('shoulder_the_frame', 'Putting his shoulder to the frame to see whether the whole house tips', 18, 'none',
        [k(.15, y=.1, x=.2), k(.35, 'frame_right', x=.2, y=.4, b=.8, w=.3, mark='hnn'), k(.55, 'frame_right', x=.2, y=.4, b=1.1, w=.6, eye='>', mark='HNNN'), k(.75, x=-.3, y=.1, eye='-'), k(.9, eye='o')],
        [], g='test', ages=GROWN, obj=[(.35, dict(shake=.2)), (.55, dict(shake=.5)), (.75, dict(shake=0))])
    o.r('inspect_dish', 'Tilting his head down the dark doorway to inspect the dish at the back', 20, 'none',
        [k(.12, 'threshold', x=.4, y=.5), k(.35, 'doorway_dark', x=1, y=.9, b=.4), k(.55, 'inner_dish', x=1.2, y=1.2, b=.6, eye='O', mark='hm'), k(.75, 'doorway_dark', x=.4, y=.4, eye='-'), k(.9, eye='o')],
        [], g='test', prefer=['curious'])
    o.r('waddle_the_floor', 'Pacing the floor out in waddles, three in, three back', 22, 'none',
        [k(.12, 'doorsill', x=.3, l=1, mark='1'), k(.3, 'threshold', x=.3, r=1, mark='2'), k(.5, 'inner_dish', x=.3, l=1, mark='3'), k(.7, 'threshold', x=-.3, r=1, mark='...'), k(.88, 'doorsill', y=.2, eye='-')],
        [], g='test')
    o.r('weigh_the_bowl', 'Rocking the bowl with his foot to guess how much is in it', 16, 'none',
        [k(.15, y=.4, x=.3, l=1), k(.35, 'bowl_edge', y=.6, x=.5, l=1, b=.3), k(.55, 'bowl_edge', y=.6, x=.5, l=1, b=.4, eye='O', mark='slosh'), k(.8, y=.3, eye='-')],
        [], g='test', when=['bowl>.2'])
    # ---------------- rest
    o.r('nap_in_the_dark', 'Curling up just inside the doorway for a long doze', 30, 'none',
        [k(.15, 'threshold', x=.3, y=.3), k(.3, 'doorway_dark', y=1, b=1.1, w=.2), k(.5, 'doorway_dark', y=1.4, b=1.3, eye='-', mark='z'), k(.75, 'doorway_dark', y=1.4, b=1.3, eye='-', mark='zZ'), k(.9, y=.7, b=.5, eye='o')],
        [(.5, 'doze')], g='rest', when=['tired', 'warmth>.2'], say=["Four-hour nap. Felt like ten seconds. Perfect.", "Woke up. Regret nothing. Napping again."])
    o.r('doze_in_the_shade', 'Dozing in the shadow of the planks with his bill under a wing', 26, 'none',
        [k(.15, y=.3), k(.35, 'plank_right', x=-.2, y=.8, b=.9, w=.4), k(.6, 'plank_right', x=-.5, y=1, b=1, w=.7, eye='-', mark='z'), k(.85, 'plank_right', x=-.5, y=1, b=1, w=.7, eye='-')],
        [], g='rest', when=['sun', 'day'], prefer=['tired'])
    o.r('lean_on_warm_planks', 'Leaning his belly against sun-warmed planks', 24, 'none',
        [k(.15, y=.1, x=.2), k(.35, 'plank_right', x=.1, y=.4, b=.6, w=.2), k(.6, 'plank_right', x=.1, y=.4, b=.7, w=.4, eye='-', mark='ahh'), k(.85, 'plank_right', x=.1, y=.4, b=.7, eye='-')],
        [(.6, 'warm')], g='rest', when=['sun', 'warmth>.3'], prefer=['happy'])
    o.r('sulk_in_the_dark', 'Retreating into the dark doorway to sulk with his back to the world', 26, 'none',
        [k(.15, x=-.2, y=.2), k(.35, 'doorway_dark', x=-.5, y=.8, b=.6, eye='>'), k(.6, 'doorway_dark', x=-.6, y=1, b=.8, eye='-', mark='hmph'), k(.85, 'doorway_dark', x=-.6, y=1, b=.8, eye='-')],
        [], g='rest', when=['sad'], prefer=['grumpy'], say=["Not sulking. Brooding. It's a different font.", "Sulking. Don't ask. Don't look."])
    o.r('watch_dusk_from_sill', 'Sitting on the sill watching the light go out of the garden', 28, 'none',
        [k(.15, 'doorsill', x=.1, y=.2, b=.4), k(.4, 'doorsill', x=.3, y=-.3, b=.8, eye='-'), k(.7, 'doorsill', x=.3, y=-.4, b=.8, eye='-', mark='...'), k(.9, 'doorsill', x=.3, y=-.2, b=.8)],
        [], g='rest', when=['dusk'], prefer=['sad', 'elder'])
    o.r('sleep_upright_on_bolts', 'Sleeping upright against the bottom bolts with his bill tucked in', 30, 'none',
        [k(.15, y=.2), k(.35, 'bolt_a', x=-.2, y=.7, b=.8, w=.3), k(.6, 'bolt_a', x=-.3, y=1, b=1, w=.6, eye='-', mark='zzz'), k(.85, 'bolt_b', x=-.3, y=1, b=1, w=.6, eye='-', mark='zZ')],
        [(.6, 'doze')], g='rest', when=['night_late', 'tired'], say=["Asleep standing. Duck skill. Put it on the CV.", "Do not poke the sleeping duck. I have a plan."])
    # ---------------- weather
    o.r('tip_out_bowl', 'Heaving the rain-filled bowl over to tip it out', 20, 'none',
        [k(.15, 'bowl_rim', x=.5, y=.7, b=.3), k(.35, 'bowl_rim', x=.2, y=.2, b=.8, w=.6, mark='hng'), k(.55, 'bowl_edge', x=.6, y=.4, b=1, w=.9, mark='glug'), k(.75, x=-.5, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
        [(.55, 'tip')], g='weather', when=['bowl>.3'], ages=GROWN)
    o.r('watch_rain_from_sill', 'Watching the rain from the dry doorsill with his bill on his chest', 26, 'none',
        [k(.15, 'doorsill', y=.1, b=.3), k(.4, 'doorsill', y=.5, b=.8, eye='-'), k(.7, 'doorsill', y=.5, b=.8, eye='o', mark='drip'), k(.9, 'doorsill', y=.4, b=.7, eye='-')],
        [(.4, 'warm')], g='weather', when=['wet', 'damp<.6'])
    o.r('belly_mop_threshold', 'Dragging his belly over the sodden threshold to mop it', 18, 'none',
        [k(.15, y=.4, x=.3), k(.35, 'threshold', x=.5, y=1, b=1.2, w=.2), k(.55, 'doorsill', x=.5, y=1, b=1.3, w=.3, eye='>', mark='shhh'), k(.75, x=.1, y=.3, b=.2, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
        [(.55, 'dry')], g='weather', when=['damp>.5'], prefer=['grumpy'], say=["Wet belly. For the house. You're welcome.", "The floor is clean now. It's wet. Different."])
    o.r('scrape_frost', 'Scraping the frost off the planks with a wing', 18, 'wing',
        [k(.15, 'plank_left', reach=.6, x=.3, y=.4), k(.35, 'plank_left', reach=1, x=.4, y=.4, w=1, r=1), k(.55, 'knot_left', reach=1, x=.4, y=.3, w=1, l=1, mark='skrk'), k(.75, 'plank_left', reach=1, x=.4, y=.4, w=.8, r=1), k(.9, eye='-', mark='brr')],
        [(.55, 'scrape')], g='weather', when=['cold', 'frost>.3'], prefer=['grumpy'])
    o.r('crack_bowl_ice', 'Stamping on the iced-over bowl until the top cracks', 18, 'none',
        [k(.15, y=-.3, b=-.6, w=.5), k(.3, 'bowl_rim', y=.3, b=1, l=1, mark='crk'), k(.5, y=-.4, b=-.8, w=.7), k(.65, 'bowl_edge', y=.3, b=1.2, r=1, mark='CRACK'), k(.85, y=.2, eye='^')],
        [(.65, 'crack')], g='weather', when=['frost>.4', 'bowl>.2'], prefer=['grumpy'], say=["Ice. Broken. A foot against a puddle. Victory.", "Ice. Eleven. Me: nil. No wait. Me: one."])
    o.r('huddle_in_the_cold', 'Packing himself into the back of the kennel with his feet tucked under', 28, 'none',
        [k(.15, 'threshold', x=.3, y=.4), k(.35, 'doorway_dark', x=.4, y=.9, b=.8), k(.55, 'inner_dish', x=.3, y=1.2, b=1.2, w=.5, eye='-', mark='brr'), k(.8, 'inner_dish', x=.3, y=1.3, b=1.3, w=.8, eye='-')],
        [(.55, 'huddle')], g='weather', when=['cold', 'warmth<.4'], prefer=['tired'], say=["Frozen toes. Warm bum. Compromise.", "Warm bum. Cold toes. Fine."])
    o.r('brace_in_the_gale', 'Hanging onto the doorframe while the wind whistles through the kennel', 20, 'none',
        [k(.15, 'frame_left', x=.3, y=.3, b=.3), k(.35, 'frame_left', x=-.3, y=.6, b=.6, w=.8, eye='>'), k(.6, 'frame_right', x=-.3, y=.6, b=.7, w=.9, eye='@', mark='WHEEE'), k(.85, 'frame_left', x=.2, y=.3, b=.3, eye='-')],
        [(.35, 'snag')], g='weather', when=['windy', 'warmth<.5'])
    # ---------------- show
    o.r('shout_at_the_sign', 'Bellowing at the sign over the door that this is, in fact, his house', 14, 'none',
        [k(.15, x=.2, y=-.5, b=-.2), k(.4, x=.4, y=-1.2, b=-.4, w=.8, mark='HEY', eye='O'), k(.6, x=.4, y=-1.2, b=-.4, w=1, mark='CHEESE', eye='>'), k(.85, y=-.3, eye='^')],
        [(.4, 'mark')], g='show', far=True, prefer=['happy'], say=["Read it. It says CHEESE. Not DOG. I checked.", "Name over the door. First time in my life I've felt expensive."])
    o.r('pose_in_doorway', 'Posing in the doorway like the cover of a magazine about kennels', 18, 'none',
        [k(.15, 'threshold', x=.2, y=-.1), k(.35, 'doorway_dark', x=.4, y=-.6, b=-.2, w=.4, eye='^'), k(.6, 'doorway_dark', x=.6, y=-.8, b=-.3, w=.8, eye='^', mark='click'), k(.85, 'doorway_dark', x=.3, y=-.5, w=.4, eye='-')],
        [(.6, 'tour')], g='show', prefer=['happy'])
    o.r('knock_then_answer', 'Knocking on his own doorframe and then answering it politely', 18, 'none',
        [k(.15, 'frame_left', x=.8, y=.3, mark='tok'), k(.3, 'frame_left', x=.8, y=.3, mark='tok'), k(.45, 'doorsill', y=.1, x=-.3), k(.6, 'threshold', x=.3, y=-.3, b=-.2, w=.4, eye='o', mark='Hello?'), k(.85, y=-.2, eye='^')],
        [(.3, 'tour')], g='show', say=["Who is it? Me. Come in, me.", "Always so good to see me."])
    o.r('house_tour', 'Giving the house a tour: the door, the planks, the bolts, the bowl', 26, 'wing',
        [k(.12, 'frame_left', reach=.8, x=.3, y=-.2, w=1), k(.3, 'plank_left', reach=.8, x=.4, y=-.3, w=1), k(.5, 'bolt_c', reach=.8, x=.4, y=.2, w=1), k(.7, 'bowl_rim', reach=.8, x=.4, y=.4, w=1), k(.88, y=-.2, w=.6, eye='^')],
        [(.5, 'tour')], g='show', ages=GROWN, say=["On your left, a wall. On your right, a wall. Questions? No.", "Gift shop's closed. As is everything else."])
    o.r('point_at_the_roof', 'Pointing his wing at the roof and naming the unlicensed architect', 14, 'none',
        [k(.15, x=.2, y=-.2), k(.4, x=.4, y=-.9, w=.8, reach=1, eye='>'), k(.6, x=.4, y=-1, w=1, reach=1, mark='THAT'), k(.85, y=-.2, eye='-')],
        [(.4, 'tour')], g='show', far=True)
    o.r('bow_to_nobody', 'Bowing on the doorstep to an audience of nobody', 16, 'none',
        [k(.15, 'doorsill', x=.1, y=-.3, w=.3), k(.35, 'doorsill', x=.5, y=1.2, b=.8, w=1, eye='^'), k(.55, 'doorsill', x=.5, y=1.2, b=.8, w=1), k(.75, 'doorsill', x=.1, y=-.4, w=.6, eye='o'), k(.9, eye='^')],
        [(.35, 'tour')], g='show', prefer=['happy'], say=["Thank you. Thank you. The garden loved it.", "Standing ovation. From a bush. Counts."])
    # ---------------- mishap
    o.r('tail_snagged_on_bolt', 'Backing out of the corner and snagging his tail on a bolt', 18, 'none',
        [k(.15, 'doorway_dark', x=.2, y=.3), k(.3, 'bolt_a', x=-.4, y=.3, b=.3, l=1, mark='step'), k(.5, 'bolt_a', x=-1, y=.3, b=.6, w=.8, eye='O', mark='SNAG'), k(.75, 'bolt_a', x=-1.2, y=.4, b=.8, w=1, r=1, mark='RIP'), k(.9, eye='@')],
        [(.5, 'snag')], g='mishap', prefer=['young'], say=["Snagged. The bolt won. Again.", "My tail is on the house. Leave it."])
    o.r('slip_on_wet_sill', 'Skidding across the wet sill and ending up flat in the doorway', 18, 'none',
        [k(.15, 'doorsill', x=.4, l=1), k(.3, 'doorsill', x=1, y=.5, b=-.4, w=1, eye='O', mark='WHOA'), k(.5, 'threshold', x=1.4, y=1.5, b=1.2, w=.4, mark='SPLAT'), k(.75, 'threshold', y=1.4, b=1.1, eye='@'), k(.9, y=.5, eye='-')],
        [(.5, 'slosh')], g='mishap', when=['damp>.4'], say=["Wet sill. Flat duck. I blame the sill.", "Slid right in. Style: none."])
    o.r('step_in_the_bowl', 'Stepping into the bowl and having to hop home with it as a boot', 18, 'none',
        [k(.15, y=.1, x=.3, l=1), k(.3, 'bowl_rim', x=.3, y=.3, b=.3, l=1, eye='O', mark='plip'), k(.5, 'bowl_edge', x=.2, y=.4, b=.7, l=1, mark='clonk'), k(.7, 'bowl_edge', x=.1, y=.5, b=.8, r=1, w=.7, eye='>'), k(.88, eye='-')],
        [(.5, 'slosh')], g='mishap', when=['bowl>.2'], prefer=['young', 'curious'], say=["Foot in bowl. Bowl on foot. We are one.", "Foot in the bowl. Bowl on the foot. Pals."])
    o.r('stuck_in_doorframe', 'Charging the doorway too wide and wedging at the shoulders', 22, 'none',
        [k(.12, x=.5, y=.1, w=.7, eye='>'), k(.3, 'frame_left', x=.8, y=.1, w=1, mark='oof'), k(.5, 'frame_right', x=1, y=.1, w=1, l=1, eye='@', mark='mmmf'), k(.7, 'frame_left', x=1.1, y=.1, w=1, r=1, mark='POP'), k(.88, x=1.6, y=.8, b=.5, eye='-')],
        [(.7, 'rub')], g='mishap', ages=GROWN, say=["The doorway shrank. That's the only explanation.", "Wedged in a dog door. Don't mention it."])
    o.r('fly_chase_headbutt', 'Snapping at a fly in the doorway and headbutting the frame instead', 16, 'none',
        [k(.12, 'threshold', x=.3, y=-.2, b=-.3, eye='>'), k(.3, x=.8, y=-.6, b=-.5, w=.6, eye='@', mark='snap'), k(.5, 'frame_right', x=1.6, y=.2, b=.4, w=1, mark='BONK'), k(.7, 'plank_right', x=-.3, y=.8, b=.8, eye='@'), k(.88, eye='-')],
        [(.5, 'snag')], g='mishap', ages=YOUNG, prefer=['curious'], obj=[(.5, dict(shake=.5)), (.7, dict(shake=0))])
    return o


def toy_car():
    P = lambda c, r: (round(c / 65, 3), round(r / 38, 3))
    o = Obj('toy_car', 'placed',
            fields=dict(speed=(0, 0, 1), air=(1, 0, 1), puddle=(0, 0, 1), frost=(0, 0, 1), lamp=(0, 0, 1)),
            physics=[('speed', 'decay', 0, 'always'), ('air', 'rate', -.00005, 'always'), ('air', 'rate', -.0003, 'cold'), ('puddle', 'rate', .003, 'wet'),
                     ('puddle', 'rate', -.0005, 'dry&warm'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('lamp', 'rate', -.004, 'always')],
            effects=dict(
                polish=[('obj.dirt', 'add', -.25)], buff=[('obj.dirt', 'add', -.1), ('obj.condition', 'add', .02)], scoop=[('obj.dirt', 'add', -.2), ('speed', 'add', .05)],
                pick=[('obj.dirt', 'add', -.15), ('air', 'add', -.02)], fix=[('obj.condition', 'add', .05)], wipe=[('obj.dirt', 'add', -.15), ('frost', 'mul', .3)],
                push=[('speed', 'set', 1)], haul=[('speed', 'add', .3)], flick=[('lamp', 'set', 1)], dark=[('lamp', 'set', 0)], brake=[('speed', 'set', 0)],
                steer=[('speed', 'set', .5), ('obj.dirt', 'add', .02)], fun=[('need.fun', 'add', 2)], nudge=[('speed', 'add', .15), ('obj.dirt', 'add', .02)], doze=[('need.energy', 'add', 3)],
                pump=[('air', 'set', 1)], scrape=[('frost', 'set', 0)], chip=[('frost', 'mul', .6), ('air', 'add', .05)], splash=[('puddle', 'mul', .4), ('obj.wetness', 'add', .1)],
                dry=[('obj.wetness', 'add', -.3), ('puddle', 'add', -.1)], keep=[('lamp', 'set', 1), ('need.fun', 'add', 1)], rev=[('speed', 'add', .2), ('lamp', 'add', .3)],
                pin=[('speed', 'mul', .2), ('obj.dirt', 'add', .05)], bump=[('obj.condition', 'add', -.04)], company=[('need.social', 'add', 2)], mirror=[('lamp', 'add', .2)], slap=[('speed', 'add', .1), ('obj.dirt', 'add', .03)], rattle=[('obj.dirt', 'add', .03), ('air', 'add', -.03)], glint=[('obj.dirt', 'add', -.05), ('lamp', 'add', .1)], jam=[('lamp', 'set', 1), ('obj.condition', 'add', -.02)]),
            anchors=dict(tread_left=P(20, 35), tread_right=P(47, 35), tyre_front=P(12, 32), tyre_back=P(53, 32), hub_left=P(19, 31), hub_right=P(46, 31),
                         arch_left=P(19, 27), arch_right=P(46, 27), sill=P(30, 29), under_mid=P(32, 33), headlamp=P(12, 26), tail_lamp=P(52, 26),
                         door_panel=P(30, 22), belt_left=P(12, 23), belt_mid=P(33, 23), belt_right=P(54, 23), side_left=P(9, 25), side_right=P(56, 25),
                         hood_top=P(15, 18), window_sill=P(30, 16), window_glass=P(40, 12)))
    # ---------------- care
    o.r('polish_door', 'Polishing the door panel in slow circles with a wing', 18, 'wing',
        [k(.15, 'door_panel', reach=.6, x=.3, y=-.1), k(.3, 'door_panel', reach=1, x=.3, y=-.1, w=.8, l=1), k(.5, 'belt_mid', reach=1, x=.3, y=-.2, w=1, r=1), k(.7, 'door_panel', reach=1, x=.3, y=-.1, w=.8, l=1), k(.9, y=.1, eye='^')],
        [(.5, 'polish')], g='care', prefer=['grown'], say=["Mirror finish. I can see my disappointment.", "Shiny. Now it just needs somewhere to go."])
    o.r('buff_hubs', 'Buffing each hub with the underside of a wing until it winks', 18, 'wing',
        [k(.15, 'hub_left', reach=.7, x=.3, y=.6, b=.2), k(.3, 'hub_left', reach=1, x=.4, y=.7, b=.4, w=1, l=1), k(.55, 'hub_right', reach=1, x=.4, y=.7, b=.4, w=1, r=1), k(.75, 'hub_right', reach=1, x=.3, y=.6, b=.3, w=.6, mark='ting'), k(.9, eye='^')],
        [(.55, 'buff')], g='care')
    o.r('scoop_arch_grit', 'Scooping packed grit out of the wheel arches with his bill', 20, 'none',
        [k(.12, x=.5, y=.4), k(.3, 'arch_left', x=1.1, y=.5, b=.2, mark='scrk'), k(.5, 'arch_left', x=1.3, y=.4, b=.2, eye='O'), k(.7, 'arch_right', x=1.1, y=.5, b=.2, mark='scrk'), k(.88, eye='^')],
        [(.5, 'scoop')], g='care', ages=GROWN, prefer=['grumpy'], obj=[(.5, dict(sway=.2))])
    o.r('pick_tread', 'Picking dried mud out of the tread one chunk at a time', 20, 'none',
        [k(.12, y=.5, x=.3), k(.3, 'tread_left', x=1, y=1.5, b=.6, mark='tk'), k(.5, 'tread_left', x=1, y=1.5, b=.6, w=.4, mark='tk'), k(.7, 'tread_right', x=1, y=1.5, b=.6, mark='tk'), k(.88, y=.2, eye='-')],
        [(.5, 'pick')], g='care', prefer=['curious'], say=["Mud. All of it. Mine now. Gross.", "Gunk out. Gunk in my mouth. Fair trade."])
    o.r('tighten_hub_nut', 'Turning a loose hub nut tight with his bill', 16, 'none',
        [k(.15, y=.4, x=.5), k(.3, 'hub_left', x=1.1, y=1, b=.5, mark='crk'), k(.45, 'hub_left', x=1.1, y=1, b=.5, w=.3, mark='crk'), k(.6, 'hub_left', x=1.2, y=1.1, b=.6, w=.6, eye='>', mark='SNK'), k(.85, y=.2, eye='^')],
        [(.6, 'fix')], g='care', ages=GROWN)
    o.r('wipe_cabin_glass', 'Wiping the cabin glass corner to corner with a wing', 18, 'wing',
        [k(.15, 'window_sill', reach=.7, x=.2, y=-.3, w=.4), k(.3, 'window_glass', reach=1, x=.2, y=-.6, w=1, l=1), k(.5, 'window_sill', reach=1, x=.2, y=-.4, w=1, r=1), k(.7, 'window_glass', reach=1, x=.2, y=-.6, w=1, l=1), k(.9, eye='^')],
        [(.5, 'wipe')], g='care', ages=GROWN)
    # ---------------- use
    o.r('shove_from_behind', 'Putting his breast to the tail and shoving the car forward', 18, 'none',
        [k(.12, x=.5, y=.3, eye='>'), k(.3, 'side_right', x=.9, y=.6, b=.7, w=.3, mark='hup'), k(.5, 'side_right', x=1.1, y=.7, b=1, w=.3, r=1, mark='HUP'), k(.7, x=.9, y=.5, b=.4, l=1), k(.88, eye='^')],
        [(.5, 'push')], g='use', prefer=['happy'], obj=[(.5, dict(shake=.3)), (.7, dict(sway=.6))], say=["Go on then. Off you go.", "Rolled it. Not one thank you."])
    o.r('haul_back_by_bumper', 'Hauling the car back by its front end with his bill', 18, 'none',
        [k(.12, y=.4, x=.3), k(.3, 'side_left', x=1, y=.8, b=.5), k(.5, 'side_left', x=-.6, y=.6, b=1, w=.5, mark='hnng'), k(.7, 'side_left', x=-.8, y=.6, b=1.1, w=.6, l=1, mark='HNNG'), k(.88, eye='-')],
        [(.5, 'haul')], g='use', ages=GROWN, obj=[(.5, dict(shake=.4)), (.7, dict(sway=-.5))])
    o.r('peck_headlamp_awake', 'Pecking the headlamp awake', 14, 'none',
        [k(.15, y=.3, x=.5), k(.3, 'headlamp', x=1, y=.6, b=.3, mark='tk'), k(.5, 'headlamp', x=.4, y=-.2, w=.4, eye='O'), k(.75, x=-.2, y=0, eye='^')],
        [(.3, 'flick')], g='use', when=['lamp<.5'], obj=[(.3, dict(glow=.6)), (.5, dict(glow=1))], say=["Let there be glare.", "Lights on. Nobody's home. Waste of a lamp."])
    o.r('smother_tail_lamp', 'Smothering the tail lamp under a wing to put it out', 14, 'wing',
        [k(.15, 'tail_lamp', reach=.6, x=.3, y=.3), k(.35, 'tail_lamp', reach=1, x=.3, y=.4, b=.3, w=1), k(.55, 'tail_lamp', reach=1, x=.3, y=.4, b=.3, w=1, eye='-'), k(.8, y=.1, eye='^')],
        [(.35, 'dark')], g='use', when=['lamp>.5'], obj=[(.35, dict(glow=.2)), (.6, dict(glow=0))])
    o.r('chock_the_front_tyre', 'Throwing himself against the front tyre to stop the car rolling', 16, 'none',
        [k(.12, x=.6, y=.2, eye='>'), k(.3, 'tyre_front', x=.8, y=.6, b=.8, w=.7, mark='WHUMP'), k(.5, 'tyre_front', x=.9, y=.6, b=1.2, w=.5, eye='@', mark='nnh'), k(.75, y=.3, b=.4, eye='-')],
        [(.5, 'brake')], g='use', when=['speed>.3'], obj=[(.3, dict(shake=.6)), (.5, dict(sway=0))], say=["Stopped it. With my face. Tactical.", "Stopped it. Cheese 1, car 0. Faceplant counts."])
    o.r('steer_by_the_tyres', 'Leaning on the front tyre while dragging the back one to steer', 20, 'none',
        [k(.12, 'tyre_front', x=.8, y=.4, b=.4), k(.3, 'tyre_front', x=1, y=.5, b=.7, w=.4, l=1), k(.55, 'tyre_back', x=-.6, y=.4, b=.9, w=.5, r=1, mark='nngh'), k(.75, 'tyre_back', x=-.7, y=.4, b=.8, w=.3), k(.9, eye='^')],
        [(.55, 'steer')], g='use', ages=GROWN, obj=[(.3, dict(sway=.3)), (.55, dict(sway=.7)), (.75, dict(sway=.2))])
    # ---------------- play
    o.r('ride_the_sill', 'Riding the rolling car on the sill with his wings out like a surfer', 20, 'none',
        [k(.12, 'sill', y=.3, b=.4, w=.3, l=1), k(.3, 'sill', y=-.2, b=.5, w=1, eye='O', mark='WOO'), k(.55, 'sill', y=-.3, b=.6, w=1, l=1, eye='^'), k(.8, 'sill', y=0, b=.4, w=.6, r=1, mark='wobble'), k(.9, eye='@')],
        [(.3, 'fun')], g='play', when=['speed>.3'], prefer=['happy', 'young'], obj=[(.3, dict(sway=.5)), (.6, dict(sway=-.4))], say=["WOO. Wheeeeee. Ahem. I mean: acceptable.", "Surfing a toy. Best day of the week."])
    o.r('tyre_to_tyre_hops', 'Hopping from one tyre to the other like stepping stones', 18, 'none',
        [k(.12, 'tread_left', y=.2, b=.5, l=1), k(.3, y=-.5, b=-.8, w=.8), k(.45, 'under_mid', y=.4, b=.8, r=1), k(.62, y=-.5, b=-.8, w=.8), k(.78, 'tread_right', y=.2, b=.5, l=1), k(.9, eye='^')],
        [(.45, 'fun')], g='play', prefer=['young', 'happy'])
    o.r('race_alongside', 'Racing alongside the rolling car and slapping every panel', 20, 'none',
        [k(.12, 'side_left', x=.6, w=.6, l=1), k(.3, 'door_panel', x=.8, w=.7, r=1), k(.5, 'belt_mid', x=.9, w=.7, l=1), k(.7, 'side_right', x=1, w=.8, r=1, eye='>'), k(.88, x=.2, w=.4, eye='^')],
        [(.5, 'slap')], g='play', when=['speed>.3'], prefer=['happy'])
    o.r('hide_beneath_car', 'Hiding beneath the car between the wheels and jumping out at its tyres', 22, 'none',
        [k(.12, y=.4, b=.4), k(.3, 'under_mid', y=1.2, b=1.2, w=.2, eye='-'), k(.5, 'under_mid', y=1.3, b=1.3, w=.3, eye='>'), k(.68, 'hub_right', x=1, y=-.4, b=-.8, w=1, mark='BOO'), k(.88, eye='^')],
        [(.68, 'rattle')], g='play', ages=YOUNG + ['juvenile'], prefer=['young'])
    o.r('billiards_nudges', 'Nudging the car along with the tip of his bill like a billiards cue', 18, 'none',
        [k(.15, y=.3, x=.4), k(.3, 'side_left', x=1.2, y=1.1, b=.2, mark='tk'), k(.5, x=-.2, y=.4, eye='>'), k(.65, 'side_left', x=1.4, y=1.1, b=.2, mark='TK'), k(.85, y=.2, eye='-')],
        [(.65, 'nudge')], g='play', prefer=['curious'], obj=[(.3, dict(sway=.2)), (.65, dict(sway=.5))])
    o.r('rev_and_launch', 'Making engine noises at the tyre, then launching it with a kick', 18, 'none',
        [k(.15, 'tread_left', x=.6, y=.6, b=.3, mark='brm'), k(.35, 'tread_left', x=.6, y=.6, b=.4, w=.4, mark='BRRM'), k(.55, 'tyre_front', x=.4, y=.3, b=-.4, l=1, w=1, mark='VROOM'), k(.75, x=.8, y=.2, eye='^')],
        [(.55, 'rev')], g='play', prefer=['happy', 'young'], obj=[(.35, dict(shake=.4)), (.55, dict(glow=.6, sway=.8))], say=["Brmbrm. It's a duck car now.", "VROOM. Subtle. As ever."])
    # ---------------- test
    o.r('tap_the_glass', 'Tapping the cabin glass to find out whether anyone is in', 16, 'none',
        [k(.12, y=-.2, x=.3), k(.3, 'window_sill', x=.9, y=-.4, mark='tok'), k(.5, 'window_glass', x=.9, y=-.5, mark='tok'), k(.75, y=-.2, x=-.1, eye='-', mark='nobody')],
        [], g='test', ages=GROWN, prefer=['curious'])
    o.r('smell_the_rubber', 'Sniffing the tread to see what it has been driven through', 14, 'none',
        [k(.15, y=.6, x=.4), k(.35, 'tread_right', x=1, y=1.6, b=.6, eye='O'), k(.55, 'tread_right', x=1.2, y=1.7, b=.6, eye='O', mark='sniff'), k(.8, x=-.3, y=.3, eye='-')],
        [], g='test', prefer=['curious', 'young'])
    o.r('squeeze_tyre_check', 'Squeezing the tyre wall in his bill to gauge the air', 16, 'none',
        [k(.15, y=.4, x=.4), k(.3, 'tyre_back', x=1, y=.8, b=.4), k(.5, 'tyre_back', x=1.1, y=.8, b=.4, eye='O', mark='squish'), k(.75, 'tyre_front', x=1, y=.8, b=.4), k(.9, eye='-')],
        [], g='test', when=['air<.9'], prefer=['curious'])
    o.r('door_lean_test', 'Leaning on the door with his whole weight to see if the brake is on', 18, 'none',
        [k(.15, y=.1, x=.3), k(.35, 'door_panel', x=.6, y=.2, b=.8, w=.3, mark='hnn'), k(.55, 'door_panel', x=.7, y=.2, b=1.1, w=.6, eye='>', mark='HNNN'), k(.75, x=-.2, y=.1, eye='-')],
        [], g='test', ages=GROWN, when=['speed<=.3'], obj=[(.35, dict(sway=.2)), (.55, dict(sway=.5))])
    o.r('waddle_the_length', 'Waddling the length of the car to measure it: nine steps, then twelve', 20, 'none',
        [k(.12, 'headlamp', x=.3, l=1, mark='1'), k(.3, 'door_panel', x=.4, r=1, mark='5'), k(.5, 'tail_lamp', x=.4, l=1, mark='9'), k(.7, 'door_panel', x=-.2, y=.3, r=1, mark='12?'), k(.88, 'headlamp', y=.3, eye='-')],
        [], g='test', say=["Nine one way, twelve the other. The car is lying.", "Measured it. Still not enough room for my pride."])
    o.r('rap_the_belt', 'Rapping the belt bar from end to end and humming the notes', 18, 'none',
        [k(.12, 'belt_left', x=.8, y=.1, mark='tk'), k(.3, 'belt_mid', x=.8, y=.1, mark='tk'), k(.5, 'belt_right', x=.8, y=.1, mark='tk'), k(.7, 'belt_mid', x=.5, y=0, mark='tk'), k(.88, y=0, eye='-')],
        [], g='test', ages=['duckling', 'juvenile'] + GROWN[1:])
    # ---------------- rest
    o.r('doze_under_the_car', 'Dozing in the shade under the car with his bill on his chest', 30, 'none',
        [k(.15, y=.4, b=.3), k(.35, 'under_mid', y=1.4, b=1.3, w=.2), k(.6, 'under_mid', y=1.6, b=1.5, eye='-', mark='z'), k(.85, 'under_mid', y=1.6, b=1.5, eye='-', mark='zZ')],
        [(.6, 'doze')], g='rest', when=['tired', 'sun'], say=["Shade. Quiet. A tyre for a pillow. Four stars.", "Slept under a car. This is what freedom looks like."])
    o.r('slump_against_door', 'Slumping against the door panel with his feet stuck out', 24, 'none',
        [k(.15, x=.1, y=.2), k(.35, 'door_panel', x=.2, y=.5, b=.8, w=.2), k(.6, 'door_panel', x=.1, y=.7, b=1, eye='-', mark='ahh'), k(.85, 'door_panel', x=.1, y=.7, b=1, eye='-')],
        [(.6, 'doze')], g='rest', when=['tired'], prefer=['elder'])
    o.r('sit_on_the_arch', 'Perching on the wheel arch with his feet swinging', 24, 'none',
        [k(.15, y=-.2, b=-.4, w=.6), k(.35, 'arch_left', y=.2, b=.6, w=.2, l=1), k(.6, 'arch_left', y=.3, b=.7, r=1, eye='-'), k(.85, 'arch_left', y=.3, b=.7, l=1, eye='-')],
        [], g='rest', when=['sun'], prefer=['happy'])
    o.r('sulk_behind_tail', 'Sulking behind the tail lamp where nobody can see him', 24, 'none',
        [k(.15, x=-.2, y=.3), k(.35, 'tail_lamp', x=-.5, y=.9, b=.6, eye='>'), k(.6, 'tail_lamp', x=-.6, y=1, b=.8, eye='-', mark='hmph'), k(.85, 'tail_lamp', x=-.6, y=1, b=.8, eye='-')],
        [], g='rest', when=['sad'], prefer=['grumpy'], say=["Sulking. Car's fine. It doesn't talk back.", "I'm not upset. The car is upset. Through me."])
    o.r('chat_with_headlamp', 'Sitting by the headlamp and talking to it like company', 26, 'none',
        [k(.15, x=.2, y=.2), k(.35, 'headlamp', x=.8, y=.3, b=.5, eye='o'), k(.6, 'headlamp', x=.8, y=.2, b=.6, w=.4, mark='...', eye='^'), k(.85, 'headlamp', x=.7, y=.3, b=.6, eye='-')],
        [(.6, 'company')], g='rest', when=['lonely'], say=["Good chat. You listen better than the ducks.", "Same time tomorrow? You'll be here. You always are."])
    o.r('shelter_beneath_in_rain', 'Backing under the sill out of the rain and watching the drops run off', 28, 'none',
        [k(.15, y=.4, b=.2), k(.35, 'sill', x=-.2, y=.8, b=.8, w=.3), k(.6, 'sill', x=-.2, y=1, b=1, eye='-', mark='drip'), k(.85, 'sill', x=-.2, y=1, b=1, eye='-')],
        [(.6, 'doze')], g='rest', when=['wet', 'puddle<.7'])
    # ---------------- weather
    o.r('stomp_the_puddle', 'Stomping in the puddle under the tyre until it is all over the car', 18, 'none',
        [k(.12, y=.3, x=.3), k(.3, 'tyre_front', y=.5, b=.7, l=1, mark='splash'), k(.5, 'tyre_front', y=.5, b=.8, r=1, mark='SPLOSH'), k(.7, 'hub_left', y=.5, b=.8, l=1, eye='O'), k(.88, eye='^')],
        [(.5, 'splash')], g='weather', when=['puddle>.4'], prefer=['happy', 'young'], say=["Puddle. Mine. Look at the state of the car.", "Splashed. Cleaned. Soaked. Pick one."])
    o.r('dry_the_hubs_in_sun', 'Drying the wet hubs off with his tail feathers in the sun', 22, 'none',
        [k(.15, x=-.2, y=.2), k(.3, 'hub_left', x=-.5, y=.5, b=.6, w=.3), k(.55, 'hub_right', x=-.6, y=.5, b=.7, w=.5, mark='fff'), k(.8, x=0, y=.2, eye='^')],
        [(.55, 'dry')], g='weather', when=['sun', 'puddle>.3'])
    o.r('scrape_the_windscreen', 'Scraping the frost off the cabin glass with a wing', 22, 'wing',
        [k(.15, 'window_sill', reach=.7, x=.2, y=-.4, w=.4), k(.35, 'window_glass', reach=1, x=.2, y=-.7, w=1, r=1, mark='skrk'), k(.55, 'window_glass', reach=1, x=.2, y=-.7, w=1, l=1, mark='skrk'), k(.8, eye='-', mark='brr')],
        [(.55, 'scrape')], g='weather', when=['cold', 'frost>.3'], ages=GROWN, prefer=['grumpy'])
    o.r('chip_frost_off_treads', 'Chipping frost out of the treads with the tip of his bill', 20, 'none',
        [k(.12, y=.5, x=.3), k(.3, 'tread_left', x=1, y=1.4, b=.5, mark='tik'), k(.5, 'tread_left', x=1, y=1.4, b=.5, eye='O', mark='TIK'), k(.7, 'tread_right', x=1, y=1.4, b=.5, mark='tik'), k(.88, eye='-', mark='brr')],
        [(.5, 'chip')], g='weather', when=['frost>.3', 'cold'])
    o.r('cup_the_headlamp', 'Cupping a wing round the headlamp to keep it alight in the wind', 22, 'wing',
        [k(.15, 'headlamp', reach=.7, x=.4, y=.1, w=.5), k(.35, 'headlamp', reach=1, x=.3, y=.2, b=.4, w=1, eye='>'), k(.6, 'headlamp', reach=1, x=.3, y=.2, b=.4, w=1, eye='@', mark='fff'), k(.85, 'headlamp', reach=.6, x=.2, y=.1, w=.5, eye='-')],
        [(.35, 'keep')], g='weather', when=['windy', 'lamp>.2'], obj=[(.35, dict(glow=1)), (.6, dict(glow=.8))], say=["Not on my watch. Not in this wind.", "The wind blew. The lamp held. So did I."])
    o.r('huff_the_stiff_tyre', 'Huffing warm breath into the valve of the stiff cold tyre until it plumps', 22, 'none',
        [k(.12, y=.5, x=.3), k(.3, 'hub_right', x=1, y=1, b=.5, mark='hff'), k(.5, 'hub_right', x=1, y=1, b=.7, w=.4, mark='HHFF'), k(.7, 'hub_right', x=1, y=1, b=.7, eye='O', mark='puff'), k(.88, y=.2, eye='^')],
        [(.5, 'pump')], g='weather', when=['cold', 'air<.6'], obj=[(.5, dict(puff=.6))])
    o.r('heave_against_wind_roll', 'Heaving against the side to stop the wind rolling the car off', 20, 'none',
        [k(.12, x=.5, y=.3, eye='>'), k(.3, 'door_panel', x=.7, y=.4, b=.8, w=.5, mark='hnn'), k(.55, 'door_panel', x=.7, y=.4, b=1.2, w=.8, eye='@', mark='HNNNN'), k(.8, x=.1, y=.2, eye='-')],
        [(.55, 'brake')], g='weather', when=['windy', 'speed>.3'], ages=GROWN, obj=[(.3, dict(sway=.5)), (.55, dict(sway=0))])
    # ---------------- show
    o.r('preen_in_the_glass', 'Preening in the dark cabin glass like it is a mirror', 20, 'none',
        [k(.15, y=-.2), k(.3, 'window_sill', x=.7, y=-.4, w=.4), k(.5, 'window_glass', x=.7, y=-.7, w=.7, eye='^', mark='hm'), k(.75, 'window_glass', x=.8, y=-.7, w=.2, eye='o'), k(.9, eye='^')],
        [(.5, 'mirror')], g='show', ages=GROWN, say=["Stunning. Of course. Anyone else here?", "That duck again. Looking good, mate."])
    o.r('hood_ornament_pose', 'Freezing on the hood with his bill out as the ornament', 22, 'none',
        [k(.15, 'sill', y=.3, b=.4), k(.35, 'hood_top', x=.8, y=-.4, b=-.2, w=1, eye='^'), k(.6, 'hood_top', x=.9, y=-.5, b=-.2, w=1, eye='>'), k(.85, 'hood_top', x=.9, y=-.4, w=.8, eye='^')],
        [(.35, 'mirror')], g='show', ages=GROWN, prefer=['happy'])
    o.r('reveal_the_hub', 'Whipping a wing off the hub like a magician revealing a trick', 16, 'wing',
        [k(.15, 'hub_right', reach=.7, x=.2, y=.3, w=.5), k(.4, 'hub_right', reach=.2, x=.1, y=-.5, b=-.3, w=1, eye='O', mark='TA-DA'), k(.7, 'hub_right', reach=.2, x=.1, y=-.4, w=1, eye='^'), k(.88, y=0, w=.3, eye='o')],
        [(.4, 'glint')], g='show', say=["Ta-da. Hubcap. Nothing up my sleeve. I have no sleeves.", "Tada. Hubcap. Hold the applause."])
    o.r('parade_lap', 'Parading all round the car in a high march and saluting every lamp', 24, 'none',
        [k(.12, 'headlamp', y=-.5, b=-.3, w=.5, l=1), k(.3, 'side_left', y=-.5, b=-.3, w=.7, r=1), k(.5, 'tail_lamp', y=-.5, b=-.3, w=.7, l=1), k(.7, 'side_right', y=-.5, b=-.3, w=.7, r=1), k(.88, 'headlamp', y=-.4, w=1, eye='^')],
        [(.5, 'flick')], g='show', obj=[(.5, dict(glow=.8))], prefer=['happy'])
    o.r('wind_up_the_take_off', 'Charging it like a starting grid and shoving it off with a flourish', 20, 'none',
        [k(.12, x=-.4, y=-.3, b=-.2, w=.5), k(.3, 'side_right', x=.2, y=.4, b=.8, w=.2, mark='READY'), k(.5, 'side_right', x=.8, y=.5, b=1.2, w=1, mark='GO'), k(.75, x=.6, y=0, w=1, eye='^')],
        [(.5, 'haul')], g='show', ages=GROWN, obj=[(.5, dict(sway=.8, shake=.3))])
    o.r('signal_then_stay', 'Flashing the tail lamp with a wing to signal a left turn, then not turning', 18, 'wing',
        [k(.15, 'tail_lamp', reach=.6, x=.2, y=.2), k(.3, 'tail_lamp', reach=1, x=.2, y=.2, w=1, eye='o'), k(.5, 'tail_lamp', reach=.4, x=.3, y=0, w=.4, mark='tik tik'), k(.7, 'tail_lamp', reach=1, x=.2, y=.2, w=1), k(.88, y=-.2, eye='-', mark='...')],
        [(.3, 'flick')], g='show', obj=[(.3, dict(glow=1)), (.5, dict(glow=0)), (.7, dict(glow=1))], say=["Indicated. Did not turn. Rules are guidelines.", "Left, signalling. Straight, going."])
    # ---------------- mishap
    o.r('foot_under_the_tyre', 'Letting the car roll slowly onto his foot and hopping about', 18, 'none',
        [k(.12, 'tyre_front', y=.3, x=.3, l=1), k(.3, 'tyre_front', y=.6, b=.5, r=1, eye='O', mark='hm'), k(.5, 'tyre_front', y=.8, b=.8, r=1, eye='@', mark='OW'), k(.7, 'tyre_front', y=-.3, b=-.7, w=1, l=1, mark='AAH'), k(.88, y=.4, eye='-')],
        [(.5, 'pin')], g='mishap', when=['speed>.3'], prefer=['young'], obj=[(.3, dict(sway=.3)), (.5, dict(shake=.2))], say=["Ow. Shit. It's on my foot. It was my foot a minute ago.", "It's on my foot. Please advise."])
    o.r('slip_in_the_puddle', 'Slipping in the puddle beside the car and sliding into the tyre', 18, 'none',
        [k(.15, y=.1, x=.4, l=1), k(.3, 'tread_left', x=1.2, y=.4, b=-.3, w=1, eye='O', mark='WHOA'), k(.5, 'tyre_front', x=1.5, y=1.5, b=1.2, mark='SPLAT'), k(.75, 'tyre_front', y=1.3, b=1, eye='@'), k(.9, y=.5, eye='-')],
        [(.5, 'splash')], g='mishap', when=['puddle>.4'], say=["Wet. Tyre. Face. In that order.", "Wet floor. I said what I said."])
    o.r('head_stuck_in_lamp', 'Putting his bill in the headlamp to peek and getting it stuck', 20, 'none',
        [k(.12, y=.2, x=.5), k(.3, 'headlamp', x=1.3, y=.4, b=.4), k(.5, 'headlamp', x=1.5, y=.4, b=.7, w=.4, l=1, eye='@', mark='mmf'), k(.7, 'headlamp', x=1.6, y=.4, b=.8, w=1, r=1, mark='POP'), k(.88, x=-.2, y=.5, eye='O')],
        [(.5, 'jam')], g='mishap', prefer=['young', 'curious'], obj=[(.5, dict(glow=1, shake=.3)), (.7, dict(shake=.6))], say=["It lit up. I did that. With my face.", "Don't ask. Don't film. Leave."])
    o.r('knocked_by_the_belt', 'Standing up fast under the belt bar and clonking his skull', 16, 'none',
        [k(.12, 'under_mid', y=.5, b=.8), k(.3, 'under_mid', y=-.2, b=-.4, w=.6), k(.45, 'belt_left', y=-.8, b=-.9, w=1, eye='@', mark='CLONK'), k(.7, 'belt_left', y=1, b=1, eye='@'), k(.88, eye='-')],
        [(.45, 'bump')], g='mishap', ages=['duckling', 'juvenile'])
    o.r('bounced_off_the_arch', 'Wedging between the tyre and the arch and popping out like a cork', 20, 'none',
        [k(.12, x=.5, eye='>'), k(.3, 'arch_right', x=.9, y=.1, b=.4, w=.4, mark='oof'), k(.5, 'arch_right', x=1, y=.1, b=.7, l=1, eye='O', mark='mmf'), k(.7, 'arch_right', x=1.2, y=.1, b=.8, r=1, w=1, mark='POP'), k(.88, x=1.6, y=.9, b=.6, eye='@')],
        [(.7, 'bump')], g='mishap', ages=['juvenile', 'young_adult', 'adult', 'mature'])
    return o


def gazebo():
    P = lambda c, r: (round(c / 105, 3), round(r / 53, 3))
    o = Obj('gazebo', 'placed',
            fields=dict(leaves=(0, 0, 1), puddle=(0, 0, 1), warm=(0, 0, 1), frost=(0, 0, 1), bloom=(0, 0, 1), echo=(0, 0, 1)),
            physics=[('leaves', 'rate', .002, 'windy'), ('puddle', 'rate', .003, 'wet'), ('puddle', 'rate', -.0005, 'dry&warm'), ('warm', 'rate', .0004, 'sun'),
                     ('warm', 'rate', -.0006, 'cold'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('bloom', 'rate', .0004, 'sun'),
                     ('bloom', 'rate', -.0008, 'cold'), ('echo', 'rate', -.01, 'always')],
            effects=dict(
                sweep=[('leaves', 'mul', .1), ('obj.dirt', 'add', -.1)], scrub=[('obj.dirt', 'add', -.25)], mop=[('obj.wetness', 'add', -.3)], mend=[('obj.condition', 'add', .05)],
                tend=[('bloom', 'add', .15)], dust=[('obj.dirt', 'add', -.12), ('warm', 'add', -.02)], rest=[('need.energy', 'add', 2)], survey=[('need.fun', 'add', 2)],
                greet=[('need.social', 'add', 2)], scratch=[('obj.dirt', 'add', .03), ('echo', 'add', .1)], shout=[('echo', 'set', 1)], scuff=[('obj.dirt', 'add', .05), ('leaves', 'add', .05)],
                dive=[('leaves', 'mul', .5), ('obj.dirt', 'add', .05), ('need.fun', 'add', 2)], answer=[('echo', 'add', .3), ('obj.dirt', 'add', .01)],
                doze=[('need.energy', 'add', 3), ('warm', 'add', -.03)], bask=[('need.energy', 'add', 2), ('warm', 'add', -.05)], shed=[('puddle', 'mul', .3)],
                flap=[('leaves', 'mul', .4)], chip=[('frost', 'mul', .3)], splash=[('puddle', 'mul', .4), ('obj.wetness', 'add', .1)], listen=[('echo', 'add', .05), ('warm', 'add', .02)],
                stuck=[('frost', 'add', -.15), ('obj.condition', 'add', -.01)], argue=[('echo', 'mul', .2)], serenade=[('bloom', 'add', .1), ('echo', 'set', .5)],
                strut=[('need.fun', 'add', 3), ('leaves', 'mul', .9)], company=[('need.social', 'add', 2)], steady=[('obj.condition', 'add', .02), ('leaves', 'add', .05)], crack=[('obj.condition', 'add', -.04)], tip=[('leaves', 'add', .3)]),
            anchors=dict(floor_mid=P(53, 49), floor_front=P(40, 50), floor_left=P(36, 49), floor_right=P(70, 49), plinth_left=P(16, 50), plinth_right=P(87, 50),
                         rail_base_left=P(22, 48), rail_base_right=P(90, 48), lattice_left=P(24, 44), lattice_right=P(80, 44), lattice_edge_right=P(74, 44),
                         flower_left=P(15, 45), flower_right=P(86, 45), rim_left=P(24, 40), rim_right=P(80, 40), knob_left=P(15, 40), knob_right=P(85, 40),
                         post_foot_left=P(16, 39), post_foot_right=P(86, 39), rail_outer_left=P(10, 44), rail_outer_right=P(95, 44), rail_inner_right=P(88, 44)))
    # ---------------- care
    o.r('sweep_floor', 'Sweeping the floorboards clear of leaves with sideways wing strokes', 20, 'wing',
        [k(.12, 'floor_left', reach=.6, x=.3, y=.4, l=1), k(.3, 'floor_mid', reach=1, x=.4, y=.5, w=1, r=1), k(.5, 'floor_right', reach=1, x=.4, y=.5, w=1, l=1), k(.7, 'floor_mid', reach=1, x=.4, y=.5, w=1, r=1), k(.88, y=.1, eye='^')],
        [(.5, 'sweep')], g='care', when=['leaves>.3'], prefer=['grown'], say=["Swept it. Wind is already making a face about it.", "Clean floor. Four seconds. Enjoy."])
    o.r('scrub_lattice', 'Scrubbing the lattice with a wing, one diamond at a time', 20, 'wing',
        [k(.12, 'lattice_left', reach=.6, x=.3, y=.2), k(.3, 'flower_left', reach=1, x=.3, y=.2, w=.8, l=1), k(.5, 'lattice_left', reach=1, x=.3, y=.1, w=1, r=1), k(.7, 'rail_base_left', reach=1, x=.3, y=.5, w=.8, l=1), k(.88, eye='^')],
        [(.5, 'scrub')], g='care', prefer=['grumpy'])
    o.r('mop_wet_rim', 'Mopping the rain off the rim with his breast and a lot of grunting', 18, 'none',
        [k(.15, x=.3, y=-.2), k(.3, 'rim_left', x=.4, y=-.3, b=-.2, w=.2, mark='hnn'), k(.5, 'rim_left', x=.6, y=-.3, b=-.2, w=.4), k(.7, 'knob_left', x=.4, y=-.2, b=-.1, w=.3), k(.9, eye='-')],
        [(.5, 'mop')], g='care', ages=GROWN, when=['!wet'])
    o.r('hammer_slat', 'Hammering a loose lattice slat back into place with his bill', 16, 'none',
        [k(.12, y=.3, x=.5), k(.3, 'lattice_right', x=1.1, y=.6, b=.3, mark='tk'), k(.45, y=-.3, x=.3), k(.6, 'lattice_edge_right', x=1.1, y=.6, b=.3, mark='TK'), k(.8, y=.1, eye='^')],
        [(.6, 'mend')], g='care', say=["Slat's back. Don't lean on it. I will.", "Fixed. It'll fall off again. Job security."])
    o.r('prop_up_flowers', 'Propping the leaning flowers upright against the lattice', 20, 'wing',
        [k(.12, 'flower_left', reach=.7, x=.3, y=.3), k(.3, 'flower_left', reach=1, x=.4, y=.3, b=.2, w=.8), k(.55, 'flower_right', reach=1, x=.4, y=.3, b=.2, w=.8), k(.78, 'flower_right', reach=.6, x=.2, y=.1, w=.4, eye='^')],
        [(.55, 'tend')], g='care', when=['bloom<.8'], prefer=['happy'])
    o.r('dust_the_plinths', 'Dusting the stone feet at each end with a flick of the wing', 16, 'wing',
        [k(.12, 'plinth_left', reach=.7, x=.3, y=.7, b=.2), k(.3, 'plinth_left', reach=1, x=.3, y=.7, b=.2, w=.9, mark='fff'), k(.6, 'plinth_right', reach=1, x=.3, y=.7, b=.2, w=.9, mark='fff'), k(.8, y=.2, eye='-')],
        [(.6, 'dust')], g='care', prefer=['curious'])
    # ---------------- use
    o.r('step_up_and_sit', 'Stepping up into the gazebo and sitting where a seat would be', 24, 'none',
        [k(.12, 'floor_front', x=.3, y=.1, l=1), k(.3, 'floor_mid', x=.2, y=.3, b=.3, r=1), k(.55, 'floor_mid', x=0, y=.5, b=1, w=.3, eye='-'), k(.8, 'floor_mid', x=0, y=.6, b=1, eye='o')],
        [(.55, 'rest')], g='use', prefer=['tired', 'elder'], say=["Gazebo. Seat. Nobody put one. Typical.", "Sat on the floor. Floor's a seat if you believe."])
    o.r('survey_the_garden', 'Resting his wings on the rim and surveying the garden like a landlord', 22, 'wing',
        [k(.15, 'rim_left', reach=.6, x=.2, y=-.2), k(.35, 'rim_left', reach=1, x=.5, y=-.4, b=.2, w=.6, eye='>'), k(.6, 'rim_left', reach=1, x=.6, y=-.5, b=.2, w=.6, eye='-', mark='hm'), k(.85, 'rim_left', reach=.6, x=.4, y=-.3, eye='^')],
        [(.35, 'survey')], g='use', ages=GROWN, prefer=['grumpy'], say=["All mine. All rented. I'm sure the pond said something.", "Garden's fine. Staff are awful."])
    o.r('doorman_at_the_entry', 'Standing at the entry and nodding at everyone who is not there', 22, 'none',
        [k(.15, 'floor_front', y=-.2), k(.3, 'floor_front', x=.2, y=-.5, b=-.2, w=.2, eye='^', mark='evening'), k(.5, 'floor_front', x=.3, y=-.4, b=-.2, eye='o'), k(.7, 'floor_front', x=.2, y=-.5, b=-.2, w=.2, eye='^', mark='madam'), k(.88, y=-.1)],
        [(.3, 'greet')], g='use', when=['lonely'], say=["Welcome. Mind the floor. Mind me.", "Nobody came. The doorman has dignity."])
    o.r('back_scratch_on_post', 'Scratching his back up and down the post foot', 18, 'none',
        [k(.15, x=-.3, y=.1), k(.3, 'post_foot_left', x=-.4, y=.4, b=.5, w=.3), k(.5, 'post_foot_left', x=-.4, y=.4, b=1, w=.3, eye='^', mark='ahhh'), k(.7, 'post_foot_left', x=-.4, y=.2, b=.4, w=.2), k(.88, eye='-')],
        [(.5, 'scratch')], g='use', ages=GROWN, prefer=['happy'])
    o.r('pace_the_floor', 'Pacing the floor in a slow, serious circle with his wings behind him', 24, 'none',
        [k(.12, 'floor_left', x=.2, y=.3, b=.2, w=-.2, l=1), k(.3, 'floor_mid', x=.2, y=.3, b=.2, w=-.2, r=1), k(.5, 'floor_right', x=.2, y=.3, b=.2, w=-.2, l=1), k(.7, 'floor_mid', x=.2, y=.3, b=.2, w=-.2, r=1), k(.88, y=.1)],
        [(.5, 'scuff')], g='use', prefer=['grumpy', 'curious'])
    o.r('settle_on_plinth', 'Squatting on the plinth with his chin up like a garden ornament', 24, 'none',
        [k(.15, 'plinth_right', y=.1, b=.3), k(.35, 'plinth_right', y=-.3, b=.8, w=.2), k(.6, 'plinth_right', y=-.6, b=.9, eye='-'), k(.85, 'plinth_right', y=-.5, b=.9, eye='-')],
        [], g='use', prefer=['elder', 'happy'])
    # ---------------- play
    o.r('hide_behind_flowers', 'Ducking down behind the lattice flowers and popping up with a roar', 20, 'none',
        [k(.12, 'flower_right', y=.8, b=.9, eye='-'), k(.35, 'flower_right', y=1.1, b=1.1, eye='>'), k(.55, 'flower_right', y=-.5, b=-.7, w=1, eye='O', mark='RAAH'), k(.8, 'flower_right', y=0, w=.4, eye='^')],
        [(.55, 'scuff')], g='play', prefer=['young', 'happy'], obj=[(.55, dict(shake=.2))])
    o.r('leaf_pile_dive', 'Raking the leaves into a heap and diving in head first', 22, 'none',
        [k(.12, 'floor_left', x=.5, y=.6, b=.3, l=1), k(.3, 'floor_mid', x=.8, y=1, b=.5, r=1), k(.5, y=-.4, b=-.8, w=.8), k(.65, 'floor_mid', x=1.4, y=1.8, b=1.2, w=1, mark='FWUMP'), k(.88, y=.5, b=.3, eye='^')],
        [(.65, 'dive')], g='play', when=['leaves>.3'], prefer=['happy', 'young'], say=["Leaves. Dive. Regret nothing. Find leaf in ear.", "Leaf in my ear. Won't be taking questions."])
    o.r('rim_tightrope', 'Walking the lattice rim like a tightrope with his wings out', 22, 'none',
        [k(.12, 'rim_left', y=.2, b=.3, w=.8, l=1), k(.3, 'rim_left', x=.2, y=.2, b=.3, w=1, r=1), k(.5, 'knob_left', x=.2, y=.2, b=.2, w=1, l=1, eye='O'), k(.7, 'rim_left', x=.2, y=.2, b=.3, w=1, r=1), k(.88, y=0, w=.5, eye='^')],
        [(.5, 'scuff')], g='play', ages=GROWN, prefer=['happy'])
    o.r('spin_round_the_post', 'Spinning round the post by one wing until he cannot see straight', 20, 'wing',
        [k(.12, 'post_foot_left', reach=.7, x=.3, w=.5), k(.3, 'post_foot_left', reach=1, x=.4, b=-.2, w=1, l=1, mark='wheee'), k(.5, 'post_foot_left', reach=1, x=-.4, b=-.2, w=1, r=1, eye='@'), k(.7, 'post_foot_left', reach=1, x=.4, b=-.2, w=1, l=1, eye='@'), k(.88, y=.5, b=.5, eye='@')],
        [(.5, 'scuff')], g='play', ages=GROWN, prefer=['happy'])
    o.r('plinth_to_plinth_leaps', 'Leaping across the floor from one plinth to the other', 20, 'none',
        [k(.12, 'plinth_left', y=.3, b=.7), k(.28, y=-.6, b=-1, w=1), k(.45, 'floor_mid', y=.3, b=.6, l=1), k(.62, y=-.6, b=-1, w=1), k(.8, 'plinth_right', y=.3, b=.7, r=1), k(.92, eye='^')],
        [(.8, 'scuff')], g='play', prefer=['young'])
    o.r('chase_the_sun_patch', 'Chasing the sun patch across the boards with his bill and never quite catching it', 22, 'none',
        [k(.12, 'floor_front', x=1, y=1.2, b=.4), k(.3, 'floor_left', x=1.1, y=1.2, b=.3, l=1), k(.5, 'floor_mid', x=1.1, y=1.2, b=.3, r=1, eye='>'), k(.7, 'floor_right', x=1.2, y=1.4, b=.4, l=1), k(.88, y=.4, eye='-')],
        [(.5, 'scuff')], g='play', when=['sun', 'warm>.2'], prefer=['young', 'curious'])
    # ---------------- test
    o.r('sniff_the_flowers', 'Sniffing the flowers one after the other and rating them', 18, 'none',
        [k(.12, y=.4, x=.5), k(.3, 'flower_left', x=1, y=.5, b=.3, eye='O', mark='sniff'), k(.5, 'flower_right', x=1, y=.5, b=.3, eye='O', mark='sniff'), k(.7, y=.3, x=0, eye='-', mark='hm'), k(.88, eye='^')],
        [], g='test', when=['bloom>.3'], prefer=['curious'])
    o.r('rap_the_post', 'Rapping the post foot with his bill to hear how hollow it is', 16, 'none',
        [k(.12, y=-.2, x=.4), k(.3, 'post_foot_left', x=.9, y=-.3, mark='tok'), k(.5, 'post_foot_left', x=.9, y=-.3, mark='tonk'), k(.75, y=-.1, x=-.1, eye='-', mark='solid')],
        [], g='test', ages=GROWN, prefer=['curious'])
    o.r('tug_a_slat', 'Tugging a lattice slat with his bill to see if it comes loose', 16, 'none',
        [k(.12, y=.3, x=.4), k(.3, 'lattice_edge_right', x=.9, y=.5, b=.3), k(.5, 'lattice_edge_right', x=-.4, y=.4, b=.7, w=.4, mark='hnng'), k(.7, 'lattice_edge_right', x=.9, y=.5, b=.3, eye='-'), k(.88, eye='^')],
        [], g='test', say=["Tugged it. It tugged back. We're even.", "Slat held. I held a grudge."])
    o.r('time_the_echo', 'Snapping his bill shut and timing how long the roof takes to answer', 16, 'none',
        [k(.12, 'floor_left', y=.2, x=.3), k(.3, 'floor_left', x=.8, y=-.4, mark='CLAP'), k(.5, 'floor_left', x=-.1, y=-.3, eye='O', mark='...'), k(.7, 'floor_left', x=.2, y=-.2, eye='-', mark='1.4s')],
        [(.3, 'answer')], g='test', prefer=['curious'])
    o.r('count_the_diamonds', 'Counting the lattice diamonds from the edge to the flowers', 20, 'none',
        [k(.12, 'rail_outer_left', x=.5, y=.2, mark='1'), k(.3, 'lattice_left', x=.8, y=.2, mark='5'), k(.5, 'flower_left', x=.8, y=.2, mark='11'), k(.7, 'rail_base_left', x=.6, y=.5, mark='...nine?'), k(.88, y=.3, eye='-')],
        [], g='test', prefer=['curious'])
    o.r('stare_at_the_roof', 'Staring up at the roof until deciding it is a very long way up', 18, 'none',
        [k(.15, 'floor_mid', y=-.3), k(.4, 'floor_mid', x=-.4, y=-1.2, b=-.2, eye='O'), k(.65, 'floor_mid', x=-.6, y=-1.5, b=-.2, eye='O', mark='...'), k(.85, 'floor_mid', y=-.2, eye='-', mark='no')],
        [], g='test', prefer=['curious'])
    # ---------------- rest
    o.r('nap_on_the_floor', 'Flopping in the middle of the floor and sleeping like a dropped coat', 30, 'none',
        [k(.15, y=.4, b=.3), k(.35, 'floor_mid', y=1.4, b=1.2, w=.3), k(.6, 'floor_mid', y=1.6, b=1.4, eye='-', mark='z'), k(.85, 'floor_mid', y=1.6, b=1.4, eye='-', mark='zZ')],
        [(.6, 'doze')], g='rest', when=['tired'], say=["Nap. Gazebo. Roof does nothing, it's perfect.", "Gazebo nap. Roof does nothing, it's perfect."])
    o.r('bask_on_warm_boards', 'Pressing his belly flat on the sun-warmed boards', 28, 'none',
        [k(.15, y=.3), k(.35, 'floor_front', y=1.5, b=1.3, w=.7), k(.6, 'floor_front', y=1.6, b=1.4, w=.3, eye='-', mark='ahh'), k(.85, 'floor_front', y=1.6, b=1.4, w=.3, eye='-')],
        [(.6, 'bask')], g='rest', when=['sun', 'warm>.3'], prefer=['happy'])
    o.r('chin_on_the_plinth', 'Resting his chin on the plinth and watching the garden go by', 26, 'none',
        [k(.15, y=.2, b=.3), k(.35, 'plinth_left', x=.5, y=1, b=.9), k(.6, 'plinth_left', x=.6, y=1.1, b=1, eye='-', mark='...'), k(.85, 'plinth_left', x=.6, y=1.1, b=1, eye='-')],
        [], g='rest', prefer=['elder', 'sad'])
    o.r('sulk_against_the_rail', 'Sulking against the outer rail with his back to the gazebo', 24, 'none',
        [k(.15, x=-.2, y=.3), k(.35, 'rail_outer_right', x=-.5, y=.8, b=.6, eye='>'), k(.6, 'rail_outer_right', x=-.6, y=1, b=.8, eye='-', mark='hmph'), k(.85, 'rail_outer_right', x=-.6, y=1, b=.8, eye='-')],
        [], g='rest', when=['sad'], prefer=['grumpy'], say=["Sulking in a gazebo. Peak villain.", "Everything's fine. Nothing has ever been fine."])
    o.r('lie_under_the_roof_dusk', 'Lying on his back at dusk, counting the roof beams as they go dark', 30, 'none',
        [k(.15, y=.3), k(.35, 'floor_left', x=-.2, y=1.2, b=1.4, w=.3, eye='o'), k(.6, 'floor_right', x=-.4, y=1.3, b=1.5, eye='-', mark='...'), k(.85, 'floor_right', x=-.4, y=1.3, b=1.5, eye='-')],
        [], g='rest', when=['dusk', 'tired'], prefer=['sad'])
    o.r('sit_by_the_flowers', 'Sitting among the flowers, telling them about his day', 26, 'none',
        [k(.15, x=.1, y=.1), k(.35, 'flower_left', x=.4, y=.3, b=.7, eye='o'), k(.6, 'flower_left', x=.5, y=.2, b=.8, w=.4, eye='^', mark='...'), k(.85, 'flower_left', x=.5, y=.3, b=.8, eye='-')],
        [(.6, 'company')], g='rest', when=['lonely'], say=["They don't answer. They also don't judge. Best listeners.", "Told the flowers. They nodded. Wind did that."])
    # ---------------- weather
    o.r('push_out_the_puddle', 'Pushing the puddle off the boards with his whole belly', 20, 'none',
        [k(.12, y=.3, x=.4), k(.3, 'floor_left', x=.8, y=1, b=1, w=.2), k(.5, 'floor_mid', x=1, y=1.1, b=1.2, w=.3, eye='>', mark='shhh'), k(.7, 'floor_right', x=1, y=1.1, b=1.2), k(.88, y=.2, eye='-')],
        [(.5, 'shed')], g='weather', when=['puddle>.3'], prefer=['grumpy'])
    o.r('stomp_the_puddle', 'Stomping in the puddle by the entry until he is as wet as it is', 18, 'none',
        [k(.12, y=.3, x=.3), k(.3, 'floor_front', y=.5, b=.7, l=1, mark='splash'), k(.5, 'floor_front', y=.5, b=.8, r=1, mark='SPLOSH'), k(.7, 'floor_left', y=.5, b=.8, l=1, eye='O'), k(.88, eye='^')],
        [(.5, 'splash')], g='weather', when=['puddle>.4'], prefer=['happy', 'young'], say=["Puddle. Mine. Don't tell anyone how wet I am.", "Soaked, delighted, unrepentant."])
    o.r('flap_the_leaves_out', 'Flapping the wind-blown leaves back out between the posts', 22, 'wing',
        [k(.12, 'floor_left', reach=.7, x=.3, y=.3, w=.5), k(.3, 'floor_mid', reach=1, x=.4, y=.2, w=1, mark='fwap'), k(.5, 'floor_right', reach=1, x=.4, y=.2, w=1, r=1, mark='FWAP'), k(.7, 'floor_mid', reach=1, x=.4, y=.2, w=1, l=1, eye='>'), k(.88, eye='-', mark='...')],
        [(.5, 'flap')], g='weather', when=['windy', 'leaves>.4'], prefer=['grumpy'], obj=[(.5, dict(puff=.5))])
    o.r('chip_the_frost_rim', 'Chipping the frost off the lattice rim with the tip of his bill', 22, 'none',
        [k(.12, y=.3, x=.5), k(.3, 'rim_left', x=1, y=-.2, b=-.2, mark='tik'), k(.5, 'rim_left', x=1, y=-.2, b=-.2, w=.3, mark='TIK'), k(.7, 'knob_left', x=1, y=-.2, b=-.2, mark='tik'), k(.88, eye='-', mark='brr')],
        [(.5, 'chip')], g='weather', when=['cold', 'frost>.3'], ages=GROWN)
    o.r('listen_to_the_roof', 'Standing dead centre with his bill up, listening to the rain hammer the roof', 26, 'none',
        [k(.15, 'floor_mid', y=-.2), k(.4, 'floor_mid', x=-.2, y=-.7, b=-.1, eye='O'), k(.65, 'floor_mid', x=-.2, y=-.8, b=-.1, eye='-', mark='drum'), k(.85, 'floor_mid', y=-.3, eye='^')],
        [(.4, 'listen')], g='weather', when=['wet', 'puddle<.7'])
    o.r('shield_flowers_from_gale', 'Spreading both wings round the flowers to shield them from the gale', 22, 'wing',
        [k(.12, 'flower_left', reach=.6, x=.2, y=.4, w=.5), k(.3, 'flower_left', reach=1, x=.3, y=.5, b=.4, w=1, eye='>'), k(.55, 'flower_left', reach=1, x=.2, y=.6, b=.6, w=1, eye='@', mark='nnh'), k(.8, 'flower_left', reach=.6, x=.1, y=.3, eye='-')],
        [(.55, 'tend')], g='weather', when=['windy', 'bloom>.3'], ages=GROWN, prefer=['happy'])
    o.r('hide_behind_post_in_the_wind', 'Hugging the post foot while the wind howls through the open sides', 24, 'none',
        [k(.15, 'post_foot_left', x=.3, y=.2, b=.3), k(.35, 'post_foot_left', x=-.3, y=.6, b=.7, w=.8, eye='>'), k(.6, 'post_foot_left', x=-.3, y=.7, b=.8, w=.9, eye='@', mark='WHOOO'), k(.85, 'post_foot_left', x=-.2, y=.4, b=.4, eye='-')],
        [(.6, 'steady')], g='weather', when=['windy'], ages=GROWN)
    # ---------------- show
    o.r('sing_up_at_the_roof', 'Singing up at the roof and letting the echo carry it', 22, 'none',
        [k(.12, 'floor_mid', y=-.3, b=-.1), k(.3, 'floor_mid', x=-.3, y=-1.2, b=-.3, w=.6, mark='HOOOONK'), k(.5, 'floor_mid', x=-.3, y=-1.3, b=-.3, w=1, eye='O', mark='HONK'), k(.75, 'floor_mid', y=-.5, eye='^')],
        [(.3, 'shout')], g='show', prefer=['happy'], say=["Heard that, roof? Say it back.", "Fine acoustics. Terrible audience."])
    o.r('grand_entrance_strut', 'Strutting up through the entry with his wings back like a bride on a bad day', 22, 'none',
        [k(.12, 'floor_front', x=.2, y=-.5, b=-.3, w=.4, l=1), k(.3, 'floor_left', x=.2, y=-.5, b=-.3, w=.6, r=1), k(.5, 'floor_mid', x=.2, y=-.6, b=-.3, w=.7, l=1, eye='^'), k(.75, 'floor_mid', x=.1, y=-.5, b=-.2, w=1, eye='^'), k(.9, y=0)],
        [(.5, 'strut')], g='show', prefer=['happy'], say=["Applause, please. Wings only. I'm not made of money.", "Nobody clapped. I took it as awe."])
    o.r('serenade_the_blooms', 'Crooning at the flowers until they lean his way', 24, 'none',
        [k(.12, 'floor_left', y=-.2, b=.2, w=.2), k(.3, 'flower_left', x=.5, y=-.4, b=-.1, w=.6, eye='^', mark='la'), k(.55, 'flower_left', x=.5, y=-.5, b=-.1, w=.8, eye='-', mark='LAAA'), k(.8, 'flower_right', x=.4, y=-.3, w=.4, eye='o')],
        [(.55, 'serenade')], g='show', when=['bloom<.9'], prefer=['happy'])
    o.r('argue_with_the_echo', 'Arguing with his own echo and losing every round', 22, 'none',
        [k(.12, 'floor_mid', x=.2, y=-.4), k(.3, 'floor_mid', x=.4, y=-.9, b=-.2, w=.5, mark='SHUT IT'), k(.5, 'floor_mid', x=-.2, y=-.4, eye='>', mark='...'), k(.7, 'floor_mid', x=.5, y=-1, b=-.2, w=1, eye='@', mark='YOU SHUT IT'), k(.9, y=0, eye='-')],
        [(.5, 'argue')], g='show', when=['echo>.3'], prefer=['grumpy'], say=["Didn't say that. Said that last. Shut up.", "Echo's winning on points. Nobody check."])
    o.r('speech_from_the_rim', 'Delivering a speech on the history of gazebos from the rim', 26, 'none',
        [k(.15, 'rim_right', y=-.2, b=.2, w=.4), k(.35, 'rim_right', x=.3, y=-.7, b=-.1, w=.9, mark='FRIENDS'), k(.55, 'knob_right', x=.3, y=-.7, b=-.1, w=1, mark='GAZEBOS'), k(.8, 'rim_right', x=.2, y=-.4, w=.6, eye='^', mark='thanks')],
        [(.35, 'shout')], g='show', ages=GROWN, say=["Thank you. Questions? Roof. Bad. Lovely.", "Standing ovation from a fence post."])
    o.r('pose_at_the_rail', 'Posing at the outer rail with one wing on the lattice like a magazine cover', 18, 'none',
        [k(.15, y=-.1, x=.2), k(.4, 'rail_outer_left', x=.5, y=-.4, w=.7, eye='^'), k(.6, 'rail_outer_left', x=.5, y=-.5, w=.9, eye='-', mark='click'), k(.85, y=0, eye='o')],
        [], g='show', prefer=['happy'])
    # ---------------- mishap
    o.r('trip_on_plinth', 'Tripping over the plinth and landing face first in the lattice', 18, 'none',
        [k(.15, 'plinth_left', x=.4, y=.2, l=1), k(.3, x=1, y=.7, b=-.4, w=.8, eye='O', mark='WHOA'), k(.5, 'lattice_left', x=1.5, y=1, b=.8, w=1, mark='CRUNCH'), k(.75, 'lattice_left', y=.9, b=.6, eye='@'), k(.9, eye='-')],
        [(.5, 'crack')], g='mishap', prefer=['young'], say=["Lattice: bent. Dignity: also bent.", "I'm fine. The lattice isn't. Not my fault."])
    o.r('head_through_the_lattice', 'Pushing his head through a lattice diamond and having to be a very long duck to get out', 22, 'none',
        [k(.12, x=.5, eye='>'), k(.3, 'lattice_right', x=1.2, y=.4, b=.5, mark='squeeze'), k(.5, 'lattice_right', x=1.4, y=.4, b=.9, w=.5, l=1, eye='@', mark='mmmf'), k(.7, 'lattice_right', x=1.4, y=.4, b=1, w=1, r=1, mark='POP'), k(.88, x=1.6, y=.9, b=.6, eye='-')],
        [(.7, 'crack')], g='mishap', ages=YOUNG + ['juvenile'], prefer=['curious'], say=["Head in. Head stuck. Head out. All fine.", "Head stuck. Head out. Head fine. I'm fine."])
    o.r('skid_on_the_leaves', 'Skidding on the damp leaves and ending on his back in the entry', 18, 'none',
        [k(.15, 'floor_front', x=.5, l=1), k(.3, 'floor_front', x=1.1, y=.5, b=-.5, w=1, eye='O', mark='WHOA'), k(.5, 'floor_front', x=1.5, y=1.6, b=1.3, w=.4, mark='THUD'), k(.75, 'floor_front', y=1.4, b=1.1, eye='@'), k(.9, y=.5, eye='-')],
        [(.5, 'tip')], g='mishap', when=['leaves>.4'], say=["Leaves. Floor. Face. The usual.", "Fell on my arse. Nobody saw. Possibly saw."])
    o.r('bill_stuck_to_the_frost', 'Licking the frosty rim for a dare and finding his bill stuck there', 24, 'none',
        [k(.12, y=.2, x=.4), k(.3, 'rim_right', x=1, y=-.3, b=-.2, eye='O', mark='lick'), k(.5, 'rim_right', x=1, y=-.3, b=-.2, w=.5, eye='@', mark='mmf'), k(.7, 'rim_right', x=-.4, y=-.3, b=.2, w=1, l=1, mark='RIP'), k(.88, y=.4, eye='-', mark='ow')],
        [(.5, 'stuck')], g='mishap', ages=GROWN, when=['cold', 'frost>.4'], say=["Don't lick the frost. Noted. Too late.", "It said 'dare me'. It lied."])
    o.r('miss_the_jump_to_rim', 'Jumping for the rim, missing, and bouncing off the plinth', 18, 'none',
        [k(.12, y=.4, b=.8), k(.3, y=-1, b=-1.2, w=1, eye='>'), k(.45, 'rim_left', x=.6, y=-.6, b=-.8, w=1, mark='nngh'), k(.6, 'plinth_left', y=1, b=1.2, w=.4, eye='@', mark='BONK'), k(.88, y=.4, eye='-')],
        [(.6, 'scuff')], g='mishap', ages=GROWN, prefer=['grumpy'])
    return o


def main():
    which = sys.argv[1:] or ['toy_sandbox', 'dog_house', 'toy_car', 'gazebo']
    for n, f in (('toy_sandbox', sandbox), ('dog_house', dog_house), ('toy_car', toy_car), ('gazebo', gazebo)):
        if n in which:
            f().emit()


if __name__ == '__main__':
    main()
