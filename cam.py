import cv2
import mediapipe as mp
import time

# --- Configuration ---
# Sensitivity: Lower number = more strict (e.g., 0.02), Higher = more relaxed (e.g., 0.08)
POSTURE_THRESHOLD = 0.05 
ALERT_COLOR = (0, 0, 255)  # Red (BGR)
NORMAL_COLOR = (0, 255, 0) # Green (BGR)

# Initialize AI models
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

def detect_posture():
    cap = cv2.VideoCapture(0)
    
    print("AI Camera Started. Press 'q' to quit.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Flip for natural 'mirror' view and convert for AI processing
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            # Draw AI skeleton overlay
            mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Get key coordinates
            lm = results.pose_landmarks.landmark
            nose_y = lm[mp_pose.PoseLandmark.NOSE].y
            l_sh_y = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            r_sh_y = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
            shoulder_avg_y = (l_sh_y + r_sh_y) / 2

            # --- Alert Logic ---
            # If the nose falls too close to the shoulder line (slouching)
            if nose_y > (shoulder_avg_y - POSTURE_THRESHOLD):
                # Visual Alert: Thick Red Border and Text
                cv2.rectangle(frame, (0,0), (frame.shape[1], frame.shape[0]), ALERT_COLOR, 15)
                cv2.putText(frame, "!!! ALERT: BAD POSTURE !!!", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, ALERT_COLOR, 3)
            else:
                cv2.putText(frame, "Posture: Good", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, NORMAL_COLOR, 2)

        else:
            cv2.putText(frame, "No Student Detected", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Show output
        cv2.imshow('AI Posture Cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_posture()
