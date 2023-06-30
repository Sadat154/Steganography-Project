from PIL import Image

def hide_message(image_path, message):
    image = Image.open(image_path)
    width, height = image.size
    pixel_map = image.load()

    binary_message = ''.join(format(ord(char), '08b') for char in message)

    if len(binary_message) > width * height:
        raise ValueError("Message is too long to be hidden in the image.")

    bit_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixel_map[x, y]

            if bit_index < len(binary_message):
                r = (r & 0xFE) | int(binary_message[bit_index])
                bit_index += 1

            pixel_map[x, y] = (r, g, b)

    output_image_path = 'stego_image.png'
    image.save(output_image_path)
    print("Message hidden successfully in the image.")

def extract_message(image_path):
    image = Image.open(image_path)
    width, height = image.size
    pixel_map = image.load()

    extracted_message = []
    bit_index = 0
    binary_message = ''

    for y in range(height):
        for x in range(width):
            r, _, _ = pixel_map[x, y]
            binary_message += str(r & 0x01)
            bit_index += 1

            if bit_index % 8 == 0:
                extracted_message.append(binary_message)
                binary_message = ''

    message = ''.join(chr(int(binary, 2)) for binary in extracted_message)

    return message


# Example usage:
image_path = 'Zilla.jpeg'
message = "The person reading this is homosexual"

# Hide the message in the image
# hide_message(image_path, message)

# Extract the hidden message from the stego image
extracted_message = extract_message('stego_image.png')
# print("Extracted Message:", extracted_message)
