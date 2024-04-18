import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from TestValidator import TestValidator  # noqa: E402
from person import Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class AbstractValidatorTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.testValidatorWithPreValidate:TestValidatorWithPreValidate
        CultureScope.SetDefaultCulture()
        self.validator: TestValidator = TestValidator()
        # testValidatorWithPreValidate = TestValidatorWithPreValidate()

    def test_When_the_Validators_pass_then_the_validatorRunner_should_return_true(self):
        self.validator.rule_for(lambda x: x.Forename).not_null()
        self.assertTrue(self.validator.validate(Person(Forename="Jeremy")))

    def test_When_the_validators_fail_then_validatorrunner_should_return_false(self):
        self.validator.rule_for(lambda x: x.Forename).not_null()
        self.assertFalse(self.validator.validate(Person()).is_valid)

    def test_When_the_validators_fail_then_the_errors_Should_be_accessible_via_the_errors_property(self):
        self.validator.rule_for(lambda x: x.Forename).not_null()
        result = self.validator.validate(Person())
        self.assertEqual(len(result.errors), 1)

    def test_Should_validate_public_Field(self):
        self.validator.rule_for(lambda x: x.NameField).not_null()
        result = self.validator.validate(Person())
        self.assertEqual(len(result.errors), 1)

    def test_WithMessage_should_override_error_message(self):
        self.validator.rule_for(lambda x: x.Forename).not_null().with_message("Foo")
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorMessage, "Foo")

    def test_Default_error_code_should_be_class_name(self):
        self.validator.rule_for(lambda x: x.Forename).not_null()
        result = self.validator.validate(Person())
        self.assertEqual(result.errors[0].ErrorCode, "NotNullValidator")

    # def Can_replace_default_errorcode_resolver(self):
    #     ValidatorOptions.Global.ErrorCodeResolver = lambda x: x.GetType().Name.Split('`')[0] + "_foo"
    #     self.validator.rule_for(lambda x: x.Forename).not_null()
    #     result = self.validator.validate(Person())
    #     ValidatorOptions.Global.ErrorCodeResolver = None
    #     self.assertEqual(result.errors[0].ErrorCode, "NotNullValidator_foo")

    # def WithErrorCode_should_override_error_code(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null().WithErrorCode("ErrCode101")
    #     result = self.validator.validate(Person())
    #     self.assertEqual(result.errors[0].ErrorCode, "ErrCode101")

    # def WithMessage_and_WithErrorCode_should_override_error_message_and_error_code(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null().with_message("Foo").WithErrorCode("ErrCode101")
    #     result = self.validator.validate(Person())
    #     self.assertEqual(result.errors[0].ErrorMessage, "Foo")
    #     self.assertEqual(result.errors[0].ErrorCode, "ErrCode101")

    # def WithName_should_override_field_name(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null().WithName("First Name")
    #     result = self.validator.validate(Person())
    #     self.assertEqual(result.errors[0].ErrorMessage, "'First Name' must not be empty.")

    # def WithName_should_override_field_name_with_value_from_other_property(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null().WithName(lambda x: x.Surname)
    #     result = self.validator.validate(Person(Surname="Foo"))
    #     self.assertEqual(result.errors[0].ErrorMessage, "'Foo' must not be empty.")

    # def OverridePropertyName_should_override_property_name(self):
    #     self.validator.rule_for(lambda x: x.Surname).not_null().OverridePropertyName("foo")
    #     result = self.validator.validate(Person())
    #     self.assertEqual(result.errors[0].PropertyName, "foo")

    # def OverridePropertyName_with_lambda_should_override_property_name(self):
    #     self.validator.rule_for(lambda x: x.Surname).not_null().OverridePropertyName(lambda x: x.Forename)
    #     result = self.validator.validate(Person())
    #     self.assertEqual(result.errors[0].PropertyName, "Forename")

    def Should_not_main_state(self):
        self.validator.rule_for(lambda x: x.Forename).not_null()
        self.validator.validate(Person())
        result = self.validator.validate(Person())
        self.assertEqual(len(result.errors), 1)

    def Should_throw_when_rule_is_null(self):
        with self.assertRaises(AttributeError):  # TODOL: Verify if it's the correct Error
            self.validator.rule_for(None)

    # def Should_validate_single_property(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null()
    #     self.validator.rule_for(lambda x: x.Surname).not_null()
    #     result = self.validator.validate(Person(), lambda v: v.IncludeProperties(lambda x: x.Surname))
    #     self.assertEqual(len(result.errors), 1)

    # def Should_validate_single_Field(self):
    #     self.validator.rule_for(lambda x: x.NameField).not_null()
    #     result = self.validator.validate(Person(), lambda v: v.IncludeProperties(lambda x: x.NameField))
    #     self.assertEqual(len(result.errors), 1)

    # def Should_throw_for_non_member_expression_when_validating_single_property(self):
    #     Assert.Throws<ArgumentException>((lambda ): self.validator.validate(Person(), lambda v: v.IncludeProperties(lambda x: "foo")))

    # def Should_be_valid_when_there_are_no_failures_for_single_property(self):
    #     self.validator.rule_for(lambda x: x.Surname).not_null()
    #     result = self.validator.validate(Person(Surname="foo"), lambda v: v.IncludeProperties(lambda x: x.Surname))
    #     self.assertTrue(result)

    # def Should_validate_single_property_where_property_as_string(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null()
    #     self.validator.rule_for(lambda x: x.Surname).not_null()
    #     result = self.validator.validate(Person(), lambda v: v.IncludeProperties("Surname"))
    #     self.assertEqual(len(result.errors), 1)

    # def Should_validate_single_property_where_invalid_property_as_string(self):
    #     self.validator.rule_for(lambda x: x.Forename).not_null()
    #     self.validator.rule_for(lambda x: x.Surname).not_null()
    #     result = self.validator.validate(Person(), lambda v: v.IncludeProperties("Surname1"))
    #     self.assertEqual(len(result.errors), 0)

    # def Validates_single_property_by_path(self):
    #     addressValidator = InlineValidator < Address > ()
    #     addressValidator.rule_for(lambda x: x.Line1).not_null()
    #     addressValidator.rule_for(lambda x: x.Line2).not_null()

    #     self.validator.rule_for(lambda x: x.Address).set_validator(addressValidator)
    #     self.validator.rule_for(lambda x: x.Forename).not_null()

    #     result = self.validator.validate(Person(Address=Address()), lambda v: v.IncludeProperties("Address.Line1"))
    #     self.assertEqual(len(result.errors), 1)
    #     self.assertEqual(result.errors.Single().PropertyName, "Address.Line1")

    # def CanValidateInstancesOfType_returns_true_when_comparing_against_same_type(self):
    #     self.validator = (IValidator)this.self.validator
    #     self.validator.CanValidateInstancesOfType(typeof(Person)).ShouldBeTrue()

    # def CanValidateInstancesOfType_returns_true_when_comparing_against_subclass(self):
    #     self.validator = (IValidator)this.self.validator
    #     self.validator.CanValidateInstancesOfType(typeof(DerivedPerson)).ShouldBeTrue()

    # def CanValidateInstancesOfType_returns_false_when_comparing_against_some_other_type(self):
    #     self.validator = (IValidator)this.self.validator
    #     self.validator.CanValidateInstancesOfType(typeof(Address)).ShouldBeFalse()

    # def Uses_named_parameters_to_validate_ruleset(self):
    #     self.validator.RuleSet("Names", (lambda ): {
    #         self.validator.rule_for(lambda x: x.Surname).not_null()
    #         self.validator.rule_for(lambda x: x.Forename).not_null()
    #     )
    #     self.validator.rule_for(lambda x: x.Id).not_equal(0)

    #     result = self.validator.validate(Person(), lambda v: v.IncludeRuleSets("Names"))
    #     self.assertEqual(len(result.errors),2)


