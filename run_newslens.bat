@echo off
title NewsLens
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Setting up NewsLens for the first time...
  python -m venv .venv
  call .venv\Scripts\activate.bat
  python -m pip install -r requirements.txt
) else (
  call .venv\Scripts\activate.bat
)

start "" /B python app.py
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:5000
pause
