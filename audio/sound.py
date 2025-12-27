"""
Sound system - chiptune music and sound effects using terminal beeps.

Uses multiple approaches:
1. Terminal bell (\a) for simple beeps
2. /dev/console for frequency control (if available)
3. paplay/aplay for more complex sounds (if available)
4. Fallback to silent operation
"""
import os
import sys
import time
import threading
import subprocess
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import random


class SoundType(Enum):
    """Types of sounds."""
    QUACK = "quack"
    QUACK_HAPPY = "quack_happy"
    QUACK_SAD = "quack_sad"
    QUACK_EXCITED = "quack_excited"
    EAT = "eat"
    SPLASH = "splash"
    SLEEP = "sleep"
    WAKE = "wake"
    PET = "pet"
    PLAY = "play"
    LEVEL_UP = "level_up"
    ALERT = "alert"
    MUSIC_NOTE = "music_note"
    STEP = "step"


@dataclass
class Note:
    """A musical note."""
    frequency: int  # Hz
    duration: float  # seconds


# Musical note frequencies (Hz)
NOTES = {
    'C3': 131, 'D3': 147, 'E3': 165, 'F3': 175, 'G3': 196, 'A3': 220, 'B3': 247,
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349, 'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698, 'G5': 784, 'A5': 880, 'B5': 988,
    'C6': 1047,
}


# Sound effect definitions as note sequences
SOUND_EFFECTS = {
    SoundType.QUACK: [
        Note(400, 0.08), Note(350, 0.12),
    ],
    SoundType.QUACK_HAPPY: [
        Note(500, 0.06), Note(600, 0.06), Note(500, 0.1),
    ],
    SoundType.QUACK_SAD: [
        Note(300, 0.15), Note(250, 0.2),
    ],
    SoundType.QUACK_EXCITED: [
        Note(600, 0.05), Note(700, 0.05), Note(800, 0.05), Note(700, 0.05), Note(600, 0.08),
    ],
    SoundType.EAT: [
        Note(300, 0.03), Note(350, 0.03), Note(300, 0.03), Note(400, 0.05),
    ],
    SoundType.SPLASH: [
        Note(200, 0.02), Note(300, 0.02), Note(250, 0.02), Note(350, 0.02),
        Note(200, 0.02), Note(400, 0.03),
    ],
    SoundType.SLEEP: [
        Note(200, 0.3), Note(150, 0.4),
    ],
    SoundType.WAKE: [
        Note(300, 0.1), Note(400, 0.1), Note(500, 0.15),
    ],
    SoundType.PET: [
        Note(400, 0.1), Note(500, 0.1), Note(600, 0.15),
    ],
    SoundType.PLAY: [
        Note(500, 0.05), Note(600, 0.05), Note(700, 0.05), Note(600, 0.05),
        Note(700, 0.05), Note(800, 0.1),
    ],
    SoundType.LEVEL_UP: [
        Note(400, 0.1), Note(500, 0.1), Note(600, 0.1), Note(700, 0.1),
        Note(800, 0.1), Note(900, 0.1), Note(1000, 0.2),
    ],
    SoundType.ALERT: [
        Note(800, 0.1), Note(600, 0.1), Note(800, 0.1),
    ],
    SoundType.MUSIC_NOTE: [
        Note(440, 0.1),
    ],
    SoundType.STEP: [
        Note(150, 0.03),
    ],
}


# Chiptune melodies for background music
MELODIES = {
    "happy": [
        ('C4', 0.2), ('E4', 0.2), ('G4', 0.2), ('C5', 0.4),
        ('G4', 0.2), ('E4', 0.2), ('C4', 0.4),
    ],
    "idle": [
        ('C4', 0.3), ('D4', 0.3), ('E4', 0.3), ('D4', 0.3),
    ],
    "sad": [
        ('A3', 0.4), ('G3', 0.4), ('F3', 0.4), ('E3', 0.6),
    ],
    "playful": [
        ('C4', 0.1), ('D4', 0.1), ('E4', 0.1), ('G4', 0.1),
        ('E4', 0.1), ('D4', 0.1), ('C4', 0.2),
        ('G4', 0.1), ('A4', 0.1), ('G4', 0.1), ('E4', 0.2),
    ],
    "sleepy": [
        ('C4', 0.5), ('B3', 0.5), ('A3', 0.5), ('G3', 0.8),
    ],
    "alert": [
        ('E5', 0.1), ('E5', 0.1), ('E5', 0.1),
    ],
}


