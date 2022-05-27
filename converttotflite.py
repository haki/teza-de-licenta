import tensorflow as tf

model = tf.keras.models.load_model('models/model.h5')  # Load the model
converter = tf.lite.TFLiteConverter.from_keras_model(model)  # Convert the model

tflite_model = converter.convert()  # Convert the model
open("models/converted_model.tflite", "wb").write(tflite_model)  # Save the model
