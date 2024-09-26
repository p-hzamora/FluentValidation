import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from fluent_validation.enums import ApplyConditionTo
from fluent_validation.abstract_validator import AbstractValidator
from TestValidator import TestValidator
from person import Order, Person


class TestConditionValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda x: x.Forename).not_null().when(lambda x: x.Id == 0)


# class TestConditionAsyncValidator(AbstractValidator[Person]):
#     def __init__(self):
#         super().__init__()
#         self.rule_for(lambda x: x.Forename).not_null().WhenAsync(self.async_lambda)

#     @staticmethod
#     async def async_lambda(x: Person):
#         return x.Id == 0


class InverseConditionValidator(AbstractValidator[Person]):
    def __init__(self):
        super().__init__(Person)
        self.rule_for(lambda x: x.Forename).not_null().unless(lambda x: x.Id == 0)


# class InverseConditionAsyncValidator(AbstractValidator[Person]):
#     def __init__(self):
#         super().__init__()
#         self.rule_for(lambda x: x.Forename).not_null().UnlessAsync(self.async_lambda)

#     @staticmethod
#     async def async_lambda(x: Person):
#         return x.Id == 0


class ConditionTests(unittest.TestCase):
    def test_Validation_should_succeed_when_condition_does_not_match(self) -> None:
        validator = TestConditionValidator()
        result = validator.validate(Person(Id=1))
        self.assertTrue(result.is_valid)

    # async def test_Validation_should_succeed_when_async_condition_does_not_match(self):
    #     validator = TestConditionAsyncValidator()
    #     result = await validator.ValidateAsync(Person(Id=1))
    #     self.assertTrue(result.is_valid)

    def test_Validation_should_fail_when_condition_matches(self) -> None:
        validator = TestConditionValidator()
        result = validator.validate(Person())
        self.assertFalse(result.is_valid)

    # async def Task Validation_should_fail_when_async_condition_matches(self):
    # 	validator = TestConditionAsyncValidator()
    # 	result = await validator.ValidateAsync(Person())
    # 	self.assertFalse(result.is_valid)

    def test_Validation_should_succeed_when_condition_matches(self) -> None:
        validator = InverseConditionValidator()
        result = validator.validate(Person())
        self.assertTrue(result.is_valid)

    # async def Task Validation_should_succeed_when_async_condition_matches(self):
    # 	validator = InverseConditionAsyncValidator()
    # 	result = await validator.ValidateAsync(Person())
    # 	self.assertTrue(result.is_valid)

    def test_Validation_should_fail_when_condition_does_not_match(self) -> None:
        validator = InverseConditionValidator()
        result = validator.validate(Person(Id=1))
        self.assertFalse(result.is_valid)

    # async def Task Validation_should_fail_when_async_condition_does_not_match(self):
    # 	validator = InverseConditionAsyncValidator()
    # 	result = await validator.ValidateAsync(Person(Id=1))
    # 	self.assertFalse(result.is_valid)

    def test_Condition_is_applied_to_all_validators_in_the_chain(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null().not_equal("foo").when(lambda x: x.Id > 0))

        result = validator.validate(Person())
        self.assertEqual(len(result.errors), 0)

    # async def Task Async_condition_is_applied_to_all_validators_in_the_chain(self):
    # 	validator = TestValidator {
    # 		lambda v: v.rule_for(lambda x: x.Surname).not_null().not_equal("foo").WhenAsync(async (x,c) => x.Id > 0)

    # 	result = await validator.ValidateAsync(Person())
    # 	result.Errors.Count.ShouldEqual(0)

    # def test_Async_condition_is_applied_to_all_validators_in_the_chain_when_executed_synchronously(self)->None:
    # 	validator = TestValidator {
    # 		lambda v: v.rule_for(lambda x: x.Surname).not_null().not_equal("foo").WhenAsync(async (x,c) => x.Id > 0)

    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() =>
    # 		validator.validate(Person()))

    # async def Task Sync_condition_is_applied_to_async_validators(self):
    # 	validator = TestValidator {
    # 		lambda v: v.rule_for(lambda x: x.Surname)
    # 			.MustAsync(async (val, token) => val is not None)
    # 			.MustAsync(async (val, token) => val != "foo")
    # 			.when(lambda x: x.Id > 0)

    # 	result = await validator.ValidateAsync(Person())
    # 	result.Errors.Count.ShouldEqual(0)

    def test_Condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator(self) -> None:
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null().not_equal("foo").when(lambda x: x.Id > 0, ApplyConditionTo.CurrentValidator))

        result = validator.validate(Person())
        self.assertEqual(len(result.errors), 1)

    # async def Task Async_condition_is_applied_to_single_validator_in_the_chain_when_ApplyConditionTo_set_to_CurrentValidator(self):
    # 	validator = TestValidator {
    # 		lambda v: v.rule_for(lambda x: x.Surname).not_null().not_equal("foo").WhenAsync(async (x,c) => x.Id > 0, ApplyConditionTo.CurrentValidator)

    # 	result = await validator.ValidateAsync(Person())
    # 	result.Errors.Count.ShouldEqual(1)

    # def test_Async_condition_throws_when_executed_synchronosuly_with_synchronous_role(self)->None:
    # 	validator = TestValidator()
    # 	validator.rule_for(lambda x: x.Surname).not_null()
    # 		.WhenAsync((x, token) => Task.FromResult(False))

    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() =>
    # 		validator.validate(Person()))

    # def test_Async_condition_throws_when_executed_synchronosuly_with_asynchronous_rule(self)->None:
    # 	validator = TestValidator()
    # 	validator.rule_for(lambda x: x.Surname)
    # 		.MustAsync((surname, c) => Task.FromResult(surname is not None))
    # 		.WhenAsync((x, token) => Task.FromResult(False))

    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() => validator.validate(Person()))

    # def test_Async_condition_throws_when_executed_synchronosuly_with_synchronous_collection_role(self)->None:
    # 	validator = TestValidator()
    # 	validator.rule_for_each(lambda x: x.NickNames).not_null()
    # 		.WhenAsync((x, token) => Task.FromResult(False))
    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() =>
    # 		validator.validate(Person {NickNames = string[0]}))

    # def test_Async_condition_throws_when_invoked_synchronosuly_with_asynchronous_collection_rule(self)->None:
    # 	validator = TestValidator()
    # 	validator.rule_for_each(lambda x: x.NickNames)
    # 		.MustAsync((n, c) => Task.FromResult(n is not None))
    # 		.WhenAsync((x, token) => Task.FromResult(False))

    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() => validator.validate(Person {NickNames = string[0]}))

    # def test_Can_access_property_value_in_custom_condition(self)->None:
    #     validator = TestValidator()
    #     validator.rule_for(lambda x: x.Surname).must(lambda v: False).Configure(lambda cfg: cfg.ApplyCondition(context => cfg.GetPropertyValue(context.InstanceToValidate) is not None))

    #     result = validator.validate(Person())
    #     self.assertTrue(result.is_valid)

    #     result = validator.validate(Person(Surname = "foo"))
    #     self.assertFalse(result.is_valid)

    # def test_Can_access_property_value_in_custom_condition_foreach(self)->None:
    #     validator = TestValidator()
    #     validator.rule_for_each(lambda x: x.Orders).must(lambda v: False).Configure(lambda cfg: cfg.ApplyCondition(context => cfg.GetPropertyValue(context.InstanceToValidate) is not None))

    #     result = validator.validate(Person())
    #     self.assertTrue(result.is_valid)

    #     result = validator.validate(Person(Orders = [Order()]))
    #     self.assertFalse(result.is_valid)


if __name__ == "__main__":
    unittest.main()
