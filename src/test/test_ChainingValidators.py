import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from TestValidator import TestValidator
from person import Person


class ChainingValidatorsTester(unittest.TestCase):
    def setUp(self):
        self.validator: TestValidator = TestValidator()

    def test_Should_create_multiple_validators(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().not_equal("foo")

        self.assertEqual(len(self.validator[0].Components), 2)

    def test_Should_execute_multiple_validators(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().equal("Foo")

        self.assertEqual(len(self.validator.validate(Person()).errors), 2)

    def test_Options_should_only_apply_to_current_validator(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_message("null").equal("foo").with_message("equal")

        results = self.validator.validate(Person())
        self.assertEqual(results.errors[0].ErrorMessage, "null")
        self.assertEqual(results.errors[1].ErrorMessage, "equal")


if __name__ == "__main__":
    unittest.main()
