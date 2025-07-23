from typing import Callable
import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from person import Order, Person

from fluent_validation.abstract_validator import AbstractValidator
from fluent_validation.InlineValidator import InlineValidator


class RulesetChildRulesValidator(AbstractValidator[Person]):
    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_set(
            "testing",
            lambda: (
                self.rule_for(lambda a: a.Surname).not_empty(),
                self.rule_for_each(lambda a: a.Orders).child_rules(
                    lambda child: child.rule_for(lambda o: o.ProductName).not_empty(),
                ),
            ),
        )


class RulesetChildValidatorRulesValidator(AbstractValidator[Person]):
    class RulesetOrderValidator(AbstractValidator[Order]):
        def __init__(self) -> None:
            super().__init__(Order)
            self.rule_set("b", lambda: (self.rule_for(lambda o: o.ProductName).not_empty()))

    def __init__(self) -> None:
        super().__init__(Person)
        self.rule_set(
            "a, b",
            lambda: (
                self.rule_for(lambda x: x.Surname).not_empty(),
                self.rule_for(lambda x: x).child_rules(lambda child: (child.rule_for_each(lambda o: o.Orders).set_validator(self.RulesetOrderValidator()))),
            ),
        )

    class Foo:
        def __init__(self):
            self.Names: list[str] = []

    class Bar:
        def __init__(self):
            self.Foos: list[RulesetChildValidatorRulesValidator.Foo] = []

    class Baz:
        def __init__(self):
            self.Bars: list[RulesetChildValidatorRulesValidator.Bar] = []


class Root:
    def __init__(self):
        self.Data: Bar = None


class Base:
    def __init__(self) -> None:
        self.Value: int = None


class Bar(Base):
    def __init__(self) -> None:
        super().__init__()
        self.BarValue: int = None


class RootValidator(AbstractValidator[Root]):
    def __init__(self) -> None:
        super().__init__(Root)
        self.rule_for(lambda x: x).child_rules(self.RootRules())

    @classmethod
    def BaseRules(cls) -> Callable[[InlineValidator[Base]], None]:
        return lambda rules: rules.rule_for(lambda x: x.Value).not_equal(-1)

    @classmethod
    def RootRules(cls) -> Callable[[InlineValidator[Root]], None]:
        return lambda rules: rules.rule_for(lambda x: x.Data).child_rules(cls.BaseRules())


class ChildRulesTests(unittest.TestCase):
    def test_Can_define_nested_rules_for_collection(self):
        validator = InlineValidator[Person](Person)

        validator.rule_for_each(lambda x: x.Orders).child_rules(
            lambda order: (
                order.rule_for(lambda x: x.ProductName).not_null(),
                order.rule_for(lambda x: x.Amount).greater_than(0),
            )
        )

        result = validator.validate(
            Person(
                Orders=[
                    Order(ProductName=None, Amount=10),
                    Order(ProductName="foo", Amount=0),
                    Order(ProductName="foo", Amount=10),
                ]
            )
        )

        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].PropertyName, "Orders[0].ProductName")
        self.assertEqual(result.errors[1].PropertyName, "Orders[1].Amount")

    def test_ChildRules_works_with_RuleSet(self):
        validator = RulesetChildRulesValidator()

        # As Child Rules are implemented as a child validator, the child rules are technically
        # not inside the "testing" ruleset (going by the usual way rulesets cascade).
        # However, child rules should still be executed.
        result = validator.validate(Person(Orders=[Order()]), lambda options: options.IncludeRuleSets("testing"))

        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.errors[0].PropertyName, "Surname")
        self.assertEqual(result.errors[1].PropertyName, "Orders[0].ProductName")

        # They shouldn't be executed if a different ruleset is chosen.
        result = validator.validate(Person(Orders=[Order()]), lambda options: options.IncludeRuleSets("other"))
        self.assertEqual(len(result.errors), 0)

    # def test_ChildRules_works_with_SetValidator_and_RuleSet(self):
    # 	validator = RulesetChildValidatorRulesValidator()

    # 	# If the validator inside a child rule specifies a rule set "b",
    # 	# the rules inside the rule set "b" should not be used for the validation
    # 	# if the validation context specified the ruleset "a"
    # 	result = validator.validate(Person {
    # 		Orders = [
    # 			Order()
    # 		}
    # 	}, lambda options: options.IncludeRuleSets("a"))

    # 	self.assertEqual(len(result.errors),1)
    # 	self.assertEqual(result.errors[0].PropertyName,"Surname")
    # }

    # def test_Multiple_levels_of_nested_child_rules_in_ruleset(self):
    # 	validator = InlineValidator<RulesetChildValidatorRulesValidator.Baz>()
    # 	validator.rule_set("Set1", lambda:(
    # 		validator.rule_for_each(baz => baz.Bars)
    # 			.child_rules(barRule => barRule.rule_for_each(bar => bar.Foos)
    # 				.child_rules(fooRule => fooRule.rule_for_each(foo => foo.Names)
    # 					.child_rules(name => name.rule_for(n => n)
    # 						.not_empty()
    # 						.WithMessage("Name is required"))))
    # 	})

    # 	foos = self.oo:list[RulesetChildValidatorRulesValidator] = []
    # 		new() { Names = { "Bob" }},
    # 		new() { Names = { string.Empty }},
    # 	}

    # 	bars = self.ar:list[RulesetChildValidatorRulesValidator] = []
    # 		new(),
    # 		new() { Foos = foos }
    # 	}

    # 	baz = RulesetChildValidatorRulesValidator.Baz {
    # 		Bars = bars
    # 	}

    # 	result = validator.validate(baz, lambda options: options.IncludeRuleSets("Set1"))
    # 	result.is_valid.ShouldBeFalse()
    # }

    # def test_Doesnt_throw_InvalidCastException(self):
    # 	# FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # 	# See https://github.com/p-hzamora/FluentValidation/issues/2165
    # 	validator = RootValidator()
    # 	_root = Root()
    # 	_root.Data = Bar()
    # 	_root.Data.Value = -1
    # 	result = validator.validate(_root)
    # 	self.assertEqual(len(result.errors), 1)


if __name__ == "__main__":
    unittest.main()
