"""Wave 1a v2 repertoire: birdhouse, tire_swing, toy_seesaw, rubber_duck. Every routine is hand-written under the v2 rules."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN

# ============================================================ birdhouse
# A box on a pole. Drawn parts (rep.py birdhouse): pole (12-76 px, walls at both edges), foot slab (6 px), the box floor
# rim (87), its underside edge (82), the front ledge (93), the doorway panel above it, two plates (117) and the roof.
o = Obj('birdhouse', 'placed',
        fields=dict(footing=(1, 0, 1)),
        physics=[('footing', 'rate', -.0004, 'wet'), ('footing', 'rate', -.0002, 'windy')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrub=[('obj.dirt', 'add', -.25)], dust=[('obj.dirt', 'add', -.2)],
            tamp=[('footing', 'set', 1)], dig=[('footing', 'add', -.3)], dry=[('obj.wetness', 'add', -.4)],
            clean_bill=[('need.cleanliness', 'add', 1)], maypole=[('need.fun', 'add', 2)]),
        anchors=dict(pole_high=(.492, .811), pole_high_r=(.557, .811), pole_mid=(.508, .868), pole_mid_r=(.557, .868),
                     pole_low=(.508, .925), pole_low_r=(.557, .925),
                     foot_l=(.41, .981, 'surface'), foot_mid=(.459, .981, 'surface'), foot_r=(.508, .981, 'surface'),
                     floor_rim=(.23, .717), under_edge=(.508, .736), ledge=(.41, .698), plate_l=(.262, .623)))
# --- care
o.r('wipe_pole', "Wiping the pole with a wing, from the foot up as high as he can reach", 16, 'wing',
    [k(.15, 'pole_low', reach=.6, x=.3), k(.35, 'pole_low', reach=1, x=.4, y=.2, mark='fff'), k(.55, 'pole_mid', reach=1, x=.4, y=-.2, mark='fff'), k(.78, 'pole_high', reach=1, x=.5, y=-.7, mark='fff'), k(.9, eye='^')],
    [(.78, 'wipe')], g='care', act=('wipe', 'pole'), when=['obj_dirt>.3'],
    say=["Pole's clean. The house won't notice. I'll know.", "Grime's on my wing now. It travels."])

o.r('scrub_foot_slab', "Scrubbing the foot slab clean with his bill, from one end to the other", 16, 'none',
    [k(.2, 'foot_l', x=.9, y=.8, b=.5), k(.4, 'foot_l', x=1.2, y=1, b=.6, mark='skrt'), k(.6, 'foot_mid', x=1.2, y=1.1, b=.6, mark='skrt'), k(.8, 'foot_r', x=1.2, y=1, b=.6, mark='skrt'), k(.92, y=.2, eye='^')],
    [(.8, 'scrub')], g='care', act=('scrub', 'foot'), when=['obj_dirt>.3'])
o.r('dust_floor_with_a_twig', "Dusting the floor rim and the edge below it with a twig held at full stretch", 20, 'twig',
    [k(.15, 'floor_rim', reach=.7, y=-.4), k(.4, 'floor_rim', reach=1, x=.4, y=-.7, mark='fff'), k(.65, 'under_edge', reach=1, x=.5, y=-.7, mark='fff'), k(.85, y=-.2, eye='^')],
    [(.65, 'dust')], g='care', act=('sweep', 'floor_rim'), when=['obj_dirt>.3'])
o.r('stamp_soil_flat', "Stamping the soil round the pole's foot flat, left foot then right, left side then right", 16, 'none',
    [k(.2, 'foot_l', y=.4, l=1), k(.4, 'foot_l', y=.7, b=.4, r=1, mark='thud'), k(.6, 'foot_r', y=.7, b=.4, l=1, mark='thud'), k(.8, 'foot_r', y=.7, b=.4, r=1, mark='thud'), k(.92, eye='^')],
    [(.6, 'tamp')], g='weather', act=('stamp', 'soil'), when=['footing<.7'], prefer=['grown', 'wet'],
    say=["Stamped it down. Soil can't say I didn't try.", "Pole's snug again. Nobody's grateful. Standard."])
o.r('scrape_bill_clean', "Scraping his bill clean along the pole's edge, left side then right", 14, 'none',
    [k(.2, 'pole_mid', x=.8, y=.3), k(.4, 'pole_mid', x=1.1, y=.5, b=.2, mark='skrk'), k(.6, 'pole_mid_r', x=1.1, y=.5, b=.2, mark='skrk'), k(.85, y=-.2, eye='^')],
    [(.6, 'clean_bill')], g='care', act=('scrape', 'pole_edge'))
# --- use
o.r('knock_like_a_door', "Knocking three times at the pole like a front door, then cocking his head to wait", 16, 'none',
    [k(.2, 'pole_high', x=.6, y=.2), k(.32, 'pole_high', x=1.1, y=.3, mark='tok'), k(.44, 'pole_high', x=.6, y=.2), k(.56, 'pole_high', x=1.1, y=.3, mark='tok'), k(.68, 'pole_high', x=.6, y=.2, mark='tok'), k(.85, x=-.4, y=-.8, eye='o', mark='...')],
    [], g='use', act=('knock', 'pole'),
    say=["Three knocks. Polite. Can't say I didn't try.", "Either empty or ignoring a duck. Even odds."])

o.r('peer_up_at_the_doorway', "Rocking back on his heels, one wing against the pole, to peer up at the doorway for any sign of life", 16, 'wing',
    [k(.2, 'pole_mid_r', reach=.5, x=-1.2, y=-1.6, b=.6, eye='o'), k(.45, 'pole_mid_r', reach=.8, x=-1.5, y=-2, b=1.2, eye='O', mark='hm'), k(.7, 'pole_mid_r', reach=.8, x=-1.2, y=-1.6, b=.6, eye='o'), k(.88, x=0, y=0, eye='-')],
    [], g='use', act=('peer', 'doorway'), prefer=['curious'])
o.r('shout_up_the_doorway', "Gripping the pole with one wing and shouting up at the doorway to ask whether anyone is home", 14, 'wing',
    [k(.2, 'pole_high', reach=.6, x=-1.2, y=-1.6), k(.4, 'pole_high', reach=1, x=-1.5, y=-2, b=.8, eye='O', mark='HELLO'), k(.62, 'pole_high', reach=1, x=-1.5, y=-2, b=1.2, mark='ANYONE'), k(.85, x=0, y=.6, eye='-', mark='...')],
    [], g='use', act=('shout', 'doorway'), prefer=['lonely'],
    say=["Hello. It's a duck, not a bailiff.", "The roof echoed. The roof sounds smug."])

o.r('stand_guard_at_the_pole', "Standing guard at the pole with a wing raised to his brow, scanning the yard", 20, 'wing',
    [k(.2, 'pole_low_r', reach=.3, y=-.3), k(.4, 'pole_low_r', reach=1, x=.3, y=-.7, eye='>', mark='hm'), k(.62, 'pole_low_r', reach=1, x=-.2, y=-.7, eye='o'), k(.82, 'pole_low_r', reach=.4, x=.4, y=-.4, eye='>')],
    [], g='use', act=('guard', 'pole'), prefer=['grumpy'])
o.r('prod_the_ledge', "Reaching a twig up to the front ledge and prodding along it to feel for anything left there", 20, 'twig',
    [k(.15, 'ledge', reach=.6, y=-.5), k(.4, 'ledge', reach=1, x=.5, y=-.8, mark='tk'), k(.62, 'ledge', reach=1, x=.5, y=-.8, b=.2, mark='tk'), k(.82, x=0, y=-.4, eye='-', mark='nope')],
    [], g='use', act=('prod', 'ledge'),
    say=["Ledge is empty. I checked with a stick, like a professional.", "If a twig says no one's home, that's legally binding."])

o.r('tap_plate_hollow', "Tapping the left plate twice with his bill to hear whether it rings hollow", 14, 'none',
    [k(.2, 'plate_l', x=.8, y=-.3, b=-.3), k(.4, 'plate_l', x=1.2, y=-.2, b=-.2, mark='tok'), k(.6, 'plate_l', x=.8, y=-.3, b=-.3), k(.78, 'plate_l', x=1.2, y=-.2, b=-.2, mark='tok'), k(.9, eye='o')],
    [], g='use', act=('tap', 'plate'), prefer=['curious'])
# --- play
o.r('race_the_pole', "Sprinting at the pole and slapping it with a wing as he swerves away", 14, 'wing',
    [k(.2, x=-.8, b=.5, eye='>'), k(.4, 'pole_mid', reach=1, x=.9, b=-.5, mark='SLAP'), k(.6, x=-.9, b=-.4, l=1, eye='>'), k(.85, x=0, eye='^')],
    [], g='play', act=('race', 'pole'), prefer=['happy', 'young'])
o.r('peek_round_the_pole', "Peeking round the pole's left edge, then its right, ducking back each time", 20, 'none',
    [k(.2, 'pole_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'pole_mid', x=1.4, y=0, eye='O', mark='!'), k(.6, 'pole_mid_r', x=-1.2, y=.8, b=.6, eye='o'), k(.82, 'pole_mid_r', x=1.4, y=0, eye='O', mark='boo')],
    [], g='play', act=('hide', 'pole'), prefer=['happy', 'young'],
    say=["The pole kept dead still. Poor sport.", "Peek one. Peek two. The tension was all mine."])

o.r('maypole_spin', "Hooking a wing round the pole and swinging himself round and round like a maypole", 18, 'wing',
    [k(.15, 'pole_mid', reach=.6, x=.3), k(.35, 'pole_mid', reach=1, x=.5, b=-.4, l=1, mark='wheee'), k(.55, 'pole_mid_r', reach=1, x=.5, b=-.4, r=1, eye='@'), k(.78, 'pole_mid', reach=.5, x=.2, y=.4, eye='O')],
    [(.55, 'maypole')], g='play', act=('spin', 'pole'), prefer=['happy'],
    say=["Round the pole, wing hooked, no ribbons. Budget cuts.", "Dizzy. Delighted. Both the pole's fault."])

o.r('hop_on_the_slab', "Hopping onto the foot slab and off again three times, a bit higher each hop", 18, 'none',
    [k(.15, 'foot_mid', perch=1, b=-.4), k(.3, 'foot_mid', b=.3), k(.45, 'foot_mid', perch=1, b=-.8, w=.5, mark='hup'), k(.6, 'foot_mid', b=.4), k(.78, 'foot_mid', perch=1, b=-1.2, w=1, eye='^', mark='HUP'), k(.92, b=.3)],
    [], g='play', act=('hop', 'foot'), prefer=['happy', 'young'])
o.r('chase_his_tail_round_the_pole', "Chasing his own tail in tight circles at the pole's foot until the yard spins", 16, 'none',
    [k(.2, x=-.6, b=.3, eye='o'), k(.4, x=.9, y=.4, l=1, eye='@'), k(.6, x=-.9, y=.5, r=1, eye='@', mark='grr'), k(.8, x=.5, y=.8, b=.7, eye='O')],
    [], g='play', act=('chase', 'tail'), prefer=['young'],
    say=["Caught it. Didn't know what to do. Same as every chase.", "Dizzy, dignified. Pick one."])

# --- test
o.r('sniff_up_the_pole', "Sniffing up the pole inch by inch for a trace of whoever lives up there", 18, 'none',
    [k(.2, 'pole_low', x=.5, y=.5, b=.3), k(.4, 'pole_low', x=.9, y=.9, b=.2, eye='o', mark='snf'), k(.6, 'pole_mid', x=.9, y=.3, mark='snf'), k(.8, 'pole_high', x=.9, y=-.3, eye='O', mark='snf')],
    [], g='test', act=('sniff', 'pole'), prefer=['curious'])
o.r('measure_himself_against_the_pole', "Standing tall at the pole and laying a wing flat from his crown to the wood to mark his height", 20, 'wing',
    [k(.15, 'pole_mid_r', reach=.4, x=-.4), k(.4, 'pole_high_r', reach=1, x=-.3, y=-.4, eye='^'), k(.6, 'pole_high_r', reach=1, x=-.3, y=-.5, b=.2, mark='this much'), k(.85, 'pole_mid_r', reach=.4, y=0, eye='-')],
    [], g='test', act=('measure', 'height'), prefer=['curious', 'young'],
    say=["Same mark as last time. No growth. Bread, please.", "Marked my height on a pole. It's something."])

o.r('dig_beside_the_slab', "Digging beside the foot slab with his bill to find out how deep the pole goes", 18, 'none',
    [k(.2, 'foot_l', x=.8, y=1, b=.5), k(.4, 'foot_l', x=1.3, y=1.4, b=.7, mark='scrf'), k(.6, 'foot_l', x=1.3, y=1.5, b=.8, l=1, mark='scrf'), k(.82, 'foot_l', x=.4, y=.6, b=.3, eye='o')],
    [(.6, 'dig')], g='test', act=('dig', 'soil'), prefer=['curious'],
    say=["Dug a bit. The soil went deeper than I wanted to follow.", "A hole's just soil changing its mind."])

o.r('ear_to_the_pole', "Resting his ear against the pole and listening up it for any shuffling from the box", 22, 'none',
    [k(.2, 'pole_high_r', x=.4, y=.6), k(.4, 'pole_high_r', x=-1.2, y=1.6, b=.6, eye='-', mark='...'), k(.7, 'pole_high', x=-1.2, y=1.6, b=1.2, eye='o', mark='...'), k(.88, x=0, y=0, eye='-')],
    [], g='test', act=('listen', 'pole'), prefer=['curious', 'lonely'])
# --- rest
o.r('wait_for_a_tenant', "Waiting by the pole for someone to turn up, shifting from foot to foot", 24, 'none',
    [k(.2, 'pole_mid_r', x=.2, y=-.2), k(.4, 'pole_mid_r', x=.2, y=-.4, l=1, eye='o'), k(.6, 'pole_mid_r', x=.2, y=-.4, r=1, eye='o', mark='...'), k(.8, 'pole_mid_r', x=.4, y=-.5, eye='>')],
    [], g='rest', act=('wait', 'pole'), when=['lonely'],
    say=["Still no tenant. Either the rent's off or the pole is.", "I'm not waiting. I'm standing here. Neutrally."])

o.r('lean_on_the_pole', "Leaning his chest against the pole with his chin on its edge and his eyes half shut", 22, 'none',
    [k(.2, 'pole_mid', x=.4, y=.2, b=.2), k(.4, 'pole_mid', x=.9, y=.7, b=.5, eye='-'), k(.7, 'pole_mid', x=1.4, y=1.2, b=1, eye='-', mark='mm'), k(.9, y=0, b=.2, eye='^')],
    [], g='rest', act=('lean', 'pole'), prefer=['tired'])
o.r('warm_up_on_the_slab', "Sitting up on the foot slab in a patch of sun with his wings open and his eyes shut", 26, 'none',
    [k(.2, 'foot_l', perch=1, b=.4, w=.4), k(.4, 'foot_l', perch=1, b=.9, w=1, eye='-'), k(.7, 'foot_l', perch=1, b=.9, w=1, eye='-', mark='ahh'), k(.9, 'foot_l', perch=1, b=.2, eye='^')],
    [], g='rest', act=('warm', 'foot'), when=['sun', 'warm'])
# --- weather
o.r('rub_the_wet_pole_dry', "Rubbing the damp pole dry with his chest feathers, one side then the other", 18, 'none',
    [k(.2, 'pole_mid', x=-.2, y=.6, b=.6), k(.4, 'pole_mid', x=-1.2, y=.6, b=.6, w=.6, mark='fff'), k(.62, 'pole_mid_r', x=-1.2, y=.6, b=.6, w=1, mark='fff'), k(.85, y=0, eye='^')],
    [(.62, 'dry')], g='weather', act=('dry', 'pole'), when=['obj_wetness>.3'],
    say=["Dried it with my chest. My feathers have gone mournful.", "Dry pole, damp duck. Fair trade, by somebody's maths."])

o.r('follow_a_raindrop_down', "Following a bead of rain down the pole with his bill, high to low, then starting over", 20, 'none',
    [k(.2, 'pole_high', x=.6, y=-.3, eye='o'), k(.38, 'pole_mid', x=.8, y=.1, eye='o'), k(.55, 'pole_low', x=1, y=.6, b=.3, eye='O'), k(.7, 'pole_high', x=.6, y=-.3, eye='o'), k(.88, 'pole_mid', x=.8, y=.1)],
    [], g='weather', act=('chase', 'bead'), when=['obj_wetness>.3'], prefer=['curious'],
    say=["Raced a raindrop. Lost. It had gravity.", "It reached the bottom first and had the decency to vanish."])

# --- show
o.r('doorman_stance', "Standing stiff at the pole's foot like the house's doorman, chin high, one wing across his chest", 18, 'wing',
    [k(.2, 'pole_low', reach=.4, y=-.5, x=-.2), k(.45, 'pole_low', reach=.9, y=-1, x=-.3, eye='^'), k(.75, 'pole_low', reach=.9, y=-1, x=-.3, b=.2, eye='-', mark='sir'), k(.9, reach=.2, eye='^')],
    [], g='show', act=('pose', 'doorway'), prefer=['happy', 'grown'],
    say=["Doorman. Employer's out. Pay's atrocious.", "Anyone gets past me, I'll look at them hard."])

o.r('tap_dance_on_the_slab', "Tap-dancing on the foot slab with his wings out and his chin up", 18, 'none',
    [k(.2, 'foot_l', perch=1, l=1, w=.6), k(.4, 'foot_mid', perch=1, r=1, w=1, y=-.4), k(.6, 'foot_mid', perch=1, l=1, w=1, y=-.4, b=-.3, mark='tk'), k(.8, 'foot_r', perch=1, r=1, w=.6, b=.3, mark='tk'), k(.92, eye='^')],
    [], g='show', act=('dance', 'foot'), prefer=['happy'])

# --- mishap
o.r('act_out_a_birds_arrival', "Acting out a bird coming home: a run-up, a flapping landing on the foot slab, a proud fold of the wings", 20, 'none',
    [k(.12, x=-1.6, b=.8, eye='>'), k(.3, 'foot_r', perch=1, w=1, y=-1.8, b=-1.6, mark='fwp fwp'), k(.5, 'foot_mid', perch=1, w=.6, b=.6), k(.72, 'foot_mid', perch=1, w=0, y=-.6, b=1, eye='^', mark='home'), k(.9, 'foot_mid', perch=1, eye='^')],
    [], g='show', act=('show', 'arrival'), prefer=['happy', 'young'],
    say=["That's how a bird does it. Landing: seven. Dismount: wet.", "Practising for when I'm allowed in."])
o.r('crow_at_dawn', "Crowing at the dawn from the foot slab with his chest out, as if the whole house were his", 18, 'none',
    [k(.2, 'foot_mid', perch=1, b=.6), k(.4, 'foot_mid', perch=1, y=-1.8, x=-1.4, w=1, eye='^', mark='COCK-A-'), k(.62, 'foot_l', perch=1, y=-2, x=-1.8, w=1, mark='DOODLE'), k(.85, 'foot_l', perch=1, eye='^')],
    [], g='show', act=('shout', 'dawn'), when=['dawn'], prefer=['happy'],
    say=["I'm a duck. The noise is the same as long as you commit.", "Sunrise has been told. It can go on now."])
o.r('fit_wings_to_the_doorway', "Stretching his wings out along the foot slab to see whether he would fit through the doorway above, tip to tip", 18, 'none',
    [k(.2, 'foot_r', perch=1, w=.6, y=-.6), k(.4, 'foot_r', perch=1, w=1, y=-1.8, x=-1.2, eye='o'), k(.65, 'foot_l', perch=1, w=1, y=-1.8, x=-1.2, eye='O', mark='hm'), k(.85, 'foot_l', perch=1, w=.4, eye='-', mark='no')],
    [], g='test', act=('fit', 'doorway'), prefer=['curious'])
o.r('squint_along_the_pole', "Squinting up along the pole with one eye shut to check that it stands true", 16, 'none',
    [k(.2, 'pole_low_r', x=.6, y=.6, eye='-'), k(.45, 'pole_low_r', x=-1.2, y=-1.8, b=.6, eye='-'), k(.7, 'pole_low_r', x=-1.2, y=-2, b=1, eye='o', mark='...'), k(.88, x=0, eye='-')],
    [], g='test', act=('peer', 'pole'), prefer=['curious', 'grown'])
o.r('rap_the_slab_ends', "Rapping the left end of the foot slab and then its middle to hear whether they ring alike", 16, 'none',
    [k(.2, 'foot_l', x=.8, y=1, b=.6), k(.35, 'foot_l', x=1.4, y=1.4, b=.8, mark='tk'), k(.55, 'foot_mid', x=1.4, y=1.4, b=.8, mark='tk'), k(.75, x=-1.2, y=-1.8, eye='o', mark='...'), k(.9, eye='-')],
    [], g='test', act=('tap', 'slab'), prefer=['curious'])
o.r('stakeout_from_the_slab', "Sitting up on the foot slab with his eyes on the doorway, keeping a bird-watcher's patient watch", 28, 'none',
    [k(.2, 'foot_r', perch=1, b=.6, x=-.4), k(.4, 'foot_r', perch=1, b=1, x=-1.4, y=-1.8, eye='o'), k(.7, 'foot_r', perch=1, b=1, x=-1.8, y=-1.8, eye='o', mark='...'), k(.9, 'foot_r', perch=1, b=.4, eye='-')],
    [], g='rest', act=('perch', 'foot'), prefer=['curious', 'lonely'],
    say=["Sat for an hour. Saw a leaf. It was brilliant.", "If anyone moves in, I've got dibs on the ledge."])
o.r('flap_at_the_pole', "Flapping flat out with his bill against the pole, trying to lift himself up to the doorway and getting an inch", 16, 'none',
    [k(.2, 'pole_low', x=.6, y=.6, w=.4), k(.4, 'pole_low', x=1.4, y=1.8, b=-1.6, w=1, l=1, r=1, mark='fwp'), k(.6, 'pole_low', x=1.4, y=1.8, b=-2, w=1, l=1, r=1, mark='FWP'), k(.8, 'pole_low', x=.6, y=.6, b=.6, w=.4, eye='-')],
    [], g='play', act=('hop', 'pole'), prefer=['young', 'curious'],
    say=["An inch up. Personal best. Gravity says nice try.", "Wings work. The rest of me is on a different contract."])

o.r('toppled_looking_at_the_roof', "Rearing back with a wing against the pole to see the roofline, and rearing too far onto his tail", 18, 'wing',
    [k(.2, 'pole_high_r', reach=.6, x=-1.2, y=-1.8, b=.6, eye='o'), k(.4, 'pole_high_r', reach=1, x=-1.8, y=-2, b=1.2, eye='O'), k(.6, x=-2.4, y=-2, b=2, w=.5, eye='@', mark='whoa'), k(.82, y=.6, b=1.6, eye='-', mark='...')],
    [], g='mishap', act=('peer', 'roofline'), prefer=['young', 'curious'],
    say=["The roof's fine. I'm horizontal. Thanks for asking.", "Looked up too hard. The pole watched me fall. No comment."])
o.r('twig_whacks_back', "Jabbing at the floor's edge so hard that the twig skids off and whacks him between the eyes", 16, 'twig',
    [k(.15, 'under_edge', reach=.6, y=-.6, x=.3), k(.4, 'under_edge', reach=1, x=1.2, y=-1.8, b=.6, mark='JAB'), k(.6, x=-1.2, y=1.8, b=1.2, eye='@', mark='tonk'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('knock', 'twig'), prefer=['grumpy'],
    say=["Hit myself with my own stick. Elegance, check.", "The edge won. The edge didn't even do anything."])
o.r('missed_the_ledge_jump', "Jumping up at the front ledge, missing it, and smacking his chest against the pole", 16, 'none',
    [k(.2, x=-1.4, b=.8, eye='>'), k(.4, x=.4, b=-2, w=1, y=-.6, mark='HUP'), k(.58, 'pole_high_r', x=1.6, y=.4, b=-.4, eye='O', mark='thump'), k(.82, x=-.6, y=.6, b=.8, eye='@')],
    [], g='mishap', act=('hop', 'ledge'), prefer=['young'])
o.emit(need=37)

# ============================================================ tire_swing
# A tyre on a rope from a beam, post on the left. Drawn parts (rep.py tire_swing): the post (full height, base plate), the rope,
# the tyre ring (22-168 px: low tip, belly, flanks, walls, sides) and the hole in it (lip at 58 px, edges at 80 px).
# Riding and exploring the swing are native acts; none of these ride it.
o = Obj('tire_swing', 'placed',
        fields=dict(twist=(0, 0, 1), frost=(0, 0, 1)),
        physics=[('twist', 'rate', -.0004, 'always'), ('twist', 'rate', .003, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrape=[('obj.dirt', 'add', -.2)], fluff=[('need.cleanliness', 'add', 1)],
            chip=[('frost', 'mul', .2)], dry=[('obj.wetness', 'add', -.4)],
            unkink=[('twist', 'mul', .1)], roll=[('twist', 'add', .5)], catch=[('twist', 'mul', .2)], unwound=[('twist', 'set', 0)],
            company=[('need.social', 'add', 2)]),
        anchors=dict(post_base=(.148, .959, 'surface'), post_low=(.148, .892), post_mid=(.148, .824),
                     tyre_tip=(.506, .919), tyre_belly_l=(.444, .905), tyre_belly_r=(.58, .905),
                     tyre_flank_l=(.383, .892), tyre_flank_r=(.63, .892), tyre_wall_l=(.333, .865), tyre_wall_r=(.679, .865),
                     tyre_side_l=(.309, .838), tyre_side_r=(.704, .838),
                     hole_lip=(.506, .851), hole_edge_l=(.42, .811), hole_edge_r=(.593, .811), rope_foot=(.506, .635)))
# --- care
o.r('wipe_flank_clean', "Wiping dried mud off the tyre's flank with a wing, left rim to right", 16, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.4, y=.6), k(.35, 'tyre_flank_l', reach=1, x=.8, y=.6, b=.6, mark='skrk'), k(.6, 'tyre_flank_r', reach=1, x=.8, y=.6, b=.6, mark='skrk'), k(.85, eye='^')],
    [(.6, 'wipe')], g='care', act=('wipe', 'flank'), when=['obj_dirt>.3'], obj=[(.35, dict(sway=.2)), (.6, dict(sway=-.2))],
    say=["Wiped the flank. Mud, meet wing. Wing, meet regret.", "It's cleaner. It still hangs there like a dare."])

o.r('scrape_the_tread', "Scraping caked mud out of the tread along the tyre's bottom edge with his bill", 16, 'none',
    [k(.2, 'tyre_tip', x=.9, y=1, b=.6), k(.4, 'tyre_tip', x=1.4, y=1.4, b=.8, mark='tk'), k(.6, 'tyre_belly_l', x=1.4, y=1.4, b=.8, mark='tk'), k(.8, 'tyre_belly_r', x=1.4, y=1.4, b=.8, mark='tk'), k(.92, y=.2, eye='^')],
    [(.6, 'scrape')], g='care', act=('scrape', 'tread'), when=['obj_dirt>.3'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))],
    say=["Scraped the muck out. There's a lot of muck. It will return.", "Clean tread. Only my conscience has improved."])

o.r('fluff_up_on_the_tread', "Fluffing his ruffled feathers by dragging each side along the tyre's rough wall in turn", 18, 'none',
    [k(.2, 'tyre_wall_l', x=-.8, y=.5, w=.4), k(.4, 'tyre_wall_l', x=-1.4, y=.6, b=.6, w=1, mark='fff'), k(.6, 'tyre_wall_r', x=-1.4, y=.6, b=.6, w=1, mark='fff'), k(.82, eye='^', w=.4)],
    [(.6, 'fluff')], g='care', act=('fluff', 'feathers'), prefer=['grumpy'],
    say=["Rubbed my sides on a tyre. Feel groomed. Smell of garage.", "Magnificent again. The tyre's a good sport, being rubber."])

# --- weather
o.r('chip_frost_off_the_tyre', "Chipping the frost off the tyre's side with the edge of his bill, working up the flank", 20, 'none',
    [k(.2, 'tyre_belly_l', x=.8, y=.8, b=.6), k(.4, 'tyre_flank_l', x=1.4, y=1, b=.8, mark='tik'), k(.6, 'tyre_wall_l', x=1.4, y=.8, b=.6, mark='tik'), k(.8, 'tyre_wall_l', x=1.4, y=.8, b=.2, mark='tik'), k(.92, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'tyre'), when=['frost>.3'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))],
    say=["Frost's off. The tyre looks thawed or insulted, hard to tell.", "My bill's gone numb. It chipped what I couldn't feel."])

o.r('rub_the_wet_tyre_dry', "Backing up to the damp tyre and rubbing its flank dry with his tail feathers", 18, 'none',
    [k(.2, 'tyre_flank_r', x=-.8, y=.6, b=.6), k(.4, 'tyre_flank_r', x=-1.4, y=.8, b=.8, w=.6, mark='fff'), k(.62, 'tyre_wall_r', x=-1.4, y=.8, b=.8, w=1, mark='fff'), k(.85, eye='^', w=.4)],
    [(.62, 'dry')], g='weather', act=('dry', 'tyre'), when=['obj_wetness>.3'])
o.r('unwind_the_gale_twist', "Walking the tyre back round at the sides until the wind's twist is out of the rope", 22, 'wing',
    [k(.15, 'tyre_side_l', reach=.5, x=.4, y=.6), k(.35, 'tyre_side_l', reach=1, x=.9, y=.6, b=.6, mark='hnng'), k(.55, 'tyre_side_r', reach=1, x=.9, y=.6, b=.6, mark='hnng'), k(.8, eye='^')],
    [(.55, 'unkink')], g='weather', act=('straighten', 'rope'), when=['twist>.4'], obj=[(.35, dict(sway=.3)), (.55, dict(sway=-.5)), (.8, dict(sway=.2))],
    say=["Untwisted the rope. The wind's furious. Good.", "Tyre hangs straight. I'm taking credit."])

# --- use
o.r('wind_the_rope_up', "Walking the tyre round and round to wind its rope up tight, right wall to left", 22, 'wing',
    [k(.15, 'tyre_wall_r', reach=.5, x=.5, y=.6), k(.35, 'tyre_wall_r', reach=1, x=.9, b=.6, l=1, mark='hnnng'), k(.55, 'tyre_wall_l', reach=1, x=.9, b=.6, r=1, mark='hnnng'), k(.8, x=-1.2, y=1.2, eye='O')],
    [(.55, 'roll')], g='use', act=('roll', 'tyre'), when=['twist<.6'], prefer=['curious'], obj=[(.35, dict(sway=.3)), (.55, dict(sway=.5, shake=.2))])
o.r('heave_the_edge_up', "Heaving the tyre's low edge up on its rope and letting it flop back with a thump", 16, 'wing',
    [k(.15, 'tyre_tip', reach=.5, y=.6, b=.6), k(.35, 'tyre_tip', reach=1, y=-.2, b=-.6, mark='hng'), k(.55, x=-1.2, y=1.2, b=.6, eye='-'), k(.75, eye='^', mark='thunk')],
    [], g='use', act=('lift', 'tyre'), ages=GROWN, obj=[(.35, dict(sway=.6)), (.6, dict(sway=-.4, shake=.3))])
o.r('hook_the_rope_with_a_twig', "Hooking the rope with a twig and hauling the tyre out sideways to full stretch before letting go", 24, 'twig',
    [k(.15, 'rope_foot', reach=.6, y=-.5, x=.3), k(.4, 'rope_foot', reach=1, x=1.2, y=-.8, b=.6, mark='hnf'), k(.6, 'rope_foot', reach=1, x=1.5, y=-.8, b=.6, l=1), k(.78, x=-1.2, y=.6, eye='O')],
    [], g='use', act=('hook', 'rope'), obj=[(.4, dict(sway=.5)), (.6, dict(sway=1)), (.8, dict(sway=-.8))])
o.r('look_out_through_the_ring', "Pushing his head into the hole to look out at the yard through the ring", 16, 'none',
    [k(.2, 'hole_lip', x=.6, y=.8, b=.6), k(.45, 'hole_edge_l', x=1.6, y=1.6, b=.8, eye='o', mark='hm'), k(.7, 'hole_edge_l', x=1.8, y=1.8, b=.8, eye='O'), k(.88, x=0, eye='-')],
    [], g='use', act=('peer', 'hole'), shown='head', prefer=['curious'])
o.r('push_for_a_missing_friend', "Giving the empty tyre push after push, a little harder each time, the way you would for a friend", 24, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.4, y=.6), k(.3, 'tyre_flank_l', reach=1, x=.7, y=.6, b=.6), k(.5, 'tyre_flank_l', reach=1, x=1.1, y=.8, b=.8, mark='hup'), k(.7, 'tyre_flank_l', reach=1, x=1.6, y=1, b=1, mark='HUP'), k(.88, eye='-', x=-.4, y=.2)],
    [(.7, 'company')], g='use', act=('push', 'tyre'), when=['lonely'], obj=[(.3, dict(sway=.3)), (.5, dict(sway=.6)), (.7, dict(sway=1)), (.88, dict(sway=-.6))],
    say=["Pushed it harder each time. It didn't giggle. High standards.", "That's more swing than I've had from a friend."])

o.r('tug_the_rim_toward_him', "Pulling the tyre's rim toward him with his bill and letting it snap back", 14, 'none',
    [k(.2, 'tyre_belly_r', x=.8, y=.8, b=.6), k(.4, 'tyre_belly_r', x=-1.4, y=1.2, b=.8, mark='hnn'), k(.6, x=.4, y=.6, eye='o', mark='...'), k(.8, 'tyre_belly_r', x=1.4, y=.8, b=.6, mark='twang')],
    [], g='use', act=('tug', 'tyre'), obj=[(.4, dict(sway=-.5)), (.6, dict(sway=.8)), (.8, dict(sway=-.3))])
# --- play
o.r('shove_and_flatten', "Shoving the tyre off at arm's length and flattening himself as it sails back past", 18, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.3, y=.6), k(.3, 'tyre_flank_l', reach=1, x=.8, b=-1.6, mark='hup'), k(.5, x=.2, y=1.6, b=1.6, eye='O'), k(.7, x=.2, y=1.6, b=1.6, eye='-', mark='whoosh'), k(.88, eye='^')],
    [], g='play', act=('shove', 'tyre'), prefer=['happy'], obj=[(.3, dict(sway=.3)), (.45, dict(sway=1)), (.6, dict(sway=-1)), (.75, dict(sway=.5))])
o.r('poke_and_run', "Poking the tyre's bottom tip and sprinting away before it can come back round", 14, 'none',
    [k(.2, 'tyre_tip', x=1.4, y=.8, b=.6, mark='boop'), k(.4, x=-1.4, b=-1.6, w=1, eye='>'), k(.6, x=-2, l=1, b=-1.6, eye='>'), k(.85, x=-.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('nudge', 'tyre'), prefer=['grumpy', 'young'], obj=[(.25, dict(sway=.6)), (.6, dict(sway=-.6))],
    say=["Poked. Ran. It's coming. They always come back.", "I'm not scared. I'm tactically elsewhere."])

o.r('pat_the_tyre_on_its_return', "Pushing the tyre away, then slapping its flank as it comes back, like a high five from something with no hands", 20, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.3), k(.3, 'tyre_flank_l', reach=1, x=.7, b=.4, mark='hup'), k(.5, x=-.4, w=.4, eye='o'), k(.68, 'tyre_flank_r', reach=1, x=.9, y=.4, b=-.6, mark='SLAP'), k(.85, eye='^')],
    [], g='play', act=('pat', 'tyre'), prefer=['happy'], obj=[(.3, dict(sway=.7)), (.5, dict(sway=-.7)), (.68, dict(sway=.5))])
o.r('peek_round_the_post', "Peeking round the post's edge at the tyre every time it swings by, ducking back each pass", 20, 'none',
    [k(.2, 'post_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'post_mid', x=1.4, y=0, eye='O'), k(.6, 'post_low', x=-1.2, y=.8, b=.6, eye='o'), k(.8, 'post_low', x=1.4, y=0, eye='O', mark='ha')],
    [], g='play', act=('hide', 'post'), prefer=['curious', 'young'], obj=[(.2, dict(sway=.7)), (.5, dict(sway=-.6)), (.8, dict(sway=.5))])
o.r('bump_the_tyre_with_his_chest', "Hopping up at the tyre's low edge and bumping it with his chest, a bit higher each time", 18, 'none',
    [k(.15, 'tyre_tip', x=.4, b=.6), k(.3, 'tyre_tip', x=1.4, y=.5, b=-1.6, mark='bump'), k(.5, 'tyre_belly_l', x=1.4, y=.5, b=-2, w=.6, mark='BUMP'), k(.7, 'tyre_belly_l', x=1.8, y=.5, b=-2.4, w=1, mark='BUMP'), k(.88, x=0, eye='^')],
    [], g='play', act=('hop', 'tyre'), prefer=['happy', 'young'], obj=[(.3, dict(sway=.3)), (.5, dict(sway=.5)), (.7, dict(sway=.8))])
o.r('catch_the_spinning_tyre', "Catching the rope-spun tyre by its rim and bracing both feet until it stops dead", 16, 'none',
    [k(.2, 'tyre_flank_r', x=-.4, y=.4, b=.4, eye='o'), k(.4, 'tyre_flank_r', x=1.6, y=.8, b=1, l=1, r=1, mark='skrrk'), k(.65, 'tyre_flank_r', x=1.6, y=.8, b=1, eye='-'), k(.85, y=.2, eye='^')],
    [(.4, 'catch')], g='play', act=('catch', 'tyre'), when=['twist>.4'], obj=[(.2, dict(shake=.5)), (.4, dict(shake=.6)), (.7, dict(sway=0))])
o.r('race_the_tyre_to_the_post', "Shoving the tyre off and racing it to the post and back before it finishes its swing", 20, 'none',
    [k(.15, 'tyre_flank_l', x=.8, y=.4, b=.4), k(.3, x=-1.6, b=-1.6, w=1, eye='>'), k(.5, 'post_low', x=1.4, b=-1.6, l=1, eye='>', mark='TAG'), k(.72, x=1.6, b=-1.6, r=1, eye='>'), k(.88, x=.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('race', 'tyre'), prefer=['happy'], obj=[(.15, dict(sway=.8)), (.5, dict(sway=-.9)), (.75, dict(sway=.6))])
# --- test
o.r('sniff_up_the_flank', "Sniffing up the flank from the tread for any trace of the road it came off", 18, 'none',
    [k(.2, 'tyre_belly_l', x=.5, y=.8, b=.6), k(.4, 'tyre_wall_l', x=1.1, y=.6, eye='o', mark='snf'), k(.6, 'tyre_side_l', x=1.1, y=.2, eye='O', mark='snf'), k(.82, x=0, eye='-')],
    [], g='test', act=('sniff', 'tread'), prefer=['curious'], ages=GROWN)
o.r('knock_for_hollow', "Rapping the tyre's wall twice with his bill to hear what is inside it", 14, 'none',
    [k(.2, 'tyre_wall_r', x=.8, y=.5, b=.6), k(.4, 'tyre_wall_r', x=1.6, y=.5, mark='tok'), k(.6, 'tyre_wall_r', x=.8, y=.5, b=.6), k(.78, 'tyre_wall_r', x=1.6, y=.5, mark='tok'), k(.9, x=-.4, y=-1.6, eye='o')],
    [], g='test', act=('knock', 'tyre'), prefer=['curious'], obj=[(.4, dict(shake=.2)), (.78, dict(shake=.2))])
o.r('weigh_the_tyre', "Pressing a wing against the tyre's belly to feel how heavy it hangs", 16, 'wing',
    [k(.2, 'tyre_belly_r', reach=.5, x=.5, y=.6), k(.45, 'tyre_belly_r', reach=1, x=1.1, y=.6, b=.8, eye='>', mark='hnng'), k(.7, 'tyre_belly_r', reach=1, x=1.4, y=.8, b=1, mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('weigh', 'tyre'), obj=[(.45, dict(sway=.3)), (.7, dict(sway=.2))])
o.r('count_the_post_marks', "Counting the marks up the post from its low end, bill touching each one", 20, 'none',
    [k(.2, 'post_low', x=.5, y=.5, b=.6), k(.4, 'post_low', x=.8, y=.4, eye='o', mark='one'), k(.6, 'post_mid', x=.8, y=-.2, eye='o', mark='two'), k(.8, 'post_mid', x=.2, y=-1.8, b=.6, eye='O', mark='...')],
    [], g='test', act=('count', 'post'), prefer=['curious'])
o.r('measure_up_to_the_tyre', "Standing flank to flank with the tyre and laying a wing along both to see who is taller", 20, 'wing',
    [k(.15, 'tyre_side_r', reach=.4, x=-.4, y=-.2), k(.4, 'tyre_side_r', reach=1, x=.2, y=-1.8, b=.4, mark='hm'), k(.65, 'tyre_side_r', reach=1, x=.2, y=-1.8, b=.8, eye='^', mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('measure', 'tyre'), prefer=['curious', 'young'])
# --- rest
o.r('lean_against_the_post', "Leaning his back against the post with his chin up and his eyes half shut", 22, 'none',
    [k(.2, 'post_low', x=-.4, y=.2, b=.4), k(.4, 'post_low', x=-1.4, y=-1.8, b=1.6, eye='-', w=.4), k(.7, 'post_low', x=-1.8, y=-1.8, b=2, w=1, eye='-', mark='mm'), k(.9, y=0, eye='^')],
    [], g='rest', act=('lean', 'post'), prefer=['tired'])
o.r('chin_on_the_rim', "Resting his chin against the tyre's low rim, eyes half shut, while it drifts gently", 22, 'none',
    [k(.2, 'tyre_flank_r', x=.4, y=.6, b=.6), k(.4, 'tyre_flank_r', x=1.5, y=1.8, b=1.6, eye='-'), k(.7, 'tyre_flank_r', x=1.8, y=2.4, b=2, eye='-', mark='mm'), k(.9, y=.2, eye='^')],
    [], g='rest', act=('lean', 'rim'), prefer=['tired', 'sad'], obj=[(.4, dict(sway=.2)), (.7, dict(sway=-.2))])
o.r('hug_the_tyre', "Wrapping both wings round the tyre's side and holding on with his cheek against the rubber", 24, 'wing',
    [k(.2, 'tyre_flank_r', reach=.5, x=.4, y=.4), k(.45, 'tyre_flank_r', reach=1, x=.9, y=.8, b=.4, eye='-'), k(.75, 'tyre_flank_r', reach=1, x=.9, y=.8, b=.4, eye='-', mark='mm'), k(.9, reach=.2, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'tyre'), when=['lonely'],
    say=["Hugged a tyre. It was warmer than expected. So's my face.", "Don't ask what I whispered into it."])
# --- show
o.r('showroom_pose', "Posing beside the tyre with a wing on its wall like a salesman unveiling this year's model", 18, 'wing',
    [k(.15, 'tyre_wall_l', reach=.4, y=-.2, x=-.4), k(.4, 'tyre_wall_l', reach=1, y=-1.8, x=-.4, eye='^', mark='behold'), k(.7, 'tyre_wall_l', reach=1, y=-1.8, x=-.6, b=.4, eye='-'), k(.88, reach=.2, eye='^')],
    [], g='show', act=('pose', 'tyre'), prefer=['happy', 'grown'])
# --- mishap
o.r('stuck_in_the_hole', "Wedging his head into the hole to the shoulders, sticking, and hauling out with a pop", 24, 'none',
    [k(.15, x=.6, eye='>'), k(.3, 'hole_lip', x=1.8, y=1.8, b=1.6, mark='oof'), k(.5, 'hole_lip', x=2, y=2, b=2, l=1, eye='O', mark='...'), k(.68, 'hole_edge_r', x=2.2, y=2, b=2, r=1, w=1, mark='POP'), k(.85, x=-1.6, y=1.8, b=1.2, eye='@')],
    [], g='mishap', act=('stuck', 'hole'), shown='head', prefer=['young', 'grumpy'], obj=[(.3, dict(sway=.5)), (.5, dict(shake=.6)), (.68, dict(sway=-.6)), (.85, dict(sway=.2))],
    say=["Head's through, brain's behind. Stuck between them.", "Pulled free. Left a feather and some dignity."])

o.r('turned_back_on_the_shove', "Giving the tyre a big shove, turning away, and taking a wallop to the back of the head as it swings back", 18, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.3), k(.3, 'tyre_flank_l', reach=1, x=.9, b=.4, mark='HUP'), k(.5, x=-.8, y=-.4, eye='^', mark='ha'), k(.68, 'tyre_tip', reach=.5, x=-1.8, y=1.8, b=1.8, eye='@', mark='BONK'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('shove', 'return'), obj=[(.3, dict(sway=.8)), (.55, dict(sway=-.6)), (.68, dict(shake=.3))],
    say=["Clocked from behind by a tyre. Telling no one.", "It had a head start and a rope. Unfair."])

o.r('swatted_by_the_unwinding_rope', "Letting go of the over-wound tyre and being swatted round by it as it spins free", 18, 'none',
    [k(.2, 'tyre_wall_l', x=.8, b=.8, eye='@'), k(.4, 'tyre_wall_l', x=1.4, b=1, w=1, eye='@'), k(.6, 'tyre_wall_r', x=2.4, y=1.8, b=.6, w=1, eye='@', mark='WHUMP'), k(.85, x=.8, y=1, b=1.4, eye='-')],
    [(.6, 'unwound')], g='mishap', act=('spin', 'body'), when=['twist>.4'], prefer=['young'], obj=[(.4, dict(sway=.8)), (.55, dict(shake=.8))])
o.r('count_the_gale_spins', "Nodding his bill against the post once for every turn the gale gives the tyre", 22, 'none',
    [k(.2, 'post_mid', x=.4, y=.4, eye='o'), k(.4, 'post_mid', x=1.4, y=.4, b=.6, mark='one'), k(.6, 'post_mid', x=.4, y=.2), k(.8, 'post_mid', x=1.4, y=.4, b=.6, mark='two', eye='@')],
    [], g='weather', act=('count', 'spins'), when=['windy', 'twist>.3'], prefer=['curious'], obj=[(.2, dict(sway=.9)), (.45, dict(sway=-1)), (.7, dict(sway=.9))],
    say=["Eleven turns, then I lost count. The wind didn't.", "Counted till I was dizzier than the tyre."])

o.r('count_the_swings', "Giving the tyre one push and counting its swings out loud until it comes to a stop", 24, 'wing',
    [k(.15, 'tyre_wall_r', reach=.6, x=.4, y=.4), k(.3, 'tyre_wall_r', reach=1, x=.9, b=.4, mark='hup'), k(.5, x=-.4, y=-1.8, eye='o', mark='one two'), k(.75, x=-.4, y=-1.8, eye='@', mark='...four'), k(.9, y=.2, eye='-')],
    [], g='test', act=('count', 'swings'), prefer=['curious'], obj=[(.3, dict(sway=.8)), (.45, dict(sway=-.6)), (.6, dict(sway=.4)), (.8, dict(sway=-.2))],
    say=["Seven swings, then it stopped. So did my interest.", "Counted aloud. The tyre didn't thank me."])

o.r('drum_solo_on_the_tyre', "Performing a drum solo with his bill, belly then flank then wall, the tyre ringing a muffled note", 20, 'none',
    [k(.15, 'tyre_belly_l', x=.8, y=.4, b=.4), k(.3, 'tyre_belly_l', x=1.4, y=.4, mark='dum'), k(.45, 'tyre_flank_l', x=1.4, y=.4, b=.4, mark='dum'), k(.6, 'tyre_wall_l', x=1.4, y=.4, mark='DUM'), k(.8, 'tyre_wall_l', x=-.4, y=-1.8, w=1, eye='^', mark='tsss')],
    [], g='show', act=('drum', 'tyre'), prefer=['happy'], obj=[(.3, dict(shake=.1)), (.45, dict(shake=.1)), (.6, dict(shake=.2))],
    say=["Drum solo. Muffled but sincere.", "The tyre has one note and it's a sigh."])

o.r('mime_the_swing', "Swaying side to side in front of the tyre with his wings out, copying its swing beat for beat", 22, 'none',
    [k(.2, x=-1.4, y=.4, w=.6, eye='o'), k(.4, x=1.4, y=.4, w=1, l=1, eye='^'), k(.6, x=-1.4, y=.4, w=1, r=1, eye='^'), k(.8, x=1.4, y=.4, w=.6, l=1, eye='^', mark='whee')],
    [], g='show', act=('show', 'swing'), prefer=['happy'], obj=[(.2, dict(sway=.8)), (.4, dict(sway=-.8)), (.6, dict(sway=.8)), (.8, dict(sway=-.6))],
    say=["Did the swing without the swing. Subtle. Misunderstood.", "Wings out, hips going. The tyre should take notes."])

o.r('flourish_off_the_base_plate', "Springing off the post's base plate, tapping the lip of the hole with his bill as a flourish, and sticking the landing", 20, 'none',
    [k(.15, 'post_base', perch=1, b=.6, x=-.4), k(.3, 'post_base', perch=1, b=-2, w=1, mark='HUP'), k(.5, 'hole_lip', x=2, y=.4, b=-2.4, w=1, mark='tk'), k(.7, x=.4, y=.4, b=1.2, w=.4), k(.88, eye='^', mark='ta-da')],
    [], g='show', act=('hop', 'plate'), prefer=['happy', 'young'], obj=[(.5, dict(sway=.3))])
o.r('kick_the_tread', "Kicking the tread in a temper and hopping away holding his toe", 16, 'none',
    [k(.2, 'tyre_belly_l', x=-.8, y=.4, r=1), k(.4, 'tyre_belly_l', x=-1.4, y=.6, r=1, b=.6, mark='THWK'), k(.6, x=.4, y=1.8, b=.8, l=1, eye='O', mark='ow'), k(.82, x=.4, y=.8, l=1, b=.4, eye='@')],
    [], g='mishap', act=('kick', 'tread'), prefer=['grumpy'], obj=[(.4, dict(sway=.3))],
    say=["Kicked a tyre. It's been kicked by better.", "My toe has filed an appeal."])

o.r('missed_the_hop', "Hopping for the hole, hitting the tyre's side wall instead, and bouncing off onto his tail", 16, 'none',
    [k(.2, x=.6, b=.8, eye='>'), k(.4, 'tyre_side_l', x=1.4, b=-2, w=1, mark='hup'), k(.6, x=-1.8, y=1.8, b=1.6, l=1, r=1, eye='@', mark='thud'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('hop', 'hole'), prefer=['young'], obj=[(.4, dict(sway=.7)), (.6, dict(sway=-.5))])
o.r('trip_over_the_base_plate', "Backing away from the swinging tyre, catching a heel against the post's base plate, and landing on his tail", 18, 'none',
    [k(.2, x=1.4, y=.4, eye='o'), k(.4, 'post_base', x=-1.4, y=.4, b=.6, l=1, eye='O'), k(.6, x=-2.4, y=-1.6, b=1.8, w=1, eye='@', mark='WHUMP'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('walk_into', 'plate'), prefer=['young'], obj=[(.2, dict(sway=.8)), (.5, dict(sway=-.7))],
    say=["The plate tripped me. It's been there longer.", "Landed on my tail. Tail's seen worse."])

o.emit(need=39)

# ============================================================ toy_seesaw
# An A-frame with a centre post (rung marks), a flat plank on a hinge, studs along the plank face, a seat pad and a handle
# at each end. Parts never move: only the whole toy sways or shakes. Riding it is native, so none of these ride.
o = Obj('toy_seesaw', 'placed',
        fields=dict(leaves=(0, 0, 1), frost=(0, 0, 1), snowcap=(0, 0, 1)),
        physics=[('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrub=[('obj.dirt', 'add', -.25)], dust=[('obj.dirt', 'add', -.2)],
            sweep=[('leaves', 'set', 0)], chip=[('frost', 'mul', .2)], scoop=[('snowcap', 'mul', .2)],
            snooze=[('need.energy', 'add', 3)], fun=[('need.fun', 'add', 2)]),
        anchors=dict(base_l=(.444, .952, 'surface'), base_mid=(.505, .952, 'surface'), base_r=(.566, .952, 'surface'),
                     leg_l_low=(.434, .905), leg_l_mid=(.455, .786), leg_l_top=(.475, .667),
                     leg_r_low=(.566, .905), leg_r_mid=(.545, .786), leg_r_top=(.535, .667),
                     post_low=(.505, .857), post_mid=(.505, .786), post_top=(.505, .643),
                     plank_under_l=(.242, .619), plank_under_r=(.768, .619), plank_face_l=(.242, .595),
                     plank_end_l=(.091, .595), plank_end_r=(.919, .595), plank_face_r=(.808, .595), hinge=(.505, .595), plank_under_m=(.444, .619),
                     stud_l=(.131, .571), stud_m=(.313, .571), seat_l=(.172, .5), seat_r=(.838, .5), handle_l=(.242, .405)))
# --- care
o.r('wipe_the_plank_face', "Wiping the grime off the plank's face with a wing, from the left end in to the hinge", 18, 'wing',
    [k(.15, 'plank_under_l', reach=.6, x=.4, y=.6), k(.35, 'plank_under_l', reach=1, x=.8, y=.6, b=.6, mark='fff'), k(.55, 'plank_face_l', reach=1, x=.8, y=.2, b=.4, mark='fff'), k(.75, 'hinge', reach=1, x=.8, y=-.2, mark='fff'), k(.9, eye='^')],
    [(.75, 'wipe')], g='care', act=('wipe', 'plank'), when=['obj_dirt>.3'], obj=[(.35, dict(shake=.1)), (.75, dict(shake=.1))])
o.r('scrub_the_base_bar', "Scrubbing the base bar clean with his bill, from the left foot to the right", 18, 'none',
    [k(.2, 'base_l', x=.9, y=1, b=.6), k(.4, 'base_l', x=1.4, y=1.4, b=.8, mark='skrt'), k(.6, 'base_mid', x=1.4, y=1.4, b=.8, mark='skrt'), k(.8, 'base_r', x=1.4, y=1.4, b=.8, mark='skrt'), k(.92, y=.2, eye='^')],
    [(.8, 'scrub')], g='care', act=('scrub', 'base'), when=['obj_dirt>.3'])
o.r('dust_the_seat_pad', "Reaching a twig up to dust the left seat pad, stroke after stroke along it", 20, 'twig',
    [k(.15, 'seat_l', reach=.6, y=-.5), k(.4, 'seat_l', reach=1, x=.5, y=-.8, mark='fff'), k(.6, 'seat_l', reach=1, x=-.2, y=-.8, b=.2, mark='fff'), k(.82, y=-.3, eye='^')],
    [(.6, 'dust')], g='care', act=('wipe', 'seat'), when=['obj_dirt>.3'])
o.r('sweep_leaves_off_the_base', "Sweeping the drifted leaves off the base bar with a wing, one foot to the other", 18, 'wing',
    [k(.15, 'base_l', reach=.5, x=.3, y=.6), k(.4, 'base_l', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.62, 'base_r', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.85, eye='^')],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['fall'])
# --- weather
o.r('chip_frost_off_the_base', "Chipping the frost off the base bar with the edge of his bill, working along it", 18, 'none',
    [k(.2, 'base_l', x=.8, y=.8, b=.6), k(.4, 'leg_l_low', x=1.4, y=.8, b=.6, mark='tik'), k(.6, 'base_l', x=1.4, y=1.2, b=.8, mark='tik'), k(.8, 'base_mid', x=1.4, y=1.2, b=.8, mark='tik'), k(.92, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'base'), when=['frost>.3'])
o.r('scoop_snow_off_the_feet', "Scooping the snow banked round the A-frame's feet aside with his bill, left leg then right", 20, 'none',
    [k(.2, 'leg_l_low', x=.9, y=1, b=.6), k(.4, 'leg_l_low', x=1.5, y=1.4, b=.8, mark='fshh'), k(.65, 'leg_r_low', x=1.5, y=1.4, b=.8, mark='fshh'), k(.85, y=.3, eye='^')],
    [(.65, 'scoop')], g='weather', act=('scoop', 'snow'), when=['snowcap>.3'],
    say=["Dug the legs out. The seesaw's grateful, in a wooden way.", "Snow's gone. It'll hold a grudge, same as me."])

# --- use
o.r('press_the_end_up', "Shoving the plank's left end up with a wing and letting it drop back with a clunk", 18, 'wing',
    [k(.15, 'plank_end_l', reach=.6, x=.3, b=.4), k(.35, 'plank_end_l', reach=1, x=.9, y=-.2, b=-1.6, mark='hng'), k(.55, x=-1.2, y=.6, b=.6, eye='o'), k(.72, eye='-', mark='clunk')],
    [], g='use', act=('press', 'plank_end'), obj=[(.35, dict(sway=.7)), (.55, dict(sway=-.4, shake=.3))])
o.r('lever_the_end_with_a_twig', "Wedging a twig against the plank's right end and levering until the whole toy rocks", 22, 'twig',
    [k(.15, 'plank_end_r', reach=.6, x=.3, y=-.4), k(.4, 'plank_end_r', reach=1, x=1.2, y=-.8, b=.8, mark='hnnf'), k(.62, 'plank_end_r', reach=1, x=1.5, y=-.8, b=1.2, l=1), k(.82, x=-.4, y=.4, eye='^')],
    [], g='use', act=('tilt', 'plank'), obj=[(.4, dict(sway=.5)), (.62, dict(sway=1)), (.82, dict(sway=-.5))])
o.r('drum_along_the_plank', "Drumming along the plank's face with his bill, from the left end to the right", 20, 'none',
    [k(.15, 'plank_under_l', x=.6, y=-.2), k(.3, 'plank_under_l', x=1.4, y=-.2, mark='tok'), k(.45, 'plank_under_m', x=1.4, y=-.4, mark='tok'), k(.6, 'plank_under_r', x=1.4, y=-.6, mark='tok'), k(.78, 'plank_under_r', x=.6, y=-.2), k(.9, eye='^')],
    [], g='use', act=('drum', 'plank'), prefer=['happy'], obj=[(.3, dict(shake=.1)), (.45, dict(shake=.1)), (.6, dict(shake=.1))],
    say=["Plank's got rhythm. I've got a bill. We're a band.", "Tok tok tok. Percussion is the only honest job."])

o.r('tug_the_handle', "Hooking a twig round the left handle pole and tugging it like a lever", 20, 'twig',
    [k(.15, 'handle_l', reach=.6, y=-.5, x=.3), k(.4, 'handle_l', reach=1, x=1.2, y=-.8, b=.8, mark='hnf'), k(.55, 'handle_l', reach=1, x=-.8, y=-.4, b=.4), k(.75, x=.4, y=.4, eye='-', mark='...')],
    [], g='use', act=('tug', 'handle'), obj=[(.4, dict(shake=.2))],
    say=["Pulled the lever. Nothing happened. Engineering.", "Whatever that's for, it isn't for ducks."])

o.r('tap_the_seat_pad', "Tapping the right seat pad twice with a twig to hear whether it is padded at all", 16, 'twig',
    [k(.15, 'seat_r', reach=.6, y=-.5), k(.35, 'seat_r', reach=1, x=.8, y=-.8, mark='tk'), k(.55, 'seat_r', reach=.6, x=.3, y=-.6), k(.72, 'seat_r', reach=1, x=.8, y=-.8, mark='tk'), k(.9, y=-.2, eye='o')],
    [], g='use', act=('tap', 'seat'), prefer=['curious'])
# --- play
o.r('hop_up_and_down_the_base', "Hopping up onto the base bar and bouncing on it so the whole toy trembles", 18, 'none',
    [k(.15, 'base_mid', perch=1, b=.6), k(.3, 'base_mid', perch=1, b=-1.6, w=.6, mark='hup'), k(.45, 'base_mid', perch=1, b=1.2), k(.6, 'base_mid', perch=1, b=-2, w=1, mark='HUP'), k(.78, 'base_mid', perch=1, b=1.2), k(.92, eye='^')],
    [(.6, 'fun')], g='play', act=('hop', 'base'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.2)), (.6, dict(shake=.5)), (.78, dict(shake=.2))])
o.r('walk_the_base_beam', "Walking the base bar from end to end like a balance beam with his wings out", 20, 'none',
    [k(.15, 'base_l', perch=1, w=.4, y=-.2), k(.35, 'base_l', perch=1, l=1, w=1, b=.6, mark='...'), k(.6, 'base_mid', perch=1, r=1, w=1, b=.6), k(.8, 'base_r', perch=1, l=1, w=1, b=.8, eye='O'), k(.92, 'base_r', perch=1, w=.4, eye='^')],
    [], g='play', act=('balance', 'base'), prefer=['curious', 'young'])
o.r('race_round_the_frame', "Running a lap of the frame and slapping each leg as he passes", 18, 'wing',
    [k(.15, x=-1.6, b=.8, eye='>'), k(.3, 'leg_l_low', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.5, 'post_low', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.7, 'leg_r_low', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.88, x=1.2, eye='^')],
    [], g='play', act=('race', 'frame'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.2)), (.5, dict(shake=.2)), (.7, dict(shake=.2))])
# --- test
o.r('count_the_studs', "Counting the studs along the plank with the tip of a twig, tapping each one", 22, 'twig',
    [k(.15, 'stud_l', reach=.6, y=-.5, x=.3), k(.35, 'stud_l', reach=1, x=.7, y=-.7, mark='one'), k(.6, 'stud_m', reach=1, x=.7, y=-.7, mark='two'), k(.82, 'stud_m', reach=.5, x=.2, y=-.8, eye='o', mark='...')],
    [], g='test', act=('count', 'studs'), prefer=['curious'])
o.r('sniff_the_plank', "Sniffing along the plank's face for the smell of whoever sat here last", 18, 'none',
    [k(.2, 'plank_under_l', x=.5, y=-.2, b=.2), k(.4, 'plank_face_l', x=1.2, y=-.4, eye='o', mark='snf'), k(.6, 'plank_face_l', x=1.5, y=-.6, b=.4, eye='O', mark='snf'), k(.82, x=0, eye='-')],
    [], g='test', act=('sniff', 'plank'), prefer=['curious'],
    say=["Splinters, rain and someone else's turn.", "Smells like a playground that gave up."])

o.r('listen_at_the_hinge', "Pressing his ear to the hinge with a wing braced beside it, listening for a creak", 22, 'wing',
    [k(.2, 'hinge', reach=.5, x=.5, y=-.2), k(.4, 'hinge', reach=1, x=.1, y=-1.8, b=.6, eye='-', mark='...'), k(.7, 'hinge', reach=1, x=.1, y=-1.8, b=1.4, eye='o', mark='...'), k(.88, x=0, eye='-')],
    [], g='test', act=('listen', 'hinge'), prefer=['curious'])
o.r('shove_the_frame_to_test', "Throwing his shoulder against the right leg to see whether the frame will scoot", 16, 'none',
    [k(.2, x=-1.4, y=.6), k(.4, 'leg_r_mid', x=1.6, b=.8, mark='hup'), k(.55, 'leg_r_low', x=1.6, b=1, mark='...'), k(.85, x=0, eye='-')],
    [], g='test', act=('shake', 'frame'), obj=[(.4, dict(shake=.4)), (.55, dict(shake=.2))])
o.r('peck_up_the_rungs', "Pecking up the centre post rung by rung, as far as his bill will go", 20, 'none',
    [k(.2, 'post_low', x=.6, y=.8, b=.6), k(.4, 'post_low', x=1.4, y=1.2, mark='tk'), k(.6, 'post_mid', x=1.4, y=.4, mark='tk'), k(.8, 'post_top', x=1.4, y=-.4, mark='tk'), k(.92, eye='^')],
    [], g='test', act=('peck', 'rungs'),
    say=["Eight rungs. Decoration with ambitions.", "Pecked every one. Still on the ground. Okay, then."])

o.r('compare_the_two_ends', "Looking from the left end of the plank to the right, a wing out at each, judging which is lower", 22, 'wing',
    [k(.15, 'plank_end_l', reach=.5, x=.2, y=-.4, eye='o'), k(.35, 'plank_end_l', reach=1, x=.2, y=-1.8, eye='O', mark='hm'), k(.6, 'plank_end_r', reach=1, x=.2, y=-1.8, eye='o'), k(.82, 'plank_end_r', reach=.5, x=-.2, y=-.6, eye='-', mark='level')],
    [], g='test', act=('compare', 'ends'), prefer=['curious', 'grown'])
# --- rest
o.r('nap_on_the_base_bar', "Curling up on the base bar with his bill tucked, dozing", 28, 'none',
    [k(.2, 'base_l', perch=1, x=.4, y=.8, b=.6), k(.4, 'base_l', perch=1, y=1.4, b=1.2, eye='-'), k(.7, 'base_l', perch=1, y=1.5, b=1.2, eye='-', mark='zzz'), k(.9, 'base_l', perch=1, y=.2, b=.3, eye='^')],
    [(.4, 'snooze')], g='rest', act=('nap', 'base'), prefer=['tired', 'night'])
o.r('wait_for_a_partner', "Waiting beside the left leg for someone to turn up for the far seat, glancing along the plank", 24, 'none',
    [k(.2, 'leg_l_mid', x=.2, y=-.2), k(.4, 'leg_l_mid', x=.2, y=-1.6, l=1, eye='o'), k(.6, 'leg_l_mid', x=1.4, y=-1.6, r=1, eye='o', mark='...'), k(.8, 'leg_l_mid', x=.6, y=-.5, eye='>')],
    [], g='rest', act=('wait', 'partner'), when=['lonely'],
    say=["It takes two. I brought one. Maths is brutal.", "The far seat's empty. It's honest about it, at least."])

o.r('sulk_at_the_far_leg', "Walking to the far leg, turning his back to the empty seats and sulking against it", 24, 'none',
    [k(.2, 'leg_r_low', x=.4, y=.6, b=.4), k(.4, 'leg_r_low', x=-.4, y=1.2, b=1.2, eye='-'), k(.75, 'leg_r_low', x=-.4, y=1.2, b=1.2, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [], g='rest', act=('sulk', 'leg'), when=['sad'],
    say=["Built for two. Used by one. A metaphor, probably.", "Don't say it's only a seesaw. Let me have this."])

# --- show
o.r('strike_the_a', "Standing at the post with a wing out to each leg, making himself the third side of the A", 20, 'wing',
    [k(.15, 'post_mid', reach=.4, y=-.3), k(.4, 'leg_l_mid', reach=1, x=-.2, y=-1.8, mark='A'), k(.65, 'leg_r_mid', reach=1, x=-.2, y=-1.8, mark='A'), k(.85, y=-.2, eye='^')],
    [], g='show', act=('pose', 'frame'), prefer=['happy'])
o.r('chant_see_saw', "Chanting see and then saw, wings up for see and down for saw", 20, 'none',
    [k(.2, y=-1.8, w=1, x=-.8, l=1, mark='see'), k(.4, y=1.2, w=.2, b=.8, mark='saw'), k(.6, y=-1.8, w=1, x=-.8, r=1, mark='SEE'), k(.8, y=1.2, w=.2, b=.8, mark='SAW')],
    [], g='show', act=('sing', 'chant'), prefer=['happy', 'young'],
    say=["See. Saw. Repeat. The lyrics aren't the point.", "I did the chorus. The seesaw did nothing, as usual."])

o.r('dance_along_the_base', "Dancing along the base bar from one foot to the other, a little hop at each end", 20, 'none',
    [k(.15, 'base_r', perch=1, l=1, w=.6), k(.35, 'base_mid', perch=1, r=1, w=1, y=-.4), k(.55, 'base_l', perch=1, l=1, b=-1.6, w=1, mark='hup'), k(.78, 'base_mid', perch=1, r=1, w=.6, b=.4), k(.92, eye='^')],
    [], g='show', act=('dance', 'base'), prefer=['happy'])
o.r('hail_the_far_seat', "Cupping a wing to his bill and calling along the plank to the far seat", 16, 'wing',
    [k(.2, 'leg_r_low', reach=.5, x=-.4, y=-.4), k(.4, 'leg_r_low', reach=1, x=-.8, y=-1.8, eye='O', mark='OI'), k(.62, 'leg_r_low', reach=1, x=-.8, y=-1.8, b=.8, mark='YOUR TURN'), k(.85, y=.4, eye='-', mark='...')],
    [], g='show', act=('shout', 'seat'), prefer=['lonely'])
# --- mishap
o.r('heaved_it_and_got_bonked', "Heaving the plank's left end up, stepping back to admire it, and getting the drop back square across his beak", 20, 'wing',
    [k(.15, 'plank_end_l', reach=.6, x=.3, b=.4), k(.3, 'plank_end_l', reach=1, x=.9, y=-.2, b=-1.6, mark='hng'), k(.5, x=-.8, y=-.6, eye='^', mark='ha'), k(.68, 'plank_under_l', reach=.5, x=-1.8, y=1.8, b=1.8, eye='@', mark='BONK'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('lift', 'plank_end'), obj=[(.3, dict(sway=.7)), (.55, dict(sway=-.6)), (.68, dict(shake=.4))],
    say=["Lifted it. Admired it. It disagreed with me.", "Fair. I'd drop on me too."])

o.r('banged_his_head_peering_through', "Poking his head through the gap beside the post to peer out at the yard and cracking it on the leg", 20, 'none',
    [k(.2, 'post_low', x=.8, y=.6, b=.6), k(.45, 'post_low', x=1.6, y=1.2, b=.8, eye='o', mark='hm'), k(.65, 'leg_l_mid', x=-1.8, y=1.8, b=1.2, eye='@', mark='CRACK'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('peer', 'frame'), shown='head', obj=[(.65, dict(shake=.3))])
o.r('drum_the_legs', "Playing the A-frame's legs like a xylophone, tapping up the left one and down the right", 20, 'none',
    [k(.15, 'leg_l_low', x=.8, y=.4, b=.4), k(.3, 'leg_l_low', x=1.4, y=.4, b=.4, mark='ting'), k(.45, 'leg_l_mid', x=1.4, y=-.4, mark='tang'), k(.6, 'leg_r_mid', x=1.4, y=-.4, mark='TING'), k(.75, 'leg_r_low', x=1.4, y=.4, b=.4, mark='tong'), k(.9, eye='^')],
    [], g='play', act=('drum', 'legs'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.1)), (.45, dict(shake=.1)), (.6, dict(shake=.1)), (.75, dict(shake=.1))],
    say=["Tune's rubbish. The legs never learned the words.", "Four notes, all damp. Still a hit."])

o.r('pat_the_plank_like_a_horse', "Patting the plank along its length like a horse's neck, left end to right, murmuring good plank", 22, 'wing',
    [k(.15, 'plank_under_l', reach=.5, x=.3), k(.35, 'plank_under_l', reach=1, x=.6, y=.4, mark='pat'), k(.55, 'plank_under_m', reach=1, x=.6, y=.4, mark='pat'), k(.75, 'plank_under_r', reach=1, x=.6, y=.4, mark='pat'), k(.9, eye='^', mark='good plank')],
    [], g='show', act=('pat', 'plank'), prefer=['happy', 'lonely'], obj=[(.35, dict(sway=.1)), (.55, dict(sway=.1)), (.75, dict(sway=.1))],
    say=["Good plank. Who's a good plank. Not an answer.", "Patted it end to end. It didn't buck. Wooden manners."])

o.r('peck_the_hinge_cap', "Pecking at the round cap at the hinge's centre as though it were an eye that had just winked", 16, 'none',
    [k(.2, 'hinge', x=.8, y=-.2, eye='o'), k(.35, 'hinge', x=1.4, y=-.2, eye='O', mark='tk'), k(.5, x=-.8, y=-1.8, eye='@'), k(.7, 'hinge', x=1.4, y=-.2, mark='tk'), k(.88, eye='-')],
    [], g='show', act=('peck', 'hinge'), prefer=['curious', 'grumpy'],
    say=["It winked first. I'm only returning the favour.", "Pecked a wink. Strange feeling. Worth it."])

o.r('sight_along_the_plank', "Laying his cheek against the plank's face near the right end and sighting along it to check that it runs straight", 20, 'wing',
    [k(.2, 'plank_face_r', reach=.5, x=.4, y=.2), k(.4, 'plank_face_r', reach=.8, x=-.4, y=1.2, b=.8, eye='-'), k(.65, 'plank_face_r', reach=.8, x=-1.4, y=1.8, b=1.2, eye='o', mark='...'), k(.85, eye='-')],
    [], g='test', act=('peer', 'plank'), prefer=['curious', 'grown'])
o.r('chin_on_the_plank_edge', "Propping his chin against the plank's low edge like a bar rail and watching the yard go by", 24, 'none',
    [k(.2, 'plank_under_r', x=.4, y=.4, b=.4), k(.45, 'plank_under_r', x=1, y=1.2, b=1, eye='-'), k(.75, 'plank_under_r', x=1.4, y=1.8, b=1.6, eye='o', mark='mm'), k(.9, y=0, eye='^')],
    [], g='rest', act=('lean', 'plank'), prefer=['tired', 'sad'],
    say=["Leaning on the bar. One duck, one plank, no drinks.", "Usual order: nothing. Make it a double."])

o.r('bounced_off_the_end_of_the_bar', "Bouncing so hard on the base bar that the frame throws him off the end and onto his tail", 18, 'none',
    [k(.15, 'base_r', perch=1, b=.6), k(.3, 'base_r', perch=1, b=-2, w=.6, mark='hup'), k(.5, 'base_r', perch=1, b=-2.4, w=1, eye='O', mark='HUP'), k(.7, x=-1.8, y=1.8, b=1.8, w=.6, l=1, eye='@', mark='thud'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('hop', 'bar'), prefer=['young', 'happy'], obj=[(.3, dict(shake=.3)), (.5, dict(shake=.6)), (.7, dict(shake=.2))],
    say=["Bounced myself out of my own game. Impressive, in a way.", "The bar says that's enough fun. The bar's a snob."])
o.emit(need=35)

# ============================================================ rubber_duck
# A big bath duck facing right: head with eye, flat bill, a wing mark, a tail point on the left, a rounded belly,
# a flat base rim and ripples below it. The squeak is the toy's whole point.
o = Obj('rubber_duck', 'placed',
        fields=dict(leaves=(0, 0, 1), snowcap=(0, 0, 1), heat=(0, 0, 1)),
        physics=[('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm'),
                 ('heat', 'rate', .002, 'sun'), ('heat', 'rate', -.001, '!sun')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], polish=[('obj.dirt', 'add', -.2)], scrape=[('obj.dirt', 'add', -.2)],
            sweep=[('leaves', 'set', 0)], knock_snow=[('snowcap', 'mul', .2)], cool=[('heat', 'mul', .5)],
            squeak=[('need.fun', 'add', 2)], snooze=[('need.energy', 'add', 3)], company=[('need.social', 'add', 2)]),
        anchors=dict(base_l=(.255, .838, 'surface'), base_mid=(.49, .838, 'surface'), base_r=(.725, .838, 'surface'),
                     ripple_l=(.392, .865), ripple_r=(.608, .865), tail_tip=(.098, .649), flank_l=(.157, .703),
                     belly_low=(.608, .784), belly_mid=(.51, .676, 'inside'), belly_r=(.745, .703),
                     wing_mark=(.392, .595), back_hump=(.235, .514), chest_r=(.863, .595), chest_hi=(.843, .486),
                     neck_back=(.51, .378), neck_front=(.863, .378), cheek=(.863, .243), eye_spot=(.706, .243),
                     bill_tip=(.902, .324), crest=(.686, .108)))
# --- care
o.r('wipe_the_belly', "Wiping the belly with long wing strokes, low curve to the right side", 18, 'wing',
    [k(.15, 'belly_low', reach=.6, x=.4, y=.6), k(.35, 'belly_low', reach=1, x=.8, y=.6, b=.6, mark='fff'), k(.55, 'belly_mid', reach=1, x=.8, y=.4, b=.4, mark='fff'), k(.75, 'belly_r', reach=1, x=.8, y=.2, mark='fff'), k(.9, eye='^')],
    [(.75, 'wipe')], g='care', act=('wipe', 'belly'), when=['obj_dirt>.3'], obj=[(.35, dict(sway=.1)), (.75, dict(sway=-.1))],
    say=["Belly's wiped. It's still a belly. I still did it.", "Rubber shines. Smug rubber, now."])

o.r('buff_the_bill', "Buffing the big flat bill with the feathers of his chest until it shines", 18, 'none',
    [k(.2, 'bill_tip', x=-.8, y=-.6, b=.4), k(.4, 'bill_tip', x=-1.4, y=-1.8, w=.4, mark='squk'), k(.6, 'bill_tip', x=-1.8, y=-1.8, w=.8, mark='squk'), k(.85, eye='^')],
    [(.6, 'polish')], g='care', act=('polish', 'bill'), when=['obj_dirt>.3'], ages=GROWN, obj=[(.4, dict(sway=.2)), (.6, dict(sway=-.2))],
    say=["Bill's gleaming. I could see me in it, if I looked.", "Chest feathers: the only cloth I own."])

o.r('pick_the_base_seam', "Picking grime out of the base rim with his bill, working from the left end to the right", 18, 'none',
    [k(.2, 'base_l', x=.9, y=.8, b=.6), k(.4, 'base_l', x=1.4, y=1.2, b=.8, mark='tk'), k(.6, 'base_mid', x=1.4, y=1.2, b=.8, mark='tk'), k(.8, 'base_r', x=1.4, y=1.2, b=.8, mark='tk'), k(.92, y=.2, eye='^')],
    [(.8, 'scrape')], g='care', act=('scrape', 'base'), when=['obj_dirt>.3'])
o.r('sweep_leaves_off_the_ripples', "Sweeping the leaves that have drifted round its base off the ripples with a wing", 18, 'wing',
    [k(.15, 'ripple_l', reach=.5, x=.3, y=.6), k(.4, 'ripple_l', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.62, 'ripple_r', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.85, eye='^')],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['fall'])
# --- weather
o.r('knock_the_snow_cap_off', "Knocking the snow cap off its head with a twig, topmost bit first", 20, 'twig',
    [k(.15, 'crest', reach=.6, y=-.6, x=.3), k(.4, 'crest', reach=1, x=.6, y=-.8, mark='whap'), k(.6, 'crest', reach=1, x=.6, y=-.8, mark='fshh'), k(.85, y=-.3, eye='^')],
    [(.6, 'knock_snow')], g='weather', act=('knock', 'snow'), when=['snowcap>.4'], ages=GROWN, obj=[(.4, dict(sway=.3)), (.6, dict(shake=.3))])
o.r('fan_the_hot_belly', "Fanning the sun-baked belly with a wing until the heat comes off it", 20, 'wing',
    [k(.15, 'belly_mid', reach=.5, x=.3), k(.35, 'belly_mid', reach=1, x=.5, y=.6, b=.4, mark='fwp'), k(.55, 'belly_mid', reach=.3, x=.3, y=.4), k(.75, 'belly_mid', reach=1, x=.5, y=.6, b=.4, mark='fwp'), k(.9, eye='^')],
    [(.75, 'cool')], g='weather', act=('cool', 'belly'), when=['heat>.5'])
# --- use
o.r('squeeze_the_belly', "Squeezing the belly between both wings until it gives one long dry squeak", 16, 'wing',
    [k(.2, 'belly_mid', reach=.6, x=.3, b=.4), k(.4, 'belly_mid', reach=1, x=.9, b=.8, mark='squuueak'), k(.6, 'belly_mid', reach=.4, x=.3, b=.2), k(.85, eye='^')],
    [(.4, 'squeak')], g='use', act=('squeeze', 'belly'), prefer=['happy', 'curious'], obj=[(.4, dict(shake=.3, puff=.3)), (.6, dict(sway=.2))],
    say=["Squeak. Honest noise. Better than most things I say.", "One note, and it sticks to it."])

o.r('stand_on_the_tail', "Bearing down with his whole weight against the tail point until the squeak comes from the other end", 16, 'none',
    [k(.2, 'tail_tip', x=-.4, y=.6, l=1), k(.4, 'tail_tip', x=-.6, y=1, b=.8, l=1, mark='squk'), k(.6, 'tail_tip', x=-.6, y=1, b=1.2, r=1, mark='SQUK'), k(.85, eye='^')],
    [(.4, 'squeak')], g='use', act=('press', 'tail'), obj=[(.4, dict(sway=.3, puff=.3)), (.6, dict(sway=-.2, puff=.3))])
o.r('rock_it_by_the_flank', "Shoving the flank so the whole duck rocks on its base and keeps going", 18, 'none',
    [k(.2, 'flank_l', x=-.8, y=.6), k(.4, 'flank_l', x=1.6, y=.8, b=.8, mark='hup'), k(.6, x=.6, y=.8, eye='o'), k(.82, x=.6, y=.6, eye='O')],
    [], g='use', act=('rock', 'body'), prefer=['happy', 'young'], obj=[(.4, dict(sway=.8)), (.6, dict(sway=-.7)), (.8, dict(sway=.5))])
o.r('spin_it_by_the_tail', "Hooking a wing round the tail point and dragging it round until the whole duck is turning on its base like a top", 20, 'wing',
    [k(.2, 'tail_tip', reach=.5, x=.8, y=1, b=.6), k(.4, 'tail_tip', reach=1, x=1.4, y=1.4, b=1, mark='hnn'), k(.6, 'tail_tip', reach=1, x=1.4, y=1.4, b=1, eye='@'), k(.85, x=.4, eye='O')],
    [], g='use', act=('spin', 'tail'), prefer=['curious', 'young'], obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.6)), (.85, dict(sway=.3))],
    say=["Round it goes. Stomachs hold. Yet.", "I spun a duck. Put that on my headstone."])

o.r('nod_it_by_the_bill', "Pushing the cheek down and letting go so the head bobs up and down like it agrees", 18, 'wing',
    [k(.15, 'cheek', reach=.6, x=.4, y=-.6), k(.35, 'cheek', reach=1, x=.7, y=-.4, b=.6, mark='nnh'), k(.5, x=-.8, y=-.4, eye='o'), k(.7, 'cheek', reach=1, x=.7, y=-.4, b=.6, mark='nnh'), k(.88, eye='^')],
    [], g='use', act=('push', 'cheek'), obj=[(.35, dict(sway=.4)), (.55, dict(sway=-.3)), (.75, dict(sway=.3))])
# --- play
o.r('race_round_and_slap', "Racing round the duck and slapping its flank at the end of every lap", 18, 'wing',
    [k(.15, x=-1.6, b=.8, eye='>'), k(.35, 'flank_l', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.55, 'belly_r', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.8, x=1.2, eye='^')],
    [], g='play', act=('race', 'duck'), prefer=['happy', 'young'], obj=[(.35, dict(sway=.2)), (.55, dict(sway=-.2))])
o.r('sumo_bump', "Belly-bumping the duck like a sumo wrestler, backing off and going in again", 18, 'none',
    [k(.2, 'belly_low', x=-1.4, y=.6, b=.6), k(.4, 'belly_low', x=2.4, y=.8, b=.8, mark='BUMP'), k(.6, x=-1.4, y=.6, b=.4), k(.8, 'belly_low', x=2.4, y=.8, b=.8, mark='BUMP')],
    [], g='play', act=('shove', 'belly'), prefer=['grumpy', 'happy'], obj=[(.4, dict(sway=.6, shake=.2)), (.8, dict(sway=.8, shake=.3))],
    say=["Sumo rules: bump, back up, bump. It lost on points.", "Belly to belly. Mine's the squishier opinion."])

o.r('boop_the_bill', "Booping the tip of its bill with his own and dodging back, daring it to boop back", 14, 'none',
    [k(.2, 'bill_tip', x=1.4, y=-.4, eye='o'), k(.4, 'bill_tip', x=2, y=-.4, mark='boop'), k(.6, x=-1.6, b=-1.6, eye='>'), k(.85, x=-.4, y=.4, eye='O', mark='...')],
    [], g='play', act=('nudge', 'bill'), ages=GROWN, prefer=['happy'])
o.r('hop_on_the_base_rim', "Hopping up onto the base rim and off again, higher each hop, at the duck's feet", 16, 'none',
    [k(.15, 'base_mid', perch=1, b=-.4), k(.3, 'base_mid', b=.6), k(.5, 'base_mid', perch=1, b=-1.6, w=.6, mark='hup'), k(.65, 'base_mid', b=.8), k(.82, 'base_mid', perch=1, b=-2.4, w=1, eye='^', mark='HUP'), k(.94, b=.6)],
    [], g='play', act=('hop', 'base'), prefer=['happy', 'young'])
o.r('chase_the_ripples', "Chasing the ripples round its base, stamping at each wave", 18, 'none',
    [k(.2, 'ripple_l', x=-.8, y=.6, l=1), k(.4, 'ripple_l', x=.8, y=.6, b=.6, r=1, mark='splt'), k(.6, 'ripple_r', x=.8, y=.6, b=.6, l=1, mark='splt'), k(.82, 'ripple_r', x=-.8, y=.4, eye='^')],
    [], g='play', act=('chase', 'ripples'), prefer=['happy', 'young'])
o.r('bounce_off_the_belly', "Leaping at the belly and bouncing off it backwards onto his tail", 16, 'none',
    [k(.2, x=-1.4, b=.8, eye='>'), k(.4, 'belly_mid', x=1.8, b=-2, w=1, mark='boing'), k(.6, x=-2.4, y=1.8, b=1.8, w=.5, eye='@', mark='whump'), k(.85, y=.4, eye='^')],
    [], g='play', act=('hop', 'belly'), prefer=['happy', 'young'], obj=[(.4, dict(sway=.4, puff=.3)), (.6, dict(sway=-.3))])
# --- test
o.r('find_where_the_squeak_lives', "Squeezing along the belly a little at a time to find the spot the squeak lives in", 24, 'wing',
    [k(.15, 'belly_low', reach=.5, x=.3), k(.3, 'belly_low', reach=.8, x=.6, mark='...'), k(.45, 'belly_mid', reach=.8, x=.6, mark='...'), k(.6, 'belly_r', reach=.9, x=.8, mark='...'), k(.75, 'chest_r', reach=1, x=.9, eye='O', mark='squk'), k(.9, eye='o')],
    [], g='test', act=('squeeze', 'squeak'), prefer=['curious'], obj=[(.75, dict(puff=.3))])
o.r('rap_the_cheek', "Rapping the cheek with his bill to find out whether the head is hollow", 14, 'none',
    [k(.2, 'cheek', x=.8, y=-.4, b=.4), k(.4, 'cheek', x=1.4, y=-.2, mark='tok'), k(.6, 'cheek', x=.8, y=-.4, b=.4), k(.8, 'cheek', x=1.4, y=-.2, mark='tok'), k(.92, eye='o')],
    [], g='test', act=('knock', 'head'), prefer=['curious'])
o.r('sniff_the_wing_mark', "Sniffing the mark on its side to find out what the smell of bath is made of", 16, 'wing',
    [k(.2, 'wing_mark', reach=.4, x=.6, y=.4), k(.45, 'wing_mark', reach=.6, x=1.4, y=.8, eye='o', mark='snf'), k(.65, 'wing_mark', reach=.6, x=1.4, y=.8, eye='O', mark='snf'), k(.85, eye='-')],
    [], g='test', act=('sniff', 'wing'), prefer=['curious'],
    say=["Rubber, bleach, someone's childhood, boiled.", "Smells like a bathroom. Not mine. I use the pond."])

o.r('tug_the_tail', "Tugging the tail point to see whether it comes off, and watching it not come off", 16, 'none',
    [k(.2, 'tail_tip', x=.8, y=.6, b=.6), k(.4, 'tail_tip', x=.4, y=1, b=1, w=.4, mark='hnn'), k(.6, x=-1.4, y=1.2, b=1.6, w=.6, mark='hnnng'), k(.8, eye='-')],
    [], g='test', act=('tug', 'tail'), obj=[(.5, dict(shake=.2))])
o.r('stare_into_the_eye', "Staring into its eye from a wing's width away to see who blinks first", 20, 'wing',
    [k(.2, 'eye_spot', reach=.4, x=.6, eye='o'), k(.45, 'eye_spot', reach=.6, x=1.4, eye='O', mark='...'), k(.7, 'eye_spot', reach=.6, x=1.4, eye='O', mark='...'), k(.88, x=0, eye='-')],
    [], g='test', act=('test', 'eye'), prefer=['curious', 'grumpy'],
    say=["It never blinked. Painted open. Cheating.", "Won on a technicality. The technicality's rubber."])

o.r('taste_the_bill', "Licking the belly once to find out whether rubber has any flavour", 14, 'none',
    [k(.2, 'belly_r', x=1, y=-.4), k(.4, 'belly_r', x=2, y=-.2, eye='o', mark='chew'), k(.6, 'belly_r', x=2, y=-.2, eye='O', mark='chew'), k(.82, x=-1.4, y=-1.8, eye='@', mark='ptoo')],
    [], g='test', act=('taste', 'belly'))
# --- rest
o.r('doze_against_the_belly', "Dozing with his head laid against the low curve of the belly, rising and falling with the squeak of its air", 30, 'none',
    [k(.2, 'belly_low', x=.6, y=.8, b=.6), k(.45, 'belly_low', x=.8, y=1.8, b=1.6, eye='-'), k(.75, 'belly_low', x=.8, y=1.8, b=1.8, eye='-', mark='zzz'), k(.9, y=.2, eye='^')],
    [(.45, 'snooze')], g='rest', act=('nap', 'belly'), prefer=['tired', 'night'])
o.r('bask_on_the_warm_rubber', "Pressing his chest to the sun-warmed rubber until the chill goes out of his feathers", 24, 'none',
    [k(.2, 'belly_r', x=.4, y=.6, b=.4), k(.45, 'belly_r', x=.8, y=1.2, b=1, eye='-'), k(.75, 'belly_r', x=1.4, y=1.8, b=1.6, eye='-', mark='ahh'), k(.9, y=0, eye='^')],
    [(.45, 'snooze')], g='rest', act=('warm', 'belly'), when=['heat>.4'], prefer=['cold', 'tired'],
    say=["Warm rubber. Better than a bed. Smells like one, too.", "Thawing against a duck. Tell no one."])

o.r('sit_on_the_base_rim', "Sitting up on the base rim beside the tail with his back to the duck, watching the yard", 26, 'none',
    [k(.2, 'base_l', perch=1, b=.4, x=-.4), k(.45, 'base_l', perch=1, b=1, x=-1.4, y=-1.8, eye='o'), k(.75, 'base_l', perch=1, b=1, x=-1.8, y=-1.8, eye='-', mark='mm'), k(.9, 'base_l', perch=1, b=.4, eye='^')],
    [], g='rest', act=('perch', 'base'), prefer=['tired', 'lonely'])
# --- show
o.r('claim_to_be_the_real_one', "Lecturing the duck's neck, squared up, that he is the real duck here and it is a toy", 22, 'none',
    [k(.2, 'neck_front', x=1.4, y=-.4, eye='>'), k(.4, 'neck_front', x=1.8, y=-.2, mark='QUACK'), k(.6, 'neck_back', x=1.4, y=-.2, eye='>', mark='quack'), k(.85, x=-.8, eye='-', mark='hmph')],
    [], g='show', act=('argue', 'neck'), ages=GROWN, prefer=['grumpy'],
    say=["I'm the real one. I tire and have opinions.", "It squeaked at me. First one to disagree in a week."])

o.r('belly_duet', "Squeezing out a belly note and quacking back at it, then again, a higher one", 22, 'wing',
    [k(.15, 'belly_mid', reach=.6, x=.3), k(.3, 'belly_mid', reach=1, x=.8, b=.6, mark='squk'), k(.5, x=-.6, y=-1.8, eye='^', mark='QUACK'), k(.7, 'belly_low', reach=1, x=.8, b=.6, mark='SQUK'), k(.88, eye='^', x=.4)],
    [(.3, 'company')], g='show', act=('sing', 'belly'), prefer=['happy'], obj=[(.3, dict(puff=.3)), (.7, dict(puff=.4, sway=.2))])
o.r('match_its_pose', "Standing beside the duck with his chest out and his bill tilted at exactly its angle", 20, 'none',
    [k(.2, 'chest_r', x=-.4, y=-.4), k(.45, 'chest_r', x=-1.4, y=-1.8, b=.6, w=.4, eye='^'), k(.7, 'chest_r', x=-1.8, y=-2, b=.8, w=.6, eye='-', mark='...'), k(.9, eye='^')],
    [], g='show', act=('pose', 'chest'), prefer=['happy', 'grown'])
o.r('shake_the_bill_like_a_hand', "Shaking the tip of its bill like a handshake and telling it he is very pleased to meet it", 18, 'wing',
    [k(.15, 'bill_tip', reach=.5, x=.4, y=-.4), k(.35, 'bill_tip', reach=1, x=.8, y=-.4, b=-.6, mark='how do'), k(.55, 'bill_tip', reach=1, x=.8, y=-.4, b=.6), k(.75, 'bill_tip', reach=1, x=.8, y=-.4, b=-.6), k(.9, eye='^')],
    [], g='show', act=('shake', 'bill'), ages=GROWN, obj=[(.35, dict(sway=.3)), (.55, dict(sway=-.3)), (.75, dict(sway=.3))],
    say=["Pleased to meet you. Nice grip. No blood flow.", "It didn't give its name. Rude, or brief."])

o.r('critic_circle', "Circling the duck with one eye shut like an art critic judging its proportions", 24, 'none',
    [k(.15, 'tail_tip', x=.6, y=.2, eye='o'), k(.35, 'flank_l', x=.8, y=-.6, eye='-'), k(.55, 'belly_low', x=.8, y=.6, eye='o', mark='hm'), k(.75, 'belly_r', x=.6, y=.4, eye='-', mark='mm'), k(.9, 'chest_r', x=.4, eye='^')],
    [], g='show', act=('compare', 'proportions'), prefer=['curious', 'grown'],
    say=["Too round, too yellow, too confident. Four stars.", "Excellent bill, dreadful tail. Critics will talk."])

# --- mishap
o.r('overreached_for_the_crest', "Stretching a twig up toward the crest, overbalancing, and sitting down hard on his tail", 18, 'twig',
    [k(.15, 'crest', reach=.6, y=-.6, x=.3), k(.4, 'crest', reach=1, x=1.2, y=-1.8, b=-.6, mark='nnf'), k(.6, 'crest', reach=1, x=-1.8, y=-2, b=.4, eye='O'), k(.78, x=-2.4, y=1.8, b=2, eye='@', mark='WHUMP'), k(.92, y=.6, eye='-')],
    [], g='mishap', act=('prod', 'crest'), prefer=['young'], obj=[(.4, dict(sway=.3)), (.78, dict(shake=.3))],
    say=["Reached the crest. Almost. My arse got there first.", "Twig, balance, gravity. Gravity's a sore winner."])

o.r('weigh_it_at_the_base', "Pressing his shoulder against the base rim to learn how heavy the duck really is", 16, 'none',
    [k(.2, 'base_r', x=-.8, y=.6, b=.6), k(.4, 'base_r', x=1.6, y=.8, b=1, mark='hnng'), k(.6, 'base_r', x=1.8, y=.8, b=1.4, eye='>'), k(.85, eye='-')],
    [], g='test', act=('weigh', 'base'), obj=[(.4, dict(sway=.2)), (.6, dict(sway=0))])
o.r('ear_to_the_belly', "Laying his ear against the belly, a wing braced beside it, and listening for where the squeak echoes", 20, 'wing',
    [k(.2, 'belly_mid', reach=.5, x=.4, y=.6, b=.4), k(.4, 'belly_mid', reach=.8, x=-.4, y=1.8, b=1.4, eye='-', mark='...'), k(.7, 'belly_mid', reach=.8, x=-.4, y=1.8, b=1.8, eye='o', mark='...'), k(.88, eye='-')],
    [], g='test', act=('listen', 'belly'), prefer=['curious'],
    say=["Hollow in there. Echoes. Reminds me of me.", "Something rattles. Something always rattles."])

o.r('frame_the_portrait', "Framing the duck between his wings like a photographer and nodding at the shot", 18, 'none',
    [k(.2, x=-.8, y=-.4, w=.6), k(.4, x=-1.4, y=-1.8, w=1, eye='o', mark='hold it'), k(.6, x=-1.4, y=-1.8, w=1, b=.6, eye='^', mark='click'), k(.82, x=-.4, w=.4, eye='-')],
    [], g='show', act=('show', 'duck'), prefer=['curious', 'happy'])
o.r('hug_the_duck', "Wrapping both wings round the duck's chest and holding on, cheek against the rubber", 24, 'wing',
    [k(.2, 'chest_r', reach=.5, x=.4, y=.4), k(.45, 'chest_r', reach=1, x=.9, y=.8, b=.4, eye='-'), k(.75, 'chest_r', reach=1, x=.9, y=.8, b=.4, eye='-', mark='mm'), k(.9, reach=.2, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'chest'), when=['lonely'],
    say=["It squeaks when you hold it. Nicest thing said to me today.", "Research. A hug. A toy. For science."])

o.r('shoved_the_neck_and_took_the_nod', "Shoving the front of the neck to make it nod, and taking the head's bounce back across his beak", 18, 'none',
    [k(.2, 'neck_front', x=.8, y=.4), k(.4, 'neck_front', x=1.8, y=.6, b=.6, mark='hup'), k(.6, x=-1.8, y=1.8, b=1.4, w=.6, eye='@', mark='tonk'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('shove', 'neck'), prefer=['grumpy'], obj=[(.4, dict(sway=.6)), (.55, dict(sway=-.6, shake=.2))],
    say=["It nodded back. Harder. Better swing than mine.", "That's a head with a grudge."])

o.r('rain_drumming_on_its_head', "Laying his ear against the back of the neck while the rain drums the head above it, listening to it ring", 22, 'wing',
    [k(.2, 'neck_back', reach=.5, x=.4, y=-.4), k(.4, 'neck_back', reach=1, x=-.4, y=-1.8, b=.6, eye='-', mark='...'), k(.7, 'neck_back', reach=1, x=-.4, y=-2, b=1.2, eye='o', mark='...'), k(.88, eye='-')],
    [], g='weather', act=('listen', 'head'), when=['obj_wetness>.3'], prefer=['curious'],
    say=["Rain on a rubber head. A drum with a punchline.", "Sounds like thinking. Mine, usually."])
o.emit(need=38)
