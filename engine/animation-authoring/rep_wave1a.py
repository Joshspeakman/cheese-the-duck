"""Wave 1a repertoire: tire_swing, toy_seesaw, birdhouse, rubber_duck. Every routine is hand-written."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rep import Obj, k, YOUNG, GROWN

# ============================================================ tire_swing
o = Obj('tire_swing', 'placed',
        fields=dict(swing=(0, 0, 1), rain=(0, 0, 1), twist=(0, 0, 1), leaves=(0, 0, 1), frost=(0, 0, 1)),
        physics=[('swing', 'decay', 0, 'always'), ('swing', 'rate', .02, 'windy'),
                 ('rain', 'rate', .002, 'wet'), ('rain', 'rate', -.0003, 'dry&warm'),
                 ('twist', 'rate', -.0004, 'always'),
                 ('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('frost', 'rate', .002, 'cold'), ('frost', 'rate', -.003, 'warm')],
        effects=dict(
            scrub=[('obj.dirt', 'add', -.4)], scrape=[('obj.dirt', 'add', -.2)], scour=[('obj.dirt', 'add', -.3), ('obj.wetness', 'add', .15)],
            tamp=[('obj.condition', 'add', .1)], huddle=[('need.energy', 'add', 1), ('swing', 'mul', .9)], unkink=[('twist', 'mul', .1), ('swing', 'add', .2)], level=[('obj.condition', 'add', .05), ('twist', 'mul', .5)],
            rock=[('swing', 'add', .4)], wind=[('twist', 'add', .5)], unwind=[('twist', 'set', 0), ('need.fun', 'add', 3)],
            ride=[('swing', 'mul', .6), ('need.fun', 'add', 2)], stop=[('swing', 'mul', .1)], push=[('swing', 'set', 1)],
            nudge=[('swing', 'add', .3)], slap=[('swing', 'add', .2), ('need.fun', 'add', 1)], peek=[('need.fun', 'add', 1)],
            rest=[('need.energy', 'add', 3)], shade=[('need.energy', 'add', 2)], lull=[('need.energy', 'add', 1)],
            pour=[('rain', 'mul', .15)], blot=[('rain', 'mul', .5), ('obj.wetness', 'add', -.4)], thaw=[('frost', 'mul', .2)],
            sweep=[('leaves', 'set', 0)], grip=[('swing', 'mul', .7)], brace=[('swing', 'mul', .8), ('twist', 'add', .1)], splash=[('rain', 'add', -.2), ('obj.wetness', 'add', .3), ('need.fun', 'add', 2)],
            tumble=[('twist', 'mul', .3), ('swing', 'set', .3)], stuck=[('frost', 'mul', .6)], slip=[('rain', 'mul', .8), ('obj.wetness', 'add', .2)],
            wedge=[('swing', 'add', .4), ('obj.condition', 'add', -.05)], bonk=[('swing', 'mul', .5)], tally=[('leaves', 'add', .2)]),
        anchors=dict(tyre_low=(.53, .905), hole=(.53, .85), tyre_side=(.41, .78), tyre_far=(.62, .78), tyre_rim_l=(.33, .865), tyre_rim_r=(.68, .865),
                     tyre_crown=(.53, .66), rope_hang=(.53, .62), post_foot=(.15, .93), post_waist=(.15, .81), post_high=(.15, .65)))
# --- care
o.r('wipe_mud', "Wiping dried mud off the tyre's flank with a wing, left rim to right", 16, 'wing',
    [k(.15, 'tyre_rim_l', reach=.6, w=.4), k(.4, 'tyre_rim_l', x=.4, w=.8, mark='skrk'), k(.65, 'tyre_rim_r', x=.5, w=.8, mark='skrk'), k(.85, eye='^')],
    [(.65, 'scrub')], g='care', obj=[(.4, dict(sway=.2)), (.65, dict(sway=-.2))])
o.r('peck_tread', "Pecking caked mud out of the tread along the tyre's underside", 14, 'none',
    [k(.2, 'tyre_low', y=.9, b=.4), k(.4, 'tyre_low', y=1.3, b=.6, mark='tk'), k(.6, 'tyre_rim_l', y=1.3, b=.6, mark='tk'), k(.85, y=.2, eye='^')],
    [(.6, 'scrape')], g='care', obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))])
o.r('scour_hole', "Scouring bird muck off the inside of the hole with his bill, far wall last", 18, 'none',
    [k(.2, 'hole', x=.9, y=.4, b=.3), k(.45, 'hole', x=1.2, y=.6, b=.5, mark='skritch'), k(.65, 'tyre_far', x=1.2, y=.3, b=.5), k(.85, x=-.3, eye='^')],
    [(.65, 'scour')], g='care', say=["Whose muck is this. Don't answer, it's obviously a pigeon's.", "Scrubbed it. The pigeon will just do it again out of spite."],
    obj=[(.45, dict(sway=.3)), (.65, dict(sway=.3))])
o.r('tamp_post_foot', "Tamping the soil back down around the post's foot, one foot then the other", 16, 'none',
    [k(.2, 'post_foot', y=.4, b=.4, l=1), k(.4, 'post_foot', b=.4, r=1), k(.6, 'post_foot', b=.4, l=1), k(.82, eye='^', mark='ha')],
    [(.6, 'tamp')], g='care', ages=GROWN)
o.r('unkink_rope', "Pushing the tyre back round against the twist, far wall first, until the rope hangs straight", 20, 'wing',
    [k(.15, 'tyre_far', reach=.5, w=.4), k(.35, 'tyre_far', x=.7, w=.8, b=.2, mark='hnng'), k(.55, 'tyre_side', x=.7, w=.8, b=.2, mark='hnng'), k(.8, eye='^')],
    [(.55, 'unkink')], g='care', when=['twist>.4'], obj=[(.35, dict(sway=.3)), (.55, dict(sway=-.5)), (.75, dict(sway=.2))])
o.r('twig_level', "Hooking the rope with a twig and hauling it down until the tyre hangs level", 22, 'twig',
    [k(.15, 'rope_hang', reach=.7, w=.3), k(.4, 'rope_hang', x=.5, y=-.4, b=.3, mark='hnf'), k(.6, 'rope_hang', x=.5, y=-.4, b=.6, l=1), k(.85, eye='^')],
    [(.6, 'level')], g='care', prefer=['twist>.2', 'grown'], obj=[(.6, dict(sway=.5)), (.8, dict(sway=-.2))])
# --- use
o.r('sit_in_hole', "Settling into the hole with his tail out the back and rocking his hips", 18, 'none',
    [k(.2, 'hole', x=.8, y=.4, b=.2), k(.4, 'hole', x=.3, b=.9, mark='plop'), k(.6, 'hole', x=.3, b=.9, w=.3, mark='hup'), k(.8, x=-.2, b=.2, eye='^')],
    [(.4, 'rock')], g='use', when=['swing<.5'], prefer=['swing<.2', 'happy'], obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.5)), (.8, dict(sway=.3))])
o.r('wind_it_up', "Walking the tyre round and round to wind the rope up tight", 22, 'wing',
    [k(.15, 'tyre_side', reach=.5, w=.5), k(.35, 'tyre_side', x=.8, w=.9, b=.3, l=1), k(.55, 'tyre_far', x=.8, w=.9, b=.3, r=1, mark='hnnng'), k(.8, x=-.4, y=.6, eye='O')],
    [(.55, 'wind')], g='use', when=['twist<.6'], prefer=['curious'], obj=[(.35, dict(sway=.3)), (.55, dict(sway=.5, shake=.2))])
o.r('ride_the_unwind', "Sitting in the hole while the rope spins itself out, bill pointing outward", 20, 'none',
    [k(.2, 'hole', x=.8, y=.4, b=.2), k(.4, 'hole', x=.6, b=.8, eye='@', mark='wheee'), k(.65, 'hole', x=.6, b=.8, w=1, eye='@'), k(.85, x=.2, y=.9, b=.5, eye='O')],
    [(.4, 'unwind')], g='use', when=['twist>.4'], prefer=['happy'], obj=[(.4, dict(sway=.4)), (.65, dict(shake=.4))],
    say=["Round and round. Gave me a new perspective: nothing has changed.", "Nope. Nothing's stopped spinning. Including me."])
o.r('hop_on_mid_swing', "Hopping into the hole as the tyre swings past and riding it out", 18, 'none',
    [k(.2, x=.4, b=-.6, eye='>'), k(.4, 'hole', x=.5, b=-.2, w=1, mark='hup'), k(.6, 'hole', x=.3, b=.7, mark='...'), k(.85, x=-.3, b=.2, eye='^')],
    [(.4, 'ride')], g='use', when=['swing>.5'], prefer=['happy', 'young'], obj=[(.4, dict(sway=1)), (.6, dict(sway=-.7)), (.85, dict(sway=.2))])
o.r('brake_with_feet', "Planting both feet and gripping the tyre's low rim to stop the swing dead", 14, 'none',
    [k(.2, x=.6, y=.2), k(.4, 'tyre_low', x=1, y=.7, b=.6, l=1, r=1, mark='skrrk'), k(.65, 'tyre_low', x=1, y=.7, b=.6, eye='-'), k(.85, eye='^')],
    [(.4, 'stop')], g='use', when=['swing>.5'], obj=[(.2, dict(sway=1)), (.4, dict(shake=.5)), (.7, dict(sway=0))])
o.r('shoulder_it_out', "Backing off, running at the tyre and shouldering its flank into a first swing", 16, 'none',
    [k(.2, x=-.6, b=.4), k(.4, 'tyre_rim_l', x=1.2, y=.2, w=.6, mark='HUP'), k(.55, x=.3, b=-.3), k(.8, eye='^')],
    [(.4, 'push')], g='use', when=['swing<.2'], prefer=['grown'], obj=[(.4, dict(sway=.8)), (.6, dict(sway=-.9)), (.8, dict(sway=.6))])
# --- play
o.r('shove_and_duck', "Shoving the tyre off and flattening himself as it sails back over his head", 18, 'wing',
    [k(.15, 'tyre_low', reach=.6, w=.5), k(.3, 'tyre_low', x=.4, b=-.3, w=1, mark='hup'), k(.5, y=1.4, b=.9, eye='O'), k(.7, y=1.4, b=.9, eye='-', mark='whoosh'), k(.88, eye='^')],
    [(.3, 'push')], g='play', prefer=['swing<.2', 'happy'], obj=[(.3, dict(sway=.3)), (.45, dict(sway=1)), (.6, dict(sway=-1)), (.75, dict(sway=.5))])
o.r('through_the_hole', "Diving through the hole in one go and skidding out the far side on his chest", 16, 'none',
    [k(.2, x=.2, b=.5, eye='>'), k(.4, 'hole', x=1.5, y=.3, b=.2, w=1, mark='fwip'), k(.6, 'tyre_far', x=1.6, y=1, b=.8, eye='@'), k(.85, y=.2, eye='^')],
    [(.4, 'nudge')], g='play', prefer=['happy', 'young'], obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.4))], say=["Through the hole. Out the other side. Nothing changed. Still me.", "Threaded myself. Eight out of ten, dismount was ropey."])
o.r('peck_the_pendulum', "Pecking the swinging tyre at the bottom of every pass", 20, 'none',
    [k(.2, 'tyre_low', y=.6, b=.3, mark='tk'), k(.4, 'tyre_side', x=.5, y=.9, b=.3, mark='tk'), k(.6, 'tyre_low', y=.6, b=.3, mark='tk'), k(.85, y=-.1, eye='^')],
    [(.4, 'slap')], g='play', when=['swing>.3'], prefer=['curious'], obj=[(.2, dict(sway=.8)), (.4, dict(sway=-.6)), (.6, dict(sway=.5))])
o.r('high_five_pass', "Slapping the tyre's flank as it swings by, like a high five from something with no hands", 14, 'wing',
    [k(.2, x=-.3, w=.5), k(.4, 'tyre_rim_r', reach=1, w=1, mark='SLAP'), k(.55, w=.2, x=.2), k(.8, eye='^')],
    [(.4, 'slap')], g='play', when=['swing>.3'], prefer=['happy'], obj=[(.3, dict(sway=.7)), (.5, dict(sway=-.5))])
o.r('hide_behind_post', "Ducking behind the post as the tyre swings and peeking round it every pass", 20, 'none',
    [k(.2, 'post_waist', x=-.2, y=.3, b=.2, eye='o'), k(.4, 'post_waist', x=.6, y=.3, eye='O'), k(.6, 'post_waist', x=-.2, y=.3, eye='o'), k(.8, 'post_waist', x=.6, y=.3, eye='O', mark='ha')],
    [(.8, 'peek')], g='play', when=['swing>.3'], prefer=['curious'], obj=[(.2, dict(sway=.7)), (.5, dict(sway=-.6)), (.8, dict(sway=.5))])
o.r('poke_and_run', "Poking the tyre's low rim and sprinting off before it can come back round", 14, 'none',
    [k(.2, 'tyre_low', x=1, y=.5, b=.3, mark='boop'), k(.4, x=-.8, b=-.4, w=1, eye='>'), k(.6, x=-1.2, b=-.4, l=1, eye='>'), k(.85, x=-.2, y=.3, eye='O', mark='...')],
    [(.2, 'nudge')], g='play', prefer=['grumpy', 'young'], obj=[(.25, dict(sway=.6)), (.6, dict(sway=-.6))], say=["Poked it. Ran. It's still coming. They always come back.", "I'm not scared. I'm tactically elsewhere."])
# --- test
o.r('shake_the_post', "Throwing his whole weight against the post to see how firmly it is set", 14, 'none',
    [k(.2, x=-.5, y=.2), k(.4, 'post_waist', x=1.3, b=.4, mark='hup'), k(.6, 'post_waist', x=1.3, b=.4, mark='...'), k(.85, x=.1, eye='-')],
    [(.4, 'nudge')], g='test', obj=[(.4, dict(shake=.5)), (.6, dict(shake=.2))])
o.r('sniff_the_rubber', "Sniffing the tyre's side wall for any trace of what the tyre used to be on", 14, 'none',
    [k(.2, x=.5, y=.3), k(.45, 'tyre_rim_l', x=1, y=.9, b=.4, eye='o', mark='snf'), k(.65, 'tyre_rim_l', x=.9, y=1, b=.4, eye='O', mark='snf'), k(.85, y=-.2, eye='-')],
    [], g='test', say=["Rubber. Old rubber. A tyre that's seen things. Mostly dogs.", "Smells like a road. Never been on a road. Hate it."])
o.r('hang_off_the_rim', "Hanging off the tyre's far rim by his bill, feet off the ground, to test the rope", 16, 'none',
    [k(.2, 'tyre_rim_r', x=1, y=.6, b=.3), k(.4, 'tyre_rim_r', x=1, y=.6, l=1, r=1, b=-.4, mark='hnn'), k(.6, 'tyre_rim_r', x=1, y=.6, l=1, r=1, b=-.4, eye='>'), k(.82, b=.3, y=.5, eye='O')],
    [(.4, 'nudge')], g='test', obj=[(.4, dict(sway=.5)), (.6, dict(sway=.5, shake=.2)), (.82, dict(sway=-.3))])
o.r('knock_for_hollow', "Knocking on the tyre's wall with his bill to hear what the inside says back", 14, 'none',
    [k(.2, 'tyre_rim_r', x=.8, y=.7), k(.4, 'tyre_rim_r', x=1.2, y=.7, mark='tok'), k(.6, 'tyre_rim_r', x=.8, y=.7, mark='tok'), k(.82, eye='o', x=-.2)],
    [], g='test', prefer=['curious'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))])
o.r('peer_through_hole', "Pushing his bill into the hole and squinting at the world through a ring", 14, 'none',
    [k(.2, x=.4, y=.4), k(.45, 'hole', x=1.4, y=.2, b=.3, eye='o'), k(.7, 'hole', x=1.4, y=.2, b=.3, eye='O', mark='hm'), k(.88, x=0, eye='-')],
    [], g='test', prefer=['curious'])
o.r('count_the_spins', "Nudging the tyre once and counting how many times the twist spins it", 18, 'none',
    [k(.2, 'tyre_rim_l', x=.8, y=.4), k(.35, 'tyre_rim_l', x=1.2, y=.4, mark='tap'), k(.55, x=-.2, y=-.3, eye='o'), k(.75, x=-.2, y=-.3, eye='@', mark='...'), k(.9, eye='-')],
    [(.35, 'nudge')], g='test', prefer=['twist>.2', 'curious'], obj=[(.35, dict(sway=.5)), (.6, dict(sway=-.4)), (.8, dict(sway=.2))])
# --- rest
o.r('nap_in_hole', "Curling up in the hole with his head under his wing while the tyre creaks him to sleep", 30, 'none',
    [k(.2, 'hole', x=.8, y=.5, b=.4), k(.4, 'hole', x=.3, y=1, b=1, eye='-'), k(.7, 'hole', x=.3, y=1.1, b=1, eye='-', mark='zzz'), k(.9, y=.3, b=.3, eye='^')],
    [(.4, 'rest')], g='rest', when=['swing<.3'], prefer=['tired', 'night'], obj=[(.4, dict(sway=.2)), (.7, dict(sway=-.2))])
o.r('lean_on_post', "Leaning his back against the post and watching the tyre do nothing", 20, 'none',
    [k(.2, 'post_waist', x=-.3, y=.1), k(.5, 'post_waist', x=-.5, b=.3, eye='-', w=.2), k(.75, 'post_waist', x=-.5, b=.3, eye='-'), k(.9, eye='^')],
    [(.5, 'lull')], g='rest', prefer=['tired', 'sad'])
o.r('sit_in_its_shade', "Parking himself under the tyre's shadow in the heat with his eyes shut", 24, 'none',
    [k(.2, 'tyre_low', y=.4, b=.5), k(.45, 'tyre_low', y=.6, b=.9, eye='-'), k(.75, 'tyre_low', y=.6, b=.9, eye='-', mark='ahh'), k(.9, y=0, b=.2, eye='^')],
    [(.45, 'shade')], g='rest', when=['sun', 'warm', 'day'], prefer=['tired'], obj=[(.45, dict(sway=.1))])
o.r('sulk_at_the_post', "Turning his back on the tyre and sulking at the post's foot", 22, 'none',
    [k(.2, 'post_foot', x=-.6, y=.5, b=.4), k(.45, 'post_foot', x=-.8, y=.8, b=.8, eye='-'), k(.75, 'post_foot', x=-.8, y=.8, b=.8, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [(.45, 'lull')], g='rest', when=['sad'], say=["Nobody asked the swing. The swing didn't offer. Fine.", "I'm not sulking. I'm the post now."])
o.r('shelter_in_the_storm', "Backing under the tyre's dripping rim with his tail to the weather until the storm gives up", 32, 'none',
    [k(.2, 'tyre_rim_l', x=-.8, y=.4, b=.4), k(.4, 'tyre_low', x=-.5, y=.9, b=.9, w=.2, eye='-'), k(.7, 'tyre_low', x=-.5, y=1, b=1, w=.2, eye='-', mark='...'), k(.9, 'tyre_rim_l', y=.3, b=.3, eye='O')],
    [(.4, 'huddle')], g='rest', when=['storm', 'wet'], obj=[(.4, dict(shake=.4)), (.7, dict(shake=.5))])
o.r('count_swings_sitting', "Sitting at the post's foot watching the swinging tyre until his head goes back and forth too", 24, 'none',
    [k(.2, 'post_foot', x=.3, b=.5, eye='o'), k(.4, 'post_foot', x=.6, b=.6, eye='o'), k(.6, 'tyre_rim_l', x=-.2, b=.6, eye='@'), k(.85, 'post_foot', x=.6, b=.6, eye='-', mark='zz')],
    [(.6, 'peek')], g='rest', when=['swing>.4'], obj=[(.2, dict(sway=.9)), (.4, dict(sway=-.9)), (.6, dict(sway=.8)), (.8, dict(sway=-.6))])
# --- show
o.r('throne_pose', "Sitting up in the hole with his chest out like it is a throne and the yard is his", 18, 'none',
    [k(.2, 'hole', x=.8, y=.3, b=.2), k(.4, 'hole', x=.1, y=-.5, b=.8, w=.6, eye='^'), k(.7, 'hole', x=.1, y=-.7, b=.8, w=1, mark='ha'), k(.88, x=-.1, eye='^')],
    [(.4, 'peek')], g='show', when=['swing<.4'], prefer=['happy', 'grown'], obj=[(.4, dict(sway=.3)), (.7, dict(sway=-.2))],
    say=["Sat in a tyre. Called it a throne. Nobody argued. Nobody was here.", "All hail me. The swing's the ruler of nothing."])
o.r('ringmaster_bow', "Bowing to the empty yard and spinning the tyre for the grand finale", 20, 'wing',
    [k(.2, 'tyre_rim_l', reach=.8, w=.8, y=.6), k(.4, x=-.4, y=1.2, w=1, mark='ta-da'), k(.65, 'tyre_side', reach=1, w=1, x=.6, mark='HUP'), k(.85, eye='^', w=.6)],
    [(.65, 'wind')], g='show', when=['twist<.5'], prefer=['happy'], obj=[(.65, dict(sway=.7, shake=.1)), (.85, dict(sway=-.4))])
o.r('argue_with_the_tyre', "Squaring up to the tyre with his bill against its rim and listing everything wrong with it", 20, 'none',
    [k(.2, 'tyre_far', x=1, y=.6, eye='>'), k(.4, 'tyre_far', x=1.2, y=.8, b=.2, mark='quack'), k(.6, 'tyre_far', x=1, y=.6, eye='>', mark='QUACK'), k(.85, x=-.4, y=.2, eye='-', mark='hmph')],
    [], g='show', prefer=['grumpy'], say=["It's a circle. It's a rubber circle. Why's everyone so impressed.", "I've been outclassed by something that hangs from a rope."])
o.r('judge_the_exhibit', "Pacing round the post and under the tyre like a judge at a show, then scoring it with a nod", 22, 'none',
    [k(.2, 'post_foot', x=.2, y=.2, b=.3), k(.4, 'post_foot', x=.5, y=-.2, eye='o'), k(.6, 'tyre_low', x=.5, y=.3, b=.2, eye='O'), k(.85, 'tyre_low', x=.3, y=.4, eye='-', mark='six')],
    [(.6, 'peek')], g='show', prefer=['curious', 'grown'], obj=[(.6, dict(sway=.2))])
o.r('flamingo_in_the_hole', "Standing on one foot in the centre of the hole and holding a pose until it wobbles", 18, 'none',
    [k(.2, 'hole', x=.5, y=.2), k(.4, 'hole', x=.2, y=-.4, l=1, w=.7, eye='^'), k(.65, 'hole', x=.2, y=-.4, l=1, w=1, eye='O', mark='...'), k(.88, x=.1, eye='-')],
    [(.4, 'grip')], g='show', when=['swing<.2'], prefer=['curious'], obj=[(.4, dict(sway=.2)), (.65, dict(sway=-.3)), (.8, dict(sway=.3))])
o.r('hold_court_by_the_post', "Holding court at the post with one wing on it, telling a story at an audience of rope", 22, 'wing',
    [k(.2, 'post_waist', reach=.8, w=.5, x=.2), k(.4, 'post_waist', reach=.8, w=1, x=.5, mark='and then'), k(.6, 'post_waist', reach=.8, w=.7, y=-.4, mark='...'), k(.85, x=0, eye='^')],
    [(.4, 'peek')], g='show', prefer=['lonely', 'happy'], say=["And then I said, nobody. Because I'm speaking to a post.", "Lovely crowd. Doesn't heckle. Doesn't leave."])
# --- weather
o.r('tip_out_the_rain', "Heaving the tyre's low side up on its rope until the pooled rain sluices out over his feet", 22, 'wing',
    [k(.15, 'tyre_low', reach=.5, w=.4), k(.35, 'tyre_low', y=-.4, b=-.3, w=1, mark='hng'), k(.55, 'hole', x=.3, y=.4, b=.5, mark='glug'), k(.75, x=-.5, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
    [(.55, 'pour')], g='weather', when=['!wet', 'rain>.3'], ages=GROWN, obj=[(.35, dict(sway=.6)), (.6, dict(sway=.6, shake=.3)), (.8, dict(sway=0))])
o.r('blot_it_dry', "Rubbing the damp tyre dry with his tail feathers, rim to rim", 18, 'none',
    [k(.2, 'tyre_rim_r', x=-.6, y=.3, b=.4), k(.4, 'tyre_rim_r', x=-.9, y=.3, b=.5, w=.5, mark='fff'), k(.6, 'tyre_rim_l', x=-.9, y=.3, b=.5, w=.5, mark='fff'), k(.85, eye='^')],
    [(.6, 'blot')], g='weather', when=['!wet', 'rain>.15'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=-.3))])
o.r('chip_off_the_frost', "Chipping the frost off the tyre's side with the edge of his bill", 20, 'none',
    [k(.2, 'tyre_side', x=.7, y=.7, b=.3), k(.4, 'tyre_side', x=1.1, y=.9, b=.4, mark='tik'), k(.6, 'tyre_side', x=1.1, y=.9, b=.4, mark='tik'), k(.85, y=0, eye='^')],
    [(.6, 'thaw')], g='weather', when=['frost>.3'], say=["Frost. The tyre's gone all sparkly. It had a plan and I ruined it.", "Chipped it off. It'll be back. So will I."],
    ages=GROWN, obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))])
o.r('sweep_leaves_out', "Sweeping the heap of drifted leaves out of the hole with his wing", 20, 'wing',
    [k(.15, 'hole', reach=.5, w=.4), k(.4, 'hole', x=.5, w=.9, mark='fshh'), k(.6, 'tyre_low', x=.7, w=.9, b=.3, mark='fshh'), k(.85, eye='^')],
    [(.6, 'sweep')], g='weather', when=['leaves>.3'], prefer=['fall'], obj=[(.4, dict(sway=.2)), (.6, dict(sway=-.2))])
o.r('hold_on_in_the_gust', "Wedging into the hole with his wings clamped as a gust rocks the whole tyre", 18, 'none',
    [k(.2, 'hole', x=.7, y=.4, b=.5), k(.4, 'hole', x=.2, y=.6, b=.8, eye='>', mark='eek'), k(.65, 'hole', x=.2, y=.6, b=.8, eye='@'), k(.85, y=.1, eye='O')],
    [(.4, 'brace')], g='weather', when=['windy', 'swing>.2'], obj=[(.3, dict(sway=.9)), (.5, dict(sway=-.9)), (.7, dict(sway=.8))])
o.r('stamp_the_puddle', "Stamping about in the rain pooled in the hole, one foot after the other", 16, 'none',
    [k(.2, 'hole', y=.3, l=1), k(.4, 'hole', y=.3, r=1, mark='splt'), k(.6, 'hole', y=.3, l=1, mark='splt'), k(.82, b=-.3, w=.8, eye='^')],
    [(.4, 'splash')], g='weather', when=['rain>.5', '!wet'], prefer=['happy', 'young'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.3))],
    say=["Puddle. Mine. Finders keepers, droppers weepers.", "Boots are for people with fewer feathers."])
# --- mishap
o.r('wedged_in_hole', "Diving through the hole, wedging at the hips and kicking until he pops out", 24, 'none',
    [k(.15, x=.5, eye='>'), k(.3, 'hole', x=1.1, y=-.3, b=.8, mark='oof'), k(.5, 'hole', x=1.1, y=-.3, b=1, l=1, eye='O', mark='...'), k(.68, 'hole', x=1.2, y=-.3, b=1, r=1, w=1, mark='POP'), k(.85, x=1.6, y=.9, b=.6, eye='@')],
    [(.3, 'wedge'), (.68, 'wedge')], g='mishap', prefer=['young', 'grumpy'], obj=[(.3, dict(sway=.5)), (.5, dict(shake=.6)), (.68, dict(sway=-.6)), (.85, dict(sway=.2))],
    say=["Wedged by the arse. Dignity: gone.", "I meant to do that. All of it. Especially the stuck part."])
o.r('hit_by_the_return', "Standing in the arc and taking the tyre in the back of the head on its way home", 16, 'none',
    [k(.2, x=.3, y=.2, eye='o'), k(.4, 'tyre_rim_r', x=-.8, y=.8, b=.6, eye='O', mark='bonk'), k(.6, x=-.2, y=1.6, b=1, eye='@', mark='...'), k(.85, y=.4, eye='-')],
    [(.4, 'bonk')], g='mishap', when=['swing>.5'], say=["OW. Shit. Okay. Zero stars, would touch again.", "That's the last time I turn my back on a tyre."],
    obj=[(.3, dict(sway=1)), (.45, dict(sway=-.4)), (.6, dict(shake=.3))])
o.r('slip_on_the_wet_tread', "Skidding down the wet tyre wall and landing in the rain pooled below", 16, 'none',
    [k(.2, 'tyre_side', x=.6, y=.5, b=.3), k(.4, 'tyre_side', x=.2, y=.2, b=-.3, l=1, r=1, eye='O', mark='whoa'), k(.6, 'tyre_low', x=-.4, y=1.4, b=1, eye='@', mark='splat'), k(.85, y=.4, eye='-')],
    [(.6, 'slip')], g='mishap', when=['rain>.25'], obj=[(.4, dict(sway=.4)), (.6, dict(shake=.4))])
o.r('spun_out_dizzy', "Letting go too late and being flung out of the spin to land in a heap", 18, 'none',
    [k(.2, 'hole', x=.6, b=.8, eye='@'), k(.4, 'hole', x=.6, b=.8, w=1, eye='@'), k(.6, x=1.8, y=1.2, b=.6, w=1, eye='@', mark='WHUMP'), k(.85, x=.4, y=.6, b=.8, eye='-')],
    [(.4, 'tumble')], g='mishap', when=['twist>.4'], prefer=['young'], obj=[(.4, dict(sway=.8)), (.55, dict(shake=.8))])
o.r('bill_frozen_to_the_rim', "Pecking the frosted tyre and getting his bill stuck to it, tugging free", 22, 'none',
    [k(.2, 'tyre_rim_l', x=.8, y=.7, b=.4), k(.35, 'tyre_rim_l', x=1.2, y=.8, b=.5, mark='tk'), k(.55, 'tyre_rim_l', x=1.2, y=.8, b=.5, l=1, eye='>', mark='mmf'), k(.75, 'tyre_rim_l', x=.4, y=.6, b=.2, w=1, eye='@', mark='POP'), k(.9, y=.2, eye='-')],
    [(.55, 'stuck')], g='mishap', when=['frost>.5'], say=["Bill stuck to it. Nobody saw that. Nobody's allowed to have seen that.", "Frost has a sense of humour, and it's trash."],
    obj=[(.55, dict(shake=.5))])
o.r('missed_the_hop', "Hopping for the hole, hitting the tyre's flank instead and bouncing off on his back", 16, 'none',
    [k(.2, x=.3, b=.5, eye='>'), k(.4, 'tyre_side', x=1, b=-.8, w=1, mark='hup'), k(.6, x=-1.2, y=1.2, b=.8, l=1, r=1, eye='@', mark='thud'), k(.85, x=0, y=.5, eye='-')],
    [(.4, 'tally')], g='mishap', prefer=['young'], obj=[(.4, dict(sway=.7)), (.6, dict(sway=-.5))])
o.emit()

# ============================================================ toy_seesaw
o = Obj('toy_seesaw', 'placed',
        fields=dict(tilt=(.5, 0, 1), damp=(0, 0, 1), squeak=(0, 0, 1), snowcap=(0, 0, 1)),
        physics=[('tilt', 'decay', .5, 'always'), ('damp', 'rate', .002, 'wet'), ('damp', 'rate', -.0003, 'dry&warm'),
                 ('squeak', 'rate', .0004, 'damp>.3'), ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm')],
        effects=dict(
            tip_lo=[('tilt', 'set', 0)], tip_hi=[('tilt', 'set', 1)], level=[('tilt', 'set', .5), ('squeak', 'mul', .8)],
            bounce_lo=[('tilt', 'add', -.3)], bounce_hi=[('tilt', 'add', .3)],
            wipe=[('damp', 'mul', .3), ('obj.wetness', 'add', -.4)], drain=[('damp', 'mul', .4), ('tilt', 'add', .3)],
            splash=[('damp', 'mul', .8), ('obj.wetness', 'add', .2), ('need.fun', 'add', 2)], hush=[('squeak', 'mul', .4)],
            creak=[('squeak', 'add', .3), ('tilt', 'add', .1)], rattle=[('squeak', 'add', .2), ('need.fun', 'add', 1)],
            sweep_snow=[('snowcap', 'set', 0)], kick_snow=[('snowcap', 'mul', .5), ('need.fun', 'add', 1)],
            scrub=[('obj.dirt', 'add', -.3)], scrape=[('obj.dirt', 'add', -.15)], mend=[('obj.condition', 'add', .1)],
            knock=[('obj.condition', 'add', -.05)], slip=[('damp', 'mul', .8), ('tilt', 'add', -.3)],
            shade=[('need.energy', 'add', 2)], huddle=[('need.energy', 'add', 1), ('damp', 'mul', .95)], doze=[('need.energy', 'add', 3)],
            cheer=[('need.fun', 'add', 1)], wait=[('need.social', 'add', 1)]),
        anchors=dict(base_l=(.44, .95), base_r=(.58, .95), leg_l_low=(.45, .88), leg_r_low=(.575, .88), brace_foot=(.51, .93), brace_low=(.51, .857),
                     brace_mid=(.51, .786), leg_l_mid=(.475, .738), leg_r_mid=(.55, .738), cradle=(.51, .667), plank_under_l=(.22, .62), plank_under_r=(.74, .62),
                     plank_l=(.2, .595), plank_r=(.78, .595), hinge_plate=(.51, .595), hinge_pin=(.5, .571), seat_floor_l=(.18, .548), seat_floor_r=(.8, .548)))
# --- care
o.r('scrub_the_base', "Scrubbing the dried mud off the base bar with a wing, end to end", 16, 'wing',
    [k(.15, 'base_l', reach=.5, w=.4, y=.5), k(.4, 'base_l', x=.4, w=.8, y=.6, mark='skrk'), k(.65, 'base_r', x=.4, w=.8, y=.6, mark='skrk'), k(.85, eye='^')],
    [(.65, 'scrub')], g='care', obj=[(.4, dict(shake=.1)), (.65, dict(shake=.1))])
o.r('pick_dust_from_hinge', "Picking packed dust out around the hinge pin with the tip of his bill", 18, 'wing',
    [k(.2, 'hinge_pin', reach=.6, w=.5, y=-.3), k(.4, 'hinge_pin', x=.6, y=-.2, mark='tk'), k(.6, 'hinge_plate', x=.6, y=-.1, mark='tk'), k(.85, x=0, eye='^')],
    [(.6, 'scrape')], g='care', ages=GROWN, obj=[(.4, dict(shake=.1)), (.6, dict(shake=.1))])
o.r('stamp_the_brace_true', "Stamping the loose brace foot back into line, left foot then right", 14, 'none',
    [k(.2, 'brace_foot', y=.4, b=.4, l=1), k(.4, 'brace_foot', y=.4, b=.4, r=1, mark='thud'), k(.6, 'brace_low', y=.4, b=.4, l=1, mark='thud'), k(.85, eye='^')],
    [(.6, 'mend')], g='care', obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))])
o.r('lift_the_low_end_level', "Wedging his back under the plank's low end and pushing until the seat boxes sit level", 20, 'none',
    [k(.2, 'plank_under_l', x=-.3, y=.4, b=.5), k(.4, 'plank_under_l', x=-.3, y=.6, b=-.3, mark='hng'), k(.6, 'plank_under_l', x=-.3, y=.4, b=-.5, w=.6, mark='HUP'), k(.85, x=0, y=.2, eye='^')],
    [(.6, 'level')], g='care', when=['tilt<.3'], ages=GROWN, obj=[(.4, dict(sway=.3)), (.6, dict(sway=-.3)), (.8, dict(sway=0))])
o.r('lean_on_the_high_end', "Leaning on the hinge plate with one wing until the high end sinks back to level", 16, 'wing',
    [k(.2, 'hinge_plate', reach=.7, w=.5, x=.3), k(.45, 'hinge_plate', reach=.9, w=.9, x=.6, y=.3, mark='hnn'), k(.7, 'hinge_plate', reach=.9, w=.9, x=.6, y=.3, eye='-'), k(.88, eye='^')],
    [(.7, 'level')], g='care', when=['tilt>.7'], ages=GROWN, obj=[(.45, dict(sway=.4)), (.7, dict(sway=-.4))])
o.r('dust_the_seat_box', "Dusting the seat box with a twig, leaning back to see it from afar", 20, 'twig',
    [k(.2, 'seat_floor_l', reach=.8, w=.3, y=-.3), k(.4, 'seat_floor_l', reach=1, w=.7, y=-.5, mark='fff'), k(.6, 'seat_floor_r', reach=1, w=.7, y=-.5, mark='fff'), k(.85, y=.1, eye='-')],
    [(.6, 'scrub')], g='care', prefer=['grown', 'curious'], obj=[(.4, dict(shake=.1))])
# --- use
o.r('hang_and_drop_the_end', "Taking the plank's low-side edge in his bill and hanging off it until that end bangs down", 18, 'none',
    [k(.2, 'plank_under_l', x=.8, y=-.2, b=.3), k(.4, 'plank_under_l', x=.9, y=-.1, b=-.6, l=1, r=1, mark='hnn'), k(.6, 'plank_under_l', x=.9, y=0, b=.2, l=1, r=1, eye='>', mark='BANG'), k(.85, b=.5, y=.3, eye='O')],
    [(.6, 'tip_lo')], g='use', when=['tilt>.3'], ages=GROWN, prefer=['grown'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=-1, shake=.4)), (.85, dict(sway=-.3))])
o.r('heave_the_end_up', "Putting his shoulder under the far end of the plank and heaving it up high", 20, 'none',
    [k(.2, 'plank_under_r', x=.7, y=.3, b=.4), k(.45, 'plank_under_r', x=1, y=.5, b=-.2, mark='hnng'), k(.7, 'plank_under_r', x=1.1, y=.1, b=-.7, w=.8, mark='HUP'), k(.88, y=.2, eye='O')],
    [(.7, 'tip_hi')], g='use', when=['tilt<.7'], ages=GROWN, obj=[(.45, dict(sway=.3)), (.7, dict(sway=1)), (.88, dict(sway=.3))], say=["Up it goes. Everything I do is a lift. Nobody's grateful.", "Heave. Ho. Heave. Ho. Worth nothing, as usual."])
o.r('rock_it_in_shoves', "Rocking the plank in short wing shoves: down at this end, up at that one", 22, 'wing',
    [k(.15, 'plank_l', reach=.5, w=.4), k(.3, 'plank_l', reach=1, w=.8, y=.4, mark='push'), k(.6, 'plank_r', reach=1, w=.8, y=.4, mark='push'), k(.85, eye='^')],
    [(.3, 'bounce_lo'), (.6, 'bounce_hi')], g='use', prefer=['curious'], obj=[(.3, dict(sway=-.6)), (.6, dict(sway=.6)), (.85, dict(sway=0))])
o.r('shift_weight_on_the_brace', "Leaning on the brace and shifting weight foot to foot until the whole frame creaks", 18, 'wing',
    [k(.2, 'brace_mid', reach=.6, w=.4, x=.3), k(.4, 'brace_mid', reach=.9, w=.7, x=.6, l=1, mark='creak'), k(.6, 'brace_mid', reach=.9, w=.7, x=.6, r=1, mark='creak'), k(.85, eye='-')],
    [(.6, 'creak')], g='use', obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))], say=["It creaks. I creak. We're equals, really.", "That's an old noise. I like old noises."])
o.r('butt_the_leg', "Backing off a step and butting the leg with his rump to see if it nudges the plank", 16, 'none',
    [k(.2, x=-.8, b=.2), k(.4, 'leg_l_mid', x=-1.3, y=.2, b=.3, w=.4, mark='BUMP'), k(.6, x=-.2, y=.6, eye='o'), k(.85, eye='-', x=0)],
    [(.4, 'bounce_lo')], g='use', ages=GROWN, obj=[(.4, dict(shake=.3, sway=-.3)), (.6, dict(sway=.2))])
o.r('lever_the_cradle', "Pushing up into the cradle of the A-frame with his head to lift the plank a hair", 18, 'wing',
    [k(.2, 'cradle', reach=.5, w=.4, x=.5, y=.2), k(.4, 'cradle', reach=.8, w=.8, x=.8, y=-.4, mark='hn'), k(.65, 'hinge_plate', reach=.9, w=.8, x=.6, y=-.4, mark='hn'), k(.85, eye='^')],
    [(.65, 'bounce_hi')], g='use', ages=GROWN, obj=[(.4, dict(sway=.2)), (.65, dict(sway=.4)), (.85, dict(sway=0))])
# --- play
o.r('tunnel_run', "Racing through the A-frame under the plank from one leg to the other, slapping each as he goes", 16, 'none',
    [k(.2, 'leg_l_low', x=.6, y=.3, w=.6, eye='>'), k(.45, x=1.4, y=.3, b=.2, w=1, eye='>', mark='zip'), k(.7, 'leg_r_low', x=.4, y=.2, w=.6, mark='slap'), k(.88, eye='^')],
    [(.7, 'cheer')], g='play', prefer=['happy', 'young'], obj=[(.7, dict(shake=.2))])
o.r('jackhammer_the_base', "Hopping on the base bar with both feet like a very small jackhammer", 14, 'none',
    [k(.2, 'base_l', y=.3, b=.4), k(.35, 'base_l', y=.3, b=-.5, w=.6, mark='tk'), k(.55, 'base_l', y=.3, b=.5, mark='tk'), k(.75, 'base_l', y=.3, b=-.5, w=.6, mark='tk'), k(.9, y=0, eye='^')],
    [(.55, 'rattle')], g='play', prefer=['happy', 'young'], obj=[(.35, dict(shake=.3)), (.55, dict(shake=.5)), (.75, dict(shake=.3))])
o.r('shove_and_sprint_under', "Shoving one end down, then sprinting under the plank to be there when the other end rises", 18, 'none',
    [k(.2, 'plank_under_l', x=.8, y=.2, b=.3), k(.35, 'plank_under_l', x=1, y=.3, b=.4, mark='shove'), k(.55, x=1.6, y=.2, b=-.2, w=1, eye='>'), k(.75, 'plank_under_r', x=.8, y=.3, eye='O', mark='ha')],
    [(.35, 'bounce_lo')], g='play', ages=GROWN, prefer=['happy'], obj=[(.35, dict(sway=-.7)), (.6, dict(sway=0)), (.75, dict(sway=.5))])
o.r('peek_from_the_cradle', "Squeezing in against the brace between the legs with his bill poking out like a periscope", 20, 'none',
    [k(.2, 'brace_low', x=.4, y=.2, b=.3), k(.4, 'brace_low', x=.2, y=-.6, b=.1, eye='o'), k(.65, 'brace_low', x=.2, y=-.9, b=.1, eye='O', mark='...'), k(.85, y=0, eye='^')],
    [(.65, 'cheer')], g='play', ages=YOUNG + ['juvenile'], prefer=['young', 'curious'])
o.r('drum_the_base', "Drumming a beat on the base bar with alternating feet, nodding along", 18, 'none',
    [k(.2, 'base_r', y=.4, b=.3, l=1), k(.35, 'base_r', y=.4, b=.3, r=1, mark='tk'), k(.5, 'base_r', y=.4, b=.3, l=1, mark='tk'), k(.65, 'base_r', y=.4, b=.3, r=1, mark='tk'), k(.85, y=0, eye='^')],
    [(.5, 'rattle')], g='play', obj=[(.35, dict(shake=.2)), (.65, dict(shake=.2))])
o.r('belly_slide_the_base', "Throwing himself down at one end of the base and sliding along it on his belly", 14, 'none',
    [k(.2, 'base_l', x=1, y=.6, b=.5, eye='>'), k(.45, 'base_l', x=1.4, y=1, b=1, w=1, mark='fwoosh'), k(.7, 'base_r', x=1.2, y=1.2, b=1, eye='@'), k(.88, y=.3, b=.3, eye='^')],
    [(.7, 'cheer')], g='play', prefer=['happy', 'young'])
# --- test
o.r('tap_the_leg_and_listen', "Rapping the leg with his bill and standing very still to hear how long it hums", 16, 'none',
    [k(.2, 'leg_l_low', x=.8, y=.5), k(.4, 'leg_l_low', x=1.1, y=.7, mark='tonk'), k(.6, x=-.2, y=.1, eye='o', mark='...'), k(.8, eye='-')],
    [], g='test', prefer=['curious'], obj=[(.4, dict(shake=.2))])
o.r('listen_at_the_brace', "Laying the side of his head on the brace and shoving the frame to hear if it is squeaking", 18, 'none',
    [k(.2, 'brace_low', x=.3, y=.5, b=.3), k(.4, 'brace_low', x=.6, y=.8, b=.5, eye='o', mark='...'), k(.6, 'brace_low', x=.9, y=.8, b=.5, mark='squk'), k(.85, y=.2, eye='-')],
    [], g='test', prefer=['squeak>.2', 'curious'], obj=[(.6, dict(shake=.2))])
o.r('weigh_the_plank', "Lifting one end of the plank a hair on his bill and letting it clunk down to weigh it", 16, 'wing',
    [k(.2, 'plank_under_r', reach=.6, w=.4, y=.2), k(.4, 'plank_under_r', reach=1, w=.8, y=-.4, mark='hn'), k(.6, 'plank_under_r', reach=.2, w=.3, mark='CLUNK'), k(.85, eye='o')],
    [(.6, 'bounce_hi')], g='test', ages=GROWN, prefer=['curious'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=.1, shake=.2))])
o.r('check_the_clearance', "Backing under the plank to find out how little room is left above his head", 18, 'none',
    [k(.2, 'brace_low', x=.4, y=.2), k(.4, 'plank_under_l', x=-.2, y=-.5, b=-.4, eye='o'), k(.65, 'plank_under_l', x=-.3, y=-.5, b=.6, eye='O', mark='hm'), k(.85, y=.2, eye='-')],
    [], g='test', ages=GROWN, prefer=['curious', 'grown'])
o.r('squint_at_the_hinge_pin', "Squinting at the hinge pin to see whether the dark ring around it is rust or just dirt", 18, 'wing',
    [k(.2, 'hinge_pin', reach=.4, w=.3, y=-.6), k(.45, 'hinge_pin', reach=.9, w=.5, x=.8, y=-.3, eye='o'), k(.7, 'hinge_pin', reach=.9, x=.8, y=-.3, eye='O', mark='hm'), k(.88, eye='-')],
    [], g='test', ages=GROWN, prefer=['curious'])
o.r('poke_seat_box_hollow', "Rapping the underside of the seat box with a twig to hear if it is hollow", 20, 'twig',
    [k(.2, 'seat_floor_r', reach=.6, w=.3, y=-.4), k(.4, 'seat_floor_r', reach=1, w=.6, y=-.6, mark='tok'), k(.6, 'seat_floor_r', reach=1, w=.6, y=-.6, mark='tok'), k(.85, eye='-')],
    [(.6, 'rattle')], g='test', ages=GROWN, prefer=['curious'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.2))])
# --- rest
o.r('shade_under_the_plank', "Sitting between the legs in the plank's shadow, back against the brace, eyes shut", 28, 'none',
    [k(.2, 'brace_low', x=-.3, y=.3, b=.4), k(.45, 'brace_low', x=-.5, y=.6, b=.9, eye='-'), k(.75, 'brace_low', x=-.5, y=.6, b=.9, eye='-', mark='ahh'), k(.9, y=.1, eye='^')],
    [(.45, 'shade')], g='rest', when=['sun', 'warm', 'day'], prefer=['tired'])
o.r('storm_huddle_under_plank', "Huddling at the brace's foot with his head tucked until the weather gets bored", 32, 'none',
    [k(.2, 'brace_foot', x=-.3, y=.5, b=.5), k(.4, 'brace_foot', x=-.5, y=1, b=1, eye='-'), k(.7, 'brace_foot', x=-.5, y=1.1, b=1, eye='-', mark='...'), k(.9, y=.3, b=.3, eye='O')],
    [(.4, 'huddle')], g='rest', when=['storm', 'wet'], obj=[(.4, dict(shake=.3)), (.7, dict(shake=.4))])
o.r('doze_against_the_leg', "Dozing with his shoulder wedged against the leg, hearing the plank hum above him", 28, 'none',
    [k(.2, 'leg_r_low', x=-.2, y=.4, b=.5), k(.45, 'leg_r_low', x=-.4, y=.8, b=.9, eye='-'), k(.75, 'leg_r_low', x=-.4, y=.8, b=.9, eye='-', mark='zzz'), k(.9, y=.2, eye='^')],
    [(.45, 'doze')], g='rest', when=['night'], prefer=['tired'])
o.r('sulk_on_the_base', "Sitting on the base bar with his back to the plank, sulking at the ground", 22, 'none',
    [k(.2, 'base_l', x=-.7, y=.5, b=.5), k(.45, 'base_l', x=-.9, y=1, b=.9, eye='-'), k(.75, 'base_l', x=-.9, y=1, b=.9, eye='-', mark='hmph'), k(.9, y=.3, eye='-')],
    [(.45, 'huddle')], g='rest', when=['sad'], say=["Seesaw for two. Cheese for one. Maths isn't my problem.", "Don't look at me. I'm the base now."])
o.r('wait_for_a_partner', "Sitting at the foot of the leg looking at the plank like someone is about to turn up", 26, 'none',
    [k(.2, 'leg_l_low', x=.2, y=.2, b=.5, eye='o'), k(.45, 'leg_l_low', x=.5, y=-.2, b=.6, eye='O'), k(.7, 'leg_l_low', x=.3, y=.5, b=.8, eye='-', mark='...'), k(.9, eye='-')],
    [(.7, 'wait')], g='rest', when=['lonely'], say=["Two seats. One duck. The maths is rude.", "Nobody's coming. I know. I'm waiting out of spite."])
o.r('windbreak_at_the_leg', "Tucking in on the lee side of the leg with his tail to the wind", 24, 'none',
    [k(.2, 'leg_r_mid', x=-.5, y=.3, b=.4), k(.45, 'leg_r_mid', x=-.7, y=.5, b=.8, eye='-'), k(.75, 'leg_r_mid', x=-.7, y=.5, b=.8, eye='-', mark='brr'), k(.9, y=.1, eye='^')],
    [(.45, 'huddle')], g='rest', when=['windy'], obj=[(.45, dict(shake=.2))])
# --- show
o.r('present_to_a_buyer', "Presenting the seesaw to an imaginary buyer with a flourish at each end of the plank", 22, 'wing',
    [k(.2, 'plank_l', reach=1, w=1, x=.3, mark='behold'), k(.45, x=-.3, w=.5, eye='^'), k(.7, 'plank_r', reach=1, w=1, x=.3, mark='and!'), k(.88, w=.4, eye='^')],
    [], g='show', ages=GROWN, prefer=['happy'], say=["Fully functional. Both ends. Previous owner: nobody, so, mint condition.", "Do I sound like a salesman? Good. Buy it."])
o.r('flamingo_on_the_base', "Standing on one foot on the base bar and holding a pose until it wobbles", 18, 'none',
    [k(.2, 'base_l', x=.4, y=.2, b=.2), k(.4, 'base_l', x=.2, y=-.4, l=1, w=.7, eye='^'), k(.65, 'base_l', x=.2, y=-.4, l=1, w=1, eye='O', mark='...'), k(.88, x=.1, eye='-')],
    [], g='show', prefer=['curious', 'happy'])
o.r('tightrope_the_base', "Strutting along the base bar like a tightrope walker, wings out for balance", 18, 'none',
    [k(.15, 'base_l', x=.4, y=.1, w=1, l=1), k(.4, 'base_l', x=.6, y=-.3, w=1, r=1), k(.65, 'base_r', x=.6, y=-.3, w=1, l=1), k(.85, 'base_r', x=.2, w=.6, eye='^', mark='ta-da')],
    [], g='show', prefer=['happy', 'young'])
o.r('argue_with_the_brace', "Squaring up to the brace and lecturing it on who is in charge here", 20, 'wing',
    [k(.2, 'brace_mid', reach=.5, x=.8, eye='>'), k(.4, 'brace_mid', reach=.8, w=.7, x=1.1, y=.4, mark='QUACK'), k(.65, 'brace_mid', reach=.8, w=.5, x=1, eye='>', mark='quack'), k(.85, x=-.3, eye='-', mark='hmph')],
    [], g='show', ages=GROWN, prefer=['grumpy'], say=["I've got three feet of plank and no authority. Welcome to my life.", "The brace started it. It looked at me. Rude."])
o.r('portrait_in_the_cradle', "Standing between the legs with his back to the brace and his chest out like an official portrait", 18, 'none',
    [k(.2, 'leg_r_low', x=.2, y=.2, b=.3), k(.4, 'leg_r_low', x=0, y=-.5, b=0, w=.4, eye='^'), k(.7, 'brace_low', x=0, y=-.6, w=.6, eye='^', mark='cheese'), k(.88, eye='-')],
    [(.7, 'cheer')], g='show', prefer=['happy', 'grown'])
o.r('bow_to_the_plank', "Taking a deep bow to the plank as though it has just won something", 18, 'none',
    [k(.2, 'plank_under_l', x=.6, y=.2), k(.4, x=.2, y=1.4, b=.6, w=.8, mark='ta-da'), k(.65, x=.2, y=1.4, b=.6, w=.8), k(.85, 'plank_under_r', x=.4, y=-.2, eye='^')],
    [(.85, 'cheer')], g='show', ages=GROWN, prefer=['happy', 'grown'])
# --- weather
o.r('wipe_the_plank_dry', "Wiping the damp off the underside of the plank with his tail, left to right", 18, 'none',
    [k(.2, 'plank_under_l', x=-.5, y=.2, b=.5), k(.4, 'plank_under_l', x=-.8, y=.3, b=.5, w=.5, mark='fff'), k(.6, 'plank_under_r', x=-.8, y=.3, b=.5, w=.5, mark='fff'), k(.85, eye='^')],
    [(.6, 'wipe')], g='weather', when=['!wet', 'damp>.2'], ages=GROWN, obj=[(.4, dict(sway=.2)), (.6, dict(sway=-.2))])
o.r('sweep_snow_from_the_leg', "Sweeping the snow banked against the leg out of the way with a wing", 18, 'wing',
    [k(.15, 'leg_l_low', reach=.5, w=.4), k(.4, 'leg_l_low', reach=.9, x=.4, w=.9, mark='fshh'), k(.65, 'base_l', reach=.9, x=.4, w=.9, b=.3, mark='fshh'), k(.85, eye='^')],
    [(.65, 'sweep_snow')], g='weather', when=['snowcap>.3'], prefer=['snow'])
o.r('kick_the_snow_bank', "Kicking the snow drift off the base bar, one foot at a time", 16, 'none',
    [k(.2, 'base_r', y=.2, b=.3, l=1), k(.4, 'base_r', y=.2, b=.3, r=1, mark='pff'), k(.6, 'base_r', y=.2, b=.3, l=1, mark='pff'), k(.85, b=-.3, w=.7, eye='^')],
    [(.6, 'kick_snow')], g='weather', when=['snowcap>.3'], prefer=['happy'], say=["Kicked a snowbank. Felt something. Not sure what. Probably spite.", "Winter's just stationary water. Can still be kicked."])
o.r('stamp_the_puddles', "Stamping through the puddles pooled at the A-frame's foot until they splash the leg", 16, 'none',
    [k(.2, 'base_l', y=.3, l=1), k(.4, 'base_l', y=.3, r=1, mark='splt'), k(.6, 'leg_l_low', y=.2, l=1, mark='SPLT'), k(.82, b=-.3, w=.8, eye='^')],
    [(.6, 'splash')], g='weather', when=['damp>.5', '!wet'], prefer=['happy', 'young'], obj=[(.6, dict(shake=.2))])
o.r('hush_the_wet_hinge', "Leaning his whole weight on the brace until the wet hinge groans quiet", 22, 'none',
    [k(.2, 'brace_low', x=.5, y=.3, b=.4), k(.4, 'brace_low', x=.9, y=.5, b=.6, mark='eeek'), k(.65, 'brace_low', x=.9, y=.5, b=.7, eye='-', mark='...'), k(.85, y=0, eye='^')],
    [(.65, 'hush')], g='weather', when=['squeak>.3', 'damp>.2'], say=["Shut up, hinge. I've got more rust than you and I'm not squeaking.", "Quiet now. Good. Back to being furniture."],
    obj=[(.4, dict(shake=.2)), (.65, dict(shake=0))])
o.r('run_the_rain_off', "Heaving the wet end of the plank upward so the rain slides off it", 20, 'none',
    [k(.2, 'plank_under_r', x=.7, y=.3, b=.4), k(.45, 'plank_under_r', x=1, y=.5, b=-.3, mark='hnng'), k(.7, 'plank_under_r', x=1, y=.2, b=-.6, w=.7, mark='shlk'), k(.88, y=.4, eye='O')],
    [(.7, 'drain')], g='weather', when=['damp>.4', '!wet'], ages=GROWN, obj=[(.45, dict(sway=.3)), (.7, dict(sway=.8, shake=.2)), (.88, dict(sway=.3))])
# --- mishap
o.r('clipped_by_the_drop', "Ducking under the plank just as the far end drops, getting clipped on the head", 16, 'none',
    [k(.2, x=.4, y=.3), k(.4, 'plank_under_l', x=.3, y=-.3, b=-.2, eye='O'), k(.6, 'plank_under_l', x=-.5, y=1.2, b=1, eye='@', mark='CLONK'), k(.85, y=.4, eye='-')],
    [(.6, 'knock')], g='mishap', when=['tilt>.3'], ages=GROWN, say=["OW. Shit. Okay. Zero stars, would touch again.", "Head versus plank. Plank wins. Plank always wins."],
    obj=[(.4, dict(sway=-.4)), (.6, dict(sway=-1, shake=.5))])
o.r('bill_stuck_in_the_brace', "Poking his bill between brace and leg, getting it stuck and hauling out backwards", 22, 'none',
    [k(.2, 'brace_mid', x=.6, y=.5, b=.3), k(.35, 'brace_mid', x=1.2, y=.7, b=.4, mark='tk'), k(.55, 'brace_mid', x=.6, y=.5, b=.7, l=1, eye='>', mark='mmf'), k(.75, 'brace_mid', x=-1, y=.2, b=.9, w=1, eye='@', mark='POP'), k(.9, y=.2, eye='-')],
    [(.55, 'creak')], g='mishap', ages=YOUNG + ['juvenile'], prefer=['young', 'curious'], obj=[(.55, dict(shake=.4))])
o.r('skid_on_the_wet_base', "Skidding on the wet base bar and sliding under the plank on his back", 16, 'none',
    [k(.2, 'base_l', x=.6, y=.5, b=.3), k(.4, 'base_l', x=.2, y=.2, b=-.3, l=1, r=1, eye='O', mark='whoa'), k(.6, 'leg_l_low', x=-1, y=1.2, b=1, eye='@', mark='thump'), k(.85, y=.4, eye='-')],
    [(.6, 'slip')], g='mishap', when=['damp>.4'], obj=[(.6, dict(shake=.4, sway=-.3))], say=["The base is wet. I am now also wet. Fair is fair.", "Slid. Landed. Pretended it was a plan."])
o.r('flipped_by_the_rebound', "Hanging off the plank's end when it flips back and being launched upward", 20, 'none',
    [k(.2, 'plank_under_l', x=.8, y=-.2, b=.3), k(.4, 'plank_under_l', x=.9, y=-.1, b=-.5, l=1, r=1, mark='hnn'), k(.6, 'plank_under_r', x=.9, y=-.3, b=-1, w=1, l=1, r=1, eye='O', mark='WHEE'), k(.85, x=1.2, y=1.3, b=.8, eye='@', mark='thud')],
    [(.6, 'tip_hi')], g='mishap', when=['tilt<.7'], ages=GROWN, prefer=['young', 'grumpy'], say=["Went up. Came down. Sat there. Learned nothing, which is on brand.", "I was airborne. For a second. Most dignified second of my day."],
    obj=[(.4, dict(sway=-.4)), (.6, dict(sway=1, shake=.4)), (.85, dict(sway=-.3))])
o.r('walked_into_the_leg', "Hurrying past in the dark and walking face first into the leg", 14, 'none',
    [k(.2, x=.8, eye='>'), k(.4, 'leg_r_low', x=1.5, y=.6, b=.2, eye='O', mark='BONK'), k(.6, x=-.5, y=.5, b=.5, eye='@'), k(.85, y=.2, eye='-', mark='...')],
    [(.4, 'knock')], g='mishap', when=['night'], prefer=['tired'], obj=[(.4, dict(shake=.3))])
o.r('stuck_under_the_plank', "Squeezing into the gap under the plank for a look and finding he is stuck", 22, 'none',
    [k(.2, 'cradle', x=.6, y=.5, b=.3), k(.4, 'cradle', x=1, y=-.5, b=.8, eye='O', mark='oof'), k(.6, 'cradle', x=1, y=-.5, b=1, l=1, eye='@', mark='...'), k(.8, x=-.8, y=.8, b=.9, w=1, eye='>', mark='POP'), k(.92, y=.3, eye='-')],
    [(.6, 'creak')], g='mishap', ages=GROWN, prefer=['curious', 'grumpy'], say=["Fitted yesterday. Fitted before breakfast. The seesaw has grown.", "Stuck again. Tell nobody. I'm busy."],
    obj=[(.4, dict(shake=.3)), (.6, dict(shake=.5, sway=.2))])
o.emit()

# ============================================================ birdhouse
o = Obj('birdhouse', 'placed',
        fields=dict(damp=(0, 0, 1), leaves=(0, 0, 1), snowcap=(0, 0, 1), web=(.2, 0, 1), sway=(0, 0, 1)),
        physics=[('damp', 'rate', .002, 'wet'), ('damp', 'rate', -.0003, 'dry&warm'),
                 ('leaves', 'rate', .0006, 'fall'), ('leaves', 'rate', -.0008, 'windy'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm'),
                 ('web', 'rate', .0001, 'always'), ('web', 'rate', -.0005, 'wet'),
                 ('sway', 'decay', 0, 'always'), ('sway', 'rate', .02, 'windy')],
        effects=dict(
            wipe_web=[('web', 'set', 0)], scrub=[('obj.dirt', 'add', -.3)], scrape=[('obj.dirt', 'add', -.15)],
            pull_leaves=[('leaves', 'mul', .4), ('obj.dirt', 'add', -.05)], steady=[('sway', 'mul', .3)], mend=[('obj.condition', 'add', .1)],
            plug=[('leaves', 'mul', .5), ('damp', 'mul', .9)], chime=[('sway', 'add', .3), ('need.fun', 'add', 1)], nudge=[('sway', 'add', .3)],
            scratch=[('need.cleanliness', 'add', 1)], air=[('damp', 'mul', .6)], cheer=[('need.fun', 'add', 1)],
            scatter=[('leaves', 'mul', .5), ('need.fun', 'add', 2)], shade=[('need.energy', 'add', 2)],
            huddle=[('need.energy', 'add', 1), ('damp', 'mul', .95)], doze=[('need.energy', 'add', 3)], wait=[('need.social', 'add', 1)],
            wipe=[('damp', 'mul', .3), ('obj.wetness', 'add', -.4)], shake_snow=[('snowcap', 'mul', .2), ('sway', 'add', .3)],
            sweep_snow=[('snowcap', 'set', 0)], splash=[('damp', 'mul', .8), ('obj.wetness', 'add', .2), ('need.fun', 'add', 2)],
            stuck=[('web', 'mul', .5), ('obj.condition', 'add', -.02)], knock=[('obj.condition', 'add', -.05)],
            slip=[('damp', 'mul', .8), ('sway', 'add', .3)], slide=[('snowcap', 'mul', .2), ('sway', 'add', .2)], dump=[('leaves', 'set', 0), ('sway', 'add', .1)]),
        anchors=dict(sill=(.5, .698), base_slab=(.5, .679), floor_bar=(.5, .66), lower_slot=(.54, .604), window_hole=(.47, .528),
                     hole_l_low=(.26, .623), hole_l_high=(.26, .472), hole_r_low=(.69, .623), hole_r_high=(.69, .472),
                     post_l=(.18, .585), spindle_l=(.23, .49), right_rail=(.79, .547),
                     eave_under=(.5, .434), eave_lip=(.5, .415), shingle_low=(.5, .396), shingle_mid=(.5, .302), shingle_high=(.5, .245), crown=(.5, .151)))
# --- care
o.r('sweep_cobwebs', "Sweeping the cobwebs out of each hole with a wing, left hole to right", 20, 'wing',
    [k(.15, 'hole_l_low', reach=.5, w=.4), k(.35, 'hole_l_low', x=.5, w=.8, mark='fff'), k(.55, 'window_hole', x=.5, w=.8, mark='fff'), k(.75, 'hole_r_low', x=.5, w=.8, mark='fff'), k(.9, eye='^')],
    [(.75, 'wipe_web')], g='care', when=['web>.3'], prefer=['curious'], obj=[(.35, dict(shake=.1)), (.55, dict(shake=.1)), (.75, dict(shake=.1))])
o.r('scrub_the_sill', "Scrubbing the dirt off the sill and base slab with a wing", 16, 'wing',
    [k(.15, 'sill', reach=.5, w=.4, y=.5), k(.4, 'sill', x=.4, w=.8, y=.7, mark='skrk'), k(.65, 'base_slab', x=.4, w=.8, y=.5, mark='skrk'), k(.85, eye='^')],
    [(.65, 'scrub')], g='care')
o.r('hook_leaves_from_eave', "Hooking the drifted leaves out from under the eave with a twig", 22, 'twig',
    [k(.15, 'eave_under', reach=.6, w=.3, y=-.3), k(.4, 'eave_under', reach=1, x=.5, y=-.5, w=.7, mark='hk'), k(.6, 'eave_under', reach=1, x=.4, y=-.5, w=.7, mark='fshh'), k(.85, y=.1, eye='^')],
    [(.6, 'pull_leaves')], g='care', when=['leaves>.3'], prefer=['fall', 'grown'], obj=[(.4, dict(shake=.2)), (.6, dict(shake=.1))])
o.r('shove_it_upright', "Shoving the leaning house back upright by its right rail with his shoulder", 18, 'none',
    [k(.2, 'right_rail', x=-.5, y=.3, b=.3), k(.4, 'right_rail', x=1, y=.3, b=.5, mark='hnng'), k(.65, 'right_rail', x=1, y=.2, b=.6, eye='-'), k(.85, x=0, eye='^')],
    [(.65, 'steady')], g='care', when=['sway>.3'], obj=[(.2, dict(sway=-.6)), (.4, dict(sway=.3)), (.65, dict(sway=0))])
o.r('chip_mud_off_the_shingles', "Chipping a dried mud smear off the low shingles with his bill", 18, 'wing',
    [k(.2, 'shingle_low', reach=.6, w=.4, y=-.3), k(.4, 'shingle_low', reach=.9, x=.7, y=-.2, mark='tk'), k(.6, 'shingle_low', reach=.9, x=.7, y=-.2, mark='tk'), k(.85, y=.1, eye='^')],
    [(.6, 'scrape')], g='care', ages=GROWN, obj=[(.4, dict(shake=.1)), (.6, dict(shake=.1))])
o.r('press_the_slat_back', "Pressing the loose lower slat back into its slot with both feet", 16, 'none',
    [k(.2, 'lower_slot', y=.4, b=.4, l=1), k(.4, 'lower_slot', y=.4, b=.4, r=1, mark='thud'), k(.6, 'floor_bar', y=.4, b=.4, l=1, mark='thud'), k(.85, eye='^')],
    [(.6, 'mend')], g='care', obj=[(.4, dict(shake=.1)), (.6, dict(shake=.2))])
# --- use
o.r('landlord_tour', "Taking the landlord's tour: sill, low hole, centre hole, other low hole, nodding at each", 24, 'none',
    [k(.15, 'sill', x=.3, y=.2), k(.35, 'hole_l_low', x=.7, y=.3, eye='o', mark='mm'), k(.55, 'window_hole', x=.7, y=.2, eye='o', mark='hm'), k(.75, 'hole_r_low', x=.7, y=.3, eye='o', mark='mm'), k(.9, eye='^')],
    [], g='use', prefer=['curious', 'grown'], say=["Three holes, no tenants, good light. I'd rent it. Obviously not to birds.", "Inspected. Damp's a bit mean in the corners. Standard."])
o.r('plug_the_draught', "Rolling the loose leaves into the floor gap with a foot to plug the draught", 18, 'none',
    [k(.2, 'floor_bar', y=.4, b=.3, l=1), k(.4, 'floor_bar', y=.6, b=.5, r=1, mark='fsh'), k(.6, 'lower_slot', y=.6, b=.5, l=1, mark='fsh'), k(.85, eye='^')],
    [(.6, 'plug')], g='use', prefer=['leaves>.15'], obj=[(.4, dict(shake=.1))])
o.r('ring_the_eave', "Tapping the underside of the eave with his bill until the whole house chimes faintly", 18, 'wing',
    [k(.2, 'eave_under', reach=.5, w=.5, y=-.4), k(.4, 'eave_under', reach=.9, w=.7, y=-.6, mark='ting'), k(.6, 'eave_under', reach=.9, w=.7, y=-.6, mark='ting'), k(.85, eye='o')],
    [(.6, 'chime')], g='use', prefer=['happy', 'curious'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=.5)), (.85, dict(sway=-.2))])
o.r('rock_the_rail', "Rocking the right rail back and forth with his shoulder to feel the house shift", 16, 'none',
    [k(.2, 'right_rail', x=-.3, b=.3), k(.4, 'right_rail', x=.7, y=.2, b=.5, mark='hnn'), k(.6, 'right_rail', x=-.1, b=.3), k(.8, 'right_rail', x=.7, y=.2, b=.5, mark='hnn'), k(.92, eye='o')],
    [(.8, 'nudge')], g='use', when=['sway<.5'], obj=[(.4, dict(sway=.4)), (.6, dict(sway=-.2)), (.8, dict(sway=.5))])
o.r('fit_the_bill_in', "Fitting his bill into the centre hole as far as it goes to see how deep the room is", 18, 'none',
    [k(.2, 'sill', x=.3, y=.2), k(.45, 'window_hole', x=1.2, y=.1, b=.2, eye='o'), k(.7, 'window_hole', x=1.5, y=.1, b=.2, eye='O', mark='hm'), k(.88, eye='-')],
    [], g='use', prefer=['curious'])
o.r('scratch_on_the_rail', "Rubbing his cheek against the corner of the spindle to scratch an itch", 16, 'none',
    [k(.2, 'spindle_l', x=.3, y=.2), k(.4, 'spindle_l', x=.8, y=.5, mark='mm'), k(.6, 'spindle_l', x=1, y=.5, eye='-', mark='mmm'), k(.85, y=0, eye='^')],
    [(.6, 'scratch')], g='use', ages=GROWN, prefer=['grumpy'], obj=[(.5, dict(shake=.1))])
# --- play
o.r('peekaboo_through_the_holes', "Playing peekaboo: bill in the left hole, then a sprint round, then the centre hole", 20, 'none',
    [k(.2, 'hole_l_low', x=.9, y=.2, eye='o', mark='boo'), k(.4, x=-.3, b=-.3, eye='>'), k(.6, x=-.8, b=-.4, l=1, eye='>'), k(.8, 'window_hole', x=.9, y=.2, eye='O', mark='BOO')],
    [(.8, 'cheer')], g='play', prefer=['happy', 'young'], say=["Boo. Nobody's in. Boo anyway.", "It's a game of one. Winner: me. Loser: also me."])
o.r('knock_and_run', "Knocking on the sill with his bill and bolting before anyone could answer", 14, 'none',
    [k(.2, 'sill', x=.8, y=.7, mark='tok'), k(.4, 'sill', x=1.2, y=.8, mark='TOK'), k(.55, x=-1, b=-.4, w=1, eye='>'), k(.8, x=-1.5, b=-.3, l=1, eye='>', mark='ha')],
    [(.4, 'cheer')], g='play', prefer=['happy', 'young'])
o.r('hop_for_the_high_hole', "Hopping up to peck the rim of the high hole and landing in a heap", 16, 'none',
    [k(.2, x=.3, b=.5), k(.4, 'hole_r_high', x=.8, b=-1, w=1, eye='O', mark='hup'), k(.6, x=-.4, y=1, b=.9, eye='@', mark='thud'), k(.85, y=.3, eye='-')],
    [(.4, 'nudge')], g='play', ages=['juvenile', 'young_adult', 'adult', 'mature', 'legendary'], prefer=['happy'], obj=[(.4, dict(sway=.3)), (.6, dict(sway=-.2))])
o.r('march_the_slab', "Marching the length of the base slab with his bill dragging, from the left post to the right rail", 20, 'none',
    [k(.2, 'post_l', x=.8, y=.4, b=.2), k(.4, 'base_slab', x=1, y=.6, b=.3, l=1, mark='tk'), k(.6, 'base_slab', x=1, y=.6, b=.3, r=1, mark='tk'), k(.85, 'right_rail', x=.5, eye='^')],
    [(.85, 'cheer')], g='play', prefer=['happy'])
o.r('belly_flop_in_the_leaves', "Taking a run up and belly-flopping into the leaves heaped under the sill", 16, 'none',
    [k(.2, x=-.4, b=.4), k(.4, 'sill', x=1.3, y=.8, b=-.4, w=1, mark='hup'), k(.55, 'sill', x=1.3, y=1.3, b=.8, eye='@', mark='fwoomf'), k(.85, y=.4, eye='^')],
    [(.55, 'scatter')], g='play', when=['leaves>.3'], prefer=['happy', 'young'], obj=[(.55, dict(shake=.2))],
    say=["Leaves. Pile of. I'm in it. Mood: soft.", "Do not tell the birdhouse I did that. It's fussy."])
o.r('shout_into_the_hole', "Shouting into the high hole and waiting for it to shout something back", 18, 'none',
    [k(.2, 'hole_l_high', x=.7, y=-.4, b=-.2), k(.4, 'hole_l_high', x=1.3, y=-.5, mark='HELLO'), k(.6, 'hole_l_high', x=1, y=-.5, eye='o', mark='...'), k(.85, y=0, eye='-')],
    [(.4, 'cheer')], g='play', ages=['juvenile', 'young_adult', 'adult', 'mature', 'legendary'], prefer=['lonely'])
# --- test
o.r('listen_at_the_hole', "Laying the side of his head against the low hole and listening for anyone moving", 22, 'none',
    [k(.2, 'hole_r_low', x=.2, y=.5, b=.3), k(.4, 'hole_r_low', x=.4, y=.9, b=.4, eye='o', mark='...'), k(.7, 'hole_r_low', x=.4, y=.9, b=.4, eye='O', mark='...'), k(.88, eye='-')],
    [], g='test', prefer=['curious', 'lonely'], say=["Nothing in there but my own breathing. Which is a lot, actually.", "Quiet. Suspiciously quiet. Probably an ambush."])
o.r('sniff_the_dark', "Sniffing the high hole for what lives in there, and not liking the answer", 16, 'none',
    [k(.2, 'hole_l_high', x=.7, y=.2), k(.4, 'hole_l_high', x=1.2, y=.4, eye='o', mark='snf'), k(.6, 'hole_l_high', x=.8, y=.6, eye='-', mark='snf'), k(.85, x=-.3, eye='-')],
    [], g='test', prefer=['curious'], say=["Smells like pine and tiny feet. Tiny judgemental feet.", "Dust. Old dust. Dust with opinions."])
o.r('tap_the_shingles', "Tapping along the roof shingles with a wing, left edge to right, listening to the tone", 20, 'wing',
    [k(.2, 'shingle_low', reach=.5, w=.4, y=-.4), k(.4, 'shingle_low', reach=.9, w=.6, y=-.5, mark='tk'), k(.6, 'shingle_mid', reach=.9, w=.6, y=-.6, mark='tk'), k(.85, y=0, eye='o')],
    [], g='test', ages=GROWN, prefer=['curious'], obj=[(.4, dict(shake=.1)), (.6, dict(shake=.1))])
o.r('try_the_hole_for_size', "Pushing his head at the low hole to find out whether it fits (it does not)", 18, 'none',
    [k(.2, 'hole_l_low', x=.8, y=.1), k(.4, 'hole_l_low', x=1.3, y=.1, b=.2, eye='O', mark='mm'), k(.6, 'hole_l_low', x=1.6, y=.1, b=.4, eye='>', mark='mmf'), k(.85, x=-.3, y=.4, eye='-')],
    [], g='test', prefer=['curious', 'young'], obj=[(.6, dict(shake=.2))])
o.r('wiggle_the_slat', "Wiggling the loose slat with his bill to find out just how loose it is", 16, 'none',
    [k(.2, 'lower_slot', x=.6, y=.6, b=.3), k(.4, 'lower_slot', x=1, y=.8, b=.4, mark='tk'), k(.6, 'lower_slot', x=1, y=.8, b=.4, w=.3, mark='tk'), k(.85, eye='o')],
    [(.6, 'nudge')], g='test', obj=[(.6, dict(sway=.3, shake=.1))])
o.r('prod_the_ridge', "Prodding the ridge of the roof with a twig to find out whether it is solid", 20, 'twig',
    [k(.2, 'crown', reach=.7, w=.3, y=-.5), k(.45, 'crown', reach=1, x=.4, y=-.7, w=.7, mark='tk'), k(.65, 'shingle_high', reach=1, x=.4, y=-.7, w=.7, mark='tk'), k(.88, y=0, eye='-')],
    [], g='test', ages=GROWN, prefer=['curious', 'grown'], obj=[(.45, dict(shake=.1))])
# --- rest
o.r('shade_by_the_wall', "Sitting with his back to the spindle in the eave's shade, eyes half shut", 28, 'none',
    [k(.2, 'post_l', x=-.3, y=.3, b=.4), k(.45, 'post_l', x=-.5, y=.6, b=.9, eye='-'), k(.75, 'post_l', x=-.5, y=.6, b=.9, eye='-', mark='ahh'), k(.9, y=.1, eye='^')],
    [(.45, 'shade')], g='rest', when=['sun', 'warm', 'day'], prefer=['tired'])
o.r('storm_huddle_by_the_slab', "Huddling against the base slab under the eave, head tucked, until the storm is bored", 32, 'none',
    [k(.2, 'base_slab', x=-.5, y=.5, b=.5), k(.4, 'floor_bar', x=-.7, y=1, b=1, eye='-'), k(.7, 'floor_bar', x=-.7, y=1.1, b=1, eye='-', mark='...'), k(.9, y=.3, b=.3, eye='O')],
    [(.4, 'huddle')], g='rest', when=['storm', 'wet'], obj=[(.4, dict(shake=.3)), (.7, dict(shake=.4))])
o.r('doze_on_the_sill', "Dozing on the sill with his bill under the lowest hole, hearing nothing at all", 28, 'none',
    [k(.2, 'sill', x=.2, y=.4, b=.5), k(.45, 'sill', x=.1, y=.9, b=.9, eye='-'), k(.75, 'sill', x=.1, y=.9, b=.9, eye='-', mark='zzz'), k(.9, y=.2, eye='^')],
    [(.45, 'doze')], g='rest', when=['night'], prefer=['tired'])
o.r('sulk_facing_the_wall', "Turning his face to the wall of the house and sulking at the post", 22, 'none',
    [k(.2, 'spindle_l', x=.6, y=.4, b=.4), k(.45, 'spindle_l', x=.9, y=.8, b=.8, eye='-'), k(.75, 'spindle_l', x=.9, y=.8, b=.8, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [(.45, 'huddle')], g='rest', when=['sad'], say=["Houses for everybody. Except me. I live in a puddle with a lot of principles.", "Fine. Stay in there. I'll keep the wall company."])
o.r('wait_by_the_low_hole', "Sitting by the low hole waiting for a tenant who has not come", 26, 'none',
    [k(.2, 'hole_l_low', x=.2, y=.3, b=.5, eye='o'), k(.45, 'hole_l_low', x=.5, y=-.1, b=.6, eye='O'), k(.7, 'hole_l_low', x=.3, y=.5, b=.8, eye='-', mark='...'), k(.9, eye='-')],
    [(.7, 'wait')], g='rest', when=['lonely'], say=["Nobody in. Nobody out. Roommate goals.", "It's quiet. That's the whole house's personality."])
o.r('lee_of_the_rail', "Tucking in on the lee side of the rail with his tail to the wind and his bill down", 24, 'none',
    [k(.2, 'right_rail', x=-.4, y=.3, b=.4), k(.45, 'right_rail', x=-.7, y=.6, b=.8, eye='-'), k(.75, 'right_rail', x=-.7, y=.6, b=.8, eye='-', mark='brr'), k(.9, y=.1, eye='^')],
    [(.45, 'huddle')], g='rest', when=['windy'], obj=[(.45, dict(shake=.2))])
# --- show
o.r('doorman_bow', "Standing at the sill like a doorman and bowing to each empty low hole in turn", 20, 'none',
    [k(.2, 'hole_l_low', x=.2, y=-.2, b=0), k(.4, 'hole_l_low', x=.2, y=1.2, b=.4, mark='welcome'), k(.6, 'hole_r_low', x=.2, y=-.4, w=.3), k(.8, 'hole_r_low', x=.2, y=1.2, b=.4, mark='welcome'), k(.92, eye='^')],
    [(.8, 'cheer')], g='show', prefer=['happy'], say=["Welcome. Mind the step. Do not bring your friends.", "Fully staffed. By me. Salary: bread."])
o.r('estate_agent_pitch', "Pitching the house to an empty yard with a wing at each high hole in turn", 24, 'wing',
    [k(.2, 'hole_l_high', reach=1, w=1, x=.2, mark='behold'), k(.45, x=-.2, w=.4, eye='^'), k(.7, 'hole_r_high', reach=1, w=1, x=.2, mark='and!'), k(.88, w=.4, eye='^')],
    [], g='show', ages=['juvenile', 'young_adult', 'adult', 'mature', 'legendary'], prefer=['happy', 'grown'], say=["Three bedrooms, no kitchen, no bathroom. Open plan. Don't look up.", "Near a duck. Transport links: wings."])
o.r('stand_by_it_proud', "Standing at the corner post with his chest out like he built every slat of it", 18, 'none',
    [k(.2, 'post_l', x=.2, y=.2, b=.2), k(.4, 'post_l', x=0, y=-.5, w=.4, eye='^'), k(.7, 'post_l', x=0, y=-.6, w=.7, eye='^', mark='ha'), k(.88, eye='-')],
    [(.7, 'cheer')], g='show', prefer=['happy', 'grown'])
o.r('lecture_the_centre_hole', "Squaring up to the centre hole with his bill in the opening and lecturing the dark", 20, 'none',
    [k(.2, 'spindle_l', x=.8, y=.1, eye='>'), k(.4, 'window_hole', x=1.2, y=.2, mark='QUACK'), k(.6, 'window_hole', x=1, y=.1, eye='>', mark='quack'), k(.85, x=-.3, eye='-', mark='hmph')],
    [], g='show', prefer=['grumpy'], say=["I'm not shouting. I'm projecting.", "Nobody's in there. I'm winning the argument."])
o.r('wave_goodbye_to_the_holes', "Waving a wing at the low hole, then stopping, then waving again in case anyone saw", 20, 'wing',
    [k(.2, 'hole_r_low', reach=.8, w=.8, x=.2), k(.4, 'hole_r_low', reach=.3, w=.3, x=-.2), k(.6, 'hole_r_low', reach=.8, w=.8, x=.2, mark='bye'), k(.82, x=-.5, eye='^')],
    [(.6, 'cheer')], g='show', prefer=['lonely', 'happy'])
o.r('survey_the_house', "Pacing the width of the house with one wing out as if it were a blueprint", 24, 'wing',
    [k(.15, 'post_l', reach=.6, w=.6, x=.3), k(.4, 'sill', reach=.8, w=.7, x=.3, mark='mm'), k(.65, 'right_rail', reach=.8, w=.7, x=.3, mark='hm'), k(.85, w=.3, x=0, eye='^')],
    [], g='show', ages=GROWN, prefer=['grown', 'curious'])
# --- weather
o.r('wipe_the_damp_off', "Wiping the damp off the sill and lower slat with his tail feathers", 18, 'none',
    [k(.2, 'sill', x=-.5, y=.2, b=.5), k(.4, 'sill', x=-.8, y=.3, b=.5, w=.5, mark='fff'), k(.6, 'lower_slot', x=-.8, y=.3, b=.5, w=.5, mark='fff'), k(.85, eye='^')],
    [(.6, 'wipe')], g='weather', when=['!wet', 'damp>.2'], ages=GROWN)
o.r('knock_the_snow_off_the_roof', "Knocking the snow off the roof with a twig, ridge to low edge", 22, 'twig',
    [k(.15, 'shingle_mid', reach=.6, w=.3, y=-.5), k(.4, 'shingle_mid', reach=1, x=.4, y=-.7, w=.8, mark='whap'), k(.6, 'shingle_low', reach=1, x=.4, y=-.6, w=.8, mark='fshh'), k(.85, y=.1, eye='^')],
    [(.6, 'shake_snow')], g='weather', when=['snowcap>.3'], ages=GROWN, obj=[(.4, dict(sway=.3)), (.6, dict(sway=.4, shake=.2))])
o.r('brush_snow_off_the_sill', "Brushing the snow off the sill and the lower hole with a wing", 18, 'wing',
    [k(.15, 'sill', reach=.5, w=.4), k(.4, 'sill', reach=.9, x=.4, w=.9, mark='fshh'), k(.65, 'hole_l_low', reach=.9, x=.4, w=.9, mark='fshh'), k(.85, eye='^')],
    [(.65, 'sweep_snow')], g='weather', when=['snowcap>.3'], prefer=['snow'])
o.r('stamp_the_puddle_under', "Stamping in the puddle under the sill until it flies up the slab", 16, 'none',
    [k(.2, 'sill', y=.3, l=1), k(.4, 'sill', y=.3, r=1, mark='splt'), k(.6, 'base_slab', y=.3, l=1, mark='SPLT'), k(.82, b=-.3, w=.8, eye='^')],
    [(.6, 'splash')], g='weather', when=['damp>.5', '!wet'], prefer=['happy', 'young'], obj=[(.6, dict(shake=.2))],
    say=["Puddle's mine. The house can have the dry bit. It's welcome.", "Splash. Splash. Dignity's overrated."])
o.r('air_the_house', "Hooking the wet slat open with his bill to let the damp air out of the house", 20, 'none',
    [k(.2, 'lower_slot', x=.7, y=.5, b=.3), k(.4, 'lower_slot', x=1.2, y=.6, b=.4, mark='hk'), k(.6, 'floor_bar', x=.9, y=.5, b=.4, mark='fff'), k(.85, eye='^')],
    [(.6, 'air')], g='weather', when=['damp>.3', '!wet'], prefer=['sun'], obj=[(.4, dict(shake=.1))])
o.r('hold_it_steady_in_the_gust', "Bracing both feet against the rail to hold the house steady in the gusts", 20, 'none',
    [k(.2, 'base_slab', x=.8, y=.3, b=.5), k(.4, 'right_rail', x=1.1, y=.4, b=.8, eye='>', mark='eek'), k(.65, 'right_rail', x=1.1, y=.4, b=.8, l=1, r=1, eye='@'), k(.85, y=.1, eye='O')],
    [(.4, 'steady')], g='weather', when=['windy', 'sway>.2'], obj=[(.2, dict(sway=.6)), (.4, dict(sway=-.5)), (.65, dict(sway=.2))])
# --- mishap
o.r('head_stuck_in_the_hole', "Jamming his head into the low hole and walking backwards until it comes out with a pop", 22, 'none',
    [k(.2, 'hole_l_low', x=1, y=.2, b=.3), k(.4, 'hole_l_low', x=1.7, y=.2, b=.5, eye='O', mark='mmf'), k(.6, 'hole_l_low', x=1.7, y=.2, b=.8, l=1, eye='@', mark='...'), k(.8, 'hole_l_low', x=-1, y=.4, b=.9, w=1, eye='>', mark='POP'), k(.92, y=.3, eye='-')],
    [(.6, 'stuck')], g='mishap', prefer=['young', 'curious'], say=["Stuck. Not panicking. Just thinking about it. With my arse.", "It was bigger when I looked at it. That's not my fault. That's perspective."], obj=[(.6, dict(shake=.4)), (.8, dict(shake=.3))])
o.r('bonked_by_the_swinging_house', "Leaning in on the rail as the house sways back and getting bonked on the head", 16, 'none',
    [k(.2, x=.4, y=.2, eye='o'), k(.4, 'right_rail', x=.8, y=.5, b=.3, eye='O', mark='oh'), k(.6, 'right_rail', x=-.6, y=1, b=.9, eye='@', mark='BONK'), k(.85, y=.4, eye='-')],
    [(.6, 'knock')], g='mishap', when=['sway>.3'], say=["OW. Shit. Okay. Zero stars, would touch again.", "House hit back. Of course it did."], obj=[(.3, dict(sway=-.6)), (.6, dict(sway=.8, shake=.3))])
o.r('slip_on_the_wet_sill', "Skidding on the wet sill and landing on his chest against the base slab", 16, 'none',
    [k(.2, 'sill', x=.7, y=.5, b=.3), k(.4, 'sill', x=.2, y=.2, b=-.3, l=1, r=1, eye='O', mark='whoa'), k(.6, 'base_slab', x=1.4, y=1.2, b=1, eye='@', mark='splat'), k(.85, y=.4, eye='-')],
    [(.6, 'slip')], g='mishap', when=['damp>.4'], obj=[(.6, dict(sway=.3, shake=.3))])
o.r('snow_slides_off', "Poking the heavy shingles and having the whole snow load slide down on his head", 18, 'wing',
    [k(.2, 'shingle_low', reach=.6, w=.4, y=-.3), k(.4, 'shingle_low', reach=.9, x=.5, y=-.4, mark='tk'), k(.55, 'shingle_low', x=-.2, y=1.2, b=.9, w=.3, eye='@', mark='FWUMP'), k(.8, y=.5, b=.5, eye='-', mark='brr')],
    [(.55, 'slide')], g='mishap', when=['snowcap>.5'], ages=GROWN, obj=[(.55, dict(sway=.4, shake=.5))])
o.r('leaf_dump', "Tugging at a loose slat and getting every leaf in the eave dumped down his neck", 18, 'none',
    [k(.2, 'lower_slot', x=.7, y=.5, b=.4), k(.4, 'lower_slot', x=1.1, y=.6, b=.4, mark='tug'), k(.55, 'floor_bar', x=-.3, y=1.2, b=.9, eye='@', mark='FSHHH'), k(.8, y=.5, b=.5, eye='-')],
    [(.55, 'dump')], g='mishap', when=['leaves>.5'], obj=[(.55, dict(sway=.3, shake=.4))])
o.r('walked_into_the_post', "Hurrying past in the dark and walking face first into the post", 14, 'none',
    [k(.2, x=.8, eye='>'), k(.4, 'post_l', x=1.5, y=.6, b=.2, eye='O', mark='BONK'), k(.6, x=-.5, y=.5, b=.5, eye='@'), k(.85, y=.2, eye='-', mark='...')],
    [(.4, 'knock')], g='mishap', when=['night'], prefer=['tired'], obj=[(.4, dict(shake=.3))])
o.emit()

# ============================================================ rubber_duck
o = Obj('rubber_duck', 'placed',
        fields=dict(squeak=(0, 0, 1), water=(0, 0, 1), bob=(0, 0, 1), snowcap=(0, 0, 1), heat=(0, 0, 1)),
        physics=[('squeak', 'decay', 0, 'always'), ('bob', 'decay', 0, 'always'), ('bob', 'rate', .02, 'windy'),
                 ('water', 'rate', .002, 'wet'), ('water', 'rate', -.0003, 'dry&warm'),
                 ('snowcap', 'rate', .002, 'snow'), ('snowcap', 'rate', -.001, 'warm'),
                 ('heat', 'rate', .002, 'sun'), ('heat', 'rate', -.001, '!sun')],
        effects=dict(
            wipe=[('obj.dirt', 'add', -.3)], scrape=[('obj.dirt', 'add', -.15)], polish=[('obj.dirt', 'add', -.2), ('need.cleanliness', 'add', 1)],
            mend=[('obj.condition', 'add', .1)], squeeze=[('squeak', 'set', 1), ('bob', 'add', .2)], press=[('squeak', 'add', .4), ('need.fun', 'add', 1)],
            hush=[('squeak', 'mul', .3)], push=[('bob', 'set', 1)], steady=[('bob', 'mul', .2)], stir=[('bob', 'add', .2), ('need.fun', 'add', 1)],
            cheer=[('need.fun', 'add', 1)], bump=[('bob', 'add', .4), ('squeak', 'add', .3)], nudge=[('bob', 'add', .3)],
            shade=[('need.energy', 'add', 2)], huddle=[('need.energy', 'add', 1), ('heat', 'mul', .9)], doze=[('need.energy', 'add', 3)],
            hug=[('need.social', 'add', 2), ('heat', 'mul', .95)], warm=[('need.energy', 'add', 2), ('heat', 'mul', .8)],
            shake_out=[('water', 'mul', .3), ('bob', 'add', .5)], blot=[('water', 'mul', .5), ('obj.wetness', 'add', -.4)],
            brush_snow=[('snowcap', 'set', 0)], knock_snow=[('snowcap', 'mul', .2), ('bob', 'add', .3)],
            splash=[('water', 'add', -.1), ('obj.wetness', 'add', .2), ('need.fun', 'add', 2)], slip=[('water', 'mul', .8), ('bob', 'add', .3)],
            bonk=[('bob', 'mul', .5), ('obj.condition', 'add', -.02)], knock=[('obj.condition', 'add', -.05)],
            slide=[('snowcap', 'mul', .2), ('squeak', 'set', .6)]),
        anchors=dict(base_rim=(.51, .838), ripple=(.51, .865), belly_low=(.35, .784), belly_rear=(.235, .757), belly_mid=(.43, .703), belly_r=(.8, .703),
                     flank_l=(.196, .649), tail_tip=(.118, .649), patch=(.39, .568), back_hump=(.27, .486), waterline_l=(.37, .432), breast_r=(.84, .54),
                     neck_back=(.55, .378), head_cheek=(.7, .297), eye_spot=(.745, .243), bill_tip=(.9, .324), crest=(.57, .135)))
# --- care
o.r('dust_the_belly', "Dusting the belly with long wing strokes, left side round to right", 18, 'wing',
    [k(.15, 'belly_mid', reach=.5, w=.4), k(.4, 'belly_mid', x=.4, w=.9, mark='fff'), k(.65, 'belly_r', x=.4, w=.9, mark='fff'), k(.85, eye='^')],
    [(.65, 'wipe')], g='care', obj=[(.4, dict(sway=.1)), (.65, dict(sway=-.1))])
o.r('pick_the_seam_clean', "Picking grime out of the seam under the belly with his bill, working back to the base", 18, 'none',
    [k(.2, 'belly_low', x=.8, y=.7, b=.4), k(.4, 'belly_low', x=1.2, y=.9, b=.5, mark='tk'), k(.6, 'base_rim', x=1.2, y=.9, b=.5, mark='tk'), k(.85, y=0, eye='^')],
    [(.6, 'scrape')], g='care', obj=[(.4, dict(shake=.1)), (.6, dict(shake=.1))])
o.r('buff_the_bill', "Buffing the big rubber bill with his chest feathers until it shines", 18, 'none',
    [k(.2, 'bill_tip', x=-.2, y=-.2, b=.2), k(.4, 'bill_tip', x=-.5, y=-.3, w=.4, mark='squk'), k(.6, 'bill_tip', x=-.7, y=-.3, w=.6, mark='squk'), k(.85, eye='^')],
    [(.6, 'polish')], g='care', ages=GROWN, obj=[(.4, dict(sway=.2)), (.6, dict(sway=-.2))])
o.r('pop_out_the_dent', "Pressing a dent in the cheek back out with his bill until it pops", 16, 'wing',
    [k(.2, 'head_cheek', reach=.5, w=.4, y=-.4), k(.4, 'head_cheek', reach=.9, x=.7, y=-.3, mark='nnh'), k(.6, 'head_cheek', reach=.9, x=.7, y=-.3, w=.7, mark='pop'), k(.85, eye='^')],
    [(.6, 'mend')], g='care', ages=GROWN, obj=[(.6, dict(shake=.2))])
o.r('stamp_the_tail_flat', "Stamping the curled tail back down flat with his foot", 14, 'none',
    [k(.2, 'tail_tip', x=-.4, y=.3, b=.4, l=1), k(.4, 'tail_tip', x=-.4, y=.4, b=.5, l=1, mark='thud'), k(.6, 'flank_l', y=.4, b=.5, r=1, mark='thud'), k(.85, eye='^')],
    [(.6, 'mend')], g='care', obj=[(.4, dict(sway=.1)), (.6, dict(sway=.2))])
o.r('dust_the_crest', "Dusting the crest of the head with a twig, leaning back to see the top", 22, 'twig',
    [k(.2, 'crest', reach=.7, w=.3, y=-.5), k(.4, 'crest', reach=1, x=.3, y=-.7, w=.6, mark='fff'), k(.6, 'head_cheek', reach=1, x=.3, y=-.7, w=.6, mark='fff'), k(.85, y=.1, eye='-')],
    [(.6, 'wipe')], g='care', ages=GROWN, prefer=['grown'])
# --- use
o.r('squeeze_the_belly', "Squeezing the belly between both wings until it gives a long dry squeak", 16, 'wing',
    [k(.2, 'belly_mid', reach=.6, w=.4, b=.2), k(.4, 'belly_mid', reach=1, w=.9, b=.5, mark='squuueak'), k(.6, 'belly_mid', reach=.4, w=.4, b=.1), k(.85, eye='^')],
    [(.4, 'squeeze')], g='use', when=['squeak<.5'], prefer=['happy', 'curious'], obj=[(.4, dict(shake=.3, puff=.2)), (.6, dict(sway=.2))],
    say=["Squeak. Honest noise. Better than most of the things I say.", "I'm fairly sure that's its whole personality."])
o.r('sit_on_the_hump', "Sitting on the duck's back hump so the whole body creaks under him", 20, 'none',
    [k(.2, 'back_hump', x=.3, y=.2, b=.2), k(.4, 'back_hump', x=.1, b=.9, mark='plop'), k(.65, 'back_hump', x=.1, b=.9, w=.3, mark='squk'), k(.85, y=.2, b=.3, eye='^')],
    [(.4, 'press')], g='use', ages=GROWN, prefer=['tired', 'happy'], obj=[(.4, dict(sway=.3)), (.65, dict(sway=-.2, puff=.2))])
o.r('muffle_the_squeak', "Leaning his full weight on the belly until the squeak dies in its throat", 18, 'none',
    [k(.2, 'belly_r', x=.6, y=.3, b=.3), k(.4, 'belly_r', x=1, y=.4, b=.6, mark='squk'), k(.65, 'belly_r', x=1.1, y=.4, b=.7, eye='-', mark='...'), k(.85, y=0, eye='^')],
    [(.65, 'hush')], g='use', when=['squeak>.4'], say=["Quiet. Shh. Quack's a better noise anyway.", "It squeaks. I lean. We both know who wins."])
o.r('rock_it_by_the_flank', "Shoving the flank so it rocks on its base like a weeble and keeps going", 18, 'none',
    [k(.2, 'flank_l', x=-.5, y=.2), k(.4, 'flank_l', x=1, y=.3, b=.4, mark='hup'), k(.6, x=.2, y=.3, eye='o'), k(.8, x=.2, eye='O')],
    [(.4, 'push')], g='use', when=['bob<.2'], prefer=['happy', 'young'], obj=[(.4, dict(sway=.8)), (.6, dict(sway=-.7)), (.8, dict(sway=.5))])
o.r('catch_the_bill_to_stop_it', "Grabbing the rocking duck by the bill to still its bobbing", 16, 'none',
    [k(.2, x=.6, y=-.3, eye='>'), k(.4, 'bill_tip', x=1.2, y=-.2, b=.2, mark='gotcha'), k(.65, 'bill_tip', x=1, y=-.2, b=.4, eye='-'), k(.85, eye='^')],
    [(.4, 'steady')], g='use', when=['bob>.4'], ages=GROWN, obj=[(.2, dict(sway=.8)), (.4, dict(sway=0))])
o.r('stir_the_ripples', "Stirring the ripples around the base with his bill so the duck sets bobbing", 18, 'none',
    [k(.2, 'ripple', x=.6, y=.8, b=.4), k(.4, 'ripple', x=1, y=1.1, b=.5, mark='blp'), k(.6, 'ripple', x=1.2, y=1.1, b=.5, mark='blp'), k(.85, y=.3, eye='^')],
    [(.6, 'stir')], g='use', prefer=['curious'], obj=[(.4, dict(sway=.2)), (.6, dict(sway=.4))], say=["Ripples. Mine. Every one personally authorised.", "It bobs when I tell it to. It's the only one that does."])
# --- play
o.r('race_round_and_slap', "Racing around it and slapping its flank on every lap", 16, 'none',
    [k(.2, 'flank_l', x=.8, w=.8, eye='>'), k(.4, x=1.2, b=-.3, w=1, eye='>'), k(.65, 'belly_r', x=.8, w=.8, mark='slap'), k(.85, x=.5, eye='^')],
    [(.65, 'cheer')], g='play', prefer=['happy', 'young'])
o.r('sumo_bump', "Belly-bumping it like a sumo, backing off and going in again", 16, 'none',
    [k(.2, 'belly_low', x=-.6, y=.2, b=.3), k(.4, 'belly_low', x=1.4, y=.4, b=.4, mark='BUMP'), k(.6, x=-.7, y=.3, b=.2), k(.8, 'belly_low', x=1.4, y=.4, b=.4, mark='BUMP')],
    [(.4, 'bump'), (.8, 'bump')], g='play', prefer=['grumpy', 'happy'], obj=[(.4, dict(sway=.6, shake=.2)), (.8, dict(sway=.8, shake=.3))])
o.r('bounce_off_the_belly', "Leaping at the belly and bouncing off backwards onto his tail", 16, 'none',
    [k(.2, x=-.3, b=.6, eye='>'), k(.4, 'belly_mid', x=1.2, b=-1, w=1, mark='boing'), k(.6, x=-1.6, y=.8, b=.9, w=.5, eye='@', mark='whump'), k(.85, y=.2, eye='^')],
    [(.4, 'press')], g='play', prefer=['happy', 'young'], obj=[(.4, dict(sway=.4, puff=.3)), (.6, dict(sway=-.3))])
o.r('spin_the_tail', "Dragging the tail round until the whole duck is spinning on its base like a top", 20, 'none',
    [k(.2, 'tail_tip', x=.5, y=.5, b=.3), k(.4, 'tail_tip', x=1, y=.7, b=.5, mark='hnn'), k(.6, 'tail_tip', x=1, y=.7, b=.5, w=.7, eye='@'), k(.85, x=.2, eye='O')],
    [(.4, 'nudge')], g='play', prefer=['curious', 'young'], obj=[(.4, dict(sway=.5)), (.6, dict(sway=-.6)), (.85, dict(sway=.3))], say=["Round it goes. Nobody's seasick. Not yet.", "I spun a duck. Put that on my tombstone."])
o.r('hide_behind_the_duck', "Ducking behind the duck's back, watching round its breast, then jumping out", 20, 'none',
    [k(.2, 'belly_rear', x=-.3, y=.3, b=.4, eye='o'), k(.4, 'belly_rear', x=-.3, y=.3, b=.5, eye='o'), k(.65, 'breast_r', x=.6, y=.2, eye='O', mark='BOO'), k(.85, eye='^')],
    [(.65, 'cheer')], g='play', prefer=['happy', 'young'])
o.r('stomp_the_ripples', "Counting out a rhythm by stamping at the ripples around its base", 18, 'none',
    [k(.2, 'base_rim', y=.3, l=1), k(.4, 'base_rim', y=.3, r=1, mark='tk'), k(.6, 'base_rim', y=.3, l=1, mark='tk'), k(.85, eye='^')],
    [(.6, 'cheer')], g='play', obj=[(.4, dict(sway=.1)), (.6, dict(sway=.2))])
# --- test
o.r('find_where_the_squeak_lives', "Squeezing along the belly a little at a time to find which spot the squeak lives in", 24, 'wing',
    [k(.15, 'belly_rear', reach=.5, w=.4), k(.35, 'belly_low', reach=.8, w=.6, mark='...'), k(.55, 'belly_mid', reach=.8, w=.6, mark='...'), k(.75, 'belly_r', reach=.9, w=.8, eye='O', mark='squk'), k(.9, eye='o')],
    [], g='test', prefer=['curious'], obj=[(.75, dict(puff=.3))])
o.r('rap_the_head', "Rapping the cheek with his bill to find out whether the head is hollow", 14, 'none',
    [k(.2, 'head_cheek', x=.8, y=-.2, b=.2), k(.4, 'head_cheek', x=1.1, y=-.1, mark='tok'), k(.6, 'head_cheek', x=.8, y=-.2, mark='tok'), k(.82, eye='o')],
    [], g='test', ages=GROWN, prefer=['curious'])
o.r('sniff_the_patch', "Sniffing the patch on its side to find out what the smell of bath is made of", 16, 'wing',
    [k(.2, 'patch', reach=.4, x=.5, y=.2), k(.45, 'patch', reach=.6, x=1, y=.4, eye='o', mark='snf'), k(.65, 'patch', reach=.6, x=1, y=.4, eye='O', mark='snf'), k(.85, eye='-')],
    [], g='test', prefer=['curious'], say=["Rubber. Bleach. Regret. Someone's childhood.", "Smells like a bathroom. Not mine. I use the pond."])
o.r('weigh_it_at_the_base', "Pressing his shoulder against the base to learn how heavy the duck really is", 16, 'none',
    [k(.2, 'base_rim', x=-.4, y=.3, b=.4), k(.4, 'base_rim', x=1, y=.4, b=.6, mark='hnng'), k(.6, 'base_rim', x=1.1, y=.4, b=.7, eye='>'), k(.85, eye='-')],
    [(.4, 'nudge')], g='test', obj=[(.4, dict(sway=.2)), (.6, dict(sway=0))])
o.r('tug_the_tail', "Tugging the tail to see whether it comes off (it does not)", 16, 'none',
    [k(.2, 'tail_tip', x=.5, y=.3, b=.3), k(.4, 'tail_tip', x=.2, y=.5, b=.6, w=.4, mark='hnn'), k(.6, 'tail_tip', x=-.8, y=.5, b=.8, w=.6, mark='hnnng'), k(.8, eye='-')],
    [], g='test', obj=[(.5, dict(shake=.2))])
o.r('stare_into_the_eye', "Staring into the eye from a hand's width away to see who blinks first", 20, 'wing',
    [k(.2, 'eye_spot', reach=.4, x=.6, eye='o'), k(.45, 'eye_spot', reach=.6, x=1, eye='O', mark='...'), k(.7, 'eye_spot', reach=.6, x=1, eye='O', mark='...'), k(.88, x=0, eye='-')],
    [], g='test', ages=GROWN, prefer=['curious', 'grumpy'])
# --- rest
o.r('shade_at_the_flank', "Sitting against its warm flank in the shadow it casts, eyes shut", 28, 'none',
    [k(.2, 'belly_rear', x=-.3, y=.3, b=.4), k(.45, 'belly_rear', x=-.5, y=.6, b=.9, eye='-'), k(.75, 'belly_rear', x=-.5, y=.6, b=.9, eye='-', mark='ahh'), k(.9, y=.1, eye='^')],
    [(.45, 'shade')], g='rest', when=['sun', 'warm', 'day'], prefer=['tired'])
o.r('storm_huddle_at_the_base', "Huddling against the base under its belly, bill down, until the storm moves on", 32, 'none',
    [k(.2, 'belly_low', x=-.4, y=.5, b=.5), k(.4, 'base_rim', x=-.6, y=1, b=1, eye='-'), k(.7, 'base_rim', x=-.6, y=1.1, b=1, eye='-', mark='...'), k(.9, y=.3, b=.3, eye='O')],
    [(.4, 'huddle')], g='rest', when=['storm', 'wet'], obj=[(.4, dict(shake=.3)), (.7, dict(shake=.4))])
o.r('doze_on_the_belly', "Dozing with his head laid on the low curve of the belly, rising and falling with the air", 30, 'none',
    [k(.2, 'belly_mid', x=.4, y=.5, b=.5), k(.45, 'belly_mid', x=.3, y=.9, b=.9, eye='-'), k(.75, 'belly_mid', x=.3, y=.9, b=.9, eye='-', mark='zzz'), k(.9, y=.2, eye='^')],
    [(.45, 'doze')], g='rest', when=['night'], prefer=['tired'])
o.r('sulk_at_the_tail', "Turning his back on the duck and sulking at its tail", 22, 'none',
    [k(.2, 'tail_tip', x=-.6, y=.5, b=.4), k(.45, 'tail_tip', x=-.9, y=.8, b=.8, eye='-'), k(.75, 'tail_tip', x=-.9, y=.8, b=.8, eye='-', mark='hmph'), k(.9, y=.2, eye='-')],
    [(.45, 'huddle')], g='rest', when=['sad'], say=["It's got a smile painted on. Must be nice. Mine's real effort.", "Don't squeak at me. I'm not in the mood to be agreed with."])
o.r('hug_the_duck', "Wrapping both wings round its belly and holding on, cheek against the rubber", 24, 'wing',
    [k(.2, 'belly_r', reach=.5, w=.6, x=.4), k(.45, 'belly_r', reach=1, w=1, x=.8, y=.4, eye='-'), k(.7, 'belly_r', reach=1, w=1, x=.8, y=.4, eye='-', mark='mm'), k(.9, w=.4, eye='^')],
    [(.45, 'hug')], g='rest', when=['lonely'], say=["It squeaks when you hold it. That's the nicest thing anyone's said to me today.", "Don't tell anyone. I'm hugging a toy. It's fine. It's research."])
o.r('bask_against_the_warm_rubber', "Pressing his chest to the sun-warmed rubber until the chill goes out of his feathers", 24, 'none',
    [k(.2, 'belly_mid', x=.2, y=.3, b=.4), k(.45, 'belly_mid', x=.4, y=.5, b=.8, eye='-'), k(.75, 'belly_mid', x=.4, y=.5, b=.8, eye='-', mark='ahh'), k(.9, y=0, eye='^')],
    [(.45, 'warm')], g='rest', when=['heat>.4'], prefer=['cold', 'tired'])
# --- show
o.r('compare_profiles', "Standing bill to bill with the duck, comparing profiles from the same angle", 20, 'none',
    [k(.2, 'bill_tip', x=1, y=-.2), k(.4, 'bill_tip', x=1.2, y=-.3, w=.3, eye='o'), k(.65, 'bill_tip', x=1.4, y=-.3, w=.6, eye='-', mark='hm'), k(.85, x=0, y=0, eye='^')],
    [(.65, 'cheer')], g='show', ages=GROWN, prefer=['happy'], say=["Same beak. Same colour. Mine moves. Edge: me.", "Pretty sure we're related. On the paint side."])
o.r('claim_to_be_the_real_one', "Lecturing the duck's neck, squared up, that he is the real duck here and it is a toy", 22, 'none',
    [k(.2, 'neck_back', x=.8, y=-.2, eye='>'), k(.4, 'neck_back', x=1.2, y=-.1, mark='QUACK'), k(.6, 'neck_back', x=1, y=-.1, eye='>', mark='quack'), k(.85, x=-.3, eye='-', mark='hmph')],
    [], g='show', ages=GROWN, prefer=['grumpy'], say=["I'm the real one. You can tell because I get tired and have opinions.", "It squeaked at me. Rude. First person to disagree all week."])
o.r('squeak_duet', "Squeezing out a belly note and quacking back at it, then again, a higher one", 22, 'wing',
    [k(.15, 'belly_mid', reach=.6, w=.5), k(.3, 'belly_mid', reach=1, w=.9, b=.4, mark='squk'), k(.5, y=-.4, x=.3, eye='^', mark='QUACK'), k(.7, 'belly_low', reach=1, w=.9, b=.4, mark='SQUK'), k(.88, eye='^', x=.2)],
    [(.3, 'press'), (.7, 'press')], g='show', when=['squeak<.8'], prefer=['happy'], obj=[(.3, dict(puff=.3)), (.7, dict(puff=.4, sway=.2))])
o.r('present_it_to_the_yard', "Presenting the duck to the yard with a wing sweep from its tail up to its head", 22, 'wing',
    [k(.15, 'tail_tip', reach=1, w=.8, x=.2, mark='behold'), k(.4, 'back_hump', reach=1, w=1, x=.3), k(.65, 'head_cheek', reach=1, w=1, x=.3, y=-.3, mark='the duck'), k(.88, w=.4, eye='^')],
    [], g='show', ages=GROWN, prefer=['happy', 'grown'])
o.r('critic_walk_round', "Walking round the duck with one eye shut like an art critic judging its proportions", 24, 'none',
    [k(.15, 'tail_tip', x=.3, y=.2, eye='o'), k(.4, 'flank_l', x=.5, y=-.2, eye='-'), k(.65, 'belly_low', x=.5, y=.2, eye='o', mark='hm'), k(.85, 'belly_r', x=.3, eye='-', mark='mm')],
    [], g='show', prefer=['curious', 'grown'], say=["Too round. Too yellow. Too confident. Four stars.", "Excellent bill. Dreadful arse. Critics will talk."])
o.r('bow_to_the_duck', "Bowing low to the duck at the water's edge as if it were royalty", 20, 'none',
    [k(.2, 'ripple', x=.3, y=.2), k(.4, 'ripple', x=.2, y=1.3, b=.5, mark='your grace'), k(.65, 'ripple', x=.2, y=1.3, b=.5), k(.85, 'base_rim', x=.3, y=-.2, eye='^')],
    [(.85, 'cheer')], g='show', prefer=['happy'])
# --- weather
o.r('shake_the_water_out', "Tipping the duck on its tail and shaking the trapped rainwater out of its seam", 22, 'none',
    [k(.2, 'tail_tip', x=-.6, y=.3, b=.4), k(.4, 'tail_tip', x=-1, y=.5, b=.8, mark='hnng'), k(.6, 'belly_rear', x=-1, y=.4, b=.6, w=.6, mark='glug'), k(.85, x=-.2, eye='^')],
    [(.6, 'shake_out')], g='weather', when=['water>.4', '!wet'], ages=GROWN, obj=[(.4, dict(sway=.7)), (.6, dict(sway=-.6, shake=.3)), (.8, dict(sway=0))])
o.r('blot_the_belly_dry', "Blotting the rain off the belly with a wing, from the seam up", 16, 'wing',
    [k(.15, 'belly_low', reach=.5, w=.4), k(.4, 'belly_low', reach=.8, x=.4, w=.8, mark='fff'), k(.65, 'belly_mid', reach=.9, x=.4, w=.8, mark='fff'), k(.85, eye='^')],
    [(.65, 'blot')], g='weather', when=['!wet', 'water>.15'])
o.r('brush_snow_off_the_cheek', "Brushing the snow off its head and cheek with a wing", 18, 'wing',
    [k(.15, 'head_cheek', reach=.5, w=.4, y=-.3), k(.4, 'head_cheek', reach=.9, x=.4, w=.9, y=-.3, mark='fshh'), k(.65, 'neck_back', reach=.9, x=.4, w=.9, mark='fshh'), k(.85, eye='^')],
    [(.65, 'brush_snow')], g='weather', when=['snowcap>.3'], ages=GROWN, prefer=['snow'])
o.r('knock_the_snow_cap_off', "Knocking the snow cap off its crest with a twig, topmost bit first", 20, 'twig',
    [k(.15, 'crest', reach=.6, w=.3, y=-.5), k(.4, 'crest', reach=1, x=.4, y=-.7, w=.8, mark='whap'), k(.6, 'crest', reach=1, x=.4, y=-.7, w=.8, mark='fshh'), k(.85, y=.1, eye='^')],
    [(.6, 'knock_snow')], g='weather', when=['snowcap>.4'], ages=GROWN, obj=[(.4, dict(sway=.3)), (.6, dict(sway=.3, shake=.2))])
o.r('stamp_the_puddle_round_it', "Stamping through the puddle that has formed round its base, kicking spray at the belly", 16, 'none',
    [k(.2, 'ripple', y=.3, l=1), k(.4, 'ripple', y=.3, r=1, mark='splt'), k(.6, 'belly_low', y=.3, l=1, mark='SPLT'), k(.82, b=-.3, w=.8, eye='^')],
    [(.6, 'splash')], g='weather', when=['water>.5', '!wet'], prefer=['happy', 'young'], obj=[(.6, dict(shake=.2))],
    say=["Puddle. Mine. The duck can float there if it wants.", "Wet feet. Dry principles."])
o.r('hold_it_in_the_gust', "Bracing against the flank with both feet to stop a gust knocking the duck over", 20, 'none',
    [k(.2, 'flank_l', x=.8, y=.3, b=.5), k(.4, 'flank_l', x=1.1, y=.4, b=.8, eye='>', mark='eek'), k(.65, 'flank_l', x=1.1, y=.4, b=.8, l=1, r=1, eye='@'), k(.85, y=.1, eye='O')],
    [(.4, 'steady')], g='weather', when=['windy', 'bob>.2'], obj=[(.2, dict(sway=.7)), (.4, dict(sway=-.6)), (.65, dict(sway=.3))])
# --- mishap
o.r('squeak_blast', "Squeezing too hard and getting the whole squeak in the face from a hand's width away", 16, 'none',
    [k(.2, 'belly_mid', x=.7, y=.5, b=.3), k(.4, 'belly_mid', x=1.2, y=.6, b=.6, eye='O', mark='SQUEEEAK'), k(.6, x=-1.2, y=.2, b=.4, w=1, eye='@', mark='...'), k(.85, y=.1, eye='-')],
    [(.4, 'squeeze')], g='mishap', when=['squeak<.5'], prefer=['curious'], obj=[(.4, dict(shake=.5, puff=.5))],
    say=["That was a lot of squeak. I now hear in ducks.", "OW. Shit. Okay. Zero stars, would touch again."])
o.r('knocked_by_the_rock_back', "Giving it a big shove, then taking its rock back square in the chest", 16, 'none',
    [k(.2, 'flank_l', x=-.4, y=.2), k(.4, 'flank_l', x=1.2, y=.2, b=.4, mark='HUP'), k(.6, 'flank_l', x=-1.6, y=.8, b=1, eye='@', mark='oof'), k(.85, y=.3, eye='-')],
    [(.6, 'bonk')], g='mishap', when=['bob>.5'], obj=[(.3, dict(sway=-.5)), (.6, dict(sway=.9, shake=.3))])
o.r('slip_in_the_puddle', "Skidding in the puddle round the base and sliding beneath the duck on his back", 16, 'none',
    [k(.2, 'ripple', x=.6, y=.5, b=.3), k(.4, 'ripple', x=.2, y=.2, b=-.3, l=1, r=1, eye='O', mark='whoa'), k(.6, 'base_rim', x=-1, y=1.2, b=1, eye='@', mark='splat'), k(.85, y=.4, eye='-')],
    [(.6, 'slip')], g='mishap', when=['water>.4'], obj=[(.6, dict(shake=.4, sway=.3))])
o.r('squeaked_in_the_ear', "Pecking at the big bill and being squeaked at from right beside his ear", 14, 'none',
    [k(.2, 'bill_tip', x=.8, y=-.3), k(.4, 'bill_tip', x=1.3, y=-.2, mark='tk'), k(.55, 'bill_tip', x=-.5, y=.4, b=.5, eye='@', mark='SQUK'), k(.85, y=.1, eye='-', mark='...')],
    [(.55, 'squeeze')], g='mishap', ages=GROWN, say=["It squeaked into my ear. Now I hear squeaks. Everywhere. I'm doing a squeak.", "Never again. Until Thursday."],
    obj=[(.55, dict(shake=.3, puff=.3))])
o.r('snow_slides_off_its_head', "Pushing at the neck as the snow slides off the head and lands on him in a lump", 18, 'wing',
    [k(.2, 'neck_back', reach=.6, w=.4), k(.4, 'neck_back', reach=.9, x=.6, mark='hup'), k(.55, 'neck_back', x=-.3, y=1.2, b=.9, w=.3, eye='@', mark='FWUMP'), k(.8, y=.5, b=.5, eye='-', mark='brr')],
    [(.55, 'slide')], g='mishap', when=['snowcap>.5'], ages=GROWN, obj=[(.55, dict(sway=.3, shake=.4))])
o.r('walked_into_it_in_the_dark', "Hurrying past in the dark and walking face first into its breast", 14, 'none',
    [k(.2, x=.8, eye='>'), k(.4, 'breast_r', x=1.5, y=.6, b=.2, eye='O', mark='BONK'), k(.6, x=-.5, y=.5, b=.5, eye='@', mark='squk'), k(.85, y=.2, eye='-', mark='...')],
    [(.4, 'knock')], g='mishap', when=['night'], prefer=['tired'], obj=[(.4, dict(shake=.3, puff=.2))])
o.emit()
