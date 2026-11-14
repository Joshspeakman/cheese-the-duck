"""Display v3 (user decision 2026-11-14: a shared host counts host acts + item acts).
trophy_case (placed, 48, its own drawing) carries the shared case acts once: glass (breath fog, nose prints, rime, glare), slats, studs, rail, doors, base.
The eight shown things (ancient_amulet, lucky_charm, earth_token, sky_token, water_token, magpie_friendship_charm, rainbow_charm, dance_medal) author only what
that thing alone allows (lifting it out, what he does with it in his bill, its cord / ribbon / emblem / element, duets), 12 each, and declare no case state.
Host drawing (106 cols x 78 rows, 7.19 px a row, standing line row 75): base slats every fifth column rows 67-71 (58-29 px), `o` studs at each end of row 70 (36 px),
bottom rail row 72 (22 px), trim bars rows 65 and 62 (72 and 93 px), lower shelf board row 63 (86 px), `(=)` plates on the left frame (rows 63, 53, 43...),
centre door seam col 53 rows 14-60, lowest shelf ledge row 61 (101 px) with three `[____]` stands at row 60 (108 px; slots centred on cols 22, 48, 74),
glass panes between the frame posts and the seam. The shown thing is the anchor `item` (115 px, the lowest slot). Anchors are literal (col/105, row/77)."""
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


def P(c, r, *fl):
    return (round(c / 105, 4), round(r / 77, 4), *([' '.join(fl)] if fl else []))


COUNT = {}


