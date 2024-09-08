from __future__ import annotations
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .Resources.ILanguageManager import ILanguageManager


class ExtensionsInternal:
    @staticmethod
    def Guard(obj: Any, message: str, paramName: str):
        if obj is None:
            raise AttributeError(message, name=paramName)

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

    @staticmethod
    def split_pascal_case(input_str: str) -> str:
        if input_str is None or input_str.isspace():
            return input_str

        retVal = []
        for i in range(len(input_str)):
            current_char = input_str[i]
            if current_char.isupper():
                if (i > 1 and not input_str[i - 1].isupper()) or (i + 1 < len(input_str) and not input_str[i + 1].isupper()):
                    retVal.append(" ")

            if not current_char == "." or i + 1 == len(input_str) or not input_str[i + 1].isupper():
                retVal.append(current_char)

        return "".join(retVal).strip()

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
    def ResolveErrorMessageUsingErrorCode(error_code: str, fall_back_Key: str) -> str:
        from .Resources.LanguageManager import LanguageManager  # FIXME [ ]: I don't know how to avoid this import to prevent circular imports

        languageManager: ILanguageManager = LanguageManager()
        if error_code is not None:
            result: str = languageManager.GetString(error_code)

            if result is not None and not result.isspace():
                return result
        return languageManager.GetString(fall_back_Key)
