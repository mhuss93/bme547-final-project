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
    """Converts image from address to Base64 encoded string.

    :param img_loc: Image address.
    :type img_loc: str
    :return: Base64 encoded image.
    :rtype: str
    """

    with open(img_loc, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
        imageFile.close()
        return img_str


# Decode str file to image
def str2imgFile(img_loc, img_str):
    """Saves Base64 encoded string to disk as image.

    :param img_loc: Location to save image.
    :type img_loc: str
    :param img_str: [Base64 encoded image string.
    :type img_str: str
    :return: 0 (complete execution)
    :rtype: int
    """
    with open(img_loc, "wb") as fh:
        decstr = base64.b64decode(img_str)
        fh.write(decstr)
        fh.close()
    return 0


# Encode image array to str
def imgArray2str(img):
    """Convert image array to base64 encoded string.

    :param img: Image array.
    :type img: np.array
    :return: Base64 encoded string.
    :rtype: [type]
    """
    _, img_buf = cv2.imencode(".png", img)
    img_buf_64 = base64.b64encode(img_buf)
    b64_imgString = str(img_buf_64, encoding='utf-8')
    payload = {"img": b64_imgString}
    return b64_imgString


# Encode image array to str
def imgArray2str2(img):
    """Convert image array to base64 encoded string.

    :param img: Image array.
    :type img: np.array
    :return: Base64 encoded string.
    :rtype: [type]
    """
    _, img_buf = cv2.imencode(".png", img)
    img_buf_64 = base64.b64encode(img_buf)
    b64_imgString = str(img_buf_64, encoding='utf-8')
    payload = {"img": b64_imgString}
    return b64_imgString


# Decode str to image array
def str2imgArray(img_str):
    """Convert Base64 encoded image string.

    :param img_str: Base64 encoded image.
    :type img_str: str
    :return: Image array.
    :rtype: np.array
    """
    img_bytes = base64.b64decode(img_str)
    img_buf = io.BytesIO(img_bytes)
    img_array = mpimg.imread(img_buf, format='JPG')
    return img_array


if __name__ == "__main__":
    # create an img string from file
    img_loc = 'image_0001.jpg'
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
    img_str = imgArray2str(img)
    imgback = str2imgArray(img_str)
    temp = imgback.copy()
    temp[:, :, 0] = imgback[:, :, 2]
    temp[:, :, 2] = imgback[:, :, 0]
    imgback = temp
    print('imgback')
    print(imgback)
    # show the decoded image
    imshow(imgback, cmap=get_cmap('gray'))
    title('two')
    show()
