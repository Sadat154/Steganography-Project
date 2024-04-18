import unittest
from PIL import Image
import os
from SteganographyAlgorithm import SteganographyAlgorithm


class MessageTooLargeError(Exception):
    pass
class TestSteganographyAlgorithm(unittest.TestCase):
    def setUp(self):
        self.steg_algo = SteganographyAlgorithm()

#################################################Chunks#########################################
    def test_chunks_with_valid_input(self):
        result = list(self.steg_algo.chunks([1, 2, 3, 4, 5, 6, 7, 8], 2))
        self.assertEqual(result, [[1, 2], [3, 4], [5, 6], [7, 8]])

    def test_chunks_with_empty_list(self):
        result = list(self.steg_algo.chunks([], 2))
        self.assertEqual(result, [])

    def test_chunks_with_chunk_size_greater_than_list_length(self):
        result = list(self.steg_algo.chunks([1, 2, 3], 5))
        self.assertEqual(result, [[1, 2, 3]])

    def test_chunks_with_chunk_size_zero(self):
        with self.assertRaises(ValueError):
            list(self.steg_algo.chunks([1, 2, 3], 0))

    def test_chunks_with_negative_chunk_size(self):
        with self.assertRaises(ValueError):
            list(self.steg_algo.chunks([1, 2, 3], -1))

#################################################Chunks#########################################


#################################################Message_To_Bin#########################################
class TestMessageToBin(unittest.TestCase):
    def setUp(self):
        self.message_to_bin = SteganographyAlgorithm().message_to_bin

    def test_empty_string(self):
        self.assertEqual(self.message_to_bin(''), '', 'Empty string should return an empty string')

    def test_single_character(self):
        self.assertEqual(self.message_to_bin('a'), '01100001', 'Character "a" should return "01100001"')

    def test_multiple_characters(self):
        self.assertEqual(self.message_to_bin('abc'), '011000010110001001100011', 'String "abc" should return "011000010110001001100011"')

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            self.message_to_bin(123)

#################################################Message_To_Bin#########################################


##################Open_Image######################


class TestOpenImage(unittest.TestCase):
    def setUp(self):
        self.open_image = SteganographyAlgorithm().open_image

    def test_valid_image_path(self):
        # Create a small image for testing
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save('test_image.jpg')
        img.close()

        opened_img = self.open_image('test_image.jpg')
        self.assertIsInstance(opened_img, Image.Image, 'Should return an instance of PIL.Image.Image')
        opened_img.close()

        # Clean up the test image
        os.remove('test_image.jpg')

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.open_image('non_existent_file.jpg')


    def test_non_image_file(self):
        # Create a non-image file for testing
        with open('test_file.txt', 'w') as f:
            f.write('This is a test file.')

        with self.assertRaises(Exception):
            self.open_image('test_file.txt')

        # Clean up the test file
        os.remove('test_file.txt')
##################Open_Image######################

########################DEC_TO_BIN######################
class TestDecimalToBinary(unittest.TestCase):
    def setUp(self):
        self.decimal_to_binary = SteganographyAlgorithm().decimal_to_binary

    def test_zero(self):
        self.assertEqual(self.decimal_to_binary(0), '00000000', 'Decimal 0 should return "00000000"')

    def test_positive_integer(self):
        self.assertEqual(self.decimal_to_binary(10), '00001010', 'Decimal 10 should return "00001010"')

    def test_large_positive_integer(self):
        self.assertEqual(self.decimal_to_binary(255), '11111111', 'Decimal 255 should return "11111111"')

    def test_negative_integer(self):
        with self.assertRaises(ValueError):
            self.decimal_to_binary(-1)

    def test_non_integer_input(self):
        with self.assertRaises(TypeError):
            self.decimal_to_binary('abc')
########################DEC_TO_BIN######################





