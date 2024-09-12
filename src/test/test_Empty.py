from __future__ import annotations
import sys
from typing import Iterable
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.InlineValidator import InlineValidator
from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class EmptyTester(unittest.TestCase):
    def setUp(self) -> None:
        CultureScope.SetDefaultCulture()

    def test_When_there_is_a_value_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).empty())

        result = validator.validate(Person(Surname="Foo"))
        self.assertFalse(result.is_valid)

    def test_When_value_is_null_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).empty())

        result = validator.validate(Person(Surname=None))
        self.assertTrue(result.is_valid)

    def test_When_value_is_empty_string_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).empty())

        result = validator.validate(Person(Surname=""))
        self.assertTrue(result.is_valid)

    def test_When_value_is_whitespace_validation_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).empty())

        result = validator.validate(Person(Surname="         "))
        self.assertTrue(result.is_valid)

    def test_When_value_is_Default_for_type_validator_should_pass_datetime(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.DateOfBirth).empty())

        result = validator.validate(Person(DateOfBirth=None))  # DateOfBirth=default
        self.assertTrue(result.is_valid)

    def test_When_value_is_Default_for_type_validator_should_pass_int(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).empty())

        result = validator.validate(Person(Id=0))
        self.assertTrue(result.is_valid)

        result1 = validator.validate(Person(Id=1))
        self.assertFalse(result1.is_valid)

    def test_Passes_when_collection_empty(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Children).empty())

        result = validator.validate(Person(Children=list[Person]()))
        self.assertTrue(result.is_valid)

    def test_When_validation_fails_error_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).empty())

        result = validator.validate(Person(Surname="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must be empty.")

    def test_Passes_for_ienumerable_that_doesnt_implement_ICollection(self):
        validator = InlineValidator[TestModel]()
        validator.rule_for(lambda x: x.Strings).empty()

        result = validator.validate(TestModel())
        self.assertTrue(result.is_valid)


class TestModel:
    @property
    def Strings(self) -> Iterable[str]:
        return iter(())


if __name__ == "__main__":
    unittest.main()
