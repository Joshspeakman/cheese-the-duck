"""Wave 1 v3 repertoire: tire_swing, toy_seesaw, birdhouse, rubber_duck, toy_sandbox, dog_house, toy_car, gazebo.
Every routine is written out by hand under the v3 rules (parts table from each blueprint, marks on visible fields, stricter same-act, stock and inspecting caps,
verb in label, buildings sway <= .15, perched acts and duets where the drawing allows). Each drawing was printed with rep.py first; the heights and parts are in the comments."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN

# ============================================================ tire_swing
# Blueprint: type 'tire' (playground-workshop): a tall post on the left with bolts down its face, a slanting arm out from its top,
# a rope hanging from the arm, a tyre ring (22-168 px) with a hole through the middle (lip at ~58 px). Riding it is native; none of these ride it.
# The whole sprite is 488 px tall, so a push only ever moves it a little (sway <= .15).
o = Obj('tire_swing', 'placed',
        parts=dict(post='the tall painted post, bolts down its face', plate='the flat base plate at the post foot', beam='the slanting arm out from the post top',
                   rope='the rope hanging from the arm', tyre='the rubber tyre ring with its walls, flanks and belly', hole='the hole through the middle of the tyre'),
        fields=dict(twist=(0, 0, 1), frost=(0, 0, 1), leaves=(0, 0, 1)),
        physics=[('twist', 'rate', -.0004, 'always'), ('twist', 'rate', .003, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm'),
                 ('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrape=[('obj.dirt', 'add', -.2)], fluff=[('need.cleanliness', 'add', 1)],
            chip=[('frost', 'mul', .2)], dry=[('obj.wetness', 'add', -.4)], scuff=[('obj.condition', 'add', -.25)], patch=[('obj.condition', 'add', .4)],
            unkink=[('twist', 'mul', .1)], wind=[('twist', 'add', .5)], catch=[('twist', 'mul', .2)], unwound=[('twist', 'set', 0)],
            company=[('need.social', 'add', 2)], sweep=[('leaves', 'set', 0)], snooze=[('need.energy', 'add', 3)], giggle=[('need.fun', 'add', 2)]),
        anchors=dict(post_base=(.148, .959, 'surface'), post_low=(.148, .892), post_mid=(.148, .824),
                     tyre_tip=(.506, .919), tyre_belly_l=(.444, .905), tyre_belly_r=(.58, .905),
                     tyre_flank_l=(.383, .892), tyre_flank_r=(.63, .892), tyre_wall_l=(.333, .865), tyre_wall_r=(.679, .865),
                     tyre_side_l=(.309, .838), tyre_side_r=(.704, .838),
                     hole_lip=(.506, .851, 'surface'), hole_edge_l=(.42, .811), hole_edge_r=(.593, .811), rope_foot=(.506, .635)),
        marks=[('frost', .3, '*.*.*', 'tyre_wall_l', 'frost'), ('leaves', .3, ',;,.;', 'post_base', 'leaf')])
S = dict(sway=.12)
# --- care
o.r('wipe_flank_clean', "Giving the tyre's flank a long wipe with a wing to lift dried mud, left rim to right", 16, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.4, y=.6), k(.35, 'tyre_flank_l', reach=1, x=.8, y=.6, b=.6, mark='skrk'), k(.6, 'tyre_flank_r', reach=1, x=.8, y=.6, b=.6, mark='skrk'), k(.85, eye='^')],
    [(.6, 'wipe')], g='care', act=('wipe', 'flank'), when=['obj_dirt>.3'], obj=[(.35, dict(sway=.1)), (.6, dict(sway=-.1))],
    say=["Wiped the flank. Mud, meet wing. Wing, meet regret.", "It's cleaner. It still hangs there like a dare."])
o.r('scrape_the_tread', "Scraping caked mud out of the tread along the tyre's bottom edge with his bill", 16, 'none',
    [k(.2, 'tyre_tip', x=.6, y=1.6, b=1.2), k(.4, 'tyre_tip', x=1.8, y=1.8, b=1.4, r=1, mark='tk'), k(.6, 'tyre_belly_l', x=1.8, y=1.8, b=1.4, l=1, mark='tk'), k(.8, 'tyre_belly_r', x=1.8, y=1.8, b=1.4, r=1, mark='tk'), k(.92, y=.6, eye='^')],
    [(.6, 'scrape')], g='care', act=('scrape', 'tread'), when=['obj_dirt>.3'], obj=[(.4, dict(shake=.1))],
    say=["Scraped the muck out. There's a lot of muck. It will return.", "Clean tread. Only my conscience has improved."])
o.r('fluff_up_on_the_wall', "Fluffing his ruffled feathers by dragging each side along the tyre's rough wall in turn", 18, 'none',
    [k(.2, 'tyre_wall_l', x=-.8, y=.5, w=.4), k(.4, 'tyre_wall_l', x=-1.4, y=.6, b=.6, w=1, mark='fff'), k(.6, 'tyre_wall_r', x=-1.4, y=.6, b=.6, w=1, mark='fff'), k(.82, eye='^', w=.4)],
    [(.6, 'fluff')], g='care', act=('fluff', 'feathers'), prefer=['grumpy'],
    say=["Rubbed my sides on a tyre. Feel groomed. Smell of garage.", "Magnificent again. The tyre's a good sport, being rubber."])
o.r('sweep_leaves_from_the_plate', "Sweeping the leaves drifted round the post's base plate out toward the tyre with a wing", 18, 'wing',
    [k(.15, 'post_base', reach=.5, x=.3, y=.6), k(.4, 'post_base', reach=1, x=1.6, y=1.8, b=1.2, mark='fshh'), k(.62, 'post_base', reach=1, x=-1.2, y=1.8, b=1.4, l=1, mark='fshh'), k(.85, y=.6, eye='^')],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'])
o.r('patch_the_scuffed_wall', "Mending the scuffed rubber by pressing a peeled flap flat against the tyre's wall with a wing", 20, 'wing',
    [k(.15, 'tyre_wall_r', reach=.4, x=.4, y=.6), k(.4, 'tyre_wall_r', reach=1, x=1, y=1, b=.8, mark='prss'), k(.62, 'tyre_side_r', reach=1, x=1, y=.8, b=.8, mark='prss'), k(.85, reach=.1, eye='^')],
    [(.62, 'patch')], g='care', act=('mend', 'wall'), when=['obj_condition<.6'], obj=[(.4, dict(shake=.1))],
    say=["Pressed the flap back down. Held. For now. Like most promises.", "Mended it. Don't ask what with. Spit, mostly."])
# --- weather
o.r('chip_frost_off_the_tyre', "Chipping the frost off the tyre's side with the edge of his bill, working up the flank", 20, 'none',
    [k(.2, 'tyre_belly_l', x=.8, y=.8, b=.6), k(.4, 'tyre_flank_l', x=1.4, y=1, b=.8, mark='tik'), k(.6, 'tyre_wall_l', x=1.4, y=.8, b=.6, mark='tik'), k(.8, 'tyre_wall_l', x=1.4, y=.8, b=.2, mark='tik'), k(.92, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'tyre'), when=['frost>.3'], obj=[(.4, dict(shake=.1)), (.6, dict(shake=.1))],
    say=["Frost's off. The tyre looks thawed or insulted, hard to tell.", "My bill's gone numb. It chipped what I couldn't feel."])
o.r('rub_the_wet_tyre_dry', "Backing up to the damp tyre and rubbing its flank dry with his tail feathers", 18, 'none',
    [k(.2, 'tyre_flank_r', x=-.8, y=.6, b=.6), k(.4, 'tyre_flank_r', x=-1.4, y=.8, b=.8, w=.6, mark='fff'), k(.62, 'tyre_wall_r', x=-1.4, y=.8, b=.8, w=1, mark='fff'), k(.85, eye='^', w=.4)],
    [(.62, 'dry')], g='weather', act=('dry', 'tyre'), when=['obj_wetness>.3'],
    say=["Dried it with my arse. The towel was busy being absent.", "Flank's dry. My tail feathers are now a sponge."])
o.r('straighten_the_gale_twist', "Straightening the wind's twist out of the rope by walking the tyre back round at its sides", 22, 'wing',
    [k(.15, 'tyre_side_l', reach=.5, x=.4, y=.6), k(.35, 'tyre_side_l', reach=1, x=.9, y=.6, b=.6, mark='hnng'), k(.55, 'tyre_side_r', reach=1, x=.9, y=.6, b=.6, mark='hnng'), k(.8, eye='^')],
    [(.55, 'unkink')], g='weather', act=('straighten', 'rope'), when=['twist>.4'], obj=[(.35, dict(sway=.1)), (.55, dict(sway=-.1))],
    say=["Untwisted the rope. The wind's furious. Good.", "Tyre hangs straight. I'm taking credit."])
o.r('catch_the_whipped_tyre', "Catching the wind-whipped tyre by its rim and bracing both feet until it stops dead", 16, 'none',
    [k(.2, 'tyre_flank_r', x=-.4, y=.4, b=.4, eye='o'), k(.4, 'tyre_flank_r', x=1.6, y=.8, b=1, l=1, r=1, mark='skrrk'), k(.65, 'tyre_flank_r', x=1.6, y=.8, b=1, eye='-'), k(.85, y=.2, eye='^')],
    [(.4, 'catch')], g='weather', act=('catch', 'tyre'), when=['twist>.4'], obj=[(.2, dict(shake=.12)), (.4, dict(shake=.15)), (.7, dict(sway=0))])
o.r('brace_against_the_gust', "Bracing his back against the post while a gust sets the tyre jittering on its rope", 24, 'none',
    [k(.2, 'post_low', x=-.4, y=.2, b=.4), k(.4, 'post_low', x=-1.4, y=.6, b=1.6, w=.6, eye='>', mark='fff'), k(.7, 'post_low', x=-2.2, y=1.6, b=2.4, w=1, l=1, eye='>'), k(.9, y=0, eye='^')],
    [], g='weather', act=('brace', 'post'), when=['windy'], obj=[(.3, dict(sway=.12)), (.5, dict(sway=-.12)), (.7, dict(sway=.12))],
    say=["Gust hit. I held the post. The post held me. Fair trade.", "Wind's got a grudge against my feathers."])
# --- use
o.r('push_for_a_missing_friend', "Pushing the empty tyre again and again, a little harder each time, the way you would for a friend", 24, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.4, y=.6), k(.3, 'tyre_flank_l', reach=1, x=.7, y=.6, b=.6), k(.5, 'tyre_flank_l', reach=1, x=1.1, y=.8, b=.8, mark='hup'), k(.7, 'tyre_flank_l', reach=1, x=1.6, y=1, b=1, mark='HUP'), k(.88, eye='-', x=-.4, y=.2)],
    [(.7, 'company')], g='use', act=('push', 'tyre'), when=['lonely'], obj=[(.3, dict(sway=.08)), (.5, dict(sway=.12)), (.7, dict(sway=.15)), (.88, dict(sway=-.1))],
    say=["Pushed it harder each time. It didn't giggle. High standards.", "That's more swing than I've had from a friend."])
o.r('heave_the_edge_up', "Lifting the tyre's low edge up on its rope and letting it flop back with a thump", 16, 'wing',
    [k(.15, 'tyre_tip', reach=.5, y=.6, b=.6), k(.35, 'tyre_tip', reach=1, y=-.2, b=-.6, mark='hng'), k(.55, x=-1.2, y=1.2, b=.6, eye='-'), k(.75, eye='^', mark='thunk')],
    [], g='use', act=('lift', 'tyre'), ages=GROWN, obj=[(.35, dict(sway=.1)), (.6, dict(sway=-.1, shake=.1))])
o.r('hook_the_rope_with_a_twig', "Hooking the rope with a twig and hauling the tyre out sideways before letting go", 24, 'twig',
    [k(.15, 'rope_foot', reach=.6, y=-.5, x=.3), k(.4, 'rope_foot', reach=1, x=1.2, y=-.8, b=.6, mark='hnf'), k(.6, 'rope_foot', reach=1, x=1.5, y=-.8, b=.6, l=1), k(.78, x=-1.2, y=.6, eye='O')],
    [], g='use', act=('hook', 'rope'), ages=GROWN, obj=[(.4, dict(sway=.1)), (.6, dict(sway=.15)), (.8, dict(sway=-.12))])
o.r('peer_out_through_the_ring', "Pushing his head into the hole to peer out at the yard through the ring", 16, 'none',
    [k(.2, 'hole_lip', x=.6, y=.8, b=.6), k(.45, 'hole_edge_l', x=1.6, y=1.6, b=.8, eye='o', mark='hm'), k(.7, 'hole_edge_l', x=1.8, y=1.8, b=.8, eye='O'), k(.88, x=0, eye='-')],
    [], g='use', act=('peer', 'hole'), shown='head', prefer=['curious'])
o.r('tug_the_rim_toward_him', "Tugging the tyre's rim toward him with his bill and letting it snap back", 14, 'none',
    [k(.2, 'tyre_belly_r', x=.8, y=.8, b=.6), k(.4, 'tyre_belly_r', x=-1.4, y=1.2, b=.8, mark='hnn'), k(.6, x=.4, y=.6, eye='o', mark='...'), k(.8, 'tyre_belly_r', x=1.4, y=.8, b=.6, mark='twang')],
    [], g='use', act=('tug', 'tyre'), obj=[(.4, dict(sway=-.1)), (.6, dict(sway=.12)), (.8, dict(sway=-.1))])
o.r('push_the_tyre_round_to_wind_up', "Pushing the tyre round at its walls to wind the rope up tight", 22, 'wing',
    [k(.15, 'tyre_wall_r', reach=.5, x=.5, y=.6), k(.35, 'tyre_wall_r', reach=1, x=.9, b=.6, l=1, mark='hnnng'), k(.55, 'tyre_wall_l', reach=1, x=.9, b=.6, r=1, mark='hnnng'), k(.8, x=-1.2, y=1.2, eye='O')],
    [(.55, 'wind')], g='use', act=('push', 'rope'), when=['twist<.6'], prefer=['curious'], obj=[(.35, dict(sway=.1)), (.55, dict(sway=.12, shake=.1))])
o.r('shove_a_friend_in_the_ring', "Shoving the tyre with a friend sat in its hole, a little higher each time", 26, 'wing',
    [k(.15, 'tyre_belly_l', reach=.6, x=.4, y=.4), k(.3, 'tyre_belly_l', reach=1, x=.8, b=.6, mark='hup'), k(.55, 'tyre_belly_l', reach=1, x=1.2, b=.8, mark='HUP'), k(.8, x=-.4, y=-.4, eye='^', mark='ha')],
    [(.55, 'giggle')], g='use', act=('shove', 'ring'), ages=GROWN, obj=[(.3, dict(sway=.1)), (.55, dict(sway=.15)), (.8, dict(sway=-.12))],
    duo=[k(.15, 'tyre_tip', x=.4, y=.4, eye='o'), k(.3, 'hole_lip', perch=1, x=-.4, w=.4), k(.55, 'hole_lip', perch=1, x=-.4, w=1, eye='^', mark='wheee'), k(.8, 'hole_lip', perch=1, x=-.2, w=.4, eye='^')],
    say=["Shoved a friend in the tyre. The friend is the cargo. I am the engine.", "Higher? Higher. Their screaming is technically positive feedback."])
# --- play
o.r('shove_and_flatten', "Shoving the tyre off at arm's length and flattening himself as it sails back past", 18, 'wing',
    [k(.15, 'tyre_wall_l', reach=.6, x=.3, y=.6), k(.3, 'tyre_wall_l', reach=1, x=.8, b=-1.6, mark='hup'), k(.5, x=.2, y=1.6, b=1.6, eye='O'), k(.7, x=.2, y=1.6, b=1.6, eye='-', mark='whoosh'), k(.88, eye='^')],
    [], g='play', act=('shove', 'tyre'), prefer=['happy'], obj=[(.3, dict(sway=.1)), (.45, dict(sway=.15)), (.6, dict(sway=-.15)), (.75, dict(sway=.08))])
o.r('poke_and_run', "Nudging the tyre's bottom tip and sprinting away before it can come back round", 14, 'none',
    [k(.2, 'tyre_tip', x=1.4, y=.8, b=.6, mark='boop'), k(.4, x=-1.4, b=-1.6, w=1, eye='>'), k(.6, x=-2, l=1, b=-1.6, eye='>'), k(.85, x=-.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('nudge', 'tyre'), prefer=['grumpy', 'young'], obj=[(.25, dict(sway=.1)), (.6, dict(sway=-.1))],
    say=["Poked. Ran. It's coming. They always come back.", "I'm not scared. I'm tactically elsewhere."])
o.r('pat_the_tyre_on_its_return', "Pushing the tyre away, then patting its flank as it comes back, like a high five from something with no hands", 20, 'wing',
    [k(.15, 'tyre_side_l', reach=.6, x=.3), k(.3, 'tyre_side_l', reach=1, x=.7, b=.4, mark='hup'), k(.5, x=-.4, w=.4, eye='o'), k(.68, 'tyre_belly_r', reach=1, x=.9, y=.4, b=-.6, mark='SLAP'), k(.85, eye='^')],
    [], g='play', act=('pat', 'tyre'), prefer=['happy'], obj=[(.3, dict(sway=.1)), (.5, dict(sway=-.1)), (.68, dict(sway=.08))])
o.r('hide_round_the_post', "Hide and seek round the post's edge, popping out at the tyre each time it swings by", 20, 'none',
    [k(.2, 'post_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'post_mid', x=1.4, y=0, eye='O'), k(.6, 'post_low', x=-1.2, y=.8, b=.6, eye='o'), k(.8, 'post_low', x=1.4, y=0, eye='O', mark='ha')],
    [], g='play', act=('hide', 'post'), prefer=['curious', 'young'], obj=[(.2, dict(sway=.1)), (.5, dict(sway=-.1)), (.8, dict(sway=.08))])
o.r('hop_up_and_bump_the_tyre', "Hopping up at the tyre's low edge and bumping it with his chest, a bit higher each time", 18, 'none',
    [k(.15, 'tyre_tip', x=.4, b=.6), k(.3, 'tyre_tip', x=1.4, y=.5, b=-1.6, mark='bump'), k(.5, 'tyre_belly_l', x=1.4, y=.5, b=-2, w=.6, mark='BUMP'), k(.7, 'tyre_belly_l', x=1.8, y=.5, b=-2.4, w=1, mark='BUMP'), k(.88, x=0, eye='^')],
    [], g='play', act=('hop', 'tyre'), prefer=['happy', 'young'], obj=[(.3, dict(sway=.08)), (.5, dict(sway=.1)), (.7, dict(sway=.15))])
o.r('race_the_tyre_to_the_post', "A race with the tyre: shoving it off, sprinting to the post and back before it finishes its swing", 20, 'none',
    [k(.15, 'tyre_flank_l', x=.8, y=.4, b=.4), k(.3, x=-1.6, b=-1.6, w=1, eye='>'), k(.5, 'post_low', x=1.4, b=-1.6, l=1, eye='>', mark='TAG'), k(.72, x=1.6, b=-1.6, r=1, eye='>'), k(.88, x=.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('race', 'tyre'), prefer=['happy'], obj=[(.15, dict(sway=.12)), (.5, dict(sway=-.12)), (.75, dict(sway=.1))])
o.r('dance_with_the_tyre', "Dancing a slow waltz with the tyre, one wing on its wall, leading it round with every step", 24, 'wing',
    [k(.15, 'tyre_wall_l', reach=.5, x=.2), k(.35, 'tyre_wall_l', reach=1, x=.6, y=-.4, b=.4, l=1, mark='one'), k(.55, 'tyre_side_l', reach=1, x=-.4, y=-.4, b=.4, r=1, mark='two'), k(.75, 'tyre_wall_l', reach=1, x=.6, y=-.4, b=.4, l=1, mark='three'), k(.9, reach=.2, eye='^')],
    [], g='play', act=('dance', 'tyre'), prefer=['happy'], obj=[(.35, dict(sway=.1)), (.55, dict(sway=-.1)), (.75, dict(sway=.1))],
    say=["Waltzed with a tyre. It led. I let it. No comment.", "One two three, one two three. Rubber has no rhythm."])
o.r('pass_the_tyre_back_and_forth', "Catching the tyre off a friend's pat and sending it back, over and over", 24, 'wing',
    [k(.15, 'tyre_wall_r', reach=.5, x=.4), k(.3, 'tyre_wall_r', reach=1, x=.8, b=.4, mark='hup'), k(.5, x=-.4, w=.4, eye='o'), k(.7, 'tyre_wall_r', reach=1, x=.8, b=.4, mark='hup'), k(.88, eye='^')],
    [], g='play', act=('catch', 'wall'), ages=GROWN, obj=[(.3, dict(sway=.1)), (.5, dict(sway=-.1)), (.7, dict(sway=.1))],
    duo=[k(.15, 'tyre_wall_l', reach=.4, x=.2), k(.4, x=-.4, w=.4, eye='o'), k(.5, 'tyre_side_l', reach=1, x=.8, b=.4, mark='PAT'), k(.8, eye='^', w=.6)],
    say=["Passed it to a friend, got it back. Best conversation I've had all week.", "We said nothing and the tyre did all the talking."])
# --- test
o.r('knock_for_hollow', "Knocking on the tyre's wall twice with his bill to hear what is inside it", 14, 'none',
    [k(.2, 'tyre_wall_r', x=.8, y=.5, b=.6), k(.4, 'tyre_wall_r', x=1.6, y=.5, mark='tok'), k(.6, 'tyre_wall_r', x=.8, y=.5, b=.6), k(.78, 'tyre_wall_r', x=1.6, y=.5, mark='tok'), k(.9, x=-.4, y=-1.6, eye='o')],
    [], g='test', act=('knock', 'wall'), prefer=['curious'], obj=[(.4, dict(shake=.1)), (.78, dict(shake=.1))])
o.r('weigh_the_tyre', "Weighing the tyre by pressing a wing against its belly to feel how heavy it hangs", 16, 'wing',
    [k(.2, 'tyre_belly_r', reach=.5, x=.5, y=.6), k(.45, 'tyre_belly_r', reach=1, x=1.1, y=.6, b=.8, eye='>', mark='hnng'), k(.7, 'tyre_belly_r', reach=1, x=1.4, y=.8, b=1, mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('weigh', 'belly'), obj=[(.45, dict(sway=.1)), (.7, dict(sway=.06))])
o.r('measure_up_to_the_tyre', "Standing flank to flank with the tyre and measuring a wing along both to see who is taller", 20, 'wing',
    [k(.15, 'tyre_side_r', reach=.4, x=-.4, y=-.2), k(.4, 'tyre_side_r', reach=1, x=.2, y=-1.8, b=.4, mark='hm'), k(.65, 'tyre_side_r', reach=1, x=.2, y=-1.8, b=.8, eye='^', mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('measure', 'tyre'), prefer=['curious', 'young'])
o.r('count_the_swings', "Giving the tyre one push and counting its swings out loud until it comes to a stop", 24, 'wing',
    [k(.15, 'tyre_flank_r', reach=.6, x=.4, y=.4), k(.3, 'tyre_flank_r', reach=1, x=.9, b=.4, mark='hup'), k(.5, x=-.4, y=-1.8, eye='o', mark='one two'), k(.75, x=-.4, y=-1.8, eye='@', mark='...four'), k(.9, y=.2, eye='-')],
    [], g='test', act=('count', 'swings'), prefer=['curious'], obj=[(.3, dict(sway=.1)), (.45, dict(sway=-.08)), (.6, dict(sway=.06)), (.8, dict(sway=-.04))],
    say=["Seven swings, then it stopped. So did my interest.", "Counted aloud. The tyre didn't thank me."])
o.r('lick_the_tread', "Tasting the tread with one lick to find out what a road tastes like", 14, 'none',
    [k(.2, 'tyre_belly_l', x=.6, y=.6, b=.6), k(.4, 'tyre_belly_l', x=1.6, y=1.4, b=.8, eye='o', mark='lick'), k(.65, 'tyre_belly_r', x=-1.4, y=-1.8, eye='@', mark='ptoo'), k(.85, x=0, eye='-')],
    [], g='test', act=('taste', 'tread'),
    say=["Road, rain and a bit of dog. Zero bread.", "Tastes how it looks. Like going nowhere, gently."])
o.r('balance_on_the_base_plate', "Balancing on one foot on the post's base plate while the tyre swings past, then switching feet", 22, 'none',
    [k(.15, 'post_base', perch=1, x=.2, y=.4), k(.35, 'post_base', perch=1, x=.4, y=.4, b=.4, l=1, w=1, eye='o'), k(.6, 'post_base', perch=1, x=-.4, y=.4, b=.6, r=1, w=1, eye='O', mark='whoa'), k(.85, 'post_base', perch=1, x=0, eye='^')],
    [], g='test', act=('balance', 'plate'), prefer=['young', 'happy'], obj=[(.3, dict(sway=.1)), (.6, dict(sway=-.1))],
    say=["Four seconds on one foot. Write it down.", "One foot, one plate, zero dignity. Ten out of ten."])
# --- rest
o.r('lean_against_the_post', "Leaning his back against the post with his chin up and his eyes half shut", 22, 'none',
    [k(.2, 'post_low', x=-.4, y=.2, b=.4), k(.4, 'post_low', x=-1.4, y=-1.8, b=1.6, eye='-', w=.4), k(.7, 'post_low', x=-1.8, y=-1.8, b=2, w=1, eye='-', mark='mm'), k(.9, y=0, eye='^')],
    [], g='rest', act=('lean', 'post'), prefer=['tired'])
o.r('chin_on_the_rim', "Leaning his chin on the tyre's low rim, eyes half shut, while it drifts gently", 22, 'none',
    [k(.2, 'tyre_flank_r', x=.4, y=.6, b=.6), k(.4, 'tyre_flank_r', x=1.5, y=1.8, b=1.6, eye='-'), k(.7, 'tyre_flank_r', x=1.8, y=2.4, b=2, eye='-', mark='mm'), k(.9, y=.2, eye='^')],
    [], g='rest', act=('lean', 'rim'), prefer=['tired', 'sad'], obj=[(.4, dict(sway=.06)), (.7, dict(sway=-.06))])
o.r('hug_the_tyre', "Wrapping both wings round the tyre's side and holding on with his cheek against the rubber", 24, 'wing',
    [k(.2, 'tyre_side_l', reach=.5, x=.8, y=1.2, b=.6), k(.45, 'tyre_side_l', reach=1, x=1.4, y=1.8, b=1.2, eye='-'), k(.75, 'tyre_side_l', reach=1, x=1.8, y=2, b=1.6, eye='-', mark='mm'), k(.9, reach=.2, y=.6, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'tyre'), when=['lonely'],
    say=["Hugged a tyre. It was warmer than expected. So's my face.", "Don't ask what I whispered into it."])
o.r('nap_curled_in_the_hole', "Curling up on the hole's lip to nap with his bill tucked under a wing", 28, 'none',
    [k(.2, 'hole_lip', perch=1, x=.4, y=.8, b=.6), k(.4, 'hole_lip', perch=1, y=1.4, b=1.2, eye='-'), k(.7, 'hole_lip', perch=1, y=1.5, b=1.2, eye='-', mark='zzz'), k(.9, y=.2, b=.3, eye='^')],
    [(.4, 'snooze')], g='rest', act=('nap', 'hole'), ages=GROWN, prefer=['tired', 'night'], obj=[(.4, dict(sway=.06)), (.7, dict(sway=-.06))],
    say=["Napped in a tyre. Woke up with a tread pattern on my arse.", "Best bed I never paid for. Smells of garage."])
o.r('preen_sitting_in_the_hole', "Perching on the hole's lip to groom his chest feathers one at a time", 22, 'none',
    [k(.2, 'hole_lip', perch=1, x=.4, y=.6), k(.4, 'hole_lip', perch=1, x=.8, y=1.8, b=.6, mark='fff'), k(.6, 'hole_lip', perch=1, x=1.2, y=1.8, b=.8, mark='fff'), k(.85, 'hole_lip', perch=1, y=.2, eye='^', w=.6)],
    [], g='rest', act=('groom', 'chest'), ages=GROWN, prefer=['happy'])
o.r('sulk_at_the_tyre', "Turning his back to the tyre and sulking with his bill against its wall", 22, 'none',
    [k(.2, 'tyre_wall_l', x=-.4, y=.8, b=.6), k(.4, 'tyre_wall_l', x=-1.4, y=1.2, b=1.2, eye='-'), k(.75, 'tyre_wall_l', x=-1.4, y=1.2, b=1.2, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [], g='rest', act=('sulk', 'tyre'), when=['sad'],
    say=["It swings for no one. Same as me, with less voice.", "Leave me. I'm a tyre now. Round and bitter."])
# --- show
o.r('drum_solo_on_the_tyre', "Drumming a solo with his bill, belly then flank then wall, the tyre ringing a muffled note", 20, 'none',
    [k(.15, 'tyre_belly_l', x=.8, y=.4, b=.4), k(.3, 'tyre_belly_l', x=1.4, y=.4, mark='dum'), k(.45, 'tyre_flank_l', x=1.4, y=.4, b=.4, mark='dum'), k(.6, 'tyre_wall_l', x=1.4, y=.4, mark='DUM'), k(.8, 'tyre_wall_l', x=-.4, y=-1.8, w=1, eye='^', mark='tsss')],
    [], g='show', act=('drum', 'tyre'), prefer=['happy'], obj=[(.3, dict(shake=.06)), (.45, dict(shake=.06)), (.6, dict(shake=.1))],
    say=["Drum solo. Muffled but sincere.", "The tyre has one note and it's a sigh."])
o.r('flourish_off_the_base_plate', "Hopping off the post's base plate, tapping the lip of the hole with his bill as a flourish, and sticking the landing", 20, 'none',
    [k(.15, 'post_base', perch=1, b=.6, x=-.4), k(.3, 'post_base', perch=1, b=-2, w=1, mark='HUP'), k(.5, 'hole_lip', x=2, y=.4, b=-2.4, w=1, mark='tk'), k(.7, x=.4, y=.4, b=1.2, w=.4), k(.88, eye='^', mark='ta-da')],
    [], g='show', act=('hop', 'plate'), prefer=['happy', 'young'], obj=[(.5, dict(sway=.1))])
o.r('sing_into_the_hole', "Singing into the hole with his head inside, letting the tyre hum the note back", 20, 'none',
    [k(.2, 'hole_edge_r', x=.8, y=.6), k(.4, 'hole_edge_r', x=1.8, y=1.4, b=.4, w=.6, eye='O', mark='la'), k(.65, 'hole_edge_r', x=1.8, y=1.4, b=.4, w=1, eye='O', mark='LAAA'), k(.85, x=0, eye='^')],
    [], g='show', act=('sing', 'hole'), shown='head', prefer=['happy'], obj=[(.4, dict(shake=.06)), (.65, dict(shake=.1))],
    say=["The tyre has acoustics. My voice has opinions.", "Sang into a hole. It sang back worse."])
o.r('shout_up_at_the_beam', "Shouting up at the beam where the rope starts, demanding to know why it dangles", 18, 'none',
    [k(.2, x=.4, y=-1.6, eye='>'), k(.4, x=.8, y=-2, b=.4, w=1, eye='>', mark='OI'), k(.65, x=.8, y=-2, b=.6, w=1, eye='>', mark='YOU'), k(.85, x=0, y=0, eye='-')],
    [], g='show', act=('shout', 'beam'), far=True, prefer=['grumpy'],
    say=["Yelled at the beam. It has the high ground and no manners.", "The rope came from up there. Somebody's accountable."])
o.r('argue_with_the_tyre', "Arguing with the tyre's wall, bill an inch off it, listing everything wrong with it", 20, 'none',
    [k(.2, 'tyre_wall_r', x=1.4, y=.4, eye='>'), k(.4, 'tyre_wall_r', x=1.8, y=.6, b=.4, mark='quack'), k(.6, 'tyre_side_r', x=1.6, y=.2, eye='>', mark='QUACK'), k(.85, x=-.8, y=.4, eye='-', mark='hmph')],
    [], g='show', act=('argue', 'tyre'), prefer=['grumpy'],
    say=["It's a circle. A rubber circle. Why's it get all the fuss.", "It hasn't answered back. Typical bully."])
# --- mishap
o.r('stuck_in_the_hole', "Getting stuck with his head wedged in the hole to the shoulders, then hauling out with a pop", 24, 'none',
    [k(.15, x=.6, eye='>'), k(.3, 'hole_lip', x=1.8, y=1.8, b=1.6, mark='oof'), k(.5, 'hole_lip', x=2, y=2, b=2, l=1, eye='O', mark='...'), k(.68, 'hole_edge_r', x=2.2, y=2, b=2, r=1, w=1, mark='POP'), k(.85, x=-1.6, y=1.8, b=1.2, eye='@')],
    [], g='mishap', act=('stuck', 'hole'), shown='head', prefer=['young', 'grumpy'], obj=[(.3, dict(sway=.08)), (.5, dict(shake=.12)), (.68, dict(sway=-.1)), (.85, dict(sway=.05))],
    say=["Head's through, brain's behind. Stuck between them.", "Pulled free. Left a feather and some dignity."])
o.r('turned_back_on_the_shove', "Shoving the tyre hard, turning away, and taking a wallop to the back of the head as it swings back", 18, 'wing',
    [k(.15, 'tyre_flank_l', reach=.6, x=.3), k(.3, 'tyre_flank_l', reach=1, x=.9, b=.4, mark='HUP'), k(.5, x=-.8, y=-.4, eye='^', mark='ha'), k(.68, 'tyre_tip', reach=.5, x=-1.8, y=1.8, b=1.8, eye='@', mark='BONK'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('shove', 'return'), obj=[(.3, dict(sway=.12)), (.55, dict(sway=-.1)), (.68, dict(shake=.1))],
    say=["Clocked from behind by a tyre. Telling no one.", "It had a head start and a rope. Unfair."])
o.r('knocked_flat_by_the_unwinding_rope', "Letting go of the over-wound tyre and getting knocked flat as the rope unwinds", 18, 'none',
    [k(.2, 'tyre_wall_l', x=.8, b=.8, eye='@'), k(.4, 'tyre_wall_l', x=1.4, b=1, w=1, eye='@'), k(.6, 'tyre_wall_r', x=2.4, y=1.8, b=.6, w=1, eye='@', mark='WHUMP'), k(.85, x=.8, y=1, b=1.4, eye='-')],
    [(.6, 'unwound')], g='mishap', act=('knock', 'body'), when=['twist>.4'], prefer=['young'], obj=[(.4, dict(sway=.1)), (.55, dict(shake=.15))])
o.r('kick_the_tread', "Kicking the tread in a temper and hopping away holding his toe", 16, 'none',
    [k(.2, 'tyre_belly_l', x=-.8, y=.4, r=1), k(.4, 'tyre_belly_l', x=-1.4, y=.6, r=1, b=.6, mark='THWK'), k(.6, x=.4, y=1.8, b=.8, l=1, eye='O', mark='ow'), k(.82, x=.4, y=.8, l=1, b=.4, eye='@')],
    [(.4, 'scuff')], g='mishap', act=('kick', 'tread'), prefer=['grumpy'], obj=[(.4, dict(sway=.08))],
    say=["Kicked a tyre. It's been kicked by better.", "My toe has filed an appeal."])
o.r('missed_the_hop', "Hopping for the hole, hitting the tyre's side wall instead, and bouncing off onto his tail", 16, 'none',
    [k(.2, x=.6, b=.8, eye='>'), k(.4, 'tyre_side_l', x=1.4, b=-2, w=1, mark='hup'), k(.6, x=-1.8, y=1.8, b=1.6, l=1, r=1, eye='@', mark='thud'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('hop', 'hole'), prefer=['young'], obj=[(.4, dict(sway=.1)), (.6, dict(sway=-.08))])
o.r('slid_off_the_wet_flank', "Grabbing the wet flank for balance, losing his grip and slipping down it", 16, 'none',
    [k(.2, 'tyre_wall_l', x=.8, y=.6, b=.6), k(.4, 'tyre_wall_l', x=.4, y=.2, b=-.6, l=1, r=1, eye='O', mark='whoa'), k(.6, 'tyre_tip', x=-.8, y=1.6, b=1.6, eye='@', mark='splat'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('slip', 'flank'), when=['obj_wetness>.3'], obj=[(.4, dict(sway=.08)), (.6, dict(shake=.1))])
o.emit()

# ============================================================ toy_seesaw
# Blueprint: type 'seesaw' (playground-workshop): a flat base bar, a slanting A-frame of two legs with a rung-marked centre post inside,
# one long flat plank on a hinge block (studs along its face, wavy grain on its underside), a seat pad and a handle at each end.
# Riding it is native; the plank is drawn level and never moves, only the whole toy trembles (the sprite is over 200 px: sway <= .15).
# Hatchlings work the base bar, the lower legs and the post foot; the plank underside (117 px) is for the big ages; seats, studs and
# handles need a twig.
o = Obj('toy_seesaw', 'placed',
        parts=dict(base='the flat base bar the A-frame stands on', leg='the slanting legs of the A-frame', post='the centre post inside the frame, rung marks down it',
                   plank='the long flat plank with grain along its underside', hinge='the hinge block mid-plank with its round cap', stud='the studs along the plank face',
                   seat='the seat pad at each end of the plank', handle='the handle bar over each seat'),
        fields=dict(leaves=(0, 0, 1), frost=(0, 0, 1), snowcap=(0, 0, 1)),
        physics=[('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrub=[('obj.dirt', 'add', -.25)], dust=[('obj.dirt', 'add', -.2)],
            sweep=[('leaves', 'set', 0)], chip=[('frost', 'mul', .2)], crack=[('frost', 'mul', .4)], scoop=[('snowcap', 'mul', .2)],
            snooze=[('need.energy', 'add', 3)], fun=[('need.fun', 'add', 2)], dry=[('obj.wetness', 'add', -.4)], company=[('need.social', 'add', 2)]),
        anchors=dict(base_l=(.444, .952, 'surface'), base_mid=(.505, .952, 'surface'), base_r=(.566, .952, 'surface'),
                     leg_l_low=(.434, .905), leg_l_mid=(.455, .786), leg_l_top=(.475, .667),
                     leg_r_low=(.566, .905), leg_r_mid=(.545, .786), leg_r_top=(.535, .667),
                     post_low=(.505, .857), post_mid=(.505, .786), post_top=(.505, .643),
                     plank_under_l=(.242, .619), plank_under_r=(.768, .619),
                     plank_end_l=(.091, .595), plank_end_r=(.919, .595), hinge=(.505, .595), plank_under_m=(.444, .619),
                     stud_l=(.131, .571), stud_m=(.313, .571), seat_l=(.172, .5), seat_r=(.838, .5), handle_l=(.242, .405)),
        marks=[('leaves', .3, ',;,.;', 'base_mid', 'leaf'), ('frost', .3, '*.*.*', 'base_l', 'frost'), ('snowcap', .3, '.:*:.', 'leg_l_low', 'snow')])
# --- care
o.r('wipe_the_plank_underside', "Giving the plank's grimy underside a long wipe with a wing, from the left end in to the hinge", 18, 'wing',
    [k(.15, 'plank_under_l', reach=.6, x=.4, y=.6), k(.35, 'plank_under_l', reach=1, x=.8, y=.6, b=.6, mark='fff'), k(.6, 'plank_under_m', reach=1, x=.8, y=.2, b=.4, mark='fff'), k(.9, eye='^')],
    [(.6, 'wipe')], g='care', act=('wipe', 'plank'), when=['obj_dirt>.3'], obj=[(.35, dict(shake=.1)), (.75, dict(shake=.1))])
o.r('scrub_the_base_bar', "Scrubbing the base bar clean with his bill, from the left foot to the right", 18, 'none',
    [k(.2, 'base_l', x=.9, y=1, b=.6), k(.4, 'base_l', x=1.4, y=1.4, b=.8, mark='skrt'), k(.6, 'base_mid', x=1.4, y=1.4, b=.8, mark='skrt'), k(.8, 'base_r', x=1.4, y=1.4, b=.8, mark='skrt'), k(.92, y=.2, eye='^')],
    [(.8, 'scrub')], g='care', act=('scrub', 'base'), when=['obj_dirt>.3'],
    say=["Scrubbed the bar. It's cleaner. It's still a bar.", "Bill's brown now. Moving on."])
o.r('wipe_the_seat_pad_with_a_twig', "Reaching a twig up to wipe the left seat pad, stroke after stroke along it", 20, 'twig',
    [k(.15, 'seat_l', reach=.6, y=-.5), k(.4, 'seat_l', reach=1, x=.5, y=-.8, mark='fff'), k(.6, 'seat_l', reach=1, x=-.2, y=-.8, b=.2, mark='fff'), k(.82, y=-.3, eye='^')],
    [(.6, 'dust')], g='care', act=('wipe', 'seat'), ages=GROWN, when=['obj_dirt>.3'])
o.r('sweep_leaves_off_the_base', "Sweeping the drifted leaves off the base bar with a wing, one foot to the other", 18, 'wing',
    [k(.15, 'base_l', reach=.5, x=.3, y=.6), k(.4, 'base_l', reach=1, x=1.2, y=1.4, b=.4, l=1, mark='fshh'), k(.62, 'base_r', reach=1, x=-.6, y=1.4, b=.4, r=1, mark='fshh'), k(.85, y=.6, eye='^')],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['fall'])
o.r('scrub_mud_off_the_leg_feet', "Scrubbing the mud splashed up the lower legs with his bill, left leg then right", 18, 'none',
    [k(.2, 'leg_l_low', x=.9, y=1, b=.6), k(.4, 'leg_l_low', x=1.5, y=1.4, b=.8, mark='skrt'), k(.65, 'leg_r_low', x=1.5, y=1.4, b=.8, mark='skrt'), k(.85, y=.3, eye='^')],
    [(.65, 'scrub')], g='care', act=('scrub', 'leg'), when=['obj_dirt>.3'])
# --- weather
o.r('chip_frost_off_the_base', "Chipping the frost off the base bar with the edge of his bill, working along it", 18, 'none',
    [k(.2, 'base_l', x=.8, y=.8, b=.6), k(.4, 'leg_l_low', x=1.4, y=.8, b=.6, mark='tik'), k(.6, 'base_mid', x=1.4, y=1.2, b=.8, mark='tik'), k(.8, 'base_r', x=1.4, y=1.2, b=.8, mark='tik'), k(.92, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'base'), when=['frost>.3'])
o.r('scoop_snow_off_the_feet', "Scooping the snow banked round the A-frame's left foot aside with a wing", 20, 'wing',
    [k(.15, 'base_l', reach=.5, x=.3, y=.6), k(.4, 'leg_l_low', reach=1, x=-.8, y=1.2, b=1.2, l=1, mark='fshh'), k(.65, 'leg_l_low', reach=1, x=-.2, y=1.8, b=1.6, r=1, mark='fshh'), k(.85, y=.3, eye='^')],
    [(.65, 'scoop')], g='weather', act=('scoop', 'snow'), when=['snowcap>.3'],
    say=["Dug the legs out. The seesaw's grateful, in a wooden way.", "Snow's gone. It'll hold a grudge, same as me."])
o.r('rub_the_plank_dry', "Rubbing the damp plank underside dry with his tail feathers, backed up against it", 18, 'none',
    [k(.2, 'plank_under_l', x=-.9, y=-.6, b=.2, l=1), k(.45, 'plank_under_l', x=-1.9, y=-.6, b=1.4, w=.3, mark='fff'), k(.7, 'plank_under_m', x=-1.9, y=-.8, b=1.2, w=.9, r=1, mark='fff'), k(.88, eye='^', w=.2)],
    [(.7, 'dry')], g='weather', act=('dry', 'plank'), ages=GROWN, when=['obj_wetness>.3'])
o.r('brace_at_the_leg_in_the_gale', "Bracing his shoulder against the left leg while the gust throws leaves at the frame", 24, 'none',
    [k(.2, 'leg_l_low', x=-.4, y=.2, b=.4), k(.4, 'leg_l_low', x=-1.4, y=.6, b=1.6, w=.6, eye='>', mark='fff'), k(.7, 'leg_l_mid', x=-2, y=1.4, b=2.2, w=1, l=1, eye='>'), k(.9, y=0, eye='^')],
    [], g='weather', act=('brace', 'leg'), when=['windy'], obj=[(.3, dict(shake=.1)), (.5, dict(shake=.15)), (.7, dict(shake=.1))],
    say=["Gust tried the frame. I tried the gust. Frame won, narrowly.", "Leaves in my face. I'm taking it personally."])
o.r('hop_the_frost_off_the_bar', "Hopping from foot to foot on the frosted base bar, cracking the frost with every landing", 20, 'none',
    [k(.15, 'base_l', perch=1, x=.2, b=.4), k(.35, 'base_mid', perch=1, b=-1.6, l=1, mark='crk'), k(.55, 'base_r', perch=1, b=-1.6, r=1, mark='crk'), k(.8, 'base_mid', perch=1, b=-1.2, l=1, eye='^', mark='crk')],
    [(.55, 'crack')], g='weather', act=('hop', 'toes'), when=['frost>.3'], obj=[(.35, dict(shake=.08)), (.55, dict(shake=.1))])
# --- use
o.r('lever_the_end_with_a_twig', "Wedging a twig against the plank's right end and tilting it until the whole toy trembles", 22, 'twig',
    [k(.15, 'plank_end_r', reach=.6, x=.3, y=-.3), k(.4, 'plank_end_r', reach=1, x=1.1, y=-.6, b=.8, mark='hnf'), k(.6, 'plank_end_r', reach=1, x=1.4, y=-.6, b=1.2, l=1), k(.8, x=-.8, y=.4, eye='o', mark='...')],
    [], g='use', act=('tilt', 'plank'), ages=GROWN, obj=[(.4, dict(shake=.1)), (.6, dict(shake=.15)), (.8, dict(sway=-.1))])
o.r('drum_along_the_plank', "Drumming along the plank's underside with his bill, from the left end to the hinge", 20, 'none',
    [k(.15, 'plank_under_l', x=.6, y=-.4), k(.35, 'plank_under_l', x=1.2, y=-.6, mark='dum'), k(.55, 'plank_under_m', x=1.2, y=-.6, mark='dum'), k(.75, 'plank_under_m', x=1.4, y=-.6, mark='DUM'), k(.9, x=0, eye='^')],
    [], g='use', act=('drum', 'plank'), ages=GROWN, prefer=['happy'], obj=[(.35, dict(shake=.06)), (.55, dict(shake=.08)), (.75, dict(shake=.1))])
o.r('tug_the_handle_with_a_twig', "Hooking a twig round the left handle bar and tugging it like a lever", 22, 'twig',
    [k(.15, 'handle_l', reach=.6, y=-.6), k(.4, 'handle_l', reach=1, x=-1.2, y=-.8, b=.6, mark='hnf'), k(.6, 'handle_l', reach=1, x=-1.5, y=-.8, b=.8, l=1), k(.8, x=.4, y=.4, eye='-')],
    [], g='use', act=('tug', 'handle'), ages=['adult', 'mature', 'elder', 'legendary'], obj=[(.4, dict(sway=.1)), (.6, dict(shake=.12))])
o.r('tap_the_seat_pad', "Tapping the right seat pad twice with a twig to hear whether it is padded at all", 18, 'twig',
    [k(.2, 'seat_r', reach=.6, y=-.5), k(.4, 'seat_r', reach=1, x=.4, y=-.8, mark='tok'), k(.6, 'seat_r', reach=.6, y=-.5), k(.8, 'seat_r', reach=1, x=.4, y=-.8, mark='tok'), k(.92, eye='o')],
    [], g='use', act=('tap', 'seat'), ages=GROWN, obj=[(.4, dict(shake=.06)), (.8, dict(shake=.06))])
o.r('peck_up_the_rungs', "Pecking up the centre post rung by rung, as far as his bill will go", 20, 'none',
    [k(.2, 'post_low', x=.5, y=.5, b=.6), k(.4, 'post_low', x=.9, y=.2, mark='tk'), k(.6, 'post_mid', x=.9, y=-.4, b=-.4, mark='tk'), k(.8, 'post_top', x=.4, y=-1.4, b=-.6, eye='o', mark='...')],
    [], g='use', act=('peck', 'rungs'), prefer=['curious'])
o.r('take_turns_pressing_the_ends', "Pressing the plank's left end with a twig while a friend presses the right, taking turns", 26, 'twig',
    [k(.15, 'plank_end_l', reach=.6, x=.3, y=-.3), k(.3, 'plank_end_l', reach=1, x=1.1, y=-.6, b=.8, mark='hup'), k(.55, x=-.4, y=-.6, eye='o'), k(.7, 'plank_end_l', reach=1, x=1.1, y=-.6, b=.8, mark='hup'), k(.88, eye='^')],
    [(.7, 'fun')], g='use', act=('press', 'ends'), ages=GROWN, obj=[(.3, dict(sway=.12)), (.55, dict(sway=-.12)), (.7, dict(sway=.12))],
    duo=[k(.15, 'plank_end_r', reach=.5, x=.2), k(.4, 'plank_end_r', reach=1, x=1.1, y=-.6, b=.8, mark='hup'), k(.6, x=-.4, y=-.6, eye='o'), k(.85, eye='^')],
    say=["One end goes down, the other goes up. Physics, apparently.", "Took turns. Lost count. Won anyway."])
o.r('nudge_a_friend_along_the_bar', "Nudging a friend along the base bar with his shoulder until they swap feet with him", 22, 'none',
    [k(.15, 'base_l', perch=1, x=.4, y=.2), k(.35, 'base_l', perch=1, x=1.2, y=.4, b=.6, mark='hup'), k(.6, 'base_mid', perch=1, x=1.2, y=.4, b=.6, mark='hup'), k(.85, 'base_mid', perch=1, x=0, eye='^')],
    [(.6, 'company')], g='use', act=('nudge', 'base'), obj=[(.35, dict(shake=.06)), (.6, dict(shake=.08))],
    duo=[k(.15, 'base_r', perch=1, x=-.2), k(.45, 'base_r', perch=1, x=-.4, b=.6, eye='o'), k(.65, 'base_mid', perch=1, x=.2, b=-1, w=1, eye='^'), k(.85, 'base_mid', perch=1, eye='^')],
    say=["Shoved them off their foot. They shoved back. Civilised.", "We traded ends. Neither of us won."])
# --- play
o.r('hop_up_and_down_the_base', "Hopping along the base bar and bouncing on it so the whole toy trembles", 18, 'none',
    [k(.15, 'base_l', perch=1, b=.6), k(.35, 'base_l', perch=1, b=-2, w=.6, mark='boing'), k(.6, 'base_mid', perch=1, b=-2, w=.6, mark='boing'), k(.85, 'base_r', perch=1, b=-2.4, w=1, eye='^', mark='BOING')],
    [], g='play', act=('hop', 'base'), prefer=['happy', 'young'], obj=[(.35, dict(shake=.06)), (.6, dict(shake=.1)), (.85, dict(shake=.12))])
o.r('walk_the_base_like_a_beam', "Balancing along the base bar from end to end like a beam, wings out", 22, 'none',
    [k(.15, 'base_l', perch=1, x=.4, w=.6), k(.4, 'base_l', perch=1, x=.8, w=1, l=1, eye='o'), k(.65, 'base_mid', perch=1, x=.8, w=1, r=1, eye='O'), k(.88, 'base_r', perch=1, x=.4, w=.4, eye='^')],
    [], g='play', act=('balance', 'base'), prefer=['curious'])
o.r('race_round_the_frame', "A race round the frame, slapping each leg as he passes", 20, 'none',
    [k(.15, 'leg_l_low', x=.8, b=.4, eye='>'), k(.35, 'leg_l_low', x=1.6, b=-1.6, w=1, mark='TAG'), k(.6, 'leg_r_low', x=1.6, b=-1.6, l=1, eye='>', mark='TAG'), k(.82, x=.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('race', 'frame'), prefer=['happy'])
o.r('drum_the_legs', "Drumming on the A-frame's legs like a xylophone, tapping up the left one and down the right", 22, 'none',
    [k(.15, 'leg_l_low', x=.8, y=.4, b=.4), k(.3, 'leg_l_mid', x=1.2, y=-.2, mark='dong'), k(.45, 'leg_l_top', x=1.2, y=-.6, mark='dang'), k(.65, 'leg_r_top', x=1.2, y=-.6, mark='dong'), k(.8, 'leg_r_low', x=1.2, y=.4, mark='DUNG')],
    [], g='play', act=('drum', 'legs'), ages=GROWN, prefer=['happy'], obj=[(.3, dict(shake=.06)), (.45, dict(shake=.08)), (.65, dict(shake=.08))])
o.r('hide_and_seek_round_the_post', "Hide and seek round the A-frame, ducking out from one leg then the other", 20, 'none',
    [k(.2, 'leg_r_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'leg_r_mid', x=1.4, y=0, eye='O'), k(.6, 'leg_l_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.8, 'leg_l_mid', x=1.4, y=0, eye='O', mark='ha')],
    [], g='play', act=('hide', 'post'), prefer=['curious', 'young'])
o.r('chase_a_friend_round_the_post', "Chasing a friend round the centre post, the pair of them circling the frame", 24, 'none',
    [k(.15, 'post_low', x=.8, b=.4, eye='>'), k(.35, 'leg_r_low', x=1.6, b=-1.6, w=1, eye='>', mark='HA'), k(.6, 'post_mid', x=1.6, b=-1.6, r=1, eye='>'), k(.85, x=.4, y=.6, eye='O', mark='...')],
    [(.6, 'fun')], g='play', act=('chase', 'post'), prefer=['happy'],
    duo=[k(.15, 'leg_l_low', x=.4, b=.4, eye='o'), k(.4, 'leg_l_mid', x=1.6, b=-1.6, w=1, eye='>'), k(.65, 'leg_r_mid', x=1.6, b=-1.6, l=1, eye='>'), k(.85, x=.4, eye='^')],
    say=["Chased a friend round a post. The post stayed neutral.", "Caught them round the pole. Let go. Dignity first."])
# --- test
o.r('count_the_studs', "Counting the studs along the plank with the tip of a twig, tapping each one", 22, 'twig',
    [k(.15, 'stud_l', reach=.6, y=-.5), k(.35, 'stud_l', reach=1, x=.8, y=-.7, mark='one'), k(.6, 'stud_m', reach=1, x=.8, y=-.7, mark='two'), k(.82, y=-.3, eye='@', mark='...')],
    [], g='test', act=('count', 'studs'), ages=GROWN, prefer=['curious'])
o.r('measure_himself_on_the_leg', "Standing beside the left leg and laying a wing along it to measure how much taller it is", 20, 'wing',
    [k(.15, 'leg_l_low', reach=.4, x=-.8, y=.2, b=.2), k(.4, 'leg_l_mid', reach=1, x=-.2, y=-1.2, b=1, w=.4, mark='hm'), k(.65, 'leg_l_top', reach=1, x=-.2, y=-2.2, b=1.4, eye='^', mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('measure', 'leg'), prefer=['curious', 'young'])
o.r('sniff_the_plank_underside', "Sniffing along the plank's underside for the smell of whoever sat here last", 18, 'none',
    [k(.2, 'plank_under_l', x=.6, y=-.6, b=-.2), k(.4, 'plank_under_l', x=1.1, y=-.8, eye='o', mark='snf'), k(.6, 'plank_under_m', x=1.1, y=-.8, eye='O', mark='snf'), k(.82, x=0, eye='-')],
    [], g='test', act=('sniff', 'plank'), ages=GROWN, prefer=['curious'])
o.r('lick_the_leg', "Tasting the left leg with one lick to find out what a seesaw tastes like", 14, 'none',
    [k(.2, 'leg_l_low', x=.6, y=.6, b=.6), k(.4, 'leg_l_low', x=1.6, y=1.2, b=.8, eye='o', mark='lick'), k(.65, 'leg_l_mid', x=-1.4, y=-1.8, eye='@', mark='ptoo'), k(.85, x=0, eye='-')],
    [], g='test', act=('taste', 'leg'),
    say=["Paint, splinters, a bit of other duck. Zero stars.", "Tastes like waiting for someone."])
o.r('throw_a_shoulder_at_the_frame', "Testing the frame by throwing a shoulder against the right leg to see whether it scoots", 18, 'none',
    [k(.2, 'leg_r_low', x=-.8, y=.4, b=.4), k(.4, 'leg_r_low', x=-1.8, y=.6, b=1.6, mark='HUP'), k(.6, 'leg_r_low', x=-1.8, y=.6, b=1.6, eye='-', mark='nope'), k(.82, x=.4, y=.4, eye='>')],
    [], g='test', act=('test', 'leg'), obj=[(.4, dict(shake=.12))],
    say=["Didn't scoot. It's bolted down. Admirable. Annoying.", "Shoulder hurts. Frame doesn't even know."])
o.r('weigh_the_plank_up_from_below', "Weighing the plank by pressing a wing up against its underside to feel how heavy it is", 18, 'wing',
    [k(.2, 'plank_under_r', reach=.5, x=.5, y=-.4), k(.45, 'plank_under_r', reach=1, x=1.1, y=-.6, b=.8, eye='>', mark='hnng'), k(.7, 'plank_under_r', reach=1, x=1.4, y=-.6, b=1, mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('weigh', 'plank'), ages=GROWN, obj=[(.45, dict(shake=.06))])
o.r('press_the_post_to_check_the_bolts', "Pressing his whole weight against the centre post to check the frame is bolted down", 18, 'none',
    [k(.2, 'post_mid', x=.6, y=.4, b=.4), k(.4, 'post_mid', x=1.6, y=.8, b=1.4, mark='hnn'), k(.65, 'post_mid', x=1.8, y=.8, b=1.6, eye='-'), k(.85, y=.2, eye='^')],
    [], g='test', act=('press', 'post'), obj=[(.45, dict(shake=.06))])
# --- rest
o.r('nap_on_the_base_bar', "Napping curled up on the base bar with his bill tucked", 28, 'none',
    [k(.2, 'base_mid', perch=1, x=.4, y=.8, b=.6), k(.4, 'base_mid', perch=1, y=1.4, b=1.2, eye='-'), k(.7, 'base_mid', perch=1, y=1.5, b=1.2, eye='-', mark='zzz'), k(.9, y=.2, b=.3, eye='^')],
    [(.4, 'snooze')], g='rest', act=('nap', 'base'), prefer=['tired', 'night'])
o.r('wait_for_a_partner', "Waiting beside the left leg for someone to turn up for the far seat, glancing along the plank", 24, 'none',
    [k(.2, 'leg_l_low', x=.2, y=-.2), k(.4, 'leg_l_low', x=.2, y=-1.6, l=1, eye='o'), k(.6, 'leg_l_low', x=.2, y=-1.6, r=1, eye='o', mark='...'), k(.8, 'leg_l_low', x=.6, y=-.5, eye='>')],
    [], g='rest', act=('wait', 'partner'), when=['lonely'])
o.r('sulk_at_the_far_leg', "Sulking against the far leg with his back to the empty seats", 22, 'none',
    [k(.2, 'leg_r_low', x=-.9, y=1.4, b=.2, l=1), k(.45, 'leg_r_low', x=-2, y=1.8, b=.8, eye='-'), k(.75, 'leg_r_low', x=-2.2, y=2.2, b=.8, r=1, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [], g='rest', act=('sulk', 'leg'), when=['sad'],
    say=["Two seats, no one. The plank has taught me about life.", "Even the seesaw has someone on the other end. Smug thing."])
o.r('lean_on_the_plank_edge', "Leaning his chin against the plank's low edge like a bar rail and watching the yard go by", 22, 'none',
    [k(.2, 'plank_under_l', x=.4, y=-.4, b=.4), k(.4, 'plank_under_l', x=1.2, y=-.4, b=1, eye='-'), k(.7, 'plank_under_l', x=1.4, y=-.4, b=1.4, eye='-', mark='mm'), k(.9, y=.2, eye='^')],
    [], g='rest', act=('lean', 'plank'), ages=GROWN, prefer=['tired'])
o.r('warm_against_the_sunny_leg', "Warming his cheek and chest against the sun-baked leg until the chill leaves his feathers", 24, 'none',
    [k(.2, 'leg_r_low', x=.4, y=.4, b=.4), k(.4, 'leg_r_mid', x=1.4, y=1.4, b=1.2, eye='-'), k(.75, 'leg_r_mid', x=1.6, y=1.6, b=1.6, eye='-', mark='mm'), k(.9, y=.2, eye='^')],
    [], g='rest', act=('warm', 'leg'), when=['sun', 'cold'])
o.r('hug_the_leg', "Wrapping both wings round the right leg and holding on with his cheek against the wood", 24, 'wing',
    [k(.2, 'leg_r_low', reach=.5, x=.4, y=.6, b=.2), k(.45, 'leg_r_low', reach=1.5, x=.8, y=1, b=.8, eye='-'), k(.75, 'leg_r_low', reach=1.5, x=1, y=1, b=.8, w=.4, eye='-', mark='mm'), k(.9, reach=.2, y=.2, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'leg'), when=['lonely'],
    say=["Hugged a leg. It didn't hug back. Wood's like that.", "Don't tell the plank. It's the sensitive one."])
# --- show
o.r('chant_see_saw', "Singing see and then saw, wings up for see and down for saw, thumping a leg in time", 22, 'none',
    [k(.15, 'leg_l_low', x=.4, y=-.4, w=.4), k(.3, 'leg_l_low', x=.4, y=-1.4, w=1, mark='SEE'), k(.5, 'leg_r_low', x=.6, y=1.2, b=.8, w=0, mark='SAW'), k(.7, 'leg_l_low', x=.4, y=-1.4, w=1, mark='SEE'), k(.88, y=1.2, b=.8, eye='^', mark='SAW')],
    [], g='show', act=('sing', 'chant'), prefer=['happy'], obj=[(.3, dict(sway=.06)), (.5, dict(sway=-.06)), (.7, dict(sway=.06))],
    say=["See. Saw. See. Saw. It's all I know and I'm proud of it.", "I did the chant. The seesaw stayed level out of spite."])
o.r('dance_along_the_base', "Dancing along the base bar from one foot to the other, a little hop at each end", 22, 'none',
    [k(.15, 'base_l', perch=1, x=.2, y=-.4, w=.4), k(.35, 'base_l', perch=1, x=.6, y=-.4, b=-1.4, w=1, l=1, mark='ta'), k(.6, 'base_r', perch=1, x=-.8, y=-.6, b=-.8, w=1, r=1), k(.85, 'base_l', perch=1, x=.6, y=-.4, b=-1.4, w=1, l=1, mark='da')],
    [], g='show', act=('dance', 'base'), prefer=['happy'])
o.r('hail_the_far_seat', "Cupping a wing to his bill and shouting along the plank to the far seat", 18, 'none',
    [k(.2, x=.2, y=-1.2, w=.4, eye='>'), k(.4, x=1.4, y=-2.4, b=.8, w=.8, l=1, eye='>', mark='OI'), k(.65, x=1.4, y=-2.4, b=1.2, w=1, r=1, eye='>', mark='SIT DOWN'), k(.85, x=-.4, eye='-')],
    [], g='show', act=('shout', 'seat'), far=True, prefer=['grumpy'],
    say=["Called the far seat. It has terrible manners.", "I'd take a seat. Then I'd have to get up."])
o.r('pat_the_plank_like_a_horse', "Patting the plank along its length like a horse's neck, left end to right, murmuring good plank", 22, 'wing',
    [k(.15, 'plank_under_l', reach=.5, x=.3, y=-.2), k(.35, 'plank_under_l', reach=1, x=.6, y=-.4, mark='pat'), k(.55, 'plank_under_m', reach=1, x=.6, y=-.4, mark='pat'), k(.8, 'plank_under_r', reach=1, x=.6, y=-.4, mark='good plank')],
    [], g='show', act=('pat', 'plank'), ages=GROWN, prefer=['happy'])
o.r('peck_the_hinge_cap', "Pecking at the round cap on the hinge as though it were an eye that had just winked", 18, 'twig',
    [k(.2, 'hinge', reach=.6, y=-.4), k(.4, 'hinge', reach=1, x=.8, y=-.8, mark='tk'), k(.6, 'hinge', reach=1, x=.8, y=-.8, mark='tk'), k(.85, eye='o', mark='...')],
    [], g='show', act=('peck', 'hinge'), ages=GROWN, prefer=['curious'], obj=[(.4, dict(shake=.05)), (.6, dict(shake=.05))])
o.r('sing_see_saw_in_rounds', "Singing see at one leg while a friend sings saw at the other, trading the words back and forth", 24, 'none',
    [k(.15, 'leg_l_low', x=.4, y=-.6, w=.4), k(.3, 'leg_l_low', x=.6, y=-1.8, b=.4, w=1, mark='SEE'), k(.55, 'leg_l_low', x=.2, y=-.8, b=.2, w=.4, eye='o'), k(.75, 'leg_l_low', x=.6, y=-1.8, b=.4, w=1, mark='SEE'), k(.9, eye='^')],
    [], g='show', act=('sing', 'rounds'), prefer=['happy'], obj=[(.3, dict(sway=.08)), (.75, dict(sway=-.08))],
    duo=[k(.15, 'leg_r_low', x=.4, y=-.6, w=.4), k(.4, 'leg_r_low', x=.2, y=-.8, b=.2, eye='o'), k(.55, 'leg_r_low', x=.6, y=-1.8, b=.4, w=1, mark='SAW'), k(.9, eye='^')],
    say=["See, saw, see, saw. We're not good. We're loud.", "Sang it in rounds. The legs hummed along."])
# --- mishap
o.r('lifted_it_and_got_bonked', "Lifting the plank's left end with a twig, stepping back to admire it, and taking the drop square on the beak", 22, 'twig',
    [k(.15, 'plank_end_l', reach=.6, y=-.3), k(.35, 'plank_end_l', reach=1, x=.5, y=-.6, b=-.8, mark='hng'), k(.55, x=-1.2, y=-.4, eye='^', mark='ha'), k(.72, 'plank_under_l', x=1.2, y=1.4, b=1.2, eye='@', mark='BONK'), k(.9, y=.6, eye='-')],
    [], g='mishap', act=('lift', 'plank_end'), ages=GROWN, obj=[(.35, dict(sway=.1)), (.72, dict(shake=.15))],
    say=["It was up. I admired it. It came down. We're not speaking.", "Bonked on my own good idea."])
o.r('stuck_in_the_gap_by_the_post', "Getting stuck with his head wedged in the gap between the post and the leg, then hauling out", 24, 'none',
    [k(.15, x=.6, y=.4, eye='>'), k(.3, 'post_low', x=1.4, y=1.2, b=.8, mark='oof'), k(.5, 'post_low', x=1.6, y=1.4, b=1.2, r=1, eye='O', mark='...'), k(.7, 'leg_l_low', x=1.8, y=1.4, b=1.6, l=1, w=.6, mark='POP'), k(.85, x=-2.2, y=.6, b=2, eye='@')],
    [], g='mishap', act=('stuck', 'gap'), shown='head', prefer=['young'], obj=[(.5, dict(shake=.1))])
o.r('bounced_off_the_end_of_the_bar', "Hopping so hard on the base bar that the frame throws him off the end onto his tail", 20, 'none',
    [k(.15, 'base_r', perch=1, b=.6), k(.35, 'base_r', perch=1, b=-2.4, w=1, mark='BOING'), k(.55, x=-1.8, y=1.8, b=1.8, w=1, l=1, r=1, eye='@', mark='thud'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('hop', 'bar'), prefer=['young'], obj=[(.35, dict(shake=.1)), (.55, dict(shake=.14))])
o.r('stubbed_a_toe_on_the_bar', "Kicking the base bar's end to hear it twang and finding out what a stubbed toe sounds like", 16, 'none',
    [k(.2, 'base_l', x=-1.2, y=.2, l=1), k(.4, 'base_l', x=-2, y=.2, l=1, b=1, mark='TWANG'), k(.6, x=1, y=1, b=.4, r=1, eye='O', mark='ow'), k(.82, x=1.6, y=2.2, r=1, b=1.4, eye='@')],
    [], g='mishap', act=('kick', 'bar'), prefer=['grumpy'], obj=[(.4, dict(shake=.08))],
    say=["It twanged. I swore. We both vibrated.", "Toe hurts. Bar's fine. Typical."])
o.r('slid_on_the_wet_bar', "Reaching for the wet base bar, losing his footing, and slipping down onto his tail", 16, 'none',
    [k(.2, 'base_mid', x=.8, y=.6, b=.6), k(.4, 'base_mid', x=.4, y=.2, b=-.6, l=1, r=1, eye='O', mark='whoa'), k(.6, x=-1.8, y=1.6, b=1.6, eye='@', mark='splat'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('slip', 'bar'), when=['obj_wetness>.3'], obj=[(.4, dict(shake=.06))])
o.r('knocked_his_head_standing_up', "Standing up too fast and knocking his head on the plank's underside", 16, 'none',
    [k(.2, 'leg_l_mid', x=.2, y=.4, b=.8), k(.4, 'plank_under_l', x=.4, y=-1.4, b=-1.6, eye='O'), k(.55, 'plank_under_l', x=.2, y=-1.8, b=-2, eye='@', mark='BONK'), k(.8, x=-.4, y=1.4, b=1, eye='-')],
    [], g='mishap', act=('knock', 'plank'), ages=GROWN, obj=[(.55, dict(shake=.1))],
    say=["Plank 1, skull 0. Rematch denied.", "That's a hard seat for a soft head."])
o.emit()

# ============================================================ birdhouse
# Blueprint (home-workshop): a 54-high house, shingle roof, plank walls with nail heads, a door panel with a perch bar across its foot,
# wall plates (the (=) glyphs: plates, not holes), set on a bare pole (12-76 px) with a foot slab (6 px). The box floor is 87 px up,
# the front ledge 93, the perch bar 105, the roof eave 181. Hatchlings work only the pole and its foot; duck stage inhabitants live in
# it (native shelter), so nothing here moves in.
o = Obj('birdhouse', 'placed',
        parts=dict(pole='the bare pole under the house', foot='the flat foot slab at the pole base', ground='the ground round the foot slab',
                   underside='the underside edge of the house floor', floor='the floor rim sticking out at the left', ledge='the front ledge below the door',
                   perch='the perch bar across the foot of the door', door='the door panel and its frame', plate='the wall plates on the planks',
                   wall='the plank walls with nail heads', eave='the overhanging eave of the roof', roof='the shingled roof'),
        fields=dict(pit=(0, 0, 1), leaves=(0, 0, 1), frost=(0, 0, 1), snowcap=(0, 0, 1)),
        physics=[('pit', 'rate', .0004, 'wet'),
                 ('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrub=[('obj.dirt', 'add', -.25)], dust=[('obj.dirt', 'add', -.2)], polish=[('obj.dirt', 'add', -.15)],
            tamp=[('pit', 'set', 0)], dig=[('pit', 'add', .4)], dry=[('obj.wetness', 'add', -.4)], scuff=[('obj.condition', 'add', -.25)],
            clean_bill=[('need.cleanliness', 'add', 1)], maypole=[('need.fun', 'add', 2)],
            sweep=[('leaves', 'set', 0)], chip=[('frost', 'mul', .2)], clear=[('snowcap', 'mul', .2)],
            snooze=[('need.energy', 'add', 3)], company=[('need.social', 'add', 2)], admire=[('need.social', 'add', 1.5)]),
        anchors=dict(pole_top=(.508, .77), pole_high=(.492, .811), pole_high_r=(.557, .811), pole_mid=(.508, .868), pole_mid_r=(.557, .868),
                     pole_low=(.508, .925), pole_low_r=(.557, .925),
                     foot_l=(.41, .981, 'surface'), foot_mid=(.459, .981, 'surface'), foot_r=(.508, .981, 'surface'),
                     floor_rim=(.23, .717), underside_edge=(.508, .736), ledge=(.41, .698), perch_bar=(.43, .66), plate_l=(.262, .623),
                     wall_nail=(.18, .58), eave_l=(.15, .42)),
        marks=[('pit', .3, 'o.o', 'foot_mid', 'mud'), ('leaves', .3, ',;,.;', 'foot_l', 'leaf'), ('frost', .3, '*.*.*', 'pole_mid', 'frost'),
               ('snowcap', .3, '.:*:.', 'foot_r', 'snow'), ('snowcap', .3, '.:*:*:.', 'eave_l', 'snow')])
# --- care
o.r('wipe_the_pole', "Giving the pole a wipe with a wing, from the foot up as high as he can reach", 16, 'wing',
    [k(.15, 'pole_low', reach=.6, x=.3), k(.35, 'pole_low', reach=1, x=1.4, y=.2, mark='fff'), k(.55, 'pole_mid', reach=1, x=1.4, y=-.2, mark='fff'), k(.78, 'pole_high', reach=1, x=1.5, y=-.7, mark='fff'), k(.9, eye='^')],
    [(.78, 'wipe')], g='care', act=('wipe', 'pole'), when=['obj_dirt>.3'],
    say=["Pole's clean. The house won't notice. I'll know.", "Grime's on my wing now. It travels."])
o.r('scrub_the_foot_slab', "Scrubbing the foot slab clean with his bill, from one end to the other", 16, 'none',
    [k(.2, 'foot_l', x=.9, y=.8, b=.5), k(.4, 'foot_l', x=1.2, y=1, b=.6, mark='skrt'), k(.6, 'foot_mid', x=1.2, y=1.1, b=.6, mark='skrt'), k(.8, 'foot_r', x=1.2, y=1, b=.6, mark='skrt'), k(.92, y=.2, eye='^')],
    [(.8, 'scrub')], g='care', act=('scrub', 'foot'), when=['obj_dirt>.3'])
o.r('scrape_bill_clean_on_the_pole', "Scraping his bill clean along the pole's edge, left side then right", 14, 'none',
    [k(.2, 'pole_mid', x=.8, y=.3), k(.4, 'pole_mid', x=1.1, y=.5, b=.2, mark='skrk'), k(.6, 'pole_mid_r', x=1.1, y=.5, b=.2, mark='skrk'), k(.85, y=-.2, eye='^')],
    [(.6, 'clean_bill')], g='care', act=('scrape', 'pole_edge'))
o.r('sweep_leaves_off_the_slab', "Sweeping the drifted leaves off the foot slab with a wing, one end to the other", 18, 'wing',
    [k(.15, 'foot_l', reach=.5, x=.3, y=.6), k(.4, 'foot_l', reach=1, x=2.2, y=1.4, b=.4, l=1, mark='fshh'), k(.62, 'foot_r', reach=1, x=-1.6, y=1.4, b=.4, r=1, mark='fshh'), k(.85, y=.6, eye='^', x=0.9)],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['fall'])
o.r('wipe_the_underside_with_a_twig', "Reaching a twig up to wipe the underside edge of the floor, stroke after stroke", 20, 'twig',
    [k(.15, 'underside_edge', reach=.7, y=-.4), k(.4, 'underside_edge', reach=1, x=.4, y=-.7, mark='fff'), k(.65, 'floor_rim', reach=1, x=.5, y=-.7, mark='fff'), k(.85, y=-.2, eye='^')],
    [(.65, 'dust')], g='care', act=('wipe', 'underside'), when=['obj_dirt>.3'])
o.r('polish_the_perch_bar', "Polishing the perch bar with the flat of a wing until it shines a little", 18, 'wing',
    [k(.15, 'perch_bar', reach=.6, x=.3, y=-.4), k(.4, 'perch_bar', reach=1, x=1.7, y=-.6, mark='fff'), k(.65, 'ledge', reach=1, x=1.7, y=-.4, mark='fff'), k(.85, y=-.2, eye='^', x=0.9)],
    [(.65, 'polish')], g='care', act=('polish', 'perch'), when=['obj_dirt>.3'], ages=GROWN)
o.r('wipe_his_feet_on_the_slab', "Giving his feet a wipe on the foot slab like a doormat, left foot then right", 16, 'none',
    [k(.2, 'foot_mid', perch=1, l=1, b=.4), k(.4, 'foot_mid', perch=1, l=1, b=.6, mark='shff'), k(.6, 'foot_mid', perch=1, r=1, b=.6, mark='shff'), k(.82, 'foot_mid', perch=1, y=.2, eye='^')],
    [(.6, 'clean_bill')], g='care', act=('wipe', 'feet'))
# --- weather
o.r('chip_frost_off_the_pole', "Chipping the frost off the pole with the edge of his bill, working up it", 18, 'none',
    [k(.2, 'pole_low', x=.8, y=.8, b=.6), k(.4, 'pole_mid', x=1.4, y=.8, b=.6, mark='tik'), k(.6, 'pole_high', x=1.4, y=.4, b=.2, mark='tik'), k(.85, y=-.2, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'pole'), when=['frost>.3'])
o.r('scrape_frost_off_the_eave', "Scraping the frost off the roof eave with the tip of a twig, end to end", 20, 'twig',
    [k(.15, 'eave_l', reach=.6, y=-.5, x=.2), k(.4, 'eave_l', reach=1, x=.8, y=-.8, mark='krr'), k(.62, 'eave_l', reach=1, x=1.4, y=-.8, b=.4, l=1, mark='krr'), k(.82, y=-.3, eye='^')],
    [(.62, 'chip')], g='weather', act=('scrape', 'eave'), ages=['adult', 'mature', 'elder', 'legendary'], when=['frost>.3'])
o.r('scoop_snow_off_the_slab', "Scooping the snow banked round the foot slab aside with his bill, end to end", 20, 'none',
    [k(.2, 'foot_l', x=.9, y=1, b=.6), k(.4, 'foot_l', x=2.5, y=1.4, b=.8, mark='fshh'), k(.65, 'foot_r', x=2.5, y=1.4, b=.8, mark='fshh'), k(.85, y=.3, eye='^', x=0.9)],
    [(.65, 'clear')], g='weather', act=('scoop', 'snow'), when=['snowcap>.3'],
    say=["Snow's off the slab. The house stays snug, smug and tall.", "Dug out a doormat. No one's coming."])
o.r('sweep_snow_off_the_eave', "Sweeping the snow off the roof eave with a twig, left to right", 22, 'twig',
    [k(.15, 'eave_l', reach=.6, y=-.5), k(.4, 'eave_l', reach=1, x=1, y=-.8, b=.4, mark='fshh'), k(.65, 'eave_l', reach=1, x=1.6, y=-.8, b=.8, l=1, mark='fshh'), k(.85, y=-.3, eye='^')],
    [(.65, 'clear')], g='weather', act=('sweep', 'snow'), ages=['adult', 'mature', 'elder', 'legendary'], when=['snowcap>.3'])
o.r('rub_the_wet_pole_dry', "Backing up to the damp pole and rubbing it dry with his tail feathers", 18, 'none',
    [k(.2, 'pole_mid', x=-.9, y=-.2, b=.3, l=1), k(.45, 'pole_mid', x=-1.8, y=-.2, b=1.2, w=.3, mark='fff'), k(.7, 'pole_high', x=-1.8, y=-.4, b=1.2, w=.9, r=1, mark='fff'), k(.88, eye='^', w=.2)],
    [(.7, 'dry')], g='weather', act=('dry', 'pole'), when=['obj_wetness>.3'])
o.r('brace_against_the_pole_in_the_gale', "Bracing his back against the pole while the gust whips leaves round the house", 24, 'none',
    [k(.2, 'pole_low', x=-.4, y=.2, b=.4), k(.4, 'pole_low', x=-2.4, y=.6, b=1.6, w=.6, eye='>', mark='fff'), k(.7, 'pole_mid', x=-3.2, y=1.6, b=2.4, w=1, l=1, eye='>'), k(.9, y=0, eye='^', x=0.9)],
    [], g='weather', act=('brace', 'pole'), when=['windy'], obj=[(.3, dict(sway=.1)), (.5, dict(sway=-.1)), (.7, dict(sway=.1))],
    say=["Wind wants the house. I'm in the way. Good.", "The pole creaks. I creak louder."])
o.r('hunch_by_the_pole_in_the_storm', "Taking shelter in the lee of the pole as the storm blows over, bill low, waiting it out", 32, 'none',
    [k(.2, 'pole_low', x=-.4, y=.6, b=.6), k(.4, 'pole_low', x=-1.2, y=1.2, b=1.4, eye='-'), k(.7, 'pole_low', x=-1.2, y=1.4, b=1.6, eye='-', mark='brr'), k(.9, y=.2, eye='^')],
    [], g='weather', act=('shelter', 'pole'), when=['storm', 'wet'])
# --- use
o.r('tap_the_perch_bar', "Tapping the perch bar twice with a wing to hear whether it is hollow", 16, 'wing',
    [k(.2, 'perch_bar', reach=.6, y=-.4), k(.4, 'perch_bar', reach=1, x=.6, y=-.6, mark='tok'), k(.6, 'perch_bar', reach=.6, y=-.4), k(.8, 'perch_bar', reach=1, x=.6, y=-.6, mark='tok'), k(.92, eye='o')],
    [], g='use', act=('tap', 'perch'), ages=GROWN, obj=[(.4, dict(shake=.05)), (.8, dict(shake=.05))])
o.r('press_the_wall_plate', "Pressing a wing against the wall plate to feel whether it gives", 16, 'wing',
    [k(.2, 'plate_l', reach=.5, x=.4, y=-.2), k(.45, 'plate_l', reach=1, x=2, y=-.4, b=.8, mark='hnng'), k(.7, 'plate_l', reach=1, x=2.4, y=-.4, b=1, mark='...'), k(.88, reach=.1, eye='-', x=0.9)],
    [], g='use', act=('press', 'plate'), ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], obj=[(.45, dict(shake=.05))])
o.r('knock_at_the_door', "Knocking at the door, three raps, then standing back to wait for an answer", 22, 'wing',
    [k(.15, 'ledge', reach=.6, x=.2, y=-.3), k(.3, 'ledge', reach=1, x=.7, y=-.5, mark='knk'), k(.45, 'perch_bar', reach=1, x=.7, y=-.5, mark='knk'), k(.6, x=-.4, y=-1, eye='o', mark='...'), k(.85, eye='^')],
    [(.45, 'company')], g='use', act=('knock', 'door'), ages=GROWN, obj=[(.3, dict(shake=.05)), (.45, dict(shake=.05))],
    duo=[k(.15, 'pole_mid_r', x=.2), k(.55, 'pole_mid_r', x=.8, y=-.4, mark='who'), k(.7, 'pole_mid_r', x=.8, y=-.6, mark='is it?'), k(.9, eye='^')],
    say=["Knocked. A friend answered from the pole. House stayed silent.", "Who's there? Me. Me who? Me, the duck."])
o.r('hook_the_perch_with_a_twig', "Hooking a twig over the perch bar and tugging the whole house to feel how firmly it is fixed", 24, 'twig',
    [k(.15, 'perch_bar', reach=.6, y=-.5, x=.3), k(.4, 'perch_bar', reach=1, x=-1, y=-.8, b=.8, mark='hnf'), k(.6, 'perch_bar', reach=1, x=-1.4, y=-.8, b=1.2, l=1), k(.8, x=.4, y=.4, eye='-')],
    [], g='use', act=('tug', 'perch'), ages=GROWN, obj=[(.4, dict(shake=.1)), (.6, dict(shake=.14))])
o.r('shove_the_pole', "Shoving the pole with his shoulder to see whether the house rocks", 18, 'none',
    [k(.2, 'pole_mid', x=-.8, y=.4, b=.4), k(.4, 'pole_mid', x=-2.8, y=.6, b=1.6, mark='HUP'), k(.6, 'pole_mid', x=-2.8, y=.6, b=1.6, eye='-', mark='nope'), k(.82, x=1.4, y=.4, eye='>')],
    [], g='use', act=('shove', 'pole'), obj=[(.4, dict(shake=.12)), (.6, dict(shake=.06))],
    say=["Shoved it. It shrugged. I've been out-stubborned by timber.", "Not a wobble. Shame."])
o.r('dig_at_the_foot', "Digging a pit beside the foot slab with his bill to see how deep the pole goes", 20, 'none',
    [k(.15, 'foot_l', x=.8, y=1.4, b=.6), k(.35, 'foot_l', x=1.6, y=2.2, b=1.2, mark='scrt'), k(.55, 'foot_l', x=1.6, y=2.2, b=1.4, l=1, mark='scrt'), k(.8, 'foot_l', x=.6, y=.8, b=.4, eye='^')],
    [(.55, 'dig')], g='use', act=('dig', 'ground'), when=['pit<.6'],
    say=["Dug a hole beside a pole. The pole is unmoved. So am I.", "Found dirt. More dirt. Called it progress."])
o.r('press_the_pit_flat', "Pressing the pit flat again with both feet, left foot then right", 16, 'none',
    [k(.2, 'foot_mid', l=1, y=.4), k(.4, 'foot_mid', y=.8, b=.6, r=1, mark='thud'), k(.6, 'foot_r', y=.8, b=.6, l=1, mark='thud'), k(.82, 'foot_r', y=.4, b=.4, r=1, eye='^')],
    [(.6, 'tamp')], g='use', act=('press', 'ground'), when=['pit>.3'], prefer=['grown'],
    say=["Filled it in. Evidence gone. Never happened.", "Stamped it flat. The ground can sulk, I've seen worse."])
# --- play
o.r('hide_round_the_pole', "Hide and seek round the pole, ducking out one side then the other", 18, 'none',
    [k(.2, 'pole_mid', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'pole_mid_r', x=2.4, y=0, eye='O'), k(.6, 'pole_low', x=-2.2, y=.8, b=.6, eye='o'), k(.8, 'pole_low_r', x=2.4, y=0, eye='O', mark='ha')],
    [], g='play', act=('hide', 'pole'), prefer=['curious', 'young'])
o.r('dance_round_the_pole', "Dancing round the pole like a maypole, a wing trailing along it", 22, 'wing',
    [k(.15, 'pole_low', reach=.5, x=.2), k(.35, 'pole_low_r', reach=1, x=.6, b=-.6, l=1, mark='la'), k(.55, 'pole_mid_r', reach=1, x=-.4, b=-.6, r=1, mark='la'), k(.75, 'pole_mid', reach=1, x=.6, b=-.6, l=1, mark='la'), k(.9, reach=.2, eye='^')],
    [(.55, 'maypole')], g='play', act=('dance', 'pole'), prefer=['happy', 'young'])
o.r('race_to_the_pole_and_back', "A race to the pole and back, slapping it at the turn", 16, 'none',
    [k(.2, x=-1.6, b=-1.6, w=1, eye='>'), k(.4, 'pole_mid', x=1.6, b=-1.6, l=1, eye='>', mark='TAG'), k(.65, x=-1.6, b=-1.6, r=1, eye='>'), k(.85, x=.4, y=.6, eye='O', mark='...')],
    [], g='play', act=('race', 'pole'), prefer=['happy'])
o.r('chase_a_friend_round_the_pole', "Chasing a friend round the pole, the pair of them circling its foot", 24, 'none',
    [k(.15, 'pole_low', x=.8, b=.4, eye='>'), k(.35, 'pole_low_r', x=2.6, b=-1.6, w=1, eye='>', mark='HA'), k(.6, 'pole_mid_r', x=2.6, b=-1.6, r=1, eye='>', y=.8), k(.85, x=1.4, y=.6, eye='O', mark='...')],
    [(.6, 'maypole')], g='play', act=('chase', 'pole'), prefer=['happy'],
    duo=[k(.15, 'pole_low_r', x=.4, b=.4, eye='o'), k(.4, 'pole_mid', x=1.6, b=-1.6, w=1, eye='>'), k(.65, 'pole_low', x=1.6, b=-1.6, l=1, eye='>'), k(.85, x=.4, eye='^')],
    say=["Chased a friend round a pole. The pole stayed neutral.", "Caught a friend. Released on pole-parole."])
o.r('hop_from_the_slab_to_the_ledge', "Hopping up from the foot slab to peck the top of the pole, again and again", 20, 'none',
    [k(.15, 'foot_mid', perch=1, b=.6), k(.35, 'pole_top', x=1.6, y=-.4, b=-2.4, w=1, mark='tk'), k(.55, 'foot_mid', perch=1, b=.6), k(.8, 'pole_top', x=1.6, y=-.4, b=-2.4, w=1, eye='^', mark='tk')],
    [], g='play', act=('hop', 'pole_top'), prefer=['happy', 'young'], obj=[(.35, dict(shake=.05)), (.8, dict(shake=.05))])
o.r('hop_and_bump_the_pole', "Hopping at the pole and bumping it with his chest, harder each time", 18, 'none',
    [k(.15, 'pole_mid', x=-.4, b=.8), k(.3, 'pole_mid', x=-1, y=.8, b=-1.4, mark='bump'), k(.5, 'pole_high', x=-1.4, y=.8, b=-1.8, w=.6, mark='BUMP'), k(.7, 'pole_high', x=-1.8, y=.8, b=-2.2, w=1, mark='BUMP'), k(.88, x=0, eye='^')],
    [], g='play', act=('hop', 'pole'), prefer=['happy', 'young'], obj=[(.3, dict(shake=.04)), (.5, dict(shake=.06)), (.7, dict(shake=.09))])
o.r('try_to_climb_the_pole', "Trying to climb the pole, flapping up it two hops and sliding back down every time", 22, 'none',
    [k(.15, 'pole_low', x=.6, y=.2, b=.4), k(.3, 'pole_mid', x=.8, y=-.6, b=-1.4, w=1, mark='flap'), k(.5, 'pole_high', x=.8, y=-.8, b=-1.8, w=1, mark='flap'), k(.7, 'pole_low', x=.2, y=.6, b=1, l=1, r=1, eye='@', mark='squeak'), k(.88, y=.2, eye='-')],
    [], g='play', act=('climb', 'pole'), prefer=['young'])
# --- test
o.r('count_the_nail_heads', "Counting the nail heads along the plank wall with the tip of a wing, tapping each one", 22, 'wing',
    [k(.15, 'wall_nail', reach=.5, x=.2, y=-.4), k(.4, 'wall_nail', reach=1, x=1.5, y=-.6, mark='one'), k(.65, 'plate_l', reach=1, x=1.5, y=-.6, mark='two'), k(.85, eye='@', mark='...', x=0.9)],
    [], g='test', act=('count', 'nails'), ages=['adult', 'mature', 'elder', 'legendary'], prefer=['curious'])
o.r('measure_himself_on_the_pole', "Measuring himself against the pole, standing back to it with a wing flat on his crown", 20, 'wing',
    [k(.15, 'pole_low', reach=.4, x=-.4, y=-.2), k(.4, 'pole_mid', reach=1, x=-.2, y=-1.8, b=.4, mark='hm'), k(.65, 'pole_high', reach=1, x=-.2, y=-1.8, b=.8, eye='^', mark='...'), k(.88, reach=.1, eye='-')],
    [], g='test', act=('measure', 'pole'), prefer=['curious', 'young'])
o.r('listen_at_the_door', "Listening at the door with his cheek on the perch bar for any sound inside", 20, 'none',
    [k(.2, 'perch_bar', x=.4, y=-.4, b=-.2), k(.4, 'perch_bar', x=.8, y=-.8, b=-.4, eye='o', mark='...'), k(.65, 'perch_bar', x=.8, y=-.8, b=-.4, eye='O', mark='...'), k(.85, x=0, eye='-')],
    [], g='test', act=('listen', 'door'), ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], prefer=['curious'])
o.r('taste_the_pole', "Tasting the pole with one lick to find out what weather tastes like", 14, 'none',
    [k(.2, 'pole_low', x=.6, y=.6, b=.6), k(.4, 'pole_low', x=2.6, y=1.2, b=.8, eye='o', mark='lick'), k(.65, 'pole_high', x=-2.4, y=-1.8, eye='@', mark='ptoo'), k(.85, x=1, eye='-')],
    [], g='test', act=('taste', 'pole'),
    say=["Wood, rain, bird. Not food, not even insulting food.", "Tastes like somebody else's front door."])
o.r('balance_on_the_foot_slab', "Balancing on one foot on the foot slab, switching feet when it gets hard", 22, 'none',
    [k(.15, 'foot_l', perch=1, x=.2, y=.4), k(.35, 'foot_l', perch=1, x=.4, y=.4, b=.4, l=1, w=1, eye='o'), k(.6, 'foot_r', perch=1, x=-.4, y=.4, b=.6, r=1, w=1, eye='O', mark='whoa'), k(.85, 'foot_r', perch=1, x=0, eye='^')],
    [], g='test', act=('balance', 'foot'), prefer=['young', 'happy'],
    say=["Slab, foot, wobble. Knees in the wind.", "One foot, one slab, zero dignity. Ten out of ten."])
# --- rest
o.r('lean_on_the_pole', "Leaning his back against the pole with his chin up and his eyes half shut", 22, 'none',
    [k(.2, 'pole_low', x=-.4, y=.2, b=.4), k(.4, 'pole_low', x=-2.4, y=-1.8, b=1.6, eye='-', w=.4), k(.7, 'pole_mid', x=-2.8, y=-1.8, b=2, w=1, eye='-', mark='mm'), k(.9, y=0, eye='^', x=0.9)],
    [], g='rest', act=('lean', 'pole'), prefer=['tired'])
o.r('hug_the_pole', "Wrapping both wings round the pole and holding on with his cheek against the wood", 24, 'wing',
    [k(.2, 'pole_low', reach=.5, x=.4, y=.8, b=.4), k(.45, 'pole_mid', reach=1, x=.8, y=1.6, b=1, eye='-'), k(.75, 'pole_mid_r', reach=1, x=1, y=1.8, b=1.2, w=.4, eye='-', mark='mm'), k(.9, reach=.2, y=.6, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'pole'), when=['lonely'],
    say=["Hugged a pole. It's the most reliable friend I have.", "Don't ask what I whispered into the wood."])
o.r('nap_curled_on_the_foot_slab', "Napping curled up on the foot slab with his bill tucked under a wing", 28, 'none',
    [k(.2, 'foot_l', perch=1, x=.4, y=.8, b=.6), k(.4, 'foot_l', perch=1, y=1.4, b=1.2, eye='-', x=0.9), k(.7, 'foot_l', perch=1, y=1.5, b=1.2, eye='-', mark='zzz', x=0.9), k(.9, y=.2, b=.3, eye='^', x=0.9)],
    [(.4, 'snooze')], g='rest', act=('nap', 'foot'), prefer=['tired', 'night'])
o.r('sulk_at_the_pole', "Sulking at the pole with his back turned to the house above", 22, 'none',
    [k(.2, 'pole_low_r', x=-.9, y=1.4, b=.2, l=1), k(.45, 'pole_low_r', x=-3, y=1.8, b=.8, eye='-'), k(.75, 'pole_low_r', x=-3.2, y=2.2, b=.8, r=1, eye='-', mark='hmph'), k(.9, y=.2, eye='-', x=0.9)],
    [], g='rest', act=('sulk', 'pole'), when=['sad'],
    say=["House has a door and a view. I have a pole.", "Sulking costs nothing. Best deal I've had."])
o.r('warm_against_the_sunny_pole', "Warming his cheek and chest against the sun-baked pole until the chill leaves his feathers", 24, 'none',
    [k(.2, 'pole_high', x=.4, y=.4, b=.4), k(.4, 'pole_high', x=1.4, y=1.2, b=1.2, eye='-'), k(.75, 'pole_mid_r', x=1.6, y=1.6, b=1.6, eye='-', mark='mm'), k(.9, y=.2, eye='^')],
    [], g='rest', act=('warm', 'pole'), when=['sun', 'cold'])
# --- show
o.r('shout_up_at_the_roof', "Shouting up at the roof, demanding whoever owns it come down", 18, 'none',
    [k(.2, x=.2, y=-1.2, w=.4, eye='>'), k(.4, x=2.4, y=-2.4, b=.8, w=.8, l=1, eye='>', mark='OI'), k(.65, x=2.4, y=-2.4, b=1.2, w=1, r=1, eye='>', mark='COME DOWN'), k(.85, x=-1.4, eye='-')],
    [], g='show', act=('shout', 'roof'), far=True, prefer=['grumpy'],
    say=["Shouted at the roof. Roof's got height and no manners.", "Nobody's in. Probably. Rude either way."][:1] + ["I'll wait. I've got all day and no plans."])
o.r('sing_up_the_pole', "Singing up the pole to the empty doorway, bill pressed to the wood to carry the note", 22, 'none',
    [k(.2, 'pole_high', x=.6, y=-.6), k(.4, 'pole_high', x=1.6, y=-1.6, b=.4, w=.6, eye='O', mark='la'), k(.65, 'pole_high_r', x=1.6, y=-1.6, b=.4, w=1, eye='O', mark='LAAA'), k(.85, x=0, eye='^')],
    [], g='show', act=('sing', 'house'), prefer=['happy'], obj=[(.4, dict(shake=.04)), (.65, dict(shake=.06))],
    say=["Sang up the pole. The pole hummed along and did the harmony.", "Sang a lullaby to an empty house. It slept."])
o.r('drum_on_the_pole', "Drumming a solo on the pole with his bill, low end then high", 20, 'none',
    [k(.15, 'pole_low', x=.8, y=.4, b=.4), k(.3, 'pole_low', x=1.4, y=.4, mark='dum'), k(.5, 'pole_mid', x=1.4, y=.2, b=.4, mark='dum'), k(.7, 'pole_high', x=1.4, y=-.2, mark='DUM'), k(.88, x=-.4, y=-1.8, w=1, eye='^', mark='tsss')],
    [], g='show', act=('drum', 'pole'), prefer=['happy'], obj=[(.3, dict(shake=.04)), (.5, dict(shake=.05)), (.7, dict(shake=.06))])
o.r('argue_with_the_doorway', "Arguing up at the house from the pole's top, bill jabbing at the doorway", 20, 'none',
    [k(.2, 'pole_top', x=1.4, y=-.6, eye='>'), k(.4, 'pole_top', x=1.8, y=-.8, b=.4, mark='quack'), k(.6, 'pole_top', x=1.6, y=-1, eye='>', mark='QUACK'), k(.85, x=-.8, y=.4, eye='-', mark='hmph')],
    [], g='show', act=('argue', 'house'), ages=['duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'], prefer=['grumpy'],
    say=["Told the house what I think. It didn't answer, so I win.", "House has no windows. Smart. Dodges all feedback."])
o.r('show_the_house_to_a_friend', "Showing a friend the house with a long wing sweep from the pole up to the doorway", 22, 'wing',
    [k(.15, 'pole_low', reach=.5, x=.2), k(.4, 'pole_high', reach=1, x=1.4, y=-.6, w=.4, mark='behold'), k(.65, 'pole_top', reach=1, x=1.4, y=-.8, mark='the house'), k(.88, y=-.2, eye='^', x=0.9)],
    [(.65, 'admire')], g='show', act=('show', 'house'), prefer=['happy'],
    duo=[k(.15, 'pole_low_r', x=.2, eye='o'), k(.4, 'pole_mid_r', x=.6, y=-1, eye='O', mark='ooh'), k(.7, 'pole_mid_r', x=.6, y=-1.4, eye='^'), k(.88, eye='^')],
    say=["Showed a friend the house. They were impressed. They're easily impressed.", "Admired the doorway together. Nobody went in."][:1] + ["That's the whole tour. Gift shop's closed."])
# --- mishap
o.r('kick_the_pole', "Kicking the pole in a temper and hopping away holding his toe", 16, 'none',
    [k(.2, 'pole_low', x=-1.2, y=.2, l=1), k(.4, 'pole_low', x=-3, y=.2, l=1, b=1, mark='THWK'), k(.6, x=2, y=1, b=.4, r=1, eye='O', mark='ow'), k(.82, x=2.6, y=2.2, r=1, b=1.4, eye='@')],
    [(.4, 'scuff')], g='mishap', act=('kick', 'pole'), prefer=['grumpy'], obj=[(.4, dict(shake=.06))],
    say=["Kicked the pole. The pole kicked back, with the wood.", "The big toe wants a lawyer."])
o.r('slipped_on_the_wet_slab', "Landing on the wet foot slab, losing his footing, and slipping off onto his tail", 16, 'none',
    [k(.2, 'foot_r', perch=1, x=.8, y=.6, b=.6), k(.4, 'foot_r', perch=1, x=.4, y=.2, b=-.6, l=1, r=1, eye='O', mark='whoa'), k(.6, x=-1.8, y=1.6, b=1.6, eye='@', mark='splat'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('slip', 'foot'), when=['obj_wetness>.3'])
o.r('knocked_his_head_on_the_ledge', "Standing up from the pole's foot and knocking his head on the front ledge", 16, 'none',
    [k(.2, 'pole_high', x=.2, y=.4, b=.8), k(.4, 'ledge', x=1.4, y=-1.4, b=-1.6, eye='O'), k(.55, 'ledge', x=1.2, y=-1.8, b=-2, eye='@', mark='BONK'), k(.8, x=-1.4, y=1.4, b=1, eye='-')],
    [], g='mishap', act=('knock', 'ledge'), ages=['juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'], obj=[(.55, dict(shake=.06))],
    say=["Ledge 1, skull 0. Rematch denied.", "That's a hard step for a soft head."])
o.r('hopped_for_the_perch_and_missed', "Hopping for the perch bar, missing, and bouncing off the door onto his tail", 16, 'none',
    [k(.2, x=.6, b=.8, eye='>'), k(.4, 'perch_bar', x=2.4, b=-2, w=1, mark='hup'), k(.6, x=-2.8, y=1.8, b=1.6, l=1, r=1, eye='@', mark='thud'), k(.85, y=.6, eye='-', x=0.9)],
    [], g='mishap', act=('hop', 'perch'), ages=GROWN, prefer=['young'], obj=[(.4, dict(shake=.06))])
o.r('shook_the_pole_and_wore_the_snow', "Shaking the pole to drop the snow off the roof, and wearing all of it", 20, 'none',
    [k(.2, 'pole_mid', x=-.8, y=.4, b=.4), k(.4, 'pole_mid', x=-1.6, y=.6, b=1.6, mark='HNNG'), k(.55, 'pole_mid', x=-1.6, y=.6, b=-1.4, eye='O', mark='FLUMP'), k(.8, x=.4, y=1.8, b=1.4, eye='@')],
    [(.55, 'clear')], g='mishap', act=('shake', 'pole'), when=['snowcap>.3'], obj=[(.4, dict(shake=.14)), (.55, dict(shake=.12))],
    say=["Shook the pole. All the snow, one duck. Efficient.", "Feels like a hat. A cold one."])
o.emit()

# ============================================================ rubber_duck
# Blueprint: type 'duck', style 'rubber' (playground-workshop): a big bath duck facing right on a flat base rim with ripples below it:
# round head with an eye and a flat bill, a wing mark on the flank, a pointed tail at the left, a rounded belly. 134 px tall. The
# squeak is the toy's whole point. It is a toy, not a pet: nothing here treats it as alive.
o = Obj('rubber_duck', 'placed',
        parts=dict(tail='the pointed tail at the left', flank='the flank behind the wing', belly='the rounded belly', wing='the wing mark on the side',
                   back='the humped back', chest='the chest at the right', neck='the neck', cheek='the cheek below the eye', eye='the painted eye',
                   bill='the big flat bill', crest='the top of the head', base='the flat base rim', ripple='the ripples drawn below the base'),
        fields=dict(leaves=(0, 0, 1), snowcap=(0, 0, 1), heat=(0, 0, 1), frost=(0, 0, 1)),
        physics=[('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm'),
                 ('heat', 'rate', .002, 'sun'), ('heat', 'rate', -.001, '!sun'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], polish=[('obj.dirt', 'add', -.2)], scrape=[('obj.dirt', 'add', -.2)], scour=[('obj.dirt', 'add', -.25)],
            sweep=[('leaves', 'set', 0)], knock_snow=[('snowcap', 'mul', .2)], cool=[('heat', 'mul', .5)],
            squeak=[('need.fun', 'add', 2)], honk=[('need.fun', 'add', 1.5)], snooze=[('need.energy', 'add', 3)], company=[('need.social', 'add', 2)],
            dry=[('obj.wetness', 'add', -.4)], chip=[('frost', 'mul', .2)], splat=[('snowcap', 'mul', .3), ('need.cleanliness', 'add', -1)],
            scuff=[('obj.condition', 'add', -.25)], smooth=[('obj.condition', 'add', .4)]),
        anchors=dict(base_l=(.255, .838, 'surface'), base_mid=(.49, .838, 'surface'), base_r=(.725, .838, 'surface'),
                     ripple_l=(.392, .865, 'surface'), ripple_r=(.608, .865, 'surface'), tail_tip=(.098, .649), flank_l=(.157, .703),
                     belly_low=(.608, .784), belly_mid=(.51, .676, 'inside'), belly_r=(.745, .703),
                     wing_mark=(.392, .595), back_hump=(.235, .514), chest_r=(.863, .595), chest_hi=(.843, .486),
                     neck_back=(.51, .378), neck_front=(.863, .378), cheek=(.863, .243), eye_spot=(.706, .243),
                     bill_tip=(.902, .324), crest=(.686, .108)),
        marks=[('snowcap', .3, '.:*:.', 'crest', 'snow'), ('leaves', .3, ',;,.;', 'ripple_l', 'leaf'), ('frost', .3, '*.*.*', 'flank_l', 'frost'),
               ('heat', .5, '~ ~ ~', 'back_hump', 'glow')])
# --- care
o.r('wipe_the_belly', "Giving the belly a long wipe with a wing, low curve to the right side", 18, 'wing',
    [k(.15, 'belly_low', reach=.6, x=.4, y=.6), k(.35, 'belly_low', reach=1, x=.8, y=.6, b=.6, mark='fff'), k(.55, 'belly_mid', reach=1, x=.8, y=.4, b=.4, mark='fff'), k(.75, 'belly_r', reach=1, x=.8, y=.2, mark='fff'), k(.9, eye='^')],
    [(.75, 'wipe')], g='care', act=('wipe', 'belly'), when=['obj_dirt>.3'], obj=[(.35, dict(sway=.1)), (.75, dict(sway=-.1))],
    say=["Belly's wiped. It's still a belly. I still did it.", "Rubber shines. Smug rubber, now."])
o.r('buff_the_bill', "Polishing the big flat bill with the feathers of his chest until it shines", 18, 'none',
    [k(.2, 'bill_tip', x=-.8, y=-.6, b=.4), k(.4, 'bill_tip', x=-1.4, y=-1.8, w=.4, mark='squk'), k(.6, 'bill_tip', x=-1.8, y=-1.8, w=.8, mark='squk'), k(.85, eye='^')],
    [(.6, 'polish')], g='care', act=('polish', 'bill'), when=['obj_dirt>.3'], ages=GROWN, obj=[(.4, dict(sway=.1)), (.6, dict(sway=-.1))],
    say=["Bill's gleaming. I could see me in it, if I looked.", "Chest feathers: the only cloth I own."])
o.r('pick_the_base_seam', "Scraping grime out of the base rim with his bill, working from the left end to the right", 18, 'none',
    [k(.2, 'base_l', x=.9, y=.8, b=.6), k(.4, 'base_l', x=1.4, y=1.2, b=.8, mark='tk'), k(.6, 'base_mid', x=1.4, y=1.2, b=.8, mark='tk'), k(.8, 'base_r', x=1.4, y=1.2, b=.8, mark='tk'), k(.92, y=.2, eye='^')],
    [(.8, 'scrape')], g='care', act=('scrape', 'base'), when=['obj_dirt>.3'])
o.r('sweep_leaves_off_the_ripples', "Sweeping the leaves that have drifted round its base off the ripples with a wing", 18, 'wing',
    [k(.15, 'ripple_l', reach=.5, x=.3, y=.6), k(.4, 'ripple_l', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.62, 'ripple_r', reach=1, x=.7, y=.8, b=.6, mark='fshh'), k(.85, eye='^')],
    [(.62, 'sweep')], g='care', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['fall'])
o.r('scrub_the_wing_mark', "Scrubbing the dried mud out of the wing mark with a wing of his own", 18, 'wing',
    [k(.15, 'wing_mark', reach=.5, x=.3, y=.4), k(.35, 'wing_mark', reach=1, x=.9, y=.2, b=.8, l=1, mark='skrt'), k(.55, 'flank_l', reach=1, x=.9, y=.2, b=.8, r=1, mark='skrt'), k(.8, 'wing_mark', reach=1, x=.5, y=.2, b=.4, eye='^')],
    [(.55, 'scour')], g='care', act=('scrub', 'wing'), when=['obj_dirt>.3'], ages=['juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary'])
o.r('rub_the_damp_back_dry', "Backing up to the damp hump of the back and drying it with his tail feathers", 18, 'none',
    [k(.2, 'back_hump', x=-.9, y=-.4, b=.2, l=1), k(.45, 'back_hump', x=-1.9, y=-.4, b=1.2, w=.3, mark='fff'), k(.7, 'back_hump', x=-1.9, y=-.6, b=1, w=.9, r=1, mark='fff'), k(.88, eye='^', w=.2)],
    [(.7, 'dry')], g='care', act=('dry', 'back'), when=['obj_wetness>.3'], ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'])
o.r('mend_the_scuffed_base', "Mending the scuffed base rim by rubbing the rubber smooth again with a wing", 18, 'wing',
    [k(.15, 'base_l', reach=.5, x=.3, y=.6), k(.4, 'base_l', reach=1, x=1, y=1.2, b=.6, mark='rrb'), k(.62, 'base_mid', reach=1, x=1, y=1.2, b=.8, mark='rrb'), k(.85, y=.4, eye='^')],
    [(.62, 'smooth')], g='care', act=('mend', 'base'), when=['obj_condition<.6'],
    say=["Rubbed it smooth. Good as scuffed. Better, nearly.", "Fixed my own damage. Growth, I think."])
# --- weather
o.r('knock_the_snow_cap_off', "Knocking the snow cap off its head with a twig, topmost bit first", 20, 'twig',
    [k(.15, 'crest', reach=.6, y=-.6, x=.3), k(.4, 'crest', reach=1, x=1.9, y=-.8, mark='whap'), k(.6, 'crest', reach=1, x=1.9, y=-.8, mark='fshh'), k(.85, y=-.3, eye='^', x=1.17)],
    [(.6, 'knock_snow')], g='weather', act=('knock', 'snow'), when=['snowcap>.4'], ages=GROWN, obj=[(.4, dict(sway=.2)), (.6, dict(shake=.2))],
    say=["Snow off the head. It looks relieved, as much as rubber can.", "Hat's gone. Duck's still dumber than it looks."])
o.r('fan_the_hot_back', "Fanning the sun-baked back with a wing until the heat comes off it, cooling it down", 20, 'wing',
    [k(.15, 'back_hump', reach=.5, x=.3), k(.35, 'back_hump', reach=1, x=.5, y=.6, b=.4, mark='fwp'), k(.55, 'back_hump', reach=.3, x=.3, y=.4), k(.75, 'back_hump', reach=1, x=.5, y=.6, b=.4, mark='fwp'), k(.9, eye='^')],
    [(.75, 'cool')], g='weather', act=('cool', 'back'), when=['heat>.5'], ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'])
o.r('chip_frost_off_the_tail', "Chipping the frost off the tail point and flank with the edge of his bill", 18, 'none',
    [k(.2, 'tail_tip', x=.8, y=.6, b=.6), k(.4, 'tail_tip', x=1.4, y=.8, b=.8, mark='tik'), k(.6, 'flank_l', x=1.4, y=.8, b=.6, mark='tik'), k(.85, eye='^')],
    [(.6, 'chip')], g='weather', act=('chip', 'tail'), when=['frost>.3'])
o.r('brace_against_the_flank_in_the_gale', "Bracing his shoulder against the flank while the gust tries to push the duck over", 24, 'none',
    [k(.2, 'flank_l', x=-.4, y=.2, b=.4), k(.4, 'flank_l', x=-2.7, y=.6, b=1.6, w=.6, eye='>', mark='fff'), k(.7, 'flank_l', x=-3.5, y=1.6, b=2.4, w=1, l=1, eye='>'), k(.9, y=0, eye='^', x=1.17)],
    [], g='weather', act=('brace', 'flank'), when=['windy'], obj=[(.3, dict(sway=.3)), (.5, dict(sway=-.3)), (.7, dict(sway=.3))],
    say=["Gust shoved the duck, I shoved back. Rubber one, wind nil.", "Stood my ground. The duck stood its base."])
o.r('shelter_in_the_ducks_lee', "Taking shelter on the lee side of the big duck as the storm blows over, bill low", 32, 'none',
    [k(.2, 'flank_l', x=-.4, y=.6, b=.6), k(.4, 'flank_l', x=-2.5, y=1.2, b=1.4, eye='-'), k(.7, 'flank_l', x=-2.5, y=1.4, b=1.6, eye='-', mark='brr'), k(.9, y=.2, eye='^', x=1.17)],
    [], g='weather', act=('shelter', 'flank'), when=['storm', 'wet'])
# --- use
o.r('squeeze_the_belly', "Squeezing the belly between both wings until it gives one long dry squeak", 16, 'wing',
    [k(.2, 'belly_mid', reach=.6, x=.3, b=.4), k(.4, 'belly_mid', reach=1, x=.9, b=.8, mark='squuueak'), k(.6, 'belly_mid', reach=.4, x=.3, b=.2), k(.85, eye='^')],
    [(.4, 'squeak')], g='use', act=('squeeze', 'belly'), prefer=['happy', 'curious'], obj=[(.4, dict(shake=.3, puff=.3)), (.6, dict(sway=.2))],
    say=["Squeak. Honest noise. Better than most things I say.", "One note, and it sticks to it."])
o.r('stand_on_the_tail', "Pressing down on the tail point with his whole weight until the squeak comes from the other end", 16, 'none',
    [k(.2, 'tail_tip', x=-.4, y=.6, l=1), k(.4, 'tail_tip', x=-.6, y=1, b=.8, l=1, mark='squk'), k(.6, 'tail_tip', x=-.6, y=1, b=1.2, r=1, mark='SQUK'), k(.85, eye='^')],
    [(.4, 'squeak')], g='use', act=('press', 'tail'), obj=[(.4, dict(sway=.3, puff=.3)), (.6, dict(sway=-.2, puff=.3))])
o.r('rock_it_by_the_flank', "Shoving the flank so the whole duck rocks on its base and keeps rocking", 18, 'none',
    [k(.2, 'wing_mark', x=-.8, y=.6), k(.4, 'flank_l', x=1.6, y=.8, b=.8, mark='hup'), k(.6, x=.6, y=.8, eye='o'), k(.82, x=.6, y=.6, eye='O')],
    [], g='use', act=('rock', 'body'), prefer=['happy', 'young'], obj=[(.4, dict(sway=.8)), (.6, dict(sway=-.7)), (.8, dict(sway=.5))])
o.r('nod_it_by_the_cheek', "Pushing the cheek down and letting go so the head bobs up and down like it agrees", 18, 'wing',
    [k(.15, 'cheek', reach=.6, x=.4, y=-.6), k(.35, 'cheek', reach=1, x=.7, y=-.4, b=.6, mark='nnh'), k(.5, x=-.8, y=-.4, eye='o'), k(.7, 'cheek', reach=1, x=.7, y=-.4, b=.6, mark='nnh'), k(.88, eye='^')],
    [], g='use', act=('push', 'cheek'), ages=GROWN, obj=[(.35, dict(sway=.4)), (.55, dict(sway=-.3)), (.75, dict(sway=.3))])
o.r('tilt_the_tail_with_a_twig', "Hooking a twig round the tail point and tilting the whole duck back on its base", 22, 'twig',
    [k(.15, 'tail_tip', reach=.6, y=.3, x=.3), k(.4, 'tail_tip', reach=1, x=-.6, y=.5, b=.8, mark='hnf'), k(.6, 'tail_tip', reach=1, x=-1.2, y=.6, b=1.2, l=1), k(.8, x=.6, y=.2, eye='o', mark='...')],
    [], g='use', act=('tilt', 'tail'), obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.5)), (.8, dict(sway=.2))])
o.r('play_the_duck_like_an_organ', "Squeezing the belly while a friend leans on the tail, squeaking out a tune between them", 24, 'wing',
    [k(.15, 'belly_low', reach=.5, x=.3), k(.3, 'belly_low', reach=1, x=.9, b=.8, mark='squek'), k(.5, 'belly_r', reach=.5, x=.3, b=.2), k(.7, 'belly_r', reach=1, x=.9, b=.8, mark='SQUEK'), k(.88, eye='^')],
    [(.7, 'honk')], g='use', act=('squeeze', 'tune'), prefer=['happy'], obj=[(.3, dict(puff=.3)), (.7, dict(puff=.3, sway=.2))],
    duo=[k(.15, 'tail_tip', x=-.2), k(.4, 'tail_tip', x=-.6, y=.8, b=.8, mark='sqk'), k(.6, 'tail_tip', x=-.2), k(.8, 'tail_tip', x=-.6, y=.8, b=.8, mark='SQK'), k(.92, eye='^')],
    say=["Two ducks, one duck. Four squeaks, no melody. Our best work.", "Jazz, if jazz was a rubber bath toy."])
o.r('boop_the_bill_tip', "Nudging the tip of its bill with his own, then dodging back and daring it to nudge back", 14, 'none',
    [k(.2, 'bill_tip', x=1, y=-.4, b=-.4), k(.4, 'bill_tip', x=1.8, y=-.6, b=-.8, mark='boop'), k(.6, x=-1.2, y=.2, b=.4, eye='>'), k(.82, x=.8, y=-.2, eye='o')],
    [], g='use', act=('nudge', 'bill'), ages=GROWN, obj=[(.4, dict(sway=.2))],
    say=["Booped it. It didn't boop back. It never does. Coward.", "Bill to bill. Short on conversation."])
# --- play
o.r('race_round_and_slap', "A race round the duck, slapping its flank at the end of every lap", 18, 'wing',
    [k(.15, x=-1.6, b=.8, eye='>'), k(.35, 'flank_l', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.55, 'belly_r', reach=1, x=.8, b=-1.6, mark='SLAP'), k(.8, x=1.2, eye='^')],
    [], g='play', act=('race', 'duck'), prefer=['happy', 'young'], obj=[(.35, dict(sway=.2)), (.55, dict(sway=-.2))])
o.r('sumo_bump', "Shoving the duck with his belly like a sumo wrestler, backing off and going in again", 18, 'none',
    [k(.2, 'belly_low', x=-1.4, y=.6, b=.6), k(.4, 'belly_low', x=2.4, y=.8, b=.8, mark='BUMP'), k(.6, x=-1.4, y=.6, b=.4), k(.8, 'belly_low', x=2.4, y=.8, b=.8, mark='BUMP')],
    [], g='play', act=('shove', 'belly'), prefer=['grumpy', 'happy'], obj=[(.4, dict(sway=.6, shake=.2)), (.8, dict(sway=.8, shake=.3))],
    say=["Sumo rules: bump, back up, bump. It lost on points.", "Belly to belly. Mine's the squishier opinion."])
o.r('hide_and_seek_round_the_duck', "Hide and seek round the duck's tail and chest, popping out at the other side", 20, 'none',
    [k(.2, 'tail_tip', x=-1.2, y=.8, b=.6, eye='o'), k(.4, 'chest_r', x=2.7, y=0, eye='O'), k(.6, 'tail_tip', x=-2.5, y=.8, b=.6, eye='o'), k(.8, 'chest_r', x=2.7, y=0, eye='O', mark='ha')],
    [], g='play', act=('hide', 'duck'), prefer=['curious', 'young'])
o.r('splash_in_the_ripples', "Splashing in the ripples below the base, one foot then the other, till the duck gets the spray", 20, 'none',
    [k(.15, 'ripple_l', perch=1, l=1, b=.4), k(.35, 'ripple_l', perch=1, l=1, b=-.8, mark='splsh'), k(.6, 'ripple_r', perch=1, r=1, b=-.8, mark='splsh'), k(.85, 'ripple_r', perch=1, b=-1, w=1, eye='^', mark='SPLSH')],
    [], g='play', act=('splash', 'ripples'), prefer=['happy', 'young'])
o.r('dance_with_the_duck', "Dancing a slow waltz with the duck, a wing on its chest, leading it round with every step", 24, 'wing',
    [k(.15, 'chest_r', reach=.5, x=.2), k(.35, 'chest_r', reach=1, x=1.9, y=-.4, b=.4, l=1, mark='one'), k(.55, 'chest_hi', reach=1, x=-1.7, y=-.4, b=.4, r=1, mark='two'), k(.75, 'chest_r', reach=1, x=1.9, y=-.4, b=.4, l=1, mark='three'), k(.9, reach=.2, eye='^')],
    [], g='play', act=('dance', 'duck'), prefer=['happy'], ages=GROWN, obj=[(.35, dict(sway=.2)), (.55, dict(sway=-.2)), (.75, dict(sway=.2))])
o.r('shove_it_from_both_sides', "Shoving the duck's back while a friend shoves its chest, rocking it between them", 24, 'none',
    [k(.15, 'back_hump', x=-.6, y=.4, b=.4), k(.35, 'back_hump', x=-1.8, y=.6, b=1.4, mark='hup'), k(.6, 'back_hump', x=-.6, y=.4, b=.4), k(.8, 'back_hump', x=-1.8, y=.6, b=1.4, mark='HUP'), k(.92, eye='^')],
    [], g='play', act=('shove', 'flank'), ages=GROWN, obj=[(.35, dict(sway=.5)), (.6, dict(sway=-.5)), (.8, dict(sway=.7))],
    duo=[k(.15, 'chest_r', x=.4), k(.4, 'chest_r', x=1.6, y=.6, b=1.2, mark='hup'), k(.65, 'chest_r', x=.4), k(.85, 'chest_r', x=1.6, y=.6, b=1.2, mark='HUP')])
# --- test
o.r('peer_into_the_painted_eye', "Peering into the painted eye, nose to nose, to see if it blinks", 20, 'none',
    [k(.2, 'cheek', x=.6, y=-.4), k(.4, 'eye_spot', x=1.4, y=-.8, eye='o', mark='...'), k(.65, 'eye_spot', x=1.8, y=-1, b=.2, eye='O', mark='...'), k(.85, x=-.6, eye='-')],
    [], g='test', act=('peer', 'eye'), ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], prefer=['curious'],
    say=["It never blinked. Painted open. Cheating.", "Won on a technicality. The technicality's rubber."])
o.r('taste_the_rubber', "Tasting the flank with one lick to find out what bath rubber tastes like", 14, 'none',
    [k(.2, 'belly_low', x=.6, y=.6, b=.6), k(.4, 'belly_low', x=2.9, y=1.2, b=.8, eye='o', mark='lick'), k(.65, 'flank_l', x=-2.7, y=-1.8, eye='@', mark='ptoo'), k(.85, x=1.3, eye='-')],
    [], g='test', act=('taste', 'flank'),
    say=["Rubber, bleach, someone's childhood, boiled.", "Smells like a bathroom. Not mine. I use the pond."])
o.r('knock_on_the_belly', "Knocking on the belly twice to hear what is inside", 14, 'none',
    [k(.2, 'belly_mid', x=.8, y=.5, b=.6), k(.4, 'belly_mid', x=2.9, y=.5, mark='tok'), k(.6, 'belly_mid', x=2.1, y=.5, b=.6), k(.78, 'belly_mid', x=2.9, y=.5, mark='tok'), k(.9, x=-.4, y=-1.6, eye='o')],
    [], g='test', act=('knock', 'belly'), prefer=['curious'], obj=[(.4, dict(shake=.1)), (.78, dict(shake=.1))],
    say=["Hollow in there. Echoes. Reminds me of me.", "Something rattles. Something always rattles."])
o.r('weigh_the_chest', "Weighing the duck by leaning a wing on its chest to feel how firmly it sits", 16, 'wing',
    [k(.2, 'chest_r', reach=.5, x=.5, y=.6), k(.45, 'chest_r', reach=1, x=2.4, y=.6, b=.8, eye='>', mark='hnng'), k(.7, 'chest_r', reach=1, x=2.7, y=.8, b=1, mark='...'), k(.88, reach=.1, eye='-', x=1.17)],
    [], g='test', act=('weigh', 'chest'), obj=[(.45, dict(sway=.1))])
o.r('measure_up_to_the_neck', "Standing back to the neck and laying a wing flat to measure who is taller", 20, 'wing',
    [k(.15, 'neck_back', reach=.4, x=-.4, y=-.2), k(.4, 'neck_back', reach=1, x=1.5, y=-1.8, b=.4, mark='hm'), k(.65, 'neck_front', reach=1, x=1.5, y=-1.8, b=.8, eye='^', mark='...'), k(.88, reach=.1, eye='-', x=1.17)],
    [], g='test', act=('measure', 'neck'), ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], prefer=['curious', 'young'])
o.r('sniff_the_flank', "Sniffing along the flank for the smell of the bath it came from", 18, 'none',
    [k(.2, 'flank_l', x=.6, y=.6, b=.4), k(.4, 'wing_mark', x=1.1, y=.4, eye='o', mark='snf'), k(.6, 'back_hump', x=1.1, y=-.4, eye='O', mark='snf'), k(.82, x=0, eye='-')],
    [], g='test', act=('sniff', 'flank'), ages=GROWN, prefer=['curious'])
# --- rest
o.r('lean_on_the_flank', "Leaning his back against the flank with his chin up and his eyes half shut", 22, 'none',
    [k(.2, 'flank_l', x=-.4, y=.2, b=.4), k(.4, 'wing_mark', x=-2.7, y=-1.8, b=1.6, eye='-', w=.4), k(.7, 'wing_mark', x=-3.1, y=-1.8, b=2, w=1, eye='-', mark='mm'), k(.9, y=0, eye='^', x=1.17)],
    [], g='rest', act=('lean', 'flank'), prefer=['tired'])
o.r('nap_on_the_base_rim', "Napping curled up on the base rim with his bill tucked under a wing", 28, 'none',
    [k(.2, 'base_mid', perch=1, x=.4, y=.8, b=.6), k(.4, 'base_mid', perch=1, y=1.4, b=1.2, eye='-', x=1.17), k(.7, 'base_mid', perch=1, y=1.5, b=1.2, eye='-', mark='zzz', x=1.17), k(.9, y=.2, b=.3, eye='^', x=1.17)],
    [(.4, 'snooze')], g='rest', act=('nap', 'base'), prefer=['tired', 'night'])
o.r('hug_the_duck', "Wrapping both wings round the big duck's chest and holding on with his cheek against the rubber", 24, 'wing',
    [k(.2, 'chest_r', reach=.5, x=.4, y=.8, b=.4), k(.45, 'chest_r', reach=1, x=.9, y=1.6, b=1.2, eye='-'), k(.75, 'chest_hi', reach=1, x=1.2, y=1.8, b=1.6, w=.4, eye='-', mark='mm'), k(.9, reach=.2, y=.6, eye='^')],
    [(.45, 'company')], g='rest', act=('wrap', 'chest'), when=['lonely'],
    say=["I'm the real one. I tire and have opinions.", "It squeaked at me. First one to disagree in a week."])
o.r('sulk_at_the_tail', "Sulking at the tail point with his back turned to the duck's smug face", 22, 'none',
    [k(.2, 'tail_tip', x=-.9, y=1.4, b=.2, l=1), k(.45, 'tail_tip', x=-3.3, y=1.8, b=.8, eye='-'), k(.75, 'tail_tip', x=-3.5, y=2.2, b=.8, r=1, eye='-', mark='hmph'), k(.9, y=.2, eye='-', x=1.17)],
    [], g='rest', act=('sulk', 'tail'), when=['sad'],
    say=["Duck's got a smile painted on. Must be nice to be told.", "Sat with the quiet end. Quiet gets me."])
o.r('warm_against_the_sunny_back', "Warming his chest against the sun-baked back until the chill leaves his feathers", 24, 'none',
    [k(.2, 'back_hump', x=.4, y=.4, b=.4), k(.4, 'back_hump', x=2.7, y=1.2, b=1.2, eye='-'), k(.75, 'neck_back', x=2.9, y=1.6, b=1.6, eye='-', mark='mm'), k(.9, y=.2, eye='^', x=1.17)],
    [], g='rest', act=('warm', 'back'), when=['heat>.4', 'cold'], ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'],
    say=["Warm rubber. Better than a bed. Smells like one, too.", "Thawing against a duck. Tell no one."])
# --- show
o.r('sing_along_with_the_squeak', "Singing along with the squeak, one belly press for every note", 22, 'wing',
    [k(.15, 'belly_low', reach=.5, x=.3), k(.3, 'belly_low', reach=1, x=.8, y=-.8, b=.6, w=.6, eye='O', mark='la squeak'), k(.55, 'belly_low', reach=.4, x=.3, y=-.4), k(.75, 'belly_low', reach=1, x=.8, y=-1.2, b=.8, w=1, eye='O', mark='LA SQUEEAK'), k(.9, eye='^')],
    [(.75, 'honk')], g='show', act=('sing', 'squeak'), prefer=['happy'], obj=[(.3, dict(puff=.3)), (.75, dict(puff=.3))],
    say=["That was a lot of squeak. I now hear in ducks.", "My ears are ringing in rubber."])
o.r('shout_into_the_painted_eye', "Shouting at the painted eye to see if it'll flinch", 18, 'none',
    [k(.2, x=-.6, y=.6, b=.8, eye='>'), k(.4, x=2.2, y=-.4, b=-.6, w=.4, r=1, eye='>', mark='OI'), k(.65, x=2.4, y=-.8, b=1.6, w=.8, l=1, eye='>', mark='BLINK'), k(.85, x=-.4, eye='-')],
    [], g='show', act=('shout', 'eye'), far=True, prefer=['grumpy'],
    say=["Told the eye off. It didn't flinch. Painted on, like my patience.", "Someone's got to say it."])
o.r('argue_with_the_duck', "Arguing with the duck's smile, bill an inch from the rubber, listing its faults", 20, 'none',
    [k(.2, 'chest_r', x=1.4, y=.4, eye='>'), k(.4, 'chest_r', x=3.1, y=.6, b=.4, mark='quack'), k(.6, 'neck_front', x=2.9, y=.2, eye='>', mark='QUACK'), k(.85, x=-2.1, y=.4, eye='-', mark='hmph')],
    [], g='show', act=('argue', 'duck'), prefer=['grumpy'],
    say=["Too round, too yellow, too confident. Four stars.", "Excellent bill, dreadful tail. Critics will talk."])
o.r('drum_on_the_belly', "Drumming a solo on the belly with his bill, low curve then high, the duck ringing like a bucket", 20, 'none',
    [k(.15, 'belly_low', x=.8, y=.4, b=.4), k(.3, 'belly_low', x=2.7, y=.4, mark='dum'), k(.5, 'belly_mid', x=2.7, y=.2, b=.4, mark='dum'), k(.7, 'belly_r', x=2.7, y=.2, mark='DUM'), k(.88, x=-.4, y=-1.8, w=1, eye='^', mark='tsss')],
    [], g='show', act=('drum', 'belly'), prefer=['happy'], obj=[(.3, dict(shake=.1)), (.5, dict(shake=.1)), (.7, dict(shake=.15))],
    say=["Rain on a rubber head. A drum with a punchline.", "Sounds like thinking. Mine, usually."])
o.r('shake_the_neck_and_wear_the_snow', "Shaking the neck to dump the snow cap off the head, and wearing every flake", 20, 'none',
    [k(.2, 'neck_back', x=-.8, y=.4, b=.4), k(.4, 'neck_back', x=-2.9, y=.6, b=1.6, mark='HNNG'), k(.55, 'neck_back', x=-2.9, y=.6, b=-1.4, eye='O', mark='FLUMP'), k(.8, x=1.7, y=1.8, b=1.4, eye='@')],
    [(.55, 'splat')], g='mishap', act=('shake', 'neck'), when=['snowcap>.4'], ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], obj=[(.4, dict(shake=.3)), (.55, dict(shake=.2))],
    say=["Shook the neck. All the snow, one duck. Efficient.", "Snow hat, fitted. Colder than advertised."])
o.r('strut_in_front_of_the_duck', "Showing off in front of the duck, strutting along the base rim with wings out like the better duck", 22, 'none',
    [k(.15, 'base_l', perch=1, x=.4, w=.6), k(.35, 'base_l', perch=1, x=.8, y=-.6, w=1, l=1, eye='^'), k(.6, 'base_mid', perch=1, x=.8, y=-.6, w=1, r=1, eye='^'), k(.85, 'base_r', perch=1, x=.4, y=-.4, w=.8, l=1, eye='^', mark='ta-da')],
    [], g='show', act=('show', 'rim'), prefer=['happy', 'grown'],
    say=["Strutted past. The duck didn't look. It can't. I still won.", "Better posture, better bill, worse squeak. Even trade."])
# --- mishap
o.r('slid_on_the_wet_base', "Reaching for the wet base rim, losing his footing, and slipping down onto his tail", 16, 'none',
    [k(.2, 'base_r', x=.8, y=.6, b=.6), k(.4, 'base_r', x=.4, y=.2, b=-.6, l=1, r=1, eye='O', mark='whoa'), k(.6, x=-1.8, y=1.6, b=1.6, eye='@', mark='splat'), k(.85, y=.6, eye='-')],
    [], g='mishap', act=('slip', 'base'), when=['obj_wetness>.3'])
o.r('kick_the_base_in_a_huff', "Kicking the base rim in a temper and hopping away holding his toe", 16, 'none',
    [k(.2, 'base_l', x=-1.2, y=.2, l=1), k(.4, 'base_l', x=-3.3, y=.2, l=1, b=1, mark='THWK'), k(.6, x=2.3, y=1, b=.4, r=1, eye='O', mark='ow'), k(.82, x=2.9, y=2.2, r=1, b=1.4, eye='@')],
    [(.4, 'scuff')], g='mishap', act=('kick', 'base'), prefer=['grumpy'], obj=[(.4, dict(sway=.1))],
    say=["Kicked a duck's feet. They're rubber. Mine aren't.", "Toe says rubber hits back."])
o.r('hop_and_bounce_off_the_belly', "Hopping at the chest and bouncing off it onto his tail", 16, 'none',
    [k(.2, x=.6, b=.8, eye='>'), k(.4, 'chest_hi', x=2.7, b=-2, w=1, mark='hup'), k(.6, x=-3.1, y=1.8, b=1.6, l=1, r=1, eye='@', mark='boing'), k(.85, y=.6, eye='-', x=1.17)],
    [], g='mishap', act=('hop', 'belly'), prefer=['young'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=-.3))])
o.r('shoved_it_and_took_the_swing_back', "Shoving the duck hard, turning away, and taking a wallop to the back of the head as it rocks back", 18, 'wing',
    [k(.15, 'neck_back', reach=.6, x=.3), k(.3, 'neck_back', reach=1, x=2.2, b=.4, mark='HUP'), k(.5, x=-2.1, y=-.4, eye='^', mark='ha'), k(.68, 'flank_l', reach=.5, x=-3.1, y=1.8, b=1.8, eye='@', mark='BONK'), k(.88, y=.6, eye='-')],
    [], g='mishap', act=('shove', 'return'), ages=GROWN, obj=[(.3, dict(sway=.6)), (.55, dict(sway=-.5)), (.68, dict(shake=.2))],
    say=["Clocked from behind by a bath toy. Telling no one.", "It had a head start and a heavy bottom. Unfair."])
o.r('catch_the_tipping_duck', "Catching the tipping duck on his back before it goes over, legs shaking", 20, 'none',
    [k(.2, 'back_hump', x=-.6, y=.4, b=.6, eye='o'), k(.4, 'back_hump', x=-1.8, y=.8, b=1.8, l=1, r=1, eye='O', mark='NNGH'), k(.65, 'back_hump', x=-1.8, y=.8, b=1.6, eye='@', mark='...'), k(.85, y=.4, eye='-')],
    [], g='mishap', act=('catch', 'duck'), ages=['young_adult', 'adult', 'mature', 'elder', 'legendary'], obj=[(.3, dict(sway=.6)), (.5, dict(sway=.8, shake=.2)), (.75, dict(sway=0))])
o.r('knocked_by_the_nodding_head', "Leaning in to squint at the eye and getting knocked on the beak by the nodding head", 18, 'none',
    [k(.2, 'eye_spot', x=.6, y=-.4, eye='o'), k(.4, 'eye_spot', x=1, y=-.6, b=.4, mark='nnh'), k(.6, 'eye_spot', x=1.8, y=-1, eye='@', mark='BONK'), k(.85, x=-1, y=.8, eye='-')],
    [], g='mishap', act=('knock', 'head'), ages=GROWN, obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.4, shake=.2))])
o.emit()

# Drawing (96 x 42 cells, 7.3 px a row, standing line row 39): back rim rows 17-39 (170 px+, looked at), side walls cols 7 and 88
# from 168 px down, sand rows 23-33 (the front sand row is 44 px up), base board top edge row 34 (36 px), nine studs row 35 (29 px),
# bucket cols 13-20 rows 27-30 (66-87 px), shovel upright cols 78-80 (D grip 102 px, shaft 87-95, blade 80), a ring of ( ) with ~ at its
# top and bottom (66-102 px).
o = Obj('toy_sandbox', 'placed',
        parts=dict(sand='the sand filling the box', board='the base board along the front edge', stud='the nine studs along the base board', wall='the side walls and the back rim',
                   bucket='the bucket standing in the sand', shovel='the upright shovel by the right wall', ring='the oval ring scratched into the sand',
                   pit='the dug pit in the sand', mound='the heap of sand'),
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
                     ring_l=(0.326, 0.634), ring_r=(0.684, 0.634), ring_near=(0.505, 0.732)),
            marks=[('pit', .3, '(o o)', 'sand_deep', 'mud'), ('mound', .3, '/^^^\\', 'sand_a', 'dust'), ('tracks', .3, 'v v v', 'sand_c', 'dust'), ('water', .3, '~~~', 'bucket_rim', 'water'), ('frost', .3, '*.*.*', 'board_m', 'frost')])
# ---------------- care
o.r('sweep_board', 'Sweeping spilled sand off the base board with a wing', 16, 'wing',
    [k(.12, 'board_l', reach=.6, x=.3, y=.4), k(.3, 'board_l', reach=1, x=1.2, y=1.4, b=.6, l=1), k(.5, 'board_m', reach=1, x=1.4, y=1.6, b=.8, r=1), k(.7, 'board_r', reach=1, x=1.2, y=1.4, b=.6, l=1), k(.88, y=.6, eye='^')],
    [(.5, 'sweep')], g='care', act=('sweep', 'board'), when=['obj_dirt>.3'], prefer=['grown'])
o.r('rake_tracks', 'A rake of his feet through the sand until his own prints are gone', 18, 'none',
    [k(.15, 'sand_a', perch=1, x=.3, y=.5, b=.3), k(.3, 'sand_a', perch=1, x=.2, y=.6, b=.5, l=1), k(.5, 'sand_b', perch=1, x=.2, y=.6, b=.5, r=1), k(.7, 'sand_c', perch=1, x=.2, y=.6, b=.5, l=1), k(.88, y=.2, eye='-')],
    [(.5, 'smooth')], g='care', act=('rake', 'tracks'), when=['tracks>.3'], prefer=['curious'],
    say=["Smooth again. No evidence.", "A clean sand floor. Very innocent."])
o.r('refill_pit', 'Filling the pit back in by nosing sand over its lip until it is level', 20, 'none',
    [k(.15, x=.3, y=.5), k(.3, 'sand_c', x=1.1, y=1.3, b=.5), k(.5, 'sand_b', x=.4, y=.9, b=.4, mark='fff'), k(.7, 'sand_c', x=1.1, y=1.3, b=.5), k(.88, y=.1, w=.4, eye='-')],
    [(.5, 'refill')], g='care', act=('fill', 'pit'), when=['pit>.3'], prefer=['grown'])
o.r('plough_heap', 'Pushing the heap flat with his chest', 18, 'none',
    [k(.15, x=.5, y=.6, eye='>'), k(.35, 'sand_deep', x=.9, y=1, b=.8, mark='hrr'), k(.55, 'sand_a', x=1, y=1.1, b=.9), k(.75, x=.3, y=.4, b=.3, w=.5, eye='^')],
    [(.55, 'level')], g='care', act=('push', 'mound'), when=['mound>.3'], prefer=['grumpy'], obj=[(.35, dict(shake=0.15)), (.6, dict(shake=0.15))])
o.r('hammer_stud', 'Mending a loose stud by hammering it back down with his bill', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'stud_3', x=1, y=1.5, b=.4, mark='tak'), k(.45, x=.2, y=.4), k(.6, 'stud_3', x=1, y=1.6, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
    [(.6, 'mend')], g='care', act=('mend', 'stud'), when=['obj_condition<.6'],
    say=["Back down. You are welcome, wood.", "One stud. Lifelong enemy now."])
o.r('fan_sand_dry', 'Drying the soaked sand by fanning it with both wings from the board edge', 20, 'none',
    [k(.15, 'board_m', perch=1, x=.2, y=.2, w=.3), k(.3, 'board_m', perch=1, x=.2, y=-.2, w=1, mark='fwp'), k(.5, 'board_m', perch=1, x=.2, y=-.3, w=0), k(.7, 'board_m', perch=1, x=.2, y=-.2, w=1, mark='fwp'), k(.88, y=.2, w=.3, eye='-')],
    [(.5, 'dry')], g='care', act=('dry', 'sand'), when=['obj_wetness>.3'], prefer=['sun'])
# ---------------- use
o.r('dig_pit', 'Digging a pit with both feet flying backwards', 20, 'none',
    [k(.15, 'sand_b', perch=1, x=.3, y=.6, b=.3), k(.3, 'sand_b', perch=1, y=1.2, b=1, l=1, mark='dig'), k(.5, 'sand_b', perch=1, y=1.4, b=1.1, r=1), k(.7, 'sand_b', perch=1, y=1.4, b=1.2, l=1), k(.88, x=.2, y=.2, w=.4, eye='^')],
    [(.5, 'dig')], g='use', act=('dig', 'sand'), prefer=['happy', 'young'], obj=[(.3, dict(shake=0.15)), (.6, dict(shake=0.15))],
    say=["Down we go. Still no treasure. Typical.", "Dug it. Fell in it. In that order."])
o.r('tamp_sand_flat', 'Patting the sand firm with the flat of a wing', 16, 'wing',
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
o.r('scrape_ring_deeper', 'Digging the ring deeper by scraping along its bottom with his bill', 20, 'none',
    [k(.15, x=.4, y=.2), k(.3, 'ring_near', x=1.2, y=-.4, b=.4, mark='scr'), k(.5, 'ring_near', x=1.3, y=-.2, b=.5), k(.7, 'ring_near', x=1.2, y=-.4, b=.4, mark='scr'), k(.88, eye='^')],
    [(.5, 'trench')], g='use', act=('dig', 'ring'), ages=GROWN, prefer=['happy'])
# ---------------- play
o.r('sand_angel', 'Pressing a sand angel by flopping flat on his back and flapping', 18, 'none',
    [k(.15, 'sand_b', perch=1, y=-.4, b=-.5, w=.6, eye='>'), k(.3, 'sand_b', perch=1, y=1.5, b=1.4, w=1, mark='floomp'), k(.5, 'sand_b', perch=1, y=1.5, b=1.4, w=0), k(.7, 'sand_b', perch=1, y=1.5, b=1.4, w=1), k(.9, y=.3, b=.2, eye='^')],
    [(.5, 'print')], g='play', act=('press', 'sand'), prefer=['happy', 'young'], obj=[(.3, dict(shake=0.15)), (.6, dict(shake=0.15))],
    say=["Angel. Look at the wingspan on that.", "Lie in it, get up, regret nothing."])
o.r('hop_a_trail', 'Hopping in three jumps from the right sand to the left to lay a trail', 20, 'none',
    [k(.12, 'board_r', perch=1, x=.4, y=.5, b=.5, l=1), k(.3, y=-.4, b=-.7, w=.5), k(.45, 'sand_b', perch=1, x=.5, y=.5, b=.6, r=1), k(.62, y=-.4, b=-.7, w=.5), k(.78, 'sand_a', perch=1, x=.5, y=.5, b=.6, l=1), k(.9, eye='^')],
    [(.45, 'print')], g='play', act=('hop', 'sand'), prefer=['happy'])
o.r('stomp_heap_flat', 'Hopping up and down on the heap until it is a pancake', 18, 'none',
    [k(.15, 'sand_c', perch=1, y=-.3, b=-.6, w=.5), k(.3, 'sand_c', perch=1, y=.4, b=1.1, l=1, mark='thud'), k(.45, 'sand_c', perch=1, y=-.4, b=-.9, w=1), k(.6, 'sand_c', perch=1, y=.4, b=1.3, r=1, mark='THUD'), k(.8, y=.2, b=.3, eye='^')],
    [(.6, 'level')], g='play', act=('hop', 'mound'), when=['mound>.3'], prefer=['grumpy'], obj=[(.3, dict(shake=0.15)), (.6, dict(shake=0.15))],
    say=["Flattened. It had it coming.", "Heap: gone. Me: taller."])
o.r('fling_sand_at_wall', 'Throwing billfuls of sand over his shoulder at the left wall', 18, 'none',
    [k(.15, x=.3, y=.4), k(.3, 'sand_a', x=1.1, y=1.4, b=.5, mark='hup'), k(.45, y=-.5, x=-.6, w=.5, eye='>'), k(.6, 'sand_a', x=1.1, y=1.4, b=.5, mark='hup'), k(.75, y=-.5, x=-.7, w=.8, eye='>'), k(.9, eye='-')],
    [(.3, 'fling')], g='play', act=('throw', 'sand'), prefer=['grumpy'], say=["Take that, wall. And that.", "Sand: airborne. Wall: unmoved. Draw."])
o.r('toss_and_catch', 'Tossing a billful of sand straight up and catching it again', 16, 'none',
    [k(.15, 'sand_b', x=1.4, y=1.4, b=.6), k(.3, x=-.6, y=-1.4, b=-.8, w=.6, eye='O'), k(.45, x=-.6, y=-1.6, b=-1, w=.3, l=1, eye='>'), k(.6, 'sand_b', x=1.4, y=1.4, b=.6, mark='gulp'), k(.8, x=-.3, y=-.3, eye='-')],
    [], g='play', act=('catch', 'sand'), prefer=['happy'],
    duo=[k(.15, 'sand_c', perch=1, x=.4), k(.4, 'sand_c', perch=1, x=-.4, y=-.8, b=-.5, w=.6, eye='o'), k(.62, 'sand_c', perch=1, x=1.4, y=1.4, b=.6, mark='gulp'), k(.85, 'sand_c', perch=1, eye='^')],
    say=["Threw sand at a friend, who caught it. Friendship, through grit.", "Missed theirs. Mine's the one that counts."])
o.r('leap_off_board', 'Climbing up on the base board and leaping off into the sand', 16, 'none',
    [k(.15, 'board_l', perch=1, x=.3, y=.2, b=.5), k(.3, 'board_l', perch=1, y=-.4, b=-.6, w=.5), k(.45, y=-.8, b=-1, w=1, eye='O'), k(.62, 'sand_a', perch=1, y=.6, b=1.2, l=1, mark='FOOMP'), k(.82, y=.2, b=.2, w=.5, eye='^')],
    [], g='play', act=('climb', 'board'), prefer=['young', 'happy'])
o.r('honk_into_bucket', 'Shouting into the bucket mouth like a megaphone', 14, 'wing',
    [k(.15, 'bucket_rim', reach=.6, x=.4, y=-.2, w=.2), k(.35, 'bucket_rim', reach=1, x=1.2, y=.5, w=.3, mark='HONK'), k(.55, 'bucket_rim', reach=1, x=1.2, y=.5, w=.5, mark='HONK', eye='O'), k(.75, x=-.4, y=-.5, eye='^')],
    [(.35, 'fun')], g='play', act=('shout', 'bucket'), shown='head', ages=GROWN, say=["Sounds like a bigger me.", "Bucket has better acoustics than the barn."])
# ---------------- test
o.r('taste_sand', 'Tasting a billful of sand and deciding against it', 14, 'none',
    [k(.15, 'sand_a', x=1.4, y=1.4, b=.6), k(.35, x=.4, y=.4, b=.2, eye='-', mark='...'), k(.55, x=-.8, y=-.6, b=-.4, w=.5, eye='>', mark='ptui'), k(.75, y=.8, b=.3, eye='-')],
    [], g='test', act=('taste', 'sand'), prefer=['curious', 'young'], say=["Tastes like the floor. Because it is the floor.", "Sand. Still sand. Zero stars."])
o.r('knock_left_wall', 'Knocking on both side walls with his bill and listening for hollow', 16, 'none',
    [k(.12, 'wall_l', x=1.2, y=.6, b=.3, mark='tok'), k(.3, 'wall_l', x=.8, y=-.3, b=-.3, l=1, mark='tok'), k(.55, x=-.6, y=-.6, w=.4, eye='-'), k(.75, 'wall_r', x=1.2, y=.6, b=.5, mark='tok'), k(.9, eye='^')],
    [], g='test', act=('knock', 'wall'))
o.r('tug_stuck_shovel', 'Tugging at the shovel by the grip, then the shaft, to see how deep it is stuck', 18, 'none',
    [k(.15, x=.4, y=-.2), k(.3, 'shovel_grip', x=.8, y=-.3, b=.4, mark='hnh'), k(.5, 'shovel_shaft', x=.9, y=-.3, b=.8, l=1, mark='HNNH'), k(.7, x=-.5, y=-.2, w=.6, eye='>'), k(.88, eye='-')],
    [], g='test', act=('tug', 'shovel'), ages=GROWN)
o.r('measure_the_ring', 'Pacing out the ring to measure it, from the left arc to the right, counting steps under his breath', 22, 'none',
    [k(.12, 'ring_l', x=.6, y=-.2, b=.2, l=1), k(.32, 'ring_near', x=.9, y=-.4, b=.3, r=1), k(.52, 'ring_r', x=.6, y=-.2, b=.2, l=1), k(.72, x=.2, y=-.1, eye='-', mark='nine'), k(.9, eye='^')],
    [], g='test', act=('measure', 'ring'), ages=GROWN, prefer=['curious'])
o.r('count_the_studs', 'Tapping each stud along the base board and counting to nine', 20, 'none',
    [k(.12, 'stud_1', x=1.4, y=.8, b=1, mark='1'), k(.3, 'stud_3', x=1.6, y=.6, b=.8, r=1, mark='3'), k(.5, 'stud_6', x=1.4, y=.8, b=1.2, l=1, mark='6'), k(.7, 'stud_9', x=1.6, y=.6, b=.8, r=1, mark='9'), k(.88, x=-.4, y=-.2, w=.4, eye='-', mark='nine')],
    [], g='test', act=('count', 'studs'), prefer=['curious'])
o.r('peer_down_the_pit', 'Leaning out over the edge of the pit and peering at the bottom', 18, 'none',
    [k(.15, x=.5, y=.3), k(.35, 'sand_c', x=1.1, y=1.5, b=.6, eye='O'), k(.55, 'sand_b', x=1.3, y=1.9, b=.7, mark='hmm'), k(.75, x=.3, y=.4, eye='-'), k(.9, eye='^')],
    [], g='test', act=('peer', 'pit'), when=['pit>.3'], prefer=['curious'])
o.r('sniff_wet_sand', 'Testing the sodden sand with a toe to see how deep the soaking goes', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'sand_c', x=1, y=1.3, b=.4, mark='snf'), k(.5, 'sand_c', x=1.2, y=1.4, b=.4, mark='snf snf'), k(.7, x=-.2, y=.3, eye='>', mark='ugh'), k(.88, eye='-')],
    [], g='test', act=('test', 'sand'), when=['obj_wetness>.3'], prefer=['curious'])
# ---------------- rest
o.r('nap_in_the_sand', 'Napping flat in the sand after wriggling a hollow for himself', 28, 'none',
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
o.r('sulk_at_the_far_wall', 'Sulking at the right wall with his back turned and refusing to explain', 24, 'none',
    [k(.15, x=-.5, y=.3, w=.4), k(.35, 'wall_r', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'wall_r', x=-.6, y=2.2, b=.9, w=.7, eye='-', mark='hmph'), k(.85, 'wall_r', x=-.4, y=2.4, b=.4, w=.4, eye='-')],
    [], g='rest', act=('sulk', 'wall'), when=['sad'], prefer=['grumpy'], say=["Not sulking. Facing the wall. Different.", "Sand did this to me."])
# ---------------- weather
o.r('tip_out_the_rain', 'Pouring the rainwater out of the bucket by tipping it over', 20, 'wing',
    [k(.15, 'bucket_rim', reach=.6, x=.3, y=-.2, w=.5), k(.35, 'bucket_rim', reach=1, x=.2, y=-.4, b=.4, w=1, mark='hng'), k(.55, 'bucket_rim', reach=1, x=.5, y=.3, b=.7, w=.9, mark='glug'), k(.75, x=-.4, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
    [(.55, 'tip')], g='weather', act=('pour', 'bucket'), when=['water>.3'], ages=GROWN, obj=[(.35, dict(sway=0.15)), (.55, dict(shake=0.15))])
o.r('squelch_the_soaked_sand', 'Splashing the soaked sand underfoot until it squelches up between his toes', 18, 'none',
    [k(.15, 'sand_a', perch=1, y=.3, x=.3), k(.3, 'sand_a', perch=1, y=.6, b=.6, l=1, mark='squelch'), k(.5, 'sand_b', perch=1, y=.6, b=.7, r=1, mark='squelch'), k(.7, 'sand_c', perch=1, y=.6, b=.7, l=1, eye='O', mark='squelch'), k(.9, eye='^')],
    [(.5, 'squelch')], g='weather', act=('splash', 'sand'), when=['obj_wetness>.5'], prefer=['happy'])
o.r('prop_the_slumping_heap', 'Pressing his wings against the heap so the rain cannot slump it', 22, 'wing',
    [k(.15, 'sand_deep', reach=.6, x=.3, y=.7), k(.35, 'sand_deep', reach=1, x=.6, y=.8, b=.4, w=1), k(.55, 'sand_a', reach=1, x=.7, y=.9, b=.5, w=1, eye='>'), k(.8, x=.1, eye='-', mark='ugh')],
    [(.55, 'tamp')], g='weather', act=('press', 'mound'), when=['wet', 'mound>.3'])
o.r('chip_the_crust', 'Chipping the sun-baked crust with his bill until it cracks', 20, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'sand_c', x=1, y=1.4, b=.4, mark='tak'), k(.45, x=.6, y=.5, w=.5), k(.6, 'sand_c', x=1, y=1.5, b=.5, mark='TAK'), k(.8, x=.1, eye='^')],
    [(.6, 'crack')], g='weather', act=('chip', 'sand'), when=['firm>.6'], prefer=['grumpy'])
o.r('scrape_frost_off_board', 'Scraping the frost off the base board with the edge of a wing', 18, 'wing',
    [k(.12, 'board_l', reach=.6, x=.2, y=.5), k(.3, 'board_m', reach=1, x=.9, y=1.2, b=.8), k(.5, 'board_m', reach=1, x=1.2, y=1.4, b=1, mark='skr'), k(.7, 'board_r', reach=1, x=.9, y=1.2, b=.8), k(.88, y=.6, eye='-')],
    [(.5, 'scrape')], g='weather', act=('scrape', 'board'), when=['cold', 'frost>.3'])
o.r('dust_bath_in_the_sand', 'Fluffing up in the bone-dry sand so the dust flies up through his feathers', 24, 'none',
    [k(.15, 'sand_c', perch=1, y=.6, b=.3), k(.3, 'sand_c', perch=1, x=1, y=.6, b=1.2, w=1, mark='fff'), k(.5, 'sand_c', perch=1, x=-1, y=.6, b=1.4, w=0, l=1), k(.7, 'sand_c', perch=1, x=1, y=.6, b=1.2, w=1, r=1, mark='fff'), k(.9, y=.2, w=.4, eye='^')],
    [(.5, 'dustbath')], g='weather', act=('fluff', 'sand'), when=['dry', 'warm', 'obj_wetness<.3'], prefer=['happy'], say=["Clean now. Dirtier. Same thing.", "Dust bath. Filthy, correct, dignified."])
# ---------------- show
o.r('king_of_the_heap', 'Showing himself king of the heap, standing on it with his wings spread', 22, 'none',
    [k(.15, 'sand_deep', y=.3, b=.5), k(.3, 'sand_c', perch=1, y=-.5, b=-.4, w=.6), k(.5, 'sand_c', perch=1, y=-.9, b=-.2, w=1, eye='^', mark='BOW'), k(.75, 'sand_c', perch=1, y=-.9, b=-.2, w=1), k(.9, y=0, eye='o')],
    [], g='show', act=('show', 'mound'), when=['mound>.3'], prefer=['happy'], say=["King of this exact pile. Bow or leave.", "Long live me. Short pile."])
o.r('sign_the_sand', 'Writing CHEESE along the front sand with the tip of his bill to show who owns it', 22, 'none',
    [k(.12, 'sand_a', x=1.4, y=1.5, b=.6), k(.3, 'sand_deep', x=1.2, y=1.2, b=.3, l=1), k(.5, 'sand_c', x=1.4, y=1.5, b=.7, r=1), k(.7, x=.3, y=-.4, w=.5, eye='^'), k(.88, x=.1, y=.3, eye='o')],
    [(.5, 'print')], g='show', act=('show', 'sand'), prefer=['curious'], say=["Cheese was here. Cheese is always here.", "Signed it. Let the wind try to forge it."])
o.r('drum_the_bucket', 'Drumming at the bucket rim with both wings, a fast tattoo', 18, 'wing',
    [k(.15, 'bucket_rim', reach=.6, x=.3), k(.3, 'bucket_rim', reach=1, w=.8, mark='rrrr'), k(.42, 'bucket_side', reach=.6, w=.2, mark='rrrr'), k(.56, 'bucket_base', reach=.4, w=.5, mark='dunk'), k(.7, 'bucket_rim', reach=1, w=.9, mark='TSH'), k(.85, y=1, b=.5, w=1, eye='^')],
    [], g='show', act=('drum', 'bucket'), ages=GROWN, say=["Thank you. Tip the bucket.", "Encore? No. I have standards."])
o.r('tap_dance_the_board', 'Tap-dancing the length of the base board with a click at every stud', 20, 'none',
    [k(.12, 'board_l', perch=1, y=-.3, b=-.3, w=.7, l=1, mark='tk'), k(.32, 'board_m', perch=1, y=-.3, b=-.3, w=.9, r=1, mark='tk'), k(.52, 'board_m', perch=1, y=-.4, b=-.5, w=1, l=1, mark='tk tk'), k(.72, 'board_r', perch=1, y=-.3, b=-.3, w=.9, r=1, mark='tk'), k(.9, y=.4, b=.5, w=0, eye='^')],
    [(.52, 'fun')], g='show', act=('dance', 'board'), prefer=['young', 'happy'])
o.r('argue_with_the_shovel', 'Jabbing a wing at the shovel grip and arguing whose sandbox this is', 22, 'wing',
    [k(.15, x=-.4, y=-.8, w=.3), k(.35, 'shovel_grip', reach=.8, x=1.4, y=-1, b=-.6, w=.5, mark='MINE'), k(.55, 'shovel_grip', reach=1, x=1.8, y=-1, b=-.8, eye='>', mark='no, MINE'), k(.75, x=-.8, y=-.2, eye='-'), k(.9, eye='^')],
    [], g='show', act=('argue', 'shovel'), ages=GROWN, prefer=['grumpy'])
# ---------------- mishap
o.r('head_wedged_in_bucket', 'Getting stuck headfirst in the bucket mouth at the shoulders and kicking out', 22, 'none',
    [k(.15, x=.5, eye='>'), k(.3, 'bucket_rim', x=1.2, y=.6, b=.8, mark='oof'), k(.5, 'bucket_rim', x=1.3, y=.6, b=1, l=1, eye='O', mark='mmf'), k(.7, 'bucket_rim', x=1.3, y=.6, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
    [(.7, 'dent')], g='mishap', act=('stuck', 'bucket'), shown='head', ages=GROWN, prefer=['young', 'grumpy'], obj=[(.5, dict(shake=0.15)), (.7, dict(shake=0.15))],
    say=["Wedged by the shoulders. Bucket won.", "I meant to do that. All of it."])
o.r('trip_on_the_board', 'Tripping over the base board, slipping, and eating a billful of sand', 16, 'none',
    [k(.15, 'board_l', x=.5, y=.3, l=1), k(.3, x=1.1, y=.8, b=-.4, w=.8, eye='O'), k(.5, 'sand_a', x=1.6, y=1.8, b=1, w=1, mark='FFF'), k(.75, y=.6, b=.4, eye='@'), k(.9, eye='-')],
    [(.5, 'scatter')], g='mishap', act=('slip', 'board'), say=["Face. Sand. Dignity: buried.", "The board moved. It is always the board."])
o.r('bonk_the_shovel_shaft', 'Knocking his head on the shovel shaft by marching at it head down', 16, 'none',
    [k(.15, x=.4, y=.4), k(.3, x=1, y=.3, b=.3, w=.3, mark='hup'), k(.45, 'shovel_shaft', x=1.2, y=.2, b=.4, eye='O', mark='BONK'), k(.65, x=-1, y=-.3, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('knock', 'shovel'), ages=GROWN, say=["Saw the shaft coming. Chose violence anyway.", "Shaft: unharmed. Skull: negotiating."])
o.r('climb_out_of_the_pit', 'Sinking to the knees in the pit and climbing out, heaving himself over the edge', 20, 'none',
    [k(.15, 'sand_b', perch=1, x=.4, y=.4), k(.3, 'sand_b', perch=1, x=.2, y=.2, b=1.1, l=1, eye='O'), k(.5, 'sand_b', perch=1, x=.2, y=.3, b=1.6, r=1, w=.6, mark='hnnng'), k(.7, 'sand_b', perch=1, x=.3, y=-.3, b=-.5, w=1, mark='POP'), k(.88, y=.8, eye='-')],
    [(.5, 'slump')], g='mishap', act=('climb', 'pit'), when=['pit>.3'], prefer=['young'])
o.r('cave_in_the_heap', 'Digging at the foot of the heap until the whole top comes down on his head', 20, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'sand_a', x=1, y=1.2, b=.7, l=1, mark='dig'), k(.5, 'sand_a', x=1.2, y=1.5, b=.9, r=1, eye='O'), k(.65, 'sand_a', y=2, b=1.4, w=1, mark='FWUMP', eye='@'), k(.88, y=1.2, b=1, eye='-', mark='...')],
    [(.65, 'cave')], g='mishap', act=('dig', 'mound'), when=['mound>.3'], prefer=['curious'], obj=[(.5, dict(shake=0.15)), (.65, dict(shake=0.15))], say=["I dug. It fell. Physics is a snitch.", "Buried by my own heap. Good work, me."])
o.r('blow_sand_back_in_his_face', 'Blowing a billful of sand off the board against the wind and wearing it', 16, 'none',
    [k(.15, 'board_m', x=1, y=1.2, b=.4), k(.3, x=-.3, y=-.3, w=.4), k(.45, x=1, y=.6, mark='fff'), k(.6, 'board_m', y=1.2, b=.6, w=.8, eye='@', mark='pfft'), k(.8, x=-.3, y=.4, eye='-')],
    [(.6, 'scatter')], g='mishap', act=('blow', 'sand'), when=['windy'], say=["Blew it away. It came back. Rude.", "Wind: one. Eyes: nil."])
o.emit()

# Drawing (70 x 43 cells, 9.3 px a row, standing line row 40): roof rows 7-21 (180 px+) with the CHEESE sign at row 19 (196 px), eave rows 22-23
# (158-168 px), left panel cols 10-23 (three planks, bolts at cols 11 16 21 on rows 24 31 38, a knot at cols 15-17 on rows 25 and 33),
# door frame cols 25-45 with nested frames inside, sill row 38 (19 px), threshold row 40 (0 px), right panel cols 48-59 (bolts col 51, a knot at
# cols 54-56), the water bowl cols 56-63 rows 40-41 (0 px). Nothing here moves: only the whole house can sway or shake.
o = Obj('dog_house', 'placed',
        parts=dict(plank='the plank panels either side of the door, three planks wide', bolt='the bolts along the bottom rail and in the panels', plate='the (=) wall plates on the panels, flat metal plates',
                   frame='the nested door frame', door='the dark doorway', sill='the sill along the foot of the doorway', threshold='the threshold slab in front of the doorway',
                   bowl='the water bowl by the right of the door', sign='the CHEESE sign across the roof', roof='the shingled roof and its eave'),
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
                     plate_l=(0.232, 0.786), plate_r=(0.797, 0.786), frame_l=(0.362, 0.833), frame_l2=(0.362, 0.714), frame_r=(0.652, 0.833), frame_r2=(0.652, 0.714),
                     door_dark=(0.522, 0.810), sill_a=(0.420, 0.905, 'surface'), sill_b=(0.580, 0.905, 'surface'), threshold_l=(0.464, 0.952), threshold_r=(0.609, 0.952),
                     bowl_l=(0.841, 0.952, 'surface'), bowl_r=(0.899, 0.952, 'surface')),
        marks=[('water', .3, '~~~', 'bowl_l', 'water'), ('frost', .3, '*.*.*', 'sill_a', 'frost'), ('warmth', .5, '~ ~ ~', 'plank_r', 'glow')])
# ---------------- care
o.r('scrub_planks', 'Scrubbing the left planks with a wing until the mud comes off', 18, 'wing',
    [k(.12, 'plank_l', reach=.6, x=.3, y=.4), k(.3, 'plank_l', reach=1, x=.5, y=.6, l=1), k(.5, 'plank_l', reach=1, x=.6, y=.8, b=.3, r=1, mark='skrk'), k(.7, 'plank_l', reach=1, x=.5, y=.5, l=1), k(.88, eye='^')],
    [(.5, 'scrub')], g='care', act=('scrub', 'planks'), when=['obj_dirt>.3'], prefer=['grown'])
o.r('sweep_sill', 'Sweeping the sill clean with the flat of a wing', 16, 'wing',
    [k(.12, 'sill_a', reach=.6, x=.3, y=.5), k(.3, 'sill_a', reach=1, x=.5, y=.7, l=1), k(.55, 'sill_b', reach=1, x=.6, y=.7, r=1), k(.75, 'sill_b', reach=.7, x=.3, y=.4), k(.9, eye='-')],
    [(.55, 'sweep')], g='care', act=('sweep', 'sill'), when=['obj_dirt>.3'])
o.r('scour_bowl_rim', 'Scrubbing the bowl rim with his bill until it shines', 16, 'none',
    [k(.12, 'bowl_l', x=.5, y=.8, b=.3), k(.3, 'bowl_l', x=1.2, y=1.6, b=.7, mark='skrr'), k(.55, 'bowl_r', x=1.2, y=1.6, b=.7, mark='skrr'), k(.75, x=.5, y=.8, eye='-'), k(.9, eye='^')],
    [(.55, 'scour')], g='care', act=('scrub', 'bowl'), when=['obj_dirt>.3'])
o.r('mop_frame_dry', 'Mopping both sides of the door frame dry with his breast and a lot of grunting', 20, 'none',
    [k(.12, 'frame_l', x=.4, y=.4), k(.3, 'frame_l', x=1.9, y=.5, b=.4, mark='hff'), k(.5, 'frame_l', x=2, y=.4, b=.6), k(.7, 'frame_r', x=1.9, y=.5, b=.4, mark='hff'), k(.88, x=.1, eye='^')],
    [(.5, 'dry')], g='care', act=('dry', 'frame'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=0.15)), (.7, dict(shake=0.15))])
o.r('hammer_loose_bolt', 'Mending a loose bolt by hammering it back down with his bill', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'bolt_l2', x=1.6, y=2, b=1, l=1, mark='tak'), k(.45, x=.2, y=.4), k(.6, 'bolt_l2', x=1.6, y=2.2, b=1.2, r=1, mark='TAK'), k(.8, x=.1, eye='^')],
    [(.6, 'bolt')], g='care', act=('mend', 'bolt'), when=['obj_condition<.6'])
# ---------------- use
o.r('guard_the_bowl', 'Taking up guard at the bowl with his wings out, daring the garden to come closer', 22, 'none',
    [k(.15, y=.3, b=.2), k(.35, 'bowl_r', perch=1, x=.6, y=.6, w=1, eye='>'), k(.6, 'bowl_r', perch=1, x=1.2, y=1.2, b=1, w=1, eye='>', mark='hsss'), k(.85, 'bowl_r', perch=1, x=.6, y=.6, w=1, eye='>')],
    [], g='use', act=('guard', 'bowl'), prefer=['grumpy'], say=["Come closer. Go on. I am three bowls tall.", "The bowl is mine. The garden can fetch its own."])
o.r('knock_then_answer', 'Knocking at the door frame, then turning round and answering it politely', 20, 'none',
    [k(.12, 'frame_l', x=.9, y=.4, mark='knock'), k(.3, 'frame_l', x=.9, y=.5, mark='knock'), k(.5, x=-.7, y=-.5, w=.5, eye='O', mark='Hello?'), k(.7, x=.4, y=.2, b=.3, w=0, eye='^', mark='Coming!'), k(.88, eye='-')],
    [], g='use', act=('knock', 'frame'),
    duo=[k(.15, 'door_dark', x=.4), k(.45, 'door_dark', x=.8, y=-.2, mark='Who is it?'), k(.65, 'door_dark', x=.6, y=-.4, b=.3, eye='^', mark='Coming!'), k(.85, eye='^')],
    say=["Knocked. Answered. Still not home.", "Rude of me to answer. I'd have let it ring."])
o.r('peer_into_the_dark', 'Poking just his head through the dark doorway to peer round both ways', 20, 'none',
    [k(.15, x=.4, y=.2), k(.3, 'door_dark', x=1.4, y=.3, b=.3, eye='O'), k(.5, 'door_dark', x=1.5, y=.4, b=.4, eye='>', mark='hm'), k(.7, 'door_dark', x=1.5, y=.3, b=.4, eye='-'), k(.88, x=.2, eye='-')],
    [], g='use', act=('peer', 'doorway'), shown='head', prefer=['curious'])
o.r('holler_at_the_door', 'Cupping a wing at the door frame and shouting that dinner is ready', 18, 'wing',
    [k(.15, 'frame_r', reach=.5, x=.2, y=-.3), k(.35, 'frame_r', reach=1, x=.6, y=-.8, b=-.2, mark='DINNER'), k(.55, 'frame_r', reach=1, x=.7, y=-.9, b=-.3, eye='O', mark='DINNER!'), k(.75, x=-.2, y=.2, eye='-', mark='...')],
    [], g='use', act=('shout', 'frame'), prefer=['lonely'], say=["Dinner's ready. There is no dinner. Come anyway.", "Shouted dinner. The garden stayed home."])
o.r('splash_the_bowl', 'Dunking his bill and splashing the bowl water all over the doorstep', 16, 'none',
    [k(.15, 'bowl_l', x=.7, y=.9, b=.3), k(.3, 'bowl_l', x=1.2, y=1.6, b=.5, mark='glub'), k(.5, 'bowl_l', x=1.2, y=1.6, b=.6, w=.8, mark='SPLOSH'), k(.75, x=-.4, y=.2, w=.5, eye='O'), k(.9, eye='^')],
    [(.5, 'slosh')], g='use', act=('splash', 'bowl'), when=['water>.2'], prefer=['happy'], say=["More on the doorstep than in the bowl. Fine.", "Wet now. Chose it."])
o.r('scrape_feet_clean', 'Scraping his feet clean along the threshold, one then the other, before not going in', 18, 'none',
    [k(.12, 'threshold_l', x=.3, y=.4, l=1), k(.3, 'threshold_l', x=.3, y=.5, b=.3, r=1, mark='skrt'), k(.5, 'threshold_r', x=.3, y=.4, b=.2, l=1, mark='skrt'), k(.7, 'threshold_r', x=.4, y=.5, b=.3, r=1), k(.88, eye='^')],
    [(.5, 'wipe')], g='use', act=('scrape', 'feet'), prefer=['curious'])
# ---------------- play
o.r('hop_up_and_off_the_sill', 'Hopping up on the sill and off again like a step stool', 16, 'none',
    [k(.15, 'sill_a', perch=1, y=-.3, b=-.6, w=.5), k(.3, 'sill_a', perch=1, y=.3, b=.8, l=1), k(.45, y=-.6, b=-.9, w=1), k(.62, 'sill_b', perch=1, y=.3, b=.8, r=1), k(.8, y=-.4, b=-.8, w=.8, eye='^')],
    [], g='play', act=('hop', 'sill'), prefer=['young', 'happy'])
o.r('race_the_bolts', 'A race along the front of the house, tapping every low bolt with his bill', 18, 'none',
    [k(.12, 'bolt_l1', x=.6, y=1.2, b=.5, mark='tk'), k(.3, 'bolt_l2', x=1.7, y=1.3, b=.4, l=1, mark='tk'), k(.48, 'bolt_l3', x=1.8, y=1.2, b=.5, r=1, mark='tk'), k(.68, 'bolt_r', x=1.9, y=1.3, b=.4, l=1, mark='tk'), k(.88, x=.2, w=.7, eye='^')],
    [(.68, 'fun')], g='play', act=('race', 'bolts'), prefer=['young', 'happy'])
o.r('flatten_at_the_frame', 'Hide and seek at the door frame, flattening himself against it and bursting out at nothing', 18, 'none',
    [k(.15, 'frame_r', x=-.3, y=.3, b=.4), k(.35, 'frame_r', x=-.4, y=.6, b=.7, eye='-'), k(.55, 'frame_r', x=-.4, y=.6, b=.7, eye='-', mark='...'), k(.7, x=1.2, y=-.4, b=-1.6, l=1, eye='O', mark='BOO'), k(.88, y=.3, eye='^')],
    [], g='play', act=('hide', 'frame'), prefer=['young'], say=["Boo. Nothing. Good.", "Got it. Whatever it was."])
o.r('spy_at_the_knot', 'Pulling at the edge of the left plate with his bill to see if it comes off', 16, 'none',
    [k(.15, x=.4, y=-.2), k(.3, 'plate_l', x=1, y=-.4, b=.2, eye='-'), k(.5, 'plate_l', x=1.2, y=-.4, b=.3, eye='O', mark='hmm'), k(.7, 'plate_l', x=1.2, y=-.4, b=.3, eye='>'), k(.88, x=.2, eye='-')],
    [], g='play', act=('pull', 'plate'), ages=GROWN, prefer=['curious'])
o.r('dig_beside_the_threshold', 'Digging furiously at the ground beside the threshold with both feet, burying nothing', 18, 'none',
    [k(.12, 'threshold_l', x=.4, y=.8, b=.5), k(.3, 'threshold_l', x=.5, y=1.2, b=1, l=1, mark='dig'), k(.5, 'threshold_l', x=.5, y=1.4, b=1.2, r=1, mark='dig dig'), k(.7, 'threshold_l', x=.4, y=1.4, b=1.3, l=1), k(.88, y=.2, w=.4, eye='^')],
    [(.5, 'muddy')], g='play', act=('dig', 'ground'), prefer=['happy'], say=["Hole. Empty. Plan: fully on track.", "Dog taught me this. Dog is not credited."])
o.r('chase_his_tail', 'Chasing his own tail in tight circles, snapping at it', 16, 'none',
    [k(.15, 'threshold_r', x=.5, y=.3, b=.4, l=1), k(.3, 'threshold_r', x=-.7, y=.6, b=.7, r=1), k(.5, 'threshold_r', x=.7, y=.4, b=.8, l=1, eye='@'), k(.7, 'threshold_r', x=-.7, y=.6, b=.7, r=1), k(.88, x=.1, eye='o')],
    [], g='play', act=('chase', 'tail'), prefer=['young', 'happy'])
o.r('roll_over_and_play_dead', 'Trying to hide on the threshold by flopping onto his back and playing dead', 20, 'none',
    [k(.12, 'threshold_l', x=.4, y=.5, b=.6), k(.3, 'threshold_r', x=.8, y=1.2, b=1.2, l=1, r=1), k(.5, 'threshold_l', y=1.5, b=1.4, eye='-', mark='*thud*'), k(.7, 'threshold_l', y=1.5, b=1.4, eye='-', mark='...'), k(.88, y=.4, b=.4, eye='^')],
    [], g='play', act=('hide', 'threshold'), prefer=['happy'], say=["Dead. Convincing. Applaud.", "Rolled over. Dog house approves."])
# ---------------- test
o.r('tap_for_hollow', 'Tapping the left planks with his bill to hear which one is hollow', 16, 'none',
    [k(.12, 'plank_l', x=1.2, y=.6, b=.3, mark='tok'), k(.3, 'plank_l', x=.7, y=-.2, b=-.2, l=1, mark='tok'), k(.55, x=-.5, y=-.5, w=.4, eye='-'), k(.75, 'plank_l', x=1.2, y=.6, b=.5, mark='tonk'), k(.9, eye='^')],
    [], g='test', act=('tap', 'planks'))
o.r('count_the_bolts', 'Tapping each low bolt along the bottom rail and counting under his breath', 20, 'none',
    [k(.1, 'bolt_l1', x=.8, y=1.4, b=.6, mark='1'), k(.28, 'bolt_l2', x=1, y=1.2, b=.3, l=1, mark='2'), k(.46, 'bolt_l3', x=.6, y=1, b=.8, r=1, mark='3'), k(.66, 'plate_l', x=1.1, y=1.4, b=.4, l=1, mark='4'), k(.86, x=-.4, y=-.2, w=.4, eye='-', mark='four')],
    [], g='test', act=('count', 'bolts'), prefer=['curious'])
o.r('put_a_shoulder_to_it', 'Pressing his shoulder to the door frame to see whether the whole house tips', 18, 'none',
    [k(.12, x=.2, y=.3), k(.3, 'frame_l', x=.8, y=.5, b=.5, mark='hnnh'), k(.5, 'frame_r', x=.9, y=.6, b=.8, l=1, mark='HNNNH'), k(.7, x=-.5, y=-.3, w=.7, eye='-'), k(.88, eye='^')],
    [], g='test', act=('press', 'frame'), ages=GROWN)
o.r('sniff_the_right_planks', 'Tasting the right planks to find out what has been leaning there', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'plank_r', x=1, y=1, b=.4, mark='snf'), k(.5, 'plank_r', x=1.2, y=.8, b=.5, mark='snf snf'), k(.7, x=-.2, y=.3, eye='>', mark='ugh'), k(.88, eye='-')],
    [], g='test', act=('taste', 'planks'), prefer=['curious'])
o.r('measure_the_rain_in_the_bowl', 'Plumbing the bowl with a wing to measure how much rain it caught', 16, 'wing',
    [k(.15, 'bowl_l', reach=.6, x=.3, y=.5), k(.35, 'bowl_l', reach=1, x=.5, y=1, b=.4, mark='plip'), k(.55, x=.1, y=.2, w=.6, eye='-', mark='two wings'), k(.75, x=-.2, y=-.2, eye='^')],
    [], g='test', act=('measure', 'bowl'), when=['water>.2'])
o.r('ring_the_bowl', 'Ringing the bowl by tapping its rim from side to side to hear what note it is', 16, 'none',
    [k(.12, 'bowl_l', x=1, y=1.4, b=.3, mark='ting'), k(.3, 'bowl_r', x=1, y=1.4, b=.3, mark='tong'), k(.5, x=-.3, y=-.2, eye='-', mark='B flat'), k(.7, 'bowl_l', x=1, y=1.4, b=.5, mark='dink'), k(.88, eye='^')],
    [], g='test', act=('ring', 'bowl'))
o.r('stand_by_the_frame', 'Hopping to touch the door frame as high as he can reach, a mark higher each time', 18, 'none',
    [k(.15, 'door_dark', x=.8, y=.8, b=.3), k(.35, 'frame_l', x=.1, y=-1.6, b=-1.5, w=.4, eye='O'), k(.6, 'frame_l', x=.1, y=-1.8, b=-1.7, w=.6, eye='>'), k(.8, x=-1.2, y=1.4, b=1.4, w=0, eye='-', mark='ugh')],
    [], g='test', act=('hop', 'frame'))
o.r('crane_at_the_sign', "Singing the sign's letters up at it, one note each, from the doorstep", 18, 'wing',
    [k(.15, y=-.8, x=-.2), k(.3, y=-1.2, x=-.4, reach=.8, b=-.3, eye='O'), k(.5, y=-1.5, x=-.4, reach=1, b=-.5, mark='C H E E'), k(.7, y=-1.5, x=-.5, reach=1, b=-.5, eye='>', mark='S E'), k(.88, y=-.2, eye='^')],
    [], g='test', act=('sing', 'sign'), far=True, say=["Six letters. All mine.", "CHEESE. I checked. It is a good name."])
# ---------------- rest
o.r('lean_on_warm_planks', 'Leaning his belly against sun-warmed planks with his eyes shut', 24, 'none',
    [k(.15, y=.2, x=.3), k(.35, 'plank_r', x=.8, y=.4, b=.3, eye='-'), k(.6, 'plank_r', x=1, y=.7, b=.7, eye='-', mark='ahh'), k(.85, 'plank_r', x=1, y=.7, b=.7, eye='-')],
    [(.6, 'warm')], g='rest', act=('lean', 'planks'), when=['sun', 'warmth>.3'], prefer=['tired'])
o.r('sit_on_the_sill_at_dusk', 'Sitting on the sill with his chin up, watching the light go out of the garden', 26, 'none',
    [k(.15, 'sill_b', perch=1, y=.3, b=.2), k(.4, 'sill_b', perch=1, y=-.8, b=.9, eye='-'), k(.7, 'sill_b', perch=1, y=-1.4, x=-.6, b=1.4, eye='-', mark='...'), k(.9, 'sill_b', perch=1, y=.1, b=.3, eye='o')],
    [], g='rest', act=('sit', 'sill'), when=['dusk'], prefer=['happy'], say=["Light goes. I stay. Efficient.", "Best seat on the lot, and it is a step."])
o.r('sulk_at_the_frame', 'Sulking at the door frame with his back turned, refusing to explain', 24, 'none',
    [k(.15, x=-.5, y=.3, w=.4), k(.35, 'frame_l2', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'frame_l2', x=-1, y=1.4, b=.9, l=1, eye='-', mark='hmph'), k(.85, 'frame_l2', x=-1, y=1.6, b=1.1, eye='-')],
    [], g='rest', act=('sulk', 'frame'), when=['sad'], prefer=['grumpy'], say=["Not sulking. Facing the other way. Different.", "The house did this. I am saying nothing."])
o.r('wait_at_the_threshold', 'Keeping guard at the threshold with his bill pointed down the path, ready for anyone', 26, 'none',
    [k(.15, y=.2, x=.2), k(.4, 'threshold_l', x=.5, y=-.2, b=.3, eye='>'), k(.65, 'threshold_l', x=.7, y=-.3, b=.3, eye='>', mark='...'), k(.85, 'threshold_l', x=.4, y=.3, b=.5, eye='-', mark='sigh')],
    [], g='rest', act=('guard', 'threshold'), when=['lonely'])
# ---------------- weather
o.r('bail_out_the_rain', 'Scooping the rainwater out of the bowl with quick flicks of a wing', 20, 'wing',
    [k(.15, 'bowl_l', reach=.6, x=.3, y=.6), k(.35, 'bowl_l', reach=1, x=.6, y=1, b=.4, w=.5, mark='flick'), k(.55, 'bowl_l', reach=1, x=.6, y=1, b=.5, mark='flick'), k(.75, x=-.3, y=.2, eye='-', mark='ugh'), k(.9, eye='^')],
    [(.55, 'bail')], g='weather', act=('scoop', 'bowl'), when=['water>.3'], prefer=['grown'])
o.r('crack_the_bowl_ice', 'Chipping the iced-over bowl with his bill until the top cracks', 18, 'none',
    [k(.15, x=.4, y=.4), k(.3, 'bowl_r', x=1, y=1.3, b=.4, mark='tak'), k(.5, x=.4, y=.4, w=.4), k(.65, 'bowl_r', x=1.1, y=1.5, b=.6, mark='CRACK'), k(.85, x=.1, eye='^')],
    [(.65, 'scrape')], g='weather', act=('chip', 'bowl'), when=['cold', 'frost>.4', 'water>.2'], prefer=['grumpy'])
o.r('scrape_the_frost', 'Scraping the frost off the left planks with the edge of a wing', 18, 'wing',
    [k(.12, 'plank_l', reach=.6, x=.2, y=.5), k(.3, 'plank_l', reach=1, x=.3, y=.7, b=.3), k(.5, 'plank_l', reach=1, x=.3, y=.7, b=.4, mark='skr'), k(.7, 'plank_r', reach=1, x=.3, y=.6, b=.3), k(.88, eye='-')],
    [(.5, 'scrape')], g='weather', act=('scrape', 'planks'), when=['cold', 'frost>.3'])
o.r('cool_his_feet', 'Standing in the bowl with the sun on his back to cool his feet', 24, 'none',
    [k(.15, y=.2, b=.1), k(.35, 'bowl_l', perch=1, y=.5, b=.4, l=1, eye='-'), k(.6, 'bowl_l', perch=1, y=.6, b=.6, r=1, eye='-', mark='aah'), k(.85, 'bowl_l', perch=1, y=.4, b=.4, eye='^')],
    [(.6, 'cool')], g='weather', act=('cool', 'bowl'), when=['sun', 'warm', 'water>.3'], prefer=['happy'])
o.r('shelter_from_the_rain', 'Taking shelter against the right planks, hugging them close while the rain comes down', 28, 'none',
    [k(.15, y=.2, x=.2), k(.35, 'bolt_r', x=-.4, y=.9, b=.7, w=.6), k(.6, 'bolt_r', x=-1.2, y=1.6, b=1.6, w=.8, eye='-', mark='brr'), k(.85, 'bolt_r', x=-1.2, y=1.6, b=1.6, w=.8, eye='-')],
    [], g='weather', act=('shelter', 'planks'), when=['wet', 'obj_wetness<.6'], say=["Dry-ish. The eave tries. I respect it.", "Rain, again. As if I asked."])
o.r('brace_the_frame_in_a_gale', 'Gripping the door frame with both feet braced while the wind comes through', 22, 'none',
    [k(.15, y=.3, x=.3), k(.35, 'frame_r2', x=.8, y=.6, b=.6, w=.7, l=1), k(.6, 'frame_r2', x=1, y=.8, b=.9, w=1, eye='>', mark='hnng'), k(.85, 'frame_r2', x=.6, y=.6, b=.5, w=.5, r=1)],
    [], g='weather', act=('brace', 'frame'), when=['windy'])
# ---------------- show
o.r('bellow_at_the_sign', 'Shouting up at the sign that this is, in fact, his house', 18, 'none',
    [k(.15, y=-.6, x=-.3), k(.35, y=-1.6, x=-1.2, b=-1.5, w=.5, eye='O', mark='MY HOUSE'), k(.55, y=-1.8, x=-1.2, b=-1.8, w=1, eye='>', mark='MINE'), k(.75, y=-.4, x=-.2, w=.4, eye='^')],
    [], g='show', act=('shout', 'sign'), far=True, say=["Says CHEESE. Spelled it myself.", "Sign agrees. Sign is on my side."])
o.r('pose_at_the_frame', 'Showing off against the door frame like the cover of a magazine about kennels', 22, 'none',
    [k(.15, y=.2, x=.2), k(.35, 'frame_l2', x=.2, y=-.4, b=-.3, w=.5, eye='-'), k(.55, 'frame_r2', x=.3, y=-.6, b=-.3, w=.7, eye='^'), k(.8, 'frame_r2', x=.3, y=-.7, b=-.3, w=.9, eye='^', mark='click')],
    [], g='show', act=('show', 'frame'), prefer=['happy'], say=["Kennels Monthly. Cover price: nothing.", "Hold still. They are always watching."])
o.r('give_the_house_tour', 'Showing a friend round the house: the bolts, the dark doorway, the planks and the bowl', 28, 'none',
    [k(.1, 'bolt_l2', x=.6, y=.8, w=.5, mark='bolts'), k(.3, 'door_dark', x=.7, y=-.2, w=.8, mark='door'), k(.5, 'plank_r', x=.8, y=.4, w=1, mark='planks'), k(.7, 'bowl_r', perch=1, x=.6, y=.5, w=.9, mark='bowl'), k(.9, y=1, b=.5, w=1, eye='^')],
    [], g='show', act=('show', 'house'), say=["Home. Bolts, a bowl and zero staff.", "Tour ends here. Tipping is encouraged."])
o.r('argue_with_the_knot', 'Arguing with the right plate, jabbing a wing at it and telling it to stop staring', 20, 'wing',
    [k(.15, y=.1, x=.2), k(.35, 'plate_r', reach=.8, x=.8, y=-.3, b=-.1, eye='>', mark='what'), k(.55, 'plate_r', reach=1, x=1, y=-.4, b=-.2, eye='O', mark='WHAT'), k(.75, x=-.3, y=.1, eye='-', mark='creepy')],
    [], g='show', act=('argue', 'plate'), ages=GROWN, prefer=['grumpy'])
o.r('tightrope_the_sill', "Balancing along the bowl's rim like a tightrope with his wings out and his chin up", 20, 'none',
    [k(.12, 'bowl_l', perch=1, y=-.2, b=.2, w=.7, l=1), k(.32, 'bowl_l', perch=1, y=-.4, b=-.1, w=1, r=1), k(.55, 'bowl_r', perch=1, y=-.4, b=-.2, w=1, l=1, eye='O'), k(.78, 'bowl_r', perch=1, y=-.2, b=.1, w=.8, r=1), k(.9, y=.3, w=0, eye='^')],
    [], g='show', act=('balance', 'bowl'), prefer=['young', 'happy'])
# ---------------- mishap
o.r('slip_on_the_wet_sill', 'Slipping on the wet sill and skidding along it to end up flat on the doorstep', 16, 'none',
    [k(.15, 'sill_a', perch=1, x=.4, y=.2, b=.3, l=1), k(.3, 'sill_a', perch=1, x=.8, y=-.3, b=-.5, w=1, eye='O'), k(.5, 'threshold_l', x=1.2, y=1.4, b=1.3, w=1, mark='FWAP'), k(.75, y=.8, b=.6, eye='@'), k(.9, eye='-')],
    [(.5, 'muddy')], g='mishap', act=('slip', 'sill'), when=['obj_wetness>.4'], say=["Floor won. Floor always wins.", "Meant to lie down. Meant to do it dramatically."])
o.r('jammed_in_the_doorway', 'Getting stuck in the doorway after charging it too wide, jamming at the shoulders', 22, 'none',
    [k(.15, x=.5, eye='>'), k(.3, 'frame_l', x=1.2, y=.5, b=.7, mark='oof'), k(.5, 'door_dark', x=1.4, y=.5, b=1, l=1, eye='O', mark='mmf'), k(.7, 'door_dark', x=1.4, y=.5, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
    [(.7, 'dent')], g='mishap', act=('stuck', 'doorway'), ages=GROWN, prefer=['young', 'grumpy'], obj=[(.5, dict(shake=0.15)), (.7, dict(shake=0.15))],
    say=["Too wide. Entirely the doorway's fault.", "Popped out. Dignity stayed inside."])
o.r('tail_snagged_on_a_bolt', 'Backing away and hooking his tail feathers on a bolt', 18, 'none',
    [k(.15, x=-.2, y=.2), k(.35, 'bolt_l3', x=-.9, y=.6, b=.4, l=1, mark='tug'), k(.55, 'bolt_l3', x=-1.2, y=.7, b=.8, w=.6, eye='O', mark='RRIP'), k(.75, x=.6, y=.8, b=.5, eye='@'), k(.9, eye='-')],
    [], g='mishap', act=('hook', 'bolt'), say=["Lost a feather. It is a bolt now.", "Backing up: not my event."])
o.r('walked_into_the_frame', 'Knocking his head on the frame by strolling out with his eyes fixed on the sign', 16, 'none',
    [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'door_dark', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'frame_r', x=1.3, y=.3, b=.5, eye='O', mark='BONK'), k(.65, x=-1, y=-.2, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('knock', 'head'), say=["Looking at the sign. Not looking at the frame. Learned.", "Wood: hard. Beak: also hard. Draw."])
o.r('stub_a_toe_on_the_bowl', 'Kicking the bowl rim with his toe and hopping about while the water sloshes', 16, 'none',
    [k(.15, y=.1, x=.2), k(.3, 'bowl_r', x=.4, y=.4, b=.4, l=1, mark='tk'), k(.48, 'bowl_r', x=.2, y=.2, b=1, l=1, eye='O', mark='OW'), k(.68, x=-.2, y=-.4, b=-.7, l=1, w=.8, eye='@'), k(.88, eye='-')],
    [(.48, 'slosh')], g='mishap', act=('kick', 'bowl'), when=['water>.2'], say=["The bowl moved. Never trust a bowl.", "Toe: one. Bowl: two. Bowl is winning."])
o.r('shake_off_like_a_dog', 'Shaking himself off like a dog and spraying the planks', 16, 'none',
    [k(.15, 'plank_l', x=.2, y=.2, b=.3), k(.3, 'plank_l', x=.3, y=.3, b=.8, w=1, mark='brrrr'), k(.45, 'plank_l', x=.3, y=.3, b=.8, w=0, l=1), k(.6, 'plank_l', x=.3, y=.3, b=.8, w=1, r=1, mark='BRRR'), k(.82, y=.2, w=.3, eye='^')],
    [(.45, 'soak')], g='mishap', act=('shake', 'feathers'), when=['wet'], prefer=['happy'])
o.r('fit_the_doorway_side_on', 'Turning side-on at the doorway to find out if two ducks would fit', 18, 'none',
    [k(.15, 'door_dark', x=.2, y=.2), k(.35, 'frame_r', x=.6, y=.3, b=.2, w=.5), k(.55, 'frame_l', x=.9, y=.4, b=.4, w=.9, eye='-'), k(.75, 'door_dark', x=.3, y=-.2, w=0, eye='^', mark='two')],
    [], g='use', act=('fit', 'doorway'), say=["Two ducks. Tight. Cosy. Fine.", "Fits. I would be the one at the front."])
o.emit()

# Drawing (66 x 39 cells, 4.9 px a row, tyre bottoms 15 px up): cab rows 7-18 with two panes (top 151 px, pane bottoms 107 px), body box rows 18-29
# with a trim line at row 23 (73 px) and a short bar at row 20 (87 px), two lamps at row 26 (58 px), tyres cols 11-27 and 40-55 rows 28-35 with hubs at
# row 31 (34 px) and tread bands at rows 27 and 35, the body's lower edge row 29 (44 px). Nothing here moves: only the whole car can sway or shake.
o = Obj('toy_car', 'placed',
        parts=dict(tail='the tail end of the body', front='the front end of the body', lamp='the lamp at each end of the body', wall='the tyre walls', hub='the hub cap in the middle of each tyre',
                   tread='the tread bands round each tyre', sill='the lower edge of the body between the tyres', trim='the trim line along the side panel', panel='the side panel with its door handle bar',
                   glass='the two panes of the cab', arch='the arch of body above each tyre'),
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
                     panel_h=(0.585, 0.526), glass_a=(0.446, 0.421), glass_b=(0.600, 0.421), glass_c=(0.385, 0.342)),
        marks=[('lit', .3, '*.*', 'lamp_l', 'glow'), ('frost', .3, '*.*.*', 'glass_a', 'frost'), ('warmth', .5, '~ ~ ~', 'panel_h', 'glow')])
# ---------------- care
o.r('polish_the_side', 'Polishing the side panel in slow circles with a wing', 18, 'wing',
    [k(.12, 'panel_h', reach=.6, x=.3, y=.3), k(.3, 'panel_h', reach=1, x=1.1, y=-.4, l=1), k(.5, 'trim_b', reach=1, x=1.1, y=.8, b=.6, r=1, mark='squk'), k(.7, 'panel_h', reach=1, x=1.1, y=-.4, l=1), k(.88, eye='^')],
    [(.5, 'polish')], g='care', act=('polish', 'panel'), when=['obj_dirt>.3'], prefer=['grown'], obj=[(.5, dict(glow=.5))])
o.r('pick_mud_out_of_the_tread', 'Scraping dried mud out of the bottom tread, one chunk at a time', 20, 'none',
    [k(.12, 'tread_lb', x=.6, y=1.2, b=.6), k(.3, 'tread_lb', x=1.1, y=1.7, b=.8, mark='pk'), k(.5, 'tread_rb', x=1.1, y=1.6, b=.7, l=1, mark='pk'), k(.7, 'tread_rb', x=1.2, y=1.8, b=.9, mark='pk'), k(.88, x=.2, y=.2, eye='^')],
    [(.5, 'mud')], g='care', act=('scrape', 'tread'), when=['obj_dirt>.3'], prefer=['curious'])
o.r('wipe_the_lamps_clear', 'Giving each lamp a wipe with the underside of a wing until it shows clear', 16, 'wing',
    [k(.12, 'lamp_l', reach=.6, x=.3, y=.3), k(.3, 'lamp_l', reach=1, x=.4, y=.2, w=.3, l=1), k(.55, 'lamp_r', reach=1, x=.4, y=.2, r=1, mark='squk'), k(.75, 'lamp_r', reach=.6, x=.2, y=.1), k(.9, eye='^')],
    [(.55, 'wipe')], g='care', act=('wipe', 'lamp'), when=['obj_dirt>.3'])
o.r('hold_the_rocking_still', 'Bracing a wing at each end of the car until the rocking stops', 22, 'wing',
    [k(.12, 'tail_low', reach=.6, x=.4, y=.3, b=.3), k(.3, 'tail_low', reach=1, x=.6, y=.5, b=.7, mark='hnh'), k(.55, 'front_low', reach=1, x=.6, y=.5, b=.7, l=1), k(.78, 'front_low', reach=.6, x=.2, y=.2), k(.9, eye='-')],
    [(.55, 'steady')], g='care', act=('brace', 'car'), when=['rock>.3'], obj=[(.3, dict(sway=.5)), (.55, dict(sway=.1))])
# ---------------- use
o.r('shove_from_the_tail', 'Putting his breast to the tail and shoving the car forward', 18, 'none',
    [k(.12, 'tail_low', x=.4, y=.4, b=.3), k(.3, 'tail_low', x=1, y=.5, b=.8, l=1, mark='hup'), k(.5, 'tail_low', x=1.3, y=.4, b=1.2, r=1, mark='HNNH'), k(.72, x=-.3, y=-.2, w=.5, eye='O'), k(.88, eye='^')],
    [(.5, 'shove')], g='use', act=('shove', 'tail'), ages=GROWN, obj=[(.3, dict(sway=.4)), (.5, dict(sway=1)), (.7, dict(sway=.4))], say=["It moved. I shall be known as a mover.", "Pushed it. Left it. Maximum effort."])
o.r('haul_back_by_the_lamp', 'Pulling the front end back by its lamp frame with his bill', 18, 'none',
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
o.r('bounce_off_the_tyre', 'Hopping at the left tyre wall and bouncing off it like a trampoline', 16, 'none',
    [k(.12, 'wall_l', x=.6, y=.3, b=.4), k(.3, 'wall_l', x=1.1, y=.5, b=1.3, l=1, mark='boing'), k(.5, y=-.9, b=-1.2, w=1, eye='O'), k(.68, 'wall_l', x=1.1, y=.5, b=1.4, r=1, mark='BOING'), k(.86, y=.2, b=.3, eye='^')],
    [(.68, 'honk')], g='play', act=('hop', 'tyre'), prefer=['young', 'happy'], obj=[(.3, dict(sway=.3)), (.68, dict(sway=.5))])
o.r('drum_the_trim_line', 'Drumming along the trim line from one end to the other like a xylophone', 20, 'wing',
    [k(.12, 'trim_a', reach=.7, w=.4, mark='tik'), k(.3, 'trim_a', reach=1, w=.8, mark='tak'), k(.5, 'trim_b', reach=1, w=.8, mark='tik'), k(.7, 'trim_c', reach=1, w=.9, mark='TSH'), k(.88, y=.8, b=.4, w=1, eye='^')],
    [], g='play', act=('drum', 'trim'), ages=GROWN, say=["Car percussion. Four notes, one of them rust.", "I would tour this. The car says no."])
o.r('race_between_the_hubs', 'A race from the left hub to the right, slapping each with a wing', 16, 'none',
    [k(.12, 'hub_l', x=.5, y=.9, b=.5, l=1, mark='slap'), k(.3, y=-.3, b=-.5, w=.9), k(.5, 'hub_r', x=.6, y=.9, b=.6, r=1, mark='SLAP'), k(.7, y=-.3, b=-.5, w=.9), k(.88, 'hub_l', x=.5, y=.9, b=.5, l=1)],
    [], g='play', act=('race', 'hubs'), prefer=['young', 'happy'])
o.r('peek_round_each_tyre', 'Playing seek round each tyre, peeking round the left then the right for an invisible rival', 20, 'none',
    [k(.12, 'wall_l', x=-.3, y=.5, b=.4, eye='>'), k(.3, 'wall_l', x=.9, y=-.3, b=.2, eye='O'), k(.5, y=.3, b=-.4, w=.4), k(.68, 'wall_r', x=-.3, y=.5, b=.4, eye='>'), k(.85, 'wall_r', x=.9, y=-.3, b=.2, eye='O')],
    [], g='play', act=('seek', 'tyres'), prefer=['young'])
o.r('rev_then_boot_the_tail', 'Revving at the left lamp with engine noises, then kicking the tail to launch it', 22, 'none',
    [k(.12, 'lamp_l', x=.8, y=.2, b=.3, mark='brrm'), k(.3, 'lamp_l', x=1, y=.4, b=.6, w=.5, mark='BRRRM'), k(.5, x=-.8, y=-.3, b=-.5, w=1, eye='>'), k(.68, 'tail_low', x=.4, y=.5, b=.8, l=1, mark='KICK'), k(.88, y=.2, eye='^')],
    [(.68, 'shove')], g='play', act=('kick', 'tail'), ages=GROWN, obj=[(.68, dict(sway=.9)), (.85, dict(sway=.2))], say=["Brrm. Kick. Go. Nothing. Brrm again.", "Launched it. In my head it is in Spain."])
o.r('donut_round_the_tyre', 'A race in circles round the right tyre with a wing out for the corners', 18, 'none',
    [k(.12, 'wall_r', x=.6, y=.3, w=.5, l=1), k(.3, 'wall_r', x=.2, y=.5, b=.6, w=1, r=1, mark='eeEEE'), k(.5, 'wall_r', x=.4, y=.6, b=.8, w=1, l=1), k(.7, 'wall_r', x=.2, y=.5, b=.6, w=1, r=1, mark='eeEEE'), k(.88, y=.3, b=.3, eye='@')],
    [], g='play', act=('race', 'tyre'), prefer=['happy'])
o.r('nudge_the_tail_like_a_cue', 'Nudging the tail along with the tip of his bill like a billiards cue', 22, 'none',
    [k(.12, x=.2, y=.2, b=.3, eye='-'), k(.3, 'tail_up', x=-.4, y=.4, b=.4), k(.45, 'tail_up', x=.9, y=.5, b=.5, mark='tk'), k(.6, 'tail_up', x=-.4, y=.4, b=.4), k(.75, 'tail_up', x=1, y=.5, b=.5, mark='tk')],
    [], g='play', act=('nudge', 'tail'), ages=GROWN, obj=[(.45, dict(sway=.3)), (.75, dict(sway=.3))],
    duo=[k(.15, 'front_up', x=.2), k(.4, 'front_up', x=-.4, y=.4, b=.4), k(.55, 'front_up', x=.9, y=.5, b=.5, mark='tk'), k(.8, 'front_up', x=-.4, y=.4, b=.4), k(.9, eye='^')],
    say=["Tapped it down to them like a snooker pro. They tapped it back. Amateurs.", "Two ducks, one car, no cue. Billiards, sort of."])
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
o.r('sniff_the_tread', 'Tasting the lower tread to work out what it has been driven through', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'tread_lb', x=1.6, y=2, b=1.2, mark='snf'), k(.5, 'tread_lb', x=1.8, y=2.2, b=1.6, mark='snf snf'), k(.7, x=-1.4, y=-.4, eye='>', mark='ugh'), k(.88, eye='-')],
    [], g='test', act=('taste', 'tread'), prefer=['curious'])
o.r('tap_the_cabin_glass', 'Tapping the cabin glass to find out whether anyone is driving', 16, 'none',
    [k(.12, 'glass_a', x=.8, y=-.3), k(.3, 'glass_a', x=2.1, y=-.2, b=.2, mark='tok'), k(.5, 'glass_b', x=2.1, y=-.2, b=.2, mark='tok tok'), k(.7, x=-1.3, y=-.5, w=.4, eye='-', mark='nobody'), k(.88, eye='^')],
    [], g='test', act=('tap', 'glass'), ages=GROWN, say=["Knocked. Nothing. The car drives itself. Concerning.", "No answer. Fine. Rude."])
o.r('lean_on_the_sill_for_weight', 'Hanging his full weight at the sill to see if the springs give', 16, 'none',
    [k(.15, 'sill_b', x=.5, y=.5, b=.3), k(.35, 'sill_b', x=.9, y=.8, b=.9, mark='creak'), k(.55, 'sill_b', x=1, y=.9, b=1.4, eye='O'), k(.8, x=-.2, y=-.2, eye='-', mark='hm')],
    [], g='test', act=('weigh', 'sill'), obj=[(.35, dict(sway=.3)), (.55, dict(sway=.6))], prefer=['curious'])
o.r('count_the_tyre_rings', 'Counting the rings of the left tyre from the outside in', 20, 'none',
    [k(.1, 'wall_l', x=.4, y=.8, b=.3, mark='1'), k(.3, 'tread_lt', x=.7, y=1, b=.5, mark='2'), k(.5, 'hub_l', x=.5, y=1.2, b=.7, mark='3'), k(.7, 'wall_l', x=-.2, y=.3, eye='-', mark='four?'), k(.88, eye='^')],
    [], g='test', act=('count', 'rings'))
o.r('listen_for_an_engine', 'Pressing an ear to the side panel and listening for an engine', 18, 'none',
    [k(.12, x=.2, y=-.3), k(.3, 'panel_h', x=.5, y=-.3, b=.3, eye='-'), k(.55, 'panel_h', x=.7, y=-.2, b=.5, eye='-', mark='...'), k(.78, x=-.3, y=-.5, w=.5, eye='O', mark='nothing')],
    [], g='test', act=('listen', 'car'), ages=GROWN)
o.r('hug_the_tyre_to_measure', 'Wrapping both wings round the left tyre to see whether his wingspan reaches', 18, 'none',
    [k(.12, 'wall_l', x=.4, y=.4, w=.3), k(.3, 'wall_l', x=.6, y=.6, b=.5, w=1, mark='hnf'), k(.55, 'wall_l', x=.7, y=.7, b=.8, w=1, eye='>'), k(.78, x=-.2, y=-.2, w=0, eye='-', mark='not quite')],
    [], g='test', act=('wrap', 'tyre'))
# ---------------- rest
o.r('nap_against_the_tyre', 'Napping against the right tyre with his bill tucked under a wing', 28, 'none',
    [k(.15, y=.3, x=.3), k(.35, 'wall_r', x=.9, y=.9, b=.6, eye='-'), k(.6, 'hub_r', x=1.5, y=1.8, b=1.6, eye='-', mark='z'), k(.85, 'hub_r', x=1.6, y=2.2, b=2, eye='-', mark='zZ')],
    [(.6, 'toast')], g='rest', act=('nap', 'tyre'), when=['tired'])
o.r('warm_up_at_the_panel', 'Soaking up the sun with his cheek flat against the warm side panel', 26, 'none',
    [k(.15, y=.3, x=.3), k(.35, 'panel_h', x=.6, y=.4, b=.3, eye='-'), k(.6, 'panel_h', x=.8, y=.7, b=.7, w=.3, eye='-', mark='ahh'), k(.85, 'panel_h', x=.8, y=.7, b=.7, eye='-')],
    [(.6, 'warm')], g='rest', act=('warm', 'panel'), when=['sun', 'warmth>.3'], prefer=['happy'])
o.r('tell_the_lamp_his_day', 'Sitting nose to nose with the left lamp, telling it about his day', 28, 'none',
    [k(.15, y=.2, x=.2), k(.35, 'lamp_l', x=.6, y=.4, b=.6, eye='-'), k(.6, 'lamp_l', x=.7, y=.5, b=.9, eye='-', mark='...and then'), k(.85, 'lamp_l', x=.5, y=.4, b=.8, eye='^', mark='anyway')],
    [], g='rest', act=('sit', 'lamp'), when=['lonely'], say=["It listens. It is a lamp. Zero interruptions.", "Told it everything. It lit up. Supportive."])
o.r('sulk_at_the_tail', 'Sulking at the tail with his back to the car, muttering', 24, 'none',
    [k(.15, x=-.5, y=.3, w=.4), k(.35, 'tail_low', x=-.6, y=.9, b=.5, eye='>'), k(.6, 'tail_low', x=-1.6, y=.4, b=1.6, r=1, eye='-', mark='hmph'), k(.85, 'tail_low', x=-1.8, y=.2, b=1.8, eye='-')],
    [], g='rest', act=('sulk', 'tail'), when=['sad'], prefer=['grumpy'], say=["Do not look at the car. It knows what it did.", "Fine. Be a car. See if I care."])
# ---------------- weather
o.r('wipe_the_frost_off_the_glass', 'Giving the cabin glass a wipe, corner to corner, to clear the frost', 20, 'wing',
    [k(.12, 'glass_a', reach=.7, x=.2, y=-.3), k(.3, 'glass_a', reach=1, x=.4, y=-.2, l=1), k(.5, 'glass_b', reach=1, x=.4, y=-.2, r=1, mark='skr'), k(.68, 'glass_c', reach=1, x=.4, y=-.3, l=1), k(.88, eye='-')],
    [(.5, 'chipfrost')], g='weather', act=('wipe', 'glass'), ages=GROWN, when=['cold', 'frost>.3'])
o.r('chip_frost_from_the_tread', 'Chipping frost out of the upper tread with the tip of his bill', 18, 'none',
    [k(.12, x=.4, y=.5), k(.3, 'tread_lt', x=1, y=1, b=.4, mark='tk'), k(.5, 'tread_lt', x=1.1, y=1.1, b=.5, mark='tak'), k(.7, 'tread_rb', x=1.1, y=1.3, b=.6, l=1, mark='tk'), k(.88, eye='^')],
    [(.5, 'chipfrost')], g='weather', act=('chip', 'tread'), when=['cold', 'frost>.3'], prefer=['grumpy'])
o.r('cup_the_lamp_in_the_wind', 'Bracing a wing round the left lamp to keep it alight against the wind', 22, 'wing',
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
o.r('preen_in_the_dark_glass', 'Grooming his chest feathers at the cabin glass as if it were a mirror', 20, 'none',
    [k(.15, 'glass_c', x=.4, y=-.2, b=.2, eye='O'), k(.35, 'glass_c', x=.5, y=-.3, w=.5, eye='^', mark='hello'), k(.55, 'glass_c', x=.4, y=-.2, w=.8, l=1, eye='^'), k(.78, 'glass_c', x=.5, y=-.3, w=.4, eye='>', mark='lookin good')],
    [], g='show', act=('groom', 'glass'), ages=GROWN, prefer=['happy'], say=["Handsome devil in there. Same as ever.", "Reflection agrees with me. Always does."])
o.r('whip_the_wing_off_the_hub', 'Opening a wing off the hub cap like a magician revealing the trick', 18, 'wing',
    [k(.12, 'hub_r', reach=.5, w=.5, y=.5), k(.3, 'hub_r', reach=1, w=1, x=.5, y=.8, b=.4), k(.5, y=-.4, b=-.4, reach=1, w=1, eye='^', mark='TA-DA'), k(.7, 'hub_r', reach=.6, x=.2, y=.6), k(.88, y=.6, b=.4, eye='^')],
    [], g='show', act=('open', 'hub'), prefer=['happy'], say=["Behold: a hub. It was there the whole time.", "Gasp, please. Gasp. There it is."])
o.r('flash_a_turn_signal', 'Showing a left-turn signal by sweeping a wing twice past the right lamp, then going straight', 20, 'wing',
    [k(.12, 'lamp_r', reach=.6, x=.3, y=.2), k(.3, 'lamp_r', reach=1, x=.4, y=.3, w=.5, mark='tik'), k(.5, 'lamp_r', reach=1, x=.4, y=.3, w=.5, mark='tik'), k(.7, y=.1, x=-.5, w=.6, eye='>', mark='left'), k(.88, x=.4, eye='-', mark='straight')],
    [], g='show', act=('show', 'lamp'), obj=[(.3, dict(glow=.7)), (.5, dict(glow=.7))], say=["Indicated left. Went straight. Cars do it daily.", "Signal given. Not a single reaction. Perfect."])
o.r('wave_the_car_in', 'Showing the car in with both wings like a parking attendant', 22, 'none',
    [k(.12, 'tail_up', x=.3, y=.2, w=.5), k(.3, 'tail_up', x=.4, y=-.2, b=-.2, w=1, mark='this way'), k(.5, 'front_up', x=.4, y=-.3, b=-.3, w=.4, l=1, mark='keep coming'), k(.72, 'front_up', x=.5, y=-.2, b=-.2, w=1, eye='O', mark='STOP'), k(.88, y=.2, w=0, eye='^')],
    [], g='show', act=('show', 'car'), ages=GROWN, say=["Perfectly parked. Carless. Still counts.", "Parking attendant. Zero pay. Full authority."])
o.r('quote_a_price_at_the_hub', 'Showing the gap above the tyre with a sucked-in bill, like a mechanic about to quote a price', 22, 'none',
    [k(.12, 'sill_a', x=.5, y=.3, b=.3), k(.3, 'sill_a', x=.9, y=.6, b=.5, eye='-', mark='hmmmm'), k(.52, 'sill_a', x=.3, y=.2, b=.2, w=.5, eye='O', mark='ooh'), k(.72, y=-.4, x=-.2, w=.7, eye='^', mark='four hundred'), k(.88, eye='-')],
    [], g='show', act=('show', 'arch'), say=["Four hundred. Cash. Plus a bread.", "Worrying noise. I will not say which. Four hundred."])
o.r('take_a_bow_in_the_glow', 'Taking a bow beside the lit right lamp as if it were a stage light', 22, 'none',
    [k(.12, 'lamp_r', x=.2, y=.2, w=.5), k(.35, 'lamp_r', x=.2, y=-.3, w=1, eye='^', mark='thank you'), k(.6, 'lamp_r', x=.8, y=1.2, b=1, w=1), k(.85, 'lamp_r', x=.1, y=-.2, w=.5, eye='^')],
    [], g='show', act=('bow', 'lamp'), when=['lit>.5'], obj=[(.35, dict(glow=.8))])
# ---------------- mishap
o.r('slip_beside_the_tyre', 'Slipping on wet ground beside the tyre and sliding bill first at it', 16, 'none',
    [k(.15, x=.4, y=.2, b=.3, l=1), k(.3, x=.9, y=-.3, b=-.6, w=1, eye='O'), k(.5, 'wall_l', x=1.5, y=1.4, b=1, w=1, mark='FWAP'), k(.75, y=.8, b=.6, eye='@'), k(.9, eye='-')],
    [(.5, 'muddy')], g='mishap', act=('slip', 'tyre'), when=['obj_wetness>.4'], say=["Wet floor. Car side impact. Both fine.", "Slid. Stopped. Tyre did not move."])
o.r('lunge_at_his_reflection', 'Chasing his reflection across the cabin glass to settle who is better looking', 18, 'none',
    [k(.12, y=-.2, x=.2), k(.3, 'glass_a', x=.9, y=-.2, b=.3, eye='>', mark='you'), k(.48, 'glass_a', x=1.5, y=.2, b=.9, eye='O', mark='BONK'), k(.7, x=-1, y=-.3, b=-.3, w=1, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('chase', 'reflection'), ages=GROWN, say=["Reflection won. By a head. Mine.", "Bonk. Same duck. Same pain."])
o.r('boot_the_tyre_too_hard', 'Kicking the lower right tread harder than planned and hopping about on one foot', 16, 'none',
    [k(.12, y=.1, x=.2), k(.3, 'tread_rb', x=-.8, y=.2, b=.2, r=1, mark='tk'), k(.48, 'tread_rb', x=-1.4, y=.2, b=.6, r=1, eye='O', mark='OW'), k(.68, x=.8, y=1.4, b=-1.4, r=1, w=1, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('kick', 'tyre'), say=["Tyre: soft. Tyre: not soft. Foot: sorry.", "I kicked a tyre. I am a man now. A duck."])
o.r('walk_into_the_panel', 'Wandering along with his eyes fixed up at the cabin and walking straight at the side panel', 16, 'none',
    [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'sill_a', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'panel_h', x=2.2, y=.8, b=.8, l=1, eye='O', mark='BONK'), k(.65, x=-2, y=1, b=1.6, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('walk_into', 'panel'), ages=GROWN, say=["The car was there the whole time. Rude.", "I looked up. Mistake. Panel was waiting."])
o.r('snag_a_feather_on_the_lamp', 'Hooking a wing feather on the lamp frame while backing off', 18, 'none',
    [k(.15, x=-.2, y=.2), k(.35, 'lamp_r', x=-1.4, y=.3, b=.4, r=1, mark='tug'), k(.55, 'front_low', x=-2, y=.3, b=1.6, w=1, eye='O', mark='RRIP'), k(.75, x=1, y=1.4, b=.5, eye='@'), k(.9, eye='-')],
    [], g='mishap', act=('hook', 'lamp'), say=["Lost a feather. The lamp has a trophy.", "It grabbed me. I will remember the lamp."])
o.r('caught_by_the_rebound', 'Leaning in to look at the rocking car and catching the rebound square in his chest', 18, 'none',
    [k(.15, x=.3, y=.3), k(.3, 'panel_h', x=.7, y=.5, b=.3, eye='O'), k(.5, 'sill_a', x=-1.2, y=-.4, b=-.7, w=1, eye='@', mark='OOF'), k(.7, y=1.2, b=1, eye='@'), k(.88, y=.4, b=.4, eye='-')],
    [], g='mishap', act=('catch', 'car'), when=['rock>.3'], obj=[(.3, dict(sway=-.6)), (.5, dict(sway=.9)), (.7, dict(sway=-.2))], say=["It swung back. Of course it swung back.", "Got me. Fair. I started the rocking."])
o.emit()

# Drawing (106 x 54 cells, 8.5 px a row, standing line row 50): finial row 4 (390 px), roof rows 7-26, eave rows 27-28 (about 200 px), two posts of
# three-wide columns at cols 17-20 and 82-85 (rows 29-47), outer lines at cols 10 and 95, a lattice panel on each side (cols 11-32 and 74-95, rows 40-48:
# top rail 85 px, base rail 17 px) with diamonds and a flower cluster at row 45 (43 px), a potted plant at each foot (tubs row 50, foliage row 49).
# The open middle is the floor at the standing line. Nothing here moves: only the whole gazebo can sway.
o = Obj('gazebo', 'placed',
        parts=dict(floor='the open floor at the standing line', pot='the clay pot at the foot of each side', plant='the foliage growing out of each pot (a potted plant, not a plinth)',
                   rail='the lattice rails, a low base rail and a top rail on each side', lattice='the diamond lattice panels either side', flower='the flower clusters worked into the lattice',
                   post='the post at each side', roof='the pagoda roof and its eave', finial='the finial on top'),
        fields=dict(leaves=(0, 0, 1), frost=(0, 0, 1), warmth=(0, 0, 1)),
        physics=[('leaves', 'rate', .0006, 'windy'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                 ('warmth', 'rate', .0004, 'sun'), ('warmth', 'rate', -.0006, 'cold'), ('warmth', 'rate', -.0002, 'night')],
        effects=dict(
            sweepleaf=[('leaves', 'set', 0)], scrub=[('obj.dirt', 'add', -.25)], dry=[('obj.wetness', 'add', -.3)], polish=[('obj.dirt', 'add', -.15)],
            soil=[('obj.dirt', 'add', -.1)], scatter=[('leaves', 'mul', .4)], chip=[('frost', 'mul', .2)], warmfeet=[('warmth', 'add', -.2), ('need.energy', 'add', 2)],
            smear=[('obj.dirt', 'add', .1)], scratch=[('need.cleanliness', 'add', 1)], dent=[('obj.condition', 'add', -.1)], crowd=[('need.social', 'add', 2)],
            hush=[('need.energy', 'add', 1)]),
        anchors=dict(floor_l=(0.362, 0.943, 'inside surface'), floor_c=(0.505, 0.943, 'inside surface'), floor_r=(0.667, 0.943, 'inside surface'),
                     pot_l=(0.181, 0.943), pot_r=(0.819, 0.943), plant_l=(0.133, 0.925), plant_r=(0.848, 0.925),
                     rail_lo_l=(0.152, 0.906, 'surface'), rail_lo_m=(0.267, 0.906, 'surface'), rail_lo_r=(0.762, 0.906, 'surface'),
                     lattice_l=(0.248, 0.830), lattice_l2=(0.286, 0.811), lattice_r=(0.781, 0.830), flower_l=(0.143, 0.849), flower_r=(0.819, 0.849),
                     rail_up_l=(0.229, 0.755), rail_up_r=(0.762, 0.755), post_l=(0.171, 0.698), post_r=(0.800, 0.698)),
        marks=[('leaves', .3, ',;,.;', 'floor_c', 'leaf'), ('frost', .3, '*.*.*', 'rail_up_l', 'frost'), ('warmth', .5, '~ ~ ~', 'floor_l', 'glow')])
# ---------------- care
o.r('sweep_the_leaves', 'Sweeping the floorboards clear of leaves with sideways wing strokes', 20, 'wing',
    [k(.12, 'floor_l', reach=.6, x=.3, y=.5), k(.3, 'floor_l', reach=1, x=.5, y=.7, l=1), k(.5, 'floor_c', reach=1, x=.6, y=.7, r=1, mark='shff'), k(.7, 'floor_r', reach=1, x=.5, y=.7, l=1), k(.88, eye='^')],
    [(.5, 'sweepleaf')], g='care', act=('sweep', 'floor'), when=['leaves>.3'], prefer=['grown'])
o.r('scrub_the_lattice', 'Scrubbing the left lattice with a wing, one diamond at a time', 22, 'wing',
    [k(.12, 'lattice_l', reach=.6, x=.3, y=.3), k(.3, 'lattice_l', reach=1, x=.4, y=.4, l=1, mark='skrk'), k(.5, 'lattice_l2', reach=1, x=.5, y=.4, r=1, mark='skrk'), k(.7, 'lattice_l', reach=1, x=.4, y=.5, l=1), k(.88, eye='^')],
    [(.5, 'scrub')], g='care', act=('scrub', 'lattice'), when=['obj_dirt>.3'])
o.r('mop_the_wet_rail', 'Drying the wet side rails by mopping them with his breast and a lot of grunting', 22, 'none',
    [k(.12, 'rail_up_l', x=.3, y=-.3), k(.3, 'rail_up_l', x=.7, y=-.2, b=.3, mark='hff'), k(.5, 'rail_up_l', x=.9, y=-.1, b=.5), k(.7, 'rail_up_r', x=.7, y=-.2, b=.3, mark='hff'), k(.88, x=.1, eye='^')],
    [(.5, 'dry')], g='care', act=('dry', 'rail'), ages=GROWN, when=['obj_wetness>.3'])
o.r('wipe_the_post_clean', 'Polishing the right post with a wing, as high as he can reach', 18, 'wing',
    [k(.12, 'post_r', reach=.6, x=.4, y=-.3), k(.3, 'post_r', reach=1, x=1.5, y=-.5, b=-.2, mark='skrk'), k(.5, 'post_r', reach=1, x=1.6, y=-.7, b=-.3, l=1), k(.7, 'post_r', reach=1, x=1.5, y=-.5, b=-.2, r=1, mark='skrk'), k(.88, eye='^')],
    [(.5, 'polish')], g='care', act=('polish', 'post'), ages=GROWN, when=['obj_dirt>.3'])
o.r('wipe_the_pot_rims', 'Giving both pot rims a wipe with the underside of a wing to clear the soil', 18, 'wing',
    [k(.12, 'pot_l', reach=.6, x=.3, y=.8, b=.3), k(.3, 'pot_l', reach=1, x=.5, y=1, b=.6, w=.3), k(.55, 'pot_r', reach=1, x=.5, y=1, b=.6, w=.3, mark='sff'), k(.75, 'pot_r', reach=.6, x=.2, y=.5), k(.9, eye='^')],
    [(.55, 'soil')], g='care', act=('wipe', 'pot'), when=['obj_dirt>.3'])
# ---------------- use
o.r('rest_his_wings_on_the_rail', 'Leaning both wings along the right side rail, surveying the garden like a landlord', 24, 'none',
    [k(.15, y=.1, x=.3), k(.35, 'rail_up_r', x=.5, y=-.3, b=.2, w=.6, eye='-'), k(.6, 'rail_up_r', x=.8, y=-.4, b=.3, w=.8, eye='>', mark='hm'), k(.85, 'rail_up_r', x=.7, y=-.4, b=.3, w=.8, eye='>')],
    [], g='use', act=('lean', 'rail'), ages=GROWN)
o.r('hold_the_entry_open', 'Holding the entry open with a wing for guests who are not coming', 22, 'wing',
    [k(.15, y=.1, x=.2), k(.35, 'floor_c', perch=1, reach=.8, y=-.2, b=-.1, mark='after you'), k(.6, 'floor_c', perch=1, reach=1, y=.4, b=.3, x=.4, eye='^', mark='madam'), k(.85, 'floor_c', perch=1, reach=.5, y=.1, eye='-', mark='...')],
    [], g='use', act=('open', 'entry'), prefer=['lonely'],
    duo=[k(.15, 'floor_l', perch=1, x=.2), k(.4, 'floor_l', perch=1, x=.5, y=-.2, b=.2, mark='after you'), k(.65, 'floor_c', perch=1, x=.4, y=.2, b=.3, eye='^', mark='no, you'), k(.88, 'floor_c', perch=1, eye='-')],
    say=["Held the door. No guests. Principle.", "After you. After you. Fine, me first."])
o.r('scratch_his_back_on_the_post', 'Grooming his back by scratching it up and down the left post with a happy groan', 20, 'none',
    [k(.15, 'post_l', x=-.5, y=.4, b=.4), k(.35, 'post_l', x=-1, y=1, b=1.2, eye='-', mark='ahh'), k(.55, 'post_l', x=-1, y=-1.2, b=-1.2, eye='-', mark='ooh'), k(.75, 'post_l', x=-1, y=1, b=1.2, eye='-'), k(.9, y=0, eye='^')],
    [(.55, 'scratch')], g='use', act=('groom', 'post'), ages=GROWN)
o.r('rap_the_rail_to_order', 'Tapping the side rails with a wing to call the whole garden to order', 20, 'wing',
    [k(.12, 'rail_up_l', reach=.7, x=.2, y=-.2), k(.3, 'rail_up_l', reach=1, x=.3, y=-.3, w=.5, mark='tok tok'), k(.5, 'rail_up_r', reach=1, x=.3, y=-.3, w=.5, mark='TOK TOK'), k(.72, y=-.5, x=-.3, w=1, eye='O', mark='ORDER'), k(.9, eye='-')],
    [(.5, 'crowd')], g='use', act=('tap', 'rail'), ages=GROWN)
# ---------------- play
o.r('spin_round_the_post', 'Dancing round the right post with one wing hooked round it, a pole-dance of sorts', 18, 'none',
    [k(.12, 'post_r', x=.4, y=.2, w=.4), k(.3, 'post_r', x=.5, y=.3, w=.8, l=1), k(.5, 'post_r', x=-.5, y=.4, b=.4, w=1, r=1, eye='@'), k(.7, 'post_r', x=.6, y=.5, b=.5, w=1, l=1), k(.9, y=.6, b=.8, eye='@', mark='...')],
    [], g='play', act=('dance', 'post'), ages=GROWN, prefer=['young', 'happy'], obj=[(.5, dict(sway=.1)), (.7, dict(sway=-.1))])
o.r('count_to_ten_at_the_post', 'Counting to ten against the right post with his eyes shut, then setting off to seek', 22, 'none',
    [k(.12, 'post_r', x=.6, y=.8, b=.5, eye='-', mark='one'), k(.3, 'post_r', x=.7, y=.9, b=.6, eye='-', mark='five'), k(.5, 'post_r', x=.7, y=.9, b=.6, eye='-', mark='TEN'), k(.7, y=-.5, x=-.4, w=1, eye='O', mark='ready!'), k(.88, y=.1, w=.3, eye='>')],
    [], g='play', act=('seek', 'post'), ages=GROWN, prefer=['young'])
o.r('jump_out_at_the_lattice', 'Hide and jump-out among the flowers, flattening himself against the lattice and bursting out with a roar', 18, 'none',
    [k(.15, 'flower_r', x=-.3, y=.3, b=.4), k(.35, 'flower_r', x=-.4, y=.6, b=.7, eye='-'), k(.55, 'flower_r', x=-.4, y=.6, b=.7, eye='-', mark='...'), k(.7, y=-.8, b=-.8, w=1, eye='O', mark='RAAH'), k(.88, y=.3, eye='^')],
    [], g='play', act=('hide', 'lattice'), prefer=['young'], say=["RAAH. A flower flinched. I counted it.", "Lattice got the fright of its life."])
o.r('rake_and_dive_the_leaves', 'A rake of the leaves into a heap with his feet, then a dive flat into it', 24, 'none',
    [k(.12, 'floor_l', perch=1, x=.3, y=.5, b=.3, l=1), k(.3, 'floor_c', perch=1, x=.2, y=.7, b=.6, r=1, mark='shff'), k(.5, y=-.6, b=-.8, w=.8), k(.65, 'floor_c', perch=1, y=1.6, b=1.5, w=1, mark='FFWUMP'), k(.88, y=.3, b=.3, eye='^')],
    [(.65, 'scatter')], g='play', act=('rake', 'leaves'), when=['leaves>.3'], prefer=['happy', 'young'], say=["Leaf pile. Deep. Not deep enough.", "Dived. Landed. Leaves everywhere. Peak duck."])
o.r('toss_leaves_like_confetti', 'Throwing a billful of leaves over his head like confetti', 20, 'none',
    [k(.12, 'floor_r', x=.8, y=1.3, b=.5), k(.3, 'floor_r', x=1.1, y=1.6, b=.8, mark='fff'), k(.5, y=-1.2, x=-.4, b=-.8, w=1, eye='^', mark='YAY'), k(.7, y=-.4, b=-.3, w=.8), k(.88, y=.2, eye='-')],
    [(.3, 'scatter')], g='play', act=('throw', 'leaves'), when=['leaves>.3'], prefer=['happy'])
o.r('hop_the_board_seams', 'Hopping the floorboards from the right seam to the left, never touching a crack', 18, 'none',
    [k(.12, 'floor_c', perch=1, x=.3, y=-.3, b=-.4, l=1), k(.3, 'floor_c', perch=1, y=.3, b=.6, r=1, mark='hup'), k(.5, 'floor_l', perch=1, y=-.4, b=-.7, w=.6), k(.7, 'floor_l', perch=1, y=.3, b=.7, l=1, mark='hup'), k(.88, y=-.2, w=.4, eye='^')],
    [], g='play', act=('hop', 'boards'), prefer=['young', 'happy'])
o.r('race_between_the_tubs', 'A race from the left pot to the right, slapping each plant with a wing', 18, 'none',
    [k(.12, 'plant_l', x=.6, y=1, b=.5, l=1, mark='slap'), k(.3, y=-.3, b=-.6, w=.9), k(.5, y=-.3, b=-.6, w=1), k(.7, 'plant_r', x=.6, y=1, b=.5, r=1, mark='SLAP'), k(.88, x=.1, w=.5, eye='^')],
    [], g='play', act=('race', 'pots'), prefer=['young'])
# ---------------- test
o.r('sniff_the_flowers', 'Pressing his bill deep into each flower cluster for a long smell, one after the other', 16, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'flower_l', x=1, y=.6, b=.3, mark='snf'), k(.5, 'flower_l', x=.4, y=.2, eye='-', mark='7/10'), k(.7, 'flower_r', x=1, y=.6, b=.3, mark='snf snf'), k(.88, x=.2, eye='^', mark='8/10')],
    [], g='test', act=('press', 'flowers'), prefer=['curious'], say=["Left: six. Right: seven. Both lying about being rose.", "Pollen. In the nose. Rating: sneeze."])
o.r('knock_the_post_for_hollow', 'Knocking at each post in turn with his bill to hear which one is hollow', 16, 'none',
    [k(.12, 'post_r', x=1, y=-.4, mark='tok'), k(.3, 'post_r', x=.8, y=-.1, b=.3, mark='tok'), k(.5, x=-.4, y=-.5, w=.4, eye='-'), k(.7, 'post_l', x=1, y=-.3, b=.4, mark='tonk'), k(.9, eye='^')],
    [], g='test', act=('knock', 'post'), ages=GROWN)
o.r('knock_the_tub', 'Knocking the left tub with his bill and listening to the clay answer', 14, 'none',
    [k(.15, x=.4, y=.5), k(.3, 'pot_l', x=1, y=1.5, b=.5, mark='tok'), k(.5, 'pot_l', x=1.1, y=1.6, b=.6, mark='tonk'), k(.7, x=-.2, y=.3, eye='-', mark='hollow'), k(.88, eye='^')],
    [], g='test', act=('knock', 'pot'))
o.r('count_the_diamonds', 'Counting the lattice diamonds from the post to the flowers', 22, 'none',
    [k(.1, 'lattice_l2', x=.8, y=-.2, mark='1'), k(.3, 'lattice_l', x=.9, y=.1, b=.2, mark='5'), k(.5, 'lattice_l', x=.9, y=.4, b=.4, l=1, mark='11'), k(.7, 'flower_l', x=.9, y=.3, b=.3, r=1, mark='14'), k(.88, x=-.2, eye='-', mark='lost count')],
    [], g='test', act=('count', 'diamonds'), prefer=['curious'])
o.r('pace_out_the_floor', 'Pacing the floor out to measure it in solemn waddles: nine across, nine back', 22, 'none',
    [k(.1, 'floor_r', perch=1, x=.4, y=.1, b=.2, l=1, mark='1'), k(.3, 'floor_c', perch=1, x=.3, y=.2, b=.3, r=1, mark='5'), k(.5, 'floor_l', perch=1, x=.4, y=.1, b=.2, l=1, mark='9'), k(.72, 'floor_c', perch=1, x=.2, y=.2, b=.3, r=1), k(.9, x=-.2, y=-.1, eye='-', mark='nine')],
    [], g='test', act=('measure', 'floor'), prefer=['curious'], say=["Nine across. Nine back. Floor is exactly a floor.", "Measured. It fits. I knew it would."])
o.r('listen_at_the_post', 'Pressing an ear to the right post to listen for whether the roof is humming', 18, 'none',
    [k(.12, 'rail_up_l', x=.2, y=-.2), k(.3, 'post_r', x=1.1, y=-1.4, b=.3, eye='-'), k(.55, 'post_r', x=1.5, y=-1.8, b=.9, eye='-', mark='...'), k(.78, x=-.3, y=-.5, w=.5, eye='O', mark='nothing')],
    [], g='test', act=('listen', 'post'), ages=GROWN)
o.r('hang_off_the_rail', 'Hanging his full weight at the left side rail to see whether it holds a duck', 18, 'none',
    [k(.15, 'rail_up_l', x=.6, y=-.2, b=.2), k(.35, 'rail_up_l', x=1, y=.2, b=.8, mark='creak'), k(.55, 'rail_up_l', x=1, y=.4, b=1.4, eye='O'), k(.8, x=-.1, y=-.3, eye='-', mark='holds')],
    [], g='test', act=('weigh', 'rail'), ages=GROWN)
o.r('stand_next_to_the_post', 'Testing the left post by shoving his shoulder against it', 18, 'none',
    [k(.15, 'rail_up_l', x=-.3, y=.2, b=.3), k(.35, 'post_l', x=-.3, y=-1.6, b=-1.4, w=.4, eye='O'), k(.6, 'post_l', x=-.4, y=-1.8, b=-1.7, w=.6, eye='>', mark='taller'), k(.8, x=-1.2, y=1.4, b=1.4, w=0, eye='-', mark='ugh')],
    [], g='test', act=('test', 'post'), say=["Post wins by a roof. Fair.", "Tall as a post. Almost. Practically."])
# ---------------- rest
o.r('lean_back_on_the_lattice', 'Leaning his back against the left lattice with his eyes shut', 24, 'none',
    [k(.15, y=.2, x=.2, w=.3), k(.35, 'lattice_l', x=-.5, y=.5, b=.4, eye='-'), k(.6, 'lattice_l', x=-.8, y=1.2, b=1.2, eye='-', mark='z'), k(.85, 'lattice_l', x=-.8, y=1.3, b=1.5, eye='-')],
    [(.6, 'hush')], g='rest', act=('lean', 'lattice'), when=['tired'])
o.r('sulk_at_the_rail', 'Sulking along the side rails with his back to the garden', 24, 'none',
    [k(.15, x=-.5, y=.3, w=.4), k(.35, 'rail_up_r', x=-1.4, y=.5, b=.5, l=1, eye='>'), k(.6, 'rail_up_l', x=-1.4, y=1.8, b=1.5, r=1, eye='-', mark='hmph'), k(.85, 'rail_up_l', x=-2.2, y=1.2, b=.9, eye='-')],
    [], g='rest', act=('sulk', 'rail'), ages=GROWN, when=['sad'], prefer=['grumpy'])
o.r('wait_for_company', 'Keeping guard in the middle of the floor with his bill turned toward the garden path', 26, 'none',
    [k(.15, y=.2, x=.2), k(.4, 'floor_c', perch=1, x=.5, y=-.2, b=.2, eye='>'), k(.65, 'floor_c', perch=1, x=.7, y=-.3, b=.3, eye='>', mark='...'), k(.85, 'floor_c', perch=1, x=.4, y=.3, b=.5, eye='-', mark='sigh')],
    [], g='rest', act=('guard', 'floor'), when=['lonely'])
o.r('perch_on_the_base_rail', 'Perching on the right base rail to watch the garden go dark', 28, 'none',
    [k(.15, 'rail_lo_r', perch=1, y=.2, b=.3), k(.4, 'rail_lo_r', perch=1, y=.5, b=.9, eye='-'), k(.7, 'rail_lo_r', perch=1, y=.4, b=.9, eye='-', mark='...'), k(.9, 'rail_lo_r', perch=1, y=.1, b=.3, eye='o')],
    [], g='rest', act=('perch', 'rail'), when=['dusk'], prefer=['happy'])
# ---------------- weather
o.r('stand_dry_in_the_rain', 'Taking shelter dead centre with his wings tucked in, listening to the rain hammer the roof', 32, 'none',
    [k(.15, 'floor_l', perch=1, y=.1), k(.35, 'floor_c', perch=1, y=.6, x=.2, b=.6, w=0, eye='-'), k(.6, 'floor_c', perch=1, y=.9, x=.1, b=1.2, w=0, eye='-', mark='drum drum'), k(.85, 'floor_c', perch=1, y=.4, x=.2, b=.5, w=0, eye='^', mark='dry')],
    [], g='weather', act=('shelter', 'floor'), when=['wet'], obj=[(.6, dict(shake=.05))], say=["Dry. Smug. Listen to it fall on someone else.", "Roof works. Roof is my friend today."])
o.r('chip_the_frost_off_the_rail', 'Chipping the frost off the side rails with the tip of his bill', 20, 'none',
    [k(.12, 'rail_up_l', x=.6, y=-.3), k(.3, 'rail_up_l', x=1, y=-.1, b=.3, mark='tk'), k(.5, 'rail_up_r', x=1, y=-.1, b=.4, mark='tak'), k(.7, 'rail_up_r', x=1, y=-.1, b=.4, mark='tk'), k(.88, eye='-')],
    [(.5, 'chip')], g='weather', act=('chip', 'rail'), ages=GROWN, when=['cold', 'frost>.3'], prefer=['grumpy'])
o.r('scrape_frost_off_the_lattice', 'Scraping the frost off the right lattice with the edge of a wing', 20, 'wing',
    [k(.12, 'lattice_r', reach=.6, x=.2, y=.2), k(.3, 'lattice_r', reach=1, x=.3, y=.3, b=.2), k(.5, 'lattice_r', reach=1, x=.3, y=.4, b=.3, mark='skr'), k(.7, 'flower_r', reach=1, x=.3, y=.3, b=.2), k(.88, eye='-')],
    [(.5, 'chip')], g='weather', act=('scrape', 'lattice'), when=['cold', 'frost>.3'])
o.r('hold_the_post_in_the_gale', 'Bracing against the left post with both feet planted while the wind comes through', 22, 'none',
    [k(.15, y=.3, x=.3), k(.35, 'post_l', x=1.6, y=1.2, b=1.4, w=.4, r=1), k(.6, 'post_l', x=2, y=1.6, b=1.8, w=.4, eye='>', mark='hnng'), k(.85, 'post_l', x=-1.4, y=1.2, b=1.2, w=.4, l=1)],
    [], g='weather', act=('brace', 'post'), ages=GROWN, when=['windy'], obj=[(.35, dict(sway=.1)), (.6, dict(sway=-.1))])
o.r('warm_his_feet_on_the_boards', 'Standing on the sun-warmed boards and lifting each foot in turn', 24, 'none',
    [k(.15, y=.1, b=.1), k(.35, 'floor_r', perch=1, y=.4, b=.3, l=1, eye='-'), k(.6, 'floor_r', perch=1, y=.4, b=.4, r=1, eye='-', mark='ahh'), k(.85, 'floor_r', perch=1, y=.3, b=.2, l=1, eye='^')],
    [(.6, 'warmfeet')], g='weather', act=('warm', 'floor'), when=['sun', 'warmth>.3'], prefer=['happy'])
o.r('cool_off_in_the_draught', 'Holding his wings out at the open sides of the floor to cool off in the breeze', 24, 'none',
    [k(.15, y=.2, b=.2), k(.35, 'floor_l', perch=1, y=-.4, b=-.3, w=1, eye='-', mark='phew'), k(.6, 'floor_r', perch=1, y=-.5, b=-.4, w=1, eye='^', mark='ahh'), k(.85, 'floor_r', perch=1, y=-.2, b=-.1, w=.4, eye='-')],
    [], g='weather', act=('cool', 'floor'), obj=[(.35, dict(sway=.1)), (.6, dict(sway=-.1))], when=['sun', 'warm'], prefer=['happy'], say=["Open sides. Free breeze. Zero rent.", "Fanning myself. Dignity: optional."])
o.r('wrap_both_wings_round_the_flowers', 'Wrapping both wings round the left flowers to shield them from the gale', 22, 'wing',
    [k(.15, y=.3, x=.2), k(.35, 'flower_l', reach=.8, x=.5, y=.6, b=.4, w=1, mark='whoosh'), k(.6, 'flower_l', reach=1, x=.6, y=.8, b=.6, w=1, eye='>'), k(.85, 'flower_l', reach=.5, x=.3, y=.4, eye='-', mark='there')],
    [], g='weather', act=('wrap', 'flowers'), when=['windy'], prefer=['curious'])
# ---------------- show
o.r('bellow_up_at_the_roof', 'Shouting up at the roof until it answers', 20, 'none',
    [k(.15, y=-.4), k(.35, 'floor_r', perch=1, y=-1.4, x=-.5, b=-.3, w=.5, eye='O', mark='HELLO'), k(.55, 'floor_r', perch=1, y=-1.6, x=-.6, b=-.4, w=1, eye='>', mark='HELLO!'), k(.78, 'floor_r', perch=1, y=-.4, x=-.2, w=.3, eye='-', mark='...hello')],
    [], g='show', act=('shout', 'roof'), say=["Echo is just me, later. Still the best audience.", "Roof says it back. Louder. Cheeky."])
o.r('waltz_the_floor_alone', 'Dancing the length of the floor in a waltz with an invisible partner', 24, 'none',
    [k(.12, 'floor_l', perch=1, x=.2, y=-.2, b=-.2, w=.6, l=1), k(.3, 'floor_r', perch=1, x=.3, y=-.3, b=-.4, w=1, r=1), k(.5, 'floor_l', perch=1, x=.2, y=-.2, b=-.2, w=.6, l=1), k(.7, 'floor_r', perch=1, x=.3, y=-.3, b=-.4, w=1, r=1), k(.88, y=.4, b=.5, w=0, eye='^')],
    [], g='show', act=('dance', 'floor'), prefer=['happy'], say=["My partner is the best lead I ever had.", "One two three. One two floor."])
o.r('tightrope_the_base_rail', 'Balancing along the left base rail like a tightrope with his wings out', 20, 'none',
    [k(.12, 'rail_lo_l', perch=1, x=-.4, y=-.2, b=.4, w=.5, r=1), k(.35, 'rail_lo_l', perch=1, x=.4, y=-.8, b=-.3, w=1, l=1), k(.6, 'rail_lo_m', perch=1, x=-.4, y=-.8, b=-.5, w=1, r=1, eye='O'), k(.8, 'rail_lo_m', perch=1, x=.4, y=.2, b=.3, w=.9, l=1), k(.92, y=.3, w=0, eye='^')],
    [], g='show', act=('balance', 'rail'), prefer=['young', 'happy'])
o.r('serenade_the_flowers', 'Singing to the left flowers with a wing on his chest', 22, 'none',
    [k(.15, y=.2, x=.2), k(.35, 'flower_l', x=.6, y=-.2, b=.2, w=.5, eye='^', mark='la'), k(.6, 'flower_l', x=.8, y=-.4, b=.1, w=.8, eye='-', mark='LAAAH'), k(.85, 'flower_l', x=.4, y=.3, b=.4, w=.3, eye='^', mark='...')],
    [], g='show', act=('sing', 'flowers'), prefer=['happy'], say=["They leaned in. Wind, probably. Allow me this.", "Flowers: attentive. Roof: jealous."])
o.r('pose_at_the_rail', 'Showing off at the right side rail with one wing against the post, like the cover of a magazine about gazebos', 22, 'none',
    [k(.15, y=.2, x=.2), k(.35, 'rail_up_r', x=.8, y=-1.8, b=-.3, w=1, eye='-'), k(.55, 'post_r', x=.8, y=-1.8, b=.6, l=1, eye='^'), k(.8, 'post_r', x=1.2, y=-2, b=.6, l=1, eye='^', mark='click')],
    [], g='show', act=('show', 'rail'), ages=GROWN, prefer=['happy'], say=["Gazebo Monthly. Cover price: one bread.", "Hold it. Hold it. Perfect. Now with attitude."])
o.r('strut_in_like_a_bride', 'Showing how a bride on a bad day strides up the floor, wings back', 24, 'none',
    [k(.12, 'floor_r', perch=1, x=.2, y=-.4, w=.5), k(.35, 'floor_r', perch=1, x=.3, y=-.6, b=-.3, w=.9, l=1, mark='dum dum de dum'), k(.6, 'floor_c', perch=1, x=.3, y=-.6, b=-.3, w=.9, r=1), k(.85, 'floor_c', perch=1, x=.3, y=-.5, w=.5, eye='^', mark='I do')],
    [], g='show', act=('show', 'entry'), say=["I do. I always do. Nobody asks me.", "Bouquet? No. Beak? Yes. Aisle: also yes."][1:] + ["I do. Whatever she's asking, I do."])
o.r('argue_with_the_echo', 'Arguing with his own echo and losing every round', 24, 'none',
    [k(.15, 'floor_l', perch=1, x=.3, y=-.6, w=.4, mark='I win'), k(.35, 'floor_l', perch=1, x=.5, y=-.9, b=-.2, w=.8, eye='>', mark='I WIN'), k(.55, 'floor_l', perch=1, x=-.4, y=-.5, w=0, eye='O', mark='no I win'), k(.75, 'floor_l', perch=1, x=-.6, y=.4, b=.5, eye='-', mark='...hm')],
    [], g='show', act=('argue', 'roof'), prefer=['grumpy'], say=["Echo gets the last word. Always. Cheat.", "Won the argument. Until it replied."])
# ---------------- mishap
o.r('skid_on_the_leaves', 'Slipping on the loose leaves and ending up flat on his back at the entry', 16, 'none',
    [k(.15, 'floor_r', perch=1, x=.4, y=.2, b=.3, l=1), k(.3, 'floor_r', perch=1, x=-.8, y=-.3, b=-.5, r=1, eye='O'), k(.5, 'floor_c', x=-1.8, y=1.8, b=1.8, w=.5, mark='FWAP'), k(.75, y=.8, b=1.2, eye='@'), k(.9, eye='-')],
    [(.5, 'smear')], g='mishap', act=('slip', 'floor'), when=['leaves>.4'], say=["Leaves: slippery. Ego: bruised.", "The floor and I are no longer speaking."])
o.r('head_through_a_diamond', 'Getting stuck with his head through a lattice diamond, having to be a very long duck to get out', 24, 'none',
    [k(.15, x=.5, eye='>'), k(.3, 'lattice_r', x=1.2, y=.4, b=.7, mark='oof'), k(.5, 'lattice_r', x=1.3, y=.4, b=1, l=1, eye='O', mark='mmf'), k(.7, 'lattice_r', x=1.3, y=.4, b=1, r=1, w=1, mark='POP'), k(.88, x=1.6, y=1, b=.6, eye='@')],
    [(.7, 'dent')], g='mishap', act=('stuck', 'lattice'), shown='head', prefer=['young', 'grumpy'], obj=[(.5, dict(shake=0.15)), (.7, dict(shake=0.15))],
    say=["Narrow diamond. Wide ambition.", "Out. Bill: stretched. Pride: elsewhere."])
o.r('bonk_the_post', 'Knocking his head on the right post by gazing up at the roof beams while walking at it', 16, 'none',
    [k(.15, y=-.8, x=-.2, eye='^'), k(.3, 'floor_r', x=.4, y=-.8, b=.2, eye='^'), k(.45, 'post_r', x=1.3, y=.2, b=.5, eye='O', mark='BONK'), k(.65, x=-1, y=-.2, b=-.3, w=.9, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('knock', 'head'), ages=GROWN, say=["Looked up. Post did not. Post: rude.", "Roof: beautiful. Post: also there. Noted."])
o.r('snag_a_feather_in_the_foliage', 'Hooking a wing feather in the foliage while backing off from the right plant', 18, 'none',
    [k(.15, x=-.2, y=.2), k(.35, 'plant_r', x=-.4, y=1.2, b=.8, l=1, r=1, mark='tug'), k(.55, 'plant_r', x=-.6, y=1.6, b=1.2, w=.3, eye='O', mark='RRIP'), k(.75, x=.2, y=.2, b=1.8, eye='@'), k(.9, eye='-')],
    [], g='mishap', act=('hook', 'plant'), say=["It kept the feather. Souvenir.", "Plant 1. Duck 0. Plant to be watched."])
o.r('miss_the_jump_to_the_rail', 'Trying to climb to the top rail with a jump, missing by a wing, and sliding down the lattice', 18, 'none',
    [k(.15, 'lattice_l', x=.3, y=.2, b=.4, l=1), k(.3, y=-1, b=-1.2, w=1, eye='O'), k(.45, 'rail_up_l', x=.6, y=-.2, b=-.5, w=1, mark='grab'), k(.62, 'lattice_l', x=.4, y=.8, b=.9, w=.6, mark='sliiide'), k(.85, y=.6, b=.5, eye='@')],
    [], g='mishap', act=('climb', 'rail'), ages=GROWN, prefer=['young'], say=["Missed by one wing. It was a big wing.", "Rail: unclimbed. Lattice: slid."])
o.r('kick_the_tub_showing_off', 'Throwing a high kick at the right tub rim to impress nobody and meeting it', 16, 'none',
    [k(.15, y=-.2, x=.2), k(.3, 'pot_r', x=.4, y=.2, b=-.6, l=1, w=.5), k(.48, 'pot_r', x=.2, y=.2, b=1, l=1, eye='O', mark='OW'), k(.68, x=-.2, y=-.4, b=-.7, l=1, w=.8, eye='@'), k(.88, eye='-')],
    [], g='mishap', act=('kick', 'pot'), say=["Tub: unharmed. Toe: negotiating.", "High kick. Low result."])
o.emit()

