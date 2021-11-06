import glob
import os.path
import time
import cv2
from sift_feature.sift_query import Query_Image


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


if __name__ == "__main__":
    st = time.time()
    path = "/home/huyphuong99/Desktop/material/test/pepsicoca"
    path_img1 = f"{path}/pepsi02.jpg"
    path_img2 = f"{path}/pepsilogo10.jpg"
    path_list_img = take_list()
    path_list_img_pepsi = take_list(type_img="pepsi*")
    path_list_img_coca = take_list(type_img="coca*")
    path_file_json = "./data/file_test.json"

    logo1 = f"{path}/pepsilogo15.jpg"
    logo2 = f"{path}/pepsilogo16.jpg"
    CompareImg = Query_Image()
    img1 = read_img(logo1)
    img2 = read_img(logo2)
    CompareImg.add_logo2json(path_file_json, [img1, img2])
    # compare_two_img(logo1, logo2)
    # compare_img_logo(path_img1, path_img2)

