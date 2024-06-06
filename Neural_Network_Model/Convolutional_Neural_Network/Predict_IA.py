import json
from tensorflow.keras.models import load_model # type: ignore
import tensorflow as tf


# Predecir
def Fn_Predecir(x, model, clases):
    preds = model.predict(x)
    pred_class = tf.argmax(preds, axis=1).numpy()[0]
    class_label = clases[pred_class]
    print("La imagen pertenece a la clase:", class_label)
    return class_label
    
def Fn_Mapear_json():
    with open('class_indices.json') as f:
        clases_json = json.load(f)
    clases = {v: k for k, v in clases_json.items()}
    return clases

def Fn_Main(Ruta_img):
    model = load_model('modelo_IaOutfit.h5')
    class_json = Fn_Mapear_json()
    imagen_path = Ruta_img
    img = tf.keras.preprocessing.image.load_img(imagen_path, target_size=(224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    resultado_prediccion = Fn_Predecir(x, model, class_json)
    return resultado_prediccion
    
    
    
if __name__ == '__main__':
    ruta = r"C:\Users\USER\Downloads\zapato.jpg"
    Fn_Main(ruta)