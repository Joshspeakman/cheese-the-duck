"""Tests for core.update_scheduler — periodic callback management."""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.update_scheduler import UpdateScheduler


def test_register_and_unregister():
    sched = UpdateScheduler()
    sched.register("test_sys", lambda: None, 1.0)
    stats = sched.get_stats()
    assert "test_sys" in stats
    sched.unregister("test_sys")
    stats = sched.get_stats()
    assert "test_sys" not in stats


def test_update_fires_callback():
    results = []
    sched = UpdateScheduler()
    sched.register("counter", lambda: results.append(1), 0.0, enabled=True)
    sched.update(time.time())
    assert len(results) == 1


def test_disabled_system_does_not_fire():
    results = []
    sched = UpdateScheduler()
    sched.register("counter", lambda: results.append(1), 0.0, enabled=False)
    sched.update(time.time())
    assert len(results) == 0


def test_enable_disable():
    results = []
    sched = UpdateScheduler()
    sched.register("counter", lambda: results.append(1), 0.0, enabled=False)
    sched.enable("counter")
    sched.update(time.time())
    assert len(results) == 1
    sched.disable("counter")
    results.clear()
    sched.update(time.time() + 1)
    assert len(results) == 0


def test_force_run():
    results = []
    sched = UpdateScheduler()
    sched.register("counter", lambda: results.append(1), 999.0, enabled=True)
    sched.force_run("counter")
    assert len(results) == 1


def test_exception_does_not_crash():
    sched = UpdateScheduler()
    sched.register("bad", lambda: 1 / 0, 0.0, enabled=True)
    sched.update(time.time())  # Should not raise


def test_get_stats_run_count():
    sched = UpdateScheduler()
    sched.register("counter", lambda: None, 0.0, enabled=True)
    sched.update(time.time())
    sched.update(time.time() + 1)
    stats = sched.get_stats()
    assert stats["counter"]["run_count"] >= 2
