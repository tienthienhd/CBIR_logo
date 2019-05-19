import cv2
import numpy
import matplotlib.pyplot as plt

sift = cv2.xfeatures2d.SIFT_create()

def read_img(file):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    return img

def get_subimg(img, bboxes):
    result = []
    for x, y, w, h in bboxes:
        x1 = int(x)
        x2 = int(x + w)
        y1 = int(y)
        y2 = int(y + h)
        result.append(img[y1:y2, x1:x2])
    return result

def get_features(list_img):

    for img in list_img:
        kp, des = sift.detectAndCompute(img, None)


def show(img):
    plt.imshow(img)
    plt.show()

# sub = get_subimg(read_img('data/images/adidas/000001.jpg'), [[427, 284,  87,  81],[167, 396,  61,  97]])
# show(sub[1])




img = cv2.imread('data/images/adidas/000001.jpg', cv2.IMREAD_GRAYSCALE)

img1 = img[284: 284+81, 427:427 + 87]
img2 = img[396:396+97, 167:167+61]


sift = cv2.xfeatures2d.SIFT_create(nfeatures=0, nOctaveLayers=3, contrastThreshold=0.04, edgeThreshold=10, sigma=1.6)
# surf = cv2.xfeatures2d.SURF_create()
# orb = cv2.ORB_create(nfeatures=1500)

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
print(len(des1))
print(len(des2))

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(des1, des2)

matches = sorted(matches, key = lambda x:x.distance)
matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:5], None, flags=2)
# img = cv2.drawKeypoints(img, keypoints, None)

plt.imshow(matching_result, cmap='gray')
plt.show()
#
