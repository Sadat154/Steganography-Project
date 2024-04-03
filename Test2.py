import cv2
import numpy as np


#Spatial domain = BIT Sub
#Transform domain techniquqe = DCT
secret_message = 'Hi'

binary_message = (','.join(format(ord(char), '08b') for char in secret_message)).split(',')

x = []
for char in binary_message:
    counter = 0
    for bin_letter in char:
        if bin_letter == '0':
            x.append(-1)
        else:
            x.append(1)

x = [x[i:i+8] for i in range(0, len(x), 8)] #Binary of the characters
print(x) #bi

#B,G,R for imread
#Image
current_image_array = cv2.imread('cropped.jpg') # Load image as an np array
height, width = current_image_array.shape[:2]
length_of_array = len(current_image_array)
# cv2.imshow('CurrImg', current_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#Now we want binary of the chosen channel, start off with red [a,b,2]

Counter = 0
red_cmp = []
for row in range(height):
    temp = []
    for col in range(width):
        temp.append(current_image_array[row,col,2])
        Counter += 1

        if Counter == width: #first row completed
            red_cmp.append(temp)
            temp = []
            Counter = 0


#Now convert each pixel to binary
pixels_binary = []
for row in red_cmp:
    for pixel in row:
        pixel_to_binary = format(pixel, '08b')
        pixel_to_binary = [int(x) for x in pixel_to_binary]
        pixels_binary.append(pixel_to_binary)

print(pixels_binary) #b

key1 = '123'
key1 =[int(x) for x in key1]





