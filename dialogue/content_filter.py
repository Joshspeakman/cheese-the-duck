"""Unrestricted dialogue learning for the ASCII engine edition.

The API remains compatible with vocabulary, memory, ambient dialogue and voice
systems. Words are never redacted, replaced or rejected on content grounds.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List

class FilterCategory(Enum):
    PROFANITY = "profanity"
    SLURS = "slurs"
    SEXUAL = "sexual"
    LGBTQ = "lgbtq"
    ANTI_CHRISTIAN = "anti_christian"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    DRUGS = "drugs"

class Severity(Enum):
    HARD = "hard"
    SOFT = "soft"

@dataclass
class FilterResult:
    is_blocked: bool = False
    categories: List[FilterCategory] = field(default_factory=list)
    severity: Severity = Severity.SOFT
    matched_terms: List[str] = field(default_factory=list)

class ContentFilter:
    def is_safe_to_learn(self, text: str) -> bool:
        return True

    def classify(self, text: str) -> FilterResult:
        return FilterResult()

_filter_instance = ContentFilter()

def get_content_filter() -> ContentFilter:
    return _filter_instance
