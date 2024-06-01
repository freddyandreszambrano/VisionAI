import json
from tensorflow.keras.models import load_model
import tensorflow as tf

# Cargar el modelo
model = load_model('modelo_IaOutfit.keras')
# model.summary()

# Cargar el JSON de clasificación
with open('class_indices.json') as f:
    clases_json = json.load(f)

# Invertir el JSON para mapear índices a etiquetas
clases = {v: k for k, v in clases_json.items()}

# Predecir
imagen_path = r"C:\Users\USER\Downloads\camisa.jpg"
img = tf.keras.preprocessing.image.load_img(imagen_path, target_size=(224, 224))
x = tf.keras.preprocessing.image.img_to_array(img)
x = tf.expand_dims(x, axis=0)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)

# Predecir
preds = model.predict(x)
pred_class = tf.argmax(preds, axis=1).numpy()[0]
class_label = clases[pred_class]
print("La imagen pertenece a la clase:", class_label)
