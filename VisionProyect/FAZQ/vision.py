import tensorflow as tf
import numpy as np
# from tensorflow import keras

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt



def entrenar_modelo():
    # Cargar el dataset Fashion MNIST
    fashion_mnist = tf.keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    # Normalizar los datos (transformarlos a valores de 0 a 1)
    train_images = train_images / 255.0
    test_images = test_images / 255.0
    # Reajustar las imágenes para que tengan un solo canal de color
    train_images = train_images[..., tf.newaxis]
    test_images = test_images[..., tf.newaxis]
    model = tf.keras.models.Sequential([
      tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
      tf.keras.layers.MaxPooling2D((2, 2)),
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
      tf.keras.layers.MaxPooling2D((2, 2)),
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(64, activation='relu'),
      tf.keras.layers.Dense(10) # 10 clases en Fashion MNIST
    ])



    model.compile(optimizer='adam', #tambien podemor usar el algoritmo sgd
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])
    #Entrenar el modelo 
    model.fit(train_images, train_labels, epochs=10, validation_split=0.2)
    # Evaluar la precision 
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)

if __name__ == "__main__":
    # Ejecutar el entrenamiento solo si este archivo se ejecuta directamente
    modelo_entrenado = entrenar_modelo()


# Guardar el modelo en un archivo ---FALTA COMPLETAR ---




# Realizar predicciones en el conjunto de test
# predictions = model.predict(test_images)
# predicted_classes = np.argmax(predictions, axis=1)     
# # Las etiquetas verdaderas están en test_labels
# true_classes = test_labels

# Crear la MATRIZ de confusión
# cm = confusion_matrix(true_classes, predicted_classes)
# class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
#                'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Visualizar la matriz de confusión
# plt.figure(figsize=(10,8))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
# plt.xlabel('Predicted Label')
# plt.ylabel('True Label')
# plt.title('Confusion Matrix')
# plt.show()



# Ejecutar la aplicación de la interfaz de usuario
