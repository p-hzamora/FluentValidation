# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

from typing import Any
from fluent_validation.enums import Severity as _Severity


class ValidationFailure:
    __slots__ = (
        "_PropertyName",
        "_ErrorMessage",
        "_AttemptedValue",
        "_CustomState",
        "_ErrorCode",
        "_severity",
        "_FormattedMessagePlaceholderValues",
    )

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

    @CustomState.setter
    def CustomState(self, v: Any) -> object:
        self._CustomState = v

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
