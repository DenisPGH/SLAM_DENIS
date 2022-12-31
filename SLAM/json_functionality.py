import json
### JUST FOR TEST

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

