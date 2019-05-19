import json
import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import time
import matplotlib.pyplot as plt


sift = cv2.xfeatures2d.SIFT_create()
threshold = 70
rate = 0.65

start = time.time()

def query_img(link, data):
    result_link = []
    result_key = []
    result_lenth = []

    img = cv2.imread(link) #cv2.IMREAD_GRAYSCALE
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
                key_matched = matching(kp_query, des_query, keypoint, des)
                if key_matched != -1:
                    result_key.append(key)
                    result_lenth.append(key_matched)
                    break
            except:
                continue

    sort = list(np.argsort(result_lenth))
    sort.reverse()
    for i in sort:
        result_link.append(result_key[i])
    return result_link

def matching(kp1, des1, kp2, des2):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)


    good = []
    for m, n in matches:
        if m.distance < rate * n.distance:
            good.append([m])

    # print(len(good))

    # # get all key point matched with query
    # kp_matches = []
    # for m in good:
    #     kp_matches.append(kp2[m.trainIdx].pt)
    #
    # # clustering kp to elim incorect keypoint
    # eps = 5
    # min_point = 2
    # kp_filted = DBSCAN(kp_matches, eps=eps, min_samples=min_point)
    # matches_filted = []
    # for i, value in enumerate(kp_filted):
    #     if value != -1:
    #         matches_filted.append(matches[i])

    # print(matches_filted)
    if len(good) > threshold:
        return len(good)
    else:
        return -1


def match_and_box(img_path_1, img_path_2):
    img1 = cv2.imread(img_path_1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img_path_2, cv2.IMREAD_GRAYSCALE)

    sift = cv2.xfeatures2d.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    x = []
    for m, n in matches:
        # print(m)
        x.append(kp2[m.trainIdx].pt)

    kp_filted = DBSCAN(eps=5, min_samples=2).fit_predict(x)
    matches_2 = []
    for i, value in enumerate(kp_filted):
        if value != -1:
            matches_2.append(matches[i])

    # img2 = cv2.drawKeypoints(img2, kp2_, img2)
    #
    # plt.imshow(img2)
    # plt.show()

    good = []
    for m, n in matches:
        good.append(m)
        # if m.distance < 0.7*n.distance:
        #     good.append(m)

    matching_result = cv2.drawMatches(img1, kp1, img2, kp2, good, None, flags=2)
    #
    plt.imshow(matching_result, cmap='gray')
    plt.savefig('static/imgs/matched_kp.png')

    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        matchesMask = None

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)

    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
    plt.imshow(img3, 'gray')
    plt.savefig('static/imgs/matched_kp_filted.png')
