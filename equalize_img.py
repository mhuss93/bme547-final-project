from matplotlib.pyplot import imread, imshow, show, subplot, title, get_cmap, hist
from skimage.exposure import equalize_hist
import numpy as np
import matplotlib.pyplot as plt

# histogram equalization
def equalize_img(img_loc):
    """
    Take address of image to be processed as img_loc.
    Computes equalization and returns both the input img and equalized img.

    param:
    img_loc - address to access image to be processed

    returns:
    img - 2D array of input image
    eq - 2D array of equalized image
    """
    img = imread(img_loc)
    eq = np.asarray(equalize_hist(img)*255, dtype= 'uint8')
    return img, eq


if __name__ == "__main__":

    img, eq_img = equalize_img('image_0001.jpg')
    plt.imsave('equalized_image.jpg', eq_img)
    subplot(221); imshow(img, cmap= get_cmap('gray')); title('Original')
    subplot(222); hist(img.flatten(), 256, range=(0,256)); title('Histogram of original')
    subplot(223); imshow(eq_img, cmap= get_cmap('gray')); title('Equalized')
    subplot(224); hist(eq_img.flatten(), 256, range=(0,256)); title('Histogram of equalized')
    show()
