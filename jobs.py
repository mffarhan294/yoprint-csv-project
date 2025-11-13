import csv, os
from datetime import datetime
from db import SessionLocal
from models import Upload, Product

def clean_value(value):
    if value is None:
        return ""
    cleaned = (
        value.replace("\ufeff", "")  # Remove BOM
             .strip()
    )
    return cleaned


def process_csv_job(upload_id, file_path):
    print(">>> Background job started for upload:", upload_id)

    session = SessionLocal()
    upload = session.get(Upload, upload_id)

    if not upload:
        print("Upload record not found, stopping job.")
        session.close()
        return

    upload.status = "processing"
    session.commit()

    os.makedirs("error_logs", exist_ok=True)
    error_log_path = os.path.join("error_logs", f"error_log_{upload_id}.csv")

    total = success = errors = 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f, \
             open(error_log_path, "w", encoding="utf-8", newline="") as ef:

            reader = csv.DictReader(f)
            error_writer = csv.writer(ef)
            error_writer.writerow(["timestamp", "row_number", "error", "raw_row"])

            for row_number, row in enumerate(reader, start=2):

                print(f"Processing row #{row_number}")
                total += 1

                try:
                    unique_key = clean_value(row.get("UNIQUE_KEY"))
                    if not unique_key:
                        raise ValueError("Missing UNIQUE_KEY")

                    # UPSERT
                    product = session.query(Product).filter_by(unique_key=unique_key).first()

                    if not product:
                        product = Product(unique_key=unique_key)
                        session.add(product)
                        session.flush()  # Ensure INSERT is applied

                    # UPDATE fields
                    product.product_title = clean_value(row.get("PRODUCT_TITLE"))
                    product.product_description = clean_value(row.get("PRODUCT_DESCRIPTION"))
                    product.style = clean_value(row.get("STYLE#"))
                    product.sanmar_mainframe_color = clean_value(row.get("SANMAR_MAINFRAME_COLOR"))
                    product.size = clean_value(row.get("SIZE"))
                    product.color_name = clean_value(row.get("COLOR_NAME"))

                    price_raw = clean_value(row.get("PIECE_PRICE"))
                    product.piece_price = float(price_raw) if price_raw else None

                    session.flush()
                    success += 1

                except Exception as e:
                    errors += 1
                    print(f"Error at row {row_number}: {e}")
                    error_writer.writerow([
                        datetime.utcnow().isoformat(),
                        row_number,
                        str(e),
                        repr(row)
                    ])

            # final commit
            session.commit()

        upload.status = "completed"
        upload.total_rows = total
        upload.success_rows = success
        upload.error_rows = errors
        upload.message = f"Processed {total} rows. Success: {success}, Errors: {errors}"

        print(">>> Job completed successfully!")

    except Exception as e:
        upload.status = "failed"
        upload.message = f"Failed: {e}"
        print(">>> Job failed:", e)
        session.rollback()

    finally:
        session.commit()
        session.close()
