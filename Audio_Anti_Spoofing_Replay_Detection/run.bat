@echo off
setlocal
cd /d "%~dp0"
set "PYTHON="

rem Prefer a project-local virtual environment.
if exist "%~dp0.venv\Scripts\python.exe" call :try_python "%~dp0.venv\Scripts\python.exe"

rem Otherwise try Python installations available on PATH.
if not defined PYTHON for /f "delims=" %%P in ('where python 2^>nul') do if not defined PYTHON call :try_python "%%P"

rem Common portable/local Python 3.12 locations.
if not defined PYTHON if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" call :try_python "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PYTHON if exist "%~dp0..\quran\tools\python312\python.exe" call :try_python "%~dp0..\quran\tools\python312\python.exe"

if not defined PYTHON (
  echo Python compatible version was not found.
  echo Please install Python 3.12 or use the project virtual environment.
  pause
  exit /b 1
)

"%PYTHON%" "%~dp0app\demo.py"
if errorlevel 1 (
  echo.
  echo The application could not be started. Check the dependencies in requirements.txt.
  pause
)
endlocal
exit /b

:try_python
set "CANDIDATE=%~1"
"%CANDIDATE%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 set "PYTHON=%CANDIDATE%"
exit /b
