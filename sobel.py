import cv2 as cv

import img_to_file


def sobel(filename):
    window_name = "Sobel Operator on " + filename
    scale = 1
    delta = 0
    ddepth = -1

    src = cv.imread(filename, cv.IMREAD_COLOR)

    src = cv.GaussianBlur(src, (3, 3), 0)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    grad_x = cv.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    img_to_file.img_to_file(grad, filename, "sobel", "png")

    return grad
