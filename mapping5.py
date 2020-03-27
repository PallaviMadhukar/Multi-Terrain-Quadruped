from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import matplotlib.pyplot as plt
import math

#import classification
#obstacle_limit=classification.obstacle
obstacle_limit=25
scale=5
threshold=obstacle_limit/scale+1

f= open("mapping_text.txt","r")
string=str(f.read())
string=(string.strip()).split("\n")
f.close()

l=[] #all elements
for line in string:
    l.append(line.split(" "))

l1=[] #only decision var
for row in range(len(l)):
    l1.append(l[row][1])

l1=[] #only ultrasonic
for row in range(len(l)):
    l1.append(math.floor(float(l[row][0])/scale)+1)
print(l1)

l2=[] #only decision var
for row in range(len(l)):
    l2.append(int(l[row][1]))

sq=max(l1)*3
if ((sq%2)==0): #make even odd
   sq=sq+1
mid=math.floor(sq/2)
print(sq, mid)

obstacle=1 #prob of obstacle ----1/3
clear= -1
unsure=0
#obstacle=0 #prob of white space
#clear=1

compass=1 #n,s,e,w

def main():  
  global compass
  bw = [[unsure for i in range(sq)] for j in range(sq)]
  print(bw)

  bw[mid][mid]=clear #init position
  a=mid #x position
  b=mid #y position
  print(a,b,compass)

  al,bl,ar,br=body(a,b,compass)
  if(bw[bl][al]!=clear):
      bw[bl][al]=(bw[bl][al]*0.2+clear*0.8)
  if(bw[br][ar]!=clear):
      bw[br][ar]=(bw[br][ar]*0.2+clear*0.8)
      
  for count, num in enumerate(l1): #obstacle at num
    num=int(num)
    obs_a=a
    obs_b=b
    for steps in range(0, num):
        #obstacle is num steps infront of current step
        obs_a,obs_b,_ =set_axis(obs_a,obs_b,compass,1) #we dont update position a,b, 
        bw[obs_a][obs_b]=(bw[obs_a][obs_b]+clear)/2

        obs_ar,obs_br,_ = set_axis(obs_a,obs_b,compass,6) #right
        bw[obs_br][obs_ar]=(bw[obs_br][obs_ar]+clear)/2

        obs_al,obs_bl,_ = set_axis(obs_a,obs_b,compass,7) #left
        bw[obs_bl][obs_al]=(bw[obs_bl][obs_al]+clear)/2

        obs_ard,obs_brd,_ = set_axis(obs_ar,obs_br,compass,1) #right diagonal
        bw[obs_brd][obs_ard]=(bw[obs_brd][obs_ard]+clear)/2

        obs_ald,obs_bld,_ = set_axis(obs_al,obs_bl,compass,1) #left diagonal
        bw[obs_bld][obs_ald]=(bw[obs_bld][obs_ald]+obstacle)/2
        
    bw[obs_b][obs_a]=obstacle #bw[y][x]
    #around obstacle likely obstacle
    obs_ar,obs_br,_ = set_axis(obs_a,obs_b,compass,6) #right
    bw[obs_br][obs_ar]=(bw[obs_br][obs_ar]+obstacle)/2

    obs_al,obs_bl,_ = set_axis(obs_a,obs_b,compass,7) #left
    bw[obs_bl][obs_al]=(bw[obs_bl][obs_al]+obstacle)/2

    obs_ard,obs_brd,_ = set_axis(obs_ar,obs_br,compass,1) #right diagonal
    bw[obs_brd][obs_ard]=(bw[obs_brd][obs_ard]+obstacle)/2

    obs_ald,obs_bld,_ = set_axis(obs_al,obs_bl,compass,1) #left diagonal
    bw[obs_bld][obs_ald]=(bw[obs_bld][obs_ald]+obstacle)/2

    obs_af,obs_bf,_ = set_axis(obs_a,obs_b,compass,1) #forward
    bw[obs_bf][obs_af]=(bw[obs_bf][obs_af]+obstacle)/2

    a,b, compass= set_axis(a,b,compass,l2[count])   
    print(a,b,compass, num, l2[count]) 
    bw[b][a]=clear #bw[y][x]

    al,bl,ar,br=body(a,b,compass)
    if(bw[bl][al]!=clear):
      bw[bl][al]=(bw[bl][al]*0.2+clear*0.8)
    if(bw[br][ar]!=clear):
      bw[br][ar]=(bw[br][ar]*0.2+clear*0.8)

  fig = plt.figure()
  ax = fig.gca(projection='3d')

  # Make data.
  X = np.arange(-mid, mid+1)
  Y = np.arange(-mid, mid+1)
  print(len(X))
  X, Y = np.meshgrid(X, Y)
  Z =np.array(bw)
  print(Z)
  print(len(Z))

  # Plot the surface.
  surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)

  # Customize the z axis.
  ax.set_zlim(-1.01, 1.01)
  ax.zaxis.set_major_locator(LinearLocator(10))
  ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

  # Add a color bar which maps values to colors.
  fig.colorbar(surf, aspect=10, label='Probability of obstacle')
 
  plt.show()


def set_axis(a,b,compass, step):
  if(compass==1): #north
     if(step==6): #right
         a,b=pos_x(a,b,1)
         compass=3 #east
     elif(step==7): #left
         a,b=neg_x(a,b,1)
         compass=4 #west
     elif(step==8): #backward
          a,b=neg_y(a,b,6)
     else:
         a,b=pos_y(a,b,step) 

  elif(compass==2): #south
     if(step==6): #right
         a,b=neg_x(a,b,1)
         compass=4 #west
     elif(step==7): #left
         a,b=pos_x(a,b,1)
         compass=3 #east
     elif(step==8): #backward
        a,b=pos_y(a,b,6)
     else:
         a,b=neg_y(a,b,step) 

  elif(compass==3): #east
     if(step==6): #right
         a,b=neg_y(a,b,1)
         compass=2 #south
     elif(step==7): #left
         a,b=pos_y(a,b,1)
         compass=1 #north
     elif(step==8): #backward
         a,b=neg_x(a,b,6)
     else:
         a,b=pos_x(a,b,step) 

  elif(compass==4): #west
     if(step==8): #backward
         a,b=pos_x(a,b,2)
     elif(step==6): #right
         a,b=pos_y(a,b,1)
         compass=1 #north
     elif(step==7): #left
         a,b=neg_y(a,b,1)
         compass=2 #south
     else:
         a,b=neg_x(a,b,6) 

  return a,b,compass

def pos_y(a,b, colour):
  b=b-1
  return a,b

def neg_y(a,b, colour):
  b=b+1
  return a,b

def pos_x(a,b, colour):
  a=a+1
  return a,b

def neg_x(a,b, colour):
  a=a-1
  return a,b

def body(a,b,compass):
  if(compass==1): #nsew
     al=a-1
     ar=a+1
     return al,b,ar,b
  elif(compass==2):
     al=a+1
     ar=a+1
     return al,b,ar,b
  elif(compass==3):
     bl=b+1
     br=b-1
     return a,bl,a,br
  elif(compass==4):
     bl=b-1
     br=b+1
     return a,bl,a,br

if __name__ == '__main__':
      main()
