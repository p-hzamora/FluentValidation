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

from dataclasses import dataclass

import re
from typing import Callable, Optional, overload, override
from fluent_validation.IValidationContext import ValidationContext

from fluent_validation.validators.PropertyValidator import PropertyValidator


type _FlagsType = int | re.RegexFlag


class IRegularExpressionValidator[T]:
    _expression: str
    _regex_func: Callable[[T], re.Pattern]


@dataclass
class RegularExpressionValidator[T](PropertyValidator[T, str], IRegularExpressionValidator[T]):
    @overload
    def __init__(self, expression: str): ...
    @overload
    def __init__(self, expression: re.Pattern): ...
    @overload
    def __init__(self, expression: str, options: _FlagsType): ...
    @overload
    def __init__(self, expression: Callable[[T], str]): ...
    @overload
    def __init__(self, expression: Callable[[T], re.Pattern]): ...
    @overload
    def __init__(self, expression: Callable[[T], str], options: _FlagsType): ...

    def __init__(self, expression: str | re.Pattern, options: _FlagsType = re.NOFLAG):
        if isinstance(expression, str) and options == 0:
            self.__init__exp_str(expression)
        elif isinstance(expression, re.Pattern) and options == 0:
            self.__init__exp_re_pattern(expression)
        elif isinstance(expression, re.Pattern) and options != 0:
            self.__init__exp_re_pattern_options(expression, options)
        elif callable(expression):
            self.__init__with_callable_dynamic(expression, options)
        else:
            raise Exception("No se ha inicializado la variable correctamente")

    def __init__exp_str(self, expression: str):
        self._expression = expression
        self._regex_func = lambda x: self.CreateRegex(expression)

    def __init__exp_re_pattern(self, expression: re.Pattern):
        self._expression = str(expression)
        self._regex_func = lambda x: expression

    def __init__exp_re_pattern_options(self, expression: str, options: _FlagsType):
        self._expression = expression
        self._regex_func = lambda x: self.CreateRegex(expression, options)

    @override
    def is_valid(self, context: ValidationContext[T], value: str):
        if value is None:
            return True

        regex: re.Pattern = self._regex_func(context.instance_to_validate)

        if not regex.match(value):
            context.MessageFormatter.AppendArgument("RegularExpression", str(regex.pattern))
            return False
        return True

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)

    @staticmethod
    def CreateRegex(expression: str, RegexOptions: _FlagsType = re.NOFLAG) -> re.Pattern:
        return re.compile(expression, RegexOptions)

    def __init__with_callable_dynamic(self, expression: Callable[[T], str | re.Pattern], options: _FlagsType = re.NOFLAG):
        """
        Handles callable that returns either str or re.Pattern.
        Type discovery happens at runtime on first call.
        """
        self._expression = f"Dynamic: {expression.__name__ if hasattr(expression, '__name__') else 'lambda'}"
        self._cached_func: Optional[Callable[[T], re.Pattern]] = None
        self._original_callable = expression
        self._options = options

        def dynamic_regex_func(instance: T) -> re.Pattern:
            # Cache the resolved function after first call
            if self._cached_func is None:
                result = self._original_callable(instance)

                if isinstance(result, str):
                    # It returns string, so create a function that compiles it
                    self._cached_func = lambda x: self.CreateRegex(self._original_callable(x), self._options)
                elif isinstance(result, re.Pattern):
                    # It returns pattern, so use it directly (ignore options if provided)
                    if self._options != re.NOFLAG:
                        # If options were provided but we got a Pattern, we need to recompile
                        self._cached_func = lambda x: self.CreateRegex(self._original_callable(x).pattern, self._options)
                    else:
                        self._cached_func = self._original_callable
                else:
                    raise TypeError(f"Callable must return str or re.Pattern, got {type(result)}")

            return self._cached_func(instance)

        self._regex_func = dynamic_regex_func
