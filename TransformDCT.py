from PIL import Image
import numpy as np
import math

class DCTSteganography:
    def __init__(self, original_image_path, delim='GZOHLUMXWRDTCQF'):
        self.original_image_path = original_image_path
        self.delim = delim

    def _message_to_bin(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message

    def _block_dct(self, block):
        return np.round(np.dot(np.dot(self.transpose_matrix, block), self.dct_matrix) / 2)

    def _block_idct(self, block):
        return np.round(np.dot(np.dot(self.dct_matrix.T, block), self.transpose_matrix.T) / 2)

    def _encode_block(self, block, bit):
        # Modify the last coefficient of the block to encode one bit
        block[-1, -1] = math.floor(block[-1, -1] / 2) * 2 + int(bit)

    def _decode_block(self, block):
        # Retrieve the last bit from the last coefficient of the block
        return str(int(block[-1, -1]) % 2)

    def _process_image(self, process_function, bitstream):
        image = Image.open(self.original_image_path)
        width, height = image.size
        block_size = 8

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                block = np.array(image.crop((x, y, x + block_size, y + block_size)))
                processed_block = process_function(block, next(bitstream))
                image.paste(Image.fromarray(processed_block.astype(np.uint8)), (x, y))

        return image

    def encode_dct(self, secret_message, output_image_path):
        binary_message = self._message_to_bin(secret_message) + self.delim
        bitstream = iter(binary_message)

        self.dct_matrix = np.zeros((8, 8))
        self.transpose_matrix = np.zeros((8, 8))

        for i in range(8):
            for j in range(8):
                self.dct_matrix[i, j] = math.cos((2 * i + 1) * j * math.pi / 16)
                self.transpose_matrix[i, j] = self.dct_matrix[j, i]

        encoded_image = self._process_image(self._encode_block, bitstream)
        encoded_image.save(output_image_path)

    def decode_dct(self):
        bitstream = ''

        def decode_function(block):
            nonlocal bitstream
            bitstream += self._decode_block(block)

        self._process_image(decode_function, iter('1'))

        # Remove trailing delimiter
        bitstream = bitstream[:-(len(self.delim))]

        # Convert binary message to string
        decoded_message = ''.join([chr(int(bitstream[i:i + 8], 2)) for i in range(0, len(bitstream), 8)])
        return decoded_message


# Example usage:
original_image_path = 'path/to/original/image.jpg'
secret_message = 'Hello, this is a DCT steganography example!'
output_image_path = 'path/to/output/encoded_image_dct.png'

# Create an instance of the DCTSteganography class
dct_steganography = DCTSteganography(original_image_path)

# Encode the message using DCT steganography
dct_steganography.encode_dct(secret_message, output_image_path)

# Decode the message using DCT steganography
decoded_message = dct_steganography.decode_dct()
print("Decoded Message:", decoded_message)
