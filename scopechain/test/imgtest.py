import cv2
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

# image to string and to image module

with open('./image.png', 'rb') as img:
    base64_string = base64.b64encode(img.read())

img = Image.open(BytesIO(base64.b64decode(base64_string)))
plt.imshow(img)


imgdata = base64.b64decode(base64_string)
filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
with open(filename, 'wb') as f:
    f.write(imgdata)
