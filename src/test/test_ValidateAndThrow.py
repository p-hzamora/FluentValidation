import sys
import unittest
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())

from fluent_validation import ValidationFailure
from TestValidatorWithPreValidate import TestValidatorWithPreValidate
from fluent_validation.ValidationException import ValidationException
from fluent_validation.InlineValidator import InlineValidator
from TestValidator import TestValidator  # noqa: E402
from person import _Address as Address, Person  # noqa: E402
from CultureScope import CultureScope  # noqa: E402


class ValidateAndThrowTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CultureScope.SetDefaultCulture()

    def test_Throws_exception(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        with self.assertRaises(ValidationException):
            validator.validate_and_throw(Person())

    def test_Throws_exception_with_a_ruleset(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        ruleSetName: str = "blah"
        validator.rule_set(ruleSetName, lambda: validator.rule_for(lambda x: x.Forename).not_null())

        with self.assertRaises(ValidationException):
            validator.validate(Person(), lambda v: v.IncludeRuleSets(ruleSetName).ThrowOnFailures())

    # 	def test_Task Throws_exception_async(self)->None:
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}

    # 		await Assert.ThrowsAsync<ValidationException>(async lambda: {
    # 			await validator.ValidateAndThrowAsync(Person())
    # 		})
    # 	}

    # 	def test_Task Throws_exception_with_a_ruleset_async(self)->None:
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}

    # 		ruleSetName:str = "blah"
    # 		validator.rule_set(ruleSetName, lambda: { validator.rule_for(lambda x: x.Forename).not_null() })

    # 		await Assert.ThrowsAsync<ValidationException>(async lambda: {
    # 			await validator.ValidateAsync(Person(), lambda v: v.IncludeRuleSets(ruleSetName).ThrowOnFailures())
    # 		})
    # 	}

    def test_Does_not_throw_when_valid(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        validator.validate_and_throw(Person(Surname="foo"))

    def test_Does_not_throw_when_valid_and_a_ruleset(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        ruleSetName: str = "blah"
        validator.rule_set(ruleSetName, lambda: {validator.rule_for(lambda x: x.Forename).not_null()})

        person = Person(
            Forename="foo",
            Surname="foo",
        )
        validator.validate(person, lambda v: v.IncludeRuleSets(ruleSetName).ThrowOnFailures())

    # 	def test_Task Does_not_throw_when_valid_async(self)->None:
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}

    # 		await validator.ValidateAndThrowAsync(Person(Surname = "foo"))
    # 	}

    # 	def test_Task Does_not_throw_when_valid_and_a_ruleset_async(self)->None:
    # 		validator = TestValidator(
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}

    # 		ruleSetName:str = "blah"
    # 		validator.rule_set(ruleSetName, lambda: { validator.rule_for(lambda x: x.Forename).not_null() })

    # 		person = Person(
    # 			Forename = "foo",
    # 			Surname = "foo"
    # 		)
    # 		await validator.ValidateAsync(person, lambda v: v.IncludeRuleSets(ruleSetName).ThrowOnFailures())

    def test_Populates_errors(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        with self.assertRaises(ValidationException):
            try:
                validator.validate_and_throw(Person())
            except ValidationException as ex:
                self.assertEqual(len(ex.Errors), 1)
                raise ValidationException

    def test_ToString_provides_error_details(self) -> None:
        validator = TestValidator(
            lambda v: v.rule_for(lambda x: x.Surname).not_null(),
            lambda v: v.rule_for(lambda x: x.Forename).not_null(),
        )

        with self.assertRaises(ValidationException):
            try:
                validator.validate_and_throw(Person())
            except ValidationException as ex:
                expected: str = "Validation failed: \n -- Surname: 'Surname' must not be empty. Severity: Error\n -- Forename: 'Forename' must not be empty."
                self.assertTrue(ex.message, expected)
                raise ValidationException

    # 	def test_Serializes_exception(self)->None:
    # 		v = ValidationException(List<ValidationFailure> {ValidationFailure("test", "test")})
    # 		raw = JsonConvert.SerializeObject(v)
    # 		deserialized = JsonConvert.DeserializeObject<ValidationException>(raw)

    # 		deserialized.Errors.Count().ShouldEqual(1)
    # 	}

    # FIXME [ ]: Implement ValidationException's __init__ overload
    # def test_ValidationException_provides_correct_message_when_appendDefaultMessage_true(self) -> None:
    #     userMessage = "exception occured during testing"
    #     validationFailures: list[ValidationFailure] = [ValidationFailure("test", "test")]
    #     exception = ValidationException(errors=validationFailures)
    #     exceptionWithUserMessage = ValidationException(
    #         message=userMessage,
    #         errors=validationFailures,
    #         appendDefaultMessage=True,
    #     )

    #     self.assertEqual(exceptionWithUserMessage.message, f"{userMessage} {exception.message}")

    # 	def test_ValidationException_provides_correct_message_when_appendDefaultMessage_False(self)->None:
    # 		userMessage = "exception occured during testing"
    # 		validationFailures = List<ValidationFailure> {ValidationFailure("test", "test")}
    # 		exceptionWithUserMessage = ValidationException(userMessage, validationFailures, False)

    # 		exceptionWithUserMessage.Message.ShouldEqual(userMessage)
    # 	}

    def test_Only_root_validator_throws(self) -> None:
        validator = InlineValidator[Person](Person)
        addressValidator = InlineValidator[Address](Address)
        addressValidator.rule_for(lambda x: x.Line1).not_null()
        validator.rule_for(lambda x: x.Address).set_validator(addressValidator)
        validator.rule_for(lambda x: x.Forename).not_null()

        # Child validator shouldn't throw the exception, only the root validator should.
        # If the child validator threw the exception, then there would only be 1 failure in the validation result.
        # But if the root is throwing, then there should be 2 (as it collected its own failure and the child failure).
        with self.assertRaises(ValidationException):
            try:
                validator.validate_and_throw(Person(Address=Address()))
            except ValidationException as e:
                self.assertEqual(len(e.Errors), 2)
                raise ValidationException

    def test_Throws_exception_when_preValidate_fails_and_continueValidation_true(self) -> None:
        validator = TestValidatorWithPreValidate(
            PreValidateMethod=lambda context, result: (
                result.errors.append(ValidationFailure("test", "test")),
                True,
            )[1]
        )

        with self.assertRaises(ValidationException):
            validator.validate_and_throw(Person())

    def test_Throws_exception_when_preValidate_fails_and_continueValidation_False(self) -> None:
        validator = TestValidatorWithPreValidate(PreValidateMethod=lambda context, result: (result.errors.append(ValidationFailure("test", "test")), False)[1])

        with self.assertRaises(ValidationException):
            validator.validate_and_throw(Person())

    def test_Does_not_throws_exception_when_preValidate_ends_with_continueValidation_False(self) -> None:
        validator = TestValidatorWithPreValidate(PreValidateMethod=lambda context, result: (False))
        validator.validate_and_throw(Person())

    # def test_Task Throws_exception_when_preValidate_fails_and_continueValidation_true_async(self)->None:
    #     validator = TestValidatorWithPreValidate(
    #         PreValidateMethod = lambda context, result:(
    #             result.errors.append(ValidationFailure("test", "test"))
    #             return True
    #         )
    #     )

    #     await Assert.ThrowsAsync<ValidationException>(async lambda: {
    #         await validator.ValidateAndThrowAsync(Person())
    #     ))
    # )

    # def test_Task Throws_exception_when_preValidate_fails_and_continueValidation_False_async(self)->None:
    #     validator = TestValidatorWithPreValidate(
    #         PreValidateMethod = lambda context, result:(
    #             result.errors.append(ValidationFailure("test", "test"))
    #             return False
    #         )
    #     )

    #     await Assert.ThrowsAsync<ValidationException>(async lambda: {
    #         await validator.ValidateAndThrowAsync(Person())
    #     ))
    # )

    # def test_Task Does_not_throws_exception_when_preValidate_ends_with_continueValidation_False_async(self)->None:
    #     validator = TestValidatorWithPreValidate(
    #         PreValidateMethod = lambda context, result:(
    #     )

    #     await validator.ValidateAndThrowAsync(Person())
    # )


# 	def test_Throws_when_calling_validator_as_interface(self)->None:
# 		IValidator<TestType> validator = InterfaceValidator()
# 		test = TestType {
# 			TestInt = 0
# 		}
# 		Assert.Throws<ValidationException>(lambda: validator.validate_and_throw(test))
# 	}

# 	public class InterfaceValidator : AbstractValidator<ITestType> {
# 		public InterfaceValidator() {
# 			rule_for(t => t.TestInt).GreaterThanOrEqualTo(1)
# 		}
# 	}

# 	public class TestType : ITestType {
# 		public int TestInt { get set }
# 	}

# 	public interface ITestType {
# 		int TestInt { get set }
# 	}
# }
# `


if __name__ == "__main__":
    unittest.main()
