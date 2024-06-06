import cv2
import numpy as np
from colorthief import ColorThief
import webcolors

def Fn_obtener_nombre_color(rgb_color):
    min_colores = {}
    for hex_color, nombre in webcolors.CSS3_HEX_TO_NAMES.items():
        r_hex, g_hex, b_hex = webcolors.hex_to_rgb(hex_color)
        rd = (r_hex - rgb_color[0]) ** 2
        gd = (g_hex - rgb_color[1]) ** 2
        bd = (b_hex - rgb_color[2]) ** 2
        min_colores[(rd + gd + bd)] = nombre
    return min_colores[min(min_colores.keys())]

def Fn_segmentar_y_analizar_prenda(ruta_imagen):
    imagen = cv2.imread(ruta_imagen)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    _, imagen_umbral = cv2.threshold(imagen_gris, 240, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(imagen_umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mascara = np.zeros_like(imagen)
    cv2.drawContours(mascara, contornos, -1, (255, 255, 255), -1)

    ladron_color = ColorThief(ruta_imagen)
    paleta_colores = ladron_color.get_palette(color_count=5)  # Obtener los 5 colores más dominantes

    return paleta_colores

if __name__ == "__main__":
    ruta_imagen = r"C:\Users\USER\Downloads\camiseta.jpg"
    color_dominantes =Fn_segmentar_y_analizar_prenda(ruta_imagen)
    print("Nombres de colores dominantes:", color_dominantes)