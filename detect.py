import cv2
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from ultralytics import YOLO

# Load Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://roadwatch-system-default-rtdb.firebaseio.com/"
    })

# Load ML model
with open("model/model.pkl", "rb") as f:
    clf = pickle.load(f)

# Load YOLOv8 (auto-downloads on first run)
yolo = YOLO("yolov8n.pt")

# GPS coordinates of your CCTV camera (set manually)
CAMERA_LAT = 16.5062   # Change to your city
CAMERA_LON = 80.6480

def classify_severity(bbox_area):
    width = int(bbox_area ** 0.5)
    features = [[
        int(bbox_area),          # crack_area_px
        round(width * 0.02, 2),  # depth_estimate (approximation)
        width,                   # pothole_width_px
        80,                      # brightness_diff (fixed estimate)
        1                        # road_type = city
    ]]
    return clf.predict(features)[0]

def push_to_firebase(lat, lon, severity):
    ref = db.reference("potholes")
    ref.push({
        "latitude": lat,
        "longitude": lon,
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "active",
        "confirmed_count": 1
    })
    print(f"Pushed: {severity} at ({lat}, {lon})")

def run_detection(source=0):  # 0 = webcam, or pass video file path
    cap = cv2.VideoCapture(source)
    frame_skip = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_skip += 1
        if frame_skip % 5 != 0:  # Process every 5th frame
            continue

        results = yolo(frame, verbose=False)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = yolo.names[cls_id]

                if "pothole" in label.lower() or cls_id == 0:  # adjust class id
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    area = (x2 - x1) * (y2 - y1)
                    severity = classify_severity(area)

                    # Draw box on frame
                    color = {"High":(0,0,255),"Medium":(0,165,255),"Low":(0,200,0)}
                    cv2.rectangle(frame, (x1,y1), (x2,y2), color[severity], 2)
                    cv2.putText(frame, severity, (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color[severity], 2)

                    push_to_firebase(CAMERA_LAT, CAMERA_LON, severity)

        cv2.imshow("RoadWatch CCTV", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_detection(source=0)  # Change to "video.mp4" for file input