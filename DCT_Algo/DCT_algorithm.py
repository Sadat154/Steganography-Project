import numpy as np
from PIL import Image

def dct_2d(block):
    return np.fft.fftshift(np.fft.dct(np.fft.dct(block.T, norm='ortho').T, norm='ortho'))

def idct_2d(block):
    return np.fft.idct(np.fft.idct(np.fft.ifftshift(block.T).T, norm='ortho'), norm='ortho')

def hide_message(image_path, message, output_path):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size

    # Convert the message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in message)

    # Calculate the maximum message length that can be hidden
    max_message_length = (width * height * 3) // 8

    # Check if the message is too large to fit in the image
    if len(binary_message) > max_message_length:
        raise ValueError("Message is too large to be hidden in the image.")

    # Convert the image to a numpy array
    image_array = np.array(image)

    # Convert the image array to floating point
    image_array = image_array.astype(float)

    # Perform DCT on each 8x8 block of the image
    block_index = 0
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            # Get the 8x8 block
            block = image_array[y:y+8, x:x+8]

            # Perform DCT on the block
            dct_block = dct_2d(block)

            # Embed the message bits in the DC coefficient
            for i in range(3):
                if block_index < len(binary_message):
                    bit = int(binary_message[block_index])
                    if bit == 0:
                        dct_block[0, 0, i] = abs(dct_block[0, 0, i])
                    else:
                        dct_block[0, 0, i] = -abs(dct_block[0, 0, i])
                    block_index += 1

            # Perform inverse DCT on the modified block
            modified_block = idct_2d(dct_block)

            # Update the original image array with the modified block
            image_array[y:y+8, x:x+8] = modified_block

    # Clip pixel values to the valid range (0-255)
    image_array = np.clip(image_array, 0, 255)

    # Convert the image array back to unsigned 8-bit integers
    image_array = image_array.astype(np.uint8)

    # Create a new image from the modified image array
    modified_image = Image.fromarray(image_array)

    # Save the modified image
    output_path = "N:/Github/Steganography-Project/DCT_Algo/DCT_images/" + output_path
    modified_image.save(output_path)

def extract_message(image_path):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size

    binary_message = ''

    # Convert the image to a numpy array
    image_array = np.array(image)

    # Convert the image array to floating point
    image_array = image_array.astype(float)

    # Extract the message bits from the DC coefficients
    block_index = 0
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            # Get the 8x8 block
            block = image_array[y:y+8, x:x+8]

            # Perform DCT on the block
            dct_block = dct_2d(block)

            # Extract the message bits from the DC coefficient
            for i in range(3):
                value = dct_block[0, 0, i]
                bit = 1 if value < 0 else 0
                binary_message += str(bit)
                block_index += 1

    # Convert binary message to ASCII
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message



def generate_stego_images():

    initial_image = "N://Github//Steganography-Project//Kung_fu_panda.png"
    for i in range(0,100,10):
        output_image = f"output_img_{i}.png"
        message = 'a'*i
        hide_message(initial_image, message, output_image)

    print("Image generation for the DCT algo completed")

generate_stego_images()

#    output_path = "N:/Github/Steganography-Project/DCT_Algo/DCT_images/" + output_path


# message = extract_message("N:\Github\Steganography-Project\DCT_Algo\DCT_images\output_img_200000.png")
# print(message)