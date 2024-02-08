

class ExtensionsInternal:
	# @staticmethod
    # def Guard(this object obj, string message, string paramName) {
	# 	if (obj == null) {
	# 		throw new ArgumentNullException(paramName, message);
	# 	}
	# }

	# @staticmethod
    # def Guard(this string str, string message, string paramName) {
	# 	if (str == null) {
	# 		throw new ArgumentNullException(paramName, message);
	# 	}

	# 	if (string.IsNullOrEmpty(str)) {
	# 		throw new ArgumentException(message, paramName);
	# 	}
	# }

	# @staticmethod
    # bool IsParameterExpression(this LambdaExpression expression) {
	# 	return expression.Body.NodeType == ExpressionType.Parameter;
	# }

	# @staticmethod
    # string SplitPascalCase(this string input) {
	# 	if (string.IsNullOrEmpty(input))
	# 		return input;

	# 	var retVal = new StringBuilder(input.Length + 5);

	# 	for (int i = 0; i < input.Length; ++i) {
	# 		var currentChar = input[i];
	# 		if (char.IsUpper(currentChar)) {
	# 			if ((i > 1 && !char.IsUpper(input[i - 1]))
	# 			    || (i + 1 < input.Length && !char.IsUpper(input[i + 1])))
	# 				retVal.Append(' ');
	# 		}

	# 		if(!char.Equals('.', currentChar)
	# 		   || i + 1 == input.Length
	# 		   || !char.IsUpper(input[i + 1])) {
	# 			retVal.Append(currentChar);
	# 		}
	# 	}

	# 	return retVal.ToString().Trim();
	# }

	# @staticmethod
    # T GetOrAdd<T>(this IDictionary<string, object> dict, string key, Func<T> value) {
	# 	if (dict.TryGetValue(key, out var tmp)) {
	# 		if (tmp is T result) {
	# 			return result;
	# 		}
	# 	}

	# 	var val = value();
	# 	dict[key] = val;
	# 	return val;
	# }

	@staticmethod
	def ResolveErrorMessageUsingErrorCode(error_code:str, fall_back_Key:str)->str:
		from .Resources.ILanguageManager import ILanguageManager  #FIXME [ ]: I don't know how to avoid this import to prevent circular imports
		from .Resources.LanguageManager import LanguageManager  #FIXME [ ]: I don't know how to avoid this import to prevent circular imports

		languageManager:ILanguageManager = LanguageManager()
		if error_code is not None:
			result:str = languageManager.GetString(error_code)

			if not result.isspace() and result is not None:
				return result
		return languageManager.GetString(fall_back_Key)
