import cv2 as cv


def img_to_file(img, name, suffix, file_type):
    file_address = ""
    for i in range(len(name)-1, 0, -1):
        if name[i] == ".":
            file_address = name[:i] + "_" + suffix + "." + file_type

    cv.imwrite(file_address, img)
