from PIL import Image
from SteganographyAlgorithm import SteganographyAlgorithm

DELIM = "%$Â£QXT"


class BitSubEncoderDecoder(SteganographyAlgorithm):
    def __init__(
        self, original_image_path, encoded_image_path, secret_message, bit_position
    ):
        super().__init__(original_image_path, encoded_image_path, secret_message, bit_position)
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
            for y in range(original_image.size[1]):
                for x in range(original_image.size[0]):
                    pixel = list(original_image.getpixel((x, y)))
                    pixellist_to_binary = [self.decimal_to_binary(i) for i in pixel]

                    for i in range(self.channels):
                        if data_index < len(binary_message):

                            pixel_binary = list(
                                [j for j in pixellist_to_binary[i]]
                            )  # Split the pixel into its binary letters

                            pixel_binary[self.bit_position] = binary_message[data_index]
                            # Need to convert value to decimal now

                            pixel_binary = self.binary_to_decimal("".join(pixel_binary))
                            # Finally need to adjust the decimal value stored in pixel
                            pixel[i] = pixel_binary
                            # pixel[i] = pixel[i] & ~(1 << self.bit_position) | (int(binary_message[data_index]) << self.bit_position)

                            data_index += 1

                    original_image.putpixel((x, y), tuple(pixel))
            original_image.save(self.encoded_image_path)
        else:
            if (
                len(binary_message)
                > original_image.size[0] * original_image.size[1]
            ):
                raise ValueError("Message is too long to be encoded in the greyscale image")

            pixels = list(self.original_image.getdata())
            # Encode the secret message into the specified bit of each pixel
            encoded_pixels = []
            for pixel, bit in zip(pixels, binary_message):
                # Clear the specified bit and set it to the secret message bit
                new_pixel = (pixel & ~(1 << (7 - self.bit_position))) | (int(bit) << (7 - self.bit_position))
                encoded_pixels.append(new_pixel)
            encoded_pixels = encoded_pixels + pixels[len(binary_message):]
            # Create a new image with the encoded pixel data
            encoded_image = Image.new("L", self.original_image.size)
            encoded_image.putdata(encoded_pixels)
            encoded_image.save(self.encoded_image_path)




    def decode_image(self):
        encoded_image = Image.open(self.encoded_image_path)

        binary_message = ""
        message_length = 0
        decoded_message = ""
        if self.mode != "L":
            while decoded_message[-(len(self.DELIM)) :] != self.DELIM:
                for y in range(encoded_image.size[1]):
                    for x in range(encoded_image.size[0]):
                        pixel = list(encoded_image.getpixel((x, y)))

                        for i in range(3):
                            binary_message += str(
                                (self.decimal_to_binary(pixel[i]))[self.bit_position]
                            )

                            decoded_message = "".join(
                                [
                                    chr(int(binary_message[i : i + 8], 2))
                                    for i in range(0, len(binary_message), 8)
                                ]
                            )
                            message_length += 1
                            if self.DELIM in decoded_message:
                                break

                        if self.DELIM in decoded_message:
                            break

                    if self.DELIM in decoded_message:
                        break

                if self.DELIM in decoded_message:
                    break

        else:
            pixels = encoded_image.getdata()

            for pixel in pixels:
                bin_val = self.decimal_to_binary(pixel)
                binary_message += bin_val[self.bit_position]

                decoded_message = "".join(
                    [
                        chr(int(binary_message[i: i + 8], 2))
                        for i in range(0, len(binary_message), 8)
                    ]
                )
                message_length += 1
                if self.DELIM in decoded_message:
                    break


        return decoded_message[: -(len(DELIM))]

