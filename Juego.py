import math
import pygame
import sys
import random
from Carro import Carro
from Mapa import Mapa
from Sensores import Sensores
from genetic import Genetico

pygame.init()  # initialize pygame

clock = pygame.time.Clock()

screenwidth, screenheight = (480, 640)

screen = pygame.display.set_mode((screenwidth, screenheight))

num_poblacion = 2
num_generaciones = 1
carros = []

max_speed = 5
aceleracion = 0
friccion = 0.15
velocidad = 0
angulo = 0

pygame.mouse.set_visible(1)

pygame.display.set_caption('Conducción')

road = None
for i in range(num_poblacion):
    carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
    if i == 0:
        road = Mapa(carro.y, screenheight, "road.png")
    sensor = Sensores(carro, screen, road)
    carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo, 0])

genetico = Genetico(num_poblacion, num_generaciones, carros)
genetico.crea_poblacion()

while True:

    time = clock.tick(60)/10
    
    carros_ordenados = sorted(genetico.carros, key=lambda item: item[6])
    carros_no_chocados = []
    for i in range(len(carros_ordenados)):
        if carros_ordenados[i][0].damage != True:
            carros_no_chocados.append(carros_ordenados[i])
    carros_ordenados = carros_no_chocados.copy()
    if len(carros_ordenados) == 0:
        for i in range(num_poblacion):
            carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
            sensor = Sensores(carro, screen, road)
            carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo, 0])

        genetico = Genetico(num_poblacion, num_generaciones, carros)
        genetico.crea_poblacion()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    
    citizen = 0
    for i in carros_ordenados:
        prediccion = genetico.poblacion[citizen].predice([[random.randint(0,7) for _ in range(6)]])
        if prediccion[1] == 1:
            i[4] = -0.2
        else:
            i[4] = 0
        if prediccion[0] == 1:
            i[5] += 0.05
        elif prediccion[2] == 1:
            i[5] -= 0.05

        i[3] += i[4]
        
        i[3] = i[0].Fisicas(i[3], i[4], friccion)
    
        i[2] += math.sin(i[5])*i[3]

        i[0].UpdateCoords(i[2], road, 0)
        
        if citizen == 0:
            road.UpdateCoords(i[3], time)

            road.Show(screen)
        
        if i[5] == 0:
            i[0].Show(screen, i[5])
        else:
            i[0].Rotate(screen, i[5])

        i[1].Show(i[5])
        citizen += 1

    pygame.display.update()