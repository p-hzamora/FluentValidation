from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import unittest
import sys
from pathlib import Path


sys.path.append([str(x) for x in Path(__file__).parents if x.name == "src"].pop())


from fluent_validation.syntax import IRuleBuilderOptions
from fluent_validation.InlineValidator import InlineValidator
from fluent_validation.abstract_validator import AbstractValidator
from TestValidator import TestValidator
from person import Country, IAddress, Order, Person, _Address as Address


class PersonValidator(InlineValidator[Person]):
    def __init__[TProperty](self, *ruleCreator: Callable[[InlineValidator[Person]], IRuleBuilderOptions[Person, TProperty]]) -> None:
        super().__init__(Person, *ruleCreator)
        self.rule_for(lambda x: x.Forename).not_null()
        self.rule_for(lambda x: x.Address).set_validator(AddressValidator())


class AddressValidator(AbstractValidator[Address]):
    def __init__(self):
        super().__init__(Address)
        self.rule_for(lambda x: x.Postcode).not_null()
        self.rule_for(lambda x: x.Country).set_validator(CountryValidator())


class CountryValidator(AbstractValidator[Country]):
    def __init__(self):
        super().__init__(Country)
        self.rule_for(lambda x: x.Name).not_null()


class PointlessStringValidator(AbstractValidator[str]):
    def __init__(self) -> None:
        super().__init__(str)


@dataclass(frozen=True, eq=True)
class InfiniteLoop:
    Property: InfiniteLoop2 = None


@dataclass(frozen=True, eq=True)
class InfiniteLoop2:
    Property: InfiniteLoop


class InfiniteLoopValidator(AbstractValidator[InfiniteLoop]):
    def __init__(self):
        self.rule_for(lambda x: x.Property).set_validator(InfiniteLoop2Validator())


class InfiniteLoop2Validator(AbstractValidator[InfiniteLoop2]):
    def __init__(self):
        self.rule_for(lambda x: x.Property).set_validator(InfiniteLoopValidator())


# class TracksAsyncCallValidator[T](InlineValidator[T]):

# 	bool? WasCalledAsync

# 	override ValidationResult Validate(ValidationContext[T] context) {
# 		WasCalledAsync = false
# 		return base.validate(context)
# 	}

# 	override Task[ValidationResult] ValidateAsync(ValidationContext[T] context, CancellationToken cancellation = CancellationToken()) {
# 		WasCalledAsync = true
# 		return base.ValidateAsync(context, cancellation)
# 	}
# }


@dataclass(frozen=True, eq=True)
class TestObject:
    Foo1: TestDetailObject = None
    Foo2: TestDetailObject = None


@dataclass(frozen=True, eq=True)
class TestDetailObject:
    Surname: str


class TestObjectValidator(AbstractValidator[TestObject]):
    def __init__(self):
        super().__init__(TestObject)
        self.rule_for(lambda x: x.Foo1.Surname).not_empty().when(lambda x: x.Foo1 is not None)
        self.rule_for(lambda x: x.Foo2.Surname).not_empty()


