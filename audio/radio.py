"""
Radio system for Cheese the Duck.

Streams royalty-free music from various duck-themed stations.
Features DJ Duck live sessions on Saturday evenings.
"""

import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Callable, Dict, List
import urllib.request
import urllib.error


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
    # Fallback URLs if primary fails
    fallback_urls: List[str] = field(default_factory=list)
    # Whether this station is always available
    always_available: bool = True


# Station definitions with royalty-free stream URLs
# Using public radio streams that allow non-commercial use
STATIONS: Dict[StationID, RadioStation] = {
    StationID.QUACK_FM: RadioStation(
        id=StationID.QUACK_FM,
        name="Quack FM",
        tagline="Music for staring at walls.",
        stream_url="https://streams.ilovemusic.de/iloveradio17.mp3",  # Lofi stream
        genre="lofi",
        fallback_urls=[
            "https://stream.laut.fm/lofi",
            "https://streams.fluxfm.de/Chillhop/mp3-128/streams.fluxfm.de/",
        ]
    ),
    StationID.THE_POND: RadioStation(
        id=StationID.THE_POND,
        name="The Pond",
        tagline="Water. Just water.",
        stream_url="https://stream.laut.fm/natureclassics",  # Nature/ambient
        genre="ambient",
        fallback_urls=[
            "https://ice1.somafm.com/dronezone-128-mp3",
            "https://ice1.somafm.com/deepspaceone-128-mp3",
        ]
    ),
    StationID.BREAD_CRUMBS: RadioStation(
        id=StationID.BREAD_CRUMBS,
        name="Bread Crumbs",
        tagline="8-bit nostalgia for ducks.",
        stream_url="https://ice1.somafm.com/8bitpoppy-128-mp3",  # Chiptune
        genre="chiptune",
        fallback_urls=[
            "https://rainwave.cc/tune_in/5.ogg",
            "https://stream.laut.fm/chiptunes",
        ]
    ),
    StationID.FEATHER_BONE: RadioStation(
        id=StationID.FEATHER_BONE,
        name="Feather & Bone",
        tagline="Smooth. Like a duck's back.",
        stream_url="https://ice1.somafm.com/secretagent-128-mp3",  # Jazz/lounge
        genre="jazz",
        fallback_urls=[
            "https://ice1.somafm.com/sonicuniverse-128-mp3",
            "https://stream.laut.fm/jazz",
        ]
    ),
    StationID.HONK_RADIO: RadioStation(
        id=StationID.HONK_RADIO,
        name="HONK Radio",
        tagline="Chaotic energy for chaotic ducks.",
        stream_url="https://ice1.somafm.com/poptron-128-mp3",  # Upbeat electronic
        genre="upbeat",
        fallback_urls=[
            "https://ice1.somafm.com/defcon-128-mp3",
            "https://stream.laut.fm/electroswing",
        ]
    ),
    StationID.NOOK_RADIO: RadioStation(
        id=StationID.NOOK_RADIO,
        name="Nook Radio",
        tagline="Hourly vibes. Like a certain island.",
        stream_url="hourly",  # Special marker for hourly music
        genre="hourly",
        fallback_urls=[]
    ),
    StationID.DJ_DUCK_LIVE: RadioStation(
        id=StationID.DJ_DUCK_LIVE,
        name="DJ Duck Live",
        tagline="He's here. He has opinions.",
        stream_url="https://ice1.somafm.com/groovesalad-128-mp3",  # Eclectic mix
        genre="eclectic",
        fallback_urls=[
            "https://ice1.somafm.com/lush-128-mp3",
            "https://ice1.somafm.com/indiepop-128-mp3",
        ],
        always_available=False  # Only on Saturdays 8pm-midnight
    ),
}


