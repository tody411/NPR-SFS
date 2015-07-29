
# -*- coding: utf-8 -*-
## @package setup
#
#  setup utility package.
#  @author      tody
#  @date        2015/07/29

from setuptools import setup, find_packages
from npr_sfs import __author__, __version__, __license__

setup(
        name = 'npr_sfs',
        version          = __version__,
        description      = 'Sample implementations of Shape-From-Shading techniques for NPR.',
        license          = __license__,
        author           = __author__,
        url              = 'https://github.com/junion-org/pip_github_test.git',
        packages=['inversetoon'],
        )

