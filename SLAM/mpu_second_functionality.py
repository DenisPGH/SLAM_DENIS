import time
import smbus
from time import sleep
import math

### THE ADRESS OF THIS MPU MUSS NOT TO BE 0x68!!!!!!!!!!

class MPU_SECOND:
    def __init__(self):
        self.BUS_NANO=0
        self.actual_theta_angle = 0
        self.bus = smbus.SMBus(self.BUS_NANO)  # or bus = smbus.SMBus(0) for older version boards
        self.Device_Address = 0x69 # 0x69
        self.PWR_MGMT_1 = 0x6B
        self.SMPLRT_DIV = 0x19
        self.CONFIG = 0x1A
        self.GYRO_CONFIG = 0x1B
        self.INT_ENABLE = 0x38
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47
        self.interval_measurment = 0.1  # 100ms
        self.prev_time = 0
        self.current_time = 0
        self.offset_z = 0
        self.sum_angular_velocity = 0  # sum of angular velocity, measured from gyroscope
        self.mpu_yaw_divider_factor = 2940 # old on

        self.mpu_yaw_divider_factor_left = 3600 # 3600    dies shoud be changed to lower/higher
        
        self.mpu_yaw_divider_factor_right = 3200 # 3200
        self.real_yaw_angle_degrees = 0

        self.HIGH_NEUTRAL_RANGE = 100# 90
        self.LOW_NEUTRAL_RANGE = -120 # -200
        ##############################
        self.ERROR_FACTOR_TURNING_RIGHTS=1

    def MPU_Init(self):
        """ helper for measuring MPU"""
        # write to sample rate register
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 7)

        # Write to power management register
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)

        # Write to Configuration register
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)

        # Write to Gyro configuration register
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24)

        # Write to interrupt enable register
        self.bus.write_byte_data(self.Device_Address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        """ helper for measuring MPU"""
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if (value > 32768):
            value = value - 65536
        return value

    def current_angular_velocity_yaw_angle(self):
        """
        mesure the acc of z
        :return: current acceleration-angular velocity
        """
        try:
            self.MPU_Init()
            gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
        except:
            self.MPU_Init()
            gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
        #self.MPU_Init()
        #gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
        self.actual_theta_angle = gyro_z
        if self.actual_theta_angle >= self.HIGH_NEUTRAL_RANGE or \
                self.actual_theta_angle <= self.LOW_NEUTRAL_RANGE:
            return self.actual_theta_angle
        else:
            return 0

    def return_true_if_angle_reached(self, wished_angle):
        """
        it measure the acc and calculate the real angle of rotation,
         if wished angle is reached return TRUE

        :param wished_angle: angle wich I want to achieve
        :return: when is acheave return True
        """
        self.sum_angular_velocity = 0
        g_gain = 0.07
        est_drift_z = 0.01
        in_deg = 0
        while True:
            in_deg = self.sum_angular_velocity // self.mpu_yaw_divider_factor
            if in_deg >= wished_angle:
                self.sum_angular_velocity = 0
                break
            else:
                # print(f"{self.current_angle_degree*3.3/1024:.2f}")
                # print(f"{in_deg:.2f}")
                pass

            self.current_time = time.time()
            # acc = self.current_gyro_acc_of_yaw_angle()* g_gain
            acc = self.current_angular_velocity_yaw_angle()
            # delta_time=(self.current_time-self.prev_time)
            delta_time = 0.02
            current_angle_z = acc * delta_time - est_drift_z
            # self.current_angle_degree+=current_angle_z # only test, formula need here
            self.sum_angular_velocity += acc  # only test, formula need here
            self.prev_time = self.current_time

        return True

    def return_real_yaw_angle_in_degree(self, dir_turning: str):
        """
        dir_turning= R or L
        it calculate the angle of rotation in degrees and store it to
        mpu_current_yaw_angle and also return the calculated
        :return: real angle in degrees
        """
        current_angular_velocity = self.current_angular_velocity_yaw_angle()
        if dir_turning == 'R':
            self.sum_angular_velocity += abs(current_angular_velocity)
            self.real_yaw_angle_degrees = self.sum_angular_velocity // self.mpu_yaw_divider_factor_right
            return self.real_yaw_angle_degrees
        elif dir_turning == 'L':
            self.sum_angular_velocity += abs(current_angular_velocity)
            self.real_yaw_angle_degrees = self.sum_angular_velocity // self.mpu_yaw_divider_factor_left
            return self.real_yaw_angle_degrees

    def reset(self):
        return

# a=MPU()
# b=a.return_true_if_angle_reached(100)
# print(b)