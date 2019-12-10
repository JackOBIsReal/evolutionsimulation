from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D

xp = []
yp = []
zp = []

for i in range(60):
    for k in range(60):
        
        xs = i/10.0
        ys = k/10.0
        xp.append(xs)
        yp.append(ys)
for i in range(60):
    for k in range(60):
        zs = math.sin(xp[i*60])*yp[k]
        
        zp.append(zs)#*yp[k])

print len(xp), len(yp), len(zp)
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')


ax.plot_wireframe(xp, yp, zp, rstride = 1, cstride = 1)

plt.show()
