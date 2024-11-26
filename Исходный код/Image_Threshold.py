import cv2
import numpy as np

def equi_threshold(image, block_size=15):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    half_window = block_size // 2
    height, width = image.shape
    output = np.zeros_like(image)
    for y in range(half_window, height - half_window):
        for x in range(half_window, width - half_window):
            window = image[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
            mean_val = np.mean(window)
            if image[y, x] >= mean_val:
                output[y, x] = 255
            else:
                output[y, x] = 0
    return output

def bernsen_thresholding(image, block_size=15, k=0.15):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    half_window = block_size // 2
    height, width = image.shape
    output = np.zeros_like(image)
    for y in range(half_window, height - half_window):
        for x in range(half_window, width - half_window):
            window = image[y - half_window:y + half_window + 1, x - half_window:x + half_window + 1]
            min_val = np.min(window).astype(np.float64)
            max_val = np.max(window).astype(np.float64)
            mean_val = np.float64(min_val + max_val) / 2
            if image[y, x] > mean_val + k * (max_val - min_val):
                output[y, x] = 255
            else:
                output[y, x] = 0
    return output