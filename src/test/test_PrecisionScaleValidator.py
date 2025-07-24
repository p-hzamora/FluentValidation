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

from __future__ import annotations
from decimal import Decimal
import unittest

import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Person


class ScalePrecisionValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

    def test_Scale_precision_should_be_valid(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(4, 2, False))

        result = validator.validate(Person(Discount=Decimal("12.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("2.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("-2.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("0.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("0.04")))
        self.assertTrue(result.is_valid)

    def test_Scale_precision_should_be_valid_nullable(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableDiscount).precision_scale(4, 2, False))

        result = validator.validate(Person(NullableDiscount=Decimal("12.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(NullableDiscount=Decimal("2.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(NullableDiscount=Decimal("-2.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(NullableDiscount=Decimal("0.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(NullableDiscount=None))
        self.assertTrue(result.is_valid)

    def test_Scale_precision_should_not_be_valid(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(4, 2, False))

        result = validator.validate(Person(Discount=Decimal("123.456778")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 9 digits and 6 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("12.3414")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 6 digits and 4 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("1.344")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 4 digits and 3 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("156.3")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 5 digits and 2 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("65.430")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 5 digits and 3 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("0.003")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 4 digits and 3 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("0.030303")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 7 digits and 6 decimals were found.")

    def test_Scale_precision_should_not_be_valid_nullable(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableDiscount).precision_scale(4, 2, False).with_name("Discount"))

        result = validator.validate(Person(NullableDiscount=Decimal("123.456778")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 9 digits and 6 decimals were found.")

        result = validator.validate(Person(NullableDiscount=Decimal("12.3414")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 6 digits and 4 decimals were found.")

        result = validator.validate(Person(NullableDiscount=Decimal("1.344")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 4 digits and 3 decimals were found.")

        result = validator.validate(Person(NullableDiscount=Decimal("156.3")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 5 digits and 2 decimals were found.")

        result = validator.validate(Person(NullableDiscount=Decimal("65.430")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 5 digits and 3 decimals were found.")

    def test_Scale_precision_should_be_valid_when_they_are_equal(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(2, 2, False))

        result = validator.validate(Person(Discount=Decimal("0.34")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("0.3")))
        self.assertTrue(result.is_valid)

        # COMMENT: I believed that in the original C# library, 0M represents a decimal as 0.00, but that's not true
        # TODOL [x]: translate 0M as Decimal("0.00") to assert True
        result = validator.validate(Person(Discount=Decimal("0.00")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("-0.34")))
        self.assertTrue(result.is_valid)

    def test_Scale_precision_should_not_be_valid_when_they_are_equal(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(2, 2, False))

        result = validator.validate(Person(Discount=Decimal("123.456778")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 2 digits in total, with allowance for 2 decimals. 9 digits and 6 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("0.341")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 2 digits in total, with allowance for 2 decimals. 4 digits and 3 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("0.041")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 2 digits in total, with allowance for 2 decimals. 4 digits and 3 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("1.34")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 2 digits in total, with allowance for 2 decimals. 3 digits and 2 decimals were found.")

        # COMMENT: in the original C# library, 1M represent a decimal as 1.00. Thats the reason why get an error
        result = validator.validate(Person(Discount=Decimal("1")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 2 digits in total, with allowance for 2 decimals. 3 digits and 2 decimals were found.")

    def test_Scale_precision_should_be_valid_when_ignoring_trailing_zeroes(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(4, 2, True))

        result = validator.validate(Person(Discount=Decimal("15.0000000000000000000000000")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("0000000000000000000015.0000000000000000000000000")))
        self.assertTrue(result.is_valid)

        result = validator.validate(Person(Discount=Decimal("65.430")))
        self.assertTrue(result.is_valid)

    def test_Scale_precision_should_not_be_valid_when_ignoring_trailing_zeroes(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Discount).precision_scale(4, 2, True))

        result = validator.validate(Person(Discount=Decimal("1565.0")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 6 digits and 2 decimals were found.")

        result = validator.validate(Person(Discount=Decimal("15.0000000000000000000000001")))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "'Discount' must not be more than 4 digits in total, with allowance for 2 decimals. 27 digits and 25 decimals were found.")


if __name__ == "__main__":
    unittest.main()
