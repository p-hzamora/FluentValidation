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

import inspect
import re
from typing import Any, Callable


class LambdaExpression:
    REGEX: re.Pattern = re.compile(r"lambda[^)]*?")

    def __init__(self, func: Callable[..., Any]) -> None:
        self._lambda: Callable[..., Any] = func

    @property
    def func(self) -> Callable[..., Any]:
        return self._lambda

    @property
    def lambda_to_string(self) -> str:
        get_source = inspect.getsource(self._lambda).strip()

        return self.get_real_lambda_from_source_code(get_source)

    @staticmethod
    def get_real_lambda_from_source_code(chain: str):
        chain = re.search(r"lambda.+", chain).group()
        n = len(chain)
        open_parenthesis: list[int] = [0] * n
        result: str = ""

        for i in range(n):
            char = chain[i]

            if char == "(":
                open_parenthesis[i] = 1

            if char == ")":
                open_parenthesis[i] = -1

            if sum(open_parenthesis) < 0:
                break

            result += char

        return result
