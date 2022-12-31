
"""
1. def with comunication to ardino nano via UART
2. return the currect orientation from MPU
"""
import serial
serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
def read_mpu_from_arduino_nano():
    # return the value of MPU z angle=> 0-360
    data=''
    if serial_port.inWaiting() > 0:  # chete ot MEGA
        data = serial_port.read()
    return data