#     def Validates_type_when_using_non_generic_validate_overload(self):
#         IValidator nonGenericValidator = self.validator

#         Assert.Throws<InvalidOperationException>(() =>
#             nonGenericValidator.validate(ValidationContext<string>("foo")))

#     def RuleForeach_with_null_instances(self):
#         model = Person(
#             NickNames = string[] { None }


#         self.validator.RuleForEach(lambda x: x.NickNames).not_null()
#         result = self.validator.validate(model)
#         Console.WriteLine(result.errors[0].ErrorMessage)
#         self.assertFalse(result)

#     private class DerivedPerson : Person( }


#     [MemberData(nameof(PreValidationReturnValueTheoryData))]
#     def WhenPreValidationReturnsFalse_ResultReturnToUserImmediatly_Validate(selfV: preValidationResult) {
#         testValidatorWithPreValidate.PreValidateMethod = (context, validationResultlambda ): {
#             foreach (ValidationFailure validationFailure in preValidationResult.errors) {
#                 validationResult.errors.Add(validationFailure)


#             return false

#         testValidatorWithPreValidate.rule_for(persolambda n: person.Age).greater_than_or_equal_to(0)

#         result = testValidatorWithPreValidate.validate(Person() { Age = -1 })

#         Assert.equal(preValidationResult.errors.Count, result.errors.Count)
#         Assert.DoesNotContain(nameof(Person.Age), result.errors.Select(failurlambda e: failure.PropertyName))

