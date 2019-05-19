import cv2
import matplotlib.pyplot as plt
from scipy.misc import imread
import numpy as np
from sklearn.cluster import DBSCAN

def dbscan(D, eps, minpts):
        return DBSCAN(eps=eps, min_samples=minpts).fit_predict(D)

img1 = cv2.imread('test/test2.PNG', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('test/test.jpg', cv2.IMREAD_GRAYSCALE)



sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(des1, des2)
# print(matches[0])

matches = sorted(matches, key = lambda x:x.distance)
matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, flags=2)
# img = cv2.drawKeypoints(img, keypoints, None)

# plt.imshow(matching_result, cmap='gray')
# plt.show()

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)


x = []
for m, n in matches:
    # print(m)
    x.append(kp2[m.trainIdx].pt)

kp_filted = dbscan(x, 5, 2)
matches_2 = []
for i, value in enumerate(kp_filted):
    if value != -1:
        matches_2.append(matches[i])



# img2 = cv2.drawKeypoints(img2, kp2_, img2)
#
# plt.imshow(img2)
# plt.show()



good = []
for m,n in matches:
    good.append(m)
    # if m.distance < 0.7*n.distance:
    #     good.append(m)

matching_result = cv2.drawMatches(img1, kp1, img2, kp2, good, None, flags=2)
#
plt.imshow(matching_result, cmap='gray')
plt.show()

MIN_MATCH_COUNT = 10
if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)


img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
plt.imshow(img3, 'gray'),plt.show()
