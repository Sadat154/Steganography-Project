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



def extract_message(image_path):
    image = Image.open(image_path)
    width, height = image.size

    binary_message = ''
    delimiter = '11111111'

    print(image.getpixel((1,1)))


# original_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/Kung_fu_panda.png"
# output_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/LSB_Algo/LSB_images/output_img_testing.png"

original_path = "N:/Github/Steganography-Project/Kung_fu_panda.png"
output_path = "N:/Github/Steganography-Project/LSB_Algo/LSB_images/hidden.png"

message = "Ligma balls"


# hide_message(original_path,message,output_path)
extract_message(output_path)







