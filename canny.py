import cv2 as cv

import img_to_file


def canny(filename, low_threshold):
    window_name = "Canny edge detection on " + filename
    ratio = 3
    kernel_size = 3

    src = cv.imread(filename, cv.IMREAD_COLOR)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    blur = cv.blur(gray, (3, 3))

    edges = cv.Canny(blur, low_threshold, low_threshold*ratio, kernel_size)

    mask = edges != 0

    dst = src * (mask[:, :, None].astype(src.dtype))

    img_to_file.img_to_file(dst, filename, "canny", "png")

    return dst


def canny_img(img, low_threshold):
    ratio = 3
    kernel_size = 3

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blur = cv.blur(gray, (3, 3))

    edges = cv.Canny(blur, low_threshold, low_threshold*ratio, kernel_size)

    mask = edges != 0

    dst = img * (mask[:, :, None].astype(img.dtype))

    return dst
