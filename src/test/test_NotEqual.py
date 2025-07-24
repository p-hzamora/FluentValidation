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
from dataclasses import dataclass
import sys
from typing import override
import unittest
from pathlib import Path
from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.enums import StringComparer


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())
from CultureScope import CultureScope
from person import Person
from TestValidator import TestValidator
from fluent_validation import AbstractValidator


class MyValueType:
    def __init__(self, value: int = 0):
        self._value: int = value

    @property
    def None_(self) -> MyValueType:
        return MyValueType()

    @property
    def Value(self) -> int:
        return self._value if self._value is not None else -1

    @override
    def __hash__(self) -> int:
        return 0 if self._value is None else hash(self._value)

    @override
    def __str__(self) -> str:
        return str(self._value) if self._value is not None else ""

    @override
    def __eq__(self, other: object) -> bool:
        if other is None or not isinstance(other, MyValueType):
            return False

        return self._value == other._value

    # static bool operator ==(MyValueType first, MyValueType second) {
    #    return first.Equals(second)

    # static bool operator !=(MyValueType first, MyValueType second) {
    #     return !(first == second)
    # }


@dataclass
class MyType:
    Value: MyValueType = MyValueType()


class MyTypeValidator(AbstractValidator[MyType]):
    def __init__(self):
        super().__init__()
        self.rule_for(lambda myType: myType.Value).not_equal(MyValueType().None_)


class NotEqualValidatorTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

    def test_When_the_objects_are_equal_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Foo"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertFalse(result.is_valid)

    def test_When_the_objects_are_not_equal_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Bar"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertTrue(result.is_valid)

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Foo"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Forename' must not be equal to 'Foo'.")

    def test_Validates_across_properties(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname).with_message("{ComparisonProperty}"))

        result = validator.validate(Person(Surname="foo", Forename="foo"))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "Surname")

    def test_Comparison_property_uses_custom_resolver(self):
        originalResolver = ValidatorOptions.Global.DisplayNameResolver

        try:
            ValidatorOptions.Global.DisplayNameResolver = lambda type, member, expr: member.Name + "Foo"
            validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname).with_message("{ComparisonProperty}"))

            result = validator.validate(Person(Surname="foo", Forename="foo"))
            self.assertEqual(result.errors[0].ErrorMessage, "SurnameFoo")
        finally:
            ValidatorOptions.Global.DisplayNameResolver = originalResolver

    # def test_Should_store_property_to_compare(self):
    # 	validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname))
    # 	propertyValidator = validator.CreateDescriptor()
    # 		.GetValidatorsForMember("Forename")
    # 		.Select(lambda x: x.Validator)
    # 		.OfType<NotEqualValidator<Person,string>>()
    # 		.Single()

    # 	propertyValidator.MemberToCompare.ShouldEqual(typeof(Person).GetProperty("Surname"))

    # def test_Should_store_comparison_type(self):
    # 	validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname))
    # 	propertyValidator = validator.CreateDescriptor()
    # 		.GetValidatorsForMember("Forename")
    # 		.Select(lambda x: x.Validator)
    # 		.OfType<NotEqualValidator<Person,string>>()
    # 		.Single()
    # 	propertyValidator.Comparison.ShouldEqual(Comparison.not_equal)

    def test_Should_not_be_valid_for_case_insensitve_comparison(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("FOO"))
        result = validator.validate(Person(Forename="foo"))
        self.assertTrue(result.is_valid)

    def test_Should_not_be_valid_for_case_insensitve_comparison_with_expression(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname, StringComparer.OrdinalIgnoreCase)
        )  # FIXME [x]: Try to use implement StringComparer.OrdinalIgnoreCase
        result = validator.validate(Person(Forename="foo", Surname="FOO"))  # original
        self.assertFalse(result.is_valid)

    def test_Should_handle_custom_value_types_correctly(self):
        myType = MyType()
        myTypeValidator = MyTypeValidator()

        validationResult = myTypeValidator.validate(myType)
        self.assertFalse(validationResult.is_valid)

    def test_Should_use_ordinal_comparison_by_default(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Surname).not_equal("a")
        result = validator.validate(Person(Surname="a\0"))
        self.assertTrue(result.is_valid)


if __name__ == "__main__":
    unittest.main()
