import math

from BitSubStega import BitSubEncoderDecoder
from DCTStega import DCTSteg
from PIL import Image

DELIM = "%$Â£QXT"

####The following are for testing the BitSubEncoderDecoder class in BitSubStega.py####


### Set Up ###
testing_image_path = "TestingImage.jpg"
testing_image = Image.open(testing_image_path)
maximum_chars = 3 * testing_image.size[0] * testing_image.size[1]

bit_position = (
    4  # The bit position chosen does not matter for the purpose of tests 1.1-1.4
)


### Test: 1.1 ###

secret_message = "Hello World!"  # Expected
output_image_path = "TestingOutput/1.1.png"
image_object = BitSubEncoderDecoder(
    testing_image_path, output_image_path, secret_message, bit_position
)
try:
    image_object.encode_image()
    print("1.1 Completed")
except:
    print("1.1 Failed")


### Test: 1.2 ###

secret_message = "A" * math.trunc(
    (((maximum_chars - 8 * len(DELIM))) / 8)
)  # This is the max characters that can be embedded into the TestingImage
output_image_path = "TestingOutput/1.2.png"
image_object = BitSubEncoderDecoder(
    testing_image_path, output_image_path, secret_message, bit_position
)
try:
    image_object.encode_image()
    print("1.2 Completed")
except:
    print("1.2 Failed")


### Test: 1.3 ###

secret_message = "Computer Science"
output_image_path = "TestingOutput/1.3.png"
image_object = BitSubEncoderDecoder(
    testing_image_path, output_image_path, secret_message, bit_position
)
image_object.encode_image()

output_message = image_object.decode_image()

if output_message == secret_message:
    print("1.3 Completed")


### Test: 1.4 ###

secret_message = "A" * (maximum_chars + 10)  # Value greater than max character
output_image_path = "TestingOutput/1.4.png"
image_object = BitSubEncoderDecoder(
    testing_image_path, output_image_path, secret_message, bit_position
)
try:
    image_object.encode_image()
except ValueError:
    print("1.4 Completed")


### Test: 1.5 ###
try:
    for i in range(0, 8):  # Bit
        secret_message = "Hello World"
        output_image_path = f"TestingOutput/1.5_bit_position{i+1}.png"
        image_object = BitSubEncoderDecoder(
            testing_image_path, output_image_path, secret_message, i
        )
        image_object.encode_image()
    print("1.5 Completed")

except:
    print("1.5 Failed")


### The following are tests for testing the DCTSteg class in DCTStega.py ###


### Set Up ###
testing_image_path = "TestingImage.jpg"
testing_image = Image.open(testing_image_path)
maximum_DCT_chars = int((testing_image.size[1] / 8) * (testing_image.size[0] / 8))


bit_position = (
    4  # The bit position chosen does not matter for the purpose of tests 2.1-2.4
)
channel_choice = (
    "r"  # The channel chosen does not matter for the purpose of tests 2.1-2.4
)

### Test: 2.1 ###

secret_message = "Hello World!"  # Expected
output_image_path = "TestingOutput/2.1.png"
image_object = DCTSteg(
    testing_image_path, output_image_path, secret_message, bit_position, channel_choice
)
try:
    image_object.encode_image()
    print("2.1 Completed")
except:
    print("2.1 Failed")


### Test: 2.2 ###

secret_message = "A" * math.trunc(
    maximum_DCT_chars - len(DELIM)
)  # This is the max characters that can be embedded into the TestingImage
output_image_path = "TestingOutput/2.2.png"
image_object = DCTSteg(
    testing_image_path, output_image_path, secret_message, bit_position, channel_choice
)
try:
    image_object.encode_image()
    print("2.2 Completed")
except:
    print("2.2 Failed")


### Test: 2.3 ###

secret_message = "Computer Science"
output_image_path = "TestingOutput/2.3.png"
image_object = DCTSteg(
    testing_image_path, output_image_path, secret_message, bit_position, "b"
)
image_object.encode_image()

output_message = image_object.decode_image()

if output_message == secret_message:
    print("2.3 Completed")
else:
    print("2.3 Failed")


### Test: 2.4 ###

secret_message = "A" * (maximum_chars + 10)  # Value greater than max character
output_image_path = "TestingOutput/2.4.png"
image_object = DCTSteg(
    testing_image_path, output_image_path, secret_message, bit_position, channel_choice
)
try:
    image_object.encode_image()
except:  # Custom exception "MessageTooLargeError" should be raised
    print("2.4 Completed")


### Test: 2.5.1 ###
try:
    for i in range(0, 8):  # Bit
        secret_message = "Hello World"
        output_image_path = f"TestingOutput/2.5.1_bit_position-{i+1}.png"
        image_object = DCTSteg(
            testing_image_path, output_image_path, secret_message, i, channel_choice
        )
        image_object.encode_image()
    print("2.5.1 Completed")

except:
    print("2.5.1 Failed")


### Test: 2.5.2 ###
channels = ["r", "g", "b"]
try:
    for i in channels:  # Bit
        secret_message = "Hello World"
        output_image_path = f"TestingOutput/2.5_channel-{i}.png"
        image_object = DCTSteg(
            testing_image_path, output_image_path, secret_message, bit_position, i
        )
        image_object.encode_image()
    print("2.5.2 Completed")

except:
    print("2.5.2 Failed")
