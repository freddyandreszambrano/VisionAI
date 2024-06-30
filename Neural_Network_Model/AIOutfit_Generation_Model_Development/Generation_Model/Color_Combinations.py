import os
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import ast

# Función para convertir cadena de color a lista de valores RGB
def color_str_to_list(color_str):
    return np.array(ast.literal_eval(color_str))

# Intentar cargar el dataset con manejo de errores
archivo = 'T:/CONTRUCCION DE SOFTWARE/ProyectoFinal/VIEW/Neural_Network_Model/AIOutfit_Generation_Model_Development/dataset.csv'

# Verficar si el archivo existe
if os.path.exists(archivo):
    print("El archivo existe. Cargando...")
    try:
        # Intenta leer el archivo con la codificación correcta
        data = pd.read_csv(archivo, encoding='utf-8')
        print("Archivo cargado correctamente.")
    except Exception as e:
        print("Error al leer el archivo CSV:", e)
        exit()
else:
    print("No se encontró el archivo CSV en la ruta especificada.")
    exit()

# Mostrar las columnas del DataFrame para verificar su contenido
print("Columnas del DataFrame:", data.columns)

# Convertir las columnas de colores a listas de valores RGB
data['COLOR1'] = data['COLOR1'].apply(color_str_to_list)
data['COLOR2'] = data['COLOR2'].apply(color_str_to_list)
data['COLOR3'] = data['COLOR3'].apply(color_str_to_list)

# Asegurarse de que la columna 'COMBINABLE' sea de tipo int
data['COMBINABLE'] = data['COMBINABLE'].astype(int)

# Separar características y etiquetas
X = data[['INDICE', 'COLOR1', 'COLOR2', 'COLOR3']]
y = data['COMBINABLE']

# One-hot encoding para el índice
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=np.float32)
X_indice = encoder.fit_transform(X[['INDICE']])

# Normalizar los colores y convertir a tipo float32
def normalize_colors(colors):
    return np.array(colors) / 255.0

X_colors = np.hstack([
    normalize_colors(X['COLOR1'].values.tolist()),
    normalize_colors(X['COLOR2'].values.tolist()),
    normalize_colors(X['COLOR3'].values.tolist())
]).astype(np.float32)

# Concatenar índice codificado y colores normalizados
X = np.concatenate([X_indice, X_colors], axis=1)

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Asegurarse de que las etiquetas sean de tipo float32
y_train = y_train.astype(np.float32)
y_test = y_test.astype(np.float32)

# Definir el modelo
model = Sequential([
    tf.keras.Input(shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Salida binaria (combinable o no combinable)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluar el modelo
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Precisión del modelo en el conjunto de datos de prueba:", test_acc)

# Guardar el modelo entrenado en un archivo .h5
# model.save('modelo_outfit.h5')
# print("Modelo guardado como 'modelo_outfit.h5'.")

# Ejemplo de predicción
nueva_entrada = pd.DataFrame([['TRIADICA', '(255,69,0)', '(124,252,25)', '(138,43,226)']], columns=['INDICE', 'COLOR1', 'COLOR2', 'COLOR3'])

# Convertir las columnas de colores a listas de valores RGB
nueva_entrada['COLOR1'] = nueva_entrada['COLOR1'].apply(color_str_to_list)
nueva_entrada['COLOR2'] = nueva_entrada['COLOR2'].apply(color_str_to_list)
nueva_entrada['COLOR3'] = nueva_entrada['COLOR3'].apply(color_str_to_list)

# Normalizar los colores y convertir a tipo float32
nueva_entrada_colors = np.concatenate([
    normalize_colors(nueva_entrada['COLOR1'].values.tolist()),
    normalize_colors(nueva_entrada['COLOR2'].values.tolist()),
    normalize_colors(nueva_entrada['COLOR3'].values.tolist())
]).astype(np.float32)

# One-hot encoding para la nueva entrada
nueva_entrada_indice = encoder.transform(nueva_entrada[['INDICE']])

# Concatenar índice codificado y colores normalizados
nueva_entrada_preparada = np.concatenate([nueva_entrada_indice, nueva_entrada_colors.reshape(1, -1)], axis=1)

# Verificar el formato de nueva_entrada_preparada
print("Shape de nueva_entrada_preparada:", nueva_entrada_preparada.shape)
print("Tipos de datos de nueva_entrada_preparada:", nueva_entrada_preparada.dtype)

# Predicción
prediccion = model.predict(nueva_entrada_preparada)
print('Combinable' if prediccion > 0.5 else 'No combinable')
