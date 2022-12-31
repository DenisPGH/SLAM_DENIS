import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from SLAM.helfer_functionality import Helfer
import matplotlib; matplotlib.use("TkAgg")

hf=Helfer()

data = np.array([
    [0, 0],
    [0, 10],
    [10, 0],
    [10,10],
    [10,-10],
    [-10,-10],
    [-10,10],
    [-10,0],
    [0,-10],

])
plt.scatter(0,0,color='green')

def animate(i):
    """ this function represent the logic of the animation, it repeat every time, by ani
    and gives new values, which are visualisate every new frame on the screen
    there is a way with figure, where YOU can add particulary/wishes dimensions of the picture like a radar"""
    lidar_dict = {}
    lidar_list = []
    plt.clf()
    distance=random.randint(1, 5)
    for a in range(1, 361):
        """ here generate a imitation of the data from lidar, angle and distance, a is angle"""
        lidar_dict[a] = distance
    for k, v in lidar_dict.items():
        """ here I make a list with list_x_y-packet[x,y] from dict values , which contain all
         point to visualisation on the current frame===== this is not realy neccery"""
        current_list = []
        b, c = hf.coordinates_from_x_y_distance_and_angle(0,0,k, v)
        current_list.append(b)
        current_list.append(c)
        lidar_list.append(current_list)

    data_2 = np.array(lidar_list)
    x, y = data_2.T

    plt.scatter(x, y, color='green',s=0.5)
    plt.scatter(0, 0, color='red')





ani = FuncAnimation(plt.gcf(), animate, interval=50)
plt.show()

