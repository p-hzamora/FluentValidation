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

from typing import Callable, overload, override
from fluent_validation.validators.AbstractComparisonValidator import (
    AbstractComparisonValidator,
    Comparison,
)


class GreaterThanValidator[T, TProperty](AbstractComparisonValidator[T, TProperty]):
    @overload
    def __init__(self, value: TProperty): ...

    @overload
    def __init__(self, valueToCompareFunc: Callable[[T], TProperty], memberDisplayName: str): ...

    @overload
    def __init__(
        self,
        valueToCompareFunc: Callable[[T], tuple[bool, TProperty]],
        memberDisplayName: str,
    ): ...

    def __init__(self, value=None, valueToCompareFunc=None, memberDisplayName=None):
        super().__init__(
            valueToCompareFunc=valueToCompareFunc,
            memberDisplayName=memberDisplayName,
            value=value,
        )

    @override
    @property
    def Comparison(self) -> Comparison:
        return Comparison.greater_than

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
