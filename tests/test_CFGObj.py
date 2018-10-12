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
    self.test_JSON_Nested_Objects()
    self.test_JSON_Nested_Arrays()

  def test_JSON_Nested_Arrays(self):
    testJSONPath = os.path.join(os.path.dirname(__file__), "data", "testArrayData.json")
    testObj = cfgutils.CFGObj.from_json_file(testJSONPath)
    
    print("testObj:", cfgutils.CFGObj.toString(testObj))
    self.assertNotEqual(testObj, None)
    self.assertEqual(testObj[0].a, 123)
    self.assertEqual(testObj[1].b, 456)
    self.assertEqual(testObj[2].c, 789)
    self.assertEqual(testObj[2].d[0], 'a')
    self.assertEqual(testObj[2].d[1], 'b')
    self.assertEqual(testObj[2].d[2], 'c')
    self.assertEqual(testObj[2].d[3], 'd')

  def test_JSON_Nested_Objects(self):
    testJSONPath = os.path.join(os.path.dirname(__file__), "data", "testData.json")
    testObj = cfgutils.CFGObj.from_json_file(testJSONPath)

    print(str(testObj))
    self.assertNotEqual(testObj, None)
    self.assertEqual(testObj.a, 1)
    self.assertEqual(testObj.b, "apple")
    self.assertIsInstance(testObj, cfgutils.CFGObj)
    self.assertEqual(testObj.c.d, "banana")
    self.assertEqual(testObj.c.e, "bones")