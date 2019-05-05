import pandas as pd
import json
import cv2
import os

sift = cv2.xfeatures2d.SIFT_create()

folder_data = "data/"

with open("data.json") as json_file:
    data = json.load(json_file)
# print(len(data.keys()))
file_dict = data['file']
name_dict = data['name']
boxes_dict = data['bboxes']

save = {}
i = 0
for key in file_dict.keys():
    filename = folder_data + file_dict[key].split("\\")[0] + "/" + file_dict[key].split("\\")[1]
    name = name_dict[key]
    box = boxes_dict[key]

    if os.path.exists(filename):
        save[filename] = {}
        save[filename]["class"] = name
        save[filename]["sub_img"] = []
        img = cv2.imread(filename)
        for b in box:
            im = img[int(b[1]):int(b[1])+int(b[3]), int(b[0]): int(b[0]) + int(b[2]),:]
            cv2.imshow("test", im)
            cv2.waitKey(0)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            kp, des = sift.detectAndCompute(im, None)
            if des is not None:
                boxes = {}
                boxes["x"] = int(b[0])
                boxes["y"] = int(b[1])
                boxes["w"] = int(b[2])
                boxes["h"] = int(b[3])
                boxes["kp"] = []
                boxes["des"] = []

                for i, k in enumerate(kp):
                    keypoint = {}
                    x, y = kp[i].pt
                    size = kp[i].size
                    angle = kp[i].angle
                    response = kp[i].response
                    octave = kp[i].octave
                    class_id = kp[i].class_id
                    keypoint["x"] = x
                    keypoint["y"] = y
                    keypoint["size"] = size
                    keypoint["angle"] = angle
                    keypoint["response"] = response
                    keypoint["octave"] = octave
                    boxes["kp"].append(keypoint)   
                    boxes["des"].append(des[i].tolist())
            save[filename]["sub_img"].append(boxes)

test = json.dumps(save)
f = open("dict_test.json", "w")
f.write(test)
f.close()


                
                



