import re
from typing import Any


class MessageFormatter:
    _placeholderValues: dict[str, object] = {}
    _keyRegex: re.Pattern = re.compile(r"{([^{}:]+)(?::([^{}]+))?}")
    PropertyName = "PropertyName"
    PropertyValue = "PropertyValue"

    def __repr__(self) -> str:
        return f"{MessageFormatter.__name__}"

    def AppendArgument(self, name: str, value: object):
        self._placeholderValues[name] = value
        return self

    def AppendPropertyName(self, name: str):
        return self.AppendArgument(self.PropertyName, name)

    def AppendPropertyValue(self, value: object):
        return self.AppendArgument(self.PropertyValue, value)

    def BuildMessage(self, messageTemplate: str) -> str:
        return self.replace_placeholders(messageTemplate, self.PlaceholderValues)

    def replace_placeholders(self, message_template: str, placeholder_values: dict[str, Any]):
        def replace(match: re.Match) -> str:
            key = match.group(1)

            if key not in placeholder_values:
                return match.group(0)  # No placeholder / value

            value = placeholder_values[key]
            if match.group(2):  # Format specified?
                return f"{value:{match.group(2)}}"
            else:
                return str(value)

        return self._keyRegex.sub(replace, message_template)

    @property
    def PlaceholderValues(self) -> dict[str, object]:
        return self._placeholderValues

    def Reset(self) -> None:
        self._placeholderValues.clear()
