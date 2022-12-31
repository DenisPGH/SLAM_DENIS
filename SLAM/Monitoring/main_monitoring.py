import json

from SLAM.Monitoring.db_monitoring import DBInfoROBO
from SLAM.Monitoring.visualisation_monitoring import VisualisationMonitoring
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from SLAM.helfer_functionality import Helfer
import random
from SLAM.helfer_functionality import Helfer
import matplotlib; matplotlib.use("TkAgg")
visual=VisualisationMonitoring()
hf=Helfer()
DB=DBInfoROBO()

dimensions_world_frame=340
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
plt.scatter(0,0,color='green')

point_size=0.6
color_node='black'
size_node_point=1
font_size_node_text=5
fig, ax = plt.subplots()


def real_mapping(i):
    data_w=np.array(world_frame)
    x_world,y_world=data_w.T
    all_x = []
    all_y = []
    all_nodes_names = DB.all_nodes_names_r()
    points_dict = {}

    colors = {1: 'green', 2: 'green', 3: 'green', 4: 'green', 5: 'green', 6: 'green'}
    for node_name in all_nodes_names:
        points_dict[node_name]={}
        points_dict[node_name]['node_points'] = []
        points_dict[node_name]['coord_of_node'] = []
        list_coord = DB.return_all_coord_for_a_node_r(node_name)
        coord_of_node = DB.return_own_coord_of_node_r(node_name)
        points_dict[node_name]['node_points']=list_coord
        points_dict[node_name]['coord_of_node']=coord_of_node
        with open('points_robo_2.txt', 'w') as file:
            file.write(str(points_dict))


        try:
            all_x.append(coord_of_node[0][0])
            all_y.append(coord_of_node[0][1])
        except:
            all_x.append(0)
            all_y.append(0)
        data = np.array(list_coord)
        node = np.array(coord_of_node)
        try:
            x, y = data.T
        except:
            x,y=0,0
        try:
            x_n, y_n = node.T
        except:
            x_n, y_n = 0,0
        try:
            col = colors[node_name]
        except:
            col = 'green'
        ax.scatter(x, y, color=f'{col}', s=point_size)
        ax.scatter(x_n, y_n, color=f'{color_node}', s=size_node_point)
        ax.scatter(x_world, y_world, color='red', s=10)
        ax.annotate(node_name, (x_n, y_n), fontsize=font_size_node_text)



    plt.plot(all_x, all_y, 'k')
    plt.axis('equal')
    fig.show()




ani = FuncAnimation(plt.gcf(), real_mapping, interval=50)
fig.show()


