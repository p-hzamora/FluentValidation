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

from fluent_validation.validators.RangeValidator import IComparer
from fluent_validation.validators.ComparableComparer import IComparable
from person import _Address as Address


class StreetNumberComparer(IComparer[Address]):
    def TryParseStreetNumber(self, s: str) -> bool:
        try:
            streetNumberStr = s.split(" ")[0]
            return True, int(streetNumberStr)
        except ValueError:
            return False, None

    def GetValue(self, o: object) -> int:
        if isinstance(o, Address):
            boolean, streetNumber = self.TryParseStreetNumber(o.Line1)
            if boolean:
                return streetNumber
        raise ValueError("Can't convert", o)

    def Compare(self, x: Address, y: Address) -> int:
        if x == y:
            return 0
        if x is None:
            return -1
        if y is None:
            return 1
        return IComparable(self.GetValue(x)).CompareTo(self.GetValue(y))
