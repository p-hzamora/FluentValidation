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
    def IncludeProperties(self, *properties: str) -> ValidationStrategy[T]: ...
    @overload
    def IncludeProperties(self, *properties: Callable[[T, object]]) -> ValidationStrategy[T]: ...

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
        if not self._ruleSets:
            self._ruleSets = []
        self._ruleSets.append(RulesetValidatorSelector.DefaultRuleSetName)
        return self

    def IncludeAllRuleSets(self) -> ValidationStrategy[T]:
        if not self._ruleSets:
            self._ruleSets = []
        self._ruleSets.append(RulesetValidatorSelector.WildcardRuleSetName)
        return self

    def IncludeRuleSets(self, *ruleSets: str) -> ValidationStrategy[T]:
        if ruleSets is not None and len(ruleSets) > 0:
            if self._ruleSets is None:
                self._ruleSets = list(ruleSets)
            else:
                self._ruleSets.extend(ruleSets)
        return self

    def UseCustomSelector(self, selector: IValidatorSelector) -> ValidationStrategy[T]:
        self._customSelector = selector
        return self

    def ThrowOnFailures(self) -> ValidationStrategy[T]:
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
