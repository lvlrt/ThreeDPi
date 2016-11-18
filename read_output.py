import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
for i in [5, 25,24,23,19,13,12,6,21,20,26,16,22,27,18,17]:
	GPIO.setup(i, GPIO.OUT)
for i in [5, 25,24,23,19,13,12,6,21,20,26,16,22,27,18,17]:
	print(GPIO.input(i))
