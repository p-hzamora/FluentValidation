import unittest
import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation.validators.NotNullValidator import INotNullValidator
from fluent_validation.IValidationRule import IValidationRule
from CultureScope import CultureScope
from TestValidator import TestValidator
from person import Person


class CustomMessageFormatTester(unittest.TestCase):
    def setUp(self):
        self.validator: TestValidator = TestValidator()
        CultureScope.SetDefaultCulture()

    def test_Should_format_custom_message(self):
        expected: str = "Surname"
        self.validator.rule_for(lambda x: x.Surname).not_null().with_message("{PropertyName}")
        error: str = self.validator.validate(Person()).errors[0].ErrorMessage
        self.assertEqual(error, expected)

    def test_Uses_custom_delegate_for_building_message(self):
        def _lambda(cfg: IValidationRule):
            cfg.MessageBuilder = lambda context: "Test " + str(context.InstanceToValidate.Id)

        self.validator.rule_for(lambda x: x.Surname).not_null().configure(_lambda)

        error = self.validator.validate(Person()).errors[0].ErrorMessage
        self.assertEqual(error, "Test 0")

    def test_Uses_custom_delegate_for_building_message_only_for_specific_validator(self):
        def _lambda(cfg: IValidationRule[Person, str]):
            cfg.MessageBuilder = lambda context: "Foo" if isinstance(context.PropertyValidator, INotNullValidator) else context.GetDefaultMessage()

        self.validator.rule_for(lambda x: x.Surname).not_null().not_empty().configure(_lambda)

        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "Foo")
        self.assertEqual(result.errors[1].ErrorMessage, "'Surname' must not be empty.")

    def test_Uses_property_value_in_message(self):
        self.validator.rule_for(lambda x: x.Surname).not_equal("foo").with_message(lambda person: f"was {person.Surname}")
        error = self.validator.validate(Person(Surname="foo")).errors[0].ErrorMessage
        self.assertEqual(error, "was foo")

    def test_Replaces_propertyvalue_placeholder(self):
        self.validator.rule_for(lambda x: x.Email).email_address().with_message("Was '{PropertyValue}'")
        result = self.validator.validate(Person(Email="foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "Was 'foo'")

    def test_Replaces_propertyvalue_with_empty_string_when_null(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_message("Was '{PropertyValue}'")
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "Was ''")

    def test_Includes_property_path(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_message("{PropertyPath}")
        self.validator.rule_for_each(lambda x: x.Orders).not_null().with_message("{PropertyPath}")

        result = self.validator.validate(
            Person(
                Orders=[
                    None,
                ]
            )
        )

        self.assertEqual(result.errors[0].ErrorMessage, "Surname")
        self.assertEqual(result.errors[1].ErrorMessage, "Orders[0]")


if __name__ == "__main__":
    unittest.main()
