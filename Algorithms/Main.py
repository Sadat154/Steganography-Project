import pathlib
DELIMITER = '%$£QXT'

def message_to_binary(message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message







#
# secret_message = input("Enter the message you would like to hide within the image: ")
# bit_position = int(input("Which Bit position of the pixels in the image would you like to modify (1-8): "))


#Obtain file path of folder which contains all other pieces of code, images etc
file_path = str(pathlib.Path(__file__).parent.resolve()).replace('\\','/') # replaces back slash with forward slash to make the string easier to deal with
folder_slash_index = file_path.rfind('/')
file_path = file_path[:folder_slash_index] #This is the file path where everything is contained
