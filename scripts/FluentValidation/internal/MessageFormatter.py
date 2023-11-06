import re

class MessageFormatter():
	_placeholderValues:dict[str,object] = {}
	_keyRegex:re.Pattern = re.compile("{([^{}:]+)(?::([^{}]+))?}")
	PropertyName = "PropertyName"
	PropertyValue = "PropertyValue"

	def AppendArgument(self, name:str, value:object):
		self._placeholderValues[name] = value
		return self


	def AppendPropertyName(self, name:str):
		return self.AppendArgument(self.PropertyName, name)


	def AppendPropertyValue(self, value:object):
		return self.AppendArgument(self.PropertyValue, value)
	

	def BuildMessage(self, messageTemplate:str)->str:
		return messageTemplate
	# 	return self._keyRegex.sub(messageTemplate, m =>	{
	# 		var key = m.Groups[1].Value;

	# 		if (!_placeholderValues.TryGetValue(key, out var value))
	# 			return m.Value; // No placeholder / value

	# 		var format = m.Groups[2].Success // Format specified?
	# 			? $"{{0:{m.Groups[2].Value}}}"
	# 			: null;

	# 		return format == null
	# 			? value?.ToString()
	# 			: str.Format(format, value);
	# 	});
	# }

	@property
	def PlaceholderValues(self)->dict[str,object]: return self._placeholderValues

	def Reset(self)->None:
		self._placeholderValues.clear()