#     [MemberData(nameof(PreValidationReturnValueTheoryData))]
#     async Task WhenPreValidationReturnsFalse_ResultReturnToUserImmediatly_ValidateAsync(ValidationResult preValidationResult) {
#         testValidatorWithPreValidate.PreValidateMethod = (context, validationResultlambda ): {
#             foreach (ValidationFailure validationFailure in preValidationResult.errors) {
#                 validationResult.errors.Add(validationFailure)


#             return false

#         testValidatorWithPreValidate.rule_for(persolambda n: person.Age).MustAsync((age, tokenlambda ): Task.FromResult(age >= 0))

#         result = await testValidatorWithPreValidate.ValidateAsync(Person() { Age = -1 })

#         Assert.equal(preValidationResult.errors.Count, result.errors.Count)
#         Assert.DoesNotContain(nameof(Person.Age), result.errors.Select(failurlambda e: failure.PropertyName))

#     def PreValidate_bypasses_nullcheck_on_instance(self):
#         testValidatorWithPreValidate.rule_for(lambda x: x.Surname).not_null()
#         testValidatorWithPreValidate.PreValidateMethod = (ctx, rlambda ): false

#         result = testValidatorWithPreValidate.validate((Person)None)
#         self.assertTrue(result)


#     def WhenPreValidationReturnsTrue_ValidatorsGetHit_Validate(self):
#         const string testProperty = "TestProperty"
#         const string testMessage = "Test Message"
#         testValidatorWithPreValidate.PreValidateMethod = (context, validationResultlambda ): {
#             validationResult.errors.Add(ValidationFailure(testProperty, testMessage))
#             return true

#         testValidatorWithPreValidate.rule_for(persolambda n: person.Age).greater_than_or_equal_to(0)

#         result = testValidatorWithPreValidate.validate(Person() { Age = -1 })

#         Assert.Contains(nameof(Person.Age), result.errors.Select(failurlambda e: failure.PropertyName))
#         Assert.Contains(testProperty, result.errors.Select(failurlambda e: failure.PropertyName))
#         Assert.Contains(testMessage, result.errors.Select(failurlambda e: failure.ErrorMessage))

#     async Task WhenPreValidationReturnsTrue_ValidatorsGetHit_ValidateAsync() {
#         const string testProperty = "TestProperty"
#         const string testMessage = "Test Message"
#         testValidatorWithPreValidate.PreValidateMethod = (context, validationResultlambda ): {
#             validationResult.errors.Add(ValidationFailure(testProperty, testMessage))
#             return true

#         testValidatorWithPreValidate.rule_for(persolambda n: person.Age).MustAsync((age, tokenlambda ): Task.FromResult(age >= 0))

#         result = await testValidatorWithPreValidate.ValidateAsync(Person() { Age = -1 })

#         Assert.Contains(nameof(Person.Age), result.errors.Select(failurlambda e: failure.PropertyName))
#         Assert.Contains(testProperty, result.errors.Select(failurlambda e: failure.PropertyName))
#         Assert.Contains(testMessage, result.errors.Select(failurlambda e: failure.ErrorMessage))

#     def PropertyName_With_Periods_Displays_Correctly_In_Messages(self):
#         self.validator.rule_for(lambda x: x.Address.Line1).not_null().with_message("{PropertyName}")

#         validationResult = self.validator.validate(Person( Address = Address() })

#         self.assertEqual(validationResult.errors.First().ErrorMessage, "Address Line1")

#     def Message_arguments_should_be_updated_on_failure_instances(self):
#         self.validator.rule_for(lambda x: x.Surname).not_empty()
#         self.validator.rule_for(lambda x: x.Forename).not_empty()

#         // Failure instances should have different placeholders
#         result = self.validator.validate(Person())
#         self.assertEqual(result.errors[0].FormattedMessagePlaceholderValues["PropertyName"], "Surname")
#         self.assertEqual(result.errors[1].FormattedMessagePlaceholderValues["PropertyName"], "Forename")

#     static TheoryData<ValidationResult> PreValidationReturnValueTheoryData = TheoryData<ValidationResult> {
#         ValidationResult(),
#         ValidationResult(List<ValidationFailure> {ValidationFailure(nameof(Person.AnotherInt), $"{nameof(Person.AnotherInt)} Test Message")})

# }

if __name__ == "__main__":
    unittest.main()
