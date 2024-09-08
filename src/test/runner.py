import unittest

import test_AbstractValidator
import test_Equal
import test_GreaterThanOrEqual
import test_GreaterThanValidator
import test_LessThanOrEqual
import test_LessThanValidator
import test_LengtValidator
import test_PredicateValidator
import test_Ruleset
import test_NotNull
import test_Condition
import test_SharedCondition
import test_ValidateAndThrow
import test_NameResolutionPluggability

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
        *loader.loadTestsFromModule(test_Ruleset),
        *loader.loadTestsFromModule(test_NotNull),
        *loader.loadTestsFromModule(test_Condition),
        *loader.loadTestsFromModule(test_SharedCondition),
        *loader.loadTestsFromModule(test_ValidateAndThrow),
        *loader.loadTestsFromModule(test_NameResolutionPluggability),
    ]
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner()
result = runner.run(suite)
