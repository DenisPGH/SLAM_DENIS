import numpy as np
from matplotlib import pyplot as plt

def f(x):
    return (x**2)+2*x**2 +20*x**3
new_places=[]
r=100
for a in range(-r,r+1):
    new_places.append([a,f(a)])
dimensions_world_frame=60
world_frame = np.array([
    [0, 0],
    [0, dimensions_world_frame],
    [dimensions_world_frame, 0],
    [dimensions_world_frame,dimensions_world_frame],
    [dimensions_world_frame,-dimensions_world_frame],
    [-dimensions_world_frame,-dimensions_world_frame],
    [-dimensions_world_frame,dimensions_world_frame],
    [-dimensions_world_frame,0],
    [0,-dimensions_world_frame],

])

point_size=30
data=np.array(new_places)
x,y=data.T

x_w,y_w=world_frame.T
fig, ax = plt.subplots()
ax.scatter(x, y, color=f'red', s=point_size)

ax.scatter(0, 0, color='black', s=point_size)
ax.scatter(x_w, y_w, color='black', s=point_size)
plt.grid()
fig.show()
