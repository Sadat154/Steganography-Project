import math
import os
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
        current_image_path = f"{base_filepath}/OriginalImages/{img[0]}.{img[1]}"
        current_image = Image.open(current_image_path)

        for bit_position in range(0, 8):  # Bit
            # Need to obtain maximum amount of characters available to be embedded into the image
            max_chars = 3 * current_image.size[0] * current_image.size[1]

            # For each bit, 4 images need to be produced
            for j in range(1, 5):
                percentage = j / 4
                chars_to_be_embedded = "a" * math.trunc(
                    (((percentage * max_chars)) / 8)
                )  # We divide by 8 to account for the binary
                chars_to_be_embedded = chars_to_be_embedded[
                    : -(len(DELIM)+1)
                ]  # We need to account for the delimiter that will be added
                output_image_path = f"{base_filepath}/ModifiedImages/BitSubModifiedImages/{j}_{img[0]}[{bit_position+1}]_{j/4*100}%.png"
                ImageObj = BitSub.BitSubEncoderDecoder(
                    pathlib.Path(current_image_path),
                    pathlib.Path(output_image_path),
                    chars_to_be_embedded,
                    bit_position,
                )
                ImageObj.encode_image()

                Bit_Images_List.append(ImageObj)

    return Bit_Images_List  # So we have a way to access all the image objects


def generate_dct_images(base_filepath, images_list):
    colour_channels = ["red", "green", "blue"]
    DCT_Images_List = []

    for images in images_list:
        current_image_path = f"{base_filepath}/OriginalImages/{images[0]}.{images[1]}"
        current_image = Image.open(current_image_path)
        width, height = current_image.size[0], current_image.size[1]
        max_chars = (width / 8) * (height / 8)


        for channel_choice in colour_channels:
            for bit_position in range(0, 8):
                for j in range(1, 5):
                    percentage = j / 4
                    chars_to_be_embedded = "a" * math.trunc(
                        (((percentage * max_chars)) / 8)
                    )  # We divide by 8 to account for the binary
                    chars_to_be_embedded = chars_to_be_embedded[
                        : -len(DELIM)
                    ]  # We need to account for the delimiter that will be added
                    output_image_path = f"{base_filepath}/ModifiedImages/DCTModifiedImages/{j}_{images[0]}[{bit_position+1}]_{j/4*100}%_{channel_choice}.png"
                    ImageObj = DCT.DCTSteg(
                        pathlib.Path(current_image_path),
                        pathlib.Path(output_image_path),
                        chars_to_be_embedded,
                        bit_position,
                        channel_choice[0],
                    )
                    ImageObj.encode_image()

                    DCT_Images_List.append(ImageObj)
    return DCT_Images_List


