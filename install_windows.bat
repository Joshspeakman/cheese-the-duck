@echo off
REM ============================================================
REM Cheese the Duck - Windows Installer
REM ============================================================
REM This script installs Cheese the Duck on Windows systems.
REM 
REM Usage:
REM   Double-click install_windows.bat
REM   Or run from Command Prompt: install_windows.bat
REM ============================================================

setlocal enabledelayedexpansion

echo ╔════════════════════════════════════════════════════════════╗
echo ║          🦆 Cheese the Duck - Windows Installer             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Get script directory
set "SCRIPT_DIR=%~dp0"
set "INSTALL_DIR=%LOCALAPPDATA%\CheeseTheDuck"

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   X Error: Python not found!
    echo.
    echo   Please install Python 3.8+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo   Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
echo   √ Python %PYTHON_VERSION% found

REM Create install directory
echo.
echo Creating installation directory...
if exist "%INSTALL_DIR%" rmdir /s /q "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%"

REM Copy files
echo Copying game files...
xcopy "%SCRIPT_DIR%*" "%INSTALL_DIR%\" /e /i /q /y >nul

REM Remove installer scripts from installed location
del /q "%INSTALL_DIR%\install_windows.bat" 2>nul
del /q "%INSTALL_DIR%\install_linux.sh" 2>nul
del /q "%INSTALL_DIR%\build_installer.py" 2>nul

REM Create virtual environment
echo.
echo Setting up Python environment...
cd /d "%INSTALL_DIR%"

if not exist ".venv" (
    python -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
echo   √ Dependencies installed

REM Download AI model (optional)
echo.
set /p download_model="Download AI model for conversations? (~700MB) [y/N]: "
if /i "%download_model%"=="y" (
    echo Downloading AI model...
    python download_model.py
)

REM Create launcher batch file
echo.
echo Creating launcher...
(
echo @echo off
echo cd /d "%INSTALL_DIR%"
echo if exist ".venv\Scripts\python.exe" ^(
echo     .venv\Scripts\python.exe main.py %%*
echo ^) else ^(
echo     python main.py %%*
echo ^)
) > "%INSTALL_DIR%\CheeseTheDuck.bat"

REM Create desktop shortcut
echo Creating shortcuts...
set "SHORTCUT=%USERPROFILE%\Desktop\Cheese the Duck.lnk"

REM Use PowerShell to create shortcut
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%INSTALL_DIR%\CheeseTheDuck.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'A terminal-based virtual pet game'; $s.Save()"

if exist "%SHORTCUT%" (
    echo   √ Desktop shortcut created
) else (
    echo   ! Could not create desktop shortcut
)

REM Create Start Menu shortcut
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Cheese the Duck.lnk"
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%START_MENU%'); $s.TargetPath = '%INSTALL_DIR%\CheeseTheDuck.bat'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Description = 'A terminal-based virtual pet game'; $s.Save()"

if exist "%START_MENU%" (
    echo   √ Start Menu shortcut created
) else (
    echo   ! Could not create Start Menu shortcut
)

REM Done
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                  √ Installation Complete!                   ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo To play Cheese the Duck:
echo.
echo   Option 1: Double-click "Cheese the Duck" on your Desktop
echo.
echo   Option 2: Find "Cheese the Duck" in the Start Menu
echo.
echo   Option 3: Run directly:
echo             %INSTALL_DIR%\CheeseTheDuck.bat
echo.
echo Installed to: %INSTALL_DIR%
echo.
echo To uninstall:
echo   1. Delete the desktop shortcut
echo   2. Delete: %INSTALL_DIR%
echo.
pause
