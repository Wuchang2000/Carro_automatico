import math
import pygame


class Sensores:
    def __init__(self, carro, surface, road, trafico):
        self.carro = carro
        self.surface = surface
        self.num_sensores = 3
        self.longitud = 200
        self.separacion = math.pi/4
        self.sensores = []
        self.toques = []
        self.road = road
        # self.trafico = trafico

    def Update(self, angulo):
        self.sensores = []
        for i in range(self.num_sensores):
            t = i/(self.num_sensores-1)
            start = self.separacion/2
            end =- start
            angulo_Interpolado = self.Lerp(start, end, t) + angulo
            inicio =  self.carro.shape.get_rect(topleft = (self.carro.x, self.carro.y)).center
            final = (inicio[0]-math.sin(angulo_Interpolado)*self.longitud, 
                inicio[1]-math.cos(angulo_Interpolado)*self.longitud)
            self.sensores.append([inicio, final])
        self.toques = []
        for i in range(len(self.sensores)):
            self.toques.append(self.Reading(self.sensores[i], self.road.borders))

    def Reading(self, sensores, borders):
        toques = []
        for i in range(len(borders)):
            toque = self.Interseccion(sensores[0], sensores[1],
            borders[i][0], borders[i][1])
            if toque:
                toques.append(toque)
        # for k in self.trafico:
        #     poligono = k.Poligono()
        #     for i in range(len(poligono)):
        #         toque = self.Interseccion(
        #             poligono[i], poligono[(i+1)%len(poligono)],
        #             sensores[0], sensores[1])
        #         if toque:
        #             toques.append(toque)

        if len(toques) == 0:
            return None
        else:
            salidas = list(map(lambda x: x[2], toques))
            minSalida = min(salidas)
            return [x for x in toques if x[2] == minSalida]

    def Interseccion(self, A, B, C, D):
        tTop = (D[0]-C[0])*(A[1]-C[1])-(D[1]-C[1])*(A[0]-C[0])
        uTop = (C[1]-A[1])*(A[0]-B[0])-(C[0]-A[0])*(A[1]-B[1])
        bottom = (D[1]-C[1])*(B[0]-A[0])-(D[0]-C[0])*(B[1]-A[1])

        if bottom != 0:
            t = tTop/bottom
            u = uTop/bottom
            if t >= 0 and t <= 1 and u >= 0 and u <= 1:
                return [self.Lerp(A[0], B[0], t),
                    self.Lerp(A[1], B[1], t),
                    t]
        return None

    def Show(self, angulo):
        self.Update(angulo)
        for i in range(self.num_sensores):
            if self.toques[i]:
                pygame.draw.line(self.surface, (255, 255, 0), 
                self.sensores[i][0], (self.toques[i][0][0], self.toques[i][0][1]), 5)
                pygame.draw.line(self.surface, (0, 0, 0), 
                self.sensores[i][1], (self.toques[i][0][0], self.toques[i][0][1]), 5)
            else:
                pygame.draw.line(self.surface, (255, 255, 0), 
                self.sensores[i][0], self.sensores[i][1], 5)
    
    def Lerp(self, start, end, t):
        return ((1-t)*start)+(t*end)
