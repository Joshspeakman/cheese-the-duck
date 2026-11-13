# Keeping pond (user decision 2026-11-13)

Catches can really live in a placed `koi_pond` (existing shop item, "Beautiful fish
friends!"). Catching is unchanged. Nothing is fabricated: every kept fish is one real
catch record, and each record can be kept at most once.

## Who can live there (honest physical limits)
Freshwater species that fit (≤100 cm): minnow, goldfish, carp, bass, catfish, trout,
koi, salmon, golden_koi, ghost_fish. Capacity: total kept length ≤ 320 cm per pond.
Cannot be kept here (open decision for the user): pufferfish (saltwater), swordfish
(ocean, 1–3 m), sturgeon (1–4 m), ancient_dragon_fish (2–5 m).

## Native state (`engine/keeping.py`, saved in the koi_pond's object state)
- pond: clarity, algae, leaves, ice, oxygen, plants, flakes (floating food), bell
  (feeding-bell conditioning), plus `fish: [...]`
- fish: id, species, catch (caught_at), size (from the catch, grows slowly), name,
  hunger, mood, health, trust, growth
- physics (hours scale): hunger rises; health falls when hungry, water dirty or oxygen
  low; mood follows hunger, crowding, clarity; algae grows in sun; leaves fall in fall;
  ice in cold; oxygen drops in heat; growth only when fed and healthy.
- species traits: active hours (catfish/ghost night, goldfish/trout morning), dwelling
  (bottom: carp, catfish; top: goldfish, minnow), schooling (minnow), glow (ghost fish
  at night, golden koi at dawn), jumpiness (trout, bass, salmon), whiskers (catfish, carp).
- keep(catch) / release(fish): release returns it to the wild pond (ecology fish +),
  marks the catch released so it cannot be kept again.

## 48 archetypes (each species' version differs by its own behaviour beats)
Feeding: flakes, hand-feed from the bill, treat (real fish_treat consumed through its
handler), feeding-bell conditioning, sinking pellet (bottom dwellers).
Water care: net leaves, scrub algae, top up water, feather water test, plant a cutting,
ice air-hole, lily-pad shade, skim pollen, clear weed tangle, splash-aerate.
Health: fin check, medicine (real item via handler), rescue a jumper (event), separate a
squabble, calm after a storm.
Bond/play: koi kiss, follow-the-wingtip trick, peekaboo, edge race, leaf-boat push, chin
tickle, feet nibble, bubble talk, reed-hoop jump (high trust), fetch a floating berry.
Observation: measure on the marker stick, compare with the wild record, sketch its
pattern, dawn rise, night watch (sleep vs active by species), rain ripples, schooling.
Management: keep a fresh catch, release to the wild, name it, introduce a newcomer, count.
Species signature (one each): catfish whisker-feel, ghost-fish glow, golden-koi shimmer,
goldfish bubble-nose, minnow swirl, bass insect jump, trout rapid leap, salmon current
push, carp mud stir, koi sunset colours.
Social: show a visitor, visitor feeds it, sulking fish apology, cold-night cover.

## Build order
1. keeping.py core + art of real fish in the pond + journal keep/release + checks. (commit)
2. Routines in batches through the generalised repertoire engine, with per-species
   distinctness checks. (commits)
3. Visitor roles at the keeping pond.
