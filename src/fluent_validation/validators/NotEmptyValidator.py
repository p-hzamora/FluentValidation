import datetime
from typing import override, Iterable
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.validators.IpropertyValidator import IPropertyValidator


def is_not_default(value):
    if isinstance(value, int | float):
        return value != 0

    if isinstance(value, datetime.datetime):
        # We assume that a minimun datetime means that the data is not valid, that is, it's empty
        return value != datetime.datetime.min
    return value is not None


class INotEmptyValidator(IPropertyValidator): ...


class NotEmptyValidator[T, TProperty](PropertyValidator, INotEmptyValidator):
    @override
    def is_valid(self, _: ValidationContext[T], value: TProperty):
        if value is None:
            return False

        if isinstance(value, str) and value.strip() == "":
            return False

        if isinstance(value, Iterable):
            if hasattr(value, "__len__"):
                return len(value) > 0

            if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
                try:
                    iterator = iter(value)
                    if next(iterator, None) is None:
                        return False
                    pass
                except StopIteration:
                    return False

        # For primitive types, check against their default value
        # Python does not have a generic default
        return is_not_default(value)

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
