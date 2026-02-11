"""
Radio system for Cheese the Duck.

Streams royalty-free music from various duck-themed stations.
Features DJ Duck live sessions on Saturday evenings.

DESIGN: Minimal overhead - just spawn mpv/ffplay and let it run.
No polling loops, no thread management, just subprocess control.
"""

import atexit
import logging
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Callable, Dict, List

logger = logging.getLogger(__name__)


class StationID(Enum):
    """Available radio stations."""
    QUACK_FM = "quack_fm"
    THE_POND = "the_pond"
    BREAD_CRUMBS = "bread_crumbs"
    FEATHER_AND_BONE = "feather_and_bone"
    HONK_RADIO = "honk_radio"
    NOOK_RADIO = "nook_radio"
    DJ_DUCK_LIVE = "dj_duck_live"


@dataclass
class RadioStation:
    """Definition of a radio station."""
    id: StationID
    name: str
    tagline: str
    stream_url: str
    genre: str
    fallback_urls: List[str] = field(default_factory=list)
    always_available: bool = True
    volume_boost: int = 0  # Volume adjustment: positive = louder, negative = quieter


# Station definitions
STATIONS: Dict[StationID, RadioStation] = {
    StationID.QUACK_FM: RadioStation(
        id=StationID.QUACK_FM,
        name="Quack FM",
        tagline="Lofi beats for staring at walls",
        stream_url="https://ice1.somafm.com/groovesalad-256-mp3",
        genre="lofi",
        fallback_urls=["https://ice2.somafm.com/groovesalad-256-mp3"],
        volume_boost=10,
    ),
    StationID.THE_POND: RadioStation(
        id=StationID.THE_POND,
        name="The Pond",
        tagline="Ambient nature sounds",
        stream_url="https://ice1.somafm.com/dronezone-256-mp3",
        genre="ambient",
        fallback_urls=["https://ice2.somafm.com/dronezone-256-mp3"],
        volume_boost=15,
    ),
    StationID.BREAD_CRUMBS: RadioStation(
        id=StationID.BREAD_CRUMBS,
        name="Bread Crumbs",
        tagline="8-bit chiptune nostalgia",
        stream_url="https://stream.laut.fm/chiptune",
        genre="chiptune",
        fallback_urls=["https://ice1.somafm.com/cliqhop-256-mp3"],
        volume_boost=5,
    ),
    StationID.FEATHER_AND_BONE: RadioStation(
        id=StationID.FEATHER_AND_BONE,
        name="Feather & Bone",
        tagline="Smooth jazz",
        stream_url="https://ice1.somafm.com/secretagent-256-mp3",
        genre="jazz",
        fallback_urls=["https://ice2.somafm.com/secretagent-256-mp3"],
        volume_boost=10,
    ),
    StationID.HONK_RADIO: RadioStation(
        id=StationID.HONK_RADIO,
        name="HONK Radio",
        tagline="Chaotic upbeat energy",
        stream_url="https://streams.ilovemusic.de/iloveradio1.mp3",
        genre="dance",
        fallback_urls=["https://stream.laut.fm/partyhard"],
        volume_boost=0,
    ),
    StationID.NOOK_RADIO: RadioStation(
        id=StationID.NOOK_RADIO,
        name="Nook Radio",
        tagline="Hourly music that changes with the time of day",
        stream_url="nook",  # Special marker — URL generated dynamically
        genre="hourly",
        fallback_urls=[],
        volume_boost=30,
    ),
    StationID.DJ_DUCK_LIVE: RadioStation(
        id=StationID.DJ_DUCK_LIVE,
        name="DJ Duck Live",
        tagline="Saturday nights 8pm-midnight with deadpan commentary",
        stream_url="https://ice1.somafm.com/lush-128-mp3",
        genre="live",
        fallback_urls=["https://ice2.somafm.com/lush-128-mp3"],
        always_available=False,  # Only Saturday 8pm-midnight
        volume_boost=10,
    ),
}


def _get_nook_url() -> str:
    """Get current hour's Nook Radio URL."""
    now = datetime.now()
    hour_12 = now.hour % 12 or 12
    am_pm = "am" if now.hour < 12 else "pm"
    return f"https://d17orwheorv96d.cloudfront.net/new-horizons/{hour_12}{am_pm}.ogg"


