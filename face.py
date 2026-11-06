import cv2
import numpy as np

# Open the connection to the default webcam (0)
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Error: Could not access webcam device hardware.")
    exit()

print("\n==============================================")
print("Proportional Face Tracker Active Completely Offline!")
print("Background doors and large walls will be ignored.")
print("Press the 'Q' key on your keyboard to quit safely.")
print("==============================================")

while True:
    success, frame = webcam.read()
    if not success:
        print("Error: Failed to grab frame stream.")
        break
        
    # Flip the frame for a natural mirror view
    frame = cv2.flip(frame, 1)
    
    # Convert the frame from BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Human skin tone boundaries in HSV color space
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Create a binary mask isolating skin colors
    skin_mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)
    
    # Clean up random dots in the background
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)
    
    # Find contours/shapes of all isolated color areas
    contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # FILTER: Exclude tiny noise AND massive background objects like doors
        # A human face close to a webcam typically ranges between 5,000 and 60,000 pixels.
        if 5000 < area < 60000:
            x, y, w, h = cv2.boundingRect(contour)
            
            # FILTER: Check the structural aspect ratio
            # A human face is slightly taller than it is wide. 
            # We ensure the ratio stays between a reasonable portrait shape.
            aspect_ratio = float(w) / h
            if 0.6 < aspect_ratio < 1.3:
                # Draw the green tracking rectangle over your face area
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "FACE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Render the video stream inside the pop-up window
    cv2.imshow('Offline Computer Vision System', frame)
    
    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up resources safely
webcam.release()
cv2.destroyAllWindows()
print("\nSystem shut down cleanly.")
