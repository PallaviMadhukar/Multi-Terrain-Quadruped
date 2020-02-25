#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import math

PIN_TRIGGER1 = 12
PIN_ECHO1 = 16
      
PIN_TRIGGER2=18
PIN_ECHO2=22

x1o=6.72
x2o=9.15
threshold=1
limit=300
alpha=math.pi/3
l=6
theta_limit=30
h_limit=5

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

def calc(x1,x2):
      h=round((x2o-x2)*math.sin(alpha),2)
      theta=(math.pi/2)-alpha-math.atan((abs(x1-x2))/l)
      theta=round(math.degrees(theta),2)
      return h,theta

def classify(x1,x2):
    h,theta=calc(x1,x2)
    print(h,theta)
    if((abs(x1-x1o)<=threshold) and (abs(x2-x2o)<=threshold)):
      print("Flat ground")
    elif((x1-x1o)<=(-threshold)and (x2-x2o)<=(-threshold) and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      if(theta>1 and theta<theta_limit):
         print("Up slope")
      elif(h<h_limit):
         print("Up stair")
      else:
         print("Obstacle")
    elif((x1-x1o)>threshold and (x2-x2o)>threshold and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      print("Down stairs")
    elif(abs(x1-x1o)>threshold and abs(x2-x2o)>threshold and x1-x1o-threshold>x2-x2o+threshold):
      print("Down slope")

try:
 while(1):
    dist1=distance(PIN_TRIGGER1,PIN_ECHO1)
    while(dist1>limit):
      print("Waiting for dist 1")
      dist1=distance(PIN_TRIGGER1,PIN_ECHO1)
    dist2=distance(PIN_TRIGGER2,PIN_ECHO2)
    while(dist2>limit):
      print("Waiting for dist 2")
      dist2=distance(PIN_TRIGGER2,PIN_ECHO2)
    print( "Distance1: ",dist1,"cm")
    print( "Distance2: ",dist2,"cm")
    classify(dist1,dist2)


finally:
   pass