# @@trophy_case
def trophy_case():
    o = Obj('trophy_case', 'placed',
            parts=dict(slat='the vertical base slats along the foot of the case', stud='the round studs at each end of the base', rail='the bottom rail the case stands on',
                       trim='the two horizontal trim bars above the base', sill='the lower shelf board in front of the first stands', plate='the (=) plates on the frame post',
                       ledge='the lowest shelf ledge', stand='the three small stands on the ledge', seam='the seam where the two glass doors meet',
                       frame='the frame post at the side', glass='the glass pane of the doors'),
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), scuffs=(0, 0, 1), dull=(.3, 0, 1), rime=(0, 0, 1), glare=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('scuffs', 'rate', -.0002, 'always'), ('dull', 'rate', .0004, 'always'),
                     ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm'), ('glare', 'rate', .002, 'sun'), ('glare', 'rate', -.001, 'always')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], scrawl=[('fog', 'mul', .4)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         smooth=[('scuffs', 'set', 0)], scuff=[('scuffs', 'add', .4)], shine=[('dull', 'set', 0)], defrost=[('rime', 'set', 0)], scrape=[('rime', 'mul', .2)],
                         shade=[('glare', 'mul', .2)], sweep=[('obj.dirt', 'add', -.3)], dust=[('obj.dirt', 'add', -.4)], dry=[('obj.wetness', 'add', -.3)],
                         smudge=[('obj.dirt', 'add', .2)], jig=[('need.fun', 'add', 2)], mates=[('need.social', 'add', 2)], rest=[('need.energy', 'add', 2)],
                         primp=[('need.cleanliness', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('scuffs', .3, '.:.:.', 'rail', 'dust'),
                   ('rime', .3, '*-*-*', 'trim_hi', 'frost'), ('glare', .3, '. * .', 'sill_r', 'glow'), ('dull', .6, '. . .', 'stud_l', 'dust')],
            anchors=dict(slat_a=P(26, 69), slat_b=P(41, 67), slat_c=P(56, 70), slat_d=P(71, 68), slat_e=P(86, 69),
                         stud_l=P(10, 70), stud_r=P(95, 70), rail=P(53, 72, 'surface'), rail_l=P(30, 72, 'surface'), rail_r=P(78, 72, 'surface'),
                         trim_lo=P(50, 65), trim_hi=P(50, 62), sill=P(40, 63), sill_r=P(70, 63), plate_lo=P(11, 63),
                         ledge=P(30, 61), ledge_r=P(66, 61), stand_l=P(22, 60), stand_m=P(48, 60), stand_r=P(74, 60), seam_lo=P(53, 58),
                         frame_l=P(11, 66), frame_r=P(91, 60), glass_l=P(15, 59), glass_m=P(49, 58), glass_r=P(88, 59)))
    # ---------------- care
    o.r('wipe_the_breath_mist_off', 'Clearing the breath mist off the glass in wide wipes of the wing', 16, 'wing',
        [k(.12, 'glass_l', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'glass_l', reach=1, x=.7, y=-.5, b=-.3, w=.3), k(.5, 'glass_m', reach=1, x=.7, y=-.4, b=-.2),
         k(.7, 'glass_m', reach=1, x=.6, y=-.6, b=-.4, l=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['grown'], say=["Clear. Now the stands can watch me back.", "Mist gone. So is the evidence."])
    o.r('buff_the_nose_prints_off', 'Buffing the nose prints off the pane near the frame with a wipe of the wing tip', 18, 'wing',
        [k(.12, 'glass_r', reach=.6, x=.3, y=-.2, b=.3), k(.3, 'glass_r', reach=1, x=.5, y=-.3, b=.5, mark='squeak'), k(.5, 'frame_r', reach=1, x=.6, y=-.4, b=.2, r=1),
         k(.7, 'glass_r', reach=1, x=.5, y=-.3, b=.4, l=1), k(.88, y=-.2, eye='-')],
        [(.5, 'buff')], g='care', act=('wipe', 'prints'), when=['prints>.3'], prefer=['curious'])
    o.r('scrub_the_toe_scuffs_off_the_rail', 'Scrubbing the toe scuffs off the bottom rail with the side of his bill, end to end', 18, 'none',
        [k(.12, 'rail_l', x=1, y=1.3, b=.7), k(.3, 'rail_l', x=1.2, y=1.4, b=.9, l=1, mark='rub'), k(.5, 'rail', x=1.2, y=1.4, b=.9), k(.7, 'rail_r', x=1.3, y=1.4, b=.9, r=1),
         k(.88, 'rail_r', x=.8, y=.9, b=.6, eye='^')],
        [(.5, 'smooth')], g='care', act=('scrub', 'scuffs'), when=['scuffs>.3'], say=["Scrubbed my own footprints off. Looks like a clean getaway.", "Rail's clean. The next scuff is on someone else."])
    o.r('polish_the_end_studs', 'Polishing the two end studs of the base with his bill, left then right, till they shine', 20, 'none',
        [k(.12, 'stud_l', x=1.1, y=1.1, b=.6, mark='rub'), k(.3, 'stud_l', x=.9, y=.9, b=.8, l=1), k(.5, x=-.3, y=-.3, b=-.5, w=.8, r=1), k(.7, 'stud_r', x=1.2, y=1.1, b=.7, mark='rub'),
         k(.88, 'stud_r', x=.9, y=.9, b=.6, eye='^')],
        [(.7, 'shine')], g='care', act=('polish', 'studs'), when=['dull>.4'], prefer=['happy'], say=["Brass again. I can see my own chin in it.", "Two studs gleaming. The rest of the case can catch up."])
    o.r('sweep_the_ledge_with_a_twig', 'Sweeping the dust off the lowest ledge and round the stands with the end of a twig', 18, 'twig',
        [k(.12, 'ledge', reach=.6, x=.3, y=.2), k(.3, 'ledge', reach=1, x=.5, y=.4, b=.3, mark='shff'), k(.5, 'stand_l', reach=1, x=.5, y=.3, b=.4),
         k(.7, 'ledge_r', reach=1, x=.5, y=.4, b=.3, l=1), k(.88, eye='^')],
        [(.5, 'sweep')], g='care', act=('sweep', 'ledge'), when=['obj_dirt>.3'])
    o.r('dry_the_rain_streaks_off_the_glass', 'Drying the rain streaks off the lower pane with a wing, sill to trim', 18, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'sill', reach=1, x=.7, y=-.5, b=-.3, w=.3), k(.5, 'trim_hi', reach=1, x=.6, y=-.3, b=.2, r=1),
         k(.7, 'trim_lo', reach=1, x=.5, y=-.2, b=.3), k(.88, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'])
    o.r('chip_the_rime_off_the_frame', 'Chipping the rime off the frame post and the low plate with the tip of a wing', 16, 'wing',
        [k(.12, 'plate_lo', reach=.6, x=.2, y=-.2, b=.3), k(.3, 'plate_lo', reach=1, x=.5, y=-.4, b=.5, mark='tk'), k(.5, 'frame_l', reach=1, x=.5, y=-.3, b=.6, l=1, mark='tk'),
         k(.7, 'plate_lo', reach=1, x=.4, y=-.4, b=.5), k(.88, eye='-')],
        [(.5, 'defrost')], g='care', act=('chip', 'rime'), when=['rime>.3'], ages=GROWN)
    o.r('shield_the_pane_from_the_glare', 'Guarding the pane from the sun glare with one wing held out flat like a visor', 20, 'wing',
        [k(.12, 'glass_m', reach=.5, x=.2, y=-.4, b=.1), k(.3, 'glass_m', reach=1, x=.3, y=-.7, b=-.4, w=.8, eye='-'), k(.55, 'glass_m', reach=1, x=.3, y=-.8, b=-.5, w=1, eye='>'),
         k(.8, 'seam_lo', reach=1, x=.2, y=-.4, b=-.2), k(.9, eye='^')],
        [(.55, 'shade')], g='care', act=('guard', 'glare'), when=['glare>.3'], prefer=['curious'])
    o.r('polish_the_slats_with_a_wing', 'Polishing the dust off the base slats with the flat of a wing, left to right', 20, 'wing',
        [k(.12, 'slat_a', reach=.5, x=.4, y=.8, b=.5), k(.3, 'slat_b', reach=1, x=.7, y=1.1, b=.8, l=1), k(.5, 'slat_c', reach=1, x=.8, y=1.2, b=.9), k(.7, 'slat_d', reach=1, x=.8, y=1.2, b=.9, r=1),
         k(.88, 'slat_e', reach=.6, x=.5, y=.8, eye='^')],
        [(.5, 'dust')], g='care', act=('polish', 'slats'), when=['obj_dirt>.4'])
    # ---------------- use
    o.r('huff_a_fog_onto_the_glass', 'Blowing a long huff at the pane until it fogs up', 14, 'none',
        [k(.15, 'glass_l', x=.8, y=-.5, b=.2), k(.35, 'glass_l', x=1.1, y=-.7, b=.4, w=.4, mark='haaah'), k(.6, 'glass_l', x=1.1, y=-.8, b=.5, eye='O'), k(.85, x=.3, y=-.3, eye='^')],
        [(.35, 'huff')], g='use', act=('blow', 'glass'), prefer=['curious'], say=["Fogged it. Weather, but mine.", "Breath on glass. I am basically a cloud."])
    o.r('squash_his_bill_against_the_pane', 'Pressing his bill flat against the pane to look at the stands', 16, 'none',
        [k(.15, 'glass_m', x=.9, y=-.4, b=.3), k(.3, 'glass_m', x=1.3, y=-.7, b=.5, mark='squish'), k(.6, 'glass_m', x=1.4, y=-.7, b=.6, eye='O'), k(.85, x=.2, y=-.2, eye='-')],
        [(.3, 'nose')], g='use', act=('press', 'glass'), prefer=['young'])
    o.r('peck_a_rude_word_into_the_fog', 'Pecking a rude word into the fogged pane and wiping half of it out again', 18, 'none',
        [k(.12, 'glass_r', x=.8, y=-.4, b=.2), k(.3, 'glass_r', x=1.2, y=-.6, b=.4, mark='tk'), k(.45, 'glass_r', x=1.2, y=-.7, b=.3, mark='tk'), k(.62, 'glass_r', x=1.1, y=-.5, b=.5, l=1, eye='>'),
         k(.85, eye='^')],
        [(.62, 'scrawl')], g='use', act=('peck', 'mist'), when=['fog>.3'], prefer=['grumpy'], say=["Wrote what I think of the stands. Smudged the worst bit.", "A word of three letters. It was 'arse'."])
    o.r('knock_twice_on_the_door_seam', 'Knocking twice on the door seam with the knuckle of his bill and waiting', 14, 'none',
        [k(.15, x=.4, y=-.3), k(.3, 'seam_lo', x=1.2, y=-.7, b=.2, mark='tok'), k(.45, 'seam_lo', x=.4, y=-.2), k(.62, 'seam_lo', x=1.3, y=-.7, b=.3, mark='tok'), k(.85, x=.2, y=-.3, eye='-')],
        [], g='use', act=('knock', 'doors'), prefer=['curious'], say=['Knocked twice. The case is out. Or ignoring me.', 'No one home but a trophy stand.'])
    o.r('hook_a_wing_in_the_seam_and_heave', 'Hooking a wing into the door seam and heaving to open the doors', 20, 'wing',
        [k(.12, 'seam_lo', reach=.5, x=.4, y=-.3, b=.2), k(.3, 'seam_lo', reach=1, x=.6, y=-.5, b=.5, l=1), k(.5, 'seam_lo', reach=1, x=.7, y=-.4, b=.9, r=1, mark='hnngh'),
         k(.72, 'seam_lo', reach=1, x=.2, y=-.2, b=.2, eye='>'), k(.9, eye='-')],
        [], g='use', act=('open', 'doors'), say=["Locked. Of course it is. Who locks a duck out?", "Heaved till my wing creaked. The doors won."])
    o.r('peer_in_at_the_three_stands', 'Peering in at the three stands, left to right, for anything left on them', 22, 'none',
        [k(.12, 'stand_l', x=.8, y=-.5, b=.2), k(.3, 'stand_l', x=1.1, y=-.7, b=.3, eye='O'), k(.5, 'stand_m', x=1.1, y=-.7, b=.2, eye='O'), k(.7, 'stand_r', x=1.1, y=-.7, b=.2, eye='-'),
         k(.88, x=.2, y=-.3, eye='^')],
        [], g='use', act=('peer', 'stands'), ages=GROWN)
    o.r('tap_each_stand_with_a_twig', 'Tapping each of the three stands with a twig to hear which one rings hollow', 22, 'twig',
        [k(.12, 'stand_l', reach=.6, x=.3, y=-.3), k(.3, 'stand_l', reach=1, x=.6, y=-.6, b=-.3, mark='tink'), k(.5, 'stand_m', reach=1, x=.6, y=-.6, b=-.3, mark='tonk'),
         k(.7, 'stand_r', reach=1, x=.6, y=-.6, b=-.3, mark='tink'), k(.88, eye='-')],
        [], g='use', act=('tap', 'stands'), ages=GROWN, say=["Tink, tonk, tink. Solid wood, all three. Disappointing.", "Tapped the stands like a doctor. They're all fine."])
    # ---------------- play
    o.r('drum_along_the_slats', 'Drumming his bill along the base slats from the left end to the right', 20, 'none',
        [k(.12, 'slat_a', x=1.1, y=1.2, b=.5, mark='tk'), k(.28, 'slat_b', x=1.1, y=1.1, b=.6, mark='tk'), k(.44, 'slat_c', x=1.2, y=1.2, b=.6, l=1, mark='tk'),
         k(.6, 'slat_d', x=1.1, y=1.1, b=.6, mark='tk'), k(.76, 'slat_e', x=1.2, y=1.2, b=.7, r=1, mark='tk'), k(.9, eye='^')],
        [(.76, 'jig')], g='play', act=('drum', 'slats'), prefer=['happy'], say=["Slats make a rubbish drum. I'm in a band now.", "Rat-a-tat. The case has rhythm, who knew."])
    o.r('race_the_length_of_the_rail', 'Running a race along the bottom rail from the left end to the right, both feet on it', 18, 'none',
        [k(.12, 'rail_l', perch=1, x=.5, y=.3, b=.4), k(.3, 'rail_l', perch=1, x=1, y=.4, b=-.3, w=.6, l=1), k(.5, 'rail', perch=1, x=1.3, y=.4, b=-.4, w=.8, r=1),
         k(.7, 'rail_r', perch=1, x=1.4, y=.4, b=-.3, w=.8, l=1, eye='>'), k(.88, 'rail_r', perch=1, x=.4, b=.2, eye='^')],
        [], g='play', act=('race', 'rail'), prefer=['young', 'happy'], say=['Rail to rail in no time. I win. Not one timer present.', 'Fastest duck on this rail. Only duck on this rail.'])
    o.r('hop_the_gaps_between_the_slats', 'Hopping along the foot of the case, one foot at a time, tapping every slat he passes', 20, 'none',
        [k(.12, 'slat_b', x=.9, y=1, b=-.5, l=1), k(.3, 'slat_c', x=1, y=1.1, b=-.7, r=1, mark='tk'), k(.5, 'slat_d', x=1, y=1, b=-.6, l=1), k(.7, 'slat_e', x=1.1, y=1.1, b=-.7, r=1),
         k(.88, eye='^')],
        [], g='play', act=('hop', 'slats'), prefer=['young'])
    o.r('peek_round_the_left_stud', 'Seeking out the left stud, peeking round it, ducking back and peeking again', 18, 'none',
        [k(.15, 'stud_l', x=1.3, y=.9, b=.4, eye='o'), k(.32, x=-.9, y=-.1, b=-.2), k(.5, 'stud_l', x=1.5, y=1, b=.5, eye='O'), k(.68, x=-1, y=-.2, b=-.3), k(.85, 'stud_l', x=1.2, y=.8, b=.3, eye='^')],
        [], g='play', act=('seek', 'stud'), prefer=['young'])
    o.r('chase_his_reflection_across_the_pane', 'Chasing his reflection across the pane, left post to right post and back again', 20, 'wing',
        [k(.12, 'glass_l', reach=.6, x=.6, y=-.3, b=.3), k(.3, 'glass_m', reach=1, x=1, y=-.4, b=-.2, mark='gotcha'), k(.5, 'glass_r', reach=1, x=1.1, y=-.4, b=-.3, l=1, eye='>'),
         k(.72, 'glass_m', reach=1, x=-.5, y=-.2, b=.2, r=1), k(.88, eye='@')],
        [(.5, 'mates')], g='play', act=('chase', 'reflection'), prefer=['happy', 'curious'])
    o.r('shoulder_the_frame_post', 'Shoving the frame post with his shoulder to see whether the whole case budges', 18, 'none',
        [k(.15, 'frame_l', x=.6, y=.6, b=.8), k(.34, 'frame_l', x=1, y=.9, b=1.4, mark='hup'), k(.5, 'frame_l', x=1.2, y=1, b=1.8, l=1, r=1, eye='>'), k(.7, x=-.5, y=.2, b=.4),
         k(.88, eye='-')],
        [], g='play', act=('shove', 'frame'), ages=GROWN, prefer=['grumpy'])
    # ---------------- test
    o.r('lick_the_bottom_rail', 'Tasting the bottom rail with a lick to test whether it is real brass', 14, 'none',
        [k(.15, 'rail_r', x=.9, y=1.3, b=.8), k(.35, 'rail_r', x=1.2, y=1.6, b=1, eye='-', mark='...'), k(.55, 'rail_r', x=-.5, y=-.2, b=.2, eye='>', mark='bleh'), k(.85, x=.1, eye='-')],
        [], g='test', act=('taste', 'rail'), prefer=['young', 'curious'], say=["Cold. Tastes of nothing. Expensive nothing.", "Not brass. I'd know. I've licked worse."])
    o.r('ear_against_the_slats', 'Listening with an ear pressed against the slats for a hum from the case', 16, 'none',
        [k(.15, 'slat_c', x=.7, y=1.4, b=.7), k(.35, 'slat_c', x=.5, y=1.8, b=1, eye='-'), k(.6, 'slat_d', x=.5, y=1.8, b=1, eye='O'), k(.85, x=.1, y=.3, eye='^')],
        [], g='test', act=('listen', 'slats'), say=['Wood. Quiet wood. Might be the case sulking.', 'Heard my own pulse. Wrong thing, still alive.'])
    o.r('count_the_studs_out', 'Counting out the studs, one at each end, and getting two both times', 16, 'none',
        [k(.12, 'stud_l', x=1, y=1, b=.6, mark='one'), k(.3, x=-.2, y=.2, b=.2, w=.3), k(.5, 'stud_r', x=1.2, y=1.1, b=.7, mark='two'), k(.7, x=-.2, y=.2, b=.2, w=.3), k(.88, 'stud_l', x=.8, y=.9, b=.4, eye='@')],
        [], g='test', act=('count', 'studs'), prefer=['curious'])
    o.r('try_the_door_seam_with_a_shoulder', 'Testing the door seam with a shoulder and the pane beside it to see whether the case is locked', 20, 'none',
        [k(.15, 'seam_lo', x=.5, y=-.3, b=.5), k(.34, 'seam_lo', x=.9, y=-.5, b=1.2, mark='thunk'), k(.5, 'glass_m', x=.9, y=-.4, b=1.3, l=1), k(.7, 'seam_lo', x=-.3, y=-.1, b=.3, eye='>'),
         k(.88, eye='-')],
        [], g='test', act=('test', 'doors'), ages=GROWN)
    o.r('lean_on_a_slat_to_weigh_the_case', 'Weighing the case by leaning on a slat with all his weight and feeling for give', 18, 'none',
        [k(.15, 'slat_b', x=.6, y=.8, b=.6), k(.35, 'slat_b', x=.9, y=1.1, b=1.4, eye='>'), k(.55, 'slat_b', x=1, y=1.2, b=1.8, l=1), k(.78, x=-.3, y=.1, b=.2, eye='-'), k(.9, eye='^')],
        [], g='test', act=('weigh', 'case'))
    o.r('knock_a_slat_to_hear_the_hollow', 'Knocking a single slat with his bill and cocking his head to hear it ring', 14, 'none',
        [k(.15, 'slat_e', x=.8, y=1, b=.4), k(.3, 'slat_e', x=1.3, y=1.4, b=.8, mark='tonk'), k(.5, x=.2, y=.3, b=.2, w=.4, eye='O'), k(.75, 'slat_e', x=1.1, y=1.2, b=.5, eye='-')],
        [], g='test', act=('knock', 'slats'))
    # ---------------- rest
    o.r('doze_off_with_his_bill_on_the_rail', 'Napping with his bill resting at the bottom rail', 28, 'none',
        [k(.15, 'rail', x=.8, y=1.2, b=.8), k(.4, 'rail', x=1.1, y=1.9, b=1.4, eye='-'), k(.7, 'rail', x=1.1, y=2, b=1.5, eye='-', mark='zzz'), k(.9, x=.3, y=.4, eye='^')],
        [(.7, 'rest')], g='rest', act=('nap', 'rail'), when=['tired'], say=['Rail makes a decent pillow. Cold, but decent.', 'Out like a light. A very small light.'])
    o.r('sulk_with_his_back_to_the_slats', 'Turning his tail to the case and sulking with his back against the slats', 22, 'none',
        [k(.15, 'slat_a', x=-.8, y=.4, b=.6), k(.4, 'slat_a', x=-1.2, y=1, b=1.2, eye='-'), k(.7, 'slat_a', x=-1.3, y=1.2, b=1.3, eye='-', mark='hmph'), k(.9, x=-.3, y=.3)],
        [], g='rest', act=('sulk', 'slats'), when=['sad'], say=['Back to the case. It knows what it did.', 'Sulking at furniture. Peak form.'])
    o.r('lean_a_shoulder_on_the_end_stud', 'Leaning a shoulder against the end stud and sighing at the closed doors', 20, 'none',
        [k(.15, 'stud_r', x=-.4, y=.4, b=.5), k(.4, 'stud_r', x=-.7, y=.7, b=1, eye='-'), k(.7, 'stud_r', x=-.7, y=.7, b=1.1, eye='-', mark='sigh'), k(.9, x=-.2, y=.2)],
        [], g='rest', act=('lean', 'stud'), say=['Leaned for a bit. The stud held. Teamwork.', 'Sighed at the doors. They did not sigh back.'])
    o.r('sit_on_the_rail_and_dangle', 'Sitting on the bottom rail with his feet dangling and watching the yard', 24, 'none',
        [k(.15, 'rail_l', perch=1, x=.2, y=.5, b=1.3), k(.4, 'rail_l', perch=1, x=.1, y=.5, b=1.6, l=1), k(.65, 'rail_l', perch=1, x=.1, y=.5, b=1.6, r=1), k(.88, 'rail_l', perch=1, x=.3, y=.3, b=1)],
        [(.65, 'rest')], g='rest', act=('sit', 'rail'))
    o.r('fluff_up_at_his_own_reflection', 'Fluffing his feathers at his reflection in the lower pane, one cheek and then the other', 20, 'wing',
        [k(.12, 'glass_l', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'glass_l', reach=1, x=.6, y=-.4, b=.5, w=.3, eye='^'), k(.52, 'glass_m', reach=1, x=.6, y=-.4, b=.6, l=1), k(.75, 'glass_l', reach=1, x=.5, y=-.3, b=.4, r=1, eye='^'),
         k(.9, eye='-')],
        [(.52, 'primp')], g='rest', act=('fluff', 'reflection'), prefer=['happy'], say=["Handsome. The glass agrees, which is all I ask of glass.", "One cheek, other cheek. Done. Devastating."])
    # ---------------- weather
    o.r('warm_his_back_on_the_sunny_slats', 'Warming his back against the sun-heated slats with his wings half open', 24, 'none',
        [k(.15, 'slat_d', x=-.5, y=.4, b=.6), k(.4, 'slat_d', x=-.8, y=.7, b=1, w=.4, eye='-'), k(.7, 'slat_d', x=-.8, y=.7, b=1.1, w=.5, eye='-'), k(.9, x=-.2, y=.3)],
        [], g='weather', act=('warm', 'slats'), when=['sun'], say=['Slats are warm. Back is warm. Mood: warm.', 'Sun on the wood, wood on my back. Peak duck.'])
    o.r('brace_against_the_foot_in_the_storm', 'Bracing his back against the foot of the case in the storm, rain drumming on the glass', 32, 'none',
        [k(.12, 'slat_c', x=-.6, y=.5, b=.6), k(.3, 'slat_c', x=-1.4, y=1.6, b=1.8, eye='-'), k(.5, 'stud_r', x=-1.2, y=1.2, b=1.4, l=1, mark='brr'), k(.7, 'stud_r', x=-.5, y=.4, b=2.2, r=1, w=.5),
         k(.92, x=-.2, y=.2)],
        [], g='weather', act=('brace', 'case'), when=['wet', 'storm'])
    o.r('scrape_the_ice_off_the_sill', 'Scraping the ice off the lower shelf board with a twig, end to end', 20, 'twig',
        [k(.12, 'sill', reach=.6, x=.3, y=.2, b=.3), k(.3, 'sill', reach=1, x=.5, y=.4, b=.5, mark='skrr'), k(.5, 'sill_r', reach=1, x=.5, y=.5, b=.6, l=1), k(.72, 'trim_lo', reach=1, x=.5, y=.4, b=.5),
         k(.88, eye='-')],
        [(.5, 'scrape')], g='weather', act=('scrape', 'ice'), when=['cold', 'rime>.3'], ages=GROWN)
    o.r('fluff_up_against_the_cold_base', 'Fluffing every feather up against the cold, huddled at the foot of the base', 22, 'none',
        [k(.15, 'slat_a', x=.3, y=-.3, b=-.3), k(.35, 'slat_a', x=.2, y=1.6, b=1.7, w=.9, eye='-'), k(.58, 'slat_b', x=.1, y=-.4, b=-.6, w=1, mark='brr'), k(.8, 'slat_b', x=.2, y=1.5, b=1.2, w=.4),
         k(.92, eye='^')],
        [], g='weather', act=('fluff', 'base'), when=['cold'])
    o.r('breathe_on_the_stud_to_thaw_it', 'Blowing a slow warm breath on the frosty left stud and the slat beside it until they drip', 20, 'none',
        [k(.12, 'stud_l', x=1.1, y=.5, b=-.3, l=1), k(.32, 'stud_l', x=1.6, y=.2, b=-.6, w=.6, mark='haaah'), k(.55, 'slat_a', x=1.6, y=.1, b=-.8, w=.8, r=1, eye='-'), k(.8, x=.2, y=1.4, b=1.4, eye='^')],
        [], g='weather', act=('warm', 'stud'), when=['cold'])
    # ---------------- show
    o.r('bow_low_at_the_foot_of_the_case', 'Bowing low at the foot of the case, bill brushing the bottom rail on the way down and up', 14, 'none',
        [k(.15, x=-.8, y=-.8, b=-.9), k(.4, 'rail_l', x=1.6, y=2.4, b=1.5), k(.6, 'rail', x=1.6, y=2.6, b=1.6, mark='ta-da'), k(.85, x=.3, y=-.8, b=-.8, w=.8, eye='^')],
        [], g='show', act=('bow', 'rail'), prefer=['happy'], say=["Bowed to the case. It didn't clap. Rude.", "Low bow, high standards. Next time, flowers."])
    o.r('argue_with_the_glass', 'Arguing with the glass, jabbing his bill at it and being ignored', 18, 'none',
        [k(.15, 'glass_r', x=.9, y=-.4, b=.3), k(.3, 'glass_r', x=1.3, y=-.6, b=.5, mark='AND'), k(.5, 'glass_r', x=.5, y=-.2, b=.2, w=.6, eye='>'), k(.7, 'glass_r', x=1.4, y=-.7, b=.6, eye='@', mark='ANOTHER'),
         k(.9, eye='-')],
        [], g='show', act=('argue', 'glass'), prefer=['grumpy'], say=["You're a window with ideas. Sit down.", "Won the argument. Glass said nothing, as is its way."])
    o.r('shout_up_at_the_stands', 'Shouting up at the three stands to send something down, a wing cupped at his bill', 18, 'wing',
        [k(.15, 'stand_m', reach=.5, x=.2, y=-.4), k(.3, 'stand_m', reach=1, x=.3, y=-1, b=-.4, w=.6, mark='OI'), k(.55, 'stand_m', reach=1, x=.4, y=-1.2, b=-.6, w=.8, eye='@', mark='OIII'),
         k(.8, x=.1, y=-.2, eye='-')],
        [], g='show', act=('shout', 'stands'), ages=GROWN)
    o.r('serenade_the_doors', 'Singing a long wobbly note to the closed doors with a wing over his heart', 22, 'wing',
        [k(.12, 'glass_m', reach=.5, x=.2, y=-.3, b=.2), k(.3, 'seam_lo', reach=1, x=.3, y=-.7, b=-.3, w=.5, mark='laaa'), k(.55, 'glass_m', reach=1, x=.5, y=-.9, b=-.5, w=.9, eye='^', mark='laaaa'),
         k(.78, 'seam_lo', reach=.6, x=.2, y=-.2, b=.2), k(.9, eye='-')],
        [], g='show', act=('sing', 'doors'), prefer=['happy'])
    o.r('dance_a_jig_along_the_rail', 'Dancing a quick jig on the bottom rail with his wings out', 20, 'none',
        [k(.12, 'rail_r', perch=1, x=.4, y=.2, b=-.4, w=.4, l=1), k(.3, 'rail_r', perch=1, x=.7, y=.2, b=-.6, w=.8, r=1), k(.5, 'rail', perch=1, x=.5, y=.3, b=-.7, w=1, l=1),
         k(.7, 'rail', perch=1, x=.8, y=.2, b=-.6, w=.8, r=1), k(.88, 'rail', perch=1, x=.3, b=.2, eye='^')],
        [(.5, 'jig')], g='show', act=('dance', 'rail'), prefer=['happy'])
    # ---------------- mishap
    o.r('skid_on_the_wet_ground_at_the_foot', 'Slipping on the wet ground at the foot of the case and ending in a heap against the end slat', 18, 'none',
        [k(.15, x=.7, y=.2, b=-.3), k(.35, x=1.3, y=.5, b=-.7, w=.8, l=1, r=1, eye='O', mark='whoa'), k(.55, 'slat_e', x=1.4, y=2, b=2, eye='@', mark='thud'), k(.8, 'rail_r', x=.8, y=1, b=1, eye='-'),
         k(.92, eye='^')],
        [], g='mishap', act=('slip', 'rail'), when=['obj_wetness>.3'])
    o.r('topple_over_craning_for_the_top', 'Balancing on tiptoe to see over the ledge and toppling over backwards', 18, 'none',
        [k(.15, x=.2, y=-1, b=-.6), k(.35, x=-.2, y=-1.6, b=-1, w=.6, eye='O'), k(.55, x=-1.2, y=-2, b=-1.4, w=1, l=1, r=1, eye='@', mark='whoa'), k(.75, x=-1, y=1, b=1.8, w=.5, eye='@', mark='thud'),
         k(.9, y=.4, eye='-')],
        [], g='mishap', act=('balance', 'tiptoes'), prefer=['young'], say=["Looked up. Fell down. The case watched.", "Backwards. Elegant. No witnesses, I checked twice."])
    o.r('boot_the_rail_and_hop_about', 'Kicking the bottom rail like a football and hopping about clutching the sore foot', 18, 'none',
        [k(.15, 'rail_l', x=.5, y=.3, b=-.2), k(.32, 'rail_l', x=1, y=.6, b=-.6, l=1, mark='THWACK'), k(.5, x=-.6, y=.8, b=-1, r=1, eye='@', mark='ow'), k(.72, x=-.8, y=.9, b=-.8, l=1, eye='>'),
         k(.9, eye='-')],
        [(.32, 'scuff')], g='mishap', act=('kick', 'rail'), prefer=['grumpy'], say=["Kicked a rail. The rail is fine. My foot isn't.", "Zero stars. Would kick again, harder."])
    o.r('rap_the_seam_too_hard', 'Pecking the door seam much too hard and hopping about clutching his bill', 18, 'none',
        [k(.15, 'seam_lo', x=.6, y=-.3, b=.3), k(.32, 'seam_lo', x=1.6, y=-.9, b=.8, mark='TOCK'), k(.5, x=-.7, y=.5, b=-.5, w=.7, eye='@', mark='ow'), k(.72, x=-.5, y=.8, b=-.7, l=1, r=1), k(.9, eye='-')],
        [(.32, 'smudge')], g='mishap', act=('peck', 'seam'), prefer=['young'])
    o.r('leap_for_a_stand_and_land_on_his_tail', 'Hopping up at the nearest stand, missing, and landing on his tail at the foot of the case', 20, 'none',
        [k(.15, 'stand_l', x=.4, y=-.2, b=-.1), k(.3, x=.6, y=-.8, b=-1.4, w=1, l=1, r=1, eye='O'), k(.46, x=.9, y=-1, b=-1.8, w=1, eye='O'), k(.66, x=-.8, y=.6, b=1.8, w=.4, eye='@', mark='plop'),
         k(.88, y=.4, eye='-')],
        [], g='mishap', act=('hop', 'stand'), prefer=['young'])
    return done(o)


CASE_PARTS = dict(slat='the vertical base slats along the foot of the case', stud='the round studs at each end of the base', rail='the bottom rail the case stands on',
                  stand='the small stands on the lowest ledge', ledge='the lowest shelf ledge', glass='the glass pane of the doors', plate='the (=) plate on the frame post',
                  trim='the trim bar above the base', sill='the lower shelf board')


# @@ancient_amulet
def ancient_amulet():
    # Drawing: a cord loop above (a ring of parentheses, 126-139 px), a pointed medallion whose rim is dotted rays, and in the middle an eye emblem.
    o = Obj('ancient_amulet', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, cord='the cord loop above the medallion', medallion='the pointed medallion', rays='the dotted rays round the medallion', eye='the eye emblem in the middle'),
            fields=dict(twist=(0, 0, 1), dull=(.3, 0, 1)),
            physics=[('twist', 'rate', -.0004, 'always'), ('dull', 'rate', .0004, 'always')],
            effects=dict(twirl=[('twist', 'add', .5)], untwist=[('twist', 'set', 0)], shine=[('dull', 'set', 0)], smudge=[('obj.dirt', 'add', .15)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_b=P(41, 67), rail_l=P(30, 72), stud_l=P(10, 70), stand_l=P(22, 60), ledge=P(30, 61), glass_l=P(15, 59), glass_m=P(49, 58)))
    # ---- from the foot of the case (young ages reach only this far)
    o.r('shout_up_at_the_eye', "Shouting up at the amulet's eye to blink first, a wing cupped at his bill", 16, 'wing',
        [k(.15, 'slat_b', reach=.5, x=.6, y=-.6, b=.3), k(.3, 'slat_b', reach=1, x=.9, y=-1.3, b=-.7, w=.5, mark='BLINK'), k(.55, 'slat_b', reach=1, x=1.1, y=-1.5, b=-.9, w=.9, eye='@', mark='BLINK'),
         k(.8, x=-.2, y=.2, b=.4, eye='-')],
        [], g='show', act=('shout', 'eye'), say=["Stared at it for a minute. It won. Cheat.", "Eye contest, lost to a ceramic. Rematch."])
    o.r('hop_for_the_cord', 'Hopping up at the amulet over and over, as if the cord loop were a branch, and landing on his tail', 20, 'none',
        [k(.15, 'rail_l', x=.4, y=-.3, b=-.1), k(.3, x=.5, y=-.9, b=-1.4, w=1, l=1, r=1, eye='O'), k(.45, x=.7, y=-1, b=-1.8, w=1, eye='O'), k(.66, x=-.7, y=.6, b=1.8, w=.4, eye='@', mark='plop'),
         k(.88, y=.4, eye='-')],
        [], g='mishap', act=('hop', 'cord'), prefer=['young'], say=["Missed the cord by a duck's length. A short duck.", "Landed on my arse. Amulet unbothered."])
    o.r('listen_at_the_slat_under_it', 'Listening with an ear pressed to the slat below the amulet for the hum it is famous for', 18, 'none',
        [k(.15, 'slat_a', x=.7, y=1.4, b=.8), k(.35, 'slat_a', x=.5, y=1.9, b=1.1, eye='-'), k(.58, 'slat_b', x=.5, y=1.8, b=1.1, eye='O'), k(.85, x=.1, y=.3, eye='>')],
        [], g='test', act=('listen', 'slat'))
    o.r('nap_with_the_eye_watching', 'Napping against the left stud with the amulet\'s eye watching over him', 28, 'none',
        [k(.15, 'stud_l', x=-.5, y=.4, b=.7), k(.4, 'stud_l', x=-.9, y=1, b=1.4, eye='-'), k(.7, 'stud_l', x=-.9, y=1.2, b=1.6, eye='-', mark='zzz'), k(.9, x=-.2, y=.3, eye='^')],
        [(.7, 'rest')], g='rest', act=('nap', 'eye'), when=['tired'])
    # ---- once it is out of the case in his bill (young adult and up)
    o.r('lift_it_out_and_turn_it_in_the_light', 'Lifting the amulet out of its place in his bill, turning it in the light and setting it back on its stand', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=.9, y=-1, b=-.4), k(.58, 'item', x=.7, y=-.6, eye='O'), k(.74, 'stand_l', x=1.2, y=-.5), k(.88, eye='^')],
        [], g='use', act=('lift', 'amulet'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))],
        say=["Out of the case. Alarms: none. Result.", "Held up to the light. It caught my ego too."])
    o.r('dangle_it_by_the_cord', 'Rocking the amulet on its cord in his bill and watching the medallion swing and twist', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.5, b=.2), k(.4, 'item', x=1.5, y=-.4, b=.3, l=1), k(.55, 'item', x=1.5, y=-.4, b=.3, r=1, eye='O'), k(.7, 'item', x=1.3, y=-.5, b=.2), k(.88, eye='-')],
        [(.55, 'twirl')], g='play', act=('rock', 'cord'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=0))])
    o.r('hook_the_cord_to_unwind_it', 'Hooking the twisted cord over the ledge and letting the amulet unwind itself', 22, 'none',
        [k(.1, x=.4, y=-.2), k(.24, 'item', x=1.3, y=-.5, b=.2), k(.42, 'ledge', x=1.4, y=.3, b=.5, mark='hook'), k(.6, 'ledge', x=.9, y=.4, b=.5, eye='O'), k(.76, 'item', x=1.2, y=-.4, b=.2), k(.9, eye='^')],
        [(.6, 'untwist')], g='care', act=('hook', 'cord'), when=['twist>.3'], ages=GROWN,
        obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))], say=["Unwound. The cord is straight. My life isn't.", "Spun itself dizzy and stopped. Relatable."])
    o.r('rub_the_medallion_on_his_chest', 'Polishing the lifted amulet over his chest feathers until the medallion shines', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.4, b=.3, mark='hup'), k(.45, 'item', x=.2, y=.5, b=.6, w=.3, mark='rub'), k(.62, 'item', x=.1, y=.6, b=.7, mark='rub'), k(.78, 'item', x=1.2, y=-.4, b=.3),
         k(.9, eye='^')],
        [(.62, 'shine')], g='care', act=('polish', 'medallion'), when=['dull>.4'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Rubbed it on my chest. Shiny. So am I, now.", "Bright as a new coin. Cheaper, though."])
    o.r('carry_it_a_lap_round_the_case', 'Carrying the lifted amulet a lap round the case, strutting, and parking it on the ledge', 26, 'none',
        [k(.1, x=.4, y=-.2), k(.22, 'item', x=1.3, y=-.5, b=.3), k(.38, x=1.1, y=-.1, b=-.4, l=1), k(.54, x=1.4, y=-.2, b=-.5, r=1, w=.4), k(.7, 'ledge', x=1.2, y=.2, b=.4), k(.88, eye='^')],
        [(.7, 'fun')], g='play', act=('carry', 'amulet'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.76, dict(hold=1)), (.86, dict(hold=0))], say=['Lap done. It felt old and I felt great.', 'Paraded an antique. Posh.'])
    o.r('hold_it_up_to_the_glass_and_stare_back', 'Peering at the lifted amulet beside the pane by moonlight until its eye and its reflection stare each other down', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.5, b=.2), k(.45, 'glass_l', x=1.3, y=-.7, b=.3, eye='O'), k(.62, 'glass_l', x=1.4, y=-.8, b=.2, eye='@'), k(.78, 'item', x=1.2, y=-.4), k(.9, eye='^')],
        [], g='weather', act=('peer', 'eye'), when=['night'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('mouth_the_cord_to_taste_it', 'Mouthing the cord of the lifted amulet to taste it and spitting out the fluff', 16, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.45, 'item', x=1.1, y=-.8, b=.4, eye='-', mark='...'), k(.62, 'item', x=-.4, y=-.9, b=-.4, w=.8, l=1, eye='>', mark='ptui'),
         k(.8, 'stand_l', x=1, y=-.5, b=.2), k(.9, eye='-')],
        [(.62, 'smudge')], g='use', act=('taste', 'cord'), ages=GROWN, prefer=['young', 'curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.7, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))], say=["Old. Dusty. Tastes like a museum's armpit.", "Ancient. Tastes ancient. Spat."])
    o.r('lift_it_out_to_show_a_friend', 'Showing the amulet to a friend: lifted out in his bill and held up for them to inspect', 26, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=1.7, y=-1.8, b=-1.2, w=.6), k(.6, 'item', x=1.8, y=-1.9, b=-1.1, w=.8, eye='^'), k(.76, 'glass_m', x=1.2, y=-.5), k(.9, eye='^')],
        [], g='show', act=('show', 'amulet'), ages=GROWN, prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.9, b=.2, eye='O'), k(.62, 'item', x=.9, y=-1, b=.3, eye='O', mark='ooh'), k(.8, x=-.2, y=-.4, eye='^')])
    return done(o)


