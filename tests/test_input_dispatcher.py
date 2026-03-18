"""Tests for core.input_dispatcher — input routing and priority."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.input_dispatcher import InputDispatcher, InputHandlerBase


class MockHandler(InputHandlerBase):
    def __init__(self, handles=True):
        self._handles = handles
        self.calls = []

    def handle(self, key, overlay):
        self.calls.append((key, overlay))
        return self._handles


def test_dispatch_global_handler():
    disp = InputDispatcher()
    h = MockHandler(handles=True)
    disp.register_global_handler(h, priority=10)
    assert disp.dispatch("q", "none") is True
    assert len(h.calls) == 1


def test_unhandled_returns_false():
    disp = InputDispatcher()
    assert disp.dispatch("x", "none") is False


def test_priority_ordering():
    order = []
    class H1(InputHandlerBase):
        def handle(self, key, overlay):
            order.append("low")
            return False
    class H2(InputHandlerBase):
        def handle(self, key, overlay):
            order.append("high")
            return False
    disp = InputDispatcher()
    disp.register_global_handler(H1(), priority=100)  # Higher number = later
    disp.register_global_handler(H2(), priority=10)   # Lower number = earlier
    disp.dispatch("x", "none")
    assert order[0] == "high"


def test_handler_returning_true_stops_chain():
    h1 = MockHandler(handles=True)
    h2 = MockHandler(handles=True)
    disp = InputDispatcher()
    disp.register_global_handler(h1, priority=10)   # Lower = fires first
    disp.register_global_handler(h2, priority=100)  # Higher = fires later
    disp.dispatch("x", "none")
    assert len(h1.calls) == 1
    assert len(h2.calls) == 0


def test_handler_exception_does_not_crash():
    class BadHandler(InputHandlerBase):
        def handle(self, key, overlay):
            raise RuntimeError("boom")
    disp = InputDispatcher()
    disp.register_global_handler(BadHandler(), priority=10)
    result = disp.dispatch("x", "none")
    assert result is False
