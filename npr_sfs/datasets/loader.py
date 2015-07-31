
# -*- coding: utf-8 -*-
## @package npr_sfs.datasets.loader
#
#  Dataset loader functions.
#  @author      tody
#  @date        2015/07/29

import os
from npr_sfs.io.image import loadAlpha

from npr_sfs.util.logger import getLogger
logger = getLogger(__name__)

data_dir = os.path.dirname(__file__)


## Data names.
def dataNames():
    images = os.listdir(data_dir)
    data_names = []

    for image in images:
        data_names.append(image.replace(".png", ""))
    return data_names


## Data file name.
def dataFile(data_name):
    img_file = os.path.join(data_dir, "%s.png" % data_name)
    logger.debug(img_file)
    return img_file


## Load data for the data name.
def loadData(data_name, loader_func=loadAlpha):
    img_file = dataFile(data_name)
    C_8U = loader_func(img_file)
    return C_8U