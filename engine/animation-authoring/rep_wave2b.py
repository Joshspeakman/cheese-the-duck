"""Wave 2b: rainbow_slide, toy_slide, water_slide, water_slide_mega, toy_trampoline, trampoline. Every routine is hand-written.
Anchors are (column, row) of each drawing (rep.py <id>), converted to fractions by pm(). Riding and exploring are native: these are the other acts."""
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

DIM = dict(rainbow_slide=(110, 75), toy_slide=(100, 71), water_slide=(108, 74), water_slide_mega=(116, 81), toy_trampoline=(88, 50), trampoline=(74, 39))


def pm(oid):
    w, rows = DIM[oid]
    return lambda c, r, *fl: (round(c / (w - 1), 4), round(r / rows, 4), *([' '.join(fl)] if fl else []))


def toy_slide():
    # Drawing (100 x 72 cells, 7.7 px a row, standing line row 68): a scaffold tower on the left, cols 8-28: two rails (cols 8, 11) with rung pairs `==`
    # at rows 66 61 56 51 46 (15, 54, 92, 131, 169 px), deck boards `=====` cols 12-24 on the same rows, a second rail pair cols 25-28, bolt heads `o`
    # (col 12 and col 24, rows 58 48), a zig-zag stair `/` `\` between the decks; the chute is a three-lane plastic run (`|||`) coming down to the right,
    # cols 78-95, with a bolt at its foot (col 87, row 66), a hollow apron `___` (row 67, 8 px) and the chute's end row 68.
    P = pm('toy_slide')
    o = Obj('toy_slide', 'placed',
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), heat=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('heat', 'rate', .0012, 'sun'), ('heat', 'rate', -.0008, 'night')],
            effects=dict(scrub=[('obj.dirt', 'add', -.25)], sweep=[('obj.dirt', 'add', -.15)], wipe=[('obj.wetness', 'add', -.3)], tighten=[('obj.condition', 'add', .2)], clunk=[('obj.condition', 'add', -.15)], smear=[('obj.dirt', 'add', .12)],
                         chip=[('frost', 'mul', .2)], shove=[('drift', 'set', 0)], fan=[('heat', 'mul', .4)],
                         laugh=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(post_l=P(8, 68), rung_lo=P(9, 66, 'surface'), rail_l=P(8, 63), rung_mid=P(9, 61, 'surface'), bolt_l=P(12, 58), deck_lo=P(16, 66, 'surface'),
                         deck_lo2=P(22, 66, 'surface'), deck_two=P(18, 61, 'surface'), post_r=P(27, 68), rung_r=P(26, 66), bolt_r=P(24, 58),
                         apron_l=P(80, 67, 'surface'), apron_r=P(92, 67, 'surface'), foot_bolt=P(87, 66), lane_a=P(85, 64, 'surface'), lane_b=P(90, 65),
                         lane_c=P(86, 61, 'surface'), lip_edge=P(78, 62), lane_d=P(80, 59)))
    # ---------------- care
    o.r('scrub_lanes', 'Scrubbing the chute lanes clean at their foot with a wing', 20, 'wing',
        [k(.12, 'lane_a', reach=.6, x=.4, y=.8, b=.2), k(.3, 'lane_a', reach=1, x=.7, y=1, b=.6, l=1, mark='skrk'), k(.5, 'lane_b', reach=1, x=.8, y=1.1, b=.7, r=1, mark='skrk'),
         k(.7, 'lane_c', reach=1, x=.6, y=.8, b=.3, l=1), k(.9, eye='^')],
        [(.5, 'scrub')], g='care', act=('scrub', 'lanes'), when=['obj_dirt>.3'], prefer=['grown'],
        say=["Lanes clean. Wing grey. Worth it.", "Scrubbed a slide I never ride. Look at me."])
    o.r('wipe_rail', 'Wiping the ladder rail dry end to end with a wing', 18, 'wing',
        [k(.12, 'rail_l', reach=.5, x=.3, y=.4), k(.3, 'rail_l', reach=1, x=.5, y=.2, b=-.4, w=0, mark='fwip'), k(.5, 'rung_mid', reach=1, x=.5, y=.2, b=-.6, r=1),
         k(.7, 'rail_l', reach=1, x=.6, y=.5, b=.2, l=1), k(.9, eye='-')],
        [(.5, 'wipe')], g='care', act=('wipe', 'rail'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.15))],
        say=["Dry rail. Nobody say thanks, it's creepy.", "Wiped it twice. The rail stayed rude."])
    o.r('sweep_apron', 'Sweeping grit off the landing apron with a wing', 16, 'wing',
        [k(.1, 'apron_l', reach=.5, x=.6, y=1, b=.5), k(.3, 'apron_l', reach=1, x=.9, y=1.3, b=.8, l=1), k(.5, 'apron_r', reach=1, x=.9, y=1.3, b=.8, r=1, mark='fff'),
         k(.75, 'apron_r', reach=.6, x=.4, y=.8, b=.3), k(.9, eye='^')],
        [(.5, 'sweep')], g='care', act=('sweep', 'apron'), when=['obj_dirt>.3'])
    o.r('snug_foot_bolt', 'Twisting the loose bolt at the chute foot snug with his bill', 18, 'none',
        [k(.1, x=.5, y=.7), k(.25, 'foot_bolt', x=1.1, y=1.6, b=.8, mark='nnk'), k(.42, 'foot_bolt', x=1.2, y=1.8, b=1, l=1), k(.6, 'foot_bolt', x=1.3, y=1.9, b=1.1, r=1, mark='NNK'),
         k(.8, x=.3, y=.4, w=.5, eye='>'), k(.92, eye='^')],
        [(.6, 'tighten')], g='care', act=('mend', 'bolt'), when=['obj_condition<.6'],
        say=["Bolt is snug. Don't ask where the spanner went.", "Fixed it with my face again."])
    o.r('chip_lane_ice', 'Chipping frost off the middle lane with a twig', 22, 'twig',
        [k(.12, 'lane_c', reach=.6, x=.4), k(.3, 'lane_c', reach=1, x=.7, y=.5, b=.3, mark='tk'), k(.48, 'lane_d', reach=1, x=.8, y=.5, b=.5, r=1, mark='tk'),
         k(.66, 'lane_c', reach=1, x=.9, y=.6, b=.6, l=1, mark='tk'), k(.85, eye='^')],
        [(.66, 'chip')], g='weather', act=('chip', 'lane'), when=['frost>.3'])
    o.r('shove_drift_off', 'Shovelling a snow drift off the apron with his breast', 20, 'none',
        [k(.1, 'apron_l', x=.4, y=.8, b=.3), k(.3, 'apron_l', x=.8, y=1.5, b=.9, l=1, mark='fsh'), k(.55, 'apron_r', x=1.1, y=1.8, b=1.2, r=1, mark='FSH'),
         k(.8, x=.2, y=.6, b=.2, w=.6), k(.92, eye='^')],
        [(.55, 'shove')], g='weather', act=('push', 'drift'), when=['drift>.3'],
        say=["Snow gone. Hands are cold. I have no hands.", "Shoved the drift off. Chest is a plough now."])
    # ---------------- use / test
    o.r('count_rungs', 'Counting the ladder rungs with a tap of the bill each, losing count at the second', 24, 'none',
        [k(.1, 'rung_lo', x=.6, y=.8, b=.3, mark='1'), k(.28, 'rung_lo', x=.9, y=1.5, b=.8, mark='tk'), k(.44, 'rung_mid', x=1.1, y=-.6, b=-.5, mark='tk'),
         k(.6, 'rung_r', x=.4, y=.9, b=.4, eye='-', mark='3?'), k(.8, 'rung_lo', x=.6, y=1.2, b=.6, mark='1'), k(.92, eye='>')],
        [], g='test', act=('count', 'rungs'), prefer=['curious'],
        say=["Four. Five. Four again. Rungs are cheating.", "Counted them all. The answer is rungs."])
    o.r('flap_up_first_deck', 'Flapping up onto the first deck and looking down at the apron', 20, 'none',
        [k(.12, 'deck_lo', x=.3, y=.5, b=.5), k(.3, 'deck_lo', perch=1, x=.5, y=-.3, b=-1, w=1, l=1, mark='hup'), k(.5, 'deck_lo', perch=1, x=.8, y=.6, b=.1, eye='o'),
         k(.7, 'deck_lo2', perch=1, x=.3, y=.4, b=-.2, w=.4), k(.9, x=.4, y=.8, b=.6, eye='^')],
        [], g='use', act=('climb', 'deck'), prefer=['young'])
    o.r('walk_the_deck_boards', 'Walking the first deck board to board, wings out like it is a wire', 22, 'wing',
        [k(.1, 'deck_lo', perch=1, reach=.8, x=.2, b=-.2), k(.3, 'deck_lo', perch=1, reach=1, x=.2, y=.2, b=.3, l=1), k(.5, 'deck_lo2', perch=1, reach=1, x=.2, y=.2, b=.4, r=1),
         k(.7, 'deck_lo2', perch=1, reach=.6, x=.1, b=-.4, l=1, eye='-'), k(.9, 'deck_lo2', perch=1, reach=.2, x=.4, y=.5, b=.2)],
        [], g='play', act=('balance', 'deck'), prefer=['curious'])
    o.r('drum_the_lanes', 'Drumming the three lanes in turn, the hollow plastic booming', 20, 'none',
        [k(.1, 'lane_a', x=.7, y=.8, b=.3), k(.25, 'lane_a', x=1.1, y=1.5, b=.9, mark='dok'), k(.4, 'lane_b', x=1.1, y=1.5, b=.9, l=1, mark='dok'), k(.55, 'lane_c', x=1.1, y=1.4, b=1, r=1, mark='DOK'),
         k(.75, 'lane_b', x=1.2, y=1.6, b=1, mark='dok'), k(.9, eye='^')],
        [(.55, 'laugh')], g='play', act=('drum', 'lanes'), prefer=['happy'],
        say=["Plastic boom. Three lanes, one rhythm. Mine.", "Hollow slide, hollow head. Good acoustics."])
    o.r('chase_the_post', 'Chasing his own tail around the ladder post and the far post', 22, 'none',
        [k(.1, 'post_l', x=.5, y=.5, b=.2), k(.25, 'post_l', x=1.3, y=1.2, b=.8, l=1, w=1), k(.42, 'post_r', x=-.5, y=1, b=.4, r=1, w=1), k(.6, 'post_l', x=1.3, y=1.3, b=.9, l=1),
         k(.8, 'post_r', x=-.6, y=1.1, b=.5, r=1, eye='@'), k(.92, x=.2, y=.4, b=.1, eye='-')],
        [(.6, 'laugh')], g='play', act=('chase', 'post'), prefer=['grumpy'],
        say=["The tail is winning. The tail has always won.", "Dizzy. Worth it. Mostly dizzy."])
    o.r('lean_on_ladder_post', 'Leaning back against the ladder post with his wings folded', 24, 'none',
        [k(.15, 'post_l', x=-.3, b=-.3), k(.35, 'post_l', x=-1, y=-.8, b=-.9, l=1), k(.6, 'post_l', x=-1.3, y=-.5, b=.8, eye='-'), k(.82, 'post_l', x=-1.2, y=-.8, b=-1.2, r=1, eye='-', mark='hm'), k(.94, eye='^')],
        [(.6, 'rest')], g='rest', act=('lean', 'post'))
    o.r('nap_on_apron', 'Napping flat on the landing apron, bill to the sun-warmed lip', 36, 'none',
        [k(.12, 'apron_r', perch=1, x=.3, b=.6), k(.3, 'apron_r', perch=1, x=.6, y=.9, b=1.4, eye='-'), k(.6, 'apron_r', perch=1, x=.6, y=1, b=1.5, eye='-', mark='zzz'), k(.85, 'apron_r', perch=1, x=.4, y=.5, b=.8, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'apron'), prefer=['tired'], when=['day'],
        say=["Apron. Sun. Nobody on the chute. Perfect.", "Woke up with a plastic grid on my cheek."])
    o.r('sulk_at_the_rung', 'Sulking at the lowest rung, bill resting on it', 24, 'none',
        [k(.15, 'rung_lo', x=.5, y=.6, b=.3), k(.4, 'rung_lo', x=.8, y=1.2, b=.8, eye='-'), k(.7, 'rung_lo', x=.8, y=1.3, b=.9, eye='-', mark='hmph'), k(.9, x=.2, y=.4, b=.2, eye='^')],
        [], g='rest', act=('sulk', 'rung'), prefer=['grumpy', 'sad'],
        say=["Rung. Fine. You win. Again.", "Sulking. Rung is not even listening."])
    o.r('slip_on_wet_apron', 'Skating across the wet apron on two flat feet and ending in a skid', 18, 'none',
        [k(.12, 'apron_l', perch=1, x=.2, b=.2), k(.3, 'apron_l', perch=1, x=.5, b=-.4, w=1, l=1, r=1, mark='eep'), k(.5, 'apron_r', perch=1, x=1.2, y=1.2, b=1.4, w=1, eye='O', mark='WHEE'),
         k(.8, 'apron_r', perch=1, x=.4, y=1, b=.9, eye='@')],
        [(.5, 'smear')], g='mishap', act=('slip', 'apron'), when=['obj_wetness>.3'],
        say=["Wet apron. Dry dignity. Pick one.", "Slid the full length. Zero stars."])
    o.r('jam_bill_in_seam', 'Wedging his bill into the lane seam at the foot and yanking it out with a pop', 22, 'none',
        [k(.12, x=.6, y=.6), k(.3, 'lane_a', x=1.2, y=1.2, b=.8, mark='oof'), k(.5, 'lane_a', x=1.3, y=1.3, b=1, l=1, eye='O', mark='...'), k(.7, 'lane_a', x=1.4, y=1.2, b=1.1, r=1, w=1, mark='POP'),
         k(.88, x=1.9, y=1, b=.5, eye='@')],
        [(.7, 'smear')], g='mishap', act=('stuck', 'seam'), shown='head', prefer=['young'])
    o.r('crack_head_on_rung', 'Straightening up too fast and cracking his skull against a rung', 18, 'none',
        [k(.1, 'rung_mid', x=.6, y=1, b=.8), k(.28, 'rung_mid', x=.6, y=1.4, b=1.3, l=1), k(.42, 'rung_mid', x=.8, y=-1.4, b=-1.2, w=1, eye='O', mark='TONK'), k(.62, x=-.7, y=1.5, b=1, w=1, r=1, eye='@'), k(.88, x=.2, y=.5, b=.3, eye='>')],
        [(.42, 'clunk')], g='mishap', act=('knock', 'rung'),
        say=["Rung hit first. I demand a rematch.", "Skull one, rung one. Rung bruise-free."])
    o.r('pose_on_the_apron_lip', 'Posing on the apron lip, one wing up, like it is a podium', 18, 'none',
        [k(.15, 'apron_l', perch=1, x=.3, b=-.2), k(.4, 'apron_l', perch=1, x=.2, y=-.5, b=-.6, w=1, l=1), k(.7, 'apron_r', perch=1, x=.1, y=-.7, b=-.5, w=1, r=1, eye='^'), k(.9, 'apron_r', perch=1, x=.3, b=-.1, w=.3)],
        [], g='show', act=('pose', 'lip'), prefer=['happy'])
    o.r('sing_down_the_chute', 'Calling hello into the lane mouth and waiting for an echo that mocks him', 24, 'none',
        [k(.12, 'lane_a', x=.7, y=.5, b=.3), k(.3, 'lane_a', x=1.2, y=.2, b=.4, w=.6, mark='HELLO'), k(.5, 'lane_a', x=1.0, y=.3, b=.2, eye='o', mark='...'), k(.7, 'lane_a', x=.9, y=.4, b=.3, w=.3, eye='>', mark='ello'), k(.9, eye='-')],
        [], g='show', act=('sing', 'chute'), shown='head', prefer=['lonely'],
        say=["Echo said hello back. Rude tone.", "Chute is the only one who answers me."])
    o.r('bow_to_the_ladder', 'Bowing to the ladder after an unasked-for show', 16, 'none',
        [k(.15, 'post_l', x=-.4, y=-.8, b=-.8, w=.6), k(.4, 'post_l', x=1.2, y=1.8, b=1.3, w=1, l=1, mark='ta-da'), k(.65, 'post_l', x=1, y=2.4, b=1.6, w=1, r=1), k(.88, 'post_l', x=.2, y=-.3, b=-.3, w=0, eye='^')],
        [], g='show', act=('bow', 'ladder'))
    o.r('hot_foot_lane', 'Tapping a sun-hot lane with one foot and hopping off with a squeak', 18, 'none',
        [k(.15, 'lane_b', x=.5, y=1, b=.5), k(.32, 'lane_b', x=.8, y=1.4, b=.8, l=1, mark='tsk'), k(.5, 'lane_b', x=.4, y=-.2, b=-.8, l=1, r=1, w=1, eye='O', mark='YIP'), k(.78, x=-.5, y=.3, b=.2, w=.6, eye='>')],
        [], g='weather', act=('test', 'lane'), when=['heat>.3'], prefer=['curious'],
        say=["Hot. Plastic hot. Nature does this to spite me.", "Foot is fine. Pride is toast."])
    o.r('fan_the_hot_lane', 'Fanning the sun-hot lane with a big flap of his wing', 20, 'wing',
        [k(.12, 'lane_c', reach=.5, x=.3, y=.8), k(.3, 'lane_c', reach=1, x=.5, y=.5, b=-.2, mark='fwoo'), k(.5, 'lane_d', reach=.4, x=.5, y=.5, b=-.4, r=1, mark='fwoo'),
         k(.7, 'lane_c', reach=1, x=.6, y=.5, b=-.2, l=1, mark='fwoo'), k(.9, eye='-')],
        [(.5, 'fan')], g='weather', act=('blow', 'lane'), when=['heat>.4'])
    # ---------------- v3 top-up: tricks down the lower chute (perch along its lane anchors), the ladder, more upkeep and rest
    o.r('roll_down_the_lower_chute', 'Rolling down the lower chute like a log with his wings tucked, ending in a heap on the apron', 20, 'none',
        [k(.12, 'lane_c', perch=1, x=.3, b=.8, w=0), k(.3, 'lane_c', perch=1, x=.5, y=1.2, b=1.8, eye='-'), k(.5, 'lane_a', perch=1, x=.6, y=1.5, b=2, l=1, r=1, eye='@', mark='brrrm'), k(.72, 'apron_l', perch=1, x=1, y=1.8, b=1.5, eye='O'), k(.9, 'apron_l', perch=1, x=.3, y=.6, b=.5, eye='^')],
        [], g='use', act=('roll', 'chute'), prefer=['happy'], say=["Rolled. Landed. Opinions: dizzy.", "Chute gave me a free lap of the room."])
    o.r('headfirst_down_the_chute', 'Going down the lower chute headfirst, neck out flat and wings swept back', 20, 'none',
        [k(.12, 'lane_c', perch=1, x=.4, y=.5, b=.4), k(.3, 'lane_c', perch=1, x=1.7, y=1.8, b=1.2, w=1, eye='>', mark='ZZZT'), k(.5, 'lane_a', perch=1, x=2, y=2.2, b=1.4, w=1, eye='>'), k(.72, 'apron_r', perch=1, x=2.2, y=2.4, b=1.6, w=1, eye='O', mark='BAM'), k(.9, 'apron_r', perch=1, x=.4, y=.8, b=.5, eye='@')],
        [], g='use', act=('race', 'lane'), prefer=['young', 'happy'])
    o.r('backwards_down_the_chute', 'Going down the chute backwards on his tail, feet kicking up at the sky', 22, 'none',
        [k(.12, 'lane_c', perch=1, x=-.5, y=-.4, b=-.5), k(.3, 'lane_c', perch=1, x=-1.4, y=-1.2, b=-1, l=1, r=1, eye='o', mark='eek'), k(.52, 'lane_a', perch=1, x=-1.8, y=-1.4, b=-1.3, l=1, r=1, w=1), k(.74, 'apron_l', perch=1, x=-1.2, y=.6, b=1, eye='@'), k(.92, 'apron_l', perch=1, x=.2, b=.2, eye='-')],
        [], g='use', act=('drag', 'lane'), prefer=['grown'])
    o.r('brake_halfway_down', 'Braking halfway down the chute with both feet flat against the lane, skidding to a squeaky stop', 20, 'none',
        [k(.12, 'lane_c', perch=1, x=.3, b=.5), k(.3, 'lane_a', perch=1, x=.6, y=.3, b=-.8, l=1, r=1, w=.6, mark='SKREE'), k(.52, 'lane_a', perch=1, x=-.8, y=-.4, b=-1.2, l=1, r=1, w=1, eye='O'), k(.72, 'lane_a', perch=1, x=.4, y=.8, b=.9, eye='-', mark='phew'), k(.9, 'apron_l', perch=1, x=.2, b=.2, eye='^')],
        [], g='use', act=('brace', 'lane'),
        say=["Brakes held. Feet smoking. Pride intact.", "Stopped halfway. Called it a strategy."])
    o.r('spin_down_the_chute_flat', 'Spinning flat down the lower chute like a dropped plate, one wing out as a rudder', 22, 'wing',
        [k(.12, 'lane_c', perch=1, reach=.3, x=.2, b=.3), k(.3, 'lane_c', perch=1, reach=1, x=.5, y=.9, b=1.2, l=1), k(.5, 'lane_a', perch=1, reach=1, x=-.6, y=1.2, b=1.4, r=1), k(.7, 'apron_r', perch=1, reach=1, x=.8, y=1.6, b=1.1, l=1, eye='@'), k(.9, 'apron_r', perch=1, reach=.2, x=.2, b=.2, eye='-')],
        [], g='use', act=('spin', 'chute'), prefer=['curious'])
    o.r('climb_the_ladder_rungs', 'Climbing the ladder rung by rung with a wing hooked ahead of him, then hopping off', 26, 'wing',
        [k(.1, 'rung_lo', perch=1, reach=.3, x=.3, b=.4), k(.28, 'rung_lo', perch=1, reach=1, x=.5, y=-.4, b=-.5, l=1, mark='hup'), k(.46, 'rung_mid', perch=1, reach=1, x=.5, y=-.7, b=-.8, r=1), k(.64, 'deck_two', perch=1, reach=.6, x=.3, y=.4, b=.3, eye='o'), k(.84, 'rung_lo', perch=1, reach=.2, x=.2, b=.5, w=0, eye='^')],
        [], g='use', act=('climb', 'rungs'), ages=GROWN, prefer=['young'])
    o.r('polish_the_foot_bolt', 'Rubbing the chute foot bolt shiny with a wing, breath-fogging it first', 18, 'wing',
        [k(.12, 'foot_bolt', reach=.4, x=.5, y=.9, b=.3), k(.3, 'foot_bolt', reach=1, x=.9, y=1.2, b=.9, mark='hah'), k(.5, 'foot_bolt', reach=1, x=.8, y=1.1, b=.8, l=1, mark='rub'), k(.7, 'foot_bolt', reach=1, x=.8, y=1.2, b=.9, r=1, mark='rub'), k(.9, eye='^')],
        [(.5, 'scrub')], g='care', act=('polish', 'bolt'), when=['obj_dirt>.4'])
    o.r('pat_the_lanes_dry', 'Patting the wet lanes dry with the pad of his breast, working up from the apron', 22, 'none',
        [k(.1, 'apron_l', x=.3, y=.6, b=.4), k(.28, 'lane_a', x=.5, y=1, b=1.2, mark='pff'), k(.46, 'lane_b', x=.5, y=1, b=1.3, w=.4, mark='pff'), k(.66, 'lane_c', x=.6, y=-.4, b=-.5, w=.6), k(.86, x=.1, eye='-')],
        [(.46, 'wipe')], g='care', act=('dry', 'lanes'), when=['obj_wetness>.4'])
    o.r('scrape_frost_from_the_apron', 'Scraping a frost skin off the apron with the side of a foot', 20, 'none',
        [k(.1, 'apron_l', perch=1, x=.2, y=.4, b=.5), k(.28, 'apron_l', perch=1, x=.5, y=.7, b=.9, l=1, mark='zzk'), k(.5, 'apron_r', perch=1, x=.5, y=.7, b=.9, r=1, mark='zzk'), k(.7, 'apron_r', perch=1, x=.3, y=.4, b=.5, l=1, eye='^')],
        [(.5, 'chip')], g='weather', act=('scrape', 'apron'), when=['frost>.4'])
    o.r('hunker_by_the_post', 'Hunkering by the ladder foot with his neck in, waiting out the wind', 30, 'none',
        [k(.15, 'post_r', x=-.4, y=.5, b=.8), k(.4, 'post_r', x=-.9, y=1.2, b=1.3, w=.6, eye='-'), k(.7, 'post_r', x=-1, y=1.3, b=1.4, w=.7, eye='-', mark='brr'), k(.9, 'post_r', x=-.3, y=.4, b=.5, eye='^')],
        [], g='rest', act=('shelter', 'post'), when=['windy'])
    o.r('sit_on_the_apron_lip', 'Sitting on the apron with his feet stuck out in front, bill on his chest', 28, 'none',
        [k(.15, 'apron_r', perch=1, x=.3, b=.5), k(.38, 'apron_r', perch=1, x=.2, y=.6, b=1.1, l=1, r=1, eye='o'), k(.64, 'apron_l', perch=1, x=.2, y=.7, b=1.2, eye='-', mark='hm'), k(.88, 'apron_l', perch=1, x=.3, y=.2, b=.4, eye='^')],
        [], g='rest', act=('sit', 'apron'), prefer=['tired'])
    o.r('wait_at_the_ladder_foot', 'Waiting at the ladder foot eyeing the apron in case somebody queues', 26, 'none',
        [k(.12, 'post_l', x=.2, y=-.5, b=-.3), k(.34, 'rung_lo', x=.4, y=-1, b=-.8, eye='o', mark='...'), k(.58, 'post_l', x=.2, y=.9, b=.6, l=1, eye='-'), k(.8, 'rung_lo', x=.3, y=-1.1, b=-.9, r=1, eye='o'), k(.94, eye='>')],
        [], g='rest', act=('wait', 'ladder'), prefer=['lonely'])
    o.r('listen_to_the_post_hum', 'Pressing an ear-hole to the far post to hear the chute tick when the wind is up', 22, 'none',
        [k(.12, 'post_r', x=.3, y=.3, b=.2), k(.3, 'post_r', x=1, y=-.6, b=-.9, eye='o'), k(.52, 'post_r', x=1.2, y=-1, b=-1.2, eye='-', mark='tick'), k(.74, 'post_r', x=.8, y=.6, b=.3, eye='O', mark='...'), k(.9, eye='>')],
        [], g='test', act=('listen', 'post'), when=['windy'], prefer=['curious'])
    o.r('pace_out_the_apron', 'Pacing out the apron with deliberate steps, counting steps and arguing about the total', 24, 'wing',
        [k(.1, 'apron_l', perch=1, reach=.5, x=.2, b=.2, l=1), k(.3, 'apron_l', perch=1, reach=1, x=.4, y=.3, b=.1, r=1, mark='7'), k(.5, 'apron_r', perch=1, reach=1, x=.4, y=.3, b=.1, l=1, mark='8'), k(.7, 'apron_r', perch=1, reach=.6, x=.2, y=.5, b=.3, r=1, eye='@', mark='9?'), k(.9, 'apron_r', perch=1, reach=.1, eye='-')],
        [], g='test', act=('measure', 'apron'))
    o.r('tap_the_high_bolt', 'Tapping the ladder bolt with his bill and listening for what is loose', 20, 'wing',
        [k(.12, 'bolt_r', reach=.6, x=.4, y=-.2, b=-.2), k(.3, 'bolt_r', reach=1, x=.9, y=-.5, b=-.4, mark='tk'), k(.5, 'bolt_l', reach=1, x=.9, y=-.5, b=-.5, l=1, mark='tk'), k(.7, 'bolt_r', reach=1, x=.5, y=-.2, b=-.2, eye='o'), k(.9, eye='-')],
        [], g='test', act=('tap', 'bolt'), prefer=['curious'])
    o.r('sniff_the_lane', 'Sniffing along the lane for old crumbs, bill following the seam to the foot', 20, 'none',
        [k(.1, 'lane_c', x=.3, y=-.8, b=-.6), k(.3, 'lane_d', x=1, y=.9, b=.9, mark='snf'), k(.5, 'lane_c', x=1.3, y=1.4, b=1.4, mark='snf'), k(.7, 'lane_a', x=1.5, y=1.9, b=1.8, eye='o', mark='snf'), k(.9, eye='>')],
        [], g='test', act=('sniff', 'lane'), prefer=['curious'])
    o.r('weigh_the_low_rung', 'Stepping on the lowest rung with one foot, then the other, to see if it holds him', 22, 'none',
        [k(.1, 'rung_lo', perch=1, x=.3, b=.3, l=1), k(.3, 'rung_lo', perch=1, x=.5, y=.6, b=.8, l=1, r=1, mark='creak'), k(.5, 'rung_lo', perch=1, x=.2, y=1, b=1.2, eye='o'), k(.7, 'rung_lo', perch=1, x=.4, y=.4, b=.2, eye='^'), k(.9, 'rung_lo', perch=1, x=.2, b=.2)],
        [], g='test', act=('weigh', 'rung'), prefer=['grown'])
    o.r('peer_up_the_chute', 'Craning his neck to peer up the chute from the apron, one eye closed', 22, 'none',
        [k(.12, 'apron_l', x=.1, y=-.4, b=-.4), k(.32, 'lane_a', x=.4, y=-1.3, b=-1.2, w=.4, eye='o'), k(.52, 'lane_a', x=.6, y=-1.5, b=-1.5, w=.6, eye='O', l=1), k(.74, 'apron_l', x=.1, y=.3, b=.2, eye='-'), k(.9, eye='>')],
        [], g='test', act=('peer', 'chute'))
    o.r('hop_the_apron_squares', 'Hopscotching between the two apron ends, one foot, two feet, one foot', 20, 'none',
        [k(.1, 'apron_l', perch=1, x=.3, b=-.6, l=1), k(.28, 'apron_l', perch=1, x=.4, b=-1.2, l=1, r=1, w=.4), k(.48, 'apron_r', perch=1, x=.4, b=-.6, r=1), k(.68, 'apron_r', perch=1, x=.4, b=-1.3, l=1, r=1, w=.6, mark='hup'), k(.88, 'apron_r', perch=1, x=.2, b=.2, eye='^')],
        [], g='play', act=('hop', 'apron'), prefer=['young', 'happy'])
    o.r('kick_grit_off_the_apron', 'Kicking apron grit into a spray of little dust puffs with alternate feet', 18, 'none',
        [k(.12, 'apron_l', x=.3, y=.5, b=.3), k(.3, 'apron_l', x=.6, y=.9, b=.9, l=1, mark='tsh'), k(.5, 'apron_r', x=.6, y=.9, b=.9, r=1, mark='tsh'), k(.7, 'apron_r', x=.5, y=.7, b=.6, l=1, eye='>'), k(.9, eye='^')],
        [(.5, 'sweep')], g='play', act=('kick', 'grit'), when=['obj_dirt>.3'])
    o.r('tug_the_rail_back', 'Tugging at the ladder rail with a hooked wing in a one-sided tug of war', 22, 'wing',
        [k(.1, 'rail_l', reach=.4, x=-.2, b=-.2), k(.28, 'rail_l', reach=1, x=-.8, y=-.3, b=-.8, w=0, mark='hnn'), k(.46, 'rail_l', reach=1, x=-1.1, y=-.2, b=-1.1, l=1, mark='HNN'), k(.64, 'rail_l', reach=.4, x=.8, y=.8, b=1.2, r=1, eye='@', mark='pop'), k(.86, eye='-')],
        [], g='play', act=('tug', 'rail'), obj=[(.3, dict(shake=.2)), (.5, dict(shake=.4))], prefer=['grumpy'])
    o.r('kick_the_ladder_post', 'Kicking the ladder post for no reason and hopping off on one foot', 18, 'none',
        [k(.12, 'post_l', x=.3, y=.4, b=.3), k(.3, 'post_l', x=.5, y=.7, b=-.4, l=1, mark='tok'), k(.46, 'post_l', x=-.3, y=-.5, b=-1.4, l=1, w=1, eye='O', mark='OW'), k(.66, x=-.8, y=1, b=.4, r=1, eye='@'), k(.88, eye='>')],
        [(.46, 'clunk')], g='mishap', act=('kick', 'post'), prefer=['grumpy'])
    o.r('catch_a_wing_on_the_bolt', 'Catching a wing against the ladder bolt and flapping until it lets go', 22, 'wing',
        [k(.12, 'bolt_l', reach=.5, x=.2, y=-.2), k(.3, 'bolt_l', reach=1, x=.4, y=-.5, b=-.3, mark='hm'), k(.5, 'bolt_l', reach=1, x=-.5, y=-.8, b=-.9, l=1, r=1, eye='O', mark='MPH'), k(.7, 'bolt_l', reach=1, x=-.8, y=-1, b=-1.3, eye='@', mark='POP'), k(.9, x=.2, eye='-')],
        [], g='mishap', act=('hook', 'bolt'), ages=GROWN)
    o.r('tumble_off_the_apron_end', 'Tumbling off the end of the apron in a flapping somersault and getting up cross', 20, 'none',
        [k(.12, 'apron_r', perch=1, x=.3, b=.2), k(.3, 'apron_r', perch=1, x=1.1, y=1, b=-1, w=1, mark='whoa'), k(.5, 'apron_r', perch=1, x=-1.2, y=-1.5, b=1.8, w=1, l=1, r=1, eye='O', mark='THUMP'), k(.72, 'apron_r', perch=1, x=.8, y=1.5, b=1.2, eye='@'), k(.9, 'apron_r', perch=1, x=.2, b=.3, eye='>')],
        [(.5, 'smear')], g='mishap', act=('fold', 'apron'),
        say=["Landing scored a four. By me.", "Tumble. Thud. Sue the apron."])
    o.r('dance_on_the_apron', 'Dancing a clumsy shuffle across the apron with his wings out like a signpost', 24, 'none',
        [k(.1, 'apron_l', perch=1, x=.2, b=.3, l=1), k(.3, 'apron_l', perch=1, x=.2, y=-.3, b=-.5, r=1, w=1), k(.5, 'apron_r', perch=1, x=.2, y=-.3, b=.6, l=1, w=.5), k(.7, 'apron_r', perch=1, x=.1, y=-.6, b=-.6, r=1, l=1, w=1, eye='^'), k(.9, 'apron_r', perch=1, x=.2, b=.1, w=0)],
        [], g='show', act=('dance', 'apron'), prefer=['happy'])
    o.r('present_the_slide', 'Presenting the whole chute with a long flourish of the wing, like he built it himself', 24, 'wing',
        [k(.1, 'apron_l', perch=1, reach=.2, x=.1, y=-.3), k(.34, 'lane_a', reach=1, x=.1, y=-.7, b=-.4, mark='behold'), k(.58, 'lane_c', reach=1, x=.1, y=-1, b=-.8, l=1), k(.82, 'lip_edge', reach=.6, x=.2, y=-.4, eye='^')],
        [], g='show', act=('present', 'slide'), prefer=['happy'], say=["Slide. Mine now. Public access by invitation.", "Showed it to the lawn. Lawn nodded."])
    o.r('argue_with_the_bolt', 'Arguing with the foot bolt, wing jabbing at its head while it says nothing', 20, 'wing',
        [k(.12, 'foot_bolt', reach=.5, x=.3, y=.4), k(.3, 'foot_bolt', reach=1, x=.8, y=-.2, b=.3, mark='YOU'), k(.5, 'foot_bolt', reach=1, x=.9, y=-.4, b=.5, r=1, mark='YOU'), k(.7, 'foot_bolt', reach=.6, x=.4, y=.8, b=.9, l=1, eye='>'), k(.9, eye='-')],
        [], g='show', act=('argue', 'bolt'), prefer=['grumpy'])
    o.emit()


def rainbow_slide():
    # Drawing (110 x 76 cells, 7.9 px a row, standing line row 72): the same scaffold tower as the toy slide, cols 8-28, but taller (rung/deck rows every
    # 5 rows from row 71: 8, 48, 87, 127 px); chute on the right, cols 86-102, with three lanes `|||` `||` `||`, a bolt at its foot (col 97, row 70),
    # a wide apron `_________________` cols 88-104 at row 71 (8 px), and the chute's lowest rim on row 72. Its nature: the painted rainbow one.
    P = pm('rainbow_slide')
    o = Obj('rainbow_slide', 'placed',
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), shine=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('shine', 'rate', .004, 'rainbow_sky'), ('shine', 'rate', -.0005, 'always')],
            effects=dict(polish=[('obj.dirt', 'add', -.3)], brush=[('obj.dirt', 'add', -.15)], pat=[('obj.wetness', 'add', -.25)], tighten=[('obj.condition', 'add', .2)],
                         thud=[('obj.condition', 'add', -.15)], scuff=[('obj.dirt', 'add', .12)], chip=[('frost', 'mul', .25)], plough=[('drift', 'mul', .2)],
                         bask=[('shine', 'add', -.3), ('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], laugh=[('need.fun', 'add', 2)]),
            anchors=dict(post_l=P(8, 72), rung_lo=P(10, 71, 'surface'), rail_l=P(8, 67), rung_mid=P(12, 66, 'surface'), deck_lo=P(17, 71, 'surface'), deck_lo2=P(24, 71, 'surface'),
                         deck_two=P(17, 66, 'surface'), post_r=P(28, 72), rung_r=P(26, 71), apron_l=P(90, 71, 'surface'), apron_r=P(103, 71, 'surface'),
                         foot_bolt=P(97, 70), lane_a=P(94, 69, 'surface'), lane_b=P(100, 69), lane_c=P(93, 66, 'surface'), lane_d=P(97, 63), lip_edge=P(86, 66)))
    # ---------------- care
    o.r('polish_the_lanes', 'Polishing the painted lanes at the foot until the colours show', 22, 'wing',
        [k(.1, 'lane_a', reach=.5, x=.5, y=.6, b=.1), k(.28, 'lane_a', reach=1, x=.9, y=1.2, b=.5, r=1, mark='sqk'), k(.46, 'lane_b', reach=1, x=.9, y=1.2, b=.5, l=1, mark='sqk'),
         k(.64, 'lane_c', reach=1, x=.5, y=.6, b=-.2, r=1, mark='sqk'), k(.84, 'lane_b', reach=.4, x=.3, y=.4, eye='^')],
        [(.64, 'polish')], g='care', act=('polish', 'lanes'), when=['obj_dirt>.3'], prefer=['happy'],
        say=["Shiny. Now the colours look at me back.", "Polished it. Streaks stay. So do I."])
    o.r('pat_the_foot_dry', 'Patting the wet chute foot dry with his breast, wing over wing', 20, 'none',
        [k(.1, 'apron_l', x=.3, y=.6, b=.2), k(.28, 'lane_a', x=.7, y=1.3, b=1, mark='pff'), k(.46, 'lane_b', x=.7, y=1.3, b=1.1, w=.4, mark='pff'), k(.66, 'apron_r', x=.5, y=1.1, b=.9, w=.8, r=1), k(.88, x=.1, b=-.2, eye='-')],
        [(.46, 'pat')], g='care', act=('dry', 'foot'), when=['obj_wetness>.3'])
    o.r('brush_the_rungs', 'Brushing grit off the low rungs one by one with the tip of a wing', 18, 'wing',
        [k(.12, 'rung_lo', reach=.7, x=.2, y=.4), k(.32, 'rung_lo', reach=1, x=.4, y=.6, b=-.3, l=1, mark='fff'), k(.52, 'rung_mid', reach=1, x=.4, y=.2, b=-.8, r=1, mark='fff'),
         k(.72, 'rung_r', reach=1, x=.3, y=.8, b=.2, mark='fff'), k(.9, eye='^')],
        [(.52, 'brush')], g='care', act=('sweep', 'rungs'), when=['obj_dirt>.3'])
    o.r('tighten_foot_bolt', 'Winding the foot bolt tight with his bill, then listening for a squeak', 20, 'none',
        [k(.12, x=.4, y=.5), k(.3, 'foot_bolt', x=1.3, y=1.9, b=.9, mark='ck'), k(.46, 'foot_bolt', x=1.4, y=2, b=1, r=1, mark='ck'), k(.62, 'foot_bolt', x=1.4, y=2, b=1.1, l=1, mark='CK'),
         k(.8, x=.6, y=-.3, b=-.5, eye='o', mark='...'), k(.92, eye='^')],
        [(.62, 'tighten')], g='care', act=('tug', 'bolt'), when=['obj_condition<.6'],
        say=["Bolt tight. Squeak gone. I accept the credit.", "Turned it with my face. Engineering."])
    o.r('chip_ice_off_the_apron', 'Chipping a frost crust off the apron rim with a twig', 22, 'twig',
        [k(.12, 'apron_l', reach=.5, x=.5, y=.9, b=.4), k(.3, 'apron_l', reach=1, x=.8, y=1.3, b=.8, mark='tk'), k(.5, 'apron_r', reach=1, x=.9, y=1.3, b=.9, l=1, mark='tk'),
         k(.7, 'apron_r', reach=1, x=.6, y=1.1, b=.7, r=1, mark='TK'), k(.88, eye='^')],
        [(.7, 'chip')], g='weather', act=('chip', 'apron'), when=['frost>.3'])
    o.r('plough_the_apron_drift', 'Ploughing a snow drift off the apron with a bill held low', 22, 'none',
        [k(.1, 'apron_r', x=.3, y=.8, b=.2), k(.3, 'apron_r', x=1, y=2, b=1.2, mark='shhh'), k(.55, 'apron_l', x=1.2, y=2, b=1.3, l=1, r=1, mark='SHHH'), k(.8, x=.4, y=.5, b=.2, w=.5, eye='>'), k(.92, eye='-')],
        [(.55, 'plough')], g='weather', act=('rake', 'drift'), when=['drift>.3'],
        say=["Drift ploughed. I am a snowplough with opinions.", "Snow on my bill. Not a good look."])
    # ---------------- use / test
    o.r('listen_to_the_rail', 'Pressing his bill to the ladder rail to hear the wind thrum it', 22, 'none',
        [k(.12, 'rail_l', x=.5, y=.2, b=-.3), k(.3, 'rail_l', x=1.3, y=-.8, b=-1, eye='o', l=1), k(.55, 'rail_l', x=1.5, y=-1, b=-1.3, eye='-', mark='hmmm'), k(.78, 'rail_l', x=.9, y=.6, b=.4, eye='O', mark='...'), k(.92, eye='>')],
        [], g='test', act=('listen', 'rail'), when=['windy'], prefer=['curious'],
        say=["Rail hums in the wind. Off-key. Typical.", "Heard a note. Told it to stop."])
    o.r('measure_up_the_rail', 'Standing against the ladder rail to see how tall he is on it', 20, 'wing',
        [k(.12, 'post_l', reach=.2, x=.2, b=-.2), k(.32, 'rail_l', reach=1, x=-.2, y=-.9, b=-1, w=1), k(.5, 'rung_mid', reach=1, x=-.2, y=-.9, b=-1.2, mark='tap'), k(.7, 'rail_l', reach=1, x=.2, y=.2, b=.4, l=1), k(.9, eye='>')],
        [], g='test', act=('measure', 'rail'), prefer=['young', 'curious'],
        say=["Taller than the first rung. Gloating rights obtained.", "Slide is huge. I am tiny. Fine."])
    o.r('hop_the_first_deck', 'Hopping up onto the first deck board, two flaps and a landing', 20, 'none',
        [k(.1, 'deck_lo', x=.4, b=.6), k(.28, 'deck_lo', perch=1, x=.6, y=-.5, b=-1.4, w=1, r=1, mark='hup'), k(.5, 'deck_lo', perch=1, x=.3, y=.2, b=.5, eye='o'),
         k(.7, 'deck_lo2', perch=1, x=.8, y=-.6, b=-1, w=.8, l=1), k(.88, 'deck_lo2', perch=1, x=.2, b=.2, eye='^')],
        [], g='use', act=('hop', 'deck'), prefer=['young'])
    o.r('slalom_the_posts', 'Racing between the two ladder posts and back with his neck out flat', 22, 'none',
        [k(.1, 'post_l', x=.8, y=.8, b=.4), k(.26, 'post_r', x=1.6, y=1.4, b=1.2, w=1, l=1, mark='zoom'), k(.46, 'post_l', x=1.6, y=1.4, b=1.2, w=1, r=1), k(.66, 'post_r', x=1.8, y=1.6, b=1.3, w=1, l=1, mark='ZOOM'), k(.86, 'post_l', x=.3, b=.2, eye='@')],
        [(.66, 'laugh')], g='play', act=('race', 'posts'), prefer=['happy'],
        say=["Won. Against nobody. Close finish.", "Lap four. Legs are voting to leave."])
    o.r('kick_the_apron_grit', 'Kicking grit off the apron with one foot, left then right', 18, 'none',
        [k(.12, 'apron_l', x=.3, y=.4, b=.2), k(.3, 'apron_l', x=.6, y=.8, b=.7, l=1, mark='tsh'), k(.5, 'apron_l', x=.6, y=.8, b=.7, r=1, mark='tsh'), k(.7, 'apron_r', x=.5, y=.8, b=.6, l=1, mark='TSH'), k(.9, eye='-')],
        [(.5, 'brush')], g='play', act=('kick', 'grit'), prefer=['grumpy'], when=['obj_dirt>.3'])
    o.r('sit_on_the_apron', 'Sitting on the apron rim with his feet out, watching the lanes', 26, 'none',
        [k(.15, 'apron_l', perch=1, x=.3, b=.5), k(.35, 'apron_l', perch=1, x=.5, y=.3, b=1.2, eye='o'), k(.6, 'apron_r', perch=1, x=.5, y=.2, b=1.3, eye='-'), k(.85, 'apron_r', perch=1, x=.3, b=.4, eye='^')],
        [(.6, 'rest')], g='rest', act=('sit', 'apron'), prefer=['tired'])
    o.r('nap_on_the_first_deck', 'Dozing flat on the first deck board, one wing over his eyes', 36, 'none',
        [k(.12, 'deck_lo', perch=1, x=.2, b=.6), k(.3, 'deck_lo', perch=1, x=.4, y=.9, b=1.5, w=.5, eye='-'), k(.6, 'deck_lo', perch=1, x=.4, y=1, b=1.6, w=.8, eye='-', mark='zzz'), k(.85, 'deck_lo2', perch=1, x=.2, y=.4, b=.7, w=0, eye='^')],
        [(.6, 'rest')], g='rest', act=('nap', 'deck'), prefer=['tired'], when=['night'],
        say=["Deck is hard. Dreams are soft. Net win.", "Slept on a plank. Spine filed a complaint."])
    o.r('shelter_by_the_post', 'Huddling against the ladder post, shoulders to the wind', 30, 'none',
        [k(.15, 'post_r', x=-.3, y=.4, b=.6), k(.4, 'post_r', x=-.8, y=1, b=1, w=.5, eye='-'), k(.7, 'post_r', x=-.9, y=1.1, b=1.1, w=.6, eye='-', mark='brr'), k(.9, 'post_r', x=-.4, y=.4, b=.4, eye='^')],
        [], g='rest', act=('shelter', 'post'), when=['windy', 'cold'])
    o.r('slide_on_the_slick_apron', 'Going down in a long skid on the slick apron, wings flat out', 18, 'none',
        [k(.1, 'apron_l', perch=1, x=.3, b=.1), k(.3, 'apron_l', perch=1, x=.8, y=.5, b=-.6, w=1, l=1, mark='oop'), k(.52, 'apron_r', perch=1, x=1.5, y=1.6, b=1.6, w=1, r=1, eye='>', mark='WHEEEE'), k(.8, 'apron_r', perch=1, x=.6, y=1.2, b=1.1, eye='@')],
        [(.52, 'scuff')], g='mishap', act=('slip', 'apron'), when=['obj_wetness>.3'],
        say=["Skidded. Face first. Rainbow looked on.", "No harm. Mostly to my reputation."])
    o.r('bill_caught_in_lane', 'Pushing his bill into a lane seam to see how deep it goes, and getting held', 24, 'none',
        [k(.12, x=.4, y=.4), k(.3, 'lane_b', x=1.2, y=1.3, b=.9, mark='hm'), k(.5, 'lane_b', x=1.3, y=1.4, b=1.1, l=1, r=1, eye='O', mark='mmf'), k(.72, 'lane_b', x=1.5, y=1.2, b=1.2, w=1, mark='POP'), k(.88, x=1.7, y=.8, b=.5, eye='@')],
        [(.72, 'scuff')], g='mishap', act=('stuck', 'lane'), shown='head', prefer=['curious'])
    o.r('bonk_the_foot_bolt', 'Head-butting the foot bolt out of spite and bouncing off', 18, 'none',
        [k(.14, 'foot_bolt', x=-.4, y=-.6, b=-.4), k(.32, 'foot_bolt', x=1.5, y=1.6, b=.5, w=1, mark='GRR'), k(.46, 'foot_bolt', x=-.6, y=-1, b=-1.1, w=1, eye='O', mark='DONK'), k(.7, x=-1.3, y=1.2, b=.5, r=1, eye='@'), k(.9, eye='-')],
        [(.46, 'thud')], g='mishap', act=('knock', 'bolt'), prefer=['grumpy'],
        say=["Bolt won. Bolt is metal. Obviously.", "I butted a bolt. My plan had holes."])
    o.r('present_to_the_rainbow', 'Presenting the slide to the rainbow sky with both wings, like a landlord', 28, 'none',
        [k(.12, 'apron_l', perch=1, x=.2, b=-.2), k(.35, 'apron_l', perch=1, x=.2, y=-.7, b=-.5, w=1, l=1, mark='behold'), k(.6, 'apron_r', perch=1, x=.2, y=-.8, b=-.6, w=1, r=1, eye='^'), k(.86, 'apron_r', perch=1, x=.4, y=.3, b=.3, w=.2)],
        [(.6, 'bask')], g='show', act=('present', 'slide'), when=['rainbow_sky', 'shine>.3'], prefer=['happy'],
        say=["Rainbow for the slide. Zero for me. Bitter.", "Look at it. Look. Okay, enough."])
    o.r('argue_with_the_chute', 'Arguing with the chute from the apron, wing jabbing at its rim', 20, 'wing',
        [k(.12, 'lip_edge', reach=.6, x=.3, y=.4), k(.3, 'lip_edge', reach=1, x=.8, y=-.3, b=.2, mark='NO'), k(.5, 'lane_c', reach=1, x=.9, y=-.5, b=.4, r=1, mark='NO'), k(.7, 'lip_edge', reach=1, x=.5, y=.6, b=.8, l=1, eye='>', mark='!!'), k(.9, eye='-')],
        [], g='show', act=('argue', 'chute'), prefer=['grumpy'],
        say=["Chute had no rebuttal. Won on silence.", "Called it a plastic tongue. Felt good."])
    o.r('pose_at_the_foot', 'Striking a pose at the chute foot with one foot up on the rim', 18, 'none',
        [k(.14, 'apron_r', perch=1, x=.2, b=-.4), k(.4, 'apron_r', perch=1, x=-.2, y=-.4, b=-1, w=.6, l=1, eye='^'), k(.68, 'apron_r', perch=1, x=.8, y=-.6, b=-.8, w=1, r=1, l=1), k(.9, 'apron_r', perch=1, x=.2, b=-.2)],
        [], g='show', act=('pose', 'foot'), prefer=['happy'])
    # ---------------- v3 top-up
    o.r('roll_the_painted_run', 'Rolling down the painted run with his wings pinned, arriving as a dizzy ball', 22, 'none',
        [k(.12, 'lane_c', perch=1, x=.2, b=.5), k(.3, 'lane_c', perch=1, x=.2, y=1.5, b=2.2, eye='-'), k(.52, 'lane_a', perch=1, x=.4, y=1.8, b=2.4, l=1, r=1, mark='wub wub'), k(.74, 'apron_l', perch=1, x=.9, y=2.2, b=1.8, eye='@'), k(.9, 'apron_l', perch=1, x=.3, y=.4, b=.4, eye='^')],
        [], g='use', act=('roll', 'lanes'), prefer=['young'])
    o.r('plunge_down_beak_first', 'Plunging down the run beak first with both wings laid flat along his back', 20, 'none',
        [k(.12, 'lane_c', perch=1, x=.6, y=.9, b=.6), k(.3, 'lane_c', perch=1, x=2, y=2.2, b=1, w=.4, eye='>', mark='VWOOM'), k(.5, 'lane_a', perch=1, x=2.4, y=2.6, b=1.3, w=.6), k(.72, 'apron_r', perch=1, x=2.6, y=2.9, b=1.5, eye='O', mark='SPLAT'), k(.9, 'apron_r', perch=1, x=.6, y=1, b=.6, eye='@')],
        [], g='use', act=('race', 'run'), prefer=['happy'], say=["Fastest duck on the rainbow. Sole entrant.", "Beak first. Lessons: none learned."])
    o.r('trail_backwards_down', 'Trailing down the run backwards with his feet up on the rim, saying goodbye to the tower', 22, 'none',
        [k(.12, 'lane_c', perch=1, x=-.7, y=-.8, b=-.8, w=.5), k(.32, 'lane_c', perch=1, x=-1.6, y=-1.5, b=-1.4, l=1, w=.8, eye='-'), k(.54, 'lane_a', perch=1, x=-2, y=-1.8, b=-1.7, r=1, w=1), k(.76, 'apron_l', perch=1, x=-1, y=.4, b=1.2, eye='@'), k(.92, 'apron_l', perch=1, x=.1, b=.1, eye='^')],
        [], g='use', act=('drag', 'run'), prefer=['grown'])
    o.r('stop_hard_at_the_foot', 'Stopping dead at the foot with both heels dug into the apron, thrown forward onto his chin', 20, 'none',
        [k(.12, 'lane_a', perch=1, x=.4, b=.3), k(.3, 'apron_l', perch=1, x=.8, y=.5, b=-1, l=1, r=1, w=.8, mark='SKRRT'), k(.5, 'apron_l', perch=1, x=1.8, y=2, b=1.9, eye='O', mark='THUD'), k(.72, 'apron_l', perch=1, x=.6, y=1.2, b=.8, eye='@'), k(.9, 'apron_l', perch=1, x=.2, b=.2, eye='-')],
        [], g='use', act=('brace', 'apron'), say=["Heels dug in. Chin dug in more.", "Brakes work. Face is the brakes."])
    o.r('spin_down_like_a_top', 'Spinning down the run like a top with one wing out, drawing a spiral of scuffs', 22, 'wing',
        [k(.12, 'lane_c', perch=1, reach=.3, x=.1, b=.2), k(.3, 'lane_c', perch=1, reach=1, x=-.4, y=.6, b=.8, r=1), k(.5, 'lane_a', perch=1, reach=1, x=.6, y=1, b=1.1, l=1), k(.7, 'apron_r', perch=1, reach=1, x=-.7, y=1.3, b=1.3, r=1, eye='@'), k(.9, 'apron_r', perch=1, reach=.1, x=.1, eye='-')],
        [], g='use', act=('spin', 'run'), prefer=['curious'])
    o.r('climb_the_ladder_by_the_rung', 'Climbing the ladder one rung at a time, the left wing locked on the rung above', 26, 'wing',
        [k(.1, 'rung_lo', perch=1, reach=.4, x=.4, b=.5), k(.3, 'rung_lo', perch=1, reach=1, x=.8, y=-.8, b=-.8, r=1, mark='hup'), k(.5, 'rung_mid', perch=1, reach=1, x=.7, y=-1, b=-1, l=1), k(.7, 'deck_two', perch=1, reach=.5, x=.3, y=.5, b=.5, eye='o'), k(.88, 'rung_lo', perch=1, reach=.2, x=.2, b=.4, eye='^')],
        [], g='use', act=('climb', 'ladder'), ages=GROWN)
    o.r('scrub_the_rails', 'Scrubbing the ladder rails with a wing from the bottom rung to as high as he can reach', 22, 'wing',
        [k(.1, 'rail_l', reach=.5, x=.2, y=.2), k(.28, 'rail_l', reach=1, x=.3, y=-.4, b=-.5, mark='skrk'), k(.46, 'rung_mid', reach=1, x=.4, y=-.7, b=-.8, l=1, mark='skrk'), k(.66, 'rail_l', reach=1, x=.4, y=.4, b=.3, r=1, mark='skrk'), k(.86, eye='^')],
        [(.46, 'polish')], g='care', act=('scrub', 'rails'), when=['obj_dirt>.3'])
    o.r('wipe_the_wet_apron', 'Wiping the wet apron with his tail end, left to right and back again', 20, 'none',
        [k(.1, 'apron_l', x=.1, y=.5, b=1.1), k(.3, 'apron_l', x=-.3, y=.9, b=1.8, w=.4, mark='fwp'), k(.5, 'apron_r', x=-.3, y=.9, b=1.9, w=.5, mark='fwp'), k(.7, 'apron_r', x=-.1, y=.5, b=1.2, eye='-'), k(.9, eye='^')],
        [(.5, 'pat')], g='care', act=('wipe', 'apron'), when=['obj_wetness>.3'])
    o.r('scrape_ice_from_the_run', 'Scraping a sheet of ice off the run foot with a stiff twig', 22, 'twig',
        [k(.12, 'lane_a', reach=.4, x=.3, y=.7, b=.3), k(.3, 'lane_a', reach=1, x=.6, y=.9, b=.5, mark='zrk'), k(.5, 'lane_b', reach=1, x=.7, y=.8, b=.6, r=1, mark='zrk'), k(.7, 'lane_c', reach=1, x=.6, y=.3, b=.2, l=1, mark='ZRK'), k(.88, eye='^')],
        [(.7, 'chip')], g='weather', act=('scrape', 'lanes'), when=['frost>.3'])
    o.r('scoop_the_drift', 'Scooping a snow drift off the apron with his bill and tossing it over his shoulder', 22, 'none',
        [k(.1, 'apron_r', x=.4, y=.9, b=.6), k(.28, 'apron_r', x=1.2, y=1.8, b=1.4, mark='fsh'), k(.42, 'apron_r', x=-.6, y=-.6, b=-.8, w=.6, mark='fup'), k(.6, 'apron_l', x=1.2, y=1.8, b=1.4, l=1, mark='fsh'), k(.8, 'apron_l', x=-.5, y=-.5, b=-.7, w=.6, eye='>'), k(.92, eye='-')],
        [(.6, 'plough')], g='weather', act=('scoop', 'drift'), when=['drift>.3'])
    o.r('warm_up_on_the_lit_run', 'Warming his breast against the sun-bright run with a long contented sigh', 24, 'none',
        [k(.12, 'lane_a', x=.2, y=.4, b=.4), k(.34, 'lane_a', x=.1, y=1, b=1.4, eye='-'), k(.62, 'lane_b', x=.1, y=1.1, b=1.5, eye='-', mark='ahhh'), k(.86, 'lane_b', x=.2, y=.3, b=.4, eye='^')],
        [(.62, 'bask')], g='weather', act=('warm', 'run'), when=['shine>.4', 'day'])
    o.r('tap_the_iced_rung', 'Tapping the iced rung to hear whether the frost sounds hollow', 20, 'none',
        [k(.1, 'rung_lo', x=.3, y=.7, b=.4), k(.26, 'rung_lo', x=.8, y=1.3, b=.9, mark='tk'), k(.44, 'rung_mid', x=.8, y=-.5, b=-.7, mark='tk'), k(.62, 'rung_lo', x=.9, y=1.4, b=1, l=1, mark='tkk'), k(.84, eye='^')],
        [(.62, 'chip')], g='weather', act=('tap', 'rung'), when=['frost>.5'])
    o.r('sniff_the_run', 'Sniffing along the run for stale crumbs, nose in every seam', 20, 'none',
        [k(.1, 'lane_c', x=.3, y=-.6, b=-.5), k(.3, 'lane_d', x=1.2, y=.9, b=.8, mark='snf'), k(.5, 'lane_a', x=1.5, y=1.5, b=1.3, mark='snf'), k(.7, 'foot_bolt', x=1.7, y=2, b=1.6, eye='o', mark='snf'), k(.9, eye='>')],
        [], g='test', act=('sniff', 'run'), prefer=['curious'])
    o.r('weigh_the_bottom_rung', 'Standing on the bottom rung with his whole weight to see whether it gives', 22, 'none',
        [k(.1, 'rung_lo', perch=1, x=.2, b=.4, l=1), k(.3, 'rung_lo', perch=1, x=.4, y=.5, b=1, r=1, mark='creak'), k(.5, 'rung_lo', perch=1, x=.3, y=.9, b=1.4, eye='o'), k(.72, 'rung_lo', perch=1, x=.4, y=.3, b=.3, eye='^')],
        [], g='test', act=('weigh', 'rung'))
    o.r('peer_up_the_tower', 'Tipping his head right back to peer up the tower, one wing steadying him at the post', 22, 'none',
        [k(.12, 'post_r', x=.1, y=-.4, b=-.3), k(.34, 'post_r', x=.2, y=-1.5, b=-1.4, w=.4, eye='o'), k(.56, 'post_r', x=-.2, y=-1.8, b=-1.8, w=.8, eye='O', l=1), k(.78, 'post_r', x=.1, y=.2, b=.2, eye='-'), k(.92, eye='>')],
        [], g='test', act=('peer', 'tower'))
    o.r('count_the_lanes', 'Counting the lanes at the foot with a tap of the bill each, getting it right once', 22, 'none',
        [k(.1, 'lane_a', x=.4, y=.9, b=.4, mark='1'), k(.3, 'lane_a', x=1, y=1.5, b=.8, mark='tk'), k(.5, 'lane_b', x=1, y=1.5, b=.8, mark='tk'), k(.7, 'lip_edge', x=.8, y=-.4, b=-.4, mark='3'), k(.9, 'lane_b', x=.4, y=.8, b=.4, eye='-')],
        [], g='test', act=('count', 'lanes'))
    o.r('chase_the_post_shadow', 'Chasing the ladder post shadow round and round until the post wins', 22, 'none',
        [k(.1, 'post_l', x=.8, y=.5, b=.2), k(.28, 'post_r', x=1.8, y=1.5, b=1.4, w=1, l=1), k(.46, 'post_l', x=-.8, y=1.2, b=.6, r=1, w=1), k(.64, 'post_r', x=1.9, y=1.6, b=1.5, w=1, l=1), k(.84, 'post_l', x=.3, y=.4, eye='@')],
        [(.64, 'laugh')], g='play', act=('chase', 'post'), prefer=['happy'])
    o.r('dance_on_the_deck', 'Dancing a wobbly jig along the low deck boards, feet going in two directions', 24, 'none',
        [k(.1, 'deck_lo', perch=1, x=.3, b=.2, l=1), k(.28, 'deck_lo', perch=1, x=.2, y=-.4, b=-.7, r=1, w=1), k(.48, 'deck_lo2', perch=1, x=.2, y=-.4, b=.8, l=1, w=.4), k(.68, 'deck_lo2', perch=1, x=.1, y=-.7, b=-.8, r=1, l=1, w=1, eye='^'), k(.9, 'deck_lo2', perch=1, x=.2, b=.1)],
        [], g='play', act=('dance', 'deck'), prefer=['happy'])
    o.r('hop_the_apron_ends', 'Hopping the apron end to end on one foot, then the other, switching without a plan', 20, 'none',
        [k(.1, 'apron_l', perch=1, x=.4, b=-.7, l=1), k(.3, 'apron_l', perch=1, x=.5, b=-1.5, l=1, w=.6), k(.5, 'apron_r', perch=1, x=.5, b=-.8, r=1), k(.7, 'apron_r', perch=1, x=.5, b=-1.6, r=1, w=.8, mark='hup'), k(.9, 'apron_r', perch=1, x=.2, b=.2, eye='^')],
        [], g='play', act=('hop', 'apron'), prefer=['young'])
    o.r('balance_along_the_deck', 'Balancing along the low deck with one wing out and the other held to his chest', 24, 'wing',
        [k(.1, 'deck_lo', perch=1, reach=.6, x=.2, b=-.3), k(.3, 'deck_lo', perch=1, reach=1, x=.2, y=.3, b=.3, l=1), k(.52, 'deck_lo2', perch=1, reach=1, x=.2, y=.3, b=.4, r=1), k(.74, 'deck_lo2', perch=1, reach=.4, x=.1, y=.5, b=-.4, l=1, eye='-'), k(.9, 'deck_lo2', perch=1, reach=.1, x=.3, b=.2)],
        [], g='play', act=('balance', 'deck'))
    o.r('lean_on_the_far_post', 'Leaning back against the far post and letting the run go by', 24, 'none',
        [k(.14, 'post_r', x=-.6, y=.4, b=.5), k(.4, 'post_r', x=-1.4, y=-.8, b=-1.2, r=1, w=.5), k(.7, 'post_r', x=-1.2, y=.2, b=1, eye='-', mark='mm'), k(.9, 'post_r', x=-.3, y=.3, b=.1, eye='^')],
        [], g='rest', act=('lean', 'post'))
    o.r('sulk_at_the_bottom_rung', 'Sulking at the bottom rung with his bill in his chest', 26, 'none',
        [k(.15, 'rung_lo', x=.5, y=1, b=.6), k(.4, 'rung_lo', x=.9, y=1.5, b=1.1, eye='-'), k(.7, 'rung_lo', x=1, y=1.7, b=1.3, eye='-', mark='hmph'), k(.9, x=.3, y=.4, b=.2, eye='^')],
        [], g='rest', act=('sulk', 'rung'), prefer=['sad', 'grumpy'], say=["Rainbow slide. Grey duck. Compare.", "No. Leave me with my rung."])
    o.r('wait_for_a_turn', 'Waiting at the foot of the ladder for a turn that is going to be his own', 28, 'none',
        [k(.12, 'post_l', x=.3, y=-.5, b=-.4), k(.34, 'rung_lo', x=.5, y=-1.1, b=-.9, eye='o', mark='...'), k(.56, 'post_l', x=.3, y=.8, b=.7, l=1, eye='-'), k(.8, 'rung_lo', x=.4, y=-1.2, b=-1, r=1, eye='o'), k(.94, eye='>')],
        [], g='rest', act=('wait', 'ladder'), prefer=['lonely'])
    o.r('stub_a_toe_on_the_post', 'Stubbing a toe against the ladder post and hopping around it cursing', 18, 'none',
        [k(.12, 'post_l', x=.4, y=.5, b=.3), k(.3, 'post_l', x=.8, y=.9, b=-.6, l=1, mark='tok'), k(.46, 'post_l', x=-.5, y=-.7, b=-1.6, l=1, w=1, eye='O', mark='FFS'), k(.66, 'post_r', x=-1, y=1.1, b=.6, r=1, eye='@'), k(.88, eye='>')],
        [(.46, 'thud')], g='mishap', act=('kick', 'post'), prefer=['grumpy'], say=["Post: 1. Toe: 0. Language: unprintable.", "Hopped. Swore. Still own a post-shaped grudge."])
    o.r('hang_a_wing_on_the_bolt', 'Hooking a wing round the foot bolt and tugging until it comes free with a snap', 22, 'wing',
        [k(.12, 'foot_bolt', reach=.5, x=.3, y=.4), k(.3, 'foot_bolt', reach=1, x=.5, y=.2, b=.3, mark='hm'), k(.5, 'foot_bolt', reach=1, x=-.4, y=-.2, b=-.9, l=1, r=1, eye='O', mark='MPH'), k(.7, 'foot_bolt', reach=1, x=-.9, y=-.5, b=-1.3, w=0, eye='@', mark='SNAP'), k(.9, x=.2, eye='-')],
        [], g='mishap', act=('hook', 'bolt'))
    o.r('somersault_off_the_apron', 'Somersaulting off the apron end in a flap of wings and landing on his back', 20, 'none',
        [k(.12, 'apron_r', perch=1, x=.2, b=.3), k(.3, 'apron_r', perch=1, x=.9, y=1.2, b=-1.2, w=1, mark='eep'), k(.5, 'apron_r', perch=1, x=-1.4, y=-1.8, b=2, w=1, l=1, r=1, eye='O', mark='BONK'), k(.74, 'apron_r', perch=1, x=.7, y=1.6, b=1.3, eye='@'), k(.9, 'apron_r', perch=1, x=.3, b=.3, eye='>')],
        [(.5, 'scuff')], g='mishap', act=('fold', 'apron'))
    o.r('sing_up_the_run', 'Singing up the run to hear the hum come back, hitting the seam note every time', 24, 'none',
        [k(.12, 'lane_a', x=.4, y=-.4, b=-.3), k(.3, 'lane_a', x=1.1, y=-1, b=-.9, w=.8, mark='LAAAH'), k(.5, 'lane_b', x=1.2, y=-1.1, b=-1, w=1, eye='^', mark='LAAAH'), k(.72, 'lane_a', x=.6, y=-.4, b=-.2, eye='o', mark='la?'), k(.9, eye='-')],
        [], g='show', act=('sing', 'run'), prefer=['lonely'])
    o.r('bow_to_the_ladder_top', 'Bowing to the top of the ladder as if the sky had clapped', 18, 'none',
        [k(.15, 'post_r', x=-.4, y=-1, b=-1, w=.6), k(.4, 'post_r', x=1, y=2, b=1.4, w=1, l=1, mark='bravo'), k(.65, 'post_r', x=1.1, y=2.4, b=1.7, w=1, r=1), k(.88, 'post_r', x=.1, y=-.4, b=-.4, eye='^')],
        [], g='show', act=('bow', 'ladder'))
    o.r('compare_the_lanes', 'Comparing the lanes side by side, head tilting from the left lane to the right', 24, 'none',
        [k(.12, 'lane_a', x=.5, y=.6, b=.3), k(.32, 'lane_a', x=1, y=1.2, b=.7, eye='o'), k(.5, 'lane_b', x=1, y=1.2, b=.7, eye='O'), k(.7, 'lane_a', x=.9, y=.4, b=.2, eye='-', mark='hm'), k(.88, 'lane_b', x=.5, y=.9, b=.5, eye='>')],
        [], g='show', act=('compare', 'lanes'), prefer=['curious'])
    o.emit()


def water_slide():
    # Drawing (108 x 75 cells, 7.7 px a row, standing line row 71): a ground floor `|=========0=========|` cols 8-28 (0 px), then the scaffold tower with
    # rail pairs and rungs every 5 rows (38, 77, 115 px); the chute comes down on the right to cols 84-100 with a bolt at row 66 (col 86), lane seams
    # `||`, spray `~` over its mouth (row 64, 54 px), and lands in a drawn pool: front brim `(` cols 57-62 and `)` cols 98-103, ripple dashes `--` on row 68
    # (cols 65, 79, 93) and mist `~~` on row 69 (cols 72, 86). Nothing of him goes in the pool; he works its brim and the chute foot.
    P = pm('water_slide')
    o = Obj('water_slide', 'placed',
            fields=dict(pool=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('pool', 'rate', .002, 'wet'), ('pool', 'rate', -.001, 'sun'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(skim=[('obj.dirt', 'add', -.2)], scour=[('obj.dirt', 'add', -.3)], flick=[('obj.wetness', 'add', -.25)], tighten=[('obj.condition', 'add', .2)],
                         thud=[('obj.condition', 'add', -.15)], splash=[('obj.wetness', 'add', .2), ('pool', 'add', -.15)], muddy=[('obj.dirt', 'add', .12)], bruise=[('obj.dirt', 'add', .14)],
                         chip=[('frost', 'mul', .25)], laugh=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)], bail=[('pool', 'add', -.3)]),
            anchors=dict(floor_l=P(12, 71, 'surface'), floor_r=P(24, 71, 'surface'), rail_l=P(8, 69), rung_lo=P(9, 66, 'surface'), deck_lo=P(17, 66, 'surface'), rail_r=P(28, 69),
                         pool_l=P(57, 68), lip_l=P(59, 70, 'surface'), pool_r=P(103, 68), lip_r=P(101, 70, 'surface'), ripple_a=P(65, 68), ripple_b=P(79, 68),
                         mist_a=P(72, 69), mist_b=P(86, 69), foot_bolt=P(86, 66), spray=P(94, 64), lane_a=P(91, 69, 'surface'), lane_b=P(97, 68), lane_c=P(86, 63, 'surface'), lane_m=P(90, 67, 'surface')))
    # ---------------- care
    o.r('skim_the_ripples', 'Skimming the pool top clean with a long wing sweep from brim to brim', 22, 'wing',
        [k(.1, 'lip_l', reach=.5, x=.5, y=.8, b=.3), k(.3, 'ripple_a', reach=1, x=.9, y=1, b=.6, l=1, mark='shff'), k(.5, 'ripple_b', reach=1, x=.9, y=1, b=.6, r=1, mark='shff'),
         k(.72, 'pool_r', reach=1, x=.7, y=.9, b=.4, l=1), k(.9, eye='^')],
        [(.72, 'skim')], g='care', act=('sweep', 'pool'), when=['obj_dirt>.3'],
        say=["Skimmed it. The pool looks cleaner than me.", "Pond scum on my wing. Medal worn."])
    o.r('scour_the_lane_seams', 'Scouring the slimed lane seams with a stiff bill, up and down', 22, 'none',
        [k(.1, 'lane_a', x=.4, y=.7, b=.2), k(.26, 'lane_a', x=1, y=1.5, b=.8, mark='skr'), k(.4, 'lane_b', x=1, y=-.3, b=-.4, mark='skr'), k(.56, 'lane_a', x=1.2, y=1.6, b=.9, l=1, mark='SKR'),
         k(.76, 'lane_b', x=.6, y=.5, b=.2, r=1), k(.9, eye='>')],
        [(.56, 'scour')], g='care', act=('scrub', 'seams'), when=['obj_dirt>.4'])
    o.r('flick_water_off_the_rail', 'Flicking the spray off the ladder rail with his wing until it squeaks', 18, 'wing',
        [k(.12, 'rail_l', reach=.5, x=.2, y=.2), k(.3, 'rail_l', reach=1, x=.3, y=.4, b=.3, mark='fip'), k(.5, 'rail_r', reach=1, x=.3, y=.4, b=.3, r=1, mark='fip'), k(.7, 'rail_r', reach=.3, x=.1, y=.2, w=.4), k(.9, eye='-')],
        [(.5, 'flick')], g='care', act=('shake', 'rail'), when=['obj_wetness>.5'])
    o.r('tighten_the_spout_bolt', 'Biting the foot bolt round a quarter turn with his bill', 18, 'none',
        [k(.12, x=.5, y=.6), k(.3, 'foot_bolt', x=1.2, y=.2, b=.4, mark='ng'), k(.5, 'foot_bolt', x=1.4, y=.2, b=.5, l=1, mark='ng'), k(.7, 'foot_bolt', x=1.5, y=.3, b=.6, r=1, mark='NG'), k(.9, x=.3, eye='^')],
        [(.7, 'tighten')], g='care', act=('mend', 'bolt'), when=['obj_condition<.6'],
        say=["Bolt tight. Water stays where I put it.", "Bit it into line. Dental work."])
    o.r('chip_ice_off_the_brim', 'Chipping a frozen rind off the pool brim with a twig', 22, 'twig',
        [k(.12, 'lip_l', reach=.5, x=.4, y=.9, b=.5), k(.3, 'lip_l', reach=1, x=.7, y=1.2, b=.7, mark='tk'), k(.5, 'lip_r', reach=1, x=.8, y=1.1, b=.8, l=1, mark='tk'), k(.72, 'lip_r', reach=1, x=.8, y=1.3, b=.9, r=1, mark='TK'), k(.9, eye='>')],
        [(.72, 'chip')], g='weather', act=('chip', 'brim'), when=['frost>.3'])
    # ---------------- use / test
    o.r('dabble_at_the_brim', 'Dabbling his bill through the pool brim, tasting nothing and enjoying it', 24, 'none',
        [k(.1, 'lip_l', perch=1, x=.4, y=.5, b=.3), k(.28, 'lip_l', perch=1, x=1.4, y=1.3, b=1.1, mark='gloop'), k(.46, 'lip_l', perch=1, x=1.5, y=1.4, b=1.2, eye='-', mark='glp'), k(.64, 'lip_l', perch=1, x=1.4, y=1.2, b=1, eye='o', mark='glop'), k(.86, 'lip_l', perch=1, x=.3, y=.5, b=.3, eye='^')],
        [(.46, 'muddy')], g='use', act=('peck', 'pool'), shown='head', when=['pool>.3'], prefer=['happy'],
        say=["Pool is wet. I checked with my face.", "Ducks dabble. It's not a hobby, it's the law."])
    o.r('splash_the_pool', 'Splashing the pool up the chute foot with a big wing slap', 20, 'wing',
        [k(.1, 'ripple_b', reach=.4, x=.3, y=.5, b=.3), k(.28, 'ripple_b', reach=1, x=.2, y=-.4, b=-.9, w=1, l=1, mark='SPLAT'), k(.46, 'mist_b', reach=1, x=.2, y=.4, b=.5, r=1, mark='splt'), k(.64, 'lane_a', reach=1, x=.2, y=-.6, b=-1.1, mark='SPLAT'), k(.88, eye='^')],
        [(.46, 'splash'), (.64, 'laugh')], g='play', act=('splash', 'pool'), when=['pool>.3'], prefer=['happy'],
        say=["Soaked the chute. It had it coming.", "Splash. Splash. Splash. I am three."])
    o.r('catch_the_spray', 'Catching the chute spray in his open bill, head thrown back', 20, 'none',
        [k(.12, 'spray', x=.2, y=-.4, b=-.4), k(.3, 'spray', x=.6, y=-1.2, b=-1, w=.8, eye='O', mark='ahh'), k(.5, 'spray', x=.8, y=-1.3, b=-1.2, w=1, l=1, mark='glk'), k(.72, 'spray', x=.5, y=-.6, b=-.5, r=1, eye='^'), k(.9, x=0, y=.2, b=0)],
        [], g='play', act=('catch', 'spray'), prefer=['curious'])
    o.r('dip_a_foot_in_the_brim', 'Testing the pool with one foot and drawing it back in a hurry', 20, 'none',
        [k(.12, 'lip_r', perch=1, x=.2, y=.4, b=.2), k(.3, 'lip_r', perch=1, x=.3, y=.8, b=.4, l=1, eye='o'), k(.46, 'lip_r', perch=1, x=.2, y=.9, b=.7, l=1, mark='brr'), k(.62, 'lip_r', perch=1, x=-.4, y=-.2, b=-.5, l=1, w=.6, eye='>'), k(.84, 'lip_r', perch=1, x=.2, b=.1, eye='-')],
        [], g='test', act=('test', 'brim'), prefer=['curious'], when=['cold'],
        say=["Cold. Brain says leave. Foot already left.", "Water is a liar. It looked nice."])
    o.r('count_the_ripple_rings', 'Counting the ripple dashes along the pool, three, then three again', 24, 'none',
        [k(.1, 'ripple_a', x=.5, y=.7, b=.3, mark='1'), k(.28, 'ripple_a', x=1, y=1.3, b=.7, mark='2'), k(.46, 'mist_a', x=1, y=1.2, b=.6, mark='3'), k(.64, 'ripple_b', x=1, y=1.3, b=.7, mark='4?'), k(.82, 'mist_b', x=1.1, y=1.4, b=.8, eye='@', mark='...'), k(.94, eye='-')],
        [], g='test', act=('count', 'ripples'), prefer=['curious'])
    o.r('chase_the_mist_marks', 'Chasing the mist marks along the pool front, bill snapping', 22, 'none',
        [k(.1, 'mist_a', x=.6, y=.8, b=.4), k(.26, 'mist_b', x=1.4, y=1.2, b=.9, w=1, l=1, mark='snp'), k(.42, 'mist_a', x=1.4, y=1.3, b=1, w=1, r=1, mark='snp'), k(.6, 'mist_b', x=1.6, y=1.4, b=1.1, w=1, l=1, mark='SNP'), k(.8, 'ripple_b', x=.3, y=.6, b=.2, eye='@')],
        [(.6, 'laugh')], g='play', act=('chase', 'mist'), prefer=['happy'])
    o.r('race_the_pool_brim', 'Racing along the pool brim from the left horn to the right, one flap too many', 20, 'wing',
        [k(.1, 'lip_l', perch=1, reach=.4, x=.6, b=.2), k(.3, 'lip_l', perch=1, reach=1, x=1, y=.4, b=-.5, l=1), k(.55, 'lip_r', perch=1, reach=1, x=1.4, y=.5, b=-.7, r=1, mark='whoo'), k(.8, 'lip_r', perch=1, reach=.6, x=.4, y=.8, b=.6, eye='@', mark='ooh')],
        [], g='play', act=('race', 'brim'), prefer=['young', 'happy'])
    o.r('sit_on_the_pool_lip', 'Sitting on the pool brim with his feet hanging out, looking sour', 28, 'none',
        [k(.15, 'lip_r', perch=1, x=.3, b=.5), k(.35, 'lip_r', perch=1, x=.6, y=.5, b=1.2, eye='o'), k(.62, 'lip_r', perch=1, x=.5, y=.4, b=1.4, eye='-', mark='sigh'), k(.88, 'lip_r', perch=1, x=.3, b=.3, eye='^')],
        [(.62, 'rest')], g='rest', act=('sit', 'brim'))
    o.r('lean_on_the_ladder_rail', 'Leaning his shoulder to the ladder rail, wings folded, ignoring all splashing', 26, 'none',
        [k(.14, 'rail_l', x=-.3, y=.1, b=-.3), k(.4, 'rail_l', x=-1.1, y=-.6, b=-1, l=1), k(.66, 'rail_l', x=-1.2, y=-.4, b=.5, eye='-', mark='hm'), k(.9, 'rail_l', x=-.3, b=-.2, eye='^')],
        [(.66, 'rest')], g='rest', act=('lean', 'rail'), prefer=['tired'])
    o.r('slip_on_the_wet_floor', 'Skidding across the ground floor planks and ending flat', 18, 'none',
        [k(.12, 'floor_l', perch=1, x=.2, b=.1), k(.3, 'floor_l', perch=1, x=.9, y=.4, b=-.7, w=1, l=1, mark='eep'), k(.5, 'floor_r', perch=1, x=1.6, y=1.8, b=1.7, w=1, r=1, eye='O', mark='THUD'), k(.8, 'floor_r', perch=1, x=.5, y=1.3, b=1.1, eye='@')],
        [(.5, 'muddy')], g='mishap', act=('slip', 'floor'), when=['obj_wetness>.4'],
        say=["Floor was wet. I was optimistic.", "Flat. The planks say sorry. They are lying."])
    o.r('stuck_in_the_lane_mouth', 'Pushing his head into the chute mouth to look down it, and sticking', 24, 'none',
        [k(.12, x=.5, y=.4), k(.3, 'lane_c', x=1.2, y=.5, b=.8, mark='hm'), k(.5, 'lane_c', x=1.3, y=.6, b=1, l=1, r=1, eye='O', mark='mmf'), k(.72, 'lane_c', x=1.5, y=.4, b=1.2, w=1, mark='POP'), k(.88, x=1.9, y=1, b=.6, eye='@')],
        [(.72, 'muddy')], g='mishap', act=('stuck', 'chute'), shown='head', prefer=['young'])
    o.r('rattle_head_on_the_bolt', 'Whacking his head against the foot bolt standing up from a dabble', 18, 'none',
        [k(.1, 'foot_bolt', x=.5, y=1.4, b=1.2), k(.3, 'foot_bolt', x=.6, y=1.6, b=1.3, l=1), k(.44, 'foot_bolt', x=.8, y=-1.2, b=-1.1, w=1, eye='O', mark='BONK'), k(.62, x=-1, y=1, b=.7, r=1, eye='@'), k(.88, eye='-')],
        [(.44, 'thud')], g='mishap', act=('knock', 'bolt'),
        say=["Hit the bolt. The bolt is fine. Typical.", "Bolt: 1. Skull: 0. Rematch tomorrow."])
    o.r('bow_to_the_spray', 'Bowing to the mist over the pool as if it were the front row', 16, 'wing',
        [k(.15, 'mist_b', reach=.3, x=-.3, y=-.6, b=-.8), k(.4, 'mist_b', reach=1, x=.9, y=1.7, b=1.2, l=1, mark='thank you'), k(.65, 'mist_a', reach=1, x=1, y=2.1, b=1.5, r=1), k(.88, 'mist_a', reach=.2, x=.1, y=-.5, b=-.4, eye='^')],
        [], g='show', act=('bow', 'mist'))
    o.r('shout_at_the_pool_edge', 'Shouting at the pool from the brim about who owns the splash', 22, 'wing',
        [k(.12, 'lip_l', perch=1, reach=.3, x=.3, b=.2), k(.3, 'lip_l', perch=1, reach=1, x=1, y=-.5, b=-.2, mark='MINE'), k(.5, 'lip_l', perch=1, reach=1, x=1.1, y=-.7, b=.2, l=1, mark='MINE'), k(.72, 'lip_l', perch=1, reach=.5, x=.5, y=.6, b=.5, eye='>'), k(.9, 'lip_l', perch=1, eye='-')],
        [], g='show', act=('argue', 'pool'), prefer=['grumpy'],
        say=["Pool had a go back. Won on volume.", "Mine. Splash is mine. Ask the sky."])
    o.r('nap_on_the_ground_floor', 'Dozing flat on the ground floor boards with the spray misting over him', 36, 'none',
        [k(.12, 'floor_l', perch=1, x=.2, b=.6), k(.3, 'floor_l', perch=1, x=.4, y=.9, b=1.5, eye='-'), k(.6, 'floor_l', perch=1, x=.4, y=1, b=1.6, eye='-', mark='zzz'), k(.86, 'floor_l', perch=1, x=.2, y=.4, b=.6, eye='^')],
        [], g='rest', act=('nap', 'floor'), prefer=['tired'])
    # ---------------- v3 top-up
    o.r('roll_down_into_the_spray', 'Rolling down the wet chute foot like a barrel, wings pinned, to stop at the spray', 20, 'none',
        [k(.12, 'lane_m', perch=1, x=.3, b=.6), k(.3, 'lane_m', perch=1, x=.3, y=1.3, b=1.9, eye='-', mark='hrr'), k(.52, 'lane_a', perch=1, x=.5, y=1.6, b=2.1, l=1, r=1, mark='wub'), k(.76, 'lane_a', perch=1, x=1, y=2, b=1.6, eye='@'), k(.92, 'lane_a', perch=1, x=.2, y=.4, b=.4, eye='^')],
        [], g='use', act=('roll', 'chute'), prefer=['young'])
    o.r('shoot_the_foot_headfirst', 'Shooting down the foot of the chute headfirst, spray flying off his bill', 20, 'none',
        [k(.12, 'lane_c', perch=1, x=.5, y=.7, b=.5), k(.3, 'lane_m', perch=1, x=1.8, y=2, b=1.1, w=.5, eye='>', mark='WHEEE'), k(.52, 'lane_a', perch=1, x=2.2, y=2.5, b=1.3, w=.6), k(.74, 'lane_a', perch=1, x=2.4, y=2.7, b=1.5, eye='O', mark='SPLASH'), k(.9, 'lane_a', perch=1, x=.5, y=.9, b=.5, eye='@')],
        [], g='use', act=('race', 'spout'), ages=GROWN, say=["Headfirst. Water in places. Zero regrets.", "Face-first into the splash. Ten out of ten."])
    o.r('slide_back_into_the_mist', 'Easing down the wet foot backwards with his feet kicking mist', 22, 'none',
        [k(.12, 'lane_m', perch=1, x=-.6, y=-.7, b=-.7), k(.32, 'lane_m', perch=1, x=-1.5, y=-1.4, b=-1.2, l=1, w=.7, eye='o'), k(.54, 'lane_a', perch=1, x=-1.9, y=-1.7, b=-1.6, r=1, w=1), k(.76, 'lane_a', perch=1, x=-.9, y=.5, b=1.1, eye='@'), k(.92, 'lane_a', perch=1, x=.1, b=.1, eye='-')],
        [], g='use', act=('drag', 'chute'))
    o.r('dig_in_the_heels_mid_slide', 'Digging both heels into the wet lane halfway to stop short of the pool, and not quite managing', 20, 'none',
        [k(.12, 'lane_m', perch=1, x=.4, b=.4), k(.3, 'lane_m', perch=1, x=.8, y=.4, b=-1.1, l=1, r=1, w=.8, mark='SKREE'), k(.5, 'lane_a', perch=1, x=-.9, y=-.3, b=-1.3, l=1, r=1, w=1, eye='O'), k(.72, 'lane_a', perch=1, x=.6, y=1, b=.9, eye='-', mark='phew'), k(.9, 'lane_a', perch=1, x=.2, b=.2, eye='^')],
        [], g='use', act=('brace', 'chute'))
    o.r('spin_down_the_wet_foot', 'Spinning down the wet foot in a flat circle, one wing flicking spray', 22, 'wing',
        [k(.12, 'lane_m', perch=1, reach=.3, x=.1, b=.3), k(.3, 'lane_m', perch=1, reach=1, x=-.5, y=.5, b=.9, l=1), k(.5, 'lane_a', perch=1, reach=1, x=.7, y=1.1, b=1.2, r=1, mark='fwsh'), k(.72, 'lane_a', perch=1, reach=1, x=-.8, y=1.4, b=1.4, l=1, eye='@'), k(.9, 'lane_a', perch=1, reach=.1, eye='-')],
        [], g='use', act=('spin', 'chute'))
    o.r('climb_the_wet_ladder', 'Climbing the wet ladder rung by rung with a wing on the rail and spray on his feathers', 26, 'wing',
        [k(.1, 'rung_lo', perch=1, reach=.4, x=.3, b=.5), k(.3, 'rung_lo', perch=1, reach=1, x=.7, y=-.7, b=-.7, l=1, mark='hup'), k(.5, 'deck_lo', perch=1, reach=1, x=.5, y=-.4, b=-.4, r=1), k(.7, 'deck_lo', perch=1, reach=.5, x=.3, y=.5, b=.4, eye='o', mark='drip'), k(.88, 'rung_lo', perch=1, reach=.2, x=.2, b=.4, eye='^')],
        [], g='use', act=('climb', 'ladder'), ages=GROWN)
    o.r('polish_the_ladder_rail', 'Polishing the wet ladder rail dry-bright with long wing strokes', 20, 'wing',
        [k(.1, 'rail_r', reach=.4, x=.2, y=.3), k(.28, 'rail_r', reach=1, x=.4, y=.5, b=.4, mark='squk'), k(.46, 'rail_l', reach=1, x=.5, y=-.3, b=-.4, l=1, mark='squk'), k(.66, 'rail_l', reach=1, x=.4, y=.6, b=.5, r=1), k(.86, eye='^')],
        [(.46, 'skim')], g='care', act=('polish', 'rail'), when=['obj_dirt>.4'])
    o.r('mop_the_floor_planks', 'Mopping the ground floor planks with his breast feathers until they stop shining wet', 22, 'none',
        [k(.1, 'floor_l', perch=1, x=.1, y=.5, b=1), k(.3, 'floor_l', perch=1, x=-.2, y=1, b=1.9, w=.5, mark='fwp'), k(.5, 'floor_r', perch=1, x=-.2, y=1, b=2, w=.6, mark='fwp'), k(.7, 'floor_r', perch=1, x=-.1, y=.6, b=1.1, eye='-'), k(.88, 'floor_r', perch=1, x=.1, b=.2, eye='^')],
        [(.5, 'flick')], g='care', act=('dry', 'floor'), when=['obj_wetness>.6'])
    o.r('scrape_ice_off_the_lane', 'Scraping an ice skin off the lane foot with the flat of a twig, from the lip up', 22, 'twig',
        [k(.12, 'lane_a', reach=.4, x=.3, y=.6, b=.3), k(.3, 'lane_a', reach=1, x=.6, y=.8, b=.6, mark='zrk'), k(.5, 'lane_m', reach=1, x=.6, y=.5, b=.4, r=1, mark='zrk'), k(.7, 'lane_c', reach=1, x=.5, y=.1, b=.2, l=1, mark='ZRK'), k(.88, eye='^')],
        [(.7, 'chip')], g='weather', act=('scrape', 'lane'), when=['frost>.4'])
    o.r('bail_the_full_pool', 'Bailing an over-full pool back from the brim with his bill, three scoops and a spit', 24, 'none',
        [k(.1, 'lip_l', perch=1, x=.4, y=.8, b=.5), k(.26, 'lip_l', perch=1, x=1.4, y=1.8, b=1.4, mark='glp'), k(.4, 'lip_l', perch=1, x=-.6, y=-.6, b=-.8, w=.5, mark='ptoo'), k(.58, 'lip_l', perch=1, x=1.5, y=1.9, b=1.5, l=1, mark='glp'), k(.78, 'lip_l', perch=1, x=-.5, y=-.5, b=-.7, w=.5, eye='>'), k(.92, 'lip_l', perch=1, x=.2, y=.3, b=.2, eye='-')],
        [(.58, 'bail')], g='weather', act=('scoop', 'pool'), when=['pool>.5'], say=["Bailed it. Pool refilled it. Pool has no manners.", "Three scoops. The pool didn't notice."])
    o.r('crouch_by_the_rail_from_wind', 'Crouching by the far rail with his neck down while the wind throws the spray sideways', 30, 'none',
        [k(.15, 'rail_r', x=-.4, y=.6, b=.8), k(.4, 'rail_r', x=-1, y=1.3, b=1.4, w=.6, eye='-'), k(.7, 'rail_r', x=-1.1, y=1.4, b=1.5, w=.7, eye='-', mark='brr'), k(.9, 'rail_r', x=-.3, y=.4, b=.4, eye='^')],
        [], g='weather', act=('shelter', 'rail'), when=['windy', 'wet'])
    o.r('warm_up_on_the_planks', 'Spreading his wings on the sun-hot floor planks to dry and soak it up', 28, 'none',
        [k(.12, 'floor_r', perch=1, x=.2, y=.4, b=.7), k(.34, 'floor_r', perch=1, x=.2, y=.9, b=1.5, w=1, eye='-'), k(.62, 'floor_l', perch=1, x=.2, y=1, b=1.6, w=1, eye='-', mark='ahh'), k(.86, 'floor_l', perch=1, x=.2, y=.3, b=.4, w=.3, eye='^')],
        [], g='weather', act=('warm', 'floor'), when=['sun'])
    o.r('shake_off_the_spray', 'Shaking the spray out of his feathers with a full-body rattle at the foot of the chute', 18, 'none',
        [k(.12, 'lane_a', x=.2, y=.4, b=.3), k(.3, 'lane_a', x=-.3, y=-.8, b=-1.2, w=1, l=1, mark='brrrt'), k(.46, 'lane_a', x=.4, y=.9, b=1.4, w=.6, r=1, mark='brrrt'), k(.66, 'lane_a', x=-.4, y=-.9, b=-1.3, w=1, mark='BRRT'), k(.86, x=.1, eye='^')],
        [], g='weather', act=('fluff', 'feathers'), when=['wet'])
    o.r('sniff_the_pool_edge', 'Sniffing around the pool brim with his bill an inch off it, suspicious of the water', 20, 'none',
        [k(.1, 'lip_r', perch=1, x=.6, y=1, b=.7), k(.3, 'lip_r', perch=1, x=1.3, y=1.5, b=1.2, mark='snf'), k(.5, 'pool_l', perch=0, x=1.4, y=1.7, b=1.3, mark='snf'), k(.7, 'lip_r', perch=1, x=1.2, y=1.4, b=1.1, eye='o'), k(.9, 'lip_r', perch=1, x=.2, b=.2, eye='>')],
        [], g='test', act=('sniff', 'pool'), prefer=['curious'])
    o.r('listen_at_the_chute_foot', 'Holding his head to the chute foot and listening to the water rushing from far up', 22, 'none',
        [k(.12, 'lane_a', x=.4, y=.5, b=.2), k(.3, 'lane_a', x=1, y=1.1, b=.5, eye='o'), k(.5, 'lane_a', x=1.2, y=1.2, b=.6, eye='O', mark='shhhh'), k(.72, 'lane_b', x=1, y=-.1, b=-.1, w=.4, eye='@'), k(.9, eye='>')],
        [], g='test', act=('listen', 'chute'), when=['wet'])
    o.r('ring_the_ladder_rail', 'Ringing the ladder rail with a bill-tap and holding an ear to the hum', 20, 'none',
        [k(.1, 'rail_l', x=.5, y=.9, b=.6), k(.26, 'rail_l', x=1.5, y=-.4, b=-.9, mark='TING'), k(.42, 'rail_l', x=-.5, y=1, b=1, eye='O', mark='TING'), k(.62, 'rail_l', x=-1.2, y=-1.2, b=-1.3, eye='o', mark='...'), k(.84, eye='-')],
        [], g='test', act=('ring', 'rail'), prefer=['curious'])
    o.r('measure_the_pool_across', 'Pacing the brim with a wing held out to guess the pool width, getting different answers each way', 26, 'wing',
        [k(.1, 'lip_l', perch=1, reach=.5, x=.2, b=.2, l=1), k(.3, 'lip_l', perch=1, reach=1, x=.4, y=.3, b=.1, r=1, mark='..9'), k(.52, 'lip_r', perch=1, reach=1, x=.4, y=.3, b=.1, l=1, mark='..13'), k(.74, 'lip_r', perch=1, reach=.6, x=.2, y=.5, b=.3, r=1, eye='@'), k(.9, 'lip_r', perch=1, reach=.1, eye='-')],
        [], g='test', act=('measure', 'pool'))
    o.r('dance_on_the_floor_planks', 'Dancing a damp little shuffle across the floor planks, slipping on the beat', 24, 'none',
        [k(.1, 'floor_l', perch=1, x=.8, y=.6, b=.9, l=1), k(.3, 'floor_l', perch=1, x=-.5, y=-.9, b=-1.1, r=1, w=.6), k(.5, 'floor_r', perch=1, x=.9, y=.9, b=1.2, l=1, w=1), k(.7, 'floor_r', perch=1, x=-.6, y=-1.1, b=-1.3, r=1, l=1, w=.7, eye='^'), k(.9, 'floor_r', perch=1, x=.3, b=.3)],
        [], g='play', act=('dance', 'floor'), prefer=['happy'])
    o.r('hop_the_mist_marks', 'Hopping from mist mark to mist mark along the pool front, never landing twice on one', 22, 'none',
        [k(.1, 'mist_a', x=.4, b=-.6, l=1, r=1), k(.28, 'mist_b', x=.9, b=-1.2, w=1, mark='hup'), k(.46, 'mist_a', x=.9, b=-1.4, w=1), k(.66, 'ripple_b', x=1, b=-1.3, w=1, mark='HUP'), k(.86, 'mist_b', x=.2, b=.3, eye='@')],
        [], g='play', act=('hop', 'mist'), prefer=['young', 'happy'])
    o.r('wait_by_the_ladder_for_company', 'Waiting at the ladder foot for company that is late again, glancing up and down', 28, 'none',
        [k(.12, 'rail_l', x=-.3, y=-.9, b=-.7, w=.3), k(.34, 'rung_lo', x=.2, y=-1.6, b=-1.3, eye='o', mark='...'), k(.56, 'rail_l', x=.5, y=1.2, b=1, l=1, eye='-'), k(.8, 'rung_lo', x=.1, y=-1.5, b=-1.4, r=1, eye='o', w=.5), k(.94, eye='>')],
        [], g='rest', act=('wait', 'ladder'), prefer=['lonely'])
    o.r('sulk_at_the_pool_edge', 'Sulking at the pool edge with his reflection, which sulks back', 26, 'none',
        [k(.15, 'lip_l', perch=1, x=.5, y=1, b=.8), k(.4, 'lip_l', perch=1, x=1, y=1.6, b=1.4, eye='-'), k(.7, 'lip_l', perch=1, x=1.1, y=1.7, b=1.5, eye='-', mark='hmph'), k(.9, 'lip_l', perch=1, x=.3, y=.4, b=.3, eye='^')],
        [], g='rest', act=('sulk', 'brim'), prefer=['sad', 'grumpy'], say=["Reflection sulks better. Rude.", "Not talking. To water. To anyone."])
    o.r('sit_on_the_floor_boards', 'Sitting on the floor boards with the spray misting his back, wings drooped', 28, 'none',
        [k(.15, 'floor_l', perch=1, x=.3, b=.5), k(.38, 'floor_l', perch=1, x=.4, y=.6, b=1.2, w=.3, eye='o'), k(.64, 'floor_r', perch=1, x=.4, y=.5, b=1.4, w=.4, eye='-', mark='sigh'), k(.88, 'floor_r', perch=1, x=.3, y=.2, b=.4, eye='^')],
        [], g='rest', act=('sit', 'floor'), prefer=['tired'])
    o.r('kick_the_ladder_rail', 'Kicking the ladder rail, regretting it, and hopping a circle round the planks', 18, 'none',
        [k(.12, 'rail_r', x=.4, y=.5, b=.3), k(.3, 'rail_r', x=.7, y=.9, b=-.5, l=1, mark='tak'), k(.46, 'rail_r', x=-.4, y=-.6, b=-1.5, l=1, w=1, eye='O', mark='OW'), k(.66, 'floor_r', x=-.9, y=1.1, b=.5, r=1, eye='@'), k(.88, eye='>')],
        [(.46, 'thud')], g='mishap', act=('kick', 'rail'), prefer=['grumpy'])
    o.r('tumble_off_the_floor_edge', 'Tumbling off the floor edge in a flap of wings and landing flat on his bill', 20, 'none',
        [k(.12, 'floor_r', perch=1, x=.2, b=.3), k(.3, 'floor_r', perch=1, x=1.1, y=1, b=-1, w=1, mark='whoa'), k(.5, 'floor_r', perch=1, x=-1.3, y=-1.6, b=1.9, w=1, l=1, r=1, eye='O', mark='SPLAT'), k(.74, 'floor_r', perch=1, x=.7, y=1.5, b=1.2, eye='@'), k(.9, 'floor_r', perch=1, x=.3, b=.3, eye='>')],
        [(.5, 'bruise')], g='mishap', act=('fold', 'floor'), say=["Fell off a floor. How. Don't answer.", "Bill first into the damp. Salty. Not salty."])
    o.r('hook_a_wing_on_the_foot_bolt', 'Hooking a wing round the foot bolt and flapping until it lets go', 22, 'wing',
        [k(.12, 'foot_bolt', reach=.5, x=.2, y=.3), k(.3, 'foot_bolt', reach=1, x=.4, y=.1, b=.3, mark='hm'), k(.5, 'foot_bolt', reach=1, x=-.6, y=-.4, b=-.9, l=1, r=1, eye='O', mark='MPH'), k(.7, 'foot_bolt', reach=1, x=-1, y=-.7, b=-1.3, eye='@', mark='POP'), k(.9, x=.2, eye='-')],
        [], g='mishap', act=('hook', 'bolt'))
    o.r('pose_at_the_pool_edge', 'Posing at the pool edge, chest out, one foot up as if the water were applauding', 18, 'none',
        [k(.14, 'lip_r', perch=1, x=.5, y=.4, b=.5), k(.4, 'lip_r', perch=1, x=-.9, y=-1.2, b=-1.6, w=.4, r=1, eye='^'), k(.66, 'lip_r', perch=1, x=1, y=-1.4, b=-1.3, w=.9, l=1), k(.9, 'lip_r', perch=1, x=.3, b=.2)],
        [], g='show', act=('pose', 'brim'), prefer=['happy'])
    o.r('present_the_water_slide', 'Presenting the chute, tower and pool with one grand sweep of both wings, like a hotel owner', 26, 'wing',
        [k(.1, 'floor_l', perch=1, reach=.3, x=.1, y=-.4, b=-.3), k(.32, 'rail_l', reach=1, x=.1, y=-.8, b=-.5, mark='behold'), k(.56, 'lane_c', reach=1, x=.1, y=-1, b=-.8, l=1), k(.8, 'lip_r', perch=1, reach=.4, x=.2, y=-.3, b=-.2, eye='^')],
        [], g='show', act=('present', 'slide'), say=["Pool, slide, floor. Rates negotiable.", "Look at all this. Mine. Bring a towel."])
    o.r('sing_to_the_chute_echo', 'Singing at the chute foot, then answering his own echo in a second voice', 24, 'none',
        [k(.12, 'lane_a', x=.9, y=.8, b=.9), k(.3, 'lane_a', x=1.8, y=-1.4, b=-1.2, w=.5, mark='LAAA'), k(.5, 'lane_b', x=-.4, y=-1.7, b=-1.6, w=1, eye='^', mark='laaa'), k(.72, 'lane_a', x=1.5, y=.9, b=.9, eye='o', mark='la?'), k(.9, eye='-')],
        [], g='show', act=('sing', 'chute'), prefer=['lonely'])
    o.r('compare_the_ripple_rows', 'Comparing the two ripple rows against each other, head swinging from one to the other', 24, 'none',
        [k(.12, 'ripple_a', x=.5, y=.6, b=.3), k(.32, 'ripple_a', x=1, y=1.2, b=.7, eye='o'), k(.52, 'mist_a', x=1, y=1.2, b=.7, eye='O'), k(.72, 'ripple_b', x=.9, y=.4, b=.2, eye='-', mark='hm'), k(.9, 'mist_b', x=.5, y=.9, b=.5, eye='>')],
        [], g='show', act=('compare', 'ripples'), prefer=['curious'])
    o.emit()


def water_slide_mega():
    # Drawing (116 x 82 cells, 8.1 px a row, standing line row 78): the tall tower (decks every 5 rows from row 76: 16, 57, 97, 138 px) on the left,
    # no ground floor, then the long chute coming down at the right, cols 88-106, a bolt at row 72 (col 92, 49 px) and one low at row 76 (col 101, 16 px),
    # spray `~` above the mouth (row 70, 65 px), and a deeper, wider pool: front brim `(` cols 65-70 and `)` cols 106-111, ripple dashes `--` on
    # row 75 (cols 73, 87, 101) and mist `~~` on row 76 (cols 80, 94). He works the brim, the foot bolts and the lane mouths.
    P = pm('water_slide_mega')
    o = Obj('water_slide_mega', 'placed',
            fields=dict(pool=(0, 0, 1), frost=(0, 0, 1), roar=(0, 0, 1)),
            physics=[('pool', 'rate', .0015, 'wet'), ('pool', 'rate', -.0008, 'sun'), ('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'),
                     ('roar', 'rate', .003, 'storm'), ('roar', 'rate', -.001, 'calm')],
            effects=dict(skim=[('obj.dirt', 'add', -.25)], polish=[('obj.dirt', 'add', -.15)], blot=[('obj.wetness', 'add', -.3)], tighten=[('obj.condition', 'add', .2)],
                         dent=[('obj.condition', 'add', -.15)], sluice=[('obj.wetness', 'add', .2), ('pool', 'add', -.2)], scrape=[('frost', 'mul', .2)],
                         soak=[('obj.dirt', 'add', .12)], bail=[('pool', 'add', -.3)], bruise=[('obj.dirt', 'add', .14)], hush=[('roar', 'mul', .3)], laugh=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(rung_lo=P(9, 76, 'surface'), rail_l=P(8, 73), deck_lo=P(17, 76, 'surface'), deck_lo2=P(25, 76, 'surface'), post_r=P(27, 78), pool_l=P(65, 75),
                         lip_l=P(67, 77, 'surface'), lip_r=P(109, 77, 'surface'), pool_r=P(111, 75), ripple_a=P(73, 75), ripple_b=P(87, 75), ripple_c=P(102, 75),
                         mist_a=P(80, 76), mist_b=P(94, 76), foot_bolt=P(101, 76), bolt_hi=P(92, 72), spray=P(88, 70), lane_a=P(96, 74, 'surface'), lane_b=P(99, 72, 'surface'), lane_c=P(92, 69), lane_m=P(100, 75, 'surface')))
    # ---------------- care
    o.r('skim_the_deep_side', 'Skimming the deep side of the pool with a wing, brim to brim in four strokes', 24, 'wing',
        [k(.1, 'lip_l', perch=1, reach=.5, x=.3, y=.7, b=.2), k(.26, 'ripple_a', reach=1, x=.7, y=1.2, b=.8, l=1, mark='shf'), k(.42, 'ripple_b', reach=1, x=.7, y=1.2, b=.8, r=1, mark='shf'),
         k(.58, 'ripple_c', reach=1, x=.7, y=1.2, b=.8, l=1, mark='shf'), k(.76, 'pool_r', reach=1, x=.5, y=.9, b=.4, r=1), k(.92, eye='^')],
        [(.76, 'skim')], g='care', act=('sweep', 'pool'), when=['obj_dirt>.3'],
        say=["Clean pool. Too big to show off.", "Four strokes. Pool is a lot."])
    o.r('polish_the_low_bolt', 'Buffing the low foot bolt with a wing until it shines back at him', 18, 'wing',
        [k(.12, 'foot_bolt', reach=.5, x=.4, y=.7, b=.3), k(.3, 'foot_bolt', reach=1, x=.7, y=1, b=.7, mark='rub'), k(.5, 'foot_bolt', reach=1, x=.6, y=.9, b=.6, l=1, mark='rub'), k(.7, 'foot_bolt', reach=1, x=.5, y=1.1, b=.8, r=1), k(.9, eye='^')],
        [(.5, 'polish')], g='care', act=('polish', 'bolt'), when=['obj_dirt>.4'])
    o.r('blot_the_brim_dry', 'Blotting the pool brim with his own breast feathers, back and forth', 20, 'none',
        [k(.1, 'lip_l', perch=1, x=.2, y=.4, b=.6), k(.3, 'lip_l', perch=1, x=.1, y=.9, b=1.6, w=.5, mark='fwp'), k(.5, 'lip_r', perch=1, x=.1, y=.9, b=1.6, w=.5, mark='fwp'), k(.78, 'lip_r', perch=1, x=.2, y=.3, b=.7, eye='-')],
        [(.5, 'blot')], g='care', act=('dry', 'brim'), when=['obj_wetness>.5'])
    o.r('crank_the_high_bolt', 'Cranking the high foot bolt round with his bill, eyes screwed shut', 22, 'none',
        [k(.1, x=.5, y=-.2, b=-.3), k(.28, 'bolt_hi', x=1.5, y=-1, b=-.6, eye='-', mark='kr'), k(.46, 'bolt_hi', x=1.6, y=-1.1, b=-.7, eye='-', l=1, mark='kr'), k(.64, 'bolt_hi', x=1.7, y=-1.2, b=-.9, eye='-', r=1, mark='KR'), k(.84, x=.4, y=.4, b=.2, eye='^')],
        [(.64, 'tighten')], g='care', act=('tug', 'bolt'), when=['obj_condition<.6'], ages=GROWN,
        say=["Cranked it. My neck now has a corner.", "Bolt tight. Jaw loose."])
    o.r('scrape_ice_from_the_lane_mouth', 'Scraping the frost crust off the lane mouth with a twig, all arm', 22, 'twig',
        [k(.12, 'lane_c', reach=.4, x=.3, y=-.3, b=-.3), k(.3, 'lane_c', reach=1, x=.5, y=-.6, b=-.6, mark='skrk'), k(.5, 'lane_b', reach=1, x=.6, y=-.4, b=-.4, r=1, mark='skrk'), k(.7, 'lane_a', reach=1, x=.7, y=.5, b=.4, l=1, mark='SKRK'), k(.9, eye='^')],
        [(.7, 'scrape')], g='weather', act=('scrape', 'lane'), when=['frost>.3'])
    o.r('hush_the_roar', 'Slapping the lane mouth to quiet the storm roar down its throat', 24, 'wing',
        [k(.12, 'lane_a', reach=.4, x=.3, y=.5, b=.2), k(.3, 'lane_a', reach=1, x=-.3, y=-.5, b=-.7, w=1, mark='SLAP'), k(.5, 'lane_b', reach=1, x=-.2, y=-.6, b=-.8, r=1, mark='SLAP'), k(.7, 'lane_a', reach=.5, x=.4, y=.4, b=.2, eye='-', mark='shh'), k(.9, eye='^')],
        [(.5, 'hush')], g='weather', act=('press', 'lane'), when=['roar>.3'], prefer=['grumpy'],
        say=["Roar quit. Slapped it into silence.", "Shh. Slide. Shh. Please."])
    # ---------------- use / test
    o.r('sniff_the_pool', 'Sniffing along the pool brim for anything rotten, bill working left to right', 20, 'none',
        [k(.1, 'lip_l', perch=1, x=.5, y=.9, b=.6), k(.3, 'lip_l', perch=1, x=1.1, y=1.2, b=.9, mark='snf'), k(.5, 'lip_l', perch=1, x=1.2, y=1.3, b=1, eye='-', mark='snf'), k(.7, 'lip_r', perch=1, x=1.2, y=1.3, b=1, eye='o', mark='...'), k(.9, 'lip_r', perch=1, x=.2, y=.4, b=.2, eye='>')],
        [], g='test', act=('sniff', 'pool'), prefer=['curious'],
        say=["Smells like money and cheap towels.", "Chlorine. Or somebody's excuses."])
    o.r('pace_out_the_brim', 'Pacing out the brim heel to toe with his wing out for balance, counting under his breath', 26, 'wing',
        [k(.1, 'lip_l', perch=1, reach=.5, x=.2, b=.2, l=1), k(.3, 'lip_l', perch=1, reach=1, x=.4, y=.3, b=.1, r=1, mark='...12'), k(.5, 'lip_r', perch=1, reach=1, x=.4, y=.3, b=.1, l=1, mark='..40'), k(.7, 'lip_r', perch=1, reach=.6, x=.2, y=.5, b=.2, r=1, eye='@', mark='ish'), k(.9, 'lip_r', perch=1, reach=.1, x=.1, b=0)],
        [], g='test', act=('measure', 'brim'), prefer=['curious'])
    o.r('listen_at_the_lane', 'Pressing his bill against the lane and hearing the whole roar from far up', 22, 'none',
        [k(.12, 'lane_a', x=.4, y=.5, b=.2), k(.3, 'lane_a', x=1, y=1, b=.5, eye='o'), k(.5, 'lane_a', x=1.1, y=1, b=.6, eye='O', mark='RRRR'), k(.7, 'lane_b', x=1, y=-.2, b=-.2, w=.4, eye='@'), k(.9, x=-.5, y=.3, eye='>')],
        [], g='test', act=('listen', 'lane'), when=['wet'], prefer=['curious'])
    o.r('kick_a_wave_across', 'Kicking the pool across the brim with a flat foot, left, right, left', 20, 'none',
        [k(.1, 'lip_l', perch=1, x=.2, b=.1), k(.28, 'lip_l', perch=1, x=.5, y=.3, b=-.3, l=1, mark='sploosh'), k(.46, 'lip_l', perch=1, x=.6, y=.3, b=-.4, r=1, mark='sploosh'), k(.66, 'ripple_a', perch=0, x=.8, y=.4, b=-.5, l=1, w=1, mark='SPLOOSH'), k(.88, 'lip_l', perch=1, x=.2, b=.2, eye='^')],
        [(.46, 'sluice'), (.66, 'laugh')], g='play', act=('kick', 'water'), when=['pool>.3'], prefer=['happy'],
        say=["Waves made. Arrangements for a flood pending.", "Kick. Flood. Damage. Fine."])
    o.r('hop_the_mist_patches', 'Hopping from mist patch to mist patch along the pool front, four hops', 22, 'none',
        [k(.1, 'mist_a', x=.4, b=-.5, l=1, r=1), k(.28, 'mist_b', x=.9, b=-1.2, w=1, mark='hup'), k(.46, 'mist_a', x=.9, b=-1.3, w=1, mark='hup'), k(.64, 'mist_b', x=1, b=-1.4, w=1, mark='HUP'), k(.84, 'ripple_b', x=.2, b=.3, eye='@')],
        [], g='play', act=('hop', 'mist'), prefer=['young', 'happy'])
    o.r('dance_on_the_lower_deck', 'Dancing a stiff little two-step on the lower deck board', 24, 'none',
        [k(.1, 'deck_lo', perch=1, x=.2, b=.3, l=1), k(.28, 'deck_lo', perch=1, x=.3, y=.3, b=-.5, r=1, w=1), k(.46, 'deck_lo2', perch=1, x=.3, y=.3, b=.5, l=1, w=.4), k(.64, 'deck_lo2', perch=1, x=.2, y=-.3, b=-.6, r=1, w=1, eye='^'), k(.86, 'deck_lo', perch=1, x=.2, b=.1, w=0)],
        [(.64, 'laugh')], g='play', act=('dance', 'deck'), prefer=['happy'],
        say=["Left foot. Right foot. Nailed it.", "Dance floor was a plank. Still counts."])
    o.r('sit_on_the_far_brim', 'Sitting at the far brim, chin down, feeling very small next to the pool', 28, 'none',
        [k(.15, 'lip_r', perch=1, x=.2, b=.6), k(.4, 'lip_r', perch=1, x=.5, y=.7, b=1.3, eye='o'), k(.65, 'lip_r', perch=1, x=.5, y=.7, b=1.4, eye='-', mark='...'), k(.88, 'lip_r', perch=1, x=.2, y=.3, b=.4, eye='^')],
        [(.65, 'rest')], g='rest', act=('sit', 'brim'), prefer=['sad'])
    o.r('lean_on_the_ladder_post', 'Propped against the far ladder post, bill tucked, a whole slide away from the water', 26, 'none',
        [k(.14, 'post_r', x=-.3, b=-.2), k(.4, 'post_r', x=-1, y=-.6, b=-1, r=1), k(.66, 'post_r', x=-1.2, y=-.3, b=.6, eye='-', mark='hm'), k(.9, 'post_r', x=-.3, b=0, eye='^')],
        [(.66, 'rest')], g='rest', act=('lean', 'post'))
    o.r('skid_on_the_brim', 'Skidding down the wet brim on both feet, wings windmilling', 18, 'none',
        [k(.12, 'lip_l', perch=1, x=.3, b=.1), k(.3, 'lip_l', perch=1, x=1, y=.6, b=-.9, w=1, l=1, r=1, mark='whoa'), k(.5, 'lip_r', perch=1, x=1.8, y=1.7, b=1.5, w=1, eye='O', mark='CRASH'), k(.8, 'lip_r', perch=1, x=.4, y=1.4, b=1.2, eye='@')],
        [(.5, 'soak')], g='mishap', act=('slip', 'brim'), when=['obj_wetness>.4'],
        say=["Brim won. Brim always wins.", "Down. Skid. Wet. Fine."])
    o.r('wedged_in_the_big_lane', 'Peering down the big lane mouth head first and wedging his shoulders', 26, 'none',
        [k(.12, x=.5, y=-.3), k(.3, 'lane_a', x=1.3, y=.5, b=.8), k(.5, 'lane_a', x=1.5, y=.6, b=1.1, l=1, r=1, eye='O', mark='mph'), k(.72, 'lane_a', x=1.7, y=.4, b=1.3, w=1, mark='POP'), k(.9, x=2, y=1, b=.6, eye='@')],
        [(.72, 'soak')], g='mishap', act=('stuck', 'lane'), shown='head', prefer=['young'])
    o.r('crash_against_the_high_bolt', 'Jumping for the high foot bolt and denting himself off the rebound', 20, 'none',
        [k(.1, 'bolt_hi', x=.3, y=.6, b=1), k(.3, 'bolt_hi', x=.5, y=-.4, b=-1.6, w=1, mark='hup'), k(.46, 'bolt_hi', x=1.4, y=-1, b=-1.8, w=1, eye='O', mark='TANG'), k(.66, x=-1.2, y=1.3, b=.9, r=1, eye='@'), k(.9, eye='>')],
        [(.46, 'dent')], g='mishap', act=('knock', 'bolt'), ages=GROWN,
        say=["Bolt rang like a bell. So did my skull.", "Dented the bolt. Or my plans. Can't tell."])
    o.r('wait_at_the_ladder_foot', 'Waiting at the ladder foot, glancing up the tower and then at his own feet', 30, 'none',
        [k(.12, 'rail_l', x=.1, y=-.6, b=-.4), k(.3, 'rung_lo', x=.3, y=-1.2, b=-.8, eye='o', mark='...'), k(.5, 'rail_l', x=.1, y=.8, b=.5, eye='-', l=1), k(.7, 'rung_lo', x=.2, y=-1.3, b=-.9, eye='o', r=1), k(.9, x=-.2, y=.3, b=.2, eye='>')],
        [], g='rest', act=('wait', 'ladder'), prefer=['lonely'],
        say=["Nobody is coming down. I am not a patient duck.", "Waited for the queue. There is no queue."])
    o.r('present_the_pool', 'Presenting the whole pool with a sweep of both wings, like a showroom', 24, 'wing',
        [k(.12, 'lip_l', perch=1, reach=.3, x=.1, y=-.4, b=-.3), k(.34, 'ripple_a', perch=0, reach=1, x=.1, y=-.7, b=-.6, mark='behold'), k(.56, 'ripple_c', reach=1, x=.1, y=-.7, b=-.6, l=1), k(.8, 'lip_r', perch=1, reach=.4, x=.2, y=-.2, b=-.2, eye='^')],
        [], g='show', act=('present', 'pool'), prefer=['happy'],
        say=["Pool. Mine. Admission is bread.", "Showed it to nobody. Nobody was impressed."])
    o.r('sing_over_the_spray', 'Singing at the spray mouth, mostly to hear himself bounce back', 24, 'none',
        [k(.12, 'spray', x=.2, y=-.5, b=-.3), k(.3, 'spray', x=.9, y=-1.4, b=-1.1, w=.8, mark='LAAA'), k(.5, 'spray', x=1, y=-1.5, b=-1.2, w=1, eye='^', mark='LAAAA'), k(.72, 'spray', x=.3, y=-.5, b=-.4, eye='o', mark='la?'), k(.9, eye='-')],
        [], g='show', act=('sing', 'spray'), prefer=['lonely'],
        say=["Echo sings flat. Typical for a tenant.", "Held a note for two seconds. Record."])
    o.r('pose_on_the_deck', 'Striking a hero pose on the lower deck board, chest out to the pool', 18, 'none',
        [k(.14, 'deck_lo2', perch=1, x=.2, b=-.3), k(.4, 'deck_lo2', perch=1, x=-.4, y=-.7, b=-1.1, w=.8, l=1), k(.66, 'deck_lo2', perch=1, x=-.6, y=-1, b=-1.3, w=1, r=1, l=1, eye='^'), k(.9, 'deck_lo2', perch=1, x=.2, b=-.2)],
        [], g='show', act=('pose', 'deck'), prefer=['happy'])
    # ---------------- v3 top-up
    o.r('roll_down_the_mega_run', 'Rolling down the lower run like a barrel with his wings pinned, a long way round to the spray', 22, 'none',
        [k(.12, 'lane_b', perch=1, x=.2, b=.4), k(.3, 'lane_b', perch=1, x=.3, y=1.4, b=2, eye='-', mark='brrr'), k(.52, 'lane_a', perch=1, x=.5, y=1.7, b=2.3, l=1, r=1, mark='wub wub'), k(.76, 'lane_m', perch=1, x=1.1, y=2.1, b=1.7, eye='@'), k(.92, 'lane_m', perch=1, x=.2, y=.4, b=.4, eye='^')],
        [], g='use', act=('roll', 'run'), ages=GROWN, prefer=['happy'])
    o.r('dive_down_the_big_run', 'Diving down the big run headfirst with his bill leading and his wings swept flat', 22, 'none',
        [k(.12, 'lane_b', perch=1, x=.6, y=1, b=.7), k(.3, 'lane_b', perch=1, x=2.1, y=2.3, b=1.1, w=.4, eye='>', mark='AAAAH'), k(.52, 'lane_a', perch=1, x=2.5, y=2.8, b=1.4, w=.7), k(.76, 'lane_m', perch=1, x=2.7, y=3, b=1.7, eye='O', mark='SPLOOSH'), k(.9, 'lane_m', perch=1, x=.7, y=1.1, b=.7, eye='@')],
        [], g='use', act=('race', 'lane'), ages=GROWN, say=["Dived. Survived. Immediately undid both.", "Biggest slide, smallest regrets."])
    o.r('reverse_down_the_run', 'Reversing down the run on his tail with his feet pedalling up at the sky', 24, 'none',
        [k(.12, 'lane_b', perch=1, x=-.7, y=-.9, b=-.9, w=.5), k(.32, 'lane_b', perch=1, x=-1.7, y=-1.6, b=-1.5, l=1, w=.8, eye='-'), k(.54, 'lane_a', perch=1, x=-2.1, y=-2, b=-1.9, r=1, w=1), k(.78, 'lane_m', perch=1, x=-1.1, y=.6, b=1.3, eye='@'), k(.92, 'lane_m', perch=1, x=.1, b=.1, eye='-')],
        [], g='use', act=('drag', 'run'), ages=GROWN)
    o.r('brake_with_both_feet', 'Braking mid-run with both feet flat against the lane, sliding the last stretch on a squeal', 22, 'none',
        [k(.12, 'lane_b', perch=1, x=.5, b=.5), k(.3, 'lane_a', perch=1, x=.9, y=.5, b=-1.2, l=1, r=1, w=.9, mark='SKREEEE'), k(.5, 'lane_a', perch=1, x=-1, y=-.4, b=-1.4, l=1, r=1, w=1, eye='O'), k(.74, 'lane_m', perch=1, x=.7, y=1.1, b=1, eye='-', mark='phew'), k(.9, 'lane_m', perch=1, x=.2, b=.2, eye='^')],
        [], g='use', act=('brace', 'run'), ages=GROWN)
    o.r('whirl_down_the_run', 'Whirling down the run flat as a coin with a wing out, spraying his own spin around him', 24, 'wing',
        [k(.12, 'lane_b', perch=1, reach=.3, x=.1, b=.3), k(.3, 'lane_a', perch=1, reach=1, x=-.5, y=.6, b=.9, l=1), k(.52, 'lane_a', perch=1, reach=1, x=.8, y=1.2, b=1.3, r=1, mark='fwsh'), k(.74, 'lane_m', perch=1, reach=1, x=-.9, y=1.5, b=1.5, l=1, eye='@'), k(.9, 'lane_m', perch=1, reach=.1, eye='-')],
        [], g='use', act=('spin', 'run'), ages=GROWN)
    o.r('climb_the_mega_ladder', 'Climbing the big ladder rung by rung with a wing on the rail, then hopping off at the first deck', 28, 'wing',
        [k(.1, 'rung_lo', perch=1, reach=.4, x=.3, b=.5), k(.3, 'rung_lo', perch=1, reach=1, x=.8, y=-.8, b=-.8, l=1, mark='hup'), k(.5, 'deck_lo', perch=1, reach=1, x=.6, y=-.5, b=-.5, r=1), k(.7, 'deck_lo2', perch=1, reach=.5, x=.3, y=.5, b=.4, eye='o'), k(.88, 'rung_lo', perch=1, reach=.2, x=.2, b=.4, eye='^')],
        [], g='use', act=('climb', 'ladder'))
    o.r('scrub_the_rungs', 'Scrubbing the big ladder rungs with a wing one by one, skipping none and grumbling about all', 24, 'wing',
        [k(.1, 'rung_lo', reach=.7, x=.6, y=.8, b=.6), k(.28, 'rung_lo', reach=1, x=1.1, y=1.2, b=1.1, mark='skrk'), k(.46, 'rail_l', reach=1, x=-.3, y=-.9, b=-1.2, l=1, mark='skrk'), k(.66, 'rung_lo', reach=1, x=1.2, y=1.3, b=1.2, r=1, mark='skrk'), k(.86, eye='^')],
        [(.46, 'polish')], g='care', act=('scrub', 'rungs'), when=['obj_dirt>.3'])
    o.r('blot_the_bolts_dry', 'Blotting the foot bolts dry with a wing, the low one first and the high one on tiptoe', 22, 'wing',
        [k(.1, 'foot_bolt', reach=.5, x=.3, y=.5, b=.3), k(.3, 'foot_bolt', reach=1, x=.6, y=.7, b=.7, mark='fwp'), k(.52, 'bolt_hi', reach=1, x=.6, y=-.4, b=-.8, l=1, mark='fwp'), k(.74, 'bolt_hi', reach=.5, x=.3, y=-.2, b=-.3, r=1), k(.9, eye='-')],
        [(.52, 'blot')], g='care', act=('wipe', 'bolt'), when=['obj_wetness>.5'])
    o.r('chip_ice_off_the_brim', 'Chipping a frozen rind off the near brim with his bill, then kicking the lumps away', 22, 'none',
        [k(.1, 'lip_l', perch=1, x=.4, y=.8, b=.6), k(.28, 'lip_l', perch=1, x=.9, y=1.5, b=1.1, mark='tk'), k(.46, 'lip_r', perch=1, x=.9, y=1.5, b=1.1, l=1, mark='tk'), k(.66, 'lip_r', perch=1, x=.5, y=.9, b=.4, r=1, mark='tsh'), k(.86, 'lip_r', perch=1, x=.2, y=.2, b=.1, eye='^')],
        [(.46, 'scrape')], g='weather', act=('chip', 'brim'), when=['frost>.3'])
    o.r('bail_the_overflow', 'Bailing the overflow back into the pool with his bill, scoop after scoop', 26, 'none',
        [k(.1, 'lip_r', perch=1, x=.4, y=.8, b=.5), k(.26, 'lip_r', perch=1, x=1.4, y=1.8, b=1.4, mark='glp'), k(.4, 'lip_r', perch=1, x=-.6, y=-.6, b=-.8, w=.5, mark='ptoo'), k(.58, 'lip_r', perch=1, x=1.5, y=1.9, b=1.5, l=1, mark='glp'), k(.76, 'lip_r', perch=1, x=-.5, y=-.5, b=-.7, w=.5, eye='>'), k(.92, 'lip_r', perch=1, x=.2, y=.3, b=.2, eye='-')],
        [(.58, 'bail')], g='weather', act=('scoop', 'pool'), when=['pool>.5'])
    o.r('huddle_by_the_post_in_spray', 'Huddling by the far post with the storm spray flying sideways past him', 30, 'none',
        [k(.15, 'post_r', x=.8, y=-.3, b=.2, l=1), k(.4, 'post_r', x=-1.4, y=2.2, b=2.4, w=.9, eye='-'), k(.7, 'post_r', x=-1.5, y=2.3, b=2.5, w=.3, r=1, eye='-', mark='brr'), k(.9, 'post_r', x=.6, y=-.2, b=.2, eye='^')],
        [], g='weather', act=('shelter', 'post'), when=['windy'])
    o.r('bask_on_the_deck_board', 'Spreading both wings on the sun-lit deck board and letting the heat dry him', 28, 'none',
        [k(.12, 'deck_lo', perch=1, x=.7, y=-.3, b=-.3), k(.34, 'deck_lo', perch=1, x=-.5, y=1.4, b=2, w=.6, eye='-'), k(.62, 'deck_lo2', perch=1, x=-.5, y=1.5, b=2.1, w=1, eye='-', mark='ahh'), k(.86, 'deck_lo2', perch=1, x=.6, y=-.4, b=-.3, w=.2, eye='^')],
        [], g='weather', act=('warm', 'deck'), when=['sun'])
    o.r('rattle_the_spray_off', 'Rattling the spray off his feathers at the foot of the run, wings snapping', 18, 'none',
        [k(.12, 'lane_m', x=.2, y=.5, b=.4), k(.3, 'lane_m', x=-.3, y=-.9, b=-1.3, w=1, l=1, mark='brrt'), k(.46, 'lane_m', x=.4, y=1, b=1.5, w=.6, r=1, mark='brrt'), k(.66, 'lane_m', x=-.4, y=-1, b=-1.4, w=1, mark='BRRT'), k(.86, x=.1, eye='^')],
        [], g='weather', act=('fluff', 'feathers'), when=['wet'])
    o.r('ring_the_ladder_rail', 'Ringing the ladder rail with the tip of his bill and holding still for the hum', 20, 'none',
        [k(.1, 'rail_l', x=.6, y=.9, b=.7), k(.26, 'rail_l', x=1.6, y=-.5, b=-1, mark='TANG'), k(.42, 'rail_l', x=-.6, y=1.1, b=1.1, eye='O', mark='TANG'), k(.62, 'rail_l', x=-1.3, y=-1.3, b=-1.4, eye='o', mark='...'), k(.84, eye='-')],
        [], g='test', act=('ring', 'rail'))
    o.r('peer_up_the_mega_tower', 'Tilting his head back to size up the tower, then backing off to see the top', 24, 'none',
        [k(.12, 'rung_lo', x=.1, y=-.5, b=-.4), k(.34, 'rung_lo', x=.2, y=-1.7, b=-1.6, w=.5, eye='o'), k(.56, 'post_r', x=-.3, y=-2, b=-2, w=.9, eye='O', l=1), k(.78, 'post_r', x=.1, y=.3, b=.3, eye='-'), k(.92, eye='>')],
        [], g='test', act=('peer', 'tower'))
    o.r('count_the_ripple_dashes', 'Counting the ripple dashes along the pool and arguing with the total', 24, 'none',
        [k(.1, 'ripple_a', x=.5, y=.7, b=.3, mark='1'), k(.28, 'ripple_b', x=1, y=1.3, b=.7, mark='2'), k(.46, 'ripple_c', x=1, y=1.3, b=.7, mark='3'), k(.64, 'mist_a', x=1.1, y=1.4, b=.8, mark='3?'), k(.82, 'mist_b', x=1.2, y=1.5, b=.9, eye='@', mark='...'), k(.94, eye='-')],
        [], g='test', act=('count', 'ripples'))
    o.r('chase_the_mist_along_the_front', 'Chasing the mist patches along the pool front, snapping at each as it fades', 22, 'none',
        [k(.1, 'mist_a', x=1.2, y=1.4, b=1), k(.26, 'mist_b', x=-.6, y=-.5, b=-1.2, w=.6, l=1, mark='snp'), k(.42, 'mist_a', x=1.8, y=1.8, b=1.5, w=.5, r=1, mark='snp'), k(.6, 'ripple_c', x=-.7, y=-.7, b=-1.4, w=1, l=1, mark='SNP'), k(.8, 'ripple_b', x=.7, y=1, b=.7, eye='@')],
        [], g='play', act=('chase', 'mist'), prefer=['happy'])
    o.r('walk_the_deck_on_one_wing', 'Teetering along the lower deck on one wing and one foot, calling it training', 24, 'wing',
        [k(.1, 'deck_lo', perch=1, reach=.9, x=.5, y=.5, b=.5), k(.3, 'deck_lo', perch=1, reach=.3, x=-.4, y=-.5, b=-.9, l=1), k(.52, 'deck_lo2', perch=1, reach=.8, x=.5, y=.6, b=.6, r=1), k(.74, 'deck_lo2', perch=1, reach=.2, x=-.4, y=-.6, b=-.9, l=1, eye='-'), k(.9, 'deck_lo2', perch=1, reach=.1, x=.2, b=.1)],
        [], g='play', act=('balance', 'deck'))
    o.r('race_the_far_brim', 'Racing round the far brim and back, wings out like an aeroplane with a grudge', 22, 'wing',
        [k(.1, 'lip_l', perch=1, reach=.4, x=.7, b=.2), k(.3, 'lip_l', perch=1, reach=1, x=1.1, y=.5, b=-.5, l=1), k(.55, 'lip_r', perch=1, reach=1, x=1.5, y=.6, b=-.7, r=1, mark='nyoom'), k(.8, 'lip_r', perch=1, reach=.6, x=.5, y=.9, b=.6, eye='@')],
        [], g='play', act=('race', 'brim'), prefer=['young'])
    o.r('nap_on_the_deck', 'Dozing on the low deck with his bill under a wing, the spray ticking past his tail', 36, 'none',
        [k(.12, 'deck_lo', perch=1, x=-.5, y=.9, b=.9, w=.5), k(.3, 'deck_lo', perch=1, x=-.7, y=1.7, b=1.9, eye='-'), k(.6, 'deck_lo2', perch=1, x=-.7, y=1.9, b=2, w=.9, eye='-', mark='zzz'), k(.85, 'deck_lo2', perch=1, x=-.2, y=.9, b=.9, eye='^')],
        [], g='rest', act=('nap', 'deck'), prefer=['tired'], say=["Slept on a deck. Woke up on a deck. Consistent.", "Deck is firm. So is my resolve to nap."])
    o.r('sulk_at_the_near_brim', 'Sulking at the near brim and refusing to look at the pool', 26, 'none',
        [k(.15, 'lip_l', perch=1, x=-.4, y=.4, b=.4, w=.5), k(.4, 'lip_l', perch=1, x=-.6, y=1.9, b=1.8, eye='-'), k(.7, 'lip_l', perch=1, x=-.7, y=2.1, b=2, w=.4, eye='-', mark='hmph'), k(.9, 'lip_l', perch=1, x=-.2, y=.6, b=.5, eye='^')],
        [], g='rest', act=('sulk', 'brim'), prefer=['sad', 'grumpy'])
    o.r('sit_on_the_second_deck_board', 'Sitting on the second deck board with his feet tucked and one eye on the pool', 28, 'none',
        [k(.15, 'deck_lo2', perch=1, x=.8, b=.9), k(.38, 'deck_lo2', perch=1, x=1, y=.2, b=1.8, w=.6, eye='o'), k(.64, 'deck_lo', perch=1, x=.9, y=.1, b=1.9, eye='-', mark='sigh'), k(.88, 'deck_lo', perch=1, x=.7, b=.7, eye='^')],
        [], g='rest', act=('sit', 'deck'), prefer=['tired'])
    o.r('kick_the_ladder_post', 'Kicking the far post, regretting it, and hopping off on one foot', 18, 'none',
        [k(.12, 'post_r', x=.8, y=1, b=.8), k(.3, 'post_r', x=1.2, y=1.4, b=-.9, l=1, mark='tak'), k(.46, 'post_r', x=-.8, y=-1, b=-1.9, l=1, w=.8, eye='O', mark='OW'), k(.66, x=-1.4, y=1.6, b=.9, r=1, eye='@'), k(.88, eye='>')],
        [(.46, 'dent')], g='mishap', act=('kick', 'post'), prefer=['grumpy'], say=["Post didn't move. My toe did. Elsewhere.", "Kicked the post. Post wins. Again."])
    o.r('tumble_off_the_deck_end', 'Tumbling off the end of the deck in a flap of wings and landing flat on his bill', 22, 'none',
        [k(.12, 'deck_lo2', perch=1, x=.6, y=.5, b=.8), k(.3, 'deck_lo2', perch=1, x=1.6, y=1.6, b=-1.5, w=.7, mark='whoa'), k(.5, 'deck_lo2', perch=1, x=-1.8, y=-2.1, b=2.4, w=1, l=1, r=1, eye='O', mark='SPLAT'), k(.74, 'deck_lo2', perch=1, x=1.1, y=2, b=1.7, eye='@'), k(.9, 'deck_lo2', perch=1, x=.6, b=.6, eye='>')],
        [(.5, 'bruise')], g='mishap', act=('fold', 'deck'))
    o.r('hook_a_wing_on_the_low_bolt', 'Hooking a wing round the low foot bolt and flapping until it snaps free', 22, 'wing',
        [k(.12, 'foot_bolt', reach=.8, x=.6, y=.7, b=.6), k(.3, 'foot_bolt', reach=.3, x=.9, y=.4, b=.8, mark='hm'), k(.5, 'foot_bolt', reach=1, x=-1, y=-.9, b=-1.4, l=1, r=1, eye='O', mark='MPH'), k(.7, 'foot_bolt', reach=.2, x=-1.4, y=-1.2, b=-1.8, eye='@', mark='POP'), k(.9, x=.5, eye='-')],
        [], g='mishap', act=('hook', 'bolt'))
    o.r('bow_to_the_ripples', 'Bowing to the ripples in turn, left row then right, as if they had curtain-called', 20, 'none',
        [k(.15, 'pool_l', x=-.3, y=-.5, b=-.5, w=.6), k(.38, 'ripple_a', x=.9, y=1.8, b=1.3, w=1, l=1, mark='merci'), k(.6, 'ripple_c', x=1, y=2.2, b=1.6, w=1, r=1), k(.86, 'ripple_c', x=.1, y=-.3, b=-.3, eye='^')],
        [], g='show', act=('bow', 'ripples'))
    o.r('argue_with_the_lane_mouth', 'Arguing with the lane mouth, wing pointing up the run as the water answers', 22, 'wing',
        [k(.12, 'lane_a', reach=.9, x=.8, y=.8, b=.6), k(.3, 'lane_a', reach=.3, x=1.4, y=-.7, b=-.3, mark='NO'), k(.5, 'lane_b', reach=1, x=1.5, y=-.9, b=.1, r=1, mark='NO'), k(.7, 'lane_a', reach=.4, x=.9, y=.9, b=1.2, l=1, eye='>', mark='!!'), k(.9, eye='-')],
        [], g='show', act=('argue', 'lane'), prefer=['grumpy'])
    o.r('compare_the_two_runs', 'Comparing the low and the high lane, head swinging up and down the run', 24, 'none',
        [k(.12, 'lane_a', x=.5, y=.6, b=.3), k(.32, 'lane_a', x=1, y=1.2, b=.7, eye='o'), k(.5, 'lane_b', x=1, y=-.4, b=-.5, eye='O'), k(.7, 'lane_c', x=.9, y=-1, b=-1, eye='-', mark='hm'), k(.9, 'lane_m', x=.5, y=.9, b=.5, eye='>')],
        [], g='show', act=('compare', 'lanes'), prefer=['curious'])
    o.emit()


def trampoline():
    # Drawing (74 x 40 cells, 6.5 px a row, standing line row 29): a low oval frame seen from the front. Left and right rim arcs `(` `)` rows 22-29,
    # the mat inside it as `. :` dots, far rim marks `=` on rows 19-21 (58 to 65 px), short legs `|` at cols 12 and 64 (row 28-29), springs `//` and the
    # leg feet below the standing line (never touched). Bouncing is native, so these are the other acts: the mat as a floor, the rim and legs.
    P = pm('trampoline')
    o = Obj('trampoline', 'placed',
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm')],
            effects=dict(sweep=[('obj.dirt', 'add', -.25)], blot=[('obj.wetness', 'add', -.3)], scrape=[('frost', 'mul', .2)], plough=[('drift', 'set', 0)],
                         square=[('obj.condition', 'add', .2)], sag=[('obj.condition', 'add', -.15)], smudge=[('obj.dirt', 'add', .12)],
                         giggle=[('need.fun', 'add', 2)], doze=[('need.energy', 'add', 2)], bruise=[('obj.dirt', 'add', .14)]),
            anchors=dict(rim_l=P(5, 26), rim_r=P(68, 26), mat_a=P(20, 27, 'surface'), mat_b=P(37, 26, 'surface'), mat_c=P(52, 27, 'surface'),
                         mat_front=P(37, 28, 'surface'), far_l=P(21, 20), far_r=P(57, 20), leg_l=P(12, 29), leg_r=P(64, 29),
                         spring_l=P(17, 30), spring_r=P(57, 30), foot_l=P(12, 37), foot_r=P(56, 37)))
    # ---------------- care
    o.r('sweep_the_mat', 'Sweeping the mat with long wing strokes from the left rim to the right', 22, 'wing',
        [k(.1, 'mat_a', perch=1, reach=.4, x=.4, y=.7, b=.4), k(.3, 'mat_a', perch=1, reach=1, x=.7, y=1, b=.8, l=1, mark='shff'), k(.5, 'mat_b', perch=1, reach=1, x=.7, y=1, b=.8, r=1, mark='shff'),
         k(.7, 'mat_c', perch=1, reach=1, x=.7, y=1, b=.8, l=1, mark='shff'), k(.9, 'mat_c', perch=1, reach=.2, x=.2, b=.2, eye='^')],
        [(.7, 'sweep')], g='care', act=('sweep', 'mat'), when=['obj_dirt>.3'],
        say=["Mat swept. Now nobody can blame the mat.", "Dust on the wing. Bread crumbs, hopefully."])
    o.r('blot_the_wet_mat', 'Blotting the wet mat dry with his breast, one wide arc at a time', 24, 'none',
        [k(.1, 'mat_c', perch=1, x=.2, y=.4, b=.6), k(.3, 'mat_c', perch=1, x=.1, y=.9, b=1.7, w=.5, mark='fwp'), k(.5, 'mat_b', perch=1, x=.1, y=.9, b=1.8, w=.6, mark='fwp'), k(.7, 'mat_a', perch=1, x=.1, y=.9, b=1.7, w=.5, mark='fwp'), k(.9, 'mat_a', perch=1, x=.2, b=.4, eye='-')],
        [(.5, 'blot')], g='care', act=('dry', 'mat'), when=['obj_wetness>.3'])
    o.r('scrape_frost_off_the_mat', 'Scraping a frost crust off the mat with the flat of his foot, three raspy goes', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.2, y=.4, b=.5), k(.28, 'mat_front', perch=1, x=.4, y=.6, b=.8, l=1, mark='zzrk'), k(.46, 'mat_b', perch=1, x=.4, y=.6, b=.8, r=1, mark='zzrk'), k(.64, 'mat_b', perch=1, x=.4, y=.6, b=.9, l=1, mark='ZZRK'), k(.86, 'mat_b', perch=1, x=.1, b=.2, eye='^')],
        [(.64, 'scrape')], g='weather', act=('scrape', 'mat'), when=['frost>.3'])
    o.r('plough_drift_off_the_mat', 'Ploughing a snow drift off the mat edge with his chest', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.3, y=.8, b=.4), k(.3, 'mat_front', perch=1, x=1, y=1.7, b=1.2, w=.6, mark='shhh'), k(.5, 'mat_c', perch=1, x=1.2, y=1.8, b=1.3, l=1, mark='SHHH'), k(.72, 'mat_c', perch=1, x=.4, y=.8, b=.3, w=.9, eye='>'), k(.9, 'mat_c', perch=1, x=.1, b=0, eye='-')],
        [(.5, 'plough')], g='weather', act=('push', 'drift'), when=['drift>.3'],
        say=["Snow off the mat. Snow on my back. Even.", "Ploughed it. Nobody asked. Nobody thanked."])
    o.r('square_up_the_leg', 'Shouldering the left leg back square after it slumped', 20, 'none',
        [k(.12, 'leg_l', x=.3, y=.4, b=.3), k(.3, 'leg_l', x=-.3, y=-.3, b=-.6, mark='hup'), k(.5, 'leg_l', x=-.8, y=-.6, b=-1, l=1, mark='nnng'), k(.7, 'leg_l', x=-1, y=-.6, b=-1.1, r=1, mark='THUNK'), k(.9, x=.2, y=.2, eye='^')],
        [(.7, 'square')], g='care', act=('straighten', 'leg'), when=['obj_condition<.6'],
        say=["Leg level. Mat stays flat. I am structural.", "Shoved it straight. Zero training."])
    # ---------------- use / test
    o.r('press_the_mat_with_a_wing', 'Pressing down on the mat with one wing to see how far it gives', 20, 'wing',
        [k(.12, 'mat_front', perch=1, reach=.3, x=.3, y=.7, b=.5), k(.3, 'mat_front', perch=1, reach=1, x=.4, y=1.2, b=1.2, eye='o'), k(.5, 'mat_front', perch=1, reach=1, x=.4, y=1.4, b=1.5, l=1, mark='bwomp'), k(.7, 'mat_front', perch=1, reach=.5, x=.2, y=.6, b=.6, eye='O'), k(.9, 'mat_front', perch=1, reach=.1, eye='-')],
        [], g='test', act=('press', 'mat'), prefer=['curious'],
        say=["It gives. It also gives back. Hm.", "Pressed it. It pressed my ego."])
    o.r('tap_the_rim_ring', 'Tapping the rim arc left and right for the boing it hums back', 20, 'none',
        [k(.1, 'rim_l', x=.4, y=.6, b=.3), k(.26, 'rim_l', x=.9, y=1.1, b=.7, mark='tk'), k(.5, 'rim_r', x=.9, y=-.2, b=-.2, mark='tk'), k(.7, 'rim_l', x=.9, y=1.1, b=.7, eye='o', mark='tk-tk'), k(.9, x=.2, eye='>')],
        [], g='test', act=('tap', 'rim'), prefer=['curious'])
    o.r('peer_along_the_far_rim', 'Standing on tiptoe to peer along the far rim, neck out like a periscope', 22, 'none',
        [k(.12, 'far_l', x=.3, y=-.5, b=-.6), k(.3, 'far_l', x=.7, y=-1.4, b=-1.4, w=.5, l=1, eye='o'), k(.5, 'far_r', x=.9, y=-1.6, b=-1.5, w=.5, r=1, eye='O'), k(.72, 'far_r', x=.4, y=-.6, b=-.5, eye='-'), k(.9, x=0, y=.2, b=.1, eye='>')],
        [], g='test', act=('peer', 'rim'), prefer=['young'])
    o.r('roll_across_the_mat', 'Rolling flat across the mat from one side to the other, chuckling', 24, 'none',
        [k(.1, 'mat_a', perch=1, x=.2, b=.4), k(.3, 'mat_a', perch=1, x=.4, y=1, b=1.6, w=1, l=1, eye='-', mark='hrm'), k(.5, 'mat_b', perch=1, x=.4, y=1, b=1.8, w=1, r=1, eye='^', mark='hrr'), k(.7, 'mat_c', perch=1, x=.4, y=1, b=1.7, w=1, l=1, mark='hrh'), k(.9, 'mat_c', perch=1, x=.3, y=.3, b=.5, eye='@')],
        [(.7, 'giggle')], g='play', act=('roll', 'mat'), prefer=['happy'],
        say=["Rolled. Got dizzy. Rolled again.", "Mat is soft. I am soft. We understand each other."])
    o.r('race_the_front_edge', 'Racing the mat front edge from the left rim to the right and back', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.6, y=.3, b=.2), k(.28, 'mat_c', perch=1, x=1.5, y=.4, b=-.4, w=1, l=1, mark='zip'), k(.5, 'mat_a', perch=1, x=1.5, y=.4, b=-.5, w=1, r=1, mark='zip'), k(.7, 'mat_c', perch=1, x=1.6, y=.5, b=-.5, w=1, l=1, mark='ZIP'), k(.9, 'mat_front', perch=1, x=.4, b=.1, eye='@')],
        [], g='play', act=('race', 'edge'), prefer=['young', 'happy'])
    o.r('kick_the_rim', 'Kicking the right rim arc with a flat foot, then hopping away on his other foot', 18, 'none',
        [k(.12, 'rim_r', x=.2, y=.4, b=.2), k(.3, 'rim_r', x=.4, y=.6, b=-.3, l=1, mark='tang'), k(.46, 'rim_r', x=.5, y=.7, b=-.5, l=1, eye='>', mark='TANG'), k(.64, 'rim_r', x=-.4, y=-.2, b=-1, r=1, w=1, eye='O', mark='yow'), k(.86, 'rim_r', x=.2, b=.2, eye='^')],
        [(.46, 'sag')], g='mishap', act=('kick', 'rim'), prefer=['grumpy'],
        say=["Kicked the rim. Rim kicked back. Rude.", "Toes fine. Pride bent."])
    o.r('sit_on_the_mat_edge', 'Sitting at the mat edge with his feet tucked, looking at the sky', 28, 'none',
        [k(.15, 'mat_front', perch=1, x=.2, b=.6), k(.4, 'mat_front', perch=1, x=.2, y=-.6, b=1.2, eye='o'), k(.65, 'mat_front', perch=1, x=.2, y=-.6, b=1.3, eye='-', mark='...'), k(.88, 'mat_front', perch=1, x=.2, y=.2, b=.4, eye='^')],
        [(.65, 'doze')], g='rest', act=('sit', 'edge'), prefer=['tired'])
    o.r('nap_in_the_mat_dip', 'Napping flat in the middle of the mat, the dip hugging him', 40, 'none',
        [k(.12, 'mat_b', perch=1, x=.2, b=.8), k(.3, 'mat_b', perch=1, x=.4, y=.9, b=1.8, eye='-'), k(.6, 'mat_b', perch=1, x=.4, y=1, b=1.9, eye='-', mark='zzz'), k(.85, 'mat_b', perch=1, x=.2, y=.4, b=.8, eye='^')],
        [(.6, 'doze')], g='rest', act=('nap', 'mat'), prefer=['tired'], when=['day'],
        say=["Mat is basically a bed that hates rules.", "Slept. Springs complained. I ignored them."])
    o.r('lean_on_the_right_leg', 'Leaning back against the right leg, arms folded, thinking', 24, 'none',
        [k(.14, 'leg_r', x=-.5, y=.3, b=.3, w=.4), k(.4, 'leg_r', x=-1.4, y=-.9, b=-1.4, r=1, w=1), k(.7, 'leg_r', x=-1.3, y=-.2, b=.9, eye='-', mark='hmm'), k(.9, 'leg_r', x=-.4, y=.2, b=.1, eye='^')],
        [], g='rest', act=('lean', 'leg'))
    o.r('slip_off_the_wet_mat', 'Skating on the wet mat and shooting off the front edge', 18, 'none',
        [k(.12, 'mat_b', perch=1, x=.2, b=.1), k(.3, 'mat_b', perch=1, x=.8, y=.5, b=-.7, w=1, l=1, mark='oop'), k(.5, 'mat_front', perch=1, x=1.7, y=1.8, b=1.8, w=1, r=1, eye='O', mark='SKRRT'), k(.8, 'mat_front', perch=1, x=.5, y=1.2, b=1, eye='@')],
        [(.5, 'smudge')], g='mishap', act=('slip', 'mat'), when=['obj_wetness>.4'],
        say=["Mat betrayed me. Damp and unsorry.", "Skated off. Grace was not invited."])
    o.r('sink_into_the_dip', 'Sinking so deep into the mat dip that he needs two goes to stand', 24, 'none',
        [k(.1, 'mat_b', perch=1, x=.3, b=1), k(.3, 'mat_b', perch=1, x=.5, y=1.4, b=2, eye='O'), k(.5, 'mat_b', perch=1, x=.7, y=1.2, b=1.5, w=1, l=1, r=1, mark='ugh'), k(.7, 'mat_b', perch=1, x=.5, y=1.4, b=2.1, eye='>', mark='uugh'), k(.88, 'mat_b', perch=1, x=.2, b=.4, eye='@')],
        [(.88, 'smudge')], g='mishap', act=('stuck', 'mat'), prefer=['grown'],
        say=["Stuck. In a trampoline. Don't write this down.", "Got up. Second go. Nobody saw. Right?"])
    o.r('bow_to_the_far_rim', 'Bowing to the far rim, wings out, as if it clapped', 18, 'wing',
        [k(.15, 'far_l', reach=.5, x=-.2, y=-.6, b=-.6), k(.4, 'far_r', reach=1, x=.9, y=1.8, b=1.3, l=1, mark='ta-da'), k(.65, 'far_r', reach=1, x=1, y=2.2, b=1.6, r=1), k(.88, 'far_l', reach=.2, x=.1, y=-.4, b=-.3, eye='^')],
        [], g='show', act=('bow', 'rim'))
    o.r('pose_on_the_mat_centre', 'Posing on the mat centre with one foot up, like he built it', 18, 'none',
        [k(.14, 'mat_b', perch=1, x=.2, b=-.3), k(.4, 'mat_b', perch=1, x=-.4, y=-.8, b=-1.2, w=.7, l=1, eye='^'), k(.66, 'mat_b', perch=1, x=.6, y=-.9, b=-1, w=1, r=1, l=1), k(.9, 'mat_b', perch=1, x=.2, b=-.1)],
        [], g='show', act=('pose', 'mat'), prefer=['happy'])
    o.r('argue_with_the_legs', 'Arguing with both legs in turn about whose idea the wobble was', 22, 'wing',
        [k(.12, 'leg_l', reach=.5, x=.3, y=.2, b=.2), k(.3, 'leg_l', reach=1, x=.8, y=-.3, b=.2, mark='YOU'), k(.5, 'leg_r', reach=1, x=.9, y=-.4, b=.3, r=1, mark='NO, YOU'), k(.7, 'leg_l', reach=1, x=.6, y=.5, b=.8, l=1, eye='>', mark='!!'), k(.9, eye='-')],
        [], g='show', act=('argue', 'leg'), prefer=['grumpy'],
        say=["Both legs agreed. Against me. Cowards.", "Wobble was theirs. I wrote it down."])
    # ---------------- v3 top-up: the other tricks on the mat (perch + b hops), the springs and feet in front, more upkeep
    o.r('seat_drop_on_the_mat', 'Dropping onto the mat on his tail end from a standing hop and sitting in the dent', 20, 'none',
        [k(.12, 'mat_b', perch=1, x=.3, b=-1.4, w=.6), k(.3, 'mat_b', perch=1, x=.2, y=.4, b=-2, w=1, l=1, r=1, mark='hup'), k(.5, 'mat_b', perch=1, x=-.3, y=1.3, b=2.2, eye='O', mark='BWOMP'), k(.72, 'mat_b', perch=1, x=.4, y=.9, b=1.4, eye='-'), k(.9, 'mat_b', perch=1, x=.2, b=.3, eye='^')],
        [], g='use', act=('sit', 'mat'), prefer=['happy'], say=["Seat drop. Perfect landing. Mat disagrees.", "Sat down hard. The mat caught on."])
    o.r('belly_flop_on_the_mat', 'Belly-flopping onto the mat arms wide and bouncing once flat on his front', 20, 'none',
        [k(.12, 'mat_a', perch=1, x=.4, b=-1.6, w=1), k(.3, 'mat_a', perch=1, x=1.2, y=1.6, b=-1, w=1, eye='>', mark='hup'), k(.48, 'mat_b', perch=1, x=1.6, y=2.3, b=2.2, w=1, eye='O', mark='FWOMP'), k(.7, 'mat_b', perch=1, x=1.4, y=2, b=-.8, w=.7), k(.9, 'mat_b', perch=1, x=.3, y=.6, b=.6, eye='@')],
        [], g='use', act=('hop', 'mat'), prefer=['young', 'happy'])
    o.r('spin_on_the_mat', 'Spinning round on the mat on one foot, hop after hop, until he is facing the wrong way', 22, 'none',
        [k(.1, 'mat_b', perch=1, x=.3, b=-.8, l=1), k(.26, 'mat_b', perch=1, x=-.5, y=.4, b=-1.2, r=1, w=1, mark='whirr'), k(.44, 'mat_c', perch=1, x=.7, y=.4, b=-1.2, l=1, w=1), k(.62, 'mat_a', perch=1, x=-.7, y=.5, b=-1.3, r=1, w=1, mark='WHIRR'), k(.82, 'mat_b', perch=1, x=.2, y=.9, b=.8, eye='@')],
        [], g='use', act=('spin', 'mat'), prefer=['happy'])
    o.r('freeze_at_the_top_of_a_hop', 'Hopping and freezing in mid-air for a count of two, pretending the mat is not a factor', 20, 'none',
        [k(.12, 'mat_b', perch=1, x=.2, b=.4), k(.3, 'mat_b', perch=1, x=.4, y=-.6, b=-2.4, w=.6, l=1, r=1, mark='hup'), k(.5, 'mat_b', perch=1, x=.4, y=-.6, b=-2.4, w=.6, l=1, r=1, eye='o', mark='...'), k(.7, 'mat_b', perch=1, x=.3, y=.5, b=1.2, eye='O', mark='bwomp'), k(.9, 'mat_b', perch=1, x=.2, b=.3, eye='^')],
        [], g='use', act=('balance', 'mat'), prefer=['curious'])
    o.r('bounce_across_to_the_front_edge', 'Hopping across the mat in three long bounces and fetching up at the front edge', 22, 'none',
        [k(.1, 'mat_a', perch=1, x=.5, b=-1), k(.28, 'mat_b', perch=1, x=1.4, y=.3, b=-1.8, w=.8, mark='boing'), k(.48, 'mat_c', perch=1, x=1.5, y=.3, b=-1.9, w=.8, mark='boing'), k(.68, 'mat_front', perch=1, x=1.7, y=.5, b=-1.7, w=.8, mark='BOING'), k(.86, 'mat_front', perch=1, x=.4, y=.8, b=.8, eye='@')],
        [], g='use', act=('race', 'mat'), prefer=['young'])
    o.r('climb_up_over_the_rim', 'Hauling himself up the front of the rim in three flapping tries and rolling onto the mat', 24, 'wing',
        [k(.1, 'rim_l', reach=.4, x=.3, y=.6, b=.4), k(.26, 'rim_l', reach=1, x=.9, y=-.6, b=-.9, l=1, mark='hup'), k(.42, 'mat_a', perch=1, reach=1, x=.9, y=-.3, b=-1, r=1, mark='hup'), k(.62, 'mat_a', perch=1, reach=.5, x=.5, y=.9, b=1.2, eye='@'), k(.86, 'mat_a', perch=1, reach=.1, x=.2, b=.3, eye='^')],
        [], g='use', act=('climb', 'rim'), ages=GROWN)
    o.r('polish_the_rim', 'Polishing the rim arc with a wing, left side then right, until it squeaks', 20, 'wing',
        [k(.1, 'rim_l', reach=.5, x=.2, y=.3), k(.28, 'rim_l', reach=1, x=.4, y=.6, b=.5, mark='squk'), k(.5, 'rim_r', reach=1, x=.4, y=.6, b=.5, l=1, mark='squk'), k(.72, 'rim_r', reach=.5, x=.2, y=.2, r=1), k(.9, eye='^')],
        [(.5, 'sweep')], g='care', act=('polish', 'rim'), when=['obj_dirt>.4'])
    o.r('wipe_the_wet_legs', 'Wiping both wet legs dry with a wing, then shaking the wing out', 20, 'wing',
        [k(.1, 'leg_l', reach=.4, x=.3, y=.4, b=.3), k(.28, 'leg_l', reach=1, x=.6, y=.7, b=.6, mark='fwp'), k(.5, 'leg_r', reach=1, x=.6, y=.7, b=.6, l=1, mark='fwp'), k(.7, 'leg_r', reach=.3, x=-.3, y=-.2, b=-.5, r=1, mark='flk'), k(.9, eye='-')],
        [(.5, 'blot')], g='care', act=('wipe', 'legs'), when=['obj_wetness>.4'])
    o.r('nudge_the_spring_back', 'Nudging a bent spring coil back into line with his bill, tutting', 20, 'none',
        [k(.1, 'spring_l', x=.4, y=.8, b=.4), k(.28, 'spring_l', x=1.1, y=1.6, b=1.2, mark='nk'), k(.46, 'spring_l', x=1.3, y=1.9, b=1.5, l=1, mark='nk'), k(.66, 'spring_l', x=1.4, y=2, b=1.6, r=1, mark='NK'), k(.86, x=.4, y=.5, b=.3, eye='^')],
        [(.66, 'square')], g='care', act=('fit', 'spring'), when=['obj_condition<.6'], say=["Coil is back in line. Don't tell the others.", "Fixed the spring. Wing is now a spring."])
    o.r('scrape_ice_from_the_rim', 'Scraping an ice crust off the front rim with the flat of a foot', 20, 'none',
        [k(.1, 'rim_l', x=.3, y=.6, b=.5), k(.28, 'rim_l', x=.6, y=.8, b=.9, l=1, mark='zzk'), k(.5, 'rim_r', x=.6, y=.8, b=.9, r=1, mark='zzk'), k(.7, 'rim_r', x=.3, y=.4, b=.4, l=1, eye='^')],
        [(.5, 'scrape')], g='weather', act=('scrape', 'rim'), when=['frost>.4'])
    o.r('scoop_snow_off_the_front', 'Scooping a snow drift off the front of the mat with his bill and flinging it aside', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.4, y=.9, b=.6), k(.28, 'mat_front', perch=1, x=1.3, y=1.9, b=1.5, mark='fsh'), k(.42, 'mat_front', perch=1, x=-.6, y=-.6, b=-.8, w=.6, mark='fup'), k(.6, 'mat_a', perch=1, x=1.3, y=1.9, b=1.5, l=1, mark='fsh'), k(.8, 'mat_a', perch=1, x=-.5, y=-.5, b=-.7, w=.6, eye='>'), k(.92, 'mat_a', perch=1, x=.2, eye='-')],
        [(.6, 'plough')], g='weather', act=('scoop', 'drift'), when=['drift>.3'])
    o.r('hunker_by_the_leg', 'Hunkering by the left leg with his neck pulled in while the wind drags over the mat', 30, 'none',
        [k(.15, 'leg_l', x=.5, y=1.1, b=1.2, w=.3), k(.4, 'leg_l', x=-.8, y=1.9, b=2.1, w=.8, eye='-'), k(.7, 'leg_l', x=-.9, y=2, b=2.2, w=.5, eye='-', mark='brr'), k(.9, 'leg_l', x=.2, y=.9, b=.9, eye='^')],
        [], g='weather', act=('shelter', 'leg'), when=['windy'])
    o.r('warm_up_on_the_sun_mat', 'Laying his breast on the sun-warm mat, wings spread, and sighing', 28, 'none',
        [k(.12, 'mat_c', perch=1, x=.8, y=-.2, b=-.2), k(.34, 'mat_c', perch=1, x=-.6, y=1.5, b=2.1, w=1, eye='-'), k(.62, 'mat_a', perch=1, x=-.6, y=1.6, b=2.2, w=1, eye='-', mark='ahhh'), k(.86, 'mat_a', perch=1, x=.7, y=-.3, b=-.2, w=.2, eye='^')],
        [], g='weather', act=('warm', 'mat'), when=['sun'])
    o.r('shake_the_rain_off', 'Shaking the rain out of his feathers at the mat edge, wings snapping like towels', 18, 'none',
        [k(.12, 'mat_front', perch=1, x=.2, b=.4), k(.3, 'mat_front', perch=1, x=-.4, y=-.9, b=-1.3, w=1, l=1, mark='brrt'), k(.46, 'mat_front', perch=1, x=.5, y=1, b=1.5, w=.6, r=1, mark='brrt'), k(.66, 'mat_front', perch=1, x=-.5, y=-1, b=-1.4, w=1, mark='BRRT'), k(.86, 'mat_front', perch=1, x=.1, eye='^')],
        [], g='weather', act=('fluff', 'feathers'), when=['wet'])
    o.r('listen_to_the_springs', 'Laying his ear against the spring row and listening to them tick as the air cools', 22, 'none',
        [k(.12, 'spring_l', x=.3, y=.7, b=.4), k(.3, 'spring_l', x=1, y=1.4, b=1, eye='o'), k(.5, 'spring_r', x=1.1, y=1.5, b=1.1, eye='O', mark='tik'), k(.72, 'spring_r', x=1, y=.3, b=.2, eye='@', mark='tik'), k(.9, eye='>')],
        [], g='test', act=('listen', 'springs'), prefer=['curious'])
    o.r('flick_the_springs', 'Flicking each spring with his bill and listening to the notes go sour', 22, 'none',
        [k(.1, 'spring_l', x=.5, y=.9, b=.5), k(.26, 'spring_l', x=1.2, y=1.6, b=1.1, mark='boing'), k(.42, 'spring_r', x=1.2, y=1.6, b=1.1, mark='boyng'), k(.6, 'spring_l', x=1.4, y=1.9, b=1.4, l=1, mark='BOYNG'), k(.8, x=.3, y=.4, b=.2, eye='o')],
        [], g='test', act=('ring', 'springs'), prefer=['curious'])
    o.r('weigh_the_mat_with_a_foot', 'Testing the mat with one foot and then the other, a quarter of his weight at a time', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.2, b=.3, l=1), k(.3, 'mat_front', perch=1, x=.4, y=.6, b=.8, l=1, mark='bf'), k(.5, 'mat_front', perch=1, x=.4, y=1.1, b=1.2, r=1, mark='bf'), k(.7, 'mat_front', perch=1, x=.3, y=1.4, b=1.8, l=1, r=1, eye='o'), k(.9, 'mat_front', perch=1, x=.2, b=.3, eye='^')],
        [], g='test', act=('weigh', 'mat'))
    o.r('dance_a_jig_on_the_mat', 'Dancing a springy jig across the mat with every hop going higher than the last', 24, 'none',
        [k(.1, 'mat_a', perch=1, x=.3, b=-.5, l=1), k(.28, 'mat_a', perch=1, x=.3, y=-.3, b=-1.3, r=1, w=.6), k(.46, 'mat_b', perch=1, x=.3, y=-.4, b=-1.8, l=1, w=.8), k(.66, 'mat_c', perch=1, x=.2, y=-.6, b=-2.3, r=1, l=1, w=1, eye='^', mark='hup'), k(.86, 'mat_c', perch=1, x=.2, b=.3)],
        [(.66, 'giggle')], g='play', act=('dance', 'mat'), prefer=['happy'])
    o.r('hop_the_row_of_springs', 'Hopping along the spring row from one coil to the next, never touching the same one twice', 22, 'none',
        [k(.1, 'spring_l', x=.6, b=-.6, l=1), k(.28, 'foot_l', x=1.2, b=-1.2, r=1, w=.7, mark='hup'), k(.48, 'spring_r', x=1.3, b=-1.3, l=1, w=.7), k(.68, 'foot_r', x=1.4, b=-1.2, r=1, w=.8, mark='HUP'), k(.86, 'spring_r', x=.3, b=.3, eye='@')],
        [], g='play', act=('hop', 'springs'), prefer=['young'])
    o.r('chase_himself_round_the_legs', 'Chasing his own tail round and round the foot of the left leg, then the right', 22, 'none',
        [k(.1, 'foot_l', x=.8, y=.5, b=.2), k(.28, 'foot_l', x=1.9, y=1.5, b=1.2, w=1, l=1), k(.46, 'foot_r', x=-.9, y=1.2, b=.6, r=1, w=1), k(.64, 'foot_l', x=2, y=1.6, b=1.3, w=1, l=1), k(.84, 'foot_r', x=.3, y=.4, eye='@')],
        [], g='play', act=('chase', 'legs'), prefer=['grumpy'])
    o.r('kick_the_foot_pad', 'Kicking the leg foot pad along the ground like a football and chasing it back', 20, 'none',
        [k(.1, 'foot_l', x=.3, y=.4, b=.3), k(.28, 'foot_l', x=.6, y=.8, b=-.6, l=1, mark='tok'), k(.46, 'foot_l', x=1, y=1, b=-1.1, r=1, w=.6, mark='TOK'), k(.66, 'foot_r', x=1.2, y=1.2, b=-.6, l=1), k(.86, 'foot_r', x=.3, y=.4, eye='^')],
        [], g='play', act=('kick', 'pad'), prefer=['happy'])
    o.r('sulk_at_the_rim', 'Sulking at the rim with his bill pressed to its cold arc', 26, 'none',
        [k(.15, 'rim_r', x=.5, y=1, b=.6), k(.4, 'rim_r', x=.9, y=1.5, b=1, eye='-'), k(.7, 'rim_r', x=1, y=1.7, b=1.2, eye='-', mark='hmph'), k(.9, x=.3, y=.4, b=.2, eye='^')],
        [], g='rest', act=('sulk', 'rim'), prefer=['sad', 'grumpy'])
    o.r('wait_by_the_mat_for_a_turn', 'Waiting at the mat edge, glancing from the far rim to his own feet', 28, 'none',
        [k(.12, 'mat_front', perch=1, x=.2, y=-.7, b=-.4), k(.34, 'mat_front', perch=1, x=.4, y=-1.2, b=-.8, eye='o', mark='...'), k(.56, 'mat_front', perch=1, x=.2, y=.9, b=.9, l=1, eye='-'), k(.8, 'mat_front', perch=1, x=.3, y=-1.3, b=-1, r=1, eye='o'), k(.94, 'mat_front', perch=1, eye='>')],
        [], g='rest', act=('wait', 'mat'), prefer=['lonely'])
    o.r('sit_by_the_foot_pad', 'Sitting by the foot pad with his back to the leg and his feet stuck out', 26, 'none',
        [k(.15, 'foot_r', x=-.3, b=.7), k(.38, 'foot_r', x=-.5, y=.4, b=1.4, l=1, r=1, eye='o'), k(.64, 'foot_r', x=-.6, y=.5, b=1.6, eye='-', mark='sigh'), k(.88, 'foot_r', x=-.2, y=.2, b=.4, eye='^')],
        [], g='rest', act=('sit', 'pad'), prefer=['tired'])
    o.r('bonk_head_on_the_leg', 'Straightening up too quick beside the right leg and bonking his head against it', 18, 'none',
        [k(.12, 'leg_r', x=.4, y=1.1, b=1), k(.3, 'leg_r', x=.5, y=1.5, b=1.4, l=1), k(.44, 'leg_r', x=.9, y=-1.4, b=-1.3, w=1, eye='O', mark='TONK'), k(.64, x=-.8, y=1.4, b=.9, r=1, eye='@'), k(.88, eye='-')],
        [(.44, 'sag')], g='mishap', act=('knock', 'leg'), say=["Leg 1. Skull 0. Leg also bent.", "Hit it. It hit back. Physics."])
    o.r('roll_off_the_mat_edge', 'Rolling off the mat edge in a flap of wings and landing on his back looking at the sky', 20, 'none',
        [k(.12, 'mat_c', perch=1, x=.5, y=.7, b=.8), k(.3, 'mat_front', perch=1, x=1.5, y=1.5, b=-1.4, w=.8, mark='whoa'), k(.5, 'mat_front', perch=1, x=-1.8, y=-2, b=2.3, w=1, l=1, r=1, eye='O', mark='THUMP'), k(.74, 'mat_front', perch=1, x=1, y=1.9, b=1.6, eye='@'), k(.9, 'mat_front', perch=1, x=.5, b=.5, eye='>')],
        [(.5, 'bruise')], g='mishap', act=('fold', 'mat'))
    o.r('foot_caught_in_a_coil', 'Poking a foot past the coils for a look, and hopping about with a spring attached', 22, 'none',
        [k(.12, 'spring_r', x=.4, y=.8, b=.4), k(.3, 'spring_r', x=.8, y=1.4, b=1, l=1, mark='hm'), k(.5, 'spring_r', x=1.1, y=1.6, b=1.3, l=1, eye='O', mark='mmf'), k(.7, 'spring_r', x=-1.2, y=-.8, b=-1.4, l=1, w=1, mark='POP'), k(.9, x=.4, y=.9, b=.6, eye='@')],
        [], g='mishap', act=('hook', 'spring'), ages=GROWN, prefer=['curious'])
    o.r('boing_impressions_for_the_sky', 'Making boing noises at the sky from the mat centre, one more hopeful than the last', 24, 'none',
        [k(.12, 'mat_b', perch=1, x=.3, y=-.5, b=-.6), k(.3, 'mat_b', perch=1, x=.8, y=-1.4, b=-1.4, w=.6, mark='boing'), k(.5, 'mat_b', perch=1, x=1.2, y=-1.7, b=-1.9, w=.9, eye='^', mark='BOING'), k(.72, 'mat_b', perch=1, x=.6, y=-.6, b=-.5, eye='o', mark='b-oing?'), k(.9, 'mat_b', perch=1, x=.2, eye='-')],
        [], g='show', act=('sing', 'mat'), prefer=['lonely'], say=["Boing. Boing. Boooing. Encore denied.", "Mat said nothing. Typical audience."])
    o.r('present_the_trampoline', 'Presenting the whole trampoline, rim to leg to mat, with a wing flourish', 24, 'wing',
        [k(.1, 'leg_l', reach=.3, x=.1, y=-.3, b=-.2), k(.3, 'rim_l', reach=1, x=.1, y=-.7, b=-.5, mark='behold'), k(.52, 'far_l', reach=1, x=.1, y=-1, b=-.8, l=1), k(.76, 'rim_r', reach=.8, x=.2, y=-.4, b=-.3, r=1, eye='^')],
        [], g='show', act=('present', 'trampoline'), prefer=['happy'], say=["Trampoline. Mine. Bounces by appointment.", "Gave it a tour. It looked flat."])
    o.r('compare_the_two_far_marks', 'Comparing the two far rim marks, head swinging, deciding that one is higher', 22, 'none',
        [k(.12, 'far_l', x=.4, y=-.9, b=-.9), k(.32, 'far_l', x=1.2, y=-1.9, b=-2, eye='o'), k(.52, 'far_r', x=-.3, y=-2, b=-2.2, eye='O', w=.7), k(.72, 'far_l', x=1, y=.6, b=.6, eye='-', mark='hm'), k(.9, 'far_r', x=.4, y=-.9, b=-.9, eye='>')],
        [], g='show', act=('compare', 'rim'), prefer=['curious'])
    o.emit()