# @@lucky_charm
def lucky_charm():
    # Drawing: a cord loop above, a six-sided charm with a clover emblem in the middle (a V of two leaves over a stem), a crystal point on top of the hexagon.
    o = Obj('lucky_charm', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, cord='the cord loop above the charm', hexagon='the six-sided rim of the charm', clover='the clover emblem in the middle', crystal='the crystal point on top'),
            fields=dict(luck=(0, 0, 1), gleam=(.4, 0, 1)),
            physics=[('luck', 'rate', -.0005, 'always'), ('gleam', 'rate', -.0004, 'always')],
            effects=dict(wish=[('luck', 'set', 1)], shine=[('gleam', 'set', 1)], glint=[('gleam', 'add', .3)], fun=[('need.fun', 'add', 2)]),
            anchors=dict(item=0, slat_b=P(41, 67), slat_c=P(56, 70), rail_l=P(30, 72), stud_r=P(95, 70), stand_l=P(22, 60), ledge=P(30, 61),
                         glass_m=P(49, 58), sill=P(40, 63), plate_lo=P(11, 63)))
    o.r('knock_three_times_on_the_wood', 'Knocking three times on the wooden base for luck, bill to the middle slat', 16, 'none',
        [k(.15, 'slat_c', x=.9, y=1.1, b=.4), k(.3, 'slat_c', x=1.4, y=1.5, b=.8, mark='tok'), k(.45, 'slat_c', x=.6, y=.8, b=.2), k(.6, 'slat_c', x=1.4, y=1.5, b=.8, mark='tok'),
         k(.75, 'slat_c', x=1.4, y=1.5, b=.9, mark='tok'), k(.9, eye='^')],
        [(.75, 'wish')], g='use', act=('knock', 'slats'), when=['luck<.6'], say=["Knocked three times. Luck, if you're in, I'm out here.", "Wood's good for luck. Also for headaches."])
    o.r('balance_on_one_foot_for_luck', 'Balancing on one foot with both wings out and his eyes shut to keep his luck from tipping', 18, 'none',
        [k(.15, 'rail_l', x=.3, y=.2, b=-.2, l=1), k(.35, 'rail_l', x=.1, y=-.3, b=-.6, w=1, l=1, eye='-'), k(.6, 'rail_l', x=-.2, y=-.4, b=-.7, w=1, l=1, eye='-', mark='steady'),
         k(.8, 'rail_l', x=.6, y=.6, b=.5, w=.4, l=1, r=1, eye='O', mark='whoa'), k(.92, eye='^')],
        [], g='play', act=('balance', 'foot'), prefer=['curious'])
    o.r('rap_the_wood_too_hard', 'Pecking the wood for luck much too hard and hopping about clutching his bill', 16, 'none',
        [k(.15, 'stud_r', x=.7, y=.8, b=.3), k(.32, 'stud_r', x=1.7, y=1.4, b=.9, mark='CRACK'), k(.5, x=-.8, y=.4, b=-.6, w=.7, eye='@', mark='ow'), k(.7, x=-.6, y=.7, b=-.8, l=1, r=1),
         k(.9, eye='-')],
        [], g='mishap', act=('peck', 'wood'), prefer=['young'], say=["That's what the knocking was for. Not that hard.", "Bill hurts. The luck is rated zero."])
    o.r('lean_into_the_slats_with_a_sigh', 'Leaning his whole weight against the slats and sighing at the charm above', 20, 'none',
        [k(.15, 'slat_b', x=-.3, y=.3, b=.5), k(.4, 'slat_b', x=-.8, y=.9, b=1.3, eye='-'), k(.7, 'slat_b', x=-.9, y=1, b=1.4, l=1, mark='sigh'), k(.9, x=-.2, y=.2)],
        [], g='rest', act=('lean', 'slats'))
    o.r('lift_the_charm_out_into_the_light', 'Lifting the charm out in his bill, turning it to see the clover catch the light, and setting it back', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.7, b=.2, mark='hup'), k(.42, 'item', x=1, y=-1.1, b=-.5), k(.58, 'item', x=.6, y=-.7, eye='O'), k(.74, 'stand_l', x=1.3, y=-.4), k(.88, eye='^')],
        [], g='use', act=('lift', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Out it comes. Fortune, meet duck.", "Took it out. Nothing fell on me. Early luck."])
    o.r('kiss_the_charm_for_luck', 'Tapping the lifted charm with a loud smack of his bill and holding it still for a moment', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.4, y=-.6, b=.2), k(.45, 'item', x=1.6, y=-.5, b=.4, mark='smack'), k(.62, 'item', x=1.5, y=-.6, b=.3, eye='^'), k(.8, 'item', x=1.2, y=-.4), k(.9, eye='-')],
        [(.45, 'wish')], g='use', act=('tap', 'charm'), when=['luck<.6'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.82, dict(hold=1)), (.88, dict(hold=0))])
    o.r('buff_the_crystal_on_his_chest', 'Polishing the crystal point over his chest feathers until it throws a spark', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.4, b=.3), k(.44, 'item', x=.1, y=.5, b=.7, w=.3, mark='rub'), k(.6, 'item', x=.2, y=.7, b=.8, mark='rub'), k(.78, 'item', x=1.3, y=-.5, b=.3),
         k(.9, eye='^')],
        [(.6, 'shine')], g='care', act=('polish', 'crystal'), when=['gleam<.5'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Crystal's bright. The luck can see where it's going.", "Buffed. Now it sparkles like it owes me."])
    o.r('weigh_the_charm_in_his_bill', 'Weighing the lifted charm in his bill, bobbing it up and down to see what luck weighs', 20, 'none',
        [k(.1, x=.4, y=-.2), k(.25, 'item', x=1.2, y=-.5, b=.2), k(.4, 'item', x=1.4, y=.3, b=.6), k(.55, 'item', x=1.4, y=-.7, b=-.3), k(.7, 'item', x=1.4, y=.4, b=.7), k(.82, 'ledge', x=1.2, y=.1, b=.3),
         k(.92, eye='^')],
        [], g='test', act=('weigh', 'charm'), ages=GROWN,
        obj=[(.25, dict(hold=0)), (.36, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))], say=['Luck weighs about a grape. Noted.', 'Hefted it. Heavier than hope, lighter than bread.'])
    o.r('carry_the_charm_for_a_lucky_lap', 'Carrying the lifted charm a lap round the case, strutting, and touching the rail for luck', 26, 'none',
        [k(.1, x=.4, y=-.2), k(.22, 'item', x=1.3, y=-.5, b=.3), k(.38, x=1.1, y=-.1, b=-.4, l=1), k(.54, x=1.4, y=-.2, b=-.5, r=1, w=.4), k(.72, 'rail_l', x=1.2, y=.9, b=.6), k(.88, eye='^')],
        [(.72, 'fun')], g='play', act=('carry', 'charm'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))], say=['Lap complete. Luck: pending.', 'Strutted. Luck followed. Or it was my tail.'])
    o.r('tilt_the_crystal_into_the_sun', 'Tilting the lifted charm toward the sun so the crystal throws a spot of light on the glass', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2), k(.45, 'glass_m', x=1.5, y=-.9, b=-.3), k(.62, 'glass_m', x=1.6, y=-1.1, b=-.5, eye='O', mark='ping'), k(.78, 'item', x=1.3, y=-.5), k(.9, eye='^')],
        [(.62, 'glint')], g='weather', act=('tilt', 'crystal'), when=['sun'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Sun on the crystal. A dot of light. I made a disco.", "Aimed it at the glass. Direct hit. Still unlucky."])
    o.r('squint_at_the_clover', 'Peering cross-eyed at the clover on the lifted charm to find which leaf is the lucky one', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.1, y=-.5, b=.2), k(.45, 'item', x=1.6, y=.2, b=.6, eye='@'), k(.65, 'item', x=1.7, y=.3, b=.5, eye='@'), k(.8, 'sill', x=1.2, y=-.1), k(.9, eye='-')],
        [], g='test', act=('peer', 'clover'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))])
    o.r('pass_the_charm_to_a_friend_for_a_turn', 'Presenting the lifted charm to a friend for their turn at being lucky, then taking it back', 28, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.4, 'item', x=1.8, y=-1.3, b=-.8, w=.4), k(.58, 'item', x=1.4, y=-.7, b=-.2, w=.2), k(.78, 'plate_lo', x=1.2, y=-.4), k(.9, eye='^')],
        [], g='show', act=('present', 'charm'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.9, b=.3, eye='O'), k(.62, 'item', x=1.1, y=-1, b=.4, eye='^', mark='ooh'), k(.8, x=-.1, y=-.4, eye='^')])
    return done(o)


