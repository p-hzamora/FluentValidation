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

from datetime import datetime
import sys
import unittest
from pathlib import Path

# from StreetNumberComparer import StreetNumberComparer


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from StreetNumberComparer import StreetNumberComparer
from fluent_validation.validators.RangeValidator import RangeValidatorFactory
from TestValidator import TestValidator  # noqa: E402

from person import _Address as Address  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class ExclusiveBetweenValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()
        self._fromDate: datetime = datetime(2009, 1, 1)
        self._toDate: datetime = datetime(2009, 12, 31)

    def test_When_the_value_is_between_the_range_specified_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=5))
        self.assertTrue(result.is_valid)

    def test_When_the_value_is_smaller_than_the_range_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=0))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_range_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=11))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_exactly_the_size_of_the_upper_bound_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=10))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_exactly_the_size_of_the_lower_bound_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=1))
        self.assertFalse(result.is_valid)

    def test_When_the_to_is_smaller_than_the_from_then_the_validator_should_throw(self):
        with self.assertRaises(IndexError):
            TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(10, 1))

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).exclusive_between(1, 10))
        result = validator.validate(Person(Id=0))
        self.assertEqual(result.errors[0].ErrorMessage, "'Id' must be between 1 and 10 (exclusive). You entered 0.")

    def test_To_and_from_properties_should_be_set(self):
        validator = RangeValidatorFactory.CreateExclusiveBetween(1, 10)
        self.assertEqual(validator.From, 1)
        self.assertEqual(validator.To, 10)

    def test_When_the_value_is_between_the_range_specified_then_the_validator_should_pass_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("aa", "zz"))
        result = validator.validate(Person(Surname="bbb"))
        self.assertTrue(result.is_valid)

    def test_When_the_value_is_smaller_than_the_range_then_the_validator_should_fail_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("bbb", "zz"))
        result = validator.validate(Person(Surname="aaa"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_range_then_the_validator_should_fail_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("aaa", "bbb"))
        result = validator.validate(Person(Surname="zzz"))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_exactly_the_size_of_the_upper_bound_then_the_validator_should_pass_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("aa", "zz"))
        result = validator.validate(Person(Surname="aa"))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_exactly_the_size_of_the_lower_bound_then_the_validator_should_pass_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("aa", "zz"))
        result = validator.validate(Person(Surname="zz"))
        self.assertFalse(result.is_valid)

    def test_When_the_to_is_smaller_than_the_from_then_the_validator_should_throw_for_strings(self):
        with self.assertRaises(IndexError):
            RangeValidatorFactory.CreateExclusiveBetween("ccc", "aaa")

    def test_When_the_validator_fails_the_error_message_should_be_set_for_strings(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exclusive_between("bbb", "zzz"))
        result = validator.validate(Person(Surname="aaa"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must be between bbb and zzz (exclusive). You entered aaa.")

    def test_To_and_from_properties_should_be_set_for_strings(self):
        validator = RangeValidatorFactory.CreateExclusiveBetween("a", "c")
        self.assertEqual(validator.From, "a")
        self.assertEqual(validator.To, "c")

    def test_To_and_from_properties_should_be_set_for_dates(self):
        validator = RangeValidatorFactory.CreateExclusiveBetween(self._fromDate, self._toDate)
        self.assertEqual(validator.From, self._fromDate)
        self.assertEqual(validator.To, self._toDate)

    def test_Validates_with_nullable_when_property_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).exclusive_between(1, 5))
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).exclusive_between(1, 5))
        result = validator.validate(Person(NullableInt=10))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_between_the_range_specified_by_icomparer_then_the_validator_should_pass(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Address).exclusive_between(
                Address(Line1="3 Main St."),
                Address(Line1="10 Main St."),
                StreetNumberComparer(),
            )
        )
        result = validator.validate(Person(Address=Address(Line1="5 Main St.")))
        self.assertTrue(result.is_valid)

    def test_When_the_value_is_smaller_than_the_range_by_icomparer_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address).exclusive_between(Address(Line1="3 Main St."), Address(Line1="10 Main St."), StreetNumberComparer()))

        result = validator.validate(Person(Address=Address(Line1="1 Main St.")))
        self.assertFalse(result.is_valid)

    def test_When_the_value_is_larger_than_the_range_by_icomparer_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address).exclusive_between(Address(Line1="3 Main St."), Address(Line1="10 Main St."), StreetNumberComparer()))
        result = validator.validate(Person(Address=Address(Line1="11 Main St.")))
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
