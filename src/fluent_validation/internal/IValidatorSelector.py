from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.fluent_validation.IValidationContext import IValidationContext
    from src.fluent_validation.IValidationRule import IValidationRule


class IValidatorSelector(ABC):
    @abstractmethod
    def CanExecute(self, rule: IValidationRule, propertyPath: str, context: IValidationContext) -> bool: ...
