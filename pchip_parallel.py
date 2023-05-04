import numpy as np
from scipy.interpolate import PchipInterpolator as pchip
import cv2
from concurrent.futures import ProcessPoolExecutor as PPE
import sys

PATH = str(sys.argv[1])
MAGNIFICATION = int(sys.argv[2])

img = cv2.imread(PATH)

# ------------vertical interpolation------------
height = img.shape[0]
width = img.shape[1]

magnified_height = height * MAGNIFICATION
magnified_width = width * MAGNIFICATION
tolerance = 1.0 / MAGNIFICATION

# blue
vertical_blue_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_blue_func[i] = pchip(np.arange(0, width), img[i, :, 0])

# green
vertical_green_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_green_func[i] = pchip(np.arange(0, width), img[i, :, 1])

# red
vertical_red_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_red_func[i] = pchip(np.arange(0, width), img[i, :, 2])

def ImageGenerator(i):
    row = np.zeros((1, magnified_width, 3), np.uint8)
    for j in np.arange(0, width, tolerance):
        row[0, round(j * MAGNIFICATION), 0] = vertical_blue_func[i](j)
        row[0, round(j * MAGNIFICATION), 1] = vertical_green_func[i](j)
        row[0, round(j * MAGNIFICATION), 2] = vertical_red_func[i](j)
    return row
img = np.concatenate(
    list(PPE().map(ImageGenerator, np.arange(0, height))), axis=0
)

print("finish vertical interpolation")

# ------------horizon interpolation------------

horizon_blue_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_blue_func[i] = pchip(np.arange(0, height), img[:, i, 0])

horizon_green_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_green_func[i] = pchip(np.arange(0, height), img[:, i, 1])

horizon_red_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_red_func[i] = pchip(np.arange(0, height), img[:, i, 2])

def ImageGenerator(i):
    row = np.zeros((1, magnified_height, 3), np.uint8)
    for j in np.arange(0, height, tolerance):
        row[0, round(j* MAGNIFICATION), 0] = horizon_blue_func[i](j)
        row[0, round(j* MAGNIFICATION), 1] = horizon_green_func[i](j)
        row[0, round(j* MAGNIFICATION), 2] = horizon_red_func[i](j)
    return row
img = np.concatenate(
    list(PPE().map(ImageGenerator, np.arange(0, magnified_width))), axis=0
)

img = img.transpose(1, 0, 2)
print("finish horizon interpolation")

cv2.imwrite("pchip_generated.png", img)
print("generation success")
