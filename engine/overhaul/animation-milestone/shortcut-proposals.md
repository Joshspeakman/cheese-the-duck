# Shortcut scout: proposals (read-only review of codex/ascii-engine-port @ 1172b6d)
I could NOT profile the native phase (a native
run was blocked by the permission classifier), so native-time claims below are reasoned from the code, not
measured; proposal 3 starts with a 10-minute profile to confirm. Static phase measured: 0.43 s total (imports
dominate), so static checks are never the bottleneck.
Cost anatomy (estimates). Remaining work is mostly 442 objects owing 48 (248 placed + 194 portable); wearables
(109 x 24) and displays (44 x 12) are small. A 48-routine object is ~30 KB of generator (~8k output tokens): that
is the irreducible authoring cost. What a worker pays on top of it, and what can be cut:
- authoring-brief.md 46 KB (~12k tokens), of which section 1 (design review) and large parts of 2 are superseded.
- The "finished generator for technique": worker-prompt names rep_wave2a.py = 160 KB (~40k tokens); v3 generators
  are 90-200 KB. Largest single read. It is also v2 while the rules are v3.
- `rep.py <id>` prints per object (3-5k tokens each, x7), review-wave1.md 4 KB, queue entries, rep.py itself if read (39 KB).
- Retry cycles: every helper refusal aborts the whole generator on the FIRST failing assertion.

## Ranked proposals

### 1. Lint mode: collect every refusal in one pass, with fix hints (rep.py)   [saves most iterations]
What: `REP_LINT=1` (or `Obj.lint=True`): wrap `Obj.r()` so an AssertionError is recorded (key, message) instead of
aborting; snapshot/restore the mutable counters (acts, verbs, fired, needy, far, untouched, places_seen, sigs,
hcontent, group, sentences, used_anchors, _known) via copy.deepcopy before each call so a refused routine leaves no
trace. `emit()` in lint mode prints all refusals grouped by kind plus a hand-in gap report (groups vs lo..hi per
group, unused anchors, per-age reach vs floor, verbs left, stock/inspect caps used) and writes NOTHING; normal
`emit()` is unchanged and still the only path that writes the file. Add hints to the common refusals: "same act as X"
-> print the five signature components of both and which ones already differ (needs two); "out of reach" -> the
anchor's px height, the hatchling/adult limits and the object's anchors under 63 px; "label must say the verb" ->
print the required stem (`verb.split('_')[0][:4]`, e.g. `scoo`); "perch needs surface" -> list the surface anchors;
"(verb,part) already used" -> list unused verbs from VERBS and the used (verb,part) pairs; "can never come true / always
true" -> print the field's default, range and who moves it.
Saving: each batch is 6-9 objects x 48 calls; refusals appear one at a time, each costing an edit + a rerun + a
re-read of tool output (~15-30k tokens of cached context per loop, plus the node sprite() spawns). Lint turns N
sequential retries into ~1-2. Expect 20-35% off iteration tokens and 5-10 min per batch (my estimate; the lead's
log of retries per batch would confirm).
Risk: low. Lint mode cannot write files; hand-in path untouched. The one hazard is half-applied state from a refused
call (hence the deepcopy snapshot) producing false cascades; keep the `emit` guard `assert not self.lint_errors`.
Verify: run lint on an existing good generator (rep_display_v3.py): zero errors and no file written; seed a
generator with 5 known defects (reach, stamp, label verb, unused anchor, group): all 5 reported once; byte-compare
JSON from normal emit before/after the change for rep_display_v3.py.

### 2. Worker kit: rules card + per-batch prep sheet + one short exemplar   [saves ~50-80k tokens per batch of 7]
What (three files, lead-generated, no rule changes):
a) `overhaul/animation-milestone/rules-card.md` (~3 KB): 2a+ and 2a distilled to one-line rules, the reach table, the
   verb list (printed by the helper from VERBS), UNIVERSAL/INSPECT/CLEAN sets, tags (TAGS), `Obj`/`r()` signatures, the
   checklist. Source of truth stays the brief; generate it from rep.py constants so it cannot drift
   (`rep.py --card`). worker-prompt.md says "read the card; the brief only if the card does not answer".
b) `scripts/prep-batch.py <ids>` writes `prep/<batch>.md`: per object, the queue entry (host, consumable, need,
   native_acts, wonder_routines), `rep.py` drawing + blueprint + own-anchor table with px heights, a one-line
   "reachable at 63/82 px" strip (rows/parts a hatchling can touch), the family JSON's act labels only (not the file),
   a ready `Obj(...)` skeleton (parts dict from blueprint props, anchor candidates from the drawing's own anchors,
   low anchors pre-flagged "surface"), and sibling objects in the same batch. Workers then print nothing themselves.
c) `rep_example.py` (~15 KB): one placed object in full (about 14 routines, with every kind of construct: perch, obj
   moves, marks, gates, a duet, lines) plus 3-4 routines each for portable/wearable/display/keeping, written to v3.
   Replaces "read rep_wave2a.py (160 KB)". Taken from a reviewer-approved finished object so the quality bar is shown.
