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
    NOOK_RADIO = "nook_radio"


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


# Station definitions - just Nook Radio now
STATIONS: Dict[StationID, RadioStation] = {
    StationID.NOOK_RADIO: RadioStation(
        id=StationID.NOOK_RADIO,
        name="Nook Radio",
        tagline="Hourly vibes. Like a certain island.",
        stream_url="nook",  # Special marker
        genre="hourly",
        fallback_urls=[],
        volume_boost=30  # Boost volume for better audibility
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
    
    def _build_command(self, url: str) -> List[str]:
        """Build player command with volume."""
        # Get volume with per-station adjustment
        station_boost = 0
        if self._current_station:
            station_boost = self._current_station.volume_boost
        effective_volume = max(0, min(100, self._volume + station_boost))
        
        if self._player == "mpv":
            return [
                "mpv",
                "--no-video",
                "--really-quiet",
                "--no-terminal",
                "--network-timeout=30",  # Prevent hung connection
                f"--volume={effective_volume}",
                url
            ]
        elif self._player == "ffplay":
            return [
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-loglevel", "quiet",
                "-infbuf",  # Use infinite buffer to reduce CPU wake-ups
                "-framedrop",  # Allow frame dropping (audio only anyway)
                "-volume", str(effective_volume),
                url
            ]
        elif self._player == "vlc":
            return [
                "vlc",
                "--intf", "dummy",
                "--no-video",
                f"--gain={effective_volume / 100}",
                url
            ]
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
            station_id = StationID.NOOK_RADIO

        station = STATIONS.get(station_id)
        if not station:
            return

        # Get URL for Nook Radio (hour-based)
        url = _get_nook_url()

        # Build command before spawning thread
        cmd = self._build_command(url)
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
        
        for station in STATIONS.values():
            is_current = (
                self._current_station and 
                self._current_station.id == station.id
            )
            
            stations.append({
                "id": station.id,
                "name": station.name,
                "tagline": station.tagline,
                "genre": station.genre,
                "available": True,
                "is_current": is_current,
                "status": "Playing" if is_current else "",
            })
        
        return stations
    
    def update(self):
        """Called from game loop - no-op now that DJ Duck is removed."""
        pass


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
