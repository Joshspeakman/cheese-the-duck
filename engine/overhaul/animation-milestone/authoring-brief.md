> Lead update (after review): section 1 defects 1-8, 10-16, 18, 19 are fixed in the engine or harness; 9 (wearables drawn on the body only) and 17 (fields drawn) are addressed by requiring the item to be worn and by `obj.*` targets for real wear. Repertoire-only fields still have no drawing of their own; the act shows them.

# Repertoire engine: design review and authoring brief

Reviewed at `cfaaeb2` on `codex/ascii-engine-port` (2026-11-13). Paths are under `engine/`. Line numbers are pinned to that commit (`git show cfaaeb2:engine/<file>`); the working tree has moved since. Nothing in the repository was changed. Sections 2 to 4 are the worker prompt. Section 1 and the appendix are for the lead.

## 1. Design review (lead)

What holds: one `apply` path, completion recorded once, no possession changes, replay is a no-op, and a native run costs about 0.02 s (koi and scarf_red: 67 runs in 1 s), so the full matrix of 609 x 48 x 8 runs is one to two hours. "Shown" means I ran the real code with the case loaded in memory; "read" means from the source only.

**Fake distinctness passes**
1. `check_repertoire.py:53-58 signature()` calls two routines different when any one of six parts differs, and most parts are free to change. Shown on `koi_scatter_flakes`: each of these alone counts as a new sequence: tool renamed `wing` to `feather`; a key nothing draws (`"zz":1`); one empty keyframe; the event pointed at a second effect name with the same rows; an anchor renamed at the same x,y; `shake` swapped for `glow`; one `x` moved from 0 to .6. "Run until PASS" teaches workers exactly these. Compare effect rows by content, anchors by position and tool by class, drop undrawn keys, collapse repeated poses, and require two parts to differ (the appendix helper does).
2. There is no sibling check (read). `repertoire-engine.md:41-42` and the harness docstring (`check_repertoire.py:5`) promise one, but `sigs = {}` (`check_repertoire.py:71`) is per object, so `koi.json` with `koi` replaced by `carp` passes. Most exposed: 14 kept fish, 15 cards, 11 badges, 8 pools, 8 rugs, 109 wearables.
3. Track keys beyond the pose joints count toward the signature (`check_repertoire.py:54`), but `repertoire-routines.mjs:9,14` samples only `x y b w l r reach contact`. Unlike the wonders, object parts are never drawn here.
4. `tool` is a free string (read). Anything but `none` or `wing` gets 1.6 x body reach (`export-repertoire-reach.mjs:16`) and the same `/` shaft (`repertoire-routines.mjs:43`). "Long pole" buys an adult 188 px of reach and a new signature.

**Impossible contacts pass**
5. Effects fire on a timer (`repertoire.py:298`); nothing ties an event to a touching pose, and the harness checks only event order (`check_repertoire.py:79`). Shown: an event with no `contact` keyframe exports `contactHeight 0`, in reach of every age. The committed pilot has one (`scarf_red.json`, `scarf_snuggle`).
6. The reach scan samples 41 points (`export-repertoire-reach.mjs:22`). Shown: a contact pulse .015 wide on an anchor 336 px up exports height 0.
7. A drawing's own anchor wins by name (lead: now only when it is a finite point) even when it is not a point (`repertoire-routines.mjs:19`). koi_pond has `rim: 44` and `swimRadius: 26`; bounce_house has `surface: "castle"`, `slots`, `controls`, `route`. Shown: an authored `rim` on a fish gives NaN, so height 0 and every age; the node test's `assert.ok` (`tests/repertoire.test.mjs:20`) passes on the truthy 44.
8. Nothing checks that a fractional anchor lands on ink (read). The top 27% of the koi_pond box is blank.
9. Reach is height only, on one sprite per object (read). Display objects are measured on their own sprite (`hostItem`, `export-repertoire-reach.mjs:13`; `tests/repertoire.test.mjs:11`) but drawn on the trophy case or cabinet. Sea fish are measured on infinity_pool though pool_large is also a host.
10. Wearables need only ownership (`repertoire.py:141`; the harness only appends to `owned_items`, `check_repertoire.py:168-171`), so Cheese can rewrap a scarf he is not wearing. The routine plays on his body alone (`ultra-world.mjs:550`) and reach is waived (`export-repertoire-reach.mjs:19`). Until the item must be worn, 109 x 48 wearable routines are body pose only.
11. `obj` reactions move the whole host sprite (`repertoire-routines.mjs:24-28`, `ultra-world.mjs:354`): a fish routine's `shake` shakes the pond, and `lift` would lift a gong.

