import json
import os
from typing import List, Tuple, Dict

import cv2
import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
from sklearn.cluster import DBSCAN


class LabelNotFoundException(Exception):
    """raise if label not found in data"""
    pass


class QueryImage:
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.threshold = 15
        self.rate = .7
        self.data_path = './file_keypoint.json'
        if os.path.exists(self.data_path):
            with open(self.data_path) as json_file:
                self.data = json.load(json_file)
        else:
            self.data = {}

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
            x.append(kp2[m.trainIdx].pt)
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

    def create_file_keypoint(self, kp: List, des: List[np.ndarray], type_img: str) -> Dict:
        result = {}
        result[type_img] = {}
        result[type_img]["imgs"] = []
        for i in range(len(kp)):
            result[type_img]["imgs"].append(self.take_kp_des(kp[i], des[i]))
        return result

    def save_keypoint(self, kp1, kp2, des1, des2):
        r = self.create_file_keypoint([kp1, kp2], [des1, des2])
        test = json.dumps(r)
        with open(self.data_path, "w") as f:
            f.write(test)

    @staticmethod
    def take_inf_kp(kp):
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

    def load_file_keypoint(self, label: str):
        if label not in self.data:
            raise LabelNotFoundException(f"Not found label: {label}")
        info = self.data[label]["imgs"]
        keypoints = []
        deses = []
        for sub_inf in info:
            kp = sub_inf["kp"]
            take_kp = self.take_inf_kp(kp)
            des = np.array(sub_inf["des"])
            keypoints.append(take_kp)
            deses.append(des)
        return {
            "keypoints": keypoints,
            "deses": deses
        }

    def compare_img(self, kp1, des1, kp2, des2):
        good = self.matching(kp1, kp2, des1, des2)
        check = True
        if len(good) < self.threshold:
            check = False
        return good, check


    def add_logo2json(self, imgs, label: str):
        if not isinstance(imgs, list):
            imgs = [imgs]

        if label not in self.data:
            self.data[label] = {}
            self.data[label]["imgs"] = []

        info: list = self.data[label]["imgs"]

        for img in imgs:
            kp, des = self.get_keypoint(img)
            info.append(self.take_kp_des(kp, des))
        with open(self.data_path, 'w') as fp:
            fp.write(json.dumps(self.data))
        logger.info(f"You added a logo {label} success to file json")
        return True

    def check_img_have_logo(self, img, label):

        info_json = self.load_file_keypoint(label)
        kp, des = self.get_keypoint(img)
        # self.visualize_match_point(img, kp)
        goods, checks = [], []
        count = 0
        for i in range(len(info_json["keypoints"])):
            good, check = self.compare_img(kp, des, info_json["keypoints"][i], info_json["deses"][i])
            if check:
                count += 1
            goods.append(len(good))
        half = round(len(goods) / 2)
        if count >= half:
            logger.info(f"Image have logo, CORRECT: {count}/{len(goods)}")
            return True
        else:
            logger.info(f"Image not have logo, CORRECT:  {count}/{len(goods)}")
            return False

    def check_two_img(self, img1, img2, label):
        info_json = self.load_file_keypoint(label)
        kp1, des1 = self.get_keypoint(img1)
        kp2, des2 = self.get_keypoint(img2)
        good1, check1 = [], []
        good2, check2 = [], []
        count1, count2 = 0, 0
        for i in range(len(info_json["keypoints"])):
            good_of_kp1, check_of_kp1 = self.compare_img(kp1, des1, info_json["keypoints"][i],
                                                         info_json["deses"][i])
            good_of_kp2, check_of_kp2 = self.compare_img(kp2, des2, info_json["keypoints"][i],
                                                         info_json["deses"][i])
            # self.visualize_match_point(img1, kp1, img1, check_of_kp1, good_of_kp1)
            if check_of_kp1:
                count1 += 1
            if check_of_kp2:
                count2 += 1
            good1.append(len(good_of_kp1))
            good2.append(len(good_of_kp2))
        half = round(len(good1) / 2)
        if count1 >= half and count2 >= half:
            logger.info(f"Both pictures are of the SAME type of logo")
            return True
        else:
            logger.info(f"Both images are DIFFERENT logo")
            return False

    @staticmethod
    def visualize_keypoint(img, kp):
        result = cv2.drawKeypoints(img, kp, 0, (0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.imshow(result)
        plt.title(f"Image: | Good: {len(kp)}")
        plt.show()
