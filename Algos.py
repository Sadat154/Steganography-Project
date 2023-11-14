###Try LSB Algo

from PIL import Image

def string_to_binary(message):
    return ' '.join(format(ord(x), 'b') for x in message)

def binary_to_String(message):
    return ''.join(chr(int(x, 2)) for x in message.split())



if __name__ == '__main__':
    message_to_hide = 'SHUSH'
    print(string_to_binary(message_to_hide))

    test = '1010011 1001000 1010101 1010011 1001000'
    print(binary_to_String(test))