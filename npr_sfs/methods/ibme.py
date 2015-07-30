# -*- coding: utf-8 -*-
## @package npr_sfs.methods.ibme
#
#  Image-Based Material Editing [Kahn et al. 2006].
#  @author      tody
#  @date        2015/07/30

"""Usage: ibme.py [<input>] [-h] [-o] [-q]

<input>        Input image.
-h --help      Show this help.
-o --output    Save output files. [default: False]
-q --quiet     No GUI. [default: False]

"""
from docopt import docopt

import numpy as np
import cv2

import matplotlib.pyplot as plt

from npr_sfs.datasets.loader import dataFile
from npr_sfs.io.image import loadRGBA, saveGray, saveRGBA
from npr_sfs.cv.image import luminance, alpha
from npr_sfs.plot.window import showMaximize
from npr_sfs.cv.normal import normalizeImage, normalToColor

from npr_sfs.util.logger import getLogger
logger = getLogger(__name__)


def computeGradientNormals(D_32F, sigma=5.0):
    h, w = D_32F.shape

    gx = cv2.Sobel(D_32F, cv2.CV_64F, 1, 0, ksize=1)
    gx = cv2.GaussianBlur(gx, (0, 0), sigma)

    gy = cv2.Sobel(D_32F, cv2.CV_64F, 0, 1, ksize=1)
    gy = cv2.GaussianBlur(gy, (0, 0), sigma)

    T_32F = np.zeros((h, w, 3), dtype=np.float32)
    T_32F[:, :, 0] = 1.0
    T_32F[:, :, 2] = gx

    B_32F = np.zeros((h, w, 3), dtype=np.float32)
    B_32F[:, :, 1] = 1.0
    B_32F[:, :, 2] = -gy

    T_flat = T_32F.reshape(-1, 3)
    B_flat = B_32F.reshape(-1, 3)

    N_flat = np.cross(T_flat, B_flat)
    N_32F = N_flat.reshape(h, w, 3)
    N_32F = normalizeImage(N_32F)

    return N_32F


def depthRecovery(I_32F, sigma_range=0.1, sigma_space=10,
                  w_base=0.9, w_detail=0.1):
    BL = cv2.bilateralFilter(I_32F, -1, sigma_range, sigma_space)
    DL = I_32F - BL
    D_32F = w_base * BL + w_detail * DL
    return D_32F


def estimateNormal(I_32F):
    D_32F = depthRecovery(I_32F)
    N_32F = computeGradientNormals(D_32F)

    return N_32F, D_32F


def showResult(C_8U, D_32F, N_32F, A_8U):
    logger.info("showResult")
    plt.subplot(131)
    plt.title('Original Color')
    plt.imshow(C_8U)

    plt.subplot(132)
    plt.title('Depth')
    plt.imshow(D_32F, cmap=plt.cm.gray)

    plt.subplot(133)
    plt.title('Estimated Normal')
    plt.imshow(normalToColor(N_32F, A_8U))
    showMaximize()


def saveResult(input_file, A_8U, N_32F):
    logger.info("saveResult")
    N_file = input_file.replace(".png", "_N.png")
    saveRGBA(normalToColor(N_32F, A_8U), N_file)


def main(input_file, output_file, quiet):
    C_8U = loadRGBA(input_file)
    A_8U = alpha(C_8U)
    I_32F = luminance(C_8U)
    N_32F, D_32F = estimateNormal(I_32F)

    if output_file:
        saveResult(input_file, A_8U, N_32F)

    if quiet:
        return

    showResult(C_8U, D_32F, N_32F, A_8U)

if __name__ == '__main__':
    args = docopt(__doc__)

    if args['<input>']:
        input_file = args['<input>']
    else:
        input_file = dataFile("ThreeBox")

    output_file = args['--output']
    quiet = args['--quiet']
    main(input_file, output_file, quiet)