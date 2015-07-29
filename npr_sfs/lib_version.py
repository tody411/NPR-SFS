
# -*- coding: utf-8 -*-
## @package npr_sfs.lib_version
#
#  npr_sfs.lib_version utility package.
#  @author      tody
#  @date        2015/07/29

from npr_sfs.util.logger import getLogger
logger = getLogger(__name__)

try:
    import numpy as np
except:
    logger.error("NumPy cannot be loaded.")

try:
    import scipy as sp
except:
    logger.error("SciPy cannot be loaded.")

try:
    import matplotlib
except:
    logger.error("matplotlib cannot be loaded.")

try:
    import pyamg
except:
    logger.error("PyAMG cannot be loaded.")

try:
    import cv2
except:
    logger.error("OpenCV cannot be loaded.")


if __name__ == '__main__':
    logger.info("Requred libraries.")
    print "* NumPy: %s" % np.version.version
    print "* SciPy: %s" % sp.version.version
    print "* matplotlib: %s" % matplotlib.__version__
    print "* OpenCV: %s" % cv2.__version__
    print "* PyAMG: %s" % pyamg.__version__
