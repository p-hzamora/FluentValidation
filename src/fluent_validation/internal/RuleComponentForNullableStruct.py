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
from typing import TYPE_CHECKING, Optional, override

from fluent_validation.internal.RuleComponent import RuleComponent

if TYPE_CHECKING:
    from fluent_validation.IValidationContext import ValidationContext
    from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator, IPropertyValidator


class RuleComponentForNullableStruct[T, TProperty](RuleComponent[T, Optional[TProperty]]):
    __slots__ = (
        "_propertyValidator",
        "_asyncPropertyValidator",
    )

    _propertyValidator: IPropertyValidator[T, TProperty]
    _asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty]

    def __init__(self, propertyValidator: IPropertyValidator[T, TProperty] = None, _asyncPropertyValidator: IAsyncPropertyValidator[T, TProperty] = None) -> None:
        super().__init__(None)
        self._propertyValidator: Optional[IPropertyValidator[T, TProperty]] = propertyValidator
        self._asyncPropertyValidator: Optional[IAsyncPropertyValidator[T, TProperty]] = _asyncPropertyValidator

    @override
    @property
    def Validator(self) -> IPropertyValidator | IAsyncPropertyValidator:
        return self._propertyValidator or self._asyncPropertyValidator

    @override
    @property
    def SupportsAsynchronousValidation(self) -> bool:
        return self._asyncPropertyValidator is not None

    @override
    @property
    def SupportsSynchronousValidation(self) -> bool:
        return self._propertyValidator is not None

    @override
    def InvokePropertyValidator(self, context: ValidationContext[T], value: Optional[TProperty]) -> bool:
        if value is None:
            return True
        return self._propertyValidator.is_valid(context, value)

    @override
    async def InvokePropertyValidatorAsync(self, context: ValidationContext[T], value: Optional[TProperty]) -> bool:
        if value is None:
            return True
        return await self._asyncPropertyValidator.IsValidAsync(context, value)
