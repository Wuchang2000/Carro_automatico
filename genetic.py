import numpy as np
from neurona import Cerebro

class Genetico:
    def __init__(self, num_poblacion, num_generaciones, carros):
        self.num_poblacion = num_poblacion
        self.poblacion = []
        self.carros = carros
        self.generaciones = num_generaciones
        self.mejor = None
    
    def crea_poblacion(self):
        for i in range(self.num_poblacion):
            self.poblacion.append(Cerebro())
    
    def selecciona_mejores(self, carros):
        self.carros = sorted(self.carros, key=lambda item: item[6])
        if self.mejor == None or self.mejor[0][6] < self.carros[0][6]:
            self.mejor = [self.carros[0], self.poblacion[self.carros[0][8]]]
        for i in range(0, self.num_poblacion, 2):
            self.mezcla(self.poblacion[self.carros[i][8]], self.poblacion[self.carros[i+1][8]])
        self.carros = carros
        for i in self.poblacion:
            i.nuevo_interprete()
    
    def mezcla(self, padre1, padre2):
        for i in range(len(padre1.modelo.layers)):
            pesos_p1 = padre1.modelo.layers[i].get_weights()[0]
            pesos_p2 = padre2.modelo.layers[i].get_weights()[0]
            mitad1 = np.shape(pesos_p1)[0]
            mitad2 = np.shape(pesos_p1)[1]
            salida = np.shape(padre1.modelo.layers[i].get_weights()[1])[0]
            indice1 = np.random.randint(round(mitad1/2)-1, mitad1-1)
            indice2 = mitad1-indice1
            mitad1_nuevo_peso1 = pesos_p1[:indice1, :]
            mitad2_nuevo_peso1 = pesos_p1[indice1:, :]
            mitad1_nuevo_peso2 = pesos_p2[:indice2, :]
            mitad2_nuevo_peso2 = pesos_p2[indice2:, :]
            fusionada1 = np.concatenate((mitad1_nuevo_peso1, mitad1_nuevo_peso2))
            fusionada2 = np.concatenate((mitad2_nuevo_peso1, mitad2_nuevo_peso2))
            # nuevo_peso1 = np.split(pesos_p1, 2)
            # nuevo_peso2 = np.split(pesos_p2, 2)
            # fusionada1 = np.concatenate((nuevo_peso1[0], nuevo_peso2[0]), axis=0)
            # fusionada2 = np.concatenate((nuevo_peso1[1], nuevo_peso2[1]), axis=0)
            fusionada1, fusionada2 = self.mutacion(fusionada1, fusionada2)
            peso_hijo1 = [
                fusionada1.reshape(mitad1, mitad2),
                np.zeros((salida,))
            ]
            peso_hijo2 = [
                fusionada2.reshape(mitad1, mitad2),
                np.zeros((salida,))
            ]
            padre1.modelo.layers[i].set_weights(peso_hijo1)
            padre2.modelo.layers[i].set_weights(peso_hijo2)

    def mutacion(self, hijo1, hijo2):
        for hijo in [hijo1, hijo2]:
            for fila in hijo:
                for elemento in fila:
                    if np.random.rand() > 0.02:
                        elemento = np.random.uniform(-1.0, 1.0)
        
        return hijo1, hijo2
    
    def exportaMejor(self):
        self.mejor[1].exporta()