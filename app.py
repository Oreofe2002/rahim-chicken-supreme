from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

CSV_FILE_PATH = "catering_leads.csv"


# Create CSV file if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp",
                "Customer Name",
                "Phone Number",
                "Order Details"
            ])


initialize_csv()


# THIS IS THE IMPORTANT PART
# It makes your website appear when someone visits the Render URL
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Catering form
@app.route("/api/catering", methods=["POST"])
def process_catering_inquiry():

    client_data = request.get_json()

    if not client_data or "name" not in client_data or "phone" not in client_data:
        return jsonify({
            "status": "rejected",
            "message": "Incomplete data"
        }), 400

    sender_name = client_data["name"]
    sender_phone = client_data["phone"]
    order_notes = client_data.get(
        "notes",
        "No custom instructions logged."
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(
            CSV_FILE_PATH,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                current_time,
                sender_name,
                sender_phone,
                order_notes
            ])

        return jsonify({
            "status": "delivered",
            "message": "Log updated!"
        }), 200

    except Exception as e:

        print(f"Error logging to spreadsheet: {e}")

        return jsonify({
            "status": "failed"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )