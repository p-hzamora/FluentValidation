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

from fluent_validation.InlineValidator import InlineValidator
from fluent_validation import AbstractValidator, CascadeMode as _CascadeMode
from TestValidator import TestValidator
from person import Country, IAddress, Person, Order, _Address as Address


class Department:
    def __init__(
        self,
        Manager: Person = None,
        Assistant: Person = None,
        Employees: None | list[Person] = None,
    ) -> None:
        self.Manager: Person = Manager
        self.Assistant: Person = Assistant
        self.Employees: None | list[Person] = Employees


class DepartmentValidator(AbstractValidator[Department]):
    def __init__(self) -> None:
        super().__init__(Department)
        self.CascadeMode = _CascadeMode.Stop  # _CascadeMode.StopOnFirstFailure
        self.rule_for(lambda x: x.Manager).not_null()
        self.rule_for(lambda x: x.Assistant.Surname).not_equal(lambda x: x.Manager.Surname).when(lambda x: x.Assistant is not None and x.Manager.Surname is not None)


class PersonValidator(InlineValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_for(lambda x: x.Forename).not_null()
        self.when(
            lambda x: x.Address is not None,
            lambda: (
                self.rule_for(lambda x: x.Address.Postcode).not_null(),
                self.rule_for(lambda x: x.Address.Country.Name).not_null().when(lambda x: x.Address.Country is not None),
                self.rule_for(lambda x: x.Address.Line1).not_null().when(lambda x: x.Address.Line2 is not None),
            ),
        )


class ChainedValidationTester(unittest.TestCase):
    def setUp(self):
        self.validator: PersonValidator = PersonValidator()
        self.person: Person = Person(Address=Address(Country=Country()), Orders=[Order(Amount=5), Order(ProductName="Foo")])

    def test_Validates_chained_property(self):
        results = self.validator.validate(self.person)

        self.assertEqual(len(results.errors), 3)
        self.assertEqual(results.errors[0].PropertyName, "Forename")
        self.assertEqual(results.errors[1].PropertyName, "Address.Postcode")
        self.assertEqual(results.errors[2].PropertyName, "Address.Country.Name")

    def test_Chained_validator_should_not_be_invoked_on_null_property(self):
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    def test_Should_allow_normal_rules_and_chained_property_on_same_property(self):
        self.validator.rule_for(lambda x: x.Address.Line1).not_null()
        result = self.validator.validate(self.person)
        self.assertEqual(len(result.errors), 4)

    def test_Explicitly_included_properties_should_be_propagated_to_nested_validators(self):
        results = self.validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Address))
        self.assertEqual(len(results.errors), 2)
        self.assertEqual(results.errors[0].PropertyName, "Address.Postcode")
        self.assertEqual(results.errors[-1].PropertyName, "Address.Country.Name")

    def test_Explicitly_included_properties_should_be_propagated_to_nested_validators_using_strings(self):
        results = self.validator.validate(self.person, lambda v: v.IncludeProperties("Address"))
        self.assertEqual(len(results.errors), 2)
        self.assertEqual(results.errors[0].PropertyName, "Address.Postcode")
        self.assertEqual(results.errors[-1].PropertyName, "Address.Country.Name")

    def test_Chained_property_should_be_excluded(self):
        results = self.validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Surname))
        self.assertEqual(len(results.errors), 0)

    def test_Condition_should_work_with_chained_property(self):
        person = Person(Address=Address(Line2="foo"))

        result = self.validator.validate(person)
        self.assertEqual(len(result.errors), 3)
        self.assertEqual(result.errors[-1].PropertyName, "Address.Line1")

    def test_Can_validate_using_validator_for_base_type(self):
        addressValidator = InlineValidator[IAddress](IAddress)
        addressValidator.rule_for(lambda x: x.Line1).not_null()

        validator = TestValidator()
        validator.rule_for(lambda x: x.Address).set_validator(addressValidator)

        result = self.validator.validate(Person(Address=Address()))
        self.assertFalse(result.is_valid)

    def test_Separate_validation_on_chained_property(self):
        validator = DepartmentValidator()
        result = validator.validate(Department(Manager=Person(), Assistant=Person()))
        self.assertTrue(result.is_valid)

    def test_Separate_validation_on_chained_property_valid(self):
        validator = DepartmentValidator()
        result = validator.validate(Department(Manager=Person(Surname="foo")))
        self.assertTrue(result.is_valid)

    def test_Separate_validation_on_chained_property_conditional(self):
        validator = DepartmentValidator()
        result = validator.validate(Department(Manager=Person(Surname="foo"), Assistant=Person(Surname="foo")))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Assistant.Surname")

    # def test_Chained_validator_descriptor(self):
    # 	descriptor = self.validator.CreateDescriptor()

    # 	members = descriptor.GetMembersWithValidators().ToList()
    # 	members.Count.ShouldEqual(4)
    # 	members[0].Key.ShouldEqual("Forename")
    # 	members[1].Key.ShouldEqual("Address.Postcode")
    # 	members[2].Key.ShouldEqual("Address.Country.Name")
    # 	members[3].Key.ShouldEqual("Address.Line1")

    def test_Uses_explicit_ruleset(self):
        addressValidator = InlineValidator[Address](Address)
        addressValidator.rule_set("ruleset1", lambda: (addressValidator.rule_for(lambda x: x.Line1).not_null()))
        addressValidator.rule_for(lambda x: x.Line2).not_null()
        self.validator = InlineValidator[Person](Person)
        self.validator.rule_for(lambda x: x.Address).set_validator(addressValidator, "ruleset1")

        result = self.validator.validate(Person(Address=Address()))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Address.Line1")


if __name__ == "__main__":
    unittest.main()