Saving: exemplar 40k -> ~5k tokens; brief 12k -> ~1.5k; per-object rep.py prints folded into one sheet: ~60k per worker run (8-10k of the 45-60k per object).
Risk: low-medium. A short exemplar can pull workers toward copying its acts (stamp risk, which the helper still refuses)
-> the exemplar must be flagged "technique only, do not reuse acts or lines" and use an object no worker will get (e.g.
a finished one). A distilled card can omit a rule: generate it from code, and keep the brief linked.
Verify: pilot one batch with the kit against a same-shape batch run the old way; compare tokens, retries, and the reviewer's
rejection rate; the helper/harness refusals are unchanged, so guarantees are untouched.

### 3. Native harness: shards, keep-going, incremental result cache (check_repertoire.py)   [biggest wall-clock win]
What (same checks, same ages, same sim):
a) `--jobs N` (default 1): the parent runs the static phase once, then spawns N child processes of itself with
   `--objects <slice> --child`, round-robin by object (each already gets its own mkdtemp CHEESE_SAVE_DIR; the
   rotation check is per object, so slicing by object is exact). Merge their JSON result lines; PASS only if all
   PASS. Cap N at cores-2 (M1 Pro) and let the lead pass `--jobs 3` when four workers are active.
b) `--keep-going`: record a failing (routine, age, label) with its message and continue to the next routine instead of
   aborting; print all failures at the end and exit non-zero. A 13-minute fish run that dies at routine 40 of the
   third object currently throws away everything and the rerun starts from scratch.
