# Face Recognition System

This repository contains two face recognition/detection systems implemented in Python:

1. **Advanced Face Recognition System** (`face_recognition_system.py`) - Uses the `face_recognition` library for accurate face recognition
2. **Simple Face Detection** (`simple_face_detection.py`) - Uses OpenCV's Haar Cascades for basic face detection

## Features

### Advanced Face Recognition System
- Real-time face recognition using webcam
- Face recognition in static images
- Ability to learn and recognize multiple people
- High accuracy using deep learning models

### Simple Face Detection
- Real-time face detection using webcam
- Face detection in static images
- Eye detection within detected faces
- Lightweight and fast processing

## Installation

1. **Install Python 3.7 or higher**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note for Windows users:** You might need to install Visual Studio Build Tools or Visual Studio Community for compiling dlib. Alternatively, you can install a pre-compiled version:
   ```bash
   pip install dlib
   ```

## Usage

### Advanced Face Recognition System

1. **Run the main script:**
   ```bash
   python face_recognition_system.py
   ```

2. **Setup known faces:**
   - Create a `known_faces` directory (it will be created automatically)
   - Add face images of people you want to recognize
   - Name the files with the person's name (e.g., `john_doe.jpg`, `jane_smith.jpg`)
   - Each image should contain one clear face

3. **Choose your option:**
   - Option 1: Real-time recognition using webcam
   - Option 2: Recognize faces in a specific image file

### Simple Face Detection

1. **Run the simple detection script:**
   ```bash
   python simple_face_detection.py
   ```

2. **Choose your option:**
   - Option 1: Real-time detection using webcam
   - Option 2: Detect faces in a specific image file

## Requirements

- Python 3.7+
- OpenCV
- face_recognition library
- numpy
- A webcam (for real-time detection)

## File Structure

```
sanjana-demo/
├── face_recognition_system.py    # Advanced face recognition
├── simple_face_detection.py      # Basic face detection
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── known_faces/                  # Directory for known face images (created automatically)
```

## Tips for Better Results

### For Face Recognition:
- Use clear, well-lit photos for known faces
- Ensure faces are facing forward in training images
- Keep one face per training image
- Use high-quality images (at least 300x300 pixels)

### For Face Detection:
- Ensure good lighting conditions
- Face should be clearly visible and not too small
- Works best with frontal faces

## Troubleshooting

1. **Webcam not working:**
   - Check if webcam is connected and not being used by another application
   - Try changing the camera index in `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` or higher

2. **Installation issues:**
   - For Windows: Install Visual Studio Build Tools
   - For macOS: Install Xcode command line tools with `xcode-select --install`
   - For Linux: Install build essentials with `sudo apt-get install build-essential`

3. **Poor recognition accuracy:**
   - Add more training images per person
   - Ensure training images are clear and well-lit
   - Adjust the confidence threshold (currently set to 0.6)

## Performance Notes

- The advanced face recognition system processes every other frame for better performance
- You can adjust the frame processing frequency by modifying the `process_this_frame` logic
- For better performance on slower systems, you can reduce the video resolution

## License

This project is open source and available under the MIT License.
This is my first repo
<br>
added new changes
