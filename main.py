import cv2
import numpy as np
import os

# ASCII characters used to represent different brightness levels (dark to light)
ASCII_CHARS = " .:-=+*#%@"


def frame_to_ascii(frame, cols=120):
    """Convert a video frame to ASCII art."""
    h, w, _ = frame.shape
    aspect_ratio = h / w
    # Terminal characters are vertically elongated, so adjust the height.
    rows = max(1, int(cols * aspect_ratio * 0.45))

    small_frame = cv2.resize(frame, (cols, rows))
    gray_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

    num_chars = len(ASCII_CHARS)
    ascii_frame = []
    for row in gray_frame:
        line = "".join(ASCII_CHARS[int(pixel / 255 * (num_chars - 1))] for pixel in row)
        ascii_frame.append(line)

    return "\n".join(ascii_frame)


def ascii_camera():
    """Show the webcam feed as ASCII art in the terminal."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open your webcam.")
        return

    print("Starting ASCII Camera. Press Ctrl+C to quit.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read a frame from the webcam.")
                break

            frame = cv2.flip(frame, 1)
            ascii_art = frame_to_ascii(frame)
            os.system("cls" if os.name == "nt" else "clear")
            print(ascii_art)
    except KeyboardInterrupt:
        print("\nASCII Camera stopped.")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def face_tracker():
    """Mark skin-colored regions that may resemble a face using simple HSV filters."""
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("Error: Could not access webcam device hardware.")
        return

    print("\n==============================================")
    print("Proportional Face Tracker Active (offline)")
    print("This uses skin-color and shape heuristics; it may mistake other objects for a face.")
    print("Press Q in the video window to quit safely.")
    print("==============================================")

    try:
        while True:
            success, frame = webcam.read()
            if not success:
                print("Error: Failed to grab frame stream.")
                break

            # Flip the frame for a natural mirror view.
            frame = cv2.flip(frame, 1)
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Basic skin-tone range in HSV; results vary with lighting and skin tones.
            lower_skin = np.array([0, 20, 70], dtype=np.uint8)
            upper_skin = np.array([20, 255, 255], dtype=np.uint8)
            skin_mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)

            # Remove small noise and smooth the mask.
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
            skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)

            contours, _ = cv2.findContours(
                skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)
                # Heuristic filters; these values depend on camera resolution and distance.
                if 5000 < area < 60000:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h
                    if 0.6 < aspect_ratio < 1.3:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(
                            frame,
                            "POSSIBLE FACE",
                            (x, max(y - 10, 0)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )

            cv2.imshow("Offline Skin-Color Face Tracker", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        webcam.release()
        cv2.destroyAllWindows()
        print("\nFace tracker shut down cleanly.")


def main():
    print("Choose a program:")
    print("1. ASCII Camera")
    print("2. Face Tracker")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        ascii_camera()
    elif choice == "2":
        face_tracker()
    else:
        print("Invalid choice. Please run the program again and enter 1 or 2.")


if __name__ == "__main__":
    main()
