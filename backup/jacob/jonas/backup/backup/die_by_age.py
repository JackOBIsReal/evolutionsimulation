import random
import math
e = math.e

log = []
for i in range(5000):
    #val = 0.000015*(e**(-1*(i)+4.8)+20*i-4)
    #print val
    alive = True
    a = 0.0
    while alive:
        x = random.uniform(0, 1)
        val = 0.00000001*(e**(-1.0*(a)+4.8)+20.0*a-4.0)
        #print x, val, a
        if x < val: 
            alive = False
            log.append(a)
        a += 1

av = 0.0
for i in range(len(log)):
    av += log[i]
print (av/len(log))/365
