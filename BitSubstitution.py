import time
#LSB DONE

from PIL import Image

def message_to_bin(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def encode_bit(original_image_path, secret_message, output_image_path, bit_position=0):
    # Open the original image
    original_image = Image.open(original_image_path)
    secret_message += Delim
    # Convert the secret message to binary
    binary_message = message_to_bin(secret_message)

    # Check if the message can be encoded in the image
    if len(binary_message) > 3 * original_image.size[0] * original_image.size[1]:
        raise ValueError("Message is too long to be encoded in the image")
    test = 1
    # Encode the message in the image
    data_index = 0
    for y in range(original_image.size[1]):
        for x in range(original_image.size[0]):
            pixel = list(original_image.getpixel((x, y)))

            # Replace the least significant bit with the message data
            for i in range(3):  # Iterate over RGB components
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~(1 << bit_position) | (int(binary_message[data_index]) << bit_position)
                    data_index += 1

            original_image.putpixel((x, y), tuple(pixel))

    # Save the encoded image
    original_image.save(output_image_path)

def decode_bit(encoded_image_path, bit_position=0):
    # Open the encoded image
    encoded_image = Image.open(encoded_image_path)

    # Extract the hidden message from the image
    binary_message = ''
    message_length = 0
    decoded_message = ''

    while decoded_message[-(len(Delim)):] != Delim:
        for y in range(encoded_image.size[1]):
            for x in range(encoded_image.size[0]):
                pixel = list(encoded_image.getpixel((x, y)))

                # Extract the least significant bit from each RGB component
                for i in range(3):
                    binary_message += str((pixel[i] >> bit_position) & 1)
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



        #Ensure that the extracted message is a multiple of 8 (one character)
        remaining_bits = message_length % 8
        if remaining_bits != 0:
            # Remove the extra bits to align to the nearest byte boundary
            binary_message = binary_message[:-remaining_bits]

        #Convert binary message to string

    return decoded_message[:-(len(Delim))]


# Example usage:

Delim = 'GZOHLUMXWRDTCQF'

original_image_path = 'C:/Users/Nafis/Documents/GitHub/Steganography-Project/cropped.jpg'
secret_message = 'abc'
output_image_path = 'C:/Users/Nafis/Documents/GitHub/Steganography-Project/BitSubResults/BitSub1.png'
bit_position_to_encode = 0 # 0 = LSB, 7 = MSB


# Encode the message
encode_bit(original_image_path, secret_message, output_image_path, bit_position_to_encode)

# Decode the message

decoded_message = decode_bit(output_image_path, bit_position_to_encode)

print("Decoded Message:", decoded_message)
