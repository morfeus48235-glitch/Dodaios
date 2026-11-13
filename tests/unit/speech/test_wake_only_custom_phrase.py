"""A bare custom wake word is a wake-only turn, not a request for the brain.

Live 2026-11-12: with the wake word "Nova", the transcript "Nova." passed the
wake-only guard (it only knew "Jarvis"), reached a small local model as if it
were a command, and the user heard "I recognized the action but couldn't
execute it." instead of Nova listening for the actual question.
"""

from __future__ import annotations

import pytest

from dodaios.speech.pipeline import _is_wake_only


@pytest.mark.parametrize(
    "text",
    ["Nova.", "nova", "Nova!", "Hey Nova.", "OK, Nova?", "Nova. Nova.", "  NOVA  "],
)
def test_bare_custom_wake_word_is_wake_only(text: str) -> None:
    assert _is_wake_only(text, "Nova")


def test_multi_word_custom_phrase_and_its_prefix() -> None:
    assert _is_wake_only("Hey Athena Prime.", "Hey Athena Prime")
    assert _is_wake_only("athena prime", "Hey Athena Prime")


def test_accents_fold_like_the_wake_matcher() -> None:
    assert _is_wake_only("Zoé.", "Zoe")


@pytest.mark.parametrize(
    "text",
    [
        "Nova, what time is it?",
        "What time is it, Nova?",
        "Nova Scotia weather",
        "Nova Nova Nova what",
        "Novak.",
    ],
)
def test_a_request_that_names_the_wake_word_still_reaches_the_brain(text: str) -> None:
    assert not _is_wake_only(text, "Nova")


def test_built_in_jarvis_forms_are_unchanged() -> None:
    assert _is_wake_only("Hey Jarvis.")
    assert _is_wake_only("Jarvis", "Nova")
    assert not _is_wake_only("Jarvis, open the editor", "Nova")


def test_without_a_custom_phrase_nova_is_an_ordinary_word() -> None:
    assert not _is_wake_only("Nova.")
    assert not _is_wake_only("Nova.", None)
    assert not _is_wake_only("Nova.", "")


def test_short_noise_is_still_wake_only() -> None:
    assert _is_wake_only("uh", "Nova")
    assert _is_wake_only(".", None)
