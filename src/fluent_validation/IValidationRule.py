from abc import ABC, abstractmethod

from typing import Iterable, Callable
from .internal.IRuleComponent import IRuleComponent
from .IValidationContext import IValidationContext
from .internal.MessageBuilderContext import IMessageBuilderContext
from .validators.IpropertyValidator import IPropertyValidator


class IValidatoinRule_no_args(ABC):
    @property
    @abstractmethod
    def Components(self) -> Iterable[IRuleComponent]:
        ...

    @property
    @abstractmethod
    def PropertyName(self) -> str:
        ...

    @property
    @abstractmethod
    def TypeToValidate(self) -> type:
        ...

    @abstractmethod
    def get_display_name(context: IValidationContext) -> str:
        ...


class IValidationRule[T, TProperty](IValidatoinRule_no_args):
    @property
    @abstractmethod
    def Current(self) -> IRuleComponent:
        ...

    @abstractmethod
    def AddValidator(validator: IPropertyValidator[T, TProperty]):
        ...

    @property
    @abstractmethod
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]:
        ...  # {get; set;}


class IValidationRuleInternal[T, TProperty](IValidationRule[T, TProperty]):
    ...
