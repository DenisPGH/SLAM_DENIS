# for n,info in nodes.items():
#     if nodes[n] not in m.all_nodes_names():
#         m.add_node_into_graph_node_table(n, info[x], info[y])
#         m.add_new_coordinate(n,info[coord])
#     if n !=1:
#         m.add_edge(f'{n}-{n-1}', n, f'{n}', f"{n-1}", info[dist], info[dir])
#         m.add_edge(f'{n-1}-{n}', n-1, f'{n-1}', f"{n}", info[dist], info[dir]+180)
#
#
#
# m.con.close()

#m.create_db_table_graph_node()
#m.create_coordinates_table_in_db()
#m.add_node_into_graph_node_table(0,10)
#m.create_db_table_edges('edges')
#m.drop_table('edges')
#m.add_edge('2-1',1,'1','2',10,270)
#print(m.return_kinder_edges_for_node(2))


# con = sqlite3.connect('map.db')
# cur = con.cursor()
# #cur.execute(''' DROP TABLE edges''')
# #cur.execute('''CREATE TABLE edges
#              #  (id integer primary key, source_node text, destination_node text, distance real, direction_angle integer)''')
# dist=30
# #cur.execute("INSERT INTO edges VALUES ('a','b',100,35)")
# cur.execute('''INSERT INTO edges (id,source_node,destination_node,distance,direction_angle)
#                 VALUES (?, ?, ?, ?, ?);''',(20,'a','b',dist,0))
#
# con.commit()
# con.close()


# m.create_new_unique_into_DB(nodes)
# #print(m.return_all_coord_for_a_node(1))
# m.con.close()
import math

matrix_2=[["*******************************************"],
          ["*-----------------------------------------*"],
          ["*----------------------**-----------------*"],
          ["*----------------------**-----------------*"],
          ["*----------------------**-----------------*"],
          ["*************************-----*************"],
          ["**----------------------------------------*"],
          ["**-----------------------------**---------*"],
          ["**-----------------------------**---------*"],
          ["************************************----***"],
          ["**------------**--------------------------*"],
          ["**------------**--------------------------*"],
          ["**----------------------------------------*"],
          ["*******************************************"],


        ]
matrix=[list(x[0]) for x in matrix_2]


def coordinates_from_distance_and_angle(distance: float, angle: int):
    """ this function returns the coordinates(x,y) of the given point by its distance to the center of lidar
    and angle between 0-360
    angle in degrees"""
    if 0 <= angle < 45:
        y = distance * math.cos(math.radians(angle))
        x = distance * math.sin(math.radians(angle))
        return (x, y)
    elif 45 <= angle < 90:
        y = distance * math.sin(math.radians(angle - 45))
        x = distance * math.cos(math.radians(angle - 45))
        return (x, y)
    elif 90 <= angle < 135:
        y = (distance * math.sin(math.radians(angle - 90)))
        x = (distance * math.cos(math.radians(angle - 90)))
        return (x, -y)
    elif 135 <= angle < 180:
        y = (distance * math.cos(math.radians(abs(angle - 180))))
        x = (distance * math.sin(math.radians(abs(angle - 180))))
        return (x, -y)
    elif 180 <= angle < 225:
        y = (distance * math.cos(math.radians(abs(angle - 180))))
        x = (distance * math.sin(math.radians(abs(angle - 180))))
        return (-x, -y)
    elif 225 <= angle < 270:
        y = (distance * math.sin(math.radians(abs(angle - 270))))
        x = (distance * math.cos(math.radians(abs(angle - 270))))
        return (-x, -y)
    elif 270 <= angle < 315:
        y = (distance * math.sin(math.radians(abs(angle - 315))))
        x = (distance * math.cos(math.radians(abs(angle - 315))))
        return (-x, y)
    elif 315 <= angle <= 360:
        y = (distance * math.cos(math.radians(abs(angle - 360))))
        x = (distance * math.sin(math.radians(abs(angle - 360))))
        return (-x, y)


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#from LOGIC import SlamMainLogic




#sl=SlamMainLogic()

### 1. have to build graph first
#### or run test file to store test graph into db

#sl.move_from_A_to_B(1,4)



######## TESTING HERE ###########
import time
from ARDUINO_MEGA import BODY
from speaking_function import Voice
# from SLAM.mapping import MapInDataBase
# from SLAM.graph_functionality import ShortestPath

# sp=ShortestPath()
# db=MapInDataBase()
# db.clear_graph_in_DB()
# a='a'
# world_matrix=[[a,a,a,a,a,a,a],
#               [a,0,0,0,0,0,a],
#               [a,0,0,0,0,0,a],
#               [a,0,0,0,0,0,a],
#               [a,0,0,0,0,0,a],
#               [a,0,0,0,0,0,a],
#               [a,a,a,a,a,a,a],


#               ]
# world_matrix=[[a,a,a,a,a,a,a,a,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,0,0,0,0,0,0,0,a],
#               [a,a,a,a,a,a,a,a,a],
#               ]


# dist=2
# numbered_world_matrix=sp.number_nodes_in_matrix(world_matrix,0)
# sp.print_matrix(numbered_world_matrix)
# sp.create_graph_from_LIDAR_coordinates_already_stored_into_world_matrix(numbered_world_matrix,dist,a)

b=BODY()
# while True:
#     #print(b.read_from_mega("speed"))
#     print(b.read_from_mega("dist"))


#print(b.read_from_mega('dist'))
time.sleep(2)
b.move_one_step_command(0,50)
b.move_one_step_command(90,50)
b.move_one_step_command(180,50)
b.move_one_step_command(270,50)
# b.move_one_step_command(0,0)

