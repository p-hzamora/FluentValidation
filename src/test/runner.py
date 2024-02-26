import unittest

import test_AbstractValidator
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
suite.addTests(
    [
        *loader.loadTestsFromModule(test_AbstractValidator),
        *loader.loadTestsFromModule(test_Equal),
        *loader.loadTestsFromModule(test_GreaterThanOrEqual),
        *loader.loadTestsFromModule(test_GreaterThanValidator),
        *loader.loadTestsFromModule(test_LessThanOrEqual),
        *loader.loadTestsFromModule(test_LessThanValidator),
        *loader.loadTestsFromModule(test_LengtValidator),
        *loader.loadTestsFromModule(test_PredicateValidator),
    ]
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner()
result = runner.run(suite)
