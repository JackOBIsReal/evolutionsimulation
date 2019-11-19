import turtle
import time
import os
import math
import random

global animals
animals = []
global bunnies
bunnies = []
global dbunnies
dbunnies = []
global plants
plants = []
global dplants
dplants = []
global foxes
foxes = []
global dfoxes
dfoxes = []
#age

#adapt to the number of plants missing

#generating new plants
def genplants():
    plants.append([random.uniform(-480, 480), random.uniform(-480, 480)])
    dplants.append(turtle.Turtle())
    dplants[len(dplants)-1].shape('triangle')
    dplants[len(dplants)-1].penup()
    dplants[len(dplants)-1].color('green')
    dplants[len(dplants)-1].speed(0)
    dplants[len(dplants)-1].setheading(90)
    dplants[len(dplants)-1].setposition(plants[len(plants)-1])

#gen new bunnies
def newbunny(pos, speed, sens):
   bunnies.append(Bunny(pos, speed, sens))
   dbunnies.append(turtle.Turtle())
   dbunnies[len(dbunnies)-1].shape('square')
   dbunnies[len(dbunnies)-1].penup()
   dbunnies[len(dbunnies)-1].color('red')
   dbunnies[len(dbunnies)-1].speed(0)
   dbunnies[len(dbunnies)-1].setposition(pos)

#Bunny class
class Bunny:
    #constructor
    def __init__(self, pos, speed, sens):# sexdrive, thurst, hunger):
        self.pos = pos
        self.speed = speed
        self.sens = sens
        animals.append(self)
        #self.sexdrive = sexdrive
        #self.thurst = thurst
        #self.hunger = hunger


    #collision detection
    def collision(self):
        #other animals, Border, water
        if self.pos[0]<-480:
            self.pos[0] = -480
        if self.pos[0]>480:
            self.pos[0]=480
        
        if self.pos[1]<-480:
            self.pos[1] = -480
        if self.pos[1]>480:
            self.pos[1]=480

    #make th bunny move randomly
    def moverandom(self): 
        x = random.randint(-1, 1)
        self.pos[0] +=x * self.speed
        x = random.randint(-1, 1)
        self.pos[1] +=x * self.speed
        self.collision()
        for i in range(len(bunnies)):            
            if bunnies[i] == self:
                dbunnies[i].setposition(self.pos)
                break
    #measure distance
    def distance(self):
        closest = 45646464 
        for plant in plants:
            dx = abs(self.pos[0]-plant[0])
            dy = abs(self.pos[1]-plant[1])
            d = math.sqrt(dx**2 + dy**2)
            if d < closest:
                closest = d
                
                target = plant
        
        return closest, target


    #improve movement pattern
    #dx/dy * Pythagoras
    def movetargeted(self, target):
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        while math.sqrt(dx**2+dy**2)>self.speed:
            mx = dx/dy
            my = dy/dx
            d = math.sqrt(mx**2+my**2)
            mx *=(self.speed/d)
            my *=(self.speed/d)
            #doodoo
            if dx > 0:
                self.pos[0] += abs(mx)
            if dy > 0:
                self.pos[1] += abs(my)
            
            if dx < 0:
                self.pos[0] -= abs(mx)
            if dy < 0:
                self.pos[1] -= abs(my)

            for i in range(len(bunnies)):
                if bunnies[i] == self:
                    dbunnies[i].setposition(self.pos)           
            
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]
    
    #bunny eats a plant
    #doesnnt eat new plants
    def eat(self, target):
        i = plants.index(target)
        dplants[i].hideturtle()
        dplants.pop(i)
        plants.pop(i)
        genplants()


#gen new foxes
def newfox(pos, speed, sens):
   foxes.append(Fox(pos, speed, sens))
   dfoxes.append(turtle.Turtle())
   dfoxes[len(dfoxes)-1].shape('square')
   dfoxes[len(dfoxes)-1].penup()
   dfoxes[len(dfoxes)-1].color('orange')
   dfoxes[len(dfoxes)-1].speed(0)
   dfoxes[len(dfoxes)-1].setposition(pos)

#fox class
class Fox:
    #constructor
    def __init__(self, pos, speed, sens):
        self.pos = pos
        self.speed = speed
        self.sens = sens
        animals.append(self)

    #make th bunny move randomly
    def moverandom(self): 
        x = random.randint(-1, 1)
        self.pos[0] +=x * self.speed
        x = random.randint(-1, 1)
        self.pos[1] +=x * self.speed
        self.collision()
        for i in range(len(foxes)):            
            if foxes[i] == self:
                dfoxes[i].setposition(self.pos)
                break

    #collision detection
    def collision(self):
        #other animals, Border, water
        if self.pos[0]<-480:
            self.pos[0] = -480
        if self.pos[0]>480:
            self.pos[0]=480
        
        if self.pos[1]<-480:
            self.pos[1] = -480
        if self.pos[1]>480:
            self.pos[1]=480
        
    def distance(self):
        closest = 45646464 
        for bunny in bunnies:
            dx = abs(self.pos[0]-bunny.pos[0])
            dy = abs(self.pos[1]-bunny.pos[1])
            d = math.sqrt(dx**2 + dy**2)
            if d < closest:
                closest = d
                target = bunny.pos
        return closest, target

    def movetargeted(self, target):
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        while math.sqrt(dx**2+dy**2)>self.speed:
            mx = dx/dy
            my = dy/dx
            d = math.sqrt(mx**2+my**2)
            mx *=(self.speed/d)
            my *=(self.speed/d)
            #doodoo
            if dx > 0:
                self.pos[0] += abs(mx)
            if dy > 0:
                self.pos[1] += abs(my)
            
            if dx < 0:
                self.pos[0] -= abs(mx)
            if dy < 0:
                self.pos[1] -= abs(my)

            for i in range(len(foxes)):
                if foxes[i] == self:
                    dfoxes[i].setposition(self.pos)           
            
            dx = target[0] - self.pos[0]
            dy = target[1] - self.pos[1]

    def eat(self, target):
        for i in range(len(bunnies)-1):
            if bunnies[i].pos == target:
                dbunnies[i].hideturtle()
                dbunnies.pop(i)
                bunnies.pop(i)





#setup screen
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Space time")

#border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("black")
border_pen.penup()
border_pen.setposition(-500, -500)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(1000)
    border_pen.lt(90)
border_pen.hideturtle()

#create object for each animal with values position, hunger, thirst,
#horneyness
#genes:pregnancy duration, speed(bad for hunger), hotness, speed of 
#getting horney,
#beak move targeted if bunney gets avay

for i in range(50):
    genplants()
for i in range(20):
    newbunny([random.uniform(-480, 480), random.uniform(-480, 480)], 10, 100)
for i in range(10):
    newfox([random.uniform(-480, 480), random.uniform(-480, 480)], 15, 100)
while True:
    for animal in animals:
        animal.moverandom()
        distance, target = animal.distance()

        if distance < animal.sens:
            animal.movetargeted(target)
            animal.eat(target)
            
raw_input('jksdafkja')
