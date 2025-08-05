#!/usr/bin/env python3
"""
Setup script for Face Recognition System
This script helps install dependencies and set up the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python {version.major}.{version.minor} detected. Python 3.7+ is required.")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("✗ requirements.txt not found")
        return False
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements")

def create_directories():
    """Create necessary directories"""
    known_faces_dir = Path("known_faces")
    if not known_faces_dir.exists():
        known_faces_dir.mkdir()
        print("✓ Created 'known_faces' directory")
        
        # Create a sample instruction file
        instruction_file = known_faces_dir / "README.txt"
        with open(instruction_file, 'w') as f:
            f.write("""How to add known faces:

1. Add clear face images to this directory
2. Name files with the person's name (e.g., 'john_doe.jpg')
3. Use formats: .jpg, .jpeg, .png
4. Ensure each image contains only one face
5. Use well-lit, frontal face photos for best results

Example filenames:
- john_smith.jpg
- jane_doe.png
- alice_johnson.jpeg
""")
        print("✓ Created instruction file in known_faces directory")
    else:
        print("✓ 'known_faces' directory already exists")

def check_webcam():
    """Check if webcam is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Webcam is accessible")
                return True
            else:
                print("⚠ Webcam detected but unable to read frames")
                return False
        else:
            print("⚠ No webcam detected or webcam is in use")
            return False
    except ImportError:
        print("⚠ Cannot check webcam (OpenCV not installed yet)")
        return False

def main():
    print("Face Recognition System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n⚠ Some packages failed to install. You may need to:")
        print("1. Install Visual Studio Build Tools (Windows)")
        print("2. Install Xcode command line tools (macOS)")
        print("3. Install build-essential (Linux)")
        print("\nThen run this setup script again.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check webcam (after OpenCV is installed)
    check_webcam()
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Add face images to the 'known_faces' directory")
    print("2. Run: python face_recognition_system.py")
    print("   or: python simple_face_detection.py")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
