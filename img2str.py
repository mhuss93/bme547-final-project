import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
import base64


# Encode image to str
def img2str(img_loc):
    """
    Takes in address of image to be encoded into str.
    Encodes the image into a string.

    param:
    img_loc - location of address

    returns:
    img_str - string of encoded image
    """
    with open(img_loc, "rb") as imageFile:
        img_str = base64.b64encode(imageFile.read())
        return img_str


# Decode str to image
def str2img(img_loc, img_str):
    """
    Takes in name of encoded image to save.
    Decodes the string and saves the image.

    param:
    img_loc - location of address

    returns:
    img_str - string of encoded image
    """
    with open(img_loc, "wb") as fh:
        decstr = base64.b64decode(img_str)
        fh.write(decstr)
        fh.close()
    return 0


if __name__ == "__main__":
    # covert image to string
    img_loc = 'reversed_image.png'
    img_str = img2str(img_loc)
    # convert string back to image
    img_loc = 'reversed_imageback.png'
    str2img(img_loc, img_str)
    img = imread(img_loc)
    imshow(img, cmap=get_cmap('gray'))
    show()
