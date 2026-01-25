"""
Radio system for Cheese the Duck.

Streams royalty-free music from various duck-themed stations.
Features DJ Duck live sessions on Saturday evenings.

DESIGN: Minimal overhead - just spawn mpv/ffplay and let it run.
No polling loops, no thread management, just subprocess control.
"""

import subprocess
import os
import signal
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Callable, Dict, List


class StationID(Enum):
    """Available radio stations."""
    QUACK_FM = "quack_fm"
    THE_POND = "the_pond"
    BREAD_CRUMBS = "bread_crumbs"
    FEATHER_BONE = "feather_bone"
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


# Station definitions - royalty-free streams
STATIONS: Dict[StationID, RadioStation] = {
    StationID.QUACK_FM: RadioStation(
        id=StationID.QUACK_FM,
        name="Quack FM",
        tagline="Music for staring at walls.",
        stream_url="https://ice1.somafm.com/groovesalad-128-mp3",
        genre="lofi",
        fallback_urls=["https://ice1.somafm.com/lush-128-mp3"]
    ),
    StationID.THE_POND: RadioStation(
        id=StationID.THE_POND,
        name="The Pond",
        tagline="Water. Just water.",
        stream_url="https://ice1.somafm.com/dronezone-128-mp3",
        genre="ambient",
        fallback_urls=["https://ice1.somafm.com/deepspaceone-128-mp3"]
    ),
    StationID.BREAD_CRUMBS: RadioStation(
        id=StationID.BREAD_CRUMBS,
        name="Bread Crumbs",
        tagline="8-bit nostalgia for ducks.",
        stream_url="https://ice1.somafm.com/8bitpoppy-128-mp3",
        genre="chiptune",
        fallback_urls=[]
    ),
    StationID.FEATHER_BONE: RadioStation(
        id=StationID.FEATHER_BONE,
        name="Feather & Bone",
        tagline="Smooth. Like a duck's back.",
        stream_url="https://ice1.somafm.com/secretagent-128-mp3",
        genre="jazz",
        fallback_urls=["https://ice1.somafm.com/sonicuniverse-128-mp3"]
    ),
    StationID.HONK_RADIO: RadioStation(
        id=StationID.HONK_RADIO,
        name="HONK Radio",
        tagline="Chaotic energy for chaotic ducks.",
        stream_url="https://ice1.somafm.com/poptron-128-mp3",
        genre="upbeat",
        fallback_urls=["https://ice1.somafm.com/defcon-128-mp3"]
    ),
    StationID.NOOK_RADIO: RadioStation(
        id=StationID.NOOK_RADIO,
        name="Nook Radio",
        tagline="Hourly vibes. Like a certain island.",
        stream_url="nook",  # Special marker
        genre="hourly",
        fallback_urls=[]
    ),
    StationID.DJ_DUCK_LIVE: RadioStation(
        id=StationID.DJ_DUCK_LIVE,
        name="DJ Duck Live",
        tagline="He's here. He has opinions.",
        stream_url="https://ice1.somafm.com/indiepop-128-mp3",
        genre="eclectic",
        fallback_urls=[],
        always_available=False
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
    
    # Very quiet - background ambiance only
    DEFAULT_VOLUME = 5  # 5% volume
    
    def __init__(self, on_track_change: Optional[Callable[[str], None]] = None):
        self._current_station: Optional[RadioStation] = None
        self._is_playing = False
        self._volume = self.DEFAULT_VOLUME
        self._enabled = True
        self._process: Optional[subprocess.Popen] = None
        self._on_track_change = on_track_change
        self._on_start_callback: Optional[Callable[[], None]] = None
        self._dj_duck_saturdays = True
        self._last_station_before_dj: Optional[StationID] = None
        
        # Find player once at init
        self._player = self._find_player()
    
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
        if self._player == "mpv":
            return [
                "mpv",
                "--no-video",
                "--really-quiet",
                "--no-terminal",
                f"--volume={self._volume}",
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
                "-volume", str(self._volume),
                url
            ]
        elif self._player == "vlc":
            return [
                "vlc",
                "--intf", "dummy",
                "--no-video",
                f"--gain={self._volume / 100}",
                url
            ]
        return []
    
    def _kill_process(self):
        """Kill current process if running."""
        if self._process is None:
            return
        
        try:
            # Try SIGTERM first
            self._process.terminate()
            try:
                self._process.wait(timeout=0.05)
            except subprocess.TimeoutExpired:
                # Force kill
                self._process.kill()
                try:
                    self._process.wait(timeout=0.05)
                except subprocess.TimeoutExpired:
                    pass
        except OSError:
            pass
        
        self._process = None
    
    @property
    def is_playing(self) -> bool:
        return self._is_playing
    
    @property
    def current_station(self) -> Optional[RadioStation]:
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
    
    def set_dj_duck_saturdays(self, enabled: bool):
        self._dj_duck_saturdays = enabled
    
    def set_dj_commentary_callback(self, callback):
        pass  # Not used in minimal implementation
    
    def is_dj_duck_live(self) -> bool:
        if not self._dj_duck_saturdays:
            return False
        now = datetime.now()
        return now.weekday() == 5 and 20 <= now.hour < 24
    
    def get_dj_duck_status(self) -> str:
        if self.is_dj_duck_live():
            return "LIVE NOW"
        now = datetime.now()
        days = (5 - now.weekday()) % 7
        if days == 0:
            return "Live today 8pm" if now.hour < 20 else "Next Saturday"
        elif days == 1:
            return "Tomorrow 8pm"
        return "Saturday 8pm"
    
    def get_available_stations(self) -> List[RadioStation]:
        return list(STATIONS.values())
    
    def play(self, station_id: Optional[StationID] = None):
        """Start playing a station."""
        if not self._enabled or not self._player:
            return
        
        # DJ Duck auto-switch
        if self.is_dj_duck_live() and station_id != StationID.DJ_DUCK_LIVE:
            if self._current_station:
                self._last_station_before_dj = self._current_station.id
            station_id = StationID.DJ_DUCK_LIVE
        
        if station_id is None:
            station_id = StationID.QUACK_FM
        
        station = STATIONS.get(station_id)
        if not station:
            return
        
        if station.id == StationID.DJ_DUCK_LIVE and not self.is_dj_duck_live():
            return
        
        # Kill any existing process first
        self._kill_process()
        
        # Get URL
        if station.id == StationID.NOOK_RADIO:
            url = _get_nook_url()
        else:
            url = station.stream_url
        
        # Build and spawn command
        cmd = self._build_command(url)
        if not cmd:
            return
        
        try:
            # Spawn detached - we don't need to monitor it
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent
            )
        except OSError:
            return
        
        self._current_station = station
        self._is_playing = True
        
        # Mute game music
        if self._on_start_callback:
            try:
                self._on_start_callback()
            except Exception:
                pass
        
        if self._on_track_change:
            self._on_track_change(station.name)
    
    def stop(self):
        """Stop radio."""
        self._kill_process()
        self._is_playing = False
        self._current_station = None
    
    def change_station(self, station_id: StationID) -> bool:
        if station_id == StationID.DJ_DUCK_LIVE and not self.is_dj_duck_live():
            return False
        self.play(station_id)
        return True
    
    def get_station_list(self) -> List[Dict]:
        """Get station list for menu."""
        stations = []
        dj_live = self.is_dj_duck_live()
        
        for station in STATIONS.values():
            is_current = (
                self._current_station and 
                self._current_station.id == station.id
            )
            
            if station.id == StationID.DJ_DUCK_LIVE:
                available = dj_live
                status = self.get_dj_duck_status()
            else:
                available = True
                status = "Playing" if is_current else ""
            
            stations.append({
                "id": station.id,
                "name": station.name,
                "tagline": station.tagline,
                "genre": station.genre,
                "available": available,
                "is_current": is_current,
                "status": status,
            })
        
        return stations
    
    def update(self):
        """Called from game loop - minimal, just check DJ Duck."""
        if not self._is_playing or not self._dj_duck_saturdays:
            return
        
        # Check if DJ Duck time ended
        if self._current_station and self._current_station.id == StationID.DJ_DUCK_LIVE:
            if not self.is_dj_duck_live() and self._last_station_before_dj:
                self.play(self._last_station_before_dj)


# Singleton instance
_radio_player: Optional[RadioPlayer] = None


def get_radio_player() -> RadioPlayer:
    """Get or create the radio player singleton."""
    global _radio_player
    if _radio_player is None:
        _radio_player = RadioPlayer()
    return _radio_player
