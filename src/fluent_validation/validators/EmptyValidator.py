from typing import Iterable, override

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.IValidationContext import ValidationContext


class EmptyValidator[T, TProperty](PropertyValidator[T, TProperty]):
    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        if value is None:
            return True

        if isinstance(value, str) and (value.isspace()):
            return True

        if isinstance(value, Iterable) and (self.IsEmpty(value)):
            return True

        return value == type(value)()

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)

    @staticmethod
    def IsEmpty(enumerable: Iterable) -> bool:
        enumerator = iter(enumerable)

        try:
            next(enumerator)
            return False
        except StopIteration:
            return True
