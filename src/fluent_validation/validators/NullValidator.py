from typing import override

from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.IpropertyValidator import IPropertyValidator
from fluent_validation.validators.PropertyValidator import PropertyValidator


class INullValidator(IPropertyValidator): ...


class NullValidator[T, TProperty](PropertyValidator[T, TProperty], INullValidator):
    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        return value is None

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)
