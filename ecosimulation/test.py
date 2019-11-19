import pygame
import math
import random

rand = random.uniform
root = math.sqrt

global animals
animals = []
global plants
plants = []
global waters
waters = []

dsize = (1850, 990)
pygame.init()
win = pygame.display.set_mode(dsize)

def water():
    waters.append([[120, 70], [80, 60]])
    waters.append([[1200, 700], [80, 60]])
    waters.append([[520, 870], [100, 40]])
    waters.append([[720, 200], [400, 700]])
    for water in waters:
        pygame.draw.rect(win, (0, 0, 255), (water[0][0], water[0][1], water[1][0], water[1][1]))



class Animal:
    def __init__(self, pos):
        self.pos = pos
        self.sex = bool(random.getrandbits(1))
        self.v = 10
        self.sens = 300
        self.hung = 0
        self.thurst = 0
        self.sexd = 0
        self.age = 0
        self.ex = []

    def draw(self):
        if isinstance(self, Rabbit):
            if self.sex == 0:
                color = (0, 0, 0)
            else:
                color = (86, 73, 76)
        elif self.sex == 0:
            color = (232, 66, 0)
        else:
            color = (168, 93, 10)
        pygame.draw.rect(win, color, (self.pos[0], self.pos[1], 10, 10))

    def moverandom(self):
        x = rand(-1, 1)
        y = rand(-1, 1)
        self.m = [x, y]
        self.pos[0] += x*self.v
        self.pos[1] += y*self.v
        self.collision()

    def collision(self):

        if self.pos[0] < 20:
            self.pos[0] = 20
        
        if self.pos[1] < 20:
            self.pos[1] = 20
        if self.pos[0] > 1780:
            self.pos[0] = 1780
        if self.pos[1] > 970:
            self.pos[1] = 970

        ax = self.pos[0] + 10
        ay = self.pos[1] + 10
        
        for water in waters:
            lt = water[0]
            rt = [water[0][0] + water[1][0], water[0][1]]
            lb = [water[0][0], water[0][1] + water[1][1]]
            rb = [water[0][0] + water[1][0], water[0][1] + water[1][1]]
            lbor = water[0][0]
            rbor = water[0][0] + water[1][0]
            tbor = water[0][1]
            bbor = water[0][1] + water[1][1]
            borders = [lbor, rbor, tbor, bbor]
            if ax >= water[0][0] and self.pos[0] <= water[0][0] + water[1][0]:
                if ay >= water[0][1] and self.pos[1] <= water[0][1] + water[1][1]:
                    closest = [568656, None]
                    for i in range(len(borders)):
                        if borders[i] < closest[0]:
                            closest = [borders[i], i]
                    if closest[1] == 0:
                        self.pos[0] = water[0][0] -10
                    if closest[1] == 1:
                        self.pos[0] = water[0][0] + water[1][0]
                    if closest[1] == 2:
                        self.pos[1] = water[0][1] - 10
                    if closest[1] == 3:
                        self.pos[1] = water[0][1] + water[1][1]


                        
class Rabbit(Animal):
    pass

for i in range(100):
    #genplants()
    animals.append(Rabbit([rand(20, 1780), rand(20, 970)]))
    #animals.append(Fox([rand(20, 1780), rand(20, 970)]))




running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                running = False
    water()


#mainloop
    for animal in animals:
        animal.moverandom()
        animal.draw()    
    pygame.display.update()
    win.fill((0, 255, 0))


