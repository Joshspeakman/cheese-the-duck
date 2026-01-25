"""
Auto-update system for Cheese the Duck.
Checks GitHub releases and updates the game while preserving save files.
"""
import os
import sys
import json
import shutil
import tempfile
import zipfile
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    import urllib.request
    import urllib.error
    HAS_URLLIB = True
except ImportError:
    HAS_URLLIB = False

from config import GAME_DIR, SAVE_DIR


# Game version - Update this when releasing new versions
GAME_VERSION = "1.6.0"

# GitHub repository info
GITHUB_OWNER = "Joshspeakman"
GITHUB_REPO = "cheese-the-duck"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
GITHUB_TAGS_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/tags"

# URL for pre-built .deb packages (we'll build and host these)
DEB_DOWNLOAD_URL = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases/download"


class UpdateStatus(Enum):
    """Status of the update check."""
    UP_TO_DATE = "up_to_date"
    UPDATE_AVAILABLE = "update_available"
    CHECK_FAILED = "check_failed"
    NO_INTERNET = "no_internet"
    UPDATING = "updating"
    UPDATE_COMPLETE = "update_complete"
    UPDATE_FAILED = "update_failed"


@dataclass
class UpdateInfo:
    """Information about an available update."""
    current_version: str
    latest_version: str
    release_notes: str
    download_url: str
    status: UpdateStatus


