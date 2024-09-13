from __future__ import annotations
from typing import Any, Callable, NamedTuple, Optional, Self, overload, override
from abc import ABC, abstractmethod
from collections import deque

from fluent_validation.ValidatorOptions import ValidatorOptions
from fluent_validation.internal.IValidatorSelector import IValidatorSelector

from .internal.MessageFormatter import MessageFormatter
from .internal.PropertyChain import PropertyChain
from .results.ValidationFailure import ValidationFailure
from .internal.ValidationStrategy import ValidationStrategy


class StackParams[T](NamedTuple):
    IsChildContext: bool
    IsChildCollectionContext: bool
    ParentContext: IValidationContext
    Chain: PropertyChain
    SharedConditionCache: dict[str, dict[T, bool]]


class IValidationContext(ABC):
    @property
    @abstractmethod
    def instance_to_validate(self) -> Any: ...

    @property
    @abstractmethod
    def RootContextData(self) -> dict[str, set[str]]: ...

    @property
    @abstractmethod
    def PropertyChain(self) -> dict[str, object]: ...

    @property
    @abstractmethod
    def Selector(self) -> IValidatorSelector: ...

    @property
    @abstractmethod
    def IsChildContext(self) -> bool: ...

    @property
    @abstractmethod
    def IsChildCollectionContext(self) -> bool: ...

    @property
    @abstractmethod
    def ParentContext(self) -> Self: ...

    @property
    @abstractmethod
    def IsAsync(self) -> bool: ...

    @property
    @abstractmethod
    def ThrowOnFailures(self) -> bool: ...


class IHasFailures(ABC):
    @property
    @abstractmethod
    def Failures(self) -> list[ValidationFailure]: ...


