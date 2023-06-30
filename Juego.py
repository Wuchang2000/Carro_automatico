import math
import pygame
import sys
from Carro import Carro
from Mapa import Mapa
from Sensores import Sensores

pygame.init()  # initialize pygame

clock = pygame.time.Clock()

screenwidth, screenheight = (480, 640)

screen = pygame.display.set_mode((screenwidth, screenheight))

max_speed = 5
aceleracion = 0
friccion = 0.15
velocidad = 0
angulo = 0
angulo_temp = 0

pygame.mouse.set_visible(1)

pygame.display.set_caption('Condución')

carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
road = Mapa(carro.y, screenheight, "road.png")
# trafico = []
# for i in range(2):
#     trafico.append(Carro(screenheight, screenwidth, False, 'DUMMY', 0, "carro.png"))
sensores = Sensores(carro, screen, road, None)

x = carro.x
y = carro.y

while True:

    if carro.damage:
        carro = Carro(screenheight, screenwidth, False, 'USER', max_speed, "carro.png")
        road = Mapa(carro.y, screenheight, "road.png")
        # trafico = []
        # for i in range(2):
        #     trafico.append(Carro(screenheight, screenwidth, False, 'DUMMY', 0, "carro.png"))
        sensores = Sensores(carro, screen, road, None)
        x = carro.x
        y = carro.y
        aceleracion = 0
        velocidad = 0
        angulo = 0

    time = clock.tick(60)/10

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                aceleracion = -0.2
            elif event.key == pygame.K_DOWN:
                aceleracion = 0.2
            elif event.key == pygame.K_RIGHT:
                angulo -= 0.05
            elif event.key == pygame.K_LEFT:
                angulo += 0.05
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                aceleracion = 0

    velocidad += aceleracion
    
    velocidad = carro.Fisicas(velocidad, aceleracion, friccion)
    
    x += math.sin(angulo)*velocidad
    y += math.cos(angulo)*velocidad 

    carro.UpdateCoords(x, road, 0, None)

    road.UpdateCoords(velocidad, time)

    road.Show(screen)
    
    if angulo == 0:
        carro.Show(screen, angulo)
    else:
        carro.Rotate(screen, angulo)
    
    # for i in trafico:
    #     i.UpdateCoords(x, road, velocidad, None)
    #     i.Show(screen, 0)

    sensores.Show(angulo)

    pygame.display.update()