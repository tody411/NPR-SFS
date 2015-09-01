# -*- coding: utf-8 -*-
## @package npr_sfs.results.ibme
#
#  npr_sfs.results.ibme utility package.
#  @author      tody
#  @date        2015/09/01


from npr_sfs.results.results import batchResults, resultFile, resultDir

from npr_sfs.io_util.image import saveNormal, loadRGBA
from npr_sfs.datasets.loader import loadData
from npr_sfs.cv.image import alpha, luminance
from npr_sfs.methods.ibme import estimateNormal

batch_name = "IBME"


def batch_func(data_name):
    C_8U = loadData(data_name, loader_func=loadRGBA)
    A_8U = alpha(C_8U)
    I_32F = luminance(C_8U)
    N_32F, D_32F = estimateNormal(I_32F)

    result_dir = resultDir(batch_name)
    N_file = resultFile(result_dir, data_name)
    saveNormal(N_file, N_32F, A_8U)


if __name__ == '__main__':
    batchResults(batch_func, batch_name)
