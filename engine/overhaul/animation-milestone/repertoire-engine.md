# Repertoire engine (scales the 48-per-object milestone)

Goal: every one of the 609 objects gets 48 meaningful, physically distinct sequences,
authored as DATA and executed by ONE native engine, validated by ONE harness. Family
engines (keepsakes, playkit, castle, wonders...) keep working; the repertoire layer adds
the remaining sequences without another work key per family.

## Data (one file per object): `client/animation/repertoire/<object_id>.json`
```
{ "object": "rubber_duck", "host": "placed|portable|keeping|display|wearable",
  "fields": {"name": [default, min, max]},          // saved in obj['rep']
  "physics": [[field, op, value, when]],            // same DSL as wonders
  "triggers": [[when, effects]],
  "effects": {"name": [[target, op, value]]},       // target: field | "subject.<field>" | "need.<need>" | "ecology.<k>"
  "anchors": {"name": {"x": 0..1, "y": 0..1}},      // fractions of the drawn sprite box; named builder anchors win if present
  "subjects": {"from": "keeping.fish|display.items", "pick": "hungriest|species|stable"},   // optional
  "routines": { "<id>": { "label", "duration", "track": [[t, pose]], "events": [[t, effect]],
                 "when": [...], "prefer": [...], "ages": null|[...], "tool": "wing|none|<tool>",
                 "say": null|cue, "species": null|[...], "obj": [[t, {"sway","lift","shake","glow","puff"}]] } } }
```
`obj` keyframes animate the object itself at draw time (painter sway/lift/shake + overlay
glyphs at anchors), so objects whose builders lack moving parts still respond physically.

## Native (`engine/repertoire.py`)
Generalises wonders.py (same rule DSL, sliced physics, contacts at authored moments,
completion once, no rewards, reach table, storms, ages, mood/needs context, say lines).
Plan key `rep_work`; request via pond command `rep_action` (text = routine id); autonomous
choice through `decide()` alongside family defaults; visitor company reuses
wonder_company's join/operate logic parameterised by plan key.
Need effects (`need.fun` etc.) go through `pond.change_need` exactly once at contact.
Consumables are never consumed by repertoire routines (family handlers own quantities).

## Renderer
`client/repertoire-routines.mjs`: shared sampler (held anchors), geometry using named or
fractional anchors on ANY construction, stretched wing / tool shafts, object reactions.

## Validation (`engine/check_repertoire.py`, `engine/tests/repertoire.test.mjs`)
Per object: 48 routines; each eligible in a synthesised authored context at every age
that can reach it; no work before arrival; exact contacts in order at the object; one
completion + memory; no items/coins; replay no-op. Distinctness: no two routines of an
object share (events, anchors, tool, parts/obj keys, quantised pose trace); siblings in
a family must differ from each other per routine id. Reach table regenerated from art.

## Authoring workflow (agents)
Lead (Opus) owns engine, integration, harness, merges. Sonnet workers author object files
in batches of 4-8 objects (exclusive files only), run `check_repertoire.py --objects ...`
and `node --test tests/repertoire.test.mjs` until PASS, return evidence. Fable reviews a
sample per family for meaningful distinctness before the family is marked done.
