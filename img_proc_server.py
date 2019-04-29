import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist, imsave
from skimage.exposure import equalize_hist, rescale_intensity, adjust_log
from skimage import util

import numpy as np


# histogram equalization
def equalize_img(img):
    """
    Take address of image to be processed as img_loc.
    Computes equalization and returns both the input img and equalized img.

    param:
    img - address to access image to be processed

    returns:
    img - 2D array of input image
    equalized - 2D array of equalized image
    """
    equalized = np.asarray(equalize_hist(img)*255, dtype='uint8')
    return equalized[:, :, 0:3]


# constrast stretching
def contr_stretch_img(img):
    """
    Take address of image to be processed as img_loc.
    Computes contrast stretch and returns both the input img and stretched img.

    param:
    img - address to access image to be processed

    returns:
    img - 2D array of input image
    stretch_img - 2D array of stretched image
    """
    stretched = np.asarray(rescale_intensity(img, in_range=(0, 200)),
                           dtype='uint8')
    return stretched[:, :, 0:3]


# log correction
def log_correct_img(img):
    """
    Take address of image to be processed as img_loc.
    Computes log correction and returns both the input img and corrected img.

    param:
    img - address to access image to be processed

    returns:
    img - 2D array of input image
    log_img - 2D array of log corrected image
    """
    log_img = np.asarray(adjust_log(img, 2), dtype='uint8')
    return log_img[:, :, 0:3]


# reverse video
def reverse_img(img):
    """
    Take address of image to be processed as img_loc.
    Computes log correction and returns both the input img and corrected img.

    param:
    img - address to access image to be processed

    returns:
    img - 2D array of input image
    reverse_img - 2D array of reversed image
    """
    reverse_img = np.asarray(util.invert(img), dtype='uint8')
    return reverse_img[:, :, 0:3]


# pull out RGB values for histogram
def RGB(img):
    """
    Takes img as np.array. Seperates rgb values and returns 3 arrays.

    param:
    img - array of image after performing imread

    returns:
    r, g, b - arrays of values for each color
    """
    img_shape = img.shape
    r = []
    g = []
    b = []
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            r.append(img[i, j, 0])
            g.append(img[i, j, 1])
            b.append(img[i, j, 2])
    return r, g, b


# plot histograms for RGB
def plot_rgb(r, g, b):
    """
    Plots the 3 histograms for colors red, green blue of inputted image array

    param:
    r, g, b - arrays of values for each color

    returns:
    nothing - plots the histograms
    """
    plt.figure()
    subplot(311)
    hist(r, 256, range=(0, 256), color='red')
    title('Red')
    subplot(312)
    hist(g, 256, range=(0, 256), color='green')
    title('Green')
    subplot(313)
    hist(b, 256, range=(0, 256), color='blue')
    title('Blue')
    plt.show()


if __name__ == "__main__":
    # create an img string from file
    from encode_decode import imgFile2str
    img_loc = 'reversed_image.png'
    img_str = imgFile2str(img_loc)
    # covert string to img array
    from encode_decode import str2imgArray
    img = str2imgArray(img_str)
    # show the image
    imshow(img, cmap=get_cmap('gray'))
    title('img')
    show()
    # reverse
    reverse = reverse_img(img)
    # show the reversed image
    imshow(reverse, cmap=get_cmap('gray'))
    title('reverse')
    show()
    # plot histogram for original
    r, g, b = RGB(img)
    plot_rgb(r, g, b)
    # plot histogram for reversed
    r, g, b = RGB(reverse)
    plot_rgb(r, g, b)
