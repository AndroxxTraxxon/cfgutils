import unittest
import sys
import os
import cfgutils
class test_CFGObj(unittest.TestCase):
  def runTest(self):
    self.test_JSON_Import()

  def setUp(self):
    print("Running {0}.setUp()".format(self.__class__.__name__))

  def tearDown(self):
    print("Running {0}.tearDown()".format(self.__class__.__name__))

  def test_JSON_Import(self):
    self.assertTrue(True)
    testJSONPath = os.path.join(os.path.dirname(__file__), "data", "testData.json")
    testObj = cfgutils.CFGObj.from_json_file(testJSONPath)

    print(str(testObj))
    self.assertNotEqual(testObj, None)
    self.assertEqual(testObj.a, 1)
    self.assertEqual(testObj.b, "apple")
    self.assertIsInstance(testObj, cfgutils.CFGObj)
    self.assertEqual(testObj.c.d, "banana")
    self.assertEqual(testObj.c.e, "bones")