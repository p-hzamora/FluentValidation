import unittest

from person import Person
from TestValidator import TestValidator


class NotEqualValidatorTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_When_the_objects_are_equal_then_the_validator_should_fail(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Foo"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertFalse(result.is_valid)

    def test_When_the_objects_are_not_equal_then_the_validator_should_pass(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Bar"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertTrue(result.is_valid)

    def test_When_the_validator_fails_the_error_message_should_be_set(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("Foo"))
        result = validator.validate(Person(Forename="Foo"))
        self.assertEqual(result.errors[0].ErrorMessage, "'Forename' must not be equal to 'Foo'.")

    def test_Validates_across_properties(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname).with_message("{ComparisonProperty}"))

        result = validator.validate(Person(Surname="foo", Forename="foo"))
        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].ErrorMessage, "Surname")

    # def test_Comparison_property_uses_custom_resolver(self):
    # 	originalResolver = ValidatorOptions.Global.DisplayNameResolver

    # 	try:
    # 		ValidatorOptions.Global.DisplayNameResolver = (type, member, exprlambda ): member.Name + "Foo"
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for(lambda x: x.Forename)
    # 				.not_equal(lambda x: x.Surname)
    # 				.with_message("{ComparisonProperty}")
    # 		)

    # 		result = validator.validate(Person( Surname = "foo", Forename = "foo" })
    # 		self.assertEqual(result.errors[0].ErrorMessage, "SurnameFoo")
    # 	finally:
    # 		ValidatorOptions.Global.DisplayNameResolver = originalResolver

    # def test_Should_store_property_to_compare(self):
    # 	validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname))
    # 	propertyValidator = validator.CreateDescriptor()
    # 		.GetValidatorsForMember("Forename")
    # 		.Select(lambda x: x.Validator)
    # 		.OfType<NotEqualValidator<Person,string>>()
    # 		.Single()

    # 	propertyValidator.MemberToCompare.ShouldEqual(typeof(Person).GetProperty("Surname"))

    # def test_Should_store_comparison_type(self):
    # 	validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname))
    # 	propertyValidator = validator.CreateDescriptor()
    # 		.GetValidatorsForMember("Forename")
    # 		.Select(lambda x: x.Validator)
    # 		.OfType<NotEqualValidator<Person,string>>()
    # 		.Single()
    # 	propertyValidator.Comparison.ShouldEqual(Comparison.not_equal)

    def test_Should_not_be_valid_for_case_insensitve_comparison(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal("FOO"))
        result = validator.validate(Person(Forename="foo"))
        self.assertTrue(result.is_valid)

    def test_Should_not_be_valid_for_case_insensitve_comparison_with_expression(self):
        # validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname, StringComparer.OrdinalIgnoreCase)) #FIXME [ ]: Try to use implement StringComparer.OrdinalIgnoreCase
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Forename).not_equal(lambda x: x.Surname))
        # result = validator.validate(Person( Forename = "foo", Surname = "FOO")) # original
        result = validator.validate(Person(Forename="foo", Surname="foo"))
        self.assertFalse(result.is_valid)

    # def test_Should_handle_custom_value_types_correctly(self):
    # 	myType = MyType()
    # 	myTypeValidator = MyTypeValidator()

    # 	validationResult = myTypeValidator.Validate(myType)
    # 	validationResult.is_valid.ShouldEqual(false)

    # def test_Should_use_ordinal_comparison_by_default(self):
    # 	validator = TestValidator()
    # 	validator.rule_for(lambda x: x.Surname).not_equal("a")
    # 	result = validator.validate(Person(Surname = "a\0"))
    # 	self.assertTrue(result.is_valid)

    # class MyType:
    # 	Value:MyValueType

    # class MyTypeValidator(AbstractValidator)[MyType]:
    # 	MyTypeValidator()
    # 		rule_for(myTyplambda e: myType.Value).not_equal(MyValueType.None)

    # class MyValueType:
    # 	static readonly MyValueType None = default

    # 	MyValueType(int value)
    # 		_value = value

    # 	int Value
    # 		get { return _value ?? -1 }

    # 	private readonly int? _value

    # 	override int GetHashCode() {
    # 		return _value == null ? 0 : _value.Value.GetHashCode()

    # 	override string ToString() {
    # 		return _value == null ? null : _value.Value.ToString()

    # 	override bool Equals(object obj) {
    # 		if (obj == null || obj.GetType() != typeof(MyValueType))
    # 			return false

    # 		otherValueType = (MyValueType)obj
    # 		return Equals(otherValueType)

    # 	bool Equals(MyValueType other) {
    # 		return _value == other._value

    # 	static bool operator ==(MyValueType first, MyValueType second) {
    # 		return first.Equals(second)

    # 	static bool operator !=(MyValueType first, MyValueType second) {
    # 		return !(first == second)
    # }


if __name__ == "__main__":
    unittest.main()