class ComplexValidationTester(unittest.TestCase):
    def setUp(self):
        self.validator: PersonValidator = PersonValidator()
        self.person: Person = Person(Address=Address(Country=Country()), Orders=[Order(Amount=5), Order(ProductName="Foo")])

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Validates_complex_property(self):
    #     results = self.validator.validate(self.person)

    #     self.assertEqual(len(results.errors), 3)
    #     self.assertEqual(results.errors[0].PropertyName, "Forename")
    #     self.assertEqual(results.errors[1].PropertyName, "Address.Postcode")
    #     self.assertEqual(results.errors[2].PropertyName, "Address.Country.Name")

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Should_override_propertyName(self):
    #     validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address).set_validator(AddressValidator()).override_property_name("Address2"))

    #     results = validator.validate(self.person)
    #     self.assertEqual(results.errors[0].PropertyName, "Address2.Postcode")

    def test_Complex_validator_should_not_be_invoked_on_null_property(self):
        results = self.validator.validate(Person())
        self.assertEqual(len(results.errors), 1)

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Should_allow_normal_rules_and_complex_property_on_same_property(self):
    #     self.validator.rule_for(lambda x: x.Address.Line1).not_null()
    #     result = self.validator.validate(self.person)
    #     self.assertEqual(len(result.errors), 4)

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Explicitly_included_properties_should_be_propagated_to_nested_validators(self):
    #     results = self.validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Address))
    #     self.assertEqual(len(results.errors), 2)
    #     self.assertEqual(results.errors[0].PropertyName, "Address.Postcode")
    #     self.assertEqual(results.errors[-1].PropertyName, "Address.Country.Name")

    # # FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
    # def test_Explicitly_included_properties_should_be_propagated_to_nested_validators_using_strings(self):
    #     results = self.validator.validate(self.person, lambda v: v.IncludeProperties("Address"))
    #     self.assertEqual(len(results.errors), 2)
    #     self.assertEqual(results.errors[0].PropertyName, "Address.Postcode")
    #     self.assertEqual(results.errors[-1].PropertyName, "Address.Country.Name")

    def test_Complex_property_should_be_excluded(self):
        results = self.validator.validate(self.person, lambda v: v.IncludeProperties(lambda x: x.Surname))
        self.assertEqual(len(results.errors), 0)

    def test_Condition_should_work_with_complex_property(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address).set_validator(AddressValidator()).when(lambda x: x.Address.Line1 == "foo"))

        result = validator.validate(self.person)
        self.assertTrue(result.is_valid)

    # [Fact]
    # async Task Condition_should_work_with_complex_property_when_invoked_async() {
    # 	validator = TestValidator() {
    # 		lambda v: v.rule_for(lambda x: x.Address).set_validator(AddressValidator()).when(lambda x: x.Address.Line1 == "foo")
    # 	}

    # 	result = await self.validator.ValidateAsync(self.person)
    # 	result.is_valid.ShouldBeTrue()
    # }

    # [Fact]
    # async Task Async_condition_should_work_with_complex_property() {
    # 	validator = TestValidator() {
    # 		lambda v: v.rule_for(lambda x: x.Address).set_validator(AddressValidator()).WhenAsync(async (x, c) => x.Address.Line1 == "foo")
    # 	}

    # 	result = await self.validator.ValidateAsync(self.person)
    # 	result.is_valid.ShouldBeTrue()
    # }

    # def test_Async_condition_throws_when_validator_invoked_synchronously(self):
    # 	validator = TestValidator() {
    # 		lambda v: v.rule_for(lambda x: x.Address).set_validator(AddressValidator()).WhenAsync(async (x, c) => x.Address.Line1 == "foo")
    # 	}

    # 	Assert.Throws<AsyncValidatorInvokedSynchronouslyException>(() => self.validator.validate(self.person))
    # }

    def test_Can_validate_using_validator_for_base_type(self):
        addressValidator = InlineValidator[IAddress](IAddress, lambda v: v.rule_for(lambda x: x.Line1).not_null())

        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address).set_validator(addressValidator))

        result = validator.validate(Person(Address=Address()))
        self.assertFalse(result.is_valid)

    def test_Can_directly_validate_multiple_fields_of_same_type(self):
        sut = TestObjectValidator()
        testObject = TestObject(Foo2=TestDetailObject(Surname="Bar"))

        # Should not throw
        sut.validate(testObject)

    # def test_Validates_child_validator_synchronously(self):
    # 	validator = TracksAsyncCallValidator<Person>()
    # 	addressValidator = TracksAsyncCallValidator<Address>()
    # 	addressValidator.rule_for(lambda x: x.Line1).not_null()
    # 	validator.rule_for(lambda x: x.Address).set_validator(addressValidator)

    # 	self.validator.validate(Person() {Address = Address()})
    # 	self.assertEqual(addressValidator.WasCalledAsync,false)

    # def test_Validates_child_validator_asynchronously(self):
    # 	validator = TracksAsyncCallValidator<Person>()
    # 	addressValidator = TracksAsyncCallValidator<Address>()
    # 	addressValidator.rule_for(lambda x: x.Line1).not_null()
    # 	validator.rule_for(lambda x: x.Address).set_validator(addressValidator)

    # 	self.validator.ValidateAsync(Person(Address = Address())).GetAwaiter().GetResult()
    # 	self.assertEqual(addressValidator.WasCalledAsync,True)


# FIXME [ ]: We need to resolve event loop to propagate the values throw the conditions properly
# def test_Multiple_rules_in_chain_with_childvalidator_shouldnt_reuse_accessor(self):
#     validator = InlineValidator[Person](Person)
#     addrValidator = InlineValidator[Address](Address)
#     addrValidator.rule_for(lambda x: x.Line1).not_null()

#     validator.rule_for(lambda x: x.Address).set_validator(addrValidator).must(lambda a: a is not None)

#     result = self.validator.validate(Person(Address=Address()))
#     self.assertEqual(len(result.errors), 1)

# [Fact]
# async Task Multiple_rules_in_chain_with_childvalidator_shouldnt_reuse_accessor_async() {
# 	validator = InlineValidator<Person>()
# 	addrValidator = InlineValidator<Address>()
# 	addrValidator.rule_for(lambda x: x.Line1).MustAsync((l, t) => Task.FromResult(l is not None))

# 	validator.rule_for(lambda x: x.Address).set_validator(addrValidator)
# 		.MustAsync((a, t) => Task.FromResult(a is not None))

# 	result = await self.validator.ValidateAsync(Person() {Address = Address()})
# 	self.assertEqual(len(result.errors), 1)
# }

# [Fact]
# void Should_not_infinite_loop() {
# 	val = InfiniteLoopValidator()
# 	target = InfiniteLoop()
# 	target.Property = InfiniteLoop2 {Property = target}
# 	val.validate(target)
# }

# private static str PointlessMethod() {
# 	return null
# }


if __name__ == "__main__":
    unittest.main()
