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

from enum import Enum
from typing import override, Type

from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.enums import StringComparer
from fluent_validation.validators.PropertyValidator import PropertyValidator


class StringEnumValidator[T](PropertyValidator[T, str]):
    def __init__(self, enumType: Type[Enum], caseSensitive: bool):
        if enumType is None:
            raise TypeError("enumType")

        self.CheckTypeIsEnum(enumType)

        self._caseSensitive: bool = caseSensitive
        self._enumNames: list[str] = [x.name for x in enumType]

    @override
    def is_valid(self, context: ValidationContext[T], value: str) -> bool:
        if value is None:
            return True
        comparison = StringComparer.Ordinal if self._caseSensitive else StringComparer.OrdinalIgnoreCase
        return any([comparison(value, x) for x in self._enumNames])

    def CheckTypeIsEnum(self, enumType: Type[Enum]) -> None:
        if not issubclass(enumType, Enum):
            message: str = f"The type '{enumType.__name__}' is not an enum and can't be used with is_enum_name. (Parameter 'enumType')"
            raise TypeError(message)

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        # Intentionally the same message as EnumValidator.
        return self.Localized(errorCode, "EnumValidator")
