# YoPrint CSV Importer

This project is a CSV processing system built with **Flask**, **SQLite**, and **Python background threads**.  
It allows users to upload CSV files, clean the data, and perform **idempotent UPSERT operations** using a `UNIQUE_KEY`.

This implementation follows the YoPrint Coding Project requirements:

- Cleans non-UTF8 characters  
- Idempotent file processing (same file can be uploaded multiple times)  
- UPSERT using `UNIQUE_KEY`  
- Runs CSV processing in a background worker  
- Logs problematic rows  
- Uses SQLite for easy local testing  

---

## 📁 Project Structure

yoprint_cvs_app/
│
├── app.py # Flask application
├── db.py # SQLite database setup
├── models.py # SQLAlchemy ORM models
├── jobs.py # Background CSV processing job
│
├── templates/
│ └── index.html # Frontend upload page
│
├── uploads/ # Uploaded CSVs (ignored in GitHub)
├── error_logs/ # Error logs (ignored in GitHub)
│
├── .gitignore # Prevents tracking DB, uploads, logs, cache
├── requirements.txt # Python dependencies
└── Readme.md # Documentation


---

## ▶️ Running the Project

1. Create a virtual environment:
python -m venv venv


2. Activate it:
venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt


4. Start the Flask app:
python app.py


The application will run at:
http://127.0.0.1:5000/


---

## 📤 Uploading a CSV File

1. Click **Choose File**
2. Select your CSV
3. Click **Upload**

After uploading:

- A new upload record will appear  
- Status will show **processing**  
- Background job continues even if you navigate away  

---

## 🔧 How UPSERT Works

Each row must include `UNIQUE_KEY`.

- If `UNIQUE_KEY` does **not** exist → INSERT  
- If `UNIQUE_KEY` exists → UPDATE  

This ensures idempotency (safe to re-upload the file multiple times).

---

## 📝 Notes

- SQLite database, uploads, and logs are excluded from GitHub using `.gitignore`
- A new database is automatically created on startup  
