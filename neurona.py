from tensorflow.keras.layers import Dense
from tensorflow.keras import Sequential

#Variables: 3 sensores, posicion (x,y), velocidad
#Salidas: derecha, adelante, izquierda

class Cerebro:

    def __init__(self):
        entrada = Dense(units=6, input_shape=(6,))
        oculta = Dense(units=12, activation='relu')
        salida = Dense(units=3, activation='sigmoid')
        self.modelo = Sequential([entrada, oculta, salida])
    
    def predice(self, entradas):
        prediccion = self.modelo.predict(entradas)
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
    
    def actualiza_pesos(self, weights):
        self.modelo.set_weights(weights)