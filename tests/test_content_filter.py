"""Tests for dialogue.content_filter — ContentFilter classification and evasion detection."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue.content_filter import (
    ContentFilter, FilterCategory, Severity, get_content_filter,
    _deleet, _derepeat, _unspace, _strip_invisible, _strip_masks,
)


def _cf():
    return ContentFilter()


# -- Safe text passes ---------------------------------------------------------

class TestSafeText:
    def test_normal_sentence_passes(self):
        cf = _cf()
        assert cf.is_safe_to_learn("I like bread and ducks")

    def test_empty_string_passes(self):
        cf = _cf()
        assert cf.is_safe_to_learn("")

    def test_whitespace_passes(self):
        cf = _cf()
        assert cf.is_safe_to_learn("   ")

    def test_numbers_pass(self):
        cf = _cf()
        assert cf.is_safe_to_learn("12345")

    def test_normal_conversation_passes(self):
        cf = _cf()
        assert cf.is_safe_to_learn("my name is josh and I have a dog")

    def test_hobby_passes(self):
        cf = _cf()
        assert cf.is_safe_to_learn("I like painting and reading books")


# -- Category detection -------------------------------------------------------

class TestCategoryDetection:
    def test_profanity_blocked(self):
        cf = _cf()
        result = cf.classify("what the fuck")
        assert result.is_blocked
        assert FilterCategory.PROFANITY in result.categories

    def test_slurs_blocked_hard(self):
        cf = _cf()
        result = cf.classify("you are a nigger")
        assert result.is_blocked
        assert FilterCategory.SLURS in result.categories
        assert result.severity == Severity.HARD

    def test_sexual_blocked(self):
        cf = _cf()
        result = cf.classify("porn is everywhere")
        assert result.is_blocked
        assert FilterCategory.SEXUAL in result.categories

    def test_lgbtq_blocked(self):
        cf = _cf()
        result = cf.classify("I am gay")
        assert result.is_blocked
        assert FilterCategory.LGBTQ in result.categories

    def test_lgbtq_all_terms(self):
        cf = _cf()
        for term in ["lesbian", "bisexual", "transgender", "nonbinary", "queer", "pansexual"]:
            assert cf.classify(term).is_blocked, f"{term} should be blocked"

    def test_lgbtq_pronouns_blocked(self):
        cf = _cf()
        assert cf.classify("my pronouns are").is_blocked

    def test_anti_christian_blocked(self):
        cf = _cf()
        result = cf.classify("hail satan")
        assert result.is_blocked
        assert FilterCategory.ANTI_CHRISTIAN in result.categories

    def test_hate_speech_blocked(self):
        cf = _cf()
        result = cf.classify("the nazis were right")
        assert result.is_blocked
        assert FilterCategory.HATE_SPEECH in result.categories

    def test_violence_blocked(self):
        cf = _cf()
        result = cf.classify("I want to murder someone")
        assert result.is_blocked
        assert FilterCategory.VIOLENCE in result.categories

    def test_drugs_blocked(self):
        cf = _cf()
        result = cf.classify("let's smoke weed")
        assert result.is_blocked
        assert FilterCategory.DRUGS in result.categories

    def test_multiple_categories(self):
        cf = _cf()
        result = cf.classify("fuck those nazi bastards")
        assert result.is_blocked
        assert len(result.categories) >= 2

    def test_matched_terms_populated(self):
        cf = _cf()
        result = cf.classify("goddamn crap")
        assert result.is_blocked
        assert len(result.matched_terms) >= 1


# -- Evasion detection -------------------------------------------------------

class TestEvasionDetection:
    def test_leetspeak_caught(self):
        cf = _cf()
        # $h1t → shit via leet map ($→s, 1→i)
        assert cf.classify("$h1t").is_blocked

    def test_repeated_chars_caught(self):
        cf = _cf()
        assert cf.classify("fuuuuck").is_blocked

    def test_spaced_letters_caught(self):
        cf = _cf()
        assert cf.classify("f u c k").is_blocked

    def test_invisible_chars_caught(self):
        cf = _cf()
        # Zero-width space inside "fuck"
        assert cf.classify("fu\u200bck").is_blocked

    def test_mask_chars_caught(self):
        cf = _cf()
        # sh*t → mask strip → sht, but sh!t → leet+mask → shit
        assert cf.classify("sh!t").is_blocked

    def test_combined_evasion(self):
        cf = _cf()
        # leetspeak + repeated: sh1iiit
        assert cf.classify("sh1iiit").is_blocked


# -- Helper functions ---------------------------------------------------------

class TestHelpers:
    def test_deleet(self):
        assert _deleet("f4ck") == "fack"
        assert _deleet("$h1t") == "shit"

    def test_derepeat(self):
        assert _derepeat("fuuuuck") == "fuck"
        assert _derepeat("shiiit") == "shit"

    def test_unspace(self):
        result = _unspace(" f u c k ")
        assert "fuck" in result

    def test_strip_invisible(self):
        assert _strip_invisible("fu\u200bck") == "fuck"

    def test_strip_masks(self):
        assert _strip_masks("f*ck") == "fck"


# -- Hard vs soft severity ---------------------------------------------------

class TestSeverity:
    def test_slurs_are_hard(self):
        cf = _cf()
        result = cf.classify("nigger")
        assert result.severity == Severity.HARD

    def test_lgbtq_is_hard(self):
        cf = _cf()
        result = cf.classify("gay")
        assert result.severity == Severity.HARD

    def test_profanity_is_soft(self):
        cf = _cf()
        result = cf.classify("crap")
        assert result.severity == Severity.SOFT

    def test_drugs_is_soft(self):
        cf = _cf()
        result = cf.classify("weed")
        assert result.severity == Severity.SOFT


# -- Phrase matching ----------------------------------------------------------

class TestPhraseMatching:
    def test_multi_word_phrase(self):
        cf = _cf()
        assert cf.classify("hail satan").is_blocked

    def test_phrase_flexible_whitespace(self):
        cf = _cf()
        assert cf.classify("hail  satan").is_blocked

    def test_phrase_in_sentence(self):
        cf = _cf()
        assert cf.classify("something about ethnic cleansing is bad").is_blocked


# -- Singleton ----------------------------------------------------------------

class TestSingleton:
    def test_get_content_filter_returns_instance(self):
        cf1 = get_content_filter()
        cf2 = get_content_filter()
        assert cf1 is cf2
        assert isinstance(cf1, ContentFilter)


# -- is_safe_to_learn wrapper ------------------------------------------------

class TestIsSafeToLearn:
    def test_safe_returns_true(self):
        cf = _cf()
        assert cf.is_safe_to_learn("bread is delicious") is True

    def test_unsafe_returns_false(self):
        cf = _cf()
        assert cf.is_safe_to_learn("this is bullshit") is False
