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
from abc import ABC

from typing import Callable, Type, overload, override
from fluent_validation import CascadeMode, ValidationContext
from fluent_validation.internal.PropertyRule import PropertyRule
from fluent_validation.IValidator import IValidator
from fluent_validation.validators.ChildValidatorAdaptor import ChildValidatorAdaptor
from fluent_validation.internal.MemberNameValidatorSelector import MemberNameValidatorSelector


class IIncludeRule(ABC): ...


class IncludeRule[T](PropertyRule[T, T], IIncludeRule):
    @overload
    def __init__(self, validator: IValidator[T], cascadeModeThunk: Callable[[], CascadeMode], typeToValidate: Type): ...
    @overload
    def __init__(self, validator: Callable[[ValidationContext[T], T], IValidator[T]], cascadeModeThunk: Callable[[], CascadeMode], typeToValidate: Type, validatorType: Type): ...

    def __init__(self, validator: Callable[[ValidationContext[T], T], IValidator[T]], cascadeModeThunk: Callable[[], CascadeMode], typeToValidate: Type, validatorType: None | Type = None):
        if callable(validator):
            super().__init__(None, lambda x: x, None, cascadeModeThunk, typeToValidate)
            adaptor = ChildValidatorAdaptor[T, T](validator, validatorType)
            # Note: ChildValidatorAdaptor implements both IPropertyValidator and IAsyncPropertyValidator
            # So calling AddAsyncValidator will actually register it as supporting both sync and async.
            self.AddAsyncValidator(adaptor, adaptor)
        else:
            super().__init__(None, lambda x: x, None, cascadeModeThunk, typeToValidate)
            adaptor = ChildValidatorAdaptor[T, T](validator, type(validator))
            # Note: ChildValidatorAdaptor implements both IPropertyValidator and IAsyncPropertyValidator
            # So calling AddAsyncValidator will actually register it as supporting both sync and async.
            self.AddAsyncValidator(adaptor, adaptor)

    @overload
    @staticmethod
    def Create(validator: IValidator[T], cascadeModeThunk: Callable[[], CascadeMode], type_model: T) -> IncludeRule[T]: ...
    @overload
    @staticmethod
    def Create[TValidator: IValidator[T]](validator: Callable[[T], TValidator], cascadeModeThunk: Callable[[], CascadeMode], type_model: T) -> IncludeRule[T]: ...

    @staticmethod
    def Create[TValidator: IValidator[T]](validator: Callable[[T], TValidator], cascadeModeThunk: Callable[[], CascadeMode], type_model: T) -> IncludeRule[T]:
        if callable(validator):
            return IncludeRule[T](lambda ctx, _: validator(ctx.instance_to_validate), cascadeModeThunk, type_model, type(TValidator))
        else:
            return IncludeRule[T](validator, cascadeModeThunk, type_model)

    @override
    async def ValidateAsync(self, context: ValidationContext[T], useAsync: bool):  # , CancellationToken cancellation
        # Special handling for the MemberName selector.
        # We need to disable the MemberName selector's cascade functionality whilst executing
        # an include rule, as an include rule should be have as if its children are actually children of the parent.
        # Also ensure that we only add/remove the state key if it's not present already.
        # If it is present already then we're in a situation where there are nested include rules
        # in which case only the root include rule should add/remove the key.
        # See https://github.com/p-hzamora/FluentValidation/issues/1989

        shouldAddStateKey: bool = MemberNameValidatorSelector.DisableCascadeKey not in context.RootContextData

        if shouldAddStateKey:
            context.RootContextData[MemberNameValidatorSelector.DisableCascadeKey] = True

        await super().ValidateAsync(context, useAsync)  # , cancellation

        if shouldAddStateKey:
            context.RootContextData.pop(MemberNameValidatorSelector.DisableCascadeKey)

    def ValidateSync(self, context: ValidationContext[T]) -> None:
        """Synchronous version of ValidateAsync to avoid event loop deadlocks."""
        shouldAddStateKey: bool = MemberNameValidatorSelector.DisableCascadeKey not in context.RootContextData

        if shouldAddStateKey:
            context.RootContextData[MemberNameValidatorSelector.DisableCascadeKey] = True

        super().ValidateSync(context)

        if shouldAddStateKey:
            context.RootContextData.pop(MemberNameValidatorSelector.DisableCascadeKey)
