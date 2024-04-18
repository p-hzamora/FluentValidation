import unittest

from person import Person
from TestValidator import TestValidator
from CultureScope import CultureScope
import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from FluentValidation.validators.LengthValidator import LengthValidator  # noqa: E402


class LengthValidatorTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

    def test_When_the_text_is_between_the_range_specified_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(1, 10))
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_between_the_lambda_range_specified_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(lambda x: x.min_length, lambda x: x.max_length))
        result = validator.validate(Person(Surname="Test", min_length=1, max_length=10))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_smaller_than_the_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(5, 10))
        result = validator.validate(Person(Surname="Test"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_smaller_than_the_lambda_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(lambda x: x.min_length, lambda x: x.max_length))
        result = validator.validate(Person(Surname="Test", min_length=5, max_length=10))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(1, 2))
        result = validator.validate(Person(Surname="Test"))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_larger_than_the_lambda_range_then_the_validator_should_fail(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(lambda x: x.min_length, lambda x: x.max_length))
        result = validator.validate(Person(Surname="Test", min_length=1, max_length=2))
        self.assertFalse(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_upper_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(1, 4))
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lambda_upper_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(lambda x: x.min_length, lambda x: x.max_length))
        result = validator.validate(Person(Surname="Test", min_length=1, max_length=4))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lower_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(4, 5))
        result = validator.validate(Person(Surname="Test"))
        self.assertTrue(result.is_valid)

    def test_When_the_text_is_exactly_the_size_of_the_lambda_lower_bound_then_the_validator_should_pass(
        self,
    ):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(lambda x: x.min_length, lambda x: x.max_length))
        result = validator.validate(Person(Surname="Test", min_length=4, max_length=5))
        self.assertTrue(result.is_valid)

    def test_When_the_max_is_smaller_than_the_min_then_the_validator_should_throw(self):
        with self.assertRaises(Exception):
            TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(10, 1))

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).length(1, 2))
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
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).exact_length(5))  # can't use length method due to the lack of overload in Python
        result = validator.validate(Person(Surname=None))
        self.assertTrue(result.is_valid)

    def test_When_the_minlength_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).min_length(4))
        result = validator.validate(Person(Surname="abc"))
        self.assertEqual(
            result.errors[0].ErrorMessage,
            "The length of 'Surname' must be at least 4 characters. You entered 3 characters.",
        )

    def test_When_the_maxlength_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).max_length(4))
        result = validator.validate(Person(Surname="abcde"))
        self.assertEqual(
            result.errors[0].ErrorMessage,
            "The length of 'Surname' must be 4 characters or fewer. You entered 5 characters.",
        )


if __name__ == "__main__":
    unittest.main()
