import pathlib
import BitSubStega
import DCTStega

from BitSubStega import BitEncoderDecoder

def message_to_binary(message):
    binary_message = "".join(format(ord(char), "08b") for char in message)
    return binary_message


def obtain_filepath():
    # Obtain file path of folder which contains all other pieces of code, images etc
    file_path = str(pathlib.Path(__file__).parent.resolve()).replace(
        "\\", "/"
    )  # replaces back slash with forward slash to make the string easier to deal with
    folder_slash_index = file_path.rfind("/")
    file_path = file_path[
        :folder_slash_index
    ]  # This is the file path where everything is contained

    return file_path


def generate_bitsub_images():
        image_names = ['','','']
        original_image = Image.open(original_image_path)
        for i in range(0,8): #Bit
            #Need to obtain maximum amount of characters available to be embedded into the image
            max_chars = 3 * original_image.size[0] * original_image.size[1]

            #For each bit, 4 images need to be produced
            for j in range(1,5):
                percentage = j/4
                chars_to_be_embedded = 'a' * math.trunc((((percentage * max_chars)) / 8)-len(Delim)) # We divide by 8 to account for the binary
                output_image_path = f'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub_bitpos[{8-(i)}]_{j/4*100}%.png'
                ImageObj = BitEncoderDecoder(original_image_path,output_image_path,i)
                ImageObj.encode_bit((chars_to_be_embedded))
                Images.append(ImageObj)
    pass


def main():
    pass
