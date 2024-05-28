import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D,Input,Concatenate
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow  import keras
import matplotlib.pyplot as plt


def preprocess_image(image_path):
    # Abrir la imagen y convertirla a formato RGB
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        # Redimensionar la imagen a 224x224
        img = img.resize((224, 224))
        return img



def Main():
   # Cargar MobileNetV2 preentrenado con pesos de ImageNet
    base_model = MobileNetV2(weights='imagenet', include_top=False)
    #base_model.summary()
    
    model_cnn = keras.Sequential()
    for layer in base_model.layers:
        # if 'conv' in layer.name or 'bn' in layer.name or 'relu' in layer.name:
        model_cnn.add(layer)
    #model_cnn.summary()
    
    #congelamos las capas de la red convolucional para que no se puedan entrenar
    for layer in model_cnn.layers:
        layer.trainable = False
    

    model_cnn.add(GlobalAveragePooling2D())
    model_cnn.add(Dense(1024, activation='relu'))  
    model_cnn.add(Dense(10, activation='softmax'))  
    
    # model_cnn.summary()
    
    directoria_data = r'T:\CONTRUCCION DE SOFTWARE\ProyectoFinal\VIEW\Neural_Network_Model\DataSet'

    #Generadores para sets de entrenamiento y pruebas
    batch_size=32
    target_size=(28, 28)
    datagen = ImageDataGenerator(rescale=1./255)
    print(datagen)
    dataset = datagen.flow_from_directory(
            directoria_data,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical',
            color_mode='rgb'
        )
   

    # data_gen_pruebas = datagen.flow_from_directory(
    #     directoria_data,
    #     target_size=(224, 224),
    #     batch_size=32,
    #     class_mode='categorical',
    #     subset='validation'
    # )
    
    model_cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    model_cnn.summary()
    
   
    #Entrenar el modelo
    EPOCAS = 10
    historial = model_cnn.fit(dataset, epochs=EPOCAS)
    # historial = model_cnn.fit(
    #     data_gen_entrenamiento, epochs=EPOCAS,validation_data=data_gen_pruebas
    # )
    
    Fn_graficas_precicion(historial)
        
    # Guardar el modelo
    model_cnn.save("modelo_IaOutit.h5")


def Fn_graficas_precicion(historial):
    acc = historial.history['accuracy']
    val_acc = historial.history['val_accuracy']

    loss = historial.history['loss']
    val_loss = historial.history['val_loss']

    rango_epocas = range(50)

    plt.figure(figsize=(8,8))
    plt.subplot(1,2,1)
    plt.plot(rango_epocas, acc, label='Precisión Entrenamiento')
    plt.plot(rango_epocas, val_acc, label='Precisión Pruebas')
    plt.legend(loc='lower right')
    plt.title('Precisión de entrenamiento y pruebas')

    plt.subplot(1,2,2)
    plt.plot(rango_epocas, loss, label='Pérdida de entrenamiento')
    plt.plot(rango_epocas, val_loss, label='Pérdida de pruebas')
    plt.legend(loc='upper right')
    plt.title('Pérdida de entrenamiento y pruebas')
    plt.show()
        

if __name__ == '__main__':
    Main()
