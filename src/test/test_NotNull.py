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

from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class NotNullTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

    def test_NotNullValidator_should_pass_if_value_has_value(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname="Foo"))
        self.assertTrue(result.is_valid)

    def test_NotNullValidator_should_fail_if_value_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname=None))
        self.assertFalse(result.is_valid)

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname=None))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must not be empty.")

    def test_Not_null_validator_should_not_crash_with_non_nullable_value_type(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).not_null())
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Fails_when_nullable_value_type_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).not_null())
        result = validator.validate(Person())
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
