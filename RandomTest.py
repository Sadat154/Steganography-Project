import cv2
import numpy as np

g = 'Hi'
le=len(g)
i=0
a=list();
for i in range(le):
   a.append(0)  #initializing
j=0
for i in g:
    a[j]=ord(i)
    j+=1
print(a)  #ascii values
bi= [ [ 0 for i in range(8) ] for j in range(le) ]
j=0
i=7
while(j<le):
    while(i>-1):
        bi[j][i]=a[j]%2
        a[j]=(a[j]-bi[j][i])//2
        i-=1
    j+=1
    i=7
print("binary",bi)

i=0
j=0
while(j<le):
   while(i<8):
      if bi[j][i]==0:
         bi[j][i]=-1
      i+=1
   j+=1
   i=0
i=0
j=0
print('-1 conv',bi)#this is where 0s are converted to -1s

#image
grap = cv2.imread("cropped.jpg")
#grep = grap.load()
leng=len(grap)
b= [ [ 0 for i in range(8) ] for j in range(leng) ]
while(j<leng):
    while(i<8):
       b[j][i]=grap[j,i,2]
       i+=1
    j+=1
    i=0
print(b) #pixel values
print(len(b))


#Issues with the above code is that it currently only considers the red channel,
# and only the first 8 pixels of each row

Bi= [ [ 0 for i in range(8) ] for j in range(leng*8) ]
j=0
i=7
k=0
while(j<leng):
   while(k<8):
       while(i>-1):
          if j>0:
              Bi[k+(8*j)][i]=b[j][k]%2
              b[j][k]=(b[j][k]-  Bi[k+(8*j)][i])//2
          else:
              Bi[k][i]=b[j][k]%2
              b[j][k]=(b[j][k]-  Bi[k][i])//2
          i-=1
       k+=1
       i=7
   j+=1
   k=0
print(Bi)
#binary of pixel values;not displayed

key = '1234'
lenge=len(key)
o=list();
for i in range(lenge):
   o.append(0)  #initializing
j=0
for i in key:
    o[j]=int(i)
    j+=1
j=0
i=0
print(o)#key 1 displayed
while(j<le):
   for l in o:
      if i>7:
          i=0
      if j>0:
         Bi[l+(8*j)][7]=bi[j][i]
      else:
         Bi[l][7]=bi[j][i]
      i+=1
   j+=1
   i=0
print("lsb changed")
print(Bi)

