
from mpu_functionality import MPU
from mpu_second_functionality import MPU_SECOND
mpu_1=MPU()
mpu_2=MPU_SECOND()
#from lidar_functionality import DeniLidar
#dl=DeniLidar()
try:
    min_1=10000
    max_1=-10000
    min_2=10000
    max_2=-10000
    while True:
        
        #res_1=mpu_1.return_real_yaw_angle_in_degree('R')
        #res_2=mpu_2.return_real_yaw_angle_in_degree('R')
        
        res=mpu_1.current_angular_velocity_yaw_angle()
        res_2=mpu_2.current_angular_velocity_yaw_angle()
        if res<min_1:
            min_1=res
        if res_2<min_2:
            min_2=res_2

        if res>max_1:
            max_1=res
        if res_2>max_2:
            max_2=res_2
        print(f"mpu 1: {res:.2f} , mpu 2 : {res_2:.2f}")

    print(f" min 1: {min_1} , max 1: {max_1} ||| min 2: {min_2} , max: {max_2}")
        # dl.start_lidar_measuring()
        # dl.stop_lidar_measuring()
except KeyboardInterrupt:
    print(f" min 1: {min_1} , max 1: {max_1} ||| min 2: {min_2} , max: {max_2}")