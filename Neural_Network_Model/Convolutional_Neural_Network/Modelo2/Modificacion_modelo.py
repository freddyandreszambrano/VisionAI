from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Conv2D




# Cargar el modelo previamente entrenado en formato .keras
modelo = load_model('my_model.keras')
# Verificar la configuración actual de la primera capa
print(modelo.layers[0].get_config())

# Modificar la primera capa para aceptar imágenes en color
modelo.layers[0] = Conv2D(32, (3, 3), activation='relu')

# Compilar el modelo
modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# Guardar el modelo modificado
modelo.save('my_model.keras')

# Cargar el modelo previamente entrenado en formato .h5
modelo = load_model('my_model.keras')

# Verificar la configuración de la primera capa
print(modelo.layers[0].get_config())