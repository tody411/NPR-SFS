# -*- coding: utf-8 -*-
## @package npr_sfs.main
#
#  Main functions.
#  @author      tody
#  @date        2015/09/01

from npr_sfs.datasets.loader import dataNames, loadData

import results.ibme
import results.lumo
import results.compare
from npr_sfs.results.results import batchResults

batch_modules = [results.ibme,
                 results.lumo,
                 results.compare]

if __name__ == '__main__':
    for batch_module in batch_modules:
        batchResults(batch_module.batch_func, batch_module.batch_name)


