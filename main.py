import cv2
import mediapipe as mp
from utility import get_gesture
import requests

# Initialize MediaPipe Hands and drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

gesture = ""
cap = cv2.VideoCapture(0)

ESP32_IP = "http://192.168.138.226"  # Replace with actual ESP32 IP

gesture_map = {
    "Fist Closed": "fist_close",
    "Fist Open": "fist_open",
    "Thumb Up": "thumbs_up",
    "Thumb Down": "thumbs_down"
}

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        lst = []
        idx_lst = []
        frame_height, frame_width, _ = frame.shape

        answer_lst = get_gesture(results, frame, lst, idx_lst)

        if answer_lst is not None:
            gesture = answer_lst[0]
            lst = answer_lst[1]
            idx_lst = answer_lst[2]

            print(f"Detected Gesture: '{gesture}'")

            if gesture in gesture_map:
                try:
                    url = f"{ESP32_IP}/{gesture_map[gesture]}"
                    print("→ Sending URL:", url)
                    response = requests.get(url, timeout=1)
                    print("ESP32 Response:", response.text)
                except Exception as e:
                    print("Error sending gesture:", e)

            merged = list(zip(idx_lst, lst))
            for tup in merged:
                cv2.circle(frame, tup[1], 4, (0, 0, 255), -1)
                cv2.putText(frame, str(tup[0]), tup[1], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("Hand Landmarks", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows()
