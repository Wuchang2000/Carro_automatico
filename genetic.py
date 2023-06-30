import numpy as np
from neurona import Cerebro

class Genetico:
    def __init__(self, num_poblacion, num_generaciones, carros):
        self.num_poblacion = num_poblacion
        self.poblacion = []
        self.carros = carros
        self.generaciones = num_generaciones
    
    def crea_poblacion(self):
        for i in range(self.num_poblacion):
            self.poblacion.append(Cerebro())
    
    def selecciona_mejores(self, poblacion_puntos):
        for i in sorted(poblacion_puntos[1]):
            print(i[1])