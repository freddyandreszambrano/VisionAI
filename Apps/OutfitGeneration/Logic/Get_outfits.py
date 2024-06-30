import random
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
import ast

def color_str_to_list(color_str):
    """Convierte una cadena de color en una lista de valores RGB."""
    if color_str.startswith('[') and color_str.endswith(']'):
        return np.array(ast.literal_eval(color_str))
    else:
        raise ValueError("Formato de cadena de color no válido: debe estar en formato '[R, G, B]'")

def normalize_colors(colors):
    """Normaliza los valores de color RGB."""
    return np.array(colors) / 255.0

def Fn_generate_outfits(model_path, selected_items, garment_data, num_outfits=3):
    try:
        model = load_model(model_path)
        print("Modelo cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        raise RuntimeError(f"Error al cargar el modelo: {e}")

    # Categorías de prendas disponibles
    lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
    lista_categorias_inferior = ['Trouser']
    lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']

    # Filtrar prendas disponibles según categoría
    prendas_superior = [g for g in garment_data if g['category'] in lista_categorias_superior]
    prendas_inferior = [g for g in garment_data if g['category'] in lista_categorias_inferior]
    prendas_zapatos = [g for g in garment_data if g['category'] in lista_categorias_zapatos]

    print(f"Prendas superiores disponibles: {prendas_superior}")
    print(f"Prendas inferiores disponibles: {prendas_inferior}")
    print(f"Prendas de zapatos disponibles: {prendas_zapatos}")

    outfits = []

    def generate_single_outfit(superior, inferior, zapato):
        # Función para generar un único outfit con las prendas dadas
        entrada = pd.DataFrame(
            [['NEUTRAL', superior['dominant_color'], inferior['dominant_color'], zapato['dominant_color']]],
            columns=['INDICE', 'COLOR1', 'COLOR2', 'COLOR3']
        )

        # Preparación de la entrada para el modelo
        entrada['COLOR1'] = [color_str_to_list(entrada['COLOR1'].values[0])]
        entrada['COLOR2'] = [color_str_to_list(entrada['COLOR2'].values[0])]
        entrada['COLOR3'] = [color_str_to_list(entrada['COLOR3'].values[0])]
        nueva_entrada_colors = np.concatenate([
            normalize_colors(entrada['COLOR1'][0]),
            normalize_colors(entrada['COLOR2'][0]),
            normalize_colors(entrada['COLOR3'][0])
        ]).astype(np.float32)

        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=np.float32)
        encoder.fit(pd.DataFrame([['NEUTRAL']], columns=['INDICE']))
        nueva_entrada_indice = encoder.transform(entrada[['INDICE']])
        nueva_entrada_preparada = np.concatenate([nueva_entrada_indice, nueva_entrada_colors.reshape(1, -1)], axis=1)

        if nueva_entrada_preparada.shape[1] != 16:
            falta = 16 - nueva_entrada_preparada.shape[1]
            nueva_entrada_preparada = np.hstack([nueva_entrada_preparada, np.zeros((1, falta), dtype=np.float32)])

        try:
            # Predicción del modelo
            prediccion = model.predict(nueva_entrada_preparada)
            resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
            return {
                'prenda_superior': {
                    'id': superior['id'],
                    'category': superior['category'],
                    'image': superior['image'],
                },
                'prenda_inferior': {
                    'id': inferior['id'],
                    'category': inferior['category'],
                    'image': inferior['image'],
                },
                'zapato': {
                    'id': zapato['id'],
                    'category': zapato['category'],
                    'image': zapato['image'],
                },
                'resultado': resultado
            }
        except Exception as e:
            print(f"Error al realizar la predicción: {e}")
            raise RuntimeError(f"Error al realizar la predicción: {e}")


 

    return outfits


if __name__ == '__main__':
    model_path = 'Outfit_Generator_Model.h5'
    selected_items = {
        'superior': {'id': 1, 'category': 'Shirt', 'dominant_color': '[255,0,0]', 'image': 'image_path1'},
        'inferior': None,
        'zapatos': None
    }
    garment_data = [
        {'id': 1, 'category': 'Shirt', 'dominant_color': '[255,0,0]', 'image': 'image_path1'},
        {'id': 2, 'category': 'Trouser', 'dominant_color': '[0,255,0]', 'image': 'image_path2'},
        {'id': 3, 'category': 'Sneaker', 'dominant_color': '[0,0,255]', 'image': 'image_path3'}
    ]
    num_outfits = 3
    outfits = Fn_generate_outfits(model_path, selected_items, garment_data, num_outfits)
    print("Outfits generados:", outfits)
