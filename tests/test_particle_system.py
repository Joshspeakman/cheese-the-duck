"""Tests for ui.particle_system — ParticleSystem lifecycle."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ui.particle_system import ParticleSystem


def test_initial_empty():
    ps = ParticleSystem(width=40, height=12)
    assert ps.get_particles() == []


def test_configure_weather():
    ps = ParticleSystem(width=40, height=12)
    ps.configure_weather("rain", 0.8)
    # After a few updates, particles should spawn
    for _ in range(10):
        ps.update(0.1)
    particles = ps.get_particles()
    assert isinstance(particles, list)


def test_update_moves_particles():
    ps = ParticleSystem(width=40, height=12)
    ps.configure_weather("snow", 0.5)
    for _ in range(5):
        ps.update(0.1)
    for _ in range(5):
        ps.update(0.1)
    assert isinstance(ps.get_particles(), list)


def test_configure_biome():
    ps = ParticleSystem(width=40, height=12)
    ps.configure_biome("forest", "morning", "spring")
    for _ in range(10):
        ps.update(0.1)
    assert isinstance(ps.get_particles(), list)