**Gaps that stop or mislead batches**
12. The portable host (175 objects) fails on the second run of one object. Shown with `feather` and `acorn`: "Give that a moment. Cheese would enjoy some variety." (`living_world.py:563-564`); `reset()` (`check_repertoire.py:122-132`) does not clear `last_use` on the shared state.
13. `give()` places everything as a habitat item (`check_repertoire.py:138-143`), yet 49 of the 267 placed objects come from decorations, blueprints or the garden. Shown for one case: `rubber_duck` as the first object raises a bare `StopIteration` at `:142` (the first sync drops the placement; a second attempt works). The other 48 were not tried.
14. Rows that do nothing pass. `apply` skips `need.*` with any op but `add`, unknown needs, `subject.*` off a keeping host and unknown fields (`repertoire.py:66,76,82`); the harness accepts any `subject.`, `need.` or `keeping.` prefix (`check_repertoire.py:70`) and counts a call to `apply` as a contact (`:259`, `:300`). Forty-eight empty effects with different names are 48 signatures. The spec's `ecology.<k>` target does not exist.
15. No floor per age: one reachable age passes (`check_repertoire.py:88`), and `--quick` runs only the youngest (`:271`). An object can end with nothing for a hatchling.
16. Gates are forced, not earned: `setup_for` (`check_repertoire.py:192`) writes field values, so `when: ["shine>.9"]` passes when nothing can raise `shine`. A bare `!powered` on an object with no `power` field is always true (`check_repertoire.py:39`, `:50`).
17. Fields are invisible (read). They live in `obj['rep']`; that state reaches `itemSprite` (`physical-objects.mjs:4`) but no client code reads `.rep`, and effects cannot reach the state that is drawn (`obj['wonder']`, waterworks, `dirt`, `condition`). 435 objects have a family engine: a repertoire `water` beside the real one is two truths. Add effect targets for real state.
18. One bad file stops everyone: a duplicate id or a missing `when`, `prefer`, `tool`, `events` or `effects` fails `import engine.repertoire` or a live decision (`repertoire.py:20-25`, `:213-227`, `:296`), and every worker's build rewrites `repertoire.json` and `repertoire-reach.json`. Use one worktree per worker; rebuild the two bundles at merge.
19. Autonomous choice strands most of the 48 (read): `appeal` (`repertoire.py:220-230`) caps the novelty penalty at 20, so a routine with three tags and two preferences (46) beats an ungated one (10) for ever. `choices()` also ignores `pick` (`:327`). Rotate by least used among the eligible.
20. Art is still moving: work-queue.json lists 122 objects as `pending` and 487 as under review. Fractional anchors go stale silently when a drawing changes shape.

Spec and code disagree: `lines` and routine-level `pick` exist only in code; the spec's `subjects` block and `ecology.` target exist only in the spec.

## 2a. Version 2 rules (lead, after the wave-1 acceptance review): these override anything below

What the screen shows. Cheese's feet stay on the standing line (the object's front edge) unless a keyframe has `perch` (0 to 1): then his feet go to the touched anchor, which must be flagged `"surface"` and be at most 0.6 x his body height for that age (the helper limits the ages). He stands with his bill (tool `none`) or wing/stick tip at the touched place and walks between anchors. `x` pushes his head forward, `y` drops it, `b` squats or hops the body, `l`/`r` lift a foot; `w` only shows with tool `none`; with wing or stick `reach` sets the arm. He is never drawn behind, under or inside anything, and the object's own parts never move (only the whole sprite sways, shakes or lifts; `glow`/`puff` draw at the touch).

