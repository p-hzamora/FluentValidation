from typing import override
from src.fluent_validation.IValidationContext import ValidationContext
from src.fluent_validation.validators.PropertyValidator import PropertyValidator


class NoopPropertyValidator[T, TProperty](PropertyValidator[T, TProperty]):
    @override
    def is_valid(context: ValidationContext[T], value: TProperty) -> bool:
        return True
