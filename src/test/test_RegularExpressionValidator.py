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
import sys
import re
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Person


class RegularExpressionValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()
        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(r"^\w\d$"))
        self.validator2 = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(lambda x: x.Regex))
        self.validator3 = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(lambda x: x.AnotherRegex))

    def test_When_the_text_matches_the_regular_expression_then_the_validator_should_pass(self):
        input_text = "S3"
        result = self.validator.validate(Person(Surname=input_text))
        self.assertTrue(result.is_valid)

    def test_When_the_text_does_not_match_the_regular_expression_then_the_validator_should_fail(self):
        result = self.validator.validate(Person(Surname="S33"))
        self.assertFalse(result.is_valid)

        result = self.validator.validate(Person(Surname=" 5"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_empty_then_the_validator_should_fail(self):
        result = self.validator.validate(Person(Surname=""))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_null_then_the_validator_should_pass(self):
        result = self.validator.validate(Person(Surname=None))
        self.assertTrue(result.is_valid)

    def test_When_validation_fails_the_default_error_should_be_set(self):
        result = self.validator.validate(Person(Surname="S33"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' is not in the correct format.")

    def test_When_the_text_matches_the_lambda_regular_expression_then_the_validator_should_pass(self):
        input_text = "S3"
        result = self.validator2.validate(Person(Surname=input_text, Regex=r"^\w\d$"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_matches_the_lambda_regex_regular_expression_then_the_validator_should_pass(self):
        input_text = "S3"
        result = self.validator3.validate(Person(Surname=input_text, AnotherRegex=re.compile(r"^\w\d$")))
        self.assertTrue(result.is_valid)

    def test_When_the_text_does_not_match_the_lambda_regular_expression_then_the_validator_should_fail(self):
        result = self.validator2.validate(Person(Surname="S33", Regex=r"^\w\d$"))
        self.assertFalse(result.is_valid)

        result = self.validator2.validate(Person(Surname=" 5", Regex=r"^\w\d$"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_does_not_match_the_lambda_regex_regular_expression_then_the_validator_should_fail(self):
        result = self.validator3.validate(Person(Surname="S33", AnotherRegex=re.compile(r"^\w\d$")))
        self.assertFalse(result.is_valid)

        result = self.validator3.validate(Person(Surname=" 5", AnotherRegex=re.compile(r"^\w\d$")))
        self.assertFalse(result.is_valid)

    def test_Can_access_expression_in_message(self):
        v = TestValidator()
        v.rule_for(lambda x: x.Forename).matches(r"^\w\d$").with_message("test {RegularExpression}")

        result = v.validate(Person(Forename=""))
        self.assertEqual(result.errors[0].ErrorMessage, r"test ^\w\d$")

    def test_Can_access_expression_in_message_lambda(self):
        v = TestValidator()
        v.rule_for(lambda x: x.Forename).matches(lambda x: x.Regex).with_message("test {RegularExpression}")

        result = v.validate(Person(Forename="", Regex=r"^\w\d$"))
        self.assertEqual(result.errors[0].ErrorMessage, r"test ^\w\d$")

    def test_Can_access_expression_in_message_lambda_regex(self):
        v = TestValidator()
        v.rule_for(lambda x: x.Forename).matches(lambda x: x.AnotherRegex).with_message("test {RegularExpression}")

        result = v.validate(Person(Forename="", AnotherRegex=re.compile(r"^\w\d$")))
        self.assertEqual(result.errors[0].ErrorMessage, r"test ^\w\d$")

    def test_Uses_regex_object(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(re.compile(r"^\w\d$")))
        input_text = "S3"
        result = validator.validate(Person(Surname=input_text))
        self.assertTrue(result.is_valid)

    def test_Uses_lazily_loaded_expression(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(lambda x: r"^\w\d$"))
        input_text = "S3"
        result = validator.validate(Person(Surname=input_text))
        self.assertTrue(result.is_valid)

    def test_Uses_lazily_loaded_expression_with_options(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).matches(r"^\w\d$"))  # Note: Python re doesn't have exact equivalent to RegexOptions.Compiled
        input_text = "S3"
        result = validator.validate(Person(Surname=input_text))
        self.assertTrue(result.is_valid)


if __name__ == "__main__":
    unittest.main()
