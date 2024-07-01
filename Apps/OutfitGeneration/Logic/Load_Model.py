import random
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
import ast
import json 

def color_str_to_list(color_str):
    if color_str.startswith('[') and color_str.endswith(']'):
        color_list = np.array(ast.literal_eval(color_str))
        return color_list
    else:
        raise ValueError("Formato de cadena de color no válido: debe estar en formato '[R, G, B]'")

def normalize_colors(colors):
    normalized_colors = np.array(colors) / 255.0
    return normalized_colors

def generate_outfits(model_path, garment_data, num_outfits=3):
    try:
        model = load_model(model_path)
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")
    
    try:
        with open('Color_combinations_type_classes.json', 'r') as file:
            Tipo_de_combinaciones = json.load(file)
    except Exception as e:
        print(f"Error al cargar el archivo de combinaciones: {e}")
    
    Combinacion_elegida = random.choice(list(Tipo_de_combinaciones.keys()))
    print (f"Combinacion elegida: {Combinacion_elegida}")
    
    
    lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
    lista_categorias_inferior = ['Trouser']
    lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']

    prendas_superior = [g for g in garment_data if g['category'] in lista_categorias_superior]
    prendas_inferior = [g for g in garment_data if g['category'] in lista_categorias_inferior]
    prendas_zapatos = [g for g in garment_data if g['category'] in lista_categorias_zapatos]

    outfits = []

    for _ in range(num_outfits):
        prenda_superior = random.choice(prendas_superior)
        prenda_inferior = random.choice(prendas_inferior)
        prenda_zapato = random.choice(prendas_zapatos)
        
        
        Combinacion_elegida = random.choice(list(Tipo_de_combinaciones.keys()))
        print (f"Tipo de combinacion elegida: {Combinacion_elegida}")

        entrada = pd.DataFrame(
            [[Combinacion_elegida, prenda_superior['dominant_color'], prenda_inferior['dominant_color'], prenda_zapato['dominant_color']]],
            columns=['INDICE', 'COLOR1', 'COLOR2', 'COLOR3']
        )

        entrada['COLOR1'] = [color_str_to_list(entrada['COLOR1'].values[0])]
        entrada['COLOR2'] = [color_str_to_list(entrada['COLOR2'].values[0])]
        entrada['COLOR3'] = [color_str_to_list(entrada['COLOR3'].values[0])]

        nueva_entrada_colors = np.concatenate([
            normalize_colors(entrada['COLOR1'][0]),
            normalize_colors(entrada['COLOR2'][0]),
            normalize_colors(entrada['COLOR3'][0])
        ]).astype(np.float32)

        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=np.float32)
        encoder.fit(pd.DataFrame([[Combinacion_elegida]], columns=['INDICE']))
        nueva_entrada_indice = encoder.transform(entrada[['INDICE']])

        nueva_entrada_preparada = np.concatenate([nueva_entrada_indice, nueva_entrada_colors.reshape(1, -1)], axis=1)

        if nueva_entrada_preparada.shape[1] != 16:
            falta = 16 - nueva_entrada_preparada.shape[1]
            nueva_entrada_preparada = np.hstack([nueva_entrada_preparada, np.zeros((1, falta), dtype=np.float32)])

        try:
            prediccion = model.predict(nueva_entrada_preparada)
            resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
            outfits.append({
                'prenda_superior': {
                    'id': prenda_superior['id'],
                    'category': prenda_superior['category'],
                    'image': prenda_superior['image'],
                },
                'prenda_inferior': {
                    'id': prenda_inferior['id'],
                    'category': prenda_inferior['category'],
                    'image': prenda_inferior['image'],
                },
                'zapato': {
                    'id': prenda_zapato['id'],
                    'category': prenda_zapato['category'],
                    'image': prenda_zapato['image'],
                },
                'resultado': resultado
            })
        except Exception as e:
            raise RuntimeError(f"Error al realizar la predicción: {e}")
        
    return outfits


if __name__ == "__main__":
    prenda_1 = {
        'category': 'Coat',
        'dominant_color': '[47,79,79]'
    }
    prenda_2 = {
        'category': 'Trouser',
        'dominant_color': '[169,169,169]'
    }
    prenda_3 = {
        'category': 'Sneaker',
        'dominant_color': '[210,180,140]'
    }

    all_data_for_generation = [prenda_1, prenda_2, prenda_3]
    
    model_path = 'Outfit_Generator_Model.h5'
    outfits = generate_outfits(model_path, all_data_for_generation)
    print(outfits)
