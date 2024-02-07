import cv2
import serial
from keras.models import load_model
import numpy as np
from recognition import Detector

bandController = '/dev/ttyACM0'
kameraID = 1

try:
    MySerialInterface = serial.Serial(bandController)  #
except:
    MySerialInterface=None
    print("Fehler! Kein Bandkontroller (Arduino)")
    exit(2)

#Beide Pusher in Parkposition
MySerialInterface.write(b'2:5;')
MySerialInterface.write(b'3:5;')

try:
    MyCamera = cv2.VideoCapture(kameraID)
except:
    MyCamera=None
    print("Fehler! Keine Kamera")
    exit(2)


detector = Detector("../model/keras_model.h5", "../model/labels.txt")


# Check if the camera opened successfully
if not MyCamera.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, flipped_frame = MyCamera.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv2.flip(flipped_frame, 1)

    class_name, confidence_score = detector.detect(frame)


    # Display the prediction and confidence score on the frame
    cv2.putText(frame, f"{class_name}: {confidence_score:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
