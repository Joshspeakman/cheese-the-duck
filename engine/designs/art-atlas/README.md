# Current art atlas

Build a standalone, offline HTML review of the current Ultra artwork:

```sh
engine/node_modules/.bin/electron engine/designs/art-atlas/export.cjs
```

The output is `engine/artifacts/art-atlas/Cheese - Complete Art Atlas.html`.
It embeds the actual production renderer modules and three terrain backgrounds;
no server, game installation, simulation process or save is needed to view it.
The exporter records module hashes and checks the delivered HTML with external
network requests blocked. Preview screenshots and `checks.json` accompany it.

Coverage: 40 regular friends, 8 rare visitors, 774 event/encounter/recipe records,
542 items, the full 109-piece fitted wardrobe, 132 individual event sprites and
8 living pond stories. Event definitions determine whether a sprite actually
appears; text-only area events and encounters do not receive invented art.
Current shared item families and shared event assets are labeled explicitly.
The wardrobe overlaps the item catalog by 42 IDs; 67 wardrobe definitions live
outside that catalog and appear in the separate Wearables section.

Rare visitors currently remain at a fixed offset from Cheese. Six use the event
renderer; the merchant and celebrity use the visitor duck rig. Regular friends
use the friend movement animator. The atlas preserves these distinctions and
previews only sprite animation, not scene trajectories or particle emitters.
The detail view includes a game-scale comparison, all nine ages for wearable
try-on, original ASCII references, current dialogue and exportable review notes.

The atlas is a snapshot of the source at export time. It makes no gameplay edits.
Keep `pond-cast/catalog.mjs` synchronized with the underlying registries when
adding/removing definitions; the exporter reads event flags, rare visitors and
stories directly from their Python definitions each time.
