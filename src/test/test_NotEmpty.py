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
from typing import Iterator
import datetime

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Person
from fluent_validation.InlineValidator import InlineValidator


class TestModel:
    @property
    def Strings(self) -> Iterator[str]:
        return iter([])


class NotEmptyTester(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

    def test_When_there_is_a_value_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        result = validator.validate(Person(Surname="Foo"))
        self.assertTrue(result.is_valid)

    def test_When_value_is_null_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        result = validator.validate(Person(Surname=None))
        self.assertFalse(result.is_valid)

    def test_When_value_is_empty_string_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        result = validator.validate(Person(Surname=""))
        self.assertFalse(result.is_valid)

    def test_When_value_is_whitespace_validation_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        result = validator.validate(Person(Surname="         "))
        self.assertFalse(result.is_valid)

    def test_When_value_is_Default_for_type_validator_should_fail_datetime(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.DateOfBirth).not_empty())

        result = validator.validate(Person(DateOfBirth=datetime.datetime.min))
        self.assertFalse(result.is_valid)

    def test_When_value_is_Default_for_type_validator_should_fail_int(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).not_empty())

        result = validator.validate(Person(Id=0))
        self.assertFalse(result.is_valid)

        result1 = validator.validate(Person(Id=1))
        self.assertTrue(result1.is_valid)

    def test_Fails_when_collection_empty(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Children).not_empty())

        result = validator.validate(Person(Children=[]))
        self.assertFalse(result.is_valid)

    def test_When_validation_fails_error_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        result = validator.validate(Person(Surname=None))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must not be empty.")

    def test_Fails_for_ienumerable_that_doesnt_implement_ICollection(self):
        validator = InlineValidator(TestModel, lambda v: v.rule_for(lambda x: x.Strings).not_empty())

        result = validator.validate(TestModel())
        self.assertFalse(result.is_valid)

    def test_Fails_for_array(self):
        validator = InlineValidator(list)
        validator.rule_for(lambda x: x).not_empty()
        result = validator.validate([])
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
