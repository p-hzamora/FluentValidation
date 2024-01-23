import sys
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name =="stc_project"].pop())

import  unittest
from stc.common.test.test_FluentValidation.TestValidator import TestValidator
from stc.common.test.test_FluentValidation.person import Person


class LessThanValidatorTester
	int value = 1

	def __init__(self):
		CultureScope.SetDefaultCulture()
	}

	[Fact]
	public void Should_fail_when_greater_than_input() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(value))
		var result = validator.Validate(new Person{Id=2})
		result.IsValid.ShouldBeFalse()
	}

	[Fact]
	public void Should_succeed_when_less_than_input() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(value))

		var result = validator.Validate(new Person{Id=0})
		result.IsValid.ShouldBeTrue()
	}

	[Fact]
	public void Should_fail_when_equal_to_input() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(value))
		var result = validator.Validate(new Person{Id=value})
		result.IsValid.ShouldBeFalse()
	}

	[Fact]
	public void Should_set_default_validation_message_when_validation_fails() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(value))
		var result = validator.Validate(new Person{Id=2})
		result.Errors.Single().ErrorMessage.ShouldEqual("'Id' must be less than '1'.")
	}

	[Fact]
	public void Validates_against_property() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(x => x.AnotherInt).WithMessage("{ComparisonProperty}"))
		var result = validator.Validate(new Person { Id = 2, AnotherInt = 1 })
		result.IsValid.ShouldBeFalse()
		result.Errors[0].ErrorMessage.ShouldEqual("Another Int")
	}

	[Fact]
	public void Comparison_property_uses_custom_resolver() {
		var originalResolver = ValidatorOptions.Global.DisplayNameResolver

		try {
			ValidatorOptions.Global.DisplayNameResolver = (type, member, expr) => member.Name + "Foo"
			var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(x => x.AnotherInt).WithMessage("{ComparisonProperty}"))
			var result = validator.Validate(new Person { Id = 2, AnotherInt = 1 })
			result.Errors[0].ErrorMessage.ShouldEqual("AnotherIntFoo")
		}
		finally {
			ValidatorOptions.Global.DisplayNameResolver = originalResolver
		}
	}

	[Fact]
	public void Should_throw_when_value_to_compare_is_null() {
		Expression<Func<Person, int>> nullExpression = null
		Assert.Throws<ArgumentNullException>(() =>
			new TestValidator(v => v.RuleFor(x => x.Id).LessThan(nullExpression))
		)
	}

	[Fact]
	public void Extracts_property_from_expression() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(x => x.AnotherInt))
		var propertyValidator = validator.CreateDescriptor().GetValidatorsForMember("Id")
			.Select(x => x.Validator)
			.OfType<LessThanValidator<Person, int>>().Single()
		propertyValidator.MemberToCompare.ShouldEqual(typeof(Person).GetProperty("AnotherInt"))
	}

	[Fact]
	public void Validates_with_nullable_property() {
		var validator = new TestValidator(v => v.RuleFor(x => x.Id).LessThan(x => x.NullableInt))

		var resultNull = validator.Validate(new Person { Id = 0, NullableInt = null })
		var resultLess = validator.Validate(new Person { Id = 0, NullableInt = -1 })
		var resultEqual = validator.Validate(new Person { Id = 0, NullableInt = 0 })
		var resultMore = validator.Validate(new Person { Id = 0, NullableInt = 1 })

		resultNull.IsValid.ShouldBeFalse()
		resultLess.IsValid.ShouldBeFalse()
		resultEqual.IsValid.ShouldBeFalse()
		resultMore.IsValid.ShouldBeTrue()
	}

	[Fact]
	public void Validates_nullable_with_nullable_property() {
		var validator = new TestValidator(v => v.RuleFor(x => x.NullableInt).LessThan(x => x.OtherNullableInt))

		var resultNull = validator.Validate(new Person { NullableInt = 0, OtherNullableInt = null })
		var resultLess = validator.Validate(new Person { NullableInt = 0, OtherNullableInt = -1 })
		var resultEqual = validator.Validate(new Person { NullableInt = 0, OtherNullableInt = 0 })
		var resultMore = validator.Validate(new Person { NullableInt = 0, OtherNullableInt = 1 })

		resultNull.IsValid.ShouldBeFalse()
		resultLess.IsValid.ShouldBeFalse()
		resultEqual.IsValid.ShouldBeFalse()
		resultMore.IsValid.ShouldBeTrue()
	}

	[Fact]
	public void Extracts_property_from_constant_using_expression() {
		IComparisonValidator validator = new LessThanValidator<Person,int>(2)
		validator.ValueToCompare.ShouldEqual(2)
	}

	[Fact]
	public void Comparison_type() {
		var validator = new LessThanValidator<Person,int>(1)
		validator.Comparison.ShouldEqual(Comparison.LessThan)
	}

	[Fact]
	public void Validates_with_nullable_when_property_is_null() {
		var validator = new TestValidator(v => v.RuleFor(x => x.NullableInt).LessThan(5))
		var result = validator.Validate(new Person())
		result.IsValid.ShouldBeTrue()
	}

	[Fact]
	public void Validates_with_nullable_when_property_not_null() {
		var validator = new TestValidator(v => v.RuleFor(x => x.NullableInt).LessThan(5))
		var result = validator.Validate(new Person { NullableInt = 10 })
		result.IsValid.ShouldBeFalse()
	}

	[Fact]
	public void Validates_with_nullable_when_property_null_cross_property() {
		var validator = new TestValidator(v => v.RuleFor(x => x.NullableInt).LessThan(x => x.Id))
		var result = validator.Validate(new Person {Id = 5})
		result.IsValid.ShouldBeTrue()
	}

	[Fact]
	public void Validates_with_nullable_when_property_not_null_cross_property() {
		var validator = new TestValidator(v => v.RuleFor(x => x.NullableInt).LessThan(x => x.Id))
		var result = validator.Validate(new Person {NullableInt = 10, Id = 5})
		result.IsValid.ShouldBeFalse()
	}
}
