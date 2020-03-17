#!/usr/bin/python
import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER1 = 12
PIN_ECHO1 = 16
      
PIN_TRIGGER2=18
PIN_ECHO2=22

#PIN_TRIGGER2=19
#PIN_ECHO2=21

#GPIO.setup(PIN_TRIGGER1, GPIO.OUT)
#GPIO.setup(PIN_ECHO1, GPIO.IN)
##GPIO.setup(PIN_TRIGGER2, GPIO.OUT)
#GPIO.setup(PIN_ECHO2, GPIO.IN)

def distance(PIN_TRIGGER, PIN_ECHO):
      GPIO.setmode(GPIO.BOARD)
      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)
      GPIO.output(PIN_TRIGGER, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(PIN_TRIGGER, GPIO.HIGH)
      time.sleep(0.00001)
      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      pulse_start_time=time.time()
      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      dist = round(pulse_duration * 17150, 2)
      GPIO.cleanup()
      return dist
try:
 while(1):
    dist1=distance(PIN_TRIGGER1,PIN_ECHO1)
    print( "Distance1: ",dist1,"cm")
    dist2=distance(PIN_TRIGGER2,PIN_ECHO2)
    #dist1b=distance(PIN_TRIGGER1,PIN_ECHO1)
    #dist2b=distance(PIN_TRIGGER2,PIN_ECHO2)
    #dist1=round((dist1a+dist1b)/2)
    #dist2=round((dist2a+dist2b)/2)
    print( "Distance2: ",dist2,"cm")

finally:
    GPIO.cleanup()
