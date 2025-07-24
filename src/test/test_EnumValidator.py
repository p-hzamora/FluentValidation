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
from typing import Optional
import unittest
import sys
from pathlib import Path
from enum import Flag


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.InlineValidator import InlineValidator
from person import EnumGender, Person
from CultureScope import CultureScope
from TestValidator import TestValidator


@dataclass
class Foo:
    Gender: Optional[EnumGender] = None


# region Flag enum helpers
@dataclass
class FlagsEnumPoco:
    SByteValue: Optional[SByteEnum] = None
    ByteValue: Optional[ByteEnum] = None
    Int16Value: Optional[Int16Enum] = None
    UInt16Value: Optional[UInt16Enum] = None
    Int32Value: Optional[Int32Enum] = None
    UInt32Value: Optional[UInt32Enum] = None
    Int64Value: Optional[Int64Enum] = None
    UInt64Value: Optional[UInt64Enum] = None
    EnumWithNegativesValue: Optional[EnumWithNegatives] = None
    EnumWithOverlappingFlagsValue: Optional[EnumWithOverlappingFlags] = None

    def PopulateWithValidValues(self) -> None:
        self.SByteValue = SByteEnum.B | SByteEnum.C
        self.ByteValue = ByteEnum.B | ByteEnum.C
        self.Int16Value = Int16Enum.B | Int16Enum.C
        self.UInt16Value = UInt16Enum.B | UInt16Enum.C
        self.Int32Value = Int32Enum.B | Int32Enum.C
        self.UInt32Value = UInt32Enum.B | UInt32Enum.C
        self.Int64Value = Int64Enum.B | Int64Enum.C
        self.UInt64Value = UInt64Enum.B | UInt64Enum.C
        self.EnumWithNegativesValue = EnumWithNegatives.Bar
        self.EnumWithOverlappingFlagsValue = EnumWithOverlappingFlags.A

    def PopulateWithInvalidPositiveValues(self) -> None:
        self.SByteValue = 123  # (SByteEnum)123
        self.ByteValue = 123  # (ByteEnum)123
        self.Int16Value = 123  # (Int16Enum)123
        self.UInt16Value = 123  # (UInt16Enum)123
        self.Int32Value = 123  # (Int32Enum)123
        self.UInt32Value = 123  # (UInt32Enum)123
        self.Int64Value = 123  # (Int64Enum)123
        self.UInt64Value = 123  # (UInt64Enum)123
        self.EnumWithNegativesValue = 123  # (EnumWithNegatives)123
        self.EnumWithOverlappingFlagsValue = 123  # (EnumWithOverlappingFlags)123

    def PopulateWithInvalidNegativeValues(self) -> None:
        self.SByteValue = -123  # SByteEnum(-123)
        self.Int16Value = -123  # Int16Enum(-123)
        self.Int32Value = -123  # Int32Enum(-123)
        self.Int64Value = -123  # Int64Enum(-123)
        self.EnumWithNegativesValue = -123  # EnumWithNegatives(-123)
        self.EnumWithOverlappingFlagsValue = -123  # EnumWithOverlappingFlags(-123)


# [Flags]
class SByteEnum(Flag):  # sbyte {
    A = 0
    B = 1
    C = 2


# [Flags]
class ByteEnum(Flag):  # byte {
    A = 0
    B = 1
    C = 2


# [Flags]
class Int16Enum(Flag):  # short {
    A = 0
    B = 1
    C = 2


# [Flags]
class UInt16Enum(Flag):  # ushort {
    A = 0
    B = 1
    C = 2


# [Flags]
class Int32Enum(Flag):  # int {
    A = 0
    B = 1
    C = 2


# [Flags]
class UInt32Enum(Flag):  # uint {
    A = 0
    B = 1
    C = 2


# [Flags]
class Int64Enum(Flag):  # long {
    A = 0
    B = 1
    C = 2


# [Flags]
class UInt64Enum(Flag):  # ulong {
    A = 0
    B = 1
    C = 2


# [Flags]
class EnumWithNegatives(Flag):
    All = ~0
    Bar = 1
    Foo = 2


# NB this enum actually confuses the built-in Enum.ToString() functionality - it shows 7 for A|B.
# [Flags]
class EnumWithOverlappingFlags(Flag):
    A = 3
    B = 4
    C = 5


# endregion


class EnumValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

        self.validator: TestValidator = TestValidator(lambda v: v.rule_for(lambda x: x.Gender).is_in_enum())

    def test_IsValidTests(self):
        self.assertTrue(self.validator.validate(Person(Gender=EnumGender.Female)).is_valid)  # Simplest valid value
        self.assertTrue(self.validator.validate(Person(Gender=EnumGender.Male)).is_valid)  # Other valid value
        self.assertTrue(self.validator.validate(Person(Gender=EnumGender(1))).is_valid)  # Casting with valid value

    def test_When_the_enum_is_not_initialized_with_valid_value_then_the_validator_should_fail(self):
        result = self.validator.validate(Person())  # Default value 0 is not defined in Enum
        self.assertFalse(result.is_valid)

    ## COMMENT: In Python, unlike in C#, the compiler raises an error if the data you are trying to cast, does not exist.
    # def test_When_the_enum_is_initialized_with_invalid_value_then_the_validator_should_fail(self):
    #     result = self.validator.validate(Person(Gender=EnumGender(3)))  # 3 in not defined in Enum
    #     self.assertFalse(result.is_valid)

    def test_When_validation_fails_the_default_error_should_be_set(self):
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "'Gender' has a range of values which does not include '0'.")

    def test_Nullable_enum_valid_when_property_value_is_null(self):
        validator = InlineValidator[Foo](Foo)
        validator.rule_for(lambda x: x.Gender).is_in_enum()
        result = validator.validate(Foo())
        self.assertTrue(result.is_valid)

    def test_Nullable_enum_valid_when_value_specified(self):
        validator = InlineValidator[Foo](Foo)
        validator.rule_for(lambda x: x.Gender).is_in_enum()
        result = validator.validate(Foo(Gender=EnumGender.Male))
        self.assertTrue(result.is_valid)

    def test_Nullable_enum_invalid_when_bad_value_specified(self):
        validator = InlineValidator[Foo](Foo)
        validator.rule_for(lambda x: x.Gender).is_in_enum()
        result = validator.validate(Foo(Gender=42))
        self.assertFalse(result.is_valid)

    def test_Flags_enum_valid_when_using_bitwise_value(self):
        inlineValidator = self.Create_validator()
        poco = FlagsEnumPoco()
        poco.PopulateWithValidValues()

        result = inlineValidator.validate(poco)
        self.assertTrue(result.is_valid)

        # special case - valid negative value
        poco.EnumWithNegativesValue = EnumWithNegatives.All
        result = inlineValidator.validate(poco)
        self.assertTrue(result.is_valid)

    def test_Flags_enum_with_overlapping_flags_valid_when_using_bitwise_value(self):
        inlineValidator = InlineValidator[FlagsEnumPoco](FlagsEnumPoco)
        inlineValidator.rule_for(lambda x: x.EnumWithOverlappingFlagsValue).is_in_enum()

        poco = FlagsEnumPoco()

        # test all combinations
        poco.EnumWithOverlappingFlagsValue = EnumWithOverlappingFlags.A | EnumWithOverlappingFlags.B
        self.assertTrue(inlineValidator.validate(poco).is_valid)

        poco.EnumWithOverlappingFlagsValue = EnumWithOverlappingFlags.B | EnumWithOverlappingFlags.C
        self.assertTrue(inlineValidator.validate(poco).is_valid)

        poco.EnumWithOverlappingFlagsValue = EnumWithOverlappingFlags.A | EnumWithOverlappingFlags.C
        self.assertTrue(inlineValidator.validate(poco).is_valid)

        poco.EnumWithOverlappingFlagsValue = EnumWithOverlappingFlags.A | EnumWithOverlappingFlags.B | EnumWithOverlappingFlags.C
        self.assertTrue(inlineValidator.validate(poco).is_valid)

    def test_Flags_enum_validates_correctly_when_using_zero_value(self):
        inlineValidator = self.Create_validator()

        poco = FlagsEnumPoco(EnumWithNegativesValue=0, EnumWithOverlappingFlagsValue=0)

        # all default to zero
        result = inlineValidator.validate(poco)

        property_names = [x.PropertyName for x in result.errors]
        self.assertIn("EnumWithNegativesValue", property_names)
        self.assertIn("EnumWithOverlappingFlagsValue", property_names)
        self.assertEqual(len(result.errors), 2)
        self.assertFalse(result.is_valid)

    def test_Flags_enum_invalid_when_using_outofrange_positive_value(self):
        inlineValidator = self.Create_validator()

        poco = FlagsEnumPoco()
        poco.PopulateWithInvalidPositiveValues()

        result = inlineValidator.validate(poco)
        self.assertFalse(result.is_valid)
        property_names = [x.PropertyName for x in result.errors]
        self.assertIn("ByteValue", property_names)
        self.assertIn("SByteValue", property_names)
        self.assertIn("Int16Value", property_names)
        self.assertIn("UInt16Value", property_names)
        self.assertIn("Int32Value", property_names)
        self.assertIn("UInt32Value", property_names)
        self.assertIn("Int64Value", property_names)
        self.assertIn("UInt64Value", property_names)
        self.assertIn("EnumWithNegativesValue", property_names)

    def test_Flags_enum_invalid_when_using_outofrange_negative_value(self):
        inlineValidator = self.Create_validator()

        poco = FlagsEnumPoco()
        poco.PopulateWithInvalidNegativeValues()

        result = inlineValidator.validate(poco)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].PropertyName, "SByteValue")
        self.assertEqual(result.errors[1].PropertyName, "Int16Value")
        self.assertEqual(result.errors[2].PropertyName, "Int32Value")
        self.assertEqual(result.errors[3].PropertyName, "Int64Value")

    @staticmethod
    def Create_validator() -> InlineValidator[FlagsEnumPoco]:
        inlineValidator = InlineValidator[FlagsEnumPoco](FlagsEnumPoco)
        inlineValidator.rule_for(lambda x: x.SByteValue).is_in_enum()
        inlineValidator.rule_for(lambda x: x.ByteValue).is_in_enum()
        inlineValidator.rule_for(lambda x: x.Int16Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.UInt16Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.Int32Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.UInt32Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.Int64Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.UInt64Value).is_in_enum()
        inlineValidator.rule_for(lambda x: x.EnumWithNegativesValue).is_in_enum()
        inlineValidator.rule_for(lambda x: x.EnumWithOverlappingFlagsValue).is_in_enum()

        return inlineValidator


if __name__ == "__main__":
    unittest.main()
