import random
import numpy as np
import pandas as pd
from keras.models import load_model
from keras.optimizers import Adam
from sklearn.preprocessing import OneHotEncoder
import ast
import json
import logging

def color_str_to_list(color_str):
    if color_str.startswith('[') and color_str.endswith(']'):
        color_list = np.array(ast.literal_eval(color_str))
        return color_list
    else:
        raise ValueError("Formato de cadena de color no válido: debe estar en formato '[R, G, B]'")

def normalize_colors(colors):
    normalized_colors = np.array(colors) / 255.0
    return normalized_colors

def function_generate_outfits(model_path, garment_data, data_filtro):
    try:
        model = load_model(model_path)
        # Compilar el modelo si no está compilado
        if not model.optimizer:
            model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    except Exception as e:
        raise RuntimeError(f"Error al cargar o compilar el modelo: {e}")
    
    try:
        with open('Color_combinations_type_classes.json', 'r') as file:
            Tipo_de_combinaciones = json.load(file)
    except Exception as e:
        raise RuntimeError(f"Error al cargar el archivo de combinaciones: {e}")
    
    if data_filtro == 'DIA':
        tipos_validos = ['ANALOGAS', 'MONOCROMATICA']
    elif data_filtro == 'NOCHE':
        tipos_validos = ['COMPLEMENTARIO']
    elif data_filtro == 'BODA':
        tipos_validos = ['ANALOGAS']  # Puedes ajustar según los tipos válidos para boda
    else:
        tipos_validos = list(Tipo_de_combinaciones.keys())

    # Elegir una combinación válida aleatoriamente si no se especifica un tipo válido
    Combinacion_elegida = random.choice([Tipo_de_combinaciones.get(tipo, None) for tipo in tipos_validos])

    if Combinacion_elegida is None:
        raise ValueError(f"No se encontró una combinación para el filtro: {data_filtro}")

    print(f"Combinacion elegida: {Combinacion_elegida}")

    lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
    lista_categorias_inferior = ['Trouser']
    lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']

    prendas_superior = [g for g in garment_data if g['category'] in lista_categorias_superior]
    prendas_inferior = [g for g in garment_data if g['category'] in lista_categorias_inferior]
    prendas_zapatos = [g for g in garment_data if g['category'] in lista_categorias_zapatos]

    if not prendas_superior or not prendas_inferior or not prendas_zapatos:
        raise ValueError("No hay suficientes prendas para generar un outfit.")

    # Determinar el número mínimo de prendas en las tres categorías
    num_outfits = min(len(prendas_superior), len(prendas_inferior), len(prendas_zapatos))
    print(f"Número máximo de outfits a generar: {num_outfits}")

    outfits = []

    while num_outfits > 0:
        try:
            prenda_superior = random.choice(prendas_superior)
            prenda_inferior = random.choice(prendas_inferior)
            prenda_zapato = random.choice(prendas_zapatos)
        except IndexError:
            print("No hay suficientes prendas para generar un outfit.")
            break

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
            num_outfits -= 1
        except Exception as e:
            raise RuntimeError(f"Error al realizar la predicción: {e}")

    # Si no se pudo generar ningún outfit, generar un outfit aleatorio
    num_outfits = min(len(prendas_superior), len(prendas_inferior), len(prendas_zapatos))

    if not outfits:
        while num_outfits > 0:
            print("No se pudieron generar outfits combinables, generando un outfit aleatorio.")
            prenda_superior = random.choice(prendas_superior)
            prenda_inferior = random.choice(prendas_inferior)
            prenda_zapato = random.choice(prendas_zapatos)
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
                'resultado': 'Aleatorio'
            })
            num_outfits -= 1
        
    return outfits

if __name__ == "__main__":
    prenda_1 = {
        'id': 1,
        'category': 'Coat',
        'dominant_color': '[47,79,79]',
        'image': 'path/to/image1.jpg'
    }
    prenda_2 = {
        'id': 2,
        'category': 'Trouser',
        'dominant_color': '[169,169,169]',
        'image': 'path/to/image2.jpg'
    }
    prenda_3 = {
        'id': 3,
        'category': 'Sneaker',
        'dominant_color': '[210,180,140]',
        'image': 'path/to/image3.jpg'
    }

    all_data_for_generation = [prenda_1, prenda_2, prenda_3]
    
    model_path = 'Outfit_Generator_Model.h5'
    data_filtro = 'DIA'  # Este es el valor que se obtiene de la solicitud GET en la vista Django
    outfits = function_generate_outfits(model_path, all_data_for_generation, data_filtro)
    print(outfits)
