from ultralytics import YOLO
from PIL import Image
import cv2
import math
import matplotlib.pyplot as plt

model=YOLO("yolov8n.pt")

def videoStream():
    cap = cv2.VideoCapture(0)
    classNames = ["car","truck","vehicle"]

    while True:
        success, img = cap.read()
        if not success:
            break

        # Doing detections using YOLOv8 frame by frame
        results = model(img, stream=True)

        # Process the detected objects and draw bounding boxes
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name} {conf:.2f}'

                text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, thickness=1)
                c2_x = x1 + text_size[0] + 10
                c2_y = y1 - text_size[1] - 5
                cv2.rectangle(img, (x1, y1), (c2_x, c2_y), [0, 255, 0], -1, cv2.LINE_AA)
                cv2.putText(img, label, (x1, y1 - 2), 0, 0.7, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        if not ret:
            break

        # Convert the frame buffer to bytes
        frame_bytes = buffer.tobytes()

        # Yield the frame as byte stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

def imageCapture(img_path):
    results = model.predict(source=img_path, show=False)  # Perform detection on the image
    img = results[0].orig_img
    
    # Draw bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            class_name = model.names[cls]
            label = f'{class_name} {conf:.2f}'
            text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, thickness=1)

            c2_x = x1 + text_size[0] + 10
            c2_y = y1 - text_size[1] - 5
            cv2.rectangle(img, (x1, y1), (c2_x, c2_y), [0, 255, 0], -1, cv2.LINE_AA)
            cv2.putText(img, label, (x1, y1 - 2), 0, 0.7, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
    
    cv2.imwrite("static/result.jpg", img)  # Save the processed image