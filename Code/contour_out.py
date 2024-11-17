import cv2
import os

video_path = '../object_video.mp4'  
# output_folder = '../contour_image'  
output_video_path = '../contour.mp4'  

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

    # Find contours in the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original frame with a light green color (BGR format)
    contour_frame = frame.copy()  
    cv2.drawContours(contour_frame, contours, -1, (144, 238, 144), 5)  

    # Save the contour image
    # contour_filename = os.path.join(output_folder, f"contour_{frame_count:04d}.jpg")
    # cv2.imwrite(contour_filename, contour_frame)
    # print(f"Saved contour image: {contour_filename}")
    
    # Write the frame with contours to the output video
    out_video.write(contour_frame)

    frame_count += 1

cap.release()
out_video.release()

print(f"Contour video saved to {output_video_path}.")