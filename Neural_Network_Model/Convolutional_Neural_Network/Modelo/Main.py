import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import numpy as np
import Graficar_metricas_entrenamiento





def preprocess_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array


def create_model():
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False

    inputs = Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    outputs = Dense(10, activation='softmax')(x)

    model = Model(inputs, outputs)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.trainable = True
    return model


def save_model(model, model_path):
    model.save(model_path, save_format='tf')


def load_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print("Modelo cargado exitosamente")
        return model
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return None


def train_model(model, data_dir, batch_size=32, target_size=(224, 224), epochs=10):
    datagen = ImageDataGenerator(rescale=1. / 255, validation_split=0.2)

    train_gen = datagen.flow_from_directory(
        data_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_gen = datagen.flow_from_directory(
        data_dir,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    history = model.fit(train_gen, epochs=epochs, validation_data=val_gen)
    return history



def main():
    model_path = "modelo_IaOutfit.keras"
    data_dir = r'T:\CONTRUCCION DE SOFTWARE\ProyectoFinal\VIEW\Neural_Network_Model\DataSet'

    if not os.path.exists(model_path):
        model = create_model()
        history = train_model(model, data_dir)
        Graficar_metricas_entrenamiento.plot_training_history(history)
        save_model(model, model_path)
    else:
        # Resetear el gráfico de TensorFlow
        tf.keras.backend.clear_session()
        model = load_model(model_path)

    if model:
        image_path = r"T:\CONTRUCCION DE SOFTWARE\ProyectoFinal\VIEW\Neural_Network_Model\DataSet\Sandal\1_6cb8e1de-1962-4462-8d39-5216a64b962d.png"
        predictions = model.predict(image_path)
        print("Predicciones:", predictions)

if __name__ == '__main__':
    main()
