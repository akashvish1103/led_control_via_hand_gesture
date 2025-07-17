# 🤖 Hand Gesture Controlled LED with OpenCV, MediaPipe, and ESP32 (WiFi)

This project demonstrates a computer vision-based system that detects **hand gestures using OpenCV and MediaPipe** to control a **Wi-Fi connected LED via ESP32**. 

The LED responds to the following gestures:
- 👍 **Thumbs Up** → Increase brightness
- 👎 **Thumbs Down** → Decrease brightness
- 🖐️ **Fist Open** → Turn ON the LED
- ✊ **Fist Closed** → Turn OFF the LED

---

## 🔧 Technologies Used

- 🐍 **Python**
- 📸 **OpenCV** — Image processing and webcam feed
- 🤚 **MediaPipe Hands** — Hand landmark detection
- 🔌 **ESP32 (Wi-Fi)** — Receives commands and controls LED
- 🌐 **HTTP Requests** — Communication between Python and ESP32
- 💡 **LED with PWM** — For brightness control

---

## 📷 Gesture Mapping Logic

| Gesture       | Action              |
|---------------|---------------------|
| Thumbs Up     | Increase brightness |
| Thumbs Down   | Decrease brightness |
| Fist Open     | Turn ON the LED     |
| Fist Closed   | Turn OFF the LED    |

---

## 🛠️ How It Works

1. The webcam captures the live video stream.
2. MediaPipe detects and classifies hand gestures in real-time.
3. Detected gestures are mapped to corresponding commands.
4. Python sends an HTTP request to the ESP32’s IP address.
5. ESP32 processes the request and updates the LED state accordingly.

---

## ⚙️ Setup Instructions

### 🖥️ Python + OpenCV + MediaPipe (PC Side)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gesture-led-esp32.git
   cd gesture-led-esp32