class ValidationContext[T](IValidationContext, IHasFailures):
    __slots__ = (
        "_instance_to_validate",
        "_PropertyChain",
        "_Selector",
        "_failures",
        "_messageFormatter",
        "_property_path",
        "_displayNameFunc",
        "_ThrowOnFailures",
        "_RootContextData",
        "_IsChildContext",
        "_IsChildCollectionContext",
        "_RawPropertyName",
        "_is_async",
        "_parentContext",
        "_sharedConditionCache",
    )

    @overload
    def __init__(self, instanceToValidate: T): ...
    @overload
    def __init__(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector): ...
    @overload
    def __init__(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector, failures: list[ValidationFailure], messageFormatter: MessageFormatter): ...

    def __init__(
        self,
        instance_to_validate: Optional[T] = None,
        propertyChain: Optional[PropertyChain] = None,
        validatorSelector: Optional[IValidatorSelector] = None,
        failures: Optional[list[ValidationFailure]] = None,
        messageFormatter: Optional[MessageFormatter] = None,
    ):
        if instance_to_validate and all(x is None for x in [propertyChain, validatorSelector, failures, messageFormatter]):
            self.__init__one_attr(instance_to_validate)
        elif instance_to_validate and propertyChain and validatorSelector and all(x is None for x in [failures, messageFormatter]):
            self.__init__three_attr(instance_to_validate, propertyChain, validatorSelector)
        else:
            self.__init__all_attr(instance_to_validate, propertyChain, validatorSelector, failures, messageFormatter)

    def __init__one_attr(self, instanceToValidate: T):
        self.__init__(instanceToValidate, None, ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory())

    def __init__three_attr(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector):
        self.__init__(instanceToValidate, propertyChain, validatorSelector, [], ValidatorOptions.Global.MessageFormatterFactory())

    def __init__all_attr(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector, failures: list[ValidationFailure], messageFormatter: MessageFormatter):
        self._instance_to_validate: T = instanceToValidate

        self._PropertyChain = PropertyChain(propertyChain)
        self._Selector = validatorSelector
        # COMMENT!!: I added 'is not None' to the 'failures if failures else []' conditional because the 'failures' variable could be an empty list, and otherwise, it could return False.
        # It was creating an empty list instead of assigning the original list when 'failures' was an empty list.
        # That's the reason why failures was not passed by reference and the information was not propagated properly.
        self._failures: list[ValidationFailure] = failures if failures is not None else []
        self._messageFormatter: MessageFormatter = messageFormatter if messageFormatter is not None else MessageFormatter()
        self._property_path: Optional[str] = None
        self._displayNameFunc: Optional[str] = None
        self._ThrowOnFailures: bool = False
        self._RootContextData: dict[str, Any] = {}
        self._IsChildContext: bool = False
        self._IsChildCollectionContext: bool = False
        self._RawPropertyName: str = None
        self._is_async: bool = False
        self._parentContext: IValidationContext = None
        self._sharedConditionCache: dict[str, dict[T, bool]] = None
        self._state: deque[StackParams] = None

    @override
    @property
    def Failures(self) -> list[ValidationFailure]:
        return self._failures

    @property
    def MessageFormatter(self) -> MessageFormatter:
        return self._messageFormatter

    @property
    def PropertyPath(self) -> str:
        return self._property_path

    @property
    def RawPropertyName(self) -> str:
        return self._RawPropertyName

    @RawPropertyName.setter
    def RawPropertyName(self, value: str) -> str:
        self._RawPropertyName = value

    @property
    def DisplayName(self) -> Optional[str]:
        if self._displayNameFunc:
            return self._displayNameFunc(self)
        return None

    @staticmethod
    def CreateWithOptions(instanceToValidate: T, options: Callable[[ValidationStrategy], None]) -> "ValidationContext[T]":
        strategy = ValidationStrategy()
        options(strategy)
        return strategy.BuildContext(instanceToValidate)

    @override
    @property
    def instance_to_validate(self) -> T:
        return self._instance_to_validate

    @instance_to_validate.setter
    def instance_to_validate(self, value: T) -> None:
        self._InstanceToValidate = value

    @override
    @property
    def RootContextData(self) -> dict[str, set[str]]:
        return self._RootContextData

    @RootContextData.setter
    def RootContextData(self, value: dict[str, set[str]]) -> None:
        self._RootContextData = value

    @property
    def PropertyChain(self) -> PropertyChain:
        return self._PropertyChain

    @PropertyChain.setter
    def PropertyChain(self, value: PropertyChain) -> None:
        self._PropertyChain = value

    # object IValidationContext.InstanceToValidate => InstanceToValidate

    @override
    @property
    def Selector(self) -> IValidatorSelector:
        return self._Selector

    @Selector.setter
    def Selector(self, value: IValidatorSelector) -> None:
        self._Selector = value

    @override
    @property
    def IsChildContext(self) -> bool:
        return self._IsChildContext

    @IsChildContext.setter
    def IsChildContext(self, value: bool) -> None:
        self._IsChildContext = value

    @override
    @property
    def IsChildCollectionContext(self) -> bool:
        return self._IsChildCollectionContext

    @IsChildCollectionContext.setter
    def IsChildCollectionContext(self, value: bool) -> None:
        self._IsChildCollectionContext = value

    # This is the root context so it doesn't have a parent.
    # Explicit implementation so it's not exposed necessarily.
    @property
    def ParentContext(self) -> IValidationContext:
        return self._parentContext

    @property
    def IsAsync(self) -> bool:
        return self._is_async

    @IsAsync.setter
    def IsAsync(self, value: bool) -> None:
        self._is_async = value

    @override
    @property
    def ThrowOnFailures(self) -> bool:
        return self._ThrowOnFailures

    @override
    @ThrowOnFailures.setter
    def ThrowOnFailures(self, value: bool) -> None:
        self._ThrowOnFailures = value

    @property
    def SharedConditionCache(self) -> dict[str, dict[T, bool]]:
        if self._sharedConditionCache is None:
            self._sharedConditionCache = {}
        return self._sharedConditionCache

    @staticmethod
    def GetFromNonGenericContext(context: IValidationContext) -> "ValidationContext[T]":
        # Already of the correct type.
        # FIXME [ ]: this conditional is not working properly. The original is '(context is ValidationContext<T> c)'
        if isinstance(context, ValidationContext):
            return context

        # Use None in isinstance because 'default' does not exist in python
        # Parameters match
        if not isinstance(context.instance_to_validate, ValidationContext):
            raise ValueError(f"Cannot validate instances of type '{type(context.instance_to_validate)}' This validator can only validate instances of type '{ValidationContext.__name__}'.")

        failures = context.Failures if isinstance(context, IHasFailures) else []
        validation = ValidationContext[T](context.instance_to_validate, context.PropertyChain, context.Selector, failures, ValidatorOptions.Global.MessageFormatterFactory())
        validation.IsChildContext = context.IsChildContext
        validation.RootContextData = context.RootContextData
        validation.ThrowOnFailures = context.ThrowOnFailures
        validation._parentContext = context.ParentContext
        validation._is_async = context.IsAsync
        return validation

    def CloneForChildValidator[TChild](self, instanceToValidate: TChild, preserveParentContext: bool = False, selector: Optional[IValidatorSelector] = None) -> ValidationContext[TChild]:
        _selector = self.Selector if not selector else selector
        res = ValidationContext[TChild](instanceToValidate, self.PropertyChain, _selector, self.Failures, self.MessageFormatter)
        res.IsChildContext = True
        res.RootContextData = self.RootContextData
        res._parentContext = (self if preserveParentContext else None,)
        res._is_async = self.IsAsync
        return res

    def PrepareForChildCollectionValidator(self) -> None:
        if not self._state:
            self._state = deque()

        self._state.append(StackParams(self.IsChildContext, self.IsChildCollectionContext, self._parentContext, self.PropertyChain, self._sharedConditionCache))
        self.IsChildContext = True
        self.IsChildCollectionContext = True
        self._parentContext = self._parentContext
        self.PropertyChain = PropertyChain()
        self._sharedConditionCache = self._sharedConditionCache

    def RestoreState(self) -> None:
        state = self._state.pop()
        self.IsChildContext = state.IsChildContext
        self.IsChildCollectionContext = state.IsChildCollectionContext
        self._parentContext = state.ParentContext
        self.PropertyChain = state.Chain
        self._sharedConditionCache = state.SharedConditionCache

    def AddFailure_validationFailure(self, failure: ValidationFailure) -> None:
        self.Failures.append(failure)

    def AddFailure_property_errorMssg(self, propertyName: str, errorMessage: str) -> None:
        errorMessage = MessageFormatter.BuildMessage(errorMessage)
        prop_name: str = propertyName if propertyName is not None else ""
        self.AddFailure(ValidationFailure(PropertyChain.BuildPropertyPath(prop_name), errorMessage))

    def AddFailure_errorMssg(self, errorMessage: str) -> None:
        errorMessage = MessageFormatter.BuildMessage(errorMessage)
        self.AddFailure(ValidationFailure(self.PropertyPath, errorMessage))

    @overload
    def AddFailure(self, failure: ValidationFailure) -> None: ...
    @overload
    def AddFailure(self, propertyName: str, errorMessage: str) -> None: ...
    @overload
    def AddFailure(self, errorMessage: str) -> None: ...

    def AddFailure(self, failure: Optional[ValidationFailure] = None, propertyName: Optional[str] = None, errorMessage: Optional[str] = None) -> None:
        if failure and not all([propertyName, errorMessage]):
            self.AddFailure_validationFailure(failure)
        elif not all([failure, propertyName]) and errorMessage:
            self.AddFailure_errorMssg(errorMessage)
        elif not failure and propertyName is not None and errorMessage is not None:
            self.AddFailure_property_errorMssg(propertyName, errorMessage)
        else:
            raise AttributeError

    def InitializeForPropertyValidator(self, propertyPath: str, displayNameFunc: Callable[[Self], str], rawPropertyName: str) -> None:
        self._property_path = propertyPath
        self._displayNameFunc = displayNameFunc
        # it used in 'CreateNewValidationContextForChildValidator' method
        self.RawPropertyName = rawPropertyName
        return None
