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
-q --quiet     No GUI, [default: False]

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


def computeGradientNormals(I_32F, sigma=10.0):
    h, w = I_32F.shape

    I_32F_blur = cv2.GaussianBlur(I_32F, (0, 0), sigma)

    gx = cv2.Sobel(I_32F_blur, cv2.CV_64F, 1, 0, ksize=11)
    gy = cv2.Sobel(I_32F_blur, cv2.CV_64F, 0, 1, ksize=11)

    N_32F = np.zeros((h, w, 3), dtype=np.float32)

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
    N_32F = cv2.GaussianBlur(N_32F, (0, 0), sigma)
    N_32F = normalizeImage(N_32F)

    return N_32F


def estimateNormal(I_32F):
    N_32F = computeGradientNormals(I_32F)

    return N_32F


def showResult(C_8U, I_32F, N_32F, A_8U):
    logger.info("showResult")
    plt.subplot(131)
    plt.title('Original Color')
    plt.imshow(C_8U)

    plt.subplot(132)
    plt.title('Luminance')
    plt.imshow(I_32F, cmap=plt.cm.gray)

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
    N_32F = estimateNormal(I_32F)

    if output_file:
        saveResult(input_file, A_8U, N_32F)

    if quiet:
        return

    showResult(C_8U, I_32F, N_32F, A_8U)

if __name__ == '__main__':
    args = docopt(__doc__)

    if args['<input>']:
        input_file = args['<input>']
    else:
        input_file = dataFile("ThreeBox")

    output_file = args['--output']
    quiet = args['--quiet']
    main(input_file, output_file, quiet)