import numpy as np
import cv2
from scipy.interpolate import RectBivariateSpline
from concurrent.futures import ProcessPoolExecutor as PPE
import sys

PATH = str(sys.argv[1])
MAGNIFICATION = float(sys.argv[2])

img = cv2.imread(PATH)
# get the height and width of the image
height = img.shape[0]
width = img.shape[1]

# get the blue channel
blue = img[:, :, 0]
x = np.arange(0, width)
y = np.arange(0, height)
blue_func = RectBivariateSpline(y, x, blue)

# get the green channel
green = img[:, :, 1]
x = np.arange(0, width)
y = np.arange(0, height)
green_func = RectBivariateSpline(y, x, green)

# get the red channel
red = img[:, :, 2]
x = np.arange(0, width)
y = np.arange(0, height)
red_func = RectBivariateSpline(y, x, red)


magnified_height = round(height * MAGNIFICATION)
magnified_width = round(width * MAGNIFICATION)
tolerance = 1.0 / MAGNIFICATION

# 画像生成
def ImageGenerator(i):
    row = np.zeros((1, magnified_width, 3), np.uint8)
    for j in np.arange(0, width, tolerance):
        row[0, round(j * MAGNIFICATION), 0] = blue_func(i, j)
        row[0, round(j * MAGNIFICATION), 1] = green_func(i, j)
        row[0, round(j * MAGNIFICATION), 2] = red_func(i, j)
    return row

img = np.concatenate(
    list(PPE().map(ImageGenerator, np.arange(0, height, tolerance))), axis=0
)

cv2.imwrite("generated.png", img)
print("generation success")
