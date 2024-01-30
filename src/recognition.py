import cv2
from keras.models import load_model
#from PIL import Image, ImageOps
import numpy as np

# Load the model
model = load_model("../model/keras_model.h5", compile=False)

# Load the labels
class_names = open("../model/labels.txt", "r").readlines()

# Initialize the camera
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, flipped_frame = cap.read()
    frame = cv2.flip(flipped_frame, 1)

    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Resize the frame to 224x224
    resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_LANCZOS4)

    # Convert the image to a numpy array and normalize it
    # OpenCV captures images in BGR format by default
    normalized_image_array = (resized_frame.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Convert the image to a numpy array and normalize it
    #image_array = np.asarray(pil_image)
    #normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

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