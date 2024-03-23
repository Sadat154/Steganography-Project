import math
import cv2
import numpy as numpy
from PIL import Image

Delim = '%$£QXT'
class BitEncoderDecoder:
    def __init__(self, original_image_path, encoded_image_path, bit_position):
        self.original_image = Image.open(original_image_path)
        self.encoded_image_path = encoded_image_path #Where the encoded image shall be stored
        self.bit_position = bit_position
        self.number_of_channels = 3


    def _message_to_bin(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message

    def encode_bit(self, secret_message):
        original_image = self.original_image
        secret_message += Delim # Delimiter to indicate end of message
        binary_message = self._message_to_bin(secret_message)
        if len(binary_message) > self.number_of_channels * original_image.size[0] * original_image.size[1]:
            raise ValueError("Message is too long to be encoded in the image")

        data_index = 0
        for y in range(original_image.size[1]):
            for x in range(original_image.size[0]):
                pixel = list(original_image.getpixel((x, y)))

                for i in range(self.number_of_channels):
                    if data_index < len(binary_message):
                        pixel[i] = pixel[i] & ~(1 << self.bit_position) | (int(binary_message[data_index]) << self.bit_position)
                        data_index += 1

                original_image.putpixel((x, y), tuple(pixel))

        original_image.save(self.encoded_image_path)

    def decode_bit(self):
        encoded_image = Image.open(self.encoded_image_path)

        binary_message = ''
        message_length = 0
        decoded_message = ''

        while decoded_message[-(len(Delim)):] != Delim:
            for y in range(encoded_image.size[1]):
                for x in range(encoded_image.size[0]):
                    pixel = list(encoded_image.getpixel((x, y)))

                    for i in range(3):
                        binary_message += str((pixel[i] >> self.bit_position) & 1)
                        decoded_message = ''.join(
                            [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)])
                        if Delim in decoded_message:
                            print(decoded_message)
                            break
                        message_length += 1

                    if Delim in decoded_message:
                        break

                if Delim in decoded_message:
                    break

            if Delim in decoded_message:
                break

            remaining_bits = message_length % 8
            if remaining_bits != 0:
                binary_message = binary_message[:-remaining_bits]

        return decoded_message[:-(len(Delim))]



original_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'


def _message_to_bin(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message
#
# def generate_bitsub_images(original_image_path):
#     Images = []
#     original_image = Image.open(original_image_path)
#     for i in range(0,8): #Bit
#         #Need to obtain maximum amount of characters available to be embedded into the image
#         max_chars = 3 * original_image.size[0] * original_image.size[1]
#
#         #For each bit, 4 images need to be produced
#         for j in range(1,5):
#             percentage = j/4
#             chars_to_be_embedded = 'a' * math.trunc((((percentage * max_chars)) / 8)-len(Delim)) # We divide by 8 to account for the binary
#             output_image_path = f'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub_bitpos[{8-(i)}]_{j/4*100}%.png'
#             ImageObj = BitEncoderDecoder(original_image_path,output_image_path,i)
#             ImageObj.encode_bit((chars_to_be_embedded))
#             Images.append(ImageObj)
#
# generate_bitsub_images(original_image_path)
#Need to use decode_bit to test that the code works properly
# 25%,50%,75%,100% - bit 1-8 so 4*8 = 32 images for one image. Ideal 3 images.

# x = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/IbrahimLikesKids.png'
# TEST = BitEncoderDecoder(original_image_path, x,7)


# secret_msg = 'ABC'
# output_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/ABCtest2.png'
#
# decTest = BitEncoderDecoder(original_image_path, output_path,0)
#
# decTest.encode_bit(secret_msg)
#
# print(decTest.decode_bit())

#REMINDER THE WAY MY CODE WORKS IF BIT POSITION = 0 THEN LSB IF =7 THEN MSB