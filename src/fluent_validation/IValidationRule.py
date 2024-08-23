from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Iterable, Callable, TYPE_CHECKING
from .internal.IRuleComponent import IRuleComponent

if TYPE_CHECKING:
    from .IValidationContext import IValidationContext
    from .internal.MessageBuilderContext import IMessageBuilderContext
    from .validators.IpropertyValidator import IPropertyValidator


class IValidatoinRule_no_args(ABC):
    @property
    @abstractmethod
    def Components(self) -> Iterable[IRuleComponent]: ...

    @property
    @abstractmethod
    def PropertyName(self) -> str: ...

    @property
    @abstractmethod
    def TypeToValidate(self) -> type: ...

    @property
    @abstractmethod
    def RuleSets(self) -> set[str]: ...

    @RuleSets.setter
    @abstractmethod
    def RuleSets(self, value: set[str]) -> None: ...

    @abstractmethod
    def get_display_name(context: IValidationContext) -> str: ...


class IValidationRule[T, TProperty](IValidatoinRule_no_args):
    @property
    @abstractmethod
    def Current(self) -> IRuleComponent: ...

    @abstractmethod
    def AddValidator(validator: IPropertyValidator[T, TProperty]): ...

    @property
    @abstractmethod
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]: ...  # {get; set;}

    @MessageBuilder.setter
    @abstractmethod
    def MessageBuilder(self, value: Callable[[IMessageBuilderContext[T, TProperty]], str]) -> None: ...


class IValidationRuleInternal[T, TProperty](IValidationRule[T, TProperty]): ...
