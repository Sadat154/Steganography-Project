import cv2
import numpy as np
from PIL import Image
DELIMITER = ''
class DCTSteg:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.height, self.width, self.channels = self.image.shape

    def dct(self, block): #Converts image into the frequency domain
        return cv2.dct(block.astype(np.float32))

    def idct(self, block):
        return cv2.idct(block.astype(np.float32))

    def message_to_bin(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message

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
    def adjust_height(self, file):
        pass

    def embed_message(self, message, bit_position):
        message_bits = self.message_to_bin(message) + DELIMITER

        # Check if message can fit in the image
        if len(message_bits) > (self.height * self.width * 3 - 1):
            raise ValueError("Message is too large to embed in image.")


        message_index = 0
        for y in range(0, self.height, 8):
            for x in range(0, self.width, 8):
                block = self.image[y:y + 8, x:x + 8]
                dct_block = self.dct(block)

                # Modify chosen bit of top-left coefficient (Y channel)
                if message_index < len(message_bits):
                    mask = 1 << (bit_position - 1)  # Create mask for chosen bit
                    dct_block[0, 0] = (dct_block[0, 0] & ~mask) | (int(message_bits[message_index]) << (bit_position - 1))
                    message_index += 1

                # Apply inverse DCT and update image block
                updated_block = self.idct(dct_block)
                self.image[y:y + 8, x:x + 8] = np.clip(updated_block, 0, 255).astype(np.uint8)

    def dct(self, block):
        if block.dtype != np.float32:
            block = block.astype(np.float32)
        return cv2.dct(block)

    def extract_message(self, bit_position):
        message_bits = []
        for y in range(0, self.height, 8):
            for x in range(0, self.width, 8):
                block = self.image[y:y + 8, x:x + 8]
                dct_block = self.dct(block)

                # Extract chosen bit from coefficient (Y channel)
                mask = 1 << (bit_position - 1)  # Create mask for chosen bit
                message_bits.append(str((dct_block[0, 0] & mask) >> (bit_position - 1)))

        # Convert binary string to characters
        message = ''.join(chr(int(chunk, 2)) for chunk in zip(*[iter(message_bits)] * 8))
        return message.rstrip('\0')  # Remove trailing null characters

    def save_stego_image(self, path):
        cv2.imwrite(path, self.image)


# Example usage
image_path = "C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/Jpeg_test.jpg"
steg = DCTSteg(image_path)

# Choose bit position to modify (1-8)
bit_position = int(input("Enter bit position to modify (1-8): "))

# Embed message
secret_message = "This is a secret message"
steg.embed_message(secret_message, bit_position)

# Save the stego image
stego_image_path = "C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub12.png"
steg.save_stego_image(stego_image_path)

# Extract message from stego image (optional)
extracted_message = steg.extract_message(bit_position)
print("Extracted message:", extracted_message)
