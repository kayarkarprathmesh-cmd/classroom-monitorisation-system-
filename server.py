import cv2
import json
from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Global variable to store the latest score for the dashboard
current_engagement = 0

def generate_frames():
    global current_engagement
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # 1. Run AI Detection
            results = model(frame, stream=True, verbose=False)
            
            found_person = False
            for r in results:
                if len(r.boxes) > 0:
                    found_person = True
                    for box in r.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 204), 2)

            # 2. Logic for Attention Score
            # If person is detected, score is high; if not, it drops
            if found_person:
                current_engagement = min(100, current_engagement + 5)
            else:
                current_engagement = max(0, current_engagement - 10)

            # 3. Encode for Web Streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Route 1: The Main Dashboard Page
@app.route('/')
def index():
    return render_template('index.html')

# Route 2: The Video Stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route 3: The Data API for the Chart
@app.route('/api/stats')
def stats():
    return jsonify({"average": current_engagement})

if __name__ == "__main__":
    # Use threaded=True to handle video and API requests at the same time
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
