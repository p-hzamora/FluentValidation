from abc import abstractmethod

from ..IValidationContext import ValidationContext
from ..validators.IpropertyValidator import IPropertyValidator
from ..ValidatorOptions import ValidatorOptions


class PropertyValidator[T, TProperty](IPropertyValidator[T, TProperty]):
    @property
    def Name(self):
        return self.__class__.__name__

    def get_default_message_template(self, error_code: str) -> str:
        return "No default error message has been specified"

    @abstractmethod
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool: ...

    def Localized(self, error_code: str, fall_back_Key: str):
        return ValidatorOptions.Global.LanguageManager.ResolveErrorMessageUsingErrorCode(error_code, fall_back_Key)
