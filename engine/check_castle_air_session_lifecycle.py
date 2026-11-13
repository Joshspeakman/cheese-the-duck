"""Independent public air-procedure sessions through actual DesktopGame ordering.

The shared disposable fixture isolates unrelated ambient decisions, while the
actual Cheese/regular/rare movers, host dispatch and native mechanisms run.
"""
import copy
import json
import sys
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from engine import check_castle_air_lifecycle as h
from engine import carnival, castle_work as castle, castle_air_session as sessions
from engine import castle_air_roles as roles


@contextmanager
def clocks():
    with h.controlled_clocks(), patch.object(roles,'datetime',h.SimDatetime):
        yield


def request(score='castle_pressure_check',mode='solo',material=None):
    base=dict(vent=0.,hose=0.,kink=0.,dust=0.,motor='on',power_hold=False,
              powered=True,rotor_speed=1.,pressure=.45)
    base.update(material or {})
    pond,iid,obj,key=h.fixture(mode,material=base,long_visit=True)
    if mode=='flight':
        h.game.renderer.duck_pos.x,h.game.renderer.duck_pos.y=60.,26.
    if h.game.friends.current_visit:
        h.game.friends.current_visit.started_at=h.SimDatetime.now().isoformat()
        pond.minds.sync()
        pond.minds.tasks[key]=dict(action='observe',until=pond.minds.now+1000,
                                  context=pond.minds.context(key))
    before=h.ownership(pond,obj)
    ok,reason=carnival.request(pond,'bounce_house',score,iid,together=mode!='solo')
    h.check(ok,mode+' '+score+': public procedure acquisition: '+reason)
    plan=pond.state['plan'];work=plan['carnival_work'];owner=sessions.session(pond,plan)
    h.check(owner is not None and owner.work is work and work['id']==score and plan['phase']=='act',
            mode+': one private session owns the unchanged outer procedure and active service clock')
    return pond,plan,work,obj,key,owner,before


def step_to_beat(work,dt=.2):
    child=work.get('atomic')
    if child:
        due=[at*castle.ROUTINES[child['id']]['duration']-child['clock']
             for i,(at,_,_) in enumerate(castle.ROUTINES[child['id']]['effects'])
             if i not in child['events'] and at*castle.ROUTINES[child['id']]['duration']>child['clock']]
        if due:dt=min(dt,min(due))
    h.step(dt)


