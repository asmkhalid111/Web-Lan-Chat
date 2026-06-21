:: run_tests.bat
@echo off
echo Running tests...

IF NOT EXIST "venv\Scripts\activate" (
    echo Virtual environment not found. Run run_server.bat first.
    pause
    exit /b
)

call venv\Scripts\activate
pytest tests/ -v

pause