########################BIN_TO_DEC######################
class TestBinaryToDecimal(unittest.TestCase):
    def setUp(self):
        self.binary_to_decimal = SteganographyAlgorithm().binary_to_decimal

    def test_zero(self):
        self.assertEqual(self.binary_to_decimal('00000000'), 0, 'Binary "00000000" should return 0')

    def test_positive_integer(self):
        self.assertEqual(self.binary_to_decimal('00001010'), 10, 'Binary "00001010" should return 10')

    def test_large_positive_integer(self):
        self.assertEqual(self.binary_to_decimal('11111111'), 255, 'Binary "11111111" should return 255')

    def test_invalid_binary_string(self):
        with self.assertRaises(ValueError):
            self.binary_to_decimal('abc')

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            self.binary_to_decimal(123)

########################BIN_TO_DEC######################


########################RESIZE_IMAGE####################
class TestResizeImage(unittest.TestCase):
    def setUp(self):
        self.resize_image = SteganographyAlgorithm().resize_image

    def test_resize_image(self):
        # Create a small image for testing
        img = Image.new('RGB', (10, 10), color = 'red')
        resized_img, new_height, new_width = self.resize_image(img)
        self.assertEqual((new_width, new_height), (16, 16), 'Image of size 10x10 should be resized to 16x16')

    def test_image_already_multiple_of_eight(self):
        # Create a small image for testing
        img = Image.new('RGB', (16, 16), color = 'red')
        resized_img, new_height, new_width = self.resize_image(img)
        self.assertEqual((new_width, new_height), (16, 16), 'Image of size 16x16 should remain 16x16')

    def test_non_image_input(self):
        with self.assertRaises(AttributeError):
            self.resize_image('not an image')

########################RESIZE_IMAGE####################










################ADJUST_BITMASK####################
class TestAdjustBitmask(unittest.TestCase):
    def setUp(self):
        self.adjust_bitmask = SteganographyAlgorithm().adjust_bitmask

    def test_zero(self):
        self.assertEqual(self.adjust_bitmask(0), 128, 'Bit position 0 should return 128')

    def test_positive_integer(self):
        self.assertEqual(self.adjust_bitmask(3), 240, 'Bit position 3 should return 240')

    def test_large_positive_integer(self):
        self.assertEqual(self.adjust_bitmask(7), 255, 'Bit position 7 should return 255')

    def test_negative_integer(self):
        with self.assertRaises(ValueError):
            self.adjust_bitmask(-1)

    def test_non_integer_input(self):
        with self.assertRaises(TypeError):
            self.adjust_bitmask('abc')

################ADJUST_BITMASK####################

############CHECK MESSAGE LENGTH##################
class TestCheckMessageLengthDCT(unittest.TestCase):
    def setUp(self):
        self.check_message_length_DCT = SteganographyAlgorithm().check_message_length_DCT

    def test_message_fits(self):
        try:
            self.check_message_length_DCT(64, 64, 'Hello World') #Expected
        except MessageTooLargeError:
            self.fail('MessageTooLargeError raised unexpectedly!')

    def test_message_too_large(self): #Invalid # Need to ask sir to help me with this as it is a custom exception
        with self.assertRaises(MessageTooLargeError):
            self.check_message_length_DCT(64, 64, 'This message is definitely too long to fit in the image, because it is just too large to fit in the image!')

    def test_zero_dimensions(self):#Boundary # Need help with this too
        with self.assertRaises(MessageTooLargeError):
            self.check_message_length_DCT(0, 0, 'Any message')

    def test_non_integer_dimensions(self):
        with self.assertRaises(TypeError):
            self.check_message_length_DCT('abc', 64, 'Any message')

        with self.assertRaises(TypeError):
            self.check_message_length_DCT(64, 'abc', 'Any message')

    def test_non_string_message(self):
        with self.assertRaises(TypeError):
            self.check_message_length_DCT(64, 64, 123)



if __name__ == "__main__":
    unittest.main()