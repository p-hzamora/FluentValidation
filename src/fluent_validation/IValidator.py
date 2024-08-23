from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, overload, Optional

if TYPE_CHECKING:
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy
    from src.fluent_validation.IValidationContext import IValidationContext
    from .results.ValidationResult import ValidationResult


class IValidator[T](ABC):
    @abstractmethod
    def Validate(instance: T) -> ValidationResult:
        ...
