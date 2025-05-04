@echo off
setlocal

:: Set virtual environment directory
set VENV_DIR=venv

:: Check if virtual environment exists
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

:: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

:: Install required packages
pip install --upgrade pip
pip install matplotlib networkx

:: Run your Python script (replace script.py with your filename)
python CourseGraphUI.py

endlocal
pause