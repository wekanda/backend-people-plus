@echo off
title PEOPLE PULSE - HR Server
cd /d "%~dp0"
echo Starting PEOPLE PULSE server...
echo Open http://127.0.0.1:8000 in your browser when it says "Application startup complete".
echo.
".venv-1\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000
pause