import pygame

class Mapa:

    def __init__(self, y, screenheight, imagefile):

        self.img = pygame.image.load(imagefile)
        self.coord = [0, 0]
        self.coord2 = [0, -screenheight]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]

        p = (-1.0, -1000000)
        p1 = (68, y+1000000)
        p2 = (895, y+1000000)
        self.borders = [[p1, p], [p2, p]]

    def Show(self, surface):
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)
    
    def UpdateCoords(self, speed_y, time):
        distance_y = speed_y * time
        self.coord[1] -= distance_y
        self.coord2[1] -= distance_y
        
        if self.coord2[1] >= 0:
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original
        elif self.coord2[1] < self.y2_original:
            self.coord[1] = -self.y2_original
            self.coord2[1] = self.y_original
