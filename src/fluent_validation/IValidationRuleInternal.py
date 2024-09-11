from __future__ import annotations
from abc import abstractmethod
from typing import Iterable, TYPE_CHECKING


from fluent_validation.IValidationRule import IValidationRule

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext


class IValidationRuleInternal[T, TProperty](IValidationRule[T, TProperty]):
    @abstractmethod
    async def ValidateAsync(context: ValidationContext[T], useAsync: bool): ...

    @abstractmethod
    def AddDependentRules(rules: Iterable[IValidationRuleInternal]) -> None: ...
