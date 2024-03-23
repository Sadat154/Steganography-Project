import numpy as np
from PIL import Image


x = Image.open("cropped.jpg")
ch = np.array(x)
print(ch)
print(ch[:, :, 0])