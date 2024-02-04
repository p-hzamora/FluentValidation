import sys
import unittest
from pathlib import Path


sys.path.append(
    [str(x) for x in Path(__file__).parents if x.name == "FluentValidation"].pop()
)

from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402

from src.FluentValidation.DefaultValidatorExtensions import ValidatorOptions  # noqa: E402, F401


class EqualValidatorTests(unittest.TestCase):
    # def __init__(self):

    # self.CultureScope.SetDefaultCulture()

    def test_When_the_objects_are_equal_validation_should_succeed(self):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Forename).Equal("Foo")
        )
        result = validator.validate(Person(Forename="Foo"))

        self.assertTrue(result.is_valid)

    def test_When_the_objects_are_not_equal_validation_should_fail(self):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Forename).Equal("Foo")
        )
        result = validator.validate(Person(Forename="Bar"))

        self.assertFalse(result.is_valid)

    # def test_When_validation_fails_the_error_should_be_set(self):
    #     validator = TestValidator(
    #         lambda v: v.RuleFor(lambda x: x.Forename).Equal("Foo")
    #     )
    #     result = validator.validate(Person(Forename="Bar"))

    #     result.errors[0].ErrorMessage.ShouldEqual(
    #         "'Forename' must be equal to 'Foo'."
    #     )

    # def test_Should_store_property_to_compare(self):
    # 	validator =TestValidator(lambda v: v.RuleFor(lambda x: x.Forename).Equa(lambda x: x.Surname))
    # 	descriptor = validator.CreateDescriptor()
    # 	propertyValidator = descriptor.GetValidatorsForMember("Forename")
    # 		.Selec(lambda x: x.Validator)
    # 		.Cast<EqualValidator<Person,string>>().Single()

    # 	propertyValidator.MemberToCompare.ShouldEqual(typeof(Person).GetProperty("Surname"))
    # }

    # def test_Should_store_comparison_type(self):
    # 	validator =TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Equal("Foo"))
    # 	descriptor = validator.CreateDescriptor()
    # 	propertyValidator = descriptor.GetValidatorsForMember("Surname")
    # 		.Selec(lambda x: x.Validator)
    # 		.Cast<EqualValidator<Person,string>>().Single()

    # 	propertyValidator.Comparison.ShouldEqual(Comparison.Equal)

    def test_Validates_against_property(self):
        validator = TestValidator(
            lambda v: v.RuleFor(lambda x: x.Surname)
            .Equal(lambda x: x.Forename)
            .WithMessage("{ComparisonProperty}")
        )
        result = validator.validate(Person(Surname="foo", Forename="bar"))
        self.assertFalse(result.is_valid)
        # result.Errors[0].ErrorMessage.ShouldEqual("Forename")

    # def test_Comparison_property_uses_custom_resolver(self):
    # 	originalResolver = ValidatorOptions.Global.DisplayNameResolver

    # 	try:
    # 		ValidatorOptions.Global.DisplayNameResolver = (type, member,(lambda ): member.Name + "Foo"
    # 		validator =TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Equa(lambda x: x.Forename).WithMessage("{ComparisonProperty}")}
    # 		result = validator.validate(Person {Surname = "foo", Forename = "bar"})
    # 		# result.Errors[0].ErrorMessage.ShouldEqual("ForenameFoo")
    # 	finally:
    # 		ValidatorOptions.Global.DisplayNameResolver = originalResolver

    # def test_Should_succeed_on_case_insensitive_comparison(self):
    # 	validator =TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Equal("FOO", StringComparerOrdinalIgnoreCase))
    # 	result = validator.validate(Person(Surname = "foo" ))

    # 	self.assertTrue(result.is_valid)

    # def test_Should_succeed_on_case_insensitive_comparison_using_expression(self):
    # 	validator =TestValidator(lambda v: v.RuleFor(lambda x: x.Surname).Equa(lambda x: x.Forename, StringComparer.OrdinalIgnoreCase))
    # 	result = validator.validate(Person(Surname = "foo", Forename = "FOO"))

    # 	self.assertTrue(result.is_valid)

    def test_Should_use_ordinal_comparison_by_default(self):
        validator = TestValidator()
        validator.RuleFor(lambda x: x.Surname).Equal("a")
        result = validator.validate(Person(Surname="a\0"))
        self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
