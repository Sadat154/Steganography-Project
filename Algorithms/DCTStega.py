import itertools
import cv2
import numpy as np
from PIL import Image


channels_dict = {"r": 0, "g": 1, "b": 2}


quantisation_table = np.array(
    [
        [16, 11, 10, 16, 24, 40, 51, 61,],  # Luminance (Y) Quantization Table (Standard Quality)
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99],
    ]
)


class DCTSteg:
    def __init__(self, image_path, secret_message, binary_message, channel):
        self.original_image = Image.open(image_path)
        self.height = self.original_image.size[1]
        self.width = self.original_image.size[0]
        self.channels = 3
        self.secret_message = secret_message
        self.binary_message = binary_message
        self.channel_to_modify = channels_dict[channel.lower()]
        self.__DELIM = "%$£QXT"

    def resize_image(self, img):
        height, width = self.height, self.width
        new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
        new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

        # Resize image to a multiple of 8
        resized_image = Image.new("RGB", (new_width, new_height), (0, 0, 0))
        resized_image.paste(img, (0, 0))

        return resized_image, new_height, new_width

    def adjust_bitmask(self, bitpos):

        bitchoice = bitpos + 1
        ans = 0
        for i in range(0, (8 - bitchoice)):
            logical_left_shift = 1 << (i)
            ans += logical_left_shift

        finalAns = 255 - ans

        return finalAns

    def check_message_length(self, height, width, message):
        if (width / 8) * (height / 8) < len(message):
            print("Error: Message too large to encode in image")
            return False

    def encode_image(self, bitpos):
        resized_img, row, column = self.resize_image(self.original_image)
        img = np.array(resized_img)

        print(((self.width / 8) * (self.height / 8)))

        # Hide message in the blue channel so we need to separate it
        current_channel = img[:, :, self.channel_to_modify]

        # Convert channel to type float 32 for dct function
        current_channel = np.float32(current_channel)

        # Need to split the channel into 8x8 blocks
        image_blocks = [
            np.round(current_channel[j : j + 8, i : i + 8] - 128)
            for (j, i) in itertools.product(range(0, row, 8), range(0, column, 8))
        ]

        # Run the 8x8 blocks through the DCT function
        dct_blocks = [np.round(cv2.dct(image_block)) for image_block in image_blocks]

        # Run the 8x8 blocks through the quantisation table
        quantised_blocks = [
            np.round(dct_block / quantisation_table) for dct_block in dct_blocks
        ]

        # Encoding a bit in the chosen bit
        message_index = 0
        for quantised_block in quantised_blocks:  # Iterate through the blocks
            DC_coeff = quantised_block[0][0]
            DC_coeff = np.uint8(DC_coeff)
            DC_coeff = np.unpackbits(DC_coeff)
            DC_coeff[bitpos] = self.binary_message[message_index]
            DC_coeff = np.packbits(DC_coeff)
            DC_coeff = np.float32(DC_coeff)
            DC_coeff = DC_coeff - self.adjust_bitmask(
                bitpos
            )  # value to be minused must be changed e.g., if bit pos = 7(8) we minus 255 if 6(7) we minus 254
            quantised_block[0][0] = DC_coeff
            message_index += 1
            if message_index == len(self.binary_message):
                break
        # Run the blocks inversely through the quantisation table
        updated_blocks = [
            quantised_block * quantisation_table + 128
            for quantised_block in quantised_blocks
        ]

        updated_channel = []

        for chunkRowBlocks in self.chunks(
            updated_blocks, column / 8
        ):  # For each 8 length-ed chunk
            for rowBlockNum in range(8):  # 0-7 to iterate through chunk
                for block in chunkRowBlocks:  # For each item in the chunk
                    updated_channel.extend(
                        block[rowBlockNum]
                    )  # Update the blue channel

        # Shape array into correct format such that it can be converted back into an image using PIL
        updated_channel = np.array(updated_channel).reshape(row, column)
        # Blue channel currently in float32 format, need to convert
        updated_channel = np.uint8(updated_channel)

        original_rows = self.height
        original_columns = self.width

        if self.channel_to_modify == 1:  # Green channel has been modified, rest same
            blue_img = Image.fromarray(img[:, :, 2][:original_rows, :original_columns])
            red_img = Image.fromarray(img[:, :, 0][:original_rows, :original_columns])
            green_img = Image.fromarray(
                updated_channel[:original_rows, :original_columns]
            )
        elif (
            self.channel_to_modify == 2
        ):  # Blue channel has been modified rest stay the same
            blue_img = Image.fromarray(
                updated_channel[:original_rows, :original_columns]
            )
            red_img = Image.fromarray(img[:, :, 0][:original_rows, :original_columns])
            green_img = Image.fromarray(img[:, :, 1][:original_rows, :original_columns])

        else:  # Red channel has been modified the rest stay the same
            blue_img = Image.fromarray(img[:, :, 2][:original_rows, :original_columns])
            red_img = Image.fromarray(
                updated_channel[:original_rows, :original_columns]
            )
            green_img = Image.fromarray(img[:, :, 1][:original_rows, :original_columns])

        final_img = Image.merge("RGB", (red_img, green_img, blue_img))
        # final_img.show()
        # final_img.save('C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/A_5_DCT.png')
        # Add code which saves final_img and encoding FINISHED!

    def decode_image(self, image_path, bit_pos):
        img = Image.open(image_path)
        img, row, column = self.resize_image(
            img
        )  # Row, Column remains unchanged, however image changes

        img = np.array(img)

        # Obtain blue channel as this was the channel that was modified
        blue_channel = img[:, :, 2]

        # Convert to float32 for dct function
        blue_channel = np.float32(blue_channel)

        # break into 8x8 blocks
        image_blocks = [
            blue_channel[j : j + 8, i : i + 8] - 128
            for (j, i) in itertools.product(range(0, row, 8), range(0, column, 8))
        ]

        # run 8x8 blocks through the quantisation table
        quantised_blocks = [
            image_block / quantisation_table for image_block in image_blocks
        ]

        dec_value = 0  # Will be used to store the decimal value of a character
        finalMsg = ""
        i = 0

        for quantised_block in quantised_blocks:
            DC_coeff = quantised_block[0][0]
            DC_coeff = np.uint8(DC_coeff)
            DC_coeff = np.unpackbits(DC_coeff)

            if DC_coeff[bit_pos] == 1:
                dec_value += (0 & 1) << (7 - i)

            elif DC_coeff[bit_pos] == 0:
                dec_value += (1 & 1) << (7 - i)
            i += 1
            if i == 8:
                finalMsg += chr(dec_value)
                i = 0
                dec_value = 0
                # Now we want to check if delimiter has been reached so that we can end the decoding process
                if self.__DELIM in finalMsg:
                    return finalMsg[: -(len(self.__DELIM))]

    def chunks(
        self, currentlist, n
    ):  # Takes a list and splits it into chunks of size n
        m = int(n)
        for i in range(0, len(currentlist), m):
            yield currentlist[i : i + m]


# BitChoice = 8 # 0 = MSB, 7 = LSB
