import json
import time
from LOGIC import SlamMainLogic, StoreJson
from helfer_functionality import Helfer
from lidar_functionality import DeniLidar
from mapping_DB_functionality import MapInDataBase
from MEGA_functionality import BODY
from visualisation_functionality import Visualisation
from mpu_functionality import MPU
from speak_functionality import Voice

db=MapInDataBase()
logic=SlamMainLogic()
lid=DeniLidar()
body=BODY()
sj=StoreJson()
visual=Visualisation()
helper=Helfer()
stimme=Voice()
### 0 batery status
all_scans_dict={}
print(body.status_bateries())
## 1 create test path
x,y,coord,dist,dir='x','y','coord','dist','dir'
test_path=[(0,0),(0,50),(0,50),(90,50),(180,50),
            (180,50),(270,50),(45,50),(225,60),(90,10),
            (180,20),(180,50),(180,50),(180,50)
            ] # (dir,dist)



### 1 clear the map
db.clear_graph_in_DB()
print(db.all_nodes_names())
### 2 map the room
time.sleep(3)
counter=0
prev_node_x,prev_node_y=0,0
for dir_walking,distance_ in test_path[:8]:

    counter+=1
    print(f"Step===={counter}")
    stimme.speak_this(f"Стъпка {counter}!!")
    current_dict={}
    body.move_one_step_command(dir_walking,distance_)   
    #create coordinates for this node
    try:
        lid.start_lidar_measuring()
    except:
        print('error by scaning')
        lid.start_lidar_measuring()

    lid.stop_lidar_measuring()
    current_node=counter
    #### here kalman filter for node coord update###################
    cur_node_x,cur_node_y=helper.coordinates_new_pos_car(prev_node_x,prev_node_y,dir_walking,distance_)
    cur_coord_list=[]
    coor_from_json_file=sj.return_info_from_json_file()
    all_scans_dict[counter] = coor_from_json_file
    db.clear_coord_for_node(counter)
    for angle_point,distance_point in coor_from_json_file:
        ### here Kalman filter for update for point/landmark####################
        x_point,y_point=helper.coordinates_from_x_y_distance_and_angle(dir_walking,cur_node_x,cur_node_y,angle_point,distance_point)
        cur_coord_list.append((x_point,y_point))
    # 2:{'x':0,'y':100,'coord':[(0,50)],dist:100,dir:0},
    current_dict[counter]={x:cur_node_x,
                           y:cur_node_y,
                           coord:cur_coord_list,
                           dist:distance_,
                           dir: dir_walking
                           }
    db.create_new_unique_into_DB(current_dict)
    prev_node_x,prev_node_y=cur_node_x,cur_node_y
    #lid.stop_lidar_measuring()

stimme.speak_this(f"Край na mapping!!")
## 3 visual all
#visual.show_all_points_in_db()

### 6 store the dist,angle in a json file


sj.strore_this_into_json_file_where(all_scans_dict,'/home/nanorobo/Desktop/Robo/Robo/SLAM/lidar_test_UKF_2.json')





















