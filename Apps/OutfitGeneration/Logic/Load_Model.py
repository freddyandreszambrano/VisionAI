# outfit_generator.py
import random
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import OneHotEncoder
import ast
import json

def color_str_to_list(color_str):
    try:
        return np.array(ast.literal_eval(color_str))
    except ValueError:
        raise ValueError("Formato de cadena de color no válido: debe estar en formato '[R, G, B]'")

def normalize_colors(colors):
    return np.array(colors) / 255.0

def load_tipo_de_combinaciones(path='Color_combinations_type_classes.json'):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise RuntimeError(f"Error al cargar el archivo de combinaciones: {e}")

def generate_outfits(model_path, garment_data, num_outfits=3):
    try:
        model = load_model(model_path)
        print(f"Modelo cargado correctamente desde {model_path}")
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")

    tipo_de_combinaciones = load_tipo_de_combinaciones()
    print(f"Tipo de combinaciones cargado: {tipo_de_combinaciones}")
    
    categorias = {
        'superior': ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt'],
        'inferior': ['Trouser'],
        'zapatos': ['Sneaker', 'Sandal', 'Ankle boot']
    }

    prendas = {key: [g for g in garment_data if g['category'] in categorias[key]] for key in categorias}

    for key, value in prendas.items():
        print(f"{key.capitalize()} clothes: {value}")

    outfits = []

    for _ in range(num_outfits):
        prenda_superior = random.choice(prendas['superior'])
        prenda_inferior = random.choice(prendas['inferior'])
        prenda_zapato = random.choice(prendas['zapatos'])
        
        print(f"Selected clothes - Superior: {prenda_superior}, Inferior: {prenda_inferior}, Zapato: {prenda_zapato}")
        
        combinacion_elegida = random.choice(list(tipo_de_combinaciones.keys()))
        print(f"Tipo de combinacion elegida: {combinacion_elegida}")

        entrada = pd.DataFrame(
            [[combinacion_elegida, prenda_superior['dominant_color'], prenda_inferior['dominant_color'], prenda_zapato['dominant_color']]],
            columns=['INDICE', 'COLOR1', 'COLOR2', 'COLOR3']
        )

        entrada['COLOR1'] = [color_str_to_list(entrada['COLOR1'].values[0])]
        entrada['COLOR2'] = [color_str_to_list(entrada['COLOR2'].values[0])]
        entrada['COLOR3'] = [color_str_to_list(entrada['COLOR3'].values[0])]

        print(f"Entrada colores: {entrada}")

        nueva_entrada_colors = np.concatenate([
            normalize_colors(entrada['COLOR1'][0]),
            normalize_colors(entrada['COLOR2'][0]),
            normalize_colors(entrada['COLOR3'][0])
        ]).astype(np.float32)

        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=np.float32)
        encoder.fit(pd.DataFrame([[combinacion_elegida]], columns=['INDICE']))
        nueva_entrada_indice = encoder.transform(entrada[['INDICE']])
        nueva_entrada_preparada = np.concatenate([nueva_entrada_indice, nueva_entrada_colors.reshape(1, -1)], axis=1)

        falta = 16 - nueva_entrada_preparada.shape[1]
        nueva_entrada_preparada = np.hstack([nueva_entrada_preparada, np.zeros((1, falta), dtype=np.float32)])
        print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

        try:
            prediccion = model.predict(nueva_entrada_preparada)
            resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
            print(f"Predicción: {prediccion}, Resultado: {resultado}")

            outfits.append({
                'prenda_superior': prenda_superior,
                'prenda_inferior': prenda_inferior,
                'zapato': prenda_zapato,
                'resultado': resultado
            })
        except Exception as e:
            raise RuntimeError(f"Error al realizar la predicción: {e}")
        
    return outfits

if __name__ == "__main__":
    prenda_1 = {
        'id': 1,
        'category': 'Coat',
        'dominant_color': '[47,79,79]',
        'image': 'image_1.jpg'
    }
    prenda_2 = {
        'id': 2,
        'category': 'Trouser',
        'dominant_color': '[169,169,169]',
        'image': 'image_2.jpg'
    }
    prenda_3 = {
        'id': 3,
        'category': 'Sneaker',
        'dominant_color': '[210,180,140]',
        'image': 'image_3.jpg'
    }

    all_data_for_generation = [prenda_1, prenda_2, prenda_3]
    
    selected_items = {
        'superior': prenda_1  # Simular que el usuario ha seleccionado una prenda superior
    }

    model_path = 'Outfit_Generator_Model.h5'
    outfits = generate_outfits(model_path, selected_items, all_data_for_generation)
    print(outfits)
