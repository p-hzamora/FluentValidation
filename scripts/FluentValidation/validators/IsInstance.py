from typing import Any
from IValidationContext import ValidationContext
from validators.PropertyValidator import PropertyValidator


class IsInstance[TProperty](PropertyValidator):
    def __init__(self, instance:TProperty):
        self._instance = instance


    def is_valid(self, context: ValidationContext, value:Any) -> bool:
        if not isinstance(value, self._instance):
            # context.MessageFormatter.AppendArgument(")
            return False
        return True
        