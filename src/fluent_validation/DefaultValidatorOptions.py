from __future__ import annotations

import inspect
from typing import Callable, TYPE_CHECKING, overload

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
    def configure(ruleBuilder: IRuleBuilderInitial[T, TProperty], configurator: Callable[[IValidationRule[T, TProperty]], None]) -> IRuleBuilderOptions[T, TProperty]:
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
    def configurable[TCollectionElement](ruleBuilder: IRuleBuilderInitialCollection[T, TCollectionElement]) -> ICollectionRule[T, TCollectionElement]:
        ...
        # return (ICollectionRule[T, TCollectionElement]) ((IRuleBuilderInternal[T, TCollectionElement]) ruleBuilder).Rule;

    @staticmethod
    def configurable(ruleBuilder: IRuleBuilder[T, TProperty]) -> IValidationRule[T, TProperty]:
        return ruleBuilder.Rule

    # FIXME [ ]: the type of 'ruleBuilder' used to be 'IRuleBuilderInitial' and it should return the same
    def Cascade(ruleBuilder: IRuleBuilder[T, TProperty], cascadeMode: CascadeMode) -> IRuleBuilder[T, TProperty]:
        ruleBuilder.configurable(ruleBuilder).CascadeMode = cascadeMode
        return ruleBuilder

    # public static IRuleBuilderInitialCollection[T, TProperty] Cascade[T, TProperty](this IRuleBuilderInitialCollection[T, TProperty] ruleBuilder, CascadeMode cascadeMode) {
    #     Configurable(ruleBuilder).CascadeMode = cascadeMode;
    #     return ruleBuilder;
    # }

    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: str) -> IRuleBuilder[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: Callable[[T], str]) -> IRuleBuilder[T, TProperty]: ...
    @overload
    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: Callable[[T, TProperty], str]) -> IRuleBuilder[T, TProperty]: ...

    def with_message(ruleBuilder: IRuleBuilder[T, TProperty], errorMessage: str | Callable[[T], str] | Callable[[T, TProperty], str]):
        if callable(errorMessage):
            n_params = len(inspect.signature(errorMessage).parameters)

            # TODOM: Check why 'instance_to_validate' is not detected by python's IDE
            if n_params == 1:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, val: errorMessage(None if ctx is None else ctx.instance_to_validate))
            elif n_params == 2:
                ruleBuilder.configurable(ruleBuilder).Current.set_error_message(lambda ctx, value: errorMessage(None if ctx is None else ctx.instance_to_validate, value))
        elif isinstance(errorMessage, str):
            DefaultValidatorOptions.configurable(ruleBuilder).Current.set_error_message(errorMessage)
        else:
            raise AttributeError

        return ruleBuilder

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def WithErrorCode(rule: IRuleBuilder[T, TProperty], errorCode: str) -> IRuleBuilder[T, TProperty]:
        rule.configurable(rule).Current.ErrorCode = errorCode
        return rule

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def when(rule: IRuleBuilder[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilder[T, TProperty]:
        return rule._When(lambda x, _: predicate(x), applyConditionTo)

    # def when(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T],bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     return rule._When(lambda x, ctx: predicate(x), applyConditionTo)

    def _When(
        rule: IRuleBuilder[T, TProperty],
        predicate: Callable[[T, ValidationContext[T]], bool],
        applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators,
    ) -> IRuleBuilder[T, TProperty]:
        # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
        rule.configurable(rule).ApplyCondition(lambda ctx: predicate(ctx.instance_to_validate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
        return rule

    # def when(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T, ValidationContext[T]], bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     # Default behaviour for when/unless as of v1.3 is to apply the condition to all previous validators in the chain.
    #     rule.Configurable(rule).ApplyCondition(lambda ctx: predicate((T)ctx.InstanceToValidate, ValidationContext[T].GetFromNonGenericContext(ctx)), applyConditionTo)
    #     return rule

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilderOptions' and it should return the same
    def unless(rule: IRuleBuilder[T, TProperty], predicate: Callable[[T], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators) -> IRuleBuilder[T, TProperty]:
        return rule._Unless(lambda x, _: predicate(x), applyConditionTo)

    # def unless(rule:IRuleBuilderOptionsConditions[T, TProperty], predicate:Callable[[T],bool], applyConditionTo:ApplyConditionTo = ApplyConditionTo.AllValidators)->IRuleBuilderOptionsConditions[T, TProperty]:
    #     return rule.unless(lambda x, ctx: predicate(x), applyConditionTo)

    # FIXME [ ]: the type of 'rule' used to be 'IRuleBuilder' and it should return the same
    def _Unless(
        rule: IRuleBuilder[T, TProperty], predicate: Callable[[T, ValidationContext[T]], bool], applyConditionTo: ApplyConditionTo = ApplyConditionTo.AllValidators
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

    #     public static IRuleBuilderInitialCollection<T, TCollectionElement> Where<T, TCollectionElement>(this IRuleBuilderInitialCollection<T, TCollectionElement> rule, Callable<TCollectionElement, bool> predicate) {
    #         # This overload supports RuleFor().SetCollectionValidator() (which returns IRuleBuilderOptions<T, IEnumerable<TElement>>)
    #         Configurable(rule).Filter = predicate;
    #         return rule;
    #     }

    @overload
    def with_name(rule: IRuleBuilder[T, TProperty], nameProvider: str) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]
    @overload
    def with_name(rule: IRuleBuilder[T, TProperty], nameProvider: Callable[[T], str]) -> IRuleBuilder[T, TProperty]: ...  # (?<!#)\s+IRuleBuilderOptions[T, TProperty]

    def with_name(rule: IRuleBuilder[T, TProperty], nameProvider: str | Callable[[T], str]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderOptions[T, TProperty]
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
    def orverride_property_name(rule: IRuleBuilder[T, TProperty], propertyName: str) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]
    @overload
    def orverride_property_name(rule: IRuleBuilder[T, TProperty], propertyName: Callable[[T], object]) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]

    def orverride_property_name(rule: IRuleBuilder[T, TProperty], propertyName: Callable[[T], object]) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderOptions[T, TProperty]
        if callable(propertyName):
            member = MemberInfo(propertyName)
            if member is None:
                raise Exception("Must supply a MemberExpression when calling orverride_property_name")
            return rule.orverride_property_name(member.Name)

        # Allow str.Empty as this could be a model-level rule.
        if propertyName is None:
            raise Exception("A 'propertyName' must be specified when calling orverride_property_name.")
        rule.configurable(rule).PropertyName = propertyName
        return rule

    #     public static IRuleBuilderOptions[T, TProperty] WithState(rule:IRuleBuilderOptions[T, TProperty], Callable<T, object> stateProvider) {
    #         var wrapper = new Callable<ValidationContext[T], TProperty, object>((ctx, _) => stateProvider(ctx.InstanceToValidate));
    #         Configurable(rule).Current.CustomStateProvider = wrapper;
    #         return rule;
    #     }

    #     public static IRuleBuilderOptions[T, TProperty] WithState(rule:IRuleBuilderOptions[T, TProperty], Callable<T, TProperty, object> stateProvider) {

    #         var wrapper = new Callable<ValidationContext[T], TProperty, object>((ctx, val) => {
    #             return stateProvider(ctx.InstanceToValidate, val);
    #         });

    #         Configurable(rule).Current.CustomStateProvider = wrapper;
    #         return rule;
    #     }

    @overload
    def with_severity(rule: IRuleBuilder[T, TProperty], severityProvider: _Severity) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]:
    @overload
    def with_severity(rule: IRuleBuilder[T, TProperty], severityProvider: Callable[[T], _Severity]) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]:
    @overload
    def with_severity(rule: IRuleBuilder[T, TProperty], severityProvider: Callable[[T, TProperty], _Severity]) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]:
    @overload
    def with_severity(
        rule: IRuleBuilder[T, TProperty], severityProvider: Callable[[T, TProperty, ValidationContext[T]], _Severity]
    ) -> IRuleBuilder[T, TProperty]: ...  # IRuleBuilderOptions[T, TProperty]:

    def with_severity(
        rule: IRuleBuilder[T, TProperty], severityProvider: _Severity | Callable[[T, TProperty, ValidationContext[T]], _Severity]
    ) -> IRuleBuilder[T, TProperty]:  # IRuleBuilderOptions[T, TProperty]:
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
