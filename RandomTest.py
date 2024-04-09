from PIL import Image
image_path = 'C:/Users/Nafis/Desktop/Python_projects/Steganography-Project/OriginalImages/GreyScale.webp'
image = Image.open(image_path)

for y in range(image.size[1]):
    for x in range(image.size[0]):
        pixel = list(image.getpixel((x, y)))
        print(pixel)