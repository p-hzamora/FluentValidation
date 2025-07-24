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
from typing import Callable, Iterable, override, TYPE_CHECKING
from fluent_validation.IValidationRule import IValidationRule
from fluent_validation.internal.IValidatorSelector import IValidatorSelector
from fluent_validation.enums import StringComparer

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

        if any([StringComparer.OrdinalIgnoreCase(self.DefaultRuleSetName, x) for x in self._rulesetsToExecute]):
            if rule.RuleSets is None or len(rule.RuleSets) == 0 or any([StringComparer.OrdinalIgnoreCase(self.DefaultRuleSetName, x) for x in rule.RuleSets]):
                executed.add(self.DefaultRuleSetName)
                return True

        if rule.RuleSets is not None and len(rule.RuleSets) > 0 and self._rulesetsToExecute:
            # FIXME [x]: try to get the intersection with
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
