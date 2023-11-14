###Try LSB Algo

from PIL import Image

def string_to_binary(message):
    return ' '.join(format(ord(x), 'b') for x in message)

def binary_to_String(message):
    return ''.join(chr(int(x, 2)) for x in message.split())


def hide_message(message, imagepath):
    #Open original image
    original_image = Image.open(imagepath)

    #Convert the message into binary
    binary_message = string_to_binary(message)

    #Check if size of message is too large
    if len(binary_message) > 3 * original_image.size[0] * original_image.size[1]:
        raise ValueError("Message is too long to be encoded in the image")


    #Encode message into image now




if __name__ == '__main__':
    message_to_hide = 'Testing 123 4 5 '
    image_path = 'C:/Users/naf15/Downloads/12x12.jpg'
    hide_message(message_to_hide, image_path)