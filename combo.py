import calibration #main, distance, get_o_t
import classification #main, distance, readings, classify, calc
import creep #main, pinsetup, init, coxa, femur, tibia, begin, forward, backward, turn_left, turn_right, setServo, setServo_invert, leg1, leg2, leg3, leg4 
import trot #main, pinsetup, begin, leg1_p2l, leg2_l2p, leg3_l2p, leg4_p2l, forward, setServo, setServo_invert, leg1, leg2, leg3, leg4
import time

def set_o_t():
#calibrate and set values
   mean1, mean2, threshold=calibration.get_o_t()
   print(mean1, mean2, threshold)
   classification.x1o=mean1
   classification.x2o=mean2
   classification.threshold=threshold

def main():
   creep.pinsetup()
   creep.begin()
   time.sleep(5)
   set_o_t()
   while(1):
     option3()
 
def option1(): #measures after each step/x steps
     decision=classification.readings()
     if(decision==1): #flat ground
        creep.forward()
#        creep.walk(1,3)
     elif(decision==2): #up stair
        creep.forward()
#        creep.walk(1,3)
     elif(decision==3): #up slope
        creep.forward()
#        trot.walk(3)
     elif(decision==4): #down stair
        creep.forward()
#        creep.walk(1,3)
     elif(decision==5): #down slope
        creep.forward()
#        creep.walk(1,3)

def option2(): #segregate according to creep and trot
     decision=classification.readings()
     if(decision==3): #up slope is trot
        trot.forward()
#        trot.walk(3)
     else:
        creep.forward()
#        creep.walk(1,3)

def option3(): #obstacle
    print(classification.x1o,classification.x2o, classification.threshold)
    decision=classification.stream()
    print(decision)
    if(decision==6): #obstacle
        creep.walk(2,3) #back
        creep.walk(4,5) #turn right by convention
    else: #flat ground/up down slope/up down stair
        creep.walk(1,3)

if __name__ == '__main__':
    main()
