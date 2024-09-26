from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional
import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Country, Order, Payment, Person, _Address as Address
from fluent_validation.InlineValidator import InlineValidator


@dataclass
class TestObject:
    SomeProperty: Any = None
    SomeOtherProperty: Any = None
    SomeNullableProperty: Optional[Decimal] = None


class ValidatorSelectorTests(unittest.TestCase):
    def setUp(self) -> None:
        CultureScope.SetDefaultCulture()

    def test_MemberNameValidatorSelector_returns_true_when_property_name_matches(self):
        validator = InlineValidator[TestObject](TestObject, lambda v: v.rule_for(lambda x: x.SomeProperty).not_null())

        result = validator.validate(TestObject(), lambda v: v.IncludeProperties("SomeProperty"))
        self.assertEqual(len(result.errors), 1)

    def test_Does_not_validate_other_property(self):
        validator = InlineValidator[TestObject](TestObject, lambda v: v.rule_for(lambda x: x.SomeOtherProperty).not_null())

        result = validator.validate(TestObject(), lambda v: v.IncludeProperties("SomeProperty"))
        self.assertEqual(len(result.errors), 0)

    def test_validates_property_using_expression(self):
        validator = InlineValidator[TestObject](TestObject, lambda v: v.rule_for(lambda x: x.SomeProperty).not_null())

        result = validator.validate(TestObject(), lambda v: v.IncludeProperties(lambda x: x.SomeProperty))
        self.assertEqual(len(result.errors), 1)

    def test_Does_not_validate_other_property_using_expression(self):
        validator = InlineValidator[TestObject](
            TestObject,
            lambda v: v.rule_for(lambda x: x.SomeOtherProperty).not_null(),
        )

        result = validator.validate(TestObject(), lambda v: v.IncludeProperties(lambda x: x.SomeProperty))
        self.assertEqual(len(result.errors), 0)

    def test_validates_nullable_property_with_overriden_name_when_selected(self):
        validator = InlineValidator[TestObject](
            TestObject,
            lambda v: v.rule_for(lambda x: x.SomeNullableProperty).greater_than(Decimal("0")).when(lambda x: x.SomeNullableProperty is not None).override_property_name("SomeNullableProperty"),
        )

        result = validator.validate(TestObject(SomeNullableProperty=Decimal("0")), lambda v: v.IncludeProperties(lambda x: x.SomeNullableProperty))
        self.assertEqual(len(result.errors), 1)

    def test_Includes_nested_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null(), lambda v: v.rule_for(lambda x: x.Address.Id).not_equal(0))

        result = validator.validate(Person(Address=Address()), lambda v: v.IncludeProperties("Address.Id"))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Address.Id")

    def test_Includes_nested_property_using_expression(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null(), lambda v: v.rule_for(lambda x: x.Address.Id).not_equal(0))

        result = validator.validate(Person(Address=Address()), lambda v: v.IncludeProperties(lambda x: x.Address.Id))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Address.Id")

    def test_Can_use_property_with_include(self):
        validator = TestValidator()
        validator2 = TestValidator()
        validator2.rule_for(lambda x: x.Forename).not_null()

        validator.Include(validator2)

        result = validator.validate(Person(), lambda v: v.IncludeProperties("Forename"))
        self.assertFalse(result.is_valid)

    def test_Executes_correct_rule_when_using_property_with_include(self):
        validator = TestValidator()
        validator2 = TestValidator()
        validator2.rule_for(lambda x: x.Forename).not_null()
        validator2.rule_for(lambda x: x.Surname).not_null()
        validator.Include(validator2)

        result = validator.validate(Person(), lambda v: v.IncludeProperties("Forename"))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Forename")

    # async def test_Executes_correct_rule_when_using_property_with_include_async(self):
    # 	validator = TestValidator()
    # 	validator2 = TestValidator()
    # 	validator2.rule_for(lambda x: x.Forename).not_null()
    # 	validator2.rule_for(lambda x: x.Surname).not_null()
    # 	validator.Include(validator2)

    # 	result = await validator.ValidateAsync(Person(), lambda v: v.IncludeProperties("Forename"))
    # 	self.assertEqual(len(result.errors),1)
    #   self.assertEqual( 	result.errors[0].PropertyName,"Forename")

    # def test_Executes_correct_rule_when_using_property_with_nested_includes(self):
    # 	validator3 = TestValidator()
    # 	validator3.rule_for(lambda x: x.Age).greater_than(0)

    # 	# In the middle validator ensure that the Include statement is
    # 	# before the additional rules in order to trigger the case reported in
    # 	# https://github.com/FluentValidation/FluentValidation/issues/1989
    # 	validator2 = TestValidator()
    # 	validator2.Include(validator3)
    # 	validator2.rule_for(lambda x: x.Orders).not_empty()

    # 	validator = TestValidator()
    # 	validator.Include(validator2)

    # 	# FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # 	result = validator.validate(Person(), lambda v: v.IncludeProperties("Age"))
    # 	self.assertEqual(len(result.errors),1)
    # 	self.assertEqual(result.errors[0].PropertyName,"Age")

    # 	result = validator.validate(Person(Age = 1), lambda v: v.IncludeProperties("Age"))
    # 	self.assertEqual(len(result.errors),0)

    def test_Only_validates_doubly_nested_property(self):
        person = Person(Address=Address(Country=Country()), Orders=[Order(Amount=5), Order(ProductName="Foo")])

        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Address.Country.Name).not_empty()

        # child_rules should not be included. Bug prior to 11.1.1 meant that child_rules were
        # incorrectly included for execution.
        validator.rule_for_each(lambda x: x.Orders).child_rules(
            lambda x: (
                x.rule_for(lambda y: y.Amount).greater_than(6),
                x.rule_for(lambda y: y.ProductName).min_length(5),
            )
        )

        result = validator.validate(person, lambda options: options.IncludeProperties("Address.Country.Name"))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Address.Country.Name")
        self.assertEqual(result.errors[0].ErrorMessage, "'Address Country Name' must not be empty.")

    def test_Only_validates_child_property_for_single_item_in_collection(self):
        person = Person(
            Address=Address(Country=Country()),
            Orders=[
                Order(Amount=5),
                Order(ProductName="Foo"),
            ],
        )

        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Address.Country.Name).not_empty()
        validator.rule_for_each(lambda x: x.Orders).child_rules(
            lambda x: (
                x.rule_for(lambda y: y.Amount).greater_than(6),
                x.rule_for(lambda y: y.ProductName).min_length(5),
            )
        )

        result = validator.validate(person, lambda opt: opt.IncludeProperties("Orders[1].Amount"))
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].PropertyName, "Orders[1].Amount")
        self.assertEqual(result.errors[0].ErrorMessage, "'Amount' must be greater than '6'.")

    def test_Only_validates_single_child_property_of_all_elements_in_collection(self):
        person = Person(
            Address=Address(Country=Country()),
            Orders=[
                Order(Amount=5),
                Order(ProductName="Foo"),
                Order(Amount=10),
            ],
        )

        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Address.Country.Name).not_empty()
        validator.rule_for_each(lambda x: x.Orders).child_rules(
            lambda x: (
                x.rule_for(lambda y: y.Amount).greater_than(6),
                x.rule_for(lambda y: y.ProductName).min_length(5),
            )
        )

        # FIXME [x]: does not working when use '[]' wildcard
        result = validator.validate(person, lambda opt: opt.IncludeProperties("Orders[].Amount"))
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].PropertyName, "Orders[0].Amount")
        self.assertEqual(result.errors[0].ErrorMessage, "'Amount' must be greater than '6'.")
        self.assertEqual(result.errors[1].PropertyName, "Orders[1].Amount")
        self.assertEqual(result.errors[1].ErrorMessage, "'Amount' must be greater than '6'.")

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Only_validates_single_child_property_of_all_elements_in_nested_collection(self):
    #     person = Person(
    #         Orders=[
    #             Order(
    #                 Amount=5,
    #                 Payments=[
    #                     Payment(Amount=0),
    #                 ],
    #             ),
    #             Order(
    #                 ProductName="Foo",
    #                 Payments=[
    #                     Payment(Amount=1),
    #                     Payment(Amount=0),
    #                 ],
    #             ),
    #         ],
    #     )

    #     validator = InlineValidator[Person](Person)
    #     validator.rule_for_each(lambda x: x.Orders).child_rules(
    #         lambda x: (
    #             x.rule_for(lambda y: y.Amount).greater_than(6),
    #             x.rule_for_each(lambda y: y.Payments).child_rules(
    #                 lambda a: (
    #                     a.rule_for(
    #                         lambda b: b.Amount,
    #                     ).greater_than(0)
    #                 )
    #             ),
    #         )
    #     )

    #     result = validator.validate(person, lambda opt: opt.IncludeProperties("Orders[].Payments[].Amount"))
    #     self.assertEqual(len(result.errors), 2)
    #     self.assertEqual(result.errors[0].PropertyName, "Orders[0].Payments[0].Amount")
    #     self.assertEqual(result.errors[0].ErrorMessage, "'Amount' must be greater than '0'.")
    #     self.assertEqual(result.errors[1].PropertyName, "Orders[1].Payments[1].Amount")
    #     self.assertEqual(result.errors[1].ErrorMessage, "'Amount' must be greater than '0'.")


if __name__ == "__main__":
    unittest.main()
