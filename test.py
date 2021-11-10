import glob
import os.path
import time

import cv2

from sift_query import QueryImage


def read_img(img):
    return cv2.imread(img, cv2.IMREAD_GRAYSCALE)


def take_list(path="/home/huyphuong99/Desktop/material/test/pepsicoca", type_img="*"):
    return [path for path in glob.glob(os.path.join(path, type_img))]


def compare_img_logo(path1, path2):
    if os.path.exists(path1):
        img1 = read_img(path1)

    if isinstance(path2, str):
        img2 = read_img(path2)
        a = CompareImg.match_box(img1, img2)
        print(f"Result: {a}")
    elif isinstance(path2, list):
        count = 0
        for i, p in enumerate(path_list_img_pepsi):
            img = read_img(p)
            a = CompareImg.match_box(img1, img)
            if a[0]:
                count += 1
            if i == 10:
                break
        _time, total_img = time.time() - st, len(path_list_img_pepsi) + 1
        print("-" * 50)
        print(f"Image is True: {count}|{total_img}, Totqal time: {_time}, Average time each image:{_time / total_img}")


def compare_two_img(path1, path2):
    if os.path.exists(path1) and os.path.exists(path2):
        img1 = read_img(path1)
        img2 = read_img(path2)
    else:
        raise print("Either path does not exist")
    CompareImg.check_two_img(img1, img2)


def add2json(path_logo1, path_logo2):
    path_file_json = "file_keypoint.json"
    logo1 = read_img(path_logo1)
    logo2 = read_img(path_logo2)
    CompareImg.add_logo2json([logo1, logo2], "coca")


if __name__ == "__main__":
    st = time.time()
    CompareImg = QueryImage()
    path = "/home/huyphuong99/Desktop/material/test/pepsicoca"
    path_img1 = f"{path}/pepsi02.jpg"
    path_img2 = f"{path}/pepsi8.jpg"
    path_list_img = take_list()
    path_list_img_pepsi = take_list(type_img="pepsi*")
    compare_img_logo(path_img1, path_img2)
