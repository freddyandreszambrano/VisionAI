import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

longitud, altura = 150, 150
modelo = 'modelo.keras'

# Cargar el modelo
cnn = load_model(modelo)

# Función de predicción
def predict(file):
    x = load_img(file, target_size=(longitud, altura))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    x /= 255.0  # Normalizar la imagen

    array = cnn.predict(x)
    result = array[0]
    answer = np.argmax(result)
    
    # Mapear los índices a las clases correspondientes
    clases = ["Ankle boot", "Bag", "Coat", "Dress", "Pullover", "Sandal", "Shirt", "Sneaker", "T-shirt", "Trouser"]  # Asegúrate de que esto coincida con tus clases
    if answer < len(clases):
        print(f"pred: {clases[answer]}")
    else:
        print("Clase desconocida")

    return answer

# Ruta de la imagen para la predicción
ruta_imagen = r"C:\Users\USER\Downloads\sandalia.jpg"
predict(ruta_imagen)
