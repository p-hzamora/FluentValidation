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
#
#
from __future__ import annotations

from typing import Callable, Optional, overload, TYPE_CHECKING

from .IValidatorSelector import IValidatorSelector
from fluent_validation.ValidatorOptions import ValidatorOptions
from .MemberNameValidatorSelector import MemberNameValidatorSelector
from .RuleSetValidatorSelector import RulesetValidatorSelector


if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext


class ValidationStrategy[T]:
    def __init__(self):
        self._properties: Optional[list[str]] = None
        self._ruleSets: Optional[list[str]] = None
        self._throw: bool = False
        self._customSelector: Optional[MemberNameValidatorSelector] = None

    @overload
    def IncludeProperties(self, *properties: str) -> ValidationStrategy[T]:
        """
            Indicates that only the specified properties should be validated.

        Args:
               properties: The property names to validate.

        """
        ...

    @overload
    def IncludeProperties(self, *properties: Callable[[T, object]]) -> ValidationStrategy[T]:
        """
        Indicates that only the specified properties should be validated.

        Args:
            properties: The properties to validate, defined as expressions.
        """
        ...

    def IncludeProperties(self, *properties) -> ValidationStrategy[T]:
        if isinstance(properties[0], str):
            if self._properties is None:
                self._properties = list(properties)
            else:
                self._properties.extend(properties)

        else:
            if self._properties is None:
                self._properties = MemberNameValidatorSelector.MemberNamesFromExpressions(*properties)
            else:
                self._properties.extend(MemberNameValidatorSelector.MemberNamesFromExpressions(*properties))

        return self

    def IncludeRulesNotInRuleSet(self) -> ValidationStrategy[T]:
        """
        Indicates that all rules not in a rule-set should be included for validation (the equivalent of calling IncludeRuleSets("default")).
        This method can be combined with IncludeRuleSets.
        """
        if not self._ruleSets:
            self._ruleSets = []
        self._ruleSets.append(RulesetValidatorSelector.DefaultRuleSetName)
        return self

    def IncludeAllRuleSets(self) -> ValidationStrategy[T]:
        """
        Indicates that all rules should be executed, regardless of whether or not they're in a ruleset.
        This is the equivalent of IncludeRuleSets("*").
        """
        if not self._ruleSets:
            self._ruleSets = []
        self._ruleSets.append(RulesetValidatorSelector.WildcardRuleSetName)
        return self

    def IncludeRuleSets(self, *ruleSets: str) -> ValidationStrategy[T]:
        """
        Indicates that only the specified rule sets should be validated.

        Args:
            ruleSets: The names of the rulesets to validate.
        """
        if ruleSets is not None and len(ruleSets) > 0:
            if self._ruleSets is None:
                self._ruleSets = list(ruleSets)
            else:
                self._ruleSets.extend(ruleSets)
        return self

    def UseCustomSelector(self, selector: IValidatorSelector) -> ValidationStrategy[T]:
        """
        Indicates that the specified selector should be used to control which rules are executed.

        Args:
            selector: The custom selector to use
        """
        self._customSelector = selector
        return self

    def ThrowOnFailures(self) -> ValidationStrategy[T]:
        """Indicates that the validator should throw an exception if it fails, rather than return a validation result."""
        self._throw = True
        return self

    def GetSelector(self) -> IValidatorSelector:
        selector: IValidatorSelector = None

        if self._properties is not None or self._ruleSets is not None or self._customSelector is not None:
            selectors: list[IValidatorSelector] = []

            if self._customSelector is not None:
                selectors.append(self._customSelector)

            if self._properties is not None:
                selectors.append(ValidatorOptions.Global.ValidatorSelectors.MemberNameValidatorSelectorFactory(self._properties))

            if self._ruleSets is not None:
                selectors.append(ValidatorOptions.Global.ValidatorSelectors.RulesetValidatorSelectorFactory(self._ruleSets))

            selector = selectors[0] if len(selectors) == 1 else ValidatorOptions.Global.ValidatorSelectors.CompositeValidatorSelectorFactory(selectors)
        else:
            selector = ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory()

        return selector

    def BuildContext(self, instance: T) -> ValidationContext[T]:
        from fluent_validation.IValidationContext import ValidationContext

        validation = ValidationContext[T](instance, None, self.GetSelector())
        validation.ThrowOnFailures = self._throw
        return validation
