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
    def __init__(self, max_features=None, nOctaveLayers=None, contrastThreshold=None, edgeThreshold=None, sigma=None,
                 threshold=15, rate=0.7):
        self.sift = cv2.SIFT_create(nfeatures=max_features, nOctaveLayers=nOctaveLayers,
                                    contrastThreshold=contrastThreshold, edgeThreshold=edgeThreshold, sigma=sigma)
        self.threshold = threshold
        self.rate = rate
        self.data_path = './file_keypoint.json'
        if os.path.exists(self.data_path):
            with open(self.data_path) as json_file:
                try:
                    self.data = json.load(json_file)
                except:
                    logger.info("File json is Empty. Please add logo to file")
                    self.data = {}
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

    def take_kp_des(self, kp: Tuple, des: np.ndarray, img) -> Dict:
        result_dict = {}
        result_dict["kp"] = []
        for element in kp:
            result_dict["kp"].append(self.take_kp(element))
        result_dict["des"] = des.tolist()
        result_dict["img"] = img.tolist()
        return result_dict

    def create_file_keypoint(self, kp: List, des: List[np.ndarray], type_img: str, img) -> Dict:
        result = {}
        result[type_img] = {}
        result[type_img]["imgs"] = []
        for i in range(len(kp)):
            result[type_img]["imgs"].append(self.take_kp_des(kp[i], des[i], img))
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
        images = []
        for sub_inf in info:
            kp = sub_inf["kp"]
            take_kp = self.take_inf_kp(kp)
            des = sub_inf["des"]
            if "img" in sub_inf:
                img = sub_inf["img"]
                images.append(img)
            keypoints.append(take_kp)
            deses.append(des)
        return {
            "keypoints": keypoints,
            "deses": deses,
            "images": images
        }

    def compare_img(self, kp1, des1, kp2, des2):
        good = self.matching(kp1, kp2, des1, des2)
        check = False
        if len(good) >= self.threshold:
            check = True
        return good, check

    def add_logo2json(self, imgs, label: str):
        if isinstance(imgs, str):
            imgs = self.read_img(imgs)

        if not isinstance(imgs, list):
            imgs = [imgs]

        if label not in self.data:
            self.data[label] = {}
            self.data[label]["imgs"] = []

        info: list = self.data[label]["imgs"]

        for img in imgs:
            kp, des = self.get_keypoint(img)
            info.append(self.take_kp_des(kp, des, img))
        with open(self.data_path, 'w') as fp:
            fp.write(json.dumps(self.data))
        logger.info(f"You added a logo {label} success to file json")
        return True

    def check_img_have_logo(self, img, label):
        if isinstance(img, str):
            img = self.read_img(img)
        info_json = self.load_file_keypoint(label)
        kp, des = self.get_keypoint(img)
        # self.visualize_keypoint(img, kp)
        goods, checks = [], []
        count = 0
        for i in range(len(info_json["keypoints"])):
            good, check = self.compare_img(kp, des, info_json["keypoints"][i], info_json["deses"][i])
            if check:
                count += 1
            goods.append(len(good))

        logger.debug(f"List matches: {goods}")
        half = len(goods) * 0.4
        if len(goods) >= 10:
            half = 10
        if count >= half:
            logger.info(f"Image have logo, CORRECT: {count}/{len(goods)}")
            return True
        else:
            logger.info(f"Image not have logo, CORRECT:  {count}/{len(goods)}")
            return False

    def check_match_kp(self, lb, kp1, des1, kp2, des2):
        good1, check1 = [], []
        good2, check2 = [], []
        count1, count2 = 0, 0
        info_json = self.load_file_keypoint(lb)
        for i in range(len(info_json["keypoints"])):
            good_of_kp1, check_of_kp1 = self.compare_img(kp1, des1, info_json["keypoints"][i],
                                                         info_json["deses"][i])
            good_of_kp2, check_of_kp2 = self.compare_img(kp2, des2, info_json["keypoints"][i],
                                                         info_json["deses"][i])
            if check_of_kp1:
                count1 += 1
            if check_of_kp2:
                count2 += 1
            good1.append(len(good_of_kp1))
            good2.append(len(good_of_kp2))
        logger.debug(f"List matches image 1: {good1}")
        logger.debug(f"List matches image 2: {good2}")
        return count1, count2, good1

    def take_result_compare(self, lb_check, kp1, des1, kp2, des2, check_compare=False):
        count1, count2, good1 = self.check_match_kp(lb_check, kp1, des1, kp2, des2)
        half = len(good1) * .4
        if count1 >= half and count2 >= half:
            check_compare = True
        return check_compare, good1

    def check_two_img(self, img1: np.ndarray, img2: np.ndarray, lb_check=None):
        if isinstance(img1, str):
            img1 = self.read_img(img1)
        if isinstance(img2, str):
            img2 = self.read_img(img2)

        label = list(self.data.keys())
        check_compare = False

        kp1, des1 = self.get_keypoint(img1)
        kp2, des2 = self.get_keypoint(img2)
        # self.visualize_match_img(img1, kp1, img2, kp2, good)
        choose_lb = None
        if lb_check is not None:
            check_compare, good = self.take_result_compare(lb_check[0], kp1, des1, kp2, des2, check_compare)
            if check_compare:
                choose_lb = lb_check[0]
        else:
            for lb in label:
                check_compare, good = self.take_result_compare(lb, kp1, des1, kp2, des2, check_compare)
                if check_compare:
                    choose_lb = lb
                    break

        if check_compare:
            logger.info(f"Both pictures are of the SAME type of logo")
        else:
            good_couple, check_couple = self.compare_img(kp1, des1, kp2, des2)
            if check_couple:
                logger.info(f"Both pictures are of the SAME type of logo")
                return check_couple, choose_lb
            else:
                logger.info(f"Both images are DIFFERENT logo")
        logger.debug(f"Label of image: {choose_lb}")
        return check_compare, choose_lb

    @staticmethod
    def visualize_keypoint(img, kp):
        result = cv2.drawKeypoints(img, kp, 0, (0, 255, 0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        plt.imshow(result)
        plt.title(f"Image: | Total Keypoint: {len(kp)}")
        plt.show()

    @staticmethod
    def visualize_match_img(img1, kp1, img2, kp2, good):
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                           singlePointColor=None,
                           matchesMask=matchesMask,  # draw only inliers
                           flags=2)
        img = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
        plt.imshow(img)
        plt.title(f"Image matches with together, GOOD = {len(good)}")
        plt.show()

    def match_box(self, img1: np.ndarray, img2: np.ndarray):
        kp1, des1 = self.get_keypoint(img1)
        kp2, des2 = self.get_keypoint(img2)
        good, check = self.compare_img(kp1, des1, kp2, des2)
        self.visualize_match_img(img1, kp1, img2, kp2, good)
        return [check]

    def delete_logo(self, name_logo):
        if name_logo not in self.data:
            raise LabelNotFoundException(f"Not found label: {name_logo}")
        del self.data[name_logo]
        with open(self.data_path, "w") as fp:
            fp.write(json.dumps(self.data))
        logger.info(f"Logo {name_logo} is deleted out of file json")
        return True
