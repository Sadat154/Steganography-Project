from PIL import Image


def hide_message(original_path, message, output_path):
    #image dimensions
    image = Image.open(original_path)
    width, height = image.size

    #message in binary form
    binary_message = ''.join(format(ord(character), '08b') for character in message)

    #max number of characters
    max_len = width * height * 3 # Resolution * 3 cos RGB (3 characters can be stored per pixel)


    if len(message) > max_len:
        raise ValueError ("Message size too large!")

    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y))) # get the decimal of every pixel in [R,G,B] format

            #Modify LSB of every colour channel
            for index in range(3):
                pixel[index] = pixel[index] & 0xFE | int(binary_message[index]) # 0xFE in binary is "11111110", the use of & converts LSB to 0, then





original_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/Kung_fu_panda.png"
output_path = "C:/Users/Nafis/Documents/GitHub/Steganography-Project/LSB_Algo/LSB_images/output_img_testing.png"
message = "Ligma balls"

hide_message(original_path,message,output_path)








