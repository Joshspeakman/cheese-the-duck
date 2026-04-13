"""
Sound system - chiptune music and sound effects using terminal beeps.
Now also supports WAV file playback for realistic duck sounds!

Uses multiple approaches:
1. WAV files via pygame/aplay/paplay (preferred)
2. Terminal bell (\a) for simple beeps
3. /dev/console for frequency control (if available)
4. Fallback to silent operation
"""
import sys
import time
import threading
import logging
import subprocess
import shutil
import concurrent.futures
from typing import Optional, Dict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import random

from core.event_bus import event_bus, ActionPerformedEvent, ItemUsedEvent, AchievementUnlockedEvent

# Configure logging for sound system
logger = logging.getLogger(__name__)

# Cache for command availability detection (class-level, computed once)
_COMMAND_CACHE: Dict[str, Optional[str]] = {}

def _which_cached(cmd: str) -> Optional[str]:
    """Check if a command exists using shutil.which with caching."""
    if cmd not in _COMMAND_CACHE:
        _COMMAND_CACHE[cmd] = shutil.which(cmd)
    return _COMMAND_CACHE[cmd]


class SoundType(Enum):
    """Types of sounds."""
    QUACK = "quack"
    QUACK_HAPPY = "quack_happy"
    QUACK_SAD = "quack_sad"
    QUACK_EXCITED = "quack_excited"
    QUACK_GRUMPY = "quack_grumpy"
    QUACK_PETTY = "quack_petty"
    QUACK_DRAMATIC = "quack_dramatic"
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
    DISCOVER = "discover"
    COLLECT = "collect"
    TRADE = "trade"
    HOUR_CHIME = "hour_chime"
    # Stingers — short musical cues for events
    STINGER_ACHIEVEMENT = "stinger_achievement"
    STINGER_SEASON_CHANGE = "stinger_season_change"
    STINGER_FRIEND_ARRIVE = "stinger_friend_arrive"
    STINGER_MILESTONE = "stinger_milestone"


# Sound definitions (frequency, duration pairs)
SOUND_EFFECTS = {
    SoundType.QUACK: [(800, 0.1), (600, 0.15)],
    SoundType.QUACK_HAPPY: [(900, 0.1), (1100, 0.1), (900, 0.15)],
    SoundType.QUACK_SAD: [(600, 0.2), (400, 0.25)],
    SoundType.QUACK_EXCITED: [(800, 0.08), (1000, 0.08), (1200, 0.08), (1000, 0.12)],
    SoundType.QUACK_GRUMPY: [(500, 0.15), (350, 0.2)],
    SoundType.QUACK_PETTY: [(700, 0.06), (500, 0.06), (700, 0.06), (500, 0.12)],
    SoundType.QUACK_DRAMATIC: [(600, 0.12), (900, 0.12), (600, 0.12), (1100, 0.2)],
    SoundType.EAT: [(400, 0.05), (500, 0.05), (400, 0.05)],
    SoundType.SPLASH: [(300, 0.1), (500, 0.05), (200, 0.15)],
    SoundType.SLEEP: [(300, 0.3), (250, 0.4)],
    SoundType.WAKE: [(400, 0.1), (600, 0.1), (800, 0.15)],
    SoundType.PET: [(500, 0.1), (600, 0.1), (700, 0.15)],
    SoundType.PLAY: [(800, 0.08), (1000, 0.08), (1200, 0.08), (1000, 0.08)],
    SoundType.LEVEL_UP: [(523, 0.15), (659, 0.15), (784, 0.15), (1047, 0.3)],
    SoundType.ALERT: [(1000, 0.1), (800, 0.1), (1000, 0.1)],
    SoundType.MUSIC_NOTE: [(523, 0.2)],
    SoundType.STEP: [(200, 0.05), (250, 0.05)],
    SoundType.CRAFT_COMPLETE: [(600, 0.1), (800, 0.1), (1000, 0.2)],
    SoundType.BUILD_COMPLETE: [(500, 0.1), (700, 0.1), (900, 0.1), (1100, 0.2)],
    SoundType.DISCOVER: [(400, 0.1), (600, 0.1), (800, 0.1), (1000, 0.15)],
    SoundType.COLLECT: [(500, 0.08), (700, 0.08), (900, 0.12)],
    SoundType.TRADE: [(700, 0.1), (900, 0.1), (700, 0.15)],
    SoundType.HOUR_CHIME: [(523, 0.4), (392, 0.4)],
    # Stingers
    SoundType.STINGER_ACHIEVEMENT: [(523, 0.1), (659, 0.1), (784, 0.1), (1047, 0.1), (1319, 0.25)],
    SoundType.STINGER_SEASON_CHANGE: [(392, 0.2), (523, 0.2), (659, 0.2), (784, 0.3)],
    SoundType.STINGER_FRIEND_ARRIVE: [(659, 0.1), (784, 0.1), (659, 0.15)],
    SoundType.STINGER_MILESTONE: [(523, 0.1), (784, 0.1), (1047, 0.1), (784, 0.1), (1047, 0.25)],
}


