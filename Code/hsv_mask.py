import cv2
import os

video_path = '../object_video.mp4'  
# output_folder = '../masked_red_image'  
output_video_path = '../masked_red.mp4'  

# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_rate = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
out_video = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

lower_red1 = (0, 120, 70)  # Lower bound of red (HSV)
upper_red1 = (10, 255, 255)  # Upper bound of red (HSV)

lower_red2 = (170, 120, 70)  # Lower bound of red (second range)
upper_red2 = (180, 255, 255)  # Upper bound of red (second range)

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    
    red_mask = cv2.bitwise_or(mask1, mask2)

    red_highlighted = cv2.bitwise_and(frame, frame, mask=red_mask)

    # Optionally: Convert the frame to grayscale (black and white) to see just the red parts on a black background
    red_highlighted_bw = cv2.cvtColor(red_highlighted, cv2.COLOR_BGR2GRAY)
    red_highlighted_colored = cv2.cvtColor(red_highlighted_bw, cv2.COLOR_GRAY2BGR)

    # Write the processed frame to the output video
    out_video.write(red_highlighted_colored)

    # Save the red mask (optional)
    # mask_filename = os.path.join(output_folder, f"red_mask_{frame_count:04d}.jpg")
    # cv2.imwrite(mask_filename, red_mask)
    # print(f"Saved red mask: {mask_filename}")
    
    frame_count += 1

# Release the video capture and writer objects
cap.release()
out_video.release()

print(f"Video with red masks saved to {output_video_path}.")
