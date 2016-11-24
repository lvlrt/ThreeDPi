#imports
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 
import RPi.GPIO as GPIO
import sys

goal_temp=sys.argv[1]

pin=15
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin,1)
pwm.start(0)

a_pin = 8
b_pin = 9

def discharge():
  GPIO.setup(a_pin, GPIO.IN)
  GPIO.setup(b_pin, GPIO.OUT)
  GPIO.output(b_pin, False)
  time.sleep(0.005)

def charge_time():
  GPIO.setup(b_pin, GPIO.IN)
  GPIO.setup(a_pin, GPIO.OUT)
  count = 0
  GPIO.output(a_pin, True)
  while not GPIO.input(b_pin):
    count = count + 1
  return count

print('Temprature set to '+goal_temp)

lookupfile = open('temp_resistor_val_table','r')
lookuptable = {}
for line in lookupfile: #get a lookuptable with the key the temp and the value the time value to fill the capacitor to a 1.65V
    lookuptable[float(line.split(',')[0])]=float(line.split(',')[2].replace('\n',''))

def calc_ttfc(temp):
    
    #adc_val=R/(R+fixed_R)*max_adc
    for t,ttfc in lookuptable.items():
        print(t)
        if t==int(temp):
            print(temp+' equals to ttfc of ',ttfc)
            return ttfc

def calc_temp(v):
    #R=fixed_R/(max_adc/adc_val-1)
    #TODO resistance to temp
    diff = float('inf')
    for temperature,ttfc in lookuptable.items():
        if diff > abs(v-ttfc):
            diff=abs(v-ttfc)
            x=temperature
    return x

goal_ttfc = calc_ttfc(goal_temp)

try:
    while True:
        discharge()
        ttfc=charge_time()
        discharge()
        if ttfc > goal_ttfc:
            pwm.ChangeDutyCycle(50)
            #GPIO.output(pin,1)
            print('Heating up... ['+str(calc_temp(ttfc))+']')
        else:
            pwm.ChangeDutyCycle(0)
            #GPIO.output(pin,0)
            print('Temprature reached ['+str(calc_temp(ttfc))+']')
        time.sleep(1)
except KeyboardInterrupt:
    #TODO null the pin
    pwm.stop()
    GPIO.output(pin,0)
    print('Heater turned off')
    pass
