"""Disposable metadata fixtures only: no simulation/save and no acceptance credit."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
MODULE = REPO / 'engine/overhaul/animation-milestone/validate_evidence.py'
spec = importlib.util.spec_from_file_location('evidence_validator', MODULE)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EvidenceValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cheese-evidence-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.base = self.root / 'engine/overhaul/animation-milestone'
        (self.base / 'repertoires').mkdir(parents=True)
        for name in ['engine/client/item-catalog.mjs', 'engine/client/wearable-catalog.mjs', 'engine/overhaul/animation-milestone/requirements.json']:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)
        self.doc = {'schemaVersion': 1, 'objectId': 'bounce_house', 'verifiedSequences': 0,
                    'candidates': [{'id': 'fixture_candidate', 'status': 'candidate', 'verified': False}]}
        self.write('repertoires/bounce_house.candidates.json', self.doc)

    def write(self, name, data):
        (self.base / name).write_text(json.dumps(data))

    def run_audit(self):
        return validator.audit(self.root)

    def fails(self, fragment):
        result = self.run_audit()
        self.assertEqual(result['result'], 'FAIL')
        self.assertTrue(any(fragment in error for error in result['errors']), result['errors'])
        self.assertEqual(result['supportedAcceptedClaims'], 0)

    def test_real_scope_and_source_only_candidates_are_not_verification(self):
        result = self.run_audit()
        self.assertEqual(result['result'], 'PASS', result['errors'])
        self.assertEqual(result['scope']['totalUniqueObjects'], 609)
        self.assertEqual(result['scope']['supplementalWardrobeIDs'], 67)
        self.assertEqual(result['candidateBindings'], 1)
        self.assertEqual(result['supportedAcceptedClaims'], 0)
        self.assertFalse(result['semanticCertification'])
        self.assertEqual(len(result['objectsWithoutRepertoireRecords']), 608)

    def test_whole_repertoire_acceptance_requires_full_scope(self):
        self.write('repertoires/bounce_house.json', {'schemaVersion': 1, 'objectId': 'bounce_house',
            'status': 'accepted', 'verifiedSequences': 0, 'sequences': []})
        self.fails('requires all 48 supported sequences')

    def test_audit_does_not_modify_any_input(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.run_audit()
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_duplicate_tracker_ids_rejected_but_cross_catalogue_overlap_allowed(self):
        path = self.base / 'requirements.json'
        data = validator.read_json(path)
        data['items'].append(copy.deepcopy(data['items'][0]))
        path.write_text(json.dumps(data))
        self.fails('duplicate id')

    def test_missing_supplemental_union_id_rejected(self):
        path = self.base / 'requirements.json'
        data = validator.read_json(path)
        data['wardrobe'] = [r for r in data['wardrobe'] if r.get('inMainCatalogue')]
        path.write_text(json.dumps(data))
        self.fails('missing union ID')

    def test_duplicate_generated_json_keys_rejected(self):
        path = self.root / 'engine/client/item-catalog.mjs'
        path.write_text('export const ITEM_CATALOG = {"x":{"id":"x"},"x":{"id":"x"}};')
        self.fails('duplicate JSON key')

    def test_candidate_duplicate_id_and_unknown_object_rejected(self):
        self.doc['candidates'].append(copy.deepcopy(self.doc['candidates'][0]))
        self.doc['objectId'] = 'not_real'
        self.write('repertoires/bounce_house.candidates.json', self.doc)
        self.fails('duplicate id')
        self.fails('unknown referenced object')

    def test_sound_candidate_cannot_claim_verified(self):
        self.doc['candidates'][0].update(classification='sound_candidate', status='verified', verified=True)
        self.write('repertoires/bounce_house.candidates.json', self.doc)
        self.fails('candidate-only file')

    def test_verified_manifest_without_trace_and_bindings_rejected(self):
        self.write('repertoires/bounce_house.json', {'schemaVersion': 1, 'objectId': 'bounce_house',
            'sequences': [{'id': 'fixture_candidate', 'status': 'verified', 'unresolvedBindings': []}]})
        self.fails('unsupported acceptance')
        self.fails('nonempty requiredBindings')

    def test_replayed_claim_requires_native_render_provenance(self):
        self.write('repertoires/bounce_house.json', {'schemaVersion': 1, 'objectId': 'bounce_house',
            'sequences': [{'id': 'fixture_candidate', 'status': 'replayed'}]})
        self.fails('replay/review claim lacks')

    def test_unknown_evidence_reference_rejected(self):
        self.doc['candidates'][0]['evidence'] = ['does-not-exist']
        self.write('repertoires/bounce_house.candidates.json', self.doc)
        self.fails('unknown evidence reference')

    def test_artifact_without_provenance_cannot_pass_as_native_trace(self):
        path = self.root / 'fake-trace.json'
        path.write_text(json.dumps({'objectId': 'bounce_house', 'sequenceId': 'fixture_candidate'}))
        self.write('evidence-index.json', {'schemaVersion': 1, 'artifacts': [{
            'id': 'trace', 'objectId': 'bounce_house', 'sequenceId': 'fixture_candidate',
            'kind': 'native_trace', 'path': 'fake-trace.json', 'sha256': validator.digest(path)}]})
        self.fails('missing trace provenance')
        self.fails('no native instance/actor/frame trace')

    def test_escaping_artifact_and_stale_dependency_rejected(self):
        self.write('evidence-index.json', {'schemaVersion': 1, 'artifacts': [{
            'id': 'trace', 'objectId': 'bounce_house', 'sequenceId': 'fixture_candidate',
            'kind': 'native_trace', 'path': '../outside.json', 'sha256': '0'*64,
            'provenance': {'producer': 'unit fixture', 'command': 'not executed', 'sourceRevision': 'test',
                'fixture': {'disposable': True}, 'productionEntry': 'test',
                'dependencies': {'engine/client/item-catalog.mjs': '0'*64}}}]})
        self.fails('missing or escaping artifact')
        self.fails('stale hash')

    def test_tracker_credit_without_indexed_acceptance_rejected(self):
        path = self.base / 'requirements.json'
        data = validator.read_json(path)
        data['items'][0]['verifiedSequences'] = 1
        path.write_text(json.dumps(data))
        self.fails('unsupported verifiedSequences')


if __name__ == '__main__':
    unittest.main()
