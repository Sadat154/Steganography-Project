from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import face
import cv2
import numpy as np


class DCTImage():
    def __init__(self, original_image_path, encoded_image_path, bit_position=0):
        self.original_image = Image.open(original_image_path)
        self.encoded_image_path = encoded_image_path  # Where the encoded image shall be stored
        self.bit_position = bit_position
        self.array = np.array(list(self.original_image.getdata())) # Creates an array of the RGB/RGBA of each pixel sequentially
        self.number_of_channels = 3 if self.original_image.mode == 'RGB' else 4
        self.raw_cover_image = cv2.imread(original_image_path, flags=cv2.IMREAD_COLOR)



    def DivideImageIntoBlocks(self):
        Blocks = []



        height, width = self.raw_cover_image.shape[:2]

        #Force image to be 8x8
        while width % 8 != 0:
            width += 1

        while height % 8 != 0:
            height += 1

        #Now we need to pad the image using cv2
        padded_image = cv2.resize(self.raw_cover_image, (width,height))
        data = Image.fromarray(padded_image)
        data.show()

        x = Image.open(padded_image)
        x.show()



original_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'
secret_message = 'abcDEF'
output_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub31.png'

test = DCTImage(original_image_path, output_image_path)

test.DivideImageIntoBlocks()