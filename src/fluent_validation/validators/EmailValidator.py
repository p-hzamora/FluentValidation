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

from __future__ import annotations
import enum
import re
import typing

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.validators.RegularExpressionValidator import IRegularExpressionValidator
from fluent_validation.IValidationContext import ValidationContext


class IEmailValidator: ...


class EmailValidationMode(enum.Enum):
    """Defines which mode should be used for email validation."""

    """Uses a regular expression for email validation. This is the same regex used by the EmailAddressAttribute in .NET 4.x."""
    # [Obsolete("Regex-based email validation is not recommended and is no longer supported.")]
    Net4xRegex = (enum.auto(),)

    """Uses the simplified ASP.NET Core logic for checking an email address, which just checks for the presence of an @ sign."""
    AspNetCoreCompatible = (enum.auto(),)


# Email regex matches the one used in the DataAnnotations EmailAddressAttribute for consistency/parity with DataAnnotations. This is not a fully comprehensive solution, but is "good enough" for most cases.
# [Obsolete("Regex-based email validation is not recommended and is no longer supported.")]
class EmailValidator[T](PropertyValidator[T, str], IRegularExpressionValidator, IEmailValidator):
    expression: str = r"^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-||_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+([a-z]+|\d|-|\.{0,1}|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])?([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$"

    def __init__(self) -> None:
        self._regex: re = self.CreateRegEx()

    @property
    def Name(self) -> str:
        return "EmailValidator"

    @typing.override
    def is_valid(self, context: ValidationContext[T], value: str) -> bool:
        if value is None:
            return True

        if not self._regex.match(value):
            return False

        return True

    @property
    def Expression(self) -> str:
        return self._expression

    @classmethod
    def CreateRegEx(cls) -> re.Pattern:
        return re.compile(cls.expression, re.IGNORECASE)

    @typing.override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)


class AspNetCoreCompatibleEmailValidator[T](PropertyValidator[T, str], IEmailValidator):
    @property
    def Name(self) -> str:
        return "EmailValidator"

    @typing.override
    def is_valid(self, context: ValidationContext[T], value: str) -> bool:
        if value is None:
            return True

        # only return True if there is only 1 '@' character
        # and it is neither the first nor the last character
        count = value.count("@")
        index: int = value.index("@") if count > 0 else 0

        return all(
            [
                index is not None,
                index > 0,
                index != len(value) - 1,
                count == 1,
            ]
        )

    @typing.override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)
