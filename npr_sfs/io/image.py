
# -*- coding: utf-8 -*-
## @package npr_sfs.io.image
#
#  Image io functions.
#  @author      tody
#  @date        2015/07/29


import cv2
from npr_sfs.cv.image import *
from npr_sfs.cv.normal import colorToNormal, normalToColor


def loadGray(file_path):
    bgr = cv2.imread(file_path)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray


def loadRGB(file_path):
    bgr = cv2.imread(file_path)
    return bgr2rgb(bgr)


def loadRGBA(file_path):
    bgra = cv2.imread(file_path, -1)
    return bgra2rgba(bgra)


def loadAlpha(file_path):
    bgra = cv2.imread(file_path, -1)
    return alpha(bgra)


def saveRGBA(file_path, img):
    bgra = rgba2bgra(img)
    cv2.imwrite(file_path, bgra)


def saveRGB(file_path, img):
    bgr = rgb2bgr(img)
    cv2.imwrite(file_path, bgr)


def saveGray(file_path, img):
    rgbImg = rgb(img)
    cv2.imwrite(file_path, rgbImg)


def saveImage(file_path, img):
    img_8U = to8U(img)

    if len(img_8U.shape) == 2:
        saveGray(file_path, img_8U)
        return

    if img_8U.shape[2] == 3:
        saveRGB(file_path, img_8U)
        return

    if img_8U.shape[2] == 4:
        saveRGBA(file_path, img_8U)
        return


def loadNormal(file_path):
    C_8U = loadRGBA(file_path)
    A_8U = alpha(C_8U)
    C_8U = cv2.bilateralFilter(C_8U, 5, 0.1, 5)
    C_8U[:, :, 3] = A_8U
    N_32F = colorToNormal(C_8U)
    return N_32F, A_8U


def saveNormal(file_path, N_32F, A_8U=None):
    C_8U = normalToColor(N_32F, A_8U)
    saveImage(file_path, C_8U)