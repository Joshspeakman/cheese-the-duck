"""The ASCII edition preserves uncensored dialogue in every learning consumer."""
import pytest
from dialogue.content_filter import ContentFilter, get_content_filter

@pytest.mark.parametrize('text', ['', 'I like bread', 'What the fuck, Cheese?',
                                  'This is bullshit.', 'I am gay.', 'I disagree with religion.',
                                  'A story about drugs and violence', '<script>alert(1)</script>'])
def test_dialogue_is_not_censored(text):
    result = ContentFilter().classify(text)
    assert not result.is_blocked
    assert result.matched_terms == []
    assert get_content_filter().is_safe_to_learn(text)

def test_filter_is_shared():
    assert get_content_filter() is get_content_filter()
