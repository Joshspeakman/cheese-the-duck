#!/usr/bin/env python3
"""
Build a standalone Windows installer for Cheese the Duck.

This creates a fully offline installer that includes:
- Python runtime (embedded)
- All game files and dependencies
- Optional AI model
- Desktop/Start Menu shortcuts

Output: CheeseTheDuck-Setup.exe

Requirements (on Windows):
  pip install pyinstaller

For creating the final installer, Inno Setup is used (free):
  https://jrsoftware.org/isdl.php

Usage:
  python build_windows_installer.py          # Build without AI model
  python build_windows_installer.py --model  # Include AI model (~700MB)
"""
import os
import sys
import shutil
import subprocess
import glob
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
BUILD_DIR = SCRIPT_DIR / "build"
DIST_DIR = SCRIPT_DIR / "dist"
INSTALLER_DIR = SCRIPT_DIR / "installer_build"

# Game version (read from updater.py)
def get_version():
    """Extract version from core/updater.py"""
    updater_path = SCRIPT_DIR / "core" / "updater.py"
    if updater_path.exists():
        with open(updater_path, 'r') as f:
            for line in f:
                if line.startswith('GAME_VERSION'):
                    # Extract: GAME_VERSION = "1.4.1"
                    return line.split('"')[1]
    return "1.0.0"

VERSION = get_version()

# Files and directories to include
DATA_DIRS = [
    "audio",
    "core",
    "dialogue", 
    "duck",
    "ui",
    "world",
    "data",
    "assets",
]

DATA_FILES = [
    "config.py",
    "game_logger.py",
    "download_model.py",
    "cheese.ico",
    "*.wav",
    "*.mp3",
]

EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    ".git",
    ".venv",
    "build",
    "dist",
    "installer_build",
    "*.deb",
    "logs",
    ".fuse_hidden*",
]


def print_header(text):
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_requirements():
    """Check that we're on Windows and have required tools."""
    if sys.platform != 'win32':
        print("⚠️  This script is designed to run on Windows.")
        print("   You can still generate the Inno Setup script,")
        print("   but the full build requires Windows.")
        return False
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    return True


def clean_build():
    """Clean previous build artifacts."""
    print_header("Cleaning previous builds")
    
    for dir_path in [BUILD_DIR, DIST_DIR, INSTALLER_DIR]:
        if dir_path.exists():
            print(f"  Removing {dir_path.name}/...")
            shutil.rmtree(dir_path)
    
    print("✓ Clean complete")


def build_with_pyinstaller(include_model=False):
    """Build standalone executable with PyInstaller."""
    print_header("Building with PyInstaller")
    
    # Prepare data arguments
    add_data = []
    
    for data_dir in DATA_DIRS:
        src_path = SCRIPT_DIR / data_dir
        if src_path.exists():
            add_data.extend(["--add-data", f"{src_path};{data_dir}"])
            print(f"  + {data_dir}/")
    
    # Add individual files
    for pattern in DATA_FILES:
        if "*" in pattern:
            for f in glob.glob(str(SCRIPT_DIR / pattern)):
                if os.path.isfile(f):
                    add_data.extend(["--add-data", f"{f};."])
                    print(f"  + {os.path.basename(f)}")
        else:
            src_path = SCRIPT_DIR / pattern
            if src_path.exists():
                add_data.extend(["--add-data", f"{src_path};."])
                print(f"  + {pattern}")
    
    # Add models directory if including AI model
    if include_model:
        models_dir = SCRIPT_DIR / "models"
        if models_dir.exists() and any(models_dir.glob("*.gguf")):
            add_data.extend(["--add-data", f"{models_dir};models"])
            print("  + models/ (AI model)")
        else:
            print("  ⚠️  No AI model found in models/ - skipping")
    
    # Icon
    icon_path = SCRIPT_DIR / "cheese.ico"
    icon_opt = ["--icon", str(icon_path)] if icon_path.exists() else []
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "CheeseTheDuck",
        "--onedir",
        "--console",
        "--noconfirm",
        "--clean",
        # Hidden imports that PyInstaller might miss
        "--hidden-import", "blessed",
        "--hidden-import", "pygame",
        "--hidden-import", "llama_cpp",
    ] + icon_opt + add_data + [
        str(SCRIPT_DIR / "main.py")
    ]
    
    print()
    print("Running PyInstaller (this may take a few minutes)...")
    subprocess.check_call(cmd, cwd=str(SCRIPT_DIR))
    
    output_dir = DIST_DIR / "CheeseTheDuck"
    if output_dir.exists():
        print(f"✓ Build complete: {output_dir}")
        return output_dir
    else:
        print("✗ Build failed!")
        return None


