# 🛡️ Adaptive Human Risk Engine (AHRE)

> **Detecting risky user behavior before it becomes a security incident.**

AHRE is an Explainable AI (XAI) and Machine Learning powered cyber-risk assessment system. It analyzes employee/user behavioral logs to establish normal baseline activity, detect meaningful behavioral deviations, compute dynamic 0-100 risk scores, explain score spikes, and display actionable threat insights on an interactive security dashboard.

---

## 📌 Project Architecture

```text
User Activity Logs (CERT Dataset)
             ↓
[ Member 1 ] Data Pipeline & Behavioral Baseline Profiling
             ↓
[ Member 2 ] Anomaly Detection Model & Risk Score Engine (0-100) + XAI Explainer
             ↓
[ Member 3 ] Security Monitoring Dashboard & Threat Alerts
```

---

## 📁 Repository Structure

```text
MINOR/
├── data/
│   ├── raw/                 # CERT raw CSV logs (Logon, Device, File, HTTP, Email)
│   └── processed/           # Extracted behavioral feature matrix
├── src/
│   ├── data_pipeline/       # Log ingestion, cleaning & user baseline extraction
│   ├── models/              # Isolation Forest / Autoencoder & Risk Scoring Engine
│   └── dashboard/           # Flask API & Frontend Security UI
├── notebooks/               # EDA and experiment notebooks
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 👥 Team Work Division

| Member | Primary Responsibility | Focus Area |
| :--- | :--- | :--- |
| **Member 1** | Data Pipeline Lead | Data cleaning, CERT log parsing, user baseline calculation |
| **Member 2** | ML & Explainability Lead | Anomaly detection model, 0-100 risk scoring algorithm, SHAP explanations |
| **Member 3** | Dashboard & UI Lead | Interactive security dashboard, threat ledger, alert visualizations |

---

## ⚙️ Quick Start Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd MINOR
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📊 Dataset Requirements
This project utilizes the **CERT Insider Threat Dataset** (Carnegie Mellon SEI).
Place raw CSV dataset files inside `data/raw/`.
