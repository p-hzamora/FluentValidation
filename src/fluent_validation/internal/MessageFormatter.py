import re


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
        return self.replace_placeholders(messageTemplate)

    def replace_placeholders(self, message_template: str):
        def replace(match: re.Match[str]) -> str:
            key = match.group(1)

            if key not in self._placeholderValues:
                return match.group(0)  # No placeholder / value

            value = self._placeholderValues.get(key)

            format = match.group(2)
            if format is None:
                return str(value) if value is not None else None
            format_string = f"{{0:{format}}}"
            return format_string.format(value)  # Format specified?

        return self._keyRegex.sub(replace, message_template)

    @property
    def PlaceholderValues(self) -> dict[str, object]:
        return self._placeholderValues

    def Reset(self) -> None:
        self._placeholderValues.clear()
