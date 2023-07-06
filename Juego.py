import math
import pygame
import sys
import random
from Carro import Carro
from Mapa import Mapa
from Sensores import Sensores
from genetic import Genetico

pygame.init()

clock = pygame.time.Clock()

screenwidth, screenheight = (480, 640)

screen = pygame.display.set_mode((screenwidth, screenheight))

num_poblacion = 30
num_generaciones = 10
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
    carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo, 0, 0, i])

genetico = Genetico(num_poblacion, num_generaciones, carros)
genetico.crea_poblacion()
carros_ordenados = sorted(genetico.carros, key=lambda item: item[6])

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

def actualiza_carros(nuevo):
    for i in genetico.carros:
        if nuevo[8] == i[8]:
            i = nuevo

font = pygame.font.SysFont('arial', 32)
text1 = font.render('HOLA', True, (0, 0, 0), (255, 255, 255))
text2 = font.render('HOLA', True, (0, 0, 0), (255, 255, 255))
textRect1 = text1.get_rect()
textRect2 = text2.get_rect()
textRect1.center = (100, 50)
textRect2.center = (100, 85)
arriba = "\u2191"
abajo = "\u2193"


while True:

    time = clock.tick(60)/10

    carros_ordenados = sorted(carros_ordenados, key=lambda item: item[6])
    carros_no_chocados = []
    top_y = 0
    for i in range(len(carros_ordenados)):
        actualiza_carros(carros_ordenados[i])
        if carros_ordenados[i][0].damage != True and abs(carros_ordenados[i][5]) < 5 and \
            carros_ordenados[i][7] < 50 and abs(carros_ordenados[i][6]) < 2e3:
            if len(carros_no_chocados) == 0:
                carros_ordenados[i][0].tipo = 'USER'
                top_y = carros_ordenados[i][0].y
                carros_ordenados[i][0].y = screenheight-carros_ordenados[i][0].shape.get_height()-25
            else:
                carros_ordenados[i][0].tipo = 'DUMMY'
                carros_ordenados[i][0].y = carros_no_chocados[0][0].y-\
                    (top_y-carros_ordenados[i][0].y)
            carros_no_chocados.append(carros_ordenados[i])
    carros_ordenados = carros_no_chocados
    if len(carros_ordenados) == 0:
        num_generaciones -= 1
        if num_generaciones != 0:
            carros = []
            for i in range(num_poblacion):
                carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
                sensor = Sensores(carro, screen, road)
                carros.append([carro, sensor, carro.x, velocidad, aceleracion, angulo, 0, 0, i])
            genetico.selecciona_mejores(carros)
            carros_ordenados = sorted(genetico.carros, key=lambda item: item[6])
        else:
            sys.exit()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    
    citizen = 0
    for i in carros_ordenados:
        i[1].Show(i[5])
        prediccion = genetico.poblacion[i[8]].predice(obten_parametros(i))
        if prediccion[1] == 1 and (abs(i[5]) <= 1.55 or abs(i[5]) >= 4.55):
            i[4] = -0.2
            i[7] = 0
        elif prediccion[1] == 1:
            i[4] = 0.2
            i[7] = 0
        else:
            i[4] = 0
            i[7] += 1
        if prediccion[0] == 1:
            i[5] += 0.05
        elif prediccion[2] == 1:
            i[5] -= 0.05

        i[3] += i[4]
        
        i[3] = i[0].Fisicas(i[3], i[4], friccion)

        i[6] += math.cos(i[5])*i[3]
    
        i[2] += math.sin(i[5])*i[3]

        i[0].UpdateCoords(i[2], road, carros_ordenados[0][3], i[3])
        
        if citizen == 0:
            road.UpdateCoords(i[3], time)

            road.Show(screen)
        
        if i[5] == 0:
            i[0].Show(screen, i[5])
        else:
            i[0].Rotate(screen, i[5])

        i[1].Show(i[5])
        citizen += 1
    
    if len(carros_ordenados) != 0:
        text1 = f"Velocidad actual: {str(round(abs(carros_ordenados[0][3]), 3))} "+\
        f"{arriba if carros_ordenados[0][3] < 0 else abajo}"
        text2 = f"Quedan: {str(len(carros_ordenados))}"
        screen.blit(font.render(text1, True, (0, 0, 0), (255, 255, 255)), textRect1)
        screen.blit(font.render(text2, True, (0, 0, 0), (255, 255, 255)), textRect2)

    pygame.display.update()