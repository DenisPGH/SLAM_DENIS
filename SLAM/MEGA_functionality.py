
"""
class comunication to mega
"""
import math
from math import  cos,sin
import time
import numpy as np

import smbus
import serial
from PID import PIDTurning, PIDStreight
from EKF_classes_functionality import EKFDeniTheta
#from mpu_second_functionality import MPU_SECOND
from mapping_DB_functionality import MapInDataBase
from helfer_functionality import Helfer
from speak_functionality import Voice
from graph_functionality import DeniGraphMatrixWorld
from mpu_functionality import MPU


class BODY:
    """ EVERYTHING WITH BODY CONTROLING ANG COMUNICATION"""

    def __init__(self):
        self.ARDUINO_NANO_ADRESS_BUS=1
        self.address= 0x60
        self.bus= smbus.SMBus(self.ARDUINO_NANO_ADRESS_BUS)
        self.serial_port = serial.Serial(
                port="/dev/ttyTHS1",
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
        )

        self.ACTUAL_CAR_ORIENTATION=0 # allways start from 0 degree the robot-NORD
        self.rotator_calculator=DeniGraphMatrixWorld()
        self.current_theta_angle=0
        self.radius_wheel=6.8 # 6.8cm
        self.width_of_car=18  # 25 cm
        self.last_time_measurment=0
        self.current_time_measurment=0
        self.actual_x_postion=0
        self.actual_y_postion=0

        self.pid_turning=PIDTurning()
        self.pid_moving=PIDStreight()
        self.speaking=Voice()
        self.dict_values_income_mega={'speed': '', 'dist': ''}
        self.rotation_angle=0
        self.gyroscope=MPU()
        #self.gyroscope_second=MPU_SECOND()
        self.helfer=Helfer()
        self.distance_enc_last_step=0
        self.current_measured_distance=0
        self.SPEED_LEN_MESSAGE = 4
        self.DISTANCE_LEN_MESSAGE = 2

        self.current_degree_measured_mpu=0
        self.reduce_factor=1 # 0.95
        self.factor_range=50

        self.db=MapInDataBase()
        self.ekf_deni_body=EKFDeniTheta()

        self.scale_mpu_1=1
        self.scale_mpu_2=0.8

        self.rpm_to_radians = 0.10471975512


    def StringToBytes(self,val):
        """
        helper function for sending message to MEGA
        """

        retVal = []
        for c in val:
            retVal.append(ord(c))
        return retVal

    def write_to_mega(self,value,LED=0):
        #print(value)
        """
        'value' in  format= '00,LED,0,0,0,4,1' ==>> '00,pwm1,pwm2,pwm3,pwm4,direction,state-always 1'
        """
        # separate in list
        separated_parts=value.split(',')
        # change index 1
        separated_parts[0]=str(LED) # 1= ON, 0=OFF
        # combine into string again
        value= (",").join(separated_parts)


        byteValue = self.StringToBytes(value)
        self.bus.write_i2c_block_data(self.address, 0x00, byteValue)  # first byte is 0=command byte.. just is.
        return -1

    def read_from_mega(self,type_message:str):
        """
        speed=> 'VAT,DEG,RPM,RPM'
        dist=> "CM,CM"
        type_message== "speed" or "dist"('speed' read the speeds, 'dist' read the distances)
        read i2c message from arduino mega and return the message
        :return: list with values
        """
        smsMessage = ""
        data_received_from_Arduino = self.bus.read_i2c_block_data(self.address, 0, 30)
        for i in range(len(data_received_from_Arduino)):
            smsMessage += chr(data_received_from_Arduino[i])
        final_message=smsMessage.split('T')[0]
        #print(final_message)
        
        if len(final_message.split('|'))== self.SPEED_LEN_MESSAGE:
            self.dict_values_income_mega['speed']=final_message
        elif len(final_message.split('|'))== self.DISTANCE_LEN_MESSAGE:
            self.dict_values_income_mega['dist']=final_message
        return self.dict_values_income_mega[type_message].split('|')

    def real_time__theta_angle_calculator(self, vel_l, vel_r):
        """
        this can work only for going ahead
        this function calculate the actual angle of orientation of the car in the world
        :return: current actual theta angle in degrees
        """
        self.current_time_measurment=time.time()
        delta_time=self.current_time_measurment-self.last_time_measurment
        self.current_theta_angle+=(abs(vel_l)+abs(vel_r))/self.width_of_car*delta_time
        if self.current_theta_angle >= 2 * math.pi:
            self.current_theta_angle = 0
        return math.degrees(self.current_theta_angle)


    def status_bateries(self):
        """
        :return: bat1 status as string
        """
        try:
            bat=self.read_from_mega('speed')[0]
            return float(bat)
        except:
            bat=self.read_from_mega('speed')[0]
            return float(bat)

        


    def travaled_distance_updating(self):
        """
        update the traveled distance into self.current_measured_distance
        """
        try:
            enc_L,enc_R=self.read_from_mega('dist')
        except:
            enc_L,enc_R=self.read_from_mega('dist')
        self.current_measured_distance=((abs(float(enc_L)))+abs(float(enc_R)))/2


    def rotate_car_to_wished_orientation_angle(self, target_direction:int):
        """
        with help from MPU and angular velocity , measure the angle of turning
        function to rotate the robot until reach the wished target direction in degree
        PID control the turning, and if it is made well
        return True=> car can go ahead in this direction

        :param target_direction: which dir it shoud go in degrees
        :return: true if car is right oriented
        """
        command_mega=''
        separated_degrees_if_more_than_90=[]
        ### update CAR Orientation after errors
        # theta_from_encoders= int(self.orientation_of_the_car())
        # #theta_after_ekf=self.ekf_deni_body.calculate_error_turning([theta_from_encoders])
        # #theta_after_ekf=int(theta_after_ekf)
        # self.ACTUAL_CAR_ORIENTATION=theta_from_encoders #theta_after_ekf was before
        # self.current_theta_angle= theta_from_encoders # theta_after_ekf was before
        #print('cur theta ang ', self.current_theta_angle)

        while True:
            if self.ACTUAL_CAR_ORIENTATION==target_direction:
                return True
            else:
                dir_rotation, degrees_from_act_to_target_pos = self.rotator_calculator.commands_for_rotation_from_direction_to_target_dir(
                    self.current_theta_angle, target_direction)
                if degrees_from_act_to_target_pos >90:
                    separated_degrees_if_more_than_90.append(90)
                    separated_degrees_if_more_than_90.append(degrees_from_act_to_target_pos-90) 
                else:
                    separated_degrees_if_more_than_90.append(degrees_from_act_to_target_pos)
                
                for angle in separated_degrees_if_more_than_90:
                    #print("NEW_MINI_STEP!!!!!!")
                    self.gyroscope.sum_angular_velocity=0
                    #self.gyroscope_second.sum_angular_velocity=0
                    self.current_degree_measured_mpu=0
                    while True:
                        mpu_a=self.gyroscope.return_real_yaw_angle_in_degree(dir_rotation)* self.scale_mpu_1
                        #mpu_b=self.gyroscope_second.return_real_yaw_angle_in_degree(dir_rotation)* self.scale_mpu_2
                        #self.current_degree_measured_mpu=(abs(mpu_a)+ abs(mpu_b))/2
                        self.current_degree_measured_mpu=abs(mpu_a)
                        #print(self.current_degree_measured_mpu, '===',angle)
                        #self.current_degree_measured_mpu=(abs(mpu_b))
                        #print(f"{mpu_a:.2f} + {mpu_b:.2f} = {self.current_degree_measured_mpu:.2f} ||| {angle}")
                        #if self.current_degree_measured_mpu==angle:
                        # bias=2
                        # if angle-bias <= self.current_degree_measured_mpu <= angle+bias :
                        if  self.current_degree_measured_mpu >= angle :
                            ### EKF again
                            # theta_from_encoders = self.orientation_of_the_car()
                            # theta_after_ekf = self.ekf_deni_body.calculate_error_turning([theta_from_encoders])
                            self.ACTUAL_CAR_ORIENTATION= target_direction # theta_after_ekf
                            self.current_theta_angle= target_direction # theta_after_ekf
                            self.gyroscope.sum_angular_velocity=0
                            self.gyroscope.actual_theta_angle=0 # added here
                            #### second gyro ################
                            #self.gyroscope_second.sum_angular_velocity = 0
                            #self.gyroscope_second.actual_theta_angle=0 # added here
                            self.current_degree_measured_mpu=0
                            self.travaled_distance_updating()
                            ### update into DB
                            #self.db.update_position_in__DB()
                            #self.orientation_of_the_car() # just print the result from the encoders
                            #print('done orientation')
                            break
                        if dir_rotation == 'L':
                            command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 2)
                        elif dir_rotation == 'R':
                            command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 3)
                        # elif self.current_degree_measured_mpu > angle:
                        #     # 2==turn right, 3 =turn left
                        #     if dir_rotation == 'L':
                        #         command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 2)
                        #     elif dir_rotation == 'R':
                        #         command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 3)
                        # elif self.current_degree_measured_mpu < angle:
                        #     if dir_rotation == 'L':
                        #         command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 3)
                        #     elif dir_rotation == 'R':
                        #         command_mega = self.pid_turning.output(angle, self.current_degree_measured_mpu, 2)

                        self.write_to_mega(command_mega)
                        self.last_time_measurment=time.time()              
                self.write_to_mega('00,0,0,0,0,4,1') #stop car
                return True


    def move_one_step_command(self, direction, distance,LED=0,current_node=0):
        """
        Function: to move the robot in that direction, so far, as var distance says
        when the distance is reach, robot stop
        1. turn the robot in wished direction
        2. far till reach the wished distance
        3.stop, and wait next step

        :param direction: degree 0-360
        :param distance: in cm
        :param current_node: node which I am after move this step
        :return:
        """
        # bigger than some value
        if distance>=self.factor_range:
            self.reduce_factor=0.95
        command_mega=''
        distance*=self.reduce_factor# again add *1
        self.travaled_distance_updating()
        self.distance_enc_last_step = self.current_measured_distance
        #print('New step !!!!!!!!!!!!!!!!!!!!!!!')
        #print(self.ACTUAL_CAR_ORIENTATION)
        #print(self.read_from_mega('dist'))
        #print(f"{distance},  {self.current_measured_distance},  {self.distance_enc_last_step}")
        #if 1==1:
        if self.rotate_car_to_wished_orientation_angle(direction):
            self.travaled_distance_updating() 
            self.distance_enc_last_step=self.current_measured_distance     
            while True:
                self.travaled_distance_updating()

                speed_L=float(self.read_from_mega('speed')[2])
                speed_R=float(self.read_from_mega('speed')[3])
                #print(self.read_from_mega('speed')[2:])
                #print(self.read_from_mega('speed')[1])
                #mpu_a=self.gyroscope.return_real_yaw_angle_in_degree('R')* self.scale_mpu_1
                #mpu_b=self.gyroscope_second.return_real_yaw_angle_in_degree('R')* self.scale_mpu_2
                #print(f"{mpu_a:.2f} , {mpu_b:.2f}")

                if self.distance_enc_last_step==0 and distance==0:
                    new_dist=self.current_measured_distance
                else:
                    new_dist=self.current_measured_distance - self.distance_enc_last_step
                # if distance>self.factor_range:
                #     new_dist+=1 # it is inertion and make 10% more
                if new_dist>=distance or distance==0 :
                    self.distance_enc_last_step=self.current_measured_distance
                    break
                # elif new_dist>distance:
                #     command_mega=self.pid_moving.output_ahead_back(distance, new_dist,6)
                elif new_dist<distance:
                    #command_mega = self.pid_moving.output_ahead_back(distance, new_dist, 5) # ahead
                    #command_mega = self.pid_moving.output_ahead_back_2(speed_L, speed_R, 5)
                    command_mega='00,0,0,0,0,5,1'
                self.write_to_mega(command_mega,LED)
                
               # print(f"theta = {self.orientation_of_the_car()} , {self.gyroscope.return_real_yaw_angle_in_degree('R')} ,  {self.gyroscope_second.return_real_yaw_angle_in_degree('R')}")
        else:
            self.speaking.speak_this("Error I moved longer, than it was needed!!!")
           
        
        self.write_to_mega('00,0,0,0,0,4,1',LED)  # stop the car

        """ ODOMETRY HERE"""
        # print(self.ODOMETRY())
        # self.write_to_mega('00,0,0,0,0,4,1',LED)  # stop the car
         # null encoders
        
        
        """ update the coord of the car with the new values, after moving, EKF?????? """
        self.actual_x_postion,self.actual_y_postion=self.helfer.update_new_coordinates_from_theta_and_dist\
            (self.ACTUAL_CAR_ORIENTATION,self.actual_x_postion,self.actual_y_postion,direction,distance)
        #print(self.actual_x_postion,self.actual_y_postion)
        # update the new coordinates, orientation and node name into DB
        self.db.update_position_in__DB(current_node,self.ACTUAL_CAR_ORIENTATION,self.actual_x_postion,self.actual_y_postion)
        #print('teta ===   ',self.orientation_of_the_car())
        return


    def orientation_of_the_car(self):
        """
        read the value from the mega and return it
        :return: orientation in degrees 0-360
        """
        try:
            from_mega=float(self.read_from_mega('speed')[1]) # second value is theta from encoders
        except:
            from_mega=float(self.read_from_mega('speed')[1])

        # if from_mega <0:
        #     from_mega=360-abs(from_mega)
        #print(f'theta == {from_mega}')
        return from_mega

    def ODOMETRY(self):

        """
        Calculation odometry parameters from speed and theta information
         # RR=(R_w)*((rpm_R + rpm_L )/(rpm_L - rpm_R));

        :return: new x, new y, new theta
        """

        
        THETA = self.orientation_of_the_car()  # in DEG
        vel_L=float(self.read_from_mega('speed')[2]) * self.rpm_to_radians #
        vel_R=float(self.read_from_mega('speed')[3]) * self.rpm_to_radians #

        R=self.width_of_car*((vel_R+vel_L)/(vel_L-vel_R))
        ICC_x= self.actual_x_postion - R * sin(self.ACTUAL_CAR_ORIENTATION)
        ICC_y= self.actual_x_postion + R * cos(self.ACTUAL_CAR_ORIENTATION)


        R_matrix=np.array([[cos(THETA), -sin(THETA), 0 ],
                           [sin(THETA) , cos(THETA) ,0 ],
                           [0         ,   0 ,        1 ],
                           ])
        A=np.array([self.actual_x_postion-ICC_x,
                    self.actual_y_postion-ICC_y,
                    self.ACTUAL_CAR_ORIENTATION])

        B=np.array([ICC_x, ICC_y, THETA])
        odometry= R_matrix @ A + B.T


        return odometry




