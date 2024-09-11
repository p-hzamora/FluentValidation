from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext


class IPropertyValidator_no_generic(ABC):
    @property
    @abstractmethod
    def Name(self) -> str: ...

    @abstractmethod
    def get_default_message_template(self, error_code: str) -> str: ...


class IPropertyValidator[T, TProperty](IPropertyValidator_no_generic):
    @abstractmethod
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool: ...


class IAsyncPropertyValidator[T, TProperty](IPropertyValidator_no_generic):
    @abstractmethod
    async def IsValidAsync(self, context: ValidationContext[T], value: TProperty) -> bool: ...
