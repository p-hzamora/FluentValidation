from typing import override, Iterable
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.validators.IpropertyValidator import IPropertyValidator


class INotEmptyValidator(IPropertyValidator): ...


class NotEmptyValidator[T, TProperty](PropertyValidator, INotEmptyValidator):
    @override
    def is_valid(self, _: ValidationContext[T], value: TProperty):
        if value is None:
            return False

        if isinstance(value, str):
            return not value.isspace() and value != ""

        if isinstance(value, Iterable):
            return len(value) > 0

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
