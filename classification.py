#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import math

#writing into file
f=open("mapping_text.txt","w+")

PIN_TRIGGER1 = 12
PIN_ECHO1 = 16
      
PIN_TRIGGER2=18
PIN_ECHO2=22

PIN_TRIGGER3=19
PIN_ECHO3=21

x1o=14.34
x2o=17.75
threshold=1
limit=100 #garbage values
alpha=math.pi/3 #90- angle at which sensors are placed
l=6 #distance between sensors
theta_min=0 #angle at which walking style has to change
theta_max=15 #angle beyond which robot cannot climb slope
h_limit_up=0.5 #stair difference in height
h_limit_down=0.9
obstacle=25 #

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
    print(avg_h,theta)
    if((abs(x1-x1o)<=threshold) and (abs(x2-x2o)<=threshold)):
      print("Flat ground")
      f.write("1\n")
      return 1
    elif((x1-x1o)<=(-threshold)and (x2-x2o)<=(-threshold) and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      print(abs(x2-x1))
      print(abs(h1-h2))
      if(abs(h1-h2)<h_limit_up):
         print("Up stair with height ",avg_h)
         f.write("2\n")
         return 2
      elif(theta>theta_min and theta<theta_max):
         print("Up slope with angle ", theta)
         f.write("3\n")
         return 3
      else:
         print("Robot cannot climb up")
         f.write("6\n")
         return 6
    elif((x1-x1o)>threshold and (x2-x2o)>threshold and abs(x1-x1o)-threshold<abs(x2-x2o)+threshold):
      print(abs(x2-x1))
      print(abs(h1-h2))
      if(abs(h1-h2)<h_limit_down):
          print("Down stairs with height ", avg_h)
          f.write("4\n")
          return 4
      else:
         print("Robot cannot climb down")
         f.write("6\n")
         return 6
    elif(abs(x1-x1o)>threshold and abs(x2-x2o)>threshold and x1-x1o-threshold>x2-x2o+threshold):
#      if(abs(theta)>theta_min and abs(theta)<theta_max):
         print(abs(x2-x1))
         print(abs(h1-h2))
         print("Down slope with angle ", theta)
         f.write("5\n")
         return 5
    else:
      return 0

def readings():
 while(1):
  dist3=round(distance(PIN_TRIGGER3,PIN_ECHO3),2)
  print( "Distance3: ",dist3,"cm")
  if(dist3<obstacle):
    dist3=round(distance(PIN_TRIGGER3,PIN_ECHO3),2)
    print( "Distance3: ",dist3,"cm")
    if(dist3<obstacle):
      f.write("%f 6\n" %dist3)
      return 6
#  else:
  f.write("%f " %dist3)
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
      return decision

def stream():
 while(1):
  dist3=round(distance(PIN_TRIGGER3,PIN_ECHO3),2)
  print( "Distance3: ",dist3,"cm")
  if(dist3<obstacle):
    dist3=round(distance(PIN_TRIGGER3,PIN_ECHO3),2)
    print( "Distance3: ",dist3,"cm")
    if(dist3<obstacle):
      f.write("%f 6\n" %dist3)
      return 6
  f.write("%f " %dist3)
#  else:
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
  print(decision)
  if(decision):
      return decision
      
def main():
   try:
      while(1):
         output=readings()
         rd=input("Another reading? Enter y/n: ")
         if(rd=='n'):
           break;
   except KeyboardInterruptError:
      f.close()

if __name__ == '__main__':
    main()

