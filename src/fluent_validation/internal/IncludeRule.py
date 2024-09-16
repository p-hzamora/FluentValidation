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
    def Create(validator: IValidator[T], cascadeModeThunk: Callable[[], CascadeMode]) -> IncludeRule[T]: ...
    @overload
    @staticmethod
    def Create[TValidator: IValidator[T]](validator: Callable[[T], TValidator], cascadeModeThunk: Callable[[], CascadeMode]) -> IncludeRule[T]: ...

    @staticmethod
    def Create[TValidator: IValidator[T]](validator: Callable[[T], TValidator], cascadeModeThunk: Callable[[], CascadeMode]) -> IncludeRule[T]:
        if callable(validator):
            return IncludeRule[T](lambda ctx, _: validator(ctx.instance_to_validate), cascadeModeThunk, type(T), type(TValidator))
        else:
            return IncludeRule[T](validator, cascadeModeThunk, type(T))

    @override
    async def ValidateAsync(self, context: ValidationContext[T], useAsync: bool):  # , CancellationToken cancellation
        # Special handling for the MemberName selector.
        # We need to disable the MemberName selector's cascade functionality whilst executing
        # an include rule, as an include rule should be have as if its children are actually children of the parent.
        # Also ensure that we only add/remove the state key if it's not present already.
        # If it is present already then we're in a situation where there are nested Include rules
        # in which case only the root Include rule should add/remove the key.
        # See https://github.com/FluentValidation/FluentValidation/issues/1989

        shouldAddStateKey: bool = MemberNameValidatorSelector.DisableCascadeKey not in context.RootContextData

        if shouldAddStateKey:
            context.RootContextData[MemberNameValidatorSelector.DisableCascadeKey] = True

        await super().ValidateAsync(context, useAsync)  # , cancellation

        if shouldAddStateKey:
            context.RootContextData.pop(MemberNameValidatorSelector.DisableCascadeKey)
