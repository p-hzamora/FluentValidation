from typing import Callable, Optional, overload

from src.fluent_validation.AsyncValidatorInvokedSynchronouslyException import AsyncValidatorInvokedSynchronouslyException
from ..IValidationContext import ValidationContext
from ..internal.IRuleComponent import IRuleComponent
from ..validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator


class RuleComponent[T, TProperty](IRuleComponent):
    @overload
    def __init__(self, property_validator: IPropertyValidator[T, TProperty]) -> None: ...
    @overload
    def __init__(self, asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty], propertyValidator: IPropertyValidator[T, TProperty]): ...

    def __init__(self, property_validator=None, asyncPropertyValidator=None) -> None:
        self._property_validator: IPropertyValidator[T, TProperty] = property_validator
        self._error_message: Optional[str] = None
        self._asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty] = asyncPropertyValidator
        self._errorMessageFactory: Callable[[ValidationContext], T] = None

        self._condition: Callable[[ValidationContext[T], bool]] = None

    def __repr__(self) -> str:
        return f"<RuleComponent validator: {self.ErrorCode}>"

    @property
    def ErrorCode(self) -> str:
        return self._property_validator.__class__.__name__  # Nombre de la clase del validador

    @property
    def Validator(self) -> IPropertyValidator:
        return self._property_validator  # falta implementar => (IPropertyValidator) _propertyValidator ?? _asyncPropertyValidator;

    @property
    def SupportsSynchronousValidation(self) -> bool:
        return self._property_validator is not None

    @property
    def SupportsAsynchronousValidation(self) -> bool:
        return self._asyncPropertyValidator is not None

    def set_error_message(self, error_message: str) -> None:
        self._error_message = error_message

    async def ValidateAsync(self, context: ValidationContext[T], value: TProperty, useAsync: bool) -> bool:
        if useAsync:
            # If ValidateAsync has been called on the root validator, then always prefer
            # the asynchronous property validator (if available).
            if self.SupportsAsynchronousValidation:
                return await self.InvokePropertyValidatorAsync(context, value)

            # If it doesn't support Async validation, then this means
            # the property validator is a Synchronous.
            # We don't need to explicitly check SupportsSynchronousValidation.
            return self.InvokePropertyValidator(context, value)

        # If Validate has been called on the root validator, then always prefer
        # the synchronous property validator.
        if self.SupportsSynchronousValidation:
            return self.InvokePropertyValidator(context, value)
        # Root Validator invoked synchronously, but the property validator
        # only supports asynchronous invocation.
        raise AsyncValidatorInvokedSynchronouslyException

    def InvokePropertyValidator(self, context: ValidationContext[T], value: TProperty) -> bool:
        return self._property_validator.is_valid(context, value)

    async def InvokePropertyValidatorAsync(self, context: ValidationContext[T], value: TProperty):
        return self._asyncPropertyValidator.IsValidAsync(context, value)

    def InvokeCondition(self, context: ValidationContext[T]) -> bool:
        if self._condition is not None:
            return self._condition(context)
        return True

    def GetErrorMessage(self, context: Optional[ValidationContext[T]], value: TProperty):
        # FIXME [x]: self._error_message has value when it must by empty test "test_When_the_maxlength_validator_fails_the_error_message_should_be_set"
        rawTemplate: Optional[str] = setattr(self._errorMessageFactory, value) if self._errorMessageFactory else self._error_message
        if rawTemplate is None:
            rawTemplate = self.Validator.get_default_message_template(self.ErrorCode)  # original

        if context is None:
            return rawTemplate

        return context.MessageFormatter.BuildMessage(rawTemplate)
