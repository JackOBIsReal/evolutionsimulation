import argparse

#using argparse to get the information about language, folder and text from CLI
parser = argparse.ArgumentParser("")
parser.add_argument('-s', dest='show', action='store_true', default=False, help="show the simulation live. Overwrites -pgtf.")
parser.add_argument('-pgtf', dest='pygame_to_file', action='store_true', default=False, help='save the pygame images as a file instead of rendering them on screen')
parser.add_argument('-r', dest='repeat', action='store_true', default=False, help='repeat after finish WIP')
parser.add_argument('-wf', dest='write_to_file', action='store_true', default=False, help='write everything to a file instead of to the console / screen')
parser.add_argument('-hl', dest='headless', action='store_true', default=False, help='weather the programm is run on a server')
parser.add_argument('-sp', dest='skip_plot', action='store_true', default=False, help='Skip the plotting and output as video')
parser.add_argument('-dr', dest='count_death_reason', action='store_true', default=False, help='list the death reasons of the animals')

parser.add_argument('-o', dest='outputName', action='store', default='simulationOutput', help='name of the output files')
parser.add_argument('-fps', dest='fps', action='store', default=15, help='set the fps count of the output videos')
parser.add_argument('-c', dest='dayCount', action='store', default=300, help='cutoff day')
parser.add_argument('-pc', dest='plantCount', action='store', default=20, help='set the initial amount of plants')
parser.add_argument('-rc', dest='rabbitCount', action='store', default=20, help='set the initial amount of rabbits')
parser.add_argument('-fc', dest='foxCount', action='store', default=20, help='set the initial amount of foxes')

args = parser.parse_args()

from mpl_toolkits.mplot3d import axes3d
import numpy as np
import re
if args.show or args.pygame_to_file:
    import pygame
import math
import random
import time
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
if args.headless:
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os
import sys
import timeit
import datetime

import cv2
import numpy as np
import glob

#mathematische Vereinfachungen
rand = random.uniform
root = math.sqrt
global e 
e = math.e
global pi
pi = math.pi

global animals
animals = []
global plants
plants = []
global dayCounter
dayCounter = 0
global speed # in millisekunden die die deltaZeit
speed = []
global rabbitCount # Anzahl hasen/fuechse
rabbitCount = []
global foxCount
foxCount = []
global hungerScalar
hungerScalar = 199
global x_plot #axis of plot
x_plot = []
global y_plot
y_plot = []
global z_plot
z_plot = []

global ageCount
ageCount = [0] * 2
global starveCount
starveCount = [0] * 2
global eatCount
eatCount = 0

global dsize
dsize = (1850, 990)

if args.show:
    #pygame.init()
    win = pygame.display.set_mode(dsize, 0, 32)
elif args.pygame_to_file:
    win = pygame.Surface(dsize)

global logfile
global outputPath 
try:
    os.mkdir(args.outputName)
    logfile = open(args.outputName + "/log.txt", "w")
    outputPath = args.outputName
