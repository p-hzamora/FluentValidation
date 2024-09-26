from __future__ import annotations
import unittest
import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import ValidationResult
from fluent_validation.InlineValidator import InlineValidator


class Customer:
    def __init__(
        self,
        Id: int = 0,
        Name: str = None,
    ) -> None:
        self.Id: int = Id
        self.Name: str = Name

    def Validate(self) -> ValidationResult:
        Validator = InlineValidator[Customer](
            Customer,
            lambda v: v.rule_for(lambda x: x.Name).not_null(),
            lambda v: v.rule_for(lambda x: x.Id).not_equal(0),
        )
        return Validator.validate(self)


class InlineValidatorTester(unittest.TestCase):
    def test_Uses_inline_validator_to_build_rules(self):
        cust = Customer()
        result = cust.Validate()

        self.assertEqual(len(result.errors), 2)


if __name__ == "__main__":
    unittest.main()
