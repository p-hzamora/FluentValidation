from dataclasses import dataclass
import sys
from typing import Type
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from fluent_validation.InlineValidator import InlineValidator
from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402


from fluent_validation.validators.PredicateValidator import PredicateValidator
from fluent_validation.validators.EqualValidator import EqualValidator
from fluent_validation.validators.GreaterThanOrEqualValidator import GreaterThanOrEqualValidator
from fluent_validation.validators.GreaterThanValidator import GreaterThanValidator
from fluent_validation.validators.LengthValidator import ExactLengthValidator, LengthValidator, MaximumLengthValidator, MinimumLengthValidator
from fluent_validation.validators.LessThanOrEqualValidator import LessThanOrEqualValidator
from fluent_validation.validators.LessThanValidator import LessThanValidator
from fluent_validation.validators.NotEmptyValidator import NotEmptyValidator
from fluent_validation.validators.NotEqualValidator import NotEqualValidator
from fluent_validation.validators.NotNullValidator import NotNullValidator
from fluent_validation.validators.ScalePrecisionValidator import ScalePrecisionValidator
from fluent_validation.validators.EmptyValidator import EmptyValidator


@dataclass
class Model:
    # Idk what's Guid in Python
    Ids: list


class DefaultValidatorExtensionTester(unittest.TestCase):
    def setUp(self):
        self.validator: InlineValidator[Person] = TestValidator()

    def test_NotNull_should_create_NotNullValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).not_null()
        self.AssertValidator(NotNullValidator[Person, str])

    def test_NotEmpty_should_create_NotEmptyValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).not_empty()
        self.AssertValidator(NotEmptyValidator[Person, str])

    def test_Empty_should_create_EmptyValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).empty()
        self.AssertValidator(EmptyValidator[Person, str])

    def test_Length_should_create_LengthValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).length(1, 20)
        self.AssertValidator(LengthValidator[Person])

    def test_Length_should_create_ExactLengthValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).exact_length(5)
        self.AssertValidator(ExactLengthValidator[Person])

    def test_Length_should_create_MaximumLengthValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).max_length(5)
        self.AssertValidator(MaximumLengthValidator[Person])

    def test_Length_should_create_MinimumLengthValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).min_length(5)
        self.AssertValidator(MinimumLengthValidator[Person])

    def test_NotEqual_should_create_NotEqualValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).not_equal("Foo")
        self.AssertValidator(NotEqualValidator[Person, str])

    def test_NotEqual_should_create_NotEqualValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).not_equal(lambda x: "Foo")
        self.AssertValidator(NotEqualValidator[Person, str])

    def test_Equal_should_create_EqualValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).equal("Foo")
        self.AssertValidator(EqualValidator[Person, str])

    def test_Equal_should_create_EqualValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).equal(lambda x: "Foo")
        self.AssertValidator(EqualValidator[Person, str])

    def test_Must_should_create_PredicteValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).must(lambda x: True)
        self.AssertValidator(PredicateValidator[Person, str])

    def test_Must_should_create_PredicateValidator_with_context(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).must(lambda x, val: True)
        self.AssertValidator(PredicateValidator[Person, str])

    # def test_Must_should_create_PredicateValidator_with_PropertyValidatorContext(self)->None:
    # 	hasPropertyValidatorContext = False
    # 	self.validator.rule_for(lambda x: x.Surname).must(lambda x, val, ctx: hasPropertyValidatorContext = ctx is not None
    # 		return True
    # )
    # 	self.validator.Validate(Person() {
    # 		Surname = "Surname"
    # )
    # 	self.ssertValidator([PredicateValidator[Person,str])
    # 	hasPropertyValidatorContext.ShouldBeTrue()

    # def test_MustAsync_should_create_AsyncPredicteValidator(self)->None:
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, cancel) =] True)
    # 	self.ssertValidator([AsyncPredicateValidator[Person,str])

    # def test_MustAsync_should_create_AsyncPredicateValidator_with_context(self)->None:
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async (x, val) =] True)
    # 	self.ssertValidator([AsyncPredicateValidator[Person,str])

    # def test_MustAsync_should_create_AsyncPredicateValidator_with_PropertyValidatorContext(self)->None:
    # 	hasPropertyValidatorContext = False
    # 	self.validator.rule_for(lambda x: x.Surname).MustAsync(async lambda x, val, ctx, cancel: hasPropertyValidatorContext = ctx is not None
    # 		return True
    # )
    # 	self.validator.ValidateAsync(Person {
    # 		Surname = "Surname"
    # ).Wait()
    # 	self.ssertValidator([AsyncPredicateValidator[Person,str])
    # 	hasPropertyValidatorContext.ShouldBeTrue()

    def test_LessThan_should_create_LessThanValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).less_than("foo")
        self.AssertValidator(LessThanValidator[Person, str])

    def test_LessThan_should_create_LessThanValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).less_than(lambda x: "foo")
        self.AssertValidator(LessThanValidator[Person, str])

    def test_LessThanOrEqual_should_create_LessThanOrEqualValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).less_than_or_equal_to("foo")
        self.AssertValidator(LessThanOrEqualValidator[Person, str])

    def test_LessThanOrEqual_should_create_LessThanOrEqualValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).less_than_or_equal_to(lambda x: "foo")
        self.AssertValidator(LessThanOrEqualValidator[Person, str])

    def test_LessThanOrEqual_should_create_LessThanOrEqualValidator_with_lambda_with_other_Nullable(self) -> None:
        self.validator.rule_for(lambda x: x.NullableInt).less_than_or_equal_to(lambda x: x.OtherNullableInt)
        self.AssertValidator(LessThanOrEqualValidator[Person, int])

    def test_GreaterThan_should_create_GreaterThanValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).greater_than("foo")
        self.AssertValidator(GreaterThanValidator[Person, str])

    def test_GreaterThan_should_create_GreaterThanValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).greater_than(lambda x: "foo")
        self.AssertValidator(GreaterThanValidator[Person, str])

    def test_GreaterThanOrEqual_should_create_GreaterThanOrEqualValidator_with_explicit_value(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).greater_than_or_equal_to("foo")
        self.AssertValidator(GreaterThanOrEqualValidator[Person, str])

    def test_GreaterThanOrEqual_should_create_GreaterThanOrEqualValidator_with_lambda(self) -> None:
        self.validator.rule_for(lambda x: x.Surname).greater_than_or_equal_to(lambda x: "foo")
        self.AssertValidator(GreaterThanOrEqualValidator[Person, str])

    def test_GreaterThanOrEqual_should_create_GreaterThanOrEqualValidator_with_lambda_with_other_Nullable(self) -> None:
        self.validator.rule_for(lambda x: x.NullableInt).greater_than_or_equal_to(lambda x: x.OtherNullableInt)
        self.AssertValidator(GreaterThanOrEqualValidator[Person, int])

    def test_ScalePrecision_should_create_ScalePrecisionValidator(self) -> None:
        self.validator.rule_for(lambda x: x.Discount).precision_scale(5, 2, False)
        self.AssertValidator(ScalePrecisionValidator[Person])

    def test_ScalePrecision_should_create_ScalePrecisionValidator_with_ignore_trailing_zeros(self) -> None:
        self.validator.rule_for(lambda x: x.Discount).precision_scale(5, 2, True)
        self.AssertValidator(ScalePrecisionValidator[Person])

    # def async Task MustAsync_should_not_throw_InvalidCastException(self):
    # 	model = Model {
    # 		Ids = Guid[0]

    # 	validator = AsyncModelTestValidator()
    # 	// fails with "Specified cast is not valid" error
    # 	result = await self.validator.ValidateAsync(model)
    # 	result.IsValid.ShouldBeTrue()

    def AssertValidator[TValidator](self, t_validator: Type[TValidator]):
        # cast to (IValidationRule[Person])
        rule = self.validator[0]

        if (res := rule.Components[-1]) is not None:
            self.assertEqual(res.Validator.Name, t_validator.__name__)


# class AsyncModelTestValidator : AbstractValidator[Model] {
# 	AsyncModelTestValidator() {
# 		RuleForEach(m =] m.Ids)
# 			.MustAsync((g, cancel) =] Task.FromResult(True))


if __name__ == "__main__":
    unittest.main()
