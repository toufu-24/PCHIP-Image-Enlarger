import numpy as np
from scipy.interpolate import PchipInterpolator as pchip
from concurrent.futures import ProcessPoolExecutor as PPE
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
import math

PATH = "READMEcomponents/Mandrill/Mandrill.jpg"

img = cv2.imread(PATH)
# ４倍だけ拡大する
new_img = np.zeros((img.shape[0] * 4, img.shape[1] * 4, 3), dtype=np.uint8)
for i in tqdm(range(img.shape[0])):
    for j in range(img.shape[1]):
        new_img[i * 4, j * 4] = img[i, j]
        new_img[i * 4 + 1, j * 4] = img[i, j]
        new_img[i * 4, j * 4 + 1] = img[i, j]
        new_img[i * 4 + 1, j * 4 + 1] = img[i, j]
        new_img[i * 4 + 2, j * 4] = img[i, j]
        new_img[i * 4 + 3, j * 4] = img[i, j]
        new_img[i * 4 + 2, j * 4 + 1] = img[i, j]
        new_img[i * 4 + 3, j * 4 + 1] = img[i, j]
        new_img[i * 4, j * 4 + 2] = img[i, j]
        new_img[i * 4, j * 4 + 3] = img[i, j]
        new_img[i * 4 + 1, j * 4 + 2] = img[i, j]
        new_img[i * 4 + 1, j * 4 + 3] = img[i, j]
        new_img[i * 4 + 2, j * 4 + 2] = img[i, j]
        new_img[i * 4 + 3, j * 4 + 2] = img[i, j]
        new_img[i * 4 + 2, j * 4 + 3] = img[i, j]
        new_img[i * 4 + 3, j * 4 + 3] = img[i, j]
img = new_img
cv2.imwrite("read.png", img)
print("generation success")