class GameUpdater:
    """Handles checking for and applying game updates."""

    def __init__(self):
        self.current_version = GAME_VERSION
        self._update_info: Optional[UpdateInfo] = None
        self._last_check_error: Optional[str] = None
        # Check if we're in a system-managed location (apt install)
        self._is_system_install = self._check_system_install()
    
    def _check_system_install(self) -> bool:
        """Check if the game is installed in a system location (e.g., /opt, /usr)."""
        game_path = str(GAME_DIR)
        system_prefixes = ['/opt/', '/usr/', '/snap/']
        return any(game_path.startswith(prefix) for prefix in system_prefixes)
    
    def is_system_install(self) -> bool:
        """Return True if this is a system-level installation (apt/deb)."""
        return self._is_system_install
    
    def is_updatable(self) -> bool:
        """Return True if the game can be updated in-place (non-system install)."""
        if self._is_system_install:
            return False
        # Check if we have write permission
        try:
            test_file = GAME_DIR / ".update_test"
            test_file.touch()
            test_file.unlink()
            return True
        except (OSError, PermissionError):
            return False

    def _parse_version(self, version_str: str) -> Tuple[int, ...]:
        """Parse version string into tuple for comparison."""
        # Remove 'v' prefix if present
        version_str = version_str.lstrip('v').strip()
        try:
            parts = version_str.split('.')
            result = []
            for p in parts:
                # Extract leading digits (handles suffixes like '1a', '2b')
                num = ''
                for c in p:
                    if c.isdigit():
                        num += c
                    else:
                        break
                result.append(int(num) if num else 0)
            return tuple(result) if result else (0, 0, 0)
        except (ValueError, AttributeError):
            return (0, 0, 0)

    def _version_compare(self, v1: str, v2: str) -> int:
        """
        Compare two version strings.
        Returns: -1 if v1 < v2, 0 if equal, 1 if v1 > v2
        """
        v1_tuple = self._parse_version(v1)
        v2_tuple = self._parse_version(v2)
        
        if v1_tuple < v2_tuple:
            return -1
        elif v1_tuple > v2_tuple:
            return 1
        return 0

    def _refresh_current_version(self):
        """Re-read the current version from the source file in case it was updated."""
        try:
            updater_path = Path(__file__)
            content = updater_path.read_text()
            for line in content.split('\n'):
                if line.startswith('GAME_VERSION'):
                    # Extract version from: GAME_VERSION = "1.2.9"
                    version = line.split('=')[1].strip().strip('"').strip("'")
                    self.current_version = version
                    break
        except Exception:
            pass  # Keep existing version if read fails

    def check_for_updates(self) -> UpdateInfo:
        """
        Check GitHub for the latest release (tries tags first, then releases).
        
        Returns:
            UpdateInfo with status and version details
        """
        # Refresh version in case files were updated externally
        self._refresh_current_version()
        
        if not HAS_URLLIB:
            return UpdateInfo(
                current_version=self.current_version,
                latest_version="",
                release_notes="",
                download_url="",
                status=UpdateStatus.CHECK_FAILED
            )

        try:
            headers = {
                'User-Agent': f'CheeseTheDuck/{self.current_version}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Try tags API first (more reliable for this repo)
            latest_version = None
            download_url = ""
            release_notes = ""
            
            try:
                request = urllib.request.Request(GITHUB_TAGS_URL, headers=headers)
                with urllib.request.urlopen(request, timeout=10) as response:
                    tags_data = json.loads(response.read().decode('utf-8'))
                
                if tags_data and len(tags_data) > 0:
                    latest_version = tags_data[0].get('name', '0.0.0')
                    # Build download URL from tag
                    download_url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/tags/{latest_version}.zip"
                    release_notes = f"Update to {latest_version}"
            except Exception:
                pass  # Fall through to releases API
            
            # If tags didn't work, try releases API
            if not latest_version:
                request = urllib.request.Request(GITHUB_API_URL, headers=headers)
                with urllib.request.urlopen(request, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                
                latest_version = data.get('tag_name', '0.0.0')
                release_notes = data.get('body', 'No release notes available.')
                
                # Find the source code zip download URL
                assets = data.get('assets', [])
                for asset in assets:
                    if asset.get('name', '').endswith('.zip'):
                        download_url = asset.get('browser_download_url', '')
                        break
                
                # If no asset, use the auto-generated source zip
                if not download_url:
                    download_url = data.get('zipball_url', '')
            
            # Compare versions
            comparison = self._version_compare(self.current_version, latest_version)
            
            if comparison < 0:
                status = UpdateStatus.UPDATE_AVAILABLE
            else:
                status = UpdateStatus.UP_TO_DATE
            
            self._update_info = UpdateInfo(
                current_version=self.current_version,
                latest_version=latest_version,
                release_notes=release_notes[:500] if release_notes else "",
                download_url=download_url,
                status=status
            )
            return self._update_info

        except urllib.error.HTTPError as e:
            self._last_check_error = str(e)
            # 404 means no releases exist yet
            if e.code == 404:
                return UpdateInfo(
                    current_version=self.current_version,
                    latest_version="",
                    release_notes="",
                    download_url="",
                    status=UpdateStatus.UP_TO_DATE  # No releases = up to date
                )
            return UpdateInfo(
                current_version=self.current_version,
                latest_version="",
                release_notes="",
                download_url="",
                status=UpdateStatus.CHECK_FAILED
            )
        except urllib.error.URLError as e:
            self._last_check_error = str(e)
            return UpdateInfo(
                current_version=self.current_version,
                latest_version="",
                release_notes="",
                download_url="",
                status=UpdateStatus.NO_INTERNET
            )
        except Exception as e:
            self._last_check_error = str(e)
            return UpdateInfo(
                current_version=self.current_version,
                latest_version="",
                release_notes="",
                download_url="",
                status=UpdateStatus.CHECK_FAILED
            )

    def download_and_apply_update(self, update_info: UpdateInfo) -> UpdateStatus:
        """
        Download and apply an update.
        
        This will:
        1. Download the new version to a temp directory
        2. Backup current game files (not save data)
        3. Replace game files with new version
        4. Preserve the save directory completely
        
        Args:
            update_info: The update information from check_for_updates
            
        Returns:
            UpdateStatus indicating success or failure
        """
        if not update_info.download_url:
            return UpdateStatus.UPDATE_FAILED

        try:
            # Create temp directory for download
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zip_path = temp_path / "update.zip"
                extract_path = temp_path / "extracted"
                
                # Download the update
                request = urllib.request.Request(
                    update_info.download_url,
                    headers={'User-Agent': f'CheeseTheDuck/{self.current_version}'}
                )
                
                with urllib.request.urlopen(request, timeout=60) as response:
                    with open(zip_path, 'wb') as f:
                        f.write(response.read())
                
                # Extract the zip
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Find the actual game directory in the extracted files
                # GitHub zips have a folder like "repo-name-version/"
                extracted_contents = list(extract_path.iterdir())
                if len(extracted_contents) == 1 and extracted_contents[0].is_dir():
                    source_dir = extracted_contents[0]
                else:
                    source_dir = extract_path
                
                # Create backup of current game (exclude save dir, pycache, etc.)
                backup_dir = temp_path / "backup"
                backup_dir.mkdir()
                
                # Directories/files to exclude from update
                exclude_patterns = {
                    '__pycache__', '.git', '.venv', 'venv', 
                    'data', 'logs', 'models', '.pyc'
                }
                
                # Copy new files to game directory
                for item in source_dir.iterdir():
                    dest = GAME_DIR / item.name
                    
                    # Skip excluded items
                    if any(exc in str(item) for exc in exclude_patterns):
                        continue
                    
                    # Backup existing file/folder
                    if dest.exists():
                        backup_dest = backup_dir / item.name
                        if dest.is_dir():
                            shutil.copytree(dest, backup_dest)
                        else:
                            shutil.copy2(dest, backup_dest)
                    
                    # Copy new version
                    if item.is_dir():
                        if dest.exists():
                            # Try to remove existing directory, handling locked files
                            try:
                                shutil.rmtree(dest, ignore_errors=False)
                            except OSError:
                                # If rmtree fails, try removing with ignore_errors
                                # then manually remove any remaining files
                                shutil.rmtree(dest, ignore_errors=True)
                                if dest.exists():
                                    # Force remove any remaining items
                                    for root, dirs, files in os.walk(dest, topdown=False):
                                        for name in files:
                                            try:
                                                os.remove(os.path.join(root, name))
                                            except OSError:
                                                pass
                                        for name in dirs:
                                            try:
                                                os.rmdir(os.path.join(root, name))
                                            except OSError:
                                                pass
                                    try:
                                        os.rmdir(dest)
                                    except OSError:
                                        pass
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                
                # Save data is preserved automatically since it's in ~/.cheese_the_duck
                # and we never touch that directory
                
                return UpdateStatus.UPDATE_COMPLETE

        except Exception as e:
            self._last_check_error = str(e)
            return UpdateStatus.UPDATE_FAILED

    def download_and_install_deb(self, update_info: UpdateInfo) -> UpdateStatus:
        """
        Download and install a .deb package update for system installs.
        
        This builds the .deb locally from source and installs it using pkexec
        for a graphical sudo prompt.
        
        Args:
            update_info: The update information from check_for_updates
            
        Returns:
            UpdateStatus indicating success or failure
        """
        if not HAS_URLLIB:
            self._last_check_error = "urllib not available"
            return UpdateStatus.UPDATE_FAILED
        
        try:
            # Create temp directory for build
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                version = update_info.latest_version.lstrip('v')
                deb_name = f"cheese-the-duck_{version}-1_all.deb"
                deb_path = temp_path / deb_name
                
                # Download source code
                zip_url = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/archive/refs/tags/{update_info.latest_version}.zip"
                zip_path = temp_path / "source.zip"
                
                request = urllib.request.Request(
                    zip_url,
                    headers={'User-Agent': f'CheeseTheDuck/{self.current_version}'}
                )
                
                with urllib.request.urlopen(request, timeout=60) as response:
                    with open(zip_path, 'wb') as f:
                        f.write(response.read())
                
                # Extract source
                extract_path = temp_path / "extracted"
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Find extracted directory
                extracted_contents = list(extract_path.iterdir())
                if len(extracted_contents) == 1 and extracted_contents[0].is_dir():
                    source_dir = extracted_contents[0]
                else:
                    source_dir = extract_path
                
                # Build .deb package structure
                pkg_dir = temp_path / f"cheese-the-duck_{version}-1_all"
                
                # Create directory structure
                (pkg_dir / "DEBIAN").mkdir(parents=True)
                (pkg_dir / "opt" / "cheese-the-duck").mkdir(parents=True)
                (pkg_dir / "usr" / "bin").mkdir(parents=True)
                (pkg_dir / "usr" / "share" / "applications").mkdir(parents=True)
                (pkg_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True)
                
                # Copy game files
                for item in source_dir.iterdir():
                    if item.name in ['__pycache__', '.git', '.venv', 'venv', 'data', 'logs']:
                        continue
                    dest = pkg_dir / "opt" / "cheese-the-duck" / item.name
                    if item.is_dir():
                        shutil.copytree(item, dest, dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, dest)
                
                # Create launcher script
                launcher = pkg_dir / "usr" / "bin" / "cheese-the-duck"
                launcher.write_text('''#!/bin/bash
# Cheese the Duck Launcher
GAME_DIR="/opt/cheese-the-duck"
VENV_DIR="$HOME/.local/share/cheese-the-duck/venv"

# Game requires 116x35 terminal for best experience
GAME_COLS=120
GAME_ROWS=45

if [ -t 1 ]; then
    printf '\\033[8;%d;%dt' "$GAME_ROWS" "$GAME_COLS"
    sleep 0.1
fi

cd "$GAME_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "Setting up Cheese the Duck (first run)..."
    mkdir -p "$HOME/.local/share/cheese-the-duck"
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -q --upgrade pip
    "$VENV_DIR/bin/pip" install -q -r requirements.txt
    echo "Setup complete! Starting game..."
fi

exec "$VENV_DIR/bin/python" main.py "$@"
''')
                launcher.chmod(0o755)
                
                # Create desktop launcher (spawns terminal with proper size)
                desktop_launcher = pkg_dir / "usr" / "bin" / "cheese-the-duck-desktop"
                desktop_launcher.write_text('''#!/bin/bash
# Cheese the Duck Desktop Launcher
# Launches the game in a properly-sized terminal window
# Reads user's preferred terminal from settings if configured

GAME_COLS=120
GAME_ROWS=45
SETTINGS_FILE="$HOME/.cheese_the_duck/settings.json"

# Read preferred terminal from settings
get_preferred_terminal() {
    if [ -f "$SETTINGS_FILE" ]; then
        if command -v python3 &>/dev/null; then
            PREF=$(python3 -c "import json; d=json.load(open('$SETTINGS_FILE')); print(d.get('system',{}).get('preferred_terminal','auto'))" 2>/dev/null)
            echo "$PREF"
            return
        fi
    fi
    echo "auto"
}

# Launch with specific terminal
launch_with_terminal() {
    local term="$1"
    shift
    
    case "$term" in
        gnome-terminal)
            gnome-terminal --geometry="${GAME_COLS}x${GAME_ROWS}" -- cheese-the-duck "$@" 2>/dev/null && return 0
            gnome-terminal -- cheese-the-duck "$@" && return 0
            ;;
        konsole)
            konsole -e cheese-the-duck "$@" && return 0
            ;;
        xfce4-terminal)
            xfce4-terminal --geometry="${GAME_COLS}x${GAME_ROWS}" -e "cheese-the-duck" && return 0
            ;;
        xterm)
            TERM=xterm-256color xterm -geometry "${GAME_COLS}x${GAME_ROWS}" -fa 'Monospace' -fs 11 -e cheese-the-duck "$@" && return 0
            ;;
        tilix)
            tilix -e "cheese-the-duck" && return 0
            ;;
        terminator)
            terminator --geometry="${GAME_COLS}x${GAME_ROWS}" -e "cheese-the-duck" && return 0
            ;;
        mate-terminal)
            mate-terminal --geometry="${GAME_COLS}x${GAME_ROWS}" -e "cheese-the-duck" && return 0
            ;;
        lxterminal)
            lxterminal --geometry="${GAME_COLS}x${GAME_ROWS}" -e "cheese-the-duck" && return 0
            ;;
        alacritty)
            alacritty -o "window.dimensions.columns=${GAME_COLS}" -o "window.dimensions.lines=${GAME_ROWS}" -e cheese-the-duck "$@" && return 0
            ;;
        kitty)
            kitty -o initial_window_width=${GAME_COLS}c -o initial_window_height=${GAME_ROWS}c cheese-the-duck "$@" && return 0
            ;;
        wezterm)
            wezterm start --width ${GAME_COLS} --height ${GAME_ROWS} -- cheese-the-duck "$@" && return 0
            ;;
        foot)
            foot -W ${GAME_COLS}x${GAME_ROWS} cheese-the-duck "$@" && return 0
            ;;
        x-terminal-emulator)
            x-terminal-emulator -e cheese-the-duck "$@" && return 0
            ;;
    esac
    return 1
}

# Auto-detect and use first available terminal
auto_detect_terminal() {
    for term in gnome-terminal konsole xfce4-terminal xterm tilix terminator mate-terminal lxterminal alacritty kitty wezterm foot x-terminal-emulator; do
        if command -v "$term" &>/dev/null; then
            launch_with_terminal "$term" "$@" && return 0
        fi
    done
    cheese-the-duck "$@"
}

# Main
PREFERRED=$(get_preferred_terminal)

if [ "$PREFERRED" = "auto" ] || [ -z "$PREFERRED" ]; then
    auto_detect_terminal "$@"
else
    if command -v "$PREFERRED" &>/dev/null; then
        launch_with_terminal "$PREFERRED" "$@" || auto_detect_terminal "$@"
    else
        auto_detect_terminal "$@"
    fi
fi
''')
                desktop_launcher.chmod(0o755)
                
                # Create desktop entry (uses desktop launcher, Terminal=false)
                desktop_entry = pkg_dir / "usr" / "share" / "applications" / "cheese-the-duck.desktop"
                desktop_entry.write_text(f'''[Desktop Entry]
Version={version}
Type=Application
Name=Cheese the Duck
Comment=A terminal-based virtual pet game
Exec=cheese-the-duck-desktop
Icon=cheese-the-duck
Terminal=false
Categories=Game;Simulation;
Keywords=duck;pet;virtual;game;terminal;
StartupNotify=false
''')
                
                # Copy icon if available
                icon_src = source_dir / "assets" / "cheese.ico"
                if icon_src.exists():
                    # Try to convert with ImageMagick
                    icon_dest = pkg_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "cheese-the-duck.png"
                    try:
                        subprocess.run(
                            ["convert", f"{icon_src}[8]", "-resize", "256x256", str(icon_dest)],
                            capture_output=True, timeout=30
                        )
                    except Exception:
                        pass  # Icon is optional
                
                # Create DEBIAN/control
                control = pkg_dir / "DEBIAN" / "control"
                control.write_text(f'''Package: cheese-the-duck
Version: {version}-1
Section: games
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-venv, python3-pip, libsdl2-2.0-0, libsdl2-mixer-2.0-0
Recommends: imagemagick
Maintainer: Cheese the Duck Team <cheese@example.com>
Description: A terminal-based virtual pet duck game
 Cheese the Duck is an interactive terminal game where you care for
 your virtual pet duck named Cheese.
Homepage: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}
''')
                
                # Build .deb
                result = subprocess.run(
                    ["dpkg-deb", "--build", "--root-owner-group", str(pkg_dir), str(deb_path)],
                    capture_output=True, timeout=60
                )
                
                if result.returncode != 0:
                    self._last_check_error = f"dpkg-deb failed: {result.stderr.decode()[:100]}"
                    return UpdateStatus.UPDATE_FAILED
                
                if not deb_path.exists():
                    self._last_check_error = "Failed to build .deb package"
                    return UpdateStatus.UPDATE_FAILED
                
                # Install using pkexec (graphical sudo prompt)
                # Try pkexec first (graphical), fall back to sudo
                install_cmd = None
                
                # Check for pkexec (graphical environments)
                if shutil.which("pkexec"):
                    install_cmd = ["pkexec", "apt", "install", "-y", str(deb_path)]
                # Fall back to sudo in terminal
                elif shutil.which("sudo"):
                    install_cmd = ["sudo", "apt", "install", "-y", str(deb_path)]
                else:
                    self._last_check_error = "No pkexec or sudo available"
                    return UpdateStatus.UPDATE_FAILED
                
                result = subprocess.run(install_cmd, capture_output=True, timeout=120)
                
                if result.returncode != 0:
                    stderr = result.stderr.decode()[:200]
                    # Check if user cancelled auth dialog
                    if "dismissed" in stderr.lower() or "cancelled" in stderr.lower():
                        self._last_check_error = "Update cancelled by user"
                    else:
                        self._last_check_error = f"Install failed: {stderr}"
                    return UpdateStatus.UPDATE_FAILED
                
                return UpdateStatus.UPDATE_COMPLETE

        except subprocess.TimeoutExpired:
            self._last_check_error = "Update timed out"
            return UpdateStatus.UPDATE_FAILED
        except Exception as e:
            self._last_check_error = str(e)
            return UpdateStatus.UPDATE_FAILED

    def get_status_message(self, status: UpdateStatus) -> str:
        """Get a user-friendly message for an update status."""
        messages = {
            UpdateStatus.UP_TO_DATE: f"Game is up to date (v{self.current_version})",
            UpdateStatus.UPDATE_AVAILABLE: "New update available!",
            UpdateStatus.CHECK_FAILED: "Could not check for updates",
            UpdateStatus.NO_INTERNET: "No internet connection",
            UpdateStatus.UPDATING: "Downloading update...",
            UpdateStatus.UPDATE_COMPLETE: "Update complete! Restart to apply.",
            UpdateStatus.UPDATE_FAILED: "Update failed",
        }
        return messages.get(status, "Unknown status")

    def get_last_error(self) -> Optional[str]:
        """Get the last error message if any."""
        return self._last_check_error


# Global updater instance
game_updater = GameUpdater()
