
# -*- coding: utf-8 -*-
## @package npr_sfs.plot.window
#
#  Matplot window utility package.
#  @author      tody
#  @date        2015/07/29

from matplotlib import pyplot as plt

def showMaximize():
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()