c) Result cache `engine/.cache/rep-native.json` keyed per (routine JSON hash + the object's spec hash [effects, anchors,
   fields, physics, host] + a hash of every engine source the sim reads [git tree hash of engine/*.py, world/, core/,
   duck/ ... or `git rev-parse HEAD:engine HEAD:world ...`]) -> list of ages that passed. Cache only PASSES; a hit skips
   that routine's native runs. The object-level rotation check is also cached by the spec hash of the whole file.
   Any engine edit changes the code hash and invalidates everything. `--no-cache` forces a full rerun (use for sign-off
   and the lead's final merge check).
Saving: (a) is ~Nx on idle cores (a 6-fish run of 13 min -> ~4-5 min at N=3-4 alongside other workers; a 20-min
placed-batch strict check likewise); (b)+(c) turn the "fix one thing, rerun everything" loop into rerunning only changed
routines (the rerun after a fix: minutes -> seconds). Expect the lead's post-merge re-check to be a pure cache hit when
the merge changed nothing (it re-runs the same JSON the worker passed), if the worker's cache is carried or the lead
runs with the same cache path (put it under the shared repo, not per worktree: `REP_CACHE=/abs/path`).
Risk: medium for (c) only. A stale cache could mask a regression. Mitigations: key includes the engine tree hash;
include python/node versions; final sign-off and any engine change use `--no-cache`; cache stores no failures.
(a)/(b) are risk-free for guarantees. The checks and 8-age rule are untouched.
First step: cProfile one `--quick --objects <fish>` run (likely hot: p.sync() every 5 steps, R.eligible, give()/K.keep); a setup snapshot cache is worth it only if give() dominates.
Verify: old vs new on 4 finished objects (one per host) must give identical runs/checks; inject a defect at age legendary and confirm all modes catch it; poison the cache by editing an engine file and confirm a full rerun.

### 4. One command to land a worker's batch (scripts/land-batch.py)   [saves ~10-15 lead minutes per batch]
What: `land-batch.py --worktree PATH --objects a,b,c [--no-cache]`:
1. copy only the worker's `engine/animation-authoring/rep_<batch>.py` and `client/animation/repertoire/<obj>.json` (the
   object list comes from `git -C PATH diff --name-only`; refuse any other path touched, e.g. a changed rep.py);
2. regenerate (never merge) the generated bundles: `build-repertoire.mjs`, `export-repertoire-reach.mjs` (these two
   files conflict between parallel worktrees; tell workers not to commit them, the script owns them);
3. `check_repertoire.py --strict --jobs N` on the batch PLUS the static cross-object checks over the union (see 5);
4. `node --test tests/repertoire.test.mjs`, `build-repertoire.mjs --check`, `export-repertoire-reach.mjs --check`;
5. recompute work-queue.json `repertoire_routines` per object and `progress` from the repertoire folder (script, not
   hand-edited; the queue currently is hand-synced, 196 KB file with a progress block);
6. optionally `rep-check.cjs` + print the first review sheet path; then `git add` exactly the files above and commit with
   a templated message (routine counts per object, shortfalls) and the required trailer lines; push only with `--push`.
Risk: low; it only orchestrates existing steps and stops on the first failure. It must refuse to commit on any red step
and never use `force`. Verify: dry-run mode printing the commands; run on the already-landed wave 5a and expect a no-op diff.

### 5. Cross-worker visibility and one precomputed index (rep.py)   [prevents merge-time rework; saves seconds per run]
Problem: `_other_stamps`, `_other_contents`, `_known_lines` each glob and json-parse every file in OUT (3 full scans
per Obj, so 3x per object per generator run; at 600 files x ~50 routines that is tens of MB parsed per run and growing),
and a worker in its own worktree only sees finished objects at ITS base commit, never the parallel workers' output. Two
workers' stamps, contents or lines collide only when the lead merges, which means a rework.
What: (a) a module-level cache so the three scans share one parse per process; (b) `REP_PEERS=dir1:dir2` extra
directories (the other three worktrees' `client/animation/repertoire/`) read in the same scans, so a stamp or copied
line against a peer's finished objects is refused immediately in the worker (the lead sets it when launching, plus
a peers refresh before the worker's final emit); (c) `land-batch.py` runs the same union check. The peer files are
read-only inputs; nothing in them is written.
Saving: minutes of rework per collision (each collision costs a worker rerun of ~100k+ tokens if the merge fails
late); (a) shaves a few seconds from each of ~10-15 generator runs per batch. Risk: low (stricter, never looser).
Verify: construct two worktrees with an intentionally colliding act; the second worker's helper refuses with the
peer's key named; without REP_PEERS behaviour is byte-identical.

### 6. Batch shape and ordering (policy, no code)   [saves roughly 10-20% of per-object overhead]
- Keep families together in ONE worker (seeds 16, gem 9, rock 9, flowerpot 8, leaf 8, rug 8+5, crumbs 8, pool 8,
  fountain 7, feather 7, house 5, lamp 5...): siblings must differ from each other, and a worker authoring them in one
  generator can plan the differences up front; splitting a family across parallel workers is exactly the case the helper
  cannot see (proposal 5). 267 distinct host/family groups exist; 67 wearables have no family: batch by body spot.
- Light hosts bigger, heavy hosts smaller: wearables (24, no sprite measuring, BODY_SPOTS anchors) and displays (12) in
  batches of 12-16; placed/portable 48s at 6-7 (the 30 KB-per-object output makes 9+ push context past useful quality
  and lengthen the strict check). The fixed prefix (rules, exemplar, tool setup) is paid once per worker, so the savings
  come mainly from the wearable/display tail (153 objects, ~30% of remaining objects but ~8% of the routines).
- Order: run the 2-3 hardest families first so rule questions reach the lead before four workers repeat them; never mix host kinds in a batch.
Risk: policy only. Verify: track tokens/object per batch shape for 2-3 batches.

### 7. Worker iteration tiers (worker-prompt.md checklist)   [saves a worker-side hour per few batches]
What: iteration uses `check_repertoire.py --quick --objects X` (one youngest reachable age per routine: already exists)
plus the static phase; the strict 8-age run is done ONCE at the end and, with proposal 3, is incremental and keep-going.
Also: fix the checklist order to run `--strict --frames 2` once only (frames only at the final), and cap rep-check at one
sheet (already). Also state in worker-prompt.md: "never wait for the strict run to look at the sheet" (run it in the
background and read the sheet from a quick run).
Saving: a worker that reruns strict (15-20 min) 2-3 times -> once. Risk: low; sign-off still requires the full strict.
Verify: the final landed result is the same strict PASS line; the lead's land-batch re-checks with --no-cache.

### 8. Machine-measured anchor candidates (part of 2b)
prep-batch.py lists inked clusters with x/y fractions, px height, flat-top (surface) flag and same-touch-place groups, so anchor guesses (empty air, same place, taken name, perch too high; typically 2-5 refusals per object) stop. The helper and `--mark` still validate; low risk.
## Rejected (would weaken a rule, or not worth it)
- Skipping ages ("age runs are provably equivalent"): I cannot prove it from the code (age changes the duck's body, speed,
  eligibility, destination via the pond plan); the rule says every age runs natively. Not proposed.
- Template/loop-generated routines, shared act libraries across siblings: they create stamps/relabels the rules forbid.
- Dropping rep-check or the reviewer pass: only visual proof labels match the screen.
## Observations for the lead
- At HEAD the static check already fails on finished fish: `check_repertoire.py --quick --objects bass` -> bass_scoop_the_leaves
  _from_the_leaping_lane is a stamped copy of catfish_skim_the_leaf_mat; `--objects koi` -> koi_hand_feed_the_hungriest
  is a stamped copy of ghost_fish_peer_at_the_pale_scales / salmon_peer_at_the_scale_sheen. These fish are in the rework pile
  (v3 stamp definition); the same check run by workers will hit them only when they touch those objects, but land-batch
  (proposal 4) should run the static checks over ALL objects and report pre-existing failures separately.
- Suggested order to implement (cost to build -> payoff): 1, 3(a,b), 4, 2, 5, 7, then 3(c), 6, 8.