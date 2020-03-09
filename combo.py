import calibration #main, distance, get_o_t
import classification #main, distance, readings, classify, calc
import creep #main, pinsetup, init, coxa, femur, tibia, begin, forward, backward, turn_left, turn_right, setServo, setServo_invert, leg1, leg2, leg3, leg4 
import trot #main, pinsetup, begin, leg1_p2l, leg2_l2p, leg3_l2p, leg4_p2l, forward, setServo, setServo_invert, leg1, leg2, leg3, leg4

def set_o_t():
#calibrate and set values
   mean1, mean2, threshold=calibration.get_o_t()
   print(mean1, mean2, threshold)
   classification.x1o=mean1
   classification.x2o=mean1
   classification.threshold=threshold
