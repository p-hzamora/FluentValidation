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
from fluent_validation.internal.Resources.ILanguageManager import CultureInfo
from person import Person
from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.internal.MessageFormatter import MessageFormatter
from fluent_validation.InlineValidator import InlineValidator


class LocalisedMessagesTester(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

    def tearDown(self):
        CultureScope.SetDefaultCulture()

    def test_Correctly_assigns_default_localized_error_message(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_empty())

        cultures = ["en", "de", "fr", "es", "ca", "de", "it", "nl", "pl", "pt", "ru", "sv", "ar"]

        for culture in cultures:
            with CultureScope(culture) as scope:
                scope.set_CurrentUICulture(CultureInfo(culture))

                message = ValidatorOptions.Global.LanguageManager.GetString("NotEmptyValidator")
                error_message = MessageFormatter().AppendPropertyName("Surname").BuildMessage(message)

                result = validator.validate(Person(Surname=None))
                self.assertEqual(result.errors[0].ErrorMessage, error_message)

    def test_Uses_func_to_get_message(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Forename).not_null().with_message(lambda x: "el foo")

        result = validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "el foo")

    def test_Formats_string_with_placeholders(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Forename).not_null().with_message(lambda x: f"{{PropertyName}} {x.AnotherInt}")

        result = validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "Forename 0")

    def test_Formats_string_with_placeholders_when_you_cant_edit_the_string(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Forename).not_null().with_message(lambda x: f"{{PropertyName}} {x.AnotherInt}")

        result = validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "Forename 0")

    def test_Uses_string_format_with_property_value(self):
        validator = TestValidator()
        validator.rule_for(lambda x: x.Forename).equal("Foo").with_message(lambda x, forename: f"Hello {forename}")

        result = validator.validate(Person(Forename="Jeremy"))
        self.assertEqual(result.errors[0].ErrorMessage, "Hello Jeremy")

    def test_Does_not_throw_InvalidCastException_when_using_RuleForEach(self):
        validator = InlineValidator(Person)
        validator.rule_for_each(lambda x: x.NickNames).must(lambda x: False).with_message(lambda parent, name: "x")

        result = validator.validate(Person(NickNames=["What"]))
        self.assertEqual(result.errors[0].ErrorMessage, "x")


if __name__ == "__main__":
    unittest.main()
