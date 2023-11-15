import cv2 as cv

import canny
import Melt_Region


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


def melt_pool_boundaries(weighted_edges, min_area, space_threshold):
    # Colors of the melt pools. B channel is always non-zero for sake of algorithm below
    n_colours = 5
    colouring = [[255, 0, 0], [1, 255, 0], [1, 0, 255], [255, 255, 0], [255, 0, 255]]
    regions = []        # Graph of melt pool regions for distinct colouring
    region_id = -1
    # 2D array corresponding to each pixel. Stores the region to which the pixel is attributed to
    region_map = weighted_edges.copy()
    img_out = weighted_edges.copy()
    for i in range(len(weighted_edges)):
        for j in range(len(weighted_edges[i])):
            img_out[i][j] = 0
            region_map[i][j] = -1   # -1 indicates pixel has not been attributed to a melt pool/region
    img_out = cv.cvtColor(img_out, cv.COLOR_GRAY2BGR)
    # Loop until we get to a pixel that is not an edge and also not already attributed to a melt pool.
    for i in range(len(weighted_edges)):
        for j in range(len(weighted_edges[i])):
            if weighted_edges[i][j] > 0 or img_out[i][j][0] > 0:
                continue
            print("Seed point: (" + str(i) + ", " + str(j) + ")")
            thresh = 0
            pixel_count = 1
            # Array of pixels that belong in this particular melt pool
            pixels = [[i, j]]
            # Add the melt region to the graph
            regions.append(Melt_Region.MeltRegion(region_id, n_colours))
            region_id = region_id + 1
            # Expand the melt pool until it is above the minimum area
            while pixel_count < min_area:
                # Raising edge crossing threshold
                thresh = thresh + 1
                # Stop if edge crossing threshold reaches 100 but melt pool area is still not above minimum
                if thresh > 100:
                    break
                print("Counted " + str(pixel_count) + " pixels at threshold of " + str(thresh))
                # Fill the area reachable within the current edge crossing threshold
                space = True
                space_loop = 0
                space_filled_px = 0
                while space:
                    print(pixels)
                    space_loop = space_loop + 1
                    print("Space Loop " + str(space_loop))
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
                                # Continue if the neighbouring pixel is already attributed to another melt pool.
                                # Also add the connection to the graph of melt regions if it is not already connected
                                if img_out[pixel[0]+m][pixel[1]+n][0] > 0:
                                    connected_region = region_map[pixel[0]+m][pixel[1]+n]
                                    if not(regions[region_id].check_connectivity(connected_region)):
                                        # Form a two-way connection between the two regions
                                        regions[region_id].add_connection(regions[connected_region])
                                        regions[connected_region].add_connection(regions[region_id])
                                    continue
                                # Continue if the neighbouring pixel is an edge that is greater than the threshold
                                if weighted_edges[pixel[0]+m][pixel[1]+n] > thresh:
                                    continue
                                # Attribute the neighbouring pixel to this melt pool
                                pixels.append([pixel[0]+m, pixel[1]+n])
                                pixel_count = pixel_count + 1
                                space_filled_px = space_filled_px + 1
                                # There was space for another pixel
                                space = True
                    if not space:
                        print("No room to expand")
                    if space_filled_px > space_threshold:
                        break

                    # Check if the area centroid of the melt pool is still within the melt pool.
                    # If it is not then this indicates the melt pool has taken on an excessively concave shape and the
                    # threshold should be incremented.
                    x_sum = 0
                    y_sum = 0
                    for pixel in pixels:
                        x_sum = x_sum + pixel[0]
                        y_sum = y_sum + pixel[1]
                    x_centroid = int(x_sum/pixel_count)
                    y_centroid = int(y_sum/pixel_count)
                    if not([x_centroid, y_centroid] in pixels):
                        print("Melt pool centroid not within melt pool")
                        break

            # Colour the melt pool area that was found
            print("Isolating Melt Pool at Threshold " + str(thresh))
            print("Region ID: " + str(region_id))
            for pixel in pixels:
                # Label pixels as belonging to this region
                region_map[pixel[0]][pixel[1]] = region_id
                regions[region_id].set_colour()
                colour = regions[region_id].get_colour_id()
                img_out[pixel[0]][pixel[1]] = colouring[colour]
            regions[region_id].set_pixels(pixels)

    n_melt_regions = len(regions)
    avg_melt_pool_area = 0
    avg_connectivity = 0
    for region in regions:
        avg_melt_pool_area = avg_melt_pool_area + region.get_n_pixels()
        avg_connectivity = avg_connectivity + region.get_connectivity()
    avg_melt_pool_area = avg_melt_pool_area / n_melt_regions
    avg_connectivity = avg_connectivity / n_melt_regions
    print("Melt Regions Identified: " + str(n_melt_regions))
    print("Average Melt Pool Area (Pixels): " + str(avg_melt_pool_area))
    print("Average Connectivity: " + str(avg_connectivity))
    return img_out
