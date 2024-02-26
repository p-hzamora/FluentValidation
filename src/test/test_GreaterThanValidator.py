import unittest

from person import Person
from TestValidator import TestValidator
from CultureScope import CultureScope


class GreaterThanValidatorTester(unittest.TestCase):
    VALUE: int = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).greater_than(self.VALUE))

    def test_should_fail_when_less_than_input(self) -> None:
        result = self.validator.validate(Person(Id=0))
        self.assertFalse(result.is_valid)

    def test_should_succeed_when_greater_than_input(self) -> None:
        result = self.validator.validate(Person(Id=2))
        self.assertTrue(result.is_valid)

    def test_should_fail_when_equal_to_input(self) -> None:
        result = self.validator.validate(Person(Id=self.VALUE))
        self.assertFalse(result.is_valid)

    def test_validates_with_nullable_property(self) -> None:
        self.validator = TestValidator(lambda v: v.rule_for(lambda x: x.Id).greater_than(lambda x: x.NullableInt))

        resultNull = self.validator.validate(Person(Id=0, NullableInt=None))
        resultLess = self.validator.validate(Person(Id=0, NullableInt=-1))
        resultEqual = self.validator.validate(Person(Id=0, NullableInt=0))
        resultMore = self.validator.validate(Person(Id=0, NullableInt=1))

        self.assertFalse(resultNull.is_valid)
        self.assertTrue(resultLess.is_valid)
        self.assertFalse(resultEqual.is_valid)
        self.assertFalse(resultMore.is_valid)

    def test_Validates_nullable_with_nullable_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).greater_than(lambda x: x.OtherNullableInt))

        resultNull = validator.validate(Person(NullableInt=0, OtherNullableInt=None))
        resultLess = validator.validate(Person(NullableInt=0, OtherNullableInt=-1))
        resultEqual = validator.validate(Person(NullableInt=0, OtherNullableInt=0))
        resultMore = validator.validate(Person(NullableInt=0, OtherNullableInt=1))

        self.assertFalse(resultNull.is_valid)
        self.assertTrue(resultLess.is_valid)
        self.assertFalse(resultEqual.is_valid)
        self.assertFalse(resultMore.is_valid)

    # def test_Comparison_Type(self)-> None:
    # 	propertyValidator = validator.CreateDescriptor()
    # 		.GetValidatorsForMember("Id")
    # 		.Select(x => x.Validator)
    # 		.OfType<GreaterThanValidator<Person,int>>().Single()

    # 	propertyValidator.Comparison.ShouldEqual(Comparison.greater_than)

    def test_Validates_with_nullable_when_property_is_null(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).greater_than(5))
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).greater_than(5))
        result = validator.validate(Person(NullableInt=1))
        self.assertFalse(result.is_valid)

    def test_Validates_with_nullable_when_property_is_null_cross_property(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).greater_than(lambda x: x.Id))
        result = validator.validate(Person(Id=5))
        self.assertTrue(result.is_valid)

    def test_Validates_with_nullable_when_property_not_null_cross_property(
        self,
    ) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.NullableInt).greater_than(lambda x: x.Id))
        result = validator.validate(Person(NullableInt=1, Id=5))
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
