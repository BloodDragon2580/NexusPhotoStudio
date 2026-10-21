@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (echo Python 3 fehlt & pause & exit /b 1)
where cargo >nul 2>nul
if errorlevel 1 (echo Rust/Cargo fehlt & pause & exit /b 1)
echo ==== Nexus Photo Studio Alpha ====
python tools\generate_nexus_icons.py .
if errorlevel 1 (echo Icon-Generierung fehlgeschlagen & pause & exit /b 1)
cargo build --release --locked -p photocraft
if errorlevel 1 (echo Build fehlgeschlagen & pause & exit /b 1)
python tools\verify_nexus_exe_icon.py target\release\photocraft.exe assets\app-icon\photocraft.ico
if errorlevel 1 (echo Nexus-EXE-Icon-Pruefung fehlgeschlagen & pause & exit /b 1)
copy /Y target\release\photocraft.exe NexusPhotoStudio.exe
if errorlevel 1 (echo Kopieren fehlgeschlagen & pause & exit /b 1)
echo Fertig: NexusPhotoStudio.exe (ungesignierte Alpha)
pause
