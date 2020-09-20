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

sq=2*len(l1)+1 #so it is odd
mid=math.floor(sq/2)
#print(sq, mid)

obstacle=1 #prob of obstacle ----1/3
clear= 0
unsure=0.5
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
      
  for decision in l1:
    decision=int(decision)
    if(decision==6):
      #obstacle is infront of current step
      obs_a,obs_b,_ =set_axis(a,b,compass,1) #we dont update position a,b, compass
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

      a,b,_=set_axis(a,b,compass,8) #go back one step

    a,b, compass= set_axis(a,b,compass,int(decision))   
    print(a,b,compass, decision) 
    bw[b][a]=clear #bw[y][x]

    al,bl,ar,br=body(a,b,compass)
    if(bw[bl][al]!=clear):
      bw[bl][al]=(bw[bl][al]*0.2+clear*0.8)
    if(bw[br][ar]!=clear):
      bw[br][ar]=(bw[br][ar]*0.2+clear*0.8)

  #plot
  ax = plt.gca()
#  im = ax.imshow(bw, cmap='gray') #dark to light bar - prob of white space -----2/3
  im = ax.imshow(bw, cmap='Greys') #light to dark bar- prob of obstacle

  #bar
  cbar = ax.figure.colorbar(im, ax=ax)  
 # cbar.ax.set_ylabel('Probability of no obstacle', rotation=-90, va="bottom") #---3/3
  cbar.ax.set_ylabel('Probability of obstacle', rotation=-90, va="bottom") 
  
  #graph axis
  col_labels=[]
  row_labels=[]
  for i in range(0,sq): #initialize
    col_labels.append(i)
    row_labels.append(i)
  ax.set_xticks(col_labels)
  ax.set_yticks(row_labels)
  for offset, count in enumerate(range(0,mid+1)): #number starting from center
    col_labels[mid+offset]=count
    col_labels[mid-offset]=count
    row_labels[mid+offset]=count
    row_labels[mid-offset]=count
 # print(col_labels)
 # print(row_labels)  
  ax.set_xticklabels(col_labels)
  ax.set_yticklabels(row_labels)
  ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)

  #start
  plt.plot(mid,mid,marker='*', color='blue', markersize='10')
  ax.annotate('start',(mid+1,mid), color='blue')
  plt.plot(a,b,marker='*', color='red', markersize='10')
  ax.annotate('end',(a+1,b),color='red')
 # x=[1.5,2.5]
 # y=[1.5,2.5]
 # plt.plot(x,y,color='red', label='hi')
 
#  plt.legend() 
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
