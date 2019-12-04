import argparse

#using argparse to get the information about language, folder and text from CLI
parser = argparse.ArgumentParser("")
parser.add_argument('-s', dest='show', action='store_true', default=False, help="show the simulation live")
parser.add_argument('-r', dest='repeat', action='store_true', default=False, help='repeat after finish WIP')
parser.add_argument('-o', dest='outputName', action='store', default='simulationOutput', help='name of the output files')
parser.add_argument('-c', dest='dayCount', action='store', default=300, help='cutoff day')
parser.add_argument('-pc', dest='plantCount', action='store', default=20, help='set the initial amount of plants')
parser.add_argument('-rc', dest='rabbitCount', action='store', default=20, help='set the initial amount of rabbits')
parser.add_argument('-fc', dest='foxCount', action='store', default=20, help='set the initial amount of foxes')

args = parser.parse_args()

import pygame
import math
import random
import time
import matplotlib.pyplot as plt
import os
import sys
import timeit

rand = random.uniform
root = math.sqrt

global animals
animals = []
global plants
plants = []
global counter
counter = 0
global x
global speed
global rabbitCount
global foxCount
global dievalue
dievalue = 200
x = []
speed = []
rabbitCount = []
foxCount = []
global e 
e = math.e
if args.show:
    if args.show:
        dsize = (1850, 990)
        pygame.init()
        win = pygame.display.set_mode(dsize)


def genplants():
    x = rand(20, 1830)
    y = rand(20, 970)
    ax = x + 10
    ay = y + 10
    plants.append([x, y])

    if args.show:
        drawplants()

def drawplants():
    for plant in plants:
        pygame.draw.rect(win, (0, 80, 0), (plant[0], plant[1] ,10, 10))

