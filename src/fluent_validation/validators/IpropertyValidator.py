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
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext


class IPropertyValidator_no_generic(ABC):
    @property
    @abstractmethod
    def Name(self) -> str: ...

    @abstractmethod
    def get_default_message_template(self, error_code: str) -> str: ...


class IPropertyValidator[T, TProperty](IPropertyValidator_no_generic):
    @abstractmethod
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool: ...


class IAsyncPropertyValidator[T, TProperty](IPropertyValidator_no_generic):
    @abstractmethod
    async def IsValidAsync(self, context: ValidationContext[T], value: TProperty) -> bool: ...
