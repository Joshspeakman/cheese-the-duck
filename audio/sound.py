"""
Sound system - chiptune music and sound effects using terminal beeps.
Now also supports WAV file playback for realistic duck sounds!

Uses multiple approaches:
1. WAV files via pygame/aplay/paplay (preferred)
2. Terminal bell (\a) for simple beeps
3. /dev/console for frequency control (if available)
4. Fallback to silent operation
"""
import os
import sys
import time
import threading
import logging
import subprocess
import concurrent.futures
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import random

# Configure logging for sound system
logger = logging.getLogger(__name__)


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
    # New exploration/crafting/building sounds
    CRAFT_COMPLETE = "craft_complete"
    BUILD_COMPLETE = "build_complete"
    DISCOVERY = "discovery"
    EXPLORE = "explore"
    GATHER = "gather"


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
    # New exploration/crafting/building sounds
    SoundType.CRAFT_COMPLETE: [
        Note(523, 0.08), Note(659, 0.08), Note(784, 0.08), Note(1047, 0.15),
    ],
    SoundType.BUILD_COMPLETE: [
        Note(392, 0.1), Note(494, 0.1), Note(587, 0.1), Note(784, 0.1),
        Note(587, 0.08), Note(784, 0.2),
    ],
    SoundType.DISCOVERY: [
        Note(784, 0.1), Note(880, 0.1), Note(988, 0.1), Note(1047, 0.15),
        Note(988, 0.08), Note(1047, 0.25),
    ],
    SoundType.EXPLORE: [
        Note(330, 0.08), Note(392, 0.08), Note(440, 0.1),
    ],
    SoundType.GATHER: [
        Note(262, 0.05), Note(294, 0.05), Note(330, 0.08),
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


# ============== DYNAMIC MUSIC SYSTEM ==============

class MusicContext(Enum):
    """Context types for dynamic music selection."""
    DEFAULT = "default"
    HAPPY = "happy"
    SAD = "sad"
    CALM = "calm"
    ENERGETIC = "energetic"
    STORMY = "stormy"
    MYSTERIOUS = "mysterious"
    CELEBRATION = "celebration"


@dataclass
class MusicTrack:
    """A music track configuration."""
    context: MusicContext
    audio_file: Optional[str]  # WAV/MP3 file name (without path)
    melody_name: Optional[str]  # Chiptune melody key as fallback
    priority: int  # Higher = more important, overrides lower priority


# Music track mappings - audio file takes precedence, melody is fallback
# Prefer WAV files for wider player compatibility (aplay, paplay)
MUSIC_TRACKS = {
    MusicContext.DEFAULT: MusicTrack(MusicContext.DEFAULT, "Main.wav", "idle", 0),
    MusicContext.CALM: MusicTrack(MusicContext.CALM, "Bell Breeze Loop.wav", "idle", 1),
    MusicContext.HAPPY: MusicTrack(MusicContext.HAPPY, "sunny_day1.wav", "happy", 3),
    MusicContext.ENERGETIC: MusicTrack(MusicContext.ENERGETIC, "sunny_day2.wav", "playful", 3),
    MusicContext.SAD: MusicTrack(MusicContext.SAD, None, "sad", 3),
    MusicContext.MYSTERIOUS: MusicTrack(MusicContext.MYSTERIOUS, None, "sleepy", 2),
    MusicContext.STORMY: MusicTrack(MusicContext.STORMY, None, "alert", 4),
    MusicContext.CELEBRATION: MusicTrack(MusicContext.CELEBRATION, "Title.wav", None, 5),
}


def get_music_context(
    weather: str = "sunny",
    time_of_day: str = "day",
    duck_mood: str = "content",
    event: Optional[str] = None
) -> MusicContext:
    """
    Determine the appropriate music context based on game state.

    Priority (highest to lowest):
    1. Events (level_up, friend_arrival)
    2. Weather extremes (stormy, rainbow)
    3. Duck mood (ecstatic/happy, miserable/sad)
    4. Normal weather (rainy, snowy, sunny)
    5. Time of day (night, morning)
    6. Default (calm/neutral)

    Args:
        weather: Current weather type
        time_of_day: Current time of day
        duck_mood: Duck's current mood state
        event: Active event type (if any)

    Returns:
        MusicContext appropriate for the current game state
    """
    weather = weather.lower() if weather else "sunny"
    time_of_day = time_of_day.lower() if time_of_day else "day"
    duck_mood = duck_mood.lower() if duck_mood else "content"

    # Priority 1: Events (highest priority)
    if event:
        event = event.lower()
        if event in ["level_up", "achievement"]:
            return MusicContext.CELEBRATION
        if event in ["friend_arrival", "visitor_arrival"]:
            return MusicContext.HAPPY

    # Priority 2: Extreme weather
    if weather == "stormy":
        return MusicContext.STORMY
    if weather == "rainbow":
        return MusicContext.CELEBRATION

    # Priority 3: Duck mood (strong emotions)
    if duck_mood in ["ecstatic", "happy"]:
        return MusicContext.HAPPY
    if duck_mood in ["miserable", "sad"]:
        return MusicContext.SAD

    # Priority 4: Normal weather influences
    if weather in ["snowy", "foggy"]:
        return MusicContext.CALM
    if weather == "rainy":
        return MusicContext.MYSTERIOUS
    if weather in ["sunny", "windy"]:
        return MusicContext.ENERGETIC

    # Priority 5: Time of day
    if time_of_day in ["night", "late_night", "midnight"]:
        return MusicContext.MYSTERIOUS
    if time_of_day in ["morning", "dawn"]:
        return MusicContext.ENERGETIC

    # Priority 6: Default
    return MusicContext.CALM


class SoundEngine:
    """
    Handles sound playback using various system methods.
    Now includes WAV file playback support!
    Uses pygame for MP3 music when available.
    Thread-safe implementation with proper locking.
    """
    
    # Thread pool for sound effect playback (max 4 concurrent sounds)
    _sound_executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

    def __init__(self):
        # Thread lock for shared state access
        self._lock = threading.Lock()
        
        self.enabled = True  # Enabled by default
        self.volume = 1.0  # 0.0 to 1.0 (quack volume - max, pygame caps at 1.0)
        self.music_volume = 0.4  # Background music volume (40% - increased for better audibility)
        self.music_muted = False  # Separate mute for music
        self._sound_method = self._detect_sound_method()
        self._music_thread: Optional[threading.Thread] = None
        self._music_playing = False
        self._music_process: Optional[subprocess.Popen] = None
        self._current_melody = None
        self._music_channel = None  # For seamless looping with Sound object
        self._music_sound = None  # Cached music Sound object
        
        # Initialize thread pool for sound effects
        if SoundEngine._sound_executor is None:
            SoundEngine._sound_executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=4, 
                thread_name_prefix="SoundEffect"
            )

        # Try to initialize pygame for music
        self._pygame_available = False
        try:
            import pygame
            # Smaller buffer for tighter looping
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            self._pygame_available = True
        except Exception:
            pass
        
        # Audio file paths
        self._audio_dir = Path(__file__).parent.parent
        self._wav_files = {
            'quack': self._audio_dir / 'single-quack-from-a-duck.wav',
            'title': self._audio_dir / 'Title.wav',
            'sunny_day': self._audio_dir / 'sunny_day.wav',
            'levelup': self._audio_dir / 'levelup.wav',
        }
        self._music_process = None  # Track music subprocess for stopping
        self._music_files = {
            'main': self._audio_dir / 'Main.mp3',
            'Main.mp3': self._audio_dir / 'Main.mp3',
            'Main.wav': self._audio_dir / 'Main.wav',
            'Title.wav': self._audio_dir / 'Title.wav',
            'Bell Breeze Loop.wav': self._audio_dir / 'Bell Breeze Loop.wav',
            'sunny_day1.wav': self._audio_dir / 'sunny_day1.wav',
            'sunny_day2.wav': self._audio_dir / 'sunny_day2.wav',
        }

        # Dynamic music system state
        self._current_context: Optional[MusicContext] = None
        self._crossfade_thread: Optional[threading.Thread] = None
        self._crossfading = False
        self._event_music_end_time: float = 0  # When event music should end
        self._previous_context: Optional[MusicContext] = None  # For resuming after events
        self._music_cooldown_until: float = 0  # Cooldown period before next play

        # Check which audio files exist
        self._available_wavs = {
            name: path for name, path in self._wav_files.items() 
            if path.exists()
        }
        self._available_music = {
            name: path for name, path in self._music_files.items()
            if path.exists()
        }
        
        # Detect players
        self._wav_player = self._detect_wav_player()
        self._music_player = self._detect_music_player()

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
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
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
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
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
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        # Fallback to terminal bell
        return 'bell'

    def _detect_wav_player(self) -> Optional[str]:
        """Detect available WAV file player."""
        # Check for paplay (PulseAudio) - best for most Linux
        try:
            result = subprocess.run(
                ['which', 'paplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'paplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Check for aplay (ALSA)
        try:
            result = subprocess.run(
                ['which', 'aplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'aplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Check for ffplay (ffmpeg)
        try:
            result = subprocess.run(
                ['which', 'ffplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'ffplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        return None

    def _detect_music_player(self) -> Optional[str]:
        """Detect available music player for MP3/WAV files."""
        # Check for mpv (best for seamless looping)
        try:
            result = subprocess.run(
                ['which', 'mpv'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'mpv'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        # Check for ffplay (ffmpeg) - good fallback
        try:
            result = subprocess.run(
                ['which', 'ffplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'ffplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        # Check for mpg123 (lightweight mp3 player)
        try:
            result = subprocess.run(
                ['which', 'mpg123'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'mpg123'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        # Check for aplay (ALSA - WAV files only, but works as fallback)
        try:
            result = subprocess.run(
                ['which', 'aplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'aplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        # Check for paplay (PulseAudio)
        try:
            result = subprocess.run(
                ['which', 'paplay'],
                capture_output=True,
                timeout=1
            )
            if result.returncode == 0:
                return 'paplay'
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass

        return None

    def play_background_music(self, music_name: str = 'main'):
        """Play background music on loop at low volume."""
        if not self.enabled or self.music_muted:
            return

        if music_name not in self._available_music:
            return

        # Stop any existing music first
        self.stop_background_music()

        music_path = self._available_music[music_name]
        self._music_playing = True

        # Prefer pygame for MP3 playback - with cooldown between loops
        if self._pygame_available:
            try:
                import pygame

                def pygame_loop():
                    try:
                        sound = pygame.mixer.Sound(str(music_path))
                        sound.set_volume(self.music_volume)
                        self._music_sound = sound
                    except Exception:
                        # Fallback to streaming for large files
                        sound = None

                    while self._music_playing and not self.music_muted:
                        try:
                            if sound:
                                # Play once (loops=0)
                                self._music_channel = sound.play(loops=0)
                                # Wait for it to finish
                                while self._music_channel and self._music_channel.get_busy():
                                    if not self._music_playing or self.music_muted:
                                        sound.stop()
                                        return
                                    time.sleep(0.1)
                            else:
                                # Use streaming music
                                pygame.mixer.music.load(str(music_path))
                                pygame.mixer.music.set_volume(self.music_volume)
                                pygame.mixer.music.play(0)
                                while pygame.mixer.music.get_busy():
                                    if not self._music_playing or self.music_muted:
                                        pygame.mixer.music.stop()
                                        return
                                    time.sleep(0.1)

                            # Cooldown: wait 2-5 minutes before playing again
                            cooldown = random.uniform(120, 300)
                            for _ in range(int(cooldown * 10)):
                                if not self._music_playing or self.music_muted:
                                    return
                                time.sleep(0.1)
                        except Exception:
                            break

                    self._music_playing = False

                self._music_thread = threading.Thread(target=pygame_loop)
                self._music_thread.daemon = True
                self._music_thread.start()
                return
            except Exception:
                pass
        
        # Fallback to system players if pygame fails
        if not self._music_player:
            return
        
        def play_loop():
            while self._music_playing and not self.music_muted:
                try:
                    if self._music_player == 'mpv':
                        # mpv with loop and low volume
                        vol_percent = int(self.music_volume * 100)
                        self._music_process = subprocess.Popen(
                            ['mpv', '--no-video', '--loop=inf', 
                             f'--volume={vol_percent}', '--really-quiet',
                             str(music_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._music_player == 'ffplay':
                        # ffplay with loop
                        vol_percent = int(self.music_volume * 100)
                        self._music_process = subprocess.Popen(
                            ['ffplay', '-nodisp', '-loop', '0',
                             '-volume', str(vol_percent), '-loglevel', 'quiet',
                             str(music_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._music_player == 'mpg123':
                        # mpg123 with loop (we'll loop in Python)
                        self._music_process = subprocess.Popen(
                            ['mpg123', '-q', '--scale', str(int(self.music_volume * 32768)),
                             str(music_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                        # Continue loop
                        continue
                    elif self._music_player == 'aplay':
                        # aplay for WAV files (loop in Python with cooldown)
                        self._music_process = subprocess.Popen(
                            ['aplay', '-q', str(music_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                        # Wait 2-5 minutes before looping again
                        cooldown = random.uniform(120, 300)
                        for _ in range(int(cooldown * 10)):
                            if not self._music_playing or self.music_muted:
                                break
                            time.sleep(0.1)
                        continue
                    elif self._music_player == 'paplay':
                        # paplay for WAV files with volume control
                        pa_volume = int(self.music_volume * 65536)
                        self._music_process = subprocess.Popen(
                            ['paplay', '--volume', str(pa_volume), str(music_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                        # Wait 2-5 minutes before looping again
                        cooldown = random.uniform(120, 300)
                        for _ in range(int(cooldown * 10)):
                            if not self._music_playing or self.music_muted:
                                break
                            time.sleep(0.1)
                        continue
                except Exception:
                    pass
                
                # If we get here without looping player, wait and try again
                if self._music_playing and not self.music_muted:
                    time.sleep(0.1)
                else:
                    break
            
            self._music_playing = False
        
        self._music_thread = threading.Thread(target=play_loop)
        self._music_thread.daemon = True
        self._music_thread.start()

    def stop_background_music(self):
        """Stop background music."""
        self._music_playing = False

        # Stop pygame Sound object if active
        if self._music_sound:
            try:
                self._music_sound.stop()
            except Exception:
                pass
            self._music_sound = None
            self._music_channel = None

        # Stop pygame streaming music if active
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.stop()
            except Exception:
                pass

        # Stop subprocess-based music
        if self._music_process:
            try:
                self._music_process.terminate()
                self._music_process.wait(timeout=1)
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                try:
                    self._music_process.kill()
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    pass
            self._music_process = None
        if self._music_thread:
            self._music_thread.join(timeout=0.5)
            self._music_thread = None

    def toggle_music_mute(self) -> bool:
        """Toggle music mute on/off. Returns new muted state."""
        self.music_muted = not self.music_muted
        if self.music_muted:
            # Mute - pause Sound or streaming music
            if self._music_channel:
                try:
                    self._music_channel.pause()
                except Exception:
                    pass
            elif self._pygame_available:
                try:
                    import pygame
                    pygame.mixer.music.pause()
                except Exception:
                    pass
            else:
                self.stop_background_music()
        else:
            # Unmute - resume Sound or streaming music
            if self._music_channel:
                try:
                    self._music_channel.unpause()
                except Exception:
                    self.play_background_music()
            elif self._pygame_available:
                try:
                    import pygame
                    pygame.mixer.music.unpause()
                except Exception:
                    self.play_background_music()
            else:
                self.play_background_music()
        return self.music_muted

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0). Recommended to keep low (0.1-0.2)."""
        self.music_volume = max(0.0, min(1.0, volume))
        # Update Sound object volume if playing
        if self._music_sound:
            try:
                self._music_sound.set_volume(self.music_volume)
            except Exception:
                pass
        # Update pygame streaming music volume if playing
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.set_volume(self.music_volume)
            except Exception:
                pass

    # ============== DYNAMIC MUSIC METHODS ==============

    def update_music(self, context: MusicContext, force: bool = False):
        """
        Update background music based on the current context.

        Automatically handles track switching with crossfade when the context changes.
        Does nothing if the context hasn't changed (unless force=True).
        Respects cooldown period between plays.

        Args:
            context: The new MusicContext to switch to
            force: If True, bypass cooldown and start music immediately
        """
        if not self.enabled or self.music_muted:
            return

        # Don't interrupt ongoing crossfade (unless forcing)
        if self._crossfading and not force:
            return

        current_time = time.time()

        # Force mode: clear cooldown and stop any playing music
        if force:
            self._music_cooldown_until = 0
            self._event_music_end_time = 0
            if self._music_sound:
                try:
                    self._music_sound.stop()
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    pass
            self._music_channel = None
            self._current_context = None
        else:
            # Check if we should ignore this update (event music playing)
            if current_time < self._event_music_end_time:
                return  # Event music still playing

            # Check if we're in cooldown (don't restart music)
            if current_time < self._music_cooldown_until:
                return  # Still in cooldown

            # Check if music is still playing
            if self._music_channel and self._music_channel.get_busy():
                return  # Music still playing, wait for it to finish

        # Start crossfade to new track (or restart same track after cooldown)
        self._crossfade_to_context(context)

    def play_event_music(self, context: MusicContext, duration: float = 5.0):
        """
        Play temporary event music that overrides normal music.

        After the duration, the previous music context will resume.

        Args:
            context: The music context to play
            duration: How long to play this music before resuming normal music
        """
        if not self.enabled or self.music_muted:
            return

        # Save current context to resume later
        if self._current_context and self._current_context != context:
            self._previous_context = self._current_context

        # Set event end time
        self._event_music_end_time = time.time() + duration

        # Switch to event music
        self._crossfade_to_context(context)

    def _crossfade_to_context(self, new_context: MusicContext):
        """
        Crossfade from current music to new context.

        Uses a 2-second crossfade for smooth transitions.
        """
        if self._crossfading:
            return  # Already crossfading

        track = MUSIC_TRACKS.get(new_context)
        if not track:
            return

        # Find the audio file to play
        audio_file = None
        if track.audio_file and track.audio_file in self._available_music:
            audio_file = track.audio_file
        elif track.audio_file:
            # Check if file exists by path
            audio_path = self._audio_dir / track.audio_file
            if audio_path.exists():
                self._available_music[track.audio_file] = audio_path
                audio_file = track.audio_file

        # If no audio file, skip this context (don't use beeping fallback)
        if not audio_file:
            # Just silently skip - no beeping fallback as it's annoying
            return

        # Perform crossfade with pygame
        if self._pygame_available:
            self._crossfading = True

            def do_crossfade():
                try:
                    import pygame
                    fade_duration = 2.0  # 2 second crossfade
                    steps = 20
                    step_duration = fade_duration / steps

                    # Fade out current music
                    if self._music_sound and self._music_channel:
                        start_volume = self._music_sound.get_volume()
                        for i in range(steps):
                            vol = start_volume * (1 - (i + 1) / steps)
                            try:
                                self._music_sound.set_volume(vol)
                            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                                break
                            time.sleep(step_duration)
                        try:
                            self._music_sound.stop()
                        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                            pass

                    # Load and start new music at low volume, fade in
                    # Play ONCE (loops=0), not infinite
                    music_path = self._available_music.get(audio_file)
                    if music_path and music_path.exists():
                        try:
                            new_sound = pygame.mixer.Sound(str(music_path))
                            new_sound.set_volume(0)
                            new_channel = new_sound.play(loops=0)  # Play once only

                            # Fade in
                            for i in range(steps):
                                vol = self.music_volume * ((i + 1) / steps)
                                try:
                                    new_sound.set_volume(vol)
                                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                                    break
                                time.sleep(step_duration)

                            # Update state
                            self._music_sound = new_sound
                            self._music_channel = new_channel
                            self._music_sound.set_volume(self.music_volume)

                            # Wait for track to finish, then set cooldown
                            while new_channel and new_channel.get_busy():
                                if self.music_muted:
                                    new_sound.stop()
                                    break
                                time.sleep(0.5)

                            # Set cooldown: 2-5 minutes before playing again
                            self._music_cooldown_until = time.time() + random.uniform(120, 300)

                        except Exception:
                            pass

                    self._current_context = new_context
                except Exception:
                    pass
                finally:
                    self._crossfading = False

            self._crossfade_thread = threading.Thread(target=do_crossfade)
            self._crossfade_thread.daemon = True
            self._crossfade_thread.start()
        else:
            # No pygame, just switch directly
            self.stop_background_music()
            self._current_context = new_context
            if audio_file in self._available_music:
                # Use existing play_background_music logic
                old_music_files = self._music_files.copy()
                self._music_files['dynamic'] = self._available_music[audio_file]
                self._available_music['dynamic'] = self._available_music[audio_file]
                self.play_background_music('dynamic')
                self._music_files = old_music_files

    def get_current_context(self) -> Optional[MusicContext]:
        """Get the current music context."""
        return self._current_context

    def play_wav(self, wav_name: str, volume: Optional[float] = None):
        """Play a WAV file if available."""
        if not self.enabled:
            return
        
        if wav_name not in self._available_wavs:
            return
        
        wav_path = self._available_wavs[wav_name]
        vol = volume if volume is not None else self.volume
        
        # Prefer pygame for proper volume control
        if self._pygame_available:
            def play_pygame():
                try:
                    import pygame
                    sound = pygame.mixer.Sound(str(wav_path))
                    sound.set_volume(vol)
                    sound.play()
                except Exception:
                    pass
            thread = threading.Thread(target=play_pygame)
            thread.daemon = True
            thread.start()
            return
        
        # Fallback to system player
        if not self._wav_player:
            return
        
        def play():
            try:
                if self._wav_player == 'paplay':
                    # PulseAudio volume is 0-65536
                    pa_volume = int(vol * 65536)
                    subprocess.run(
                        ['paplay', '--volume', str(pa_volume), str(wav_path)],
                        capture_output=True,
                        timeout=10
                    )
                elif self._wav_player == 'aplay':
                    subprocess.run(
                        ['aplay', '-q', str(wav_path)],
                        capture_output=True,
                        timeout=10
                    )
                elif self._wav_player == 'ffplay':
                    volume_arg = f"volume={vol}"
                    subprocess.run(
                        ['ffplay', '-nodisp', '-autoexit', '-volume', str(int(vol * 100)), 
                         str(wav_path)],
                        capture_output=True,
                        stderr=subprocess.DEVNULL,
                        timeout=10
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                pass  # Silently fail if playback issues
        
        # Play in background thread
        thread = threading.Thread(target=play)
        thread.daemon = True
        thread.start()

    def play_wav_music(self, wav_name: str, loop: bool = False):
        """Play a WAV file as background music, optionally looping."""
        if not self.enabled:
            return
        
        if wav_name not in self._available_wavs:
            return
        
        if not self._wav_player:
            return
        
        self.stop_music()
        self._music_playing = True
        wav_path = self._available_wavs[wav_name]
        # Use music_volume for background music (lower volume)
        music_vol = self.music_volume
        
        def play_loop():
            while self._music_playing:
                try:
                    if self._wav_player == 'paplay':
                        # PulseAudio volume: 65536 = 100%, scale by music_volume
                        pa_volume = int(music_vol * 65536)
                        self._music_process = subprocess.Popen(
                            ['paplay', '--volume', str(pa_volume), str(wav_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._wav_player == 'aplay':
                        self._music_process = subprocess.Popen(
                            ['aplay', '-q', str(wav_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._wav_player == 'ffplay':
                        self._music_process = subprocess.Popen(
                            ['ffplay', '-nodisp', '-autoexit', '-volume', 
                             str(int(music_vol * 100)), str(wav_path)],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    pass
                
                if not loop or not self._music_playing:
                    break
            
            self._music_playing = False
            self._music_process = None
        
        self._music_thread = threading.Thread(target=play_loop)
        self._music_thread.daemon = True
        self._music_thread.start()

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
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
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
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            self._play_bell()

    def _play_bell(self):
        """Play terminal bell."""
        sys.stdout.write('\a')
        sys.stdout.flush()

    def play_sound(self, sound_type):
        """Play a sound effect. Accepts SoundType enum or string."""
        if not self.enabled:
            return
        
        # Handle string input by converting to SoundType
        if isinstance(sound_type, str):
            try:
                sound_type = SoundType(sound_type)
            except ValueError:
                # Try uppercase
                try:
                    sound_type = SoundType[sound_type.upper()]
                except KeyError:
                    return  # Unknown sound type, silently ignore

        notes = SOUND_EFFECTS.get(sound_type, [])
        if not notes:
            return

        # Play in a thread to not block
        thread = threading.Thread(target=self._play_notes, args=(notes,))
        thread.daemon = True
        thread.start()

    def _play_notes(self, notes: List[Note]):
        """Play a sequence of notes."""
        # Disabled - terminal beeps are annoying
        # Use WAV files for sound effects instead
        pass

    def play_melody(self, melody_name: str, loop: bool = False):
        """Play a melody. Disabled to avoid terminal beeping."""
        # Disabled - terminal beeps are annoying and disruptive
        # The game now relies on WAV/MP3 files for music
        pass

    def stop_music(self):
        """Stop currently playing music."""
        self._music_playing = False
        # Terminate the subprocess if running
        if self._music_process:
            try:
                self._music_process.terminate()
                self._music_process.wait(timeout=0.5)
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                try:
                    self._music_process.kill()
                except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                    pass
            self._music_process = None
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

    def set_volume(self, volume: float):
        """Set volume level (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))

    def get_volume(self) -> float:
        """Get current volume level."""
        return self.volume

    def volume_up(self, step: float = 0.1) -> float:
        """Increase volume by step. Returns new volume."""
        self.volume = min(1.0, self.volume + step)
        return self.volume

    def volume_down(self, step: float = 0.1) -> float:
        """Decrease volume by step. Returns new volume."""
        self.volume = max(0.0, self.volume - step)
        return self.volume

    def get_volume_display(self) -> str:
        """Get a visual representation of current volume."""
        bars = int(self.volume * 10)
        return "█" * bars + "." * (10 - bars)


def count_syllables(text: str) -> int:
    """
    Count approximate syllables in text for quacking purposes.
    Uses a simple heuristic based on vowel groups.
    """
    import re
    
    # Clean text - remove non-alphabetic characters
    text = text.lower()
    words = re.findall(r'[a-z]+', text)
    
    total_syllables = 0
    for word in words:
        # Count vowel groups
        vowels = 'aeiouy'
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e' at end
        if word.endswith('e') and count > 1:
            count -= 1
        
        # Every word has at least 1 syllable
        count = max(1, count)
        total_syllables += count
    
    return max(1, total_syllables)  # At least 1 syllable


class DuckSounds:
    """
    Duck-specific sound effects.
    """

    def __init__(self, engine: SoundEngine):
        self.engine = engine
        self._quack_thread = None

    def quack(self, mood: str = "normal"):
        """Play a quack sound based on mood."""
        # Try to play the real duck WAV file first
        if 'quack' in self.engine._available_wavs:
            self.engine.play_wav('quack')
        else:
            # Fallback to synthesized quacks
            if mood in ["ecstatic", "happy"]:
                self.engine.play_sound(SoundType.QUACK_HAPPY)
            elif mood in ["sad", "miserable"]:
                self.engine.play_sound(SoundType.QUACK_SAD)
            elif mood == "excited":
                self.engine.play_sound(SoundType.QUACK_EXCITED)
            else:
                self.engine.play_sound(SoundType.QUACK)

    def quack_for_text(self, text: str, mood: str = "normal"):
        """
        Play quacks for each syllable in the text.
        Quacks are spaced out to simulate speech.
        """
        syllables = count_syllables(text)
        # Cap at reasonable number to avoid spam
        syllables = min(syllables, 15)
        
        def _quack_sequence():
            for i in range(syllables):
                self.quack(mood)
                if i < syllables - 1:
                    # Vary timing slightly for natural feel
                    delay = 0.15 + random.uniform(-0.03, 0.05)
                    time.sleep(delay)
        
        # Run in thread to not block game
        self._quack_thread = threading.Thread(target=_quack_sequence, daemon=True)
        self._quack_thread.start()

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
        # Try WAV file first, fall back to synthesized sound
        # Level up is mixed at 50% volume to avoid being too jarring
        if 'levelup' in self.engine._available_wavs:
            self.engine.play_wav('levelup', volume=0.5)
        else:
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
