import pygame
import math
import random
import time

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


def genplants():
    x = rand(20, 1830)
    y = rand(20, 970)
    ax = x + 10
    ay = y + 10
    for water in waters:
        lbor = water[0][0]
        rbor = water[0][0] + water[1][0]
        tbor = water[0][1]
        bbor = water[0][1] + water[1][1]
        hborders = [tbor, bbor]
        vborders = [lbor, rbor]
        if ax >= water[0][0] and x <= water[0][0] + water[1][0]:
            if ay >= water[0][1] and y <= water[0][1] + water[1][1]:
                closest = [568656, None]

                for i in range(len(vborders)):
                    if abs(vborders[i] - x) < closest[0]:
                        closest = [abs(vborders[i] - x), i]

                for i in range(len(hborders)):
                    if abs(hborders[i] - y) < closest[0]:
                        closest = [abs(hborders[i] - y), i + 2]

                if closest[1] == 0:
                    x = water[0][0] -10
                if closest[1] == 1:
                    x = water[0][0] + water[1][0]
                if closest[1] == 2: 
                    y = water[0][1] - 10
                if closest[1] == 3:
                    y = water[0][1] + water[1][1]
    plants.append([x, y])

    drawplants()

def drawplants():
    for plant in plants:
        pygame.draw.rect(win, (0, 80, 0), (plant[0], plant[1] ,10, 10))

class Animal:
    def __init__(self, pos):
        self.pos = pos
        self.sex = bool(random.getrandbits(1))
        self.v = 5
        self.sens = 300
        self.hung = 100
        self.thurst = 100
        self.sexd = 100
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
            lbor = water[0][0]
            rbor = water[0][0] + water[1][0]
            tbor = water[0][1]
            bbor = water[0][1] + water[1][1]
            hborders = [tbor, bbor]
            vborders = [lbor, rbor]
            if ax >= water[0][0] and self.pos[0] <= water[0][0] + water[1][0]:
                if ay >= water[0][1] and self.pos[1] <= water[0][1] + water[1][1]:
                    closest = [568656, None]

                    for i in range(len(vborders)):
                        if abs(vborders[i] - self.pos[0]) < closest[0]:
                            closest = [abs(vborders[i] - self.pos[0]), i]

                    for i in range(len(hborders)):
                        if abs(hborders[i] - self.pos[1]) < closest[0]:
                            closest = [abs(hborders[i] - self.pos[1]), i + 2]

                    if closest[1] == 0:
                        self.pos[0] = water[0][0] -10
                    if closest[1] == 1:
                        self.pos[0] = water[0][0] + water[1][0]
                    if closest[1] == 2:
                        self.pos[1] = water[0][1] - 10
                    if closest[1] == 3:
                        self.pos[1] = water[0][1] + water[1][1]
    def movetargeted(self):
        if self.target in animals:

            dx = self.target.pos[0] - self.pos[0]
            dy = self.target.pos[1] - self.pos[1]
#        if isinstance(self.target, Rabbit):
#            dx = self.target.pos[0] - self.pos[0]
#            dy = self.target.pos[1] - self.pos[1]
        else:
            
            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]

        if self.distance(self.target) < self.v:
            if isinstance(self, Rabbit):
                if self.target in plants:
                    self.eat()
                if isinstance(self.target, Rabbit) and self.sex != self.target.sex:
                    self.mate()
            if isinstance(self, Fox):
                if isinstance(self.target, Rabbit):
                    self.eat()
                if isinstance(self.target, Fox) and self.sex != self.target.sex:
                   pass
                if self.target in waters:
                   self.thurst -= 50
        
        elif dx == 0 and dy > 0:
            self.pos[1] += self.v
        elif dx == 0 and dy < 0:
            self.pos[1] -= self.v

        elif dy == 0 and dx > 0:
            self.pos[0] += self.v
        elif dy == 0 and dx < 0:
            self.pos[1] -= self.v
        else:
            mx = dx / dy
            my = dy / dx
            d = root(mx ** 2 + my ** 2)
            if dx > 0:
                self.pos[0] += abs(mx)
            if dy > 0:
                self.pos[1] += abs(my)

            if dx < 0:
                self.pos[0] -= abs(mx)
            if dy < 0:
                self.pos[1] -= abs(my)
            self.collision()

    def eat(self):
        
        if self.target in plants:
            plants.remove(self.target)
            genplants()
            self.hung -= 50

        if isinstance(self.target, Rabbit):
            animals.remove(self.target)
            self.hung -= 50



    def findclosest(self, targets):

        if type(targets[0]) == int or type(targets[0]) == float:
            return targets
        closest = [None, 6757865]
        for target in targets:
            if isinstance(target, Animal):
                a = self.distance(target.pos)
            else:
                a = self.distance(target)
            if a < closest[1]:
                closest = [target, a]
        return closest[0]
    
    def distance(self, target):
        if isinstance(target, Animal):
            dx = target.pos[0] - self.pos[0]
            dy = target.pos[1] - self.pos[1]
        else:
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
        return root(dx **2 + dy ** 2)

    def waterdistance(self, water):
        ax = self.pos[0]
        ay = self.pos[1]
        r = None
        if ax < water[0][0]:
            if ay < water[0][1]:
                #obere linke ecke
                r = water[0]
                d = self.distance(water[0])
            elif ay < water[0][1] + water[1][1]:
                #x ditance zur Linken Kante
                r = [water[0][0], self.pos[1]]
                d = abs(water[0][0] - self.pos[0])
            else:
                #untere linke Ecke
                corn = [water[0][0], water[1][1]]
                r = corn
                d = self.distance(corn)
        elif ax < water[0][0] + water[1][0]:
            if ay < water[0][1]:
                #yditance zur oberen Kante
                r = [self.pos[0], water[0][1]]
                d = water[0][1] - self.pos[1]
            elif ay < water[0][1] + water[1][1]:
                #im wasser
                #checken ob das passier
                print 'error'
                self.collision()
            else:
                # Ydistance zur unteren Kante
                p = water[0][1] + water[1][1]
                d = p - self.pos[1]
                r = [self.pos[0], p]
        else:
            if ay < water[0][1]:
                #clsosest point = water[0][0] + water[1][0]
                corn = [water[0][0] + water[1][0], water[0][1]]
                r = corn
                d = self.distance(corn)
            elif ay < water[0][1] + water[1][1]:
                #x ditance rechte Kante
                p = water[0][0] + water[1][0]
                d = p - self.pos[0]
                r = [p, self.pos[1]]
            else:
                #untere rechte Ecke
                corn = [water[0][0] + water[0][1], water[0][1] + water[1][1]]
                r = corn
                d = self.distance(corn)
        return d, r

    def clearmates(self):
        
        for ex in self.ex:
            ex[1] -= 1
            if ex[1] <= 0:
                self.ex.remove(ex)


