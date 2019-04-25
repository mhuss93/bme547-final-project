import matplotlib.pyplot as plt
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
from skimage.exposure import rescale_intensity
import numpy as np


# constrast stretching
def contr_str_img(img_loc):
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
    stretch = np.asarray(rescale_intensity(img, in_range=(0, 220)),
                         dtype='uint8')
    return img, stretch


if __name__ == "__main__":
    img, stretch_img = contr_str_img('image_0041.jpg')
    plt.imsave('stretched_image.jpg', stretch_img)
    fig = plt.figure(figsize=(8, 5))
    subplot(221)
    imshow(img, cmap=get_cmap('gray'))
    title('Original')
    subplot(222)
    hist(img.flatten(), 256, range=(0, 256))
    title('Histogram of original')
    subplot(223)
    imshow(stretch_img, cmap=get_cmap('gray'))
    title('Stretched')
    subplot(224)
    hist(stretch_img.flatten(), 256, range=(0, 256))
    title('Histogram of stretched')
    fig.tight_layout()
    show()
