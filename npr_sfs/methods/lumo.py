

# -*- coding: utf-8 -*-
## @package npr_sfs.lumo
#
#  Implementation of Lumo [Johnston et al. 2002].
#  @author      tody
#  @date        2015/07/29

"""Usage: lumo.py <input> [-h] [-o output] [--quiet]

<input>      input image.
-h --help    show this
-o output    specify output file [default: ./lumo.png]
--quiet      No GUI, [default: False]

"""
from docopt import docopt
import numpy as np
import cv2
import pyamg
from pyamg.gallery import laplacian

import matplotlib.pyplot as plt

from npr_sfs.io.image import loadAlpha
from npr_sfs.cv.normal import normalToColor
from npr_sfs.util.timer import timing_func
from npr_sfs.np.norm import normalizeVectors

from npr_sfs.datasets.loader import loadData


## Silhouette normal from the alpha mask.
def computeSilhouetteNormal(A_8U, sigma=7.0):
    height, width = A_8U.shape[0], A_8U.shape[1]

    A_8U_blur = cv2.GaussianBlur(A_8U, (0, 0), width * sigma / 1024.0)
    A_8U_blur = (1.0 / 255.0) * np.float32(A_8U_blur)

    gx = cv2.Sobel(A_8U_blur, cv2.CV_64F, 1, 0, ksize=5)
    gy = cv2.Sobel(A_8U_blur, cv2.CV_64F, 0, 1, ksize=5)

    N_32F = np.zeros((height, width, 3), dtype=np.float32)

    N_32F[:, :, 0] = -gx
    N_32F[:, :, 1] = gy
    N_32F[:, :, 2] = A_8U_blur

    gxy_norm = np.zeros((height, width))

    gxy_norm[:, :] = np.sqrt(gx[:, :] * gx[:, :] + gy[:, :] * gy[:, :])

    Nxy_norm = np.zeros((height, width))
    Nxy_norm[:, :] = np.sqrt(1.0 - A_8U_blur[:, :])

    wgxy = np.zeros((height, width))
    wgxy[:, :] = Nxy_norm[:, :] / (0.001 + gxy_norm[:, :])

    #N = wgxy * N
    N_32F[:, :, 0] = wgxy[:, :] * N_32F[:, :, 0]
    N_32F[:, :, 1] = wgxy[:, :] * N_32F[:, :, 1]

    return N_32F


def makeConstraints(A_8U, alpha_th=20, w_cons=1e+10):
    N0_32F = computeSilhouetteNormal(A_8U)

    h, w = A_8U.shape

    L = laplacian.poisson((h, w))
    L_lil = L.tolil()

    A_flat = A_8U.flatten()
    silhouette_ids = np.where(A_flat < alpha_th)

    for silhouette_id in silhouette_ids:
        #L_lil[silhouette_id, :] = 0.0
        L_lil[silhouette_id, silhouette_id] = w_cons

    A = L_lil.tocsr()

    N0_flat = N0_32F.reshape(h * w, 3)
    N0_flat[A_flat > alpha_th, :] = 0.0
    b = w_cons * N0_flat

    return A, b, N0_32F


@timing_func
def solvePyamg(A, b):
    ml = pyamg.smoothed_aggregation_solver(A)

    x = np.zeros(b.shape)
    for bi in range(3):
        x[:, bi] = ml.solve(b[:,bi], tol=1e-10)
    return x


def lumoAlphaMask(A_8U):
    h, w = A_8U.shape
    A, b, N0_32F = makeConstraints(A_8U)

    N_flat = solvePyamg(A, b)
    N_flat = normalizeVectors(N_flat)
    N_32F = N_flat.reshape(h, w, 3)

    plt.subplot(131)
    plt.title('Alpha Mask')
    plt.imshow(A_8U)

    plt.subplot(132)
    plt.title('Initial Normal')
    plt.imshow(normalToColor(N0_32F))

    plt.subplot(133)
    plt.title('Estimate Normal')
    plt.imshow(normalToColor(N_32F, A_8U))
    plt.show()

    return A_8U


def lumoFile(file_path):
    A_8U = loadAlpha(file_path)
    lumoAlphaMask(A_8U)

if __name__ == '__main__':
#     args = docopt(__doc__,'TreeBox --quiet=True')
#     print args.get('--quiet')
    import sys
    if len(sys.argv) > 1:
        lumoFile(sys.argv[1])
    else:
        A_8U = loadData("ThreeBox")
        lumoAlphaMask(A_8U)
