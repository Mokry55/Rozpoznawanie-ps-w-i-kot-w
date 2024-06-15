import tensorflow as tf
import numpy as np
import tkinter as tk
from tkinter import filedialog
import logging
import os

# Configure logging
log_file = os.path.join(os.path.dirname(__file__), 'app.log')
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Example of logging usage
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

try:
    # Funkcje do przetwarzania pojedynczego obrazu i klasyfikacji
    def preprocess_image(image_path, target_size=(150, 150)):
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=target_size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalizacja
        return img_array

    def classify_image(model, image_path):
        img_array = preprocess_image(image_path)
        prediction = model.predict(img_array)
        if prediction[0] > 0.5:
            return 'Dog'
        else:
            return 'Cat'

    # Załaduj model
    model_path = os.path.join(os.path.dirname(__file__), 'best_model.keras')
    model = tf.keras.models.load_model(model_path)

    # Interfejs użytkownika
    def main():
        root = tk.Tk()
        root.withdraw()  # Ukryj główne okno

        while True:
            image_path = filedialog.askopenfilename()
            if image_path:
                result = classify_image(model, image_path)
                logging.info(f'The image is classified as: {result}')
                print(f'The image is classified as: {result}')
            else:
                logging.info("No image selected!")
                print("No image selected!")

            cont = input("Do you want to classify another image? (Y/N): ").strip().lower()
            if cont != 'y':
                break

    if __name__ == "__main__":
        main()

except Exception as e:
    logging.error("An exception occurred", exc_info=True)