def create_inno_setup_script(include_model=False):
    """Generate Inno Setup script for creating Windows installer."""
    print_header("Creating Inno Setup Script")
    
    installer_dir = INSTALLER_DIR
    installer_dir.mkdir(parents=True, exist_ok=True)
    
    iss_content = f'''; Inno Setup Script for Cheese the Duck
; Generated automatically by build_windows_installer.py

#define MyAppName "Cheese the Duck"
#define MyAppVersion "{VERSION}"
#define MyAppPublisher "Cheese the Duck Team"
#define MyAppURL "https://github.com/Joshspeakman/cheese-the-duck"
#define MyAppExeName "CheeseTheDuck.exe"

[Setup]
AppId={{{{B8A3E5C2-9F1D-4E2A-B3C7-D8E9F0A1B2C3}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\CheeseTheDuck
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile={SCRIPT_DIR}\\LICENSE
OutputDir={INSTALLER_DIR}
OutputBaseFilename=CheeseTheDuck-{VERSION}-Setup
SetupIconFile={SCRIPT_DIR}\\cheese.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "{DIST_DIR}\\CheeseTheDuck\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent shellexec

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
'''
    
    iss_path = installer_dir / "CheeseTheDuck.iss"
    with open(iss_path, 'w') as f:
        f.write(iss_content)
    
    print(f"✓ Inno Setup script created: {iss_path}")
    return iss_path


def build_installer_with_inno(iss_path):
    """Compile the installer using Inno Setup."""
    print_header("Building Installer with Inno Setup")
    
    # Common Inno Setup installation paths
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]
    
    iscc_path = None
    for path in inno_paths:
        if os.path.exists(path):
            iscc_path = path
            break
    
    if not iscc_path:
        print("⚠️  Inno Setup not found!")
        print()
        print("To create the final installer:")
        print("  1. Download Inno Setup from: https://jrsoftware.org/isdl.php")
        print("  2. Install it (free)")
        print("  3. Open the generated .iss file:")
        print(f"     {iss_path}")
        print("  4. Click Build → Compile")
        print()
        print("Or run from command line after installing Inno Setup:")
        print(f'  "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe" "{iss_path}"')
        return None
    
    print(f"Found Inno Setup: {iscc_path}")
    print("Compiling installer...")
    
    subprocess.check_call([iscc_path, str(iss_path)])
    
    # Find output
    output_files = list(INSTALLER_DIR.glob("*.exe"))
    if output_files:
        output = output_files[0]
        print(f"✓ Installer created: {output}")
        return output
    
    return None


def create_portable_zip():
    """Create a portable ZIP distribution (no installer needed)."""
    print_header("Creating Portable ZIP")
    
    dist_path = DIST_DIR / "CheeseTheDuck"
    if not dist_path.exists():
        print("✗ Build directory not found!")
        return None
    
    zip_name = f"CheeseTheDuck-{VERSION}-Windows-Portable"
    zip_path = DIST_DIR / zip_name
    
    shutil.make_archive(str(zip_path), 'zip', str(DIST_DIR), "CheeseTheDuck")
    
    print(f"✓ Portable ZIP created: {zip_path}.zip")
    return f"{zip_path}.zip"


def main():
    parser = argparse.ArgumentParser(description="Build Windows installer for Cheese the Duck")
    parser.add_argument("--model", action="store_true", help="Include AI model in build (~700MB)")
    parser.add_argument("--skip-pyinstaller", action="store_true", help="Skip PyInstaller build (use existing)")
    parser.add_argument("--portable-only", action="store_true", help="Only create portable ZIP, no installer")
    args = parser.parse_args()
    
    print()
    print("🦆 Cheese the Duck - Windows Installer Builder")
    print(f"   Version: {VERSION}")
    print()
    
    is_windows = check_requirements()
    
    if not args.skip_pyinstaller:
        clean_build()
        
        if is_windows:
            dist_path = build_with_pyinstaller(include_model=args.model)
            if not dist_path:
                print("Build failed!")
                return 1
        else:
            print()
            print("⚠️  Not running on Windows - can only generate scripts.")
            print("   Run this script on Windows to create the full build.")
            print()
    
    # Create portable ZIP
    zip_path = create_portable_zip()
    
    if not args.portable_only:
        # Create Inno Setup script
        iss_path = create_inno_setup_script(include_model=args.model)
        
        # Try to build installer
        if is_windows:
            installer_path = build_installer_with_inno(iss_path)
    
    print()
    print_header("Build Complete!")
    print()
    print("Distribution files:")
    print(f"  📁 Build folder: {DIST_DIR / 'CheeseTheDuck'}")
    if zip_path:
        print(f"  📦 Portable ZIP: {zip_path}")
    print(f"  📜 Inno Script:  {INSTALLER_DIR / 'CheeseTheDuck.iss'}")
    print()
    
    if is_windows:
        installer_files = list(INSTALLER_DIR.glob("*.exe"))
        if installer_files:
            print(f"  🎉 INSTALLER:    {installer_files[0]}")
    else:
        print("To create the installer:")
        print("  1. Copy this project to a Windows machine")
        print("  2. Run: python build_windows_installer.py")
        print("  3. Install Inno Setup if prompted")
    
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
