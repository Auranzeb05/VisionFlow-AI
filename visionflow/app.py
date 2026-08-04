import os
import sys

import cv2
from speed_estimator import SpeedEstimator
from traffic_density import TrafficDensity
from vehicle_counter import VehicleCounter
from wrong_way_detector import WrongWayDetector

from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolo11n.pt")


# Create objects
counter = VehicleCounter()
density = TrafficDensity()
speed_estimator = SpeedEstimator()
wrong_way = WrongWayDetector()


# Project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Video path
video_path = os.path.join(BASE_DIR, "videos", "highway.mp4")


# Open video
cap = cv2.VideoCapture(video_path)


if not cap.isOpened():
    print("Error: Video not detected")
    sys.exit()


print("VisionFlow AI Started...")


while cap.isOpened():
    success, frame = cap.read()

    if not success:
        break

    # YOLO tracking
    results = model.track(frame, persist=True, conf=0.3, imgsz=416, verbose=False)

    boxes = results[0].boxes

    # Wrong way detection
    wrong_way_ids = wrong_way.check(boxes)

    # Update speed
    speed_estimator.update(boxes)

    # Vehicle counter
    if boxes.id is not None:
        counter.update(boxes, results[0].names)

    # Draw detections
    annotated_frame = results[0].plot()

    # -----------------------------
    # Individual vehicle speed
    # -----------------------------

    for box in boxes:
        if box.id is not None:
            track_id = int(box.id.item())

            speed = speed_estimator.get_speed(track_id)

            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)

            cv2.putText(
                annotated_frame, f"{speed} km/h", (x1, y1 - 45), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3
            )

    # -----------------------------
    # Wrong way highlight
    # -----------------------------

    for box in boxes:
        if box.id is not None:
            track_id = int(box.id.item())

            if track_id in wrong_way_ids:
                x1, y1, x2, y2 = box.xyxy[0]

                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 180), 6)

                cv2.putText(
                    annotated_frame,
                    f"WRONG WAY ID:{track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

    # -----------------------------
    # Analytics
    # -----------------------------

    total_vehicles = counter.get_count()

    vehicle_details = counter.get_details()

    traffic_status = density.calculate(total_vehicles)

    average_speed = speed_estimator.get_average_speed()

    print(f"Vehicles: {total_vehicles} | Traffic: {traffic_status} | Avg Speed: {average_speed} km/h")

    # Dashboard

    cv2.putText(annotated_frame, f"Vehicles: {total_vehicles}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Traffic: {traffic_status}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(
        annotated_frame, f"Cars: {vehicle_details['car']}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
    )

    cv2.putText(
        annotated_frame,
        f"Buses: {vehicle_details['bus']}",
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        annotated_frame,
        f"Trucks: {vehicle_details['truck']}",
        (20, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        annotated_frame,
        f"Motorcycles: {vehicle_details['motorcycle']}",
        (20, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        annotated_frame,
        f"Bicycles: {vehicle_details['bicycle']}",
        (20, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        annotated_frame, f"Avg Speed: {average_speed} km/h", (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
    )

    # Show video

    cv2.imshow("VisionFlow AI", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()


print("Total Vehicles Detected:", counter.get_count())

print("Vehicle Details:", counter.get_details())
