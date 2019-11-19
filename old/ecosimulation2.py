import pygame
import random
import math

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
    plants.append([rand(20, 1780), rand(20, 970)])
    drawplants()

def drawplants():
    for plant in plants:
        pygame.draw.rect(win, (0, 80, 0), (plant[0], plant[1] ,20, 20))

class Animal:
    def __init__(self, pos):
        self.pos = pos
        self.v = 10
        self.hung = 100 #abjust randomly
        self.thurst = 100000 #adjust
        self.sex = bool(random.getrandbits(1))
        self.sexd = 10
        self.sens = 300
        self.targets = []
        self.target = None
        self.efac = 5

    def draw(self):
        if isinstance(self, Rabbit):
            color = (86, 73, 76)
        else:
            color = (232, 66, 0)
        print self.pos
        pygame.draw.rect(win, color, (self.pos[0], self.pos[1], 20, 20))

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

    def eat(self):
        if self.target in plants:
            plants.remove(self.target)
        if self.target in animals:
            animals.remove(self.target)
        self.hung -= 50

    def mate(self):
        if isinstance(self, Fox):
            animals.append(Fox(self.pos))
        else:
            animals.append(Rabbit(self.pos))
        self.sexd = 0
        self.target.sexd = 0


    def movetargeted(self):
        
        if isinstance(self.target, Animal):

            dx = self.target.pos[0] - self.pos[0]
            dy = self.target.pos[1] - self.pos[1]
        else:

            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]
        if math.sqrt(dx ** 2 + dy ** 2) < self.v:
            if isinstance(self, Rabbit):
                if self.target in plants:
                    self.eat()
                else:
                    self.mate()
            if isinstance(self, Fox):
                if isinstance(self.target, Rabbit):
                    self.eat()
                else:
                    self.mate()

        elif dx == 0:
            self.pos[1] += self.v
        elif dy == 0:
            self.pos[0] += self.v
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


    def findclosest(self, targets, sort):
        closest = [None, 78378378]
        
        for target in targets:
            if target[1] < closest[1]:
                closest = target
        #change later
        self.targets.append([closest[0], sort])


    def distance(self, target):
        if isinstance(target, Animal):
            dx = target.pos[0] - self.pos[0]
            dy = target.pos[1] - self.pos[1]
        else:    
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
        d = root(dx ** 2 + dy ** 2)
        return d


    def inrange(self):
        print 'inrarnage'
        eat_d = []
        mate_d = []
        if isinstance(self, Rabbit):
            #find closest one
            for plant in plants:
                d = self.distance(plant)
                if d < self.sens:
                    eat_d.append([plant, d])

            for animal in animals:
                if isinstance(animal,Rabbit):
                    if animal.sex != self.sex:
                        d = self.distance(animal)
                        if d < self.sens:
                            if animal.sex != self.sex:
                                mate_d.append([animal, d])
                #flee
                else:
                    pass
        else:
            for animal in animals:
                d = self.distance(animal)
                if d < self.sens:
                    if isinstance(animal, Rabbit):
                        eat_d.append([animal, d])
                    else:
                        if animal.sex != self.sex:
                            mate_d.append([animal, d])
                    
        if len(eat_d) != 0:
            self.findclosest(eat_d, self.hung)
        if len(mate_d) != 0:
            self.findclosest(mate_d, self.sexd)

        self.choosetarget()

    def choosetarget(self):
        print 'check'
        #sort needs int an array
        needs = [self.hung, self.sexd, self.thurst]
        for i in range(len(needs)-1, 0, -1):
            for j in range(i):
                if needs[j] < needs[j+1]:
                    temp = needs[j]
                    needs[j] = needs[j+1]
                    needs[j+1] = temp
        state = False
        for need in needs:

            for i in range(len(self.targets)):
                if self.targets[i][1] == need:
                    self.target = self.targets[i][0]
                    state = True
                    break
        if state:
            self.movetargeted()
        else:
            self.target = None 
            self.moverandom()


class Rabbit(Animal):
    #call parent mathod from ckild method
    pass



class Fox(Animal):
    pass

#genplants()
for i in range(10):
    genplants()
    animals.append(Rabbit([rand(20, 1780), rand(20, 970)]))
    animals.append(Fox([rand(20, 1780), rand(20, 970)]))
running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                running = False
    water()
    drawplants()
#    animals.draw
#mainloop
    for animal in animals:
        animal.targets = []
        animal.target = None
        animal.thurst += animal.efac
        animal.hung += animal.efac
        animal.sexd += animal.efac
        animal.inrange()

        animal.draw()    
    pygame.display.update()
    win.fill((0, 255, 0))
