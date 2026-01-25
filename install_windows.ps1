# ============================================================
# Cheese the Duck - Windows Installer (PowerShell)
# ============================================================
# Professional installer with location selection, auto-download
# of Python if needed, and proper shortcuts with icons.
#
# Usage: Right-click → Run with PowerShell
#        Or: powershell -ExecutionPolicy Bypass -File install_windows.ps1
# ============================================================

param(
    [string]$InstallPath = "",
    [switch]$Uninstall = $false,
    [switch]$Silent = $false
)

$ErrorActionPreference = "Stop"

# Configuration
$AppName = "Cheese the Duck"
$AppExeName = "CheeseTheDuck"
$DefaultInstallDir = "$env:LOCALAPPDATA\CheeseTheDuck"
$PythonMinVersion = [version]"3.8.0"
$PythonDownloadUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$RepoUrl = "https://github.com/Joshspeakman/cheese-the-duck/archive/refs/heads/main.zip"
$RepoName = "cheese-the-duck-main"

# Detect run mode (local from cloned repo, or remote download)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($ScriptDir) -or -not (Test-Path "$ScriptDir\main.py")) {
    $RunMode = "remote"
} else {
    $RunMode = "local"
}

# Console colors
function Write-Header {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║           🦆 Cheese the Duck - Windows Installer            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Message)
    Write-Host "  → " -NoNewline -ForegroundColor Yellow
    Write-Host $Message
}

function Write-Success {
    param([string]$Message)
    Write-Host "  ✓ " -NoNewline -ForegroundColor Green
    Write-Host $Message
}

function Write-Error {
    param([string]$Message)
    Write-Host "  ✗ " -NoNewline -ForegroundColor Red
    Write-Host $Message
}

function Write-Info {
    param([string]$Message)
    Write-Host "  ℹ " -NoNewline -ForegroundColor Blue
    Write-Host $Message
}

# Check if running as admin (for Python install if needed)
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check Python installation
function Get-PythonInfo {
    $pythonPaths = @(
        "python",
        "python3",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe",
        "$env:ProgramFiles\Python310\python.exe"
    )
    
    foreach ($pythonPath in $pythonPaths) {
        try {
            $versionOutput = & $pythonPath --version 2>&1
            if ($versionOutput -match "Python (\d+\.\d+\.\d+)") {
                $version = [version]$Matches[1]
                if ($version -ge $PythonMinVersion) {
                    return @{
                        Path = $pythonPath
                        Version = $version
                        Found = $true
                    }
                }
            }
        } catch {
            continue
        }
    }
    
    return @{ Found = $false }
}

# Download and install Python
function Install-Python {
    Write-Step "Python not found. Downloading Python 3.12..."
    
    $tempInstaller = "$env:TEMP\python-installer.exe"
    
    try {
        # Download Python installer
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $PythonDownloadUrl -OutFile $tempInstaller -UseBasicParsing
        Write-Success "Downloaded Python installer"
        
        # Install Python silently
        Write-Step "Installing Python (this may take a minute)..."
        $installArgs = "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_doc=0"
        Start-Process -FilePath $tempInstaller -ArgumentList $installArgs -Wait -NoNewWindow
        
        # Refresh environment
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        # Verify installation
        Start-Sleep -Seconds 2
        $pythonInfo = Get-PythonInfo
        if ($pythonInfo.Found) {
            Write-Success "Python $($pythonInfo.Version) installed successfully"
            return $pythonInfo
        } else {
            throw "Python installation verification failed"
        }
    } finally {
        if (Test-Path $tempInstaller) {
            Remove-Item $tempInstaller -Force
        }
    }
}

# Create shortcuts with icon
function New-Shortcut {
    param(
        [string]$ShortcutPath,
        [string]$TargetPath,
        [string]$WorkingDirectory,
        [string]$IconPath,
        [string]$Description
    )
    
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $WorkingDirectory
    $Shortcut.Description = $Description
    if ($IconPath -and (Test-Path $IconPath)) {
        $Shortcut.IconLocation = "$IconPath,0"
    }
    $Shortcut.Save()
}

# Select install location
function Select-InstallLocation {
    if (-not $Silent) {
        Write-Host ""
        Write-Host "Select installation location:" -ForegroundColor Yellow
        Write-Host "  [1] Default: $DefaultInstallDir"
        Write-Host "  [2] Custom location"
        Write-Host ""
        
        $choice = Read-Host "Enter choice (1 or 2)"
        
        if ($choice -eq "2") {
            Add-Type -AssemblyName System.Windows.Forms
            $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
            $folderBrowser.Description = "Select installation folder for Cheese the Duck"
            $folderBrowser.RootFolder = "MyComputer"
            $folderBrowser.ShowNewFolderButton = $true
            
            if ($folderBrowser.ShowDialog() -eq "OK") {
                return Join-Path $folderBrowser.SelectedPath "CheeseTheDuck"
            }
        }
    }
    
    return $DefaultInstallDir
}