# @@earth_token
def earth_token():
    # Drawing: a six-sided token with a dotted rim, a jagged mountain in the middle (two peaks) and a small sprig beside it. No cord.
    o = Obj('earth_token', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, rim='the dotted rim of the hexagonal token', mountain='the mountain with two peaks', sprig='the small sprig beside the mountain'),
            fields=dict(grit=(.3, 0, 1), ring=(0, 0, 1)),
            physics=[('grit', 'rate', .0004, 'always'), ('ring', 'rate', -.0008, 'always')],
            effects=dict(clang=[('ring', 'set', 1)], hush=[('ring', 'set', 0)], scour=[('grit', 'set', 0)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_c=P(56, 70), slat_d=P(71, 68), rail_l=P(30, 72), stud_l=P(10, 70), stand_l=P(22, 60), ledge=P(30, 61), glass_m=P(49, 58),
                         plate_lo=P(11, 63)))
    o.r('press_an_ear_to_the_floor_for_a_rumble', 'Listening with an ear flat to the floor beside the rail for the earth to rumble', 18, 'none',
        [k(.15, 'rail_l', x=.4, y=1.5, b=1.1), k(.35, 'rail_l', x=.2, y=2.1, b=1.6, eye='-'), k(.6, 'rail_l', x=.1, y=2.2, b=1.7, eye='O', mark='mmm'), k(.85, x=.5, y=.4, b=.2, eye='>')],
        [], g='test', act=('listen', 'rail'))
    o.r('tap_a_mountain_rhythm_on_the_slats', 'Tapping the slats in a mountain rhythm, three up and two down, with his bill', 20, 'none',
        [k(.12, 'slat_a', x=1, y=1.3, b=.5, mark='tk'), k(.28, 'slat_c', x=1.1, y=1.4, b=.6, mark='tk'), k(.44, 'slat_d', x=1.1, y=1.4, b=.7, l=1, mark='tk'), k(.6, 'slat_c', x=1, y=1.2, b=.5, mark='tk'),
         k(.76, 'slat_a', x=1, y=1.1, b=.4, r=1, mark='tk'), k(.9, eye='^')],
        [], g='play', act=('tap', 'slats'), prefer=['happy'], say=["Peak, peak, valley. It's a song if I say so.", "Mountain music. Very low-budget."])
    o.r('climb_the_slats_toward_the_token', 'Climbing up the slats toward the token, getting two rows high, and sliding down flat', 20, 'none',
        [k(.12, 'slat_d', x=.8, y=.8, b=-.3), k(.3, 'slat_d', x=1.2, y=-.4, b=-.9, w=.6, l=1), k(.48, 'slat_d', x=1.4, y=-.8, b=-1.2, w=.8, r=1, eye='O'), k(.68, 'slat_d', x=-.2, y=1.2, b=1.6, w=.4, eye='@', mark='fwump'),
         k(.88, eye='-')],
        [], g='mishap', act=('climb', 'slats'), prefer=['young'], say=["Climbed the foot of the case. Summit: the second slat.", "Sliding down was the faster half."])
    o.r('sit_down_beside_the_left_stud', 'Sitting down beside the left stud with his bill propped against it and a view of the mountain', 24, 'none',
        [k(.15, 'stud_l', x=.3, y=.6, b=1.1), k(.4, 'stud_l', x=.2, y=.8, b=1.5, l=1), k(.65, 'stud_l', x=.2, y=.9, b=1.6, eye='-', mark='sigh'), k(.88, x=.3, y=.3, b=.6)],
        [(.65, 'rest')], g='rest', act=('sit', 'stud'), when=['tired'])
    o.r('lift_the_token_out_and_hold_it_flat', 'Lifting the token out in his bill, holding it flat to look at the mountain, and setting it back', 22, 'none',
        [k(.1, x=.6, y=-.4), k(.25, 'item', x=1.4, y=-.5, b=.3, mark='hup'), k(.42, 'item', x=1.1, y=-.1, b=-.2), k(.58, 'item', x=.8, y=.2, b=-.3, eye='O'), k(.74, 'stand_l', x=1.1, y=-.4), k(.88, eye='^')],
        [], g='use', act=('lift', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Heavier than it looks. Like most mountains.", "Out of the case. The mountain's thrilled."])
    o.r('ring_the_rim_against_the_stud', 'Tapping the rim of the lifted token against the stud like a coin to make it ring', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.6, b=.2), k(.44, 'stud_l', x=1.5, y=1, b=.7, mark='TING'), k(.6, 'stud_l', x=1.2, y=.8, b=.4, eye='O'), k(.76, 'item', x=1.2, y=-.4), k(.9, eye='^')],
        [(.44, 'clang')], g='use', act=('tap', 'rim'), ages=GROWN,
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))])
    o.r('hold_the_ringing_token_to_his_ear', 'Listening to the ringing token held up beside his ear until the note dies away', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.1, y=-.6, b=.2), k(.45, 'item', x=.2, y=-1, b=-.2, eye='O', mark='...'), k(.65, 'item', x=.1, y=-1.1, b=-.3, eye='-'), k(.8, 'item', x=1.1, y=-.4), k(.9, eye='^')],
        [(.65, 'hush')], g='test', act=('listen', 'token'), when=['ring>.3'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.82, dict(hold=1)), (.88, dict(hold=0))], say=["Rings like a church bell with a head cold.", "The note faded. Mountains do that, I'm told."])
    o.r('scrub_the_mountain_on_his_chest', 'Scrubbing the mountain on the lifted token over his chest feathers to rub the grit off', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.4, b=.3), k(.44, 'item', x=.1, y=.6, b=.8, w=.3, mark='skr'), k(.6, 'item', x=.2, y=.8, b=.9, mark='skr'), k(.78, 'item', x=1.2, y=-.5, b=.3),
         k(.9, eye='^')],
        [(.6, 'scour')], g='care', act=('scrub', 'mountain'), when=['grit>.4'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Grit off. Peaks sharp. Ready for the weather forecast.", "Rubbed the dirt out of the mountains. Landscaping, but small."])
    o.r('carry_the_token_a_lap_like_a_trophy', 'Carrying the token a lap round the case, bill held high like a trophy, and touching the rail', 26, 'none',
        [k(.1, x=.3, y=-.3), k(.22, 'item', x=1.5, y=-.9, b=.3), k(.38, x=1.5, y=-.8, b=-.3, l=1), k(.54, x=1.7, y=-.9, b=-.4, r=1, w=.5), k(.72, 'rail_l', x=1.1, y=.7, b=.5), k(.88, eye='^')],
        [(.72, 'fun')], g='play', act=('carry', 'token'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))], say=['Trophy lap, no race. Still applauded myself.', 'Held the mountain high. Felt tall.'])
    o.r('weigh_the_token_against_the_ledge', 'Weighing the lifted token in his bill against the ledge to see which is the heavier mountain', 20, 'none',
        [k(.1, x=.4, y=-.2), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.42, 'ledge', x=1.5, y=.3, b=.7), k(.58, 'item', x=1.3, y=-.7, b=-.3), k(.74, 'ledge', x=1.5, y=.4, b=.8, eye='>'), k(.88, eye='-')],
        [], g='test', act=('weigh', 'token'), ages=GROWN,
        obj=[(.25, dict(hold=0)), (.36, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=0))])
    o.r('warm_the_token_in_the_sun', 'Warming the lifted token in a patch of sun by the glass until the mountain face glints', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.6, b=.2), k(.45, 'glass_m', x=1.4, y=-.8, b=-.1, eye='-'), k(.7, 'glass_m', x=1.5, y=-.9, b=-.2, eye='^'), k(.82, 'item', x=1.2, y=-.4), k(.92, eye='^')],
        [], g='weather', act=('warm', 'token'), when=['sun'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))])
    o.r('present_the_mountain_to_a_friend', 'Presenting the lifted token to a friend so they can feel the weight of the mountain', 26, 'none',
        [k(.1, x=.7, y=-.5, b=.4), k(.22, 'item', x=1.1, y=-.9, b=.5), k(.4, 'item', x=2.2, y=-1.6, b=-1.3, w=.7), k(.58, 'item', x=1.9, y=-1.1, b=-.6, w=.3), k(.78, 'plate_lo', x=1.5, y=-.2, b=.2), k(.9, eye='^')],
        [], g='show', act=('present', 'mountain'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.8, b=.3, eye='O'), k(.62, 'item', x=.9, y=-.7, b=.6, eye='@', mark='oof'), k(.8, x=-.2, y=-.2, eye='^')])
    return done(o)


