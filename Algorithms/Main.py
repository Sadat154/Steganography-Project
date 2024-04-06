import math
import pathlib
import BitSubStega as BitSub
import DCTStega as DCT
from PIL import Image

DELIM = "%$£QXT"

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


def generate_bitsub_images(base_filepath, image_names):

        Bit_Images_List = []
        for img in image_names:
            current_image_path = f'{base_filepath}/OriginalImages/{img[0]}.{img[1]}'
            current_image = Image.open(current_image_path)

            for bit_position in range(0,8): #Bit
                #Need to obtain maximum amount of characters available to be embedded into the image
                max_chars = 3 * current_image.size[0] * current_image.size[1]

                #For each bit, 4 images need to be produced
                for j in range(1,5):
                    percentage = j/4
                    chars_to_be_embedded = 'a' * math.trunc((((percentage * max_chars)) / 8)) # We divide by 8 to account for the binary
                    chars_to_be_embedded = chars_to_be_embedded[:-len(DELIM)] #We need to account for the delimiter that will be added
                    output_image_path = f'{base_filepath}/ModifiedImages/BitSubModifiedImages/{img[0]}[{bit_position+1}]_{j/4*100}%.png'
                    ImageObj = BitSub.BitEncoderDecoder(current_image_path,output_image_path, chars_to_be_embedded, bit_position)
                    ImageObj.encode_bit()

                    Bit_Images_List.append(ImageObj)

        return Bit_Images_List #So we have a way to access all the image objects

def generate_dct_images(base_filepath, images_list):
    colour_channels = ['red','green','blue']
    DCT_Images_List = []

    for images in images_list:
        current_image_path = f'{base_filepath}/OriginalImages/{images[0]}.{images[1]}'
        current_image = Image.open(current_image_path)
        width, height = current_image.size[0], current_image.size[1]
        max_chars = (width / 8) * (height/8)

        for channel_choice in colour_channels:
            for bit_position in range(0,8):
                for j in range(1,5):
                    percentage = j/4
                    chars_to_be_embedded = 'a' * math.trunc((((percentage * max_chars)) / 8))  # We divide by 8 to account for the binary
                    chars_to_be_embedded = chars_to_be_embedded[:-len(DELIM)]  # We need to account for the delimiter that will be added
                    output_image_path = f'{base_filepath}/ModifiedImages/DCTModifiedImages/{images[0]}[{bit_position+1}]_{j/4*100}%_{channel_choice}.png'
                    ImageObj = DCT.DCTSteg(current_image_path, output_image_path, chars_to_be_embedded, bit_position, channel_choice[0])
                    ImageObj.encode_image()

                    DCT_Images_List.append(ImageObj)
                    return DCT_Images_List

def create_html_for_images(folder_path, num_images):
    # Create the HTML file
    html_filename = "StegImgResults.html"
    with open(html_filename, "w") as html_file:
        # Write the HTML header
        html_file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Image Gallery</title>\n</head>\n<body>\n")

        # Get a list of image files in the specified folder
        image_files = [filename for filename in pathlib.Path(folder_path).iterdir() if filename.suffix.lower() in (".jpg", ".png", ".gif")]

        # Limit the number of images to the specified count
        num_images = min(num_images, len(image_files))

        # Write image tags to the HTML file
        for i in range(num_images):
            image_path = image_files[i]
            html_file.write(f'<img src="{image_path}" alt="Image {i+1}">\n')

        # Write the HTML footer
        html_file.write("</body>\n</html>")

    print(f"HTML file '{html_filename}' created successfully!")


if __name__ == '__main__':
    base_filepath = obtain_filepath()
    image_names = [['Colourful','jpg'],['SimilarColours','jpg'],['GreyScale','webp']]
    #BitSub_Images = generate_bitsub_images(base_filepath, image_names)
    #DCT_Images = generate_dct_images(base_filepath, image_names)
    #Image generation complete