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

from typing import Iterable, override

from fluent_validation.validators.PropertyValidator import PropertyValidator
from fluent_validation.IValidationContext import ValidationContext


class EmptyValidator[T, TProperty](PropertyValidator[T, TProperty]):
    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        if value is None:
            return True

        if isinstance(value, str) and (value.isspace()):
            return True

        if isinstance(value, Iterable) and (self.IsEmpty(value)):
            return True

        return value == type(value)()

    @override
    def get_default_message_template(self, errorCode: str) -> str:
        return self.Localized(errorCode, self.Name)

    @staticmethod
    def IsEmpty(enumerable: Iterable) -> bool:
        enumerator = iter(enumerable)

        try:
            next(enumerator)
            return False
        except StopIteration:
            return True
