from typing import Callable, override

from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator
from .IpropertyValidator import IPropertyValidator

# 	public delegate bool Predicate(T instanceToValidate, TProperty propertyValue, ValidationContext<T> propertyValidatorContext);


class IPredicateValidator(IPropertyValidator):
    pass


class PredicateValidator[T, TProperty](PropertyValidator[T, TProperty], IPredicateValidator):
    def __init__(self, predicate: Callable[[T, TProperty, ValidationContext[T]], bool]):
        self._predicate: Callable[[T, TProperty, ValidationContext[T]], bool] = predicate

    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        if not self._predicate(context.instance_to_validate, value, context):
            return False
        return True

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
