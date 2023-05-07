import numpy as np
import cv2
from PIL import Image
import math
import time
def shi_tomasi_corner(image):
    start_time = time.time()

    img = cv2.imread(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    number_of_points = 30
    neighborhood = 3
    threshold = 0.01

    corners = cv2.goodFeaturesToTrack(gray, number_of_points, threshold, 10)

    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 4, 255, -1)

    runtime = time.time() - start_time

    return img, number_of_points, str(neighborhood), threshold, round(runtime, 2)

def harris_corner(image):
    start_time = time.time()

    threshold = 0.01
    img = cv2.imread(image)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    neighborhood = 4

    dst = cv2.cornerHarris(gray, neighborhood, 3, 0.01)
    corner_map = dst[dst > threshold * dst.max()]

    number_of_points = np.count_nonzero(corner_map)

    img[dst > threshold * dst.max()] = [255, 0, 0]

    runtime = time.time() - start_time

    return img, number_of_points, str(neighborhood), threshold, round(runtime, 2)


def FAST_corner(image):
    start_time = time.time()
    img = cv2.imread(image)

    fast = cv2.FastFeatureDetector_create()

    key_points = fast.detect(img, None)


    threshold = fast.getThreshold()

    neighborhood = fast.getType()
    number_of_points = len(key_points)

    img = cv2.drawKeypoints(img, key_points, None, (255, 0, 0))

    runtime = time.time() - start_time

    return img, number_of_points, str(neighborhood), threshold, round(runtime, 2)

def moravec_corner(image):
    start_time = time.time()
    threshold = 100
    img = Image.open(image).convert("L")

    output_img = cv2.cvtColor(cv2.imread(image, 0), cv2.COLOR_GRAY2RGB)

    xy_shifts = [(1, 0), (1, 1), (0, 1), (-1, 1)]

    neighborhood_px = 4
    number_of_points = 0
    for y in range(1, img.size[1] - 1):
        for x in range(1, img.size[0] - 1):
            E = 100000
            for shift in xy_shifts:
                diff = img.getpixel((x + shift[0], y + shift[1]))
                diff = diff - img.getpixel((x, y))
                diff = diff * diff
                if diff < E:
                    E = diff

            if E > threshold:
                output_img[y, x] = (255, 0, 0)
                number_of_points += 1

    runtime = time.time() - start_time

    return output_img, number_of_points, str(neighborhood_px), threshold, round(runtime, 2)

def susan_corner(image):
    start_time = time.time()

    img = Image.open(image).convert('L')

    img2 = np.array(img)
    shape1 = np.shape(img2)
    img1 = np.zeros(shape1)

    mask_radius = 3
    length = 7
    maximum = 0
    susan_mask = np.ones((7, 7))

    img1[:] = img2[:]
    z = np.zeros(shape1)

    x_min = y_min = mask_radius
    x_max = shape1[0] - mask_radius
    y_max = shape1[1] - mask_radius

    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            susan_mask[:] = img1[i-mask_radius:i+mask_radius+1, j-mask_radius:j+mask_radius+1]
            centre = mask_radius
            intensity = susan_mask[mask_radius, mask_radius]

            for m in range(0, length):
                for n in range(0, length):
                    if (m-centre)*(m-centre) + (n-centre)*(n-centre) <= mask_radius*mask_radius:
                        susan_mask[m][n] = math.exp(-math.pow(((susan_mask[m][n]-intensity)/27), 6))
                    else:
                        susan_mask[m][n] = 0

            susan_mask[mask_radius, mask_radius] = 0
            n_pixel = np.sum(susan_mask)
            z[i][j] = n_pixel
            if maximum < n_pixel:
                maximum = n_pixel

    threshold = maximum/2
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            if z[i][j] >= threshold:
                z[i][j] = 0
            else:
                z[i][j] = 1

    number_of_points = np.sum(np.nonzero(z))

    img = Image.open(image)

    output_img = Image.fromarray(z).convert("RGB")

    w, h = output_img.size

    for i in range(0, w):
        for j in range(0, h):
            if output_img.getpixel((i, j)) == (0, 0, 0):
                output_img.putpixel((i, j), img.getpixel((i, j)))
            else:
                output_img.putpixel((i, j), (255, 0, 0))

    runtime = time.time() - start_time

    return output_img, number_of_points, str(mask_radius), threshold, round(runtime, 2)


