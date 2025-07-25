import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402

from fluent_validation.ValidatorOptions import ValidatorOptions  # noqa: E402, F401
from fluent_validation.validators.AbstractComparisonValidator import (  # noqa: E402
    Comparison,
    IComparisonValidator,  # noqa: F401
)
from fluent_validation.validators.LessThanOrEqualValidator import (  # noqa: E402
    LessThanOrEqualValidator,
)  # noqa: E402

from CultureScope import CultureScope  # noqa: E402


class LessThanOrEqualToValidatorTester(unittest.TestCase):
    value: int = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than_or_equal_to(self.value))

    def test_Should_fail_when_greater_than_input(self):
        result = self.validator.validate(Person(Id=2))
        self.assertFalse(result.is_valid)

    def test_Should_succeed_when_less_than_input(self):
        result = self.validator.validate(Person(Id=0))
        self.assertTrue(result.is_valid)

    def test_Should_succeed_when_equal_to_input(self):
        result = self.validator.validate(Person(Id=self.value))
        self.assertTrue(result.is_valid)

    def test_Should_set_default_error_when_validation_fails(self):
        result = self.validator.validate(Person(Id=2))
        self.assertEqual(result.errors[0].ErrorMessage, "'Id' must be less than or equal to '1'.")
        self.assertEqual(result.errors[0].ErrorMessage, "'Id' must be less than or equal to '1'.")

    def test_Comparison_type(self):
        self.assertEqual(
            LessThanOrEqualValidator[Person, int](self.value).Comparison,
            Comparison.LessThanOrEqual,
        )

    def test_Validates_with_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than_or_equal_to(lambda x: x.AnotherInt).with_message("{ComparisonProperty}"))
        result = validator.validate(Person(Id=1, AnotherInt=0))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "Another Int")

    def test_Comparison_property_uses_custom_resolver(self):
        originalResolver = ValidatorOptions.Global.DisplayNameResolver

        try:
            ValidatorOptions.Global.DisplayNameResolver = lambda type, member, exprlambda: member.Name + "Foo"
            validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than_or_equal_to(lambda x: x.AnotherInt).with_message("{ComparisonProperty}"))
            result = validator.validate(Person(Id=1, AnotherInt=0))
            self.assertEqual(result.errors[0].ErrorMessage, "AnotherIntFoo")

        finally:
            ValidatorOptions.Global.DisplayNameResolver = originalResolver

    def test_Validates_with_nullable_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).less_than_or_equal_to(lambda x: x.NullableInt))

        resultNull = validator.validate(Person(Id=0, NullableInt=None))
        resultLess = validator.validate(Person(Id=0, NullableInt=-1))
        resultEqual = validator.validate(Person(Id=0, NullableInt=0))
        resultMore = validator.validate(Person(Id=0, NullableInt=1))

        self.assertFalse(resultNull.is_valid)
        self.assertFalse(resultLess.is_valid)
        self.assertTrue(resultEqual.is_valid)
        self.assertTrue(resultMore.is_valid)

    def test_Validates_nullable_with_nullable_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(lambda x: x.OtherNullableInt))

        resultNull = validator.validate(Person(NullableInt=0, OtherNullableInt=None))
        resultLess = validator.validate(Person(NullableInt=0, OtherNullableInt=-1))
        resultEqual = validator.validate(Person(NullableInt=0, OtherNullableInt=0))
        resultMore = validator.validate(Person(NullableInt=0, OtherNullableInt=1))

        self.assertFalse(resultNull.is_valid)
        self.assertFalse(resultLess.is_valid)
        self.assertTrue(resultEqual.is_valid)
        self.assertTrue(resultMore.is_valid)

    def test_Validates_with_nullable_when_property_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(5))
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(5))
        result = validator.validate(Person(NullableInt=10))
        self.assertFalse(result.is_valid)

    def test_Validates_with_nullable_when_property_is_null_cross_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(lambda x: x.Id))
        result = validator.validate(Person(Id=5))
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null_cross_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(lambda x: x.Id))
        result = validator.validate(Person(NullableInt=10, Id=5))
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
