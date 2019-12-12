import argparse

#using argparse to get the information about language, folder and text from CLI
parser = argparse.ArgumentParser("")
parser.add_argument('-s', dest='show', action='store_true', default=False, help="show the simulation live")
parser.add_argument('-r', dest='repeat', action='store_true', default=False, help='repeat after finish WIP')
parser.add_argument('-wf', dest='write_to_file', action='store_true', default=False, help='write everything to a file instead of to the console / screen')
parser.add_argument('-hl', dest='headless', action='store_true', default=False, help='weather the programm is run on a server')
parser.add_argument('-sp', dest='skip_plot', action='store_true', default=False, help='Skip the plotting and output as video')

parser.add_argument('-o', dest='outputName', action='store', default='simulationOutput', help='name of the output files')
parser.add_argument('-c', dest='dayCount', action='store', default=300, help='cutoff day')
parser.add_argument('-pc', dest='plantCount', action='store', default=20, help='set the initial amount of plants')
parser.add_argument('-rc', dest='rabbitCount', action='store', default=20, help='set the initial amount of rabbits')
parser.add_argument('-fc', dest='foxCount', action='store', default=20, help='set the initial amount of foxes')

args = parser.parse_args()

from mpl_toolkits.mplot3d import axes3d
import numpy as np
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

rand = random.uniform
root = math.sqrt

global animals
animals = []
global plants
plants = []
global counter
counter = 0
global speed
global rabbitCount
global foxCount
global dievalue
global birth_time
birth_time = []
global v_dist
v_dist = []
global n_v_dist
n_v_dist = []
global speed_counter
speed_counter = 0
global animal_born
animal_born = []
dievalue = 199
global x_plot
global y_plot
global z_plot
x_plot = []
y_plot = []
z_plot = []
speed = []
rabbitCount = []
foxCount = []
global e 
e = math.e
global pi
pi = math.pi

global windowWidth
global windowHeight
functionalPlantCountForFullSizedWindow = 100
windowHeight = round(990 / float(functionalPlantCountForFullSizedWindow) * math.sqrt(float(args.plantCount)))
windowWidth = round(1850 / float(functionalPlantCountForFullSizedWindow) * math.sqrt(float(args.plantCount)))
#das hier legt irgendwann mal die Feldgroesse fest

if args.show:
    dsize = (1850, 990)
    pygame.init()
    win = pygame.display.set_mode(dsize)

global logfile
global logpath 
try:
    os.mkdir(args.outputName)
    logfile = open(args.outputName + "/log.txt", "w")
    logpath = args.outputName
