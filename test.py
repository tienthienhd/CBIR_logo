import glob
import os.path
import time
import cv2
from sift_feature.sift_query import Query_Image


def read_img(img):
    return cv2.imread(img, cv2.IMREAD_GRAYSCALE)


def take_list(path="/home/huyphuong99/Desktop/material/test/pepsicoca", type_img="*"):
    return [path for path in glob.glob(os.path.join(path, type_img))]


def preprocessing(img1, img2):
    h1, w1, _ = img1.shape
    h2, w2, _ = img2.shape
    h, w = max(h1, h2), max(w1, w2)



def handle(path1, path2):
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


if __name__ == "__main__":
    st = time.time()
    path = "/home/huyphuong99/Desktop/material/test/pepsicoca"
    path_img1 = "/home/huyphuong99/Desktop/material/test/pepsicoca/pepsi4.jpg"
    path_img2 = "/home/huyphuong99/Desktop/material/test/pepsicoca/pepsilogo17.jpg"
    path_list_img = take_list()
    path_list_img_pepsi = take_list(type_img="pepsi*")
    path_list_img_coca = take_list(type_img="coca*")
    CompareImg = Query_Image()
    handle(path_img1, path_img2)


# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img_rgb = cv2.imread('/home/huyphuong99/Desktop/material/test/pepsicoca/pepsilogo16.jpg')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('/home/huyphuong99/Desktop/material/test/pepsicoca/pepsi08.jpg', 0)
#
# # plt.imshow(template)
# # plt.show()
# height, width = template.shape[::]
# res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# plt.imshow(res, cmap='gray')
# plt.show()
#
# threshold = 0.3 #For TM_CCOEFF_NORMED, larger values = good fit.
#
# loc = np.where(res >= threshold)
#
# for pt in zip(loc[::-1]):
#     cv2.rectangle(img_rgb, pt, (pt[0] + width, pt[1] + height), (255, 0, 0), 1)
#
# cv2.imshow("Matched image", img_rgb)
# cv2.waitKey()
# cv2.destroyAllWindows()