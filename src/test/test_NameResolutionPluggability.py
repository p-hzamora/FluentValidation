import sys
from typing import override
import unittest
from pathlib import Path

sys.path.append([str(x) for x in Path(__file__).parents if x.name == "fluent_validation"].pop())


from TestValidator import TestValidator
from person import Person, _Address as Address
from src.fluent_validation.ValidatorOptions import ValidatorOptions

from src.fluent_validation.internal.TrackingCollection import IDisposable


class NameResolutionPluggabilityTester(unittest.TestCase, IDisposable):
    def test_Uses_custom_property_name(self):
        ValidatorOptions.Global.PropertyNameResolver = lambda type, prop, expr: "foo"

        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Surname).not_null())

        error = validator.validate(Person()).errors[0]
        self.assertEqual(error.PropertyName, "foo")

    def test_Resolves_nested_properties(self):
        validator = TestValidator(lambda v: v.rule_for(lambda x: x.Address.Country).not_null())

        error = validator.validate(Person(Address=Address())).errors[0]
        self.assertEqual(error.PropertyName, "Address.Country")

    # def ShouldHaveValidationError_Should_support_custom_propertynameresolver(self):
    # 	try:
    # 		ValidatorOptions.Global.PropertyNameResolver = lambda type, prop, expr: "foo"
    # 		validator = TestValidator() {
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}
    # 		validator.TestValidate(Person()).ShouldHaveValidationErrorFor(lambda x: x.Surname)
    # 	}
    # 	finally {
    # 		ValidatorOptions.Global.PropertyNameResolver = null
    # 	}
    # }

    # def ShouldHaveValidationError_Should_support_custom_propertynameresolver_with_include_properties(self):
    # 	try:
    # 		ValidatorOptions.Global.PropertyNameResolver = lambda type, prop, expr: "foo"
    # 		validator = TestValidator() {
    # 			lambda v: v.rule_for(lambda x: x.Surname).not_null()
    # 		}
    # 		validator.TestValidate(Person(), strategy => strategy.IncludeProperties(lambda x: x.Surname)).ShouldHaveValidationErrorFor(lambda x: x.Surname)
    # 	}
    # 	finally {
    # 		ValidatorOptions.Global.PropertyNameResolver = null
    # 	}
    # }

    # def ShouldHaveValidationError_Should_support_custom_propertynameresolver_with_include_properties_and_nested_properties(self):
    # 	try:
    # 		ValidatorOptions.Global.PropertyNameResolver = lambda type, prop, expr: "foo"
    # 		validator = TestValidator() {
    # 			lambda v: v.rule_for(lambda x: x.Address.Line1).not_null()
    # 		}
    # 		validator.TestValidate(Person {
    # 			Address = Address()
    # 		}, strategy => strategy.IncludeProperties(lambda x: x.Address.Line1)).ShouldHaveValidationErrorFor(lambda x: x.Address.Line1)
    # 	}
    # 	finally {
    # 		ValidatorOptions.Global.PropertyNameResolver = null

    @override
    def Dispose(self) -> None:
        ValidatorOptions.Global.PropertyNameResolver = None

    @override
    def __enter__(self): ...
    @override
    def __exit__(self): ...


if __name__ == "__main__":
    unittest.main()
