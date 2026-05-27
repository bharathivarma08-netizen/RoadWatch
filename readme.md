# 🛣️ RoadWatch

An AI-powered road monitoring and toll management system that detects potholes using CCTV footage and provides real-time dashboards for drivers, admins, and toll operators.

---

## 🚀 Features

- 🔍 **Pothole Detection** — YOLOv8 + OpenCV CCTV pipeline for real-time road condition analysis
- 🤖 **ML Prediction** — Random Forest model trained on road condition data
- 🚗 **5 Portals** — Login, User, Driver, Toll, and Admin dashboards
- 🔥 **Firebase Integration** — Real-time database for all routes and portals
- 📊 **Admin Dashboard** — Monitor road reports, manage users, view analytics

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| ML Model | Random Forest (scikit-learn) |
| Computer Vision | YOLOv8, OpenCV |
| Database | Firebase (Realtime DB) |

---

## 📁 Project Structure

```
RoadWatch/
├── app.py                  # Main Flask application
├── detect.py               # CCTV pothole detection (YOLOv8 + OpenCV)
├── train_model.py          # ML model training script
├── generate_dataset.py     # Dataset generation utility
├── requirements.txt        # Python dependencies
├── templates/              # HTML portals (login, user, driver, toll, admin)
├── static/                 # CSS and JavaScript files
├── model/
│   └── model.pkl           # Trained Random Forest model
└── data/
    └── pothole_data.csv    # Road condition dataset
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/RoadWatch.git
cd RoadWatch
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Firebase
- Create a Firebase project at [firebase.google.com](https://firebase.google.com)
- Download your service account key and save it as `firebase-key.json` in the root folder
- ⚠️ Never commit `firebase-key.json` to GitHub

### 4. Run the application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🖥️ Portals

| Portal | URL | Description |
|--------|-----|-------------|
| Login | `/` | Authentication page |
| User | `/user` | Report road issues |
| Driver | `/driver` | View road conditions on route |
| Toll | `/toll` | Toll booth management |
| Admin | `/admin` | Full system dashboard |

---

## 🤖 ML Model

- **Algorithm:** Random Forest Classifier
- **Training data:** `data/pothole_data.csv`
- **Model file:** `model/model.pkl`
- **Training script:** `train_model.py`

To retrain the model:
```bash
python train_model.py
```

---

## 📹 Demo

- - 🎥 **Demo Video:** [Watch on Google Drive](https://drive.google.com/file/d/1I9EbodpdDMEOjuo4gOa5C4Vk29_TrZxE/view?usp=drivesdk)
- 🌐 **Live Demo:** `http://localhost:5000`

---

## 📦 Requirements

See `requirements.txt` for the full list. Key dependencies:

```
flask
firebase-admin
scikit-learn
opencv-python
ultralytics
pandas
numpy
```

---

## 🏆 Built For

**National Road Safety Hackathon 2026 — IIT Madras (CoERS & RBG Labs)**