def create_html_for_images(file_path, image_names, type):
    images_per_row = 4  # This is a fixed value as we have generated images in which 25%,50%,75%,100% of the image has been modified
    rows_bitsub = (
        len(image_names) * 8
    )  # For every image, we have a row for every bit position so 8 rows per image since 8 positions
    rows_dct = len(image_names) * 8 * 3
    num_rows = (
        rows_bitsub + rows_dct
    )  # This equates to the number of images in the modifiedimagesfile / 4 as for each type of modification we have generated 4 images

    BitSubFilePath = f"{file_path}/ModifiedImages/BitSubModifiedImages"
    all_bitsub_images = os.listdir(BitSubFilePath)
    with open("Index.html", "w") as f:
        # Write the HTML header
        f.write(
            """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="style.css">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Steganography Project Results</title>
        </head>
        """)
        if type == 1 or type == 3:
            f.write("""
            <body>
    
                <h2>Bit Substitution Results</h2>
    
                <br><br>
                <br><br>
                <br><br>
    
            """
            )

            # Loop through each row for bit sub
            for i in range(rows_bitsub):

                # Find Bit Position
                CurrentRow = all_bitsub_images[
                    i::rows_bitsub
                ]  # In a given row, the bit position will be same for all the images
                # square_bracket = CurrentRow[0].find('[') # Using first image, could use any, using [ to find bit pos
                bit_position = CurrentRow[0][1 + CurrentRow[0].find("[")]

                f.write(f"<h3>Bit Substitution: Bit Position {bit_position}</h3>")
                f.write('<div class="row">')

                # Display images in each row
                for j in range(1, images_per_row + 1):
                    f.write(
                        f"""
                    <div class="column">
                        <div class="image-container">
                            <img src="/{BitSubFilePath}/{all_bitsub_images[i::rows_bitsub][j-1]}" width="100%;">
                            <div class="text">{(j/4)*100}%</div>
                        </div>
                    </div>
                    """
                    )

                f.write("</div>")  # Close the row div
                f.write(
                    """
                        <br><br>
                        <br><br>
                        <br><br>
                    """
                )
        if type == 2 or type == 3:
            f.write("""<h2>DCT Results</h2>""")
            f.write(
                """
                    <br><br>
                    <br><br>
                    <br><br>
                """
            )
            DCTFilePath = f"{file_path}/ModifiedImages/DCTModifiedImages"
            all_dct_images = os.listdir(DCTFilePath)

            for i in range(rows_dct):
                # For a given row the bit position and the channel modified for all the images will be the same
                CurrentRow = all_dct_images[
                    i::rows_dct
                ]  # In a given row, the bit position will be same for all the images
                bit_position = CurrentRow[0][1 + CurrentRow[0].find("[")]
                channel = CurrentRow[0][
                    CurrentRow[0].rfind("_") + 1 : CurrentRow[0].rfind(".")
                ]  # the channel name will be from the last '_' to the '.'

                f.write(
                    f"<h3>DCT: Bit Position: {bit_position} Channel: {channel.title()}</h3>"
                )
                f.write('<div class="row">')

                # Display images in each row
                for j in range(1, images_per_row + 1):
                    f.write(
                        f"""
                    <div class="column">
                        <div class="image-container">
                            <img src="/{DCTFilePath}/{all_dct_images[i::rows_dct][j-1]}" width="100%;">
                            <div class="text">{(j/4)*100}%</div>
                        </div>
                    </div>
                    """
                    )

                f.write("</div>")  # Close the row div
                f.write(
                    """
                        <br><br>
                        <br><br>
                        <br><br>
                    """
                )

        # Write the HTML footer
        f.write(
            """
        </body>
        </html>
        """
        )

    # print(f"HTML file '{html_filename}' created successfully!")


if __name__ == "__main__":
    base_filepath = obtain_filepath()

    # image_names = [['Colourful','jpg'],['SimilarColours','jpg'],['GreyScale','webp']] #Can be changed by the user
    image_names = os.listdir(f"{base_filepath}/OriginalImages")
    image_names = [i.split('.') for i in image_names]

    print(len(image_names))
    # Need to implement it so the user can decide what algorithms a html file will be generated for

    get_user_choice =-1

    print("**NOTE** Please ensure you have placed the image files you would like to test in the 'OriginalImages' folder **NOTE**")

    if len(image_names) == 0:
        raise ValueError("Please place the image(s) you would like to test in the 'OriginalImages' folder!")

    while get_user_choice not in range(1, 3+1):
        get_user_choice = int(input(
            """Please Enter which algorithm you would like to test:
        1. Bit Substitution Based Steganography
        2. DCT Based Steganography
        3. Both
        
        Option: """
        ))

    create_html_for_images(base_filepath,image_names,3)

    if get_user_choice == 1:
        generate_bitsub_images(base_filepath, image_names)
        create_html_for_images(base_filepath, image_names, get_user_choice)

    elif get_user_choice == 2:
        generate_dct_images(base_filepath, image_names)
        create_html_for_images(base_filepath, image_names, get_user_choice)

    elif get_user_choice == 3:  # Regardless of if they input 3 or an invalid input, we will do both
        generate_dct_images(base_filepath, image_names)
        generate_bitsub_images(base_filepath, image_names)
        create_html_for_images(base_filepath, image_names, get_user_choice)



    #IMPORTANT NEED TO ADD THE HOVER THING TO HTML


