import numpy as np
from matplotlib import pyplot as plt_source
from mapping_DB_functionality import MapInDataBase
import time


class Visualisation:
    def __init__(self):
        self.DB=MapInDataBase()
        self.plt=plt_source
        self.font_size_node_text=20
        self.size_node_point=20
        self.point_size=10
        self.color_node='black'

    def show_points_for_one_node(self, node_name, color='green'):
        """
        visualize of the map where is the node and its detected points
        :param node_name: node id
        :param color: which color to be its points
        :return:
        """
        list_coord=self.DB.return_all_coord_for_a_node(node_name)
        coord_of_node=self.DB.return_own_coord_of_node(node_name)
        self.DB.close()
        data=np.array(list_coord)
        node=np.array(coord_of_node)
        x,y=data.T
        x_n,y_n=node.T
        fig, ax = self.plt.subplots()
        ax.scatter(x, y, color=f'{color}', s=self.point_size)
        ax.scatter(x_n, y_n, color=f'{self.color_node}', s=self.size_node_point)
        ax.annotate(node_name, (x_n, y_n),fontsize=self.font_size_node_text)
        fig.show()
        time.sleep(20)
        return

    def show_all_points_in_db(self):
        """
        in plot
        show all nodes location
        show path between the node
        show all detected points for coresponding to each node
        """

        all_x=[]
        all_y=[]
        all_nodes_names=self.DB.all_nodes_names()
        #colors={1:'red',2:'green',3:'blue',4:'yellow',5:'black',6:'red'}
        colors={1:'green',2:'green',3:'green',4:'green',5:'green',6:'green'}
        fig, ax = self.plt.subplots()
        for node_name in all_nodes_names:
            list_coord = self.DB.return_all_coord_for_a_node(node_name)
            coord_of_node = self.DB.return_own_coord_of_node(node_name)
            all_x.append(coord_of_node[0][0])
            all_y.append(coord_of_node[0][1])
            data = np.array(list_coord)
            node = np.array(coord_of_node)
            x, y = data.T
            x_n, y_n = node.T
            try:
                col=colors[node_name]
            except:
                col='green'

            ax.scatter(x, y, color=f'{col}', s=self.point_size)
            ax.scatter(x_n, y_n, color=f'{self.color_node}', s=self.size_node_point)
            ax.annotate(node_name, (x_n, y_n), fontsize=self.font_size_node_text)

        self.plt.plot(all_x,all_y,'k')
        self.DB.close()
        self.plt.axis('equal')
        fig.show()
        time.sleep(20)



