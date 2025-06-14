
# 🐦 BirdCam Server on Ubuntu (Proxmox VM)

This project hosts a local HTTP server to receive images and sensor data from your ESP32-CAM, classify the bird species, annotate the image, and serve a simple gallery interface.

---

## 🔧 Setup Instructions (One Time Only)

### 1. Install Required Packages
```bash
sudo apt update
sudo apt install python3-venv python3-full
```

### 2. Create a Python Virtual Environment
```bash
python3 -m venv birdcam-env
```

### 3. Activate the Environment
```bash
source birdcam-env/bin/activate
```

### 4. Install Required Python Libraries
```bash
pip install flask pillow opencv-python numpy pytz
```

---

## 🚀 Running the Server

From the root of the project:

```bash
source birdcam-env/bin/activate
python server.py
```

Then open your browser at:
```
http://<your-server-ip>:8080/
```

---

## ⏱️ Development Tips

- While the virtual environment is active, you can modify `server.py` and restart to see changes.
- To auto-restart the server on code changes during development:
```bash
export FLASK_ENV=development
python server.py
```

---

## 🧠 Useful Commands

### Activate virtual environment (always do this before running server)
```bash
source birdcam-env/bin/activate
```

### Deactivate virtual environment
```bash
deactivate
```

### Reinstall dependencies (if `requirements.txt` exists)
```bash
pip install -r requirements.txt
```

---

## 🌍 Remote Development via VS Code

1. Install **Remote - SSH** extension in VS Code
2. Connect to this server via `Remote-SSH: Connect to Host...`
3. Work in your local VS Code, but on your server's filesystem

---

## 🛠️ Troubleshooting

- If `pip` fails due to "externally-managed environment", always use the virtual environment.
- If the server doesn't respond, make sure port 8080 is open or not blocked by firewall.

---

## 🗑️ Remove the Environment (if needed)

```bash
rm -rf birdcam-env
```

---

## 🧪 Testing Upload from ESP32

Make sure your ESP32 POSTs to:
```
http://<your-server-ip>:8080/upload
```

And the content-type is set to:
```
application/octet-stream
```

---

Happy birdwatching! 🐥
