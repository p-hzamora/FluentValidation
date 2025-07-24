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

from typing import Callable, TYPE_CHECKING, Optional, Type, TypeVar, overload

from fluent_validation.enums import ApplyConditionTo
from fluent_validation.LambdaExpression import LambdaExpression

if TYPE_CHECKING:
    from fluent_validation.enums import CascadeMode as _CascadeMode
    from fluent_validation.IValidationContext import ValidationContext
    from .internal.IRuleComponent import IRuleComponent
    from .IValidationContext import IValidationContext
    from .internal.MessageBuilderContext import IMessageBuilderContext
    from .validators.IpropertyValidator import IPropertyValidator
    from fluent_validation.validators.IpropertyValidator import IAsyncPropertyValidator


class IValidatoinRule_no_args(ABC):
    @property
    @abstractmethod
    def Components(self) -> list[IRuleComponent]: ...

    @property
    @abstractmethod
    def RuleSets(self) -> set[str]: ...

    @RuleSets.setter
    @abstractmethod
    def RuleSets(self, value: set[str]) -> None: ...

    @abstractmethod
    def get_display_name(context: IValidationContext) -> str: ...

    @property
    @abstractmethod
    def PropertyName(self) -> str: ...

    @property
    @abstractmethod
    def TypeToValidate(self) -> Optional[Type]: ...

    @property
    @abstractmethod
    def HasCondition(self) -> bool: ...

    @property
    @abstractmethod
    def HasAsyncCondition(self) -> bool: ...

    @property
    @abstractmethod
    def Expression(self) -> LambdaExpression: ...

    @property
    @abstractmethod
    def dependent_rules(self) -> Optional[list[IValidationRule]]: ...


CancellationToken = TypeVar("CancellationToken")


class IValidationRule_one_arg[T](IValidatoinRule_no_args):
    ...

    @abstractmethod
    def ApplyCondition(self, predicate: Callable[[ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    # @abstractmethod
    # def ApplyAsyncCondition(self, predicate: Callable[[ValidationContext[T], CancellationToken], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators): ...

    @abstractmethod
    def ApplySharedCondition(self, condition: Callable[[ValidationContext[T]], bool]): ...

    # @abstractmethod
    # def ApplySharedAsyncCondition(self, condition: Callable[[ValidationContext[T], CancellationToken], bool]): ...


class IValidationRule[T, TProperty](IValidationRule_one_arg[T]):
    @overload
    def SetDisplayName(self, name: str) -> None: ...
    @overload
    def SetDisplayName(self, name: Callable[[ValidationContext[T]], str]) -> None: ...

    @abstractmethod
    def SetDisplayName(self, name: str | Callable[[ValidationContext[T]], str]) -> None: ...

    @property
    @abstractmethod
    def CascadeMode(self) -> _CascadeMode: ...

    @abstractmethod
    def AddValidator(self, validator: IPropertyValidator[T, TProperty]): ...

    @abstractmethod
    def AddAsyncValidator(self, asyncValidator: IAsyncPropertyValidator[T, TProperty], fallback: IPropertyValidator[T, TProperty] = None) -> None: ...

    @property
    @abstractmethod
    def Current(self) -> IRuleComponent: ...

    @property
    @abstractmethod
    def MessageBuilder(self) -> Callable[[IMessageBuilderContext[T, TProperty]], str]: ...  # {get; set;}

    @MessageBuilder.setter
    @abstractmethod
    def MessageBuilder(self, value: Callable[[IMessageBuilderContext[T, TProperty]], str]) -> None: ...

    if TYPE_CHECKING:

        def GetPropertyValue(self, prop_: T) -> TProperty: ...
