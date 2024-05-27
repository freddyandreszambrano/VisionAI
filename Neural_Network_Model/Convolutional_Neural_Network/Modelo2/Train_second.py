import json
import os
import shutil
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense


def Fn_Train_second():
   Ruta_base = r'T:\CONTRUCCION DE SOFTWARE\ProyectoFinal\VIEW\Neural_Network_Model'
   carpeta_fuente = os.path.join(Ruta_base, 'Training Data')
   carpeta_destino = os.path.join(Ruta_base, 'DataSet')
   Ls_nombres_carpetas = Fn_obtener_nombres_carpetas(carpeta_fuente)
  
   #Fn_copy_images(Ls_nombres_carpetas,carpeta_destino,carpeta_fuente)
   #Fn_aumentar_dataSet(Ruta_base, carpeta_destino)
   dataset_entrenamiento  = Fn_Entrenar_ModeloIA(carpeta_destino)
   Fn_Entrenar(dataset_entrenamiento)
   
   
   



def Fn_obtener_nombres_carpetas(Directorio_fuente):
   try:
        Ls_nombres_carpetas = []
        for elemento_carpeta in os.listdir(Directorio_fuente):
            if os.path.isdir(os.path.join(Directorio_fuente, elemento_carpeta)):
                Ls_nombres_carpetas.append(elemento_carpeta)
        return Ls_nombres_carpetas
   except FileNotFoundError as e:
        print(f"Error: El directorio '{Directorio_fuente}' no existe.")
        return []

def Fn_copy_images(Ls_name_file, directorio_destino, directorio_fuente):
   
   for nombre_carpeta in Ls_name_file:
        directorio_fuente_actual = os.path.join(directorio_fuente, nombre_carpeta)
        directorio_destino_actual = os.path.join(directorio_destino, nombre_carpeta)

        if not os.path.exists(directorio_destino_actual):
            os.makedirs(directorio_destino_actual)

        contador_max_img = 0
        for imagen in os.listdir(directorio_fuente_actual):
            if contador_max_img < 100:
                shutil.copy(os.path.join(directorio_fuente_actual, imagen), directorio_destino_actual)
                contador_max_img += 1
            else:
                break

   
def Fn_aumentar_dataSet(Ruta_base,carpeta_fuente ):
  pass


def Fn_Entrenar_ModeloIA(Directorio_dataset):
   batch_size=32
   target_size=(28, 28)
   datagen = ImageDataGenerator(rescale=1./255)
   print(datagen)
   dataset = datagen.flow_from_directory(
        Directorio_dataset,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        color_mode='rgb'
    )
   
   class_indices = dataset.class_indices
   with open('class_indices.json', 'w') as f:
      json.dump(class_indices, f)
  
   return dataset


def Fn_Entrenar (Dataset):
   modelo =  crear_nuevo_modelo()
   modelo.summary()
    
   modelo.fit(Dataset, epochs=10)
    
   modelo.save('IAoutfit.keras')
   
   

def crear_nuevo_modelo():
    modelo = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 3)),  # RGB images
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])
    modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return modelo

if __name__ == "__main__":
    Fn_Train_second()