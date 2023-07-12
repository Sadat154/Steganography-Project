from PIL import Image

def hide_message(image_path, message, output_path):
    image = Image.open(image_path)
    width, height = image.size

    # Convert the message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in message)

    # Check if the message is too large to fit in the image
    max_message_length = width * height * 3  # Each pixel has RGB channels
    if len(binary_message) > max_message_length:
        raise ValueError("Message is too large to be hidden in the image.")

    # Add a delimiter to mark the end of the message
    binary_message += '1111111111111110'  # Using 16 bits as the delimiter

    index = 0  # Current bit index in the binary message

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))

            # Modify the least significant bit of each color channel
            for i in range(3):
                if index < len(binary_message):
                    pixel[i] = pixel[i] & 0xFE | int(binary_message[index])
                    index += 1

            image.putpixel((x, y), tuple(pixel))

    # Save the modified image
    output_path = "N:/Github/Steganography-Project/LSB_Algo/LSB_images/" + output_path
    image.save(output_path)

def extract_message(image_path):
    image = Image.open(image_path)
    width, height = image.size

    binary_message = ''
    delimiter = '1111111111111110'

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))

            # Extract the least significant bit from each color channel
            for i in range(3):
                binary_message += str(pixel[i] & 1)

                # Check if the delimiter is reached
                if binary_message[-16:] == delimiter:
                    # Remove the delimiter and convert binary to ASCII
                    binary_message = binary_message[:-16]
                    message = ''
                    for i in range(0, len(binary_message), 8):
                        byte = binary_message[i:i+8]
                        message += chr(int(byte, 2))
                    return message

    return None



# Hide a message in an image

def generate_stego_images():

    initial_image = "N://Github//Steganography-Project//Kung_fu_panda1.png"
    for i in range(0,1000000,100000):
        output_image = f"output_img_{i}.png"
        message = 'a'*i
        hide_message(initial_image, message, output_image)

    print("Image generation for the LSB algo completed")

generate_stego_images()


# message = extract_message("N:\Github\Steganography-Project\LSB_Algo\LSB_images\output_img_81000.png")
# print(message)
#

# Extract the hidden message from an image
# message = extract_message("output_image.png")
# print("Extracted message:", message)

