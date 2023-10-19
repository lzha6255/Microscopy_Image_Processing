import sobel
import canny


if __name__ == '__main__':
    ebsd_scan = "images\\A.tif"
    canny.canny(ebsd_scan, 50)
    sobel.sobel(ebsd_scan)
