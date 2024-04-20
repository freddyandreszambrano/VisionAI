import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

from vision import entrenar_modelo


# Cargar el modelo previamente entrenado
model = entrenar_modelo()

def preprocess_image(image):
    # Convertir la imagen a una matriz NumPy
     # Convertir la imagen a escala de grises
    image_gray = image.convert('L')
    # Normalizar y ajustar el tamaño de la imagen
    image_resized = image_gray.resize((28, 28))
    image_normalized = np.array(image_resized) / 255.0
    image_normalized = image_normalized[..., np.newaxis]
    image_normalized = np.expand_dims(image_normalized, axis=0)
    return image_normalized


def load_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        temp_image_path = 'temp_image.jpg'
        Image.open(file_path).save(temp_image_path)
        image = Image.open(temp_image_path)
        image = preprocess_image(image)
        #image_for_display = Image.fromarray((image[0] * 255).astype(np.uint8))  # Convertir imagen procesada a valores de 0 a 255
        image_for_display = Image.fromarray((image[0, ..., 0] * 255).astype(np.uint8)) 
        image_for_display = image_for_display.resize((200, 200))  # Redimensionar la imagen para mostrarla
        photo = ImageTk.PhotoImage(image_for_display)
        label.configure(image=photo)
        label.image = photo
        predict_button.config(state=tk.NORMAL)

def predict_image():
    global model
    global label_result
    image = preprocess_image(Image.open(filedialog.askopenfilename()))
    prediction = model.predict(image)
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    predicted_class = class_names[np.argmax(prediction)]
    label_result.config(text=f"Prediction: {predicted_class}")

root = tk.Tk()
root.title("Fashion Image Classifier")

load_button = tk.Button(root, text="Cargar Imagen", command=load_image)
load_button.pack()

label = tk.Label(root)
label.pack()

predict_button = tk.Button(root, text="Predecir", command=predict_image, state=tk.DISABLED)
predict_button.pack()

label_result = tk.Label(root, text="")
label_result.pack()

root.mainloop()
