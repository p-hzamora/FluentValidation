from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Iterable, Callable, TYPE_CHECKING, TypeVar

# from src.fluent_validation.enums import ApplyConditionTo

if TYPE_CHECKING:
    # from src.fluent_validation.IValidationContext import ValidationContext
    from .internal.IRuleComponent import IRuleComponent
    from .IValidationContext import IValidationContext
    from .internal.MessageBuilderContext import IMessageBuilderContext
    from .validators.IpropertyValidator import IPropertyValidator


class IValidatoinRule_no_args(ABC):
    @property
    @abstractmethod
    def Components(self) -> Iterable[IRuleComponent]: ...

    @property
    @abstractmethod
    def RuleSets(self) -> set[str]: ...

    @RuleSets.setter
    @abstractmethod
    def RuleSets(self, value: set[str]) -> None: ...

    @abstractmethod
    def get_display_name(context: IValidationContext) -> str: ...

    @property
    @abstractmethod
    def PropertyName(self) -> str: ...

    @property
    @abstractmethod
    def TypeToValidate(self) -> type: ...

    # bool HasCondition { get; }

    # bool HasAsyncCondition { get; }

    # LambdaExpression Expression { get; }

    # @property
    # @abstractmethod
    # def DependentRules(self) -> Iterable[IValidationRule]: ...


CancellationToken = TypeVar("CancellationToken")


class IValidationRule_one_arg[T](IValidatoinRule_no_args):
    ...
    # @abstractmethod
    # def ApplyCondition(predicate: Callable[[ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    # @abstractmethod
    # def ApplyAsyncCondition(predicate: Callable[[ValidationContext[T], CancellationToken], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    # @abstractmethod
    # def ApplySharedCondition(condition: Callable[[ValidationContext[T]], bool]): ...

    # @abstractmethod
    # def ApplySharedAsyncCondition(condition: Callable[[ValidationContext[T], CancellationToken], bool]): ...


class IValidationRule[T, TProperty](IValidationRule_one_arg[T]):
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
