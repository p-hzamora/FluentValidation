from __future__ import annotations
from typing import Optional
import unittest

import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.abstract_validator import AbstractValidator
from fluent_validation.internal.PropertyChain import PropertyChain
from fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
from fluent_validation.results.ValidationResult import ValidationResult
from person import _Address as Address, Order
from person import Person


class RulesetTests(unittest.TestCase):
    def AssertExecuted(self, result: ValidationResult, *names: str) -> None:
        len_names = len(names)
        self.assertEqual(len(result.RuleSetsExecuted), len_names)
        self.assertEqual(len(set(result.RuleSetsExecuted) & set(names)), len_names)

    def test_Executes_rules_in_specified_ruleset(self):
        validator = TestValidator()
        result = validator.validate(ValidationContext[Person](Person(), PropertyChain(), RulesetValidatorSelector(["Names"])))

        self.assertEqual(len(result.errors), 2)  # 2 rules in this ruleset
        self.AssertExecuted(result, "Names")

    def test_Executes_rules_not_specified_in_ruleset(self):
        validator = TestValidator()
        result = validator.validate(Person())

        self.assertEqual(len(result.errors), 1)  # 1 rule not inside a ruleset
        self.AssertExecuted(result, "default")

    def test_Ruleset_cascades_to_child_validator(self):
        addressValidator = InlineValidator[Address](Address)
        addressValidator.rule_set("Test", lambda: addressValidator.rule_for(lambda x: x.Line1).not_null())

        validator = TestValidator()

        validator.rule_set("Test", lambda: validator.rule_for(lambda x: x.Address).set_validator(addressValidator))

        person = Person(Address=Address())

        result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(["Test"])))

        self.assertEqual(len(result.errors), 1)
        self.AssertExecuted(result, "Test")

    def test_Ruleset_cascades_to_child_collection_validator(self):
        orderValidator = InlineValidator[Order](Order)
        orderValidator.rule_set("Test", lambda: {orderValidator.rule_for(lambda x: x.ProductName).not_null()})

        validator = TestValidator()

        validator.rule_set("Test", lambda: {validator.rule_for_each(lambda x: x.Orders).set_validator(orderValidator)})

        person = Person(Orders=[Order(), Order()])

        result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(["Test"])))

        self.assertEqual(len(result.errors), 2)  # one for each order
        self.AssertExecuted(result, "Test")

    def test_Executes_multiple_rulesets(self):
        validator = TestValidator()
        validator.rule_set("Id", lambda: {validator.rule_for(lambda x: x.Id).not_equal(0)})

        person = Person()
        result = validator.validate(ValidationContext[Person](person, PropertyChain(), RulesetValidatorSelector(["Names", "Id"])))

        self.assertEqual(len(result.errors), 3)
        self.AssertExecuted(result, "Names", "Id")

    def test_Executes_all_rules(self):
        validator = TestValidator()
        person = Person()
        result = validator.validate(person, lambda v: v.IncludeAllRuleSets())
        self.assertEqual(len(result.errors), 3)
        self.AssertExecuted(result, "Names", "default")

    def test_Executes_rules_in_default_ruleset_and_specific_ruleset(self):
        validator = TestValidator()
        validator.rule_set("foo", lambda: {validator.rule_for(lambda x: x.Age).not_equal(0)})

        result = validator.validate(Person(), lambda v: v.IncludeRulesNotInRuleSet().IncludeRuleSets("Names"))
        self.assertEqual(len(result.errors), 3)
        self.AssertExecuted(result, "default", "Names")

    def test_WithMessage_works_inside_rulesets(self):
        validator = TestValidator2()
        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Names"))
        self.assertEqual("foo", result.errors[0].ErrorMessage)
        self.AssertExecuted(result, "Names")

    def test_Ruleset_selection_should_not_cascade_downwards_when_set_on_property(self):
        validator = TestValidator4()
        person_container = PersonContainer()
        person_container.Person = Person()
        result = validator.validate(person_container, lambda v: v.IncludeRuleSets("Names"))
        self.assertTrue(result.is_valid)
        self.AssertExecuted(result)

    def test_Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement(self):
        validator = TestValidator3()
        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Names"))
        self.assertFalse(result.is_valid)
        self.AssertExecuted(result, "Names")

    def test_Ruleset_selection_should_cascade_downwards_with_when_setting_child_validator_using_include_statement_with_lambda(self):
        validator = InlineValidator[Person](Person)
        validator.Include(lambda x: TestValidator2())
        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Names"))
        self.assertFalse(result.is_valid)

    def test_Trims_spaces(self):
        validator = InlineValidator[Person](Person)
        validator.rule_set("First", lambda: {validator.rule_for(lambda x: x.Forename).not_null()})
        validator.rule_set("Second", lambda: {validator.rule_for(lambda x: x.Surname).not_null()})

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("First", "Second"))
        self.assertEqual(len(result.errors), 2)
        self.AssertExecuted(result, "First", "Second")

    def test_Applies_multiple_rulesets_to_rule(self):
        validator = InlineValidator[Person](Person)
        validator.rule_set("First, Second", lambda: validator.rule_for(lambda x: x.Forename).not_null())

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("First"))
        self.assertEqual(len(result.errors), 1)
        self.AssertExecuted(result, "First")

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Second"))
        self.assertEqual(len(result.errors), 1)
        self.AssertExecuted(result, "Second")

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Third"))
        self.assertEqual(len(result.errors), 0)
        self.AssertExecuted(result)

        result = validator.validate(Person())
        self.assertEqual(len(result.errors), 0)
        self.AssertExecuted(result, "default")

    def test_Executes_in_rule_in_ruleset_and_default(self):
        validator = InlineValidator[Person](Person)
        validator.rule_set("First, Default", lambda: {validator.rule_for(lambda x: x.Forename).not_null()})

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("First"))
        self.assertEqual(len(result.errors), 1)
        self.AssertExecuted(result, "First")

        result = validator.validate(Person(), lambda v: v.IncludeRuleSets("Second"))
        self.assertEqual(len(result.errors), 0)
        self.AssertExecuted(result)

        result = validator.validate(Person())
        self.assertEqual(len(result.errors), 1)
        self.AssertExecuted(result, "default")

    def test_Executes_in_rule_in_default_and_none(self):
        validator = InlineValidator[Person](Person)
        # FIXME [x]: Fails because of 'rule_set' is case-sensitive. Must be case-insensitive
        validator.rule_set("First, Default", lambda: validator.rule_for(lambda x: x.Forename).not_null())
        validator.rule_for(lambda x: x.Forename).not_null()

        result = validator.validate(Person(), lambda v: v.IncludeRulesNotInRuleSet())
        self.assertEqual(len(result.errors), 2)
        self.AssertExecuted(result, "default")

    def test_Combines_rulesets_and_explicit_properties(self):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Forename).not_null()
        validator.rule_for(lambda x: x.Surname).not_null()
        validator.rule_set("Test", lambda: validator.rule_for(lambda x: x.Age).greater_than(0))

        result = validator.validate(
            Person(),
            lambda options: (
                options.IncludeRuleSets("Test"),
                options.IncludeProperties(lambda x: x.Forename),
            ),
        )

        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].PropertyName, "Forename")
        self.assertEqual(result.errors[1].PropertyName, "Age")

    #     def test_Task(selfC:bines_rulesets_and_explicit_properties_async() {
    #         validator = InlineValidator[Person](Person)
    #         validator.rule_for(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
    #         validator.rule_for(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
    #         validator.rule_set("Test", lambda: {
    #             validator.rule_for(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
    #         })

    #         result = await validator.validateAsync(Person(), lambda options:{
    #             options.IncludeRuleSets("Test")
    #             options.IncludeProperties(lambda x: x.Forename)
    #         })

    #         result.Errors.Count.ShouldEqual(2)
    #         result.Errors[0].PropertyName.ShouldEqual("Forename")
    #         result.Errors[1].PropertyName.ShouldEqual("Age")
    #     }

    def test_Includes_combination_of_rulesets(self):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Forename).not_null()
        validator.rule_set("Test1", lambda: validator.rule_for(lambda x: x.Surname).not_null())
        validator.rule_set("Test2", lambda: validator.rule_for(lambda x: x.Age).greater_than(0))

        result = validator.validate(Person(), lambda options: {options.IncludeRuleSets("Test1").IncludeRulesNotInRuleSet()})

        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].PropertyName, "Forename")
        self.assertEqual(result.errors[1].PropertyName, "Surname")

    #     def test_Task(selfI:ludes_combination_of_rulesets_async() {
    #         validator = InlineValidator[Person](Person)
    #         validator.rule_for(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
    #         validator.rule_set("Test1", lambda: {
    #             validator.rule_for(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
    #         })
    #         validator.rule_set("Test2", lambda: {
    #             validator.rule_for(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
    #         })

    #         result = await validator.validateAsync(Person(), lambda options:{
    #             options.IncludeRuleSets("Test1").IncludeRulesNotInRuleSet()
    #         })

    #         result.Errors.Count.ShouldEqual(2)
    #         result.Errors[0].PropertyName.ShouldEqual("Forename")
    #         result.Errors[1].PropertyName.ShouldEqual("Surname")
    #     }

    def test_Includes_all_rulesets(self):
        validator = InlineValidator[Person](Person)
        validator.rule_for(lambda x: x.Forename).not_null()
        validator.rule_set("Test1", lambda: validator.rule_for(lambda x: x.Surname).not_null())
        validator.rule_set("Test2", lambda: validator.rule_for(lambda x: x.Age).greater_than(0))

        result = validator.validate(Person(), lambda options: {options.IncludeAllRuleSets()})

        self.assertEqual(len(result.errors), 3)


