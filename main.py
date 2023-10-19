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
            if i == 0 and j == 1:
                blur = cv.blur(img.copy(), (3, 3))
                labelled = cv.putText(blur, "Blurred", org, font, font_scale, color, thickness, cv.LINE_AA)
                row = np.concatenate((row, labelled), axis=1)
            else:
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


def colored_threshold_overlay(img, overlay, thresh, colour):
    img_out = img.copy()
    for i in range(len(img)):
        for j in range(len(img[i])):
            print(overlay[i][j])
            if overlay[i][j] > thresh:
                img_out[i][j] = colour
    return img_out


# Gets the scale length in pixels by walking diagonally from bottom left corner until scale is reached and then walking
# left and right to determine the length of the scale. Assumes that the scale is dark on a white background.
def get_scale_length(img, thresh):
    coords = [0, len(img)-1]
    while True:
        # Take step diagonally in NE direction
        coords[0] = coords[0] + 1
        coords[1] = coords[1] - 1
        # Check if there has been a significant colour drop
        if img[coords[1]+1][coords[0]-1] - img[coords[1]][coords[0]] > thresh:
            break
    # Remember x coordinate
    x = coords[0]
    length = [0, 0]
    # Walking left
    while img[coords[1]][coords[0]-1] - img[coords[1]][coords[0]] < thresh:
        coords[0] = coords[0] - 1
        length[0] = length[0] + 1
    coords[0] = x
    # Walking right
    while img[coords[1]][coords[0]+1] - img[coords[1]][coords[0]] < thresh:
        coords[0] = coords[0] + 1
        length[1] = length[1] + 1
    print(str(length[0] + length[1] + 1) + " pixels")       # Add 1 to count the pixel that was originally intercepted


if __name__ == '__main__':
    ebsd_scan = "images\\A.tif"
    sobel.sobel(ebsd_scan)
    ebsd_img = cv.imread(ebsd_scan, cv.IMREAD_COLOR)
    ebsd_img_gray = cv.cvtColor(ebsd_img, cv.COLOR_BGR2GRAY)
    img_to_file.img_to_file(canny_array(ebsd_img, 3, 3, 3, 30), ebsd_scan, "matrix", "png")
    ebsd_edges = canny.canny_img(ebsd_img, 36)
    ebsd_edges = cv.cvtColor(ebsd_edges, cv.COLOR_BGR2GRAY)
    ebsd_overlay = colored_threshold_overlay(ebsd_img, ebsd_edges, 127, [255, 0, 0])
    img_to_file.img_to_file(ebsd_overlay, ebsd_scan, "overlay", "png")
    get_scale_length(ebsd_img_gray, 10)
