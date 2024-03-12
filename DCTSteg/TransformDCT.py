import numpy as np
from PIL import Image

class DCTSteganography:
    def __init__(self, src_image_path):
        self.src_image = Image.open(src_image_path)
        self.width, self.height = self.src_image.size
        self.array = np.array(list(self.src_image.getdata()))
        self.mode = self.src_image.mode
        self.n = 3 if self.mode == 'RGB' else 4  # Number of color channels

    def encode_dct(self, message, dest_image_path):
        # Add a delimiter to the message
        message += "$t3g0"
        b_message = ''.join([format(ord(char), "08b") for char in message])
        req_pixels = len(b_message)

        # Check if enough pixels are available
        total_pixels = self.array.size // self.n
        if req_pixels > total_pixels:
            raise ValueError("Insufficient pixels for the secret message.")

        # Apply DCT to the image
        dct_array = np.zeros_like(self.array, dtype=float)
        for i in range(total_pixels):
            block = self.array[i].reshape(8, -1)  # Reshape to 8x8 or 8x4 based on color channels
            dct_block = np.round(np.fft.dct(block, norm="ortho"))
            dct_array[i] = dct_block.flatten()

        # Modify the DCT coefficients
        for i in range(req_pixels):
            dct_array[i] += int(b_message[i], 2)  # Add the message bits to DCT coefficients

        # Inverse DCT to reconstruct the stego-image
        stego_array = np.zeros_like(self.array)
        for i in range(total_pixels):
            stego_block = dct_array[i].reshape(8, -1)
            stego_block = np.round(np.fft.idct(stego_block, norm="ortho"))
            stego_array[i] = stego_block.flatten()

        # Create a new image with modified pixels
        encoded_image = Image.new(self.mode, (self.width, self.height))
        encoded_image.putdata([tuple(pixel) for pixel in stego_array])
        encoded_image.save(dest_image_path)
        print(f"Encoded image saved as {dest_image_path}")


source_image_path = "C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg"
secret_msg = "HELLO"
stego_image_path = "C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub312.png"

stego = DCTSteganography(source_image_path)
stego.encode_dct(secret_msg, stego_image_path)