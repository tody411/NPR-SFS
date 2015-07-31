
# -*- coding: utf-8 -*-
## @package npr_sfs.cv.normal
#
#  Normal image functions.
#  @author      tody
#  @date        2015/07/29

import numpy as np
import cv2

from npr_sfs.cv.image import rgb, to32F, to8U, setAlpha, alpha
from npr_sfs.np.norm import normalizeVectors
from npr_sfs.util.timer import timing_func


## RGBA to normal.
@timing_func
def colorToNormal(C_8U):
    rgb_8U = rgb(C_8U)
    A_8U = alpha(C_8U)

    C_32F = to32F(rgb_8U)

    N_32F = 2.0 * C_32F - 1.0

    N_32F = cv2.bilateralFilter(N_32F, 5, 0.1, 5)

    N_32F[A_8U < 10, :] = np.array([0.0, 0.0, 0.0])

    N_32F_normalized = normalizeImage(N_32F)

    return N_32F_normalized


## Normal to RGB.
def normalToColor(N_32F, A_8U=None):
    C_32F = 0.5 * N_32F + 0.5
    C_8U = to8U(C_32F)

    if A_8U is not None:
        C_8U = setAlpha(C_8U, A_8U)

    return C_8U


## Normalize the normal image.
def normalizeImage(N_32F):
    N_flat = N_32F.reshape((-1, 3))
    N_flat_normalized = normalizeVectors(N_flat)

    N_32F_normalized = N_flat_normalized.reshape(N_32F.shape)
    return N_32F_normalized
