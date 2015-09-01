# -*- coding: utf-8 -*-
## @package npr_sfs.results.lumo
#
#  npr_sfs.results.lumo utility package.
#  @author      tody
#  @date        2015/09/01
from npr_sfs.results.results import batchResults, resultFile, resultDir
from npr_sfs.methods.lumo import estimateNormal
from npr_sfs.io_util.image import saveNormal
from npr_sfs.datasets.loader import loadData

batch_name = "Lumo"


def batch_func(data_name):
    A_8U = loadData(data_name)
    N0_32F, N_32F = estimateNormal(A_8U)

    result_dir = resultDir(batch_name)
    N_file = resultFile(result_dir, data_name)
    saveNormal(N_file, N_32F, A_8U)


if __name__ == '__main__':
    batchResults(batch_func, batch_name)
