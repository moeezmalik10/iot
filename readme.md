# 🛡️ IoT Device Security Scanner

A **Flask-based IoT Network Security Scanner** that detects connected devices, captures their network traffic, extracts features, and predicts their **risk level** (High / Medium / Low / Safe) using a pre-trained Machine Learning model.  

---

## 📊 Dataset

This project uses the **IoT Intrusion Detection Dataset** available on Kaggle:  
🔗 [IoT Intrusion Dataset – Kaggle](https://www.kaggle.com/datasets/subhajournal/iotintrusion?resource=download)

---

## 🚀 Key Features

✅ Scan your local subnet to discover IoT devices  
✅ Capture live network packets using Scapy  
✅ Extract and analyze traffic flow features  
✅ Predict device security risk via ML model  
✅ Visual dashboard with pie chart & summaries  
✅ Export full scan report as PDF  
✅ Supports multilingual UI (English / Urdu / Punjabi)  

---

## 🧠 Tech Stack

| Technology | Purpose |
|-------------|----------|
| **Flask** | Backend web framework |
| **Scapy** | Packet sniffing & feature extraction |
| **Nmap** | Device discovery on network |
| **scikit-learn** | ML model (Decision Tree Classifier) |
| **Bootstrap 5** | Frontend styling |
| **Chart.js** | Graphical result visualization |
| **jsPDF** | PDF report generation |

---

## 🧩 Project Structure

IOT_Device_scanner/
├── app.py # Flask web app
├── feature_extractor.py # Feature extraction logic
├── scanner.py # Network device discovery
├── iot_scanner_model.pkl # Trained ML model
├── templates/
│ └── UI.html # Main web interface
└── README.md


---

## ⚙️ Installation & Setup

### 1Clone or Download Project
If downloaded manually, extract it into a folder, e.g.:
C:\Users<yourname>\Downloads\FlaskSetUp


### 2️(Optional) Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate    # For Windows
# OR
source venv/bin/activate # For Linux/macOS

3️Install Required Libraries
pip install -r requirements.txt


If requirements.txt isn’t available, manually install these:
Flask, scapy, numpy, scikit-learn, chart.js, jspdf

4️⃣ Run the App (As Administrator)

Packet sniffing requires elevated privileges:

python app.py


Once running, open your browser at:
👉 http://127.0.0.1:5000
🖥️ Usage Guide

Click Start Security Scan

Wait while your network is scanned

View results in the dashboard:

Risk summary pie chart

Individual device cards (IP, MAC, risk level, flow count)

Export report as PDF for documentation

⚠️ Notes

Run as Administrator / sudo — required for Scapy to capture packets

Ensure NPcap is installed and the correct network interface is selected in app.py

If no packets are captured, increase:

CAPTURE_DURATION = 15


For large .pkl model files (>25 MB), host externally (Google Drive, GitHub Releases, etc.)

💡 Credits & License

Dataset: IoT Intrusion Detection Dataset
 by SubhaJournal

Developed using:

Flask

Scapy

Bootstrap

Chart.js

jsPDF

Licensed under the MIT License.

💬 “Secure your IoT world — one packet at a time.”