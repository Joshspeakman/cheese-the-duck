# Fish: honest 48-sequence outline test (2026-11-13)

What a fish IS in the game today: `g.fishing.fish_caught[species]` is a list of catch
records (size, spot, bait, date, record flag). A catch lowers the pond's wild fish
level (`ecology.fish`). No caught fish is kept anywhere physical. Each species has real
data: rarity, size range, spots (pond/river/lake/ocean/secret cove), time of day,
season, preferred bait, fun fact.

So only two things can back an interaction without inventing objects:
- **A. the catch record** (Cheese recalling, comparing, telling)
- **B. wild fish of that species at Home Pond**, only where the species' own spots,
  season and time allow, scaled by the pond's fish level.

## Koi (pond species: B and A available)

Kept (distinct purpose + contact/state change + koi-specific):
1. Dawn rise: watch koi break the surface (B, time-gated)
2. Feed crumbs at the bank (B; consumes real bread through the original handler)
3. Koi kiss: koi mouths at Cheese's bill at the surface (B)
4. Paddle while koi nibble his feet (B, warm season)
5. Skim fallen leaves off the koi's patch (B, fall; changes pond litter)
6. Break an air hole in the ice for them (B, winter; changes pond ice)
7. Shade the shallows with a lily pad in a heat wave (B)
8. Follow a koi along the bank (B; Cheese's walk path follows it)
9. Count the koi (B; reads actual fish level)
10. Spread wings to show the record size (A; reads record)
11. Tell a visitor the koi fun fact (A + visitor company)
12. Try to catch one (real fishing minigame; existing system)
13. Clear algae from the koi's corner (B; changes clarity)
14. Rain watch: koi rising to raindrops (B, wet)

Struck as variants of the above (label, time, mood, or onlooker only): watch at dusk,
watch at night, sad watching, count again with a friend, feed with a visitor, admire
colours, name a koi, wave at koi, sleepy watching... (about 20 more lines, all
relabels of 1, 2, 8 or 9).

**Result: about 14 genuinely distinct sequences**, not 48.

## Swordfish (ocean species: A only)

Never present at Home Pond (spots: ocean), so B is impossible without inventing fish.
Kept: recall the catch, compare the record size, act out the fight, tell a visitor.
**Result: about 4.** The same holds for every ocean, river and lake species.

## Conclusion

With today's game state, fish top out around 14 (pond species) and 4 (others). Getting
to 48 honestly needs a new physical home for caught fish (for example an aquarium or
keeping pond where catches can actually live), which is new gameplay and the user's call.
