#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import statistics
#GPIO.setmode(GPIO.BOARD)

PIN_TRIGGER1 = 12
PIN_ECHO1 = 16
      
PIN_TRIGGER2=18
PIN_ECHO2=22

num_measure=20
limit=50

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
  dist1=[]
  dist2=[]
  for x in range(num_measure):
    reading1=distance(PIN_TRIGGER1,PIN_ECHO1)
    reading2=distance(PIN_TRIGGER2,PIN_ECHO2)
    print(x, reading1, reading2)
    if(reading1<limit):
      dist1.append(reading1)
    if(reading2<limit):
      dist2.append(reading2)

  print("dist1")
  print("Minimum=",min(dist1))
  print("Maximum=",max(dist1))
  print("Mean=",round(statistics.mean(dist1),2))
  print("\ndist2")
  print("Minimum=",min(dist2))
  print("Maximum=",max(dist2))
  print("Mean=",round(statistics.mean(dist2),2))

finally:
  pass
