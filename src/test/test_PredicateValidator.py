import unittest
from TestValidator import TestValidator
from person import Person


class PredicateValidatorTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # CultureScope.SetDefaultCulture()
        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).must(lambda forename: forename == "Jeremy"))

    def test_Should_fail_when_predicate_returns_false(self):
        result = self.validator.validate(Person(Forename="Foo"))
        self.assertFalse(result.is_valid)

    def test_Should_succeed_when_predicate_returns_true(self):
        result = self.validator.validate(Person(Forename="Jeremy"))
        self.assertTrue(result.is_valid)

    def test_Should_throw_when_predicate_is_null(self):
        with self.assertRaises(TypeError):
            TestValidator(lambda v: v.rule_for(lambda x: x.Surname).must(None))

    def test_When_validation_fails_the_default_error_should_be_set(self):
        result = self.validator.validate(Person(Forename="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "The specified condition was not met for 'Forename'.")

    def test_When_validation_fails_metadata_should_be_set_on_failure(self):
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Forename).must(lambda forename: forename == "Jeremy")
            # .with_message(lambda x: TestMessages.ValueOfForPropertyNameIsNotValid)
        )

        result = validator.validate(Person(Forename="test"))
        error = result.errors[0]

        self.assertIsNotNone(error)
        self.assertEqual(error.PropertyName, "Forename")
        self.assertEqual(error.AttemptedValue, "test")
        self.assertEqual(error.ErrorCode, "PredicateValidator")

        self.assertEqual(len(error.FormattedMessagePlaceholderValues), 3)
        self.assertTrue("PropertyName" in error.FormattedMessagePlaceholderValues)
        self.assertTrue("PropertyValue" in error.FormattedMessagePlaceholderValues)
        self.assertTrue("PropertyPath" in error.FormattedMessagePlaceholderValues)

        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyName"], "Forename")
        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyValue"], "test")
        self.assertEqual(error.FormattedMessagePlaceholderValues["PropertyPath"], "Forename")
