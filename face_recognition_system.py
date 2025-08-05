import cv2
import face_recognition
import numpy as np
import os
from pathlib import Path

class FaceRecognitionSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def load_known_faces(self, known_faces_dir="known_faces"):
        """
        Load known faces from a directory containing images
        Each image should be named with the person's name (e.g., "john_doe.jpg")
        """
        if not os.path.exists(known_faces_dir):
            print(f"Creating directory: {known_faces_dir}")
            os.makedirs(known_faces_dir)
            print(f"Please add face images to the '{known_faces_dir}' directory")
            return

        for image_file in Path(known_faces_dir).glob("*.jpg"):
            # Load image
            image = face_recognition.load_image_file(str(image_file))
            
            # Get face encoding
            face_encodings = face_recognition.face_encodings(image)
            
            if face_encodings:
                # Use the first face found in the image
                face_encoding = face_encodings[0]
                
                # Get person's name from filename (without extension)
                name = image_file.stem.replace("_", " ").title()
                
                # Store the face encoding and name
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)
                
                print(f"Loaded face for: {name}")
            else:
                print(f"No face found in {image_file}")

    def recognize_faces_in_image(self, image_path):
        """
        Recognize faces in a single image
        """
        # Load the image
        image = face_recognition.load_image_file(image_path)
        
        # Find face locations and encodings
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Convert to BGR for OpenCV
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Loop through each face in the image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                name = self.known_face_names[best_match_index]
            
            # Draw rectangle around face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw label with name
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(image, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
        
        return image

    def real_time_face_recognition(self):
        """
        Real-time face recognition using webcam
        """
        # Initialize webcam
        video_capture = cv2.VideoCapture(0)
        
        if not video_capture.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("Starting real-time face recognition. Press 'q' to quit.")
        
        while True:
            # Grab a single frame
            ret, frame = video_capture.read()
            
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Only process every other frame to save time
            if self.process_this_frame:
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                
                # Convert BGR to RGB
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find face locations and encodings
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                
                self.face_names = []
                for face_encoding in self.face_encodings:
                    # Check if the face matches any known faces
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    
                    # Use the known face with the smallest distance
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index] and face_distances[best_match_index] < 0.6:
                        name = self.known_face_names[best_match_index]
                    
                    self.face_names.append(name)
            
            self.process_this_frame = not self.process_this_frame
            
            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)
            
            # Display the resulting image
            cv2.imshow('Face Recognition', frame)
            
            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

def main():
    # Create face recognition system
    fr_system = FaceRecognitionSystem()
    
    # Load known faces
    fr_system.load_known_faces()
    
    if not fr_system.known_face_encodings:
        print("\nNo known faces loaded. Please add face images to the 'known_faces' directory.")
        print("Each image should contain one face and be named with the person's name (e.g., 'john_doe.jpg')")
        return
    
    while True:
        print("\nFace Recognition System")
        print("1. Real-time face recognition (webcam)")
        print("2. Recognize faces in image file")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            fr_system.real_time_face_recognition()
        
        elif choice == '2':
            image_path = input("Enter path to image file: ").strip()
            if os.path.exists(image_path):
                result_image = fr_system.recognize_faces_in_image(image_path)
                cv2.imshow('Face Recognition Result', result_image)
                print("Press any key to continue...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Image file not found!")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
