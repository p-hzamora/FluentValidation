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
