# Repertoire worker instructions (lead-maintained; read fully before starting)

You author animation data for "Cheese the Duck", the user's own ASCII duck life-sim. Work ONLY in the git
worktree the lead gave you (run every command from its root; `.venv` and `engine/node_modules` are linked in).
Do not touch any other folder, do not commit, do not push.

## Read first
1. `engine/overhaul/animation-milestone/authoring-brief.md`: section 2a (v2 rules, these override
   everything), then sections 2, 3, 4.
2. `engine/overhaul/animation-milestone/review-wave1.md`: what the reviewer rejected (stamps, impossible
   staging, padding, dead gates, copied lines). Repeat none of it.
3. One finished v2 generator for technique (do not reuse its acts or lines): `engine/animation-authoring/rep_wave2a.py`.
4. The work-queue entry of each object (`engine/overhaul/animation-milestone/work-queue.json`): `host`,
   `consumable`, `family_engine`, `native_acts` (never repeat those), `wonder_routines` (the helper subtracts them).
   If `family_engine` is set, skim that family's JSON in `engine/client/animation/` and do not repeat its sequences.
5. The helper `engine/animation-authoring/rep.py` (never edit it). Print each drawing with
   `.venv/bin/python engine/animation-authoring/rep.py <id>` (digits mark the drawing's own anchors) and check
   yours with `--mark <your generator>`.

## Write
One generator `engine/animation-authoring/rep_<batch>.py` (sys.path.insert the animation-authoring folder)
emitting each object's JSON via `o.emit()` (hand-in). Every routine hand-written; no loops or name lists
stamping routines. Siblings each get their own acts built from what differs in their drawing and nature.

Quality bar (the user rejects filler and asked that nothing be cut): the object's full count of different
purposeful acts a duck could really do with it, true to its drawing; labels matching what the renderer shows
(feet on the standing line unless perched on a low "surface" anchor; never behind/under); state that matters
and survives between visits (obj_dirt / obj_wetness / obj_condition for wear); Cheese's voice deadpan, cheeky,
uncensored where earned; original lines. Universal acts (nap, bow, slip...) and common verbs are allowed once
per object when done with this object's parts and its own movement; identical drawn tracks are stamps and refused.

## Checklist (worktree root): BUILD PHASE (user 2026-11-14: focus on building, deeper QA later)
1. `.venv/bin/python engine/animation-authoring/rep_<batch>.py` (the helper's rules are the quality bar; all must pass)
2. `node engine/scripts/build-repertoire.mjs`
3. `node engine/scripts/export-repertoire-reach.mjs` (none of YOUR routines unreachable)
4. `.venv/bin/python engine/check_repertoire.py --quick --objects <a,b,c>` (one comma-separated list; quick = youngest age only) must PASS
5. Read your labels group by group; rewrite any pair that could swap tracks unnoticed.
No strict all-ages run, no review sheets in the build phase: the lead runs the deep QA later.

If the helper or harness refuses something you believe is right, or something fails outside your files, stop
and report it rather than working around it. If an object cannot reach its count with genuinely different real
acts, stop at what you have (emit with `need=<count>`) and report the count and why; do not pad.
Be economical: do not print files you do not need. Run checks in the foreground (a full six-object strict check can take 15-20 min); never wait with a shell loop on `pgrep -f <pattern>` (the loop's own command line matches the pattern, so it never ends).

## Return (under 120 lines)
Files written; per object: routines, per-age reach, groups, routines with lines, perched routines; result lines
of steps 3-5; per object the acts as "verb part" only, grouped; anything you could not make different.
