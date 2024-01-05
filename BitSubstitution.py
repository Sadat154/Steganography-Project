from PIL import Image

class BitEncoderDecoder:
    def __init__(self, original_image_path, encoded_image_path, delim, bit_position=0):
        self.original_image_path = original_image_path
        self.encoded_image_path = encoded_image_path
        self.bit_position = bit_position
        self.delim = delim


    def _message_to_bin(self, message):
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        return binary_message

    def encode_bit(self, secret_message):
        original_image = Image.open(self.original_image_path)
        secret_message += self.delim
        binary_message = self._message_to_bin(secret_message)

        if len(binary_message) > 3 * original_image.size[0] * original_image.size[1]:
            raise ValueError("Message is too long to be encoded in the image")

        data_index = 0
        for y in range(original_image.size[1]):
            for x in range(original_image.size[0]):
                pixel = list(original_image.getpixel((x, y)))

                for i in range(3):
                    if data_index < len(binary_message):
                        pixel[i] = pixel[i] & ~(1 << self.bit_position) | (int(binary_message[data_index]) << self.bit_position)
                        data_index += 1

                original_image.putpixel((x, y), tuple(pixel))

        original_image.save(output_image_path)

    def decode_bit(self):
        encoded_image = Image.open(self.encoded_image_path)

        binary_message = ''
        message_length = 0
        decoded_message = ''

        while decoded_message[-(len(self.delim)):] != self.delim:
            for y in range(encoded_image.size[1]):
                for x in range(encoded_image.size[0]):
                    pixel = list(encoded_image.getpixel((x, y)))

                    for i in range(3):
                        binary_message += str((pixel[i] >> self.bit_position) & 1)
                        decoded_message = ''.join(
                            [chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8)])
                        if self.delim in decoded_message:
                            print(decoded_message)
                            break
                        message_length += 1

                    if self.delim in decoded_message:
                        break

                if self.delim in decoded_message:
                    break

            if self.delim in decoded_message:
                break

            remaining_bits = message_length % 8
            if remaining_bits != 0:
                binary_message = binary_message[:-remaining_bits]

        return decoded_message[:-(len(self.delim))]


# Example usage:
original_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/cropped.jpg'
secret_message = 'abc'
output_image_path = 'C:/Users/naf15/OneDrive/Desktop/Python_Projects/Steganography-Project/BitSubResults/BitSub3.png'
delim='GZOHLUMXWRDTCQF'
bit_position_to_encode = 0  # 0 = LSB, 7 = MSB

bit_encoder_decoder = BitEncoderDecoder(original_image_path, output_image_path, delim, bit_position_to_encode) #Object
bit_encoder_decoder.encode_bit(secret_message) #Object has been encoded

decoded_message = bit_encoder_decoder.decode_bit() #Decode the object

print("Decoded Message:", decoded_message)
