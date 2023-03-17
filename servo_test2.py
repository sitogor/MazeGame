from gpiozero import Servo 
from time import sleep 

from gpiozero.pins.pigpio import PiGPIOFactory 

factory = PiGPIOFactory()

servo = Servo(18, min_pulse_width = 0.5/1000 , max_pulse_width = 2.5/1000, pin_factory = factory)

while(1):
	x = input()
	
	
	# for values in range(-180,180,60):
	servo.value =  float(x)
	sleep(1)
