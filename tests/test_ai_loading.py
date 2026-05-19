from __future__ import annotations

from types import SimpleNamespace

from core.game import Game
from duck.duck import Duck
from dialogue.llm_chat import LLMChat


class _FakeLLM:
    def __init__(self):
        self.started = False
        self.ready = False
        self.loading = True
        self.last_error = None
        self.duck_brain = None
        self.history = None

    def start_background_loading(self):
        self.started = True
        return True

    def is_ready_for_inference(self):
        return self.ready

    def is_loading(self):
        return self.loading

    def is_available(self):
        return self.ready

    def get_last_error(self):
        return self.last_error

    def set_duck_brain(self, duck_brain):
        self.duck_brain = duck_brain

    def set_conversation_history(self, history):
        self.history = history


class _FakeBrain:
    def __init__(self):
        self.llm = None
        self.conversation_memory = SimpleNamespace(get_recent_context=lambda limit: [])

    def set_llm_chat(self, llm):
        self.llm = llm


def test_llm_response_does_not_sync_load_while_background_loading(monkeypatch):
    llm = object.__new__(LLMChat)
    llm._available = False
    llm._loading = True
    llm._disabled = False
    llm._llama = None
    llm._last_error = None

    def fail_sync_load():
        raise AssertionError("synchronous model load should not run")

    llm._check_availability = fail_sync_load

    assert llm.generate_response(Duck.create_new(), "hello") is None


def test_game_enters_ai_loading_screen_until_model_ready(monkeypatch):
    fake_llm = _FakeLLM()

    import dialogue.llm_chat as llm_module

    monkeypatch.setattr(llm_module, "get_llm_chat", lambda background=True: fake_llm)
    monkeypatch.setattr(
        "core.game.get_settings",
        lambda: SimpleNamespace(gameplay=SimpleNamespace(ai_enabled=True)),
    )

    game = object.__new__(Game)
    game._state = "playing"
    game.duck_brain = _FakeBrain()
    game._ai_loading_timeout = 90.0

    assert game._enter_ai_loading_if_needed(target_state="playing") is True
    assert fake_llm.started is True
    assert game._state == "ai_loading"
    assert game.duck_brain.llm is fake_llm

    fake_llm.ready = True
    fake_llm.loading = False
    game._update_ai_loading()

    assert game._state == "playing"
    assert game._ai_loading_llm is None