#####
def orientation_of_car(self):
    """
    read the info via UART from adruino nano- send string with z angle

    :return: current orientation of the car in degree 0-360
    """

    data = 0
    if self.serial_port.inWaiting() > 0:  # chete ot MEGA
        data = self.serial_port.read()
    return data  # format the string well!!!


def theta_angle_calculator_rotation(self,dist_l,dist_r):
        """
        calculating the rotation angle of the car in a point, not moving

        :param dist_l: dist of left wheel
        :param dist_r: dist of right wheel
        :return: the angle of rotation of the car
        """
        return self.rotation_angle


def turn_car_right_direction_encoder(self, direction):
        """
        TEST FUNCTION-NOT in use for now -31.07.2022
        :param direction: desired direction
        :return: True if car is oriented to this directon and False if not.
        """

        if self.ACTUAL_CAR_ORIENTATION==direction:
            return True
        else:
            dir_rotation,degrees=self.rotator_calculator.commands_for_rotation_from_direction_to_target_dir(self.ACTUAL_CAR_ORIENTATION, direction)
            while True:

                enc_A, enc_B = self.read_from_mega('dist') # len 2
                if enc_A+enc_B==0:
                    return True
                if dir_rotation=='L':
                    self.write_to_mega('00,255,255,255,255,3,1')
                elif dir_rotation=='R':
                    self.write_to_mega('00,255,255,255,255,2,1')


        return False


def fahrt_from_A_to_B_point(self,commands):
        """
        not in use
        command cames from path calculator in form dict
        :param commands: {1: {'dir': 180, 'dist': 10.0}, 2: ['END']}
        :return: nothing, DIRECT commands to the motors
        """
        if not isinstance(commands,dict):
            return 'ERROR=== NO SUCH WAY!!!!'
        for step, info in commands.items():
            if isinstance(info,dict):
                self.move_one_step_command(info['dir'],info['dist'])
            else:
                print("DONE")



def combine_final_function(self, graph, matrix, start:str, target:str):
        """
        NOT USE THIS !!!!!! this is for testing
        this function create new graph, find, path and return a dict
        with steps, directions and distance to the goal.

        :param graph: graph
        :param matrix:
        :param start: node name from where
        :param target: node name to where
        :return: dict {step_number: {'dir': 'up', 'dist': 10cm}}
        """
        # return dict with steps,directions,distances
        numbered_fields_matrix = self.number_nodes_in_matrix(matrix)
        graph = self.create_graph_from_matrix(numbered_fields_matrix)
        #graph=graph
        start_node = int(start)  # 3
        target_node = int(target)  # 364
        distances, parents = self.find_shortest_way_between_two_nodes(start_node, target_node, graph)
        path, dict_path = list(self.generate_path_from_source_to_target(target_node, parents))
        final_matrix_with_marked_road = self.mark_path_on_the_map(dict_path, numbered_fields_matrix)
        #self.print_matrix(final_matrix_with_marked_road)
        commands = self.commands_to_the_target(list(path), graph)
        return commands


def coordinates_from_distance_and_angle(self, distance: float, angle: int):
    """
    OLD ONE, NOT SO TRUE!!!!

    this function returns the coordinates(x,y) of the given point by
    its distance to the center of map 0,0
    and angle between 0-360
    angle in degrees
    return the new coordinates tuple (x,y)"""
    if 0 <= angle < 45:
        y = distance * math.cos(math.radians(angle))
        x = distance * math.sin(math.radians(angle))
        return (x, y)
    elif 45 <= angle < 90:
        y = distance * math.sin(math.radians(angle - 45))
        x = distance * math.cos(math.radians(angle - 45))
        return (x, y)
    elif 90 <= angle < 135:
        y = (distance * math.sin(math.radians(angle - 90)))
        x = (distance * math.cos(math.radians(angle - 90)))
        return (x, -y)
    elif 135 <= angle < 180:
        y = (distance * math.cos(math.radians(abs(angle - 180))))
        x = (distance * math.sin(math.radians(abs(angle - 180))))
        return (x, -y)
    elif 180 <= angle < 225:
        y = (distance * math.cos(math.radians(abs(angle - 180))))
        x = (distance * math.sin(math.radians(abs(angle - 180))))
        return (-x, -y)
    elif 225 <= angle < 270:
        y = (distance * math.sin(math.radians(abs(angle - 270))))
        x = (distance * math.cos(math.radians(abs(angle - 270))))
        return (-x, -y)
    elif 270 <= angle < 315:
        # dava greshka tuk ne veren gradus
        y = (distance * math.sin(math.radians(abs(angle - 270))))
        x = (distance * math.cos(math.radians(abs(angle - 270))))
        return (-x, y)
    elif 315 <= angle <= 360:
        y = (distance * math.cos(math.radians(abs(angle - 360))))
        x = (distance * math.sin(math.radians(abs(angle - 360))))
        return (-x, y)
    return (0, 0)  # if error


# import paramiko
# from paramiko import SSHClient
#
# # ssh = SSHClient()
# # ssh.load_system_host_keys()
# # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # ssh.connect(host=hostname, username='username', password='password')
# ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sqlite3 /path/to/yourdb.sqlite3 "select * from table;"')
# stdout=ssh_stdout.readlines()
# print(stdout)
#


import numpy as np
# import os
# #source_folder="/usr/nanorobo/Desktop/Robo"
#
# monitoring_database='C:\\Users\\Owner\\Desktop\\projects\\Robo\\Robo\\SLAM\\Monitoring\\map_monitoring.db'
#
# s = paramiko.SSHClient()
# s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# s.connect("192.168.1.115",22,username='nanorobo',password='D_12-K9',timeout=4)
#
# sftp = s.open_sftp()
# #robo_db=sftp.listdir(source_folder)
# robo_db=sftp.readlink(robo_database)
