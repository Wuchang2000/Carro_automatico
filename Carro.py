import pygame
import math
import random

class Carro:

    def __init__(self, screenheight, screenwidth, damage, tipo, max_speed, imagefile):

        self.shape = pygame.image.load(imagefile)
        if tipo == 'USER':
            self.max_speed = max_speed
            self.y = screenheight - self.shape.get_height() - 25
            self.x = screenwidth/2 - self.shape.get_width()/2 + 30
        else:
            self.max_speed = random.randint(1, 5)
            self.y = 461 - 50
            self.x = screenwidth/2 - self.shape.get_width()/2 + random.choice((0, 140, -140))
        self.damage = damage
        self.puntos = []
        self.angulo = 0
        self.tipo = tipo
        self.velocidad = 0

    def Show(self, surface, angulo):
        self.angulo = angulo
        pygame.draw.polygon(surface, (0, 0, 0), self.Poligono())
        surface.blit(self.shape, (self.x, self.y))

    def Rotate(self, surface, angulo):
        self.angulo = angulo
        carro_rotado = pygame.transform.rotate(self.shape, math.degrees(self.angulo))
        new_rect = carro_rotado.get_rect(
            center = self.shape.get_rect(topleft = (self.x, self.y)).center)
        pygame.draw.polygon(surface, (0, 0, 0), self.Poligono())
        surface.blit(carro_rotado, new_rect)

    def Poligono(self):
        self.puntos = []
        x, y = self.shape.get_rect(topleft = (self.x, self.y)).center
        rad = math.hypot(self.shape.get_width(), self.shape.get_height())/2
        alpha = math.atan2(self.shape.get_width(), self.shape.get_height())
        self.puntos.append([x-math.sin(self.angulo-alpha)*rad, y-math.cos(self.angulo-alpha)*rad])
        self.puntos.append([x-math.sin(self.angulo+alpha)*rad, y-math.cos(self.angulo+alpha)*rad])
        self.puntos.append([x-math.sin(math.pi+self.angulo-alpha)*rad, y-math.cos(math.pi+self.angulo-alpha)*rad])
        self.puntos.append([x-math.sin(math.pi+self.angulo+alpha)*rad, y-math.cos(math.pi+self.angulo+alpha)*rad])
        return self.puntos

    def assessDamage(self, borders):
        choques = []
        for i in range(len(borders)):
            if self.interseccionPol(self.Poligono(), borders[i]):
                choques.append(True)
                return True
    
    def interseccionPol(self, poligono, borders):
        for i in range(len(poligono)):
            for j in range(len(borders)):
                touch = self.Interseccion(
                    poligono[i], poligono[(i+1)%len(poligono)],
                    borders[j], borders[(j+1)%len(borders)])
                if touch:
                    return True
        
        return False

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

    def Lerp(self, start, end, t):
        return ((1-t)*start)+(t*end)
    
    def UpdateCoords(self, x, road, velocidad):
        if self.tipo == 'USER':
            self.x = x-self.shape.get_width()/2
            self.damage = self.assessDamage(road.borders)
        else:
            self.velocidad += -1*(self.max_speed*0.1)
            if self.velocidad <= -1*self.max_speed:
                self.velocidad = self.Fisicas(self.velocidad, 0, 0.15)
            
            if velocidad <= self.velocidad:
                self.y -= -1*abs(self.velocidad-velocidad)
            else:
                self.y += self.velocidad+(-1*velocidad)

    def Fisicas(self, velocidad, aceleracion, friccion):
        if abs(velocidad) >= self.max_speed:
            velocidad = velocidad/abs(velocidad) * self.max_speed

        if aceleracion == 0:
            if velocidad > 0:
                velocidad -= friccion
                if velocidad < friccion:
                    velocidad = 0
            elif velocidad < 0:
                velocidad += friccion
                if velocidad > -0.2:
                    velocidad = 0

        return velocidad