#     def test_Task(selfI:ludes_all_rulesets_async() {
#         validator = InlineValidator[Person](Person)
#         validator.rule_for(lambda x: x.Forename).MustAsync((x,t) => Task.FromResult(x != null))
#         validator.rule_set("Test1", lambda: {
#             validator.rule_for(lambda x: x.Surname).MustAsync((x,t) => Task.FromResult(x != null))
#         })
#         validator.rule_set("Test2", lambda: {
#             validator.rule_for(lambda x: x.Age).MustAsync((x,t) => Task.FromResult(x > 0))
#         })

#         result = await validator.validateAsync(Person(), lambda options:{
#             options.IncludeAllRuleSets()
#         })

#         result.Errors.Count.ShouldEqual(3)
#     }


class TestValidator(InlineValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_set(
            "Names",
            lambda: (
                self.rule_for(lambda x: x.Surname).not_null(),
                self.rule_for(lambda x: x.Forename).not_null(),
            ),
        )

        self.rule_for(lambda x: x.Id).not_empty()


class TestValidator2(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_set("Names", lambda: self.rule_for(lambda x: x.Surname).not_null().with_message("foo"))


class TestValidator3(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)

        # TODOL: added Include method in AbstractValidator
        self.Include(TestValidator2())


class PersonContainer:
    def __init__(self) -> None:
        self._person: Person = None

    @property
    def Person(self) -> Person:
        return self._person

    @Person.setter
    def Person(self, value: Person) -> None:
        self._person = value


class TestValidator4(AbstractValidator[PersonContainer]):
    def __init__(self):
        super().__init__(PersonContainer)
        self.rule_for(lambda x: x.Person).set_validator(TestValidator2())


if __name__ == "__main__":
    unittest.main()
