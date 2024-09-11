from __future__ import annotations
from typing import Iterable, override, TYPE_CHECKING

from fluent_validation.internal.IValidatorSelector import IValidatorSelector

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import IValidationContext
    from fluent_validation.IValidationRule import IValidationRule


class CompositeValidatorSelector(IValidatorSelector):
    def __init__(self, selectors: Iterable[IValidatorSelector]):
        self._selectors: Iterable[IValidatorSelector] = selectors

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool:
        return any([s.CanExecute(rule, propertyPath, context) for s in self._selectors])
