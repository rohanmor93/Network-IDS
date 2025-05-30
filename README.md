# 🛡️ Intrusion Detection System (IDS) Web Application

A full-stack machine learning–based IDS built with Python (Flask), Scapy, PyShark, and Tailwind CSS. This project detects network intrusions by classifying packets as **Attack** or **Normal** using a trained ML model and offers multiple modes of input: manual, CSV-based, and real-time live capture.

---

## 📌 Features

- 🔐 **Login Authentication Page**
- ✍️ **Manual Feature Entry** – Enter 41 features manually to get predictions
- 📂 **CSV File Upload** – Upload a dataset and classify multiple entries
- 🌐 **Real-Time Packet Capture** – Select a network interface to sniff packets and detect live threats
- 📊 **Table-Based Results** – Color-coded tabular output (green for normal, red for attack)
- 📡 **Interface Detection** – Dynamically fetches available network interfaces
- 🎨 **Neon-styled UI** – Built using Tailwind CSS and responsive HTML

---

## 🚀 Demo

> *Coming Soon: Add a link to the Vercel deployment if hosted*

---

## 🛠️ Technologies Used

| Layer       | Tools & Libraries                                |
|-------------|--------------------------------------------------|
| Frontend    | HTML, Tailwind CSS, JavaScript, Axios            |
| Backend     | Flask, Scapy, PyShark, psutil, netifaces         |
| ML Model    | Scikit-learn, Pandas, NumPy, Joblib              |
| Dataset     | [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html) |
| Deployment  | GitHub, Vercel *(Frontend)*                      |

---

## 🧠 How It Works

- **Manual Entry:** Accepts 41 features to classify a single data point.
- **CSV Upload:** Reads a CSV with 41 columns, applies the model, returns a prediction for each row.
- **Live Capture:** Uses Scapy or PyShark to sniff packets from a selected interface and classifies them on the fly.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ids-webapp.git
   cd ids-webapp
