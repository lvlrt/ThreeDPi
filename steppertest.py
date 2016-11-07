#	Simple Test Code for Rapsberry Pi Laser Engraver
#	Ian D. Miller
#	Jan 7, 2014
#	http://www.pxlweavr.com
#	info [at] pxlweavr.com

print("Program Started")

import RPi.GPIO as GPIO
import Motor_control
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
from numpy import pi, sin, cos, sqrt, arccos, arcsin

#Test program for stepper motor

GPIO.setmode(GPIO.BCM)

motor=Bipolar_Stepper_Motor(5,25,24,23)
motor2=Bipolar_Stepper_Motor(19,13,12,6)
motor3=Bipolar_Stepper_Motor(21,20,26,16)

try:
    while True:
        direction = int(input("Input Direction X: "))
        steps = int(input("Input Step Number X: "))
        direction2 = int(input("Input Direction Y: "))
        steps2 = int(input("Input Step Number Y: "))
        direction3 = int(input("Input Direction Z: "))
        steps3 = int(input("Input Step Number Z: "))

        motor.move(direction,steps,0.01)
        motor2.move(direction2,steps2,0.01)
        motor3.move(direction3,steps3,0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