class Animal:
    def __init__(self, pos, age):
        self.pos = pos
        self.sex = bool(random.getrandbits(1))
        self.v = 5
        self.sens = 300
        self.hung = 50

        self.sexd = 100
        self.fuckedAlready = 0
        self.age = age
        self.ex = []
        self.target = None

    def resetFuckery(self):
        if self.fuckedAlready > 0:
            self.fuckedAlready -= 1

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

    #check for fobidden areas of the map: water borders
    def collision(self):
        #check borders of map
        if self.pos[0] < 20:
            self.pos[0] = 20
        
        if self.pos[1] < 20:
            self.pos[1] = 20
        if self.pos[0] > 1780:
            self.pos[0] = 1780
        if self.pos[1] > 970:
            self.pos[1] = 970
        #check water
        #warning
        ax = self.pos[0] + 10
        ay = self.pos[1] + 10
    
    #move towards self.target
    def movetargeted(self):
        #define vec to self.target
        if isinstance(self.target, Animal):
            dx = self.target.pos[0] - self.pos[0]
            dy = self.target.pos[1] - self.pos[1]
        else: 
            dx = self.target[0] - self.pos[0]
            dy = self.target[1] - self.pos[1]
        #if self.target is closer than one step
        if self.distance(self.target) < self.v:
            #if self is rabbit
            if isinstance(self, Rabbit):
                #eat plant
                if self.target in plants:
                    self.eat()
                #fuck other rabbits
                if isinstance(self.target, Rabbit) and self.sex != self.target.sex:
                    self.mate()
            #if self is fox
            if isinstance(self, Fox):
                if isinstance(self.target, Rabbit):
                    #eat rabbits
                    self.eat()
                if isinstance(self.target, Fox) and self.sex != self.target.sex: 
                    #fuck other foxes
                    self.mate()
        #check if one of components = 0 because fuck math
        elif dx == 0 and dy > 0:
            self.pos[1] += self.v
        elif dx == 0 and dy < 0:
            self.pos[1] -= self.v

        elif dy == 0 and dx > 0:
            self.pos[0] += self.v
        elif dy == 0 and dx < 0:
            self.pos[1] -= self.v
        else:
            #else normalize vec
            # i forgot to normalize to fucking self.v i guess
            mx = dx / dy
            my = dy / dx
            d = root(mx ** 2 + my ** 2)
            #move in the respective components
            if dx > 0:
                self.pos[0] += abs(mx)
            if dy > 0:
                self.pos[1] += abs(my)

            if dx < 0:
                self.pos[0] -= abs(mx)
            if dy < 0:
                self.pos[1] -= abs(my)
            self.collision()

    #die when i tell you to
    def die(self):
        x = random.uniform(0, 1)
        val = 0.00000001*(e**(-1.0*(self.age)+4.8)+20.0*self.age-4.0)#die of old age 
        
        if x < val:
            animals.remove(self)

    #starve as i please
    def starve(self):
        x = random.uniform(0, 2)
        #print x, val, a
        if x < self.hung / dievalue:
            animals.remove(self)

    #eat palnst or rabbits
    def eat(self):
        if self.target in plants:
            plants.remove(self.target)
            genplants()
            self.hung -= 50

        if isinstance(self.target, Rabbit): 
            animals.remove(self.target)
            self.hung -= 50

    #find closest potetial target
    def findclosest(self, targets):
        #wtf
        if type(targets[0]) == int or type(targets[0]) == float:
            return targets
        #set stupid high number
        closest = [None, 6757865]
        for target in targets:
            #if anything is closer than previous replace
            if isinstance(target, Animal):
                a = self.distance(target.pos)
            else:
                a = self.distance(target)
            if a < closest[1]:
                closest = [target, a]
        return closest[0]
    
    #measure distance to what the hell i want
    def distance(self, target):
        if isinstance(target, Animal):
            #pythagoras
            dx = target.pos[0] - self.pos[0]
            dy = target.pos[1] - self.pos[1]
        else:
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
        return root(dx **2 + dy ** 2)

    #find the best target
    def choosetarget(self):
        #sort according to pressures
        needs = [[self.hung, 'hung'], [self.sexd, 'sex']]
        for i in range(len(needs)-1, 0, -1):
            for j in range(i):
                if needs[j][0] < needs[j+1][0]:
                    temp = needs[j]
                    needs[j] = needs[j+1]
                    needs[j+1] = temp
        #look for matches and define self.target
        for need in needs: 
            if need[1] == 'hung':
                if self.targets[0] != None:
                    self.target = self.targets[0]
                    break
            if need[1] == 'sex':
                if self.targets[1] != None:
                    self.target = self.targets[1]
                    break
    #fuck needs enhancement shitload of it actually
    def mate(self):
        if isinstance(self, Rabbit):
            animals.append(Rabbit([self.pos[0] + 5, self.pos[1] + 5], 0))
        else:
            animals.append(Fox([self.pos[0] + 5, self.pos[1] + 5], 0))
        self.sexd -= 50
        self.ex.append([self.target, 50])
        self.target.ex.append([self, 50])
    
    #remove saved partners after cetrain time
    def clearmates(self):
        for ex in self.ex:
            ex[1] -= 1
            if ex[1] <= 0:
                self.ex.remove(ex)


