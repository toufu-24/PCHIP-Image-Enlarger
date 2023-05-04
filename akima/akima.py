import numpy as np
from scipy.interpolate import Akima1DInterpolator as akima
import cv2
import sys

PATH = str(sys.argv[1])
MAGNIFICATION = float(sys.argv[2])


img = cv2.imread(PATH)
MAGNIFICATION = int(MAGNIFICATION)
print("MAGNIFICATION: ", MAGNIFICATION)
# ------------vertical interpolation------------
height = img.shape[0]
width = img.shape[1]

magnified_height = height * MAGNIFICATION
magnified_width = width * MAGNIFICATION
tolerance = 1.0 / MAGNIFICATION

# blue
vertical_blue_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_blue_func[i] = akima(np.arange(0, width), img[i, :, 0])

# green
vertical_green_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_green_func[i] = akima(np.arange(0, width), img[i, :, 1])

# red
vertical_red_func = np.zeros(height, dtype=object)
for i in range(height):
    vertical_red_func[i] = akima(np.arange(0, width), img[i, :, 2])

magnified_img = np.zeros((magnified_height, magnified_width, 3), dtype=np.uint8)

for i in np.arange(0, height, 1):
    for j in np.arange(0, width, tolerance):
        magnified_img[i, round(j * MAGNIFICATION), 0] = vertical_blue_func[i](j)
        magnified_img[i, round(j * MAGNIFICATION), 1] = vertical_green_func[i](j)
        magnified_img[i, round(j * MAGNIFICATION), 2] = vertical_red_func[i](j)
img = magnified_img
print("finish vertical interpolation")

# ------------horizon interpolation------------

horizon_blue_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_blue_func[i] = akima(np.arange(0, magnified_height), img[:, i, 0])

horizon_green_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_green_func[i] = akima(np.arange(0, magnified_height), img[:, i, 1])

horizon_red_func = np.zeros(magnified_width, dtype=object)
for i in range(magnified_width):
    horizon_red_func[i] = akima(np.arange(0, magnified_height), img[:, i, 2])

for i in np.arange(0, height, tolerance):
    for j in np.arange(0, magnified_width, 1):
        img[round(i * MAGNIFICATION), j, 0] = horizon_blue_func[j](i)
        img[round(i * MAGNIFICATION), j, 1] = horizon_green_func[j](i)
        img[round(i * MAGNIFICATION), j, 2] = horizon_red_func[j](i)
print("finish horizon interpolation")

cv2.imwrite("akima_generated.png", img)
print("generation success")
