"""Native mixer teardown regression: exercise SDL in disposable subprocesses."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run_audio(code):
    result = subprocess.run([sys.executable, '-c', code], cwd=ROOT,
                            env={**os.environ, 'SDL_AUDIODRIVER': 'dummy'},
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, (result.returncode, result.stdout, result.stderr)


def test_shutdown_waits_for_sound_creation_and_rejects_late_producers():
    run_audio('''
import threading, time
import pygame
from audio.sound import sound_engine as engine, SoundType
entered, release, finished = threading.Event(), threading.Event(), threading.Event()
original = pygame.mixer.Sound
def blocked_sound(*args, **kwargs):
    entered.set()
    assert release.wait(3)
    assert pygame.mixer.get_init(), 'mixer closed while a worker still owned it'
    return original(*args, **kwargs)
pygame.mixer.Sound = blocked_sound
engine.play_sound(SoundType.LEVEL_UP)
assert entered.wait(3)
def close():
    engine.shutdown()
    finished.set()
closer = threading.Thread(target=close)
closer.start()
assert engine._audio_stopping.wait(3)
assert not finished.wait(.05), 'shutdown must wait for in-flight native calls'
assert engine._start_audio_worker(lambda: None) is None
release.set()
closer.join(3)
assert finished.is_set()
assert not engine._audio_workers
assert not pygame.mixer.get_init()
engine.shutdown()
engine.play_sound(SoundType.LEVEL_UP)
assert not engine._audio_workers
''')


def test_repeated_shutdown_during_sfx_wav_and_crossfade():
    run_audio('''
import time, threading
import pygame
from audio.sound import SoundEngine, SoundType, MusicContext, sound_engine
sound_engine.shutdown()
for iteration in range(20):
    engine = SoundEngine()
    assert pygame.mixer.get_init()
    engine._crossfade_to_context(MusicContext.CALM)
    engine._play_fallback_ambient(MusicContext.CALM)
    def produce():
        for _ in range(12):
            engine.play_sound(SoundType.LEVEL_UP)
            if engine._available_wavs:
                engine.play_wav(next(iter(engine._available_wavs)))
            time.sleep(.002)
    producer = threading.Thread(target=produce)
    producer.start()
    time.sleep((iteration % 5) * .005)
    engine.shutdown()
    producer.join()
    engine.shutdown()
    assert not engine._audio_workers
    assert not pygame.mixer.get_init()
''')
