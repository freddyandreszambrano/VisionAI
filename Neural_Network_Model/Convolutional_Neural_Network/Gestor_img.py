import os 
import shutil
from PIL import Image

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
            if contador_max_img < 40:
                ruta_imagen_fuente = os.path.join(directorio_fuente_actual, imagen)
                ruta_imagen_destino = os.path.join(directorio_destino_actual, os.path.splitext(imagen)[0] + '.png')
                
                with Image.open(ruta_imagen_fuente) as img:
                    img = img.resize((224, 224))
                    img.save(ruta_imagen_destino, format='PNG')

                contador_max_img += 1
            else:
                break


def Main():
   Ruta_base = r'T:\CONTRUCCION DE SOFTWARE\ProyectoFinal\VIEW\Neural_Network_Model'
   carpeta_fuente = os.path.join(Ruta_base, 'Training Data')
   carpeta_destino = os.path.join(Ruta_base, 'DataSet')
   Ls_nombres_carpetas = Fn_obtener_nombres_carpetas(carpeta_fuente)
  
   Fn_copy_images(Ls_nombres_carpetas,carpeta_destino,carpeta_fuente)

if __name__ == "__main__":
    Main()