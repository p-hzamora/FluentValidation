import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from FluentValidation.validators.AbstractComparisonValidator import (  # noqa: E402
    Comparison,
    IComparisonValidator,
)
from FluentValidation.validators.LessThanValidator import LessThanValidator  # noqa: E402


class LessThanValidatorTester(unittest.TestCase):
    value: int = 1

    def test_Should_fail_when_greater_than_input(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(self.value))
        result = validator.validate(Person(Id=2))

        self.assertFalse(result.is_valid)

    def test_Should_succeed_when_less_than_input(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(self.value))

        result = validator.validate(Person(Id=0))
        self.assertTrue(result.is_valid)

    def test_Should_fail_when_equal_to_input(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(self.value))
        result = validator.validate(Person(Id=self.value))
        self.assertFalse(result.is_valid)

    def test_Should_set_default_validation_message_when_validation_fails(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(self.value))
        result = validator.validate(Person(Id=2))
        self.assertEqual(result.errors[0].ErrorMessage, "'Id' must be less than '1'.")

    def test_Validates_against_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(lambda x: x.AnotherInt).with_message(r"{ComparisonProperty}"))
        result = validator.validate(Person(Id=2, AnotherInt=1))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "Another Int")

    def test_Comparison_property_uses_custom_resolver(self) -> None:
        try:
            validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(lambda x: x.AnotherInt).with_message(r"ComparisonProperty"))
            result = validator.validate(Person(Id=2, AnotherInt=1))
            self.assertEqual(result.errors[0].ErrorMessage, "ComparisonProperty")
        finally:
            pass

    def test_Validates_with_nullable_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than(lambda x: x.NullableInt))

        resultNull = validator.validate(Person(Id=0, NullableInt=None))
        resultLess = validator.validate(Person(Id=0, NullableInt=-1))
        resultEqual = validator.validate(Person(Id=0, NullableInt=0))
        resultMore = validator.validate(Person(Id=0, NullableInt=1))

        self.assertFalse(resultNull.is_valid)  # ShouldBeFalse
        self.assertFalse(resultLess.is_valid)  # ShouldBeFalse
        self.assertFalse(resultEqual.is_valid)  # ShouldBeFalse
        self.assertTrue(resultMore.is_valid)  # ShouldBeTrue

    def test_Validates_nullable_with_nullable_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than(lambda x: x.OtherNullableInt))

        resultNull = validator.validate(Person(NullableInt=0, OtherNullableInt=None))
        resultLess = validator.validate(Person(NullableInt=0, OtherNullableInt=-1))
        resultEqual = validator.validate(Person(NullableInt=0, OtherNullableInt=0))
        resultMore = validator.validate(Person(NullableInt=0, OtherNullableInt=1))

        self.assertFalse(resultNull.is_valid)  # ShouldBeFalse()
        self.assertFalse(resultLess.is_valid)  # ShouldBeFalse()
        self.assertFalse(resultEqual.is_valid)  # ShouldBeFalse()
        self.assertTrue(resultMore.is_valid)  # ShouldBeTrue()

    def test_Extracts_property_from_constant_using_expression(self) -> None:
        validator: IComparisonValidator = LessThanValidator[Person, int](2)
        self.assertEqual(validator.ValueToCompare, 2)

    def test_Comparison_type(self) -> None:
        validator = LessThanValidator[Person, int](1)
        self.assertEqual(validator.Comparison, Comparison.less_than)

    def test_Validates_with_nullable_when_property_is_null(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than(5))
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than(5))
        result = validator.validate(Person(NullableInt=10))
        self.assertFalse(result.is_valid)

    def test_Validates_with_nullable_when_property_null_cross_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than(lambda x: x.Id))
        result = validator.validate(Person(Id=5))
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null_cross_property(
        self,
    ) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than(lambda x: x.Id))
        result = validator.validate(Person(NullableInt=10, Id=5))
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
