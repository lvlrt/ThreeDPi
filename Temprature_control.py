#imports
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 
import RPi.GPIO as GPIO
import sys

pin=2
channel=0
goal_temp=sys.argv[1]

fixed_R=4700
max_adc=1023

SPI_PORT=0
SPI_DEVICE=0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT,SPI_DEVICE))

print('Temprature set to '+goal_temp)

#setup GPIO en pin setup out
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT)

lookupfile = open('lookuptable','r')
lookuptable = {}
for line in lookupfile:
    lookuptable[int(line.split(',')[0])]=int(line.split(',')[1].replace('\n',''))


def calc_adc_val(temp):
    
    #TODO resistance??
    #adc_val=R/(R+fixed_R)*max_adc
    for adc_val,t in lookuptable.items():
        if t==int(temp):
            print(temp+' equals to adc of ',adc_val)
            return adc_val

def calc_temp(adc_val):
    #R=fixed_R/(max_adc/adc_val-1)
    #TODO resistance to temp
    if adc_val in lookuptable:
        return lookuptable[adc_val]
    else:
        return ''

goal_adc_val = calc_adc_val(goal_temp)

try:
    while True:
        if mcp.read_adc(channel) < goal_adc_val:
            GPIO.output(pin,1)
            print('Heating up... ['+calc_temp(mcp.read_adc(channel))+']')
        else:
            GPIO.output(pin,0)
            print('Temprature reached ['+calc_temp(mcp.read_adc(channel))+']')
        time.sleep(1)
except KeyboardInterrupt:
    #TODO null the pin
    GPIO.output(pin,0)
    print('Heater turned off')
    pass
