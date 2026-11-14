"""Wave 5a: six things shown in the trophy case: earth_token, sky_token, water_token, magpie_friendship_charm, rainbow_charm, dance_medal.
Every routine is hand-written. Host trophy_case (106 cols x 77 rows, 7.2 px a row, standing line row 75): base slats rows 67-71 (58-29 px, a `|` every fifth column from 11),
`o` studs at each end of row 70 (36 px), bottom rail row 72 (22 px), trim bars rows 65 and 62 (72 and 93 px), the sill bar row 63 (86 px), plates `(=)` on the left frame,
door seam at col 53, three `[____]` stands at row 60 (108 px). The shown thing is `item` (115 px, lowest slot). Anchors are literal fractions (col/105, row/77)
so rep.py --mark can draw them. Marks draw visible state on the case: breath mist and nose prints on the glass, scuffs, rime, glare."""
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
COUNT_NEED = {}


def done(o):
    COUNT[o.d['object']] = len(o.d['routines'])
    return o


# @@dance_medal
def dance_medal():
    # Drawing: a wide ribbon in a V (slashes, 166 px down to a `[=]` clasp at 99 px), a round medal with a ring of arcs and, inside, a small upright emblem
    # (`/|   |`, `| 1 |`, `o_|  o`, `(_)`) that I do not name: it is "the emblem". What it IS here is an invitation: it is a dance medal, so the acts are steps, turns and
    # judging, done at the foot of the case where there is room. Floor = the standing line in front of the base.
    o = Obj('dance_medal', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), scuffs=(0, 0, 1), glare=(0, 0, 1), rime=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('scuffs', 'rate', -.0002, 'always'),
                     ('glare', 'rate', .002, 'sun'), ('glare', 'rate', -.001, 'always'), ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         scuff=[('scuffs', 'add', .4)], smooth=[('scuffs', 'set', 0)], shade=[('glare', 'mul', .2)], defrost=[('rime', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         jig=[('need.fun', 'add', 2)], primp=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('scuffs', .3, '.:.:.', 'rail', 'dust'),
                   ('rime', .3, '*-*-*', 'trim_l', 'frost'), ('glare', .3, '. * .', 'sill_r', 'glow')],
            anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_c=(0.8190, 0.8961), slat_d=(0.1524, 0.8831), slat_e=(0.3429, 0.9091), slat_g=(0.6286, 0.8831), slat_h=(0.7238, 0.9091), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), sill=(0.3810, 0.8182), sill_r=(0.6667, 0.8182), plate_lo=(0.1048, 0.8182), seam_lo=(0.5048, 0.7532)))
    # ---------------- care
    o.r('sweep_the_toe_scuffs_off_the_rail', 'Sweeping the toe scuffs off the bottom rail with a wing, left end to right', 16, 'wing',
        [k(.12, 'rail_l', reach=.6, x=.3, y=.8, b=.5), k(.3, 'rail_l', reach=1, x=.6, y=1.2, b=.8, l=1), k(.5, 'rail', reach=1, x=.6, y=1.2, b=.9), k(.7, 'rail_r', reach=1, x=.6, y=1.3, b=.9, r=1), k(.88, eye='^')],
        [(.5, 'smooth')], g='care', act=('sweep', 'scuffs'), when=['scuffs>.3'], prefer=['grown'], say=["Swept my own footprints. Evidence of a good night.", "Floor's clean. Dancing can resume."])
    o.r('rub_the_nose_prints_off_in_small_circles', 'Rubbing the nose prints off the pane in small circles with a wing, ear to ear', 18, 'wing',
        [k(.12, 'trim_l', reach=.6, x=.3, y=-.2, b=.3), k(.3, 'trim_l', reach=1, x=.5, y=-.4, b=.5, w=.3), k(.5, 'trim_lo', reach=1, x=.5, y=-.4, b=.4, l=1), k(.7, 'trim_lo', reach=1, x=.6, y=-.3, b=.5, r=1), k(.88, eye='-')],
        [(.5, 'buff')], g='care', act=('wipe', 'prints'), when=['prints>.3'], prefer=['curious'])
    o.r('polish_the_end_studs_with_his_bill', 'Polishing the two end studs with his bill, spinning on the spot between them', 18, 'none',
        [k(.12, 'stud_l', x=1.1, y=1.1, b=.6, mark='rub'), k(.3, 'stud_l', x=.9, y=.9, b=.8, l=1), k(.5, x=-.3, y=-.3, b=-.5, w=.8, r=1), k(.7, 'stud_r', x=1.2, y=1.1, b=.7, mark='rub'), k(.88, 'stud_r', x=.9, y=.9, b=.6, eye='^')],
        [(.7, 'clean')], g='care', act=('polish', 'studs'), when=['obj_dirt>.3'], prefer=['happy'])
    o.r('dry_the_rain_off_the_glass', 'Drying the rain streaks off the pane with a wing, down from the sill to the trim', 18, 'wing',
        [k(.12, 'sill_r', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'sill_r', reach=1, x=.7, y=-.5, b=-.3, w=.3), k(.5, 'trim_lo', reach=1, x=.6, y=-.3, b=.2, r=1), k(.7, 'trim_l', reach=1, x=.5, y=-.2, b=.3), k(.88, eye='^')],
        [(.5, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'])
    o.r('chip_the_rime_off_the_left_trim', 'Chipping the rime off the left trim and plate with the tip of a wing', 16, 'wing',
        [k(.12, 'trim_l', reach=.6, x=.2, y=-.2, b=.3), k(.3, 'trim_l', reach=1, x=.5, y=-.4, b=.5, mark='tk'), k(.5, 'plate_lo', reach=1, x=.5, y=-.3, b=.6, l=1, mark='tk'), k(.7, 'plate_lo', reach=1, x=.4, y=-.4, b=.5), k(.88, eye='-')],
        [(.5, 'defrost')], g='care', act=('chip', 'rime'), when=['rime>.3'], ages=GROWN)
    o.r('primp_his_feathers_in_the_glass', 'Primping his feathers at the pane, one cheek and then the other, for the judges', 18, 'none',
        [k(.12, x=.4, y=-.2, b=.3), k(.3, 'sill', x=1.1, y=-.5, b=.4, eye='O'), k(.5, 'sill', x=.9, y=-.3, b=.3, w=.5, l=1, eye='^'), k(.7, 'sill', x=1.0, y=-.5, b=.4, w=.6, r=1, mark='hm'), k(.88, y=.1, eye='^')],
        [(.5, 'primp')], g='care', act=('groom', 'feathers'), prefer=['happy'], say=["Presentable. Judges: undecided. Mirror: obsessed.", "One cheek better than the other. Showing that one."])
    # ---------------- use
    o.r('hold_the_ribbon_up_to_his_neck', 'Lifting the medal out in his bill and holding its ribbon up against his neck to see how it would hang', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.42, 'item', x=.4, y=.6, b=.7, l=1), k(.6, 'item', x=.3, y=.8, b=.9, r=1, eye='^', mark='hm'), k(.76, 'item', x=1.2, y=-.5, b=.2), k(.9, eye='^')],
        [], g='use', act=('fit', 'ribbon'), ages=GROWN, prefer=['happy'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.64, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        say=["Suits me. Everything does. The ribbon is a bit long.", "Neck: decorated. Ego: also decorated."])
    o.r('tap_out_the_beat_on_the_rail', 'Tapping the beat out on the bottom rail with alternate feet, bill nodding along', 16, 'none',
        [k(.12, 'rail', x=.4, y=.5, b=.3, l=1), k(.3, 'rail', x=.5, y=.7, b=.5, r=1, mark='tk'), k(.48, 'rail', x=.5, y=.7, b=.4, l=1, mark='tk'), k(.66, 'rail', x=.5, y=.7, b=.5, r=1, mark='tk'), k(.84, 'rail', x=.4, y=.4, b=.3, eye='^')],
        [(.66, 'scuff')], g='use', act=('tap', 'rail'), prefer=['happy', 'young'], say=["One two three four. Five is where I get lost.", "The rail has rhythm. The rail has no choice."])
    o.r('count_the_beat_in_a_mutter', 'Counting the beat under his breath with his head swaying, one, two, three, and again', 18, 'none',
        [k(.15, x=.2, y=-.2, b=.3, mark='1'), k(.32, x=.5, y=-.4, b=-.3, mark='2'), k(.5, x=.2, y=-.2, b=.3, l=1, mark='3'), k(.68, x=-.4, y=-.4, b=-.3, mark='1'), k(.86, x=.2, y=-.2, b=.2, r=1, eye='-')],
        [], g='use', act=('count', 'beat'), prefer=['curious'])
    o.r('peer_up_the_ribbon_to_the_top', 'Peering up the long ribbon to where it starts, head tipped further back each time', 16, 'none',
        [k(.15, x=.6, y=-.8, b=-.5), k(.35, x=-.6, y=-1.5, b=-.9, eye='O'), k(.55, x=-1.2, y=-2.0, b=-1.4, w=.3, eye='O', mark='ooh'), k(.8, x=.3, y=-.5, b=.3, eye='-')],
        [], g='use', act=('peer', 'ribbon'), prefer=['curious', 'young'])
    o.r('carry_the_medal_round_in_a_small_waltz', 'Carrying the medal out in his bill and turning a slow waltz with it before putting it back', 28, 'none',
        [k(.1, x=.5, y=-.3), k(.22, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.4, 'item', x=.8, y=-.9, b=-.5, l=1), k(.56, 'item', x=.5, y=-.7, b=-.6, r=1), k(.7, 'item', x=.8, y=-.9, b=-.5, l=1, w=.4), k(.84, 'item', x=1.2, y=-.5, b=.2), k(.94, eye='^')],
        [(.56, 'jig')], g='use', act=('carry', 'medal'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.72, dict(hold=1)), (.86, dict(hold=1)), (.92, dict(hold=0))],
        say=["Waltzed with a medal. It never steps on toes.", "Led, obviously. It's a medal. It followed."])
    o.r('rap_the_lower_trim_in_tango_time', 'Rapping the lower trim bar with his bill in tango time, slow slow quick quick slow', 18, 'none',
        [k(.12, 'trim_l', x=1.2, y=-.3, b=.4, mark='tk'), k(.28, 'trim_l', x=1.3, y=-.3, b=.5, l=1, mark='tk'), k(.42, 'trim_lo', x=1.2, y=-.3, b=.3, mark='tk tk'), k(.58, 'trim_lo', x=1.3, y=-.3, b=.4, r=1, mark='tk tk'), k(.76, 'trim_lo', x=1.2, y=-.4, b=.5, w=.4, mark='TK'), k(.9, eye='^')],
        [], g='use', act=('drum', 'trim'), ages=['duckling', *GROWN], prefer=['grumpy', 'curious'])
    o.r('ask_the_doors_for_the_next_dance', 'Knocking on the door seam to ask the case for the next dance and waiting for the answer', 18, 'none',
        [k(.12, x=.3, y=-.4, b=.2), k(.3, 'seam_lo', x=1.0, y=-.7, b=.2, mark='tk'), k(.48, x=-.2, y=-.3, b=-.2, w=.3, eye='O'), k(.66, 'seam_lo', x=1.0, y=-.7, b=.3, l=1, mark='tk tk'), k(.84, y=.2, eye='-', mark='...')],
        [], g='use', act=('knock', 'doors'), ages=GROWN, prefer=['lonely', 'curious'], say=["Asked politely. The doors have two left feet.", "No answer. I'll take that as a maybe."])
    # ---------------- play
    o.r('hop_step_along_the_slats', 'Hop-stepping along the base, a slat to a hop, left foot then right', 18, 'none',
        [k(.1, 'slat_d', x=.5, y=.7, b=.4, l=1), k(.28, 'slat_a', x=.5, y=.5, b=-.8, r=1, w=.4), k(.46, 'slat_e', x=.5, y=.6, b=.4, l=1), k(.64, 'slat_b', x=.5, y=.5, b=-.8, r=1, w=.4), k(.84, 'slat_g', x=.5, y=.6, b=.4, l=1, eye='^')],
        [(.84, 'jig')], g='play', act=('hop', 'slats'), prefer=['young', 'happy'])
    o.r('spin_till_the_floor_tilts', 'Spinning on the spot before the case, wings out, until the whole floor tilts', 18, 'none',
        [k(.12, x=.3, y=-.2, b=.2), k(.3, x=.9, y=-.6, b=-.8, w=1, l=1), k(.5, x=-.9, y=-.6, b=-.9, w=1, r=1, mark='whee'), k(.7, x=.8, y=-.5, b=-.7, w=1, l=1), k(.88, x=.1, y=.6, b=.8, eye='@')],
        [], g='play', act=('spin', 'floor'), prefer=['young', 'happy'])
    o.r('moonwalk_back_along_the_rail', 'Moonwalking backwards along the bottom rail, bill up, as if gliding', 20, 'none',
        [k(.1, 'rail_r', x=-.2, y=-.5, b=.2, l=1), k(.3, 'rail', x=-.6, y=-.7, b=.3, r=1), k(.5, 'rail', x=-.8, y=-.8, b=.2, l=1, mark='shh'), k(.7, 'rail_l', x=-.8, y=-.8, b=.3, r=1), k(.88, x=.2, y=-.3, w=.4, eye='^')],
        [(.7, 'scuff')], g='play', act=('drag', 'feet'), prefer=['happy'], say=["Smooth. Backwards. Nobody saw the stumble.", "That's the glide. The stumble was choreography."])
    o.r('kick_line_for_one', 'Kicking each leg out to the side in turn like a whole chorus line, all of it him', 18, 'none',
        [k(.12, x=.2, y=-.3, b=-.3, w=.5), k(.3, x=.3, y=-.5, b=-.5, w=.8, l=1), k(.46, x=.3, y=-.5, b=-.4, w=.8, r=1), k(.62, x=.4, y=-.6, b=-.6, w=1, l=1), k(.78, x=.4, y=-.6, b=-.6, w=1, r=1), k(.9, eye='^')],
        [], g='play', act=('kick', 'line'), prefer=['happy', 'young'])
    o.r('rock_side_to_side_to_a_slow_song', 'Rocking side to side at the foot of the case to a slow song only he can hear', 22, 'none',
        [k(.15, 'slat_c', x=-.3, y=.2, b=.4, l=1), k(.35, x=.5, y=-.2, b=.6, r=1, eye='-'), k(.55, 'slat_c', x=-.4, y=.1, b=.5, l=1, eye='-', mark='la'), k(.75, x=.5, y=-.2, b=.6, r=1, eye='-'), k(.9, eye='^')],
        [], g='play', act=('rock', 'hips'), prefer=['sad', 'happy'])
    o.r('rise_on_his_toes_with_a_wing_on_the_slat', 'Rising onto his toes with one wing on a slat for a barre and holding the pose', 20, 'wing',
        [k(.12, 'slat_g', reach=.6, x=.2, y=-.2, b=.2), k(.3, 'slat_g', reach=1, x=.2, y=-1.0, b=-.7, l=1), k(.52, 'slat_g', reach=1, x=.3, y=-1.3, b=-.9, l=1, r=1, mark='...'), k(.72, 'slat_g', reach=1, x=.2, y=-.8, b=-.5, r=1), k(.88, eye='^')],
        [], g='play', act=('balance', 'toes'), prefer=['curious', 'happy'])
    # ---------------- test
    o.r('mimic_the_emblem_to_see_if_it_fits', 'Mimicking the emblem pose before the case, wings out, to see whether he fits the medal', 20, 'none',
        [k(.15, x=.2, y=-.4, b=-.2, w=.5), k(.35, x=.6, y=-1.0, b=-.7, w=1, l=1, eye='>'), k(.55, x=.7, y=-1.1, b=-.8, w=1, l=1, r=1, mark='hm'), k(.75, x=.3, y=-.4, b=-.3, w=.5, eye='-'), k(.9, eye='^')],
        [], g='test', act=('compare', 'emblem'), prefer=['curious'], say=["Close. The emblem has fewer chins.", "Matches the pose. Not the grace. Yet."])
    o.r('listen_at_the_lower_trim_for_music', 'Listening with his ear flat to the lower trim bar for any music in the case', 18, 'none',
        [k(.15, x=.5, y=-.3, b=.2), k(.35, 'trim_l', x=-.2, y=-.7, b=.6, eye='-'), k(.58, 'trim_l', x=-.3, y=-.7, b=.8, l=1, eye='-', mark='...'), k(.78, x=.4, y=-.5, b=.3, w=.4, eye='O')],
        [], g='test', act=('listen', 'trim'), ages=['duckling', *GROWN], prefer=['curious'])
    o.r('pace_out_a_stride_along_the_base', 'Pacing out his stride along the base, slat to slat, to check he can reach the next dance', 22, 'none',
        [k(.1, 'stud_l', x=.4, y=.5, b=.3, l=1), k(.3, 'slat_a', x=.6, y=.5, b=-.2, r=1), k(.5, 'slat_b', x=.6, y=.5, b=-.2, l=1), k(.7, 'slat_h', x=.6, y=.5, b=-.2, r=1), k(.88, 'stud_r', x=.4, y=.5, b=.3, eye='-', mark='hm')],
        [], g='test', act=('measure', 'stride'), prefer=['curious'])
    o.r('sniff_the_ribbon_for_old_sweat', 'Lifting the medal out in his bill to sniff the ribbon for old sweat and trophies past', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.25, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.45, 'item', x=1.0, y=.4, b=.7, eye='-', mark='snf'), k(.62, 'item', x=1.0, y=.5, b=.8, l=1, eye='O'), k(.78, 'item', x=1.2, y=-.5, b=.2), k(.9, eye='>')],
        [], g='test', act=('sniff', 'ribbon'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.66, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))], say=["Sweat, polish and applause. Mostly applause.", "Smells like someone else's best night."])
    o.r('weigh_the_medal_in_his_bill_for_effort', 'Weighing the lifted medal in his bill, up and down, to judge how much effort it cost to win', 22, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.3, mark='hup'), k(.4, 'item', x=1.5, y=-1.0, b=-.5), k(.54, 'item', x=1.2, y=.2, b=.7), k(.68, 'item', x=1.5, y=-1.0, b=-.5), k(.82, 'item', x=1.2, y=-.5, b=.2), k(.92, eye='-')],
        [], g='test', act=('weigh', 'medal'), ages=GROWN, prefer=['curious', 'grumpy'],
        obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))])
    o.r('try_the_floor_with_one_toe_then_both', 'Trying the floor at the foot of the case with one toe, then both, for sprung boards', 18, 'none',
        [k(.15, 'rail', x=.3, y=.8, b=.4, l=1), k(.33, 'rail', x=.3, y=.9, b=.6, l=1, mark='tk'), k(.52, 'rail', x=.2, y=.7, b=.9, l=1, r=1, mark='tk tk'), k(.7, 'rail', x=.3, y=.7, b=1.0, w=.4, eye='-'), k(.88, eye='^')],
        [], g='test', act=('test', 'floor'), prefer=['curious', 'young'])
    # ---------------- rest
    o.r('nap_with_his_chin_on_the_rail', 'Napping with his chin resting against the bottom rail and one foot still keeping time', 28, 'none',
        [k(.15, x=.6, y=.5, b=.3), k(.4, 'rail', x=.4, y=1.5, b=1.2, eye='-'), k(.7, 'rail', x=.4, y=1.7, b=1.4, r=1, eye='-', mark='zzz'), k(.9, x=-.3, y=-.3, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'rail'), when=['tired'], say=["Dreamt of a quickstep. Woke up with cramp.", "Out cold. Left foot still dancing."])
    o.r('lean_on_the_end_stud_catching_breath', 'Leaning a shoulder against the end stud, panting from all that dancing', 18, 'none',
        [k(.15, x=.3, y=.2, b=.3, l=1), k(.4, 'stud_r', x=-.8, y=.5, b=1.0, w=.3), k(.65, 'stud_r', x=-.9, y=.7, b=1.2, r=1, eye='-', mark='huff'), k(.88, x=.2, y=.2, b=.3)],
        [], g='rest', act=('lean', 'stud'), when=['scuffs>.35'], prefer=['tired'])
    o.r('sulk_that_nobody_will_partner_him', 'Sulking with his tail to the case because nobody will partner him', 22, 'none',
        [k(.15, x=-.8, y=.1, b=.2, l=1), k(.4, 'slat_c', x=-1.4, y=.8, b=1.2, w=.2, eye='-'), k(.7, 'slat_c', x=-1.5, y=1.0, b=1.3, w=.6, r=1, eye='-', mark='hmph'), k(.9, x=-.4, y=.4, b=.5)],
        [], g='rest', act=('sulk', 'partner'), when=['lonely'], say=["Wallflower. Of the duck variety. Great hair though.", "Two left feet and nobody to step on."])
    o.r('wait_with_a_foot_tapping_for_the_band', 'Waiting at the foot of the case with one foot tapping for a band that never starts', 26, 'none',
        [k(.15, x=.3, y=.1, b=.3, l=1), k(.35, x=.2, y=-.4, b=.6, r=1, eye='O'), k(.55, x=.3, y=.1, b=.7, l=1, mark='...'), k(.75, x=.2, y=-.4, b=.6, r=1, eye='-'), k(.9, x=.1, y=.2, b=.3, eye='>')],
        [], g='rest', act=('wait', 'band'), prefer=['lonely', 'curious'])
    o.r('sit_out_a_dance_by_the_end_stud', 'Sitting a dance out by the end stud with his bill on his chest, watching nobody dance', 24, 'none',
        [k(.15, 'stud_l', x=.3, y=.3, b=.5, l=1), k(.4, 'stud_l', x=.2, y=1.0, b=1.4, eye='-'), k(.65, 'stud_l', x=.2, y=1.2, b=1.5, eye='o', mark='sigh'), k(.85, x=.2, y=.4, b=.6, r=1)],
        [], g='rest', act=('sit', 'studs'), prefer=['sad', 'tired'])
    # ---------------- weather
    o.r('shade_the_glare_and_dance_in_the_dark_patch', 'Spreading a wing over the glare on the pane and shuffling along the patch of shade it makes', 20, 'wing',
        [k(.12, 'sill_r', reach=.6, x=.2, y=-.4, b=.2), k(.3, 'sill_r', reach=1, x=.5, y=-.8, b=-.4, w=.4), k(.5, 'sill_r', reach=1, x=.3, y=-.5, b=.4, l=1), k(.7, 'sill_r', reach=1, x=.4, y=-.7, b=-.3, r=1), k(.88, eye='^')],
        [(.3, 'shade')], g='weather', act=('hide', 'glare'), when=['glare>.3'], ages=GROWN, say=["Glare gone. Shadow's got better footwork than me.", "Shaded it. Dance floor now in mood lighting."])
    o.r('warm_each_foot_in_turn_by_the_rimed_trim', 'Lifting each frozen foot in turn beside the rimed trim and tucking it up to warm', 22, 'none',
        [k(.12, 'trim_l', x=.3, y=.4, b=.3), k(.3, 'trim_l', x=.2, y=.6, b=.7, l=1), k(.5, 'trim_l', x=.2, y=.6, b=.7, r=1, eye='-'), k(.7, x=.4, y=.2, b=.4, l=1, r=1, mark='brr'), k(.88, eye='^')],
        [], g='weather', act=('warm', 'feet'), when=['rime>.3'], ages=['duckling', *GROWN], prefer=['cold'])
    o.r('huddle_close_to_the_case_in_the_storm', 'Huddling close against the case with his back to the storm and the rain drumming a tune', 32, 'none',
        [k(.1, 'slat_b', x=-.5, y=.3, b=.6, l=1), k(.26, 'slat_b', x=-1.1, y=.9, b=1.1, w=.6, eye='>'), k(.44, 'slat_g', x=-1.3, y=1.5, b=1.9, w=.2, eye='-'), k(.7, 'slat_g', x=-1.2, y=1.2, b=1.6, r=1, eye='-', mark='drip'), k(.88, 'slat_g', x=-.4, y=.6, b=.9, eye='>')],
        [], g='weather', act=('shelter', 'case'), when=['storm', 'wet'])
    o.r('tap_along_to_the_rain_on_the_pane', 'Tapping the upper sill of the pane with his bill in time with the rain, swaying with every drop', 20, 'none',
        [k(.12, 'sill', x=.8, y=-.6, b=.1, l=1), k(.3, 'sill_r', x=1.1, y=-1.0, b=-.5, w=.3, mark='tk'), k(.48, 'sill', x=.9, y=-.8, b=-.2, w=.5, r=1, mark='tk'), k(.66, 'sill_r', x=1.1, y=-1.0, b=-.5, w=.3, mark='tk tk'), k(.84, 'sill', x=.7, y=-.5, b=0, eye='^')],
        [], g='weather', act=('tap', 'pane'), ages=GROWN, when=['obj_wetness>.3'], prefer=['happy'])
    o.r('puff_breath_clouds_and_waltz_through_them', 'Puffing out breath clouds in the cold and wheeling round after each one', 20, 'none',
        [k(.12, 'sill', x=1.2, y=-.4, b=.2, mark='haaa'), k(.3, x=-.4, y=-.5, b=-.5, w=.8, l=1, eye='O'), k(.5, 'sill', x=1.3, y=-.5, b=.3, mark='haaa'), k(.7, x=.5, y=-.4, b=-.6, w=.8, r=1), k(.88, eye='^')],
        [(.12, 'huff')], g='weather', act=('blow', 'clouds'), when=['cold'], ages=['duckling', *GROWN], prefer=['young', 'happy'])
    # ---------------- show
    o.r('bow_to_the_medal_with_a_flourish', 'Bowing to the medal with a flourish, one wing sweeping the floor and his bill at the rail', 16, 'none',
        [k(.14, x=-.8, y=-1.2, b=-.9, w=1, r=1), k(.34, x=.4, y=-.3, b=.2, w=1, l=1), k(.52, 'rail_l', x=1.7, y=1.4, b=1.6, w=.5, r=1), k(.7, 'rail_l', x=1.8, y=1.6, b=1.8, w=.3, mark='ta-da'), k(.88, x=-.2, y=-.4, b=-.2, w=.2, eye='^')],
        [], g='show', act=('bow', 'medal'), prefer=['happy'])
    o.r('present_the_medal_to_the_empty_floor', 'Presenting the medal to the empty floor with a sweep of his wing, as if announcing the winner', 18, 'wing',
        [k(.12, reach=.3, x=.3, y=-.2, b=.4, r=1), k(.3, reach=1, x=1.1, y=-.4, b=.9, l=1), k(.5, reach=1, x=1.3, y=.1, b=1.2, mark='and the winner'), k(.7, reach=1, x=.9, y=-.5, b=.6, r=1, w=.2), k(.88, reach=0, y=.3, b=.3, eye='^')],
        [], g='show', act=('present', 'winner'), prefer=['happy'], say=["And the winner is: the case. Sorry. Next year.", "Announced it. Crowd of one. Wild."])
    o.r('strike_the_emblem_pose_at_the_slat', 'Striking the emblem pose with one wing hooked round a slat, chin up for the judges', 18, 'wing',
        [k(.12, 'slat_h', reach=.6, x=.2, y=-.3, b=-.2), k(.34, 'slat_h', reach=1, x=.5, y=-1.2, b=-.5, w=.8, l=1), k(.58, 'slat_h', reach=1, x=.6, y=-1.4, b=-.6, w=.5, l=1, mark='...'), k(.82, y=.3, b=.2, eye='^')],
        [], g='show', act=('pose', 'emblem'), prefer=['happy'])
    o.r('argue_a_low_score_with_the_judges', 'Arguing his score with the judges, wing jabbing at the pane, and getting no reply', 18, 'none',
        [k(.12, x=1.4, y=.4, b=.7, eye='>'), k(.3, 'trim_lo', x=1.0, y=-.8, b=-.3, w=.9, mark='SEVEN?'), k(.5, x=-.6, y=.5, b=1.1, l=1), k(.68, 'trim_l', x=.9, y=-.9, b=-.4, w=1, r=1, mark='TEN!'), k(.9, y=.9, b=.5, eye='-')],
        [], g='show', act=('argue', 'judges'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["Seven? Seven. Judges are paid in bread, clearly.", "Appealed. Judges: none. Glass: smug."])
    o.r('hum_the_tune_the_medal_must_have_won_to', 'Humming the tune the medal must have won to, wing over his heart, swaying', 22, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.3, b=.2), k(.3, reach=1, x=.3, y=-.8, b=-.3, w=.4, mark='mmm'), k(.5, reach=1, x=.4, y=-1.0, b=-.5, w=.5, l=1, mark='MMM'), k(.7, reach=1, x=.3, y=-.7, b=-.2, r=1, mark='mm'), k(.88, eye='^')],
        [], g='show', act=('sing', 'tune'), prefer=['happy', 'lonely'])
    o.r('shout_encore_up_at_the_ribbon', 'Shouting ENCORE up at the ribbon, wings thrown wide, over and over', 14, 'none',
        [k(.15, x=.3, y=-.6, b=-.3), k(.35, x=1.6, y=-2.2, b=-1.6, w=1, mark='ENCORE'), k(.6, x=1.7, y=-2.3, b=-1.7, w=1, l=1, mark='ENCORE!'), k(.85, x=-.2, y=.2, eye='-')],
        [], g='show', far=True, act=('shout', 'encore'), prefer=['happy', 'grumpy'], say=["Encore. ENCORE. They never do one.", "Demanded another. Medal stayed put. Diva."])
    # ---------------- mishap
    o.r('tie_his_feet_in_a_knot_mid_step', 'Tying his own feet in a knot mid-step and hopping round to get them loose with a pop', 22, 'none',
        [k(.12, 'slat_e', x=.3, y=.5, b=.5, l=1), k(.3, 'slat_e', x=.4, y=.8, b=.9, l=1, r=1, eye='O', mark='huh'), k(.5, 'slat_e', x=.5, y=1.1, b=1.3, l=1, r=1, w=.5, eye='@', mark='mrf'), k(.7, x=.2, y=-.5, b=-1.1, w=1, mark='POP'), k(.88, y=.6, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'feet'), prefer=['young', 'grumpy'], say=["Knotted. Left foot did it. I'm not talking to it.", "Untied myself. A little encore of dignity."])
    o.r('skid_along_the_rimed_foot_of_the_case', 'Skidding along the rimed foot of the case in a perfect split and ending flat against the rail', 18, 'none',
        [k(.14, 'slat_d', x=.5, y=.3, b=.5, l=1), k(.3, x=.9, y=-.5, b=-.9, w=1, l=1, r=1, eye='O', mark='WAH'), k(.5, 'rail_l', x=1.4, y=1.9, b=1.8, w=.7, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('slip', 'rime'), when=['rime>.3'], prefer=['young'])
    o.r('spin_too_hard_and_hit_the_case', 'Spinning too hard on the spot and bouncing off the case with a squeak', 16, 'none',
        [k(.14, x=.4, y=-.3, b=-.3, w=.7, l=1), k(.3, x=1.2, y=-.6, b=-.9, w=1, r=1), k(.46, 'slat_b', x=1.5, y=.4, b=1.0, eye='@', mark='oof'), k(.64, x=-1.0, y=-.5, b=-.8, w=.9, l=1, eye='@'), k(.86, x=.1, y=.4, b=.4, eye='-')],
        [], g='mishap', act=('walk_into', 'case'), prefer=['young'])
    o.r('stamp_out_a_missed_step', 'Stamping out a missed step at the rail, three times, until it learns', 14, 'none',
        [k(.14, 'rail_r', x=.2, y=.5, b=.3, l=1), k(.3, 'rail_r', x=.3, y=.6, b=.9, l=1, mark='STOMP'), k(.46, x=-.2, y=-.3, b=-.8, r=1, w=.6), k(.62, 'rail_r', x=.3, y=.6, b=1.0, r=1, mark='STOMP'), k(.8, 'rail_r', x=.3, y=.6, b=1.1, l=1, mark='STOMP'), k(.92, eye='-')],
        [(.62, 'scuff')], g='mishap', act=('stamp', 'step'), prefer=['grumpy'])
    o.r('hook_a_toe_on_the_end_stud_mid_leap', 'Hooking a toe on the end stud mid-leap and limping about on the other foot', 16, 'none',
        [k(.14, 'stud_r', x=.5, y=.5, b=-.5, l=1), k(.3, 'stud_r', x=1.2, y=.4, b=1.0, r=1, eye='O', mark='yoink'), k(.5, x=-.4, y=-.4, b=-1.2, w=.8, l=1, eye='@', mark='OW'), k(.7, x=.2, y=.5, b=.6, r=1, eye='>'), k(.88, eye='-')],
        [], g='mishap', act=('hook', 'stud'), prefer=['young'], say=["Stud 1, toe 0. The stud has been there longer.", "Hopped it off. It was a planned limp."])
    o.r('wrench_a_wing_in_a_flourish_and_shake_it_out', 'Wrenching a wing in a showy flourish and shaking it out with a groan', 18, 'none',
        [k(.14, x=.3, y=-.5, b=-.4, w=.6), k(.3, x=.7, y=-1.0, b=-.8, w=1, l=1, mark='TA-'), k(.46, x=-.3, y=.4, b=.9, w=1, eye='O', mark='ow'), k(.64, x=-.2, y=.5, b=.6, w=.4, r=1), k(.82, x=.1, y=.3, b=.4, w=.8, eye='-')],
        [], g='mishap', act=('shake', 'wing'), prefer=['happy', 'grumpy'])
    # ---------------- duets (a friend takes their own part)
    o.r('waltz_along_the_base_with_a_friend', 'Waltzing along the base with a friend, one forward as the other steps back, slat by slat', 26, 'none',
        [k(.1, 'slat_d', x=.4, y=.3, b=.4, l=1), k(.28, 'slat_a', x=.6, y=-.2, b=-.5, w=.5, r=1), k(.46, 'slat_e', x=.5, y=-.3, b=-.6, w=.6, l=1, mark='one-two-three'), k(.64, 'slat_b', x=.6, y=-.2, b=-.5, w=.5, r=1), k(.84, 'slat_g', x=.4, y=.3, b=.4, eye='^')],
        [(.46, 'mates')], g='play', act=('dance', 'base'), prefer=['happy', 'lonely'],
        duo=[k(.1, 'slat_g', x=-.3, y=.3, b=.4, r=1), k(.28, 'slat_b', x=-.5, y=-.2, b=-.5, w=.5, l=1), k(.46, 'slat_e', x=-.4, y=-.3, b=-.6, w=.6, r=1), k(.64, 'slat_a', x=-.5, y=-.2, b=-.5, w=.5, l=1), k(.84, 'slat_d', x=-.3, y=.3, b=.4, eye='^')],
        say=["Waltzed with a friend. Nobody led. Everybody fell over.", "Slow dance. Faster feelings."])
    o.r('judge_each_others_spins_out_of_ten', 'Taking turns to spin for the other and scoring the spin out of ten with a tap on the rail', 28, 'none',
        [k(.12, x=.2, y=-.3, b=-.2, w=.5), k(.26, x=.8, y=-.7, b=-.8, w=1, l=1), k(.4, x=.2, y=.2, b=.4, eye='-'), k(.54, 'rail_r', x=.4, y=.6, b=.5, r=1, mark='7'), k(.72, 'rail_r', x=.5, y=.7, b=.6, l=1, mark='tk'), k(.88, eye='^')],
        [], g='test', act=('count', 'scores'), prefer=['happy', 'curious'],
        duo=[k(.12, 'rail_l', x=.4, y=.6, b=.5, l=1), k(.26, 'rail_l', x=.4, y=.5, b=.4, mark='tk'), k(.4, x=.8, y=-.7, b=-.8, w=1, r=1), k(.54, x=-.8, y=-.7, b=-.9, w=1, l=1), k(.72, x=.2, y=.2, b=.4, eye='^')],
        say=["Eight. For effort. Minus two for the smirk.", "I gave myself a ten. Friend gave me a look."])
    o.r('lift_the_medal_so_a_friend_can_read_it', 'Lifting the medal out in his bill and holding it still so a friend can read the emblem', 26, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.6, b=.2, mark='hup'), k(.44, 'item', x=1.7, y=-1.7, b=-1.0, w=.5), k(.62, 'item', x=1.8, y=-1.8, b=-1.1, w=.7, eye='^'), k(.78, 'item', x=1.2, y=-.5), k(.9, eye='^')],
        [], g='use', act=('show', 'medal'), ages=GROWN, prefer=['happy'],
        obj=[(.24, dict(hold=0)), (.44, dict(hold=1)), (.68, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.2, x=.3, y=-.3), k(.42, 'slat_b', x=.9, y=.3, b=.5, eye='o'), k(.6, 'slat_b', x=.8, y=-.5, b=.2, eye='O', mark='dance?'), k(.8, x=-.2, y=-.4, w=.4, eye='^')])
    o.r('lead_a_conga_down_the_rail', 'Leading a conga down the bottom rail with a friend hopping after him, kicking on every fourth beat', 26, 'none',
        [k(.1, 'rail_l', x=.5, y=.4, b=-.3, l=1), k(.28, 'rail', x=.5, y=.3, b=-.6, r=1), k(.46, 'rail', x=.6, y=.3, b=-.8, l=1, w=.6, mark='hey'), k(.64, 'rail_r', x=.5, y=.3, b=-.6, r=1), k(.84, 'rail_r', x=.4, y=.4, b=-.3, l=1, eye='^')],
        [], g='play', act=('race', 'conga'), prefer=['happy', 'young'],
        duo=[k(.1, 'rail_l', x=.3, y=.3, b=-.3, r=1), k(.3, 'rail_l', x=.4, y=.3, b=-.5, l=1), k(.5, 'rail', x=.5, y=.3, b=-.7, r=1), k(.7, 'rail', x=.5, y=.3, b=-.7, l=1, w=.6), k(.88, 'rail_r', x=.3, y=.4, b=-.3, eye='^')])
    o.r('sweep_the_breath_mist_off_in_figures_of_eight', 'Wiping the breath mist off the pane in wide figures of eight with a wing, a dance in itself', 20, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.3, b=.3), k(.3, 'sill', reach=1, x=.7, y=-.5, b=-.5, w=.5, l=1), k(.5, 'trim_lo', reach=1, x=.6, y=-.4, b=-.3, w=.4), k(.7, 'sill', reach=1, x=.8, y=-.5, b=-.6, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['happy'])
    o.r('flatten_his_nose_to_the_pane_to_watch_the_emblem', 'Flattening his nose to the pane for a closer look at the emblem and its tiny steps', 18, 'none',
        [k(.14, x=.5, y=-.3, b=.2), k(.32, 'trim_lo', x=1.4, y=-.6, b=.5, eye='O', mark='mmf'), k(.52, 'trim_lo', x=1.5, y=-.7, b=.6, r=1, eye='O'), k(.72, 'trim_lo', x=1.4, y=-.6, b=.5, l=1, eye='>'), k(.88, x=-.3, y=-.2, w=.3, eye='-')],
        [(.32, 'nose')], g='test', act=('press', 'pane'), ages=['duckling', *GROWN], prefer=['curious', 'young'])
    # @@end2
    return done(o)


# @@earth_token
def earth_token():
    # Drawing: a round token with an arc of dots; inside it a small mountain peak (`/\\`, `/  \\/\\`, `/_ _1_ \\`) over a ground line, a stray `x` and `+` outside the ring.
    # What it IS here is the ground: solid, heavy, slow. The acts feel for it, test it, dig at it, stand like it and shift its grit and leaves; nothing is invented on the drawing.
    o = Obj('earth_token', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), grit=(0, 0, 1), leaves=(0, 0, 1), frost=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('grit', 'rate', -.0002, 'always'),
                     ('leaves', 'rate', .002, 'windy'), ('leaves', 'rate', -.0003, 'always'), ('frost', 'rate', .002, 'snow'), ('frost', 'rate', -.002, 'warm')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         kick_up=[('grit', 'add', .4)], tidy=[('grit', 'set', 0)], bare=[('leaves', 'set', 0)], scatter=[('leaves', 'mul', .4)], thaw=[('frost', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         fun=[('need.fun', 'add', 2)], tidyup=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('grit', .3, '.:.:.', 'rail_ll', 'dust'),
                   ('leaves', .3, ';"~;"', 'rail_rr', 'leaf'), ('frost', .3, '*-*-*', 'trim_r', 'frost')],
 anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_c=(0.8190, 0.8961), slat_d=(0.1524, 0.8831), slat_e=(0.3429, 0.9091), slat_g=(0.6286, 0.8831), slat_h=(0.7238, 0.9091), slat_j=(0.2952, 0.8701), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), rail_ll=(0.1714, 0.9351), rail_rr=(0.8571, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), trim_r=(0.7619, 0.8442), sill=(0.3810, 0.8182), plate_lo=(0.1048, 0.8182), seam_lo=(0.5048, 0.7532), trim_hi=(0.4762, 0.8052)))
    # ---------------- care
    o.r('sweep_the_kicked_up_grit_off_the_foot', 'Sweeping the kicked-up grit into a line along the foot of the case with a wing, then off the end', 18, 'wing',
        [k(.1, 'rail_ll', reach=.6, x=.2, y=.9, b=.6), k(.28, 'rail_l', reach=1, x=.5, y=1.3, b=1.0, l=1), k(.48, 'rail', reach=1, x=.5, y=1.4, b=1.1), k(.68, 'rail_r', reach=1, x=.6, y=1.4, b=1.0, r=1), k(.86, 'rail_rr', reach=1, x=.5, y=1.1, b=.7, eye='^')],
        [(.68, 'tidy')], g='care', act=('sweep', 'grit'), when=['grit>.3'], prefer=['grown'], say=["Grit's gone. Nobody will know what I did down here.", "Swept it up. The earth will file a complaint."])
    o.r('scrub_the_nose_prints_with_the_side_of_his_bill', 'Scrubbing the nose prints off the pane with the side of his bill, as hard as he can manage', 20, 'none',
        [k(.12, x=.5, y=-.2, b=.3), k(.3, 'trim_l', x=1.0, y=-.1, b=.8, mark='sqk'), k(.5, 'trim_lo', x=1.2, y=-.3, b=.9, l=1, mark='sqk'), k(.7, 'trim_r', x=1.0, y=-.1, b=.8, r=1, mark='sqk'), k(.88, y=-.2, eye='-')],
        [(.5, 'buff')], g='care', act=('scrub', 'prints'), ages=['duckling', *GROWN], when=['prints>.3'], prefer=['curious'])
    o.r('rub_the_pane_clear_in_one_hard_stroke', 'Huffing once and rubbing the fogged pane clear with the whole wing in one hard stroke', 14, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.4, b=.1), k(.32, 'sill', reach=1, x=.9, y=-.8, b=-.6, w=.5, l=1), k(.52, 'sill', reach=1, x=1.1, y=-.7, b=-.7, w=.6), k(.72, 'trim_lo', reach=1, x=.6, y=-.4, b=-.2, r=1), k(.88, eye='^')],
        [(.52, 'clear')], g='care', act=('polish', 'pane'), when=['fog>.3'], ages=GROWN)
    o.r('buff_the_bottom_rail_with_a_wing', 'Buffing the bottom rail with the flat of a wing, end to end, until the wood shows its grain', 20, 'wing',
        [k(.1, 'rail_rr', reach=.6, x=.3, y=.9, b=.5), k(.3, 'rail_r', reach=1, x=.5, y=1.2, b=.9, r=1), k(.5, 'rail', reach=1, x=.5, y=1.3, b=1.0), k(.7, 'rail_ll', reach=1, x=.5, y=1.2, b=.9, l=1, mark='shff'), k(.88, eye='^')],
        [(.5, 'clean')], g='care', act=('polish', 'rail'), when=['obj_dirt>.3'], prefer=['happy'])
    o.r('shake_the_wet_off_at_the_foot_of_the_case', 'Wiping the rain off the lower pane with a wing then shaking the drops out of his feathers', 20, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.3, y=-.3, b=.3), k(.3, 'trim_lo', reach=1, x=.6, y=-.5, b=.5, l=1), k(.5, 'trim_l', reach=1, x=.5, y=-.4, b=.6), k(.66, x=-.4, y=-.2, b=-.6, w=1, r=1, mark='brrr'), k(.84, x=.2, y=.2, b=.3, eye='-')],
        [(.5, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'], ages=['duckling', *GROWN])
    o.r('shake_the_grit_out_of_his_own_feathers', 'Shaking the grit out of his own feathers after the digging, from his crown to his tail', 18, 'none',
        [k(.12, x=.3, y=.3, b=.4), k(.3, x=.9, y=.5, b=-.6, w=1, l=1, mark='fff'), k(.5, 'rail_l', x=-.9, y=.5, b=-.8, w=1, r=1, mark='fff'), k(.7, x=.6, y=.4, b=-.5, w=.8, l=1), k(.88, x=.1, y=.3, b=.2, eye='^')],
        [(.5, 'tidyup')], g='care', act=('fluff', 'feathers'), when=['grit>.3'], prefer=['grumpy'])
    # ---------------- use
    o.r('press_a_foot_flat_and_feel_for_a_rumble', 'Pressing one foot flat to the ground at the foot of the case, bill down, to feel for a rumble', 20, 'none',
        [k(.14, 'slat_c', x=.4, y=.6, b=.6, l=1), k(.34, 'rail_r', x=.5, y=1.2, b=1.0, l=1, eye='-'), k(.58, 'rail_r', x=.4, y=1.5, b=1.2, l=1, eye='-', mark='...'), k(.8, x=-.2, y=-.5, b=-.3, w=.4, eye='O', mark='huh')],
        [], g='use', act=('test', 'ground'), prefer=['curious'], say=["Nothing. Very still. Suspiciously earth-like.", "No rumble. Just me being heavy."])
    o.r('lift_the_token_and_feel_how_it_drags_him', 'Lifting the token out in his bill and feeling it drag his head down towards the ground', 24, 'none',
        [k(.1, x=.5, y=-.3), k(.24, 'item', x=1.3, y=-.5, b=.3, mark='hup'), k(.42, 'item', x=1.5, y=.9, b=1.2, l=1, r=1, eye='>'), k(.6, 'item', x=1.6, y=1.2, b=1.5, eye='>', mark='hnng'), k(.78, 'item', x=1.2, y=-.4, b=.3), k(.9, eye='-')],
        [], g='use', act=('weigh', 'token'), ages=GROWN, prefer=['grumpy', 'curious'],
        obj=[(.24, dict(hold=0)), (.42, dict(hold=1)), (.66, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        say=["It weighs like a mountain. In fairness, it is one.", "Lifted it. Spine filed a complaint."])
    o.r('carry_the_token_three_slow_steps', 'Carrying the token three slow steps in his bill, one heavy foot at a time, and setting it back', 28, 'none',
        [k(.1, x=.4, y=-.3), k(.2, 'item', x=1.3, y=-.5, b=.3, mark='hup'), k(.36, 'item', x=1.5, y=.5, b=1.0, l=1), k(.5, 'item', x=1.5, y=.6, b=1.1, r=1), k(.64, 'item', x=1.5, y=.5, b=1.0, l=1), k(.8, 'item', x=1.2, y=-.4, b=.3), k(.92, eye='-')],
        [], g='use', act=('carry', 'token'), ages=GROWN, prefer=['grown'],
        obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.68, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))])
    o.r('scrabble_at_the_foot_of_the_case_as_if_digging', 'Scrabbling at the foot of the case with both feet as if he could dig down to the roots', 18, 'none',
        [k(.12, 'rail_l', x=.5, y=1.0, b=.7, l=1), k(.28, 'rail_l', x=.6, y=1.4, b=1.1, l=1, mark='skrt'), k(.44, 'rail_l', x=.6, y=1.4, b=1.2, r=1, mark='skrt'), k(.6, 'rail_l', x=.6, y=1.5, b=1.2, l=1, mark='skrt'), k(.8, x=.2, y=.5, b=.4, eye='-')],
        [(.44, 'kick_up')], g='use', act=('dig', 'base'), prefer=['young', 'curious'])
    o.r('peer_up_the_peak_and_back_down_again', 'Peering up at the peak on the token, then down at his own feet, then up again, comparing', 18, 'none',
        [k(.14, x=.3, y=-.8, b=-.3), k(.32, x=-.5, y=-1.6, b=-.8, eye='O'), k(.5, x=.4, y=1.3, b=.9, eye='-'), k(.68, x=-.6, y=-1.7, b=-.9, eye='O', mark='hm'), k(.86, x=0, y=.1, b=.1, eye='-')],
        [], g='use', act=('peer', 'peak'), prefer=['curious', 'young'])
    o.r('gong_the_left_plate_to_hear_it_ring', 'Banging the left plate on the frame with a wing so it rings like a stone bell', 16, 'wing',
        [k(.14, 'plate_lo', reach=.6, x=.3, y=-.3, b=.2), k(.32, 'plate_lo', reach=1, x=.6, y=-.6, b=-.5, w=.5, mark='BONG'), k(.5, x=-.4, y=-.2, b=.3, eye='O'), k(.68, 'plate_lo', reach=1, x=.6, y=-.6, b=-.6, w=.5, l=1, mark='BONG'), k(.86, eye='^')],
        [], g='use', act=('ring', 'plate'), ages=GROWN, prefer=['grumpy', 'happy'], say=["Rang it. Stone doesn't ring. Metal's lying to me.", "BONG. Again. For the neighbours."])
    # ---------------- play
    o.r('climb_the_slats_one_hard_hop_at_a_time', 'Climbing up the slats like a hillside, one hard hop at a time, bill leading', 20, 'none',
        [k(.1, 'slat_e', x=.5, y=.7, b=.6, l=1), k(.28, 'slat_a', x=.7, y=.2, b=-.9, r=1), k(.46, 'slat_j', x=.8, y=-.2, b=-1.1, l=1, w=.4), k(.66, 'slat_j', x=.9, y=-.4, b=-1.3, r=1, w=.5, mark='hup'), k(.86, x=.2, y=.4, b=.4, eye='^')],
        [(.46, 'fun')], g='play', act=('climb', 'slats'), prefer=['young', 'happy'])
    o.r('bulldoze_a_drift_of_leaves_with_his_chest', 'Bulldozing a drift of leaves along the foot of the case with his chest, head down', 20, 'none',
        [k(.12, 'rail_rr', x=.9, y=1.1, b=.9, l=1), k(.3, 'rail_r', x=1.2, y=1.3, b=1.2, r=1, mark='shrr'), k(.5, 'rail', x=1.3, y=1.4, b=1.3, l=1, mark='shrr'), k(.7, 'rail_l', x=1.2, y=1.3, b=1.2, r=1), k(.88, x=.3, y=.4, b=.4, eye='^')],
        [(.5, 'scatter')], g='play', act=('push', 'leaves'), when=['leaves>.3'], prefer=['happy', 'grumpy'])
    o.r('butt_a_slat_to_see_who_gives_first', 'Butting a slat with the top of his head to see who gives first, twice, getting a lump', 16, 'none',
        [k(.14, 'slat_b', x=.3, y=.5, b=.4), k(.3, 'slat_b', x=1.5, y=.8, b=.9, l=1, mark='BONK'), k(.46, x=-.9, y=-.3, b=-.3, w=.4, eye='@'), k(.62, 'slat_b', x=1.6, y=.9, b=1.0, r=1, mark='BONK'), k(.8, x=-.3, y=.5, b=.5, eye='-')],
        [], g='play', act=('nudge', 'slat'), prefer=['grumpy', 'young'], say=["Slat 2, head 0. Slat's got seniority.", "Gave first. A lump. Nobody tell the slat."])
    o.r('stand_as_one_peak_on_one_foot', 'Standing as one peak on one foot, both wings spread into a point, and holding it for the count', 24, 'none',
        [k(.12, x=.6, y=.8, b=.8), k(.3, x=.8, y=-1.2, b=-1.3, w=1, l=1), k(.52, x=.9, y=-1.6, b=-1.5, w=1, l=1, mark='...'), k(.72, x=.9, y=-1.6, b=-1.5, w=1, l=1, eye='-'), k(.88, y=.5, b=.6, eye='^')],
        [], g='play', act=('balance', 'peak'), prefer=['happy', 'curious'])
    o.r('kick_a_spray_of_grit_down_the_rail', 'Kicking a spray of grit down the rail with alternate feet and watching how far it flies', 16, 'none',
        [k(.12, 'rail_l', x=.3, y=.6, b=.5, l=1), k(.3, 'rail_l', x=.4, y=.8, b=-.4, l=1, w=.5, mark='fsss'), k(.46, 'rail', x=.4, y=.8, b=-.5, r=1, w=.5, mark='fsss'), k(.64, x=.5, y=-.3, b=-.2, w=.4, eye='^'), k(.84, eye='-')],
        [(.3, 'kick_up')], g='play', act=('kick', 'grit'), prefer=['young', 'grumpy'])
    o.r('march_on_the_spot_like_a_mountain_guard', 'Marching in place at the foot of the case, bill high, as if the mountain wanted guarding', 20, 'none',
        [k(.12, x=.4, y=-.4, b=.1, l=1), k(.28, x=.4, y=-.5, b=.3, r=1, mark='hup'), k(.44, x=.4, y=-.5, b=.2, l=1), k(.6, x=.4, y=-.5, b=.3, r=1, mark='hup'), k(.78, x=.3, y=-.6, b=.1, w=.3, eye='>'), k(.9, eye='-')],
        [], g='play', act=('guard', 'peak'), prefer=['grumpy', 'curious'])
    # ---------------- test
    o.r('knock_on_the_slats_to_hear_if_they_are_stone', 'Knocking on three different slats to hear whether any of them is stone, and cocking his head at each', 20, 'none',
        [k(.12, 'slat_d', x=1.2, y=1.0, b=.5, mark='tok'), k(.3, x=-.4, y=-.4, b=-.2, w=.3), k(.44, 'slat_h', x=1.3, y=1.1, b=.6, l=1, mark='tok'), k(.6, x=-.4, y=-.4, b=-.2, w=.3, eye='O'), k(.76, 'slat_c', x=1.3, y=1.1, b=.6, r=1, mark='tok'), k(.9, eye='-')],
        [], g='test', act=('knock', 'slats'), prefer=['curious'], say=["Wood. Wood. Wood. Disappointing consistency.", "Not stone. I'd have felt it in the beak."])
    o.r('put_an_ear_to_the_rail_for_the_deep_hum', 'Laying his ear to the bottom rail and listening for the deep hum the earth is supposed to make', 22, 'none',
        [k(.14, x=.4, y=.5, b=.4), k(.34, 'rail_rr', x=-.3, y=.9, b=1.1, eye='-'), k(.58, 'rail_rr', x=-.4, y=1.0, b=1.3, l=1, eye='-', mark='...'), k(.8, x=.3, y=-.4, b=.1, w=.4, eye='O')],
        [], g='test', act=('listen', 'ground'), prefer=['curious', 'lonely'])
    o.r('lick_the_grit_to_find_out_what_it_is', 'Licking a finger of grit off the rail to find out what kind of earth it is', 16, 'none',
        [k(.14, 'rail_l', x=1.0, y=1.5, b=.9), k(.34, 'rail_l', x=1.2, y=1.7, b=1.1, eye='-', mark='...'), k(.54, x=-.8, y=-.5, b=-.3, w=.7, l=1, eye='>', mark='ptui'), k(.8, y=.5, b=.3, eye='-')],
        [], g='test', act=('taste', 'grit'), when=['grit>.3'], prefer=['curious', 'young'], say=["Grit. Earth. Slightly chicken. Don't ask.", "Tastes like the floor. It is the floor."])
    o.r('sniff_the_token_for_rain_and_roots', 'Lifting the token in his bill to sniff it for rain and roots, then for history', 22, 'none',
        [k(.1, x=.2, y=-.5, b=-.2), k(.25, 'item', x=1.0, y=-.8, b=.5, mark='hup'), k(.44, 'item', x=-.4, y=1.6, b=-.3, eye='-', mark='snf'), k(.6, 'item', x=-.5, y=1.8, b=-.5, l=1, eye='O', mark='snf'), k(.78, 'item', x=1.0, y=-.9, b=.5), k(.9, eye='>')],
        [], g='test', act=('sniff', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.68, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('measure_the_peak_against_himself', 'Standing tall at the glass and measuring the little peak against his own height with a wing', 20, 'wing',
        [k(.14, 'stud_r', reach=.6, x=.2, y=-.3, b=.1), k(.32, 'stud_r', reach=1, x=.2, y=-.9, b=-.7, w=.2), k(.52, 'stud_r', reach=1, x=.3, y=-1.2, b=-1.0, l=1, mark='hm'), k(.74, 'stud_r', reach=.8, x=.1, y=-.4, b=-.3, r=1), k(.88, eye='-')],
        [], g='test', act=('measure', 'peak'), prefer=['curious'])
    o.r('compare_a_footprint_in_the_grit_with_his_own', 'Setting a foot beside a footprint in the grit and comparing size, toe by toe', 18, 'none',
        [k(.14, 'rail', x=.3, y=1.0, b=.8, l=1), k(.34, 'rail', x=.4, y=1.3, b=1.1, l=1, eye='O'), k(.54, 'rail', x=.3, y=1.4, b=1.2, l=1, r=1, mark='hm'), k(.76, x=.2, y=.2, b=.3, eye='>')],
        [], g='test', act=('compare', 'footprints'), when=['grit>.3'], prefer=['curious'])
    # ---------------- rest
    o.r('nap_curled_up_like_a_boulder_against_the_foot', 'Napping curled tight against the foot of the case like a boulder, bill tucked in', 30, 'none',
        [k(.15, 'slat_a', x=-.4, y=.4, b=.6), k(.4, 'slat_a', x=-.8, y=1.4, b=1.8, eye='-'), k(.7, 'slat_a', x=-.8, y=1.6, b=2.0, eye='-', mark='zzz'), k(.9, x=-.2, y=-.2, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'boulder'), when=['tired'], say=["Boulder mode. Do not kick. Do not weigh.", "Asleep. Rolled slightly. Lichen pending."])
    o.r('lean_into_the_end_stud_like_a_wall', 'Leaning his whole weight into the end stud to see which of them is the wall', 20, 'none',
        [k(.14, x=.3, y=.2, b=.3), k(.4, 'stud_l', x=-1.0, y=.4, b=1.4, w=.2), k(.64, 'stud_l', x=-1.2, y=.6, b=1.7, l=1, eye='-', mark='hnn'), k(.86, x=.2, y=.3, b=.4, eye='-')],
        [], g='rest', act=('lean', 'stud'), prefer=['tired', 'grumpy'])
    o.r('sulk_with_a_heavy_back_to_the_world', 'Sulking with a heavy back to the world, bill sunk and wings pinned flat', 24, 'none',
        [k(.14, x=-.9, y=.1, b=.3, l=1), k(.4, 'slat_g', x=-1.5, y=1.0, b=1.4, w=.1, eye='-'), k(.7, 'slat_g', x=-1.7, y=1.2, b=1.5, r=1, eye='-', mark='hmph'), k(.9, x=-.5, y=.4, b=.6)],
        [], g='rest', act=('sulk', 'ground'), when=['sad'], say=["Heavy mood. Dense. Very earthy.", "The ground gets me. It's a low bar."])
    o.r('wait_like_a_rock_with_one_eye_open', 'Waiting at the foot of the case as still as a rock with one eye open for anything moving', 28, 'none',
        [k(.14, x=.2, y=.2, b=.5, eye='o'), k(.4, x=.1, y=.5, b=1.0, eye='-'), k(.62, x=.2, y=.4, b=1.0, eye='o', mark='...'), k(.82, x=.2, y=.3, b=.8, eye='O')],
        [], g='rest', act=('wait', 'rock'), prefer=['curious', 'lonely'])
    o.r('sit_plump_at_the_end_with_his_chin_on_his_chest', 'Sitting plump at the end of the case with his chin pressed to his chest, a small mound of duck', 26, 'none',
        [k(.14, 'stud_r', x=.3, y=.5, b=.7), k(.4, 'stud_r', x=.2, y=1.2, b=1.5, eye='-'), k(.66, 'stud_r', x=.2, y=1.4, b=1.7, eye='-', mark='...'), k(.86, x=.3, y=.4, b=.5, r=1)],
        [], g='rest', act=('sit', 'mound'), prefer=['tired', 'sad'])
    # ---------------- weather
    o.r('sweep_the_blown_leaves_off_the_foot', 'Sweeping the blown leaves off the foot of the case with a wing, a few strokes at a time', 20, 'wing',
        [k(.1, 'rail_rr', reach=.6, x=.3, y=1.0, b=.6), k(.3, 'rail_rr', reach=1, x=.7, y=1.3, b=.9, r=1, mark='shf'), k(.5, 'rail_r', reach=1, x=.7, y=1.4, b=1.0), k(.7, 'rail', reach=1, x=.6, y=1.4, b=1.0, l=1, mark='shf'), k(.88, eye='^')],
        [(.5, 'bare')], g='weather', act=('sweep', 'leaves'), when=['leaves>.3'], prefer=['grown'], say=["Leaves off. Wind will bring them back. We have a thing.", "Swept. The wind took that personally."])
    o.r('scuff_through_the_drifted_leaves_for_the_noise', 'Scuffing through the drifted leaves along the foot of the case for the crunch, there and back', 18, 'none',
        [k(.12, 'rail_rr', x=.4, y=.6, b=.5, l=1), k(.3, 'rail_r', x=.5, y=.5, b=-.5, r=1, w=.4, mark='crnch'), k(.5, 'rail', x=.5, y=.5, b=-.5, l=1, w=.4, mark='crnch'), k(.7, 'rail_r', x=.5, y=.5, b=-.5, r=1, w=.4, mark='crnch'), k(.86, x=.3, y=.4, b=.3, eye='^')],
        [(.5, 'scatter')], g='weather', act=('kick', 'leaves'), when=['leaves>.4'], prefer=['young', 'happy'])
    o.r('scrape_the_frost_off_the_right_trim_with_a_foot', 'Scraping the frost off the right trim bar with the side of a raised foot, ending on one leg', 18, 'wing',
        [k(.12, 'trim_r', reach=.6, x=.3, y=-.2, b=.3), k(.3, 'trim_r', reach=1, x=.6, y=-.5, b=-.2, w=.4, l=1, mark='scrk'), k(.5, 'trim_r', reach=1, x=.6, y=-.5, b=-.3, w=.5, l=1, mark='scrk'), k(.7, 'trim_r', reach=1, x=.4, y=-.4, b=-.2, l=1, r=1), k(.88, eye='-')],
        [(.5, 'thaw')], g='weather', act=('scrape', 'frost'), when=['frost>.3'], ages=['duckling', *GROWN])
    o.r('huddle_into_the_base_and_let_it_storm', 'Huddling hard against the base with his bill buried in his chest while the storm leans on the case', 34, 'none',
        [k(.1, 'slat_h', x=-.2, y=.2, b=.5), k(.24, 'slat_h', x=-.9, y=1.3, b=1.7, l=1, eye='-'), k(.5, 'slat_h', x=-1.1, y=1.6, b=2.0, w=.4, eye='-', mark='boom'), k(.76, 'slat_h', x=-.9, y=1.2, b=1.5, r=1, eye='>'), k(.9, 'slat_h', x=-.3, y=.5, b=.8)],
        [], g='weather', act=('shelter', 'base'), when=['storm', 'wet'])
    o.r('breathe_in_the_wet_wood_smell', 'Breathing in the smell of rain on the wooden base like wet earth, eyes shut, bill lifted', 20, 'none',
        [k(.14, 'slat_e', x=.5, y=.5, b=.4), k(.34, 'slat_e', x=.9, y=1.0, b=.7, eye='-', mark='snnf'), k(.56, x=.3, y=-.7, b=-.4, w=.3, eye='-', mark='ahh'), k(.76, 'slat_e', x=.8, y=.8, b=.6, eye='-', mark='snnf'), k(.9, eye='^')],
        [], g='weather', act=('sniff', 'rain'), when=['obj_wetness>.3'], prefer=['happy', 'curious'])
    # ---------------- show
    o.r('bow_to_the_mountain_with_his_whole_weight', 'Bowing to the mountain with his whole weight, bill almost to the rail, and holding the bow too long', 18, 'none',
        [k(.15, x=-.3, y=-.4, b=-.2), k(.38, 'rail_l', x=1.1, y=1.6, b=1.4, w=.2), k(.6, 'rail_l', x=1.3, y=2.0, b=1.8, w=.2, mark='...'), k(.76, 'rail_l', x=1.2, y=1.8, b=1.6), k(.9, x=-.2, y=-.3, b=-.2, eye='^')],
        [], g='show', act=('bow', 'peak'), prefer=['happy'])
    o.r('present_the_token_to_the_empty_garden', 'Presenting the token to an empty garden, wing sweeping low from left to right like a sunrise', 18, 'wing',
        [k(.14, reach=.2, x=-.3, y=.1, b=.3), k(.34, reach=1, x=.5, y=.5, b=.5, l=1), k(.54, reach=1, x=.8, y=-.2, b=0, mark='behold'), k(.72, reach=1, x=.9, y=-.6, b=-.4, r=1), k(.88, reach=0, y=.3, b=.2, eye='^')],
        [], g='show', act=('present', 'earth'), prefer=['happy'], say=["Behold the ground. You are standing on it.", "Earth, ladies and geese. Sorry. Ducks."])
    o.r('pose_as_a_mountain_with_a_cloud_on_his_head', 'Posing as a mountain with one wing raised over his head like a cloud and his feet planted wide', 22, 'none',
        [k(.14, x=.2, y=.3, b=.5, l=1), k(.38, x=.3, y=-.4, b=1.0, w=.6, l=1, r=1), k(.6, x=.3, y=-.8, b=1.2, w=1, l=1, r=1, mark='...'), k(.8, x=.2, y=-.4, b=.8, w=.4), k(.92, eye='^')],
        [], g='show', act=('pose', 'mountain'), prefer=['happy'])
    o.r('argue_with_the_stone_about_who_is_older', 'Arguing with the little peak about who is older, jabbing at the pane and getting no reply', 20, 'none',
        [k(.14, x=.7, y=.1, b=.4, eye='>'), k(.32, 'trim_lo', x=1.2, y=-.2, b=.7, w=.5, mark='OLDER'), k(.5, x=-.4, y=.5, b=.9, l=1, r=1), k(.68, 'trim_l', x=1.2, y=-.3, b=.8, w=.7, mark='ME!'), k(.88, y=.7, b=.8, eye='-')],
        [], g='show', act=('argue', 'stone'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["I'm older than the rock. In spirit. Spiritually, I'm a boulder.", "Stone never answers. Maybe that is the win."])
    o.r('shout_into_the_pane_for_an_echo', 'Shouting HELLO at the pane to hear whether the mountain sends it back, three times', 14, 'none',
        [k(.14, x=.5, y=-.3, b=-.3), k(.34, 'trim_hi', x=1.7, y=-.6, b=-.9, w=1, mark='HELLO'), k(.52, x=-.7, y=-.4, b=-.3, w=.5, eye='O'), k(.7, 'trim_hi', x=1.8, y=-.6, b=-1.0, w=1, mark='HELLO'), k(.88, eye='-', mark='...')],
        [], g='show', far=True, act=('shout', 'echo'), ages=GROWN, prefer=['lonely', 'grumpy'], say=["No echo. Everyone's out. I checked.", "Hello. Hello. Hel. The mountain's busy."])
    o.r('hum_one_low_note_to_the_peak', 'Humming one very low note to the peak until his whole chest rattles', 22, 'none',
        [k(.14, x=.2, y=.3, b=.4), k(.32, x=.3, y=.6, b=.9, eye='-', mark='mmmm'), k(.52, x=.3, y=.8, b=1.1, l=1, eye='-', mark='MMMM'), k(.72, x=.3, y=.7, b=1.0, r=1, eye='-', mark='mmm'), k(.9, eye='^')],
        [], g='show', act=('sing', 'rumble'), prefer=['sad', 'happy'])
    # ---------------- mishap
    o.r('sink_a_foot_into_the_grit_and_rock_it_free', 'Sinking a foot into the heap of grit and rocking from side to side to work it free', 20, 'none',
        [k(.14, 'rail_l', x=.3, y=.7, b=.7, l=1), k(.32, 'rail_l', x=.4, y=1.0, b=1.2, l=1, r=1, eye='O', mark='huh'), k(.5, 'rail_l', x=.6, y=1.3, b=1.7, l=1, r=1, w=.4, eye='@', mark='mrf'), k(.7, 'rail_l', x=-.3, y=-.4, b=-1.0, w=1, mark='SHLUP'), k(.88, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'grit'), when=['grit>.3'], prefer=['young', 'grumpy'], say=["Ankle-deep in my own mess. Metaphorically also.", "Out. With a noise. Do not mention the noise."])
    o.r('skid_down_the_frosted_slats_on_his_belly', 'Skidding along the frosted foot of the case on his belly, wings out, and fetching up at the stud', 18, 'none',
        [k(.14, 'slat_d', x=.5, y=.4, b=.6, r=1), k(.3, x=1.0, y=-.6, b=-1.0, w=1, l=1, r=1, eye='O', mark='WHEE'), k(.5, 'stud_l', x=1.6, y=1.8, b=2.0, w=.6, eye='@', mark='splat'), k(.8, x=.3, y=.6, b=.7, eye='-')],
        [], g='mishap', act=('slip', 'frost'), when=['frost>.3'], prefer=['young'])
    o.r('back_into_the_base_in_the_dark', 'Backing into the base in the dark, bouncing off with a clunk and an outraged look', 14, 'none',
        [k(.14, x=-.6, y=.3, b=.4, l=1), k(.32, 'slat_g', x=-1.5, y=.5, b=1.1, eye='O', mark='clunk'), k(.5, x=.9, y=-.5, b=-.9, w=.8, r=1, eye='@'), k(.8, x=.2, y=.3, b=.3, eye='>')],
        [], g='mishap', act=('walk_into', 'base'), when=['night'])
    o.r('stamp_to_make_the_ground_answer', 'Stamping to make the ground answer, getting a throbbing foot and nothing else', 16, 'none',
        [k(.14, 'rail', x=.3, y=.5, b=.4, l=1), k(.3, 'rail', x=.3, y=.7, b=1.1, l=1, mark='STOMP'), k(.46, x=-.4, y=-.5, b=-1.0, l=1, w=.7, eye='O', mark='OW'), k(.64, x=.3, y=.6, b=.6, r=1, eye='>'), k(.84, eye='-')],
        [], g='mishap', act=('stamp', 'ground'), prefer=['grumpy'])
    o.r('catch_a_toe_on_the_low_slat_and_hop_it_off', 'Catching a toe on the low slat and hopping round with the foot clutched in both wings', 16, 'none',
        [k(.14, 'slat_e', x=.5, y=.4, b=-.3, r=1), k(.3, 'slat_e', x=1.1, y=.5, b=1.0, l=1, eye='O', mark='yoink'), k(.5, x=-.5, y=-.4, b=-1.3, w=.9, r=1, eye='@', mark='OW'), k(.7, x=.2, y=.6, b=.7, l=1, eye='>'), k(.88, eye='-')],
        [], g='mishap', act=('hook', 'slat'), prefer=['young'])
    o.r('heave_at_the_door_seam_to_make_the_earth_move', 'Heaving at the door seam to make the earth move, and getting the whole case to rattle once', 20, 'none',
        [k(.14, x=.3, y=-.4, b=.3), k(.32, 'seam_lo', x=1.0, y=-.8, b=.9, mark='hnng'), k(.5, 'seam_lo', x=1.2, y=-.9, b=1.2, l=1, mark='RATTLE'), k(.68, x=-.7, y=-.3, b=-.6, w=.7, eye='O'), k(.86, eye='-')],
        [], g='mishap', act=('shake', 'doors'), ages=GROWN, prefer=['grumpy', 'curious'])
    # ---------------- duets (a friend takes their own part)
    o.r('scoop_a_heap_of_grit_together', 'Scooping grit into a heap with a friend, one from each end, until they meet in the middle', 24, 'none',
        [k(.1, 'rail_ll', x=.5, y=1.0, b=.8, l=1), k(.28, 'rail_l', x=.7, y=1.3, b=1.1, r=1, mark='skrt'), k(.46, 'rail', x=.7, y=1.4, b=1.2, l=1, mark='skrt'), k(.66, 'rail', x=.6, y=1.3, b=1.0, r=1), k(.84, x=.2, y=.5, b=.4, eye='^')],
        [(.46, 'kick_up'), (.66, 'mates')], g='play', act=('scoop', 'grit'), prefer=['happy', 'lonely'],
        duo=[k(.1, 'rail_rr', x=.4, y=.9, b=.8, r=1), k(.3, 'rail_r', x=.6, y=1.2, b=1.1, l=1), k(.5, 'rail_r', x=.6, y=1.4, b=1.2, r=1, mark='skrt'), k(.7, 'rail', x=.6, y=1.3, b=1.0, l=1), k(.86, x=.2, y=.5, b=.4, eye='^')],
        say=["Met in the middle. Heap fully built. Neither of us won.", "Two ducks, one mound. Mine has the better side."])
    o.r('one_thumps_the_rail_the_other_listens_at_the_slat', 'Thumping the rail in a slow pattern while a friend listens at the slat for the answer, then swapping', 28, 'none',
        [k(.12, 'rail_r', x=.3, y=.6, b=.5, l=1), k(.26, 'rail_r', x=.3, y=.7, b=1.0, l=1, mark='thm'), k(.4, 'rail_r', x=.3, y=.7, b=1.0, r=1, mark='thm'), k(.58, 'slat_h', x=-.3, y=.9, b=1.0, eye='-'), k(.76, 'slat_h', x=-.4, y=1.0, b=1.2, eye='-', mark='...'), k(.9, eye='^')],
        [], g='test', act=('tap', 'rail'), prefer=['curious', 'happy'],
        duo=[k(.12, 'slat_h', x=-.3, y=.9, b=1.0, eye='-'), k(.26, 'slat_h', x=-.4, y=1.0, b=1.2, eye='o', mark='ssh'), k(.4, 'slat_h', x=-.4, y=1.0, b=1.2, eye='O'), k(.6, 'rail_r', x=.3, y=.6, b=.6, r=1), k(.76, 'rail_r', x=.3, y=.7, b=1.0, l=1, mark='thm')])
    o.r('shoulder_the_foot_of_the_case_side_by_side', 'Putting both shoulders to the foot of the case beside a friend and heaving, twice, to see if the earth moves', 26, 'none',
        [k(.12, 'slat_a', x=.3, y=.3, b=.5), k(.3, 'slat_a', x=1.0, y=.6, b=1.5, l=1, mark='HNNG'), k(.46, x=-.3, y=-.1, b=.4, w=.4), k(.64, 'slat_a', x=1.1, y=.7, b=1.7, r=1, mark='HNNNG'), k(.82, x=-.5, y=.2, b=.5, w=.5, eye='>')],
        [], g='use', act=('push', 'case'), prefer=['grumpy', 'happy'],
        duo=[k(.12, 'slat_j', x=.3, y=.3, b=.5), k(.32, 'slat_j', x=1.0, y=.6, b=1.5, r=1), k(.48, x=-.3, y=-.1, b=.4, w=.4), k(.66, 'slat_j', x=1.1, y=.7, b=1.7, l=1), k(.84, x=-.5, y=.2, b=.5, w=.5, eye='>')],
        say=["Two of us. One case. The case isn't even sweating.", "It moved a bit. That was the friend leaving."])
    o.r('stand_back_to_back_as_twin_peaks', 'Leaning back to back with a friend at the foot of the case, two peaks holding each other up', 24, 'none',
        [k(.14, 'slat_c', x=-.2, y=.2, b=.4, l=1), k(.36, 'slat_c', x=-1.0, y=.5, b=1.4, w=.4, eye='-'), k(.6, 'slat_c', x=-1.1, y=.6, b=1.6, w=.6, r=1, mark='...'), k(.8, x=.2, y=.3, b=.3, eye='^')],
        [], g='rest', act=('lean', 'partner'), prefer=['lonely', 'tired'],
        duo=[k(.14, 'slat_c', x=-.2, y=.2, b=.4, r=1), k(.36, 'slat_c', x=-.9, y=.5, b=1.4, w=.4, eye='-'), k(.6, 'slat_c', x=-1.0, y=.6, b=1.6, w=.6, l=1), k(.8, x=.2, y=.3, b=.3, eye='^')])
    o.r('huff_a_cloud_onto_the_pane_and_peck_a_mountain_in_it', 'Huffing a patch of mist onto the pane and pecking a lopsided mountain into it, twice', 20, 'none',
        [k(.12, 'sill', x=1.2, y=-.4, b=.4, mark='haaa'), k(.3, 'sill', x=1.3, y=-.7, b=.7, l=1, mark='tk'), k(.5, 'trim_l', x=1.3, y=-.5, b=.6, mark='tk'), k(.7, 'sill', x=1.2, y=-.7, b=.7, r=1, mark='tk'), k(.88, eye='^')],
        [(.12, 'huff')], g='use', act=('blow', 'glass'), ages=GROWN, prefer=['happy', 'curious'], say=["Mountain: wonky. Cloud: fine. Gone by tea.", "Drew a mountain in my own breath. Peak artist."])
    o.r('flatten_his_nose_to_the_peak_and_squint', 'Flattening his nose to the pane for a close squint at the peak and the dots round it', 18, 'none',
        [k(.14, x=.4, y=-.3, b=.2), k(.32, 'trim_lo', x=1.4, y=-.7, b=.5, eye='O', mark='mmf'), k(.52, 'trim_lo', x=1.5, y=-.8, b=.7, l=1, eye='>'), k(.7, 'trim_l', x=1.4, y=-.6, b=.5, r=1, eye='O'), k(.88, x=-.2, y=-.2, w=.3, eye='-')],
        [(.32, 'nose')], g='test', act=('press', 'glass'), ages=['duckling', *GROWN], prefer=['curious', 'young'])
    # @@e_end2
    return done(o)


# @@sky_token
def sky_token():
    # Drawing: a round token; inside, a cloud outline (`(   )` arcs), a short wind line (`- = -`), curved wind `.--.` and an arc across the top, a `Z` and a few stray
    # specks outside the ring that I do not name. What it IS here is air: the acts are wind, wings, light and weather, done at the foot of the case and at the glass.
    o = Obj('sky_token', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), glint=(0, 0, 1), rime=(0, 0, 1), gale=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('glint', 'rate', .0025, 'sun'), ('glint', 'rate', -.0008, 'always'),
                     ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm'), ('gale', 'rate', .003, 'windy'), ('gale', 'rate', -.0004, 'always')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         dim=[('glint', 'mul', .2)], thaw=[('rime', 'set', 0)], calm=[('gale', 'set', 0)], stir=[('gale', 'add', .4)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         fun=[('need.fun', 'add', 2)], preen=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('glint', .3, '. * .', 'sill_r', 'glow'),
                   ('rime', .3, '*-*-*', 'trim_l', 'frost'), ('gale', .3, '~ . ~', 'ledge', 'dust')],
anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_c=(0.8190, 0.8961), slat_d=(0.1524, 0.8831), slat_e=(0.3429, 0.9091), slat_f=(0.4381, 0.9221), slat_g=(0.6286, 0.8831), slat_i=(0.9143, 0.8961), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), sill=(0.3810, 0.8182), sill_r=(0.6667, 0.8182), ledge=(0.2857, 0.7922), seam_lo=(0.5048, 0.7532), plate_lo=(0.1048, 0.8182)))
    # ---------------- care
    o.r('wipe_the_mist_up_the_pane_in_tall_streaks', 'Wiping the breath mist up the pane in tall streaks with a wing, like clearing a patch of sky', 18, 'wing',
        [k(.12, 'sill', reach=.6, x=.2, y=-.4, b=.2), k(.3, 'sill', reach=1, x=.5, y=-.7, b=-.2, w=.3, l=1), k(.5, 'trim_lo', reach=1, x=.4, y=-.5, b=.4), k(.7, 'sill_r', reach=1, x=.5, y=-.7, b=-.3, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['grown'], say=["Cleared a little sky. Mine now.", "Mist off. The clouds on the token stayed. Loyal."])
    o.r('scrub_off_the_nose_prints_in_a_zigzag', 'Scrubbing the nose prints off the lower pane in a zigzag, bill down, like a plough', 18, 'none',
        [k(.12, x=.7, y=.3, b=.5), k(.28, 'trim_l', x=1.1, y=.1, b=.9, l=1, mark='sqk'), k(.44, 'trim_lo', x=1.2, y=.5, b=.5, r=1, mark='sqk'), k(.62, 'trim_lo', x=1.2, y=.1, b=.9, l=1, mark='sqk'), k(.8, x=.3, y=-.2, b=.2, eye='-')],
        [(.44, 'buff')], g='care', act=('scrub', 'prints'), ages=['duckling', *GROWN], when=['prints>.3'], prefer=['curious'])
    o.r('mop_the_rain_off_the_lower_pane_with_a_wing', 'Mopping the rain off the lower pane with the flat of a wing, sweeping to one corner and wringing it out', 20, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.3, y=-.3, b=.3), k(.3, 'trim_lo', reach=1, x=.6, y=-.4, b=.5), k(.5, 'trim_l', reach=1, x=.6, y=-.4, b=.6, l=1), k(.7, x=-.5, y=.3, b=-.5, w=1, r=1, mark='wring'), k(.86, eye='-')],
        [(.5, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'], ages=['duckling', *GROWN])
    o.r('blow_the_blown_dust_off_the_ledge', 'Blowing the wind-blown dust off the lowest ledge in one long puff and sneezing at the result', 18, 'none',
        [k(.14, x=.3, y=-.5, b=.2), k(.32, 'ledge', x=1.4, y=-.9, b=.6, mark='fff'), k(.5, 'ledge', x=1.5, y=-1.0, b=.7, w=.3, l=1, mark='FFFF'), k(.66, x=-.8, y=-.3, b=-.6, w=.7, eye='>', mark='choo'), k(.84, eye='-')],
        [(.5, 'calm')], g='care', act=('blow', 'dust'), when=['gale>.3'], ages=GROWN, prefer=['curious'])
    o.r('preen_his_wing_feathers_ready_for_flight', 'Preening his wing feathers one by one at the glass as if a flight were scheduled', 20, 'none',
        [k(.12, x=.4, y=.2, b=.2), k(.3, 'sill', x=.8, y=.4, b=.5, w=.8, l=1, eye='>'), k(.5, 'sill', x=.7, y=.6, b=.6, w=1, eye='-'), k(.7, 'sill', x=.8, y=.4, b=.5, w=.7, r=1, mark='prr'), k(.88, x=.2, y=-.2, b=-.1, w=.4, eye='^')],
        [(.5, 'preen')], g='care', act=('groom', 'wings'), ages=GROWN, prefer=['happy'])
    o.r('rub_the_studs_up_to_a_shine_in_turn', 'Rubbing each end stud up to a shine in turn with the side of his bill, wings out for balance', 18, 'none',
        [k(.12, 'stud_r', x=1.1, y=1.0, b=.8, w=.4), k(.3, 'stud_r', x=.9, y=.8, b=.9, w=.5, r=1, mark='rub'), k(.5, x=-.2, y=-.3, b=-.5, w=.9, l=1), k(.7, 'stud_l', x=1.2, y=1.1, b=.8, w=.4, mark='rub'), k(.88, 'stud_l', x=.8, y=.7, b=.7, w=.4, eye='^')],
        [(.3, 'clean')], g='care', act=('polish', 'studs'), when=['obj_dirt>.3'])
    # ---------------- use
    o.r('hold_the_token_up_high_as_if_flying_it', 'Lifting the token in his bill and holding it up high, wings beating, as if he were flying it', 26, 'none',
        [k(.1, x=.4, y=-.2), k(.22, 'item', x=1.3, y=-.5, b=.2, mark='hup'), k(.4, 'item', x=1.5, y=-1.6, b=-1.2, w=1), k(.58, 'item', x=1.6, y=-1.7, b=-1.3, w=.6, l=1, r=1, eye='^'), k(.76, 'item', x=1.2, y=-.5, b=.2), k(.9, eye='^')],
        [], g='use', act=('lift', 'token'), ages=GROWN, prefer=['happy', 'young'],
        obj=[(.22, dict(hold=0)), (.4, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        say=["Airborne. By proxy. The token did the flying.", "Held it up. Nothing flew. Clouds were embarrassed."])
    o.r('puff_at_the_pane_to_move_the_cloud_along', 'Puffing at the pane to push the little cloud along, then checking if it moved at all', 16, 'none',
        [k(.14, x=.3, y=-.3, b=.2), k(.32, 'trim_lo', x=1.4, y=-.6, b=.5, mark='fuuu'), k(.5, 'trim_l', x=1.4, y=-.6, b=.5, l=1, mark='fuuu'), k(.68, x=-.4, y=-.5, b=-.3, w=.4, eye='O'), k(.86, eye='-')],
        [(.32, 'huff')], g='use', act=('blow', 'cloud'), ages=['duckling', *GROWN], prefer=['curious', 'young'])
    o.r('fan_both_wings_wide_to_catch_the_draught', 'Fanning both wings wide at the foot of the case to catch whatever draught there is', 20, 'none',
        [k(.12, x=.2, y=-.2, b=.1), k(.3, x=.4, y=-.8, b=-.5, w=1), k(.5, x=.5, y=-1.0, b=-.7, w=1, l=1, mark='fwoo'), k(.7, x=.4, y=-.8, b=-.5, w=1, r=1), k(.88, x=.1, y=.2, b=.2, w=.3, eye='-')],
        [], g='use', act=('open', 'wings'), prefer=['windy', 'happy'])
    o.r('blow_across_the_door_seam_for_a_whistle', 'Blowing across the door seam to make it whistle and cocking his head for the note', 16, 'none',
        [k(.14, x=.3, y=-.4, b=.3), k(.32, 'seam_lo', x=1.2, y=-.8, b=.9, mark='fweee'), k(.5, 'seam_lo', x=1.3, y=-.9, b=1.0, l=1, mark='fweeeee'), k(.7, x=-.5, y=-.4, b=-.3, w=.4, eye='O', mark='!'), k(.86, eye='-')],
        [(.5, 'stir')], g='use', act=('blow', 'seam'), ages=GROWN, prefer=['curious', 'happy'], say=["Whistled. Seam did the note. I did the lungs.", "A tune. Well. A hole with an opinion."])
    o.r('chase_the_cloud_with_his_bill_along_the_foot', 'Following the little cloud with his bill, tracking it across the glass from the left end to the right', 20, 'none',
        [k(.12, x=.4, y=-.6, b=-.2), k(.3, 'slat_d', x=.5, y=-1.0, b=-.4, eye='O'), k(.5, 'slat_g', x=.6, y=-1.1, b=-.5, l=1, eye='O'), k(.7, 'slat_i', x=.6, y=-1.0, b=-.4, r=1, eye='>'), k(.88, eye='-')],
        [], g='use', act=('chase', 'cloud'), prefer=['curious', 'young'])
    o.r('peer_into_the_sun_arc_and_regret_it', 'Peering up at the arc across the top of the token until the glare makes him sneeze', 16, 'none',
        [k(.14, x=.3, y=-.9, b=-.3), k(.34, x=-.4, y=-1.6, b=-.7, eye='O'), k(.52, x=-.7, y=-1.9, b=-.9, w=.3, eye='@', mark='ow'), k(.7, x=.3, y=.6, b=.5, eye='>', mark='choo'), k(.88, eye='-')],
        [], g='use', act=('peer', 'sun'), prefer=['curious'])
    o.r('lift_the_token_out_to_the_light', 'Lifting the token out in his bill and tilting it to the light so the cloud seems to drift', 24, 'none',
        [k(.1, x=.2, y=.2), k(.25, 'item', x=1.1, y=-.3, b=.4, mark='hup'), k(.42, 'item', x=1.4, y=-.9, b=.0, l=1), k(.58, 'item', x=1.5, y=-1.0, b=-.1, r=1, eye='O'), k(.76, 'item', x=1.1, y=-.3, b=.4), k(.9, eye='^')],
        [], g='use', act=('tilt', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.25, dict(hold=0)), (.42, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))])
    # ---------------- play
    o.r('hop_flat_out_along_the_slats_beating_both_wings', 'Hopping flat out along the base, a slat to a hop, beating both wings as if about to take off', 18, 'none',
        [k(.1, 'slat_d', x=.6, y=-.2, b=-.3, w=.8, l=1), k(.28, 'slat_a', x=.8, y=-.5, b=-1.0, w=1, r=1), k(.46, 'slat_e', x=.8, y=-.5, b=-1.1, w=1, l=1), k(.64, 'slat_b', x=.8, y=-.5, b=-1.2, w=1, r=1, mark='whff'), k(.84, 'slat_g', x=.4, y=.2, b=.3, w=.3, eye='^')],
        [(.64, 'fun')], g='play', act=('hop', 'slats'), prefer=['young', 'happy'])
    o.r('spin_both_wings_like_a_rotor', 'Spinning on the spot with both wings out like a rotor, hoping to rise an inch', 18, 'none',
        [k(.12, x=.2, y=-.1, b=.2), k(.28, x=1.0, y=-.5, b=-.6, w=1, l=1), k(.46, x=-1.0, y=-.5, b=-.8, w=1, r=1, mark='whirr'), k(.64, x=1.0, y=-.6, b=-1.0, w=1, l=1, r=1), k(.8, x=.2, y=.6, b=.7, eye='@')],
        [], g='play', act=('spin', 'rotor'), prefer=['young', 'happy'])
    o.r('race_the_cloud_shadow_down_the_rail', 'Racing an imaginary cloud shadow down the length of the rail with his wings flat back', 18, 'none',
        [k(.1, 'rail_l', x=.4, y=.2, b=.4, l=1), k(.28, 'rail', x=1.0, y=.1, b=-.4, w=.5, r=1), k(.46, 'rail', x=1.3, y=0, b=-.5, w=.7, l=1, mark='zoom'), k(.66, 'rail_r', x=1.3, y=0, b=-.5, w=.7, r=1), k(.84, 'rail_r', x=.2, y=.5, b=.6, eye='O')],
        [], g='play', act=('race', 'cloud'), prefer=['young', 'happy'])
    o.r('chase_the_glint_up_and_down_the_pane', 'Chasing the sun glint as it jumps about the pane, snapping at it and never landing it', 20, 'none',
        [k(.12, 'sill_r', x=.9, y=-.7, b=.4, l=1), k(.28, 'sill_r', x=1.3, y=-1.0, b=-.3, w=.4, mark='snap'), k(.44, 'trim_lo', x=1.2, y=-.4, b=.2, r=1, mark='snap'), k(.6, 'sill', x=1.3, y=-.9, b=-.3, w=.4, l=1, mark='snap'), k(.8, y=.4, b=.4, eye='@')],
        [(.44, 'fun')], g='play', act=('chase', 'glint'), when=['glint>.3'], ages=GROWN, prefer=['young', 'happy'])
    o.r('snap_at_the_gust_as_it_goes_by', 'Snapping at the gust as it goes past, head whipping left and right, like at a passing fly', 16, 'none',
        [k(.12, x=.6, y=-.3, b=.2), k(.28, x=1.3, y=-.5, b=-.4, w=.5, mark='snap'), k(.44, x=-1.2, y=-.5, b=-.4, w=.5, l=1, mark='snap'), k(.62, x=1.3, y=-.5, b=-.5, w=.6, r=1, mark='snap'), k(.8, x=.3, y=.4, b=.3, eye='@')],
        [], g='play', act=('catch', 'gust'), when=['gale>.3'], prefer=['young', 'curious'])
    o.r('hold_a_plane_on_one_foot_with_wings_flat', 'Holding a plane on one foot at the foot of the case, wings flat out, tipping slowly left and right', 22, 'none',
        [k(.12, x=.4, y=.2, b=.4), k(.3, x=.9, y=-.6, b=-1.0, w=1, l=1), k(.48, x=1.0, y=-.6, b=-1.2, w=1, l=1, mark='nnnn'), k(.66, x=-.9, y=-.6, b=-1.2, w=1, r=1), k(.84, x=.2, y=.6, b=.8, eye='^')],
        [], g='play', act=('balance', 'wings'), prefer=['happy', 'curious'])
    # ---------------- test
    o.r('hold_a_wing_up_to_find_which_way_the_wind_blows', 'Holding one wing up at the foot of the case to find which way the wind is blowing, then the other', 20, 'none',
        [k(.14, x=.2, y=-.3, b=.1), k(.32, x=.5, y=-.8, b=-.4, w=.6, l=1, eye='-'), k(.5, x=-.5, y=-.8, b=-.5, w=.6, r=1, eye='o'), k(.7, x=.4, y=-.6, b=-.3, w=.5, eye='>', mark='hm'), k(.86, eye='-')],
        [], g='test', act=('test', 'wind'), when=['gale>.3'], prefer=['curious'], say=["Wind from the left. Or my left. Or just rude.", "Tested it. Wind: yes. Direction: moody."])
    o.r('measure_how_high_a_hop_gets_him_up_the_stud', 'Measuring how high a hop gets him against the end stud, three tries, each a bit short', 20, 'none',
        [k(.12, 'stud_l', x=.4, y=.4, b=.5), k(.26, 'stud_l', x=.8, y=-.4, b=-1.0, w=.6, l=1), k(.4, 'stud_l', x=.4, y=.5, b=.6), k(.54, 'stud_l', x=.9, y=-.6, b=-1.3, w=.7, r=1, mark='hup'), k(.7, 'stud_l', x=.4, y=.5, b=.7, eye='>'), k(.86, eye='-')],
        [], g='test', act=('measure', 'hop'), prefer=['young', 'curious'])
    o.r('compare_his_wingspan_with_the_cloud', 'Spreading both wings wide to compare his wingspan with the cloud on the token, tip to tip', 20, 'wing',
        [k(.14, 'slat_f', reach=.5, x=.3, y=-.4, b=-.2), k(.34, 'slat_f', reach=1, x=.4, y=-1.0, b=-.6, l=1), k(.54, 'slat_f', reach=1, x=.5, y=-1.2, b=-.8, r=1, mark='hm'), k(.74, 'slat_f', reach=.5, x=.3, y=-.5, b=-.3), k(.88, eye='-')],
        [], g='test', act=('compare', 'wingspan'), prefer=['curious'])
    o.r('sniff_the_air_that_comes_from_the_doors', 'Sniffing along the door seam for the air that comes out of the case, a long suspicious draw', 16, 'none',
        [k(.14, x=.3, y=-.3, b=.2), k(.34, 'seam_lo', x=1.0, y=-.6, b=.6, eye='-', mark='snf'), k(.52, 'seam_lo', x=1.1, y=-.7, b=.7, l=1, eye='O', mark='snf'), k(.72, x=-.4, y=-.3, b=-.2, w=.4, eye='>'), k(.88, eye='-')],
        [], g='test', act=('sniff', 'air'), ages=GROWN, prefer=['curious'])
    o.r('lick_the_pane_to_taste_the_cloud', 'Licking the lower pane to find out what the cloud tastes like, and finding out it is glass', 14, 'none',
        [k(.14, 'trim_l', x=1.0, y=-.3, b=.5), k(.34, 'trim_l', x=1.4, y=-.5, b=.7, eye='-', mark='...'), k(.54, x=-.7, y=-.3, b=-.3, w=.7, l=1, eye='>', mark='bleh'), k(.8, y=.4, b=.3, eye='-')],
        [(.34, 'nose')], g='test', act=('taste', 'cloud'), ages=['duckling', *GROWN], prefer=['curious', 'young'], say=["Cloud: glass. Disappointing, and no cloud.", "Tastes of window. Fluffy on the outside."])
    o.r('listen_to_the_slats_for_the_wind_in_the_base', 'Listening along the slats for any wind in the base, ear to one, then the next, then the next', 22, 'none',
        [k(.12, 'slat_c', x=-.2, y=.7, b=.8, eye='-'), k(.3, 'slat_c', x=-.3, y=.9, b=1.0, eye='-', mark='...'), k(.5, 'slat_g', x=-.3, y=.9, b=1.0, l=1, eye='-'), k(.7, 'slat_i', x=-.3, y=.9, b=1.0, r=1, eye='o', mark='!'), k(.88, x=.2, y=-.3, w=.3, eye='O')],
        [], g='test', act=('listen', 'slats'), prefer=['curious'])
    # ---------------- rest
    o.r('nap_with_his_bill_tipped_up_at_the_pane', 'Napping with his bill tipped up at the pane, dreaming of a long glide that never ends in a wall', 30, 'none',
        [k(.15, x=.2, y=-.4, b=.4), k(.4, 'rail', x=.1, y=-.6, b=1.3, eye='-'), k(.7, 'rail', x=.1, y=-.7, b=1.5, w=.3, eye='-', mark='zzz'), k(.9, x=-.2, y=-.2, w=.4, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'sky'), when=['tired'], say=["Dreamt of height. Woke up at ankle level.", "Flew all night. Landed in the same spot."])
    o.r('lean_on_the_right_stud_and_watch_for_birds', 'Leaning against the right stud with his bill up, watching for birds that do not come', 22, 'none',
        [k(.14, x=.3, y=-.2, b=.3, l=1), k(.4, 'stud_r', x=-.8, y=-.6, b=1.1, w=.3), k(.66, 'stud_r', x=-.9, y=-.8, b=1.3, r=1, eye='o', mark='...'), k(.86, x=.2, y=.2, b=.3)],
        [], g='rest', act=('lean', 'stud'), prefer=['lonely', 'sad'])
    o.r('sulk_because_he_is_grounded', 'Sulking with folded wings because everything with feathers is allowed up except him', 24, 'none',
        [k(.12, x=-.5, y=-.3, b=.8, r=1), k(.36, 'slat_a', x=-1.2, y=.6, b=.7, w=.3, eye='-'), k(.62, 'slat_a', x=-2.0, y=1.5, b=1.8, w=.1, l=1, eye='-', mark='hmph'), k(.84, x=-.7, y=.8, b=.2)],
        [], g='rest', act=('sulk', 'wings'), when=['sad'], say=["Grounded. Has wings. Has opinions about wings.", "Everything flies. Everything, apart from me."])
    o.r('wait_for_a_gust_to_lift_him', 'Waiting with both wings half open for a gust that might lift him off the ground this time', 28, 'none',
        [k(.14, x=.5, y=-.6, b=.6, w=.4), k(.38, x=.8, y=-1.0, b=-.5, w=.8, eye='o'), k(.6, x=.8, y=-1.2, b=-.7, w=1, eye='O', mark='...'), k(.8, x=.4, y=-.4, b=.6, w=.3, eye='-')],
        [], g='rest', act=('wait', 'gust'), prefer=['lonely', 'curious'])
    o.r('sit_and_watch_the_cloud_go_nowhere', 'Sitting with his bill propped up on the rail, watching the little cloud go nowhere, patiently', 26, 'none',
        [k(.14, 'rail_l', x=.3, y=.2, b=.7), k(.4, 'rail_l', x=.2, y=-.5, b=1.2, eye='-'), k(.66, 'rail_l', x=.2, y=-.6, b=1.3, eye='o', mark='...'), k(.86, x=.2, y=.3, b=.5, r=1)],
        [], g='rest', act=('sit', 'rail'), prefer=['sad', 'tired'])
    # ---------------- weather
    o.r('shield_his_eyes_and_dim_the_glint', 'Raising a wing like a visor and tilting it until the glint on the pane drops to a dull gleam', 20, 'wing',
        [k(.12, 'sill_r', reach=.6, x=.2, y=-.5, b=.2), k(.3, 'sill_r', reach=1, x=.4, y=-.9, b=-.3, w=.4, l=1), k(.5, 'sill_r', reach=1, x=.3, y=-.7, b=.3, eye='-'), k(.7, 'sill_r', reach=1, x=.4, y=-.9, b=-.3, r=1), k(.88, eye='^')],
        [(.5, 'dim')], g='weather', act=('hide', 'glint'), when=['glint>.3'], ages=GROWN)
    o.r('brace_into_the_gust_with_his_bill_down', 'Bracing into the gust with his bill down and both feet planted, the dust whirling round him', 22, 'none',
        [k(.12, 'slat_e', x=.3, y=.2, b=.6, w=.2), k(.3, 'slat_e', x=.8, y=.8, b=1.3, w=.4, l=1, mark='shhh'), k(.52, 'slat_e', x=1.0, y=1.0, b=1.6, w=.5, r=1, eye='>'), k(.74, 'slat_e', x=.7, y=.6, b=1.0, w=.3), k(.9, eye='-')],
        [], g='weather', act=('brace', 'gale'), when=['gale>.3'], prefer=['grown'])
    o.r('chip_the_rime_off_the_left_trim', 'Chipping the rime off the left trim bar with the tip of a wing before it spreads', 16, 'wing',
        [k(.12, 'trim_l', reach=.6, x=.2, y=-.3, b=.3), k(.3, 'trim_l', reach=1, x=.5, y=-.5, b=.6, mark='tk'), k(.5, 'trim_l', reach=1, x=.6, y=-.6, b=.5, r=1, mark='tk'), k(.7, 'trim_lo', reach=1, x=.5, y=-.4, b=.4), k(.88, eye='-')],
        [(.5, 'thaw')], g='weather', act=('chip', 'rime'), when=['rime>.3'], ages=['duckling', *GROWN])
    o.r('huddle_close_while_the_storm_wrings_the_sky', 'Huddling close against the foot of the case while the storm wrings the sky out over everything', 34, 'none',
        [k(.1, 'slat_d', x=-.3, y=.3, b=.7, r=1), k(.28, 'slat_d', x=-1.0, y=1.0, b=1.4, w=.5, eye='>'), k(.54, 'slat_a', x=-1.2, y=1.4, b=1.8, w=.2, eye='-', mark='CRACK'), k(.78, 'slat_a', x=-1.0, y=1.1, b=1.5, l=1, eye='>'), k(.9, 'slat_a', x=-.4, y=.4, b=.7)],
        [], g='weather', act=('shelter', 'storm'), when=['storm', 'wet'])
    o.r('follow_a_rain_streak_down_the_pane_with_his_bill', 'Following one rain streak all the way down the pane with his bill, and rooting for it', 18, 'none',
        [k(.12, 'sill', x=.9, y=-.9, b=.1), k(.3, 'sill', x=1.2, y=-.6, b=.4, mark='go'), k(.5, 'trim_lo', x=1.3, y=-.2, b=.6), k(.7, 'trim_lo', x=1.2, y=.1, b=.9, eye='O', mark='yes!'), k(.88, eye='^')],
        [], g='weather', act=('chase', 'streak'), when=['obj_wetness>.3'], ages=GROWN, prefer=['young', 'happy'])
    # ---------------- show
    o.r('bow_to_the_whole_sky_from_a_great_height', 'Bowing to the whole sky from as great a height as a duck can manage, up on his toes first', 18, 'none',
        [k(.12, x=.2, y=-.8, b=-.8, w=.5), k(.32, x=.3, y=-1.3, b=-1.2, w=1, l=1, r=1), k(.52, 'rail_r', x=1.2, y=1.8, b=1.5, w=.6), k(.7, 'rail_r', x=1.3, y=2.0, b=1.7, w=.3, mark='...'), k(.88, x=-.2, y=-.5, b=-.3, eye='^')],
        [], g='show', act=('bow', 'sky'), prefer=['happy'])
    o.r('present_the_token_to_a_passing_cloud', 'Presenting the token to an invisible passing cloud with a wide slow sweep of the wing', 18, 'wing',
        [k(.12, reach=.2, x=-.2, y=-.5, b=-.2), k(.32, reach=.8, x=.4, y=-.9, b=-.5), k(.52, reach=1, x=.8, y=-1.2, b=-.8, w=.4, mark='behold'), k(.72, reach=1, x=.9, y=-1.0, b=-.6, l=1), k(.88, reach=0, y=.2, b=.2, eye='^')],
        [], g='show', act=('present', 'cloud'), prefer=['happy'], say=["Behold the sky. It's on show. Entry free. Seats: ground.", "Presented it to a cloud. It drifted off. Rude. Typical cloud."])
    o.r('pose_mid_flight_with_the_wings_swept_back', 'Posing mid-flight on tiptoe with the wings swept back and his bill into the wind, one foot off', 22, 'none',
        [k(.14, x=.4, y=.3, b=.5, l=1), k(.36, x=.8, y=-.7, b=-1.0, w=.6, l=1), k(.58, x=1.2, y=-1.0, b=-1.4, w=1, l=1, r=1, mark='...'), k(.78, x=1.0, y=-.8, b=-1.1, w=.8, l=1), k(.92, eye='^')],
        [], g='show', act=('pose', 'flight'), prefer=['happy'])
    o.r('argue_with_the_clouds_about_right_of_way', 'Arguing with the little clouds about right of way, wing jabbing up at the pane', 20, 'none',
        [k(.14, x=.8, y=-.3, b=.4, eye='>'), k(.34, 'trim_lo', x=1.4, y=-.8, b=.6, w=.9, mark='MY SKY'), k(.5, x=-.3, y=.4, b=.8, l=1, r=1), k(.7, 'trim_l', x=1.5, y=-.9, b=.7, w=1, mark='MINE!'), k(.88, y=.8, b=.6, eye='-')],
        [], g='show', act=('argue', 'clouds'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["Cloud cut in. I had right of way. And wings, nominally.", "It drifted off mid-sentence. Typical of the sky."])
    o.r('shout_up_for_the_wind_to_come_back', 'Shouting up for the wind to come back, wings flung wide, again and again', 14, 'none',
        [k(.14, x=.3, y=-.6, b=-.3, w=.4), k(.34, x=1.5, y=-2.0, b=-1.4, w=1, mark='WIND!'), k(.58, x=1.6, y=-2.1, b=-1.5, w=1, l=1, mark='WIIIND!'), k(.84, x=-.3, y=.2, eye='-')],
        [], g='show', far=True, act=('shout', 'wind'), prefer=['lonely', 'grumpy'], say=["Come back. I wasn't done with you.", "Called the wind. It's at a better party."])
    o.r('sing_a_breezy_tune_with_a_wing_cupped', 'Singing a breezy little tune up at the token with a wing cupped to his bill and his tail swaying', 22, 'wing',
        [k(.1, reach=.3, x=.5, y=.2, b=.5), k(.28, reach=1, x=.9, y=-.5, b=0, w=.7, l=1, mark='doo'), k(.46, reach=1, x=1.1, y=-1.4, b=-.9, w=.3, mark='DOO'), k(.66, reach=1, x=.7, y=-.3, b=.2, r=1, mark='doo-doo'), k(.86, eye='^')],
        [], g='show', act=('sing', 'breeze'), prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('tangle_his_wings_mid_flap_and_flop', 'Tangling both wings mid-flap and flopping round in a knot until one comes loose with a pop', 22, 'none',
        [k(.14, x=.5, y=-.4, b=-.6, w=1), k(.3, x=.6, y=.3, b=.5, w=.5, l=1, r=1, eye='O', mark='huh'), k(.48, x=.5, y=.9, b=1.2, w=.2, l=1, r=1, eye='@', mark='mrf'), k(.68, x=-.4, y=-.8, b=-1.2, w=1, mark='POP'), k(.86, y=.5, b=.5, eye='-')],
        [], g='mishap', act=('stuck', 'wings'), prefer=['young', 'grumpy'], say=["Wing in wing. A very short flight. Wardrobe-related.", "Free. Mostly. One feather's in witness protection."])
    o.r('skid_on_the_frosty_slats_and_go_nose_first', 'Skidding along the frosty foot of the case and going nose first into the rail', 16, 'none',
        [k(.14, 'slat_i', x=.5, y=.3, b=.5, l=1), k(.3, x=1.2, y=-.4, b=-.8, w=1, l=1, r=1, eye='O', mark='WHEE'), k(.5, 'rail_r', x=1.7, y=1.9, b=1.9, w=.6, eye='@', mark='splat'), k(.8, x=.3, y=.5, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'rime'), when=['rime>.3'], prefer=['young'])
    o.r('look_up_at_the_arc_and_walk_into_the_glass', 'Looking up at the arc on the token and bonking face first against the pane', 14, 'none',
        [k(.14, x=.5, y=-1.0, b=.2), k(.3, x=.7, y=-1.6, b=.5, eye='O'), k(.46, 'trim_l', x=1.6, y=-.7, b=.9, eye='@', mark='bonk'), k(.62, x=-1.0, y=.6, b=-.8, w=.7, eye='@'), k(.84, x=.2, y=.4, b=.3, eye='-')],
        [], g='mishap', act=('walk_into', 'glass'), ages=['duckling', *GROWN], prefer=['curious', 'young'])
    o.r('stamp_a_tantrum_at_the_ground_for_not_letting_go', 'Stamping a tantrum at the rail for refusing to let go of his feet, then trying a second time', 14, 'none',
        [k(.14, 'rail_l', x=.3, y=.4, b=.4, l=1), k(.3, 'rail_l', x=.4, y=.6, b=1.1, l=1, mark='STOMP'), k(.46, x=-.3, y=-.7, b=-1.0, w=1, r=1), k(.64, 'rail_l', x=.4, y=.7, b=1.2, r=1, mark='STOMP'), k(.82, eye='-')],
        [], g='mishap', act=('stamp', 'tantrum'), prefer=['grumpy', 'sad'])
    o.r('launch_off_the_rail_and_land_on_his_beak', 'Launching himself off the rail with a hop and a flap and landing flat on his beak', 16, 'none',
        [k(.14, 'rail', x=.4, y=.3, b=.8), k(.28, x=.9, y=-.7, b=-1.4, w=1, l=1, r=1, mark='HUP'), k(.42, x=1.2, y=-1.0, b=-1.6, w=1, eye='^'), k(.58, x=1.5, y=1.8, b=1.8, w=.6, eye='@', mark='thud'), k(.8, x=.2, y=.6, b=.5, eye='-')],
        [], g='mishap', act=('hop', 'rail'), prefer=['young', 'happy'])
    o.r('catch_a_wing_on_the_plate_and_flap_it_free', 'Catching a wing on the left plate while stretching and flapping it free again with a yelp', 18, 'wing',
        [k(.14, 'plate_lo', reach=.6, x=.3, y=-.3, b=.2), k(.3, 'plate_lo', reach=1, x=.5, y=-.4, b=-.5, w=.8, eye='O', mark='yoink'), k(.5, 'plate_lo', reach=1, x=.2, y=.4, b=.6, l=1, r=1, eye='@', mark='mrf'), k(.7, x=-.7, y=-.6, b=-.9, w=1, mark='PTHWOP'), k(.88, eye='-')],
        [], g='mishap', act=('hook', 'wing'), ages=GROWN, prefer=['grumpy'])
    # ---------------- duets (a friend takes their own part)
    o.r('race_two_cloud_shadows_down_the_rail', 'Racing a friend down the rail, each following a cloud shadow of their own, wings flat back', 22, 'none',
        [k(.1, 'rail_l', x=.3, y=.2, b=.4, l=1), k(.28, 'rail', x=1.1, y=0, b=-.5, w=.6, r=1), k(.46, 'rail', x=1.4, y=-.1, b=-.6, w=.8, l=1, mark='zoom'), k(.66, 'rail_r', x=1.4, y=-.1, b=-.6, w=.8, r=1), k(.84, 'rail_r', x=.2, y=.5, b=.6, eye='O')],
        [(.66, 'mates')], g='play', act=('race', 'shadows'), prefer=['young', 'happy'],
        duo=[k(.1, 'rail_l', x=.2, y=.2, b=.4, r=1), k(.3, 'rail', x=1.0, y=0, b=-.5, w=.6, l=1), k(.5, 'rail', x=1.3, y=-.1, b=-.6, w=.8, r=1), k(.7, 'rail_r', x=1.5, y=-.1, b=-.7, w=.8, l=1), k(.88, 'rail_r', x=.3, y=.4, b=.5, eye='>')],
        say=["Photo finish. We both lost. Cloud shadow won.", "A tie. I'm calling it a win for me."])
    o.r('one_flaps_one_leans_into_the_gust', 'Flapping a gust up for a friend who leans into it with their head down, then swapping places', 26, 'none',
        [k(.12, 'slat_g', x=.3, y=-.3, b=.2), k(.28, 'slat_g', x=.7, y=-.9, b=-.6, w=1, l=1, mark='fwoo'), k(.44, 'slat_g', x=.7, y=-.9, b=-.7, w=1, r=1, mark='fwoo'), k(.6, 'slat_b', x=.9, y=.9, b=1.4, w=.3, eye='>'), k(.78, 'slat_b', x=1.0, y=1.0, b=1.6, w=.4, r=1), k(.9, eye='^')],
        [], g='test', act=('brace', 'partner'), prefer=['happy', 'curious'],
        duo=[k(.12, 'slat_b', x=.9, y=.9, b=1.4, w=.3, eye='>'), k(.28, 'slat_b', x=1.0, y=1.1, b=1.6, w=.3, l=1), k(.44, 'slat_b', x=1.0, y=1.1, b=1.6, w=.4, r=1), k(.6, 'slat_g', x=.7, y=-.9, b=-.6, w=1, mark='fwoo'), k(.78, 'slat_g', x=.7, y=-.9, b=-.7, w=1, l=1)])
    o.r('stretch_wings_back_to_back_to_see_who_spans_more', 'Stretching both wings out back to back with a friend to see who spans more, and cheating by a feather', 24, 'none',
        [k(.14, 'slat_c', x=-.2, y=-.2, b=.2), k(.34, 'slat_c', x=-.4, y=-.8, b=-.5, w=1, eye='>'), k(.54, 'slat_c', x=-.5, y=-1.0, b=-.7, w=1, l=1, mark='hm'), k(.74, 'slat_c', x=-.2, y=-.4, b=-.2, w=.5), k(.88, eye='-')],
        [], g='test', act=('measure', 'spans'), prefer=['curious', 'happy'],
        duo=[k(.14, 'slat_c', x=-.2, y=-.2, b=.2), k(.34, 'slat_c', x=-.4, y=-.8, b=-.5, w=1), k(.54, 'slat_c', x=-.5, y=-1.1, b=-.8, w=1, r=1), k(.74, 'slat_c', x=-.2, y=-.4, b=-.2, w=.5, eye='O'), k(.88, eye='^')])
    o.r('toss_the_hop_to_each_other_and_catch_it', 'Hopping up and flapping to catch a friend as they hop and flap, a game with no ball and a lot of landing', 26, 'none',
        [k(.12, 'slat_a', x=.4, y=.3, b=.6), k(.28, 'slat_a', x=.7, y=-.5, b=-1.1, w=1, l=1), k(.42, 'slat_a', x=.5, y=.2, b=.5), k(.58, 'slat_a', x=.8, y=-.6, b=-1.3, w=1, r=1, mark='hup'), k(.8, 'slat_a', x=.3, y=.4, b=.5, eye='^')],
        [], g='play', act=('hop', 'partner'), prefer=['happy', 'young'],
        duo=[k(.12, 'slat_e', x=.4, y=.3, b=.6), k(.3, 'slat_e', x=.5, y=.2, b=.5), k(.46, 'slat_e', x=.7, y=-.5, b=-1.1, w=1, r=1), k(.62, 'slat_e', x=.5, y=.2, b=.5), k(.8, 'slat_e', x=.7, y=-.6, b=-1.3, w=1, l=1)],
        say=["Hop, catch, hop. We never agreed what the catch was.", "Nobody dropped anything. Because there was nothing."])
    # @@s_end
    return done(o)


# @@water_token
def water_token():
    # Drawing: a round token; inside, a drop outline (`/ \\`, `(   )`, `\`1'`) over a row of waves (`~ ~ ~`), with a few spray quotes (`"`) at the bottom outside the ring.
    # What it IS here is water: ripples, beads, splashes and rain, done with breath, wings and feet at the foot of the case and at the glass. Nothing is drunk or spilled.
    o = Obj('water_token', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), beads=(0, 0, 1), rime=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('beads', 'rate', .002, 'wet'), ('beads', 'rate', -.0008, 'always'),
                     ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         bead=[('beads', 'add', .4)], unbead=[('beads', 'set', 0)], thaw=[('rime', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         fun=[('need.fun', 'add', 2)], tidyup=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('beads', .3, '. o . o', 'sill_r', 'water'), ('rime', .3, '*-*-*', 'trim_l', 'frost')],
anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_c=(0.8190, 0.8961), slat_e=(0.3429, 0.9091), slat_f=(0.4381, 0.9221), slat_g=(0.6286, 0.8831), slat_h=(0.7238, 0.9091), slat_k=(0.5810, 0.9221), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), rail_rr=(0.8571, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), trim_r=(0.7619, 0.8442), sill=(0.3810, 0.8182), sill_r=(0.6667, 0.8182), seam_lo=(0.5048, 0.7532), plate_lo=(0.1048, 0.8182)))
    # ---------------- care
    o.r('wipe_the_beaded_drops_off_the_pane_in_columns', 'Wiping the beaded drops off the pane in neat columns with a wing, top to bottom, left then right', 20, 'wing',
        [k(.1, 'sill_r', reach=.6, x=.2, y=-.4, b=.1), k(.26, 'sill_r', reach=1, x=.6, y=-.5, b=.3, w=.3), k(.44, 'trim_r', reach=1, x=.6, y=-.3, b=.5, l=1), k(.62, 'trim_lo', reach=1, x=.5, y=-.3, b=.6), k(.78, 'trim_l', reach=1, x=.5, y=-.2, b=.5, r=1), k(.9, eye='^')],
        [(.44, 'unbead')], g='care', act=('wipe', 'beads'), when=['beads>.3'], ages=['duckling', *GROWN], prefer=['grown'], say=["Beads off. They'll be back. Water has a long memory.", "Wiped every drop. Counted none. Respect."])
    o.r('dab_the_rain_off_the_glass_dry', 'Dabbing the rain off the glass dry with the tip of a wing, one patch at a time, wringing it between', 22, 'wing',
        [k(.12, 'trim_r', reach=.6, x=.3, y=-.2, b=.4), k(.28, 'trim_r', reach=1, x=.5, y=-.3, b=.7, w=.2, mark='dab'), k(.44, x=-.4, y=.3, b=-.4, w=1, l=1, mark='wring'), k(.6, 'trim_lo', reach=1, x=.5, y=-.3, b=.7, mark='dab'), k(.78, 'trim_l', reach=1, x=.5, y=-.2, b=.6, r=1), k(.9, eye='-')],
        [(.6, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'], ages=['duckling', *GROWN])
    o.r('rub_the_nose_prints_off_with_a_damp_wing', 'Rubbing the nose prints off the pane with the underside of a wing, working inwards from the edges', 18, 'wing',
        [k(.12, 'trim_r', reach=.6, x=.3, y=-.3, b=.3), k(.3, 'trim_r', reach=1, x=.5, y=-.4, b=.5, l=1), k(.5, 'trim_lo', reach=1, x=.5, y=-.4, b=.4, mark='sqk'), k(.7, 'trim_l', reach=1, x=.5, y=-.4, b=.5, r=1), k(.86, eye='-')],
        [(.5, 'buff')], g='care', act=('wipe', 'prints'), ages=['duckling', *GROWN], when=['prints>.3'], prefer=['curious'])
    o.r('clear_the_breath_fog_with_one_spin_of_the_wing', 'Clearing the breath fog with one big circle of the wing, like wiping a bathroom mirror', 16, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.5, b=.2), k(.3, 'sill', reach=1, x=.8, y=-.9, b=-.4, w=.6, l=1), k(.5, 'sill', reach=1, x=1.0, y=-.8, b=-.6, w=.7, r=1), k(.7, 'trim_lo', reach=1, x=.5, y=-.4, b=-.1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], ages=GROWN)
    o.r('polish_the_rail_to_a_waterproof_shine', 'Polishing the bottom rail end to end with a wing until water would roll right off it', 20, 'wing',
        [k(.1, 'rail_rr', reach=.6, x=.2, y=1.0, b=.7), k(.28, 'rail_r', reach=1, x=.5, y=1.3, b=1.0, r=1), k(.46, 'rail', reach=1, x=.5, y=1.4, b=1.1), k(.64, 'rail_l', reach=1, x=.5, y=1.3, b=1.0, l=1, mark='shff'), k(.84, eye='^')],
        [(.46, 'clean')], g='care', act=('polish', 'rail'), when=['obj_dirt>.3'], prefer=['happy'])
    o.r('shake_himself_dry_from_bill_to_tail', 'Shaking himself dry from bill to tail in a spray, the whole duck like a wet dog', 16, 'none',
        [k(.12, x=.3, y=.3, b=.4), k(.3, x=1.0, y=.4, b=-.8, w=1, l=1, mark='brrr'), k(.5, 'rail_l', x=-1.0, y=.4, b=-1.0, w=1, r=1, mark='BRRR'), k(.7, x=.6, y=.3, b=-.6, w=.7, l=1), k(.88, x=.1, y=.2, b=.3, eye='^')],
        [(.5, 'tidyup')], g='care', act=('shake', 'feathers'), when=['obj_wetness>.3'], prefer=['grumpy'], say=["Shook. Sprayed. Nobody saw. Everybody's damp.", "Dry enough. The rest is character."])
    # ---------------- use
    o.r('tilt_the_token_to_watch_the_drop_wobble', 'Lifting the token out in his bill and tilting it slowly from side to side to watch the drop wobble', 24, 'none',
        [k(.1, x=.3, y=-.2), k(.24, 'item', x=1.2, y=-.4, b=.3, mark='hup'), k(.4, 'item', x=1.0, y=-.5, b=-.5, l=1), k(.54, 'item', x=1.6, y=-.5, b=.5, r=1), k(.68, 'item', x=1.0, y=-.5, b=-.5, l=1, eye='O'), k(.8, 'item', x=1.2, y=-.4, b=.3), k(.92, eye='^')],
        [], g='use', act=('tilt', 'token'), ages=GROWN, prefer=['curious'],
        obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.7, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))], say=["Nothing spilled. It's a picture of water. I checked twice.", "Tilted it. The wave stayed polite. Drama-free water."])
    o.r('peer_into_the_drop_for_a_fish', 'Peering into the drop on the token for a fish, then a bigger fish, then at all costs a duck', 18, 'none',
        [k(.14, x=.5, y=-.6, b=-.2), k(.32, x=.9, y=-1.1, b=-.5, eye='o'), k(.5, x=1.1, y=-1.3, b=-.7, eye='O', mark='hm'), k(.7, x=-.2, y=-.8, b=-.3, eye='-'), k(.86, eye='>')],
        [], g='use', act=('peer', 'drop'), prefer=['curious', 'young'])
    o.r('blow_ripples_across_the_fogged_glass', 'Blowing a long breath at the pane so the fog ripples out in rings, then another one', 16, 'none',
        [k(.14, x=.4, y=-.3, b=.2), k(.3, 'sill', x=1.3, y=-.7, b=.5, mark='fooo'), k(.48, 'sill', x=1.4, y=-.8, b=.6, l=1, mark='fooo'), k(.66, x=-.5, y=-.4, b=-.3, w=.4, eye='O'), k(.84, eye='-')],
        [(.3, 'huff')], g='use', act=('blow', 'ripples'), ages=GROWN, prefer=['curious', 'happy'])
    o.r('peck_a_wave_into_the_fog', 'Pecking a row of waves into the fogged pane with the tip of his bill, three humps and a splash', 20, 'none',
        [k(.12, 'sill', x=1.1, y=-.6, b=.5), k(.28, 'sill', x=1.3, y=-.8, b=.2, mark='tk'), k(.44, 'sill_r', x=1.3, y=-.8, b=.4, l=1, mark='tk'), k(.6, 'sill_r', x=1.4, y=-.9, b=.1, r=1, mark='tk'), k(.78, 'sill_r', x=.9, y=-1.0, b=-.3, w=.6, mark='splsh'), k(.9, eye='^')],
        [], g='use', act=('peck', 'waves'), when=['fog>.3'], ages=GROWN, prefer=['happy', 'young'])
    o.r('drum_the_pane_like_a_drop_hitting_water', 'Drumming the lower pane with his bill, slow like a drop and then fast like a downpour', 18, 'none',
        [k(.12, 'trim_lo', x=1.0, y=-.2, b=.3, mark='tk'), k(.3, 'trim_lo', x=1.2, y=-.4, b=.5, mark='tk'), k(.46, 'trim_l', x=1.2, y=-.4, b=.4, l=1, mark='tk tk'), k(.62, 'trim_r', x=1.2, y=-.4, b=.5, r=1, mark='tktktk'), k(.8, 'trim_lo', x=1.0, y=-.2, b=.3, mark='tktktk'), k(.92, eye='-')],
        [], g='use', act=('drum', 'pane'), ages=['duckling', *GROWN], prefer=['young', 'happy'])
    o.r('rock_the_token_like_a_little_boat', 'Rocking the lifted token on its wave like a little boat, bill held steady and the body swaying', 24, 'none',
        [k(.1, x=.2, y=-.1), k(.22, 'item', x=1.1, y=-.3, b=.4, mark='hup'), k(.38, 'item', x=1.2, y=-.4, b=.9, l=1), k(.52, 'item', x=1.2, y=-.4, b=-.3, r=1, eye='-'), k(.66, 'item', x=1.2, y=-.4, b=.9, l=1), k(.8, 'item', x=1.1, y=-.3, b=.4), k(.92, eye='^')],
        [], g='use', act=('rock', 'token'), ages=GROWN, prefer=['happy'],
        obj=[(.22, dict(hold=0)), (.38, dict(hold=1)), (.7, dict(hold=1)), (.82, dict(hold=1)), (.9, dict(hold=0))])
    o.r('count_the_three_waves_with_a_wing', 'Counting the three waves below the drop with the tip of a wing, one humped stroke at a time', 20, 'wing',
        [k(.12, 'sill', reach=.6, x=.3, y=-.5, b=.2), k(.3, 'sill', reach=1, x=.6, y=-.7, b=.4, mark='1'), k(.48, 'sill_r', reach=1, x=.6, y=-.7, b=.4, l=1, mark='2'), k(.66, 'sill_r', reach=1, x=.6, y=-.7, b=.5, r=1, mark='3'), k(.84, eye='-', mark='three')],
        [], g='use', act=('count', 'waves'), ages=['duckling', *GROWN], prefer=['curious'])
    # ---------------- play
    o.r('splash_at_the_foot_of_the_case_with_both_wings', 'Splashing at the foot of the case with both wings as if wading, throwing imaginary spray up the slats', 18, 'none',
        [k(.12, 'slat_e', x=.4, y=.5, b=.5, l=1), k(.28, 'slat_e', x=.8, y=-.4, b=-.7, w=1, l=1, mark='splsh'), k(.44, 'slat_f', x=.8, y=-.4, b=-.8, w=1, r=1, mark='SPLSH'), k(.62, 'slat_g', x=.8, y=-.4, b=-.7, w=1, l=1, mark='splsh'), k(.82, x=.3, y=.4, b=.4, eye='^')],
        [(.44, 'fun')], g='play', act=('splash', 'spray'), prefer=['young', 'happy'])
    o.r('bob_like_a_cork_along_the_rail', 'Bobbing like a cork along the bottom rail, up and down with every imaginary swell', 20, 'none',
        [k(.1, 'rail_l', x=.4, y=.8, b=1.2), k(.26, 'rail_l', x=.6, y=-.8, b=-1.4, w=.3), k(.42, 'rail', x=.4, y=.9, b=1.3), k(.58, 'rail', x=.6, y=-.9, b=-1.5, w=.4, mark='bloop'), k(.74, 'rail_r', x=.4, y=.8, b=1.2), k(.88, x=.3, y=-.5, b=-.6, eye='^')],
        [], g='play', act=('float', 'swell'), prefer=['young', 'happy'])
    o.r('dodge_the_dripping_beads_by_hopping_aside', 'Hopping aside from each drip as the beads run down the pane, left, right, left, never quite fast enough', 20, 'none',
        [k(.12, 'slat_h', x=.3, y=-.3, b=.3), k(.28, 'slat_h', x=.5, y=-.4, b=-.9, w=.5, l=1, mark='hup'), k(.44, 'slat_k', x=.5, y=-.4, b=-.9, w=.5, r=1, mark='hup'), k(.6, 'slat_h', x=.5, y=-.4, b=-.9, w=.5, l=1, eye='O'), k(.78, x=.3, y=.6, b=.7, eye='@')],
        [], g='play', act=('hop', 'drips'), when=['beads>.3'], ages=GROWN, prefer=['young'])
    o.r('race_the_drips_down_the_pane_and_lose', 'Racing two drips down the pane by tracking them with his bill, backing the left one, and losing', 20, 'none',
        [k(.12, 'sill_r', x=.9, y=-.9, b=.1), k(.28, 'sill_r', x=1.2, y=-.6, b=.4, mark='go'), k(.46, 'trim_r', x=1.3, y=-.3, b=.7), k(.64, 'trim_lo', x=1.3, y=.1, b=1.0, eye='O'), k(.82, y=.8, b=.6, eye='-', mark='bah')],
        [], g='play', act=('race', 'drips'), when=['beads>.3'], ages=GROWN, prefer=['grumpy', 'young'], say=["Backed the left one. Right one cheated.", "Lost to a drip. Not my best week."])
    o.r('whirl_into_a_whirlpool_and_stagger_out', 'Whirling on the spot faster and faster like a whirlpool until his own feet drain away and he staggers out', 20, 'none',
        [k(.12, x=.2, y=.1, b=.3), k(.28, x=.9, y=-.3, b=-.6, w=1, l=1), k(.44, x=-1.0, y=-.3, b=-.8, w=1, r=1, mark='glug'), k(.6, x=1.0, y=-.4, b=-.9, w=1, l=1), k(.76, x=-.4, y=.9, b=.9, w=.3, r=1, eye='@'), k(.9, x=.1, y=.3, b=.2, eye='-')],
        [], g='play', act=('spin', 'whirlpool'), prefer=['young', 'happy'])
    o.r('flick_spray_off_his_wingtips_at_the_slats', 'Flicking spray off his wingtips at the slats, wing after wing, as if the case needed a rinse', 16, 'wing',
        [k(.12, 'slat_a', reach=.5, x=.3, y=.5, b=.4), k(.3, 'slat_a', reach=1, x=.6, y=.3, b=-.5, w=.4, l=1, mark='flk'), k(.46, 'slat_b', reach=1, x=.6, y=.3, b=-.5, w=.4, r=1, mark='flk'), k(.64, 'slat_c', reach=1, x=.6, y=.3, b=-.5, w=.4, l=1, mark='flk'), k(.84, eye='^')],
        [], g='play', act=('throw', 'spray'), prefer=['happy', 'grumpy'])
    # ---------------- test
    o.r('lick_a_bead_off_the_glass_to_test_it', 'Licking one bead off the pane to test whether it is rain or just the case sweating', 14, 'none',
        [k(.12, 'trim_r', x=.6, y=.1, b=.9, r=1), k(.3, 'trim_r', x=1.8, y=-.9, b=1.1, eye='-', mark='...'), k(.48, 'trim_r', x=1.9, y=-1.0, b=1.2, w=.3, eye='-'), k(.66, x=-.9, y=.2, b=-.6, w=.9, r=1, eye='O', mark='hm'), k(.86, y=.5, b=.4, eye='-')],
        [(.3, 'nose')], g='test', act=('taste', 'beads'), when=['beads>.3'], ages=['duckling', *GROWN], prefer=['curious', 'young'], say=["Just rain. Rain with notes of window.", "Tastes of nothing. Wet nothing. Refreshing."])
    o.r('sniff_the_token_for_salt_and_sea', 'Lifting the token out in his bill and sniffing it for salt and sea, finding a faint trace of case', 22, 'none',
        [k(.1, x=.4, y=-.6, b=-.1), k(.24, 'item', x=.9, y=-.7, b=.6, mark='hup'), k(.42, 'item', x=1.5, y=.9, b=-.6, eye='-', mark='snf'), k(.58, 'item', x=1.6, y=1.1, b=-.8, l=1, eye='O', mark='snf'), k(.74, 'item', x=.9, y=-.7, b=.6), k(.9, eye='>')],
        [], g='test', act=('sniff', 'token'), ages=GROWN, prefer=['curious'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.64, dict(hold=1)), (.76, dict(hold=1)), (.88, dict(hold=0))])
    o.r('hold_the_token_to_his_ear_like_a_shell', 'Holding the lifted token up to his ear like a shell to hear whether the sea is in there', 24, 'none',
        [k(.1, x=.3, y=-.1, b=.2), k(.24, 'item', x=1.2, y=-.4, b=.5, mark='hup'), k(.42, 'item', x=-.4, y=-.9, b=.9, eye='-'), k(.6, 'item', x=-.5, y=-1.0, b=1.0, l=1, eye='-', mark='shhh'), k(.76, 'item', x=1.0, y=-.4, b=.4, eye='O'), k(.9, eye='^')],
        [], g='test', act=('listen', 'token'), ages=GROWN, prefer=['curious', 'lonely'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        say=["Heard the sea. Or my own head. Same sound.", "It said shhh. Everyone says shhh to me."])
    o.r('measure_the_depth_against_a_slat_with_a_wing', 'Measuring how deep the waves would come up the slats with the length of a wing held flat to each', 20, 'wing',
        [k(.12, 'slat_c', reach=.5, x=.3, y=.4, b=.4), k(.3, 'slat_c', reach=1, x=.5, y=.5, b=.7, l=1), k(.5, 'slat_h', reach=1, x=.5, y=.5, b=.7, mark='hm'), k(.7, 'slat_k', reach=1, x=.5, y=.5, b=.7, r=1), k(.86, eye='-', mark='deep')],
        [], g='test', act=('measure', 'depth'), prefer=['curious'])
    o.r('look_for_his_reflection_ripple_in_the_pane', 'Peering at his own face rippling in the lower pane and pulling faces to see which way it ripples back', 20, 'none',
        [k(.14, x=.5, y=-.3, b=.2), k(.32, 'trim_r', x=1.0, y=-.6, b=.4, eye='O'), k(.5, 'trim_r', x=.6, y=-.5, b=.8, eye='>', mark='hm'), k(.68, 'trim_r', x=1.1, y=-.7, b=.2, w=.5, eye='^'), k(.86, x=.2, y=-.2, eye='-')],
        [], g='test', act=('compare', 'reflection'), ages=['duckling', *GROWN], prefer=['curious', 'happy'])
    o.r('dab_a_toe_at_the_floor_to_test_for_puddles', 'Dabbing a toe at the foot of the case to test whether the floor is wet before committing', 18, 'none',
        [k(.14, 'rail_rr', x=.3, y=.7, b=.5, l=1), k(.32, 'rail_rr', x=.3, y=.9, b=.9, l=1, mark='dab'), k(.5, x=-.4, y=-.2, b=-.6, l=1, eye='>'), k(.68, 'rail_rr', x=.3, y=.9, b=.9, r=1, mark='dab'), k(.86, eye='-')],
        [], g='test', act=('test', 'floor'), when=['obj_wetness>.3'], prefer=['curious', 'young'])
    # ---------------- rest
    o.r('nap_to_the_rhythm_of_the_drips', 'Napping to the rhythm of the drips with his bill against the rail, one eye dripping too', 30, 'none',
        [k(.15, x=.5, y=.4, b=.4), k(.4, 'rail_l', x=.4, y=1.3, b=1.3, eye='-'), k(.7, 'rail_l', x=.4, y=1.5, b=1.5, r=1, eye='-', mark='zzz'), k(.9, x=-.3, y=-.3, w=.3, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'ripples'), when=['tired'], say=["Drip. Drip. Drip. Zzz. Drip.", "Lulled by water. Woke up thinking I was a pond."])
    o.r('lean_on_the_wet_end_stud_and_stare', 'Leaning against the end stud and staring at the wet slats going nowhere', 20, 'none',
        [k(.14, x=.2, y=.2, b=.3, r=1), k(.4, 'stud_l', x=-.9, y=.5, b=1.2, w=.3), k(.66, 'stud_l', x=-1.0, y=.7, b=1.4, l=1, eye='-', mark='...'), k(.86, x=.3, y=.2, b=.3)],
        [], g='rest', act=('lean', 'stud'), prefer=['sad', 'tired'])
    o.r('sulk_under_his_own_small_raincloud', 'Sulking with his head hung low in his own small raincloud of a mood, tail dripping', 24, 'none',
        [k(.14, x=-.6, y=.3, b=.5, l=1), k(.4, 'slat_b', x=-1.1, y=1.1, b=1.2, w=.1, eye='-'), k(.7, 'slat_b', x=-1.3, y=1.3, b=1.4, r=1, eye='-', mark='drip'), k(.9, x=-.4, y=.5, b=.6)],
        [], g='rest', act=('sulk', 'drizzle'), when=['sad'], say=["Tiny raincloud. Personal. Tailored.", "It follows me. It's the closest thing I have to a friend."])
    o.r('wait_for_the_tide_to_come_in', 'Waiting at the foot of the case for the tide to come in, bill pointed at the horizon of the rail', 28, 'none',
        [k(.14, x=.4, y=-.2, b=.3), k(.36, x=.6, y=-.5, b=.6, eye='o'), k(.58, x=.6, y=-.6, b=.8, eye='o', mark='...'), k(.8, x=.4, y=-.2, b=.3, eye='>')],
        [], g='rest', act=('wait', 'tide'), prefer=['lonely', 'curious'])
    o.r('sit_in_a_little_heap_and_listen_to_the_rain', 'Sitting in a little heap at the foot of the case and listening to the rain tap the glass above him', 28, 'none',
        [k(.14, 'slat_f', x=.2, y=.4, b=.8), k(.4, 'slat_f', x=.1, y=-.3, b=1.3, eye='-'), k(.66, 'slat_f', x=.1, y=-.4, b=1.4, eye='o', mark='tk tk'), k(.86, x=.2, y=.2, b=.5, r=1)],
        [], g='rest', act=('sit', 'rain'), when=['obj_wetness>.3'], prefer=['sad', 'tired'])
    # ---------------- weather
    o.r('lick_the_run_of_beads_for_the_rain', 'Following a run of beads down the pane with his tongue-tip for the taste of the rain, one drop after the next', 18, 'none',
        [k(.12, 'sill_r', x=1.1, y=-.8, b=.2), k(.3, 'sill_r', x=1.4, y=-.9, b=.4, mark='slp'), k(.48, 'trim_r', x=1.4, y=-.5, b=.6, eye='-'), k(.66, 'trim_lo', x=1.3, y=-.2, b=.8, eye='-', mark='slp'), k(.84, y=.3, b=.3, eye='^')],
        [], g='weather', act=('chase', 'beads'), when=['beads>.4'], ages=GROWN, prefer=['happy', 'young'])
    o.r('chip_the_rime_off_the_pane_corner', 'Chipping the rime off the left corner of the pane with the tip of a wing, tiny flakes flying', 16, 'wing',
        [k(.12, 'trim_l', reach=.6, x=.2, y=-.3, b=.3), k(.3, 'trim_l', reach=1, x=.5, y=-.4, b=.5, mark='tk'), k(.5, 'plate_lo', reach=1, x=.5, y=-.4, b=.6, l=1, mark='tk'), k(.7, 'trim_l', reach=1, x=.4, y=-.3, b=.4, r=1), k(.88, eye='-')],
        [(.5, 'thaw')], g='weather', act=('chip', 'rime'), when=['rime>.3'], ages=GROWN)
    o.r('huddle_in_against_the_foot_while_the_storm_pours', 'Huddling hard in against the foot of the case with his head down as the storm pours and the glass streams', 34, 'none',
        [k(.1, 'slat_g', x=-.2, y=.5, b=.8, l=1), k(.28, 'slat_g', x=-.8, y=1.1, b=1.4, w=.4, eye='>'), k(.52, 'slat_k', x=-1.0, y=1.4, b=1.8, w=.1, eye='-', mark='SPLAT'), k(.76, 'slat_k', x=-.8, y=1.0, b=1.4, r=1, eye='>'), k(.9, 'slat_k', x=-.3, y=.4, b=.7)],
        [], g='weather', act=('shelter', 'wall'), when=['storm', 'wet'])
    o.r('splash_through_the_wet_at_the_foot_of_the_case', 'Splashing along the wet foot of the case with high knees and wide wings, enjoying every step', 20, 'none',
        [k(.1, 'rail_rr', x=.4, y=.2, b=-.3, l=1), k(.26, 'rail_r', x=.5, y=.2, b=-.9, w=.8, r=1, mark='splsh'), k(.42, 'rail', x=.5, y=.2, b=-1.0, w=.9, l=1, mark='SPLSH'), k(.58, 'rail_l', x=.5, y=.2, b=-.9, w=.8, r=1, mark='splsh'), k(.8, x=.3, y=.5, b=.5, eye='^')],
        [(.42, 'fun')], g='weather', act=('splash', 'wet'), when=['obj_wetness>.3'], prefer=['young', 'happy'])
    o.r('puff_a_cloud_and_watch_it_bead_on_the_cold_glass', 'Puffing a breath cloud at the cold glass and watching it bead and run down into the rail', 18, 'none',
        [k(.12, 'trim_r', x=.9, y=-.5, b=.3), k(.3, 'trim_r', x=1.3, y=-.7, b=.6, mark='haaa'), k(.5, x=-.3, y=-.4, b=-.2, w=.4, eye='O'), k(.7, 'trim_r', x=1.1, y=-.3, b=.5, eye='-'), k(.86, eye='^')],
        [(.3, 'bead')], g='weather', act=('blow', 'beads'), when=['cold'], ages=['duckling', *GROWN], prefer=['curious'])
    # ---------------- show
    o.r('bow_to_the_wave_and_bob_back_up', 'Bowing to the wave, bill almost to the rail, and bobbing back up on the swell like a cork', 16, 'none',
        [k(.14, x=-.7, y=-.5, b=-.9, w=.8, r=1), k(.34, 'rail_r', x=1.1, y=1.3, b=1.2, w=.2), k(.52, 'rail_r', x=1.2, y=1.6, b=1.5, mark='bloop'), k(.7, x=-.4, y=-.8, b=-.8, w=.7, l=1), k(.88, eye='^')],
        [], g='show', act=('bow', 'wave'), prefer=['happy'])
    o.r('present_the_token_to_the_dry_land', 'Presenting the token to the dry land with a long wing sweep, as if announcing a very small ocean', 18, 'wing',
        [k(.12, reach=.3, x=.5, y=-.2, b=.3, l=1), k(.3, reach=.8, x=.9, y=.3, b=.7), k(.5, reach=1, x=1.1, y=.5, b=.9, w=.3, mark='behold'), k(.7, reach=1, x=.8, y=-.3, b=.3, r=1), k(.88, reach=0, y=.2, b=.2, eye='^')],
        [], g='show', act=('present', 'ocean'), prefer=['happy'], say=["An ocean. Small. Pocket-sized. Ocean-adjacent.", "Presented the sea to a patch of floor. Floor unmoved."])
    o.r('pose_as_a_breaking_wave_one_wing_curled_over', 'Posing as a breaking wave with one wing curled over his head and his chest thrust out to the foam', 22, 'none',
        [k(.14, x=.3, y=.2, b=.7), k(.36, x=.8, y=-.5, b=.2, w=.5, r=1), k(.58, x=1.0, y=-1.0, b=-.6, w=1, r=1, mark='...'), k(.78, x=.9, y=-.7, b=-.3, w=.9), k(.92, eye='^')],
        [], g='show', act=('pose', 'wave'), prefer=['happy'])
    o.r('argue_with_the_tide_about_who_is_in_charge', 'Arguing with the tide about who is in charge of the case, wing jabbing at the drop', 20, 'none',
        [k(.14, x=.9, y=.3, b=.5, eye='>'), k(.32, 'trim_r', x=1.1, y=-.4, b=.8, w=.7, mark='MINE'), k(.5, x=-.5, y=.5, b=1.0, l=1, r=1), k(.68, 'trim_r', x=1.2, y=-.5, b=.9, w=1, mark='ME!'), k(.88, y=.8, b=.7, eye='-')],
        [], g='show', act=('argue', 'tide'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["The tide went out mid-argument. Cowardly. Wet. Cowardly.", "I win. Water has no counter-argument. It just drips."])
    o.r('shout_for_the_sea_to_come_out_and_fight', 'Shouting for the sea to come out and fight, wings flung back, at the top of his lungs', 14, 'none',
        [k(.14, x=.5, y=-.5, b=-.4), k(.34, x=1.5, y=-1.8, b=-1.2, w=1, mark='SEA!'), k(.58, x=1.7, y=-2.0, b=-1.4, w=1, l=1, mark='OI SEA!'), k(.84, x=-.3, y=.3, eye='-')],
        [], g='show', far=True, act=('shout', 'sea'), prefer=['grumpy', 'lonely'], say=["The sea declined. Weak showing.", "Challenged an ocean. It sent a drip."])
    o.r('sing_a_sea_shanty_to_the_token', 'Singing a sea shanty at the token with one wing on his heart, swaying like a boat in a heavy swell', 24, 'wing',
        [k(.1, reach=.2, x=.2, y=.2, b=.6), k(.26, reach=1, x=.5, y=-.4, b=.9, w=.3, l=1, mark='yo-ho'), k(.42, reach=1, x=.6, y=-.5, b=-.2, w=.4, mark='YO-HO'), k(.6, reach=1, x=.5, y=-.4, b=.9, w=.3, r=1, mark='yo-ho'), k(.78, reach=.8, x=.4, y=-.5, b=-.3, w=.4), k(.9, eye='^')],
        [], g='show', act=('sing', 'shanty'), prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('wedge_his_bill_in_the_seam_and_pull_out_with_a_pop', 'Pushing his bill through the door seam to look for water and pulling it out again with a pop', 22, 'none',
        [k(.14, x=.4, y=-.5, b=.3), k(.32, 'seam_lo', x=1.3, y=-.7, b=.7, mark='mmf'), k(.5, 'seam_lo', x=1.5, y=-.8, b=.9, l=1, eye='@', mark='mrf'), k(.68, 'seam_lo', x=1.7, y=-.9, b=1.1, r=1, w=1, mark='POP'), k(.86, x=-1.0, y=.6, b=.7, eye='@')],
        [], g='mishap', act=('stuck', 'seam'), shown='head', ages=GROWN, prefer=['curious', 'grumpy'], say=["Stuck by the beak. Beak's very stubborn. So am I.", "Popped out. Seam kept some of my dignity."])
    o.r('slip_on_the_wet_foot_of_the_case_and_slide_off', 'Slipping on the wet foot of the case and sliding the whole length of it on his belly', 18, 'none',
        [k(.14, 'slat_a', x=.4, y=.3, b=.5, l=1), k(.3, x=1.1, y=-.6, b=-1.1, w=1, l=1, r=1, eye='O', mark='WHOA'), k(.5, 'rail_r', x=1.7, y=2.0, b=2.1, w=.6, eye='@', mark='splat'), k(.8, x=.3, y=.6, b=.7, eye='-')],
        [], g='mishap', act=('slip', 'wetness'), when=['obj_wetness>.3'], prefer=['young'])
    o.r('back_into_the_door_in_the_dark_and_go_clunk', 'Backing into the doors in the dark and going clunk, then clunk again turning round', 14, 'none',
        [k(.14, x=-.6, y=.3, b=.3, r=1), k(.3, 'slat_b', x=-1.4, y=.5, b=1.2, eye='O', mark='clunk'), k(.46, x=.9, y=-.4, b=-.7, w=.7, l=1, eye='@'), k(.62, 'slat_e', x=-1.5, y=.5, b=1.2, eye='@', mark='clunk'), k(.84, x=.2, y=.3, b=.4, eye='>')],
        [], g='mishap', act=('walk_into', 'doors'), when=['night'])
    o.r('stamp_a_puddle_that_is_only_the_floor', 'Stamping a puddle that turns out to be only the floor and hurting a foot proving it', 16, 'none',
        [k(.14, 'rail_l', x=.3, y=.4, b=.4, r=1), k(.3, 'rail_l', x=.3, y=.7, b=1.2, r=1, mark='SPLSH'), k(.46, x=-.5, y=-.6, b=-1.1, r=1, w=.7, eye='O', mark='OW'), k(.64, x=.3, y=.6, b=.7, l=1, eye='>'), k(.84, eye='-')],
        [], g='mishap', act=('stamp', 'puddle'), prefer=['young', 'grumpy'])
    o.r('hook_a_foot_in_the_rail_and_hop_it_out_of_the_wet', 'Hooking a foot round the rail by accident and hauling it loose in a spray', 18, 'none',
        [k(.12, 'rail_rr', x=.8, y=.9, b=-.5, r=1), k(.28, 'rail_rr', x=1.4, y=1.3, b=1.4, l=1, r=1, eye='O', mark='yoink'), k(.46, 'rail_rr', x=.2, y=.5, b=.4, l=1, w=.7, eye='@', mark='SPRAY'), k(.64, x=-.9, y=-.8, b=-1.0, w=1, r=1, eye='>', mark='OW'), k(.84, x=.1, y=.4, b=.5, eye='-')],
        [], g='mishap', act=('hook', 'rail'), prefer=['young'])
    o.r('jump_back_from_a_drip_that_lands_on_his_head', 'Jumping three steps back when a drip lands on his head, then glaring at the pane about it', 16, 'none',
        [k(.14, 'slat_h', x=.3, y=.4, b=.4), k(.3, 'slat_h', x=-.6, y=-.6, b=-1.1, w=.8, l=1, eye='O', mark='EEP'), k(.46, x=-.9, y=-.8, b=-1.3, w=1, r=1, eye='@'), k(.66, 'stud_r', x=.9, y=.5, b=.8, l=1, eye='>', mark='huh'), k(.86, eye='-')],
        [], g='mishap', act=('hop', 'drip'), when=['beads>.3'], prefer=['young', 'curious'])
    # ---------------- duets (a friend takes their own part)
    o.r('splash_fight_with_a_friend_at_the_foot', 'Splashing it out with a friend at the foot of the case, one wing-load of imaginary spray at a time', 24, 'none',
        [k(.1, 'slat_a', x=.4, y=.3, b=.4, l=1), k(.26, 'slat_a', x=.9, y=-.5, b=-.8, w=1, l=1, mark='SPLSH'), k(.44, x=-.5, y=.4, b=.7, w=.4, eye='O'), k(.6, 'slat_b', x=.9, y=-.5, b=-.9, w=1, r=1, mark='SPLSH'), k(.8, x=.3, y=.4, b=.4, eye='^')],
        [(.6, 'mates')], g='play', act=('splash', 'partner'), prefer=['happy', 'young'],
        duo=[k(.1, 'slat_h', x=.4, y=.3, b=.4, r=1), k(.3, x=-.5, y=.4, b=.7, w=.4, eye='O'), k(.46, 'slat_h', x=.9, y=-.5, b=-.8, w=1, r=1, mark='SPLSH'), k(.64, x=-.5, y=.4, b=.7, w=.4), k(.82, 'slat_h', x=.8, y=-.5, b=-.9, w=1, l=1, eye='^')],
        say=["Soaked. Neither of us is even wet. Fully committed.", "He splashed first. I splashed harder. Honour restored."])
    o.r('bob_in_turn_like_two_corks', 'Bobbing up and down in turn with a friend along the rail, one rising as the other sinks, like two corks', 24, 'none',
        [k(.1, 'rail_l', x=.4, y=.7, b=1.1), k(.26, 'rail_l', x=.5, y=-.7, b=-1.3, w=.3), k(.42, 'rail_l', x=.4, y=.8, b=1.2), k(.58, 'rail_l', x=.5, y=-.8, b=-1.4, w=.4, mark='bloop'), k(.78, x=.3, y=-.2, b=-.3, eye='^')],
        [], g='use', act=('float', 'partner'), prefer=['happy', 'lonely'],
        duo=[k(.1, 'rail_r', x=.5, y=-.8, b=-1.4, w=.3), k(.26, 'rail_r', x=.4, y=.8, b=1.2), k(.42, 'rail_r', x=.5, y=-.7, b=-1.3, w=.4), k(.58, 'rail_r', x=.4, y=.8, b=1.2), k(.78, x=.3, y=-.2, b=-.3, eye='^')])
    o.r('dry_the_pane_from_both_ends_until_they_meet', 'Drying the pane from opposite ends with a friend, wings sweeping in until they meet in the middle', 24, 'wing',
        [k(.1, 'trim_r', reach=.6, x=.3, y=-.3, b=.4), k(.28, 'trim_r', reach=1, x=.5, y=-.4, b=.6, l=1), k(.46, 'trim_lo', reach=1, x=.5, y=-.4, b=.6), k(.64, 'trim_lo', reach=1, x=.4, y=-.3, b=.5, r=1, mark='hello'), k(.84, eye='^')],
        [(.46, 'dry')], g='care', act=('dry', 'pane'), when=['obj_wetness>.3'], ages=['duckling', *GROWN], prefer=['happy'],
        duo=[k(.1, 'trim_l', reach=.6, x=.3, y=-.3, b=.4), k(.3, 'trim_l', reach=1, x=.5, y=-.4, b=.6, r=1), k(.48, 'trim_lo', reach=1, x=.5, y=-.4, b=.6), k(.66, 'trim_lo', reach=1, x=.4, y=-.3, b=.5, l=1), k(.84, eye='^')])
    o.r('lift_the_token_so_a_friend_can_hear_the_sea', 'Lifting the token out and holding it low so a friend can put an ear to it and listen for the sea', 26, 'none',
        [k(.1, x=.3, y=-.1, b=.2), k(.24, 'item', x=1.2, y=-.4, b=.5, mark='hup'), k(.42, 'item', x=1.5, y=.4, b=1.0, eye='-'), k(.62, 'item', x=1.6, y=.5, b=1.1, l=1, eye='^'), k(.78, 'item', x=1.1, y=-.3, b=.4), k(.9, eye='^')],
        [], g='use', act=('show', 'token'), ages=GROWN, prefer=['happy', 'lonely'],
        obj=[(.24, dict(hold=0)), (.42, dict(hold=1)), (.68, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.2, x=.3, y=-.3), k(.44, 'slat_b', x=-.4, y=.6, b=.9, eye='-'), k(.62, 'slat_b', x=-.5, y=.7, b=1.0, eye='O', mark='shhh'), k(.8, x=-.2, y=-.4, w=.4, eye='^')],
        say=["Friend heard the sea. Friend heard me breathing. Same noise.", "Held it low. They said waves. I said bread."])
    # @@w_end
    return done(o)


# @@magpie_friendship_charm
def magpie_friendship_charm():
    # Drawing: a cord loop with a knot (`( ... )`, `.-||`) above a pendant ring; in the ring a magpie: head `(o)` with a beak `>=`, a wavy tail `~~~`, a body `_/` and feet `/\\`.
    # The cord hangs 119-146 px up, past every age but a twig, so it is never touched. What it IS here is a friendship with a magpie: greetings, calls and answers, head tilts,
    # being company; no magpie arrives and nothing is given. `bond` is how warm the friendship feels (slow), and the acts that deepen it gate the ones that lean on it.
    o = Obj('magpie_friendship_charm', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), bond=(.5, 0, 1), shine=(0, 0, 1), rime=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('bond', 'rate', -.0004, 'always'),
                     ('shine', 'rate', .0025, 'sun'), ('shine', 'rate', -.0008, 'always'), ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         warm=[('bond', 'add', .3)], dim=[('shine', 'mul', .2)], thaw=[('rime', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         fun=[('need.fun', 'add', 2)], tidyup=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 3)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('bond', .8, '* . *', 'trim_hi', 'glow'),
                   ('shine', .3, '. * .', 'sill_r', 'glow'), ('rime', .3, '*-*-*', 'trim_l', 'frost')],
anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_d=(0.1524, 0.8831), slat_e=(0.3429, 0.9091), slat_g=(0.6286, 0.8831), slat_h=(0.7238, 0.9091), slat_i=(0.9143, 0.8961), slat_l=(0.7714, 0.8701), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), rail_ll=(0.1714, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), trim_r=(0.7619, 0.8442), sill=(0.3810, 0.8182), sill_r=(0.6667, 0.8182), trim_hi=(0.4762, 0.8052), ledge=(0.2857, 0.7922), seam_lo=(0.5048, 0.7532), plate_lo=(0.1048, 0.8182)))
    # ---------------- care
    o.r('clear_the_breath_off_the_pane_around_the_pendant', 'Clearing the breath mist off the pane round the pendant with a wing, careful of the little bird', 18, 'wing',
        [k(.12, 'sill', reach=.6, x=.2, y=-.4, b=.3), k(.3, 'sill', reach=1, x=.4, y=-.6, b=.2, w=.2, l=1), k(.5, 'sill_r', reach=1, x=.5, y=-.6, b=.1), k(.7, 'trim_lo', reach=1, x=.4, y=-.4, b=.4, r=1), k(.88, eye='^')],
        [(.5, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['happy'], say=["Cleared round the bird. It looked pleased. It's a pendant.", "Fog off. Beak showing. Magpie: unimpressed, forever."])
    o.r('scrub_the_prints_off_in_two_tidy_rows', 'Scrubbing the nose prints off in two tidy rows with the side of his bill, the way a friend would', 20, 'none',
        [k(.12, x=.6, y=.2, b=.5), k(.28, 'trim_l', x=1.0, y=.2, b=.9, mark='sqk'), k(.44, 'trim_lo', x=1.1, y=.2, b=.9, l=1, mark='sqk'), k(.6, 'trim_r', x=1.0, y=.2, b=.9, r=1, mark='sqk'), k(.78, y=-.2, b=.2, eye='-')],
        [(.44, 'buff')], g='care', act=('scrub', 'prints'), ages=['duckling', *GROWN], when=['prints>.3'], prefer=['curious'])
    o.r('blot_the_wet_off_the_pane_with_a_tucked_wing', 'Blotting the wet off the pane with a tucked wing so the magpie does not catch cold', 20, 'wing',
        [k(.12, 'trim_r', reach=.6, x=.3, y=-.3, b=.3), k(.3, 'trim_r', reach=1, x=.4, y=-.4, b=.6, mark='blot'), k(.48, 'trim_lo', reach=1, x=.4, y=-.4, b=.7, l=1), k(.66, 'trim_l', reach=1, x=.4, y=-.3, b=.6, r=1, mark='blot'), k(.86, eye='-')],
        [(.48, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'], ages=['duckling', *GROWN])
    o.r('shine_the_end_studs_for_a_visitor', 'Shining the end studs for a visitor, bill and spit and a good deal of squeaking', 18, 'none',
        [k(.12, 'stud_l', x=1.0, y=1.1, b=.7, mark='rub'), k(.3, 'stud_l', x=.8, y=.9, b=.9, l=1, mark='sqk'), k(.5, x=-.3, y=-.3, b=-.4, w=.6, r=1), k(.7, 'stud_r', x=1.1, y=1.1, b=.8, mark='rub'), k(.88, 'stud_r', x=.8, y=.9, b=.7, r=1, eye='^')],
        [(.7, 'clean')], g='care', act=('polish', 'studs'), when=['obj_dirt>.3'], prefer=['happy'])
    o.r('smarten_himself_up_for_the_magpie', 'Smartening himself up for the magpie, a feather smoothed at a time and a last look at the glass', 20, 'none',
        [k(.12, x=.5, y=.3, b=.3), k(.3, 'sill', x=.9, y=.3, b=.6, w=.7, l=1, eye='>'), k(.5, 'sill', x=.7, y=.6, b=.7, w=.9, eye='-'), k(.7, 'sill', x=.9, y=.3, b=.5, w=.6, r=1, eye='^', mark='hm'), k(.88, eye='^')],
        [(.5, 'tidyup')], g='care', act=('groom', 'feathers'), prefer=['happy', 'curious'])
    o.r('sweep_the_ledge_clean_with_a_twig_like_a_nest', 'Sweeping the lowest ledge clean with a twig as if tidying a nest ready for company', 20, 'twig',
        [k(.12, 'ledge', reach=.6, x=.3, y=.1, b=.2), k(.3, 'ledge', reach=1, x=.6, y=.3, b=.4, mark='shff'), k(.5, 'ledge', reach=1, x=.6, y=.3, b=.5, l=1), k(.7, 'trim_hi', reach=1, x=.5, y=.2, b=.3), k(.88, eye='^')],
        [(.5, 'clean')], g='care', act=('sweep', 'ledge'), when=['obj_dirt>.3'], ages=GROWN)
    # ---------------- use
    o.r('hold_the_charm_out_eye_to_eye', 'Lifting the charm out in his bill and holding it out at bill length, eye to eye with the magpie', 26, 'none',
        [k(.1, x=.4, y=-.2), k(.24, 'item', x=1.3, y=-.4, b=.3, mark='hup'), k(.42, 'item', x=1.6, y=-.2, b=.4, eye='O'), k(.62, 'item', x=1.7, y=-.1, b=.5, l=1, eye='^', mark='hello'), k(.78, 'item', x=1.2, y=-.4, b=.3), k(.9, eye='^')],
        [(.62, 'warm')], g='use', act=('show', 'charm'), ages=GROWN, prefer=['happy', 'lonely'], obj=[(.24, dict(hold=0)), (.42, dict(hold=1)), (.68, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))],
        say=["Eye to eye. It blinked first. Pendants cheat.", "Said hello. It said nothing. Best conversation this week."])
    o.r('listen_at_the_charm_for_chatter', 'Holding the lifted charm to his ear to listen for the magpie chatter, then chattering back', 24, 'none',
        [k(.1, x=.3, y=-.1, b=.2), k(.24, 'item', x=1.2, y=-.4, b=.5, mark='hup'), k(.42, 'item', x=-.4, y=-.8, b=.8, eye='-'), k(.58, 'item', x=-.5, y=-.9, b=.9, l=1, eye='O', mark='chak'), k(.74, 'item', x=1.4, y=-.5, b=.4, w=.3, mark='chak-chak'), k(.9, eye='^')],
        [], g='use', act=('listen', 'charm'), ages=GROWN, prefer=['lonely', 'curious'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.68, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=0))])
    o.r('tap_the_pane_twice_and_wait_for_two_back', 'Tapping the pane twice with his bill and waiting for two taps back, like a call and an answer', 22, 'none',
        [k(.12, 'trim_lo', x=1.0, y=-.3, b=.4, mark='tk tk'), k(.28, x=-.2, y=-.4, b=-.2, eye='o'), k(.44, x=-.2, y=-.5, b=-.3, eye='O', mark='...'), k(.6, 'trim_r', x=1.1, y=-.3, b=.5, l=1, mark='tk tk'), k(.8, x=.1, y=-.3, eye='^')],
        [(.6, 'warm')], g='use', act=('tap', 'pane'), ages=['duckling', *GROWN], when=['bond<.7'], prefer=['lonely'], say=["Two taps. Silence. Magpie's playing it cool.", "Waited. Got nothing. Still counts as a conversation."])
    o.r('count_the_tail_waves_with_a_wing_tip', 'Counting the wavy marks of the magpie tail with the tip of a wing, one wave at a time', 18, 'wing',
        [k(.1, 'sill_r', reach=.6, x=.1, y=.2, b=-.2, l=1), k(.28, 'sill_r', reach=1, x=.3, y=.4, b=-.3, mark='1'), k(.44, 'sill', reach=1, x=.2, y=.6, b=-.5, w=.2, mark='2'), k(.6, 'trim_lo', reach=1, x=.4, y=.4, b=-.2, r=1, mark='3'), k(.78, 'trim_lo', reach=.7, x=.2, y=.1, b=0), k(.9, eye='-', mark='tail')],
        [], g='use', act=('count', 'tail'), ages=['duckling', *GROWN], prefer=['curious'])
    o.r('peer_at_the_magpie_until_it_peers_back', 'Peering at the magpie head with one eye and then the other, daring it to peer back', 20, 'none',
        [k(.14, x=.8, y=-.8, b=-.8), k(.32, x=1.6, y=-1.3, b=-1.2, eye='o'), k(.5, x=-1.0, y=-1.5, b=-1.4, eye='O', mark='hm'), k(.68, x=1.6, y=-1.3, b=-1.2, eye='o'), k(.86, x=.3, y=.4, b=.4, eye='>')],
        [], g='use', act=('peer', 'magpie'), prefer=['curious', 'young'])
    o.r('ring_the_plate_like_a_doorbell_for_the_magpie', 'Ringing the left plate on the frame like a doorbell, politely, in case the magpie is home', 18, 'wing',
        [k(.14, 'plate_lo', reach=.6, x=.3, y=-.2, b=.2), k(.32, 'plate_lo', reach=1, x=.5, y=-.4, b=.1, mark='ding'), k(.5, x=-.3, y=-.3, b=.2, eye='o'), k(.68, 'plate_lo', reach=1, x=.5, y=-.4, b=.1, l=1, mark='ding'), k(.86, eye='^')],
        [(.68, 'warm')], g='use', act=('ring', 'plate'), ages=GROWN, when=['bond<.7'], prefer=['lonely'], say=["Rang. Nobody answered. Magpie's being rude. It's a pendant.", "Doorbell. Dignity. Wait. Nothing."])
    # ---------------- play
    o.r('hop_sideways_with_both_feet_like_a_magpie', 'Hopping sideways along the foot of the case with both feet together like a magpie on a lawn, head cocked', 20, 'none',
        [k(.1, 'slat_d', x=.3, y=-.3, b=.4), k(.26, 'slat_e', x=.4, y=-.5, b=-.9, l=1, r=1), k(.42, 'slat_g', x=.3, y=-.4, b=.5), k(.58, 'slat_h', x=.4, y=-.5, b=-1.0, l=1, r=1, mark='hup'), k(.78, 'slat_i', x=.3, y=-.3, b=.4, eye='^')],
        [(.78, 'fun')], g='play', act=('hop', 'magpie'), prefer=['young', 'happy'])
    o.r('seek_the_charm_round_the_stud_and_pop_out', 'Peeking round the end stud at the charm, ducking back, and popping out again with a "found you"', 20, 'none',
        [k(.12, 'stud_r', x=.8, y=.5, b=.6), k(.28, 'stud_r', x=1.5, y=.8, b=1.4, eye='o'), k(.44, x=-.4, y=.2, b=.3, eye='-'), k(.6, 'stud_r', x=1.6, y=.8, b=1.5, l=1, eye='O', mark='boo'), k(.8, x=-.3, y=-.3, b=-.2, w=.5, eye='^')],
        [], g='play', act=('seek', 'stud'), prefer=['young', 'curious'])
    o.r('race_along_the_rail_with_his_own_shadow', 'Racing his own shadow along the bottom rail and cheating at the end by sitting down', 18, 'none',
        [k(.1, 'rail_ll', x=.4, y=.3, b=.4, l=1), k(.28, 'rail_l', x=1.0, y=.1, b=-.4, w=.5, r=1), k(.46, 'rail', x=1.3, y=0, b=-.5, w=.6, l=1, mark='zip'), k(.66, 'rail_r', x=1.3, y=0, b=-.5, w=.6, r=1), k(.84, 'rail_r', x=.2, y=.5, b=.9, eye='^')],
        [], g='play', act=('race', 'shadow'), prefer=['young', 'happy'])
    o.r('spin_after_his_own_tail_feathers', 'Spinning after his own tail feathers like a magpie caught on a thing it cannot reach', 18, 'none',
        [k(.12, x=.2, y=.3, b=.4), k(.28, x=-1.0, y=.3, b=-.5, w=.8, l=1), k(.44, x=1.0, y=.3, b=-.6, w=.8, r=1, mark='chak'), k(.6, x=-1.0, y=.3, b=-.7, w=.9, l=1), k(.76, x=.4, y=.8, b=.8, eye='@'), k(.9, eye='-')],
        [], g='play', act=('chase', 'tail'), prefer=['young', 'happy'])
    o.r('shuffle_the_hop_and_flap_along_the_slats', 'Shuffling a hop-and-flap along the slats in a magpie jig, three steps one way and three the other', 22, 'none',
        [k(.1, 'slat_b', x=.4, y=-.2, b=.3, l=1), k(.24, 'slat_g', x=.5, y=-.3, b=-.7, w=.9, r=1), k(.38, 'slat_h', x=.5, y=-.3, b=.2, l=1), k(.52, 'slat_g', x=.4, y=-.3, b=-.8, w=.9, r=1, mark='chak'), k(.68, 'slat_b', x=.5, y=-.3, b=.2, l=1), k(.84, 'slat_b', x=.3, y=-.2, b=.3, w=.4, eye='^')],
        [], g='play', act=('dance', 'slats'), prefer=['happy', 'young'], say=["Magpie jig. Original steps. Self-taught. Broken ankle pending.", "The charm kept time. Rare quality in a pendant."])
    o.r('flick_the_tail_at_the_glass_like_a_dare', 'Flicking his tail feathers at the glass like a dare and checking over his shoulder for the answer', 16, 'none',
        [k(.12, x=-.4, y=.2, b=.3), k(.3, 'slat_a', x=-1.0, y=.4, b=1.0, w=.8, l=1, mark='wiggle'), k(.46, 'slat_a', x=-1.1, y=.5, b=1.1, w=1, r=1, mark='wiggle'), k(.64, x=.9, y=-.4, b=-.3, eye='>'), k(.82, eye='^')],
        [], g='play', act=('shake', 'tail'), prefer=['grumpy', 'happy'])
    # ---------------- test
    o.r('sniff_the_charm_for_nest_and_feather', 'Lifting the charm in his bill and sniffing it for nest and feather and whatever a friend smells of', 22, 'none',
        [k(.1, x=.3, y=-.1, b=.3), k(.24, 'item', x=1.2, y=-.4, b=.6, mark='hup'), k(.4, 'item', x=1.5, y=.8, b=.2, eye='-', mark='snf'), k(.56, 'item', x=-.3, y=1.3, b=.5, l=1, eye='O', mark='snf'), k(.74, 'item', x=1.0, y=-.5, b=.5), k(.9, eye='^')],
        [], g='test', act=('sniff', 'charm'), ages=GROWN, prefer=['curious'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.64, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))])
    o.r('weigh_the_friendship_in_his_bill', 'Weighing the lifted charm in his bill, bobbing it, to decide how much a friendship weighs', 22, 'none',
        [k(.1, x=.4, y=-.2), k(.24, 'item', x=1.3, y=-.5, b=.3, mark='hup'), k(.4, 'item', x=1.4, y=-1.0, b=-.6), k(.54, 'item', x=1.3, y=.3, b=.8), k(.68, 'item', x=1.4, y=-1.0, b=-.6, eye='^'), k(.82, 'item', x=1.2, y=-.4, b=.3), k(.92, eye='-')],
        [], g='test', act=('weigh', 'charm'), ages=GROWN, prefer=['curious', 'lonely'], obj=[(.24, dict(hold=0)), (.38, dict(hold=1)), (.72, dict(hold=1)), (.84, dict(hold=1)), (.9, dict(hold=0))], say=["Light. Friendship is light. Rent isn't.", "Weighed it. Mostly string. Mostly good."])
    o.r('check_whether_the_magpie_blinks', 'Staring at the magpie for a whole count of ten to see whether it blinks, losing at six', 20, 'none',
        [k(.12, x=.7, y=-.6, b=.4, eye='o'), k(.3, x=1.0, y=-.8, b=.6, eye='O', mark='1-2-3'), k(.5, x=1.0, y=-.9, b=.8, eye='O', mark='...'), k(.68, x=.8, y=-.7, b=.9, l=1, eye='-', mark='blink'), k(.86, x=.2, y=.2, b=.3, eye='>')],
        [], g='test', act=('test', 'eye'), prefer=['curious', 'grumpy'])
    o.r('measure_his_bill_against_the_beak_with_a_wing', 'Measuring his own bill against the little beak with the length of a wing held flat to the glass', 20, 'wing',
        [k(.14, 'sill', reach=.6, x=.4, y=-.5, b=.2), k(.32, 'sill', reach=1, x=.9, y=-.8, b=.1, w=.2, l=1), k(.52, 'sill_r', reach=1, x=1.0, y=-.8, b=.2, mark='hm'), k(.72, 'sill_r', reach=.6, x=.3, y=-.3, b=.3, r=1), k(.88, eye='>', mark='bigger')],
        [], g='test', act=('measure', 'beak'), ages=['duckling', *GROWN], prefer=['curious'])
    o.r('tilt_his_head_to_match_the_magpie_head', 'Tilting his head to match the magpie head exactly, hold, then a quarter turn more, hold', 18, 'none',
        [k(.14, x=.5, y=-.4, b=.6), k(.32, x=1.4, y=-1.2, b=-1.0, eye='o'), k(.48, x=1.5, y=-1.3, b=-1.1, eye='o', mark='...'), k(.66, x=-1.4, y=-1.5, b=-1.3, eye='O'), k(.84, x=.2, y=.3, b=.4, eye='^')],
        [], g='test', act=('compare', 'tilt'), prefer=['curious', 'young'])
    o.r('knock_at_the_slats_for_a_friendly_voice', 'Knocking at the slats for a friendly voice, two slow knocks and a third to be sure', 20, 'none',
        [k(.12, 'slat_i', x=1.2, y=1.0, b=.5, mark='tok'), k(.28, x=-.3, y=-.3, b=-.2, eye='o'), k(.46, 'slat_i', x=1.3, y=1.1, b=.6, l=1, mark='tok'), k(.62, x=-.3, y=-.4, b=-.2, eye='O'), k(.8, 'slat_l', x=1.3, y=1.1, b=.6, r=1, mark='tok', eye='-')],
        [], g='test', act=('knock', 'slats'), prefer=['lonely', 'curious'])
    # ---------------- rest
    o.r('nap_fluffed_up_like_a_magpie_in_a_nest', 'Napping fluffed up like a magpie in a nest, one eye on the charm and then none', 30, 'none',
        [k(.14, 'slat_e', x=.3, y=.5, b=.8, w=.3), k(.38, 'slat_e', x=.2, y=1.2, b=1.5, w=.5, eye='o'), k(.66, 'slat_e', x=.2, y=1.5, b=1.8, w=.6, eye='-', mark='zzz'), k(.88, x=-.2, y=-.2, w=.4, eye='O')],
        [(.38, 'rest')], g='rest', act=('nap', 'nest'), when=['tired'], say=["Fluffed. Nest-ish. Eyes: closed. Beak: open. Snoring.", "Guarded the charm for six minutes. Then rested my case."])
    o.r('lean_on_the_end_stud_beside_the_charm', 'Leaning on the end stud as near to the charm as the case allows, bill tilted its way', 20, 'none',
        [k(.14, x=.3, y=-.2, b=.3, l=1), k(.4, 'stud_l', x=-.8, y=-.3, b=1.1, w=.2), k(.64, 'stud_l', x=-.9, y=-.5, b=1.3, r=1, eye='o', mark='...'), k(.86, x=.2, y=.1, b=.3)],
        [], g='rest', act=('lean', 'stud'), prefer=['lonely', 'tired'])
    o.r('sulk_because_the_magpie_has_not_called', 'Sulking with his back to the glass because the magpie has not called in a week and he is not counting', 24, 'none',
        [k(.12, x=-.9, y=.1, b=.4, r=1), k(.4, 'slat_g', x=-1.5, y=.9, b=1.3, w=.2, eye='-'), k(.68, 'slat_g', x=-1.7, y=1.1, b=1.4, w=.5, l=1, eye='-', mark='hmph'), k(.9, x=-.5, y=.5, b=.6)],
        [], g='rest', act=('sulk', 'silence'), when=['lonely', 'bond<.5'], say=["Not counting. It's been exactly nine days.", "No call. No note. Fine. I have bread."])
    o.r('wait_for_an_answer_with_his_head_on_one_side', 'Waiting with his head on one side for an answer from the pendant, sure it is only thinking', 28, 'none',
        [k(.14, x=.4, y=-.3, b=.4), k(.36, x=.7, y=-.6, b=.8, eye='o'), k(.58, x=-.7, y=-.8, b=.9, eye='o', mark='...'), k(.8, x=.4, y=-.3, b=.5, eye='O')],
        [], g='rest', act=('wait', 'reply'), prefer=['lonely', 'curious'])
    o.r('sit_side_by_side_with_the_pendant_saying_nothing', 'Sitting at the foot of the case facing the pendant, the two of them saying nothing, which is friendship', 28, 'none',
        [k(.14, 'rail_l', x=.3, y=.1, b=.6), k(.4, 'rail_l', x=.2, y=-.4, b=1.2, eye='-'), k(.66, 'rail_l', x=.2, y=-.5, b=1.3, eye='o', mark='...'), k(.86, x=.2, y=.2, b=.4, l=1)],
        [(.4, 'mates')], g='rest', act=('sit', 'rail'), prefer=['sad', 'tired'], say=["Said nothing. It said nothing back. Peak friendship.", "Comfortable silence. Mostly his. A little mine."])
    # ---------------- weather
    o.r('wink_back_at_the_sunny_gleam', 'Winking back at the gleam off the pane as the sun hits the glass, one eye and then the other, like a signal', 18, 'none',
        [k(.12, 'sill_r', x=.7, y=-.6, b=.3), k(.3, 'sill_r', x=1.0, y=-.9, b=.4, eye='-', mark='wink'), k(.48, 'sill_r', x=1.0, y=-.9, b=.5, l=1, eye='o', mark='wink'), k(.66, 'sill_r', x=1.0, y=-.9, b=.4, eye='-'), k(.84, eye='^')],
        [], g='weather', act=('peer', 'gleam'), when=['shine>.3'], ages=GROWN, prefer=['happy', 'curious'])
    o.r('shade_the_charm_from_the_noon_glare', 'Shading the charm from the noon glare with a wing held up flat so the magpie can keep its eyes open', 20, 'wing',
        [k(.12, 'sill_r', reach=.6, x=.2, y=-.4, b=.2), k(.3, 'sill_r', reach=1, x=.4, y=-.8, b=-.2, w=.3, l=1), k(.5, 'sill_r', reach=1, x=.3, y=-.7, b=.2, eye='-'), k(.7, 'sill_r', reach=1, x=.4, y=-.8, b=-.2, r=1), k(.88, eye='^')],
        [(.5, 'dim')], g='weather', act=('hide', 'shine'), when=['shine>.4'], ages=GROWN)
    o.r('chip_the_frost_off_beside_the_pendant', 'Chipping the frost off the left trim beside the pendant with a wing, a flake at a time', 16, 'wing',
        [k(.1, 'plate_lo', reach=.6, x=.1, y=-.1, b=.1), k(.3, 'plate_lo', reach=1, x=.7, y=-.7, b=-.4, w=.3, mark='tk'), k(.48, 'trim_l', reach=1, x=.8, y=-.8, b=-.5, l=1, mark='tk'), k(.66, 'trim_l', reach=1, x=.2, y=-.1, b=.7, r=1), k(.84, eye='-')],
        [(.48, 'thaw')], g='weather', act=('chip', 'rime'), when=['rime>.3'], ages=GROWN)
    o.r('huddle_in_a_ball_against_the_foot_for_the_storm', 'Huddling in a tight ball against the foot of the case while the storm shakes the glass, charm swinging above', 34, 'none',
        [k(.1, 'slat_h', x=-.3, y=.4, b=.7, r=1), k(.28, 'slat_h', x=-.9, y=1.0, b=1.5, w=.5, eye='>'), k(.52, 'slat_l', x=-1.1, y=1.3, b=1.8, w=.2, eye='-', mark='BOOM'), k(.76, 'slat_l', x=-.9, y=1.0, b=1.4, l=1, eye='>'), k(.9, 'slat_l', x=-.3, y=.4, b=.7)],
        [], g='weather', act=('shelter', 'storm'), when=['storm', 'wet'])
    o.r('shake_the_rain_off_his_back_and_check_the_charm', 'Shaking the rain off his back in a spray and checking the charm stayed dry, which it did, which is its trick', 18, 'none',
        [k(.12, x=.3, y=.3, b=.4), k(.3, x=.9, y=.4, b=-.7, w=1, l=1, mark='brrr'), k(.48, 'rail_r', x=-.9, y=.4, b=-.9, w=1, r=1, mark='BRRR'), k(.68, x=.5, y=-.3, b=-.4, w=.4, eye='O'), k(.86, eye='^')],
        [(.48, 'tidyup')], g='weather', act=('shake', 'rain'), when=['obj_wetness>.3'], prefer=['grumpy'])
    # ---------------- show
    o.r('bow_to_the_charm_as_to_an_old_friend', 'Bowing to the charm as to an old friend, a quick bob first and then the proper one with a flourish of the wing', 16, 'none',
        [k(.12, x=.4, y=.2, b=.4), k(.26, 'rail_r', x=1.0, y=1.0, b=1.0), k(.42, x=-.3, y=-.5, b=-.3, w=.4), k(.62, 'rail_r', x=1.3, y=1.8, b=1.6, w=.9, mark='...'), k(.8, x=-.3, y=-.4, b=-.2, w=.3, eye='^')],
        [], g='show', act=('bow', 'charm'), prefer=['happy'])
    o.r('present_the_charm_to_the_whole_room_as_his_friend', 'Presenting the charm to the whole room as his friend, one wing out, the other on his heart', 18, 'wing',
        [k(.12, reach=.2, x=.2, y=.2, b=.4), k(.3, reach=.9, x=.7, y=-.2, b=.2, w=.2), k(.5, reach=1, x=.9, y=-.5, b=0, w=.5, mark='my friend'), k(.7, reach=1, x=.7, y=-.3, b=.3, l=1), k(.86, reach=0, y=.2, b=.2, eye='^')],
        [], g='show', act=('present', 'friend'), prefer=['happy', 'lonely'], say=["Meet my friend. Don't mention the beak. It's sensitive.", "Introduced it round. Room: empty. Warm anyway."])
    o.r('strike_the_head_tilt_pose_with_one_foot_up', 'Striking the magpie pose, head cocked, one foot raised, an eye fixed on whatever glitters', 22, 'none',
        [k(.14, x=.3, y=.2, b=.6, l=1), k(.36, x=.9, y=-.6, b=-.6, w=.3, l=1), k(.58, x=1.1, y=-.9, b=-.8, w=.4, l=1, eye='o', mark='...'), k(.78, x=.9, y=-.6, b=-.5, l=1, eye='O'), k(.92, eye='^')],
        [], g='show', act=('pose', 'magpie'), prefer=['happy', 'curious'])
    o.r('argue_over_who_is_the_better_thief', 'Arguing over who is the better thief, wing jabbing at the pane, and losing to a bird made of ink', 20, 'none',
        [k(.14, x=.6, y=.2, b=.5, eye='>'), k(.32, 'trim_lo', x=1.3, y=-.5, b=.8, w=.8, mark='ME'), k(.5, x=-.5, y=.6, b=1.1, l=1, r=1), k(.68, 'trim_r', x=1.2, y=-.5, b=.9, w=1, mark='NO, ME'), k(.88, y=.6, b=.5, eye='-')],
        [], g='show', act=('argue', 'thief'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["Better thief. Stole a march on me. Fine. Draw.", "It never took my bread. Respect. Suspicion."])
    o.r('call_chak_chak_across_the_garden', 'Calling CHAK CHAK across the garden for the magpie to answer, hands cupped round his bill like a wing', 14, 'none',
        [k(.14, x=.4, y=-.4, b=-.2), k(.34, x=1.4, y=-1.6, b=-1.1, w=1, mark='CHAK CHAK'), k(.58, x=1.5, y=-1.7, b=-1.2, w=1, l=1, mark='CHAK CHAK'), k(.84, x=-.3, y=.3, eye='-', mark='...')],
        [], g='show', far=True, act=('shout', 'magpie'), prefer=['lonely'], say=["Chak chak. Nothing. It's busy being famous.", "Called twice. Got a wind. Might count."])
    o.r('sing_the_dawn_song_to_the_pendant', 'Singing the dawn song to the pendant in a thin early voice, bill up, swaying with the first light', 24, 'none',
        [k(.12, x=.2, y=-.2, b=.4), k(.3, x=.5, y=-.7, b=.0, w=.3, mark='la'), k(.5, x=.6, y=-.9, b=-.3, w=.5, l=1, mark='la la'), k(.7, x=.5, y=-.7, b=.0, w=.4, r=1, mark='la'), k(.88, eye='^')],
        [], g='show', act=('sing', 'dawn'), when=['dawn'], prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('peer_into_the_seam_for_the_magpie_and_get_stuck', 'Pushing his head into the door seam to see whether the magpie is hiding in there, and being stuck a while', 22, 'none',
        [k(.12, x=.7, y=-1.0, b=.1), k(.3, 'seam_lo', x=1.0, y=-.4, b=1.2, mark='hmm'), k(.48, 'seam_lo', x=1.3, y=-.4, b=1.6, r=1, eye='@', mark='mrf'), k(.66, 'seam_lo', x=1.5, y=-.5, b=1.0, l=1, w=1, mark='POP'), k(.84, x=-1.4, y=.9, b=.4, eye='@')],
        [], g='mishap', act=('stuck', 'seam'), shown='head', ages=GROWN, prefer=['curious', 'grumpy'])
    o.r('slip_on_the_wet_while_nodding_at_the_charm', 'Slipping on the wet at the foot of the case while nodding hello to the charm and going over backwards', 16, 'none',
        [k(.14, 'slat_a', x=.5, y=.3, b=.5, l=1), k(.3, x=-.9, y=-.5, b=-1.0, w=1, r=1, eye='O', mark='WHOA'), k(.5, 'rail_l', x=-1.6, y=1.7, b=2.0, w=.5, eye='@', mark='thud'), k(.8, x=.2, y=.5, b=.6, eye='-')],
        [], g='mishap', act=('slip', 'wetness'), when=['obj_wetness>.3'], prefer=['young'])
    o.r('walk_into_the_case_while_waving_goodbye', 'Bumping the case in the dark while waving goodbye to the charm over his shoulder', 14, 'none',
        [k(.12, x=-.4, y=-.2, b=.3, w=.6, r=1), k(.3, 'slat_g', x=-1.5, y=.3, b=1.0, w=.9, eye='O', mark='bonk'), k(.48, x=.8, y=-.4, b=-.8, w=.8, l=1, eye='@'), k(.8, x=.2, y=.4, b=.4, eye='>')],
        [], g='mishap', act=('walk_into', 'case'), when=['night'])
    o.r('stamp_about_in_a_huff_that_nobody_called', 'Stamping about in a huff that nobody called, one foot after the other, and stubbing a toe on the rail', 16, 'none',
        [k(.14, 'rail_ll', x=.3, y=.4, b=.4, l=1), k(.3, 'rail_ll', x=.3, y=.7, b=1.0, l=1, mark='STOMP'), k(.46, 'rail_l', x=.3, y=.7, b=1.0, r=1, mark='STOMP'), k(.62, 'rail_l', x=-.5, y=-.4, b=-1.2, l=1, w=.8, eye='O', mark='OW'), k(.82, eye='-')],
        [], g='mishap', act=('stamp', 'huff'), prefer=['grumpy', 'lonely'])
    o.r('catch_a_toe_on_the_stud_waving_and_hop_off', 'Catching a toe on the end stud while waving at the charm and hopping off clutching it', 16, 'none',
        [k(.14, 'stud_l', x=.4, y=-.2, b=-.3, w=.5, r=1), k(.3, 'stud_l', x=1.0, y=.5, b=1.1, w=.2, l=1, eye='O', mark='yoink'), k(.5, x=-.4, y=-.6, b=-1.3, w=.9, r=1, eye='@', mark='OW'), k(.7, x=.2, y=.6, b=.6, l=1, eye='>'), k(.88, eye='-')],
        [], g='mishap', act=('hook', 'stud'), prefer=['young'])
    o.r('knock_over_his_own_nod_and_roll_to_the_rail', 'Nodding at the charm so hard he tips forward and rolls to the rail, still nodding', 16, 'none',
        [k(.14, x=.6, y=-.4, b=.2), k(.3, x=1.2, y=.5, b=.9, eye='^'), k(.46, x=1.7, y=1.8, b=1.7, w=.4, eye='O'), k(.62, 'rail', x=1.8, y=2.0, b=2.0, w=.6, eye='@', mark='oof'), k(.84, x=.2, y=.6, b=.5, eye='-')],
        [], g='mishap', act=('balance', 'nod'), prefer=['young', 'happy'])
    # ---------------- duets (a friend takes their own part)
    o.r('tilt_heads_in_unison_at_the_charm', 'Tilting heads in unison with a friend at the charm, left, right, left, until nobody is sure who started', 24, 'none',
        [k(.12, 'rail_l', x=.4, y=-.3, b=.4), k(.28, 'rail_l', x=1.2, y=-.9, b=-.7, eye='o'), k(.44, 'rail_l', x=-1.2, y=-.9, b=-.8, eye='O'), k(.6, 'rail_l', x=1.2, y=-.9, b=-.7, eye='o', mark='hm'), k(.8, x=.2, y=.2, b=.3, eye='^')],
        [(.6, 'mates')], g='test', act=('compare', 'tilts'), prefer=['happy', 'curious'],
        duo=[k(.12, 'rail_r', x=.4, y=-.3, b=.4), k(.3, 'rail_r', x=-1.2, y=-.9, b=-.7, eye='O'), k(.46, 'rail_r', x=1.2, y=-.9, b=-.8, eye='o'), k(.62, 'rail_r', x=-1.2, y=-.9, b=-.7, eye='O'), k(.82, x=.2, y=.2, b=.3, eye='^')],
        say=["Same tilt. Same face. Friend: far better at it.", "We looked like a pair of pendants. Not the pretty kind."])
    o.r('hop_sideways_side_by_side_like_two_magpies', 'Hopping sideways side by side with a friend along the rail like two magpies on a lawn, heads cocked at the same worm', 24, 'none',
        [k(.1, 'rail_ll', x=.6, y=.5, b=.9), k(.26, 'rail_l', x=.8, y=-.7, b=-1.4, l=1, r=1), k(.42, 'rail', x=.6, y=.6, b=1.0), k(.58, 'rail', x=.8, y=-.7, b=-1.5, l=1, r=1, mark='hup'), k(.78, 'rail_r', x=.4, y=-.2, b=.3, eye='^')],
        [], g='play', act=('hop', 'partner'), prefer=['happy', 'young'],
        duo=[k(.1, 'rail_l', x=.6, y=.5, b=.9), k(.28, 'rail', x=.8, y=-.7, b=-1.4, l=1, r=1), k(.44, 'rail_r', x=.6, y=.6, b=1.0), k(.6, 'rail_r', x=.8, y=-.7, b=-1.5, l=1, r=1), k(.8, 'rail_r', x=.4, y=-.2, b=.3, eye='^')])
    o.r('lift_the_charm_between_two_bills', 'Lifting the charm out between two bills with a friend and setting it back in the exact same place, to prove it', 28, 'none',
        [k(.1, x=.3, y=-.2), k(.22, 'item', x=1.2, y=-.4, b=.3, mark='hup'), k(.4, 'item', x=1.6, y=-.9, b=-.4, l=1), k(.56, 'item', x=1.4, y=-.5, b=.4, r=1), k(.72, 'item', x=1.2, y=-.4, b=.3, eye='^'), k(.9, eye='^')],
        [], g='use', act=('carry', 'charm'), ages=GROWN, prefer=['happy', 'lonely'], obj=[(.22, dict(hold=0)), (.4, dict(hold=1)), (.62, dict(hold=1)), (.74, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.18, x=.3, y=-.2), k(.4, 'item', x=1.2, y=-.5, b=.3, eye='o'), k(.58, 'item', x=1.3, y=-.6, b=.4, l=1, eye='O'), k(.76, 'item', x=1.1, y=-.4, b=.3, eye='^')])
    o.r('call_and_answer_on_two_slats', 'Calling on one slat and a friend answering on the next, back and forth, until it sounds like a conversation', 26, 'none',
        [k(.12, 'slat_d', x=1.1, y=.9, b=.5, mark='tok'), k(.28, x=-.3, y=-.4, b=-.2, eye='o'), k(.44, 'slat_d', x=1.2, y=1.0, b=.6, l=1, mark='tok tok'), k(.62, x=-.3, y=-.4, b=-.2, eye='O'), k(.8, 'slat_d', x=1.1, y=.9, b=.5, r=1, mark='tok'), k(.92, eye='^')],
        [], g='play', act=('tap', 'slats'), prefer=['lonely', 'happy'],
        duo=[k(.2, x=-.3, y=-.4, b=-.2, eye='o'), k(.34, 'slat_e', x=1.1, y=.9, b=.5, mark='tok'), k(.52, 'slat_e', x=1.2, y=1.0, b=.6, r=1, mark='tok tok'), k(.7, x=-.3, y=-.4, b=-.2, eye='O'), k(.86, 'slat_e', x=1.1, y=.9, b=.5, l=1, mark='tok')])
    o.r('huff_a_patch_of_mist_and_peck_two_birds_in_it', 'Huffing a patch of mist onto the pane and pecking two small birds into it, side by side, one a bit crooked', 20, 'none',
        [k(.12, 'sill', x=1.2, y=-.5, b=.4, mark='haaa'), k(.3, 'sill', x=1.3, y=-.8, b=.2, mark='tk'), k(.48, 'sill_r', x=1.3, y=-.8, b=.3, l=1, mark='tk'), k(.66, 'sill_r', x=1.4, y=-.9, b=.1, r=1, mark='tk'), k(.86, eye='^')],
        [(.12, 'huff')], g='use', act=('peck', 'birds'), ages=GROWN, prefer=['happy', 'lonely'], say=["Two birds. Side by side. One's me. Crooked.", "Drew a friend in fog. It'll be gone by noon. Like most."])
    o.r('press_his_nose_to_the_beak_for_a_proper_hello', 'Pressing his nose to the glass at the beak for a proper hello, eyes crossed, and leaving a print', 18, 'none',
        [k(.14, x=.5, y=-.4, b=.3), k(.32, 'trim_lo', x=1.5, y=-.7, b=.6, eye='O', mark='mmf'), k(.5, 'trim_lo', x=1.6, y=-.8, b=.7, r=1, eye='@'), k(.7, 'trim_l', x=1.4, y=-.6, b=.5, l=1, eye='o'), k(.88, x=-.3, y=-.2, w=.3, eye='^')],
        [(.32, 'nose')], g='test', act=('press', 'glass'), ages=['duckling', *GROWN], prefer=['curious', 'lonely'])
    # @@m_end2
    return done(o)


# @@rainbow_charm
def rainbow_charm():
    # Drawing: the same cord loop above a pendant ring (never touched: 119-146 px up); in the ring a rainbow arch of nested arcs (`.--==--.`, `/.-=2-.\\`) standing on two
    # legs (`| |  | |`), and a row of `=-=` stripes along the foot of the ring. What it IS here is the arch: tracing it, counting its bands, chasing its foot and the light it throws.
    # `prism` is the bright flecks the glass throws when the sun is out or a rainbow hangs in the sky.
    o = Obj('rainbow_charm', 'display', on='trophy_case',
            fields=dict(fog=(0, 0, 1), prints=(0, 0, 1), prism=(0, 0, 1), rime=(0, 0, 1)),
            physics=[('fog', 'rate', -.0006, 'always'), ('prints', 'rate', -.0003, 'always'), ('prism', 'rate', .0025, 'sun'), ('prism', 'rate', .004, 'rainbow_sky'),
                     ('prism', 'rate', -.0008, 'always'), ('rime', 'rate', .002, 'snow'), ('rime', 'rate', -.002, 'warm')],
            effects=dict(huff=[('fog', 'add', .5)], clear=[('fog', 'set', 0)], nose=[('prints', 'add', .35)], buff=[('prints', 'set', 0)],
                         catch=[('prism', 'mul', .3)], thaw=[('rime', 'set', 0)],
                         clean=[('obj.dirt', 'add', -.3)], dry=[('obj.wetness', 'add', -.3)],
                         fun=[('need.fun', 'add', 2)], tidyup=[('need.cleanliness', 'add', 2)], rest=[('need.energy', 'add', 2)], mates=[('need.social', 'add', 2)]),
            marks=[('fog', .3, '~ ~ ~', 'sill', 'water'), ('prints', .3, 'o  o', 'trim_lo', 'dust'), ('prism', .3, '. * . *', 'sill_r', 'glow'), ('rime', .3, '*-*-*', 'trim_l', 'frost')],
anchors=dict(item=0, slat_a=(0.2476, 0.8961), slat_b=(0.5333, 0.8961), slat_c=(0.8190, 0.8961), slat_f=(0.4381, 0.9221), slat_g=(0.6286, 0.8831), slat_h=(0.7238, 0.9091), slat_j=(0.2952, 0.8701), slat_k=(0.5810, 0.9221), slat_l=(0.7714, 0.8701), stud_l=(0.0952, 0.9091), stud_r=(0.9048, 0.9091), rail=(0.5048, 0.9351), rail_l=(0.2857, 0.9351), rail_r=(0.7429, 0.9351), rail_rr=(0.8571, 0.9351), trim_lo=(0.4762, 0.8442), trim_l=(0.1905, 0.8442), trim_r=(0.7619, 0.8442), sill=(0.3810, 0.8182), sill_r=(0.6667, 0.8182), ledge=(0.2857, 0.7922), seam_lo=(0.5048, 0.7532), plate_lo=(0.1048, 0.8182)))
    # ---------------- care
    o.r('wipe_the_mist_off_in_one_big_arc', 'Wiping the breath mist off the pane in one big arc with a wing, high over to low, like a rainbow in reverse', 18, 'wing',
        [k(.12, 'trim_l', reach=.6, x=.2, y=-.3, b=.4), k(.3, 'sill', reach=1, x=.5, y=-.8, b=-.5, w=.4, l=1), k(.48, 'sill_r', reach=1, x=.6, y=-.9, b=-.6, w=.5), k(.66, 'trim_r', reach=1, x=.5, y=-.4, b=.2, r=1), k(.86, eye='^')],
        [(.48, 'clear')], g='care', act=('wipe', 'mist'), when=['fog>.3'], prefer=['happy'], say=["Cleared an arc. Looks a bit like effort. It was.", "Mist off. Colours showing. Stripes on parade."])
    o.r('rub_the_nose_prints_off_with_a_flat_wing', 'Rubbing the nose prints off the lower pane with a flat wing in long strokes, stripe by stripe', 18, 'wing',
        [k(.12, 'trim_lo', reach=.6, x=.3, y=-.2, b=.5), k(.3, 'trim_lo', reach=1, x=.5, y=-.2, b=.8, w=.2), k(.48, 'trim_r', reach=1, x=.6, y=-.3, b=.7, l=1), k(.66, 'trim_r', reach=1, x=.5, y=-.2, b=.9), k(.84, eye='-')],
        [(.48, 'buff')], g='care', act=('wipe', 'prints'), ages=['duckling', *GROWN], when=['prints>.3'], prefer=['curious'])
    o.r('dab_the_drizzle_off_the_pane_bit_by_bit', 'Dabbing the drizzle off the pane bit by bit with a wing tip so the colours come back', 20, 'wing',
        [k(.12, 'sill_r', reach=.6, x=.2, y=-.4, b=.1), k(.3, 'sill_r', reach=1, x=.5, y=-.6, b=.3, mark='dab'), k(.48, 'sill', reach=1, x=.4, y=-.6, b=.4, l=1, mark='dab'), k(.66, 'trim_lo', reach=1, x=.4, y=-.3, b=.5, mark='dab'), k(.84, eye='^')],
        [(.48, 'dry')], g='care', act=('dry', 'glass'), when=['obj_wetness>.3'], ages=GROWN)
    o.r('buff_the_studs_to_a_rainbow_gleam', 'Buffing the two end studs with his chest feathers until each throws a little gleam of its own', 20, 'none',
        [k(.12, 'stud_r', x=.5, y=1.2, b=.9), k(.3, 'stud_r', x=.3, y=1.5, b=1.2, r=1, mark='rub'), k(.5, x=-.3, y=-.2, b=-.4, w=.7, l=1), k(.7, 'stud_l', x=.5, y=1.2, b=.9, mark='rub'), k(.88, 'stud_l', x=.3, y=1.5, b=1.1, l=1, eye='^')],
        [(.7, 'clean')], g='care', act=('polish', 'studs'), when=['obj_dirt>.3'], prefer=['happy'])
    o.r('sweep_the_foot_of_the_charm_strip_with_a_twig', 'Sweeping the dusty ledge clean with a twig, one pass for each stripe', 20, 'twig',
        [k(.12, 'ledge', reach=.6, x=.3, y=.1, b=.3), k(.3, 'ledge', reach=1, x=.5, y=.3, b=.5, mark='shf'), k(.48, 'ledge', reach=1, x=.6, y=.3, b=.6, l=1, mark='shf'), k(.66, 'ledge', reach=1, x=.5, y=.3, b=.5, r=1), k(.86, eye='^')],
        [(.48, 'clean')], g='care', act=('sweep', 'ledge'), when=['obj_dirt>.3'], ages=GROWN)
    o.r('fluff_himself_into_stripes_for_the_charm', 'Fluffing himself into stripes for the charm, wing feathers one way and tail feathers the other, and admiring the result', 20, 'none',
        [k(.12, x=.3, y=.4, b=.5), k(.3, 'sill', x=.8, y=.4, b=.7, w=.9, l=1, eye='>'), k(.5, 'sill', x=.6, y=.6, b=.8, w=.6, eye='-', mark='ffff'), k(.7, 'sill', x=.8, y=.3, b=.6, w=1, r=1, eye='^'), k(.88, eye='^')],
        [(.5, 'tidyup')], g='care', act=('fluff', 'feathers'), ages=GROWN, prefer=['happy', 'curious'])
    # ---------------- use
    o.r('tilt_the_charm_so_the_arch_catches_the_light', 'Lifting the charm out in his bill and tilting it slowly so the arch catches the light one stripe at a time', 26, 'none',
        [k(.1, x=.3, y=-.3, b=.1), k(.22, 'item', x=1.2, y=-.5, b=.4, mark='hup'), k(.4, 'item', x=1.3, y=-.9, b=-.1, l=1), k(.56, 'item', x=1.6, y=-1.1, b=-.3, r=1, eye='O'), k(.72, 'item', x=1.3, y=-.7, b=.2), k(.84, 'item', x=1.2, y=-.4, b=.4), k(.94, eye='^')],
        [], g='use', act=('tilt', 'charm'), ages=GROWN, prefer=['curious', 'happy'], obj=[(.22, dict(hold=0)), (.4, dict(hold=1)), (.74, dict(hold=1)), (.86, dict(hold=1)), (.92, dict(hold=0))],
        say=["Caught a stripe. Then another. Then the sun, in the eye.", "Every angle's a different colour. Show-off. I approve."])
    o.r('count_the_stripes_along_the_base_of_the_ring', 'Lifting the charm and counting the stripes along the foot of its ring with his bill, getting a different number each time', 28, 'none',
        [k(.1, x=.3, y=-.2), k(.2, 'item', x=1.3, y=-.5, b=.3, mark='hup'), k(.34, 'item', x=1.0, y=.6, b=.7, mark='1'), k(.48, 'item', x=1.1, y=.7, b=.8, l=1, mark='2'), k(.62, 'item', x=1.2, y=.8, b=.9, r=1, mark='3'), k(.78, 'item', x=1.3, y=-.4, b=.3, eye='-', mark='lots'), k(.92, eye='>')],
        [], g='use', act=('count', 'stripes'), ages=GROWN, prefer=['curious'], obj=[(.2, dict(hold=0)), (.34, dict(hold=1)), (.8, dict(hold=1)), (.88, dict(hold=1)), (.92, dict(hold=0))])
    o.r('look_the_whole_arch_through_with_each_eye', 'Looking the whole arch through, left leg to right, with one eye and then the other, to see which sees more colours', 20, 'none',
        [k(.14, x=.7, y=-.6, b=.2), k(.3, x=1.5, y=-1.1, b=-.4, eye='o'), k(.5, x=-1.3, y=-1.3, b=-.6, eye='O', mark='hm'), k(.68, x=1.5, y=-1.1, b=-.4, eye='o'), k(.86, x=.2, y=.2, b=.2, eye='-')],
        [], g='use', act=('peer', 'arch'), prefer=['curious', 'young'])
    o.r('huff_on_the_pane_and_draw_an_arch_in_the_mist', 'Huffing on the pane and pecking an arch in the mist with his bill, then three smaller ones inside it', 22, 'none',
        [k(.1, 'sill', x=1.1, y=-.4, b=.3, mark='haaa'), k(.26, 'sill', x=1.3, y=-.9, b=.0, mark='tk'), k(.42, 'sill_r', x=1.4, y=-1.0, b=-.1, l=1, mark='tk'), k(.58, 'trim_r', x=1.3, y=-.5, b=.3, r=1, mark='tk'), k(.76, 'sill_r', x=1.0, y=-.9, b=.0, mark='tk tk'), k(.9, eye='^')],
        [(.1, 'huff')], g='use', act=('peck', 'arch'), ages=GROWN, prefer=['happy', 'young'], say=["Four arches. Three wonky. One of them's me.", "Drew a rainbow in my own breath. Peak talent."])
    o.r('walk_the_rail_on_tiptoe_like_a_rainbow_bridge', 'Walking the rail on tiptoe like a rainbow bridge, wings out for balance, and not looking down', 24, 'none',
        [k(.1, 'rail_l', x=.3, y=-.3, b=-.5, w=.6, l=1), k(.28, 'rail_l', x=.5, y=-.7, b=-.8, w=1, r=1), k(.46, 'rail', x=.5, y=-.8, b=-.9, w=1, l=1, mark='eep'), k(.64, 'rail_r', x=.5, y=-.7, b=-.8, w=1, r=1), k(.82, 'rail_rr', x=.3, y=-.3, b=-.4, w=.5, eye='^')],
        [], g='use', act=('balance', 'rail'), prefer=['happy', 'young'])
    o.r('ring_the_plate_like_a_bell_for_a_change_of_weather', 'Ringing the left plate on the frame like a bell, asking for a bit of sun after the rain', 16, 'wing',
        [k(.14, 'plate_lo', reach=.6, x=.3, y=-.3, b=.1), k(.32, 'plate_lo', reach=1, x=.5, y=-.5, b=-.2, mark='ding'), k(.5, x=-.2, y=-.8, b=-.3, eye='O'), k(.68, 'plate_lo', reach=1, x=.6, y=-.5, b=-.3, l=1, mark='DING'), k(.86, eye='^')],
        [], g='use', act=('ring', 'plate'), ages=GROWN, when=['obj_wetness>.3'], prefer=['sad', 'curious'], say=["Rang for sun. A cloud answered. Weather has a sense of humour.", "Ding. If it's not sunny in ten, I'm filing a complaint."])
    # ---------------- play
    o.r('leap_from_stud_to_stud_like_the_two_legs', 'Leaping from the left stud to the right stud and back like the two legs of the arch, a hop at every step', 22, 'none',
        [k(.1, 'stud_l', x=.4, y=.4, b=.6, l=1), k(.26, 'slat_f', x=.6, y=-.6, b=-1.2, w=.7, r=1), k(.42, 'stud_r', x=.5, y=.4, b=.7, l=1, mark='hup'), k(.6, 'slat_j', x=.6, y=-.6, b=-1.2, w=.7, r=1), k(.8, 'stud_l', x=.4, y=.4, b=.6, eye='^')],
        [(.42, 'fun')], g='play', act=('hop', 'studs'), prefer=['young', 'happy'])
    o.r('chase_the_foot_of_the_rainbow_down_the_rail', 'Chasing the foot of the rainbow down the bottom rail, always just one step short of it, and never touching it', 20, 'none',
        [k(.1, 'rail_l', x=.4, y=.3, b=.4, l=1), k(.26, 'rail', x=1.2, y=.2, b=-.5, w=.6, r=1), k(.42, 'rail_r', x=1.5, y=.1, b=-.6, w=.8, l=1, mark='almost'), k(.58, 'rail_rr', x=1.5, y=.1, b=-.6, w=.8, r=1), k(.76, 'rail_rr', x=.2, y=.7, b=.8, eye='@'), k(.9, eye='-')],
        [], g='play', act=('chase', 'rainbow'), prefer=['young', 'happy'], say=["Almost had the end. It moved. Rude. Colourful, but rude.", "Raced it to the stud. Lost. It's a very fast arch."])
    o.r('dig_at_the_foot_of_the_arch_for_a_pot_of_something', 'Digging at the foot of the case where the arch would land, sure there is a pot of something, and finding the rail', 20, 'none',
        [k(.12, 'rail_rr', x=.4, y=1.1, b=.8, l=1), k(.28, 'rail_rr', x=.5, y=1.5, b=1.2, l=1, mark='skrt'), k(.44, 'rail_rr', x=.5, y=1.6, b=1.3, r=1, mark='skrt'), k(.6, 'rail_rr', x=.4, y=1.7, b=1.4, l=1, eye='O', mark='...'), k(.78, x=-.5, y=.5, b=.4, w=.4, eye='-', mark='bah')],
        [], g='play', act=('dig', 'foot'), prefer=['curious', 'grumpy'], say=["No pot. Dug a bit. Found rail. Grudge acquired.", "Nothing at the end. The legend is a big liar."])
    o.r('spin_till_every_colour_runs_together', 'Spinning on the spot until every colour runs together into one brown smear and then falling over', 18, 'none',
        [k(.12, x=.2, y=.2, b=.3), k(.28, x=1.1, y=-.4, b=-.7, w=1, l=1), k(.44, x=-1.1, y=-.4, b=-.9, w=1, r=1, mark='whirr'), k(.6, x=1.1, y=-.5, b=-1.0, w=1, l=1, r=1), k(.76, x=-.2, y=1.0, b=1.2, w=.3, eye='@', mark='thud'), k(.9, eye='-')],
        [], g='play', act=('spin', 'colours'), prefer=['young', 'happy'])
    o.r('snap_at_the_gleams_as_they_flick_over_the_slats', 'Snapping at the gleams as they flick across the slats, one jump each, never landing a single one', 20, 'none',
        [k(.12, 'slat_g', x=.7, y=.2, b=.5), k(.28, 'slat_g', x=1.1, y=-.3, b=-.9, w=.5, l=1, mark='snap'), k(.44, 'slat_h', x=1.2, y=-.3, b=-.9, w=.5, r=1, mark='snap'), k(.6, 'slat_k', x=1.1, y=-.3, b=-.9, w=.5, l=1, mark='snap'), k(.8, x=.3, y=.6, b=.5, eye='@')],
        [], g='play', act=('catch', 'gleams'), when=['prism>.3'], prefer=['young', 'happy'])
    o.r('hold_the_arch_on_one_foot_wings_in_a_curve', 'Holding the arch on one foot with both wings in a curve over his head, not wobbling, much', 24, 'none',
        [k(.12, x=.4, y=.4, b=.6), k(.3, x=.6, y=-.9, b=-1.3, w=.8, l=1), k(.5, x=.8, y=-1.4, b=-1.6, w=1, l=1, mark='...'), k(.68, x=.8, y=-1.4, b=-1.6, w=1, l=1, eye='-'), k(.84, x=.3, y=.6, b=.8, eye='^')],
        [], g='play', act=('balance', 'arch'), prefer=['happy', 'curious'])
    # ---------------- test
    o.r('sniff_the_charm_for_rain_and_hope', 'Lifting the charm in his bill to sniff it for the smell of rain and, past that, a bit of hope', 22, 'none',
        [k(.1, x=.5, y=-.4, b=.2), k(.24, 'item', x=1.1, y=-.9, b=.5, mark='hup'), k(.4, 'item', x=1.0, y=1.2, b=.9, eye='-', mark='snf'), k(.56, 'item', x=1.1, y=1.4, b=1.0, l=1, eye='O', mark='snf'), k(.74, 'item', x=1.1, y=-.9, b=.5), k(.9, eye='^')],
        [], g='test', act=('sniff', 'charm'), ages=GROWN, prefer=['curious'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.64, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))])
    o.r('span_the_arch_with_both_wings_to_measure_it', 'Spreading both wings against the slats to measure how wide the arch is from leg to leg, then again to be sure', 22, 'wing',
        [k(.12, 'slat_a', reach=.5, x=.3, y=.3, b=.4), k(.3, 'slat_a', reach=1, x=.5, y=.4, b=.6, l=1), k(.5, 'slat_l', reach=1, x=.6, y=.5, b=.6, mark='hm'), k(.7, 'slat_a', reach=1, x=.5, y=.4, b=.6, r=1), k(.86, eye='-', mark='wide')],
        [], g='test', act=('measure', 'arc'), prefer=['curious'])
    o.r('lick_a_stripe_of_the_rail_for_flavour', 'Licking the rail where the stripes would land to find out what colour tastes like, and finding out it is wood', 16, 'none',
        [k(.14, 'rail_r', x=1.1, y=1.6, b=.9), k(.32, 'rail_r', x=1.3, y=1.8, b=1.1, eye='-', mark='...'), k(.5, x=-.9, y=-.4, b=-.3, w=.8, r=1, eye='>', mark='ptui'), k(.8, y=.5, b=.3, eye='-')],
        [], g='test', act=('taste', 'stripes'), prefer=['curious', 'young'], say=["Orange tastes like wood. Possibly. Also like regret.", "Colours have no flavour. Colours are liars."])
    o.r('hold_the_charm_against_his_own_feathers', 'Holding the lifted charm against his own wing to see whether any of his feathers match a stripe', 24, 'none',
        [k(.1, x=.3, y=-.2, b=.2), k(.24, 'item', x=1.2, y=-.4, b=.4, mark='hup'), k(.42, 'item', x=.4, y=.5, b=1.0, w=.5, l=1), k(.58, 'item', x=.3, y=.7, b=1.1, w=.7, r=1, eye='>', mark='hm'), k(.74, 'item', x=1.2, y=-.4, b=.4), k(.9, eye='-')],
        [], g='test', act=('compare', 'feathers'), ages=GROWN, prefer=['curious', 'grumpy'], obj=[(.24, dict(hold=0)), (.4, dict(hold=1)), (.66, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))])
    o.r('listen_for_the_hush_after_the_rain', 'Listening at the slats for the hush after the rain, ear to one slat, then the next one along', 22, 'none',
        [k(.1, x=.3, y=.4, b=.6), k(.26, 'slat_b', x=-.9, y=1.5, b=.6, eye='-'), k(.46, 'slat_b', x=-1.0, y=1.7, b=.4, l=1, eye='-', mark='...'), k(.64, 'slat_c', x=-1.0, y=1.7, b=.5, eye='o', mark='hush'), k(.84, x=.6, y=-.6, b=-.2, w=.5, eye='O')],
        [], g='test', act=('listen', 'slats'), prefer=['curious', 'lonely'])
    o.r('press_his_nose_to_the_stripes_and_count_their_edges', 'Pressing his nose to the pane at the arch and counting the edges of each stripe, then leaving a print', 18, 'none',
        [k(.12, x=.9, y=.3, b=.7, r=1), k(.3, 'trim_r', x=1.8, y=-.3, b=1.3, eye='O', mark='mmf'), k(.5, 'trim_lo', x=1.9, y=-.4, b=1.4, l=1, eye='@'), k(.7, 'trim_l', x=1.7, y=-.3, b=1.2, eye='o'), k(.88, x=-.6, y=-.6, b=-.3, w=.4, eye='^')],
        [(.3, 'nose')], g='test', act=('press', 'glass'), ages=['duckling', *GROWN], prefer=['curious', 'young'])
    # ---------------- rest
    o.r('nap_curled_in_the_colours_at_the_foot_of_the_case', 'Napping curled up in a ball at the foot of the case, as if the whole rainbow were a blanket', 30, 'none',
        [k(.15, 'slat_f', x=-.3, y=.6, b=.8), k(.4, 'slat_f', x=-.7, y=1.3, b=1.7, eye='-'), k(.7, 'slat_f', x=-.8, y=1.5, b=1.9, w=.2, eye='-', mark='zzz'), k(.9, x=-.2, y=-.3, w=.4, eye='O')],
        [(.4, 'rest')], g='rest', act=('nap', 'colours'), when=['tired'], say=["Dreamt in colour. Woke up in beige.", "Slept in stripes. Dawn arrived in plain."])
    o.r('lean_against_the_stud_like_a_leg_of_the_arch', 'Leaning against the left stud like a leg of the arch, one foot lifted, holding it up for a rest', 20, 'none',
        [k(.14, x=.3, y=.2, b=.4, r=1), k(.4, 'stud_l', x=-.9, y=.2, b=1.1, w=.2), k(.66, 'stud_l', x=-1.0, y=.4, b=1.3, l=1, eye='-', mark='...'), k(.86, x=.3, y=.2, b=.4)],
        [], g='rest', act=('lean', 'stud'), prefer=['tired', 'sad'])
    o.r('sulk_because_the_colours_only_come_after_rain', 'Sulking with grey in his mood because the colours only come out after the rain and he did all the waiting', 24, 'none',
        [k(.14, x=-.6, y=.4, b=.5, l=1), k(.4, 'slat_k', x=-1.2, y=1.2, b=1.2, w=.1, eye='-'), k(.7, 'slat_k', x=-1.4, y=1.4, b=1.5, r=1, eye='-', mark='hmph'), k(.9, x=-.5, y=.5, b=.6)],
        [], g='rest', act=('sulk', 'rain'), when=['sad'], say=["Rain first. Colours second. Typical. Nothing's ever free.", "Sulking in grey. Only the rainbow gets to be fancy."])
    o.r('wait_for_the_sun_to_break_through', 'Waiting at the foot of the case with one eye on the sky for the sun to break through and light the arch', 28, 'none',
        [k(.14, x=.6, y=-.8, b=.9), k(.36, x=1.0, y=-1.3, b=-.4, eye='o'), k(.58, x=1.1, y=-1.5, b=-.6, eye='o', mark='...'), k(.8, x=.5, y=-.4, b=.8, eye='O')],
        [], g='rest', act=('wait', 'sun'), prefer=['sad', 'curious'])
    o.r('sit_with_his_bill_tucked_in_where_the_arch_lands', 'Sitting at the right end of the case with his bill tucked in, patient as a man who has lost a pot of something', 28, 'none',
        [k(.12, 'rail_rr', x=.5, y=.9, b=.4, r=1), k(.34, 'rail_rr', x=.4, y=.6, b=1.2, eye='-'), k(.6, 'rail_rr', x=.3, y=1.8, b=1.9, l=1, eye='o', mark='sigh'), k(.84, x=.6, y=.7, b=.6)],
        [], g='rest', act=('sit', 'foot'), prefer=['sad', 'tired'])
    # ---------------- weather
    o.r('flash_the_prism_back_with_a_wing', 'Flashing the prism flecks back across the slats with the flat of a wing like a mirror, until the glass goes dull', 20, 'wing',
        [k(.1, 'sill_r', reach=.6, x=-.2, y=-.1, b=.6), k(.28, 'sill_r', reach=1, x=.2, y=-.4, b=-.7, w=.8, r=1, mark='flash'), k(.46, 'sill', reach=1, x=-.3, y=-.5, b=.5, l=1, mark='flash'), k(.64, 'sill_r', reach=1, x=.3, y=-.5, b=-.8, w=.6), k(.84, eye='^')],
        [(.46, 'catch')], g='weather', act=('shake', 'prism'), when=['prism>.4'], ages=GROWN, prefer=['happy', 'young'])
    o.r('stretch_both_wings_up_to_match_the_arch_in_the_sky', 'Stretching both wings up in a curve to match the real arch in the sky, tip to tip, for the photograph', 22, 'none',
        [k(.12, x=.2, y=-.2, b=.2), k(.32, x=.4, y=-.9, b=-.6, w=.9, l=1), k(.54, x=.5, y=-1.3, b=-1.0, w=1, l=1, r=1, mark='...'), k(.74, x=.4, y=-1.0, b=-.7, w=.9), k(.88, x=.1, y=.2, b=.2, eye='^')],
        [], g='weather', act=('open', 'arch'), when=['rainbow_sky'], prefer=['happy', 'curious'], say=["Matched the sky. Better posture. Fewer stripes.", "Held the pose. A cloud stole the light. Typical cloud."])
    o.r('chip_the_frost_off_the_left_trim_in_one_go', 'Chipping the frost off the left trim in one go with the tip of a wing, from the plate up to the corner', 16, 'wing',
        [k(.1, 'plate_lo', reach=.6, x=.2, y=-.2, b=.5), k(.28, 'plate_lo', reach=1, x=.4, y=-.5, b=.8, w=.2, mark='tk'), k(.46, 'trim_l', reach=1, x=.5, y=-.6, b=.7, l=1, mark='tk'), k(.64, 'trim_l', reach=1, x=.6, y=-.7, b=.6, mark='tk'), k(.82, eye='-')],
        [(.46, 'thaw')], g='weather', act=('chip', 'rime'), when=['rime>.3'], ages=GROWN)
    o.r('huddle_close_against_the_slats_until_it_clears', 'Huddling close against the slats until the storm clears, then peeking up for the first stripe of colour', 34, 'none',
        [k(.1, 'slat_l', x=-.2, y=.3, b=.6), k(.26, 'slat_l', x=-.8, y=.9, b=1.3, w=.4, eye='>'), k(.5, 'slat_j', x=-1.0, y=1.2, b=1.7, w=.2, eye='-', mark='CRASH'), k(.72, 'slat_j', x=-.8, y=.8, b=1.2, l=1, eye='-'), k(.88, 'slat_j', x=.2, y=-.8, b=-.2, w=.4, eye='O', mark='ooh')],
        [], g='weather', act=('shelter', 'slats'), when=['storm', 'wet'])
    o.r('watch_the_rain_thin_out_on_the_glass_for_a_bow', 'Watching the rain thin out on the glass with his bill tipped up, waiting for the first bow of colour', 22, 'none',
        [k(.14, 'sill', x=.6, y=-.6, b=.3), k(.34, 'sill', x=.9, y=-1.0, b=.0, eye='o'), k(.54, 'sill', x=1.0, y=-1.2, b=-.2, l=1, eye='O', mark='...'), k(.74, 'sill', x=.9, y=-1.0, b=0, eye='^', mark='ooh'), k(.9, eye='^')],
        [], g='weather', act=('peer', 'rain'), when=['obj_wetness>.3'], ages=GROWN, prefer=['curious', 'young'])
    # ---------------- show
    o.r('bow_to_the_arch_down_to_the_last_stripe', 'Bowing to the arch from tall to small, one stripe lower at a time, until his bill is on the rail', 18, 'none',
        [k(.12, x=-.4, y=-.8, b=-.6, w=.4), k(.28, x=.2, y=.2, b=.3, w=.3), k(.44, 'rail_l', x=.8, y=.9, b=.8), k(.6, 'rail_l', x=1.2, y=1.6, b=1.5, w=.5, mark='...'), k(.78, x=-.3, y=-.4, b=-.2, w=.2, eye='^')],
        [], g='show', act=('bow', 'arch'), prefer=['happy'])
    o.r('present_the_arch_to_the_empty_sky', 'Presenting the arch to the empty sky, one wing carving the curve in the air from low to high to low', 18, 'wing',
        [k(.12, reach=.3, x=-.2, y=.3, b=.5, r=1), k(.3, reach=.8, x=.2, y=-.4, b=-.2), k(.5, reach=1, x=.5, y=-1.0, b=-.8, w=.4, mark='behold'), k(.7, reach=1, x=.2, y=-.3, b=-.2, l=1), k(.86, reach=0, y=.3, b=.4, eye='^')],
        [], g='show', act=('present', 'rainbow'), prefer=['happy'], say=["Behold. Sky: please hold still. It does not.", "Every colour, all at once. You're welcome. Nobody's here."])
    o.r('pose_with_the_legs_wide_and_the_wings_in_an_arch', 'Posing with his legs wide as the arch and both wings curved over his head, bill pointed at the sun', 22, 'none',
        [k(.14, x=.3, y=.4, b=.8, l=1, r=1), k(.36, x=.5, y=-.4, b=.5, w=.6, l=1, r=1), k(.58, x=.6, y=-1.0, b=.2, w=1, l=1, r=1, mark='...'), k(.78, x=.5, y=-.7, b=.4, w=.8, l=1, r=1), k(.92, eye='^')],
        [], g='show', act=('pose', 'arch'), prefer=['happy'])
    o.r('argue_with_the_arch_about_who_has_more_colours', 'Arguing with the arch about who has more colours, wing jabbing at the pane and counting his own on his fingers', 20, 'none',
        [k(.14, x=.8, y=.2, b=.4, eye='>'), k(.32, 'trim_r', x=1.3, y=-.6, b=.7, w=.8, mark='MORE'), k(.5, x=-.5, y=.5, b=1.0, l=1, r=1, mark='1.2.3'), k(.68, 'trim_lo', x=1.2, y=-.5, b=.8, w=1, mark='MORE!'), k(.88, y=.7, b=.7, eye='-')],
        [], g='show', act=('argue', 'colours'), ages=['duckling', *GROWN], prefer=['grumpy'], say=["Said I've got six colours. It said it's got seven. Showoff.", "Lost on colours. I'm mostly yellow. Orange. A bit orange."])
    o.r('shout_for_the_sun_to_come_out_and_finish_it', 'Shouting for the sun to come out and finish the job, wings flung to the sky, at the full pitch of his bill', 14, 'none',
        [k(.14, x=.4, y=-.5, b=-.4), k(.34, x=1.6, y=-1.9, b=-1.3, w=1, mark='SUN!'), k(.58, x=1.7, y=-2.1, b=-1.5, w=1, l=1, mark='SUUUN!'), k(.84, x=-.3, y=.2, eye='-')],
        [], g='show', far=True, act=('shout', 'rainbow'), prefer=['sad', 'grumpy'], say=["Sun, come out. You're half done. We're all watching.", "Bellowed at the sky. Sky said drizzle. Sky's got range."])
    o.r('sing_the_colour_song_one_note_per_stripe', 'Singing the colour song to the charm one note per stripe, climbing up the notes on tiptoe and coming back down', 24, 'none',
        [k(.12, x=.2, y=.2, b=.6), k(.28, x=.3, y=-.3, b=.2, w=.2, mark='do'), k(.4, x=.4, y=-.6, b=-.2, w=.4, l=1, mark='re'), k(.52, x=.5, y=-1.0, b=-.7, w=.7, mark='mi'), k(.66, x=.4, y=-.5, b=-.1, w=.4, r=1, mark='so'), k(.82, x=.3, y=.2, b=.5, eye='^', mark='do')],
        [], g='show', act=('sing', 'colours'), prefer=['happy', 'lonely'])
    # ---------------- mishap
    o.r('push_his_head_into_the_seam_for_a_closer_look_and_stick', 'Pushing his head into the door seam for a closer look at the arch and sticking there until a hard pull frees him', 22, 'none',
        [k(.12, x=.5, y=-.7, b=.2), k(.3, 'seam_lo', x=1.1, y=-.6, b=.8, mark='hmm'), k(.48, 'seam_lo', x=1.4, y=-.6, b=1.0, l=1, r=1, eye='@', mark='mrrf'), k(.66, 'seam_lo', x=1.6, y=-.7, b=1.4, w=.9, mark='POP'), k(.84, x=-1.2, y=.7, b=.6, eye='@')],
        [], g='mishap', act=('stuck', 'seam'), shown='head', ages=GROWN, prefer=['curious', 'grumpy'])
    o.r('slip_on_the_wet_foot_of_the_case_and_end_in_a_rainbow_of_arms_and_legs', 'Slipping on the wet foot of the case and ending in a tangle of wings and legs along the slats', 18, 'none',
        [k(.14, 'slat_h', x=.3, y=.4, b=.4, r=1), k(.3, x=1.0, y=-.5, b=-1.0, w=1, l=1, r=1, eye='O', mark='WAAH'), k(.48, 'slat_k', x=1.5, y=1.7, b=1.9, w=.8, eye='@', mark='splat'), k(.8, x=.4, y=.7, b=.7, eye='-')],
        [], g='mishap', act=('slip', 'wetness'), when=['obj_wetness>.3'], prefer=['young'])
    o.r('bump_the_glass_while_staring_at_the_bands', 'Bumping the glass in the dark while staring at the bands, and bouncing back a step', 14, 'none',
        [k(.14, x=.8, y=-.9, b=.1), k(.3, x=1.1, y=-1.3, b=.3, eye='O'), k(.46, 'trim_r', x=1.9, y=-.5, b=1.4, eye='@', mark='bonk'), k(.62, x=-1.2, y=.4, b=-.9, w=.8, eye='@'), k(.84, x=.1, y=.4, b=.4, eye='>')],
        [], g='mishap', act=('walk_into', 'glass'), when=['night'], ages=['duckling', *GROWN])
    o.r('stamp_the_empty_ground_where_the_pot_should_be', 'Stamping the ground where the pot should be, once, twice, a third time, and not a clink to be heard', 16, 'none',
        [k(.14, 'rail_rr', x=.3, y=.5, b=.5, l=1), k(.3, 'rail_rr', x=.4, y=.8, b=1.2, l=1, mark='STOMP'), k(.46, x=-.4, y=-.4, b=-.9, r=1, w=.6), k(.62, 'rail_rr', x=.4, y=.8, b=1.3, r=1, mark='STOMP'), k(.8, 'rail_rr', x=.4, y=.9, b=1.4, l=1, eye='-', mark='stomp')],
        [], g='mishap', act=('stamp', 'pot'), prefer=['grumpy', 'young'])
    o.r('trip_over_the_end_stud_chasing_a_gleam', 'Stumbling at the end stud while chasing a gleam, catching a toe and limping about on the other foot', 16, 'none',
        [k(.14, 'stud_r', x=.7, y=.2, b=-.5, w=.4, l=1), k(.3, 'stud_r', x=1.5, y=.6, b=1.1, l=1, eye='O', mark='yoink'), k(.5, x=-.5, y=-.7, b=-1.4, w=1, r=1, eye='@', mark='OW'), k(.7, x=.4, y=.7, b=.7, l=1, eye='>'), k(.88, eye='-')],
        [], g='mishap', act=('hook', 'stud'), prefer=['young'])
    o.r('lose_his_balance_on_the_rail_bridge_and_drop_to_the_slats', 'Losing his balance on his rail bridge and dropping flat to the slats with both wings out like a fallen rainbow', 18, 'none',
        [k(.14, 'rail', x=.3, y=-.3, b=-.8, w=.8, l=1), k(.32, 'rail', x=.5, y=-.7, b=-1.2, w=1, r=1, eye='O', mark='eep'), k(.5, 'slat_f', x=1.4, y=1.9, b=2.0, w=1, eye='@', mark='plop'), k(.8, x=.3, y=.6, b=.7, w=.4, eye='-')],
        [], g='mishap', act=('balance', 'bridge'), prefer=['young', 'happy'])
    # ---------------- duets (a friend takes their own part)
    o.r('stand_shoulder_to_shoulder_as_the_two_legs_of_one_arch', 'Standing shoulder to shoulder with a friend as the two legs of one arch, wings joined overhead in a curve', 26, 'none',
        [k(.12, 'stud_l', x=.3, y=.2, b=.5, l=1), k(.3, 'stud_l', x=.5, y=-.6, b=-.3, w=.8), k(.5, 'stud_l', x=.6, y=-1.1, b=-.7, w=1, mark='...'), k(.7, 'stud_l', x=.5, y=-.7, b=-.3, w=.8, eye='^'), k(.86, x=.2, y=.2, b=.3)],
        [(.5, 'mates')], g='show', act=('stack', 'arch'), prefer=['happy', 'lonely'],
        duo=[k(.12, 'slat_f', x=.3, y=.2, b=.5, r=1), k(.32, 'slat_f', x=.5, y=-.6, b=-.3, w=.8), k(.52, 'slat_f', x=.6, y=-1.1, b=-.7, w=1), k(.72, 'slat_f', x=.5, y=-.7, b=-.3, w=.8, eye='^'), k(.88, x=.2, y=.2, b=.3)],
        say=["Two legs, one arch, no pot. Nobody expected a pot.", "Held the arch together. Mine held better. Obviously."])
    o.r('hop_the_stripes_in_turn_calling_the_colours', 'Hopping the stripes at the foot of the case in turn with a friend, calling out each one as he lands', 26, 'none',
        [k(.1, 'slat_g', x=.4, y=-.2, b=.4), k(.24, 'slat_g', x=.6, y=-.5, b=-1.1, w=.5, l=1, mark='red?'), k(.38, 'slat_h', x=.4, y=.3, b=.5), k(.54, 'slat_h', x=.6, y=-.5, b=-1.2, w=.5, r=1, mark='blue?'), k(.72, 'slat_k', x=.4, y=.3, b=.5, eye='^')],
        [], g='play', act=('hop', 'stripes'), prefer=['happy', 'young'],
        duo=[k(.12, 'slat_j', x=.4, y=.3, b=.5), k(.3, 'slat_j', x=.4, y=.3, b=.5), k(.46, 'slat_l', x=.6, y=-.5, b=-1.1, w=.5, r=1, mark='green?'), k(.64, 'slat_l', x=.4, y=.3, b=.5), k(.82, 'slat_l', x=.6, y=-.5, b=-1.2, w=.5, l=1, eye='^')])
    o.r('hold_the_charm_out_so_a_friend_can_pick_a_stripe', 'Lifting the charm out and holding it low so a friend can point at a favourite stripe, while he argues for another', 26, 'none',
        [k(.1, x=.6, y=-.7, b=-.2), k(.22, 'item', x=.9, y=-1.0, b=.8, mark='hup'), k(.4, 'item', x=1.9, y=-1.4, b=-.7, eye='O'), k(.58, 'item', x=1.0, y=1.0, b=1.4, l=1, eye='>', mark='no, that one'), k(.76, 'item', x=.9, y=-1.0, b=.8), k(.9, eye='^')],
        [], g='use', act=('fit', 'stripes'), ages=GROWN, prefer=['happy', 'lonely'], obj=[(.22, dict(hold=0)), (.4, dict(hold=1)), (.64, dict(hold=1)), (.78, dict(hold=1)), (.88, dict(hold=0))],
        duo=[k(.2, x=.3, y=-.3), k(.42, 'slat_b', x=.9, y=.3, b=.5, eye='o'), k(.6, 'slat_b', x=.9, y=-.3, b=.3, w=.5, r=1, eye='O', mark='this one'), k(.8, x=-.2, y=-.3, w=.4, eye='^')])
    o.r('play_tag_round_the_foot_of_the_case', 'Playing tag at the foot of the case with a friend, a lap each way, and always being it', 26, 'none',
        [k(.1, 'rail_l', x=.4, y=.3, b=.4, l=1), k(.26, 'rail', x=1.1, y=.1, b=-.5, w=.5, r=1), k(.42, 'rail_r', x=1.4, y=0, b=-.6, w=.7, l=1, mark='tag'), k(.58, 'rail', x=-.8, y=.2, b=-.5, w=.6, r=1), k(.76, 'rail_l', x=.3, y=.4, b=.5, eye='>')],
        [], g='play', act=('chase', 'partner'), prefer=['happy', 'young'],
        duo=[k(.1, 'rail', x=.3, y=.2, b=.4, r=1), k(.28, 'rail_r', x=.9, y=.1, b=-.5, w=.5, l=1), k(.44, 'rail_rr', x=1.2, y=0, b=-.6, w=.6, r=1), k(.6, 'rail_r', x=-.6, y=.2, b=-.4, w=.5, l=1), k(.8, 'rail', x=.3, y=.3, b=.5, eye='^')],
        say=["Tag. Still it. Been it since morning. It's a career.", "Chased a friend round the foot. Nobody caught anybody. Perfect."])
    # @@r_end
    return done(o)


if __name__ == '__main__':
    for n in sys.argv[1:] or ['earth_token', 'sky_token', 'water_token', 'magpie_friendship_charm', 'rainbow_charm', 'dance_medal']:
        globals()[n]().emit(need=COUNT_NEED.get(n))
