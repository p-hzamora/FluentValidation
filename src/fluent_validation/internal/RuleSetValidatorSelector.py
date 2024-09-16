from __future__ import annotations
from typing import Callable, Iterable, override, TYPE_CHECKING
from fluent_validation.IValidationRule import IValidationRule
from fluent_validation.internal.IValidatorSelector import IValidatorSelector

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext


def get_or_add[T](dictionary: dict, key: str, factory: Callable[..., T]) -> set:
    if key not in dictionary:
        dictionary[key] = factory()
    return dictionary[key]


# TODOL: Check how to implement 'case insensitive'. Currently it's case sensitive
class RulesetValidatorSelector(IValidatorSelector):
    DefaultRuleSetName: str = "default"
    WildcardRuleSetName: str = "*"

    DefaultRuleSetNameInArray: list[str] = [DefaultRuleSetName]

    @property
    def RuleSets(self) -> Iterable[str]:
        return self._rulesetsToExecute

    def __init__(self, rulesetsToExecute: Iterable[str]):
        self._rulesetsToExecute: Iterable[str] = rulesetsToExecute

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext):
        executed: set[str] = get_or_add(context.RootContextData, "_FV_RuleSetsExecuted", lambda: set())

        if (rule.RuleSets is None or len(rule.RuleSets) == 0) and self._rulesetsToExecute:
            if self.IsIncludeRule(rule):
                return True

        if (rule.RuleSets is None or len(rule.RuleSets) == 0) and not self._rulesetsToExecute:
            executed.add(self.DefaultRuleSetName)
            return True

        if self.DefaultRuleSetName in self._rulesetsToExecute:
            if rule.RuleSets is None or len(rule.RuleSets) == 0 or self.DefaultRuleSetName in rule.RuleSets:
                executed.add(self.DefaultRuleSetName)
                return True

        if rule.RuleSets is not None and len(rule.RuleSets) > 0 and self._rulesetsToExecute:
            intersection = set(rule.RuleSets) & set(self._rulesetsToExecute)
            if intersection:
                for r in intersection:
                    executed.add(r)
                return True

        if self.WildcardRuleSetName in self._rulesetsToExecute:
            if rule.RuleSets is None or len(rule.RuleSets) == 0:
                executed.add(self.DefaultRuleSetName)
            else:
                for r in rule.RuleSets:
                    executed.add(r)
            return True
        return False

    @staticmethod
    def IsIncludeRule(rule: IValidationRule) -> bool:
        from fluent_validation.internal.IncludeRule import IIncludeRule

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
