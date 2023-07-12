import math
import pygame
import sys
from Carro import Carro
from Mapa import Mapa
from Sensores import Sensores
from neurona import Cerebro

pygame.init()

clock = pygame.time.Clock()

screenwidth, screenheight = (480, 640)

screen = pygame.display.set_mode((screenwidth, screenheight))

pygame.mouse.set_visible(1)

pygame.display.set_caption('Conducción')

max_speed = 5
aceleracion = 0
friccion = 0.15
velocidad = 0
angulo = 0

carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
road = Mapa(carro.y, screenheight, "road.png")
sensor = Sensores(carro, screen, road)
cerebro = Cerebro(True)

x = carro.x
y = carro.y

def obten_parametros():
    parametros = []
    for distancia in sensor.toques:
        if distancia == None:
            parametros.append(1)
        else:
            parametros.append(distancia[0][2])
    parametros.append(carro.x/screenwidth)
    parametros.append(abs(angulo)/5)
    parametros.append(abs(velocidad)/max_speed)
    return [parametros]

while True:

    time = clock.tick(60)/10

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
    
    if carro.damage:
        sys.exit()

    sensor.Show(angulo)
    prediccion = cerebro.predice(obten_parametros())
    if prediccion[1] == 1 and (abs(angulo) <= 1.55 or abs(angulo) >= 4.55):
        aceleracion = -0.2
    elif prediccion[1] == 1:
        aceleracion = 0.2
    else:
        aceleracion = 0
    if prediccion[0] == 1:
        angulo += 0.05
    elif prediccion[2] == 1:
        angulo -= 0.05

    velocidad += aceleracion
    
    velocidad = carro.Fisicas(velocidad, aceleracion, friccion)

    y += math.cos(angulo)*velocidad

    x += math.sin(angulo)*velocidad

    carro.UpdateCoords(x, road, velocidad, velocidad)
    
    road.UpdateCoords(velocidad, time)

    road.Show(screen)
    
    if angulo == 0:
        carro.Show(screen, angulo)
    else:
        carro.Rotate(screen, angulo)

    sensor.Show(angulo)

    pygame.display.update()