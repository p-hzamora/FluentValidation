import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from CultureScope import CultureScope
from TestValidator import TestValidator


from person import EnumGender, Person


class StringEnumValidatorTests(unittest.TestCase):
    def setUp(self):
        CultureScope.SetDefaultCulture()

        self._caseInsensitiveValidator: TestValidator = TestValidator(lambda v: v.rule_for(lambda x: x.GenderString).is_enum_name(EnumGender, False))

        self._caseSensitiveValidator: TestValidator = TestValidator(lambda v: v.rule_for(lambda x: x.GenderString).is_enum_name(EnumGender, True))

    def test_IsValidTests_CaseInsensitive_CaseCorrect(self):
        self.assertTrue(self._caseInsensitiveValidator.validate(Person(GenderString="Female")).is_valid)
        self.assertTrue(self._caseInsensitiveValidator.validate(Person(GenderString="Male")).is_valid)

    def test_IsValidTests_CaseInsensitive_CaseIncorrect(self):
        self.assertTrue(self._caseInsensitiveValidator.validate(Person(GenderString="femAlE")).is_valid)
        self.assertTrue(self._caseInsensitiveValidator.validate(Person(GenderString="maLe")).is_valid)

    def test_IsValidTests_CaseSensitive_CaseCorrect(self):
        self.assertTrue(self._caseSensitiveValidator.validate(Person(GenderString="Female")).is_valid)
        self.assertTrue(self._caseSensitiveValidator.validate(Person(GenderString="Male")).is_valid)

    def test_IsValidTests_CaseSensitive_CaseIncorrect(self):
        self.assertFalse(self._caseSensitiveValidator.validate(Person(GenderString="femAlE")).is_valid)
        self.assertFalse(self._caseSensitiveValidator.validate(Person(GenderString="maLe")).is_valid)

    def test_When_the_property_is_initialized_with_invalid_string_then_the_validator_should_fail(self):
        self.assertFalse(self._caseInsensitiveValidator.validate(Person(GenderString="other")).is_valid)

    def test_When_the_property_is_initialized_with_empty_string_then_the_validator_should_fail(self):
        self.assertFalse(self._caseInsensitiveValidator.validate(Person(GenderString="")).is_valid)

    def test_When_the_property_is_initialized_with_null_then_the_validator_should_be_valid(self):
        self.assertTrue(self._caseInsensitiveValidator.validate(Person(GenderString=None)).is_valid)

    def test_When_validation_fails_the_default_error_should_be_set(self):
        result = self._caseInsensitiveValidator.validate(Person(GenderString="invalid"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Gender String' has a range of values which does not include 'invalid'.")

    def test_When_enumType_is_null_it_should_throw(self):
        with self.assertRaises(TypeError):
            try:
                TestValidator(lambda v: v.rule_for(lambda x: x.GenderString).is_enum_name(Person))
            except TypeError as e:
                expectedMessage: str = "The type 'Person' is not an enum and can't be used with is_enum_name. (Parameter 'enumType')"
                self.assertEqual(expectedMessage, e.args[0])
                raise TypeError

    # def test_When_enumType_is_not_an_enum_it_should_throw(self):
    # 	exception = Assert.Throws<TypeError>(() =>TestValidator(lambda v: v.rule_for(lambda x: x.GenderString).is_enum_name(typeof(Person)) })
    # 	string expectedMessage = "The type 'Person' is not an enum and can't be used with is_enum_name. (Parameter 'enumType')"
    # 	exception.Message.ShouldEqual(expectedMessage)


if __name__ == "__main__":
    unittest.main()
