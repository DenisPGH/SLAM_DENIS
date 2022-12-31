from rplidar import RPLidar
import numpy as np
import json
from json_functionality import StoreJson



"""{'model': 24, 
'firmware': (1, 29), 
'hardware': 7, 
'serialnumber': 'E280ED93C0EA98C9A5E698F2775E4669'}
('Good', 0)
"""

class DeniLidar:
    def __init__(self):
        self.lidar = RPLidar('/dev/ttyUSB0')
        self.list_lidar = []
        self.distance = 0
        self.angle = 0
        self.dict_dist={}
        self.sj=StoreJson()

    def start_lidar_measuring(self):
        self.lidar.connect()
        """
        the function measure the lidar result(angle-deg,distance), and store into self.list_lidar
        :return:
        """
        counter = 0
        from_lidar = self.lidar.iter_scans()
        counter_cycle=0
        for scan in from_lidar:
            counter_cycle+=1
            #print(f'start, counter=={counter}')
            counter += 1
            self.list_lidar = []
            offsets = np.array([(meas[1], meas[2]) for meas in scan])
            for degree, dist in offsets:
                self.list_lidar.append((degree, dist // 10))
            #print(self.list_lidar)
            if counter_cycle >=2:
                self.stop_lidar_measuring
                self.sj.strore_this_into_json_file(self.list_lidar)
                break


    def stop_lidar_measuring(self):
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()



