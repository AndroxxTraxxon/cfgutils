import sys

testflags = ("test", "-t")

def main():
  print("__main__.py:main")
  for testflag in testflags:
    if testflag in sys.argv:
      importTest()
      exit(0)


def importTest():
  print("__main__.py:test")
  print("Testing {0}...".format(str(sys.modules[__name__].__file__)))
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