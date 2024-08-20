from typing import override

from src.fluent_validation.IValidationContext import IValidationContext
from src.fluent_validation.IValidationRule import IValidationRule
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from src.fluent_validation.internal.RuleSetValidatorSelector import RulesetValidatorSelector

class DefaultValidatorSelector(IValidatorSelector):
    @override
    def CanExecute(rule:IValidationRule, propertyPath:str,context:IValidationContext):
        #By default we ignore any rules part of a RuleSet.
        if rule.RuleSets is not None & len(rule.RuleSets) > 0 and RulesetValidatorSelector.DefaultRuleSetName.lower() not in rule.RuleSets:
            return False
        return True
    