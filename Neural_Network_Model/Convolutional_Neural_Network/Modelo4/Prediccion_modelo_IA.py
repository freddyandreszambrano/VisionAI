from keras.models import load_model

# Cargar el modelo incluyendo las capas de MobileNet
modelo = load_model("modelo_IaOutit.keras")

# Revisar la arquitectura del modelo cargado
modelo.summary()

