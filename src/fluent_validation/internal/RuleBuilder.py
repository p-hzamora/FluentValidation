# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
import inspect
from typing import Any, Callable, TYPE_CHECKING, overload

from fluent_validation.IValidator import IValidator
from fluent_validation.validators.ChildValidatorAdaptor import ChildValidatorAdaptor

from fluent_validation.validators.IpropertyValidator import IPropertyValidator
from fluent_validation.syntax import IRuleBuilderInternal, IRuleBuilderOptions, IRuleBuilderInitial, IRuleBuilderInitialCollection, IRuleBuilderOptionsConditions

if TYPE_CHECKING:
    from fluent_validation.internal.RuleComponent import RuleComponent
    from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from fluent_validation.abstract_validator import AbstractValidator


class RuleBuilder[T, TProperty](
    IRuleBuilderOptions[T, TProperty],
    IRuleBuilderInitial[T, TProperty],
    IRuleBuilderInitialCollection[T, TProperty],
    IRuleBuilderOptionsConditions[T, TProperty],
    IRuleBuilderInternal[T, TProperty],
):
    def __init__(self, rule: IValidationRuleInternal[T, TProperty], parent: AbstractValidator[T]):
        self._rule: IValidationRuleInternal[T, TProperty] = rule
        self.parent_validator: AbstractValidator[T] = parent

    @property
    def Rule(self) -> IValidationRuleInternal[T, TProperty]:
        return self._rule

    @property
    def ParentValidator(self) -> AbstractValidator[T]:
        return self.parent_validator

    def set_validator(self, validator, *ruleSets) -> IRuleBuilderOptions[T, TProperty]:
        if isinstance(validator, IPropertyValidator):
            return self.set_validator_IPropertyValidator(validator)

        elif isinstance(validator, IValidator):
            return self.set_validator_IValidator(validator, *ruleSets)

        elif callable(validator) and len(inspect.signature(validator).parameters) == 1:
            return self.set_validator_Callable_T(validator, *ruleSets)

        elif callable(validator) and len(inspect.signature(validator).parameters) == 2:
            return self.set_validator_Callable_T_TProperty(validator, *ruleSets)

        else:
            raise AttributeError(validator)

    @overload
    def dependent_rules(self: IRuleBuilderOptions, action: Callable[..., Any]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def dependent_rules(self: IRuleBuilderOptionsConditions, action: Callable[..., Any]) -> IRuleBuilderOptionsConditions[T, TProperty]: ...

    def dependent_rules(self, action: Callable[..., Any]) -> IRuleBuilderOptionsConditions[T, TProperty]:
        self._DependentRulesInternal(action)
        return self

    def _DependentRulesInternal(self, action: Callable[..., None]) -> None:
        dependencyContainer: list[IValidationRuleInternal[T]] = []

        # Capture any rules added to the parent validator inside this delegate.
        with self.ParentValidator.Rules.Capture(dependencyContainer.append):
            action()

        if self.Rule.RuleSets is not None and len(self.Rule.RuleSets) > 0:
            for dependentRule in dependencyContainer:
                if dependentRule.RuleSets is None:
                    dependentRule.RuleSets = self.Rule.RuleSets

        self.Rule.AddDependentRules(dependencyContainer)
        return self

    def set_validator_IPropertyValidator(self, validator: IPropertyValidator[T, TProperty]) -> IRuleBuilderOptions[T, TProperty]:
        self.Rule.AddValidator(validator)
        return self

    def set_validator_IValidator(self, validator: IValidator[TProperty], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]:
        # TODOH [x]: Create ChildValidatorAdaptor class ASAP
        adaptor = ChildValidatorAdaptor[T, TProperty](validator, type(validator))
        adaptor.RuleSets = ruleSets

        self.Rule.AddAsyncValidator(adaptor, adaptor)
        return self

    def set_validator_Callable_T[TValidator: IValidator[TProperty]](self, validator: Callable[[T], TValidator], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]:
        # TODOH [x]: We need to implement this method to use set_validator properly
        adaptor = ChildValidatorAdaptor[T, TProperty](lambda context, _: validator(context.instance_to_validate), type(TValidator))
        adaptor.RuleSets = ruleSets
        # ChildValidatorAdaptor supports both sync and async execution.
        self.Rule.AddAsyncValidator(adaptor, adaptor)
        return self

    def set_validator_Callable_T_TProperty[TValidator: IValidator[TProperty]](self, validator: Callable[[T, TProperty], TValidator], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]:
        # TODOH [x]: We need to implement this method to use set_validator properly
        adaptor = ChildValidatorAdaptor[T, TProperty](lambda context, val: validator(context.instance_to_validate, val), type(TValidator))
        adaptor.RuleSets = ruleSets
        # ChildValidatorAdaptor supports both sync and async execution.
        self.Rule.AddAsyncValidator(adaptor, adaptor)
        return self

    def AddComponent(self, component: RuleComponent[T, TProperty]) -> None:
        self.Rule.Components.append(component)
        return None
