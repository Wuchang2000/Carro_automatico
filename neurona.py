from tensorflow.keras.layers import Dense
from tensorflow.keras import Sequential
import tensorflow as tf
from numpy import array, float32

#Variables: 3 sensores, posicion x, angulo, velocidad
#Salidas: derecha, adelante, izquierda

class Cerebro:

    def __init__(self, carga = False):
        if carga:
            self.usar_modelo()
            self.nuevo_interprete()
        else:
            entrada = Dense(units=6, input_shape=(6,))
            oculta = Dense(units=3, activation='relu')
            salida = Dense(units=3, activation='sigmoid')
            self.modelo = Sequential([entrada, oculta, salida])
            converter = tf.lite.TFLiteConverter.from_keras_model(self.modelo)
            tflite_model = converter.convert()
            self.interprete = tf.lite.Interpreter(model_content=tflite_model)
            self.interprete.allocate_tensors()
    
    def predice(self, entradas):
        entradas = array(entradas).astype(float32)
        self.interprete.set_tensor(self.interprete.get_input_details()[0]["index"], entradas)
        self.interprete.invoke()
        prediccion = self.interprete.get_tensor(self.interprete.get_output_details()[0]["index"])
        prediccion = prediccion[0]
        #Saber si gira a derecha o izquierda
        if prediccion[0] >= 0.5:
            prediccion[0] = 1
            prediccion[2] = 0
        elif prediccion[2] >= 0.5:
            prediccion[0] = 0
            prediccion[2] = 1
        else:
            prediccion[0] = 0
            prediccion[2] = 0
        #Saber si acelera o no
        if prediccion[1] >= 0.5:
            prediccion[1] = 1
        else:
            prediccion[1] = 0

        return prediccion
    
    def nuevo_interprete(self):
        converter = tf.lite.TFLiteConverter.from_keras_model(self.modelo)
        tflite_model = converter.convert()
        self.interprete = tf.lite.Interpreter(model_content=tflite_model)
        self.interprete.allocate_tensors()
    
    def exporta(self):
        self.modelo.save('best_model.h5')

    def usar_modelo(self):
        self.modelo = tf.keras.models.load_model('best_model.h5')