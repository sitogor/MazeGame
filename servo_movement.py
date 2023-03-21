#!/usr/bin/env python
import RPi.GPIO as GPIO
import pigpio
import time

servo = 18
servo2 = 17

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
 
while True:
    x = str(input())

    if x == 'mo':
        print( "0 deg" )
        pwm.set_servo_pulsewidth( servo, 1700 )
        pwm.set_servo_pulsewidth( servo2, 900 )
         
        time.sleep(0.5)
    if x == 'l':
        print( "left" )
        pwm.set_servo_pulsewidth( servo, 1800 ) 
        pwm.set_servo_pulsewidth( servo2, 900 )
        time.sleep(0.5)
    if x == 'r':
        print( "right" )
        pwm.set_servo_pulsewidth( servo, 1600 )
        # pwm.set_servo_pulsewidth( servo2, 900 ) 
        time.sleep(0.5)
    if x == 'u':
        print( "up" )
        pwm.set_servo_pulsewidth( servo2, 800 )
        # pwm.set_servo_pulsewidth( servo, 1700 )
        time.sleep(0.5)
    if x == 'd':
        print( "down" )
        pwm.set_servo_pulsewidth( servo2, 1000 )
        # pwm.set_servo_pulsewidth( servo, 1700 )
    if x == 'm':
        print( "0deg" )
        pwm.set_servo_pulsewidth( servo2, 900 )
        # pwm.set_servo_pulsewidth( servo, 1700 )
    if x == 'e':
        break

# while True:
    # print( "0 deg" )
    # pwm.set_servo_pulsewidth( servo2, 900 ) ;
    # time.sleep(3)
    
    # print( "down" )
    # pwm.set_servo_pulsewidth( servo2, 1000 ) ;
    # time.sleep(3)
    
    # print( "up" )
    # pwm.set_servo_pulsewidth( servo2, 800 ) ;
    # time.sleep(3)

# turning off servo
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )

pwm.set_PWM_dutycycle( servo2, 0 )
pwm.set_PWM_frequency( servo2, 0 )
