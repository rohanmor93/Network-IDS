from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from flask_cors import CORS
import joblib
from netifaces import interfaces
import numpy as np
import pandas as pd
import psutil
from scapy.all import sniff, IP, TCP, UDP
import threading
import pyshark

app = Flask(__name__)
CORS(app)
app.secret_key = 'd3e9a8d90be38d348f87f5ae07c91e63c0bd2ff80f1bc01c93d0a1c9fbeadb70'

# Dummy credentials
USERNAME = "admin"
PASSWORD = "rohan123"

# Load model
model = joblib.load("backend/model/ids_model.joblib")

# --------------- Authentication -------------------

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == USERNAME and password == PASSWORD:
        session["user"] = username
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/", methods=["GET"])
def home():
    if "user" in session:
        return render_template("index.html")
    return redirect(url_for("login_page"))

# ---------- ROUTE: Predict from 41 Features ----------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = data.get("features")
        if not features or len(features) != 41:
            return jsonify({"error": "Expected 41 features"}), 400

        features_array = np.array(features).reshape(1, -1)
        prediction = model.predict(features_array)[0]
        result = "Attack" if prediction == 1 else "Normal"
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- ROUTE: Predict from Uploaded CSV ----------
@app.route("/predict_csv", methods=["POST"])
def predict_csv():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        df = pd.read_csv(file)

        if df.shape[1] != 41:
            return jsonify({'error': f'CSV must have 41 features, found {df.shape[1]}'}), 400

        preds = model.predict(df)
        readable_preds = ["Attack" if p == 1 else "Normal" for p in preds]
        return jsonify({'results': readable_preds})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------- ROUTE: Get Network Interfaces ----------
@app.route("/get_interfaces", methods=["GET"])
def get_interfaces():
    try:
        interfaces = list(psutil.net_if_addrs().keys())
        return jsonify({"interfaces": interfaces})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Helper: Extract Features from Packet ----------
def extract_features(packet):
    try:
        protocol = 0
        sport, dport = 0, 0
        if packet.haslayer(TCP):
            protocol = 1
            sport = packet[TCP].sport
            dport = packet[TCP].dport
        elif packet.haslayer(UDP):
            protocol = 2
            sport = packet[UDP].sport
            dport = packet[UDP].dport

        length = len(packet)

        features = [0] * 41
        features[0] = protocol
        features[1] = sport
        features[2] = dport
        features[3] = length

        return features
    except Exception as e:
        print(f"[Feature Extraction Error] {e}")
        return None

# ---------- ROUTE: Start Real-Time Packet Capture ----------
@app.route("/start_capture", methods=["GET"])
# ---------- ROUTE: Start Real-Time Packet Capture ----------
@app.route("/start_capture", methods=["GET"])
@app.route("/start_capture", methods=["GET"])
def start_capture():
    interface = request.args.get("interface")
    packet_limit = int(request.args.get("count", 10))

    if not interface:
        return jsonify({"error": "No interface specified"}), 400

    results = []

    def process_packet(packet):
        try:
            # Optional: filter only IP packets
            # if IP in packet:
            features = extract_features(packet)
            if features:
                features_array = np.array(features).reshape(1, -1)
                prediction = model.predict(features_array)[0]
                result = "Attack" if prediction == 1 else "Normal"
                summary = {
                    "packet": packet.summary(),
                    "prediction": result
                }
                print(summary)
                results.append(summary)
        except Exception as e:
            print(f"[Processing Error] {e}")

    try:
        sniff_thread = threading.Thread(
            target=sniff,
            kwargs={
                'iface': interface,
                'prn': process_packet,
                'count': packet_limit,
                'store': False
            }
        )
        sniff_thread.start()
        sniff_thread.join()

        return jsonify({"capture_data": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# @app.route("/start_capture_pyshark", methods=["GET"])
# def start_capture_pyshark():
#     interface = request.args.get("interface")
#     packet_limit = int(request.args.get("count", 10))

#     if not interface:
#         return jsonify({"error": "No interface specified"}), 400

#     results = []

#     try:
#         capture = pyshark.LiveCapture(interface=interface)

#         for i, packet in enumerate(capture.sniff_continuously(packet_count=packet_limit)):
#             try:
#                 features = extract_pyshark_features(packet)
#                 if features:
#                     features_array = np.array(features).reshape(1, -1)
#                     prediction = model.predict(features_array)[0]
#                     result = "Attack" if prediction == 1 else "Normal"

#                     summary = {
#                         "packet": str(packet.highest_layer),
#                         "prediction": result
#                     }
#                     print(summary)
#                     results.append(summary)
#             except Exception as e:
#                 print(f"[PyShark Packet Error] {e}")

#         return jsonify({"capture_data": results})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
# def extract_pyshark_features(packet):
#     try:
#         features = [0] * 41
#         protocol = 0
#         sport, dport = 0, 0
#         length = int(packet.length)

#         if hasattr(packet, 'tcp'):
#             protocol = 1
#             sport = int(packet.tcp.srcport)
#             dport = int(packet.tcp.dstport)
#         elif hasattr(packet, 'udp'):
#             protocol = 2
#             sport = int(packet.udp.srcport)
#             dport = int(packet.udp.dstport)

#         features[0] = protocol
#         features[1] = sport
#         features[2] = dport
#         features[3] = length

#         return features
#     except Exception as e:
#         print(f"[PyShark Feature Extraction Error] {e}")
#         return None



# ---------- Main ----------
if __name__ == "__main__":
    app.run(debug=True)