from abc import ABC, abstractmethod
from typing import override
from fluent_validation.IValidationContext import IValidationContext, ValidationContext
from fluent_validation.internal.RuleComponent import RuleComponent

from fluent_validation.internal.IRuleComponent import IRuleComponent
from fluent_validation.validators.IpropertyValidator import IPropertyValidator

from fluent_validation.internal.MessageFormatter import MessageFormatter


class IMessageBuilderContext[T, TProperty](ABC):
    @property
    @abstractmethod
    def Component(self) -> IRuleComponent: ...

    @property
    @abstractmethod
    def PropertyValidator(self) -> IPropertyValidator: ...

    @property
    @abstractmethod
    def ParentContext(self) -> IValidationContext: ...

    @property
    @abstractmethod
    def PropertyName(self) -> str: ...

    @property
    @abstractmethod
    def DisplayName(self) -> str: ...

    @property
    @abstractmethod
    def MessageFormatter(self) -> MessageFormatter: ...

    @property
    @abstractmethod
    def InstanceToValidate(self) -> T: ...

    @property
    @abstractmethod
    def PropertyValue(self) -> TProperty: ...

    @abstractmethod
    def GetDefaultMessage() -> str: ...


class MessageBuilderContext[T, TProperty](IMessageBuilderContext[T, TProperty]):
    _innerContext: ValidationContext[T]
    _value: TProperty

    def __init__(
        self,
        innerContext: ValidationContext[T],
        value: TProperty,
        component: RuleComponent[T, TProperty],
    ):
        self._innerContext = innerContext
        self._value = value
        self._component = component

    @property
    def Component(self) -> RuleComponent[T, TProperty]:
        return self._component

    # IRuleComponent[T, TProperty] IMessageBuilderContext[T, TProperty].Component => Component;

    @property
    def PropertyValidator(self) -> IPropertyValidator:
        return self.Component.Validator

    @property
    def ParentContext(self) -> ValidationContext[T]:
        return self._innerContext

    @override
    @property
    def PropertyName(self) -> str:
        return self._innerContext.PropertyPath

    @override
    @property
    def DisplayName(self) -> str:
        return self._innerContext.DisplayName

    @property
    def MessageFormatter(self) -> MessageFormatter:
        return self._innerContext.MessageFormatter

    @property
    def InstanceToValidate(self) -> T:
        return self._innerContext.instance_to_validate

    @property
    def PropertyValue(self) -> TProperty:
        return self._value

    def GetDefaultMessage(self) -> str:
        return self.Component.GetErrorMessage(self._innerContext, self._value)
