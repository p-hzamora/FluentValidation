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


class MyResources:
    @staticmethod
    def CustomProperty():
        return "foo"


class LocalisedNameTester(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

    def tearDown(self):
        CultureScope.SetDefaultCulture()

    def test_Uses_localized_name(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null().with_name("foo"))

        result = validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "'foo' must not be empty.")

    def test_Uses_localized_name_expression(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null().with_name(lambda x: MyResources.CustomProperty()))

        result = validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "'foo' must not be empty.")


if __name__ == "__main__":
    unittest.main()
