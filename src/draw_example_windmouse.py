import matplotlib.pyplot as plt
import numpy as np
from windmouse import wind_mouse

fig = plt.figure(figsize=[13,13])
plt.axis('off')
for y in np.linspace(-200,200,25):
    points = []
    wind_mouse(0,y,500,y,move_mouse=lambda x,y: points.append([x,y]),G_0=9, W_0=3, M_0=15, D_0=10)
    points = np.asarray(points)
    plt.plot(*points.T)
plt.xlim(-50,550)
plt.ylim(-250,250)
plt.show()