class MusicContext(Enum):
    """Context that determines which background music plays."""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    RAIN = "rain"
    FESTIVAL = "festival"
    PEACEFUL = "peaceful"
    ADVENTURE = "adventure"
    # Mood/weather-based contexts (used by get_music_context)
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
    """A background music track definition."""
    context: MusicContext
    name: str
    audio_file: Optional[str] = None  # WAV/MP3 filename if available
    tempo_bpm: int = 120
    notes: list = None  # Fallback beep notes


# Music track definitions
# Available audio files: Bell Breeze Loop.wav, sunny_day1.wav, sunny_day2.wav, Main.mp3
# Keys match what _scan_audio_assets registers (lowercase stem).
MUSIC_TRACKS = {
    # Contexts returned by get_music_context()
    MusicContext.CALM: MusicTrack(
        context=MusicContext.CALM,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=85,
    ),
    MusicContext.HAPPY: MusicTrack(
        context=MusicContext.HAPPY,
        name="Sunny Day",
        audio_file="sunny_day1",
        tempo_bpm=110,
    ),
    MusicContext.ENERGETIC: MusicTrack(
        context=MusicContext.ENERGETIC,
        name="Sunny Day 2",
        audio_file="sunny_day2",
        tempo_bpm=120,
    ),
    MusicContext.SAD: MusicTrack(
        context=MusicContext.SAD,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=85,
    ),
    MusicContext.MYSTERIOUS: MusicTrack(
        context=MusicContext.MYSTERIOUS,
        name="Main Theme",
        audio_file="main",
        tempo_bpm=100,
    ),
    MusicContext.STORMY: MusicTrack(
        context=MusicContext.STORMY,
        name="Main Theme",
        audio_file="main",
        tempo_bpm=100,
    ),
    MusicContext.CELEBRATION: MusicTrack(
        context=MusicContext.CELEBRATION,
        name="Sunny Day",
        audio_file="sunny_day1",
        tempo_bpm=110,
    ),
    MusicContext.DEFAULT: MusicTrack(
        context=MusicContext.DEFAULT,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=85,
    ),
    # Legacy time-of-day / event contexts
    MusicContext.MORNING: MusicTrack(
        context=MusicContext.MORNING,
        name="Sunny Day",
        audio_file="sunny_day1",
        tempo_bpm=100,
    ),
    MusicContext.AFTERNOON: MusicTrack(
        context=MusicContext.AFTERNOON,
        name="Sunny Day 2",
        audio_file="sunny_day2",
        tempo_bpm=110,
    ),
    MusicContext.EVENING: MusicTrack(
        context=MusicContext.EVENING,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=90,
    ),
    MusicContext.NIGHT: MusicTrack(
        context=MusicContext.NIGHT,
        name="Main Theme",
        audio_file="main",
        tempo_bpm=70,
    ),
    MusicContext.RAIN: MusicTrack(
        context=MusicContext.RAIN,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=80,
    ),
    MusicContext.FESTIVAL: MusicTrack(
        context=MusicContext.FESTIVAL,
        name="Sunny Day",
        audio_file="sunny_day1",
        tempo_bpm=140,
    ),
    MusicContext.PEACEFUL: MusicTrack(
        context=MusicContext.PEACEFUL,
        name="Bell Breeze",
        audio_file="bell breeze loop",
        tempo_bpm=85,
    ),
    MusicContext.ADVENTURE: MusicTrack(
        context=MusicContext.ADVENTURE,
        name="Sunny Day 2",
        audio_file="sunny_day2",
        tempo_bpm=130,
    ),
}


