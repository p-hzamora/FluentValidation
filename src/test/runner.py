import unittest

import test_Equal
import test_GreaterThanOrEqual
import test_GreaterThanValidator
import test_LessThanOrEqual
import test_LessThanValidator
import test_LengtValidator
import test_PredicateValidator

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(test_Equal))
suite.addTests(loader.loadTestsFromModule(test_GreaterThanOrEqual))
suite.addTests(loader.loadTestsFromModule(test_GreaterThanValidator))
suite.addTests(loader.loadTestsFromModule(test_LessThanOrEqual))
suite.addTests(loader.loadTestsFromModule(test_LessThanValidator))
suite.addTest(loader.loadTestsFromModule(test_LengtValidator))
suite.addTest(loader.loadTestsFromModule(test_PredicateValidator))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner()
result = runner.run(suite)
