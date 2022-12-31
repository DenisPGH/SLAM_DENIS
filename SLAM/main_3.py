#from LOGIC import SlamMainLogic
from MEGA_functionality import BODY
##from speak_functionality import Voice
import time
#from mapping_DB_functionality import MapInDataBase
#from listening_functionality import ListeningComands
# sm=SlamMainLogic()
# lc=ListeningComands()
# map=MapInDataBase()
# stimme=Voice()
bodddy=BODY()



# start position, aways 0,0,0,0

# map.del_table_position()
# map.create_db_table_position()
# map.add_the_first_coordinates()
# map.update_position_in__DB(1,0,0,0)
# a=map.return_current_location_of_the_robot()
# print(f"Location = {a}")
##map.print_all_info_from_table_nodes()

mode=3  # 0= nothing , 1=create map   2= node listening, 3= testing, debug

if mode==1:
    # create marshrut
    test_path=[(0,0),(0,20),(0,30),(0,50)] # [(dir,dist),]
    sm.build_path(test_path)
    bodddy.orientation_of_the_car()
    print(f" BAT = {bodddy.status_bateries()}")
    


elif mode==2:
    stimme.speak_this('Начало!')
    map.print_all_info_from_table_nodes()
    print(type(map.all_nodes_names()[0]))
    try:
        while True:
            # start listening
            target_node=lc.listening()
            #print("target node ", target_node)
            if target_node==100:
                stimme.speak_this('Край!') #break up the loop
                break
            if target_node in map.all_nodes_names():
                sm.move_to_node(target_node)
            else:
                error_=f"{target_node} is not part in our graph map"
                stimme.speak_this(error_)
    except KeyboardInterrupt:
        pass

elif mode==3:
    
   
    #stimme.speak_this('Debug modus')
    # from mpu_functionality import MPU
    # from mpu_second_functionality import MPU_SECOND
    # mpu_1=MPU()
    # mpu_2=MPU_SECOND()
    # res_1=mpu_1.return_real_yaw_angle_in_degree('R')
    # res_2=mpu_2.return_real_yaw_angle_in_degree('R')
    # print(f"mpu 1: {res_1:.2f} , mpu 2 : {res_2:.2f}")
    #time.sleep(6)

    #bodddy.write_to_mega('00,0,0,0,0,9,1')# null theta
    # a=bodddy.orientation_of_the_car()
    # print(a)
    bodddy.move_one_step_command(0,0)
    # bodddy.move_one_step_command(270,20)
    # bodddy.move_one_step_command(180,30)
    # bodddy.move_one_step_command(90,30)
    # bodddy.move_one_step_command(0,0)
  
    
    #bodddy.move_one_step_command(90,0)
    #bodddy.move_one_step_command(0,0)
    #bodddy.move_one_step_command(90,0)
    #time.sleep(1)
    
    #bodddy.move_one_step_command(0,20)
    
    # res_1=mpu_1.return_real_yaw_angle_in_degree('R')
    # res_2=mpu_2.return_real_yaw_angle_in_degree('R')
    # print(f"mpu 1: {res_1:.2f} , mpu 2 : {res_2:.2f}")

    print(f" BAT = {bodddy.status_bateries()}")
    #while True:
    #  bodddy.write_to_mega('00,0,0,50,50,5,1')
    #  time.sleep(2)
    #  bodddy.write_to_mega('00,0,0,50,50,4,1')
    #  time.sleep(2)
    #  a=bodddy.read_from_mega('speed')
    #  b=bodddy.read_from_mega('dist')
    #  print(f"speed= {a}, dist= {b}")


