# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion


from __future__ import annotations
from typing import Type, Optional, overload, Callable, override

from fluent_validation.IValidator import IValidator
from fluent_validation.internal.IValidatorSelector import IValidatorSelector
from fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector
from fluent_validation.validators.EmptyValidator import ValidationContext

import inspect
from .ChildValidatorAdaptor import ChildValidatorAdaptor


class DerivedValidatorFactory[T, TProperty]:
    _innerValidator: IValidator
    _factory: Callable[[ValidationContext[T, TProperty]], IValidator]
    RuleSets: list[str]

    @overload
    def __init__(self, innerValidator: IValidator, *ruleSets: str): ...
    @overload
    def __init__(self, innerValidator: Callable[[ValidationContext[T, TProperty]], IValidator], *ruleSets: str): ...

    def __init__(self, innerValidator: Optional[IValidator] | Callable[[ValidationContext[T, TProperty]], IValidator] = None, *ruleSets: str):
        if callable(innerValidator):
            self._factory = innerValidator
        else:
            self._innerValidator = innerValidator

        self.RuleSets = ruleSets

    def GetValidator(self, context: ValidationContext[T], value: TProperty) -> IValidator:
        if hasattr(self, "_factory") and self._factory is not None:
            return self._factory(context, value)
        if hasattr(self, "_innerValidator"):
            return self._innerValidator
        return None


class PolymorphicValidator[T, TProperty](ChildValidatorAdaptor[T, TProperty]):
    """
    Performs runtime checking of the value being validated, and passes validation off to a subclass validator.

    Args:
            T: Root model type
            TProperty: Base type of property being validated
    """

    _derivedValidators: dict[Type, DerivedValidatorFactory] = {}

    # Need the base constructor call, even though we're just passing None.
    def __init__(self, t_property: Type[TProperty]):
        super().__init__(None, t_property)

    def __add_with_validator[TDerived](self, validatorFactory: IValidator[TDerived], *ruleSets: str) -> PolymorphicValidator[T, TProperty]:
        """
        Adds a validator to handle a specific subclass.

        Args:
                derivedValidator: The derived validator
                ruleSets: Optionally specify rulesets to execute. If set, rules not in these rulesets will not be run

        Returns:
                PolymorphicValidator[T, TProperty]
        """
        if validatorFactory is None:
            raise ValueError("derivedValidator cannot be None")

        derivedType = validatorFactory._type_model
        self._derivedValidators[derivedType] = DerivedValidatorFactory(validatorFactory, *ruleSets)
        return self

    def __add_with_factory_single_param(self, validatorFactory: Callable[[T], IValidator], *ruleSets: str) -> PolymorphicValidator[T, TProperty]:
        """
        Adds a validator to handle a specific subclass.

        Args:
                validatorFactory: The derived validator factory function
                ruleSets: Optionally specify rulesets to execute. If set, rules not in these rulesets will not be run

        Returns:
                PolymorphicValidator[T, TProperty]
        """
        if validatorFactory is None:
            raise ValueError("validatorFactory cannot be None")

        # Note: In Python, we'd need to handle type detection differently
        # This is a simplified version - you'd need to specify the type somehow
        derivedType = None  # Would need to be passed or inferred
        self._derivedValidators[derivedType] = DerivedValidatorFactory(lambda context, _: validatorFactory(context.instance_to_validate), *ruleSets)
        return self

    def __add_with_factory_two_params[TDerived](self, validatorFactory: Callable[[T, TDerived], IValidator], *ruleSets: str) -> PolymorphicValidator[T, TProperty]:
        """
        Adds a validator to handle a specific subclass.

        Args:
                validatorFactory: The derived validator factory function
                ruleSets: Optionally specify rulesets to execute. If set, rules not in these rulesets will not be run

        Returns:
                PolymorphicValidator[T, TProperty]
        """
        if validatorFactory is None:
            raise ValueError("validatorFactory cannot be None")

        # Note: In Python, we'd need to handle type detection differently
        derivedType = None  # Would need to be passed or inferred
        self._derivedValidators[derivedType] = DerivedValidatorFactory(lambda context, value: validatorFactory(context.instance_to_validate, value), *ruleSets)
        return self

    def add[TDerived](self, validatorFactory: Callable[[T, TDerived], IValidator], *ruleSets: str) -> PolymorphicValidator[T, TProperty]:
        # when we passes a IValidator
        if len(ruleSets) == 1 and isinstance(ruleSets[0], IValidator):
            validator = ruleSets[0]
            ruleSets = ruleSets[1:]
            return self._add_with_type(validatorFactory, validator, *ruleSets)

        if not callable(validatorFactory):
            return self.__add_with_validator(validatorFactory, *ruleSets)

        n_param = len(inspect.signature(validatorFactory).parameters)
        if n_param == 1:
            return self.__add_with_factory_single_param(validatorFactory, *ruleSets)

        if n_param == 2:
            return self.__add_with_factory_two_params(validatorFactory, *ruleSets)

        raise ValueError

    def _add_with_type(self, subclassType: Type, validator: IValidator, *ruleSets: str) -> PolymorphicValidator[T, TProperty]:
        """

        Adds a validator to handle a specific subclass. This method is not publicly exposed as it
        takes a non-generic IValidator instance which could result in a type-unsafe validation operation.
        It allows derived validators more flexibility in handling type conversion. If you make use of this method, you
        should ensure that the validator can correctly handle the type being validated.

        Args:
                        subclassType: The subclass type
                        validator: The validator instance
                        ruleSets: Optionally specify rulesets to execute. If set, rules not in these rulesets will not be run

        Returns:
                        PolymorphicValidator[T, TProperty]
        """
        if subclassType is None:
            raise ValueError("subclassType cannot be None")
        if validator is None:
            raise ValueError("validator cannot be None")
        if not validator.CanValidateInstancesOfType(subclassType):
            validator_type_name = type(validator).__name__
            subclass_type_name = subclassType.__name__
            raise RuntimeError(f"Validator {validator_type_name} can't validate instances of type {subclass_type_name}")

        self._derivedValidators[subclassType] = DerivedValidatorFactory(validator, ruleSets)
        return self

    @override
    def GetValidator(self, context: ValidationContext[T], value: TProperty) -> IValidator:
        # bail out if the current item is None
        if value is None:
            return None

        if derivedValidatorFactory := (self._derivedValidators.get(type(value))):
            return derivedValidatorFactory.GetValidator(context, value)

        return None

    @override
    def GetSelector(self, context: ValidationContext[T], value: TProperty) -> IValidatorSelector:
        derivedValidatorFactory = self._derivedValidators.get(type(value), None)
        if derivedValidatorFactory and derivedValidatorFactory.RuleSets and len(derivedValidatorFactory.RuleSets) > 0:
            return RulesetValidatorSelector(derivedValidatorFactory.RuleSets)

        return None
