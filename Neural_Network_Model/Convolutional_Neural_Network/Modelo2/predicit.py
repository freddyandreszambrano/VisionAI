import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import requests
from io import BytesIO

# Función para cargar el modelo
def cargar_modelo(ruta_modelo):
    modelo = load_model(ruta_modelo)
    return modelo

# Función para preprocesar una imagen desde una URL
def preprocesar_imagen_desde_url(url_imagen, target_size=(28, 28)):
    respuesta = requests.get(url_imagen)
    img = Image.open(BytesIO(respuesta.content)).convert('RGB')
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalización
    return img_array

# Función para preprocesar una imagen desde un archivo local
def preprocesar_imagen_desde_archivo(ruta_imagen, target_size=(28, 28)):
    img = Image.open(ruta_imagen).convert('RGB')
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalización
    return img_array

# Función para predecir la clase de una imagen
def predecir_imagen(modelo, img_array):
    prediccion = modelo.predict(img_array)
    clase_predicha = np.argmax(prediccion, axis=1)
    return clase_predicha[0]

# Función principal para cargar el modelo y predecir
def main():
    ruta_modelo = 'modelo.keras'  
    modelo = cargar_modelo(ruta_modelo)
    
    metodo = input("¿Deseas predecir una imagen desde una URL o desde un archivo local? (Escribe 'url' o 'archivo'): ").strip().lower()
    
    if metodo == 'url':
        url_imagen = input("Introduce la URL de la imagen: ").strip()
        img_array = preprocesar_imagen_desde_url(url_imagen)
    elif metodo == 'archivo':
        ruta_imagen = input("Introduce la ruta del archivo de imagen: ").strip()
        img_array = preprocesar_imagen_desde_archivo(ruta_imagen)
    else:
        print("Método no reconocido. Por favor, escribe 'url' o 'archivo'.")
        return
    
    clase = predecir_imagen(modelo, img_array)
    print(f'La clase predicha para la imagen es: {clase}')

if __name__ == '__main__':
    main()