# @@sky_token
def sky_token():
    # Drawing: a round token with a cloud (a low arch of dots) over a jagged bolt in the middle, rim of dashes and small stars outside. No cord.
    o = Obj('sky_token', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, rim='the round rim of the token', cloud='the cloud above the middle', bolt='the jagged bolt in the middle'),
            fields=dict(static=(0, 0, 1), haze=(.3, 0, 1)),
            physics=[('static', 'rate', -.0008, 'always'), ('haze', 'rate', .0004, 'always')],
            effects=dict(charge=[('static', 'set', 1)], zap=[('static', 'set', 0)], clear=[('haze', 'set', 0)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_b=P(41, 67), slat_d=P(71, 68), rail_l=P(30, 72), stud_r=P(95, 70), stand_l=P(22, 60), glass_l=P(15, 59), sill=P(40, 63),
                         plate_lo=P(11, 63)))
    o.r('shout_up_at_the_cloud_for_rain', 'Shouting up at the cloud on the token for rain, a wing cupped to his bill', 18, 'wing',
        [k(.15, 'slat_d', reach=.5, x=.5, y=-.5, b=.2), k(.3, 'slat_d', reach=1, x=.7, y=-1.2, b=-.5, w=.7, mark='RAIN'), k(.55, 'slat_d', reach=1, x=.9, y=-1.4, b=-.8, w=.9, eye='@', mark='RAAAIN'),
         k(.8, x=-.1, y=0, b=.3, eye='-')],
        [], g='show', act=('shout', 'cloud'), say=["Asked nicely. Then not nicely. Dry as a bone.", "Cloud's on a token. Of course it won't rain."])
    o.r('hop_at_the_cloud_and_miss', 'Hopping up toward the cloud above, missing it by a mile and landing flat', 18, 'none',
        [k(.15, 'stud_r', x=.2, y=-.3, b=-.2), k(.3, x=.3, y=-.7, b=-1.3, w=1, l=1, r=1, eye='O'), k(.46, x=.5, y=-.9, b=-1.7, w=1, eye='O'), k(.66, x=-.5, y=.8, b=1.9, w=.4, eye='@', mark='fwump'),
         k(.88, y=.3, eye='-')],
        [], g='mishap', act=('hop', 'cloud'), prefer=['young'])
    o.r('nap_with_one_eye_on_the_cloud', 'Napping against the slats with one eye on the cloud above', 26, 'none',
        [k(.15, 'slat_b', x=-.2, y=.8, b=.9), k(.4, 'slat_b', x=-1.1, y=.6, b=1.9, w=.4, eye='-'), k(.7, 'slat_b', x=-1.2, y=.7, b=2, l=1, eye='-', mark='zzz'), k(.9, x=-.1, y=.1, b=.5, eye='^')],
        [(.7, 'rest')], g='rest', act=('nap', 'cloud'), when=['tired'])
    o.r('catch_the_wind_at_the_foot', 'Catching the wind with a raised wing at the foot of the case, the way the token promises', 22, 'wing',
        [k(.12, 'slat_b', reach=.4, x=.2, y=.3, b=.2), k(.3, 'slat_b', reach=.9, x=.3, y=-.3, b=-.4, w=.6), k(.55, 'slat_b', reach=1, x=.4, y=-.5, b=-.7, w=1, l=1), k(.78, 'slat_b', reach=.6, x=.2, y=-.1, b=-.2, r=1),
         k(.9, eye='^')],
        [], g='weather', act=('catch', 'wind'), when=['windy'])
    o.r('lift_the_token_out_to_the_light', 'Lifting the token out in his bill, tilting it so the bolt flashes, and setting it back', 22, 'none',
        [k(.1, x=.6, y=-.3), k(.25, 'item', x=1.3, y=-.7, b=.2, mark='hup'), k(.42, 'item', x=1.2, y=-1.2, b=-.5), k(.58, 'item', x=.8, y=-.8, b=-.2, eye='O'), k(.74, 'stand_l', x=1.2, y=-.4), k(.88, eye='^')],
        [], g='use', act=('lift', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Out it comes. Zero thunder. Disappointing.", "Cloud in my bill. Finally I'm above something."])
    o.r('fluff_up_against_the_token_for_static', 'Fluffing his feathers against the lifted token until the static crackles', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.4, b=.3), k(.44, 'item', x=.3, y=.7, b=.9, w=.6, mark='skrr'), k(.6, 'item', x=.2, y=.9, b=1, w=.9, mark='skrr'), k(.78, 'item', x=1.3, y=-.5, b=.3),
         k(.9, eye='@')],
        [(.6, 'charge')], g='play', act=('fluff', 'feathers'), ages=GROWN, prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Frizzy. Crackly. A proper storm cloud.", "Every feather's standing up. They all agree."])
    o.r('zap_the_stud_with_the_bolt', 'Tapping the charged token against the stud so the bolt gives it a zap', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.6, b=.2), k(.44, 'stud_r', x=1.6, y=1.1, b=.8, w=.8, mark='ZAP'), k(.58, 'stud_r', x=-.6, y=.2, b=-.8, w=1, l=1, r=1, eye='@'), k(.76, 'item', x=1, y=-.4),
         k(.9, eye='>')],
        [(.44, 'zap')], g='use', act=('tap', 'bolt'), when=['static>.4'], ages=GROWN,
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))], say=["ZAP. Right in the beak. Worth it.", "Stud's fine. I'm still ringing."])
    o.r('blow_on_the_cloud_to_see_it_drift', 'Blowing on the cloud of the lifted token to test whether it drifts', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.1, y=-.6, b=.2), k(.42, 'glass_l', x=1.4, y=-.8, b=.3, mark='fffh'), k(.6, 'glass_l', x=1.5, y=-.9, b=.4, eye='O'), k(.78, 'item', x=1.1, y=-.4), k(.9, eye='-')],
        [], g='test', act=('blow', 'cloud'), ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('polish_the_haze_off_the_cloud', 'Polishing the haze off the cloud with a few breaths and a rub against his chest', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.5, b=.3), k(.42, 'item', x=1.4, y=-.6, b=.4, mark='haah'), k(.6, 'item', x=.2, y=.7, b=.9, mark='rub'), k(.78, 'item', x=1.3, y=-.5, b=.3), k(.9, eye='^')],
        [(.6, 'clear')], g='care', act=('polish', 'cloud'), when=['haze>.4'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('run_a_race_with_the_token_like_a_kite', 'Running a race round the case with the token held high like a kite and the wind at his tail', 24, 'none',
        [k(.1, x=.3, y=-.3), k(.2, 'item', x=1.6, y=-1, b=.2), k(.36, x=1.4, y=-.9, b=-.5, w=.5, l=1), k(.52, x=1.8, y=-1.1, b=-.7, w=.8, r=1), k(.7, 'rail_l', x=1.2, y=.8, b=.6), k(.88, eye='^')],
        [(.7, 'fun')], g='play', act=('race', 'token'), ages=GROWN, prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.32, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=0))])
    o.r('peer_at_the_bolt_cross_eyed', 'Peering cross-eyed at the bolt on the lifted token to see where it points', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.1, y=-.5, b=.2), k(.45, 'item', x=1.6, y=.3, b=.6, eye='@'), k(.65, 'item', x=1.7, y=.4, b=.5, eye='@'), k(.8, 'sill', x=1.1, y=-.1), k(.9, eye='-')],
        [], g='test', act=('peer', 'bolt'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))], say=['Cross-eyed. The bolt points at my own beak. Cheeky.', 'Looked hard. Still just a bolt. Still impressive.'])
    o.r('present_the_storm_to_a_friend', 'Presenting the lifted token to a friend, bolt first, as proof that he commands the weather', 26, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.6, b=.2), k(.4, 'item', x=1.8, y=-1.3, b=-.8, w=.4), k(.58, 'item', x=1.5, y=-.9, b=-.3), k(.78, 'plate_lo', x=1.1, y=-.3), k(.9, eye='^')],
        [], g='show', act=('present', 'bolt'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=.9, y=-.9, b=.3, eye='O'), k(.62, 'item', x=1, y=-1, b=.4, eye='@', mark='eep'), k(.8, x=-.3, y=-.4, eye='^')])
    return done(o)


