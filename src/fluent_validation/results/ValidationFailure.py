from typing import Any
from fluent_validation.enums import Severity as _Severity


class ValidationFailure:
    def __init__(
        self,
        PropertyName: str = None,
        ErrorMessage: str = None,
        AttemptedValue: object = None,
        ErrorCode: str = None,
    ):
        self._PropertyName: str = PropertyName
        self._ErrorMessage: str = ErrorMessage
        self._AttemptedValue: object = AttemptedValue

        self._CustomState: object = None
        self._ErrorCode: str = ErrorCode
        self._severity: _Severity = _Severity.Error
        self._FormattedMessagePlaceholderValues: dict[str, object] = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._PropertyName} {id(self)}>"

    @property
    def PropertyName(self) -> str:
        return self._PropertyName

    @property
    def ErrorMessage(self) -> str:
        return self._ErrorMessage

    @property
    def AttemptedValue(self) -> object:
        return self._AttemptedValue

    @property
    def CustomState(self) -> object:
        return self._CustomState

    @property
    def Severity(self) -> _Severity:
        return self._severity

    @Severity.setter
    def Severity(self, value: _Severity) -> None:
        self._severity = value

    @property
    def ErrorCode(self) -> str:
        return self._ErrorCode

    @ErrorCode.setter
    def ErrorCode(self, value: str) -> None:
        self._ErrorCode = value

    @property
    def FormattedMessagePlaceholderValues(self) -> dict[str, Any]:
        return self._FormattedMessagePlaceholderValues

    @FormattedMessagePlaceholderValues.setter
    def FormattedMessagePlaceholderValues(self, value: dict[str, Any]):
        self._FormattedMessagePlaceholderValues = value

    def __str__(self) -> str:
        return self._ErrorMessage
