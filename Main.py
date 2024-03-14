DELIMITER = '%$£QXT'

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message







secret_message = input("Enter the message you would like to hide within the image: ")
bit_position = int(input("Which Bit position of the pixels in the image would you like to modify (1-8): "))