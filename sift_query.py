import json
import os.path

import cv2
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict


class Query_Image:
    def __init__(self):
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.threshold = 15
        self.rate = .7
        self.data_path = 'data.json'

    def read_img(self, img):
        return cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    def convert2gray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def matching(self, kp1, kp2, des1, des2):
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, np.float32(des2), k=2)

        x = []
        for m, n in matches:
            # print(m)
            x.append(kp2[m.trainIdx].pt)
        # kp_filted = KMeans().fit_predict(x)
        kp_filted = DBSCAN(eps=5, min_samples=2).fit_predict(x)
        matches_2 = []
        for i, value in enumerate(kp_filted):
            if value != -1:
                matches_2.append(matches[i])

        good = []
        for m, n in matches_2:
            if m.distance < self.rate * n.distance:
                good.append(m)
        return good

    def get_keypoint(self, img):
        return self.sift.detectAndCompute(img, None)

    @staticmethod
    def take_kp(kp_i) -> Dict:
        dict_kp = {}
        x, y = kp_i.pt
        dict_kp["x"] = x
        dict_kp["y"] = y
        dict_kp["size"] = kp_i.size
        dict_kp["angle"] = kp_i.angle
        dict_kp["response"] = kp_i.response
        dict_kp["octave"] = kp_i.octave
        return dict_kp

    def take_kp_des(self, kp: Tuple, des: np.ndarray) -> Dict:
        result_dict = {}
        result_dict["kp"] = []
        for element in kp:
            result_dict["kp"].append(self.take_kp(element))
        result_dict["des"] = des.tolist()
        return result_dict

    def create_file_keypoint(self, kp: List, des: List[np.ndarray], type_img: str = "pepsi") -> Dict:
        result = {}
        result[type_img] = {}
        result[type_img]["imgs"] = []
        for i in range(len(kp)):
            result[type_img]["imgs"].append(self.take_kp_des(kp[i], des[i]))
        return result

    def save_keypoint(self, kp1, kp2, des1, des2, path_out: str = "./data"):
        r = self.create_file_keypoint([kp1, kp2], [des1, des2])
        test = json.dumps(r)
        with open(os.path.join(path_out, "file_keypoint.json"), "w") as f:
            f.write(test)

    def take_inf_kp(self, kp):
        keypoint = []
        for sub_kp in kp:
            x = sub_kp["x"]
            y = sub_kp["y"]
            size = sub_kp["size"]
            angle = sub_kp["angle"]
            response = sub_kp["response"]
            octave = sub_kp["octave"]
            keypoint.append(cv2.KeyPoint(x, y, size=size, angle=angle, response=response, octave=octave))
        return keypoint

    def load_file_keypoint(self, file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)

        info = data["pepsi"]["imgs"]
        keypoints = []
        deses = []
        for sub_inf in info:
            kp = sub_inf["kp"]
            take_kp = self.take_inf_kp(kp)
            des = np.array(sub_inf["des"])
            keypoints.append(take_kp)
            deses.append(des)
        return keypoints, deses

    def compare_img(self, kp1, des1, kp2, des2):
        good = self.matching(kp1, kp2, des1, des2)
        check = True
        if len(good) < self.threshold:
            check = False
        return good, check

    def detect_keypoint(self, img1, img2, kp1, kp2, good):
        matchesMask = None
        if len(good) > self.threshold:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            h, w = img1.shape[:2]
            pts = np.float32([[0, 0],
                              [0, h - 1],
                              [w - 1, h - 1],
                              [w - 1, 0]]
                             ).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            # img2 = cv2.polylines(img2, [np.int32(dst)], True, (50, 50, 50), 3, cv2.LINE_AA)
        return img2, matchesMask

    def add_logo2json(self, imgs, file_json = None):
        if file_json is None:
            file_json = "./data/file_keypoint.json"
        with open(file_json) as json_file:
            data = json.load(json_file)
        info: list = data["pepsi"]["imgs"]
        if not isinstance(imgs, list):
            imgs = [imgs]
        for img in imgs:
            kp, des = self.get_keypoint(img)
            info.append(self.take_kp_des(kp, des))
        # with open(file_json, 'w') as fp:
        #     fp.write(json.dumps(data))
        print("You added a logo success to file json")

    def visualize_match_point(self, img1, kp1, img2, kp2, good):
        img2, matchesMask = self.detect_keypoint(img1, img2, kp1, kp2, good)
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img3)
        plt.title(f"Image: | Good: {len(good)}")
        plt.show()
        plt.savefig('static/imgs/matched_kp_filted.jpg')

    def check_img_have_logo(self, img):
        path_json = "./data/file_keypoint.json"
        list_kp, list_des = self.load_file_keypoint(path_json)
        kp, des = self.get_keypoint(img)
        goods, checks = [], []
        count = 0
        for i in range(len(list_kp)):
            good, check = self.compare_img(kp, des, list_kp[i], list_des[i])
            if check:
                count += 1
            goods.append(len(good))
        half = round(len(goods) / 2)
        if count >= half:
            print(f"Image have logo, CORRECT: {count}/{len(goods)}")
            return True
        else:
            print(f"Image not have logo, CORRECT:  {count}/{len(goods)}")
            return False

    def check_two_img(self, img1, img2):
        path_json = "./data/file_keypoint.json"
        list_kp, list_des = self.load_file_keypoint(path_json)
        kp1, des1 = self.get_keypoint(img1)
        kp2, des2 = self.get_keypoint(img2)
        good1, check1 = [], []
        good2, check2 = [], []
        count1, count2 = 0, 0
        for i in range(len(list_kp)):
            good_of_kp1, check_of_kp1 = self.compare_img(kp1, des1, list_kp[i], list_des[i])
            good_of_kp2, check_of_kp2 = self.compare_img(kp2, des2, list_kp[i], list_des[i])
            # self.visualize_match_point(img1, kp1, img1, check_of_kp1, good_of_kp1)
            if check_of_kp1:
                count1 += 1
            if check_of_kp2:
                count2 += 1
            good1.append(len(good_of_kp1))
            good2.append(len(good_of_kp2))
        half = round(len(good1) / 2)
        if count1 >= half and count2 >= half:
            print(f"Both pictures are of the SAME type of logo")
            return True
        else:
            print(f"Both images are DIFFERENT logo")
            return False
        print(good1, "\n", good2)
