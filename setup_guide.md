# Driver Drowsiness Detection System - Setup Guide

## Overview
This program detects driver drowsiness by monitoring eye closure in real-time using your webcam. It triggers an alarm when eyes remain closed for more than 1-2 seconds.

## Prerequisites
- Python 3.7 or higher
- Webcam (integrated or external)
- Windows OS (uses winsound for alerts)

## Installation Steps

### 1. Install Python Dependencies
Open Command Prompt or PowerShell in the `Driving Simulator` directory and run:

```
pip install -r requirements.txt
```

**Note:** dlib requires a C++ compiler. If installation fails:
- Install Microsoft C++ Build Tools for Visual Studio
- Or use: `pip install dlib-wheel` (easier alternative)

### 2. Download dlib Face Landmark Model

The program requires the pre-trained facial landmark detector model. Follow these steps:

#### Option A: Manual Download (Recommended)
1. Download: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
2. Extract the file (use 7-Zip, WinRAR, or built-in extraction)
3. Place the extracted file `shape_predictor_68_face_landmarks.dat` in the **same directory** as `code.py`

#### Option B: Automatic Download (Python Script)
Create a file named `download_model.py` and run it:

```python
import bz2
import urllib.request
import os

url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
output_file = "shape_predictor_68_face_landmarks.dat.bz2"

print("Downloading model... This may take a few minutes.")
urllib.request.urlretrieve(url, output_file)

print("Extracting model...")
with bz2.open(output_file) as f_in:
    with open("shape_predictor_68_face_landmarks.dat", "wb") as f_out:
        f_out.write(f_in.read())

os.remove(output_file)
print("Done! Model is ready.")
```

Run with: `python download_model.py`

## Running the Program

```
python code.py
```

### Console Output
- Shows status messages (face detected, drowsiness alerts)
- Displays frame-by-frame analysis

### On-Screen Display
- **Left/Right EAR**: Eye Aspect Ratio for each eye (0 = closed, ~0.4+ = open)
- **Average EAR**: Combined eye closure metric
- **Closed Frames Counter**: How many consecutive frames eyes have been closed
- **Face Rectangle**: Green box around detected face
- **Eye Contours**: Yellow outlines around detected eyes
- **Alarm Alert**: Red box and "ALARM" text when drowsiness detected

### Controls
- **'q' key**: Quit the program
- **Ctrl+C**: Emergency exit

## How It Works

1. **Face Detection**: Uses dlib's frontal face detector to locate the driver's face
2. **Eye Localization**: Extracts the 68 facial landmarks and focuses on the eye regions
3. **EAR Calculation**: Computes the Eye Aspect Ratio using the formula:
   ```
   EAR = (||p2-p6|| + ||p3-p5||) / (2 * ||p1-p4||)
   ```
4. **Drowsiness Detection**: When average EAR drops below 0.3 for 30 consecutive frames (~1 second at 30fps), an alarm triggers
5. **Alert System**: Continuous beeping (1000 Hz) until eyes open again

## Configuration

You can adjust these parameters in `code.py`:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `EAR_THRESHOLD` | 0.3 | EAR value below which eyes are considered closed |
| `EAR_CONSECUTIVE_FRAMES` | 30 | Number of frames before triggering alarm |
| `ALARM_DURATION` | 0.5 | Duration of each beep in seconds |

**For more sensitive detection:** Lower `EAR_THRESHOLD` or decrease `EAR_CONSECUTIVE_FRAMES`

**For less sensitive detection:** Raise `EAR_THRESHOLD` or increase `EAR_CONSECUTIVE_FRAMES`

## Troubleshooting

### Issue: "No face detected"
- Ensure your face is visible to the webcam
- Check lighting conditions
- Position yourself directly facing the camera
- Restart the program

### Issue: "shape_predictor_68_face_landmarks.dat not found"
- Download the model file (see Setup Step 2)
- Verify the file is in the same directory as `code.py`
- Check for typos in filename

### Issue: dlib installation fails
- Install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or use `pip install dlib-wheel` as an easier alternative

### Issue: Alarm sounds continuously
- This is expected behavior - the driver's eyes must open to stop the alarm
- Open your eyes in front of the webcam
- Verify adequate lighting

### Issue: Webcam not opening
- Check if another application is using the webcam
- Close other video applications (Skype, browsers, etc.)
- Try unplugging and replugging the webcam

## Performance Tips

1. **Lighting**: Ensure good lighting for better face detection
2. **Distance**: Position 30-60 cm from webcam
3. **Angle**: Face the camera directly, not at an angle
4. **Processing**: Program uses resized frames (640x480) for speed on slower computers

## Safety Notes

- This system is for **alerting only** and should not be relied upon as the primary safety mechanism
- Always follow safe driving practices
- Pull over safely if drowsy
- Consider taking breaks during long drives

## File Structure

```
Driving Simulator/
├── code.py                              # Main program
├── requirements.txt                     # Dependencies
├── setup_guide.md                       # This file
├── shape_predictor_68_face_landmarks.dat # Model file (download separately)
└── download_model.py                    # Optional automatic downloader
```

## Support

For issues with:
- **dlib**: https://github.com/davisking/dlib
- **OpenCV**: https://docs.opencv.org/
- **scipy**: https://docs.scipy.org/

