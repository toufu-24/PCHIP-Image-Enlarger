import numpy as np
from scipy.interpolate import RectBivariateSpline
import matplotlib.pyplot as plt
import cv2
import pickle
import sys

PATH = str(sys.argv[1])
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

func_file_name = "function.pkl"
# save the functions
with open(func_file_name, "wb") as f:
    pickle.dump(int(height), f)
    pickle.dump(int(width), f)
    pickle.dump(blue_func, f)
    pickle.dump(green_func, f)
    pickle.dump(red_func, f)

