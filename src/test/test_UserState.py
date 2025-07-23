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

from fluent_validation.IValidationContext import ValidationContext

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from TestValidator import TestValidator
from person import Person


class UserStateTester(unittest.TestCase):
    def setUp(self):
        self.validator = TestValidator()

    def test_Stores_user_state_against_validation_failure(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_state(lambda x: "foo")
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].CustomState, "foo")

    def test_Throws_when_provider_is_null(self):
        with self.assertRaises(TypeError):
            self.validator.rule_for(lambda x: x.Surname).not_null().with_state(None)

    def test_Correctly_provides_object_being_validated(self):
        result_person = None

        def state_provider(x):
            nonlocal result_person
            result_person = x
            return object()

        self.validator.rule_for(lambda x: x.Surname).not_null().with_state(state_provider)

        person = Person()
        self.validator.validate(person)

        self.assertIs(result_person, person)

    def test_Can_provide_state_for_item_in_collection(self):
        self.validator.rule_for_each(lambda x: x.Children).not_null().with_state(lambda person, child: "test")
        result = self.validator.validate(Person(Children=[None]))
        self.assertEqual(str(result.errors[0].CustomState), "test")

    def test_Can_provide_state_from_validation_context(self):
        person = Person()
        
        self.validator.rule_for(lambda e: e.Surname).not_null().with_state(lambda p, surname,ctx: (p,surname,ctx.RootContextData['test']))

        context = ValidationContext(person)
        context.RootContextData['test'] = 'foo'
        result = self.validator.validate(context)

        custom_state = result.errors[0].CustomState
        self.assertIs(custom_state[0], person)
        self.assertIsNone(custom_state[1])  # surname should be None
        self.assertEqual(custom_state[2], "foo")


if __name__ == "__main__":
    unittest.main()