class SoundEngine:
    """
    Cross-platform sound engine.
    Tries multiple methods to produce sound.
    """

    # Shared thread pool for non-blocking sound playback
    _sound_executor: Optional[concurrent.futures.ThreadPoolExecutor] = None

    def __init__(self):
        self.enabled = True
        self.volume = 0.5
        self.music_volume = 0.15  # Music is quieter than SFX
        self.music_muted = False
        self._sound_method = None
        self._music_playing = False
        self._music_thread = None
        self._music_process = None
        self._music_files: Dict[str, Path] = {}  # name -> path
        self._wav_player = None
        self._available_wavs: Dict[str, Path] = {}  # name -> path
        self._available_music: Dict[str, Path] = {}  # name -> path
        self._pygame_available = False
        # Dynamic music state
        self._current_context: Optional[MusicContext] = None
        self._previous_context: Optional[MusicContext] = None
        self._crossfading = False
        self._crossfade_thread = None
        self._music_sound = None  # pygame Sound object for current music
        self._music_channel = None  # pygame Channel for current music
        self._music_cooldown_until: float = 0  # timestamp when cooldown expires
        self._event_music_end_time: float = 0  # timestamp when event music expires
        # Audio directory — project root where audio files live
        self._audio_dir = Path(__file__).parent.parent
        # Radio player instance (lazy-loaded)
        self._radio = None
        self._radio_was_playing = None
        self._detect_capabilities()

    @classmethod
    def _get_executor(cls) -> concurrent.futures.ThreadPoolExecutor:
        """Get or create the shared thread pool executor."""
        if cls._sound_executor is None:
            cls._sound_executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=2, thread_name_prefix="sound"
            )
        return cls._sound_executor

    def _detect_capabilities(self):
        """Detect what sound methods are available."""
        # Try to initialize pygame mixer for WAV playback
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._pygame_available = True
            logger.debug("pygame mixer initialized")
        except (ImportError, Exception) as e:
            logger.debug("pygame not available: %s", e)
            self._pygame_available = False

        # Check for WAV players
        for player in ['paplay', 'aplay', 'ffplay']:
            if _which_cached(player):
                self._wav_player = player
                break

        # Check for beep command
        if _which_cached('beep'):
            self._sound_method = 'beep'
        elif _which_cached('speaker-test'):
            self._sound_method = 'speaker-test'
        else:
            self._sound_method = 'bell'

        # Scan for audio assets
        self._scan_audio_assets()

    def _scan_audio_assets(self):
        """Scan the audio directory for WAV and music files."""
        if not self._audio_dir.exists():
            return

        # Name aliases: map friendly keys to actual file stems
        _WAV_ALIASES = {
            "single-quack-from-a-duck": "quack",
        }

        # Music file stems (WAV files that should be treated as music, not SFX)
        _MUSIC_STEMS = {"Bell Breeze Loop", "sunny_day1", "sunny_day2"}
        # WAV music files also accessible via play_wav_music (need to be in both dicts)
        _WAV_MUSIC_STEMS = {"Title"}

        # Scan for WAV files in root audio dir
        for wav_file in self._audio_dir.glob("*.wav"):
            stem = wav_file.stem
            if stem in _MUSIC_STEMS:
                # Register as music only
                self._available_music[wav_file.name] = wav_file
                self._available_music[stem.lower()] = wav_file
                logger.debug("Found music WAV: %s", stem)
            elif stem in _WAV_MUSIC_STEMS:
                # Register as both music and WAV (for play_wav_music)
                self._available_music[wav_file.name] = wav_file
                self._available_music[stem.lower()] = wav_file
                self._available_wavs[stem.lower()] = wav_file
                self._available_wavs[stem] = wav_file
                logger.debug("Found WAV music: %s", stem)
            else:
                # Register as SFX under stem (lowercase) and any alias
                key = stem.lower()
                self._available_wavs[key] = wav_file
                self._available_wavs[stem] = wav_file
                if stem in _WAV_ALIASES:
                    self._available_wavs[_WAV_ALIASES[stem]] = wav_file
                logger.debug("Found WAV: %s", key)

        # Scan sfx/ subdirectory if it exists
        sfx_dir = self._audio_dir / "sfx"
        if sfx_dir.exists():
            for wav_file in sfx_dir.glob("*.wav"):
                stem = wav_file.stem
                self._available_wavs[stem.lower()] = wav_file
                self._available_wavs[stem] = wav_file
                if stem in _WAV_ALIASES:
                    self._available_wavs[_WAV_ALIASES[stem]] = wav_file
                logger.debug("Found SFX WAV: %s", stem)

        # Scan for MP3/OGG music files
        for ext in ('*.mp3', '*.ogg'):
            for music_file in self._audio_dir.glob(ext):
                self._available_music[music_file.name] = music_file
                # Also register under lowercase stem for easy lookup
                self._available_music[music_file.stem.lower()] = music_file
                logger.debug("Found music: %s", music_file.name)

        # Scan music/ subdirectory if it exists
        music_dir = self._audio_dir / "music"
        if music_dir.exists():
            for music_file in music_dir.glob("*.*"):
                if music_file.suffix.lower() in ('.wav', '.mp3', '.ogg'):
                    self._available_music[music_file.name] = music_file
                    self._available_music[music_file.stem.lower()] = music_file
                    logger.debug("Found music: %s", music_file.name)

    def play_background_music(self, track_name: str = None):
        """Play background music. Uses pygame streaming for MP3/OGG, or WAV player."""
        if not self.enabled or self.music_muted:
            return

        # Radio takes priority
        if self.is_radio_playing():
            return

        if self._music_playing:
            return  # Already playing

        # Try to find a music file
        music_path = None
        if track_name and track_name in self._available_music:
            music_path = self._available_music[track_name]
        elif self._available_music:
            # Pick a random available track
            track_name = random.choice(list(self._available_music.keys()))
            music_path = self._available_music[track_name]

        if not music_path or not music_path.exists():
            return

        # Use pygame for music (supports MP3/OGG streaming)
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self._music_playing = True
                logger.debug("Playing music: %s", track_name)
                return
            except Exception as e:
                logger.debug("pygame music failed: %s", e)

        # Fallback to WAV player for WAV files
        if music_path.suffix.lower() == '.wav':
            self.play_wav_music(music_path.stem, loop=True)

    def stop_background_music(self):
        """Stop background music."""
        self._music_playing = False
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.stop()
            except Exception:
                pass
        self.stop_music()

    def toggle_music(self) -> bool:
        """Toggle music mute. Returns new mute state."""
        self.music_muted = not self.music_muted
        if self.music_muted:
            self.stop_background_music()
        # When re-enabling, don't force-start — let the normal
        # update_music() cycle handle when music should next play.
        return self.music_muted

    # Alias used by InputDispatcher and game.py
    toggle_music_mute = toggle_music

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

    # ============== RADIO INTEGRATION ==============

    def get_radio(self):
        """Get the radio player instance, configured to mute game music."""
        if self._radio is None:
            from audio.radio import get_radio_player
            self._radio = get_radio_player()
            # Set up callbacks once when radio is first accessed
            self._radio.set_on_start_callback(self._mute_music_for_radio)
            self._radio.set_on_hour_chime(self._play_hour_chime)
        return self._radio

    def _mute_music_for_radio(self):
        """Mute game music when radio is playing."""
        self._current_context = None  # reset so music restarts when radio stops
        self.stop_music()

    def _play_hour_chime(self):
        """Play a clock chime when the hour changes on Nook Radio."""
        self.play_sound(SoundType.HOUR_CHIME)

    def play_radio(self, station_id=None):
        """
        Start radio playback.

        Args:
            station_id: Optional StationID to play. If None, uses last station.
        """
        # Stop background music if playing - can't have both at once
        if self._music_playing:
            self.stop_background_music()

        radio = self.get_radio()
        if station_id is None:
            # Use last station from settings if available
            try:
                from core.settings import settings_manager
                last_station = settings_manager.settings.audio.last_radio_station
                if last_station:
                    from audio.radio import StationID
                    station_id = StationID(last_station)
            except Exception:
                pass
        radio.play(station_id)

    def stop_radio(self):
        """Stop radio playback."""
        self.get_radio().stop()
        self._current_context = None  # allow update_music() to restart after radio stops

    def change_radio_station(self, station_id):
        """Change to a different radio station."""
        from audio.radio import StationID
        if isinstance(station_id, str):
            station_id = StationID(station_id)

        # Stop background music if playing - can't have both at once
        if self._music_playing:
            self.stop_background_music()

        result = self.get_radio().change_station(station_id)

        # Save last station to settings
        if result:
            try:
                from core.settings import settings_manager
                settings_manager.set_value("audio", "last_radio_station", station_id.value)
            except Exception:
                pass

        return result

    def set_radio_volume(self, volume: float):
        """Set radio volume (0.0 to 1.0)."""
        self.get_radio().set_volume(volume)
        try:
            from core.settings import settings_manager
            settings_manager.set_value("audio", "radio_volume", volume)
        except Exception:
            pass

    def is_radio_playing(self) -> bool:
        """Check if radio is currently playing."""
        return self.get_radio().is_playing

    def get_radio_stations(self):
        """Get list of available radio stations for menu display."""
        return self.get_radio().get_station_list()

    def update_radio(self, weather: str = "sunny"):
        """
        Update radio state (call from game loop).

        Handles Nook Radio hour/weather transitions.
        """
        radio = self.get_radio()
        radio.set_weather(weather)
        radio.update()

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

        # Radio takes priority - don't start/update background music
        if self.is_radio_playing():
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

        # Radio takes priority - don't play event music over radio
        if self.is_radio_playing():
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

        # Radio takes priority - don't start background music
        if self.is_radio_playing():
            return

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

        # If no audio file, use synthesized ambient fallback
        if not audio_file:
            self._play_fallback_ambient(new_context)
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

                    # Abort early if radio started or crossfade was cancelled
                    if self.is_radio_playing() or not self._crossfading:
                        self._crossfading = False
                        return

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

                    # Don't start new music if radio started during fade-out
                    if self.is_radio_playing() or not self._crossfading:
                        self._crossfading = False
                        return

                    # Load and start new music at low volume, fade in
                    # Play ONCE (loops=0), not infinite
                    music_path = self._available_music.get(audio_file)
                    if music_path and music_path.exists():
                        try:
                            new_sound = pygame.mixer.Sound(str(music_path))
                            new_sound.set_volume(0)
                            new_channel = new_sound.play(loops=0)  # Play once only
                            if new_channel is None:
                                self._crossfading = False
                                return

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
                                if self.music_muted or self.is_radio_playing():
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

    def _play_fallback_ambient(self, context: MusicContext):
        """
        Play a short synthesized ambient tone sequence when no audio file is available.

        Gives the game an Animal Crossing feel — periodic ambient tones that reflect
        the current time/mood context.  The 2-5 minute cooldown set here ensures they
        play sparingly rather than constantly.
        """
        # Mark context and set cooldown immediately so update_music() won't double-fire
        self._current_context = context
        self._music_cooldown_until = time.time() + random.uniform(120, 300)

        if not self._pygame_available or not self.enabled or self.music_muted:
            return

        # Context → tone sequences  (frequency Hz, duration seconds)
        _AMBIENT_TONES = {
            MusicContext.HAPPY:       [(523, 0.25), (659, 0.25), (784, 0.25), (1047, 0.5)],
            MusicContext.CELEBRATION: [(523, 0.15), (659, 0.15), (784, 0.15), (1047, 0.4), (1318, 0.6)],
            MusicContext.ENERGETIC:   [(523, 0.2),  (659, 0.2),  (784, 0.2),  (523, 0.3)],
            MusicContext.CALM:        [(392, 0.4),  (494, 0.4),  (523, 0.6)],
            MusicContext.MYSTERIOUS:  [(349, 0.5),  (440, 0.4),  (392, 0.7)],
            MusicContext.SAD:         [(349, 0.6),  (311, 0.8)],
            MusicContext.STORMY:      [(261, 0.5),  (220, 0.5),  (196, 0.8)],
            MusicContext.MORNING:     [(523, 0.2),  (659, 0.2),  (784, 0.3)],
            MusicContext.AFTERNOON:   [(392, 0.3),  (523, 0.3),  (659, 0.5)],
            MusicContext.EVENING:     [(330, 0.4),  (415, 0.4),  (392, 0.6)],
            MusicContext.NIGHT:       [(261, 0.6),  (311, 0.5),  (370, 0.8)],
        }

        tones = _AMBIENT_TONES.get(context, _AMBIENT_TONES[MusicContext.CALM])

        def _play():
            try:
                import pygame
                import array
                import math
                sample_rate = 44100
                for freq, duration in tones:
                    if self.is_radio_playing() or self.music_muted:
                        return  # radio started or muted — abort
                    n_samples = int(sample_rate * duration)
                    fade_len = min(int(n_samples * 0.15), 400)
                    buf = array.array('h')
                    for i in range(n_samples):
                        val = math.sin(2 * math.pi * freq * i / sample_rate)
                        if fade_len > 0:
                            if i < fade_len:
                                val *= i / fade_len
                            elif i >= n_samples - fade_len:
                                val *= (n_samples - 1 - i) / fade_len
                        sample = int(val * 32767 * self.music_volume)
                        buf.append(sample)
                        buf.append(sample)
                    sound = pygame.mixer.Sound(buffer=buf)
                    sound.play()
                    pygame.time.wait(int(duration * 1000))
            except Exception:
                pass

        thread = threading.Thread(target=_play, daemon=True)
        thread.start()

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

        self.stop_music()
        self._music_playing = True
        wav_path = self._available_wavs[wav_name]

        # Prefer pygame for music (proper volume control, no subprocess)
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.music.load(str(wav_path))
                pygame.mixer.music.set_volume(self.music_volume)
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops)
                logger.debug("Playing WAV music via pygame: %s", wav_name)
                return
            except Exception as e:
                logger.debug("pygame WAV music failed: %s", e)

        if not self._wav_player:
            return
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
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._wav_player == 'aplay':
                        self._music_process = subprocess.Popen(
                            ['aplay', '-q', str(wav_path)],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                        self._music_process.wait()
                    elif self._wav_player == 'ffplay':
                        self._music_process = subprocess.Popen(
                            ['ffplay', '-nodisp', '-autoexit', '-volume',
                             str(int(music_vol * 100)), str(wav_path)],
                            stdin=subprocess.DEVNULL,
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
        """Play a sound effect. Accepts SoundType enum or string.

        Uses pygame to generate synthesized tones from the SOUND_EFFECTS
        definitions. Falls back to terminal beep methods if pygame is
        unavailable.
        """
        if not self.enabled:
            return

        # Resolve string to SoundType enum
        if isinstance(sound_type, str):
            # Map string names to SoundType values
            _STRING_MAP = {
                "menu_move": SoundType.STEP,
                "menu_select": SoundType.MUSIC_NOTE,
                "collect": SoundType.COLLECT,
                "discovery": SoundType.DISCOVER,
                "craft_complete": SoundType.CRAFT_COMPLETE,
                "build_complete": SoundType.BUILD_COMPLETE,
                "build": SoundType.BUILD_COMPLETE,
                "level_up": SoundType.LEVEL_UP,
                "success": SoundType.LEVEL_UP,
            }
            sound_type = _STRING_MAP.get(sound_type)
            if sound_type is None:
                return

        effects = SOUND_EFFECTS.get(sound_type)
        if not effects:
            return

        # Try pygame sine-wave synthesis
        if self._pygame_available:
            def _play_tones():
                try:
                    import pygame
                    import array
                    import math
                    sample_rate = 44100
                    for freq, duration in effects:
                        n_samples = int(sample_rate * duration)
                        fade_len = min(int(n_samples * 0.1), 200)
                        buf = array.array('h')  # signed short
                        for i in range(n_samples):
                            val = math.sin(2 * math.pi * freq * i / sample_rate)
                            # Apply fade envelope
                            if fade_len > 0:
                                if i < fade_len:
                                    val *= i / fade_len
                                elif i >= n_samples - fade_len:
                                    val *= (n_samples - 1 - i) / fade_len
                            # Scale down synth SFX so they don't overpower music
                            sample = int(val * 32767 * self.volume * 0.15)
                            buf.append(sample)  # left
                            buf.append(sample)  # right
                        sound = pygame.mixer.Sound(buffer=buf)
                        sound.play()
                        pygame.time.wait(int(duration * 1000))
                except Exception:
                    pass

            thread = threading.Thread(target=_play_tones, daemon=True)
            thread.start()
            return

        # Fallback to beep/bell methods
        for freq, duration in effects:
            self.play_tone(freq, duration)

    def play_melody(self, melody_name: str, loop: bool = False):
        """Play a melody. Disabled - use play_background_music() instead."""
        # Terminal beeps disabled - use WAV/MP3 files instead
        pass

    def stop_music(self):
        """Stop currently playing music. Immediate kill, non-blocking."""
        self._music_playing = False

        # Capture and clear references
        proc = self._music_process
        self._music_process = None
        old_thread = self._music_thread
        self._music_thread = None

        # Immediate kill - don't use background thread
        # ffplay with -loop 0 runs forever, so we must use SIGKILL
        if proc:
            try:
                proc.kill()  # SIGKILL - immediate termination
            except OSError:
                pass

        if old_thread is not None and old_thread.is_alive():
            old_thread.join(timeout=1.0)

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

    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0). Affects all sounds."""
        self.volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))

    def set_music_enabled(self, enabled: bool):
        """Enable or disable background music."""
        if enabled:
            self.music_muted = False
        else:
            self.music_muted = True
            self.stop_music()

    def shutdown(self):
        """Clean up all audio resources. Call on game exit."""
        # Stop radio subprocess first
        try:
            self.stop_radio()
        except Exception:
            pass
        self.stop_music()
        # Shutdown the shared thread pool executor
        if SoundEngine._sound_executor is not None:
            SoundEngine._sound_executor.shutdown(wait=False)
            SoundEngine._sound_executor = None
        # Quit pygame mixer if it was initialized
        if self._pygame_available:
            try:
                import pygame
                pygame.mixer.quit()
            except Exception:
                pass
            self._pygame_available = False


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
        self._panic_active = False

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
            elif mood in ["excited", "dramatic"]:
                self.engine.play_sound(SoundType.QUACK_DRAMATIC)
            elif mood == "petty":
                self.engine.play_sound(SoundType.QUACK_PETTY)
            elif mood in ["grumpy", "annoyed"]:
                self.engine.play_sound(SoundType.QUACK_GRUMPY)
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
        # Level up is mixed at 25% volume to avoid being too jarring
        if 'levelup' in self.engine._available_wavs:
            self.engine.play_wav('levelup', volume=0.25)
        else:
            self.engine.play_sound(SoundType.LEVEL_UP)

    def alert(self):
        """Play alert sound."""
        self.engine.play_sound(SoundType.ALERT)

    def step(self):
        """Play footstep sound."""
        self.engine.play_sound(SoundType.STEP)

    def panic(self):
        """Play repeating SOS quack pattern until stop_panic() is called."""
        self._panic_active = True
        def _panic_loop():
            while self._panic_active:
                # SOS: 3 short, 3 long, 3 short
                for _ in range(3):
                    if not self._panic_active:
                        return
                    self.quack("excited")
                    time.sleep(0.1)
                time.sleep(0.15)
                for _ in range(3):
                    if not self._panic_active:
                        return
                    self.quack("excited")
                    time.sleep(0.25)
                time.sleep(0.15)
                for _ in range(3):
                    if not self._panic_active:
                        return
                    self.quack("excited")
                    time.sleep(0.1)
                # Pause between SOS repeats
                time.sleep(0.6)
        self._quack_thread = threading.Thread(target=_panic_loop, daemon=True)
        self._quack_thread.start()

    def stop_panic(self):
        """Stop the SOS panic loop."""
        self._panic_active = False

    def relief(self):
        """Play a relieved sigh-quack — encounter resolved positively."""
        self.stop_panic()
        def _relief_sequence():
            time.sleep(0.2)
            self.quack("happy")
            time.sleep(0.3)
            self.quack("happy")
        self._quack_thread = threading.Thread(target=_relief_sequence, daemon=True)
        self._quack_thread.start()

    def random_quack(self):
        """Play a random quack variation."""
        variations = [
            SoundType.QUACK,
            SoundType.QUACK_HAPPY,
            SoundType.QUACK_EXCITED,
            SoundType.QUACK_GRUMPY,
            SoundType.QUACK_PETTY,
            SoundType.QUACK_DRAMATIC,
        ]
        self.engine.play_sound(random.choice(variations))

    # ── Stingers ────────────────────────────────────────────────────────
    def play_stinger(self, event_type: str):
        """Play a short musical stinger for a game event."""
        stinger_map = {
            "achievement": SoundType.STINGER_ACHIEVEMENT,
            "season_change": SoundType.STINGER_SEASON_CHANGE,
            "friend_arrive": SoundType.STINGER_FRIEND_ARRIVE,
            "milestone": SoundType.STINGER_MILESTONE,
        }
        sound_type = stinger_map.get(event_type)
        if sound_type:
            self.engine.play_sound(sound_type)

    # ── Signature sounds ────────────────────────────────────────────────
    def play_signature(self, action: str):
        """Play a signature sound cue for specific game moments."""
        sig_map = {
            "discover": SoundType.DISCOVER,
            "collect": SoundType.COLLECT,
            "craft": SoundType.CRAFT_COMPLETE,
            "build": SoundType.BUILD_COMPLETE,
            "trade": SoundType.TRADE,
            "level_up": SoundType.LEVEL_UP,
        }
        sound_type = sig_map.get(action)
        if sound_type:
            self.engine.play_sound(sound_type)


# Global instances
sound_engine = SoundEngine()
duck_sounds = DuckSounds(sound_engine)


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
    """
    weather = weather.lower() if weather else "sunny"
    time_of_day = time_of_day.lower() if time_of_day else "day"
    duck_mood = duck_mood.lower() if duck_mood else "content"

    # Priority 1: Events
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
    if duck_mood == "dramatic":
        return MusicContext.ENERGETIC
    if duck_mood == "petty":
        return MusicContext.MYSTERIOUS

    # Priority 4: Atmospheric weather (only truly atmospheric conditions override time-of-day)
    # Sunny/windy are neutral — let time-of-day take precedence for AC-style hourly music
    if weather in ["snowy", "foggy"]:
        return MusicContext.CALM
    if weather == "rainy":
        return MusicContext.MYSTERIOUS

    # Priority 5: Time of day — all 8 periods mapped for Animal Crossing feel
    if time_of_day in ["night", "midnight"]:
        return MusicContext.SAD
    if time_of_day == "late_night":
        return MusicContext.CALM
    if time_of_day in ["dawn", "morning"]:
        return MusicContext.ENERGETIC
    if time_of_day == "midday":
        return MusicContext.HAPPY
    if time_of_day == "afternoon":
        return MusicContext.CALM
    if time_of_day in ["evening", "dusk"]:
        return MusicContext.MYSTERIOUS

    # Priority 6: Default
    return MusicContext.CALM


# ── Event Bus Subscriber Hooks ─────────────────────────────────────────────

def _on_action_sound(event):
    """Hook: play SFX for actions."""
    try:
        action = getattr(event, "action", "")
        action_sound_map = {
            "feed": "eat", "eat": "eat", "pet": "pet",
            "play": "play", "sleep": "sleep", "wake": "wake",
            "clean": "splash", "swim": "splash",
            "craft": "craft_complete", "build": "build_complete",
        }
        wav_name = action_sound_map.get(action)
        if wav_name and wav_name in sound_engine._available_wavs:
            sound_engine.play_wav(wav_name)
        elif action in ("quack", "talk"):
            duck_sounds.quack()
        else:
            logger.debug("No SFX mapped for action=%s", action)
    except Exception:
        logger.debug("Error in _on_action_sound", exc_info=True)


def _on_item_sound(event):
    """Hook: play SFX for item use."""
    try:
        item_name = getattr(event, "item_name", "")
        logger.debug("Item used SFX: %s", item_name)
        item_key = item_name.lower().replace(" ", "_")
        if item_key in sound_engine._available_wavs:
            sound_engine.play_wav(item_key)
        elif any(food in item_key for food in ("bread", "crumb", "seed", "worm", "apple", "pie")):
            duck_sounds.eat()
        elif any(toy in item_key for toy in ("ball", "toy", "mirror")):
            duck_sounds.play()
        else:
            duck_sounds.quack()
    except Exception:
        logger.debug("Error in _on_item_sound", exc_info=True)


def _on_achievement_sound(event):
    """Hook: play achievement jingle."""
    try:
        name = getattr(event, "name", "unknown")
        logger.debug("Achievement SFX: %s", name)
        duck_sounds.level_up()
    except Exception:
        logger.debug("Error in _on_achievement_sound", exc_info=True)


try:
    event_bus.subscribe(ActionPerformedEvent, _on_action_sound, priority=80)
    event_bus.subscribe(ItemUsedEvent, _on_item_sound, priority=80)
    event_bus.subscribe(AchievementUnlockedEvent, _on_achievement_sound, priority=80)
except Exception:
    pass
