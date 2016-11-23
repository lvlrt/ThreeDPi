import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
for i in [5, 25,24,23,19,13,12,6,21,20,26,16,22,27,18,17]:
	GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
for i in [5, 25,24,23,19,13,12,6,21,20,26,16,22,27,18,17]:
	GPIO.output(i, 0)
#for interactive
print('5, 25,24,23,19,13,12,6,21,20,26,16,22,27,18,17')
print('GPIO.output(i, 0)')
