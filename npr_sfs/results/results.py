# -*- coding: utf-8 -*-
## @package npr_sfs.results.results
#
#  npr_sfs.results.results utility package.
#  @author      tody
#  @date        2015/09/01

import os
from npr_sfs.io_util.image import loadAlpha
from npr_sfs.datasets.loader import loadData, dataNames

_root_dir = os.path.dirname(__file__)


## Result directory.
def resultDir(batch_name=""):
    result_dir = os.path.join(_root_dir, batch_name)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir


## Result file path for file name and extension.
def resultFile(result_dir, file_name, file_ext=".png"):
    result_file = os.path.join(result_dir, file_name + file_ext)
    return result_file


## Batch command for the target data names, ids.
#
#  @param batch_func batch_func(image_file) for an image file.
#  @param batch_name batch command name.
def batchResults(batch_func, batch_name):
    data_names = dataNames()
    for data_name in data_names:
        print "%s: %s" % (batch_name, data_name)
        batch_func(data_name)


if __name__ == '__main__':
    print resultDir()
    print resultFile("testImage")