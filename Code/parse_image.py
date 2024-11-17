import cv2
import os

video_path = '../object_video.mp4'  # Replace with the path to your video file
output_folder = '../parsed_image'  # Folder to save the frames

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
    
    # Save the frame as a jpg file
    cv2.imwrite(frame_filename, frame)
    
    print(f"Saved: {frame_filename}") 
    
    frame_count += 1
    
cap.release()

print(f"All frames saved to {output_folder}.")