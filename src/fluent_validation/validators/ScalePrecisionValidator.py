# Attribution: This class was contributed to FluentValidation using code posted on StackOverflow by Jon Skeet
# The original code can be found at https:#stackoverflow.com/a/764102
# [p-hzamora] I've tried to adapt it with Decimal object in Python

from decimal import Decimal
from typing import override, NewType

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.IValidationContext import ValidationContext

UInt = NewType("UInt", int)

class ScalePrecisionValidator[T](PropertyValidator[T, Decimal]):
    """
    Allows a decimal to be validated for scale and precision.
    Scale would be the number of digits to the right of the decimal point.
    Precision would be the number of digits. This number includes both the left and the right sides of the decimal point.

    It implies certain range of values that will be accepted by the validator.
    It permits up to Precision - Scale digits to the left of the decimal point and up to Scale digits to the right.

    It can be configured to use the effective scale and precision
    (i.e. ignore trailing zeros) if required.

    123.4500 has an scale of 4 and a precision of 7, but an effective scale
    and precision of 2 and 5 respectively.
    """

    # TODO: For 12.0 swap the parameter order to match the PrecisionScale extension methods and add parameter for IgnoreTrailingZeros.
    def __init__(self, scale: int, precision: int, ignoreTrailingZeros: bool = False):
        self._Scale: int = scale
        self._Precision: int = precision
        self._IgnoreTrailingZeros: bool = ignoreTrailingZeros

        if self.Scale < 0:
            raise ValueError(f"Scale must be a positive integer. [value:{self.Scale}].")
        if self.Precision < 0:
            raise ValueError(f"Precision must be a positive integer. [value:{self.Precision}].")
        if self.Precision < self.Scale:
            raise ValueError(f"Scale must be less than precision. [scale:{self.Scale}, precision:{self.Precision}].")

    @property
    def Scale(self) -> int:
        return self._Scale

    @Scale.setter
    def Scale(self, value: int) -> None:
        self._Scale = value

    @property
    def Precision(self) -> int:
        return self._Precision

    @Precision.setter
    def Precision(self, value: int) -> None:
        self._Precision = value

    @property
    def IgnoreTrailingZeros(self) -> bool:
        return self._IgnoreTrailingZeros

    @IgnoreTrailingZeros.setter
    def IgnoreTrailingZeros(self, value: bool) -> None:
        self._IgnoreTrailingZeros = value

    @override
    def is_valid(self, context: ValidationContext[T], decimalValue: Decimal) -> bool:
        # TODOM: That conditional does not exist in the original code. Check it
        if decimalValue is None:
            return True

        scale = self.GetScale(decimalValue)
        precision = self.GetPrecision(decimalValue)
        actualIntegerDigits = precision - scale
        expectedIntegerDigits = self.Precision - self.Scale
        if scale > self.Scale or actualIntegerDigits > expectedIntegerDigits:
            # Precision and scale alone may not be enough to describe why a value is invalid.
            # For example, given an expected precision of 3 and scale of 2, the value "123" is invalid, even though precision
            # is 3 and scale is 0. So as a workaround we can provide actual precision and scale as if value
            # was "right-padded" with zeros to the amount of expected decimals, so that it would look like
            # complement zeros were added in the decimal part for calculation of precision. In the above
            # example actual precision and scale would be printed as 5 and 2 as if value was 123.00.
            printedActualScale = max(scale, self.Scale)
            printedActualPrecision = max(actualIntegerDigits, 1) + printedActualScale

            (
                context.MessageFormatter.AppendArgument("ExpectedPrecision", self.Precision)
                .AppendArgument("ExpectedScale", self.Scale)
                .AppendArgument("Digits", printedActualPrecision)
                .AppendArgument("ActualScale", printedActualScale),
            )

            return False

        return True

    def GetMantissa(self, decimal: Decimal) -> Decimal:
        # bits = self.GetBits(decimal)
        # return (bits[2] * 4294967296m * 4294967296m) + (bits[1] * 4294967296m) + bits[0]
        return decimal.normalize().as_tuple().digits

    def GetUnsignedScale(self, decimal: Decimal) -> UInt:
        return abs(decimal.as_tuple().exponent)

    def GetScale(self, decimal: Decimal) -> int:
        scale: UInt = self.GetUnsignedScale(decimal)
        if self.IgnoreTrailingZeros:
            return int(scale - self.NumTrailingZeros(decimal))

        return int(scale)

    def NumTrailingZeros(self, decimal: Decimal) -> UInt:
        trailingZeros: UInt = 0
        digits = decimal.as_tuple().digits

        for digit in digits[::-1]:
            if digit == 0:
                trailingZeros += 1
            else:
                break
        return trailingZeros

    def GetPrecision(self, decimal: Decimal) -> int:
        # Precision: number of times we can divide by 10 before we get to 0
        precision = len(decimal.as_tuple().digits)
        if self.IgnoreTrailingZeros:
            return int(precision - self.NumTrailingZeros(decimal))
        return int(precision)

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)
