from scipy.ndimage.filters import gaussian_filter
from scipy import misc
import numpy as np


def scale_space(image, n_octaves=4, s=2):
    n_blur = s + 3
    k = 2 ** (1.0 / s)
    sigmas = np.zeros((n_octaves, n_blur))
    init_sigma = 2 ** (-0.5)
    for i in range(n_octaves):
        for j in range(n_blur):
            sigmas[i, j] = k ** ((2*i-1) + j)

    # resize image
    img_resize = []
    for i in range(n_octaves):
        if i == 0:
            img_resize.append(misc.imresize(image, 200, 'bilinear').astype(int))
        else:
            img_resize.append(misc.imresize(img_resize[i-1], 50, 'bilinear').astype(int))

    blured = []
    for i in range(n_octaves):
        b = []
        for j in range(n_blur):
            b.append(gaussian_filter(img_resize[0], sigmas[i, j]))
        blured.append(b)
    print(blured)


scale_space([[1, 2, 3],
             [3, 4, 5],
             [4, 5, 6]])