# @@water_token
def water_token():
    # Drawing: a round token with a dotted rim, in the middle a small drop between two curved lines, and three tildes (a wave) under it; a few quote-mark splashes below.
    o = Obj('water_token', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, rim='the round rim of the token', drop='the drop in the middle', wave='the wave of tildes under the drop', splash='the splash marks under the token'),
            fields=dict(ripple=(0, 0, 1), sheen=(.4, 0, 1)),
            physics=[('ripple', 'rate', -.001, 'always'), ('sheen', 'rate', -.0004, 'always')],
            effects=dict(slosh=[('ripple', 'set', 1)], calm=[('ripple', 'set', 0)], gloss=[('sheen', 'set', 1)], dry=[('obj.wetness', 'add', -.3)], fun=[('need.fun', 'add', 2)],
                         rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_c=P(56, 70), rail_l=P(30, 72), stud_r=P(95, 70), stand_l=P(22, 60), ledge=P(30, 61), glass_l=P(15, 59), glass_m=P(49, 58),
                         sill=P(40, 63),))
    o.r('catch_raindrops_with_his_bill_up', 'Catching raindrops on his bill at the foot of the case, face tipped up toward the token', 24, 'none',
        [k(.15, 'slat_c', x=.5, y=-.4, b=.2), k(.35, 'slat_c', x=.6, y=-1.3, b=-.5, eye='O'), k(.6, 'slat_c', x=.7, y=-1.5, b=-.6, w=.4, mark='plip'), k(.82, x=-.2, y=.3, b=.4, eye='^')],
        [], g='weather', act=('catch', 'rain'), when=['wet'], say=['Rain on my bill. A free shower, with a side of trophy.', 'Caught three drops. Missed the fourth. Fine.'])
    o.r('sing_a_drizzly_song_to_the_drop', 'Singing a drizzly little song to the drop on the token, one hand on the rail', 22, 'wing',
        [k(.12, 'rail_l', reach=.5, x=.3, y=-.2, b=.3), k(.3, 'rail_l', reach=1, x=.4, y=-.8, b=-.3, w=.5, mark='la'), k(.55, 'rail_l', reach=1, x=.5, y=-1, b=-.5, w=.8, eye='^', mark='laa'),
         k(.78, 'rail_l', reach=.6, x=.2, y=-.1, b=.2), k(.9, eye='-')],
        [], g='show', act=('sing', 'drop'), prefer=['happy'], say=["Drip, drip, drip. It's a ballad if you're patient.", "The drop didn't clap. Wet audience."])
    o.r('slip_on_the_wet_ground_before_the_token', 'Slipping on the wet ground at the foot of the case, as if the token had made it', 18, 'none',
        [k(.15, x=.7, y=.2, b=-.3), k(.35, x=1.5, y=.6, b=-.8, w=.9, l=1, r=1, eye='O', mark='whoa'), k(.55, 'slat_a', x=1.5, y=2.2, b=2.1, eye='@', mark='splat'), k(.8, 'slat_a', x=.9, y=1.1, b=1.1, eye='-'),
         k(.92, eye='^')],
        [], g='mishap', act=('slip', 'slat'), when=['wet'], say=["Wet floor, wet token. Coincidence? Yes.", "Flat on my back. Dry on top, suspiciously."])
    o.r('doze_off_with_the_waves_in_his_head', 'Napping against the right stud, the wave on the token lapping at the back of his mind', 28, 'none',
        [k(.15, 'stud_r', x=-.6, y=.2, b=.4), k(.4, 'stud_r', x=-1.3, y=1.4, b=1.1, w=.5, eye='-'), k(.7, 'stud_r', x=-1.4, y=1.5, b=1.2, r=1, eye='-', mark='zzz'), k(.9, x=-.4, y=.1, b=.3, eye='^')],
        [(.7, 'rest')], g='rest', act=('nap', 'wave'), when=['tired'])
    o.r('lift_the_token_out_to_see_the_drop', 'Lifting the token out in his bill, holding it up to see the drop gleam, and setting it back', 22, 'none',
        [k(.1, x=.5, y=-.4), k(.25, 'item', x=1.4, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=1, y=-1, b=-.4), k(.58, 'item', x=.9, y=-.7, eye='O'), k(.74, 'stand_l', x=1.1, y=-.5), k(.88, eye='^')],
        [], g='use', act=('lift', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Out it comes. Not a drop spilled, for a drop.", "Held it level. Nothing sloshed. Boring wave."])
    o.r('tilt_the_token_to_slosh_the_wave', 'Tilting the lifted token side to side to slosh the wave below the drop', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.4, 'item', x=1.1, y=-.3, b=.6, l=1), k(.55, 'item', x=1.6, y=-.4, b=-.3, r=1, eye='O'), k(.7, 'item', x=1.1, y=-.3, b=.6, l=1),
         k(.85, eye='^')],
        [(.55, 'slosh')], g='use', act=('tilt', 'wave'), ages=GROWN, prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.36, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=0))], say=["Sloshed it. The wave was cross.", "Tilt left, tilt right. I'm the sea."])
    o.r('watch_the_wave_settle', 'Peering at the sloshing wave on the lifted token until it settles flat again', 22, 'none',
        [k(.1, x=.6, y=-.4, b=.1), k(.25, 'item', x=1.2, y=-.8, b=.5), k(.45, 'glass_l', x=1.9, y=.5, b=.9, eye='O'), k(.65, 'glass_l', x=2, y=.6, b=.8, eye='-'), k(.8, 'item', x=1.2, y=-.7, b=.1), k(.9, eye='^')],
        [(.65, 'calm')], g='test', act=('peer', 'wave'), when=['ripple>.3'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.82, dict(hold=1)), (.88, dict(hold=0))])
    o.r('polish_the_drop_till_it_gleams', 'Polishing the drop on the lifted token with the side of his bill until it gleams', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.5, b=.3), k(.44, 'item', x=1.5, y=-.2, b=.5, mark='sqk'), k(.6, 'item', x=1.6, y=-.1, b=.6, mark='sqk'), k(.78, 'item', x=1.2, y=-.4), k(.9, eye='^')],
        [(.6, 'gloss')], g='care', act=('polish', 'drop'), when=['sheen<.5'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('dry_the_token_on_the_ledge', 'Drying the lifted token on the ledge and then on his chest feathers till no bead is left', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.2, y=-.4, b=.3), k(.4, 'ledge', x=1.4, y=.5, b=.7, mark='pat'), k(.58, 'ledge', x=1.5, y=.6, b=.8, mark='pat'), k(.74, 'item', x=.2, y=.6, b=.8, mark='rub'),
         k(.9, eye='^')],
        [(.58, 'dry')], g='care', act=('dry', 'token'), when=['obj_wetness>.3'], ages=GROWN,
        obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=['Dry token. Wet duck. We both come out ahead.', 'Every bead off. It looks smug.'])
    o.r('carry_the_token_without_spilling_the_wave', 'Carrying the token a lap round the case at a very careful walk so the wave does not spill', 28, 'none',
        [k(.1, x=.3, y=-.3), k(.22, 'item', x=1.3, y=-.5, b=.3), k(.38, x=1.1, y=-.3, b=-.1, l=1), k(.54, x=1.2, y=-.3, b=-.1, r=1), k(.72, 'rail_l', x=1, y=.7, b=.5), k(.88, eye='^')],
        [(.72, 'fun')], g='play', act=('carry', 'wave'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))])
    o.r('weigh_the_token_beside_the_glass', 'Weighing the lifted token in his bill against the pane to see which holds more water', 20, 'none',
        [k(.1, x=.4, y=-.2), k(.25, 'item', x=1.3, y=-.5, b=.2), k(.42, 'glass_m', x=1.5, y=-.5, b=.5), k(.58, 'item', x=1.3, y=-.8, b=-.3), k(.74, 'glass_m', x=1.5, y=-.4, b=.6), k(.88, eye='-')],
        [], g='test', act=('weigh', 'drop'), ages=GROWN,
        obj=[(.25, dict(hold=0)), (.36, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=0))])
    o.r('present_the_drop_to_a_friend', 'Presenting the lifted token to a friend, drop first, like the one that finally fell on his head', 26, 'none',
        [k(.1, x=.4, y=-.6, b=.5), k(.22, 'item', x=1.5, y=-.9, b=.7), k(.4, 'item', x=2, y=-1.7, b=-1.1, w=.6), k(.58, 'item', x=1.7, y=-1, b=-.4, w=.2), k(.78, 'sill', x=1.3, y=-.5, b=.1), k(.9, eye='^')],
        [], g='show', act=('present', 'drop'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.9, b=.2, eye='O'), k(.62, 'item', x=.9, y=-1, b=.3, eye='O', mark='ooh'), k(.8, x=-.1, y=-.4, eye='^')])
    return done(o)