def complete_case(score,mode='solo',material=None,capture=None):
    pond,plan,work,obj,key,owner,_=request(score,mode,material)
    before=h.rewards(pond,obj,key)
    initial_shell=h.actual_egg() if mode=='egg' else None
    actual_reads=[];effects=[];pending=[];apply=castle.apply

    def capture_frame(label):
        if capture is None:return
        capture(dict(label=label,score=score,mode=mode,session_phase=owner.phase,
                     occurrence=work['air_procedure']['current_occurrence'],
                     events=copy.deepcopy(pending),work=copy.deepcopy(work),
                     operator=copy.deepcopy(owner.actual(owner.operator)),
                     observer=copy.deepcopy(owner.actual(owner.observer)) if owner.observer else None,
                     scene=h.snapshot(h.game,h.game.renderer)))

    def record_apply(target,child,index,effect):
        record=None
        if target is obj:
            actual=owner.actual(owner.operator)
            effects.append((child['occurrence_id'],index,effect[1]))
            record=dict(occurrence_id=child['occurrence_id'],atomic_id=child['id'],index=index,
                        clock=child['clock'],field=effect[1],value=effect[2],
                        actual_operator=copy.deepcopy(actual),before=copy.deepcopy(target['castle']))
            assert owner.op['phase']=='hold' and h.close_points(actual['root'],owner.op['root']), 'effect without actual published operator hold'
            if effect[1]=='inspection':
                actual_reads.append((child['occurrence_id'],round(target['castle']['pressure'],3)))
                assert owner.op['observation_ready'] is True and owner.op['contact_ready'] is False,'gauge read without actual observation authority'
        result=apply(target,child,index,effect)
        if record is not None:
            record['after']=copy.deepcopy(target['castle']);pending.append(record)
        return result

    phases=[];frame_count=0
    capture_frame('initial')
    with patch.object(castle,'apply',record_apply):
        for _ in range(2400):
            if pond.state.get('plan') is not plan:break
            pending.clear()
            previous=(owner.phase,work['air_procedure']['current_occurrence'],owner.op['phase'],owner.op['station_index'])
            step_to_beat(work);frame_count+=1
            if not phases or phases[-1]!=owner.phase:phases.append(owner.phase)
            if not work.get('recorded'):
                assert h.rewards(pond,obj,key)==before,'procedure emitted an intermediate generic, social or learning reward'
            if mode=='egg':assert h.actual_egg()==initial_shell,'session moved or turned the stationary egg'
            if pond.state.get('plan') is plan:
                projected=h.snapshot(h.game,h.game.renderer)['living']['plan']['carnival_work']
                assert projected['id']==score and projected.get('air_procedure'),'post-host session snapshot lost its native binding'
                assert '_journal' not in json.dumps(projected),'private execution history escaped into scene'
            current=(owner.phase,work['air_procedure']['current_occurrence'],owner.op['phase'],owner.op['station_index'])
            if pending:
                child=work.get('atomic')
                assert child and child['clock']==pending[-1]['clock'],'actual frame did not stop at native event boundary'
                capture_frame('native_event')
            elif current!=previous:capture_frame('phase_or_occurrence')
        else:raise AssertionError('public procedure timed out: '+repr((owner.phase,work)))
    h.check(work.get('recorded') is True and not work.get('interrupted'),
            mode+' '+score+': complete actual session: '+str(work.get('physical_error')))
    h.check(owner.completed and owner.receipt and owner.phase=='done' and not pond.minds.carnival_guests and sessions.session(pond) is None,
            mode+': final receipt releases the exact session and guest lease')
    h.check(owner.receipt['observations'] and [(r['occurrence_id'],r['pressure']) for r in owner.receipt['observations']]==actual_reads,
            mode+': whole receipt retains actual independently numbered gauge observations')
    h.check(len(effects)==len(set(effects)) and h.close_points(owner.actual(owner.operator)['root'],owner.contract['origin']),
            mode+': child effects consume once and actual operator returns to original root')
    if owner.observer:
        h.check(h.close_points(owner.actual(owner.observer)['root'],owner.watch['exit']) and
                phases.index('operator_exit')<phases.index('observer_exit'),
                mode+': independently moved observer exits after the actual operator')
    after=h.rewards(pond,obj,key)
    reader=owner.operator['actor'];counts=pond.minds.model.residents[reader]['counts'];old=before['brains'][reader]['counts']
    h.check(counts['observe']-old['observe']==len(actual_reads) and
            counts['practice']-old['practice']==int(bool(owner.receipt['mechanical_contacts'])) and
            counts['share']-old['share']==int(mode!='solo'),
            mode+': reader receives only demonstrated observation/practice and completed shared participation')
    h.check(after['uses']==before['uses'] and after['needs']==before['needs'] and after['skills']==before['skills'] and
            obj['carnival_routines']=={score:1},
            mode+': one outer history and no generic uses, needs, skills or child completion history')
    if mode=='egg':h.check(h.egg_credit(pond)==before['egg'],'stationary egg receives no model/action/observation reward')
    if owner.observer:
        watcher=owner.observer['actor'];counts=pond.minds.model.residents[watcher]['counts'];old=before['brains'][watcher]['counts']
        h.check(counts['observe']==old['observe']+1 and counts['share']==old['share']+1 and counts['practice']==old['practice'],
                mode+': observer receives watching/shared experience without mechanical practice')
    pending.clear();capture_frame('final')
    pond._complete(plan)
    h.check(h.rewards(pond,obj,key)==after,mode+': duplicate consumed-plan callback grants no second receipt')
    print('SESSION',mode,score,frame_count,'frames',len(effects),'effects',phases)


def until(predicate,work,label):
    for _ in range(2400):
        if predicate():return
        if work.get('interrupted'):raise AssertionError(label+': '+str(work.get('physical_error')))
        step_to_beat(work)
    raise AssertionError('session boundary timeout: '+label)


