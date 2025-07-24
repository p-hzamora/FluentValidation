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

from typing import Optional
from fluent_validation.validators.RangeValidator import IComparer


class IComparable[T]:
    def __init__(self, value: T) -> None:
        self.value: T = value

    """
	Summary:
			Compares the current instance with another object of the same type and returns
			an integer that indicates whether the current instance precedes, follows, or
			occurs in the same position in the sort order as the other object.

	Parameters:
	other:
			An object to compare with this instance.

	Returns:
			A value that indicates the relative order of the objects being compared. The
			return value has these meanings:

			Value – Meaning
			Less than zero – This instance precedes other in the sort order.
			Zero – This instance occurs in the same position in the sort order as other.

			Greater than zero – This instance follows other in the sort order.
	"""

    def CompareTo(self, other: Optional[T]) -> int:
        if self.value < other:
            return -1
        elif self.value > other:
            return 1
        return 0


class ComparableComparer[T: IComparable[T]](IComparer[T]):
    @staticmethod
    def Compare(x: T, y: T) -> int:
        return IComparable(x).CompareTo(y)
