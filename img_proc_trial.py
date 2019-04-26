from img_proc import equalize_img
from img_proc import contr_stretch_img
from img_proc import log_correct_img
from img_proc import reverse_img
from img_proc import RGB
from img_proc import plot_rgb

if __name__ == "__main__":
    img_loc = 'image_0008.jpg'
    img, equalized = equalize_img(img_loc)
    r,g,b = RGB(equalized)
    plot_rgb(r, g, b)
