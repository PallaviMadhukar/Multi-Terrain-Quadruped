# importing the required module 
import matplotlib.pyplot as plt
f= open("mapping_text.txt","r")
string=str(f.read())
string=(string.strip()).split("\n")
f.close()

l=[]
for i in string:
    l.append(i.split(" "))
print(l)

a=1
b=1
compass=1 #n,s,e,w

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
  if(colour==1): #flat ground, backward, up slope, down slope, up stair, down stair
    plt.plot(x, y, color='black')
  elif(colour==2):
    plt.plot(x, y, color='red', linewidth=1)
  elif(colour==3): 
    plt.plot(x, y, color='green')
  elif(colour==4):
    plt.plot(x, y, color='yellow')
  elif(colour==5):
    plt.plot(x, y, color='cyan')
  elif(colour==6): 
    plt.plot(x, y, color='plum')
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
  if(colour==1): #black
    plt.plot(x, y, color='black')
  elif(colour==2): #red
    plt.plot(x, y, color='red', linewidth=1)
  elif(colour==3): 
    plt.plot(x, y, color='green')
  elif(colour==4):
    plt.plot(x, y, color='yellow')
  elif(colour==5):
    plt.plot(x, y, color='cyan')
  elif(colour==6): 
    plt.plot(x, y, color='plum')
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
  if(colour==1): #black
    plt.plot(x, y, color='black')
  elif(colour==2): #red
    plt.plot(x, y, color='red', linewidth=1)
  elif(colour==3): 
    plt.plot(x, y, color='green')
  elif(colour==4):
    plt.plot(x, y, color='yellow')
  elif(colour==5):
    plt.plot(x, y, color='cyan')
  elif(colour==6): 
    plt.plot(x, y, color='plum')
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
  if(colour==1): #flat ground
    plt.plot(x, y, color='black') #colour palette is on useful links
  elif(colour==2): #back
    plt.plot(x, y, color='red', linewidth=1)
  elif(colour==3): #upstair
    plt.plot(x, y, color='green')
  elif(colour==4):#downstair
    plt.plot(x, y, color='yellow')
  elif(colour==5): #upslope
    plt.plot(x, y, color='cyan')
  elif(colour==6): #downslope
    plt.plot(x, y, color='plum')
  return a,b

def main():
  l=string
  global a
  global b
  global compass
  plt.text(a,b,'start')
  
  for i in l:
    print(i[0])
    if i[1]=='1':
      a,b, compass= set_axis(a,b,compass,1)
    elif i[1]=='2':
      a,b, compass= set_axis(a,b,compass,2)
    elif i[1]=='3':
      a,b, compass= set_axis(a,b,compass,3)
    elif i[1]=='4':
      a,b, compass= set_axis(a,b,compass,4)
    elif i[1]=='5':
      a,b, compass= set_axis(a,b,compass,5)
    elif i[1]=='6':
      a,b, compass= set_axis(a,b,compass,6)

  '''
  a,b, compass= set_axis(a,b,compass,1) #1 forward(flat ground), 2 backward, 3 right, 4 left
  a,b, compass= set_axis(a,b,compass,1) #5 upstair, 6 downstair, 7 upslope, 8 downslope
  a,b, compass= set_axis(a,b,compass,2) 
  a,b, compass= set_axis(a,b,compass,3) 
  a,b, compass= set_axis(a,b,compass,1) 
  a,b, compass= set_axis(a,b,compass,3) 
'''

  plt.text(a,b,'end')

  # naming the x axis 
  plt.xlabel('x - axis') 
  # naming the y axis 
  plt.ylabel('y - axis') 
    
  # giving a title to my graph 
  plt.title('Robot mapping') 
    
  # function to show the plot 
  plt.show() 

def set_axis(a,b,compass, step):
  if(compass==1): #north
     if(step==1): #forward
         a,b=pos_y(a,b,1) 
     elif(step==2): #backward
         a,b=neg_y(a,b,2)
     elif(step==3): #right
         a,b=pos_x(a,b,1)
         compass=3 #east
     elif(step==4): #left
         a,b=neg_x(a,b,1)
         compass=4 #west
     elif(step==5): #upstair
         a,b=pos_y(a,b,3) 
     elif(step==6): #downstair
         a,b=pos_y(a,b,4) 
     elif(step==7): #upslope
         a,b=pos_y(a,b,5)
     elif(step==8): #downslope
         a,b=pos_y(a,b,6) 

  elif(compass==2): #south
     if(step==1): #forward
         a,b=neg_y(a,b,1)
     elif(step==2): #backward
         a,b=pos_y(a,b,2)
     elif(step==3): #right
         a,b=neg_x(a,b,1)
         compass=4 #west
     elif(step==4): #left
         a,b=pos_x(a,b,1)
         compass=3 #east
     elif(step==5): #upstair
         a,b=neg_y(a,b,3) 
     elif(step==6): #downstair
         a,b=neg_y(a,b,4) 
     elif(step==7): #upslope
         a,b=neg_y(a,b,5)
     elif(step==8): #downslope
         a,b=neg_y(a,b,6) 

  elif(compass==3): #east
     if(step==1): #forward
         a,b=pos_x(a,b,1)
     elif(step==2): #backward
         a,b=neg_x(a,b,2)
     elif(step==3): #right
         a,b=neg_y(a,b,1)
         compass=2 #south
     elif(step==4): #left
         a,b=pos_y(a,b,1)
         compass=1 #north
     elif(step==5): #upstair
         a,b=pos_x(a,b,3) 
     elif(step==6): #downstair
         a,b=pos_x(a,b,4) 
     elif(step==7): #upslope
         a,b=pos_x(a,b,5)
     elif(step==8): #downslope
         a,b=pos_x(a,b,6) 

  elif(compass==4): #west
     if(step==1): #forward
         a,b=neg_x(a,b,1)
     elif(step==2): #backward
         a,b=pos_x(a,b,2)
     elif(step==3): #right
         a,b=pos_y(a,b,1)
         compass=1 #north
     elif(step==4): #left
         a,b=neg_y(a,b,1)
         compass=2 #south
     elif(step==5): #upstair
         a,b=neg_x(a,b,3) 
     elif(step==6): #downstair
         a,b=neg_x(a,b,4) 
     elif(step==7): #upslope
         a,b=neg_x(a,b,5)
     elif(step==8): #downslope
         a,b=neg_x(a,b,6) 

  return a,b,compass

if __name__ == '__main__':
    main()

