from typing import Iterable, override
from src.fluent_validation.IValidationContext import IValidationContext
from src.fluent_validation.IValidationRule import IValidationRule
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector


class CompositeValidatorSelector(IValidatorSelector):
    def __init__(self, selectors: Iterable[IValidatorSelector]):
        self._selectors: Iterable[IValidatorSelector] = selectors

    @override
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool:
        return any([s.CanExecute(rule, propertyPath, context) for s in self._selectors])
