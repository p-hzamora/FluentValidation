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

import inspect
from typing import Any, Callable, TYPE_CHECKING, overload

from fluent_validation.enums import ApplyConditionTo, CascadeMode, Severity as _Severity
from fluent_validation.IValidationContext import ValidationContext
from fluent_validation.MemberInfo import MemberInfo


if TYPE_CHECKING:
    from fluent_validation.syntax import (  # noqa: F401
        IRuleBuilderOptions,
        IRuleBuilderInitial,
        IRuleBuilder,
        IRuleBuilderInternal,
        IRuleBuilderOptionsConditions,
    )
    from .IValidationRule import IValidationRule
    from fluent_validation.syntax import IRuleBuilderInitialCollection
    from fluent_validation.ICollectionRule import ICollectionRule

from fluent_validation.internal.ExtensionInternal import ExtensionsInternal


class DefaultValidatorOptions[T, TProperty]:
    @overload
    def configure(ruleBuilder: IRuleBuilderInitial[T, TProperty], configurator: Callable[[IValidationRule[T, TProperty]], None]) -> IRuleBuilderInitial[T, TProperty]:
        """
        Configures the rule.

        Attribute
        -

        - "ruleBuilder"
        - "configurator" Action to configure the object.
        """
        ...

    @overload
    def configure(ruleBuilder: IRuleBuilderOptions[T, TProperty], configurator: Callable[[IValidationRule[T, TProperty]], None]) -> IRuleBuilderOptions[T, TProperty]:
        """
            Configures the rule.

        Attribute
        -

            - "ruleBuilder"
            - "configurator" Action to configure the object.
        """
        ...

    @overload
    def configure[T, TElement](ruleBuilder: IRuleBuilderInitialCollection[T, TElement], configurator: Callable[[ICollectionRule[T, TElement]], None]) -> IRuleBuilderInitialCollection[T, TElement]:
        """
            Configures the rule object.
            -

        - "ruleBuilder"
            - "configurator" Action to configure the object.

        """
        ...

    def configure[T, TElement](ruleBuilder: IRuleBuilderInitialCollection[T, TElement], configurator: Callable[[ICollectionRule[T, TElement]], None]) -> IRuleBuilderInitialCollection[T, TElement]:
        """
            Configures the rule object.
            -

        - "ruleBuilder"
            - "configurator" Action to configure the object.

        """
        configurator(ruleBuilder.configurable(ruleBuilder))
        return ruleBuilder

    @overload
    @staticmethod
    def configurable(ruleBuilder: IRuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]: ...

    @overload
    @staticmethod
    def configurable[TCollectionElement](ruleBuilder: IRuleBuilderInitialCollection[T, TCollectionElement]) -> ICollectionRule[T, TCollectionElement]: ...

    @staticmethod
    def configurable(ruleBuilder: IRuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    # FIXME [x]: the type of 'ruleBuilder' used to be 'IRuleBuilderInitial' and it should return the same
    def cascade(ruleBuilder: IRuleBuilder[T, TProperty], cascadeMode: CascadeMode) -> IRuleBuilderInitial[T, TProperty]:
        """
        Specifies the cascade mode for failures.
        If set to cref="CascadeMode.Stop" then execution of the rule will stop once the first validator in the chain fails.
        If set to cref="CascadeMode.Continue" then all validators in the chain will execute regardless of failures.
        """
        ruleBuilder.configurable(ruleBuilder).CascadeMode = cascadeMode
        return ruleBuilder

    @overload
    def with_message(ruleBuilder: IRuleBuilderOptions[T, TProperty], errorMessage: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilderOptions[T, TProperty], errorMessage: Callable[[T], str]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilderOptions[T, TProperty], errorMessage: Callable[[T, TProperty], str]) -> IRuleBuilderOptions[T, TProperty]: ...

    def with_message(ruleBuilder: IRuleBuilderOptions[T, TProperty], errorMessage: str | Callable[[T], str] | Callable[[T, TProperty], str]) -> IRuleBuilderOptions[T, TProperty]:
        """
        Specifies a custom error message to use when validation fails.
        Only applies to the rule that directly precedes it.

        This method supports three different ways to specify error messages:

        1. **Static string message**: A simple string that will be used as-is
        2. **Dynamic message with instance**: A function that takes the instance being validated
           and returns a localized message string
        3. **Dynamic message with instance and property**: A function that takes both the instance
           being validated and the property value, returning a localized message string

        Args:
            ruleBuilder (IRuleBuilderOptions[T, TProperty]): The current rule builder
            errorMessage (str | Callable[[T], str] | Callable[[T, TProperty], str]):
                The error message to use. Can be:
                - str: A static error message
                - Callable[[T], str]: Function taking instance, returning message
                - Callable[[T, TProperty], str]: Function taking instance and property value, returning message

        Returns:
            IRuleBuilderOptions[T, TProperty]: The rule builder options with the custom error message applied

        ## Available Placeholders

        When using string messages, you can include placeholders that will be automatically replaced:

        ### Common Placeholders (available for all validators):
        - `{PropertyName}` - Name of the property being validated
        - `{PropertyValue}` - Current value of the property
        - `{PropertyPath}` - The full path of the property

        ### Validator-Specific Placeholders:

        **Comparison Validators** (`equal`, `not_equal`, `less_than`, `greater_than`, etc.):
        - `{ComparisonValue}` - Value being compared against
        - `{ComparisonProperty}` - Name of the property being compared against (if any)

        **Length Validators** (`length`, `min_length`, `max_length`):
        - `{min_length}` - Minimum length
        - `{max_length}` - Maximum length
        - `{total_length}` - Number of characters entered

        **Range Validators** (`inclusive_between`, `exclusive_between`):
        - `{From}` - Lower bound of the range
        - `{To}` - Upper bound of the range

        **Regular Expression Validator** (`matches`):
        - `{RegularExpression}` - Regular expression that was not matched

        **Precision/Scale Validator** (`precision_scale`):
        - `{ExpectedPrecision}` - Expected precision
        - `{ExpectedScale}` - Expected scale
        - `{Digits}` - Total number of digits in the property value
        - `{ActualScale}` - Actual scale of the property value

        Examples:
            >>> # Static message
            >>> rule.with_message("This field is required")

            >>> # Static message with placeholders
            >>> rule.with_message("'{PropertyName}' should be between {min_length} and {max_length} characters")

            >>> # Dynamic message using instance
            >>> rule.with_message(lambda person: f"Name is required for {person.title}")

            >>> # Dynamic message using instance and property value
            >>> rule.with_message(lambda person, age: f"Age {age} is invalid for {person.name}")
        """
        if callable(errorMessage):
            n_params = len(inspect.signature(errorMessage).parameters)

            # TODOM [x]: Check why 'instance_to_validate' is not detected by python's IDE
            if n_params == 1:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, val: errorMessage(None if ctx is None else ctx.instance_to_validate))
            elif n_params == 2:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, value: errorMessage(None if ctx is None else ctx.instance_to_validate, value))
        elif isinstance(errorMessage, str):
            DefaultValidatorOptions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
        else:
            raise AttributeError

        return ruleBuilder

    # FIXME [x]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def WithErrorCode(rule: IRuleBuilderOptions[T, TProperty], errorCode: str) -> IRuleBuilderOptions[T, TProperty]:
        rule.configurable(rule).Current.ErrorCode = errorCode
        return rule

    # FIXME [x]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def when(rule: IRuleBuilderOptions[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilderOptions[T, TProperty]:
        """
        Specifies a condition limiting when the validator should run.
        The validator will only be executed if the result of the predicate returns True.

        Args:
            rule (IRuleBuilderOptions[T, TProperty]): The current rule.
            predicate (Callable[[T], bool]): A function that specifies a condition for when the validator should run.
            applyConditionTo (ApplyConditionTo, optional): Whether the condition should be applied to the current rule or all rules in the chain. Defaults to ApplyConditionTo.AllValidators.

        Returns:
            IRuleBuilderOptions[T, TProperty]: The rule builder options with the condition applied.
        """
        return rule._When(lambda x, ctx: predicate(x), applyConditionTo)

    def _When(
        rule: IRuleBuilderOptions[T, TProperty],
        predicate: Callable[[T, ValidationContext[T]], bool],
        applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators,
    ) -> IRuleBuilderOptions[T, TProperty]:
        # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
        rule.configurable(rule).ApplyCondition(lambda ctx: predicate(ctx.instance_to_validate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
        return rule

    # FIXME [x]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def unless(rule: IRuleBuilderOptions[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilderOptions[T, TProperty]:
        return rule._Unless(lambda x, ctx: predicate(x), applyConditionTo)

    # FIXME [x]: the type of 'rule' used to be 'IRuleBuilder' and it should return the same
    def _Unless(
        rule: IRuleBuilderOptions[T, TProperty], predicate: Callable[[T, ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators
    ) -> IRuleBuilderOptions[T, TProperty]:
        return rule._When(lambda x, ctx: not predicate(x, ctx), applyConditionTo)

    #   def unless(
    #        rule: IRuleBuilderOptionsConditions[T, TProperty], predicate: Callable[[T, ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators
    #    ) -> IRuleBuilderOptionsConditions[T, TProperty]:
    #        return rule.when(lambda x, ctx: not predicate(x, ctx), applyConditionTo)

    #     public static IRuleBuilderOptions[T, TProperty] WhenAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
    #     }

    #     public static IRuleBuilderOptionsConditions[T, TProperty] WhenAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.WhenAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
    #     }

    #     public static IRuleBuilderOptions[T, TProperty] WhenAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
    #         Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo);
    #         return rule;
    #     }

    #     public static IRuleBuilderOptionsConditions[T, TProperty] WhenAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
    #         Configurable(rule).ApplyAsyncCondition((ctx, ct) => predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx), ct), applyConditionTo);
    #         return rule;
    #     }

    #     public static IRuleBuilderOptions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
    #     }

    #     public static IRuleBuilderOptionsConditions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.UnlessAsync((x, ctx, ct) => predicate(x, ct), applyConditionTo);
    #     }

    #     public static IRuleBuilderOptions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo);
    #     }

    #     public static IRuleBuilderOptionsConditions[T, TProperty] UnlessAsync(rule:IRuleBuilderOptionsConditions[T, TProperty], Callable<T, ValidationContext[T], CancellationToken, Task<bool>> predicate, ApplyConditionTo applyConditionTo = ApplyConditionTo.AllValidators) {
    #         return rule.WhenAsync(async (x, ctx, ct) => !await predicate(x, ctx, ct), applyConditionTo);
    #     }

    # FIXME [x]: the type of rule would be 'IRuleBuilderInitialCollection'
    def where[TCollectionElement](rule: IRuleBuilderInitialCollection[T, TCollectionElement], predicate: Callable[[TCollectionElement], bool]) -> IRuleBuilderInitialCollection[T, TCollectionElement]:
        # This overload supports RuleFor().SetCollectionValidator() (which returns IRuleBuilderOptions<T, IEnumerable<TElement>>)
        rule_configurable: ICollectionRule = rule.configurable(rule)
        rule_configurable.Filter = predicate
        return rule

    @overload
    def with_name(rule: IRuleBuilderOptions[T, TProperty], nameProvider: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_name(rule: IRuleBuilderOptions[T, TProperty], nameProvider: Callable[[T], str]) -> IRuleBuilderOptions[T, TProperty]: ...  # (?<!#)\s+IRuleBuilderOptions[T, TProperty]

    def with_name(rule: IRuleBuilderOptions[T, TProperty], nameProvider: str | Callable[[T], str]) -> IRuleBuilderOptions[T, TProperty]:
        if callable(nameProvider):

            def _lambda(context: ValidationContext[T]):
                instance = context.instance_to_validate if context else None
                return nameProvider(instance)

            # Must use null propagation here.
            # The MVC clientside validation will try and retrieve the name, but won't
            # be able to to so if we've used this overload of WithName.
            rule.configurable(rule).SetDisplayName(_lambda)
        else:
            rule.configurable(rule).SetDisplayName(nameProvider)
        return rule

    @overload
    def override_property_name(rule: IRuleBuilderOptions[T, TProperty], propertyName: str) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def override_property_name(rule: IRuleBuilderOptions[T, TProperty], propertyName: Callable[[T], object]) -> IRuleBuilderOptions[T, TProperty]: ...

    def override_property_name(rule: IRuleBuilderOptions[T, TProperty], propertyName: Callable[[T], object]) -> IRuleBuilderOptions[T, TProperty]:
        if callable(propertyName):
            member = MemberInfo(propertyName)
            if member is None:
                raise Exception("Must supply a MemberExpression when calling override_property_name")
            return rule.override_property_name(member.Name)

        # Allow str.Empty as this could be a model-level rule.
        if propertyName is None:
            raise Exception("A 'propertyName' must be specified when calling override_property_name.")
        rule.configurable(rule).PropertyName = propertyName
        return rule

    @overload
    def with_state(rule: IRuleBuilderOptions[T, TProperty], stateProvider: Callable[[T], object]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_state(rule: IRuleBuilderOptions[T, TProperty], stateProvider: Callable[[T, TProperty], object]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_state(rule: IRuleBuilderOptions[T, TProperty], stateProvider: Callable[[T, TProperty, ValidationContext[T]], object]) -> IRuleBuilderOptions[T, TProperty]: ...

    def with_state(rule: IRuleBuilderOptions[T, TProperty], stateProvider) -> IRuleBuilderOptions[T, TProperty]:
        """
            Specifies custom state that should be stored alongside the validation message when validation fails for this rule.

        Args:
                - rule:IRuleBuilderOptions
                - stateProvider
        """
        n_params = len(inspect.signature(stateProvider).parameters)

        if n_params == 1:
            wrapper: Callable[[ValidationContext[T]], Any] = lambda ctx, _: stateProvider(ctx.instance_to_validate)  # noqa: E731

        elif n_params == 2:
            wrapper: Callable[[ValidationContext[T, TProperty]], Any] = lambda ctx, val: stateProvider(ctx.instance_to_validate, val)  # noqa: E731

        elif n_params == 3:
            wrapper: Callable[[ValidationContext[T, TProperty]], Any] = lambda ctx, val: stateProvider(ctx.instance_to_validate, val, ctx)  # noqa: E731

        rule.configurable(rule).Current.CustomStateProvider = wrapper
        return rule

    @overload
    def with_severity(rule: IRuleBuilderOptions[T, TProperty], severityProvider: _Severity) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_severity(rule: IRuleBuilderOptions[T, TProperty], severityProvider: Callable[[T], _Severity]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_severity(rule: IRuleBuilderOptions[T, TProperty], severityProvider: Callable[[T, TProperty], _Severity]) -> IRuleBuilderOptions[T, TProperty]: ...
    @overload
    def with_severity(rule: IRuleBuilderOptions[T, TProperty], severityProvider: Callable[[T, TProperty, ValidationContext[T]], _Severity]) -> IRuleBuilderOptions[T, TProperty]: ...

    def with_severity(rule: IRuleBuilderOptions[T, TProperty], severityProvider: _Severity | Callable[[T, TProperty, ValidationContext[T]], _Severity]) -> IRuleBuilderOptions[T, TProperty]:
        """Specifies custom severity that should be stored alongside the validation message when validation fails for this rule."""

        def SeverityProvider(ctx: ValidationContext[T], value: TProperty) -> _Severity:
            match len(inspect.signature(severityProvider).parameters):
                case 1:
                    return severityProvider(ctx.instance_to_validate)
                case 2:
                    return severityProvider(ctx.instance_to_validate, value)
                case 3:
                    return severityProvider(ctx.instance_to_validate, value, ctx)
                case _:
                    raise ValueError

        if severityProvider is None:
            ExtensionsInternal.Guard(severityProvider, "A lambda expression must be passed to WithSeverity", severityProvider)

        if isinstance(severityProvider, _Severity):
            rule.configurable(rule).Current.SeverityProvider = lambda a, b: severityProvider
            return rule

        rule.configurable(rule).Current.SeverityProvider = SeverityProvider
        return rule


#     public static IRuleBuilderInitialCollection<T, TCollectionElement> OverrideIndexer<T, TCollectionElement>(this IRuleBuilderInitialCollection<T, TCollectionElement> rule, Callable<T, IEnumerable<TCollectionElement>, TCollectionElement, int, str> callback) {
#         # This overload supports RuleFor().SetCollectionValidator() (which returns IRuleBuilderOptions<T, IEnumerable<TElement>>)
#         Configurable(rule).IndexBuilder = callback;
#         return rule;
#     }
# }
