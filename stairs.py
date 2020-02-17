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

leg1_offset = [0,10,10,0] #first 0 is dummy
leg2_offset = [0,0,10,0]
leg3_offset = [0, 0,20,-10]
leg4_offset = [0,0,0,-10]

front_lateral = 140
front_parallel = 90
front_lateral_add = 0

back_lateral = 40
back_parallel = 90
back_lateral_add = 0

footup_13 = 60
footup_24= 120
footdown=90

pincer_up_13= 60
pincer_up_24 = 120
pincer_down = 90

leg1_footdown = footdown
leg2_footdown = footdown
leg3_footdown = footdown
leg4_footdown = footdown

leg_formation = 0

channel_cur = [0,90,90,90,90,90,90,90,90,90,90,90,90]

def pinsetup():
    GPIO.setmode(GPIO.BOARD)
    
def main():
    pinsetup()
    
def init():
    #all are lateral
    print("init")
    leg1(front_lateral,footdown,pincer_down) #leftside
    leg2(back_lateral,footdown,pincer_down)

    leg3(back_lateral,footdown,pincer_down) #rightside
    leg4(front_lateral,footdown,pincer_down)

def setServo(channel,angle):
    if(angle<0):
        angle = 0
    elif(angle>180):
        angle = 180
    i2c_mutex.acquire()
    pwm.set_pwm(channel,0,(int)((angle*2.5)+150))
    i2c_mutex.release()

def setServo_invert(channel,angle):
    if(angle<0):
        angle = 0
    elif(angle>180):
        angle = 180

    i2c_mutex.acquire()
    pwm.set_pwm(channel,0,(int)((angle*-2.5)+600))
    i2c_mutex.release()


def leg1(angle1,angle2,angle3):
    angle1 = angle1+leg1_offset[1]
    angle2 = angle2+leg1_offset[2]
    angle3 = angle3+leg1_offset[3]

    while(channel_cur[1] != angle1 or channel_cur[2] != angle2 or channel_cur[3] != angle3 ):
        ##ANGLE1
        if angle1 > channel_cur[1]:
            channel_cur[1] = channel_cur[1] +1
            setServo_invert(1,channel_cur[1])
        elif angle1 < channel_cur[1]:
            channel_cur[1] = channel_cur[1] -1
            setServo_invert(1,channel_cur[1])

        ##ANGLE2
        if angle2 > channel_cur[2]:
            channel_cur[2] = channel_cur[2] +1
            setServo_invert(2,channel_cur[2])
        elif angle2 < channel_cur[2]:
            channel_cur[2] = channel_cur[2] -1
            setServo_invert(2,channel_cur[2])

        ##ANGLE3
        if angle3 > channel_cur[3]:
            channel_cur[3] = channel_cur[3] +1
            setServo(3,channel_cur[3])
        elif angle3 < channel_cur[3]:
            channel_cur[3] = channel_cur[3] -1
            setServo(3,channel_cur[3])

        time.sleep(move_delay)




def leg2(angle1,angle2,angle3):
    angle1 = angle1+leg2_offset[1]
    angle2 = angle2+leg2_offset[2]
    angle3 = angle3+leg2_offset[3]

    while(channel_cur[4] != angle1 or channel_cur[5] != angle2 or channel_cur[6] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[4]:
            channel_cur[4] = channel_cur[4] +1
            setServo_invert(4,channel_cur[4])
        elif angle1 < channel_cur[4]:
            channel_cur[4] = channel_cur[4] -1
            setServo_invert(4,channel_cur[4])

        ##ANGLE2
        if angle2 > channel_cur[5]:
            channel_cur[5] = channel_cur[5] +1
            setServo_invert(5,channel_cur[5])
        elif angle2 < channel_cur[5]:
            channel_cur[5] = channel_cur[5] -1
            setServo_invert(5,channel_cur[5])

        ##ANGLE3
        if angle3 > channel_cur[6]:
            channel_cur[6] = channel_cur[6] +1
            setServo(6,channel_cur[6])
        elif angle3 < channel_cur[6]:
            channel_cur[6] = channel_cur[6] -1
            setServo(6,channel_cur[6])

        time.sleep(move_delay)



def leg3(angle1,angle2,angle3):
    angle1 = angle1+leg3_offset[1]
    angle2 = angle2+leg3_offset[2]
    angle3 = angle3+leg3_offset[3]

    while(channel_cur[7] != angle1 or channel_cur[8] != angle2 or channel_cur[9] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[7]:
            channel_cur[7] = channel_cur[7] +1
            setServo(7,channel_cur[7])
        elif angle1 < channel_cur[7]:
            channel_cur[7] = channel_cur[7] -1
            setServo(7,channel_cur[7])

        ##ANGLE2
        if angle2 > channel_cur[8]:
            channel_cur[8] = channel_cur[8] +1
            setServo_invert(8,channel_cur[8])
        elif angle2 < channel_cur[8]:
            channel_cur[8] = channel_cur[8] -1
            setServo_invert(8,channel_cur[8])

        ##ANGLE3
        if angle3 > channel_cur[9]:
            channel_cur[9] = channel_cur[9] +1
            setServo(9,channel_cur[9])
        elif angle3 < channel_cur[9]:
            channel_cur[9] = channel_cur[9] -1
            setServo(9,channel_cur[9])

        time.sleep(move_delay)

def leg4(angle1,angle2,angle3):
    angle1 = angle1+leg4_offset[1]
    angle2 = angle2+leg4_offset[2]
    angle3 = angle3+leg4_offset[3]

    while(channel_cur[10] != angle1 or channel_cur[11] != angle2 or channel_cur[12] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[10]:
            channel_cur[10] = channel_cur[10] +1
            setServo(10,channel_cur[10])
        elif angle1 < channel_cur[10]:
            channel_cur[10] = channel_cur[10] -1
            setServo(10,channel_cur[10])

        ##ANGLE2
        if angle2 > channel_cur[11]:
            channel_cur[11] = channel_cur[11] +1
            setServo_invert(11,channel_cur[11])
        elif angle2 < channel_cur[11]:
            channel_cur[11] = channel_cur[11] -1
            setServo_invert(11,channel_cur[11])

        ##ANGLE3
        if angle3 > channel_cur[12]:
            channel_cur[12] = channel_cur[12] +1
            setServo(12,channel_cur[12])
        elif angle3 < channel_cur[12]:
            channel_cur[12] = channel_cur[12] -1
            setServo(12,channel_cur[12])

        time.sleep(move_delay)

if __name__ == '__main__':
    main()
