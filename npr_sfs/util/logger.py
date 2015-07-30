
# -*- coding: utf-8 -*-
## @package npr_sfs.util.logger
#
#  Log utility package.
#  @author      tody
#  @date        2015/07/29

import logging


def createFormatter():
    formatter = createPackageFormatter()
    return formatter


def createPackageFormatter():
    formatter = logging.Formatter(fmt='%(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    return formatter


def getLogger(logger_name, level=logging.DEBUG):
    return getStreamLogger(logger_name, level)


def getStreamLogger(logger_name, level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    formatter = createFormatter()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