def assert_interrupted(pond,work,obj,key,before,label):
    h.check(work.get('interrupted') and not work.get('recorded') and pond.state.get('plan') is None and
            sessions.session(pond) is None and not pond.minds.carnival_guests,
            label+': drops exact live session and reservation')
    h.check(h.rewards(pond,obj,key)==before,label+': grants no partial procedure reward')


def pause_and_callback_review():
    for mode in ('solo','shared','egg','flight'):
        pond,plan,work,obj,key,owner,_=request(mode=mode)
        before=h.rewards(pond,obj,key);phase=copy.deepcopy(work['air_procedure'])
        pond._complete(plan)
        h.check(h.rewards(pond,obj,key)==before and work['air_procedure']==phase and not work.get('recorded'),
                mode+': premature whole-procedure callback cannot advance work or grant rewards')
        h.step(0)
        assert_interrupted(pond,work,obj,key,before,mode+' premature whole callback')
        pond,plan,work,obj,key,owner,_=request(mode=mode)
        before=h.rewards(pond,obj,key)
        until(lambda:bool(work['air_procedure']['observations']),work,'first real read before pause')
        reader=carnival.conversation(pond,plan,owner.operator['actor'])
        h.check(reader['role']=='operator' and len(reader['observations'])==1 and
                reader['last_read_pressure']==work['air_procedure']['observations'][0]['pressure'],
                mode+': public operator context contains only its actual archived reading')
        if owner.observer:
            watcher=carnival.conversation(pond,plan,owner.observer['actor'])
            h.check(watcher['role']=='observer' and watcher['observations']==[] and watcher['last_read_pressure'] is None,
                    mode+': observer context cannot claim to have read the dial')
        if mode=='egg':h.check(carnival.conversation(pond,plan,'cheese') is None,'stationary egg has no verbal operator or observer context')
        original=copy.deepcopy(work['air_procedure']);child=copy.deepcopy(work.get('atomic'))
        roots=[copy.deepcopy(owner.actual(a)['root']) for a in (owner.operator,owner.observer) if a]
        plan['paused']=True;h.game.duck.current_action='feed';h.game.renderer.duck_pos.set_state_by_name('eating',0)
        for _ in range(4):h.step()
        h.check(work['air_procedure']==original and work.get('atomic')==child and
                roots==[owner.actual(a)['root'] for a in (owner.operator,owner.observer) if a] and
                h.game.renderer.duck_pos.get_state()=='eating' and not owner.op['observation_ready'],
                mode+': pause with care keeps actual roots, child history and care pose')
        h.game.duck.current_action=None
        h.game.duck.growth_stage='hatchling' if mode=='egg' else 'elder'
        h.step(0)
        assert_interrupted(pond,work,obj,key,before,mode+' growth while paused after consumed reading')
        h.check(work['air_procedure']==original and obj['castle_inspections']['pressure']==1,
                mode+': interruption preserves consumed observation but never completes the recipe')


def ownership_review():
    for mode in ('shared','egg','flight'):
        for replace_target in (False,True):
            pond,plan,work,obj,key,owner,_=request(mode=mode)
            guest=owner.observer if mode=='flight' else owner.operator
            def moving():
                lease=pond.minds.carnival_guests[owner.guest_key]
                return not h.close_points(owner.actual(guest)['root'],lease['target'])
            until(moving,work,'real helper approach before target cleanup')
            h.step(0)
            root=copy.deepcopy(owner.actual(guest)['root']);before=h.rewards(pond,obj,key)
            target=[root[0]+2.,root[1]+1.]
            if mode=='flight':
                mover=h.game.guest_motion
                if replace_target:mover.target=tuple(target)
            else:
                mover=h.visitor_animator
                if replace_target:
                    mover._target_x=target[0]-h.game.renderer._camera_x
                    mover._target_y=target[1]-h.game.renderer._camera_y
            # Invalidation occurs before the actual host mover boundary. An
            # independent new target must survive; the old owned target stops.
            h.game.duck.growth_stage='hatchling' if mode=='egg' else 'elder'
            h.step(0)
            actual_target=list(mover.target) if mode=='flight' else [mover._target_x+h.game.renderer._camera_x,mover._target_y+h.game.renderer._camera_y]
            assert_interrupted(pond,work,obj,key,before,mode+' moving helper cleanup')
            h.check(h.close_points(actual_target,target if replace_target else root),
                    mode+': actual host cleanup '+('preserves independently replaced target' if replace_target else 'pins only the old owned target'))

    for mode in ('shared','flight'):
        pond,plan,work,obj,key,owner,_=request(mode=mode)
        before=h.rewards(pond,obj,key)
        plan['paused']=True
        h.clock+=400 if mode=='shared' else 180
        h.step(0)
        assert_interrupted(pond,work,obj,key,before,mode+' departure during pause')


