from typing import Callable
from ..IValidationContext import ValidationContext
from ..internal.IRuleComponent import IRuleComponent
from ..validators.IpropertyValidator import IPropertyValidator


class RuleComponent[T, TProperty](IRuleComponent):
    def __init__(self, property_validator: IPropertyValidator[T, TProperty]) -> None:
        self._property_validator: IPropertyValidator[T, TProperty] = property_validator
        self._error_message = property_validator.get_default_message_template(self.ErrorCode)
        self._errorMessageFactory: Callable[[ValidationContext], T] = None

    def __repr__(self) -> str:
        return f"<RuleComponent validator: {self.ErrorCode}>"

    @property
    def ErrorCode(self) -> str:
        return self._property_validator.__class__.__name__  # Nombre de la clase del validador

    @property
    def Validator(self) -> IPropertyValidator:
        return self._property_validator  # falta implementar => (IPropertyValidator) _propertyValidator ?? _asyncPropertyValidator;

    def set_error_message(self, error_message: str) -> None:
        self._error_message = error_message

    def invoke_property_validator(self, context: ValidationContext[T], value: TProperty) -> bool:
        return self.Validator.is_valid(context, value)

    def ValidateAsync(self, context: ValidationContext[T], value: TProperty) -> bool:
        return self.invoke_property_validator(context, value)

    def GetErrorMessage(self, context: ValidationContext[T], value: TProperty):
        # FIXME [ ]: self._error_message has value when it must by empty test "test_When_the_maxlength_validator_fails_the_error_message_should_be_set"
        rawTemplate: str = setattr(self._errorMessageFactory, value) if self._errorMessageFactory else self._error_message
        if rawTemplate is None:
            rawTemplate = self.Validator.get_default_message_template(self.ErrorCode)  # original

        if context is None:
            return rawTemplate

        return context.MessageFormatter.BuildMessage(rawTemplate)
