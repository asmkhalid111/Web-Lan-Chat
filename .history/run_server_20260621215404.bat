@echo off
echo Setting up environment...

IF NOT EXIST "venv\Scripts\activate" (
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo Starting server...
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

pause