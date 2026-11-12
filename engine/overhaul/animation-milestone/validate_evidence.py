#!/usr/bin/env python3
"""Read-only scope/evidence audit; never edits trackers or certifies semantic truth.

Catalogues are generated JSON exports (parsed as data, never executed). Optional
repertoires/*.json use schemaVersion/objectId and candidates[] or sequences[].
*.candidates.json is source-only and cannot claim acceptance. An optional
 evidence-index.json has schemaVersion:1, artifacts:[{id,objectId,sequenceId,
kind,path,sha256,provenance:{producer,command,sourceRevision,dependencies,
fixture:{disposable:true},productionEntry}}]. Paths are repository-relative;
dependencies maps paths to SHA256. No index means no runtime evidence.

Verified sequence claims additionally require requiredBindings/completedBindings,
unresolvedBindings, evidence refs and an explicit hash-bound reviewer decision.
This validates provenance/structure only; authentic execution and semantic review
remain human/runner obligations. A successful audit is not milestone completion.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
KINDS = {'native_trace', 'render', 'semantic_review', 'coverage', 'interruptions'}
STAGES = {'candidate', 'implemented', 'replayed', 'reviewed', 'verified', 'accepted'}
ACCEPTED = {'verified', 'accepted'}


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path, export=None):
    text = path.read_text()
    if export:
        match = re.fullmatch(r'\s*(?://[^\n]*\n)*export const ' + export + r'\s*=\s*(\{.*\});\s*', text, re.S)
        if not match:
            raise ValueError(f'not a generated JSON export: {path}')
        text = match[1]
    return json.loads(text, object_pairs_hook=unique_pairs)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root=ROOT, milestone=None):
    root = Path(root).resolve()
    milestone = Path(milestone or root / 'engine/overhaul/animation-milestone')
    errors, warnings = [], []

    def load(path, export=None):
        try:
            return read_json(path, export)
        except (OSError, ValueError) as exc:
            errors.append(f'{path.name}: {exc}')
            return {}

    def path_for(name):
        if not isinstance(name, str) or not name or Path(name).is_absolute():
            errors.append(f'invalid repository-relative path: {name!r}')
            return None
        path = (root / name).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            errors.append(f'missing or escaping artifact/dependency: {name}')
            return None
        return path

    def hashed(name, sha, label):
        path = path_for(name)
        if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
            errors.append(f'{label}: missing/invalid SHA256')
        elif path and digest(path) != sha:
            errors.append(f'{label}: stale hash for {name}')
        return path

    def rows_ids(rows, label):
        result = {}
        if not isinstance(rows, list):
            errors.append(f'{label}: expected list')
            return result
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
                errors.append(f'{label}: missing string id')
                continue
            if row['id'] in result:
                errors.append(f'{label}: duplicate id {row["id"]}')
            result[row['id']] = row
        return result

    main = load(root / 'engine/client/item-catalog.mjs', 'ITEM_CATALOG')
    wear = load(root / 'engine/client/wearable-catalog.mjs', 'WEARABLE_CATALOG')
    for label, catalog in [('catalogue', main), ('wearables', wear)]:
        for key, row in catalog.items():
            if not isinstance(row, dict) or row.get('id') != key:
                errors.append(f'{label}: key/id mismatch {key}')
    union = set(main) | set(wear)
    tracker = load(milestone / 'requirements.json')
    tracked_main = rows_ids(tracker.get('items'), 'tracker items')
    tracked_wear = rows_ids(tracker.get('wardrobe'), 'tracker wardrobe')
    for oid, row in tracked_wear.items():
        if row.get('inMainCatalogue') is not (oid in main):
            errors.append(f'tracker wardrobe/{oid}: incorrect inMainCatalogue flag')
    for label, expected, actual in [('items', set(main), set(tracked_main)), ('wardrobe', set(wear), set(tracked_wear)), ('union', union, set(tracked_main) | set(tracked_wear))]:
        for key in sorted(expected - actual):
            errors.append(f'tracker {label}: missing union ID {key}')
        for key in sorted(actual - expected):
            errors.append(f'tracker {label}: unknown ID {key}')
    counts = {'items': len(main), 'wearableIDs': len(wear), 'supplementalWardrobeIDs': len(set(wear)-set(main)), 'totalUniqueObjects': len(union)}
    for key, count in counts.items():
        if tracker.get('scope', {}).get(key) != count:
            errors.append(f'scope {key}: declared {tracker.get("scope", {}).get(key)!r}, actual {count}')
    if len(union) != 609:
        errors.append(f'milestone requires 609 unique objects; found {len(union)}')

    documents, records, candidate_keys, sequence_keys = [], {}, set(), set()
    for path in sorted((milestone / 'repertoires').glob('*.json')):
        doc = load(path)
        if doc.get('schemaVersion') != 1:
            errors.append(f'{path.name}: unsupported schemaVersion')
        oid = doc.get('objectId')
        if oid not in union:
            errors.append(f'{path.name}: unknown referenced object {oid}')
        source_only = path.name.endswith('.candidates.json')
        field = 'candidates' if source_only else 'sequences'
        entries = rows_ids(doc.get(field), path.name)
        documents.append((oid, doc, source_only))
        for sid, seq in entries.items():
            key = (oid, sid)
            seen = candidate_keys if source_only else sequence_keys
            if key in seen:
                errors.append(f'duplicate {field} binding {oid}/{sid}')
            seen.add(key)
            if seq.get('objectId', oid) != oid:
                errors.append(f'{oid}/{sid}: sequence references a different object')
            status = seq.get('status')
            if status not in STAGES:
                errors.append(f'{oid}/{sid}: invalid status {status!r}')
            claim = status in ACCEPTED or seq.get('verified') is True or seq.get('verification_status') in ACCEPTED
            if source_only and (claim or status != 'candidate'):
                errors.append(f'{oid}/{sid}: candidate-only file cannot claim acceptance/progress')
            if not source_only or key not in records:
                records[key] = (seq, claim and not source_only)
        if source_only and (doc.get('verifiedSequences', 0) != 0 or doc.get('verified_sequences', 0) != 0):
            errors.append(f'{path.name}: candidate-only file cannot claim verified count')

    index_path = milestone / 'evidence-index.json'
    index = load(index_path) if index_path.exists() else {'schemaVersion': 1, 'artifacts': []}
    if index.get('schemaVersion') != 1:
        errors.append('evidence index: unsupported schemaVersion')
    artifacts = rows_ids(index.get('artifacts'), 'evidence artifacts')
    payloads = {}
    for aid, art in artifacts.items():
        before = len(errors)
        key = (art.get('objectId'), art.get('sequenceId'))
        if key[0] not in union:
            errors.append(f'{aid}: unknown referenced object {key[0]}')
        if key not in records:
            errors.append(f'{aid}: unknown sequence binding {key}')
        if art.get('kind') not in KINDS:
            errors.append(f'{aid}: unsupported evidence kind')
        path = hashed(art.get('path'), art.get('sha256'), aid)
        prov = art.get('provenance', {})
        if not isinstance(prov, dict):
            prov = {}
        for name in ['producer', 'command', 'sourceRevision', 'productionEntry']:
            if not prov.get(name):
                errors.append(f'{aid}: missing trace provenance {name}')
        if not isinstance(prov.get('fixture'), dict) or prov['fixture'].get('disposable') is not True:
            errors.append(f'{aid}: missing disposable fixture provenance')
        deps = prov.get('dependencies')
        if not isinstance(deps, dict) or not deps:
            errors.append(f'{aid}: missing current dependency hashes')
        else:
            for name, sha in deps.items():
                hashed(name, sha, aid)
        payload = load(path) if path and art.get('kind') != 'render' else {}
        if art.get('kind') != 'render':
            if payload.get('objectId') != key[0] or payload.get('sequenceId') != key[1]:
                errors.append(f'{aid}: artifact identity does not match index')
        if art.get('kind') == 'native_trace':
            if not payload.get('objectInstance') or not payload.get('actors') or not payload.get('frames'):
                errors.append(f'{aid}: no native instance/actor/frame trace')
            if payload.get('entryKind') not in {'production_command', 'production_selection'}:
                errors.append(f'{aid}: trace does not establish production entry')
        payloads[aid] = (payload, len(errors) == before)

    supported = {}
    for (oid, sid), (seq, accepted) in records.items():
        refs = seq.get('evidence', seq.get('evidence_refs', {}).get('runtime_artifacts', []))
        if not isinstance(refs, list):
            errors.append(f'{oid}/{sid}: evidence refs must be a list')
            refs = []
        if len(refs) != len(set(str(ref) for ref in refs)):
            errors.append(f'{oid}/{sid}: duplicate evidence reference')
        resolved = []
        for ref in refs:
            if not isinstance(ref, str) or ref not in artifacts:
                errors.append(f'{oid}/{sid}: unknown evidence reference {ref!r}')
                continue
            art = artifacts[ref]
            if (art.get('objectId'), art.get('sequenceId')) != (oid, sid):
                errors.append(f'{oid}/{sid}: evidence belongs to another binding: {ref}')
                continue
            if payloads[ref][1]:
                resolved.append(art)
        kinds = {art['kind'] for art in resolved}
        if seq.get('status') in {'replayed', 'reviewed'} and not {'native_trace', 'render'} <= kinds:
            errors.append(f'{oid}/{sid}: replay/review claim lacks current native/render evidence')
        if seq.get('status') == 'reviewed' and 'semantic_review' not in kinds:
            errors.append(f'{oid}/{sid}: reviewed claim lacks semantic review evidence')
        if not accepted:
            continue
        before = len(errors)
        if not KINDS <= kinds:
            errors.append(f'{oid}/{sid}: unsupported acceptance; missing current evidence {sorted(KINDS-kinds)}')
        required = seq.get('requiredBindings')
        completed = seq.get('completedBindings')
        if not isinstance(required, list) or not required or not all(isinstance(v, str) and v for v in required):
            errors.append(f'{oid}/{sid}: acceptance requires nonempty requiredBindings')
            required = []
        if not isinstance(completed, list) or set(map(str, completed)) != set(required) or seq.get('unresolvedBindings') != []:
            errors.append(f'{oid}/{sid}: acceptance has incomplete or unresolved bindings')
        review_ids = [art['id'] for art in resolved if art['kind'] == 'semantic_review']
        for aid in review_ids:
            review = payloads[aid][0]
            hashes = {art['id']: art['sha256'] for art in resolved if art['kind'] != 'semantic_review'}
            if review.get('decision') != 'accepted' or not review.get('reviewer') or review.get('artifactHashes') != hashes or not review.get('nearestCandidatesReviewed'):
                errors.append(f'{oid}/{sid}: review not explicitly bound to current artifacts/nearest candidates')
        for art in resolved:
            data = payloads[art['id']][0]
            if art['kind'] == 'coverage' and (not required or set(map(str, data.get('completedBindings', []))) != set(required)):
                errors.append(f'{oid}/{sid}: coverage artifact does not positively complete bindings')
            if art['kind'] == 'interruptions' and (data.get('exactlyOnce') is not True or not data.get('cases')):
                errors.append(f'{oid}/{sid}: no exactly-once interruption evidence')
        if len(errors) == before:
            supported[oid] = supported.get(oid, 0) + 1
    # Counts are checked, never written. Invalid evidence cannot back tracker credit.
    if errors:
        supported = {}
    for oid, doc, source_only in documents:
        if not source_only and doc.get('verifiedSequences', 0) != supported.get(oid, 0):
            errors.append(f'{oid}: repertoire has unsupported verifiedSequences')
        if doc.get('status') in ACCEPTED and supported.get(oid, 0) < 48:
            errors.append(f'{oid}: repertoire acceptance requires all 48 supported sequences')
    for label, entries in [('items', tracked_main), ('wardrobe', tracked_wear)]:
        for oid, row in entries.items():
            value = row.get('verifiedSequences', 0)
            if not isinstance(value, int) or isinstance(value, bool) or value != supported.get(oid, 0):
                errors.append(f'tracker {label}/{oid}: unsupported verifiedSequences={value!r}; indexed current claims={supported.get(oid, 0)}')
    if not artifacts:
        warnings.append('No runtime evidence indexed; source candidates earn no verified-sequence credit.')
    covered = {oid for oid, _, _ in documents if oid in union}
    return {'result': 'FAIL' if errors else 'PASS', 'scope': counts,
            'candidateBindings': len(candidate_keys), 'sequenceBindings': len(sequence_keys),
            'objectsWithRepertoireRecords': len(covered), 'objectsWithoutRepertoireRecords': sorted(union-covered),
            'artifacts': len(artifacts), 'supportedAcceptedClaims': sum(supported.values()),
            'semanticCertification': False, 'errors': errors, 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--milestone', type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.root, args.milestone)
    except (TypeError, AttributeError, ValueError) as exc:
        result = {'result': 'FAIL', 'errors': [f'malformed schema: {exc}'], 'semanticCertification': False}
    print(json.dumps(result, indent=2))
    return 1 if result['result'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
