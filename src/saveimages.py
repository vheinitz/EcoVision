import cv2
import os
import time

basedir = "C:/Users/Emily/Documents/JuFo2023/JuFo2023Emily/img/"
# Initialize the camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    key = cv2.waitKey(1)

    if key != -1:
        # Convert ASCII code to character and use as directory name
        dir_name = basedir + chr(key)

        # Create directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Generate timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")

        # Construct filename and save image
        filename = f"{dir_name}/{timestamp}.png"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")

    # Break the loop if 'q' is pressed
    if key == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()