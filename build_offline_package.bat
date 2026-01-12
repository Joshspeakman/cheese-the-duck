@echo off
REM ============================================================
REM Cheese the Duck - Offline Installer Builder for Windows
REM ============================================================
REM This creates a fully standalone, offline installer package.
REM No Python installation required on target machine!
REM
REM Prerequisites (on build machine):
REM   - Python 3.10+ installed
REM   - Internet connection (to download embedded Python)
REM
REM Output:
REM   - dist\CheeseTheDuck-Portable\ (run directly)
REM   - dist\CheeseTheDuck-Setup.exe (if Inno Setup installed)
REM
REM Usage:
REM   build_offline_package.bat           (without AI model)
REM   build_offline_package.bat --model   (with AI model ~700MB)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   Cheese the Duck - Offline Package Builder
echo ============================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "BUILD_DIR=%SCRIPT_DIR%build_offline"
set "DIST_DIR=%SCRIPT_DIR%dist"
set "EMBED_DIR=%BUILD_DIR%\python_embed"
set "OUTPUT_DIR=%DIST_DIR%\CheeseTheDuck-Portable"

set "PYTHON_VERSION=3.11.7"
set "PYTHON_EMBED_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-amd64.zip"
set "GET_PIP_URL=https://bootstrap.pypa.io/get-pip.py"

REM Parse arguments
set "INCLUDE_MODEL=0"
if "%1"=="--model" set "INCLUDE_MODEL=1"

REM Check for curl or PowerShell
where curl >nul 2>&1
if %errorlevel% equ 0 (
    set "DOWNLOADER=curl"
) else (
    set "DOWNLOADER=powershell"
)

echo Step 1: Cleaning previous builds...
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%BUILD_DIR%"
mkdir "%OUTPUT_DIR%"

echo Step 2: Downloading Python embedded distribution...
set "PYTHON_ZIP=%BUILD_DIR%\python_embed.zip"

if "%DOWNLOADER%"=="curl" (
    curl -L -o "%PYTHON_ZIP%" "%PYTHON_EMBED_URL%"
) else (
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_EMBED_URL%' -OutFile '%PYTHON_ZIP%'"
)

if not exist "%PYTHON_ZIP%" (
    echo ERROR: Failed to download Python embedded!
    exit /b 1
)

echo Step 3: Extracting Python...
mkdir "%EMBED_DIR%"
powershell -Command "Expand-Archive -Path '%PYTHON_ZIP%' -DestinationPath '%EMBED_DIR%' -Force"

REM Enable site-packages in embedded Python
echo Step 4: Configuring embedded Python...
set "PTH_FILE="
for %%f in ("%EMBED_DIR%\python*._pth") do set "PTH_FILE=%%f"
if defined PTH_FILE (
    REM Uncomment import site line
    powershell -Command "(Get-Content '%PTH_FILE%') -replace '#import site', 'import site' | Set-Content '%PTH_FILE%'"
)

echo Step 5: Installing pip...
set "GET_PIP=%BUILD_DIR%\get-pip.py"
if "%DOWNLOADER%"=="curl" (
    curl -L -o "%GET_PIP%" "%GET_PIP_URL%"
) else (
    powershell -Command "Invoke-WebRequest -Uri '%GET_PIP_URL%' -OutFile '%GET_PIP%'"
)

"%EMBED_DIR%\python.exe" "%GET_PIP%" --no-warn-script-location

echo Step 6: Installing dependencies...
"%EMBED_DIR%\python.exe" -m pip install --no-warn-script-location -q blessed pygame

REM llama-cpp-python is optional and large
if %INCLUDE_MODEL% equ 1 (
    echo Installing llama-cpp-python (this may take a while)...
    "%EMBED_DIR%\python.exe" -m pip install --no-warn-script-location llama-cpp-python
) else (
    echo Skipping llama-cpp-python (use --model to include)
)

echo Step 7: Copying game files...
REM Copy Python runtime
xcopy "%EMBED_DIR%\*" "%OUTPUT_DIR%\runtime\" /e /i /q /y >nul

REM Copy game source
for %%d in (audio core dialogue duck ui world data assets) do (
    if exist "%SCRIPT_DIR%%%d" (
        xcopy "%SCRIPT_DIR%%%d" "%OUTPUT_DIR%\%%d\" /e /i /q /y >nul
        echo   + %%d\
    )
)

REM Copy individual files
for %%f in (main.py config.py game_logger.py download_model.py cheese.ico) do (
    if exist "%SCRIPT_DIR%%%f" (
        copy "%SCRIPT_DIR%%%f" "%OUTPUT_DIR%\" >nul
        echo   + %%f
    )
)

REM Copy audio files
for %%f in ("%SCRIPT_DIR%*.wav" "%SCRIPT_DIR%*.mp3") do (
    if exist "%%f" (
        copy "%%f" "%OUTPUT_DIR%\" >nul
    )
)

REM Copy models if requested
if %INCLUDE_MODEL% equ 1 (
    if exist "%SCRIPT_DIR%models" (
        xcopy "%SCRIPT_DIR%models" "%OUTPUT_DIR%\models\" /e /i /q /y >nul
        echo   + models\ (AI model)
    )
)

echo Step 8: Creating launcher...
(
echo @echo off
echo setlocal
echo cd /d "%%~dp0"
echo set "PATH=%%~dp0runtime;%%~dp0runtime\Scripts;%%PATH%%"
echo runtime\python.exe main.py %%*
echo endlocal
) > "%OUTPUT_DIR%\CheeseTheDuck.bat"

REM Create a VBS launcher for no console window on double-click (optional)
(
echo Set WshShell = CreateObject("WScript.Shell"^)
echo WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject"^).GetParentFolderName(WScript.ScriptFullName^)
echo WshShell.Run "CheeseTheDuck.bat", 1, False
) > "%OUTPUT_DIR%\CheeseTheDuck.vbs"

echo Step 9: Cleaning up...
rmdir /s /q "%BUILD_DIR%" 2>nul

echo.
echo ============================================================
echo   Build Complete!
echo ============================================================
echo.
echo Output: %OUTPUT_DIR%
echo.
echo To distribute:
echo   1. Zip the CheeseTheDuck-Portable folder
echo   2. Users can extract anywhere and run CheeseTheDuck.bat
echo.
echo To create an installer with Inno Setup:
echo   python build_windows_installer.py
echo.

REM Calculate size
for /f "tokens=3" %%a in ('dir "%OUTPUT_DIR%" /s ^| findstr "File(s)"') do set SIZE=%%a
echo Package size: approximately %SIZE% bytes
echo.

pause
