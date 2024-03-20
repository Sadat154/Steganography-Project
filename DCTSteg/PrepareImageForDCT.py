import cv2
import numpy as np
from PIL import Image

class DCTSteg:
    def __init__(self, image_path):
        self.original_image = Image.open(image_path)
        self.height = self.original_image.size[1]
        self.width = self.original_image.size[0]
        self.channels = 3 if self.original_image.mode == 'RGB' else 4 #Redundant, should be 3, if 4 then tell them to choose another image



    def resize_image(self):
        height, width = self.height, self.width
        new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
        new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

        # Resize image to a multiple of 8
        resized_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
        resized_image.paste(self.original_image, (0, 0))
        resized_image.show()

    def check_message_length(self, height, width, message):
        if((width/8)*(height/8)<len(message)):
            print("Error: Message too large to encode in image")
            return False


    def split_into_RGB(self,x,y):
        pixel = list(self.original_image.getpixel((x, y)))
        rPix = pixel[0]
        gPix = pixel[1]
        bPix = pixel[2]
        #Need to make changes to the blue channel as human eye less likely to perceive changes made in blue channel
        return rPix,gPix,bPix


    def encode_image(self):
        #blue_channel = b = img[:,:,0]


path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'
test = DCTSteg(path)
test.resize_image()