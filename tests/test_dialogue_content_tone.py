from __future__ import annotations

from pathlib import Path


CONTENT_ROOTS = ("dialogue", "duck", "world")
EXCLUDED_FILES = {
    Path("dialogue/content_filter.py"),
}
FORBIDDEN_SEXUAL_JOKE_TERMS = (
    "striptease",
    "sexy",
    "horny",
    "seduce",
    "kinky",
    "nude",
    "naked",
    "make out",
    "thirst trap",
    "hot and bothered",
)


def test_handwritten_dialogue_has_no_sexual_joke_terms():
    repo_root = Path(__file__).resolve().parent.parent
    offenders = []

    for root_name in CONTENT_ROOTS:
        for path in (repo_root / root_name).rglob("*.py"):
            rel_path = path.relative_to(repo_root)
            if rel_path in EXCLUDED_FILES:
                continue
            text = path.read_text(encoding="utf-8").lower()
            for term in FORBIDDEN_SEXUAL_JOKE_TERMS:
                if term in text:
                    offenders.append(f"{rel_path}: {term}")

    assert not offenders, "Remove sexual joke terms from content: " + ", ".join(offenders)
