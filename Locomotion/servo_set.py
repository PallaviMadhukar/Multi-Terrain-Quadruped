from __future__ import division
import time
import RPi.GPIO as GPIO
from threading import Thread, Lock

cur_angle_mutex = Lock()
i2c_mutex = Lock()

# Import the PCA9685 module.
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

pwm.set_pwm_freq(60)

move_delay = 0.0005
step_delay = 0.001

channel_cur = [0,90,90,90,90,90,90,90,90,90,90,90,90]

def main():
    pinsetup()
    for i in range(1,13):
      test(i) #enter channel

#        _____
#3 2 1 -|     |-  10 11 12 
#       |     |
#6 5 4 -|_____|-   7  8  9
#       |_____|

def pinsetup():
    GPIO.setmode(GPIO.BOARD)

def test(channel):
  setServo(channel,89)

def setServo(channel,angle):
    if(angle<0):
        angle = 0
    elif(angle>180):
        angle = 180
    i2c_mutex.acquire()
    pwm.set_pwm(channel,0,(int)((angle*2.5)+150))
    i2c_mutex.release()

if __name__ == '__main__':
    main()
