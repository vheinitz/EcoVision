import cv2
from keras.models import load_model
import numpy as np


class Detector:
    def __init__(self, model_path, labels_path):
        """
        Initialize the Object Detector with a model and labels.
        Args:
            model_path (str): Path to the model file.
            labels_path (str): Path to the labels file.
        """
        self.model = load_model(model_path, compile=False)
        self.class_names = open(labels_path, "r").readlines()

    def detect(self, frame):
        # Resize the frame to 224x224
        resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_LANCZOS4)

        # Convert the image to a numpy array and normalize it
        # OpenCV captures images in BGR format by default
        normalized_image_array = (resized_frame.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # Load the image into the array
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # Predicts the model
        prediction = self.model.predict(data)
        index = np.argmax(prediction)
        class_name = self.class_names[index].strip()
        confidence_score = prediction[0][index]
        return (class_name, confidence_score)


if __name__ == "__main__":

    d = Detector("../model/keras_model.h5", "../model/labels.txt")

    r = d.detect("NONE");