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

from .ExclusiveBetweenValidator import IBetweenValidator
from .RangeValidator import IComparer, RangeValidator


class IInclusiveBetweenValidator(IBetweenValidator): ...


class InclusiveBetweenValidator[T, TProperty](RangeValidator[T, TProperty], IInclusiveBetweenValidator):
    """Performs range validation where the property value must be between the two specified values (inclusive)."""

    def __init__(self, from_: TProperty, to: TProperty, comparer: IComparer[T]):  # comparer:IComparer[TProperty]
        super().__init__(from_, to, comparer)

    def HasError(self, value: TProperty) -> bool:
        return self.Compare(value, self.From) < 0 or self.Compare(value, self.To) > 0
