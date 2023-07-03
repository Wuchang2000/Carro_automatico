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

num_poblacion = 5
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
    carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo])

genetico = Genetico(num_poblacion, num_generaciones, carros)
genetico.crea_poblacion()

def obten_parametros(carro):
    parametros = []
    for distancia in carro[1].toques:
        if distancia == None:
            parametros.append(1)
        else:
            parametros.append(distancia[0][2])
    parametros.append(carro[0].x/screenwidth)
    parametros.append(abs(carro[5])/5)
    parametros.append(abs(carro[3])/max_speed)
    return [parametros]


while True:

    time = clock.tick(60)/10
    
    carros_ordenados = sorted(genetico.carros, key=lambda item: item[3])
    carros_no_chocados = []
    for i in range(len(carros_ordenados)):
        if carros_ordenados[i][0].damage != True and abs(carros_ordenados[i][5]) < 5:
            carros_no_chocados.append(carros_ordenados[i])
    carros_ordenados = carros_no_chocados
    if len(carros_ordenados) == 0:
        num_generaciones -= 1
        if num_generaciones != 0:
            for i in range(num_poblacion):
                carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
                sensor = Sensores(carro, screen, road)
                carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo])

            genetico = Genetico(num_poblacion, num_generaciones, carros)
            genetico.crea_poblacion()
        else:
            sys.exit()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    
    citizen = 0
    for i in carros_ordenados:
        i[1].Show(i[5])
        prediccion = genetico.poblacion[citizen].predice(obten_parametros(i))
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

        print(prediccion)
        i[1].Show(i[5])
        citizen += 1

    pygame.display.update()