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
