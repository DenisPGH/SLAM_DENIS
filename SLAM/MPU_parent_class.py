

class MPU__PARENT:
    def __init__(self):
        self.sum_angular_velocity=0
        self.mpu_yaw_divider_factor_right=0
        self.mpu_yaw_divider_factor_left=0
        self.ERROR_FACTOR_TURNING_RIGHTS=1
    def yaw_angle__in__degrees(self,dir_turning:str, current_angular_velocity = 0):
        """
        :param dir_turning=
        :param current_angular_velocity: get dinamicali from the child class
        dir_turning= R or L
        it calculate the angle of rotation in degrees and store it to
        mpu_current_yaw_angle and also return the calculated
        :return: real angle in degrees
        """
        #current_angular_velocity = self.current_angular_velocity_yaw_angle()

        # self.sum_angular_velocity += abs(current_angular_velocity) # old version
        # self.real_yaw_angle_degrees = self.sum_angular_velocity // self.mpu_yaw_divider_factor # old version
        if dir_turning == 'R':
            self.sum_angular_velocity += abs(current_angular_velocity)
            self.real_yaw_angle_degrees = self.sum_angular_velocity // self.mpu_yaw_divider_factor_right
            return self.real_yaw_angle_degrees
        elif dir_turning == 'L':
            self.sum_angular_velocity -= abs(current_angular_velocity)
            self.real_yaw_angle_degrees = self.sum_angular_velocity // self.mpu_yaw_divider_factor_left
            return (float(self.real_yaw_angle_degrees) * self.ERROR_FACTOR_TURNING_RIGHTS)  # 0.94