import pytest
import numpy as np


# test the encode and decode funcs
black = np.zeros((100, 100, 3))
sum_black = np.sum(black)
white = np.ones((100, 100, 3))*255
sum_white = np.sum(white)


# testing reversal function with white and black squares
@pytest.mark.parametrize("img, expected", [
    (black, sum_white),
    (white, sum_black), ])
def test_encode_decode(img, expected):
    from img_proc_server import reverse_img
    # turn to string and back to img array
    reverse = reverse_img(img)
    reverse = 255-img
    print('img')
    print(img)
    print('reverse')
    print(reverse)
    summa = np.sum(reverse)
    assert summa == expected
