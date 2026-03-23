"""
Driver Drowsiness Detection System
Using webcam to detect when driver's eyes are closed for too long
and trigger an alarm alert.
"""

import cv2
import mediapipe as mp
import numpy as np
import winsound
import threading
import time
from scipy.spatial import distance

# ==================== CONFIGURATION ====================
EAR_THRESHOLD = 0.3  # Eye Aspect Ratio threshold (below this = eyes closed)
EAR_CONSECUTIVE_FRAMES = 30  # Frames to consider eyes closed (at ~30fps = ~1 second)
ALARM_DURATION = 0.5  # Duration of each alarm beep in seconds

# ==================== HELPER FUNCTIONS ====================

def calculate_eye_aspect_ratio(eye_landmarks):
    """
    Calculate Eye Aspect Ratio (EAR) from eye landmarks.
    
    EAR formula:
    EAR = ||p2 - p6|| + ||p3 - p5|| / (2 * ||p1 - p4||)
    
    Where p1-p6 are the eye landmark coordinates.
    Values closer to 0 indicate closed eyes.
    
    Args:
        eye_landmarks: Array of 6 eye landmark coordinates
    
    Returns:
        float: Eye Aspect Ratio value
    """
    # Calculate distances between vertical eye landmarks
    vertical_distance_1 = distance.euclidean(eye_landmarks[1], eye_landmarks[5])
    vertical_distance_2 = distance.euclidean(eye_landmarks[2], eye_landmarks[4])
    
    # Calculate distance between horizontal eye landmarks
    horizontal_distance = distance.euclidean(eye_landmarks[0], eye_landmarks[3])
    
    # Calculate EAR
    ear = (vertical_distance_1 + vertical_distance_2) / (2.0 * horizontal_distance)
    return ear


def trigger_alarm(duration=ALARM_DURATION):
    """
    Play a beep alarm sound using Windows winsound module.
    Runs in a separate thread to not block video capture.
    
    Args:
        duration: Duration of the beep in seconds
    """
    try:
        # Beep: frequency=1000 Hz, duration in milliseconds
        winsound.Beep(1000, int(duration * 1000))
    except Exception as e:
        print(f"Error playing alarm: {e}")


def play_alarm_continuously(stop_event, interval=0.3):
    """
    Play alarm beeps continuously until stop_event is set.
    Runs in a separate thread.
    
    Args:
        stop_event: threading.Event to signal when to stop
        interval: Interval between beeps in seconds
    """
    while not stop_event.is_set():
        trigger_alarm(ALARM_DURATION)
        time.sleep(interval)


