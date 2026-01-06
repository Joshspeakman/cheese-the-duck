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
GAME_VERSION = "1.0.0"

# GitHub repository info
GITHUB_OWNER = "Joshspeakman"
GITHUB_REPO = "cheese-the-duck"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"


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

    def _parse_version(self, version_str: str) -> Tuple[int, ...]:
        """Parse version string into tuple for comparison."""
        # Remove 'v' prefix if present
        version_str = version_str.lstrip('v').strip()
        try:
            parts = version_str.split('.')
            return tuple(int(p) for p in parts)
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

    def check_for_updates(self) -> UpdateInfo:
        """
        Check GitHub for the latest release.
        
        Returns:
            UpdateInfo with status and version details
        """
        if not HAS_URLLIB:
            return UpdateInfo(
                current_version=self.current_version,
                latest_version="",
                release_notes="",
                download_url="",
                status=UpdateStatus.CHECK_FAILED
            )

        try:
            # Create request with User-Agent header (required by GitHub API)
            request = urllib.request.Request(
                GITHUB_API_URL,
                headers={
                    'User-Agent': f'CheeseTheDuck/{self.current_version}',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            latest_version = data.get('tag_name', '0.0.0')
            release_notes = data.get('body', 'No release notes available.')
            
            # Find the source code zip download URL
            download_url = ""
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
                release_notes=release_notes[:500],  # Truncate long notes
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
                            shutil.rmtree(dest)
                        shutil.copytree(item, dest)
                    else:
                        shutil.copy2(item, dest)
                
                # Save data is preserved automatically since it's in ~/.cheese_the_duck
                # and we never touch that directory
                
                return UpdateStatus.UPDATE_COMPLETE

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
