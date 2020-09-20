# importing the required module 
import matplotlib.pyplot as plt
import math
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

a=1
b=1
compass=1 #n,s,e,w

def palette(x,y, colour):
  if(colour==1): #flat ground/right/left
    plt.plot(x, y, color='black')
  elif(colour==2): #up stair
    plt.plot(x, y, color='plum')
  elif(colour==3): #up slope
    plt.plot(x, y, color='green')
  elif(colour==4): #down stair
    plt.plot(x, y, color='yellow')
  elif(colour==5): #down slope
    plt.plot(x, y, color='cyan')
  elif(colour==6): #backward
    plt.plot(x, y, color='red', linewidth=1)

def pos_y(a,b, colour):
  #forward
  x=[]
  y=[]
  x.append(a)
  y.append(b)
  b=b+1
  x.append(a)
  y.append(b)
  print(x,y)
  palette(x,y,colour)
  return a,b

def neg_y(a,b, colour):
  #backward
  x=[]
  y=[]
  x.append(a)
  y.append(b)
  b=b-1
  x.append(a)
  y.append(b)
  print(x,y)
  palette(x,y,colour)
  return a,b

def pos_x(a,b, colour):
  #right
  x=[]
  y=[]
  x.append(a)
  y.append(b)
  a=a+1
  x.append(a)
  y.append(b)
  print(x,y)
  palette(x,y,colour)
  return a,b

def neg_x(a,b, colour):
  #left
  x=[]
  y=[]
  x.append(a)
  y.append(b)
  a=a-1
  x.append(a)
  y.append(b)
  print(x,y)
  palette(x,y,colour)
  return a,b

def main():
  global a
  global b
  global compass
  plt.text(a,b,'start')
  
  for decision in l1:
    a,b, compass= set_axis(a,b,compass,int(decision))

  plt.text(a,b,'end')

  # naming the x axis 
  plt.xlabel('X (1 unit=1 step)') 
  # naming the y axis 
  plt.ylabel('Y (1 unit=1 step)') 
    
  # giving a title to my graph 
  plt.title('Trajectory mapping') 
    
  #equal axis
  sq=math.ceil(max(a,b)/10)*10
  plt.axis([0,sq,0,sq])

  #label
  plt.plot(0, 0, color='black', label='Flat ground')
  plt.plot(0, 0, color='plum', label='Up stair')
  plt.plot(0, 0, color='green', label='Up slope')
  plt.plot(0, 0, color='yellow', label='Down stair')
  plt.plot(0, 0, color='cyan', label='Down slope')
  plt.plot(0, 0, color='red', label='Backwards')
  plt.legend()

  # function to show the plot 
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

if __name__ == '__main__':
    main()