def draw_face_and_eyes(frame, landmarks_list, ear_left, ear_right):
    """
    Draw landmarks and eyes on the video frame.
    Also display EAR values and status.

    Args:
        frame: Video frame to draw on
        landmarks_list: List of MediaPipe normalized landmarks
        ear_left: Left eye aspect ratio
        ear_right: Right eye aspect ratio

    Returns:
        frame: Modified frame with drawings
    """
    h, w = frame.shape[:2]

    # Left eye indices in MediaPipe face mesh
    left_eye_indices = [33, 160, 158, 133, 153, 144]
    # Right eye indices in MediaPipe face mesh
    right_eye_indices = [362, 385, 387, 263, 373, 380]

    # Convert normalized coordinates to pixel coordinates
    left_eye = np.array([(int(landmarks_list[i].x * w), int(landmarks_list[i].y * h))
                         for i in left_eye_indices])
    right_eye = np.array([(int(landmarks_list[i].x * w), int(landmarks_list[i].y * h))
                          for i in right_eye_indices])

    # Draw contours around eyes
    cv2.polylines(frame, [left_eye], True, (0, 255, 255), 2)
    cv2.polylines(frame, [right_eye], True, (0, 255, 255), 2)

    # Display EAR values
    cv2.putText(frame, f"Left EAR: {ear_left:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, f"Right EAR: {ear_right:.2f}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Display average EAR
    avg_ear = (ear_left + ear_right) / 2
    cv2.putText(frame, f"Average EAR: {avg_ear:.2f}", (10, 110),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return frame


def main():
    """
    Main function to run the drowsiness detection system.
    """
    print("Initializing Driver Drowsiness Detection System...")

    # Initialize MediaPipe face detection and face mesh
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh

    face_detection = mp_face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    )
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Cannot open webcam!")
        return

    print("Webcam initialized successfully.")
    print("Press 'q' to quit.")

    # Variables to track drowsiness
    consecutive_closed_frames = 0
    alarm_active = False
    alarm_stop_event = threading.Event()
    alarm_thread = None

    # Get frame properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # Eye landmarks indices in MediaPipe face mesh
    left_eye_indices = [33, 160, 158, 133, 153, 144]
    right_eye_indices = [362, 385, 387, 263, 373, 380]

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Failed to read frame from webcam!")
                break

            # Resize frame for faster processing (optional)
            frame = cv2.resize(frame, (640, 480))
            h, w, c = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            face_detection_results = face_detection.process(rgb_frame)

            if face_detection_results.detections is None or len(face_detection_results.detections) == 0:
                # No face detected
                cv2.putText(frame, "No face detected", (10, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                consecutive_closed_frames = 0
            else:
                # Process face mesh for landmarks
                face_mesh_results = face_mesh.process(rgb_frame)

                if face_mesh_results.multi_face_landmarks and len(face_mesh_results.multi_face_landmarks) > 0:
                    landmarks = face_mesh_results.multi_face_landmarks[0].landmark

                    # Extract eye regions
                    left_eye = np.array([(landmarks[i].x, landmarks[i].y) for i in left_eye_indices])
                    right_eye = np.array([(landmarks[i].x, landmarks[i].y) for i in right_eye_indices])

                    # Calculate Eye Aspect Ratio for both eyes
                    ear_left = calculate_eye_aspect_ratio(left_eye)
                    ear_right = calculate_eye_aspect_ratio(right_eye)
                    avg_ear = (ear_left + ear_right) / 2

                    # Draw face and eyes on frame
                    frame = draw_face_and_eyes(frame, landmarks, ear_left, ear_right)

                    # Check if eyes are closed
                    if avg_ear < EAR_THRESHOLD:
                        consecutive_closed_frames += 1
                    else:
                        consecutive_closed_frames = 0
                        # Stop alarm if eyes are open
                        if alarm_active:
                            alarm_stop_event.set()
                            if alarm_thread and alarm_thread.is_alive():
                                alarm_thread.join(timeout=1)
                            alarm_active = False
                            alarm_stop_event.clear()

                    # Trigger alarm if eyes closed for too long
                    if consecutive_closed_frames >= EAR_CONSECUTIVE_FRAMES and not alarm_active:
                        print(f"⚠️  DROWSINESS DETECTED! Eyes closed for {consecutive_closed_frames} frames")
                        alarm_active = True
                        alarm_stop_event.clear()
                        # Start alarm in background thread
                        alarm_thread = threading.Thread(target=play_alarm_continuously,
                                                       args=(alarm_stop_event,))
                        alarm_thread.daemon = True
                        alarm_thread.start()

                    # Display alarm status
                    if alarm_active:
                        cv2.putText(frame, "ALARM: EYES CLOSED!", (10, frame.shape[0] - 60),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]),
                                     (0, 0, 255), 3)

                    # Display closed frames counter
                    cv2.putText(frame, f"Closed Frames: {consecutive_closed_frames}/{EAR_CONSECUTIVE_FRAMES}",
                                (10, frame.shape[0] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # Display instructions
            cv2.putText(frame, "Press 'q' to quit", (frame.shape[1] - 250, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            # Show frame
            cv2.imshow("Driver Drowsiness Detection", frame)

            # Exit on 'q' key press
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nShutting down...")
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        # Cleanup
        if alarm_active:
            alarm_stop_event.set()
            if alarm_thread and alarm_thread.is_alive():
                alarm_thread.join(timeout=1)

        face_detection.close()
        face_mesh.close()
        cap.release()
        cv2.destroyAllWindows()
        print("Program terminated.")


# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    main()
