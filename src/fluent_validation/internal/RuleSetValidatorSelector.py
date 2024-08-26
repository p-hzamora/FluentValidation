from __future__ import annotations
from typing import Iterable, override, TYPE_CHECKING
from src.fluent_validation.IValidationRule import IValidationRule
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from src.fluent_validation.internal.IncludeRule import IIncludeRule

if TYPE_CHECKING:
    from src.fluent_validation.IValidationContext import IValidationContext


def get_or_add(dictionary: dict, key: str, factory) -> set:
    if key not in dictionary:
        dictionary[key] = factory()
    return dictionary[key]


class RulesetValidatorSelector(IValidatorSelector):
    DefaultRuleSetName: str = "default"
    WildcardRuleSetName: str = "*"

    DefaultRuleSetNameInArray: list[str] = [DefaultRuleSetName]

    @property
    def RuleSets(self) -> Iterable[str]:
        return self._rulesetsToExecute

    def __init__(self, rulesetsToExecute: Iterable[str]):
        self._rulesetsToExecute: Iterable[str] = [x.lower() for x in rulesetsToExecute]

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext):
        executed: set = get_or_add(context.RootContextData, "_FV_RuleSetsExecuted", lambda: set())

        RuleSetsLower:None|list[str] = [x.lower() for x in rule.RuleSets] if rule.RuleSets else None

        if (RuleSetsLower is None or len(RuleSetsLower) == 0) and self._rulesetsToExecute:
            if self.IsIncludeRule(rule):
                return True

        if (RuleSetsLower is None or len(RuleSetsLower) == 0) and not self._rulesetsToExecute:
            executed.add(self.DefaultRuleSetName)
            return True

        if self.DefaultRuleSetName in self._rulesetsToExecute:
            if RuleSetsLower is None or len(RuleSetsLower) == 0 or self.DefaultRuleSetName in RuleSetsLower:
                executed.add(self.DefaultRuleSetName)
                return True

        if RuleSetsLower is not None and len(RuleSetsLower) > 0 and self._rulesetsToExecute:
            intersection = set(RuleSetsLower) & set(self._rulesetsToExecute)
            if intersection:
                for r in intersection:
                    executed.add(r)
                return True

        if self.WildcardRuleSetName in self._rulesetsToExecute:
            if RuleSetsLower is None or len(RuleSetsLower) == 0:
                executed.add(self.DefaultRuleSetName)
            else:
                for r in RuleSetsLower:
                    executed.add(r)
            return True
        return False

    @staticmethod
    def IsIncludeRule(rule: IValidationRule) -> bool:
        return isinstance(rule, IIncludeRule)

    @staticmethod
    def LegacyRulesetSplit(ruleSet: str) -> list[str]:
        return [x.strip() for x in ruleSet.split(",", "")]

    # TODOH: Check

    # internal static string[] LegacyRulesetSplit(string ruleSet) {
    # 	var ruleSetNames = ruleSet.Split(',', ';')
    # 		.Select(x => x.Trim())
    # 		.ToArray();

    # 	return ruleSetNames;
    # }
