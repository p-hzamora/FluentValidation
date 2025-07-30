# region License
# Copyright (c) .NET Foundation and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# The latest version of this file can be found at https://github.com/p-hzamora/FluentValidation
# endregion

from __future__ import annotations
from typing import Any


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
