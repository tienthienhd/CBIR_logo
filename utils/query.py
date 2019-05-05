import json
import cv2
import numpy as np

import time



sift = cv2.xfeatures2d.SIFT_create()
threshold = 30
rate = 0.7

start = time.time()

def query_img(link, data):
    result = []
    img = cv2.imread(link, cv2.IMREAD_GRAYSCALE)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp_query, des_query = sift.detectAndCompute(img, None)
    des_query = np.array(des_query, dtype=np.float32)
    for key in data.keys():
        infor_img = data[key]
        name = infor_img["class"]
        boxes = infor_img["sub_img"]

        for box in boxes:
            kp = box["kp"]
            des = box["des"]
            des = np.array(des, dtype=np.float32)
            keypoint = []
            for k in kp:
                value_x = k["x"]
                value_y = k["y"]
                size = k["size"]
                angle = k["angle"]
                response = k["response"]
                octave = k["octave"]
                keypoint.append(
                    cv2.KeyPoint(value_x, value_y, _size=size, _angle=angle, _response=response, _octave=octave))
            try:
                if matching(des_query, des):
                    result.append(key)
                    break
            except:
                continue
    return result

def matching(des1, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < rate * n.distance:
            good.append([m])
    if len(good) > threshold:
        return True
    else:
        return False
