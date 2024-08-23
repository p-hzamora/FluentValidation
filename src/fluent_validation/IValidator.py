from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, overload

if TYPE_CHECKING:
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy
    from src.fluent_validation.IValidationContext import IValidationContext
    from .results.ValidationResult import ValidationResult


class IValidator[T](ABC):
    @overload
    def validate(validator: "IValidator[T]", instance: T) -> ValidationResult: ...

    @overload
    def validate(validator: "IValidator[T]", instance: IValidationContext) -> ValidationResult: ...

    @overload
    def validate(validator: "IValidator[T]", instance: T, options: Callable[[ValidationStrategy[T]], None]) -> ValidationResult: ...

    @abstractmethod
    def validate(validator, instance, options): ...
