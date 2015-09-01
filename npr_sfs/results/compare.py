# -*- coding: utf-8 -*-
## @package npr_sfs.results.compare
#
#  npr_sfs.results.compare utility package.
#  @author      tody
#  @date        2015/09/01

import os
import matplotlib.pyplot as plt

from npr_sfs.results.results import batchResults, resultFile, resultDir
from npr_sfs.datasets.loader import loadData
from npr_sfs.io_util.image import loadRGBA
from npr_sfs.plot.window import showMaximize

batch_name="Compare"


_root_dir = os.path.dirname(__file__)


def methodNames():
    dirs = os.listdir(_root_dir)

    method_dirs = [metohd_dir for metohd_dir in dirs if os.path.isdir(metohd_dir) and metohd_dir != batch_name]
    return method_dirs


def methodDir(method_name):
    return os.path.join(_root_dir, method_name)


def methodFile(method_name, data_name):
    return os.path.join(methodDir(method_name), data_name + ".png")


def batch_func(data_name):
    method_names = methodNames()
    NO_32F = loadData(data_name, loader_func=loadRGBA)

    fig = plt.figure(figsize=(10, 4))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.05, hspace=0.1)

    font_size = 15
    fig.suptitle("NPR-SFS", fontsize=font_size)

    num_cols = len(method_names) + 1
    fig.add_subplot(1, num_cols, 1)
    plt.title("Ground truth", fontsize=font_size)
    plt.imshow(NO_32F)
    plt.axis('off')

    col_id = 2

    for method_name in method_names:
        method_file = methodFile(method_name, data_name)
        N_32F = loadRGBA(method_file)

        fig.add_subplot(1, num_cols, col_id)
        plt.title(method_name, fontsize=font_size)
        plt.imshow(N_32F)
        plt.axis('off')
        col_id += 1

    result_dir = resultDir(batch_name)
    result_file = resultFile(result_dir, data_name)
    plt.savefig(result_file)

if __name__ == '__main__':
    print methodNames()
    batchResults(batch_func, batch_name)

