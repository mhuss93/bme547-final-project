import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
from skimage import util
import numpy as np


def reverse_img(img_loc):
    """
    Take address of image to be processed as img_loc.
    Computes log correction and returns both the input img and corrected img.

    param:
    img_loc - address to access image to be processed

    returns:
    img - 2D array of input image
    log_img - 2D array of log corrected image
    """
    img = imread(img_loc)
    print('img values: {}' .format(img))
    reverse_img = np.asarray(util.invert(img), dtype='uint8')
    return img, reverse_img


if __name__ == "__main__":
    img, reverse_img = reverse_img('image_0001.jpg')
    plt.imsave('reversed_image.jpg', reverse_img)
    fig = plt.figure(figsize=(8, 5))
    subplot(221)
    imshow(img, cmap=get_cmap('gray'))
    title('Original')
    subplot(222)
    hist(img.flatten(), 256, range=(0, 256))
    title('Histogram of original')
    subplot(223)
    imshow(reverse_img, cmap=get_cmap('gray'))
    title('Log Corrected')
    subplot(224)
    hist(reverse_img.flatten(), 256, range=(0, 256))
    title('Histogram of Log Corrected')
    fig.tight_layout()
    show()
