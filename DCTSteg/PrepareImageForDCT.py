from PIL import Image
import numpy as np
from scipy.fftpack import dct, idct

class DCTSteganography:
    def __init__(self, cover_image_path):
        self.cover_image = Image.open(cover_image_path)
        self.cover_array = np.array(self.cover_image)
        self.quantization_table = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                            [12, 12, 14, 19, 26, 58, 60, 55],
                                            [14, 13, 16, 24, 40, 57, 69, 56],
                                            [14, 17, 22, 29, 51, 87, 80, 62],
                                            [18, 22, 37, 56, 68, 109, 103, 77],
                                            [24, 35, 55, 64, 81, 104, 113, 92],
                                            [49, 64, 78, 87, 103, 121, 120, 101],
                                            [72, 92, 95, 98, 112, 100, 103, 99]])

    def preprocess_image(self):
        height, width = self.cover_array.shape[:2]
        new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
        new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

        # Resize image to a multiple of 8
        resized_image = Image.new('RGB', (new_width, new_height), (0, 0, 0))
        resized_image.paste(self.cover_image, (0, 0))
        self.cover_array = np.array(resized_image)

    def dct_transform(self):
        return dct(dct(self.cover_array, axis=0, norm='ortho'), axis=1, norm='ortho')

    def idct_transform(self, dct_array):
        return idct(idct(dct_array, axis=0, norm='ortho'), axis=1, norm='ortho')

    def hide_message(self, message, output_path):
        self.preprocess_image()
        dct_array = self.dct_transform()

        message_bin = ''.join(format(ord(char), '08b') for char in message)
        message_bin += '1111111111111110'  # Add a delimiter to mark the end of the message

        flat_dct = (dct_array * 255).astype(int).flatten()  # Convert DCT coefficients to integers
        index = 0

        for i in range(min(len(flat_dct), len(message_bin))):
            row, col = i // 8, i % 8
            flat_dct[i] = (flat_dct[i] // self.quantization_table[row, col]) * self.quantization_table[row, col] + int(message_bin[i])

        stego_dct_array = (flat_dct.reshape(dct_array.shape) / 255.0).astype(np.float32)
        stego_image_array = self.idct_transform(stego_dct_array)

        stego_image = Image.fromarray(np.clip(stego_image_array, 0, 255).astype(np.uint8))
        stego_image.save(output_path)

    def reveal_message(self, stego_image_path):
        stego_image = Image.open(stego_image_path)
        stego_array = np.array(stego_image)

        stego_dct_array = self.dct_transform()
        flat_stego_dct = (stego_dct_array * 255).astype(int).flatten()  # Convert DCT coefficients to integers

        binary_message = ''
        delimiter_found = False

        for i in range(min(len(flat_stego_dct), 8 * 8)):
            row, col = i // 8, i % 8
            flat_stego_dct[i] = (flat_stego_dct[i] // self.quantization_table[row, col]) * self.quantization_table[row, col]

            binary_message += str(flat_stego_dct[i] & 1)
            if binary_message[-16:] == '1111111111111110':  # Check for the delimiter
                delimiter_found = True
                break

        if delimiter_found:
            # Extract the message until the delimiter is found
            message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message)-16, 8)])
            return message
        else:
            print("Delimiter not found. No hidden message.")
            return None

# Updated variable values
cover_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'
stego_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub23442272.png'
secret_message = 'abkjhkjhhj'

# Hide message
dct_steganography = DCTSteganography(cover_image_path)
dct_steganography.hide_message(secret_message, stego_image_path)

# Reveal message
revealed_message = dct_steganography.reveal_message(stego_image_path)
print("Revealed Message:", revealed_message)
