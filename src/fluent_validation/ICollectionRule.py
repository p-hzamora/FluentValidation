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
from abc import abstractmethod
from typing import Callable

from fluent_validation.IValidationRule import IValidationRule


class ICollectionRule[T, TElement](IValidationRule[T, TElement]):
    """
    Represents a rule defined against a collection with rule_for_each.
    : T -> Root object
    : TElement -> Type of each element in the collection
    """

    @property
    @abstractmethod
    def Filter(self) -> Callable[[TElement], bool]:
        """
        Filter that should include/exclude items in the collection.
        """

    @property
    @abstractmethod
    def IndexBuilder(self) -> Callable[[T, list[TElement], TElement, int], str]:
        """
        Constructs the indexer in the property name associated with the error message.
        By default this is "[" + index + "]"
        """
