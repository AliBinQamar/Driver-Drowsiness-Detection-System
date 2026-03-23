```markdown
# 🚗 Driver Drowsiness Detection System

A real-time **driver drowsiness detection system** built with Python that monitors eye activity using a webcam and alerts the driver when signs of fatigue are detected.

---

## 📌 Overview

This project uses **computer vision and facial landmark detection** to track eye movement. If the driver’s eyes remain closed for a certain duration, the system triggers an alert sound to prevent potential accidents.

---

## ✨ Features

- 👁️ Real-time eye detection  
- ⚠️ Detects drowsiness based on eye closure  
- 🔊 Instant alert (beep sound)  
- 🎥 Live webcam monitoring  
- ⚡ Fast and lightweight  

---

## 🛠️ Technologies Used

- Python  
- OpenCV  
- MediaPipe  
- NumPy  
- Pygame (for sound alerts)  

---

## 📂 Project Structure

```

Driver-Drowsiness-Detection-System/
│
├── code.py              # Main Python script
├── alarm.wav            # Alert sound file
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── assets/              # Optional (screenshots/videos)

````

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/AliBinQamar/Driver-Drowsiness-Detection-System.git
cd Driver-Drowsiness-Detection-System
````

2. Create virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python code.py
```

* Make sure your webcam is enabled
* Sit in front of the camera
* The system will monitor your eyes in real-time
* If drowsiness is detected → 🚨 alert sound will trigger

---

## 🧠 How It Works

* Detects face using MediaPipe
* Tracks eye landmarks
* Calculates **Eye Aspect Ratio (EAR)**
* If EAR drops below threshold → eyes considered closed
* If closed for a few seconds → alert is triggered

---

## ⚠️ Limitations

* Requires proper lighting
* May be less accurate with glasses
* Depends on webcam quality
* Not a replacement for professional safety systems

---

## 🚀 Future Improvements

* Head pose detection
* Mobile app version
* AI-based fatigue prediction
* Integration with smart vehicles
* Dashboard for analytics

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Make changes
4. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👤 Author

**Ali Qamar**
GitHub: [https://github.com/AliBinQamar](https://github.com/AliBinQamar)

```
```
