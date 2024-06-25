import webcolors
import colorsys

def obtener_hsv(color_name):
    """
    Convierte un color de nombre a HSV.
    :param color_name: Nombre del color.
    :return: Tupla HSV del color.
    """
    rgb_color = webcolors.name_to_rgb(color_name)
    return colorsys.rgb_to_hsv(rgb_color.red / 255.0, rgb_color.green / 255.0, rgb_color.blue / 255.0)

def es_complementario(hsv1, hsv2):
    """
    Determina si dos colores HSV son complementarios.
    :param hsv1: Tupla HSV del primer color.
    :param hsv2: Tupla HSV del segundo color.
    :return: True si los colores son complementarios, False en caso contrario.
    """
    hue1, _, _ = hsv1
    hue2, _, _ = hsv2
    return abs(hue1 - hue2) >= 0.5

def Fn_combinacion_colores_outfit(color1, color2):
    """
    Comprueba si dos colores combinan bien.
    :param color1: Nombre del color dominante de la prenda superior.
    :param color2: Nombre del color dominante de la prenda inferior.
    :return: True si los colores combinan bien, False en caso contrario.
    """
    try:
        # Convertir nombres de colores a HSV
        hsv1 = obtener_hsv(color1)
        hsv2 = obtener_hsv(color2)
        
        # Verificar si los colores son complementarios
        return es_complementario(hsv1, hsv2)
    except ValueError as e:
        print(f"Error al convertir los nombres de colores a HSV: {e}")
        return False

if __name__ == "__main__":
    color1 = "red"
    color2 = "blue"
    print(Fn_combinacion_colores_outfit(color1, color2))  