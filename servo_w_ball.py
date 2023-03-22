#!/usr/bin/env python
import RPi.GPIO as GPIO
import pigpio
import time
import socket
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

pwm = pigpio.pi()
pwm.set_mode(servo2, pigpio.OUTPUT)
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo2, 50 )
pwm.set_PWM_frequency( servo, 100 )

# mo = 1700
# l = 1800
# r = 1600

# mo = 900
# d = 1000
# u = 800
pwm.set_servo_pulsewidth(servo,1700)
pwm.set_servo_pulsewidth( servo2, 900 )
while True:
    data= conn.recv(BUFFER_SIZE)
    if not data:break
    print("recieved data:", data)
    # d= int(data)
    # print(d)
    #conn.send(data)
    # if data == b'52':
        # print('move servo')
        # pwm.set_servo_pulsewidth( servo, 1600 )
        # pwm.set_servo_pulsewidth( servo2, 900 )
        # # time.sleep(0.5)
        # # pwm.set_servo_pulsewidth(servo,1700)
    # if data == b'85':
        # print('move servo!!!')
        # pwm.set_servo_pulsewidth( servo, 1700 )
        # pwm.set_servo_pulsewidth( servo2, 1000 )
        
        
        
    # if data == b':
        # print( "0 deg" )
        # pwm.set_servo_pulsewidth( servo, 1700 )
        # pwm.set_servo_pulsewidth( servo2, 900 )
         
     
    # x = input()
        
    if data == b'l':
        print( "left" )
        pwm.set_servo_pulsewidth( servo, 1800 ) 
        pwm.set_servo_pulsewidth( servo2, 900 )
        # time.sleep(0.5)
    if data == b'r':
        print( "right" )
        pwm.set_servo_pulsewidth( servo, 1600 )
        # pwm.set_servo_pulsewidth( servo2, 900 ) 
        # time.sleep(0.5)
    if data == b'u':
        print( "up" )
        pwm.set_servo_pulsewidth( servo2, 800 )
        # pwm.set_servo_pulsewidth( servo, 1700 )
        # time.sleep(0.5)
    if data == b'd':
        print( "down" )
        pwm.set_servo_pulsewidth( servo2, 1000 )
        # pwm.set_servo_pulsewidth( servo, 1700 )
    if data == b'nan':
        pass
    # if x == 'm':
        # print( "0deg" )
        # pwm.set_servo_pulsewidth( servo2, 900 )
        # # pwm.set_servo_pulsewidth( servo, 1700 )
    # if x == 'e':
        # break
