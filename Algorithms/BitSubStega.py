from PIL import Image
from SteganographyAlgorithm import SteganographyAlgorithm


class BitSubEncoderDecoder(SteganographyAlgorithm):
    def __init__(
        self, original_image_path, encoded_image_path, secret_message, bit_position
    ):
        super().__init__(
            original_image_path, encoded_image_path, secret_message, bit_position
        )
        self.channels = 3
        self.secret_message = secret_message

    def encode_image(self):
        original_image = self.original_image
        secret_message = (
            self.secret_message + self.DELIM
        )  # Delimiter to indicate end of message
        binary_message = self.message_to_bin(secret_message)
        if self.mode != "L":
            if (
                len(binary_message)
                > self.channels * original_image.size[0] * original_image.size[1]
            ):

                raise ValueError("Message is too long to be encoded in the image")

            data_index = 0
            for y in range(original_image.size[1]):  # Iterate through every pixel
                for x in range(original_image.size[0]):
                    pixel = list(original_image.getpixel((x, y)))
                    pixellist_to_binary = [
                        self.decimal_to_binary(i) for i in pixel
                    ]  # Convert every pixel into binary

                    for i in range(self.channels):
                        if data_index < len(binary_message):

                            pixel_binary = list(
                                [j for j in pixellist_to_binary[i]]
                            )  # Split the pixel into its binary letters e.g., ['10'] = ['1','0']

                            # Modify the chosen bit position
                            pixel_binary[self.bit_position] = binary_message[data_index]

                            # Need to convert pixel back in to binary
                            pixel_binary = self.binary_to_decimal("".join(pixel_binary))

                            # Modify the original list of pixels
                            pixel[i] = pixel_binary

                            # pixel[i] = pixel[i] & ~(1 << self.bit_position) | (int(binary_message[data_index]) << self.bit_position)
                            data_index += 1

                    # Create a new image with the pixels we have modified
                    original_image.putpixel((x, y), tuple(pixel))
            # Save the image
            original_image.save(self.encoded_image_path)
        else:
            if len(binary_message) > original_image.size[0] * original_image.size[1]:
                raise ValueError(
                    "Message is too long to be encoded in the greyscale image"
                )  # Greyscale images only have one channel, so 1/3 the characters can be embedded, relative to RGB images

            pixels = list(self.original_image.getdata())
            # Encode the secret message into the specified bit of each pixel
            encoded_pixels = []
            for pixel, bit in zip(pixels, binary_message):
                # Clear the specified bit and set it to the secret message bit
                new_pixel = (pixel & ~(1 << (7 - self.bit_position))) | (
                    int(bit) << (7 - self.bit_position)
                )
                encoded_pixels.append(new_pixel)
            encoded_pixels = (
                encoded_pixels + pixels[len(binary_message) :]
            )  # Not all pixels will be modified, so we add the remaining unmodified pixels too

            # Create a new image with the encoded pixel data
            encoded_image = Image.new("L", self.original_image.size)
            encoded_image.putdata(encoded_pixels)
            encoded_image.save(self.encoded_image_path)

    def decode_image(self):
        # Open the image file that contains the encoded message
        encoded_image = Image.open(self.encoded_image_path)

        # Initialise variables to store the binary and decoded message
        binary_message = ""
        message_length = 0
        decoded_message = ""

        # Check if the image is not in 'L' mode (greyscale)
        if self.mode != "L":
            # Continue looping until the delimiter is found in the decoded message
            while decoded_message[-(len(self.DELIM)) :] != self.DELIM:
                # Iterate over each pixel in the image
                for y in range(encoded_image.size[1]):
                    for x in range(encoded_image.size[0]):
                        # Get the RGB values of the pixel
                        pixel = list(encoded_image.getpixel((x, y)))

                        # Iterate over each color channel
                        for i in range(3):
                            # Extract the bit at the specified position and add it to the binary message
                            binary_message += str(
                                (self.decimal_to_binary(pixel[i]))[self.bit_position]
                            )

                            # Convert the binary message to a string every 8 bits (1 byte)
                            decoded_message = "".join(
                                [
                                    chr(int(binary_message[i : i + 8], 2))
                                    for i in range(0, len(binary_message), 8)
                                ]
                            )
                            # Increment the message length counter
                            message_length += 1
                            # Break the loop if the delimiter is found
                            if self.DELIM in decoded_message:
                                break

                        if self.DELIM in decoded_message:
                            break

                    if self.DELIM in decoded_message:
                        break

                if self.DELIM in decoded_message:
                    break

        # If the image is in 'L' mode (greyscale)
        else:
            # Get all pixel values of the image
            pixels = encoded_image.getdata()

            # Iterate over each pixel
            for pixel in pixels:
                # Convert the pixel value to binary
                bin_val = self.decimal_to_binary(pixel)
                # Extract the bit at the specified position and add it to the binary message
                binary_message += bin_val[self.bit_position]

                # Convert the binary message to a string every 8 bits (1 byte)
                decoded_message = "".join(
                    [
                        chr(int(binary_message[i : i + 8], 2))
                        for i in range(0, len(binary_message), 8)
                    ]
                )
                # Increment the message length counter
                message_length += 1
                # Break the loop if the delimiter is found
                if self.DELIM in decoded_message:
                    break

        # Return the decoded message without the delimiter
        return decoded_message[: -(len(self.DELIM))]
