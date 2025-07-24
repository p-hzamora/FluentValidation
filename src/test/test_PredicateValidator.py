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
from TestValidator import TestValidator
from person import Person
from CultureScope import CultureScope


class PredicateValidatorTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        CultureScope.SetDefaultCulture()
        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).must(lambda forename: forename == "Jeremy"))

    def test_Should_fail_when_predicate_returns_false(self):
        result = self.validator.validate(Person(Forename="Foo"))
        self.assertFalse(result.is_valid)

    def test_Should_succeed_when_predicate_returns_true(self):
        result = self.validator.validate(Person(Forename="Jeremy"))
        self.assertTrue(result.is_valid)

    def test_Should_throw_when_predicate_is_null(self):
        with self.assertRaises(TypeError):
            TestValidator(lambda v: v.rule_for(lambda x: x.Surname).must(None))

    def test_When_validation_fails_the_default_error_should_be_set(self):
        result = self.validator.validate(Person(Forename="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "The specified condition was not met for 'Forename'.")

    def test_When_validation_fails_metadata_should_be_set_on_failure(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Forename).must(lambda forename: forename == "Jeremy")
            # .with_message(lambda x: TestMessages.ValueOfForPropertyNameIsNotValid)
        )

        result = validator.validate(Person(Forename="test"))
        error = result.errors[0]

        self.assertIsNotNone(error)
        self.assertEqual(error.PropertyName, "Forename")
        self.assertEqual(error.AttemptedValue, "test")
        self.assertEqual(error.ErrorCode, "PredicateValidator")

        self.assertEqual(len(error.FormattedMessagePlaceholderValues), 3)
        self.assertTrue("PropertyName" in error.FormattedMessagePlaceholderValues)
        self.assertTrue("PropertyValue" in error.FormattedMessagePlaceholderValues)
        self.assertTrue("PropertyPath" in error.FormattedMessagePlaceholderValues)

        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyName"], "Forename")
        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyValue"], "test")
        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyPath"], "Forename")


if __name__ == "__main__":
    unittest.main()
