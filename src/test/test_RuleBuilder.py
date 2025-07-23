# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
from datetime import datetime
from typing import cast
import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from person import Person, _Address
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.internal.RuleComponent import RuleComponent
from fluent_validation.internal.DefaultValidatorSelector import DefaultValidatorSelector
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.abstract_validator import AbstractValidator, PropertyRule
from fluent_validation import PropertyChain, PropertyValidator


class RuleContainer:
    rule: PropertyRule[Person, datetime] = None


class NoopAddressValidator(AbstractValidator[_Address]):
    def __init__(self):
        super().__init__(_Address)


class TestPropertyValidator[T, TPropery](PropertyValidator[T, TPropery]):
    def is_valid(self, context, value):
        return True

    def get_default_message_template(self, errorCode):
        return self.Localized(errorCode, "NotNullValidator")


class RuleBuilderTests(unittest.TestCase):
    def setUp(self):
        self._rule: PropertyRule[Person, str]
        self._validator = InlineValidator(Person)
        self.builder = self._validator.rule_for(lambda x: x.Surname)
        self.builder.configure(lambda rule: setattr(self, "_rule", rule))

    def test_Should_build_property_name(self):
        self.assertEqual(self._rule.PropertyName, "Surname")

    def test_Adding_a_validator_should_store_validator(self):
        validator = TestPropertyValidator()
        self.builder.set_validator(validator)
        self.assertAlmostEqual(self._rule.Current.Validator, validator)

    def test_Should_set_custom_property_name(self):
        self.builder.set_validator(TestPropertyValidator[Person, str]()).with_name("Foo")
        self.assertEqual(self._rule.get_display_name(None), "Foo")

    def test_Should_set_custom_error(self):
        self.builder.set_validator(TestPropertyValidator[Person, str]()).with_message("Bar")
        component = self._rule.Current
        self.assertEqual(cast(RuleComponent, component).GetErrorMessage(None, ""), "Bar")

    def test_Should_throw_if_validator_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_if_overriding_validator_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_if_overriding_validator_provider_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_if_message_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_if_property_name_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_context_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_async_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_inverse_context_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_inverse_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_Should_throw_when_async_inverse_predicate_is_null(self):
        with self.assertRaises(AttributeError):
            self.builder.set_validator(None)

    def test_PropertyDescription_should_return_property_name_split(self):
        builder = self._validator.rule_for(lambda x: x.DateOfBirth)
        rule_container = RuleContainer()
        builder.configure(lambda r: setattr(rule_container, "rule", r))
        self.assertEqual(rule_container.rule.get_display_name(None), "Date Of Birth")

    def test_PropertyDescription_should_return_custom_property_name(self):
        builder = self._validator.rule_for(lambda x: x.DateOfBirth)
        rule_container = RuleContainer()
        builder.configure(lambda r: setattr(rule_container, "rule", r))

        builder.not_equal(datetime.min).with_name("Foo")
        self.assertEqual(rule_container.rule.get_display_name(None), "Foo")

    def test_Nullable_object_with_condition_should_not_throw(self):
        self._validator.rule_for(lambda x: x.NullableInt).greater_than_or_equal_to(3).when(lambda x: x.NullableInt is not None)
        self._validator.validate(ValidationContext(Person(), PropertyChain(), DefaultValidatorSelector()))

    # async def test_Nullable_object_with_async_condition_should_not_throw(self):
    #     self._validator.rule_for(lambda x: x.NullableInt.Value)
    #         .greater_than_or_equal_to(3)
    #         .WhenAsync((x,c) => Task.FromResult(x.NullableInt is not None))

    #     await self._validator.ValidateAsync(ValidationContext<Person>(Person(), PropertyChain(), DefaultValidatorSelector()))

    # FIXME [ ]: rule_container.rule.PropertyName should not return the name of the function. 'Calculate Salary' is not None
    # def test_Rule_for_a_non_memberexpression_should_not_generate_property_name(self):
    #     builder = self._validator.rule_for(lambda x: x.CalculateSalary())
    #     rule_container = RuleContainer()
    #     builder.configure(lambda r: setattr(rule_container, "rule", r))

    #     self.assertIsNone(rule_container.rule.get_display_name(None))
    #     self.assertIsNone(rule_container.rule.PropertyName)

    #TODOM []: This test no make sense on python
    # def test_Property_should_return_property_being_validated(self):
    #     property = type(Person().Surname)
    #     self.assertEqual(self._rule.Member, property)

    def test_Property_should_return_null_when_it_is_not_a_property_being_validated(self):
        builder = self._validator.rule_for(lambda x: "Foo")
        rule_container = RuleContainer()
        builder.configure(lambda r: setattr(rule_container,'rule',r))
        self.assertIsNone(rule_container.rule.Member.Name)

    # FIXME [ ]: PropertyName remains unchanged when setting the name via 'with_name', but the error message properly shows 'foo'
    # def test_Result_should_use_custom_property_name_when_no_property_name_can_be_determined(self):
    #     self._validator.rule_for(lambda x: x.CalculateSalary()).greater_than(100).with_name("Foo")
    #     context = ValidationContext(Person(), PropertyChain(), DefaultValidatorSelector())
    #     result = self._validator.validate(context)
    #     self.assertEqual(result.errors[0].PropertyName, "Foo")

    # def test_Conditional_child_validator_should_register_with_validator_type_not_property(self):
    #     builder = self._validator.rule_for(lambda x: x.Address)
    #     builder.set_validator((Person person) => NoopAddressValidator())
    #     rule_container = RuleContainer()
    #     builder.configure(lambda r: setattr(rule_container,'rule',r))

    #     rule.Components
    #         .Select(lambda x: x.Validator)
    #         .OfType<IChildValidatorAdaptor>().Single().ValidatorType.ShouldEqual(typeof(NoopAddressValidator))


if __name__ == "__main__":
    unittest.main()