class SoundEngine:
    """
    Handles sound playback using various system methods.
    """

    def __init__(self):
        self.enabled = False  # Disabled by default
        self.volume = 0.5  # 0.0 to 1.0
        self._sound_method = self._detect_sound_method()
        self._music_thread: Optional[threading.Thread] = None
        self._music_playing = False
        self._current_melody = None

    def _detect_sound_method(self) -> str:
        """Detect the best available sound method."""
        # Check for paplay (PulseAudio)
        try:
            result = subprocess.run(
                ['which', 'paplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'paplay'
        except:
            pass

        # Check for speaker-test
        try:
            result = subprocess.run(
                ['which', 'speaker-test'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'speaker-test'
        except:
            pass

        # Check for beep command
        try:
            result = subprocess.run(
                ['which', 'beep'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'beep'
        except:
            pass

        # Fallback to terminal bell
        return 'bell'

    def play_tone(self, frequency: int, duration: float):
        """Play a single tone."""
        if not self.enabled:
            return

        if self._sound_method == 'beep':
            self._play_beep(frequency, duration)
        elif self._sound_method == 'speaker-test':
            self._play_speaker_test(frequency, duration)
        else:
            self._play_bell()

    def _play_beep(self, frequency: int, duration: float):
        """Play using the beep command."""
        try:
            duration_ms = int(duration * 1000)
            subprocess.run(
                ['beep', '-f', str(frequency), '-l', str(duration_ms)],
                capture_output=True,
                timeout=duration + 0.5
            )
        except:
            self._play_bell()

    def _play_speaker_test(self, frequency: int, duration: float):
        """Play using speaker-test."""
        try:
            subprocess.run(
                ['speaker-test', '-t', 'sine', '-f', str(frequency),
                 '-l', '1', '-p', str(int(duration * 1000))],
                capture_output=True,
                timeout=duration + 0.5,
                stderr=subprocess.DEVNULL
            )
        except:
            self._play_bell()

    def _play_bell(self):
        """Play terminal bell."""
        sys.stdout.write('\a')
        sys.stdout.flush()

    def play_sound(self, sound_type: SoundType):
        """Play a sound effect."""
        if not self.enabled:
            return

        notes = SOUND_EFFECTS.get(sound_type, [])
        if not notes:
            return

        # Play in a thread to not block
        thread = threading.Thread(target=self._play_notes, args=(notes,))
        thread.daemon = True
        thread.start()

    def _play_notes(self, notes: List[Note]):
        """Play a sequence of notes."""
        for note in notes:
            self.play_tone(note.frequency, note.duration)
            time.sleep(note.duration * 0.8)  # Slight overlap

    def play_melody(self, melody_name: str, loop: bool = False):
        """Play a melody."""
        if not self.enabled:
            return

        melody = MELODIES.get(melody_name)
        if not melody:
            return

        self._current_melody = melody_name
        self._music_playing = True

        def play_loop():
            while self._music_playing:
                for note_name, duration in melody:
                    if not self._music_playing:
                        break
                    freq = NOTES.get(note_name, 440)
                    self.play_tone(freq, duration)
                    time.sleep(duration)
                if not loop:
                    break
            self._music_playing = False

        self._music_thread = threading.Thread(target=play_loop)
        self._music_thread.daemon = True
        self._music_thread.start()

    def stop_music(self):
        """Stop currently playing music."""
        self._music_playing = False
        if self._music_thread:
            self._music_thread.join(timeout=0.5)

    def set_enabled(self, enabled: bool):
        """Enable or disable sound."""
        self.enabled = enabled
        if not enabled:
            self.stop_music()

    def toggle(self) -> bool:
        """Toggle sound on/off. Returns new state."""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
        return self.enabled


class DuckSounds:
    """
    Duck-specific sound effects.
    """

    def __init__(self, engine: SoundEngine):
        self.engine = engine

    def quack(self, mood: str = "normal"):
        """Play a quack sound based on mood."""
        if mood in ["ecstatic", "happy"]:
            self.engine.play_sound(SoundType.QUACK_HAPPY)
        elif mood in ["sad", "miserable"]:
            self.engine.play_sound(SoundType.QUACK_SAD)
        elif mood == "excited":
            self.engine.play_sound(SoundType.QUACK_EXCITED)
        else:
            self.engine.play_sound(SoundType.QUACK)

    def eat(self):
        """Play eating sound."""
        self.engine.play_sound(SoundType.EAT)

    def splash(self):
        """Play splash sound."""
        self.engine.play_sound(SoundType.SPLASH)

    def sleep(self):
        """Play sleep sound."""
        self.engine.play_sound(SoundType.SLEEP)

    def wake(self):
        """Play wake up sound."""
        self.engine.play_sound(SoundType.WAKE)

    def pet(self):
        """Play petting sound."""
        self.engine.play_sound(SoundType.PET)

    def play(self):
        """Play playing sound."""
        self.engine.play_sound(SoundType.PLAY)

    def level_up(self):
        """Play level up/growth sound."""
        self.engine.play_sound(SoundType.LEVEL_UP)

    def alert(self):
        """Play alert sound."""
        self.engine.play_sound(SoundType.ALERT)

    def step(self):
        """Play footstep sound."""
        self.engine.play_sound(SoundType.STEP)

    def random_quack(self):
        """Play a random quack variation."""
        variations = [
            SoundType.QUACK,
            SoundType.QUACK_HAPPY,
            SoundType.QUACK_EXCITED,
        ]
        self.engine.play_sound(random.choice(variations))


# Global instances
sound_engine = SoundEngine()
duck_sounds = DuckSounds(sound_engine)
