from pathlib import Path
from PIL import Image

# Custom exception for when the message is too large to encode in the image
class MessageTooLargeError(Exception):
    pass


class SteganographyAlgorithm:
    def __init__(
        self,
        original_image_path: Path = None,
        encoded_image_path: Path = None,
        secret_message: str = "",
        bit_position: int = -1,
        channel: str = "",
    ):
        self.DELIM = "%$Â£QXT"
        if original_image_path is not None:
            self.original_image = self.open_image(original_image_path)
            self.height = self.original_image.size[1]
            self.width = self.original_image.size[0]
            self.mode = self.original_image.mode
        self.encoded_image_path = encoded_image_path
        self.secret_message = secret_message
        self.bit_position = bit_position
        self.channel = channel

    def open_image(self, image_path):
        try:
            img = Image.open(image_path)
            return img
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {image_path}")
        except Exception as e:
            raise Exception(f"Error opening image: {e}")

    def message_to_bin(self, message):
        binary_message = "".join(format(ord(char), "08b") for char in message)
        return binary_message

    def decimal_to_binary(self, decimal_value):  # Only for positive decimal values
        if decimal_value < 0:
            raise ValueError()
        # Convert decimal to binary string
        binary_string = bin(decimal_value)[2:]  # Remove '0b' prefix from binary string
        # Pad the binary string with leading zeros if necessary to ensure it's 8 bits long
        padded_binary_string = binary_string.zfill(8)
        return padded_binary_string

    def binary_to_decimal(self, binary_string):
        # Convert binary string to decimal value
        decimal_value = int(binary_string, 2)
        return decimal_value

    # Method to check if the message can fit in the image using DCT based steganography
    def check_message_length_DCT(self, height, width, message):
        total = (width / 8) * (height / 8)
        length = len(message)
        if total < length:
            raise MessageTooLargeError(
                f"Message ({length}) is too large to be encode in the image ({total})"
            )

    def chunks(
        self, currentlist, n
    ):  # Takes a list and splits it into chunks of size n
        m = int(n)
        if m < 0:
            raise ValueError()
        for i in range(0, len(currentlist), m):
            yield currentlist[i : i + m]

    # Method to resize an image to a multiple of 8
    def resize_image(self, img):
        # height, width = self.height, self.width
        width, height = img.size
        new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
        new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

        # Resize image to a multiple of 8
        resized_image = img.resize((new_width, new_height))
        return resized_image, new_height, new_width


    # Adjusts bitmask for encoding using DCT
    def adjust_bitmask(self, bitpos):
        if bitpos < 0:
            raise ValueError()

        bitchoice = bitpos + 1
        ans = 0
        for i in range(0, (8 - bitchoice)):
            logical_left_shift = 1 << (i)
            ans += logical_left_shift

        finalAns = 255 - ans

        return finalAns

    def encode_image(self):
        pass

    def decode_image(self):
        pass
