from __future__ import annotations
from typing import TYPE_CHECKING, Callable

from src.fluent_validation.IValidationContext import ValidationContext

if TYPE_CHECKING:
    from src.fluent_validation.IValidator import IValidator
    from src.fluent_validation.results.ValidationResult import ValidationResult
    from src.fluent_validation.internal.ValidationStrategy import ValidationStrategy


class DefaultValidatorExtensions_Validate:
    def validate[T](validator: IValidator[T], instance: T, options: Callable[[ValidationStrategy[T]], None]) -> ValidationResult:
        validator.validate(ValidationContext[T].CreateWithOptions(instance, options))

    # def Task<ValidationResult> ValidateAsync[T](this IValidator[T] validator, T instance, Action<ValidationStrategy[T]> options, CancellationToken cancellation = default)
    # 	=> validator.ValidateAsync(ValidationContext[T].CreateWithOptions(instance, options), cancellation)

    def validate_and_throw[T](validator: IValidator[T], instance: T) -> None:
        validator.validate(instance, lambda options: options.ThrowOnFailures())

    # async def Task ValidateAndThrowAsync[T](this IValidator[T] validator, T instance, CancellationToken cancellationToken = default) {
    # 	await validator.ValidateAsync(instance, options => {
    # 		options.ThrowOnFailures()
    # 	}, cancellationToken)
