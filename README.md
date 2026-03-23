<<<<<<< HEAD
🚗 Driver Drowsiness Detection System (Python)

A real-time driver monitoring system that detects eye closure using a webcam and triggers an alert sound when drowsiness is detected. This project is designed to enhance road safety by warning drivers before fatigue leads to accidents.

📌 Features
👁️ Real-time eye tracking using computer vision
⚠️ Detects eye closure / drowsiness
🔊 Audio alert (beep sound) when eyes remain closed
🎥 Works with live webcam feed
⚡ Lightweight and fast execution
🛠️ Tech Stack
Python
OpenCV – for video processing
MediaPipe – for facial landmark detection
NumPy – for calculations
Pygame / Beep Sound Module – for alert system
=======
# Quick Start Guide - Driver Drowsiness Detection

## 30-Second Setup

### Step 1: Install Dependencies
Open PowerShell in the `Driving Simulator` folder and run:
```powershell
pip install -r requirements.txt
```

### Step 2: Download Model File
```powershell
python download_model.py
```
Wait for the download to complete (~5-10 minutes on average internet).

### Step 3: Run the Program
```powershell
python code.py
```

## That's It!

The program will:
- Show a video feed from your webcam
- Draw green boxes around your face
- Show Eye Aspect Ratio (EAR) values
- **Beep an alarm** if you close your eyes for ~1 second
- Stop the alarm when you open your eyes

## What You'll See

```
Left EAR: 0.45      ← Higher = eyes open, Lower = eyes closed
Right EAR: 0.42
Average EAR: 0.43
Closed Frames: 0/30 ← When this reaches 30→ ALARM!
```

## Exit

Press **'q'** to quit the program.

## Didn't Work?

1. **"No face detected"**: Move closer to camera, check lighting
2. **"Model not found"**: Run `python download_model.py` again
3. **dlib install fails**: Run `pip install dlib-wheel` instead

For detailed help, see `setup_guide.md`
>>>>>>> 7d04600 (Code uploaded)
