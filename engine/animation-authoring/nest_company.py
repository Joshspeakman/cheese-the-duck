"""Complementary actions at the outside edge of an occupied nest."""
import json
from pathlib import Path

def k(at,**pose):return dict(at=at,**pose)
def score(label,anchor,cores,track,lead=None):
    return dict(label=label,anchor=anchor,cores=cores,track=[k(0),*track,k(1)],
                lead=[k(0),*(lead or [k(.7,eye='^'),k(.9,eye='^')]),k(1)])

SCORES={
 'left_rim':score('Holding the left rim while Cheese tucks the loose ends','left',
     ['tuck_left_edge','mend_gap'],[
     k(.12,y=1,w=.3,reach=.25),k(.25,y=1.3,w=.65,reach=.7,contact=.9),
     k(.48,y=1,w=.8,reach=1,contact=1,eye='>'),k(.72,y=.8,w=.65,reach=.8,contact=1),
     k(.84,y=-.3,w=.3,reach=.2,eye='^'),k(.94,y=.4,eye='^')]),
 'right_rim':score('Steadying the outer rim while Cheese braces and tucks it','right',
     ['tuck_right_edge','crossbrace_twig','tighten_braid'],[
     k(.13,x=.3,y=.7,w=.4,reach=.3),k(.3,y=1.4,w=.7,reach=.9,contact=1),
     k(.52,x=.5,y=1.2,w=.8,reach=1,contact=1),k(.76,y=1,w=.7,reach=.9,contact=1),
     k(.88,y=-.4,w=.2,eye='^')]),
 'weave_tension':score('Keeping the outer braid steady through Cheese’s over-and-under weave','right',
     ['weave_rim'],[
     k(.13,y=1,w=.4,reach=.4),k(.26,y=1.4,w=.7,reach=1,contact=1),
     k(.38,y=.7,w=.5,reach=.8,contact=1),k(.48,y=1.5,w=.8,reach=1,contact=1),
     k(.6,y=.7,w=.5,reach=.8,contact=1),k(.76,y=1.4,w=.8,reach=1,contact=1),
     k(.87,y=-.3,w=.3,eye='^')]),
 'lining_fan':score('Fanning loose fibres toward Cheese as he fluffs the lining','right',
     ['fluff_center','widen_bowl','bedtime_tuck'],[
     k(.16,y=.8,w=.2),k(.28,y=-.3,w=1.1),k(.43,y=.9,w=.25),
     k(.57,y=-.4,w=1.2),k(.72,y=.6,w=.3),k(.88,y=-.2,w=.7,eye='^')]),
 'tamp_rhythm':score('Counting and tapping along while Cheese pats the bedding','right',
     ['tamp_floor','toe_trace','tail_wriggle'],[
     k(.15,y=.8,l=1),k(.25,b=.3,mark='1'),k(.4,r=1,y=.5),
     k(.55,b=.4,mark='2'),k(.7,l=1,w=.4),k(.82,b=.4,mark='3',eye='^'),k(.93,y=.4,eye='^')]),
 'lining_inspect':score('Leaning in to admire the feather and leaf arrangement','right',
     ['straighten_feather','leaf_underlay','spring_feather','fall_leaf_catch','polish_pebble','bowl_test'],[
     k(.15,x=.2,y=1),k(.32,x=.6,y=1.6,eye='O'),k(.48,x=-.4,y=-.3),
     k(.64,x=.5,y=1.3,w=.25),k(.8,y=-.4,w=.6,eye='^'),k(.93,y=.5)]),
 'quiet_guard':score('Keeping quiet company beside Cheese’s resting place','right',
     ['curl_sleep','one_eye_guard','dream_paddle','long_yawn','foot_tuck','chin_on_rim','satisfied_sigh','shy_hide','cold_huddle','noon_doze','moon_watch'],[
     k(.15,x=-.4,y=.6),k(.32,x=-.8,y=-.4,eye='>'),k(.5,x=.4,y=.8,eye='-'),
     k(.68,x=-.7,y=-.5,eye='>'),k(.83,x=.3,y=.6,eye='^')],
     [k(.25,eye='-'),k(.55,eye='-'),k(.85,eye='-')]),
 'summer_fan':score('Sharing a gentle cooling breeze beside the nest','right',
     ['heat_fan'],[
     k(.14,y=-.5,w=.3,gape=.3),k(.3,w=1.1,y=.5),k(.44,w=.2,y=-.4),
     k(.58,w=1.2,y=.5),k(.72,w=.25,y=-.3),k(.87,w=.9,eye='^')]),
 'young_support':score('Steadying the rim for a small duck’s careful tuck','right',
     ['tuck_right_edge','crossbrace_twig','tighten_braid','weave_rim'],[
     k(.1,y=1,w=.3,reach=.3),k(.24,y=1.7,w=.7,reach=1,contact=1,eye='^'),
     k(.46,y=1.4,w=.6,reach=.9,contact=1),k(.7,y=1.6,w=.7,reach=1,contact=1),
     k(.84,y=.6,w=.3,eye='^'),k(.94,y=.9,eye='^')]),
 'patient_company':score('Waiting patiently beside Cheese’s unhurried nest work','right',[],[
     k(.17,y=.6,eye='-'),k(.36,x=.3,y=1.1),k(.55,x=.5,y=1.4,w=.2),
     k(.74,y=.5,eye='^'),k(.9,y=-.2,eye='^')]),
 'hover_observer':score('Hovering beside the nest to watch Cheese work','right',[],[
     k(.15,y=-.4,w=.8),k(.33,x=.3,y=.5,w=.3),k(.51,x=.4,y=.8,w=.7),
     k(.7,x=-.3,y=-.4,w=.4),k(.88,y=.3,w=.8,eye='^')]),
}
if __name__=='__main__':
    target=Path(__file__).resolve().parents[1]/'client/animation/nest-company.json'
    target.write_text(json.dumps(SCORES,indent=2)+'\n')
    print(f'Wrote {len(SCORES)} nest companion scores')
