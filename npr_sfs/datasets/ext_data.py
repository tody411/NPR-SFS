
# -*- coding: utf-8 -*-
## @package npr_sfs.datasets.ext_data
#
#  npr_sfs.datasets.ext_data utility package.
#  @author      tody
#  @date        2015/10/06

import os

_ext_data_roots = ["C:/Users/tody/OneDrive/Projects/npr_sfs/datasets"]


def extDataRoot():
    for root in _ext_data_roots:
        if os.path.exists(root):
            return root


def extDataDirNames():
    file_names = os.listdir(extDataRoot())
    dir_names = [file_name for file_name in file_names if os.path.isdir(os.path.join(extDataRoot(), file_name))]
    return dir_names


def extDataDir(dir_name):
    return os.path.join(extDataRoot(), dir_name)


def extDataFiles(dir_name, file_filter=None):
    data_dir = extDataDir(dir_name)

    file_names = os.listdir(data_dir)
    file_path_list = [os.path.join(data_dir, file_name) for file_name in file_names]

    if file_filter is not None:
        file_path_list = [file_path for file_path in file_path_list if file_filter in file_path]
    return file_path_list



