# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

import unittest

import test_AbstractValidator
import test_Equal
import test_GreaterThanOrEqual
import test_GreaterThanValidator
import test_LessThanOrEqualToValidator
import test_LessThanValidator
import test_LengthValidator
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
import test_PrecisionScaleValidator
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
import test_StringEnumValidator
import test_ComplexValidation
import test_InlineValidator
import test_EmailValidator
import test_TrackingCollection
import test_LanguageManager
import test_RuleBuilder
import test_UserState
import test_NotEmpty
import test_ValidationResult
import test_RuleDependency
import test_RegularExpressionValidator
import test_LocalisedMessages
import test_PropertyChain
import test_InheritanceValidator
import python_test.test_extract_type_when_using_cast_method as _python_cast_method

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(
    (
        *loader.loadTestsFromModule(_python_cast_method),
        *loader.loadTestsFromModule(test_InheritanceValidator),
        *loader.loadTestsFromModule(test_PropertyChain),
        *loader.loadTestsFromModule(test_RegularExpressionValidator),
        *loader.loadTestsFromModule(test_LocalisedMessages),
        *loader.loadTestsFromModule(test_NotEmpty),  # FIXME [ ]: This test is depending on the other. Probably some contexts are not being erased as it should be
        *loader.loadTestsFromModule(test_RuleDependency),  # FIXME [ ]: This test is depending on the other. Probably some contexts are not being erased as it should be
        *loader.loadTestsFromModule(test_RuleBuilder),
        *loader.loadTestsFromModule(test_EmailValidator),
        *loader.loadTestsFromModule(test_TrackingCollection),
        *loader.loadTestsFromModule(test_InlineValidator),
        *loader.loadTestsFromModule(test_ComplexValidation),
        *loader.loadTestsFromModule(test_StringEnumValidator),
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
        *loader.loadTestsFromModule(test_PrecisionScaleValidator),
        *loader.loadTestsFromModule(test_DefaultValidatorExtension),
        *loader.loadTestsFromModule(test_AbstractValidator),
        *loader.loadTestsFromModule(test_ForEachRule),
        *loader.loadTestsFromModule(test_Equal),
        *loader.loadTestsFromModule(test_GreaterThanOrEqual),
        *loader.loadTestsFromModule(test_GreaterThanValidator),
        *loader.loadTestsFromModule(test_LessThanOrEqualToValidator),
        *loader.loadTestsFromModule(test_LessThanValidator),
        *loader.loadTestsFromModule(test_LengthValidator),
        *loader.loadTestsFromModule(test_PredicateValidator),
        *loader.loadTestsFromModule(test_Ruleset),
        *loader.loadTestsFromModule(test_NotNull),
        *loader.loadTestsFromModule(test_Condition),
        *loader.loadTestsFromModule(test_SharedCondition),
        *loader.loadTestsFromModule(test_ValidateAndThrow),
        *loader.loadTestsFromModule(test_NameResolutionPluggability),
        *loader.loadTestsFromModule(test_LanguageManager),
        *loader.loadTestsFromModule(test_UserState),
        *loader.loadTestsFromModule(test_ValidationResult),
    )
)

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=0)
result = runner.run(suite)
