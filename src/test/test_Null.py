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

import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.InlineValidator import InlineValidator
from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class NullTester(unittest.TestCase):
    def setUp(sefl):
        CultureScope.SetDefaultCulture()

    def test_NullValidator_should_fail_if_value_has_value(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).null())
        result = validator.validate(Person(Surname="Foo"))
        self.assertFalse(result.is_valid)

    def test_NullValidator_should_pass_if_value_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).null())
        result = validator.validate(Person(Surname=None))
        self.assertTrue(result.is_valid)

    def test_When_the_validator_passes_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).null())
        result = validator.validate(Person(Surname="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must be empty.")

    def test_Not_null_validator_should_not_crash_with_non_nullable_value_type(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).null())
        result = validator.validate(Person())
        self.assertFalse(result.is_valid)

    def test_Passes_when_nullable_value_type_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).null())
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_NullProperty_should_throw_NullReferenceException(self):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: len(x.Orders)).not_empty()

        with self.assertRaises(TypeError) as ex:
            validator.validate(Person(Orders=None))

        self.assertEqual(ex.exception.args[0], "TypeError occurred when executing rule for 'lambda x: len(x.Orders)'. If this property can be None you should add a null check using a when condition")
        self.assertIsNotNone(ex.exception)
        self.assertIsInstance(ex.exception, TypeError)

    def test_ForEachNullProperty_should_throw_NullReferenceException_when_exception_occurs(self):
        validator = InlineValidator[Person](Person)
        validator.rule_for_each(lambda x: x.Orders[0].Payments).not_null()

        with self.assertRaises(TypeError) as ex:
            validator.validate(Person(Orders=None))

        self.assertEqual(
            ex.exception.args[0],
            "TypeError occurred when executing rule for 'lambda x: x.Orders[0].Payments'. If this property can be None you should add a null check using a when condition",
        )
        self.assertIsNotNone(ex.exception)
        self.assertIsInstance(ex.exception, TypeError)


if __name__ == "__main__":
    unittest.main()