except:
    os.mkdir(args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", ""))
    logfile = open(args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", "")+ "/log.txt", "w")
    outputPath = args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", "")

try:
    os.mkdir('tmp')
except:
    pass

def log(string): #logs to console and file
    print string
    logfile.write(str(string) + "\n")

def genplant(): #generates the plant
    x = rand(20, dsize[0] - 20)
    y = rand(20, dsize[1] - 20)
    plants.append([x, y])

    if args.show or args.pygame_to_file:
        drawplants()

def drawplants():
    for plant in plants:
        pygame.draw.rect(win, (0, 80, 0), (plant[0], plant[1] ,10, 10))

class Animal:
    def __init__(self, age, dad, mome):
        #if faster more hunger
        self.sex = bool(random.getrandbits(1))
        self.dad = dad
        self.mome = mome
        if self.mome == None:
            self.pos = [rand(0, dsize[0]), rand(0, dsize[1])]
        else:
            self.pos = [self.mome.pos[0]+10, self.mome.pos[1]+10]
        self.mutate()
        self.sens = 300 # TODO austarieren
        self.hung = 50
        self.dir = [None, None]
        self.sexd = 100
        self.fuckedAlready = 0
        self.age = age
        self.ex = []
        self.target = None

    def mutate(self):
        # define speed
        val = 150 # ballance value to be adjusted TODO
        if self.dad == None or self.mome == None:
            mv = 5 # adjust TODO
            mh = 2
            ms = 2 
        else:
            mv = (self.dad.v + self.mome.v) / 2
            mh = (self.dad.hungi + self.mome.hungi) / 2
            ms = (self.dad.sexdi + self.mome.sexdi) / 2

        #adjust TODO
        xv = rand(-5, 5)
        xh = rand(-5, 5)
        xs = rand(-5, 5)
        #use invers on some of th traits
        sv = 3 #sigma should be abjusted TODO
        sh = 3 #sigma should be abjusted TODO
        ss = 3 #sigma should be abjusted TODO
        v = abs(1/(sv*root(2*pi))*e**((-1/2)*((xv-mv)/sv)**2))
        h = abs(1/(sh*root(2*pi))*e**((-1/2)*((xh-mh)/sh)**2))
        s = abs(1/(ss*root(2*pi))*e**((-1/2)*((xs-ms)/ss)**2))
        if v + h + s <= val:
            self.v = v
            self.hungi = h
            self.sexdi = s
        else:
            traits = [v, h, s]
            temp = random.randint(0,2)
            alt = val - traits[(temp+1)%3] - traits[(temp+2)%3]
            while alt <= 0:
                xv = rand(-5, 5)
                xh = rand(-5, 5)
                xs = rand(-5, 5)
                v = abs(1/(sv*root(2*pi))*e**((-1/2)*((xv-m)/sv)**2))
                h = abs(1/(sh*root(2*pi))*e**((-1/2)*((xh-m)/sh)**2))
                s = abs(1/(ss*root(2*pi))*e**((-1/2)*((xs-m)/ss)**2))
                traits = [v, h, s]
                temp = random.randint(0,2)
                alt = val - traits[(temp+1)%3] - traits[(temp+2)%3]
            self.v = v
            self.hungi = h
            self.sexdi = s
            #sum of parameters can't be more than val

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
        if self.pos[0] > dsize[0] - 20:
            self.pos[0] = dsize[0] - 20 
        if self.pos[1] > dsize[1] - 20:
            self.pos[1] = dsize[1] - 20
    
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
       
        else:
            #else normalize vec 
            mx = (dx / (root(dx**2 + dy**2)))*self.v
            my = (dy / (root(dx**2 + dy**2)))*self.v
            self.dir = [mx, my]
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
            if isinstance(self, Rabbit):
                ageCount[0] += 1
            else:
                ageCount[1] += 1
            log("age" + str(self.__class__.__name__))
            animals.remove(self) # i used the stones to destroy the stones

    #starve as i please
    def starve(self):
        x = random.uniform(0, 2)
        #print x, val, a
        if x < self.hung / hungerScalar: # TODO
            if isinstance(self, Rabbit):
                starveCount[0] += 1
            else:
                starveCount[1] += 1
            log("starve" + str(self.__class__.__name__))
            animals.remove(self) # i used the stones to destroy the stones

    #eat palnst or rabbits
    def eat(self):
        if self.target in plants:
            plants.remove(self.target)
            genplant()
            self.hung -= 50 # TODO

        if isinstance(self.target, Rabbit): 
            animals.remove(self.target)
            log("eaten")
            eatCount += 1
            self.hung -= 50 # TODO

    #find closest potetial target
    def findclosest(self, targets):
        if type(targets[0]) == int or type(targets[0]) == float:
            return targets
        #set stupid high number
        closest = [None, dsize[0]**2]
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

    #fuck needs enhancement shitload of it actually TODO
    def mate(self):
        if isinstance(self, Rabbit):
            animals.append(Rabbit(0, self, self.target))# TODO
        else:
            animals.append(Fox([self.pos[0] + 5, self.pos[1] + 5], 0, self, self.target)) # TODO wieder das mit den Eltern
            
        self.hung += 20 # rest in animal TODO
        self.fuckedAlready = 6 # TODO
        self.sexd -= 50 # TODO
        self.ex.append([self.target, 50]) # TODO
        self.target.ex.append([self, 50]) # TODO
    
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
        direction = True
        
        if self.hung / float(hungerScalar) > 0.25: # TODO
            for plant in plants:
                if self.distance(plant) <= self.sens:
                    direction = False
                    food.append(plant)
                    #check this
            if len(food) != 0:
                self.targets[0] = self.findclosest(food)
            else:
                self.targets[0] = None
        
        if self.hung / hungerScalar < 1.6 and self.sexd > 50 and self.fuckedAlready == 0: # TODO lauft immer weg
            if self.age > 100:
                for animal in animals:
                    if self.distance(animal) <= self.sens and isinstance(animal, Rabbit):
                        if animal.age > 100 and self.sex != animal.sex:
                            if self.sex == 1 and self not in animal.ex:
                                #if all criterial met add to patrners
                                mate.append(animal) 
                    elif self.distance(animal) <= self.sens and isinstance(animal, Fox):
                        #finclosest fox
                        self.target = animal
                        self.run()
                        
        if len(mate) != 0: # TODO
            #find closest partner
            self.targets[1] = self.findclosest(mate)
            direction = False
        else:
            self.targets[1] = None

        if direction:
            #if nothing in reach
            self.moverandom()
        else:
            self.choosetarget()
            self.movetargeted()
            
    def run(self): # RUN! da dadadadadadadadadadadadad daaa dadadadadaddaadadada
        self.movetargeted() 
        self.dir[0] *= -2
        self.dir[1] *= -2

        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        self.collision()

class Fox(Animal):
    #same for foxes jus other tastes (more deadly)
    def findtarget(self):
        self.target = None
        food = []
        mate = []
        self.targets = [None]*2
        direction = True

        for animal in animals: # TODO hunger einbauen
            if self.distance(animal.pos) <= self.sens:
                if isinstance(animal, Rabbit):
                    food.append(animal)
                    #self.target = self.findclosest(food)
                elif self.age > 100 and self.sex != animal.sex:
                    if self.sex == 1 and self not in animal.ex:
                        mate.append(animal)

        if len(food) != 0:
            self.targets[0] = self.findclosest(food)
            direction = False
        else:
            self.targets[0] = None
        
        if len(mate) != 0:
            self.targets[1] = self.findclosest(mate)
            direction = False
        else:
            self.targets[1] = None

        if direction: 
            self.moverandom()
        else:
            self.choosetarget()
            self.movetargeted()

#you didn't comment either
#well, you got a point...

#vorbereitung echte Simulation
for i in range(int(args.plantCount)):
    genplant()
for i in range(int(args.rabbitCount)):
    animals.append(Rabbit(rand(0, 100), None, None))
for i in range(int(args.foxCount)):
    animals.append(Fox(rand(0, 100), None, None))


running = True

#main

while running:
    starttime = time.time()
    if args.show:
        # check for break
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
        animal.die()
        animal.starve()
    
    for animal in animals:
        animal.findtarget()
    #increment all timedependant variables
    for animal in animals:
        if args.show or args.pygame_to_file:
            animal.draw()
            print animal.v
        animal.age += 1
        animal.hung += animal.hungi
        animal.sexd += animal.sexdi
    #draw
    if args.show or args.pygame_to_file: # TODO
        drawplants()
        if args.show:
            pygame.display.update()
        elif args.pygame_to_file:
            pygame.image.save(win, "tmp/1" + format(dayCounter, '010d') + ".png")
        win.fill((0, 255, 0))
    endtime = time.time()
    foxcounter = 0
    rabbitcounter = 0
    #matplot i guess
    for animal in animals:
        #count what is fox and Rabbit
        if isinstance(animal, Rabbit):
            rabbitcounter += 1
        elif isinstance(animal, Fox):
            foxcounter += 1
        else:
            log(animal.__class__.__name__)
    dayCounter += 1
    log(str(endtime - starttime) + " " + str(dayCounter) + " " + str(foxcounter) + " " + str(rabbitcounter) + " " + str(len(plants)))
    speed.append((endtime - starttime)*1000)
    #day of sim
    # x.append(dayCounter)
    rabbitCount.append(rabbitcounter)
    foxCount.append(foxcounter)
    #the end

    x_plot.append([])
    y_plot.append([])
    z_plot.append([])

    iasdf = 0
    for animal in animals:
        if isinstance(animal, Rabbit):
            x_plot[-1].append(animal.v) 
            y_plot[-1].append(animal.hungi)
            z_plot[-1].append(animal.sexdi)
            iasdf += 1
    
    if dayCounter == int(args.dayCount) or rabbitcounter == 0 or foxcounter == 0:
        running = False
        if not args.skip_plot:
            log('creating images')

            maxx = 0
            minx = 10000
            maxy = 0
            miny = 10000
            maxz = 0
            minz = 10000
            for i in x_plot:
                for j in i:
                    if maxx <= j:
                        maxx = j
                    if minx >= j:
                        minx = j
                        
            for i in y_plot:
                for j in i:
                    if maxy <= j:
                        maxy = j
                    if miny >= j:
                        miny = j
                        
            for i in z_plot:
                for j in i:
                    if maxz <= j:
                        maxz = j
                    if minz >= j:
                        minz = j

            toolbar_width = 40
            toolbar_progress_current = 0

            sys.stdout.write("[%s]" % (" " * toolbar_width))
            sys.stdout.flush()
            sys.stdout.write("\b" * (toolbar_width+1))

            for i in range(len(x_plot)):
                #log(str(i) + '/' + str(len(x_plot)))

                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                plt.title('Startwerte:\nFuechse: ' + str(args.foxCount) + ' Hasen: ' + str(args.rabbitCount) + ' Pflanzen: ' + str(args.plantCount) + '\nHasen: Blau, Fuechse: Rot')
                ax.set_xlim3d(minx, maxx)
                ax.set_xlabel('speed')
                ax.set_ylim3d(miny, maxy)
                ax.set_ylabel('hunger resistance')
                ax.set_zlim3d(minz, maxz)
                ax.set_zlabel('sexdrive')
                ax.scatter(x_plot[i], y_plot[i], z_plot[i])

                fig.savefig(os.getcwd() + '/tmp/'+ format(i, '010d'), dpi=300)

                plt.close(fig)

                if math.floor(i/len(x_plot)) != toolbar_progress_current:
                    toolbar_progress_current = i/len(x_plot)
                    sys.stdout.write("-")
                    sys.stdout.flush()

            log('creating movie from images')
            size = 0
            img_array = []
            for filename in glob.glob(os.getcwd() + '/tmp/*.png'):
                trueName = re.split('\\\|/', filename)[-1][0]
                if trueName == '0':
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width,height)
                    img_array.append(img)

            out = cv2.VideoWriter(outputPath + '/video.avi', cv2.VideoWriter_fourcc(*'DIVX'), int(args.fps), size)

            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()      

            size = 0
            img_array = []

            for filename in glob.glob(os.getcwd() + '/tmp/*.png'):
                trueName = re.split('\\\|/', filename)[-1][0]
                if trueName == '1':
                    img = cv2.imread(filename)
                    height, width, layers = img.shape
                    size = (width,height)
                    img_array.append(img) 

            out = cv2.VideoWriter(outputPath + '/video2.avi', cv2.VideoWriter_fourcc(*'DIVX'), int(args.fps), size)

            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()

            log('cleaning up')

            import shutil
            shutil.rmtree('tmp')
            
            infofile = open(outputPath + "/info.txt", "w")
            infofile.write('[rabbit, fox]\nstarved: '+str(starveCount)+'\nage: ' + str(ageCount)+'\nrabbits eaten: ' +str(eatCount))
            log('finished')
