import numpy as np
import cv2
import pickle
from concurrent.futures import ProcessPoolExecutor as PPE
import sys

MAGNIFICATION = sys.argv[1]

func_file_name = "function.pkl"
with open(func_file_name, "rb") as f:
    # pklファイルからhieghtとwidthを読み込み
    height = pickle.load(f)  
    width = pickle.load(f)
    # 関数読み込み
    blue_func = pickle.load(f)
    green_func = pickle.load(f)
    red_func = pickle.load(f)

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
