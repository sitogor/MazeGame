#!/usr/bin/env python
import RPi.GPIO as GPIO
import pigpio
import time
import socket
import math 
TCP_IP = '169.254.22.20'
TCP_PORT = 5005
BUFFER_SIZE = 20
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn,addr = s.accept()
print('Connection adddress:', addr)

servo = 17
servo2 = 18


# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
servo_middle = 1545
k1 = 50 #scale factor for servo1
# servo_left = 1510
# servo_right = 1580


servo2_middle = 917
k2 = 83 #scale factor for servo2
# servo2_down = 954
# servo2_up = 880



pwm = pigpio.pi()
pwm.set_mode(servo2, pigpio.OUTPUT)
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo2, 50 )
pwm.set_PWM_frequency( servo, 100 )

# # mo = 1700
# # l = 1800
# # r = 1600

# # mo = 900
# # d = 1000
# # u = 800
pwm.set_servo_pulsewidth(servo,servo_middle)
pwm.set_servo_pulsewidth( servo2, servo2_middle )

while True:
    data= conn.recv(BUFFER_SIZE)
    if not data:break
    print("recieved data:", data)
    pwm.set_servo_pulsewidth( servo, data[0])
    pwm.set_servo_pulsewidth( sero2,data[1])
    # d1 = data[0]*math.cos(data[1])
    # d2 = data[0]*math.sin(data[1])
    # duty1 = servo_middle + d1*k1
    # duty2 = servo_middle + d2*k2
    # pwm.set_servo_pulsewidth( servo,duty1 )
    # pwm.set_servo_pulsewidth( servo2, duty2 )

