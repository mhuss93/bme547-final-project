import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
import base64
import struct
import io
import cv2


# Encode image file to str
def imgFile2str(img_loc):
    """
    Takes in address of image file to be encoded into str.
    Encodes the image into a string.

    param:
    img_loc - location of address

    returns:
    img_str - string of encoded image
    """
    with open(img_loc, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
        imageFile.close()
        return img_str


# Decode str file to image
def str2imgFile(img_loc, img_str):
    """
    Takes in name of encoded image to save as file.
    Decodes the string and saves the image.

    param:
    img_loc - location of address
    img_str - the string of the image

    returns:
    nothing
    """
    with open(img_loc, "wb") as fh:
        decstr = base64.b64decode(img_str)
        fh.write(decstr)
        fh.close()
    return 0


# Encode image array to str
def imgArray2str(img):
    """
    Takes in image rbg array to be encoded into str.
    Encodes the array into a string.

    param:
    img - image rgb array

    returns:
    img_str - string of encoded image
    """
    _, img_buf = cv2.imencode(".png", img)
    img_buf_64 = base64.b64encode(img_buf)
    b64_imgString = str(img_buf_64, encoding='utf-8')
    payload = {"img": b64_imgString}
    return b64_imgString


# Encode image array to str
def imgArray2str2(img):
    """
    Takes in image rbg array to be encoded into str.
    Encodes the array into a string.

    param:
    img - image rgb array

    returns:
    img_str - string of encoded image
    """
    _, img_buf = cv2.imencode(".png", img)
    img_buf_64 = base64.b64encode(img_buf)
    b64_imgString = str(img_buf_64, encoding='utf-8')
    payload = {"img": b64_imgString}
    return b64_imgString


# Decode str to image array
def str2imgArray(img_str):
    """
    Takes in name of encoded image to save.
    Decodes the string and saves the image.

    param:
    img_loc - location of address

    returns:
    img - array of decoded image
    """
    img_bytes = base64.b64decode(img_str)
    img_buf = io.BytesIO(img_bytes)
    img_array = mpimg.imread(img_buf, format='JPG')
    return img_array


if __name__ == "__main__":
    # create an img string from file
    img_loc = 'reversed_image.png'
    img_str = imgFile2str(img_loc)
    # covert string to img array
    img = str2imgArray(img_str)
    print('img')
    print(img)
    # show the image
    imshow(img, cmap=get_cmap('gray'))
    title('one')
    show()
    # turn to string and back to img array
    img_str = imgArray2str2(img)
    imgback = str2imgArray(img_str)
    print('imgback')
    print(imgback)
    # show the decoded image
    imshow(imgback, cmap=get_cmap('gray'))
    title('two')
    show()
