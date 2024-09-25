from enum import Enum, Flag
from typing import Any, Type, override
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator


class EnumValidator[T, TProperty: Enum](PropertyValidator[T, TProperty]):
    def __init__(self, enumType: Type[TProperty]) -> None:
        super().__init__()
        self._enumType: Type[TProperty] = enumType

    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        if value is None:
            return True

        if not issubclass(self._enumType, Enum):
            return False

        if isinstance(self._enumType, Flag):
            return self.IsFlagsEnumDefined(value)
        return value in self._enumType

    def IsFlagsEnumDefined(self, enum: Any | TProperty) -> bool:
        if isinstance(enum, int):
            return self.EvaluateFlagEnumValues(enum, self._enumType)
        raise TypeError(f"Unexpected type of '{type(enum).__name__}' during flags enum evaluation.")

    @staticmethod
    def EvaluateFlagEnumValues(value: int, enumType: Type[Enum]):
        mask: int = 0
        for enumValue in enumType:
            enum_as_int: int = enumValue.value
            if (enum_as_int & value) == enum_as_int:
                mask |= enum_as_int
                if mask == value:
                    return True
        return False

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)
