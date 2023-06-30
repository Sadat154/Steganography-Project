from PIL import Image


def encode_message(image_path, message):
    image = Image.open(image_path)
    width, height = image.size
    max_chars = width * height * 3 // 8  # Maximum number of characters that can be encoded
    if len(message) > max_chars:
        raise ValueError("Message is too long to be encoded in the image.")

    binary_message = ''.join(format(ord(c), '08b') for c in message)  # Convert message to binary

    encoded_image = image.copy()
    index = 0  # Index for traversing the binary message

    # Iterate through each pixel and modify the least significant bit of each color channel
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            if index < len(binary_message):
                for i in range(3):
                    pixel[i] = pixel[i] & 0xFE | int(binary_message[index])
                    index += 1
            else:
                break
            encoded_image.putpixel((x, y), tuple(pixel))

    encoded_image.save("encoded_image.png")  # Save the encoded image


def decode_message(image_path):
    encoded_image = Image.open(image_path)
    width, height = encoded_image.size

    binary_message = ""

    # Iterate through each pixel and retrieve the least significant bit of each color channel
    for y in range(height):
        for x in range(width):
            pixel = list(encoded_image.getpixel((x, y)))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    decoded_message = ""

    # Convert binary message to ASCII characters
    for i in range(0, len(binary_message), 8):
        decoded_message += chr(int(binary_message[i:i + 8], 2))

    return decoded_message


# Example usage:
image_path = "cover_image.png"
message_to_encode = "This is a secret message!"

# Encode the message in the image
encode_message(image_path, message_to_encode)

# Decode the message from the encoded image
decoded_message = decode_message("encoded_image.png")
print("Decoded message:", decoded_message)
