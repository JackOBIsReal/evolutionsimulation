import os
from time import sleep
import random
import math

pc = 500
rc = 500
fc = 150

mv = 10.0
mh = 0.5
ms = 2.0

sens = 300

def startSimulation(mv_f, mh_f, ms_f, sens_f, iteration, number):
    os.system('screen -S "{}_{}" -dm python2.7 ecosimulation.py -c 10000 -sp -o training -hl -pc {} -rc {} -fc {} -mv {} -mh {} -ms {} -sens {}'.format(iteration, number, pc, rc, fc, mv_f, mh_f, ms_f, sens_f))
iteration = 0
def hold():
    active = True
    while active:
        try:
            f1 = open("training1/info.txt")
            f2 = open("training2/info.txt")
            f3 = open("training3/info.txt")
            f4 = open("training4/info.txt")
            f5 = open("training5/info.txt")
            f1.close()
            f2.close()
            f3.close()
            f4.close()
            f5.close()
            active = False
            return False
        except Exception as e:
            if e == IOError:
                sleep(1)
                continue
            if e == KeyboardInterrupt:
                return True

population = []
for i in range(5):
    startSimulation(mv, mh, ms, sens, iteration, i)
population.append([mv, mh, ms, sens])
def sortVal(val): 
    return val[-1]
try:
    population.sort(key=sortVal)
    active = True
    while active
        iteration += 1
        print str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)
        if hold():
            active = False
        dtag = 0
        drabbit = 0
        dfox = 0
        for i in range(1, 6):
            with open('training' + str(i) + '/log.txt') as f:
                tag = 0
                rabbit = 0
                fox = 0
                for line in f:
                    if 'neuerTag' in line:
                        line = line.split(' ')
                        tag = line[1]
                        if line[2] > fox:
                            fox = line[2]
                        if line[3] > rabbit:
                            rabbit = line[3]
                dtag += float(tag) / float(5)
                dfox += float(fox) / float(5)
                drabbit += float(rabbit) / float(5)
        os.system('rm -r training*/')
        print('tage {}, fuechse {}, hasen {}'.format(dtag, dfox, drabbit))
        fittness = dtag
        if drabbit > 2000:
            fittness -= abs(drabbit - 2000)
        if dfox > 2000:
            fittness -= abs(dfox - 2000)

        population[-1].append(fittness)
        population.sort(key=sortVal)

        if len(population) >= 2:
            parents = [population[-1],population[-2]]
            child = [None] * 4

            for i in range(len(child)):
                child[i] = parents[random.randrange(0,2)][i]

            print 'waiting for simulations to end'
            print population
            population.append(child)
            for i in range(5):
                startSimulation(mv, mh, ms, sens, iteration, i)
except:
    print population
    os.system('echo "' + str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)+'\n'+str(population)'" >> long-term-output.txt')