class Rabbit(Animal):
    
    def findtarget(self):
        food = []
        mate = []
        drinks = []
        self.targets = [None]*3
        d = True
        
        for plant in plants:
            if self.distance(plant) <= self.sens:
                d = False
                food.append(plant)
                #check this
        if len(food) != 0:
            self.targets[0] = self.findclosest(food)
        else:
            self.targets[0] = None
        
        if self.age > 100:
            for animal in animals:
                if self.distance(animal) <= self.sens and animal.age > 100:
                    if isinstance(animal, Rabbit) and self.sex != animal.sex:
                        if self.sex == 1 and self not in animal.ex:
                            d = False
                            mate.append(animal)
        if len(mate) != 0:
            self.targets[1] = self.findclosest(mate)

        else:
            self.targets[1] = None

        for water in waters:
            x = self.waterdistance(water)
            if x[0] <= self.sens:
                d = False
                drinks.append(water)
        if len(drinks) != 0:
            self.targets[2] = self.findclosest(x[1])
        else:
            self.targets[2] = None



        self.choosetarget()

        if d:
            self.moverandom()
        else:
            self.movetargeted()
            
    def choosetarget(self):
        #sort according to pressures
        needs = [[self.hung, 'hung'], [self.sexd, 'sex'], [self.thurst, 'thurst']]
        for i in range(len(needs)-1, 0, -1):
            for j in range(i):
                if needs[j][0] < needs[j+1][0]:
                    temp = needs[j]
                    needs[j] = needs[j+1]
                    needs[j+1] = temp

        for need in needs:
            if need[0] > 0:
                if need[1] == 'hung':
                    if self.targets[0] != None:
                        self.target = self.targets[0]
                        break
                if need[1] == 'sex':
                    if self.targets[1] != None:
                        self.target = self.targets[1]
                        break
                if need[1] == 'thurst':
                    if self.targets[2] != None:
                        self.target = self.targets[2]
                        break

    def mate(self):
        animals.append(Rabbit([self.pos[0] + 5, self.pos[1] + 5]))
        self.sexd -= 50
        self.ex.append([self.target, 50])
        self.target.ex.append([self, 50])

class Fox(Animal):
    def findtarget(self):
        self.target = None
        food = []
        d = True
        
        for animal in animals:
            if isinstance(animal, Rabbit):
                if self.distance(animal.pos) <= self.sens:
                    d = False
                    food.append(animal)
                    #self.target = self.findclosest(food)
        
        if d:
            self.moverandom()
        else:
            self.movetargeted()

water()

for i in range(20):
    genplants()
    animals.append(Rabbit([rand(20, 1780), rand(20, 970)]))
    #animals.append(Fox([rand(20, 1780), rand(20, 970)]))


running = True

#main
while running:
    starttime = time.time()
    water()
    #check for break
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                running = False

    for animal in animals:
        animal.collision()
        animal.clearmates()
        animal.findtarget()


        animal.draw()
        animal.age += 1
        animal.hung += 2
#        animal.thurst += 3
        animal.sexd += 4

    
    drawplants()
    pygame.display.update()
    win.fill((0, 255, 0))
    endtime = time.time()
    print endtime - starttime
