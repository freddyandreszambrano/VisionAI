import json
import random
from keras.models import load_model
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import ast

def color_str_to_list(color_str):
    if color_str.startswith('[') and color_str.endswith(']'):
        return list(map(int, color_str[1:-1].split(',')))
    else:
        raise ValueError("Formato de cadena de color no válido: debe estar en formato '[R, G, B]'")

def normalize_colors(color_list):
    return np.array(color_list) / 255.0

def Fn_generate_outfits(model_path, selected_items, garment_data):
    try:
        model = load_model(model_path)
        print("Modelo cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        raise RuntimeError(f"Error al cargar el modelo: {e}")
    
    try:
        with open('Color_combinations_type_classes.json', 'r') as file:
            Tipo_de_combinaciones = json.load(file)
            print("Archivo de combinaciones cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el archivo de combinaciones: {e}")
        Tipo_de_combinaciones = {}

    lista_categorias_superior = ['Coat', 'Dress', 'Pullover', 'Shirt', 'T-shirt']
    lista_categorias_inferior = ['Trouser']
    lista_categorias_zapatos = ['Sneaker', 'Sandal', 'Ankle boot']

    prendas_superior = [g for g in garment_data if g['category'] in lista_categorias_superior]
    prendas_inferior = [g for g in garment_data if g['category'] in lista_categorias_inferior]
    prendas_zapatos = [g for g in garment_data if g['category'] in lista_categorias_zapatos]

    print(f"Prendas superior: {prendas_superior}")
    print(f"Prendas inferior: {prendas_inferior}")
    print(f"Prendas zapatos: {prendas_zapatos}")

    # Determinar el número mínimo de prendas en las tres categorías
    num_outfits = min(len(prendas_superior), len(prendas_inferior), len(prendas_zapatos))
    print(f"Número de outfits a generar: {num_outfits}")
    
    def is_combination_valid(model, combinacion_elegida, superior, inferior, zapatos):
        entrada = pd.DataFrame(
            [[combinacion_elegida, superior['dominant_color'], inferior['dominant_color'], zapatos['dominant_color']]],
            columns=['INDICE', 'COLOR1', 'COLOR2', 'COLOR3']
        )

        entrada['COLOR1'] = [color_str_to_list(entrada['COLOR1'].values[0])]
        entrada['COLOR2'] = [color_str_to_list(entrada['COLOR2'].values[0])]
        entrada['COLOR3'] = [color_str_to_list(entrada['COLOR3'].values[0])]
        print(f"Entrada después de convertir colores: {entrada}")

        nueva_entrada_colors = np.concatenate([
            normalize_colors(entrada['COLOR1'][0]),
            normalize_colors(entrada['COLOR2'][0]),
            normalize_colors(entrada['COLOR3'][0])
        ]).astype(np.float32)

        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore', dtype=np.float32)
        encoder.fit(pd.DataFrame([[combinacion_elegida]], columns=['INDICE']))
        nueva_entrada_indice = encoder.transform(entrada[['INDICE']])

        nueva_entrada_preparada = np.concatenate([nueva_entrada_indice, nueva_entrada_colors.reshape(1, -1)], axis=1)

        if nueva_entrada_preparada.shape[1] != 16:
            falta = 16 - nueva_entrada_preparada.shape[1]
            nueva_entrada_preparada = np.hstack([nueva_entrada_preparada, np.zeros((1, falta), dtype=np.float32)])

        print(f"Nueva entrada preparada para el modelo: {nueva_entrada_preparada}")

        try:
            prediccion = model.predict(nueva_entrada_preparada)
            print(f"Predicción del modelo: {prediccion}")
            return prediccion[0] > 0.5  # Asumiendo que el modelo devuelve una probabilidad
        except Exception as e:
            raise RuntimeError(f"Error al realizar la predicción: {e}")

    outfits = []
    Combinacion_elegida = random.choice(list(Tipo_de_combinaciones.keys())) if Tipo_de_combinaciones else 'default'
    print(f"Combinación elegida: {Combinacion_elegida}")
    
    if 'superior' in selected_items and selected_items['superior']:
        superior_item = selected_items['superior']
        print(f"Prenda superior seleccionada: {superior_item}")

        for _ in range(num_outfits):
            
            prenda_zapato = random.choice(prendas_zapatos)
            prenda_inferior = random.choice(prendas_inferior)
            entrada = pd.DataFrame(
                [[Combinacion_elegida, superior_item['dominant_color'], prenda_inferior['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                if resultado == 'Combinable':
                    outfits.append({
                        'prenda_superior': {
                            'id': superior_item['id'],
                            'category': superior_item['category'],
                            'image': superior_item['url'],
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
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}") 
    else:
        print("No hay prenda superior seleccionada, no se puede generar outfits.")

    if 'inferior' in selected_items and selected_items['inferior']:
        inferior_item = selected_items['inferior']
        print(f"Prenda inferior seleccionada: {inferior_item}")

        for _ in range(num_outfits):

            prenda_zapato = random.choice(prendas_zapatos)
            prenda_superior = random.choice(prendas_superior)

            entrada = pd.DataFrame(
                [[Combinacion_elegida, prenda_superior['dominant_color'], inferior_item['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                outfits.append({
                    'prenda_superior': {
                        'id': prenda_superior['id'],
                        'category': prenda_superior['category'],
                        'image': prenda_superior['image'],
                        },
                    'prenda_inferior': {
                        'id': inferior_item['id'],
                        'category': inferior_item['category'],
                        'image': inferior_item['url'],
                    },
                    'zapato': {
                        'id': prenda_zapato['id'],
                        'category': prenda_zapato['category'],
                        'image': prenda_zapato['image'],
                    },
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}")
    else:
        print("No hay prenda inferior seleccionada, no se puede generar outfits.")
            
    if 'zapatos' in selected_items and selected_items['zapatos']:
        prenda_zapato = selected_items['zapatos']
        print(f"Prenda de zapatos seleccionada: {prenda_zapato}")
            

        for _ in range(num_outfits):
            inferior_item = random.choice(prendas_inferior)
            prenda_superior = random.choice(prendas_superior)
            entrada = pd.DataFrame(
                [[Combinacion_elegida, prenda_superior['dominant_color'], inferior_item['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                outfits.append({
                    'prenda_superior': {
                        'id': prenda_superior['id'],
                        'category': prenda_superior['category'],
                        'image': prenda_superior['image'],
                    },
                    'prenda_inferior': {
                        'id': inferior_item['id'],
                        'category': inferior_item['category'],
                        'image': inferior_item['image'],
                    },
                    'zapato': {
                        'id': prenda_zapato['id'],
                        'category': prenda_zapato['category'],
                        'image': prenda_zapato['url'],
                    },
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}")
    else:
        print("No hay prenda 'ZAPATO' seleccionada, no se puede generar outfits.")
        
    if 'inferior' in selected_items and selected_items['inferior'] and 'superior' in selected_items and selected_items['superior']:
        prenda_superior = selected_items['superior']
        inferior_item = selected_items['inferior']
        print("Prenda superior e inferior seleccionadas")
        
        for _ in range(num_outfits):
            prenda_zapato = random.choice(prendas_zapatos)
            
            entrada = pd.DataFrame(
                [[Combinacion_elegida, prenda_superior['dominant_color'], inferior_item['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                outfits.append({
                    'prenda_superior': {
                        'id': prenda_superior['id'],
                        'category': prenda_superior['category'],
                        'image': prenda_superior['url'],
                    },
                    'prenda_inferior': {
                        'id': inferior_item['id'],
                        'category': inferior_item['category'],
                        'image': inferior_item['url'],
                    },
                    'zapato': {
                        'id': prenda_zapato['id'],
                        'category': prenda_zapato['category'],
                        'image': prenda_zapato['image'],
                    },
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}")
    else:
        print("No hay prenda superior ni inferior seleccionada, no se puede generar outfits.")

    if 'zapatos' in selected_items and selected_items['zapatos'] and 'superior' in selected_items and selected_items['superior']:
        prenda_superior = selected_items['superior']
        prenda_zapato = selected_items['zapatos']
        print("Prenda superior y zapatos seleccionados")
        
        for _ in range(num_outfits):
            inferior_item = random.choice(prendas_inferior)
            
            entrada = pd.DataFrame(
                [[Combinacion_elegida, prenda_superior['dominant_color'], inferior_item['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                outfits.append({
                    'prenda_superior': {
                        'id': prenda_superior['id'],
                        'category': prenda_superior['category'],
                        'image': prenda_superior['url'],
                    },
                    'prenda_inferior': {
                        'id': inferior_item['id'],
                        'category': inferior_item['category'],
                        'image': inferior_item['image'],
                    },
                    'zapato': {
                        'id': prenda_zapato['id'],
                        'category': prenda_zapato['category'],
                        'image': prenda_zapato['url'],
                    },
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}")
    else:
        print("No hay prenda superior ni zapatos seleccionados, no se puede generar outfits.")

    if 'zapatos' in selected_items and selected_items['zapatos'] and 'inferior' in selected_items and selected_items['inferior']:
        prenda_zapato = selected_items['zapatos']
        print("Prenda inferior y zapatos seleccionados")
        
        for _ in range(num_outfits):
            prenda_superior = random.choice(prendas_superior)
            inferior_item = selected_items['inferior']
            
            entrada = pd.DataFrame(
                [[Combinacion_elegida, prenda_superior['dominant_color'], inferior_item['dominant_color'], prenda_zapato['dominant_color']]],
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

            print(f"Nueva entrada preparada: {nueva_entrada_preparada}")

            try:
                prediccion = model.predict(nueva_entrada_preparada)
                resultado = 'Combinable' if prediccion > 0.5 else 'No combinable'
                print(f"Resultado de la predicción: {resultado}")
                outfits.append({
                    'prenda_superior': {
                        'id': prenda_superior['id'],
                        'category': prenda_superior['category'],
                        'image': prenda_superior['image'],
                    },
                    'prenda_inferior': {
                        'id': inferior_item['id'],
                        'category': inferior_item['category'],
                        'image': inferior_item['url'],
                    },
                    'zapato': {
                        'id': prenda_zapato['id'],
                        'category': prenda_zapato['category'],
                        'image': prenda_zapato['url'],
                    },
                    'resultado': resultado
                })
            except Exception as e:
                print(f"Error al realizar la predicción: {e}")
                raise RuntimeError(f"Error al realizar la predicción: {e}")
    else:
        print("No hay prenda inferior ni zapatos seleccionados, no se puede generar outfits.")

    return outfits

if __name__ == "__main__":
    prenda_1 = {
        'id': 1,
        'category': 'Coat',
        'dominant_color': '[47,79,79]',
        'url': 'image_1.jpg'
    }
    prenda_2 = {
        'id': 2,
        'category': 'Trouser',
        'dominant_color': '[169,169,169]',
        'url': 'image_2.jpg'
    }
    prenda_3 = {
        'id': 3,
        'category': 'Sneaker',
        'dominant_color': '[210,180,140]',
        'url': 'image_3.jpg'
    }

    all_data_for_generation = [prenda_1, prenda_2, prenda_3]
    
    selected_items = {
        'superior': prenda_1  # Simular que el usuario ha seleccionado una prenda superior
    }

    model_path = 'Outfit_Generator_Model.h5'
    outfits = Fn_generate_outfits(model_path, selected_items, all_data_for_generation)
    print(outfits)
