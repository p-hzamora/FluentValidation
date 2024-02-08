from typing import Any, override
from ..IValidationContext import ValidationContext
from ..validators.PropertyValidator import PropertyValidator


class IsInstance[TProperty](PropertyValidator):
    def __init__(self, instance: TProperty):
        self._instance = instance

    @override
    def is_valid(self, context: ValidationContext, value: Any) -> bool:
        if value is None:
            return True

        if not isinstance(value, self._instance):
            context.MessageFormatter.AppendArgument("Current value:", type(value))
            context.MessageFormatter.AppendArgument("Expected value:", self._instance)
            return False
        return True

    @override
    def get_default_message_template(self) -> str:
        return f"IsInstance failed. Value is not '{self._instance}'"
        