class RadioPlayer:
    """
    Handles streaming radio playback for the game.
    
    Runs on a separate thread to not block the game loop.
    Uses mpv/ffplay for streaming, with pygame fallback.
    """
    
    def __init__(self, on_track_change: Optional[Callable[[str], None]] = None):
        """
        Initialize the radio player.
        
        Args:
            on_track_change: Callback when track/station changes (for DJ Duck commentary)
        """
        self._current_station: Optional[RadioStation] = None
        self._is_playing = False
        self._volume = 0.15  # 15% default - radio should be subtle background
        self._enabled = True
        self._process: Optional[subprocess.Popen] = None
        self._play_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()  # Protect process and generation access
        self._generation = 0  # Incremented on each play/stop to invalidate old threads
        self._on_track_change = on_track_change
        self._last_station_before_dj: Optional[StationID] = None
        self._dj_duck_saturdays = True
        
        # Detect available player (cache result)
        self._player_cmd = self._detect_player()
        
        # DJ Duck commentary callback
        self._dj_commentary_callback: Optional[Callable[[], str]] = None
        
        # Callback when radio starts (for muting game music)
        self._on_start_callback: Optional[Callable[[], None]] = None
    
    def set_on_start_callback(self, callback: Optional[Callable[[], None]]):
        """Set callback to run when radio starts (e.g., mute game music)."""
        self._on_start_callback = callback
    
    def _detect_player(self) -> Optional[List[str]]:
        """Detect available audio player for streaming."""
        players = [
            (["mpv", "--no-video", "--really-quiet"], "mpv"),
            (["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"], "ffplay"),
            (["vlc", "--intf", "dummy", "--no-video"], "vlc"),
        ]
        
        for cmd, name in players:
            try:
                result = subprocess.run(
                    [cmd[0], "--version"],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return cmd
            except (subprocess.SubprocessError, FileNotFoundError, OSError):
                continue
        
        return None
    
    @property
    def is_playing(self) -> bool:
        """Whether radio is currently playing."""
        return self._is_playing
    
    @property
    def current_station(self) -> Optional[RadioStation]:
        """Currently playing station."""
        return self._current_station
    
    @property
    def volume(self) -> float:
        """Current volume level (0.0 - 1.0)."""
        return self._volume
    
    @property
    def enabled(self) -> bool:
        """Whether radio is enabled."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool):
        """Enable or disable radio."""
        self._enabled = value
        if not value and self._is_playing:
            self.stop()
    
    def set_volume(self, volume: float):
        """Set radio volume (0.0 - 1.0)."""
        self._volume = max(0.0, min(1.0, volume))
        # Volume is applied when starting stream, can't change mid-stream easily
    
    def set_dj_duck_saturdays(self, enabled: bool):
        """Enable/disable automatic DJ Duck on Saturdays."""
        self._dj_duck_saturdays = enabled
    
    def set_dj_commentary_callback(self, callback: Optional[Callable[[], str]]):
        """Set callback for DJ Duck commentary generation."""
        self._dj_commentary_callback = callback
    
    def is_dj_duck_live(self) -> bool:
        """Check if DJ Duck should be live (Saturday 8pm-midnight)."""
        if not self._dj_duck_saturdays:
            return False
        
        now = datetime.now()
        # Saturday = 5 (Monday is 0)
        is_saturday = now.weekday() == 5
        is_evening = 20 <= now.hour < 24
        
        return is_saturday and is_evening
    
    def get_dj_duck_status(self) -> str:
        """Get DJ Duck availability status string."""
        if self.is_dj_duck_live():
            return "🔴 LIVE NOW"
        
        now = datetime.now()
        days_until_saturday = (5 - now.weekday()) % 7
        if days_until_saturday == 0 and now.hour >= 24:
            days_until_saturday = 7
        
        if days_until_saturday == 0:
            if now.hour < 20:
                return f"Live today at 8pm"
            else:
                return "Returns next Saturday 8pm"
        elif days_until_saturday == 1:
            return "Live tomorrow at 8pm"
        else:
            return f"Returns Saturday 8pm"
    
    def get_available_stations(self) -> List[RadioStation]:
        """Get list of currently available stations."""
        available = []
        for station in STATIONS.values():
            if station.always_available or self.is_dj_duck_live():
                available.append(station)
            elif station.id == StationID.DJ_DUCK_LIVE:
                # Include DJ Duck but mark as unavailable
                available.append(station)
        return available
    
    def play(self, station_id: Optional[StationID] = None):
        """
        Start playing a radio station.
        
        Args:
            station_id: Station to play. If None, uses last station or default.
        """
        if not self._enabled:
            return
        
        if self._player_cmd is None:
            # No player available
            return
        
        # Check for DJ Duck auto-switch
        if self.is_dj_duck_live() and station_id != StationID.DJ_DUCK_LIVE:
            if self._current_station and self._current_station.id != StationID.DJ_DUCK_LIVE:
                self._last_station_before_dj = self._current_station.id
            station_id = StationID.DJ_DUCK_LIVE
        
        # Default to Quack FM
        if station_id is None:
            station_id = StationID.QUACK_FM
        
        station = STATIONS.get(station_id)
        if not station:
            return
        
        # Don't allow DJ Duck outside of schedule
        if station.id == StationID.DJ_DUCK_LIVE and not self.is_dj_duck_live():
            return
        
        # Stop current playback (fast)
        self.stop()
        
        self._current_station = station
        self._is_playing = True
        
        # Get new generation under lock - this invalidates any old threads
        with self._lock:
            self._generation += 1
            my_generation = self._generation
        
        # Mute game music when radio starts
        if self._on_start_callback:
            try:
                self._on_start_callback()
            except Exception:
                pass
        
        # Start playback in background thread with generation token
        self._play_thread = threading.Thread(
            target=self._stream_loop,
            args=(station, my_generation),
            daemon=True
        )
        self._play_thread.start()
        
        # Trigger track change callback
        if self._on_track_change:
            self._on_track_change(station.name)
    
    def stop(self):
        """Stop radio playback - kills process immediately."""
        self._is_playing = False
        self._current_station = None
        
        # Increment generation and get process under lock
        # This invalidates any running threads immediately
        with self._lock:
            self._generation += 1
            proc = self._process
            self._process = None
        
        # Kill process outside lock
        if proc:
            try:
                proc.kill()  # SIGKILL
                proc.wait(timeout=0.1)  # Brief wait to reap zombie
            except (OSError, subprocess.TimeoutExpired):
                pass
        
        self._play_thread = None
    
    def change_station(self, station_id: StationID):
        """Change to a different station."""
        if station_id == StationID.DJ_DUCK_LIVE and not self.is_dj_duck_live():
            return False
        
        self.play(station_id)
        return True
    
    def _is_stale(self, generation: int) -> bool:
        """Check if this thread's generation is outdated."""
        with self._lock:
            return self._generation != generation
    
    def _stream_loop(self, station: RadioStation, generation: int):
        """Background thread that handles streaming."""
        # Check if already stale before doing anything
        if self._is_stale(generation):
            return
            
        # Special handling for Nook Radio (hourly music)
        if station.id == StationID.NOOK_RADIO:
            self._nook_radio_loop(generation)
            return
        
        urls_to_try = [station.stream_url] + station.fallback_urls
        
        for url in urls_to_try:
            if self._is_stale(generation):
                return
            
            try:
                # Build command with volume
                cmd = self._player_cmd.copy()
                
                # Add volume flag based on player
                if "mpv" in cmd[0]:
                    cmd.extend([f"--volume={int(self._volume * 100)}", url])
                elif "ffplay" in cmd[0]:
                    cmd.extend(["-volume", str(int(self._volume * 100)), url])
                else:
                    cmd.append(url)
                
                # Check again before spawning
                if self._is_stale(generation):
                    return
                
                # Create process under lock
                with self._lock:
                    if self._generation != generation:
                        return
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self._process = proc
                
                # Wait for process to end or generation change
                while not self._is_stale(generation):
                    if proc.poll() is not None:
                        # Process ended, try next URL or restart
                        break
                    
                    # Check if DJ Duck time ended
                    if station.id == StationID.DJ_DUCK_LIVE and not self.is_dj_duck_live():
                        # Switch back to previous station
                        if self._last_station_before_dj:
                            threading.Thread(
                                target=lambda: self.play(self._last_station_before_dj),
                                daemon=True
                            ).start()
                        return
                    
                    time.sleep(0.5)
                
                # Clean up if we're stale (another station started)
                if self._is_stale(generation):
                    try:
                        proc.kill()
                    except OSError:
                        pass
                    return
                
            except (subprocess.SubprocessError, OSError):
                continue
    
    def _nook_radio_loop(self, generation: int):
        """
        Play hourly Animal Crossing-style music from nook.camp CDN.
        
        Music changes based on the current hour and loops until stopped.
        """
        # Nook-desktop CDN base URL
        base_url = "https://d17orwheorv96d.cloudfront.net"
        # Available game soundtracks
        games = ["new-leaf", "new-horizons", "wild-world", "population-growing"]
        current_game_idx = 0
        last_hour = None
        local_proc = None  # Track process locally
        
        while not self._is_stale(generation):
            # Get current hour in nook format
            now = datetime.now()
            hour_12 = now.hour % 12 or 12
            am_pm = "am" if now.hour < 12 else "pm"
            hour_str = f"{hour_12}{am_pm}"
            
            # Check if hour changed - switch track
            if hour_str != last_hour:
                last_hour = hour_str
                
                # Stop current track if playing
                if local_proc and local_proc.poll() is None:
                    try:
                        local_proc.kill()
                        local_proc.wait(timeout=0.5)
                    except (subprocess.TimeoutExpired, OSError):
                        pass
                
                # Check if stale after cleanup
                if self._is_stale(generation):
                    return
                
                # Build URL for current hour
                game = games[current_game_idx % len(games)]
                url = f"{base_url}/{game}/{hour_str}.ogg"
                
                # Try to play
                if self._player_cmd:
                    try:
                        cmd = self._player_cmd.copy()
                        
                        # Add volume and loop flags
                        if "mpv" in cmd[0]:
                            cmd.extend([
                                f"--volume={int(self._volume * 100)}",
                                "--loop=inf",  # Loop the hourly track
                                url
                            ])
                        elif "ffplay" in cmd[0]:
                            cmd.extend([
                                "-volume", str(int(self._volume * 100)),
                                "-loop", "0",  # Loop forever
                                url
                            ])
                        else:
                            cmd.append(url)
                        
                        with self._lock:
                            if self._generation != generation:
                                return
                            local_proc = subprocess.Popen(
                                cmd,
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                            self._process = local_proc
                    except (subprocess.SubprocessError, OSError):
                        # Try next game on failure
                        current_game_idx += 1
            
            # Wait before checking again (check every 0.5 seconds for responsiveness)
            for _ in range(60):  # 30 second total check interval
                if self._is_stale(generation):
                    if local_proc:
                        try:
                            local_proc.kill()
                        except OSError:
                            pass
                    return
                time.sleep(0.5)
    
    def get_station_list(self) -> List[Dict]:
        """Get formatted list of stations for menu display."""
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
                status = "▶ Now Playing" if is_current else ""
            
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
        """
        Called periodically to check for DJ Duck schedule changes.
        
        Call this from the game loop to auto-switch to/from DJ Duck.
        """
        if not self._is_playing or not self._dj_duck_saturdays:
            return
        
        dj_live = self.is_dj_duck_live()
        
        # Auto-switch to DJ Duck when going live
        if dj_live and self._current_station:
            if self._current_station.id != StationID.DJ_DUCK_LIVE:
                self._last_station_before_dj = self._current_station.id
                self.change_station(StationID.DJ_DUCK_LIVE)
                
                # Generate DJ commentary
                if self._dj_commentary_callback:
                    try:
                        self._dj_commentary_callback()
                    except Exception:
                        pass
        
        # Auto-switch away from DJ Duck when show ends
        elif not dj_live and self._current_station:
            if self._current_station.id == StationID.DJ_DUCK_LIVE:
                target = self._last_station_before_dj or StationID.QUACK_FM
                self.change_station(target)


# Singleton instance
_radio_player: Optional[RadioPlayer] = None


def get_radio_player() -> RadioPlayer:
    """Get the global radio player instance."""
    global _radio_player
    if _radio_player is None:
        _radio_player = RadioPlayer()
    return _radio_player
