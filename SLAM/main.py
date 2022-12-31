import json
import time
from LOGIC import SlamMainLogic, StoreJson
from helfer_functionality import Helfer
from lidar_functionality import DeniLidar
from mapping_DB_functionality import MapInDataBase
from MEGA_functionality import BODY
from visualisation_functionality import Visualisation
from mpu_functionality import MPU

db=MapInDataBase()
logic=SlamMainLogic()
lid=DeniLidar()
body=BODY()
sj=StoreJson()
visual=Visualisation()
helper=Helfer()

## 1 creare db with empty graph-only one time
# db.drop_table('node')
# db.drop_table('edges')
# db.create_db_table_graph_node()
# db.create_db_table_edges()
#db.create_coordinates_table_in_db()

## 2 create new test graph
db.clear_graph_in_DB()
x,y,coord,dist,dir='x','y','coord','dist','dir'
nodes={1:{'x':0,'y':0,'coord':[(0,0)],dist:0,dir:0},
       2:{'x':0,'y':50,'coord':[(0,50)],dist:50,dir:0},
       3:{'x':50,'y':50,'coord':[(50,50)],dist:50,dir:90},
       4:{'x':50,'y':0,'coord':[(50,0)],dist:50,dir:180},
       5:{'x':1,'y':0,'coord':[(1,0)],dist:49,dir:270},
       }


nodes_2={1:{'x':0,'y':0,'coord':[(0,0)],dist:0,dir:0},
       2:{'x':0,'y':100,'coord':[(0,50)],dist:100,dir:0},
       3:{'x':200,'y':100,'coord':[(50,50)],dist:50,dir:90},
       4:{'x':200,'y':200,'coord':[(50,0)],dist:100,dir:180},
       5:{'x':1,'y':0,'coord':[(1,0)],dist:49,dir:270},
       }
db.create_new_unique_into_DB(nodes_2)

## 3 print the created nodes and edges
# print(body.read_from_mega("speed"))
# print(body.read_from_mega("dist"))
# 
# db.print_all_info_from_table_nodes()
# db.print_all_info_from_table_edges()
#db.close()




## 4 test find a path between two nodes
#print(body.status_bateries())
# mpu=MPU()
# while True:
#        #print(mpu.current_angular_velocity_yaw_angle())
#        print(mpu.return_real_yaw_angle_in_degree())
#time.sleep(7)
#logic.move_from_A_to_B(1,5)
#logic.move_from_A_to_B(5,1)
# logic.move_from_A_to_B(1,2)
# logic.move_from_A_to_B(2,1)
#body.move_one_step_command(0,10)
#body.move_one_step_command(0,20)
# body.move_one_step_command(0,0)
# body.move_one_step_command(315,0)
# body.move_one_step_command(0,0)


### 5 run lidar and store the coord into db
for a in range(1,4):
       lid.start_lidar_measuring()
       lid.stop_lidar_measuring()
       current_node=a
       cur_node_x=0
       cur_node_y=0
       cur_coord_list=[]
       coor=sj.return_info_from_json_file()
       db.clear_coord_for_node(current_node)
       for angle,dist in coor:
              ##print(angle,dist)
              x,y=helper.coordinates_from_x_y_distance_and_angle(cur_node_x,cur_node_y,angle,dist)
              cur_coord_list.append((x,y))

       db.add_new_coordinate(current_node, cur_coord_list)
       db.print_all_coord_for_node(current_node)

