def toy_trampoline():
    # Drawing (88 x 51 cells, 7 px a row, standing line row 40): a net-walled trampoline. Posts `|` at cols 11 and 77 run up to their caps `(o)` at 247 px;
    # the net `/ \` diamonds fill rows 10-34 between them (the low rows 33-34 are 42 to 49 px), with `=` knots in rows 30-32 (56 to 70 px), net skirt `(` `)`
    # around the mat rows 35-40, mat dots `. :` rows 35-40 (0 to 35 px), springs and legs below the line. Riding is native: here are the net, posts,
    # knots and the mat front he can reach.
    P = pm('toy_trampoline')
    o = Obj('toy_trampoline', 'placed',
            fields=dict(frost=(0, 0, 1), drift=(0, 0, 1), tension=(0, 0, 1)),
            physics=[('frost', 'rate', .0015, 'cold'), ('frost', 'rate', -.002, 'warm'), ('drift', 'rate', .002, 'snow'), ('drift', 'rate', -.0015, 'warm'),
                     ('tension', 'rate', .0004, 'always')],
            effects=dict(wash=[('obj.dirt', 'add', -.25)], shake_dry=[('obj.wetness', 'add', -.3)], knot=[('obj.condition', 'add', .2), ('tension', 'set', 0)],
                         tear=[('obj.condition', 'add', -.15)], smudge=[('obj.dirt', 'add', .12)], chip=[('frost', 'mul', .2)], knock=[('drift', 'set', 0)],
                         giggle=[('need.fun', 'add', 2)], doze=[('need.energy', 'add', 2)], tweak=[('obj.condition', 'add', .2)], bruise=[('obj.dirt', 'add', .14)]),
            anchors=dict(pole_l=P(11, 33), pole_r=P(77, 33), net_a=P(14, 34), net_b=P(36, 34), net_c=P(60, 34), knot_a=P(16, 32), knot_b=P(33, 31), knot_c=P(69, 32),
                         knot_hi=P(49, 30), skirt_l=P(12, 37), skirt_r=P(74, 37), mat_a=P(24, 39, 'surface'), mat_b=P(44, 39, 'surface'), mat_front=P(36, 40, 'surface'),
                         spring_l=P(17, 41), spring_r=P(56, 41), foot_l=P(19, 48), foot_r=P(71, 48)))
    # ---------------- care
    o.r('hose_off_the_netting', 'Shaking rain off the net by working the nearest post back and forth', 22, 'none',
        [k(.1, 'pole_l', x=.3, y=.2, b=.2), k(.28, 'pole_l', x=-.5, y=-.4, b=-.7, mark='rrk'), k(.46, 'pole_l', x=-.8, y=-.5, b=-.9, l=1, mark='rrk'), k(.64, 'pole_l', x=-.5, y=-.4, b=-.6, r=1, mark='RRK'), k(.84, 'net_a', x=.2, y=.3, eye='^')],
        [(.64, 'shake_dry')], g='care', act=('shake', 'net'), when=['obj_wetness>.3'], obj=[(.3, dict(shake=.4)), (.5, dict(shake=.6)), (.7, dict(shake=.3))],
        say=["Rain flew everywhere. Mostly at me.", "Shook the net. The net shook me back."])
    o.r('wash_the_skirt', 'Rubbing the dirty net skirt with a wing until the grey comes off', 22, 'wing',
        [k(.1, 'skirt_l', reach=.5, x=.3, y=.8, b=.4), k(.28, 'skirt_l', reach=1, x=.7, y=1.1, b=.8, l=1, mark='skrk'), k(.46, 'mat_front', reach=1, x=.7, y=1.3, b=.9, r=1, mark='skrk'), k(.66, 'skirt_r', reach=1, x=.7, y=1.1, b=.8, l=1, mark='skrk'), k(.88, eye='^')],
        [(.66, 'wash')], g='care', act=('scrub', 'skirt'), when=['obj_dirt>.3'])
    o.r('knot_the_loose_netting', 'Pulling the slack out of a net knot with his bill and tying it off tight', 22, 'none',
        [k(.1, x=.4, y=.1), k(.28, 'knot_a', x=1.1, y=-.4, b=-.4, mark='tg'), k(.46, 'knot_a', x=1.3, y=-.6, b=-.6, l=1, mark='tg'), k(.62, 'knot_b', x=1.4, y=-.7, b=-.7, r=1, mark='TG'), k(.82, 'knot_b', x=.4, y=.2, w=.5, eye='^')],
        [(.62, 'knot')], g='care', act=('tie', 'knot'), when=['obj_condition<.6', 'tension>.3'],
        say=["Tied it. Looks like I know what I'm doing.", "Knot's tight. Net's calm. My bill hurts."])
    o.r('chip_ice_from_the_net', 'Picking ice off the low net with the tip of a wing, one diamond at a time', 22, 'wing',
        [k(.1, 'net_a', reach=.4, x=.2, y=.2), k(.28, 'net_a', reach=1, x=.5, y=.5, b=.3, mark='tk'), k(.46, 'net_b', reach=1, x=.5, y=.5, b=.3, l=1, mark='tk'), k(.64, 'net_c', reach=1, x=.5, y=.5, b=.3, r=1, mark='tk'), k(.86, eye='^')],
        [(.64, 'chip')], g='weather', act=('chip', 'net'), when=['frost>.3'])
    o.r('knock_snow_off_the_net', 'Butting the low net upwards so the snow slides off the mat edge', 22, 'none',
        [k(.1, 'net_b', x=.3, y=.4, b=.2), k(.26, 'net_b', x=.8, y=-.3, b=-.6, mark='hmf'), k(.42, 'net_b', x=1, y=-.4, b=-.8, w=.6, mark='HMF'), k(.6, 'net_c', x=1, y=-.4, b=-.8, l=1, w=.6, mark='HMF'), k(.84, x=0, y=.8, b=.3, eye='>')],
        [(.6, 'knock')], g='weather', act=('knock', 'snow'), when=['drift>.3'],
        say=["Snow gone. Net bounced. Dignity bounced less.", "Butted a net. Won. Sort of."])
    # ---------------- use / test
    o.r('pluck_the_net_like_a_harp', 'Plucking the low net with his bill like a harp, one string at a time', 24, 'none',
        [k(.1, 'net_a', x=.5, y=.5, b=.2), k(.26, 'net_a', x=1, y=.8, b=.5, mark='twang'), k(.42, 'net_b', x=1, y=.8, b=.5, mark='twang'), k(.58, 'net_c', x=1, y=.8, b=.5, mark='twang'), k(.8, 'net_b', x=.5, y=.4, b=.1, eye='o', mark='...')],
        [(.58, 'giggle')], g='play', act=('tap', 'net'), prefer=['happy'],
        say=["Net harp. Three notes. All sharp.", "Duck concerto in N minor."])
    o.r('count_the_net_diamonds', 'Counting the net diamonds up from the mat, quietly losing count', 24, 'none',
        [k(.1, 'skirt_l', x=.3, y=.9, b=.6, mark='1'), k(.28, 'net_a', x=.9, y=-.5, b=-.8, mark='2'), k(.46, 'knot_a', x=1.3, y=-1.6, b=-1.6, w=.5, mark='3'), k(.62, 'knot_hi', x=1.4, y=-2, b=-2, w=1, eye='@', mark='4?'), k(.82, 'net_b', x=.2, y=.9, b=.4, eye='-', mark='...')],
        [], g='test', act=('count', 'net'), prefer=['curious'])
    o.r('hook_a_foot_in_the_net', 'Hooking one foot into a net diamond and hopping away on his other, testing the grip', 22, 'none',
        [k(.1, 'net_c', x=.3, y=.4, b=.4), k(.28, 'net_c', x=.5, y=.8, b=.8, l=1, mark='hn'), k(.46, 'net_c', x=.6, y=1, b=1, l=1, r=1, eye='o'), k(.64, 'net_c', x=-.4, y=-.2, b=-.6, l=1, w=1, mark='hup', eye='>'), k(.84, x=.2, b=.2, eye='-')],
        [], g='test', act=('hook', 'net'), prefer=['young'])
    o.r('peer_past_the_net_at_the_mat', 'Peering past the net at the mat, one eye then the other', 22, 'none',
        [k(.12, 'net_b', x=.4, y=.1, b=.2), k(.3, 'net_b', x=1.1, y=.6, b=.5, eye='o'), k(.5, 'net_a', x=1.2, y=.8, b=.6, eye='O', mark='hm'), k(.7, 'net_c', x=1.2, y=.8, b=.6, eye='o'), k(.9, x=.2, eye='-')],
        [], g='test', act=('peer', 'net'), shown='head')
    o.r('ring_the_post', 'Ringing the left post with his bill like a gong, then holding an ear to it', 22, 'none',
        [k(.1, 'pole_l', x=.6, y=.8, b=.5), k(.24, 'pole_l', x=1.5, y=-.6, b=-.9, mark='BONG'), k(.4, 'pole_l', x=-.4, y=1, b=.9, eye='O', mark='BONG'), k(.6, 'pole_l', x=-1.1, y=-1.3, b=-1.3, eye='o', mark='...'), k(.82, x=.2, y=.2, eye='-')],
        [], g='test', act=('ring', 'post'), prefer=['curious'])
    o.r('race_the_net_skirt', 'Racing along the net skirt from the left post to the right post and back', 22, 'none',
        [k(.1, 'pole_l', x=.6, y=.3, b=.2), k(.3, 'skirt_l', x=1.5, y=.4, b=-.4, w=1, l=1, mark='zip'), k(.5, 'skirt_r', x=1.5, y=.4, b=-.5, w=1, r=1, mark='zip'), k(.7, 'pole_r', x=1.6, y=.5, b=-.5, w=1, l=1, mark='ZIP'), k(.9, 'pole_l', x=.3, b=.1, eye='@')],
        [(.7, 'giggle')], g='play', act=('race', 'skirt'), prefer=['young', 'happy'])
    o.r('sit_on_the_mat_front', 'Sitting at the mat front with his back to the net, watching clouds', 28, 'none',
        [k(.15, 'mat_front', perch=1, x=.2, b=.5), k(.4, 'mat_front', perch=1, x=-.2, y=-.8, b=1.2, eye='o'), k(.66, 'mat_front', perch=1, x=-.2, y=-.8, b=1.3, eye='-', mark='...'), k(.88, 'mat_front', perch=1, x=.2, y=.2, b=.4, eye='^')],
        [(.66, 'doze')], g='rest', act=('sit', 'mat'), prefer=['tired'])
    o.r('lean_on_the_right_post', 'Leaning back against the right post with his eyes shut', 26, 'none',
        [k(.14, 'pole_r', x=-.6, y=.5, b=.7, l=1), k(.4, 'pole_r', x=-1.5, y=-1, b=-.7, w=.8), k(.66, 'pole_r', x=-1.1, y=.1, b=1.1, r=1, eye='-', mark='hm'), k(.9, 'pole_r', x=-.2, y=.3, b=.1, eye='^')],
        [(.66, 'doze')], g='rest', act=('lean', 'post'))
    o.r('nap_on_the_mat', 'Napping on the mat with the netting swaying past him', 40, 'none',
        [k(.12, 'mat_a', perch=1, x=.6, y=.2, b=.5, w=.3), k(.3, 'mat_a', perch=1, x=.8, y=1.3, b=1.4, eye='-'), k(.6, 'mat_b', perch=1, x=.8, y=1.5, b=1.5, w=.6, eye='-', mark='zzz'), k(.85, 'mat_b', perch=1, x=.4, y=.7, b=.6, eye='^')],
        [], g='rest', act=('nap', 'mat'), prefer=['tired'], when=['night'],
        say=["Net around me. Safe as a teabag.", "Slept in a cage. Like a pampered pet."])
    o.r('tangled_in_the_net_skirt', 'Walking into the net skirt headfirst and winding himself up in it', 24, 'none',
        [k(.12, x=.5, y=.2, b=.2), k(.3, 'skirt_l', x=1.3, y=.8, b=.8, mark='oh'), k(.5, 'skirt_l', x=1.5, y=1, b=1.1, l=1, w=1, eye='O', mark='mmf'), k(.72, 'skirt_l', x=1.7, y=.6, b=1.3, r=1, w=1, mark='POP'), k(.9, x=2, y=1, b=.5, eye='@')],
        [(.72, 'smudge')], g='mishap', act=('stuck', 'skirt'), shown='head', prefer=['young'],
        say=["Net wrapped me. Net was jealous.", "Got out. Not going to talk about how."])
    o.r('rip_a_knot_loose', 'Tugging a knot too hard so it gives with a twang and flings him back', 18, 'none',
        [k(.12, 'knot_c', x=.4, y=-.4, b=-.4), k(.3, 'knot_c', x=1.3, y=-.8, b=-.8, mark='tgg'), k(.46, 'knot_c', x=-1.4, y=-1.2, b=-1.6, w=1, eye='O', mark='TWANG'), k(.68, x=-1.6, y=1.2, b=1, r=1, l=1, eye='@'), k(.9, eye='-')],
        [(.46, 'tear')], g='mishap', act=('pull', 'knot'), prefer=['grumpy'],
        say=["Knot went. I went. The net regrets nothing.", "My fault. I would do it again."])
    o.r('bow_to_the_net', 'Bowing to the net like a dinner guest who has lost the table', 16, 'none',
        [k(.15, 'net_b', x=-.2, y=-.4, b=-.5, w=.5), k(.4, 'net_b', x=.9, y=1.7, b=1.3, w=1, l=1, mark='pray'), k(.65, 'net_b', x=1, y=2.2, b=1.6, w=1, r=1), k(.88, 'net_b', x=.1, y=-.3, w=0, eye='^')],
        [], g='show', act=('bow', 'net'))
    o.r('present_the_cage', 'Presenting the whole mat and net with a sweep of one wing', 24, 'wing',
        [k(.12, 'skirt_l', reach=.3, x=.1, y=-.4, b=-.3), k(.34, 'net_a', reach=1, x=.1, y=-.7, b=-.5, mark='behold'), k(.58, 'net_c', reach=1, x=.1, y=-.7, b=-.6, l=1), k(.82, 'skirt_r', reach=.3, x=.2, y=-.2, eye='^')],
        [], g='show', act=('present', 'mat'), prefer=['happy'],
        say=["Mat, net, bounce, regrets. All included.", "Cage with a view. Ten out of twelve."])
    # ---------------- v3 top-up: mat tricks, springs and feet in front, net and post upkeep
    o.r('seat_drop_into_the_dent', 'Dropping onto the mat on his tail end from a stiff little hop, sitting in the dent it makes', 20, 'none',
        [k(.12, 'mat_a', perch=1, x=.1, b=-1.2, w=.4), k(.3, 'mat_a', perch=1, x=.1, y=.2, b=-1.9, w=.9, l=1, r=1, mark='hup'), k(.5, 'mat_a', perch=1, x=-.6, y=1.6, b=2.4, eye='O', mark='BWUMP'), k(.72, 'mat_a', perch=1, x=.1, y=1.1, b=1.7, eye='-'), k(.9, 'mat_a', perch=1, x=.3, b=.2, eye='^')],
        [], g='use', act=('sit', 'dent'), prefer=['happy'])
    o.r('belly_hop_across_the_mat', 'Hopping across the mat flat on his belly, a little pop with each push of the wings', 22, 'none',
        [k(.12, 'mat_a', perch=1, x=1, y=1.8, b=1.8, w=.4), k(.3, 'mat_a', perch=1, x=1.8, y=2.4, b=-.6, w=1, mark='pop'), k(.5, 'mat_b', perch=1, x=1.9, y=2.5, b=1.9, w=1, mark='pop'), k(.7, 'mat_b', perch=1, x=1.7, y=2.2, b=-.5, w=.8, eye='>'), k(.9, 'mat_b', perch=1, x=.4, y=.8, b=.6, eye='@')],
        [], g='use', act=('hop', 'mat'), prefer=['young', 'happy'])
    o.r('twirl_on_the_spot', 'Twirling on the spot with a wing out until the netting blurs', 22, 'wing',
        [k(.1, 'mat_front', perch=1, reach=.3, x=.2, b=-.7, l=1), k(.28, 'mat_front', perch=1, reach=1, x=-.6, y=.5, b=-1.1, r=1, mark='whirr'), k(.48, 'mat_b', perch=1, reach=1, x=.8, y=.5, b=-1.1, l=1), k(.68, 'mat_front', perch=1, reach=1, x=-.8, y=.6, b=-1.2, r=1, mark='WHIRR'), k(.86, 'mat_front', perch=1, reach=.2, x=.2, y=1, b=.8, eye='@')],
        [], g='use', act=('spin', 'mat'), prefer=['happy'])
    o.r('freeze_mid_bounce', 'Bouncing high and freezing mid-air with a calm face while the net watches', 20, 'none',
        [k(.12, 'mat_b', perch=1, x=.1, b=.7), k(.3, 'mat_b', perch=1, x=.2, y=-.8, b=-2.6, w=.5, l=1, r=1, mark='hup'), k(.5, 'mat_b', perch=1, x=.2, y=-.8, b=-2.6, w=.5, l=1, r=1, eye='-', mark='...'), k(.72, 'mat_b', perch=1, x=.1, y=.7, b=1.4, eye='O', mark='bump'), k(.9, 'mat_b', perch=1, x=.1, b=.2, eye='^')],
        [], g='use', act=('balance', 'mat'), prefer=['curious'])
    o.r('bounce_toward_the_netting', 'Bouncing in three rising hops toward the netting and bumping the net with his chest', 24, 'none',
        [k(.1, 'mat_front', perch=1, x=.4, b=-.9), k(.28, 'mat_a', perch=1, x=.9, y=-.2, b=-1.7, w=.6, mark='boing'), k(.48, 'mat_b', perch=1, x=1.3, y=-.3, b=-2.1, w=.8, mark='boing'), k(.66, 'net_b', x=1.7, y=-.4, b=-2.4, w=1, eye='>', mark='BONG'), k(.86, 'mat_b', perch=1, x=-.4, y=.9, b=.9, eye='@')],
        [], g='use', act=('race', 'netting'), prefer=['young'])
    o.r('scramble_up_the_skirt', 'Scrabbling up the net skirt to the mat with a wing hooked ahead, ending in a belly slide', 24, 'wing',
        [k(.1, 'skirt_l', reach=.4, x=.4, y=.6, b=.4), k(.26, 'skirt_l', reach=1, x=.9, y=-.6, b=-.9, l=1, mark='hup'), k(.44, 'mat_a', perch=1, reach=1, x=1, y=-.2, b=-1, r=1), k(.62, 'mat_a', perch=1, reach=.4, x=.7, y=1.4, b=1.8, eye='@'), k(.86, 'mat_a', perch=1, reach=.1, x=.2, b=.3, eye='^')],
        [], g='use', act=('climb', 'skirt'), ages=GROWN)
    o.r('polish_the_posts', 'Polishing both posts with a wing as high as it will go, then standing back to squint', 22, 'wing',
        [k(.1, 'pole_l', reach=.5, x=.2, y=.2), k(.28, 'pole_l', reach=1, x=.4, y=-.6, b=-.9, mark='squk'), k(.5, 'pole_r', reach=1, x=.4, y=-.6, b=-.9, l=1, mark='squk'), k(.7, 'pole_r', reach=.5, x=.1, y=.4, b=.4, r=1, eye='o'), k(.9, eye='^')],
        [(.5, 'wash')], g='care', act=('polish', 'posts'), when=['obj_dirt>.4'])
    o.r('wipe_the_wet_mat_front', 'Wiping the wet mat front with his breast, back and forth, until the dark patch is gone', 24, 'none',
        [k(.1, 'mat_front', perch=1, x=.6, y=.9, b=1.4), k(.3, 'mat_front', perch=1, x=-.5, y=1.5, b=2.3, w=.4, mark='fwp'), k(.5, 'mat_b', perch=1, x=-.5, y=1.5, b=2.4, w=.5, mark='fwp'), k(.7, 'mat_a', perch=1, x=-.4, y=1.4, b=2.2, w=.4, mark='fwp'), k(.9, 'mat_a', perch=1, x=.4, y=.5, b=.6, eye='-')],
        [(.5, 'shake_dry')], g='care', act=('wipe', 'mat'), when=['obj_wetness>.5'])
    o.r('tweak_a_spring_straight', 'Tweaking a bent spring straight with his bill, then flicking it to prove it', 22, 'none',
        [k(.1, 'spring_l', x=.7, y=1, b=.7), k(.28, 'spring_l', x=1.4, y=1.8, b=1.4, mark='nk'), k(.46, 'spring_l', x=1.6, y=2, b=1.7, l=1, mark='nk'), k(.64, 'spring_l', x=1.8, y=2.1, b=1.8, r=1, mark='NK'), k(.84, 'spring_l', x=.5, y=.7, b=.4, eye='^', mark='boing')],
        [(.64, 'tweak')], g='care', act=('fit', 'spring'), when=['obj_condition<.6'], say=["Spring straight. Tension restored. Mine too.", "Fiddled. Fixed. Took credit."])
    o.r('scrape_frost_off_the_mat', 'Scraping a frost film off the mat front with the side of a foot, three rasping goes', 22, 'none',
        [k(.1, 'mat_front', perch=1, x=.6, y=.6, b=.7), k(.28, 'mat_front', perch=1, x=.9, y=.9, b=1.1, l=1, mark='zzk'), k(.46, 'mat_a', perch=1, x=.9, y=.9, b=1.1, r=1, mark='zzk'), k(.64, 'mat_b', perch=1, x=.9, y=.9, b=1.2, l=1, mark='ZZK'), k(.84, 'mat_b', perch=1, x=.3, b=.3, eye='^')],
        [(.64, 'chip')], g='weather', act=('scrape', 'mat'), when=['frost>.4'])
    o.r('scoop_snow_off_the_mat', 'Scooping a snow drift off the mat with his bill and flinging it over the skirt', 24, 'none',
        [k(.1, 'mat_front', perch=1, x=.6, y=1.1, b=.8), k(.26, 'mat_front', perch=1, x=1.6, y=2.2, b=1.8, mark='fsh'), k(.4, 'mat_front', perch=1, x=-.8, y=-.8, b=-1, w=.7, mark='fup'), k(.58, 'mat_a', perch=1, x=1.6, y=2.2, b=1.8, l=1, mark='fsh'), k(.76, 'mat_a', perch=1, x=-.7, y=-.7, b=-.9, w=.7, eye='>'), k(.9, 'mat_a', perch=1, x=.3, eye='-')],
        [(.58, 'knock')], g='weather', act=('scoop', 'drift'), when=['drift>.4'])
    o.r('huddle_at_the_far_post', 'Huddling at the far post with his neck pulled into his chest while the wind slaps the net', 30, 'none',
        [k(.15, 'pole_r', x=.6, y=1, b=1.1, w=.2), k(.4, 'pole_r', x=-.7, y=1.8, b=2, w=.7, eye='-'), k(.7, 'pole_r', x=-.8, y=1.9, b=2.1, w=.5, eye='-', mark='brr'), k(.9, 'pole_r', x=.3, y=.8, b=.8, eye='^')],
        [], g='weather', act=('shelter', 'post'), when=['windy'])
    o.r('shake_the_wet_off_his_back', 'Shaking the wet off his back at the mat front, wings snapping like wet towels', 18, 'none',
        [k(.12, 'mat_front', perch=1, x=.4, b=.5), k(.3, 'mat_front', perch=1, x=-.5, y=-1, b=-1.4, w=1, l=1, mark='brrt'), k(.46, 'mat_front', perch=1, x=.7, y=1.2, b=1.6, w=.6, r=1, mark='brrt'), k(.66, 'mat_front', perch=1, x=-.6, y=-1.1, b=-1.5, w=1, mark='BRRT'), k(.86, 'mat_front', perch=1, x=.2, eye='^')],
        [], g='weather', act=('fluff', 'feathers'), when=['wet'])
    o.r('soak_up_the_sun_on_the_mat', 'Flattening himself on the sun-warm mat with both wings out and his eyes shut', 28, 'none',
        [k(.12, 'mat_a', perch=1, x=.9, y=-.3, b=-.4), k(.34, 'mat_a', perch=1, x=-.7, y=1.7, b=2.3, w=1, eye='-'), k(.62, 'mat_b', perch=1, x=-.7, y=1.8, b=2.4, w=1, eye='-', mark='ahhh'), k(.86, 'mat_b', perch=1, x=.8, y=-.4, b=-.4, w=.2, eye='^')],
        [], g='weather', act=('warm', 'mat'), when=['sun'])
    o.r('listen_to_the_spring_row', 'Laying an ear to the spring row and hearing them tick as they settle', 22, 'none',
        [k(.12, 'spring_l', x=.4, y=.9, b=.5), k(.3, 'spring_l', x=1.1, y=1.6, b=1.1, eye='o'), k(.5, 'spring_r', x=1.2, y=1.7, b=1.2, eye='O', mark='tik'), k(.72, 'spring_r', x=1.1, y=.4, b=.3, eye='@', mark='tik'), k(.9, eye='>')],
        [], g='test', act=('listen', 'springs'), prefer=['curious'])
    o.r('weigh_the_mat_edge', 'Putting weight on the mat edge a little at a time, one foot then the other, to see if it holds', 24, 'none',
        [k(.1, 'mat_front', perch=1, x=.4, b=.5, l=1), k(.3, 'mat_front', perch=1, x=.6, y=.9, b=1, l=1, mark='bf'), k(.5, 'mat_front', perch=1, x=.6, y=1.4, b=1.5, r=1, mark='bf'), k(.7, 'mat_front', perch=1, x=.5, y=1.7, b=2.1, l=1, r=1, eye='o'), k(.9, 'mat_front', perch=1, x=.4, b=.5, eye='^')],
        [], g='test', act=('weigh', 'mat'))
    o.r('dance_a_bouncy_jig', 'Dancing a bouncy jig along the mat, every hop a little higher than the one before', 26, 'none',
        [k(.1, 'mat_a', perch=1, x=.4, b=-.4, l=1), k(.28, 'mat_a', perch=1, x=.4, y=-.2, b=-1.4, r=1, w=.5), k(.46, 'mat_b', perch=1, x=.4, y=-.3, b=-1.9, l=1, w=.8), k(.66, 'mat_b', perch=1, x=.3, y=-.5, b=-2.5, r=1, l=1, w=1, eye='^', mark='hup'), k(.86, 'mat_b', perch=1, x=.3, b=.4)],
        [], g='play', act=('dance', 'mat'), prefer=['happy'])
    o.r('hop_the_spring_row', 'Hopping the spring row front to back and over the foot pads, one coil at a time', 22, 'none',
        [k(.1, 'spring_l', x=.8, b=-.7, l=1), k(.28, 'foot_l', x=1.4, b=-1.3, r=1, w=.7, mark='hup'), k(.48, 'spring_r', x=1.5, b=-1.4, l=1, w=.7), k(.68, 'foot_r', x=1.6, b=-1.3, r=1, w=.9, mark='HUP'), k(.86, 'spring_r', x=.4, b=.4, eye='@')],
        [], g='play', act=('hop', 'springs'), prefer=['young'])
    o.r('chase_himself_round_the_feet', 'Chasing his own tail round the left foot pad and then the right, getting nowhere fast', 22, 'none',
        [k(.1, 'foot_l', x=1, y=.6, b=.3), k(.28, 'foot_l', x=2.1, y=1.7, b=1.3, w=1, l=1), k(.46, 'foot_r', x=-1.1, y=1.3, b=.7, r=1, w=1), k(.64, 'foot_l', x=2.2, y=1.8, b=1.4, w=1, l=1), k(.84, 'foot_r', x=.4, y=.5, eye='@')],
        [], g='play', act=('chase', 'legs'), prefer=['grumpy'])
    o.r('kick_a_foot_pad_along', 'Kicking a foot pad along the ground and trotting after it, like a very small striker', 20, 'none',
        [k(.1, 'foot_l', x=.5, y=.5, b=.4), k(.28, 'foot_l', x=.8, y=.9, b=-.7, l=1, mark='tok'), k(.46, 'foot_l', x=1.2, y=1.1, b=-1.2, r=1, w=.6, mark='TOK'), k(.66, 'foot_r', x=1.4, y=1.3, b=-.7, l=1), k(.86, 'foot_r', x=.4, y=.5, eye='^')],
        [], g='play', act=('kick', 'pad'), prefer=['happy'])
    o.r('sulk_at_the_netting', 'Sulking with his bill poked at the netting and his back turned to the mat', 26, 'none',
        [k(.15, 'net_a', x=.6, y=1.2, b=.8), k(.4, 'net_a', x=1, y=1.7, b=1.3, eye='-'), k(.7, 'net_c', x=1.1, y=1.9, b=1.5, eye='-', mark='hmph'), k(.9, 'net_c', x=.4, y=.5, b=.3, eye='^')],
        [], g='rest', act=('sulk', 'net'), prefer=['sad', 'grumpy'], say=["Net is judging. I can feel the diamonds.", "Stuck in a hammock for ants. Hmph."])
    o.r('wait_by_the_mat_edge', 'Waiting at the mat edge for a bounce that has not been scheduled', 28, 'none',
        [k(.12, 'mat_front', perch=1, x=.3, y=-.8, b=-.5), k(.34, 'mat_front', perch=1, x=.5, y=-1.4, b=-1, eye='o', mark='...'), k(.56, 'mat_front', perch=1, x=.3, y=1, b=1, l=1, eye='-'), k(.8, 'mat_front', perch=1, x=.4, y=-1.5, b=-1.1, r=1, eye='o'), k(.94, 'mat_front', perch=1, eye='>')],
        [], g='rest', act=('wait', 'mat'), prefer=['lonely'])
    o.r('sit_by_the_right_foot', 'Sitting by the right foot pad with his back to it and his feet stuck out', 26, 'none',
        [k(.15, 'foot_r', x=-.4, b=.8), k(.38, 'foot_r', x=-.6, y=.5, b=1.5, l=1, r=1, eye='o'), k(.64, 'foot_r', x=-.7, y=.6, b=1.7, eye='-', mark='sigh'), k(.88, 'foot_r', x=-.3, y=.3, b=.5, eye='^')],
        [], g='rest', act=('sit', 'pad'), prefer=['tired'])
    o.r('roll_off_the_mat', 'Rolling off the mat edge in a flap of wings and landing on his back staring at the sky', 20, 'none',
        [k(.12, 'mat_b', perch=1, x=-.3, y=.2, b=1.3, w=.3), k(.3, 'mat_front', perch=1, x=2.3, y=2.2, b=-2.1, w=.5, mark='whoa'), k(.5, 'mat_front', perch=1, x=-2.4, y=-2.5, b=2.9, w=.8, l=1, r=1, eye='O', mark='THUMP'), k(.74, 'mat_front', perch=1, x=1.5, y=2.5, b=2.1, eye='@'), k(.9, 'mat_front', perch=1, x=.1, b=1, eye='>')],
        [(.5, 'bruise')], g='mishap', act=('fold', 'mat'), say=["Rolled off a trampoline. Rated it. Zero stars.", "Landed on my back. Sky looks fine."])
    o.r('bonk_head_on_the_post', 'Straightening up too quick and cracking his head against the near post', 18, 'none',
        [k(.12, 'pole_l', x=.6, y=1.3, b=1.2), k(.3, 'pole_l', x=.7, y=1.7, b=1.6, l=1), k(.44, 'pole_l', x=1, y=-1.5, b=-1.4, w=1, eye='O', mark='DONG'), k(.64, x=-.9, y=1.5, b=1, r=1, eye='@'), k(.88, eye='-')],
        [(.44, 'tear')], g='mishap', act=('knock', 'pole'))
    o.r('catch_a_foot_in_a_coil', 'Poking a foot past a spring coil for a look and ending up hopping with a spring attached', 22, 'none',
        [k(.12, 'spring_r', x=.5, y=.9, b=.5), k(.3, 'spring_r', x=.9, y=1.5, b=1.1, l=1, mark='hm'), k(.5, 'spring_r', x=1.2, y=1.7, b=1.4, l=1, eye='O', mark='mmf'), k(.7, 'spring_r', x=-1.3, y=-.9, b=-1.5, l=1, w=1, mark='POP'), k(.9, x=.5, y=1, b=.7, eye='@')],
        [], g='mishap', act=('hook', 'spring'), ages=GROWN, prefer=['curious'])
    o.r('stub_a_toe_on_the_foot_pad', 'Stubbing a toe against the left foot pad and hopping in a furious little circle', 18, 'none',
        [k(.12, 'foot_r', x=.5, y=.8, b=.5), k(.3, 'foot_r', x=.9, y=1.2, b=-.6, l=1, mark='tok'), k(.46, 'foot_r', x=-.6, y=-.8, b=-1.7, l=1, w=1, eye='O', mark='FFS'), k(.66, 'foot_r', x=-1.1, y=1.3, b=.7, r=1, eye='@'), k(.88, eye='>')],
        [], g='mishap', act=('knock', 'pad'), prefer=['grumpy'], say=["Toe lost. Pad undamaged. Language unchanged.", "Hopped it off. Told nobody."])
    o.r('boing_for_the_clouds', 'Calling boing at the clouds from the middle of the mat, getting no answer', 24, 'none',
        [k(.12, 'mat_a', perch=1, x=-.4, y=.9, b=.9), k(.3, 'mat_b', perch=1, x=-.7, y=-2, b=-2.4, w=.3, mark='boing'), k(.5, 'mat_b', perch=1, x=-1.1, y=-2.4, b=-2.9, w=.6, eye='^', mark='BOING'), k(.72, 'mat_a', perch=1, x=-.2, y=.8, b=1, eye='o', mark='...?'), k(.9, 'mat_a', perch=1, x=-.1, b=.1, eye='-')],
        [], g='show', act=('sing', 'mat'), prefer=['lonely'], say=["Clouds ignored it. Clouds ignore everyone.", "Sang boing. Got boing back. In my head."])
    o.r('compare_the_net_knots', 'Comparing the net knots one by one, head tilting, deciding the high one is smugger', 24, 'none',
        [k(.12, 'knot_a', x=.5, y=-.6, b=-.6), k(.32, 'knot_b', x=1, y=-1.1, b=-1.1, eye='o'), k(.52, 'knot_c', x=1, y=-1.2, b=-1.2, eye='O'), k(.72, 'knot_hi', x=.9, y=-1.6, b=-1.6, eye='-', mark='hm'), k(.9, 'knot_a', x=.4, y=-.5, b=-.5, eye='>')],
        [], g='show', act=('compare', 'knots'), prefer=['curious'])
    o.r('pose_with_the_netting_behind', 'Posing at the mat front with the whole net looming over his shoulders, wings open', 18, 'none',
        [k(.14, 'mat_front', perch=1, x=.7, y=.5, b=.7), k(.4, 'mat_front', perch=1, x=-.8, y=-1.3, b=-1.8, w=.6, l=1, eye='^'), k(.66, 'mat_front', perch=1, x=1.1, y=-1.5, b=-1.5, w=1, r=1), k(.9, 'mat_front', perch=1, x=.4, b=.4)],
        [], g='show', act=('pose', 'mat'), prefer=['happy'])
    o.r('argue_with_the_posts', 'Arguing with each post in turn about which one is leaning, and losing to both', 22, 'wing',
        [k(.12, 'pole_l', reach=.5, x=.5, y=.2, b=.1), k(.3, 'pole_l', reach=1, x=1, y=-.4, b=.3, mark='YOU'), k(.5, 'pole_r', reach=1, x=1.1, y=-.6, b=.4, r=1, mark='NO, YOU'), k(.7, 'pole_l', reach=1, x=.7, y=.4, b=.9, l=1, eye='>', mark='!!'), k(.9, eye='-')],
        [], g='show', act=('argue', 'pole'), prefer=['grumpy'], say=["Posts agree. Both wrong. Both smug.", "Won the argument. Posts still standing."])
    o.emit()


if __name__ == '__main__':
    toy_slide()
    rainbow_slide()
    water_slide()
    water_slide_mega()
    trampoline()
    toy_trampoline()
