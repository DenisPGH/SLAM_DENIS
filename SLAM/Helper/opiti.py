import math

class Test:
    def __init__(self):
        self.width_car=25 # cm
        self.rotation_angle=0



    def theta_angle_calculator_rotation(self, dist_l, dist_r):
        rotation_angle_l=math.degrees(math.atan(dist_l/12.5))
        rotation_angle_r=math.degrees(math.atan(dist_r/12.5))
        print(rotation_angle_r,'r',rotation_angle_l)
        self.rotation_angle=(rotation_angle_r+rotation_angle_l)/2

        return self.rotation_angle

a=Test()

s=a.theta_angle_calculator_rotation(6,6)
print(s)



class MPU:
    def actuall_z_angle(self):
        pass