# Main uninstall function
function Uninstall-CheeseTheDuck {
    Write-Header
    Write-Host "Uninstalling $AppName..." -ForegroundColor Yellow
    Write-Host ""
    
    # Read install location from registry
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\CheeseTheDuck"
    $installDir = $DefaultInstallDir
    
    if (Test-Path $regPath) {
        $installDir = (Get-ItemProperty -Path $regPath -Name "InstallLocation" -ErrorAction SilentlyContinue).InstallLocation
        if (-not $installDir) { $installDir = $DefaultInstallDir }
    }
    
    # Remove shortcuts
    Write-Step "Removing shortcuts..."
    $desktopShortcut = "$env:USERPROFILE\Desktop\Cheese the Duck.lnk"
    $startMenuFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Cheese the Duck"
    
    if (Test-Path $desktopShortcut) { Remove-Item $desktopShortcut -Force }
    if (Test-Path $startMenuFolder) { Remove-Item $startMenuFolder -Recurse -Force }
    Write-Success "Shortcuts removed"
    
    # Remove installation directory
    Write-Step "Removing program files..."
    if (Test-Path $installDir) {
        Remove-Item $installDir -Recurse -Force
        Write-Success "Program files removed"
    }
    
    # Remove registry entry
    Write-Step "Removing registry entries..."
    if (Test-Path $regPath) {
        Remove-Item $regPath -Force
        Write-Success "Registry entries removed"
    }
    
    Write-Host ""
    Write-Success "$AppName has been uninstalled successfully!"
    Write-Host ""
    
    if (-not $Silent) {
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

# Main install function
function Install-CheeseTheDuck {
    Write-Header
    
    # Select install location
    if ($InstallPath) {
        $installDir = $InstallPath
    } else {
        $installDir = Select-InstallLocation
    }
    
    Write-Info "Installing to: $installDir"
    Write-Host ""
    
    # Check Python
    Write-Step "Checking Python installation..."
    $pythonInfo = Get-PythonInfo
    
    if (-not $pythonInfo.Found) {
        if (-not $Silent) {
            Write-Host ""
            $downloadPython = Read-Host "Python 3.8+ not found. Download and install? (Y/n)"
            if ($downloadPython -ne "n" -and $downloadPython -ne "N") {
                $pythonInfo = Install-Python
            } else {
                Write-Error "Python is required. Please install Python 3.8+ from https://python.org"
                return
            }
        } else {
            $pythonInfo = Install-Python
        }
    } else {
        Write-Success "Python $($pythonInfo.Version) found"
    }
    
    $pythonPath = $pythonInfo.Path
    
    # Create installation directory
    Write-Step "Creating installation directory..."
    if (Test-Path $installDir) {
        Remove-Item $installDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Success "Directory created"
    
    # Get game files
    if ($RunMode -eq "remote") {
        Write-Step "Downloading game files from GitHub..."
        $tempZip = "$env:TEMP\cheese-the-duck.zip"
        $tempExtract = "$env:TEMP\cheese-the-duck-extract"
        
        try {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            Invoke-WebRequest -Uri $RepoUrl -OutFile $tempZip -UseBasicParsing
            
            # Extract
            if (Test-Path $tempExtract) { Remove-Item $tempExtract -Recurse -Force }
            Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force
            
            # Move contents from extracted folder to install dir
            $extractedDir = "$tempExtract\$RepoName"
            Get-ChildItem -Path $extractedDir | ForEach-Object {
                if ($_.Name -notin @(".venv", ".git", "__pycache__", "build", "dist", "StupidDuckCS", "debian")) {
                    if ($_.PSIsContainer) {
                        Copy-Item $_.FullName -Destination $installDir -Recurse -Force
                    } else {
                        Copy-Item $_.FullName -Destination $installDir -Force
                    }
                }
            }
            Write-Success "Files downloaded"
        } finally {
            if (Test-Path $tempZip) { Remove-Item $tempZip -Force }
            if (Test-Path $tempExtract) { Remove-Item $tempExtract -Recurse -Force }
        }
    } else {
        Write-Step "Copying game files..."
        $excludeFiles = @("install_windows.ps1", "install_windows.bat", "install_linux.sh", ".venv", ".git", "__pycache__", "*.pyc", "build", "dist", "StupidDuckCS", "debian")
        
        Get-ChildItem -Path $ScriptDir -Exclude $excludeFiles | ForEach-Object {
            if ($_.PSIsContainer) {
                if ($_.Name -notin @(".venv", ".git", "__pycache__", "build", "dist", "StupidDuckCS", "debian")) {
                    Copy-Item $_.FullName -Destination $installDir -Recurse -Force
                }
            } else {
                Copy-Item $_.FullName -Destination $installDir -Force
            }
        }
        Write-Success "Files copied"
    }
    
    # Create virtual environment
    Write-Step "Setting up Python environment..."
    Push-Location $installDir
    try {
        & $pythonPath -m venv .venv 2>&1 | Out-Null
        
        # Activate and install requirements
        $pipPath = Join-Path $installDir ".venv\Scripts\pip.exe"
        & $pipPath install --upgrade pip -q 2>&1 | Out-Null
        & $pipPath install -r requirements.txt -q 2>&1 | Out-Null
        Write-Success "Dependencies installed"
    } finally {
        Pop-Location
    }
    
    # Download AI model
    Write-Step "Downloading AI model (this may take a while)..."
    Push-Location $installDir
    try {
        $venvPython = Join-Path $installDir ".venv\Scripts\python.exe"
        & $venvPython download_model.py --auto
    } finally {
        Pop-Location
    }
    
    # Create launcher batch file
    Write-Step "Creating launcher..."
    $launcherContent = @"
@echo off
cd /d "$installDir"
.venv\Scripts\python.exe main.py %*
"@
    Set-Content -Path "$installDir\$AppExeName.bat" -Value $launcherContent
    Write-Success "Launcher created"
    
    # Create shortcuts
    Write-Step "Creating shortcuts..."
    $iconPath = Join-Path $installDir "cheese.ico"
    $launcherPath = Join-Path $installDir "$AppExeName.bat"
    
    # Desktop shortcut
    $desktopShortcut = "$env:USERPROFILE\Desktop\Cheese the Duck.lnk"
    New-Shortcut -ShortcutPath $desktopShortcut -TargetPath $launcherPath -WorkingDirectory $installDir -IconPath $iconPath -Description "A terminal-based virtual pet game"
    Write-Success "Desktop shortcut created"
    
    # Start Menu shortcut
    $startMenuFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Cheese the Duck"
    New-Item -ItemType Directory -Path $startMenuFolder -Force | Out-Null
    New-Shortcut -ShortcutPath "$startMenuFolder\Cheese the Duck.lnk" -TargetPath $launcherPath -WorkingDirectory $installDir -IconPath $iconPath -Description "A terminal-based virtual pet game"
    New-Shortcut -ShortcutPath "$startMenuFolder\Uninstall Cheese the Duck.lnk" -TargetPath "powershell.exe" -WorkingDirectory $installDir -IconPath "" -Description "Uninstall Cheese the Duck"
    # Fix uninstaller shortcut target
    $uninstallShortcut = "$startMenuFolder\Uninstall Cheese the Duck.lnk"
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($uninstallShortcut)
    $Shortcut.TargetPath = "powershell.exe"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$installDir\install_windows.ps1`" -Uninstall"
    $Shortcut.WorkingDirectory = $installDir
    $Shortcut.Save()
    Write-Success "Start Menu shortcuts created"
    
    # Copy installer script for uninstall
    Copy-Item "$ScriptDir\install_windows.ps1" -Destination $installDir -Force
    
    # Add to Windows Programs (Add/Remove Programs)
    Write-Step "Registering with Windows..."
    $regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\CheeseTheDuck"
    New-Item -Path $regPath -Force | Out-Null
    Set-ItemProperty -Path $regPath -Name "DisplayName" -Value $AppName
    Set-ItemProperty -Path $regPath -Name "DisplayIcon" -Value $iconPath
    Set-ItemProperty -Path $regPath -Name "InstallLocation" -Value $installDir
    Set-ItemProperty -Path $regPath -Name "UninstallString" -Value "powershell.exe -ExecutionPolicy Bypass -File `"$installDir\install_windows.ps1`" -Uninstall"
    Set-ItemProperty -Path $regPath -Name "Publisher" -Value "Cheese the Duck Team"
    Set-ItemProperty -Path $regPath -Name "DisplayVersion" -Value "1.2.0"
    Set-ItemProperty -Path $regPath -Name "NoModify" -Value 1 -Type DWord
    Set-ItemProperty -Path $regPath -Name "NoRepair" -Value 1 -Type DWord
    Write-Success "Registered in Add/Remove Programs"
    
    # Done!
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              Installation Complete! 🦆                      ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Info "Installed to: $installDir"
    Write-Info "Desktop shortcut: Cheese the Duck"
    Write-Info "Start Menu: Cheese the Duck"
    Write-Host ""
    Write-Host "To play: Double-click the desktop shortcut or find in Start Menu" -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $Silent) {
        $playNow = Read-Host "Launch the game now? (Y/n)"
        if ($playNow -ne "n" -and $playNow -ne "N") {
            Start-Process -FilePath $launcherPath -WorkingDirectory $installDir
        }
        
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
}

# Main entry point
if ($Uninstall) {
    Uninstall-CheeseTheDuck
} else {
    Install-CheeseTheDuck
}
