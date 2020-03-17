#!/usr/bin/python
import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER1 = 19
PIN_ECHO1 = 21
      
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

finally:
    GPIO.cleanup()
