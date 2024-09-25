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
import test_ForEachRule
import test_DefaultValidatorExtension
import test_CreditCardValidator
import test_ScalePrecisionValidator
import test_Empty
import test_Null
import test_CascadingFailures
import test_ChainedValidation
import test_ChainingValidators
import test_LegacyCascadeModeProperties
import test_InclusiveBetweenValidator
import test_ExclusiveBetweenValidator
import test_Extension
import test_CustomMessageFormat
import test_ValidatorSelector
import test_UserSeverity
import test_ChildRules
import test_CascadingFailuresLegacy
import test_CollectionValidatorWithParent
import test_EnumValidator

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(
    (
        *loader.loadTestsFromModule(test_EnumValidator),
        *loader.loadTestsFromModule(test_CollectionValidatorWithParent),
        *loader.loadTestsFromModule(test_CascadingFailuresLegacy),
        *loader.loadTestsFromModule(test_ChildRules),
        *loader.loadTestsFromModule(test_UserSeverity),
        *loader.loadTestsFromModule(test_ValidatorSelector),
        *loader.loadTestsFromModule(test_CustomMessageFormat),
        *loader.loadTestsFromModule(test_Extension),
        *loader.loadTestsFromModule(test_InclusiveBetweenValidator),
        *loader.loadTestsFromModule(test_ExclusiveBetweenValidator),
        *loader.loadTestsFromModule(test_LegacyCascadeModeProperties),
        *loader.loadTestsFromModule(test_ChainedValidation),
        *loader.loadTestsFromModule(test_ChainingValidators),
        *loader.loadTestsFromModule(test_CascadingFailures),
        *loader.loadTestsFromModule(test_Null),
        *loader.loadTestsFromModule(test_Empty),
        *loader.loadTestsFromModule(test_CreditCardValidator),
        *loader.loadTestsFromModule(test_ScalePrecisionValidator),
        *loader.loadTestsFromModule(test_DefaultValidatorExtension),
        *loader.loadTestsFromModule(test_ForEachRule),  # FIXME [ ]: If I add this module at the end of the tuple, then I get 6 errors like '- foo[0].foo + Orders[0].ProductName'
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

    )
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner()
result = runner.run(suite)