def acquisition_review():
    for mode in ('solo','shared','egg','flight'):
        pond,iid,obj,key=h.fixture(mode,long_visit=True,material=dict(vent=0.,hose=0.,kink=0.,dust=0.))
        if mode=='flight':h.game.renderer.duck_pos.x,h.game.renderer.duck_pos.y=60.,26.
        if h.game.friends.current_visit:h.game.friends.current_visit.started_at=h.SimDatetime.now().isoformat()
        h.game.duck.needs.hunger=10
        if mode!='egg':h.game.renderer.duck_pos.move_to(40,27)
        before=h.ownership(pond,obj)
        ok,reason=carnival.request(pond,'bounce_house','castle_pressure_check',iid,together=mode!='solo')
        h.check(not ok and h.ownership(pond,obj)==before and sessions.session(pond) is None,
                mode+': urgent-care refusal preserves all existing roots, targets, tasks, materials and leases: '+reason)


def settled_pause_review():
    pond,plan,work,obj,key,owner,_=request(mode='shared')
    before=h.rewards(pond,obj,key);advance=owner.advance
    def pause_at_actual_exit(dt):
        advance(dt)
        if owner.phase=='done':plan['paused']=True
    with patch.object(owner,'advance',pause_at_actual_exit):
        until(lambda:owner.phase=='done',work,'actual both exits before final pause')
    roots=[owner.actual(a)['root'] for a in (owner.operator,owner.observer)]
    metadata=copy.deepcopy(work['air_procedure'])
    for _ in range(5):h.step()
    h.check(pond.state['plan'] is plan and not work.get('recorded') and not work.get('interrupted') and
            h.rewards(pond,obj,key)==before and work['air_procedure']==metadata and
            [owner.actual(a)['root'] for a in (owner.operator,owner.observer)]==roots,
            'settled pause holds both actual exits without wandering, advancing history or granting receipt')
    plan['paused']=False;h.step(0)
    h.check(work.get('recorded') and owner.completed and pond.state['plan'] is None,
            'unpaused actual settled exits complete exactly one retained receipt')


def malformed_review():
    for mode in ('shared','egg','flight'):
        for malformed in (None,'broken',dict(work=None)):
            pond,plan,work,obj,key,owner,_=request(mode=mode)
            h.step(0);before=h.rewards(pond,obj,key)
            pond.minds.carnival_guests[owner.guest_key]=malformed
            h.step(0)
            assert_interrupted(pond,work,obj,key,before,mode+' malformed lease '+repr(malformed))

    for fault in ('child_clock','outer_observation','physical_alias','boolean_version'):
        pond,plan,work,obj,key,owner,_=request()
        before=h.rewards(pond,obj,key)
        if fault=='child_clock':work['atomic']['clock']+=1
        elif fault=='outer_observation':work['air_procedure']['observations'].append(dict(pressure=1.,occurrence_id='invented'))
        elif fault=='physical_alias':work['physical']=copy.deepcopy(work['physical'])
        else:work['air_procedure']['version']=True
        h.step(0)
        assert_interrupted(pond,work,obj,key,before,'malformed '+fault)