except:
    os.mkdir(args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", ""))
    logfile = open(args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", "")+ "/log.txt", "w")
    logpath = args.outputName + datetime.datetime.now().strftime("%H:%M:%S").replace(":", "")


try:
    os.mkdir('tmp')
except:
    pass

def logToFile(string):
    logfile.write(str(string) + "\n")

def log(string):
    print string
    logToFile(string)

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
    def __init__(self, pos, age, dad, mome):
        #if faster more hunger
        self.pos = pos
        self.sex = bool(random.getrandbits(1))
        self.dad = dad
        self.mome = mome
        self.v = self.mutate()#you got a stroke
        self.sens = 300
        self.hung = 50
        self.dir = [None, None]
        self.sexd = 100
        self.fuckedAlready = 0
        self.age = age
        self.ex = []
        self.target = None
        self.hungi = 2

    def mutate(self):
        #round speed to int
        #save in array
        #len of array for each speed is n_v_dist
        #if no parents m = 5
        #v = 5
        #define speed
        if self.dad == None:
            m = 5#adjust
        else:
            m = (self.dad.v + self.mome.v) / 2
        x = rand(-5, 5)
        s = 3 #sigma should be abjusted
        v = abs(1/(s*root(2*pi))*e**((-1/2)*((x-m)/s)**2))

        #data for plot
        animal_born.append([int(v), counter]) 

        return v

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
            self.dir = [0, self.v]
        elif dx == 0 and dy < 0:
            self.pos[1] -= self.v
            self.dir = [0, -1*self.v]
        elif dy == 0 and dx > 0:
            self.pos[0] += self.v
            self.dir = [self.v, 0]
        elif dy == 0 and dx < 0:
            self.pos[1] -= self.v
            self.dir = [-1*self.v, 0]
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
            log("age" + str(self.__class__.__name__))
            animals.remove(self)

    #starve as i please
    def starve(self):
        x = random.uniform(0, 2)
        #print x, val, a
        if x < self.hung / dievalue:
            log("starve" + str(self.__class__.__name__))
            animals.remove(self)

    #eat palnst or rabbits
    def eat(self):
        if self.target in plants:
            plants.remove(self.target)
            genplants()
            self.hung -= 50

        if isinstance(self.target, Rabbit): 
            animals.remove(self.target)
            log("eaten")
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
            animals.append(Rabbit([self.pos[0] + 5, self.pos[1] + 5], 0, self, self.target))# please no random position
            self.hung += 20#rest in animal
            self.sexd -= 50
            self.ex.append([self.target, 50])
            self.target.ex.append([self, 50])
            self.fuckedAlready = 6
        else:
            animals.append(Fox([self.pos[0] + 5, self.pos[1] + 5], 0, self, self.target))
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
        
        
        for animal in animals:
            if self.distance(animal) <= self.sens and isinstance(animal, Rabbit):
                if self.hung / dievalue < 1.6 and self.sexd > 50 and self.fuckedAlready == 0:
                    if self.age > 100:
                        if animal.age > 100 and self.sex != animal.sex:
                            if self.sex == 1 and self not in animal.ex:
                                #if all criterial met add to patrners
                                mate.append(animal) 
            if self.distance(animal) <= self.sens and isinstance(animal, Fox):
                #finclosest fox
                self.target = animal
                self.run()
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
            
    def run(self): 
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
    animals.append(Rabbit([rand(20, 1780), rand(20, 970)], rand(0, 100), None, None))
for i in range(int(args.foxCount)):
    animals.append(Fox([rand(20, 1780), rand(20, 970)], rand(0, 100), None, None))


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
    speed_counter = 0
    v_dist = []
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
        animal.hung += animal.hungi
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
        #count what is fox and Rabbit
        if isinstance(animal, Rabbit):
            rabbitcounter += 1
        elif isinstance(animal, Fox):
            foxcounter += 1
        else:
            log(animal.__class__.__name__)
    counter += 1
    log(str(endtime - starttime) + " " + str(counter) + " " + str(foxcounter) + " " + str(rabbitcounter) + " " + str(len(plants)))
    speed.append((endtime - starttime)*1000)
    #day of sim
    # x.append(counter)
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
            y_plot[-1].append(iasdf)
            z_plot[-1].append(iasdf)
            iasdf += 1
    
    if counter == int(args.dayCount) or rabbitcounter == 0 or foxcounter == 0:
        running = False
        if not args.skip_plot:
            img_array = []
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
                ax.set_ylabel('rabbit count')
                ax.set_zlim3d(minz, maxz)
                ax.set_zlabel('rabbit count')
                ax.scatter(x_plot[i], y_plot[i], z_plot[i])

                fig.savefig(os.getcwd() + '/tmp/'+ format(i, '010d'), dpi=300)

                plt.close(fig)

                if math.floor(i/len(x_plot)) != toolbar_progress_current:
                    toolbar_progress_current = i/len(x_plot)
                    sys.stdout.write("-")
                    sys.stdout.flush()

            log('creating movie from images')
            size = 0
            for filename in glob.glob(os.getcwd() + '/tmp/*.png'):
                print filename
                img = cv2.imread(filename)
                height, width, layers = img.shape
                size = (width,height)
                img_array.append(img)

            out = cv2.VideoWriter(logpath + '/video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
            print size
            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()       
            log('cleaning up')

            import shutil
            shutil.rmtree('tmp')
            log('finished')
        #fig, ax1 = plt.subplots()
        #plt.title("Startwerte:\nHasen: " + str(args.rabbitCount) + " Fuechse: " + str(args.foxCount) + " Pflanzen: " + str(args.plantCount))
        #ax1.set_xlabel('time (d)')
        #ax1.set_ylabel('Foxes (green)\nRabbits (blue)', color='black')
        #ax1.plot(x, foxCount, color='green')
        #ax1.tick_params(axis='y', labelcolor='black')
        
        #ax1.plot(x, rabbitCount, color = 'blue')

        #fig.tight_layout()

        #trying to plot time developement of speed ditribution
        # x = []
        # y = []
        # z = []
        # v = []#index = v, val = anzahl der tiere
        # tmax = 0


        # for i in range(len(animal_born)):
        #     #print animal_born[i][0], len(v)
        #     while animal_born[i][0] > len(v):
        #         v.append(0)
        # #noch sowas aehnliches fuer t
        # for i in range(len(animal_born)):
        #     if animal_born[i][1] > tmax:
        #         tmax = animal_born[i][1]

        # for i in range(len(animal_born)):
        #     for k in range(len(v)):
        #         if animal_born[i][0] == k:
        #             v[k] += 1
        # for i in range(tmax):
        #     x.append(i)
        # for i in range(len(v)):
        #     y.append(i)
        #     z.append(v[i])
            
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection = '3d')
        # #for i in range(len(z)):
        #     #print x[i], y[i], z[i]
        # print len(x), len(y), len(z)
        # ax.set_xlabel('time in d')
        # ax.set_ylabel('speed')
        # ax.set_zlabel('number of animals')
        # ax.plot_surface(x, y, z, rstride = 1, cstride = 1)
        
        # if not args.write_to_file:
        #     plt.show()
        #     log("test")
        # else:
        #     plt.savefig(logpath + "/plot.png")
