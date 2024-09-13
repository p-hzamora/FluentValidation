from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Callable, TYPE_CHECKING, TypeVar, overload

from fluent_validation.enums import ApplyConditionTo
from fluent_validation.LambdaExpression import LambdaExpression

if TYPE_CHECKING:
    from fluent_validation.enums import CascadeMode as _CascadeMode
    from fluent_validation.IValidationContext import ValidationContext
    from .internal.IRuleComponent import IRuleComponent
    from .IValidationContext import IValidationContext
    from .internal.MessageBuilderContext import IMessageBuilderContext
    from .validators.IpropertyValidator import IPropertyValidator
    from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator


class IValidatoinRule_no_args(ABC):
    @property
    @abstractmethod
    def Components(self) -> list[IRuleComponent]: ...

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

    @property
    @abstractmethod
    def HasCondition(self) -> bool: ...

    @property
    @abstractmethod
    def HasAsyncCondition(self) -> bool: ...

    @property
    @abstractmethod
    def Expression(self) -> LambdaExpression: ...

    @property
    @abstractmethod
    def DependentRules(self) -> list[IValidationRule]: ...


CancellationToken = TypeVar("CancellationToken")


class IValidationRule_one_arg[T](IValidatoinRule_no_args):
    ...

    @abstractmethod
    def ApplyCondition(self, predicate: Callable[[ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    # @abstractmethod
    # def ApplyAsyncCondition(self, predicate: Callable[[ValidationContext[T], CancellationToken], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    @abstractmethod
    def ApplySharedCondition(self, condition: Callable[[ValidationContext[T]], bool]): ...

    # @abstractmethod
    # def ApplySharedAsyncCondition(self, condition: Callable[[ValidationContext[T], CancellationToken], bool]): ...


class IValidationRule[T, TProperty](IValidationRule_one_arg[T]):
    @overload
    def SetDisplayName(self, name: str) -> None: ...
    @overload
    def SetDisplayName(self, name: Callable[[ValidationContext[T]], str]) -> None: ...

    @abstractmethod
    def SetDisplayName(self, name: str | Callable[[ValidationContext[T]], str]) -> None: ...

    @property
    @abstractmethod
    def CascadeMode(self) -> _CascadeMode: ...

    @abstractmethod
    def AddValidator(self, validator: IPropertyValidator[T, TProperty]): ...

    @abstractmethod
    def AddAsyncValidator(self, asyncValidator: IAsyncPropertyValidator[T, TProperty], fallback: IPropertyValidator[T, TProperty] = None) -> None: ...

    @property
    @abstractmethod
    def Current(self) -> IRuleComponent: ...

    @property
    @abstractmethod
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]: ...  # {get; set;}

    @MessageBuilder.setter
    @abstractmethod
    def MessageBuilder(self, value: Callable[[IMessageBuilderContext[T, TProperty]], str]) -> None: ...
