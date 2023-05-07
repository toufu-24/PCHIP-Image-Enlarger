import numpy as np
from scipy.interpolate import PchipInterpolator as pchip
import cv2
import sys

PATH = str(sys.argv[1])
MAGNIFICATION = float(sys.argv[2])


img = cv2.imread(PATH)
MAGNIFICATION = int(MAGNIFICATION)
print("MAGNIFICATION: ", MAGNIFICATION)
height = img.shape[0]
width = img.shape[1]

magnified_height = height * MAGNIFICATION
magnified_width = width * MAGNIFICATION
tolerance = 1.0 / MAGNIFICATION

# Duplicate the right and bottom of img by 1 pixel each
new_img = np.zeros((height + 1, width + 1, 3), dtype=np.uint8)
new_img[0:height, 0:width] = img
new_img[height, 0:width] = img[height - 1, 0:width]
new_img[0:height, width] = img[0:height, width - 1]
new_img[height, width] = img[height - 1, width - 1]
img = new_img

new_height = height + 1
new_width = width + 1

# ------------horizon interpolation------------

# blue
horizon_blue_func = np.zeros(new_height, dtype=object)
for i in range(new_height):
    horizon_blue_func[i] = pchip(np.arange(0, new_width), img[i, :, 0])

# green
horizon_green_func = np.zeros(new_height, dtype=object)
for i in range(new_height):
    horizon_green_func[i] = pchip(np.arange(0, new_width), img[i, :, 1])
# red
horizon_red_func = np.zeros(new_height, dtype=object)
for i in range(new_height):
    horizon_red_func[i] = pchip(np.arange(0, new_width), img[i, :, 2])

magnified_img = np.zeros((magnified_height, magnified_width, 3), dtype=np.uint8)

for i in np.arange(0, new_height, 1):
    for j in np.arange(0, width, tolerance):
        magnified_img[i, round(j * MAGNIFICATION), 0] = horizon_blue_func[i](j)
        magnified_img[i, round(j * MAGNIFICATION), 1] = horizon_green_func[i](j)
        magnified_img[i, round(j * MAGNIFICATION), 2] = horizon_red_func[i](j)
img = magnified_img
print("finish horizon interpolation")

# ------------vertical interpolation------------

vertical_blue_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    vertical_blue_func[i] = pchip(np.arange(0, magnified_height), img[:, i, 0])

vertical_green_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    vertical_green_func[i] = pchip(np.arange(0, magnified_height), img[:, i, 1])

vertical_red_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    vertical_red_func[i] = pchip(np.arange(0, magnified_height), img[:, i, 2])

for i in np.arange(0, height, tolerance):
    for j in np.arange(0, magnified_width, 1):
        img[round(i * MAGNIFICATION), j, 0] = vertical_blue_func[j](i)
        img[round(i * MAGNIFICATION), j, 1] = vertical_green_func[j](i)
        img[round(i * MAGNIFICATION), j, 2] = vertical_red_func[j](i)
print("finish vertical interpolation")

cv2.imwrite("pchip_generated.png", img)
print("generation success")
