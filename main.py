import cv2
import os

# The ASCII characters used to represent different brightness levels (from dark to light)
ASCII_CHARS = " .:-=+*#%@"

def frame_to_ascii(frame, cols=120):
    # Calculate target height to maintain a proper aspect ratio in the terminal
    # Terminal characters are vertically elongated, so we multiply by a scale factor (0.45)
    h, w, _ = frame.shape
    aspect_ratio = h / w
    rows = int(cols * aspect_ratio * 0.45)
    
    # Resize and convert the video frame to grayscale
    small_frame = cv2.resize(frame, (cols, rows))
    gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
    
    # Map each pixel's brightness (0-255) to an ASCII character
    ascii_frame = []
    num_chars = len(ASCII_CHARS)
    for row in gray_frame:
        line = "".join([ASCII_CHARS[int(pixel / 255 * (num_chars - 1))] for pixel in row])
        ascii_frame.append(line)
        
    return "\n".join(ascii_frame)

def main():
    # Initialize webcam (0 is usually the default built-in camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open your webcam.")
        return

    print("Starting ASCII Camera... Press 'q' to quit.")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Flip the frame horizontally for a natural "mirror" effect
            frame = cv2.flip(frame, 1)
            
            # Generate the ASCII art string
            ascii_art = frame_to_ascii(frame)
            
            # Clear the terminal screen dynamically (works on Windows and Mac/Linux)
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Print the text frame to the terminal
            print(ascii_art)
            
            # Drop OpenCV frame display window if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Safely release the camera when exiting
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
