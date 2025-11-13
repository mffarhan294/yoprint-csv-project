import traceback
import os, threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from db import Base, engine, SessionLocal
from models import Upload
from jobs import process_csv_job

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
Base.metadata.create_all(bind=engine)

def run_in_background(upload_id, file_path):
    print(">>> Starting background thread for upload:", upload_id)
    thread = threading.Thread(target=process_csv_job, args=(upload_id, file_path))
    thread.daemon = True
    thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    print(">>> Upload received")

    file = request.files.get("file")
    if not file or not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Please upload a CSV file"}), 400

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{timestamp}_{file.filename}")
    file.save(file_path)

    session = SessionLocal()
    upload = Upload(filename=file.filename, status="pending")
    session.add(upload)
    session.commit()
    upload_id = upload.id
    print(">>> Created upload record with ID:", upload_id)

    session.close()

    run_in_background(upload_id, file_path)

    return jsonify({"message": "File uploaded", "upload_id": upload_id})

@app.route("/uploads")
def uploads_list():
    session = SessionLocal()
    uploads = session.query(Upload).order_by(Upload.created_at.desc()).all()
    result = [u.to_dict() for u in uploads]
    session.close()
    return jsonify(result)

if __name__ == "__main__":
    try:
        print(">>> Flask app starting...")
        app.run(debug=True)
    except Exception as e:
        print("ERROR STARTING FLASK APP:")
        traceback.print_exc()
