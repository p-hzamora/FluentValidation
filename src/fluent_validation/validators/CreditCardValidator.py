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

from abc import ABC
from typing import override

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.IValidationContext import ValidationContext


class ICreditCardValidator(ABC): ...


class CreditCardValidator[T](PropertyValidator[T, str], ICreditCardValidator):
    """
    Ensures that the property value is a valid credit card number.
    This logic was taken from the CreditCardAttribute in the ASP.NET MVC3 source.
    """

    def __init__(self) -> None:
        super().__init__()

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)

    @override
    def is_valid(self, context: ValidationContext[T], value: str) -> str:
        if value is None:
            return True

        if not isinstance(value, str):
            return False

        value = value.replace("-", "").replace(" ", "")

        checksum: int = 0
        evenDigit: bool = False
        # http://www.beachnet.com/~hstiles/cardtype.html
        for digit in value[::-1]:
            if not digit.isdigit():
                return False

            digitValue: int = int(digit) * (2 if evenDigit else 1)
            evenDigit = not evenDigit

            while digitValue > 0:
                checksum += digitValue % 10
                digitValue //= 10

        return (checksum % 10) == 0
