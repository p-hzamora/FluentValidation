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

from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.validators.PropertyValidator import PropertyValidator
from .IpropertyValidator import IPropertyValidator

# 	public delegate bool Predicate(T instanceToValidate, TProperty propertyValue, ValidationContext<T> propertyValidatorContext);


class IPredicateValidator(IPropertyValidator):
    pass


class PredicateValidator[T, TProperty](PropertyValidator[T, TProperty], IPredicateValidator):
    def __init__(self, predicate: Callable[[T, TProperty, ValidationContext[T]], bool]):
        self._predicate: Callable[[T, TProperty, ValidationContext[T]], bool] = predicate

    @override
    def is_valid(self, context: ValidationContext[T], value: TProperty) -> bool:
        if not self._predicate(context.instance_to_validate, value, context):
            return False
        return True

    @override
    def get_default_message_template(self, error_code: str) -> str:
        return self.Localized(error_code, self.Name)
