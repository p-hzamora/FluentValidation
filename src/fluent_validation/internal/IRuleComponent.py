from abc import ABC, abstractmethod
from typing import Any, Callable, overload

from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.enums import Severity

from fluent_validation.validators.IpropertyValidator import IPropertyValidator


class IRuleComponent_no_args(ABC):
    @property
    @abstractmethod
    def HasCondition(self) -> bool: ...

    @property
    @abstractmethod
    def HasAsyncCondition(self) -> bool: ...

    @property
    @abstractmethod
    def Validator(self) -> IPropertyValidator: ...

    @abstractmethod
    def GetUnformattedErrorMessage(self) -> str: ...

    @property
    @abstractmethod
    def ErrorCode(self) -> str: ...


class IRuleComponent[T, TProperty](IRuleComponent_no_args):
    @property
    @abstractmethod
    def ErrorCode(self) -> str: ...

    @ErrorCode.setter
    @abstractmethod
    def ErrorCode(self, value: str) -> None: ...

    @property
    @abstractmethod
    def CustomStateProvider(self, value: Any) -> Callable[[ValidationContext[T], TProperty], object]: ...
    @property
    @abstractmethod
    def SeverityProvider(self, value: Any) -> Callable[[ValidationContext[T], TProperty], Severity]: ...

    @abstractmethod
    def ApplyCondition(self, condition: Callable[[ValidationContext[T]], bool]) -> None: ...

    # @abstractmethod
    # def ApplyAsyncCondition(condition: Callable[[ValidationContext[T]], bool]) -> None: ...  # void ApplyAsyncCondition(Func<ValidationContext<T>, CancellationToken, Task<bool>> condition);

    # COMMENT: errorFactory has been replaced by 'errorMessage' due to in Python there's no exist method overloading
    @overload
    def set_error_message(self, error_message: Callable[[ValidationContext[T], TProperty], str]) -> None: ...

    @overload
    def set_error_message(self, error_message: str) -> None: ...

    @abstractmethod
    def set_error_message(self, error_message): ...  # real name SetErrorMessage
