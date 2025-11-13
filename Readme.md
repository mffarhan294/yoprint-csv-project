# YoPrint CSV Import System (Flask + SQLite)

A lightweight CSV upload and import system built with:

- Flask (Python)
- SQLite (via SQLAlchemy)
- Background processing using Python threads

## Features

- Upload CSV files
- Automatically clean non-UTF8 characters
- Idempotent imports (re-uploading same file will not duplicate)
- UPSERT using UNIQUE_KEY
- Background processing (non-blocking)
- Error logging to `error_logs/`
- Upload history table with auto-refresh
- Simple UI built with HTML + JS

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
