@echo off
title EPRA Document Auto-Stamper

echo ========================================================
echo               EPRA Document Auto-Stamper
echo ========================================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed on this computer
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found on this computer.
    echo Please install Python 3 and check "Add python.exe to PATH".
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if .venv virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] First-time setup: creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SETUP] Installing dependencies from requirements.txt...
    .venv\Scripts\python.exe -m pip install --upgrade pip
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo [SETUP] Dependencies installed successfully.
    echo.
)

REM Execute batch stamping
echo Scanning for PDFs in 'completions and commencements'...
echo --------------------------------------------------------
.venv\Scripts\python.exe stamper\batch.py
echo --------------------------------------------------------
echo.
echo Check the 'completions and commencements\output' folder for stamped files.
echo.
pause
