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
from typing import Any, Callable, Self, TYPE_CHECKING, Type

from fluent_validation.MemberInfo import MemberInfo
from fluent_validation.internal.AccessorCache import AccessorCache

from fluent_validation.enums import CascadeMode
from fluent_validation.internal.RuleBase import RuleBase
from fluent_validation.internal.RuleComponent import RuleComponent

if TYPE_CHECKING:
    from fluent_validation.IValidationRuleInternal import IValidationRuleInternal
    from fluent_validation.internal.TrackingCollection import IEnumerable
    from fluent_validation.validators.IpropertyValidator import IPropertyValidator
    from fluent_validation.IValidationContext import ValidationContext


class PropertyRule[T, TProperty](RuleBase[T, TProperty, TProperty]):
    def __init__(
        self,
        member: MemberInfo,
        propertyFunc: Callable[[T], TProperty],
        expression: Callable[..., Any],
        cascadeModeThunk: Callable[[], CascadeMode],
        typeToValidate: Type,
    ) -> None:
        super().__init__(member, propertyFunc, expression, cascadeModeThunk, typeToValidate)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} from '{self.PropertyName}' at {hex(id(self))}>"

    @classmethod
    def create(cls, expression: Callable[[T], TProperty], cascadeModeThunk: Callable[[], CascadeMode], type_model: Type[T], bypassCache: bool = False) -> Self:
        member = MemberInfo(expression, type_model)
        compiled = AccessorCache[T].GetCachedAccessor(member, expression, bypassCache)

        t_property: Type[TProperty] = member.get_type_hint(type_model)
        return PropertyRule[T, TProperty](member, lambda x: compiled(x), expression, cascadeModeThunk, t_property)

    def AddValidator(self, validator: IPropertyValidator[T, TProperty]) -> None:
        component: RuleComponent = RuleComponent[T, TProperty](validator)
        self._components.append(component)
        return None

    async def ValidateAsync(self, context: ValidationContext[T], useAsync: bool) -> None:
        displayName: None | str = self.get_display_name(context)

        if self.PropertyName is None and displayName is None:
            displayName = ""

        PropertyPath: str = context.PropertyChain.BuildPropertyPath(displayName if not self.PropertyName else self.PropertyName)
        if not context.Selector.CanExecute(self, PropertyPath, context):
            return None

        if self.Condition:
            if not self.Condition(context):
                return None

        # if (AsyncCondition != null) {
        #     if (useAsync) {
        #         if (!await AsyncCondition(context, cancellation)) {
        #             return;
        #         }
        #     }
        #     else {
        #         throw new AsyncValidatorInvokedSynchronouslyException();
        #     }
        # }

        first = True
        propValue = None
        cascade = self.CascadeMode
        total_failures = len(context.Failures)

        context.InitializeForPropertyValidator(PropertyPath, self._displayNameFunc, self.PropertyName)

        for component in self.Components:
            context.MessageFormatter.Reset()

            if not component.InvokeCondition(context):
                continue

            # if component.HasAsyncCondition:
            #     if useAsync:
            #         if await component.invokeAsyncCondition(context,cancellation):
            #             continue
            #         else:
            #             raise Exception # AsyncValidatorInvokedSynchrouslyException

            if first:
                first = False
                try:
                    propValue = self.PropertyFunc(context.instance_to_validate)
                except TypeError:  # FIXME [x]: Checked this try/except
                    raise TypeError(f"TypeError occurred when executing rule for '{self.Expression.lambda_to_string}'. If this property can be None you should add a null check using a when condition")

            valid: bool = await component.ValidateAsync(context, propValue, useAsync)
            if not valid:
                self.PrepareMessageFormatterForValidationError(context, propValue)
                failure = self.CreateValidationError(context, propValue, component)
                context.Failures.append(failure)

            if len(context.Failures) > total_failures and cascade == CascadeMode.Stop:
                break

        if len(context.Failures) <= total_failures and self.dependent_rules is not None:
            for dependentRule in self.dependent_rules:
                await dependentRule.ValidateAsync(context)

        return None

    def ValidateSync(self, context: ValidationContext[T]) -> None:
        """Synchronous version of 'ValidateAsync' to avoid event loop deadlocks."""
        displayName: None | str = self.get_display_name(context)

        if self.PropertyName is None and displayName is None:
            displayName = ""

        PropertyPath: str = context.PropertyChain.BuildPropertyPath(displayName if not self.PropertyName else self.PropertyName)
        if not context.Selector.CanExecute(self, PropertyPath, context):
            return None

        if self.Condition:
            if not self.Condition(context):
                return None

        first = True
        propValue = None
        cascade = self.CascadeMode
        total_failures = len(context.Failures)

        context.InitializeForPropertyValidator(PropertyPath, self._displayNameFunc, self.PropertyName)

        for component in self.Components:
            context.MessageFormatter.Reset()

            if not component.InvokeCondition(context):
                continue

            if first:
                first = False
                try:
                    propValue = self.PropertyFunc(context.instance_to_validate)
                except TypeError:
                    raise TypeError(f"TypeError occurred when executing rule for '{self.Expression.lambda_to_string}'. If this property can be None you should add a null check using a when condition")

            valid: bool = component.ValidateSync(context, propValue)
            if not valid:
                self.PrepareMessageFormatterForValidationError(context, propValue)
                failure = self.CreateValidationError(context, propValue, component)
                context.Failures.append(failure)

            if len(context.Failures) > total_failures and cascade == CascadeMode.Stop:
                break

        if len(context.Failures) <= total_failures and self.dependent_rules is not None:
            for dependentRule in self.dependent_rules:
                dependentRule.ValidateSync(context)
        return None

    def AddDependentRules(self: IValidationRuleInternal[T], rules: IEnumerable[IValidationRuleInternal[T]]) -> None:
        if self.dependent_rules is None:
            self.dependent_rules = []
        self.dependent_rules.extend(rules)
