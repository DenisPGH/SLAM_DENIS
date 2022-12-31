"""
#TODO:
1. class with def for takes arguments and return the output to the motors in correct form
2. test after the error
"""
from simple_pid import PID

class PIDTurning:
    """
    class for correction the angle by turning with minimum errors
    """
    def __init__(self):
        self.Kp_L_lr = 1.8 #2.8 =10.3V, 1.8=11.3V,90gr
        self.Ki_L_lr = 0 #
        self.Kd_L_lr = 0  #0.01

        self.Kp_R_lr = 1.8 #2.8
        self.Ki_R_lr = 0  #
        self.Kd_R_lr = 0  #0.01
        self.PID=PID

        self.mode_for_mega=1

    def output(self, set_point, current_value, dir_rotation):
        """
        :param set_point: target value, which I want to achiev
        :param current_value: current value of the sensor
        :param dir_rotation: which direction have to turn to achieve the target
        :return: string in type '00,0,0,0,0,4,1' for direct command in Arduino Mega
        """
        pid_L_lr = self.PID(self.Kp_L_lr, self.Ki_L_lr, self.Kd_L_lr, setpoint=set_point)
        pid_L_lr.output_limits = (-255, 255)
        pid_R_lr = self.PID(self.Kp_R_lr, self.Ki_R_lr, self.Kd_R_lr, setpoint=set_point)
        pid_R_lr.output_limits = (-255, 255)
        output_pid_mega_L_lr = pid_L_lr(current_value)
        output_pid_mega_R_lr = pid_R_lr(current_value)
        string_mega = f"00,0,0,{abs(int(output_pid_mega_L_lr))},{abs(int(output_pid_mega_R_lr))},{dir_rotation},{self.mode_for_mega}"
        return string_mega



class PIDStreight:
    """
        class for correction the line ahead with minimum errors
        """
    def __init__(self):
        self.Kp_L = 9 # 10.62
        self.Ki_L = 0  # 0
        self.Kd_L = 0 # 0

        self.Kp_R = 9 # 9.2
        self.Ki_R = 0   # 0
        self.Kd_R = 0 # 0
        self.PID=PID
        self.mode_for_mega=1

    def output_ahead_back(self,set_point,current_value, direction:int):
        """
        :param set_point: target value, which I want to achiev
        :param current_value: current value of the sensor
        :param direction: which direction have to go ahead or back
        :return: string in type '00,0,0,0,0,4,1' for direct command in Arduino Mega
        """
        pid_L = self.PID(self.Kp_L, self.Ki_L, self.Kd_L, setpoint=set_point)
        pid_L.output_limits = (-255, 255)
        pid_R = self.PID(self.Kp_R, self.Ki_R, self.Kd_R, setpoint=set_point)
        pid_R.output_limits = (-255, 255)
        output_pid_mega_L = pid_L(current_value)
        output_pid_mega_R = pid_R(current_value)
        string_mega = f"00,0,0,{abs(int(output_pid_mega_L))},{abs(int(output_pid_mega_R))},{direction},{self.mode_for_mega}"
        return string_mega

    def output_ahead_back_2(self,speed_L,speed_R, direction:int):
        """
        :param speed L: actual speed in RPM from left motor
        :param speed R: actual speed in RPM from right motor
        :param direction: which direction have to go ahead or back
        :return: string in type '00,0,0,0,0,4,1' for direct command in Arduino Mega
        """
        pid_L = self.PID(self.Kp_L, self.Ki_L, self.Kd_L, setpoint=20) # target 15 RPM
        pid_L.output_limits = (-255, 255)
        pid_R = self.PID(self.Kp_R, self.Ki_R, self.Kd_R, setpoint=20)
        pid_R.output_limits = (-255, 255)
        output_pid_mega_L = pid_L(speed_L)
        output_pid_mega_R = pid_R(speed_R)
        string_mega = f"00,0,0,{abs(int(output_pid_mega_L))},{abs(int(output_pid_mega_R))},{direction},{self.mode_for_mega}"
        return string_mega