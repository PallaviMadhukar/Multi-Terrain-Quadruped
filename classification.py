#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import math

PIN_TRIGGER1 = 12
PIN_ECHO1 = 16
      
PIN_TRIGGER2=18
PIN_ECHO2=22

x1o=4.86
x2o=8.45
threshold=0.5
limit=100 #garbage values
alpha=math.pi/3 #90- angle at which sensors are placed
l=6 #distance between sensors
theta_min=4.5 #angle at which walking style has to change
theta_max=30 #angle beyond which robot cannot climb slope
h_limit_up=0.5 #stair difference in height
h_limit_down=0.9

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
      h1=round((x1o-x1)*math.sin(alpha),2)
      h2=round((x2o-x2)*math.sin(alpha),2)
      theta=(math.pi/2)-alpha-math.atan((abs(x1-x2))/l)
      theta=round(math.degrees(theta),2)
      return h1,h2,theta

def classify(x1,x2):
    h1,h2,theta=calc(x1,x2)
    avg_h=(h1+h2)/2
    print(h1,h2,theta)
    if((abs(x1-x1o)<=threshold) and (abs(x2-x2o)<=threshold)):
      print("Flat ground")
      return 1
    elif((x1-x1o)<=(-threshold)and (x2-x2o)<=(-threshold) and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      print(abs(x2-x1))
      print(abs(h1-h2))
      if(abs(h1-h2)<h_limit_up):
         print("Up stair with height ",avg_h)
         return 1
      elif(theta>theta_min and theta<theta_max):
         print("Up slope with angle ", theta)
         return 1
    elif((x1-x1o)>threshold and (x2-x2o)>threshold and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      print(abs(x2-x1))
      print(abs(h1-h2))
      if(abs(h1-h2)<h_limit_down):
          print("Down stairs with height ", avg_h)
          return 1
    elif(abs(x1-x1o)>threshold and abs(x2-x2o)>threshold and x1-x1o-threshold>x2-x2o+threshold):
#      if(abs(theta)>theta_min and abs(theta)<theta_max):
         print(abs(x2-x1))
         print(abs(h1-h2))
         print("Down slope with angle ", theta)
         return 1
    else:
      return 0

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
    decision=classify(dist1,dist2)
    if(decision):
      rd=input("Another reading? Enter y/n: ")
      if(rd=='n'):
        break;

except KeyboardInterrupt:
   pass
