from __future__ import annotations

from typing import Callable, Optional, overload, TYPE_CHECKING

from src.fluent_validation.IValidationContext import ValidationContext
from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector
from src.fluent_validation.internal.MemberNameValidatorSelector import MemberNameValidatorSelector

if TYPE_CHECKING:
    from ..IValidationContext import ValidationContext


class ValidationStrategy[T]:
    def __init__(self):
        self._properties: Optional[list[str]] = None
        self._ruleSets: Optional[list[str]] = None
        self._throw: bool = False
        self._customSelector: Optional[MemberNameValidatorSelector] = None

    @overload
    def IncludeProperties(self, *properties: str) -> "ValidationStrategy[T]": ...
    @overload
    def IncludeProperties(self, *properties: Callable[[T, object]]) -> "ValidationStrategy[T]": ...

    def IncludeProperties(self, *properties) -> "ValidationStrategy[T]":
        if self._properties is None:
            self._properties = list(properties)

        # if self._properties is None:
        #     self._properties = list(MemberNameValidatorSelector.MemberNamesFromExpressions(properties))

        if isinstance(properties[0], str):
            self._properties.extend(properties)
        else:
            self._properties.extend(MemberNameValidatorSelector.MemberNamesFromExpressions(properties))

        return self

    #     def IncludeRulesNotInRuleSet(self)->"ValidationStrategy[T]":
    #         self._ruleSets ??= new List<string>()
    #         self._ruleSets.Add(RulesetValidatorSelector.DefaultRuleSetName)
    #         return self

    #     def IncludeAllRuleSets()->"ValidationStrategy[T]":
    #         self._ruleSets ??= new List<string>()
    #         self._ruleSets.Add(RulesetValidatorSelector.WildcardRuleSetName)
    #         return self

    #     def IncludeRuleSets(params string[] ruleSets)->"ValidationStrategy[T]":
    #         if (ruleSets is not None && ruleSets.Length > 0) {
    #             if (self._ruleSets is None) {
    #                 self._ruleSets = new List<string>(ruleSets)
    #             }
    #             else {
    #                 self._ruleSets.AddRange(ruleSets)
    #             }
    #         }

    #         return self

    #     def UseCustomSelector(IValidatorSelector selector)->"ValidationStrategy[T]":
    #         if (selector is None) throw new ArgumentNoneException(nameof(selector))
    #         self._customSelector = selector
    #         return self

    #     def ThrowOnFailures()->"ValidationStrategy[T]":
    #         _throw = true
    #         return self

    def GetSelector(self) -> IValidatorSelector:
        selector: IValidatorSelector = None

        if self._properties is not None or self._ruleSets is not None or self._customSelector is not None:
            selectors: list[IValidatorSelector] = []

            if self._customSelector is not None:
                selectors.append(self._customSelector)

            if self._properties is not None:
                selectors.append(ValidatorOptions.Global.ValidatorSelectors.MemberNameValidatorSelectorFactory([self._properties]))

            if self._ruleSets is not None:
                selectors.append(ValidatorOptions.Global.ValidatorSelectors.RulesetValidatorSelectorFactory([self._ruleSets]))

            selector = selectors[0] if len(selectors) == 1 else ValidatorOptions.Global.ValidatorSelectors.CompositeValidatorSelectorFactory(selectors)
        else:
            selector = ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory()

        return selector

    def BuildContext(self, instance: T) -> "ValidationContext[T]":
        validation = ValidationContext[T](instance, None, self.GetSelector())
        validation.ThrowOnFailures = self._throw
        return validation
