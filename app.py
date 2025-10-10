# app.py
from flask import Flask, jsonify, render_template
import pickle, os, time, numpy as np, traceback
from scanner import discover_devices
from feature_extractor import capture_and_extract_for_ip

app = Flask(__name__, template_folder="templates")

MODEL_PATH = "iot_scanner_model.pkl"
NETWORK_SUBNET = "10.40.196.0/24"  # change if needed
CAPTURE_DURATION = 10               # seconds
CAPTURE_INTERFACE = "\\Device\\NPF_{BBF7B3CF-6B74-4407-BEA1-AD15A298585A}"
PCAP_FALLBACK = None                # use "sample.pcap" for testing (optional)

# Load model
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


@app.route("/")
def home():
    """Render main UI page"""
    return render_template("UI.html")


@app.route("/scan_predict", methods=["GET"])
def scan_predict():
    try:
        devices = discover_devices(NETWORK_SUBNET)
        if not devices:
            return jsonify({
                "predictions": [],
                "message": "No devices discovered on subnet."
            })

        all_results = []
        for dev in devices:
            ip = dev.get("ip")
            name = dev.get("name", ip)
            mac = dev.get("mac", "")

            features, metas = capture_and_extract_for_ip(
                ip, duration=CAPTURE_DURATION, iface=CAPTURE_INTERFACE, pcap_file=PCAP_FALLBACK
            )

            # 🧠 FIX 1: Ensure even test packets return results
            if not features or len(features) == 0:
                print(f"[!] No features extracted for {ip}. Returning placeholder.")
                all_results.append({
                    "ip": ip,
                    "name": name,
                    "mac": mac,
                    "predictions": [{"flow": "none", "risk": 0}],
                    "message": "No flows captured. Try longer capture or admin mode."
                })
                continue

            X = np.array(features)
            preds = model.predict(X) if hasattr(model, "predict") else [0]*len(X)

            # 🧠 FIX 2: Ensure UI-friendly JSON format
            flow_results = []
            for meta, pred in zip(metas, preds):
                try:
                    src, dst, sport, dport, proto = meta
                    flow_results.append({
                        "flow": f"{src}:{sport}->{dst}:{dport}",
                        "src": src, "dst": dst,
                        "sport": sport, "dport": dport,
                        "protocol": proto,
                        "risk": int(pred)
                    })
                except Exception:
                    continue

            all_results.append({
                "ip": ip,
                "name": name,
                "mac": mac,
                "predictions": flow_results,
                "packet_count": len(features)
            })

        # 🧠 FIX 3: Return total count + timestamp for UI chart
        return jsonify({
            "predictions": all_results,
            "total_devices": len(all_results),
            "timestamp": time.time()
        })

    except Exception as e:
        print("❌ Error in scan_predict:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("[!] Run as Administrator (Windows) or with sudo (Linux) to allow packet sniffing.")
    app.run(host="0.0.0.0", port=5000, debug=True)
