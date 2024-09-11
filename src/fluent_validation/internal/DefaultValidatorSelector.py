from __future__ import annotations
from typing import override, TYPE_CHECKING

from fluent_validation.internal.IValidatorSelector import IValidatorSelector
from fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext
    from fluent_validation.IValidationRule import IValidationRule


class DefaultValidatorSelector(IValidatorSelector):
    @override
    @staticmethod
    def CanExecute(rule: IValidationRule, propertyPath: str, context: IValidationContext):
        # By default we ignore any rules part of a RuleSet.
        if rule.RuleSets is not None and len(rule.RuleSets) > 0 and RulesetValidatorSelector.DefaultRuleSetName not in tuple(map(str.lower, rule.RuleSets)):
            return False
        return True
