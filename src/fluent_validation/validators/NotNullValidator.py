from typing import override
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.validators.IpropertyValidator import IPropertyValidator

class INotNullValidator(IPropertyValidator): ...



class NotNullValidator[T, TProperty](PropertyValidator[T, TProperty], INotNullValidator ):
    @override
    def is_valid(self, _: ValidationContext, value: TProperty) -> bool:
        return value is not None

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
