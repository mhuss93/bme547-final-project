import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
from skimage.exposure import equalize_hist, rescale_intensity, adjust_log
from skimage import util

import numpy as np


# histogram equalization
def equalize_img(img):
    """
    Take address of image to be processed as img_loc.
    Computes equalization and returns both the input img and equalized img.

    param:
    img_loc - address to access image to be processed

    returns:
    img - 2D array of input image
    eq - 2D array of equalized image
    """
    equalized = np.asarray(equalize_hist(img)*255, dtype='uint8')
    return equalized


# constrast stretching
def contr_stretch_img(img_loc):
    """
    Take address of image to be processed as img_loc.
    Computes contrast stretch and returns both the input img and stretched img.

    param:
    img_loc - address to access image to be processed

    returns:
    img - 2D array of input image
    stretch_img - 2D array of stretched image
    """
    img = imread(img_loc)
    stretched = np.asarray(rescale_intensity(img, in_range=(0, 220)),
                           dtype='uint8')
    return img, stretched


# log correction
def log_correct_img(img_loc):
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
    log_img = np.asarray(adjust_log(img, 1.25), dtype='uint8')
    return img, log_img


# reverse video
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
    reverse_img = np.asarray(util.invert(img), dtype='uint8')
    return img, reverse_img


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
    print('img')
    print(img)
    # show the image
    imshow(img, cmap=get_cmap('gray'))
    title('img')
    show()
    # equalize
    equalized = equalize_img(img)
    print('equalized')
    print(equalized)
    # show the image
    imshow(equalized, cmap=get_cmap('gray'))
    title('equalized')
    show()
    # plot histogram for original
    r, g, b = RGB(img)
    plot_rgb(r, g, b)
    # plot histogram for equalized
    r, g, b = RGB(equalized)
    plot_rgb(r, g, b)
