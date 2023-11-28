from PIL import Image

def message_to_bin(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def encode_lsb(original_image_path, secret_message, output_image_path):
    # Open the original image
    original_image = Image.open(original_image_path)

    # Convert the secret message to binary
    binary_message = message_to_bin(secret_message)

    # Check if the message can be encoded in the image
    if len(binary_message) > 3 * original_image.size[0] * original_image.size[1]:
        raise ValueError("Message is too long to be encoded in the image")

    # Encode the message in the image
    data_index = 0
    for y in range(original_image.size[1]):
        for x in range(original_image.size[0]):
            pixel = list(original_image.getpixel((x, y)))

            # Replace the least significant bit with the message data
            for i in range(3):  # Iterate over RGB components
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1

            original_image.putpixel((x, y), tuple(pixel))

    # Save the encoded image
    original_image.save(output_image_path + ".jpg")

def decode_lsb(encoded_image_path):
    # Open the encoded image
    encoded_image = Image.open(encoded_image_path)

    # Extract the hidden message from the image
    binary_message = ''
    for y in range(encoded_image.size[1]):
        for x in range(encoded_image.size[0]):
            pixel = list(encoded_image.getpixel((x, y)))

            # Extract the least significant bit from each RGB component
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    # Convert binary message to string
    decoded_message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])

    return decoded_message

# Example usage:
original_image_path = 'C:/Users/naf15/Downloads/12x12.jpg'
secret_message = 'Hello, this is a secret message!'
output_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/Bit-8/helpMe'

# Encode the message
encode_lsb(original_image_path, secret_message, output_image_path)


# Decode the message
decoded_message = decode_lsb(output_image_path+".JPG")
print("Decoded Message:", decoded_message)
