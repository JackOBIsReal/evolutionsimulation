import pygame
import random
import math

global aniamls
animals = []
global plants
plants = []

pygame.init()
win = pygame.display.set_mode((500, 500))

def water():
    pos = [[120, 70], [70, 120], [250, 250]]
    for i in pos:
        pygame.draw.rect(win, (0, 0, 255), (i[0], i[1] ,80, 80))

def genplants():
    x = random.uniform(20, 480)
    y = random.uniform(20, 480)
    plants.append([x, y])

def drawplants():
    for plant in plants:
        pygame.draw.rect(win, (0, 80, 0), (plant[0], plant[1] ,20, 20))

class Animal:
    def __init__(self, pos, speed, sens):
        self.pos = pos
        self.speed = speed
        self.sens = sens
        self.hunger = 100
        self.thirst = 100
        self.sex =  bool(random.getrandbits(1))
        self.sexd = 100
        #collison


    def draw(self):
        if isinstance(self, Rabbit):
            color = (86, 73, 76)
        else:
            color = (232, 66, 0)
        pygame.draw.rect(win, color, (self.pos[0], self.pos[1] ,20, 20))

    #nicht ins wasser 
    def collision(self):
        if self.pos[0] < 20 :
             self.pos[0] = 20       
        if self.pos[0] > 480:
            self.pos[0] = 480

        if self.pos[1] < 20:
             self.pos[1] = 20       
        if self.pos[1] > 480:
            self.pos[1] = 480

    #improve movement pattern
    def moverandom(self):
        dx = random.randint(-1, 1) * self.speed
        dy = random.randint(-1, 1) * self.speed
        self.pos[0] += dx
        self.pos[1] += dy
        self.collision()

    def distance(self, target):
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        d = math.sqrt(dx ** 2 + dy ** 2)
        return d
    
    #inrange muss uber mates, wasser und essen und drei objekte zurueck geben die sichtbar sind
    #wasser
    def inrange(self):
        target = None
        closest = 84327
        #generieren der arrays in in denen distance aller objekte und die ojbekte selbst gespeichert werden
        drink_d = []
        eat_d = []
        mate_d = []
        predit_d = []
        #wasser bezieht sich noch auf den Mittelpunkt(die groesse benutzen zum fixen)
        for water in waters:
            drink_d.append([self.distance(water), water])
            #go to drink
        #wenn self Rabbit ist
        if isinstance(self, Rabbit)
            for animal in animals:
                #potentieller partner(geschlecht pruefen)
                if isinstance(animal, Rabbit):
                    #go to mate
                    mate_d.append([self.distance(animal), animal])
                #fressfeind
                else:
                    #flee
                    predit_d.apppend([self.distance(animal), animal])

            #pflanzen
            for plant in plants:
                #go to eat
                eat_d.append([self.distance(palnt), plant])
        
        #wenn self Fuchs ist
        else:
            for animal in animals:
                #essen
                if isinstance(animal, Rabbit):
                    #go to eat
                    eat_d.append([self.ditance(animal), animal])
                #potentieller partner(egschlecht pruefen)
                else:
                    #go to mate
                    mate_d.append([self.distance(animal), animal])

        #nach dem naechsten wasser suchen
        drink = [5784325, None]
        for i in range(len(drink_d)):
            if drink_d[i-1][0] < drink[0]:
                drink = drink_d[i-1]
        #checken ob wasser innerhalb von sens ist
        if drink[0] > self.sens:
            drink = None

        #nach dem naechsten essen suchen
        eat = [7543205, None]
        for i in range(len(eat_d)):
            if eat_d[i-1][0] < eat[0]:
                eat = eat_d
        if eat[0] > self.sens:
            eat = None

        #nach dem naechsten Partner suchen
        mate = [7543205, None]
        for i in range(len(mate_d)):
            if mate_d[i-1][0] < mate[0]:
                mate = mate_d
        if mate[0] > self.sens:
            mate = None

        #nach dem naechsten fressfeind suchen
        predit = [7543205, None]
        for i in range(len(predit_d)):
            if predit_d[i-1][0] < predit[0]:
                predit = predit_d
        if predit[0] > self.sens:
            predit = None

        self.drink = drink
        self.eat = eat
        self.mate = mate
        self.predit = predit

    def choose_target(self):
        if self.thurst > self.hunger:





    #krueppel
    #wasser
    def movetargeted(self, target):
#        pygame.time.delay(100)
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        if math.sqrt(dx ** 2 + dy ** 2) < self.speed:
            self.eat(target)
        
        else:
            if dx == 0:
                self.pos[1] += (dy/dy) * self.speed
            if dy == 0:
                self.pos[0] += (dx/dx) * self.speed
            else:
                print dx
                mx = dx / dy
                my = dy / dx
                
                d = math.sqrt(mx ** 2 + my ** 2)
                if dx > 0:
                    self.pos[0] += abs(mx)
                if dy > 0:
                    self.pos[1] += abs(my)
    
                if dx < 0:
                    self.pos[0] -= abs(mx)
                if dy < 0:
                    self.pos[1] -= abs(my)

    def eat(self, target):

        for i in range(len(animals)):
            if animals[i-1].pos == target:
                animals.pop(i-1)
        for i in range(len(plants)):
            if plants[i-1] == target:
                plants.pop(i-1)


class Rabbit(Animal):
    pass


class Fox(Animal):
    pass


for i in range(2):
    genplants()
    animals.append(Rabbit([random.uniform(20, 480), random.uniform(20, 480)], 10, 100))
    animals.append(Fox([random.uniform(20, 480), random.uniform(20, 480)], 10, 100))
while True:
    pygame.time.delay(100)
    water()
    for animal in animals:
        animal.inrange()
        if animal.predit != None:
            animal.flee()
        else: 
            target = animal.choose_target()

        if target == None:
            animal.moverandom()
    
        
        animal.draw()
        drawplants()
        pygame.display.update()
    win.fill((0, 255, 0))