Rules (the helper enforces most of them):
1. Before writing, list every drawn part with its height and what it is (`rep.py <id>` now also marks the drawing's own anchors with digits: the real door, seat or opening). If you cannot say what a glyph is, do not name it. Check your anchors with `rep.py <id> --mark <your generator>`.
2. Labels say what is drawn: never behind/under/beneath; "in/on/into/through/across the" only with `perch` (standing on or in it) or `shown="head"` (only his head goes in).
3. Every routine declares `act=(verb, part)` from the helper's verb list. No (verb, part) twice; at most three of one verb. A new time, weather, mood or age is not a new act.
4. At most one each per object: nap, shelter, sulk, wait, walk_into, slip, stuck, stamp, bow, present, argue, pose. These ARE allowed on every object (once each), and so are common verbs like wipe, dry, chip frost, sweep leaves: what is forbidden is a stamped act, i.e. the same drawn track as on another object (the helper and harness refuse identical tracks in rendered cells), or a template that ignores this object's own parts. Do not drop an act because a sibling has a similar one; do it with this object's parts and its own movement. The rest group is not six ways to sit down: one nap, one shelter, and the others are things only this object allows.
5. Push on the part that moves. A pivot, a fixed leg or a post does not tilt, swing or roll anything.
6. An effect is the direct result of the touch. A performance has `events=[]`. No padding rows (add under 0.1, mul between 0.85 and 1.18); an effect is fired by at most three routines (a need-only effect by two); at most 8 routines carry need rows.
7. Gates must still hold when Cheese comes back (autonomous choice waits about two minutes). Never gate a routine on a `decay` field another routine sets; put cause and consequence in one routine. For state that waits (snow, frost, leaves, fill), use slow `rate` fields. A gate that is always true is refused.
8. Dirt, wetness and damage are real drawn state: use effects `obj.dirt`, `obj.wetness`, `obj.condition` and gates `obj_dirt>.3`, `obj_wetness>.3`, `obj_condition<.6`. Every routine that cleans or dries gates on the matching `obj_` field. Fields named damp/wet/dirt/mud/dust/clean/wear are refused; water/rain/puddle only for a drawn vessel that holds it (`containers={"water"}`).
9. Invent nothing the drawing lacks: no dents, loose slats, flies, pigeons, tenants, valves, or puddles where water cannot sit.
10. Lines: react to what just happened, under ten words where you can. No line from this brief or another object's file, no repeated formula ("X. Mine.", "Nobody..."), the second line is a different joke, and Cheese is a duck.
11. Native acts already exist and must not be repeated (each is ONE native gesture: e.g. one plain slide down, one plain bounce; distinct tricks with a different body and path, such as sliding down headfirst or backwards, a seat drop or a spin on the mat, ARE new acts and expected, staged with perch along the chute or mat anchors): resting inside a home (dog_house, gazebo, nests, beds, houses), riding or exploring slides, swings, trampolines, seesaws and rocking horses, and building in sandboxes. Repertoire acts are everything else a duck could do with the thing.
12. Find the parts a hatchling can reach (63 px, or a low `surface` to perch on) first and write those acts before anything else.
13. Loose (portable) objects can now be carried, tossed, rolled away and hidden: obj keys `ix`, `iy` (cells), `hold` (0..1, in his bill; needs liftable=True) and `hide` (buried/stashed). The object must end at rest and only while he holds or touches it (no gliding home). Parts drawn in front of the standing line count as ground level.
14. Worn things (wearable host): anchors are named places on his own body, from `rep.BODY_SPOTS` (crown, brow, eye, bill, cheek, nape, throat, neck, chest, shoulder, back, belly, wing, wing_tip, tail, rump, thigh, foot_l, foot_r); pass them as `anchors=dict(neck=0, chest=0)`. The worn piece itself moves with obj keys `wx`/`wy` (shift, e.g. tugged askew), `flap` (tails/brim waving), `sag` (loosened), `off` (taken off: not on his body), and once off `hold` (in his bill) or `ix`/`iy` (laid beside him). It must be back on, at rest, by the end, while he touches it. Equipment never changes.
15. Duets: `o.r(..., duo=[k(...), ...])` gives a visiting friend their own authored part (their own track and touches; at least one touch on this object). A duet runs only while a free friend is here, and waits for them to walk over. It must be a different act from the solo ones: the partner's touches count in the signature. Good duets: steadying while he climbs, taking turns, passing something between them, a two-duck game. Never on worn pieces.
16. Shown things (display host, on='trophy_case'): the case now draws the real displayed things on their slots. Anchor `item` (pass `anchors=dict(item=0, ...)`) is the thing itself on its own slot; lowest shelf 115 px (young adult and up with a wing; a twig reaches it from juvenile), so young ages work the glass, doors and base. obj `hold` lifts it out to his bill (touch `item` first; put it back by the end). The engine checks the real slot height at run time.
17. Kept fish (keeping host, on='koi_pond' or 'infinity_pool'): obj `lure` (0..1) brings the picked fish (`pick='hungriest'` or `'shyest'`) to the rim spot he is touching, so kisses, chin tickles, hand-feeding from the bill, follow-the-wingtip and hoop tricks are drawn; it swims off again by itself. Feeding needs no inventory: scatter flakes (`keeping.flakes`), ring the feeding bell (`keeping.bell`), and the fish's own state (`subject.hunger/mood/trust/health/growth`). Cheese stays on the rim (sea tank: watch and lure only).
18. Visible state: `Obj(..., marks=[(field, threshold, glyphs, anchor, tone)])` stamps a few ASCII glyphs at an anchor while the field is above the threshold (tone: snow, frost, leaf, water, mud, glow, dust, plant), e.g. `('snowcap', .3, '.:*:.', 'roof_low', 'snow')`. Give every field that stands for something you can see (snow, leaves, frost, a dug pit, a heap; fog or prints on a case's glass; leaves, ice or flakes on a pond) a mark, so the acts that change it show it. Marks work on placed, loose, shown (drawn on the case) and kept (drawn on the pond) objects.
19. If you cannot reach the object's full count with genuinely different real acts, stop and report how many you have and why. Do not pad; the lead decides.

## 2. Authoring brief (workers)

You write 48 sequences for each object in your batch. A sequence is one purposeful physical act: Cheese (a duck) walks to the object, touches named places in order, something about the object changes, he reacts and leaves. The game runs each one natively and a harness replays it at every age. The user will not accept filler: 48 means 48 different things to do, not 48 names.

**Before you start.** Take `host`, `consumable`, `family_engine`, `wonder_routines` and `art` for each object from `engine/overhaul/animation-milestone/work-queue.json`. All five hosts run natively (lead update after the review fixes): `placed` (objects stand outside through their own system: shop habitat, decoration rooms, finished structures, garden beds), `portable` (an owned loose object Cheese has set down beside him), `keeping` (a kept fish: the host sprite is the pond or sea tank), `display` (shown in a trophy case: the host sprite is `trophy_case`; its shelves start about 100 px up, so young ages work the glass, doors and base), `wearable` (only while Cheese is wearing it; anchors are named places on his own body and are not measured). An object owes `48 - wonder_routines` sequences; the helper reads that itself. If `art` is `pending`, stop and report it.

### File format (the helper in section 3 writes it)
```
{"object": "<id from work-queue.json>", "host": "placed|portable|keeping|display|wearable",
 "fields":   {"name": [default, min, max]},      // saved state of this object; names are [a-z_]+ (no digits)
 "physics":  [[field, "rate|decay|wrap", value, when]],  // outdoors. rate: +value per second while `when` holds (.0003 is about 1 per hour); decay: eases to `value` within a minute
 "triggers": [[when, [[field, op, value]]]],     // re-applied on every physics step while `when` holds, so the rows must end the condition
 "effects":  {"name": [[target, op, value]]},    // op: set add mul max min wrap; applied once at each event
 "anchors":  {"name": {"x": 0..1, "y": 0..1}},   // fractions of the host sprite box, x from the left, y from the top
 "lines":    {"<routine id>": ["...", "..."]},   // two or three spoken lines; one per run, in rotation
 "routines": {"<object>_<slug>": {
   "label": "Present-participle phrase, no full stop",   // becomes a journal memory and appears in refusals
   "duration": 10..60, "tool": "none|wing|twig|reed", "group": "care|use|play|test|rest|weather|show|mishap",
   "track":  [[t, pose]],            // t from 0 to 1; the helper adds the rest frames at 0 and 1
   "events": [[t, "effect"]],        // when each effect lands; empty for a pure performance
   "when": [...], "prefer": [...], "ages": null | [ages], "say": null | "<routine id>",
   "obj": [[t, {"sway|lift|shake|glow|puff": 0..1}]],   // optional: how the object answers
   "pick": "hungriest|shyest"}}}     // keeping only: which fish
```
Pose keys, all 0 at rest and eased between keyframes: `x` head pushed forward (+) or pulled back (-); `y` head lowered (+) or raised (-); `b` body squat (+) or hop (-); `w` wings spread; `l`, `r` left or right foot lifted; `reach` wing extended; `contact` 0 to 1 touching; `anchor` the place touched; `eye` one glyph (`o O - ^ > @`); `mark` a short sound drawn by his head. No other keys: object parts are not drawn by this engine.

### Conditions
`when` is a gate (every token must hold). `prefer` only makes a routine more likely. Tokens:
- Weather, at most one: `wet` `snow` `storm` `windy` `rainbow_sky` `sun`. Also `dry` `calm` `clear` `warm` `cold`.
- Time, at most one: `dawn` `day` `dusk` `night` `night_late` `dawn_or_day`. Season: `spring` `summer` `fall` `winter` `growing`.
- Cheese: `tired` `lonely` `sad`. In `prefer` only: `happy` `grumpy` `curious` `young` `grown` `elder` (gate by age with `ages`).
- Negations that work: `!wet !snow !storm !windy !cold !night !night_late !dawn !dusk !summer !fall !winter !rainbow_sky !tired !lonely !sad`. No others.
- Field comparisons: `rain>.3`, `swing<=.2` (`< <= > >=` only), also with `!`. On a keeping host: `fish_hunger fish_mood fish_health fish_trust fish_growth fish_count` (the best fish of this species) and `pond_clarity pond_algae pond_leaves pond_ice pond_oxygen pond_plants pond_flakes pond_bell`.
- Never: bare flag words (`powered`, `open`, `covered`, `tarp`, `oiled`); `snow` with `dry` or `warm`; `night` with `!night_late`; `growing` with `cold` or `winter`; `storm` unless the tool is `none`, `wet` is listed and the duration is 30 or more. For two bounds on one field, keep the band at least .3 wide. Every tag and negation above was run through the harness as a gate at `cfaaeb2`.

### Effect targets
- A field of this object.
- `obj.dirt`, `obj.wetness`, `obj.condition` (0 to 1): the object's real drawn wear. Cleaning lowers dirt; a mishap may lower condition. Use these instead of inventing a `dirt` field.
- `need.fun`, `need.social`, `need.energy`, `need.cleanliness` with `add`, at most 3. Using any object already lifts its usual need, so give a need row to at most 8 routines, where the act itself is the reason. Never `need.hunger`.
- Keeping hosts only: `subject.hunger|mood|health|trust|growth` (the chosen fish) and `keeping.clarity|algae|leaves|ice|oxygen|plants|flakes|bell` (the pond).
The engine silently ignores anything else; the helper refuses it.

### Anchors and reach
- Fractions are of the whole host sprite box, blank margin included. Host sprite: the object itself (placed, portable); `koi_pond` for freshwater fish; `infinity_pool` for pufferfish, swordfish, sturgeon and ancient_dragon_fish; `trophy_case` for display. Wearable anchors are places on Cheese's own body, named but not measured.
- Print the drawing first (`python3 engine/animation-authoring/rep.py <sprite id>`): each row shows its y fraction and its height in px above the ground, with an x ruler in tenths. Put anchors on ink, and do not reuse a name the drawing already has.
- A contact is in reach when its height is at most body x 1.05 (tool `none`: bill, belly, feet), x 1.1 (`wing`) or x 1.6 (`twig`, `reed`):

| px | hatchling | duckling | juvenile | young_adult | adult | mature | elder | legendary |
|---|---|---|---|---|---|---|---|---|
| body | 60 | 79 | 97 | 110 | 118 | 124 | 116 | 124 |
| none | 63 | 82 | 101 | 115 | 123 | 129 | 121 | 129 |
| wing | 66 | 86 | 106 | 121 | 129 | 135 | 127 | 135 |
| twig, reed | 96 | 126 | 154 | 176 | 188 | 197 | 185 | 197 |

- Keep contacts low. Each age needs at least a third of the object's sequences in reach (16 of 48: so 16 at or under 63 px), and adults two thirds (32 of 48). Parts above about 135 px (a swing's pivot, a tower top, a tall lamp's shade) are looked at, shouted at or thrown at, not touched.
- An anchor is held: a keyframe without one keeps the last, and reach counts every anchor held while `contact` is rising or above .05. Name an anchor only on a keyframe that touches it.
- `ages` is also for strength and size: `GROWN` for tipping, hauling or cranking; `YOUNG` for squeezing inside or under.
- `obj`: `sway` and `shake` for things a duck could really move; `lift` only for something he could carry (`liftable=True`); `glow` and `puff` draw sparks or puffs at the touched place. Not available on keeping, display or wearable hosts.

### Making 48 different acts
Plan first: a table of 48 one-line acts in eight groups, 4 to 9 in each (fewer for a wonder that already has some; the helper scales the bounds).
`care` clean, dry, mend, protect, tidy around it. `use` what it is for, one act per control or mode. `play` games he invents with it. `test` curiosity: taste, tap, weigh, measure, balance, listen. `rest` lean, nap, shelter, shade, sulk. `weather` what rain, snow, wind, frost or heat did to it, gated on a field that physics moved, never on the tag alone. `show` perform, pose, present, argue with it. `mishap` stuck, slipped, startled, knocked over, and the recovery.

Two routines are the same act unless at least two of these differ: (1) what it does, by effect rows and not by effect name; (2) which places it touches, in order; (3) how the body moves, as a coarse path of `x y b w` with repeats ignored; (4) what he uses: nothing, wing or stick. The helper enforces this. The reviewer also reads labels side by side: if two labels could swap tracks and nobody would notice, one is rejected.
- State must matter. Every field gates or attracts another routine (rain pools, so it can be tipped out, so it cannot be tipped when empty). Every effect is used. Opposites (open and close) count as two only when touches and body differ.
- Siblings (three fountains, a red and a blue cap) each get their own 48, built from what differs in the drawing and in what the thing is. Never copy a sibling's file and rename it.
- If `family_engine` is set, read that family's JSON in `engine/client/animation/` first. Do not repeat its sequences, and do not declare a field it already owns.
- Consumables: Cheese never eats, drinks, plants, spends or uses the thing up here. Handle it as an object: carry, sniff, guard, stack, balance, hide, offer, resist.
- Sea-tank fish: Cheese stays on the rim. No bill or wing in the water.

### Forbidden
- Relabels: the same act at another time, weather, season, mood or age; mirrored left and right; faster or slower; once versus three times; a new `mark` or `eye`.
- Padding to pass a check: extra keyframes, alias anchors or effects, unused keys. When the helper says "same act", write a different act.
- Invented things: items, coins, rewards, finds, food, visitors, tools (only a twig or a reed, in at most 8 of 48, for prodding or fishing something out), or parts the drawing does not have.
- Any change to inventory, money or quantities.
- Contact out of reach or on empty air; an effect with no touch (except at most 4 `far=True` acts: a throw, a shout, a breath).
- Acts a duck or the object could not physically do (lifting a fountain, climbing a pole), and labels that promise what the track does not show.
- Routines stamped out by a loop or a list of names.

### Cheese's voice (`say=`)
Give lines to 12 to 20 routines per object, two or three each, 90 characters at most. Cheese is deadpan, cheeky and pleased with himself; he holds grudges against objects and thinks about bread. Short flat sentences, first person, reacting to what just physically happened. Crude words are fine when earned (arse, crap, shit, piss) and are never censored or softened. Do not explain the joke, narrate the action, gush, or pun for filler. In the game already: "OW. Shit. Okay. Zero stars, would touch again." and "Built it. Wrecked it. Character development." Rejected: "Wheee, this is so much fun!", "I am pushing the swing.", "Oh sh*t!".

### Worked example: `tire_swing` (placed; passes the harness natively at `cfaaeb2`)
The tyre hangs 22 to 168 px above the ground and its hole is at 59 to 117 px, so low contacts suit every age. The pivot is about 445 px up.
```python
from rep import Obj, k, YOUNG, GROWN
o = Obj('tire_swing', 'placed',
        fields=dict(swing=(0, 0, 1), rain=(0, 0, 1)),
        physics=[('swing', 'decay', 0, 'always'), ('rain', 'rate', .002, 'wet'), ('rain', 'rate', -.0002, 'dry&warm')],
        effects=dict(push=[('swing', 'set', 1)], wedge=[('swing', 'add', .4)], pour=[('rain', 'mul', .15)]),
        anchors=dict(tyre_low=(.5, .91), hole=(.5, .85), tyre_side=(.4, .78), post_foot=(.11, .95)))
o.r('shove_and_duck',  # v2: add act=('shove', 'tyre') to every o.r call 'Shoving the tyre away and dropping flat before it swings back over him', 18, 'wing',
    [k(.15, 'tyre_low', reach=.6, w=.5), k(.3, 'tyre_low', x=.4, b=-.3, w=1, mark='hup'), k(.5, y=1.4, b=.9, eye='O'), k(.7, y=1.4, b=.9, eye='-', mark='whoosh'), k(.88, eye='^')],
    [(.3, 'push')], g='play', prefer=['swing<.2', 'happy'], obj=[(.3, dict(sway=.2)), (.45, dict(sway=1)), (.6, dict(sway=-1)), (.75, dict(sway=.5))])
o.r('tip_out_rain', 'Tipping the tyre up on its rope so the pooled rain runs out over his feet', 22, 'wing',
    [k(.15, 'tyre_low', reach=.5, w=.4), k(.35, 'tyre_low', y=-.4, b=-.3, w=1, mark='hng'), k(.55, 'hole', x=.3, y=.4, b=.5, mark='glug'), k(.75, x=-.5, l=1, eye='-', mark='ugh'), k(.9, eye='^')],
    [(.55, 'pour')], g='weather', when=['!wet', 'rain>.3'], ages=GROWN, obj=[(.35, dict(sway=.6)), (.6, dict(sway=.6, shake=.3)), (.8, dict(sway=0))])
o.r('wedged_in_hole', 'Jamming his head into the hole to the shoulders, sticking, and hauling back out with a pop'  # v2: shown='head', 24, 'none',
    [k(.15, x=.5, eye='>'), k(.3, 'hole', x=1.1, y=-.3, b=.8, mark='oof'), k(.5, 'hole', x=1.1, y=-.3, b=1, l=1, eye='O', mark='...'), k(.68, 'hole', x=1.2, y=-.3, b=1, r=1, w=1, mark='POP'), k(.85, x=1.6, y=.9, b=.6, eye='@')],
    [(.3, 'wedge'), (.68, 'wedge')], g='mishap', prefer=['young', 'grumpy'], obj=[(.3, dict(sway=.5)), (.5, dict(shake=.6)), (.68, dict(sway=-.6)), (.85, dict(sway=.2))],
    say=[<lines of your own: samples here are never reused>])
# ... 45 more routines ...
o.emit()   # o.emit(need=3) runs these three as a draft
```
Why these three count: different purpose (a game, a chore the rain caused, an accident), different touches (tyre bottom; bottom then hole; hole three times), different body paths, and each changes state that gates or attracts a routine.

Rejected:
- `sunset_push`, "Giving the tyre a dreamy sunset push": the shove again with `when=['dusk']`, a new label, a new `mark` and one extra keyframe. Same touch, same body, same effect. The harness alone would pass it; the helper and the reviewer do not.
- `oil_pivot`, "Oiling the squeaky pivot with a long-handled oil can and finding a coin in the grass": the pivot is about 445 px up (an adult with a stick reaches 188), the oil can is an invented tool nobody draws, the coin is an invented reward, and its `oiled` field gates nothing.

## 3. Authoring format (workers)

Write one generator per batch, `engine/animation-authoring/rep_<batch>.py`, in the style of the example. It imports the shared helper `engine/animation-authoring/rep.py` (the lead installs it from the appendix; never edit it) and emits `engine/client/animation/repertoire/<object>.json`. Those are the only files you write.
- `Obj(id, host, fields=, effects=, anchors=, physics=(), triggers=(), on=None, liftable=False)`: `anchors` is `{name: (x, y)}`; `on` is the host sprite for keeping and display objects. It refuses anchors on empty air, anchor names the drawing owns, and effect rows that would do nothing.
- `k(t, anchor=None, **pose)`: a keyframe. Giving an anchor means touching it (`contact=1`).
- `o.r(slug, label, seconds, tool, [keyframes], [(t, effect)], g=group, when=[], prefer=[], ages=None, say=[lines], obj=[(t, dict)], pick=None, far=False)`: the id becomes `<object>_<slug>`. It refuses undrawn keys, events without a touching keyframe, tags the harness cannot stage, gates nothing can reach, contacts out of reach, and an act too close to an earlier one. It orders `when` tokens the way the harness needs.
- `o.emit()`: checks the set (the object's full need, every effect used, every field read, 4 to 9 per group, the per-age floor) and writes the JSON. `o.emit(need=12)` is a draft run only.
- To save tokens, name a shared pose fragment once (`crouch = dict(y=1, b=.6)`) and keep keyframes on one line. Do not generate routines in loops.

## 4. Checklist before you return (workers)

Run from the repository root of your own worktree (the lead creates it with `.venv` and `engine/node_modules` linked in).
1. `python3 engine/animation-authoring/rep_<batch>.py` ends without an assertion for every object and prints the per-age and per-group counts.
2. `node engine/scripts/build-repertoire.mjs` rebuilds the bundle.
3. `node engine/scripts/export-repertoire-reach.mjs` reports `"unreachable":0`. The `reachableAges` it writes for each of your routines are never fewer than the helper counted.
4. `.venv/bin/python engine/check_repertoire.py --objects a,b,c` prints `"result": "PASS"`.
5. `node --test engine/tests/repertoire.test.mjs` passes.
6. Read your 48 labels group by group. Rewrite any pair that could swap tracks unnoticed, and any label that promises something the track does not show.
7. Return: the files you wrote; for each object the routine count, per-age counts, per-group counts, the number of routines with lines, and the two result lines from steps 4 and 5; the 48 labels by group; and anything you could not make different (say so, do not pad). Leave `repertoire.json` and `repertoire-reach.json` out of your commit unless the lead says otherwise.
8. If the helper or the harness refuses something you believe is right, or a failure comes from outside your files (blocked host, pending art, a crash in the harness), stop and report it. Do not work around it.

## Appendix (lead): `engine/animation-authoring/rep.py`

Tested at `cfaaeb2` with nothing written to the repository. It emits the example above, and its reach figures equal the exporter's (27, 59 and 59 px). A mechanical 59-routine set went through `emit()` at the full 48 threshold and then passed the native harness at all eight ages (472 runs), one routine per `when` token. It refuses both rejected routines, a padded copy, an anchor on empty air, an undrawn key, an event in the air, an unreachable gate, a mood tag in `when` and `need.hunger`.

It is stricter than the two committed pilots and refuses both as written: `koi.json` uses tool `rake` and `obj` on a keeping host, and `scarf_red.json` has an event with no touch. The thresholds are proposals for you to set: 16 and 32 routines in reach per age, 4 to 9 per group, twig or reed as the only tools, at most 4 `far` acts, and the extra `group` key (the engine ignores it; reviewers can sort by it).
```python
"""Shared helper for repertoire generators. Workers import it and never edit it. It is stricter than
check_repertoire.py on purpose: it refuses relabels, undrawn keys, contacts on empty air and gates nothing can reach."""
import json, os, re, subprocess
from pathlib import Path
ENG = Path(os.environ.get('REP_ENGINE') or Path(__file__).resolve().parent.parent)
OUT = Path(os.environ.get('REP_OUT') or ENG / 'client/animation/repertoire')
AGES = ['hatchling', 'duckling', 'juvenile', 'young_adult', 'adult', 'mature', 'elder', 'legendary']
YOUNG, GROWN = AGES[:2], AGES[2:]
BODY = dict(zip(AGES, (60.4, 78.7, 96.6, 110.2, 117.7, 123.5, 116., 123.5)))  # px, repertoire-reach.json bodyHeight rounded down
TOOLS = dict(none=1.05, wing=1.1, twig=1.6, reed=1.6)  # reach = body height x factor (export-repertoire-reach.mjs)
GROUPS = ('care', 'use', 'play', 'test', 'rest', 'weather', 'show', 'mishap')
POSE = {'x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor'}
TAGS = set('''always wet dry snow storm windy calm warm cold sun night day dawn dusk night_late dawn_or_day clear rainbow_sky growing spring summer fall winter
 tired lonely sad !wet !snow !storm !windy !cold !night !night_late !dawn !dusk !summer !fall !winter !rainbow_sky !tired !lonely !sad'''.split())
MOODS = {'young', 'grown', 'elder', 'happy', 'grumpy', 'curious'}  # prefer only: the harness cannot stage them
REAL = dict(subject=('hunger', 'mood', 'health', 'trust', 'growth'), keeping=('clarity', 'algae', 'leaves', 'ice', 'oxygen', 'plants', 'flakes', 'bell'), need=('fun', 'social', 'energy', 'cleanliness'))
CMP = re.compile(r'^!?([a-z_]+)(<=|>=|<|>)(-?[0-9.]+)$')
JS = ("import {itemSprite as s,itemWorldScale as w} from './client/ultra-items.mjs';const i=process.argv[1],m=s(i,0,{state:{keeping:{setup:true,fish:[]}}});"
      "console.log(JSON.stringify({w:m.width,art:m.art.map(String),row:7.5*w(i)*(m.detailScale||1)*1.5,ground:m.anchors?.entry?.y??m.art.length-1,named:Object.keys(m.anchors||{})}))")


def sprite(item):
    return json.loads(subprocess.run(['node', '--input-type=module', '-e', JS, item], cwd=ENG, capture_output=True, text=True, check=True).stdout)


def k(t, at=None, **pose):
    """Keyframe at fraction t. `at` = the anchor being touched (sets contact=1). Only name an anchor on a keyframe that touches it."""
    return [t, dict(pose, anchor=at, contact=pose.get('contact', 1)) if at else pose]


class Obj:
    def __init__(self, oid, host, fields, effects, anchors, physics=(), triggers=(), on=None, liftable=False):
        """anchors = {name: (x, y)} fractions of the host sprite; on = that sprite for keeping/display (koi_pond, infinity_pool, trophy_case)."""
        self.d = d = dict(object=oid, host=host, fields={f: list(v) for f, v in fields.items()}, physics=[list(p) for p in physics],
                          triggers=[[w, [list(r) for r in rows]] for w, rows in triggers], effects={n: [list(r) for r in rows] for n, rows in effects.items()},
                          anchors={n: dict(x=x, y=y) for n, (x, y) in anchors.items()}, lines={}, routines={})
        self.liftable, self.sigs, self.group, self.reach, self.far, self.h = liftable, {}, {}, {}, 0, dict.fromkeys(anchors, 0)
        self.spot = {n: (round(x * 8), round(y * 8)) for n, (x, y) in anchors.items()}  # where a touch is, on a coarse grid (about 15 px once measured)
        assert host in ('placed', 'portable', 'keeping', 'display', 'wearable') and (on is None) == (host not in ('keeping', 'display')), oid + ': host/on'
        assert all(re.fullmatch('[a-z_]+', f) and not f.startswith(('pond_', 'fish_')) and f != 'history' for f in fields), oid + ': field names are [a-z_]+'
        for n, rows in d['effects'].items():
            for t, op, v in rows:
                a, _, b = t.partition('.')
                ok = t in fields or (b in REAL.get(a, ()) and (a != 'need' or (op == 'add' and abs(v) <= 3)) and (a == 'need' or host == 'keeping'))
                assert ok and op in ('set', 'add', 'mul', 'max', 'min', 'wrap'), f'{oid}: effect {n} row {t} {op} would do nothing, or is not allowed'
        if host != 'wearable':  # worn things play on Cheese's own body: nothing to measure
            sp = sprite(on or oid)
            rows = len(sp['art']) - 1
            for n, (x, y) in anchors.items():
                cx, cy = round(x * (sp['w'] - 1)), round(y * rows)
                assert n not in sp['named'] and n not in ('contact', 'entry'), f'{oid}: anchor name {n} is taken by the drawing {sp["named"]}'
                assert any(sp['art'][r][max(0, cx - 4):cx + 5].strip() for r in range(max(0, cy - 1), min(rows, cy + 1) + 1)), f'{oid}: anchor {n} is on empty air'
                self.h[n], self.spot[n] = (sp['ground'] - y * rows) * sp['row'], (round(cx * sp['row'] / 22.5), round(cy * sp['row'] / 15))
                assert self.h[n] >= 0, f'{oid}: anchor {n} is below the ground line'

    def moves(self, f, rising):
        rows = [r[1:] for rws in [*self.d['effects'].values(), *[t[1] for t in self.d['triggers']]] for r in rws if r[0] == f]
        phys = [(op, v) for pf, op, v, _ in self.d['physics'] if pf == f]
        if rising:
            return any(op in ('set', 'max', 'wrap') or (op == 'add' and v > 0) for op, v in rows) or any(op != 'rate' or v > 0 for op, v in phys)
        return any(op in ('set', 'min', 'wrap', 'mul') or (op == 'add' and v < 0) for op, v in rows) or any(op != 'rate' or v < 0 for op, v in phys)

    def token(self, key, tok, gate):
        m = CMP.match(tok)
        if not m:
            assert tok in TAGS or (not gate and tok.lstrip('!') in MOODS), f'{key}: `{tok}` is not a tag the harness can stage in {"when" if gate else "prefer"}'
        elif m.group(1).startswith(('pond_', 'fish_')):
            assert self.d['host'] == 'keeping', key + ': fish_/pond_ fields need a keeping host'
        else:
            (default, lo, hi), v, rising = self.d['fields'][m.group(1)], float(m.group(3)), (m.group(2) in ('>', '>=')) != tok.startswith('!')
            holds, inside = (default > v, v < hi) if rising else (default < v, v > lo)
            assert inside and (holds or self.moves(m.group(1), rising)), f'{key}: `{tok}` can never come true: nothing moves {m.group(1)} that far'

    def r(self, slug, label, dur, tool, track, ev=(), *, g, when=(), prefer=(), ages=None, say=None, obj=(), pick=None, far=False):
        d, key, tr = self.d, self.d['object'] + '_' + slug, [[0, {}], *track, [1, {}]]
        when = sorted(when, key=lambda t: (not t.startswith('!'), t == 'storm'))  # the harness stages tokens in order: negations first, storm last
        assert key not in d['routines'] and tool in TOOLS and g in GROUPS and 10 <= dur <= 60 and len(track) >= 3, key + ': id, tool, group, duration or too few keyframes'
        assert [t for t, _ in tr] == sorted({t for t, _ in tr}) and all(set(q) <= POSE for _, q in tr), key + ': track order, or a key the renderer does not draw'
        [self.token(key, tok, True) for tok in when], [self.token(key, tok, False) for tok in prefer]
        assert 'storm' not in when or (tool == 'none' and 'wet' in when and dur >= 30), key + ': a storm routine is a long tool-free shelter that also lists `wet`'
        for t, name in ev:
            touching = any(abs(qt - t) < .011 and q.get('contact', 0) >= .5 and q.get('anchor') for qt, q in tr)
            assert name in d['effects'] and .1 <= t <= .9 and (touching or far), f'{key}: event {name} at {t} has no touching keyframe'
        self.far += bool(far)
        held, last = [], None
        for _, q in tr:
            last = q.get('anchor') or last
            held.append(last)
        assert all(a in d['anchors'] for a in held if a), key + ': undeclared anchor'
        high = max([self.h[a] for i in range(len(tr) - 1) if max(tr[i][1].get('contact', 0), tr[i + 1][1].get('contact', 0)) > .05 for a in held[i:i + 2] if a] or [0])
        self.reach[key] = [a for a in AGES if (not ages or a in ages) and high <= BODY[a] * TOOLS[tool]]
        assert self.reach[key], f'{key}: contact {high:.0f}px up is out of reach for every allowed age'
        assert all(set(q) <= {'sway', 'lift', 'shake', 'glow', 'puff'} and (self.liftable or 'lift' not in q) for _, q in obj), key + ': obj keys (lift needs liftable=True)'
        assert not obj or d['host'] in ('placed', 'portable'), key + ': obj reactions would move the whole pond or case, or nothing at all'
        touch = [self.spot[q['anchor']] for _, q in tr if q.get('anchor') and q.get('contact', 0) >= .5]
        touch = tuple(p for i, p in enumerate(touch) if not i or p != touch[i - 1])  # touching the same place again is not a new touch
        body = tuple(dict.fromkeys(tuple(round(q.get(j, 0) * 2) for j in 'xybw') for _, q in tr))
        sig = (tuple(tuple(sorted((t, op, (v > 0) - (v < 0)) for t, op, v in d['effects'][n])) for _, n in ev), touch, body, tool if tool in ('none', 'wing') else 'stick')
        for other, s in self.sigs.items():
            assert sum(a != b for a, b in zip(sig, s)) >= 2, f'{key} is the same act as {other}: change at least two of what it does, where it touches, how the body moves, what it uses'
        self.sigs[key], self.group[g] = sig, self.group.get(g, 0) + 1
        if say:
            assert len(say) >= 2 and all(len(s) <= 90 for s in say), key + ': two or three lines of at most 90 characters'
            d['lines'][key] = list(say)
        d['routines'][key] = dict(label=label, duration=dur, tool=tool, group=g, track=tr, events=[list(e) for e in ev], when=list(when), prefer=list(prefer), ages=ages,
                                  say=key if say else None, **({'obj': [list(o) for o in obj]} if obj else {}), **({'pick': pick} if pick else {}))

    def emit(self, need=48):
        d, n = self.d, len(self.d['routines'])
        used, read = {name for r in d['routines'].values() for _, name in r['events']}, ' '.join(t for r in d['routines'].values() for t in r['when'] + r['prefer'])
        per_age = {a: sum(a in v for v in self.reach.values()) for a in AGES}
        assert n >= need and used == set(d['effects']), f'{d["object"]}: {n} routines; unused effects {set(d["effects"]) - used}'
        assert all(f in read for f in d['fields']), f'{d["object"]}: every field must gate or attract some routine, or it changes nothing anyone can see'
        if need >= 48:  # a smaller `need` is a draft run, never a hand-in
            assert self.far <= 4 and all(4 <= self.group.get(g, 0) <= 9 for g in GROUPS), f'{d["object"]}: groups {self.group}, far {self.far}'
            assert min(per_age.values()) >= 16 and per_age['adult'] >= 32, f'{d["object"]}: too few routines in reach for some age {per_age}'
        head = ',\n'.join(f' {json.dumps(key)}: {json.dumps(v)}' for key, v in d.items() if key != 'routines')
        body = ',\n'.join(f'  {json.dumps(key)}: {json.dumps(r)}' for key, r in d['routines'].items())
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / (d['object'] + '.json')).write_text('{\n' + head + ',\n "routines": {\n' + body + '\n }\n}\n')
        print(d['object'], n, 'routines; in reach per age', per_age, '; groups', self.group)


if __name__ == '__main__':  # python3 engine/animation-authoring/rep.py <sprite id>: the drawing with y fraction, height in px and an x ruler in tenths
    import sys
    sp = sprite(sys.argv[1])
    n, ruler = len(sp['art']) - 1, [' '] * sp['w']
    for tenth in range(10):
        ruler[round(tenth * (sp['w'] - 1) / 10)] = str(tenth)
    print(sys.argv[1], '- anchor names already taken by the drawing:', sp['named'], '\n   y   px |' + ''.join(ruler) + '|')
    [print(f'{y / n:.2f} {(sp["ground"] - y) * sp["row"]:4.0f} |{row}|') for y, row in enumerate(sp['art']) if row.strip()]
```
