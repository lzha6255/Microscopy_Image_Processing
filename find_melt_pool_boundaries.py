import cv2 as cv

import canny


def threshold_weighted_edges(img):
    img_out = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Set the output image to black
    for i in range(len(img_out)):
        for j in range(len(img_out[i])):
            img_out[i][j] = 0

    for thresh in range(0, 101):
        canny_img = canny.canny_img(img, thresh)
        canny_img = cv.cvtColor(canny_img, cv.COLOR_BGR2GRAY)
        # Color by threshold with the highest threshold lines the brightest
        for i in range(len(img_out)):
            for j in range(len(img_out[i])):
                if canny_img[i][j] > 0:
                    img_out[i][j] = thresh

    return img_out


def melt_pool_boundaries(weighted_edges, min_area):
    # Colors of the melt pools. B channel is always non-zero for sake of algorithm below
    colouring = [[255, 0, 0], [1, 255, 0], [1, 0, 255], [255, 255, 0]]
    colour = 0
    img_out = weighted_edges.copy()
    for i in range(len(weighted_edges)):
        for j in range(len(weighted_edges[i])):
            img_out[i][j] = 0
    img_out = cv.cvtColor(img_out, cv.COLOR_GRAY2BGR)
    # Loop until we get to a pixel that is not an edge and also not already attributed to a melt pool.
    for i in range(len(weighted_edges)):
        for j in range(len(weighted_edges[i])):
            print("Seed point: (" + str(i) + ", " + str(j) + ")")
            if weighted_edges[i][j] > 0 or img_out[i][j][0] > 0:
                continue
            thresh = 0
            pixel_count = 1
            # Array of pixels that belong in this particular melt pool
            pixels = [[i, j]]
            # Expand the melt pool until it is above the minimum area bound
            # Raising threshold
            # Expand until the area under the current threshold is filled
            space = True
            while space and pixel_count < min_area:
                thresh = thresh + 1
                print(pixels)
                # Temporary copy of current melt pool pixels to avoid looping issues
                pixels_ = pixels.copy()
                # Assume there is no more space
                space = False
                for pixel in pixels_:
                    # Try to expand into the 3 x 3 square around each pixel
                    for m in range(-1, 2):
                        for n in range(-1, 2):
                            # Continue if the pixel is out of bounds
                            if pixel[0] + m < 0 or pixel[0] + m > len(weighted_edges) - 1 or pixel[1] + n < 0 or pixel[1] + n > len(weighted_edges[0]) - 1:
                                continue
                            # Continue if the neighbouring pixel is already in this melt pool
                            if [pixel[0]+m, pixel[1]+n] in pixels:
                                continue
                            # Continue if the neighbouring pixel is already attributed to another melt pool
                            if img_out[pixel[0]+m][pixel[1]+n][0] > 0:
                                continue
                            # Continue if the neighbouring pixel is an edge that is greater than the threshold
                            if weighted_edges[pixel[0]+m][pixel[1]+n] > thresh:
                                continue
                            # Attribute the neighbouring pixel to this melt pool
                            pixels.append([pixel[0]+m, pixel[1]+n])
                            pixel_count = pixel_count + 1
                            # There was space for another pixel
                            space = True
                if not space:
                    print("No room to expand")

            # Colour the melt pool area that was found
            print("Isolating Melt Pool at Threshold " + str(thresh))
            for pixel in pixels:
                img_out[pixel[0]][pixel[1]] = colouring[colour]
            # Switch to next colour
            colour = (colour + 1) % len(colouring)
    return img_out
