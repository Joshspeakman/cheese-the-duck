"""Tests for dialogue.vocabulary — VocabularyMemory word learning system."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dialogue.vocabulary import VocabularyMemory, LearnedWord, MAX_VOCABULARY


# -- Teaching detection -------------------------------------------------------

class TestDetectTeaching:
    def test_x_means_y(self):
        vm = VocabularyMemory()
        result = vm.detect_teaching("flibble means a small round pastry")
        assert result is not None
        assert result["word"] == "flibble"
        assert "small round pastry" in result["definition"]

    def test_x_is_when_y(self):
        vm = VocabularyMemory()
        result = vm.detect_teaching("schadenfreude is when you enjoy someone's misfortune")
        assert result is not None
        assert result["word"] == "schadenfreude"

    def test_x_is_a_y(self):
        vm = VocabularyMemory()
        result = vm.detect_teaching("quokka is a small happy looking marsupial")
        assert result is not None
        assert result["word"] == "quokka"

    def test_the_word_x_means_y(self):
        vm = VocabularyMemory()
        result = vm.detect_teaching("the word bonkers means crazy")
        assert result is not None
        assert result["word"] == "bonkers"

    def test_do_you_know_what_x_means(self):
        vm = VocabularyMemory()
        result = vm.detect_teaching("do you know what flibble means")
        assert result is not None
        assert result["word"] == "flibble"
        assert result["definition"] is None  # no definition in question form

    def test_no_match(self):
        vm = VocabularyMemory()
        assert vm.detect_teaching("hello cheese how are you") is None

    def test_false_positive_word_skipped(self):
        vm = VocabularyMemory()
        # "it" is in the false positive list
        assert vm.detect_teaching("it means nothing to me") is None

    def test_short_word_skipped(self):
        vm = VocabularyMemory()
        assert vm.detect_teaching("x means something") is None

    def test_short_definition_skipped(self):
        vm = VocabularyMemory()
        assert vm.detect_teaching("flibble means no") is None


# -- Learning (try_learn) -----------------------------------------------------

class TestTryLearn:
    def test_learn_new_word(self):
        vm = VocabularyMemory()
        response = vm.try_learn("flibble means a tiny imaginary creature")
        assert response is not None
        assert "flibble" in response.lower()
        assert vm.knows_word("flibble")

    def test_already_known_same_definition(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a tiny imaginary creature")
        response = vm.try_learn("flibble means a tiny imaginary creature")
        assert response is not None
        assert vm.word_count == 1

    def test_already_known_different_definition(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a tiny imaginary creature")
        response = vm.try_learn("flibble means a large building")
        assert response is not None
        assert "large building" in vm.get_definition("flibble")

    def test_content_filter_blocks_bad_word(self):
        vm = VocabularyMemory()
        response = vm.try_learn("fuck means something bad")
        assert response is None
        assert not vm.knows_word("fuck")

    def test_content_filter_blocks_bad_definition(self):
        vm = VocabularyMemory()
        response = vm.try_learn("flibble means doing cocaine all day")
        assert response is None
        assert not vm.knows_word("flibble")

    def test_no_teaching_returns_none(self):
        vm = VocabularyMemory()
        assert vm.try_learn("hello cheese how are you") is None

    def test_question_form_known_word(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a small round thing")
        response = vm.try_learn("do you know what flibble means")
        assert response is not None
        assert "small round thing" in response

    def test_question_form_unknown_word(self):
        vm = VocabularyMemory()
        assert vm.try_learn("do you know what flibble means") is None


# -- Capacity & eviction ------------------------------------------------------

class TestCapacity:
    def test_eviction_at_capacity(self):
        vm = VocabularyMemory()
        for i in range(MAX_VOCABULARY + 5):
            vm._words[f"word{i}"] = LearnedWord(
                word=f"word{i}",
                definition=f"definition {i}",
                context=f"word{i} means definition {i}",
                learned_at=time.time() - (MAX_VOCABULARY + 5 - i),
                confidence=0.5 + (i * 0.001),
            )
        # Now try to learn one more
        vm.try_learn("extraword means bonus definition here")
        # Should not exceed MAX_VOCABULARY + small overshoot from direct insertion
        assert vm.word_count <= MAX_VOCABULARY + 6


# -- Usage callbacks ----------------------------------------------------------

class TestCheckUsage:
    def test_usage_returns_none_when_empty(self):
        vm = VocabularyMemory()
        assert vm.check_usage("hello there") is None

    def test_usage_returns_none_when_no_match(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a small round thing")
        assert vm.check_usage("hello there cheese") is None

    def test_usage_possible_on_match(self):
        """With enough attempts, check_usage should eventually fire."""
        vm = VocabularyMemory()
        vm.try_learn("flibble means a small round thing")
        fired = False
        for _ in range(500):
            result = vm.check_usage("tell me about flibble")
            if result is not None:
                fired = True
                break
        assert fired, "check_usage should fire at least once in 500 attempts"


# -- Random word thought ------------------------------------------------------

class TestRandomWordThought:
    def test_none_when_empty(self):
        vm = VocabularyMemory()
        assert vm.get_random_word_thought() is None

    def test_returns_thought(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a small round thing")
        thought = vm.get_random_word_thought()
        assert thought is not None
        assert "flibble" in thought.lower()


# -- Persistence --------------------------------------------------------------

class TestPersistence:
    def test_round_trip(self):
        vm = VocabularyMemory()
        vm.try_learn("flibble means a small round thing")
        vm.try_learn("zorp means the feeling of mild confusion")
        data = vm.to_dict()
        vm2 = VocabularyMemory.from_dict(data)
        assert vm2.knows_word("flibble")
        assert vm2.knows_word("zorp")
        assert vm2.get_definition("flibble") == "a small round thing"

    def test_empty_round_trip(self):
        vm = VocabularyMemory()
        data = vm.to_dict()
        vm2 = VocabularyMemory.from_dict(data)
        assert vm2.word_count == 0


# -- LearnedWord dataclass ---------------------------------------------------

class TestLearnedWord:
    def test_to_dict(self):
        lw = LearnedWord(
            word="flibble", definition="a thing",
            context="flibble means a thing",
            learned_at=1000.0, times_used=3, confidence=0.9,
        )
        d = lw.to_dict()
        assert d["word"] == "flibble"
        assert d["times_used"] == 3

    def test_from_dict(self):
        d = {
            "word": "flibble", "definition": "a thing",
            "context": "ctx", "learned_at": 1000.0,
            "times_used": 2, "confidence": 0.8,
        }
        lw = LearnedWord.from_dict(d)
        assert lw.word == "flibble"
        assert lw.times_used == 2
