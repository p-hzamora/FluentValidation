import inspect
from typing import Callable, TypeVar

from src.fluent_validation.IValidator import IValidator

from ..IValidationRule import IValidationRule, IValidationRuleInternal
from ..validators.IpropertyValidator import IPropertyValidator
from ..syntax import IRuleBuilder, IRuleBuilderInternal, IRuleBuilderOptions


TAbstractValidator = TypeVar("TAbstractValidator")


class RuleBuilder[T, TProperty](IRuleBuilder[T, TProperty], IRuleBuilderInternal):  # IRuleBuilderOptions does not implemented due to I don't know what it does
    def __init__(self, rule: IValidationRuleInternal[T, TProperty], parent: TAbstractValidator):
        self._rule = rule
        self.parent_validator = parent

    @property
    def Rule(self) -> IValidationRule[T, TProperty]:
        return self._rule

    def set_validator(self, validator, *ruleSets) -> IRuleBuilderOptions[T, TProperty]:
        if isinstance(validator, IPropertyValidator):
            return self.set_validator_IPropertyValidator(validator)

        elif isinstance(validator, IValidator):
            return self.set_validator_IValidator(validator, ruleSets)

        elif callable(validator) and len(inspect.signature(validator).parameters) == 1:
            return self.set_validator_Callable_T(validator, ruleSets)

        elif callable(validator) and len(inspect.signature(validator).parameters) == 2:
            return self.set_validator_Callable_T_TProperty(validator, ruleSets)

        else:
            raise AttributeError(validator)

    def set_validator_IPropertyValidator(self, validator: IPropertyValidator[T, TProperty]) -> IRuleBuilderOptions[T, TProperty]:
        self.Rule.AddValidator(validator)
        return self

    def set_validator_IValidator(self, validator: IValidator[TProperty], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]:
        # TODOH []: Create ChildValidatorAdaptor class ASAP
        ...
        # adaptor = ChildValidatorAdaptor[T,TProperty](validator,type(validator))
        # adaptor.RuleSets = ruleSets

        # self.Rule.AddAsyncValidator(adaptor,adaptor)

    def set_validator_Callable_T[TValidator: IValidator[TProperty]](self, validator: Callable[[T], TValidator], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: 
        #TODOH []: We need to implement this method to use set_validator properly
        ...

    def set_validator_Callable_T_TProperty[TValidator: IValidator[TProperty]](self, validator: Callable[[T, TProperty], TValidator], *ruleSets: str) -> IRuleBuilderOptions[T, TProperty]: 
        #TODOH []: We need to implement this method to use set_validator properly
        ...
