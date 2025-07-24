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
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Person


class CreditCardValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()
        self.validator: TestValidator = TestValidator(lambda v: v.rule_for(lambda x: x.CreditCard).credit_card())

    # copied these tests from the mvc3 unit tests.
    def test_IsValidTests(self):
        self.assertTrue(self.validator.validate(Person(CreditCard=None)).is_valid)  # Optional values are always valid
        self.assertTrue(self.validator.validate(Person(CreditCard="0000000000000000")).is_valid)  # Simplest valid value
        self.assertTrue(self.validator.validate(Person(CreditCard="1234567890123452")).is_valid)  # Good checksum
        self.assertTrue(self.validator.validate(Person(CreditCard="1234-5678-9012-3452")).is_valid)  # Good checksum, with dashes
        self.assertTrue(self.validator.validate(Person(CreditCard="1234 5678 9012 3452")).is_valid)  # Good checksum, with spaces
        self.assertFalse(self.validator.validate(Person(CreditCard="0000000000000001")).is_valid)  # Bad checksum

    def test_When_validation_fails_the_default_error_should_be_set(self):
        creditcard: str = "foo"
        result = self.validator.validate(Person(CreditCard=creditcard))
        self.assertEqual(result.errors[0].ErrorMessage, "'Credit Card' is not a valid credit card number.")


if __name__ == "__main__":
    unittest.main()
