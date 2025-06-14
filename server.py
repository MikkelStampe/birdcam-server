
from flask import Flask, request, send_from_directory
from PIL import Image, ImageDraw
from datetime import datetime, timedelta
import os
import json
import pytz

from classify import classify_bird

app = Flask(__name__)
UPLOAD_FOLDER = "images"
SENSOR_DATA_FILE = "sensor_data.ndjson"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def annotate_image(path, label):
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), label, fill="yellow")
    image.save(path)

@app.route('/upload-bird', methods=['POST'])
def upload_image():
    img = request.data
    tz = pytz.timezone("Europe/Copenhagen")
    now = datetime.now(tz)
    ts = now.strftime('%Y%m%d_%H%M%S')
    human_readable = now.strftime('%d %B %Y, %H:%M:%S')

    img_path = os.path.join(UPLOAD_FOLDER, f"{ts}.jpg")
    with open(img_path, 'wb') as f:
        f.write(img)

    species = classify_bird(img_path)

    txt_path = os.path.join(UPLOAD_FOLDER, f"{ts}.txt")
    with open(txt_path, 'w') as meta_file:
        meta_file.write(f"{human_readable} — {species}")

    annotate_image(img_path, species)

    return {'status': 'ok', 'timestamp': ts, 'species': species}, 200

@app.route('/upload-sensor-data', methods=['POST'])
def upload_sensor_data():
    data = request.get_json()
    tz = pytz.timezone("Europe/Copenhagen")
    now = datetime.now(tz).isoformat()

    record = {
        "timestamp": now,
        "temp": data.get("temp"),
        "humidity": data.get("humidity"),
        "battery_mv": data.get("battery_mv")
    }

    with open(SENSOR_DATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

    return {'status': 'ok'}, 200

def load_sensor_data():
    records = []
    if os.path.exists(SENSOR_DATA_FILE):
        with open(SENSOR_DATA_FILE) as f:
            for line in f:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records

def find_nearest_sensor(timestamp_str):
    try:
        tz = pytz.timezone("Europe/Copenhagen")
        # Parse as naive, then localize to same tz as sensor data
        target_dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
        target_dt = tz.localize(target_dt)
    except Exception as e:
        print(f"Timestamp parse error: {e}")
        return None

    sensor_data = load_sensor_data()
    closest = None
    min_delta = timedelta.max
    for entry in sensor_data:
        try:
            entry_dt = datetime.fromisoformat(entry["timestamp"])
            delta = abs(entry_dt - target_dt)
            if delta < min_delta:
                min_delta = delta
                closest = entry
        except Exception as e:
            print(f"Sensor parse error: {e}")
            continue
    return closest


@app.route('/')
def index():
    files = sorted([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".jpg")], reverse=True)
    html = """
    <!doctype html>
    <html>
    <head>
        <title>BirdCam Gallery</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-4">
            <h1 class="mb-4 text-center">🐦 BirdCam Gallery</h1>
            <div class="row g-4">
    """

    for f in files:
        label = f
        txt_file = f.replace(".jpg", ".txt")
        txt_path = os.path.join(UPLOAD_FOLDER, txt_file)
        if os.path.exists(txt_path):
            with open(txt_path) as mf:
                label = mf.read().strip()

        base_name = f.replace(".jpg", "")
        sensor = find_nearest_sensor(base_name)
        sensor_info = ""
        if sensor:
            sensor_info = f"<small>🌡 {sensor['temp']}°C 💧 {sensor['humidity']}% 🔋 {sensor['battery_mv']} mV</small>"

        html += f'''
        <div class="col-md-4">
            <div class="card shadow">
                <img src="/images/{f}" class="card-img-top" alt="{f}">
                <div class="card-body text-center">
                    <p class="card-text">{label}</p>
                    <p class="card-text text-muted">{sensor_info}</p>
                </div>
            </div>
        </div>
        '''

    html += """
            </div>
        </div>
    </body>
    </html>
    """
    return html

@app.route('/images/<path:filename>')
def serve_img(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/data')
def data_table():
    data = load_sensor_data()
    html = """
    <html><head><title>Sensor Data</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head><body><div class="container py-4">
    <h2>📊 Sensor Data Table</h2>
    <table class="table table-striped">
    <thead><tr><th>Timestamp</th><th>Temp (°C)</th><th>Humidity (%)</th><th>Battery (mV)</th></tr></thead><tbody>
    """
    for entry in reversed(data):
        html += f"<tr><td>{entry['timestamp']}</td><td>{entry['temp']}</td><td>{entry['humidity']}</td><td>{entry['battery_mv']}</td></tr>"
    html += "</tbody></table></div></body></html>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
