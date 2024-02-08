import unittest

from person import Person
from TestValidator import TestValidator
import sys
from pathlib import Path

sys.path.append(
    [str(x) for x in Path(__file__).parents if x.name == "FluentValidation"].pop()
)

from src.FluentValidation.validators.LengthValidator import LengthValidator  # noqa: E402


class LengthValidatorTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_When_the_text_is_between_the_range_specified_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(1, 10)
        )
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_between_the_lambda_range_specified_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(
                lambda x: x.MinLength, lambda x: x.MaxLength
            )
        )
        result = validator.validate(Person(Surname="Test", MinLength=1, MaxLength=10))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_smaller_than_the_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(5, 10)
        )
        result = validator.validate(Person(Surname="Test"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_smaller_than_the_lambda_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(
                lambda x: x.MinLength, lambda x: x.MaxLength
            )
        )
        result = validator.validate(Person(Surname="Test", MinLength=5, MaxLength=10))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Length(1, 2))
        result = validator.validate(Person(Surname="Test"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_lambda_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(
                lambda x: x.MinLength, lambda x: x.MaxLength
            )
        )
        result = validator.validate(Person(Surname="Test", MinLength=1, MaxLength=2))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_upper_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Length(1, 4))
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lambda_upper_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(
                lambda x: x.MinLength, lambda x: x.MaxLength
            )
        )
        result = validator.validate(Person(Surname="Test", MinLength=1, MaxLength=4))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lower_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Length(4, 5))
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lambda_lower_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).Length(
                lambda x: x.MinLength, lambda x: x.MaxLength
            )
        )
        result = validator.validate(Person(Surname="Test", MinLength=4, MaxLength=5))
        self.assertTrue(result.is_valid)

    def test_When_the_max_is_smaller_than_the_min_then_the_validator_should_throw(self):
        with self.assertRaises(Exception):
            TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Length(10, 1))

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Length(1, 2))
        result = validator.validate(Person(Surname="Gire and gimble in the wabe"))
        self.assertEqual(
            result.errors[0].ErrorMessage,
            "'Surname' must be between 1 and 2 characters. You entered 27 characters.",
        )

    def test_Min_and_max_properties_should_be_set(self):
        validator = LengthValidator[Person](1, 5)
        self.assertEqual(validator.Min, 1)
        self.assertEqual(validator.Max, 5)

    def test_When_input_is_null_then_the_validator_should_pass(self):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname).ExactLength(5)
        )  # can't use Length method due to the lack of overload in Python
        result = validator.validate(Person(Surname=None))
        self.assertTrue(result.is_valid)

    def test_When_the_minlength_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).MinLength(4))
        result = validator.validate(Person(Surname="abc"))
        self.assertEqual(
            result.errors[0].ErrorMessage,
            "The length of 'Surname' must be at least 4 characters. You entered 3 characters.",
        )

    def test_When_the_maxlength_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).MaxLength(4))
        result = validator.validate(Person(Surname="abcde"))
        self.assertEqual(
            result.errors[0].ErrorMessage,
            "The length of 'Surname' must be 4 characters or fewer. You entered 5 characters.",
        )


if __name__ == "__main__":
    unittest.main()