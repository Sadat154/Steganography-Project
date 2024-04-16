from PIL import Image
def resize_image(img):
    height, width = img.height, img.width
    new_height = height + (8 - (height % 8)) if height % 8 != 0 else height
    new_width = width + (8 - (width % 8)) if width % 8 != 0 else width

    # Resize image to a multiple of 8
    resized_image = img.resize((new_width, new_height))
    return resized_image, new_height, new_width



#x = Image.open("C:\\Users\\naf15\\OneDrive\\Desktop\\Python_Projects\\Steganography-Project\\OriginalImages\\Colourful.jpg")
#x = resize_image(x)[0]
