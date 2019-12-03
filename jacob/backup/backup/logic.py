#age

import random
#adapt to the number of plants missing
#generating new plants
def genplants(num_plants):
    plants = []
    for plant in range(num_plants):
        plants.append([random.randint(-300, 300), random.randint(-300, 300)])
    return plants

class Bunny:
    #constructor
    def __init__(self, pos, speed, sens):# sexdrive, thurst, hunger):
        self.pos = pos
        self.speed = speed
        self.sens = sens
        #self.sexdrive = sexdrive
        #self.thurst = thurst
        #self.hunger = hunger

    #make th bunny move randomly
    def moverandom(self): 
        x = random.randint(-1, 1)
        self.pos[0] +=x * self.speed
        x = random.randint(-1, 1)
        self.pos[1] +=x * self.speed

    #printing position of the bunny to th console
    def printpos(self):
        print self.pos

    #bunny eats a plant
    def eat(self):
        for i in plants:
            if self.pos[0] - plants[i][0]<10 and self.pos[1] - plants[i][1]<10:
                pop.plants[i]
                genplants(1)

b1 = Bunny([0, 0], 10, 100)
#b1.pos = [0, 0]
#b1.speed = 10

plants = genplants(20)

print plants
'''
for i in range(10):
    b1.moverandom()
    b1.printpos()
    '''
