import numpy as np
import cv2 as cv

import sobel
import canny
import img_to_file


def canny_array(img, x, y, step, low_thresh):
    font = cv.FONT_HERSHEY_PLAIN
    org = (10, 50)
    font_scale = 3
    color = (255, 255, 0)
    thickness = 2

    img_out = []
    thresh = low_thresh - step          # A step will be taken before the first canny edge detect
    for i in range(y):
        row = []
        if i == 0:
            row = cv.putText(img.copy(), "Original", org, font, font_scale, color, thickness, cv.LINE_AA)
        else:
            dst = canny.canny_img(img, thresh)
            row = cv.putText(dst, str(thresh), org, font, font_scale, color, thickness, cv.LINE_AA)
        for j in range(1, x):
            thresh = thresh + step
            dst = canny.canny_img(img, thresh)
            labelled = cv.putText(dst, str(thresh), org, font, font_scale, color, thickness, cv.LINE_AA)
            row = np.concatenate((row, labelled), axis=1)
        if i == 0:
            img_out = row
        else:
            img_out = np.concatenate((img_out, row), axis=0)
        thresh = thresh + step
    return img_out

if __name__ == '__main__':
    ebsd_scan = "images\\A.tif"
    sobel.sobel(ebsd_scan)
    ebsd_img = cv.imread(ebsd_scan, cv.IMREAD_COLOR)
    img_to_file.img_to_file(canny_array(ebsd_img, 4, 3, 5, 10), ebsd_scan, "matrix", "png")