# @@magpie_friendship_charm
def magpie_friendship_charm():
    # Drawing: a cord loop above, a round charm with a small bird in the middle (an eye `o`, a beak `>=`, a tail `/\`) over a few tildes. Magpie: the thing is for sharing.
    o = Obj('magpie_friendship_charm', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, cord='the cord loop above the charm', rim='the round rim of the charm', bird='the small bird in the middle with its beak and tail', tildes='the wave of tildes at the bird'),
            fields=dict(glint=(.4, 0, 1), swap=(0, 0, 1)),
            physics=[('glint', 'rate', -.0004, 'always'), ('swap', 'rate', -.0006, 'always')],
            effects=dict(shine=[('glint', 'set', 1)], glimmer=[('glint', 'add', .3)], trade=[('swap', 'set', 1)], keep=[('swap', 'set', 0)], fun=[('need.fun', 'add', 2)],
                         rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_d=P(71, 68), rail_l=P(30, 72), stud_l=P(10, 70), stud_r=P(95, 70), stand_l=P(22, 60),
                         glass_l=P(15, 59), glass_m=P(49, 58), sill=P(40, 63), plate_lo=P(11, 63)))
    o.r('sing_a_chirp_to_the_bird', 'Singing a chirpy duet at the bird on the charm, a wing out for the harmony', 18, 'wing',
        [k(.12, 'slat_d', reach=.4, x=.3, y=-.5, b=.2), k(.3, 'slat_d', reach=.9, x=.5, y=-1, b=-.4, w=.4, mark='tweet'), k(.5, 'slat_d', reach=1, x=.6, y=-1.2, b=-.6, w=.7, eye='^', mark='tweet'),
         k(.75, 'slat_d', reach=.7, x=.3, y=-.4, b=.1), k(.9, eye='-')],
        [], g='show', act=('sing', 'bird'), prefer=['happy'], say=["Tweeted. It tweeted back. Silently. Rude.", "Great harmony. One of us is ceramic."])
    o.r('hop_at_the_bird_to_be_friends', 'Hopping up toward the bird to be friends, missing, and ending in a heap', 18, 'none',
        [k(.15, 'stud_l', x=.3, y=-.2, b=-.3), k(.3, x=.4, y=-.8, b=-1.5, w=.9, l=1, eye='O'), k(.46, x=.6, y=-.9, b=-1.9, w=1, r=1, eye='O'), k(.68, x=-.6, y=.7, b=2, w=.4, eye='@', mark='fwump'), k(.88, y=.2, eye='-')],
        [], g='mishap', act=('hop', 'bird'), prefer=['young'])
    o.r('peek_round_the_stud_at_the_bird', 'Seeking the bird with a peek round the right stud, ducking away and peeking again', 18, 'none',
        [k(.15, 'stud_r', x=1.2, y=.8, b=.3, eye='o'), k(.32, x=-1, y=0, b=-.3), k(.5, 'stud_r', x=1.6, y=.9, b=.4, eye='O'), k(.68, x=-1.1, y=-.1, b=-.4), k(.85, 'stud_r', x=1.3, y=.7, b=.2, eye='^')],
        [], g='play', act=('seek', 'bird'), prefer=['young', 'curious'])
    o.r('nap_with_the_bird_on_watch', 'Napping at the foot of the case with the bird on the charm keeping watch', 26, 'none',
        [k(.15, 'slat_a', x=.4, y=.9, b=1), k(.4, 'slat_a', x=.2, y=1.6, b=1.7, eye='-'), k(.7, 'slat_a', x=.1, y=1.8, b=1.9, r=1, eye='-', mark='zzz'), k(.9, x=.4, y=.2, b=.4, eye='^')],
        [(.7, 'rest')], g='rest', act=('nap', 'bird'), when=['tired'])
    o.r('lift_the_charm_out_for_a_look', 'Lifting the charm out in his bill, looking the bird in the eye, and setting it back', 22, 'none',
        [k(.1, x=.5, y=-.4), k(.25, 'item', x=1.4, y=-.5, b=.3, mark='hup'), k(.42, 'item', x=1, y=-.9, b=-.5), k(.58, 'item', x=.9, y=-.5, eye='O'), k(.74, 'stand_l', x=1.2, y=-.5, b=.1), k(.88, eye='^')],
        [], g='use', act=('lift', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Out of the case. The bird looked pleased. I'm choosing to read that.", "Bird to bird. Mine's bigger."])
    o.r('rock_the_charm_to_make_the_bird_bob', 'Rocking the charm on its cord in his bill to make the bird bob', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.2, y=-.6, b=.3), k(.38, 'item', x=1.6, y=-.5, b=.5, l=1), k(.54, 'item', x=1.6, y=-.5, b=.5, r=1, eye='O'), k(.7, 'item', x=1.2, y=-.6, b=.3), k(.88, eye='-')],
        [(.54, 'fun')], g='use', act=('rock', 'cord'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.36, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=0))])
    o.r('polish_the_bird_on_his_chest', 'Polishing the bird on the lifted charm over his chest feathers until its eye glints', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.1, y=-.4, b=.3), k(.44, 'item', x=.2, y=.4, b=.7, w=.4, mark='rub'), k(.6, 'item', x=.1, y=.6, b=.9, mark='rub'), k(.78, 'item', x=1.2, y=-.5, b=.3), k(.9, eye='^')],
        [(.6, 'shine')], g='care', act=('polish', 'bird'), when=['glint<.5'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Bird's eye is bright. It approves. I think.", "Shiny. Magpies would sell a cousin for this."])
    o.r('peer_into_the_birds_eye', "Peering into the bird's eye on the lifted charm to see if it winks", 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1, y=-.4, b=.2), k(.45, 'glass_l', x=1.8, y=.5, b=.9, eye='@'), k(.65, 'glass_l', x=1.9, y=.6, b=.8, eye='@'), k(.8, 'item', x=1, y=-.3), k(.9, eye='-')],
        [], g='test', act=('peer', 'bird'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.82, dict(hold=1)), (.88, dict(hold=0))], say=['Winked first. The bird lost the stare. Technically.', 'Bird eye, duck eye. A rivalry begins.'])
    o.r('carry_the_charm_round_to_show_it_off', 'Carrying the lifted charm round the case with the bird swinging, showing it to nobody in particular', 24, 'none',
        [k(.1, x=.3, y=-.3), k(.2, 'item', x=1.4, y=-.6, b=.4), k(.36, x=1.2, y=-.4, b=-.3, l=1), k(.52, x=1.6, y=-.5, b=-.4, r=1, w=.3), k(.72, 'rail_l', x=1.1, y=.8, b=.6), k(.88, eye='^')],
        [(.72, 'fun')], g='play', act=('carry', 'charm'), ages=GROWN, prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.32, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))])
    o.r('keep_the_charm_away_from_a_friend', 'Guarding the lifted charm against a friend, turning his back and clutching it close', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.2, y=-.4, b=.3), k(.4, 'plate_lo', x=-.8, y=.4, b=.8, w=.5, eye='>'), k(.58, 'plate_lo', x=-1.2, y=.6, b=1, w=.8, mark='mine'), k(.76, 'item', x=1.1, y=-.4), k(.9, eye='-')],
        [(.58, 'keep')], g='play', act=('guard', 'charm'), when=['swap>.3'], ages=GROWN,
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))], say=["Friendship's lovely. This bit is mine.", "Held on tight. Share your own charm."])
    o.r('catch_the_sun_on_the_bird', 'Tilting the charm in the sun to make the bird flash on the pane', 20, 'none',
        [k(.1, x=.7, y=-.4, b=.2), k(.25, 'item', x=1.5, y=-.7, b=.4), k(.45, 'glass_m', x=1.9, y=-1.2, b=-.6, w=.3), k(.62, 'glass_m', x=2, y=-1.4, b=-.7, w=.4, eye='O', mark='flash'), k(.78, 'item', x=1.4, y=-.6, b=.1), k(.9, eye='^')],
        [(.62, 'glimmer')], g='weather', act=('tilt', 'bird'), when=['sun'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('trade_the_charm_with_a_friend', 'Presenting the lifted charm to a friend and taking theirs in turn, then handing it back', 30, 'none',
        [k(.1, x=.5, y=-.3), k(.2, 'item', x=1.3, y=-.5, b=.3), k(.38, 'item', x=2.1, y=-1.3, b=-.8, w=.6), k(.56, 'sill', x=1.8, y=-.9, b=-.3, eye='^'), k(.75, 'item', x=1.3, y=-.5, b=.2), k(.9, eye='^')],
        [(.56, 'trade'), (.75, 'mates')], g='show', act=('present', 'charm'), ages=GROWN, prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))],
        duo=[k(.2, x=.3, y=-.3), k(.4, 'item', x=1.1, y=-.9, b=.3, eye='O'), k(.58, 'item', x=1.2, y=-1, b=.5, eye='^', mark='ooh'), k(.78, 'item', x=1, y=-.6, b=.1, eye='^')])
    return done(o)


# @@rainbow_charm
def rainbow_charm():
    # Drawing: a cord loop above, a round charm; in the middle a rainbow of three nested arcs (`.--==--.`, `/.-=-.\`, `| |  | |`) sitting on a row of `=-=` below; glowing.
    o = Obj('rainbow_charm', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, cord='the cord loop above the charm', rim='the round rim of the charm', arcs='the three nested rainbow arcs in the middle', band='the band of =-= under the arcs'),
            fields=dict(shimmer=(0, 0, 1), dull=(.3, 0, 1)),
            physics=[('shimmer', 'rate', .002, 'rainbow_sky'), ('shimmer', 'rate', -.0006, 'always'), ('dull', 'rate', .0004, 'always')],
            effects=dict(bask=[('shimmer', 'set', 1)], shine=[('dull', 'set', 0)], tire=[('shimmer', 'mul', .3)], fun=[('need.fun', 'add', 2)], rest=[('need.energy', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_c=P(56, 70), slat_d=P(71, 68), stud_l=P(10, 70), stud_r=P(95, 70), stand_l=P(22, 60), glass_l=P(15, 59),
                         glass_m=P(49, 58), sill=P(40, 63), plate_lo=P(11, 63)))
    o.r('jig_in_time_with_the_arcs', 'Dancing a jig along the foot of the case, one hop for each colour of the arcs', 20, 'none',
        [k(.12, 'slat_a', x=.5, y=.3, b=-.5, w=.4, l=1), k(.3, 'slat_c', x=.8, y=.4, b=-.7, w=.8, r=1), k(.5, 'slat_d', x=.9, y=.3, b=-.8, w=1, l=1), k(.7, 'slat_c', x=.7, y=.4, b=-.7, w=.8, r=1),
         k(.88, 'slat_a', x=.4, y=.2, b=-.3, eye='^')],
        [], g='show', act=('dance', 'arcs'), prefer=['happy'], say=["Seven colours, seven hops. Counted four. Close.", "Jig done. The arcs stayed still. Tough crowd."])
    o.r('lean_a_shoulder_on_the_right_stud', 'Leaning a shoulder against the right stud and sighing at the arcs that will not come down', 22, 'none',
        [k(.15, 'stud_r', x=-.5, y=.5, b=.4), k(.4, 'stud_r', x=-.9, y=.8, b=1.1, w=.3, eye='-'), k(.7, 'stud_r', x=-1, y=.9, b=1.3, r=1, eye='-', mark='sigh'), k(.9, x=-.3, y=.2, b=.3)],
        [(.7, 'rest')], g='rest', act=('lean', 'stud'), prefer=['tired'])
    o.r('hop_up_at_the_rainbow_and_miss', 'Hopping up toward the arcs, missing the pot of anything at the end, and landing hard', 18, 'none',
        [k(.15, 'slat_d', x=.6, y=.2, b=-.5, l=1), k(.3, x=.1, y=-1.1, b=-1.1, w=.6, eye='O'), k(.46, x=.2, y=-1.4, b=-1.5, w=1, l=1, eye='O'), k(.66, x=-1.1, y=1.2, b=1.5, w=.3, eye='@', mark='thud'), k(.9, y=.5, b=.3, eye='-')],
        [], g='mishap', act=('hop', 'arcs'), prefer=['young'])
    o.r('lean_against_the_stud_and_wait_for_the_rainbow', 'Leaning against the left stud, waiting for the sky to bring a rainbow out', 28, 'none',
        [k(.15, 'stud_l', x=-.4, y=.5, b=.6), k(.4, 'stud_l', x=-.7, y=-.2, b=1.2, eye='o'), k(.7, 'stud_l', x=-.7, y=-.3, b=1.2, l=1, eye='O', mark='...'), k(.9, x=-.2, y=.2)],
        [], g='weather', act=('wait', 'rainbow'), when=['rainbow_sky'])
    o.r('lift_the_charm_out_to_see_the_arcs', 'Lifting the charm out in his bill, holding it at arm\'s length to see the arcs glow, and setting it back', 22, 'none',
        [k(.1, x=.6, y=-.4), k(.25, 'item', x=1.5, y=-.7, b=.3, mark='hup'), k(.42, 'item', x=1.2, y=-1.2, b=-.4), k(.58, 'item', x=1, y=-.6, eye='O'), k(.74, 'stand_l', x=1.3, y=-.3), k(.88, eye='^')],
        [], g='use', act=('lift', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["Glows in my bill. Free night light.", "Out of the case. The arcs didn't stop me. Brave."])
    o.r('rock_the_charm_to_swing_the_arcs', 'Rocking the charm on its cord in his bill so the arcs swing like a pendulum', 20, 'none',
        [k(.1, x=.8, y=-.5, b=.5), k(.22, 'item', x=.9, y=-.9, b=.1), k(.38, 'item', x=2, y=-.8, b=.2, l=1), k(.54, 'item', x=.5, y=-.2, b=.7, r=1, eye='O'), k(.7, 'item', x=1.9, y=-.9, b=.1), k(.88, eye='-')],
        [(.54, 'fun')], g='use', act=('rock', 'cord'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.36, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=0))], say=['Pendulum duck. Hypnotising the slats.', 'Swing, swing. The arcs got seasick.'])
    o.r('hold_the_charm_up_to_the_rainbow_sky', 'Showing the lifted charm to the rainbow in the sky, arcs to arcs, until it blazes', 26, 'none',
        [k(.1, x=.6, y=-.4), k(.24, 'item', x=1.4, y=-.7, b=.2), k(.42, 'glass_m', x=1.6, y=-1.4, b=-.7, w=.5, eye='O'), k(.62, 'glass_m', x=1.7, y=-1.5, b=-.8, w=.8, eye='^', mark='ooh'), k(.78, 'item', x=1.3, y=-.5),
         k(.9, eye='^')],
        [(.62, 'bask')], g='weather', act=('show', 'arcs'), when=['rainbow_sky'], ages=GROWN,
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Rainbow to rainbow. The charm outshone the sky. Don't tell the sky.", "Glowing like a shop sign. Lovely."])
    o.r('buff_the_arcs_on_his_chest', 'Polishing the arcs on the lifted charm over his chest feathers until the colours separate', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.4, b=.3), k(.44, 'item', x=.3, y=.5, b=.8, w=.4, mark='rub'), k(.6, 'item', x=.1, y=.7, b=1, mark='rub'), k(.78, 'item', x=1.1, y=-.5, b=.3), k(.9, eye='^')],
        [(.6, 'shine')], g='care', act=('polish', 'arcs'), when=['dull>.4'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('peer_for_the_glow_inside_the_arcs', 'Peering at the glow inside the arcs of the lifted charm to see where it comes from', 20, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1, y=-.5, b=.2), k(.45, 'glass_l', x=2, y=.3, b=.7, eye='@'), k(.65, 'glass_l', x=2.1, y=.4, b=.6, eye='O'), k(.8, 'item', x=.9, y=-.4), k(.9, eye='-')],
        [(.65, 'tire')], g='test', act=('peer', 'glow'), when=['shimmer>.3'], ages=GROWN,
        obj=[(.25, dict(hold=0)), (.4, dict(hold=1)), (.82, dict(hold=1)), (.88, dict(hold=0))])
    o.r('carry_the_charm_in_a_wide_arc', 'Carrying the lifted charm round the case in one wide arc, bill high, and parking it by the plate', 26, 'none',
        [k(.1, x=.3, y=-.3), k(.22, 'item', x=1.3, y=-.8, b=.3), k(.38, x=1.5, y=-.9, b=-.4, l=1), k(.55, x=1.8, y=-1, b=-.5, r=1, w=.5), k(.74, 'plate_lo', x=1.3, y=-.1, b=.3), k(.88, eye='^')],
        [(.74, 'fun')], g='play', act=('carry', 'arcs'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Wide arc, high bill. Parade of one.", "Carried a rainbow. Heaviest light I've held."])
    o.r('shake_the_charm_so_the_arcs_flicker', 'Shaking the lifted charm in short jerks so the arcs flicker through their colours', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.2, y=-.6, b=.3), k(.38, 'item', x=1.6, y=-.4, b=.6, mark='zzt'), k(.5, 'item', x=1.1, y=-.7, b=-.1, mark='zzt'), k(.62, 'item', x=1.6, y=-.4, b=.6, mark='zzt'),
         k(.78, 'sill', x=1.2, y=-.3), k(.9, eye='@')],
        [], g='play', act=('shake', 'charm'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.34, dict(hold=1)), (.76, dict(hold=1)), (.84, dict(hold=0))], say=['Shook it. Colours went rude.', 'Arcs flickered like a bad bulb. Magic.'])
    o.r('present_the_glow_to_a_friend', 'Presenting the lifted charm to a friend so they can hold their paw in its glow', 26, 'none',
        [k(.1, x=.5, y=-.4), k(.22, 'item', x=1.4, y=-.8, b=.5), k(.4, 'item', x=1.9, y=-1.4, b=-1, w=.4), k(.58, 'item', x=1.5, y=-.9, b=-.4), k(.78, 'stud_l', x=1.2, y=.2, b=.3), k(.9, eye='^')],
        [], g='show', act=('present', 'glow'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=.9, y=-.9, b=.3, eye='O'), k(.62, 'item', x=1, y=-1, b=.4, eye='^', mark='aww'), k(.8, x=-.1, y=-.4, eye='^')])
    return done(o)


