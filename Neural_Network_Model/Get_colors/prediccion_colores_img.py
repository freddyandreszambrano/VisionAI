import cv2
import numpy as np
from colorthief import ColorThief

def Fn_segmentar_y_analizar_prenda(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    _, imagen_umbral = cv2.threshold(imagen_gris, 240, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(imagen_umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mascara = np.zeros_like(imagen)
    cv2.drawContours(mascara, contornos, -1, (255, 255, 255), -1)

    ladron_color = ColorThief(ruta_imagen)
    color_dominante = ladron_color.get_color(quality=1)  # Obtener el color dominante de alta calidad

    return color_dominante

if __name__ == "__main__":
    ruta_imagen = r"C:\Users\USER\Downloads\camiseta.jpg"
    color_dominante = Fn_segmentar_y_analizar_prenda(ruta_imagen)
    print("Color dominante RGB:", color_dominante)
