# -*- coding: utf-8 -*-
## @package npr_sfs.methods.lumo
#
#  Lumo [Johnston et al. 2002].
#  @author      tody
#  @date        2015/07/29

"""Usage: lumo.py [<input>] [-h] [-o] [-q]

<input>        Input image.
-h --help      Show this help.
-o --output    Save output files. [default: False]
-q --quiet     No GUI. [default: False]

"""
from docopt import docopt
import numpy as np
import cv2
import pyamg
from pyamg.gallery import laplacian

import matplotlib.pyplot as plt

from npr_sfs.io.image import loadAlpha, saveRGBA, saveGray, saveNormal
from npr_sfs.cv.normal import normalToColor
from npr_sfs.util.timer import timing_func
from npr_sfs.np.norm import normalizeVectors
from npr_sfs.plot.window import showMaximize

from npr_sfs.datasets.loader import dataFile

from npr_sfs.util.logger import getLogger
logger = getLogger(__name__)


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

    N_32F[:, :, 0] = wgxy[:, :] * N_32F[:, :, 0]
    N_32F[:, :, 1] = wgxy[:, :] * N_32F[:, :, 1]

    return N_32F


## Normal constraints from the alpha mask and the initial normal.
def normalConstraints(A_8U, N0_32F, alpha_th=20, w_sil=1e+10):
    h, w = A_8U.shape

    L = laplacian.poisson((h, w))
    L_lil = L.tolil()

    A_flat = A_8U.flatten()
    sil_ids = np.where(A_flat < alpha_th)

    for sil_id in sil_ids:
        L_lil[sil_id, sil_id] = w_sil

    A = L_lil.tocsr()

    N0_flat = N0_32F.reshape(h * w, 3)
    N0_flat[A_flat > alpha_th, :] = 0.0
    b = w_sil * N0_flat

    return A, b


def solveMG(A, b):
    ml = pyamg.smoothed_aggregation_solver(A)

    x = np.zeros(b.shape)
    for bi in range(3):
        x[:, bi] = ml.solve(b[:, bi], tol=1e-10)
    return x


def estimateNormal(A_8U):
    h, w = A_8U.shape
    N0_32F = computeSilhouetteNormal(A_8U)
    A, b = normalConstraints(A_8U, N0_32F)

    N_flat = solveMG(A, b)
    N_flat = normalizeVectors(N_flat)
    N_32F = N_flat.reshape(h, w, 3)

    return N0_32F, N_32F


def showResult(A_8U, N0_32F, N_32F):
    logger.info("showResult")

    plt.subplot(131)
    plt.title('Alpha Mask')
    plt.imshow(A_8U)

    plt.subplot(132)
    plt.title('Initial Normal')
    plt.imshow(normalToColor(N0_32F))

    plt.subplot(133)
    plt.title('Estimated Normal')
    plt.imshow(normalToColor(N_32F, A_8U))
    showMaximize()


def saveResult(input_file, A_8U, N_32F):
    logger.info("saveResult")

    N_file = input_file.replace(".png", "_N.png")
    saveNormal(N_file, N_32F, A_8U)


def main(input_file, output_file, quiet):
    A_8U = loadAlpha(input_file)
    N0_32F, N_32F = estimateNormal(A_8U)

    if output_file:
        saveResult(input_file, A_8U, N_32F)

    if quiet:
        return

    showResult(A_8U, N0_32F, N_32F)

if __name__ == '__main__':
    args = docopt(__doc__)

    if args['<input>']:
        input_file = args['<input>']
    else:
        input_file = dataFile("ThreeBox")

    output_file = args['--output']
    quiet = args['--quiet']

    main(input_file, output_file, quiet)