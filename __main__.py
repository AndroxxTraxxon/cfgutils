import sys
import os

testflags = ("test", "-t")

def main():
  # print("{0}:main".format(__file__))
  for testflag in testflags:
    if testflag in sys.argv:
      testModule()
      exit(0)


def testModule():
  print("Running {0}:testModule()".format(os.path.basename(__file__)))
  import cfgutils.tests as tests
  try:
    unittest
  except NameError:
    import unittest
  unittest.main()

def test():
  try:
    tests
  except NameError:
    import cfgutils.tests as tests
  return tests.suite()

if __name__ == "__main__":
  main()