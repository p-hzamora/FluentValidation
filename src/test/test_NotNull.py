import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "fluent_validation"].pop())

from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class NotNullTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

    def test_NotNullValidator_should_pass_if_value_has_value(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname="Foo"))
        self.assertTrue(result.is_valid)

    def test_NotNullValidator_should_fail_if_value_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname=None))
        self.assertFalse(result.is_valid)

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())
        result = validator.validate(Person(Surname=None))
        self.assertEqual(result.errors[0].ErrorMessage, "'Surname' must not be empty.")

    def test_Not_null_validator_should_not_crash_with_non_nullable_value_type(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).not_null())
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Fails_when_nullable_value_type_is_null(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).not_null())
        result = validator.validate(Person())
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
