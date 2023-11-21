###Try LSB Algo

from PIL import Image

def string_to_binary(message):
    return ''.join(format(ord(x), 'b') for x in message)

def binary_to_String(message):
    return ''.join(chr(int(x, 2)) for x in message.split())


def hide_message(message, imagepath, outputpath):
    #Open original image
    original_image = Image.open(imagepath)


    #Convert the message into binary
    binary_message = string_to_binary(message)
    print(binary_message)


    #Check if size of message is too large
    if len(binary_message) > 3 * original_image.size[0] * original_image.size[1]:
        raise ValueError("Message is too long to be encoded in the image")



    #Encode message into image now
    data_index = 0

    for height in range(original_image.size[1]):
        for width in range(original_image.size[0]):
            pixel = list(original_image.getpixel((width, height))) #Follows cartesian format (x,y)->(width,height): pixel[R, G, B]

            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1


    original_image.save(outputpath)










if __name__ == '__main__':
    message_to_hide = 'TEsting'
    image_path = 'C:/Users/naf15/Downloads/12x12.jpg'
    image_output_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/Bit-8/test'
    hide_message(message_to_hide, image_path, image_output_path)