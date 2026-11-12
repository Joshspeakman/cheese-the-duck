"""Pure animator regression: no saves, game state, or movement substitutes."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from duck.animator import DuckAnimator

checks=[]
def check(value,label):
    assert value,label
    checks.append(label)

for directed in (False,True):
    p=DuckAnimator(x=40,y=25,play_width=132,play_height=42);p.facing_right=False;calls=[]
    if directed:p.move_to(45,28,lambda data:calls.append(data),'old arrival')
    else:p.target_x=45;p.target_y=28;p._state_str='walking'
    p.facing_right=False;p._idle_timer=100;p.frozen=True
    for dt in (.3,3,30):
        p.update(dt)
        check((p.x,p.y,p.facing_right)==(40,25,False),'frozen root/facing stays exact')
        check(not p._is_directed_movement and not p._is_moving and (p.target_x,p.target_y)==(40,25),'frozen update discards movement')
        check(not calls and p._movement_callback is None and p._original_position is None,'frozen update drops callbacks and return intent')
    p.move_to(48,30,lambda _:calls.append('frozen'))
    check((p.target_x,p.target_y)==(40,25),'frozen move_to cannot install a new destination')
    p.frozen=False;p.update(.3)
    check((p.x,p.y)==(40,25) and not calls,'thaw does not resume stale movement or callback')
    p.move_to(41,25,lambda _:calls.append('new'))
    p.update(.3);p.update(.3)
    check((p.x,p.y)==(41,25) and calls==['new'],'fresh movement after thaw works once')

p=DuckAnimator(x=40,y=25,play_width=132,play_height=42);p.set_state_by_name('sleeping',0);p.facing_right=False;p.frozen=True
frame=p.animation_frame;p.update(.3)
check(p._state_str=='sleeping' and p.animation_frame!=frame,'intentional stationary animation continues')
check((p.x,p.y,p.facing_right)==(40,25,False),'stationary animation never changes root/facing')
p.set_state_by_name('sleeping',.1);p._state_start_time-=60;p.target_x=80;p.target_y=30
for _ in range(3):
    p.update(1000)
    check((p.x,p.y,p.facing_right)==(40,25,False),'expired animation cannot fall through to frozen movement')
check(p._state_str=='idle' and p._idle_timer==0,'expired frozen animation leaves no accumulated wander timer')
print('PASS frozen animator: '+str(len(checks))+' checks')
