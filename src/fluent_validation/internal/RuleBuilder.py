from typing import TypeVar

from ..IValidationRule import IValidationRule, IValidationRuleInternal
from ..validators.IpropertyValidator import IPropertyValidator
from ..syntax import IRuleBuilder, IRuleBuilderInternal


TAbstractValidator = TypeVar("TAbstractValidator")


class RuleBuilder[T, TProperty](IRuleBuilder[T, TProperty], IRuleBuilderInternal):  # IRuleBuilderOptions does not implemented due to I don't know what it does
    def __init__(self, rule: IValidationRuleInternal[T, TProperty], parent: TAbstractValidator):
        self._rule = rule
        self.parent_validator = parent

    def set_validator(self, validator: IPropertyValidator[T, TProperty]) -> IRuleBuilder[T, TProperty]:  # -> IRuleBuilderOptions[T,TProperty]
        self.Rule.AddValidator(validator)
        return self

    @property
    def Rule(self) -> IValidationRule[T, TProperty]:
        return self._rule
