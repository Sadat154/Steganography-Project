from PIL import Image


def hide_message(original_path, message, output_path):
    #Image dimensions
    image = Image.open(original_path)
    width, height = image.size

    #Message in binary form
    binary_message = ''.join(format(ord(character), '08b') for character in message)

    #Use of a delimiter makes it easier to extract the message from the stego image
    binary_message += '11111111'

    #Max number of characters
    max_len = width * height * 3 # Resolution * 3 cos RGB (3 bits can be stored per pixel)


    if len(binary_message) > max_len:
        raise ValueError ("Message size too large!")

    bit_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y))) #Get the decimal of every pixel in [R,G,B] format

            if bit_index == len(binary_message):
                break
            #Modify LSB of every colour channel
            for index in range(3):
                pixel[index] = pixel[index] & 0xFE | int(binary_message[bit_index]) #0xFE in binary is "11111110", the use of & converts LSB to 0, then the | makes the LSB same as the binary message
                bit_index += 1

            image.putpixel((x, y), tuple(pixel))

    image.save(output_path)


def show_lsb(image_path):
    image = Image.open(image_path).convert('RGB')
    width, height = image.size

    # Create a new image with a white background
    lsb_image = Image.new('RGB', (width, height), (255, 255, 255))

    # Iterate through each pixel and extract the LSB
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))

            # Extract the LSB from each color channel
            lsb_r = pixel[0] & 1
            lsb_g = pixel[1] & 1
            lsb_b = pixel[2] & 1

            # Set the pixel to black if the LSB is 0 (non-white)
            if lsb_r == 0 or lsb_g == 0 or lsb_b == 0:
                lsb_image.putpixel((x, y), (0, 0, 0))

    # Show the LSB image
    lsb_image.show()
def extract_message(image_path):
    image = Image.open(image_path)
    width, height = image.size

    binary_message = ''
    delimiter = '11111111'

    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x,y))

            for channel in range(3):
                binary_message += str(pixel[channel] & 1)

            if binary_message[-8:] == delimiter:
                binary_message = binary_message[:-8]
                message = ''
                for i in range(0,len(binary_message),8):
                    byte = binary_message[i:i+8]
                    message += chr(int(byte, 2))
                return message



def differences_in_images(original_path, stego_path):
    stego_image = Image.open(stego_path)
    width_stego, height_stego = stego_image.size

    original_image = Image.open(original_path)
    width_original, height_original = original_image.size


    for y in range(height_original):
        for x in range(width_original):
            pass


def generate_images():
    pass


original_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/Kung_fu_panda.png"
output_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/LSB_Algo/LSB_images/hidden.png"

# original_path = "N:/Github/Steganography-Project/Kung_fu_panda.png"
# output_path = "N:/Github/Steganography-Project/LSB_Algo/LSB_images/hidden.png"

message = "Ligma balls"


# hide_message(original_path,message,output_path)
# print(extract_message(output_path))

show_lsb(output_path)





