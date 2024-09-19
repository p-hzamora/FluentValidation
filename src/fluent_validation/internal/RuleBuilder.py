from __future__ import annotations
import inspect
from typing import Callable, TYPE_CHECKING

from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
from fluent_validation.IValidator import IValidator
from fluent_validation.validators.ChildValidatorAdaptor import ChildValidatorAdaptor

from fluent_validation.IValidationRule import IValidationRule
from fluent_validation.validators.IpropertyValidator import IPropertyValidator
from fluent_validation.syntax import IRuleBuilder, IRuleBuilderInternal, IRuleBuilderOptions

if TYPE_CHECKING:
    from fluent_validation.abstract_validator import AbstractValidator


class RuleBuilder[T, TProperty](IRuleBuilder[T, TProperty], IRuleBuilderInternal):  # IRuleBuilderOptions does not implemented due to I don't know what it does
    def __init__(self, rule: IValidationRuleInternal[T, TProperty], parent: AbstractValidator[T]):
        self._rule: IValidationRuleInternal[T, TProperty] = rule
        self.parent_validator: AbstractValidator[T] = parent

    @property
    def Rule(self) -> IValidationRule[T, TProperty]:
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
