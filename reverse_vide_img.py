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
    print('img size: {}' .format(size(img)))
    reverse_img = np.asarray(adjust_log(img, 1.25), dtype='uint8')
    return img, log_img


if __name__ == "__main__":
    img, log_img = log_correct_img('image_0008.jpg')
    plt.imsave('stretched_image.jpg', log_img)
    fig = plt.figure(figsize=(8, 5))
    subplot(221)
    imshow(img, cmap=get_cmap('gray'))
    title('Original')
    subplot(222)
    hist(img.flatten(), 256, range=(0, 256))
    title('Histogram of original')
    subplot(223)
    imshow(log_img, cmap=get_cmap('gray'))
    title('Log Corrected')
    subplot(224)
    hist(log_img.flatten(), 256, range=(0, 256))
    title('Histogram of Log Corrected')
    fig.tight_layout()
    show()