class RadioPlayer:
    """
    Minimal radio player - just spawns mpv/ffplay subprocess.
    
    No threads, no polling, no locks. Just subprocess management.
    """
    
    # Reasonable default volume
    DEFAULT_VOLUME = 50  # 50% volume
    
    def __init__(self, on_track_change: Optional[Callable[[str], None]] = None):
        self._current_station: Optional[RadioStation] = None
        self._is_playing = False
        self._volume = self.DEFAULT_VOLUME
        self._enabled = True
        self._process: Optional[subprocess.Popen] = None
        self._on_track_change = on_track_change
        self._on_start_callback: Optional[Callable[[], None]] = None
        self._on_hour_chime: Optional[Callable[[], None]] = None

        # Lock to prevent race conditions during station switching
        self._lock = threading.Lock()
        self._generation = 0  # Incremented on each play/stop to prevent stale threads

        # Detect player in background to avoid blocking init
        self._player: Optional[str] = None
        self._player_detected = False
        threading.Thread(target=self._detect_player_background, daemon=True).start()
    
    def _detect_player_background(self):
        """Detect available audio player in background thread."""
        self._player = self._find_player()
        self._player_detected = True
        if self._player:
            logger.info(f"Radio using audio player: {self._player}")
        else:
            logger.warning("No audio player found for radio (install mpv or ffplay)")
    
    @property
    def player_available(self) -> bool:
        """Check if an audio player is available."""
        return self._player_detected and self._player is not None
    
    @property
    def player_status(self) -> str:
        """Get player status for UI display."""
        if not self._player_detected:
            return "Detecting audio player..."
        if not self._player:
            return "No audio player found (install mpv or ffplay)"
        return f"Using {self._player}"
    
    def _find_player(self) -> Optional[str]:
        """Find available audio player."""
        # Each player has different version flag
        player_checks = [
            ("mpv", ["mpv", "--version"]),
            ("ffplay", ["ffplay", "-version"]),  # ffplay uses single dash
            ("vlc", ["vlc", "--version"]),
        ]
        for player, cmd in player_checks:
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return player
            except (OSError, subprocess.TimeoutExpired):
                continue
        return None
    
    def _build_command(self, url: str, loop: bool = False) -> List[str]:
        """Build player command with volume. If loop=True, loop finite tracks."""
        # Get volume with per-station adjustment
        station_boost = 0
        if self._current_station:
            station_boost = self._current_station.volume_boost
        effective_volume = max(0, min(100, self._volume + station_boost))
        
        if self._player == "mpv":
            cmd = [
                "mpv",
                "--no-video",
                "--really-quiet",
                "--no-terminal",
                "--network-timeout=30",  # Prevent hung connection
                f"--volume={effective_volume}",
            ]
            if loop:
                cmd.append("--loop-file=inf")
            cmd.append(url)
            return cmd
        elif self._player == "ffplay":
            cmd = [
                "ffplay",
                "-nodisp",
                "-loglevel", "quiet",
                "-infbuf",  # Use infinite buffer to reduce CPU wake-ups
                "-framedrop",  # Allow frame dropping (audio only anyway)
                "-volume", str(effective_volume),
            ]
            if loop:
                cmd.extend(["-loop", "0"])  # 0 = infinite loop
            else:
                cmd.append("-autoexit")
            cmd.append(url)
            return cmd
        elif self._player == "vlc":
            cmd = [
                "vlc",
                "--intf", "dummy",
                "--no-video",
                f"--gain={effective_volume / 100}",
            ]
            if loop:
                cmd.append("--repeat")
            cmd.append(url)
            return cmd
        return []
    
    def _kill_process(self):
        """Kill current process if running. Must be called with lock held."""
        if self._process is None:
            return

        proc = self._process
        self._process = None  # Clear reference immediately to prevent double-kill

        try:
            # Check if process is still running
            if proc.poll() is not None:
                return  # Already dead

            # Send SIGKILL immediately - ffplay/mpv don't need graceful shutdown
            # This is non-blocking, process will die asynchronously
            proc.kill()

            # Brief wait to reap zombie, but don't block if slow
            try:
                proc.wait(timeout=0.05)
            except subprocess.TimeoutExpired:
                # Spawn background thread to reap zombie later
                def reap():
                    try:
                        proc.wait(timeout=2)
                    except Exception:
                        pass
                threading.Thread(target=reap, daemon=True).start()
        except OSError:
            pass
    
    @property
    def is_playing(self) -> bool:
        with self._lock:
            return self._is_playing
    
    @property
    def current_station(self) -> Optional[RadioStation]:
        with self._lock:
            return self._current_station
    
    @property
    def volume(self) -> float:
        return self._volume / 100.0
    
    @property
    def enabled(self) -> bool:
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value
        if not value:
            self.stop()
    
    def set_volume(self, volume: float):
        """Set volume (0.0 - 1.0)."""
        self._volume = int(max(0, min(100, volume * 100)))
    
    def set_on_start_callback(self, callback: Optional[Callable[[], None]]):
        self._on_start_callback = callback
    
    def get_available_stations(self) -> List[RadioStation]:
        return list(STATIONS.values())
    
    def play(self, station_id: Optional[StationID] = None):
        """Start playing a station. Non-blocking, spawns in background thread."""
        if not self._enabled:
            return
        if not self._player_detected or not self._player:
            return  # Player not yet detected or not available

        if station_id is None:
            station_id = StationID.QUACK_FM

        station = STATIONS.get(station_id)
        if not station:
            return

        # Check DJ Duck Live availability (Saturday 8pm-midnight only)
        if station_id == StationID.DJ_DUCK_LIVE:
            now = datetime.now()
            if now.weekday() != 5 or not (20 <= now.hour < 24):
                return  # Not Saturday evening — DJ Duck is off-air

        # Get URL — special handling for Nook Radio (hour-based)
        is_nook = station.stream_url == "nook"
        if is_nook:
            url = _get_nook_url()
        else:
            url = station.stream_url

        # Build command — loop finite Nook Radio tracks for continuous playback
        cmd = self._build_command(url, loop=is_nook)
        if not cmd:
            return

        # Update state immediately with lock so UI shows "playing"
        with self._lock:
            self._generation += 1
            gen = self._generation
            self._current_station = station
            self._is_playing = True

        # Spawn subprocess in background thread to avoid blocking game loop
        # (subprocess.Popen can be slow due to fork/network)
        def spawn_player():
            with self._lock:
                # Check if stop() was called before we got the lock
                if not self._is_playing or self._generation != gen:
                    return  # Cancelled or superseded, don't spawn

                # Kill any existing process first
                self._kill_process()

                try:
                    # Spawn subprocess with all stdio redirected to prevent terminal interference
                    self._process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.DEVNULL,   # Don't steal terminal input!
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except OSError as e:
                    logger.warning(f"Failed to spawn radio player: {e}")
                    self._is_playing = False
                    self._current_station = None

        threading.Thread(target=spawn_player, daemon=True).start()

        # Callbacks - these should be fast
        if self._on_start_callback:
            try:
                self._on_start_callback()
            except Exception:
                pass

        if self._on_track_change:
            self._on_track_change(station.name)
    
    def stop(self):
        """Stop radio. Non-blocking."""
        # Update state immediately with lock
        with self._lock:
            self._generation += 1
            gen = self._generation
            self._is_playing = False
            self._current_station = None

        # Kill process in background thread to avoid blocking
        def kill_in_background():
            with self._lock:
                # Only kill if no newer play() has started
                if self._generation == gen:
                    self._kill_process()

        threading.Thread(target=kill_in_background, daemon=True).start()
    
    def change_station(self, station_id: StationID) -> bool:
        self.play(station_id)
        return True
    
    def get_station_list(self) -> List[Dict]:
        """Get station list for menu."""
        stations = []
        now = datetime.now()
        
        for station in STATIONS.values():
            is_current = (
                self._current_station and 
                self._current_station.id == station.id
            )
            
            # Check availability for DJ Duck Live
            available = True
            status_text = ""
            if station.id == StationID.DJ_DUCK_LIVE:
                if now.weekday() != 5 or not (20 <= now.hour < 24):
                    available = False
                    status_text = "Saturday 8pm-midnight"
                elif is_current:
                    status_text = "Playing"
                else:
                    status_text = "ON AIR"
            elif is_current:
                status_text = "Playing"
            
            stations.append({
                "id": station.id,
                "name": station.name,
                "tagline": station.tagline,
                "genre": station.genre,
                "available": available,
                "is_current": is_current,
                "status": status_text,
            })
        
        return stations
    
    def set_on_hour_chime(self, callback: Optional[Callable[[], None]]):
        """Set callback fired when Nook Radio crosses an hour boundary."""
        self._on_hour_chime = callback

    def update(self):
        """Called from game loop — handle Nook Radio hour transitions and track looping."""
        if not self._is_playing or not self._current_station:
            return
        
        # Nook Radio needs to switch streams on the hour
        if self._current_station.id == StationID.NOOK_RADIO:
            now = datetime.now()
            if not hasattr(self, '_last_nook_hour'):
                self._last_nook_hour = now.hour
            if now.hour != self._last_nook_hour:
                self._last_nook_hour = now.hour
                # Play hour chime
                if self._on_hour_chime:
                    try:
                        self._on_hour_chime()
                    except Exception:
                        pass
                self.play(StationID.NOOK_RADIO)  # Restart with new hour URL
            else:
                # Check if track process died unexpectedly (e.g. player doesn't
                # support --loop).  Restart to keep music going.
                with self._lock:
                    if self._process is not None and self._process.poll() is not None:
                        self._process = None
                # Restart outside lock
                if self._process is None:
                    self.play(StationID.NOOK_RADIO)
        
        # DJ Duck Live goes off-air at midnight
        if self._current_station.id == StationID.DJ_DUCK_LIVE:
            now = datetime.now()
            if now.weekday() != 5 or not (20 <= now.hour < 24):
                self.stop()  # Show's over


# Singleton instance with thread-safe initialization
_radio_player: Optional[RadioPlayer] = None
_radio_player_lock = threading.Lock()


def _cleanup_radio():
    """Kill radio process on program exit."""
    global _radio_player
    if _radio_player is not None:
        try:
            # Direct kill, no threads - we're exiting
            if _radio_player._process and _radio_player._process.poll() is None:
                _radio_player._process.kill()
                _radio_player._process.wait(timeout=0.1)
        except Exception:
            pass


# Register cleanup handler
atexit.register(_cleanup_radio)


def get_radio_player() -> RadioPlayer:
    """Get or create the radio player singleton. Thread-safe."""
    global _radio_player
    if _radio_player is None:
        with _radio_player_lock:
            # Double-check after acquiring lock
            if _radio_player is None:
                _radio_player = RadioPlayer()
    return _radio_player
