import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from TestValidator import TestValidator
from fluent_validation import (
    ValidatorOptions,
    Severity,
)

from person import Person


class UserSeverityTester(unittest.TestCase):
    def setUp(self):
        ValidatorOptions.Global.Severity = Severity.Error
        self.validator = TestValidator()

    def tearDown(self):
        ValidatorOptions.Global.Severity = Severity.Error

    def test_Stores_user_severity_against_validation_failure(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_severity(Severity.Info)
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].Severity, Severity.Info)

    def test_Defaults_user_severity_to_error(self):
        self.validator.rule_for(lambda x: x.Surname).not_null()
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].Severity, Severity.Error)

    def test_Defaults_user_severity_can_be_overridden_by_global_options(self):
        for severity in [Severity.Error, Severity.Info, Severity.Warning]:
            with self.subTest(severity=severity):
                ValidatorOptions.Global.Severity = severity
                self.validator.rule_for(lambda x: x.Surname).not_null()
                result = self.validator.validate(Person())
                self.assertEqual(result.errors[0].Severity, severity)

    def test_Throws_when_provider_is_null(self):
        with self.assertRaises(AttributeError):
            self.validator.rule_for(lambda x: x.Surname).not_null().with_severity(None)

    def test_Correctly_provides_object_being_validated(self):
        result_person = None

        def severity_func(x):
            nonlocal result_person
            result_person = x
            return Severity.Warning

        self.validator.rule_for(lambda x: x.Surname).not_null().with_severity(severity_func)

        person = Person()
        self.validator.validate(person)

        self.assertIs(result_person, person)

    def test_Can_Provide_severity_for_item_in_collection(self):
        self.validator.rule_for_each(lambda x: x.Children).not_null().with_severity(lambda person, child: Severity.Warning)
        result = self.validator.validate(Person(Children=[None]))
        self.assertEqual(result.errors[0].Severity, Severity.Warning)

    def test_Can_Provide_conditional_severity(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_severity(lambda x: Severity.Info if x.Age > 10 else Severity.Warning)

        person = Person()

        result = self.validator.validate(person)
        self.assertEqual(result.errors[0].Severity, Severity.Warning)

        person.Age = 100
        result = self.validator.validate(person)
        self.assertEqual(result.errors[0].Severity, Severity.Info)

    def test_Should_use_last_supplied_severity(self):
        self.validator.rule_for(lambda x: x.Surname).not_null().with_severity(lambda x: Severity.Warning).with_severity(Severity.Info)

        person = Person()

        result = self.validator.validate(person)
        self.assertEqual(result.errors[0].Severity, Severity.Info)


if __name__ == "__main__":
    unittest.main()
