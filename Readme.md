YoPrint CSV Importer

This project is a CSV processing system built with Flask, SQLite, and Python background threads.
It allows users to upload CSV files, clean the data, and perform idempotent UPSERT operations based on a UNIQUE_KEY.

The implementation follows all YoPrint Coding Project requirements:

- Cleans non-UTF8 characters
- Idempotent processing (same file can be uploaded multiple times safely)
- UPSERT behavior using UNIQUE_KEY
- Background worker thread for CSV processing
- Error logging for problematic rows
- SQLite database for easy local testing

---

Project Structure

yoprint_cvs_app/
│
├── app.py               # Flask application
├── db.py                # SQLite database setup
├── models.py            # SQLAlchemy ORM models
├── jobs.py              # Background CSV processing job
│
├── templates/
│   └── index.html       # Frontend upload page
│
├── uploads/             # Uploaded CSVs (ignored in GitHub)
├── error_logs/          # Error logs (ignored in GitHub)
│
├── .gitignore           # Prevents tracking DB, uploads, logs, cache
├── requirements.txt     # Python dependencies
└── README.md            # Documentation

---

Running the Project

1. Create a virtual environment
python -m venv venv

2. Activate the virtual environment
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Start the Flask app
python app.py


The application will run at:
👉 http://127.0.0.1:5000/

---

Uploading a CSV File
1. Click Choose File
2. Select your CSV
3. Click Upload


After uploading, the system will display:
- A new upload record
- Status: processing
- Background job continues even if you navigate away

---

How UPSERT Works

Each row must include a UNIQUE_KEY.
- If UNIQUE_KEY does not exist → a new record is INSERTED
- If UNIQUE_KEY already exists → the record is UPDATED

This ensures idempotency—you can safely upload the same file repeatedly without creating duplicates.

---

Notes

- SQLite database (yoprint.db), uploads, and logs are ignored via .gitignore
- A fresh database is automatically created if it doesn't exist
- Only source code is included in the repository (as required)