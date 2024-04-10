from PIL import Image

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def embed_message(original_image_path, final_image_path,message):
    img = Image.open(original_image_path)
    width, height = img.size
    binary_message = message_to_binary(message)
    message_length = len(binary_message)

    if message_length > width * height:
        raise ValueError("Message too long to embed in the image")


    data_index = 0
    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for i in range(3):  # iterating through RGB components
                if data_index < message_length:
                    print(pixel[i])
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    print(pixel[i])
                    data_index += 1

            img.putpixel((x, y), tuple(pixel))

            if data_index >= message_length:
                img.save(final_image_path)
                print("Message embedded successfully!")
                return

if __name__ == "__main__":
    image_path = 'TestingImage.jpg'
    output_path = 'TestingOutput3.png'
    message = "Hello World"
    embed_message(image_path, output_path,message)
