# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

from typing import Any, Callable, Optional, overload

from fluent_validation.AsyncValidatorInvokedSynchronouslyException import AsyncValidatorInvokedSynchronouslyException
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.internal.IRuleComponent import IRuleComponent
from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator


class RuleComponent[T, TProperty](IRuleComponent):
    __slots__ = (
        "_property_validator",
        "_error_message",
        "_error_code",
        "_asyncPropertyValidator",
        "_errorMessageFactory",
        "_condition",
        "_CustomStateProvider",
        "_SeverityProvider",
        "_asyncCondition",
    )

    @overload
    def __init__(self, property_validator: IPropertyValidator[T, TProperty]) -> None: ...
    @overload
    def __init__(self, asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty], propertyValidator: IPropertyValidator[T, TProperty]): ...

    def __init__(self, property_validator=None, asyncPropertyValidator=None) -> None:
        self._property_validator: IPropertyValidator[T, TProperty] = property_validator
        self._error_message: Optional[str] = None
        self._error_code: str = None
        self._asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty] = asyncPropertyValidator
        self._errorMessageFactory: Callable[[ValidationContext], T] = None

        self._condition: Callable[[ValidationContext[T], bool]] = None

        self._CustomStateProvider: Callable[[ValidationContext[T], TProperty], Any] = None
        self._SeverityProvider: Callable[[ValidationContext[T]], TProperty] = None

    def __repr__(self) -> str:
        return f"<RuleComponent validator: {self.ErrorCode}>"

    @property
    def HasCondition(self) -> bool:
        return self._condition is not None

    @property
    def HasAsyncCondition(self) -> bool:
        # TODOL: Checked
        return False
        # return self._asyncCondition is not None

    @property
    def Validator(self) -> IPropertyValidator:
        return self._property_validator  # needs to be implemented => (IPropertyValidator) _propertyValidator ?? _asyncPropertyValidator

    @property
    def SupportsSynchronousValidation(self) -> bool:
        return self._property_validator is not None

    @property
    def SupportsAsynchronousValidation(self) -> bool:
        return self._asyncPropertyValidator is not None

    @overload
    def set_error_message(self, error_message: Callable[[ValidationContext[T], TProperty], str]) -> None: ...
    @overload
    def set_error_message(self, error_message: str) -> None: ...

    def set_error_message(self, error_message: Callable[[ValidationContext[T], TProperty], str] | str) -> None:
        if isinstance(error_message, str):
            self._error_message = error_message
            self._errorMessageFactory = None
        elif callable(error_message):
            self._error_message = None
            self._errorMessageFactory = error_message

        else:
            raise ValueError("error_message does not expected in 'set_error_message'")

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

    def ValidateSync(self, context: ValidationContext[T], value: TProperty) -> bool:
        """Synchronous version of ValidateAsync to avoid event loop issues."""
        if self.SupportsSynchronousValidation:
            return self.InvokePropertyValidator(context, value)
        # Root Validator invoked synchronously, but the property validator
        # only supports asynchronous invocation.
        raise AsyncValidatorInvokedSynchronouslyException

    def ApplyCondition(self, condition: Callable[[ValidationContext[T]], bool]) -> None:
        if self._condition is None:
            self._condition = condition
        else:
            original = self._condition
            self._condition = lambda ctx: condition(ctx) and original(ctx)

    def InvokeCondition(self, context: ValidationContext[T]) -> bool:
        if self._condition is not None:
            return self._condition(context)
        return True

    # internal async Task<bool> InvokeAsyncCondition(ValidationContext<T> context, CancellationToken token) {
    # 	if (_asyncCondition != null) {
    # 		return await _asyncCondition(context, token);
    # 	}

    # 	return true;
    # }

    @property
    def CustomStateProvider(self) -> Callable[[ValidationContext[T], TProperty], Any]:
        """Function used to retrieve custom state for the validator"""
        return self._CustomStateProvider

    @CustomStateProvider.setter
    def CustomStateProvider(self, value: Callable[[ValidationContext[T], TProperty], Any]) -> None:
        self._CustomStateProvider = value

    @property
    def SeverityProvider(self) -> Callable[[ValidationContext[T]], TProperty]:
        """Function used to retrieve the severity for the validator"""
        return self._SeverityProvider

    @SeverityProvider.setter
    def SeverityProvider(self, value: Callable[[ValidationContext[T]], TProperty]) -> None:
        self._SeverityProvider = value

    @property
    def ErrorCode(self) -> str:
        """Retrieves the error code."""
        return self._error_code

    @ErrorCode.setter
    def ErrorCode(self, value: str) -> None:
        self._error_code = value

    def GetErrorMessage(self, context: Optional[ValidationContext[T]], value: TProperty):
        # FIXME [x]: self._error_message has value when it must by empty test "test_When_the_maxlength_validator_fails_the_error_message_should_be_set"
        rawTemplate: Optional[str] = self._errorMessageFactory(context, value) if self._errorMessageFactory else self._error_message
        if rawTemplate is None:
            rawTemplate = self.Validator.get_default_message_template(self.ErrorCode)  # original

        if context is None:
            return rawTemplate

        return context.MessageFormatter.BuildMessage(rawTemplate)

    def GetUnformattedErrorMessage(self) -> str:
        message: str = self._errorMessageFactory(None, None) if self._errorMessageFactory is not None else self._error_message

        # If no custom message has been supplied, use the default.
        if message is None:
            message = self.Validator.get_default_message_template(self.ErrorCode)
        return message


# 	/// <summary>
# 	/// Sets the overridden error message template for this validator.
# 	/// </summary>
# 	/// <param name="errorFactory">A function for retrieving the error message template.</param>
# 	public void SetErrorMessage(Func<ValidationContext<T>, TProperty, string> errorFactory) {
# 		_errorMessageFactory = errorFactory;
# 		_errorMessage = null;
# 	}

# 	/// <summary>
# 	/// Sets the overridden error message template for this validator.
# 	/// </summary>
# 	/// <param name="errorMessage">The error message to set</param>
# 	public void SetErrorMessage(string errorMessage) {
# 		_errorMessage = errorMessage;
# 		_errorMessageFactory = null;
# 	}
# }
