
# -*- coding: utf-8 -*-
## @package tests.dataset_test
#
#  Test for dataset.
#  @author      tody
#  @date        2015/07/29

import unittest
from npr_sfs.datasets.loader import dataNames


class TestDataSet(unittest.TestCase):
    def test_dataset(self):
        data_names = dataNames()
        self.assertTrue(data_names, data_names)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestDataSet))
    return suite