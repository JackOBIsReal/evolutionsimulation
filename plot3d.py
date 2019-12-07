from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

x, y, z = axes3d.get_test_data(0.05)
#print x
#print
print y
#print
#print z
ax.plot_wireframe(x, y, z, rstride = 1, cstride = 1)

plt.show()
