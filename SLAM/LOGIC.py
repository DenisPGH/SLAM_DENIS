from MEGA_functionality import BODY
#from EKF_classes_functionality import UKFDeni, EKFDeniTheta
from helfer_functionality import Helfer
from lidar_functionality import DeniLidar
from mapping_DB_functionality import MapInDataBase
from speak_functionality import Voice
from visualisation_functionality import Visualisation
from graph_functionality import DeniGraphMatrixWorld
import json
import numpy as np
"""
TODO :
- update x,y,orientation also in the logic here
"""

class Places:
    PLACES={'girl':1 , 'boy':2, 'wild':3, 'box':4} # name:node
        



class SlamMainLogic:
    def __init__(self):
        self.shortest_path=DeniGraphMatrixWorld()
        self.body=BODY()
        self.lidar='lidar class have to be here'
        self.actual_orientation=0
        self.actual_x_position=0
        self.actual_y_position=0
        ###############################
        self.db = MapInDataBase()
        #self.logic = SlamMainLogic()
        self.lid = DeniLidar()
        self.body = BODY()
        self.sj = StoreJson()
        self.visual = Visualisation()
        self.helper = Helfer()
        self.stimme = Voice()
        #self.ukf_deni=UKFDeni()
        #self.ekf_theta=EKFDeniTheta()
        self.np=np
        ######
        self.prev_node_x=0
        self.prev_node_y = 0


    def move_from__node_A__to__node_B(self, start, end):
        """
        the function find the path from node A to node B and give orders to the robot car to move there
        :param matrix: field of the room
        :param start: node from
        :param end:  node to
        :return: notingh
        """
        path=self.shortest_path.final_function(start,end)
        print(path)
        if not isinstance(path,dict):
            return 'ERROR=== NO SUCH WAY!!!!'
        for step,info in path.items():
            
            if isinstance(info, dict):
                print(f"Step: {step}")
                self.body.move_one_step_command(info['dir'], info['dist'])
            else:
                print('DONE!')

    def move_to_node(self, end:int):
        """
        the function find the path from curent location(node) to node B and give orders to the robot car to move there
        :param end:  node to
        :return: notingh
        """
        start=self.db.return_current_location_of_the_robot()[0] # return the node name
        start=int(start)
        path = self.shortest_path.final_function(start, end)
        print(path)
        last_dir=0
        if not isinstance(path, dict):
            return 'ERROR=== NO SUCH WAY!!!!'
        for step, info in path.items():
            if isinstance(info, dict):
                print(f"Step: {step}")
                self.body.move_one_step_command(info['dir'], info['dist'])
                last_dir=info['dir']
            else:
                # update only the node, ITS OK?????
                self.body.move_one_step_command(last_dir, 0,end)
                print('DONE!')
        # update info current location
        self.db.update_position_in__DB(end,self.body.ACTUAL_CAR_ORIENTATION,self.body.actual_x_postion,self.body.actual_y_postion)
        print(self.db.return_current_location_of_the_robot())


    def build_path(self,test_path):
        """
        build the path by given commands and store it into DB
        :param test_path: dict [[direction(0-360),distance(in cm)],]
        :return:
        """
        # print the batery status
        print(self.body.status_bateries())
        # variables
        all_scans_dict = {}
        x, y, coord, dist, dir = 'x', 'y', 'coord', 'dist', 'dir'
        ### 1 clear the map
        self.db.clear_graph_in_DB()
        ### 2 run the building the path and store into DB
        counter = 0
        for dir_walking, distance_ in test_path:
            counter += 1
            print(f"Step===={counter}")
            self.stimme.speak_this(f"Стъпка {counter}!!")
            current_dict_unit = {}
            self.body.move_one_step_command(dir_walking, distance_)
            # create coordinates for this node
            try:
                self.lid.start_lidar_measuring()
            except:
                print('error by scaning')
                self.lid.start_lidar_measuring()

            self.lid.stop_lidar_measuring()
            coor_from_json_file = self.sj.return_info_from_json_file()
            #### ukf for calculating the position of the robot
            #cur_node_x, cur_node_y,cur_node_theta = self.ukf_deni.localization_correction(dir_walking,distance_,coor_from_json_file)
            #### ekf calculating the theta errors
            # theta_from_encoders=self.body.orientation_of_the_car()
            # cur_node_theta=self.ekf_theta.calculate_error_turning(self.np.array([[theta_from_encoders]]))
            ### update the new position into DB
            #print(f"bevore ={theta_from_encoders}, after ekf {cur_node_theta}")

            #### old way with math ###################
            cur_node_x, cur_node_y = self.helper.coordinates_new_pos_car(self.prev_node_x, self.prev_node_y, dir_walking, distance_)
            cur_node_theta=dir_walking
            #### old way with math ###################

            self.db.update_position_in__DB(counter,cur_node_theta,cur_node_x,cur_node_y)
            #### start others
            cur_coord_list = []
            all_scans_dict[counter] = coor_from_json_file
            #self.db.clear_coord_for_node(counter)
            # calculating the coordinates of the landmarks by the coordiantes and orienatation of the robot
            for angle_point, distance_point in coor_from_json_file:
                x_point, y_point = self.helper.coordinates_from_x_y_distance_and_angle(cur_node_theta, cur_node_x, cur_node_y,
                                                                                  angle_point, distance_point)
                cur_coord_list.append((x_point, y_point))
            current_dict_unit[counter] = {x: cur_node_x,
                                     y: cur_node_y,
                                     coord: cur_coord_list,
                                     dist: distance_,
                                     dir: dir_walking
                                     }
            self.db.create_new_unique_into_DB(current_dict_unit)
            #self.stimme.speak_this(f"Край na mapping!!")
            self.db.create_new_unique_into_DB(current_dict_unit)
            self.prev_node_x, self.prev_node_y = cur_node_x, cur_node_y # update position
        self.stimme.speak_this(f"Край na mapping!!")
        ### 6 store the dist,angle in a json file
        self.sj.strore_this_into_json_file_where(all_scans_dict, '/home/nanorobo/Desktop/Robo/Robo/SLAM/lidar_test_UKF_2.json')
        ### print the new graph builded
        #self.db.print_all_info_from_table_nodes()


    def where_are_you(self):
        place=''
        current_node_DB=self.db.return_current_location_of_the_robot()[0]
        for pl,num in Places.PLACES.items():
            if num==int(current_node_DB):
                place=pl
                break

        to_say=f'I am on {place}'
        self.stimme.speak_this(to_say)
        return






#############################################################################################
###########################################    JSON        ##################################
#############################################################################################

class StoreJson:
    def __init__(self):
        self.fil='/home/nanorobo/Desktop/Robo/Robo/SLAM/lidar.json'

    def strore_this_into_json_file(self,this):
        with open(self.fil,'w') as file_lidar:
            file_lidar.write(json.dumps(this))

    def return_info_from_json_file(self):
        """ return: the last scans in form [(angle,dist),]"""
        res=''
        with open(self.fil,'r') as file_lidar:
            res=json.load(file_lidar)
        return res

    def clear_json(self):
        with open(self.fil,'w') as file_lidar:
            file_lidar.write(json.dumps([]))

    def strore_this_into_json_file_where(self,this,where):
        with open(where,'w') as file_lidar:
            file_lidar.write(json.dumps(this))

