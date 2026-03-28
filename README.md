This project is an AI-powered monitoring system designed to promote healthy study habits and track student engagement. Using Computer Vision and MediaPipe, the system detects a student's posture in real-time and provides instant visual alerts if slouching or poor posture is detected.🚀 FeaturesReal-time Posture Detection: Monitors the alignment of the head and shoulders to identify slouching.Instant Visual Alerts: Flashes a red warning border and on-screen text when poor posture is detected.Live Dashboard: A web-based interface built with Streamlit to track engagement metrics and posture history.Lightweight AI Engine: Powered by MediaPipe Pose, ensuring high performance even on standard laptops or Raspberry Pi.Engagement Tracking: Provides a visual line chart of the student's focus levels over time.🛠️ Tech StackLanguage: Python 3.10+AI Framework: MediaPipe (Pose Landmark Detection)Library: OpenCV (Video processing)Dashboard: Streamlit (Web interface)Environment: Windows / Linux / macOS💻 Installation & Setup1. Clone the RepositoryBashgit clone https://github.com/yourusername/ai-student-camera.git
cd ai-student-camera
2. Create a Virtual Environment (Recommended)PowerShell# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install opencv-python mediapipe streamlit numpy
🏃 How to RunOption A: Lightweight Camera View (cam.py)Run this for a simple, direct camera feed with posture alerts.Bashpython cam.py
Option B: Full Web Dashboard (app.py)Run this to launch the interactive dashboard in your browser.Bashstreamlit run app.py
📊 How It WorksThe system utilizes the MediaPipe Pose model to identify 33 body landmarks.Landmark Extraction: It tracks the coordinates of the Nose and Shoulders.Calculation: It calculates the vertical distance ($y$-axis) between the nose and the average shoulder level.Thresholding: If the nose drops below a specific safety threshold ($y_{\text{nose}} > y_{\text{shoulder}} - \text{threshold}$), the system triggers an alert.Feedback: The UI provides real-time feedback, helping the student maintain an upright, healthy position.📂 Project StructurePlaintext├── cam.py            # Standalone posture detection script
├── app.py            # Streamlit dashboard application
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
