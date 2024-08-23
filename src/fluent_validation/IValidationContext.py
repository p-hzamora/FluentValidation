from typing import Any, Callable, Optional, Self, overload, override
from abc import ABC, abstractmethod

from src.fluent_validation.ValidatorOptions import ValidatorOptions
from src.fluent_validation.internal.IValidatorSelector import IValidatorSelector

from .internal.MessageFormatter import MessageFormatter
from .internal.PropertyChain import PropertyChain
from .results.ValidationFailure import ValidationFailure
from .internal.ValidationStrategy import ValidationStrategy


class IValidationContext(ABC):
    @property
    @abstractmethod
    def instance_to_validate(self) -> Any: ...

    @property
    @abstractmethod
    def RootContextData(self) -> dict[str, object]: ...

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

    # @property
    # @abstractmethod
    # def ParentContext(self)->Self: ...

    # @property
    # @abstractmethod
    # def IsAsync(self)->bool: ...

    @property
    @abstractmethod
    def ThrowOnFailures(self) -> bool: ...


class IHasFailures(ABC):
    @property
    @abstractmethod
    def Failures(self) -> list[ValidationFailure]: ...


class ValidationContext[T](IValidationContext, IHasFailures):
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

    def __init__one_attr(instanceToValidate: T):
        ValidationContext(instanceToValidate, None, ValidatorOptions.Global.ValidatorSelectors.DefaultValidatorSelectorFactory())

    def __init__three_attr(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector):
        ValidationContext(instanceToValidate, propertyChain, validatorSelector, [], ValidatorOptions.Global.MessageFormatterFactory())

    def __init__all_attr(self, instanceToValidate: T, propertyChain: PropertyChain, validatorSelector: IValidatorSelector, failures: list[ValidationFailure], messageFormatter: MessageFormatter):
        self._instance_to_validate = instanceToValidate

        self._PropertyChain = PropertyChain(propertyChain)
        self._Selector = validatorSelector
        self._failures: list[ValidationFailure] = failures if failures else []
        self._MessageFormatter = messageFormatter
        self._messageFormatter: MessageFormatter = messageFormatter if messageFormatter else MessageFormatter()
        self._property_path: Optional[str] = None
        self._displayNameFunc: Optional[str] = None
        self._ThrowOnFailures: bool = False
        self._RootContextData: dict[str, Any] = {}
        self._IsChildContext: bool = False
        self._IsChildCollectionContext: bool = False
        self._RawPropertyName:str = None

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
    def DisplayName(self) -> str:  # FIXME [x]: must be Callable[[self],str]
        return self._displayNameFunc(self)

    def InitializeForPropertyValidator(self, propertyPath: str, displayNameFunc: Callable[[Self], str], rawPropertyName: str) -> None:
        self._property_path = propertyPath
        self._displayNameFunc = displayNameFunc
        # it used in 'CreateNewValidationContextForChildValidator' method
        self.RawPropertyName = rawPropertyName
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
    def RootContextData(self) -> dict[str, Any]:
        return self._RootContextData

    @RootContextData.setter
    def RootContextData(self, value: dict[str, Any]) -> None:
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

    # # This is the root context so it doesn't have a parent.
    # # Explicit implementation so it's not exposed necessarily.
    # IValidationContext IValidationContext.ParentContext => _parentContext;

    # public bool IsAsync {
    # 	get;
    # 	internal set;
    # }

    @override
    @property
    def ThrowOnFailures(self) -> bool:
        return self._ThrowOnFailures

    @override
    @ThrowOnFailures.setter
    def ThrowOnFailures(self, value: bool) -> None:
        self._ThrowOnFailures = value

    # private Dictionary<string, Dictionary<T, bool>> _sharedConditionCache;

    # internal Dictionary<string, Dictionary<T, bool>> SharedConditionCache {
    # 	get {
    # 		_sharedConditionCache ??= new();
    # 		return _sharedConditionCache;
    # 	}
    # }

    @staticmethod
    def GetFromNonGenericContext(context: IValidationContext) -> "ValidationContext[T]":
        # Already of the correct type.
        if isinstance(context, ValidationContext):
            return context

        # Use None in isinstance because 'default' does not exist in python
        # Parameters match
        if not isinstance(context.instance_to_validate, ValidationContext):
            ValueError(f"Cannot validate instances of type '{type(context.instance_to_validate)}' This validator can only validate instances of type '{ValidationContext.__name__}'.")

        failures = context.Failures if isinstance(context, IHasFailures) else []
        validation = ValidationContext[T](context.instance_to_validate, context.PropertyChain, context.Selector, failures, ValidatorOptions.Global.MessageFormatterFactory())
        validation.IsChildContext = (context.IsChildContext,)
        validation.RootContextData = (context.RootContextData,)
        validation.ThrowOnFailures = (context.ThrowOnFailures,)
        # validation._parentContext = context.ParentContext,
        # validation.IsAsync = context.IsAsync
        return validation
