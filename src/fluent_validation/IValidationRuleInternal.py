from __future__ import annotations
from abc import abstractmethod
from typing import Iterable, TYPE_CHECKING


from src.fluent_validation.IValidationRule import IValidationRule

if TYPE_CHECKING:
    from src.fluent_validation.IValidationContext import ValidationContext


class IValidationRuleInternal[T, TProperty](IValidationRule[T, TProperty]):
    @abstractmethod
    def ValidateAsync(context: ValidationContext[T], useAsync: bool): ...

    @abstractmethod
    async def AddDependentRules(rules: Iterable[IValidationRuleInternal]): ...