class Rabbit(Animal):
    
    #find target for self
    def findtarget(self):
        #initiate / reset variables
        self.target = None
        food = []
        mate = []

        self.targets = [None]*2
        d = True
        
        if self.hung / dievalue < 1.5:
            for plant in plants:
                if self.distance(plant) <= self.sens:
                    d = False
                    food.append(plant)
                    #check this
            if len(food) != 0:
                self.targets[0] = self.findclosest(food)
            else:
                self.targets[0] = None
        
        if self.sexd > 30:#self.age > 100:
            for animal in animals:
                if self.distance(animal) <= self.sens and animal.age > 100:
                    if isinstance(animal, Rabbit) and self.sex != animal.sex:
                        if self.sex == 1 and self not in animal.ex:
                            #if all criterial met add to patrners
                            mate.append(animal)
        if len(mate) != 0:
            #find closest partner
            self.targets[1] = self.findclosest(mate)
            d = False

        else:
            self.targets[1] = None

        if d:
            #if nothing in reach
            self.moverandom()
        else:
            self.choosetarget()
            self.movetargeted()
            

    def mate(self):
        if self.hung / dievalue < 1.3 and self.sexd > 50 and self.fuckedAlready == 0:
            animals.append(Rabbit([rand(20, 1780), rand(20, 970)], rand(0, 100)))
            self.hung += 25
            self.sexd -= 50
            self.ex.append([self.target, 50])
            self.target.ex.append([self, 50])
            self.fuckedAlready = 10

class Fox(Animal):
    #same for foxes jus other tastes (more deadly)
    def findtarget(self):
        self.target = None
        food = []
        mate = []
        self.targets = [None]*2
        d = True
        
        for animal in animals:
            if self.distance(animal.pos) <= self.sens:
                if isinstance(animal, Rabbit):
                    
                    food.append(animal)
                    #self.target = self.findclosest(food)
                elif self.age > 100 and self.sex != animal.sex:
                    if self.sex == 1 and self not in animal.ex:
                        
                        mate.append(animal)

        if len(food) != 0:
            self.targets[0] = self.findclosest(food)
            d = False
        else:
            self.targets[0] = None
        
        if len(mate) != 0:
            self.targets[1] = self.findclosest(mate)
            d = False
        else:
            self.targets[1] = None

        if d: 
            self.moverandom()
        else:
            
            self.choosetarget()
            self.movetargeted()

#you didn't comment either
for i in range(int(args.plantCount)):
    genplants()
for i in range(int(args.rabbitCount)):
    animals.append(Rabbit([rand(20, 1780), rand(20, 970)], rand(0, 100)))
for i in range(int(args.foxCount)):
    animals.append(Fox([rand(20, 1780), rand(20, 970)], rand(0, 100)))


running = True

#main

while running:
    starttime = time.time()
    if args.show:
        #check for break
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
    #execute methods for all animals
    for animal in animals:
        animal.resetFuckery()
        animal.collision()
        animal.clearmates()
        animal.findtarget()
        animal.die()
        animal.starve()
    #increment all timedependant variables
    for animal in animals:
        if args.show:
            animal.draw()
        animal.age += 1
        animal.hung += 2
        animal.sexd += 4
    #draw
    if args.show:
        drawplants()
        pygame.display.update()
        win.fill((0, 255, 0))
    endtime = time.time()
    foxcounter = 0
    rabbitcounter = 0
    #matplot i guess
    for animal in animals:
        if isinstance(animal, Rabbit):
            rabbitcounter += 1
        elif isinstance(animal, Fox):
            foxcounter += 1
        else:
            print animal.__class__.__name__
    counter += 1
    print str(endtime - starttime) + " " + str(counter) + " " + str(foxcounter) + " " + str(rabbitcounter) + " " + str(len(plants))
    speed.append((endtime - starttime)*1000)
    x.append(counter)
    rabbitCount.append(rabbitcounter)
    foxCount.append(foxcounter)
    if counter == int(args.dayCount) or rabbitcounter == 0:
        running = False
        fig, ax1 = plt.subplots()
        plt.title("Startwerte:\nHasen: " + str(args.rabbitCount) + " Fuechse: " + str(args.foxCount) + " Pflanzen: " + str(args.plantCount))
        ax1.set_xlabel('time (d)')
        ax1.set_ylabel('Foxes (green)\nRabbits (blue)', color='black')
        ax1.plot(x, foxCount, color='green')
        ax1.tick_params(axis='y', labelcolor='black')
        
        ax1.plot(x, rabbitCount, color = 'blue')

        fig.tight_layout()
        plt.show()