# @@dance_medal
def dance_medal():
    # Drawing: a long ribbon in a V of slashes (166 px) to a `[=]` clasp at 99 px, then a round medal with a ring of arcs and, inside, a small upright dancer figure.
    o = Obj('dance_medal', 'display', on='trophy_case',
            parts=dict(CASE_PARTS, ribbon='the long V ribbon hanging from the top', clasp='the [=] clasp where the ribbon meets the medal', medal='the round medal with its ring of arcs', dancer='the small upright dancer figure in the middle'),
            fields=dict(crease=(.3, 0, 1), flutter=(0, 0, 1)),
            physics=[('crease', 'rate', .0004, 'always'), ('flutter', 'rate', -.001, 'always')],
            effects=dict(crumple=[('crease', 'add', .4)], smooth=[('crease', 'set', 0)], snap=[('flutter', 'set', 1)], rest=[('need.energy', 'add', 2)],
                         mates=[('need.social', 'add', 2)]),
            anchors=dict(item=0, slat_a=P(26, 69), slat_b=P(41, 67), slat_d=P(71, 68), rail_l=P(30, 72), stud_l=P(10, 70), stud_r=P(95, 70), stand_l=P(22, 60), ledge=P(30, 61),
                         glass_l=P(15, 59), glass_m=P(49, 58), sill=P(40, 63), plate_lo=P(11, 63)))
    o.r('bow_to_the_medal_like_a_judge', 'Bowing low at the foot of the case, as a dancer does to the judges who gave out the medal', 16, 'none',
        [k(.15, x=-.9, y=-.9, b=-1), k(.4, 'slat_b', x=1.7, y=2.5, b=1.6), k(.6, 'slat_b', x=1.7, y=2.7, b=1.7, mark='bravo'), k(.85, x=.4, y=-.9, b=-.9, w=.9, eye='^')],
        [], g='show', act=('bow', 'medal'), prefer=['happy'], say=["Bowed first. Not one judge has called that a win.", "Judges: absent. Medal: shiny. Bow: complete."])
    o.r('shuffle_a_quick_step_to_earn_it', 'Dancing a quick step along the base to earn the medal, in time to nothing', 20, 'none',
        [k(.12, 'slat_a', x=.5, y=.5, b=-.4, l=1), k(.3, 'slat_b', x=.7, y=.5, b=-.6, w=.6, r=1), k(.5, 'slat_d', x=.8, y=.4, b=-.7, w=.9, l=1), k(.7, 'slat_b', x=.6, y=.5, b=-.5, w=.6, r=1),
         k(.88, 'slat_a', x=.3, y=.3, b=-.2, eye='^')],
        [], g='play', act=('dance', 'slats'), prefer=['happy', 'young'])
    o.r('trip_over_the_two_left_feet', 'Slipping mid-step on a dance he has not practised and ending up against the right stud', 16, 'none',
        [k(.15, x=.5, y=.1, b=-.4, l=1), k(.32, x=1.2, y=.4, b=-.8, w=.8, l=1, r=1, eye='O', mark='whoa'), k(.52, 'stud_r', x=1.5, y=1.9, b=2.1, eye='@', mark='thud'), k(.75, 'stud_r', x=.8, y=1, b=1, eye='-'),
         k(.9, eye='^')],
        [], g='mishap', act=('slip', 'step'), prefer=['young'], say=["Two left feet. Both of them mine, unfortunately.", "Dance floor: one, Cheese: nil."])
    o.r('sit_out_the_dance_at_the_stud', 'Sitting out the dance beside the left stud, a wing tapping a slow beat', 24, 'none',
        [k(.15, 'stud_l', x=.2, y=.5, b=1.2), k(.4, 'stud_l', x=.1, y=.6, b=1.5, l=1, mark='tap'), k(.65, 'stud_l', x=.1, y=.6, b=1.5, r=1, mark='tap'), k(.88, x=.3, y=.2, b=.5)],
        [(.65, 'rest')], g='rest', act=('sit', 'beat'), when=['tired'])
    o.r('lift_the_medal_out_by_its_ribbon', 'Lifting the medal out of its place by the ribbon in his bill and holding it up to the light', 22, 'none',
        [k(.1, x=.6, y=-.4), k(.25, 'item', x=1.5, y=-.9, b=.4, mark='hup'), k(.42, 'item', x=1.1, y=-1.4, b=-.6), k(.58, 'item', x=.8, y=-.8, eye='O'), k(.74, 'stand_l', x=1.2, y=-.4), k(.88, eye='^')],
        [], g='use', act=('lift', 'medal'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.62, dict(hold=1)), (.7, dict(hold=1)), (.84, dict(hold=0))], say=["The ribbon's long. The medal's heavier than my talent.", "Out of the case. No fanfare. Rude."])
    o.r('tug_the_ribbon_taut_and_let_go', 'Tugging the ribbon taut in his bill and letting it snap back against the medal', 18, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.4, y=-.6, b=.3), k(.4, 'item', x=2.1, y=-.4, b=.9, l=1, mark='hnn'), k(.52, 'item', x=-.4, y=-.5, b=-.5, w=.7, mark='SNAP'), k(.7, 'item', x=1.2, y=-.4), k(.88, eye='^')],
        [(.52, 'crumple')], g='use', act=('tug', 'ribbon'), ages=GROWN, prefer=['grumpy', 'flutter<.3'],
        obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.74, dict(hold=1)), (.84, dict(hold=0))])
    o.r('straighten_the_creased_ribbon', 'Straightening the creased ribbon along the ledge with the flat of his bill', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.3), k(.42, 'ledge', x=1.3, y=.4, b=.6, mark='shh'), k(.6, 'ledge', x=1.7, y=.5, b=.8, mark='shh'), k(.76, 'item', x=1.2, y=-.4), k(.9, eye='^')],
        [(.6, 'smooth')], g='care', act=('straighten', 'ribbon'), when=['crease>.4'], ages=GROWN,
        obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('fold_the_ribbon_in_three_and_back', 'Folding the ribbon in three along the plate with bill and wing, then letting it hang again', 24, 'wing',
        [k(.1, 'item', reach=.5, x=.8, y=-.5, b=.3), k(.26, 'plate_lo', reach=1, x=1.1, y=.1, b=.6), k(.44, 'plate_lo', reach=1, x=1.3, y=.3, b=.8, l=1), k(.62, 'plate_lo', reach=1, x=1.1, y=.1, b=.7, r=1),
         k(.8, 'item', reach=.7, x=.8, y=-.4, b=.2), k(.9, eye='^')],
        [(.62, 'crumple')], g='care', act=('fold', 'ribbon'), ages=GROWN)
    o.r('measure_the_ribbon_against_his_wing', 'Measuring the ribbon of the lifted medal against his wing, clasp to tip, and finding it longer', 22, 'none',
        [k(.1, x=.4, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.3), k(.42, 'glass_l', x=1.8, y=-.9, b=-.4, w=.6), k(.6, 'glass_l', x=2, y=-1.3, b=-.7, w=1, eye='O'), k(.78, 'item', x=1.2, y=-.4), k(.9, eye='-')],
        [], g='test', act=('measure', 'ribbon'), ages=GROWN,
        obj=[(.24, dict(hold=0)), (.36, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=['Ribbon wins by a feather. Again.', 'Measured twice. Cried once. Dramatic.'])
    o.r('catch_the_wind_in_the_ribbon', 'Catching the wind in the ribbon of the lifted medal and flying it like a banner', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.4, y=-.8, b=.3), k(.4, 'glass_m', x=1.7, y=-1.2, b=-.5, w=.6), k(.58, 'glass_m', x=1.9, y=-1.3, b=-.7, w=.9, eye='^', mark='flap'), k(.76, 'item', x=1.3, y=-.5),
         k(.9, eye='^')],
        [(.58, 'snap')], g='weather', act=('catch', 'wind'), when=['windy'], ages=GROWN,
        obj=[(.22, dict(hold=0)), (.34, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('strike_a_pose_with_the_medal_for_a_friend', 'Striking a pose with the lifted medal for a friend who judges the form', 26, 'none',
        [k(.1, x=.4, y=-.4, b=.3), k(.22, 'item', x=1.5, y=-.8, b=.5), k(.4, 'sill', x=1.9, y=-1.4, b=-1, w=.9, l=1), k(.58, 'sill', x=2, y=-1.5, b=-1.1, w=1, r=1, eye='^'), k(.78, 'item', x=1.4, y=-.5),
         k(.9, eye='^')],
        [(.58, 'mates')], g='show', act=('pose', 'medal'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.36, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.25, x=.3, y=-.3), k(.45, 'item', x=1, y=-.8, b=.3, eye='O'), k(.65, 'item', x=1.1, y=-.9, b=.5, eye='^', mark='9.5'), k(.82, x=-.1, y=-.4, eye='^')])
    o.r('dance_round_the_case_with_the_medal', 'Dancing round the case with the medal swinging from his bill, ribbon trailing in the air', 26, 'none',
        [k(.1, x=.3, y=-.3), k(.2, 'item', x=1.4, y=-.7, b=.3), k(.36, x=1.2, y=-.5, b=-.6, w=.7, l=1), k(.52, x=1.6, y=-.6, b=-.8, w=1, r=1), k(.7, 'rail_l', x=1.3, y=.6, b=.4), k(.88, eye='^')],
        [(.7, 'snap')], g='play', act=('dance', 'medal'), ages=GROWN, prefer=['happy'],
        obj=[(.2, dict(hold=0)), (.32, dict(hold=1)), (.78, dict(hold=1)), (.86, dict(hold=0))], say=['Twirled? No. Shuffled. The ribbon kept up.', 'Danced with the medal like it asked.'])
    return done(o)


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


if __name__ == '__main__':
    todo = sys.argv[1:] or ['trophy_case', 'ancient_amulet', 'lucky_charm', 'earth_token', 'sky_token', 'water_token', 'magpie_friendship_charm', 'rainbow_charm', 'dance_medal']
    for name in todo:
        o = globals()[name]()
        o.emit(**({'need': 1} if os.environ.get('DRAFT') else {}))
    print(COUNT)
