"""Merge real follow-up evidence only into previously refused matrix cases.

No frame geometry is rewritten. Sources retain their original hash-linked reports.
"""
import argparse,copy,hashlib,json,subprocess
from pathlib import Path


def load(path):
    raw=path.read_bytes();manifest=json.loads(raw)
    assert manifest['schema_version']==1 and manifest['result']=='PASS'
    frames_path=path.parent/manifest['frames_file'];payload=frames_path.read_bytes()
    assert hashlib.sha256(payload).hexdigest()==manifest['frames_sha256']
    frames=json.loads(payload);cases={c['id']:c for c in manifest['cases']}
    assert len(cases)==len(manifest['cases'])
    assert all(f['_airMatrixCase'] in cases and cases[f['_airMatrixCase']]['status']=='supported' for f in frames)
    return manifest,frames,dict(manifest_file=path.name,manifest_sha256=hashlib.sha256(raw).hexdigest(),frames_file=frames_path.name,frames_sha256=manifest['frames_sha256'],metrics_sha256=manifest.get('metrics_sha256'))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('primary',type=Path);ap.add_argument('followups',type=Path,nargs='+');ap.add_argument('--prefix',required=True);ap.add_argument('--primary-origin',type=float,nargs=2,required=True);ap.add_argument('--revision-score',action='append',default=[]);ap.add_argument('--baseline-revision',default='322afda');ap.add_argument('--cheese-origin',type=float,nargs=2,default=[44.,26.]);args=ap.parse_args()
    primary,frames,source=load(args.primary);cases={c['id']:copy.deepcopy(c) for c in primary['cases']};sources=[source];checks=primary['checks'];superseded=[]
    for case in cases.values():
        for attempt in case['attempts']:attempt.setdefault('source_manifest',args.primary.name)
    for case in cases.values():
        for attempt in case['attempts']:
            attempt.setdefault('operator_root',args.primary_origin);attempt.setdefault('cheese_root',args.cheese_origin)
    for path in args.followups:
        followup,new_frames,source=load(path);sources.append(source);checks+=followup['checks']
        for new in followup['cases']:
            old=cases[new['id']]
            if old['status']=='supported':
                assert new['score'] in args.revision_score,'Completed evidence needs an explicit authored-score revision'
                removed=[f for f in frames if f['_airMatrixCase']==new['id']]
                superseded.append(dict(case=copy.deepcopy(old),frames=len(removed),reason='Authored '+new['score']+' geometry revised; actual native run repeated'))
                frames=[f for f in frames if f['_airMatrixCase']!=new['id']]
            case=copy.deepcopy(new)
            approach=next((f['living']['plan']['carnival_work'] for f in new_frames if f['_airMatrixCase']==case['id'] and f.get('_physicalCase')=='accepted approach'),None)
            for attempt in case['attempts']:
                attempt.setdefault('source_manifest',path.name)
                if approach:
                    # This fixture initializes the same actual roots before
                    # each candidate placement; the accepted snapshot binds it.
                    attempt.setdefault('operator_root',approach['physical']['root'])
                    attempt.setdefault('cheese_root',approach['shared']['cheese']['root'] if case['mode']=='shared' else approach['physical']['root'])
            case['attempts']=old['attempts']+case['attempts'];cases[new['id']]=case
        frames.extend(new_frames)
    root=Path(__file__).resolve().parent.parent
    baseline_raw=subprocess.check_output(['git','show',args.baseline_revision+':engine/client/animation/castle-air-metrics.json'],cwd=root);baseline=json.loads(baseline_raw)
    baseline_sha=hashlib.sha256(baseline_raw).hexdigest()
    for source in sources:
        if not source['metrics_sha256']:source.update(metrics_sha256=baseline_sha,metrics_provenance='Frozen native matrix inputs from '+args.baseline_revision)
    current=json.loads((root/'engine/client/animation/castle-air-metrics.json').read_text())
    assert baseline['observation']==current['observation'],'Unreviewed observation hardware change'
    def geometry(data,case):
        entry=data['ages'][case['age']] if case['adapter']=='cheese' else data['casts'][case['cast']]
        return hashlib.sha256(json.dumps(dict(events=entry['routines'][case['score']],travel=entry['travel']),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    routines=json.loads((Path(__file__).parent/'client/animation/castle-care.json').read_text())
    for case in cases.values():
        rows=[f for f in frames if f['_airMatrixCase']==case['id']]
        if case['status']=='refused':
            assert not rows and case.get('reason') and case['attempts'];continue
        actual_geometry=geometry(current,case)
        assert case.get('geometry_sha256',geometry(baseline,case))==actual_geometry,'A changed geometry dependency lacks a new native run'
        case['geometry_sha256']=actual_geometry
        if case['mode']=='shared':assert baseline['ages'][case['age']]['travel']==current['ages'][case['age']]['travel'],'Observer envelope changed without revalidation'
        assert rows and case.get('center') and case.get('placement')
        selected=next(a for a in reversed(case['attempts']) if a['accepted'])
        # A solo operator IS Cheese; only a shared case has a separate watching
        # Cheese root, and the replay validator binds exactly what is recorded.
        case['origin']=dict(operator=selected['operator_root'])
        if case['mode']=='shared':case['origin']['cheese']=selected['cheese_root']
        approach=next(f for f in rows if f.get('_physicalCase')=='accepted approach')['living']['plan']['carnival_work']
        assert approach['physical']['root']==case['origin']['operator']
        if case['mode']=='shared':assert approach['shared']['cheese']['root']==case['origin']['cheese']
        assert {f['_physicalEvent'] for f in rows if '_physicalEvent' in f}==set(range(len(routines[case['score']]['effects'])))
        if case['adapter']=='regular':
            # Every fixture creates a fresh Stranger visit, whose authored
            # duration is120 seconds. No completed run may outlive that visit.
            assert case['seconds']<case.get('visit_duration_seconds',120)
        elif case['adapter']=='rare':assert case['seconds']<case['remaining_seconds']-6
    output=args.primary.parent;frames_file=args.prefix+'-frames.json';payload=json.dumps(frames)
    (output/frames_file).write_text(payload)
    result=dict(schema_version=1,result='PASS',scope=primary['scope'],checks=checks,frames=len(frames),frames_file=frames_file,frames_sha256=hashlib.sha256(payload.encode()).hexdigest(),sources=sources,baseline_revision=args.baseline_revision,baseline_metrics_sha256=baseline_sha,metrics_sha256=hashlib.sha256((root/'engine/client/animation/castle-air-metrics.json').read_bytes()).hexdigest(),superseded_cases=superseded,cases=list(cases.values()))
    (output/(args.prefix+'-manifest.json')).write_text(json.dumps(result,indent=2))
    print(json.dumps(dict(result='PASS',cases=len(cases),supported=sum(c['status']=='supported' for c in cases.values()),refused=sum(c['status']=='refused' for c in cases.values()),frames=len(frames),checks=checks)))


if __name__=='__main__':main()