def final_response_review():
    for fault in ('wet_exit','power_revision','pending_valve_target','growth'):
        pond,plan,work,obj,key,owner,_=request(material=dict(vent=.8,hose=.6,kink=.8))
        before=h.rewards(pond,obj,key);real_complete=owner.complete
        def changed_final_callback():
            if fault=='wet_exit':
                with patch('engine.terrain.water_at',lambda *args,**kwargs:True):return real_complete()
            if fault=='power_revision':
                castle.apply(obj,dict(id='castle_stop',events=[],automatic=False),0,(0.,'motor','off'))
                castle.apply(obj,dict(id='castle_start',events=[],automatic=False),0,(0.,'motor','on'))
            elif fault=='pending_valve_target':obj['castle']['targets']['vent']=.8
            else:h.game.duck.growth_stage='elder'
            return real_complete()
        with patch.object(owner,'complete',changed_final_callback):
            for _ in range(2200):
                if pond.state.get('plan') is None:break
                step_to_beat(work)
            else:raise AssertionError('no actual final callback for '+fault)
        assert_interrupted(pond,work,obj,key,before,'changed final '+fault)


def reload_review():
    from engine.living_world import LivingPond
    pond,plan,work,obj,key,owner,_=request(material=dict(vent=.8,hose=.6,kink=.8))
    until(lambda:obj['castle']['targets']['vent']==.35,work,'first actual valve movement before reload')
    saved=json.loads(json.dumps(pond.save()))
    h.check('_journal' not in json.dumps(saved),'save excludes private session and execution journal')
    recorded=copy.deepcopy(saved['plan']['carnival_work']);root=h.cheese_root()
    restored=LivingPond(saved)
    h.check(restored.state['plan'] is None and sessions.session(restored) is None,
            'loading strips the saved procedure instead of reconstructing live ownership')
    h.game.living_pond=restored
    try:
        restored.attach(h.game,offline=False)
        loaded=restored.object_state('bounce_house',plan['instance'])
        h.check(loaded['castle']['targets']['vent']==.35 and not loaded['carnival_routines'] and loaded['uses']==0 and
                not restored.minds.carnival_guests and h.cheese_root()==root,
                'reload retains actual partial valve work without root snapping or completion reward')
        restored._complete(plan)
        h.check(not loaded['carnival_routines'] and recorded['air_procedure']['current_occurrence']=='seal_valve',
                'stale pre-load callback cannot fabricate a private session or receipt')
    finally:
        restored.minds.close();h.game.living_pond=pond
        pond.cancel()


if __name__=='__main__':
    try:
        h.start_test_game()
        frames=[]
        with clocks():
            cases=[] if '--boundaries' in sys.argv else [('castle_pressure_check','solo',None)] if '--smoke' in sys.argv else [
                ('castle_pressure_check','solo',None),
                ('castle_pressure_check','solo',dict(vent=.8,hose=.6,kink=.8)),
                ('castle_dust_service','solo',dict(dust=.8,hose=.6,kink=.8)),
                ('castle_pressure_check','shared',None),
                ('castle_pressure_check','shared',dict(vent=.8,hose=.6,kink=.8)),
                ('castle_dust_service','shared',dict(dust=.8,hose=.6,kink=.8)),
                ('castle_pressure_check','egg',None),
                ('castle_dust_service','egg',dict(dust=.8,motor='off',power_hold=True,powered=False,rotor_speed=0.)),
                ('castle_pressure_check','flight',None),
                ('castle_dust_service','flight',None),
            ]
            for score,mode,material in cases:
                complete_case(score,mode,material,frames.append if '--capture' in sys.argv else None)
            if '--smoke' not in sys.argv:
                pause_and_callback_review();malformed_review();final_response_review();reload_review()
                ownership_review();acquisition_review();settled_pause_review()
        if '--capture' in sys.argv:
            path=h.ROOT/'artifacts/animation-milestone/castle-air-session-lifecycle-frames.json'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(dict(schema_version=1,source='actual DesktopGame update; real event-boundary dt, no pose/root rewrite',frames=frames),indent=2)+'\n')
            print('CAPTURE',path,len(frames),'actual source frames')
        print('PASS public castle air session lifecycle: '+str(len(h.checks))+' checks')
    finally:
        h.game.living_pond.minds.close()
        if getattr(h.game,'_save_executor',None):h.game._save_executor.shutdown(wait=True)
