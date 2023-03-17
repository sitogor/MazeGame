#!/usr/bin/env python
import RPi.GPIO as GPIO
import pigpio
import time

servo = 27

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)


pwm.set_PWM_frequency( servo, 50 )

# mo = 1700
# l = 1800
# r = 1600

while True:
    x = str(input())

    if x == 'mo':
        print( "0 deg" )
        pwm.set_servo_pulsewidth( servo, 1700 ) 
        time.sleep(0.5)
    if x == 'l':
        print( "left" )
        pwm.set_servo_pulsewidth( servo, 1800 ) 
        time.sleep(0.5)
    if x == 'r':
        print( "right" )
        pwm.set_servo_pulsewidth( servo, 1600 ) 
        time.sleep(0.5)
    
    if x == 'e':
        break

# print( "0 deg" )
# pwm.set_servo_pulsewidth( servo, 1700 ) ;
# time.sleep( 3 )

# print( "left" )
# pwm.set_servo_pulsewidth( servo, 1800 ) ;
# time.sleep( 3 )

# print( "right" )
# pwm.set_servo_pulsewidth( servo, 1600 ) ;
# time.sleep( 3 )

# turning off servo
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )
