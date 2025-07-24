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

from typing import Callable, override

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.validators.AbstractComparisonValidator import Comparison

from .EqualValidator import EqualValidator, IEqualityComparer


class NotEqualValidator[T, TProperty](EqualValidator[T, TProperty]):
    def __init__(
        self,
        valueToCompare: TProperty = None,
        comparer: IEqualityComparer[TProperty] = None,
        comparisonProperty: Callable[[T], TProperty] = None,
        member: MemberInfo = None,
        memberDisplayName: str = None,
    ):
        super().__init__(
            valueToCompare,
            comparer,
            comparisonProperty,
            member,
            memberDisplayName,
        )

    @override
    @property
    def Comparison(self) -> Comparison:
        return Comparison.not_equal

    def Compare(self, comparisonValue: TProperty, propertyValue: TProperty) -> bool:
        return not super().Compare(comparisonValue, propertyValue)
