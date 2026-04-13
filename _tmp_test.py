from audio.sound import get_music_context
tests = [
    ("sunny", "dawn", "content", "energetic"),
    ("sunny", "morning", "content", "energetic"),
    ("sunny", "midday", "content", "happy"),
    ("sunny", "afternoon", "content", "calm"),
    ("sunny", "evening", "content", "mysterious"),
    ("sunny", "dusk", "content", "mysterious"),
    ("sunny", "night", "content", "sad"),
    ("sunny", "late_night", "content", "calm"),
    ("stormy", "night", "content", "stormy"),
    ("rainy", "morning", "content", "mysterious"),
    ("snowy", "midday", "content", "calm"),
    ("windy", "midday", "content", "happy"),
    ("sunny", "day", "happy", "happy"),
    ("sunny", "day", "miserable", "sad"),
]
all_ok = True
for w, t, m, expected in tests:
    result = get_music_context(weather=w, time_of_day=t, duck_mood=m)
    ok = result.value == expected
    if not ok:
        all_ok = False
    print(f"  {t:12s} {w:8s} {m:10s} -> {result.value:15s} {'OK' if ok else 'FAIL expected=' + expected}")
print("ALL OK" if all_ok else "SOME FAILURES")
