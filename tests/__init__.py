import unittest
from cfgutils.tests.test_CFGObj import test_CFGObj

def suite():
  testsuite = unittest.TestSuite()
  testsuite.addTest(test_CFGObj())
  return testsuite