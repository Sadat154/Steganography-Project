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
        if (
            len(binary_message)
            > self.channels * original_image.size[0] * original_image.size[1]
        ):
            print(len(binary_message))
            print(self.channels * original_image.size[0] * original_image.size[1])
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
                        # print(test[i])
                        data_index += 1

                original_image.putpixel((x, y), tuple(pixel))

        original_image.save(self.encoded_image_path)

    def decode_image(self):
        encoded_image = Image.open(self.encoded_image_path)

        binary_message = ""
        message_length = 0
        decoded_message = ""

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

                if DELIM in decoded_message:
                    break

            if DELIM in decoded_message:
                break

            remaining_bits = message_length % 8
            if remaining_bits != 0:
                binary_message = binary_message[:-remaining_bits]

        return decoded_message[: -(len(DELIM))]


#
# def generate_bitsub_images(original_image_path):
#     Images = []
#     original_image = Image.open(original_image_path)
#     for i in range(0,8): #Bit
#         #Need to obtain maximum amount of characters available to be embedded into the image
#         max_chars = 3 * original_image.size[0] * original_image.size[1]
#
#         #For each bit, 4 images need to be produced
#         for j in range(1,5):
#             percentage = j/4
#             chars_to_be_embedded = 'a' * math.trunc((((percentage * max_chars)) / 8)-len(Delim)) # We divide by 8 to account for the binary
#             output_image_path = f'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub_bitpos[{8-(i)}]_{j/4*100}%.png'
#             ImageObj = BitEncoderDecoder(original_image_path,output_image_path,i)
#             ImageObj.encode_bit((chars_to_be_embedded))
#             Images.append(ImageObj)
#
# generate_bitsub_images(original_image_path)
# Need to use decode_bit to test that the code works properly
# 25%,50%,75%,100% - bit 1-8 so 4*8 = 32 images for one image. Ideal 3 images.


# REMINDER THE WAY MY CODE WORKS IF BIT POSITION = 0 THEN MSB IF =7 THEN LSB Fixed the issue GG
