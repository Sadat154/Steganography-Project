import itertools
import cv2
import numpy as np
from PIL import Image




quantisation_table = np.array([[16,11,10,16,24,40,51,61],     # Luminance (Y) Quantization Table (Standard Quality)
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])
class DCTSteg:
    def __init__(self, image_path):
        self.original_image = Image.open(image_path)
        self.height = self.original_image.size[1]
        self.width = self.original_image.size[0]
        self.channels = 3 if self.original_image.mode == 'RGB' else 4 #Redundant, should be 3, if 4 then tell them to choose another image
        self.secret_message = '1'
        self.binary_message = ''


    def resize_image(self):
        height, width = self.height, self.width
        new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
        new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

        # Resize image to a multiple of 8
        resized_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
        resized_image.paste(self.original_image, (0, 0))


        return resized_image, new_height, new_width

    def check_message_length(self, height, width, message):
        if((width/8)*(height/8)<len(message)):
            print("Error: Message too large to encode in image")
            return False


    # def split_into_RGB(self,x,y):
    #     pixel = list(self.original_image.getpixel((x, y)))
    #     rPix = pixel[0]
    #     gPix = pixel[1]
    #     bPix = pixel[2]
    #
    #     #Need to make changes to the blue channel as human eye less likely to perceive changes made in blue channel
    #     return rPix,gPix,bPix
    #Above may be redundant


    def encode_image(self, bitpos):
        resized_img, row, column = self.resize_image()
        img = np.array(resized_img)


        #Hide message in the blue channel so we need to separate it
        blue_channel = img[:, :, 2]

        #Convert channel to type float 32 for dct function
        blue_channel = np.float32(blue_channel)

        #Need to split the channel into 8x8 blocks
        image_blocks = [np.round(blue_channel[j:j + 8, i:i + 8] - 128) for (j, i) in itertools.product(range(0, row, 8), range(0, column, 8))]


        #Run the 8x8 blocks through the DCT function
        dct_blocks = [np.round(cv2.dct(image_block)) for image_block in image_blocks]

        #Run the 8x8 blocks through the quantisation table
        quantised_blocks = [np.round(dct_block/quantisation_table) for dct_block in dct_blocks]

        #Encoding a bit in the chosen bit
        message_index = 0
        for quantised_block in quantised_blocks: #Iterate through the blocks
            Test = quantised_block[0][0]
            Test = np.uint8(Test)
            Test = np.unpackbits(Test)
            Test[bitpos] = self.secret_message[message_index]
            Test = np.packbits(Test)
            Test = np.float32(Test)
            Test = Test - 255
            quantised_block[0][0] = Test
            message_index += 1
            if message_index == len(self.secret_message):
                break
        #Run the blocks inversely through the quantisation table
        updated_blocks = [quantised_block * quantisation_table+128 for quantised_block in quantised_blocks]

        updated_blue_channel = []

        for chunkRowBlocks in self.chunks(updated_blocks, column/8): # For each 8 length-ed chunk
            for rowBlockNum in range(8): #0-7 to iterate through chunk
                for block in chunkRowBlocks: #For each item in the chunk
                    updated_blue_channel.extend(block[rowBlockNum]) #Update the blue channel

        #Shape array into correct format such that it can be converted back into an image using PIL
        updated_blue_channel = np.array(updated_blue_channel).reshape(row,column)
        #Blue channel currently in float32 format, need to convert
        updated_blue_channel = np.uint8(updated_blue_channel)

        original_rows = self.height
        original_columns = self.width

        blue_img = Image.fromarray(updated_blue_channel[:original_rows, :original_columns]) #
        red_img = Image.fromarray(img[:,:,0][:original_rows, :original_columns])
        green_img = Image.fromarray(img[:,:,1][:original_rows, :original_columns])

        final_img = Image.merge('RGB', (red_img, green_img, blue_img))
        #final_img.show()
        #Add code which saves final_img and encoding FINISHED!




    def chunks(self, currentlist, n): #Takes a list and splits it into chunks of size n
        m = int(n)
        for i in range(0, len(currentlist), m):
            yield currentlist[i:i + m]




path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'
test = DCTSteg(path)
BitChoice = 8 # 1 = MSB, 8 = LSB

test.encode_image(BitChoice-1)