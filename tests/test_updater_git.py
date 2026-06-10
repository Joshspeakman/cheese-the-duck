"""Regression tests for the git-based update path.

install_linux.sh drops an untracked uninstall.sh into every local install,
which used to make _update_via_git abort with "Local changes detected" —
git-clone installs could never self-update.
"""

import subprocess

import pytest

import core.updater as updater_module
from core.updater import GameUpdater, UpdateStatus


def _git(cwd, *args):
    result = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True
    )
    assert result.returncode == 0, f"git {' '.join(args)} failed: {result.stderr}"
    return result.stdout.strip()


@pytest.fixture
def cloned_install(tmp_path, monkeypatch):
    """A local clone one commit behind its origin, like a stale install."""
    origin = tmp_path / "origin"
    origin.mkdir()
    _git(origin, "init", "-b", "main")
    _git(origin, "config", "user.email", "test@example.com")
    _git(origin, "config", "user.name", "Test")
    (origin / "game.txt").write_text("v1")
    _git(origin, "add", "game.txt")
    _git(origin, "commit", "-m", "v1")

    clone = tmp_path / "install"
    _git(tmp_path, "clone", "-q", str(origin), str(clone))
    _git(clone, "config", "user.email", "test@example.com")
    _git(clone, "config", "user.name", "Test")

    # Origin moves ahead (a release)
    (origin / "game.txt").write_text("v2")
    _git(origin, "add", "game.txt")
    _git(origin, "commit", "-m", "v2")

    monkeypatch.setattr(updater_module, "GAME_DIR", clone)
    return clone


def _make_updater(monkeypatch):
    updater = GameUpdater()
    # Don't touch pip/venv in tests
    monkeypatch.setattr(updater, "_ensure_venv_deps", lambda: None)
    return updater


def test_git_update_succeeds_with_untracked_files(cloned_install, monkeypatch):
    """Untracked files (e.g. uninstall.sh) must not block the update."""
    (cloned_install / "uninstall.sh").write_text("#!/bin/bash\n")

    updater = _make_updater(monkeypatch)
    status = updater._update_via_git()

    assert status == UpdateStatus.UPDATE_COMPLETE, updater._last_check_error
    assert (cloned_install / "game.txt").read_text() == "v2"
    # The untracked file survives the update
    assert (cloned_install / "uninstall.sh").exists()


def test_git_update_blocked_by_tracked_changes(cloned_install, monkeypatch):
    """Real local modifications must still abort the update."""
    (cloned_install / "game.txt").write_text("my local hack")

    updater = _make_updater(monkeypatch)
    status = updater._update_via_git()

    assert status == UpdateStatus.UPDATE_FAILED
    assert "Local changes" in (updater._last_check_error or "")
    # The local modification is preserved
    assert (cloned_install / "game.txt").read_text() == "my local hack"
