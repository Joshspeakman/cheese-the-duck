#!/usr/bin/env python3
"""
Build script for creating Cheese the Duck installers.

Creates standalone executables for Linux and Windows using PyInstaller.
Run: python build_installer.py

Requirements: pip install pyinstaller
"""
import os
import sys
import shutil
import platform
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(SCRIPT_DIR, "dist")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")

# Directories and files to include
DATA_DIRS = [
    "audio",
    "core", 
    "dialogue",
    "duck",
    "ui",
    "world",
    "models",
    "data",
    "assets",
]

DATA_FILES = [
    "config.py",
    "game_logger.py",
    "*.wav",
    "*.mp3",
]


def check_pyinstaller():
    """Ensure PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def build_executable():
    """Build the executable using PyInstaller."""
    system = platform.system().lower()
    
    # Determine output name
    if system == "windows":
        exe_name = "CheeseTheDuck.exe"
        icon_opt = []  # Add --icon=icon.ico if you have one
    else:
        exe_name = "CheeseTheDuck"
        icon_opt = []
    
    print(f"Building for {system}...")
    
    # Build data arguments for PyInstaller
    add_data = []
    separator = ";" if system == "windows" else ":"
    
    for data_dir in DATA_DIRS:
        src_path = os.path.join(SCRIPT_DIR, data_dir)
        if os.path.exists(src_path):
            add_data.extend(["--add-data", f"{src_path}{separator}{data_dir}"])
    
    # Add individual files
    for pattern in DATA_FILES:
        if "*" in pattern:
            import glob
            for f in glob.glob(os.path.join(SCRIPT_DIR, pattern)):
                if os.path.isfile(f):
                    add_data.extend(["--add-data", f"{f}{separator}."])
        else:
            src_path = os.path.join(SCRIPT_DIR, pattern)
            if os.path.exists(src_path):
                add_data.extend(["--add-data", f"{src_path}{separator}."])
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CheeseTheDuck",
        "--onedir",  # Create a directory with all files
        "--console",  # Terminal application
        "--noconfirm",  # Overwrite without asking
        "--clean",  # Clean build
    ] + icon_opt + add_data + [
        os.path.join(SCRIPT_DIR, "main.py")
    ]
    
    print("Running PyInstaller...")
    subprocess.check_call(cmd, cwd=SCRIPT_DIR)
    
    print(f"\n✅ Build complete!")
    print(f"   Output: {os.path.join(DIST_DIR, 'CheeseTheDuck')}")
    
    return os.path.join(DIST_DIR, "CheeseTheDuck")


def create_zip_package(dist_path):
    """Create a distributable zip package."""
    system = platform.system().lower()
    
    if system == "windows":
        archive_name = "CheeseTheDuck-Windows"
    else:
        archive_name = "CheeseTheDuck-Linux"
    
    archive_path = os.path.join(DIST_DIR, archive_name)
    
    print(f"Creating {archive_name}.zip...")
    shutil.make_archive(archive_path, 'zip', DIST_DIR, "CheeseTheDuck")
    
    print(f"✅ Package created: {archive_path}.zip")
    return f"{archive_path}.zip"


def main():
    print("=" * 60)
    print("🦆 Cheese the Duck - Build Installer")
    print("=" * 60)
    print()
    
    # Check dependencies
    check_pyinstaller()
    
    # Clean previous builds
    if os.path.exists(BUILD_DIR):
        print("Cleaning previous build...")
        shutil.rmtree(BUILD_DIR)
    
    # Build executable
    dist_path = build_executable()
    
    # Create zip package
    zip_path = create_zip_package(dist_path)
    
    print()
    print("=" * 60)
    print("🎉 Build Complete!")
    print("=" * 60)
    print()
    print("Distribution files:")
    print(f"  📁 Folder: {dist_path}")
    print(f"  📦 Archive: {zip_path}")
    print()
    print("To run the game:")
    if platform.system().lower() == "windows":
        print("  1. Extract the zip file")
        print("  2. Run CheeseTheDuck.exe")
    else:
        print("  1. Extract the zip file")
        print("  2. Run ./CheeseTheDuck")
    print()


if __name__ == "__main__":
    main()
